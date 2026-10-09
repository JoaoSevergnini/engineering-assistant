# Diagnóstico consolidado — V536

Pavimento: DIFERENCIADO.

Estado técnico: **FAIL**. Execução: **PARTIALLY_EXECUTED**.

| Disciplina | Execução | Resultado técnico |
|---|---|---|
| positive_flexure | PARTIALLY_EXECUTED | INCONCLUSIVE |
| negative_flexure | NOT_EXECUTED | INCONCLUSIVE |
| anchorage | PARTIALLY_EXECUTED | FAIL |
| shear | NOT_EXECUTED | INCONCLUSIVE |
| suspension | NOT_EXECUTED | INCONCLUSIVE |

Geometria, materiais, fontes e versões constam no contexto do JSON associado.

## ('DISCIPLINE', 'anchorage')

| Ocorrência | Controle | Estado | Vão / intervalo | Necessário | Fornecido | Unidade | Motivo / pendência |
|---|---|---|---|---|---|---|---|
| occ-1e6543a3649f03b8fbcfdec2 | module_coverage | INCONCLUSIVE | [None, None] | não documentado | não documentado | não documentado | ['module_scope_incomplete', ['applicable checks not completely documented', 'physical_location_not_documented']] |
| occ-50816f07df7cf5588098a111 | module_coverage | INCONCLUSIVE | [None, None] | não documentado | não documentado | não documentado | ['module_scope_incomplete', ['applicable checks not completely documented', 'physical_location_not_documented']] |

## ('DISCIPLINE', 'negative_flexure')

| Ocorrência | Controle | Estado | Vão / intervalo | Necessário | Fornecido | Unidade | Motivo / pendência |
|---|---|---|---|---|---|---|---|
| occ-a399ae8cb48fbaa0be2befc7 | module_availability | INCONCLUSIVE | [None, None] | não documentado | não documentado | não documentado | ['module_not_executed', ['module results unavailable']] |

## ('DISCIPLINE', 'positive_flexure')

| Ocorrência | Controle | Estado | Vão / intervalo | Necessário | Fornecido | Unidade | Motivo / pendência |
|---|---|---|---|---|---|---|---|
| occ-c6457d9270aa959378c13c30 | module_coverage | INCONCLUSIVE | [None, None] | não documentado | não documentado | não documentado | ['module_scope_incomplete', ['applicable checks not completely documented', 'physical_location_not_documented']] |
| occ-fee0ee3c028bc4ca8d9c67aa | module_coverage | INCONCLUSIVE | [None, None] | não documentado | não documentado | não documentado | ['module_scope_incomplete', ['applicable checks not completely documented', 'physical_location_not_documented']] |

## ('DISCIPLINE', 'shear')

| Ocorrência | Controle | Estado | Vão / intervalo | Necessário | Fornecido | Unidade | Motivo / pendência |
|---|---|---|---|---|---|---|---|
| occ-0ae214cebacb67742a1e730d | module_availability | INCONCLUSIVE | [None, None] | não documentado | não documentado | não documentado | ['module_not_executed', ['module results unavailable']] |

## ('DISCIPLINE', 'suspension')

| Ocorrência | Controle | Estado | Vão / intervalo | Necessário | Fornecido | Unidade | Motivo / pendência |
|---|---|---|---|---|---|---|---|
| occ-8b7dbbfa2246426cea15d674 | module_availability | INCONCLUSIVE | [None, None] | não documentado | não documentado | não documentado | ['module_not_executed', ['module results unavailable']] |

## ('REGION', 1, (-0.12, 0.12))

| Ocorrência | Controle | Estado | Vão / intervalo | Necessário | Fornecido | Unidade | Motivo / pendência |
|---|---|---|---|---|---|---|---|
| occ-0bddcba88bc0059747b8f7f9 | node_complete | INCONCLUSIVE | [1, [-0.12, 0.12]] | não documentado | não documentado | não documentado | [None, ['original check unresolved']] |

## ('REGION', 1, (3.06, 4.26))

| Ocorrência | Controle | Estado | Vão / intervalo | Necessário | Fornecido | Unidade | Motivo / pendência |
|---|---|---|---|---|---|---|---|
| occ-b67ab118e03014433c5347b7 | node_complete | INCONCLUSIVE | [1, [3.06, 4.26]] | não documentado | não documentado | não documentado | [None, ['original check unresolved']] |

## ('REINFORCEMENT', ('N2', 'N3'), None)

| Ocorrência | Controle | Estado | Vão / intervalo | Necessário | Fornecido | Unidade | Motivo / pendência |
|---|---|---|---|---|---|---|---|
| occ-d3bb660f3c53f5e23bc6b67f | flexural_capacity | INCONCLUSIVE | [1, [3.06, 3.66]] | 317.74526665 | não documentado | kN.m | ['unresolved', ['unresolved']] |

## ('REINFORCEMENT', ('N2',), None)

| Ocorrência | Controle | Estado | Vão / intervalo | Necessário | Fornecido | Unidade | Motivo / pendência |
|---|---|---|---|---|---|---|---|
| occ-3f66ba59fc8bc308d79db1f2 | flexural_capacity | INCONCLUSIVE | [1, [0.0, 0.12]] | 22.82007455 | não documentado | kN.m | ['unresolved', ['unresolved']] |
| occ-59354ae06699de58cbbd1fbb | anchorage_length | FAIL | [1, [-0.12, 0.12]] | 24.203000349699796 | 21.5 | cm | ['existing support anchorage', []] |

## Auditoria dos modos de ancoragem

Nenhuma observação de modo não governante.

6 relações individuais preservadas no JSON, sem expandir todas as combinações neste relatório.

Nenhuma correção proposta ou selecionada; selected_solution=null e detailing_optimization=null. Não é declaração de segurança global da estrutura.
