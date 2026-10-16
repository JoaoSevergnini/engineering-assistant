from pathlib import Path
import json,sys,math,inspect,hashlib
from dataclasses import asdict
ROOT=Path(r'\\srvmaster\PUBLICO\Joao Severgnini\Simon\engineering-assistant');OUT=ROOT/'analises/atp_s07_vigas_terreo/rodada_02_modelo_atualizado'
sys.path[:0]=[str(ROOT/'tools/reinforcement_checks'),str(ROOT.parent/'concretopy')]
import concretopy as api
from shear_review import design_shear,public_shear_api
T=json.loads((OUT/'tqs_operacional.json').read_text(encoding='utf8'))
# count, phi, optional layer distribution. Intermediate-height steel deliberately not moved to an outer layer.
def bar(n,p,l=None):return {'count':n,'phi':p,'layers':l or [n]}
B16=lambda n:bar(n,16);B20=lambda n:bar(n,20);B12=lambda n:bar(n,12.5);B10=lambda n:bar(n,10)
C={
1:('V1',['1'],30,55,[B16(4)],[B16(4),B16(4)],6.3,15,2,True),
2:('V2',['1','2','3'],30,50,[B16(4),B16(3),B16(4)],[B16(4),B20(3),B20(3),B16(4)],6.3,15,2,True),
4:('V4',['1'],40,50,[B20(6)],[B20(6),B20(5)],6.3,20,4,False),
14:('V33',['1','2','3'],19,50,[B16(2)]*3,[B16(2)]*4,6.3,15,2,False),
15:('V12',['1','2'],40,50,[B20(4)]*2,[B12(4),B20(6),B16(4)],6.3,20,4,False),
16:('V13',['1'],40,50,[B12(4)],[B16(4),B16(4)],6.3,20,4,True),
17:('V14',['1','2','3','4','5','6'],40,50,[B20(4)]*3+[B20(5)]*3,[B10(4),B20(5),B20(5),B20(7),B20(7),bar(5,20,[4,1]),B10(4)],8,17,4,False),
21:('V15',['1','2','3','4','5','6'],30,50,[B20(4),B20(3),B20(3),B16(5),B12(3),B12(4)],None,8,17,2,False),
22:('V16',['2','3'],30,50,[B12(4),B16(4)],[B12(2),B20(3),B10(2)],6.3,15,2,False),
25:('V19',['2','3','4','5'],30,50,[B20(3),B20(2),B12(3),B12(2)],[B16(4),B16(4),B16(2),B12(3),B10(3)],6.3,15,2,False),
26:('V20',['1','2','3'],19,50,[B16(2)]*3,[B16(2)]*4,6.3,15,2,False),
28:('V22',['2','3'],40,50,[B20(4),B16(4)],[B16(4),B20(4),B10(4)],6.3,15,4,False),
29:('V23',['1'],19,165,[bar(3,20,[2,1])],[bar(3,16,[2,1])]*2,6.3,17,2,False),
31:('V25',['1B'],19,165,[bar(4,20,[2,2])],[B10(2),bar(3,16,[2,1])],6.3,17,2,False),
32:('V26',['2','3'],40,50,[B20(4),B16(4)],[B16(4),B20(4),B10(4)],6.3,15,4,False),
34:('V28',['1'],40,50,[B20(5)],[B20(4),B20(6)],8,20,4,False),
39:('V30',['1'],19,165,[bar(3,20,[2,1])],[bar(3,16,[2,1])]*2,6.3,17,2,False),
41:('V32',['1B'],19,165,[bar(4,20,[2,2])],[B10(2),bar(3,16,[2,1])],6.3,17,2,False),
43:('V35',['2','3','4','5'],30,50,[B20(3),B20(2),B20(2),B12(3)],[B16(3),B20(3),B16(3),B16(3),B10(4)],6.3,15,2,False)}

for n,v in list(C.items()):
 model,tokens,bw,h,pos,neg,phi,s,legs,complete=v
 tokens=[g['span_token'] for g in T[f'V{n}']['geometry'] if g['span_token']!='1B'] if n not in [31,41] else ['1B']
 if n==15:pos=[B20(4)]*3+[B20(6)];neg=[B12(4),B20(6),B16(4),B20(8),B20(6)]
 C[n]=(f'V{n}',tokens,bw,h,pos,neg,phi,s,legs,complete)
C.update({
5:('V5',['1'],19,50,[B16(3)],[B20(2),bar(3,20,[2,1])],10,12,2,False),
11:('V11',['1'],24,80,[B20(2)],[B10(3),B12(2)],8,15,2,False),
18:('V18',['1','2'],30,50,[B16(3),B16(2)],[B10(2),B20(3),B20(2)],6.3,15,2,False),
19:('V19',['1'],30,50,[B16(3)],[B16(4)]*2,6.3,15,2,False),
20:('V20',['1'],30,50,[B16(3)],[B16(4)]*2,6.3,15,2,False),
27:('V27',['1'],24,50,[B20(2)],[B16(4),B16(2)],8,12,2,False),
30:('V30',['1'],24,60,[B16(2)],[B12(3),B16(3)],6.3,12,2,False),
33:('V33',['1'],30,50,[B12(3)],[B20(2)]*2,8,15,2,True),
35:('V35',['1','2'],30,50,[B20(2),B16(2)],[B16(3),B16(4),B10(3)],6.3,15,2,False),
36:('V36',['1'],30,50,[B16(4)],[B10(2),B16(4)],6.3,15,2,False),
37:('V37',['1'],30,50,[B20(2)],[B16(4),B20(4)],6.3,15,2,False),
38:('V38',['1'],24,50,[B20(2)],[B16(4),B10(3)],8,12,2,False),
40:('V40',['1'],30,50,[B12(3)],[B20(2)]*2,8,15,2,True),
44:('V44',['1'],40,50,[B20(4)],[B12(4),B16(4)],8,17,4,False),
45:('V45',['1'],24,50,[B20(2)],[B10(3),B12(2)],6.3,20,2,False),
46:('V46',['1'],30,50,[B20(3)],[B20(3),B10(4)],6.3,15,2,False),
47:('V47',['1'],30,50,[B20(2)],[B20(3),B10(3)],8,10,2,False),
48:('V48',['1'],30,50,[B20(2)],[B12(4),B16(4)],6.3,15,2,False)
})

# Variable sections: conservative positive/shear screen at minimum DRAWN depth only.
# Do not use this lower bound as a geometric reconciliation or for minimum steel at h>50.
C.update({
23:('V23',['1','2'],30,50,[B16(2),B16(2)],None,6.3,15,2,False),
24:('V24',['1','2','3'],30,50,[B12(2),B20(2),B20(2)],None,6.3,15,2,False),
42:('V42',['1','2','3','4','5','6','7'],30,50,[B16(2),B10(3),B16(2),B20(2),B20(2),B20(2),B16(2)],None,6.3,15,2,False),
49:('V49',['1'],24,50,[B12(3)],None,6.3,20,2,False),
50:('V50',['1'],24,50,[B16(2)],None,6.3,20,2,False)
})
C[240]=('V23',['3'],30,80,[B20(3)],[B16(4),B16(4)],6.3,15,2,False)
R=[]
for n,(model,tokens,bw,h,pos,neg,phi,s,legs,complete) in C.items():
 entry={'beam_id':f'V{n}','model_name':model,'status':'SECTION_SCREENING_NOT_GLOBAL_APPROVAL','section_cm':[bw,h],'source':'manual visual observations in crops; TQS series in tqs_operacional.json','composition_complete_at_positive_peak':complete,'limitations':['Both C35 and C40 checked as sensitivity; staged compression block not replaced by an invented homogeneous material.','Only listed outer tension steel credited; intermediate-height bars not moved into this layer.','Negative maximum may lie in support; face mapping/limits require regional verification.','Minimum stirrup spacing and indirect suspension remain independent.'],'spans':[]}
 if n in [23,24,42,49,50]:entry['limitations'] += ['VARIABLE SECTION LOWER-BOUND SCREEN h50 ONLY; not physical regional verification; minima at larger heights remain pending.']
 for j,token in enumerate(tokens):
  series=[q for q in T[model]['series'] if q['span_token']==token];g=next(g for g in T[model]['geometry'] if g['span_token']==token)
  sp={'token':token,'model_length_m':g['length_m'],'checks':[]}
  moments=[q for q in series if q['label'] in ['M MX.','M MN.']];qseries=[q for q in series if q['label'].startswith('Q')]
  for sign in ['POSITIVE','NEGATIVE']:
   choices=[(v,k,q) for q in moments for k,v in enumerate(q['values_si'])];v,k,q=(max(choices,key=lambda z:z[0]) if sign=='POSITIVE' else min(choices,key=lambda z:z[0]));mk=max(0,v if sign=='POSITIVE' else -v)
   cfg=pos[j] if sign=='POSITIVE' else (None if neg is None or k not in [0,12] else neg[j if k==0 else j+1])
   ch={'sign':sign,'Msk_knm':mk,'Msd_knm':mk*1.4,'section_index':k+1,'source':q['source'],'composition':cfg,'results':[]}
   if not cfg:ch['state']='COMPOSITION_RECONCILIATION_REQUIRED';sp['checks'].append(ch);continue
   for fck in [35,40]:
    sec=api.SecaoRetangular(bw=bw,h=h,cobrimento=3.5,diametro_estribo_mm=phi)
    layers=[api.CamadaArmaduraLongitudinal(count,api.Barra(cfg['phi'])) for count in cfg['layers']]
    ds=api.calcular_alturas_uteis_camadas(sec,layers)
    layers=[api.CamadaArmaduraLongitudinal(x.numero_barras,x.barra,d) for x,d in zip(layers,ds)]
    flex=api.verificar_flexao_viga_retangular(sec,api.Concreto(fck),api.Aco(500),layers,gamma_c=1.4,gamma_s=1.15,gamma_f=1.4,verificar_armadura_minima=False)
    rr=asdict(flex);mrd=flex.mrd_kncm/100;ac=bw*h;w0=bw*h*h/6;mdmin=.8*w0*api.Concreto(fck).fctk_sup*.1/100
    # Exact minimum route of 17.3.5.2.1, instead of applying tabulated d/h=.8 as an equality to actual d/h.
    ch['results'].append({'fck_mpa':fck,'concretopy':rr,'MRd_knm':mrd,'capacity_sufficient':mrd>=mk*1.4,'utilization':mk*1.4/mrd,'minimum_by_moment':{'Mdmin_knm':mdmin,'As_absolute_min_cm2':.0015*ac,'passes':mrd>=mdmin and flex.as_total_cm2>=.0015*ac,'source':'NBR6118:2023 17.3.5.2.1, printed p131, consulted'},'steel_tension_upper_bound_knm':flex.as_total_cm2*500/1.15*.1*max(ds)/100})
   ch['state']='SCREEN_PASS' if all(r['capacity_sufficient'] for r in ch['results']) else 'REQUIRES_REGIONAL_REVIEW'

   sp['checks'].append(ch)
  shear_cfg=pos[j];depth=h-3.5-phi/10-shear_cfg['phi']/20-(len(shear_cfg['layers'])-1)*(max(2,shear_cfg['phi']/10)+shear_cfg['phi']/10)/2
  vk,k,q=max([(abs(v),k,q) for q in qseries for k,v in enumerate(q['values_si'])],key=lambda z:z[0]);ph=6.3 if n==21 and j>=4 else phi;space=15 if n==21 and j>=4 else s
  sh={'Vk_kn':vk,'Vsd_kn':vk*1.4,'source':q['source'],'section_index':k+1,'stirrup':{'diameter_mm':ph,'spacing_cm':space,'legs':legs,'provided_cm2_m':legs*api.Barra(ph).area_cm2*100/space},'effective_depth_cm':depth,'basis':'outer tension layer centroid; provisional where whole regional inventory not reconciled','results':[]}
  for fck in [35,40]:
   ctx={'section':{'bw':bw,'h':h,'cobrimento':3.5,'diametro_estribo_mm':ph},'fck_mpa':fck,'fyk_mpa':500,'gamma_f':1.4,'gamma_c':1.4,'gamma_s':1.15,'effective_depth':{'status':'PASS','selected':{'source':'section screening only'},'d_cm':depth},'axial_force_kn':0,'stirrup_angle_degrees':90}
   r=design_shear(ctx,public_shear_api(),vk,ph)
   sh['results'].append({'fck_mpa':fck,'design':r,'area_sufficient':sh['stirrup']['provided_cm2_m']>=r['governing_Asw_per_s_cm2_m'] if r.get('governing_Asw_per_s_cm2_m') is not None else None,'spacing_sufficient':space<=r['maximum_spacing_code_cm'] if r.get('maximum_spacing_code_cm') is not None else None,'minimum_spacing':'PENDING_VIBRATOR_ACCESS_18.3.3.2','transverse_branch_spacing':'PENDING_BRANCH_POSITIONS_18.3.3.2'})
  sp['shear']=sh;entry['spans'].append(sp)
 R.append(entry)
supp=next(b for b in R if b['beam_id']=='V240');base=next(b for b in R if b['beam_id']=='V24');supp['spans'][0]['model_name']='V23';supp['spans'][0]['documentary_span']='V24 P785-P778, first detail span; conservative three phi20 only at h80';base['spans'].insert(0,supp['spans'][0]);base['limitations'].append('First detail span belongs to model V23 token3; remaining spans to V24 tokens1-3.');R.remove(supp)
(OUT/'triagem_secoes_criticas.json').write_text(json.dumps(R,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf8')
for b in R:
 flags=[]
 for sp in b['spans']:
  for q in sp['checks']:
   if q.get('results') and any(not r['capacity_sufficient'] for r in q['results']):flags.append((sp['token'],q['sign'],round(q['Msd_knm'],1),round(q['results'][0]['MRd_knm'],1)))
  if any(r['area_sufficient'] is False for r in sp['shear']['results']):flags.append((sp['token'],'SHEAR_AREA_SCREEN',round(sp['shear']['Vsd_kn'],1)))
 print(b['beam_id'],flags)
print('BEAMS_SCREENED',len(R),'SPANS',sum(len(b['spans']) for b in R))
