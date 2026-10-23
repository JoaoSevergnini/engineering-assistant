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
for e in inv[2:]:
 n=e['sheet'];gg=json.loads((out/(n+'_glyphs.json')).read_text());p=fitz.open(e['path'])[0];paths=p.get_drawings();segments=[]
 for x in paths:
  if x.get('layer') not in ('3','8'):continue
  for it in x['items']:
   if it[0]=='l':segments.append(dict(a=list(it[1]),b=list(it[2]),layer=x.get('layer')))
 markers=[[(x['rect'].x0+x['rect'].x1)/2,(x['rect'].y0+x['rect'].y1)/2] for x in paths if x.get('layer')=='6' and any(it[0]=='c' for it in x['items'])]
 table=json.loads((out/'tabelas_aco_extraidas.json').read_text(encoding='utf8')).get(n,[])
 occurrences=[]
 for g in gg:
  if g['char']!='N' or g['score']>35:continue
  rot=g['rotation'];x0,y0,x1,y1=g['rect'] if rot==0 else [-g['rect'][3],g['rect'][0],-g['rect'][1],g['rect'][2]]
  if not 3<y1-y0<9 or g['rect'][0]>2300:continue
  top=row(gg,rot,x0-32,y0-2,x0+185,y1+2);bot=row(gg,rot,x0-32,y0+6.3,x0+185,y1+10.8)
  seedtext=row(gg,rot,x0-.25,y0-2,x0+185,y1+2)
  nominal=re.search(r'C=(\d+(?:\.\d+)?)',top) or re.search(r'C=(\d+(?:\.\d+)?)',bot)
  candidates=[]
  for tt in table:
   if not seedtext.startswith(tt['mark']):continue
   remainder=seedtext[len(tt['mark']):];remainder=remainder.lstrip('O');pm=re.match(r'(\d+(?:\.\d*)?)',remainder)
   token=pm[1] if pm else '';actual=f"{tt['diameter_mm']:g}";Cmatch=nominal is not None and nominal[1]==f"{tt['C_cm']:g}"
   score=6 if Cmatch else 0
   if token==actual:score+=4
   elif token.startswith(actual) or (token and actual.startswith(token)):score+=3
   elif token and actual.endswith(token) and Cmatch:score+=2
   elif not token and Cmatch:score+=1
   else:continue
   if score>=3:candidates.append((score,tt))
  candidates.sort(key=lambda t:-t[0]);inferred=None
  if not candidates and nominal:
   near=re.match(r'N(\d+)',seedtext);prefix=near[1] if near else ''
   global_matches=[tt for tt in table if nominal[1]==f"{tt['C_cm']:g}" and (tt['mark'][1:].startswith(prefix) or prefix.startswith(tt['mark'][1:]))]
   if len(global_matches)==1:candidates=[(10,global_matches[0])]
  if candidates and (len(candidates)==1 or candidates[0][0]>candidates[1][0]):inferred=candidates[0][1]
  m=re.search(r'N(\d+)O(\d+(?:\.\d+)?)',top)
  if inferred:mark=inferred['mark'];dia=inferred['diameter_mm']
  elif m:mark='N'+m[1];dia=float(m[2])
  else:continue
  ms=re.search(r'C/(\d+(?:\.\d+)?)',top) or re.search(r'C/(\d+(?:\.\d+)?)',bot) or re.search(r'C(\d+(?:\.\d+)?)C=',top) or re.search(r'/(\d+(?:\.\d+)?)C=',top)
  spacing=float(ms[1]) if ms else None
  if dia not in [5,6.3,8,10,12.5,16,20,25,32]:continue
  if spacing is not None and not 5<=spacing<=40:spacing=None
  bars=[]
  def point(pt):return pt if rot==0 else [-pt[1],pt[0]]
  raw=[]
  for seg in segments:
   if seg['layer']!='8':continue
   a,b=point(seg['a']),point(seg['b']);left,right=sorted([a[0],b[0]])
   if abs(a[1]-b[1])<.1 and right-left>4 and 1<a[1]-y1<13:raw.append((left,a[1],right))
  raw.sort(key=lambda z:(round(z[1],1),z[0]));merged=[]
  for left,yy,right in raw:
   if merged and abs(yy-merged[-1][1])<.15 and left-merged[-1][2]<=6.0:merged[-1]=(merged[-1][0],yy,max(right,merged[-1][2]))
   else:merged.append((left,yy,right))
  bars=[z for z in merged if z[0]-3<=x0<=z[2]+3 and z[2]-z[0]>15]
  geom=None;status='PENDING_BAR_GEOMETRY'
  if len(bars)==1:
   left,ybar,right=bars[0];axes=[]
   for seg in segments:
    if seg['layer']!='3':continue
    a,b=point(seg['a']),point(seg['b']);up,down=sorted([a[1],b[1]])
    if abs(a[0]-b[0])<.1 and down-up>12 and left-.1<=a[0]<=right+.1 and up+.1<ybar<down-.1:axes.append((a[0],up,down))
   axes=list(set(axes)); axes=[ax for ax in axes if any(abs(point(mk)[0]-ax[0])<.85 and abs(point(mk)[1]-ybar)<.85 for mk in markers)]
   if len(axes)==1:
    xx,up,down=axes[0];geom=[left,up,right,down];status='NOMINAL_RECTANGLE_CANDIDATE'
   else:status='PENDING_DISTRIBUTION_AXIS_'+str(len(axes))
  elif len(bars)>1:status='PENDING_BAR_AMBIGUITY'
  actual_rot=rot
  association='PARALLEL_TEXT_BAR_WITH_CIRCLE'
  if geom is None and spacing is not None:
   # Search both bar directions, explicitly requiring a circle and perpendicular distribution axis.
   options=[];cx=(g['rect'][0]+g['rect'][2])/2;cy=(g['rect'][1]+g['rect'][3])/2
   for brot in (rot,):
    def bt(pt):return pt if brot==0 else [-pt[1],pt[0]]
    raw=[]
    for seg in segments:
     if seg['layer']!='8':continue
     aa,bb=bt(seg['a']),bt(seg['b']);ll,rr=sorted([aa[0],bb[0]])
     if abs(aa[1]-bb[1])<.1 and rr-ll>3 and 1<aa[1]-y1<13:raw.append((ll,aa[1],rr))
    raw.sort(key=lambda z:(round(z[1],1),z[0]));merged=[]
    for ll,yy,rr in raw:
     if merged and abs(yy-merged[-1][1])<.15 and ll-merged[-1][2]<=6.0:merged[-1]=(merged[-1][0],yy,max(rr,merged[-1][2]))
     else:merged.append((ll,yy,rr))
    for mk in markers:
     distance=math.hypot(mk[0]-cx,mk[1]-cy)
     if distance>120:continue
     mx,my=bt(mk)
     for ll,yy,rr in merged:
      if abs(yy-my)>.85 or not ll-.2<mx<rr+.2 or rr-ll<12:continue
      axes=[]
      for seg in segments:
       if seg['layer']!='3':continue
       aa,bb=bt(seg['a']),bt(seg['b']);up,down=sorted([aa[1],bb[1]])
       if abs(aa[0]-bb[0])<.1 and abs(aa[0]-mx)<.85 and up+.1<my<down-.1 and down-up>12:axes.append((up,down))
      axes=list(set(axes))
      if len(axes)==1:options.append((distance,brot,[ll,axes[0][0],rr,axes[0][1]]))
   dedup={}
   for dd,rr,bb in options:
    kk=(rr,tuple(round(z,1) for z in bb));vv=(round(dd,3),rr,tuple(bb))
    if kk not in dedup or vv[0]<dedup[kk][0]:dedup[kk]=vv
   options=sorted(dedup.values())
   if options and (len(options)==1 or options[1][0]-options[0][0]>4):
    distance,actual_rot,geom=options[0];geom=list(geom);status='NOMINAL_RECTANGLE_CANDIDATE';association='NEAREST_CIRCLE_AND_PERPENDICULAR_AXIS_REQUIRES_VISUAL_REVIEW'
  box=(geom if actual_rot==0 or geom is None else [geom[1],-geom[2],geom[3],-geom[0]])
  if any(abs(g['rect'][0]-h['label_rect'][0])<1 and abs(g['rect'][1]-h['label_rect'][1])<1 for h in occurrences):continue
  occurrences.append(dict(id=n+'-O'+str(len(occurrences)+1).zfill(3),sheet=n,mark=mark,diameter_mm=dia,spacing_cm=spacing,As_individual_cm2_m=math.pi*(dia/10)**2/4*100/spacing if spacing else None,top=top,bottom=bot,label_rect=g['rect'],rotation=rot,bar_rotation=actual_rot,association=association,region_pdf=box,geometry_status=status,bar_candidates=bars))
 all_occ.extend(occurrences);print(n,len(occurrences),collections.Counter(x['geometry_status'] for x in occurrences),flush=True)
(out/'ocorrencias_extraidas.json').write_text(json.dumps(all_occ,indent=2,ensure_ascii=False),encoding='utf8')


