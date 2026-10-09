# V536 N2: correções por área corrigida — escopo atualizado

Pino, trajetória curva e interferência com armadura do pilar: NOT_EXECUTED_BY_SCOPE_DECISION; não são PASS nem pendências bloqueantes. Demais controles permanecem independentes.

Cenário de gancho previamente confirmado pelo engenheiro é preservado. Não se soma desenvolvimento horizontal+vertical como ancoragem. As_corr e As_adicional vêm exclusivamente do Concretopy.

| Configuração | Tipo | Geometria no escopo | Estrutura | Resultado | Pendências |
|---|---|---|---|---|---|
| existing_area_correction | AREA_CORRECTION | PASS | FAIL | FAIL | affected_scaling, recheck_scaling_for_modified_longitudinal_configuration |
| extend_N3_1 | EXTEND_OTHER_BARS | PASS | INCONCLUSIVE | INCONCLUSIVE | affected_scaling, recheck_scaling_for_modified_longitudinal_configuration |
| extend_N3_2 | EXTEND_OTHER_BARS | PASS | INCONCLUSIVE | INCONCLUSIVE | affected_scaling, recheck_scaling_for_modified_longitudinal_configuration |
| extend_N3_3 | EXTEND_OTHER_BARS | PASS | INCONCLUSIVE | INCONCLUSIVE | affected_scaling, recheck_scaling_for_modified_longitudinal_configuration |
| redistribute_2x12.5_2x16 | REDISTRIBUTE_BARS | PASS | FAIL | FAIL | affected_scaling, recheck_scaling_for_modified_longitudinal_configuration |
| redistribute_2x12.5_3x16 | REDISTRIBUTE_BARS | PASS | FAIL | FAIL | affected_scaling, recheck_scaling_for_modified_longitudinal_configuration |
| redistribute_3x12.5_2x16 | REDISTRIBUTE_BARS | PASS | FAIL | FAIL | affected_scaling, recheck_scaling_for_modified_longitudinal_configuration |
| redistribute_3x12.5_3x16 | REDISTRIBUTE_BARS | PASS | FAIL | FAIL | affected_scaling, recheck_scaling_for_modified_longitudinal_configuration |
| redistribute_2x12.5_2x20 | REDISTRIBUTE_BARS | PASS | FAIL | FAIL | affected_scaling, recheck_scaling_for_modified_longitudinal_configuration |
| redistribute_2x12.5_3x20 | REDISTRIBUTE_BARS | PASS | FAIL | FAIL | affected_scaling, recheck_scaling_for_modified_longitudinal_configuration |
| redistribute_3x12.5_2x20 | REDISTRIBUTE_BARS | PASS | FAIL | FAIL | affected_scaling, recheck_scaling_for_modified_longitudinal_configuration |
| redistribute_3x12.5_3x20 | REDISTRIBUTE_BARS | PASS | FAIL | FAIL | affected_scaling, recheck_scaling_for_modified_longitudinal_configuration |
| redistribute_2x16_2x20 | REDISTRIBUTE_BARS | PASS | FAIL | FAIL | affected_scaling, recheck_scaling_for_modified_longitudinal_configuration |
| redistribute_2x16_3x20 | REDISTRIBUTE_BARS | PASS | FAIL | FAIL | affected_scaling, recheck_scaling_for_modified_longitudinal_configuration |
| redistribute_3x16_2x20 | REDISTRIBUTE_BARS | PASS | FAIL | FAIL | affected_scaling, recheck_scaling_for_modified_longitudinal_configuration |
| redistribute_3x16_3x20 | REDISTRIBUTE_BARS | PASS | FAIL | FAIL | affected_scaling, recheck_scaling_for_modified_longitudinal_configuration |

Cada candidata registra separadamente executados/aprovados, executados/reprovados, não executados por escopo e inconclusivos. Auditoria anterior à exclusão preservada. Área corrigida não comprova todas as condições construtivas. Escalonamentos alterados permanecem pendentes; não se presume atendimento.

Grampos: calculados Ø6,3/Ø8/Ø10 usando As_adicional da N2 original, dois ramos, boa aderência e API de lb existente. Contribuição resistente conjunta NÃO creditada: falta modelo compatível de transferência e posição física da distribuição.

Prioridade: alterar barras existentes; depois avaliar complementação compatível. Nenhuma solução escolhida ou aprovada. selected_solution=null. PDF e históricos preservados.

## Grampos calculados, sem crédito resistente conjunto

| Bitola (mm) | Peças | L mínimo longitudinal (cm) | Contribuição conjunta comprovada |
|---|---|---|---|
| 6.3 | 2 | 60.000000 | Não |
| 8 | 2 | 65.557351 | Não |
| 10 | 1 | 76.571689 | Não |

As_corr original=10,609669966527639 cm²; As existente=9,42477796076938 cm²; As adicional=1,1848920057582593 cm². Valores API, sem copiar fórmulas.

## Validação e arquivos

Alterados correction_engine.py e correction_engine.md; referência positive-support-correction atualizada. Criados validar_v536_correction_scope.py, test_correction_scope.py e resultados scope_updated JSON/Markdown próprios.

8 testes novos aprovados. Suíte completa: 1.065 testes engineering-assistant (39+30+57+939); 427 Concretopy; quick_validate válido. Regressões positivas, negativas e de cortante preservadas. Concretopy não alterado. Após o último ajuste de apresentação de grampos, testes específicos reexecutados e aprovados.

Limitação de implementação: o adaptador ainda não fornece o mapeamento regional completo das marcas propostas para reverificar os escalonamentos modificados. Esse controle permanece INCONCLUSIVE; não se inventou atendimento. A N2 original continua FAIL. Prolongamentos de 1/2/3 barras N3 passam nos controles locais recalculados, mas não possuem conclusão completa.
