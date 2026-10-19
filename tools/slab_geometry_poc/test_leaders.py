"""Synthetic leader tests; no evidence of real-sheet accuracy."""
import copy
import math
import unittest
from automatic import inventory,line_geometry,distribution_axes,junctions
from leaders import (EndpointGraph,trace_leaders,resolve_trace,enrich_with_leaders,
                     read_sheet_with_leaders,terminal_contact)
from test_geometry import segment


def leader_fixture(multiple_segments=False):
    text=dict(id='T1',text='N1 2x3 Ø 12.5 C=100',bbox=[0,0,30,10],direction=[1,0])
    points=[[0,11],[35,11],[40,16],[45,16],[50,25]] if multiple_segments else [[0,11],[35,11],[50,25]]
    segs=[segment('L'+str(i),a,b) for i,(a,b) in enumerate(zip(points,points[1:]))]
    tip=points[-1];previous=points[-2];dx,dy=tip[0]-previous[0],tip[1]-previous[1];length=math.hypot(dx,dy);u=[dx/length,dy/length]
    for i,side in enumerate((-1,1)):
        tail=[tip[0]-6*u[0]+side*.8*(-u[1]),tip[1]-6*u[1]+side*.8*u[0]]
        segs.append(segment('W'+str(i),tail,tip))
    segs.extend([segment('BAR1',[50,20],[50,70]),segment('BAR2',[52.8,20],[52.8,70])])
    data=dict(texts=[text],paths=[],segments=segs)
    layout=dict(detail_roi_pt=[-100,-100,200,200],steel_table_roi_pt=[500,500,600,600],scale_denominator=50)
    return data,layout


class SyntheticLeaderTests(unittest.TestCase):
    def read(self,data,layout):return read_sheet_with_leaders(data,layout)['occurrences'][0]

    def test_inclined_leader_and_vertical_group(self):
        data,layout=leader_fixture();o=self.read(data,layout)
        self.assertEqual(o['status'],'ASSOCIATED');self.assertEqual(o['representation_kind'],'LOCALIZED')
        self.assertEqual(o['leader_association']['trace']['segment_ids'],['L0','L1'])
        self.assertEqual([s['id'] for s in o['associated_lines']],['BAR1','BAR2'])
        self.assertIsNone(o['region_pdf_pt'])
        self.assertEqual(o['call']['quantity_factors'],[2,3])
        self.assertEqual(o['leader_association']['multiplicity_geometry'],'NOT_INFERRED_FROM_PRINTED_FACTORS')

    def test_multiple_segments_and_direction_changes(self):
        data,layout=leader_fixture(True);o=self.read(data,layout)
        self.assertEqual(o['status'],'ASSOCIATED')
        self.assertEqual(o['leader_association']['trace']['segment_ids'],['L0','L1','L2','L3'])

    def test_crossing_another_entity_does_not_switch(self):
        data,layout=leader_fixture();data['segments'].append(segment('CROSS',[20,18],[90,18]))
        o=self.read(data,layout)
        self.assertEqual(o['status'],'ASSOCIATED')
        trace=o['leader_association']['trace']
        self.assertEqual(trace['segment_ids'],['L0','L1'])
        self.assertIn('CROSS',[c['other_segment_id'] for c in trace['crossings']])

    def test_two_destinations_remain_ambiguous(self):
        data,layout=leader_fixture();data['segments'].append(segment('OTHER',[49,20],[49,70]))
        o=self.read(data,layout)
        self.assertEqual(o['status'],'AMBIGUOUS');self.assertEqual(len(o['leader_candidates']),2)
        self.assertIsNone(o['leader_association']);self.assertIsNone(o['region_pdf_pt'])

    def test_no_arrow_no_complete_route(self):
        data,layout=leader_fixture();data['segments']=[s for s in data['segments'] if not s['id'].startswith('W')]
        o=self.read(data,layout)
        self.assertNotEqual(o['status'],'ASSOCIATED');self.assertEqual(o['leader_search']['traces'],[])

    def test_terminal_circle_marker(self):
        data,layout=leader_fixture();data['segments']=[s for s in data['segments'] if not s['id'].startswith('W')]
        data['paths']=[dict(id='MARKER',bbox=[49,24,51,26],items=[['c']]*4)]
        o=self.read(data,layout)
        self.assertEqual(o['status'],'ASSOCIATED')
        self.assertEqual(o['leader_association']['trace']['terminal_kind'],'CIRCULAR_MARKER')

    def test_broken_chain_is_not_replaced_by_proximity(self):
        data,layout=leader_fixture();data['segments'][1]['a']=[36,11]
        o=self.read(data,layout);self.assertNotEqual(o['status'],'ASSOCIATED')

    def test_limits_are_explicit_and_block_acceptance(self):
        data,layout=leader_fixture(True)
        o=inventory(data['texts'],layout['detail_roi_pt'])['occurrences'][0]
        traces=trace_leaders(o,data,EndpointGraph(data['segments']),max_segments=1)
        self.assertIn('SEGMENT_LIMIT',traces['search_limits']);self.assertEqual(traces['traces'],[])

    def test_rotated_leader_horizontal_group(self):
        data,layout=leader_fixture()
        for s in data['segments']:
            for key in ('a','b'):s[key]=[s[key][1],-s[key][0]]
        data['texts'][0]['bbox']=[0,-30,10,0];data['texts'][0]['direction']=[0,-1]
        o=self.read(data,layout);self.assertEqual(o['status'],'ASSOCIATED')
        self.assertTrue(all(s['orientation']==0 for s in o['associated_lines']))

    def test_color_and_order_independence(self):
        data,layout=leader_fixture();original=self.read(data,layout)
        for s in data['segments']:s['color']=[.1,.7,.2]
        data['segments'].reverse()
        replay=self.read(data,layout)
        self.assertEqual(original['status'],replay['status'])
        self.assertEqual(original['associated_lines'],replay['associated_lines'])
        self.assertEqual(original['leader_association']['trace']['segment_ids'],replay['leader_association']['trace']['segment_ids'])

    def test_no_forced_distribution_when_spacing_printed(self):
        data,layout=leader_fixture();data['texts'][0]['text']='N1 6 Ø 12.5 C/12 C=100'
        o=self.read(data,layout);self.assertEqual(o['status'],'PARTIAL')
        self.assertIsNone(o['leader_association']);self.assertIsNone(o['region_pdf_pt'])

    def test_bounded_terminal_contact_records_original_tip(self):
        data,layout=leader_fixture();o=self.read(data,layout);trace=o['leader_association']['trace']
        target=dict(o['associated_lines'][0],a=[50.4,20],b=[50.4,70])
        contact=terminal_contact(trace,target)
        self.assertEqual(contact['raw_tip'],[50,25]);self.assertGreater(contact['shaft_extension_pt'],0)
        target.update(a=[55,20],b=[55,70]);self.assertIsNone(terminal_contact(trace,target))

    def test_shared_target_is_not_two_proved_physical_occurrences(self):
        data,layout=leader_fixture();other=copy.deepcopy(data['texts'][0]);other['id']='OTHER_TEXT'
        data['texts'].append(other)
        occurrences=read_sheet_with_leaders(data,layout)['occurrences']
        self.assertTrue(all(o['status']=='AMBIGUOUS' for o in occurrences))
        self.assertTrue(all(o['reason']=='LEADER_TARGET_SHARED_WITH_ANOTHER_REPRESENTATION' for o in occurrences))

    def test_second_route_without_supported_target_still_blocks_acceptance(self):
        data,layout=leader_fixture();tip=[70,-10];previous=[35,11]
        data['segments'].append(segment('BRANCH',previous,tip))
        delta=[tip[0]-previous[0],tip[1]-previous[1]];length=math.hypot(*delta);u=[v/length for v in delta]
        for i,side in enumerate((-1,1)):
            tail=[tip[0]-6*u[0]-side*.8*u[1],tip[1]-6*u[1]+side*.8*u[0]]
            data['segments'].append(segment('BRANCH_W'+str(i),tail,tip))
        o=self.read(data,layout)
        self.assertEqual(len(o['leader_search']['traces']),2)
        self.assertEqual(o['status'],'AMBIGUOUS');self.assertEqual(len(o['unresolved_terminal_routes']),1)


if __name__=='__main__':unittest.main()
