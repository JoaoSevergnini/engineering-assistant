"""Integrated V536 golden contracts; resistant equations stay in Concretopy."""
from importlib.util import spec_from_file_location,module_from_spec
from pathlib import Path
import hashlib,json
from unittest import TestCase
ROOT=Path(__file__).resolve().parents[2]
spec=spec_from_file_location('v536_positive_integrated',ROOT/'analises/pranchas/validar_v536_positivo_completo.py')
fixture=module_from_spec(spec);spec.loader.exec_module(fixture)

class V536PositiveIntegratedTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result=fixture.build_golden();cls.stages=cls.result['stages']
        cls.golden=fixture.read('V536_positive_reinforcement_complete_golden.json')
    def test_persisted_golden_summary(self):
        self.assertEqual(self.result['summary'],self.golden['summary'])
        self.assertEqual(self.result['coverage'],self.golden['coverage'])
    def test_regional_capacity_matches_prior_scaling(self):
        old=fixture.read('V536_N3_scaling_check.json')
        regions=self.stages['positive_flexure_sampled_model']['result']['regions']
        self.assertAlmostEqual(regions[0]['concretopy']['mk_equivalente_kncm']/100,old['remaining_capacity']['Mk_equivalent_knm'])
        self.assertAlmostEqual(regions[-1]['concretopy']['mk_equivalente_kncm'],old['before_flexure']['concretopy_result']['mk_equivalente_kncm'])
        self.assertTrue(all(r['capacity_sufficient'] for r in regions))
    def test_scaling_before_after_and_reference_regression(self):
        current=self.stages['positive_scaling']['result'];old=fixture.read('V536_N3_scaling_check.json')
        self.assertEqual(current['composition_before']['marks'],old['composition_before']['marks'])
        self.assertEqual(current['composition_after']['marks'],old['composition_after']['marks'])
        self.assertEqual(current['event_x_m'],old['event_x_m'])
        self.assertAlmostEqual(current['moment_diagram']['selected_x_nec_m'],old['moment_diagram']['selected_x_nec_m'])
    def test_both_scaling_conditions_preserved(self):
        r=self.stages['positive_scaling']['result'];g=fixture.read('V536_N3_scaling_check.json')
        for condition in ('condition_A','condition_B'):
            self.assertEqual(r[condition]['passes'],g[condition]['passes'])
            self.assertAlmostEqual(r[condition]['available_length_cm'],g[condition]['available_length_cm'])
            self.assertAlmostEqual(r[condition]['required_length_cm'],g[condition]['required_length_cm'])
    def test_left_support_matches_corrected_golden(self):
        current=self.stages['left_support_and_anchorage']['result']
        previous=fixture.read('V536_left_support_anchorage_check.json')['exploration']['existing']
        for key in ('As_support_cm2','As_effective_cm2','lb_ef_cm','lb_nec_cm','As_additional_cm2'):
            self.assertAlmostEqual(current['metrics'][key],previous['metrics'][key])
        self.assertFalse(current['passes']);self.assertEqual(len(current['states']),2)
    def test_generic_search_matches_original_exploration(self):
        r=self.stages['generic_anchorage_exploration']['result']
        g=fixture.read('V536_left_support_anchorage_check.json')['exploration']
        self.assertEqual(r['valid_alternative_ids'],g['valid_alternative_ids'])
        self.assertEqual(len(r['alternatives']),len(g['alternatives']))
        self.assertTrue(any(c['passes'] and c['integration_transverse_fit']['cabimento_transversal'] is False for c in r['alternatives']))
        self.assertTrue(all(c['ready_for_detailing'] is False for c in r['alternatives']))
    def test_extension_retains_real_full_recalculation(self):
        r=self.stages['correction_alternatives']['result'];g=fixture.read('V536_support_correction.json')
        self.assertEqual(r['recommended_ids'],g['recommended_ids'])
        for a,b in zip(r['extensions'],g['extensions']):
            self.assertTrue(a['original_span_capacity_not_reduced'])
            for key in ('d_cm','x_cm','z_cm','lb_nec_cm','As_additional_cm2'):
                self.assertAlmostEqual(a['support_check']['metrics'][key],b['support_check']['metrics'][key])
    def test_staples_match_current_individual_golden(self):
        r=self.stages['complementary_staples']['result'];g=fixture.read('V536_support_staples.json')
        self.assertEqual(len(r['staples']),len(g['staples']))
        for a,b in zip(r['staples'],g['staples']):
            self.assertEqual(a['quantity'],b['quantity'])
            for key in ('As_supplied_cm2','lb_grampo_cm','L_long_cm','L_transversal_cm','altura_ocupada_cm'):
                self.assertAlmostEqual(a[key],b[key])
            self.assertTrue(a['distribuicao_vertical_definida']);self.assertFalse(a['ready_for_detailing'])
    def test_missing_right_support_and_unsampled_end_not_approved(self):
        self.assertTrue(self.stages['right_support_and_anchorage']['result']['longitudinal_anchorage_passes'])
        self.assertIsNone(self.stages['right_support_and_anchorage']['result']['support_verified'])
        self.assertFalse(self.result['coverage']['whole_physical_domain_sampled'])
        self.assertFalse(self.result['coverage']['extrapolation'])
        self.assertFalse(self.result['summary']['complete_positive_approval'])
        self.assertIsNone(self.result['summary']['positive_reinforcement_approved'])
    def test_hypothesis_does_not_override_documentary_geometry(self):
        strict=self.stages['positive_flexure_documentary']['result']
        self.assertTrue(strict['span_summary']['incomplete'])
        self.assertTrue(any('unresolved_transverse_geometry' in r['blockers'] for r in strict['regions']))
        self.assertTrue(self.result['summary']['sampled_positive_flexure_passes'])
    def test_no_correction_silently_selected(self):
        self.assertIsNone(self.result['summary']['selected_solution'])
        for name in ('correction_alternatives','generic_anchorage_exploration','complementary_staples'):
            self.assertIsNone(self.stages[name]['result']['selected_solution'])
        comparisons=self.stages['complementary_staples']['result']['comparison']
        self.assertTrue(any(c['id']=='extend_N3_1' and c['anchorage_passes'] for c in comparisons))
    def test_recomputation_keeps_sources_read_only(self):
        before={n:hashlib.sha256((fixture.OUT/n).read_bytes()).hexdigest() for n in fixture.INPUTS}
        fixture.build_golden()
        self.assertEqual(before,{n:hashlib.sha256((fixture.OUT/n).read_bytes()).hexdigest() for n in fixture.INPUTS})
