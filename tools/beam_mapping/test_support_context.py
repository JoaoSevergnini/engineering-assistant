import copy
import json
from pathlib import Path
import unittest
from support_context import resolve_support, interpret_origin
from map_beam import map_beam

ROOT = Path(__file__).resolve().parents[2]
def load(name):
    return json.loads((ROOT/'analises/pranchas'/name).read_text(encoding='utf8'))

class SupportContextTests(unittest.TestCase):
    def setUp(self): self.c = load('V1001_V9001_support_context.json')
    def resolve(self, beam='V1001', support='P2A', context=True):
        return resolve_support('P2A/P2B', support, beam, 'left', self.c if context else None)
    def test_direct(self):
        self.assertEqual(resolve_support('P2A','P2A','V1001','left',None)['method'],'direct_identity')
    def test_tower_a(self):
        r=self.resolve();self.assertEqual(r['document_label'],'P2A/P2B');self.assertEqual(r['candidates'],['P2A','P2B']);self.assertTrue(r['evidence'])
    def test_tower_b(self): self.assertEqual(self.resolve('V9001','P2B')['resolved_support_id'],'P2B')
    def test_no_candidate(self):
        with self.assertRaisesRegex(ValueError,'support_context_mismatch'): self.resolve(support='P9')
    def test_ambiguity(self):
        self.c['members'].append(copy.deepcopy(self.c['members'][0]))
        with self.assertRaisesRegex(ValueError,'ambiguous_support_mapping'): self.resolve()
    def test_slash_without_context(self):
        with self.assertRaisesRegex(ValueError,'unrecognized_grouped_support_context'): self.resolve(context=False)
    def test_origin(self):
        s='face interna do apoio esquerdo P2A/P2B';r=interpret_origin(s,'P2A/P2B')
        self.assertEqual(r,{'original':s,'origin_type':'left_support_inner_face','origin_support_label':'P2A/P2B'})
    def test_v501_unchanged(self):
        out=map_beam(load('V501_V503_beam_model.json'),load('V501_tqs.json'),load('V501_tqs_positions.json'),[load('V541_tqs.json'),load('V542_tqs.json')])
        golden=load('V501_beam_mapping.json');golden.pop('inputs',None);self.assertEqual(out,golden)
    def test_real_v1001(self):
        d,t,p=[load(n) for n in ('V1001_beam_model.json','V1001_tqs.json','V1001_tqs_positions.json')];before=copy.deepcopy(d)
        out=map_beam(d,t,p,[load('V1014_tqs.json'),load('V1015_tqs.json')],support_context=self.c)
        golden=load('V1001_beam_mapping.json');golden.pop('inputs',None);self.assertEqual(out,golden);self.assertEqual(d,before)
        bars={b['mark']:b for b in out['reinforcement']}
        self.assertEqual((bars['N3']['x_start_common'],bars['N3']['x_end_common']),(.18,6.68))
        self.assertEqual((bars['N5']['x_start_common'],bars['N5']['x_end_common']),(.18,8.13))
        self.assertEqual(out['force_series'],p['beam']['spans'][0]['internal_forces'])
    def test_documented_members_are_distinct_from_confirmed_towers(self):
        self.c['type']='documented_shared_detail_members'
        self.assertEqual(self.resolve('V9001','P2B')['method'],'drawing_group_and_ordered_tqs_support')
        self.c['evidence']=None
        with self.assertRaisesRegex(ValueError,'missing_support_context_evidence'): self.resolve('V9001','P2B')

    def test_missing_evidence(self):
        self.c['evidence']=[]
        with self.assertRaisesRegex(ValueError,'missing_support_context_evidence'): self.resolve()
    def test_wrong_tower(self):
        with self.assertRaisesRegex(ValueError,'support_context_mismatch'): self.resolve(support='P2B')
