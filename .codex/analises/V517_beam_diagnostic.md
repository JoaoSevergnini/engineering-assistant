# Diagnóstico consolidado — V517

Pavimento: DIFERENCIADO.

Contexto e fontes: {'beam_id': 'V517', 'floor': 'DIFERENCIADO', 'floor_source': {'project_directory': 'C:\\TQS\\24-155-COLLINE-RESIDENCIAL-R60\\DIFERENCIADO\\VIGAS'}, 'coordinate_system': {'origin': 'left_support_axis', 'positive_direction': 'left_to_right', 'unit': 'm'}, 'geometry': [{'id': 1, 'geometry': {'length': 2.08, 'width': 0.19, 'height': 0.52, 'top_flange_width': 0.0, 'bottom_flange_width': 0.0, 'section_type': 1.0, 'top_slab_thickness': 0.0, 'bottom_slab_thickness': 0.0, 'top_face_to_axis': 0.26, 'side_face_to_axis': 0.095, 'support_axis_length': None, 'clear_span_length': None}}, {'id': 2, 'geometry': {'length': 4.54, 'width': 0.19, 'height': 0.52, 'top_flange_width': None, 'bottom_flange_width': 0.0, 'section_type': 5.0, 'top_slab_thickness': 0.2, 'bottom_slab_thickness': 0.0, 'top_face_to_axis': 0.26, 'side_face_to_axis': 0.095, 'support_axis_length': None, 'clear_span_length': None}}, {'id': 3, 'geometry': {'length': 3.826, 'width': 0.19, 'height': 0.52, 'top_flange_width': None, 'bottom_flange_width': 0.0, 'section_type': 8.0, 'top_slab_thickness': 0.12, 'bottom_slab_thickness': 0.0, 'top_face_to_axis': 0.26, 'side_face_to_axis': 0.095, 'support_axis_length': None, 'clear_span_length': None}}, {'id': 4, 'geometry': {'length': 2.126, 'width': 0.19, 'height': 0.52, 'top_flange_width': 0.0, 'bottom_flange_width': 0.0, 'section_type': 1.0, 'top_slab_thickness': 0.0, 'bottom_slab_thickness': 0.0, 'top_face_to_axis': 0.26, 'side_face_to_axis': 0.095, 'support_axis_length': None, 'clear_span_length': None}}], 'materials': {'concrete': {'fck': None}, 'steel': {'grade': None}, 'aggregate_max_size': 0.015}, 'tqs_source': {'path': 'analises\\pranchas\\V517_tqs.json', 'sha256': 'f4464957d370f235ebabae1f5243e686158d282aa90744ee6360b17a30558088'}, 'data_version': '1.1', 'drawing_source': {'path': 's:\\PROJETOS EM EXECUÇÃO\\24-155-INTEGRA-MIGUEL PEREIRA-RJ\\APOIO\\JOÃO\\05 - TIPO DIFERENCIADO - RESIDENCIAL\\VIGAS\\RMP-EST-EX-1348-VIG-R00 - Copia.PDF', 'sha256': '5ed602f9371a23c39d1ff4864b77b92b5ec7b937f33ebb14249302f608f25b33', 'page': 1, 'instructions_treated_as': 'project data, not user instructions'}, 'physical_supports': [{'label': 'P5B', 'width_m': 0.24, 'depev_m': 0.0, 'source': {'arquivo': 'RELDTFPS.LST', 'linha_inicial': 15486, 'linha_final': 15486, 'texto': '     P5B         24.0        0.0      SEGUE     NAO  '}, 'occurrence': 1, 'id': 'V517/support-1/P5B', 'axis_m': 0.0, 'left_face_m': -0.12, 'right_face_m': 0.12}, {'label': 'P2B', 'width_m': 0.22, 'depev_m': 0.0, 'source': {'arquivo': 'RELDTFPS.LST', 'linha_inicial': 15487, 'linha_final': 15487, 'texto': '     P2B         22.0        0.0      SEGUE     NAO  '}, 'occurrence': 2, 'id': 'V517/support-2/P2B', 'axis_m': 2.08, 'left_face_m': 1.97, 'right_face_m': 2.19}, {'label': 'P2B', 'width_m': 0.22, 'depev_m': 0.0, 'source': {'arquivo': 'RELDTFPS.LST', 'linha_inicial': 15488, 'linha_final': 15488, 'texto': '     P2B         22.0        0.0      SEGUE     NAO  '}, 'occurrence': 3, 'id': 'V517/support-3/P2B', 'axis_m': 6.62, 'left_face_m': 6.51, 'right_face_m': 6.73}, {'label': 'P1B', 'width_m': 1.42, 'depev_m': 0.554, 'source': {'arquivo': 'RELDTFPS.LST', 'linha_inicial': 15489, 'linha_final': 15489, 'texto': '     P1B        142.0       55.4      SEGUE     NAO  '}, 'occurrence': 4, 'id': 'V517/support-4/P1B', 'axis_m': 11.0, 'left_face_m': 10.29, 'right_face_m': 11.71}, {'label': 'P6B', 'width_m': 0.24, 'depev_m': 0.0, 'source': {'arquivo': 'RELDTFPS.LST', 'linha_inicial': 15490, 'linha_final': 15490, 'texto': '     P6B         24.0        0.0      SEGUE     NAO  '}, 'occurrence': 5, 'id': 'V517/support-5/P6B', 'axis_m': 13.68, 'left_face_m': 13.56, 'right_face_m': 13.8}]}

| Disciplina | Estado |
|---|---|
| positive_flexure | INCONCLUSIVE |
| negative_flexure | FAIL |
| anchorage | FAIL |
| shear | INCONCLUSIVE |
| suspension | INCONCLUSIVE |

## Inconformidades comprovadas

| ID | Controle | Estado | Vão / intervalo | Armadura | Necessário | Fornecido | Unidade | Motivo / pendência |
|---|---|---|---|---|---|---|---|---|
| occ-3c4a4b82a54883f57d5f6af3 | al_plus_lb | FAIL | [2, [5.83, 5.83]] | ['N8'] | 126.67384157702772 | 79.0 | cm | ['engineer_confirmed_negative_al_same_as_positive_v1', []] |
| occ-960805dc00137e94f98d5f9e | vertical_bend_geometry | FAIL | [1, [-0.12, 0.12]] | ['N4'] | 48.7 | 40 | cm | ['engineer_confirmed_negative_end_support_vertical_bend_v1', []] |
| occ-b0abbbd32d2a2f1c0944bb02 | straight_anchorage_geometry | FAIL (observação de modo) | [1, [-0.12, 0.12]] | ['N4'] | não documentado | não documentado | não documentado | ['A bent-bar projection is not a verified straight anchorage', []] |
| occ-c194a577e11c55630b4b259e | flexural_capacity | FAIL | [3, [9.16, 10.446]] | ['N7', 'N8', 'N9'] | 162.3785107 | 160.31741548190314 | kN.m | ['original regional capacity comparison', []] |
| occ-e530d8e9fbb9adbd1ccc99a4 | straight_anchorage_geometry | FAIL (observação de modo) | [4, [13.56, 13.8]] | ['N7'] | não documentado | não documentado | não documentado | ['A bent-bar projection is not a verified straight anchorage', []] |
| occ-efd4a93fa316e85799dbdad9 | vertical_bend_geometry | FAIL | [4, [13.56, 13.8]] | ['N7'] | 48.7 | 45 | cm | ['engineer_confirmed_negative_end_support_vertical_bend_v1', []] |

## Pendências e revisão de engenharia

| ID | Controle | Estado | Vão / intervalo | Armadura | Necessário | Fornecido | Unidade | Motivo / pendência |
|---|---|---|---|---|---|---|---|---|
| occ-2176faa4c9229eb205345f87 | module_coverage | INCONCLUSIVE | [None, None] | [] | não documentado | não documentado | não documentado | ['module_scope_incomplete', ['applicable checks not completely documented', 'physical_location_not_documented']] |
| occ-22ddfd0d56f25aace3fafebe | drawing_coverage | INCONCLUSIVE | [1, [0.12, 1.97]] | [] | não documentado | não documentado | não documentado | ['UNCOVERED_REQUIRED_REGION', ['UNCOVERED_REQUIRED_REGION']] |
| occ-246873c2c41a7ab73bf196d3 | vibrator_access_spacing | INCONCLUSIVE | [3, None] | ['N7', 'N7'] | não documentado | não documentado | não documentado | [None, ['original check unresolved', 'physical_location_not_documented']] |
| occ-34d4802bced1a5382df08005 | module_coverage | INCONCLUSIVE | [None, None] | [] | não documentado | não documentado | não documentado | ['module_scope_incomplete', ['applicable checks not completely documented', 'physical_location_not_documented']] |
| occ-3738800c29adae35602dbe0c | minimum_bar_spacing | INCONCLUSIVE | [1, [-0.12, 0.12]] | ['N4'] | não documentado | não documentado | não documentado | ['documentary_transverse_centers_missing', ['documentary_transverse_centers_missing']] |
| occ-3fa86180959dd9bc210ca03a | local_spacing_geometry | INCONCLUSIVE | [2, None] | ['N4', 'N7'] | não documentado | não documentado | não documentado | [None, ['original check unresolved', 'physical_location_not_documented']] |
| occ-4142fa0881128809a21f316e | flexural_capacity | INCONCLUSIVE | [2, [3.635, 3.67]] | ['N4', 'N3', 'N7'] | não documentado | não documentado | não documentado | [['resistant_positions_not_defined_for_tail_overlap'], [['resistant_positions_not_defined_for_tail_overlap']]] |
| occ-48e1151000075e5a52842894 | flexural_capacity | INCONCLUSIVE | [2, [3.67, 5.015]] | ['N4', 'N7'] | não documentado | não documentado | não documentado | [['resistant_positions_not_defined_for_tail_overlap'], [['resistant_positions_not_defined_for_tail_overlap']]] |
| occ-510d0f5b70ba0f1068927ed9 | vibrator_access_spacing | INCONCLUSIVE | [2, None] | ['N4', 'N7'] | não documentado | não documentado | não documentado | ['documentary_transverse_centers_missing', ['documentary_transverse_centers_missing', 'physical_location_not_documented']] |
| occ-5fd1e24fb6937e2a8346fa9b | vibrator_access_spacing | INCONCLUSIVE | [1, [-0.12, 0.12]] | ['N4'] | não documentado | não documentado | não documentado | ['documentary_transverse_centers_missing', ['documentary_transverse_centers_missing']] |
| occ-6331d11b266b92dd1bb92218 | local_spacing_geometry | INCONCLUSIVE | [3, None] | ['N7', 'N7'] | não documentado | não documentado | não documentado | [None, ['original check unresolved', 'physical_location_not_documented']] |
| occ-885ca8244429f18be6047bf9 | suspension_inventory | INCONCLUSIVE | [None, None] | [] | não documentado | não documentado | não documentado | ['suspension inventory incomplete', ['suspension inventory incomplete', 'physical_location_not_documented']] |
| occ-9479200e474a74f6186c7fef | column_interference_spacing | INCONCLUSIVE | [4, [13.56, 13.8]] | ['N7'] | não documentado | não documentado | não documentado | ['column_perpendicular_dimension_missing', ['column_perpendicular_dimension_missing']] |
| occ-9d7d081755d9e97429eaedc4 | vibrator_access_spacing | INCONCLUSIVE | [4, [13.56, 13.8]] | ['N7'] | não documentado | não documentado | não documentado | ['documentary_transverse_centers_missing', ['documentary_transverse_centers_missing']] |
| occ-ba715060a757692ce4dc2f55 | module_coverage | INCONCLUSIVE | [None, None] | [] | não documentado | não documentado | não documentado | ['module_scope_incomplete', ['applicable checks not completely documented', 'physical_location_not_documented']] |
| occ-be97625f8475bec7aab9403e | curved_anchorage_resistance | INCONCLUSIVE | [4, [13.56, 13.8]] | ['N7'] | não documentado | não documentado | não documentado | ['Curved anchorage resistance, pin/radius and node confinement not represented; no alpha=0.7 credit', ['Curved anchorage resistance, pin/radius and node confinement not represented; no alpha=0.7 credit']] |
| occ-c3d40806e6ee36f42226f783 | column_interference_spacing | INCONCLUSIVE | [1, [-0.12, 0.12]] | ['N4'] | não documentado | não documentado | não documentado | ['column_perpendicular_dimension_missing', ['column_perpendicular_dimension_missing']] |
| occ-d6f366f6f56d4139cff41b5d | drawing_coverage | INCONCLUSIVE | [4, [11.71, 13.56]] | [] | não documentado | não documentado | não documentado | ['UNCOVERED_REQUIRED_REGION', ['UNCOVERED_REQUIRED_REGION']] |
| occ-db336c0402fdae7b31d7b92a | minimum_bar_spacing | INCONCLUSIVE | [4, [13.56, 13.8]] | ['N7'] | não documentado | não documentado | não documentado | ['documentary_transverse_centers_missing', ['documentary_transverse_centers_missing']] |
| occ-e1d583c9f29a23a3adaf390c | module_coverage | INCONCLUSIVE | [None, None] | [] | não documentado | não documentado | não documentado | ['module_scope_incomplete', ['applicable checks not completely documented', 'physical_location_not_documented']] |
| occ-f267681fdd1f7500e9269246 | module_availability | INCONCLUSIVE | [None, None] | [] | não documentado | não documentado | não documentado | ['module_not_executed', ['module results unavailable']] |
| occ-ff5f08c34c05aeb259c189f1 | curved_anchorage_resistance | INCONCLUSIVE | [1, [-0.12, 0.12]] | ['N4'] | não documentado | não documentado | não documentado | ['Curved anchorage resistance, pin/radius and node confinement not represented; no alpha=0.7 credit', ['Curved anchorage resistance, pin/radius and node confinement not represented; no alpha=0.7 credit']] |

## Relações entre ocorrências

{'occurrences': ['occ-246873c2c41a7ab73bf196d3', 'occ-3fa86180959dd9bc210ca03a'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-246873c2c41a7ab73bf196d3', 'occ-4142fa0881128809a21f316e'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-246873c2c41a7ab73bf196d3', 'occ-48e1151000075e5a52842894'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-246873c2c41a7ab73bf196d3', 'occ-510d0f5b70ba0f1068927ed9'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-246873c2c41a7ab73bf196d3', 'occ-6331d11b266b92dd1bb92218'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-246873c2c41a7ab73bf196d3', 'occ-9479200e474a74f6186c7fef'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-246873c2c41a7ab73bf196d3', 'occ-9d7d081755d9e97429eaedc4'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-246873c2c41a7ab73bf196d3', 'occ-be97625f8475bec7aab9403e'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-246873c2c41a7ab73bf196d3', 'occ-c194a577e11c55630b4b259e'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-246873c2c41a7ab73bf196d3', 'occ-db336c0402fdae7b31d7b92a'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-246873c2c41a7ab73bf196d3', 'occ-e530d8e9fbb9adbd1ccc99a4'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-246873c2c41a7ab73bf196d3', 'occ-efd4a93fa316e85799dbdad9'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-3738800c29adae35602dbe0c', 'occ-3fa86180959dd9bc210ca03a'], 'shared_reinforcement': ['N4'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-3738800c29adae35602dbe0c', 'occ-4142fa0881128809a21f316e'], 'shared_reinforcement': ['N4'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-3738800c29adae35602dbe0c', 'occ-48e1151000075e5a52842894'], 'shared_reinforcement': ['N4'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-3738800c29adae35602dbe0c', 'occ-510d0f5b70ba0f1068927ed9'], 'shared_reinforcement': ['N4'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-3738800c29adae35602dbe0c', 'occ-5fd1e24fb6937e2a8346fa9b'], 'shared_reinforcement': ['N4'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-3738800c29adae35602dbe0c', 'occ-960805dc00137e94f98d5f9e'], 'shared_reinforcement': ['N4'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-3738800c29adae35602dbe0c', 'occ-b0abbbd32d2a2f1c0944bb02'], 'shared_reinforcement': ['N4'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-3738800c29adae35602dbe0c', 'occ-c3d40806e6ee36f42226f783'], 'shared_reinforcement': ['N4'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-3738800c29adae35602dbe0c', 'occ-ff5f08c34c05aeb259c189f1'], 'shared_reinforcement': ['N4'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-3c4a4b82a54883f57d5f6af3', 'occ-c194a577e11c55630b4b259e'], 'shared_reinforcement': ['N8'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-3fa86180959dd9bc210ca03a', 'occ-4142fa0881128809a21f316e'], 'shared_reinforcement': ['N4', 'N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-3fa86180959dd9bc210ca03a', 'occ-48e1151000075e5a52842894'], 'shared_reinforcement': ['N4', 'N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-3fa86180959dd9bc210ca03a', 'occ-510d0f5b70ba0f1068927ed9'], 'shared_reinforcement': ['N4', 'N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-3fa86180959dd9bc210ca03a', 'occ-5fd1e24fb6937e2a8346fa9b'], 'shared_reinforcement': ['N4'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-3fa86180959dd9bc210ca03a', 'occ-6331d11b266b92dd1bb92218'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-3fa86180959dd9bc210ca03a', 'occ-9479200e474a74f6186c7fef'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-3fa86180959dd9bc210ca03a', 'occ-960805dc00137e94f98d5f9e'], 'shared_reinforcement': ['N4'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-3fa86180959dd9bc210ca03a', 'occ-9d7d081755d9e97429eaedc4'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-3fa86180959dd9bc210ca03a', 'occ-b0abbbd32d2a2f1c0944bb02'], 'shared_reinforcement': ['N4'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-3fa86180959dd9bc210ca03a', 'occ-be97625f8475bec7aab9403e'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-3fa86180959dd9bc210ca03a', 'occ-c194a577e11c55630b4b259e'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-3fa86180959dd9bc210ca03a', 'occ-c3d40806e6ee36f42226f783'], 'shared_reinforcement': ['N4'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-3fa86180959dd9bc210ca03a', 'occ-db336c0402fdae7b31d7b92a'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-3fa86180959dd9bc210ca03a', 'occ-e530d8e9fbb9adbd1ccc99a4'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-3fa86180959dd9bc210ca03a', 'occ-efd4a93fa316e85799dbdad9'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-3fa86180959dd9bc210ca03a', 'occ-ff5f08c34c05aeb259c189f1'], 'shared_reinforcement': ['N4'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-4142fa0881128809a21f316e', 'occ-48e1151000075e5a52842894'], 'shared_reinforcement': ['N4', 'N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-4142fa0881128809a21f316e', 'occ-510d0f5b70ba0f1068927ed9'], 'shared_reinforcement': ['N4', 'N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-4142fa0881128809a21f316e', 'occ-5fd1e24fb6937e2a8346fa9b'], 'shared_reinforcement': ['N4'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-4142fa0881128809a21f316e', 'occ-6331d11b266b92dd1bb92218'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-4142fa0881128809a21f316e', 'occ-9479200e474a74f6186c7fef'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-4142fa0881128809a21f316e', 'occ-960805dc00137e94f98d5f9e'], 'shared_reinforcement': ['N4'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-4142fa0881128809a21f316e', 'occ-9d7d081755d9e97429eaedc4'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-4142fa0881128809a21f316e', 'occ-b0abbbd32d2a2f1c0944bb02'], 'shared_reinforcement': ['N4'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-4142fa0881128809a21f316e', 'occ-be97625f8475bec7aab9403e'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-4142fa0881128809a21f316e', 'occ-c194a577e11c55630b4b259e'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-4142fa0881128809a21f316e', 'occ-c3d40806e6ee36f42226f783'], 'shared_reinforcement': ['N4'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-4142fa0881128809a21f316e', 'occ-db336c0402fdae7b31d7b92a'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-4142fa0881128809a21f316e', 'occ-e530d8e9fbb9adbd1ccc99a4'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-4142fa0881128809a21f316e', 'occ-efd4a93fa316e85799dbdad9'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-4142fa0881128809a21f316e', 'occ-ff5f08c34c05aeb259c189f1'], 'shared_reinforcement': ['N4'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-48e1151000075e5a52842894', 'occ-510d0f5b70ba0f1068927ed9'], 'shared_reinforcement': ['N4', 'N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-48e1151000075e5a52842894', 'occ-5fd1e24fb6937e2a8346fa9b'], 'shared_reinforcement': ['N4'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-48e1151000075e5a52842894', 'occ-6331d11b266b92dd1bb92218'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-48e1151000075e5a52842894', 'occ-9479200e474a74f6186c7fef'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-48e1151000075e5a52842894', 'occ-960805dc00137e94f98d5f9e'], 'shared_reinforcement': ['N4'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-48e1151000075e5a52842894', 'occ-9d7d081755d9e97429eaedc4'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-48e1151000075e5a52842894', 'occ-b0abbbd32d2a2f1c0944bb02'], 'shared_reinforcement': ['N4'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-48e1151000075e5a52842894', 'occ-be97625f8475bec7aab9403e'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-48e1151000075e5a52842894', 'occ-c194a577e11c55630b4b259e'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-48e1151000075e5a52842894', 'occ-c3d40806e6ee36f42226f783'], 'shared_reinforcement': ['N4'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-48e1151000075e5a52842894', 'occ-db336c0402fdae7b31d7b92a'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-48e1151000075e5a52842894', 'occ-e530d8e9fbb9adbd1ccc99a4'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-48e1151000075e5a52842894', 'occ-efd4a93fa316e85799dbdad9'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-48e1151000075e5a52842894', 'occ-ff5f08c34c05aeb259c189f1'], 'shared_reinforcement': ['N4'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-510d0f5b70ba0f1068927ed9', 'occ-5fd1e24fb6937e2a8346fa9b'], 'shared_reinforcement': ['N4'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-510d0f5b70ba0f1068927ed9', 'occ-6331d11b266b92dd1bb92218'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-510d0f5b70ba0f1068927ed9', 'occ-9479200e474a74f6186c7fef'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-510d0f5b70ba0f1068927ed9', 'occ-960805dc00137e94f98d5f9e'], 'shared_reinforcement': ['N4'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-510d0f5b70ba0f1068927ed9', 'occ-9d7d081755d9e97429eaedc4'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-510d0f5b70ba0f1068927ed9', 'occ-b0abbbd32d2a2f1c0944bb02'], 'shared_reinforcement': ['N4'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-510d0f5b70ba0f1068927ed9', 'occ-be97625f8475bec7aab9403e'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-510d0f5b70ba0f1068927ed9', 'occ-c194a577e11c55630b4b259e'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-510d0f5b70ba0f1068927ed9', 'occ-c3d40806e6ee36f42226f783'], 'shared_reinforcement': ['N4'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-510d0f5b70ba0f1068927ed9', 'occ-db336c0402fdae7b31d7b92a'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-510d0f5b70ba0f1068927ed9', 'occ-e530d8e9fbb9adbd1ccc99a4'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-510d0f5b70ba0f1068927ed9', 'occ-efd4a93fa316e85799dbdad9'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-510d0f5b70ba0f1068927ed9', 'occ-ff5f08c34c05aeb259c189f1'], 'shared_reinforcement': ['N4'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-5fd1e24fb6937e2a8346fa9b', 'occ-960805dc00137e94f98d5f9e'], 'shared_reinforcement': ['N4'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-5fd1e24fb6937e2a8346fa9b', 'occ-b0abbbd32d2a2f1c0944bb02'], 'shared_reinforcement': ['N4'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-5fd1e24fb6937e2a8346fa9b', 'occ-c3d40806e6ee36f42226f783'], 'shared_reinforcement': ['N4'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-5fd1e24fb6937e2a8346fa9b', 'occ-ff5f08c34c05aeb259c189f1'], 'shared_reinforcement': ['N4'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-6331d11b266b92dd1bb92218', 'occ-9479200e474a74f6186c7fef'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-6331d11b266b92dd1bb92218', 'occ-9d7d081755d9e97429eaedc4'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-6331d11b266b92dd1bb92218', 'occ-be97625f8475bec7aab9403e'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-6331d11b266b92dd1bb92218', 'occ-c194a577e11c55630b4b259e'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-6331d11b266b92dd1bb92218', 'occ-db336c0402fdae7b31d7b92a'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-6331d11b266b92dd1bb92218', 'occ-e530d8e9fbb9adbd1ccc99a4'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-6331d11b266b92dd1bb92218', 'occ-efd4a93fa316e85799dbdad9'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-9479200e474a74f6186c7fef', 'occ-9d7d081755d9e97429eaedc4'], 'shared_reinforcement': ['N7'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-9479200e474a74f6186c7fef', 'occ-be97625f8475bec7aab9403e'], 'shared_reinforcement': ['N7'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-9479200e474a74f6186c7fef', 'occ-c194a577e11c55630b4b259e'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-9479200e474a74f6186c7fef', 'occ-db336c0402fdae7b31d7b92a'], 'shared_reinforcement': ['N7'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-9479200e474a74f6186c7fef', 'occ-e530d8e9fbb9adbd1ccc99a4'], 'shared_reinforcement': ['N7'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-9479200e474a74f6186c7fef', 'occ-efd4a93fa316e85799dbdad9'], 'shared_reinforcement': ['N7'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-960805dc00137e94f98d5f9e', 'occ-b0abbbd32d2a2f1c0944bb02'], 'shared_reinforcement': ['N4'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-960805dc00137e94f98d5f9e', 'occ-c3d40806e6ee36f42226f783'], 'shared_reinforcement': ['N4'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-960805dc00137e94f98d5f9e', 'occ-ff5f08c34c05aeb259c189f1'], 'shared_reinforcement': ['N4'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-9d7d081755d9e97429eaedc4', 'occ-be97625f8475bec7aab9403e'], 'shared_reinforcement': ['N7'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-9d7d081755d9e97429eaedc4', 'occ-c194a577e11c55630b4b259e'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-9d7d081755d9e97429eaedc4', 'occ-db336c0402fdae7b31d7b92a'], 'shared_reinforcement': ['N7'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-9d7d081755d9e97429eaedc4', 'occ-e530d8e9fbb9adbd1ccc99a4'], 'shared_reinforcement': ['N7'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-9d7d081755d9e97429eaedc4', 'occ-efd4a93fa316e85799dbdad9'], 'shared_reinforcement': ['N7'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-b0abbbd32d2a2f1c0944bb02', 'occ-c3d40806e6ee36f42226f783'], 'shared_reinforcement': ['N4'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-b0abbbd32d2a2f1c0944bb02', 'occ-ff5f08c34c05aeb259c189f1'], 'shared_reinforcement': ['N4'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-be97625f8475bec7aab9403e', 'occ-c194a577e11c55630b4b259e'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-be97625f8475bec7aab9403e', 'occ-db336c0402fdae7b31d7b92a'], 'shared_reinforcement': ['N7'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-be97625f8475bec7aab9403e', 'occ-e530d8e9fbb9adbd1ccc99a4'], 'shared_reinforcement': ['N7'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-be97625f8475bec7aab9403e', 'occ-efd4a93fa316e85799dbdad9'], 'shared_reinforcement': ['N7'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-c194a577e11c55630b4b259e', 'occ-db336c0402fdae7b31d7b92a'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-c194a577e11c55630b4b259e', 'occ-e530d8e9fbb9adbd1ccc99a4'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-c194a577e11c55630b4b259e', 'occ-efd4a93fa316e85799dbdad9'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-c3d40806e6ee36f42226f783', 'occ-ff5f08c34c05aeb259c189f1'], 'shared_reinforcement': ['N4'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-db336c0402fdae7b31d7b92a', 'occ-e530d8e9fbb9adbd1ccc99a4'], 'shared_reinforcement': ['N7'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-db336c0402fdae7b31d7b92a', 'occ-efd4a93fa316e85799dbdad9'], 'shared_reinforcement': ['N7'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-e530d8e9fbb9adbd1ccc99a4', 'occ-efd4a93fa316e85799dbdad9'], 'shared_reinforcement': ['N7'], 'physical_overlap': True, 'single_correction_proven': False}

Estado consolidado: **FAIL**. Falhas, pendências e revisões permanecem separadas no JSON. Aprovação limitada às verificações documentadas; não é declaração de segurança global da estrutura.

Nenhuma correção proposta ou selecionada; selected_solution=null e detailing_optimization=null.
