"""Independent mark identities with real Concretopy and unchanged event controls."""
from copy import deepcopy
from unittest import TestCase
from test_longitudinal_negative import api,context,bar,diagram,shear
from longitudinal_review import check_bar_event,negative_support_terminal_demand
from termination_event import describe_termination
from moment_diagram import MomentDiagram

class CoincidentTerminationTests(TestCase):
 def bars(self):return [bar('KEEP'),bar('A',2,phi=16,end=3.6),bar('B',3,phi=12.5,count=1,end=3.6)]
 def check(self,mark,bars=None,side='RIGHT',d=None):return check_bar_event(bars or self.bars(),context(),d or diagram(),shear(),api,mark=mark,cut_side=side)
 def test_two_independent_marks(self):
  for mark in ('A','B'):
   r=self.check(mark);self.assertTrue(r['complete']);self.assertEqual(r['termination_event']['selected_mark'],mark)
 def test_three_coincident_marks(self):
  bars=self.bars()+[bar('C',4,count=1,phi=10,end=3.6)]
  for mark in ('A','B','C'):
   r=self.check(mark,bars);self.assertEqual(r['termination_event']['geometrically_terminated_marks'],['A','B','C']);self.assertTrue(r['complete'])
 def test_different_diameters(self):self.assertNotEqual(self.check('A')['lb_basic_cm'],self.check('B')['lb_basic_cm'])
 def test_different_layers(self):
  a=self.check('A');self.assertEqual([b['layers'] for b in a['reinforcement_before_cut']],[[2],[0,2],[0,0,1]])
 def test_different_quantities(self):self.assertEqual([b['bars'] for b in self.check('B')['reinforcement_before_cut']],[2,2,1])
 def test_required_ends_distinct_provided_equal(self):
  a,b=self.check('A'),self.check('B');self.assertEqual(a['provided_end_position_m'],b['provided_end_position_m']);self.assertNotEqual(a['required_end_position_m'],b['required_end_position_m'])
 def test_real_after_not_selected_removal(self):
  for mark in ('A','B'):self.assertEqual([b['mark'] for b in self.check(mark)['reinforcement_after_cut']],['KEEP'])
 def test_no_artificial_sequence(self):self.assertIsNone(self.check('A')['termination_event']['ordered_cut_sequence'])
 def test_order_independent(self):
  for mark in ('A','B'):
   a,b=self.check(mark),self.check(mark,list(reversed(self.bars())))
   self.assertEqual(a['termination_event'],b['termination_event']);self.assertEqual(a['checks'],b['checks']);self.assertEqual(a['required_end_position_m'],b['required_end_position_m'])
 def test_shared_actual_remaining_capacity(self):self.assertEqual(self.check('A')['capacity_remaining'],self.check('B')['capacity_remaining'])
 def test_actual_before_centroid_shared(self):self.assertEqual(self.check('A')['d_for_al'],self.check('B')['d_for_al'])
 def test_own_ten_phi(self):self.assertEqual((self.check('A')['ten_phi_cm'],self.check('B')['ten_phi_cm']),(16,12.5))
 def test_input_not_mutated(self):
  bars=self.bars();old=deepcopy(bars);self.check('A',bars);self.check('B',bars);self.assertEqual(bars,old)
 def test_left_symmetric(self):
  bars=self.bars()
  for b in bars:b['x_start_common'],b['x_end_common']=-b['x_end_common'],-b['x_start_common']
  for mark in ('A','B'):
   a,b=self.check(mark),self.check(mark,bars,'LEFT',diagram((0,-180,0),(-4,-2,0)))
   self.assertEqual(a['checks']['al_plus_lb']['required_length_cm'],b['checks']['al_plus_lb']['required_length_cm']);self.assertAlmostEqual(a['required_end_position_m'],-b['required_end_position_m'])
 def test_single_mark_preserved(self):
  r=self.check('A',self.bars()[:2]);self.assertEqual(r['termination_event']['other_coincident_marks'],[]);self.assertTrue(r['complete'])
 def test_replacement_not_silently_accepted(self):
  with self.assertRaises(ValueError):describe_termination(['KEEP','A'],['KEEP','NEW'],'A',3.6,'RIGHT')
 def test_selected_mark_must_end(self):
  with self.assertRaises(ValueError):describe_termination(['KEEP','A'],['KEEP'],'KEEP',3.6,'RIGHT')
 def test_no_crossing_remains_unresolved(self):
  r=self.check('A',d=diagram((0,-50,0)));self.assertIsNone(r['passes']);self.assertIsNone(r['required_end_position_m']);self.assertIn('remaining_sufficient_entire_branch',r['diagnostics'])
 def test_margin_and_required_end_audit(self):
  r=self.check('A')
  for c in r['checks'].values():self.assertAlmostEqual(c['margin_cm'],c['available_length_cm']-c['required_length_cm']);self.assertIsNotNone(c['required_end_position_m'])

class TerminalDemandTests(TestCase):
 def d(self,left=-60,right=-20):return MomentDiagram([{'section':1,'x_m':11.554,'value_knm':left,'provenance':{'tqs':'S1'}},{'section':13,'x_m':13.68,'value_knm':right,'provenance':{'tqs':'S13'}}],{'synthetic':'sample gap to support axis intentionally retained'})
 def test_left_direct_s1(self):
  r=negative_support_terminal_demand(self.d(),'LEFT');self.assertEqual((r['section'],r['x_m'],r['Msk_signed_knm']),(1,11.554,-60));self.assertEqual(r['rule'],'engineer_confirmed_negative_support_terminal_section_demand_v1')
 def test_right_direct_s13(self):self.assertEqual(negative_support_terminal_demand(self.d(),'RIGHT')['section'],13)
 def test_positive_not_absolute_negative(self):self.assertEqual(negative_support_terminal_demand(self.d(left=40),'LEFT')['negative_demand_knm'],0)
 def test_missing_terminal_not_interpolated(self):
  with self.assertRaises(ValueError):negative_support_terminal_demand(diagram(),'RIGHT')
