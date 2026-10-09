from pathlib import Path
import json,pickle,types,copy,itertools
P=Path(r'\\srvmaster\PUBLICO\Joao Severgnini\Simon\engineering-assistant\analises\silva_jardim_tipo');ns={};exec((P/'review.py').read_text(encoding='utf8').split('for beam,t in T.items():')[0],ns);r=types.SimpleNamespace(**ns)
from concretopy.normas import espacamento_min_arm_long_viga
with (P/'runtime_cache.pkl').open('rb') as f:r.RUNTIME,r.OUTPUT=pickle.load(f)
# Material adapter only; all resistant expressions stay in existing Concretopy.
class ConservativeStirrupSteel(r.api.Aco):
 def fyd(self,gamma_s=1.15):return min(super().fyd(gamma_s),500/1.15)
public=r.public_shear_api();public.Aco=ConservativeStirrupSteel
out={};fits={}
for beam,views in r.RUNTIME.items():
 sv=[];fv=[]
 for ctx,mp,mn,sd,bars,sups,axes,clear,sr in views:
  for e in sr['shear']:
   t=copy.deepcopy(e);p=e['phi_mm'];cc=copy.deepcopy(ctx);cc['fyk_mpa']=600 if p==5 else 500
   if e['status']!='INCONCLUSIVE':
    des=r.design_shear(cc,public,e['Vsk_abs_kn'],p);prov=e['provided_Asw_per_s_cm2_m'];required=des['governing_Asw_per_s_cm2_m'];t.update(design=des,area_sufficient=prov>=required,spacing_sufficient=e['spacing_cm']<=des['maximum_spacing_code_cm']);t['status']='PASS' if t['area_sufficient'] and t['spacing_sufficient'] and des['diagonal_compression']['passes'] else 'FAIL'
   t.update(span=sr['span'],steel_class='CA60' if p==5 else 'CA50',fyk_for_minimum_mpa=cc['fyk_mpa'],fywd_adopted_mpa=500/1.15,material_source='PDF steel schedule: phi5 60B, phi6.3 50A',interpretation='fywd deliberately limited to 434.78MPa for both grades; minimal rate uses actual fyk; not a certificate of integral standard compliance')
   sv.append(t)
  for sign,regs in sr['flexure'].items():
   subset=[b for b in bars if b['function']==('positive' if sign=='POSITIVE' else 'negative')]
   for q in regs:
    mid=(q['start_m']+q['end_m'])/2;active=[b for b in subset if b['x_start_common']<=mid<=b['x_end_common']]
    for layer in range(max([len(b['layers']) for b in active],default=0)):
     phis=[b['diameter_mm'] for b in active if len(b['layers'])>layer for _ in range(b['layers'][layer])]
     if not phis:continue
     # Necessary width, minimized over actual bar order; no assumed physical centers.
     orders=set(itertools.permutations(phis)) if len(phis)<=7 else [tuple(sorted(phis))]
     needed=min(sum(order)/10+sum(max(espacamento_min_arm_long_viga(a),espacamento_min_arm_long_viga(b)) for a,b in zip(order,order[1:])) for order in orders)
     inside=ctx['section']['bw']-2*(2.5+ctx['section']['diametro_estribo_mm']/10)
     if needed>inside:
      fv.append({'span':sr['span'],'sign':sign,'interval_m':[q['start_m'],q['end_m']],'marks':q['marks'],'layer':layer+1,'bars_phi_mm':phis,'necessary_width_cm':needed,'inside_stirrup_cm':inside,'status':'VERIFY','interpretation':'Does not fit with the interpreted common physical layer; unresolved overlap layer identity may change conclusion','aggregate_assumption_mm':16,'source':'drawing_inventory.json + existing Concretopy minimum-spacing API'})
 out[beam]=sv;fits[beam]=fv
(P/'shear_review_actual_steel.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8');(P/'executability_review.json').write_text(json.dumps(fits,ensure_ascii=False,indent=2),encoding='utf8')
for b,v in out.items():
 for x in v:
  if x['status']=='FAIL':print('SHEAR',b,x['span'],x['drawn_interval_m'],x['phi_mm'],x['spacing_cm'],x['provided_Asw_per_s_cm2_m'],x['design']['governing_Asw_per_s_cm2_m'])
print('FIT',[(b,len(v)) for b,v in fits.items() if v])
