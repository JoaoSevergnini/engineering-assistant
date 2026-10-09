"""Bounded exploration of positive bars at an oriented end support.

All resistant/anchorage calculations and vertical positioning belong to
Concretopy. Inputs are previously selected/audited, not a TQS parser.
"""
from copy import deepcopy
from dataclasses import asdict, replace
from itertools import combinations
from math import isfinite

from bar_scaling import classify_bond, api_provenance
from support_geometry import normalize_side, normalize_type

PAIR_RULE = 'engineer_confirmed_end_support_effort_pairs_v1'
LENGTH_RULE = 'engineer_confirmed_end_support_available_length_v1'
POSITION_RULE = 'concretopy_vigas_k5_k7'
VALID = 'VALIDA_SEM_AREA_ADICIONAL'
LIMITATIONS = ['geometria_transversal_nao_verificada',
               'gancho_geometria_nao_verificada',
               'configuracao_local_nao_verifica_flexao_do_vao',
               'nao_dimensiona_grampos', 'nao_aprova_viga']


def _number(value, name, *, positive=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value):
        raise ValueError(name + ': expected finite number')
    if positive and value <= 0:
        raise ValueError(name + ': expected positive number')
    return value


def _integer(value, name):
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(name + ': expected positive integer')
    return value


def available_length(support_length_cm, cover_cm, provenance):
    """Geometric workflow decision, independent of documentary bar endpoint."""
    _number(support_length_cm, 'support_length_cm', positive=True)
    _number(cover_cm, 'cover_cm')
    if cover_cm < 0 or cover_cm >= support_length_cm:
        raise ValueError('invalid_support_cover')
    return {'lb_ef_cm': support_length_cm-cover_cm,
            'support_length_cm': support_length_cm, 'cover_cm': cover_cm,
            'rule': LENGTH_RULE, 'provenance': deepcopy(provenance)}


def effort_pairs(mk_positive_kncm, vk_min_signed_kn, vk_max_abs_kn, provenance):
    """Two engineer-selected envelope pairs; no claim of concomitance."""
    _number(mk_positive_kncm, 'mk_positive_kncm')
    _number(vk_min_signed_kn, 'vk_min_signed_kn')
    _number(vk_max_abs_kn, 'vk_max_abs_kn')
    if vk_max_abs_kn < 0:
        raise ValueError('vk_max_abs_kn must be a magnitude')
    pairs = []
    if mk_positive_kncm > 0:
        pairs.append({'id': 'positive_moment_min_shear', 'mk_apoio_kncm': mk_positive_kncm,
                      'vk_apoio_kn': abs(vk_min_signed_kn),
                      'vk_signed_source_kn': vk_min_signed_kn})
    pairs.append({'id': 'zero_moment_max_abs_shear', 'mk_apoio_kncm': 0,
                  'vk_apoio_kn': vk_max_abs_kn})
    for pair in pairs:
        pair.update(rule=PAIR_RULE, provenance=deepcopy(provenance))
    return pairs


def generate_alternatives(*, diameters_mm, min_bars, max_bars, max_layers,
                          position_rule=None, explicit_depths_cm=None, provenance=None):
    """Uniform bitola; enumerate positive ordered partitions across physical layers.

    Limits are caller search bounds, never normative layer/spacing limits.
    Missing positioning data remains visible as non-evaluable candidates.
    """
    for name, value in [('min_bars', min_bars), ('max_bars', max_bars), ('max_layers', max_layers)]:
        _integer(value, name)
    if max_bars < min_bars or not diameters_mm:
        raise ValueError('invalid_search_bounds')
    diameters = list(dict.fromkeys(diameters_mm))
    for phi in diameters:
        _number(phi, 'diameter_mm', positive=True)
    candidates = []
    for n in range(min_bars, max_bars+1):
        for k in range(1, min(max_layers, n)+1):
            for cuts in combinations(range(1, n), k-1):
                boundaries = (0,)+cuts+(n,)
                counts = [b-a for a,b in zip(boundaries, boundaries[1:])]
                for phi in diameters:
                    depths = (explicit_depths_cm or {}).get(phi, ())
                    candidates.append({'id': f'{n}x{phi:g}_layers_'+'_'.join(map(str, counts)),
                        'layers': [{'count': count, 'diameter_mm': phi,
                                    'd_cm': depths[i] if i < len(depths) else None}
                                   for i,count in enumerate(counts)],
                        'position_rule': position_rule,
                        'provenance': deepcopy(provenance)})
    return candidates


def evaluate_configuration(context, configuration, api):
    """Rebuild and recalculate an entire local configuration; preserve partial work."""
    out = {'configuration': deepcopy(configuration), 'status': None,
           'diagnostics': [], 'limitations': list(LIMITATIONS),
           'complete': False, 'passes': None, 'states': [],
           'flexure': None, 'bond_by_layer': [], 'anchorage': None,
           'metrics': None, 'provenance': deepcopy(context.get('provenance'))}
    def blocked(code, detail):
        out['status'] = 'NAO_AVALIAVEL_GEOMETRIA'
        out['diagnostics'].append({'code': code, 'detail': str(detail)})
        return out
    try:
        normalize_side(context.get('support_side'))
        if normalize_type(context.get('support_type')) != 'END':
            raise ValueError('only_end_support_supported')
        if context.get('horizontal') is not True or context.get('sliding_formwork') is not False:
            raise ValueError('unsupported_bond_scope')
        if not isinstance(context.get('gancho_valido'), bool):
            raise ValueError('hook_scenario_unresolved')
        length = available_length(context['support_length_cm'], context['cover_cm'],
                                  context['length_provenance'])
        out['available_length'] = length
        entries = configuration['layers']
        if not entries:
            raise ValueError('empty_configuration')
        phis = set(e['diameter_mm'] for e in entries)
        if len(phis) != 1:
            raise ValueError('mixed_bitolas_not_supported_by_aggregate_anchorage')
        for entry in entries:
            _integer(entry['count'], 'layer_count')
            _number(entry['diameter_mm'], 'diameter_mm', positive=True)
            if entry.get('d_cm') is not None:
                _number(entry['d_cm'], 'd_cm', positive=True)
        if any(e.get('d_cm') is None for e in entries) and configuration.get('position_rule') != POSITION_RULE:
            raise ValueError('layer_position_unresolved')
        section = api.SecaoRetangular(**context['section'])
        if section.cobrimento != context['cover_cm']:
            raise ValueError('cover_context_mismatch')
        concrete = api.Concreto(context['fck_mpa']); steel = api.Aco(context['fyk_mpa'])
        layers = tuple(api.CamadaArmaduraLongitudinal(e['count'], api.Barra(e['diameter_mm']), e.get('d_cm')) for e in entries)
        ds = api.calcular_alturas_uteis_camadas(section, layers)
        if any(a <= b for a,b in zip(ds,ds[1:])):
            raise ValueError('physical_layers_not_ordered_from_bottom')
        layers = tuple(replace(layer, d_cm=d) for layer,d in zip(layers,ds))
        out['resolved_layers'] = [asdict(layer) for layer in layers]
        out['position_provenance'] = {'rule': configuration.get('position_rule'),
            'explicit_depths': [e.get('d_cm') for e in entries],
            'api': api_provenance(api.calcular_alturas_uteis_camadas)}
        coefficients = {key: context[key] for key in ('gamma_f','gamma_c','gamma_s')}
        flex = api.verificar_flexao_viga_retangular(section, concrete, steel, layers, **coefficients)
        out['flexure'] = asdict(flex)
        if not flex.hipoteses_validas or not flex.ductilidade_atendida:
            raise ValueError('concretopy_flexure_hypotheses_or_ductility_invalid')
        out['bond_by_layer'] = [classify_bond(section.h, section.h-d) for d in ds]
        if len({b['boa_aderencia'] for b in out['bond_by_layer']}) != 1:
            raise ValueError('mixed_bond_not_representable_by_aggregate_anchorage')
        pairs = context['pairs']
        if not pairs or len({p['id'] for p in pairs}) != len(pairs):
            raise ValueError('empty_or_duplicate_pairs')
        common = dict(secao=section, concreto=concrete, aco=steel, camadas_apoio=layers,
            tipo_apoio='extremo', mk_positivo_max_vao_kncm=context['mk_positive_max_span_kncm'],
            mk_negativo_apoio_kncm=context['mk_negative_support_kncm'],
            d_vao_cm=context['d_span_cm'], nd_tracao_kn=context['nd_tracao_kn'], **coefficients)
        if context.get('section_span') is not None:
            common['secao_vao'] = api.SecaoRetangular(**context['section_span'])
        for key in ('d_linha_apoio_cm','d_linha_vao_cm'):
            if context.get(key) is not None:
                common[key] = context[key]
        for pair in pairs:
            result = api.calcular_armadura_positiva_apoio(**common,
                mk_apoio_kncm=pair['mk_apoio_kncm'], vk_apoio_kn=pair['vk_apoio_kn'])
            out['states'].append({'pair': deepcopy(pair), 'result': asdict(result)})
        demand = max(s['result']['as_necessaria_cm2'] for s in out['states'])
        out['governing_pairs'] = [s['pair']['id'] for s in out['states'] if s['result']['as_necessaria_cm2']==demand]
        anchor = api.verificar_ancoragem_positiva_apoio(concreto=concrete, aco=steel,
            bitola_mm=next(iter(phis)), as_calculada_cm2=demand, as_efetiva_cm2=flex.as_total_cm2,
            condicoes=api.CondicoesAncoragem(out['bond_by_layer'][0]['boa_aderencia']),
            comprimento_disponivel_cm=length['lb_ef_cm'], gancho_valido=context['gancho_valido'],
            gamma_c=context['gamma_c'], gamma_s=context['gamma_s'])
        out['anchorage'] = asdict(anchor)
        failures = []
        if not anchor.area_suficiente:
            failures.append('AREA_INSUFICIENTE')
        if anchor.comprimento_menor_lb_min:
            failures.append('ABAIXO_LB_MIN')
        if not anchor.comprimento_suficiente:
            failures.append('ANCORAGEM_INSUFICIENTE')
        if anchor.as_adicional_cm2 > 0:
            failures.append('AREA_ADICIONAL_NECESSARIA')
        out['diagnostics'] += [{'code': code} for code in failures]
        out['complete'] = True
        out['passes'] = anchor.atende and anchor.as_adicional_cm2==0
        out['status'] = VALID if out['passes'] else (
            'AREA_INSUFICIENTE' if not anchor.area_suficiente else
            'ABAIXO_LB_MIN' if anchor.comprimento_menor_lb_min else 'ANCORAGEM_INSUFICIENTE')
        r = out['states'][0]['result']
        out['metrics'] = {'number_bars': sum(e['count'] for e in entries), 'number_layers':len(entries),
            'As_effective_cm2':flex.as_total_cm2, 'As_support_cm2':demand,
            'area_excess_cm2':flex.as_total_cm2-demand, 'd_cm':r['d_cm'], 'x_cm':r['x_cm'],
            'z_cm':r['z_cm'], 'diameter_mm':next(iter(phis)),
            'lb_cm':anchor.lb_cm, 'lb_min_cm':anchor.lb_min_cm, 'lb_nec_cm':anchor.lb_nec_cm,
            'lb_ef_cm':length['lb_ef_cm'], 'anchorage_margin_cm':length['lb_ef_cm']-anchor.lb_nec_cm,
            'As_corr_cm2':anchor.as_corr_cm2, 'As_additional_cm2':anchor.as_adicional_cm2,
            'gancho_valido':context['gancho_valido'], 'geometria_transversal_nao_verificada':True}
        out['api_provenance'] = {name:api_provenance(getattr(api,name)) for name in
            ('verificar_flexao_viga_retangular','calcular_armadura_positiva_apoio','verificar_ancoragem_positiva_apoio')}
        return out
    except (ValueError, TypeError, KeyError, OverflowError) as error:
        return blocked('configuration_not_evaluable', error)


def explore_alternatives(context, existing, api, *, search):
    current = evaluate_configuration(context, existing, api)
    output = {'existing': current, 'search': deepcopy(search), 'alternatives': [],
              'valid_alternative_ids': [], 'selected_solution': None,
              'ordering': ['number_bars','number_layers','As_effective_cm2','area_excess_cm2',
                           'anchorage_margin_cm (descending)','diameter_mm'],
              'search_executed': False, 'limitations': list(LIMITATIONS)}
    # Do not optimize around unresolved original inputs, or an already passing arrangement.
    if not current['complete'] or current['passes']:
        output['search_reason'] = 'existing_not_evaluable' if not current['complete'] else 'existing_passes'
        return output
    output['search_executed'] = True
    for candidate in generate_alternatives(**search):
        output['alternatives'].append(evaluate_configuration(context,candidate,api))
    valid = [r for r in output['alternatives'] if r['status']==VALID]
    valid.sort(key=lambda r:(r['metrics']['number_bars'],r['metrics']['number_layers'],
        r['metrics']['As_effective_cm2'],r['metrics']['area_excess_cm2'],
        -r['metrics']['anchorage_margin_cm'],r['metrics']['diameter_mm'],r['configuration']['id']))
    output['valid_alternative_ids'] = [r['configuration']['id'] for r in valid]
    output['search_reason'] = 'valid_candidates_found' if valid else 'no_solution_in_configured_search'
    return output
