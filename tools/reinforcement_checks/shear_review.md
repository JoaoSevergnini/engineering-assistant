# Cortante — revisão por regiões

`shear_review.py`: orquestra cálculo público do Concretopy, referência por terços e revisão por intervalo físico desenhado. `shear_diagram.py`: adapta séries Vk ao motor linear existente sem alterar moment_diagram/tqs_shear. Procedimento completo: [referência da Skill](../../.agents/skills/reinforcement-review/references/shear-reinforcement-review.md).

APIs: `concretopy.verificacoes.dimensionar_cortante_viga`, `concretopy.normas.espacamento_max_estribo_vigas_cm`, `Barra`, `calcular_espacamento_equivalente`. SecaoRetangular com d explícito selecionado de centroides existentes; mesmo d/VRd2 para smax. Não há fórmula de resistência/minimum/smax copiada para o assistant. A única correção autorizada no Concretopy foi a comparação de ramo de smax, auditada antes da alteração.

Contratos: select_shear_depth; design_shear; shear_reference_design; check_drawn_region; inverse_shear_capacity; transition_check; review_shear_spans. Entradas auditadas de geometria, materiais, séries características, profundidade e faixas. source obrigatória, ramos explícitos; domínio/gaps respeitados. Saídas independentes, grandezas em kN/cm/cm²/m, todos os governantes e provenance. Terços não condicionam transições do desenho.

Global de cortante: falha comprovada=false; pendência necessária sem falha=null; completo e atendido=true. Prática usual é avaliação independente; não é FAIL normativo automático. Suspensão não avaliada. Sem aprovação global da viga ou solução selecionada.

Caso real: `analises/pranchas/validar_v516_v517_cortante.py`; os dois JSONs de cortante têm esforços individuais e leem os goldens longitudinais sem escrevê-los. N12 não convencional confirmado pelo engenheiro: não presumir dois ramos resistentes. Testes: `test_shear_review.py`, mais suíte completa anterior e Concretopy. Auditoria: `.codex/analises/shear_concretopy_api_audit.md`.

## Correção semântica e cobertura em pilares

`shear_coverage.classify_piece` exclui peças comprovadas de negativa de lajes adjacentes do cortante da viga, preservando geometria/fontes em `excluded_reinforcement`. Peças ambíguas não fornecem cobertura e requerem interpretação. Não há regra por nome de marca.

Fornecer `support_geometry.left/right` com type=COLUMN, type_source, source, axis_m, width_m, left_face_m e right_face_m. Faces existentes devem ser consistentes com largura/eixo. `coverage_reviews` separa TQS_SHEAR_DOMAIN e BEAM_STIRRUP_COVERAGE_DOMAIN; particiona WITHIN_SUPPORT, REQUIRED_BEAM_COVERAGE, UNCOVERED_REQUIRED_REGION e GEOMETRY_INCONCLUSIVE. Sem geometria suficiente, aprovação é null salvo falha já comprovada. Não há fallback silencioso para exigir estribos nos pilares ou dispensá-los fora deles. Esforços/crossings e cálculo resistente não mudam.

Decisões: engineer_confirmed_n12_adjacent_slab_negative_reinforcement_v1 e engineer_confirmed_stirrups_terminate_at_column_faces_v1. Ver referência da Skill para aplicabilidade e limitações.
