import copy,json,unittest
from pathlib import Path
from correction_engine import apply_scope_decision,SCOPE_RULE,EXCLUDED_NODE_CONTROLS

class CorrectionScopeTests(unittest.TestCase):
    def decision(self):return {'rule':SCOPE_RULE,'source':'engineer decision','excluded_controls':list(EXCLUDED_NODE_CONTROLS)}
    def candidate(self):return {'geometry_verification':{'checks':[{'check_id':'transverse_fit','status':'PASS','source':'geometry'},{'check_id':'node_interferences','status':'INCONCLUSIVE'}],'status':'INCONCLUSIVE','pending_information':['node_interferences']},'reverification_results':[{'check_id':'corrected_steel_area','status':'PASS','source':'Concretopy'},{'check_id':'node_interferences','status':'INCONCLUSIVE'}],'status':'INCONCLUSIVE','pending_information':['node_interferences']}
    def test_exclusions_are_not_pass(self):
        r=apply_scope_decision(self.candidate(),self.decision())
        self.assertEqual(r['status'],'PASS')
        for c in r['verification_register']['not_executed_by_scope']:
            self.assertEqual(c['execution_state'],'NOT_EXECUTED');self.assertIsNone(c['technical_status'])
    def test_original_audit_and_inputs_preserved(self):
        a=self.candidate();before=copy.deepcopy(a);r=apply_scope_decision(a,self.decision())
        self.assertEqual(a,before);self.assertEqual(r['scope_audit_before_exclusions']['status'],'INCONCLUSIVE')
    def test_real_failure_stays_failure(self):
        a=self.candidate();a['reverification_results'][0]['status']='FAIL'
        r=apply_scope_decision(a,self.decision());self.assertEqual(r['status'],'FAIL');self.assertTrue(r['verification_register']['executed_failed'])
    def test_missing_required_data_stays_inconclusive(self):
        a=self.candidate();a['reverification_results'][0]['status']='INCONCLUSIVE'
        r=apply_scope_decision(a,self.decision());self.assertEqual(r['status'],'INCONCLUSIVE');self.assertTrue(r['verification_register']['inconclusive_missing_data'])
    def test_cannot_exclude_flexure(self):
        d=self.decision();d['excluded_controls'].append('regional_positive_flexure')
        with self.assertRaises(ValueError):apply_scope_decision(self.candidate(),d)
    def test_scope_needs_source(self):
        d=self.decision();d.pop('source')
        with self.assertRaises(ValueError):apply_scope_decision(self.candidate(),d)
    def test_area_pass_does_not_prove_construction(self):self.assertFalse(apply_scope_decision(self.candidate(),self.decision())['construction_conditions_fully_proven'])
    def test_real_results_and_staples_not_credited(self):
        root=Path(__file__).resolve().parents[2];r=json.loads((root/'analises/pranchas/V536_N2_correction_engine_scope_updated.json').read_text(encoding='utf8'))
        self.assertIsNone(r['selected_solution']);self.assertFalse(r['staple_resistant_contribution_credited'])
        self.assertEqual(len(r['complementary_staples']),3)
        for a in r['alternatives']:
            self.assertFalse(a['ready_for_detailing']);self.assertEqual(len(a['verification_register']['not_executed_by_scope']),3)
            self.assertNotIn('node_interferences',a['pending_information'])

if __name__=='__main__':unittest.main()
