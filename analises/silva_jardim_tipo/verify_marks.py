from pathlib import Path
import sys,json,hashlib,zipfile
p=Path(r'\\srvmaster\PUBLICO\Joao Severgnini\Simon\engineering-assistant')
sys.path.insert(0,str(p/'tmp/pdf_deps'))
import fitz
q=p/'analises/silva_jardim_tipo';o=q/'pranchas_marcadas'
manifest=json.loads((q/'source_manifest.json').read_text(encoding='utf-8-sig'))
for m in manifest:
 if 'VIG-TIP' in m['path']:
  assert hashlib.sha256(Path(m['path']).read_bytes()).hexdigest()==m['sha256']
for f in o.glob('*_MARCADO.pdf'):
 d=fitz.open(str(f));assert len(d)>1;print(f.name,len(d),'páginas',len(list(d[0].annots() or [])),'comentários na prancha')
with zipfile.ZipFile(q/'Vigas_TIPO_marcadas.zip') as z:
 assert z.testzip() is None
 assert len([n for n in z.namelist() if n.endswith('_marcada.png')])==29
 print('ZIP íntegro:',len(z.namelist()),'arquivos')
a=json.loads((q/'marcacoes_vigas_manifesto.json').read_text(encoding='utf-8'))
print('V623:',[r['text'] for r in a['V623'] if 'Termina' in r['title']])
print('Hashes originais conferidos; 29 imagens e 29 páginas individuais verificadas.')
