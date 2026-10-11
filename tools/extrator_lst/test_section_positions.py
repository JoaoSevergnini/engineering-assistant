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


class CantileverPositionsTests(unittest.TestCase):
    def data(self, side='LEFT', length=2):
        # Signed series belonging to span 7, not the first span of a file.
        field=dict(normalizado=dict(valor=length,unidade='m'))
        raw=dict(records=[dict(normalizacao=dict(tipo='geometria_tabular',campos=dict(vao=dict(valor=7),comprimento=field))),
                          dict(normalizacao=dict(vao_original=7))])
        series=dict(sections=list(range(1,14)),values=[-i for i in range(13)],sources=['F#/normalizacao'],unit='kN.m')
        model=dict(units=dict(length='m'),beam=dict(spans=[dict(id=7,original_span_tokens=['7B'],report_span_ids={'VGESFS.LST':7},support_ids=None,internal_forces=[series])]),
                   sources={k:dict(file='VGESFS.LST',raw_pointer='/records/'+str(i)) for i,k in enumerate(('G','F'))},provenance={},policies={})
        def proved(v,u=None):return dict(value=v,state='DOCUMENTED_CONFIRMED',unit=u,provenance=[dict(fixture='synthetic reviewed form')],criterion=None)
        context={'7':dict(orientation=proved(side),physical_bounds=dict(x_start_m=proved(-2,'m'),x_end_m=proved(-2+length,'m')))}
        return model,raw,context
    def test_left_and_right_single_cantilever_preserve_values(self):
        for side,free in (('LEFT',1),('RIGHT',13)):
            m,r,c=self.data(side);before=copy.deepcopy(m)
            o,n=fill_positions(m,r,cantilever_contexts=c);s=o['beam']['spans'][0]['internal_forces'][0]
            self.assertEqual(n,1);self.assertEqual(s['positions'][0],0);self.assertEqual(s['positions'][-1],2)
            self.assertEqual(s['position_interpretation']['free_section'],free)
            self.assertEqual(s['values'],list(range(0,-13,-1)));self.assertEqual(m,before)
    def test_orientation_never_inferred_from_single_span_or_B_token(self):
        m,r,c=self.data()
        with self.assertRaisesRegex(ValueError,'cantilever_orientation_unproved'):fill_positions(m,r)
    def test_form_length_conflict_rejected(self):
        m,r,c=self.data();c['7']['physical_bounds']['x_end_m']['value']=1
        with self.assertRaisesRegex(ValueError,'cantilever_length_form_conflict'):fill_positions(m,r,cantilever_contexts=c)
    def test_series_of_another_span_rejected(self):
        m,r,c=self.data();r['records'][1]['normalizacao']['vao_original']=8
        with self.assertRaisesRegex(ValueError,'outro vao'):fill_positions(m,r,cantilever_contexts=c)
    def test_missing_cantilever_series_does_not_use_adjacent_span(self):
        m,r,c=self.data();m['beam']['spans'][0]['internal_forces']=[]
        with self.assertRaisesRegex(ValueError,'cantilever_force_series_unavailable'):fill_positions(m,r,cantilever_contexts=c)
    def test_each_cantilever_uses_its_own_series_in_multi_span_input(self):
        m,r,c=self.data();other=copy.deepcopy(m['beam']['spans'][0]);other.update(id=8,original_span_tokens=['8B'],report_span_ids={'VGESFS.LST':8})
        other['internal_forces'][0].update(sources=['F8#/normalizacao'],values=list(range(13)))
        m['beam']['spans'].append(other)
        records=copy.deepcopy(r['records']);records[0]['normalizacao']['campos']['vao']['valor']=8;records[1]['normalizacao']['vao_original']=8
        r['records']+=records
        m['sources'].update({k:dict(file='VGESFS.LST',raw_pointer='/records/'+str(i)) for k,i in (('G8',2),('F8',3))})
        c['8']=copy.deepcopy(c['7']);c['8']['orientation']['value']='RIGHT'
        out,n=fill_positions(m,r,cantilever_contexts=c)
        self.assertEqual(n,2)
        self.assertEqual(out['beam']['spans'][0]['internal_forces'][0]['position_interpretation']['free_section'],1)
        self.assertEqual(out['beam']['spans'][1]['internal_forces'][0]['position_interpretation']['free_section'],13)
        self.assertEqual(out['beam']['spans'][1]['internal_forces'][0]['values'],list(range(13)))


if __name__ == '__main__':
    unittest.main()
