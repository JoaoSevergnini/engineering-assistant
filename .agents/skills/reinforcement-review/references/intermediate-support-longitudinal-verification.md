# Classificar a verificação longitudinal após apoio intermediário

Decisão do engenheiro: `engineer_confirmed_intermediate_support_anchorage_when_not_required_v1`.

Quando uma armadura longitudinal é necessária de um lado de um apoio intermediário, atravessa o apoio e não é necessária no vão adjacente porque a armadura remanescente atende integralmente à demanda desse ramo, não se aplicam nesse lado al+lb ou al+10φ. Verificar somente 1,0 lb básico da própria barra, desde a face física voltada ao vão adjacente. Esta é uma decisão do engenheiro, não uma prescrição aqui atribuída à NBR.

## Identificar antes de calcular

Usar `tools/reinforcement_checks/intermediate_support_review.check_intermediate_bar_event`, camada acima de `longitudinal_review.check_bar_event`. A implementação atual trata negativas retas horizontais, má aderência confirmada, apoios INTERMEDIATE e posições/camadas conhecidas, em um sistema global comum. Não transportar automaticamente esta política de aderência para positivas.

1. Vincular a marca e a peça contínua aos dois vãos e ao apoio físico (`SupportGeometry`). Comprovar passagem pelas duas faces, identidade, quantidade, bitola, trajetória e origem documental.
2. Determinar before/after físicos do término segundo [eventos independentes](longitudinal-termination-events.md). A remanescente adjacente é after após todos os términos documentados coincidentes; não manter outra marca ficticiamente após seu término.
3. Preparar as posições pelo procedimento existente. Verificar a remanescente em **todas** as regiões do lóbulo negativo conectado ao apoio: extremos de regiões e vértices piecewise-linear. Reutilizar `terminal_tension_branch`, `tension_diagram` e `check_longitudinal`; a vista é −Msk, nunca abs(). O teste cobre o lóbulo completo, não aceita omitir demanda com domínio encurtado fornecido pelo chamador. Prova válida exige hipóteses/capacidades resolvidas e nenhum gap relevante. Sem extrapolar.
4. Se a remanescente não atender parte do ramo, encaminhar ao SCALING existente. Crossing branch-aware válido mantém os controles anteriores. Falta/ambiguidade de crossing permanece INCONCLUSIVE, sem fabricar referência.
5. Se a remanescente atender tudo, registrar `BAR_NOT_REQUIRED_IN_ADJACENT_SPAN`. Demonstrar a necessidade no lado anterior por comparação regional independente da composição original sem a marca selecionada, preservando posições e demais marcas originais. Isso é uma comparação de necessidade, não uma ordem fictícia de cortes. Falta de prova, composição ambígua ou geometria inválida mantém INCONCLUSIVE.
6. Com necessidade anterior e dispensa adjacente demonstradas, classificar `ANCHORAGE_BEYOND_INTERMEDIATE_SUPPORT`. Calcular apenas lb básico Concretopy e conferir o prolongamento geométrico.

## Geometria e resultado

`SupportGeometry.internal_face_m` é a face voltada ao vão adjacente; a direção é `direction_into_span`. Validar faces, largura, eixo e posição dos diagramas. Registrar também o nome físico da face derivado de suas coordenadas. Não escolher face por uma string isolada.

L_available é a distância orientada desde essa face até a extremidade documental, em cm. L_required=1,0*lb_basic; margem=L_available−L_required. Igualdade atende. Posição requerida é face+comprimento no sentido físico. Sem al, 10φ ou crossing artificial nesse cenário.

Separar `support_terminal_demand` (S1 LEFT / S13 RIGHT, posição original TQS) de `anchorage_reference_face` (geometria física). Preservar `engineer_confirmed_negative_support_terminal_section_demand_v1`; DEPEV pode participar da auditoria de esforços, mas não substitui a face física.

Cada marca coincidente conserva um resultado próprio. Quantidade, diâmetro e camada não determinam prioridade. Registrar composição, prova regional de necessidade nos dois lados, máximo de demanda adjacente, capacidade remanescente, face, extremidade, aderência, chamada lb, comprimento/margem, PASS/FAIL e provenance. Inconclusivo não equivale a falha. Não considerar uma aprovação local como aprovação da viga.

## Escopo desta etapa

Este workflow executa **verificação estrutural do detalhamento existente**. `detailing_optimization=null` e `selected_solution=null`: não propor encurtamento, eliminação, economia de aço ou redesenho. Dados uniformes de seção/camadas por chamada devem representar o ramo; variações não representáveis exigem contexto regional adicional, não hipótese silenciosa. Nó completo, dobra, emendas e interferências não são aprovados por este controle.

Regressão V516/V517: N8/N9 necessárias à esquerda de P1; N7 suficiente no lóbulo negativo do vão à direita; face direita x=11,710 m e S1 x=11,554 m são distintos. Nomes e números são apenas golden. Relatório real: `.codex/analises/V516_V517_negative_reinforcement_review.md`.
