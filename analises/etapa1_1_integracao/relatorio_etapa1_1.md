# Etapa 1.1 — Integração operacional da geometria e interpretação documental

Data: 10/10/2026. Implementação e regressão documental de V610, V611, V623 e V626, com leitura da forma fornecida durante esta sessão. Não é aprovação do pavimento nem recálculo resistente integral dessas vigas.

## 1. Arquitetura reutilizada

A [auditoria inicial](auditoria_inicial.md) foi registrada antes das alterações. Reutilizados: `longitudinal_beam_detail`, extensão `physical_geometry` 1.0, fatos de `input_evidence`, reconciliação por marca/representação, ocorrências físicas, `section_positions.fill_positions`, seleção de fontes `map_beam.selected`, `project_segments`, `project_occurrences`, `flexure_regions`, `input_preflight`, `support_correction.transverse_fit`, `longitudinal_review.check_flexure_regions` e `beam_diagnostic.consolidate`.

Não foi criado outro modelo longitudinal. O novo registro de coordenadas é um adaptador das posições locais já existentes para o eixo comum do modelo físico. Os verificadores e métodos resistentes permanecem os mesmos.

## 2. Módulos modificados e acrescentados

| Módulo | Alteração |
|---|---|
| `input_preflight.py` | Guarda adicional de cabimento nas revisões operacionais; convenções/hipóteses conservam origem. Compatibilidade histórica preservada. |
| `form_geometry.py` | Interpretação dos campos da forma, cobertura examinada, conflitos e substituição do inventário somente mediante prova de completude. Mantém apoios/transições pendentes. |
| `common_axis_registration.py` | Duas referências comprovadas por vão, identidade do eixo, escala/orientação, domínio das séries; preserva posições locais, valores e envoltórias. |
| `layer_interpretation.py` | Texto/corte/convenção por ocorrência; cabimento conjunto por face/camada usando rotina existente. |
| `floor_review.py` | Oito etapas obrigatórias, três fontes documentais, preflight em cada controle, execução protegida, diagnóstico e pendências de fronteiras. |
| `test_floor_review.py` | Casos sintéticos e integração numérica com a API existente. |
| Skill e referências | Encaminhamento obrigatório de pavimentos à nova entrada e contrato operacional documentado. |
| Scripts desta entrega | Extração revisada da forma, reprodução real, auditoria AST, testes e preservação por hashes; saídas apenas nesta pasta. |

Concretopy, scripts históricos, métodos resistentes e PDFs não foram alterados. Os bytes anteriores da skill foram preservados ao acrescentar o encaminhamento.

## 3. Integração do eixo longitudinal

`section_positions` permanece responsável por `x_local = DEPEV_esquerdo + i × comprimento_VGESFS/12`. A distância entre eixos foi conferida independentemente por `DEPEV_esquerdo + comprimento_VGESFS + DEPEV_direito` e comparada às cotas/centros dos apoios na forma. Só após concordância são registradas as posições no eixo comum.

Registrados os vãos 1/2/3 da V610, 1/2/3 da V611 e 1 da V623. Valores, sinais e envelopes TQS permanecem preservados. As âncoras, operandos e fontes aparecem em [real_replay_manifest.json](real_replay_manifest.json) e [real_replay.json](real_replay.json).

V626: a extração preservada não fornece associação/orientação de apoios suficiente para `section_positions`; o fluxo registra `Vao sem numeracao VGESFS ou orientacao dos apoios` e não presume um offset. Geometria de um encontro com outra viga não comprova direção da transferência de carga.

As coordenadas históricas das barras, extraídas graficamente, permanecem hipóteses e não alimentam a resistência. A origem física da forma foi acrescentada ao mesmo contrato de eixo; isso não converte os extremos antigos das barras em prova de registro.

## 4. Interpretação das plantas de formas

Fonte efetivamente examinada: `C:/Users/João Severgnini/Documents/arquivos/051-SJ-EST-EX-010-PLB-TP-R01.pdf`, página 1, planta TIPO e detalhes/cortes da escada. Arquivo com rotação de página 90°; as caixas de exame são coordenadas de exibição e estão identificadas assim na proveniência. Texto, palavras, caixas e SHA256 estão em `form_blocks.json`, `form_words.json` e nos quatro `*_form_reviewed.json`. Recortes PNG documentam as regiões examinadas. A leitura não transformou escala gráfica em dimensão.

Forma: examinada diretamente nesta sessão. Detalhamento e TQS: extrações preservadas em `drawing_inventory.json`, documentos da Etapa 1, `operational_tqs.json` e `*_tqs_raw.json`, com referências/linhas de origem. Os originais de detalhamento/LST não foram relidos nesta sessão. A forma R01 e os detalhamentos preservados R00 exigem controle de compatibilidade de revisões antes de conclusão integral.

Estados independentes: informação comprovada; ausente na região examinada da prancha; presente mas não extraída; divergente; região não examinada. A ausência na prancha exige declaração de exame, escopo e proveniência. Fonte indisponível não vira ausência documental. O inventário de apoios contém faces e eixos; posições transversais/offsets não integralmente extraídos continuam pendentes.

## 5. Tratamento das mudanças de seção e desníveis

| Caso | Informação agora documentada no eixo físico | Limite restante |
|---|---|---|
| V610 | No vão P35–P32: 0–1,22 m, h=129,5 cm; 1,22–2,38 m, h=47 cm; 2,38–3,60 m, h=122 cm, D=+75 cm. Cotas 122+116+122=360 cm e detalhe da escada. | Seção/níveis dentro de P32 e associação da seção nominal LST aos trechos direitos; não usar rótulos V624/V628 como prova da seção da V610. |
| V611 | Vãos livres 0–2,82 m (h=57), 3,52–6,19 m (h=47) e 6,89–9,31 m (h=57); apoios P28/P19/P10/P1 com dimensão longitudinal 70 cm. | Cota da mudança dentro de P19, entre 2,82–3,52 m, e de P10, entre 6,19–6,89 m. |
| V623 | Vão livre P32–P23 de 3,76 m, 19/57; faces e eixos identificados por cotas/coord. Y. | Posição longitudinal da N2 continua não comprovada pela elevação truncada. |
| V626 | Trecho além da face externa P31, −0,93 a −0,80 m, 19/47; trecho livre P31–P24, 0–4,29 m, 19/57; pilares 24/80. | Transição na faixa de P31; registro dos esforços; geometria variável do detalhamento ainda não reconciliada integralmente. |

Coordenadas são relativas à origem física indicada em cada JSON. Dimensões locais documentadas não constituem certificação da geometria inteira. Regiões de apoio não resolvidas são segmentos próprios, com limites conhecidos; não são substituídas por seção média. Pontos de transição abrupta da V610 mantêm diagnóstico de tratamento unilateral pendente.

## 6. Interpretação das camadas

Prioridade ao texto próximo das barras, corte complementar; duas indicações explícitas diferentes geram `CONFLICTING`. Quando a ausência de indicação foi efetivamente examinada, adota-se primeira camada como `INFERRED_EXPLICIT_CONVENTION`, com critério do escritório e origem rastreável. Ausência de extração gera pendência.

Antes da resistência, o fluxo soma todas as ocorrências na mesma face/camada e chama `transverse_fit`. Distribuição incompatível produz falha geométrica independente e impede o cálculo resistente dependente; nenhuma distribuição alternativa é criada. Materiais, cobrimento, estribos, face e completude do inventário continuam com provas próprias.

Nos casos reais, as antigas camadas eram hipóteses manuais. Sem nova leitura comprovada dos textos/cortes de cada ocorrência, a entrada operacional as mantém pendentes, preservando o vetor anterior na origem da interpretação. Não se afirmou que as barras reais não têm indicação de camadas.

## 7. Verificações longitudinais e integração operacional

Extração → reconciliação → forma → eixo comum → camadas → preflight → verificadores existentes → diagnóstico. Todos os seis controles têm plano/estado, mesmo quando não planejados ou sem adaptador. Nenhum verificador recebe entrada pendente. A flexão possui adaptador executável padrão e lotes por vão/região; seção e diagramas vêm do modelo físico/TQS.

Ancoragem, escalonamento, cortante, continuidade e suspensão usam adaptadores explícitos dos verificadores existentes, com contratos/entradas próprios. A infraestrutura protegida foi testada para cada controle; ainda não existe seleção universal automática de adaptador para todos os tipos de nó. Adaptador ou dados ausentes são pendências, não aprovação. `check_support` deve ser chamado com `generate_corrections=False` nesta etapa.

O inventário longitudinal expõe intervalos, continuidade, términos, extensões e emendas por ocorrência. Partição/composição utiliza `flexure_regions`. O inventário não cria uma nova regra normativa nem conclui conformidade pela simples sobreposição. As regras resistentes/normativas continuam nas referências existentes; nenhum novo requisito normativo foi formulado ou atribuído à NBR nesta entrega.

O [inventário AST](legacy_callers_audit.json) lista arquivos, funções e linhas dos chamadores históricos sem importação da guarda. Inclui consumidores legados como `v501_positive_flexure`, scripts de ancoragem/escalonamento em `analises/pranchas` e revisões históricas Silva Jardim. Uma importação do preflight, isoladamente, não demonstra que todos os caminhos são protegidos; isso está indicado no inventário. Históricos permanecem para regressão.

## 8. Comparação antes/depois dos casos reais

[Comparação completa](comparativo_real.json): ocorrências V610 16→16, V611 6→6, V623 4→4 e V626 5→5. Reconciliação documental preservada nos quatro casos. N2 da V623 permanece 4Ø16 C464, com falha de plotagem e limites longitudinais pendentes.

Antes, os limites dos trechos estavam não comprovados. Agora há trechos locais e faces documentados pela forma, sete vãos com esforços registrados e pendências específicas dos nós/transições. Camadas manuais não foram promovidas a prova documental. Os controles reais continuam `PENDING/INCONCLUSIVE`, pois extremos das barras, camadas e outras entradas próprias ainda não estão comprovados.

Nenhum momento resistente real foi recalculado: `resistant_recalculation=false`, `numeric_change=null`. A alteração de resultado nesta etapa é na interpretação geométrica, na rastreabilidade dos esforços e na localização das pendências, sem comparação numérica fictícia de resistência.

## 9. Testes executados

Resultados reproduzíveis em [test_results.json](test_results.json). Suítes: modelo físico/documental, extrator LST, mapeamento e verificadores de armaduras. Os testes novos cobrem múltiplas camadas, ausência comprovada de indicação, cabimento impossível, texto/corte divergentes, soma de marcas na mesma camada, transição sem posição, substituição do inventário com prova de completude, múltiplos vãos com balanço e execução numérica pelo motor existente depois da guarda.

| Suíte | Testes | Resultado |
|---|---:|---|
| beam_model | 71 | Aprovados |
| extrator_lst | 42 | Aprovados |
| beam_mapping | 57 | Aprovados |
| reinforcement_checks | 996 | Aprovados |
| Total | 1166 | Todos aprovados |

Os 32 testes novos estão incluídos na suíte `reinforcement_checks`.

Também verificados: fonte obrigatória mesmo para inaplicabilidade; hash divergente; identidade duplicada; escala/orientação incompatível; nenhum callback resistente quando pendente; controle de suspensão independente de transição de seção; preservação da entrada e dos sinais/esforços. Dados sintéticos estão identificados e não representam comprovação das vigas reais.

Ambiente desta sessão: CPython 3.10.11 de 32 bits. O Python 3.11 usado em regressões anteriores não está instalado; o script usa `sys.executable`. Leitura/renderização do PDF foi feita com PyMuPDF em `tmp/pdf_deps`, sem alteração do Python global. Validador oficial da skill: aprovado no ambiente Windows nativo. Leitura forçada em UTF-8 ainda encontra bytes históricos inválidos no SKILL.md; esses bytes preexistentes foram preservados.

## 10. Pendências e limitações restantes

- Examinar textos de camadas e cortes de cada ocorrência nos detalhamentos originais; confirmar extremos, interrupções, prolongamentos e emendas por cotas/convenção aplicável.
- Resolver as mudanças dentro dos apoios de V611/V626 e a seção/nivelamento na transição junto a P32 da V610; esclarecer isso na forma.
- Reconciliar registro/orientação dos vãos TQS da V626. Não inferir posições de esforços a partir da distribuição dos estribos ou da escala do desenho.
- Completar cobrimento/estribos, materiais, ordem de camadas e inventários próprios dos controles; documentar offsets transversais e compatibilidade entre revisões.
- O leitor extrai zonas declaradas; reconhecimento/associação de geometria e camadas ainda requer interpretação documental rastreável. Não há descoberta automática completa de um pavimento arbitrário.
- Finalizar adaptadores específicos de nós/continuidade/cortante/suspensão conforme os contratos existentes e planejar seus controles por intervalo/evento. Sua ausência permanece explícita.
- Este conjunto real cobre quatro vigas, não o inventário completo V601–V629. `floor_approval=null` e `beam_inventory_complete=false`.

[Preservação por hashes](preservation.json) registra históricos, fontes e Concretopy. Nenhum PDF foi modificado nem proposta de correção foi gerada.
