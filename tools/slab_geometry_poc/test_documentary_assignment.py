"""Synthetic context/evidence tests and explicitly distinct real-sheet regressions."""
import copy
import json
from pathlib import Path
import unittest
from unittest.mock import patch
from polygonal_slabs import box,geo,shape,Polygon
from documentary_slab_context import u_frame,support_continuations,build_contexts
from documentary_slab_assignment import analyze
from refine_slab_assignment import refine
from test_refined_assignment import fixture,domain


def edge(id,a,b):return {'id':id,'a':list(a),'b':list(b)}


def frame():
    ring=[(0,0),(0,10),(30,10),(30,0),(28,0),(28,8),(2,8),(2,0)]
    edges=[edge('s'+str(i),a,b) for i,(a,b) in enumerate(zip(ring,ring[1:]+ring[:1]))]
    candidate={'geometry_pdf_pt':geo(Polygon(ring)),'label_evidence':[{'basis':'FULL_NAME_THICKNESS_BLOCK_POINTER'}],
        'boundary_segment_ids':[e['id'] for e in edges]}
    return candidate,edges


def support():
    entries=[]
    for x0,x1 in [(-.5,.5),(9.5,10.5)]:
        ring=[(x0,10),(x1,10),(x1,15),(x0,15)]
        entries.extend(edge(str(len(entries))+str(i),a,b) for i,(a,b) in enumerate(zip(ring,ring[1:]+ring[:1])))
    return {'geometry_pdf_pt':geo(box(0,0,10,10))},entries


def context(d):
    return {'domain_id':d['id'],'slab':d['slab'],'geometry_pdf_pt':d['geometry_pdf_pt'],'thickness_cm':d['thickness_cm'],
        'documentary_sources':d['source'],'context_id':'CTX-'+d['id'],'contour_confidence':'CANDIDATE_NOT_CONFIRMED',
        'contour_review_flag':d['review_flag']}


def evaluate(f,raw=None):
    inv={'refined_slab_assignment':refine(f),'occurrences':[dict(raw or {},occurrence_id='occ')]}
    with patch('documentary_slab_assignment.build_contexts',return_value=[context(d) for d in f['domains']]):return analyze(inv)


def candidate(y=5,x0=-2,x1=12):
    return {'bar':{'a':[x0,y],'b':[x1,y],'source_ids':['bar']},
        'distribution_candidates':[{'axis':{'a':[(x0+x1)/2,0],'b':[(x0+x1)/2,10],'source_ids':['axis']},'junction_path_ids':['marker']}]}


class SyntheticDocumentaryContextTests(unittest.TestCase):
    def test_u_context_uses_source_faces_and_pointer_without_repair(self):
        c,e=frame();before=copy.deepcopy(c);r=u_frame(c,e)
        self.assertEqual(shape(r['geometry_pdf_pt']).area,300)
        self.assertNotEqual(shape(c['geometry_pdf_pt']).area,300)
        self.assertEqual(c,before);self.assertEqual(len(r['parallel_face_evidence']),3)

    def test_u_context_rejects_no_pointer_or_simple_rectangle(self):
        c,e=frame();c['label_evidence']=[];self.assertIsNone(u_frame(c,e))
        c,e=frame();c['geometry_pdf_pt']=geo(box(0,0,30,10));self.assertIsNone(u_frame(c,e))

    def test_u_context_rejects_missing_inner_face(self):
        c,e=frame();e=[s for s in e if s['id']!='s5'];self.assertIsNone(u_frame(c,e))

    def test_capped_opposite_supports_define_context(self):
        c,e=support();r=support_continuations(c,e)
        self.assertEqual(len(r),1);self.assertEqual(shape(r[0]['geometry_pdf_pt']).bounds,(0,10,10,15))

    def test_rejects_one_support_or_missing_end_cap(self):
        c,e=support();self.assertEqual(support_continuations(c,e[:4]),[])
        self.assertEqual(support_continuations(c,e[:-1]),[])

    def test_rotated_support_context(self):
        c,e=support()
        c['geometry_pdf_pt']=geo(box(-10,0,0,10))
        for s in e:
            for k in ['a','b']:s[k]=[-s[k][1],s[k][0]]
        r=support_continuations(c,e)
        self.assertEqual(len(r),1);self.assertEqual(shape(r[0]['geometry_pdf_pt']).bounds,(-15,0,-10,10))

    def test_context_order_and_color_independence(self):
        c,e=support();a=support_continuations(c,e)
        for s in e:s['color']='different'
        self.assertEqual(a,support_continuations(c,list(reversed(e))))


class SyntheticDocumentaryAssociationTests(unittest.TestCase):
    def test_topology_alone_not_a_confidence_veto(self):
        f=fixture();f['domains'][0]['review_flag']=True
        o=evaluate(f)['occurrences'][0]
        self.assertEqual(o['state'],'RELIABLE');self.assertTrue(o['issues']['topological'])
        self.assertEqual(o['contour_confidence'],{'A':'CANDIDATE_NOT_CONFIRMED'})

    def test_consensus_slab_can_be_reliable_with_unselected_bar_alternatives(self):
        f=fixture();o=f['occurrences'][0];o.update(geometry_sources=[],segments=[],representation_kind='INCONCLUSIVE')
        r=evaluate(f,{'candidates':[candidate(5),candidate(6)]})['occurrences'][0]
        self.assertEqual(r['state'],'RELIABLE');self.assertTrue(r['requires_geometry_review'])
        self.assertEqual(r['geometry_sources'],[]);self.assertEqual(r['segments'],[])

    def test_incomplete_geometry_search_remains_probable(self):
        f=fixture();f['occurrences'][0].update(geometry_sources=[],segments=[],representation_kind='INCONCLUSIVE')
        r=evaluate(f,{'candidates':[candidate()], 'leader_search':{'search_limits':['LENGTH_LIMIT']}})['occurrences'][0]
        self.assertEqual(r['state'],'PROBABLE')

    def test_alternatives_disagree_keep_all_slabs_and_thicknesses(self):
        f=fixture([domain('A',(0,0,10,10),12),domain('B',(20,0,30,10),20)])
        f['occurrences'][0].update(geometry_sources=[],segments=[],representation_kind='INCONCLUSIVE')
        r=evaluate(f,{'candidates':[candidate(),candidate(5,18,32)]})['occurrences'][0]
        self.assertEqual(r['state'],'INDETERMINATE');self.assertEqual(r['slabs'],['A','B'])
        self.assertEqual(r['thickness_options_cm'],[12,20])
        self.assertTrue(all(a['state']=='INDETERMINATE' for a in r['slab_associations']))

    def test_accepted_region_crosses_distinct_thickness_domains(self):
        f=fixture([domain('A',(0,0,5,10),12),domain('B',(5,0,10,10),20)])
        r=evaluate(f)['occurrences'][0]
        self.assertNotEqual(r['state'],'INDETERMINATE');self.assertTrue(r['different_thickness_domains'])
        self.assertFalse(r['association_conflicts'])
        self.assertTrue(all(s['quantity_allocation'] is None for s in r['spatial_context_partition']))

    def test_overlapping_contexts_with_different_thicknesses_indeterminate(self):
        r=evaluate(fixture([domain('A',h=12),domain('B',h=20)]))['occurrences'][0]
        self.assertEqual(r['state'],'INDETERMINATE');self.assertTrue(r['association_conflicts'])

    def test_documentary_missing_thickness_is_separate_issue(self):
        f=fixture();f['domains'][0]['source']['thickness_text_ids']=[]
        r=evaluate(f)['occurrences'][0]
        self.assertEqual(r['state'],'INDETERMINATE');self.assertTrue(r['issues']['documentary'])

    def test_no_graphic_target_does_not_use_text_position(self):
        f=fixture();f['occurrences'][0].update(geometry_sources=[],segments=[],representation_kind='INCONCLUSIVE')
        r=evaluate(f,{'bbox':[0,0,5,5]})['occurrences'][0]
        self.assertEqual(r['state'],'INDETERMINATE');self.assertEqual(r['slabs'],[])


class RealSheetDocumentaryRegressions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root=Path(__file__).resolve().parents[2]
        cls.old=json.loads((root/'analises/lajes_associacao_refinada/inventario.json').read_text(encoding='utf8'))
        cls.new=json.loads((root/'analises/lajes_associacao_documental/inventario.json').read_text(encoding='utf8'))
        cls.a=cls.new['documentary_spatial_assignment'];cls.byid={o['display_id']:o for o in cls.a['occurrences']}

    def test_previous_layers_and_human_interpretations_exactly_preserved(self):
        for k,v in self.old.items():self.assertEqual(self.new[k],v,k)
        self.assertEqual(self.a['human_confirmations'],self.old['refined_slab_assignment']['human_confirmations'])
        self.assertEqual(self.byid['O053']['structural_interpretation']['active_classification'],'LAP_SPLICE')
        for id in ['O034','O035']:self.assertEqual(self.byid[id]['structural_interpretation']['active_classification'],'REINFORCEMENT')

    def test_source_geometries_and_quantities_preserved(self):
        for previous,current in zip(self.old['refined_slab_assignment']['occurrences'],self.a['occurrences']):
            for key in ['segments','geometry_sources','call','text_ids','documentary_mark']:
                self.assertEqual(previous[key],current[key],(current['display_id'],key))

    def test_l605_regressions_including_n37_and_n40(self):
        for id in ['O050','O053','O054','O055','O056','O058','O059']:
            o=self.byid[id];self.assertEqual(o['state'],'RELIABLE',id)
            self.assertEqual(o['slabs'],['L605']);self.assertEqual(o['thickness_options_cm'],[18.0])
            self.assertTrue(o['issues']['topological'])
        n41=self.byid['O057'];self.assertEqual(n41['state'],'PROBABLE')
        self.assertEqual(n41['slabs'],['L605']);self.assertTrue(n41['requires_geometry_review'])
        self.assertEqual(n41['geometry_sources'],[])

    def test_l607_supports_n24_n21_n22(self):
        for id in ['O039','O040','O047']:
            o=self.byid[id];self.assertEqual(o['state'],'RELIABLE')
            self.assertEqual(o['slabs'],['L607']);self.assertEqual(o['thickness_options_cm'],[20.0])
        self.assertEqual(self.byid['O037']['state'],'PROBABLE')
        self.assertEqual(self.byid['O037']['slabs'],['L607'])
        self.assertEqual(self.byid['O038']['state'],'RELIABLE')
        old=next(o for o in self.old['refined_slab_assignment']['occurrences'] if o['display_id']=='O047')
        self.assertEqual(old['slabs'],[]);self.assertTrue(old['segments'])

    def test_context_not_contour_repair_and_all_original_reliable_preserved(self):
        self.assertTrue(all(not c['source_contour_modified'] for c in self.a['contexts']))
        for old in self.old['refined_slab_assignment']['occurrences']:
            if old['state']=='RELIABLE':self.assertEqual(self.byid[old['display_id']]['state'],'RELIABLE')

    def test_determinism_and_color_order_invariance_real(self):
        p=copy.deepcopy(self.old);entries=p['complex_slab_contour_analysis']['linework']
        entries.reverse()
        for e in entries:e['color']=[1,0,1]
        self.assertEqual(analyze(p),self.a)

    def test_comparison_complete_and_no_physical_multi_slab_claim(self):
        self.assertEqual(len(self.a['comparison']),59)
        self.assertEqual(self.a['metrics']['states'],{'RELIABLE':50,'INDETERMINATE':3,'PROBABLE':6})
        self.assertEqual(self.a['metrics']['changed'],16)
        self.assertEqual(self.a['metrics']['multiple_slabs'],0)
        self.assertIn('O054',next(s for s in self.a['slab_index'] if s['slab']=='L605')['occurrences'])


if __name__=='__main__':unittest.main()
