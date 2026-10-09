# Diagnóstico consolidado — V516

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
| occ-62c58e423a0b78cbba6403f5 | module_coverage | INCONCLUSIVE | [None, None] | não documentado | não documentado | não documentado | ['module_scope_incomplete', ['applicable checks not completely documented', 'physical_location_not_documented']] |

## ('DISCIPLINE', 'negative_flexure')

| Ocorrência | Controle | Estado | Vão / intervalo | Necessário | Fornecido | Unidade | Motivo / pendência |
|---|---|---|---|---|---|---|---|
| occ-2036f2e3c258f94ff137eac2 | module_coverage | INCONCLUSIVE | [None, None] | não documentado | não documentado | não documentado | ['module_scope_incomplete', ['applicable checks not completely documented', 'physical_location_not_documented']] |

## ('DISCIPLINE', 'positive_flexure')

| Ocorrência | Controle | Estado | Vão / intervalo | Necessário | Fornecido | Unidade | Motivo / pendência |
|---|---|---|---|---|---|---|---|
| occ-3dc6614de9704988e84e18cf | module_availability | INCONCLUSIVE | [None, None] | não documentado | não documentado | não documentado | ['module_not_executed', ['module results unavailable']] |

## ('DISCIPLINE', 'shear')

| Ocorrência | Controle | Estado | Vão / intervalo | Necessário | Fornecido | Unidade | Motivo / pendência |
|---|---|---|---|---|---|---|---|
| occ-2047821b6eb393b53ecae18c | module_coverage | INCONCLUSIVE | [None, None] | não documentado | não documentado | não documentado | ['module_scope_incomplete', ['applicable checks not completely documented', 'physical_location_not_documented']] |

## ('DISCIPLINE', 'suspension')

| Ocorrência | Controle | Estado | Vão / intervalo | Necessário | Fornecido | Unidade | Motivo / pendência |
|---|---|---|---|---|---|---|---|
| occ-26bac0893b09c5f3d622d9ee | suspension_inventory | INCONCLUSIVE | [None, None] | não documentado | não documentado | não documentado | ['suspension inventory incomplete', ['suspension inventory incomplete', 'physical_location_not_documented']] |
| occ-2da070165b60f7e147411881 | module_coverage | INCONCLUSIVE | [None, None] | não documentado | não documentado | não documentado | ['module_scope_incomplete', ['applicable checks not completely documented', 'physical_location_not_documented']] |

## ('REGION', 1, (0.12, 1.97))

| Ocorrência | Controle | Estado | Vão / intervalo | Necessário | Fornecido | Unidade | Motivo / pendência |
|---|---|---|---|---|---|---|---|
| occ-ba5736a3c2a655ef4511254d | drawing_coverage | INCONCLUSIVE | [1, [0.12, 1.97]] | não documentado | não documentado | não documentado | ['UNCOVERED_REQUIRED_REGION', ['UNCOVERED_REQUIRED_REGION']] |

## ('REGION', 4, (11.71, 13.56))

| Ocorrência | Controle | Estado | Vão / intervalo | Necessário | Fornecido | Unidade | Motivo / pendência |
|---|---|---|---|---|---|---|---|
| occ-c6433478a4bcbc0a9df58a1c | drawing_coverage | INCONCLUSIVE | [4, [11.71, 13.56]] | não documentado | não documentado | não documentado | ['UNCOVERED_REQUIRED_REGION', ['UNCOVERED_REQUIRED_REGION']] |

## ('REINFORCEMENT', ('N3', 'N4', 'N7'), None)

| Ocorrência | Controle | Estado | Vão / intervalo | Necessário | Fornecido | Unidade | Motivo / pendência |
|---|---|---|---|---|---|---|---|
| occ-e32333415a1f096c62acf5fe | flexural_capacity | INCONCLUSIVE | [2, [3.635, 3.67]] | não documentado | não documentado | não documentado | [['resistant_positions_not_defined_for_tail_overlap'], [['resistant_positions_not_defined_for_tail_overlap']]] |

## ('REINFORCEMENT', ('N4', 'N7'), None)

| Ocorrência | Controle | Estado | Vão / intervalo | Necessário | Fornecido | Unidade | Motivo / pendência |
|---|---|---|---|---|---|---|---|
| occ-3fa58bcdcdfea30d97236678 | local_spacing_geometry | INCONCLUSIVE | [2, None] | não documentado | não documentado | não documentado | [None, ['original check unresolved', 'physical_location_not_documented']] |
| occ-44e7c6686bf0e88aa3bf6a04 | flexural_capacity | INCONCLUSIVE | [2, [3.67, 5.015]] | não documentado | não documentado | não documentado | [['resistant_positions_not_defined_for_tail_overlap'], [['resistant_positions_not_defined_for_tail_overlap']]] |
| occ-b2ea77eeb3b4a35724195f0d | vibrator_access_spacing | INCONCLUSIVE | [2, None] | não documentado | não documentado | não documentado | ['documentary_transverse_centers_missing', ['documentary_transverse_centers_missing', 'physical_location_not_documented']] |

## ('REINFORCEMENT', ('N4',), 'V516/support-1/P5A')

| Ocorrência | Controle | Estado | Vão / intervalo | Necessário | Fornecido | Unidade | Motivo / pendência |
|---|---|---|---|---|---|---|---|
| occ-2edf8f1dd2a8f290b8dffedb | vibrator_access_spacing | INCONCLUSIVE | [1, [-0.12, 0.12]] | não documentado | não documentado | não documentado | ['documentary_transverse_centers_missing', ['documentary_transverse_centers_missing']] |
| occ-3168920856b004dc78992357 | minimum_bar_spacing | INCONCLUSIVE | [1, [-0.12, 0.12]] | não documentado | não documentado | não documentado | ['documentary_transverse_centers_missing', ['documentary_transverse_centers_missing']] |
| occ-3d2c8765b2b54b0f5bad2990 | column_interference_spacing | INCONCLUSIVE | [1, [-0.12, 0.12]] | não documentado | não documentado | não documentado | ['column_perpendicular_dimension_missing', ['column_perpendicular_dimension_missing']] |
| occ-786245a7c0b220008124775d | vertical_bend_geometry | FAIL | [1, [-0.12, 0.12]] | 48.7 | 40 | cm | ['engineer_confirmed_negative_end_support_vertical_bend_v1', []] |
| occ-99e06c5594a3fa1f10f07a81 | curved_anchorage_resistance | INCONCLUSIVE | [1, [-0.12, 0.12]] | não documentado | não documentado | não documentado | ['Curved anchorage resistance, pin/radius and node confinement not represented; no alpha=0.7 credit', ['Curved anchorage resistance, pin/radius and node confinement not represented; no alpha=0.7 credit']] |

## ('REINFORCEMENT', ('N7', 'N7'), None)

| Ocorrência | Controle | Estado | Vão / intervalo | Necessário | Fornecido | Unidade | Motivo / pendência |
|---|---|---|---|---|---|---|---|
| occ-0b222b35b00b1f4f59331b36 | vibrator_access_spacing | INCONCLUSIVE | [3, None] | não documentado | não documentado | não documentado | [None, ['original check unresolved', 'physical_location_not_documented']] |
| occ-2c76484f4ec4c49ff80c36bb | local_spacing_geometry | INCONCLUSIVE | [3, None] | não documentado | não documentado | não documentado | [None, ['original check unresolved', 'physical_location_not_documented']] |

## ('REINFORCEMENT', ('N7', 'N8', 'N9'), None)

| Ocorrência | Controle | Estado | Vão / intervalo | Necessário | Fornecido | Unidade | Motivo / pendência |
|---|---|---|---|---|---|---|---|
| occ-9a2176b059a99c9a176fa784 | flexural_capacity | FAIL | [3, [9.16, 10.446]] | 168.9881928 | 160.31741548190314 | kN.m | ['original regional capacity comparison', []] |

## ('REINFORCEMENT', ('N7',), 'V516/support-5/P6A')

| Ocorrência | Controle | Estado | Vão / intervalo | Necessário | Fornecido | Unidade | Motivo / pendência |
|---|---|---|---|---|---|---|---|
| occ-0b82ea375c0ed3ff95cc04ca | minimum_bar_spacing | INCONCLUSIVE | [4, [13.56, 13.8]] | não documentado | não documentado | não documentado | ['documentary_transverse_centers_missing', ['documentary_transverse_centers_missing']] |
| occ-185f4eae3a147b9f29d3a9fa | vibrator_access_spacing | INCONCLUSIVE | [4, [13.56, 13.8]] | não documentado | não documentado | não documentado | ['documentary_transverse_centers_missing', ['documentary_transverse_centers_missing']] |
| occ-b1f56dd8f3851dd7ecad8cce | curved_anchorage_resistance | INCONCLUSIVE | [4, [13.56, 13.8]] | não documentado | não documentado | não documentado | ['Curved anchorage resistance, pin/radius and node confinement not represented; no alpha=0.7 credit', ['Curved anchorage resistance, pin/radius and node confinement not represented; no alpha=0.7 credit']] |
| occ-fa2b77bd12e1ba4b37802787 | vertical_bend_geometry | FAIL | [4, [13.56, 13.8]] | 48.7 | 45 | cm | ['engineer_confirmed_negative_end_support_vertical_bend_v1', []] |
| occ-febde9bcf9230a7b9d59e289 | column_interference_spacing | INCONCLUSIVE | [4, [13.56, 13.8]] | não documentado | não documentado | não documentado | ['column_perpendicular_dimension_missing', ['column_perpendicular_dimension_missing']] |

## ('REINFORCEMENT', ('N8',), None)

| Ocorrência | Controle | Estado | Vão / intervalo | Necessário | Fornecido | Unidade | Motivo / pendência |
|---|---|---|---|---|---|---|---|
| occ-8a762d444ee8f471631649fe | al_plus_lb | FAIL | [2, [5.83, 5.83]] | 126.67384157702772 | 79.0 | cm | ['engineer_confirmed_negative_al_same_as_positive_v1', []] |

## Auditoria dos modos de ancoragem

['N7']: straight_anchorage_geometry = FAIL original; observação não governante porque a peça é verificada em VERTICAL_BEND. A dobra e a resistência curva permanecem controles independentes.
['N4']: straight_anchorage_geometry = FAIL original; observação não governante porque a peça é verificada em VERTICAL_BEND. A dobra e a resistência curva permanecem controles independentes.

118 relações individuais preservadas no JSON, sem expandir todas as combinações neste relatório.

Nenhuma correção proposta ou selecionada; selected_solution=null e detailing_optimization=null. Não é declaração de segurança global da estrutura.
