from pathlib import Path
import sys,json,pickle,types,copy
P=Path(r'\\srvmaster\PUBLICO\Joao Severgnini\Simon\engineering-assistant\analises\silva_jardim_tipo');ns={};exec((P/'review.py').read_text(encoding='utf8').split('for beam,t in T.items():')[0],ns);r=types.SimpleNamespace(**ns)
from suspension_review import review_connection
from longitudinal_review import composition_capacity,prepare_reinforcement
from shear_diagram import ShearDiagram
with (P/'runtime_cache.pkl').open('rb') as f:r.RUNTIME,r.OUTPUT=pickle.load(f)
class YieldLimitedSteel(r.api.Aco):
 def fyd(self,gamma_s=1.15):return min(super().fyd(gamma_s),500/1.15)
api=r.public_shear_api();api.Aco=YieldLimitedSteel
I=json.loads((P/'suspension_inventory.json').read_text(encoding='utf8'));B=json.loads((P/'cantilever_review.json').read_text(encoding='utf8'))
# Beam outline dashed crossings; physical centers computed from two sides at actual 1:50 vector scale.
MAP={('V606','V623'):(2.2987,[2.2288,2.3686]),('V624','V604'):(3.6854,[3.5911,3.7797]),('V628','V604'):(11.2394,[11.1441,11.3347]),('V624','V610'):(7.4735,[7.3792,7.5678]),('V628','V610'):(15.0329,[14.9386,15.1271]),('V603','V611'):(3.80825,[3.7373,3.8792]),('V602','V611'):(5.4979,[5.428,5.5678]),('V607','V621'):(2.0424,[1.9725,2.1123]),('V606','V621'):(2.4809,[2.411,2.5508]),('V607','V619'):(2.0445,[1.9746,2.1144]),('V608','V616'):(.6547,[.5593,.75]),('V619','V609'):(2.18855,[2.0932,2.2839])}
results=[]
for obs in I:
 sender,recv=obs['supported_beam'],obs['receiving_beam'];key=(sender,recv)
 if key not in MAP:
  results.append({'sender':sender,'receiver':recv,'status':'SPECIAL','reaction':obs,'diagnostics':['cantilever-end suspension distribution origin requires explicit confirmation; model reaction preserved']});continue
 axis,faces=MAP[key];views=r.RUNTIME[recv];v=next((q for q in views if q[7][0]<=axis<=q[7][1]),None)
 if v is None:results.append({'sender':sender,'receiver':recv,'status':'INCONCLUSIVE','diagnostics':['receiving axis outside physical span']});continue
 ctx,mp,mn,sd,bars,sups,axes,clear,sr=v;cc=copy.deepcopy(ctx);cc['fyk_mpa']=500 if all(e['phi_mm']==6.3 for e in sr['shear']) else 600
 regions=[{'id':str(n),'diameter_mm':e['phi_mm'],'spacing_cm':e['spacing_cm'],'legs':2,'interval_m':e['drawn_interval_m'],'source':{'pdf':r.D[recv]['pdf'],'interpretation':e['source']},'physical_function':'CONVENTIONAL_SHEAR_STIRRUP'} for n,e in enumerate(sr['shear'])]
 span={'span_id':sr['span'],'series':sd.series,'drawn_regions':regions,'reference_legs':2,'explicit_physical_beam_domain_m':clear,'explicit_physical_domain_source':sr['geometry']}
 if recv=='V611':span['section_changes_m']=[3.88,5.43]
 sg=r.RUNTIME[sender][0][0]['section']
 connection={'id':sender+'->'+recv,'type':'BEAM_ON_BEAM','receiving_beam_id':recv,'supported_beam_id':sender,'transfer_confirmed':True,'transfer_source':obs['source'],'suspension_applicable':True,'applicability_source':'office indirect-support review criterion, conditioned to full node load path','supported_geometry':{'height_cm':sg['h'],'width_cm':sg['bw'],'source':r.D[sender]['pdf']},'placement':'INTERIOR','projected_axis_m':axis,'axis_source':{'pdf':r.D[recv]['pdf'],'page':1,'graphical_crossing_faces_m':faces,'coordinate_source':'black dashed receiving-elevation intersection + form association; beam support direction explicitly documented in VGESFS','scale':'0.5664 PDF points/cm; coordinate uncertainty approx 1cm; all accepted regions stable under this sensitivity'},'reaction':{'source':obs['source'],'nature':'CHARACTERISTIC','is_total':True,'total_source':'VGESFS R.APOIO-NO total reaction at named receiving beam','combination':'maximum characteristic envelope adopted as conditional review, nonconcomitant with receiving shear envelope','supported_beam_id':sender,'receiving_beam_id':recv,'unit':'kN','downward_sign':1,'value':obs['R_max_kn']}}
 ans=review_connection(connection,recv,[span],cc,api);ans['conditional_assumptions']='Rk total, maximum downward model envelope, suspension applicability and office combination of separate maxima; explicit case selection must be ratified';ans['sender']=sender;ans['receiver']=recv
 if recv=='V621':ans['diagnostics'].append('V606 and V607 suspension intervals overlap: no authorized combination rule; individual checks only');ans['suspension_passes']=None if ans.get('suspension_passes') is True else ans.get('suspension_passes');ans['overall_result']='INCONCLUSIVE' if ans['overall_result']=='PASS' else ans['overall_result']
 results.append(ans)
# Independent local check of documented left V626 B strip, not a suspension certificate.
view=r.RUNTIME['V626'][0];ctx,mp,mn,sd,bars,*_=view;cc=copy.deepcopy(ctx);cc['section'].update(h=47,diametro_estribo_mm=10);cc['fyk_mpa']=500
bs=B['V626'][0];physical=bs['physical_domain_m'];mid=sum(physical)/2;nb=[b for b in bars if b['function']=='negative' and b['x_start_common']<=mid<=b['x_end_common']];pc=r.prepare(nb,nb,cc);pb=prepare_reinforcement(nb,pc,r.api,flexure_sign='NEGATIVE');cap=composition_capacity(pb,mid,pc,r.api,flexure_sign='NEGATIVE');d=cap['concretopy']['d_equivalente_cm'];cc['effective_depth']={'status':'PASS','d_cm':d,'selected':{'source':'documented N4+N3 local stub upper layers, h47, phi10 stirrup'}}
lo,hi=bs['sampled_domain_m'];xs=[lo+j*(hi-lo)/12 for j in range(13)];sd2=ShearDiagram([{'quantity':'shear','unit':'kN','positions':xs,'sections':list(range(1,14)),'values':bs['series'][k]['values'],'series_id':k,'provenance':bs['series'][k]['source']} for k in ('Q MX.','Q MN.')]);q=sd2.maximum(*physical);des=r.design_shear(cc,api,q['Vsk_abs_kn'],10);provided=2*r.api.Barra(10).area_cm2/8*100
bs['local_stub_cisaillement']={'d_cm':d,'Vsk_abs_kn':q['Vsk_abs_kn'],'provided_cm2_m':provided,'design':des,'area_sufficient':provided>=des['governing_Asw_per_s_cm2_m'],'source':'PDF N7 4phi10/8, (32), section19/47; VGESFS 1B'}
(P/'suspension_regional_review.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf8');(P/'cantilever_review.json').write_text(json.dumps(B,ensure_ascii=False,indent=2),encoding='utf8')
for q in results:print(q.get('sender'),q.get('receiver'),q.get('overall_result',q.get('status')),[(v.get('asw_per_s_total_required'),v.get('provided',{}).get('Asw_per_s_cm2_m'),v.get('overall_result')) for v in q.get('subintervals',[])],q.get('diagnostics'))
print('V626local',d,q if False else bs['local_stub_cisaillement']['area_sufficient'],des.get('governing_Asw_per_s_cm2_m'))
