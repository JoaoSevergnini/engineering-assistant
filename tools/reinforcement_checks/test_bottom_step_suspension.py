"""Synthetic lower-bottom changes; real Concretopy, no alternative resistance."""
import copy
import unittest
import test_floor_review as fixtures
from test_floor_review import proved,form,api

class BottomStepTests(unittest.TestCase):
 def setUp(self):
  self.fixture=fixtures.FloorTests();self.fixture.setUp();self.addCleanup(self.fixture.doCleanups);self.case=self.fixture.case
 def section_case(self,**kwargs):return self.fixture.section_case(**kwargs)
 def run_case(self,**kwargs):return self.fixture.run_case(**kwargs)
 def setup_step(self,left_bottom=0,right_bottom=10,heights=(57,47),spacing=8):
  self.section_case(heights=heights)
  for s,b in zip(self.case['model']['physical_geometry']['segments'],(left_bottom,right_bottom)):
   s['geometry']['bottom_level_cm']=proved(b,'cm');s['geometry']['top_level_cm']=proved(b+s['geometry']['height_cm']['value'],'cm')
  self.case['form']=form(self.case['model'])
  self.case['section_checks'].update(gamma_n=proved(1.1))
  self.case['section_checks']['drawn_stirrup_regions'][0]['spacing_cm']=spacing
  self.case['section_checks']['drawn_stirrup_regions'][0]['position_state']='DOCUMENTED_CONFIRMED'
  return self.case
 def step(self):return self.run_case(api=api)['section_checks']['bottom_step_suspension'][0]
 def test_coincident_bottoms_do_not_require_extra_suspension(self):
  self.setup_step(0,0);r=self.step();self.assertEqual(r['status'],'NOT_APPLICABLE');self.assertIsNone(r['classification']['suspended_side'])
  self.assertEqual(r['input_validation']['readiness'],'NOT_APPLICABLE');self.assertEqual(r['execution_state'],'EXECUTED_COMPLETE');self.assertIsNone(r['result'])
 def test_lower_bottom_left_all_adensamento_is_left(self):
  self.setup_step();r=self.step()['result'];self.assertEqual(r['suspended_side'],'LEFT');self.assertEqual(r['distribution_interval_m'],[1.715,2]);self.assertAlmostEqual(r['additional_area']['as_suspension_cm2'],30*1.4*1.1/(500/1.15*.1))
 def test_lower_bottom_right_despite_smaller_height(self):
  self.setup_step(10,0);r=self.step()['result'];self.assertEqual(r['suspended_side'],'RIGHT');self.assertEqual(r['distribution_interval_m'],[2,2.235]);self.assertEqual(r['distribution_length_cm'],23.5)
 def test_different_one_sided_shears_govern_from_suspended_side(self):
  self.setup_step();self.case['section_checks']['domains'][0]['discontinuities_m']=[proved(2,'m')]
  self.case['section_checks']['effective_depths']={'G1':proved(53.07,'cm'),'G2':proved(43.07,'cm')}
  self.case['section_checks']['height_change_transitions']=[dict(left_segment_id='G1',right_segment_id='G2',shear_sides={'LEFT':{'max':proved(30,'kN'),'min':proved(-20,'kN')},'RIGHT':{'max':proved(200,'kN'),'min':proved(-100,'kN')}})]
  # Global physical Vk selection is incomplete at the known jump; the extra control
  # must use the explicit one-sided records, not that physical maximum.
  r=self.step();self.assertEqual(r['execution_state'],'EXECUTED_COMPLETE');self.assertEqual(r['result']['governing_shear']['Vk_original_kn'],30)
  self.assertEqual(r['result']['transition_shear_sides']['RIGHT'][0]['Vk_original_kn'],200)
 def test_sufficient_adensamento(self):
  self.setup_step();r=self.step();self.assertEqual(r['status'],'PASS');item=r['result']['subintervals'][0];self.assertAlmostEqual(item['total_required_rate_cm2_m'],item['usual_rate_cm2_m']+item['additional_rate_cm2_m'])
 def test_insufficient_adensamento(self):
  self.setup_step(spacing=20);r=self.step();self.assertEqual(r['status'],'FAIL')
 def test_unproved_extension_prevents_approval(self):
  self.setup_step();self.case['section_checks']['drawn_stirrup_regions'][0]['position_state']='ENGINEERING_ASSUMPTION';r=self.step();self.assertEqual(r['status'],'INCONCLUSIVE')
 def test_partial_coverage_is_not_averaged(self):
  self.setup_step();self.case['section_checks']['drawn_stirrup_regions'][0]['interval_m']=[1.8,2];r=self.step();self.assertEqual(r['status'],'INCONCLUSIVE');self.assertIn('full_adensamento_coverage_not_proved',r['result']['pending'])
 def test_unknown_bottom_does_not_assume_side(self):
  self.setup_step();self.case['form']['segments'][0]['fields'].pop('bottom_level_cm');r=self.step();self.assertEqual(r['execution_state'],'NOT_EXECUTED');self.assertIsNone(r['classification']['suspended_side'])
 def test_gamma_n_is_not_defaulted(self):
  self.setup_step();self.case['section_checks'].pop('gamma_n');r=self.step();self.assertEqual(r['execution_state'],'NOT_EXECUTED');self.assertIn('gamma_n',r['input_validation']['pending'])
 def test_changed_height_changes_unilateral_distribution(self):
  self.setup_step(0,10,heights=(67,47));r=self.step()['result'];self.assertEqual(r['distribution_interval_m'],[1.665,2]);self.assertEqual(r['distribution_length_cm'],33.5)
 def test_no_double_count_of_overlapping_pieces(self):
  self.setup_step();self.case['section_checks']['drawn_stirrup_regions']*=2;r=self.step();self.assertEqual(r['status'],'INCONCLUSIVE')
 def test_existing_usual_spacing_alert_is_preserved(self):
  self.setup_step(spacing=6);r=self.step();self.assertEqual(r['status'],'REQUIRES_ENGINEERING_REVIEW');self.assertTrue(r['result']['engineering_review_required'])
 def test_jump_without_one_sided_values_is_not_interpolated(self):
  self.setup_step();self.case['section_checks']['domains'][0]['discontinuities_m']=[proved(2,'m')]
  r=self.step();self.assertNotEqual(r['status'],'PASS');self.assertIsNone((r.get('result') or {}).get('additional_area'))
 def test_gap_outside_unilateral_region_does_not_block_local_control(self):
  self.setup_step()
  for series in self.case['positioned_tqs']['beam']['spans'][0]['internal_forces']:
   if series['quantity']=='shear':series['values'][0]=None
  r=self.step();self.assertEqual(r['status'],'PASS');self.assertEqual(r['result']['governing_shear']['Vk_original_kn'],30)
 def test_diagonal_failure_is_preserved_when_total_rate_unavailable(self):
  self.setup_step()
  for series in self.case['positioned_tqs']['beam']['spans'][0]['internal_forces']:
   if series['quantity']=='shear':series['values']=[2000 if series['envelope']=='max' else -2000]*6
  r=self.step();self.assertEqual(r['status'],'FAIL');self.assertEqual(r['result']['subintervals'][0]['checks']['diagonal_compression']['status'],'FAIL')
 def test_overlapping_suspension_regions_cannot_share_stirrups_silently(self):
  self.section_case(bounds=(0,1.8,2.2,4),heights=(47,57,47))
  for s,b in zip(self.case['model']['physical_geometry']['segments'],(10,0,10)):
   s['geometry']['bottom_level_cm']=proved(b,'cm');s['geometry']['top_level_cm']=proved(b+s['geometry']['height_cm']['value'],'cm')
  self.case['form']=form(self.case['model']);self.case['section_checks']['gamma_n']=proved(1.1)
  r=self.case['section_checks']['drawn_stirrup_regions'][0];r.update(spacing_cm=8,position_state='DOCUMENTED_CONFIRMED')
  for series in self.case['positioned_tqs']['beam']['spans'][0]['internal_forces']:
   if series['quantity']=='shear':series['values']=[30 if series['envelope']=='max' else -20]*6
  steps=self.run_case(api=api)['section_checks']['bottom_step_suspension']
  self.assertTrue(all(s['status']=='INCONCLUSIVE' for s in steps))
  self.assertIn('overlapping_suspension_regions_combination_unproved',steps[0]['result']['pending'])
