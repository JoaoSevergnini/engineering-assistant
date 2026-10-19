"""Real-sheet regressions. Expected counts are snapshots, NOT accuracy evidence."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import unittest
from automatic import detect_layout, read_sheet, compare_schedule

ROOT=Path(__file__).resolve().parents[2]
CASE=ROOT/'analises/lajes_geometria_automatico'


class RealAutomaticRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads((CASE/'entidades_pagina.json').read_text(encoding='utf-8'))
        cls.saved=json.loads((CASE/'inventario.json').read_text(encoding='utf-8'))
        cls.layout=detect_layout(cls.data['texts'],[0,0,2384,1684])
        cls.result=read_sheet(cls.data,cls.layout)

    def test_inventory_snapshot_not_reference_coverage(self):
        r=self.result
        self.assertEqual(len(r['occurrences']),59)
        self.assertTrue(all(o['call']['parse_complete'] for o in r['occurrences']))
        self.assertEqual(len({o['documentary_mark'] for o in r['occurrences']}),41)
        self.assertEqual(r['unowned_continuations'],[])
        self.assertEqual(r['status_counts'],dict(ASSOCIATED=30,PARTIAL=10,AMBIGUOUS=8,UNRESOLVED=11))
        self.assertIsNone(self.saved['metrics']['coverage'])
        self.assertIsNone(self.saved['metrics']['accuracy'])

    def test_n26_exact_geometric_compatibility(self):
        old=json.loads((ROOT/'analises/lajes_geometria_poc/resultado_N26.json').read_text(encoding='utf-8'))
        o=next(o for o in self.result['occurrences'] if o['documentary_mark']=='N26')
        pair=o['associations'][0];legacy=old['accepted_pairs'][0]
        self.assertEqual(pair['bar']['id'],legacy['bar']['id'])
        self.assertEqual(pair['evidence']['axis']['id'],legacy['axis']['id'])
        self.assertEqual(o['region_pdf_pt'],legacy['region_pdf_pt'])

    def test_repetitions_and_multiline_ids(self):
        repeated=[o for o in self.result['occurrences'] if o['documentary_mark']=='N24']
        self.assertEqual(sorted(o['call']['quantity'] for o in repeated),[7,20])
        self.assertNotEqual(repeated[0]['occurrence_id'],repeated[1]['occurrence_id'])
        self.assertTrue(all(o['physical_occurrence_id'] is None for o in repeated))
        self.assertEqual(len(next(o for o in self.result['occurrences'] if o['occurrence_id']=='P1-T59:0')['text_ids']),2)

    def test_full_sheet_color_and_order_independence(self):
        data=copy.deepcopy(self.data)
        for p in data['paths']:p['color']=[0,0,0];p['fill']=[0,0,0]
        data['paths'].reverse();data['segments'].reverse();data['texts'].reverse()
        replay=read_sheet(data,self.layout)
        def signature(r):
            return [(o['occurrence_id'],o['status'],o['region_pdf_pt'],[(p['bar']['id'],p['evidence']['axis']['id']) for p in o['associations']]) for o in r['occurrences']]
        self.assertEqual(signature(self.result),signature(replay))

    def test_independent_schedule_no_repeated_quantity_sums(self):
        obs=self.saved['steel_schedule']['observations']
        self.assertEqual(len(obs),41)
        r=compare_schedule(self.result['occurrences'],obs)
        self.assertEqual(r['positions_without_call'],[]);self.assertEqual(r['calls_without_table'],[])
        self.assertFalse(any(row['discrepancies'] for row in r['rows']))
        repeated=next(row for row in r['rows'] if row['mark']=='N24')
        self.assertEqual(sorted(repeated['call_quantities']),[7,20])
        self.assertIsNone(repeated['single_call_quantity_matches_table'])

    def test_false_weak_leaders_never_become_complete_regions(self):
        for id in ('P1-T65:0','P1-T118:0'):
            o=next(o for o in self.result['occurrences'] if o['occurrence_id']==id)
            self.assertEqual(o['status'],'PARTIAL');self.assertIsNone(o['region_pdf_pt'])
        o=next(o for o in self.result['occurrences'] if o['occurrence_id']=='P1-T49:1')
        self.assertEqual(o['status'],'AMBIGUOUS');self.assertIsNone(o['region_pdf_pt'])

    def test_reextract_original_when_available(self):
        path=Path(self.saved['provenance']['file'])
        if not path.exists():self.skipTest('Original PDF unavailable; saved-vector regressions still run')
        sys.path.insert(0,str(ROOT/'tmp/pdf_deps'))
        import fitz
        from geometry import extract_page
        with fitz.open(path) as doc: fresh=extract_page(doc[0])
        # PyMuPDF returns tuples for colors; the JSON inventory has lists.
        # Normalize both via JSON and compare short hashes, avoiding huge diffs.
        canonical=lambda d:hashlib.sha256(json.dumps(d,sort_keys=True,ensure_ascii=False).encode('utf-8')).hexdigest()
        self.assertEqual(canonical(fresh),canonical(self.data))


if __name__=='__main__':unittest.main()
