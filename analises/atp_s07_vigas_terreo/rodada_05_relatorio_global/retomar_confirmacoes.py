from pathlib import Path
import json,sys,copy,hashlib,datetime
R=Path(r'\\srvmaster\PUBLICO\Joao Severgnini\Simon\engineering-assistant');O=R/'analises/atp_s07_vigas_terreo/rodada_05_relatorio_global'
sys.path[:0]=[str(R/'tools/reinforcement_checks'),str(R.parent/'concretopy')]
def read(n):return json.loads((O/n).read_text(encoding='utf8'))
def save(n,v):(O/n).write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf8')
D=read('decisoes_confirmadas_2026-10-16.json')
D['latest_confirmations']={'source':'Respostas expressas de Joao, retomadas em 16/10/2026','h165_composite_stirrups':'Usar apenas os detalhes das pranchas recebidas; nao presumir detalhe complementar de fechamento/ancoragem.','V31_V41_model_origin':'Inicio do balanco coincide com eixo V12/V13; nao com face externa.','V31_V12_transfer':'V31 apoia na V12. Papel indicado como apoio no TQS esta invertido; reacao negativa corresponde a acao oposta sobre a V12, nao a levantamento nesta ligacao.','V41_V13_transfer':'Confirmacao expressa adicional: V41 apoia na V13.','V49_PC21C':'Apoio direto no bloco PC21C confirmado; nao verificar suspensao V49 sobre V26.'}
save('decisoes_confirmadas_2026-10-16.json',D)
S=read('suspensao_inventario_global.json')
for z in S:
 pair=(z['supported_beam'],z['receiving_beam'])
 if pair==('V49','V26'):
  z.setdefault('previous_beam_on_beam_assessment',copy.deepcopy(z));z['physical_classification']='DIRECT_BLOCK_SUPPORT_PC21C';z['review_status']='APOIO_DIRETO_SEM_SUSPENSAO';z['suspension_applicable']=False;z['reason']='Joao confirmou apoio direto da V49 no bloco PC21C (70x70cm, NB8,68m no fundo da V49). Rotulo V26 da reacao TQS preservado somente como origem do modelo; nao caracteriza apoio indireto fisico.';z.pop('calculation',None)
 if pair in [('V12','V31'),('V13','V41')]:
  z.setdefault('previous_model_role_assessment',copy.deepcopy(z));old=copy.deepcopy(z)
  z['supported_beam'],z['receiving_beam']=pair[1],pair[0]
  lo,hi=old['reaction_min_kn'],old['reaction_max_kn'];z['reaction_min_kn'],z['reaction_max_kn']=-hi,-lo
  z['reaction_min_tf'],z['reaction_max_tf']=(-hi/9.80665,-lo/9.80665)
  z['uplift_envelope']=False;z['physical_classification']='REVERSED_MODEL_REACTION_ACTION_REACTION';z['review_status']='PENDENTE_CALCULO_RECEPTORA' if pair[0]=='V12' else 'PENDENTE_CONFIRMACAO_SENTIDO';z['reason']='V31 descarrega na V12, conforme confirmacao de Joao. Reacao originalmente negativa na V12 foi invertida por acao-reacao; verificar suspensao na V12.' if pair[0]=='V12' else 'Sentido V41 sobre V13 interpretado pela simetria e pelo mesmo sinal negativo, mantendo confirmacao especifica pendente; nao classificar como levantamento.';z['role_source']='Resposta de Joao' if pair[0]=='V12' else 'Interpretacao por simetria da resposta; confirmar';z.pop('calculation',None)
save('suspensao_inventario_global.json',S)
# Preserve source forces and audit demand on the same physical alignment V23/V24 at P785.
T=read('tqs_operacional_atual.json');C=read('verificacoes_globais_concretopy.json');rows=[]
for x in C['results']:
 if x['beam_id'] in ['V23','V24']:
  for n in x['negative']:
   if n['support']=='P785':
    end=0 if n['end']=='left' else -1
    candidates=[{'magnitude':max(0,-s['original_values'][end]),'signed_tf_m':s['original_values'][end],'source':s['source'],'sample':1 if end==0 else 13} for s in T[x['model_name']]['series'] if s['span_token']==x['span_token'] and s['label'].startswith('M ')]
    rows.append({'beam_id':x['beam_id'],'model_name':x['model_name'],'span_token':x['span_token'],'end':n['end'],'terminal_candidates':candidates,'old_governing_Mk':n['governing_Mk_support_tfm'],'entry':n})
gov=max(v['magnitude'] for row in rows for v in row['terminal_candidates'])
for row in rows:
 n=row.pop('entry');gov=n['demand']['magnitude'];n['governing_Mk_support_tfm']=gov;n.pop('physical_alignment_governance',None)
 for s in n['scenarios']:s['capacity_passes']=s['Mk_eq_tfm']>=gov and s['concretopy']['hipoteses_validas'] is True
 row['new_governing_Mk']=gov;row['capacity_C35']=n['scenarios'][0]['Mk_eq_tfm'];row['passes_C35']=n['scenarios'][0]['capacity_passes']
save('conciliacao_negativa_P785_V23_V24.json',rows);save('verificacoes_globais_concretopy.json',C)
print(json.dumps({'recorded_decisions':True,'P785':rows,'changed_connections':[{'pair':z['supported_beam']+'->'+z['receiving_beam'],'Rmax_tf':z['reaction_max_tf'],'status':z['review_status']} for z in S if z['supported_beam'] in ['V31','V41','V49']]},ensure_ascii=True))
