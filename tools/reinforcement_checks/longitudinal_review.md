# Contrato da revisão longitudinal negativa

## Responsabilidades e reutilização

`longitudinal_review` interpreta sinal, faces, camadas e evento. `negative_detailing` aplica decisões específicas de porta-estribo, continuidade, nó e balanço. As ferramentas chamam as primitivas existentes de regiões (`flexure_regions`), configuração/resistência regional (`support_correction`), crossings (`bar_scaling.locate_references`), esforço (`moment_diagram`, `tqs_moments`, `tqs_shear`), direção (`support_geometry.OrientedAxis`) e controles (`support_anchorage`). Concretopy continua responsável por áreas de barras, posicionamento convencional, resistência, fbd, lb e al.

Os novos keywords `flexure_sign` de composição, regiões, auditoria TQS e verificação longitudinal têm default POSITIVE. Os resultados físicos positivos anteriores permanecem protegidos por testes e hashes. Não existem cópias `negative_flexure.py` / `negative_bar_scaling.py`.

## Entrada e API

- `prepare_reinforcement(bars, context, api, flexure_sign=...)`: barras com marca única, função/face, quantidade, vetor de camadas, bitola, intervalo comum e source. Contexto contém section, materiais/gammas e centros documentais ou ordem explicitamente confirmada desde a face tracionada.
- `layer_centers`: entradas documentary_layer, origin BOTTOM/TOP/COMPRESSION_FACE, value_cm e provenance. A ferramenta converte e ordena fisicamente, preservando vetor original. Sem centros, layer_order_basis=from_tension_face e layer_order_provenance são obrigatórios; a API de posicionamento do Concretopy precisa representar cada camada (mistura não resolvida bloqueia posicionamento automático).
- `check_flexure_regions(..., flexure_sign, domain=None)`: vista de sinal sem modificar o original; consulta limites e vértices de cada região. Retorna capacidades, hipóteses, esforços assinados, composição física e utilização. Regiões sem demanda negativa são NOT_APPLICABLE. Geometria não resolvida bloqueia conclusão; capacidades regionais não aprovam nó/armadura mínima.
- `check_bar_event(..., mark, cut_side, mode=SCALING|SPAN_TERMINATION, branch_domain=None)`: uma marca por evento, inclusive multilayer; segmento reto horizontal, forma deslizante excluída e contexto longitudinal explícito. `al_scope_confirmed` autoriza a seleção de Vk da regra existente. Usa ambas as envoltórias auditadas e máximo absoluto no domínio físico do vão. `span_domain_m`, quando fornecido, apenas confirma a geometria conhecida do corte, nunca autoriza extrapolar esforço.
- `terminal_tension_branch(diagram, sign, side)` seleciona o lóbulo conectado ao terminal amostrado, mantendo o ponto adjacente de sinal oposto para cruzamento linear. O chamador pode fornecer domínio de ramo validado. Pico/crossing ambíguo bloqueia.

A extremidade física nunca é arredondada para seção TQS. Se estiver além do domínio do ramo selecionado mas dentro do vão conhecido, `reference_selection_endpoint_m` é limitado ao ramo somente para selecionar crossings existentes; distâncias e posições finais usam `actual_end_position_m` documental. Nenhum esforço é extrapolado.

Antes/depois são memberships unilaterais exatas no sentido do corte, sem epsilon. Posições físicas preparadas são preservadas ao retirar camadas. Extras anteriores ao evento podem existir entre pico/crossing e corte, mas a composição do evento deve permanecer presente nesse intervalo.

## Resultado por evento

Retorna composição antes/depois; capacidade anterior e remanescente ou levada ao término; todos os crossings/diagnósticos; pico amostrado; centroide anterior para al; Vk governante com sinal/série/seção; chamada Concretopy al; ancoragem básica em má aderência; 10φ; controles independentes al_plus_lb e al_plus_10phi; posições finais exigidas e controle governante; provenance; passes/complete.

SCALING usa pico + lb e crossing remanescente + 10φ. SPAN_TERMINATION usa crossing da marca levada ao término + lb e zero + 10φ. Marcas distintas terminando na mesma coordenada recebem eventos independentes, com before/after físicos comuns e lb/10φ próprios; não existe estado intermediário nem ordem de remoção. Capacidade estritamente superior ao ramo sem crossing de plena utilização torna somente o controle correspondente NOT_APPLICABLE. Sem crossing válido no escalonamento, manter pendente.

`basic_anchorage` recupera lb básico com má aderência, sem redução por área ou gancho. É computável mesmo se d/camadas não estiverem resolvidos; al e conclusão continuam pendentes. Contextos positivos exigem a classificação geométrica já existente, portanto não usam essa política negativa.

## Detalhamento específico

`check_stirrup_holder` exige função/documentação; verifica ausência de negativo e regiões efetivas de estribos. Mudança de bitola regional não gera bitola global arbitrária. `explicit_skin` significa evidência documental explícita, não inferência por pontos do corte; function=skin isolada não basta.

`check_intermediate_continuity` recebe geometria RIGHT do vão esquerdo e LEFT do direito, no mesmo apoio físico, e verificações independentes previamente feitas com seus próprios diagramas. O chamador é responsável por vincular cada chamada ao próprio vão. Exige evidência de continuidade e trajetória/camada/bitola compatíveis. Terminar dentro do apoio ou identidade incerta não recebe crédito de continuidade.

`check_negative_end_node` diferencia apoio extremo em pilar e balanço único confirmado. O ensaio reto de nó comum utiliza lb básico integral, sem crédito por excesso de área/gancho; é verificação do cenário básico, não dimensionamento completo do nó. Balanço único utiliza a decisão 1,5lb. Quando não há espaço, calcula somente a proposta geométrica de perna de dobra min(h−c−φ_estribo,2lb), mantendo resistência de ancoragem null e fabricação incompleta. Não calcula C, raio/pino nem α=0,7. Barra que atravessa um apoio END não recebe uma regra de continuidade inventada.

`check_cantilever_free_end` compara a perna vertical documental com h−2c−φ_estribo. Mantém os controles longitudinais recebidos separadamente; não cria uma posição final fictícia somando comprimentos ortogonais. O resultado geométrico não aprova a fabricação da dobra.

## Semântica e limites

True: controle aplicável completo atendido. False: completo e falhou. Null: dependência não resolvida. NOT_APPLICABLE é explícito e preserva razão. Agregação negativa não transforma informação faltante em reprovação. `selected_solution` permanece null.

Não calcula grampos negativos, emendas, fabricação/dobra completa, interferências do nó, armadura mínima ou aprovação global. Mudança de seção/cobrimento/estribo exige contexto regional explícito; não usar valores de outra região sem hipótese documentada. Verificação de continuidade requer os dois diagramas. Aderência negativa POOR e comprimentos específicos são decisões do engenheiro, não novas prescrições normativas.

Referência operacional: [revisão negativa](../../.agents/skills/reinforcement-review/references/negative-longitudinal-review.md). Regenerar somente o novo golden: `python -B analises/pranchas/validar_v1001_negativo.py`. Testes: `python -B -m unittest discover -s tools/reinforcement_checks -p test_longitudinal_negative.py`.

`termination_event.describe_termination` registra identidade por marca/lado/extremidade e todas as marcas coincidentes. `provided_end_position_m` é documental; cada controle traz `margin_cm` e posição requerida; posição requerida global fica null enquanto inconclusivo.

`negative_support_terminal_demand(diagram, support_side)` registra `engineer_confirmed_negative_support_terminal_section_demand_v1`: LEFT=S1, RIGHT=S13, amostra original e x original, sem transporte DEPEV, interpolação ou extrapolação.

## Classificação prévia junto a apoio intermediário

`intermediate_support_review.check_intermediate_bar_event` é a camada superior para necessidade nos dois lados. O núcleo deste módulo mantém SCALING, mas não deve ser usado isoladamente para concluir que ausência de crossing é pendência quando a prova regional demonstra remanescente suficiente e necessidade anterior. Nesse caso a nova camada aplica apenas 1,0 lb básico desde `SupportGeometry.internal_face_m`, preservando separadamente a solicitação terminal S1/S13. Decisão `engineer_confirmed_intermediate_support_anchorage_when_not_required_v1`; ver referência operacional vinculada no README. Campos `classification`, `adjacent_need_evidence`, `previous_need_evidence`, `anchorage_reference_face` e `detailing_optimization=null` auditam essa decisão.

## Revisão negativa de apoio extremo

`negative_end_support_review.review_negative_end_support` descobre marcas que chegam à face END/COLUMN; `check_negative_end_support` separa flexão terminal, reta, dobra vertical e disposição transversal. Reutiliza o nó existente e a primitiva geométrica compartilhada `negative_end_vertical_bend_limits`, sem novo motor resistente. Centros transversais/cota perpendicular ausentes não são estimados. Contratos, fontes de dobra por lado e regras: [apoio negativo extremo](../../.agents/skills/reinforcement-review/references/negative-end-support.md). Sem otimização; selected_solution e detailing_optimization null.
