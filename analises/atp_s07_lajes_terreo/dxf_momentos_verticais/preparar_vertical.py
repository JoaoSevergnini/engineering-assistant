from pathlib import Path
import json,re,collections,math,numpy as np
from shapely.geometry import box
from shapely.ops import unary_union
from shapely.affinity import affine_transform
r=Path(__file__).parent;es=json.loads((r/'entidades.json').read_text(encoding='utf8'));ts=json.loads((r/'textos.json').read_text(encoding='utf8'))
# Canonical axes u=Y_DXF, v=-X_DXF. Negative moments lie above the canonical line.
parent={};segments=[]
def find(a):
 while parent[a]!=a:parent[a]=parent[parent[a]];a=parent[a]
 return a
for e in es:
 d=dict(e['pairs'])
 if e['type']!='LINE' or d.get(8) not in ['214','224']:continue
 a=(round(float(d[20]),4),round(-float(d[10]),4));b=(round(float(d[21]),4),round(-float(d[11]),4))
 for p in [a,b]:parent.setdefault(p,p)
 parent[find(a)]=find(b);segments.append((a,b,d[8]))
g=collections.defaultdict(list)
for a,b,l in segments:g[find(a)].append((a,b,l))
cs=[];nodes=collections.defaultdict(list)
for ss in g.values():
 pp=[p for a,b,l in ss for p in [a,b]];mn=min(p[1] for p in pp);base=17.5*math.floor((mn+.0002)/17.5);cs.append(dict(base=base,segments=ss))
 for u,v in pp:nodes[round(u,3)].append((v,base))
matches=[];numeric=[];iso=[]
for t in ts:
 z=re.match(r'^(-?\d+\.\d+)(tfm/m|/m)$',t['text'])
 if z:
  if z[2]=='/m':iso.append(float(z[1]))
  else:numeric.append(float(z[1]))
 if not z or z[2]!='tfm/m' or float(z[1])>=0:continue
 m=abs(float(z[1]));h=float(t['height']);u=float(t['y'])+len(t['text'])*h;v=-float(t['x'])-h/4;ns=nodes.get(round(u,3),[])
 if not ns:continue
 vv,base=min(ns,key=lambda q:abs(q[0]-v))
 if abs(vv-v)<.02:matches.append((m,vv-base))
a=np.array(matches);keep=abs(a[:,1]-1.223*a[:,0])<.03;a=a[keep];scale=(a[:,0]@a[:,1])/(a[:,0]@a[:,0]);err=abs(a[:,1]/scale-a[:,0]);cal=dict(scale=float(scale),matched=len(matches),inliers=len(a),max_error_tfm_m=float(max(err)),canonical_axes='u=Y_DXF; v=-X_DXF',text_offset='u_text+len(text)*height; v_text-height/4')
# Recover local axes from direct label/vertex associations; local lines may be off the regular mesh.
known_axes=set(17.5*math.floor((min(p[1] for a,b,l in c['segments'] for p in [a,b])+.0002)/17.5) for c in cs)
structural=[]
for e in es:
 d=dict(e['pairs'])
 if e['type']=='LINE' and d.get(8)=='242':structural.append(-float(d[10]))
vindex=collections.defaultdict(set)
for i,c in enumerate(cs):
 for a,b,l in c['segments']:
  for u,v in [a,b]:vindex[round(v,3)].add((u,v,i))
label_bases=collections.defaultdict(list)
for t in ts:
 z=re.match(r'^-(\d+\.\d+)tfm/m$',t['text'])
 if not z:continue
 m=float(z[1]);h=float(t['height']);u=float(t['y']);v=-float(t['x'])-h/4;length=len(t['text'])*h;candidates=[]
 for key in [round(v,3),round(v-.0005,3),round(v+.0005,3)]:
  for uu,vv,ix in vindex.get(key,[]):
   delta=min(abs(uu-(u+length)),abs(uu-u),abs(uu-(u+length/2)))
   if delta<.02 and abs(vv-v)<.001:candidates.append((delta,ix,vv))
 if candidates:
  _,ix,vv=min(candidates);estimate=vv-m*scale;poss=[round(estimate/17.5)*17.5]+structural
  nearest=min(poss,key=lambda z:abs(z-estimate));base=nearest if abs(nearest-estimate)<.025 else estimate
  label_bases[ix].append(base)
for ix,vals in label_bases.items():
 if max(vals)-min(vals)>.04:raise RuntimeError('Conflicting line-axis associations '+str(ix))
 base=float(np.median(vals));cs[ix]['base']=base;cs[ix]['base_source']='LABEL_VERTEX_AXIS';known_axes.add(base)
rebased=[];unlabelled_rebased=[]
for ix,c in enumerate(cs):
 old=17.5*math.floor((min(p[1] for a,b,l in c['segments'] for p in [a,b])+.0002)/17.5)
 if ix not in label_bases:
  minimum=min(p[1] for a,b,l in c['segments'] for p in [a,b]);eligible=[b for b in known_axes if b<=minimum+.0002]
  if eligible:
   nearest=max(eligible)
   if nearest>old+.025:c['base']=nearest;c['base_source']='NEAREST_CONFIRMED_LOCAL_AXIS';unlabelled_rebased.append(ix)
 if abs(c['base']-old)>.025:rebased.append(ix)
cal['local_axis_components_corrected']=len(rebased);cal['local_axis_components_from_nearby_confirmed_axis']=len(unlabelled_rebased)
(r/'auditoria_eixos_locais.json').write_text(json.dumps(dict(corrected_components=rebased,inferred_local_axis_components=unlabelled_rebased,label_associated_components=len(label_bases)),indent=2),encoding='utf8')
valid=[]
for c in cs:
 pp=[p for a,b,l in c['segments'] for p in [a,b]];u0=min(p[0] for p in pp);u1=max(p[0] for p in pp)
 if u1-u0>.02 and max(p[1] for p in pp)-c['base']>.0002:valid.append((c,u0,u1))
bases=sorted(set(c['base'] for c,a,b in valid));bands={b:((bases[i-1]+b)/2 if i else b-17.5,(bases[i+1]+b)/2 if i+1<len(bases) else b+17.5) for i,b in enumerate(bases)}
u=unary_union([box(a,bands[c['base']][0],b,bands[c['base']][1]) for c,a,b in valid]);polys=list(u.geoms) if hasattr(u,'geoms') else [u]
(r/'componentes_negativos.json').write_text(json.dumps(cs),encoding='utf8');(r/'calibracao_amplitude.json').write_text(json.dumps(cal,indent=2),encoding='utf8');(r/'regioes_negativas_geometria.json').write_text(json.dumps(dict(bands=bands,polygons=[p.__geo_interface__ for p in polys],actual_DXF_polygons=[affine_transform(p,[0,-1,1,0,0,0]).__geo_interface__ for p in polys])),encoding='utf8')
print('CALIBRATION',cal,'COMPONENTS',len(cs),'REGIONS',len(polys),'VALUES',len(numeric),'minmax',min(numeric),max(numeric),'ISO',collections.Counter(iso))
