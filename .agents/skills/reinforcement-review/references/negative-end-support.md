# Armadura negativa em apoio extremo em pilar

## Sequência de verificação

Usar `negative_end_support_review.review_negative_end_support`: confirmar SupportGeometry END e contexto COLUMN, descobrir as marcas negativas fisicamente presentes na face interna e conservar sua identidade/intervalo/camadas. Cada resultado é produzido por `check_negative_end_support`. Não transportar esta rotina para balanço ou apoio intermediário.

Verificar resistência/necessidade terminal → identificar o nó extremo → modo de ancoragem → perna vertical documentada → disposição transversal → construtibilidade. Os controles são independentes: falta de dimensão do pilar não impede concluir a dobra; falha da dobra não altera a conclusão da flexão. Não agregar num booleano opaco de aprovação do apoio/viga.

## Resistência e demanda

Reutilizar `prepare_reinforcement`, `composition_capacity` e Concretopy. Preservar face tracionada superior, d desde a inferior comprimida e centros físicos. A composição resistente é a que chega à face; diferença entre composição da face e seção terminal torna a associação inconclusiva, sem transportar esforços.

`engineer_confirmed_negative_support_terminal_section_demand_v1`: LEFT usa S1, RIGHT usa S13, diretamente com x e momento originais TQS. Momento positivo não vira solicitação negativa por abs(). Preservar a capacidade total e a comparação independente sem a marca para necessidade terminal. Isso não demonstra que uma peça possa ser reduzida: a marca pode servir outras regiões, como N7 junto a P1. Não otimizar.

## Reta e dobra vertical

Usar `SupportGeometry.penetration` e o ensaio existente `check_negative_end_node`, mantendo eixo, faces, projeção documental e seção TQS separados. O espaço geométrico reto considera largura longitudinal do apoio menos cobrimento. Uma projeção de barra dobrada não comprova desenvolvimento reto. Não somar horizontal e vertical para equivalência de lb.

Decisão `engineer_confirmed_negative_end_support_vertical_bend_v1`:

`L_vertical_required = min(h_beam - cover - stirrup_diameter_mm/10, 2*lb_basic)`.

h_beam é a **altura total da viga**. A expressão pertence ao procedimento do engenheiro, não é atribuída aqui à NBR. A primitiva geométrica compartilhada `negative_end_vertical_bend_limits` foi extraída do nó existente sem alterar seus valores. Concretopy continua calculando lb básico da própria barra, POOR pelas regras negativas confirmadas, sem redução por área ou α=0,7.

A perna fornecida precisa de identificação explícita da orientação vertical, lado do apoio, comprimento em cm e fonte documental. `bend_documents[mark]` aceita `{side, orientation: vertical, vertical_leg_cm, provenance}`; alternativamente uma descrição `end_bend` por lado na própria barra. Barra globalmente bent ou comprimento sem identificação do lado/orientação não bastam. Não criar dobra ausente.

Comparar a perna vertical fornecida à exigida; margem=provided−required. Igualdade atende. Sem geometria/documentação suficiente, INCONCLUSIVE. Um PASS geométrico não aprova resistência da ancoragem curva, pino/raio, confinamento ou fabricação; `curved_anchorage_resistance` permanece separado e inconclusivo nesse cenário.

## Disposição transversal e vibrador

`transverse_disposition` recebe os centros transversais reais (`x_cm`, desde a face lateral esquerda da viga) de cada barra individual, sua marca/bitola/camada e provenance. Conferir correspondência exata com a armadura resistente fornecida. Sem esses centros, não inventar distribuição uniforme nem aprovar o corredor porque seria possível rearranjar as barras.

`minimum_bar_spacing` reutiliza `Concretopy.normas.espacamento_min_arm_long_viga`; mantém o parâmetro default já usado de agregado 16 mm explicitamente identificado, sem certificar o agregado real ou todos os requisitos normativos. Conferir limites laterais e estribo físico. Não duplicar essa equação.

Decisão `engineer_confirmed_negative_reinforcement_vibrator_clearance_v1`: deve existir **pelo menos um** vão livre entre barras adjacentes ≥4 cm. Não é distância entre eixos; não é requisito de 4 cm em todos os vãos. Conservar os vãos individuais e seu máximo. Um corredor suficiente não dispensa os mínimos nos demais pares. Para múltiplas camadas o teste é elementar: não comprova alinhamento vertical do caminho nem todas as interferências do nó.

## Interferência simplificada do pilar

Decisão `engineer_confirmed_column_interference_effective_cover_v1`: somente quando a dimensão **perpendicular** documentada do pilar equivale à largura da viga, usar `effective_lateral_cover=real_cover+2,5 cm` no ensaio transversal. `b_useful=b−2*effective_lateral_cover`; registrar também a largura dentro do estribo, descontando o estribo real já presente. A largura longitudinal do apoio não é sua dimensão perpendicular.

Trata-se de uma sobreposição geométrica para simular interferência de barras do pilar, tomando como referência situações até aproximadamente Ø25; não muda cobrimento físico, posição vertical, d, seção do Concretopy, MRd ou lb. Verificar os mesmos centros fornecidos, sem deslocar/otimizar barras silenciosamente.

`column_geometry` recebe `perpendicular_width_cm` e provenance. O projeto não possui tolerância geral de equivalência confirmada: default é igualdade exata; tolerância não nula somente explicitamente fornecida com `tolerance_provenance`. Sem dimensão/fonte, INCONCLUSIVE. Dimensão não equivalente torna esta hipótese específica NOT_APPLICABLE, sem certificar o nó inteiro.

## Resultado e limites

Retornar separadamente flexural_capacity, straight_anchorage_geometry, vertical_bend_geometry, minimum_bar_spacing, vibrator_access_spacing, column_interference_spacing e curved_anchorage_resistance, com PASS/FAIL/INCONCLUSIVE/NOT_APPLICABLE e provenance. `selected_solution=null`, `detailing_optimization=null`, aprovação global não definida. Preservar conclusões regionais e dos apoios intermediários.

Para futura definição/otimização, documenta-se a preferência do engenheiro pela menor bitola capaz de atender em uma camada, condicionada a resistência, espaçamentos, vibrador, pilar, ancoragem e usos globais da peça. **Não executar seleção nesta etapa.**

Golden V516/V517: P5/N4 3Ø16, perna escrita 40 cm; P6/N7 2Ø20, perna escrita 45 cm. Altura 52, cobrimento 2,5 e estribo Ø8 resultam limite geométrico 48,7 cm; 2lb é maior. Ambas as dobras FAIL, independentemente da flexão terminal PASS. Centros horizontais e dimensão perpendicular de P5/P6 ausentes no modelo: controles correspondentes INCONCLUSIVE. Números e marcas são exemplos, nunca regras de produção.
