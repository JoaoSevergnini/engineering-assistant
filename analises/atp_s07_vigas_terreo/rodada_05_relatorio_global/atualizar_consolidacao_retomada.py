from pathlib import Path
O=Path(r'\\srvmaster\PUBLICO\Joao Severgnini\Simon\engineering-assistant\analises\atp_s07_vigas_terreo\rodada_05_relatorio_global');p=O/'consolidar_relatorio.py';s=p.read_text(encoding='utf8')
s=s.replace("variable={'V23','V24','V42','V49','V50'}",'variable=set() # nominal peak/support sections identified; internal transitions separately qualified')
a=s.index('# Avoid promoting provisional');s=s[:a]+'''# Updated conclusions after confirmed physical transfers and regional checks.
custom.update({
'V12':'V31 descarrega na V12, confirmado por Joao. Rk=24,46tf obtido por acao-reacao da listagem. Suspensao numerica atende com75% na V12 e25% na V31; estribos compostos138/50cm permanecem sujeitos a verificacao de funcionamento conjunto.',
'V13':'V41 descarrega na V13, confirmado por Joao. Rk=30,52tf. Distribuicao uniforme75/25 nao atende a soma com cortante regional; nao equivale a demonstracao de impossibilidade de outra distribuicao admissivel. Ver valores na secao de ligacoes.',
'V22':'Adotados2Ø12,5 deN1; elevacao indica2Ø16. Suspensao daV21 avaliada em25cm unilaterais;75% atende, mas quantidade efetiva/reparticao do tirante integral ainda nao comprovada.',
'V23':'Secoes nominais no pico e nos apoios identificadas para flexao; transicoes internas mantidas separadamente. NoP785, adotar12,997tf.m dos dois lados do mesmo alinhamentoV23/V24. Capacidade4Ø16 emh50=10,780tf.m, insuficiente.',
'V24':'Primeiro intervalo fisicoP785-P778=modeloV23/3; demais=modeloV24. NoP778 adotados4Ø16 N16, nao2Ø10 porta-estriboN18: capacidade10,780tf.m supera8,565tf.m. NoP785 a demanda compartilhada e12,997tf.m. NoP778-P769 positiva3,995tf.m supera3,452tf.m de2Ø12,5 emh50.',
'V26':'Rotulos de apoios no detalhe divergem da forma; identidade fisica adotada. Suspensao deV26 naV25 atende100% do tirante. V49 tem apoio direto confirmado no blocoPC21C, excluido da suspensao emV26.',
'V31':'Inicio1B no eixoV12, confirmado porJoao. V31 descarrega emV12. CruzamentosV9/V7 a2,325/3,545m; faceP746 a5,275m e faixa515cm conciliadas. SuspensoesV7/V9 com diagrama regional atendem numericamente; funcionamento das pecas compostas pendente.',
'V34':'FaixasN7:quatro ramos6,3c10 em115cm e c20 em334cm;N1:quatro ramos8c10 em167cm. CruzamentoV50 a4,89m desdeP760.75% atende por taxa, mas depende de comprovar tres estribos na regiao50cm e a parcela complementar naV50.',
'V41':'Inicio1B no eixoV13, confirmado porJoao. V41 descarrega emV13. CruzamentosV10/V8 a2,325/3,545m; faceP744 a5,590m e faixa547cm conciliadas. Soma conservadora dos dois tirantes e cortante regional atende3,667cm2/m existentes; suspensao emV13 tratada separadamente.',
'V49':'Mudanca50/87cm localizada pela cota130cm: xTQS=1,465m. Positiva nao atende emh50 e atende emh87; ver tabela regional. Apoio direto no blocoPC21C confirmado. Estribos externos6,3c10; pecas da primeira etapa excluidas.',
'V50':'Mudanca50/87cm localizada pela cota130cm: xTQS=3,005m. Positiva nao atende emh50 e atende emh87; ver tabela regional. Estribos externos6,3c10; pecas da primeira etapa excluidas. Suspensao naV34 depende da quantidade local de estribos e complemento naV50.'})

''' +s[a:]
s=s.replace("pf=[x for x in xs if x['positive']['scenarios'][0]['capacity_passes'] is False]", "pf=[x for x in xs if x['positive'].get('regional_capacity_passes',x['positive']['scenarios'][0]['capacity_passes']) is False]")
s=s.replace("any(z['review_status']=='INSUFICIENTE' for z in conn)","any(z['review_status'] in ['INSUFICIENTE','NAO_ATENDE_DISTRIBUICAO_UNIFORME'] for z in conn)")
s=s.replace("('PENDENTE NAS LIGAÇÕES' if conn else 'SEM LIGAÇÃO NO INVENTÁRIO')", "('ATENDE LIGAÇÕES' if conn and all(z['review_status'] in ['ATENDE','APOIO_DIRETO_SEM_SUSPENSAO'] for z in conn) else 'PENDENTE NAS LIGAÇÕES' if conn else 'SEM LIGAÇÃO NO INVENTÁRIO')")
s=s.replace('As indicações desfavoráveis deV24,V49,V50 permanecem condicionadas à posição/altura local da seção e não foram emitidas como reprovação definitiva da viga inteira.','Tambem insuficientesV24(P778-P769),V49 eV50 nos trechos de50cm. As mudancas de altura deV49/V50 foram localizadas pela cota130cm; os trechos87cm atendem. Total:oito vigas com pelo menos uma secao positiva insuficiente.')
s=s.replace('Há seis interfaces com envoltória ascendente, incluindoV12/V13, além das quatro usuais anteriormente relacionadas.','Nas ligacoesV31-V12 eV41-V13 o sentido foi corrigido por confirmacao deJoao. As outras quatro interfaces com sinal negativo exigem distinguir levantamento de inversao do papel indicado pelo modelo; pergunta encaminhada ao engenheiro. V49 apoia diretamente noPC21C e nao exige suspensao emV26.')
s=s.replace('Sinal da reação:positivo descendente, negativo ascendente.', 'Sinal da reacao:positiva descendente conforme o papel fisico validado. NasV31-V12 eV41-V13 os valores apresentados sao os opostos das reacoes originalmente negativas na listagemTQS, por acao-reacao confirmada porJoao. Nas outras quatro interfaces de sinal negativo, o sentido fisico ainda exige validacao.')
# Include the combined checks for the two new receiving beams and overlaps.
a=s.index("title('6. Fichas de verificação')")
s=s[:a]+'''for z in json.loads((O/'suspensao_sobreposicoes_V31_V41.json').read_text(encoding='utf8')):
 para(z['receiving_beam']+':soma conservadora dos dois tirantes e cortante regional='+n(z['total_required_cm2_m'])+'cm²/m;fornecida='+n(z['provided_cm2_m'])+'cm²/m. Area atende; eficacia das pecas compostas permanece separada.')
for z in json.loads((O/'suspensao_V31_V12_V41_V13.json').read_text(encoding='utf8')):
 r=z['result'];part=z['supported_25_percent'];para(z['connection']['supported_beam_id']+'→'+z['connection']['receiving_beam_id']+':distribuicao uniforme75/25. Receptora:exigida='+n(r['asw_per_s_total_required'])+'cm²/m;existente='+n(z['full_transfer']['provided_cm2_m'])+'cm²/m. Apoiada:exigida='+n(part['required_rate_cm2_m'])+'cm²/m;existente='+n(part['provided_rate_cm2_m'])+'cm²/m. Cortantes regionais e parcelas calculadas peloConcretopy; pecas compostas condicionam o resultado. A falha desta distribuicao uniforme nao esgota outras distribuicoes admissiveis.')

''' +s[a:]
a=s.index(" para('**Flexão negativa -")
s=s[:a]+''' if bid in ['V49','V50']:
  regional=next(q for q in json.loads((O/'geometria_e_flexao_regional_V49_V50.json').read_text(encoding='utf8')) if q['beam']==bid)
  para('**Flexao positiva regional - conclusao aplicavel as alturas reais.**')
  table(['h(cm)','Intervalo modelo(m)','d(cm)','Mk(tf·m)','MRd/γf(tf·m)','Resultado'],[[n(q['h_cm'],0),n(q['interval_model_m'][0],3)+'-'+n(q['interval_model_m'][1],3),n(q['concretopy']['d_equivalente_cm']),n(q['demand']['Mk_tfm']),n(q['concretopy']['mrd_kncm']/100/1.4/9.80665),result(q['capacity_passes'])] for q in regional['positive_regions']])
  para('Origem:Concretopy; geometria_e_flexao_regional_V49_V50.json. Cota130cm medida da mudanca de altura ate a face interna do pilar direito. Fundo continuo; nao e degrau de fundo. A tabela regional prevalece sobre a comparacao nominal unica acima.')
''' +s[a:]
# Replace low-position-confidence demand by the documented whole-interval conservative PASS bound.
a=s.index("   rows.append([x['span_token'],n(q['start_model_m'])",s.index("para('**Cortante"));b=s.index('\n table(',a)
s=s[:a]+'''   proof=q.get('whole_model_interval_upper_demand_check');interval_label=n(q['start_model_m'])+'–'+n(q['end_model_m']);required=s['adopted_requirement_cm2_m'];passed=s['adopted_area_passes']
   if not x['domain']['physical_block_faces_proved'] and not ad and proof and proof['passes']:
    v=proof['force_bound']['Vk_tf'];required=proof['required_cm2_m'];passed=proof['passes'];diag=proof['concretopy']['diagonal_compression']['passes'];interval_label='INTERVALO TQS INTEIRO (LIMITE)'
   rows.append([x['span_token'],interval_label,str(q['legs'])+'r Ø'+n(q['diameter_mm'],1)+'c/'+n(q['spacing_cm'],0),n(q['depth_selection']['d_cm']),n(v),n(q['provided_cm2_m']),n(required),result(passed),'L:'+result(s['longitudinal_max_spacing_passes'])+' / T:'+result(s['transverse_max_spacing_passes']),result(diag)])''' +s[b:]
s=s.replace("para('Passagem geométrica do vibrador4cm:'", "para('INTERVALO TQS INTEIRO (LIMITE):maior|Vk| de todas as13secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.')\n para('Passagem geométrica do vibrador4cm:'")
s=s.replace("['V23/V24/V42/V49/V50','Posicionar mudanças de seção, níveis e composições nos trechos físicos e consultar os esforços correspondentes','Associação geométrica não encerrada; divergência específicah110 daV42 registrada']", "['V23/V24/V42','Concluir transicoes internas; secoes nominais dos picos e apoios ja identificadas. V49/V50 encerradas quanto a posicao das mudancas50/87cm','Associacao de transicoes nao encerrada; divergenciah110 daV42 mantida']")
s=s.replace("['V31/V41 e encontros na extremidade','Associar a origem física do balanço e distinguir cruzamento interior de extremidade','Referência do modelo ainda não comprovada pela forma']", "['V31/V41 sobreV12/V13','Sentido e eixos confirmados; concluir eventual distribuicao alternativa na ligacaoV41-V13 e eficacia dos estribos compostos','Distribuicao uniforme75/25 nao atendeV41-V13; nao e falta de confirmacao do apoio']")
s=s.replace('; condições para d/2 confirmadas nos dois locais.', '; condições para d/2 confirmadas nos dois locais; V31 apoiaV12; V41 apoiaV13; inicio1B no eixo; V49 direto no blocoPC21C; estribos compostos avaliados apenas pelas pranchas recebidas.')
s=s.replace('Emissão:16/10/2026. Abrangência:', 'Emissão:16/10/2026 - revisao de retomada. Abrangência:')
p.write_text(s,encoding='utf8')
print('COMPILER_UPDATED')
