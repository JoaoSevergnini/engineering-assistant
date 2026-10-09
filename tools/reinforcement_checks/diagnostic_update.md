# Atualização do diagnóstico e contratos futuros

Usar `attach_execution(consolidate(context, modules))` para a vista aditiva 1.1. O contrato histórico 1.0 continua reproduzível. Execução e resultado técnico são independentes: NOT_EXECUTED (sem execução), PARTIALLY_EXECUTED (parte do escopo disponível), EXECUTED_INCONCLUSIVE (escopo executado com dependência inconclusiva) e EXECUTED_COMPLETE (controles concluídos, inclusive FAIL). Uma falha comprovada permanece FAIL.

O Markdown agrupa por armadura, apoio ou região física. JSON preserva todas as ocorrências, IDs, evidências e relações. Relações não provam uma correção comum. A impossibilidade reta em modo VERTICAL_BEND permanece observação de seleção de modo com FAIL original auditado, sem governar novamente. Geometria da dobra e resistência curva são controles independentes; parâmetros ausentes continuam inconclusivos.

## Extremidades sem cota

`tools/beam_mapping/termination_geometry.py` registra `engineer_confirmed_undimensioned_bar_end_external_column_face_v1`. Em apoio extremo comprovadamente em pilar, extremidade sem cota coincide com a face externa física. Cotas explícitas com fonte prevalecem sobre o desenho esquemático. Duas pontas dentro de apoios sem cotas permanecem inconclusivas. Não inferir dobra, comprimento desenvolvido nem crédito resistente de ancoragem.

O ensaio V536 preserva a reconstrução cotada da ponta direita e muda somente a interpretação esquerda da N2 para -0,120 m. A projeção entre pontas passa a 400 cm no modelo físico; os 455 cm desenvolvidos e a dobra documental de 58 cm permanecem originais. Sua consistência conjunta não foi comprovada. A penetração física de 24 cm não substitui lb_ef=24-2,5=21,5 cm.

## Contratos, sem geração de soluções

`detailing_change_contracts.py` oferece preferências configuráveis e modelo serializável de proposta. Permite futuramente alterar quantidade, bitola, comprimento, redistribuição, novas posições e mistura de bitolas. Prioridades: validade estrutural, execução simples, aproveitamento do existente e simplicidade. Até dois passos na série comercial é preferência configurável do engenheiro, não norma. Excesso moderado é admissível sem percentual arbitrário; valores abaixo dos necessários não são admissíveis.

O contrato guarda viga/pavimento, fonte/versão, marca, geometrias original/proposta, operação, grandezas/unidades, controles afetados, reverificações, evidências, pendências e aprovação. Aprovação exige evidência explícita e reverificação completa dos controles afetados. Aplicação gráfica exige correspondência física-gráfica comprovada; referência PDF permanece null quando desconhecida. Nenhuma proposta real, otimização ou edição de PDF é executada.

Fixture de nova revisão: `analises/pranchas/validar_atualizacao_diagnostico.py`. Saídas próprias `*_beam_diagnostic_updated.json` e relatórios homônimos; históricos não são sobrescritos. Concretopy continua responsável por resistência, al e ancoragem.
