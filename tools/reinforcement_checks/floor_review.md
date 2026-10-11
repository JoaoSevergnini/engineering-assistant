# Contrato operacional de pavimento — Etapa 1.1

API: `review_floor(spec, adapters=..., api=concretopy)`. CLI: `python tools/reinforcement_checks/floor_review.py manifesto.json --output resultado.json`. `--preflight-only` conserva execução pendente sem carregar a API resistente.

Reutiliza `longitudinal_beam_detail`, extensão física 1.0, eixo comum em metros, projeções por ocorrência, `flexure_regions`, `input_preflight`, `transverse_fit` e `beam_diagnostic`. Não altera métodos resistentes nem produz correções.

## Manifesto

Campos principais: `floor`, `beam_inventory_complete`, `sources` (`form`, `detailing`, `tqs`) e `beams`. Cada fonte admite `path`, `sha256`, `zones` para extração PDF, ou `extraction_archive` + `archive_sha256`. Extração preservada exige `source_sha256` e `provenance`; replay não significa releitura do original. Fonte indisponível mantém pendência.

Viga: `beam_id`, `document` 1.3 ou `model` físico preservado, `review_interval_m`, `form`, `layer_observations`, `positioned_tqs`, `registrations`, `jobs`. O domínio de planejamento não prova geometria. `detailing_extraction` opcional é específica da viga; não misturar marcas de outras vigas.

`form.coordinate_system` deve coincidir com o eixo físico e `form.provenance` identifica fontes. `segments` usa `id`, `geometry_type` e `fields`: `x_start_m`, `x_end_m`, `section_shape`, `width_cm`, `height_cm`, `top_level_cm`, `bottom_level_cm`, `lateral_offset_cm`. `detail_geometry` pode fornecer cobrimento e bitola dos estribos de fontes próprias. `support_faces`, `spans`, `transitions` mantêm as interpretações físicas. `comparisons` admite confronto explícito de fatos LST/detalhamento, sem preencher a forma silenciosamente.

Somente `segment_inventory_complete` como fato documental de valor `true` autoriza substituir integralmente os segmentos históricos pela lista da forma. Sem essa prova, segmentos antigos não reconciliados permanecem pendentes. Trechos de apoios/transições sem definição devem constar com seus limites conhecidos e geometria não resolvida; não declarar inventário completo omitindo essas regiões.

Campo de forma: `documentary_state` = `PROVED` + `fact`, `ABSENT_IN_DRAWING`, `PRESENT_NOT_EXTRACTED`, `CONFLICTING` ou `NOT_EXAMINED`. Ausência na prancha exige `review.relevant_region_examined=true`, `review.scope` e `review.provenance`. Comprovação exige fato `DOCUMENTED_CONFIRMED`, unidade e origem. `clarification` registra a informação que precisa ser cotada/esclarecida na forma. Fonte inacessível não comprova ausência na prancha.

`registrations` usa chaves de vão como strings e registra `span_id`, eixo comum e dois `anchors` de fatos `local_m/common_m` em metros. Posições locais vêm de `section_positions.fill_positions`; o adaptador preserva valores/envoltórias. Escala divergente, prova insuficiente, extrapolação ou orientação reversa ficam pendentes. Não somar vãos para fabricar offsets.

`layer_observations` usa `occurrence_id` como chave. `near_bar_text` e `section` são fatos com vetores de quantidades por camada. Texto tem prioridade; divergência comprovada com corte gera conflito. Após exame, `explicit_indication_absent=true` com `review_provenance` autoriza a primeira camada como convenção explícita do escritório. Falta de extração não autoriza essa declaração.

`jobs`: `id` único, `control`, `interval_m`, `span_id`, `inputs`, `adapter` opcional e parâmetros próprios. Flexão possui adaptador padrão; `context` + `control_inputs` criam lotes por vão/região. Contexto usa os parâmetros existentes do motor; seção local e diagrama vêm do físico/TQS. `force_position_mapping`, `moment_envelope` e `layer_fit` são derivados pelo fluxo, não liberados por um `true` arbitrário.

Demais controles usam adaptadores explícitos por caso, reutilizando `check_support` (**generate_corrections=False**), `check_drawn_region`, `check_bar_scaling`, `check_bar_event`, `check_intermediate_bar_event`, verificações de continuidade e `review_suspension`. Adaptador recebe `{model, job, inputs, registered_span, bars, layer_fit, api}` e retorna o resultado original com `status`, `overall_structural_result` ou `passes`; outros resumos devem ser normalizados preservando o original. Adaptador ausente gera pendência específica. Não há adaptador universal automático de nós/continuidade.

Se um adaptador de ancoragem/cortante/suspensão também utilizar distribuição de camadas em cálculo resistente, declarar `uses_layers_for_resistance=true` no job. Isso exige camadas, ordem, inventário completo e cabimento antes da execução. Uma verificação simplificada que não depende de camadas conserva suas dependências próprias.

## Invariantes

- Seguir extração → reconciliação → forma → eixo comum → camadas → preflight → verificadores → diagnóstico. Nenhum callback é chamado antes de `preflight`/`execute`.
- Mudanças de seção/desníveis vêm da forma; LST valida/complementa interpretação documentada. Distribuição de estribos, comprimento C e escala gráfica não provam posição da transição.
- Cabimento é conjunto por face/camada usando `support_correction.transverse_fit`. Incompatibilidade gera falha geométrica; cálculo dependente não executa nem inventa outra distribuição.
- Não criar seção média para perfis variáveis não suportados. Pontos de transição abrupta ficam pendentes de tratamento unilateral. Bloquear apenas controles dependentes.
- Inventário longitudinal conserva intervalos, continuidade, emendas, términos e prolongamentos, sem atribuir conformidade normativa pela mera sobreposição. Usar as regras já referenciadas na skill.
- Materiais, completude e aplicabilidade exigem evidência própria. Verificador/planejamento ausente não vira PASS ou NOT_APPLICABLE.
- Preservar históricos, Concretopy e métodos resistentes. Não editar PDFs nem gerar propostas/otimização.

## Trechos constantes com mudança de seção

`section_checks` aciona o procedimento definido pelo engenheiro dentro do fluxo existente. Mudanças comprovadas de largura, altura ou níveis também o acionam automaticamente. `domains` associa cada domínio documentado a `span_id` e `interval_m` (fato em metros); na ausência desse parâmetro, são usados somente os limites comprovados dos vãos físicos existentes. Apoios de geometria pendente não são atravessados.

Cada trecho seleciona |Vk| nas duas envoltórias características **dentro do intervalo físico**. Somente depois da guarda específica `SECTION_AL` é chamado `Concretopy.calcular_al`, uma vez por trecho. O contexto deve comprovar `al_scope_confirmed`, `al_scope_provenance`, estribos verticais (`stirrup_angle_degrees=90`) e ausência dos efeitos de força normal (`axial_force_kn=0`), além dos materiais. Não basta fornecer apenas resistências e coeficientes.

`effective_depths[segment_id]` aceita um fato comprovado em cm. Alternativamente, a seleção existente de d usa os centroides retornados nas composições físicas de flexão; composições incompletas impedem essa derivação. Não se estima d apenas pela altura da forma.

O resultado separa `physical_interval_m`, `shear_selection`, `al`, `moment_search_interval_m` e extremos positivos/negativos. Transições internas comprovadas ampliam ambos os lados pelo al próprio de cada trecho, limitadas ao domínio aplicável. Barras não são prolongadas: falta de prova de continuidade na região ampliada gera pendência. Essa prova conservadora não substitui os controles de escalonamento e ancoragem existentes.

`drawn_stirrup_regions` exige intervalo físico, diâmetro em mm, espaçamento em cm, número de ramos, função física e fonte. A cobertura deve ser completa e sem ambiguidade. O cortante de cada verificação é o máximo do trecho físico, sem ampliação por al.

Descontinuidades declaradas em `domains[].discontinuities_m` (fatos em m) bloqueiam a interpolação do cortante; descontinuidades de momentos devem ser declaradas na própria série. Sem valores unilaterais tratados explicitamente, os cálculos dependentes ficam pendentes.

`suspension_connections` utiliza o contrato existente de conexões e requer `suspension_inventory_source`. Na transição comprovada, a distribuição usa a menor altura adjacente e os subintervalos mantêm seus próprios contextos resistentes. Alertas de detalhamento existentes conservam `REQUIRES_ENGINEERING_REVIEW`. A aprovação local da descontinuidade e a aprovação integral da viga permanecem separadas.

Reprodução: `python analises/trechos_secao_variavel/validar.py`. Os arquivos `sintetico_*.json` demonstram o procedimento com dados de teste; `resultado_v611.json` registra somente verificações reais possíveis e suas pendências; `resultado_v607.json` preserva a regressão resistente.

### Suspensão de cortante por desnível inferior

O fluxo por trechos identifica automaticamente as mudanças entre seções físicas ordenadas e retorna `bottom_step_suspension`, separado de `suspension` por apoio indireto. Comparar `geometry.bottom_level_cm` comprovado pela forma: fundos iguais dão `NOT_APPLICABLE` exclusivamente para a armadura adicional; a menor cota identifica a seção suspensa, independentemente de altura e orientação.

Se as faces dos trechos coincidirem, a coordenada comprovada define a transição. Uma região de apoio com posição interna desconhecida não é convertida em ponto; preserva o intervalo pendente. Os trechos e a transição devem pertencer ao mesmo mecanismo físico documentado, sem atravessar apoios ou descontinuidades desconhecidas.

`section_checks.gamma_n` é um fato com coeficiente adimensional explicitamente documentado ou convenção confirmada; não há valor padrão. `height_change_transitions` permite fornecer `left_segment_id`, `right_segment_id`, `position_m` (fato em m), `gamma_n` e `shear_sides`. Esta última usa chaves `LEFT/RIGHT`, com `max/min` como fatos característicos em kN, referenciados à própria transição. Em saltos, exigir valores unilaterais comprovados; sem eles, o diagrama não interpola pelo salto. Fora de saltos, reutilizar a consulta do diagrama TQS registrado na coordenada da transição.

O cortante governante adicional é o maior absoluto das envoltórias **do lado de fundo mais baixo**, preservando os dois lados e sinais. Não usar o máximo de todo o vão. O intervalo adicional ocupa `[xt-h/200, xt]` se o fundo mais baixo estiver à esquerda ou `[xt, xt+h/200]` à direita, em metros. Nunca truncar, deslocar ou pôr parte do adensamento no lado mais alto.

Área adicional em cm² = `abs(Vk) * gamma_f * gamma_n / fyd(kN/cm²)`, com fyd retornado por Concretopy. A conversão aço/força é compartilhada com a suspensão existente. Taxa adicional em cm²/m = `As/(h/2)*100`, com h em cm. **Neste complemento**, a taxa total é a taxa usual governante de cortante da própria seção, incluindo seu mínimo quando governante, **mais** a taxa adicional. Não aplicar o fator de 75% nem a combinação do procedimento de apoio indireto.

`drawn_stirrup_regions` deve comprovar também `position_state=DOCUMENTED_CONFIRMED`, além de fonte, bitola, ramos, espaçamento e intervalo. Particionar toda a região unilateral: trecho sem cobertura, extensão presumida ou peças sobrepostas ficam inconclusivos; não somar a mesma área duas vezes. Regiões adicionais de transições distintas que se sobreponham exigem combinação documentada, preservando falhas numéricas conhecidas.

A guarda usa `height_change_suspension=True` no controle de cortante e exige geometria da transição, gamma_n, materiais, d, mapeamento, séries, regiões transversais e confirmação do escopo existente de cortante. Cabimento por ramos/porta-estribo, espaçamentos, compressão diagonal e alertas usuais reutilizam `check_drawn_region`. Aprovação local especial da descontinuidade e aprovação da viga continuam separadas.

As consultas da transição e a cobertura de cortante são validadas na região unilateral exigida. Lacunas fora dela não são transportadas para esse controle; continuam registradas nas verificações físicas correspondentes. Falha comprovada de compressão diagonal permanece FAIL mesmo quando impede calcular a taxa total.

Reprodução independente, sem sobrescrever a etapa anterior: `python analises/suspensao_desnivel_inferior/validar.py` e `python analises/suspensao_desnivel_inferior/gerar_relatorio.py`.

## Validação

Falha de plotagem longitudinal comprovada (`PLOTTING_INTEGRITY`, vista `ELEVATION`) suspende a revisão estrutural completa da viga pela guarda, incluindo controles de outra face. Conservar as posições da tabela/cortes, sem deduzir seus intervalos. A pendência é documental e exige corrigir/reemitir a prancha; não é FAIL resistente.

Transições com intervalo de influência conhecido são registradas em `regional_method_scope` e `input_validation.limitations` com `implementation=NOT_IMPLEMENTED`, mantendo `INCONCLUSIVE / NOT_EXECUTED`. A falta de cota permanece separada em `position_state`. Regiões constantes independentes mantêm o método existente, sujeito às suas próprias entradas.

`section_positions.fill_positions(..., cantilever_contexts=...)` aceita contextos por id do vão: orientação com evidência e `physical_bounds` no eixo comum. Em cada série VGESFS correspondente ao balanço, a seção inicial é a face livre LEFT e a final é a face livre RIGHT. Exige comprimento compatível com os limites da forma, identidade do vão e ordem das 13 seções; valores/sinais permanecem intactos. Balanço único também exige orientação comprovada. Não utilizar séries de outro vão para preencher uma série ausente. Registrar depois a associação local/comum pelo mecanismo existente.

`python analises/etapa1_1_integracao/validate_stage.py` reproduz quatro casos preservados, inventaria chamadores por AST, executa quatro suítes e compara hashes históricos/Concretopy. Sintéticos em `test_floor_review.py` não comprovam geometria real. V610/V611/V626 dependem da forma original para certificar transições/balanço; V623 conserva N2 e falha de plotagem sem fabricar posição longitudinal.
