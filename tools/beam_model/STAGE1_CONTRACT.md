# Contratos documentais e geometria física — Etapa 1

A extensão reutiliza `longitudinal_beam_detail`, sem criar outro modelo estrutural ou equações de resistência. O JSON documental antigo 1.1/1.2 continua produzindo o modelo antigo 1.0. O documental 1.3 acrescenta `physical_extension` 1.0 e produz modelo 1.1. O replay de `validate(model, raw)` também audita essa extensão.

## Identidades e leitura

- `mark`: posição documental (ex.: N1).
- `occurrence_id`: grupo físico distinto de barras da posição. Duas peças N1 em locais diferentes permanecem duas ocorrências.
- `representation_id`: menção em elevação, corte ou tabela. Representações adicionais nunca duplicam aço.

`pdf_observations.extract_zones(path, zones)` lê zonas explicitamente identificadas, guarda arquivo, SHA256, página, caixa e texto. Agrupa células da tabela TQS pela linha visual, preserva linhas não reconhecidas em `pending` e mantém cobertura como parcial. Não deduz coordenadas longitudinais do comprimento C ou de escala gráfica. O leitor exige a declaração das colunas da tabela e não descobre sozinho os limites de cada viga. Esquemas de tabela diferentes e formas de dobra precisam de interpretação documental adicional.

`documentary_reconciliation.reconcile(observations, coverage)` compara quantidade, bitola, comprimento nominal e forma registrada. `quantity_scope` distingue total da posição, ocorrência e contagem em corte; ocorrência/corte exigem sua identificação. Total só é confrontado com soma física quando a completude do inventário foi explicitamente comprovada. Não há prioridade da tabela sobre elevação/corte. Ausência em extração parcial não prova ausência física. Divergências, revisão comprovadamente desatualizada e perda de integridade são registradas separadamente.

## Evidências e unidades

Cada dado físico usa `{value, state, unit, provenance, criterion}`. Estados: `DOCUMENTED_CONFIRMED`, `INFERRED_EXPLICIT_CONVENTION`, `ENGINEERING_ASSUMPTION`, `CONFLICTING`, `MISSING`, `NOT_APPLICABLE`. Valores ausentes/conflitantes permanecem nulos. Dimensões da seção em cm, bitolas em mm, eixo longitudinal comum em m. Cotas/valores estruturados comprovados prevalecem sobre estimativa gráfica; duas provas divergentes permanecem conflitantes. Suposições não alimentam cálculo por padrão.

Critérios registram `origin`, `reference`, versão quando disponível e fonte: `NORMATIVE`, `OFFICE_STANDARD`, `ENGINEERING_ASSUMPTION`, `SOFTWARE_CRITERION`, `OUT_OF_SCOPE`. Origem normativa exige declaração de consulta efetiva; este trabalho não acrescentou exigências normativas.

## Geometria e barras

`physical_geometry.segments` contém intervalo e seção por trecho: forma, largura, altura, níveis superior/inferior, deslocamento lateral, cobrimento e bitola do estribo. Níveis conhecidos incompatíveis com altura geram conflito. Cada trecho identifica origem e natureza `CONSTANT`, `VARIABLE` ou `UNRESOLVED`. As fronteiras dos intervalos representam transições; não são reconstruídas a partir da distribuição de estribos. Geometria variável sem representação suportada fica pendente, sem seção média fictícia.

`occurrences` guarda quantidade, bitola, intervalos, camadas, continuidade, cortes/extensões e emendas quando documentadas. Não se reconstrói trajetória 3D nem se transforma sobreposição gráfica em colisão. Campos de continuidade/extensões/emendas não verificados continuam sem prova. A consulta `at_x` distingue presença, ausência comprovada e posição indeterminada por ocorrência. Quantidade de barras adicionais não é inferida por repetição de documentos.

`project_occurrences` adapta ao contrato dos verificadores existentes, usando chave `marca@ocorrência` e preservando `documentary_mark`. `project_segments` adapta trechos constantes para `flexure_regions`. Coordenadas gráficas e camadas supostas ficam nulas na projeção resistente por padrão.

`apply_end_convention` reutiliza `termination_geometry.interpret_endpoints` sem alterar a regra confirmada da face externa do pilar terminal. Cota explícita prevalece. Cortes em apoios internos não resolvidos permanecem pendentes. Não se inferem dobras ou comprimentos de ancoragem.

## TQS e integração

A extração e a consolidação preservam o token original `1B/2B/4B`, seu número inteiro, tipo documental e origem. O B não prova lado ou extensão física. `classify_span` separa classificação documental, comprovação física, orientação e conflito. `COLUMN_TERMINATION` é condição terminal, não substitui silenciosamente um vão ou balanço.

O mapeador legado continua limitado a um vão: não foi liberado para dados que não suporta. O caminho físico usa o eixo comum explicitamente declarado e exige prova do registro dos esforços nesse eixo (`force_position_mapping`). Não cria offsets globais presumidos, seções adicionais, combinações ou valores de esforços.

`input_preflight.preflight` verifica dependências por controle e intervalo. `execute_control` é a entrada protegida para ancoragem simplificada, cortante, escalonamento e suspensão: recebe o verificador existente como callback. `check_physical_flexure` integra flexão positiva/negativa ao motor existente com seção local constante. Pontos de transição abrupta permanecem explícitos e pendentes de geometria unilateral. `beam_diagnostic.consolidate(..., input_validation=plans)` conserva as evidências; `correction_engine` aceita a guarda opcional e recusa entradas pendentes. Nenhuma proposta foi gerada nesta etapa.

O caminho legado é compatível e não exige estes novos argumentos. Para obter as novas garantias, os chamadores devem usar a entrada protegida: a etapa não converteu automaticamente todos os scripts históricos.

Um controle exige seus dados próprios: uma falta de cobrimento não impede, por si só, a identificação de uma reação de suspensão. Divergência de comprimento nominal não bloqueia flexão se seu intervalo físico foi comprovado por outra evidência; divergências de quantidade/bitola bloqueiam a capacidade dependente. Hipóteses podem ser avaliadas apenas com opção explícita, com resultado marcado como condicional.

Permanecem as envoltórias TQS, sem exigência de combinações concomitantes. Seção T fica fora do motor retangular. Pinos, caminhos curvos e interferência com armaduras de pilares não são requisitos obrigatórios desse preflight.

## Verificação

Fixtures sintéticas estão identificadas em `stage1_test_fixtures.py`; não representam vigas reais. Regressões reais em `analises/etapa1_leitura_geometria` preservam fontes históricas, caixas/linhas/hash e pendências. Execute as quatro suítes indicadas em `test_results.json`. O leitor PDF requer PyMuPDF; os contratos e demais testes usam biblioteca padrão, e as verificações resistentes continuam usando a API existente do Concretopy.
