# Diagnóstico consolidado — V565

Pavimento: DIFERENCIADO.

Contexto e fontes: {'beam_id': 'V565', 'floor': 'DIFERENCIADO', 'floor_source': {'project_directory': 'C:\\TQS\\24-155-COLLINE-RESIDENCIAL-R60\\DIFERENCIADO\\VIGAS'}, 'coordinate_system': {'origin': 'left_support_axis', 'positive_direction': 'left_to_right', 'unit': 'm'}, 'geometry': [{'id': 1, 'geometry': {'length': 3.276, 'width': 0.19, 'height': 0.72, 'top_flange_width': None, 'bottom_flange_width': 0.0, 'section_type': 2.0, 'top_slab_thickness': 0.1, 'bottom_slab_thickness': 0.0, 'top_face_to_axis': 0.36, 'side_face_to_axis': 0.095, 'support_axis_length': None, 'clear_span_length': None}}], 'materials': {'concrete': {'fck': None}, 'steel': {'grade': None}, 'aggregate_max_size': 0.015}, 'tqs_source': {'path': 'analises\\pranchas\\V565_tqs.json', 'sha256': '97dae1934988b05c3494a7440a764ef23cd91f59fb2ce3408e62586c4360e6c9'}, 'data_version': '1.1', 'drawing_source': None, 'coordinate_source': {'path': 'analises\\pranchas\\V565_beam_mapping.json', 'sha256': 'd5c42b3cc378f7b2484875d351ed29a329488670ce314a2e00a763132d82a0aa'}, 'physical_geometry': {'detailing_clear_span': 2.94, 'tqs_clear_span': 2.94, 'difference': 0.0, 'tqs_minus_detail': 0.0, 'status': 'exact', 'tqs_length': 3.276, 'support_axis_length': 3.66}}

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
| occ-0740500f090ab87872275ff9 | module_availability | INCONCLUSIVE | [None, None] | [] | não documentado | não documentado | não documentado | ['module_not_executed', ['module results unavailable']] |
| occ-3303b73b3d8cd1abd454dff9 | module_availability | INCONCLUSIVE | [None, None] | [] | não documentado | não documentado | não documentado | ['module_not_executed', ['module results unavailable']] |
| occ-3b04030dbc81c50a46bc3f3e | support_geometry | INCONCLUSIVE | [None, None] | ['N2'] | não documentado | não documentado | não documentado | ['nao_aprova_viga', ['nao_aprova_viga', 'physical_location_not_documented']] |
| occ-4c3a97aebac0390d4878286f | module_availability | INCONCLUSIVE | [None, None] | [] | não documentado | não documentado | não documentado | ['module_not_executed', ['module results unavailable']] |
| occ-79f5b61d4cd6ad453fc34d09 | support_geometry | INCONCLUSIVE | [None, None] | ['N2'] | não documentado | não documentado | não documentado | ['gancho_geometria_nao_verificada', ['gancho_geometria_nao_verificada', 'physical_location_not_documented']] |
| occ-8212ac996fa6e051cee4409d | module_coverage | INCONCLUSIVE | [None, None] | [] | não documentado | não documentado | não documentado | ['module_scope_incomplete', ['applicable checks not completely documented', 'physical_location_not_documented']] |
| occ-8b1c6c52b84e3f8dc57be5a3 | support_geometry | INCONCLUSIVE | [None, None] | ['N2'] | não documentado | não documentado | não documentado | ['geometria_transversal_nao_verificada', ['geometria_transversal_nao_verificada', 'physical_location_not_documented']] |
| occ-c559b759c1df124c37fb2b17 | module_availability | INCONCLUSIVE | [None, None] | [] | não documentado | não documentado | não documentado | ['module_not_executed', ['module results unavailable']] |
| occ-de37f7b514d4e7227105df79 | support_geometry | INCONCLUSIVE | [None, None] | ['N2'] | não documentado | não documentado | não documentado | ['nao_dimensiona_grampos', ['nao_dimensiona_grampos', 'physical_location_not_documented']] |
| occ-e7da17a8cabf97caae8d0f2d | support_geometry | INCONCLUSIVE | [None, None] | ['N2'] | não documentado | não documentado | não documentado | ['configuracao_local_nao_verifica_flexao_do_vao', ['configuracao_local_nao_verifica_flexao_do_vao', 'physical_location_not_documented']] |

## Relações entre ocorrências

{'occurrences': ['occ-3b04030dbc81c50a46bc3f3e', 'occ-79f5b61d4cd6ad453fc34d09'], 'shared_reinforcement': ['N2'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-3b04030dbc81c50a46bc3f3e', 'occ-8b1c6c52b84e3f8dc57be5a3'], 'shared_reinforcement': ['N2'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-3b04030dbc81c50a46bc3f3e', 'occ-de37f7b514d4e7227105df79'], 'shared_reinforcement': ['N2'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-3b04030dbc81c50a46bc3f3e', 'occ-e7da17a8cabf97caae8d0f2d'], 'shared_reinforcement': ['N2'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-79f5b61d4cd6ad453fc34d09', 'occ-8b1c6c52b84e3f8dc57be5a3'], 'shared_reinforcement': ['N2'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-79f5b61d4cd6ad453fc34d09', 'occ-de37f7b514d4e7227105df79'], 'shared_reinforcement': ['N2'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-79f5b61d4cd6ad453fc34d09', 'occ-e7da17a8cabf97caae8d0f2d'], 'shared_reinforcement': ['N2'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-8b1c6c52b84e3f8dc57be5a3', 'occ-de37f7b514d4e7227105df79'], 'shared_reinforcement': ['N2'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-8b1c6c52b84e3f8dc57be5a3', 'occ-e7da17a8cabf97caae8d0f2d'], 'shared_reinforcement': ['N2'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-de37f7b514d4e7227105df79', 'occ-e7da17a8cabf97caae8d0f2d'], 'shared_reinforcement': ['N2'], 'physical_overlap': False, 'single_correction_proven': False}

Estado consolidado: **INCONCLUSIVE**. Falhas, pendências e revisões permanecem separadas no JSON. Aprovação limitada às verificações documentadas; não é declaração de segurança global da estrutura.

Nenhuma correção proposta ou selecionada; selected_solution=null e detailing_optimization=null.
