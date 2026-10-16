from pathlib import Path
import json,sys,hashlib,copy,html,collections
R=Path(r'\\srvmaster\PUBLICO\Joao Severgnini\Simon\engineering-assistant');B=R/'analises/atp_s07_vigas_terreo';O=B/'rodada_05_relatorio_global'
sys.path[:0]=[str(R/'tools/reinforcement_checks'),str(R/'tools/beam_model'),str(R.parent/'concretopy')]
D=json.loads((O/'verificacoes_globais_concretopy.json').read_text(encoding='utf8'));A=json.loads((O/'entradas_vigas_50.json').read_text(encoding='utf8'));M=json.loads((B/'rodada_02_modelo_atualizado/matriz_vigas.json').read_text(encoding='utf8'));S=json.loads((O/'suspensao_inventario_global.json').read_text(encoding='utf8'));F=json.loads((O/'inventario_fontes_atual.json').read_text(encoding='utf8'))
by={f'V{i}':[x for x in D['results'] if x['beam_id']==f'V{i}'] for i in range(1,51)}
# Mandatory floor-level guard. Missing physical evidence stays unresolved. Section calls are separate archives, not invented PASS inputs.
from floor_review import review_floor
spec=json.loads((B/'rodada_03_controles_locais/manifesto_pavimento.json').read_text(encoding='utf8'))
for k in ['form','detailing']:
 src=spec['sources'][k];src['sha256']=hashlib.sha256(Path(src['path']).read_bytes()).hexdigest()
spec['sources']['tqs']['sha256']=D['source_model_sha256']
for c in spec['beams']:
 if 'context' in c:c['context']['fck_mpa']=35
 c['jobs']=[{'id':c['beam_id']+'-'+ctrl+'-global05','control':ctrl,'interval_m':c['review_interval_m'],'interval_role':c.get('interval_role','PLANNING_NOT_GEOMETRIC_PROOF'),'inputs':{},'external_section_results':str(O/'verificacoes_globais_concretopy.json')} for ctrl in ['positive_flexure','negative_flexure','shear','suspension']]
(O/'manifesto_integracao_global.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2),encoding='utf8')
res=review_floor(spec,api=None)
compact={'scope':'Auditoria de integracao fisica; nao substitui calculos oficiais de secao arquivados; dados ausentes nao foram preenchidos por hipoteses','floor_approval':res.get('floor_approval'),'overall_status':res.get('overall_status'),'beams':[{'beam_id':b['beam_id'],'controls':[{k:c.get(k) for k in ['job_id','control','status','execution_state','missing_inputs','diagnostics']} for c in b['controls']],'diagnosis':b.get('diagnosis')} for b in res['beams']]}
(O/'auditoria_floor_review.json').write_text(json.dumps(compact,ensure_ascii=False,indent=2),encoding='utf8')

def n(x,d=2):return '-' if x is None else f'{x:.{d}f}'.replace('.',',')
def steel(c):return f"{c['count']}Ø{n(c['phi'],1).replace(',0','')}"+(' / camadas '+str(c['layers']) if len(c['layers'])>1 else '')
def result(v):return 'ATENDE' if v is True else 'NÃO ATENDE' if v is False else 'NÃO CONCLUÍDO'
def valid(sc):return sc['concretopy'].get('hipoteses_validas') is True
variable=set() # nominal peak/support sections identified; internal transitions separately qualified
custom={
'V3':'Adotados 4Ø16 de N1/corte; elevação indica 2Ø20. Barras superiores da primeira concretagem excluídas. Conferir funcionamento conjunto dos estribos de138/50cm na altura final165cm.',
'V6':'Adotados 4Ø16 de N1/corte; elevação indica 2Ø20. Conferir funcionamento conjunto dos estribos de138/50cm na altura final165cm.',
'V7':'O detalhe comum V7-V10 cita apoiosV22/V26; a forma posiciona V7 em V29/V31. Usada a identidade física da forma. Estribos138/50cm exigem comprovar funcionamento conjunto.',
'V8':'Detalhe comum cita apoiosV22/V26; forma posiciona V8 emV39/V41. Estribos138/50cm exigem comprovar funcionamento conjunto.',
'V9':'Detalhe comum cita apoiosV22/V26; forma posiciona V9 emV29/V31. Estribos138/50cm exigem comprovar funcionamento conjunto.',
'V10':'Detalhe comum cita apoiosV22/V26; forma posiciona V10 emV39/V41. Estribos138/50cm exigem comprovar funcionamento conjunto.',
'V12':'Cálculo convencional solicitado por João; sem critérios próprios de viga-parede. Barras intermediárias N3 não consideradas. A reação no encontroV31 é ascendente em ambas as envoltórias; requer ligação para levantamento.',
'V13':'Cálculo convencional solicitado por João; sem critérios próprios de viga-parede. Barras intermediárias N3 não consideradas. A reação no encontroV41 é ascendente em ambas as envoltórias; requer ligação para levantamento.',
'V15':'NB8,38m deP756/P761 confirmado. Fundo da viga8,68m: nesses apoios usar faces dos pilares; nos demais, faces dos blocos que interceptam a viga. Cortante atende nas quatro faixas/vãos calculados. Falhas negativas são independentes desse atendimento.',
'V17':'Transição entre quatro ramosØ8c/17 (3225cm) e c/10 (1535cm) ainda sem abscissa física integral comprovada. Trecho5 consultado conservadoramente com c/17; trecho6 com c/10. Não há reprovação gerada por essa aproximação.',
'V18':'Adotados3Ø16 deN5 no PC46C; elevação indica2Ø20. Estribos originais2ramosØ6,3c/15 nos dois vãos. Anotações sobrepostas são propostas e não entram no existente.',
'V19':'Positiva pelas marcas:N3 2Ø16 +N4 1Ø16=3Ø16; elevação indica4Ø12,5. Suspensão daV33 não atendida.',
'V20':'Positiva pelas marcas:N3 2Ø16 +N4 1Ø16=3Ø16; elevação indica4Ø12,5. Suspensão daV40 não atendida.',
'V21':'PC56C/PC57C:adotados5Ø20 deN5+N6; elevação indica4Ø20. Estribos originaisØ8c/17 nos quatro primeiros vãos;Ø6,3c/15 nos dois últimos. Consulta a d/2 noPC55C autorizada após confirmação das cargas superiores e reação inferior. Face dePC54C no extremo esquerdo ainda não comprovada integralmente.',
'V22':'Adotados2Ø12,5 deN1; elevação indica2Ø16. Receptora curva: a projeção do encontroV21 requer abscissa física no trecho curvo.',
'V23':'Seções variáveis. Armaduras calculadas conforme detalhamento, mas a posição das mudanças de altura e a correspondência dos apoios precisam ser concluídas antes da conclusão regional definitiva.',
'V24':'Primeiro vão físico P785-P778 corresponde ao trecho3 do modeloV23; demais trechos no modeloV24. Não associar apenas pelo nome. Mudanças de seção e barras escalonadas exigem posicionamento no eixo físico.',
'V26':'Nomes dos apoios no detalhe divergem da forma. Conferir a identidade e os níveis no trecho curvo antes de concluir suspensão emV25 ou daV49.',
'V29':'Somente2Ø10 finais considerados no topo;3Ø16 intermediários excluídos. Positiva3Ø20 em duas camadas[2,1]. Conferir ancoragem e funcionamento conjunto dos estribos138/50cm.',
'V31':'1B e2 são subdivisões do modelo junto ao mesmo P746, não dois vãos físicos. Origem física do balanço ainda não reconciliada. Somente2Ø10 finais no topo;3Ø16 intermediários excluídos.',
'V33':'Faixa129cm termina no blocoP794. Retirado o antigo déficit até a face do pilar. Cortante atende; negativaP794 e suspensão naV19 são controles distintos.',
'V34':'Faixas originais:N7 quatro ramosØ6,3c/10 em115cm e c/20 em334cm;N1 quatro ramosØ8c/10 em167cm. Domínio entre blocosP760/P747. Suspensão daV50 exige posição do encontro dentro dessas faixas.',
'V35':'Duas faixasN11 de2ramosØ6,3c/15. Cortante insuficiente nos dois intervalos; estribos menores da primeira etapa não foram somados. Reação naV15 alterna de descendente a ascendente.',
'V36':'EmC35,2ramosØ6,3c/15 atendem ao cortante calculado. Não transportar o pequeno déficit de mínimo do cenárioC40 para o resultado principalC35. Reação no encontroV5 é ascendente.',
'V37':'N7:2ramosØ6,3c/15 em418cm;N1:2ramosØ8c/15 em135cm. Cortante atende com d/2 noP725, confirmado porJoão. Positiva e negativas mantêm verificações próprias.',
'V39':'Mesmo desenho daV29. Positiva3Ø20 em camadas[2,1]. Somente2Ø10 finais no topo. Conferir funcionamento dos estribos138/50cm.',
'V40':'Faixa129cm termina no blocoP796. Correção anotada para apoioV20 já aceita; desenho-base citaV19. Cortante atende; negativaP796 e suspensão naV20 mantêm apontamentos próprios.',
'V41':'1B e2 são subdivisões numéricas junto aoP744. Origem física do balanço ainda não reconciliada. Somente2Ø10 finais no topo; barras da primeira etapa excluídas.',
'V42':'Há indicaçãoh110 no trecho do detalhamento contra rótulosh80/h50 na forma. Usadas seções do detalhamento conforme autorização; divergência forma-detalhe mantida. P791 está a+8,88m. Falta localizar todas as transições de altura no eixo físico.',
'V47':'Usada a interseção do eixo inclinado com os contornos dos blocosP751/P741 da7201. Cortante atende; o antigo máximo dentro do bloco não governa a faixa livre.',
'V48':'Domínio pelos blocosP767/P758. Diferença de cerca6,3cm entre soma da faixa e distância vetorial exige conferir a referência das pontas; não comprova falta de estribos. EmC35, o cortante calculado atende.',
'V49':'Alturas finais50/87cm; a cota130 é comprimento, não altura. N4/N5:Ø6,3c/10;N7c/20 é da primeira etapa e não foi somado. Positiva3Ø12,5 inferior; barras da primeira etapa excluídas. Conclusão da positiva depende da posição exata da mudança de altura.',
'V50':'Alturas finais50/87cm. N4/N5:Ø6,3c/10;N7c/20 é da primeira etapa. Positiva2Ø16 inferior. Verificação regional depende da posição exata da mudança de altura; não tomar a capacidadeh50 como capacidade de toda a viga.'}

# Updated conclusions after confirmed physical transfers and regional checks.
custom.update({
'V12':'V31 descarrega na V12, confirmado por Joao. Rk=24,46tf obtido por acao-reacao da listagem. Suspensao numerica atende com75% na V12 e25% na V31; estribos compostos138/50cm permanecem sujeitos a verificacao de funcionamento conjunto.',
'V13':'V41 descarrega na V13, confirmado por Joao. Rk=30,52tf. Distribuicao uniforme75/25 nao atende a soma com cortante regional; nao equivale a demonstracao de impossibilidade de outra distribuicao admissivel. Ver valores na secao de ligacoes.',
'V22':'Adotados2Ø12,5 deN1; elevacao indica2Ø16. Suspensao daV21 avaliada em25cm unilaterais;75% atende, mas quantidade efetiva/reparticao do tirante integral ainda nao comprovada.',
'V23':'Secoes nominais no pico e nos apoios identificadas para flexao; transicoes internas mantidas separadamente. NoP785, o ladoV23 usa12,997tf.m e o ladoV24 usa11,640tf.m; verificar separadamente. Capacidade4Ø16 emh50=10,780tf.m, insuficiente.',
'V24':'Primeiro intervalo fisicoP785-P778=modeloV23/3; demais=modeloV24. NoP778 adotados4Ø16 N16, nao2Ø10 porta-estriboN18: capacidade10,780tf.m supera8,565tf.m. NoP785, este ladoV24 usa11,640tf.m; o ladoV23 usa12,997tf.m, sem unificar as verificacoes. NoP778-P769 positiva3,995tf.m supera3,452tf.m de2Ø12,5 emh50.',
'V26':'Rotulos de apoios no detalhe divergem da forma; identidade fisica adotada. Suspensao deV26 naV25 atende100% do tirante. V49 tem apoio direto confirmado no blocoPC21C, excluido da suspensao emV26.',
'V31':'Inicio1B no eixoV12, confirmado porJoao. V31 descarrega emV12. CruzamentosV9/V7 a2,325/3,545m; faceP746 a5,275m e faixa515cm conciliadas. SuspensoesV7/V9 com diagrama regional atendem numericamente; funcionamento das pecas compostas pendente.',
'V34':'FaixasN7:quatro ramos6,3c10 em115cm e c20 em334cm;N1:quatro ramos8c10 em167cm. CruzamentoV50 a4,89m desdeP760.75% atende por taxa, mas depende de comprovar tres estribos na regiao50cm e a parcela complementar naV50.',
'V41':'Inicio1B no eixoV13, confirmado porJoao. V41 descarrega emV13. CruzamentosV10/V8 a2,325/3,545m; faceP744 a5,590m e faixa547cm conciliadas. Soma conservadora dos dois tirantes e cortante regional atende3,667cm2/m existentes; suspensao emV13 tratada separadamente.',
'V49':'Mudanca50/87cm localizada pela cota130cm: xTQS=1,465m. Positiva nao atende emh50 e atende emh87; ver tabela regional. Apoio direto no blocoPC21C confirmado. Estribos externos6,3c10; pecas da primeira etapa excluidas.',
'V50':'Mudanca50/87cm localizada pela cota130cm: xTQS=3,005m. Positiva nao atende emh50 e atende emh87; ver tabela regional. Estribos externos6,3c10; pecas da primeira etapa excluidas. Suspensao naV34 depende da quantidade local de estribos e complemento naV50.'})

custom.update({'V17':custom['V17']+' Sentido das interfacesV23/V42 depende do caso gravidade/vento; analise separada deJoao.', 'V35':'Duas faixasN11 de2ramos6,3c15. Cortante insuficiente nos dois intervalos. Sentido da ligacao comV15 depende do caso gravidade/vento; pendente paraJoao. Nao concluir levantamento pela envoltoria total.', 'V36':'EmC35,2ramos6,3c15 atendem ao cortante. Sentido da ligacao comV5 depende do caso gravidade/vento; pendente paraJoao. Nao concluir levantamento apenas pelo sinal negativo da listagem.'})
STATUS_S={'PENDENTE_DETALHAMENTO':'AREA ATENDE; FECHAMENTO DOS ESTRIBOS A VERIFICAR','ATENDE':'ATENDE','INSUFICIENTE':'INSUFICIENTE','PENDENTE_REPARTICAO_TIRANTE':'TIRANTE INTEGRAL A COMPROVAR','NAO_ATENDE_DISTRIBUICAO_UNIFORME':'DISTRIBUICAO UNIFORME NAO ATENDE','APOIO_DIRETO_SEM_SUSPENSAO':'APOIO DIRETO PC21C; SUSPENSAO NAO SE APLICA','ANALISE_SEPARADA_JOAO':'SENTIDO DA TRANSFERENCIA:ANALISE DE JOAO'}
def sstatus(z):return STATUS_S.get(z['review_status'],z['review_status'].replace('_',' '))

def support_label(bid,name):return 'PC21C (TQS:V26)' if bid=='V49' and name=='V26' else name

def geometry_status(bid,xs):
 if bid=='V42':return 'DIVERGENCIA DE ALTURA; TRANSICOES A CONCLUIR'
 if bid in ['V49','V50']:return 'VAO E MUDANCA50/87cm LOCALIZADOS'
 if bid in ['V31','V41']:return 'EIXOS DOS CRUZAMENTOS E FAIXAS CONCILIADOS'
 if bid in ['V12','V13']:return 'FAIXA171cm COERENTE COM152cm+19cm DA FORMA'
 if all(x['domain']['physical_block_faces_proved'] for x in xs):return 'FACES E FAIXAS CONCILIADAS; VER NOTAS DE COMPRIMENTO'
 return 'SECOES NOMINAIS CONFERIDAS; COTAS DE VAOS A CONCLUIR'

# Avoid promoting provisional span comparisons or geometry approximations to project failures.
summary=[]
for bid,xs in by.items():
 pf=[x for x in xs if x['positive'].get('regional_capacity_passes',x['positive']['scenarios'][0]['capacity_passes']) is False]
 nf=[(x,q) for x in xs for q in x['negative'] if q['scenarios'][0]['capacity_passes'] is False]
 mn=[q for x in xs for q in x['negative'] if q['scenarios'][0]['minimum_passes'] is False]
 sf=[(x,q) for x in xs for q in x['shear'] if q['scenarios'][0]['adopted_area_passes'] is False]
 conn=[z for z in S if bid in [z['supported_beam'],z['receiving_beam']]]
 summary.append({'beam_id':bid,'interval_count':len(xs),'geometry':geometry_status(bid,xs),'positive':'DEPENDE DA GEOMETRIA' if bid in variable else ('SEM MOMENTO POSITIVO' if all(x['positive']['demand']['magnitude']==0 for x in xs) else ('INSUFICIENTE' if pf else 'ATENDE SEÇÃO')),'negative':'DEPENDE DA GEOMETRIA' if bid in variable else ('INSUFICIENTE' if nf else 'ATENDE SEÇÃO'),'minimum':'DEPENDE DA GEOMETRIA' if bid in variable else ('REVER MÍNIMO' if mn else 'ATENDE NAS SEÇÕES SOLICITADAS'),'shear':'INSUFICIENTE' if sf else ('ATENDE CÁLCULO; GEOMETRIA PENDENTE' if any(not x['domain']['physical_block_faces_proved'] for x in xs) else 'ATENDE FAIXAS CALCULADAS'),'suspension':'NÃO ATENDE' if any(z['review_status'] in ['INSUFICIENTE','NAO_ATENDE_DISTRIBUICAO_UNIFORME'] for z in conn) else ('ATENDE LIGAÇÕES' if conn and all(z['review_status'] in ['ATENDE','APOIO_DIRETO_SEM_SUSPENSAO'] for z in conn) else 'PENDENTE NAS LIGAÇÕES' if conn else 'SEM LIGAÇÃO NO INVENTÁRIO'),'global_approval':None})

lines=[]
def para(s=''):lines.append(s+'\n')
def title(s,level=2):para('#'*level+' '+s)
def table(head,rows):
 lines.append('| '+' | '.join(head)+' |');lines.append('| '+' | '.join(['---']*len(head))+' |')
 for row in rows:lines.append('| '+' | '.join(str(x).replace('|','/') for x in row)+' |')
 para()
title('ATP S07 - Vigas do térreo - Relatório global de verificações',1)
para('Emissão:16/10/2026 - correcao dos negativos por lado. Abrangência:V1 aV50. Resultado principal:C35 uniforme na seção final, por simplificação confirmada porJoão. ElementosPAR excluídos.')
para('Este relatório apresenta os cálculos de seção e as verificações físicas efetivamente executadas. Não representa aprovação global das50vigas. A conferência integral das cotas de todos os vãos e das regiões de seção variável ainda não foi encerrada. Esses itens são trabalhos de leitura/associação do assistente, e não informações que se demonstrou estarem ausentes no projeto.')
title('1. Critérios adotados')
para('Norma:ABNT NBR6118:2023, exemplar disponibilizado em DOCUMENTACAO ATP. Consultados os itens17.3.5.2.1 (mínimos longitudinais),17.4.1.2.1 (consulta de cortante junto ao apoio direto),17.4.2 (cortante) e18.3.6 (suspensão). Não foram aplicados critérios internos do escritório como causa de reprovação.')
para('Solicitações características emtf e tf·m. Resistência equivalente para comparação:MRd/γf, expressa emtf·m; não é resistência característica da seção. Mantidosγf=1,4,γc=1,4 eγs=1,15 neste modelo. Conversão:1tf=9,80665kN. Armaduras emcm² ecm²/m; dimensões emcm, salvo indicação.')
para('Motor oficial:Concretopy, funçãoverificar_flexao_viga_retangular para flexão e API pública de cortante por meio dedesign_shear. O arquivo verificacoes_globais_concretopy.json preserva entradas, coeficientes, saídas brutas e fonte dos esforços. Suspensão:suspension_review.review_connection, com tensão de aço e parcela de cortante fornecidas peloConcretopy. A combinação conservadora das sobreposiçõesV29/V39 é identificada como pós-processamento dos resultados, sem nova resistência independente.')
para('Cobrimento3,5cm; agregado16mm; vibrador4cm. Consideradas somente as armaduras externas inferior/superior da seção final. Barras no topo da primeira concretagem excluídas de resistência e de d. Na positiva não foi considerada contribuição da armadura superior. d resulta das camadas e do centroide retornado peloConcretopy. Na negativa, selecionado o maximo de CADA lado do apoio, no proprio trecho. Fim do vao anterior e inicio do seguinte usam solicitacoes e armaduras proprias, mesmo no mesmo pilar. Sem unificar os valores e sem reducao para a face interna.')
para('Nos conflitos elevação versus marcas/cortes, adotadas marcas/cortes conforme confirmação deJoão; divergências registradas. Anotações nosPDFs são propostas de correção e não substituem o desenho original. V3,V6,V7-V10,V12,V13 incluídas no cálculo convencional de viga, sem avaliação dos critérios próprios de viga-parede. Esse recorte não valida o comportamento especial desses elementos.')
title('2. Documentos e cobertura')
table(['Documento','Revisão/função'],[['7201','R03 - blocos, dimensões, posição dos pilares e níveisNB'],['7202','R03 - forma térreo,parte1'],['7214','R01 - forma térreo,parte2; região verde+8,88m'],['7401','R00 - detalhamentoV1-V20'],['7402','R00 - detalhamentoV21-V32 eV39'],['7403','R01 - detalhamentoV33-V38 eV40-V50'],['7404','ElementosPAR; fora do escopo'],['VGESFS/RELDTVGS','Modelo atualizado;66registros/605séries conferidas, sem diferença numérica entre listagens']])
para('Inventário nominal:V1-V50 presentes nas formas e no detalhamento. Calculados95intervalos do modelo,190consultas negativas e102faixas de cortante. Esses intervalos não equivalem automaticamente a95vãos físicos;V31/V41 têm subdivisões junto ao mesmo apoio eV43 possui balanço. Foram conciliados23domínios completos de faixa com faces de blocos/pilares, além da facePC55C no primeiro trecho daV21; os demais conservam a referência do modelo e não encerram a verificação física da faixa.')
para('Os máximos positivos de cada intervalo foram comparados à composição indicada no ponto crítico. Essa comparação não verifica automaticamente todas as interrupções de barras. Escalonamento, ancoragem, torção e estados de serviço não integram esta emissão limitada aos controles solicitados.')
para('Cotas confirmadas:P791+8,88m;V49 com topo local+9,55m quando indicado; não aplicar correção única de nível a todo o pavimento. P756/P761:NB8,38m correto; naV15 o fundo8,68m fica acima dos blocos. O nome2aFASE identifica etapa doATP, não etapa de carregamento ou concretagem.')
title('3. Resultados que exigem atenção')
para('Flexão positiva insuficiente nas seções deV16,V21(primeiro intervalo),V25(P727-P708),V35(primeiro intervalo) eV37. Tambem insuficientesV24(P778-P769),V49 eV50 nos trechos de50cm. As mudancas de altura deV49/V50 foram localizadas pela cota130cm; os trechos87cm atendem. Total:oito vigas com pelo menos uma secao positiva insuficiente.')
para('Cortante:C35, insuficiência mantida nasV18 eV35. V21 junto aoPC55C eV37 junto aoP725 atendem usando a consulta a d/2, após confirmação expressa das condições de carga e apoio porJoão. V4,V5,V15,V33,V40,V47 atendem nas faixas recalculadas com as faces pertinentes. V36/V48 não têm déficit de mínimo no cenário principalC35. V49/V50 usamØ6,3c/10 da peça externa, não c/20 da primeira etapa.')
para('Suspensão:V33 sobreV19 eV40 sobreV20 não atendem. As demais ligações têm situação discriminada na seção5; reação ascendente não foi tratada como tirante descendente. Nas ligacoesV31-V12 eV41-V13 o sentido foi corrigido por confirmacao deJoao. As outras quatro interfaces com sinal negativo foram reservadas porJoao para analise separada com casos de gravidade e vento. V49 apoia diretamente noPC21C e nao exige suspensao emV26.')
para('Na ligacaoV41→V13, a distribuicao uniforme75/25 nao atende:receptora11,05cm²/m contra10,05cm²/m;apoiada5,06cm²/m contra3,67cm²/m. Este e o resultado da distribuicao verificada; outras distribuicoes admissiveis nao foram avaliadas. V31→V12 atende numericamente essa reparticao. Estribos compostos condicionam a conclusao de ambas.')
para('Correcao dos negativos por lado:190comparacoes auditadas,45solicitacoes corrigidas e14extremidades que passam a atender a capacidade emC35. Comparacoes refeitas com as resistencias oficiaisConcretopy arquivadas, sem nova execucao resistente porque secao,armadura e materiais nao mudaram. Essa mudanca nao aprova automaticamente minimos ou os demais controles. NaV43/P723,3/D=8,697tf·m e4/E=12,707tf·m; capacidade8,216tf·m em cada lado:ambos insuficientes.')
para('Negativas:os valores e as insuficiências aparecem por apoio nas fichas. Casos com diferença inferior a0,01tf·m permanecem decididos com precisão integral; o arredondamento das tabelas não altera o resultado.')
title('4. Quadro por viga')
table(['Viga','Positiva','Negativa','Mínimos','Cortante','Suspensão'],[[x['beam_id'],x['positive'],x['negative'],x['minimum'],x['shear'],x['suspension']] for x in summary])
title('5. Ligações entre vigas')
para('Sinal da reacao:positiva descendente conforme o papel fisico validado. NasV31-V12 eV41-V13 os valores apresentados sao os opostos das reacoes originalmente negativas na listagemTQS, por acao-reacao confirmada porJoao. Nas outras quatro interfaces de sinal negativo, os nomes sao os papeis originaisTQS e o sentido fisico fica para analise separada deJoao. Rmín/Rmáx são os extremos característicos da viga apoiada sobre a receptora. Não são reações dos pilares da receptora. A área para100% da força, quando arquivada, é apenas referência de transferência e não a armadura final de suspensão.')
table(['Apoiada→receptora','Rmín(tf)','Rmáx(tf)','Situação'],[[z['supported_beam']+'→'+z['receiving_beam'],n(z['reaction_min_tf']),n(z['reaction_max_tf']),sstatus(z)] for z in S])
for z in S:
 para('**'+z['supported_beam']+'→'+z['receiving_beam']+':** '+z['reason'])
for z in json.loads((O/'suspensao_sobreposicoes_V29_V39.json').read_text(encoding='utf8')):
 para(z['receiving_beam']+':soma conservadora de suspensão+cortante exige'+n(z['total_required_cm2_m'])+'cm²/m;fornecida'+n(z['provided_cm2_m'])+'cm²/m. Área atende; permanece comprovar o funcionamento/ancoragem das duas peças de estribo de138/50cm. Não há aprovação integral da ligação.')
for z in json.loads((O/'suspensao_sobreposicoes_V31_V41.json').read_text(encoding='utf8')):
 para(z['receiving_beam']+':soma conservadora dos dois tirantes e cortante regional='+n(z['total_required_cm2_m'])+'cm²/m;fornecida='+n(z['provided_cm2_m'])+'cm²/m. Area atende; eficacia das pecas compostas permanece separada.')
for z in json.loads((O/'suspensao_V31_V12_V41_V13.json').read_text(encoding='utf8')):
 r=z['result'];part=z['supported_25_percent'];para(z['connection']['supported_beam_id']+'→'+z['connection']['receiving_beam_id']+':distribuicao uniforme75/25. Receptora:exigida='+n(r['asw_per_s_total_required'])+'cm²/m;existente='+n(z['full_transfer']['provided_cm2_m'])+'cm²/m. Apoiada:exigida='+n(part['required_rate_cm2_m'])+'cm²/m;existente='+n(part['provided_rate_cm2_m'])+'cm²/m. Cortantes regionais e parcelas calculadas peloConcretopy; pecas compostas condicionam o resultado. A falha desta distribuicao uniforme nao esgota outras distribuicoes admissiveis.')

title('6. Fichas de verificação')
for bid,xs in by.items():
 title(bid,3);m=next(x for x in M if x['beam_id']==bid)
 para('Geometria nominal do detalhe:'+ '; '.join(str(int(q[0]))+'×'+str(int(q[1]))+'cm' for q in m['section_labels_detail_cm'])+'. Forma/detalhamento:presença nominal confirmada. '+('Divergência local de altura conforme nota abaixo.' if bid=='V42' else 'Comparação nominal de seções conforme inventário.')+' Situacao longitudinal:'+geometry_status(bid,xs)+'.')
 if bid in custom:para(custom[bid])
 para('**Flexão positiva - solicitaçõesMk e resistência equivalenteMRd/γf emtf·m.**')
 rows=[]
 for x in xs:
  p=x['positive'];s=p['scenarios'][0];c=s['concretopy'];state=result(s['capacity_passes'])
  if bid in variable:state+=' / SEÇÃO LOCAL A CONFIRMAR'
  if not valid(s):state='HIPÓTESES DO MOTOR NÃO ATENDIDAS'
  if p['demand']['magnitude']==0:state='SEM MOMENTO POSITIVO NA ENVOLTÓRIA'
  rows.append([x['model_name']+'/'+x['span_token'],'–'.join(support_label(bid,sp) for sp in x['support_names']),str(x['section_cm'][0])+'×'+str(x['section_cm'][1]),steel(p['configuration']),n(c['d_equivalente_cm']),n(p['demand']['magnitude']),n(s['Mk_eq_tfm']),result(s['minimum_passes']) if s['minimum_passes'] is not None else 'SEM Mk POSITIVO',state])
 table(['Modelo/trecho','Apoios','b×h(cm)','Armadura','d(cm)','Mk','MRd/γf','Mínimo','Resultado'],rows)
 if bid in ['V49','V50']:
  regional=next(q for q in json.loads((O/'geometria_e_flexao_regional_V49_V50.json').read_text(encoding='utf8')) if q['beam']==bid)
  para('**Flexao positiva regional - conclusao aplicavel as alturas reais.**')
  table(['h(cm)','Intervalo modelo(m)','d(cm)','Mk(tf·m)','MRd/γf(tf·m)','Resultado'],[[n(q['h_cm'],0),n(q['interval_model_m'][0],3)+'-'+n(q['interval_model_m'][1],3),n(q['concretopy']['d_equivalente_cm']),n(q['demand']['Mk_tfm']),n(q['concretopy']['mrd_kncm']/100/1.4/9.80665),result(q['capacity_passes'])] for q in regional['positive_regions']])
  para('Origem:Concretopy; geometria_e_flexao_regional_V49_V50.json. Cota130cm medida da mudanca de altura ate a face interna do pilar direito. Fundo continuo; nao e degrau de fundo. A tabela regional prevalece sobre a comparacao nominal unica acima.')
 para('**Flexao negativa - maximo de cada lado do apoio; valores absolutos emtf·m.**')
 para('E=inicio do trecho;D=fim do trecho. Em apoio intermediario, fim do trecho anterior e inicio do seguinte sao verificacoes distintas.')
 rows=[]
 for x in xs:
  for q in x['negative']:
   s=q['scenarios'][0];c=s['concretopy'];state=result(s['capacity_passes'])+(' / GEOMETRIA PENDENTE' if q['geometry_pending'] else '')
   rows.append([x['span_token']+'/'+('E' if q['end']=='left' else 'D'),support_label(bid,q['support']),n(q['section_height_cm'],0),steel(q['configuration']),n(c['d_equivalente_cm']),n(q['governing_Mk_own_side_tfm'],3),n(s['Mk_eq_tfm'],3),result(s['minimum_passes']) if s['minimum_passes'] is not None else 'SEM Mk NEGATIVO',state])
 table(['Trecho/lado','Apoio','h(cm)','Armadura superior','d(cm)','Mk negativo','MRd/γf','Mínimo','Resultado'],rows)
 
 for x in xs:
  for q in x['negative']:
   z=q['scenarios'][0];rr=z['concretopy'];mi=rr['minimum_by_actual_section']
   if z['minimum_passes'] is False:para('Mínimo não atendido no apoio'+support_label(bid,q['support'])+':As='+n(rr['as_total_cm2'])+'cm²; mínimo absoluto='+n(mi['As_absolute_min_cm2'])+'cm²; momento mínimo equivalente='+n(mi['Mk_min_eq_tfm'])+'tf·m; resistência equivalente='+n(z['Mk_eq_tfm'])+'tf·m.')
 para('Mínimos:comparação deMRd doConcretopy comMd,mín=0,8W0fctk,sup e taxa absoluta0,15%, conforme17.3.5.2.1. O arquivo bruto também conserva a avaliação tabelada do motor; ela não substitui a verificação com d efetivo. A falta de momento positivo não demonstra necessidade de armadura positiva mínima na face não tracionada.')
 para('**Cortante - Vk característico emtf; taxas emcm²/m.**')
 rows=[]
 for x in xs:
  for q in x['shear']:
   s=q['scenarios'][0];r=s['concretopy_via_adapter'];ad=q.get('adopted_direct_support_check');v=ad['Vk_tf'] if ad else q['demand']['magnitude'];vr=r.get('VRd2_kn');diag=r.get('diagonal_compression',{}).get('passes')
   proof=q.get('whole_model_interval_upper_demand_check');interval_label=n(q['start_model_m'])+'–'+n(q['end_model_m']);required=s['adopted_requirement_cm2_m'];passed=s['adopted_area_passes']
   if not x['domain']['physical_block_faces_proved'] and not ad and proof and proof['passes']:
    v=proof['force_bound']['Vk_tf'];required=proof['required_cm2_m'];passed=proof['passes'];diag=proof['concretopy']['diagonal_compression']['passes'];interval_label='INTERVALO TQS INTEIRO (LIMITE)'
   rows.append([x['span_token'],interval_label,str(q['legs'])+'r Ø'+n(q['diameter_mm'],1)+'c/'+n(q['spacing_cm'],0),n(q['depth_selection']['d_cm']),n(v),n(q['provided_cm2_m']),n(required),result(passed),'L:'+result(s['longitudinal_max_spacing_passes'])+' / T:'+result(s['transverse_max_spacing_passes']),result(diag)])
 table(['Trecho','Intervalo modelo(m)','Estribo','d(cm)','Vk','Fornecida','Exigida','Área','s máximo L/T','Biela'],rows)
 para('INTERVALO TQS INTEIRO (LIMITE):maior|Vk| de todas as13secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.')
 para('Passagem geométrica do vibrador4cm:'+('atende entre estribos nas faixas calculadas.' if all(q['spacing_cm']-q['diameter_mm']/10>=4 for x in xs for q in x['shear']) else 'há faixa a rever.')+' Esse controle não comprova ausência de congestionamento nos encontros. Espaçamento transversal entre ramos e respectivos limites estão preservados no resultado bruto; quatro ramos com peças sobrepostas dependem da disposição do corte.')
 for x in xs:
  ds=x.get('drawn_length_difference_cm')
  if ds is not None and abs(ds)>1:para('Trecho'+x['span_token']+':diferença entre domínio consultado e soma dos comprimentos de faixa='+n(ds)+'cm. Conferir referências das pontas antes de afirmar cobertura integral.')
  if not x['domain']['physical_block_faces_proved']:para('Trecho'+x['span_token']+':domínio de cortante conserva referência doTQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.')
  for q in x['shear']:
   if q.get('adopted_direct_support_check'):para('Trecho'+x['span_token']+':'+q['scenarios'][0]['adopted_basis']+'; condições confirmadas porJoão. O cortante sem redução e a consulta adotada são preservados separadamente noJSON.')
 cs=[z for z in S if bid in [z['supported_beam'],z['receiving_beam']]]
 para('**Suspensão:** '+('; '.join(z['supported_beam']+'→'+z['receiving_beam']+':'+sstatus(z) for z in cs) if cs else 'sem ligação indireta física identificada no inventário deste modelo.'))
 para('Origem:detalhe'+m['detailing_sheet']+';recorte'+Path(xs[0].get('source_crop') or m['detail_crop']).name+';esforços e resultados por modelo/trecho noJSON desta emissão. Cada linha conserva arquivo, número de linha e envoltóriaTQS.')

title('7. Itens ainda não encerrados e responsabilidade pela pendência')
table(['Item','O que falta','Origem da pendência'],[['Geometria de todos os vãos','Concluir comparação de cotas forma/detalhe e associação de faces de blocos em todas as vigas','Leitura/registro pelo assistente não concluído; não é ausência documental comprovada'],['V23/V24/V42','Concluir transicoes internas; secoes nominais dos picos e apoios ja identificadas. V49/V50 encerradas quanto a posicao das mudancas50/87cm','Associacao de transicoes nao encerrada; divergenciah110 daV42 mantida'],['V31/V41 sobreV12/V13','Sentido e eixos confirmados; concluir eventual distribuicao alternativa na ligacaoV41-V13 e eficacia dos estribos compostos','Distribuicao uniforme75/25 nao atendeV41-V13; nao e falta de confirmacao do apoio'],['V17-V23,V17-V42,V35-V15,V36-V5','Consultar esforcos por caso de gravidade e vento; definir sentido fisico antes de calcular suspensao ou levantamento','Analise separada deJoao, expressamente autorizada; caso1 localizado, listagem disponivel sem esforcos de barras'],['V21-V22,V32-V15,V50-V34','Comprovar quantidade/posicao efetiva dos estribos na regiao normativa e completar100% do tirante','Faixas e encontros localizados; fase dos estribos e reparticao do tirante integral nao encerradas'],['Peças de estribo138/50cm','Comprovar ancoragem e funcionamento conjunto na altura final165cm','Detalhe composto exige interpretação resistente; não somar quatro ramos automaticamente'],['Cabimento das armaduras nos nós','Confrontar centros, pernas dos estribos e barras das vigas/pilares que se encontram','Não encerrado nesta emissão; passagem4cm entre estribos não comprova o nó']])
para('Decisões deJoão já incorporadas:C35 uniforme; marcas/cortes prevalecem; vibrador4cm;NB deP756/P761 mantido; exclusão de barras da primeira etapa; inclusão dos cálculos convencionais das vigas altas;PAR excluídos; anotações separadas; condições para d/2 confirmadas nos dois locais; V31 apoiaV12; V41 apoiaV13; inicio1B no eixo; V49 direto no blocoPC21C; estribos compostos avaliados apenas pelas pranchas recebidas. Não reapresentar essas decisões como dúvidas abertas.')
title('8. Arquivos de cálculo e rastreabilidade')
para('Resultados oficiais de seção:verificacoes_globais_concretopy.json. Entradas:entradas_vigas_50.json. DadosTQS:tqs_operacional_atual.json;validacao_tqs_atual.json. Ligações:suspensao_inventario_global.json,suspensao_V19_V20.json,suspensao_sobreposicoes_V29_V39.json. Decisões:decisoes_confirmadas_2026-10-16.json. Integração:manifesto_integracao_global.json e auditoria_floor_review.json. Evidências visuais na pasta evidencias. Histórico de rodadas preservado.')
para('SHA256 doVGESFS atual:'+D['source_model_sha256']+'. Identificacao e assinaturas dosPDFs eminventario_fontes_atual.json; copias desta retomada preservadas emfontes_retomada. A7201 tem registro proprio emevidencias/7201_fonte.json. A7402 foi regravada:85089linhas e12recortes coincidem com o acervo. A7403 tambem foi regravada:97707linhas coincidem;16recortes conferidos por identidade de pixels em configuracao equivalente eV33 por comparacao visual. As diferencas deV33 sao comentarios e realces. Revisao dos negativos emrevisao_negativos_por_lado.json,com arquivo e linhaTQS de cada lado. Evidencias emauditoria_fontes_congeladas_retomada.json. Anotacoes sao propostas separadas; originais preservados.')
text='\n'.join(lines).replace('–','-').replace('—','-')
# Add word separation around common technical tokens for readable engineering prose without changing numbers or file identifiers.
import re
text=re.sub(r'(?<=[a-záéíóúãõç])(?=(?:V\d|P\d|PC\d|Concretopy|João|C35|C40|TQS|PAR|PDF|NB|R03|R01|R00))',' ',text)
text=re.sub(r'(?<=[\d)])(?=[a-záéíóúãõç])',' ',text)
text=re.sub(r'(?<=[a-záéíóúãõç])(?=\d)',' ',text)
text=re.sub(r'(?<=[a-záéíóúãõç])(?=[A-ZÁÉÍÓÚ])',' ',text)
text=re.sub(r'([:;])(?=\S)',r'\1 ',text)
text=re.sub(r',(?=[A-Za-zÁÉÍÓÚáéíóú])',', ',text)
text=text.replace('k N','kN').replace('NBR6118','NBR 6118').replace('ecm²','e cm²').replace('Mantidosγf','Mantidos γf').replace('eγs','e γs').replace('meiodedesign_shear','meio de design_shear')
text=text.replace('funçãoverificar','função verificar').replace('meiodedesign','meio de design').replace('pelofloor_review','pelo floor_review').replace('doConcretopy','do Concretopy').replace('dotermo','do termo').replace('emtf','em tf').replace('emcm','em cm').replace('emDOCUMENTACAO','em DOCUMENTACAO').replace('pastaevidencias','pasta evidencias')
text=re.sub(r'SHA256 do VGESFS atual: [^.]+', 'SHA256 do VGESFS atual: '+D['source_model_sha256'],text)
(O/'relatorio_global_vigas_S07.md').write_text(text,encoding='utf8');(O/'quadro_global_vigas.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'beams':len(by),'intervals':sum(map(len,by.values())),'connections':len(S),'floor_status':compact['overall_status'],'report':str(O/'relatorio_global_vigas_S07.md')},ensure_ascii=True))
if '--pdf' not in sys.argv:sys.exit(0)
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4,landscape
pdfmetrics.registerFont(TTFont('Arial',r'C:\Windows\Fonts\arial.ttf'));pdfmetrics.registerFont(TTFont('ArialB',r'C:\Windows\Fonts\arialbd.ttf'))
styles=getSampleStyleSheet();styles.add(ParagraphStyle(name='BodyATP',fontName='Arial',fontSize=9,leading=12,spaceAfter=5));styles.add(ParagraphStyle(name='CellATP',fontName='Arial',fontSize=7.3,leading=9.3));styles.add(ParagraphStyle(name='LabelATP',parent=styles['BodyATP'],keepWithNext=True));styles.add(ParagraphStyle(name='SmallATP',fontName='Arial',fontSize=7,leading=9));styles.add(ParagraphStyle(name='HATP',fontName='ArialB',fontSize=15,leading=19,spaceAfter=12,spaceBefore=10,keepWithNext=True));styles.add(ParagraphStyle(name='SubATP',fontName='ArialB',fontSize=12,leading=15,spaceAfter=9,keepWithNext=True))
W,H=landscape(A4);margin=32;avail=W-2*margin
story=[]
def ptxt(s,sty='BodyATP'):
 s=html.escape(s);s=re.sub(r'\*\*(.*?)\*\*',r'<b>\1</b>',s);return Paragraph(s,styles[sty])
def addtable(rows):
 cols=len(rows[0]);weights=[1]*cols
 if cols==9:weights=[.75,1.45,.6,1.45,.55,.6,.7,.9,1.8]
 elif cols==10:weights=[.55,1,.95,.55,.55,.65,.65,.85,.75,.7]
 elif cols==5:weights=[.4,1.3,1.3,1.8,1.3]
 elif cols==4:weights=[1.2,.65,.65,1.9]
 elif cols==3:weights=[.8,2.3,2.1]
 elif cols==2:weights=[1,3]
 widths=[avail*x/sum(weights) for x in weights];data=[[ptxt(c,'CellATP') for c in row] for row in rows];t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT');t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#DCEBEA')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F5F7F8')]),('VALIGN',(0,0),(-1,-1),'TOP'),('BOX',(0,0),(-1,-1),.4,colors.HexColor('#B8C8CB')),('INNERGRID',(0,0),(-1,-1),.25,colors.HexColor('#D5DFE1')),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]));story.extend([t,Spacer(1,8)])
raw=text.splitlines();i=0
while i<len(raw):
 line=raw[i].strip()
 if not line:i+=1;continue
 if line.startswith('|'):
  rows=[]
  while i<len(raw) and (not raw[i].strip() or raw[i].strip().startswith('|')):
   z=raw[i].strip()
   if z.startswith('|') and not re.match(r'^\|[\s|:-]+\|$',z):rows.append([x.strip() for x in z.strip('|').split('|')])
   i+=1
  if rows:addtable(rows)
  continue
 if line.startswith('### V'):
  story.append(PageBreak());story.append(ptxt(line[4:],'HATP'))
 elif line.startswith('# '):story.append(ptxt(line[2:],'HATP'))
 elif line.startswith('## '):
  if line.startswith('## 4.') or line.startswith('## 5.') or line.startswith('## 7.'):story.append(PageBreak())
  story.append(ptxt(line[3:],'SubATP'))
 else:story.append(ptxt(line,'LabelATP' if line.startswith('**') else 'BodyATP'))
 i+=1
pdf=O/'relatorio_global_vigas_S07.pdf'
def footer(canvas,doc):
 canvas.saveState();canvas.setStrokeColor(colors.HexColor('#B8C8CB'));canvas.line(margin,26,W-margin,26);canvas.setFont('Arial',7);canvas.drawString(margin,15,'ATP S07 | Térreo | C35 uniforme | Solicitações características | Resistências equivalentes Rd/γf | 16/10/2026');canvas.drawRightString(W-margin,15,str(doc.page));canvas.restoreState()
SimpleDocTemplate(str(pdf),pagesize=landscape(A4),rightMargin=margin,leftMargin=margin,topMargin=30,bottomMargin=37,title='ATP S07 - Relatório global das vigas do térreo',author='Auxiliar de engenharia - revisão para João').build(story,onFirstPage=footer,onLaterPages=footer)
print('PDF_CREATED',str(pdf))