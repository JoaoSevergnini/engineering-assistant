"""Synthetic interpretation tests and independent frozen real-sheet regressions."""
import copy
import hashlib
import json
from pathlib import Path
import unittest
from polygonal_slabs import Polygon,shape,geo,unary_union
from distributed_regions import partition,polygon
from acting_compositions import analyze,classify_presence,consolidate,query


def region(id,bounds,mark='N1',orientation=0,layer=None):
    x0,y0,x1,y1=bounds
    return {'id':id,'bbox':bounds,'polygon_pdf_pt':polygon(bounds),'occurrence_id':'occ-'+id,'display_id':'O-'+id,
        'position':mark,'orientation':orientation,'layer':layer,'source':{'text_ids':['text-'+id],'text':mark},
        'identity_group':'I-'+id,'reinforcement_role':'POSITIVE_SHEET_CONTEXT',
        'bar':{'a':[x0,(y0+y1)/2],'b':[x1,(y0+y1)/2],'source_ids':['bar-'+id]},
        'distribution_axis':{'a':[(x0+x1)/2,y0],'b':[(x0+x1)/2,y1],'source_ids':['axis-'+id]},
        'longitudinal_extent_pt':x1-x0,'transverse_extent_pt':y1-y0}


def confirmation(r,role):
    return {'region_id':r['id'],'occurrence_id':r['occurrence_id'],'position':r['position'],
        'geometry_sha256':hashlib.sha256(json.dumps(r['polygon_pdf_pt'],sort_keys=True).encode()).hexdigest(),
        'classification':role,'origin':'SYNTHETIC_ENGINEER_CONFIRMATION'}


def fixture(regions,roles=()):
    occurrences=[{'occurrence_id':r['occurrence_id'],'display_id':r['display_id'],'documentary_mark':r['position'],
        'slabs':['L'],'thickness_options_cm':[20],'state':'RELIABLE','actuation_geometry_quality':'SYNTHETIC_ACCEPTED_GEOMETRY',
        'call':{'quantity':4,'nominal_length_cm':100},'geometry_sources':[{'bar':r['bar'],'distribution_axis':r['distribution_axis']}],
        'requires_engineer_decision':False,'requires_geometry_review':False,'context_branch_sources':[],'pending_reasons':[]}
        for r in regions]
    inventory={'stage5_provenance':{'sha256':'synthetic'},
        'documentary_spatial_assignment':{'occurrences':occurrences,'human_confirmations':[]},
        'distributed_spatial_analysis':{'regions':regions,'composition_regions':partition(regions)},
        'structural_interpretation':{'function_candidates':[],'overlap_interpretations':[]}}
    profile={'source_pdf_sha256':'synthetic','records':[confirmation(regions[i],role) for i,role in roles]}
    return inventory,profile


def member(id,role='UNKNOWN',eligible=True):
    return {'id':id,'documentary_role':role,'eligible_for_area_composition':eligible,'layer':None}


class SyntheticActingCompositionTests(unittest.TestCase):
    def test_isolated_base(self):
        p,f=fixture([region('A',[0,0,10,10])],[(0,'BASE')]);a=analyze(p,f)
        self.assertEqual(a['compositions'][0]['classification'],'SINGLE_REINFORCEMENT')

    def test_confirmed_base_reinforcement(self):
        p,f=fixture([region('A',[0,0,10,10]),region('B',[2,2,8,8],'N2')],[(0,'BASE'),(1,'REINFORCEMENT')])
        a=analyze(p,f);joint=[c for c in a['compositions'] if c['classification']=='BASE_PLUS_REINFORCEMENT']
        self.assertEqual(sum(c['area_pt2'] for c in joint),36)
        self.assertTrue(all(not c['physical_addition_authorized'] for c in a['compositions']))

    def test_same_mark_separate_occurrences_not_merged(self):
        p,f=fixture([region('A',[0,0,2,2],'N14'),region('B',[5,0,7,2],'N14')],[(0,'REINFORCEMENT'),(1,'REINFORCEMENT')])
        a=analyze(p,f);self.assertEqual(len(a['consolidated_blocks']),2)
        self.assertEqual(len(a['acting_regions']),2)

    def test_same_mark_overlapping_is_not_identity(self):
        p,f=fixture([region('A',[0,0,4,4]),region('B',[2,0,6,4])]);a=analyze(p,f)
        self.assertTrue(any(c['classification']=='UNRESOLVED_COMPOSITION' for c in a['compositions']))

    def test_documentary_lap_unknown_zone_never_reinforcement(self):
        p,f=fixture([region('A',[0,0,10,10]),region('B',[8,0,12,10],'N2')],[(1,'LAP_SPLICE')])
        a=analyze(p,f)
        for c in a['compositions']:
            if 'B' in c['region_ids']:
                self.assertEqual(c['classification'],'UNRESOLVED_COMPOSITION')
                self.assertTrue(c['independent_addition_blocked']);self.assertIsNone(c['effective_resistant_contributors'])

    def test_local_confirmed_lap_classification(self):
        m=[member('A'),member('B')]
        r=classify_presence(m,manual={'classification':'LAP_SPLICE','scope':'EXACT_TEST_CELL'})
        self.assertEqual(r['classification'],'LAP_SPLICE');self.assertFalse(r['physical_addition_authorized'])

    def test_external_slab_context_does_not_clip_region(self):
        p,f=fixture([region('A',[-4,-4,20,20])]);p['candidate_slab_domain_not_used']=[0,0,10,10]
        a=analyze(p,f);self.assertEqual(a['acting_regions'][0]['original_polygon_pdf_pt'],polygon([-4,-4,20,20]))

    def test_directions_and_layers_separate(self):
        for kwargs in [{'orientation':1},{'layer':'UPPER'}]:
            p,f=fixture([region('A',[0,0,10,10],layer='LOWER'),region('B',[0,0,10,10],'N2',**kwargs)])
            a=analyze(p,f);self.assertEqual(len(a['compositions']),2)
            self.assertTrue(all(len(c['region_ids'])==1 for c in a['compositions']))
            self.assertTrue(all(c['other_direction_region_ids'] for c in a['compositions']))

    def test_reliable_slab_with_inconclusive_geometry_not_promoted(self):
        p,f=fixture([region('A',[0,0,10,10])]);p['documentary_spatial_assignment']['occurrences'][0]['requires_geometry_review']=True
        a=analyze(p,f);self.assertFalse(a['acting_regions'][0]['eligible_for_area_composition'])
        self.assertEqual(a['compositions'][0]['classification'],'UNRESOLVED_COMPOSITION')

    def test_probable_association_not_promoted_even_with_area(self):
        p,f=fixture([region('A',[0,0,10,10])]);p['documentary_spatial_assignment']['occurrences'][0]['state']='PROBABLE'
        a=analyze(p,f);self.assertEqual(a['metrics']['eligible_area_regions'],0)

    def test_multiple_reinforcements_need_explicit_complete_joint_set(self):
        members=[member('A'),member('B'),member('C')]
        self.assertEqual(classify_presence(members)['classification'],'UNRESOLVED_COMPOSITION')
        joint={'id':'explicit','members':['A','B','C'],'classification':'MULTIPLE_REINFORCEMENTS','origin':'SYNTHETIC_EXPLICIT_CONFIRMATION'}
        self.assertEqual(classify_presence(members,[joint])['classification'],'MULTIPLE_REINFORCEMENTS')
        joint['members']=['A','B']
        self.assertEqual(classify_presence(members,[joint])['classification'],'UNRESOLVED_COMPOSITION')

    def test_confirmed_subset_does_not_confirm_third_member(self):
        p,f=fixture([region('A',[0,0,10,10]),region('B',[2,2,8,8],'N2'),region('C',[3,3,7,7],'N3')],[(0,'BASE'),(1,'REINFORCEMENT')])
        triple=next(c for c in analyze(p,f)['compositions'] if len(c['region_ids'])==3)
        self.assertEqual(triple['classification'],'UNRESOLVED_COMPOSITION');self.assertTrue(triple['supported_joint_sets'])

    def test_two_bases_cover_reinforcement_without_global_addition(self):
        p,f=fixture([region('A',[0,0,5,10]),region('B',[5,0,10,10],'N2'),region('C',[2,2,8,8],'N3')],[(0,'BASE'),(1,'BASE'),(2,'REINFORCEMENT')])
        a=analyze(p,f)
        self.assertEqual(len(a['documentary_joint_relations']),2)
        self.assertTrue(all(len(c['region_ids'])==2 for c in a['compositions'] if c['classification']=='BASE_PLUS_REINFORCEMENT'))

    def test_human_conflict_not_silently_overwritten(self):
        r=classify_presence([member('A','LAP_SPLICE'),member('B')],manual={'classification':'BASE_PLUS_REINFORCEMENT'})
        self.assertEqual(r['classification'],'UNRESOLVED_COMPOSITION')
        self.assertEqual(r['manual_classification_preserved']['classification'],'BASE_PLUS_REINFORCEMENT')

    def test_stale_role_geometry_rejected(self):
        p,f=fixture([region('A',[0,0,10,10])],[(0,'BASE')]);f['records'][0]['geometry_sha256']='stale'
        with self.assertRaises(ValueError):analyze(p,f)

    def test_order_color_and_inputs_unchanged(self):
        p,f=fixture([region('A',[0,0,10,10]),region('B',[2,2,8,8],'N2')],[(0,'BASE'),(1,'REINFORCEMENT')]);before=copy.deepcopy(p)
        a=analyze(p,f);self.assertEqual(p,before)
        p['distributed_spatial_analysis']['regions'].reverse();p['distributed_spatial_analysis']['composition_regions'].reverse()
        for r in p['distributed_spatial_analysis']['regions']:r['color']='ignored'
        self.assertEqual(a,analyze(p,f))


class RealSheetActingCompositionRegressions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root=Path(__file__).resolve().parents[2];out=root/'analises/lajes_composicao_atuacao'
        cls.old=json.loads((root/'analises/lajes_associacao_documental/inventario.json').read_text(encoding='utf8'))
        cls.new=json.loads((out/'inventario.json').read_text(encoding='utf8'));cls.a=cls.new['acting_composition_analysis']
        cls.profile=json.loads((out/'confirmacoes_engenheiro.json').read_text(encoding='utf8'))
        cls.cells={c['source_composition_id']:c for c in cls.a['compositions']}

    def test_all_previous_layers_exactly_preserved(self):
        for k,v in self.old.items():self.assertEqual(self.new[k],v,k)

    def test_35_regions_and_119_cells_exact_original_points(self):
        regions={r['id']:r for r in self.a['acting_regions']}
        for r in self.old['distributed_spatial_analysis']['regions']:
            self.assertEqual(regions[r['id']]['original_polygon_pdf_pt'],r['polygon_pdf_pt'])
        for c in self.old['distributed_spatial_analysis']['composition_regions']:
            self.assertEqual(self.cells[c['id']]['original_polygon_pdf_pt'],c['polygon_pdf_pt'])
        self.assertEqual(len(self.cells),119)

    def test_n13_n14_left_right_and_third_positions(self):
        self.assertEqual(self.cells['C083']['classification'],'BASE_PLUS_REINFORCEMENT')
        self.assertEqual(self.cells['C088']['classification'],'BASE_PLUS_REINFORCEMENT')
        self.assertNotEqual(self.cells['C083']['region_ids'],self.cells['C088']['region_ids'])
        for id in ['C071','C076']:
            self.assertEqual(self.cells[id]['classification'],'UNRESOLVED_COMPOSITION')
            self.assertTrue(self.cells[id]['supported_joint_sets'])
        self.assertTrue(all(r['isolated_base_area_pt2']>0 for r in self.a['base_reinforcement_comparison']))

    def test_n40_lap_not_additional_reinforcement(self):
        r=next(r for r in self.a['acting_regions'] if r['id']=='R053');self.assertEqual(r['documentary_role'],'LAP_SPLICE')
        for c in self.a['compositions']:
            if 'R053' in c['region_ids']:
                self.assertEqual(c['classification'],'UNRESOLVED_COMPOSITION')
                self.assertTrue(c['independent_addition_blocked']);self.assertFalse(c['physical_addition_authorized'])
        self.assertEqual(self.cells['C092']['classification'],'LAP_SPLICE')

    def test_localized_l607_no_fictitious_area_and_n24_full_extent(self):
        byid={r['display_id']:r for r in self.a['acting_regions']}
        for id in ['O039','O040','O038']:
            self.assertEqual(byid[id]['kind'],'LOCALIZED_TRACES_ONLY')
            self.assertEqual(shape(byid[id]['geometry_pdf_pt']).area,0)
            self.assertFalse(byid[id]['eligible_for_area_composition'])
        self.assertTrue(byid['O047']['eligible_for_area_composition'])
        self.assertFalse(byid['O047']['slab_contours_used_for_clipping'])

    def test_nine_previous_pending_never_promoted(self):
        pending=self.a['previous_pending_occurrences'];self.assertEqual(len(pending),9)
        for r in self.a['acting_regions']:
            if r['display_id'] in pending:
                self.assertFalse(r['eligible_for_area_composition']);self.assertIsNone(r['geometry_pdf_pt'])
        self.assertEqual(self.a['metrics']['localized_trace_only'],15)

    def test_query_real_cell_and_boundary(self):
        c=self.cells['C088'];g=shape(c['geometry_pdf_pt']);p=g.representative_point()
        hit=query(self.a,p.x,p.y)['compositions'];self.assertEqual([i['source_composition_id'] for i in hit],['C088'])
        self.assertEqual(set(hit[0]['positions']),{'N13','N14'})
        x,y=g.exterior.coords[0]
        self.assertGreaterEqual(len(query(self.a,x,y)['compositions']),1)

    def test_preserved_human_residual_not_promoted(self):
        c=self.cells['C073'];self.assertEqual(c['classification'],'UNRESOLVED_COMPOSITION')
        self.assertEqual(c['manual_classification_preserved']['classification'],'GRAPHICAL_RESIDUAL')

    def test_consolidation_preserves_union_and_all_references(self):
        self.assertEqual({id for b in self.a['consolidated_blocks'] for id in b['composition_ids']},{c['id'] for c in self.a['compositions']})
        expected=unary_union([shape(c['geometry_pdf_pt']) for c in self.a['compositions']])
        actual=unary_union([shape(b['geometry_pdf_pt']) for b in self.a['consolidated_blocks']])
        self.assertTrue(actual.equals(expected))

    def test_reexecution_stable_ids_and_no_addition(self):
        self.assertEqual(analyze(self.old,self.profile),self.a)
        self.assertTrue(all(not c['physical_addition_authorized'] for c in self.a['compositions']))
        self.assertTrue(all(not c['resistance_quantities_computed'] for c in self.a['compositions']))


if __name__=='__main__':unittest.main()
