"""Real Concretopy orchestration and independent negative end-node controls."""
from copy import deepcopy
from unittest import TestCase
from test_longitudinal_negative import api,context,bar
from negative_end_support_review import check_negative_end_support,transverse_disposition,review_negative_end_support
from support_geometry import SupportGeometry
from moment_diagram import MomentDiagram
from longitudinal_review import basic_anchorage

class NegativeEndSupportTests(TestCase):
 def setUp(self):
  self.ctx=context();self.ctx['section']['bw']=30
  self.b=bar('A',count=2,start=-.215,end=4.215);self.b['shape']='bent';self.b['trajectory_id']='physical-A'
  self.d=MomentDiagram([{'section':1,'x_m':.1,'value_knm':-50,'provenance':{'TQS':'S1'}},{'section':13,'x_m':4,'value_knm':-20,'provenance':{'TQS':'S13'}}],{'synthetic':'signed terminal samples'})
 def geometry(self,side='LEFT',width=24):
  if side=='LEFT':return SupportGeometry(1,'P','LEFT','END',0,-width/100,-width/200,width,{'drawing':'physical faces'})
  return SupportGeometry(1,'P','RIGHT','END',4,4+width/100,4+width/200,width,{'drawing':'physical faces'})
 def check(self,side='LEFT',leg=70,ctx=None,prov=True,b=None,col=None,layout=None,d=None,width=24):
  return check_negative_end_support([b or self.b],ctx or self.ctx,d or self.d,api,geometry=self.geometry(side,width),mark='A',
   bend_leg_cm=leg,bend_provenance={'drawing':'vertical leg','orientation':'vertical','support_side':side} if prov else None,
   column_geometry=col,transverse_layout=layout)
 def test_left_bend(self):self.assertEqual(self.check()['anchorage_mode'],'VERTICAL_BEND')
 def test_right_bend(self):self.assertEqual(self.check('RIGHT')['anchorage_mode'],'VERTICAL_BEND')
 def test_longer_pass(self):self.assertEqual(self.check()['checks']['vertical_bend_geometry']['status'],'PASS')
 def test_equal_pass(self):self.assertEqual(self.check(leg=69)['checks']['vertical_bend_geometry']['status'],'PASS')
 def test_short_fail(self):self.assertEqual(self.check(leg=40)['checks']['vertical_bend_geometry']['status'],'FAIL')
 def test_height_governs(self):self.assertEqual(self.check()['checks']['vertical_bend_geometry']['governing'],'GEOMETRY')
 def test_two_basic_lb_governs(self):
  ctx=deepcopy(self.ctx);ctx['section']['h']=200;r=self.check(ctx=ctx,leg=200)['checks']['vertical_bend_geometry'];self.assertEqual(r['governing'],'TWO_BASIC_LB');self.assertEqual(r['vertical_bend_required_cm'],r['two_lb_cm'])
 def test_total_height_not_d(self):
  r=self.check();c=r['checks']['vertical_bend_geometry'];self.assertEqual(c['beam_height_cm'],72);self.assertEqual(c['vertical_bend_required_cm'],69);self.assertNotEqual(c['vertical_bend_required_cm'],r['checks']['flexural_capacity']['d_equivalent_cm'])
 def test_documentary_leg_missing(self):self.assertEqual(self.check(leg=None)['checks']['vertical_bend_geometry']['status'],'INCONCLUSIVE')
 def test_bend_not_invented(self):self.assertEqual(self.check(prov=False)['anchorage_mode'],'UNRESOLVED')
 def test_no_horizontal_vertical_equivalence(self):
  r=self.check(leg=40);self.assertGreater(r['checks']['straight_anchorage_geometry']['documentary_horizontal_projection_cm']+40,0);self.assertEqual(r['checks']['vertical_bend_geometry']['status'],'FAIL');self.assertEqual(r['checks']['curved_anchorage_resistance']['status'],'INCONCLUSIVE')
 def test_no_hook_reduction(self):self.assertEqual(self.check()['lb_basic_cm'],basic_anchorage(16,self.ctx,api,flexure_sign='NEGATIVE')['result']['lb_cm'])
 def test_terminal_left_S1(self):self.assertEqual(self.check()['terminal_demand']['section'],1)
 def test_terminal_right_S13(self):self.assertEqual(self.check('RIGHT')['terminal_demand']['section'],13)
 def test_terminal_not_geometric_origin(self):
  r=self.check();self.assertEqual(r['terminal_demand']['x_m'],.1);self.assertEqual(r['checks']['straight_anchorage_geometry']['reference_face_m'],0);self.assertNotIn('reference_x_m',r['checks']['vertical_bend_geometry'])
 def test_capacity_pass_bend_failure_independent(self):
  r=self.check(leg=40);self.assertEqual(r['checks']['flexural_capacity']['status'],'PASS');self.assertEqual(r['checks']['vertical_bend_geometry']['status'],'FAIL')
 def test_capacity_fail_bend_pass_independent(self):
  points=deepcopy(self.d.points);points[0]['value_knm']=-1000;d=MomentDiagram(points,self.d.provenance);r=self.check(d=d);self.assertEqual(r['checks']['flexural_capacity']['status'],'FAIL');self.assertEqual(r['checks']['vertical_bend_geometry']['status'],'PASS')
 def test_unknown_terminal_does_not_block_bend(self):
  points=deepcopy(self.d.points);points[0]['value_knm']=None;d=MomentDiagram(points,self.d.provenance);r=self.check(d=d);self.assertEqual(r['checks']['flexural_capacity']['status'],'INCONCLUSIVE');self.assertEqual(r['checks']['vertical_bend_geometry']['status'],'PASS')
 def test_column_missing_does_not_block_bend(self):
  r=self.check();self.assertEqual(r['checks']['column_interference_spacing']['status'],'INCONCLUSIVE');self.assertEqual(r['checks']['vertical_bend_geometry']['status'],'PASS')
 def test_effective_cover_not_resistant_geometry(self):
  old=deepcopy(self.ctx);a=self.check();b=self.check(col={'perpendicular_width_cm':30,'provenance':{'drawing':'column'}})
  self.assertEqual(a['capacity'],b['capacity']);self.assertEqual(self.ctx,old)
 def test_mark_global_use_preserved(self):
  r=self.check();self.assertEqual(r['physical_bar'],self.b);self.assertEqual(r['physical_bar']['trajectory_id'],'physical-A');self.assertIsNone(r['selected_solution']);self.assertIsNone(r['detailing_optimization'])
 def test_not_negative_demand_no_reduction_proposal(self):
  points=deepcopy(self.d.points);points[0]['value_knm']=50;d=MomentDiagram(points,self.d.provenance);r=self.check(d=d);self.assertEqual(r['checks']['flexural_capacity']['status'],'NOT_APPLICABLE');self.assertFalse(r['checks']['flexural_capacity']['selected_mark_required_at_terminal']);self.assertIsNone(r['detailing_optimization'])
 def test_straight_when_available(self):
  b=deepcopy(self.b);b.update(shape='straight',x_start_common=-1)
  r=self.check(width=140,b=b);self.assertEqual(r['anchorage_mode'],'STRAIGHT');self.assertEqual(r['checks']['vertical_bend_geometry']['status'],'NOT_APPLICABLE')

 def test_autonomous_mark_discovery(self):
  outside=bar('OUT',start=1,end=3)
  r=review_negative_end_support([self.b,outside],self.ctx,self.d,api,geometry=self.geometry(),bend_documents={'A':{'side':'LEFT','orientation':'vertical','vertical_leg_cm':70,'provenance':{'drawing':1}}})
  self.assertEqual([x['bar'] for x in r['marks']],['A']);self.assertEqual(r['marks'][0]['checks']['vertical_bend_geometry']['status'],'PASS')
 def test_bend_negative_does_not_block_flexure(self):
  r=self.check(leg=-1);self.assertEqual(r['checks']['vertical_bend_geometry']['status'],'INCONCLUSIVE');self.assertEqual(r['checks']['flexural_capacity']['status'],'PASS')

class TransverseDispositionTests(TestCase):
 def setUp(self):self.section=context()['section'];self.section['bw']=30
 def check(self,xs,phi=16,col=None):
  b=bar('A',count=len(xs),phi=phi)
  layout={'provenance':{'drawing':'actual dimensioned centers'},'layers':[{'layer':1,'bars':[{'mark':'A','diameter_mm':phi,'x_cm':x} for x in xs]}]}
  return transverse_disposition(self.section,[b],layout=layout,column_geometry=col)
 def test_corridor_above_four(self):self.assertEqual(self.check([4,10])['vibrator_access_spacing']['status'],'PASS')
 def test_corridor_exactly_four(self):self.assertEqual(self.check([4,9.6])['vibrator_access_spacing']['status'],'PASS')
 def test_all_corridors_below_four(self):
  r=self.check([4,9.5,15]);self.assertEqual(r['minimum_bar_spacing']['status'],'PASS');self.assertEqual(r['vibrator_access_spacing']['status'],'FAIL')
 def test_only_one_corridor_four(self):
  r=self.check([4,7.6,13.2]);self.assertEqual(r['vibrator_access_spacing']['status'],'PASS');self.assertEqual([g['free_cm'] for g in r['minimum_bar_spacing']['layers'][0]['gaps']],[2,4])
 def test_minimum_still_required(self):
  r=self.check([4,6.6,14]);self.assertEqual(r['minimum_bar_spacing']['status'],'FAIL');self.assertTrue(r['vibrator_access_spacing']['raw_corridor_passes']);self.assertEqual(r['vibrator_access_spacing']['status'],'FAIL')
 def test_free_spacing_not_axis_spacing(self):self.assertEqual(self.check([4,9.6])['vibrator_access_spacing']['maximum_free_spacing_cm'],4)
 def test_effective_cover_overlay(self):
  r=self.check([4,10],col={'perpendicular_width_cm':30,'provenance':{'drawing':'column'}});c=r['column_interference_spacing'];self.assertEqual(c['effective_lateral_cover_cm'],5);self.assertEqual(c['useful_width_cm'],20);self.assertEqual(c['status'],'FAIL');self.assertEqual(r['minimum_bar_spacing']['status'],'PASS')
 def test_column_overlay_pass(self):self.assertEqual(self.check([7,14],col={'perpendicular_width_cm':30,'provenance':{'drawing':'column'}})['column_interference_spacing']['status'],'PASS')
 def test_column_other_width_not_applicable(self):self.assertEqual(self.check([4,10],col={'perpendicular_width_cm':40,'provenance':{'drawing':'column'}})['column_interference_spacing']['status'],'NOT_APPLICABLE')
 def test_unknown_column_independent(self):
  r=self.check([4,10]);self.assertEqual(r['column_interference_spacing']['status'],'INCONCLUSIVE');self.assertEqual(r['vibrator_access_spacing']['status'],'PASS')
 def test_layout_missing_not_assumed_uniform(self):self.assertEqual(transverse_disposition(self.section,[bar()])['vibrator_access_spacing']['status'],'INCONCLUSIVE')
 def test_column_no_dimension_even_with_support_name(self):self.assertEqual(self.check([4,10],col={'support_name':'P','provenance':{'drawing':'support'}})['column_interference_spacing']['status'],'INCONCLUSIVE')
 def test_caller_tolerance_requires_provenance(self):self.assertEqual(self.check([7,14],col={'perpendicular_width_cm':30.01,'equivalence_tolerance_cm':.1,'provenance':{'drawing':'column'}})['column_interference_spacing']['status'],'INCONCLUSIVE')
 def test_caller_explicit_tolerance(self):self.assertEqual(self.check([7,14],col={'perpendicular_width_cm':30.01,'equivalence_tolerance_cm':.1,'tolerance_provenance':{'engineer':'explicit equivalence'},'provenance':{'drawing':'column'}})['column_interference_spacing']['status'],'PASS')
 def test_no_input_mutation(self):
  old=deepcopy(self.section);self.check([7,14],col={'perpendicular_width_cm':30,'provenance':{'drawing':'column'}});self.assertEqual(self.section,old)
