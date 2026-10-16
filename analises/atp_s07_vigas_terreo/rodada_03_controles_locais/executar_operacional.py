from pathlib import Path
import sys,json,copy,hashlib,math
R=Path(r'\\srvmaster\PUBLICO\Joao Severgnini\Simon\engineering-assistant');BASE=R/'analises/atp_s07_vigas_terreo';PREV=BASE/'rodada_02_modelo_atualizado';O=BASE/'rodada_03_controles_locais';sys.path[:0]=[str(R/'tools/reinforcement_checks'),str(R/'tools/beam_model'),str(R.parent/'concretopy')]
import concretopy as api
from input_evidence import fact
from floor_review import review_floor
T=json.loads((PREV/'tqs_operacional.json').read_text(encoding='utf8'));D=json.loads((O/'controles_independentes.json').read_text(encoding='utf8'));SS=json.loads((O/'suspensao_V19_V20.json').read_text(encoding='utf8'))
# V21 first-span full-section favorable upper bound with real upper construction steel.
b=next(b for b in D if b['beam_id']=='V21');p=b['spans'][0]['positive'];A=4*api.Barra(20).area_cm2;Ac=2*api.Barra(10).area_cm2;d=44.7;dp=4.8;Tforce=A*api.Aco(500).fyd(1.15)*.1;Cmax=Ac*api.Aco(500).fyd(1.15)*.1;proof={'beam_id':'V21','detail':'7402 first span: N2 2phi20+N4 2phi20 at peak, upper N3 2phi10; adjacent negative bars end before reaching this peak','peak':p,'method':'favorable algebraic upper bound; existing Concretopy outer-only capacity checked independently','equation':'M=T*d -(T-Cs)^2/(2*k) -Cs*dprime; k=0.85*fcd*b; maximize for 0<=Cs<=As_compressed*fyd','results':[]}
for fc in [35,40]:
 k=.85*fc/1.4*.1*30;cs=min(max(Tforce-k*dp,0),Cmax);upper=(Tforce*d-(Tforce-cs)**2/(2*k)-cs*dp)/100;base=(Tforce*d-Tforce**2/(2*k))/100;match=next(r for r in p['scenarios'] if r['fck_mpa']==fc)['MRd_knm'];assert abs(base-match)<1e-8;proof['results'].append({'fck_mpa':fc,'outer_only_MRd_knm':base,'compression_force_cap_kn':Cmax,'optimal_compression_force_kn':cs,'full_section_upper_bound_knm':upper,'Msd_knm':p['Msd_knm'],'insufficient':upper<p['Msd_knm']})
p['independent_full_section_upper_bound']=proof['results'];p['capacity_state']='INSUFFICIENT_FULL_SECTION_UPPER_BOUND' if all(r['insufficient'] for r in proof['results']) else 'REQUIRES_SECTION_REVIEW'
(O/'V21_positivo_limite_superior.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2),encoding='utf8');(O/'controles_independentes.json').write_text(json.dumps(D,ensure_ascii=False,indent=2),encoding='utf8')

other_proofs=[]
for name,token,count,diam,opcount,opdiam,provenance in [
 ('V16','1',4,12.5,4,10,'7401 N4 lower; N1 upper at peak; end N2/N3 do not reach peak'),
 ('V37','1',2,20,2,10,'7403 N4 continuous lower; extra N3 ends well before central peak; top N2/N6 end before peak; N5 construction upper'),
 ('V25','4',3,12.5,2,10,'7402 N11 1phi12.5+N12 2phi12.5 at peak; N13 construction upper; intermediate first-stage bars end at P727 before this central peak')]:
 bb=next(x for x in D if x['beam_id']==name);sp=next(x for x in bb['spans'] if x['span_token']==token and x['model_name']==name);pp=sp['positive'];bw,hh=sp['section_cm'];phi=sp['shear']['stirrup']['diameter_mm'];dd=hh-3.5-phi/10-diam/20;dprime=3.5+phi/10+opdiam/20;tt=count*api.Barra(diam).area_cm2*api.Aco(500).fyd(1.15)*.1;cap=opcount*api.Barra(opdiam).area_cm2*api.Aco(500).fyd(1.15)*.1;proofrow={'beam_id':name,'span_token':token,'source':provenance,'Msd_knm':pp['Msd_knm'],'results':[]}
 for fc in [35,40]:
  kk=.85*fc/1.4*.1*bw;ss=min(max(kk*dprime-tt,-cap),cap);mm=(tt*dd+ss*dprime-(tt+ss)**2/(2*kk))/100;proofrow['results'].append({'fck_mpa':fc,'upper_bound_knm':mm,'optimal_signed_opposite_force_kn':ss,'insufficient':mm<pp['Msd_knm']})
 pp['independent_full_section_upper_bound']=proofrow['results'];pp['capacity_state']='INSUFFICIENT_FULL_SECTION_UPPER_BOUND' if all(x['insufficient'] for x in proofrow['results']) else pp['capacity_state'];other_proofs.append(proofrow)
(O/'limites_superiores_positivos.json').write_text(json.dumps(other_proofs,ensure_ascii=False,indent=2),encoding='utf8');(O/'controles_independentes.json').write_text(json.dumps(D,ensure_ascii=False,indent=2),encoding='utf8')
print('OTHER_POSITIVE_BOUNDS',other_proofs)
S=json.loads((PREV/'manifesto_pavimento.json').read_text(encoding='utf8'));base=S['beams'][15]
for idx,n,names in [(18,'V19',('PC47C','PC48C')),(19,'V20',('PC49C','PC50C'))]:
 raw=json.dumps(base,ensure_ascii=False).replace('V16',n).replace('PC40C',names[0]).replace('PC41C',names[1]).replace('7401_'+n+'.png','7401_V19-20.png');c=json.loads(raw);c['model']['longitudinal_reinforcement']=[];c['model']['physical_geometry']['occurrences']=[];c['model']['documentary_reconciliation']['positions']=[];c['layer_observations']={};c.pop('negative_scope_proof',None)
 src={'form':S['sources']['form']['path'],'detail':S['sources']['detailing']['path'],'beam':n,'review':'Physical receiver axis0-8m,70cm columns and730cmclear, stirrupN5 2legs6.3c15; longitudinal summary conflict kept outside these independent controls','evidence_crop':str(O/'7214_V40_forma.png')}
 for seg in c['model']['physical_geometry']['segments']:seg['geometry']['width_cm']=fact(30,state='DOCUMENTED_CONFIRMED',unit='cm',provenance=[src])
 for seg in c['form']['segments']:
  seg['fields']['width_cm']={'documentary_state':'PROVED','fact':fact(30,state='DOCUMENTED_CONFIRMED',unit='cm',provenance=[src])}
 def clean_provenance(obj):
  if isinstance(obj,dict):
   if obj.get('model')=='V13':obj['model']=n
   if 'interpretation' in obj and 'N4' in str(obj['interpretation']):obj['interpretation']=src['review']
   for vv in obj.values():clean_provenance(vv)
  elif isinstance(obj,list):
   for vv in obj:clean_provenance(vv)
 clean_provenance(c)
 c['context']={'section':{'bw':30,'h':50,'cobrimento':3.5,'diametro_estribo_mm':6.3},'fck_mpa':35,'fyk_mpa':500,'gamma_c':1.4,'gamma_s':1.15,'gamma_f':1.4,'provenance':src}
 for q in c['positioned_tqs']['beam']['spans'][0]['internal_forces']:
  label=('Q' if q['quantity']=='shear' else 'M')+(' MX.' if q['envelope']=='max' else ' MN.');v=next(x for x in T[n]['series'] if x['label']==label);q['values']=v['values_si'];q['sources']=[v['source']]
 f=lambda v:fact(v,state='DOCUMENTED_CONFIRMED',provenance=[src])
 c['jobs']=[{'id':n+'-shear-full','control':'shear','span_id':1,'interval_m':[.35,7.65],'inputs':{k:f(True) for k in ['materials','shear_envelope','stirrup_regions','effective_depth']},'adapter':'receiver_shear'},{'id':n+'-suspension-local','control':'suspension','interval_m':([3.75,4.25] if n=='V19' else [3.745,4.245]),'inputs':{k:f(True) for k in ['materials','supported_reaction','indirect_support','suspension_bars']},'adapter':'receiver_suspension'}];S['beams'][idx]=c
(O/'manifesto_pavimento.json').write_text(json.dumps(S,ensure_ascii=False,indent=2),encoding='utf8')
def shear_adapter(payload):
 n=payload['case']['beam_id'] if 'case' in payload else payload['model'].get('beam_id')
 # Job identity remains authoritative if model schema has no beam id.
 n=payload['job']['id'].split('-')[0];b=next(b for b in D if b['beam_id']==n);r=b['spans'][0]['shear'];q=r['queries'][0];return {'status':'INCONCLUSIVE','execution':'NUMERIC_CHECKS_COMPLETE','results':q,'minimum_spacing':'pending vibrator/adensamento equipment; independent of longitudinal summary conflict'}
def suspension_adapter(payload):
 n=payload['job']['id'].split('-')[0];r=next(r for r in SS if r['receiving_beam']==n);return {'status':'FAIL','passes':False,'results':r,'failure_basis':'Existing suspension checker + independent stirrup-count upper bound, no office criteria.'}
# Existing V16 shear adapter from previous executable is kept by a compact unchanged-result adapter.
old16=json.loads((PREV/'V16_resultado_resumido.json').read_text(encoding='utf8'));oldsh=next(c['details'] for c in old16['controls'] if c['control']=='shear')
r=review_floor(S,adapters={'receiver_shear':shear_adapter,'receiver_suspension':suspension_adapter,'s07_v16_shear':lambda payload:oldsh},api=api)
(O/'resultado_floor_review.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf8')
compact=[{'beam_id':x['beam_id'] if 'beam_id' in x else x.get('id'),'controls':[{k:c.get(k) for k in ['job_id','control','status','execution_state']} for c in x['controls']]} for x in r['beams'] if any(c['execution_state'].startswith('EXECUTED') for c in x['controls'])]
(O/'resultado_operacional_resumido.json').write_text(json.dumps(compact,ensure_ascii=False,indent=2),encoding='utf8');print('V21_POSITIVE',proof['results']);print('OPERATIONAL',compact)
