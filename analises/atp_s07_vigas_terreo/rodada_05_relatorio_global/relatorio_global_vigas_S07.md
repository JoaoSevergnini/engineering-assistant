# ATP S07 - Vigas do térreo - Relatório global de verificações

Emissão: 16/10/2026 - correcao dos negativos por lado. Abrangência: V1 a V50. Resultado principal: C35 uniforme na seção final, por simplificação confirmada por João. Elementos PAR excluídos.

Este relatório apresenta os cálculos de seção e as verificações físicas efetivamente executadas. Não representa aprovação global das 50 vigas. A conferência integral das cotas de todos os vãos e das regiões de seção variável ainda não foi encerrada. Esses itens são trabalhos de leitura/associação do assistente, e não informações que se demonstrou estarem ausentes no projeto.

## 1. Critérios adotados

Norma: ABNT NBR 6118: 2023, exemplar disponibilizado em DOCUMENTACAO ATP. Consultados os itens 17.3.5.2.1 (mínimos longitudinais),17.4.1.2.1 (consulta de cortante junto ao apoio direto),17.4.2 (cortante) e 18.3.6 (suspensão). Não foram aplicados critérios internos do escritório como causa de reprovação.

Solicitações características em tf e tf·m. Resistência equivalente para comparação: MRd/γf, expressa em tf·m; não é resistência característica da seção. Mantidos γf=1,4,γc=1,4 e γs=1,15 neste modelo. Conversão: 1 tf=9,80665 kN. Armaduras em cm² e cm²/m; dimensões em cm, salvo indicação.

Motor oficial: Concretopy, função verificar_flexao_viga_retangular para flexão e API pública de cortante por meio dedesign_shear. O arquivo verificacoes_globais_concretopy.json preserva entradas, coeficientes, saídas brutas e fonte dos esforços. Suspensão: suspension_review.review_connection, com tensão de aço e parcela de cortante fornecidas pelo Concretopy. A combinação conservadora das sobreposições V29/V39 é identificada como pós-processamento dos resultados, sem nova resistência independente.

Cobrimento 3,5 cm; agregado 16 mm; vibrador 4 cm. Consideradas somente as armaduras externas inferior/superior da seção final. Barras no topo da primeira concretagem excluídas de resistência e de d. Na positiva não foi considerada contribuição da armadura superior. d resulta das camadas e do centroide retornado pelo Concretopy. Na negativa, selecionado o maximo de CADA lado do apoio, no proprio trecho. Fim do vao anterior e inicio do seguinte usam solicitacoes e armaduras proprias, mesmo no mesmo pilar. Sem unificar os valores e sem reducao para a face interna.

Nos conflitos elevação versus marcas/cortes, adotadas marcas/cortes conforme confirmação de João; divergências registradas. Anotações nos PDFs são propostas de correção e não substituem o desenho original. V3, V6, V7-V10, V12, V13 incluídas no cálculo convencional de viga, sem avaliação dos critérios próprios de viga-parede. Esse recorte não valida o comportamento especial desses elementos.

## 2. Documentos e cobertura

| Documento | Revisão/função |
| --- | --- |
| 7201 | R03 - blocos, dimensões, posição dos pilares e níveis NB |
| 7202 | R03 - forma térreo, parte 1 |
| 7214 | R01 - forma térreo, parte 2; região verde+8,88 m |
| 7401 | R00 - detalhamento V1-V20 |
| 7402 | R00 - detalhamento V21-V32 e V39 |
| 7403 | R01 - detalhamento V33-V38 e V40-V50 |
| 7404 | Elementos PAR; fora do escopo |
| VGESFS/RELDTVGS | Modelo atualizado; 66 registros/605 séries conferidas, sem diferença numérica entre listagens |


Inventário nominal: V1-V50 presentes nas formas e no detalhamento. Calculados 95 intervalos do modelo,190 consultas negativas e 102 faixas de cortante. Esses intervalos não equivalem automaticamente a 95 vãos físicos; V31/V41 têm subdivisões junto ao mesmo apoio e V43 possui balanço. Foram conciliados 23 domínios completos de faixa com faces de blocos/pilares, além da face PC55C no primeiro trecho da V21; os demais conservam a referência do modelo e não encerram a verificação física da faixa.

Os máximos positivos de cada intervalo foram comparados à composição indicada no ponto crítico. Essa comparação não verifica automaticamente todas as interrupções de barras. Escalonamento, ancoragem, torção e estados de serviço não integram esta emissão limitada aos controles solicitados.

Cotas confirmadas: P791+8,88 m; V49 com topo local+9,55 m quando indicado; não aplicar correção única de nível a todo o pavimento. P756/P761: NB8,38 m correto; na V15 o fundo 8,68 m fica acima dos blocos. O nome 2 a FASE identifica etapa do ATP, não etapa de carregamento ou concretagem.

## 3. Resultados que exigem atenção

Flexão positiva insuficiente nas seções de V16, V21(primeiro intervalo), V25(P727-P708), V35(primeiro intervalo) e V37. Tambem insuficientes V24(P778-P769), V49 e V50 nos trechos de 50 cm. As mudancas de altura de V49/V50 foram localizadas pela cota 130 cm; os trechos 87 cm atendem. Total: oito vigas com pelo menos uma secao positiva insuficiente.

Cortante: C35, insuficiência mantida nas V18 e V35. V21 junto ao PC55C e V37 junto ao P725 atendem usando a consulta a d/2, após confirmação expressa das condições de carga e apoio por João. V4, V5, V15, V33, V40, V47 atendem nas faixas recalculadas com as faces pertinentes. V36/V48 não têm déficit de mínimo no cenário principal C35. V49/V50 usamØ6,3 c/10 da peça externa, não c/20 da primeira etapa.

Suspensão: V33 sobre V19 e V40 sobre V20 não atendem. As demais ligações têm situação discriminada na seção 5; reação ascendente não foi tratada como tirante descendente. Nas ligacoes V31-V12 e V41-V13 o sentido foi corrigido por confirmacao de Joao. As outras quatro interfaces com sinal negativo foram reservadas por Joao para analise separada com casos de gravidade e vento. V49 apoia diretamente no PC21C e nao exige suspensao em V26.

Na ligacao V41→V13, a distribuicao uniforme 75/25 nao atende: receptora 11,05 cm²/m contra 10,05 cm²/m; apoiada 5,06 cm²/m contra 3,67 cm²/m. Este e o resultado da distribuicao verificada; outras distribuicoes admissiveis nao foram avaliadas. V31→V12 atende numericamente essa reparticao. Estribos compostos condicionam a conclusao de ambas.

Correcao dos negativos por lado: 190 comparacoes auditadas,45 solicitacoes corrigidas e 14 extremidades que passam a atender a capacidade em C35. Comparacoes refeitas com as resistencias oficiais Concretopy arquivadas, sem nova execucao resistente porque secao, armadura e materiais nao mudaram. Essa mudanca nao aprova automaticamente minimos ou os demais controles. Na V43/P723,3/D=8,697 tf·m e 4/E=12,707 tf·m; capacidade 8,216 tf·m em cada lado: ambos insuficientes.

Negativas: os valores e as insuficiências aparecem por apoio nas fichas. Casos com diferença inferior a 0,01 tf·m permanecem decididos com precisão integral; o arredondamento das tabelas não altera o resultado.

## 4. Quadro por viga

| Viga | Positiva | Negativa | Mínimos | Cortante | Suspensão |
| --- | --- | --- | --- | --- | --- |
| V1 | ATENDE SEÇÃO | ATENDE SEÇÃO | ATENDE NAS SEÇÕES SOLICITADAS | ATENDE CÁLCULO; GEOMETRIA PENDENTE | SEM LIGAÇÃO NO INVENTÁRIO |
| V2 | ATENDE SEÇÃO | INSUFICIENTE | ATENDE NAS SEÇÕES SOLICITADAS | ATENDE CÁLCULO; GEOMETRIA PENDENTE | SEM LIGAÇÃO NO INVENTÁRIO |
| V3 | ATENDE SEÇÃO | ATENDE SEÇÃO | REVER MÍNIMO | ATENDE CÁLCULO; GEOMETRIA PENDENTE | SEM LIGAÇÃO NO INVENTÁRIO |
| V4 | ATENDE SEÇÃO | ATENDE SEÇÃO | ATENDE NAS SEÇÕES SOLICITADAS | ATENDE FAIXAS CALCULADAS | SEM LIGAÇÃO NO INVENTÁRIO |
| V5 | ATENDE SEÇÃO | INSUFICIENTE | ATENDE NAS SEÇÕES SOLICITADAS | ATENDE FAIXAS CALCULADAS | PENDENTE NAS LIGAÇÕES |
| V6 | ATENDE SEÇÃO | ATENDE SEÇÃO | REVER MÍNIMO | ATENDE CÁLCULO; GEOMETRIA PENDENTE | SEM LIGAÇÃO NO INVENTÁRIO |
| V7 | ATENDE SEÇÃO | ATENDE SEÇÃO | REVER MÍNIMO | ATENDE CÁLCULO; GEOMETRIA PENDENTE | PENDENTE NAS LIGAÇÕES |
| V8 | ATENDE SEÇÃO | ATENDE SEÇÃO | REVER MÍNIMO | ATENDE CÁLCULO; GEOMETRIA PENDENTE | PENDENTE NAS LIGAÇÕES |
| V9 | ATENDE SEÇÃO | ATENDE SEÇÃO | REVER MÍNIMO | ATENDE CÁLCULO; GEOMETRIA PENDENTE | PENDENTE NAS LIGAÇÕES |
| V10 | ATENDE SEÇÃO | ATENDE SEÇÃO | REVER MÍNIMO | ATENDE CÁLCULO; GEOMETRIA PENDENTE | PENDENTE NAS LIGAÇÕES |
| V11 | ATENDE SEÇÃO | ATENDE SEÇÃO | REVER MÍNIMO | ATENDE CÁLCULO; GEOMETRIA PENDENTE | SEM LIGAÇÃO NO INVENTÁRIO |
| V12 | SEM MOMENTO POSITIVO | INSUFICIENTE | REVER MÍNIMO | ATENDE CÁLCULO; GEOMETRIA PENDENTE | PENDENTE NAS LIGAÇÕES |
| V13 | SEM MOMENTO POSITIVO | INSUFICIENTE | REVER MÍNIMO | ATENDE CÁLCULO; GEOMETRIA PENDENTE | NÃO ATENDE |
| V14 | ATENDE SEÇÃO | ATENDE SEÇÃO | ATENDE NAS SEÇÕES SOLICITADAS | ATENDE CÁLCULO; GEOMETRIA PENDENTE | ATENDE LIGAÇÕES |
| V15 | ATENDE SEÇÃO | INSUFICIENTE | ATENDE NAS SEÇÕES SOLICITADAS | ATENDE FAIXAS CALCULADAS | PENDENTE NAS LIGAÇÕES |
| V16 | INSUFICIENTE | INSUFICIENTE | ATENDE NAS SEÇÕES SOLICITADAS | ATENDE FAIXAS CALCULADAS | SEM LIGAÇÃO NO INVENTÁRIO |
| V17 | ATENDE SEÇÃO | ATENDE SEÇÃO | ATENDE NAS SEÇÕES SOLICITADAS | ATENDE CÁLCULO; GEOMETRIA PENDENTE | PENDENTE NAS LIGAÇÕES |
| V18 | ATENDE SEÇÃO | INSUFICIENTE | ATENDE NAS SEÇÕES SOLICITADAS | INSUFICIENTE | ATENDE LIGAÇÕES |
| V19 | ATENDE SEÇÃO | INSUFICIENTE | ATENDE NAS SEÇÕES SOLICITADAS | ATENDE CÁLCULO; GEOMETRIA PENDENTE | NÃO ATENDE |
| V20 | ATENDE SEÇÃO | INSUFICIENTE | ATENDE NAS SEÇÕES SOLICITADAS | ATENDE CÁLCULO; GEOMETRIA PENDENTE | NÃO ATENDE |
| V21 | INSUFICIENTE | INSUFICIENTE | ATENDE NAS SEÇÕES SOLICITADAS | ATENDE CÁLCULO; GEOMETRIA PENDENTE | PENDENTE NAS LIGAÇÕES |
| V22 | ATENDE SEÇÃO | ATENDE SEÇÃO | ATENDE NAS SEÇÕES SOLICITADAS | ATENDE CÁLCULO; GEOMETRIA PENDENTE | PENDENTE NAS LIGAÇÕES |
| V23 | ATENDE SEÇÃO | INSUFICIENTE | ATENDE NAS SEÇÕES SOLICITADAS | ATENDE CÁLCULO; GEOMETRIA PENDENTE | PENDENTE NAS LIGAÇÕES |
| V24 | INSUFICIENTE | INSUFICIENTE | ATENDE NAS SEÇÕES SOLICITADAS | ATENDE CÁLCULO; GEOMETRIA PENDENTE | SEM LIGAÇÃO NO INVENTÁRIO |
| V25 | INSUFICIENTE | INSUFICIENTE | ATENDE NAS SEÇÕES SOLICITADAS | ATENDE CÁLCULO; GEOMETRIA PENDENTE | ATENDE LIGAÇÕES |
| V26 | ATENDE SEÇÃO | ATENDE SEÇÃO | ATENDE NAS SEÇÕES SOLICITADAS | ATENDE CÁLCULO; GEOMETRIA PENDENTE | ATENDE LIGAÇÕES |
| V27 | ATENDE SEÇÃO | ATENDE SEÇÃO | ATENDE NAS SEÇÕES SOLICITADAS | ATENDE CÁLCULO; GEOMETRIA PENDENTE | SEM LIGAÇÃO NO INVENTÁRIO |
| V28 | ATENDE SEÇÃO | INSUFICIENTE | ATENDE NAS SEÇÕES SOLICITADAS | ATENDE CÁLCULO; GEOMETRIA PENDENTE | ATENDE LIGAÇÕES |
| V29 | ATENDE SEÇÃO | ATENDE SEÇÃO | REVER MÍNIMO | ATENDE CÁLCULO; GEOMETRIA PENDENTE | PENDENTE NAS LIGAÇÕES |
| V30 | ATENDE SEÇÃO | INSUFICIENTE | ATENDE NAS SEÇÕES SOLICITADAS | ATENDE CÁLCULO; GEOMETRIA PENDENTE | SEM LIGAÇÃO NO INVENTÁRIO |
| V31 | ATENDE SEÇÃO | INSUFICIENTE | REVER MÍNIMO | ATENDE CÁLCULO; GEOMETRIA PENDENTE | PENDENTE NAS LIGAÇÕES |
| V32 | ATENDE SEÇÃO | INSUFICIENTE | ATENDE NAS SEÇÕES SOLICITADAS | ATENDE CÁLCULO; GEOMETRIA PENDENTE | PENDENTE NAS LIGAÇÕES |
| V33 | ATENDE SEÇÃO | INSUFICIENTE | ATENDE NAS SEÇÕES SOLICITADAS | ATENDE FAIXAS CALCULADAS | NÃO ATENDE |
| V34 | ATENDE SEÇÃO | INSUFICIENTE | ATENDE NAS SEÇÕES SOLICITADAS | ATENDE FAIXAS CALCULADAS | PENDENTE NAS LIGAÇÕES |
| V35 | INSUFICIENTE | INSUFICIENTE | ATENDE NAS SEÇÕES SOLICITADAS | INSUFICIENTE | PENDENTE NAS LIGAÇÕES |
| V36 | ATENDE SEÇÃO | INSUFICIENTE | REVER MÍNIMO | ATENDE FAIXAS CALCULADAS | PENDENTE NAS LIGAÇÕES |
| V37 | INSUFICIENTE | INSUFICIENTE | ATENDE NAS SEÇÕES SOLICITADAS | ATENDE FAIXAS CALCULADAS | SEM LIGAÇÃO NO INVENTÁRIO |
| V38 | ATENDE SEÇÃO | ATENDE SEÇÃO | ATENDE NAS SEÇÕES SOLICITADAS | ATENDE CÁLCULO; GEOMETRIA PENDENTE | SEM LIGAÇÃO NO INVENTÁRIO |
| V39 | ATENDE SEÇÃO | ATENDE SEÇÃO | REVER MÍNIMO | ATENDE CÁLCULO; GEOMETRIA PENDENTE | PENDENTE NAS LIGAÇÕES |
| V40 | ATENDE SEÇÃO | INSUFICIENTE | ATENDE NAS SEÇÕES SOLICITADAS | ATENDE FAIXAS CALCULADAS | NÃO ATENDE |
| V41 | ATENDE SEÇÃO | ATENDE SEÇÃO | REVER MÍNIMO | ATENDE CÁLCULO; GEOMETRIA PENDENTE | NÃO ATENDE |
| V42 | ATENDE SEÇÃO | INSUFICIENTE | ATENDE NAS SEÇÕES SOLICITADAS | ATENDE CÁLCULO; GEOMETRIA PENDENTE | PENDENTE NAS LIGAÇÕES |
| V43 | ATENDE SEÇÃO | INSUFICIENTE | ATENDE NAS SEÇÕES SOLICITADAS | ATENDE CÁLCULO; GEOMETRIA PENDENTE | ATENDE LIGAÇÕES |
| V44 | ATENDE SEÇÃO | INSUFICIENTE | ATENDE NAS SEÇÕES SOLICITADAS | ATENDE CÁLCULO; GEOMETRIA PENDENTE | SEM LIGAÇÃO NO INVENTÁRIO |
| V45 | ATENDE SEÇÃO | ATENDE SEÇÃO | ATENDE NAS SEÇÕES SOLICITADAS | ATENDE CÁLCULO; GEOMETRIA PENDENTE | SEM LIGAÇÃO NO INVENTÁRIO |
| V46 | ATENDE SEÇÃO | ATENDE SEÇÃO | ATENDE NAS SEÇÕES SOLICITADAS | ATENDE CÁLCULO; GEOMETRIA PENDENTE | SEM LIGAÇÃO NO INVENTÁRIO |
| V47 | ATENDE SEÇÃO | INSUFICIENTE | ATENDE NAS SEÇÕES SOLICITADAS | ATENDE FAIXAS CALCULADAS | SEM LIGAÇÃO NO INVENTÁRIO |
| V48 | ATENDE SEÇÃO | INSUFICIENTE | ATENDE NAS SEÇÕES SOLICITADAS | ATENDE FAIXAS CALCULADAS | SEM LIGAÇÃO NO INVENTÁRIO |
| V49 | INSUFICIENTE | ATENDE SEÇÃO | REVER MÍNIMO | ATENDE CÁLCULO; GEOMETRIA PENDENTE | ATENDE LIGAÇÕES |
| V50 | INSUFICIENTE | ATENDE SEÇÃO | REVER MÍNIMO | ATENDE CÁLCULO; GEOMETRIA PENDENTE | PENDENTE NAS LIGAÇÕES |


## 5. Ligações entre vigas

Sinal da reacao: positiva descendente conforme o papel fisico validado. Nas V31-V12 e V41-V13 os valores apresentados sao os opostos das reacoes originalmente negativas na listagem TQS, por acao-reacao confirmada por Joao. Nas outras quatro interfaces de sinal negativo, os nomes sao os papeis originais TQS e o sentido fisico fica para analise separada de Joao. Rmín/Rmáx são os extremos característicos da viga apoiada sobre a receptora. Não são reações dos pilares da receptora. A área para 100% da força, quando arquivada, é apenas referência de transferência e não a armadura final de suspensão.

| Apoiada→receptora | Rmín(tf) | Rmáx(tf) | Situação |
| --- | --- | --- | --- |
| V7→V29 | 5,22 | 10,61 | AREA ATENDE; FECHAMENTO DOS ESTRIBOS A VERIFICAR |
| V7→V31 | 2,90 | 7,64 | AREA ATENDE; FECHAMENTO DOS ESTRIBOS A VERIFICAR |
| V8→V39 | 4,30 | 9,67 | AREA ATENDE; FECHAMENTO DOS ESTRIBOS A VERIFICAR |
| V8→V41 | 2,95 | 7,71 | AREA ATENDE; FECHAMENTO DOS ESTRIBOS A VERIFICAR |
| V9→V29 | 4,82 | 9,74 | AREA ATENDE; FECHAMENTO DOS ESTRIBOS A VERIFICAR |
| V9→V31 | 4,56 | 9,31 | AREA ATENDE; FECHAMENTO DOS ESTRIBOS A VERIFICAR |
| V10→V39 | 4,54 | 9,54 | AREA ATENDE; FECHAMENTO DOS ESTRIBOS A VERIFICAR |
| V10→V41 | 4,30 | 9,12 | AREA ATENDE; FECHAMENTO DOS ESTRIBOS A VERIFICAR |
| V31→V12 | 14,64 | 24,46 | AREA ATENDE; FECHAMENTO DOS ESTRIBOS A VERIFICAR |
| V41→V13 | 19,31 | 30,52 | DISTRIBUICAO UNIFORME NAO ATENDE |
| V14→V43 | 0,32 | 0,39 | ATENDE |
| V17→V23 | -3,33 | -2,10 | SENTIDO DA TRANSFERENCIA: ANALISE DE JOAO |
| V17→V42 | -0,55 | -0,22 | SENTIDO DA TRANSFERENCIA: ANALISE DE JOAO |
| V18→V23 | 3,59 | 5,28 | ATENDE |
| V21→V22 | 2,94 | 3,47 | TIRANTE INTEGRAL A COMPROVAR |
| V28→V15 | 5,75 | 7,56 | ATENDE |
| V32→V15 | 6,36 | 10,29 | TIRANTE INTEGRAL A COMPROVAR |
| V33→V19 | 12,98 | 15,83 | INSUFICIENTE |
| V35→V15 | -1,08 | 0,85 | SENTIDO DA TRANSFERENCIA: ANALISE DE JOAO |
| V36→V5 | -13,65 | -11,11 | SENTIDO DA TRANSFERENCIA: ANALISE DE JOAO |
| V40→V20 | 12,22 | 14,72 | INSUFICIENTE |
| V49→V26 | 6,28 | 6,82 | APOIO DIRETO PC21C; SUSPENSAO NAO SE APLICA |
| V50→V34 | 11,44 | 12,56 | TIRANTE INTEGRAL A COMPROVAR |
| V26→V25 | 0,38 | 0,39 | ATENDE |


**V7→V29: ** Calculo individual executado com d do centroide Concretopy. Pecas de estribo 138/50 cm exigem comprovar funcionamento e ancoragem conjunta. Regioes de suspensao se sobrepoem em 0,43 m; combinacao conservadora registrada separadamente.

**V7→V31: ** Posicao do cruzamento comprovada pelas cotas da forma, fora da extremidade. Area avaliada com diagrama TQS regional, S1 no eixo V12/V13 confirmado por Joao, sem reescalonamento. Resta comprovar funcionamento/ancoragem conjunta dos estribos 50/138 cm. Sobreposicoes tratadas por soma conservadora separada.

**V8→V39: ** Calculo individual executado com d do centroide Concretopy. Pecas de estribo 138/50 cm exigem comprovar funcionamento e ancoragem conjunta. Regioes de suspensao se sobrepoem em 0,43 m; combinacao conservadora registrada separadamente.

**V8→V41: ** Posicao do cruzamento comprovada pelas cotas da forma, fora da extremidade. Area avaliada com diagrama TQS regional, S1 no eixo V12/V13 confirmado por Joao, sem reescalonamento. Resta comprovar funcionamento/ancoragem conjunta dos estribos 50/138 cm. Sobreposicoes tratadas por soma conservadora separada.

**V9→V29: ** Calculo individual executado com d do centroide Concretopy. Pecas de estribo 138/50 cm exigem comprovar funcionamento e ancoragem conjunta. Regioes de suspensao se sobrepoem em 0,43 m; combinacao conservadora registrada separadamente.

**V9→V31: ** Posicao do cruzamento comprovada pelas cotas da forma, fora da extremidade. Area avaliada com diagrama TQS regional, S1 no eixo V12/V13 confirmado por Joao, sem reescalonamento. Resta comprovar funcionamento/ancoragem conjunta dos estribos 50/138 cm. Sobreposicoes tratadas por soma conservadora separada.

**V10→V39: ** Calculo individual executado com d do centroide Concretopy. Pecas de estribo 138/50 cm exigem comprovar funcionamento e ancoragem conjunta. Regioes de suspensao se sobrepoem em 0,43 m; combinacao conservadora registrada separadamente.

**V10→V41: ** Posicao do cruzamento comprovada pelas cotas da forma, fora da extremidade. Area avaliada com diagrama TQS regional, S1 no eixo V12/V13 confirmado por Joao, sem reescalonamento. Resta comprovar funcionamento/ancoragem conjunta dos estribos 50/138 cm. Sobreposicoes tratadas por soma conservadora separada.

**V31→V12: ** Sentido de transferencia confirmado por Joao. Receptora V12: regiao unilateral 82,5 cm, cortante regional obtido das series TQS, origem no eixo confirmado. Area atende com 75% na receptora e 25% na apoiada, incluindo contagem minima de estribos. Atendimento numerico=True. Falta demonstrar fechamento/ancoragem conjunta das pecas 138/50 cm pelo detalhe recebido; nao foi presumido detalhe complementar.

**V41→V13: ** Sentido de transferencia confirmado por Joao. Receptora V13: regiao unilateral 82,5 cm, cortante regional obtido das series TQS, origem no eixo confirmado. Reparticao uniforme 75/25 nao atende em pelo menos um dos elementos, somando o cortante regional. Esse resultado nao demonstra sozinho impossibilidade de outra distribuicao admissivel; consultar parcelas no registro bruto. Atendimento numerico=False. Falta demonstrar fechamento/ancoragem conjunta das pecas 138/50 cm pelo detalhe recebido; nao foi presumido detalhe complementar.

**V14→V43: ** Regiao unilateral de 25 cm no extremo, com faixa N19 desde a face livre. Maior cortante de todo balanco usado como limite superior, sem interpolacao de origem incerta. 100% do tirante atende na receptora, inclusive com apenas um estribo garantido na regiao.

**V17→V23: ** Pendente para analise separada de Joao, por autorizacao expressa. Necessario consultar gravidade(permanentes+sobrecarga) separadamente do vento: negativo em gravidade indica papel de apoio invertido; com vento pode indicar levantamento. Envoltoria total nao identifica o carregamento governante. Rotulos apoiada/receptora nesta linha sao os originais TQS, ainda nao confirmados fisicamente.

**V17→V42: ** Pendente para analise separada de Joao, por autorizacao expressa. Necessario consultar gravidade(permanentes+sobrecarga) separadamente do vento: negativo em gravidade indica papel de apoio invertido; com vento pode indicar levantamento. Envoltoria total nao identifica o carregamento governante. Rotulos apoiada/receptora nesta linha sao os originais TQS, ainda nao confirmados fisicamente.

**V18→V23: ** Regiao 4,00-4,50 m da V23 desde P799; h 50 e tops/fundos coincidentes. Exigidos 3.852 cm 2/m; N29 fornece 4,1563 cm 2/m. Verificacao local de suspensao executada, independente das falhas de flexao da V23.

**V21→V22: ** Regiao unilateral de 25 cm no extremo, com faixa N9 desde a face livre. Maior cortante de todo balanco usado como limite superior, sem interpolacao de origem incerta. 75% atende por taxa; 100% e quantidade efetiva de estribos/reparticao entre receptora e apoiada ainda precisam comprovar-se. Um estribo apenas oferece 0,6234 cm 2; dois oferecem 1,2469 cm 2.

**V28→V15: ** Cruzamento posicionado pelas cotas e deslocamentos de eixo; faixa N21 c 20 e quatro barras porta-estribo cobrem toda regiao. Tirante 100% atendido na receptora; contagem minima de dois estribos fornece 2,4938 cm 2 contra 2,3885 cm 2 necessarios.

**V32→V15: ** Cruzamento posicionado pelas cotas e deslocamentos de eixo; faixa N21 c 20 e quatro barras porta-estribo cobrem toda regiao. 75% na receptora atende; 100% exige 6,4955 cm 2/m contra 6,2345 cm 2/m. Completar tirante com parcela na apoiada ou comprovar tres estribos efetivos na regiao da receptora.

**V33→V19: ** Armadura existente nao atende a suspensao; resultados do verificador preservados.

**V35→V15: ** Pendente para analise separada de Joao, por autorizacao expressa. Necessario consultar gravidade(permanentes+sobrecarga) separadamente do vento: negativo em gravidade indica papel de apoio invertido; com vento pode indicar levantamento. Envoltoria total nao identifica o carregamento governante. Rotulos apoiada/receptora nesta linha sao os originais TQS, ainda nao confirmados fisicamente.

**V36→V5: ** Pendente para analise separada de Joao, por autorizacao expressa. Necessario consultar gravidade(permanentes+sobrecarga) separadamente do vento: negativo em gravidade indica papel de apoio invertido; com vento pode indicar levantamento. Envoltoria total nao identifica o carregamento governante. Rotulos apoiada/receptora nesta linha sao os originais TQS, ainda nao confirmados fisicamente.

**V40→V20: ** Armadura existente nao atende a suspensao; resultados do verificador preservados.

**V49→V26: ** Joao confirmou apoio direto da V49 no bloco PC21C (70 x 70 cm, NB8,68 m no fundo da V49). Rotulo V26 da reacao TQS preservado somente como origem do modelo; nao caracteriza apoio indireto fisico.

**V50→V34: ** 75% na receptora exige 2,9751 cm 2 e pelo menos 3 estribos de 4 ramos 6,3 nos 50 cm, cuja fase deve ser comprovada.100% exige 3,9668 cm 2 e nao cabe apenas nos tres estribos maximos da receptora; comprovar parcela complementar na V50 dentro de h/2=25 cm ou outro detalhe. Nao concluir apenas pela taxa 6,2345 cm 2/m.

**V26→V25: ** Regiao unilateral de 25 cm no extremo, com faixa N17 desde a face livre. Maior cortante de todo balanco usado como limite superior, sem interpolacao de origem incerta. 100% do tirante atende na receptora, inclusive com apenas um estribo garantido na regiao.

V29: soma conservadora de suspensão+cortante exige 2,92 cm²/m; fornecida 3,67 cm²/m. Área atende; permanece comprovar o funcionamento/ancoragem das duas peças de estribo de 138/50 cm. Não há aprovação integral da ligação.

V39: soma conservadora de suspensão+cortante exige 2,76 cm²/m; fornecida 3,67 cm²/m. Área atende; permanece comprovar o funcionamento/ancoragem das duas peças de estribo de 138/50 cm. Não há aprovação integral da ligação.

V31: soma conservadora dos dois tirantes e cortante regional=3,31 cm²/m; fornecida=3,67 cm²/m. Area atende; eficacia das pecas compostas permanece separada.

V41: soma conservadora dos dois tirantes e cortante regional=2,56 cm²/m; fornecida=3,67 cm²/m. Area atende; eficacia das pecas compostas permanece separada.

V31→V12: distribuicao uniforme 75/25. Receptora: exigida=8,80 cm²/m; existente=10,05 cm²/m. Apoiada: exigida=3,34 cm²/m; existente=3,67 cm²/m. Cortantes regionais e parcelas calculadas pelo Concretopy; pecas compostas condicionam o resultado. A falha desta distribuicao uniforme nao esgota outras distribuicoes admissiveis.

V41→V13: distribuicao uniforme 75/25. Receptora: exigida=11,05 cm²/m; existente=10,05 cm²/m. Apoiada: exigida=5,06 cm²/m; existente=3,67 cm²/m. Cortantes regionais e parcelas calculadas pelo Concretopy; pecas compostas condicionam o resultado. A falha desta distribuicao uniforme nao esgota outras distribuicoes admissiveis.

## 6. Fichas de verificação

### V1

Geometria nominal do detalhe: 30×55 cm. Forma/detalhamento: presença nominal confirmada. Comparação nominal de seções conforme inventário. Situacao longitudinal: SECOES NOMINAIS CONFERIDAS; COTAS DE VAOS A CONCLUIR.

**Flexão positiva - solicitações Mk e resistência equivalente MRd/γf em tf·m.**

| Modelo/trecho | Apoios | b×h(cm) | Armadura | d(cm) | Mk | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V1/1 | P701-P702 | 30×55 | 4Ø16 | 50,07 | 8,56 | 12,05 | ATENDE | ATENDE |


**Flexao negativa - maximo de cada lado do apoio; valores absolutos em tf·m.**

E=inicio do trecho; D=fim do trecho. Em apoio intermediario, fim do trecho anterior e inicio do seguinte sao verificacoes distintas.

| Trecho/lado | Apoio | h(cm) | Armadura superior | d(cm) | Mk negativo | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1/E | P701 | 55 | 4Ø16 | 50,07 | 11,127 | 12,054 | ATENDE | ATENDE |
| 1/D | P702 | 55 | 4Ø16 | 50,07 | 11,144 | 12,054 | ATENDE | ATENDE |


Mínimos: comparação de MRd do Concretopy com Md, mín=0,8W0 fctk, sup e taxa absoluta 0,15%, conforme 17.3.5.2.1. O arquivo bruto também conserva a avaliação tabelada do motor; ela não substitui a verificação com d efetivo. A falta de momento positivo não demonstra necessidade de armadura positiva mínima na face não tracionada.

**Cortante - Vk característico em tf; taxas em cm²/m.**

| Trecho | Intervalo modelo(m) | Estribo | d(cm) | Vk | Fornecida | Exigida | Área | s máximo L/T | Biela |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/15 | 50,07 | 10,05 | 4,16 | 3,85 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |


INTERVALO TQS INTEIRO (LIMITE): maior|Vk| de todas as 13 secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.

Passagem geométrica do vibrador 4 cm: atende entre estribos nas faixas calculadas. Esse controle não comprova ausência de congestionamento nos encontros. Espaçamento transversal entre ramos e respectivos limites estão preservados no resultado bruto; quatro ramos com peças sobrepostas dependem da disposição do corte.

Trecho 1: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

**Suspensão: ** sem ligação indireta física identificada no inventário deste modelo.

Origem: detalhe 7401; recorte 7401_V1.png; esforços e resultados por modelo/trecho no JSON desta emissão. Cada linha conserva arquivo, número de linha e envoltória TQS.

### V2

Geometria nominal do detalhe: 30×50 cm. Forma/detalhamento: presença nominal confirmada. Comparação nominal de seções conforme inventário. Situacao longitudinal: SECOES NOMINAIS CONFERIDAS; COTAS DE VAOS A CONCLUIR.

**Flexão positiva - solicitações Mk e resistência equivalente MRd/γf em tf·m.**

| Modelo/trecho | Apoios | b×h(cm) | Armadura | d(cm) | Mk | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V2/1 | P704-P705 | 30×50 | 4Ø16 | 45,07 | 7,31 | 10,78 | ATENDE | ATENDE |
| V2/2 | P705-P706 | 30×50 | 3Ø16 | 45,07 | 6,19 | 8,22 | ATENDE | ATENDE |
| V2/3 | P706-P707 | 30×50 | 4Ø16 | 45,07 | 7,91 | 10,78 | ATENDE | ATENDE |


**Flexao negativa - maximo de cada lado do apoio; valores absolutos em tf·m.**

E=inicio do trecho; D=fim do trecho. Em apoio intermediario, fim do trecho anterior e inicio do seguinte sao verificacoes distintas.

| Trecho/lado | Apoio | h(cm) | Armadura superior | d(cm) | Mk negativo | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1/E | P704 | 50 | 4Ø16 | 45,07 | 9,854 | 10,780 | ATENDE | ATENDE |
| 1/D | P705 | 50 | 3Ø20 | 44,87 | 13,403 | 12,433 | ATENDE | NÃO ATENDE |
| 2/E | P705 | 50 | 3Ø20 | 44,87 | 12,346 | 12,433 | ATENDE | ATENDE |
| 2/D | P706 | 50 | 3Ø20 | 44,87 | 12,713 | 12,433 | ATENDE | NÃO ATENDE |
| 3/E | P706 | 50 | 3Ø20 | 44,87 | 14,109 | 12,433 | ATENDE | NÃO ATENDE |
| 3/D | P707 | 50 | 4Ø16 | 45,07 | 11,420 | 10,780 | ATENDE | NÃO ATENDE |


Mínimos: comparação de MRd do Concretopy com Md, mín=0,8W0 fctk, sup e taxa absoluta 0,15%, conforme 17.3.5.2.1. O arquivo bruto também conserva a avaliação tabelada do motor; ela não substitui a verificação com d efetivo. A falta de momento positivo não demonstra necessidade de armadura positiva mínima na face não tracionada.

**Cortante - Vk característico em tf; taxas em cm²/m.**

| Trecho | Intervalo modelo(m) | Estribo | d(cm) | Vk | Fornecida | Exigida | Área | s máximo L/T | Biela |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/15 | 44,87 | 8,98 | 4,16 | 3,85 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 2 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/15 | 44,87 | 8,37 | 4,16 | 3,85 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 3 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/15 | 44,87 | 11,35 | 4,16 | 3,85 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |


INTERVALO TQS INTEIRO (LIMITE): maior|Vk| de todas as 13 secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.

Passagem geométrica do vibrador 4 cm: atende entre estribos nas faixas calculadas. Esse controle não comprova ausência de congestionamento nos encontros. Espaçamento transversal entre ramos e respectivos limites estão preservados no resultado bruto; quatro ramos com peças sobrepostas dependem da disposição do corte.

Trecho 1: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

Trecho 2: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

Trecho 3: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

**Suspensão: ** sem ligação indireta física identificada no inventário deste modelo.

Origem: detalhe 7401; recorte 7401_V2.png; esforços e resultados por modelo/trecho no JSON desta emissão. Cada linha conserva arquivo, número de linha e envoltória TQS.

### V3

Geometria nominal do detalhe: 24×165 cm. Forma/detalhamento: presença nominal confirmada. Comparação nominal de seções conforme inventário. Situacao longitudinal: SECOES NOMINAIS CONFERIDAS; COTAS DE VAOS A CONCLUIR.

Adotados 4Ø16 de N1/corte; elevação indica 2Ø20. Barras superiores da primeira concretagem excluídas. Conferir funcionamento conjunto dos estribos de 138/50 cm na altura final 165 cm.

**Flexão positiva - solicitações Mk e resistência equivalente MRd/γf em tf·m.**

| Modelo/trecho | Apoios | b×h(cm) | Armadura | d(cm) | Mk | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V3/1 | P740-P746 | 24×165 | 4Ø16 | 159,90 | 1,84 | 39,85 | ATENDE | ATENDE |


**Flexao negativa - maximo de cada lado do apoio; valores absolutos em tf·m.**

E=inicio do trecho; D=fim do trecho. Em apoio intermediario, fim do trecho anterior e inicio do seguinte sao verificacoes distintas.

| Trecho/lado | Apoio | h(cm) | Armadura superior | d(cm) | Mk negativo | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1/E | P740 | 165 | 2Ø10 | 160,20 | 1,194 | 7,936 | NÃO ATENDE | ATENDE |
| 1/D | P746 | 165 | 2Ø10 | 160,20 | 0,153 | 7,936 | NÃO ATENDE | ATENDE |


Mínimo não atendido no apoio P740: As=1,57 cm²; mínimo absoluto=5,94 cm²; momento mínimo equivalente=26,48 tf·m; resistência equivalente=7,94 tf·m.

Mínimo não atendido no apoio P746: As=1,57 cm²; mínimo absoluto=5,94 cm²; momento mínimo equivalente=26,48 tf·m; resistência equivalente=7,94 tf·m.

Mínimos: comparação de MRd do Concretopy com Md, mín=0,8W0 fctk, sup e taxa absoluta 0,15%, conforme 17.3.5.2.1. O arquivo bruto também conserva a avaliação tabelada do motor; ela não substitui a verificação com d efetivo. A falta de momento positivo não demonstra necessidade de armadura positiva mínima na face não tracionada.

**Cortante - Vk característico em tf; taxas em cm²/m.**

| Trecho | Intervalo modelo(m) | Estribo | d(cm) | Vk | Fornecida | Exigida | Área | s máximo L/T | Biela |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø8,0 c/15 | 159,90 | 4,38 | 6,70 | 3,08 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |


INTERVALO TQS INTEIRO (LIMITE): maior|Vk| de todas as 13 secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.

Passagem geométrica do vibrador 4 cm: atende entre estribos nas faixas calculadas. Esse controle não comprova ausência de congestionamento nos encontros. Espaçamento transversal entre ramos e respectivos limites estão preservados no resultado bruto; quatro ramos com peças sobrepostas dependem da disposição do corte.

Trecho 1: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

**Suspensão: ** sem ligação indireta física identificada no inventário deste modelo.

Origem: detalhe 7401; recorte 7401_V3.png; esforços e resultados por modelo/trecho no JSON desta emissão. Cada linha conserva arquivo, número de linha e envoltória TQS.

### V4

Geometria nominal do detalhe: 40×50 cm. Forma/detalhamento: presença nominal confirmada. Comparação nominal de seções conforme inventário. Situacao longitudinal: FACES E FAIXAS CONCILIADAS; VER NOTAS DE COMPRIMENTO.

**Flexão positiva - solicitações Mk e resistência equivalente MRd/γf em tf·m.**

| Modelo/trecho | Apoios | b×h(cm) | Armadura | d(cm) | Mk | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V4/1 | P746-P747 | 40×50 | 6Ø20 | 44,87 | 10,41 | 23,91 | ATENDE | ATENDE |


**Flexao negativa - maximo de cada lado do apoio; valores absolutos em tf·m.**

E=inicio do trecho; D=fim do trecho. Em apoio intermediario, fim do trecho anterior e inicio do seguinte sao verificacoes distintas.

| Trecho/lado | Apoio | h(cm) | Armadura superior | d(cm) | Mk negativo | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1/E | P746 | 50 | 6Ø20 | 44,87 | 11,590 | 23,907 | ATENDE | ATENDE |
| 1/D | P747 | 50 | 5Ø20 | 44,87 | 10,321 | 20,322 | ATENDE | ATENDE |


Mínimos: comparação de MRd do Concretopy com Md, mín=0,8W0 fctk, sup e taxa absoluta 0,15%, conforme 17.3.5.2.1. O arquivo bruto também conserva a avaliação tabelada do motor; ela não substitui a verificação com d efetivo. A falta de momento positivo não demonstra necessidade de armadura positiva mínima na face não tracionada.

**Cortante - Vk característico em tf; taxas em cm²/m.**

| Trecho | Intervalo modelo(m) | Estribo | d(cm) | Vk | Fornecida | Exigida | Área | s máximo L/T | Biela |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0,15-2,48 | 4 r Ø8,0 c/10 | 44,70 | 13,67 | 20,11 | 5,14 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 1 | 2,48-6,88 | 4 r Ø6,3 c/20 | 44,87 | 15,42 | 6,23 | 5,14 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |


INTERVALO TQS INTEIRO (LIMITE): maior|Vk| de todas as 13 secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.

Passagem geométrica do vibrador 4 cm: atende entre estribos nas faixas calculadas. Esse controle não comprova ausência de congestionamento nos encontros. Espaçamento transversal entre ramos e respectivos limites estão preservados no resultado bruto; quatro ramos com peças sobrepostas dependem da disposição do corte.

**Suspensão: ** sem ligação indireta física identificada no inventário deste modelo.

Origem: detalhe 7401; recorte 7401_V4.png; esforços e resultados por modelo/trecho no JSON desta emissão. Cada linha conserva arquivo, número de linha e envoltória TQS.

### V5

Geometria nominal do detalhe: 19×50 cm. Forma/detalhamento: presença nominal confirmada. Comparação nominal de seções conforme inventário. Situacao longitudinal: FACES E FAIXAS CONCILIADAS; VER NOTAS DE COMPRIMENTO.

**Flexão positiva - solicitações Mk e resistência equivalente MRd/γf em tf·m.**

| Modelo/trecho | Apoios | b×h(cm) | Armadura | d(cm) | Mk | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V5/1 | P741-P742 | 19×50 | 3Ø16 | 44,70 | 5,22 | 7,92 | ATENDE | ATENDE |


**Flexao negativa - maximo de cada lado do apoio; valores absolutos em tf·m.**

E=inicio do trecho; D=fim do trecho. Em apoio intermediario, fim do trecho anterior e inicio do seguinte sao verificacoes distintas.

| Trecho/lado | Apoio | h(cm) | Armadura superior | d(cm) | Mk negativo | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1/E | P741 | 50 | 2Ø20 | 44,50 | 8,659 | 8,181 | ATENDE | NÃO ATENDE |
| 1/D | P742 | 50 | 3Ø20 / camadas [2, 1] | 43,17 | 10,901 | 11,369 | ATENDE | ATENDE |


Mínimos: comparação de MRd do Concretopy com Md, mín=0,8W0 fctk, sup e taxa absoluta 0,15%, conforme 17.3.5.2.1. O arquivo bruto também conserva a avaliação tabelada do motor; ela não substitui a verificação com d efetivo. A falta de momento positivo não demonstra necessidade de armadura positiva mínima na face não tracionada.

**Cortante - Vk característico em tf; taxas em cm²/m.**

| Trecho | Intervalo modelo(m) | Estribo | d(cm) | Vk | Fornecida | Exigida | Área | s máximo L/T | Biela |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0,55-2,79 | 2 r Ø10,0 c/12 | 43,17 | 15,06 | 13,09 | 7,57 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |


INTERVALO TQS INTEIRO (LIMITE): maior|Vk| de todas as 13 secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.

Passagem geométrica do vibrador 4 cm: atende entre estribos nas faixas calculadas. Esse controle não comprova ausência de congestionamento nos encontros. Espaçamento transversal entre ramos e respectivos limites estão preservados no resultado bruto; quatro ramos com peças sobrepostas dependem da disposição do corte.

**Suspensão: ** V36→V5: SENTIDO DA TRANSFERENCIA: ANALISE DE JOAO

Origem: detalhe 7401; recorte 7401_V5.png; esforços e resultados por modelo/trecho no JSON desta emissão. Cada linha conserva arquivo, número de linha e envoltória TQS.

### V6

Geometria nominal do detalhe: 24×165 cm. Forma/detalhamento: presença nominal confirmada. Comparação nominal de seções conforme inventário. Situacao longitudinal: SECOES NOMINAIS CONFERIDAS; COTAS DE VAOS A CONCLUIR.

Adotados 4Ø16 de N1/corte; elevação indica 2Ø20. Conferir funcionamento conjunto dos estribos de 138/50 cm na altura final 165 cm.

**Flexão positiva - solicitações Mk e resistência equivalente MRd/γf em tf·m.**

| Modelo/trecho | Apoios | b×h(cm) | Armadura | d(cm) | Mk | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V6/1 | P743-P744 | 24×165 | 4Ø16 | 159,90 | 1,10 | 39,85 | ATENDE | ATENDE |


**Flexao negativa - maximo de cada lado do apoio; valores absolutos em tf·m.**

E=inicio do trecho; D=fim do trecho. Em apoio intermediario, fim do trecho anterior e inicio do seguinte sao verificacoes distintas.

| Trecho/lado | Apoio | h(cm) | Armadura superior | d(cm) | Mk negativo | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1/E | P743 | 165 | 2Ø10 | 160,20 | 0,677 | 7,936 | NÃO ATENDE | ATENDE |
| 1/D | P744 | 165 | 2Ø10 | 160,20 | 0,021 | 7,936 | NÃO ATENDE | ATENDE |


Mínimo não atendido no apoio P743: As=1,57 cm²; mínimo absoluto=5,94 cm²; momento mínimo equivalente=26,48 tf·m; resistência equivalente=7,94 tf·m.

Mínimo não atendido no apoio P744: As=1,57 cm²; mínimo absoluto=5,94 cm²; momento mínimo equivalente=26,48 tf·m; resistência equivalente=7,94 tf·m.

Mínimos: comparação de MRd do Concretopy com Md, mín=0,8W0 fctk, sup e taxa absoluta 0,15%, conforme 17.3.5.2.1. O arquivo bruto também conserva a avaliação tabelada do motor; ela não substitui a verificação com d efetivo. A falta de momento positivo não demonstra necessidade de armadura positiva mínima na face não tracionada.

**Cortante - Vk característico em tf; taxas em cm²/m.**

| Trecho | Intervalo modelo(m) | Estribo | d(cm) | Vk | Fornecida | Exigida | Área | s máximo L/T | Biela |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø8,0 c/15 | 159,90 | 19,40 | 6,70 | 3,08 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |


INTERVALO TQS INTEIRO (LIMITE): maior|Vk| de todas as 13 secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.

Passagem geométrica do vibrador 4 cm: atende entre estribos nas faixas calculadas. Esse controle não comprova ausência de congestionamento nos encontros. Espaçamento transversal entre ramos e respectivos limites estão preservados no resultado bruto; quatro ramos com peças sobrepostas dependem da disposição do corte.

Trecho 1: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

**Suspensão: ** sem ligação indireta física identificada no inventário deste modelo.

Origem: detalhe 7401; recorte 7401_V6.png; esforços e resultados por modelo/trecho no JSON desta emissão. Cada linha conserva arquivo, número de linha e envoltória TQS.

### V7

Geometria nominal do detalhe: 19×165 cm. Forma/detalhamento: presença nominal confirmada. Comparação nominal de seções conforme inventário. Situacao longitudinal: SECOES NOMINAIS CONFERIDAS; COTAS DE VAOS A CONCLUIR.

O detalhe comum V7-V10 cita apoios V22/V26; a forma posiciona V7 em V29/V31. Usada a identidade física da forma. Estribos 138/50 cm exigem comprovar funcionamento conjunto.

**Flexão positiva - solicitações Mk e resistência equivalente MRd/γf em tf·m.**

| Modelo/trecho | Apoios | b×h(cm) | Armadura | d(cm) | Mk | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V7/1 | V29-V31 | 19×165 | 3Ø16 | 160,07 | 8,47 | 29,96 | ATENDE | ATENDE |


**Flexao negativa - maximo de cada lado do apoio; valores absolutos em tf·m.**

E=inicio do trecho; D=fim do trecho. Em apoio intermediario, fim do trecho anterior e inicio do seguinte sao verificacoes distintas.

| Trecho/lado | Apoio | h(cm) | Armadura superior | d(cm) | Mk negativo | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1/E | V29 | 165 | 2Ø10 | 160,37 | 0,000 | 7,935 | SEM MkNEGATIVO | ATENDE |
| 1/D | V31 | 165 | 2Ø10 | 160,37 | 0,287 | 7,935 | NÃO ATENDE | ATENDE |


Mínimo não atendido no apoio V31: As=1,57 cm²; mínimo absoluto=4,70 cm²; momento mínimo equivalente=20,96 tf·m; resistência equivalente=7,94 tf·m.

Mínimos: comparação de MRd do Concretopy com Md, mín=0,8W0 fctk, sup e taxa absoluta 0,15%, conforme 17.3.5.2.1. O arquivo bruto também conserva a avaliação tabelada do motor; ela não substitui a verificação com d efetivo. A falta de momento positivo não demonstra necessidade de armadura positiva mínima na face não tracionada.

**Cortante - Vk característico em tf; taxas em cm²/m.**

| Trecho | Intervalo modelo(m) | Estribo | d(cm) | Vk | Fornecida | Exigida | Área | s máximo L/T | Biela |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/20 | 160,07 | 10,61 | 3,12 | 2,44 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |


INTERVALO TQS INTEIRO (LIMITE): maior|Vk| de todas as 13 secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.

Passagem geométrica do vibrador 4 cm: atende entre estribos nas faixas calculadas. Esse controle não comprova ausência de congestionamento nos encontros. Espaçamento transversal entre ramos e respectivos limites estão preservados no resultado bruto; quatro ramos com peças sobrepostas dependem da disposição do corte.

Trecho 1: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

**Suspensão: ** V7→V29: AREA ATENDE; FECHAMENTO DOS ESTRIBOS A VERIFICAR; V7→V31: AREA ATENDE; FECHAMENTO DOS ESTRIBOS A VERIFICAR

Origem: detalhe 7401; recorte 7401_V7-10.png; esforços e resultados por modelo/trecho no JSON desta emissão. Cada linha conserva arquivo, número de linha e envoltória TQS.

### V8

Geometria nominal do detalhe: 19×165 cm. Forma/detalhamento: presença nominal confirmada. Comparação nominal de seções conforme inventário. Situacao longitudinal: SECOES NOMINAIS CONFERIDAS; COTAS DE VAOS A CONCLUIR.

Detalhe comum cita apoios V22/V26; forma posiciona V8 em V39/V41. Estribos 138/50 cm exigem comprovar funcionamento conjunto.

**Flexão positiva - solicitações Mk e resistência equivalente MRd/γf em tf·m.**

| Modelo/trecho | Apoios | b×h(cm) | Armadura | d(cm) | Mk | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V8/1 | V39-V41 | 19×165 | 3Ø16 | 160,07 | 8,27 | 29,96 | ATENDE | ATENDE |


**Flexao negativa - maximo de cada lado do apoio; valores absolutos em tf·m.**

E=inicio do trecho; D=fim do trecho. Em apoio intermediario, fim do trecho anterior e inicio do seguinte sao verificacoes distintas.

| Trecho/lado | Apoio | h(cm) | Armadura superior | d(cm) | Mk negativo | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1/E | V39 | 165 | 2Ø10 | 160,37 | 0,061 | 7,935 | NÃO ATENDE | ATENDE |
| 1/D | V41 | 165 | 2Ø10 | 160,37 | 0,436 | 7,935 | NÃO ATENDE | ATENDE |


Mínimo não atendido no apoio V39: As=1,57 cm²; mínimo absoluto=4,70 cm²; momento mínimo equivalente=20,96 tf·m; resistência equivalente=7,94 tf·m.

Mínimo não atendido no apoio V41: As=1,57 cm²; mínimo absoluto=4,70 cm²; momento mínimo equivalente=20,96 tf·m; resistência equivalente=7,94 tf·m.

Mínimos: comparação de MRd do Concretopy com Md, mín=0,8W0 fctk, sup e taxa absoluta 0,15%, conforme 17.3.5.2.1. O arquivo bruto também conserva a avaliação tabelada do motor; ela não substitui a verificação com d efetivo. A falta de momento positivo não demonstra necessidade de armadura positiva mínima na face não tracionada.

**Cortante - Vk característico em tf; taxas em cm²/m.**

| Trecho | Intervalo modelo(m) | Estribo | d(cm) | Vk | Fornecida | Exigida | Área | s máximo L/T | Biela |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/20 | 160,07 | 9,67 | 3,12 | 2,44 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |


INTERVALO TQS INTEIRO (LIMITE): maior|Vk| de todas as 13 secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.

Passagem geométrica do vibrador 4 cm: atende entre estribos nas faixas calculadas. Esse controle não comprova ausência de congestionamento nos encontros. Espaçamento transversal entre ramos e respectivos limites estão preservados no resultado bruto; quatro ramos com peças sobrepostas dependem da disposição do corte.

Trecho 1: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

**Suspensão: ** V8→V39: AREA ATENDE; FECHAMENTO DOS ESTRIBOS A VERIFICAR; V8→V41: AREA ATENDE; FECHAMENTO DOS ESTRIBOS A VERIFICAR

Origem: detalhe 7401; recorte 7401_V7-10.png; esforços e resultados por modelo/trecho no JSON desta emissão. Cada linha conserva arquivo, número de linha e envoltória TQS.

### V9

Geometria nominal do detalhe: 19×165 cm. Forma/detalhamento: presença nominal confirmada. Comparação nominal de seções conforme inventário. Situacao longitudinal: SECOES NOMINAIS CONFERIDAS; COTAS DE VAOS A CONCLUIR.

Detalhe comum cita apoios V22/V26; forma posiciona V9 em V29/V31. Estribos 138/50 cm exigem comprovar funcionamento conjunto.

**Flexão positiva - solicitações Mk e resistência equivalente MRd/γf em tf·m.**

| Modelo/trecho | Apoios | b×h(cm) | Armadura | d(cm) | Mk | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V9/1 | V29-V31 | 19×165 | 3Ø16 | 160,07 | 8,17 | 29,96 | ATENDE | ATENDE |


**Flexao negativa - maximo de cada lado do apoio; valores absolutos em tf·m.**

E=inicio do trecho; D=fim do trecho. Em apoio intermediario, fim do trecho anterior e inicio do seguinte sao verificacoes distintas.

| Trecho/lado | Apoio | h(cm) | Armadura superior | d(cm) | Mk negativo | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1/E | V29 | 165 | 2Ø10 | 160,37 | 0,000 | 7,935 | SEM MkNEGATIVO | ATENDE |
| 1/D | V31 | 165 | 2Ø10 | 160,37 | 0,567 | 7,935 | NÃO ATENDE | ATENDE |


Mínimo não atendido no apoio V31: As=1,57 cm²; mínimo absoluto=4,70 cm²; momento mínimo equivalente=20,96 tf·m; resistência equivalente=7,94 tf·m.

Mínimos: comparação de MRd do Concretopy com Md, mín=0,8W0 fctk, sup e taxa absoluta 0,15%, conforme 17.3.5.2.1. O arquivo bruto também conserva a avaliação tabelada do motor; ela não substitui a verificação com d efetivo. A falta de momento positivo não demonstra necessidade de armadura positiva mínima na face não tracionada.

**Cortante - Vk característico em tf; taxas em cm²/m.**

| Trecho | Intervalo modelo(m) | Estribo | d(cm) | Vk | Fornecida | Exigida | Área | s máximo L/T | Biela |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/20 | 160,07 | 9,74 | 3,12 | 2,44 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |


INTERVALO TQS INTEIRO (LIMITE): maior|Vk| de todas as 13 secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.

Passagem geométrica do vibrador 4 cm: atende entre estribos nas faixas calculadas. Esse controle não comprova ausência de congestionamento nos encontros. Espaçamento transversal entre ramos e respectivos limites estão preservados no resultado bruto; quatro ramos com peças sobrepostas dependem da disposição do corte.

Trecho 1: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

**Suspensão: ** V9→V29: AREA ATENDE; FECHAMENTO DOS ESTRIBOS A VERIFICAR; V9→V31: AREA ATENDE; FECHAMENTO DOS ESTRIBOS A VERIFICAR

Origem: detalhe 7401; recorte 7401_V7-10.png; esforços e resultados por modelo/trecho no JSON desta emissão. Cada linha conserva arquivo, número de linha e envoltória TQS.

### V10

Geometria nominal do detalhe: 19×165 cm. Forma/detalhamento: presença nominal confirmada. Comparação nominal de seções conforme inventário. Situacao longitudinal: SECOES NOMINAIS CONFERIDAS; COTAS DE VAOS A CONCLUIR.

Detalhe comum cita apoios V22/V26; forma posiciona V10 em V39/V41. Estribos 138/50 cm exigem comprovar funcionamento conjunto.

**Flexão positiva - solicitações Mk e resistência equivalente MRd/γf em tf·m.**

| Modelo/trecho | Apoios | b×h(cm) | Armadura | d(cm) | Mk | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V10/1 | V39-V41 | 19×165 | 3Ø16 | 160,07 | 7,94 | 29,96 | ATENDE | ATENDE |


**Flexao negativa - maximo de cada lado do apoio; valores absolutos em tf·m.**

E=inicio do trecho; D=fim do trecho. Em apoio intermediario, fim do trecho anterior e inicio do seguinte sao verificacoes distintas.

| Trecho/lado | Apoio | h(cm) | Armadura superior | d(cm) | Mk negativo | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1/E | V39 | 165 | 2Ø10 | 160,37 | 0,209 | 7,935 | NÃO ATENDE | ATENDE |
| 1/D | V41 | 165 | 2Ø10 | 160,37 | 0,677 | 7,935 | NÃO ATENDE | ATENDE |


Mínimo não atendido no apoio V39: As=1,57 cm²; mínimo absoluto=4,70 cm²; momento mínimo equivalente=20,96 tf·m; resistência equivalente=7,94 tf·m.

Mínimo não atendido no apoio V41: As=1,57 cm²; mínimo absoluto=4,70 cm²; momento mínimo equivalente=20,96 tf·m; resistência equivalente=7,94 tf·m.

Mínimos: comparação de MRd do Concretopy com Md, mín=0,8W0 fctk, sup e taxa absoluta 0,15%, conforme 17.3.5.2.1. O arquivo bruto também conserva a avaliação tabelada do motor; ela não substitui a verificação com d efetivo. A falta de momento positivo não demonstra necessidade de armadura positiva mínima na face não tracionada.

**Cortante - Vk característico em tf; taxas em cm²/m.**

| Trecho | Intervalo modelo(m) | Estribo | d(cm) | Vk | Fornecida | Exigida | Área | s máximo L/T | Biela |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/20 | 160,07 | 9,54 | 3,12 | 2,44 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |


INTERVALO TQS INTEIRO (LIMITE): maior|Vk| de todas as 13 secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.

Passagem geométrica do vibrador 4 cm: atende entre estribos nas faixas calculadas. Esse controle não comprova ausência de congestionamento nos encontros. Espaçamento transversal entre ramos e respectivos limites estão preservados no resultado bruto; quatro ramos com peças sobrepostas dependem da disposição do corte.

Trecho 1: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

**Suspensão: ** V10→V39: AREA ATENDE; FECHAMENTO DOS ESTRIBOS A VERIFICAR; V10→V41: AREA ATENDE; FECHAMENTO DOS ESTRIBOS A VERIFICAR

Origem: detalhe 7401; recorte 7401_V7-10.png; esforços e resultados por modelo/trecho no JSON desta emissão. Cada linha conserva arquivo, número de linha e envoltória TQS.

### V11

Geometria nominal do detalhe: 24×80 cm. Forma/detalhamento: presença nominal confirmada. Comparação nominal de seções conforme inventário. Situacao longitudinal: SECOES NOMINAIS CONFERIDAS; COTAS DE VAOS A CONCLUIR.

**Flexão positiva - solicitações Mk e resistência equivalente MRd/γf em tf·m.**

| Modelo/trecho | Apoios | b×h(cm) | Armadura | d(cm) | Mk | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V11/1 | P752-P754 | 24×80 | 2Ø20 | 74,70 | 4,91 | 14,33 | ATENDE | ATENDE |


**Flexao negativa - maximo de cada lado do apoio; valores absolutos em tf·m.**

E=inicio do trecho; D=fim do trecho. Em apoio intermediario, fim do trecho anterior e inicio do seguinte sao verificacoes distintas.

| Trecho/lado | Apoio | h(cm) | Armadura superior | d(cm) | Mk negativo | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1/E | P752 | 80 | 3Ø10 | 75,20 | 3,196 | 5,536 | NÃO ATENDE | ATENDE |
| 1/D | P754 | 80 | 2Ø12,5 | 75,08 | 0,944 | 5,754 | NÃO ATENDE | ATENDE |


Mínimo não atendido no apoio P752: As=2,36 cm²; mínimo absoluto=2,88 cm²; momento mínimo equivalente=6,22 tf·m; resistência equivalente=5,54 tf·m.

Mínimo não atendido no apoio P754: As=2,45 cm²; mínimo absoluto=2,88 cm²; momento mínimo equivalente=6,22 tf·m; resistência equivalente=5,75 tf·m.

Mínimos: comparação de MRd do Concretopy com Md, mín=0,8W0 fctk, sup e taxa absoluta 0,15%, conforme 17.3.5.2.1. O arquivo bruto também conserva a avaliação tabelada do motor; ela não substitui a verificação com d efetivo. A falta de momento positivo não demonstra necessidade de armadura positiva mínima na face não tracionada.

**Cortante - Vk característico em tf; taxas em cm²/m.**

| Trecho | Intervalo modelo(m) | Estribo | d(cm) | Vk | Fornecida | Exigida | Área | s máximo L/T | Biela |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø8,0 c/15 | 74,70 | 13,70 | 6,70 | 3,08 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |


INTERVALO TQS INTEIRO (LIMITE): maior|Vk| de todas as 13 secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.

Passagem geométrica do vibrador 4 cm: atende entre estribos nas faixas calculadas. Esse controle não comprova ausência de congestionamento nos encontros. Espaçamento transversal entre ramos e respectivos limites estão preservados no resultado bruto; quatro ramos com peças sobrepostas dependem da disposição do corte.

Trecho 1: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

**Suspensão: ** sem ligação indireta física identificada no inventário deste modelo.

Origem: detalhe 7401; recorte 7401_V11.png; esforços e resultados por modelo/trecho no JSON desta emissão. Cada linha conserva arquivo, número de linha e envoltória TQS.

### V12

Geometria nominal do detalhe: 24×165 cm. Forma/detalhamento: presença nominal confirmada. Comparação nominal de seções conforme inventário. Situacao longitudinal: FAIXA171 cm COERENTE COM152 cm+19 cm DA FORMA.

V31 descarrega na V12, confirmado por Joao. Rk=24,46 tf obtido por acao-reacao da listagem. Suspensao numerica atende com 75% na V12 e 25% na V31; estribos compostos 138/50 cm permanecem sujeitos a verificacao de funcionamento conjunto.

**Flexão positiva - solicitações Mk e resistência equivalente MRd/γf em tf·m.**

| Modelo/trecho | Apoios | b×h(cm) | Armadura | d(cm) | Mk | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V12/1 | P753-V31 | 24×165 | 3Ø12,5 | 160,07 | 0,00 | 18,48 | SEM Mk POSITIVO | SEM MOMENTO POSITIVO NA ENVOLTÓRIA |


**Flexao negativa - maximo de cada lado do apoio; valores absolutos em tf·m.**

E=inicio do trecho; D=fim do trecho. Em apoio intermediario, fim do trecho anterior e inicio do seguinte sao verificacoes distintas.

| Trecho/lado | Apoio | h(cm) | Armadura superior | d(cm) | Mk negativo | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1/E | P753 | 165 | 2Ø16 | 159,90 | 72,842 | 20,144 | NÃO ATENDE | NÃO ATENDE |
| 1/D | V31 | 165 | 2Ø16 | 159,90 | 2,754 | 20,144 | NÃO ATENDE | ATENDE |


Mínimo não atendido no apoio P753: As=4,02 cm²; mínimo absoluto=5,94 cm²; momento mínimo equivalente=26,48 tf·m; resistência equivalente=20,14 tf·m.

Mínimo não atendido no apoio V31: As=4,02 cm²; mínimo absoluto=5,94 cm²; momento mínimo equivalente=26,48 tf·m; resistência equivalente=20,14 tf·m.

Mínimos: comparação de MRd do Concretopy com Md, mín=0,8W0 fctk, sup e taxa absoluta 0,15%, conforme 17.3.5.2.1. O arquivo bruto também conserva a avaliação tabelada do motor; ela não substitui a verificação com d efetivo. A falta de momento positivo não demonstra necessidade de armadura positiva mínima na face não tracionada.

**Cortante - Vk característico em tf; taxas em cm²/m.**

| Trecho | Intervalo modelo(m) | Estribo | d(cm) | Vk | Fornecida | Exigida | Área | s máximo L/T | Biela |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø8,0 c/10 | 159,90 | 39,72 | 10,05 | 3,08 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |


INTERVALO TQS INTEIRO (LIMITE): maior|Vk| de todas as 13 secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.

Passagem geométrica do vibrador 4 cm: atende entre estribos nas faixas calculadas. Esse controle não comprova ausência de congestionamento nos encontros. Espaçamento transversal entre ramos e respectivos limites estão preservados no resultado bruto; quatro ramos com peças sobrepostas dependem da disposição do corte.

Trecho 1: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

**Suspensão: ** V31→V12: AREA ATENDE; FECHAMENTO DOS ESTRIBOS A VERIFICAR

Origem: detalhe 7401; recorte 7401_V12-13.png; esforços e resultados por modelo/trecho no JSON desta emissão. Cada linha conserva arquivo, número de linha e envoltória TQS.

### V13

Geometria nominal do detalhe: 24×165 cm. Forma/detalhamento: presença nominal confirmada. Comparação nominal de seções conforme inventário. Situacao longitudinal: FAIXA171 cm COERENTE COM152 cm+19 cm DA FORMA.

V41 descarrega na V13, confirmado por Joao. Rk=30,52 tf. Distribuicao uniforme 75/25 nao atende a soma com cortante regional; nao equivale a demonstracao de impossibilidade de outra distribuicao admissivel. Ver valores na secao de ligacoes.

**Flexão positiva - solicitações Mk e resistência equivalente MRd/γf em tf·m.**

| Modelo/trecho | Apoios | b×h(cm) | Armadura | d(cm) | Mk | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V13/1 | P754-V41 | 24×165 | 3Ø12,5 | 160,07 | 0,00 | 18,48 | SEM Mk POSITIVO | SEM MOMENTO POSITIVO NA ENVOLTÓRIA |


**Flexao negativa - maximo de cada lado do apoio; valores absolutos em tf·m.**

E=inicio do trecho; D=fim do trecho. Em apoio intermediario, fim do trecho anterior e inicio do seguinte sao verificacoes distintas.

| Trecho/lado | Apoio | h(cm) | Armadura superior | d(cm) | Mk negativo | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1/E | P754 | 165 | 2Ø16 | 159,90 | 78,260 | 20,144 | NÃO ATENDE | NÃO ATENDE |
| 1/D | V41 | 165 | 2Ø16 | 159,90 | 3,007 | 20,144 | NÃO ATENDE | ATENDE |


Mínimo não atendido no apoio P754: As=4,02 cm²; mínimo absoluto=5,94 cm²; momento mínimo equivalente=26,48 tf·m; resistência equivalente=20,14 tf·m.

Mínimo não atendido no apoio V41: As=4,02 cm²; mínimo absoluto=5,94 cm²; momento mínimo equivalente=26,48 tf·m; resistência equivalente=20,14 tf·m.

Mínimos: comparação de MRd do Concretopy com Md, mín=0,8W0 fctk, sup e taxa absoluta 0,15%, conforme 17.3.5.2.1. O arquivo bruto também conserva a avaliação tabelada do motor; ela não substitui a verificação com d efetivo. A falta de momento positivo não demonstra necessidade de armadura positiva mínima na face não tracionada.

**Cortante - Vk característico em tf; taxas em cm²/m.**

| Trecho | Intervalo modelo(m) | Estribo | d(cm) | Vk | Fornecida | Exigida | Área | s máximo L/T | Biela |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø8,0 c/10 | 159,90 | 40,83 | 10,05 | 3,08 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |


INTERVALO TQS INTEIRO (LIMITE): maior|Vk| de todas as 13 secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.

Passagem geométrica do vibrador 4 cm: atende entre estribos nas faixas calculadas. Esse controle não comprova ausência de congestionamento nos encontros. Espaçamento transversal entre ramos e respectivos limites estão preservados no resultado bruto; quatro ramos com peças sobrepostas dependem da disposição do corte.

Trecho 1: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

**Suspensão: ** V41→V13: DISTRIBUICAO UNIFORME NAO ATENDE

Origem: detalhe 7401; recorte 7401_V12-13.png; esforços e resultados por modelo/trecho no JSON desta emissão. Cada linha conserva arquivo, número de linha e envoltória TQS.

### V14

Geometria nominal do detalhe: 19×50 cm. Forma/detalhamento: presença nominal confirmada. Comparação nominal de seções conforme inventário. Situacao longitudinal: SECOES NOMINAIS CONFERIDAS; COTAS DE VAOS A CONCLUIR.

**Flexão positiva - solicitações Mk e resistência equivalente MRd/γf em tf·m.**

| Modelo/trecho | Apoios | b×h(cm) | Armadura | d(cm) | Mk | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V14/1 | PC26C-PC24C | 19×50 | 2Ø16 | 45,07 | 0,43 | 5,46 | ATENDE | ATENDE |
| V14/2 | PC24C-PC20C | 19×50 | 2Ø16 | 45,07 | 0,37 | 5,46 | ATENDE | ATENDE |
| V14/3 | PC20C-V43 | 19×50 | 2Ø16 | 45,07 | 0,11 | 5,46 | ATENDE | ATENDE |


**Flexao negativa - maximo de cada lado do apoio; valores absolutos em tf·m.**

E=inicio do trecho; D=fim do trecho. Em apoio intermediario, fim do trecho anterior e inicio do seguinte sao verificacoes distintas.

| Trecho/lado | Apoio | h(cm) | Armadura superior | d(cm) | Mk negativo | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1/E | PC26C | 50 | 2Ø16 | 45,07 | 0,576 | 5,464 | ATENDE | ATENDE |
| 1/D | PC24C | 50 | 2Ø16 | 45,07 | 3,197 | 5,464 | ATENDE | ATENDE |
| 2/E | PC24C | 50 | 2Ø16 | 45,07 | 0,565 | 5,464 | ATENDE | ATENDE |
| 2/D | PC20C | 50 | 2Ø16 | 45,07 | 0,611 | 5,464 | ATENDE | ATENDE |
| 3/E | PC20C | 50 | 2Ø16 | 45,07 | 3,659 | 5,464 | ATENDE | ATENDE |
| 3/D | V43 | 50 | 2Ø16 | 45,07 | 0,009 | 5,464 | ATENDE | ATENDE |


Mínimos: comparação de MRd do Concretopy com Md, mín=0,8W0 fctk, sup e taxa absoluta 0,15%, conforme 17.3.5.2.1. O arquivo bruto também conserva a avaliação tabelada do motor; ela não substitui a verificação com d efetivo. A falta de momento positivo não demonstra necessidade de armadura positiva mínima na face não tracionada.

**Cortante - Vk característico em tf; taxas em cm²/m.**

| Trecho | Intervalo modelo(m) | Estribo | d(cm) | Vk | Fornecida | Exigida | Área | s máximo L/T | Biela |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/15 | 45,07 | 5,68 | 4,16 | 2,44 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 2 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/15 | 45,07 | 1,17 | 4,16 | 2,44 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 3 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/15 | 45,07 | 6,45 | 4,16 | 2,44 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |


INTERVALO TQS INTEIRO (LIMITE): maior|Vk| de todas as 13 secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.

Passagem geométrica do vibrador 4 cm: atende entre estribos nas faixas calculadas. Esse controle não comprova ausência de congestionamento nos encontros. Espaçamento transversal entre ramos e respectivos limites estão preservados no resultado bruto; quatro ramos com peças sobrepostas dependem da disposição do corte.

Trecho 1: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

Trecho 2: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

Trecho 3: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

**Suspensão: ** V14→V43: ATENDE

Origem: detalhe 7401; recorte 7401_V14.png; esforços e resultados por modelo/trecho no JSON desta emissão. Cada linha conserva arquivo, número de linha e envoltória TQS.

### V15

Geometria nominal do detalhe: 40×50 cm. Forma/detalhamento: presença nominal confirmada. Comparação nominal de seções conforme inventário. Situacao longitudinal: FACES E FAIXAS CONCILIADAS; VER NOTAS DE COMPRIMENTO.

NB8,38 m de P756/P761 confirmado. Fundo da viga 8,68 m: nesses apoios usar faces dos pilares; nos demais, faces dos blocos que interceptam a viga. Cortante atende nas quatro faixas/vãos calculados. Falhas negativas são independentes desse atendimento.

**Flexão positiva - solicitações Mk e resistência equivalente MRd/γf em tf·m.**

| Modelo/trecho | Apoios | b×h(cm) | Armadura | d(cm) | Mk | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V15/1 | P757-P756 | 40×50 | 4Ø20 | 44,87 | 10,58 | 16,58 | ATENDE | ATENDE |
| V15/2 | P756-P760 | 40×50 | 4Ø20 | 44,87 | 13,97 | 16,58 | ATENDE | ATENDE |
| V15/3 | P760-P758 | 40×50 | 4Ø20 | 44,87 | 12,10 | 16,58 | ATENDE | ATENDE |
| V15/4 | P758-P761 | 40×50 | 6Ø20 | 44,87 | 12,66 | 23,91 | ATENDE | ATENDE |


**Flexao negativa - maximo de cada lado do apoio; valores absolutos em tf·m.**

E=inicio do trecho; D=fim do trecho. Em apoio intermediario, fim do trecho anterior e inicio do seguinte sao verificacoes distintas.

| Trecho/lado | Apoio | h(cm) | Armadura superior | d(cm) | Mk negativo | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1/E | P757 | 50 | 4Ø12,5 | 45,24 | 16,851 | 6,838 | ATENDE | NÃO ATENDE |
| 1/D | P756 | 50 | 6Ø20 | 44,87 | 21,588 | 23,907 | ATENDE | ATENDE |
| 2/E | P756 | 50 | 6Ø20 | 44,87 | 29,229 | 23,907 | ATENDE | NÃO ATENDE |
| 2/D | P760 | 50 | 4Ø16 | 45,07 | 23,719 | 10,955 | ATENDE | NÃO ATENDE |
| 3/E | P760 | 50 | 4Ø16 | 45,07 | 22,871 | 10,955 | ATENDE | NÃO ATENDE |
| 3/D | P758 | 50 | 8Ø20 / camadas [7, 1] | 44,37 | 28,492 | 30,199 | ATENDE | ATENDE |
| 4/E | P758 | 50 | 8Ø20 / camadas [7, 1] | 44,37 | 30,378 | 30,199 | ATENDE | NÃO ATENDE |
| 4/D | P761 | 50 | 6Ø20 | 44,87 | 18,080 | 23,907 | ATENDE | ATENDE |


Mínimos: comparação de MRd do Concretopy com Md, mín=0,8W0 fctk, sup e taxa absoluta 0,15%, conforme 17.3.5.2.1. O arquivo bruto também conserva a avaliação tabelada do motor; ela não substitui a verificação com d efetivo. A falta de momento positivo não demonstra necessidade de armadura positiva mínima na face não tracionada.

**Cortante - Vk característico em tf; taxas em cm²/m.**

| Trecho | Intervalo modelo(m) | Estribo | d(cm) | Vk | Fornecida | Exigida | Área | s máximo L/T | Biela |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1,10-7,30 | 4 r Ø6,3 c/20 | 44,87 | 14,97 | 6,23 | 5,14 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 2 | 0,15-1,67 | 4 r Ø6,3 c/10 | 44,87 | 23,22 | 12,47 | 8,31 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 2 | 1,67-6,35 | 4 r Ø6,3 c/20 | 44,87 | 11,49 | 6,23 | 5,14 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 3 | 1,30-6,98 | 4 r Ø6,3 c/20 | 44,37 | 17,72 | 6,23 | 5,14 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 4 | 1,24-7,55 | 4 r Ø6,3 c/15 | 44,37 | 15,69 | 8,31 | 5,14 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |


INTERVALO TQS INTEIRO (LIMITE): maior|Vk| de todas as 13 secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.

Passagem geométrica do vibrador 4 cm: atende entre estribos nas faixas calculadas. Esse controle não comprova ausência de congestionamento nos encontros. Espaçamento transversal entre ramos e respectivos limites estão preservados no resultado bruto; quatro ramos com peças sobrepostas dependem da disposição do corte.

**Suspensão: ** V28→V15: ATENDE; V32→V15: TIRANTE INTEGRAL A COMPROVAR; V35→V15: SENTIDO DA TRANSFERENCIA: ANALISE DE JOAO

Origem: detalhe 7401; recorte 7401_V15.png; esforços e resultados por modelo/trecho no JSON desta emissão. Cada linha conserva arquivo, número de linha e envoltória TQS.

### V16

Geometria nominal do detalhe: 40×50 cm. Forma/detalhamento: presença nominal confirmada. Comparação nominal de seções conforme inventário. Situacao longitudinal: FACES E FAIXAS CONCILIADAS; VER NOTAS DE COMPRIMENTO.

**Flexão positiva - solicitações Mk e resistência equivalente MRd/γf em tf·m.**

| Modelo/trecho | Apoios | b×h(cm) | Armadura | d(cm) | Mk | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V16/1 | PC40C-PC41C | 40×50 | 4Ø12,5 | 45,24 | 15,28 | 6,84 | ATENDE | NÃO ATENDE |


**Flexao negativa - maximo de cada lado do apoio; valores absolutos em tf·m.**

E=inicio do trecho; D=fim do trecho. Em apoio intermediario, fim do trecho anterior e inicio do seguinte sao verificacoes distintas.

| Trecho/lado | Apoio | h(cm) | Armadura superior | d(cm) | Mk negativo | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1/E | PC40C | 50 | 4Ø16 | 45,07 | 9,398 | 10,955 | ATENDE | ATENDE |
| 1/D | PC41C | 50 | 4Ø16 | 45,07 | 13,769 | 10,955 | ATENDE | NÃO ATENDE |


Mínimos: comparação de MRd do Concretopy com Md, mín=0,8W0 fctk, sup e taxa absoluta 0,15%, conforme 17.3.5.2.1. O arquivo bruto também conserva a avaliação tabelada do motor; ela não substitui a verificação com d efetivo. A falta de momento positivo não demonstra necessidade de armadura positiva mínima na face não tracionada.

**Cortante - Vk característico em tf; taxas em cm²/m.**

| Trecho | Intervalo modelo(m) | Estribo | d(cm) | Vk | Fornecida | Exigida | Área | s máximo L/T | Biela |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0,15-7,45 | 4 r Ø6,3 c/20 | 45,07 | 15,40 | 6,23 | 5,14 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |


INTERVALO TQS INTEIRO (LIMITE): maior|Vk| de todas as 13 secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.

Passagem geométrica do vibrador 4 cm: atende entre estribos nas faixas calculadas. Esse controle não comprova ausência de congestionamento nos encontros. Espaçamento transversal entre ramos e respectivos limites estão preservados no resultado bruto; quatro ramos com peças sobrepostas dependem da disposição do corte.

**Suspensão: ** sem ligação indireta física identificada no inventário deste modelo.

Origem: detalhe 7401; recorte 7401_V16.png; esforços e resultados por modelo/trecho no JSON desta emissão. Cada linha conserva arquivo, número de linha e envoltória TQS.

### V17

Geometria nominal do detalhe: 40×50 cm. Forma/detalhamento: presença nominal confirmada. Comparação nominal de seções conforme inventário. Situacao longitudinal: SECOES NOMINAIS CONFERIDAS; COTAS DE VAOS A CONCLUIR.

Transição entre quatro ramosØ8 c/17 (3225 cm) e c/10 (1535 cm) ainda sem abscissa física integral comprovada. Trecho 5 consultado conservadoramente com c/17; trecho 6 com c/10. Não há reprovação gerada por essa aproximação. Sentido das interfaces V23/V42 depende do caso gravidade/vento; analise separada de Joao.

**Flexão positiva - solicitações Mk e resistência equivalente MRd/γf em tf·m.**

| Modelo/trecho | Apoios | b×h(cm) | Armadura | d(cm) | Mk | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V17/1 | V23-V901 | 40×50 | 4Ø20 | 44,70 | 2,63 | 16,51 | ATENDE | ATENDE |
| V17/2 | V901-V902 | 40×50 | 4Ø20 | 44,70 | 2,46 | 16,51 | ATENDE | ATENDE |
| V17/3 | V902-V903 | 40×50 | 4Ø20 | 44,70 | 2,37 | 16,51 | ATENDE | ATENDE |
| V17/4 | V903-V904 | 40×50 | 5Ø20 | 44,70 | 2,63 | 20,24 | ATENDE | ATENDE |
| V17/5 | V904-V905 | 40×50 | 5Ø20 | 44,70 | 2,58 | 20,24 | ATENDE | ATENDE |
| V17/6 | V905-V42 | 40×50 | 5Ø20 | 44,70 | 2,86 | 20,24 | ATENDE | ATENDE |


**Flexao negativa - maximo de cada lado do apoio; valores absolutos em tf·m.**

E=inicio do trecho; D=fim do trecho. Em apoio intermediario, fim do trecho anterior e inicio do seguinte sao verificacoes distintas.

| Trecho/lado | Apoio | h(cm) | Armadura superior | d(cm) | Mk negativo | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1/E | V23 | 50 | 4Ø10 | 45,20 | 0,693 | 4,417 | ATENDE | ATENDE |
| 1/D | V901 | 50 | 6Ø20 | 44,70 | 7,013 | 23,805 | ATENDE | ATENDE |
| 2/E | V901 | 50 | 6Ø20 | 44,70 | 7,010 | 23,805 | ATENDE | ATENDE |
| 2/D | V902 | 50 | 5Ø20 | 44,70 | 6,215 | 20,237 | ATENDE | ATENDE |
| 3/E | V902 | 50 | 5Ø20 | 44,70 | 6,215 | 20,237 | ATENDE | ATENDE |
| 3/D | V903 | 50 | 7Ø20 | 44,70 | 6,856 | 27,213 | ATENDE | ATENDE |
| 4/E | V903 | 50 | 7Ø20 | 44,70 | 6,862 | 27,213 | ATENDE | ATENDE |
| 4/D | V904 | 50 | 7Ø20 | 44,70 | 7,020 | 27,213 | ATENDE | ATENDE |
| 5/E | V904 | 50 | 7Ø20 | 44,70 | 7,020 | 27,213 | ATENDE | ATENDE |
| 5/D | V905 | 50 | 8Ø20 / camadas [7, 1] | 44,20 | 7,494 | 30,063 | ATENDE | ATENDE |
| 6/E | V905 | 50 | 8Ø20 / camadas [7, 1] | 44,20 | 7,500 | 30,063 | ATENDE | ATENDE |
| 6/D | V42 | 50 | 4Ø10 | 45,20 | 0,385 | 4,417 | ATENDE | ATENDE |


Mínimos: comparação de MRd do Concretopy com Md, mín=0,8W0 fctk, sup e taxa absoluta 0,15%, conforme 17.3.5.2.1. O arquivo bruto também conserva a avaliação tabelada do motor; ela não substitui a verificação com d efetivo. A falta de momento positivo não demonstra necessidade de armadura positiva mínima na face não tracionada.

**Cortante - Vk característico em tf; taxas em cm²/m.**

| Trecho | Intervalo modelo(m) | Estribo | d(cm) | Vk | Fornecida | Exigida | Área | s máximo L/T | Biela |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | INTERVALO TQS INTEIRO (LIMITE) | 4 r Ø8,0 c/17 | 44,70 | 5,56 | 11,83 | 5,14 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 2 | INTERVALO TQS INTEIRO (LIMITE) | 4 r Ø8,0 c/17 | 44,70 | 6,74 | 11,83 | 5,14 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 3 | INTERVALO TQS INTEIRO (LIMITE) | 4 r Ø8,0 c/17 | 44,70 | 7,06 | 11,83 | 5,14 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 4 | INTERVALO TQS INTEIRO (LIMITE) | 4 r Ø8,0 c/17 | 44,70 | 6,92 | 11,83 | 5,14 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 5 | INTERVALO TQS INTEIRO (LIMITE) | 4 r Ø8,0 c/17 | 44,20 | 7,15 | 11,83 | 5,14 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 6 | INTERVALO TQS INTEIRO (LIMITE) | 4 r Ø8,0 c/10 | 44,20 | 6,89 | 20,11 | 5,14 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |


INTERVALO TQS INTEIRO (LIMITE): maior|Vk| de todas as 13 secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.

Passagem geométrica do vibrador 4 cm: atende entre estribos nas faixas calculadas. Esse controle não comprova ausência de congestionamento nos encontros. Espaçamento transversal entre ramos e respectivos limites estão preservados no resultado bruto; quatro ramos com peças sobrepostas dependem da disposição do corte.

Trecho 1: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

Trecho 2: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

Trecho 3: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

Trecho 4: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

Trecho 5: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

Trecho 6: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

**Suspensão: ** V17→V23: SENTIDO DA TRANSFERENCIA: ANALISE DE JOAO; V17→V42: SENTIDO DA TRANSFERENCIA: ANALISE DE JOAO

Origem: detalhe 7401; recorte 7401_V17.png; esforços e resultados por modelo/trecho no JSON desta emissão. Cada linha conserva arquivo, número de linha e envoltória TQS.

### V18

Geometria nominal do detalhe: 30×50 cm. Forma/detalhamento: presença nominal confirmada. Comparação nominal de seções conforme inventário. Situacao longitudinal: FACES E FAIXAS CONCILIADAS; VER NOTAS DE COMPRIMENTO.

Adotados 3Ø16 de N5 no PC46C; elevação indica 2Ø20. Estribos originais 2 ramosØ6,3 c/15 nos dois vãos. Anotações sobrepostas são propostas e não entram no existente.

**Flexão positiva - solicitações Mk e resistência equivalente MRd/γf em tf·m.**

| Modelo/trecho | Apoios | b×h(cm) | Armadura | d(cm) | Mk | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V18/1 | V23-PC45C | 30×50 | 3Ø16 | 45,07 | 4,06 | 8,22 | ATENDE | ATENDE |
| V18/2 | PC45C-PC46C | 30×50 | 3Ø16 | 45,07 | 8,13 | 8,22 | ATENDE | ATENDE |


**Flexao negativa - maximo de cada lado do apoio; valores absolutos em tf·m.**

E=inicio do trecho; D=fim do trecho. Em apoio intermediario, fim do trecho anterior e inicio do seguinte sao verificacoes distintas.

| Trecho/lado | Apoio | h(cm) | Armadura superior | d(cm) | Mk negativo | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1/E | V23 | 50 | 2Ø10 | 45,37 | 0,000 | 2,230 | SEM MkNEGATIVO | ATENDE |
| 1/D | PC45C | 50 | 3Ø20 | 44,87 | 18,450 | 12,433 | ATENDE | NÃO ATENDE |
| 2/E | PC45C | 50 | 3Ø20 | 44,87 | 18,410 | 12,433 | ATENDE | NÃO ATENDE |
| 2/D | PC46C | 50 | 3Ø16 | 45,07 | 9,247 | 8,216 | ATENDE | NÃO ATENDE |


Mínimos: comparação de MRd do Concretopy com Md, mín=0,8W0 fctk, sup e taxa absoluta 0,15%, conforme 17.3.5.2.1. O arquivo bruto também conserva a avaliação tabelada do motor; ela não substitui a verificação com d efetivo. A falta de momento positivo não demonstra necessidade de armadura positiva mínima na face não tracionada.

**Cortante - Vk característico em tf; taxas em cm²/m.**

| Trecho | Intervalo modelo(m) | Estribo | d(cm) | Vk | Fornecida | Exigida | Área | s máximo L/T | Biela |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0,15-3,60 | 2 r Ø6,3 c/15 | 44,87 | 21,04 | 4,16 | 9,07 | NÃO ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 2 | 0,15-7,45 | 2 r Ø6,3 c/15 | 44,87 | 21,49 | 4,16 | 9,42 | NÃO ATENDE | L: ATENDE / T: ATENDE | ATENDE |


INTERVALO TQS INTEIRO (LIMITE): maior|Vk| de todas as 13 secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.

Passagem geométrica do vibrador 4 cm: atende entre estribos nas faixas calculadas. Esse controle não comprova ausência de congestionamento nos encontros. Espaçamento transversal entre ramos e respectivos limites estão preservados no resultado bruto; quatro ramos com peças sobrepostas dependem da disposição do corte.

**Suspensão: ** V18→V23: ATENDE

Origem: detalhe 7401; recorte 7401_V18.png; esforços e resultados por modelo/trecho no JSON desta emissão. Cada linha conserva arquivo, número de linha e envoltória TQS.

### V19

Geometria nominal do detalhe: 30×50 cm. Forma/detalhamento: presença nominal confirmada. Comparação nominal de seções conforme inventário. Situacao longitudinal: SECOES NOMINAIS CONFERIDAS; COTAS DE VAOS A CONCLUIR.

Positiva pelas marcas: N3 2Ø16 +N4 1Ø16=3Ø16; elevação indica 4Ø12,5. Suspensão da V33 não atendida.

**Flexão positiva - solicitações Mk e resistência equivalente MRd/γf em tf·m.**

| Modelo/trecho | Apoios | b×h(cm) | Armadura | d(cm) | Mk | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V19/1 | PC47C-PC48C | 30×50 | 3Ø16 | 45,07 | 6,80 | 8,22 | ATENDE | ATENDE |


**Flexao negativa - maximo de cada lado do apoio; valores absolutos em tf·m.**

E=inicio do trecho; D=fim do trecho. Em apoio intermediario, fim do trecho anterior e inicio do seguinte sao verificacoes distintas.

| Trecho/lado | Apoio | h(cm) | Armadura superior | d(cm) | Mk negativo | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1/E | PC47C | 50 | 4Ø16 | 45,07 | 9,146 | 10,780 | ATENDE | ATENDE |
| 1/D | PC48C | 50 | 4Ø16 | 45,07 | 12,249 | 10,780 | ATENDE | NÃO ATENDE |


Mínimos: comparação de MRd do Concretopy com Md, mín=0,8W0 fctk, sup e taxa absoluta 0,15%, conforme 17.3.5.2.1. O arquivo bruto também conserva a avaliação tabelada do motor; ela não substitui a verificação com d efetivo. A falta de momento positivo não demonstra necessidade de armadura positiva mínima na face não tracionada.

**Cortante - Vk característico em tf; taxas em cm²/m.**

| Trecho | Intervalo modelo(m) | Estribo | d(cm) | Vk | Fornecida | Exigida | Área | s máximo L/T | Biela |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/15 | 45,07 | 12,49 | 4,16 | 3,85 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |


INTERVALO TQS INTEIRO (LIMITE): maior|Vk| de todas as 13 secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.

Passagem geométrica do vibrador 4 cm: atende entre estribos nas faixas calculadas. Esse controle não comprova ausência de congestionamento nos encontros. Espaçamento transversal entre ramos e respectivos limites estão preservados no resultado bruto; quatro ramos com peças sobrepostas dependem da disposição do corte.

Trecho 1: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

**Suspensão: ** V33→V19: INSUFICIENTE

Origem: detalhe 7401; recorte 7401_V19-20.png; esforços e resultados por modelo/trecho no JSON desta emissão. Cada linha conserva arquivo, número de linha e envoltória TQS.

### V20

Geometria nominal do detalhe: 30×50 cm. Forma/detalhamento: presença nominal confirmada. Comparação nominal de seções conforme inventário. Situacao longitudinal: SECOES NOMINAIS CONFERIDAS; COTAS DE VAOS A CONCLUIR.

Positiva pelas marcas: N3 2Ø16 +N4 1Ø16=3Ø16; elevação indica 4Ø12,5. Suspensão da V40 não atendida.

**Flexão positiva - solicitações Mk e resistência equivalente MRd/γf em tf·m.**

| Modelo/trecho | Apoios | b×h(cm) | Armadura | d(cm) | Mk | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V20/1 | PC49C-PC50C | 30×50 | 3Ø16 | 45,07 | 6,83 | 8,22 | ATENDE | ATENDE |


**Flexao negativa - maximo de cada lado do apoio; valores absolutos em tf·m.**

E=inicio do trecho; D=fim do trecho. Em apoio intermediario, fim do trecho anterior e inicio do seguinte sao verificacoes distintas.

| Trecho/lado | Apoio | h(cm) | Armadura superior | d(cm) | Mk negativo | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1/E | PC49C | 50 | 4Ø16 | 45,07 | 12,604 | 10,780 | ATENDE | NÃO ATENDE |
| 1/D | PC50C | 50 | 4Ø16 | 45,07 | 8,195 | 10,780 | ATENDE | ATENDE |


Mínimos: comparação de MRd do Concretopy com Md, mín=0,8W0 fctk, sup e taxa absoluta 0,15%, conforme 17.3.5.2.1. O arquivo bruto também conserva a avaliação tabelada do motor; ela não substitui a verificação com d efetivo. A falta de momento positivo não demonstra necessidade de armadura positiva mínima na face não tracionada.

**Cortante - Vk característico em tf; taxas em cm²/m.**

| Trecho | Intervalo modelo(m) | Estribo | d(cm) | Vk | Fornecida | Exigida | Área | s máximo L/T | Biela |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/15 | 45,07 | 12,61 | 4,16 | 3,85 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |


INTERVALO TQS INTEIRO (LIMITE): maior|Vk| de todas as 13 secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.

Passagem geométrica do vibrador 4 cm: atende entre estribos nas faixas calculadas. Esse controle não comprova ausência de congestionamento nos encontros. Espaçamento transversal entre ramos e respectivos limites estão preservados no resultado bruto; quatro ramos com peças sobrepostas dependem da disposição do corte.

Trecho 1: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

**Suspensão: ** V40→V20: INSUFICIENTE

Origem: detalhe 7401; recorte 7401_V19-20.png; esforços e resultados por modelo/trecho no JSON desta emissão. Cada linha conserva arquivo, número de linha e envoltória TQS.

### V21

Geometria nominal do detalhe: 30×50 cm. Forma/detalhamento: presença nominal confirmada. Comparação nominal de seções conforme inventário. Situacao longitudinal: SECOES NOMINAIS CONFERIDAS; COTAS DE VAOS A CONCLUIR.

PC56C/PC57C: adotados 5Ø20 de N5+N6; elevação indica 4Ø20. Estribos originaisØ8 c/17 nos quatro primeiros vãos; Ø6,3 c/15 nos dois últimos. Consulta a d/2 no PC55C autorizada após confirmação das cargas superiores e reação inferior. Face de PC54C no extremo esquerdo ainda não comprovada integralmente.

**Flexão positiva - solicitações Mk e resistência equivalente MRd/γf em tf·m.**

| Modelo/trecho | Apoios | b×h(cm) | Armadura | d(cm) | Mk | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V21/1 | PC54C-PC55C | 30×50 | 4Ø20 | 44,70 | 16,87 | 16,08 | ATENDE | NÃO ATENDE |
| V21/2 | PC55C-PC56C | 30×50 | 3Ø20 | 44,70 | 7,58 | 12,38 | ATENDE | ATENDE |
| V21/3 | PC56C-PC57C | 30×50 | 3Ø20 | 44,70 | 9,66 | 12,38 | ATENDE | ATENDE |
| V21/4 | PC57C-PC59C | 30×50 | 5Ø16 | 44,90 | 10,44 | 13,20 | ATENDE | ATENDE |
| V21/5 | PC59C-PC60C | 30×50 | 3Ø12,5 | 45,24 | 0,00 | 5,13 | SEM Mk POSITIVO | SEM MOMENTO POSITIVO NA ENVOLTÓRIA |
| V21/6 | PC60C-V22 | 30×50 | 4Ø12,5 | 45,24 | 3,83 | 6,77 | ATENDE | ATENDE |


**Flexao negativa - maximo de cada lado do apoio; valores absolutos em tf·m.**

E=inicio do trecho; D=fim do trecho. Em apoio intermediario, fim do trecho anterior e inicio do seguinte sao verificacoes distintas.

| Trecho/lado | Apoio | h(cm) | Armadura superior | d(cm) | Mk negativo | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1/E | PC54C | 50 | 4Ø10 | 45,20 | 0,000 | 4,390 | SEM MkNEGATIVO | ATENDE |
| 1/D | PC55C | 50 | 5Ø20 | 44,70 | 23,756 | 19,571 | ATENDE | NÃO ATENDE |
| 2/E | PC55C | 50 | 5Ø20 | 44,70 | 23,442 | 19,571 | ATENDE | NÃO ATENDE |
| 2/D | PC56C | 50 | 5Ø20 | 44,70 | 17,701 | 19,571 | ATENDE | ATENDE |
| 3/E | PC56C | 50 | 5Ø20 | 44,70 | 17,322 | 19,571 | ATENDE | ATENDE |
| 3/D | PC57C | 50 | 5Ø20 | 44,70 | 19,794 | 19,571 | ATENDE | NÃO ATENDE |
| 4/E | PC57C | 50 | 5Ø20 | 44,70 | 19,794 | 19,571 | ATENDE | NÃO ATENDE |
| 4/D | PC59C | 50 | 4Ø16 | 44,90 | 12,049 | 10,737 | ATENDE | NÃO ATENDE |
| 5/E | PC59C | 50 | 4Ø16 | 45,07 | 12,048 | 10,780 | ATENDE | NÃO ATENDE |
| 5/D | PC60C | 50 | 4Ø16 | 45,07 | 13,810 | 10,780 | ATENDE | NÃO ATENDE |
| 6/E | PC60C | 50 | 4Ø16 | 45,07 | 13,485 | 10,780 | ATENDE | NÃO ATENDE |
| 6/D | V22 | 50 | 2Ø10 | 45,37 | 0,000 | 2,230 | SEM MkNEGATIVO | ATENDE |


Mínimos: comparação de MRd do Concretopy com Md, mín=0,8W0 fctk, sup e taxa absoluta 0,15%, conforme 17.3.5.2.1. O arquivo bruto também conserva a avaliação tabelada do motor; ela não substitui a verificação com d efetivo. A falta de momento positivo não demonstra necessidade de armadura positiva mínima na face não tracionada.

**Cortante - Vk característico em tf; taxas em cm²/m.**

| Trecho | Intervalo modelo(m) | Estribo | d(cm) | Vk | Fornecida | Exigida | Área | s máximo L/T | Biela |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0,15-7,68 | 2 r Ø8,0 c/17 | 44,70 | 15,91 | 5,91 | 5,11 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 2 | 0,35-7,70 | 2 r Ø8,0 c/17 | 44,70 | 15,31 | 5,91 | 4,63 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 3 | 0,35-7,70 | 2 r Ø8,0 c/17 | 44,70 | 13,20 | 5,91 | 3,85 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 4 | 0,35-7,70 | 2 r Ø8,0 c/17 | 44,70 | 14,37 | 5,91 | 3,90 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 5 | 0,35-3,70 | 2 r Ø6,3 c/15 | 45,07 | 9,16 | 4,16 | 3,85 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 6 | 0,35-4,06 | 2 r Ø6,3 c/15 | 45,07 | 10,19 | 4,16 | 3,85 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |


INTERVALO TQS INTEIRO (LIMITE): maior|Vk| de todas as 13 secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.

Passagem geométrica do vibrador 4 cm: atende entre estribos nas faixas calculadas. Esse controle não comprova ausência de congestionamento nos encontros. Espaçamento transversal entre ramos e respectivos limites estão preservados no resultado bruto; quatro ramos com peças sobrepostas dependem da disposição do corte.

Trecho 1: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

Trecho 1: d/2 no PC55C; condições confirmadas por João. O cortante sem redução e a consulta adotada são preservados separadamente no JSON.

**Suspensão: ** V21→V22: TIRANTE INTEGRAL A COMPROVAR

Origem: detalhe 7402; recorte 7402_V21.png; esforços e resultados por modelo/trecho no JSON desta emissão. Cada linha conserva arquivo, número de linha e envoltória TQS.

### V22

Geometria nominal do detalhe: 30×50 cm. Forma/detalhamento: presença nominal confirmada. Comparação nominal de seções conforme inventário. Situacao longitudinal: SECOES NOMINAIS CONFERIDAS; COTAS DE VAOS A CONCLUIR.

Adotados 2Ø12,5 de N1; elevacao indica 2Ø16. Suspensao da V21 avaliada em 25 cm unilaterais; 75% atende, mas quantidade efetiva/reparticao do tirante integral ainda nao comprovada.

**Flexão positiva - solicitações Mk e resistência equivalente MRd/γf em tf·m.**

| Modelo/trecho | Apoios | b×h(cm) | Armadura | d(cm) | Mk | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V22/2 | PC62C-PC61C | 30×50 | 4Ø12,5 | 45,24 | 4,80 | 6,77 | ATENDE | ATENDE |
| V22/3 | PC61C-PC58C | 30×50 | 4Ø16 | 45,07 | 7,00 | 10,78 | ATENDE | ATENDE |
| V22/1B | EXTREMIDADE_LIVRE-PC62C | 30×50 | 2Ø12,5 | 45,24 | 0,36 | 3,45 | ATENDE | ATENDE |


**Flexao negativa - maximo de cada lado do apoio; valores absolutos em tf·m.**

E=inicio do trecho; D=fim do trecho. Em apoio intermediario, fim do trecho anterior e inicio do seguinte sao verificacoes distintas.

| Trecho/lado | Apoio | h(cm) | Armadura superior | d(cm) | Mk negativo | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2/E | PC62C | 50 | 2Ø12,5 | 45,24 | 1,281 | 3,452 | ATENDE | ATENDE |
| 2/D | PC61C | 50 | 3Ø20 | 44,87 | 10,466 | 12,433 | ATENDE | ATENDE |
| 3/E | PC61C | 50 | 3Ø20 | 44,87 | 10,762 | 12,433 | ATENDE | ATENDE |
| 3/D | PC58C | 50 | 2Ø10 | 45,37 | 0,000 | 2,230 | SEM MkNEGATIVO | ATENDE |
| 1B/E | EXTREMIDADE_LIVRE | 50 | 2Ø12,5 | 45,24 | 0,000 | 3,452 | SEM MkNEGATIVO | ATENDE |
| 1B/D | PC62C | 50 | 2Ø12,5 | 45,24 | 1,279 | 3,452 | ATENDE | ATENDE |


Mínimos: comparação de MRd do Concretopy com Md, mín=0,8W0 fctk, sup e taxa absoluta 0,15%, conforme 17.3.5.2.1. O arquivo bruto também conserva a avaliação tabelada do motor; ela não substitui a verificação com d efetivo. A falta de momento positivo não demonstra necessidade de armadura positiva mínima na face não tracionada.

**Cortante - Vk característico em tf; taxas em cm²/m.**

| Trecho | Intervalo modelo(m) | Estribo | d(cm) | Vk | Fornecida | Exigida | Área | s máximo L/T | Biela |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/15 | 44,87 | 11,51 | 4,16 | 3,85 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 3 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/15 | 44,87 | 14,04 | 4,16 | 3,85 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 1B | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/15 | 45,24 | 4,05 | 4,16 | 3,85 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |


INTERVALO TQS INTEIRO (LIMITE): maior|Vk| de todas as 13 secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.

Passagem geométrica do vibrador 4 cm: atende entre estribos nas faixas calculadas. Esse controle não comprova ausência de congestionamento nos encontros. Espaçamento transversal entre ramos e respectivos limites estão preservados no resultado bruto; quatro ramos com peças sobrepostas dependem da disposição do corte.

Trecho 2: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

Trecho 3: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

Trecho 1B: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

**Suspensão: ** V21→V22: TIRANTE INTEGRAL A COMPROVAR

Origem: detalhe 7402; recorte 7402_V22.png; esforços e resultados por modelo/trecho no JSON desta emissão. Cada linha conserva arquivo, número de linha e envoltória TQS.

### V23

Geometria nominal do detalhe: 30×80 cm; 30×50 cm. Forma/detalhamento: presença nominal confirmada. Comparação nominal de seções conforme inventário. Situacao longitudinal: SECOES NOMINAIS CONFERIDAS; COTAS DE VAOS A CONCLUIR.

Secoes nominais no pico e nos apoios identificadas para flexao; transicoes internas mantidas separadamente. No P785, o lado V23 usa 12,997 tf.m e o lado V24 usa 11,640 tf.m; verificar separadamente. Capacidade 4Ø16 emh 50=10,780 tf.m, insuficiente.

**Flexão positiva - solicitações Mk e resistência equivalente MRd/γf em tf·m.**

| Modelo/trecho | Apoios | b×h(cm) | Armadura | d(cm) | Mk | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V23/1 | PC54C-P799 | 30×80 | 3Ø16 | 75,07 | 1,49 | 13,95 | ATENDE | ATENDE |
| V23/2 | P799-P785 | 30×50 | 4Ø16 | 45,07 | 9,47 | 10,78 | ATENDE | ATENDE |


**Flexao negativa - maximo de cada lado do apoio; valores absolutos em tf·m.**

E=inicio do trecho; D=fim do trecho. Em apoio intermediario, fim do trecho anterior e inicio do seguinte sao verificacoes distintas.

| Trecho/lado | Apoio | h(cm) | Armadura superior | d(cm) | Mk negativo | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1/E | PC54C | 80 | 2Ø16 | 75,07 | 0,000 | 9,385 | SEM MkNEGATIVO | ATENDE |
| 1/D | P799 | 80 | 3Ø16 | 75,07 | 6,515 | 13,947 | ATENDE | ATENDE |
| 2/E | P799 | 50 | 2Ø16 | 45,07 | 8,639 | 5,565 | ATENDE | NÃO ATENDE |
| 2/D | P785 | 50 | 4Ø16 | 45,07 | 12,997 | 10,780 | ATENDE | NÃO ATENDE |


Mínimos: comparação de MRd do Concretopy com Md, mín=0,8W0 fctk, sup e taxa absoluta 0,15%, conforme 17.3.5.2.1. O arquivo bruto também conserva a avaliação tabelada do motor; ela não substitui a verificação com d efetivo. A falta de momento positivo não demonstra necessidade de armadura positiva mínima na face não tracionada.

**Cortante - Vk característico em tf; taxas em cm²/m.**

| Trecho | Intervalo modelo(m) | Estribo | d(cm) | Vk | Fornecida | Exigida | Área | s máximo L/T | Biela |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/15 | 75,07 | 6,08 | 4,16 | 3,85 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 2 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/15 | 45,07 | 12,11 | 4,16 | 3,85 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |


INTERVALO TQS INTEIRO (LIMITE): maior|Vk| de todas as 13 secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.

Passagem geométrica do vibrador 4 cm: atende entre estribos nas faixas calculadas. Esse controle não comprova ausência de congestionamento nos encontros. Espaçamento transversal entre ramos e respectivos limites estão preservados no resultado bruto; quatro ramos com peças sobrepostas dependem da disposição do corte.

Trecho 1: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

Trecho 2: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

**Suspensão: ** V17→V23: SENTIDO DA TRANSFERENCIA: ANALISE DE JOAO; V18→V23: ATENDE

Origem: detalhe 7402; recorte 7402_V23.png; esforços e resultados por modelo/trecho no JSON desta emissão. Cada linha conserva arquivo, número de linha e envoltória TQS.

### V24

Geometria nominal do detalhe: 30×80 cm; 30×50 cm. Forma/detalhamento: presença nominal confirmada. Comparação nominal de seções conforme inventário. Situacao longitudinal: SECOES NOMINAIS CONFERIDAS; COTAS DE VAOS A CONCLUIR.

Primeiro intervalo fisico P785-P778=modelo V23/3; demais=modelo V24. No P778 adotados 4Ø16 N16, nao 2Ø10 porta-estribo N18: capacidade 10,780 tf.m supera 8,565 tf.m. No P785, este lado V24 usa 11,640 tf.m; o lado V23 usa 12,997 tf.m, sem unificar as verificacoes. No P778-P769 positiva 3,995 tf.m supera 3,452 tf.m de 2Ø12,5 emh 50.

**Flexão positiva - solicitações Mk e resistência equivalente MRd/γf em tf·m.**

| Modelo/trecho | Apoios | b×h(cm) | Armadura | d(cm) | Mk | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V23/3 | P785-P778 | 30×80 | 5Ø20 | 74,87 | 13,44 | 34,58 | ATENDE | ATENDE |
| V24/1 | P778-P769 | 30×50 | 2Ø12,5 | 45,24 | 4,00 | 3,45 | ATENDE | NÃO ATENDE |
| V24/2 | P769-P759 | 30×50 | 2Ø20 | 44,87 | 5,70 | 8,50 | ATENDE | ATENDE |
| V24/3 | P759-PC25C | 30×50 | 2Ø20 | 44,87 | 0,55 | 8,50 | ATENDE | ATENDE |


**Flexao negativa - maximo de cada lado do apoio; valores absolutos em tf·m.**

E=inicio do trecho; D=fim do trecho. Em apoio intermediario, fim do trecho anterior e inicio do seguinte sao verificacoes distintas.

| Trecho/lado | Apoio | h(cm) | Armadura superior | d(cm) | Mk negativo | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3/E | P785 | 80 | 4Ø16 | 75,07 | 11,640 | 18,421 | ATENDE | ATENDE |
| 3/D | P778 | 80 | 4Ø16 | 75,07 | 8,565 | 18,421 | ATENDE | ATENDE |
| 1/E | P778 | 50 | 4Ø16 | 45,07 | 3,289 | 10,780 | ATENDE | ATENDE |
| 1/D | P769 | 50 | 4Ø12,5 | 45,24 | 7,560 | 6,773 | ATENDE | NÃO ATENDE |
| 2/E | P769 | 50 | 4Ø12,5 | 45,24 | 10,745 | 6,773 | ATENDE | NÃO ATENDE |
| 2/D | P759 | 50 | 4Ø12,5 | 45,24 | 9,792 | 6,773 | ATENDE | NÃO ATENDE |
| 3/E | P759 | 50 | 4Ø12,5 | 45,24 | 1,161 | 6,773 | ATENDE | ATENDE |
| 3/D | PC25C | 50 | 2Ø12,5 | 45,24 | 0,777 | 3,452 | ATENDE | ATENDE |


Mínimos: comparação de MRd do Concretopy com Md, mín=0,8W0 fctk, sup e taxa absoluta 0,15%, conforme 17.3.5.2.1. O arquivo bruto também conserva a avaliação tabelada do motor; ela não substitui a verificação com d efetivo. A falta de momento positivo não demonstra necessidade de armadura positiva mínima na face não tracionada.

**Cortante - Vk característico em tf; taxas em cm²/m.**

| Trecho | Intervalo modelo(m) | Estribo | d(cm) | Vk | Fornecida | Exigida | Área | s máximo L/T | Biela |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/15 | 74,87 | 10,90 | 4,16 | 3,85 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 1 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/15 | 45,07 | 6,54 | 4,16 | 3,85 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 2 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/15 | 44,87 | 8,75 | 4,16 | 3,85 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 3 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/15 | 44,87 | 2,26 | 4,16 | 3,85 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |


INTERVALO TQS INTEIRO (LIMITE): maior|Vk| de todas as 13 secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.

Passagem geométrica do vibrador 4 cm: atende entre estribos nas faixas calculadas. Esse controle não comprova ausência de congestionamento nos encontros. Espaçamento transversal entre ramos e respectivos limites estão preservados no resultado bruto; quatro ramos com peças sobrepostas dependem da disposição do corte.

Trecho 3: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

Trecho 1: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

Trecho 2: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

Trecho 3: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

**Suspensão: ** sem ligação indireta física identificada no inventário deste modelo.

Origem: detalhe 7402; recorte 7402_V24.png; esforços e resultados por modelo/trecho no JSON desta emissão. Cada linha conserva arquivo, número de linha e envoltória TQS.

### V25

Geometria nominal do detalhe: 30×50 cm. Forma/detalhamento: presença nominal confirmada. Comparação nominal de seções conforme inventário. Situacao longitudinal: SECOES NOMINAIS CONFERIDAS; COTAS DE VAOS A CONCLUIR.

**Flexão positiva - solicitações Mk e resistência equivalente MRd/γf em tf·m.**

| Modelo/trecho | Apoios | b×h(cm) | Armadura | d(cm) | Mk | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V25/2 | P745-P730 | 30×50 | 3Ø20 | 44,87 | 8,70 | 12,43 | ATENDE | ATENDE |
| V25/3 | P730-P727 | 30×50 | 2Ø20 | 44,87 | 3,68 | 8,50 | ATENDE | ATENDE |
| V25/4 | P727-P708 | 30×50 | 3Ø12,5 | 45,24 | 7,50 | 5,13 | ATENDE | NÃO ATENDE |
| V25/5 | P708-P701 | 30×50 | 2Ø12,5 | 45,24 | 1,38 | 3,45 | ATENDE | ATENDE |
| V25/1B | EXTREMIDADE_LIVRE-P745 | 30×50 | 3Ø20 | 44,87 | 0,00 | 12,43 | SEM Mk POSITIVO | SEM MOMENTO POSITIVO NA ENVOLTÓRIA |


**Flexao negativa - maximo de cada lado do apoio; valores absolutos em tf·m.**

E=inicio do trecho; D=fim do trecho. Em apoio intermediario, fim do trecho anterior e inicio do seguinte sao verificacoes distintas.

| Trecho/lado | Apoio | h(cm) | Armadura superior | d(cm) | Mk negativo | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2/E | P745 | 50 | 4Ø16 | 45,07 | 8,961 | 10,780 | ATENDE | ATENDE |
| 2/D | P730 | 50 | 4Ø16 | 45,07 | 16,625 | 10,780 | ATENDE | NÃO ATENDE |
| 3/E | P730 | 50 | 4Ø16 | 45,07 | 6,915 | 10,780 | ATENDE | ATENDE |
| 3/D | P727 | 50 | 2Ø16 | 45,07 | 6,498 | 5,565 | ATENDE | NÃO ATENDE |
| 4/E | P727 | 50 | 2Ø16 | 45,07 | 13,317 | 5,565 | ATENDE | NÃO ATENDE |
| 4/D | P708 | 50 | 3Ø12,5 | 45,24 | 8,308 | 5,129 | ATENDE | NÃO ATENDE |
| 5/E | P708 | 50 | 3Ø12,5 | 45,24 | 3,210 | 5,129 | ATENDE | ATENDE |
| 5/D | P701 | 50 | 3Ø10 | 45,37 | 0,659 | 3,325 | ATENDE | ATENDE |
| 1B/E | EXTREMIDADE_LIVRE | 50 | 4Ø16 | 45,07 | 0,016 | 10,780 | ATENDE | ATENDE |
| 1B/D | P745 | 50 | 4Ø16 | 45,07 | 0,520 | 10,780 | ATENDE | ATENDE |


Mínimos: comparação de MRd do Concretopy com Md, mín=0,8W0 fctk, sup e taxa absoluta 0,15%, conforme 17.3.5.2.1. O arquivo bruto também conserva a avaliação tabelada do motor; ela não substitui a verificação com d efetivo. A falta de momento positivo não demonstra necessidade de armadura positiva mínima na face não tracionada.

**Cortante - Vk característico em tf; taxas em cm²/m.**

| Trecho | Intervalo modelo(m) | Estribo | d(cm) | Vk | Fornecida | Exigida | Área | s máximo L/T | Biela |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/15 | 44,87 | 10,70 | 4,16 | 3,85 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 3 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/15 | 45,07 | 5,76 | 4,16 | 3,85 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 4 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/15 | 45,07 | 8,77 | 4,16 | 3,85 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 5 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/15 | 45,24 | 6,22 | 4,16 | 3,85 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 1B | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/15 | 44,87 | 1,08 | 4,16 | 3,85 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |


INTERVALO TQS INTEIRO (LIMITE): maior|Vk| de todas as 13 secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.

Passagem geométrica do vibrador 4 cm: atende entre estribos nas faixas calculadas. Esse controle não comprova ausência de congestionamento nos encontros. Espaçamento transversal entre ramos e respectivos limites estão preservados no resultado bruto; quatro ramos com peças sobrepostas dependem da disposição do corte.

Trecho 2: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

Trecho 3: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

Trecho 4: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

Trecho 5: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

Trecho 1B: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

**Suspensão: ** V26→V25: ATENDE

Origem: detalhe 7402; recorte 7402_V25.png; esforços e resultados por modelo/trecho no JSON desta emissão. Cada linha conserva arquivo, número de linha e envoltória TQS.

### V26

Geometria nominal do detalhe: 19×50 cm. Forma/detalhamento: presença nominal confirmada. Comparação nominal de seções conforme inventário. Situacao longitudinal: SECOES NOMINAIS CONFERIDAS; COTAS DE VAOS A CONCLUIR.

Rotulos de apoios no detalhe divergem da forma; identidade fisica adotada. Suspensao de V26 na V25 atende 100% do tirante. V49 tem apoio direto confirmado no bloco PC21C, excluido da suspensao em V26.

**Flexão positiva - solicitações Mk e resistência equivalente MRd/γf em tf·m.**

| Modelo/trecho | Apoios | b×h(cm) | Armadura | d(cm) | Mk | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V26/1 | PC25C-PC21C | 19×50 | 2Ø16 | 45,07 | 0,24 | 5,46 | ATENDE | ATENDE |
| V26/2 | PC21C-PC19C | 19×50 | 2Ø16 | 45,07 | 0,47 | 5,46 | ATENDE | ATENDE |
| V26/3 | PC19C-V25 | 19×50 | 2Ø16 | 45,07 | 0,21 | 5,46 | ATENDE | ATENDE |


**Flexao negativa - maximo de cada lado do apoio; valores absolutos em tf·m.**

E=inicio do trecho; D=fim do trecho. Em apoio intermediario, fim do trecho anterior e inicio do seguinte sao verificacoes distintas.

| Trecho/lado | Apoio | h(cm) | Armadura superior | d(cm) | Mk negativo | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1/E | PC25C | 50 | 2Ø16 | 45,07 | 0,566 | 5,464 | ATENDE | ATENDE |
| 1/D | PC21C | 50 | 2Ø16 | 45,07 | 3,521 | 5,464 | ATENDE | ATENDE |
| 2/E | PC21C | 50 | 2Ø16 | 45,07 | 2,188 | 5,464 | ATENDE | ATENDE |
| 2/D | PC19C | 50 | 2Ø16 | 45,07 | 0,689 | 5,464 | ATENDE | ATENDE |
| 3/E | PC19C | 50 | 2Ø16 | 45,07 | 1,726 | 5,464 | ATENDE | ATENDE |
| 3/D | V25 | 50 | 2Ø16 | 45,07 | 0,030 | 5,464 | ATENDE | ATENDE |


Mínimos: comparação de MRd do Concretopy com Md, mín=0,8W0 fctk, sup e taxa absoluta 0,15%, conforme 17.3.5.2.1. O arquivo bruto também conserva a avaliação tabelada do motor; ela não substitui a verificação com d efetivo. A falta de momento positivo não demonstra necessidade de armadura positiva mínima na face não tracionada.

**Cortante - Vk característico em tf; taxas em cm²/m.**

| Trecho | Intervalo modelo(m) | Estribo | d(cm) | Vk | Fornecida | Exigida | Área | s máximo L/T | Biela |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/15 | 45,07 | 7,96 | 4,16 | 2,44 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 2 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/15 | 45,07 | 8,69 | 4,16 | 2,44 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 3 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/15 | 45,07 | 3,74 | 4,16 | 2,44 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |


INTERVALO TQS INTEIRO (LIMITE): maior|Vk| de todas as 13 secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.

Passagem geométrica do vibrador 4 cm: atende entre estribos nas faixas calculadas. Esse controle não comprova ausência de congestionamento nos encontros. Espaçamento transversal entre ramos e respectivos limites estão preservados no resultado bruto; quatro ramos com peças sobrepostas dependem da disposição do corte.

Trecho 1: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

Trecho 2: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

Trecho 3: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

**Suspensão: ** V49→V26: APOIO DIRETO PC21C; SUSPENSAO NAO SE APLICA; V26→V25: ATENDE

Origem: detalhe 7402; recorte 7402_V26.png; esforços e resultados por modelo/trecho no JSON desta emissão. Cada linha conserva arquivo, número de linha e envoltória TQS.

### V27

Geometria nominal do detalhe: 24×50 cm. Forma/detalhamento: presença nominal confirmada. Comparação nominal de seções conforme inventário. Situacao longitudinal: SECOES NOMINAIS CONFERIDAS; COTAS DE VAOS A CONCLUIR.

**Flexão positiva - solicitações Mk e resistência equivalente MRd/γf em tf·m.**

| Modelo/trecho | Apoios | b×h(cm) | Armadura | d(cm) | Mk | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V27/1 | P750-P739 | 24×50 | 2Ø20 | 44,70 | 4,69 | 8,36 | ATENDE | ATENDE |


**Flexao negativa - maximo de cada lado do apoio; valores absolutos em tf·m.**

E=inicio do trecho; D=fim do trecho. Em apoio intermediario, fim do trecho anterior e inicio do seguinte sao verificacoes distintas.

| Trecho/lado | Apoio | h(cm) | Armadura superior | d(cm) | Mk negativo | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1/E | P750 | 50 | 4Ø16 | 44,90 | 7,944 | 10,562 | ATENDE | ATENDE |
| 1/D | P739 | 50 | 2Ø16 | 44,90 | 2,342 | 5,500 | ATENDE | ATENDE |


Mínimos: comparação de MRd do Concretopy com Md, mín=0,8W0 fctk, sup e taxa absoluta 0,15%, conforme 17.3.5.2.1. O arquivo bruto também conserva a avaliação tabelada do motor; ela não substitui a verificação com d efetivo. A falta de momento positivo não demonstra necessidade de armadura positiva mínima na face não tracionada.

**Cortante - Vk característico em tf; taxas em cm²/m.**

| Trecho | Intervalo modelo(m) | Estribo | d(cm) | Vk | Fornecida | Exigida | Área | s máximo L/T | Biela |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø8,0 c/12 | 44,90 | 17,01 | 8,38 | 7,39 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |


INTERVALO TQS INTEIRO (LIMITE): maior|Vk| de todas as 13 secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.

Passagem geométrica do vibrador 4 cm: atende entre estribos nas faixas calculadas. Esse controle não comprova ausência de congestionamento nos encontros. Espaçamento transversal entre ramos e respectivos limites estão preservados no resultado bruto; quatro ramos com peças sobrepostas dependem da disposição do corte.

Trecho 1: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

**Suspensão: ** sem ligação indireta física identificada no inventário deste modelo.

Origem: detalhe 7402; recorte 7402_V27.png; esforços e resultados por modelo/trecho no JSON desta emissão. Cada linha conserva arquivo, número de linha e envoltória TQS.

### V28

Geometria nominal do detalhe: 40×50 cm. Forma/detalhamento: presença nominal confirmada. Comparação nominal de seções conforme inventário. Situacao longitudinal: SECOES NOMINAIS CONFERIDAS; COTAS DE VAOS A CONCLUIR.

**Flexão positiva - solicitações Mk e resistência equivalente MRd/γf em tf·m.**

| Modelo/trecho | Apoios | b×h(cm) | Armadura | d(cm) | Mk | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V28/1 | PC34C-PC28C | 40×50 | 4Ø20 | 44,87 | 11,91 | 16,58 | ATENDE | ATENDE |
| V28/2 | PC28C-V15 | 40×50 | 4Ø16 | 45,07 | 3,45 | 10,96 | ATENDE | ATENDE |


**Flexao negativa - maximo de cada lado do apoio; valores absolutos em tf·m.**

E=inicio do trecho; D=fim do trecho. Em apoio intermediario, fim do trecho anterior e inicio do seguinte sao verificacoes distintas.

| Trecho/lado | Apoio | h(cm) | Armadura superior | d(cm) | Mk negativo | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1/E | PC34C | 50 | 4Ø16 | 45,07 | 16,549 | 10,955 | ATENDE | NÃO ATENDE |
| 1/D | PC28C | 50 | 4Ø20 | 44,87 | 15,344 | 16,577 | ATENDE | ATENDE |
| 2/E | PC28C | 50 | 4Ø20 | 44,87 | 16,067 | 16,577 | ATENDE | ATENDE |
| 2/D | V15 | 50 | 4Ø10 | 45,37 | 0,000 | 4,434 | SEM MkNEGATIVO | ATENDE |


Mínimos: comparação de MRd do Concretopy com Md, mín=0,8W0 fctk, sup e taxa absoluta 0,15%, conforme 17.3.5.2.1. O arquivo bruto também conserva a avaliação tabelada do motor; ela não substitui a verificação com d efetivo. A falta de momento positivo não demonstra necessidade de armadura positiva mínima na face não tracionada.

**Cortante - Vk característico em tf; taxas em cm²/m.**

| Trecho | Intervalo modelo(m) | Estribo | d(cm) | Vk | Fornecida | Exigida | Área | s máximo L/T | Biela |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | INTERVALO TQS INTEIRO (LIMITE) | 4 r Ø6,3 c/15 | 44,87 | 17,73 | 8,31 | 5,14 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 2 | INTERVALO TQS INTEIRO (LIMITE) | 4 r Ø6,3 c/15 | 44,87 | 15,19 | 8,31 | 5,14 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |


INTERVALO TQS INTEIRO (LIMITE): maior|Vk| de todas as 13 secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.

Passagem geométrica do vibrador 4 cm: atende entre estribos nas faixas calculadas. Esse controle não comprova ausência de congestionamento nos encontros. Espaçamento transversal entre ramos e respectivos limites estão preservados no resultado bruto; quatro ramos com peças sobrepostas dependem da disposição do corte.

Trecho 1: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

Trecho 2: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

**Suspensão: ** V28→V15: ATENDE

Origem: detalhe 7402; recorte 7402_V28.png; esforços e resultados por modelo/trecho no JSON desta emissão. Cada linha conserva arquivo, número de linha e envoltória TQS.

### V29

Geometria nominal do detalhe: 19×165 cm. Forma/detalhamento: presença nominal confirmada. Comparação nominal de seções conforme inventário. Situacao longitudinal: SECOES NOMINAIS CONFERIDAS; COTAS DE VAOS A CONCLUIR.

Somente 2Ø10 finais considerados no topo; 3Ø16 intermediários excluídos. Positiva 3Ø20 em duas camadas[2,1]. Conferir ancoragem e funcionamento conjunto dos estribos 138/50 cm.

**Flexão positiva - solicitações Mk e resistência equivalente MRd/γf em tf·m.**

| Modelo/trecho | Apoios | b×h(cm) | Armadura | d(cm) | Mk | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V29/1 | P753-P740 | 19×165 | 3Ø20 / camadas [2, 1] | 158,54 | 38,06 | 45,80 | ATENDE | ATENDE |


**Flexao negativa - maximo de cada lado do apoio; valores absolutos em tf·m.**

E=inicio do trecho; D=fim do trecho. Em apoio intermediario, fim do trecho anterior e inicio do seguinte sao verificacoes distintas.

| Trecho/lado | Apoio | h(cm) | Armadura superior | d(cm) | Mk negativo | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1/E | P753 | 165 | 2Ø10 | 160,37 | 1,128 | 7,935 | NÃO ATENDE | ATENDE |
| 1/D | P740 | 165 | 2Ø10 | 160,37 | 1,155 | 7,935 | NÃO ATENDE | ATENDE |


Mínimo não atendido no apoio P753: As=1,57 cm²; mínimo absoluto=4,70 cm²; momento mínimo equivalente=20,96 tf·m; resistência equivalente=7,94 tf·m.

Mínimo não atendido no apoio P740: As=1,57 cm²; mínimo absoluto=4,70 cm²; momento mínimo equivalente=20,96 tf·m; resistência equivalente=7,94 tf·m.

Mínimos: comparação de MRd do Concretopy com Md, mín=0,8W0 fctk, sup e taxa absoluta 0,15%, conforme 17.3.5.2.1. O arquivo bruto também conserva a avaliação tabelada do motor; ela não substitui a verificação com d efetivo. A falta de momento positivo não demonstra necessidade de armadura positiva mínima na face não tracionada.

**Cortante - Vk característico em tf; taxas em cm²/m.**

| Trecho | Intervalo modelo(m) | Estribo | d(cm) | Vk | Fornecida | Exigida | Área | s máximo L/T | Biela |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/17 | 158,54 | 21,65 | 3,67 | 2,44 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |


INTERVALO TQS INTEIRO (LIMITE): maior|Vk| de todas as 13 secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.

Passagem geométrica do vibrador 4 cm: atende entre estribos nas faixas calculadas. Esse controle não comprova ausência de congestionamento nos encontros. Espaçamento transversal entre ramos e respectivos limites estão preservados no resultado bruto; quatro ramos com peças sobrepostas dependem da disposição do corte.

Trecho 1: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

**Suspensão: ** V7→V29: AREA ATENDE; FECHAMENTO DOS ESTRIBOS A VERIFICAR; V9→V29: AREA ATENDE; FECHAMENTO DOS ESTRIBOS A VERIFICAR

Origem: detalhe 7402; recorte 7402_V29-39.png; esforços e resultados por modelo/trecho no JSON desta emissão. Cada linha conserva arquivo, número de linha e envoltória TQS.

### V30

Geometria nominal do detalhe: 24×60 cm. Forma/detalhamento: presença nominal confirmada. Comparação nominal de seções conforme inventário. Situacao longitudinal: SECOES NOMINAIS CONFERIDAS; COTAS DE VAOS A CONCLUIR.

**Flexão positiva - solicitações Mk e resistência equivalente MRd/γf em tf·m.**

| Modelo/trecho | Apoios | b×h(cm) | Armadura | d(cm) | Mk | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V30/1 | PC2C-P710 | 24×60 | 3Ø16 | 55,07 | 7,14 | 10,03 | ATENDE | ATENDE |


**Flexao negativa - maximo de cada lado do apoio; valores absolutos em tf·m.**

E=inicio do trecho; D=fim do trecho. Em apoio intermediario, fim do trecho anterior e inicio do seguinte sao verificacoes distintas.

| Trecho/lado | Apoio | h(cm) | Armadura superior | d(cm) | Mk negativo | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1/E | PC2C | 60 | 3Ø12,5 | 55,24 | 10,262 | 6,258 | ATENDE | NÃO ATENDE |
| 1/D | P710 | 60 | 3Ø16 | 55,07 | 9,577 | 10,028 | ATENDE | ATENDE |


Mínimos: comparação de MRd do Concretopy com Md, mín=0,8W0 fctk, sup e taxa absoluta 0,15%, conforme 17.3.5.2.1. O arquivo bruto também conserva a avaliação tabelada do motor; ela não substitui a verificação com d efetivo. A falta de momento positivo não demonstra necessidade de armadura positiva mínima na face não tracionada.

**Cortante - Vk característico em tf; taxas em cm²/m.**

| Trecho | Intervalo modelo(m) | Estribo | d(cm) | Vk | Fornecida | Exigida | Área | s máximo L/T | Biela |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/12 | 55,07 | 14,41 | 5,20 | 3,27 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |


INTERVALO TQS INTEIRO (LIMITE): maior|Vk| de todas as 13 secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.

Passagem geométrica do vibrador 4 cm: atende entre estribos nas faixas calculadas. Esse controle não comprova ausência de congestionamento nos encontros. Espaçamento transversal entre ramos e respectivos limites estão preservados no resultado bruto; quatro ramos com peças sobrepostas dependem da disposição do corte.

Trecho 1: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

**Suspensão: ** sem ligação indireta física identificada no inventário deste modelo.

Origem: detalhe 7402; recorte 7402_V30.png; esforços e resultados por modelo/trecho no JSON desta emissão. Cada linha conserva arquivo, número de linha e envoltória TQS.

### V31

Geometria nominal do detalhe: 19×165 cm. Forma/detalhamento: presença nominal confirmada. Comparação nominal de seções conforme inventário. Situacao longitudinal: EIXOS DOS CRUZAMENTOS E FAIXAS CONCILIADOS.

Inicio 1B no eixo V12, confirmado por Joao. V31 descarrega em V12. Cruzamentos V9/V7 a 2,325/3,545 m; face P746 a 5,275 m e faixa 515 cm conciliadas. Suspensoes V7/V9 com diagrama regional atendem numericamente; funcionamento das pecas compostas pendente.

**Flexão positiva - solicitações Mk e resistência equivalente MRd/γf em tf·m.**

| Modelo/trecho | Apoios | b×h(cm) | Armadura | d(cm) | Mk | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V31/1B | EXTREMIDADE_LIVRE-P746 | 19×165 | 4Ø20 / camadas [2, 2] | 157,87 | 36,98 | 60,13 | ATENDE | ATENDE |
| V31/2 | P746-P746 | 19×165 | 4Ø20 / camadas [2, 2] | 157,87 | 0,72 | 60,13 | ATENDE | ATENDE |


**Flexao negativa - maximo de cada lado do apoio; valores absolutos em tf·m.**

E=inicio do trecho; D=fim do trecho. Em apoio intermediario, fim do trecho anterior e inicio do seguinte sao verificacoes distintas.

| Trecho/lado | Apoio | h(cm) | Armadura superior | d(cm) | Mk negativo | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1B/E | EXTREMIDADE_LIVRE | 165 | 2Ø10 | 160,37 | 0,473 | 7,935 | NÃO ATENDE | ATENDE |
| 1B/D | P746 | 165 | 2Ø10 | 160,37 | 17,342 | 7,935 | NÃO ATENDE | NÃO ATENDE |
| 2/E | P746 | 165 | 2Ø10 | 160,37 | 0,375 | 7,935 | NÃO ATENDE | ATENDE |
| 2/D | P746 | 165 | 2Ø10 | 160,37 | 0,000 | 7,935 | SEM MkNEGATIVO | ATENDE |


Mínimo não atendido no apoio EXTREMIDADE_LIVRE: As=1,57 cm²; mínimo absoluto=4,70 cm²; momento mínimo equivalente=20,96 tf·m; resistência equivalente=7,94 tf·m.

Mínimo não atendido no apoio P746: As=1,57 cm²; mínimo absoluto=4,70 cm²; momento mínimo equivalente=20,96 tf·m; resistência equivalente=7,94 tf·m.

Mínimo não atendido no apoio P746: As=1,57 cm²; mínimo absoluto=4,70 cm²; momento mínimo equivalente=20,96 tf·m; resistência equivalente=7,94 tf·m.

Mínimos: comparação de MRd do Concretopy com Md, mín=0,8W0 fctk, sup e taxa absoluta 0,15%, conforme 17.3.5.2.1. O arquivo bruto também conserva a avaliação tabelada do motor; ela não substitui a verificação com d efetivo. A falta de momento positivo não demonstra necessidade de armadura positiva mínima na face não tracionada.

**Cortante - Vk característico em tf; taxas em cm²/m.**

| Trecho | Intervalo modelo(m) | Estribo | d(cm) | Vk | Fornecida | Exigida | Área | s máximo L/T | Biela |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1B | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/17 | 157,87 | 26,09 | 3,67 | 2,44 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 2 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/17 | 157,87 | 0,00 | 3,67 | 2,44 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |


INTERVALO TQS INTEIRO (LIMITE): maior|Vk| de todas as 13 secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.

Passagem geométrica do vibrador 4 cm: atende entre estribos nas faixas calculadas. Esse controle não comprova ausência de congestionamento nos encontros. Espaçamento transversal entre ramos e respectivos limites estão preservados no resultado bruto; quatro ramos com peças sobrepostas dependem da disposição do corte.

Trecho 1B: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

Trecho 2: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

**Suspensão: ** V7→V31: AREA ATENDE; FECHAMENTO DOS ESTRIBOS A VERIFICAR; V9→V31: AREA ATENDE; FECHAMENTO DOS ESTRIBOS A VERIFICAR; V31→V12: AREA ATENDE; FECHAMENTO DOS ESTRIBOS A VERIFICAR

Origem: detalhe 7402; recorte 7402_V31.png; esforços e resultados por modelo/trecho no JSON desta emissão. Cada linha conserva arquivo, número de linha e envoltória TQS.

### V32

Geometria nominal do detalhe: 40×50 cm. Forma/detalhamento: presença nominal confirmada. Comparação nominal de seções conforme inventário. Situacao longitudinal: SECOES NOMINAIS CONFERIDAS; COTAS DE VAOS A CONCLUIR.

**Flexão positiva - solicitações Mk e resistência equivalente MRd/γf em tf·m.**

| Modelo/trecho | Apoios | b×h(cm) | Armadura | d(cm) | Mk | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V32/1 | PC35C-PC29C | 40×50 | 4Ø20 | 44,87 | 15,63 | 16,58 | ATENDE | ATENDE |
| V32/2 | PC29C-V15 | 40×50 | 4Ø16 | 45,07 | 3,32 | 10,96 | ATENDE | ATENDE |


**Flexao negativa - maximo de cada lado do apoio; valores absolutos em tf·m.**

E=inicio do trecho; D=fim do trecho. Em apoio intermediario, fim do trecho anterior e inicio do seguinte sao verificacoes distintas.

| Trecho/lado | Apoio | h(cm) | Armadura superior | d(cm) | Mk negativo | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1/E | PC35C | 50 | 4Ø16 | 45,07 | 14,410 | 10,955 | ATENDE | NÃO ATENDE |
| 1/D | PC29C | 50 | 4Ø20 | 44,87 | 12,100 | 16,577 | ATENDE | ATENDE |
| 2/E | PC29C | 50 | 4Ø20 | 44,87 | 13,095 | 16,577 | ATENDE | ATENDE |
| 2/D | V15 | 50 | 4Ø10 | 45,37 | 0,251 | 4,434 | ATENDE | ATENDE |


Mínimos: comparação de MRd do Concretopy com Md, mín=0,8W0 fctk, sup e taxa absoluta 0,15%, conforme 17.3.5.2.1. O arquivo bruto também conserva a avaliação tabelada do motor; ela não substitui a verificação com d efetivo. A falta de momento positivo não demonstra necessidade de armadura positiva mínima na face não tracionada.

**Cortante - Vk característico em tf; taxas em cm²/m.**

| Trecho | Intervalo modelo(m) | Estribo | d(cm) | Vk | Fornecida | Exigida | Área | s máximo L/T | Biela |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | INTERVALO TQS INTEIRO (LIMITE) | 4 r Ø6,3 c/15 | 44,87 | 17,02 | 8,31 | 5,14 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 2 | INTERVALO TQS INTEIRO (LIMITE) | 4 r Ø6,3 c/15 | 44,87 | 12,97 | 8,31 | 5,14 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |


INTERVALO TQS INTEIRO (LIMITE): maior|Vk| de todas as 13 secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.

Passagem geométrica do vibrador 4 cm: atende entre estribos nas faixas calculadas. Esse controle não comprova ausência de congestionamento nos encontros. Espaçamento transversal entre ramos e respectivos limites estão preservados no resultado bruto; quatro ramos com peças sobrepostas dependem da disposição do corte.

Trecho 1: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

Trecho 2: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

**Suspensão: ** V32→V15: TIRANTE INTEGRAL A COMPROVAR

Origem: detalhe 7402; recorte 7402_V32.png; esforços e resultados por modelo/trecho no JSON desta emissão. Cada linha conserva arquivo, número de linha e envoltória TQS.

### V33

Geometria nominal do detalhe: 30×50 cm. Forma/detalhamento: presença nominal confirmada. Comparação nominal de seções conforme inventário. Situacao longitudinal: FACES E FAIXAS CONCILIADAS; VER NOTAS DE COMPRIMENTO.

Faixa 129 cm termina no bloco P794. Retirado o antigo déficit até a face do pilar. Cortante atende; negativa P794 e suspensão na V19 são controles distintos.

**Flexão positiva - solicitações Mk e resistência equivalente MRd/γf em tf·m.**

| Modelo/trecho | Apoios | b×h(cm) | Armadura | d(cm) | Mk | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V33/1 | P794-V19 | 30×50 | 3Ø12,5 | 45,08 | 2,35 | 5,11 | ATENDE | ATENDE |


**Flexao negativa - maximo de cada lado do apoio; valores absolutos em tf·m.**

E=inicio do trecho; D=fim do trecho. Em apoio intermediario, fim do trecho anterior e inicio do seguinte sao verificacoes distintas.

| Trecho/lado | Apoio | h(cm) | Armadura superior | d(cm) | Mk negativo | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1/E | P794 | 50 | 2Ø20 | 44,70 | 16,069 | 8,468 | ATENDE | NÃO ATENDE |
| 1/D | V19 | 50 | 2Ø20 | 44,70 | 0,000 | 8,468 | SEM MkNEGATIVO | ATENDE |


Mínimos: comparação de MRd do Concretopy com Md, mín=0,8W0 fctk, sup e taxa absoluta 0,15%, conforme 17.3.5.2.1. O arquivo bruto também conserva a avaliação tabelada do motor; ela não substitui a verificação com d efetivo. A falta de momento positivo não demonstra necessidade de armadura positiva mínima na face não tracionada.

**Cortante - Vk característico em tf; taxas em cm²/m.**

| Trecho | Intervalo modelo(m) | Estribo | d(cm) | Vk | Fornecida | Exigida | Área | s máximo L/T | Biela |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1,05-2,33 | 2 r Ø8,0 c/15 | 44,70 | 9,43 | 6,70 | 3,85 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |


INTERVALO TQS INTEIRO (LIMITE): maior|Vk| de todas as 13 secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.

Passagem geométrica do vibrador 4 cm: atende entre estribos nas faixas calculadas. Esse controle não comprova ausência de congestionamento nos encontros. Espaçamento transversal entre ramos e respectivos limites estão preservados no resultado bruto; quatro ramos com peças sobrepostas dependem da disposição do corte.

**Suspensão: ** V33→V19: INSUFICIENTE

Origem: detalhe 7403; recorte 7403_V33.png; esforços e resultados por modelo/trecho no JSON desta emissão. Cada linha conserva arquivo, número de linha e envoltória TQS.

### V34

Geometria nominal do detalhe: 40×50 cm. Forma/detalhamento: presença nominal confirmada. Comparação nominal de seções conforme inventário. Situacao longitudinal: FACES E FAIXAS CONCILIADAS; VER NOTAS DE COMPRIMENTO.

Faixas N7: quatro ramos 6,3 c 10 em 115 cm e c 20 em 334 cm; N1: quatro ramos 8 c 10 em 167 cm. Cruzamento V50 a 4,89 m desde P760.75% atende por taxa, mas depende de comprovar tres estribos na regiao 50 cm e a parcela complementar na V50.

**Flexão positiva - solicitações Mk e resistência equivalente MRd/γf em tf·m.**

| Modelo/trecho | Apoios | b×h(cm) | Armadura | d(cm) | Mk | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V34/1 | P760-P747 | 40×50 | 5Ø20 | 44,87 | 14,93 | 20,32 | ATENDE | ATENDE |


**Flexao negativa - maximo de cada lado do apoio; valores absolutos em tf·m.**

E=inicio do trecho; D=fim do trecho. Em apoio intermediario, fim do trecho anterior e inicio do seguinte sao verificacoes distintas.

| Trecho/lado | Apoio | h(cm) | Armadura superior | d(cm) | Mk negativo | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1/E | P760 | 50 | 4Ø20 | 44,87 | 29,375 | 16,577 | ATENDE | NÃO ATENDE |
| 1/D | P747 | 50 | 6Ø20 | 44,87 | 26,171 | 23,907 | ATENDE | NÃO ATENDE |


Mínimos: comparação de MRd do Concretopy com Md, mín=0,8W0 fctk, sup e taxa absoluta 0,15%, conforme 17.3.5.2.1. O arquivo bruto também conserva a avaliação tabelada do motor; ela não substitui a verificação com d efetivo. A falta de momento positivo não demonstra necessidade de armadura positiva mínima na face não tracionada.

**Cortante - Vk característico em tf; taxas em cm²/m.**

| Trecho | Intervalo modelo(m) | Estribo | d(cm) | Vk | Fornecida | Exigida | Área | s máximo L/T | Biela |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1,00-2,15 | 4 r Ø6,3 c/10 | 44,87 | 16,10 | 12,47 | 5,14 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 1 | 2,15-5,49 | 4 r Ø6,3 c/20 | 44,87 | 9,25 | 6,23 | 5,14 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 1 | 5,49-7,17 | 4 r Ø8,0 c/10 | 44,70 | 15,05 | 20,11 | 5,14 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |


INTERVALO TQS INTEIRO (LIMITE): maior|Vk| de todas as 13 secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.

Passagem geométrica do vibrador 4 cm: atende entre estribos nas faixas calculadas. Esse controle não comprova ausência de congestionamento nos encontros. Espaçamento transversal entre ramos e respectivos limites estão preservados no resultado bruto; quatro ramos com peças sobrepostas dependem da disposição do corte.

**Suspensão: ** V50→V34: TIRANTE INTEGRAL A COMPROVAR

Origem: detalhe 7403; recorte 7403_V34.png; esforços e resultados por modelo/trecho no JSON desta emissão. Cada linha conserva arquivo, número de linha e envoltória TQS.

### V35

Geometria nominal do detalhe: 30×50 cm. Forma/detalhamento: presença nominal confirmada. Comparação nominal de seções conforme inventário. Situacao longitudinal: FACES E FAIXAS CONCILIADAS; VER NOTAS DE COMPRIMENTO.

Duas faixas N11 de 2 ramos 6,3 c 15. Cortante insuficiente nos dois intervalos. Sentido da ligacao com V15 depende do caso gravidade/vento; pendente para Joao. Nao concluir levantamento pela envoltoria total.

**Flexão positiva - solicitações Mk e resistência equivalente MRd/γf em tf·m.**

| Modelo/trecho | Apoios | b×h(cm) | Armadura | d(cm) | Mk | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V35/1 | PC36C-PC30C | 30×50 | 2Ø20 | 44,87 | 9,97 | 8,50 | ATENDE | NÃO ATENDE |
| V35/2 | PC30C-V15 | 30×50 | 2Ø16 | 45,07 | 0,41 | 5,56 | ATENDE | ATENDE |


**Flexao negativa - maximo de cada lado do apoio; valores absolutos em tf·m.**

E=inicio do trecho; D=fim do trecho. Em apoio intermediario, fim do trecho anterior e inicio do seguinte sao verificacoes distintas.

| Trecho/lado | Apoio | h(cm) | Armadura superior | d(cm) | Mk negativo | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1/E | PC36C | 50 | 3Ø16 | 45,07 | 10,145 | 8,216 | ATENDE | NÃO ATENDE |
| 1/D | PC30C | 50 | 4Ø16 | 45,07 | 21,953 | 10,780 | ATENDE | NÃO ATENDE |
| 2/E | PC30C | 50 | 4Ø16 | 45,07 | 22,808 | 10,780 | ATENDE | NÃO ATENDE |
| 2/D | V15 | 50 | 3Ø10 | 45,37 | 0,017 | 3,325 | ATENDE | ATENDE |


Mínimos: comparação de MRd do Concretopy com Md, mín=0,8W0 fctk, sup e taxa absoluta 0,15%, conforme 17.3.5.2.1. O arquivo bruto também conserva a avaliação tabelada do motor; ela não substitui a verificação com d efetivo. A falta de momento positivo não demonstra necessidade de armadura positiva mínima na face não tracionada.

**Cortante - Vk característico em tf; taxas em cm²/m.**

| Trecho | Intervalo modelo(m) | Estribo | d(cm) | Vk | Fornecida | Exigida | Área | s máximo L/T | Biela |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0,15-6,46 | 2 r Ø6,3 c/15 | 45,07 | 20,56 | 4,16 | 8,62 | NÃO ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 2 | 0,15-3,33 | 2 r Ø6,3 c/15 | 45,07 | 18,77 | 4,16 | 7,23 | NÃO ATENDE | L: ATENDE / T: ATENDE | ATENDE |


INTERVALO TQS INTEIRO (LIMITE): maior|Vk| de todas as 13 secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.

Passagem geométrica do vibrador 4 cm: atende entre estribos nas faixas calculadas. Esse controle não comprova ausência de congestionamento nos encontros. Espaçamento transversal entre ramos e respectivos limites estão preservados no resultado bruto; quatro ramos com peças sobrepostas dependem da disposição do corte.

**Suspensão: ** V35→V15: SENTIDO DA TRANSFERENCIA: ANALISE DE JOAO

Origem: detalhe 7403; recorte 7403_V35.png; esforços e resultados por modelo/trecho no JSON desta emissão. Cada linha conserva arquivo, número de linha e envoltória TQS.

### V36

Geometria nominal do detalhe: 30×50 cm. Forma/detalhamento: presença nominal confirmada. Comparação nominal de seções conforme inventário. Situacao longitudinal: FACES E FAIXAS CONCILIADAS; VER NOTAS DE COMPRIMENTO.

Em C35,2 ramos 6,3 c 15 atendem ao cortante. Sentido da ligacao com V5 depende do caso gravidade/vento; pendente para Joao. Nao concluir levantamento apenas pelo sinal negativo da listagem.

**Flexão positiva - solicitações Mk e resistência equivalente MRd/γf em tf·m.**

| Modelo/trecho | Apoios | b×h(cm) | Armadura | d(cm) | Mk | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V36/1 | V5-P735 | 30×50 | 4Ø16 | 45,07 | 9,19 | 10,78 | ATENDE | ATENDE |


**Flexao negativa - maximo de cada lado do apoio; valores absolutos em tf·m.**

E=inicio do trecho; D=fim do trecho. Em apoio intermediario, fim do trecho anterior e inicio do seguinte sao verificacoes distintas.

| Trecho/lado | Apoio | h(cm) | Armadura superior | d(cm) | Mk negativo | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1/E | V5 | 50 | 2Ø10 | 45,37 | 0,559 | 2,230 | NÃO ATENDE | ATENDE |
| 1/D | P735 | 50 | 4Ø16 | 45,07 | 22,915 | 10,780 | ATENDE | NÃO ATENDE |


Mínimo não atendido no apoio V5: As=1,57 cm²; mínimo absoluto=2,25 cm²; momento mínimo equivalente=3,04 tf·m; resistência equivalente=2,23 tf·m.

Mínimos: comparação de MRd do Concretopy com Md, mín=0,8W0 fctk, sup e taxa absoluta 0,15%, conforme 17.3.5.2.1. O arquivo bruto também conserva a avaliação tabelada do motor; ela não substitui a verificação com d efetivo. A falta de momento positivo não demonstra necessidade de armadura positiva mínima na face não tracionada.

**Cortante - Vk característico em tf; taxas em cm²/m.**

| Trecho | Intervalo modelo(m) | Estribo | d(cm) | Vk | Fornecida | Exigida | Área | s máximo L/T | Biela |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0,10-6,29 | 2 r Ø6,3 c/15 | 45,07 | 14,35 | 4,16 | 3,85 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |


INTERVALO TQS INTEIRO (LIMITE): maior|Vk| de todas as 13 secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.

Passagem geométrica do vibrador 4 cm: atende entre estribos nas faixas calculadas. Esse controle não comprova ausência de congestionamento nos encontros. Espaçamento transversal entre ramos e respectivos limites estão preservados no resultado bruto; quatro ramos com peças sobrepostas dependem da disposição do corte.

**Suspensão: ** V36→V5: SENTIDO DA TRANSFERENCIA: ANALISE DE JOAO

Origem: detalhe 7403; recorte 7403_V36.png; esforços e resultados por modelo/trecho no JSON desta emissão. Cada linha conserva arquivo, número de linha e envoltória TQS.

### V37

Geometria nominal do detalhe: 30×50 cm. Forma/detalhamento: presença nominal confirmada. Comparação nominal de seções conforme inventário. Situacao longitudinal: FACES E FAIXAS CONCILIADAS; VER NOTAS DE COMPRIMENTO.

N7: 2 ramosØ6,3 c/15 em 418 cm; N1: 2 ramosØ8 c/15 em 135 cm. Cortante atende com d/2 no P725, confirmado por João. Positiva e negativas mantêm verificações próprias.

**Flexão positiva - solicitações Mk e resistência equivalente MRd/γf em tf·m.**

| Modelo/trecho | Apoios | b×h(cm) | Armadura | d(cm) | Mk | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V37/1 | P725-P712 | 30×50 | 2Ø20 | 44,87 | 9,95 | 8,50 | ATENDE | NÃO ATENDE |


**Flexao negativa - maximo de cada lado do apoio; valores absolutos em tf·m.**

E=inicio do trecho; D=fim do trecho. Em apoio intermediario, fim do trecho anterior e inicio do seguinte sao verificacoes distintas.

| Trecho/lado | Apoio | h(cm) | Armadura superior | d(cm) | Mk negativo | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1/E | P725 | 50 | 4Ø16 | 45,07 | 18,716 | 10,780 | ATENDE | NÃO ATENDE |
| 1/D | P712 | 50 | 4Ø20 | 44,87 | 17,045 | 16,151 | ATENDE | NÃO ATENDE |


Mínimos: comparação de MRd do Concretopy com Md, mín=0,8W0 fctk, sup e taxa absoluta 0,15%, conforme 17.3.5.2.1. O arquivo bruto também conserva a avaliação tabelada do motor; ela não substitui a verificação com d efetivo. A falta de momento positivo não demonstra necessidade de armadura positiva mínima na face não tracionada.

**Cortante - Vk característico em tf; taxas em cm²/m.**

| Trecho | Intervalo modelo(m) | Estribo | d(cm) | Vk | Fornecida | Exigida | Área | s máximo L/T | Biela |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0,87-5,05 | 2 r Ø6,3 c/15 | 44,87 | 12,33 | 4,16 | 3,85 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 1 | 5,05-6,40 | 2 r Ø8,0 c/15 | 44,70 | 9,37 | 6,70 | 3,85 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |


INTERVALO TQS INTEIRO (LIMITE): maior|Vk| de todas as 13 secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.

Passagem geométrica do vibrador 4 cm: atende entre estribos nas faixas calculadas. Esse controle não comprova ausência de congestionamento nos encontros. Espaçamento transversal entre ramos e respectivos limites estão preservados no resultado bruto; quatro ramos com peças sobrepostas dependem da disposição do corte.

Trecho 1: d/2 no P725; condições confirmadas por João. O cortante sem redução e a consulta adotada são preservados separadamente no JSON.

**Suspensão: ** sem ligação indireta física identificada no inventário deste modelo.

Origem: detalhe 7403; recorte 7403_V37.png; esforços e resultados por modelo/trecho no JSON desta emissão. Cada linha conserva arquivo, número de linha e envoltória TQS.

### V38

Geometria nominal do detalhe: 24×50 cm. Forma/detalhamento: presença nominal confirmada. Comparação nominal de seções conforme inventário. Situacao longitudinal: SECOES NOMINAIS CONFERIDAS; COTAS DE VAOS A CONCLUIR.

**Flexão positiva - solicitações Mk e resistência equivalente MRd/γf em tf·m.**

| Modelo/trecho | Apoios | b×h(cm) | Armadura | d(cm) | Mk | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V38/1 | P752-P742 | 24×50 | 2Ø20 | 44,70 | 4,69 | 8,36 | ATENDE | ATENDE |


**Flexao negativa - maximo de cada lado do apoio; valores absolutos em tf·m.**

E=inicio do trecho; D=fim do trecho. Em apoio intermediario, fim do trecho anterior e inicio do seguinte sao verificacoes distintas.

| Trecho/lado | Apoio | h(cm) | Armadura superior | d(cm) | Mk negativo | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1/E | P752 | 50 | 4Ø16 | 44,90 | 10,388 | 10,562 | ATENDE | ATENDE |
| 1/D | P742 | 50 | 3Ø10 | 45,20 | 2,436 | 3,298 | ATENDE | ATENDE |


Mínimos: comparação de MRd do Concretopy com Md, mín=0,8W0 fctk, sup e taxa absoluta 0,15%, conforme 17.3.5.2.1. O arquivo bruto também conserva a avaliação tabelada do motor; ela não substitui a verificação com d efetivo. A falta de momento positivo não demonstra necessidade de armadura positiva mínima na face não tracionada.

**Cortante - Vk característico em tf; taxas em cm²/m.**

| Trecho | Intervalo modelo(m) | Estribo | d(cm) | Vk | Fornecida | Exigida | Área | s máximo L/T | Biela |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø8,0 c/12 | 44,90 | 17,76 | 8,38 | 7,97 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |


INTERVALO TQS INTEIRO (LIMITE): maior|Vk| de todas as 13 secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.

Passagem geométrica do vibrador 4 cm: atende entre estribos nas faixas calculadas. Esse controle não comprova ausência de congestionamento nos encontros. Espaçamento transversal entre ramos e respectivos limites estão preservados no resultado bruto; quatro ramos com peças sobrepostas dependem da disposição do corte.

Trecho 1: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

**Suspensão: ** sem ligação indireta física identificada no inventário deste modelo.

Origem: detalhe 7403; recorte 7403_V38.png; esforços e resultados por modelo/trecho no JSON desta emissão. Cada linha conserva arquivo, número de linha e envoltória TQS.

### V39

Geometria nominal do detalhe: 19×165 cm. Forma/detalhamento: presença nominal confirmada. Comparação nominal de seções conforme inventário. Situacao longitudinal: SECOES NOMINAIS CONFERIDAS; COTAS DE VAOS A CONCLUIR.

Mesmo desenho da V29. Positiva 3Ø20 em camadas[2,1]. Somente 2Ø10 finais no topo. Conferir funcionamento dos estribos 138/50 cm.

**Flexão positiva - solicitações Mk e resistência equivalente MRd/γf em tf·m.**

| Modelo/trecho | Apoios | b×h(cm) | Armadura | d(cm) | Mk | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V39/1 | P754-P743 | 19×165 | 3Ø20 / camadas [2, 1] | 158,54 | 42,33 | 45,80 | ATENDE | ATENDE |


**Flexao negativa - maximo de cada lado do apoio; valores absolutos em tf·m.**

E=inicio do trecho; D=fim do trecho. Em apoio intermediario, fim do trecho anterior e inicio do seguinte sao verificacoes distintas.

| Trecho/lado | Apoio | h(cm) | Armadura superior | d(cm) | Mk negativo | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1/E | P754 | 165 | 2Ø10 | 160,37 | 1,239 | 7,935 | NÃO ATENDE | ATENDE |
| 1/D | P743 | 165 | 2Ø10 | 160,37 | 1,265 | 7,935 | NÃO ATENDE | ATENDE |


Mínimo não atendido no apoio P754: As=1,57 cm²; mínimo absoluto=4,70 cm²; momento mínimo equivalente=20,96 tf·m; resistência equivalente=7,94 tf·m.

Mínimo não atendido no apoio P743: As=1,57 cm²; mínimo absoluto=4,70 cm²; momento mínimo equivalente=20,96 tf·m; resistência equivalente=7,94 tf·m.

Mínimos: comparação de MRd do Concretopy com Md, mín=0,8W0 fctk, sup e taxa absoluta 0,15%, conforme 17.3.5.2.1. O arquivo bruto também conserva a avaliação tabelada do motor; ela não substitui a verificação com d efetivo. A falta de momento positivo não demonstra necessidade de armadura positiva mínima na face não tracionada.

**Cortante - Vk característico em tf; taxas em cm²/m.**

| Trecho | Intervalo modelo(m) | Estribo | d(cm) | Vk | Fornecida | Exigida | Área | s máximo L/T | Biela |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/17 | 158,54 | 23,53 | 3,67 | 2,44 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |


INTERVALO TQS INTEIRO (LIMITE): maior|Vk| de todas as 13 secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.

Passagem geométrica do vibrador 4 cm: atende entre estribos nas faixas calculadas. Esse controle não comprova ausência de congestionamento nos encontros. Espaçamento transversal entre ramos e respectivos limites estão preservados no resultado bruto; quatro ramos com peças sobrepostas dependem da disposição do corte.

Trecho 1: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

**Suspensão: ** V8→V39: AREA ATENDE; FECHAMENTO DOS ESTRIBOS A VERIFICAR; V10→V39: AREA ATENDE; FECHAMENTO DOS ESTRIBOS A VERIFICAR

Origem: detalhe 7402; recorte 7402_V29-39.png; esforços e resultados por modelo/trecho no JSON desta emissão. Cada linha conserva arquivo, número de linha e envoltória TQS.

### V40

Geometria nominal do detalhe: 30×50 cm. Forma/detalhamento: presença nominal confirmada. Comparação nominal de seções conforme inventário. Situacao longitudinal: FACES E FAIXAS CONCILIADAS; VER NOTAS DE COMPRIMENTO.

Faixa 129 cm termina no bloco P796. Correção anotada para apoio V20 já aceita; desenho-base cita V19. Cortante atende; negativa P796 e suspensão na V20 mantêm apontamentos próprios.

**Flexão positiva - solicitações Mk e resistência equivalente MRd/γf em tf·m.**

| Modelo/trecho | Apoios | b×h(cm) | Armadura | d(cm) | Mk | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V40/1 | P796-V20 | 30×50 | 3Ø12,5 | 45,08 | 2,20 | 5,11 | ATENDE | ATENDE |


**Flexao negativa - maximo de cada lado do apoio; valores absolutos em tf·m.**

E=inicio do trecho; D=fim do trecho. Em apoio intermediario, fim do trecho anterior e inicio do seguinte sao verificacoes distintas.

| Trecho/lado | Apoio | h(cm) | Armadura superior | d(cm) | Mk negativo | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1/E | P796 | 50 | 2Ø20 | 44,70 | 17,697 | 8,468 | ATENDE | NÃO ATENDE |
| 1/D | V20 | 50 | 2Ø20 | 44,70 | 0,000 | 8,468 | SEM MkNEGATIVO | ATENDE |


Mínimos: comparação de MRd do Concretopy com Md, mín=0,8W0 fctk, sup e taxa absoluta 0,15%, conforme 17.3.5.2.1. O arquivo bruto também conserva a avaliação tabelada do motor; ela não substitui a verificação com d efetivo. A falta de momento positivo não demonstra necessidade de armadura positiva mínima na face não tracionada.

**Cortante - Vk característico em tf; taxas em cm²/m.**

| Trecho | Intervalo modelo(m) | Estribo | d(cm) | Vk | Fornecida | Exigida | Área | s máximo L/T | Biela |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1,05-2,34 | 2 r Ø8,0 c/15 | 44,70 | 8,86 | 6,70 | 3,85 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |


INTERVALO TQS INTEIRO (LIMITE): maior|Vk| de todas as 13 secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.

Passagem geométrica do vibrador 4 cm: atende entre estribos nas faixas calculadas. Esse controle não comprova ausência de congestionamento nos encontros. Espaçamento transversal entre ramos e respectivos limites estão preservados no resultado bruto; quatro ramos com peças sobrepostas dependem da disposição do corte.

**Suspensão: ** V40→V20: INSUFICIENTE

Origem: detalhe 7403; recorte 7403_V40.png; esforços e resultados por modelo/trecho no JSON desta emissão. Cada linha conserva arquivo, número de linha e envoltória TQS.

### V41

Geometria nominal do detalhe: 19×165 cm. Forma/detalhamento: presença nominal confirmada. Comparação nominal de seções conforme inventário. Situacao longitudinal: EIXOS DOS CRUZAMENTOS E FAIXAS CONCILIADOS.

Inicio 1B no eixo V13, confirmado por Joao. V41 descarrega em V13. Cruzamentos V10/V8 a 2,325/3,545 m; face P744 a 5,590 m e faixa 547 cm conciliadas. Soma conservadora dos dois tirantes e cortante regional atende 3,667 cm 2/m existentes; suspensao em V13 tratada separadamente.

**Flexão positiva - solicitações Mk e resistência equivalente MRd/γf em tf·m.**

| Modelo/trecho | Apoios | b×h(cm) | Armadura | d(cm) | Mk | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V41/1B | EXTREMIDADE_LIVRE-P744 | 19×165 | 4Ø20 / camadas [2, 2] | 157,87 | 44,62 | 60,13 | ATENDE | ATENDE |
| V41/2 | P744-P744 | 19×165 | 4Ø20 / camadas [2, 2] | 157,87 | 1,07 | 60,13 | ATENDE | ATENDE |


**Flexao negativa - maximo de cada lado do apoio; valores absolutos em tf·m.**

E=inicio do trecho; D=fim do trecho. Em apoio intermediario, fim do trecho anterior e inicio do seguinte sao verificacoes distintas.

| Trecho/lado | Apoio | h(cm) | Armadura superior | d(cm) | Mk negativo | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1B/E | EXTREMIDADE_LIVRE | 165 | 2Ø10 | 160,37 | 0,130 | 7,935 | NÃO ATENDE | ATENDE |
| 1B/D | P744 | 165 | 2Ø10 | 160,37 | 4,061 | 7,935 | NÃO ATENDE | ATENDE |
| 2/E | P744 | 165 | 2Ø10 | 160,37 | 0,184 | 7,935 | NÃO ATENDE | ATENDE |
| 2/D | P744 | 165 | 2Ø10 | 160,37 | 0,000 | 7,935 | SEM MkNEGATIVO | ATENDE |


Mínimo não atendido no apoio EXTREMIDADE_LIVRE: As=1,57 cm²; mínimo absoluto=4,70 cm²; momento mínimo equivalente=20,96 tf·m; resistência equivalente=7,94 tf·m.

Mínimo não atendido no apoio P744: As=1,57 cm²; mínimo absoluto=4,70 cm²; momento mínimo equivalente=20,96 tf·m; resistência equivalente=7,94 tf·m.

Mínimo não atendido no apoio P744: As=1,57 cm²; mínimo absoluto=4,70 cm²; momento mínimo equivalente=20,96 tf·m; resistência equivalente=7,94 tf·m.

Mínimos: comparação de MRd do Concretopy com Md, mín=0,8W0 fctk, sup e taxa absoluta 0,15%, conforme 17.3.5.2.1. O arquivo bruto também conserva a avaliação tabelada do motor; ela não substitui a verificação com d efetivo. A falta de momento positivo não demonstra necessidade de armadura positiva mínima na face não tracionada.

**Cortante - Vk característico em tf; taxas em cm²/m.**

| Trecho | Intervalo modelo(m) | Estribo | d(cm) | Vk | Fornecida | Exigida | Área | s máximo L/T | Biela |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1B | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/17 | 157,87 | 30,52 | 3,67 | 2,44 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 2 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/17 | 157,87 | 0,00 | 3,67 | 2,44 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |


INTERVALO TQS INTEIRO (LIMITE): maior|Vk| de todas as 13 secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.

Passagem geométrica do vibrador 4 cm: atende entre estribos nas faixas calculadas. Esse controle não comprova ausência de congestionamento nos encontros. Espaçamento transversal entre ramos e respectivos limites estão preservados no resultado bruto; quatro ramos com peças sobrepostas dependem da disposição do corte.

Trecho 1B: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

Trecho 2: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

**Suspensão: ** V8→V41: AREA ATENDE; FECHAMENTO DOS ESTRIBOS A VERIFICAR; V10→V41: AREA ATENDE; FECHAMENTO DOS ESTRIBOS A VERIFICAR; V41→V13: DISTRIBUICAO UNIFORME NAO ATENDE

Origem: detalhe 7403; recorte 7403_V41.png; esforços e resultados por modelo/trecho no JSON desta emissão. Cada linha conserva arquivo, número de linha e envoltória TQS.

### V42

Geometria nominal do detalhe: 30×80 cm; 30×50 cm; 30×110 cm. Forma/detalhamento: presença nominal confirmada. Divergência local de altura conforme nota abaixo. Situacao longitudinal: DIVERGENCIA DE ALTURA; TRANSICOES A CONCLUIR.

Há indicaçãoh 110 no trecho do detalhamento contra rótulosh 80/h 50 na forma. Usadas seções do detalhamento conforme autorização; divergência forma-detalhe mantida. P791 está a+8,88 m. Falta localizar todas as transições de altura no eixo físico.

**Flexão positiva - solicitações Mk e resistência equivalente MRd/γf em tf·m.**

| Modelo/trecho | Apoios | b×h(cm) | Armadura | d(cm) | Mk | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V42/1 | PC58C-P807C | 30×80 | 2Ø16 | 75,07 | 6,14 | 9,39 | ATENDE | ATENDE |
| V42/2 | P807C-P797 | 30×50 | 3Ø10 | 45,37 | 0,21 | 3,33 | ATENDE | ATENDE |
| V42/3 | P797-P791 | 30×80 | 2Ø16 | 75,07 | 4,98 | 9,39 | ATENDE | ATENDE |
| V42/4 | P791-P784 | 30×110 | 3Ø20 | 104,87 | 13,12 | 30,34 | ATENDE | ATENDE |
| V42/5 | P784-P764 | 30×50 | 2Ø20 | 44,87 | 4,17 | 8,50 | ATENDE | ATENDE |
| V42/6 | P764-P762 | 30×50 | 2Ø20 | 44,87 | 5,64 | 8,50 | ATENDE | ATENDE |
| V42/7 | P762-PC26C | 30×50 | 2Ø16 | 45,07 | 0,41 | 5,56 | ATENDE | ATENDE |


**Flexao negativa - maximo de cada lado do apoio; valores absolutos em tf·m.**

E=inicio do trecho; D=fim do trecho. Em apoio intermediario, fim do trecho anterior e inicio do seguinte sao verificacoes distintas.

| Trecho/lado | Apoio | h(cm) | Armadura superior | d(cm) | Mk negativo | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1/E | PC58C | 80 | 2Ø10 | 75,37 | 0,000 | 3,723 | SEM MkNEGATIVO | ATENDE |
| 1/D | P807C | 80 | 2Ø16 | 75,07 | 5,088 | 9,385 | ATENDE | ATENDE |
| 2/E | P807C | 50 | 2Ø16 | 45,07 | 2,019 | 5,565 | ATENDE | ATENDE |
| 2/D | P797 | 50 | 2Ø16 | 45,07 | 3,343 | 5,565 | ATENDE | ATENDE |
| 3/E | P797 | 80 | 2Ø16 | 75,07 | 7,362 | 9,385 | ATENDE | ATENDE |
| 3/D | P791 | 80 | 3Ø16 | 75,07 | 9,686 | 13,947 | ATENDE | ATENDE |
| 4/E | P791 | 80 | 3Ø16 | 75,07 | 11,789 | 13,947 | ATENDE | ATENDE |
| 4/D | P784 | 110 | 3Ø16 | 105,07 | 14,964 | 19,677 | ATENDE | ATENDE |
| 5/E | P784 | 50 | 3Ø16 | 45,07 | 9,958 | 8,216 | ATENDE | NÃO ATENDE |
| 5/D | P764 | 50 | 3Ø16 | 45,07 | 7,737 | 8,216 | ATENDE | ATENDE |
| 6/E | P764 | 50 | 3Ø16 | 45,07 | 10,300 | 8,216 | ATENDE | NÃO ATENDE |
| 6/D | P762 | 50 | 3Ø16 | 45,07 | 8,956 | 8,216 | ATENDE | NÃO ATENDE |
| 7/E | P762 | 50 | 3Ø16 | 45,07 | 1,214 | 8,216 | ATENDE | ATENDE |
| 7/D | PC26C | 50 | 2Ø10 | 45,37 | 0,000 | 2,230 | SEM MkNEGATIVO | ATENDE |


Mínimos: comparação de MRd do Concretopy com Md, mín=0,8W0 fctk, sup e taxa absoluta 0,15%, conforme 17.3.5.2.1. O arquivo bruto também conserva a avaliação tabelada do motor; ela não substitui a verificação com d efetivo. A falta de momento positivo não demonstra necessidade de armadura positiva mínima na face não tracionada.

**Cortante - Vk característico em tf; taxas em cm²/m.**

| Trecho | Intervalo modelo(m) | Estribo | d(cm) | Vk | Fornecida | Exigida | Área | s máximo L/T | Biela |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/15 | 75,07 | 6,48 | 4,16 | 3,85 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 2 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/15 | 45,07 | 3,50 | 4,16 | 3,85 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 3 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/15 | 75,07 | 7,50 | 4,16 | 3,85 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 4 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/15 | 104,87 | 11,17 | 4,16 | 3,85 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 5 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/15 | 44,87 | 7,00 | 4,16 | 3,85 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 6 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/15 | 44,87 | 7,93 | 4,16 | 3,85 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 7 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/15 | 45,07 | 1,79 | 4,16 | 3,85 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |


INTERVALO TQS INTEIRO (LIMITE): maior|Vk| de todas as 13 secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.

Passagem geométrica do vibrador 4 cm: atende entre estribos nas faixas calculadas. Esse controle não comprova ausência de congestionamento nos encontros. Espaçamento transversal entre ramos e respectivos limites estão preservados no resultado bruto; quatro ramos com peças sobrepostas dependem da disposição do corte.

Trecho 1: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

Trecho 2: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

Trecho 3: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

Trecho 4: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

Trecho 5: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

Trecho 6: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

Trecho 7: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

**Suspensão: ** V17→V42: SENTIDO DA TRANSFERENCIA: ANALISE DE JOAO

Origem: detalhe 7403; recorte 7403_V42.png; esforços e resultados por modelo/trecho no JSON desta emissão. Cada linha conserva arquivo, número de linha e envoltória TQS.

### V43

Geometria nominal do detalhe: 30×50 cm. Forma/detalhamento: presença nominal confirmada. Comparação nominal de seções conforme inventário. Situacao longitudinal: SECOES NOMINAIS CONFERIDAS; COTAS DE VAOS A CONCLUIR.

**Flexão positiva - solicitações Mk e resistência equivalente MRd/γf em tf·m.**

| Modelo/trecho | Apoios | b×h(cm) | Armadura | d(cm) | Mk | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V43/2 | P748-P737 | 30×50 | 3Ø20 | 44,87 | 8,77 | 12,43 | ATENDE | ATENDE |
| V43/3 | P737-P723 | 30×50 | 2Ø20 | 44,87 | 4,64 | 8,50 | ATENDE | ATENDE |
| V43/4 | P723-P714 | 30×50 | 2Ø20 | 44,87 | 7,52 | 8,50 | ATENDE | ATENDE |
| V43/5 | P714-P707 | 30×50 | 3Ø12,5 | 45,24 | 1,81 | 5,13 | ATENDE | ATENDE |
| V43/1B | EXTREMIDADE_LIVRE-P748 | 30×50 | 3Ø20 | 44,87 | 0,12 | 12,43 | ATENDE | ATENDE |


**Flexao negativa - maximo de cada lado do apoio; valores absolutos em tf·m.**

E=inicio do trecho; D=fim do trecho. Em apoio intermediario, fim do trecho anterior e inicio do seguinte sao verificacoes distintas.

| Trecho/lado | Apoio | h(cm) | Armadura superior | d(cm) | Mk negativo | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2/E | P748 | 50 | 3Ø16 | 45,07 | 8,222 | 8,216 | ATENDE | NÃO ATENDE |
| 2/D | P737 | 50 | 3Ø20 | 44,87 | 15,784 | 12,433 | ATENDE | NÃO ATENDE |
| 3/E | P737 | 50 | 3Ø20 | 44,87 | 8,837 | 12,433 | ATENDE | ATENDE |
| 3/D | P723 | 50 | 3Ø16 | 45,07 | 8,697 | 8,216 | ATENDE | NÃO ATENDE |
| 4/E | P723 | 50 | 3Ø16 | 45,07 | 12,707 | 8,216 | ATENDE | NÃO ATENDE |
| 4/D | P714 | 50 | 3Ø16 | 45,07 | 11,751 | 8,216 | ATENDE | NÃO ATENDE |
| 5/E | P714 | 50 | 3Ø16 | 45,07 | 5,921 | 8,216 | ATENDE | ATENDE |
| 5/D | P707 | 50 | 4Ø10 | 45,37 | 1,340 | 4,407 | ATENDE | ATENDE |
| 1B/E | EXTREMIDADE_LIVRE | 50 | 3Ø16 | 45,07 | 0,014 | 8,216 | ATENDE | ATENDE |
| 1B/D | P748 | 50 | 3Ø16 | 45,07 | 0,141 | 8,216 | ATENDE | ATENDE |


Mínimos: comparação de MRd do Concretopy com Md, mín=0,8W0 fctk, sup e taxa absoluta 0,15%, conforme 17.3.5.2.1. O arquivo bruto também conserva a avaliação tabelada do motor; ela não substitui a verificação com d efetivo. A falta de momento positivo não demonstra necessidade de armadura positiva mínima na face não tracionada.

**Cortante - Vk característico em tf; taxas em cm²/m.**

| Trecho | Intervalo modelo(m) | Estribo | d(cm) | Vk | Fornecida | Exigida | Área | s máximo L/T | Biela |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/15 | 44,87 | 10,10 | 4,16 | 3,85 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 3 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/15 | 44,87 | 6,78 | 4,16 | 3,85 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 4 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/15 | 44,87 | 8,61 | 4,16 | 3,85 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 5 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/15 | 45,07 | 4,34 | 4,16 | 3,85 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 1B | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/15 | 44,87 | 1,27 | 4,16 | 3,85 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |


INTERVALO TQS INTEIRO (LIMITE): maior|Vk| de todas as 13 secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.

Passagem geométrica do vibrador 4 cm: atende entre estribos nas faixas calculadas. Esse controle não comprova ausência de congestionamento nos encontros. Espaçamento transversal entre ramos e respectivos limites estão preservados no resultado bruto; quatro ramos com peças sobrepostas dependem da disposição do corte.

Trecho 2: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

Trecho 3: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

Trecho 4: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

Trecho 5: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

Trecho 1B: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

**Suspensão: ** V14→V43: ATENDE

Origem: detalhe 7403; recorte 7403_V43.png; esforços e resultados por modelo/trecho no JSON desta emissão. Cada linha conserva arquivo, número de linha e envoltória TQS.

### V44

Geometria nominal do detalhe: 40×50 cm. Forma/detalhamento: presença nominal confirmada. Comparação nominal de seções conforme inventário. Situacao longitudinal: SECOES NOMINAIS CONFERIDAS; COTAS DE VAOS A CONCLUIR.

**Flexão positiva - solicitações Mk e resistência equivalente MRd/γf em tf·m.**

| Modelo/trecho | Apoios | b×h(cm) | Armadura | d(cm) | Mk | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V44/1 | P738-P731 | 40×50 | 4Ø20 | 44,70 | 10,84 | 16,51 | ATENDE | ATENDE |


**Flexao negativa - maximo de cada lado do apoio; valores absolutos em tf·m.**

E=inicio do trecho; D=fim do trecho. Em apoio intermediario, fim do trecho anterior e inicio do seguinte sao verificacoes distintas.

| Trecho/lado | Apoio | h(cm) | Armadura superior | d(cm) | Mk negativo | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1/E | P738 | 50 | 4Ø12,5 | 45,08 | 3,580 | 6,812 | ATENDE | ATENDE |
| 1/D | P731 | 50 | 4Ø16 | 44,90 | 30,792 | 10,912 | ATENDE | NÃO ATENDE |


Mínimos: comparação de MRd do Concretopy com Md, mín=0,8W0 fctk, sup e taxa absoluta 0,15%, conforme 17.3.5.2.1. O arquivo bruto também conserva a avaliação tabelada do motor; ela não substitui a verificação com d efetivo. A falta de momento positivo não demonstra necessidade de armadura positiva mínima na face não tracionada.

**Cortante - Vk característico em tf; taxas em cm²/m.**

| Trecho | Intervalo modelo(m) | Estribo | d(cm) | Vk | Fornecida | Exigida | Área | s máximo L/T | Biela |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | INTERVALO TQS INTEIRO (LIMITE) | 4 r Ø8,0 c/17 | 44,70 | 21,45 | 11,83 | 6,99 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |


INTERVALO TQS INTEIRO (LIMITE): maior|Vk| de todas as 13 secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.

Passagem geométrica do vibrador 4 cm: atende entre estribos nas faixas calculadas. Esse controle não comprova ausência de congestionamento nos encontros. Espaçamento transversal entre ramos e respectivos limites estão preservados no resultado bruto; quatro ramos com peças sobrepostas dependem da disposição do corte.

Trecho 1: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

**Suspensão: ** sem ligação indireta física identificada no inventário deste modelo.

Origem: detalhe 7403; recorte 7403_V44.png; esforços e resultados por modelo/trecho no JSON desta emissão. Cada linha conserva arquivo, número de linha e envoltória TQS.

### V45

Geometria nominal do detalhe: 24×50 cm. Forma/detalhamento: presença nominal confirmada. Comparação nominal de seções conforme inventário. Situacao longitudinal: SECOES NOMINAIS CONFERIDAS; COTAS DE VAOS A CONCLUIR.

**Flexão positiva - solicitações Mk e resistência equivalente MRd/γf em tf·m.**

| Modelo/trecho | Apoios | b×h(cm) | Armadura | d(cm) | Mk | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V45/1 | P750-P753 | 24×50 | 2Ø20 | 44,87 | 3,02 | 8,40 | ATENDE | ATENDE |


**Flexao negativa - maximo de cada lado do apoio; valores absolutos em tf·m.**

E=inicio do trecho; D=fim do trecho. Em apoio intermediario, fim do trecho anterior e inicio do seguinte sao verificacoes distintas.

| Trecho/lado | Apoio | h(cm) | Armadura superior | d(cm) | Mk negativo | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1/E | P750 | 50 | 3Ø10 | 45,37 | 1,288 | 3,310 | ATENDE | ATENDE |
| 1/D | P753 | 50 | 2Ø12,5 | 45,24 | 2,634 | 3,435 | ATENDE | ATENDE |


Mínimos: comparação de MRd do Concretopy com Md, mín=0,8W0 fctk, sup e taxa absoluta 0,15%, conforme 17.3.5.2.1. O arquivo bruto também conserva a avaliação tabelada do motor; ela não substitui a verificação com d efetivo. A falta de momento positivo não demonstra necessidade de armadura positiva mínima na face não tracionada.

**Cortante - Vk característico em tf; taxas em cm²/m.**

| Trecho | Intervalo modelo(m) | Estribo | d(cm) | Vk | Fornecida | Exigida | Área | s máximo L/T | Biela |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/20 | 44,87 | 5,70 | 3,12 | 3,08 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |


INTERVALO TQS INTEIRO (LIMITE): maior|Vk| de todas as 13 secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.

Passagem geométrica do vibrador 4 cm: atende entre estribos nas faixas calculadas. Esse controle não comprova ausência de congestionamento nos encontros. Espaçamento transversal entre ramos e respectivos limites estão preservados no resultado bruto; quatro ramos com peças sobrepostas dependem da disposição do corte.

Trecho 1: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

**Suspensão: ** sem ligação indireta física identificada no inventário deste modelo.

Origem: detalhe 7403; recorte 7403_V45.png; esforços e resultados por modelo/trecho no JSON desta emissão. Cada linha conserva arquivo, número de linha e envoltória TQS.

### V46

Geometria nominal do detalhe: 30×50 cm. Forma/detalhamento: presença nominal confirmada. Comparação nominal de seções conforme inventário. Situacao longitudinal: SECOES NOMINAIS CONFERIDAS; COTAS DE VAOS A CONCLUIR.

**Flexão positiva - solicitações Mk e resistência equivalente MRd/γf em tf·m.**

| Modelo/trecho | Apoios | b×h(cm) | Armadura | d(cm) | Mk | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V46/1 | P747-P751 | 30×50 | 3Ø20 | 44,87 | 8,82 | 12,43 | ATENDE | ATENDE |


**Flexao negativa - maximo de cada lado do apoio; valores absolutos em tf·m.**

E=inicio do trecho; D=fim do trecho. Em apoio intermediario, fim do trecho anterior e inicio do seguinte sao verificacoes distintas.

| Trecho/lado | Apoio | h(cm) | Armadura superior | d(cm) | Mk negativo | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1/E | P747 | 50 | 3Ø20 | 44,87 | 9,334 | 12,433 | ATENDE | ATENDE |
| 1/D | P751 | 50 | 4Ø10 | 45,37 | 1,354 | 4,407 | ATENDE | ATENDE |


Mínimos: comparação de MRd do Concretopy com Md, mín=0,8W0 fctk, sup e taxa absoluta 0,15%, conforme 17.3.5.2.1. O arquivo bruto também conserva a avaliação tabelada do motor; ela não substitui a verificação com d efetivo. A falta de momento positivo não demonstra necessidade de armadura positiva mínima na face não tracionada.

**Cortante - Vk característico em tf; taxas em cm²/m.**

| Trecho | Intervalo modelo(m) | Estribo | d(cm) | Vk | Fornecida | Exigida | Área | s máximo L/T | Biela |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/15 | 44,87 | 12,02 | 4,16 | 3,85 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |


INTERVALO TQS INTEIRO (LIMITE): maior|Vk| de todas as 13 secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.

Passagem geométrica do vibrador 4 cm: atende entre estribos nas faixas calculadas. Esse controle não comprova ausência de congestionamento nos encontros. Espaçamento transversal entre ramos e respectivos limites estão preservados no resultado bruto; quatro ramos com peças sobrepostas dependem da disposição do corte.

Trecho 1: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

**Suspensão: ** sem ligação indireta física identificada no inventário deste modelo.

Origem: detalhe 7403; recorte 7403_V46.png; esforços e resultados por modelo/trecho no JSON desta emissão. Cada linha conserva arquivo, número de linha e envoltória TQS.

### V47

Geometria nominal do detalhe: 30×50 cm. Forma/detalhamento: presença nominal confirmada. Comparação nominal de seções conforme inventário. Situacao longitudinal: FACES E FAIXAS CONCILIADAS; VER NOTAS DE COMPRIMENTO.

Usada a interseção do eixo inclinado com os contornos dos blocos P751/P741 da 7201. Cortante atende; o antigo máximo dentro do bloco não governa a faixa livre.

**Flexão positiva - solicitações Mk e resistência equivalente MRd/γf em tf·m.**

| Modelo/trecho | Apoios | b×h(cm) | Armadura | d(cm) | Mk | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V47/1 | P751-P741 | 30×50 | 2Ø20 | 44,70 | 6,52 | 8,47 | ATENDE | ATENDE |


**Flexao negativa - maximo de cada lado do apoio; valores absolutos em tf·m.**

E=inicio do trecho; D=fim do trecho. Em apoio intermediario, fim do trecho anterior e inicio do seguinte sao verificacoes distintas.

| Trecho/lado | Apoio | h(cm) | Armadura superior | d(cm) | Mk negativo | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1/E | P751 | 50 | 3Ø20 | 44,70 | 14,817 | 12,382 | ATENDE | NÃO ATENDE |
| 1/D | P741 | 50 | 3Ø10 | 45,20 | 1,879 | 3,313 | ATENDE | ATENDE |


Mínimos: comparação de MRd do Concretopy com Md, mín=0,8W0 fctk, sup e taxa absoluta 0,15%, conforme 17.3.5.2.1. O arquivo bruto também conserva a avaliação tabelada do motor; ela não substitui a verificação com d efetivo. A falta de momento positivo não demonstra necessidade de armadura positiva mínima na face não tracionada.

**Cortante - Vk característico em tf; taxas em cm²/m.**

| Trecho | Intervalo modelo(m) | Estribo | d(cm) | Vk | Fornecida | Exigida | Área | s máximo L/T | Biela |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0,93-3,19 | 2 r Ø8,0 c/10 | 44,70 | 9,22 | 10,05 | 3,85 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |


INTERVALO TQS INTEIRO (LIMITE): maior|Vk| de todas as 13 secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.

Passagem geométrica do vibrador 4 cm: atende entre estribos nas faixas calculadas. Esse controle não comprova ausência de congestionamento nos encontros. Espaçamento transversal entre ramos e respectivos limites estão preservados no resultado bruto; quatro ramos com peças sobrepostas dependem da disposição do corte.

**Suspensão: ** sem ligação indireta física identificada no inventário deste modelo.

Origem: detalhe 7403; recorte 7403_V47.png; esforços e resultados por modelo/trecho no JSON desta emissão. Cada linha conserva arquivo, número de linha e envoltória TQS.

### V48

Geometria nominal do detalhe: 30×50 cm. Forma/detalhamento: presença nominal confirmada. Comparação nominal de seções conforme inventário. Situacao longitudinal: FACES E FAIXAS CONCILIADAS; VER NOTAS DE COMPRIMENTO.

Domínio pelos blocos P767/P758. Diferença de cerca 6,3 cm entre soma da faixa e distância vetorial exige conferir a referência das pontas; não comprova falta de estribos. Em C35, o cortante calculado atende.

**Flexão positiva - solicitações Mk e resistência equivalente MRd/γf em tf·m.**

| Modelo/trecho | Apoios | b×h(cm) | Armadura | d(cm) | Mk | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V48/1 | P767-P758 | 30×50 | 2Ø20 | 44,87 | 7,83 | 8,50 | ATENDE | ATENDE |


**Flexao negativa - maximo de cada lado do apoio; valores absolutos em tf·m.**

E=inicio do trecho; D=fim do trecho. Em apoio intermediario, fim do trecho anterior e inicio do seguinte sao verificacoes distintas.

| Trecho/lado | Apoio | h(cm) | Armadura superior | d(cm) | Mk negativo | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1/E | P767 | 50 | 4Ø12,5 | 45,24 | 19,553 | 6,773 | ATENDE | NÃO ATENDE |
| 1/D | P758 | 50 | 4Ø16 | 45,07 | 13,384 | 10,780 | ATENDE | NÃO ATENDE |


Mínimos: comparação de MRd do Concretopy com Md, mín=0,8W0 fctk, sup e taxa absoluta 0,15%, conforme 17.3.5.2.1. O arquivo bruto também conserva a avaliação tabelada do motor; ela não substitui a verificação com d efetivo. A falta de momento positivo não demonstra necessidade de armadura positiva mínima na face não tracionada.

**Cortante - Vk característico em tf; taxas em cm²/m.**

| Trecho | Intervalo modelo(m) | Estribo | d(cm) | Vk | Fornecida | Exigida | Área | s máximo L/T | Biela |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0,87-5,77 | 2 r Ø6,3 c/15 | 45,07 | 12,80 | 4,16 | 3,85 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |


INTERVALO TQS INTEIRO (LIMITE): maior|Vk| de todas as 13 secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.

Passagem geométrica do vibrador 4 cm: atende entre estribos nas faixas calculadas. Esse controle não comprova ausência de congestionamento nos encontros. Espaçamento transversal entre ramos e respectivos limites estão preservados no resultado bruto; quatro ramos com peças sobrepostas dependem da disposição do corte.

Trecho 1: diferença entre domínio consultado e soma dos comprimentos de faixa=6,30 cm. Conferir referências das pontas antes de afirmar cobertura integral.

**Suspensão: ** sem ligação indireta física identificada no inventário deste modelo.

Origem: detalhe 7403; recorte 7403_V48.png; esforços e resultados por modelo/trecho no JSON desta emissão. Cada linha conserva arquivo, número de linha e envoltória TQS.

### V49

Geometria nominal do detalhe: 24×50 cm; 24×87 cm. Forma/detalhamento: presença nominal confirmada. Comparação nominal de seções conforme inventário. Situacao longitudinal: VAO E MUDANCA50/87 cm LOCALIZADOS.

Mudanca 50/87 cm localizada pela cota 130 cm: x TQS=1,465 m. Positiva nao atende emh 50 e atende emh 87; ver tabela regional. Apoio direto no bloco PC21C confirmado. Estribos externos 6,3 c 10; pecas da primeira etapa excluidas.

**Flexão positiva - solicitações Mk e resistência equivalente MRd/γf em tf·m.**

| Modelo/trecho | Apoios | b×h(cm) | Armadura | d(cm) | Mk | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V49/1 | PC21C (TQS: V26)-P749 | 24×50 | 3Ø12,5 | 45,24 | 8,33 | 5,09 | ATENDE | NÃO ATENDE |


**Flexao positiva regional - conclusao aplicavel as alturas reais.**

| h(cm) | Intervalo modelo(m) | d(cm) | Mk(tf·m) | MRd/γf(tf·m) | Resultado |
| --- | --- | --- | --- | --- | --- |
| 50 | 0,095-1,465 | 45,24 | 8,33 | 5,09 | NÃO ATENDE |
| 87 | 1,465-2,765 | 82,25 | 8,29 | 9,41 | ATENDE |


Origem: Concretopy; geometria_e_flexao_regional_V49_V50.json. Cota 130 cm medida da mudanca de altura ate a face interna do pilar direito. Fundo continuo; nao e degrau de fundo. A tabela regional prevalece sobre a comparacao nominal unica acima.

**Flexao negativa - maximo de cada lado do apoio; valores absolutos em tf·m.**

E=inicio do trecho; D=fim do trecho. Em apoio intermediario, fim do trecho anterior e inicio do seguinte sao verificacoes distintas.

| Trecho/lado | Apoio | h(cm) | Armadura superior | d(cm) | Mk negativo | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1/E | PC21C (TQS: V26) | 50 | 2Ø10 | 45,37 | 0,026 | 2,224 | NÃO ATENDE | ATENDE |
| 1/D | P749 | 87 | 2Ø12,5 | 82,25 | 1,079 | 6,311 | NÃO ATENDE | ATENDE |


Mínimo não atendido no apoio PC21C (TQS: V26): As=1,57 cm²; mínimo absoluto=1,80 cm²; momento mínimo equivalente=2,43 tf·m; resistência equivalente=2,22 tf·m.

Mínimo não atendido no apoio P749: As=2,45 cm²; mínimo absoluto=3,13 cm²; momento mínimo equivalente=7,36 tf·m; resistência equivalente=6,31 tf·m.

Mínimos: comparação de MRd do Concretopy com Md, mín=0,8W0 fctk, sup e taxa absoluta 0,15%, conforme 17.3.5.2.1. O arquivo bruto também conserva a avaliação tabelada do motor; ela não substitui a verificação com d efetivo. A falta de momento positivo não demonstra necessidade de armadura positiva mínima na face não tracionada.

**Cortante - Vk característico em tf; taxas em cm²/m.**

| Trecho | Intervalo modelo(m) | Estribo | d(cm) | Vk | Fornecida | Exigida | Área | s máximo L/T | Biela |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/10 | 45,24 | 11,78 | 6,23 | 3,23 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 1 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/10 | 82,25 | 11,78 | 6,23 | 3,08 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |


INTERVALO TQS INTEIRO (LIMITE): maior|Vk| de todas as 13 secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.

Passagem geométrica do vibrador 4 cm: atende entre estribos nas faixas calculadas. Esse controle não comprova ausência de congestionamento nos encontros. Espaçamento transversal entre ramos e respectivos limites estão preservados no resultado bruto; quatro ramos com peças sobrepostas dependem da disposição do corte.

Trecho 1: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

**Suspensão: ** V49→V26: APOIO DIRETO PC21C; SUSPENSAO NAO SE APLICA

Origem: detalhe 7403; recorte 7403_V49.png; esforços e resultados por modelo/trecho no JSON desta emissão. Cada linha conserva arquivo, número de linha e envoltória TQS.

### V50

Geometria nominal do detalhe: 24×50 cm; 24×87 cm. Forma/detalhamento: presença nominal confirmada. Comparação nominal de seções conforme inventário. Situacao longitudinal: VAO E MUDANCA50/87 cm LOCALIZADOS.

Mudanca 50/87 cm localizada pela cota 130 cm: x TQS=3,005 m. Positiva nao atende emh 50 e atende emh 87; ver tabela regional. Estribos externos 6,3 c 10; pecas da primeira etapa excluidas. Suspensao na V34 depende da quantidade local de estribos e complemento na V50.

**Flexão positiva - solicitações Mk e resistência equivalente MRd/γf em tf·m.**

| Modelo/trecho | Apoios | b×h(cm) | Armadura | d(cm) | Mk | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V50/1 | V34-P751 | 24×50 | 2Ø16 | 45,07 | 8,71 | 5,52 | ATENDE | NÃO ATENDE |


**Flexao positiva regional - conclusao aplicavel as alturas reais.**

| h(cm) | Intervalo modelo(m) | d(cm) | Mk(tf·m) | MRd/γf(tf·m) | Resultado |
| --- | --- | --- | --- | --- | --- |
| 50 | 0,150-3,005 | 45,07 | 8,71 | 5,52 | NÃO ATENDE |
| 87 | 3,005-4,305 | 82,07 | 6,77 | 10,23 | ATENDE |


Origem: Concretopy; geometria_e_flexao_regional_V49_V50.json. Cota 130 cm medida da mudanca de altura ate a face interna do pilar direito. Fundo continuo; nao e degrau de fundo. A tabela regional prevalece sobre a comparacao nominal unica acima.

**Flexao negativa - maximo de cada lado do apoio; valores absolutos em tf·m.**

E=inicio do trecho; D=fim do trecho. Em apoio intermediario, fim do trecho anterior e inicio do seguinte sao verificacoes distintas.

| Trecho/lado | Apoio | h(cm) | Armadura superior | d(cm) | Mk negativo | MRd/γf | Mínimo | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1/E | V34 | 50 | 2Ø10 | 45,37 | 0,000 | 2,224 | SEM MkNEGATIVO | ATENDE |
| 1/D | P751 | 87 | 2Ø12,5 | 82,25 | 4,332 | 6,311 | NÃO ATENDE | ATENDE |


Mínimo não atendido no apoio P751: As=2,45 cm²; mínimo absoluto=3,13 cm²; momento mínimo equivalente=7,36 tf·m; resistência equivalente=6,31 tf·m.

Mínimos: comparação de MRd do Concretopy com Md, mín=0,8W0 fctk, sup e taxa absoluta 0,15%, conforme 17.3.5.2.1. O arquivo bruto também conserva a avaliação tabelada do motor; ela não substitui a verificação com d efetivo. A falta de momento positivo não demonstra necessidade de armadura positiva mínima na face não tracionada.

**Cortante - Vk característico em tf; taxas em cm²/m.**

| Trecho | Intervalo modelo(m) | Estribo | d(cm) | Vk | Fornecida | Exigida | Área | s máximo L/T | Biela |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/10 | 45,07 | 12,56 | 6,23 | 3,87 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |
| 1 | INTERVALO TQS INTEIRO (LIMITE) | 2 r Ø6,3 c/10 | 82,07 | 12,56 | 6,23 | 3,08 | ATENDE | L: ATENDE / T: ATENDE | ATENDE |


INTERVALO TQS INTEIRO (LIMITE): maior|Vk| de todas as 13 secoes e duas envoltorias do intervalo, inclusive apoios; atendimento com esse valor comprova resistencia por limite superior. Nao representa a posicao real da faixa nem encerra sua cobertura geometrica.

Passagem geométrica do vibrador 4 cm: atende entre estribos nas faixas calculadas. Esse controle não comprova ausência de congestionamento nos encontros. Espaçamento transversal entre ramos e respectivos limites estão preservados no resultado bruto; quatro ramos com peças sobrepostas dependem da disposição do corte.

Trecho 1: domínio de cortante conserva referência do TQS; associação integral das faces/faixas ao eixo físico ainda não concluída. Atendimento numérico não equivale à aprovação da cobertura física.

**Suspensão: ** V50→V34: TIRANTE INTEGRAL A COMPROVAR

Origem: detalhe 7403; recorte 7403_V50.png; esforços e resultados por modelo/trecho no JSON desta emissão. Cada linha conserva arquivo, número de linha e envoltória TQS.

## 7. Itens ainda não encerrados e responsabilidade pela pendência

| Item | O que falta | Origem da pendência |
| --- | --- | --- |
| Geometria de todos os vãos | Concluir comparação de cotas forma/detalhe e associação de faces de blocos em todas as vigas | Leitura/registro pelo assistente não concluído; não é ausência documental comprovada |
| V23/V24/V42 | Concluir transicoes internas; secoes nominais dos picos e apoios ja identificadas. V49/V50 encerradas quanto a posicao das mudancas 50/87 cm | Associacao de transicoes nao encerrada; divergenciah 110 da V42 mantida |
| V31/V41 sobre V12/V13 | Sentido e eixos confirmados; concluir eventual distribuicao alternativa na ligacao V41-V13 e eficacia dos estribos compostos | Distribuicao uniforme 75/25 nao atende V41-V13; nao e falta de confirmacao do apoio |
| V17-V23, V17-V42, V35-V15, V36-V5 | Consultar esforcos por caso de gravidade e vento; definir sentido fisico antes de calcular suspensao ou levantamento | Analise separada de Joao, expressamente autorizada; caso 1 localizado, listagem disponivel sem esforcos de barras |
| V21-V22, V32-V15, V50-V34 | Comprovar quantidade/posicao efetiva dos estribos na regiao normativa e completar 100% do tirante | Faixas e encontros localizados; fase dos estribos e reparticao do tirante integral nao encerradas |
| Peças de estribo 138/50 cm | Comprovar ancoragem e funcionamento conjunto na altura final 165 cm | Detalhe composto exige interpretação resistente; não somar quatro ramos automaticamente |
| Cabimento das armaduras nos nós | Confrontar centros, pernas dos estribos e barras das vigas/pilares que se encontram | Não encerrado nesta emissão; passagem 4 cm entre estribos não comprova o nó |


Decisões de João já incorporadas: C35 uniforme; marcas/cortes prevalecem; vibrador 4 cm; NB de P756/P761 mantido; exclusão de barras da primeira etapa; inclusão dos cálculos convencionais das vigas altas; PAR excluídos; anotações separadas; condições para d/2 confirmadas nos dois locais; V31 apoia V12; V41 apoia V13; inicio 1B no eixo; V49 direto no bloco PC21C; estribos compostos avaliados apenas pelas pranchas recebidas. Não reapresentar essas decisões como dúvidas abertas.

## 8. Arquivos de cálculo e rastreabilidade

Resultados oficiais de seção: verificacoes_globais_concretopy.json. Entradas: entradas_vigas_50.json. Dados TQS: tqs_operacional_atual.json; validacao_tqs_atual.json. Ligações: suspensao_inventario_global.json, suspensao_V19_V20.json, suspensao_sobreposicoes_V29_V39.json. Decisões: decisoes_confirmadas_2026-10-16.json. Integração: manifesto_integracao_global.json e auditoria_floor_review.json. Evidências visuais na pasta evidencias. Histórico de rodadas preservado.

SHA256 do VGESFS atual: f0bd8b39543e76e0be317035ba3315418c4d8159086a1ff16be547f167436d38. Identificacao e assinaturas dos PDFs eminventario_fontes_atual.json; copias desta retomada preservadas emfontes_retomada. A7201 tem registro proprio emevidencias/7201_fonte.json. A7402 foi regravada: 85089 linhas e 12 recortes coincidem com o acervo. A7403 tambem foi regravada: 97707 linhas coincidem; 16 recortes conferidos por identidade de pixels em configuracao equivalente e V33 por comparacao visual. As diferencas de V33 sao comentarios e realces. Revisao dos negativos emrevisao_negativos_por_lado.json, com arquivo e linha TQS de cada lado. Evidencias emauditoria_fontes_congeladas_retomada.json. Anotacoes sao propostas separadas; originais preservados.
