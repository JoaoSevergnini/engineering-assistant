import copy
import json
from pathlib import Path
import unittest

from section_positions import fill_positions, pointer

ROOT = Path(__file__).resolve().parents[2] / 'analises' / 'pranchas'


class SectionPositionsTests(unittest.TestCase):
    def setUp(self):
        self.model = json.loads((ROOT/'V1001_tqs.json').read_text(encoding='utf8'))
        self.raw = json.loads((ROOT/'V1001_tqs_raw.json').read_text(encoding='utf8'))

    def test_v1001_coordinates_sources_and_preservation(self):
        before_model, before_raw = copy.deepcopy(self.model), copy.deepcopy(self.raw)
        result, count = fill_positions(self.model, self.raw)
        self.assertEqual(count, 5)
        expected_cm = [38.4, 101.333333333333, 164.266666666667, 227.2,
                       290.133333333333, 353.066666666667, 416,
                       478.933333333333, 541.866666666667, 604.8,
                       667.733333333333, 730.666666666667, 793.6]
        original = self.model['beam']['spans'][0]['internal_forces']
        for i, series in enumerate(result['beam']['spans'][0]['internal_forces']):
            for actual, expected in zip(series['positions'], expected_cm):
                self.assertAlmostEqual(actual * 100, expected, places=9)
            refs = series['sources']
            self.assertTrue(all(result['sources'][r.split('#')[0]]['file']=='VGESFS.LST' for r in refs))
            self.assertEqual(series['values'], next(s['values'] for s in original if set(refs).issubset(s['sources'])))
            evidence = result['provenance'][f'/beam/spans/0/internal_forces/{i}/positions']
            files = {result['sources'][r.split('#')[0]]['file'] for r in evidence}
            self.assertEqual(files, {'VGESFS.LST', 'RELDTFPS.LST'})
            for ref in evidence:
                sid, fragment = ref.split('#')
                pointer(pointer(self.raw, result['sources'][sid]['raw_pointer']), fragment)
        self.assertEqual(self.model, before_model)
        self.assertEqual(self.raw, before_raw)

    def test_missing_chosen_source_no_fallback(self):
        for source in self.model['sources'].values():
            if source['file']=='RELDTFPS.LST':
                source['file']='RELDTFNG.LST'
        with self.assertRaisesRegex(ValueError, 'Fonte escolhida ausente'):
            fill_positions(self.model, self.raw)

    def test_bad_section_order_rejected(self):
        next(s for s in self.model['beam']['spans'][0]['internal_forces']
             if s['stage']=='model_input')['sections'].reverse()
        with self.assertRaisesRegex(ValueError, '13 secoes ordenadas'):
            fill_positions(self.model, self.raw)

    def test_wrong_span_link_rejected(self):
        self.model['beam']['spans'][0]['report_span_ids']['VGESFS.LST']=999
        with self.assertRaisesRegex(ValueError, 'Fonte escolhida ausente'):
            fill_positions(self.model, self.raw)


if __name__ == '__main__':
    unittest.main()
