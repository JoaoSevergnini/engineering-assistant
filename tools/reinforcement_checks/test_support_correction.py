"""Detail-oriented orchestration contracts; structural formulas stay in Concretopy."""
from copy import deepcopy
from importlib.util import spec_from_file_location,module_from_spec
from pathlib import Path
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import patch

from support_correction import (transverse_fit,extension_candidates,configuration_from_bars,
    check_longitudinal,preserved_original_reinforcement,diameter_steps,redistribution_candidates,
    evaluate_detail_candidate,correction_workflow)
ROOT=Path(__file__).resolve().parents[2]
spec=spec_from_file_location('correction_fixture',ROOT/'analises/pranchas/validar_v536_v565_correcao_apoio.py')
fixture=module_from_spec(spec);spec.loader.exec_module(fixture);api=fixture.api

class SupportCorrectionTests(TestCase):
    def setUp(self):self.ctx,self.bars,self.diagram=fixture.load_detail_case('V536')
    def extensions(self):return extension_candidates(self.bars,0,self.ctx['extension_target_x_m'])
    def workflow(self,context=None,diagram=None):return correction_workflow(context or self.ctx,self.bars,self.diagram if diagram is None else diagram,api,redistribution_search=fixture.SEARCH)
    def candidate(self,c):return evaluate_detail_candidate(self.ctx,self.bars,c,self.diagram,api)
    def test_minimum_spacing_diameters(self):
        for phi,expected in [(10,2),(12.5,2),(16,2),(20,2),(25,2.5)]:
            with self.subTest(phi):
                r=transverse_fit(self.ctx['section'],[{'count':2,'diameter_mm':phi}],api)
                self.assertEqual(r['layers'][0]['minimum_clear_gaps_cm'],[expected])
    def test_available_width(self):
        r=transverse_fit(self.ctx['section'],[{'count':3,'diameter_mm':20}],api)
        self.assertEqual(r['layers'][0]['available_width_cm'],13)
        self.assertEqual(r['layers'][0]['required_width_cm'],10)
    def test_one_layer_fits(self):self.assertTrue(transverse_fit(self.ctx['section'],[{'count':3,'diameter_mm':20}],api)['cabimento_transversal'])
    def test_one_layer_does_not_fit(self):self.assertFalse(transverse_fit(self.ctx['section'],[{'count':4,'diameter_mm':20}],api)['cabimento_transversal'])
    def test_two_layers(self):
        r=transverse_fit(self.ctx['section'],[{'count':3,'diameter_mm':20},{'count':3,'diameter_mm':20}],api)
        self.assertTrue(r['cabimento_transversal']);self.assertEqual(len(r['layers']),2)
    def test_mixed_layer_explicit_geometry(self):
        r=transverse_fit(self.ctx['section'],[{'diameters_mm':[12.5,20,25]}],api)
        self.assertEqual(r['layers'][0]['diameters_mm'],[12.5,20,25])
        self.assertEqual(r['layers'][0]['minimum_clear_gaps_cm'],[2,2.5])
    def test_unknown_geometry_null(self):self.assertIsNone(transverse_fit({},[{'count':3,'diameter_mm':20}],api)['cabimento_transversal'])
    def test_valid_existing_stops(self):
        ctx,bars,diagram=fixture.load_detail_case('V565')
        with patch('support_correction.extension_candidates',side_effect=AssertionError('must not search')):
            r=correction_workflow(ctx,bars,diagram,api,redistribution_search=fixture.SEARCH)
        self.assertEqual(r['next_step'],'NENHUMA_CORRECAO');self.assertEqual(r['extensions'],[]);self.assertEqual(r['redistributions'],[])
    def test_invalid_existing_searches(self):
        r=self.workflow();self.assertFalse(r['existing']['support_check']['passes']);self.assertEqual(len(r['extensions']),3)
    def test_prolong_one(self):self.assertEqual(self.extensions()[0]['changes'][0]['extended_quantity'],1)
    def test_prolong_two(self):self.assertEqual(self.extensions()[1]['changes'][0]['extended_quantity'],2)
    def test_prolong_all(self):self.assertEqual(self.extensions()[2]['changes'][0]['unextended_quantity'],0)
    def test_partial_extension_retains_unextended_interval(self):
        c=self.extensions()[0];remaining=[b for b in c['bars'] if '__remaining_' in b['mark']][0]
        self.assertEqual(remaining['bars'],2);self.assertEqual(remaining['x_start_common'],.54)
    def test_layers_and_d_not_collapsed(self):
        cfg=configuration_from_bars(self.extensions()[0]['bars'],0,'test')
        self.assertEqual([l['count'] for l in cfg['layers']],[3,1]);self.assertEqual([l['d_cm'] for l in cfg['layers']],[68,64])
    def test_full_recalculation_extension(self):
        c=self.candidate(self.extensions()[0]);old=self.workflow()['existing']['support_check']['metrics'];new=c['support_check']['metrics']
        for key in ('d_cm','x_cm','z_cm'):self.assertNotEqual(old[key],new[key])
        self.assertEqual(len(c['support_check']['states']),2)
        self.assertNotEqual(c['support_check']['states'][0]['result']['condicao_b']['decalagem']['d_cm'],68)
    def test_original_reinforcement_preserved(self):
        for c in self.extensions():self.assertTrue(preserved_original_reinforcement(self.bars,c['bars']))
    def test_original_positive_capacity_not_reduced(self):
        c=self.candidate(self.extensions()[0]);self.assertTrue(c['original_span_capacity_not_reduced'])
        self.assertTrue(all(p['capacity_not_reduced'] for p in c['capacity_preservation_comparisons']))
    def test_regions_not_just_peak(self):
        c=self.candidate(self.extensions()[0]);regions=c['longitudinal_check']['regions']
        self.assertGreater(len(regions),1);self.assertTrue(all(r['capacity_sufficient'] for r in regions))
        self.assertTrue(any(p['source_type']=='linear_interpolation' for r in regions for p in r['demand_points']))
    def test_diameter_one_step(self):self.assertEqual(diameter_steps(12.5,16,fixture.SEARCH['series']),1)
    def test_diameter_two_steps(self):self.assertEqual(diameter_steps(12.5,20,fixture.SEARCH['series']),2)
    def test_diameter_step_preference_configurable(self):
        a=redistribution_candidates(self.bars,api,self.ctx['section'],series=fixture.SEARCH['series'],max_steps=2,counts=[3])
        b=redistribution_candidates(self.bars,api,self.ctx['section'],series=fixture.SEARCH['series'],max_steps=3,counts=[3])
        self.assertTrue(all(c['diameter_steps']<=2 for c in a));self.assertTrue(any(c['diameter_steps']==3 for c in b))
    def test_redistribution_mixed_bitolas_in_distinct_layers(self):
        cs=redistribution_candidates(self.bars,api,self.ctx['section'],series=[12.5,16,20],counts=[3])
        c=next(c for c in cs if c['bars'][0]['diameter_mm']==16 and c['bars'][1]['diameter_mm']==20)
        r=self.candidate(c)
        self.assertIn('span_depth_recalculation',r);self.assertNotEqual(r['span_depth_recalculation']['d_equivalente_cm'],66)
        self.assertEqual(r['origin'],'REDISTRIBUICAO');self.assertFalse(r['recomendavel_como_correcao'])
    def test_redistribution_all_regions_rechecked(self):
        c=redistribution_candidates(self.bars,api,self.ctx['section'],series=[16,20],counts=[3])[0]
        r=self.candidate(c);self.assertGreater(len(r['longitudinal_check']['regions']),1)
        self.assertFalse(r['longitudinal_check']['compatibilidade_flexao_positiva'])
    def test_locally_valid_but_no_fit(self):
        cs=redistribution_candidates(self.bars,api,self.ctx['section'],series=[16,20],counts=[3,5])
        c=next(c for c in cs if c['bars'][0]['bars']==5 and c['bars'][1]['bars']==3)
        r=self.candidate(c);self.assertTrue(r['support_check']['passes'])
        self.assertTrue(r['longitudinal_check']['compatibilidade_flexao_positiva'])
        self.assertFalse(r['cabimento_transversal']);self.assertFalse(r['recomendavel_como_correcao'])
    def test_locally_valid_without_longitudinal_proof(self):
        r=evaluate_detail_candidate(self.ctx,self.bars,self.extensions()[0],None,api)
        self.assertTrue(r['support_check']['passes']);self.assertIsNone(r['technically_valid']);self.assertFalse(r['recomendavel_como_correcao'])
    def test_no_simple_solution_complementary_next(self):
        ctx={**self.ctx,'support_length_cm':10};r=self.workflow(context=ctx)
        self.assertEqual(r['next_step'],'AVALIAR_ARMADURA_COMPLEMENTAR')
        self.assertTrue(r['redistributions']);self.assertIsNone(r['selected_solution'])
    def test_extensions_precede_redistribution(self):
        with patch('support_correction.redistribution_candidates',side_effect=AssertionError('must not redistribute')):
            r=self.workflow()
        self.assertEqual(r['next_step'],'PROLONGAR_ARMADURA_EXISTENTE')
    def test_nothing_selected_silently(self):self.assertIsNone(self.workflow()['selected_solution'])
    def test_existing_without_proof_inconclusive(self):
        ctx,bars,diagram=fixture.load_detail_case('V565')
        r=correction_workflow(ctx,bars,None,api,redistribution_search=fixture.SEARCH)
        self.assertIsNone(r['next_step']);self.assertFalse(r['existing']['recomendavel_como_correcao'])
    def test_unknown_interval_blocks(self):
        bars=deepcopy(self.bars);bars[1]['x_start_common']=None
        r=check_longitudinal(bars,self.ctx,self.diagram,api)
        self.assertIsNone(r['compatibilidade_flexao_positiva'])
    def test_v536_golden(self):
        r=self.workflow();g=fixture.read('V536_support_correction.json')
        self.assertEqual(r['next_step'],g['next_step']);self.assertEqual(r['recommended_ids'],g['recommended_ids'])
        for a,b in zip(r['extensions'],g['extensions']):
            self.assertEqual(a['technically_valid'],b['technically_valid'])
            for key in ('d_cm','x_cm','z_cm','lb_nec_cm','As_additional_cm2'):self.assertAlmostEqual(a['support_check']['metrics'][key],b['support_check']['metrics'][key])
    def test_v565_control(self):
        ctx,bars,diagram=fixture.load_detail_case('V565');r=correction_workflow(ctx,bars,diagram,api,redistribution_search=fixture.SEARCH)
        self.assertEqual(r['next_step'],fixture.read('V565_support_correction.json')['next_step'])
        self.assertEqual(r['recommended_ids'],[])
    def test_declared_node_limits(self):
        r=self.candidate(self.extensions()[0]);self.assertTrue(r['recomendavel_como_correcao'])
        self.assertFalse(r['ready_for_detailing']);self.assertIn('gancho_geometria_nao_verificada',r['limitations'])
