# ATP S07 — rodada 04 — seção final e faces dos blocos

16/10/2026. Esta atualização substitui as premissas de contribuição das barras intermediárias e de cobertura até faces de pilares usadas na rodada03. Origem dos esclarecimentos: João e sua imagem anotada da V4. [Critérios registrados](criterios_s07_secao_final.md).

## O que foi corrigido

- Barras longitudinais do topo da primeira concretagem excluídas da resistência e de d. Usadas as armaduras externas da seção final, com altura total das duas concretagens.
- Retirada a pendência de conhecer a cota dessas barras intermediárias para esses controles. Mantidas dúvidas reais de transição, marca/bitola, material e composição externa.
- Retirados como provas de falta de cobertura os déficits anteriormente apresentados para V4 (25,40 cm), V5 (100 cm), V33 e V40 (89,50 cm). A referência deve ser a face do bloco, conforme esclarecimento do engenheiro. A V4 fornecida demonstra a distinção entre face do pilar e face do bloco.
- Resultados oficiais provenientes de **novas execuções do Concretopy**, com entradas e retornos íntegros em `resultados_secao_final_concretopy.json` e origem das funções em `proveniencia_concretopy.json`. Não foram usados limites algébricos independentes para capacidade oficial.

## Abrangência e limites desta atualização

42 vigas usuais, 82 intervalos com cálculo positivo e de cortante, e 136 consultas de capacidade negativa. Foram usados os esforços do instantâneo TQS já auditado, sem nova importação do modelo. Momento negativo mantém o máximo no apoio selecionado na revisão anterior; não retorna ao valor interpolado na face. Preservadas seções constantes registradas do detalhamento e sensibilidades C35/C40; a classe real de cada região deve prevalecer.

Na flexão, a função executada foi `Concretopy.verificar_flexao_viga_retangular`, modelo `bloco_retangular_camadas_escoadas_v1`. No cortante, `Concretopy.dimensionar_cortante_viga`, por meio do adaptador público existente `shear_review.design_shear`. Os motores não foram alterados. A reaplicação da regra de d pelo centroide das camadas externas alterou 16 alturas úteis de cortante; anteriormente alguns valores correspondiam à camada mais interna, não ao centroide governante.

Resultados apresentados em tf/tf·m. Capacidades equivalentes MRd/γf, γf=1,4 neste conjunto; γc=1,4 e γs=1,15 continuam aplicados. O JSON bruto preserva unidades internas do motor; decisões usam valores completos. Mínimos longitudinais, cobertura física integral, ancoragem/escalonamento e demais mecanismos não são declarados aprovados pela nova execução de flexão/cortante.

## Positivas desfavoráveis nas configurações consultadas

A contribuição antes aventada das barras da primeira concretagem não é mais uma dependência ou justificativa de suficiência. A tabela abaixo identifica as configurações externas desfavoráveis, sem concluir sobre regiões de geometria/transição ainda não conciliadas.

| Viga/modelo/vão | Mk (tf·m) | Capacidade equivalente C35/C40 (tf·m) | Ressalva |
|---|---:|---:|---|
| V16/V16/1 | 15,28 | 6,84/6,86 | Resultado da seção externa registrada; manter coerência documental |
| V21/V21/1 | 16,87 | 16,08/16,30 | Reconcile actual stirrup input with drawing; archived first-span input is phi8, engineer spreadsheet phi6.3 |
| V25/V25/4 | 7,50 | 5,13/5,15 | Resultado da seção externa registrada; manter coerência documental |
| V35/V35/1 | 9,97 | 8,50/8,56 | Resultado da seção externa registrada; manter coerência documental |
| V37/V37/1 | 9,95 | 8,50/8,56 | Check each actual stirrup zone with its own Vk peak in block-bounded physical domain |
| V24/V24/1 | 4,00 | 3,45/3,46 | Resolve local height/step incidence; retained section labels are not transition verification; Final upper reinforcement not fully registered; shear depth selection limited to available lower group |
| V49/V49/1 | 8,33 | 5,09/5,11 | Resolve local height/step incidence; retained section labels are not transition verification; Check each actual stirrup zone with its own Vk peak in block-bounded physical domain; Final upper reinforcement not fully registered; shear depth selection limited to available lower group |
| V50/V50/1 | 8,71 | 5,52/5,55 | Resolve local height/step incidence; retained section labels are not transition verification; Check each actual stirrup zone with its own Vk peak in block-bounded physical domain; Final upper reinforcement not fully registered; shear depth selection limited to available lower group |

## Cortante — nova altura útil, localização física ainda a concluir

A incerteza artificial criada pela contribuição das barras de topo da primeira etapa foi eliminada. O cortante foi recalculado com d da armadura externa final. **Entretanto, os esforços de referência abaixo ainda são os máximos da consulta anterior entre faces do modelo**: não foi inventada a coordenada de nenhuma face de bloco. Nos casos com faixas variáveis, a configuração fraca usada na triagem anterior continua sendo uma referência numérica, não uma verificação regional encerrada. Deve-se associar as faces dos blocos ao eixo TQS, consultar o esforço de cada faixa real e então concluir o atendimento da faixa.

| Viga/modelo/vão | d anterior → atual (cm) | Vk de referência (tf) | Asw/s considerado (cm²/m) | Asw/s requerido C35/C40 (cm²/m) | Situação física |
|---|---:|---:|---:|---:|---|
| V4/V4/1 | 44,87 → 44,87 | 21,81 | 6,23 | 7,21/6,30 | Faixas variáveis e faces dos blocos |
| V15/V15/2 | 44,87 → 44,87 | 23,22 | 6,23 | 8,31/7,40 | Faixas variáveis e faces dos blocos |
| V15/V15/3 | 40,87 → 44,37 | 20,66 | 6,23 | 6,49/5,61 | Faixas variáveis e faces dos blocos |
| V35/V35/1 | 44,87 → 45,07 | 20,56 | 4,16 | 8,62/7,94 | Faces dos blocos e domínio próprio da faixa |
| V35/V35/2 | 45,07 → 45,07 | 18,77 | 4,16 | 7,23/6,54 | Faces dos blocos e domínio próprio da faixa |
| V36/V36/1 | 45,07 → 45,07 | 22,57 | 4,16 | 10,19/9,50 | Faces dos blocos e domínio próprio da faixa |
| V37/V37/1 | 44,87 → 44,87 | 18,56 | 4,16 | 7,13/6,44 | Faixas variáveis e faces dos blocos |
| V47/V47/1 | 44,70 → 44,70 | 28,83 | 10,05 | 15,25/14,56 | Faces dos blocos e domínio próprio da faixa |
| V48/V48/1 | 44,87 → 45,07 | 21,05 | 4,16 | 9,00/8,32 | Faces dos blocos e domínio próprio da faixa |
| V49/V49/1 | 45,24 → 45,24 | 11,78 | 3,12 | 3,23/3,37 | Faixas variáveis e faces dos blocos; transição de seção |

Os alertas numéricos não são apagados; mudou sua interpretação e foram eliminadas as dependências indevidas sobre barras intermediárias. Não afirmar que todos os cortantes estejam aprovados nem manter reprovação documental derivada da face errada. Para V18, V21, V33 e demais vigas, a orientação das faces dos blocos também deve ser observada onde houver interseção; resultados da configuração consultada não substituem essa compatibilização.

## Pendências que permanecem

- Localização das faces reais dos blocos e das faixas de estribos no eixo do diagrama; esforço próprio de cada faixa. A imagem da V4 esclarece a interpretação, sem fornecer todas as cotas dos demais encontros.
- Degraus e alturas locais em V23/V24/V42/V49/V50; não usar seção média nem trasladar barras entre níveis.
- Conflitos de marcas/rótulos ainda vigentes e bitolas efetivamente detalhadas, inclusive a entrada Ø8 da V21 versus Ø6,3 da planilha do engenheiro. Não modificar a bitola só para reproduzir a planilha.
- Aplicação dos concretos C35/C40 por região/etapa e condições de redução do cortante; não reprovar C35 por um alerta exclusivo de mínimo em C40.
- Suspensão e ligações com geometria ainda não conciliada. Os resultados V19/V20 permanecem no histórico da rodada03; não houve nova execução de suspensão nesta atualização.
- Passagem do vibrador/adensamento e demais controles executivos já individualizados. Vigas-parede e PAR permanecem para análise separada de João.

**Não há aprovação global do pavimento.** A presente rodada corrige premissas e cálculos afetados, preserva os resultados oficiais e distingue o que ainda exige associação física documental. Os resultados completos, positivos/negativos/cortante e respectivos dados, estão em `resultados_secao_final_concretopy.json`.
