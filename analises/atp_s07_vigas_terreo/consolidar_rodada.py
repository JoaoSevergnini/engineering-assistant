from pathlib import Path
import json,shutil,math,hashlib
ROOT=Path(r'\\srvmaster\PUBLICO\Joao Severgnini\Simon\engineering-assistant');OUT=ROOT/'analises/atp_s07_vigas_terreo'
PROJECT=Path(r'S:\PROJETOS EM EXECUÇÃO\25-208-WERT-ATP TERRA ALL RESORT-PORTO BELO-SC\PRANCHAS\APOIO\JOAO\ATP S07');DOC=PROJECT/'DOCUMENTACAO ATP';DEST=DOC/'10 VIGAS - TERREO';DEST.mkdir(exist_ok=True)
rows=json.loads((OUT/'matriz_vigas.json').read_text(encoding='utf8'));pars=json.loads((OUT/'matriz_PAR_reservatorios.json').read_text(encoding='utf8'));ind=json.loads((OUT/'V16_conferencia_independente.json').read_text(encoding='utf8'));pilot=json.loads((OUT/'V16_resultado_resumido.json').read_text(encoding='utf8'));v21=json.loads((OUT/'V21_cortante_primeiro_vao.json').read_text(encoding='utf8'));val=json.loads((OUT/'validacao_rodada.json').read_text(encoding='utf8'));screens=json.loads((OUT/'triagem_secoes_criticas.json').read_text(encoding='utf8'))
missing=[r['beam_id'] for r in rows if not r['tqs_links']]
body='''# ATP S07 — Vigas do térreo — Rodada 01

Data: 15/10/2026. Responsável pela decisão e revisão final: João.

**Estado: revisão parcial, com uma insuficiência positiva comprovada em V16. Não é aprovação do pavimento nem fechamento da verificação total.**

## Resultado principal — V16, PC40C–PC41C

A V16 da prancha 7401 R00 corresponde à V13 do TQS, pelos apoios PC40C/PC41C e pela distância entre apoios. A seção detalhada e a forma indicam 40×50 cm. A elevação, o corte e a tabela de aço confirmam N4 = 4 Ø12,5, C850, na face inferior; N1 = 4 Ø10, C290, na região superior central. Não se usou a armadura selecionada do TQS como armadura executiva.

| Grandeza | Resultado |
|---|---:|
| Momento característico positivo máximo, VGESFS V13 | 166,066 kN·m |
| Coeficiente de ações, conforme listagens TQS | 1,40 |
| Momento solicitante de cálculo | **232,492 kN·m** |
| Área da positiva N4, 4 Ø12,5 | 4,909 cm² |
| Altura útil de N4: 50−3,5−0,63−0,625 | 45,245 cm |
| MRd da positiva N4 em seção retangular, C35 | **93,884 kN·m** |
| MRd da positiva N4, sensibilidade C40 | 94,219 kN·m |
| Msd/MRd, C35 | **2,476** |

**Apontamento VIG-RES-001 — corrigir/redimensionar a positiva de V16 frente às solicitações adotadas.** A capacidade de N4 é muito inferior à demanda, embora a armadura mínima seja atendida. Não foi selecionada uma nova armadura nem foi alterada a prancha.

A conferência independente reproduziu o equilíbrio do bloco comprimido: a=As·fyd/(0,85·fcd·bw)=2,511 cm e MRd=As·fyd·(d−a/2)=93,884 kN·m. Foram mantidas unidades cm, kN e kN·cm antes da conversão final. O cálculo resistente principal foi executado pelo fluxo floor_review e pelos verificadores existentes do Concretopy, sem alteração de seus métodos.

Como controle superior, foi considerado todo o aço que atravessa a seção de máximo positivo — N4, 4 Ø12,5, mais N1, 4 Ø10 — ficticiamente tracionado a 500 MPa, sem redução de resistência do aço, com braço de alavanca igual à altura total de 50 cm. Mesmo esse limite deliberadamente favorável é **201,258 kN·m < 232,492 kN·m**. Portanto, simplesmente contar a armadura superior ou uma mesa de concreto contida na altura documentada não resolve a insuficiência encontrada. Esse limite não é um dimensionamento normativo nem uma proposta de solução.

### Demais controles executados de V16

- **Mínimo longitudinal:** atende a via de momento mínimo e taxa absoluta do item 17.3.5.2.1, para as composições críticas verificadas. Não se confundiu atendimento ao mínimo com atendimento ao momento solicitante.
- **Negativas nas regiões críticas junto às faces dos apoios:** atendem no método retangular adotado. MRd=150,405 kN·m em C35; solicitações de cálculo nas faces de aproximadamente 81,407 e 124,436 kN·m. O trecho central e suas duas sobreposições não possuem momento negativo nas envoltórias utilizadas. Ancoragem e escalonamento não integram esta conclusão.
- **Cortante:** a faixa N5 tem dois estribos fechados sobrepostos, totalizando quatro ramos Ø6,3 c/20. A tabela confirma 74 peças, coerentes com 2×37. A área fornecida é 6,234 cm²/m. Compressão diagonal, área necessária/mínima e espaçamento máximo longitudinal atendem nos cenários C35/C40; smax longitudinal=27,042 cm, contra 20 cm desenhados. O limite transversal é maior que toda a largura de 40 cm, atendendo por esse limite geométrico conservador.
- **Espaçamento mínimo longitudinal dos estribos:** pendente a comprovação de passagem do vibrador/adensamento, conforme 18.3.3.2. Não foi aplicado mínimo interno de 8 cm.
- **Suspensão em apoio indireto:** não aplicável na V16, pela região completa da forma PC40C–PC41C e pelo inventário de ligações do modelo. Esse resultado não se estende às demais vigas.

## Premissas confirmadas nesta rodada

1. Usar esforços do TQS com as seções do detalhamento, conforme orientação expressa de João em 15/10/2026. Uma divergência geométrica TQS×documentos não bloqueia, por si só, esse cálculo autorizado. Mantêm-se necessárias a identidade física, a natureza/unidade e a associação da solicitação à região correta.
2. Apontar divergências entre forma e detalhamento. A diferença anterior de V1 — TQS 30×50 contra documentos 30×55 — deixa de ser impedimento automático. Não é uma divergência forma×detalhamento nessa seção.
3. **“2aFASE” no nome do modelo significa a etapa do ATP em que ele foi desenvolvido, conforme esclarecimento de João. Não significa etapa de concretagem ou carregamento do projeto.** Não inferir abrangência dos esforços pelo nome da pasta.
4. NBR 6118:2023, sem critérios internos de aprovação, otimização ou redesenho. Ancoragem, escalonamento, emendas, ELS e torção não foram incluídos automaticamente; dependências ou situações fora do método permanecem identificadas.

## Documentos e fontes

| Fonte | Revisão recebida | Conteúdo |
|---|---|---|
| Forma 7202 | R03 | Térreo, parte 1 |
| Forma 7214 | R01 | Térreo, parte 2 |
| Detalhe 7401 | R00 | V1–V20, com grupos |
| Detalhe 7402 | R00 | V21–V32 e V39 |
| Detalhe 7403 | R01 | V33–V38 e V40–V50 |
| Detalhe 7404 | R00 | Nove elementos PAR dos reservatórios e mísulas |

Caminhos e hashes: inventario_pranchas.json. O texto comum desses PDFs só recuperou rodapés; os dados usados foram examinados visualmente em ampliações. A limitação de extração não foi tratada como ausência na prancha.

Modelo indicado: C:/TQS/25-208-ATP___24-1454-WERT-WPBGR RESIDENCE-PE-MU2-S07-ATP2___2aFASE-Calc01/TÉRREO/VIGAS. VGESFS fornece 44 identificações: V1–V35 e nove PAR, com 485 séries de 13 seções de esforços. Valores característicos, sinais, reações máximas/mínimas, texto original e linhas de origem foram preservados em tqs_operacional.json. Conversão metrológica: 1 tf=9,80665 kN; tf·m convertido pelo mesmo fator. A natureza característica foi corroborada pela legenda de RELDTVGS.

Foram cotejadas 365 séries com a normalização do extrator documental existente, sem divergência de conversão. Cinquenta séries de vigas, incluindo tokens B e formatos não expostos pelo parser anterior, permanecem extraídas pelo adaptador documental desta rodada, com texto/linhas preservados; não foram convertidas em esforços nulos. Os 70 conjuntos restantes pertencem aos PAR e têm origem própria. Esse controle valida transcrição/conversão, não a correção do modelo de cálculo.

## Níveis e concretagem

Foram preservadas as correções do contexto: térreo principal +9,18 m; topo local do P791 +8,88 m; topo de V49 em +9,55 m no encontro com P749; primeira concretagem dos pilares indicados dos reservatórios até +9,28 m. A correção da referência de P799/P807C não substitui automaticamente todos os níveis locais da forma.

As formas assinalam regiões de primeira e segunda concretagem com concretos de 40 e 35 MPa; o rosa nos detalhes identifica a primeira etapa. Barras situadas no topo da primeira concretagem podem ficar em altura intermediária na seção final. Não foram somadas às barras inferiores ou superiores como se estivessem na mesma camada. Nas triagens C35/C40, os dois concretos são sensibilidades separadas; resultados de um cenário não reprovam automaticamente uma região cujo concreto é outro. Compressão em concretos de etapas diferentes e barras intermediárias exigem composição resistente compatível.

## Conferência documental — apontamentos

| Código | Elemento | Constatação | Encaminhamento |
|---|---|---|---|
| VIG-DOC-001 | V26, 7402 | O detalhe identifica PC26C/PC24C/PC20C, repetindo os rótulos do detalhe V14. Na posição da V26 na forma, a cadeia é PC19C/PC21C/PC25C. | Compatibilizar os apoios e as remissões do detalhe com a forma. Não selecionar esforços pelo rótulo repetido. |
| VIG-DOC-002 | V3 e V6, 7401 | O resumo inferior da elevação indica 2 Ø20; N1 indica 4 Ø16 e o corte mostra quatro barras inferiores. | Compatibilizar resumo, posição e corte antes da verificação resistente completa. Não registrar falta física de aço. |
| VIG-DOC-003 | V22, 7402 | Resumo superior esquerdo: 2 Ø16; chamada N1: 2 Ø12,5, C353. | Esclarecer a composição efetiva e compatibilizar as representações. |
| VIG-GEO-001 | V42, 7403 × formas | O detalhe inclui trecho 30×110 cm; a região correspondente da forma utiliza rótulos 30×80/30×50, com desníveis locais. | Conferir posição exata da transição, topo/fundo e incidência no encontro P791–P784 antes de fixar a divergência por trecho. Não impor mudança de seção ou nível por leitura de escala. |

Todos os identificadores V1–V50 e os nove PAR foram localizados nas formas e nos detalhes indicados. Isso fecha a presença nominal nos dois sentidos, mas **não** a conferência completa dos vãos, mudanças de seção, cotas e abrangência individual dos grupos. PAR706 não consta no conjunto examinado; a sequência não é contínua e não foi tratado como elemento faltante.

## Cortante de V21 — ponto adicional para revisão

V21 do detalhe corresponde à V15 do TQS na cadeia PC54C–PC55C–PC56C–PC57C–PC59C–PC60C. No primeiro vão, N21 é Ø8 c/17, fechado com dois ramos, Asw/s=5,914 cm²/m. Para bw/h=30/50 cm e d=44,70 cm:

- máximo entre faces na coordenada do modelo: Vsk=195,130 kN; Vsd=273,182 kN;
- taxa necessária pelo modelo I: 8,235 cm²/m em C35 ou 7,548 cm²/m em C40;
- na sensibilidade de carga distribuída avaliada a d/2 das faces, Vsd=247,333 kN; taxas necessárias de 6,757 e 6,070 cm²/m, respectivamente, ainda maiores que 5,914 cm²/m.

**VIG-CIS-001 — revisar a armadura transversal e a solicitação aplicável no primeiro vão de V21.** O resultado calculado é insuficiente no modelo I utilizado. Antes do fechamento normativo, confirmar a classificação das ações próximas aos apoios, o modelo de cortante documentado, as faixas reais e eventuais contribuições adicionais. O item 17.4.1.2.1 distingue carga distribuída e concentrada e impõe condições às reduções; não foi inventada uma redução para carga concentrada. A sensibilidade artificial d≈h foi preservada apenas como limite diagnóstico, não como altura útil física nem como aceitação.

## Cobertura resistente e limites

- 19 vigas, 45 vãos: triagem de seções críticas de flexão positiva/negativa, mínimo e cortante, usando Concretopy. O arquivo triagem_secoes_criticas.json conserva composição usada, cenário C35/C40, solicitação, capacidade e ressalvas. **Essa triagem não é revisão regional completa nem aprova as 19 vigas.** Resultados negativos não foram promovidos automaticamente a reprovação quando faltam barras intermediárias, posição das faces, mesa ou composição completa.
- V16: revisão regional executada para positivas e negativas pertinentes; controles numéricos independentes de cortante e aplicabilidade de suspensão, com resultados discriminados acima.
- V21: cálculo específico adicional de cortante no primeiro vão, com sensibilidade normativa de d/2, ainda sujeito ao enquadramento documentado das cargas e do método.
- Oito vigas curtas de h=165 cm — V3, V6, V7–V10 e V12/V13 — e nove PAR têm comportamento que exige enquadramento específico de viga-parede/elemento de reservatório. O item 22.4.1 foi consultado: o método comum de viga não encerra essa verificação. V29/V31/V39/V41, também altas, foram mantidas separadas; altura isolada não basta para classificá-las.
- 34 relações de apoio nomeadas no TQS foram inventariadas, incluindo relações entre PAR. A transferência indicada pelo modelo foi preservada, mas a reação não foi convertida automaticamente em suspensão aprovada. Direção física, posição, geometria pendurada/não pendurada, região de distribuição e aço efetivamente disponível ainda precisam conciliação para as ligações aplicáveis. Não somar máximos de reações de casos diferentes.

## Pendências para completar o escopo

1. Resolver correspondência ou obter solicitações das 20 vigas ainda sem fonte física associada: MISSING_LIST. A ausência nesta associação não prova omissão do projeto nem autoriza armadura zero, esforço zero ou aprovação.
2. Completar as relações parciais: por exemplo, V15 detalhada tem quatro vãos, enquanto a V12 do TQS associada cobre P757/P756/P760. Os demais vãos não foram preenchidos com esforços de outra viga.
3. Reconciliar os vãos e os comprimentos físicos da documentação. Não usar isoladamente o comprimento C de barra, a distribuição de estribos ou a geometria TQS como prova de cota da forma.
4. Fechar camadas/alturas de todas as barras nas seções críticas, inclusive aço do topo da primeira etapa em posição intermediária. Sem isso, as chamadas resistentes dependentes permanecem inconclusivas; não adotar primeira camada por convenção interna.
5. Fixar o enquadramento e o método aplicável aos elementos de parede/reservatório; registrar transições/desníveis por trecho e executar a suspensão das ligações comprovadas.
6. Completar os controles mínimos/máximos de estribos das faixas reais, incluindo passagem do vibrador. Os controles internos de bitolas usuais, espaçamento prático de 8 cm e quatro ramos por preferência não integram o resultado normativo.

## Matriz individual das vigas V

Presença nominal em forma/detalhe conferida em todas as linhas. “Triagem” e “fonte associada” não equivalem a aprovação; o estado resistente das demais vigas continua inconclusivo.

| Viga | Detalhe | Seções nominais b×h (cm) | Fonte TQS associada | Estado nesta rodada |
|---|---|---|---|---|
'''.replace('MISSING_LIST',', '.join(missing))
for r in rows:
 sec=' / '.join(f'{a}×{b}' for a,b in r['section_labels_detail_cm']);links='; '.join(f"{l['model_name']} ({','.join(l['span_tokens'])})" for l in r['tqs_links']) or 'não encontrada';state='V16: positiva insuficiente; demais controles discriminados' if r['beam_id']=='V16' else 'caso especial: viga-parede' if r.get('method_scope')=='SPECIAL_DEEP_BEAM_22.4.1' else 'transição/registro por trecho pendente' if r.get('method_scope')=='SECTION_OR_LEVEL_TRANSITION_REGISTRATION_REQUIRED' else 'triagem; revisão regional pendente' if r['resistant_screening']=='EXECUTED_SECTION_SCREENING' else 'sem esforço associado';body+=f"| {r['beam_id']} | {r['detailing_sheet']} | {sec} | {links} | {state} |\n"
body+='''
## Elementos PAR — presença e estado

PAR701, PAR702, PAR703, PAR704, PAR705, PAR707, PAR708, PAR709 e PAR710: presentes nas formas e na 7404. PAR701 tem seção nominal 30×442 cm; os demais, 24×412 cm. A revisão resistente específica desses elementos não foi concluída.

## Base normativa efetivamente consultada

Cópia do projeto: DOCUMENTACAO ATP/NBR_6118_2023 - CONCRETO NOVA.pdf. Foram consultados visualmente: 17.3.5.2.1, p.131 (mínimo longitudinal); 17.4.1.1.1, p.134 (mínimo transversal); 17.4.1.2.1, p.135 (cargas próximas aos apoios); 17.4.2.1/17.4.2.2, p.136 (resistência e modelo I); 18.3.3.2, p.150–151 (estribos/espaçamentos); 18.3.6, p.152 (suspensão); 22.4.1, p.184 (vigas-parede). As páginas são as impressas na norma, não índices do leitor PDF. A consulta desses itens não representa auditoria integral da biblioteca ou verificação completa de todos os elementos.

## Rastreabilidade

- matriz_vigas.json e matriz_PAR_reservatorios.json: cobertura individual e pendências.
- tqs_operacional.json: esforços/reacões originais, conversões e proveniência.
- inventario_apoios_indiretos.json: 34 ligações, sem aprovação automática de suspensão.
- V16_resultado_resumido.json e V16_conferencia_independente.json: resultados executados e controle independente.
- V21_cortante_primeiro_vao.json: faixa inicial e sensibilidade de redução.
- triagem_secoes_criticas.json: triagens condicionais, sem seleção de correção.
- validacao_rodada.json: verificações da transcrição e do caso V16.

Os originais TQS/PDF não foram modificados. As diferenças internas das ferramentas foram separadas do veredito normativo. O levantamento de 14/10 permanece como histórico; a premissa de 15/10 e o esclarecimento de “2aFASE” prevalecem nesta rodada.
'''
(OUT/'relatorio_verificacao_rodada_01.md').write_text(body,encoding='utf8')
files=['relatorio_verificacao_rodada_01.md','inventario_pranchas.json','matriz_vigas.json','matriz_PAR_reservatorios.json','tqs_operacional.json','inventario_apoios_indiretos.json','V16_resultado_resumido.json','V16_conferencia_independente.json','V21_cortante_primeiro_vao.json','triagem_secoes_criticas.json','validacao_rodada.json','premissas_2026-10-15.md']
for name in files:
 shutil.copyfile(OUT/name,DEST/name)
 assert hashlib.sha256((OUT/name).read_bytes()).digest()==hashlib.sha256((DEST/name).read_bytes()).digest()
for n in ['7401_V16.png','7401_tabela_direita.png','7402_V26.png','7401_V3.png','7401_V6.png','7402_V22.png']:
 (DEST/'EVIDENCIAS').mkdir(exist_ok=True);shutil.copyfile(OUT/'crops'/n,DEST/'EVIDENCIAS'/n)
context=DOC/'CONTEXTO ATP S07.md';text=context.read_text(encoding='utf-8-sig');marker='## Vigas do térreo — início da revisão em 15/10/2026'
addition='''

## Vigas do térreo — início da revisão em 15/10/2026

Registro: `10 VIGAS - TERREO/relatorio_verificacao_rodada_01.md` e JSONs associados.

João autorizou usar esforços TQS com seções do detalhamento, sem bloquear automaticamente por diferenças geométricas TQS×documentos. Apontar diferenças forma×detalhamento. A pendência impeditiva anterior de V1 por h50 no modelo contra h55 nos documentos foi superada para esse cálculo autorizado; preservar a diferença como origem, sem chamá-la de divergência forma×detalhamento.

João esclareceu: “2aFASE” identifica a etapa do ATP em que o modelo foi desenvolvido, e não as etapas de concretagem ou de carregamento do projeto. Não inferir a abrangência dos esforços pelo nome da pasta.

Presença nominal conferida de V1–V50 e nove PAR em formas/detalhes. Modelo contém V1–V35 e nove PAR; nomes diferem do detalhamento. Foram associadas total ou parcialmente 30 vigas detalhadas por apoios/posição, com 20 ainda sem esforço correspondente. Não há mapa prévio, conforme resposta de João. Uma relação parcial não cobre automaticamente todos os vãos.

Rodada parcial: 19 vigas/45 vãos com triagem de seções, sem aprovação regional/global. V16 do detalhe = V13 do TQS, PC40C/PC41C: positiva N4 4Ø12,5 insuficiente, Msd232,492 contra MRd93,884 kN·m em C35 (94,219 em C40). Elevação/corte/tabela conferidos; controle independente confirma. Negativas críticas atendem; cortante numérico atende, mínimo de espaçamento por vibrador pendente; suspensão não aplicável nessa viga. Não confundir o atendimento ao mínimo longitudinal com resistência suficiente.

V21 do detalhe = V15 TQS: cortante do primeiro vão exige revisão pelo resultado do modelo I, inclusive com sensibilidade d/2; classificação de cargas/reduções e composição integral precisam confirmação antes do fechamento normativo.

Apontamentos documentais: V26 nomes de apoios incompatíveis com a forma; V3/V6 resumo2Ø20 contra posição/corte4Ø16; V22 resumo2Ø16 contra N1 2Ø12,5; V42 trecho110cm versus rótulos80/50 na forma, pendente a localização exata por níveis/transição. Não declarar todos os vãos/seções integralmente compatibilizados.

34 ligações de apoio nomeadas no TQS inventariadas, sem dimensionamento/aprovação global de suspensão. Oito vigas curtas h165 e nove PAR exigem método especial; não aprovar por verificador de viga usual. Nenhum critério interno de aceitação, alteração de PDFs ou seleção de nova armadura nesta rodada. A verificação total do pavimento permanece aberta nas pendências discriminadas no relatório.
'''
if marker not in text:context.write_text(text+addition,encoding='utf8')
print('REPORT',DEST/'relatorio_verificacao_rodada_01.md');print('copied files',len(files),'report chars',len(body));print('CONTEXT_UPDATED',marker in context.read_text(encoding='utf8'))
