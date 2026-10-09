"""Escalonamento positivo no vao: geometria/workflow; fisica via Concretopy.

Comprimentos em cm, coordenadas em m, momentos em kN.m e cortantes em kN.
Scope explicito; d para al segue o centroide da composicao anterior confirmado pelo engenheiro.
"""
import copy
from dataclasses import asdict
from decimal import Decimal, localcontext
import hashlib
import inspect
from pathlib import Path

from moment_diagram import dec, diagram_from_tqs
from positive_flexure import check_positive_flexure
from termination_event import describe_termination
from tqs_shear import shear_from_tqs

BOND_RULE = 'engineer_confirmed_bond_condition_v1'
SCALING_RULE = 'engineer_confirmed_positive_bar_scaling_v1'
DEPTH_RULE = 'engineer_confirmed_al_effective_depth_v1'
SUPPORTED_SCOPE = {'flexure': 'positive', 'horizontal': True, 'hooks': False,
                   'welds': False, 'special_longitudinal_compression': False,
                   'sliding_formwork': False, 'ribbed': True,
                   'vertical_stirrups': True, 'vc_model': 'Vc0'}


def classify_bond(h_cm, y_cm):
    h, y = dec(h_cm), dec(y_cm)
    if h <= 0 or not 0 < y < h:
        raise ValueError('invalid_bar_center_geometry')
    boundary = dec(30) if h < 60 else h - 30
    return {'h_cm': float(h), 'bar_center_from_bottom_cm': float(y),
            'boundary_cm': float(boundary), 'classification': 'good' if y <= boundary else 'poor',
            'boa_aderencia': y <= boundary, 'rule': BOND_RULE,
            'provenance': {'rule_source': 'engineer confirmation, horizontal bars; boundary belongs to good bond'}}


def locate_references(diagram, mk, side, event_x):
    """Simple unimodal representation only; no arbitrary peak/crossing choice."""
    if side not in ('left', 'right'):
        raise ValueError('unsupported_cut_side')
    out = {'peak': None, 'crossings': None, 'candidates': [], 'selected_x_nec_m': None,
           'selected_crossing': None, 'selection_reason': None, 'diagnostics': [],
           'provenance': diagram.as_dict()}
    if mk is not None:
        out['crossings'] = diagram.find_crossings(mk)
    if not diagram.xs[0] <= dec(event_x) <= diagram.xs[-1]:
        out['diagnostics'].append('event_outside_sampled_moment_domain')
    if any(m is None for m in diagram.ms):
        out['diagnostics'].append('incomplete_moment_diagram')
        return out
    maximum = max(diagram.ms)
    maxima = [i for i, m in enumerate(diagram.ms) if m == maximum]
    if maximum <= 0:
        out['diagnostics'].append('no_positive_peak')
        return out
    if len(maxima) != 1:
        out['peak_candidates'] = [copy.deepcopy(diagram.points[i]) for i in maxima]
        code = 'positive_peak_plateau' if any(b == a+1 for a, b in zip(maxima, maxima[1:])) else 'multiple_positive_peaks'
        out['diagnostics'].append(code)
        return out
    i = maxima[0]
    peak = copy.deepcopy(diagram.points[i])
    peak['kind'] = 'piecewise_linear_positive_peak'
    peak['interpretation'] = 'Maximum of the adopted representation, not exact structural maximum'
    out['peak'] = peak
    direction = 1 if side == 'right' else -1
    if (i == (len(diagram.points)-1 if side == 'right' else 0) or
            direction*(dec(event_x)-diagram.xs[i]) <= 0):
        out['diagnostics'].append('event_branch_not_identifiable')
        out['peak'] = None
        return out
    branch_ids = range(i, len(diagram.segments)) if side == 'right' else range(i)
    ids = {diagram.segments[j]['segment_id'] for j in branch_ids}
    wanted = 'decreasing' if side == 'right' else 'increasing'
    if out['crossings']:
        for crossing in out['crossings']['crossings']:
            if any(s['segment_id'] in ids and s['direction'] in (wanted, 'constant') for s in crossing['segments']):
                out['candidates'].append(copy.deepcopy(crossing))
        if len(out['candidates']) > 1 or any(c['status'] == 'coincident_segment' for c in out['candidates']):
            out['diagnostics'].append('ambiguous_crossing')
    # Strict unimodality avoids accepting a later rise on either side of the peak.
    if (any(b <= a for a, b in zip(diagram.ms[:i], diagram.ms[1:i+1])) or
            any(b >= a for a, b in zip(diagram.ms[i:], diagram.ms[i+1:]))):
        out['diagnostics'].append('unsupported_non_unimodal_branch')
        out['peak'] = None
        return out
    if mk is None:
        out['diagnostics'].append('remaining_capacity_unresolved')
        return out
    if out['diagnostics']:
        return out
    if not out['candidates']:
        values = diagram.ms[i:] if side == 'right' else diagram.ms[:i+1]
        code = ('remaining_sufficient_entire_branch' if dec(mk) > max(values) else
                'remaining_insufficient_entire_branch' if dec(mk) < min(values) else 'no_valid_crossing')
        out['diagnostics'].extend(['no_valid_crossing', code] if code != 'no_valid_crossing' else [code])
        return out
    chosen = out['candidates'][0]
    out.update(selected_x_nec_m=chosen['x_m'], selected_crossing=chosen,
               selection_reason=f'Unique {wanted} crossing on the {side} branch outward from the unique positive piecewise-linear peak')
    return out


def api_provenance(function):
    path = Path(inspect.getfile(function)).resolve()
    return {'interface': function.__module__+'.'+function.__name__,
            'signature': str(inspect.signature(function)), 'file': str(path),
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def _review_copy(value):
    copied = copy.deepcopy(value)
    def rebase(node):
        if isinstance(node, dict):
            if 'shared_pointer' in node:
                node['shared_pointer'] = '/audit_context'+node['shared_pointer']
            for child in node.values():
                rebase(child)
        elif isinstance(node, list):
            for child in node:
                rebase(child)
    rebase(copied)
    return copied


def _empty(mark, side):
    return {'model_type': 'bar_scaling_check', 'schema_version': '1.0',
            'interrupted_mark': mark, 'cut_side': side, 'event_x_m': None,
            'composition_before': None, 'composition_after': None, 'remaining_composition': None,
            'remaining_capacity': None, 'moment_diagram': None, 'shear_for_al': None,
            'd_for_al': {'status': 'unresolved', 'd_cm': None}, 'bond_condition': None,
            'concretopy': {'anchorage_result': None, 'al_result': None},
            'condition_A': {'reference_point': 'x_nec', 'reference_x_m': None, 'available_length_cm': None,
                            'al_cm': None, 'ten_phi_cm': None, 'required_length_cm': None, 'passes': None,
                            'provenance': {'rule': SCALING_RULE, 'formula': 'oriented(event_x-x_nec)*100 >= al+10*phi_cm'}},
            'condition_B': {'reference_point': 'x_decay_start', 'reference_x_m': None, 'available_length_cm': None,
                            'al_cm': None, 'lb_cm': None, 'required_length_cm': None, 'passes': None,
                            'provenance': {'rule': SCALING_RULE, 'formula': 'oriented(event_x-x_decay_start)*100 >= al+lb_basic'}},
            'overall': {'complete': False, 'condition_A_passes': None, 'condition_B_passes': None, 'scaling_passes': None},
            'diagnostics': [], 'provenance': {'workflow_rule': SCALING_RULE, 'authority': 'engineer request 2026-10-05'}}


def check_scaling_event(mapping, review, diagram, shear, api, *, interrupted_mark,
                        cut_side, scope):
    """Core using already validated mapping/regions/diagram; see check_bar_scaling.

    d_for_al: Concretopy centroid of the tension composition immediately before.
    before/after mean inward/outward in the analyzed direction, not global x order.
    """
    out = _empty(interrupted_mark, cut_side)
    out.update(beam_id=mapping['beam_id'], scope=copy.deepcopy(scope), shear_for_al=copy.deepcopy(shear))
    out['audit_context'] = _review_copy(review)
    def issue(code, dependency, detail=None):
        out['diagnostics'].append({'code': code, 'dependency': dependency, 'detail': detail})
    try:
        if cut_side not in ('left', 'right'):
            raise ValueError('unsupported_cut_side')
        if not scope or not scope.get('provenance') or any(type(scope.get(k)) != type(v) or scope.get(k) != v for k, v in SUPPORTED_SCOPE.items()):
            raise ValueError('unsupported_or_unresolved_scope')
        bars = mapping['reinforcement']
        matches = [b for b in bars if b['mark'] == interrupted_mark]
        if len(matches) != 1:
            raise ValueError('interrupted_mark_not_unique')
        bar = matches[0]
        if bar.get('function') != 'positive' or bar.get('shape') != 'straight' or bar.get('face') != 'lower':
            raise ValueError('unsupported_interrupted_bar')
        for b in bars:
            if b.get('function') in ('negative', 'skin', 'anchorage_staple'):
                continue
            if dec(b['x_start_common']) >= dec(b['x_end_common']):
                raise ValueError('inconsistent_geometric_interval')
        event = bar['x_end_common' if cut_side == 'right' else 'x_start_common']
        out['event_x_m'] = event
        out['provenance']['event'] = copy.deepcopy(bar)
        supports = mapping['supports']
        if not dec(supports['left']['inner_face_x']) < dec(event) < dec(supports['right']['inner_face_x']):
            raise ValueError('cut_outside_clear_span_support_checks_not_supported')
        intervals = [r for r in review['regions'] if r['kind'] == 'interval']
        left = [r for r in intervals if dec(r['x_end_m']) == dec(event)]
        right = [r for r in intervals if dec(r['x_start_m']) == dec(event)]
        if len(left) != 1 or len(right) != 1:
            raise ValueError('event_sided_composition_not_resolved')
        before, after = (left[0], right[0]) if cut_side == 'right' else (right[0], left[0])
        def composition(region):
            c = copy.deepcopy(region['geometric_reinforcement'])
            c['bars'] = [copy.deepcopy(b) for b in bars if b['mark'] in c['marks']]
            c['region_id'] = region['region_id']
            c['provenance'] = _review_copy(region['provenance'])
            return c
        out['composition_before'], out['composition_after'] = composition(before), composition(after)
        out['remaining_composition'] = copy.deepcopy(out['composition_after'])
        bm, am = set(out['composition_before']['marks']), set(out['composition_after']['marks'])
        out['external_bends_not_checked'] = []
        for member in (b for b in bars if b['mark'] in bm):
            if member.get('shape') == 'straight' and not member.get('end_bend'):
                continue
            bend = member.get('end_bend') or {}
            bend_side = bend.get('side')
            if (member['mark'] == interrupted_mark or member.get('shape') != 'bent' or
                    bend_side not in ('left', 'right') or bend.get('direction') not in ('up', 'down') or
                    dec(bend.get('length_cm')) <= 0 or not member.get('source') or
                    dec(member.get('horizontal_length_cm')) !=
                    (dec(member['x_end_common'])-dec(member['x_start_common']))*100):
                raise ValueError('unsupported_bar_shape_or_bend')
            bend_x = member['x_start_common' if bend_side == 'left' else 'x_end_common']
            if (bend_side == 'left' and dec(bend_x) > dec(supports['left']['inner_face_x']) or
                    bend_side == 'right' and dec(bend_x) < dec(supports['right']['inner_face_x'])):
                raise ValueError('unsupported_bar_shape_or_bend')
            out['external_bends_not_checked'].append({'mark': member['mark'], 'bend_x_m': bend_x,
                'bend': copy.deepcopy(bend), 'source': copy.deepcopy(member['source']),
                'interpretation': 'Only the documented horizontal straight segment participates in span flexure; external bend and support anchorage not checked or credited'})
        out['termination_event'] = describe_termination(bm,am,interrupted_mark,event,cut_side)
        if any(r['geometric_reinforcement']['status'] != 'resolved' for r in (before, after)):
            raise ValueError('unresolved_event_composition')
        if any(r['transverse_status'] != 'resolved' for r in (before, after)) or before['transverse_geometry'] != after['transverse_geometry']:
            raise ValueError('unresolved_or_changing_event_section')
        if review.get('geometry_comparison', {}).get('status') not in (None, 'exact'):
            raise ValueError('mapping_geometry_mismatch')
        if any(s.startswith('section_geometry_mismatch') for r in (before, after) for s in r.get('blockers', [])):
            raise ValueError('section_geometry_mismatch')
        g = before['transverse_geometry']
        secao = api.SecaoRetangular(g['bw_cm'], g['h_cm'], g['cover_cm'], g['stirrup_diameter_mm'])
        before_layers = before['geometric_reinforcement']['layers']
        physical = [api.CamadaArmaduraLongitudinal(c['numero_barras'], api.Barra(c['diametro_mm'])) for c in before_layers]
        cached_before = before.get('concretopy_result') if before.get('status') == 'checked' else None
        if cached_before and cached_before.get('hipoteses_validas') is True:
            ds = cached_before['d_por_camada_cm']
            position_source = {'shared_pointer': '/before_flexure/concretopy_result/d_por_camada_cm',
                               'method': 'reuse_validated_before_flexure_layers'}
        else:
            ds = api.calcular_alturas_uteis_camadas(secao, physical)
            position_source = {'interface': api_provenance(api.calcular_alturas_uteis_camadas),
                               'method': 'Concretopy_layer_geometry_without_cached_before_flexure'}
        if len(ds) != len(before_layers) or any(not 0 < dec(d) < dec(g['h_cm']) for d in ds):
            raise ValueError('unresolved_physical_layer_positions')
        positions = {c['layer']: d for c, d in zip(before_layers, ds)}
        out['physical_layer_positions'] = {'d_cm_by_layer': positions, 'geometry': copy.deepcopy(g),
            'provenance': {**position_source, 'composition': '/composition_before',
                           'section': _review_copy(before['provenance']['transverse'])}}
        remaining = [api.CamadaArmaduraLongitudinal(c['numero_barras'], api.Barra(c['diametro_mm']), positions[c['layer']])
                     for c in after['geometric_reinforcement']['layers']]
        phi = bar['diameter_mm']
        out['condition_A']['ten_phi_cm'] = float(10*(dec(phi)/10))
        out['condition_A']['provenance']['diameter'] = {'mark': interrupted_mark, 'diameter_mm': phi, 'source': copy.deepcopy(bar['source'])}
    except (ValueError, TypeError, KeyError, IndexError) as error:
        issue(str(error), 'geometry_or_scope')
        return out

    # Bond geometry independent of the unresolved choice of d for al.
    try:
        layers = [i+1 for i, n in enumerate(bar['layers']) if n]
        if len(layers) != 1:
            raise ValueError('interrupted_mark_multiple_layers_not_supported')
        y = g['h_cm'] - positions[layers[0]]
        bond = classify_bond(g['h_cm'], y)
        bond['provenance'].update(geometry='/physical_layer_positions', interrupted_bar='/provenance/event',
                                  calculation='y = h - d_of_interrupted_physical_layer; center from bottom')
        out['bond_condition'] = bond
    except (ValueError, TypeError, KeyError) as error:
        issue(str(error), 'bond_condition')

    mk = None
    try:
        material = review['material_parameters']
        steel = review['material_interpretation']
        if steel['status'] != 'consistent' or material['fck_mpa'] is None or material['gamma_f'] is None:
            raise ValueError('unresolved_materials')
        concrete, steel_obj = api.Concreto(material['fck_mpa']), api.Aco(steel['derived_fyk_mpa'])
        signature = inspect.signature(api.verificar_flexao_viga_retangular)
        co = {k: signature.parameters[k].default for k in ('gamma_c', 'gamma_s')}
        co['gamma_f'] = material['gamma_f']
        out['concretopy']['materials'] = {'fck_mpa': concrete.fck, 'fyk_mpa': steel_obj.fyk, 'coefficients': co,
                                        'provenance': '/audit_context/material_parameters'}
    except (ValueError, TypeError, KeyError) as error:
        issue(str(error), 'materials')
        concrete = None
    if concrete is not None:
        # d for al belongs to the BEFORE tension composition, independently of the
        # remaining capacity used by x_nec. Reuse the audited region when available.
        try:
            if cached_before and cached_before.get('hipoteses_validas') is True:
                before_result = copy.deepcopy(cached_before)
                method = 'reuse_before_region_flexure'
            else:
                positioned_before = [api.CamadaArmaduraLongitudinal(c['numero_barras'], api.Barra(c['diametro_mm']), positions[c['layer']])
                                     for c in before_layers]
                before_result = asdict(api.verificar_flexao_viga_retangular(
                    secao, concrete, steel_obj, positioned_before, **co, verificar_armadura_minima=False))
                method = 'Concretopy_before_composition_flexure'
            out['before_flexure'] = {'concretopy_result': before_result,
                'provenance': {'interface': api_provenance(api.verificar_flexao_viga_retangular),
                               'method': method, 'region_id': before['region_id'],
                               'composition': '/composition_before', 'geometry': '/physical_layer_positions/geometry',
                               'materials': '/concretopy/materials'}}
            d = before_result['d_equivalente_cm']
            areas, depths = before_result['as_por_camada_cm2'], before_result['d_por_camada_cm']
            if (before_result['hipoteses_validas'] is not True or
                    len(areas) != len(before_layers) or len(depths) != len(before_layers) or
                    any(dec(area) <= 0 for area in areas) or
                    any(not 0 < dec(depth) < dec(g['h_cm']) for depth in depths) or
                    not 0 < dec(d) < dec(g['h_cm'])):
                raise ValueError('invalid_before_tension_centroid')
            out['d_for_al'] = {'status': 'resolved', 'd_cm': d, 'rule': DEPTH_RULE,
                'composition_marks': list(out['composition_before']['marks']),
                'contributions': [{'layer': layer['layer'], 'components': copy.deepcopy(layer['components']),
                                   'As_cm2': area, 'd_cm': depth}
                                  for layer, area, depth in zip(before_layers, areas, depths)],
                'provenance': {'rule_reference': 'tools/reinforcement_checks/al_effective_depth.md',
                               'centroid': '/before_flexure/concretopy_result/d_equivalente_cm',
                               'areas': '/before_flexure/concretopy_result/as_por_camada_cm2',
                               'depths': '/before_flexure/concretopy_result/d_por_camada_cm',
                               'composition': '/composition_before',
                               'selection': 'Area-weighted centroid of all tension bars participating in positive flexure immediately before the cut; Concretopy centroid reused'}}
        except (ValueError, TypeError, KeyError) as error:
            issue('d_for_al_unresolved', 'al', str(error))
        try:
            response = api.verificar_flexao_viga_retangular(secao, concrete, steel_obj, remaining,
                                                           **co, verificar_armadura_minima=False)
            out['remaining_capacity'] = {'MRd_knm': None if response.mrd_kncm is None else response.mrd_kncm/100,
                'Mk_equivalent_knm': None if response.mk_equivalente_kncm is None else response.mk_equivalente_kncm/100,
                'concretopy_result': asdict(response),
                'call': {'geometry': g, 'layers': [asdict(c) for c in remaining], 'coefficients': co,
                         'verificar_armadura_minima': False},
                'provenance': {'interface': api_provenance(api.verificar_flexao_viga_retangular),
                               'composition': '/remaining_composition', 'positions': '/physical_layer_positions',
                               'materials': '/concretopy/materials', 'conversion': 'kN.cm / 100 = kN.m'}}
            candidate = out['remaining_capacity']['Mk_equivalent_knm']
            if response.hipoteses_validas is not True or dec(candidate) <= 0 or dec(response.mrd_kncm) <= 0:
                raise ValueError('invalid_remaining_capacity')
            mk = candidate
        except (ValueError, TypeError, KeyError) as error:
            issue('concretopy_capacity_rejected', 'remaining_capacity', str(error))
        if out['bond_condition'] is not None:
            try:
                area = api.Barra(phi).area_cm2 * bar['bars']
                call = {'bitola_mm': phi, 'as_calculada_cm2': area, 'as_efetiva_cm2': area,
                        'gamma_c': co['gamma_c'], 'gamma_s': co['gamma_s']}
                response = api.calcular_ancoragem(concrete, steel_obj, **call,
                    condicoes=api.CondicoesAncoragem(boa_aderencia=out['bond_condition']['boa_aderencia']))
                if dec(response.lb_cm) <= 0:
                    raise ValueError('invalid_lb')
                out['concretopy'].update(anchorage_result=asdict(response), anchorage_call=call,
                    anchorage_provenance={'interface': api_provenance(api.calcular_ancoragem),
                        'materials': '/concretopy/materials', 'bond': '/bond_condition', 'bar': '/provenance/event',
                        'area_basis': 'Interrupted mark area via Barra; full fyd anchorage, equal areas; no excess-steel reduction or available length supplied',
                        'used_quantity': 'lb_cm basic; lb_nec and atende do not decide condition B'})
                out['condition_B']['lb_cm'] = response.lb_cm
            except (ValueError, TypeError, KeyError) as error:
                issue('concretopy_anchorage_rejected', 'lb', str(error))

    references = locate_references(diagram, mk, cut_side, event)
    if references['peak'] is not None:
        peak_x = dec(references['peak']['x_m'])
        references['peak']['location_relative_to_clear_span'] = (
            'left_support' if peak_x < dec(supports['left']['inner_face_x']) else
            'right_support' if peak_x > dec(supports['right']['inner_face_x']) else 'clear_span')
        references['peak']['scope_note'] = 'Force-diagram reference only; no support anchorage or support transverse geometry inferred'
    out['moment_diagram'] = references
    for code in references['diagnostics']:
        issue(code, 'moment_references')
    sign = 1 if cut_side == 'right' else -1
    for key, point in (('condition_A', references['selected_x_nec_m']),
                       ('condition_B', None if references['peak'] is None else references['peak']['x_m'])):
        if point is not None:
            condition = out[key]
            condition['reference_x_m'] = point
            reference_decimal = Decimal(references['selected_crossing']['x_decimal']) if key == 'condition_A' else dec(point)
            with localcontext() as context:
                context.prec = 50
                available = sign*(dec(event)-reference_decimal)*100
            condition['available_length_cm'] = float(available)
            condition['available_length_decimal_cm'] = str(available)
            condition['provenance'].update(event='/provenance/event', reference='/moment_diagram')
            if condition['available_length_cm'] < 0:
                issue('negative_available_length', key)
    # Validate that the selected capacity/position is applicable between references and cut.
    refs = [p for p in (references['selected_x_nec_m'], None if references['peak'] is None else references['peak']['x_m']) if p is not None]
    if refs:
        lo, hi = min(map(dec, refs+[event])), max(map(dec, refs+[event]))
        if dec(bar['x_start_common']) > lo or dec(bar['x_end_common']) < hi:
            issue('interrupted_bar_does_not_cover_references', 'geometry')
        for r in intervals:
            if dec(r['x_start_m']) < hi and dec(r['x_end_m']) > lo:
                in_clear = (dec(r['x_start_m']) < min(hi, dec(supports['right']['inner_face_x'])) and
                            dec(r['x_end_m']) > max(lo, dec(supports['left']['inner_face_x'])))
                # A force reference inside a support does not infer its transverse
                # detailing. Composition remains constant; section checks cover the span.
                if (set(r['geometric_reinforcement']['marks']) != bm or
                        in_clear and r['transverse_geometry'] != g):
                    issue('changing_configuration_between_references_and_cut', 'geometry')
                    break

    if out['d_for_al']['status'] != 'resolved' and not any(d['code'] == 'd_for_al_unresolved' for d in out['diagnostics']):
        issue('d_for_al_unresolved', 'al', 'Before tension composition centroid unavailable')
    if out['d_for_al']['status'] != 'resolved':
        out['d_for_al'].update(rule=DEPTH_RULE,
            provenance={'geometry': '/physical_layer_positions', 'composition': '/composition_before',
                        'rule_reference': 'tools/reinforcement_checks/al_effective_depth.md'})
    if not shear or shear.get('status') != 'resolved':
        issue('shear_for_al_unresolved', 'al', None if not shear else shear.get('diagnostic'))
    if concrete is not None and out['d_for_al']['status'] == 'resolved' and shear and shear.get('status') == 'resolved':
        try:
            call = {'b_cm': g['bw_cm'], 'd_cm': out['d_for_al']['d_cm'],
                    'vk_abs_kn': shear['Vk_used_kn'], 'gamma_f': co['gamma_f'], 'gamma_c': co['gamma_c']}
            response = api.calcular_al(concreto=concrete, **call)
            if dec(response.al_cm) <= 0:
                raise ValueError('invalid_al')
            out['concretopy'].update(al_result=asdict(response), al_call=call,
                al_provenance={'interface': api_provenance(api.calcular_al), 'd': '/d_for_al',
                               'shear': '/shear_for_al', 'materials': '/concretopy/materials',
                               'section': '/physical_layer_positions/geometry'})
            for key in ('condition_A', 'condition_B'):
                out[key]['al_cm'] = response.al_cm
        except (ValueError, TypeError, KeyError) as error:
            issue('concretopy_al_rejected', 'al', str(error))
    for key, extension in (('condition_A', 'ten_phi_cm'), ('condition_B', 'lb_cm')):
        c = out[key]
        c['provenance'].update(al='/concretopy/al_result', extension='/provenance/event' if key == 'condition_A' else '/concretopy/anchorage_result/lb_cm')
        if c['al_cm'] is not None and c[extension] is not None:
            required = dec(c['al_cm'])+dec(c[extension])
            c['required_length_cm'] = float(required)
            c['required_length_decimal_cm'] = str(required)
            if c['available_length_cm'] is not None and c['available_length_cm'] >= 0:
                c['passes'] = Decimal(c['available_length_decimal_cm']) >= required
    a, b = out['condition_A']['passes'], out['condition_B']['passes']
    complete = not out['diagnostics'] and a is not None and b is not None
    out['overall'] = {'complete': complete, 'condition_A_passes': a, 'condition_B_passes': b,
                      'scaling_passes': (a and b) if complete else None}
    return out


def check_bar_scaling(detail, tqs, positioned, mapping, raw, api, *, interrupted_mark,
                      cut_side, scope):
    """Public adapter: reuses existing validation, region and moment infrastructure."""
    try:
        review = check_positive_flexure(detail, tqs, positioned, mapping, raw, api)
        diagram = diagram_from_tqs(mapping, tqs, positioned, raw)
    except (ValueError, TypeError, KeyError, IndexError) as error:
        out = _empty(interrupted_mark, cut_side)
        out['diagnostics'].append({'code': 'invalid_pipeline_input', 'dependency': 'pipeline', 'detail': str(error)})
        return out
    try:
        shear = shear_from_tqs(mapping, tqs, positioned, raw)
    except (ValueError, TypeError, KeyError, IndexError) as error:
        shear = {'status': 'unresolved', 'diagnostic': str(error)}
    return check_scaling_event(mapping, review, diagram, shear, api,
        interrupted_mark=interrupted_mark, cut_side=cut_side, scope=scope)
