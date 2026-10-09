# Términos coincidentes — revisão pontual

A restrição nasceu no escopo inicial de uma única marca interrompida: os guardas de `bar_scaling` e `longitudinal_review` exigiam diferença before-after igual à marca selecionada. Foi substituída pela identidade por marca/lado/extremidade em `termination_event`, mantendo after físico após todos os términos documentados. Não há sequência artificial, prioridade ou composição intermediária. Assinaturas públicas e cálculos estruturais não mudaram; metadados e margens foram acrescentados.

V516 e V517: N8/N9 RIGHT em 12,840 m são avaliadas independentemente. Before N7+N8+N9, after N7; al+lb PASS, margem 3,226158 cm e término requerido desse controle 12,807738 m. al+10φ permanece null pela inexistência de crossing, pois N7 cobre todo o ramo. Posição requerida global null; não há aprovação forçada. Dados completos por marca no relatório V516_V517_negative_reinforcement_review.md e JSONs associados.

A regra terminal negativa foi documentada com provenance: LEFT=S1, RIGHT=S13; momento e x originais sem transporte DEPEV. Diagrama, resistência, al, lb básico em má aderência e seleção branch-aware preservados.

Testes: 23 novos (2/3 marcas, camadas/bitolas/quantidades distintas, required_end diferente, ausência de prioridade, orientação LEFT, invariância de entrada, single mark, inexistência de crossing e S1/S13). Suíte completa 592 aprovados; Concretopy 405 aprovados; quick_validate válido; git diff --check limpo. A comparação do golden histórico V1001 foi ajustada para comparar todos os campos persistidos, aceitando apenas o novo campo de margem sem regravar o golden.

SHA-256 de 165 arquivos protegidos, incluindo Concretopy e goldens anteriores: nenhum mudou. Comparação dos casos anteriores V516/V517 confirmou geometria, regiões de flexão, nós e resultados físicos dos demais eventos invariantes. Relatórios/goldens históricos preservados. Concretopy não foi alterado.

Limites: composição ambígua, reposição/início simultâneo, camadas sem posição e geometria não representável continuam bloqueados. SCALING sem crossing não inventa referência; por isso N8/N9 RIGHT permanecem inconclusivas apesar de al+lb atender. As falhas prévias junto a P1 e N8/LEFT e as pendências das caudas mistas continuam. Não foram implementados grampos negativos ou aprovação global.

Arquivos desta tarefa:

- `tools/reinforcement_checks/termination_event.py`
- `tools/reinforcement_checks/bar_scaling.py`
- `tools/reinforcement_checks/longitudinal_review.py`
- `tools/reinforcement_checks/test_termination_events.py`
- `tools/reinforcement_checks/test_bar_scaling.py`
- `tools/reinforcement_checks/test_longitudinal_negative.py`
- `tools/reinforcement_checks/test_v516_v517_negative.py`
- `tools/reinforcement_checks/bar_scaling.md`
- `tools/reinforcement_checks/longitudinal_review.md`
- `tools/reinforcement_checks/README.md`
- `.agents/skills/reinforcement-review/SKILL.md`
- `.agents/skills/reinforcement-review/references/longitudinal-termination-events.md`
- `.agents/skills/reinforcement-review/references/positive-bar-scaling.md`
- `.agents/skills/reinforcement-review/references/negative-longitudinal-review.md`
- `analises/pranchas/validar_v516_v517_negativo.py`
- `analises/pranchas/V516_negative_reinforcement_review.json`
- `analises/pranchas/V517_negative_reinforcement_review.json`
- `.codex/analises/V516_V517_negative_reinforcement_review.md`
- `analises/pranchas/V516_V517_negative_review_validation.json`
