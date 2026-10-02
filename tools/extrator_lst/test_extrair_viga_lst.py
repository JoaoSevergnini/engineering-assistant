"""Testes de integridade documental; nao verificam seguranca estrutural."""
import re
import unittest
from pathlib import Path
from extrair_viga_lst import extract, HEADER

SOURCE=Path(r'C:\TQS\24-155-COLLINE-RESIDENCIAL-R60\DIFERENCIADO\VIGAS')

@unittest.skipUnless(SOURCE.exists(),'Relatorios locais indisponiveis')
class ExtractionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=extract(SOURCE)
        cls.records=[r for rows in cls.data['categorias'].values() for r in rows]+cls.data['outros_dados']

    def record(self,file,line):
        return next(r for r in self.records if r['origem']['arquivo']==file and r['origem']['linha_inicial']==line)

    def test_inventory(self):
        self.assertEqual(self.data['cobertura']['arquivos_lidos'],13)
        self.assertEqual(self.data['cobertura']['blocos_extraidos'],11)
        self.assertEqual(sum(f['status']=='vazio' for f in self.data['arquivos']),2)

    def test_provenance_and_complete_coverage(self):
        seen={(r['origem']['arquivo'],r['origem']['linha_inicial']) for r in self.records}
        for block in self.data['trechos']:
            if block['tipo']!='bloco_viga': continue
            original=(SOURCE/block['arquivo']).read_bytes().decode('cp1252').split('\n')
            for n in range(block['linha_inicial'],block['linha_final']+1):
                text=original[n-1].removesuffix('\r')
                if text.strip() and not re.fullmatch(r'[-=\s]+',text):
                    self.assertIn((block['arquivo'],n),seen)
                header=HEADER.search(text)
                if header: self.assertEqual(int(header[1]),504)
        for r in self.records:
            src=r['origem']
            actual=(SOURCE/src['arquivo']).read_bytes().decode('cp1252').split('\n')[src['linha_inicial']-1].removesuffix('\r')
            self.assertEqual(src['texto'],actual)

    def test_sparse_and_dense_series(self):
        sparse=self.record('RELDTFPS.LST',66)['normalizacao']['valores']
        self.assertEqual([v['valor'] if v else None for v in sparse],[2]+[None]*11+[59])
        dense=self.record('RELDTFPS.LST',67)['normalizacao']['valores']
        self.assertEqual([v['valor'] if v else None for v in dense],[0]*13)
        self.assertEqual(self.record('VGESFS.LST',11)['normalizacao']['valores'][-1]['valor'],-.898)
        for r in self.records:
            data=r['normalizacao']
            if data and data['tipo']=='serie_13_secoes': self.assertEqual(len(data['valores']),13)

    def test_geometry_reactions_and_stirrups(self):
        geo=self.record('RELDTVGS.LST',71)['normalizacao']['campos']
        self.assertEqual(geo['comprimento']['valor'],1.206)
        reactions=self.record('VGESFS.LST',23)['normalizacao']['campos']
        self.assertEqual(reactions['nome'],'P1A')
        self.assertEqual(reactions['maxima']['valor'],.898)
        stirrups=self.record('ESTRIB.LST',16)['normalizacao']['campos']
        self.assertEqual(stirrups['fim']['valor'],111)
        self.assertEqual(stirrups['espacamento_escolhido']['valor'],15)
        self.assertEqual(stirrups['as_suspensao']['valor'],0)

    def test_similar_beam_does_not_match(self):
        with self.assertRaisesRegex(ValueError,'nao encontrada'): extract(SOURCE,'V5040')

if __name__=='__main__': unittest.main()
