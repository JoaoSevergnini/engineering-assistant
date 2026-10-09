import copy
import importlib.util
import json
from pathlib import Path
import unittest
from beam_diagnostic import consolidate,aggregate,markdown,DISCIPLINES

class BeamDiagnosticTests(unittest.TestCase):
    def setUp(self):
        self.ctx=dict(beam_id='V1',floor='F',coordinate_system={'origin':'left_support_axis','positive_direction':'left_to_right','unit':'m'})
        self.control=dict(check_id='a',check_type='anchorage_length',status='PASS',physical_interval=[1.,2.],
            span_id=1,drawing_reinforcement_ids=['N1'],required_value=30.,provided_value=40.,units='cm',
            comparison='provided_ge_required',reason='test criterion',criterion={'authority':'engineer'})
        self.modules=[dict(discipline=d,beam_id='V1',floor='F',coordinate_system=self.ctx['coordinate_system'],
            source=d+'.json',version='1',complete=True,checks=[copy.deepcopy(self.control)]) for d in DISCIPLINES]
    def result(self):return consolidate(self.ctx,self.modules)
    def test_all_pass(self):self.assertEqual(self.result()['overall_status'],'PASS')
    def test_isolated_fail(self):
        self.modules[2]['checks'][0]['status']='FAIL'
        self.assertEqual(len(self.result()['proven_nonconformities']),1)
    def test_multiple_failures(self):
        for m in self.modules[:2]:m['checks'][0]['status']='FAIL'
        self.assertEqual(len(self.result()['proven_nonconformities']),2)
    def test_fail_and_pending_retained(self):
        self.modules[0]['checks'][0]['status']='FAIL';self.modules[1]['checks'][0]['status']='INCONCLUSIVE'
        r=self.result();self.assertEqual(r['overall_status'],'FAIL');self.assertTrue(r['pending_occurrences'])
    def test_engineering_review(self):
        self.modules[0]['checks'][0]['status']='REQUIRES_ENGINEERING_REVIEW'
        r=self.result();self.assertEqual(r['overall_status'],'REQUIRES_ENGINEERING_REVIEW');self.assertFalse(r['proven_nonconformities'])
    def test_missing_module(self):
        self.modules.pop();self.assertEqual(self.result()['discipline_status']['suspension'],'INCONCLUSIVE')
    def test_explicit_inapplicability(self):
        self.modules[-1].update(applicability='NOT_APPLICABLE',applicability_evidence='proven no indirect supports',checks=[])
        self.assertEqual(self.result()['discipline_status']['suspension'],'NOT_APPLICABLE')
    def test_unproven_inapplicability_rejected(self):
        self.modules[-1].update(applicability='NOT_APPLICABLE',checks=[])
        with self.assertRaises(ValueError):self.result()
    def test_wrong_beam(self):
        self.modules[0]['beam_id']='V2'
        with self.assertRaises(ValueError):self.result()
    def test_wrong_floor(self):
        self.modules[0]['floor']='OTHER'
        with self.assertRaises(ValueError):self.result()
    def test_local_coordinate_rejected(self):
        self.modules[0]['coordinate_system']={'origin':'face','unit':'cm'}
        with self.assertRaises(ValueError):self.result()
    def test_check_coordinate_rejected(self):
        self.modules[0]['checks'][0]['coordinate_system']={'origin':'other'}
        with self.assertRaises(ValueError):self.result()
    def test_anchorage_bar_specific(self):
        c=self.modules[2]['checks'][0];c['status']='FAIL'
        o=next(x for x in self.result()['occurrences'] if x['status']=='FAIL')
        self.assertEqual(o['drawing_reinforcement_ids'],['N1']);self.assertEqual(o['category'],'INSUFFICIENT_ANCHORAGE')
    def test_longitudinal_area(self):
        self.modules[0]['checks'][0].update(status='FAIL',check_type='reinforcement_area',units='cm2')
        self.assertEqual(self.result()['occurrences'][0]['category'],'INSUFFICIENT_REINFORCEMENT_AREA')
    def test_stirrup_rate(self):
        self.modules[3]['checks'][0].update(status='FAIL',check_type='shear_reinforcement',units='cm2/m')
        self.assertEqual(self.result()['occurrences'][0]['category'],'INSUFFICIENT_STIRRUP_RATE')
    def test_spacing(self):
        self.modules[3]['checks'][0].update(status='FAIL',check_type='maximum_code_spacing',comparison='provided_le_required')
        self.assertEqual(self.result()['occurrences'][0]['category'],'EXCESSIVE_STIRRUP_SPACING')
    def test_suspension_pending(self):
        self.modules[4]['checks'][0]['status']='INCONCLUSIVE'
        self.assertEqual(self.result()['occurrences'][0]['category'],'UNVERIFIED_SUSPENSION')
    def test_same_region_not_merged(self):
        self.modules[2]['checks']=[dict(self.control,status='FAIL',check_id=str(i)) for i in range(3)]
        r=self.result();self.assertEqual(len(r['proven_nonconformities']),3);self.assertEqual(len(r['relations']),3)
    def test_related_not_single_correction(self):
        for m in self.modules[:2]:m['checks'][0]['status']='FAIL'
        self.assertFalse(self.result()['relations'][0]['single_correction_proven'])
    def test_close_disjoint_regions_not_related(self):
        self.modules[0]['checks'][0].update(status='FAIL',drawing_reinforcement_ids=['N1'])
        self.modules[1]['checks'][0].update(status='FAIL',physical_interval=[2.00001,3.],drawing_reinforcement_ids=['N2'])
        self.assertFalse(self.result()['relations'])
    def test_sources_preserved(self):
        self.modules[0]['checks'][0]['demand_source']={'file':'X','lines':[3,3]}
        self.assertTrue(any(c['demand_source']=={'file':'X','lines':[3,3]} for c in self.result()['checks']))
    def test_units_no_conversion(self):
        self.modules[0]['checks'][0]['units']='kN.cm'
        self.assertTrue(any(c['units']=='kN.cm' for c in self.result()['checks']))
    def test_serialization(self):json.dumps(self.result(),allow_nan=False)
    def test_order_independent_ids(self):
        a=self.result();self.modules.reverse();self.assertEqual([c['id'] for c in a['checks']],[c['id'] for c in self.result()['checks']])
    def test_input_immutable(self):
        before=copy.deepcopy(self.modules);self.result();self.assertEqual(before,self.modules)
    def test_incomplete_module(self):
        self.modules[0]['complete']=False;self.assertEqual(self.result()['overall_status'],'INCONCLUSIVE')
    def test_unknown_state_rejected(self):
        self.modules[0]['checks'][0]['status']='APPROVED'
        with self.assertRaises(ValueError):self.result()
    def test_negative_interval_rejected(self):
        self.modules[0]['checks'][0]['physical_interval']=[2,1]
        with self.assertRaises(ValueError):self.result()
    def test_unknown_location_pending(self):
        self.modules[0]['checks'][0]['physical_interval']=None
        self.assertTrue(any('physical_location_not_documented' in c['missing_information'] for c in self.result()['checks']))
    def test_difference_only_comparable(self):
        self.modules[0]['checks'][0].update(status='FAIL',required_value={'moment':3})
        self.assertIsNone(self.result()['occurrences'][0]['provided_minus_required'])
    def test_no_silent_solution(self):
        r=self.result();self.assertIsNone(r['selected_solution']);self.assertIsNone(r['detailing_optimization'])
    def test_straight_mode_observation_not_failure(self):
        self.modules[2]['checks'][0].update(status='FAIL',check_type='straight_anchorage_geometry',governing=False,role='MODE_SELECTION_OBSERVATION',evidence={'anchorage_mode':'VERTICAL_BEND'})
        self.modules[2]['checks'].append(dict(self.control,check_id='bend',check_type='vertical_bend_geometry'))
        r=self.result();self.assertEqual(r['overall_status'],'PASS');self.assertFalse(r['proven_nonconformities']);self.assertEqual(r['occurrences'][0]['status'],'FAIL')
    def test_markdown(self):self.assertIn('selected_solution=null',markdown(self.result()))
    def test_duplicate_identity_rejected(self):
        self.modules[0]['checks'].append(copy.deepcopy(self.control))
        with self.assertRaises(ValueError):self.result()
    def test_cannot_hide_arbitrary_failure(self):
        self.modules[0]['checks'][0].update(status='FAIL',governing=False)
        with self.assertRaises(ValueError):self.result()
    def test_check_inapplicability_needs_evidence(self):
        self.modules[0]['checks'][0]['status']='NOT_APPLICABLE'
        with self.assertRaises(ValueError):self.result()
    def test_incompatible_units_no_margin(self):
        self.modules[0]['checks'][0].update(status='FAIL',units={'required':'cm','provided':'m'})
        self.assertIsNone(self.result()['occurrences'][0]['provided_minus_required'])
    def test_source_version_does_not_change_logical_id(self):
        self.modules[0]['source']={'path':'a.json','sha256':'old'}
        before=[c['id'] for c in self.result()['checks']]
        self.modules[0]['source']['sha256']='new'
        self.assertEqual(before,[c['id'] for c in self.result()['checks']])
    def test_no_concretopy_import(self):
        import ast,beam_diagnostic
        tree=ast.parse(Path(beam_diagnostic.__file__).read_text(encoding='utf-8-sig'))
        imports=[n for n in ast.walk(tree) if isinstance(n,(ast.Import,ast.ImportFrom))]
        self.assertFalse(any('concretopy' in ast.unparse(n) for n in imports))

class HistoricalDiagnosticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root=Path(__file__).resolve().parents[2]
        spec=importlib.util.spec_from_file_location('diagnostic_cases',root/'analises/pranchas/validar_diagnostico_vigas.py')
        cls.cases=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.cases)
    def test_v501_incomplete_not_approved(self):self.assertEqual(self.cases.make('V501')['overall_status'],'INCONCLUSIVE')
    def test_v516_existing_failures(self):
        r=self.cases.make('V516');self.assertEqual(r['overall_status'],'FAIL');self.assertEqual(len(r['proven_nonconformities']),4)
        self.assertTrue(any(c['check_type']=='basic_lb_beyond_support' and c['status']=='PASS' for c in r['checks']))
    def test_v517_independent(self):
        a,b=self.cases.make('V516'),self.cases.make('V517')
        self.assertTrue(set(c['id'] for c in a['checks']).isdisjoint(c['id'] for c in b['checks']))
    def test_v536_original_not_replaced_by_alternative(self):
        r=self.cases.make('V536');self.assertEqual(r['overall_status'],'FAIL');self.assertEqual(len(r['proven_nonconformities']),1)
    def test_v565_no_known_failure_not_global_pass(self):
        r=self.cases.make('V565');self.assertEqual(r['overall_status'],'INCONCLUSIVE');self.assertFalse(r['proven_nonconformities'])
    def test_persisted_diagnostics_reproduce(self):
        for beam in ('V501','V516','V517','V536','V565'):
            saved=json.loads((self.cases.BASE/(beam+'_beam_diagnostic.json')).read_text(encoding='utf8'))
            self.assertEqual(saved,self.cases.make(beam))
    def test_real_source_pointers_resolve(self):
        cache={}
        for beam in ('V501','V516','V517','V536','V565'):
            r=self.cases.make(beam)
            for c in r['checks']:
                src=c.get('calculation_source')
                if not isinstance(src,dict) or not src.get('path'):continue
                if src['path'] not in cache:cache[src['path']]=json.loads((self.cases.ROOT/src['path']).read_text(encoding='utf8'))
                data=cache[src['path']]
                for token in src.get('pointer','').split('/')[1:]:
                    data=data[int(token)] if isinstance(data,list) else data[token.replace('~1','/').replace('~0','~')]
    def test_bend_failures_values_preserved(self):
        r=self.cases.make('V516');values=[(c['required_value'],c['provided_value']) for c in r['checks'] if c['check_type']=='vertical_bend_geometry']
        self.assertEqual(sorted(values),[(48.7,40),(48.7,45)])

if __name__=='__main__':unittest.main()
