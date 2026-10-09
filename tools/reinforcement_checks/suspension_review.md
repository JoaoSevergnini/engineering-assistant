# Contrato de suspensão

API `review_suspension(connections, receiving_beam=..., spans=..., context=..., api=..., inventory_complete=False, inventory_source=None)`; `review_connection` verifica uma ligação. Módulo independente de `review_shear_spans`, sem mutação dos parâmetros ou resultados de cortante.

Entrada connection: id, type=BEAM_ON_BEAM, supported_beam_id, receiving_beam_id, transfer_confirmed/source, suspension_applicable/applicability_source, supported_geometry(height_cm,width_cm,source); placement=INTERIOR e projected_axis_m/axis_source ou CANTILEVER_END e explicit_interval_m/explicit_interval_source; reaction(value,unit=kN,nature=CHARACTERISTIC|DESIGN,is_total,total_source,combination,source,downward_sign=±1,supported_beam_id,receiving_beam_id). downward_sign transforma a observação assinada na reação descendente sobre a receptora; não é abs automático. Uplift não formalizado permanece inconclusivo.

Spans/context: reutilizar contratos de shear_review; spans incluem séries TQS, faixas documentais e support_geometry das faces comprovadas. Domínio especial pode ser explicit_physical_beam_domain_m com explicit_physical_domain_source. section_changes_m identifica limites não atravessáveis automaticamente. Modelo é o existente de cortante vertical sem solicitação axial.

Resultado: controles independentes, reação original/considerada, área total, distribuição física, quatro taxas, máximos assinados/governantes, subintervalos por faixa, fontes e chamadas; suspensão_passes triestado e overall_result (incluindo REVIEW). selected_solution/detailing_optimization null. Overlaps de suspensão não combinados. Campos opcionais da API Concretopy ausentes geram INCONCLUSIVE.

[Procedimento e regras confirmadas](../../.agents/skills/reinforcement-review/references/suspension-reinforcement-review.md). Unidade de x em m; h/L em cm; forças kN; tensão MPa convertida em kN/cm²; áreas cm² e taxas cm²/m. `connections_from_mapping` descobre candidatos documentais de beam_mapping, sem presumir natureza/totalidade das reações extraídas ou posicionamento não mapeado.
