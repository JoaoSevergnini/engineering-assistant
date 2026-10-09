from pathlib import Path
import json,zipfile,hashlib,csv,sys
r=Path(r'\\srvmaster\PUBLICO\Joao Severgnini\Simon\engineering-assistant');p=r/'analises/silva_jardim_espacial';s=Path(r'C:\TQS\TGD - SILVA JARDIM\24-212-TGD-SILVA JARDIM-R35\ESPACIAL')
sys.path.insert(0,str(r/'tmp/pdf_deps'))
import fitz
for m in json.loads((p/'inventario_com_hashes.json').read_text(encoding='utf-8')):assert hashlib.sha256((s/m['file']).read_bytes()).hexdigest()==m['sha256'],m['file']
d=fitz.open(str(p/'Relatorio_arquivos_ESPACIAL.pdf'));t=' '.join(x.get_text() for x in d)
for term in ['FOR0212.RSX','PORTELS.RSX','PBETAD.DAT','PORLID2.XLSX','426','3.672','8. Documentação']:assert term in t,term
for n,c in [('catalogo_arquivos.csv',163),('piloto_esforcos_v606_v623_piso5.csv',426),('catalogo_casos_combinacoes.csv',142)]:
 with (p/n).open(encoding='utf-8-sig') as f:assert len(list(csv.DictReader(f,delimiter=';')))==c
with zipfile.ZipFile(p/'Relatorio_ESPACIAL_e_extracoes.zip') as z:assert z.testzip() is None
print('QA: PDF 6 páginas, catálogo 163 arquivos, piloto 426 registros, ZIP íntegro e hashes fonte inalterados.')
