import unittest
from copy import deepcopy
from input_evidence import fact, resolve
from documentary_reconciliation import reconcile
from physical_geometry import extend, classify_span, at_x, project_occurrences, project_segments
from consolidar_detalhamento import transform, validate
from stage1_test_fixtures import proved, extension, model, document
from pdf_observations import parse_label

class EvidenceTests(unittest.TestCase):
    def test_proof_requires_source(self):
        with self.assertRaises(ValueError):fact(1,state='DOCUMENTED_CONFIRMED')
    def test_convention_requires_rule(self):
        with self.assertRaises(ValueError):fact(1,state='INFERRED_EXPLICIT_CONVENTION',provenance=['x'])
    def test_normative_text_consulted(self):
        with self.assertRaises(ValueError):fact(1,state='ENGINEERING_ASSUMPTION',criterion=dict(origin='NORMATIVE',reference='fake'))
    def test_conflict_not_priority(self):self.assertEqual(resolve([proved(19,'cm'),proved(20,'cm')],unit='cm')['state'],'CONFLICTING')
    def test_dimension_beats_estimate(self):
        a=fact(20,state='ENGINEERING_ASSUMPTION',unit='cm',provenance=['graphical'])
        self.assertEqual(resolve([a,proved(19,'cm')],unit='cm')['value'],19)
    def test_unit_required(self):
        with self.assertRaises(ValueError):resolve([proved(19)],unit='cm')
    def test_no_nan(self):
        with self.assertRaises(ValueError):fact(float('nan'),state='ENGINEERING_ASSUMPTION')

class DocumentaryTests(unittest.TestCase):
    def obs(self,view,id,**kw):return dict(mark='N1',view=view,representation_id=id,provenance=[{'file':'synthetic.pdf'}],**kw)
    def complete(self):return [dict(view=v,extraction='COMPLETE',integrity='INTACT') for v in ('ELEVATION','SECTION','STEEL_SCHEDULE')]
    def result(self,obs,cov=None):return reconcile(obs,cov or self.complete())['positions'][0]
    def test_complete(self):
        r=self.result([self.obs(v,str(i),diameter_mm=16) for i,v in enumerate(('ELEVATION','SECTION','STEEL_SCHEDULE'))]);self.assertEqual(r['state'],'RECONCILED')
    def test_incomplete_does_not_prove_absence(self):
        r=self.result([self.obs('STEEL_SCHEDULE','1',quantity=4,quantity_scope='POSITION_TOTAL')]);self.assertFalse(r['physical_absence_proved'])
    def test_missing_extraction(self):
        r=self.result([self.obs('STEEL_SCHEDULE','1')],[dict(view='ELEVATION',extraction='NOT_EXTRACTED',integrity='INTACT')]);self.assertIn('REPRESENTATION_NOT_EXTRACTED',[i['code'] for i in r['issues']])
    def test_v623_truncation_contract(self):
        r=self.result([self.obs('STEEL_SCHEDULE','1',quantity=4,diameter_mm=16,nominal_length_cm=464,quantity_scope='POSITION_TOTAL')],[dict(view='ELEVATION',integrity='TRUNCATED',extraction='PARTIAL',marks=['N1'],provenance=['user confirmation'])]);self.assertIn('PLOTTING_INTEGRITY',[i['code'] for i in r['issues']]);self.assertFalse(r['physical_absence_proved'])
    def test_field_divergences(self):
        for field,a,b in [('diameter_mm',16,20),('nominal_length_cm',464,456),('shape','STRAIGHT','BENT'),('quantity',4,2)]:
            r=self.result([self.obs('STEEL_SCHEDULE','1',quantity_scope='POSITION_TOTAL',**{field:a}),self.obs('ELEVATION','2',quantity_scope='POSITION_TOTAL',**{field:b})]);self.assertEqual(r['state'],'CONFLICTING')
    def test_different_quantity_scopes_not_conflict(self):
        r=self.result([self.obs('STEEL_SCHEDULE','1',quantity=4,quantity_scope='POSITION_TOTAL'),self.obs('ELEVATION','2',quantity=2,quantity_scope='OCCURRENCE',occurrence_id='left')]);self.assertNotEqual(r['state'],'CONFLICTING')
    def test_complete_occurrence_total(self):
        obs=[self.obs('STEEL_SCHEDULE','1',quantity=5,quantity_scope='POSITION_TOTAL')]+[self.obs('ELEVATION',i,quantity=2,quantity_scope='OCCURRENCE',occurrence_id=i,physical_inventory_complete=True) for i in ('left','right')]
        self.assertIn('PHYSICAL_TOTAL_DIVERGENCE',[i['code'] for i in self.result(obs)['issues']])
    def test_section_identity(self):
        r=self.result([self.obs('SECTION','1',quantity=4,quantity_scope='SECTION_COUNT',section_id='A'),self.obs('SECTION','2',quantity=2,quantity_scope='SECTION_COUNT',section_id='B')]);self.assertNotEqual(r['state'],'CONFLICTING')
    def test_stale_proof(self):
        r=self.result([self.obs('STEEL_SCHEDULE','1',revision_status='PROVEN_STALE')]);self.assertEqual(r['state'],'CONFLICTING')
    def test_date_alone_not_stale(self):
        r=self.result([self.obs('STEEL_SCHEDULE','1',date='old')]);self.assertNotEqual(r['state'],'CONFLICTING')
    def test_duplicate_representation(self):
        with self.assertRaises(ValueError):reconcile([self.obs('SECTION','1'),self.obs('SECTION','1')],[])
    def test_label_parser(self):
        self.assertEqual(parse_label('N2 4 Ø16 C=464')['nominal_length_cm'],464)
        self.assertEqual(parse_label('4 N2 Ø16 C=464')['quantity'],4)

class PhysicalTests(unittest.TestCase):
    def test_schema_replay(self):
        d=document();d['physical_extension']['observations']=[dict(mark='N1',representation_id='r1',view='ELEVATION',provenance=['synthetic'])]
        m=transform(d);self.assertEqual(m['schema_version'],'1.1');self.assertTrue(validate(m,d)['source_projection_checked'])
    def test_repeated_mark_distinct_occurrences(self):
        m=model();b=deepcopy(m['physical_geometry']['occurrences'][0]);b['occurrence_id']='O2';m['physical_geometry']['occurrences'].append(b)
        self.assertEqual(len(at_x(m,2)['present']),2);self.assertEqual(len({b['mark'] for b in project_occurrences(m)}),2)
    def test_nominal_length_not_coordinate(self):
        e=extension();e['occurrences'][0]['x_start_m']=fact(unit='m');e['occurrences'][0]['nominal_length_cm']=464
        m=extend(dict(longitudinal_reinforcement=[dict(mark='N1')],skin_reinforcement=[]),e);self.assertEqual(at_x(m,2)['indeterminate'][0]['mark'],'N1')
    def test_unknown_end_localized(self):
        m=model();m['physical_geometry']['occurrences'][0]['x_end_m']=fact(unit='m');self.assertEqual(len(at_x(m,-1)['absent']),1);self.assertFalse(at_x(m,2)['complete'])
    def test_graphical_endpoint_not_exclusion(self):
        m=model();m['physical_geometry']['occurrences'][0]['x_start_m']=fact(0,state='ENGINEERING_ASSUMPTION',unit='m');self.assertFalse(at_x(m,-1)['complete'])
    def test_layers_conflicting(self):
        e=extension();e['occurrences'][0]['layers']=proved([3]);m=extend(dict(longitudinal_reinforcement=[dict(mark='N1')],skin_reinforcement=[]),e);self.assertEqual(m['physical_geometry']['occurrences'][0]['layers']['state'],'CONFLICTING')
    def test_levels_inconsistent(self):
        e=extension();e['segments'][0]['geometry'].update(top_level_cm=proved(0,'cm'),bottom_level_cm=proved(-47,'cm'));m=extend(dict(longitudinal_reinforcement=[dict(mark='N1')],skin_reinforcement=[]),e);self.assertEqual(m['physical_geometry']['segments'][0]['geometry']['height_cm']['state'],'CONFLICTING')
    def test_no_average_variable_section(self):
        m=model();m['physical_geometry']['segments'][0]['geometry_type']='VARIABLE';r,p=project_segments(m);self.assertFalse(r);self.assertTrue(p)
    def test_B_needs_side_and_bounds(self):
        s=classify_span(dict(tqs_span_token='1B'));self.assertEqual(s['kind'],'CANTILEVER');self.assertEqual(s['physical_validation'],'PENDING')
    def test_B_conflict(self):
        s=classify_span(dict(tqs_span_token='1B',physical_kind=proved('BETWEEN_SUPPORTS')));self.assertTrue(s['conflicting'])
    def test_B_complete(self):
        s=classify_span(dict(tqs_span_token='1B',physical_kind=proved('CANTILEVER'),orientation=proved('LEFT'),physical_bounds=dict(x_start_m=proved(0,'m'),x_end_m=proved(1,'m'))));self.assertEqual(s['physical_validation'],'VALIDATED')
    def test_between_supports(self):self.assertEqual(classify_span(dict(tqs_span_token='1'))['kind'],'BETWEEN_SUPPORTS')
    def test_column_termination_not_cantilever(self):self.assertEqual(classify_span(dict(physical_kind=proved('COLUMN_TERMINATION')))['kind'],'COLUMN_TERMINATION')
    def test_inverted_interval(self):
        e=extension();e['segments'][0]['x_end_m']=proved(-1,'m')
        with self.assertRaises(ValueError):extend(dict(longitudinal_reinforcement=[],skin_reinforcement=[]),e)

if __name__=='__main__':unittest.main()
