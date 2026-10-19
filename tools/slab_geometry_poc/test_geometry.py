import copy
import unittest
import json
from pathlib import Path
from geometry import parse_call, arrow_wings, associate


def segment(id,a,b):
    import math
    return dict(id=id,a=a,b=b,length_pt=math.dist(a,b))


def fixture():
    segs=[segment('bar',[0,10],[100,10]),segment('axis',[25,0],[25,30])]
    for i,(a,b) in enumerate([([24,5],[25,0]),([26,5],[25,0]),([24,25],[25,30]),([26,25],[25,30])]):
        segs.append(segment('wing'+str(i),a,b))
    marker=dict(id='junction',bbox=[24,9,26,11],items=[['c']]*4)
    return dict(text='N26 35 Ø 6.3 C/12 C=176.3889',bbox=[30,0,80,9]),dict(segments=segs,paths=[marker])


class GeometryTests(unittest.TestCase):
    def test_parse_and_reject_multiplicity(self):
        self.assertEqual(parse_call('N26 35 Ø 6,3 C/12 C=503')['diameter_mm'],6.3)
        self.assertIsNone(parse_call('N5 2x3 Ø 12.5 C=145'))
        self.assertFalse(parse_call('N26 35 \ufffd 6.3 C/12 C=503')['diameter_symbol_decoded'])

    def test_requires_both_arrow_ends(self):
        _,data=fixture()
        self.assertIsNotNone(arrow_wings(data['segments'][1],data['segments']))
        self.assertIsNone(arrow_wings(data['segments'][1],data['segments'][:-1]))

    def test_unique_region_and_color_independence(self):
        label,data=fixture()
        result=associate(label,data)
        self.assertEqual(len(result['accepted_pairs']),1)
        self.assertEqual(result['accepted_pairs'][0]['region_pdf_pt'],[[0,0],[100,0],[100,30],[0,30]])
        for s in data['segments']: s['color']=(1,0,1)
        data['segments'].reverse()
        self.assertEqual(result,associate(label,data))

    def test_nearby_line_not_sufficient(self):
        label,data=fixture()
        data['paths']=[]
        self.assertEqual(associate(label,data)['accepted_pairs'],[])

    def test_wrong_length_rejected(self):
        label,data=fixture()
        label['text']='N26 35 Ø 6.3 C/12 C=503'
        self.assertEqual(associate(label,data)['accepted_pairs'],[])

    def test_alternatives_not_silently_selected(self):
        label,data=fixture()
        extra=copy.deepcopy(data['segments'][0]); extra['id']='other_bar'
        data['segments'].append(extra)
        self.assertEqual(associate(label,data)['status'],'AMBIGUOUS_OR_UNRESOLVED')

    def test_real_extracted_case_and_missing_arrow(self):
        folder=Path(__file__).resolve().parents[2]/'analises/lajes_geometria_poc'
        data=json.loads((folder/'entidades_pagina.json').read_text(encoding='utf-8'))
        stored=json.loads((folder/'resultado_N26.json').read_text(encoding='utf-8'))
        result=associate(stored['label'],data)
        self.assertEqual(result['accepted_pairs'],stored['accepted_pairs'])
        self.assertTrue(stored['schedule_matches'])
        self.assertEqual(result['call']['quantity'],35)
        # Changing every color cannot change the geometric association.
        for path in data['paths']: path['color']=[0,0,0]
        self.assertEqual(associate(stored['label'],data)['accepted_pairs'],result['accepted_pairs'])
        data['segments']=[s for s in data['segments'] if s['id']!='D1601:0']
        self.assertEqual(associate(stored['label'],data)['accepted_pairs'],[])


if __name__=='__main__': unittest.main()
