from pathlib import Path
import sys,json,hashlib,csv,zipfile
P=Path(r'\\srvmaster\PUBLICO\Joao Severgnini\Simon\engineering-assistant\analises\silva_jardim_tipo');sys.path.insert(0,str(P.parent.parent/'tools/reinforcement_checks'))
from beam_diagnostic import consolidate,attach_execution
r=json.loads((P/'revisao_consolidada.json').read_text(encoding='utf8'));A=json.loads((P/'anchorage_review.json').read_text(encoding='utf8'));D=r['source_files'];diagnoses={}
for beam in D:
 cs={'origin':'first left inner support face','direction':'left to right along beam elevation','unit':'m','beam_id':beam};ctx={'beam_id':beam,'floor':'TIPO','coordinate_system':cs,'identity_proof':{'drawing':D[beam]['pdf'],'model':'TQS TIPO, named beam IDs and supports','revision_equivalence':'not fully proved'}};mods=[]
 def module(discipline,checks,filename):
  mods.append({'discipline':discipline,'beam_id':beam,'floor':'TIPO','coordinate_system':cs,'source':{'path':filename,'pointer':beam},'version':'2026-10-08-task-adapter-v1','complete':False,'missing_information':['complete physical node/geometry and integral normative verification not proved'],'checks':checks})
 for sign,disc in [('POSITIVE','positive_flexure'),('NEGATIVE','negative_flexure')]:
  checks=[]
  for i,q in enumerate(x for x in r['flexure'] if x['viga']==beam and x['sinal']==sign):
   state=q['resultado_ensaio'];state='REQUIRES_ENGINEERING_REVIEW' if state=='FAIL' else state
   checks.append({'check_id':f"span{q['vao']}-{q['inicio_m']}-{q['fim_m']}-{q['marcas']}",'check_type':'flexural_capacity','status':state,'span_id':q['vao'],'physical_interval':[q['inicio_m'],q['fim_m']],'drawing_reinforcement_ids':q['marcas'].split(', ') if q['marcas'] else [],'required_value':q['Msk_knm'],'provided_value':q['Mk_equivalente_knm'],'units':'kN.m','comparison':'provided_ge_required','drawing_source':D[beam]['pdf'],'demand_source':beam+'_tqs_raw.json','evidence':{'original_rectangular_test_status':q['resultado_ensaio'],'flange_and_compression_steel_not_credited':True,'inapplicability_proof':'no tension demand in this region' if state=='NOT_APPLICABLE' else None},'reason':'conservative rectangular regional test; geometry composition may be unresolved'})
  for i,q in enumerate(A[beam]['positive_cuts' if sign=='POSITIVE' else 'negative_cuts']):
   result=q.get('overall',{}).get('scaling_passes') if sign=='POSITIVE' else q.get('passes');state='PASS' if result is True else 'REQUIRES_ENGINEERING_REVIEW' if result is False else 'INCONCLUSIVE';x=q.get('event_x_m');checks.append({'check_id':'cut-'+str(q.get('interrupted_mark',q.get('bar_or_group',q.get('bar','unknown'))))+'-'+str(q.get('cut_side'))+'-'+str(x),'check_type':'bar_scaling','status':state,'physical_interval':[x,x] if x is not None else None,'drawing_reinforcement_ids':[q.get('interrupted_mark',q.get('bar_or_group',q.get('bar','unknown')))],'evidence':{'original_result':result,'source':'anchorage_review.json'},'reason':str(q.get('diagnostics',[]))})
  module(disc,checks,'flexao_por_regiao.csv + anchorage_review.json')
 checks=[]
 for q in (x for x in r['shear'] if x['viga']==beam):
  checks.append({'check_id':f"span{q['vao']}-{q['inicio_m']}-{q['fim_m']}",'check_type':'shear_reinforcement','status':q['resultado'],'span_id':q['vao'],'physical_interval':[q['inicio_m'],q['fim_m']],'required_value':q['Asw_s_exigida_cm2_m'],'provided_value':q['Asw_s_fornecida_cm2_m'],'units':'cm2/m','comparison':'provided_ge_required','evidence':{'d_cm':q['d_cm'],'phi_mm':q['bitola_mm'],'spacing_cm':q['espacamento_cm'],'maximum_spacing_cm':q['smax_cm'],'steel_class':q['aco']},'reason':'independent shear area and spacing; scope separate from suspension/torsion'})
 module('shear',checks,'shear_review_actual_steel.json')
 checks=[]
 for q in (x for x in r['positive_end_anchorage'] if x['viga']==beam):
  st=q['ensaio_sem_credito_gancho'];checks.append({'check_id':'positive-'+q['apoio']+'-'+q['lado'],'check_type':'support_anchorage','status':'PASS' if st is True else 'FAIL' if st is False else 'INCONCLUSIVE','required_value':q['As_apoio_cm2'],'provided_value':q['As_presente_cm2'],'units':'cm2','comparison':'provided_ge_required','reason':'END longitudinal calculation, Nd0 and no hook credit; physical projection and full node separate','evidence':q,'category':'SUPPORT_CALCULATION_SHORTFALL' if st is False else 'MISSING_DOCUMENTARY_EVIDENCE'})
 for q in (x for x in r['negative_end_anchorage'] if x['viga']==beam):
  if q['dobra_resultado']=='NOT_APPLICABLE':continue
  checks.append({'check_id':'negative-leg-'+q['apoio']+'-'+q['marca'],'check_type':'vertical_bend_geometry','status':q['dobra_resultado'],'required_value':q['perna_exigida_escritorio_cm'],'provided_value':q['perna_lida_cm'],'units':'cm','comparison':'provided_ge_required','reason':'office vertical-leg criterion, not attributed to unconsulted normative clause','evidence':q,'category':'OFFICE_BEND_CRITERION_NONCONFORMITY' if q['dobra_resultado']=='FAIL' else 'MISSING_DOCUMENTARY_EVIDENCE'})
 module('anchorage',checks,'ancoragem_positiva_extremos.csv + ancoragem_negativa_extremos.csv')
 checks=[]
 for q in (x for x in r['suspension'] if x.get('receiver')==beam):
  state=q.get('overall_result','INCONCLUSIVE');state='INCONCLUSIVE' if state=='SPECIAL' else state
  checks.append({'check_id':q['sender']+'-'+beam,'check_type':'suspension','status':state,'physical_interval':q.get('distribution',{}).get('interval_m'),'reason':'conditional characteristic maximum reaction and office distribution rules; complete node not certified','evidence':{'conditional_result':q.get('overall_result'),'original_source':'suspension_regional_review.json','diagnostics':q.get('diagnostics')},'category':'CONDITIONAL_SUSPENSION_CALCULATION_SHORTFALL' if state=='FAIL' else 'UNVERIFIED_SUSPENSION'})
 module('suspension',checks,'suspension_regional_review.json')
 diagnoses[beam]=attach_execution(consolidate(ctx,mods))
(P/'diagnostico_por_viga.json').write_text(json.dumps(diagnoses,ensure_ascii=False,indent=2),encoding='utf8')
# Source hashes for reproducibility, not proof of equivalence of project revisions.
S=Path('S:/PROJETOS EM EXECU\u00c7\u00c3O/24-212-TGD-SILVA JARDIM-POA-RS/APOIO/JO\u00c3O/TIPO');T=Path(r'C:\TQS\TGD - SILVA JARDIM\24-212-TGD-SILVA JARDIM-R35\TIPO\VIGAS')
manifest=[]
for path in sorted(S.glob('*'))+sorted(T.glob('*.LST')):
 if path.is_file() and path.suffix.lower() in ('.pdf','.lst'):
  manifest.append({'path':str(path),'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
(P/'source_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
assert set(D)=={f'V{x}' for x in range(601,630)}
assert len(r['flexure'])==333 and len(r['shear'])==66
assert len([x for x in r['suspension'] if x.get('overall_result')=='FAIL'])==3
assert all(d['selected_solution'] is None and d['detailing_optimization'] is None for d in diagnoses.values())
print('VALIDATED',len(diagnoses),'beams; sources',len(manifest))
