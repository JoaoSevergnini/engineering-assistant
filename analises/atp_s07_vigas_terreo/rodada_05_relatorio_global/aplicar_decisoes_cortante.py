from pathlib import Path
import json,sys,hashlib,inspect
R=Path(r'\\srvmaster\PUBLICO\Joao Severgnini\Simon\engineering-assistant');O=R/'analises/atp_s07_vigas_terreo/rodada_05_relatorio_global';sys.path[:0]=[str(R/'tools/reinforcement_checks'),str(R.parent/'concretopy')]
from shear_review import design_shear,public_shear_api
import concretopy as api
D=json.loads((O/'verificacoes_globais_concretopy.json').read_text(encoding='utf8'));T=json.loads((O/'tqs_operacional_atual.json').read_text(encoding='utf8'))
def interp(v,x,L):
 u=max(0,min(12,x/L*12));i=min(int(u),11);return v[i]+(v[i+1]-v[i])*(u-i)
for b in D['results']:
 if b['beam_id']=='V21' and b['span_token']=='1':b['domain']['physical_block_faces_proved']=False;b['domain']['left_face_status']='NAO_COMPROVADA_INTEGRALMENTE';b['domain']['right_face_status']='PC55C_BLOCO70_COMPROVADO'
 for q in b['shear']:
  s=q['scenarios'][0];s['adopted_requirement_cm2_m']=s['required_cm2_m'];s['adopted_area_passes']=s['area_passes'];s['adopted_basis']='Maximo da faixa entre faces; sem reducao'
  if not ((b['beam_id']=='V21' and b['span_token']=='1') or (b['beam_id']=='V37' and q['mark']=='N7')):continue
  a,z=q['start_model_m'],q['end_model_m'];d=q['depth_selection']['d_cm'];L=b['model_length_m']
  if b['beam_id']=='V21':
   a=0 # include the complete left model end; no PC54C face is needed for this conservative force check
   z=min(z,b['domain']['end_model_m']-d/200)
  else:a=max(a,b['domain']['start_model_m']+d/200)
  pts=[(abs(interp(t['original_values'],x,L)),x,t['source']) for t in T[b['model_name']]['series'] if t['span_token']==b['span_token'] and t['label'].startswith('Q') for x in [a,z]+[k*L/12 for k in range(13) if a<=k*L/12<=z]];v,x,src=max(pts,key=lambda x:x[0]);ctx={'section':{'bw':b['section_cm'][0],'h':q['section_height_cm'],'cobrimento':3.5,'diametro_estribo_mm':q['diameter_mm']},'fck_mpa':35,'fyk_mpa':500,'gamma_f':1.4,'gamma_c':1.4,'gamma_s':1.15,'effective_depth':{'status':'PASS','d_cm':d,'selected':q['depth_selection']},'axial_force_kn':0,'stirrup_angle_degrees':90};rr=design_shear(ctx,public_shear_api(),v*9.80665,q['diameter_mm']);q['adopted_direct_support_check']={'Vk_tf':v,'position_m':x,'interval_m':[a,z],'source':src,'concretopy':rr,'confirmation':'Joao confirmou cargas superiores/reacao inferior; NBR6118:2023 17.4.1.2.1; somente apoio identificado'};s['adopted_requirement_cm2_m']=rr['governing_Asw_per_s_cm2_m'];s['adopted_area_passes']=q['provided_cm2_m']>=s['adopted_requirement_cm2_m'];s['adopted_basis']='d/2 no PC55C' if b['beam_id']=='V21' else 'd/2 no P725'
D['engine_provenance']={}
for fun in [api.verificar_flexao_viga_retangular,design_shear]:
 p=Path(inspect.getsourcefile(fun));D['engine_provenance'][fun.__name__]={'file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
D['main_fck_mpa']=35;D['secondary_fck_mpa']=40;D['engineer_decisions']=str(O/'decisoes_confirmadas_2026-10-16.json')
(O/'verificacoes_globais_concretopy.json').write_text(json.dumps(D,ensure_ascii=False,indent=2),encoding='utf8')
print('C35: verificacoes adotadas e proveniencia atualizadas; dominios fisicos completos',sum(x['domain']['physical_block_faces_proved'] for x in D['results']))