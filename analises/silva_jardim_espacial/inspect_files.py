from pathlib import Path
import json,collections,hashlib
src=Path(r'C:\TQS\TGD - SILVA JARDIM\24-212-TGD-SILVA JARDIM-R35\ESPACIAL')
out=Path(r'\\srvmaster\PUBLICO\Joao Severgnini\Simon\engineering-assistant\analises\silva_jardim_espacial')
a=[]
for f in sorted(src.rglob('*')):
 if not f.is_file():continue
 st=f.stat();b=f.read_bytes()[:12000];zero=b.count(0);textlike=(zero==0 and sum(x<9 or 13<x<32 for x in b)<max(5,len(b)*.02))
 a.append(dict(file=str(f.relative_to(src)),bytes=st.st_size,mtime=st.st_mtime,textlike=textlike,head=b[:160].decode('cp1252',errors='replace')))
 if textlike and f.suffix.lower() in ['.lst','.dat','.txt','.htm','.html','.por','.pod','.rpf']:
  (out/(str(f.relative_to(src)).replace('\\','_')+'.sample.txt')).write_text(f.read_bytes()[:60000].decode('cp1252',errors='replace'),encoding='utf-8')
(out/'inventario.json').write_text(json.dumps(a,ensure_ascii=False,indent=2),encoding='utf-8')
print('FILES',len(a),'BYTES',sum(r['bytes'] for r in a))
for r in a:
 if r['file'].lower().endswith('.e3d'):continue
 print(r['file'],r['bytes'],'TEXT' if r['textlike'] else 'BIN',repr(r['head'][:70]))
