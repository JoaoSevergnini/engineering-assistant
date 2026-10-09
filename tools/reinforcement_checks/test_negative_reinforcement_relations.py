"""Contracts, real public Concretopy and historical regression protection."""
from copy import deepcopy
from decimal import Decimal
from pathlib import Path
import json
from unittest import TestCase
from unittest.mock import patch
from test_longitudinal_negative import api,bar,context,diagram
from longitudinal_review import basic_anchorage,prepare_reinforcement,composition_capacity
from negative_end_support_review import transverse_disposition
from negative_reinforcement_relations import review_negative_relation,interval_demand,compare_detailing_mass,local_overlap_disposition
from steel_mass import steel_mass

ROOT=Path(__file__).resolve().parents[2]

def supports():
 return [{'id':'A','occurrence':1,'left_face_m':-.1,'right_face_m':.1,'provenance':{'synthetic':True}},
  {'id':'B','occurrence':2,'left_face_m':3.9,'right_face_m':4.1,'provenance':{'synthetic':True}}]
def evidence(role='adjacent_support_tails'):
 return {'support_ids':['A','B'],'role':role,'existing_tail_meeting_confirmed':True,'provenance':{'synthetic':'documented structural association'}}
def groups():return bar('A',count=3,phi=16,start=-.2,end=3),bar('B',count=2,phi=20,start=1,end=4.2)
def required(gap):return {'required_end_bar_a_m':1,'required_start_bar_b_m':float(Decimal(1)+Decimal(str(gap))/100),'provenance':{'synthetic':'upstream verified structural limits'}}
def relation(a=None,b=None,d=None,**kwargs):
 aa,bb=groups()
 return review_negative_relation(a or aa,b or bb,context(),d or diagram((-60,10,-60)),api,
  support_pair=kwargs.pop('support_pair',supports()),evidence=kwargs.pop('evidence',evidence()),**kwargs)
def mass(gap=50,overlap=0,a=None,b=None,hanger=None,density=None):
 aa,bb=groups()
 return compare_detailing_mass(a or aa,b or bb,api,required_geometry=required(gap),physical_overlap_cm=overlap,
  hanger=hanger,diagram=diagram((10,10,10)),stirrups=[{'x_start_common':0,'x_end_common':4,'diameter_mm':5,'provenance':{'synthetic':1}}],
  density=density or {'kg_m3':7850,'provenance':{'synthetic':'explicit test density, no production default'}})
def holder(length=100,count=2,phi=6.3):
 return {'mark':'H','bars':count,'diameter_mm':phi,'function':'stirrup_holder','function_provenance':{'synthetic':1},
  'x_start_common':1,'x_end_common':2,'length_cm':length,'minimum_length_cm':100,
  'quantity_length_provenance':{'synthetic':'caller supplied verified count and cut length'},'minimum_length_policy_provenance':{'synthetic':1}}
def layout():
 return {'provenance':{'synthetic':'individual documentary centers'},'layers':[{'layer':1,'bars':[
  {'id':'a1','mark':'A','diameter_mm':10,'x_cm':3.5},
  {'id':'b1','mark':'B','diameter_mm':10,'x_cm':4.5},
  {'id':'a2','mark':'A','diameter_mm':10,'x_cm':10}]}]}
def spacing(**kwargs):
 return local_overlap_disposition(context()['section'],[bar('A',count=2,phi=10),bar('B',count=1,phi=10)],
  relation_type=kwargs.pop('relation_type','DETAILING_OVERLAP'),layout=kwargs.pop('layout',layout()),direct_pairs=kwargs.pop('direct_pairs',[['a1','b1']]),**kwargs)

class RelationsTests(TestCase):
 def test_same_piece_continuous(self):
  a=bar('P',start=-.2,end=4.2);a.update(trajectory_id='piece',physical_layer_id=[2],continuity_documentation={'drawing':1})
  r=relation(a,a,diagram((-100,-80,-100)))
  self.assertEqual(r['relation_classification'],'CONTINUOUS_NEGATIVE_REINFORCEMENT');self.assertFalse(r['resistance_bonus'])
 def test_same_diameter_not_continuous(self):
  a,b=groups();b['diameter_mm']=16
  self.assertNotEqual(relation(a,b)['relation_classification'],'CONTINUOUS_NEGATIVE_REINFORCEMENT')
 def test_same_mark_identity_unproven(self):
  a,b=groups();b['mark']=a['mark'];self.assertEqual(relation(a,b)['relation_classification'],'INCONCLUSIVE')
 def test_continuity_preserves_regional_failure(self):
  a=bar('P',start=-.2,end=4.2);a.update(trajectory_id='p',physical_layer_id=[2],continuity_documentation={'drawing':1})
  r=relation(a,a,regional_checks=[{'passes':False}]);self.assertEqual(r['regional_checks'],[{'passes':False}])
 def test_no_intersection_only_classification(self):
  e=evidence();e.pop('role');e.pop('existing_tail_meeting_confirmed');self.assertEqual(relation(evidence=e)['relation_classification'],'INCONCLUSIVE')
 def test_missing_association(self):self.assertEqual(relation(evidence={})['relation_classification'],'INCONCLUSIVE')
 def test_nonconsecutive_supports(self):
  s=supports();s[1]['occurrence']=3;self.assertEqual(relation(support_pair=s)['relation_classification'],'INCONCLUSIVE')
 def test_existing_tail_meeting(self):self.assertEqual(relation()['relation_classification'],'DETAILING_OVERLAP')
 def test_required_limits_missing_economics_only(self):
  r=relation();self.assertEqual(r['overlap_flexural_capacity']['status'],'PASS');self.assertIsNone(r['economic_comparison']['applicable'])
 def test_gap_over_80_independent(self):self.assertEqual(relation(d=diagram((10,10,10)),required_geometry=required(81))['relation_classification'],'INDEPENDENT_REINFORCEMENTS')
 def test_extension_gap_plus_30(self):self.assertEqual(mass()['extension_alternative']['additional_length_per_bar_cm'],80)
 def test_overlap_deficit_only(self):self.assertEqual(mass(overlap=20)['extension_alternative']['additional_length_per_bar_cm'],10)
 def test_overlap_30_no_added(self):self.assertEqual(mass(overlap=30)['extension_mass']['mass_kg'],0)
 def test_overlap_over_30_no_added(self):self.assertEqual(mass(overlap=138)['extension_mass']['mass_kg'],0)
 def test_smaller_total_area(self):self.assertEqual(mass()['smaller_As_bar'],'A')
 def test_smaller_area_not_smallest_diameter(self):
  a,b=groups();a['bars']=6;b['bars']=1;self.assertEqual(mass(a=a,b=b)['smaller_As_bar'],'B')
 def test_extension_all_bars_mass(self):
  r=mass();self.assertEqual(r['extension_alternative']['number_of_bars'],3);self.assertAlmostEqual(r['extension_mass']['total_length_m'],2.4)
 def test_density_not_invented(self):
  r=mass(density={'kg_m3':7850});self.assertEqual(r['extension_mass']['status'],'INCONCLUSIVE')
 def test_holder_existing_diameter_rule(self):
  r=mass(hanger=holder(phi=5));self.assertIn('holder_existing_rule_not_satisfied',r['diagnostics'])
 def test_holder_count_length_not_invented(self):self.assertIn('holder_count_length_or_minimum_policy_unresolved',mass()['diagnostics'])
 def test_holder_minimum_length(self):self.assertEqual(mass(hanger=holder(length=90))['hanger_mass']['status'],'INCONCLUSIVE')
 def test_holder_mass_real_area(self):
  r=mass(hanger=holder());self.assertAlmostEqual(r['hanger_mass']['mass_kg'],steel_mass(api.Barra(6.3).area_cm2,2,density_kg_m3=7850,provenance={'test':1})['mass_kg'])
 def test_holder_lighter(self):self.assertEqual(mass(hanger=holder())['lower_steel_mass_alternative'],'USE_HANGER_REINFORCEMENT')
 def test_extension_lighter(self):self.assertEqual(mass(hanger=holder(length=10000))['lower_steel_mass_alternative'],'EXTEND_NEGATIVE_REINFORCEMENT')
 def test_equal_mass_no_tiebreak(self):
  self.assertEqual(mass(hanger=holder(length=80,count=3,phi=16))['hanger_mass']['status'],'INCONCLUSIVE')
  h=holder(length=80,count=3,phi=16);h['minimum_length_cm']=0;h['x_end_common']=1.8
  self.assertEqual(mass(hanger=h)['lower_steel_mass_alternative'],'EQUIVALENT_STEEL_WEIGHT')
 def test_equal_total_area_no_arbitrary_extension(self):
  a,b=groups();b.update(bars=3,diameter_mm=16);self.assertIn('equal_total_areas_no_extension_tiebreak',mass(a=a,b=b)['diagnostics'])
 def test_lap_transition(self):
  r=relation(d=diagram((-60,-20,-60)),evidence=evidence('resistant_transition'))
  self.assertEqual(r['relation_classification'],'REINFORCEMENT_LAP_TRANSITION')
  self.assertAlmostEqual(r['overlap_length_check']['required_cm'],2*basic_anchorage(16,context(),api,flexure_sign='NEGATIVE')['result']['lb_cm'])
 def test_no_silent_transition_role(self):self.assertEqual(relation(d=diagram((-60,-20,-60)))['relation_classification'],'INCONCLUSIVE')
 def test_lap_not_30(self):
  a,b=groups();a['x_end_common']=1.3
  r=relation(a,b,diagram((-60,-20,-60)),evidence=evidence('resistant_transition'))
  self.assertFalse(r['overlap_length_check']['passes']);self.assertGreater(r['overlap_length_check']['required_cm'],30)
 def test_lap_poor_no_hook_reduction(self):
  r=relation(d=diagram((-60,-20,-60)),evidence=evidence('resistant_transition'))
  self.assertEqual(r['lap_anchorage'],basic_anchorage(16,context(),api,flexure_sign='NEGATIVE'))
 def test_full_smallest_group_capacity(self):
  r=relation();c=r['overlap_flexural_capacity'];self.assertEqual(c['reference_bar'],'A');self.assertEqual(c['number_of_bars'],3)
  a,b=groups();p=prepare_reinforcement([a],context(),api,flexure_sign='NEGATIVE')
  self.assertEqual(c['Mk_equivalent_knm'],composition_capacity(p,2,context(),api,flexure_sign='NEGATIVE')['Mk_equivalent_knm'])
 def test_not_one_bar(self):
  a,b=groups();a['bars']=1;a['layers']=[1]
  self.assertGreater(relation()['overlap_flexural_capacity']['Mk_equivalent_knm'],relation(a,b)['overlap_flexural_capacity']['Mk_equivalent_knm'])
 def test_no_mixed_centroid(self):self.assertFalse(relation()['mixed_centroid_used'])
 def test_all_internal_vertices_demand(self):
  r=interval_demand(diagram((-10,-200,-20)),.5,3.5);self.assertEqual(r['max_negative_demand_knm'],200)
 def test_positive_not_absolute(self):self.assertEqual(interval_demand(diagram((100,200,100)),.1,3.9)['max_negative_demand_knm'],0)
 def test_gap_domain_inconclusive(self):self.assertIsNone(interval_demand(diagram((-10,None,-10)),.1,3.9)['passes'])
 def test_outside_domain_inconclusive(self):self.assertIsNone(interval_demand(diagram(),-1,3)['passes'])
 def test_overlap_outside_domain(self):
  a,b=groups();a['x_end_common']=5;b['x_end_common']=6
  self.assertEqual(relation(a,b)['overlap_flexural_capacity']['status'],'INCONCLUSIVE')
 def test_unknown_own_layer_not_fabricated(self):
  a,b=groups();a['layers']=[0,3]
  self.assertEqual(relation(a,b)['overlap_flexural_capacity']['status'],'INCONCLUSIVE')
 def test_mass_cannot_approve_resistant_failure(self):
  a,b=groups();a['bars']=1;a['layers']=[1]
  r=relation(a,b,diagram((-600,10,-600)),required_geometry={'required_end_bar_a_m':2,'required_start_bar_b_m':2,'provenance':{'test':1}},hanger=holder(),density={'kg_m3':7850,'provenance':{'test':1}})
  self.assertEqual(r['overlap_flexural_capacity']['status'],'FAIL');self.assertIsNone(r['selected_solution'])
 def test_local_pair_touching_allowed(self):self.assertTrue(spacing()['local_spacing_geometry']['passes'])
 def test_general_minimum_not_relaxed(self):
  r=spacing();self.assertFalse(r['global_disposition']['minimum_bar_spacing']['passes'])
  self.assertFalse(transverse_disposition(context()['section'],[bar('A',count=2,phi=10),bar('B',count=1,phi=10)],layout=layout())['minimum_bar_spacing']['passes'])
 def test_vibrator_corridor_elsewhere(self):self.assertTrue(spacing()['vibrator_access_spacing']['passes'])
 def test_no_pair_no_exception(self):self.assertFalse(spacing(direct_pairs=[])['local_spacing_geometry']['passes'])
 def test_overlapping_material_not_physical_fit(self):
  l=layout();l['layers'][0]['bars'][1]['x_cm']=4
  self.assertFalse(spacing(layout=l)['local_spacing_geometry']['passes'])
 def test_missing_centers_unknown(self):self.assertEqual(spacing(layout=None)['vibrator_access_spacing']['status'],'INCONCLUSIVE')
 def test_no_invented_centers(self):self.assertFalse(spacing(layout=None)['invented_positions'])
 def test_wrong_relation_no_local_exception(self):self.assertEqual(spacing(relation_type='SCALING')['local_spacing_geometry']['status'],'NOT_APPLICABLE')
 def test_invalid_pair_unknown(self):self.assertEqual(spacing(direct_pairs=[['a1','missing']])['local_spacing_geometry']['status'],'INCONCLUSIVE')
 def test_automatic_role_from_signed_moment_and_support_association(self):
  e=evidence();e.pop('role')
  self.assertEqual(relation(evidence=e)['relation_classification'],'DETAILING_OVERLAP')
  self.assertEqual(relation(d=diagram((-60,-20,-60)),evidence=e)['relation_classification'],'REINFORCEMENT_LAP_TRANSITION')
 def test_required_gap_with_negative_demand_is_not_free(self):
  self.assertEqual(relation(required_geometry=required(50))['relation_classification'],'INCONCLUSIVE')
 def test_support_role_requires_actual_reinforcement_at_face(self):
  a,b=groups();a['x_start_common']=1
  self.assertEqual(relation(a,b)['relation_classification'],'INCONCLUSIVE')
 def test_equal_diameter_capacity_tie_not_arbitrary(self):
  a,b=groups();b['diameter_mm']=16
  self.assertEqual(relation(a,b)['overlap_flexural_capacity']['status'],'INCONCLUSIVE')
 def test_short_length_can_have_sufficient_capacity(self):
  a,b=groups();a['x_end_common']=1.2
  r=relation(a,b);self.assertEqual(r['overlap_length_check']['status'],'FAIL');self.assertEqual(r['overlap_flexural_capacity']['status'],'PASS')
 def test_mass_density_required(self):
  with self.assertRaises(ValueError):steel_mass(1,2,density_kg_m3=0,provenance={'test':1})
 def test_local_exception_does_not_exempt_other_gaps(self):
  l=layout();l['layers'][0]['bars'][2]['x_cm']=6
  self.assertFalse(spacing(layout=l)['local_spacing_geometry']['passes'])
 def test_no_selected_or_optimization(self):
  r=relation();self.assertIsNone(r['selected_solution']);self.assertIsNone(r['detailing_optimization']);self.assertFalse(r['ready_for_detailing'])

def gap_test(value,applicable):
 def test(self):
  r=mass(gap=value);self.assertIs(r['applicable'],applicable);self.assertEqual(r['required_overlap_cm'],30)
 return test
for value,app in [(0,True),(30,True),(79.9,True),(80,True),(80.1,False)]:
 setattr(RelationsTests,'test_gap_'+str(value).replace('.','_'),gap_test(value,app))

def lap_equality(provided,passes):
 def test(self):
  a,b=groups();a['x_end_common']=1+provided/100
  anchor=basic_anchorage(16,context(),api,flexure_sign='NEGATIVE');anchor['result']['lb_cm']=50
  with patch('negative_reinforcement_relations.basic_anchorage',return_value=anchor):
   r=relation(a,b,diagram((-60,-20,-60)),evidence=evidence('resistant_transition'))
  self.assertIs(r['overlap_length_check']['passes'],passes)
 return test
for value,passes in [(100,True),(99,False),(101,True)]:setattr(RelationsTests,'test_lap_length_'+str(value),lap_equality(value,passes))

class RelationsGoldenTests(TestCase):
 @classmethod
 def setUpClass(cls):
  cls.cases={beam:json.loads((ROOT/'analises/pranchas'/ (beam+'_negative_reinforcement_review.json')).read_text(encoding='utf8')) for beam in ('V516','V517')}
 def test_real_overlap(self):
  for c in self.cases.values():
   r=c['negative_support_relations'][0];self.assertEqual(r['relation_classification'],'DETAILING_OVERLAP')
   self.assertEqual(r['physical_overlap']['length_cm'],138);self.assertEqual(r['physical_overlap']['start_m'],3.635)
   self.assertEqual(r['overlap_flexural_capacity']['reference_bar'],'N4');self.assertEqual(r['overlap_flexural_capacity']['number_of_bars'],3)
   self.assertEqual(r['overlap_length_check']['status'],'PASS');self.assertEqual(r['overlap_flexural_capacity']['status'],'PASS')
 def test_real_continuity(self):
  for c in self.cases.values():self.assertEqual(c['negative_support_relations'][1]['relation_classification'],'CONTINUOUS_NEGATIVE_REINFORCEMENT')
 def test_real_regional_failure_preserved(self):
  for c in self.cases.values():self.assertTrue(c['known_regional_flexure_failure']);self.assertTrue(any(r['result']['passes'] is False for r in c['regions']))
 def test_real_n8_left_preserved(self):
  for c in self.cases.values():self.assertFalse(next(e for e in c['events'] if e['mark']=='N8' and e['cut_side']=='LEFT')['result']['checks']['al_plus_lb']['passes'])
 def test_real_n8_n9_right_preserved(self):
  for c in self.cases.values():
   for mark in ('N8','N9'):
    r=next(e for e in c['events'] if e['mark']==mark and e['cut_side']=='RIGHT')['result']
    self.assertTrue(r['checks']['basic_lb_beyond_support']['passes']);self.assertEqual(r['checks']['basic_lb_beyond_support']['available_length_cm'],113)
 def test_real_end_bends_preserved(self):
  for c in self.cases.values():
   for n in c['end_nodes']:self.assertEqual(n['verification']['checks']['vertical_bend_geometry']['status'],'FAIL')
 def test_old_event_interpretations_explicit(self):
  for c in self.cases.values():
   r=c['event_interpretations'];self.assertEqual([x['status'] for x in r],['SUPERSEDED']*3);self.assertEqual(r[0]['current_verification']['classification'],'ANCHORAGE_BEYOND_INTERMEDIATE_SUPPORT');self.assertTrue(r[0]['current_verification']['passes'])
 def test_real_n3_not_scaling_and_no_al(self):
  for c in self.cases.values():
   r=next(e for e in c['events'] if e['mark']=='N3' and e['cut_side']=='RIGHT')['current_verification']
   self.assertTrue(r['required_in_previous_span']);self.assertFalse(r['required_in_adjacent_span'])
   self.assertEqual(set(r['checks']),{'basic_lb_beyond_support'});self.assertNotIn('al_result',r)
   self.assertEqual({b['mark'] for b in r['documentary_composition_at_end']},{'N3','N4','N7'})
   self.assertEqual({b['mark'] for b in r['proof_subset_after_cut']},{'N4'})
   self.assertAlmostEqual(r['checks']['basic_lb_beyond_support']['available_length_cm'],148)
 def test_real_mass_and_distribution_unknown(self):
  for c in self.cases.values():
   r=c['negative_support_relations'][0];self.assertIsNone(r['economic_comparison']['applicable']);self.assertEqual(r['local_spacing_geometry']['status'],'INCONCLUSIVE')
