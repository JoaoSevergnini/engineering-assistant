"""Structural dispatch tests: real Concretopy, no duplicated resistance formulas."""
from copy import deepcopy
from decimal import Decimal
from unittest import TestCase
from test_longitudinal_negative import api,context,bar,diagram,shear
from intermediate_support_review import check_intermediate_bar_event,ANCHORAGE
from longitudinal_review import basic_anchorage,check_bar_event
from support_geometry import SupportGeometry

class IntermediateDispatchTests(TestCase):
 def setUp(self):
  self.bars=[bar('KEEP',start=-4),bar('A',2,start=-4,end=3.6)]
  for b in self.bars:b['trajectory_id']=b['mark'];b['continuity_documentation']={'drawing':'continuous piece'}
  self.g=SupportGeometry('adj','SUP','LEFT','INTERMEDIATE',.2,-.2,0,40,{'drawing':'physical support, independent of sample origin'})
  self.adj=diagram((-50,-20,0),(.4,2,4));self.prev=diagram((0,-100,-300),(-4,-2,-.4))
 def check(self,mark='A',bars=None,adj=None,g=None,prev=True,branch=None,previous=None):
  return check_intermediate_bar_event(bars or self.bars,context(),adj or self.adj,shear(),api,mark=mark,
   cut_side='LEFT' if g and g.support_side=='RIGHT' else 'RIGHT',support=g or self.g,
   previous_bars=previous if previous is not None else bars or self.bars,previous_context=context() if prev else None,
   previous_diagram=self.prev if prev else None,branch_domain=branch)
 def test_needed_previous_not_adjacent(self):
  r=self.check();self.assertEqual(r['classification'],ANCHORAGE);self.assertTrue(r['required_in_previous_span']);self.assertFalse(r['required_in_adjacent_span'])
 def test_pass(self):self.assertTrue(self.check()['passes'])
 def test_equality_pass(self):
  bars=deepcopy(self.bars);lb=basic_anchorage(16,context(),api,flexure_sign='NEGATIVE')['result']['lb_cm'];bars[1]['x_end_common']=float(Decimal('.2')+Decimal(str(lb))/100)
  r=self.check(bars=bars);self.assertEqual(r['checks']['basic_lb_beyond_support']['margin_cm'],0);self.assertTrue(r['passes'])
 def test_short_failure(self):
  bars=deepcopy(self.bars);bars[1]['x_end_common']=.6;r=self.check(bars=bars);self.assertEqual(r['classification'],ANCHORAGE);self.assertFalse(r['passes'])
 def test_no_al_or_crossing_controls(self):
  r=self.check();self.assertEqual(list(r['checks']),['basic_lb_beyond_support']);self.assertNotIn('al',r);self.assertNotIn('capacity_crossing',r)
 def test_face_not_terminal(self):
  r=self.check();self.assertEqual(r['anchorage_reference_face']['x_m'],.2);self.assertEqual(r['support_terminal_demand']['x_m'],.4);self.assertEqual(r['checks']['basic_lb_beyond_support']['available_length_cm'],340)
 def test_gap_inconclusive(self):self.assertEqual(self.check(adj=diagram((-50,None,0),(.4,2,4)))['classification'],'INCONCLUSIVE')
 def test_missing_previous_inconclusive(self):self.assertEqual(self.check(prev=False)['classification'],'INCONCLUSIVE')
 def test_crossing_remains_scaling(self):
  d=diagram((-180,-100,0),(.4,2,4));r=self.check(adj=d);old=check_bar_event(self.bars,context(),d,shear(),api,mark='A',cut_side='RIGHT');self.assertEqual(r['classification'],'SCALING');self.assertEqual(r['checks'],old['checks'])
 def test_insufficient_without_crossing_not_anchorage(self):self.assertEqual(self.check(adj=diagram((-300,-280,-260),(.4,2,4)))['classification'],'INCONCLUSIVE')
 def test_truncated_branch_cannot_hide_demand(self):
  r=self.check(adj=diagram((-180,-20,0),(.4,2,4)),branch=[2,4]);self.assertTrue(r['required_in_adjacent_span']);self.assertNotEqual(r['classification'],ANCHORAGE)
 def test_coincident_two_independent(self):
  bars=self.bars+[bar('B',3,count=1,phi=12.5,start=-4,end=3.6)]
  for b in bars:b['trajectory_id']=b['mark'];b['continuity_documentation']={'drawing':1}
  for m in ('A','B'):
   r=self.check(m,bars);self.assertEqual(r['classification'],ANCHORAGE);self.assertEqual([b['mark'] for b in r['reinforcement_after_cut']],['KEEP'])
 def test_coincident_three_independent(self):
  bars=self.bars+[bar('B',3,count=1,phi=12.5,start=-4,end=3.6),bar('C',4,count=1,phi=10,start=-4,end=3.6)]
  for b in bars:b['trajectory_id']=b['mark'];b['continuity_documentation']={'drawing':1}
  for m in ('A','B','C'):
   r=self.check(m,bars);self.assertEqual(r['classification'],ANCHORAGE);self.assertIsNone(r['termination_event']['ordered_cut_sequence'])
 def test_reverse_order_same_results(self):self.assertEqual(self.check()['checks'],self.check(bars=list(reversed(self.bars)))['checks'])
 def test_bar_identity_not_inferred_from_diameter(self):
  bars=deepcopy(self.bars);bars[1]['trajectory_id']='other';self.assertEqual(self.check(previous=bars)['classification'],'INCONCLUSIVE')
 def test_no_documented_continuity(self):
  bars=deepcopy(self.bars);bars[1].pop('continuity_documentation');self.assertEqual(self.check(bars=bars)['classification'],'INCONCLUSIVE')
 def test_previous_not_needed_not_applicable_rule(self):
  self.prev=diagram((0,-20,-40),(-4,-2,-.4));self.assertEqual(self.check()['classification'],'INCONCLUSIVE')
 def test_mirrored_left(self):
  bars=deepcopy(self.bars)
  for b in bars:b['x_start_common'],b['x_end_common']=-b['x_end_common'],-b['x_start_common']
  self.prev=diagram((-300,-100,0),(.4,2,4));g=SupportGeometry('adj','SUP','RIGHT','INTERMEDIATE',-.2,.2,0,40,{'drawing':'mirrored support'})
  d=diagram((0,-20,-50),(-4,-2,-.4));d.points[-1]['section']=13
  r=self.check(bars=bars,adj=d,g=g);self.assertEqual(r['classification'],ANCHORAGE);self.assertTrue(r['passes']);self.assertEqual(r['anchorage_reference_face']['face'],'left');self.assertEqual(r['checks']['basic_lb_beyond_support']['available_length_cm'],340)
 def test_no_optimization(self):self.assertIsNone(self.check()['detailing_optimization']);self.assertIsNone(self.check()['selected_solution'])
 def test_original_not_mutated(self):
  old=deepcopy(self.bars);self.check();self.assertEqual(self.bars,old)

 def test_wide_support_depev_sample_distinct(self):
  g=SupportGeometry('adj','WIDE','LEFT','INTERMEDIATE',.71,-.71,0,142,{'RELDTFPS':{'DEPEV':.554}})
  r=self.check(g=g,adj=diagram((-50,-20,0),(.554,2,4)));self.assertEqual(r['classification'],ANCHORAGE);self.assertEqual(r['anchorage_reference_face']['x_m'],.71);self.assertEqual(r['support_terminal_demand']['x_m'],.554);self.assertEqual(r['checks']['basic_lb_beyond_support']['available_length_cm'],289)

 def test_positive_moment_never_negative_demand(self):
  r=self.check(adj=diagram((-50,-20,500),(.4,2,4)));self.assertEqual(r['classification'],ANCHORAGE);self.assertEqual(r['adjacent_need_evidence']['maximum_negative_demand_knm'],50)
 def test_end_outside_known_adjacent_span(self):
  ctx=context();ctx['span_domain_m']=[0,3]
  r=check_intermediate_bar_event(self.bars,ctx,self.adj,shear(),api,mark='A',cut_side='RIGHT',support=self.g,previous_bars=self.bars,previous_context=context(),previous_diagram=self.prev)
  self.assertEqual(r['classification'],'INCONCLUSIVE');self.assertIn('bar_end_outside_known_adjacent_span',r['diagnostics'])
