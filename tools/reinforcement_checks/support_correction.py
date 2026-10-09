"""Detail-oriented correction of positive reinforcement at an oriented end support.

Keep generic local exploration intact. Resistant physics, vertical positioning,
anchorage and interpolation are delegated to existing primitives.
"""
from copy import deepcopy
from dataclasses import asdict
from importlib import import_module
from itertools import product

from bar_scaling import api_provenance
from flexure_regions import compose_layers, decompose_regions, contains
from support_alternatives import evaluate_configuration, POSITION_RULE
from support_geometry import normalize_side

FIT_RULE = 'engineer_confirmed_positive_bar_clear_spacing_v1'
CORRECTION_RULE = 'engineer_confirmed_positive_support_correction_hierarchy_v1'


def transverse_fit(section, layers, api):
    """One explicit diameter per physical bar; no equivalent diameter.

    Concretopy spacing default 16mm adds 1.92cm, always dominated by 2cm.
    This compatibility parameter is not an adopted project aggregate size.
    """
    out = {'cabimento_transversal': None, 'layers': [], 'rule': FIT_RULE,
           'diagnostics': [], 'provenance': {'geometry': deepcopy(section),
           'aggregate_parameter_mm': 16, 'aggregate_check': 'not_in_scope'}}
    try:
        norms = import_module('concretopy.normas')
        arrangements = import_module('concretopy.detalhamento.arranjos')
        spacing = norms.espacamento_min_arm_long_viga
        maximum = arrangements.numero_barras_maximo_camada
        out['provenance']['spacing_api'] = api_provenance(spacing)
        out['provenance']['capacity_api'] = api_provenance(maximum)
        sec = api.SecaoRetangular(**section)
        width = sec.bw-2*(sec.cobrimento+sec.diametro_estribo_mm/10)
        if width <= 0 or not layers:
            raise ValueError('invalid_internal_width_or_empty_layers')
        for i, layer in enumerate(layers,1):
            # Mixed bars may be supplied explicitly for geometry, without flexural equivalence.
            phis = layer.get('diameters_mm')
            if phis is None:
                n=layer['count']
                if type(n) is not int or n < 1:
                    raise ValueError('invalid_bar_count')
                phis=[layer['diameter_mm']]*n
            if not phis:
                raise ValueError('empty_physical_layer')
            minima=[spacing(phi) for phi in phis]
            gaps=[max(a,b) for a,b in zip(minima,minima[1:])]
            needed=sum(phi/10 for phi in phis)+sum(gaps)
            capacity=None
            fits=needed<=width
            if len(set(phis))==1:
                capacity=maximum(sec.bw,phis[0],sec.diametro_estribo_mm,sec.cobrimento)
                if fits != (len(phis)<=capacity):
                    raise ValueError('existing_primitive_capacity_conflict')
            actual=(width-sum(phi/10 for phi in phis))/(len(phis)-1) if len(phis)>1 else None
            out['layers'].append({'layer':layer.get('layer',i),'diameters_mm':list(phis),
                'available_width_cm':width,'required_width_cm':needed,
                'minimum_clear_gaps_cm':gaps,'adopted_clear_gaps_cm':gaps,
                'clear_spacing_if_uniform_cm':actual,'minimum_per_bar_cm':minima,
                'maximum_uniform_bar_count':capacity,'fits':fits})
        out['cabimento_transversal']=all(l['fits'] for l in out['layers'])
        if not out['cabimento_transversal']:
            out['diagnostics'].append('barras_nao_cabem_com_espacamento_livre_confirmado')
    except (ValueError,TypeError,KeyError,AttributeError) as error:
        out['diagnostics'].append(str(error))
    return out


def _active(bars,x):
    return [b for b in bars if b['x_start_common']<=x<=b['x_end_common']]


def configuration_from_bars(bars, x, label, *, flexure_sign="POSITIVE"):
    """Preserve explicit layer identity and positions; block missing or mixed layers."""
    composition=compose_layers(_active(bars,x),flexure_sign=flexure_sign)
    if composition['status']!='resolved':
        raise ValueError(';'.join(composition['issues']))
    layers=[]
    for layer in composition['layers']:
        active=[b for b in _active(bars,x) if len(b['layers'])>=layer['layer'] and b['layers'][layer['layer']-1]]
        ds={b.get('d_by_layer_cm',[None]*layer['layer'])[layer['layer']-1] if b.get('d_by_layer_cm') is not None else b.get('d_cm') for b in active}
        if len(ds)!=1 or None in ds:
            raise ValueError('physical_layer_depth_unresolved')
        layers.append({'count':layer['numero_barras'],'diameter_mm':layer['diametro_mm'],
                       'd_cm':next(iter(ds)),'layer':layer['layer']})
    return {'id':label,'layers':layers,'provenance':{'composition':composition,'x_m':x}}


def _validate_bars(bars, *, flexure_sign="POSITIVE"):
    function,face=("positive","lower") if flexure_sign=="POSITIVE" else ("negative","upper")
    if not bars or len({b['mark'] for b in bars})!=len(bars):
        raise ValueError('empty_or_duplicate_bar_marks')
    for b in bars:
        if b.get('x_start_common') is None or b.get('x_end_common') is None or b['x_start_common']>b['x_end_common']:
            raise ValueError('unknown_or_inverted_longitudinal_interval')
        if b.get('function')!=function or b.get('face')!=face:
            raise ValueError('unknown_positive_bar_function_or_face')
        if b.get('d_cm') is None and b.get('d_by_layer_cm') is None:
            raise ValueError('physical_bar_center_unresolved')


def check_longitudinal(bars, context, diagram, api, *, flexure_sign="POSITIVE"):
    result_key="compatibilidade_flexao_positiva" if flexure_sign=="POSITIVE" else "compatibilidade_flexao_negativa"
    """Existing region decomposition + moment queries + public Concretopy flexure.

    Check all linear-piece vertices AND limiting values at composition changes;
    no extrapolation and no approximation of demand in a short region.
    """
    out={result_key:None,'regions':[], 'diagnostics':[],
         'provenance':deepcopy(context.get('longitudinal_provenance'))}
    if diagram is None or not context.get('longitudinal_provenance'):
        out['diagnostics'].append('compatibilidade_flexao_positiva_nao_verificada')
        return out
    try:
        _validate_bars(bars,flexure_sign=flexure_sign)
        if any(m is None for m in diagram.ms):
            raise ValueError('incomplete_moment_diagram')
        domain=(float(diagram.xs[0]),float(diagram.xs[-1]))
        regions=decompose_regions(bars,domain,flexure_sign=flexure_sign)
        for region in regions:
            a,b=region['x_start_m'],region['x_end_m']
            midpoint=(a+b)/2
            if flexure_sign=='NEGATIVE':
                points=[diagram.moment_at_x(x) for x in sorted({a,b,*[float(x) for x in diagram.xs if a<=float(x)<=b]})]
                if all(p['status']=='resolved' for p in points) and not any(p['value_knm']>0 for p in points):
                    out['regions'].append({'geometry':region,'configuration':{'layers':[]},'demand_points':points,
                        'governing_demand':None,'concretopy':None,'capacity_sufficient':True,'status':'NOT_APPLICABLE',
                        'transverse_fit':None})
                    continue
            cfg=configuration_from_bars(bars,midpoint,region['region_id'],flexure_sign=flexure_sign)
            section=context.get('section_span') or context['section']
            sec=api.SecaoRetangular(**section)
            layers=tuple(api.CamadaArmaduraLongitudinal(e['count'],api.Barra(e['diameter_mm']),e['d_cm']) for e in cfg['layers'])
            fit=transverse_fit(section,cfg['layers'],api)
            points=[diagram.moment_at_x(x) for x in sorted({a,b,*[float(x) for x in diagram.xs if a<=float(x)<=b]})]
            if any(p['status']!='resolved' for p in points):
                raise ValueError('unresolved_regional_demand')
            positive=[p for p in points if p['value_knm']>0]
            flex=api.verificar_flexao_viga_retangular(sec,api.Concreto(context['fck_mpa']),api.Aco(context['fyk_mpa']),layers,
                gamma_f=context['gamma_f'],gamma_c=context['gamma_c'],gamma_s=context['gamma_s'])
            governing=max(positive,key=lambda p:p['value_knm']) if positive else None
            valid=flex.hipoteses_validas and flex.ductilidade_atendida and flex.mk_equivalente_kncm is not None
            passes=(flex.mk_equivalente_kncm/100>=governing['value_knm']) if valid and governing else True if valid else None
            out['regions'].append({'geometry':region,'configuration':cfg,'demand_points':points,
                'governing_demand':governing,'concretopy':asdict(flex),'capacity_sufficient':passes,'transverse_fit':fit})
        states=[r['capacity_sufficient'] for r in out['regions']]
        out[result_key]=(None if None in states else all(states)) if flexure_sign=='NEGATIVE' else (False if False in states else None if None in states else True)
        out['provenance'].update(region_api='flexure_regions.decompose_regions',moment_api='MomentDiagram.moment_at_x',
            flexure_api=api_provenance(api.verificar_flexao_viga_retangular),domain_m=list(domain),
            scope='Adopted sampled piecewise-linear domain; no extrapolation. Uniform section/layer parameterization explicitly supplied by caller.')
        if out[result_key] is False:
            out['diagnostics'].append('flexao_positiva_insuficiente_em_regiao')
    except (ValueError,TypeError,KeyError,IndexError) as error:
        out['diagnostics'].append('compatibilidade_flexao_positiva_nao_verificada:'+str(error))
    return out


def extension_candidates(bars, support_x, target_x, support_side="LEFT"):
    if normalize_side(support_side)=="RIGHT":
        return _right_extension_candidates(bars,support_x,target_x)
    """One interrupted mark at a time; individually extend 1..all physical bars."""
    _validate_bars(bars)
    output=[]
    for bar in bars:
        if not target_x<=support_x<bar['x_start_common']<bar['x_end_common']:
            continue
        populated=[i for i,n in enumerate(bar['layers']) if n]
        if len(populated)!=1:
            continue
        layer=populated[0]
        for quantity in range(1,bar['bars']+1):
            proposal=[deepcopy(b) for b in bars if b['mark']!=bar['mark']]
            extended=deepcopy(bar);extended.update(mark=bar['mark']+'__extended_'+str(quantity),
                origin_mark=bar['mark'],bars=quantity,x_start_common=target_x)
            extended['proposal_geometry']={'original_start_common_m':bar['x_start_common'],'proposed_start_common_m':target_x,'original_documentary_start_cm':bar.get('x_start_cm'),'note':'Original documentary fields are provenance, not proposed fabrication lengths. New bend and developed length are not designed.'}
            extended['layers']=[quantity if i==layer else 0 for i in range(len(bar['layers']))]
            proposal.append(extended)
            if quantity<bar['bars']:
                remaining=deepcopy(bar);remaining.update(mark=bar['mark']+'__remaining_'+str(bar['bars']-quantity),origin_mark=bar['mark'],bars=bar['bars']-quantity)
                remaining['layers']=[bar['bars']-quantity if i==layer else 0 for i in range(len(bar['layers']))]
                proposal.append(remaining)
            output.append({'id':'extend_'+bar['mark']+'_'+str(quantity),'origin':'PROLONGAMENTO','bars':proposal,
                'changes':[{'origin_mark':bar['mark'],'extended_quantity':quantity,'diameter_mm':bar['diameter_mm'],
                    'physical_layer':layer+1,'d_cm':bar['d_cm'],'original_start_m':bar['x_start_common'],
                    'proposed_start_m':target_x,'unextended_quantity':bar['bars']-quantity,
                    'hook_scenario':'Proposed termination at support uses caller hook scenario; bend geometry remains to review'}]})
    return output


def preserved_original_reinforcement(original, proposed):
    """Verify count/diameter/center unchanged everywhere each original mark existed."""
    try:
        _validate_bars(original);_validate_bars(proposed)
        for bar in original:
            same=[b for b in proposed if b.get('origin_mark',b['mark'])==bar['mark']]
            if sum(b['bars'] for b in same)!=bar['bars']:
                return False
            for b in same:
                if (b['diameter_mm']!=bar['diameter_mm'] or b['d_cm']!=bar['d_cm'] or
                    b['x_start_common']>bar['x_start_common'] or b['x_end_common']<bar['x_end_common']):
                    return False
            if any(sum(b['layers'][i] if i<len(b['layers']) else 0 for b in same)!=n for i,n in enumerate(bar['layers'])):
                return False
        return True
    except (ValueError,KeyError,TypeError):
        return None


def diameter_steps(lower, upper, series):
    if len(set(series))!=len(series) or sorted(series)!=list(series):
        raise ValueError('diameter_series_must_be_unique_and_increasing')
    if lower not in series or upper not in series:
        raise ValueError('diameter_missing_from_series')
    return series.index(upper)-series.index(lower)


def redistribution_candidates(bars, api, section, *, series, max_steps=2, counts=(2,3)):
    """Bounded coherent two-layer replacement preserving longitudinal profiles.

    First (smaller) layer reaches support; second (larger) retains cut profile.
    Does not optimize arbitrary bar arrangements or extend extra layers here.
    """
    if not series or type(max_steps) is not int or max_steps<1 or not counts or any(type(n) is not int or n<1 for n in counts):
        raise ValueError('invalid_redistribution_bounds')
    diameter_steps(series[0],series[-1],series)
    _validate_bars(bars)
    firsts=[b for b in bars if len(b['layers'])==1 and b['layers'][0]==b['bars']]
    seconds=[b for b in bars if len(b['layers'])==2 and b['layers'][0]==0 and b['layers'][1]==b['bars']]
    if len(bars)!=2 or len(firsts)!=1 or len(seconds)!=1:
        return []
    first,second=firsts[0],seconds[0]
    output=[]
    for low,high in product(series,repeat=2):
        steps=diameter_steps(low,high,series)
        if not 1<=steps<=max_steps:
            continue
        for n1,n2 in product(counts,repeat=2):
            physical=(api.CamadaArmaduraLongitudinal(n1,api.Barra(low)),api.CamadaArmaduraLongitudinal(n2,api.Barra(high)))
            ds=api.calcular_alturas_uteis_camadas(api.SecaoRetangular(**section),physical)
            proposal=[]
            for original,n,phi,d,vector in [(first,n1,low,ds[0],[n1]),(second,n2,high,ds[1],[0,n2])]:
                b=deepcopy(original);b.update(origin_mark=b['mark'],bars=n,diameter_mm=phi,d_cm=d,layers=vector)
                proposal.append(b)
            output.append({'id':f'redistribute_{n1}x{low:g}_{n2}x{high:g}','origin':'REDISTRIBUICAO',
                'bars':proposal,'diameter_steps':steps,'series':list(series),
                'changes':[{'original':deepcopy(a),'proposed':deepcopy(b)} for a,b in zip((first,second),proposal)],
                'original_composition':deepcopy(bars),'proposed_composition':deepcopy(proposal)})
    return output


def evaluate_detail_candidate(context, original, candidate, diagram, api, *, max_steps=2):
    out=deepcopy(candidate)
    out.update(technically_valid=None,recomendavel_como_correcao=False,ready_for_detailing=False,
        reasons=[],cabimento_transversal=None,limitations=['gancho_geometria_nao_verificada','interferencias_no_no_nao_verificadas',
            'tolerancias_e_pacotes_nao_verificados','nao_dimensiona_grampos'])
    try:
        config=configuration_from_bars(candidate['bars'],context['support_reference_x_m'],candidate['id'])
        # For redistribution, derive new span depth from the physical peak-region composition.
        local_context=deepcopy(context)
        if candidate['origin']=='REDISTRIBUICAO' and diagram is not None:
            peak=diagram.positive_maximum()['interpolated_piecewise_max']
            if peak is None:
                raise ValueError('span_depth_unresolved_without_positive_peak')
            span_cfg=configuration_from_bars(candidate['bars'],peak['x_m'],'span_peak')
            sec=api.SecaoRetangular(**(context.get('section_span') or context['section']))
            rr=api.verificar_flexao_viga_retangular(sec,api.Concreto(context['fck_mpa']),api.Aco(context['fyk_mpa']),
                tuple(api.CamadaArmaduraLongitudinal(e['count'],api.Barra(e['diameter_mm']),e['d_cm']) for e in span_cfg['layers']),
                gamma_f=context['gamma_f'],gamma_c=context['gamma_c'],gamma_s=context['gamma_s'])
            local_context['d_span_cm']=rr.d_equivalente_cm
            out['span_depth_recalculation']=asdict(rr)
        local=evaluate_configuration(local_context,config,api)
        out['support_check']=local
        fit=transverse_fit(context['section'],config['layers'],api)
        out['support_transverse_fit']=fit
        longitudinal=check_longitudinal(candidate['bars'],local_context,diagram,api)
        out['longitudinal_check']=longitudinal
        geometries=[fit['cabimento_transversal']]+[r['transverse_fit']['cabimento_transversal'] for r in longitudinal['regions']]
        out['cabimento_transversal']=False if False in geometries else None if None in geometries else True
        preserved=preserved_original_reinforcement(original,candidate['bars']) if candidate['origin']=='PROLONGAMENTO' else None
        out['original_span_reinforcement_preserved']=preserved
        if candidate['origin']=='PROLONGAMENTO' and preserved is True:
            baseline=check_longitudinal(original,local_context,diagram,api)
            comparisons=[]
            for before in baseline['regions']:
                rg=before['geometry']; x=(rg['x_start_m']+rg['x_end_m'])/2
                after=[r for r in longitudinal['regions'] if contains(r['geometry'],x)]
                if len(after)!=1 or before['concretopy']['mk_equivalente_kncm'] is None or after[0]['concretopy']['mk_equivalente_kncm'] is None:
                    comparisons.append({'x_m':x,'capacity_not_reduced':None})
                else:
                    old=before['concretopy']['mk_equivalente_kncm'];new=after[0]['concretopy']['mk_equivalente_kncm']
                    comparisons.append({'x_m':x,'original_Mk_equivalent_kncm':old,
                        'proposed_Mk_equivalent_kncm':new,'capacity_not_reduced':new>=old})
            out['capacity_preservation_comparisons']=comparisons
            preserved=all(c['capacity_not_reduced'] is True for c in comparisons) if comparisons and all(c['capacity_not_reduced'] is not None for c in comparisons) else None
            out['original_span_capacity_not_reduced']=preserved
        if local.get('metrics'):
            local['metrics']['geometria_transversal_nao_verificada']=out['cabimento_transversal'] is None
        if out['cabimento_transversal'] is True:
            local['limitations']=[l for l in local['limitations'] if l!='geometria_transversal_nao_verificada']
        if candidate['origin']=='PROLONGAMENTO' and preserved is not True:
            out['reasons'].append('prolongamento_altera_armadura_original_do_vao')
        checks=[local['passes'],out['cabimento_transversal'],longitudinal['compatibilidade_flexao_positiva']]
        if candidate['origin']=='PROLONGAMENTO':checks.append(preserved)
        out['technically_valid']=False if False in checks else None if None in checks else True
        if local['passes'] is not True:out['reasons'].append('apoio_local_nao_atende_ou_inconclusivo')
        if out['cabimento_transversal'] is not True:out['reasons'].append('cabimento_transversal_nao_atende_ou_inconclusivo')
        if longitudinal['compatibilidade_flexao_positiva'] is not True:
            out['reasons'].append('compatibilidade_flexao_positiva_nao_verificada' if longitudinal['compatibilidade_flexao_positiva'] is None else 'flexao_positiva_regional_insuficiente')
        preference_ok=candidate['origin']!='REDISTRIBUICAO' or 1<=candidate['diameter_steps']<=max_steps
        if not preference_ok:out['reasons'].append('fora_da_preferencia_de_passos_de_bitola')
        out['recomendavel_como_correcao']=out['technically_valid'] is True and preference_ok
        if out['recomendavel_como_correcao']:out['reasons'].append('candidata_coerente_para_revisao_do_engenheiro_sem_escolha_automatica')
    except (ValueError,KeyError,TypeError,IndexError) as error:
        out['reasons'].append('dados_de_correcao_inconclusivos:'+str(error))
    return out


def correction_workflow(context, bars, diagram, api, *, redistribution_search):
    out={'rule':CORRECTION_RULE,'original_composition':deepcopy(bars),'extensions':[],
         'redistributions':[],'recommended_ids':[],'selected_solution':None,'next_step':None,
         'redistribution_search':deepcopy(redistribution_search),'diagnostics':[]}
    current=evaluate_detail_candidate(context,bars,{'id':'existing','origin':'EXISTENTE','bars':deepcopy(bars),'changes':[]},diagram,api)
    out['existing']=current
    if current['technically_valid'] is True:
        out.update(next_step='NENHUMA_CORRECAO',redistribution_reason='existing_valid')
        return out
    if not current.get('support_check',{}).get('complete'):
        out['diagnostics'].append('configuracao_existente_inconclusiva')
        return out
    try:
        candidates=extension_candidates(bars,context['support_reference_x_m'],context['extension_target_x_m'],context.get('support_side','LEFT'))
        out['extensions']=[evaluate_detail_candidate(context,bars,c,diagram,api) for c in candidates]
        recommended=[c for c in out['extensions'] if c['recomendavel_como_correcao']]
        if recommended:
            out.update(next_step='PROLONGAR_ARMADURA_EXISTENTE',recommended_ids=[c['id'] for c in recommended],
                       redistribution_reason='extension_candidates_adequate; no unnecessary redistribution')
            return out
        generated=redistribution_candidates(bars,api,context.get('section_span') or context['section'],**redistribution_search)
        out['redistributions']=[evaluate_detail_candidate(context,bars,c,diagram,api,max_steps=redistribution_search.get('max_steps',2)) for c in generated]
        recommended=[c for c in out['redistributions'] if c['recomendavel_como_correcao']]
        if recommended:
            out.update(next_step='REDISTRIBUIR_ARMADURA',recommended_ids=[c['id'] for c in recommended])
        elif current.get('longitudinal_check',{}).get('compatibilidade_flexao_positiva') is None:
            out['diagnostics'].append('compatibilidade_flexao_positiva_nao_verificada; completar dados antes de recomendar correcao')
        elif current.get('longitudinal_check',{}).get('compatibilidade_flexao_positiva') is False:
            out['diagnostics'].append('flexao_positiva_original_insuficiente; armadura complementar de ancoragem nao corrige esta dependencia')
        else:
            out.update(next_step='AVALIAR_ARMADURA_COMPLEMENTAR',recommendation='RECOMENDA_AVALIAR_ARMADURA_COMPLEMENTAR_DE_ANCORAGEM')
    except (ValueError,KeyError,TypeError) as error:
        out['diagnostics'].append(str(error))
    return out


def _right_extension_candidates(bars,support_x,target_x):
    """Reuse LEFT candidate splitting through a coordinate transform of geometry.

    This reflection is strictly geometry; no effort is reflected/selected here.
    """
    mirrored=deepcopy(bars)
    for bar in mirrored:
        bar['x_start_common'],bar['x_end_common']=-bar['x_end_common'],-bar['x_start_common']
    output=extension_candidates(mirrored,-support_x,-target_x,'LEFT')
    for candidate in output:
        for bar in candidate['bars']:
            bar['x_start_common'],bar['x_end_common']=-bar['x_end_common'],-bar['x_start_common']
            if 'proposal_geometry' in bar:
                old=bar['proposal_geometry']
                bar['proposal_geometry']={'original_end_common_m':-old['original_start_common_m'],
                    'proposed_end_common_m':-old['proposed_start_common_m'],'note':old['note']}
        for change in candidate['changes']:
            change['original_end_m']=-change.pop('original_start_m')
            change['proposed_end_m']=-change.pop('proposed_start_m')
            change['added_horizontal_length_cm']=(change['proposed_end_m']-change['original_end_m'])*100
    return output
