# V536 N2: motor inicial de correções

Nenhuma solução selecionada ou aprovada. PDF e dados históricos preservados.

O cenário histórico autorizado de gancho continua auditado. As novas configurações usam gancho_valido=False, sem redução não comprovada. A N2 já possui dobra documental de 58 cm; a candidata prioritária avalia sua geometria e resistência, sem somar o desenvolvimento como ancoragem reta.

| Alternativa | Tipo | Geometria | Estrutura | Resultado | Pendências |
|---|---|---|---|---|---|
| Revisar dobra existente N2 | END_BEND | INCONCLUSIVE | INCONCLUSIVE | INCONCLUSIVE | available_horizontal_cm, available_space, available_vertical_cm, bend_pin_criterion, curved_anchorage_resistance, curved_anchorage_resistance_parameters_and_applicable_criterion, explicit_supported_bend_shape, horizontal_leg_cm, inner_bend_diameter_mm, minimum_horizontal_leg_cm, minimum_inner_diameter_mm, minimum_vertical_leg_cm, node_interferences, position_within_support, straight_leg_criteria, vertical_leg_cm |
| extend_N3_1 | EXTEND_OTHER_BARS | INCONCLUSIVE | FAIL | FAIL | affected_scaling, node_interference_geometry, node_interferences, recheck_scaling_for_modified_longitudinal_configuration |
| extend_N3_2 | EXTEND_OTHER_BARS | INCONCLUSIVE | INCONCLUSIVE | INCONCLUSIVE | affected_scaling, node_interference_geometry, node_interferences, recheck_scaling_for_modified_longitudinal_configuration |
| extend_N3_3 | EXTEND_OTHER_BARS | INCONCLUSIVE | INCONCLUSIVE | INCONCLUSIVE | affected_scaling, node_interference_geometry, node_interferences, recheck_scaling_for_modified_longitudinal_configuration |
| redistribute_2x12.5_2x16 | REDISTRIBUTE_BARS | INCONCLUSIVE | FAIL | FAIL | affected_scaling, node_interference_geometry, node_interferences, recheck_scaling_for_modified_longitudinal_configuration |
| redistribute_2x12.5_3x16 | REDISTRIBUTE_BARS | INCONCLUSIVE | FAIL | FAIL | affected_scaling, node_interference_geometry, node_interferences, recheck_scaling_for_modified_longitudinal_configuration |
| redistribute_3x12.5_2x16 | REDISTRIBUTE_BARS | INCONCLUSIVE | FAIL | FAIL | affected_scaling, node_interference_geometry, node_interferences, recheck_scaling_for_modified_longitudinal_configuration |
| redistribute_3x12.5_3x16 | REDISTRIBUTE_BARS | INCONCLUSIVE | FAIL | FAIL | affected_scaling, node_interference_geometry, node_interferences, recheck_scaling_for_modified_longitudinal_configuration |
| redistribute_2x12.5_2x20 | REDISTRIBUTE_BARS | INCONCLUSIVE | FAIL | FAIL | affected_scaling, node_interference_geometry, node_interferences, recheck_scaling_for_modified_longitudinal_configuration |
| redistribute_2x12.5_3x20 | REDISTRIBUTE_BARS | INCONCLUSIVE | FAIL | FAIL | affected_scaling, node_interference_geometry, node_interferences, recheck_scaling_for_modified_longitudinal_configuration |
| redistribute_3x12.5_2x20 | REDISTRIBUTE_BARS | INCONCLUSIVE | FAIL | FAIL | affected_scaling, node_interference_geometry, node_interferences, recheck_scaling_for_modified_longitudinal_configuration |
| redistribute_3x12.5_3x20 | REDISTRIBUTE_BARS | INCONCLUSIVE | FAIL | FAIL | affected_scaling, node_interference_geometry, node_interferences, recheck_scaling_for_modified_longitudinal_configuration |
| redistribute_2x16_2x20 | REDISTRIBUTE_BARS | INCONCLUSIVE | FAIL | FAIL | affected_scaling, node_interference_geometry, node_interferences, recheck_scaling_for_modified_longitudinal_configuration |
| redistribute_2x16_3x20 | REDISTRIBUTE_BARS | INCONCLUSIVE | FAIL | FAIL | affected_scaling, node_interference_geometry, node_interferences, recheck_scaling_for_modified_longitudinal_configuration |
| redistribute_3x16_2x20 | REDISTRIBUTE_BARS | INCONCLUSIVE | FAIL | FAIL | affected_scaling, node_interference_geometry, node_interferences, recheck_scaling_for_modified_longitudinal_configuration |
| redistribute_3x16_3x20 | REDISTRIBUTE_BARS | INCONCLUSIVE | FAIL | FAIL | affected_scaling, node_interference_geometry, node_interferences, recheck_scaling_for_modified_longitudinal_configuration |

As alternativas secundárias reconstroem camadas e recalculam flexão regional, demanda por pares, d/x/z/al e ancoragem nas APIs existentes. Falhas comprovadas permanecem FAIL mesmo coexistindo pendências. Cabimento elementar não comprova interferências do nó. Escalonamentos afetados permanecem pendentes nesta integração, portanto nenhuma alternativa está pronta para detalhamento.

Comparação sem score: primeiro validade comprovada; depois reaproveitamento, simplicidade, posições alteradas, retrabalho e consumo racional. Prolongamentos reutilizam Ø20; redistribuições alteram duas posições. Nenhuma candidata está comprovadamente válida em todos os controles.

Faltam dimensão transversal e espaço interno comprovado do pilar, diâmetro interno/pino e critério correspondente, trajetória/trechos retos e curvos, interferências e parâmetros resistentes da ancoragem curva. Não se inventaram coordenadas PDF. selected_solution=null; aprovação=PENDING_ENGINEERING_APPROVAL.

## Arquitetura, contrato e validação da implementação

O módulo independente `tools/reinforcement_checks/correction_engine.py` vincula propostas a uma ocorrência comprovada de falha de comprimento de ancoragem. Exige identidade da barra/extremidade e apoio END orientado, com provenance. Geração, geometria, reverificação por callback, comparação e aprovação permanecem etapas separadas. IDs derivam de identidade e conteúdo, sem dependência de ordem. Os dados originais são copiados.

Cada alternativa conserva ocorrência de origem completa, viga/pavimento, marca/extremidade, geometria original/proposta, dimensões alteradas, unidades, verificações afetadas, resultados e auditoria completa, pendências, viabilidades independentes, grau de intervenção e estado de aprovação. A fonte e o hash do diagnóstico e da reverificação original estão no JSON. Referência gráfica permanece null; não há correspondência PDF presumida. Preferências reutilizam detailing_change_contracts; nenhuma aprovação é automática.

O verificador elementar da dobra aceita somente uma trajetória ortogonal de 90 graus explicitamente informada, com limites geométricos e critérios de pino/pernas fornecidos e rastreáveis. Não dimensiona o pino nem inventa critério normativo. Comprimento desenvolvido é somente geometria. Posição real no apoio e interferências exigem comprovação independente. Resistência curva exige verificação específica: o fator histórico favorável não substitui essa comprovação.

Arquivos criados: correction_engine.py, correction_engine.md, test_correction_engine.py, validar_v536_correction_engine.py, V536_N2_correction_engine.json, este relatório e correction_engine_preservation.json. README das verificações foi atualizado. Infraestruturas existentes support_alternatives, support_correction, diagramas e Concretopy foram reutilizadas sem alteração.

A busca real usou três prolongamentos de N3 e redistribuições com série [12,5;16;20] mm, quantidades [2;3] por camada e diferença máxima de dois passos. Esses limites são escolhas explícitas do ensaio, não normativos. Para cada secundária foram reconstruídas camadas e recalculados os resultados das APIs existentes. A inclusão de nova posição e alterações isoladas de bitola/quantidade são tipos suportados pelo contrato para candidatos explícitos do chamador; não há geração arbitrária dessas geometrias nesta primeira versão.

22 testes novos aprovados: envelope viável/inviável, geometria ausente, curva inconclusiva, interferência, desenvolvimento sem crédito resistente, pino, fontes, identidade, determinismo/imutabilidade, extensão sem ganho, tipos secundários, chamadas independentes, controles afetados, ausência de aprovação automática, escopo END, fonte histórica preservada e ausência de IO PDF.

Suíte final engineering-assistant: 1.057 testes aprovados (39 extrator, 30 modelo, 57 mapeamento, 931 verificações). Concretopy: 427 aprovados, sem alteração nesta tarefa. quick_validate: Skill válida. git diff --check aprovado nos dois repositórios, com avisos de LF/CRLF sem erro. Auditoria SHA-256 preservou 188 arquivos históricos/Concretopy; testes adicionais confirmaram os hashes das fontes do diagnóstico atualizado.

Resultado: 16 candidatas, 13 FAIL e 3 INCONCLUSIVE, nenhum PASS completo. A dobra e os prolongamentos de duas/três barras N3 são os três inconclusivos; prolongar uma barra e as doze redistribuições possuem falhas comprovadas. Isso não altera o resultado do prolongamento de uma barra no cenário histórico com gancho autorizado: os cenários têm premissas diferentes, explicitadas no JSON.

Próximos dados necessários: dimensões internas/transversais do pilar, comprovação da trajetória e posição da dobra, critério e diâmetro do pino, pernas retas, confinamento/interferências, condições resistentes da ancoragem curva. Mudanças longitudinais exigem concluir os escalonamentos afetados. Até lá, nenhuma candidata está aprovada nem pronta para detalhamento. Nenhum desenho foi alterado e nenhuma solução foi selecionada.
