# Diagnóstico consolidado — V517

Pavimento: DIFERENCIADO.

Estado técnico: **FAIL**. Execução: **PARTIALLY_EXECUTED**.

| Disciplina | Execução | Resultado técnico |
|---|---|---|
| positive_flexure | NOT_EXECUTED | INCONCLUSIVE |
| negative_flexure | PARTIALLY_EXECUTED | FAIL |
| anchorage | PARTIALLY_EXECUTED | FAIL |
| shear | PARTIALLY_EXECUTED | INCONCLUSIVE |
| suspension | PARTIALLY_EXECUTED | INCONCLUSIVE |

Geometria, materiais, fontes e versões constam no contexto do JSON associado.

## ('DISCIPLINE', 'anchorage')

| Ocorrência | Controle | Estado | Vão / intervalo | Necessário | Fornecido | Unidade | Motivo / pendência |
|---|---|---|---|---|---|---|---|
| occ-ba715060a757692ce4dc2f55 | module_coverage | INCONCLUSIVE | [None, None] | não documentado | não documentado | não documentado | ['module_scope_incomplete', ['applicable checks not completely documented', 'physical_location_not_documented']] |

## ('DISCIPLINE', 'negative_flexure')

| Ocorrência | Controle | Estado | Vão / intervalo | Necessário | Fornecido | Unidade | Motivo / pendência |
|---|---|---|---|---|---|---|---|
| occ-2176faa4c9229eb205345f87 | module_coverage | INCONCLUSIVE | [None, None] | não documentado | não documentado | não documentado | ['module_scope_incomplete', ['applicable checks not completely documented', 'physical_location_not_documented']] |

## ('DISCIPLINE', 'positive_flexure')

| Ocorrência | Controle | Estado | Vão / intervalo | Necessário | Fornecido | Unidade | Motivo / pendência |
|---|---|---|---|---|---|---|---|
| occ-f267681fdd1f7500e9269246 | module_availability | INCONCLUSIVE | [None, None] | não documentado | não documentado | não documentado | ['module_not_executed', ['module results unavailable']] |

## ('DISCIPLINE', 'shear')

| Ocorrência | Controle | Estado | Vão / intervalo | Necessário | Fornecido | Unidade | Motivo / pendência |
|---|---|---|---|---|---|---|---|
| occ-34d4802bced1a5382df08005 | module_coverage | INCONCLUSIVE | [None, None] | não documentado | não documentado | não documentado | ['module_scope_incomplete', ['applicable checks not completely documented', 'physical_location_not_documented']] |

## ('DISCIPLINE', 'suspension')

| Ocorrência | Controle | Estado | Vão / intervalo | Necessário | Fornecido | Unidade | Motivo / pendência |
|---|---|---|---|---|---|---|---|
| occ-885ca8244429f18be6047bf9 | suspension_inventory | INCONCLUSIVE | [None, None] | não documentado | não documentado | não documentado | ['suspension inventory incomplete', ['suspension inventory incomplete', 'physical_location_not_documented']] |
| occ-e1d583c9f29a23a3adaf390c | module_coverage | INCONCLUSIVE | [None, None] | não documentado | não documentado | não documentado | ['module_scope_incomplete', ['applicable checks not completely documented', 'physical_location_not_documented']] |

## ('REGION', 1, (0.12, 1.97))

| Ocorrência | Controle | Estado | Vão / intervalo | Necessário | Fornecido | Unidade | Motivo / pendência |
|---|---|---|---|---|---|---|---|
| occ-22ddfd0d56f25aace3fafebe | drawing_coverage | INCONCLUSIVE | [1, [0.12, 1.97]] | não documentado | não documentado | não documentado | ['UNCOVERED_REQUIRED_REGION', ['UNCOVERED_REQUIRED_REGION']] |

## ('REGION', 4, (11.71, 13.56))

| Ocorrência | Controle | Estado | Vão / intervalo | Necessário | Fornecido | Unidade | Motivo / pendência |
|---|---|---|---|---|---|---|---|
| occ-d6f366f6f56d4139cff41b5d | drawing_coverage | INCONCLUSIVE | [4, [11.71, 13.56]] | não documentado | não documentado | não documentado | ['UNCOVERED_REQUIRED_REGION', ['UNCOVERED_REQUIRED_REGION']] |

## ('REINFORCEMENT', ('N3', 'N4', 'N7'), None)

| Ocorrência | Controle | Estado | Vão / intervalo | Necessário | Fornecido | Unidade | Motivo / pendência |
|---|---|---|---|---|---|---|---|
| occ-4142fa0881128809a21f316e | flexural_capacity | INCONCLUSIVE | [2, [3.635, 3.67]] | não documentado | não documentado | não documentado | [['resistant_positions_not_defined_for_tail_overlap'], [['resistant_positions_not_defined_for_tail_overlap']]] |

## ('REINFORCEMENT', ('N4', 'N7'), None)

| Ocorrência | Controle | Estado | Vão / intervalo | Necessário | Fornecido | Unidade | Motivo / pendência |
|---|---|---|---|---|---|---|---|
| occ-3fa86180959dd9bc210ca03a | local_spacing_geometry | INCONCLUSIVE | [2, None] | não documentado | não documentado | não documentado | [None, ['original check unresolved', 'physical_location_not_documented']] |
| occ-48e1151000075e5a52842894 | flexural_capacity | INCONCLUSIVE | [2, [3.67, 5.015]] | não documentado | não documentado | não documentado | [['resistant_positions_not_defined_for_tail_overlap'], [['resistant_positions_not_defined_for_tail_overlap']]] |
| occ-510d0f5b70ba0f1068927ed9 | vibrator_access_spacing | INCONCLUSIVE | [2, None] | não documentado | não documentado | não documentado | ['documentary_transverse_centers_missing', ['documentary_transverse_centers_missing', 'physical_location_not_documented']] |

## ('REINFORCEMENT', ('N4',), 'V517/support-1/P5B')

| Ocorrência | Controle | Estado | Vão / intervalo | Necessário | Fornecido | Unidade | Motivo / pendência |
|---|---|---|---|---|---|---|---|
| occ-3738800c29adae35602dbe0c | minimum_bar_spacing | INCONCLUSIVE | [1, [-0.12, 0.12]] | não documentado | não documentado | não documentado | ['documentary_transverse_centers_missing', ['documentary_transverse_centers_missing']] |
| occ-5fd1e24fb6937e2a8346fa9b | vibrator_access_spacing | INCONCLUSIVE | [1, [-0.12, 0.12]] | não documentado | não documentado | não documentado | ['documentary_transverse_centers_missing', ['documentary_transverse_centers_missing']] |
| occ-960805dc00137e94f98d5f9e | vertical_bend_geometry | FAIL | [1, [-0.12, 0.12]] | 48.7 | 40 | cm | ['engineer_confirmed_negative_end_support_vertical_bend_v1', []] |
| occ-c3d40806e6ee36f42226f783 | column_interference_spacing | INCONCLUSIVE | [1, [-0.12, 0.12]] | não documentado | não documentado | não documentado | ['column_perpendicular_dimension_missing', ['column_perpendicular_dimension_missing']] |
| occ-ff5f08c34c05aeb259c189f1 | curved_anchorage_resistance | INCONCLUSIVE | [1, [-0.12, 0.12]] | não documentado | não documentado | não documentado | ['Curved anchorage resistance, pin/radius and node confinement not represented; no alpha=0.7 credit', ['Curved anchorage resistance, pin/radius and node confinement not represented; no alpha=0.7 credit']] |

## ('REINFORCEMENT', ('N7', 'N7'), None)

| Ocorrência | Controle | Estado | Vão / intervalo | Necessário | Fornecido | Unidade | Motivo / pendência |
|---|---|---|---|---|---|---|---|
| occ-246873c2c41a7ab73bf196d3 | vibrator_access_spacing | INCONCLUSIVE | [3, None] | não documentado | não documentado | não documentado | [None, ['original check unresolved', 'physical_location_not_documented']] |
| occ-6331d11b266b92dd1bb92218 | local_spacing_geometry | INCONCLUSIVE | [3, None] | não documentado | não documentado | não documentado | [None, ['original check unresolved', 'physical_location_not_documented']] |

## ('REINFORCEMENT', ('N7', 'N8', 'N9'), None)

| Ocorrência | Controle | Estado | Vão / intervalo | Necessário | Fornecido | Unidade | Motivo / pendência |
|---|---|---|---|---|---|---|---|
| occ-c194a577e11c55630b4b259e | flexural_capacity | FAIL | [3, [9.16, 10.446]] | 162.3785107 | 160.31741548190314 | kN.m | ['original regional capacity comparison', []] |

## ('REINFORCEMENT', ('N7',), 'V517/support-5/P6B')

| Ocorrência | Controle | Estado | Vão / intervalo | Necessário | Fornecido | Unidade | Motivo / pendência |
|---|---|---|---|---|---|---|---|
| occ-9479200e474a74f6186c7fef | column_interference_spacing | INCONCLUSIVE | [4, [13.56, 13.8]] | não documentado | não documentado | não documentado | ['column_perpendicular_dimension_missing', ['column_perpendicular_dimension_missing']] |
| occ-9d7d081755d9e97429eaedc4 | vibrator_access_spacing | INCONCLUSIVE | [4, [13.56, 13.8]] | não documentado | não documentado | não documentado | ['documentary_transverse_centers_missing', ['documentary_transverse_centers_missing']] |
| occ-be97625f8475bec7aab9403e | curved_anchorage_resistance | INCONCLUSIVE | [4, [13.56, 13.8]] | não documentado | não documentado | não documentado | ['Curved anchorage resistance, pin/radius and node confinement not represented; no alpha=0.7 credit', ['Curved anchorage resistance, pin/radius and node confinement not represented; no alpha=0.7 credit']] |
| occ-db336c0402fdae7b31d7b92a | minimum_bar_spacing | INCONCLUSIVE | [4, [13.56, 13.8]] | não documentado | não documentado | não documentado | ['documentary_transverse_centers_missing', ['documentary_transverse_centers_missing']] |
| occ-efd4a93fa316e85799dbdad9 | vertical_bend_geometry | FAIL | [4, [13.56, 13.8]] | 48.7 | 45 | cm | ['engineer_confirmed_negative_end_support_vertical_bend_v1', []] |

## ('REINFORCEMENT', ('N8',), None)

| Ocorrência | Controle | Estado | Vão / intervalo | Necessário | Fornecido | Unidade | Motivo / pendência |
|---|---|---|---|---|---|---|---|
| occ-3c4a4b82a54883f57d5f6af3 | al_plus_lb | FAIL | [2, [5.83, 5.83]] | 126.67384157702772 | 79.0 | cm | ['engineer_confirmed_negative_al_same_as_positive_v1', []] |

## Auditoria dos modos de ancoragem

['N4']: straight_anchorage_geometry = FAIL original; observação não governante porque a peça é verificada em VERTICAL_BEND. A dobra e a resistência curva permanecem controles independentes.
['N7']: straight_anchorage_geometry = FAIL original; observação não governante porque a peça é verificada em VERTICAL_BEND. A dobra e a resistência curva permanecem controles independentes.

118 relações individuais preservadas no JSON, sem expandir todas as combinações neste relatório.

Nenhuma correção proposta ou selecionada; selected_solution=null e detailing_optimization=null. Não é declaração de segurança global da estrutura.
