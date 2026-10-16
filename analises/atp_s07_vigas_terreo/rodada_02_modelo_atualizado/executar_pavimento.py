from pathlib import Path
import json,sys,copy,math
ROOT=Path(r'\\srvmaster\PUBLICO\Joao Severgnini\Simon\engineering-assistant');OUT=ROOT/'analises/atp_s07_vigas_terreo/rodada_02_modelo_atualizado'
sys.path[:0]=[str(ROOT/'tools/reinforcement_checks'),str(ROOT/'tools/beam_model'),str(ROOT.parent/'concretopy')]
from floor_review import review_floor
from physical_geometry import normalize_occurrence
from input_evidence import fact
from shear_diagram import ShearDiagram
from shear_review import design_shear,public_shear_api
import concretopy as api
spec=json.loads((OUT/'manifesto_pavimento.json').read_text(encoding='utf8'));case=spec['beams'][15];m=case['model'];cs=m['physical_geometry']['coordinate_system'];p=cs['provenance'][0];T=json.loads((OUT/'tqs_operacional.json').read_text(encoding='utf8'))['V16']
def f(v=None,u=None,proof=None,state=None):return fact(v,state=state or ('DOCUMENTED_CONFIRMED' if v is not None else 'MISSING'),unit=u,provenance=[proof or p])
if not any(x['mark']=='N2' for x in m['physical_geometry']['occurrences']):
 for mark,qty,phi,a,b in [('N2',4,16,-.25,2.75),('N1',4,10,2.55,5.45),('N3',4,16,5.25,8.25)]:
  pr=dict(p,mark=mark,interpretation='N2/N3 straight C300 from 60cm outside support face; N1 straight C290 ending 220cm before right inner face. No coordinates inferred from drawing scale.')
  o=normalize_occurrence({'mark':mark,'occurrence_id':'V16-'+mark+'-negative','function':'negative','face':'upper','quantity':f(qty,proof=pr),'diameter_mm':f(phi,'mm',pr),'layers':f([qty],proof=pr),'x_start_m':f(a,'m',pr),'x_end_m':f(b,'m',pr),'provenance':[pr]})
  m['physical_geometry']['occurrences'].append(o);m['longitudinal_reinforcement'].append({'mark':mark});case['layer_observations'][o['occurrence_id']]={'near_bar_text':f([qty],proof=pr)}
 old=case['positioned_tqs']['beam']['spans'][0]['internal_forces']
 for label,env in [('Q MX.','max'),('Q MN.','min')]:
  s=next(s for s in T['series'] if s['label']==label);old.append({'quantity':'shear','envelope':env,'unit':'kN','stage':'model_input','positions':[.2+i*7.6/12 for i in range(13)],'values':s['values_si'],'sources':[s['source']]})
 base={k:f(True,proof={'source':'documentary V16 all negative positions N1/N2/N3 reconciled; negative envelope is nonnegative throughout overlap/middle 2.55-5.45m'}) for k in ['materials','layer_order','physical_inventory_complete']}
 for name,a,b in [('left',.35,2.55),('right',5.45,7.65)]:case['jobs'].append({'id':'V16-negative-'+name,'control':'negative_flexure','span_id':1,'interval_m':[a,b],'context':case['context'],'inputs':base})
 case['negative_scope_proof']={'checked_critical_regions_m':[[.35,2.55],[5.45,7.65]],'middle_m':[2.55,5.45],'reason':'M MN. and M MX. remain >=0 in middle; linear interpolation only; two overlap regions do not carry negative demand.'}
 inputs={k:f(True) for k in ['materials','shear_envelope','stirrup_regions','effective_depth']}
 case['jobs'].append({'id':'V16-shear-drawn','control':'shear','span_id':1,'interval_m':[.35,7.65],'inputs':inputs,'adapter':'s07_v16_shear'})
 noind={'source_form':p['form'],'region':'complete V16 PC40C-PC41C','model_evidence':'No receiving-beam V13 in the 44 examined support chains; no crossing beam supporting/being supported in this V16 region.'}
 case['jobs'].append({'id':'V16-suspension-not-applicable','control':'suspension','interval_m':[.35,7.65],'inputs':{},'applicability':f(None,proof=noind,state='NOT_APPLICABLE')})
(OUT/'manifesto_pavimento.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2),encoding='utf8')
def adapter(payload):
 ss=[s for s in payload['registered_span']['internal_forces'] if s['quantity']=='shear'];D=ShearDiagram([dict(s,sections=list(range(1,14)),series_id=s['envelope'],provenance=s['sources']) for s in ss]);demand=D.maximum(.35,7.65);vk=demand['Vsk_abs_kn'];r=[]
 for fc in [35,40]:
  ctx={'section':{'bw':40,'h':50,'cobrimento':3.5,'diametro_estribo_mm':6.3},'fck_mpa':fc,'fyk_mpa':500,'gamma_f':1.4,'gamma_c':1.4,'gamma_s':1.15,'effective_depth':{'status':'PASS','selected':{'source':'V16 negative4phi16 first layer is lower d=45.07 than positive4phi12.5 d45.245'},'d_cm':45.07},'axial_force_kn':0,'stirrup_angle_degrees':90}
  sh=design_shear(ctx,public_shear_api(),vk,6.3);provided=4*api.Barra(6.3).area_cm2*100/20
  stmax=min(45.07,80) if sh['Vsd_kn']<=.20*sh['VRd2_kn'] else min(.6*45.07,35)
  r.append({'fck_mpa':fc,'design':sh,'provided_cm2_m':provided,'area_sufficient':provided>=sh['governing_Asw_per_s_cm2_m'],'smax_long_cm':sh['maximum_spacing_code_cm'],'long_spacing_sufficient':20<=sh['maximum_spacing_code_cm'],'transverse_spacing_limit_cm':stmax,'transverse_spacing_sufficient':22<stmax,'transverse_basis':'Two overlapping closed stirrups width22cm per N5 and cutA; each adjacent branch gap is bounded by22cm, below the code limit; no branch center coordinate guessed','minimum_longitudinal_spacing_status':'INCONCLUSIVE','minimum_spacing_reason':'18.3.3.2 requires vibrator passage/adensamento; equipment not documented.'})
 return {'status':'INCONCLUSIVE','overall_structural_result':None,'passes':None,'results':r,'demand':demand,'limitation':'minimum longitudinal spacing operational check still pending; numeric controls retained independently'}
res=review_floor(spec,adapters={'s07_v16_shear':adapter},api=api)
(OUT/'resultado_floor_review.json').write_text(json.dumps(res,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf8')
compact={'beam_id':'V16','model_name':'V16','controls':[]}
for e in res['beams'][15]['controls']:
 row={k:e[k] for k in ['job_id','control','status','execution_state']};rr=e.get('result')
 if rr and e['control'] in ['positive_flexure','negative_flexure']:
  row['regions']=[{k:r.get(k) for k in ['MRd_knm','Mk_equivalent_knm','utilization','passes','not_applicable']}|{'Msk_max_knm':max((p.get('value_knm',0) for p in r.get('demand_points',[])),default=0)} for r in rr['regions']]
 elif rr and e['control']=='shear':row['details']=rr
 compact['controls'].append(row)
(OUT/'V16_resultado_resumido.json').write_text(json.dumps(compact,ensure_ascii=False,indent=2),encoding='utf8')
print([(r['control'],r['status'],r['execution_state']) for r in compact['controls']]);print('V16_shear_numeric',[(r['fck_mpa'],r['area_sufficient'],r['long_spacing_sufficient'],r['transverse_spacing_sufficient']) for r in next(e for e in compact['controls'] if e['control']=='shear')['details']['results']])
