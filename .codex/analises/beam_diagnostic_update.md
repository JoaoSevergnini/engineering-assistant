# Atualização do diagnóstico e preparação do módulo de correções

## Escopo e arquitetura

Esta rodada verifica o detalhamento existente. Não gera alternativas, propostas reais nem PDFs. `selected_solution` e `detailing_optimization` continuam null. Concretopy não foi alterado. O consolidador histórico permanece reproduzível; `attach_execution` acrescenta a vista 1.1, sem mudar os estados técnicos ou IDs anteriores. A interpretação geométrica fica em beam_mapping; contratos futuros ficam em módulo próprio sem cálculos resistentes.

## Arquivos desta rodada

- `tools/beam_mapping/termination_geometry.py`: interpretação rastreável das pontas sem cotas.
- `tools/reinforcement_checks/beam_diagnostic.py`: execução independente e apresentação agrupada; observações de modo separadas.
- `tools/reinforcement_checks/detailing_change_contracts.py`: preferências configuráveis e contrato serializável de alteração, sem gerador.
- `tools/reinforcement_checks/test_diagnostic_update.py`: 20 testes novos de estados, agrupamento, contratos, geometria e casos reais.
- `analises/pranchas/validar_atualizacao_diagnostico.py`: reverificação da configuração existente V536, sem chamar buscas.
- `tools/reinforcement_checks/diagnostic_update.md`, README, Skill e referência beam-diagnostic: procedimento operacional.
- Novos resultados: `V536_positive_diagnostic_reverification.json`, `V536/V516/V517_beam_diagnostic_updated.json`, relatórios homônimos em `.codex/analises`, `future_detailing_contracts.json`, `diagnostic_update_preservation.json`.

## Convenção e V536

Decisão `engineer_confirmed_undimensioned_bar_end_external_column_face_v1`: cota explícita prevalece. Na ponta sem cota em pilar extremo, usar a face externa física, sem converter deslocamento gráfico em comprimento. Ambas as pontas em apoios sem cotas permanecem inconclusivas. Não inferir dobra nem comprimento resistente.

N2 esquerda: representação anterior -0,090 m; interpretação atual -0,120 m, face externa do apoio de 24 cm centrado em x=0. A ponta direita em 3,880 m preserva a reconstrução auditada 294+82 cm, com tradução de origem. Projeção física entre pontas: 400 cm. O comprimento desenvolvido original de 455 cm e a dobra de 58 cm permanecem documentais; sua consistência conjunta não foi automaticamente comprovada. Os arquivos de entrada originais não foram alterados.

Reexecutados os módulos existentes de flexão documental, flexão por regiões, escalonamento N3 e ancoragens esquerda/direita. Não foram geradas alternativas nem recalculados cenários exploratórios de grampos.

| Controle | Resultado |
|---|---|
| Escalonamento N3 A e B | PASS |
| Ancoragem N2 à esquerda | FAIL |
| Ancoragem à direita | PASS |
| Diagnóstico V536 | FAIL / PARTIALLY_EXECUTED |

N2: As efetiva=9,424777961 cm²; demanda=5,917167968 cm². lb básico=55,071689104 cm; lb_nec=24,203000350 cm. Comprimento disponível para verificação=21,5 cm, pela decisão geométrica apoio-cobrimento; margem=-2,703000350 cm. As adicional retornada pela API=1,184892006 cm². A penetração física de 24 cm não substitui lb_ef. O cenário de gancho anteriormente confirmado foi preservado; não recebeu validação nova pela convenção de extremidade.

## Execução e apresentação

NOT_EXECUTED distingue ausência de execução de falta de conclusão técnica. PARTIALLY_EXECUTED indica escopo parcialmente disponível. EXECUTED_INCONCLUSIVE indica execução com dependência inconclusiva. EXECUTED_COMPLETE não significa aprovação: FAIL pode coexistir com execução completa. Nos três casos reais o diagnóstico técnico permanece FAIL e a execução é parcial.

Markdown agrupa ocorrências por marca, apoio ou região. O JSON conserva todos os controles, IDs, fontes e relações individuais; não são impressas todas as combinações de pares. Inviabilidade reta em VERTICAL_BEND fica auditada com seu FAIL original como observação não governante. Falhas de dobra e resistência não são suprimidas. Resistência curva permanece inconclusiva quando faltam parâmetros.

V516/V517 preservam integralmente seus IDs e resultados técnicos históricos, inclusive insuficiência regional à esquerda de P1, falha N8/LEFT e falhas das dobras N4/N7. Nenhuma nova interpretação longitudinal dessas vigas foi aplicada.

## Contratos futuros

Preferências incluem alteração de quantidades, bitolas, comprimentos, redistribuição, posições adicionais e mistura de diâmetros. Até dois passos na série é preferência configurável do engenheiro, não norma. Excesso moderado é admissível sem percentuais arbitrários; insuficiência não é admissível. O contrato de proposta guarda identidade, fonte/versão, marca, geometrias, operação, grandezas/unidades, controles afetados, reverificações, evidências, pendências e aprovação. Referência gráfica e correspondência física-gráfica permanecem null no modelo vazio. Aprovação não é automática e exige reverificações completas e evidência explícita.

## Validação e limites

- Engineering-assistant: 1.035 testes aprovados (39 extrator, 30 modelo, 57 mapeamento, 909 verificações). São 20 novos em relação aos 1.015 anteriores.
- Concretopy: 427 testes aprovados, sem alteração nesta rodada.
- quick_validate: Skill válida.
- git diff --check: aprovado nos dois repositórios; somente avisos de conversão LF/CRLF.
- Auditoria SHA-256: 188 arquivos anteriores de resultados, relatórios e Python do Concretopy preservados, conforme diagnostic_update_preservation.json.

Continuam pendentes controles documentais/geométricos já registrados. A convenção não comprova fabricação da dobra, resistência curva, interferências do nó nem correspondência com coordenadas PDF. Os contratos não implementam otimizador, seleção de correção ou edição de prancha. Não houve aprovação global da viga.
