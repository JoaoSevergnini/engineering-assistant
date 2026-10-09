# Verificação estrutural após apoio intermediário

## Mudança conceitual e arquitetura

Antes, `longitudinal_review.check_bar_event` deixava al+10φ pendente quando o crossing da remanescente não existia. O núcleo SCALING não recebeu nova física. A classificação pertence à nova camada superior `intermediate_support_review.check_intermediate_bar_event`, que identifica a necessidade antes de chamar os controles existentes. `bar_scaling`, `termination_event`, Concretopy e as fórmulas determinísticas permanecem intactos.

A suficiência é provada por `check_longitudinal` em todas as regiões/extremos e vértices do lóbulo negativo terminal completo, obtido com `terminal_tension_branch` e a vista −Msk. Não aceitar domínio truncado para omitir demanda; não usar abs(), preencher gaps ou extrapolar. Prova incompleta/ambígua mantém INCONCLUSIVE. Remanescente insuficiente com crossing válido continua SCALING. Remanescente suficiente em todo o lóbulo, necessidade anterior individual comprovada e peça contínua atravessando as duas faces conduzem a ANCHORAGE_BEYOND_INTERMEDIATE_SUPPORT.

A necessidade anterior compara independentemente cada composição original sem a marca selecionada, mantendo os peers originais; não é uma sequência de cortes. O after adjacente é sempre físico, após todos os términos coincidentes. Identidade e provenance foram preservadas.

## Geometria e regra

Decisão `engineer_confirmed_intermediate_support_anchorage_when_not_required_v1`: exigir apenas 1,0 lb básico da própria barra, desde a face física voltada ao vão adjacente. Reutilizar SupportGeometry.internal_face_m e direção para dentro do vão; nome da face determinado pelas coordenadas, não por LEFT/RIGHT isolado. Nenhum al/10φ governa esse caso.

S1/S13 permanecem como demanda terminal direta TQS pela regra `engineer_confirmed_negative_support_terminal_section_demand_v1`. Não são origem geométrica de ancoragem. Em P1, eixo 11,000 m, largura 1,420 m: face direita 11,710 m, distinta de S1 11,554 m e DEPEV 0,554 m.

## Golden V516/V517

Cada uma das quatro verificações N8/N9 RIGHT é independente. Before N7+N8+N9; after N7 (2Ø20). Mk_equivalente remanescente 87,300808664 kNm; máximos negativos relevantes 60,418770650 kNm na V516 e 64,586596900 kNm na V517. Necessidade anterior true e adjacente false são demonstradas regionalmente. Terminação documental 12,840 m; disponível desde face 113,000 cm; lb básico Concretopy, POOR, 78,673841577 cm; margem 34,326158423 cm; posição requerida pelo controle 12,496738416 m. Todos PASS, sem hardcoding desses valores na produção. Relatório completo V516_V517_negative_reinforcement_review.md.

Esta decisão supera a interpretação anterior de inconclusivo apenas para o fenômeno comprovado de ancoragem após apoio. Ausência de crossing isolada continua sem determinar aprovação, falha ou dispensa. O relatório histórico da implementação coincidente foi preservado como histórico, não como procedimento vigente.

## Verificação e limitações

23 novos testes de classificação e 4 regressões reais: ambos os sentidos, PASS/equality/FAIL, referência física distinta de seção TQS e suporte largo com DEPEV, crossing válido preservado, ramo incompleto, inexistência sem suficiência, truncamento que esconderia demanda, 2/3 marcas coincidentes, ordem independente, identidade/continuidade, necessidade anterior, sinal original, endpoint fora do vão conhecido e ausência de otimização.

Suíte engineering-assistant: 619 aprovados (39+30+34+516). Concretopy: 405 aprovados. Skill quick_validate válida; git diff --check limpo. Hashes de 173 arquivos protegidos intactos. Comparação do caso anterior confirmou todos os resultados físicos fora das quatro verificações de término direito invariantes. Concretopy e goldens históricos não relacionados não foram modificados.

Escopo implementado: negativas retas horizontais, apoio intermediário, peças/posições conhecidas, mesma referência global nos dois vãos e contexto de seção/camadas representável. A política POOR não é generalizada para positivas. Variações geométricas não representáveis ou falta de prova anterior/adjacente mantêm INCONCLUSIVE. Interferências, nó/dobra, emendas e aprovação global não são demonstrados. Falha de flexão junto a P1, N8/LEFT e pendências das caudas/dobras continuam. Continuidade resistente global segue pendente. selected_solution=null; detailing_optimization=null. Nenhuma otimização ou alteração de desenho foi proposta.

## Arquivos criados/alterados nesta tarefa

- `tools/reinforcement_checks/intermediate_support_review.py`
- `tools/reinforcement_checks/test_intermediate_support_review.py`
- `tools/reinforcement_checks/test_v516_v517_negative.py`
- `analises/pranchas/validar_v516_v517_negativo.py`
- `analises/pranchas/V516_negative_reinforcement_review.json`
- `analises/pranchas/V517_negative_reinforcement_review.json`
- `analises/pranchas/V516_V517_negative_review_validation.json`
- `.agents/skills/reinforcement-review/SKILL.md`
- `.agents/skills/reinforcement-review/references/intermediate-support-longitudinal-verification.md`
- `.agents/skills/reinforcement-review/references/negative-longitudinal-review.md`
- `.agents/skills/reinforcement-review/references/longitudinal-termination-events.md`
- `tools/reinforcement_checks/README.md`
- `tools/reinforcement_checks/longitudinal_review.md`
- `.codex/analises/V516_V517_negative_reinforcement_review.md`
- `.codex/analises/intermediate_support_longitudinal_classification.md`
