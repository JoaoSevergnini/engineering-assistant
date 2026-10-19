"""Synthetic stage 4 tests: geometry evidence and explicit convention boundaries."""
import copy
import json
from pathlib import Path
import unittest
from automatic import parse_extended
from opening_groups import recognize_openings,reconstruct_localized
from test_geometry import segment


def hole(x0=20,y0=20,x1=40,y1=40,prefix='H'):
    points=[[x0,y0],[x1,y0],[x1,y1],[x0,y1]]
    edges=[segment(prefix+str(i),a,b) for i,(a,b) in enumerate(zip(points,points[1:]+points[:1]))]
    return edges+[segment(prefix+'X1',points[0],points[2]),segment(prefix+'X2',points[1],points[3])]


def fixture(horizontal=False,factors='2x3'):
    bars=[segment('L1',[15,10],[15,50]),segment('L2',[17,10],[17,50]),
          segment('R1',[43,10],[43,50]),segment('R2',[45,10],[45,50]),
          segment('T1',[10,15],[50,15]),segment('T2',[10,17],[50,17]),
          segment('B1',[10,43],[50,43]),segment('B2',[10,45],[50,45])]
    text=f'N6 {factors} Ø 12.5 C=100'
    targeted=['T1','T2'] if horizontal else ['L1','L2']
    o=dict(occurrence_id='P1-T1',display_id='O001',documentary_mark='N6',text=text,text_ids=['T1'],
           call=parse_extended(text),representation_kind='LOCALIZED',status='ASSOCIATED',
           associated_lines=[s for s in bars if s['id'] in targeted],leader_association=dict(trace=dict(segments=[],segment_ids=[],tip=[15,25])))
    stage3=dict(provenance=dict(sha256='fixture'),layout=dict(detail_roi_pt=[0,0,100,100],scale_denominator=50),occurrences=[o])
    data=dict(segments=hole()+bars,paths=[],texts=[])
    profile=json.loads((Path(__file__).parent/'conventions/sim_opening_edge_v1.json').read_text(encoding='utf-8'))
    profile['source_pdf_sha256']='fixture'
    return stage3,data,profile


class SyntheticOpeningGroupTests(unittest.TestCase):
    def read(self,s,d,p):return reconstruct_localized(s,d,p)['localized_reconstruction']

    def test_rectangular_opening_contour_x_and_collar(self):
        s,d,p=fixture();r=recognize_openings(d,[0,0,100,100])
        self.assertEqual(len(r['openings']),1)
        h=r['openings'][0];self.assertEqual(h['bbox'],[20,20,40,40])
        self.assertEqual(len(h['diagonal_ids']),2);self.assertTrue(all(e['complete'] for e in h['edge_evidence']))

    def test_rectangle_or_rectangle_x_alone_not_opening(self):
        r=recognize_openings(dict(segments=hole(),paths=[]),[0,0,100,100])
        self.assertEqual(r['openings'],[]);self.assertEqual(len(r['candidates']),1)
        r=recognize_openings(dict(segments=hole()[:4],paths=[]),[0,0,100,100]);self.assertEqual(r['openings'],[])

    def test_two_opposite_vertical_groups_and_sim_layers(self):
        s,d,p=fixture();r=self.read(s,d,p)
        self.assertEqual(len(r['physical_groups']),2)
        self.assertEqual({g['opening_relations'][0]['side'] for g in r['physical_groups']},{'LEFT','RIGHT'})
        for g in r['physical_groups']:
            self.assertEqual(g['quantity_bars'],3);self.assertEqual(len(g['lines']),2)
            self.assertEqual((g['layer_distribution']['lower'],g['layer_distribution']['upper']),(2,1))
            self.assertEqual(g['orientation'],'VERTICAL')

    def test_horizontal_groups(self):
        s,d,p=fixture(True);r=self.read(s,d,p)
        self.assertEqual({g['opening_relations'][0]['side'] for g in r['physical_groups']},{'TOP','BOTTOM'})
        self.assertTrue(all(g['orientation']=='HORIZONTAL' for g in r['physical_groups']))

    def test_repeated_calls_share_groups(self):
        s,d,p=fixture();other=copy.deepcopy(s['occurrences'][0]);other.update(occurrence_id='P1-T2',display_id='O002')
        s['occurrences'].append(other);r=self.read(s,d,p)
        self.assertEqual(len(r['representations']),2);self.assertEqual(len(r['physical_groups']),2)
        self.assertTrue(all(g['representation_ids']==['P1-T1','P1-T2'] for g in r['physical_groups']))

    def test_one_call_has_multiple_groups(self):
        s,d,p=fixture();r=self.read(s,d,p)
        self.assertEqual(len(r['representations'][0]['group_ids']),2)
        self.assertEqual(r['representations'][0]['multiplicity']['unlocated_group_count'],0)

    def test_6x3_not_expanded_or_given_layers(self):
        s,d,p=fixture(factors='6x3');r=self.read(s,d,p)
        self.assertEqual(len(r['physical_groups']),1)
        g=r['physical_groups'][0];self.assertIsNone(g['quantity_bars']);self.assertIsNone(g['layer_distribution']['lower'])
        m=r['representations'][0]['multiplicity'];self.assertEqual(m['original_factors'],[6,3]);self.assertEqual(m['printed_total'],18)
        self.assertIsNone(m['indicated_group_count']);self.assertIsNone(m['unlocated_group_count'])

    def test_no_applicable_detail_keeps_layers_unknown(self):
        s,d,p=fixture();r=self.read(s,d,None)
        self.assertEqual(len(r['physical_groups']),1);self.assertIsNone(r['physical_groups'][0]['layer_distribution']['upper'])
        p['office']='Other office';r=self.read(s,d,p)
        self.assertFalse(r['convention_scope']['confirmed']);self.assertEqual(len(r['physical_groups']),1)

    def test_missing_opposite_group_is_not_fabricated(self):
        s,d,p=fixture();d['segments']=[x for x in d['segments'] if x['id'] not in ('R1','R2')]
        r=self.read(s,d,p);self.assertEqual(len(r['physical_groups']),1)
        record=r['representations'][0];self.assertEqual(record['multiplicity']['unlocated_group_count'],1)
        self.assertEqual(record['reconstruction_state'],'PARTIAL')
        self.assertEqual(r['physical_groups'][0]['quantity_bars'],3)

    def test_ambiguous_opening_not_nearest_choice(self):
        s,d,p=fixture();s['occurrences'][0]['associated_lines']=[x for x in d['segments'] if x['id'] in ('R1','R2')]
        d['segments']+=hole(50,20,70,40,'H2')+[segment('R3',[73,10],[73,50]),segment('R4',[75,10],[75,50])]
        r=self.read(s,d,p);g=r['physical_groups'][0]
        self.assertEqual(g['opening_association_state'],'AMBIGUOUS')
        self.assertEqual(len(g['opening_alternatives']),2);self.assertEqual(g['opening_relations'],[])
        self.assertIsNone(g['layer_distribution']['lower'])

    def test_specific_detail_conflict_retained_and_blocks_layers(self):
        s,d,p=fixture();p['specific_overrides']={'P1-T1':dict(source='specific detail',lower=3,upper=0)}
        r=self.read(s,d,p)
        self.assertIn('SPECIFIC_DETAIL_CONFLICT_REQUIRES_REVIEW',r['representations'][0]['issues'])
        self.assertEqual(len(r['physical_groups']),1)
        self.assertEqual(len(r['representations'][0]['candidate_opposite_pairs']),1)
        for g in r['physical_groups']:
            self.assertIsNone(g['layer_distribution']['upper'])
            self.assertEqual(g['evidence_state'],'CONFLICTING_REQUIRES_ENGINEER_REVIEW')
            self.assertEqual(g['issues'][0]['evidence']['lower'],3)

    def test_all_stage3_representations_and_distributed_unchanged(self):
        s,d,p=fixture();s['occurrences'].append(dict(representation_kind='DISTRIBUTED',status='ASSOCIATED',region_pdf_pt=[[1,2],[3,4]]))
        before=copy.deepcopy(s);r=reconstruct_localized(s,d,p)
        self.assertEqual(s,before);self.assertEqual(r['occurrences'],s['occurrences'])

    def test_single_group_quantity_from_text_layers_from_convention(self):
        s,d,p=fixture(factors='3');r=self.read(s,d,None)
        self.assertEqual(r['physical_groups'][0]['quantity_bars'],3);self.assertIsNone(r['physical_groups'][0]['layer_distribution']['lower'])
        r=self.read(s,d,p);self.assertEqual(len(r['physical_groups']),1)
        self.assertEqual(r['physical_groups'][0]['layer_distribution']['lower'],2)
        self.assertEqual(r['physical_groups'][0]['quantity_origin'],'EXPLICIT_SINGLE_GROUP_CALL')

    def test_unrecognized_cluster_record_preserved(self):
        s,d,p=fixture();s['occurrences'][0]['associated_lines']=[]
        r=self.read(s,d,p);self.assertEqual(len(r['representations']),1);self.assertEqual(r['physical_groups'],[])
        self.assertEqual(r['representations'][0]['multiplicity']['unlocated_group_count'],2)


if __name__=='__main__':unittest.main()
