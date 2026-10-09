import json,unittest
from pathlib import Path
from extrair_viga_lst import extract
from consolidar_viga import consolidate

ROOT=Path(__file__).resolve().parents[2]
SOURCE=Path(r'C:\TQS\TGD - SILVA JARDIM\24-212-TGD-SILVA JARDIM-R35\TIPO\VIGAS')
FIXTURE=ROOT/'analises/etapa1_leitura_geometria/balancos_reais.json'

class RealSpanFixtureTests(unittest.TestCase):
    def test_all_real_B_tokens(self):
        rows=json.loads(FIXTURE.read_text(encoding='utf-8-sig'))
        expected={'V617':'2B','V620':'2B','V622':'2B','V625':'2B','V626':'1B','V627':'2B','V629':'4B'}
        self.assertEqual({r['beam']:r['token'] for r in rows},expected)
        for r in rows:
            self.assertEqual(r['normalization']['tipo_vao_documental'],'CANTILEVER')
            self.assertIn(r['token'],r['provenance']['texto'])
            self.assertEqual(int(r['normalization']['campos']['vao']['valor']),int(r['token'][:-1]))

@unittest.skipUnless(SOURCE.exists(),'Original TQS folder unavailable')
class LiveCantileverExtractionTests(unittest.TestCase):
    def test_real_V626_B_and_main_span(self):
        m=consolidate(extract(SOURCE,'V626'))
        byid={s['id']:s for s in m['beam']['spans']}
        self.assertEqual(byid[1]['documentary_span_kind'],'CANTILEVER')
        self.assertEqual(byid[2]['documentary_span_kind'],'BETWEEN_SUPPORTS')
        self.assertEqual(byid[1]['original_span_tokens'],['1B'])
        self.assertEqual(byid[1]['physical_span_validation'],'PENDING')
        self.assertTrue(m['provenance']['/beam/spans/0/documentary_span_kind'])
    def test_live_originals_match_saved_tokens(self):
        rows=json.loads(FIXTURE.read_text(encoding='utf-8-sig'))
        for row in rows:
            raw=extract(SOURCE,row['beam'])
            found=[r['normalizacao'] for r in raw['categorias']['geometria'] if (r.get('normalizacao') or {}).get('identificador_vao_original')==row['token']]
            self.assertTrue(found,row['beam'])

if __name__=='__main__':unittest.main()
