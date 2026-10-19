"""Synthetic overlay tests and distinct frozen real-sheet regressions."""
import copy
import json
from pathlib import Path
import unittest
from polygonal_slabs import box, geo, shape, Polygon, LineString, unary_union
from slab_assignment import partition_domains, analyze, apply_confirmations


def domain(id, bounds, h=20, confirmed=False):
    return dict(id=id,slab=id,thickness_cm=h,geometry_pdf_pt=geo(box(*bounds)),confirmed=confirmed,review_flag=False)


class SyntheticAssignmentTests(unittest.TestCase):
    def test_crossing_two_thicknesses_conserves_area_and_no_quantities(self):
        source=box(0,0,10,4)
        parts=partition_domains(source,[domain('A',[0,0,5,4],12),domain('B',[5,0,10,4],20)])
        self.assertEqual([p['thickness_options_cm'] for p in parts],[[12],[20]])
        self.assertEqual(sum(p['measure'] for p in parts),40)
        self.assertTrue(unary_union([shape(p['geometry_pdf_pt']) for p in parts]).equals(source))
        self.assertTrue(all(p['quantity_allocation'] is None for p in parts))

    def test_adjacent_touch_has_no_area(self):
        p=partition_domains(box(0,0,1,1),[domain('A',[1,0,2,1])])
        self.assertEqual(p[0]['domain_ids'],[])

    def test_competing_domains_remain_indeterminate(self):
        p=partition_domains(box(0,0,2,2),[domain('A',[0,0,2,2],12),domain('B',[0,0,2,2],20)])
        self.assertEqual(p[0]['state'],'INDETERMINATE')
        self.assertEqual(p[0]['thickness_options_cm'],[12,20])

    def test_same_slab_alternatives_are_not_collapsed(self):
        a=domain('A',[0,0,2,2]);b=domain('B',[0,0,2,2]);b['slab']='A'
        p=partition_domains(box(0,0,2,2),[a,b])[0]
        self.assertEqual(p['slabs'],['A']);self.assertEqual(p['state'],'INDETERMINATE')

    def test_hole_and_uncovered_parts_preserved(self):
        d=domain('A',[0,0,4,4]);d['geometry_pdf_pt']=geo(Polygon([(0,0),(4,0),(4,4),(0,4)],holes=[[(1,1),(2,1),(2,2),(1,2)]]))
        p=partition_domains(box(0,0,4,4),[d])
        self.assertEqual(sum(s['measure'] for s in p if not s['slabs']),1)
        self.assertEqual(sum(s['measure'] for s in p),16)

    def test_confirmed_and_candidate_confidence(self):
        a=domain('A',[0,0,3,3]);g=box(1,1,2,2)
        self.assertEqual(partition_domains(g,[a])[0]['state'],'PROBABLE')
        a['confirmed']=True
        self.assertEqual(partition_domains(g,[a])[0]['state'],'RELIABLE')

    def test_vertical_localized_trace_not_area(self):
        p=partition_domains(LineString([(1,0),(1,10)]),[domain('A',[0,0,2,5],12),domain('B',[0,5,2,10],20)],1)
        self.assertEqual(sum(s['measure'] for s in p),10)
        self.assertTrue(all(shape(s['geometry_pdf_pt']).area==0 for s in p))

    def test_order_colors_and_original_coordinates(self):
        ds=[domain('A',[0,0,2,4]),domain('B',[2,0,4,4])];before=copy.deepcopy(ds)
        a=partition_domains(box(0,0,4,4),ds)
        self.assertEqual(ds,before)
        for d in ds:d['color']='irrelevant'
        self.assertEqual(a,partition_domains(box(0,0,4,4),list(reversed(ds))))

    def test_invalid_geometry_not_repaired(self):
        self.assertEqual(partition_domains(Polygon([(0,0),(2,2),(2,0),(0,2)]),[]),[])


class RealSheetAssignmentRegressions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root=Path(__file__).resolve().parents[2]
        cls.old=json.loads((root/'analises/lajes_contornos_complexos/inventario.json').read_text(encoding='utf8'))
        cls.new=json.loads((root/'analises/lajes_associacao_espessuras/inventario.json').read_text(encoding='utf8'))
        cls.a=cls.new['slab_reinforcement_assignment']

    def test_every_prior_layer_exactly_preserved(self):
        for k,v in self.old.items():self.assertEqual(self.new[k],v,k)

    def test_all_59_including_unresolved_and_repeated_marks(self):
        self.assertEqual(len(self.a['occurrences']),59)
        self.assertEqual(self.a['metrics']['without_actuation_geometry'],9)
        self.assertEqual(len([o for o in self.a['occurrences'] if o['documentary_mark']=='N14']),2)

    def test_human_full_n14_and_n40_lap_are_scoped(self):
        h={r['region_id']:r for r in self.a['human_confirmations']}
        self.assertEqual(h['R034']['scope'],'FULL_OCCURRENCE_EXTENT')
        self.assertEqual(h['R035']['classification'],'REINFORCEMENT')
        self.assertEqual(h['R053']['classification'],'LAP_SPLICE')
        p={'source_pdf_sha256':'bad','records':list(h.values())}
        with self.assertRaises(ValueError):apply_confirmations(self.old['distributed_spatial_analysis']['regions'],p,'good')

    def test_area_and_trace_length_conservation(self):
        for o in self.a['occurrences']:
            if o['representation_kind']=='DISTRIBUTED':
                r=next(r for r in self.old['distributed_spatial_analysis']['regions'] if r['occurrence_id']==o['occurrence_id'])
                self.assertAlmostEqual(sum(s['measure'] for s in o['segments']),r['area_pt2'],places=5)
            for g in o['geometry_sources']:
                if 'physical_group_id' not in g:continue
                length=sum(s['measure'] for s in o['segments'] if s.get('physical_group_id')==g['physical_group_id'])
                self.assertAlmostEqual(length,shape(g['geometry_pdf_pt']).length,places=5)

    def test_documentary_provenance_and_no_real_multi_claim(self):
        self.assertEqual(self.a['metrics']['multiple_slabs'],0)
        self.assertEqual(len(self.a['domains']),9)
        self.assertTrue(all(d['source']['thickness_texts'] for d in self.a['domains']))
        self.assertTrue(all(not d['confirmed'] for d in self.a['domains']))

    def test_reexecution_deterministic(self):
        profile={'source_pdf_sha256':self.old['stage5_provenance']['sha256'],'records':self.a['human_confirmations']}
        a=analyze(self.old,confirmations=profile)
        self.assertEqual(a['occurrences'],self.a['occurrences'])


if __name__=='__main__':unittest.main()
