# Diagnóstico consolidado — V516

Pavimento: DIFERENCIADO.

Contexto e fontes: {'beam_id': 'V516', 'floor': 'DIFERENCIADO', 'floor_source': {'project_directory': 'C:\\TQS\\24-155-COLLINE-RESIDENCIAL-R60\\DIFERENCIADO\\VIGAS'}, 'coordinate_system': {'origin': 'left_support_axis', 'positive_direction': 'left_to_right', 'unit': 'm'}, 'geometry': [{'id': 1, 'geometry': {'length': 2.08, 'width': 0.19, 'height': 0.52, 'top_flange_width': 0.0, 'bottom_flange_width': 0.0, 'section_type': 1.0, 'top_slab_thickness': 0.0, 'bottom_slab_thickness': 0.0, 'top_face_to_axis': 0.26, 'side_face_to_axis': 0.095, 'support_axis_length': None, 'clear_span_length': None}}, {'id': 2, 'geometry': {'length': 4.54, 'width': 0.19, 'height': 0.52, 'top_flange_width': None, 'bottom_flange_width': 0.0, 'section_type': 5.0, 'top_slab_thickness': 0.2, 'bottom_slab_thickness': 0.0, 'top_face_to_axis': 0.26, 'side_face_to_axis': 0.095, 'support_axis_length': None, 'clear_span_length': None}}, {'id': 3, 'geometry': {'length': 3.826, 'width': 0.19, 'height': 0.52, 'top_flange_width': None, 'bottom_flange_width': 0.0, 'section_type': 8.0, 'top_slab_thickness': 0.12, 'bottom_slab_thickness': 0.0, 'top_face_to_axis': 0.26, 'side_face_to_axis': 0.095, 'support_axis_length': None, 'clear_span_length': None}}, {'id': 4, 'geometry': {'length': 2.126, 'width': 0.19, 'height': 0.52, 'top_flange_width': 0.0, 'bottom_flange_width': 0.0, 'section_type': 1.0, 'top_slab_thickness': 0.0, 'bottom_slab_thickness': 0.0, 'top_face_to_axis': 0.26, 'side_face_to_axis': 0.095, 'support_axis_length': None, 'clear_span_length': None}}], 'materials': {'concrete': {'fck': None}, 'steel': {'grade': None}, 'aggregate_max_size': 0.015}, 'tqs_source': {'path': 'analises\\pranchas\\V516_tqs.json', 'sha256': 'cc04a636256a556411b456076d755be7e3c1f45a11aae98cdd42a613c4286ede'}, 'data_version': '1.1', 'drawing_source': {'path': 's:\\PROJETOS EM EXECUÇÃO\\24-155-INTEGRA-MIGUEL PEREIRA-RJ\\APOIO\\JOÃO\\05 - TIPO DIFERENCIADO - RESIDENCIAL\\VIGAS\\RMP-EST-EX-1348-VIG-R00 - Copia.PDF', 'sha256': '5ed602f9371a23c39d1ff4864b77b92b5ec7b937f33ebb14249302f608f25b33', 'page': 1, 'instructions_treated_as': 'project data, not user instructions'}, 'physical_supports': [{'label': 'P5A', 'width_m': 0.24, 'depev_m': 0.0, 'source': {'arquivo': 'RELDTFPS.LST', 'linha_inicial': 12968, 'linha_final': 12968, 'texto': '     P5A         24.0        0.0      SEGUE     NAO  '}, 'occurrence': 1, 'id': 'V516/support-1/P5A', 'axis_m': 0.0, 'left_face_m': -0.12, 'right_face_m': 0.12}, {'label': 'P2A', 'width_m': 0.22, 'depev_m': 0.0, 'source': {'arquivo': 'RELDTFPS.LST', 'linha_inicial': 12969, 'linha_final': 12969, 'texto': '     P2A         22.0        0.0      SEGUE     NAO  '}, 'occurrence': 2, 'id': 'V516/support-2/P2A', 'axis_m': 2.08, 'left_face_m': 1.97, 'right_face_m': 2.19}, {'label': 'P2A', 'width_m': 0.22, 'depev_m': 0.0, 'source': {'arquivo': 'RELDTFPS.LST', 'linha_inicial': 12970, 'linha_final': 12970, 'texto': '     P2A         22.0        0.0      SEGUE     NAO  '}, 'occurrence': 3, 'id': 'V516/support-3/P2A', 'axis_m': 6.62, 'left_face_m': 6.51, 'right_face_m': 6.73}, {'label': 'P1A', 'width_m': 1.42, 'depev_m': 0.554, 'source': {'arquivo': 'RELDTFPS.LST', 'linha_inicial': 12971, 'linha_final': 12971, 'texto': '     P1A        142.0       55.4      SEGUE     NAO  '}, 'occurrence': 4, 'id': 'V516/support-4/P1A', 'axis_m': 11.0, 'left_face_m': 10.29, 'right_face_m': 11.71}, {'label': 'P6A', 'width_m': 0.24, 'depev_m': 0.0, 'source': {'arquivo': 'RELDTFPS.LST', 'linha_inicial': 12972, 'linha_final': 12972, 'texto': '     P6A         24.0        0.0      SEGUE     NAO  '}, 'occurrence': 5, 'id': 'V516/support-5/P6A', 'axis_m': 13.68, 'left_face_m': 13.56, 'right_face_m': 13.8}]}

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
| occ-314d6ae7f08b124fb5e30202 | straight_anchorage_geometry | FAIL (observação de modo) | [4, [13.56, 13.8]] | ['N7'] | não documentado | não documentado | não documentado | ['A bent-bar projection is not a verified straight anchorage', []] |
| occ-69ffe16b7f821069c42fe592 | straight_anchorage_geometry | FAIL (observação de modo) | [1, [-0.12, 0.12]] | ['N4'] | não documentado | não documentado | não documentado | ['A bent-bar projection is not a verified straight anchorage', []] |
| occ-786245a7c0b220008124775d | vertical_bend_geometry | FAIL | [1, [-0.12, 0.12]] | ['N4'] | 48.7 | 40 | cm | ['engineer_confirmed_negative_end_support_vertical_bend_v1', []] |
| occ-8a762d444ee8f471631649fe | al_plus_lb | FAIL | [2, [5.83, 5.83]] | ['N8'] | 126.67384157702772 | 79.0 | cm | ['engineer_confirmed_negative_al_same_as_positive_v1', []] |
| occ-9a2176b059a99c9a176fa784 | flexural_capacity | FAIL | [3, [9.16, 10.446]] | ['N7', 'N8', 'N9'] | 168.9881928 | 160.31741548190314 | kN.m | ['original regional capacity comparison', []] |
| occ-fa2b77bd12e1ba4b37802787 | vertical_bend_geometry | FAIL | [4, [13.56, 13.8]] | ['N7'] | 48.7 | 45 | cm | ['engineer_confirmed_negative_end_support_vertical_bend_v1', []] |

## Pendências e revisão de engenharia

| ID | Controle | Estado | Vão / intervalo | Armadura | Necessário | Fornecido | Unidade | Motivo / pendência |
|---|---|---|---|---|---|---|---|---|
| occ-0b222b35b00b1f4f59331b36 | vibrator_access_spacing | INCONCLUSIVE | [3, None] | ['N7', 'N7'] | não documentado | não documentado | não documentado | [None, ['original check unresolved', 'physical_location_not_documented']] |
| occ-0b82ea375c0ed3ff95cc04ca | minimum_bar_spacing | INCONCLUSIVE | [4, [13.56, 13.8]] | ['N7'] | não documentado | não documentado | não documentado | ['documentary_transverse_centers_missing', ['documentary_transverse_centers_missing']] |
| occ-185f4eae3a147b9f29d3a9fa | vibrator_access_spacing | INCONCLUSIVE | [4, [13.56, 13.8]] | ['N7'] | não documentado | não documentado | não documentado | ['documentary_transverse_centers_missing', ['documentary_transverse_centers_missing']] |
| occ-2036f2e3c258f94ff137eac2 | module_coverage | INCONCLUSIVE | [None, None] | [] | não documentado | não documentado | não documentado | ['module_scope_incomplete', ['applicable checks not completely documented', 'physical_location_not_documented']] |
| occ-2047821b6eb393b53ecae18c | module_coverage | INCONCLUSIVE | [None, None] | [] | não documentado | não documentado | não documentado | ['module_scope_incomplete', ['applicable checks not completely documented', 'physical_location_not_documented']] |
| occ-26bac0893b09c5f3d622d9ee | suspension_inventory | INCONCLUSIVE | [None, None] | [] | não documentado | não documentado | não documentado | ['suspension inventory incomplete', ['suspension inventory incomplete', 'physical_location_not_documented']] |
| occ-2c76484f4ec4c49ff80c36bb | local_spacing_geometry | INCONCLUSIVE | [3, None] | ['N7', 'N7'] | não documentado | não documentado | não documentado | [None, ['original check unresolved', 'physical_location_not_documented']] |
| occ-2da070165b60f7e147411881 | module_coverage | INCONCLUSIVE | [None, None] | [] | não documentado | não documentado | não documentado | ['module_scope_incomplete', ['applicable checks not completely documented', 'physical_location_not_documented']] |
| occ-2edf8f1dd2a8f290b8dffedb | vibrator_access_spacing | INCONCLUSIVE | [1, [-0.12, 0.12]] | ['N4'] | não documentado | não documentado | não documentado | ['documentary_transverse_centers_missing', ['documentary_transverse_centers_missing']] |
| occ-3168920856b004dc78992357 | minimum_bar_spacing | INCONCLUSIVE | [1, [-0.12, 0.12]] | ['N4'] | não documentado | não documentado | não documentado | ['documentary_transverse_centers_missing', ['documentary_transverse_centers_missing']] |
| occ-3d2c8765b2b54b0f5bad2990 | column_interference_spacing | INCONCLUSIVE | [1, [-0.12, 0.12]] | ['N4'] | não documentado | não documentado | não documentado | ['column_perpendicular_dimension_missing', ['column_perpendicular_dimension_missing']] |
| occ-3dc6614de9704988e84e18cf | module_availability | INCONCLUSIVE | [None, None] | [] | não documentado | não documentado | não documentado | ['module_not_executed', ['module results unavailable']] |
| occ-3fa58bcdcdfea30d97236678 | local_spacing_geometry | INCONCLUSIVE | [2, None] | ['N4', 'N7'] | não documentado | não documentado | não documentado | [None, ['original check unresolved', 'physical_location_not_documented']] |
| occ-44e7c6686bf0e88aa3bf6a04 | flexural_capacity | INCONCLUSIVE | [2, [3.67, 5.015]] | ['N4', 'N7'] | não documentado | não documentado | não documentado | [['resistant_positions_not_defined_for_tail_overlap'], [['resistant_positions_not_defined_for_tail_overlap']]] |
| occ-62c58e423a0b78cbba6403f5 | module_coverage | INCONCLUSIVE | [None, None] | [] | não documentado | não documentado | não documentado | ['module_scope_incomplete', ['applicable checks not completely documented', 'physical_location_not_documented']] |
| occ-99e06c5594a3fa1f10f07a81 | curved_anchorage_resistance | INCONCLUSIVE | [1, [-0.12, 0.12]] | ['N4'] | não documentado | não documentado | não documentado | ['Curved anchorage resistance, pin/radius and node confinement not represented; no alpha=0.7 credit', ['Curved anchorage resistance, pin/radius and node confinement not represented; no alpha=0.7 credit']] |
| occ-b1f56dd8f3851dd7ecad8cce | curved_anchorage_resistance | INCONCLUSIVE | [4, [13.56, 13.8]] | ['N7'] | não documentado | não documentado | não documentado | ['Curved anchorage resistance, pin/radius and node confinement not represented; no alpha=0.7 credit', ['Curved anchorage resistance, pin/radius and node confinement not represented; no alpha=0.7 credit']] |
| occ-b2ea77eeb3b4a35724195f0d | vibrator_access_spacing | INCONCLUSIVE | [2, None] | ['N4', 'N7'] | não documentado | não documentado | não documentado | ['documentary_transverse_centers_missing', ['documentary_transverse_centers_missing', 'physical_location_not_documented']] |
| occ-ba5736a3c2a655ef4511254d | drawing_coverage | INCONCLUSIVE | [1, [0.12, 1.97]] | [] | não documentado | não documentado | não documentado | ['UNCOVERED_REQUIRED_REGION', ['UNCOVERED_REQUIRED_REGION']] |
| occ-c6433478a4bcbc0a9df58a1c | drawing_coverage | INCONCLUSIVE | [4, [11.71, 13.56]] | [] | não documentado | não documentado | não documentado | ['UNCOVERED_REQUIRED_REGION', ['UNCOVERED_REQUIRED_REGION']] |
| occ-e32333415a1f096c62acf5fe | flexural_capacity | INCONCLUSIVE | [2, [3.635, 3.67]] | ['N4', 'N3', 'N7'] | não documentado | não documentado | não documentado | [['resistant_positions_not_defined_for_tail_overlap'], [['resistant_positions_not_defined_for_tail_overlap']]] |
| occ-febde9bcf9230a7b9d59e289 | column_interference_spacing | INCONCLUSIVE | [4, [13.56, 13.8]] | ['N7'] | não documentado | não documentado | não documentado | ['column_perpendicular_dimension_missing', ['column_perpendicular_dimension_missing']] |

## Relações entre ocorrências

{'occurrences': ['occ-0b222b35b00b1f4f59331b36', 'occ-0b82ea375c0ed3ff95cc04ca'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-0b222b35b00b1f4f59331b36', 'occ-185f4eae3a147b9f29d3a9fa'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-0b222b35b00b1f4f59331b36', 'occ-2c76484f4ec4c49ff80c36bb'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-0b222b35b00b1f4f59331b36', 'occ-314d6ae7f08b124fb5e30202'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-0b222b35b00b1f4f59331b36', 'occ-3fa58bcdcdfea30d97236678'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-0b222b35b00b1f4f59331b36', 'occ-44e7c6686bf0e88aa3bf6a04'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-0b222b35b00b1f4f59331b36', 'occ-9a2176b059a99c9a176fa784'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-0b222b35b00b1f4f59331b36', 'occ-b1f56dd8f3851dd7ecad8cce'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-0b222b35b00b1f4f59331b36', 'occ-b2ea77eeb3b4a35724195f0d'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-0b222b35b00b1f4f59331b36', 'occ-e32333415a1f096c62acf5fe'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-0b222b35b00b1f4f59331b36', 'occ-fa2b77bd12e1ba4b37802787'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-0b222b35b00b1f4f59331b36', 'occ-febde9bcf9230a7b9d59e289'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-0b82ea375c0ed3ff95cc04ca', 'occ-185f4eae3a147b9f29d3a9fa'], 'shared_reinforcement': ['N7'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-0b82ea375c0ed3ff95cc04ca', 'occ-2c76484f4ec4c49ff80c36bb'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-0b82ea375c0ed3ff95cc04ca', 'occ-314d6ae7f08b124fb5e30202'], 'shared_reinforcement': ['N7'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-0b82ea375c0ed3ff95cc04ca', 'occ-3fa58bcdcdfea30d97236678'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-0b82ea375c0ed3ff95cc04ca', 'occ-44e7c6686bf0e88aa3bf6a04'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-0b82ea375c0ed3ff95cc04ca', 'occ-9a2176b059a99c9a176fa784'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-0b82ea375c0ed3ff95cc04ca', 'occ-b1f56dd8f3851dd7ecad8cce'], 'shared_reinforcement': ['N7'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-0b82ea375c0ed3ff95cc04ca', 'occ-b2ea77eeb3b4a35724195f0d'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-0b82ea375c0ed3ff95cc04ca', 'occ-e32333415a1f096c62acf5fe'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-0b82ea375c0ed3ff95cc04ca', 'occ-fa2b77bd12e1ba4b37802787'], 'shared_reinforcement': ['N7'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-0b82ea375c0ed3ff95cc04ca', 'occ-febde9bcf9230a7b9d59e289'], 'shared_reinforcement': ['N7'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-185f4eae3a147b9f29d3a9fa', 'occ-2c76484f4ec4c49ff80c36bb'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-185f4eae3a147b9f29d3a9fa', 'occ-314d6ae7f08b124fb5e30202'], 'shared_reinforcement': ['N7'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-185f4eae3a147b9f29d3a9fa', 'occ-3fa58bcdcdfea30d97236678'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-185f4eae3a147b9f29d3a9fa', 'occ-44e7c6686bf0e88aa3bf6a04'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-185f4eae3a147b9f29d3a9fa', 'occ-9a2176b059a99c9a176fa784'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-185f4eae3a147b9f29d3a9fa', 'occ-b1f56dd8f3851dd7ecad8cce'], 'shared_reinforcement': ['N7'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-185f4eae3a147b9f29d3a9fa', 'occ-b2ea77eeb3b4a35724195f0d'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-185f4eae3a147b9f29d3a9fa', 'occ-e32333415a1f096c62acf5fe'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-185f4eae3a147b9f29d3a9fa', 'occ-fa2b77bd12e1ba4b37802787'], 'shared_reinforcement': ['N7'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-185f4eae3a147b9f29d3a9fa', 'occ-febde9bcf9230a7b9d59e289'], 'shared_reinforcement': ['N7'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-2c76484f4ec4c49ff80c36bb', 'occ-314d6ae7f08b124fb5e30202'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-2c76484f4ec4c49ff80c36bb', 'occ-3fa58bcdcdfea30d97236678'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-2c76484f4ec4c49ff80c36bb', 'occ-44e7c6686bf0e88aa3bf6a04'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-2c76484f4ec4c49ff80c36bb', 'occ-9a2176b059a99c9a176fa784'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-2c76484f4ec4c49ff80c36bb', 'occ-b1f56dd8f3851dd7ecad8cce'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-2c76484f4ec4c49ff80c36bb', 'occ-b2ea77eeb3b4a35724195f0d'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-2c76484f4ec4c49ff80c36bb', 'occ-e32333415a1f096c62acf5fe'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-2c76484f4ec4c49ff80c36bb', 'occ-fa2b77bd12e1ba4b37802787'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-2c76484f4ec4c49ff80c36bb', 'occ-febde9bcf9230a7b9d59e289'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-2edf8f1dd2a8f290b8dffedb', 'occ-3168920856b004dc78992357'], 'shared_reinforcement': ['N4'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-2edf8f1dd2a8f290b8dffedb', 'occ-3d2c8765b2b54b0f5bad2990'], 'shared_reinforcement': ['N4'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-2edf8f1dd2a8f290b8dffedb', 'occ-3fa58bcdcdfea30d97236678'], 'shared_reinforcement': ['N4'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-2edf8f1dd2a8f290b8dffedb', 'occ-44e7c6686bf0e88aa3bf6a04'], 'shared_reinforcement': ['N4'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-2edf8f1dd2a8f290b8dffedb', 'occ-69ffe16b7f821069c42fe592'], 'shared_reinforcement': ['N4'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-2edf8f1dd2a8f290b8dffedb', 'occ-786245a7c0b220008124775d'], 'shared_reinforcement': ['N4'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-2edf8f1dd2a8f290b8dffedb', 'occ-99e06c5594a3fa1f10f07a81'], 'shared_reinforcement': ['N4'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-2edf8f1dd2a8f290b8dffedb', 'occ-b2ea77eeb3b4a35724195f0d'], 'shared_reinforcement': ['N4'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-2edf8f1dd2a8f290b8dffedb', 'occ-e32333415a1f096c62acf5fe'], 'shared_reinforcement': ['N4'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-314d6ae7f08b124fb5e30202', 'occ-3fa58bcdcdfea30d97236678'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-314d6ae7f08b124fb5e30202', 'occ-44e7c6686bf0e88aa3bf6a04'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-314d6ae7f08b124fb5e30202', 'occ-9a2176b059a99c9a176fa784'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-314d6ae7f08b124fb5e30202', 'occ-b1f56dd8f3851dd7ecad8cce'], 'shared_reinforcement': ['N7'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-314d6ae7f08b124fb5e30202', 'occ-b2ea77eeb3b4a35724195f0d'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-314d6ae7f08b124fb5e30202', 'occ-e32333415a1f096c62acf5fe'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-314d6ae7f08b124fb5e30202', 'occ-fa2b77bd12e1ba4b37802787'], 'shared_reinforcement': ['N7'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-314d6ae7f08b124fb5e30202', 'occ-febde9bcf9230a7b9d59e289'], 'shared_reinforcement': ['N7'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-3168920856b004dc78992357', 'occ-3d2c8765b2b54b0f5bad2990'], 'shared_reinforcement': ['N4'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-3168920856b004dc78992357', 'occ-3fa58bcdcdfea30d97236678'], 'shared_reinforcement': ['N4'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-3168920856b004dc78992357', 'occ-44e7c6686bf0e88aa3bf6a04'], 'shared_reinforcement': ['N4'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-3168920856b004dc78992357', 'occ-69ffe16b7f821069c42fe592'], 'shared_reinforcement': ['N4'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-3168920856b004dc78992357', 'occ-786245a7c0b220008124775d'], 'shared_reinforcement': ['N4'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-3168920856b004dc78992357', 'occ-99e06c5594a3fa1f10f07a81'], 'shared_reinforcement': ['N4'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-3168920856b004dc78992357', 'occ-b2ea77eeb3b4a35724195f0d'], 'shared_reinforcement': ['N4'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-3168920856b004dc78992357', 'occ-e32333415a1f096c62acf5fe'], 'shared_reinforcement': ['N4'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-3d2c8765b2b54b0f5bad2990', 'occ-3fa58bcdcdfea30d97236678'], 'shared_reinforcement': ['N4'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-3d2c8765b2b54b0f5bad2990', 'occ-44e7c6686bf0e88aa3bf6a04'], 'shared_reinforcement': ['N4'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-3d2c8765b2b54b0f5bad2990', 'occ-69ffe16b7f821069c42fe592'], 'shared_reinforcement': ['N4'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-3d2c8765b2b54b0f5bad2990', 'occ-786245a7c0b220008124775d'], 'shared_reinforcement': ['N4'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-3d2c8765b2b54b0f5bad2990', 'occ-99e06c5594a3fa1f10f07a81'], 'shared_reinforcement': ['N4'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-3d2c8765b2b54b0f5bad2990', 'occ-b2ea77eeb3b4a35724195f0d'], 'shared_reinforcement': ['N4'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-3d2c8765b2b54b0f5bad2990', 'occ-e32333415a1f096c62acf5fe'], 'shared_reinforcement': ['N4'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-3fa58bcdcdfea30d97236678', 'occ-44e7c6686bf0e88aa3bf6a04'], 'shared_reinforcement': ['N4', 'N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-3fa58bcdcdfea30d97236678', 'occ-69ffe16b7f821069c42fe592'], 'shared_reinforcement': ['N4'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-3fa58bcdcdfea30d97236678', 'occ-786245a7c0b220008124775d'], 'shared_reinforcement': ['N4'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-3fa58bcdcdfea30d97236678', 'occ-99e06c5594a3fa1f10f07a81'], 'shared_reinforcement': ['N4'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-3fa58bcdcdfea30d97236678', 'occ-9a2176b059a99c9a176fa784'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-3fa58bcdcdfea30d97236678', 'occ-b1f56dd8f3851dd7ecad8cce'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-3fa58bcdcdfea30d97236678', 'occ-b2ea77eeb3b4a35724195f0d'], 'shared_reinforcement': ['N4', 'N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-3fa58bcdcdfea30d97236678', 'occ-e32333415a1f096c62acf5fe'], 'shared_reinforcement': ['N4', 'N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-3fa58bcdcdfea30d97236678', 'occ-fa2b77bd12e1ba4b37802787'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-3fa58bcdcdfea30d97236678', 'occ-febde9bcf9230a7b9d59e289'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-44e7c6686bf0e88aa3bf6a04', 'occ-69ffe16b7f821069c42fe592'], 'shared_reinforcement': ['N4'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-44e7c6686bf0e88aa3bf6a04', 'occ-786245a7c0b220008124775d'], 'shared_reinforcement': ['N4'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-44e7c6686bf0e88aa3bf6a04', 'occ-99e06c5594a3fa1f10f07a81'], 'shared_reinforcement': ['N4'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-44e7c6686bf0e88aa3bf6a04', 'occ-9a2176b059a99c9a176fa784'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-44e7c6686bf0e88aa3bf6a04', 'occ-b1f56dd8f3851dd7ecad8cce'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-44e7c6686bf0e88aa3bf6a04', 'occ-b2ea77eeb3b4a35724195f0d'], 'shared_reinforcement': ['N4', 'N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-44e7c6686bf0e88aa3bf6a04', 'occ-e32333415a1f096c62acf5fe'], 'shared_reinforcement': ['N4', 'N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-44e7c6686bf0e88aa3bf6a04', 'occ-fa2b77bd12e1ba4b37802787'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-44e7c6686bf0e88aa3bf6a04', 'occ-febde9bcf9230a7b9d59e289'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-69ffe16b7f821069c42fe592', 'occ-786245a7c0b220008124775d'], 'shared_reinforcement': ['N4'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-69ffe16b7f821069c42fe592', 'occ-99e06c5594a3fa1f10f07a81'], 'shared_reinforcement': ['N4'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-69ffe16b7f821069c42fe592', 'occ-b2ea77eeb3b4a35724195f0d'], 'shared_reinforcement': ['N4'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-69ffe16b7f821069c42fe592', 'occ-e32333415a1f096c62acf5fe'], 'shared_reinforcement': ['N4'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-786245a7c0b220008124775d', 'occ-99e06c5594a3fa1f10f07a81'], 'shared_reinforcement': ['N4'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-786245a7c0b220008124775d', 'occ-b2ea77eeb3b4a35724195f0d'], 'shared_reinforcement': ['N4'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-786245a7c0b220008124775d', 'occ-e32333415a1f096c62acf5fe'], 'shared_reinforcement': ['N4'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-8a762d444ee8f471631649fe', 'occ-9a2176b059a99c9a176fa784'], 'shared_reinforcement': ['N8'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-99e06c5594a3fa1f10f07a81', 'occ-b2ea77eeb3b4a35724195f0d'], 'shared_reinforcement': ['N4'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-99e06c5594a3fa1f10f07a81', 'occ-e32333415a1f096c62acf5fe'], 'shared_reinforcement': ['N4'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-9a2176b059a99c9a176fa784', 'occ-b1f56dd8f3851dd7ecad8cce'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-9a2176b059a99c9a176fa784', 'occ-b2ea77eeb3b4a35724195f0d'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-9a2176b059a99c9a176fa784', 'occ-e32333415a1f096c62acf5fe'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-9a2176b059a99c9a176fa784', 'occ-fa2b77bd12e1ba4b37802787'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-9a2176b059a99c9a176fa784', 'occ-febde9bcf9230a7b9d59e289'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-b1f56dd8f3851dd7ecad8cce', 'occ-b2ea77eeb3b4a35724195f0d'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-b1f56dd8f3851dd7ecad8cce', 'occ-e32333415a1f096c62acf5fe'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-b1f56dd8f3851dd7ecad8cce', 'occ-fa2b77bd12e1ba4b37802787'], 'shared_reinforcement': ['N7'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-b1f56dd8f3851dd7ecad8cce', 'occ-febde9bcf9230a7b9d59e289'], 'shared_reinforcement': ['N7'], 'physical_overlap': True, 'single_correction_proven': False}
{'occurrences': ['occ-b2ea77eeb3b4a35724195f0d', 'occ-e32333415a1f096c62acf5fe'], 'shared_reinforcement': ['N4', 'N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-b2ea77eeb3b4a35724195f0d', 'occ-fa2b77bd12e1ba4b37802787'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-b2ea77eeb3b4a35724195f0d', 'occ-febde9bcf9230a7b9d59e289'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-e32333415a1f096c62acf5fe', 'occ-fa2b77bd12e1ba4b37802787'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-e32333415a1f096c62acf5fe', 'occ-febde9bcf9230a7b9d59e289'], 'shared_reinforcement': ['N7'], 'physical_overlap': False, 'single_correction_proven': False}
{'occurrences': ['occ-fa2b77bd12e1ba4b37802787', 'occ-febde9bcf9230a7b9d59e289'], 'shared_reinforcement': ['N7'], 'physical_overlap': True, 'single_correction_proven': False}

Estado consolidado: **FAIL**. Falhas, pendências e revisões permanecem separadas no JSON. Aprovação limitada às verificações documentadas; não é declaração de segurança global da estrutura.

Nenhuma correção proposta ou selecionada; selected_solution=null e detailing_optimization=null.
