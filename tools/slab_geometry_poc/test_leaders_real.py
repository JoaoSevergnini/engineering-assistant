"""Real-sheet stage 3 replay; snapshots are not independent engineering truth."""
import copy
import json
from pathlib import Path
import unittest
from automatic import detect_layout
from leaders import read_sheet_with_leaders,compare_previous

ROOT=Path(__file__).resolve().parents[2]
CASE=ROOT/'analises/lajes_geometria_lideres'


class RealLeaderRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads((CASE/'entidades_pagina.json').read_text(encoding='utf-8'))
        cls.prior=json.loads((ROOT/'analises/lajes_geometria_automatico/inventario.json').read_text(encoding='utf-8'))
        cls.layout=detect_layout(cls.data['texts'],[0,0,2384,1684])
        cls.result=read_sheet_with_leaders(cls.data,cls.layout)
        for i,o in enumerate(cls.result['occurrences'],1):o['display_id']=f'O{i:03}'
        cls.by_id={o['display_id']:o for o in cls.result['occurrences']}

    def test_snapshot_and_all_old_complete_geometries(self):
        self.assertEqual(self.result['status_counts'],dict(ASSOCIATED=50,PARTIAL=2,AMBIGUOUS=7,UNRESOLVED=0))
        comparison=compare_previous(self.result,self.prior)
        self.assertEqual(len(comparison['baseline_complete_associations']),30)
        self.assertTrue(all(p['exact_geometry_preserved'] for p in comparison['baseline_complete_associations']))
        old=next(o for o in self.prior['occurrences'] if o['display_id']=='O036')
        self.assertEqual(self.by_id['O036']['region_pdf_pt'],old['region_pdf_pt'])

    def test_requested_local_targets_and_no_invented_envelopes(self):
        targets={'O003':'D1638:0','O004':'D1732:0','O005':'D1632:0','O022':'D1728:0',
                 'O024':'D1726:0','O039':'D1612:0','O040':'D1616:0','O045':'D1585:0','O046':'D1574:0'}
        for id,target in targets.items():
            o=self.by_id[id];self.assertEqual(o['status'],'ASSOCIATED')
            self.assertEqual(o['representation_kind'],'LOCALIZED')
            self.assertEqual(o['leader_association']['target']['id'],target)
            self.assertIsNone(o['region_pdf_pt']);self.assertEqual(len(o['associated_lines']),2)

    def test_n2_n36_no_longer_accept_leader_as_bar(self):
        for id,target in [('O008','D1661:0'),('O058','D1883:0')]:
            o=self.by_id[id];self.assertEqual(o['status'],'ASSOCIATED')
            self.assertEqual(o['representation_kind'],'DISTRIBUTED')
            c=o['leader_association'];self.assertEqual(c['target']['id'],target)
            self.assertFalse(set(c['trace']['segment_ids'])&set(c['target']['source_ids']))
            self.assertIsNotNone(o['region_pdf_pt'])
        self.assertAlmostEqual(self.by_id['O058']['leader_association']['terminal_contact']['tip_centerline_offset_pt'],1.32,places=2)

    def test_n7_competing_destinations_preserved(self):
        for id in ('O048','O049'):
            o=self.by_id[id];self.assertEqual(o['status'],'AMBIGUOUS')
            self.assertEqual(len(o['leader_candidates']),2)
            self.assertIsNone(o['leader_association']);self.assertIsNone(o['region_pdf_pt'])

    def test_exploration_limits_do_not_promote_plausible_routes(self):
        for id in ('O012','O016','O037'):
            o=self.by_id[id];self.assertNotEqual(o['status'],'ASSOCIATED')
            self.assertTrue(o['leader_search']['search_limits'])
            self.assertIsNone(o['leader_association'])

    def test_crossings_do_not_redirect_n6(self):
        c=self.by_id['O003']['leader_association']
        self.assertEqual(c['trace']['segment_ids'],['D1346:0','D1347:0'])
        self.assertGreaterEqual(len(c['trace']['crossings']),1)
        self.assertTrue(all(p['behavior']=='CROSSED_WITHOUT_SWITCHING' for p in c['trace']['crossings']))

    def test_full_sheet_color_and_order_independence(self):
        data=copy.deepcopy(self.data)
        for p in data['paths']:p['color']=[0,0,0];p['fill']=[0,0,0]
        data['paths'].reverse();data['segments'].reverse();data['texts'].reverse()
        replay=read_sheet_with_leaders(data,self.layout)
        def signature(r):
            return [(o['occurrence_id'],o['status'],o['representation_kind'],o['region_pdf_pt'],
                     o['leader_association']['target']['id'] if o['leader_association'] else None,
                     [s['id'] for s in o['associated_lines']]) for o in r['occurrences']]
        self.assertEqual(signature(self.result),signature(replay))


if __name__=='__main__':unittest.main()
