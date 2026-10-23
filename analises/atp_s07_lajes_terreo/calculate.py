import sys,math,json,hashlib,inspect,collections
from pathlib import Path
from dataclasses import asdict
import fitz
from shapely.geometry import box,Polygon,mapping
from shapely.ops import unary_union
sys.path.insert(0,r'P:\Joao Severgnini\Simon\concretopy')
from concretopy import Barra,Aco,Concreto,SecaoRetangular,CamadaArmaduraLongitudinal,verificar_flexao_viga_retangular
out=Path(r'P:\Joao Severgnini\Simon\engineering-assistant\analises\atp_s07_lajes_terreo');inv=json.loads((out/'inventario.json').read_text(encoding='utf8'));occ=json.loads((out/'ocorrencias_extraidas.json').read_text(encoding='utf8'))
def polygons(g):
 if g.is_empty:return []
 if g.geom_type=='Polygon':return [g]
 return [p for gg in g.geoms for p in polygons(gg)] if hasattr(g,'geoms') else []
# Section resistance: exactly preserve the yielded steel tensile resultant and its centroid.
cache={}
def calc(fams,h,fck,offset):
 key=(tuple(fams),h,fck,offset)
 if key in cache:return cache[key]
 physical=[]
 for phi,sp in fams:
  ar=Barra(phi).area_cm2*100/sp;fyk=600 if phi==5 else 500;d=h-3-offset-phi/20;physical.append(dict(phi=phi,s=sp,As=ar,fyk=fyk,d=d))
 tension=sum(a['As']*(a['fyk']/1.15) for a in physical);aseq=tension/(500/1.15);deq=sum(a['As']*(a['fyk']/1.15)*a['d'] for a in physical)/tension
 phi=min(a['phi'] for a in physical);ab=Barra(phi).area_cm2;nb=max(20,math.ceil(aseq/ab));width=nb*ab*100/aseq
 # Geometry parameterization keeps effective cover exactly 3.0 cm: 2.5 + 0.5.
 # The numerical 5 mm stirrup parameter is NOT a physical slab stirrup; no automatic depths are used.
 sec=SecaoRetangular(width,h,2.5,5)
 if deq>sec.d(phi) and deq-sec.d(phi)<1e-8:deq=sec.d(phi)
 rr=verificar_flexao_viga_retangular(sec,Concreto(fck),Aco(500),[CamadaArmaduraLongitudinal(nb,Barra(phi),deq)],gamma_c=1.4,gamma_s=1.15,gamma_f=1.4,verificar_armadura_minima=False)
 raw=asdict(rr);x=rr.x_cm if hasattr(rr,'x_cm') else raw.get('linha_neutra_cm')
 mrd=raw.get('mrd_kncm');
 res=dict(As_cm2_m=sum(a['As'] for a in physical),families=physical,As_equivalent_CA50_cm2_m=aseq,d_equivalent_cm=deq,normalized_strip_width_cm=width,normalized_bar_count=nb,normalized_bar_phi_mm=phi,concretopy_result=raw)
 if mrd is not None:res.update(MRd_tfm_m=mrd*100/width/980.665,M_equivalent_tfm_m=mrd*100/width/980.665/1.4)
 else:res.update(MRd_tfm_m=None,M_equivalent_tfm_m=None)
 if x:
  strains=[]
  for a in physical:
   eps=raw['parametros']['eps_c_adotada']*(a['d']-x)/x
   strains.append(eps>=a['fyk']/1.15/210000)
  res['all_real_families_yield']=all(strains)
 if not res.get('all_real_families_yield',False):res.update(MRd_tfm_m=None,M_equivalent_tfm_m=None)
 cache[key]=res;return res
# Record source geometry and native material polygons.
models={}
for e in inv[2:]:
 n=e['sheet'];p=fitz.open(e['path'])[0];paths=p.get_drawings();green=[];diags=collections.defaultdict(set)
 for path in paths:
  if path.get('layer')=='12' and path.get('fill') and path['fill'][1]>.9 and path['fill'][0]>.5:
   pts=[]
   for it in path['items']:
    if it[0]=='l':pts.extend([list(it[1]),list(it[2])])
   if len(pts)>=3:
    pg=Polygon(pts).buffer(0)
    if pg.area>10:green.append(pg)
  if path.get('layer')=='1':
   for it in path['items']:
    if it[0]!='l':continue
    a,b=it[1:];dx=b.x-a.x;dy=b.y-a.y
    if abs(dx)>8 and abs(dy)>8 and max(abs(dx),abs(dy))<250:
     k=tuple(round(v,1) for v in [min(a.x,b.x),min(a.y,b.y),max(a.x,b.x),max(a.y,b.y)]);diags[k].add(1 if dx*dy>0 else -1)
 holes=unary_union([box(*k) for k,v in diags.items() if len(v)==2 and k[2]<2200])
 models[n]=dict(green=unary_union(green),holes=holes)
# Profiles: only explicitly identified slab interiors. The continuous main area remains h=20 as instructed.
special=[]
for x0,x1,ns in [(733.44,840.36,['L2','L4','L6']),(1639.68,1746.48,['L3','L5','L7'])]:
 for (y0,y1,h),name in zip([(1424.36,1504.04,15),(1511.24,1550.12,20),(1557.2,1636.88,15)],ns):special.append((name,h,box(x0,y0,x1,y1)))
for x0,x1,ns in [(544.92,770.28,['LF701','LF702']),(893.52,1098.24,['LF703','LF704'])]:
 for (y0,y1),name in zip([(397.4,475.76),(484.88,565.76)],ns):special.append((name,30,box(x0,y0,x1,y1)))
# Top reservoir covers use local drawings, no extension of the main 20 cm section.
for name,x0,x1,y0,y1 in [('LT701',535,778,147,227),('LT702',535,778,235,315),('LT703',885,1107,147,227),('LT704',885,1107,235,315)]:special.append((name,12,box(x0,y0,x1,y1)))
allregions=[]
for n in [str(i) for i in range(7301,7309)]:
 mainrot=90 if n in ['7302','7304','7306','7308'] else 0;face='POS' if n in ['7301','7302','7305','7306'] else 'NEG';part=1 if int(n)<7305 else 2
 relevant=[o for o in occ if o['sheet']==n and o['region_pdf'] and o['spacing_cm'] and o['bar_rotation']==mainrot]
 # Deduplicate accidental repeated readings of exactly the same physical bar/axis.
 uniq={}
 for o in relevant:
  k=(o['mark'],o['diameter_mm'],o['spacing_cm'],tuple(round(v,1) for v in o['region_pdf']));uniq[k]=o
 relevant=list(uniq.values());cells=[]
 for o in relevant:
  pg=box(*o['region_pdf']).difference(models[n]['holes']);pending=pg;new=[]
  for poly,ids in cells:
   inter=poly.intersection(pg)
   if inter.area>.5:
    rem=poly.difference(pg)
    if rem.area>.5:new.append((rem,ids))
    new.append((inter,ids+[o['id']]));pending=pending.difference(poly)
   else:new.append((poly,ids))
  if pending.area>.5:new.append((pending,[o['id']]))
  cells=new
 lookup={o['id']:o for o in relevant};outcells=[]
 for poly,ids in cells:
  for pp in polygons(poly):
   if pp.area<3:continue
   # Material split from native C35 shading. Nonshaded zone is C40 per drawing legend.
   for mat,pg in [(35,pp.intersection(models[n]['green'])),(40,pp.difference(models[n]['green']))]:
    for qq in polygons(pg):
     if qq.area<3:continue
     profs=[];remain=qq
     if part==1:
      for name,h,sp in special:
       ss=remain.intersection(sp)
       if ss.area>3:profs.append((name,h,ss));remain=remain.difference(sp)
     if remain.area>3:
      if part==1:
       top_remaining=remain.intersection(box(0,0,2200,350))
       if top_remaining.area>3:profs.append(('LT - contorno a conciliar',12,top_remaining));remain=remain.difference(top_remaining)
      if remain.area>3:profs.append(('L1/L8 - localizar no mapa' if part==1 else 'L9',20,remain))
     for slab,h,gg in profs:
      for rr in polygons(gg):
       if rr.area<3:continue
       fams=[];ambig=[];detail=[];base=[]
       for oid in ids:
        o=lookup[oid];f=(o['diameter_mm'],o['spacing_cm']);detail.append(o)
        if face=='POS' and f==(8.,14.) and h==20:base.append(o)
        else:
         if any(z['mark']==o['mark'] and (z['diameter_mm'],z['spacing_cm'])==f for z in detail[:-1]):continue
         if f in fams:ambig.append('Sobreposicao de familias iguais com marcas distintas: confirmar traspasse ou soma.')
         fams.append(f)
       if base:fams.append((8.,14.))
       if not fams:continue
       # Vertical direction sits over horizontal families. Use local horizontal envelopes when reconstructed.
       offset=0.;offset_source='HORIZONTAL_FIRST_LAYER'
       if mainrot==90:
        nh=str(int(n)-1);hs=[o for o in occ if o['sheet']==nh and o['region_pdf'] and o['spacing_cm'] and o['bar_rotation']==0 and box(*o['region_pdf']).intersects(rr)]
        if hs:offset=max(o['diameter_mm'] for o in hs)/10;offset_source='MAX_HORIZONTAL_DIAMETER_INTERSECTING_REGION_CONSERVATIVE'
        else:offset=2.;offset_source='HYPOTHESIS_20MM_HORIZONTAL_ENVELOPE_NO_LOCAL_MAPPING'
       if face=='NEG' and len(set((z['mark'],z['diameter_mm'],z['spacing_cm']) for z in detail))>1:ambig=['Capacidades individuais; soma pendente de ancoragem conforme orientacao de Joao.']
       result=calc(tuple(sorted(fams)),h,mat,offset)
       individual=[]
       if ambig:
        done=set()
        for z in detail:
         kk=(z['mark'],z['diameter_mm'],z['spacing_cm'])
         if kk in done:continue
         done.add(kk);individual.append(dict(mark=z['mark'],diameter_mm=z['diameter_mm'],spacing_cm=z['spacing_cm'],capacity=calc(((z['diameter_mm'],z['spacing_cm']),),h,mat,offset)))
       if ambig:result=dict(result,M_equivalent_tfm_m=None,MRd_tfm_m=None)
       outcells.append(dict(sheet=n,face=face,direction='H' if mainrot==0 else 'V',slab=slab,h_cm=h,fck_MPa=mat,geometry=mapping(rr),occurrences=ids,marks=sorted(set(x['mark'] for x in detail)),families=fams,base_lap_count=len(base),horizontal_offset_cm=offset,offset_source=offset_source,issues=ambig,individual_capacities=individual,result=result,status='NOMINAL_CAPACITY_GEOMETRY_REVIEW_REQUIRED'))
 grouped=collections.defaultdict(list)
 for r in outcells:
  key=(r['slab'],r['h_cm'],r['fck_MPa'],tuple(tuple(x) for x in sorted(r['families'])),r['horizontal_offset_cm'],r['offset_source'],tuple(r['issues']))
  grouped[key].append(r)
 merged_cells=[]
 for records in grouped.values():
  union=unary_union([Polygon(r['geometry']['coordinates'][0],r['geometry']['coordinates'][1:]) for r in records]).buffer(.001).buffer(-.001)
  for pp in polygons(union):
   r=dict(records[0]);r['geometry']=mapping(pp);members=[z for z in records if Polygon(z['geometry']['coordinates'][0]).intersection(pp).area>1]
   r['occurrences']=sorted(set(i for z in members for i in z['occurrences']));r['marks']=sorted(set(i for z in members for i in z['marks']));r['base_lap_count']=max(z['base_lap_count'] for z in members) if members else 0;merged_cells.append(r)
 outcells=merged_cells
 outcells.sort(key=lambda r:(Polygon(r['geometry']['coordinates'][0]).centroid.y,Polygon(r['geometry']['coordinates'][0]).centroid.x))
 for i,r in enumerate(outcells,1):r['id']=n+'-R'+str(i).zfill(3)
 allregions.extend(outcells);print(n,'regions',len(outcells),'holes',len(polygons(models[n]['holes'])),flush=True)
(out/'regioes_capacidades.json').write_text(json.dumps(allregions,ensure_ascii=False,indent=2),encoding='utf8')
provenance=dict(interface='concretopy.verificar_flexao_viga_retangular',source_file=inspect.getfile(verificar_flexao_viga_retangular),source_sha256=hashlib.sha256(Path(inspect.getfile(verificar_flexao_viga_retangular)).read_bytes()).hexdigest(),gamma_c=1.4,gamma_s=1.15,gamma_f=1.4,cover_cm=3.,method='Single equivalent yielded resultant: force-weighted depth, CA50 reference area, normalized width and integer bar count; real-family yield checked separately. Effective cover=2.5+0.5cm numerical parameterization, no physical slab stirrups.',regions=len(allregions),unique_calculations=len(cache))
(out/'proveniencia_calculos.json').write_text(json.dumps(provenance,indent=2,ensure_ascii=False),encoding='utf8');print(provenance)

