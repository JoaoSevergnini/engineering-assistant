import copy,json,sys,unittest
from pathlib import Path
from beam_diagnostic import module_execution,aggregate_execution,attach_execution,markdown,occurrence_groups
import test_beam_diagnostic as existing_tests
from detailing_change_contracts import detailing_preferences,diameter_preference,proposal_template,validate_proposal
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from tools.beam_mapping.termination_geometry import interpret_endpoints

class DiagnosticUpdateTests(unittest.TestCase):
    def test_execution_states(self):
        cases=[({'execution_state':'NOT_EXECUTED','checks':[]},'NOT_EXECUTED'),({'complete':False,'checks':[{'status':'FAIL'}]},'PARTIALLY_EXECUTED'),({'complete':True,'checks':[{'status':'INCONCLUSIVE'}]},'EXECUTED_INCONCLUSIVE'),({'complete':True,'checks':[{'status':'FAIL'}]},'EXECUTED_COMPLETE')]
        for module,state in cases:
            with self.subTest(state=state):self.assertEqual(module_execution(module),state)
    def test_execution_aggregation(self):
        for states,expected in [([], 'NOT_EXECUTED'),(['EXECUTED_COMPLETE','NOT_EXECUTED'],'PARTIALLY_EXECUTED'),(['EXECUTED_COMPLETE','EXECUTED_INCONCLUSIVE'],'EXECUTED_INCONCLUSIVE'),(['EXECUTED_COMPLETE'],'EXECUTED_COMPLETE')]:self.assertEqual(aggregate_execution(states),expected)
    def test_failure_preserved_when_partial(self):
        fixture=existing_tests.BeamDiagnosticTests();fixture.setUp();fixture.modules[0]['complete']=False;fixture.modules[0]['checks'][0]['status']='FAIL'
        original=fixture.result();updated=attach_execution(original)
        self.assertEqual(updated['overall_status'],'FAIL');self.assertEqual(updated['execution_state'],'PARTIALLY_EXECUTED')
        self.assertEqual([c['id'] for c in original['checks']],[c['id'] for c in updated['checks']])
        self.assertNotIn('execution_state',original)
    def test_grouping_keeps_occurrences_and_relations(self):
        fixture=existing_tests.BeamDiagnosticTests();fixture.setUp()
        for m in fixture.modules:m['checks'][0]['status']='FAIL'
        r=attach_execution(fixture.result());before=copy.deepcopy(r)
        groups=occurrence_groups(r);text=markdown(r)
        self.assertEqual(sum(len(g['occurrence_ids']) for g in groups),len(r['occurrences']))
        self.assertEqual(before,r);self.assertTrue(r['relations']);self.assertNotIn('single_correction_proven',text)
    def test_preferences_configurable_not_normative(self):
        p=detailing_preferences([10,12.5,16,20,25]);self.assertEqual(diameter_preference(12.5,20,p)['steps'],2)
        self.assertFalse(diameter_preference(10,20,p)['preferred']);self.assertFalse(p['diameter_step_preference_is_normative']);self.assertIsNone(p['excess_limits'])
        self.assertFalse(p['values_below_required_acceptable']);self.assertFalse(p['optimizer_implemented'])
        self.assertTrue(diameter_preference(10,20,detailing_preferences([10,12.5,16,20],max_diameter_steps=3))['preferred'])
    def test_template_serializable_without_pdf_coordinates(self):
        p=json.loads(json.dumps(proposal_template()));self.assertIsNone(p['graphical_reference']);self.assertFalse(p['ready_for_graphical_application'])
    def proposal(self):
        p=proposal_template();p.update(beam_id='V1',floor='F',drawing_source='drawing.pdf',drawing_version='R0',reinforcement_mark='N1',original_geometry={},proposed_geometry={},operation='ALTER_LENGTH');return p
    def test_draft_is_not_approved(self):self.assertFalse(validate_proposal(self.proposal())['ready_for_graphical_application'])
    def test_approval_requires_reverification(self):
        p=self.proposal();p['approval_state']='APPROVED'
        with self.assertRaises(ValueError):validate_proposal(p)
    def test_graphical_reference_requires_mapping(self):
        p=self.proposal();p['graphical_reference']={'page':1}
        with self.assertRaises(ValueError):validate_proposal(p)
    def test_reverification_identity(self):
        p=self.proposal();p['reverification_results']=[{'beam_id':'V2','floor':'F'}]
        with self.assertRaises(ValueError):validate_proposal(p)
    def test_v536_reverified(self):
        r=json.loads((ROOT/'analises/pranchas/V536_positive_diagnostic_reverification.json').read_text(encoding='utf8'))
        self.assertEqual(r['interpreted_N2']['x_start_common'],-.12)
        self.assertEqual(r['original_N2']['x_start_common'],-.09)
        self.assertFalse(r['left_support']['longitudinal_anchorage_passes'])
        self.assertTrue(r['right_support']['longitudinal_anchorage_passes'])
        self.assertTrue(r['positive_scaling']['overall']['scaling_passes'])
        self.assertIsNone(r['selected_solution']);self.assertIsNone(r['detailing_optimization'])
    def test_negative_history_preserved(self):
        for beam in ('V516','V517'):
            base=ROOT/'analises/pranchas';old=json.loads((base/(beam+'_beam_diagnostic.json')).read_text(encoding='utf8'));new=json.loads((base/(beam+'_beam_diagnostic_updated.json')).read_text(encoding='utf8'))
            self.assertEqual([(c['id'],c['status']) for c in old['checks']],[(c['id'],c['status']) for c in new['checks']]);self.assertEqual(new['overall_status'],'FAIL')

class EndpointTests(unittest.TestCase):
    def end(self):return dict(terminates_in_support=True,support_type='END',support_element='COLUMN',external_face_m=-.12,graphical_x_m=-.09,source='geometry')
    def test_face_not_graphic(self):
        e={'LEFT':self.end()};original=copy.deepcopy(e);r=interpret_endpoints(e)
        self.assertEqual(r['resolved']['LEFT']['x_m'],-.12);self.assertEqual(e,original);self.assertFalse(r['bend_geometry_inferred']);self.assertFalse(r['anchorage_length_inferred'])
    def test_explicit_dimension_wins(self):
        e=self.end();e.update(explicit_x_m=-.07,explicit_dimension_source='dimension');self.assertEqual(interpret_endpoints({'LEFT':e})['resolved']['LEFT']['x_m'],-.07)
    def test_right_face(self):
        e=self.end();e['external_face_m']=5.;self.assertEqual(interpret_endpoints({'RIGHT':e})['resolved']['RIGHT']['x_m'],5.)
    def test_both_undimensioned_inconclusive(self):self.assertEqual(interpret_endpoints({'LEFT':self.end(),'RIGHT':self.end()})['status'],'INCONCLUSIVE')
    def test_missing_source(self):
        e=self.end();e.pop('source');self.assertEqual(interpret_endpoints({'LEFT':e})['status'],'INCONCLUSIVE')
    def test_noncolumn_not_assumed(self):
        e=self.end();e['support_element']='BEAM';self.assertEqual(interpret_endpoints({'LEFT':e})['status'],'INCONCLUSIVE')
    def test_inconsistent_interval(self):
        e=dict(explicit_x_m=1.,explicit_dimension_source='dimension');self.assertEqual(interpret_endpoints({'LEFT':e,'RIGHT':e})['status'],'INCONCLUSIVE')
    def test_nonfinite_face(self):
        e=self.end();e['external_face_m']=float('nan');self.assertEqual(interpret_endpoints({'LEFT':e})['status'],'INCONCLUSIVE')

if __name__=='__main__':unittest.main()

