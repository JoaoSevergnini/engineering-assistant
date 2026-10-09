"""V516/V517 real negative review: orchestration and resolved/pending controls."""
import json,sys
from pathlib import Path
from unittest import TestCase
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'analises/pranchas'
sys.path.insert(0,str(ROOT.parent/'concretopy'))
import concretopy as api
class V516V517NegativeTests(TestCase):
 @classmethod
 def setUpClass(cls):cls.cases={b:json.loads((OUT/f'{b}_negative_reinforcement_review.json').read_text(encoding='utf8')) for b in ('V516','V517')}
 def event(self,b,m,side):return next(e['result'] for e in self.cases[b]['events'] if e['mark']==m and e['cut_side']==side)
 def test_four_spans(self):self.assertTrue(all(len(r['spans'])==4 for r in self.cases.values()))
 def test_five_support_occurrences(self):self.assertTrue(all(len(r['ordered_supports'])==5 for r in self.cases.values()))
 def test_repeated_P2_not_merged(self):
  for r in self.cases.values():
   a,b=r['ordered_supports'][1:3];self.assertEqual(a['label'],b['label']);self.assertNotEqual(a['id'],b['id']);self.assertNotEqual(a['axis_m'],b['axis_m'])
 def test_axes_from_ordered_operands(self):self.assertEqual([s['axis_m'] for s in self.cases['V516']['ordered_supports']],[0,2.08,6.62,11,13.68])
 def test_clear_spans_match_drawing(self):
  for r in self.cases.values():
   for s,value in zip(r['spans'],[185,432,356,185]):self.assertAlmostEqual(s['clear_length_cm'],value)
 def test_P1_DEPEV_preserved(self):self.assertEqual(self.cases['V516']['ordered_supports'][3]['depev_m'],.554)
 def test_no_join_across_P1_sample_gap(self):self.assertEqual(self.cases['V516']['spans'][2]['sampled_domain_m'][1],10.446);self.assertEqual(self.cases['V516']['spans'][3]['sampled_domain_m'][0],11.554)
 def test_forces_independent(self):self.assertNotEqual(self.cases['V516']['spans'][2]['diagram']['points'],self.cases['V517']['spans'][2]['diagram']['points'])
 def test_real_resistance_recomputed_by_concretopy(self):
  rr=api.verificar_flexao_viga_retangular(api.SecaoRetangular(19,52,2.5,5),api.Concreto(40),api.Aco(500),(api.CamadaArmaduraLongitudinal(3,api.Barra(20)),api.CamadaArmaduraLongitudinal(1,api.Barra(20))),gamma_f=1.4,gamma_c=1.4,gamma_s=1.15)
  for case in self.cases.values():
   region=next(r for r in case['regions'] if r['span']==3 and r['start_m']==9.16)
   self.assertAlmostEqual(region['result']['regions'][0]['Mk_equivalent_knm'],rr.mk_equivalente_kncm/100)
 def test_P1_regional_failure_both(self):
  for case in self.cases.values():self.assertTrue(case['known_regional_flexure_failure']);self.assertTrue(any(r['result']['passes'] is False for r in case['regions']))
 def test_N3_left_both_pass(self):self.assertTrue(all(self.event(b,'N3','LEFT')['passes'] is True for b in self.cases))
 def test_N8_left_basic_lb_condition_fails(self):
  for b in self.cases:self.assertFalse(self.event(b,'N8','LEFT')['checks']['al_plus_lb']['passes']);self.assertFalse(self.event(b,'N8','LEFT')['passes'])
 def test_N8_left_ten_phi_passes(self):self.assertTrue(all(self.event(b,'N8','LEFT')['checks']['al_plus_10phi']['passes'] is True for b in self.cases))
 def test_N8_available_doc_geometry(self):
  for b in self.cases:self.assertEqual(self.event(b,'N8','LEFT')['actual_end_position_m'],5.83);self.assertAlmostEqual(self.event(b,'N8','LEFT')['checks']['al_plus_lb']['available_length_cm'],79)
 def test_N9_left_scaling_pass_not_flexure_approval(self):
  for b in self.cases:self.assertTrue(self.event(b,'N9','LEFT')['passes']);self.assertTrue(self.cases[b]['known_regional_flexure_failure'])
 def test_coincident_right_cuts_independent(self):
  for b in self.cases:
   for mark in ('N8','N9'):
    r=self.event(b,mark,'RIGHT');self.assertNotIn('multiple_or_inconsistent_interruption_event',r['diagnostics']);self.assertEqual(r['termination_event']['selected_mark'],mark);self.assertEqual([x['mark'] for x in r['reinforcement_after_cut']],['N7']);self.assertIn('basic_lb_beyond_support',r['checks'])
 def test_poor_bond_own_bar(self):
  for b in self.cases:
   a=self.event(b,'N3','LEFT')['anchorage'];c=self.event(b,'N8','LEFT')['anchorage'];self.assertEqual(a['bond_condition'],'POOR');self.assertLess(a['result']['lb_cm'],c['result']['lb_cm'])
 def test_bend_geometry_not_anchorage_approval(self):
  for case in self.cases.values():
   for n in case['end_nodes']:self.assertFalse(n['result']['bend_geometry_passes']);self.assertIsNone(n['result']['passes']);self.assertIsNone(n['result']['anchorage_resistance_verified'])
 def test_continuity_physical_not_resistant_approval(self):
  for case in self.cases.values():
   self.assertEqual(len(case['intermediate_continuity']),7)
   for c in case['intermediate_continuity']:self.assertEqual(c['result']['continuity'],'CONTINUES_THROUGH_SUPPORT');self.assertIsNone(c['result']['passes'])
 def test_overlap_engineer_accepted_no_sum_credit(self):
  for case in self.cases.values():
   overlaps=[r for r in case['regions'] if r['result'].get('tail_overlap_engineer_accepted')];self.assertEqual(len(overlaps),2)
   for r in overlaps:self.assertFalse(r['result']['capacity_sum_credited']);self.assertTrue(all(c['result']['passes'] for c in r['result']['independent_reference_checks']))
 def test_no_global_approval_or_solution_selection(self):
  for case in self.cases.values():self.assertIsNone(case['global_negative_approval']);self.assertIsNone(case['selected_solution']);self.assertFalse(case['full_negative_verification_complete'])

 def test_right_P1_physical_face_not_S1(self):
  for beam in self.cases:
   for mark in ('N8','N9'):
    r=self.event(beam,mark,'RIGHT');self.assertEqual(r['anchorage_reference_face']['x_m'],11.71);self.assertEqual(r['support_terminal_demand']['x_m'],11.554);self.assertEqual(r['support_terminal_demand']['section'],1)
 def test_right_P1_classified_and_passes(self):
  for beam in self.cases:
   for mark in ('N8','N9'):
    r=self.event(beam,mark,'RIGHT');self.assertEqual(r['classification'],'ANCHORAGE_BEYOND_INTERMEDIATE_SUPPORT');self.assertTrue(r['required_in_previous_span']);self.assertFalse(r['required_in_adjacent_span']);self.assertTrue(r['passes']);self.assertEqual(list(r['checks']),['basic_lb_beyond_support'])
 def test_right_P1_length_basic_API(self):
  for beam in self.cases:
   for mark in ('N8','N9'):
    r=self.event(beam,mark,'RIGHT');c=r['checks']['basic_lb_beyond_support'];self.assertEqual(c['available_length_cm'],113);self.assertEqual(c['required_length_cm'],r['anchorage']['result']['lb_cm']);self.assertAlmostEqual(c['margin_cm'],113-c['required_length_cm']);self.assertNotIn('al',r)
 def test_right_P1_whole_branch_demonstrated(self):
  for beam in self.cases:
   for mark in ('N8','N9'):
    r=self.event(beam,mark,'RIGHT');self.assertTrue(r['adjacent_need_evidence']['sufficient_everywhere']);self.assertFalse(r['previous_need_evidence']['sufficient_everywhere']);self.assertGreater(r['capacity_remaining']['Mk_equivalent_knm'],r['adjacent_need_evidence']['maximum_negative_demand_knm'])

 def test_extreme_P5_N4_vertical_bend(self):
  for case in self.cases.values():
   r=next(n['verification'] for n in case['end_nodes'] if n['mark']=='N4');c=r['checks']['vertical_bend_geometry'];self.assertEqual(c['vertical_bend_provided_cm'],40);self.assertAlmostEqual(c['vertical_bend_required_cm'],48.7);self.assertAlmostEqual(c['margin_cm'],-8.7);self.assertEqual(c['status'],'FAIL');self.assertEqual(r['terminal_demand']['section'],1)
 def test_extreme_P6_N7_vertical_bend(self):
  for case in self.cases.values():
   r=next(n['verification'] for n in case['end_nodes'] if n['mark']=='N7');c=r['checks']['vertical_bend_geometry'];self.assertEqual(c['vertical_bend_provided_cm'],45);self.assertAlmostEqual(c['vertical_bend_required_cm'],48.7);self.assertAlmostEqual(c['margin_cm'],-3.7);self.assertEqual(c['status'],'FAIL');self.assertEqual(r['terminal_demand']['section'],13)
 def test_extreme_flexure_bend_independent(self):
  for case in self.cases.values():
   for node in case['end_nodes']:
    r=node['verification'];self.assertEqual(r['checks']['flexural_capacity']['status'],'PASS');self.assertEqual(r['checks']['vertical_bend_geometry']['status'],'FAIL');self.assertTrue(r['checks']['flexural_capacity']['selected_mark_required_at_terminal'])
 def test_extreme_missing_transverse_geometry(self):
  for case in self.cases.values():
   for node in case['end_nodes']:
    r=node['verification'];self.assertEqual(r['checks']['vibrator_access_spacing']['status'],'INCONCLUSIVE');self.assertEqual(r['checks']['column_interference_spacing']['status'],'INCONCLUSIVE');self.assertEqual(r['checks']['curved_anchorage_resistance']['status'],'INCONCLUSIVE');self.assertIsNone(r['selected_solution']);self.assertIsNone(r['detailing_optimization'])
