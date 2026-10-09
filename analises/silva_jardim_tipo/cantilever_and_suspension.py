import sys,json,re,pickle,types,copy
from pathlib import Path
P=Path(r'\\srvmaster\PUBLICO\Joao Severgnini\Simon\engineering-assistant\analises\silva_jardim_tipo')
ns={};exec((P/'review.py').read_text(encoding='utf8').split('for beam,t in T.items():')[0],ns);r=types.SimpleNamespace(**ns)
from moment_diagram import MomentDiagram
from shear_diagram import ShearDiagram
from longitudinal_review import check_flexure_regions
from suspension_review import reaction_area
from dataclasses import asdict
with (P/'runtime_cache.pkl').open('rb') as f:r.RUNTIME,r.OUTPUT=pickle.load(f)
lines=Path(r'C:\TQS\TGD - SILVA JARDIM\24-212-TGD-SILVA JARDIM-R35\TIPO\VIGAS\VGESFS.LST').read_text(encoding='cp1252').splitlines()
beam=None;blocks={}
for i,l in enumerate(lines):
 m=re.search(r'VIGA\s*[:=]\s+(\d+)\s*-\s*(V\d+)',l)
 if m:beam=m.group(2);blocks[beam]=[]
 if beam:blocks[beam].append({'line':i+1,'text':l,'file':'VGESFS.LST'})
B={};reactions=[]
for beam,views in r.RUNTIME.items():
 items=[]
 for record in blocks[beam]:
  tokens=record['text'].split()
  if len(tokens)==11 and re.fullmatch(r'\d+B',tokens[0]):
   vals=list(map(float,tokens[1:]));span=tokens[0];gs={'span_id':span,'length_m':vals[0],'bw_cm':vals[1]*100,'h_cm':vals[2]*100,'source':record,'interpretation':'literal explicit B row under geometry header; task adapter, original extractor unchanged'}
   series={}
   for obs in blocks[beam]:
    mt=re.match(r'\s*(M MN\.|M MX\.|Q MN\.|Q MX\.|MT MX\.)\s*VAO=\s*(\d+B)\s+(.+)',obs['text'])
    if mt and mt[2]==span:series[mt[1]]={'values':[float(v)*9.80665 for v in mt[3].split()],'source':obs}
   n=int(span[:-1]);right=n>max(v[-1]['span'] for v in views)
   ctx,mp,mn,sd,bars,sups,axes,clear,sr=views[-1 if right else 0]
   if right:
    start=float(mp.xs[-1]);end=start+vals[0];external=axes[-1]+sups[-1]['width_cm']/200;physical=[external,end]
   else:
    end=float(mp.xs[0]);start=end-vals[0];external=axes[0]-sups[0]['width_cm']/200;physical=[start,external]
   cc=copy.deepcopy(ctx);cc['section']['h']=gs['h_cm'];cc['section']['bw']=gs['bw_cm'];cc['span_domain_m']=[start,end]
   gs.update(sampled_domain_m=[start,end],physical_domain_m=physical,physical_length_m=round(physical[1]-physical[0],4),side='RIGHT' if right else 'LEFT',series=series,positive_support_reclassification='column with cantilever on far side is not END of physical beam')
   if set(series)>={'M MN.','M MX.','Q MN.','Q MX.'} and physical[1]>physical[0]:
    xs=[start+j*vals[0]/12 for j in range(13)]
    neg=MomentDiagram([{'x_m':x,'value_knm':v,'section':i+1,'provenance':series['M MN.']['source']} for i,(x,v) in enumerate(zip(xs,series['M MN.']['values']))],{'source':series['M MN.']['source']})
    active=[b for b in bars if b['function']=='negative' and b['x_start_common']<=sum(physical)/2<=b['x_end_common']]
    try:
     c=r.prepare(active,active,cc);flex=check_flexure_regions(active,c,neg,r.api,flexure_sign='NEGATIVE',domain=physical);gs['negative_flexure']=flex
    except (ValueError,TypeError,KeyError,IndexError) as e:gs['negative_flexure']={'passes':None,'diagnostics':[str(e)]}
    sd2=ShearDiagram([{'quantity':'shear','unit':'kN','positions':xs,'sections':list(range(1,14)),'values':series[k]['values'],'series_id':k,'provenance':series[k]['source']} for k in ('Q MX.','Q MN.')]);q=sd2.maximum(*physical)
    try:
     design=r.design_shear(cc,r.public_shear_api(),q['Vsk_abs_kn'],5);provided=2*r.api.Barra(5).area_cm2/14*100
     gs['shear']={'Vsk_abs_kn':q['Vsk_abs_kn'],'provided_cm2_m':provided,'assumed_distribution':'5mm/14cm; corroborated by separate B strip in drawing for right 70cm except pending left V626','required_cm2_m':design.get('governing_Asw_per_s_cm2_m'),'design':design,'area_sufficient':provided>=design['governing_Asw_per_s_cm2_m']}
     if not right and beam=='V626':gs['shear']['area_sufficient']=None;gs['shear']['assumed_distribution']='Left 32cm: N7 phi10/8; local h47, d and matching physical B demand remain special'
    except (ValueError,TypeError,KeyError,IndexError) as e:gs['shear']={'passes':None,'diagnostics':[str(e)]}
   items.append(gs)
 if items:B[beam]=items
 raw=json.loads((P/(beam+'_tqs_raw.json')).read_text(encoding='utf8'))
 for q in raw['categorias']['reacoes']:
  n=q.get('normalizacao') or {};c=n.get('campos',{});receiver=c.get('nome')
  if q.get('origem',{}).get('arquivo')=='VGESFS.LST' and receiver and receiver.startswith('V'):
   value=c['maxima']['normalizado']['valor'];minv=c['minima']['normalizado']['valor'];row={'supported_beam':beam,'receiving_beam':receiver,'R_max_kn':value,'R_min_kn':minv,'source':q['origem'],'status':'INCONCLUSIVE','pending':['projected physical receiving axis and same elevation confirmation','reaction nature and envelope selection/concomitance confirmation','combined regional shear+suspension and overlapping reactions']}
   if receiver in r.RUNTIME:
    rc=r.RUNTIME[receiver][0][0];reaction={'source':q['origem'],'nature':'CHARACTERISTIC','is_total':True,'total_source':'VGESFS total R.APOIO-NO; conditional interpretation','combination':'maximum global model envelope; no concomitance claimed','supported_beam_id':beam,'receiving_beam_id':receiver,'unit':'kN','downward_sign':1,'value':value}
    area=reaction_area(reaction,rc,r.api,{'supported_beam_id':beam,'receiving_beam_id':receiver});row['conditional_area_cm2']=area.get('as_suspension_cm2');row['receiving_height_cm']=rc['section']['h'];row['conditional_suspension_only_rate_cm2_m']=area['as_suspension_cm2']/rc['section']['h']*100 if area.get('as_suspension_cm2') else None;row['conditional_assumptions']='R is total characteristic downward maximum; interior distribution of total receiver height. No placement or global approval.'
   reactions.append(row)
(P/'cantilever_review.json').write_text(json.dumps(B,ensure_ascii=False,indent=2),encoding='utf8');(P/'suspension_inventory.json').write_text(json.dumps(reactions,ensure_ascii=False,indent=2),encoding='utf8')
for b,v in B.items():print(b,[(q['span_id'],q['physical_domain_m'],q.get('negative_flexure',{}).get('passes'),q.get('shear',{}).get('area_sufficient')) for q in v])
print('REACTIONS',[(x['supported_beam'],x['receiving_beam'],round(x['R_max_kn'],2),round(x.get('conditional_suspension_only_rate_cm2_m',0),2)) for x in reactions])
