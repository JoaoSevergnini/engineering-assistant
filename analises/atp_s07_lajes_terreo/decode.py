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
for e in inv[2:]:
 n=e['sheet'];p=fitz.open(e['path'])[0];gg=json.loads((out/(n+'_glyphs.json')).read_text()) if (out/(n+'_glyphs.json')).exists() else extract(p)
 for g in gg:
  scores=[]
  for rot in (0,90):
   v=canon(g,rot);dd=tn+(v*v).sum()-2*(temps@v);ii=int(dd.argmin());scores.append((float(dd[ii]),rot,chars[ii]))
  score,rot,char=min(scores);g.update(char=char,rotation=rot,score=score)
 # seed N and reconstruct full calls locally; include only glyphs matching orientation with plausible baseline
 lines=[]
 for g in gg:
  if g['char']!='N' or g['score']>50:continue
  rot=g['rotation'];r=g['rect'];
  def tr(q):
   a,b,c,d=q['rect'];return (a,b,c,d) if rot==0 else (-d,a,-b,c)
  a,b,c,d=tr(g);hh=d-b
  if not 3<hh<9:continue
  cand=[]
  for h in gg:
   aa,bb,cc,dd=tr(h)
   if aa>=a-30 and cc<=a+180 and bb>=b-2 and dd<=d+2:
    if dd-bb<1:ch='-' if cc-aa>1 else '.'
    elif cc-aa<.5:ch='1' if dd-bb>hh*.7 else '.'
    else:
     v=canon(h,rot);dist=tn+(v*v).sum()-2*(temps@v);ch=chars[int(dist.argmin())]
    cand.append((aa,cc,ch))
  cand.sort();s='';last=None
  for aa,cc,ch in cand:
   if last is not None and aa-last>hh*.6:s+=' '
   s+=ch;last=cc
  if 'N' in s:lines.append(dict(text=s,rect=r,rotation=rot,seed_score=g['score']))
 (out/(n+'_glyph_lines.json')).write_text(json.dumps(lines,indent=2),encoding='utf8');(out/(n+'_glyphs.json')).write_text(json.dumps(gg),encoding='utf8');print(n,len(gg),len(lines),flush=True)


