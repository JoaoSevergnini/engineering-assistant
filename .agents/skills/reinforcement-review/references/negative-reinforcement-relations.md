# Relações entre negativas de apoios consecutivos

## Camada semântica e entradas

Executar `tools/reinforcement_checks/negative_reinforcement_relations.py`, depois da revisão regional e dos eventos de término. O motor genérico de flexão, SCALING, apoio intermediário e apoio extremo permanece intacto. Ler também [revisão negativa](negative-longitudinal-review.md), [eventos independentes](longitudinal-termination-events.md), [apoio intermediário](intermediate-support-longitudinal-verification.md) e [apoio extremo](negative-end-support.md).

Identificar apoios consecutivos por ocorrência e geometria física, não apenas pelo nome (um mesmo rótulo pode se repetir). Preservar as peças completas: marca, quantidade, bitola, camada, intervalo, trajetória e fonte. O chamador registra a associação estrutural das armaduras aos apoios com provenance. A ferramenta comprova presença nas faces internas correspondentes e examina o diagrama com sinal entre essas faces. Uma interseção geométrica, isoladamente, não comprova o fenômeno.

`review_negative_relation` recebe peças, contexto, diagrama validado, API Concretopy, par de apoios e evidência da associação. Pode receber limites estruturalmente necessários, porta-estribo, densidade para massa e centros transversais individuais. Não inventar esses dados. O papel da relação pode ser inferido do momento e da associação documentada; uma interpretação explicitamente fornecida deve ser compatível com eles.

## Classificar antes de calcular

- **CONTINUOUS_NEGATIVE_REINFORCEMENT:** mesma marca, peça/ trajetória documentada, quantidade, bitola, camadas e intervalo; sem término entre os apoios. Exigir documentação de continuidade e intervalo atravessando ambos os apoios. Não inferir por igualdade de bitola. Preservar a revisão regional: continuidade não cria resistência, não aprova o nó e não elimina falhas. Preferência do engenheiro quando o momento negativo não zera: `engineer_confirmed_negative_continuity_preference_v1`.
- **REINFORCEMENT_LAP_TRANSITION:** peças distintas associadas aos apoios, realizando transição resistente; momento estritamente negativo em todo o intervalo conhecido entre apoios. Comprovar pelos extremos e todos os vértices do diagrama linear. Domínio incompleto/gap impede essa prova. Exigir `2*lb básico` da menor bitola, calculado pelo Concretopy, em POOR bond, sem redução por área ou alpha=0,7. Regra `engineer_confirmed_negative_lap_transition_v1`.
- **DETAILING_OVERLAP:** encontro de extensões de peças distintas, com trecho sem demanda negativa entre apoios e papel de caudas estruturais demonstrado. Para revisar encontro existente, aceita-se a evidência auditada do engenheiro; ela não define centros mistos ou limites requeridos. Exigir ultrapassagem física de 30 cm, regra `engineer_confirmed_negative_detailing_overlap_v1`.
- **INDEPENDENT_REINFORCEMENTS:** limites estruturalmente necessários conhecidos deixam gap maior que 80 cm, com trecho intermediário sem demanda negativa comprovado. Manter porta-estribo convencional como referência; não buscar sua eliminação por esta regra.
- **INCONCLUSIVE:** identidade, papel resistente, limites necessários ou domínio indispensável não comprovados. Não classificar somente por crossing ausente, interseção ou igualdade de bitolas.

## Três comprimentos e três critérios de seleção

| Grandeza | Uso |
|---|---|
| 80 cm | Limite de aplicabilidade da comparação local de massa; gap medido entre limites **estruturalmente necessários** |
| 30 cm | Ultrapassagem mínima no encontro de detalhamento |
| 2*lb básico | Traspasse na transição resistente em momento negativo contínuo |

Para escolher a candidata ao prolongamento: **menor As total**, usando quantidade completa e área de `Concretopy.Barra`. Para lb da transição: **menor bitola**. Para resistência da sobreposição: **grupo completo de menor bitola**, isoladamente. Não confundir os critérios. Empate de áreas ou grupos de mesma bitola não autoriza uma escolha arbitrária; registrar a pendência.

## Resistência de toda a sobreposição

Obter a interseção dos intervalos físicos. Pesquisar a demanda negativa nos dois extremos e em todos os vértices TQS internos usando `moment_at_x`; não extrapolar, não atravessar gaps e não converter momentos positivos em negativos por abs(). Usar somente o grupo completo de menor bitola, com sua posição resistente própria confirmada/convenção existente rastreável e API de flexão do Concretopy. Não somar grupos, usar apenas uma barra ou construir centroide misto.

Comparar `Mk_equivalent_smallest_group >= max_negative_demand_overlap`. Domínio parcial ou posição própria desconhecida torna apenas esse controle INCONCLUSIVE. Esta regra vale tanto para DETAILING_OVERLAP como para REINFORCEMENT_LAP_TRANSITION: `engineer_confirmed_negative_overlap_capacity_v1`. Manter comprimento e resistência como controles independentes PASS/FAIL/INCONCLUSIVE/NOT_APPLICABLE. Sem interseção física não existe uma região resistente de overlap para aprovar.

## Comparação local de massa

Somente quando os limites estruturais e o trecho sem demanda estiverem comprovados, aplicar gap <=80 cm (`engineer_confirmed_negative_detailing_overlap_max_gap_v1`). Não substituir limites necessários pelas pontas desenhadas.

Sem sobreposição existente, comprimento adicional por barra = gap+30 cm; se já existe sobreposição física, acrescentar somente o déficit para 30 cm, nunca mais 30 cm duas vezes. Registrar a base adotada e não confundir consumo para uma alternativa de limites necessários com alteração efetiva de uma barra desenhada mais longa. Multiplicar pela quantidade completa do grupo de menor As total.

`steel_mass.py` é a primitiva única de massa: recebe área da API Concretopy, comprimento total em metros e densidade explicitamente informada com fonte. Não possui tabela de kg/m nem densidade silenciosamente adotada. Preservar unidades e origem.

Para porta-estribo, reutilizar `negative_detailing.check_stirrup_holder`: função documental, ausência de demanda negativa, estribos regionais e bitola mínima max(6,3 mm, bitola regional). Quantidade, comprimento e política de comprimento mínimo devem estar confirmados pelo chamador. Não há regra genérica confirmada desses três dados na infraestrutura atual; sua ausência bloqueia a massa correspondente, sem inventar uma peça.

Comparar massas adicionais, sem score: EXTEND_NEGATIVE_REINFORCEMENT, USE_HANGER_REINFORCEMENT ou EQUIVALENT_STEEL_WEIGHT. Não aplicar desempate. Regra `engineer_confirmed_negative_detailing_overlap_weight_choice_v1`. O resultado econômico não transforma falha resistente em PASS, nem aplica uma alteração.

## Disposição localizada e vibrador

`local_overlap_disposition` sobrepõe a decisão `engineer_confirmed_negative_overlap_local_spacing_v1` à auditoria transversal existente, sem modificar minimum_bar_spacing nem Concretopy. Eximir do mínimo usual somente pares de barras individuais explicitamente identificados, pertencentes aos dois grupos e somente no encontro/traspasse. Não estender a exceção a outras barras ou todo o vão. Não aceitar invasão física das barras ou dos limites laterais.

Avaliar corredor >=4 cm no arranjo transversal global; ele pode estar fora do par sobreposto. Os outros espaços continuam sujeitos ao mínimo geral. Sem centros suficientes, geometria e vibrador ficam INCONCLUSIVE. Não criar camadas, centros ou distribuição uniforme. O controle elementar por camada não comprova colisões entre camadas nem todas as interferências do nó; `ready_for_detailing=false`.

## Eventos existentes, conclusão e goldens

Os controles próprios do encontro não exigem centroide misto N4+N7. Identificar separadamente os términos integrantes da relação e marcar interpretações antigas incompatíveis como SUPERSEDED, preservando os resultados históricos. Um evento SCALING verdadeiro continua exigindo o centroide anterior e todos os controles originais; não substituir sua regra pela menor bitola.

Golden V516/V517: N4/N7 são encontro de detalhamento, com interseção documental [3,635;5,015] m. Usar N4=3Ø16 isolada. N7 é uma peça contínua entre P2/P1. N4/RIGHT e N7/LEFT recebem a interpretação do encontro; N3/RIGHT é encaminhada à ancoragem após apoio intermediário: N4 isolada comprova suficiência de todo o ramo adjacente e N3 é necessária no vão anterior. Medir lb básico desde a face física, sem al ou centroide misto; preservar N7 documentalmente presente e a base conservadora da prova. Os números completos estão no relatório e JSON de cada viga; nomes/valores não são regras de produção.

Preservar a falha regional N7+N8+N9 junto a P1, a falha N8/LEFT, as ancoragens independentes N8/N9 após P1 e as dobras extremas. As decisões deste documento são procedimentos do engenheiro, não transcrições da NBR. Não selecionar nova bitola, quantidade, camada, marca ou redesenho. `selected_solution=null`, `detailing_optimization=null`; aprovação global continua fora desta camada.
