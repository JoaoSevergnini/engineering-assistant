import fitz,json,math,collections
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
out=Path(r'P:\Joao Severgnini\Simon\engineering-assistant\analises\atp_s07_lajes_terreo')
inv=json.loads((out/'inventario.json').read_text(encoding='utf8'))
def extract(p):
 paths=[x for x in p.get_drawings() if x.get('layer') in ('3','4','5') and x.get('color')==(0,0,0)]
 par=list(range(len(paths)));grid={}
 def root(i):
  while par[i]!=i:par[i]=par[par[i]];i=par[i]
  return i
 for i,x in enumerate(paths):
  r=x['rect'];q=r+(-.035,-.035,.035,.035);cand=set()
  for xx in range(math.floor(q.x0/10),math.floor(q.x1/10)+1):
   for yy in range(math.floor(q.y0/10),math.floor(q.y1/10)+1):cand.update(grid.get((xx,yy),[]));grid.setdefault((xx,yy),[]).append(i)
  for j in cand:
   s=paths[j]['rect']
   if q.x0<=s.x1 and q.x1>=s.x0 and q.y0<=s.y1 and q.y1>=s.y0:par[root(i)]=root(j)
 groups=collections.defaultdict(list)
 for i in range(len(paths)):groups[root(i)].append(i)
 gs=[]
 for ids in groups.values():
  r=fitz.Rect(paths[ids[0]]['rect']);seg=[]
  for i in ids:
   r|=paths[i]['rect']
   for it in paths[i]['items']:
    if it[0]=='l':seg.append([list(it[1]),list(it[2])])
  coords=[pt for line in seg for pt in line]; r=[min(pt[0] for pt in coords),min(pt[1] for pt in coords),max(pt[0] for pt in coords),max(pt[1] for pt in coords)] if coords else list(r); gs.append(dict(rect=r,segments=seg))
 return gs
# render isolated glyph with scale normalized by its height
# Vertical glyph reading: original text runs bottom to top. Transform (x,y)->(-y,x).
def canon(g,rot=0):
 pts=[]
 for a,b in g['segments']:
  for x,y in (a,b):pts.append((x,y) if rot==0 else (-y,x))
 if not pts:return np.zeros(4096,dtype=np.float32)
 xs,ys=zip(*pts);x0,x1=min(xs),max(xs);y0,y1=min(ys),max(ys);h=y1-y0;w=x1-x0
 if h<.2:return np.zeros(4096,dtype=np.float32)
 scale=min(46/h,54/max(w,.001));ox=(64-w*scale)/2;oy=(64-h*scale)/2
 im=Image.new('L',(64,64));dr=ImageDraw.Draw(im)
 for a,b in zip(pts[::2],pts[1::2]):dr.line((ox+(a[0]-x0)*scale,oy+(a[1]-y0)*scale,ox+(b[0]-x0)*scale,oy+(b[1]-y0)*scale),fill=255,width=3)
 im=im.filter(ImageFilter.GaussianBlur(1));return np.asarray(im,dtype=np.float32).ravel()/255
p=fitz.open(inv[2]['path'])[0];gs=json.loads((out/'training_glyphs.json').read_text());old=json.loads((out/'glyphs_7301.json').read_text());mapping={6:'8',7:'N',8:'3',9:'0',10:'O',11:'5',12:'C',13:'/',14:'2',17:'9',18:'1',27:'4',49:'6',61:'7'}
temps=[];chars=[]
for g,og in zip(gs,old):
 if og['type'] in mapping:temps.append(canon(g));chars.append(mapping[og['type']])
temps=np.array(temps);tn=(temps**2).sum(axis=1)

import re
all_occ=[]
def row(gg,rot,a,b,c,d):
 chars=[]
 for g in gg:
  aa,bb,cc,dd=g['rect'] if rot==0 else [-g['rect'][3],g['rect'][0],-g['rect'][1],g['rect'][2]]
  if aa>=a and cc<=c and bb>=b and dd<=d:
   if dd-bb<.8:ch='-' if cc-aa>1 else '.'
   elif cc-aa<.8 and dd-bb<.8:ch='.'
   else:
    v=canon(g,rot);dist=tn+(v*v).sum()-2*(temps@v);ch=chars_template[int(dist.argmin())]
   chars.append((aa,bb,cc,dd,ch))
 chars.sort();ss='';lastx=None
 for aa,bb,cc,dd,ch in chars:
  if ch=='-' and lastx is not None and abs(aa-lastx)<.15:ss=ss[:-1]+'=';lastx=aa;continue
  ss+=ch;lastx=aa
 return ss
chars_template=chars

alltables={}
for e in inv[2:]:
 n=e['sheet'];gg=json.loads((out/(n+'_glyphs.json')).read_text());ys=[]
 for g in gg:
  a,b,c,d=g['rect']
  if 2502<a<2526 and 100<b<1600 and 4<d-b<6.5:
   yy=(b+d)/2
   if not any(abs(yy-y)<.5 for y in ys):ys.append(yy)
 rows=[]
 for y in sorted(ys):
  vals=[row(gg,0,a,y-4,b,y+4) for a,b in [(2502,2526),(2526,2557),(2557,2591),(2591,2628),(2628,2669)]]
  if all(__import__('re').fullmatch(r'\d+(?:\.\d+)?',z) for z in vals[:4]):
   pos,q,phi,L=map(float,vals[:4])
   if phi in [5,6.3,8,10,12.5,16,20,25,32] and 0<pos<250:rows.append(dict(mark='N'+str(int(pos)),quantity=int(q),diameter_mm=phi,C_cm=L,values=vals))
 alltables[n]=rows;print(n,len(rows),rows[:2])
(out/'tabelas_aco_extraidas.json').write_text(json.dumps(alltables,indent=2),encoding='utf8')
# Restore captions to their proper localized-note class.
occ=json.loads((out/'ocorrencias_extraidas.json').read_text(encoding='utf8'));removed=[o for o in occ if o['id'] in ['7305-O042','7305-O043']];(out/'notas_armaduras_localizadas_furos.json').write_text(json.dumps(removed,indent=2),encoding='utf8');occ=[o for o in occ if o not in removed]
corrections=[];mismatches=[]
for o in occ:
 m=__import__('re').search(r'C=(\d+(?:\.\d+)?)',o['top']) or __import__('re').search(r'C=(\d+(?:\.\d+)?)',o['bottom'])
 if not m:continue
 L=float(m[1]);rows=alltables[o['sheet']];current=next((t for t in rows if t['mark']==o['mark']),None)
 if current and current['diameter_mm']==o['diameter_mm'] and abs(current['C_cm']-L)<1:continue
 candidates=[t for t in rows if t['diameter_mm']==o['diameter_mm'] and abs(t['C_cm']-L)<1]
 if len(candidates)==1:
  old=o['mark'];o['mark']=candidates[0]['mark'];corrections.append(dict(id=o['id'],previous=old,corrected=o['mark'],reason='Unique table row with same diameter and nominal length',C_cm=L))
 else:mismatches.append(dict(id=o['id'],mark=o['mark'],C_cm=L,current_table=current,candidates=candidates))
(out/'ocorrencias_extraidas.json').write_text(json.dumps(occ,indent=2,ensure_ascii=False),encoding='utf8');(out/'conciliacao_marcas_tabela.json').write_text(json.dumps(dict(corrections=corrections,pending=mismatches),indent=2),encoding='utf8');print('corrections',len(corrections),'mismatch',len(mismatches));print(corrections)
