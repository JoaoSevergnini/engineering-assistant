from pathlib import Path
import json,copy,hashlib,shutil
R=Path(r'\\srvmaster\PUBLICO\Joao Severgnini\Simon\engineering-assistant');O=R/'analises/atp_s07_vigas_terreo/rodada_05_relatorio_global';history=O/'historico_antes_negativos_por_lado_20261016';history.mkdir(exist_ok=True)
for name in ['verificacoes_globais_concretopy.json','relatorio_global_vigas_S07.pdf','relatorio_global_vigas_S07.md','quadro_global_vigas.json','conciliacao_negativa_P785_V23_V24.json']:
 if not (history/name).exists():shutil.copy2(O/name,history/name)
p=O/'verificacoes_globais_concretopy.json';D=json.loads(p.read_text(encoding='utf8'));T=json.loads((O/'tqs_operacional_atual.json').read_text(encoding='utf8'));assert hashlib.sha256(Path(T['V1']['source']).read_bytes()).hexdigest()==D['source_model_sha256'],'TQS source changed';changes=[];allrows=[]
for x in D['results']:
 for n in x['negative']:
  old=n['governing_Mk_support_tfm'];own=n['demand']['magnitude'];before=n['scenarios'][0]['capacity_passes'];n['governing_Mk_support_tfm']=own;n['governing_Mk_own_side_tfm']=own;n['negative_demand_scope']='ONLY_OWN_SPAN_AND_OWN_END_SUPPORT_REGION';n.pop('physical_alignment_governance',None)
  # Verify archived demand is the maximum of the two original moment envelopes in this end region.
  L=x['model_length_m'];a,z=(0,x['domain']['start_model_m']) if n['end']=='left' else (x['domain']['end_model_m'],L);values=[]
  for s in T[x['model_name']]['series']:
   if s['span_token']!=x['span_token'] or not s['label'].startswith('M '):continue
   for q in [a,z]+[i*L/12 for i in range(13) if a<=i*L/12<=z]:
    u=max(0,min(12,q/L*12));i=min(int(u),11);v=s['original_values'][i]+(s['original_values'][i+1]-s['original_values'][i])*(u-i);values.append(max(0,-v))
  assert abs(max(values)-own)<1e-8,(x['beam_id'],x['span_token'],n['end'],own,max(values))
  for sc in n['scenarios']:
   c=sc['concretopy'];sc['capacity_passes']=sc['Mk_eq_tfm'] is not None and sc['Mk_eq_tfm']>=own and c['hipoteses_validas'] is True;m=c['minimum_by_actual_section'];sc['minimum_passes']=None if own==0 else m['moment_passes'] and m['area_passes']
  row={'beam':x['beam_id'],'model':x['model_name'],'span_token':x['span_token'],'end':n['end'],'support':n['support'],'previous_shared_Mk_tf_m':old,'own_side_Mk_tf_m':own,'signed_Mk_tf_m':n['demand']['signed_value'],'source':n['demand']['source'],'capacity_C35_tf_m':n['scenarios'][0]['Mk_eq_tfm'],'before_passes_C35':before,'after_passes_C35':n['scenarios'][0]['capacity_passes']};allrows.append(row)
  if abs(old-own)>1e-10:changes.append(row)
D['negative_demand_rule']={'source':'Correcao expressa de Joao em16/10/2026; exemploV43/P723','scope':'Maximo negativo na regiao de CADA extremidade do proprio intervalo; sem unificar com trecho vizinho e sem reduzir para face interna.','official_capacities':'Reutilizadas as mesmas resistencias oficiais Concretopy arquivadas, pois secoes/armaduras/materiais nao mudaram. Refeitas comparacoes com as demandas de cada lado.'};p.write_text(json.dumps(D,ensure_ascii=False,indent=2),encoding='utf8')
audit={'negative_sides_audited':len(allrows),'demand_rows_changed':len(changes),'capacity_outcomes_changed_C35':sum(r['before_passes_C35']!=r['after_passes_C35'] for r in allrows),'changes':changes,'V43_P723':[r for r in allrows if r['beam']=='V43' and r['support']=='P723'],'all_sides':allrows,'no_new_resistance_execution':True};(O/'revisao_negativos_por_lado.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf8');(O/'conciliacao_negativa_P785_V23_V24.json').write_text(json.dumps({'criterion':'Cada lado individual; substitui unificacao anterior','sides':[r for r in allrows if r['beam'] in ['V23','V24'] and r['support']=='P785']},ensure_ascii=False,indent=2),encoding='utf8')
# Correct generating routine so a later execution cannot restore cross-side maxima.
p=O/'executar_verificacoes_95.py';s=p.read_text(encoding='utf8');a=s.index('# Maximum on each physical named support');b=s.index("out={'date':",a);s=s[:a]+'''# Each end uses its own maximum negative demand. Never unify adjacent sides.
for x in results:
 for n in x['negative']:
  gov=n['demand']['magnitude'];n['governing_Mk_support_tfm']=gov;n['governing_Mk_own_side_tfm']=gov;n['negative_demand_scope']='ONLY_OWN_SPAN_AND_OWN_END_SUPPORT_REGION'
  for sc in n['scenarios']:sc['capacity_passes']=sc['Mk_eq_tfm'] is not None and sc['Mk_eq_tfm']>=gov
''' +s[b:];p.write_text(s,encoding='utf8')
p=O/'retomar_confirmacoes.py';s=p.read_text(encoding='utf8');a=s.index(" n=row.pop('entry');n['governing_Mk_support_tfm']=gov;");b=s.index('\n for s in',a);s=s[:a]+" n=row.pop('entry');gov=n['demand']['magnitude'];n['governing_Mk_support_tfm']=gov;n.pop('physical_alignment_governance',None)"+s[b:];p.write_text(s,encoding='utf8')
# Permanent presentation rule: clarify maximum belongs to the specific side.
p=R/'profile/force-presentation.md';s=p.read_text(encoding='utf8');a=s.index('## Momento negativo no apoio');s=s[:a]+'''## Momento negativo no apoio — orientações de João em15 e16/10/2026

Usar o máximo negativo fornecido pelo TQS na região de cada extremidade do próprio vão, sem reduzir/interpolar a solicitação para a face interna. Preservar sinal, envoltória, posição e fonte. Consultar as seções terminais S1/S13 e outros pontos comprovadamente dentro do apoio, selecionando o máximo daquele lado.

Em vigas contínuas, verificar separadamente os dois lados de cada apoio: fim do vão anterior e início do vão seguinte. Não substituir os dois valores pelo maior entre eles, mesmo que o pilar e a armadura sejam iguais. Associar cada demanda à seção e à armadura correspondentes ao próprio lado. Isso também se aplica à continuidade entre vigas com nomes documentais diferentes.

Exemplo confirmado por João: V43/P723, fim do trecho3: Mk=-8,697tf·m; início do trecho4: Mk=-12,707tf·m. Não repetir12,707tf·m nos dois lados. A orientação de16/10 esclarece e substitui a interpretação anterior que unificava o apoio compartilhado. Não atribuir essa escolha do engenheiro a requisito normativo não consultado.
''';p.write_text(s,encoding='utf8')
print(json.dumps({k:v for k,v in audit.items() if k not in ['changes','all_sides']},ensure_ascii=True));print('OUTCOME_CHANGES',json.dumps([r for r in allrows if r['before_passes_C35']!=r['after_passes_C35']],ensure_ascii=True))
