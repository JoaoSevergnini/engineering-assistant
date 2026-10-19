"""Synthetic reasoning tests; real documentary regressions are a separate class."""
import copy
import json
from pathlib import Path
import unittest
from distributed_regions import area,polygon,partition
from structural_regions import (detect_slabs,relate_slabs,coverage,automatic_interpretation,
    fingerprint,consolidate,interpret,roles)


def region(id,b,orientation=0):
    return {'id':id,'bbox':b,'polygon_pdf_pt':polygon(b),'area_pt2':area(b),'orientation':orientation,
        'bar':{'a':[b[0],(b[1]+b[3])/2],'b':[b[2],(b[1]+b[3])/2]},
        'longitudinal_extent_pt':b[2]-b[0],'diameter_mm':8,'spacing_cm':14,'layer':None,
        'position':'N'+id,'occurrence_id':'O'+id,'identity_group':id}


def text(id,value,b):return {'id':id,'text':value,'bbox':b,'direction':[1,0]}


def contour(b):
    p=polygon(b)
    return [{'id':'s'+str(i),'a':a,'b':z} for i,(a,z) in enumerate(zip(p,p[1:]+p[:1]))]


def composition(members,id='cell'):
    b=[max(r['bbox'][0] for r in members),max(r['bbox'][1] for r in members),min(r['bbox'][2] for r in members),min(r['bbox'][3] for r in members)]
    return {'id':id,'bbox':b,'polygon_pdf_pt':polygon(b),'area_pt2':area(b),
        'identity_groups':[r['id'] for r in members],'contributors':members,'occurrences':[r['occurrence_id'] for r in members]}


class SyntheticStructuralTests(unittest.TestCase):
    def test_name_thickness_and_contour(self):
        texts=[text('t','L100',[4,4,6,5]),text('h','h:20',[4,5,6,6])]
        slabs=detect_slabs(texts,contour([0,0,10,10]),[-1,-1,21,21])
        self.assertEqual(slabs[0]['name'],'L100');self.assertEqual(slabs[0]['thickness_cm'],20)
        self.assertEqual(slabs[0]['contour']['bbox'],[0,0,10,10])

    def test_missing_and_competing_contours_stay_pending(self):
        texts=[text('t','L100',[4,4,6,5]),text('h','h:20',[4,5,6,6])]
        self.assertIsNone(detect_slabs(texts,[],[-2,-2,12,12])[0]['contour'])
        lines=contour([0,0,10,10])+contour([-1,-1,11,11])
        self.assertEqual(detect_slabs(texts,lines,[-2,-2,12,12])[0]['contour_state'],'AMBIGUOUS_CONTOURS')

    def test_reinforcement_entity_not_used_as_slab_edge(self):
        labels=[text('t','L100',[4,4,6,5]),text('h','h:20',[4,5,6,6])]
        self.assertIsNone(detect_slabs(labels,contour([0,0,10,10]),[-1,-1,11,11],{'s0'})[0]['contour'])

    def test_crosses_two_slabs_no_proximity_assignment(self):
        slabs=[{'contour':{'bbox':[0,0,5,10]}},{'contour':{'bbox':[5,0,10,10]}}]
        r=region('1',[3,2,8,8]);relate_slabs(slabs,[r])
        self.assertEqual([s['region_relations'][0]['area_pt2'] for s in slabs],[12,18])
        s=[{'contour':None}];relate_slabs(s,[r]);self.assertEqual(s[0]['region_relations'],[])

    def test_covered_by_single_base(self):
        c=coverage(region('r',[1,1,3,3]),[region('b',[0,0,4,4])])
        self.assertEqual(c['state'],'GRAPHICALLY_COVERED');self.assertEqual(c['covered_area_pt2'],4)

    def test_covered_by_union_not_each_base(self):
        c=coverage(region('r',[0,0,10,10]),[region('b1',[0,0,6,10]),region('b2',[4,0,10,10])])
        self.assertEqual(c['covered_area_pt2'],100);self.assertEqual(c['uncovered_area_pt2'],0)

    def test_uncovered_pieces_and_no_base(self):
        c=coverage(region('r',[0,0,10,10]),[region('b',[0,0,6,10])])
        self.assertEqual(c['uncovered_area_pt2'],40)
        self.assertFalse(c['structural_insufficiency_proved'])
        self.assertEqual(coverage(region('r',[0,0,10,10]),[])['state'],'NO_COMPATIBLE_BASE_IDENTIFIED')

    def test_base_reinforcement_proposal_not_confirmation(self):
        rr=[region('1',[0,0,100,100]),region('2',[20,20,60,60])]
        fs={r['id']:{'role_candidate':role} for r,role in zip(rr,['BASE','REINFORCEMENT'])}
        auto=automatic_interpretation(composition(rr),rr,fs)
        self.assertIn('BASE_PLUS_REINFORCEMENT',auto['proposals']);self.assertEqual(auto['classification'],'UNDETERMINED')
        # Words are optional; geometry alone may produce function candidates.
        self.assertEqual({r['role_candidate'] for r in roles(rr,[])},{'BASE','REINFORCEMENT'})

    def test_lap_pattern_not_normative_confirmation(self):
        rr=[region('1',[0,0,100,20]),region('2',[90,0,190,20])]
        auto=automatic_interpretation(composition(rr),rr,{r['id']:{'role_candidate':'UNKNOWN'} for r in rr})
        self.assertIn('LAP_SPLICE',auto['proposals']);self.assertEqual(auto['classification'],'UNDETERMINED')

    def test_residual_requires_multiple_indicators_and_three_members(self):
        rr=[region('1',[0,0,100,100]),region('2',[0,99,100,200]),region('3',[90,0,190,100])]
        auto=automatic_interpretation(composition(rr),rr,{r['id']:{'role_candidate':'UNKNOWN'} for r in rr})
        self.assertIn('GRAPHICAL_RESIDUAL',auto['proposals']);self.assertEqual(auto['classification'],'UNDETERMINED')
        rr=[region('1',[0,0,2,2]),region('2',[0,0,2,2])]
        auto=automatic_interpretation(composition(rr),rr,{r['id']:{'role_candidate':'UNKNOWN'} for r in rr})
        self.assertNotIn('GRAPHICAL_RESIDUAL',auto['proposals'])

    def test_directions_and_unknown_interpretation(self):
        rr=[region('1',[0,0,10,10]),region('2',[0,0,10,10],1)]
        auto=automatic_interpretation(composition(rr),rr,{r['id']:{'role_candidate':'UNKNOWN'} for r in rr})
        self.assertEqual(auto['classification'],'UNDETERMINED');self.assertEqual(auto['proposals'],[])

    def test_fingerprint_ignores_display_id_but_not_geometry(self):
        c=composition([region('1',[0,0,10,10]),region('2',[5,0,15,10])]);d=copy.deepcopy(c);d['id']='changed'
        self.assertEqual(fingerprint(c),fingerprint(d));d['polygon_pdf_pt'][0][0]+=.1
        self.assertNotEqual(fingerprint(c),fingerprint(d))

    def test_consolidation_connected_no_duplicate_no_gap_bridging(self):
        cells=[]
        for i,b in enumerate([[0,0,1,1],[1,0,2,1],[3,0,4,1]]):
            c=composition([region('1',b)],id=str(i));cells.append(c)
        interpretations=[{'composition_id':c['id'],'classification':'SINGLE_DISTRIBUTED','validation_state':'PENDING'} for c in cells]
        merged=consolidate(cells,interpretations)
        self.assertEqual(len(merged),2);self.assertEqual(merged[0]['occurrences'],['O1'])
        self.assertEqual(sum(s['area_pt2'] for s in merged),3)
        self.assertTrue(all(not s['resistant_use_authorized'] for s in merged))


class RealStructuralRegressions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root=Path(__file__).resolve().parents[2]
        cls.prior=json.loads((cls.root/'analises/lajes_regioes_distribuidas/inventario.json').read_text(encoding='utf-8'))
        cls.data=json.loads((cls.root/'analises/lajes_geometria_lideres/entidades_pagina.json').read_text(encoding='utf-8'))
        cls.reviews=json.loads((cls.root/'analises/lajes_interpretacao_estrutural/validacoes_engenheiro.json').read_text(encoding='utf-8'))
        cls.result=interpret(cls.prior,cls.data,cls.reviews);cls.a=cls.result['structural_interpretation']

    def test_stage5_and_n38_preserved(self):
        for k in ('occurrences','distributed_spatial_analysis','stage5_documentary_consistency'):
            self.assertEqual(self.result[k],self.prior[k])

    def test_four_human_examples_and_no_resistant_authorization(self):
        expected={'C059':'BASE_PLUS_REINFORCEMENT','C083':'BASE_PLUS_REINFORCEMENT','C092':'LAP_SPLICE','C073':'GRAPHICAL_RESIDUAL'}
        for i in self.a['overlap_interpretations']:
            if i['composition_id'] in expected:
                self.assertEqual(i['classification'],expected[i['composition_id']]);self.assertEqual(i['validation_state'],'ENGINEER_CONFIRMED')
            self.assertFalse(i['physical_addition_authorized'])
        self.assertEqual(self.a['metrics']['human_confirmations'],4)

    def test_no_ids_hardcoded_and_stale_review_not_applied(self):
        d=copy.deepcopy(self.prior)
        for c in d['distributed_spatial_analysis']['composition_regions']:c['id']='renamed-'+c['id']
        self.assertEqual(interpret(d,self.data,self.reviews)['structural_interpretation']['metrics']['human_confirmations'],4)
        reviews=copy.deepcopy(self.reviews);reviews['reviews'][0]['source_sha256']='wrong-source'
        a=interpret(self.prior,self.data,reviews)['structural_interpretation']
        self.assertEqual(a['metrics']['human_confirmations'],3);self.assertEqual(len(a['unmatched_reviews']),1)

    def test_no_manual_profile_no_automatic_certainty(self):
        a=interpret(self.prior,self.data)['structural_interpretation']
        self.assertEqual(a['metrics']['human_confirmations'],0)
        self.assertEqual(a['metrics']['classifications']['UNDETERMINED'],48)

    def test_conflicting_reviews_remain_pending(self):
        reviews=copy.deepcopy(self.reviews);other=copy.deepcopy(reviews['reviews'][0]);other['classification']='UNDETERMINED';reviews['reviews'].append(other)
        a=interpret(self.prior,self.data,reviews)['structural_interpretation']
        self.assertEqual(a['metrics']['human_confirmations'],3);self.assertEqual(len(a['review_errors']),1)

    def test_geometric_change_invalidates_review(self):
        reviews=copy.deepcopy(self.reviews);reviews['reviews'][0]['fingerprint']='old-geometry'
        self.assertEqual(interpret(self.prior,self.data,reviews)['structural_interpretation']['metrics']['human_confirmations'],3)

    def test_color_invariance(self):
        data=copy.deepcopy(self.data)
        for path in data['paths']:path['color']=[1,0,1];path['fill']=[0,1,0]
        self.assertEqual(interpret(self.prior,data,self.reviews)['structural_interpretation'],self.a)

    def test_labels_and_contours_pending_not_nearest(self):
        self.assertEqual(len(self.a['slabs']),9);self.assertTrue(all(s['thickness_cm'] for s in self.a['slabs']))
        l603=next(s for s in self.a['slabs'] if s['name']=='L603')
        self.assertIsNone(l603['contour']);self.assertEqual(l603['region_relations'],[])

    def test_containment_real_n14_covered_by_union(self):
        checks={c['reinforcement_id']:c for c in self.a['containment_checks']}
        self.assertEqual(checks['R034']['state'],'GRAPHICALLY_COVERED')
        self.assertEqual(checks['R034']['base_region_ids'],['R032','R043'])
        self.assertEqual(checks['R053']['state'],'GRAPHICALLY_UNCOVERED')

    def test_consolidated_coverage_preserves_all_composition_ids(self):
        groups=self.a['consolidated_regions'];ids=[id for g in groups for id in g['composition_ids']]
        self.assertEqual(len(ids),119);self.assertEqual(len(set(ids)),119)
        self.assertAlmostEqual(sum(g['area_pt2'] for g in groups),self.prior['distributed_spatial_analysis']['metrics']['union_area_pt2'])


if __name__=='__main__':unittest.main()
