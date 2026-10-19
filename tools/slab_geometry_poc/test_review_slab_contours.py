"""Review experiment tests, not engineering validation of slab boundaries."""
import copy
import json
from pathlib import Path
import unittest
from review_slab_contours import label_links,review


class SyntheticLabelBlockTests(unittest.TestCase):
    def test_pointer_attached_to_thickness_block(self):
        name={'id':'name','text':'L1','bbox':[0,0,10,10]};h={'id':'h','text':'h:12','bbox':[0,10,10,18]}
        slab={'label':name,'thickness_sources':['h']};line={'id':'pointer','a':[5,20],'b':[5,30]}
        self.assertEqual(label_links(slab,[name],[line]),[])
        self.assertEqual(label_links(slab,[name,h],[line])[0]['target'],[5,30])

    def test_pointer_direction_is_independent_of_segment_order(self):
        name={'id':'name','text':'L1','bbox':[0,0,10,10]};slab={'label':name,'thickness_sources':[]}
        a={'id':'p','a':[5,8],'b':[5,25]};b={'id':'p','a':[5,25],'b':[5,8]}
        self.assertEqual(label_links(slab,[name],[a]),label_links(slab,[name],[b]))


class RealContourReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root=Path(__file__).resolve().parents[2]
        cls.inv=json.loads((root/'analises/lajes_relacoes_contornos/inventario.json').read_text(encoding='utf-8'))
        cls.data=json.loads((root/'analises/lajes_geometria_lideres/entidades_pagina.json').read_text(encoding='utf-8'))
        cls.result=review(cls.inv,cls.data)

    def test_eight_candidates_and_no_invented_l603_boundary(self):
        self.assertEqual(self.result['metrics']['slabs_with_review_candidates'],8)
        self.assertEqual(next(s for s in self.result['slabs'] if s['name']=='L603')['contour_review_candidates'],[])
        self.assertEqual(self.result['metrics']['engineer_confirmed_contours'],0)

    def test_associations_are_occurrence_specific_not_mark_only(self):
        by={s['name']:s for s in self.result['slabs']}
        hits=lambda name:{h['display_id'] for c in by[name]['contour_review_candidates'] for h in c['distributed_intersections']}
        self.assertEqual(hits('L611'),{'O007','O010','O018'})
        self.assertEqual(hits('L612'),{'O006','O015'})
        self.assertEqual(hits('L607'),{'O033','O036'})
        l605=by['L605']['contour_review_candidates'][0]
        self.assertTrue(l605['thin_perimeter_review_flag'])
        self.assertTrue(next(h for h in l605['distributed_intersections'] if h['display_id']=='O058')['fraction_of_graphic_region']>.99)

    def test_input_preservation_and_color_invariance(self):
        previous=copy.deepcopy(self.inv);data=copy.deepcopy(self.data)
        for p in data['paths']:p['color']=[1,0,1];p['fill']=[1,1,0]
        self.assertEqual(review(self.inv,data),self.result);self.assertEqual(self.inv,previous)


if __name__=='__main__':unittest.main()
