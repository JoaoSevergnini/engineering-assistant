"""Stage 4 real-sheet regressions, not independent engineering acceptance."""
import copy
import json
from pathlib import Path
import unittest
from opening_groups import reconstruct_localized

ROOT=Path(__file__).resolve().parents[2]


class RealOpeningGroupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.stage3=json.loads((ROOT/'analises/lajes_geometria_lideres/inventario.json').read_text(encoding='utf-8'))
        cls.data=json.loads((ROOT/'analises/lajes_geometria_lideres/entidades_pagina.json').read_text(encoding='utf-8'))
        cls.profile=json.loads((Path(__file__).parent/'conventions/sim_opening_edge_v1.json').read_text(encoding='utf-8'))
        cls.result=reconstruct_localized(cls.stage3,cls.data,cls.profile)
        cls.reconstruction=cls.result['localized_reconstruction']

    def test_snapshot_not_coverage(self):
        m=self.reconstruction['metrics']
        self.assertEqual((m['supported_openings'],m['opening_candidates'],m['physical_groups']),(12,17,23))
        self.assertEqual(m['localized_representations'],15);self.assertEqual(m['groups_with_layer_distribution'],22)
        self.assertIsNone(m['coverage'])

    def test_all_distributed_and_n26_are_identical(self):
        self.assertEqual(self.result['occurrences'],self.stage3['occurrences'])
        self.assertEqual(sum(o['representation_kind']=='DISTRIBUTED' for o in self.result['occurrences']),35)

    def test_n6_two_sides_and_repeated_marks_are_distinct_locations(self):
        records=[r for r in self.reconstruction['representations'] if r['mark']=='N6']
        self.assertEqual(len(records),2);self.assertTrue(all(len(r['group_ids'])==2 for r in records))
        self.assertEqual(len(set(records[0]['group_ids']+records[1]['group_ids'])),4)

    def test_n8_missing_group_and_n38_unknown_multiplicity_preserved(self):
        r=next(r for r in self.reconstruction['representations'] if r['display_id']=='O023')
        self.assertEqual(len(r['group_ids']),1);self.assertEqual(r['multiplicity']['unlocated_group_count'],1)
        r=next(r for r in self.reconstruction['representations'] if r['display_id']=='O059')
        self.assertEqual(r['multiplicity']['original_factors'],[6,3]);self.assertEqual(len(r['group_ids']),1)
        self.assertFalse(r['convention_applied']);self.assertIsNone(r['multiplicity']['unlocated_group_count'])

    def test_n37_two_continuous_groups_across_two_openings_not_four(self):
        r=next(r for r in self.reconstruction['representations'] if r['display_id']=='O054')
        self.assertEqual(len(r['group_ids']),2)
        groups=[g for g in self.reconstruction['physical_groups'] if g['id'] in r['group_ids']]
        self.assertTrue(all(len(g['opening_relations'])==2 for g in groups))

    def test_color_and_order_independence(self):
        data=copy.deepcopy(self.data)
        for p in data['paths']:p['color']=[0,0,0];p['fill']=[0,0,0]
        data['paths'].reverse();data['segments'].reverse()
        result=reconstruct_localized(self.stage3,data,self.profile)['localized_reconstruction']
        self.assertEqual(result['metrics'],self.reconstruction['metrics'])
        self.assertEqual({g['id'] for g in result['physical_groups']},{g['id'] for g in self.reconstruction['physical_groups']})


if __name__=='__main__':unittest.main()
