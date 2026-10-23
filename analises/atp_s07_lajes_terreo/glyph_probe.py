import fitz,json,collections,math
from pathlib import Path
out=Path(r'P:\Joao Severgnini\Simon\engineering-assistant\analises\atp_s07_lajes_terreo');e=json.loads((out/'inventario.json').read_text(encoding='utf8'))[2];p=fitz.open(e['path'])[0]
paths=[x for x in p.get_drawings() if x.get('layer')=='5' and x.get('color')==(0,0,0)]
# Merge overlapping stroke bounding boxes. Font glyphs have disjoint x spans.
parent=list(range(len(paths)));grid={}
def root(i):
 while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
 return i
for i,x in enumerate(paths):
 r=x['rect']; q=r+(-.04,-.04,.04,.04); candidates=set()
 for xx in range(math.floor(q.x0/10),math.floor(q.x1/10)+1):
  for yy in range(math.floor(q.y0/10),math.floor(q.y1/10)+1):candidates.update(grid.get((xx,yy),[]));grid.setdefault((xx,yy),[]).append(i)
 for j in candidates:
  s=paths[j]['rect']
  if q.x0<=s.x1 and q.x1>=s.x0 and q.y0<=s.y1 and q.y1>=s.y0:parent[root(i)]=root(j)
groups=collections.defaultdict(list)
for i in range(len(paths)):groups[root(i)].append(i)
glyphs=[];types={}
for ids in groups.values():
 r=fitz.Rect(paths[ids[0]]['rect'])
 for i in ids:r|=paths[i]['rect']
 # keep original segment proportions; normalize translation, quantize native 0.12 point grid
 seg=[]
 for i in ids:
  for item in paths[i]['items']:
   if item[0]=='l':
    a,b=item[1:];seg.append(tuple(sorted([(round((a.x-r.x0)/.12),round((a.y-r.y0)/.12)),(round((b.x-r.x0)/.12),round((b.y-r.y0)/.12))])))
 key=str(sorted(seg));typ=types.setdefault(key,len(types));glyphs.append(dict(type=typ,rect=list(r),ids=ids))
(out/'glyphs_7301.json').write_text(json.dumps(glyphs),encoding='utf8')
# montage representative glyphs
from PIL import Image,ImageDraw
im=Image.new('RGB',(1000,math.ceil(len(types)/15)*65),'white');dr=ImageDraw.Draw(im)
for g in glyphs:
 t=g['type']
 if 'seen' not in locals():seen=set()
 if t in seen:continue
 seen.add(t);r=fitz.Rect(g['rect'])+(-.5,-.5,.5,.5);pix=p.get_pixmap(matrix=fitz.Matrix(4,4),clip=r,annots=False);piece=Image.frombytes('RGB',[pix.width,pix.height],pix.samples);piece.thumbnail((55,40));x=(t%15)*66;y=(t//15)*65;im.paste(piece,(x,y));dr.text((x,y+42),str(t),fill='red')
im.save(out/'glyph_montage.png');print('groups',len(glyphs),'types',len(types))
