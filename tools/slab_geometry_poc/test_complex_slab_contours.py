"""Synthetic boundary selection and independent real-sheet regressions."""
import copy
import json
import math
from pathlib import Path
import unittest
from unittest.mock import patch
from complex_slab_contours import context_segments,recognize
from polygonal_slabs import shape,Point,geo
from contour_validation import compare


def segment(id,a,b):
    return {'id':id,'path_id':id,'a':a,'b':b,'length_pt':math.dist(a,b),
            'angle_deg':math.degrees(math.atan2(b[1]-a[1],b[0]-a[0]))}


def fixture(ring,roi,label_box):
    edges=[segment('e'+str(i),a,b) for i,(a,b) in enumerate(zip(ring,ring[1:]+ring[:1]))]
    label={'id':'label','text':'SYNTHETIC_SLAB','bbox':label_box}
    thickness={'id':'h','text':'h:20','bbox':[label_box[0],label_box[3],label_box[2],label_box[3]+2]}
    slab={'id':'label','name':'SYNTHETIC_SLAB','thickness_cm':20,'label':label,'thickness_sources':['h']}
    inv={'layout':{'detail_roi_pt':roi},'structural_interpretation':{'slabs':[slab]},'occurrences':[]}
    return inv,{'segments':edges,'texts':[label,thickness],'paths':[]}


def hatch_support(data,ys):
    data['segments'].extend(segment('h'+str(i),[0,y],[3,y+3]) for i,y in enumerate(ys))


class SyntheticComplexContourTests(unittest.TestCase):
    def test_context_crossing_preserves_full_original_geometry(self):
        s=segment('crossing',[0,0],[12,0]);original=copy.deepcopy(s)
        kept,crossings,dropped=context_segments([s],[-1,-1,10.5,13])
        self.assertEqual(kept,[original]);self.assertEqual(s,original)
        self.assertEqual(crossings[0]['original_b'],[12,0]);self.assertFalse(dropped)
        self.assertFalse(context_segments([s],[-1,-1,10.5,13],1)[0])

    def test_context_fix_closes_face_without_inserting_segments(self):
        inv,data=fixture([[0,0],[100,0],[100,100],[0,100]],[-1,-1,105,113],[20,30,70,60])
        data['segments'][0]=segment('e0',[0,0],[120,0]);data['segments'][2]=segment('e2',[120,100],[0,100]);hatch_support(data,[10,50,90])
        strict=recognize(inv,data,1);result=recognize(inv,data)
        self.assertEqual(strict['metrics']['unresolved_labels'],1)
        candidate=result['candidates'][0]
        self.assertEqual(candidate['area_pt2'],10000);self.assertEqual(candidate['synthetic_closure_segments'],[])

    def test_nonconvex_l_preserves_reentrant_corner(self):
        inv,data=fixture([[0,0],[50,0],[50,10],[10,10],[10,50],[0,50]],[-1,-1,51,51],[1,30,7,36]);hatch_support(data,[8,16,24])
        result=recognize(inv,data);poly=shape(result['candidates'][0]['geometry_pdf_pt'])
        self.assertEqual(poly.area,900);self.assertFalse(poly.contains(Point(30,30)))
        self.assertTrue(poly.contains(Point(5,30)));self.assertLess(poly.area,poly.convex_hull.area)

    def test_closed_annotation_rectangle_is_not_sufficient(self):
        inv,data=fixture([[0,0],[50,0],[50,50],[0,50]],[-1,-1,51,51],[20,20,27,27])
        self.assertEqual(recognize(inv,data)['candidates'],[])
        # Known bar strokes must remain excluded even if they close a region.
        inv['occurrences']=[{'associated_lines':[dict(e,source_ids=[e['id']]) for e in data['segments']]}]
        hatch_support(data,[8,16,24]);self.assertEqual(recognize(inv,data)['candidates'],[])

    def test_no_gap_repair_or_convex_hull_fallback(self):
        inv,data=fixture([[0,0],[50,0],[50,50],[0,50]],[-1,-1,51,51],[20,20,27,27]);hatch_support(data,[8,16,24]);data['segments'][1]['b']=[50,49]
        self.assertEqual(recognize(inv,data)['candidates'],[])

    def test_long_layout_line_does_not_enter_context(self):
        kept,crossings,dropped=context_segments([segment('frame',[0,-100],[0,100])],[-1,-1,10,10])
        self.assertFalse(kept);self.assertEqual(dropped[0]['reason'],'LONG_LAYOUT_CROSSING_CONTEXT_FILTER')


class RealComplexContourRegressions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root=Path(__file__).resolve().parents[2]
        cls.inv=json.loads((cls.root/'analises/lajes_relacoes_contornos/inventario.json').read_text(encoding='utf-8'))
        cls.data=json.loads((cls.root/'analises/lajes_geometria_lideres/entidades_pagina.json').read_text(encoding='utf-8'))
        cls.result=recognize(cls.inv,cls.data)

    def test_l603_recovered_from_vectors_without_reference(self):
        c=next(s for s in self.result['slabs'] if s['name']=='L603')['candidates'][0]
        poly=shape(c['geometry_pdf_pt'])
        self.assertTrue(poly.is_valid);self.assertTrue(poly.contains(Point(600,800)));self.assertTrue(poly.contains(Point(1400,800)))
        self.assertFalse(poly.contains(Point(970,740)));self.assertFalse(poly.contains(Point(970,1050)))
        self.assertIn('D1160:0',c['crossing_roi_segment_ids']);self.assertEqual(c['synthetic_closure_segments'],[])
        self.assertFalse(c['engineer_confirmed']);self.assertFalse(self.result['reference_used_for_recognition'])

    def test_reproduce_previous_context_failure(self):
        strict=recognize(self.inv,self.data,1)
        self.assertEqual(next(s for s in strict['slabs'] if s['name']=='L603')['state'],'UNRESOLVED')
        self.assertEqual(self.result['metrics']['unique_candidate_labels'],9)

    def test_other_eight_slabs_preserved_exactly(self):
        previous=json.loads((self.root/'analises/lajes_revisao_contornos/revisao.json').read_text(encoding='utf-8'))
        for name in ('L601','L602','L604','L605','L606','L607','L611','L612'):
            expected=next(s for s in previous['slabs'] if s['name']==name)['contour_review_candidates'][0]['geometry_pdf_pt']
            actual=next(s for s in self.result['slabs'] if s['name']==name)['candidates'][0]
            self.assertEqual(actual['geometry_pdf_pt'],expected);self.assertFalse(actual['engineer_confirmed'])
        self.assertTrue(next(s for s in self.result['slabs'] if s['name']=='L605')['candidates'][0]['thin_border_review_flag'])

    def test_reference_only_evaluation_has_local_mismatch(self):
        from confirmed_slab_outline import register_outline
        profile=json.loads((self.root/'analises/lajes_l603_confirmada/confirmacao_joao_L603.json').read_text(encoding='utf-8'));reference,_=register_outline(profile)
        c=next(s for s in self.result['slabs'] if s['name']==profile['slab'])['candidates'][0]
        metrics=compare(c['geometry_pdf_pt'],geo(reference),8)
        self.assertGreater(metrics['intersection_over_union'],.95)
        self.assertGreater(metrics['exterior_hausdorff_distance_pt'],8)
        self.assertFalse(metrics['automatic_validation_authorized'])

    def test_invariance_color_order_names_and_human_contour_metadata(self):
        inv=copy.deepcopy(self.inv);data=copy.deepcopy(self.data)
        for p in data['paths']:p['color']=[1,0,1];p['fill']=[0,1,0]
        data['segments'].reverse();data['texts'].reverse()
        for s in inv['structural_interpretation']['slabs']:s['contour_alternatives']=[];s['contour']=None
        original=copy.deepcopy(inv)
        with patch('confirmed_slab_outline.register_outline',side_effect=AssertionError('Reference leaked into production')):
            result=recognize(inv,data)
        self.assertEqual(result,self.result);self.assertEqual(inv,original)

    def test_rename_slab_label_does_not_change_geometry(self):
        inv=copy.deepcopy(self.inv);s=next(s for s in inv['structural_interpretation']['slabs'] if s['name']=='L603');s['name']='UNSEEN_LABEL'
        result=recognize(inv,self.data)
        before=next(s for s in self.result['slabs'] if s['name']=='L603')['candidates'][0]['geometry_pdf_pt']
        self.assertEqual(next(s for s in result['slabs'] if s['name']=='UNSEEN_LABEL')['candidates'][0]['geometry_pdf_pt'],before)


if __name__=='__main__':unittest.main()
