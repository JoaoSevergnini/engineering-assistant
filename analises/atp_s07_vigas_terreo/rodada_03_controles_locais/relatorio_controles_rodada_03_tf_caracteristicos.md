# ATP S07 — vigas usuais — rodada 03 — apresentação em tf e tf·m

> **Premissas substituídas em 16/10/2026:** consultar a rodada04, seção final e faces dos blocos. Barras do topo da primeira concretagem não integram resistência/d; os antigos déficits de cobertura até faces de pilares foram retirados como provas de insuficiência. Este documento conserva histórico e não é a rodada vigente.


15/10/2026. Esta rodada atende à orientação de continuar os controles independentes e reunir ao final os pontos que dependem da avaliação de João. As vigas-parede e os PAR permanecem separados para sua análise. Os resultados anteriores não foram apagados.


## Convenção de apresentação atualizada em 15/10/2026

Esta versão reapresenta os resultados da rodada 03 em tf e tf·m, na base característica para comparação com o TQS. Não constitui novo processamento estrutural; conclusões, hipóteses e pendências permanecem as mesmas.

As solicitações são Mk, Vk ou Rk. As resistências são **equivalentes para comparação**, obtidas por Rd/γf, e não resistências características do material. Neste conjunto foi documentado γf=1,4; γc=1,4 e γs=1,15 continuam aplicados nos cálculos resistentes. Para os limites superiores, a tabela apresenta o limite equivalente, não uma capacidade efetiva. A conversão comum mantém a razão solicitação/resistência e a conclusão de atendimento. Usou-se 1 tf=9,80665 kN, com arredondamento apenas para apresentação.

A versão anterior e os arquivos brutos preservam as unidades e a natureza de cálculo originais para rastreabilidade. Áreas de aço e dimensões não foram convertidas para a base característica.

## Correção da solicitação negativa — máximo no apoio

Em 15/10/2026 foi confirmado que as 136 consultas anteriores de flexão negativa utilizavam interpolação na face interna do apoio. Por orientação de João, essa redução foi retirada. As solicitações e os totais negativos anteriores, preservados abaixo como histórico, estão **substituídos** pela [revisão dos máximos negativos no apoio](revisao_negativos_maximo_apoio.md), com os pontos TQS e a origem das capacidades Concretopy em `revisao_negativos_maximo_apoio.json`. Na V21/primeiro vão/direita (PC55C), Mk passa de **22,29 para 23,76 tf·m**. Foram refeitas as comparações das 136 consultas com as capacidades arquivadas do Concretopy, sem novo cálculo resistente e sem usar limites independentes como resultado oficial. A revisão não elimina pendências físicas nem aprova a composição total onde faltam posições de barras.

## Correção do resumo de cortante — alertas além da V21

A conferência de 15/10/2026 identificou que o resumo anterior não expôs todos os resultados desfavoráveis arquivados. **V18 nos dois vãos e V33 no primeiro vão também apresentam falta de área de estribos nas configurações consultadas, para C35/C40**, além da V21. Outros alertas dependem de d composto, faixas transversais ou classe de concreto; não representam aprovação nem reprovação automática da seção física. A [conferência completa dos alertas de cortante](conferencia_alertas_cortante.md) individualiza todos os casos por viga/modelo/vão, valor fornecido, requerido e dependências, com rastreabilidade em `conferencia_alertas_cortante.json`. Fonte oficial: resultados arquivados de `Concretopy.dimensionar_cortante_viga`; não houve recálculo nesta conferência.

## Conclusões novas

**Positivas insuficientes para as solicitações TQS e seções detalhadas: V16, V21, V25 (P727–P708) e V37. Suspensão insuficiente nas receptoras V19 e V20 nos encontros com V33 e V40, respectivamente.** As verificações de suspensão independem da divergência da armadura longitudinal de V19/V20.

As conclusões desfavoráveis acima não resultam apenas de ignorar aço complementar: foram usadas as barras presentes no pico e limites superiores favoráveis para sua contribuição. Uma resistência calculada de modo favorável ainda inferior à solicitação demonstra a insuficiência para a associação de esforços adotada.

Foram examinadas 42 vigas usuais, em 82 intervalos TQS associados ao detalhamento. Os intervalos não equivalem a aprovação de todos os mecanismos de cada viga. Permanecem quatro picos positivos dependentes de dados específicos: V35/primeiro vão, V24/P778–P769, V49 e V50. As razões estão individualizadas ao final.

## Premissas mantidas

- Esforços do modelo atualizado indicado por João; seções e armaduras do detalhamento recebido. As 605 séries já validadas contra RELDTVGS permanecem vigentes, com a mesma assinatura da rodada02.
- Associação por apoios, inclusive V24/P785–P778 no modelo V23/vão3. O número do intervalo sempre acompanha o nome do modelo para evitar ambiguidade.
- NBR6118:2023, sem aceitação por padrões internos do escritório. Consulta ao exemplar local:17.3.5.2.1,17.4.1.1.1,17.4.1.2.1,17.4.2.1/17.4.2.2,18.3.3.2,18.3.6 e22.4.1.
- Solicitações características em tf/tf·m convertidas por9,80665; γf=1,4, γc=1,4, γs=1,15 e fyk=500MPa. C35/C40 calculados como sensibilidades. Uma falha do cenárioC40 não reprova automaticamente uma região deC35.
- O cenárioC35 dá uma referência conservadora de resistência onde ambos os concretos são≥C35; o mínimo emC40 é a sensibilidade mais exigente de mínimo. Não se atribuiu ao aço da primeira concretagem uma posição externa fictícia.
- Preservados P791+8,88m, V49+9,55m, níveis locais e concreto em etapas do contexto. O verde da forma7214 representa+8,88m; não foi substituído genericamente por+9,18m.
- Ancoragem, escalonamento, ELS e escolha de armadura substituta permanecem fora do escopo solicitado. Estados automáticos desses controles no diagnóstico bruto não são pendências de projeto deste escopo.

## Resultado oficial de flexão positiva — Concretopy

Atualização de apresentação por orientação de João em 15/10/2026. A capacidade oficial abaixo utiliza somente as barras inferiores tracionadas. Origem: **Concretopy**, função `verificar_flexao_viga_retangular`, modelo `bloco_retangular_camadas_escoadas_v1`; resultados arquivados em `controles_independentes.json`, por `beam_id`, `span_token` e `positive.scenarios[].concretopy`. Não houve nova execução nem alteração dos dados de entrada nesta atualização.

| Viga/modelo/vão | Mk (tf·m) | Capacidade equivalente Concretopy C35 (tf·m) | Capacidade equivalente Concretopy C40 (tf·m) | Resultado para as entradas arquivadas |
|---|---:|---:|---:|---|
| V16/1 | 15,28 | 6,84 | 6,86 | Insuficiente |
| V21/1 | 16,87 | 16,08 | 16,30 | Insuficiente |
| V25/4 | 7,50 | 5,13 | 5,15 | Insuficiente |
| V37/1 | 9,95 | 8,50 | 8,56 | Insuficiente |

Todos os valores resistentes da tabela são MRd/γf, com γf=1,4 e conversão 1 tf=9,80665 kN. Os coeficientes dos materiais continuam aplicados pelo motor. O status é relativo à configuração registrada, sem aprovação global da viga.

**Entrada ainda a compatibilizar na V21:** cobrimento 3,5 cm, seção 30×50 cm, 4Ø20 inferiores, estribo Ø8 mm e d=44,70 cm no cálculo arquivado. A planilha apresentada por João usa estribo Ø6,3 mm e d=44,87 cm. A tabela registra a saída efetiva do motor; não confirma que Ø8 mm seja a bitola vigente do detalhe. Após compatibilização dessa entrada, a capacidade oficial deve ser recalculada no Concretopy. Os 16,24 tf·m anteriormente destacados são um limite algébrico auxiliar com contribuição superior; não representam o resultado oficial do Concretopy.

### Conferências independentes — auxiliares, sem substituir o resultado oficial

As tabelas de limites superiores a seguir foram obtidas por cálculo algébrico independente do assistente, a partir da equação de equilíbrio documentada e das composições registradas em `limites_superiores_positivos.json` e `V21_positivo_limite_superior.json`. Sua finalidade histórica foi testar se uma hipótese mais favorável ainda seria insuficiente. Não são saídas do Concretopy nem capacidades oficiais, e a contribuição de barras superiores nesses limites não integra a verificação positiva oficial.

## Registro anterior de flexão positiva — capacidades arquivadas e conferências auxiliares

74 das82 composições selecionadas apresentam capacidade calculada suficiente somente com as barras inferiores consideradas, nos dois cenários de concreto. São resultados de capacidade das composições registradas, sem dispensar a coerência documental/camadas, a verificação de outras faces ou as particularidades das transições. Quatro apresentam insuficiência demonstrada considerando também a camada oposta. Quatro dependem da altura ou da incidência real de barras/transições.

| Viga/trecho | Mk (tf·m) | Limite superior equivalente C35 (tf·m) | Limite superior equivalente C40 (tf·m) | Conclusão |
|---|---:|---:|---:|---|
| V16, modeloV16/vão1 | 15,28 | 6,97 | 7,03 | Insuficiente |
| V21, modeloV21/vão1 | 16,87 | 16,24 | 16,41 | Insuficiente |
| V25, modeloV25/vão4 | 7,50 | 5,21 | 5,24 | Insuficiente |
| V37, modeloV37/vão1 | 9,95 | 8,50 | 8,58 | Insuficiente |

Esses limites superiores são **maiores ou iguais à capacidade compatível com as hipóteses relaxadas**, não valores de MRd efetivo obtidos de uma análise completa de deformações. Comparar a demanda com um limite superior ainda insuficiente evita apresentar uma estimativa precisa como resistência real.

Composições e conferências:

- V16: N4 4Ø12,5 inferior e N1 4Ø10 central. N2/N3 de extremidade não alcançam o pico central. Mantida a insuficiência anterior; a camada oposta foi admitida em tração ou compressão no limite favorável.
- V21/primeiro vão: N2 2Ø20+N4 2Ø20 no pico; N3 2Ø10 superior. Foram excluídos os negativos de extremidade que não alcançam esse pico. A verificação apenas das inferiores coincide com Concretopy: equivalentes 16,08/16,30 tf·m em C35/C40. Admitir a contribuição superior de modo favorável leva somente aos limites equivalentes 16,24/16,41 tf·m, ainda abaixo de Mk=16,87 tf·m.
- V25/P727–P708: N11 1Ø12,5+N12 2Ø12,5 no pico e N13 2Ø10 superior. As barras intermediárias da região anterior terminam junto ao P727 e não foram deslocadas para este pico.
- V37: N4 2Ø20 contínuos e N5 2Ø10 superior no pico. N3 2Ø20 adicionais terminam antes do pico central; os negativos N2/N6 também não o alcançam.

A conferência independente usa equilíbrio normal e momentos: M=T·d+S·d′−(T+S)²/(2k), k=0,85fcd·b, com−As′fyd≤S≤As′fyd. S pode representar tração ou compressão; a compatibilidade de deformações é relaxada para produzir limite superior favorável. Os cálculos internos preservam suas unidades originais; os momentos apresentados foram convertidos para tf·m e para a base característica equivalente definida no início. O casoS=0 coincide com a API existente. Concretopy e seus métodos não foram modificados.

**Correções das leituras anteriores:** V18/segundo vão foi calculada com3Ø16 no pico, V30 com3Ø16 e V23/segundo vão com4Ø16. Os alertas produzidos pela quantidade menor de aço na triagem anterior não foram mantidos.

EmV42 foram usadas as alturas do detalhe nos trechos constantes:80/50/80/110/50/50/50cm. A positiva nos trechos de80/110cm atende ao cálculo com o aço externo considerado; a hipótese anteriorh50, que gerava alertas nesses trechos, foi retirada. Isso não elimina a divergência forma×detalhe do trechoh110 nem aprova a transição.

Os mínimos positivos foram calculados separadamente por Md,min=0,8W0fctk,sup e As≥0,0015Ac (verificações internas de cálculo; eventual momento mínimo apresentado segue Mk,min,eq=Md,min/γf). Um resultado favorável ao mínimo não compensa falha de resistência ao esforço solicitante.

## Histórico substituído — flexão negativa na face e armadura mínima

**Origem dos números:** a tabela de limites superiores desta seção é uma conferência algébrica independente do assistente, não a capacidade oficial do Concretopy. As consultas do motor são preservadas em `controles_independentes.json`, em `spans[].negative_faces`; não substituir sua saída por esses limites auxiliares. Mantêm-se as ressalvas de geometria e de posição das barras abaixo.

Foram calculadas136 consultas de extremidade nas composições legíveis:99 favoráveis às barras externas consideradas,13 com limite superior insuficiente e24 dependentes das posições intermediárias. Esses números não incluem as negativas ainda não definidas de todos os trechos variáveis. Também não são136 aprovações normativas de faces físicas.

A tabela seguinte conserva a demanda consultada **nas faces representadas no modelo TQS**. O resultado resistente para essa demanda está demonstrado; a associação com a face real deve ser compatibilizada quando a largura/referência do modelo diverge da documentação. Em particular, os apoios PC54C–PC60C deV21 exigem esclarecer a geometria/natureza física antes de converter todos esses resultados em reprovações na face real.

| Viga | Modelo/vão | Apoio consultado | Mk (tf·m) | Limite superior equivalente C35/C40 (tf·m) |
|---|---|---|---:|---:|
| V2 | V2/3 | P706 | 12,82 | 12,48/12,57 |
| V16 | V16/1 | PC41C | 11,99 | 10,97/11,07 |
| V21 | V21/1 | PC55C | 22,29 | 20,25/20,34 |
| V21 | V21/2 | PC55C | 21,96 | 20,25/20,34 |
| V21 | V21/4 | PC59C | 11,02 | 10,74/10,83 |
| V21 | V21/5 | PC59C | 11,12 | 10,74/10,83 |
| V21 | V21/5 | PC60C | 12,92 | 10,74/10,83 |
| V21 | V21/6 | PC60C | 12,50 | 10,74/10,83 |
| V18 | V18/1 | PC45C | 17,10 | 12,48/12,57 |
| V18 | V18/2 | PC45C | 16,20 | 12,48/12,57 |
| V33 | V33/1 | P794 | 15,89 | 8,48/8,56 |
| V37 | V37/1 | P725 | 16,92 | 10,78/10,87 |
| V40 | V40/1 | P796 | 15,53 | 8,48/8,56 |

V16/PC41C permanece insuficiente na face física já registrada. Sua conferência foi ampliada: a camada oposta pode estar em tração ou compressão, conforme o cenário. O limite equivalente agora é 10,97/11,07 tf·m, ainda abaixo de Mk=11,99 tf·m. O limite anteriorT·d isolado não deve ser usado como prova geral para os dois materiais, pois poderia omitir tração na camada oposta. A conclusão resistente é mantida pela prova ampliada.

**V29/V39 eV31/V41:** as3Ø16 estão em altura intermediária, abaixo das2Ø10 da face superior final. A análise anterior que as posicionava na face superior foi retirada. A positiva inferior e os controles independentes continuam calculados; a negativa/minimização envolvendo essa camada depende da altura real. Não foram classificadas automaticamente como vigas-parede apenas por terem165cm de altura.

Os mínimos negativos constam em cada cenário dos arquivos de cálculo e são exigidos somente onde existe tração correspondente. Uma camada externa isolada inferior ao mínimo não foi transformada em falta de aço se há armadura intermediária/pele cuja contribuição ainda depende da posição.

## Cortante, mínimos e espaçamentos

Todos os82 intervalos receberam consulta de cortante entre as faces do modelo e uma sensibilidade afastada2d dos apoios, quando há domínio suficiente. Foram calculados VRd2, área transversal requerida, mínimo e espaçamentos máximos longitudinal/transversal. A sensibilidade2d não constitui autorização genérica de redução de carga.

Em seções simples, d foi obtido das camadas externas. Em seções com barras intermediárias foram registrados limites de d: o valor externo isolado não é apresentado como a altura útil composta real. Um resultado favorável somente com esse valor não aprova o cortante composto. O limite inferior coloca uma área adicional deliberadamente generosa emd=0, sem inventar a posição das barras; falhar nesse limite conservador também não reprova a seção real.

Faixas variáveis de estribos são identificadas nos resultados deV4,V15,V17,V34,V37,V49,V50. A análise com a configuração mais fraca fornece um limite conservador, sem atribuir essa configuração a todo o vão nem emitir falha onde o estribo mais forte pode atuar. As transições mantêm sua verificação especial separada.

V16: mantidos o atendimento numérico ao cortante e aos espaçamentos máximos, com quatro ramosØ6,3c20 e anéis sobrepostos de22cm. V19/V20: cortante executado independentemente do conflito longitudinal, usando a menor altura útil das duas bitolas divergentes como referência conservadora; os cenários individuais foram preservados. O cenárioC40 não substitui a classeC35 aplicável à região quando esta está definida.

V21/primeiro vão: permanece o apontamento da rodada02, fornecido5,914cm²/m contra8,278/7,590cm²/m entre faces do modelo, ou6,797/6,109 na sensibilidade anterior d/2, emC35/C40. Fechar as condições de carga/apoio antes da conclusão integral sobre reduções.

O espaçamento mínimo por passagem do vibrador permanece uma única pendência executiva identificada ao final. Não foi usado mínimo de8cm do escritório. Número de ramos foi lido dos cortes; não foi imposto por preferência de largura.

## Coerência entre forma e cobertura das armaduras transversais

Os comprimentos da forma e as extensões cotadas de armadura foram tratados como dados independentes. A faixa de estribos foi usada para avaliar **cobertura da armadura**, nunca para fabricar o comprimento geométrico da viga.

| Viga | Vão livre obtido da forma(cm) | Soma de faixas transversais indicada(cm) | Cobertura não demonstrada(cm) |
|---|---:|---:|---:|
| V4 | 698,40 | 673,00 | 25,40 |
| V5 | 324,00 | 224,00 | 100,00 |
| V33 | 218,50 | 129,00 | 89,50 |
| V40 | 218,50 | 129,00 | 89,50 |

V4: forma7202 cota698,4; detalhe7401 faixas233+440. V5: forma7202 cadeia213,5+110,5; detalhe7401 faixa224. V33: forma7214 distância243,5 da face inferior deV19 ao eixoP794, menos raio25. V40: distância223,5 da face inferior do pilarPC49 ao eixoP796, mais20cm até a face da vigaV20, menos raio25. As duas últimas confrontam a faixa129 do detalhe7403.

Apontar necessidade de compatibilizar extensão/quantidade e cobertura integral; não escolher arbitrariamente uma extremidade para colocar a diferença. O registro não afirma que as faixas de estribos sejam cotas de geometria do detalhamento.

Mantidas as divergências já documentadas: V26/rótulos dos apoios; V3/V6 indicação geral inferior versusN1/corte; V22 indicação geral superior versusN1; V19/V20 indicação geral inferior versusN3/N4; V40: rótulo originalV19 já corrigido pela anotaçãoV20 na7403 atual; V42 altura110 versusrótulos80/50 na forma. “Indicação geral” substitui os termos ambíguos “resumo superior/inferior”.

## Suspensão — encontros verificados

Forma7214: V19/V20 eV33/V40 têm seção30×50 e faces superiores coincidentes em+8,88m. São encontros não pendurados; h_d=0, sem redução geométrica. A projeção deV33 emV19 está a35+365=400cm do eixoPC47C; V40 emV20 a35+364,5=399,5cm dePC49C. Os eixos das receptoras distam800cm e o vão livre é730cm.

Aplicou-se18.3.6 ao caso comprovado: pelo menos75% da área do tirante na receptora, em extensão máxima igual a sua altura,50cm. O75% não foi aplicado indiscriminadamente às demais ligações. A ferramenta histórica usa identificadores “engineer_confirmed”; nesta revisão a origem do critério é o texto normativo efetivamente consultado e a geometria acima, não uma confirmação fictícia de critério interno.

| Encontro | Rk total (tf) | Área mínima na receptora (cm²) | Limite superior de área disponível em 50 cm (cm²) | Resultado |
|---|---:|---:|---:|---|
| V33→V19 | 15,83 | 3,75 | 2,49 | Insuficiente |
| V40→V20 | 14,72 | 3,49 | 2,49 | Insuficiente |

A área disponível acima é um limite favorável: num intervalo de50cm com estribosØ6,3c15 há no máximo quatro estribos de dois ramos, totalizando2,494cm². Toda essa área foi atribuída à suspensão, sem reservar parcela ao cortante, e ainda assim é insuficiente. O verificador existente, com consulta regional do cortante, confirma a falha. A área necessária não depende da bitola longitudinal divergente deV19/V20.

As41 relações do modelo foram classificadas: cinco offsets aos próprios pilares; duas suspensões insuficientes acima;12 ligações dos PAR e10 interfaces de vigas-parede para análise separada; quatro ligações usuais com levantamento; oito ligações usuais com geometria/etapas a resolver. A situação de cada relação e a reação original estão em situacao_todas_ligacoes.json.

## Matriz das42 vigas usuais

A coluna positiva resume a capacidade das composições calculadas, sem aprovação global por essa coluna. As demais dependências estão nos registros individuais e na seção final.

| Viga | IntervalosTQS | Positiva | Negativa/particularidade principal |
|---|---:|---|---|
| V1 | 1 | Capacidade das configurações calculadas suficiente | Capacidade externa suficiente nas consultas realizadas |
| V2 | 3 | Capacidade das configurações calculadas suficiente | Insuficiência ao esforço consultado; verificar referências de face |
| V4 | 1 | Capacidade das configurações calculadas suficiente | Capacidade externa suficiente nas consultas realizadas |
| V5 | 1 | Capacidade das configurações calculadas suficiente | Capacidade externa suficiente nas consultas realizadas |
| V11 | 1 | Capacidade das configurações calculadas suficiente | Capacidade externa suficiente nas consultas realizadas |
| V14 | 3 | Capacidade das configurações calculadas suficiente | Capacidade externa suficiente nas consultas realizadas |
| V15 | 4 | Capacidade das configurações calculadas suficiente | Depende da altura intermediária nas seções indicadas |
| V16 | 1 | Insuficiência demonstrada | Insuficiência ao esforço consultado; verificar referências de face |
| V17 | 6 | Capacidade das configurações calculadas suficiente | Capacidade externa suficiente nas consultas realizadas |
| V18 | 2 | Capacidade das configurações calculadas suficiente | Insuficiência ao esforço consultado; verificar referências de face |
| V19 | 1 | Capacidade das configurações calculadas suficiente | Suspensão insuficiente; conflito longitudinal preservado |
| V20 | 1 | Capacidade das configurações calculadas suficiente | Suspensão insuficiente; conflito longitudinal preservado |
| V21 | 6 | Insuficiência demonstrada | Insuficiência ao esforço consultado; verificar referências de face |
| V22 | 2 | Capacidade das configurações calculadas suficiente | Capacidade externa suficiente nas consultas realizadas |
| V23 | 2 | Capacidade das configurações calculadas suficiente | Faces/alturas variáveis nas dúvidas finais |
| V24 | 4 | Dependência específica no fim | Capacidade externa suficiente nas consultas realizadas |
| V25 | 4 | Insuficiência demonstrada | Depende da altura intermediária nas seções indicadas |
| V26 | 3 | Capacidade das configurações calculadas suficiente | Capacidade externa suficiente nas consultas realizadas |
| V27 | 1 | Capacidade das configurações calculadas suficiente | Capacidade externa suficiente nas consultas realizadas |
| V28 | 2 | Capacidade das configurações calculadas suficiente | Depende da altura intermediária nas seções indicadas |
| V29 | 1 | Capacidade das configurações calculadas suficiente | Ø16 intermediárias: leitura externa anterior retirada |
| V30 | 1 | Capacidade das configurações calculadas suficiente | Depende da altura intermediária nas seções indicadas |
| V31 | 1 | Capacidade das configurações calculadas suficiente | Ø16 intermediárias: leitura externa anterior retirada |
| V32 | 2 | Capacidade das configurações calculadas suficiente | Depende da altura intermediária nas seções indicadas |
| V33 | 1 | Capacidade das configurações calculadas suficiente | Insuficiência ao esforço consultado; verificar referências de face |
| V34 | 1 | Capacidade das configurações calculadas suficiente | Depende da altura intermediária nas seções indicadas |
| V35 | 2 | Dependência específica no fim | Depende da altura intermediária nas seções indicadas |
| V36 | 1 | Capacidade das configurações calculadas suficiente | Depende da altura intermediária nas seções indicadas |
| V37 | 1 | Insuficiência demonstrada | Insuficiência ao esforço consultado; verificar referências de face |
| V38 | 1 | Capacidade das configurações calculadas suficiente | Capacidade externa suficiente nas consultas realizadas |
| V39 | 1 | Capacidade das configurações calculadas suficiente | Ø16 intermediárias: leitura externa anterior retirada |
| V40 | 1 | Capacidade das configurações calculadas suficiente | Insuficiência ao esforço consultado; verificar referências de face |
| V41 | 1 | Capacidade das configurações calculadas suficiente | Ø16 intermediárias: leitura externa anterior retirada |
| V42 | 7 | Capacidade das configurações calculadas suficiente | Faces/alturas variáveis nas dúvidas finais |
| V43 | 4 | Capacidade das configurações calculadas suficiente | Depende da altura intermediária nas seções indicadas |
| V44 | 1 | Capacidade das configurações calculadas suficiente | Depende da altura intermediária nas seções indicadas |
| V45 | 1 | Capacidade das configurações calculadas suficiente | Capacidade externa suficiente nas consultas realizadas |
| V46 | 1 | Capacidade das configurações calculadas suficiente | Capacidade externa suficiente nas consultas realizadas |
| V47 | 1 | Capacidade das configurações calculadas suficiente | Capacidade externa suficiente nas consultas realizadas |
| V48 | 1 | Capacidade das configurações calculadas suficiente | Depende da altura intermediária nas seções indicadas |
| V49 | 1 | Dependência específica no fim | Faces/alturas variáveis nas dúvidas finais |
| V50 | 1 | Dependência específica no fim | Faces/alturas variáveis nas dúvidas finais |

## Dúvidas finais para avaliação de João — motivo e alcance

Os itens abaixo não suspendem os resultados independentes já apresentados. “Não resolvido” não significa informação comprovadamente ausente na prancha; quando a leitura/compatibilização ainda não permite uma associação segura, isso é dito expressamente.

### Q01 — V35, V49, V50

Altura física das barras intermediárias no pico: V35 N3/N7; V49/V50 N8. Manter a posição da primeira concretagem, sem deslocá-la à camada inferior.

**Por que afeta a conclusão:** As barras inferiores isoladas não bastam, mas uma contribuição real intermediária pode alterar a conclusão.

### Q02 — V4, V5, V11, V14, V15, V25, V26, V28, V29, V30, V31, V32, V34, V35, V36, V38, V39, V41, V43, V44, V45, V46, V47, V48

Coordenadas verticais/camadas das barras intermediárias e de pele nas seções dependentes, incluindo N7/N4 emV29/V39 e N6/N2 emV31/V41.

**Por que afeta a conclusão:** A altura útil não pode ser a da face externa quando a resultante inclui armadura intermediária; C35/C40 já estão considerados, sem hipótese uniforme arbitrária.

### Q03 — V23, V24, V42, V49, V50

Fechar incidência dos degraus e barras que atravessam cada face: V24 junto aP769; V42 junto aP791/P784; V49/V50 na mudança50/87. ParaV49 a forma já indica130cm no trecho alto.

**Por que afeta a conclusão:** As seções constantes identificadas foram calculadas; a transição e as barras em outra altura não podem ser substituídas por seção média ou falsa camada externa.

### Q04 — V19, V20, V22, V26

Definir representação vigente onde resumo da elevação diverge das posições/cortes ou os apoios divergem da forma.

**Por que afeta a conclusão:** Foram preservados cálculos pelos dados legíveis e verificações independentes; falta documental não foi tratada como aço fisicamente ausente.

### Q05 — V17, V35, V36

Caminho de carga/ligação para os sinais invertidos nos quatro encontros normais listados em situacao_todas_ligacoes.json.

**Por que afeta a conclusão:** Não aplicar tirante de reação descendente a levantamento.

### Q06 — V14, V18, V21, V28, V32, V49, V50, V26

Resolver os oito encontros individualizados em situacao_todas_ligacoes.json, com domínio físico, geometria e altura útil onde a concretagem por etapas interfere.

**Por que afeta a conclusão:** Evita usar trecho de outra viga, truncar região normativa ou somar estribos de duas etapas como se todos atravessassem a seção final.

### Q07 — all usual beams

Diâmetro/equipamento de vibração ou critério executivo documentado de passagem/adensamento.

**Por que afeta a conclusão:** 18.3.3.2 exige passagem do vibrador; não se aplicou mínimo interno fixo de8cm.

### Q08 — V21

Natureza e faces efetivas dos apoios PC54C–PC60C e hipóteses das reduções de cortante; registrar diferença entre faces físicas e larguras da discretizaçãoTQS.

**Por que afeta a conclusão:** A capacidade ao esforço consultado foi calculada, mas as faces de19cm do modelo não constituem por si prova da geometria real.

### Ligações usuais ainda dependentes — individualização

- **V14→V43:** Recebimento próximo a extremidade/trecho de seção30x50 com barras intermediárias; vincular região normativa completa ao trecho real e sua altura útil composta.
- **V17→V23:** Reação de levantamento na envoltória: procedimento de suspensão para reação descendente não representa o mecanismo. Definir transferência/ligação para o sinal invertido.
- **V17→V42:** Reação de levantamento na envoltória: procedimento de suspensão para reação descendente não representa o mecanismo. Definir transferência/ligação para o sinal invertido.
- **V18→V23:** Receptora V23 tem mudança80/50 e desníveis; classificar a altura no encontro e redução geométrica de18.3.6, sem aplicar75% indiscriminadamente.
- **V21→V22:** Encontro no trecho curvo/balanço junto aPC62C; região normativa pode alcançar apoio/limite de vão. Fixar domínio contínuo real sem truncá-lo.
- **V28→V15:** Viga apoiada com mudança de direção e receptora em concretagem por etapas; projetar eixo do encontro e comprovar altura útil composta deV15.
- **V32→V15:** Viga apoiada com mudança de direção e receptora em concretagem por etapas; projetar eixo do encontro e comprovar altura útil composta deV15.
- **V35→V15:** Reação de levantamento na envoltória: procedimento de suspensão para reação descendente não representa o mecanismo. Definir transferência/ligação para o sinal invertido.
- **V36→V5:** Reação de levantamento na envoltória: procedimento de suspensão para reação descendente não representa o mecanismo. Definir transferência/ligação para o sinal invertido.
- **V49→V26:** Receptora curva19x50 e posição de primeira etapa; conferir eixo do recebimento/continuidade do intervalo de50cm e altura da armadura intermediária.
- **V50→V34:** Receptora40x50 com três faixas de estribos e primeira etapa; posicionar encontro na faixa correta e fornecer a altura das barras intermediárias.
- **V26→V25:** Rótulos de apoios deV26 divergentes e encontro terminal na viga de borda; confirmar relação física de transferência antes de dimensionar no receptor errado.

Vigas-parede separadas conforme orientação: V3,V6,V7–V10,V12,V13 e os nove PAR. As interfaces com receptoras usuais foram inventariadas com as reações; a compatibilização do nó deve integrar a análise especial correspondente.

## Rastreabilidade e limites da entrega

A origem do resultado deve ser distinguida em cada controle: chamadas efetivas ao Concretopy e seus registros brutos são a referência oficial; verificações algébricas, contagens e limites independentes são auxiliares identificados. Esta atualização não transforma controles sem execução do motor em verificações oficiais concluídas. Registro da tabela positiva: `resultados_oficiais_concretopy_positiva.json`.

Os dados completos constam em controles_independentes.json, matriz_cobertura_rodada_03.json, suspensao_V19_V20.json, limites_superiores_positivos.json, V21_positivo_limite_superior.json, cobertura_transversal_forma_detalhe.json e duvidas_finais_engenheiro.json. O procedimento operacional obrigatório foi novamente executado para o pavimento e para as novas verificações independentes deV19/V20, com resumo em resultado_operacional_resumido.json. O resultado completo e os scripts permanecem no diretório de trabalho.

**Não há aprovação global do pavimento.** Há falhas demonstradas e conclusões de capacidade para os dados registrados; os controles dependentes estão individualizados, sem serem classificados genericamente como falta de todas as verificações. Nenhum original TQS/PDF ou método do Concretopy foi alterado.

## Atualização documental detectada na conferência final

A7403 foi salva com novas anotações em15/10/2026 às11h25. A anotaçãoV20 corrige o apoio deV40; esse rótulo não permanece como dúvida aberta. O arquivo PDF tem nova assinatura, mas os17recortes de detalhamento, renderizados sem anotações, são idênticos pixel a pixel aos usados na análise. Não houve mudança identificada de geometria ou armaduras nesses recortes; os cálculos permanecem válidos. Registro:atualizacao_anotacao_7403.json e comparacao_visual_7403.json. Os demais cinco PDFs mantêm suas assinaturas e o TQS permanece estável.
