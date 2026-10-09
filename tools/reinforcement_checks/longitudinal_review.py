"""Sign/face interpretation and longitudinal review; shared existing engines."""
from copy import deepcopy
from dataclasses import asdict
from moment_diagram import tension_diagram,dec
from flexure_regions import decompose_regions
from support_correction import configuration_from_bars,check_longitudinal
from support_geometry import LongitudinalOrientation,normalize_side
from support_anchorage import _control,_complete_pass
from bar_scaling import locate_references,api_provenance
from termination_event import describe_termination

LAYER_RULE='engineer_confirmed_reinforcement_layer_face_order_v1'
BOND_RULE='engineer_confirmed_negative_beam_reinforcement_poor_bond_v1'
AL_RULE='engineer_confirmed_negative_al_same_as_positive_v1'
END_RULE='engineer_confirmed_negative_reinforcement_span_termination_v1'
TERMINAL_RULE='engineer_confirmed_negative_support_terminal_section_demand_v1'


def negative_support_terminal_demand(diagram,support_side):
    side=normalize_side(support_side);section=1 if side=='LEFT' else 13
    point=deepcopy(diagram.points[0 if side=='LEFT' else -1])
    if point['section']!=section or point.get('value_knm') is None:
        raise ValueError('negative_support_terminal_sample_unresolved')
    return {'support_side':side,'section':section,'x_m':point['x_m'],
        'Msk_signed_knm':point['value_knm'],'negative_demand_knm':max(0,-point['value_knm']),
        'rule':TERMINAL_RULE,'provenance':{'point':point,'diagram':deepcopy(diagram.provenance),
            'selection':'direct S1 for LEFT or S13 for RIGHT; no interpolation/extrapolation or DEPEV transport'}}


def prepare_reinforcement(bars,context,api,*,flexure_sign):
    """Physical centers, never arbitrary d from an undocumented coordinate.

    Explicit layer centers are measured from named face. Automatic positioning
    requires caller provenance confirming documentary order from tension face.
    All physical positions remain fixed when a layer is subsequently removed.
    """
    if flexure_sign not in ('POSITIVE','NEGATIVE'):raise ValueError('unknown_flexure_sign')
    function,face=('positive','lower') if flexure_sign=='POSITIVE' else ('negative','upper')
    selected=deepcopy([b for b in bars if b.get('function')==function])
    if not selected or len({b['mark'] for b in selected})!=len(selected):raise ValueError('missing_or_duplicate_reinforcement')
    section=api.SecaoRetangular(**context['section']); h=section.h
    for b in selected:
        if b.get('face')!=face or not b.get('source'):raise ValueError('reinforcement_face_or_source_unresolved')
        if dec(b['x_start_common'])>=dec(b['x_end_common']):raise ValueError('invalid_longitudinal_interval')
        vector=b.get('layers')
        if not vector or any(type(n)!=int or n<0 for n in vector) or sum(vector)!=b['bars']:raise ValueError('physical_layers_unresolved')
    centers=context.get('layer_centers')
    if centers is not None:
        if not centers:raise ValueError('layer_centers_missing')
        ds={}
        for layer in centers:
            if not layer.get('provenance'):raise ValueError('layer_coordinate_provenance_missing')
            origin=layer['origin']; value=dec(layer['value_cm'])
            if origin=='BOTTOM':y=value
            elif origin=='TOP':y=dec(h)-value
            elif origin=='COMPRESSION_FACE':y=value if flexure_sign=='NEGATIVE' else dec(h)-value
            else:raise ValueError('unknown_vertical_coordinate_origin')
            d=float(y if flexure_sign=='NEGATIVE' else dec(h)-y)
            if not 0<d<h:raise ValueError('invalid_physical_center')
            if layer['documentary_layer'] in ds:raise ValueError('duplicate_documentary_layer')
            ds[layer['documentary_layer']]=d
        if len(set(ds.values()))!=len(ds):raise ValueError('coincident_layers_unresolved')
        order={old:i for i,(old,d) in enumerate(sorted(ds.items(),key=lambda p:-p[1]),1)}
        for b in selected:
            old=deepcopy(b['layers']);new=[0]*len(ds)
            for i,n in enumerate(old,1):
                if n:
                    if i not in order:raise ValueError('missing_layer_center')
                    new[order[i]-1]=n
            b['layers']=new
            b['layer_provenance']={'rule':LAYER_RULE,'original_vector':old,'physical_order':order,'centers':deepcopy(centers)}
        depths=[ds[old] for old in sorted(ds,key=lambda k:order[k])]
    else:
        if not context.get('layer_order_provenance') or context.get('layer_order_basis')!='from_tension_face':
            raise ValueError('layer_order_or_vertical_coordinate_unresolved')
        count=max(len(b['layers']) for b in selected); physical=[]
        for i in range(count):
            phis={b['diameter_mm'] for b in selected if i<len(b['layers']) and b['layers'][i]}
            if len(phis)!=1:raise ValueError('automatic_mixed_diameter_or_missing_layer_position_unresolved')
            physical.append(api.CamadaArmaduraLongitudinal(1,api.Barra(next(iter(phis)))))
        depths=list(api.calcular_alturas_uteis_camadas(section,tuple(physical)))
        order={i:i for i in range(1,count+1)}
        for b in selected:b['layer_provenance']={'rule':LAYER_RULE,'basis':context['layer_order_provenance'],
            'position_api':api_provenance(api.calcular_alturas_uteis_camadas),'documentary_geometry':'layer order only; centers are adopted Concretopy convention, not PDF dimensions'}
    for b in selected:
        b['d_by_layer_cm']=[depths[i] if n else None for i,n in enumerate(b['layers'])]
        populated=[d for d in b['d_by_layer_cm'] if d is not None]
        b['d_cm']=populated[0] if len(populated)==1 else None
        b['flexure_sign']=flexure_sign
        b['vertical_geometry']={'tension_face':'TOP' if flexure_sign=='NEGATIVE' else 'BOTTOM',
            'compression_face':'BOTTOM' if flexure_sign=='NEGATIVE' else 'TOP','d_measured_from':'compression_face'}
    return selected


def composition_capacity(bars,x,context,api,*,flexure_sign):
    cfg=configuration_from_bars(bars,x,'resistant_composition',flexure_sign=flexure_sign)
    section=api.SecaoRetangular(**context['section'])
    layers=tuple(api.CamadaArmaduraLongitudinal(e['count'],api.Barra(e['diameter_mm']),e['d_cm']) for e in cfg['layers'])
    flex=api.verificar_flexao_viga_retangular(section,api.Concreto(context['fck_mpa']),api.Aco(context['fyk_mpa']),layers,
        **{k:context[k] for k in ('gamma_f','gamma_c','gamma_s')})
    return {'composition':cfg,'concretopy':asdict(flex),'MRd_knm':None if flex.mrd_kncm is None else flex.mrd_kncm/100,
        'Mk_equivalent_knm':None if flex.mk_equivalente_kncm is None else flex.mk_equivalente_kncm/100,
        'valid':flex.hipoteses_validas and flex.ductilidade_atendida,
        'provenance':{'flexure_api':api_provenance(api.verificar_flexao_viga_retangular),'context':deepcopy(context)}}


def check_flexure_regions(bars,context,diagram,api,*,flexure_sign,domain=None):
    out={'flexure_sign':flexure_sign,'regions':[],'passes':None,'diagnostics':[],'selected_solution':None}
    try:
        physical=prepare_reinforcement(bars,context,api,flexure_sign=flexure_sign)
        view=tension_diagram(diagram,flexure_sign,domain=domain)
        result=check_longitudinal(physical,context,view,api,flexure_sign=flexure_sign)
        out.update(physical_reinforcement=physical,result=result,
            passes=result['compatibilidade_flexao_positiva' if flexure_sign=='POSITIVE' else 'compatibilidade_flexao_negativa'])
        for region in result['regions']:
            governing=region['governing_demand']
            if region.get('status')=='NOT_APPLICABLE':
                region.update(flexure_sign=flexure_sign,passes=None,not_applicable=True)
                continue
            region.update(flexure_sign=flexure_sign,tension_face='TOP' if flexure_sign=='NEGATIVE' else 'BOTTOM',
                compression_face='BOTTOM' if flexure_sign=='NEGATIVE' else 'TOP',
                first_layer=region['configuration']['layers'][0],passes=region['capacity_sufficient'],
                governing_moment_signed=None if governing is None else governing['value_knm']*(1 if flexure_sign=='POSITIVE' else -1),
                governing_moment_abs=None if governing is None else governing['value_knm'],
                MRd_knm=region['concretopy']['mrd_kncm']/100 if region['concretopy']['mrd_kncm'] is not None else None,
                Mk_equivalent_knm=region['concretopy']['mk_equivalente_kncm']/100 if region['concretopy']['mk_equivalente_kncm'] is not None else None)
            region['utilization']=None if governing is None or not region['Mk_equivalent_knm'] else governing['value_knm']/region['Mk_equivalent_knm']
        out['regions']=result['regions'];out['diagnostics']=[code.replace('flexao_positiva','flexao_negativa') if flexure_sign=='NEGATIVE' else code for code in result['diagnostics']]
        out['provenance']={'original_diagram':diagram.as_dict(),'view':view.as_dict(),'context':deepcopy(context)}
    except (ValueError,TypeError,KeyError,IndexError) as error:out['diagnostics'].append(str(error))
    return out


def basic_anchorage(phi,context,api,*,flexure_sign):
    if flexure_sign!='NEGATIVE':raise ValueError('positive_bond_requires_physical_bar_classification')
    area=api.Barra(phi).area_cm2
    result=api.calcular_ancoragem(concreto=api.Concreto(context['fck_mpa']),aco=api.Aco(context['fyk_mpa']),bitola_mm=phi,
        as_calculada_cm2=area,as_efetiva_cm2=area,condicoes=api.CondicoesAncoragem(False),
        gamma_c=context['gamma_c'],gamma_s=context['gamma_s'])
    return {'result':asdict(result),'bond_condition':'POOR','rule':BOND_RULE,
        'provenance':{'api':api_provenance(api.calcular_ancoragem),'context':deepcopy(context),
            'area':'Concretopy.Barra unit area; equal calculated/effective for basic anchorage without reduction'}}


def check_bar_event(bars,context,diagram,shear,api,*,mark,cut_side,mode='SCALING',flexure_sign='NEGATIVE',branch_domain=None):
    """Same regions/references/oriented controls as positive; negative policy explicit.

    SCALING: peak + lb, remaining-capacity crossing + 10phi.
    SPAN_TERMINATION: own capacity crossing + lb, signed zero + 10phi.
    """
    out={'flexure_sign':flexure_sign,'mode':mode,'bar_or_group':mark,'cut_side':normalize_side(cut_side),
        'passes':None,'complete':False,'diagnostics':[],'selected_solution':None,'checks':{}}
    try:
        if flexure_sign!='NEGATIVE' or mode not in ('SCALING','SPAN_TERMINATION'):raise ValueError('unsupported_event_policy')
        if context.get('horizontal') is not True or context.get('sliding_formwork') is not False or not context.get('longitudinal_provenance'):
            raise ValueError('event_scope_or_provenance_unresolved')
        raw_matches=[b for b in bars if b.get('mark')==mark and b.get('function')=='negative']
        if len(raw_matches)==1:
            # Basic anchorage remains computable even if vertical positions are pending.
            raw=raw_matches[0]
            out['anchorage']=basic_anchorage(raw['diameter_mm'],context,api,flexure_sign=flexure_sign)
            out['lb_basic_cm']=out['anchorage']['result']['lb_cm']
            out['ten_phi_cm']=10*(raw['diameter_mm']/10)
        physical=prepare_reinforcement(bars,context,api,flexure_sign=flexure_sign)
        matches=[b for b in physical if b['mark']==mark]
        if len(matches)!=1:raise ValueError('interrupted_mark_not_unique')
        bar=matches[0]
        if bar.get('shape')!='straight':raise ValueError('event_segment_straight_geometry_unresolved')
        side=normalize_side(cut_side);event=bar['x_start_common' if side=='LEFT' else 'x_end_common']
        out['actual_end_position_m']=event
        view=tension_diagram(diagram,flexure_sign,domain=branch_domain)
        domain=context.get('span_domain_m',[float(diagram.xs[0]),float(diagram.xs[-1])])
        if not dec(domain[0])<=dec(event)<=dec(domain[1]):raise ValueError('cut_position_outside_known_physical_domain')
        selection_event=float(max(view.xs[0],min(view.xs[-1],dec(event))))
        out['reference_selection_endpoint_m']=selection_event
        regions=decompose_regions(physical,[float(diagram.xs[0]),float(diagram.xs[-1])],flexure_sign=flexure_sign)
        # One-sided physical membership, exactly at the event, without epsilon.
        before_bars=[b for b in physical if (b['x_start_common']<event<=b['x_end_common'] if side=='RIGHT' else b['x_start_common']<=event<b['x_end_common'])]
        after_bars=[b for b in physical if (b['x_start_common']<=event<b['x_end_common'] if side=='RIGHT' else b['x_start_common']<event<=b['x_end_common'])]
        bm={b['mark'] for b in before_bars};am={b['mark'] for b in after_bars}
        if mode=='SCALING':
            out['termination_event']=describe_termination(bm,am,mark,event,side)
        out['provided_end_position_m']=event
        if context.get('negative_support_side') is not None:
            out['support_terminal_demand']=negative_support_terminal_demand(diagram,context['negative_support_side'])
        sample=event
        before_capacity=composition_capacity(before_bars,sample,context,api,flexure_sign=flexure_sign)
        out.update(reinforcement_before_cut=deepcopy(before_bars),reinforcement_after_cut=deepcopy(after_bars),
            before_capacity=before_capacity,physical_regions=regions)
        if not before_capacity['valid']:raise ValueError('before_composition_capacity_invalid')
        if mode=='SCALING':
            if not after_bars:raise ValueError('remaining_composition_missing')
            remaining=composition_capacity(after_bars,event,context,api,flexure_sign=flexure_sign)
            out['capacity_remaining']=remaining
            if not remaining['valid']:raise ValueError('remaining_capacity_invalid')
            refs=locate_references(view,remaining['Mk_equivalent_knm'],side.lower(),selection_event)
            ten_reference=refs['selected_x_nec_m'];lb_reference=None if refs['peak'] is None else refs['peak']['x_m']
            out['capacity_crossing']=refs
        else:
            # Full composition carried to this end, not remnant of another event.
            own=[deepcopy(bar)]
            own_capacity=composition_capacity(own,sample,context,api,flexure_sign=flexure_sign)
            out['capacity_carried_to_end']=own_capacity
            if not own_capacity['valid']:raise ValueError('termination_composition_capacity_invalid')
            refs=locate_references(view,own_capacity['Mk_equivalent_knm'],side.lower(),selection_event)
            zero=locate_references(view,0,side.lower(),selection_event)
            out.update(capacity_crossing=refs,zero_moment_crossing=zero)
            ten_reference=zero['selected_x_nec_m'];lb_reference=refs['selected_x_nec_m']
        peak=refs.get('peak')
        if peak:
            peak['kind']='piecewise_linear_negative_peak'
            peak['peak_location']='endpoint' if dec(peak['x_m']) in (view.xs[0],view.xs[-1]) else 'internal'
        out['peak_or_decay_reference']=deepcopy(peak)
        # Configuration must remain physically the same between used references and cut.
        for reference in [ten_reference,lb_reference]:
            if reference is None:continue
            for region in regions:
                if region['kind']=='interval' and max(region['x_start_m'],min(reference,event))<min(region['x_end_m'],max(reference,event)):
                    if not bm.issubset(set(region['geometric_reinforcement']['marks'])):raise ValueError('event_composition_missing_between_reference_and_cut')
                    if set(region['geometric_reinforcement']['marks'])!=bm:
                        out.setdefault('upstream_additional_reinforcement',[]).append(deepcopy(region))
        out['d_for_al']={'d_cm':before_capacity['concretopy']['d_equivalente_cm'],'rule':AL_RULE,
            'provenance':'/before_capacity/concretopy; composition immediately before oriented event, measured from compression face'}
        al=None
        if shear and shear.get('status')=='resolved' and {s.get('envelope') for s in shear.get('series',[])}=={'max','min'} and context.get('al_scope_confirmed') is True:
            result=api.calcular_al(concreto=api.Concreto(context['fck_mpa']),b_cm=context['section']['bw'],
                d_cm=out['d_for_al']['d_cm'],vk_abs_kn=shear['Vk_used_kn'],gamma_f=context['gamma_f'],gamma_c=context['gamma_c'])
            al=result.al_cm;out['al']={'result':asdict(result),'rule':AL_RULE,'shear':deepcopy(shear),'api':api_provenance(api.calcular_al)}
        else:out['diagnostics'].append('al_context_or_shear_unresolved')
        anchor=out['anchorage']
        out['anchorage']=anchor;lb=anchor['result']['lb_cm'];ten=10*(bar['diameter_mm']/10)
        # Geometry orientation reuses the support convention as direction of the cut.
        geometry=LongitudinalOrientation(side,{'purpose':'oriented physical cut inside span','event_x_m':event,'rule':'engineer_confirmed_support_side_orientation_v1'})
        checks={'al_plus_lb':_control(geometry,event,lb_reference,None if al is None else al+lb,END_RULE if mode=='SPAN_TERMINATION' else AL_RULE),
                'al_plus_10phi':_control(geometry,event,ten_reference,None if al is None else al+ten,END_RULE if mode=='SPAN_TERMINATION' else AL_RULE)}
        if mode=='SPAN_TERMINATION' and refs['diagnostics']==['no_valid_crossing','remaining_sufficient_entire_branch']:
            checks['al_plus_lb'].update(status='NOT_APPLICABLE',passes=True,reason='Capacity exceeds entire branch; no full utilization point',required_end_position_m=None)
        for control in checks.values():
            available,required=control.get('available_length_cm'),control.get('required_length_cm')
            control['margin_cm']=None if available is None or required is None else available-required
        out['required_end_position_m']=None
        out.update(checks=checks,lb_basic_cm=lb,ten_phi_cm=ten,
            provenance={'diagram_original':diagram.as_dict(),'tension_view':view.as_dict(),'event_bar':deepcopy(bar)})
        states=[c['passes'] for c in checks.values()]
        out['passes']=_complete_pass(states);out['complete']=out['passes'] is not None
        out['diagnostics']+=refs['diagnostics'] if mode=='SCALING' or not checks['al_plus_lb'].get('status')=='NOT_APPLICABLE' else []
        if mode=='SPAN_TERMINATION':out['diagnostics']+=zero['diagnostics']
        positions=[(k,c['required_end_position_m']) for k,c in checks.items() if c.get('required_end_position_m') is not None]
        if out['complete'] and positions:
            required=max(geometry.distance_cm(event,x) for _,x in positions)
            out['required_end_position_m']=next(x for k,x in positions if geometry.distance_cm(event,x)==required)
            out['governing_check']=[k for k,x in positions if geometry.distance_cm(event,x)==required]
    except (ValueError,TypeError,KeyError,IndexError,StopIteration) as error:out['diagnostics'].append(str(error))
    return out


def check_physical_flexure(model, context, diagram, api, *, inputs, flexure_sign):
    """Optional stage-1 path: local constant sections, same legacy numerical engine.

    Boundary points at abrupt changes remain pending; no averaged section is used.
    """
    from input_preflight import prepare_local_batches, preflight, execute, overlaps
    from copy import deepcopy
    prepared = prepare_local_batches(model, flexure_sign=flexure_sign)
    out = dict(regions=[], pending_geometry=prepared['pending_geometry'],
               force_policy='TQS_ENVELOPES', correction_generation_enabled=False)
    control = 'positive_flexure' if flexure_sign == 'POSITIVE' else 'negative_flexure'
    for region in prepared['regions']:
        a,z = region['x_start_m'],region['x_end_m']
        if a == z:
            out['regions'].append(dict(region_id=region['region_id'], interval_m=[a,z],
                status='INCONCLUSIVE', execution_state='NOT_EXECUTED',
                reason='abrupt_transition_requires_one_sided_geometry'))
            continue
        plan = preflight(model, region_id=region['region_id'], interval_m=[a,z], control=control, inputs=inputs)
        local_context = deepcopy(context)
        geo = region.get('transverse_geometry')
        if geo:
            local_context['section'] = dict(bw=geo['bw_cm'],h=geo['h_cm'],cobrimento=geo['cover_cm'],diametro_estribo_mm=geo['stirrup_diameter_mm'])
        local = [b for b in prepared['bars'] if b.get('function') == ('positive' if flexure_sign=='POSITIVE' else 'negative')
                 and overlaps(b['x_start_common'],b['x_end_common'],a,z)]
        checked = execute(plan, check_flexure_regions, local, local_context, diagram, api,
                          flexure_sign=flexure_sign, domain=[a,z])
        out['regions'].append(dict(region_id=region['region_id'], interval_m=[a,z], **checked))
    return out
