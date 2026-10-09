# Correção da revisão de cortante V516/V517 — 08/10/2026

N12 foi reclassificada como ADJACENT_SLAB_NEGATIVE_REINFORCEMENT, preservada documentalmente e excluída de área/ramos/dimensionamento de estribos. A classificação exige geometria, função confirmada e fontes, sem depender da marca. Nenhum estribo de viga foi comprovado nos vãos extremos por essa exclusão.

Cobertura obrigatória separada do domínio TQS: faces físicas internas de pilares comprovados. Todos os oito intervalos anteriormente pendentes estão contidos nos pilares e recebem WITHIN_SUPPORT/NOT_APPLICABLE. Nos vãos extremos, [0,120;1,970] e [11,710;13,560] m permanecem descobertos documentalmente. Assim global_shear_approval=null em ambas; as faixas N13/N1 e a referência por terços não mudaram numericamente.

## Arquivos alterados e finalidade

- tools/reinforcement_checks/shear_coverage.py (novo): classificação funcional e partição da cobertura física com fontes/consistência geométrica.
- tools/reinforcement_checks/shear_review.py: integração, exclusão auditável e aprovação baseada na cobertura necessária.
- tools/reinforcement_checks/test_shear_coverage.py (novo): 35 testes de classificação, faces, larguras, DEPEV, cobertura real, estados e regressões.
- tools/reinforcement_checks/test_shear_review.py: adaptação dos testes afetados ao contrato de faces comprovadas e exclusão de N12; controles anteriores preservados.
- analises/pranchas/validar_v516_v517_cortante.py: evidências funcionais e geometria dos pilares, sem modificar o modelo longitudinal.
- analises/pranchas/V516_shear_reinforcement_review.json e V517_shear_reinforcement_review.json: reprocessamento real.
- analises/pranchas/V516_V517_shear_review_regression.json (novo): hashes permanentes dos controles históricos N13/N1 e referência por terços.
- analises/pranchas/V516_V517_shear_review_validation.json: validação atual e cobertura auditável.
- .agents/skills/reinforcement-review/SKILL.md e references/shear-reinforcement-review.md: procedimento consolidado.
- tools/reinforcement_checks/shear_review.md: contrato das entradas geométricas e novas saídas.
- .codex/analises/shear_concretopy_api_audit.md: esclarecimento posterior, preservando a autorização/histórico.
- .codex/analises/V516_V517_negative_reinforcement_review.md: seções 18/19 atualizadas; histórico longitudinal preservado byte a byte.
- .codex/analises/shear_review_corrections_V516_V517.md: esta entrega.

## Validação e limites

877 testes assistant aprovados; 413 Concretopy; Skill válida. Concretopy não modificado nesta rodada: comparação autorizada e oito regressões anteriores mantidas. Goldens não relacionados preservados por hashes, controles resistentes e diagramas inalterados. A geometria insuficiente/apoio de aplicabilidade não comprovada permanece inconclusiva. A regra de faces de pilares não foi estendida a apoios indiretos ou balanços. Não foram implementadas suspensão, otimização ou correções automáticas. selected_solution/detailing_optimization=null.

Tabelas de faces, eixos, larguras, domínios, oito intervalos reclassificados, faixas reais, controles numéricos e pendências estão no relatório real, seções 18/19. As fontes geométricas de P1 e DEPEV continuam separadas do domínio amostrado. A origem técnica do critério de smax e a autorização da edição são proveniências distintas.
