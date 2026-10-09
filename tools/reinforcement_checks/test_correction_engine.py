import copy,json,unittest
from correction_engine import bend_geometry,propose_corrections

class CorrectionEngineTests(unittest.TestCase):
    def geometry(self):
        names=('support_geometry','endpoint_position','cover','bar_diameter','available_space','bend_pin_criterion','straight_leg_criteria')
        return dict(bend_shape='ORTHOGONAL_90_DEG',sources={n:'explicit synthetic source' for n in names},diameter_mm=20,cover_cm=2.5,available_horizontal_cm=30,available_vertical_cm=80,inner_bend_diameter_mm=100,minimum_inner_diameter_mm=80,horizontal_leg_cm=10,vertical_leg_cm=40,minimum_horizontal_leg_cm=10,minimum_vertical_leg_cm=30,position_within_support={'status':'PASS','source':'position verification'},node_interferences={'status':'PASS','source':'node verification'})
    def diagnostic(self):return {'context':{'beam_id':'V1','floor':'F'},'occurrences':[{'occurrence_id':'o1','status':'FAIL','check_type':'anchorage_length','drawing_reinforcement_ids':['N1'],'required_value':30,'provided_value':20}]}
    def run_engine(self,**kw):return propose_corrections(self.diagnostic(),occurrence_id='o1',bar='N1',extremity='LEFT',support_geometry={'support_type':'END','support_side':'LEFT','provenance':'fixture'},original_geometry={'x_m':-.12},**kw)
    def test_viable_geometry(self):self.assertEqual(bend_geometry(self.geometry())['status'],'PASS')
    def test_impossible_geometry(self):
        g=self.geometry();g['available_horizontal_cm']=10;self.assertEqual(bend_geometry(g)['status'],'FAIL')
    def test_missing_geometry(self):self.assertEqual(bend_geometry({})['status'],'INCONCLUSIVE')
    def test_curve_inconclusive_despite_geometric_pass(self):
        a=self.run_engine(bend_data=self.geometry())['alternatives'][0]
        self.assertEqual(a['geometric_feasibility'],'PASS');self.assertEqual(a['structural_feasibility'],'INCONCLUSIVE');self.assertFalse(a['ready_for_detailing'])
    def test_interference(self):
        g=self.geometry();g['node_interferences']={'status':'FAIL','source':'collision evidence'};self.assertEqual(bend_geometry(g)['status'],'FAIL')
    def test_unknown_interference(self):
        g=self.geometry();g.pop('node_interferences');self.assertEqual(bend_geometry(g)['status'],'INCONCLUSIVE')
    def test_no_resistant_credit_for_developed_length(self):
        r=bend_geometry(self.geometry());self.assertGreater(r['geometry']['developed_length_cm'],50);self.assertFalse(r['developed_length_is_resistant_anchorage'])
    def test_bend_pin_failure(self):
        g=self.geometry();g['minimum_inner_diameter_mm']=200;self.assertEqual(bend_geometry(g)['status'],'FAIL')
    def test_favorable_geometry_without_source_is_pending(self):
        g=self.geometry();g['sources'].pop('bend_pin_criterion');self.assertEqual(bend_geometry(g)['status'],'INCONCLUSIVE')
    def test_independent_end_and_mark_validation(self):
        with self.assertRaises(ValueError):propose_corrections(self.diagnostic(),occurrence_id='o1',bar='OTHER',extremity='LEFT',support_geometry={'support_type':'END','support_side':'RIGHT','provenance':'fixture'},original_geometry={})
    def test_deterministic_and_original_immutable(self):
        d=self.diagnostic();g=self.geometry();before=copy.deepcopy((d,g))
        a=propose_corrections(d,occurrence_id='o1',bar='N1',extremity='RIGHT',support_geometry={'support_type':'END','support_side':'RIGHT','provenance':'fixture'},original_geometry={},bend_data=g)
        b=propose_corrections(d,occurrence_id='o1',bar='N1',extremity='RIGHT',support_geometry={'support_type':'END','support_side':'RIGHT','provenance':'fixture'},original_geometry={},bend_data=g)
        self.assertEqual(a,b);self.assertEqual((d,g),before);self.assertIsNone(a['selected_solution']);self.assertFalse(a['pdf_modified'])
    def secondary(self,kind='EXTEND_OTHER_BARS'):return {'type':kind,'proposed_geometry':{'end':2},'changed_dimensions':['end'],'affected_checks':['anchorage','flexure']}
    def test_extension_without_gain_fails(self):
        def verify(s):return {'checks':[{'check_id':'anchorage','status':'FAIL','source':'real verifier'}]} if s['type']!='END_BEND' else {}
        a=self.run_engine(secondary_candidates=[self.secondary()],reverify=verify)['alternatives'][1]
        self.assertEqual(a['status'],'FAIL');self.assertEqual(a['reverification_results'][1]['status'],'INCONCLUSIVE')
    def test_secondary_types(self):
        for kind in ('ALTER_DIAMETER','ALTER_QUANTITY','REDISTRIBUTE_BARS','EXTEND_OTHER_BARS','ADD_POSITION'):
            self.assertEqual(self.run_engine(secondary_candidates=[self.secondary(kind)])['alternatives'][1]['intervention_type'],kind)
    def test_each_candidate_reverified(self):
        calls=[]
        def verify(s):calls.append(s['type']);return {}
        self.run_engine(secondary_candidates=[self.secondary()],reverify=verify);self.assertEqual(calls,['END_BEND','EXTEND_OTHER_BARS'])
    def test_unproven_pass_not_accepted(self):
        def verify(s):return {'checks':[{'check_id':'curved_anchorage_resistance','status':'PASS'}]} if s['type']=='END_BEND' else {}
        self.assertEqual(self.run_engine(bend_data=self.geometry(),reverify=verify)['alternatives'][0]['status'],'INCONCLUSIVE')
    def test_complete_reverification_still_requires_engineer(self):
        def verify(s):return {'checks':[{'check_id':'curved_anchorage_resistance','status':'PASS','source':'explicit synthetic resistant verifier'}]}
        a=self.run_engine(bend_data=self.geometry(),reverify=verify)['alternatives'][0]
        self.assertEqual(a['status'],'PASS');self.assertEqual(a['engineer_approval'],'PENDING_ENGINEERING_APPROVAL');self.assertFalse(a['ready_for_detailing'])
    def test_real_v536(self):
        from pathlib import Path
        root=Path(__file__).resolve().parents[2]
        r=json.loads((root/'analises/pranchas/V536_N2_correction_engine.json').read_text(encoding='utf8'))
        self.assertEqual(r['alternatives'][0]['status'],'INCONCLUSIVE');self.assertIsNone(r['selected_solution'])
        self.assertAlmostEqual(r['original_anchorage']['lb_nec_cm'],24.203000349699796)
        self.assertTrue(all(not a['ready_for_detailing'] for a in r['alternatives']))
        self.assertTrue(any(a['intervention_type']=='EXTEND_OTHER_BARS' for a in r['alternatives']))

    def test_other_bend_shape_not_assumed(self):
        g=self.geometry();g['bend_shape']='OTHER';self.assertEqual(bend_geometry(g)['status'],'INCONCLUSIVE')
    def test_affected_controls_not_silently_omitted(self):
        a=self.run_engine(secondary_candidates=[self.secondary()])['alternatives'][1]
        self.assertEqual({c['check_id'] for c in a['reverification_results']},{'anchorage','flexure'})
        self.assertTrue(all(c['status']=='INCONCLUSIVE' for c in a['reverification_results']))
    def test_interior_support_rejected(self):
        with self.assertRaises(ValueError):propose_corrections(self.diagnostic(),occurrence_id='o1',bar='N1',extremity='LEFT',original_geometry={},support_geometry={'support_type':'INTERMEDIATE','support_side':'LEFT','provenance':'fixture'})
    def test_historical_sources_unchanged(self):
        from pathlib import Path
        import hashlib
        root=Path(__file__).resolve().parents[2]
        r=json.loads((root/'analises/pranchas/V536_N2_correction_engine.json').read_text(encoding='utf8'))
        for name,source in r['source_files'].items():self.assertEqual(hashlib.sha256((root/source['path']).read_bytes()).hexdigest(),source['sha256'])
    def test_no_pdf_io_in_engine(self):
        import inspect,correction_engine
        text=inspect.getsource(correction_engine)
        self.assertNotIn('write_text(',text);self.assertNotIn('open(',text);self.assertNotIn('fitz',text)

if __name__=='__main__':unittest.main()
