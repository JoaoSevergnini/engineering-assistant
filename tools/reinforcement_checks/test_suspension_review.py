"""Suspension contracts/orchestration; shear equations remain in Concretopy."""
from unittest import TestCase
from copy import deepcopy
from dataclasses import replace
from types import SimpleNamespace
from pathlib import Path
import json,hashlib
from test_shear_review import context,API,series,region
from shear_review import review_shear_spans,design_shear
from suspension_review import review_suspension,review_connection,distribution,reaction_area,connections_from_mapping
from shear_coverage import SLAB

ROOT=Path(__file__).resolve().parents[2]
def connection(value=100,nature='CHARACTERISTIC',**changes):
 c={'id':'J','type':'BEAM_ON_BEAM','receiving_beam_id':'SUPPORT','supported_beam_id':'SUPPORTED',
  'transfer_confirmed':True,'transfer_source':{'synthetic':'supported beam support reaction explicitly to SUPPORT'},
  'suspension_applicable':True,'applicability_source':{'engineer':'synthetic internal indirect support'},
  'supported_geometry':{'height_cm':40,'width_cm':15,'source':'synthetic structural geometry'},
  'placement':'INTERIOR','projected_axis_m':2,'axis_source':{'mapping':'supported axis projection on receiving beam axis'},
  'reaction':{'value':value,'unit':'kN','nature':nature,'is_total':True,'total_source':'synthetic all-actions support envelope',
   'combination':'synthetic C1','source':'synthetic support reaction record','downward_sign':1,'supported_beam_id':'SUPPORTED','receiving_beam_id':'SUPPORT'}}
 c.update(changes);return c

def spans(pieces=None,values=(100,100,100)):
 return [{'span_id':1,'series':[series(values)],'reference_legs':2,'drawn_regions':pieces if pieces is not None else [region(phi=8,spacing=12)],
  'support_geometry':{'left':{'type':'COLUMN','type_source':'fixture','source':'fixture','axis_m':-.1,'width_m':.2,'left_face_m':-.2,'right_face_m':0},
   'right':{'type':'COLUMN','type_source':'fixture','source':'fixture','axis_m':4.1,'width_m':.2,'left_face_m':4,'right_face_m':4.2}}}]

def run(c=None,s=None,ctx=None,api=API):return review_suspension([c or connection()],receiving_beam='SUPPORT',spans=s or spans(),context=ctx or context(),api=api,inventory_complete=True,inventory_source='synthetic structural inventory')
def item(r):return r['connections'][0]
def segment(r):return item(r)['subintervals'][0]

class ReactionTests(TestCase):
 def test_characteristic_majoration(self):
  r=item(run())['suspension'];self.assertEqual(r['total_design_kn'],140);self.assertEqual(r['considered_design_kn'],105)
 def test_design_no_double_factor(self):
  a=item(run())['suspension'];b=item(run(connection(140,'DESIGN')))['suspension'];self.assertAlmostEqual(a['as_suspension_cm2'],b['as_suspension_cm2']);self.assertEqual(b['gamma_f_applied'],1)
 def test_units_area_and_rate(self):
  r=item(run());self.assertAlmostEqual(r['suspension']['as_suspension_cm2'],2.415);self.assertAlmostEqual(r['asw_per_s_suspension'],2.415/52*100)
 def test_steel_fyd_is_public_api(self):self.assertAlmostEqual(item(run())['suspension']['fyd_mpa'],API.Aco(500).fyd(1.15))
 def test_original_reaction_provenance(self):
  c=connection();self.assertEqual(item(run(c))['suspension']['reaction'],c['reaction'])
 def test_missing_reaction(self):self.assertEqual(run(connection(reaction=None))['overall_result'],'INCONCLUSIVE')
 def test_partial_reaction(self):
  c=connection();c['reaction']['is_total']=False;self.assertIsNone(item(run(c))['suspension']['as_suspension_cm2'])
 def test_total_without_evidence(self):
  c=connection();c['reaction'].pop('total_source');self.assertEqual(run(c)['overall_result'],'INCONCLUSIVE')
 def test_missing_combination(self):
  c=connection();c['reaction']['combination']=None;self.assertEqual(run(c)['overall_result'],'INCONCLUSIVE')
 def test_unknown_nature(self):
  c=connection();c['reaction']['nature']='UNKNOWN';self.assertEqual(run(c)['overall_result'],'INCONCLUSIVE')
 def test_wrong_unit_no_silent_conversion(self):
  c=connection();c['reaction']['unit']='tf';self.assertEqual(run(c)['overall_result'],'INCONCLUSIVE')
 def test_signed_downward_reaction(self):
  c=connection(-100);c['reaction']['downward_sign']=-1;self.assertAlmostEqual(item(run(c))['suspension']['as_suspension_cm2'],2.415)
 def test_uplift_not_absolute(self):self.assertEqual(run(connection(-100))['overall_result'],'INCONCLUSIVE')
 def test_reaction_receiver_mismatch(self):
  c=connection();c['reaction']['receiving_beam_id']='OTHER';self.assertEqual(run(c)['overall_result'],'INCONCLUSIVE')
 def test_nonfinite_reaction(self):self.assertEqual(run(connection(float('nan')))['overall_result'],'INCONCLUSIVE')
 def test_unconfirmed_transfer(self):self.assertEqual(run(connection(transfer_confirmed=False))['overall_result'],'INCONCLUSIVE')
 def test_not_every_intersection_is_indirect(self):self.assertEqual(run(connection(type='INTERSECTION'))['overall_result'],'INCONCLUSIVE')
 def test_applicability_unproven(self):self.assertEqual(run(connection(suspension_applicable=None))['overall_result'],'INCONCLUSIVE')
 def test_supported_geometry_missing(self):self.assertEqual(run(connection(supported_geometry={}))['overall_result'],'INCONCLUSIVE')

class GeometryTests(TestCase):
 def test_length_receiving_height(self):self.assertEqual(item(run())['distribution']['length_cm'],52)
 def test_symmetric_about_projected_axis(self):self.assertEqual(item(run())['distribution']['interval_m'],[1.74,2.26])
 def test_not_supported_height(self):
  c=connection();c['supported_geometry']['height_cm']=100;self.assertEqual(item(run(c))['distribution']['length_cm'],52)
 def test_axis_source_needed(self):self.assertEqual(run(connection(axis_source=None))['overall_result'],'INCONCLUSIVE')
 def test_cantilever_origin_unknown(self):
  r=item(run(connection(placement='CANTILEVER_END')));self.assertEqual(r['distribution']['length_cm'],26);self.assertIsNone(r['distribution']['interval_m'])
 def test_explicit_cantilever_interval(self):
  c=connection(placement='CANTILEVER_END',explicit_interval_m=[2,2.26],explicit_interval_source={'engineer':'explicit fixture'});self.assertEqual(item(run(c))['distribution']['interval_m'],[2,2.26])
 def test_cantilever_wrong_length(self):self.assertEqual(run(connection(placement='CANTILEVER_END',explicit_interval_m=[1,2],explicit_interval_source='fixture'))['overall_result'],'INCONCLUSIVE')
 def test_cross_support_no_truncation(self):
  r=item(run(connection(projected_axis_m=0)));self.assertEqual(r['distribution']['interval_m'],[-.26,.26]);self.assertEqual(r['checks']['geometric_position']['status'],'INCONCLUSIVE')
 def test_cross_section_change(self):
  s=spans();s[0]['section_changes_m']=[2];self.assertEqual(item(run(s=s))['checks']['geometric_position']['status'],'INCONCLUSIVE')
 def test_section_change_does_not_invent_uniform_resistant_context(self):
  s=spans();s[0]['section_changes_m']=[2];r=item(run(s=s));self.assertNotIn('regional_shear_design',r);self.assertIn('shear_demand',r)
 def test_missing_physical_geometry(self):
  s=spans();s[0].pop('support_geometry');self.assertEqual(run(s=s)['overall_result'],'INCONCLUSIVE')
 def test_no_extrapolation(self):
  r=item(run(connection(projected_axis_m=0)));self.assertFalse(r['shear_demand']['complete']);self.assertEqual(r['checks']['shear_diagram_coverage']['status'],'INCONCLUSIVE')
 def test_gap_not_interpolated(self):self.assertEqual(run(s=spans(values=(100,None,100)))['overall_result'],'INCONCLUSIVE')
 def test_internal_vertex_governs(self):self.assertEqual(item(run(s=spans(values=(50,-200,50))))['shear_demand']['Vsk_abs_kn'],200)
 def test_interpolated_endpoint(self):self.assertEqual(item(run(s=spans(values=(0,100,0))))['shear_demand']['Vsk_abs_kn'],100)
 def test_independent_series_signed_maximum(self):
  s=spans();s[0]['series'].append(series((-150,-150,-150),identity='min'));r=item(run(s=s));self.assertEqual(r['shear_demand']['governing'][0]['Vsk_original_kn'],-150)

class CombinationTests(TestCase):
 def test_calculated_before_minimum(self):
  r=segment(run());self.assertLess(r['asw_per_s_shear_calculated'],r['asw_per_s_shear_minimum']);self.assertGreater(r['asw_per_s_shear_calculated'],0)
 def test_combine_raw_not_governing(self):
  r=segment(run());self.assertAlmostEqual(r['asw_per_s_total_required'],r['asw_per_s_suspension']+r['asw_per_s_shear_calculated']);self.assertLess(r['asw_per_s_total_required'],r['asw_per_s_suspension']+r['asw_per_s_shear_minimum'])
 def test_minimum_can_govern(self):
  r=segment(run(connection(1)));self.assertEqual(r['asw_per_s_total_required'],r['asw_per_s_shear_minimum'])
 def test_zero_shear_not_negative(self):
  r=segment(run(s=spans(values=(0,0,0))));self.assertEqual(r['asw_per_s_shear_calculated'],0);self.assertEqual(r['asw_per_s_total_required'],r['asw_per_s_suspension'])
 def test_legacy_api_components_unknown(self):
  original=API.dimensionar_cortante_viga
  def legacy(*a,**k):return replace(original(*a,**k),asw_por_s_calculado=None,asw_por_s_minimo=None)
  api=SimpleNamespace(**vars(API));api.dimensionar_cortante_viga=legacy
  self.assertEqual(run(api=api)['overall_result'],'INCONCLUSIVE')
 def test_known_failure_with_missing_reaction_not_hidden(self):
  r=run(connection(reaction=None),spans([region(phi=5,spacing=30)],values=(200,200,200)));self.assertEqual(r['overall_result'],'FAIL')
 def test_known_area_failure_missing_reaction_code_spacing_passes(self):
  r=run(connection(reaction=None),spans([region(phi=5,spacing=20)],values=(200,200,200)));self.assertEqual(segment(r)['checks']['maximum_code_spacing']['status'],'PASS');self.assertEqual(r['overall_result'],'FAIL')
 def test_known_fail_partial_domain_not_hidden(self):
  r=run(connection(projected_axis_m=0),spans([region(phi=5,spacing=30)],values=(200,200,200)));self.assertEqual(r['overall_result'],'FAIL')
 def test_diagonal_failure_without_documented_stirrups(self):
  self.assertEqual(run(s=spans([],values=(1000,1000,1000)))['overall_result'],'FAIL')
 def test_diagonal_failure_not_hidden(self):self.assertEqual(run(s=spans(values=(1000,1000,1000)))['overall_result'],'FAIL')
 def test_complete_single_region_pass(self):self.assertTrue(run()['suspension_passes'])
 def test_combined_failure_independent_shear_pass(self):
  s=spans([region(phi=5,spacing=14)]);r=run(s=s);self.assertEqual(segment(r)['independent_shear_check']['overall_structural_result'],'PASS');self.assertEqual(r['overall_result'],'FAIL')

class DrawnRegionTests(TestCase):
 def test_multiple_regions_each_checked(self):
  r=run(s=spans([region(phi=8,spacing=12,interval=(0,2)),region(phi=8,spacing=14,interval=(2,4))]));self.assertEqual(len(item(r)['subintervals']),2)
 def test_no_averaging_failure(self):
  r=run(s=spans([region(phi=8,spacing=8,interval=(0,2)),region(phi=5,spacing=14,interval=(2,4))]));self.assertEqual(r['overall_result'],'FAIL');self.assertEqual([i['overall_result'] for i in item(r)['subintervals']],['PASS','FAIL'])
 def test_unknown_legs(self):self.assertEqual(run(s=spans([region(legs=None)]))['overall_result'],'INCONCLUSIVE')
 def test_slab_not_credited(self):
  p=region(phi=8,spacing=20,legs=None,physical_function=SLAB,classification_evidence={'geometry':'slab continuity','function_confirmation':'engineer'});r=item(run(s=spans([p])));self.assertEqual(len(r['excluded_reinforcement']),1);self.assertNotIn('provided',r['subintervals'][0])
 def test_normative_spacing_separate(self):self.assertEqual(segment(run(s=spans([region(phi=8,spacing=40)])))['checks']['maximum_code_spacing']['status'],'FAIL')
 def test_less_than_eight_review_not_structural_fail(self):
  r=run(s=spans([region(phi=8,spacing=7)]));self.assertEqual(r['overall_result'],'REQUIRES_ENGINEERING_REVIEW');self.assertTrue(r['suspension_passes'])
 def test_special_diameter_review(self):self.assertEqual(run(s=spans([region(phi=10,spacing=8)]))['overall_result'],'REQUIRES_ENGINEERING_REVIEW')
 def test_wide_four_legs_holder_unknown(self):
  c=context();c['section']['bw']=45;r=run(s=spans([region(phi=8,spacing=8,legs=4)]),ctx=c);self.assertEqual(r['overall_result'],'INCONCLUSIVE')
 def test_wide_four_legs_confirmed_holder(self):
  c=context();c['section']['bw']=45;r=run(s=spans([region(phi=8,spacing=8,legs=4,holder_compatibility={'passes':True,'provenance':'fixture holder disposition'})]),ctx=c);self.assertTrue(r['suspension_passes'])
 def test_drawing_gap(self):self.assertEqual(run(s=spans([region(phi=8,spacing=12,interval=(0,1.9)),region(phi=8,spacing=12,interval=(2.1,4))]))['overall_result'],'INCONCLUSIVE')
 def test_fields_rate_area_not_conflated(self):
  r=item(run());self.assertNotEqual(r['suspension']['as_suspension_cm2'],r['asw_per_s_suspension'])

class IntegrationTests(TestCase):
 def test_overlapping_suspension_unknown(self):
  c,d=connection(),connection(id='K',projected_axis_m=2.1);r=review_suspension([c,d],receiving_beam='SUPPORT',spans=spans(),context=context(),api=API,inventory_complete=True,inventory_source='fixture');self.assertEqual(r['overall_result'],'INCONCLUSIVE')
 def test_overlap_preserves_proven_failure(self):
  c,d=connection(),connection(id='K');r=review_suspension([c,d],receiving_beam='SUPPORT',spans=spans([region(phi=5,spacing=14)]),context=context(),api=API,inventory_complete=True,inventory_source='fixture');self.assertEqual(r['overall_result'],'FAIL')
 def test_touching_regions_not_overlap(self):
  c,d=connection(projected_axis_m=1.74),connection(id='K',projected_axis_m=2.26);r=review_suspension([c,d],receiving_beam='SUPPORT',spans=spans(),context=context(),api=API,inventory_complete=True,inventory_source='fixture');self.assertEqual(r['overall_result'],'PASS')
 def test_input_shear_not_mutated(self):
  s=spans();c=context();before=deepcopy((s,c));run(s=s,ctx=c);self.assertEqual((s,c),before)
 def test_independent_shear_unchanged_by_suspension(self):
  s=spans();before=review_shear_spans(s,context(),API);run(s=s);after=review_shear_spans(s,context(),API);self.assertEqual(before,after)
 def test_no_connections_without_inventory_not_approved(self):self.assertIsNone(review_suspension([],receiving_beam='SUPPORT',spans=spans(),context=context(),api=API)['suspension_passes'])
 def test_confirmed_empty_inventory_not_applicable(self):self.assertEqual(review_suspension([],receiving_beam='SUPPORT',spans=spans(),context=context(),api=API,inventory_complete=True,inventory_source='fixture')['overall_result'],'NOT_APPLICABLE')
 def test_mapping_candidates_do_not_invent_reaction(self):
  r=connections_from_mapping({'indirect_relations':[{'supported_beam':'A','receiving_beam':'B','reaction':{'max':10,'min':-1},'source_records':{'line':'TQS'}}]});self.assertIsNone(r[0]['projected_axis_m']);self.assertNotIn('reaction',r[0]);self.assertTrue(r[0]['transfer_confirmed'])
 def test_solution_null(self):r=run();self.assertIsNone(r['selected_solution']);self.assertIsNone(r['detailing_optimization'])
 def test_v516_v517_old_shear_preserved(self):
  baseline=json.loads((ROOT/'analises/pranchas/suspension_review_preservation.json').read_text(encoding='utf8'))['files']
  for b in ('V516','V517'):
   for kind in ('shear','negative'):
    p=ROOT/f'analises/pranchas/{b}_{kind}_reinforcement_review.json';self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),baseline[p.relative_to(ROOT).as_posix()])
