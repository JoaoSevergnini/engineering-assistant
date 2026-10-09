"""Regression of documentary function and independently proven physical coverage."""
from unittest import TestCase
from copy import deepcopy
import json,hashlib
from pathlib import Path
from test_shear_review import context,API,series,region,diagram
from shear_review import review_shear_spans,check_drawn_region
from shear_coverage import classify_piece,physical_coverage,SLAB

ROOT=Path(__file__).resolve().parents[2]
def column(axis,width):
 return {'type':'COLUMN','type_source':'synthetic physical column drawing','source':'synthetic measured geometry','axis_m':axis,'width_m':width,'left_face_m':axis-width/2,'right_face_m':axis+width/2}
def span(pieces=None,left=None,right=None):
 return {'span_id':1,'series':[series((50,0,-50))],'reference_legs':2,'drawn_regions':pieces if pieces is not None else [region(interval=(.2,3.7))], 'support_geometry':{'left':left or column(0,.4),'right':right or column(4,.6)}}
def slab(mark='X'):
 return region(phi=8,spacing=20,legs=None,mark=mark,physical_function=SLAB,
  classification_evidence={'geometry':'asymmetric arms, continuity across adjacent slab level change','function_confirmation':{'engineer':'confirmed negative slab reinforcement'}})
def run(s):return review_shear_spans([s],context(),API)
def coverage(s):return physical_coverage(s,[0,4],s['drawn_regions'])
def real(beam):return json.loads((ROOT/f'analises/pranchas/{beam}_shear_reinforcement_review.json').read_text(encoding='utf8'))

class FunctionTests(TestCase):
 def test_adjacent_negative_classified(self):self.assertEqual(classify_piece(slab('N12'))['classification'],SLAB)
 def test_mark_not_determinant(self):self.assertEqual(classify_piece(slab('OTHER'))['classification'],SLAB)
 def test_n12_can_be_real_stirrup(self):self.assertTrue(classify_piece(region(mark='N12'))['contributes_to_beam_shear'])
 def test_excluded_no_area(self):self.assertNotIn('provided',check_drawn_region(diagram(),context(),API,slab()))
 def test_excluded_no_unknown_leg_control(self):self.assertEqual(check_drawn_region(diagram(),context(),API,slab())['checks'],{})
 def test_excluded_not_dimensioned(self):self.assertNotIn('design',check_drawn_region(diagram(),context(),API,slab()))
 def test_preserve_identity_geometry(self):
  p=slab();out=run(span([p]));self.assertEqual(out['excluded_reinforcement'][0]['piece'],p)
 def test_missing_confirmation_ambiguous(self):
  p=slab();p['classification_evidence'].pop('function_confirmation');self.assertEqual(classify_piece(p)['status'],'INCONCLUSIVE')
 def test_null_classification_evidence_is_inconclusive(self):
  p=slab();p['classification_evidence']=None;self.assertEqual(classify_piece(p)['status'],'INCONCLUSIVE')
 def test_phi_spacing_not_sufficient(self):self.assertEqual(classify_piece(region(phi=8,spacing=20,legs=None))['status'],'INCONCLUSIVE')
 def test_slab_not_coverage(self):self.assertEqual(run(span([slab()]))['coverage_reviews'][0]['uncovered_required_intervals_m'],[[.2,3.7]])
 def test_slab_does_not_mask_missing_beam_stirrups(self):self.assertIsNone(run(span([slab()]))['global_shear_approval'])

class PhysicalCoverageTests(TestCase):
 def test_domain_between_faces(self):self.assertEqual(coverage(span())['BEAM_STIRRUP_COVERAGE_DOMAIN'],[.2,3.7])
 def test_tqs_unchanged(self):self.assertEqual(coverage(span())['TQS_SHEAR_DOMAIN'],[0,4])
 def test_within_columns_not_applicable(self):
  c=coverage(span());self.assertEqual([i['status'] for i in c['intervals'] if i['classification']=='WITHIN_SUPPORT'],['NOT_APPLICABLE']*2)
 def test_uncovered_outside_column_pending(self):
  c=coverage(span([region(interval=(.3,3.7))]));self.assertEqual(c['uncovered_required_intervals_m'],[[.2,.3]])
 def test_widths_are_not_fixed_offsets(self):self.assertEqual(coverage(span(left=column(0,.8),right=column(4,.2)))['BEAM_STIRRUP_COVERAGE_DOMAIN'],[.4,3.9])
 def test_missing_geometry(self):
  s=span();s.pop('support_geometry');self.assertEqual(coverage(s)['intervals'][0]['classification'],'GEOMETRY_INCONCLUSIVE')
 def test_unproven_column_type(self):
  s=span();s['support_geometry']['left']['type']='INDIRECT';self.assertEqual(coverage(s)['status'],'INCONCLUSIVE')
 def test_inconsistent_faces(self):
  s=span();s['support_geometry']['left']['width_m']=99;self.assertEqual(coverage(s)['status'],'INCONCLUSIVE')
 def test_no_prolongation(self):
  s=span([region(interval=(1,3))]);before=deepcopy(s);coverage(s);self.assertEqual(s,before)
 def test_gap_between_faixas_pending(self):self.assertEqual(coverage(span([region(interval=(.2,2)),region(interval=(2.2,3.7))]))['uncovered_required_intervals_m'],[[2,2.2]])
 def test_cover_inside_support_not_needed_for_pass(self):self.assertTrue(run(span())['global_shear_approval'])
 def test_unknown_geometry_not_approved(self):
  s=span();s.pop('support_geometry');self.assertIsNone(run(s)['global_shear_approval'])
 def test_physical_beyond_tqs_no_extrapolation(self):
  s=span([region(interval=(-.2,3.7))],left=column(-.4,.4));r=run(s);self.assertIsNone(r['global_shear_approval']);self.assertFalse(r['shear_drawn_regions'][0]['demand']['complete'])
 def test_false_failure_precedes_unknown_coverage(self):self.assertFalse(run(span([region(spacing=30,interval=(1,3))]))['global_shear_approval'])

class RealCoverageTests(TestCase):
 def test_both_extreme_spans_uncovered(self):
  for b in ('V516','V517'):
   r=real(b);self.assertEqual([c['uncovered_required_intervals_m'] for c in r['coverage_reviews']],[[[.12,1.97]],[],[],[[11.71,13.56]]])
 def test_all_eight_old_intervals_proven_inside_columns(self):
  for b in ('V516','V517'):
   r=real(b);inside=[i['interval_m'] for c in r['coverage_reviews'] for i in c['intervals'] if i['classification']=='WITHIN_SUPPORT'];self.assertEqual(inside,[[0,.12],[1.97,2.08],[2.08,2.19],[6.51,6.62],[6.62,6.73],[10.29,10.446],[11.554,11.71],[13.56,13.68]])
 def test_p1_faces_distinct_from_depev_sampling(self):
  c=real('V516')['coverage_reviews'][3];self.assertEqual(c['support_geometry']['left']['depev_m'],.554);self.assertEqual(c['BEAM_STIRRUP_COVERAGE_DOMAIN'][0],11.71);self.assertEqual(c['TQS_SHEAR_DOMAIN'][0],11.554)
 def test_n12_separate_no_shear_regions(self):
  for b in ('V516','V517'):
   r=real(b);self.assertEqual(len(r['excluded_reinforcement']),2);self.assertEqual(len(r['shear_drawn_regions']),4);self.assertFalse(any(x['region']['mark']=='N12' for x in r['shear_drawn_regions']))
 def test_conventional_numeric_regression(self):
  snapshots=json.loads((ROOT/'analises/pranchas/V516_V517_shear_review_regression.json').read_text(encoding='utf8'))['cases']
  for b in ('V516','V517'):
   values=[{k:x[k] for k in ('demand','design','provided','checks','transition','inverse_capacity') if k in x} for x in real(b)['shear_drawn_regions']]
   digest=hashlib.sha256(json.dumps(values,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
   self.assertEqual(snapshots[b]['conventional_controls_sha256'],digest)
 def test_reference_tqs_unchanged(self):
  snapshots=json.loads((ROOT/'analises/pranchas/V516_V517_shear_review_regression.json').read_text(encoding='utf8'))['cases']
  for b in ('V516','V517'):
   digest=hashlib.sha256(json.dumps(real(b)['shear_reference_design'],sort_keys=True,ensure_ascii=False).encode()).hexdigest()
   self.assertEqual(snapshots[b]['reference_sha256'],digest)
 def test_independent_forces(self):self.assertNotEqual(real('V516')['shear_drawn_regions'][0]['demand']['Vsk_abs_kn'],real('V517')['shear_drawn_regions'][0]['demand']['Vsk_abs_kn'])
 def test_global_null_due_to_required_coverage_only(self):
  for b in ('V516','V517'):
   r=real(b);self.assertIsNone(r['global_shear_approval']);self.assertEqual(len(r['inconclusive_items']),2);self.assertFalse(r['structural_failures'])
 def test_selected_solution_null_suspension_not_evaluated(self):
  r=real('V516');self.assertIsNone(r['selected_solution']);self.assertIsNone(r['detailing_optimization']);self.assertTrue(r['suspension_not_evaluated'])

