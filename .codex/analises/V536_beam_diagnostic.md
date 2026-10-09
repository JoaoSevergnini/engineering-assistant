# Diagnóstico consolidado — V536

Pavimento: DIFERENCIADO.

Contexto e fontes: {'beam_id': 'V536', 'floor': 'DIFERENCIADO', 'floor_source': {'project_directory': 'C:\\TQS\\24-155-COLLINE-RESIDENCIAL-R60\\DIFERENCIADO\\VIGAS'}, 'coordinate_system': {'origin': 'left_support_axis', 'positive_direction': 'left_to_right', 'unit': 'm'}, 'geometry': [{'id': 1, 'geometry': {'length': 3.276, 'width': 0.19, 'height': 0.72, 'top_flange_width': None, 'bottom_flange_width': 0.0, 'section_type': 2.0, 'top_slab_thickness': 0.1, 'bottom_slab_thickness': 0.0, 'top_face_to_axis': 0.36, 'side_face_to_axis': 0.095, 'support_axis_length': None, 'clear_span_length': None}}], 'materials': {'concrete': {'fck': None}, 'steel': {'grade': None}, 'aggregate_max_size': 0.015}, 'tqs_source': {'path': 'analises\\pranchas\\V536_tqs.json', 'sha256': 'f2890481277dd3ca0933c09ee7e188f02c2efb8378a3c94f0350b0245473beb7'}, 'data_version': '1.1', 'drawing_source': {'path': 'analises/pranchas/V536_V565_detalhamento_prancha.json', 'sha256': 'af8a7e6dc40ad7f0c4b1b16706a1cdef785236b11d62dd89f7f733981b3f0613'}, 'coordinate_source': {'path': 'analises\\pranchas\\V536_beam_mapping.json', 'sha256': '7b7f843312061252da691886a12f9dc45b678943b8b37f4fa3eb938e69c8fc59'}, 'physical_geometry': {'detailing_clear_span': 2.94, 'tqs_clear_span': 2.94, 'difference': 0.0, 'tqs_minus_detail': 0.0, 'status': 'exact', 'tqs_length': 3.276, 'support_axis_length': 3.66}, 'coverage': {'physical_domain_m': [0.0, 3.66], 'sampled_domain_m': [0.0, 3.276], 'whole_physical_domain_sampled': False, 'extrapolation': False}}

| Disciplina | Estado |
|---|---|
| positive_flexure | INCONCLUSIVE |
| negative_flexure | INCONCLUSIVE |
| anchorage | FAIL |
| shear | INCONCLUSIVE |
| suspension | INCONCLUSIVE |

## Inconformidades comprovadas

| ID | Controle | Estado | Vão / intervalo | Armadura | Necessário | Fornecido | Unidade | Motivo / pendência |
|---|---|---|---|---|---|---|---|---|
| occ-cc5c33e4f26233a99f9becd3 | anchorage_length | FAIL | [None, None] | ['N2'] | 24.203000349699796 | 21.5 | cm | ['ANCORAGEM_INSUFICIENTE', ['physical_location_not_documented']] |

## Pendências e revisão de engenharia

| ID | Controle | Estado | Vão / intervalo | Armadura | Necessário | Fornecido | Unidade | Motivo / pendência |
|---|---|---|---|---|---|---|---|---|
| occ-0ae214cebacb67742a1e730d | module_availability | INCONCLUSIVE | [None, None] | [] | não documentado | não documentado | não documentado | ['module_not_executed', ['module results unavailable']] |
| occ-0ef673b43fa6475b291136ae | support_geometry | INCONCLUSIVE | [None, None] | ['N2'] | não documentado | não documentado | não documentado | ['gancho_geometria_nao_verificada', ['gancho_geometria_nao_verificada', 'physical_location_not_documented']] |
| occ-151fcbe247bfaa61b5b96e6c | support_complete | INCONCLUSIVE | ['V536:1', [3.06, 4.26]] | ['N2', 'N3'] | não documentado | não documentado | não documentado | [None, ['original check unresolved']] |
| occ-35a4cf96d4bac66c0c00ad8f | module_coverage | INCONCLUSIVE | [None, None] | [] | não documentado | não documentado | não documentado | ['module_scope_incomplete', ['applicable checks not completely documented', 'physical_location_not_documented']] |
| occ-502dbbec872ae3865d326ce4 | module_coverage | INCONCLUSIVE | [None, None] | [] | não documentado | não documentado | não documentado | ['module_scope_incomplete', ['applicable checks not completely documented', 'physical_location_not_documented']] |
| occ-55bafa5f18f791e291c198b4 | support_geometry | INCONCLUSIVE | [None, None] | ['N2'] | não documentado | não documentado | não documentado | ['configuracao_local_nao_verifica_flexao_do_vao', ['configuracao_local_nao_verifica_flexao_do_vao', 'physical_location_not_documented']] |
| occ-607fc6d995b3f310be073953 | support_geometry | INCONCLUSIVE | [None, None] | ['N2'] | não documentado | não documentado | não documentado | ['nao_dimensiona_grampos', ['nao_dimensiona_grampos', 'physical_location_not_documented']] |
| occ-6bc7408ba548472aee04c953 | flexural_capacity | INCONCLUSIVE | [1, [3.06, 3.66]] | ['N2', 'N3'] | 317.74526665 | não documentado | kN.m | ['unresolved', ['unresolved']] |
| occ-713d740b56f83a5060c62108 | support_geometry | INCONCLUSIVE | [None, None] | ['N2'] | não documentado | não documentado | não documentado | ['geometria_transversal_nao_verificada', ['geometria_transversal_nao_verificada', 'physical_location_not_documented']] |
| occ-8b7dbbfa2246426cea15d674 | module_availability | INCONCLUSIVE | [None, None] | [] | não documentado | não documentado | não documentado | ['module_not_executed', ['module results unavailable']] |
| occ-a399ae8cb48fbaa0be2befc7 | module_availability | INCONCLUSIVE | [None, None] | [] | não documentado | não documentado | não documentado | ['module_not_executed', ['module results unavailable']] |
| occ-b94848c59ecc206c638bb9a6 | support_geometry | INCONCLUSIVE | [None, None] | ['N2'] | não documentado | não documentado | não documentado | ['nao_aprova_viga', ['nao_aprova_viga', 'physical_location_not_documented']] |
| occ-f3208e56ed35fda3ac04d9be | module_coverage | INCONCLUSIVE | [None, None] | [] | não documentado | não documentado | não documentado | ['module_scope_incomplete', ['applicable checks not completely documented', 'physical_location_not_documented']] |
| occ-fb08845db1c8cc52c95cb4e9 | flexural_capacity | INCONCLUSIVE | [1, [0.0, 0.12]] | ['N2'] | 22.82007455 | não documentado | kN.m | ['unresolved', ['unresolved']] |
| occ-fb28db5564364339b50fb21f | module_coverage | INCONCLUSIVE | [None, None] | [] | não documentado | não documentado | não documentado | ['module_scope_incomplete', ['applicable checks not completely documented', 'physical_location_not_documented']] |

## Relações entre ocorrências

{'occurrences': ['occ-0ef673b43fa6475b291136ae', 'occ-151fcbe247bfaa61b5b96e6c'], 'shared_reinforcement': ['N2'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-0ef673b43fa6475b291136ae', 'occ-55bafa5f18f791e291c198b4'], 'shared_reinforcement': ['N2'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-0ef673b43fa6475b291136ae', 'occ-607fc6d995b3f310be073953'], 'shared_reinforcement': ['N2'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-0ef673b43fa6475b291136ae', 'occ-6bc7408ba548472aee04c953'], 'shared_reinforcement': ['N2'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-0ef673b43fa6475b291136ae', 'occ-713d740b56f83a5060c62108'], 'shared_reinforcement': ['N2'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-0ef673b43fa6475b291136ae', 'occ-b94848c59ecc206c638bb9a6'], 'shared_reinforcement': ['N2'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-0ef673b43fa6475b291136ae', 'occ-cc5c33e4f26233a99f9becd3'], 'shared_reinforcement': ['N2'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-0ef673b43fa6475b291136ae', 'occ-fb08845db1c8cc52c95cb4e9'], 'shared_reinforcement': ['N2'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-151fcbe247bfaa61b5b96e6c', 'occ-55bafa5f18f791e291c198b4'], 'shared_reinforcement': ['N2'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-151fcbe247bfaa61b5b96e6c', 'occ-607fc6d995b3f310be073953'], 'shared_reinforcement': ['N2'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-151fcbe247bfaa61b5b96e6c', 'occ-6bc7408ba548472aee04c953'], 'shared_reinforcement': ['N2', 'N3'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-151fcbe247bfaa61b5b96e6c', 'occ-713d740b56f83a5060c62108'], 'shared_reinforcement': ['N2'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-151fcbe247bfaa61b5b96e6c', 'occ-b94848c59ecc206c638bb9a6'], 'shared_reinforcement': ['N2'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-151fcbe247bfaa61b5b96e6c', 'occ-cc5c33e4f26233a99f9becd3'], 'shared_reinforcement': ['N2'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-151fcbe247bfaa61b5b96e6c', 'occ-fb08845db1c8cc52c95cb4e9'], 'shared_reinforcement': ['N2'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-55bafa5f18f791e291c198b4', 'occ-607fc6d995b3f310be073953'], 'shared_reinforcement': ['N2'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-55bafa5f18f791e291c198b4', 'occ-6bc7408ba548472aee04c953'], 'shared_reinforcement': ['N2'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-55bafa5f18f791e291c198b4', 'occ-713d740b56f83a5060c62108'], 'shared_reinforcement': ['N2'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-55bafa5f18f791e291c198b4', 'occ-b94848c59ecc206c638bb9a6'], 'shared_reinforcement': ['N2'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-55bafa5f18f791e291c198b4', 'occ-cc5c33e4f26233a99f9becd3'], 'shared_reinforcement': ['N2'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-55bafa5f18f791e291c198b4', 'occ-fb08845db1c8cc52c95cb4e9'], 'shared_reinforcement': ['N2'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-607fc6d995b3f310be073953', 'occ-6bc7408ba548472aee04c953'], 'shared_reinforcement': ['N2'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-607fc6d995b3f310be073953', 'occ-713d740b56f83a5060c62108'], 'shared_reinforcement': ['N2'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-607fc6d995b3f310be073953', 'occ-b94848c59ecc206c638bb9a6'], 'shared_reinforcement': ['N2'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-607fc6d995b3f310be073953', 'occ-cc5c33e4f26233a99f9becd3'], 'shared_reinforcement': ['N2'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-607fc6d995b3f310be073953', 'occ-fb08845db1c8cc52c95cb4e9'], 'shared_reinforcement': ['N2'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-6bc7408ba548472aee04c953', 'occ-713d740b56f83a5060c62108'], 'shared_reinforcement': ['N2'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-6bc7408ba548472aee04c953', 'occ-b94848c59ecc206c638bb9a6'], 'shared_reinforcement': ['N2'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-6bc7408ba548472aee04c953', 'occ-cc5c33e4f26233a99f9becd3'], 'shared_reinforcement': ['N2'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-6bc7408ba548472aee04c953', 'occ-fb08845db1c8cc52c95cb4e9'], 'shared_reinforcement': ['N2'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-713d740b56f83a5060c62108', 'occ-b94848c59ecc206c638bb9a6'], 'shared_reinforcement': ['N2'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-713d740b56f83a5060c62108', 'occ-cc5c33e4f26233a99f9becd3'], 'shared_reinforcement': ['N2'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-713d740b56f83a5060c62108', 'occ-fb08845db1c8cc52c95cb4e9'], 'shared_reinforcement': ['N2'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-b94848c59ecc206c638bb9a6', 'occ-cc5c33e4f26233a99f9becd3'], 'shared_reinforcement': ['N2'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-b94848c59ecc206c638bb9a6', 'occ-fb08845db1c8cc52c95cb4e9'], 'shared_reinforcement': ['N2'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-cc5c33e4f26233a99f9becd3', 'occ-fb08845db1c8cc52c95cb4e9'], 'shared_reinforcement': ['N2'], 'physical_overlap': False, 'single_correction_proven': False}

Estado consolidado: **FAIL**. Falhas, pendências e revisões permanecem separadas no JSON. Aprovação limitada às verificações documentadas; não é declaração de segurança global da estrutura.

Nenhuma correção proposta ou selecionada; selected_solution=null e detailing_optimization=null.
