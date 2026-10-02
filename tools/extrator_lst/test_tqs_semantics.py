"""Regressions for documented span semantics, reactions and local VAO/PONTO messages."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from consolidar_viga import consolidate
from extrair_viga_lst import extract
from test_consolidar_viga import raw_fixture, geometry, support, record, quantity

ROOT=Path(__file__).resolve().parents[2]
class TqsSemanticsTests(unittest.TestCase):
    def test_lengths_and_all_operand_sources(self):
        raw=raw_fixture()
        raw['categorias']['fixture']=[geometry('RELDTVGS.LST',1,1,7.552),
            support('RELDTVGS.LST',2,'P2',1.2,.384),support('RELDTVGS.LST',3,'P1',1.42,.494)]
        before=copy.deepcopy(raw)
        model=consolidate(raw)
        g=model['beam']['spans'][0]['geometry']
        self.assertEqual(g['length'],7.552)
        self.assertAlmostEqual(g['support_axis_length'],8.43)
        self.assertAlmostEqual(g['clear_span_length'],7.12)
        self.assertEqual(len(model['provenance']['/beam/spans/0/geometry/clear_span_length']),5)
        self.assertEqual(before,raw)
    def test_conflict_not_zero_or_preferred_precision(self):
        raw=raw_fixture()
        raw['categorias']['fixture'].append(support('RELDTFPS.LST',22,'P20',.24,.1))
        model=consolidate(raw)
        g=model['beam']['spans'][0]['geometry']
        self.assertIsNone(g['support_axis_length'])
        self.assertIsNone(g['clear_span_length'])
        self.assertTrue(any(w['code']=='derived_geometry_unresolved' for w in model['warnings']))
    def test_missing_width_does_not_block_axis_length(self):
        raw=raw_fixture()
        raw['categorias']['fixture'][2]['normalizacao']['campos'].pop('largura')
        g=consolidate(raw)['beam']['spans'][0]['geometry']
        self.assertAlmostEqual(g['support_axis_length'],1.206)
        self.assertIsNone(g['clear_span_length'])
    def test_unresolved_topology_and_units(self):
        raw=raw_fixture()
        raw['categorias']['fixture'][2]['normalizacao']['campos']['excentricidade']=quantity(5)
        self.assertIsNone(consolidate(raw)['beam']['spans'][0]['geometry']['support_axis_length'])
        raw['categorias']['fixture']=raw['categorias']['fixture'][:2]
        self.assertIsNone(consolidate(raw)['beam']['spans'][0]['geometry']['clear_span_length'])
    def test_reactions_preserve_signs_units_variants_and_unknown_support(self):
        raw=raw_fixture()
        for file,line,name,maximum,minimum,unit in [('VGESFS.LST',40,'V10',2.907,-1,'tf'),
                ('RELDTVGS.LST',41,'V10',2.91,-1,'tf'),('RELGER.LST',42,'UNKNOWN',8,2,None)]:
            raw['categorias']['fixture'].append(record(file,line,{'tipo':'reacao_apoio','campos':
                {'nome':name,'maxima':quantity(maximum,unit),'minima':quantity(minimum,unit)}}))
        raw['categorias']['duplicate']=copy.deepcopy(raw['categorias']['fixture'])
        m=consolidate(raw); rows=m['beam']['support_reactions']
        self.assertEqual(len(rows),3)
        row=next(x for x in rows if x['file']=='VGESFS.LST')
        self.assertAlmostEqual(row['min'],-9.80665)
        self.assertAlmostEqual(row['max'],28.50793155)
        unknown=next(x for x in rows if x['reported_support_name']=='UNKNOWN')
        self.assertIsNone(unknown['support_id']);self.assertIsNone(unknown['max'])
        self.assertTrue(any(w['code']=='reaction_variants' for w in m['warnings']))
    def test_local_point_messages_and_malformed_series_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'VGESFS.LST'
            local='  M(-) = 2.49 TF*M VAO= 2 PONTO= 6'
            valid='Q MN. VAO= 1 '+ ' '.join(str(-x) for x in range(13))
            malformed='M MX. VAO= 1 1 2 bad'
            p.write_text('VIGA = 999 - V999\n'+local+'\n'+valid+'\n'+malformed+'\n',encoding='cp1252')
            raw=extract(Path(tmp),'V999')
            rows=[r for c in raw['categorias'].values() for r in c]+raw['outros_dados']
            self.assertTrue(any(r['origem']['texto']==local and r['normalizacao'] is None for r in rows))
            self.assertTrue(any(r['origem']['texto']==malformed and r['normalizacao'] is None for r in rows))
            series=[r for r in rows if (r['normalizacao'] or {}).get('tipo')=='serie_13_secoes']
            self.assertEqual(len(series),1)
            self.assertEqual(series[0]['normalizacao']['valores'][-1]['valor'],-12)
    def test_actual_local_point_beams_when_lst_available(self):
        folder=Path(r'C:\TQS\24-155-COLLINE-RESIDENCIAL-R60\DIFERENCIADO\VIGAS')
        if not folder.exists():self.skipTest('Local TQS reports unavailable')
        for beam,receiver in [('V542','V501'),('V560','V503')]:
            raw=extract(folder,beam)
            model=consolidate(raw)
            self.assertTrue(any(row['reported_support_name']==receiver for row in model['beam']['support_reactions']))
            lines=[t['texto'] for t in raw['trechos'] if t['arquivo']=='VGESFS.LST']
            self.assertTrue(any('PONTO=' in line for line in lines))

    def test_real_v501_v503_and_source_specific_geometry(self):
        for beam in ('V501','V503'):
            raw=json.loads((ROOT/f'analises/pranchas/{beam}_tqs_raw.json').read_text(encoding='utf-8'))
            before=copy.deepcopy(raw)
            model=consolidate(raw)
            g=model['beam']['spans'][0]['geometry']
            self.assertIsNone(g['support_axis_length'])
            self.assertIsNone(g['clear_span_length'])
            self.assertEqual(len(model['beam']['spans'][0]['internal_forces']),14)
            self.assertTrue(all(s['positions'] is None for s in model['beam']['spans'][0]['internal_forces']))
            reactions=model['beam']['support_reactions']
            self.assertEqual(len(reactions),6)
            self.assertEqual(before,raw)
            # Documented calculation from one coherent source, not a production preference.
            rows=[]; seen=set()
            for cat in raw['categorias'].values():
                for rec in cat:
                    typ=(rec.get('normalizacao') or {}).get('tipo')
                    file=rec['origem']['arquivo'];key=(file,rec['origem']['linha_inicial'])
                    if key not in seen and ((typ=='geometria_tabular' and file=='RELDTVGS.LST') or (typ=='apoio' and file=='RELDTFPS.LST')):
                        rows.append(copy.deepcopy(rec));seen.add(key)
            # Synthetic coherent fixture uses the already extracted detail support fields.
            for rec in rows:
                if rec['normalizacao']['tipo']=='apoio':rec['origem']['arquivo']='RELDTVGS.LST'
            controlled={'schema_version':'1.0','viga':beam,'categorias':{'fixture':rows}}
            geo=consolidate(controlled)['beam']['spans'][0]['geometry']
            self.assertAlmostEqual(geo['support_axis_length'],8.43)
            self.assertAlmostEqual(geo['clear_span_length'],7.12)
            self.assertAlmostEqual(geo['clear_span_length']-7.11,.01)

if __name__=='__main__':unittest.main()
