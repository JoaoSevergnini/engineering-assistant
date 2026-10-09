# Revisão da armadura transversal ao cortante

## Escopo e sequência

Executar `tools/reinforcement_checks/shear_review.py`, com diagrama característico auditado, geometria, altura útil selecionada e faixas reais da prancha. Esta camada verifica **somente cortante**, sem suspensão, transferência de reação, combinação de áreas, correção ou redesenho.

Fluxo: obter séries Vk -> preservar domínio TQS -> referência por terços -> interpretar faixas desenhadas -> máximo |Vsk| da própria faixa -> Concretopy -> VRd2 -> Asw/s -> smax -> prática usual -> ramos -> compatibilidade física de porta-estribo quando aplicável -> conclusão específica de cortante.

Ler [dados TQS](tqs-beam-data.md), [convenções de prancha](beam-drawing-convections.md) e [revisão longitudinal](negative-longitudinal-review.md) para geometria e centroides. Não modificar os resultados longitudinais.

## Diagramas e domínio

`ShearDiagram` adapta cada série independente a `MomentDiagram`, reutilizando consultas lineares, crossings e gaps. Os nomes internos do adaptador de momento são convertidos para Vk/kN na saída de cortante; nenhuma equação de interpolação é duplicada. Preservar sinais, identificação da série, pontos, seção e provenance. Para resistência usar magnitude |Vsk|, sem destruir o sinal original.

Não transportar o esforço para face/eixo/DEPEV ou outra posição não amostrada. Consultar extremos da faixa e todos os vértices internos, interpolando somente entre pontos consecutivos válidos. Não extrapolar ou interpolar gaps. Buscar máximo entre todas as envoltórias pertinentes; conservar todos os empates e não interpolar entre séries. Parte desconhecida mantém conclusão completa inconclusiva; falha comprovada em parte conhecida continua FAIL.

## Altura útil e APIs

Decisão `engineer_confirmed_shear_effective_depth_max_layers_v1`: usar a região resistente com maior número de camadas longitudinais; empate por maior As total, depois menor d. Reutilizar áreas, camadas físicas e centroides já retornados pelo Concretopy na revisão regional. Registrar todos os candidatos, origem, empates e seleção. Não criar centroide misto de caudas de overlap, posição fictícia ou bitola equivalente. Sem dados suficientes, d fica pendente.

`concretopy.verificacoes.dimensionar_cortante_viga` recebe SecaoRetangular, Concreto, Aco, Vk em kN, gamma_f/c/s e geometria longitudinal. Retorna `asw_por_s` **cm²/m**, `vc` e `vrd2` em kN. O retorno é governante; obter o mínimo por chamada independente a Vk=0, sem copiar sua fórmula. A parcela solicitante separada não é exposta e fica explicitamente null. O contrato atual sinaliza Vsd>=VRd2 com `RompimentoBielaCompressao`; biela FAIL não é resolvida aumentando área de estribos.

A API calcula d pelo método público da seção. Para o centroide de múltiplas camadas, o assistant usa um subtipo de SecaoRetangular que mantém bw, h, cobrimento e diâmetro físico do estribo e fornece d explicitamente selecionado. Não recalcula posições nem equações de cortante. Esta integração restringe-se a estribos verticais, nk=mk=0, sem extensões silenciosas ao caso de esforço normal.

`concretopy.normas.espacamento_max_estribo_vigas_cm` recebe os mesmos d e VRd2 da chamada de cortante por adaptador de contexto; não utilizar capacidade/default de outra seção ou gamma. Nesta implementação foi corrigida **com autorização expressa do engenheiro** somente sua comparação de ramo, conforme critério por ele fornecido para 18.3.3.2. Ver [auditoria prévia da API](../../../../.codex/analises/shear_concretopy_api_audit.md). O texto integral da NBR não foi consultado: registrar a origem real, sem alegar auditoria normativa independente.

Para área usar `Barra.area_cm2` e quantidade real de ramos. Asw/s fornecido é a área resistente total por passo, com conversão explícita cm -> m; não confundir com Asw de um estribo. Opções usam a definição de área por comprimento para o limite exato de espaçamento; também preservam a sugestão prática conservadora da API pública `calcular_espacamento_equivalente`.

## SHEAR_REFERENCE_DESIGN

Dividir o **domínio TQS correspondente a cada vão** em três partes iguais. As extremidades são incluídas deterministicamente nos dois terços adjacentes. Em cada terço obter seu próprio máximo |Vk| e dimensionamento independente.

Registrar opções usuais Ø5, Ø6,3 e Ø8 e os limites por área resistente e smax. Número de ramos é cenário explicitamente declarado; cenário de referência não prova a eficácia da peça desenhada. Os terços servem como referência, comparação e diagnóstico; **não são fronteiras obrigatórias do detalhamento**.

Decisões: `engineer_confirmed_shear_reference_thirds_v1` e `engineer_confirmed_usual_stirrup_diameters_v1`. Se nenhuma opção usual atende aos demais critérios usuais, indicar REQUIRES_ENGINEERING_REVIEW; não escolher automaticamente bitola maior. Ruptura de biela permanece FAIL estrutural, não questão de bitola.

## SHEAR_DRAWN_REGION_CHECK

A fonte física é a prancha: marca, diâmetro, espaçamento, ramos, intervalo real, função e source. Não substituir por sugestão de estribos do TQS. Cada troca documental define uma faixa; preservar trechos especiais pequenos.

Intersectar o intervalo desenhado com cada domínio Vk válido e registrar partes conhecidas/desconhecidas. Dimensionar pela maior magnitude **da própria faixa**, nunca pelo terço parcialmente atravessado. Transições desenhadas não precisam coincidir com L/3 ou 2L/3. Regra `engineer_confirmed_refined_drawn_shear_region_check_v1`.

Controles separados: biela estrita VRd2>Vsd, área requerida/governante e mínimo, Asw/s fornecido, resistência dos estribos, smax normativo, prática de espaçamento/bitola, número de ramos e porta-estribo específico. Dado faltante bloqueia somente seu controle, mantendo cálculos independentes.

## Prática usual e ramos

- Ø5, Ø6,3 e Ø8 são usuais. Bitola maior é REQUIRES_ENGINEERING_REVIEW, sem FAIL automático.
- Espaçamento >=8 cm atende ao limite prático **inferior**; abaixo disso exige avaliação especial. Não confundir com smax normativo. Regra `engineer_confirmed_usual_minimum_stirrup_spacing_v1`.
- Para bw>40 cm, prática usual de 4 ramos: `engineer_confirmed_four_leg_stirrups_for_wide_beams_v1`. Quantidade realmente desenhada governa a área. Dois ramos em viga larga representam divergência da prática, não falha normativa automática.
- Quatro ramos exigem prova física de quantidade/disposição compatível de porta-estribo. Receber/verificar resultado dessa disposição com fonte; ausente -> INCONCLUSIVE. Não inventar barras ou dar crédito automático à pele. Asw/s suficiente não comprova execução.

A forma não convencional exige interpretação própria: segmentos verticais visíveis não autorizam automaticamente uma quantidade equivalente de ramos resistentes convencionais. N12 da V516/V517 foi confirmada pelo engenheiro como peça para flexão das lajes adjacentes: preservada, sem crédito automático de dois ramos de cortante.

## Transições diagnósticas

Quando a capacidade inversa não é exposta, `inverse_shear_capacity` usa somente chamadas da API pública, por bisseção em **Vk**, não discretização do diagrama em x. Registrar chamadas, bracket e restrição de biela; ausência de solução ou área abaixo do mínimo impede uma capacidade fictícia.

Com esse limite, resolver crossings analiticamente via diagrama existente em +Vk_capacity e -Vk_capacity. Exigir lado físico e domínio do ramo. Selecionar declínio de |Vk| no sentido para dentro do vão, considerando todas as séries e comprovando suficiência depois do crossing selecionado. Múltiplos crossings compatíveis na mesma série, platô, gap ou insuficiência posterior -> INCONCLUSIVE. Não escolher primeiro/último global por conveniência.

Se todas as séries já forem suficientes no ramo inteiro, limite de transição NOT_APPLICABLE: não fabricar crossing. Posição/margem diagnósticas não movem a faixa. A verificação direta de toda a faixa continua principal.

## Resultado e suspensão

PASS/FAIL estrutural, REQUIRES_ENGINEERING_REVIEW de prática usual e INCONCLUSIVE são separados. `global_shear_approval=false` diante de falha comprovada, null se controles necessários/ cobertura permanecem pendentes e nenhuma falha, true somente com todos os controles necessários satisfeitos. Isso **não aprova a viga globalmente**.

Se houver evidência de apoio indireto, registrar `suspension_check_required=true` e `suspension_result=NOT_EVALUATED`. Não calcular reação, Asw de suspensão, combinação de áreas ou capacidade de suspensão, nem reprovar por isso nesta etapa. O trecho físico N1 pode ser conferido isoladamente contra cortante, sem afirmar que sustenta a reação da viga apoiada e sem somar qualquer área de suspensão.

`selected_solution=null` e `detailing_optimization=null`. Não modificar armadura, espaçamento, ramos, comprimentos ou transições.

## Golden e limites atuais

V516/V517: esforços próprios, quatro domínios TQS, seis peças/faixas documentais originais por viga, das quais quatro faixas são estribos da viga após a exclusão funcional de N12; N12 extremos Ø8 c/20 não convencional, N13 intermediárias Ø5 c/14 e Ø5 c/10, N1 especial Ø8 c/12 no intervalo52cm. d selecionado46,7 cm conforme dados regionais e decisão acima, nunca regra hardcoded. Os campos completos estão em V516_shear_reinforcement_review.json e V517_shear_reinforcement_review.json, gerados por validar_v516_v517_cortante.py, e no relatório real, seção de cortante.

Na revisão de 08/10/2026, N12 foi excluída do cortante como armadura negativa de laje adjacente. Trechos comprovadamente internos aos pilares não exigem estribos da viga. Permanecem pendentes os trechos físicos dos vãos extremos sem estribos documentados. Preservar integralmente os goldens longitudinais e demais revisões.

## Classificação funcional e cobertura física (08/10/2026)

Antes de verificar uma peça, usar `shear_coverage.classify_piece`: armadura negativa de laje adjacente (`ADJACENT_SLAB_NEGATIVE_REINFORCEMENT`) é preservada documentalmente, mas excluída de Asw/s, ramos e chamadas de dimensionamento da viga. Exigir função confirmada, geometria e fonte; nome, bitola ou espaçamento isolados não determinam função. Caso ambíguo: INCONCLUSIVE e solicitar interpretação. Decisão `engineer_confirmed_n12_adjacent_slab_negative_reinforcement_v1`: peça dos casos reais assegura continuidade de negativa entre lajes em desnível; não é estribo da viga. Excluir não comprova armadura substituta nem aprova o vão.

`TQS_SHEAR_DOMAIN` mantém esforços/seções originais. `BEAM_STIRRUP_COVERAGE_DOMAIN` é independente: entre faces internas de pilares comprovados. `physical_coverage` requer tipo/fonte, eixo, largura longitudinal e ambas as faces consistentes. Reutilizar faces geométricas existentes; nunca inferir deslocamento fixo ou face pelo DEPEV. Decisão `engineer_confirmed_stirrups_terminate_at_column_faces_v1`: estribos da viga terminam nas faces dos pilares; não se exige continuidade dentro destes. Não estender a apoios indiretos/balanços sem regra específica.

Particionar intervalos pelas faces e limites documentais: WITHIN_SUPPORT/NOT_APPLICABLE somente com prova de contenção física no pilar; REQUIRED_BEAM_COVERAGE para cobertura comprovada; UNCOVERED_REQUIRED_REGION/INCONCLUSIVE para trecho obrigatório descoberto; GEOMETRY_INCONCLUSIVE quando faltam fontes/faces/tipo. Ambiguidade da peça não fornece cobertura. Faixas não são prolongadas e o domínio físico não autoriza extrapolação dos esforços; controle necessário sem amostragem válida permanece inconclusivo.

Correção anterior de smax no Concretopy expressamente autorizada pelo engenheiro: mantida com os oito testes. Autorização para editar e origem técnica do critério são proveniências distintas. Critério fornecido pelo engenheiro; texto integral normativo não consultado nesta rodada. Nenhuma alteração adicional no Concretopy.
