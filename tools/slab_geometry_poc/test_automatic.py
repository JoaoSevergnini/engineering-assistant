"""Synthetic tests: these prove local behavior, not sheet-wide accuracy."""
import copy
import unittest
from automatic import inventory, line_geometry, distribution_axes, junctions, associate_occurrence, parse_extended, compare_schedule
from test_geometry import fixture, segment


def text(id,value,box,direction=(1,0)):
    return dict(id=id,text=value,bbox=box,direction=list(direction))


class SyntheticAutomaticTests(unittest.TestCase):
    def test_multiple_repeated_marks_and_table_exclusion(self):
        texts=[text('a','N2 5 Ø 8 C/14 C=150',[10,10,110,20]),
               text('b','N2 5 Ø 8 C/14 C=150',[10,50,110,60]),
               text('table','N99 3 Ø 8 C=50',[210,10,280,20]),
               text('note','DETALHE N5 3 Ø 8 C=20',[10,90,110,100])]
        r=inventory(texts,[0,0,300,200],[[200,0,300,200]])
        self.assertEqual(len(r['occurrences']),2)
        self.assertEqual([o['documentary_mark'] for o in r['occurrences']],['N2','N2'])
        self.assertNotEqual(*[o['occurrence_id'] for o in r['occurrences']])
        self.assertEqual([t['id'] for t in r['excluded_call_like']],['table'])

    def test_multiline_and_printed_multiplicity(self):
        r=inventory([text('a','N5 2x3 Ø 12.5',[10,10,100,22]),text('b','C=145',[30,22,65,34])],[0,0,200,200])
        c=r['occurrences'][0]['call']
        self.assertTrue(c['parse_complete']);self.assertEqual(c['quantity_factors'],[2,3]);self.assertEqual(c['quantity'],6)
        self.assertIsNone(c['spacing_cm'])

    def test_rotated_multiline(self):
        r=inventory([text('a','N5 3 Ø 8',[10,20,22,90],(0,-1)),text('b','C=145',[22,35,34,65],(0,-1))],[0,0,200,200])
        self.assertTrue(r['occurrences'][0]['call']['parse_complete'])

    def test_incomplete_call_preserved(self):
        r=inventory([text('a','N9 3 Ø 8 C/14',[10,10,100,22]),text('b','C=unknown',[10,25,70,37])],[0,0,200,200])
        o=r['occurrences'][0]
        self.assertFalse(o['call']['parse_complete']);self.assertIn('nominal_length_cm',o['call']['missing_fields'])
        self.assertIn('C=unknown',o['text']);self.assertEqual(o['status'],'UNRESOLVED')

    def test_unowned_candidate_fragment_is_not_dropped(self):
        r=inventory([text('a','N9 ?',[10,10,100,22]),text('b','C=150',[10,80,70,92])],[0,0,200,200])
        self.assertEqual(len(r['unowned_continuations']),1)
        self.assertEqual(r['occurrences'][0]['documentary_mark'],'N9')

    def prepared(self):
        label,data=fixture();label.update(id='a',direction=[1,0])
        o=inventory([label],[-10,-10,200,200])['occurrences'][0]
        return o,data

    def test_associated_without_color(self):
        o,data=self.prepared();lines=line_geometry(data['segments'])
        result=associate_occurrence(o,lines,distribution_axes(lines,data['segments']),junctions(data['paths']))
        self.assertEqual(result['status'],'ASSOCIATED')
        for p in data['paths']:p['color']=[0,0,0]
        for s in data['segments']:s['color']=[1,0,0]
        o2,_=self.prepared();self.assertEqual(result,associate_occurrence(o2,lines,distribution_axes(lines,data['segments']),junctions(data['paths'])))

    def test_nearby_bars_ambiguous_not_nearest(self):
        o,data=self.prepared();data['segments'].append(segment('bar2',[0,11],[100,11]))
        data['paths'].append(dict(id='junction2',bbox=[24,10,26,12],items=[['c']]*4))
        lines=line_geometry(data['segments']);r=associate_occurrence(o,lines,distribution_axes(lines,data['segments']),junctions(data['paths']))
        self.assertEqual(r['status'],'AMBIGUOUS');self.assertEqual(len(r['associations']),2);self.assertIsNone(r['region_pdf_pt'])

    def test_absent_axis_partial_and_absent_marker_partial(self):
        o,data=self.prepared();lines=line_geometry(data['segments'])
        self.assertEqual(associate_occurrence(o,lines,[],junctions(data['paths']))['status'],'PARTIAL')
        o,_=self.prepared()
        self.assertEqual(associate_occurrence(o,lines,distribution_axes(lines,data['segments']),[])['status'],'PARTIAL')

    def test_fragment_merge_and_arrow_tip_boundary(self):
        segs=[segment('a',[0,0],[20,0]),segment('b',[20.1,0],[40,0])]
        self.assertEqual(len(line_geometry(segs)),1)
        segs=[segment('a',[0,0],[0,20]),segment('b',[0,20],[0,40]),segment('w1',[-1,15],[0,20]),segment('w2',[1,15],[0,20])]
        self.assertEqual(len([s for s in line_geometry(segs) if s['orientation']==1]),2)

    def test_nominal_c_not_forced_equal_to_projection(self):
        o,data=self.prepared();o['call']['nominal_length_cm']=250
        lines=line_geometry(data['segments']);r=associate_occurrence(o,lines,distribution_axes(lines,data['segments']),junctions(data['paths']))
        self.assertEqual(r['status'],'ASSOCIATED')
        self.assertFalse(r['associations'][0]['evidence']['length_agreement_auxiliary'])

    def test_displaced_text_stays_partial(self):
        o,data=self.prepared();o['bbox']=[30,-15,80,-6]
        lines=line_geometry(data['segments'])
        self.assertEqual(associate_occurrence(o,lines,distribution_axes(lines,data['segments']),junctions(data['paths']))['status'],'PARTIAL')

    def test_vertical_bar_horizontal_distribution(self):
        o,data=self.prepared()
        for s in data['segments']:
            for key in ('a','b'):s[key]=[s[key][1],-s[key][0]]
        data['paths'][0]['bbox']=[9,-26,11,-24]
        o['bbox']=[0,-80,9,-30];o['direction']=[0,-1]
        lines=line_geometry(data['segments'])
        self.assertEqual(associate_occurrence(o,lines,distribution_axes(lines,data['segments']),junctions(data['paths']))['status'],'ASSOCIATED')

    def test_fragmented_bar_retains_source_ids(self):
        o,data=self.prepared()
        data['segments']=data['segments'][1:]+[segment('part1',[0,10],[50,10]),segment('part2',[50,10],[100,10])]
        lines=line_geometry(data['segments']);r=associate_occurrence(o,lines,distribution_axes(lines,data['segments']),junctions(data['paths']))
        self.assertEqual(r['status'],'ASSOCIATED')
        self.assertEqual(r['associations'][0]['bar']['source_ids'],['part1','part2'])

    def test_repeated_quantities_are_not_summed(self):
        a=dict(occurrence_id='a',documentary_mark='N1',call=parse_extended('N1 2x3 Ø 8 C=50'))
        b=copy.deepcopy(a);b['occurrence_id']='b'
        r=compare_schedule([a,b],[dict(mark='N1',quantity=12,diameter_mm=8,nominal_length_cm=50)])['rows'][0]
        self.assertEqual(r['call_quantities'],[6,6]);self.assertNotIn('printed_factor_sum_scenario',r)
        self.assertEqual(r['quantity_comparison'],'NOT_COMPARED_REPEATED_REPRESENTATIONS')
        self.assertTrue(r['physical_quantity_comparison'].startswith('NOT_CONCLUDED'))


if __name__=='__main__':unittest.main()
