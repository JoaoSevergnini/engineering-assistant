from pathlib import Path
import sys,json,math,copy,contextlib,io,hashlib,inspect
from dataclasses import asdict
R=Path(r'\\srvmaster\PUBLICO\Joao Severgnini\Simon\engineering-assistant');O=R/'analises/atp_s07_vigas_terreo/rodada_05_relatorio_global'
sys.path[:0]=[str(R/'tools/reinforcement_checks'),str(R.parent/'concretopy')]
import concretopy as api
from shear_review import design_shear,public_shear_api
A=json.loads((O/'entradas_vigas_50.json').read_text(encoding='utf-8'));T=json.loads((O/'tqs_operacional_atual.json').read_text(encoding='utf-8'))
FACTOR=1.4*9.80665
bar=lambda n,p,l=None:{'count':n,'phi':p,'layers':l or [n]}
def interpolate(values,x,L):
 u=max(0,min(12,x/L*12));i=min(int(u),11);return values[i]+(values[i+1]-values[i])*(u-i)
def extreme(series,L,a,z,quantity='shear',sign=1):
 choices=[]
 for s in series:
  points=[a,z]+[k*L/12 for k in range(13) if a<=k*L/12<=z]
  for x in points:
   v=interpolate(s['original_values'],x,L);value=abs(v) if quantity=='shear' else max(0,sign*v)
   choices.append({'magnitude':value,'signed_value':v,'model_local_m':x,'source':s['source'],'series':s['label']})
 return max(choices,key=lambda x:x['magnitude'])
def flexure(bw,h,phi,cfg,fck):
 sec=api.SecaoRetangular(bw,h,3.5,diametro_estribo_mm=phi)
 layers=[api.CamadaArmaduraLongitudinal(n,api.Barra(cfg['phi'])) for n in cfg['layers']]
 ds=api.calcular_alturas_uteis_camadas(sec,layers);layers=[api.CamadaArmaduraLongitudinal(x.numero_barras,x.barra,d) for x,d in zip(layers,ds)]
 result=api.verificar_flexao_viga_retangular(sec,api.Concreto(fck),api.Aco(500),layers,gamma_f=1.4,verificar_armadura_minima=True)
 rr=asdict(result)
 mdmin=.8*(bw*h*h/6)*api.Concreto(fck).fctk_sup*.1 # kN.cm; demand prescribed by consulted 17.3.5.2.1, not a capacity calculation
 rr['minimum_by_actual_section']={'source':'NBR6118:2023 17.3.5.2.1; required moment 0.8W0fctk,sup and absolute rate0.15%; compare to official Concretopy capacity','Mk_min_eq_tfm':mdmin/FACTOR/100,'As_absolute_min_cm2':.0015*bw*h,'moment_passes':rr['mrd_kncm'] is not None and rr['mrd_kncm']>=mdmin,'area_passes':rr['as_total_cm2']>=.0015*bw*h}
 return rr
# Face offsets in metres from support axes, independently read from 7201 block geometry or 7202/7214 column faces.
# V15 P756/P761 keep pillar faces: NB8.38 confirmed, below beam. Other listed domains match actual drawn block-face boundaries.
manual_faces={
 ('V4','1'):(.20,.45,'P746 pilar40cm; P747 bloco90cm:7201+7202'),
 ('V5','1'):(1.15,1.35,'P741 bloco230cm; P742 bloco270cm:7201'),
 ('V15','1'):(1.35,.45,'P757 bloco270cm; P756 pilar90cm, NB8.38 confirmado'),
 ('V15','2'):(.45,1.35,'P756 pilar90cm; P760 bloco270cm:7201'),
 ('V15','3'):(1.35,.972,'P760 bloco270cm; P758 contorno triangular7201 medido nas cotas'),
 ('V15','4'):(1.487,.20,'P758 contorno triangular7201; P761 pilar40cm, NB8.38 confirmado'),
 ('V34','1'):(1.35,1.35,'P760/P747 blocos270cm na direcao longitudinal:7201'),
 ('V37','1'):(1.35,1.35,'P725/P712:blocos270cm na direcao longitudinal7201'),
 ('V33','1'):(1.15,.15,'P794 bloco230cm longitudinal; receptoraV19 largura30cm'),
 ('V40','1'):(1.15,.15,'P796 bloco230cm longitudinal; receptoraV20 largura30cm'),
 ('V36','1'):(.095,1.35,'V5 largura19cm; P735 bloco270cm:7201'),
 ('V18','1'):(.15,.35,'V23 largura30cm; PC45C bloco70cm'),('V18','2'):(.35,.35,'PC45C/PC46C blocos70cm:7201'),
 ('V16','1'):(.35,.35,'PC40C/PC41C blocos70cm:7201')}
# V35 point-charge blocks and V15 receiving width, independently shown in7201/7202.
manual_faces[('V35','1')]=(.35,.35,'PC36C/PC30C blocos70cm')
manual_faces[('V35','2')]=(.35,.20,'PC30C bloco70cm; V15 largura40cm')
# Actual point-load block dimensions from7201 replace generic19cm node widths for shear only.
for tk in ['1','2','3','4','5','6']:
 manual_faces[('V21',tk)]=(.15 if tk=='1' else .35,.15 if tk=='6' else .35,'7201:PC55C/PC56C/PC57C/PC59C/PC60C blocos70cm; extremos em V23/V22 largura30cm; conferir PC54C na ligacaoV23')
# Vector intersections for sloping V47 and vertical V48 using documented column/block contours.
blocks=json.loads((O/'evidencias/apoios_blocos_medidos.json').read_text(encoding='utf-8'))
def ray_exit(record,u,block=True):
 centre=record['column_center_pt'];polys=record['block_polygons_pt'] if block else [[(record['column_bounds_pt'][0],record['column_bounds_pt'][1]),(record['column_bounds_pt'][2],record['column_bounds_pt'][1]),(record['column_bounds_pt'][2],record['column_bounds_pt'][3]),(record['column_bounds_pt'][0],record['column_bounds_pt'][3])]]
 hits=[]
 for poly in polys:
  for p,q in zip(poly,poly[1:]+poly[:1]):
   dx,dy=q[0]-p[0],q[1]-p[1];det=u[0]*(-dy)-(-dx)*u[1]
   if abs(det)<1e-9:continue
   px,py=p[0]-centre[0],p[1]-centre[1]
   tt=(px*(-dy)-(-dx)*py)/det;ss=(u[0]*py-px*u[1])/det
   if tt>=-1e-8 and -1e-8<=ss<=1+1e-8:hits.append(tt)
 assert hits
 return max(hits)/(72/2.54) # points/(points per meter at drawing1:100)
for beam,left,right in [('V47','P751','P741'),('V48','P767','P758')]:
 p=blocks[left]['column_center_pt'];q=blocks[right]['column_center_pt'];norm=math.dist(p,q);u=((q[0]-p[0])/norm,(q[1]-p[1])/norm)
 manual_faces[(beam,'1')]=(ray_exit(blocks[left],u),ray_exit(blocks[right],(-u[0],-u[1])),'Intersecao do eixo entre pilares com contornos cotados7201; medicao vetorial, sem usar comprimento dos estribos')
results=[]
with contextlib.redirect_stdout(io.StringIO()):
 for c in A['cases']:
  bid,model,token=c['beam_id'],c['model_name'],c['span_token'];bw,h=c['section_cm'];tb=T[model];geo=next(g for g in tb['geometry'] if g['span_token']==token);L=geo['length_m'];qs=[s for s in tb['series'] if s['span_token']==token and s['label'].startswith('Q')];ms=[s for s in tb['series'] if s['span_token']==token and s['label'] in ['M MN.','M MX.']]
  bal=token.endswith('B');index=int(token.replace('B',''))-(2 if any(g['span_token'].endswith('B') for g in tb['geometry']) else 1);left=None if bal else tb['supports'][index];right=tb['supports'][0] if bal else tb['supports'][index+1]
  phi=c['shear']['stirrup']['diameter_mm'];defaultst=copy.deepcopy(c['shear']['stirrup'])
  if bid=='V17' and int(token.replace('B',''))>=6:defaultst['spacing_cm']=10
  a=0 if left is None else max(0,left['width_m']/2-left['depev_m']);z=min(L,L+right['depev_m']-right['width_m']/2);domain_source='Faces representadas no TQS; referencia de calculo, sem substituir geometria da forma';physical=False
  if (bid,token) in manual_faces:
   lf,rf,domain_source=manual_faces[(bid,token)];a=max(0,lf-(left['depev_m'] if left else 0));z=min(L,L+right['depev_m']-rf);physical=True
  if bid in ['V31','V41'] and token=='2':a,z=0,L;physical=False;domain_source='Subdivisao numerica dentro/junto ao apoio; nao e vao fisico independente'
  if z<=a:a,z=0,L;physical=False
  item={'beam_id':bid,'model_name':model,'span_token':token,'section_cm':[bw,h],'model_length_m':L,'support_names':[left['name'] if left else 'EXTREMIDADE_LIVRE',right['name']],'documentary_notes':c['documentary_notes'],'source_crop':c['source_crop'],'section_geometry_status':c['section_geometry_status'],'domain':{'start_model_m':a,'end_model_m':z,'source':domain_source,'physical_block_faces_proved':physical},'positive':{},'negative':[],'shear':[]}
  pmax=extreme(ms,L,0,L,quantity='moment');cfg=c['positive']['composition'];item['positive']={'demand':pmax,'configuration':cfg,'scenarios':[]}
  for fc in [35,40]:
   rr=flexure(bw,h,phi,cfg,fc);cap=None if rr['mrd_kncm'] is None else rr['mrd_kncm']/100/FACTOR
   minimum=rr['minimum_by_actual_section'];item['positive']['scenarios'].append({'fck_mpa':fc,'concretopy':rr,'Mk_eq_tfm':cap,'capacity_passes':cap is not None and cap>=pmax['magnitude'],'minimum_passes':None if pmax['magnitude']==0 else minimum['moment_passes'] and minimum['area_passes']})
  for nf in c['negative_faces']:
   end=nf['end'];pos=0 if end=='left' else L
   support=left if end=='left' else right
   interval=[0,a] if end=='left' else [z,L]
   nd=extreme(ms,L,*interval,quantity='moment',sign=-1)
   hh=nf.get('section_height_cm',h);ng={'end':end,'support':support['name'] if support else 'EXTREMIDADE_LIVRE','demand':nd,'configuration':nf['outer_composition'],'section_height_cm':hh,'geometry_pending':nf.get('geometry_pending',False),'scenarios':[]}
   for fc in [35,40]:
    rr=flexure(bw,hh,phi,nf['outer_composition'],fc);cap=None if rr['mrd_kncm'] is None else rr['mrd_kncm']/100/FACTOR;m=rr['minimum_by_actual_section'];ng['scenarios'].append({'fck_mpa':fc,'concretopy':rr,'Mk_eq_tfm':cap,'capacity_passes':cap is not None and cap>=nd['magnitude'],'minimum_passes':None if nd['magnitude']==0 else m['moment_passes'] and m['area_passes']})
   item['negative'].append(ng)
  # Explicit drawn zones; the final zone remains tied to the confirmed support face. Coordinate discrepancy is recorded.
  zr=A['drawn_stirrup_regions'].get(f'{bid}:{token}')
  if zr:
   starts=a;regions=[]
   for k,(pp,ss,legs,length,mark) in enumerate(zr):
    stop=min(z,starts+length/100) if k<len(zr)-1 else z
    regions.append((starts,stop,pp,ss,legs,mark,length));starts=stop
   delta=(z-a)*100-sum(q[3] for q in zr);item['drawn_length_difference_cm']=delta
  else:
   pp,ss,legs=defaultst['diameter_mm'],defaultst['spacing_cm'],defaultst['legs'];regions=[(a,z,pp,ss,legs,'Marca lida no detalhe; consultar recorte',None)]
  for aa,zz,pp,ss,legs,mark,length in regions:
   if zz<=aa:continue
   hh=87 if bid in ['V49','V50'] and mark=='N5' else h
   candidates=[]
   for origin,bc in [('inferior',cfg)]+[(q['end']+'_superior',q['configuration']) for q in item['negative']]:
    rr=flexure(bw,hh,pp,bc,35)
    candidates.append({'origin':origin,'configuration':bc,'d_cm':rr['d_equivalente_cm'],'As_cm2':rr['as_total_cm2'],'layers':len(bc['layers'])})
   selected=min(candidates,key=lambda q:(-q['layers'],-q['As_cm2'],q['d_cm']));depth=selected['d_cm'];demand=extreme(qs,L,aa,zz);provided=legs*api.Barra(pp).area_cm2*100/ss
   region={'start_model_m':aa,'end_model_m':zz,'drawn_length_cm':length,'mark':mark,'section_height_cm':hh,'diameter_mm':pp,'spacing_cm':ss,'legs':legs,'provided_cm2_m':provided,'demand':demand,'depth_selection':selected,'scenarios':[]}
   for fc in [35,40]:
    context={'section':{'bw':bw,'h':hh,'cobrimento':3.5,'diametro_estribo_mm':pp},'fck_mpa':fc,'fyk_mpa':500,'gamma_f':1.4,'gamma_c':1.4,'gamma_s':1.15,'effective_depth':{'status':'PASS','d_cm':depth,'selected':selected},'axial_force_kn':0,'stirrup_angle_degrees':90}
    rr=design_shear(context,public_shear_api(),demand['magnitude']*9.80665,pp);req=rr.get('governing_Asw_per_s_cm2_m');limit=min(depth,80) if rr.get('Vsd_kn',math.inf)<=.2*rr.get('VRd2_kn',0) else min(.6*depth,35);gap=22 if legs==4 else bw-7
    region['scenarios'].append({'fck_mpa':fc,'concretopy_via_adapter':rr,'required_cm2_m':req,'area_passes':req is not None and provided>=req,'longitudinal_max_spacing_passes':rr.get('maximum_spacing_code_cm') is not None and ss<=rr['maximum_spacing_code_cm'],'transverse_max_spacing_passes':gap<=limit,'transverse_gap_bound_cm':gap,'transverse_limit_cm':limit,'minimum_spacing_status':'PASS' if ss-pp/10>=4 else 'FAIL','clear_spacing_cm':ss-pp/10,'vibrator_diameter_cm':4,'minimum_spacing_source':'Passagem geometrica do vibrador4cm confirmado por Joao; nao e minimo fixo normativo'})
   item['shear'].append(region)
  results.append(item)
# Each end uses its own maximum negative demand. Never unify adjacent sides.
for x in results:
 for n in x['negative']:
  gov=n['demand']['magnitude'];n['governing_Mk_support_tfm']=gov;n['governing_Mk_own_side_tfm']=gov;n['negative_demand_scope']='ONLY_OWN_SPAN_AND_OWN_END_SUPPORT_REGION'
  for sc in n['scenarios']:sc['capacity_passes']=sc['Mk_eq_tfm'] is not None and sc['Mk_eq_tfm']>=gov
out={'date':'2026-10-16','scope':'V1-V50; PAR excluded; conventional beam calculations on h165 per engineer request; specialized wall-beam criteria excluded','source_model_sha256':T['V1']['sha256'],'engine':'Concretopy official public APIs; no independent resistance substitutes','unit_presentation':'tf and tf.m; characteristic demand, resistance equivalent MRd/gamma_f','gamma_f':1.4,'gamma_c':1.4,'gamma_s':1.15,'kN_per_tf':9.80665,'materials':'C35 em toda a secao final, simplificacao expressamente confirmada por Joao; C40 apenas sensibilidade complementar','results':results}
(O/'verificacoes_globais_concretopy.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'status':'OK','beams':len(set(x['beam_id'] for x in results)),'spans':len(results),'negative_queries':sum(len(x['negative']) for x in results),'shear_regions':sum(len(x['shear']) for x in results),'physically_reconciled_domains':sum(x['domain']['physical_block_faces_proved'] for x in results),'critical_shear':[{ 'beam':x['beam_id'],'token':x['span_token'],'areas':[(q['mark'],q['provided_cm2_m'],[s['required_cm2_m'] for s in q['scenarios']]) for q in x['shear']]} for x in results if x['beam_id'] in ['V4','V5','V15','V33','V37','V40']]},ensure_ascii=True))
