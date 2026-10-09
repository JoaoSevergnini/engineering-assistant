import unittest
from input_preflight import EXTERNAL_DEPENDENCIES
from input_evidence import fact
from stage1_test_fixtures import model, proved
from physical_geometry import project_occurrences
from longitudinal_review import check_physical_flexure, check_flexure_regions
from test_longitudinal_negative import api, context, diagram

class PhysicalFlexureIntegrationTests(unittest.TestCase):
    def test_constant_negative_matches_legacy_numeric_engine(self):
        m=model();m['physical_geometry']['occurrences'][0].update(function='negative',face='upper')
        ctx=context();ctx['section'].update(h=57,diametro_estribo_mm=6.3)
        bars=project_occurrences(m)
        baseline=check_flexure_regions(bars,ctx,diagram(),api,flexure_sign='NEGATIVE',domain=[0,4])
        inputs={k:proved(True) for k in EXTERNAL_DEPENDENCIES['negative_flexure']+('physical_inventory_complete',)}
        actual=check_physical_flexure(m,ctx,diagram(),api,inputs=inputs,flexure_sign='NEGATIVE')
        self.assertEqual(len(actual['regions']),1)
        self.assertEqual(actual['regions'][0]['result'],baseline)
        self.assertNotEqual(actual['regions'][0]['execution_state'],'NOT_EXECUTED')
    def test_no_API_call_for_unknown_geometry(self):
        m=model();m['physical_geometry']['segments'][0]['geometry']['height_cm']=fact(unit='cm')
        result=check_physical_flexure(m,context(),diagram(),object(),inputs={},flexure_sign='POSITIVE')
        self.assertTrue(result['regions']);self.assertTrue(all(r['execution_state']=='NOT_EXECUTED' for r in result['regions']))
    def test_T_section_not_silently_rectangular(self):
        from input_preflight import preflight
        m=model();m['physical_geometry']['segments'][0]['geometry']['section_shape']=proved('T')
        p=preflight(m,region_id='R1',interval_m=[0,4],control='positive_flexure',inputs={})
        self.assertIn('unsupported_section_shape',p['pending'])
    def test_inventory_false_not_readiness_proof(self):
        from input_preflight import preflight
        i={k:proved(True) for k in EXTERNAL_DEPENDENCIES['positive_flexure']};i['physical_inventory_complete']=proved(False)
        p=preflight(model(),region_id='R1',interval_m=[0,4],control='positive_flexure',inputs=i)
        self.assertIn('physical_inventory_complete',p['pending'])

if __name__=='__main__':unittest.main()
