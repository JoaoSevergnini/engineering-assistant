from pathlib import Path
import json,sys,contextlib,io,hashlib
from dataclasses import asdict
R=Path(r'\\srvmaster\PUBLICO\Joao Severgnini\Simon\engineering-assistant')
B=R/'analises/atp_s07_vigas_terreo';PREV=B/'rodada_03_controles_locais';O=B/'rodada_04_secao_final_blocos'
sys.path[:0]=[str(R/'tools/reinforcement_checks'),str(R.parent/'concretopy')]
import concretopy as api
from shear_review import design_shear,public_shear_api
old=json.loads((PREV/'controles_independentes.json').read_text(encoding='utf-8'))
neg=json.loads((PREV/'revisao_negativos_maximo_apoio.json').read_text(encoding='utf-8'))['rows']
factor=1.4*9.80665
variable={'V23','V24','V42','V49','V50'};zones={'V4','V15','V17','V34','V37','V49','V50'}
def flex(bw,h,phi,cfg,fc):
 sec=api.SecaoRetangular(bw,h,3.5,diametro_estribo_mm=phi)
 layers=[api.CamadaArmaduraLongitudinal(n,api.Barra(cfg['phi'])) for n in cfg['layers']]
 ds=api.calcular_alturas_uteis_camadas(sec,layers)
 layers=[api.CamadaArmaduraLongitudinal(x.numero_barras,x.barra,d) for x,d in zip(layers,ds)]
 result=api.verificar_flexao_viga_retangular(sec,api.Concreto(fc),api.Aco(500),layers,verificar_armadura_minima=False)
 return asdict(result)
results=[]
with contextlib.redirect_stdout(io.StringIO()):
 for beam in old:
  for sp in beam['spans']:
   bid=beam['beam_id'];bw,h=sp['section_cm'];st=sp['shear']['stirrup'];phi=st['diameter_mm'];p=sp['positive']
   item={'beam_id':bid,'model_name':sp['model_name'],'span_token':sp['span_token'],'section_cm':[bw,h],'criteria':'S07 engineer instruction 2026-10-16: final section; exclude longitudinal bars at top of first concrete stage; positive tension lower only; negative tension upper only','positive':{'composition':p['composition'],'Mk_tfm':p['Msk_knm']/9.80665,'scenarios':[]},'negative_supports':[],'shear_scenarios':[],'physical_dependencies':[]}
   for fc in [35,40]:
    rr=flex(bw,h,phi,p['composition'],fc)
    item['positive']['scenarios'].append({'fck_mpa':fc,'concretopy':rr,'Mk_eq_tfm':rr['mrd_kncm']/100/factor,'capacity_sufficient':rr['mrd_kncm']/100>=p['Msd_knm'],'d_cm':rr['d_equivalente_cm']})
   candidates=[{'origin':'positive_lower_final','composition':p['composition'],'result':item['positive']['scenarios'][0]['concretopy']}]
   for n in sp['negative_faces']:
    nr=next(q for q in neg if q['beam_id']==bid and q['model_name']==sp['model_name'] and q['span_token']==sp['span_token'] and q['end']==n['end'])
    nn={'end':n['end'],'support':n['support'],'Mk_tfm':nr['Mk_support_tfm'],'source':nr['governing'],'composition':n['outer_composition'],'scenarios':[]}
    for fc in [35,40]:
     rr=flex(bw,h,phi,n['outer_composition'],fc)
     nn['scenarios'].append({'fck_mpa':fc,'concretopy':rr,'Mk_eq_tfm':rr['mrd_kncm']/100/factor,'capacity_sufficient':rr['mrd_kncm']/100/factor>=nn['Mk_tfm']})
    candidates.append({'origin':'negative_upper_final_'+n['end'],'composition':n['outer_composition'],'result':nn['scenarios'][0]['concretopy']})
    item['negative_supports'].append(nn)
   # Select only eligible final-section tension groups using the existing skill rule.
   selected=min(candidates,key=lambda q:(-len(q['composition']['layers']),-q['result']['as_total_cm2'],q['result']['d_equivalente_cm']))
   depth=selected['result']['d_equivalente_cm']
   item['shear_depth']={'status':'PASS','d_cm':depth,'selected':{'origin':selected['origin'],'composition':selected['composition'],'source':'new Concretopy returned centroid; no intermediate first-stage bars'},'selection':'maximum external tension layers, then maximum As, then minimum returned centroid d','candidates':[{'origin':q['origin'],'composition':q['composition'],'d_cm':q['result']['d_equivalente_cm'],'As_cm2':q['result']['as_total_cm2']} for q in candidates],'previous_depth_cm':sp['shear']['effective_depth_conservative_cm']}
   query=next(q for q in sp['shear']['queries'] if q['scope']=='between_model_faces')
   item['shear_reference']={'scope':'prior model-face query retained as numerical reference only; block-face domain not re-extracted in this update','Vk_tf':query['Vsk_kn']/9.80665,'position_model_local_m':query['position_model_local_m'],'source':query['source'],'stirrup':st,'physical_final_status':'PENDING_BLOCK_FACE_AND_DRAWN_ZONE_RECONCILIATION'}
   for fc in [35,40]:
    ctx={'section':{'bw':bw,'h':h,'cobrimento':3.5,'diametro_estribo_mm':phi},'fck_mpa':fc,'fyk_mpa':500,'gamma_f':1.4,'gamma_c':1.4,'gamma_s':1.15,'effective_depth':item['shear_depth'],'axial_force_kn':0,'stirrup_angle_degrees':90}
    rr=design_shear(ctx,public_shear_api(),query['Vsk_kn'],phi)
    assert rr['status'] in ['PASS','FAIL'],rr
    item['shear_scenarios'].append({'fck_mpa':fc,'concretopy_via_public_adapter':rr,'provided_cm2_m':st['provided_cm2_m'],'required_cm2_m':rr.get('governing_Asw_per_s_cm2_m'),'reference_area_sufficient':rr.get('governing_Asw_per_s_cm2_m') is not None and st['provided_cm2_m']>=rr['governing_Asw_per_s_cm2_m'],'final_physical_passes':None})
   if bid in variable:item['physical_dependencies'].append('Resolve local height/step incidence; retained section labels are not transition verification')
   if bid in zones:item['physical_dependencies'].append('Check each actual stirrup zone with its own Vk peak in block-bounded physical domain')
   if bid=='V21':item['physical_dependencies'].append('Reconcile actual stirrup input with drawing; archived first-span input is phi8, engineer spreadsheet phi6.3')
   if not sp['negative_faces']:item['physical_dependencies'].append('Final upper reinforcement not fully registered; shear depth selection limited to available lower group')
   results.append(item)
assert len(results)==82
out={'date':'2026-10-16','official_resistance_engine':'Concretopy; new executions of verificar_flexao_viga_retangular and dimensionar_cortante_viga through existing shear_review adapter','raw_internal_units':'Preserved engine units kN, kN.cm; presentation is tf/tf.m characteristic equivalent for resistance','gamma_f':1.4,'kN_per_tf':9.80665,'source_efforts':'prior audited TQS snapshots; no new TQS model import','first_stage_top_bars':'excluded from resistance and d by project-specific engineer instruction','coverage_previous_deficits':'withdrawn as insufficiency claims: used pillar faces instead of block faces; no numeric block lengths invented','global_approval':False,'results':results}
(O/'resultados_secao_final_concretopy.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
# Record the callable sources used in this execution.
import inspect
provenance={}
for name,fn in [('flexure',api.verificar_flexao_viga_retangular),('shear',public_shear_api().dimensionar_cortante_viga)]:
 file=Path(inspect.getsourcefile(fn));provenance[name]={'function':fn.__module__+'.'+fn.__name__,'file':str(file),'sha256':hashlib.sha256(file.read_bytes()).hexdigest()}
(O/'proveniencia_concretopy.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'status':'OK','span_checks':len(results),'negative_support_checks':sum(len(x['negative_supports']) for x in results),'changed_shear_depths':sum(abs(x['shear_depth']['d_cm']-x['shear_depth']['previous_depth_cm'])>1e-8 for x in results),'positive_insufficient_in_both':[{'beam':x['beam_id'],'span':x['span_token']} for x in results if all(not q['capacity_sufficient'] for q in x['positive']['scenarios'])]},ensure_ascii=True))
