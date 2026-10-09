import sys,json,copy,contextlib,io
from pathlib import Path
P=Path(r'\\srvmaster\PUBLICO\Joao Severgnini\Simon\engineering-assistant\analises\silva_jardim_tipo');sys.path.insert(0,str(P))
import pickle,types
ns={}
exec((P/'review.py').read_text(encoding='utf8').split('for beam,t in T.items():')[0],ns)
r=types.SimpleNamespace(**ns)
with (P/'runtime_cache.pkl').open('rb') as f:r.RUNTIME,r.OUTPUT=pickle.load(f)
from support_geometry import SupportGeometry
from support_anchorage import check_support
from support_alternatives import effort_pairs
from longitudinal_review import prepare_reinforcement,check_bar_event
from negative_end_support_review import review_negative_end_support
from bar_scaling import check_scaling_event,SUPPORTED_SCOPE
from decimal import Decimal

def trim(x):
 if isinstance(x,list):return [trim(q) for q in x]
 if isinstance(x,dict):return {k:trim(v) for k,v in x.items() if k not in ('provenance','api','api_source','audit_context','concretopy','minimum_check','legacy_node_check','physical_bar','source_region','checks','demand','configuration','context','candidates','governing','end_support_result','capacity','capacity_without_selected_mark','transverse_disposition')}
 return x
extra={}
for beam,views in r.RUNTIME.items():
 res={'supports':[],'negative_ends':[],'negative_cuts':[],'positive_cuts':[],'notes':[]}
 for index,(ctx,mp,mn,sd,bars,sups,axes,clear,sr) in enumerate(views):
  qmax=sd.maximum(float(mp.xs[0]),float(mp.xs[-1]));sh={'status':'resolved','Vk_used_kn':qmax['Vsk_abs_kn'],'provenance':qmax,'series':[{'envelope':'max','source':'VGESFS Q MX.'},{'envelope':'min','source':'VGESFS Q MN.'}]}
  for side,k in [('LEFT',index),('RIGHT',index+1)]:
   s=sups[k];axis=Decimal(str(axes[k]));hw=Decimal(str(s['width_cm']))/200
   geo=SupportGeometry(sr['span'],s['name'],side,'END' if k in (0,len(sups)-1) else 'INTERMEDIATE',float(axis+hw if side=='LEFT' else axis-hw),float(axis-hw if side=='LEFT' else axis+hw),float(axis),s['width_cm'],{'source':s,'derivation':'RELDTFPS ordered supports, VGESFS lengths and DEPEV; physical widths'})
   if beam=='V610' and index==0:res['notes'].append('V610 first span support and cut checks blocked by elevation changes');continue
   cc=copy.deepcopy(ctx);cc.update(cover_cm=ctx['section']['cobrimento'],length_provenance=geo.as_dict(),mk_positive_max_span_kncm=max(0,float(max(mp.ms)))*100,mk_negative_support_kncm=min(0,float(mn.ms[0 if side=='LEFT' else -1]))*100,d_span_cm=ctx['effective_depth'].get('d_cm'),nd_tracao_kn=0,gancho_valido=False)
   # Both documented shear envelopes retained at terminal; envelope pairs do not imply concomitance.
   terminal=0 if side=='LEFT' else -1
   shearvals=[v['values'][terminal] for v in r.T[beam]['series'] if v['span']==sr['span'] and v['label'] in ('Q MX.','Q MN.')]
   cc['pairs']=effort_pairs(max(0,float(mp.ms[terminal]))*100,min(shearvals),max(map(abs,shearvals)),{'source':'VGESFS terminal envelopes, not concomitant combination'})
   pb=[b for b in bars if b['function']=='positive' and geo.penetration(b)['area_presente_na_face']]
   try:
    pc=r.prepare(pb,pb,cc);physical=prepare_reinforcement(pb,pc,r.api,flexure_sign='POSITIVE');answer=check_support(pc,physical,mp,r.api,geometry=geo,shear=sh,generate_corrections=False)
    answer['end_metrics']=answer.get('end_support_result',{}).get('metrics')
    answer['end_diagnostics']=answer.get('end_support_result',{}).get('diagnostics')
    answer['terminal_hypothesis']='Nd=0, no longitudinal normal-force series supplied; hook credit disabled'
    if geo.support_type=='END' and any(b['termination_by_side'][side]=='HOOK' for b in pb):
     hc=copy.deepcopy(pc);hc['gancho_valido']=True;conditional=check_support(hc,physical,mp,r.api,geometry=geo,shear=sh,generate_corrections=False);conditional['end_metrics']=conditional.get('end_support_result',{}).get('metrics')
     answer['conditional_valid_hook_result']=trim(conditional);answer['conditional_valid_hook_result']['interpretation']='conditional calculation only: hook radius, geometry and confinement not proved'
    # Keep elementary area check independent of longitudinal and physical node certification.
    answer['physical_projection_min_cm']=min([geo.penetration(b)['comprimento_penetracao_cm'] for b in pb])
   except (ValueError,KeyError,TypeError,IndexError) as e:answer={'geometry':geo.as_dict(),'diagnostics':[str(e)],'longitudinal_anchorage_passes':None}
   res['supports'].append(trim(answer))
   if geo.support_type=='END' and s['name'].startswith('P'):
    nb=[b for b in bars if b['function']=='negative' and geo.penetration(b)['area_presente_na_face']];nc=copy.deepcopy(cc);nc.update(support_element='COLUMN',support_scenario_provenance=s)
    try:nc=r.prepare(nb,nb,nc)
    except (ValueError,KeyError,TypeError,IndexError):pass
    docs={b['mark']:b.get('bend_documents',{}).get(side) for b in nb if b.get('bend_documents',{}).get(side)}
    ne=review_negative_end_support(nb,nc,mn,r.api,geometry=geo,bend_documents=docs)
    # Retain independent controls; trim intentionally excludes generic checks, add explicitly here.
    compact=trim(ne)
    for out,orig in zip(compact['marks'],ne['marks']):out['checks']=trim(orig['checks'])
    res['negative_ends'].append(compact)
  # Negative horizontal terminal events, branch restricted to monotone end zone.
  for b in [b for b in bars if b['function']=='negative']:
   for cut,key in [('LEFT','x_start_common'),('RIGHT','x_end_common')]:
    event=b[key]
    if not clear[0]<event<clear[1]:continue
    origin='RIGHT' if cut=='LEFT' else 'LEFT';pts=list(zip(map(float,mn.xs),map(float,mn.ms)));pts=pts[::-1] if origin=='RIGHT' else pts
    branch=[pts[0]]
    for pt in pts[1:]:
     if max(0,-pt[1])>max(0,-branch[-1][1])+1e-8:break
     branch.append(pt)
     if pt[1]>=0:break
    dom=sorted([branch[0][0],branch[-1][0]])
    if not dom[0]<event<dom[1]:
     res['negative_cuts'].append({'bar':b['mark'],'event_x_m':event,'cut_side':cut,'passes':None,'diagnostics':['cut outside resolved monotone terminal branch; adjacent support classification required']});continue
    involved=[v for v in bars if v['function']=='negative' and v['x_start_common']<dom[1] and v['x_end_common']>dom[0]]
    try:
     ac=r.prepare([v for v in involved if v['x_start_common']<=event<=v['x_end_common']],involved,ctx)
     involved=copy.deepcopy(involved)
     for v in involved:
      # Documented horizontal segment only; this does not verify or credit external hooks.
      if v.get('termination_by_side',{}).get(cut)!='HOOK':v['shape']='straight'
      v['horizontal_segment_only']=True
     ans=check_bar_event(involved,ac,mn,sh,r.api,mark=b['mark'],cut_side=cut,mode='SCALING',branch_domain=dom)
     item=trim(ans);item['checks']=trim(ans['checks']);item['event_x_m']=event
    except (ValueError,KeyError,TypeError,IndexError) as e:item={'bar':b['mark'],'event_x_m':event,'cut_side':cut,'passes':None,'diagnostics':[str(e)]}
    res['negative_cuts'].append(item)
  # Adapt completed positive regions without changing any resistant engine.
  regs=[]
  for n,a in enumerate(sr['flexure']['POSITIVE']):
   if not a.get('checks'):continue
   rr=a['checks']['regions'][0];gc=copy.deepcopy(a['source_region']['geometric_reinforcement']) if 'geometric_reinforcement' in a['source_region'] else None
   if gc is None:gc={'marks':[v['mark'] for v in bars if v['function']=='positive' and v['x_start_common']<a['end_m'] and v['x_end_common']>a['start_m']],'status':'resolved','layers':a['source_region'].get('layers',[])}
   layers=rr['configuration']['layers'];# Preserve physical layer components from the already audited regional decomposition.
   regs.append({'kind':'interval','region_id':str(n),'x_start_m':a['start_m'],'x_end_m':a['end_m'],'geometric_reinforcement':gc,'transverse_status':'resolved','transverse_geometry':{'bw_cm':ctx['section']['bw'],'h_cm':ctx['section']['h'],'cover_cm':2.5,'stirrup_diameter_mm':ctx['section']['diametro_estribo_mm']},'provenance':{'transverse':ctx['section']},'status':'checked','concretopy_result':rr.get('concretopy')})
  horizontal=copy.deepcopy(bars)
  for v in horizontal:
   v['shape']='straight';v.pop('end_bend',None);v['horizontal_segment_only']=True
  mapping={'beam_id':beam,'reinforcement':horizontal,'supports':{'left':{'inner_face_x':clear[0]},'right':{'inner_face_x':clear[1]}}};rv={'regions':regs,'material_parameters':{'fck_mpa':ctx['fck_mpa'],'gamma_f':ctx['gamma_f']},'material_interpretation':{'status':'consistent','derived_fyk_mpa':ctx['fyk_mpa']}}
  scope={**SUPPORTED_SCOPE,'provenance':{'source':'TQS ordinary horizontal beam, positive straight segment; special geometry kept pending'}}
  for b in [v for v in bars if v['function']=='positive']:
   for side,key in [('left','x_start_common'),('right','x_end_common')]:
    if clear[0]<b[key]<clear[1]:
     ans=check_scaling_event(mapping,rv,mp,sh,r.api,interrupted_mark=b['mark'],cut_side=side,scope=scope) if b.get('termination_by_side',{}).get(side.upper())!='HOOK' else {'interrupted_mark':b['mark'],'cut_side':side,'event_x_m':b[key],'overall':{'scaling_passes':None},'diagnostics':['internal cut has a bend; straight cut scope not applicable']}
     res['positive_cuts'].append(trim(ans))
 extra[beam]=res
 print(beam,'supports',len(res['supports']),'negative ends',len(res['negative_ends']),'cuts',len(res['positive_cuts']),len(res['negative_cuts']),flush=True)
(P/'anchorage_review.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2),encoding='utf8')
(P/'review_compact.json').write_text(json.dumps(trim(r.OUTPUT),ensure_ascii=False,indent=2),encoding='utf8')
