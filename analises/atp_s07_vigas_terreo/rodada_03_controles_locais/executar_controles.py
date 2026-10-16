from pathlib import Path
import json,sys,copy,math,contextlib,io
R=Path(r'\\srvmaster\PUBLICO\Joao Severgnini\Simon\engineering-assistant');BASE=R/'analises/atp_s07_vigas_terreo';O=BASE/'rodada_03_controles_locais';PREV=BASE/'rodada_02_modelo_atualizado'
sys.path[:0]=[str(R/'tools/reinforcement_checks'),str(R.parent/'concretopy')]
import concretopy as api
from shear_diagram import ShearDiagram
from shear_review import design_shear,public_shear_api
from suspension_review import review_connection
from dataclasses import asdict
T=json.loads((PREV/'tqs_operacional.json').read_text(encoding='utf8'))
code=(PREV/'verificar_secoes_criticas.py').read_text(encoding='utf8');ns={};exec(code[:code.index('R=[]')],ns);C=ns['C'];bar=ns['bar'];C=copy.deepcopy(C)
def alter(n,pos=None,neg=None):
 v=list(C[n]);
 if pos is not None:v[4]=pos
 if neg is not None:v[5]=neg
 C[n]=tuple(v)
alter(18,pos=[bar(3,16),bar(3,16)]);alter(30,pos=[bar(3,16)]);alter(23,pos=[bar(2,16),bar(4,16)])
alter(15,neg=[bar(4,12.5),bar(6,20),bar(4,16),bar(8,20,[7,1]),bar(6,20)])
alter(21,neg=[bar(4,10),bar(5,20),bar(5,20),bar(5,20),bar(4,16),bar(4,16),bar(2,10)])
for n in [29,39]:alter(n,neg=[bar(2,10)]*2)
for n in [31,41]:alter(n,neg=[bar(2,10)]*2)
# These members contain intermediate-height reinforcement. No invented height or transferred outer layer.
INTER={4:4,5:2,11:2,14:2,15:4,23:8,24:2,25:2,26:2,28:4,29:3,30:4,31:3,32:4,34:4,35:2,36:2,38:2,39:3,41:3,42:2,43:2,44:4,45:2,46:2,47:2,48:2,49:2,50:2,240:8}
VARIABLE={23,24,42,49,50}
def dump(name,data): (O/name).write_text(json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf8')
def value(vals,t):
 i=min(max(int(t),0),11);return vals[i]+(vals[i+1]-vals[i])*(t-i)
def flex(bw,h,phi,cfg,fc):
 sec=api.SecaoRetangular(bw,h,3.5,diametro_estribo_mm=phi);layers=[api.CamadaArmaduraLongitudinal(n,api.Barra(cfg['phi'])) for n in cfg['layers']];ds=api.calcular_alturas_uteis_camadas(sec,layers);layers=[api.CamadaArmaduraLongitudinal(x.numero_barras,x.barra,d) for x,d in zip(layers,ds)];r=api.verificar_flexao_viga_retangular(sec,api.Concreto(fc),api.Aco(500),layers,verificar_armadura_minima=False);return r,ds
results=[];susp=[]
for n,(model,tokens,bw,h,positives,negatives,phi,s,legs,complete) in C.items():
 real=24 if n==240 else n
 item={'beam_id':f'V{real}','model_name':model,'section_cm':[bw,h],'source_detail_crop':next((str(p) for p in (BASE/'crops').glob(f'*_V{real}.png')),None),'method':'existing Concretopy flexure/shear API; independent controls; no steel relocation; no office acceptance criteria','spans':[]}
 for j,token in enumerate(tokens):
  h={23:[80,50],24:[50,50,50],42:[80,50,80,110,50,50,50],240:[80]}.get(n,[C[n][3]]*len(tokens))[j]
  v=T[model];g=next(q for q in v['geometry'] if q['span_token']==token);L=g['length_m'];series=[q for q in v['series'] if q['span_token']==token];ms=[q for q in series if q['label'] in ['M MN.','M MX.']];qs=[q for q in series if q['label'].startswith('Q')]
  idx=int(token.rstrip('B'))-1-sum('B' in z['span_token'] and int(z['span_token'][:-1])<int(token.rstrip('B')) for z in v['geometry'])
  if 'B' in token:a,z=0,L;left=None;right=v['supports'][0]
  else:
   left,right=v['supports'][idx:idx+2];a=left['width_m']/2-left['depev_m'];z=L-right['width_m']/2+right['depev_m']
  positions=[a,z]+[k*L/12 for k in range(13) if a<=k*L/12<=z];pv,x,source=max([(max(0,value(q['values_si'],x/L*12)),x,q['source']) for q in ms for x in positions],key=lambda y:y[0]);p={'Msk_knm':pv,'Msd_knm':1.4*pv,'peak_model_local_m':x,'peak_fraction':x/L,'composition':positives[j],'source':source,'scenarios':[]}
  for fc in [35,40]:
   r,ds=flex(bw,h,phi,positives[j],fc);mdmin=.8*bw*h*h/6*api.Concreto(fc).fctk_sup*.1/100
   p['scenarios'].append({'fck_mpa':fc,'MRd_knm':r.mrd_kncm/100,'capacity_sufficient':r.mrd_kncm/100>=p['Msd_knm'],'As_cm2':r.as_total_cm2,'d_cm':r.d_equivalente_cm,'minimum_Md_knm':mdmin,'minimum_absolute_cm2':.0015*bw*h,'minimum_sufficient':r.mrd_kncm/100>=mdmin and r.as_total_cm2>=.0015*bw*h,'hypotheses_valid':r.hipoteses_validas,'concretopy':asdict(r)})
  if all(q['capacity_sufficient'] and q['hypotheses_valid'] for q in p['scenarios']):p['capacity_state']='SUFFICIENT_OUTER_REINFORCEMENT_LOWER_BOUND'
  else:p['capacity_state']='NEEDS_REAL_HEIGHT_OR_OTHER_DRAWN_BARS' if n in INTER or n in VARIABLE else 'OUTER_CAPACITY_DEFICIT_FULL_SECTION_BOUND_CHECKED_SEPARATELY'
  if real in [19,20,22]:p['documentary_conflict']='Alternative summary and individual positions differ; numeric position-based result retained, not documentary approval.'
  if n in VARIABLE:p['variable_section_warning']='Height at the constant span portion comes from section labels in detailing: V23 80/50; V24 first span80 and others50; V42 80/50/80/110/50/50/50. This does not approve transitions. V49/V50 peak initially h50; uncertainty in exact peak-step registration retained.'
  sp={'model_name':model,'span_token':token,'section_cm':[bw,h],'model_face_interval_m':[a,z],'model_axis_basis':'TQS effort coordinates, independently retained under user authorization; does not replace form-detail comparison','positive':p,'negative_faces':[]}
  if negatives is not None:
   for end,xx,cfg in [('left',a,negatives[j]),('right',z,negatives[j+1])]:
    mk=max(0,-min(value(q['values_si'],xx/L*12) for q in ms));nn={'end':end,'support':None if end=='left' and left is None else (left if end=='left' else right)['name'],'Msk_knm':mk,'Msd_knm':1.4*mk,'outer_composition':cfg,'scenarios':[]}
    for fc in [35,40]:
     rr,ds=flex(bw,h,phi,cfg,fc);res={'fck_mpa':fc,'MRd_outer_knm':rr.mrd_kncm/100,'outer_sufficient':rr.mrd_kncm/100>=mk*1.4,'As_cm2':rr.as_total_cm2,'d_cm':rr.d_equivalente_cm,'hypotheses_valid':rr.hipoteses_validas}
     # Relaxed upper bound for simple non-staged sections, allowing arbitrary compression steel stress <=fyd.
     if n not in INTER and n not in VARIABLE and len(cfg['layers'])==1:
      rb,db=flex(bw,h,phi,positives[j],fc);Tforce=rr.as_total_cm2*500/1.15*.1;k=.85*(fc/1.4*.1)*bw;dp=h-max(db);Cmax=rb.as_total_cm2*500/1.15*.1
      signed=min(max(k*dp-Tforce,-Cmax),Cmax);mr=(Tforce*max(ds)+signed*dp-(Tforce+signed)**2/(2*k))/100
      res['relaxed_compression_steel_upper_bound_knm']=mr;res['upper_bound_inputs']={'T_kn':Tforce,'k_kn_cm':k,'opposite_layer_depth_cm':dp,'opposite_force_abs_cap_kn':Cmax,'optimal_signed_opposite_force_kn':signed,'equation':'M=T*d + S*dprime - (T+S)^2/(2*k), -AsOpp*fyd<=S<=AsOpp*fyd; opposite bars may be in tension OR compression; no strain compatibility imposed, hence favorable upper bound'}
     
     if n not in INTER and n not in VARIABLE:
      rb,db=flex(bw,h,phi,positives[j],fc);abs_bound=rr.as_total_cm2*500/1.15*.1*max(ds)/100 + rb.as_total_cm2*500/1.15*.1*(h-min(db))/100
      res['all_drawn_steel_tension_upper_bound_knm']=abs_bound
      res['full_section_upper_bound_knm']=min(abs_bound,res.get('relaxed_compression_steel_upper_bound_knm',abs_bound))
     res['minimum_Md_knm']=.8*bw*h*h/6*api.Concreto(fc).fctk_sup*.1/100;res['minimum_absolute_cm2']=.0015*bw*h;res['minimum_outer_sufficient']=res['As_cm2']>=res['minimum_absolute_cm2'] and res['MRd_outer_knm']>=res['minimum_Md_knm'];res['minimum_full_upper_bound_insufficient']=res.get('full_section_upper_bound_knm',1e99)<res['minimum_Md_knm']
     nn['scenarios'].append(res)
    if all(q['outer_sufficient'] for q in nn['scenarios']):nn['state']='SUFFICIENT_OUTER_REINFORCEMENT_LOWER_BOUND'
    elif all(q.get('full_section_upper_bound_knm',1e99)<mk*1.4 for q in nn['scenarios']):nn['state']='INSUFFICIENT_EVEN_WITH_COMPRESSION_STEEL_UPPER_BOUND'
    else:nn['state']='DEPENDENT_ON_INTERMEDIATE_STEEL_HEIGHT' if n in INTER else 'REQUIRES_ADDITIONAL_SECTION_COMPOSITION'
    if n in [29,31,39,41]:nn['note']='Earlier screening incorrectly put intermediate 3phi16 on outer face; that result is withdrawn. Here only 2phi10 at the true outer top are credited; intermediate3phi16/skin stay at unknown true heights.'
    sp['negative_faces'].append(nn)
  # Use both signs/depths as a safe envelope, not a fictitious equivalent bar. Areas have independent scenarios.
  positive_depths=flex(bw,h,phi,positives[j],35)[1];depth=min(positive_depths)
  if negatives is not None:
   for cfg in [negatives[j],negatives[j+1]]:depth=min(depth,*flex(bw,h,phi,cfg,35)[1])
  sh={'effective_depth_conservative_cm':depth,'stirrup':{'diameter_mm':phi,'spacing_cm':s,'legs':legs,'provided_cm2_m':legs*api.Barra(phi).area_cm2*100/s},'queries':[],'minimum_spacing':'ENGINEER_VIBRATOR_OR_ADENSAMENTO_INFORMATION_REQUIRED; no fixed office minimum'}
  if n in INTER:
   unknown_area_upper=(20*api.Barra(20).area_cm2 if n in [23,24,29,30,31,39,41,42,49,50,240] else INTER[n]*api.Barra(20).area_cm2)
   lower_areas=[sum(api.Barra(positives[j]['phi']).area_cm2*c for c in positives[j]['layers'])]
   if negatives is not None:lower_areas += [cfg['count']*api.Barra(cfg['phi']).area_cm2 for cfg in [negatives[j],negatives[j+1]]]
   dlow=depth*min(lower_areas)/(min(lower_areas)+unknown_area_upper)
   sh['effective_depth_interval_cm']=[dlow,depth];sh['effective_depth_warning']='Outer-only d is NOT the actual centroid with intermediate bars. The lower endpoint intentionally puts a generous upper area of unknown bars at d=0, so it is a conservative capacity bound, not invented coordinates.'
  else:sh['effective_depth_interval_cm']=[depth,depth]
  if n==21 and j>=4:sh['stirrup']={'diameter_mm':6.3,'spacing_cm':15,'legs':2,'provided_cm2_m':2*api.Barra(6.3).area_cm2*100/15}
  for title,aa,zz in [('between_model_faces',a,z),('central_away_2d_sensitivity',a+2*depth/100,z-2*depth/100)]:
   if aa>=zz:continue
   vals=[(abs(value(q['values_si'],x/L*12)),x,q['source']) for q in qs for x in [aa,zz]+[k*L/12 for k in range(13) if aa<=k*L/12<=zz]];vk,x,src=max(vals,key=lambda t:t[0]);query={'scope':title,'interval_model_local_m':[aa,zz],'Vsk_kn':vk,'Vsd_kn':vk*1.4,'position_model_local_m':x,'source':src,'scenarios':[]}
   for fc in [35,40]:
    pp=sh['stirrup']['diameter_mm'];ctx={'section':{'bw':bw,'h':h,'cobrimento':3.5,'diametro_estribo_mm':pp},'fck_mpa':fc,'fyk_mpa':500,'gamma_f':1.4,'gamma_c':1.4,'gamma_s':1.15,'effective_depth':{'status':'PASS','selected':{'source':'outer layer centroid conservative bound, section/cut; not invented intermediate height'},'d_cm':depth},'axial_force_kn':0,'stirrup_angle_degrees':90};r=design_shear(ctx,public_shear_api(),vk,pp);translimit=min(depth,80) if r['Vsd_kn']<=.20*r['VRd2_kn'] else min(.6*depth,35);gap_bound=(22 if legs==4 else bw-7)
    query['scenarios'].append({'fck_mpa':fc,'design':r,'area_sufficient':sh['stirrup']['provided_cm2_m']>=r['governing_Asw_per_s_cm2_m'],'longitudinal_spacing_sufficient':sh['stirrup']['spacing_cm']<=r['maximum_spacing_code_cm'],'transverse_gap_upper_bound_cm':gap_bound,'transverse_limit_cm':translimit,'transverse_spacing_sufficient':gap_bound<=translimit,'gap_proof':'overlapping22cm rings from cut' if legs==4 else 'closed stirrup outer width=b-2cover bounds the gap'})
   sh['queries'].append(query)
  sh['zone_state']='UNIFORM_STIRRUPS_NUMERICAL_CHECK_EXECUTED'
  if n in [4,15,17,34,37,49,50]:sh['zone_state']='VARIABLE_STIRRUPS_WEAKEST_CONFIGURATION_BOUND; failed bound needs actual zoning, not automatic deficiency'
  if n in VARIABLE:sh['zone_state']='VARIABLE_SECTION_NEEDS_TRANSITION_GEOMETRY; h50 safe-side screen only'
  
  if n in INTER:
   for query in sh['queries']:
    extra=[]
    for fc in [35,40]:
     pp=sh['stirrup']['diameter_mm'];ctx={'section':{'bw':bw,'h':h,'cobrimento':3.5,'diametro_estribo_mm':pp},'fck_mpa':fc,'fyk_mpa':500,'gamma_f':1.4,'gamma_c':1.4,'gamma_s':1.15,'effective_depth':{'status':'PASS','selected':{'source':'rigorous lower bound; no intermediate bar relocated'},'d_cm':sh['effective_depth_interval_cm'][0]},'axial_force_kn':0,'stirrup_angle_degrees':90};r=design_shear(ctx,public_shear_api(),query['Vsk_kn'],pp);extra.append({'fck_mpa':fc,'design':r,'area_sufficient':sh['stirrup']['provided_cm2_m']>=r['governing_Asw_per_s_cm2_m'] if r.get('governing_Asw_per_s_cm2_m') is not None else False,'longitudinal_spacing_sufficient':sh['stirrup']['spacing_cm']<=r['maximum_spacing_code_cm'] if r.get('maximum_spacing_code_cm') is not None else False})
    query['lower_depth_bound_scenarios']=extra
  sp['shear']=sh;item['spans'].append(sp)
 results.append(item)
# Merge the first physical span of V24 stored in modelV23 token3.
supp=next(q for q in results if q['beam_id']=='V24' and q['model_name']=='V23');main=next(q for q in results if q['beam_id']=='V24' and q['model_name']=='V24');main['spans']=supp['spans']+main['spans'];results.remove(supp)
dump('controles_independentes.json',results)
# Documented physical receiver spans and indirect-support checks.
for receiver,supported,axis in [('V19','V33',4.),('V20','V40',3.995)]:
 vb=T[receiver];source={'form':'7214 R01','detail':'7401 R00 V19=V20 N5; 7403 R01 supported beam','crop':'7214_V40_forma.png','geometry':'Columns70cm; clear730cm; receiving axes8m. Projection V33=35+365cm; V40=35+364.5cm from left receiver axis. Both beam tops+8.88 and depths50cm.'};series=[{'quantity':'shear','unit':'kN','envelope':q['label'],'positions':[.2+i*7.6/12 for i in range(13)],'values':q['values_si'],'sections':list(range(1,14)),'provenance':q['source']} for q in vb['series'] if q['label'].startswith('Q')];support=T[supported]['supports'][1]
 span={'span_id':1,'series':series,'reference_legs':2,'drawn_regions':[{'id':receiver+'-N5','diameter_mm':6.3,'spacing_cm':15,'legs':2,'interval_m':[.35,7.65],'source':source,'physical_function':'CONVENTIONAL_SHEAR_STIRRUP'}],'support_geometry':{'left':{'type':'COLUMN','type_source':source,'source':source,'axis_m':0,'width_m':.7,'left_face_m':-.35,'right_face_m':.35},'right':{'type':'COLUMN','type_source':source,'source':source,'axis_m':8,'width_m':.7,'left_face_m':7.65,'right_face_m':8.35}}}
 conn={'id':supported+'-on-'+receiver,'type':'BEAM_ON_BEAM','receiving_beam_id':receiver,'supported_beam_id':supported,'transfer_confirmed':True,'transfer_source':support['source'],'suspension_applicable':True,'applicability_source':dict(source,norm='NBR6118:2023 18.3.6; nonhung beams, coincident top/bottom faces; no hd reduction'),'supported_geometry':{'height_cm':50,'width_cm':30,'source':source},'placement':'INTERIOR','projected_axis_m':axis,'axis_source':source,'reaction':{'value':max(support['Rmax_kN'],support['Rmin_kN']),'unit':'kN','nature':'CHARACTERISTIC','is_total':True,'total_source':dict(support['source'],interpretation='Total terminal support reaction of unique single-span beam, not receiving-column reaction; maximum support envelope under user-authorized TQS loads'),'combination':'VGESFS R.APOIO MAX/MIN characteristic support envelope, not a named simultaneous load case','source':support['source'],'downward_sign':1,'supported_beam_id':supported,'receiving_beam_id':receiver}}
 rr={'receiving_beam':receiver,'supported_beam':supported,'physical_source':source,'results':[]}
 for fc in [35,40]:
  ctx={'section':{'bw':30,'h':50,'cobrimento':3.5,'diametro_estribo_mm':6.3},'fck_mpa':fc,'fyk_mpa':500,'gamma_f':1.4,'gamma_c':1.4,'gamma_s':1.15,'effective_depth':{'status':'PASS','d_cm':45.07,'selected':{'source':'smaller depth among conflicting positive phi12.5/phi16; conservative bound only'}}};res=review_connection(conn,receiver,[span],ctx,public_shear_api());rr['results'].append({'fck_mpa':fc,'tool_result':res,'criterion_provenance':'75% minimum in receiver established here from actually consulted NBR6118:2023 18.3.6 for this nonhung coincident-face geometry; identifiers engineer_confirmed in tool are internal historical labels, not a claim João supplied an office rule.'})
 area=.75*1.4*conn['reaction']['value']/(500/1.15*.1);maxrings=math.floor(50/15)+1;provided=maxrings*2*api.Barra(6.3).area_cm2
 rr['independent_count_upper_bound']={'required_receiver_suspension_cm2':area,'norm_maximum_length_cm':50,'maximum_stirrups_in_length':maxrings,'provided_upper_bound_cm2':provided,'passes_even_ignoring_shear':provided>=area,'basis':'50cm interval with spacing15cm holds at most4stirrups; all their area generously assigned to suspension, no deduction for shear.'};susp.append(rr)
dump('suspensao_V19_V20.json',susp)
for rr in susp:print(rr['receiving_beam'],rr['independent_count_upper_bound'],[(r['fck_mpa'],r['tool_result']['overall_result'],r['tool_result'].get('asw_per_s_total_required')) for r in rr['results']])
for b in results:
 flags=[(sp['span_token'],q['support'],round(q['Msd_knm'],2)) for sp in b['spans'] for q in sp['negative_faces'] if q['state'].startswith('INSUFFICIENT')]
 if flags:print('NEGATIVE_UPPER_BOUND_FAIL',b['beam_id'],flags)
print('BEAMS',len(results),'INTERVALS',sum(len(b['spans']) for b in results))

