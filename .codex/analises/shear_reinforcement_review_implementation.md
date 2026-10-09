# Implementação da revisão de cortante

Separação SHEAR_REFERENCE_DESIGN / SHEAR_DRAWN_REGION_CHECK: o assistant interpreta geometria, séries e detalhamento; Concretopy mantém os cálculos resistentes. Sem suspensão ou otimização.

Arquivos criados: tools/reinforcement_checks/shear_diagram.py, shear_review.py, test_shear_review.py (105 testes), shear_review.md; analises/pranchas/validar_v516_v517_cortante.py, V516_shear_reinforcement_review.json, V517_shear_reinforcement_review.json, V516_V517_shear_review_validation.json; .agents/skills/reinforcement-review/references/shear-reinforcement-review.md; .codex/analises/shear_concretopy_api_audit.md e este relatório.

Arquivos atualizados: tools/reinforcement_checks/README.md; .agents/skills/reinforcement-review/SKILL.md; .codex/analises/V516_V517_negative_reinforcement_review.md (seções 18/19 acrescentadas).

Concretopy: exclusivamente a comparação autorizada em concretopy/normas/nbr6118.py; novo tests/test_shear_spacing.py com oito casos. Não se afirma que o Concretopy permaneceu intacto: houve esta correção expressamente autorizada. Demais arquivos anteriores preservados por hash.

Resultado: d=46,7 cm nas duas vigas, centroides regionais existentes selecionados por máximo número de camadas, maior As e menor d. Faixas convencionais calculáveis atendem. N12 não recebe crédito automático de dois ramos; faltam ainda fontes de cobertura de alguns trechos de nós. global_shear_approval=null nas duas vigas. Nenhuma solução selecionada.

842 testes assistant e 413 Concretopy aprovados; Skill válida. 199 arquivos anteriores preservados por hash. As tabelas completas, demandas assinadas, faixas, opções, proveniência e pendências estão nas seções 18/19 do relatório real e nos JSON. Nenhuma conclusão longitudinal foi modificada. A API não expõe a parcela Asw/s antes da governância pelo mínimo; o campo permanece null. Capacidade inversa obtida por chamadas determinísticas, crossings pela infraestrutura linear existente.
