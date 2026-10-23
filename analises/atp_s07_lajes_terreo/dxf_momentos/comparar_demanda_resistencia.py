from pathlib import Path
import json,collections,math,hashlib
from shapely.geometry import shape,Point,LineString,Polygon
from shapely.affinity import affine_transform
from shapely.ops import unary_union
from shapely.strtree import STRtree
r=Path(__file__).parent;root=r.parent
allcaps=json.loads((root/'regioes_capacidades.json').read_text(encoding='utf8'));caps=[s for s in allcaps if s['sheet'] in ['7303','7307']]
fits=json.loads((r/'alinhamento_pdf.json').read_text());dm=json.loads((r/'regioes_negativas_media_picos_resultados.json').read_text(encoding='utf8'));scale=dm['calibration']['scale'];mns=dm['regions'];mnpolys=[shape(s['geometry']) for s in mns];mntree=STRtree(mnpolys)
polys=[]
for s in caps:
 f=fits[s['sheet']];polys.append(affine_transform(shape(s['geometry']),[1/f['sx'],0,0,1/f['sy'],-f['tx']/f['sx'],-f['ty']/f['sy']]))
tree=STRtree(polys)
es=json.loads((r/'entidades.json').read_text(encoding='utf8'));supports=[]
for i,e in enumerate(es):
 d=dict(e['pairs'])
 if e['type']=='POLYLINE' and d.get(8) in ['225','207']:
  pts=[];j=i+1
  while es[j]['type']=='VERTEX':v=dict(es[j]['pairs']);pts.append((float(v[10]),float(v[20])));j+=1
  if len(pts)>3 and pts[0]==pts[-1]:
   p=Polygon(pts).buffer(0)
   if p.area>0:supports.append(p)
support=unary_union(supports)
rows=[dict(id=s['id'],sheet=s['sheet'],marks=s['marks'],families=s['families'],slab=s['slab'],h_cm=s['h_cm'],fck_MPa=s['fck_MPa'],As_cm2_m=s['result']['As_cm2_m'],Mrk_eq=s['result'].get('M_equivalent_tfm_m'),MRd=s['result'].get('MRd_tfm_m'),issues=s['issues'],mmax=0,mmax_outside_support=0,peak_point=None,peak_outside_point=None,mn_ids=set(),mean_refs={},n_intersections=0,other_sheet_overlap=False) for s in caps]
for i,p in enumerate(polys):
 for j in tree.query(p):
  if caps[i]['sheet']!=caps[int(j)]['sheet'] and p.intersection(polys[int(j)]).area>1:rows[i]['other_sheet_overlap']=True
cs=json.loads((r/'componentes_negativos.json').read_text(encoding='utf8'));coverage=unary_union(polys);gaps=[];examples=[]
def lines(g):
 if g.is_empty:return []
 if g.geom_type=='LineString':return [g]
 return [z for q in g.geoms for z in lines(q)] if hasattr(g,'geoms') else []
for c in cs:
 pts=[v for a,b,l in c['segments'] for v in [a,b]];x0=min(v[0] for v in pts);x1=max(v[0] for v in pts)
 if x1-x0<=.02 or max(v[1] for v in pts)-c['base']<=.0002:continue
 base=c['base'];mnidx=int(mntree.nearest(Point((x0+x1)/2,base)));mn=mns[mnidx];mid=mn['id'];mean=abs(mn['mean_line_peaks_signed_tfm_m'])
 for a,b,l in c['segments']:
  if abs(a[0]-b[0])<1e-6:continue
  ma=max(0,(a[1]-base)/scale);mb=max(0,(b[1]-base)/scale);line=LineString([(a[0],base),(b[0],base)])
  def moment(x):return ma+(mb-ma)*(x-a[0])/(b[0]-a[0])
  for ii in tree.query(line,predicate='intersects'):
   i=int(ii);inter=line.intersection(polys[i]);rec=rows[i]
   for seg in lines(inter):
    if seg.length<.01:continue
    rec['n_intersections']+=1;rec['mn_ids'].add(mid);rec['mean_refs'][mid]=mean
    for x,y in seg.coords:
     mm=moment(x)
     if mm>rec['mmax']:rec['mmax']=mm;rec['peak_point']=[x,y]
    for outside in lines(seg.difference(support)):
     for x,y in outside.coords:
      mm=moment(x)
      if mm>rec['mmax_outside_support']:rec['mmax_outside_support']=mm;rec['peak_outside_point']=[x,y]
  for gap in lines(line.difference(coverage).difference(support)):
   if gap.length<1:continue
   x,y=max(gap.coords,key=lambda q:moment(q[0]));mm=moment(x)
   if mm>=1.62:gaps.append(dict(mn=mid,point=[x,y],moment=mm,length=gap.length,geometry=gap.__geo_interface__))
for s in rows:
 s['mn_ids']=sorted(s['mn_ids']);s['Mmean_reference_max']=max(s['mean_refs'].values(),default=0)
 s['eta_peak']=s['mmax_outside_support']/s['Mrk_eq'] if s['Mrk_eq'] else None
 s['eta_mean_reference']=s['Mmean_reference_max']/s['Mrk_eq'] if s['Mrk_eq'] else None
 if not s['n_intersections']:s['assessment']='SEM_DEMANDA_NEGATIVA_INTERSECTADA'
 elif s['issues'] or not s['Mrk_eq']:s['assessment']='PENDENTE_CAPACIDADE'
 elif s['other_sheet_overlap']:s['assessment']='PENDENTE_SOBREPOSICAO_PRANCHAS'
 elif s['eta_peak']>1:s['assessment']='INDICIO_INSUFICIENCIA_LOCAL'
 else:s['assessment']='DEMANDA_LOCAL_NAO_SUPERA_CAPACIDADE'
# Group unmapped demand along adjacent diagram lines for separate document review.
from shapely.geometry import box
bands={float(k):v for k,v in json.loads((r/'regioes_negativas_geometria.json').read_text())['bands'].items()}
ug=unary_union([box(shape(g['geometry']).bounds[0],bands[g['point'][1]][0],shape(g['geometry']).bounds[2],bands[g['point'][1]][1]) for g in gaps])
gap_polys=list(ug.geoms) if hasattr(ug,'geoms') else ([] if ug.is_empty else [ug]);gp=[]
for p in gap_polys:
 relevant=[g for g in gaps if p.covers(Point(g['point']))]
 if not relevant:continue
 peak=max(relevant,key=lambda g:g['moment']);gp.append(dict(geometry=p.__geo_interface__,peak=peak['moment'],point=peak['point'],mn_ids=sorted(set(g['mn'] for g in relevant)),segments=len(relevant)))
gp.sort(key=lambda s:s['peak'],reverse=True)
for i,s in enumerate(gp):s['id']=f'G{i+1:03d}'
summary={n:dict(collections.Counter(s['assessment'] for s in rows if s['sheet']==n)) for n in ['7303','7307']}
out=dict(source_capacities_sha256=hashlib.sha256((root/'regioes_capacidades.json').read_bytes()).hexdigest(),units='tf.m/m',demand_nature='caracteristico',resistance='MRd/1.4 - Concretopy arquivado, sem recalculo',alignment=fits,rows=rows,gaps=gp,summary=summary)
(r/'comparacao_resultados.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print(summary,'GAPS',len(gp));print('WORST',[(s['id'],s['mmax_outside_support'],s['Mrk_eq'],s['eta_peak'],s['mn_ids']) for s in sorted([s for s in rows if s['assessment']=='INDICIO_INSUFICIENCIA_LOCAL'],key=lambda s:s['eta_peak'],reverse=True)[:15]]);print('GAPS TOP',[(s['id'],s['peak'],s['mn_ids']) for s in gp[:10]])
