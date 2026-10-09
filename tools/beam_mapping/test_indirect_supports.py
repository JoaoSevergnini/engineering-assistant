import copy
import unittest
from indirect_supports import associate, lst_relations

class IndirectSupportsTests(unittest.TestCase):
    def setUp(self):
        self.r = dict(supported_beam='A',supporting_beam='B',supported_beam_support_id=1,
                      file='VGESFS.LST',reaction_unit='kN',reaction_observations={'max':30.,'min':-2.},
                      support_relation_source=[{'line':12}],reaction_source=[{'line':12}],status='INCONCLUSIVE')
        self.e = dict(beams=['A','B'],supported_beam='A',supporting_beam='B',
                      supported_beam_support_id=1,source='plan#7',point=[2.,3.],
                      axis_position_m=2.,same_elevation_confirmed=True)
        self.m = {('A',1,'VGESFS.LST'):dict(source='report header',is_total=True,
                 nature='CHARACTERISTIC',load_case='envelope',downward_sign=1,selected_envelope='max')}
    def run_case(self,e=None,r=None,m=None):
        return associate([self.e if e is None else e],[self.r if r is None else r],
                         floor='F',semantics=self.m if m is None else m)
    def test_confirmed(self):
        row=self.run_case()[0]
        self.assertEqual(row['status'],'CONFIRMED')
        self.assertEqual(row['reaction_value'],30.)
    def test_crossing_without_support(self):
        self.assertEqual(associate([self.e],[],floor='F')[0]['status'],'INCONCLUSIVE')
    def test_reverse_direction(self):
        e=dict(self.e,supported_beam='B',supporting_beam='A')
        self.assertIn('direction_or_identifier_conflict',self.run_case(e=e)[0]['diagnostics'])
    def test_distinct_support_reactions(self):
        r2=dict(self.r,supported_beam_support_id=2,reaction_observations={'max':40.,'min':1.})
        e2=dict(self.e,supported_beam_support_id=2,axis_position_m=5.,source='plan#8')
        meta=dict(self.m,**{})
        meta[('A',2,'VGESFS.LST')]=self.m[('A',1,'VGESFS.LST')]
        rows=associate([self.e,e2],[self.r,r2],floor='F',semantics=meta)
        self.assertEqual([r['reaction_value'] for r in rows],[30.,40.])
    def test_lst_without_plan(self):
        self.assertEqual(associate([], [self.r],floor='F')[0]['diagnostics'],['plan_geometry_pending'])
    def test_support_id_mismatch(self):
        self.assertEqual(len(self.run_case(e=dict(self.e,supported_beam_support_id=2))),2)
    def test_missing_reaction(self):
        self.assertEqual(self.run_case(r=dict(self.r,reaction_observations={}))[0]['status'],'INCONCLUSIVE')
    def test_multiple_cases_not_summed(self):
        other=dict(self.r,file='OTHER.LST')
        rows=associate([self.e],[self.r,other],floor='F',semantics=self.m)
        self.assertTrue(all(r['status']=='INCONCLUSIVE' for r in rows))
        self.assertEqual(rows[0]['reaction_value'],30.)
    def test_no_nature_assumption(self):
        self.assertEqual(self.run_case(m={})[0]['status'],'INCONCLUSIVE')
    def test_partial_reaction(self):
        self.m[('A',1,'VGESFS.LST')]['is_total']=False
        self.assertEqual(self.run_case()[0]['status'],'INCONCLUSIVE')
    def test_elevation_difference(self):
        self.assertEqual(self.run_case(e=dict(self.e,same_elevation_confirmed=False))[0]['status'],'INCONCLUSIVE')
    def test_missing_coordinates(self):
        self.assertEqual(self.run_case(e=dict(self.e,point=None))[0]['status'],'INCONCLUSIVE')
    def test_nonfinite_axis(self):
        self.assertEqual(self.run_case(e=dict(self.e,axis_position_m=float('nan')))[0]['status'],'INCONCLUSIVE')
    def test_design_nature_preserved(self):
        self.m[('A',1,'VGESFS.LST')]['nature']='DESIGN'
        self.assertEqual(self.run_case()[0]['reaction_metadata']['nature'],'DESIGN')
    def test_uplift(self):
        self.m[('A',1,'VGESFS.LST')]['selected_envelope']='min'
        self.assertEqual(self.run_case()[0]['status'],'INCONCLUSIVE')
    def test_sources_preserved(self):
        self.assertEqual(self.run_case()[0]['reaction_source'],[{'line':12}])
    def test_no_mutation(self):
        before=copy.deepcopy(self.r)
        self.run_case()
        self.assertEqual(before,self.r)
    def test_real_parser_source(self):
        import json
        from pathlib import Path
        from tools.extrator_lst.consolidar_viga import consolidate
        raw=json.loads((Path(__file__).resolve().parents[2]/'analises/pranchas/V542_tqs_raw.json').read_text(encoding='utf8'))
        rows=lst_relations([consolidate(raw)])
        selected=[r for r in rows if r['supporting_beam']=='V516' and r['file']=='VGESFS.LST'][0]
        self.assertAlmostEqual(selected['reaction_observations']['max'],35.88253235)
        self.assertEqual(selected['supported_beam_support_id'],1.)
        self.assertTrue(selected['reaction_source'])

    def test_ambiguous_geometry(self):
        rows=associate([self.e,dict(self.e,point=[9.,9.])],[self.r],floor='F',semantics=self.m)
        self.assertTrue(all(r['status']=='INCONCLUSIVE' for r in rows))
    def test_unresolved_support_id(self):
        self.assertEqual(self.run_case(e=dict(self.e,supported_beam_support_id=None),
            r=dict(self.r,supported_beam_support_id=None))[0]['status'],'INCONCLUSIVE')
    def test_bridge_blocks_inconclusive(self):
        from indirect_supports import suspension_connection
        with self.assertRaises(ValueError):
            suspension_connection(self.run_case(m={})[0],connection_id='x',
                supported_geometry={'source':'plan'},applicability_source='engineer',placement='INTERIOR')
    def test_bridge_preserves_reaction_and_roles(self):
        from indirect_supports import suspension_connection
        c=suspension_connection(self.run_case()[0],connection_id='x',
            supported_geometry={'source':'plan','height_cm':52,'width_cm':19},
            applicability_source='engineer',placement='INTERIOR')
        self.assertEqual(c['reaction']['value'],30.)
        self.assertEqual(c['receiving_beam_id'],'B')
        self.assertEqual(c['projected_axis_m'],2.)
    def test_real_original_line(self):
        import json
        from pathlib import Path
        rows=json.loads((Path(__file__).resolve().parents[2]/'analises/pranchas/indirect_supports_lst_inventory.json').read_text(encoding='utf8'))['connections']
        row=next(r for r in rows if r['supported_beam']=='V542' and r['supporting_beam']=='V516' and r['file']=='VGESFS.LST')
        self.assertEqual(row['reaction_source'][0]['lines'],[1357,1357])
        self.assertIn('3.659',row['reaction_source'][0]['original_text'])
        self.assertIn('V516',row['reaction_source'][0]['original_text'])

if __name__=='__main__': unittest.main()
