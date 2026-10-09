# Diagnóstico consolidado — V501

Pavimento: DIFERENCIADO.

Contexto e fontes: {'beam_id': 'V501', 'floor': 'DIFERENCIADO', 'floor_source': {'project_directory': 'C:\\TQS\\24-155-COLLINE-RESIDENCIAL-R60\\DIFERENCIADO\\VIGAS'}, 'coordinate_system': {'origin': 'left_support_axis', 'positive_direction': 'left_to_right', 'unit': 'm'}, 'geometry': [{'id': 1, 'geometry': {'length': 7.552, 'width': 0.19, 'height': 0.72, 'top_flange_width': 0.0, 'bottom_flange_width': 0.0, 'section_type': 1.0, 'top_slab_thickness': 0.0, 'bottom_slab_thickness': 0.0, 'top_face_to_axis': 0.36, 'side_face_to_axis': 0.095, 'support_axis_length': None, 'clear_span_length': None}}], 'materials': {'concrete': {'fck': None}, 'steel': {'grade': None}, 'aggregate_max_size': 0.015}, 'tqs_source': {'path': 'analises\\pranchas\\V501_tqs.json', 'sha256': '0cf0847d245630e5ac2ab6036e3264d2983e735a1a4940072ac93b50bb9c6067'}, 'data_version': '1.1', 'drawing_source': {'path': 'C:\\Users\\João Severgnini\\Documents\\engineering-assistant\\analises\\pranchas\\V501_V503_beam_model.json', 'sha256': 'a454b67725ad2b57d43eb67db043697adbfd99f64c4e46b01252187fc1868506'}, 'coordinate_source': {'path': 'analises\\pranchas\\V501_beam_mapping.json', 'sha256': 'd14d54a4a666a2bb1fbaa34084e4082ebf9b37b79aa30ad897c2057e4f77dc05'}, 'physical_geometry': {'detailing_clear_span': 7.11, 'tqs_clear_span': 7.12, 'difference': 0.01, 'tqs_minus_detail': 0.01, 'status': 'mismatch', 'tqs_length': 7.552, 'support_axis_length': 8.43}}

| Disciplina | Estado |
|---|---|
| positive_flexure | INCONCLUSIVE |
| negative_flexure | INCONCLUSIVE |
| anchorage | INCONCLUSIVE |
| shear | INCONCLUSIVE |
| suspension | INCONCLUSIVE |

## Inconformidades comprovadas

| ID | Controle | Estado | Vão / intervalo | Armadura | Necessário | Fornecido | Unidade | Motivo / pendência |
|---|---|---|---|---|---|---|---|---|

## Pendências e revisão de engenharia

| ID | Controle | Estado | Vão / intervalo | Armadura | Necessário | Fornecido | Unidade | Motivo / pendência |
|---|---|---|---|---|---|---|---|---|
| occ-0c6dba5441257063fe8e29b3 | flexural_capacity | INCONCLUSIVE | [1, [5.97, 5.97]] | ['N5'] | não documentado | não documentado | kN.m | ['demand_not_sampled', ['demand_not_sampled']] |
| occ-21d95d7e105ceb451ce1af9f | flexural_capacity | INCONCLUSIVE | [1, [8.22, 8.43]] | [] | não documentado | não documentado | kN.m | ['demand_not_sampled', ['demand_not_sampled']] |
| occ-2e6d63da5dae2dbc58f3fdbf | module_availability | INCONCLUSIVE | [None, None] | [] | não documentado | não documentado | não documentado | ['module_not_executed', ['module results unavailable']] |
| occ-5c8f357a2aa99f71ba2f9d75 | flexural_capacity | INCONCLUSIVE | [1, [6.69, 6.69]] | ['N5'] | não documentado | não documentado | kN.m | ['demand_not_sampled', ['demand_not_sampled']] |
| occ-988982da5a924a5060ff0a3d | module_coverage | INCONCLUSIVE | [None, None] | [] | não documentado | não documentado | não documentado | ['module_scope_incomplete', ['applicable checks not completely documented', 'physical_location_not_documented']] |
| occ-b961e6bce955384294c911ef | module_availability | INCONCLUSIVE | [None, None] | [] | não documentado | não documentado | não documentado | ['module_not_executed', ['module results unavailable']] |
| occ-bb304beb0185514082028fcd | module_availability | INCONCLUSIVE | [None, None] | [] | não documentado | não documentado | não documentado | ['module_not_executed', ['module results unavailable']] |
| occ-d566c3064b4e16488ab4fb2e | flexural_capacity | INCONCLUSIVE | [1, [0.0, 0.07]] | [] | não documentado | não documentado | kN.m | ['demand_not_sampled', ['demand_not_sampled']] |
| occ-da419a72cd16334149e40c91 | module_availability | INCONCLUSIVE | [None, None] | [] | não documentado | não documentado | não documentado | ['module_not_executed', ['module results unavailable']] |

## Relações entre ocorrências

{'occurrences': ['occ-0c6dba5441257063fe8e29b3', 'occ-5c8f357a2aa99f71ba2f9d75'], 'shared_reinforcement': ['N5'], 'physical_overlap': False, 'single_correction_proven': False}

Estado consolidado: **INCONCLUSIVE**. Falhas, pendências e revisões permanecem separadas no JSON. Aprovação limitada às verificações documentadas; não é declaração de segurança global da estrutura.

Nenhuma correção proposta ou selecionada; selected_solution=null e detailing_optimization=null.
