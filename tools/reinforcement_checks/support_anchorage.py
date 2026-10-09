"""Positive support orchestration; resistant equations exclusively in Concretopy."""
from copy import deepcopy
from dataclasses import asdict
from bar_scaling import classify_bond, locate_references, api_provenance, DEPTH_RULE
from support_geometry import SupportGeometry
from support_correction import (configuration_from_bars, check_longitudinal, transverse_fit,
    extension_candidates, redistribution_candidates, preserved_original_reinforcement)
from support_alternatives import evaluate_configuration

LAST_RULE = 'engineer_confirmed_intermediate_support_last_section_moment_v1'
BASIC_RULE = 'engineer_confirmed_intermediate_support_positive_max_basic_lb_v1'
BASE_RULE = 'engineer_confirmed_intermediate_support_base_penetration_30cm_v1'
LONG_RULE = 'engineer_confirmed_intermediate_support_scaling_like_checks_v1'


def termination(bar, geometry, penetration):
    if penetration['continuity']=='CONTINUES_THROUGH_SUPPORT':
        return 'CONTINUES_THROUGH_SUPPORT'
    explicit=bar.get('termination_by_side',{}).get(geometry.support_side)
    if explicit in ('STRAIGHT','HOOK','UNKNOWN'):
        return explicit
    if bar.get('shape')=='straight':
        return 'STRAIGHT'
    bend=bar.get('end_bend') or {}
    if str(bend.get('side','')).upper()==geometry.support_side:
        return 'HOOK'
    return 'UNKNOWN'


def terminal_section(diagram, geometry):
    """Terminal in direction of support: first x for LEFT, last x for RIGHT."""
    if diagram is None or not diagram.provenance:
        raise ValueError('moment_source_unresolved')
    point=deepcopy(diagram.points[0 if geometry.support_side=='LEFT' else -1])
    if point.get('value_knm') is None or any(m is None for m in diagram.ms):
        raise ValueError('terminal_moment_or_span_maximum_unresolved')
    point.update(rule=LAST_RULE, provenance={'point':deepcopy(point), 'diagram':diagram.provenance,
        'orientation_confirmation':'Engineer confirmed terminal section in direction of support, without force mirroring'})
    return point


def _control(geometry, endpoint, reference, required, rule):
    if reference is None or required is None:
        return {'rule':rule,'passes':None,'reference_x_m':reference,'required_length_cm':required,
                'available_length_cm':None,'required_end_position_m':None}
    available=geometry.distance_cm(reference,endpoint)
    return {'rule':rule,'reference_x_m':reference,'required_length_cm':required,
        'available_length_cm':available,'required_end_position_m':geometry.required_end(reference,required),
        'passes':None if available<0 else available>=required,
        'provenance':{'geometry':geometry.as_dict(),'calculation':'oriented distance from reference to documentary end'}}


def _complete_pass(states):
    return None if not states or None in states else all(states)


def check_support(context, bars, diagram, api, *, geometry, shear=None, generate_corrections=True):
    """END delegates existing workflow; INTERMEDIATE uses A/C, never B1/B2.

    Transverse section supplied for longitudinal calculation may be an explicit
    audit hypothesis. Its use does not resolve documentary transverse geometry.
    """
    if not isinstance(geometry,SupportGeometry):
        raise TypeError('explicit_support_geometry_required')
    out={'support_side':geometry.support_side,'support_type':geometry.support_type,
        'geometry':geometry.as_dict(),'force_data_resolved':False,'flexural_demand_resolved':False,
        'required_area_cm2':None,'effective_area_at_face_cm2':None,'area_sufficient':None,
        'longitudinal_bars':[],'anchorage_mode':None,'anchorage_reference':geometry.internal_face_m,
        'basic_lb_cm':None,'lb_min_cm':None,'lb_nec_cm':None,'available_penetration_cm':None,
        'base_penetration_check':None,'zero_moment_check':None,'full_utilization_check':None,
        'longitudinal_anchorage_passes':None,
        'transverse_geometry_resolved':context.get('transverse_geometry_resolved') is True,
        'node_interferences_verified':context.get('node_interferences_verified') is True,
        'support_verified':None,'correction_required':None,'corrections':[],
        'selected_solution':None,'ready_for_detailing':False,'diagnostics':[],'concretopy':{},'provenance':deepcopy(context.get('provenance'))}
    try:
        reaching=[]
        for bar in bars:
            if bar.get('function')!='positive' or bar.get('face')!='lower':
                continue
            penetration=geometry.penetration(bar)
            record={'bar':deepcopy(bar),**penetration,'termination_type':termination(bar,geometry,penetration),
                    'area_cm2':bar['bars']*api.Barra(bar['diameter_mm']).area_cm2,
                    'area_anchored_cm2':None}
            out['longitudinal_bars'].append(record)
            if penetration['area_presente_na_face']:
                reaching.append(bar)
        if not reaching:
            raise ValueError('no_positive_bars_reaching_internal_face')
        configuration=configuration_from_bars(reaching,geometry.internal_face_m,'EXISTENTE')
        out['composition_at_face']=configuration
        if geometry.support_type=='END':
            local=deepcopy(context)
            local.update(support_side=geometry.support_side.lower(),support_type='extremo',
                support_length_cm=geometry.support_width_cm)
            existing=evaluate_configuration(local,configuration,api)
            out['end_support_result']=existing
            out['force_data_resolved']=bool(existing['states'])
            out['flexural_demand_resolved']=existing['complete']
            if existing['metrics']:
                m=existing['metrics']
                out.update(required_area_cm2=m['As_support_cm2'],effective_area_at_face_cm2=m['As_effective_cm2'],
                    basic_lb_cm=m['lb_cm'],lb_min_cm=m['lb_min_cm'],lb_nec_cm=m['lb_nec_cm'],
                    available_penetration_cm=m['lb_ef_cm'],anchorage_mode='END_LB_NEC',
                    area_sufficient=existing['anchorage']['area_suficiente'])
            out['longitudinal_anchorage_passes']=existing['passes']
            if existing['passes'] is False and generate_corrections and context.get('correction_search'):
                from support_correction import correction_workflow
                local['support_reference_x_m']=geometry.internal_face_m
                local.setdefault('extension_target_x_m',geometry.required_end(geometry.internal_face_m,geometry.support_width_cm-context['cover_cm']))
                workflow=correction_workflow(local,bars,diagram,api,redistribution_search=context['correction_search'])
                out['end_correction_workflow']=workflow
                out['corrections']=workflow['extensions']+workflow['redistributions']
            # Staple scenario remains an explicit caller decision through staple_workflow.
        else:
            if context.get('horizontal') is not True or context.get('sliding_formwork') is not False:
                raise ValueError('unsupported_or_unresolved_bond_scope')
            last=terminal_section(diagram,geometry)
            out['last_span_section']=last
            out['force_data_resolved']=True
            positive=last['value_knm']>0
            maximum=float(max(diagram.ms))
            if maximum<=0:
                raise ValueError('positive_span_maximum_unresolved')
            out['classification']='INTERMEDIATE_WITH_POSITIVE_MOMENT' if positive else 'INTERMEDIATE_WITHOUT_POSITIVE_MOMENT'
            out['classification_rule']='engineer_confirmed_intermediate_support_no_positive_moment_v1'
            out['last_section_is_positive_maximum']=positive and last['value_knm']==maximum
            sec=api.SecaoRetangular(**context['section'])
            concrete,steel=api.Concreto(context['fck_mpa']),api.Aco(context['fyk_mpa'])
            co={k:context[k] for k in ('gamma_f','gamma_c','gamma_s')}
            layers=tuple(api.CamadaArmaduraLongitudinal(e['count'],api.Barra(e['diameter_mm']),e['d_cm']) for e in configuration['layers'])
            flex=api.verificar_flexao_viga_retangular(sec,concrete,steel,layers,**co)
            out['concretopy']['flexure']=asdict(flex)
            if not flex.hipoteses_validas or not flex.ductilidade_atendida:
                raise ValueError('concretopy_flexure_invalid')
            call=dict(secao=sec,concreto=concrete,aco=steel,camadas_apoio=layers,tipo_apoio='intermediario',
                mk_apoio_kncm=max(0,last['value_knm'])*100,vk_apoio_kn=0,
                mk_positivo_max_vao_kncm=maximum*100,mk_negativo_apoio_kncm=context['mk_negative_support_kncm'],
                d_vao_cm=context['d_span_cm'],nd_tracao_kn=context['nd_tracao_kn'],**co)
            if context.get('section_span'):
                call['secao_vao']=api.SecaoRetangular(**context['section_span'])
            for key in ('d_linha_apoio_cm','d_linha_vao_cm'):
                if context.get(key) is not None: call[key]=context[key]
            demand=api.calcular_armadura_positiva_apoio(**call)
            out['concretopy']['support_demand']=asdict(demand)
            for name in ('condicao_a','condicao_b','condicao_c'):
                condition=getattr(demand,name)
                out['concretopy']['support_demand'][name]['aplicavel']=condition.aplicavel
                out['concretopy']['support_demand'][name]['as_cm2']=condition.as_cm2
            out['concretopy']['demand_call_provenance']={'api':api_provenance(api.calcular_armadura_positiva_apoio),
                'moment':'/last_span_section','vk_apoio_kn':{'value':0,'meaning':'unused API placeholder; criterion B inapplicable'},
                'span_context':deepcopy(context),'criteria':'A if positive; C via Concretopy; B inapplicable'}
            out.update(flexural_demand_resolved=True,required_area_cm2=demand.as_necessaria_cm2,
                effective_area_at_face_cm2=flex.as_total_cm2,area_sufficient=flex.as_total_cm2>=demand.as_necessaria_cm2)
            al=None; zero=None; full=None
            if not positive:
                terminal_x=last['x_m']
                zero=locate_references(diagram,0,geometry.support_side.lower(),terminal_x)
                full=locate_references(diagram,flex.mk_equivalente_kncm/100,geometry.support_side.lower(),terminal_x)
                out['moment_references']={'zero':zero,'full_utilization':full}
                out['d_for_al']={'d_cm':flex.d_equivalente_cm,'rule':DEPTH_RULE,
                    'composition':'/composition_at_face','event_x_m':geometry.internal_face_m,
                    'provenance':'Concretopy tension centroid on span side immediately before entry at internal face; unchanged composition until each analyzed end required'}
                if (shear and shear.get('status')=='resolved' and context.get('al_scope_confirmed') is True
                    and {item.get('envelope') for item in shear.get('series',[])}=={'max','min'}):
                    response=api.calcular_al(concreto=concrete,b_cm=sec.bw,d_cm=flex.d_equivalente_cm,
                        vk_abs_kn=shear['Vk_used_kn'],gamma_f=co['gamma_f'],gamma_c=co['gamma_c'])
                    al=response.al_cm
                    out['concretopy']['al']=asdict(response)
                    out['shear_for_al']=deepcopy(shear)
                else:
                    out['diagnostics'].append('shear_for_al_or_equivalent_event_scope_unresolved')
            results=[]
            for record in out['longitudinal_bars']:
                if not record['area_presente_na_face']: continue
                bar=record['bar']; phi=bar['diameter_mm']; end=record['documentary_end_x_m']
                phi_cm=phi/10
                ten_phi_cm=10*phi_cm
                record['ten_phi_cm']={'value':ten_phi_cm,'provenance':'10 * interrupted/anchored bar diameter_mm / 10; lengths in cm'}
                bond=classify_bond(sec.h,sec.h-bar['d_cm']);record['bond_condition']=bond
                area=api.Barra(phi).area_cm2
                anchor=api.calcular_ancoragem(concreto=concrete,aco=steel,bitola_mm=phi,
                    as_calculada_cm2=area,as_efetiva_cm2=area,condicoes=api.CondicoesAncoragem(bond['boa_aderencia']),
                    gamma_c=co['gamma_c'],gamma_s=co['gamma_s'])
                record.update(basic_lb_cm=anchor.lb_cm,lb_min_cm=anchor.lb_min_cm,
                    anchorage_basic_result=asdict(anchor),alpha=1.0,
                    provenance_anchorage=api_provenance(api.calcular_ancoragem))
                # lb_nec is audit only; global reduction allocation only unambiguous
                # for uniform diameter AND bond. Never governs the basic-lb case.
                uniform=len({b['diameter_mm'] for b in reaching})==1 and len({classify_bond(sec.h,sec.h-b['d_cm'])['boa_aderencia'] for b in reaching})==1
                if uniform and record['comprimento_penetracao_cm']==0 and demand.as_necessaria_cm2<=flex.as_total_cm2:
                    reduced=api.calcular_ancoragem(concreto=concrete,aco=steel,bitola_mm=phi,
                        as_calculada_cm2=demand.as_necessaria_cm2,as_efetiva_cm2=flex.as_total_cm2,
                        condicoes=api.CondicoesAncoragem(bond['boa_aderencia']),
                        gamma_c=co['gamma_c'],gamma_s=co['gamma_s'])
                    record['lb_nec_cm']=reduced.lb_nec_cm
                    record['anchorage_audit_result']=asdict(reduced)
                elif uniform and record['comprimento_penetracao_cm']>0:
                    reduced=api.verificar_ancoragem_positiva_apoio(concreto=concrete,aco=steel,bitola_mm=phi,
                        as_calculada_cm2=demand.as_necessaria_cm2,as_efetiva_cm2=flex.as_total_cm2,
                        condicoes=api.CondicoesAncoragem(bond['boa_aderencia']),
                        comprimento_disponivel_cm=record['comprimento_penetracao_cm'],gancho_valido=False,
                        gamma_c=co['gamma_c'],gamma_s=co['gamma_s'])
                    record['lb_nec_cm']=reduced.lb_nec_cm
                    record['anchorage_audit_result']=asdict(reduced)
                else: record['lb_nec_cm']=None
                controls={}
                if positive:
                    out['anchorage_mode']='INTERMEDIATE_BASIC_LB' if out['last_section_is_positive_maximum'] else 'INTERMEDIATE_POSITIVE_REDUCTION_UNRESOLVED'
                    controls['basic_lb']=_control(geometry,end,geometry.internal_face_m,anchor.lb_cm,BASIC_RULE)
                    if not out['last_section_is_positive_maximum']:
                        controls['basic_lb']['passes']=None
                        out['diagnostics'].append('intermediate_positive_nonmaximum_length_rule_unresolved')
                else:
                    out['anchorage_mode']='INTERMEDIATE_THREE_LONGITUDINAL_CONTROLS'
                    controls['base']=_control(geometry,end,geometry.internal_face_m,max(ten_phi_cm,min(geometry.support_width_cm,30)),BASE_RULE)
                    controls['base']['normative_minimum_provenance']='engineer_provided_normative_minimum_10phi; clause not audited'
                    controls['zero']=_control(geometry,end,zero['selected_x_nec_m'],None if al is None else al+ten_phi_cm,LONG_RULE)
                    if full['diagnostics']==['no_valid_crossing','remaining_sufficient_entire_branch']:
                        controls['full_utilization']={'rule':LONG_RULE,'status':'NOT_APPLICABLE',
                            'passes':True,'required_end_position_m':None,'reference_x_m':None,
                            'reason':'Capacity exceeds entire branch; no full utilization point in sampled domain',
                            'provenance':'/moment_references/full_utilization'}
                    else:
                        controls['full_utilization']=_control(geometry,end,full['selected_x_nec_m'],None if al is None else al+anchor.lb_cm,LONG_RULE)
                    for key in ('base','zero','full_utilization'):
                        out[{'base':'base_penetration_check','zero':'zero_moment_check','full_utilization':'full_utilization_check'}[key]]=controls[key]
                if record['termination_type']!='STRAIGHT':
                    record['termination_diagnostic']='intermediate_hook_continuity_or_unknown_rule_unresolved'
                    for c in controls.values(): c['passes']=None
                    out['diagnostics'].append(record['termination_diagnostic'])
                record['controls']=controls
                record['passes']=_complete_pass([c['passes'] for c in controls.values()])
                record['area_anchored_cm2']=record['area_cm2'] if record['passes'] is True else 0 if record['passes'] is False else None
                ends=[(k,c['required_end_position_m']) for k,c in controls.items() if c.get('required_end_position_m') is not None]
                if ends and record['passes'] is not None:
                    farthest=max(geometry.distance_cm(geometry.internal_face_m,x) for _,x in ends)
                    record['required_end_position_m']=geometry.required_end(geometry.internal_face_m,max(0,farthest))
                    record['governing_rules']=[k for k,x in ends if geometry.distance_cm(geometry.internal_face_m,x)==farthest]
                results.append(record['passes'])
            if not positive:
                for key,field in (('base','base_penetration_check'),('zero','zero_moment_check'),('full_utilization','full_utilization_check')):
                    entries=[(r['bar']['mark'],r['controls'][key]) for r in out['longitudinal_bars'] if r['area_presente_na_face']]
                    positioned=[c for _,c in entries if c.get('required_end_position_m') is not None]
                    representative=max(positioned,key=lambda c:geometry.distance_cm(geometry.internal_face_m,c['required_end_position_m'])) if positioned else entries[0][1]
                    out[field]={**deepcopy(representative),'by_mark':dict(entries),
                        'passes':_complete_pass([c['passes'] for _,c in entries])}
            out['required_end_positions_by_mark']={r['bar']['mark']:r.get('required_end_position_m') for r in out['longitudinal_bars'] if r['area_presente_na_face']}
            out['longitudinal_anchorage_passes']=_complete_pass([out['area_sufficient'],*results])
            anchors=[r for r in out['longitudinal_bars'] if r['area_presente_na_face']]
            out['basic_lb_cm']=max(r['basic_lb_cm'] for r in anchors)
            out['lb_min_cm']=max(r['lb_min_cm'] for r in anchors)
            out['lb_nec_cm']=max(r['lb_nec_cm'] for r in anchors) if all(r['lb_nec_cm'] is not None for r in anchors) else None
            out['available_penetration_cm']=min(r['comprimento_penetracao_cm'] for r in anchors)
            out['transverse_fit_audit_model']=transverse_fit(context['section'],configuration['layers'],api)
        passed=out['longitudinal_anchorage_passes']
        out['correction_required']=None if passed is None else not passed
        out['support_verified']=_complete_pass([passed,True if out['transverse_geometry_resolved'] else None,
            True if out['node_interferences_verified'] else None])
        out['next_step']='NENHUMA_CORRECAO' if passed is True else 'RESOLVER_PENDENCIAS' if passed is None else 'PROLONGAR_ARMADURA_EXISTENTE'
        if passed is False and generate_corrections and geometry.support_type=='INTERMEDIATE':
            proposed=deepcopy(bars); changes=[]
            for record in out['longitudinal_bars']:
                if record.get('required_end_position_m') is None or record['termination_type']!='STRAIGHT': continue
                needed=record['required_end_position_m']
                if geometry.distance_cm(record['documentary_end_x_m'],needed)<=0: continue
                if geometry.distance_cm(geometry.internal_face_m,needed)>geometry.support_width_cm:
                    out['diagnostics'].append('required_extension_exceeds_support_continuity_rule_unresolved');continue
                target=next(b for b in proposed if b['mark']==record['bar']['mark'])
                target[geometry.bar_endpoint_key]=needed
                target['proposal_geometry']={'source':deepcopy(record['bar']),'rule':'straight_own_bar_extension'}
                changes.append({'mark':target['mark'],'proposed_end_x_m':needed})
            if changes:
                result=check_support(context,proposed,diagram,api,geometry=geometry,shear=shear,generate_corrections=False)
                longitudinal=check_longitudinal(proposed,context,diagram,api)
                preserved=preserved_original_reinforcement(bars,proposed)
                adequate=(result['longitudinal_anchorage_passes'] is True and
                    longitudinal['compatibilidade_flexao_positiva'] is True and preserved is True and
                    result.get('transverse_fit_audit_model',{}).get('cabimento_transversal') is True)
                out['corrections'].append({'origin':'PROLONGAMENTO','changes':changes,'result':result,
                    'longitudinal_compatibility':longitudinal,'original_reinforcement_preserved':preserved,
                    'recomendavel_como_correcao':adequate,'selected':False,'ready_for_detailing':False})
            # Further stages must use reconstructed physical candidates and full regional checks.
            # Missing geometry/continuity never triggers automatic end-support staples.
            adequate=any(c['result']['longitudinal_anchorage_passes'] is True and
                c['longitudinal_compatibility']['compatibilidade_flexao_positiva'] is True
                and c['result'].get('transverse_fit_audit_model',{}).get('cabimento_transversal') is True
                for c in out['corrections'])
            if not adequate:
                _additional_corrections(out,context,bars,diagram,api,geometry,shear)
    except (ValueError,TypeError,KeyError,OverflowError) as error:
        out['diagnostics'].append(str(error))
    return out


def _additional_corrections(out,context,bars,diagram,api,geometry,shear):
    """Existing physical splitting/redistribution generators; no resistant formulas."""
    target=geometry.required_end(geometry.internal_face_m,geometry.support_width_cm-context['cover_cm'])
    def assess(candidate):
        ctx=deepcopy(context)
        if candidate['origin']=='REDISTRIBUICAO':
            peak=diagram.points[diagram.ms.index(max(diagram.ms))]['x_m']
            cfg=configuration_from_bars(candidate['bars'],peak,'span_peak')
            sec=api.SecaoRetangular(**(ctx.get('section_span') or ctx['section']))
            layers=tuple(api.CamadaArmaduraLongitudinal(e['count'],api.Barra(e['diameter_mm']),e['d_cm']) for e in cfg['layers'])
            flex=api.verificar_flexao_viga_retangular(sec,api.Concreto(ctx['fck_mpa']),api.Aco(ctx['fyk_mpa']),layers,
                **{k:ctx[k] for k in ('gamma_f','gamma_c','gamma_s')})
            ctx['d_span_cm']=flex.d_equivalente_cm
            ctx['span_depth_provenance']=asdict(flex)
        result=check_support(ctx,candidate['bars'],diagram,api,geometry=geometry,shear=shear,generate_corrections=False)
        longitudinal=check_longitudinal(candidate['bars'],ctx,diagram,api)
        preserved=preserved_original_reinforcement(bars,candidate['bars']) if candidate['origin']=='PROLONGAMENTO' else None
        fit=result.get('transverse_fit_audit_model',{}).get('cabimento_transversal')
        adequate=result['longitudinal_anchorage_passes'] is True and longitudinal['compatibilidade_flexao_positiva'] is True and fit is True
        if candidate['origin']=='PROLONGAMENTO': adequate=adequate and preserved is True
        return {**candidate,'result':result,'longitudinal_compatibility':longitudinal,
                'original_reinforcement_preserved':preserved,'recomendavel_como_correcao':adequate,
                'ready_for_detailing':False,'selected':False}
    extensions=extension_candidates(bars,geometry.internal_face_m,target,geometry.support_side)
    for candidate in extensions:
        out['corrections'].append(assess(candidate))
    if any(c.get('recomendavel_como_correcao') for c in out['corrections']):
        out['next_step']='PROLONGAR_ARMADURA_EXISTENTE';return
    search=context.get('correction_search')
    if search:
        for candidate in redistribution_candidates(bars,api,context["section"],**search):
            out['corrections'].append(assess(candidate))
        if any(c.get('recomendavel_como_correcao') for c in out['corrections']):
            out['next_step']='REDISTRIBUIR_ARMADURA';return
    out['next_step']='AVALIAR_PROLONGAMENTO_COHERENTE_OU_REDISTRIBUICAO'
    out['diagnostics'].append('no_adequate_straight_correction_in_supplied_geometry_and_search; no automatic intermediate staples')
