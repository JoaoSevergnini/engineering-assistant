"""Complementary anchorage studies, without changing principal reinforcement.

Engineering decisions (area target and length) are orchestration; materials,
bar areas, basic anchorage, support demand and resistance remain in Concretopy.
No geometry is inferred from the word staple, nor any final solution selected.
"""
from copy import deepcopy
from dataclasses import asdict
from math import ceil, isfinite

from bar_scaling import api_provenance, classify_bond
from support_alternatives import _number, _integer
from support_correction import correction_workflow, transverse_fit

LENGTH_RULE = 'engineer_confirmed_support_staple_length_v1'
DEFAULT_STAPLE_DIAMETERS_MM = (6.3, 8, 10)
GEOMETRY_RULE = 'engineer_confirmed_support_staple_u_geometry_v1'
QUANTITY_RULE = 'engineer_confirmed_support_staple_usual_quantity_v1'
AREA_RULE = 'engineer_confirmed_support_staple_area_target_v1'
VERTICAL_RULE = 'engineer_confirmed_support_staple_vertical_distribution_v1'
LIMITATIONS = [
    'geometria_da_dobra_nao_verificada', 'interferencias_no_no_nao_verificadas',
    'ancoragem_conjunta_nao_verificada', 'nao_aprova_viga']


def staple_length(lb_grampo_cm, lb_ef_cm):
    """Engineer-confirmed length, cm; basic lb, without al or hook reduction."""
    _number(lb_grampo_cm, 'lb_grampo_cm', positive=True)
    _number(lb_ef_cm, 'lb_ef_cm', positive=True)
    development = 2 * lb_grampo_cm + lb_ef_cm
    if not isfinite(development):
        raise ValueError('non_finite_staple_length')
    return {'two_lb_plus_lb_ef_cm': development,
            'minimum_absolute_cm': 60.0, 'L_grampo_min_cm': max(development, 60.0),
            'L_long_cm': max(development, 60.0),
            'governing_term': 'ANCORAGEM' if development >= 60 else 'MINIMO_60_CM',
            'governing_terms': ['ANCORAGEM', 'MINIMO_60_CM'] if development == 60 else
                ['ANCORAGEM' if development > 60 else 'MINIMO_60_CM'],
            'rule': LENGTH_RULE}


def staple_geometry(L_long_cm, b_cm, cover_cm):
    """Nominal engineer-defined U dimensions, not fabrication or coordinates."""
    _number(L_long_cm, 'L_long_cm', positive=True)
    _number(b_cm, 'b_cm', positive=True)
    _number(cover_cm, 'cover_cm')
    if cover_cm < 0:
        raise ValueError('negative_staple_cover')
    transverse = b_cm - 2 * cover_cm - 1
    _number(transverse, 'L_transversal_cm', positive=True)
    nominal = 2 * L_long_cm + transverse
    if not isfinite(nominal):
        raise ValueError('non_finite_staple_nominal_length')
    return {'shape': 'U', 'plane_description': 'vertical_longitudinal',
        'longitudinal_leg_count': 2, 'L_long_cm': L_long_cm,
        'b_cm': b_cm, 'cover_cm': cover_cm, 'transverse_allowance_cm': 1.0,
        'L_transversal_cm': transverse, 'L_geometrico_nominal_cm': nominal,
        'fabrication_cut_length_cm': None, 'coordinates_verified': False,
        'rule': GEOMETRY_RULE,
        'note': 'Connector dimension follows beam width by engineer decision; plane/coordinates and bends not inferred.'}


def vertical_distribution(quantity, diameter_mm, *, section=None, window=None):
    """Defined spacing, necessary envelope check, optional positioned fit.

    Window uses external faces in cm from beam bottom, explicitly supplied.
    Concrete cover envelope is a necessary bound, not proof of node clearance.
    No initial level or interference clearance is inferred from principal bars.
    """
    _integer(quantity, 'quantity')
    _number(diameter_mm, 'diameter_mm', positive=True)
    phi_cm = diameter_mm / 10
    occupied = quantity * phi_cm + (quantity - 1) * 2.0
    if not isfinite(occupied):
        raise ValueError('non_finite_staple_occupied_height')
    out = {'rule': VERTICAL_RULE, 'quantity': quantity, 'phi_cm': phi_cm,
        'distribuicao_vertical_definida': True, 'orientacao_distribuicao': 'vertical',
        'ordem_distribuicao': 'de_baixo_para_cima', 'espacamento_vertical_livre_cm': 2.0,
        'espacamento_vertical_eixos_cm': 2.0 + phi_cm,
        'altura_ocupada_cm': occupied, 'cabimento_vertical_envelope': None,
        'cabimento_vertical': None, 'distribuicao_vertical_verificada': False,
        'interferencias_do_no_verificadas': False, 'ready_for_detailing': False,
        'diagnostics': [], 'provenance': {'spacing': 'Engineer final vertical distribution decision'}}
    if section is not None:
        try:
            h, cover = section['h'], section['cobrimento']
            _number(h, 'h_cm', positive=True); _number(cover, 'cover_cm')
            if cover < 0 or 2*cover >= h:
                raise ValueError('invalid_vertical_cover_envelope')
            height = h - 2*cover
            out.update(envelope_bottom_cm=cover, envelope_top_cm=h-cover,
                altura_envelope_disponivel_cm=height,
                cabimento_vertical_envelope=occupied <= height)
            out['provenance']['envelope'] = {'section': deepcopy(section),
                'scope': 'Necessary geometric bound between concrete-cover limits; does not place first staple'}
            if occupied > height:
                out['cabimento_vertical'] = False
                out['diagnostics'].append('altura_ocupada_excede_envelope_vertical')
        except (ValueError, TypeError, KeyError) as error:
            out['diagnostics'].append('envelope_vertical_nao_resolvido:' + str(error))
    if window is not None:
        try:
            if not window.get('provenance'):
                raise ValueError('vertical_window_provenance_missing')
            bottom, top = window['bottom_cm'], window['top_cm']
            _number(bottom, 'window_bottom_cm'); _number(top, 'window_top_cm')
            if bottom < 0 or top <= bottom:
                raise ValueError('invalid_vertical_window')
            if out.get('envelope_bottom_cm') is not None and (
                bottom < out['envelope_bottom_cm'] or top > out['envelope_top_cm']):
                raise ValueError('vertical_window_outside_cover_envelope')
            fits = occupied <= top-bottom
            out.update(window=deepcopy(window), altura_vertical_disponivel_cm=top-bottom,
                first_center_from_bottom_cm=bottom+phi_cm/2,
                last_center_from_bottom_cm=bottom+phi_cm/2+(quantity-1)*(2.0+phi_cm),
                stack_top_face_cm=bottom+occupied,
                cabimento_vertical=fits, distribuicao_vertical_verificada=True)
            out['provenance']['placement'] = deepcopy(window['provenance'])
            if not fits: out['diagnostics'].append('grampos_nao_cabem_na_janela_vertical')
        except (ValueError, TypeError, KeyError) as error:
            out['diagnostics'].append('posicionamento_vertical_nao_resolvido:' + str(error))
    else:
        out['diagnostics'].append('posicao_inicial_e_limite_vertical_dos_grampos_pendentes')
    return out


def usual_quantity(quantity, *, usual_max=3):
    """Detailing preference only; never a resistance rejection."""
    _integer(usual_max, 'usual_max')
    if quantity is not None and (type(quantity) is not int or quantity < 0):
        raise ValueError('invalid_staple_quantity')
    return {'usual_quantity_max': usual_max,
        'quantidade_usual': None if quantity is None else quantity <= usual_max,
        'requer_avaliacao_especial': None if quantity is None else quantity > usual_max,
        'quantity_preference_rule': QUANTITY_RULE}


def quantity_for_area(required_cm2, unit_bar_cm2, *, contributing_legs=None):
    """No default number of contributing legs per fabricated piece.

    Equivalent bar count is available even if the piece shape is unresolved.
    A leg multiplier is an explicit caller decision, never inferred from a U.
    """
    _number(required_cm2, 'required_cm2')
    _number(unit_bar_cm2, 'unit_bar_cm2', positive=True)
    if required_cm2 < 0:
        raise ValueError('negative_complementary_area')
    if contributing_legs is not None:
        _integer(contributing_legs, 'contributing_legs')
    if required_cm2 == 0:
        return {'equivalent_bar_count': 0, 'quantity': 0, 'contributing_legs': contributing_legs,
                'As_unit_bar_cm2': unit_bar_cm2, 'As_unit_piece_cm2': None if contributing_legs is None else unit_bar_cm2 * contributing_legs,
                'As_supplied_cm2': 0.0, 'area_excess_cm2': 0.0, 'area_sufficient': True}
    equivalent = ceil(required_cm2 / unit_bar_cm2)
    quantity = None if contributing_legs is None else ceil(required_cm2 / (unit_bar_cm2 * contributing_legs))
    supplied = None if quantity is None else quantity * unit_bar_cm2 * contributing_legs
    return {'equivalent_bar_count': equivalent, 'quantity': quantity,
            'contributing_legs': contributing_legs, 'As_unit_bar_cm2': unit_bar_cm2,
            'As_unit_piece_cm2': None if contributing_legs is None else unit_bar_cm2 * contributing_legs,
            'As_supplied_cm2': supplied,
            'area_excess_cm2': None if supplied is None else supplied - required_cm2,
            'area_sufficient': None if supplied is None else supplied >= required_cm2}


def _bond(context, scenario):
    if not scenario.get('provenance'):
        raise ValueError('staple_bond_provenance_missing')
    if scenario.get('bar_center_from_bottom_cm') is not None:
        if scenario.get('horizontal') is not True or scenario.get('sliding_formwork') is not False:
            raise ValueError('unsupported_staple_bond_geometry')
        result = classify_bond(context['section']['h'], scenario['bar_center_from_bottom_cm'])
        if 'boa_aderencia' in scenario and scenario['boa_aderencia'] != result['boa_aderencia']:
            raise ValueError('staple_bond_geometry_conflicts_with_scenario')
        result.update(scenario_status='physical_position', provenance=deepcopy(scenario['provenance']))
        return result
    if type(scenario.get('boa_aderencia')) is not bool or scenario.get('status') not in ('confirmed', 'hypothesis'):
        raise ValueError('staple_bond_unresolved')
    return {'boa_aderencia': scenario['boa_aderencia'], 'bar_center_from_bottom_cm': None,
            'classification': 'good' if scenario['boa_aderencia'] else 'poor',
            'scenario_status': scenario['status'], 'provenance': deepcopy(scenario['provenance'])}


def evaluate_staple(context, required_area_cm2, lb_ef_cm, diameter_mm, api, *,
                    bond_scenario, contributing_legs=None, leg_provenance=None,
                    distribution=None, target_provenance=None, usual_max=3, vertical_window=None):
    """Compute quantities and basic-lb length; unresolved placement stays null.

    Optional distribution supplies full layer occupancy (principal + staples),
    plus leg identities. It checks horizontal fit only, not vertical spacing,
    bend/confinement or transfer of the complementary force.
    """
    out = {'origin': 'GRAMPO', 'diameter_mm': diameter_mm, 'As_required_cm2': required_area_cm2,
        'lb_ef_cm': lb_ef_cm, 'complete_calculation': False, 'quantity': None,
        'ready_for_detailing': False, 'cabimento': None, 'distribution_verified': False,
        'distribuicao_vertical_verificada': False, 'distribuicao_vertical_definida': True,
        'interferencias_do_no_verificadas': False, 'geometry': None,
        'combined_anchorage_passes': None, 'diagnostics': [], 'limitations': list(LIMITATIONS),
        'provenance': {'area_target_rule': AREA_RULE, 'area_target': deepcopy(target_provenance),
            'legs': deepcopy(leg_provenance), 'bond_scenario': deepcopy(bond_scenario)}}
    try:
        _number(diameter_mm, 'diameter_mm', positive=True)
        _number(required_area_cm2, 'required_area_cm2', positive=True)
        _number(lb_ef_cm, 'lb_ef_cm', positive=True)
        if contributing_legs is not None and not leg_provenance:
            raise ValueError('contributing_legs_provenance_missing')
        if contributing_legs not in (None, 2):
            raise ValueError('u_staple_requires_two_contributing_legs')
        bar = api.Barra(diameter_mm)
        bond = _bond(context, bond_scenario)
        out['bond_condition'] = bond
        quantities = quantity_for_area(required_area_cm2, bar.area_cm2, contributing_legs=contributing_legs)
        out.update(quantities)
        out.update(usual_quantity(out['quantity'], usual_max=usual_max))
        if out['quantity'] is not None:
            vertical = vertical_distribution(out['quantity'], diameter_mm,
                section=context.get('section'), window=vertical_window or context.get('staple_vertical_window'))
            out['vertical_distribution'] = vertical
            for key in ('distribuicao_vertical_definida', 'distribuicao_vertical_verificada',
                        'orientacao_distribuicao', 'ordem_distribuicao',
                        'espacamento_vertical_livre_cm', 'espacamento_vertical_eixos_cm',
                        'altura_ocupada_cm', 'cabimento_vertical', 'cabimento_vertical_envelope'):
                out[key] = vertical[key]
            out['diagnostics'] += vertical['diagnostics']
            out['provenance']['vertical_distribution'] = deepcopy(vertical['provenance'])
        if out['requer_avaliacao_especial']:
            out['diagnostics'].append('quantidade_acima_do_usual_requer_avaliacao_especial')
        # Equal unit areas avoid any area reduction; use ONLY returned basic lb.
        anchorage = api.calcular_ancoragem(concreto=api.Concreto(context['fck_mpa']),
            aco=api.Aco(context['fyk_mpa']), bitola_mm=diameter_mm,
            as_calculada_cm2=bar.area_cm2, as_efetiva_cm2=bar.area_cm2,
            condicoes=api.CondicoesAncoragem(bond['boa_aderencia']),
            gamma_c=context['gamma_c'], gamma_s=context['gamma_s'])
        out['concretopy_anchorage'] = asdict(anchorage)
        out['lb_grampo_cm'] = anchorage.lb_cm
        out.update(staple_length(anchorage.lb_cm, lb_ef_cm))
        try:
            geometry = staple_geometry(out['L_long_cm'], context['section']['bw'], context['cover_cm'])
            if context['section'].get('cobrimento') != context['cover_cm']:
                raise ValueError('cover_context_mismatch')
            out['geometry'] = geometry
            out.update({key: geometry[key] for key in ('b_cm', 'cover_cm', 'L_transversal_cm', 'L_geometrico_nominal_cm')})
            out['provenance']['geometry'] = {'rule': GEOMETRY_RULE,
                'section': deepcopy(context['section']), 'source': deepcopy(context.get('provenance')),
                'engineering_decision': 'Current U geometry procedure; no bend allowances formalized'}
        except (ValueError, TypeError, KeyError) as error:
            out['diagnostics'].append('geometria_nominal_nao_resolvida:' + str(error))
        out['api_provenance'] = {'basic_anchorage': api_provenance(api.calcular_ancoragem),
            'bar_area': api_provenance(api.Barra)}
        if contributing_legs is None:
            out['diagnostics'].append('quantidade_de_ramos_resistentes_nao_definida')
        if bond['scenario_status'] == 'hypothesis':
            out['diagnostics'].append('aderencia_do_grampo_nao_confirmada')
        if distribution is not None:
            if not distribution.get('provenance') or out['quantity'] is None:
                raise ValueError('staple_distribution_incomplete')
            # Validate complete occupancy and exact added leg count/diameter.
            layers = distribution['layers']
            placed = sum(l.get('staple_leg_count', 0) for l in layers)
            if placed != out['quantity'] * contributing_legs:
                raise ValueError('staple_leg_occupancy_mismatch')
            for layer in layers:
                _integer(layer['staple_leg_count'], 'staple_leg_count')
                if layer.get('diameters_mm', []).count(diameter_mm) < layer['staple_leg_count']:
                    raise ValueError('staple_diameter_missing_from_occupancy')
            fit = transverse_fit(context['section'], layers, api)
            out.update(horizontal_fit=fit, cabimento=fit['cabimento_transversal'],
                       distribution_input=deepcopy(distribution))
            if out['cabimento'] is False:
                out['diagnostics'].append('grampo_nao_cabe_transversalmente')
        if out.get('cabimento_vertical') is False:
            out['cabimento'] = False
        out['diagnostics'].append('interferencias_no_no_nao_verificadas')
        out['complete_calculation'] = contributing_legs is not None and bond['scenario_status'] != 'hypothesis' and out['geometry'] is not None
        out['status'] = 'CALCULO_COMPLETO_NO_PENDENTE' if out['complete_calculation'] else 'CALCULO_PARCIAL_HIPOTESES_PENDENTES'
    except (ValueError, TypeError, KeyError, AttributeError, OverflowError) as error:
        out['diagnostics'].append('grampo_nao_avaliavel:' + str(error))
        out['status'] = 'NAO_AVALIAVEL'
    return out


def staple_workflow(context, bars, diagram, api, *, redistribution_search,
                    diameters_mm=DEFAULT_STAPLE_DIAMETERS_MM, bond_scenarios, contributing_legs=None,
                    leg_provenance=None, study_with_valid_extension=False, usual_max=3):
    """Preserve correction hierarchy; explicit comparison may study staples too."""
    correction = correction_workflow(context, bars, diagram, api,
                                     redistribution_search=redistribution_search)
    out = {'correction': correction, 'original_composition': deepcopy(bars),
           'staples': [], 'comparison': [], 'selected_solution': None,
           'next_step': correction['next_step'], 'diagnostics': [],
           'search': {'diameters_mm': list(diameters_mm), 'bond_scenarios': deepcopy(bond_scenarios),
                      'contributing_legs': contributing_legs, 'usual_max': usual_max, 'study_with_valid_extension': study_with_valid_extension}}
    current = correction['existing']['support_check']
    if not current['complete']:
        out['diagnostics'].append('configuracao_existente_inconclusiva')
        return out
    out['As_grampo_required_cm2'] = current['metrics']['As_additional_cm2']
    if current['passes']:
        out['diagnostics'].append('nenhuma_armadura_complementar_necessaria')
        return out
    if out['As_grampo_required_cm2'] <= 0:
        out['diagnostics'].append('falha_nao_resolvida_por_area_complementar')
        return out
    if correction['next_step'] != 'AVALIAR_ARMADURA_COMPLEMENTAR' and not study_with_valid_extension:
        out['diagnostics'].append('preservada_prioridade_da_correcao_principal')
        return out
    if not diameters_mm or not bond_scenarios:
        out['diagnostics'].append('busca_de_grampos_sem_bitolas_ou_aderencia')
        return out
    target = {'source': 'existing.support_check.anchorage.as_adicional_cm2',
              'api': deepcopy(current['api_provenance']),
              'available_length': deepcopy(current['available_length']),
              'rule': AREA_RULE}
    for phi in dict.fromkeys(diameters_mm):
        for scenario in bond_scenarios:
            c = evaluate_staple(context, out['As_grampo_required_cm2'], current['metrics']['lb_ef_cm'],
                phi, api, bond_scenario=scenario, contributing_legs=contributing_legs,
                leg_provenance=leg_provenance, target_provenance=target, usual_max=usual_max)
            c['id'] = f'staple_{phi:g}_' + str(scenario.get('id', 'bond'))
            out['staples'].append(c)
            out['comparison'].append({'id': c['id'], 'origin': 'GRAMPO',
                'principal_reinforcement_preserved': True,
                'positive_flexure_passes': correction['existing']['longitudinal_check']['compatibilidade_flexao_positiva'],
                'added_pieces': c.get('quantity'), 'extended_bars': 0,
                'added_area_cm2': c.get('As_supplied_cm2'),
                'minimum_staple_length_cm': c.get('L_grampo_min_cm'),
                'longitudinal_leg_length_cm': c.get('L_long_cm'),
                'transverse_connector_length_cm': c.get('L_transversal_cm'),
                'nominal_geometric_length_cm': c.get('L_geometrico_nominal_cm'),
                'quantidade_usual': c.get('quantidade_usual'),
                'requer_avaliacao_especial': c.get('requer_avaliacao_especial'),
                'vertical_distribution': deepcopy(c.get('vertical_distribution')),
                'interferencias_do_no_verificadas': False,
                'added_horizontal_length_cm': None, 'developed_fabrication_length_cm': None,
                'cabimento': c['cabimento'], 'anchorage_passes': None,
                'requires_bend': True, 'ready_for_detailing': False,
                'limitations': deepcopy(c['limitations'])})
    for c in correction['extensions']:
        changes = c['changes']
        extra = sum((ch['added_horizontal_length_cm'] if 'added_horizontal_length_cm' in ch else (ch['original_start_m'] - ch['proposed_start_m']) * 100) * ch['extended_quantity'] for ch in changes)
        metrics = c['support_check'].get('metrics') or {}
        out['comparison'].append({'id': c['id'], 'origin': 'PROLONGAMENTO',
            'principal_reinforcement_preserved': c.get('original_span_reinforcement_preserved'),
            'positive_flexure_passes': c['longitudinal_check']['compatibilidade_flexao_positiva'],
            'added_pieces': 0, 'extended_bars': sum(ch['extended_quantity'] for ch in changes),
            'added_area_cm2': None if not metrics else metrics['As_effective_cm2'] - current['metrics']['As_effective_cm2'],
            'minimum_staple_length_cm': None, 'added_horizontal_length_cm': extra,
            'developed_fabrication_length_cm': None, 'changes': deepcopy(changes),
            'cabimento': c['cabimento_transversal'], 'anchorage_passes': c['support_check']['passes'],
            'requires_bend': context['gancho_valido'], 'ready_for_detailing': False,
            'limitations': deepcopy(c['limitations'])})
    return out
