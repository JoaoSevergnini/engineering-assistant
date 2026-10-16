from pathlib import Path
import json,sys,math,copy
from dataclasses import asdict
R=Path(r'\\srvmaster\PUBLICO\Joao Severgnini\Simon\engineering-assistant');O=R/'analises/atp_s07_vigas_terreo/rodada_05_relatorio_global';sys.path[:0]=[str(R/'tools/reinforcement_checks'),str(R.parent/'concretopy')]
import concretopy as api
from shear_review import design_shear,public_shear_api
D=json.loads((O/'verificacoes_globais_concretopy.json').read_text(encoding='utf8'));T=json.loads((O/'tqs_operacional_atual.json').read_text(encoding='utf8'));out=[]
def v(vs,x,L):
 t=max(0,min(12,x/L*12));i=min(int(t),11);return vs[i]+(vs[i+1]-vs[i])*(t-i)
def maxpos(ms,a,z,L):
 return max([{'Mk_tfm':max(0,v(s['original_values'],x,L)),'x_model_m':x,'source':s['source'],'series':s['label']} for s in ms for x in [a,z]+[k*L/12 for k in range(13) if a<=k*L/12<=z]],key=lambda x:x['Mk_tfm'])
def capacity(cfg,h):
 sec=api.SecaoRetangular(24,h,3.5,diametro_estribo_mm=6.3);ls=[api.CamadaArmaduraLongitudinal(q,api.Barra(cfg['phi'])) for q in cfg['layers']];ds=api.calcular_alturas_uteis_camadas(sec,ls);ls=[api.CamadaArmaduraLongitudinal(q.numero_barras,q.barra,d) for q,d in zip(ls,ds)];r=asdict(api.verificar_flexao_viga_retangular(sec,api.Concreto(35),api.Aco(500),ls,gamma_f=1.4,verificar_armadura_minima=True));r['MRd_over_gamma_f_tfm']=r['mrd_kncm']/100/9.80665/1.4;r['minimum_by_actual_section']={'Mk_min_eq_tfm':.8*(24*h*h/6)*api.Concreto(35).fctk_sup*.1/100/9.80665/1.4,'As_absolute_min_cm2':.0015*24*h};r['minimum_by_actual_section']['passes']=r['MRd_over_gamma_f_tfm']>=r['minimum_by_actual_section']['Mk_min_eq_tfm'] and r['as_total_cm2']>=r['minimum_by_actual_section']['As_absolute_min_cm2'];return r
for bid,axes,leftface,rightface,depev in [('V49',2.87,.095,.105,0),('V50',4.46,.20,.105,.05)]:
 b=next(x for x in D['results'] if x['beam_id']==bid);L=b['model_length_m'];xt=axes-rightface-1.30-depev;a=leftface-depev;z=axes-rightface-depev;ms=[s for s in T[bid]['series'] if s['label'] in ['M MX.','M MN.']];cfg=b['positive']['configuration'];rr=[]
 for h,aa,zz in [(50,a,xt),(87,xt,z)]:
  m=maxpos(ms,aa,zz,L);c=capacity(cfg,h);rr.append({'h_cm':h,'interval_model_m':[aa,zz],'demand':m,'concretopy':c,'capacity_passes':c['MRd_over_gamma_f_tfm']>=m['Mk_tfm']})
 source={'form':'7202 R03; cota130cm da mudanca de altura ate a face interna deP749/P751; larguras21cm dos pilares,19cmV26/40cmV34; altura50/87 indicada','detailing':'7403 R01; elevacao com fundo continuo, cortesA/B e armaduras das marcas','V50_axis_check':'415,5cm livres +20cm V34 +10,5cm P751 =446cm entre eixos; TQS441cm+DEPEV5cm=446cm','V49_axis_check':'267cm entre faces, mais9,5cm V26 e10,5cm P749=287cm entre eixos; faixa140+127cm cobre267cm','mapping':'Sem reescala; x_comum=x_TQS+DEPEV_esquerdo; transicao=distancia_eixos-meia_largura_pilar-130cm'}
 b['section_geometry_status']='TRANSICAO_50_87_COTADA_7202_ASSOCIADA_A_EIXOS';b['positive']['regional_checks_C35']=rr;b['positive']['regional_capacity_passes']=all(x['capacity_passes'] for x in rr);b['positive']['transition_model_m']=xt;b['positive']['geometry_source']=source
 for ng in b['negative']:ng['geometry_pending']=False;ng['geometry_source']=source
 b['domain']['column_face_reference_proved']=True;b['domain']['start_model_m']=a;b['domain']['end_model_m']=z;b['domain']['source']='7202/7403: intervalo comprovado ate faces dos apoios; consulta conservadora pode abranger partes embutidas em blocos; nao identifica essas faces de pilar como faces dos blocos'
 out.append({'beam':bid,'span_axes_m':axes,'model_offset_left_m':depev,'clear_between_column_faces_m':z-a,'step_distance_from_right_column_face_m':1.30,'transition_model_m':xt,'source':source,'positive_regions':rr,'positive_status':'INSUFICIENTE_NO_TRECHO_H50','stirrup_boundary_note':'FaixaN4 termina3cm apos transicao naV49 e3,5cm apos naV50 quando comprimentos totais sao medidos desde as faces. Conferir referencia real de inicio/fim/posicao do primeiro estribo; dimensao de faixa nao e posicao individual de cada peca. Nenhuma falta de armadura foi inferida dessa diferenca.'})
(O/'verificacoes_globais_concretopy.json').write_text(json.dumps(D,ensure_ascii=False,indent=2),encoding='utf8');(O/'geometria_e_flexao_regional_V49_V50.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
for b in out:print(json.dumps({'beam':b['beam'],'step_x':b['transition_model_m'],'regions':[{'h':q['h_cm'],'mk':q['demand']['Mk_tfm'],'cap':q['concretopy']['MRd_over_gamma_f_tfm'],'passes':q['capacity_passes']} for q in b['positive_regions']]},ensure_ascii=True))