"""Synthetic topology checks and separately labelled real-sheet regressions."""
import copy
import json
from pathlib import Path
import unittest
from distributed_regions import partition,polygon,rectangle,intersection,reconstruct


def r(id,b):return {'id':id,'bbox':b}


class SyntheticArrangementTests(unittest.TestCase):
    def test_partial_overlap(self):
        c=partition([r('a',[0,0,2,2]),r('b',[1,0,3,2])])
        self.assertEqual(sum(x['area_pt2'] for x in c),6)
        self.assertEqual(sum(x['area_pt2'] for x in c if len(x['region_ids'])==2),2)

    def test_containment(self):
        c=partition([r('a',[0,0,4,4]),r('b',[1,1,2,2])])
        self.assertEqual(sum(x['area_pt2'] for x in c),16)
        self.assertEqual(sum(x['area_pt2'] for x in c if len(x['region_ids'])==2),1)

    def test_adjacent_no_area_overlap(self):
        self.assertIsNone(intersection([0,0,1,1],[1,0,2,1]))
        self.assertTrue(all(len(c['region_ids'])==1 for c in partition([r('a',[0,0,1,1]),r('b',[1,0,2,1])])))

    def test_triple_and_determinism(self):
        regions=[r('a',[.123,0,4,4]),r('b',[1,0,3,4]),r('c',[2,1,5,3])]
        cells=partition(regions)
        self.assertEqual(cells,partition(list(reversed(regions))))
        self.assertTrue(any(len(c['region_ids'])==3 for c in cells))
        self.assertEqual(min(c['bbox'][0] for c in cells),.123)
        for i,c in enumerate(cells):
            for other in cells[i+1:]:self.assertIsNone(intersection(c['bbox'],other['bbox']))

    def test_invalid_and_incomplete(self):
        for p in (None,[[0,0]],[[0,0],[1,1],[1,0],[0,1]],[[0,0],[1,0],[1,float('nan')],[0,1]]):
            with self.assertRaises(ValueError):rectangle(p)
        self.assertEqual(rectangle(polygon([.123,2,3,4])),[.123,2,3,4])


class RealDistributedRegressions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root=Path(__file__).resolve().parents[2]
        cls.prior=json.loads((root/'analises/lajes_grupos_fisicos/inventario.json').read_text(encoding='utf-8'))
        cls.result=reconstruct(cls.prior);cls.a=cls.result['distributed_spatial_analysis']

    def test_snapshot_and_preservation(self):
        self.assertEqual(self.result['occurrences'],self.prior['occurrences'])
        self.assertEqual(self.result['localized_reconstruction'],self.prior['localized_reconstruction'])
        self.assertEqual((len(self.a['regions']),len(self.a['composition_regions'])),(35,119))
        old=next(o for o in self.prior['occurrences'] if o['display_id']=='O036')
        self.assertEqual(next(r for r in self.a['regions'] if r['id']=='R036')['polygon_pdf_pt'],old['region_pdf_pt'])
        for region in self.a['regions']:
            total=sum(c['area_pt2'] for c in self.a['composition_regions'] if region['id'] in c['region_ids'])
            self.assertAlmostEqual(total,region['area_pt2'],places=7)

    def test_repeated_position_not_same_identity(self):
        rr=[r for r in self.a['regions'] if r['position']=='N14']
        self.assertEqual(len(rr),2);self.assertNotEqual(rr[0]['identity_group'],rr[1]['identity_group'])

    def test_color_invariance(self):
        d=copy.deepcopy(self.prior)
        def alter(x):
            if isinstance(x,dict):
                for k,v in x.items():
                    if k in ('color','fill'):x[k]=[0,0,0]
                    else:alter(v)
            elif isinstance(x,list):
                for v in x:alter(v)
        alter(d)
        self.assertEqual(reconstruct(d)['distributed_spatial_analysis'],self.a)

    def test_n38_documentary_confirmation_separate(self):
        item=self.result['stage5_documentary_consistency'][0]
        self.assertEqual(item['original_calls'][0]['call']['quantity_factors'],[6,3])
        self.assertEqual(item['engineer_confirmation']['groups'],4)
        self.assertFalse(item['physical_groups_created'])

    def test_duplicate_call_same_raw_entities_not_double_identity(self):
        d=copy.deepcopy(self.prior);o=copy.deepcopy(next(o for o in d['occurrences'] if o['display_id']=='O036'))
        o['display_id']='O999';o['occurrence_id']='synthetic-duplicate';d['occurrences'].append(o)
        a=reconstruct(d)['distributed_spatial_analysis']
        self.assertEqual(len(a['identity_groups']),35)
        self.assertTrue(any(len(c['region_ids'])>len(c['identity_groups']) for c in a['composition_regions']))

    def test_synthetic_mutations_incomplete_and_orientation(self):
        d=copy.deepcopy(self.prior);o=next(o for o in d['occurrences'] if o['display_id']=='O036');o['region_pdf_pt']=None
        self.assertEqual(reconstruct(d)['distributed_spatial_analysis']['pending'][0]['display_id'],'O036')
        d=copy.deepcopy(self.prior);o=next(o for o in d['occurrences'] if o['display_id']=='O036');p=o['associations'][0]
        p['bar'],p['evidence']['axis']=p['evidence']['axis'],p['bar']
        a=reconstruct(d)['distributed_spatial_analysis']
        self.assertEqual(next(r for r in a['regions'] if r['id']=='R036')['orientation'],1)
        self.assertTrue(all(not c['physical_addition_authorized'] for c in a['composition_regions']))


if __name__=='__main__':unittest.main()
