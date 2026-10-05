import copy
import json
from pathlib import Path
import unittest
import subprocess
import sys
import tempfile

from map_beam import detail_to_tqs, map_beam

ROOT = Path(__file__).resolve().parents[2]


def load(name):
    return json.loads((ROOT/'analises/pranchas'/name).read_text(encoding='utf-8'))


class MappingTests(unittest.TestCase):
    def setUp(self):
        self.detail = load('V501_V503_beam_model.json')
        self.tqs = load('V501_tqs.json')
        self.pos = load('V501_tqs_positions.json')

    def run_mapping(self):
        return map_beam(self.detail, self.tqs, self.pos)

    def test_transform(self):
        self.assertEqual(detail_to_tqs(0, 1.2), .6)
        self.assertEqual(detail_to_tqs(-62, 1.2), -.02)
        self.assertEqual(detail_to_tqs(711, 1.2), 7.71)

    def test_support_order_faces_and_mismatch(self):
        out = self.run_mapping()
        self.assertEqual(out['supports']['left']['id'], 'P2A')
        self.assertEqual(out['supports']['right']['id'], 'P1A')
        self.assertEqual(out['supports']['right']['axis_x'], 8.43)
        self.assertEqual(out['supports']['left']['inner_face_x'], .6)
        self.assertEqual(out['supports']['right']['inner_face_x'], 7.72)
        self.assertEqual(out['supports']['right']['detailing_inner_face_x'], 7.71)
        self.assertEqual(out['geometry']['difference'], .01)
        self.assertEqual(out['geometry']['status'], 'mismatch')

    def test_positions_values_and_all_series_preserved_without_interpolation(self):
        out = self.run_mapping()
        self.assertEqual(out['force_series'], self.pos['beam']['spans'][0]['internal_forces'])
        self.assertEqual([s['x'] for s in out['tqs_sections']], self.pos['beam']['spans'][0]['internal_forces'][0]['positions'])
        self.assertEqual(len(out['tqs_sections']), 13)
        self.assertTrue(all(len(s['forces']) == 5 for s in out['tqs_sections']))
        self.assertEqual(len(out['unmapped_tqs_series']), 9)
        self.assertEqual(out['tqs_sections'][7]['forces'][0]['value'], 61.5073088)

    def test_actual_bar_intervals_and_coverage(self):
        bars = self.run_mapping()['reinforcement']
        self.assertEqual([b['covered_tqs_sections'] for b in bars], [list(range(1,8)),list(range(1,5)),list(range(7,14)),list(range(10,14)),list(range(1,14))])
        self.assertEqual((bars[0]['x_start_common'], bars[0]['x_end_common']), (-.02,4.63))
        self.assertEqual(bars[0]['source'], self.detail['longitudinal_reinforcement'][0]['source'])

    def test_closed_interval_exact_boundaries(self):
        bar = self.detail['longitudinal_reinforcement'][0]
        bar.update(x_start_cm=-21.6, x_end_cm=167.2)
        self.assertEqual(self.run_mapping()['reinforcement'][0]['covered_tqs_sections'], [1,2,3,4])
        bar.update(x_start_cm=167.2, x_end_cm=167.2)
        self.assertEqual(self.run_mapping()['reinforcement'][0]['covered_tqs_sections'], [4])

    def test_empty_interval_and_missing_interval(self):
        bar = self.detail['longitudinal_reinforcement'][0]
        bar.update(x_start_cm=10, x_end_cm=20)
        self.assertEqual(self.run_mapping()['reinforcement'][0]['covered_tqs_sections'], [])
        bar['x_start_cm'] = None
        self.assertIsNone(self.run_mapping()['reinforcement'][0]['covered_tqs_sections'])

    def test_independent_grouped_beams(self):
        a = self.run_mapping()
        b = map_beam(self.detail, load('V503_tqs.json'), load('V503_tqs_positions.json'))
        self.assertEqual(a['reinforcement'][0]['covered_tqs_sections'], b['reinforcement'][0]['covered_tqs_sections'])
        self.assertEqual(b['supports']['left']['id'], 'P2B')
        self.assertEqual(b['supports']['right']['id'], 'P1B')
        self.assertNotEqual(a['tqs_sections'][7]['forces'][0]['value'], b['tqs_sections'][7]['forces'][0]['value'])

    def test_indirect_relations_without_bar_or_ib_association(self):
        related = [load(f'V{n}_tqs.json') for n in (541,542,559,560)]
        out = map_beam(self.detail, self.tqs, self.pos, related)
        self.assertEqual([r['supported_beam'] for r in out['indirect_relations']], ['V541','V542'])
        self.assertTrue(all(r['x'] is None and r['drawing_indirect_support_id'] is None and r['reinforcement_mark'] is None for r in out['indirect_relations']))
        self.assertEqual(out['drawing_indirect_supports'], self.detail['indirect_supports'])

    def test_input_immutable(self):
        before = copy.deepcopy((self.detail,self.tqs,self.pos))
        self.run_mapping()
        self.assertEqual((self.detail,self.tqs,self.pos), before)

    def test_missing_geometry_rejected_without_fallback(self):
        for source in self.tqs['sources'].values():
            if source['file'] == 'RELDTFPS.LST':
                source['file'] = 'UNAVAILABLE.LST'
        with self.assertRaisesRegex(ValueError, 'Fonte escolhida'):
            self.run_mapping()

    def test_missing_positions_rejected(self):
        self.pos['beam']['spans'][0]['internal_forces'][0]['positions'] = None
        with self.assertRaisesRegex(ValueError, '13 positions'):
            self.run_mapping()

    def test_changed_forces_rejected(self):
        self.pos['beam']['spans'][0]['internal_forces'][0]['values'][0] += 1
        with self.assertRaisesRegex(ValueError, 'divergem'):
            self.run_mapping()

    def test_changed_sections_rejected(self):
        self.pos['beam']['spans'][0]['internal_forces'][0]['sections'][0] = 0
        with self.assertRaisesRegex(ValueError, '13 seções'):
            self.run_mapping()

    def test_wrong_identity_rejected(self):
        self.pos['beam']['id'] = 'V503'
        with self.assertRaisesRegex(ValueError, 'Identidade'):
            self.run_mapping()

    def test_wrong_coordinates_and_multiple_spans_rejected(self):
        self.detail['coordinate_system']['unit'] = 'm'
        with self.assertRaisesRegex(ValueError, 'Convenção'):
            self.run_mapping()
        self.detail['coordinate_system']['unit'] = 'cm'
        self.detail['spans'].append(copy.deepcopy(self.detail['spans'][0]))
        with self.assertRaisesRegex(ValueError, 'um vão'):
            self.run_mapping()

    def test_exact_geometry_status(self):
        self.detail['spans'][0].update(clear_length_cm=712, x_end_cm=712)
        out = self.run_mapping()
        self.assertEqual(out['geometry']['status'], 'exact')
        self.assertEqual(out['geometry']['difference'], 0)

    def test_reversed_bar_rejected(self):
        self.detail['longitudinal_reinforcement'][0].update(x_start_cm=10,x_end_cm=0)
        with self.assertRaisesRegex(ValueError, 'invertido'):
            self.run_mapping()

    def test_force_variants_preserved(self):
        for model in (self.tqs,self.pos):
            model['beam']['spans'][0]['internal_forces'][0]['variant'] = 'documented_variant'
        out = self.run_mapping()
        self.assertEqual(out['tqs_sections'][0]['forces'][0]['variant'], 'documented_variant')
        self.pos['beam']['spans'][0]['internal_forces'][0]['variant'] = 'other'
        with self.assertRaisesRegex(ValueError, 'divergem'):
            self.run_mapping()

    def test_conflict_within_chosen_source_rejected(self):
        warning = next(w for w in self.tqs['warnings'] if w.get('path') == '/beam/supports/1/eccentricity')
        warning['alternatives'].append({'value': .5, 'sources': ['s157#/normalizacao/campos/excentricidade']})
        with self.assertRaisesRegex(ValueError, 'conflitante'):
            self.run_mapping()

    def test_v503_related_beams_independent(self):
        related = [load(f'V{n}_tqs.json') for n in (541,542,559,560)]
        related[2]['beam']['support_reactions'][-1]['support_id'] += '\x00'
        out = map_beam(self.detail, load('V503_tqs.json'), load('V503_tqs_positions.json'), related)
        self.assertEqual([r['supported_beam'] for r in out['indirect_relations']], ['V559','V560'])
        self.assertTrue(out['indirect_relations'][0]['reaction']['support_id'].endswith('\x00'))

    def test_unclassified_bar_remains_unclassified(self):
        self.detail['longitudinal_reinforcement'][0]['function'] = None
        self.assertIsNone(self.run_mapping()['reinforcement'][0]['function'])

    def test_cli_rejects_overwrite(self):
        with tempfile.TemporaryDirectory() as folder:
            p = Path(folder)/'detail.json'
            p.write_text(json.dumps(self.detail), encoding='utf-8')
            before = p.read_bytes()
            result = subprocess.run([sys.executable,str(Path(__file__).with_name('map_beam.py')),str(p),
                                     str(ROOT/'analises/pranchas/V501_tqs.json'),str(ROOT/'analises/pranchas/V501_tqs_positions.json'),
                                     '--output',str(p)], capture_output=True)
            self.assertNotEqual(result.returncode,0)
            self.assertEqual(p.read_bytes(),before)


if __name__ == '__main__':
    unittest.main()
