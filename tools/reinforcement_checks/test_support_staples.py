"""Staple engineering decisions and real Concretopy orchestration contracts."""
from copy import deepcopy
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch
from support_staples import staple_length, quantity_for_area, evaluate_staple, staple_workflow, staple_geometry, usual_quantity, DEFAULT_STAPLE_DIAMETERS_MM, vertical_distribution

ROOT = Path(__file__).resolve().parents[2]
spec = spec_from_file_location('staple_fixture', ROOT/'analises/pranchas/validar_v536_v565_grampos.py')
fixture = module_from_spec(spec); spec.loader.exec_module(fixture)
api = fixture.api

class StapleTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.real = fixture.study('V536')
        cls.control = fixture.study('V565')
    def setUp(self):
        self.ctx, self.bars, self.diagram = fixture.load_detail_case('V536')
    def candidate(self, phi=10, **kwargs):
        return evaluate_staple(self.ctx, self.real['As_grampo_required_cm2'], 21.5, phi, api,
            bond_scenario=kwargs.pop('bond_scenario', fixture.BOND[0]),
            contributing_legs=kwargs.pop('contributing_legs', 2),
            leg_provenance=fixture.LEGS, **kwargs)
    def test_twice_basic_plus_available(self):
        r = staple_length(40, 21.5)
        self.assertEqual(r['two_lb_plus_lb_ef_cm'], 101.5)
        self.assertEqual(r['L_grampo_min_cm'], 101.5)
    def test_absolute_minimum_governs(self):
        r = staple_length(15, 20)
        self.assertEqual(r['L_grampo_min_cm'], 60)
        self.assertEqual(r['governing_term'], 'MINIMO_60_CM')
    def test_anchorage_governs(self):
        self.assertEqual(staple_length(30, 21.5)['governing_term'], 'ANCORAGEM')
    def test_equal_terms_preserved(self):
        self.assertEqual(staple_length(20, 20)['governing_terms'], ['ANCORAGEM', 'MINIMO_60_CM'])
    def test_own_basic_lb_for_each_diameter(self):
        a, b = self.candidate(10), self.candidate(20)
        self.assertNotEqual(a['lb_grampo_cm'], b['lb_grampo_cm'])
        for c in (a, b):
            self.assertEqual(c['lb_grampo_cm'], c['concretopy_anchorage']['lb_cm'])
            self.assertEqual(c['L_grampo_min_cm'], max(2*c['lb_grampo_cm']+21.5, 60))
    def test_basic_not_minimum_or_necessary(self):
        c = self.candidate(10)
        self.assertNotEqual(c['lb_grampo_cm'], c['concretopy_anchorage']['lb_min_cm'])
    def test_quantity_by_two_legs(self):
        r = quantity_for_area(3, 1, contributing_legs=2)
        self.assertEqual(r['quantity'], 2); self.assertEqual(r['As_supplied_cm2'], 4)
    def test_quantity_rounds_up(self):
        self.assertEqual(quantity_for_area(4.01, 1, contributing_legs=2)['quantity'], 3)
    def test_exact_integer_without_extra_piece(self):
        self.assertEqual(quantity_for_area(4, 1, contributing_legs=2)['quantity'], 2)
    def test_excess_area(self):
        self.assertEqual(quantity_for_area(3, 1, contributing_legs=2)['area_excess_cm2'], 1)
    def test_zero_area(self):
        self.assertEqual(quantity_for_area(0, 1, contributing_legs=2)['quantity'], 0)
    def test_unknown_legs_not_silently_doubled(self):
        c = self.candidate(contributing_legs=None)
        self.assertIsNone(c['quantity']); self.assertIsNone(c['As_supplied_cm2'])
        self.assertIn('quantidade_de_ramos_resistentes_nao_definida', c['diagnostics'])
        self.assertIsNotNone(c['L_grampo_min_cm'])
    def test_unknown_distribution(self):
        c = self.candidate()
        self.assertIsNone(c['cabimento']); self.assertFalse(c['distribution_verified'])
        self.assertFalse(c['ready_for_detailing'])
        self.assertTrue(c['distribuicao_vertical_definida'])
        self.assertIn('posicao_inicial_e_limite_vertical_dos_grampos_pendentes', c['diagnostics'])
    def test_no_automatic_combined_anchorage(self):
        self.assertIsNone(self.candidate()['combined_anchorage_passes'])
    def test_poor_bond_recalculates_lb(self):
        scenario = {**fixture.BOND[0], 'boa_aderencia': False}
        self.assertGreater(self.candidate(bond_scenario=scenario)['lb_grampo_cm'], self.candidate()['lb_grampo_cm'])
    def test_bond_physical_position(self):
        scenario = {'bar_center_from_bottom_cm': 8, 'horizontal': True, 'sliding_formwork': False,
                    'provenance': {'source': 'synthetic physical center'}}
        c = self.candidate(bond_scenario=scenario)
        self.assertTrue(c['bond_condition']['boa_aderencia'])
        self.assertEqual(c['bond_condition']['scenario_status'], 'physical_position')
    def test_conflicting_bond_blocked(self):
        scenario = {**fixture.BOND[0], 'bar_center_from_bottom_cm': 60,
                    'horizontal': True, 'sliding_formwork': False}
        self.assertEqual(self.candidate(bond_scenario=scenario)['status'], 'NAO_AVALIAVEL')
    def test_hypothesis_not_complete(self):
        self.assertFalse(self.candidate(bond_scenario={**fixture.BOND[0], 'status': 'hypothesis'})['complete_calculation'])
    def test_distribution_horizontal_fit_only(self):
        distribution = {'layers': [{'diameters_mm': [10, 10], 'staple_leg_count': 2}],
                        'provenance': {'source': 'explicit synthetic occupancy'}}
        c = self.candidate(distribution=distribution)
        self.assertTrue(c['cabimento']); self.assertFalse(c['distribution_verified'])
    def test_distribution_does_not_fit(self):
        # Principal occupancy is included; four phi20 already exceed internal width.
        distribution = {'layers': [{'diameters_mm': [20,20,20,20,10,10], 'staple_leg_count': 2}],
                        'provenance': {'source': 'synthetic full layer'}}
        c = self.candidate(distribution=distribution)
        self.assertFalse(c['cabimento']); self.assertIn('grampo_nao_cabe_transversalmente', c['diagnostics'])
    def test_distribution_leg_count_mismatch(self):
        c = self.candidate(distribution={'layers': [{'diameters_mm': [10], 'staple_leg_count': 1}],
            'provenance': {'source': 'synthetic'}})
        self.assertEqual(c['status'], 'NAO_AVALIAVEL')
    def test_diameter_search_configurable(self):
        r = staple_workflow(self.ctx, self.bars, self.diagram, api, redistribution_search=fixture.SEARCH,
            diameters_mm=[12.5], bond_scenarios=fixture.BOND, contributing_legs=2,
            leg_provenance=fixture.LEGS, study_with_valid_extension=True)
        self.assertEqual([c['diameter_mm'] for c in r['staples']], [12.5])
    def test_priority_without_requested_staple_study(self):
        r = staple_workflow(self.ctx, self.bars, self.diagram, api, redistribution_search=fixture.SEARCH,
            diameters_mm=[10], bond_scenarios=fixture.BOND, contributing_legs=2, leg_provenance=fixture.LEGS)
        self.assertEqual(r['staples'], []); self.assertEqual(r['next_step'], 'PROLONGAR_ARMADURA_EXISTENTE')
    def test_v536_real_area_from_api(self):
        r = self.real
        self.assertEqual(r['As_grampo_required_cm2'], r['correction']['existing']['support_check']['anchorage']['as_adicional_cm2'])
        self.assertFalse(r['correction']['existing']['support_check']['passes'])
        self.assertTrue(all(c['area_sufficient'] for c in r['staples']))
    def test_v536_golden(self):
        import json
        g = json.loads((fixture.OUT/'V536_support_staples.json').read_text(encoding='utf8'))
        for a, b in zip(self.real['staples'], g['staples']):
            self.assertEqual(a['quantity'], b['quantity'])
            for key in ('As_supplied_cm2', 'lb_grampo_cm', 'L_grampo_min_cm'):
                self.assertAlmostEqual(a[key], b[key])
        self.assertEqual(len(self.real['staples']), len(g['staples']))
    def test_v565_no_staples(self):
        self.assertTrue(self.control['correction']['existing']['support_check']['passes'])
        self.assertEqual(self.control['next_step'], 'NENHUMA_CORRECAO')
        self.assertEqual(self.control['staples'], []); self.assertEqual(self.control['comparison'], [])
    def test_comparison_includes_one_bar_n3(self):
        c = next(c for c in self.real['comparison'] if c['id']=='extend_N3_1')
        self.assertTrue(c['anchorage_passes']); self.assertTrue(c['positive_flexure_passes'])
        self.assertTrue(c['cabimento']); self.assertEqual(c['extended_bars'], 1)
        self.assertAlmostEqual(c['added_horizontal_length_cm'], 63)
        self.assertTrue(any(c['origin']=='GRAMPO' for c in self.real['comparison']))
    def test_original_bars_immutable(self):
        self.assertEqual(self.real['original_composition'], self.bars)
    def test_nothing_selected(self):
        self.assertIsNone(self.real['selected_solution']); self.assertIsNone(self.control['selected_solution'])
    def test_api_refusal_preserved(self):
        with patch.object(api, 'calcular_ancoragem', side_effect=ValueError('unsupported hypothesis')):
            c = self.candidate()
        self.assertEqual(c['status'], 'NAO_AVALIAVEL')
        self.assertTrue(any('unsupported hypothesis' in d for d in c['diagnostics']))
    def test_invalid_length_and_area(self):
        for lb, available in [(0,20),(20,-1),(float('nan'),20)]:
            with self.assertRaises(ValueError): staple_length(lb, available)
        with self.assertRaises(ValueError): quantity_for_area(-1,1,contributing_legs=2)

    def test_usual_diameter_6_3(self):
        self.assertEqual(self.candidate(6.3)['quantity'], 2)
    def test_usual_diameter_8(self):
        self.assertEqual(self.candidate(8)['quantity'], 2)
    def test_usual_diameter_10(self):
        self.assertEqual(self.candidate(10)['quantity'], 1)
    def test_piece_area_is_two_real_bar_areas(self):
        for phi in DEFAULT_STAPLE_DIAMETERS_MM:
            c = self.candidate(phi)
            self.assertEqual(c['As_unit_piece_cm2'], 2*api.Barra(phi).area_cm2)
    def test_usual_quantity_three(self):
        self.assertTrue(usual_quantity(3)['quantidade_usual'])
        self.assertFalse(usual_quantity(3)['requer_avaliacao_especial'])
    def test_quantity_more_than_three_special(self):
        self.assertFalse(usual_quantity(4)['quantidade_usual'])
        self.assertTrue(usual_quantity(4)['requer_avaliacao_especial'])
    def test_more_than_three_not_structurally_rejected(self):
        c = evaluate_staple(self.ctx, 20, 21.5, 6.3, api,
            bond_scenario=fixture.BOND[0], contributing_legs=2, leg_provenance=fixture.LEGS)
        self.assertGreater(c['quantity'], 3)
        self.assertTrue(c['requer_avaliacao_especial'])
        self.assertTrue(c['area_sufficient']); self.assertTrue(c['complete_calculation'])
        self.assertEqual(c['status'], 'CALCULO_COMPLETO_NO_PENDENTE')
    def test_transverse_dimension(self):
        self.assertEqual(staple_geometry(60, 25, 3)['L_transversal_cm'], 18)
    def test_v536_transverse_computed(self):
        for c in self.real['staples']:
            self.assertEqual(c['L_transversal_cm'], 13)
            self.assertEqual(c['L_transversal_cm'], c['b_cm']-2*c['cover_cm']-1)
    def test_specific_default_series(self):
        self.assertEqual(DEFAULT_STAPLE_DIAMETERS_MM, (6.3,8,10))
        r = staple_workflow(self.ctx, self.bars, self.diagram, api, redistribution_search=fixture.SEARCH,
            bond_scenarios=fixture.BOND, contributing_legs=2, leg_provenance=fixture.LEGS,
            study_with_valid_extension=True)
        self.assertEqual([c['diameter_mm'] for c in r['staples']], [6.3,8,10])
    def test_longitudinal_length_preserved_custom_10(self):
        import json
        old = json.loads((fixture.OUT/'V536_support_staples_exploratory_historical.json').read_text(encoding='utf8'))
        reference = next(c for c in old['staples'] if c['diameter_mm']==10)
        self.assertEqual(self.candidate(10)['L_long_cm'], reference['L_grampo_min_cm'])
    def test_nominal_not_fabrication(self):
        c = self.candidate(6.3)
        self.assertEqual(c['L_geometrico_nominal_cm'], 2*c['L_long_cm']+c['L_transversal_cm'])
        self.assertIsNone(c['geometry']['fabrication_cut_length_cm'])
    def test_vertical_distribution_stays_unverified(self):
        self.assertFalse(self.candidate(6.3)['distribuicao_vertical_verificada'])
        self.assertFalse(self.candidate(6.3)['ready_for_detailing'])
    def test_u_piece_representation(self):
        g = self.candidate(8)['geometry']
        self.assertEqual(g['shape'], 'U'); self.assertEqual(g['longitudinal_leg_count'], 2)
        self.assertFalse(g['coordinates_verified'])
    def test_geometry_unresolved_preserves_area_and_lb(self):
        ctx = deepcopy(self.ctx); ctx['section']['bw'] = 4
        c = evaluate_staple(ctx, 1, 21.5, 8, api, bond_scenario=fixture.BOND[0],
            contributing_legs=2, leg_provenance=fixture.LEGS)
        self.assertIsNone(c['geometry']); self.assertIsNotNone(c['lb_grampo_cm'])
        self.assertTrue(c['area_sufficient']); self.assertFalse(c['complete_calculation'])
    def test_invalid_transverse_geometry_blocked(self):
        for b, cover in [(4,2.5),(19,-1),(float('nan'),2.5)]:
            with self.assertRaises(ValueError): staple_geometry(60,b,cover)
    def test_two_ramos_required_for_u(self):
        self.assertEqual(self.candidate(contributing_legs=1)['status'], 'NAO_AVALIAVEL')
    def test_quantity_preference_source(self):
        c = self.candidate(8)
        self.assertEqual(c['usual_quantity_max'], 3)
        self.assertIn('engineer_confirmed', c['quantity_preference_rule'])

    def test_vertical_two_6_3(self):
        r = vertical_distribution(2, 6.3)
        self.assertEqual(r['espacamento_vertical_livre_cm'], 2)
        self.assertAlmostEqual(r['espacamento_vertical_eixos_cm'], 2.63)
        self.assertAlmostEqual(r['altura_ocupada_cm'], 3.26)
    def test_vertical_two_8(self):
        self.assertAlmostEqual(vertical_distribution(2,8)['espacamento_vertical_eixos_cm'], 2.8)
    def test_vertical_two_10(self):
        self.assertEqual(vertical_distribution(2,10)['espacamento_vertical_eixos_cm'], 3)
    def test_vertical_three_occupied_height(self):
        self.assertAlmostEqual(vertical_distribution(3,8)['altura_ocupada_cm'], 6.4)
    def test_vertical_one_no_gap(self):
        self.assertEqual(vertical_distribution(1,10)['altura_ocupada_cm'], 1)
    def test_clear_spacing_is_not_axis_spacing(self):
        r = vertical_distribution(2,8)
        self.assertNotEqual(r['espacamento_vertical_livre_cm'], r['espacamento_vertical_eixos_cm'])
    def test_vertical_bottom_to_top(self):
        r = vertical_distribution(3,8, window={'bottom_cm':4,'top_cm':20,'provenance':{'source':'synthetic'}})
        self.assertEqual(r['ordem_distribuicao'], 'de_baixo_para_cima')
        self.assertEqual(r['orientacao_distribuicao'], 'vertical')
        self.assertLess(r['first_center_from_bottom_cm'],r['last_center_from_bottom_cm'])
    def test_vertical_window_fits(self):
        r = vertical_distribution(2,8,section=self.ctx['section'],window={'bottom_cm':4,'top_cm':8,'provenance':{'source':'synthetic'}})
        self.assertTrue(r['cabimento_vertical']);self.assertTrue(r['distribuicao_vertical_verificada'])
        self.assertFalse(r['interferencias_do_no_verificadas']);self.assertFalse(r['ready_for_detailing'])
    def test_vertical_window_does_not_fit(self):
        r = vertical_distribution(3,8,window={'bottom_cm':4,'top_cm':8,'provenance':{'source':'synthetic'}})
        self.assertFalse(r['cabimento_vertical'])
    def test_vertical_envelope_is_only_necessary_bound(self):
        r = vertical_distribution(2,8,section=self.ctx['section'])
        self.assertTrue(r['cabimento_vertical_envelope']);self.assertIsNone(r['cabimento_vertical'])
        self.assertTrue(r['distribuicao_vertical_definida']);self.assertFalse(r['distribuicao_vertical_verificada'])
    def test_vertical_envelope_failure(self):
        r = vertical_distribution(3,10,section={'h':10,'cobrimento':2})
        self.assertFalse(r['cabimento_vertical_envelope']);self.assertFalse(r['cabimento_vertical'])
    def test_vertical_exact_fit(self):
        r = vertical_distribution(2,10,window={'bottom_cm':4,'top_cm':8,'provenance':{'source':'synthetic'}})
        self.assertTrue(r['cabimento_vertical'])
    def test_vertical_window_without_provenance_not_verified(self):
        r = vertical_distribution(2,10,window={'bottom_cm':4,'top_cm':8})
        self.assertIsNone(r['cabimento_vertical']);self.assertFalse(r['distribuicao_vertical_verificada'])
    def test_vertical_window_outside_cover_blocked(self):
        r = vertical_distribution(2,10,section=self.ctx['section'],window={'bottom_cm':0,'top_cm':8,'provenance':{'source':'synthetic'}})
        self.assertIsNone(r['cabimento_vertical'])
    def test_vertical_more_than_three_remains_special(self):
        c = evaluate_staple(self.ctx, 20,21.5,10,api,bond_scenario=fixture.BOND[0],contributing_legs=2,leg_provenance=fixture.LEGS)
        self.assertTrue(c['requer_avaliacao_especial']);self.assertTrue(c['area_sufficient'])
        self.assertTrue(c['distribuicao_vertical_definida'])
    def test_no_missing_spacing_diagnostic(self):
        c = self.candidate(6.3)
        self.assertNotIn('distribuicao_geometrica_nao_verificada',c['diagnostics'])
        self.assertNotIn('distribuicao_geometrica_nao_verificada',c['limitations'])
    def test_vertical_fit_integration_does_not_approve_node(self):
        c = self.candidate(8,vertical_window={'bottom_cm':4,'top_cm':20,'provenance':{'source':'synthetic'}})
        self.assertTrue(c['distribuicao_vertical_verificada']);self.assertTrue(c['cabimento_vertical'])
        self.assertFalse(c['ready_for_detailing']);self.assertFalse(c['interferencias_do_no_verificadas'])
