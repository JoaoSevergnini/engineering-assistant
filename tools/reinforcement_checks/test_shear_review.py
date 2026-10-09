"""Shear contracts with public Concretopy; no copied resistant equations."""
from pathlib import Path
import sys,json
from copy import deepcopy
from unittest import TestCase
from test_longitudinal_negative import api
from shear_diagram import ShearDiagram
from shear_review import public_shear_api,design_shear,check_drawn_region,reference_options,shear_reference_design,review_shear_spans,transition_check,inverse_shear_capacity,select_shear_depth

ROOT=Path(__file__).resolve().parents[2]
API=public_shear_api()
def context():
 return {'section':{'bw':19,'h':52,'cobrimento':2.5,'diametro_estribo_mm':5},'fck_mpa':40,'fyk_mpa':500,'gamma_f':1.4,'gamma_c':1.4,'gamma_s':1.15,
  'effective_depth':{'status':'PASS','d_cm':46.7,'selected':{'provenance':{'synthetic':'explicit audited physical centroid'}},'rule':'engineer_confirmed_shear_effective_depth_max_layers_v1'}}
def series(values=(100,0,-100),xs=(0,2,4),identity='max'):
 return {'quantity':'shear','unit':'kN','envelope':identity,'sections':list(range(1,len(xs)+1)),'positions':list(xs),'values':list(values),'provenance':{'synthetic':identity}}
def diagram(values=(100,0,-100),xs=(0,2,4)):return ShearDiagram([series(values,xs)])
def region(phi=5,spacing=14,legs=2,interval=(0,4),**kwargs):
 return {'id':'R','diameter_mm':phi,'spacing_cm':spacing,'legs':legs,'interval_m':list(interval),'source':{'synthetic':'drawn stirrup'},**kwargs}
def check(phi=5,spacing=14,legs=2,vk=50,interval=(0,4),ctx=None,**kwargs):
 return check_drawn_region(diagram((vk,0,-vk)),ctx or context(),API,region(phi,spacing,legs,interval,**kwargs))

class DiagramTests(TestCase):
 def test_positive_governs(self):self.assertEqual(diagram((100,0,-50)).maximum(0,4)['governing'][0]['Vsk_original_kn'],100)
 def test_negative_governs(self):self.assertEqual(diagram((50,0,-100)).maximum(0,4)['governing'][0]['Vsk_original_kn'],-100)
 def test_original_sign_preserved(self):self.assertEqual(diagram((50,0,-100)).maximum(0,4)['governing'][0]['sign'],-1)
 def test_abs_ties_retained(self):self.assertEqual(len(diagram().maximum(0,4)['governing']),2)
 def test_endpoint(self):self.assertEqual(diagram().maximum(1,4)['governing'][0]['x_m'],4)
 def test_internal_vertex(self):self.assertEqual(diagram((10,100,10)).maximum(1,3)['Vsk_abs_kn'],100)
 def test_between_start(self):self.assertEqual(diagram().maximum(1,2)['Vsk_abs_kn'],50)
 def test_between_end(self):self.assertEqual(diagram().maximum(2,3)['Vsk_abs_kn'],50)
 def test_gap(self):self.assertEqual(diagram((100,None,-100)).maximum(1,3)['status'],'INCONCLUSIVE')
 def test_partial_domain(self):
  d=diagram().maximum(-1,2,allow_intersection=True);self.assertFalse(d['complete']);self.assertEqual(d['series_coverage'][0]['check_interval_m'],[0,2])
 def test_no_domain(self):self.assertIsNone(diagram().maximum(5,6)['Vsk_abs_kn'])
 def test_multiple_identity(self):
  d=ShearDiagram([series((10,20,10)),series((-50,-60,-50),identity='min')]);r=d.maximum(0,4)
  self.assertEqual(r['governing'][0]['series_id'],'min');self.assertEqual(r['Vsk_abs_kn'],60)
 def test_no_cross_interpolation(self):
  r=ShearDiagram([series((100,0,-100)),series((-10,-10,-10),identity='min')]).maximum(1,1.5)
  self.assertEqual(r['Vsk_abs_kn'],50);self.assertEqual(len(r['series_coverage']),2)
 def test_one_series_gap_cannot_hidden(self):
  r=ShearDiagram([series((100,0,-100)),series((10,None,10),identity='min')]).maximum(0,4);self.assertFalse(r['complete'])
 def test_preserves_input(self):
  s=series();old=deepcopy(s);d=ShearDiagram([s]);d.maximum(0,4);self.assertEqual(s,old)
 def test_invalid_identity(self):
  with self.assertRaises(ValueError):ShearDiagram([series(),series()])
 def test_invalid_unit(self):
  s=series();s['unit']='tf'
  with self.assertRaises(ValueError):ShearDiagram([s])
 def test_invalid_interval(self):
  with self.assertRaises(ValueError):diagram().maximum(2,1)

class ReferenceTests(TestCase):
 def test_thirds(self):
  r=shear_reference_design(diagram(xs=(0,3,6)),context(),API,span_id=1,legs=2)
  self.assertEqual([x['interval_m'] for x in r['thirds']],[[0,2],[2,4],[4,6]])
 def test_independent_maximum(self):
  r=shear_reference_design(diagram(xs=(0,3,6)),context(),API,span_id=1,legs=2)
  self.assertEqual([x['demand']['Vsk_abs_kn'] for x in r['thirds']],[100,100/3,100])
 def test_boundary_in_both(self):
  r=shear_reference_design(diagram((0,100,0),xs=(0,2,6)),context(),API,span_id=1,legs=2)
  self.assertEqual(r['thirds'][0]['demand']['Vsk_abs_kn'],100);self.assertEqual(r['thirds'][1]['demand']['Vsk_abs_kn'],100)
 def test_no_diagram_mutation(self):
  d=diagram();old=deepcopy(d.series);shear_reference_design(d,context(),API,span_id=1,legs=2);self.assertEqual(old,d.series)
 def test_missing_domain(self):
  r=shear_reference_design(diagram((100,None,-100)),context(),API,span_id=1,legs=2)
  self.assertEqual(r['thirds'][0]['reference_options']['status'],'INCONCLUSIVE')
 def test_options_usual_only(self):self.assertEqual([x['diameter_mm'] for x in reference_options(context(),API,50,2)['options']],[5,6.3,8])
 def test_reference_not_selected(self):self.assertIsNone(reference_options(context(),API,50,2)['selected_solution'])
 def test_missing_reference_legs(self):self.assertEqual(reference_options(context(),API,50,None)['status'],'INCONCLUSIVE')
 def test_high_shear_review_not_larger_auto(self):
  r=reference_options(context(),API,350,2);self.assertEqual(r['status'],'REQUIRES_ENGINEERING_REVIEW');self.assertFalse(r['usual_solution_exists'])

class DesignTests(TestCase):
 def test_biela_pass(self):self.assertTrue(design_shear(context(),API,50,5)['diagonal_compression']['passes'])
 def test_biela_failure_separate(self):
  r=check(phi=25,spacing=1,vk=1000);self.assertEqual(r['checks']['diagonal_compression']['status'],'FAIL');self.assertEqual(r['overall_structural_result'],'FAIL')
 def test_biela_strict_equality(self):
  r=design_shear(context(),API,0,5);r=design_shear(context(),API,r['VRd2_kn']/context()['gamma_f'],5);self.assertEqual(r['status'],'FAIL')
 def test_area_pass(self):self.assertEqual(check()['checks']['shear_reinforcement']['status'],'PASS')
 def test_area_fail(self):self.assertEqual(check(phi=5,spacing=30,vk=150)['checks']['shear_reinforcement']['status'],'FAIL')
 def test_minimum(self):self.assertEqual(design_shear(context(),API,0,5)['requirement_governed_by'],'MINIMUM')
 def test_shear_governs(self):self.assertEqual(design_shear(context(),API,200,5)['requirement_governed_by'],'SHEAR')
 def test_code_spacing_independent_area(self):
  r=check(phi=25,spacing=31);self.assertEqual(r['checks']['shear_reinforcement']['status'],'PASS');self.assertEqual(r['checks']['maximum_code_spacing']['status'],'FAIL')
 def test_code_uses_current_d(self):self.assertAlmostEqual(design_shear(context(),API,50,5)['maximum_spacing_code_cm'],28.02)
 def test_code_restrictive_branch(self):self.assertAlmostEqual(design_shear(context(),API,350,5)['maximum_spacing_code_cm'],14.01)
 def test_d_not_api_default(self):self.assertEqual(design_shear(context(),API,50,5)['d_cm'],46.7)
 def test_no_equivalent_phi(self):self.assertIn('no equivalent diameter',design_shear(context(),API,50,5)['provenance']['explicit_depth_adapter'])
 def test_missing_depth(self):
  c=context();c.pop('effective_depth');self.assertEqual(design_shear(c,API,50,5)['status'],'INCONCLUSIVE')
 def test_zero_demand_still_minimum(self):self.assertGreater(design_shear(context(),API,0,5)['governing_Asw_per_s_cm2_m'],0)
 def test_area_units(self):self.assertEqual(design_shear(context(),API,0,5)['units']['Asw_per_s'],'cm2/m')
 def test_real_legs_two(self):self.assertAlmostEqual(check(legs=2)['provided']['Asw_cm2'],2*API.Barra(5).area_cm2)
 def test_real_legs_four(self):self.assertAlmostEqual(check(legs=4)['provided']['Asw_cm2'],4*API.Barra(5).area_cm2)
 def test_missing_legs(self):self.assertEqual(check(legs=None)['overall_structural_result'],'INCONCLUSIVE')
 def test_wide_four_office(self):
  c=context();c['section']['bw']=41;self.assertEqual(check(legs=4,ctx=c)['checks']['number_of_legs']['status'],'PASS')
 def test_wide_two_review_not_fail(self):
  c=context();c['section']['bw']=41;r=check(phi=8,spacing=8,legs=2,ctx=c)
  self.assertEqual(r['checks']['number_of_legs']['status'],'REQUIRES_ENGINEERING_REVIEW');self.assertEqual(r['overall_structural_result'],'PASS')
 def test_unknown_four_leg_holder(self):self.assertEqual(check(legs=4)['checks']['stirrup_holder']['status'],'INCONCLUSIVE')
 def test_verified_four_leg_holder(self):
  r=check(legs=4,holder_compatibility={'passes':True,'provenance':{'drawing':1}});self.assertEqual(r['checks']['stirrup_holder']['status'],'PASS')
 def test_failed_holder(self):self.assertEqual(check(legs=4,holder_compatibility={'passes':False,'provenance':{'drawing':1}})['overall_structural_result'],'FAIL')
 def test_practical_and_code_limits_separate(self):
  r=check(phi=8,spacing=35);self.assertEqual(r['checks']['usual_minimum_spacing']['status'],'PASS');self.assertEqual(r['checks']['maximum_code_spacing']['status'],'FAIL')
 def test_large_phi_not_structural_fail(self):
  r=check(phi=10,spacing=10);self.assertEqual(r['overall_structural_result'],'PASS');self.assertTrue(r['engineering_review_required'])
 def test_dense_spacing_not_structural_fail(self):
  r=check(phi=8,spacing=7);self.assertEqual(r['overall_structural_result'],'PASS');self.assertEqual(r['checks']['usual_minimum_spacing']['status'],'REQUIRES_ENGINEERING_REVIEW')
 def test_usual_can_fail_structurally(self):
  r=check(phi=5,spacing=20,vk=200);self.assertEqual(r['checks']['usual_diameter']['status'],'PASS');self.assertEqual(r['overall_structural_result'],'FAIL')
 def test_no_suspension_capacity_added(self):
  r=check(indirect_support_evidence={'drawing':1});self.assertTrue(r['suspension_check_required']);self.assertEqual(r['suspension_result'],'NOT_EVALUATED')
 def test_region_crosses_thirds_without_penalty(self):self.assertEqual(check(interval=(.2,3.8))['overall_structural_result'],'PASS')
 def test_own_region_max_not_third(self):
  d=diagram((300,0,-300));r=check_drawn_region(d,context(),API,region(interval=(1.9,2.1)))
  self.assertAlmostEqual(r['demand']['Vsk_abs_kn'],15);self.assertEqual(r['overall_structural_result'],'PASS')
 def test_partial_region_unknown(self):self.assertEqual(check(interval=(-1,3))['overall_structural_result'],'INCONCLUSIVE')
 def test_partial_known_fail_remains_fail(self):self.assertEqual(check(phi=5,spacing=30,vk=200,interval=(-1,3))['overall_structural_result'],'FAIL')
 def test_negative_spacing_rejected(self):self.assertEqual(check(spacing=-1)['overall_structural_result'],'INCONCLUSIVE')
 def test_axial_outside_scope(self):
  c=context();c['axial_force_kn']=10;self.assertEqual(design_shear(c,API,50,5)['status'],'INCONCLUSIVE')

class TransitionTests(TestCase):
 def test_left_crossing(self):self.assertAlmostEqual(transition_check(diagram(),50,drawn_x=1,side='LEFT',branch_domain=[0,2])['theoretical_limit_m'],1)
 def test_right_crossing(self):self.assertAlmostEqual(transition_check(diagram(),50,drawn_x=3,side='RIGHT',branch_domain=[2,4])['theoretical_limit_m'],3)
 def test_before_required_fail(self):self.assertEqual(transition_check(diagram(),50,drawn_x=.5,side='LEFT',branch_domain=[0,2])['status'],'FAIL')
 def test_equality_pass(self):self.assertEqual(transition_check(diagram(),50,drawn_x=1,side='LEFT',branch_domain=[0,2])['status'],'PASS')
 def test_conservative_pass(self):self.assertEqual(transition_check(diagram(),50,drawn_x=1.5,side='LEFT',branch_domain=[0,2])['status'],'PASS')
 def test_two_crossings_select_side(self):
  d=diagram();self.assertEqual(len(d.capacity_crossings(50)),2);self.assertEqual(transition_check(d,50,drawn_x=1,side='LEFT',branch_domain=[0,2])['theoretical_limit_m'],1)
 def test_multiple_compatible_ambiguous(self):self.assertEqual(transition_check(diagram((100,0,100,0),(0,1,2,3)),50,drawn_x=1,side='LEFT')['status'],'INCONCLUSIVE')
 def test_gap(self):self.assertEqual(transition_check(diagram((100,None,-100)),50,drawn_x=1,side='LEFT')['status'],'INCONCLUSIVE')
 def test_no_drawing_change(self):self.assertFalse(transition_check(diagram(),50,drawn_x=1,side='LEFT',branch_domain=[0,2])['drawing_changed'])
 def test_multiple_series_governing_last(self):
  d=ShearDiagram([series((100,0,-100)),series((200,0,-200),identity='min')]);r=transition_check(d,50,drawn_x=1.5,side='LEFT',branch_domain=[0,2]);self.assertEqual(r['theoretical_limit_m'],1.5)
 def test_plateau_ambiguous(self):self.assertEqual(transition_check(diagram((100,50,50,0),(0,1,2,3)),50,drawn_x=1,side='LEFT')['status'],'INCONCLUSIVE')
 def test_inverse_uses_real_api(self):
  r=inverse_shear_capacity(context(),API,5,4);self.assertEqual(r['status'],'PASS');capacity=r['Vk_capacity_kn'];self.assertLessEqual(design_shear(context(),API,capacity,5)['governing_Asw_per_s_cm2_m'],4)
 def test_below_minimum_has_no_inverse(self):self.assertEqual(inverse_shear_capacity(context(),API,5,.1)['status'],'INCONCLUSIVE')
 def test_always_sufficient_no_crossing(self):self.assertEqual(transition_check(diagram(),200,drawn_x=0,side='LEFT')['status'],'NOT_APPLICABLE')

class DepthAndCoverageTests(TestCase):
 def candidate(self,layers,area,d):
  return {'span':1,'start_m':0,'end_m':1,'marks':['A'],'result':{'regions':[{'configuration':{'layers':[{'count':1}]*layers},'concretopy':{'d_equivalente_cm':d,'as_total_cm2':area}}]}}
 def test_most_layers_before_area(self):
  r=select_shear_depth([self.candidate(1,20,50),self.candidate(2,5,46)]);self.assertEqual(r['d_cm'],46)
 def test_more_area_at_same_layers(self):
  r=select_shear_depth([self.candidate(2,5,45),self.candidate(2,10,47)]);self.assertEqual(r['d_cm'],47)
 def test_min_depth_at_same_layers_and_area(self):
  r=select_shear_depth([self.candidate(2,10,47),self.candidate(2,10,46)]);self.assertEqual(r['d_cm'],46)
 def test_all_equal_governing_preserved(self):
  r=select_shear_depth([self.candidate(2,10,47)]*2);self.assertEqual(len(r['governing']),2)
 def test_unresolved_geometry_no_depth(self):self.assertEqual(select_shear_depth([])['status'],'INCONCLUSIVE')
 def test_larger_diameter_not_usual_option(self):self.assertEqual(reference_options(context(),API,50,2,(10,))['status'],'REQUIRES_ENGINEERING_REVIEW')
 def test_decline_followed_by_incompatible_rise(self):
  self.assertEqual(transition_check(diagram(),50,drawn_x=1,side='LEFT')['status'],'INCONCLUSIVE')
 def test_unknown_transition_side(self):self.assertEqual(transition_check(diagram(),50,drawn_x=1,side='UNKNOWN')['status'],'INCONCLUSIVE')
 def test_code_uses_nondefault_gamma_and_depth(self):
  c=context();c['gamma_c']=1.6;r=design_shear(c,API,350,5)
  self.assertEqual(r['maximum_spacing_code_cm'],14.01);self.assertLess(r['VRd2_kn'],design_shear(context(),API,350,5)['VRd2_kn'])

class GlobalAndGoldenTests(TestCase):
 def test_missing_span_diagram_is_structured_unknown(self):
  r=review_shear_spans([{'span_id':1,'series':[]}],context(),API);self.assertIsNone(r['global_shear_approval']);self.assertTrue(r['inconclusive_items'])
 def test_reference_diagonal_failure_is_not_ignored(self):
  r=review_shear_spans([{'span_id':1,'series':[series((1000,0,-1000))],'reference_legs':2,'support_geometry':{'left':{'type':'COLUMN','type_source':'synthetic column','source':'synthetic geometry','axis_m':-0.1,'width_m':0.2,'left_face_m':-0.2,'right_face_m':0},'right':{'type':'COLUMN','type_source':'synthetic column','source':'synthetic geometry','axis_m':4.1,'width_m':0.2,'left_face_m':4,'right_face_m':4.2}},'drawn_regions':[]}],context(),API);self.assertFalse(r['global_shear_approval'])
 def test_reference_usual_review_item_reported(self):
  r=review_shear_spans([{'span_id':1,'series':[series((350,0,-350))],'reference_legs':2,'support_geometry':{'left':{'type':'COLUMN','type_source':'synthetic column','source':'synthetic geometry','axis_m':-0.1,'width_m':0.2,'left_face_m':-0.2,'right_face_m':0},'right':{'type':'COLUMN','type_source':'synthetic column','source':'synthetic geometry','axis_m':4.1,'width_m':0.2,'left_face_m':4,'right_face_m':4.2}},'drawn_regions':[region(phi=10,spacing=8)]}],context(),API);self.assertTrue(r['engineering_review_items'])
 def test_complete_pass(self):
  r=review_shear_spans([{'span_id':1,'series':[series((50,0,-50))],'reference_legs':2,'support_geometry':{'left':{'type':'COLUMN','type_source':'synthetic column','source':'synthetic geometry','axis_m':-0.1,'width_m':0.2,'left_face_m':-0.2,'right_face_m':0},'right':{'type':'COLUMN','type_source':'synthetic column','source':'synthetic geometry','axis_m':4.1,'width_m':0.2,'left_face_m':4,'right_face_m':4.2}},'drawn_regions':[region()]}],context(),API)
  self.assertTrue(r['global_shear_approval']);self.assertTrue(r['suspension_not_evaluated']);self.assertIsNone(r['selected_solution'])
 def test_failure_global(self):
  r=review_shear_spans([{'span_id':1,'series':[series((200,0,-200))],'reference_legs':2,'support_geometry':{'left':{'type':'COLUMN','type_source':'synthetic column','source':'synthetic geometry','axis_m':-0.1,'width_m':0.2,'left_face_m':-0.2,'right_face_m':0},'right':{'type':'COLUMN','type_source':'synthetic column','source':'synthetic geometry','axis_m':4.1,'width_m':0.2,'left_face_m':4,'right_face_m':4.2}},'drawn_regions':[region(spacing=30)]}],context(),API);self.assertFalse(r['global_shear_approval'])
 def test_uncovered_global_null(self):
  r=review_shear_spans([{'span_id':1,'series':[series((50,0,-50))],'reference_legs':2,'support_geometry':{'left':{'type':'COLUMN','type_source':'synthetic column','source':'synthetic geometry','axis_m':-0.1,'width_m':0.2,'left_face_m':-0.2,'right_face_m':0},'right':{'type':'COLUMN','type_source':'synthetic column','source':'synthetic geometry','axis_m':4.1,'width_m':0.2,'left_face_m':4,'right_face_m':4.2}},'drawn_regions':[region(interval=(.1,3.9))]}],context(),API);self.assertIsNone(r['global_shear_approval'])
 def test_overlapping_ranges_unknown(self):
  r=review_shear_spans([{'span_id':1,'series':[series((50,0,-50))],'reference_legs':2,'support_geometry':{'left':{'type':'COLUMN','type_source':'synthetic column','source':'synthetic geometry','axis_m':-0.1,'width_m':0.2,'left_face_m':-0.2,'right_face_m':0},'right':{'type':'COLUMN','type_source':'synthetic column','source':'synthetic geometry','axis_m':4.1,'width_m':0.2,'left_face_m':4,'right_face_m':4.2}},'drawn_regions':[region(),region(interval=(1,3))]}],context(),API);self.assertIsNone(r['global_shear_approval'])
 def test_consecutive_ranges_independent(self):
  r=review_shear_spans([{'span_id':1,'series':[series((50,0,-50))],'reference_legs':2,'support_geometry':{'left':{'type':'COLUMN','type_source':'synthetic column','source':'synthetic geometry','axis_m':-0.1,'width_m':0.2,'left_face_m':-0.2,'right_face_m':0},'right':{'type':'COLUMN','type_source':'synthetic column','source':'synthetic geometry','axis_m':4.1,'width_m':0.2,'left_face_m':4,'right_face_m':4.2}},'drawn_regions':[region(interval=(0,2)),region(interval=(2,4))]}],context(),API);self.assertEqual(len(r['shear_drawn_regions']),2);self.assertTrue(r['global_shear_approval'])
 def test_real_independent_beams(self):
  a,b=[json.loads((ROOT/'analises/pranchas'/ (beam+'_shear_reinforcement_review.json')).read_text(encoding='utf8')) for beam in ('V516','V517')]
  self.assertNotEqual(a['shear_drawn_regions'][2]['demand']['Vsk_abs_kn'],b['shear_drawn_regions'][2]['demand']['Vsk_abs_kn'])
 def test_real_depth(self):
  for beam in ('V516','V517'):
   r=json.loads((ROOT/'analises/pranchas'/ (beam+'_shear_reinforcement_review.json')).read_text(encoding='utf8'))
   self.assertEqual(r['effective_depth_selection']['d_cm'],46.7);self.assertEqual(r['effective_depth_selection']['selected']['provenance']['marks'],['N7','N8','N9'])
 def test_real_n12_no_assumed_legs(self):
  for beam in ('V516','V517'):
   r=json.loads((ROOT/'analises/pranchas'/ (beam+'_shear_reinforcement_review.json')).read_text(encoding='utf8'))
   self.assertIsNone(r['global_shear_approval'])
   for x in r['excluded_reinforcement']:self.assertIsNone(x['piece']['legs']);self.assertEqual(x['classification']['status'],'NOT_APPLICABLE')
 def test_real_special_region_not_merged(self):
  for beam in ('V516','V517'):
   r=json.loads((ROOT/'analises/pranchas'/ (beam+'_shear_reinforcement_review.json')).read_text(encoding='utf8'));special=[x for x in r['shear_drawn_regions'] if x['region']['mark']=='N1']
   self.assertEqual(len(special),1);self.assertEqual(special[0]['region']['interval_m'],[8.64,9.16]);self.assertEqual(special[0]['suspension_result'],'NOT_EVALUATED')
 def test_real_conventional_pass(self):
  for beam in ('V516','V517'):
   r=json.loads((ROOT/'analises/pranchas'/ (beam+'_shear_reinforcement_review.json')).read_text(encoding='utf8'))
   self.assertTrue(all(x['overall_structural_result']=='PASS' for x in r['shear_drawn_regions']))
 def test_real_thirds_twelve(self):
  r=json.loads((ROOT/'analises/pranchas/V516_shear_reinforcement_review.json').read_text(encoding='utf8'));self.assertEqual(sum(len(x['thirds']) for x in r['shear_reference_design']),12)
 def test_real_longitudinal_not_changed(self):
  r=json.loads((ROOT/'analises/pranchas/V516_shear_reinforcement_review.json').read_text(encoding='utf8'));self.assertFalse(r['longitudinal_results_modified']);self.assertIsNone(r['detailing_optimization'])

def usual_phi(phi):
 def test(self):self.assertEqual(check(phi=phi,spacing=8)['checks']['usual_diameter']['status'],'PASS')
 return test
for phi in (5,6.3,8):setattr(DesignTests,'test_usual_phi_'+str(phi).replace('.','_'),usual_phi(phi))
def usual_spacing(spacing):
 def test(self):self.assertEqual(check(phi=8,spacing=spacing)['checks']['usual_minimum_spacing']['status'],'PASS')
 return test
for spacing in (8,10,20):setattr(DesignTests,'test_usual_spacing_'+str(spacing),usual_spacing(spacing))
