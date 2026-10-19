"""Synthetic scoped hyperedges/topology; real-sheet regressions below separately."""
import copy
import json
from pathlib import Path
import unittest
from unittest.mock import patch
from distributed_regions import partition,polygon,area
from polygonal_slabs import (Polygon,box,shape,geo,polygon_candidates,normalized_topology,
                             reconstruct_slabs,excluded_entities)
from occurrence_relations import relation,propagate,build_relations,analyze_relations,consolidate_relations
from structural_regions import coverage


def region(id,b,mark=None):
    return {'id':id,'bbox':b,'polygon_pdf_pt':polygon(b),'area_pt2':area(b),'identity_group':id,
        'occurrence_id':'physical-not-proved-'+id,'display_id':'O'+id,'position':mark or 'N'+id,'orientation':0,'layer':None}


def cells_of(regions):
    cells=partition(regions);lookup={r['id']:r for r in regions}
    for c in cells:
        c['identity_groups']=[lookup[id]['identity_group'] for id in c['region_ids']]
        c['occurrences']=[lookup[id]['display_id'] for id in c['region_ids']]
    previous=[{'composition_id':c['id'],'classification':'UNDETERMINED' if len(c['region_ids'])>1 else 'SINGLE_DISTRIBUTED','validation_state':'PENDING'} for c in cells]
    return cells,previous,lookup


def lines(ring,prefix='s'):
    return [{'id':prefix+str(i),'a':a,'b':b,'basis':'SYNTHETIC_DOCUMENTED_BOUNDARY'} for i,(a,b) in enumerate(zip(ring,ring[1:]+ring[:1]))]


def slab(id,name,b):
    return {'id':id,'name':name,'label':{'id':id,'text':name,'bbox':b},'thickness_cm':20,'thickness_sources':['h'+id],'documentary_state':'NAME_AND_THICKNESS_EXTRACTED','contour_alternatives':[]}


class SyntheticRelationTests(unittest.TestCase):
    def test_reinforces_single_base_with_explicit_domain(self):
        rr=[region('a',[0,0,10,10]),region('r',[2,2,8,8])];cells,prior,lookup=cells_of(rr)
        rel=relation('REINFORCES',['a','r'],box(2,2,8,8),{'source':'synthetic engineer review'},'ENGINEER_CONFIRMED_LOCAL_SCOPE',reinforcement='r',bases=['a'],meaning='BASE_PLUS_REINFORCEMENT')
        result=propagate(cells,[rel],prior,lookup)
        self.assertEqual(sum(i['classification']=='BASE_PLUS_REINFORCEMENT' for i in result),1)

    def test_hyperedge_two_bases_active_members_per_subregion(self):
        rr=[region('a',[0,0,5,10]),region('b',[5,0,10,10]),region('r',[2,2,8,8])];cells,prior,lookup=cells_of(rr)
        rel=relation('REINFORCES',['a','b','r'],box(2,2,8,8),{},'ENGINEER_CONFIRMED_LOCAL_SCOPE',reinforcement='r',bases=['a','b'],meaning='BASE_PLUS_REINFORCEMENT')
        result=propagate(cells,[rel],prior,lookup);applicable=[i for i in result if i['classification']=='BASE_PLUS_REINFORCEMENT']
        self.assertEqual(len(applicable),2)
        self.assertTrue(all(len(i['relations'][0]['active_region_ids'])==2 for i in applicable))
        self.assertEqual(coverage(rr[2],rr[:2])['uncovered_area_pt2'],0)

    def test_lap_no_independent_addition(self):
        rr=[region('a',[0,0,10,5]),region('b',[8,0,18,5])];cells,prior,lookup=cells_of(rr)
        rel=relation('LAPS_WITH',['a','b'],box(8,0,10,5),{},'ENGINEER_CONFIRMED_LOCAL_SCOPE',meaning='LAP_SPLICE')
        result=propagate(cells,[rel],prior,lookup)
        self.assertEqual(sum(i['classification']=='LAP_SPLICE' for i in result),1)
        self.assertTrue(all(not i['physical_addition_authorized'] for i in result))

    def test_residual_hyperedge_three_occurrences(self):
        rr=[region('a',[0,0,10,10]),region('b',[0,0,10,10]),region('c',[0,0,10,10])];cells,prior,lookup=cells_of(rr)
        rel=relation('GRAPHICAL_INTERSECTION',['a','b','c'],box(0,0,10,10),{},'ENGINEER_CONFIRMED_LOCAL_SCOPE',meaning='GRAPHICAL_RESIDUAL')
        self.assertEqual(propagate(cells,[rel],prior,lookup)[0]['classification'],'GRAPHICAL_RESIDUAL')

    def test_partial_scope_does_not_classify_whole_cell(self):
        rr=[region('a',[0,0,10,10]),region('b',[0,0,10,10])];cells,prior,lookup=cells_of(rr)
        rel=relation('LAPS_WITH',['a','b'],box(0,0,5,10),{},'ENGINEER_CONFIRMED_LOCAL_SCOPE',meaning='LAP_SPLICE')
        r=propagate(cells,[rel],prior,lookup)[0]
        self.assertEqual(r['classification'],'UNDETERMINED');self.assertFalse(r['relations'][0]['full_cell'])

    def test_conflict_does_not_change_old_human_review(self):
        rr=[region('a',[0,0,10,10]),region('b',[0,0,10,10])];cells,prior,lookup=cells_of(rr)
        prior[0].update(classification='BASE_PLUS_REINFORCEMENT',validation_state='ENGINEER_CONFIRMED');saved=copy.deepcopy(prior)
        rel=relation('LAPS_WITH',['a','b'],box(0,0,10,10),{},'ENGINEER_CONFIRMED_LOCAL_SCOPE',meaning='LAP_SPLICE')
        result=propagate(cells,[rel],prior,lookup)[0]
        self.assertEqual(result['classification'],'UNDETERMINED');self.assertTrue(result['conflicts']);self.assertEqual(prior,saved)

    def test_no_transitivity_or_mark_based_propagation(self):
        rr=[region('a',[0,0,10,10],'N1'),region('b',[0,0,10,10],'N2'),region('c',[0,0,10,10],'N1')];cells,prior,lookup=cells_of(rr)
        rel=relation('REINFORCES',['a','b'],box(0,0,10,10),{},reinforcement='a',bases=['b'],meaning='BASE_PLUS_REINFORCEMENT')
        lap=relation('LAPS_WITH',['b','c'],box(0,0,10,10),{},meaning='LAP_SPLICE')
        r=propagate(cells,[rel,lap],prior,lookup)[0]
        self.assertEqual(r['relations'][0]['active_region_ids'],['a','b']);self.assertEqual(r['classification'],'UNDETERMINED')
        self.assertEqual([r['active_region_ids'] for r in r['relations']],[['a','b'],['b','c']])

    def test_shared_physical_identity_requires_specific_review(self):
        with self.assertRaises(ValueError):relation('SAME_PHYSICAL_REPRESENTATION',['a','b'],box(0,0,10,10),{},'ENGINEER_CONFIRMED_LOCAL_SCOPE')
        r=relation('SAME_PHYSICAL_REPRESENTATION',['a','b'],box(0,0,10,10),{'physical_identity_evidence':'synthetic explicit engineer review of duplicated raw representation'},'ENGINEER_CONFIRMED_LOCAL_SCOPE')
        self.assertIsNotNone(r['shared_physical_identity_id']);self.assertFalse(r['physical_addition_authorized'])

    def test_incompatible_layers_block_confirmation(self):
        rr=[region('a',[0,0,10,10]),region('b',[0,0,10,10])];rr[0]['layer']='LOWER';rr[1]['layer']='UPPER';cells,prior,lookup=cells_of(rr)
        rel=relation('LAPS_WITH',['a','b'],box(0,0,10,10),{},'ENGINEER_CONFIRMED_LOCAL_SCOPE',meaning='LAP_SPLICE')
        r=propagate(cells,[rel],prior,lookup)[0];self.assertEqual(r['classification'],'UNDETERMINED');self.assertTrue(r['conflicts'])

    def test_incompatible_orientation_is_a_conflict_not_silent_omission(self):
        rr=[region('a',[0,0,10,10]),region('b',[0,0,10,10])];rr[1]['orientation']=1;cells,prior,lookup=cells_of(rr)
        rel=relation('LAPS_WITH',['a','b'],box(0,0,10,10),{},'ENGINEER_CONFIRMED_LOCAL_SCOPE',meaning='LAP_SPLICE')
        result=propagate(cells,[rel],prior,lookup)[0]
        self.assertEqual(result['classification'],'UNDETERMINED');self.assertEqual(result['conflicts'][0]['reason'],'KNOWN_INCOMPATIBLE_ORIENTATIONS')

    def test_consolidation_no_disconnected_merge(self):
        rr=[region('a',[0,0,1,1]),region('b',[3,0,4,1])];cells,prior,lookup=cells_of(rr)
        result=propagate(cells,[],prior,lookup);groups=consolidate_relations(cells,result,[],lookup)
        self.assertEqual(len(groups),2);self.assertEqual(sum(g['area_pt2'] for g in groups),2)


class SyntheticPolygonTests(unittest.TestCase):
    def test_nonrectangular_slab_polygon(self):
        ring=[[0,0],[4,0],[4,1],[1,1],[1,4],[0,4]]
        c,d=polygon_candidates(lines(ring),[slab('t','L1',[.1,2,.8,3])])
        self.assertEqual(len(c),1);self.assertEqual(c[0]['area_pt2'],7);self.assertEqual(len(c[0]['geometry_pdf_pt']['coordinates'][0]),7)

    def test_hole_is_preserved_as_graphic_ring(self):
        outer=lines(polygon([0,0,10,10]));inner=lines(polygon([4,4,6,6]),'h')
        c,d=polygon_candidates(outer+inner,[slab('t','L1',[1,1,2,2])])
        self.assertEqual(len(c),1);self.assertEqual(c[0]['area_pt2'],96)
        self.assertEqual(shape(c[0]['geometry_pdf_pt']).intersection(box(4,4,6,6)).area,0)
        self.assertEqual(c[0]['interior_ring_state'],'GRAPHIC_RING_NOT_PROVED_STRUCTURAL_OPENING')

    def test_closed_region_without_slab_evidence_not_identified(self):
        c,d=polygon_candidates(lines(polygon([0,0,10,10])),[]);self.assertEqual(c,[])
        weak=lines(polygon([0,0,10,10]))
        for e in weak:e['basis']='UNCLASSIFIED_ORTHOGONAL_LINE_AFTER_ANNOTATION_EXCLUSION'
        c,d=polygon_candidates(weak,[slab('t','L1',[1,1,2,2])]);self.assertEqual(c,[])

    def test_external_label_requires_actual_connector(self):
        contour=lines(polygon([0,0,10,10]));label=slab('t','L1',[4,11,6,12])
        self.assertEqual(polygon_candidates(contour,[label])[0],[])
        link=[{'id':'pointer','a':[5,9],'b':[5,11.5]}]
        c,d=polygon_candidates(contour,[label],connectors=link)
        self.assertEqual(len(c),1);self.assertEqual(c[0]['label_evidence'][0]['basis'],'EXPLICIT_LABEL_CONNECTOR_INTO_FACE')

    def test_contour_competition_not_selected_by_area(self):
        labels=[slab('t','L1',[1,1,2,2])]
        # Retain old independent alternative; topology must not overwrite it.
        labels[0]['contour_alternatives']=[{'bbox':[-1,-1,11,11],'polygon_pdf_pt':polygon([-1,-1,11,11]),'edge_evidence':[]}]
        inv={'structural_interpretation':{'slabs':labels},'layout':{'detail_roi_pt':[-2,-2,12,12]},'occurrences':[],
             'distributed_spatial_analysis':{'regions':[],'composition_regions':[]}}
        with patch('polygonal_slabs.boundary_evidence',return_value=lines(polygon([0,0,10,10]))):
            result=reconstruct_slabs(inv,{'segments':[]})
        self.assertEqual(result['slabs'][0]['contour_state'],'COMPETING_CANDIDATES')

    def test_occurrence_crosses_two_preliminary_slabs(self):
        labels=[slab('a','L1',[1,1,2,2]),slab('b','L2',[6,1,7,2])]
        rr=[region('r',[3,1,8,4])];inv={'structural_interpretation':{'slabs':labels},'layout':{'detail_roi_pt':[-1,-1,11,6]},'occurrences':[],
             'distributed_spatial_analysis':{'regions':rr,'composition_regions':[]}}
        with patch('polygonal_slabs.boundary_evidence',return_value=lines(polygon([0,0,5,5]))+lines(polygon([5,0,10,5]),'b')):
            a=reconstruct_slabs(inv,{'segments':[]})
        self.assertEqual(len(a['crossing_occurrences']),1)
        self.assertEqual(sum(h['area_pt2'] for s in a['slabs'] for h in s['region_relations']),15)

    def test_no_source_coordinate_changes_and_determinism(self):
        l=lines(polygon([0,0,10,10]));saved=copy.deepcopy(l);l[0]['b'][0]+=.0001
        norm,moves=normalized_topology(l)
        self.assertTrue(moves);self.assertEqual(l[0]['b'][0],10.0001)
        label=[slab('t','L1',[1,1,2,2])]
        self.assertEqual(polygon_candidates(saved,label),polygon_candidates(list(reversed(saved)),label))


class RealRelationRegressions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root=Path(__file__).resolve().parents[2]
        cls.prior=json.loads((cls.root/'analises/lajes_interpretacao_estrutural/inventario.json').read_text(encoding='utf-8'))
        cls.data=json.loads((cls.root/'analises/lajes_geometria_lideres/entidades_pagina.json').read_text(encoding='utf-8'))
        cls.result=analyze_relations(cls.prior,cls.data);cls.a=cls.result['occurrence_relation_analysis']

    def test_all_prior_layers_n38_and_geometry_preserved(self):
        for k,v in self.prior.items():self.assertEqual(self.result[k],v)

    def test_four_local_confirmations_no_unjustified_extension(self):
        confirmed=[r for r in self.a['relations'] if r['state']=='ENGINEER_CONFIRMED_LOCAL_SCOPE']
        self.assertEqual(len(confirmed),4)
        self.assertEqual({r['evidence']['confirmed_composition_id'] for r in confirmed},{'C059','C083','C073','C092'})
        self.assertEqual(self.a['metrics']['undetermined_compositions'],44)
        self.assertEqual(self.a['metrics']['newly_interpreted_by_propagation'],0)

    def test_multiple_bases_and_n40_not_structural_error(self):
        rel=next(r for r in self.a['relations'] if r['type']=='REINFORCES' and r['reinforcement']=='R034' and r['state']=='AUTOMATIC_CANDIDATE')
        self.assertEqual(rel['bases'],['R032','R043'])
        n40=next(c for c in self.a['containment_checks'] if c['reinforcement_id']=='R053')
        self.assertFalse(n40['function_confirmed']);self.assertFalse(n40['structural_insufficiency_proved']);self.assertGreater(n40['uncovered_area_pt2'],0)

    def test_same_mark_not_same_physical_representations(self):
        self.assertFalse(any(r['type']=='SAME_PHYSICAL_REPRESENTATION' for r in self.a['relations']))
        self.assertTrue(any(r['type']=='UNDETERMINED' and r['evidence']['same_documentary_mark'] for r in self.a['relations']))

    def test_synthetic_duplicate_of_real_occurrence_needs_specific_evidence(self):
        d=copy.deepcopy(self.prior);r=copy.deepcopy(d['distributed_spatial_analysis']['regions'][0]);r.update(id='R999',occurrence_id='synthetic-duplicate',display_id='O999');d['distributed_spatial_analysis']['regions'].append(r)
        duplicates=[r for r in build_relations(d) if r['type']=='SAME_PHYSICAL_REPRESENTATION']
        self.assertEqual(len(duplicates),1);self.assertEqual(duplicates[0]['state'],'AUTOMATIC_CANDIDATE');self.assertIn('specific_evidence',duplicates[0]['evidence'])

    def test_color_invariance_relation_determinism_without_reusing_classifications(self):
        d=copy.deepcopy(self.prior)
        for r in d['distributed_spatial_analysis']['regions']:r['bar']['color']=[1,0,1];r['distribution_axis']['color']=[0,1,0]
        # IDs are based on relevant evidence; source colors are not identity evidence.
        result=build_relations(d)
        self.assertEqual([(r['type'],r['members'],r['validity_geometry_pdf_pt']) for r in result],
                         [(r['type'],r['members'],r['validity_geometry_pdf_pt']) for r in self.a['relations']])

    def test_all_119_cells_retained_and_no_physical_addition(self):
        ids=[id for g in self.a['consolidated_regions'] for id in g['composition_ids']]
        self.assertEqual(len(ids),119);self.assertEqual(len(set(ids)),119)
        self.assertTrue(all(not i['physical_addition_authorized'] for i in self.a['interpreted_compositions']))

    def test_real_l605_border_face_not_automatically_assigned_as_slab(self):
        s=next(s for s in self.a['slab_reconstruction']['slabs'] if s['name']=='L605')
        self.assertEqual(s['contour_state'],'BORDER_OR_BEAM_FACE_REVIEW_REQUIRED');self.assertIsNone(s['selected_candidate_id'])
        self.assertTrue(s['contour_candidates'][0]['border_or_beam_face_review_required'])


if __name__=='__main__':unittest.main()
