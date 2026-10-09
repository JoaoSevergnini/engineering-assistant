# Diagnóstico consolidado por viga

Executar `beam_diagnostic.consolidate(context, modules)` somente sobre verificações já calculadas. O consolidador não importa Concretopy, não interpola diagramas, não calcula capacidades e não propõe correções.

## Contrato normalizado

Contexto obrigatório: `beam_id`, `floor`, `coordinate_system` (origem física, direção, unidade). Preservar geometria/vãos, materiais, versão dos dados, fontes de desenho/TQS e prova da identidade. Um envelope por resultado/escopo contém `discipline`, `beam_id`, `floor`, `coordinate_system`, `source`, `version`, `complete`, `checks`. Disciplinas: positive_flexure, negative_flexure, anchorage, shear e suspension. Múltiplos escopos de uma disciplina são permitidos, sem confundir identidades.

Cada controle contém `check_id` lógico estável, `check_type`, `status`, localização física, marcas, valor necessário/fornecido e unidade comum quando comparáveis, fonte de demanda, desenho e cálculo, razão, critério, evidências e informações ausentes. Sem localização documental, manter null e pendência explícita. Não converter coordenadas locais/globais ou unidades por aproximação. Adaptadores podem fazer apenas conversões explícitas de unidades dos resultados existentes (kN.cm /100 → kN.m), nunca fórmulas resistentes.

`beam_diagnostic_adapters.py` conhece contratos históricos específicos. `validar_diagnostico_vigas.py` vincula os fixtures a vigas/pavimento/fonte/SHA256. Não usar busca indiscriminada por qualquer status na árvore: alternativas, modelos contextuais e históricos substituídos não equivalem ao detalhamento original vigente. Estados originais continuam nas evidências e nos arquivos-fonte imutáveis.

## Agregação e disponibilidade

Ordem governante: FAIL, INCONCLUSIVE, REQUIRES_ENGINEERING_REVIEW, PASS. NOT_APPLICABLE somente com evidência; módulo ausente produz INCONCLUSIVE/NOT_EXECUTED. Cobertura incompleta adiciona uma pendência de escopo mesmo quando os controles executados atendem. Revisão de engenharia não constitui falha normativa. Falha comprovada não apaga pendências.

A impossibilidade geométrica de ancoragem reta em uma peça com dobra documentada é uma observação para escolha do modo, não uma segunda falha governante da peça dobrada. Preservar seu FAIL original com `governing=false`, `role=MODE_SELECTION_OBSERVATION` e evidência do modo VERTICAL_BEND. A dobra e resistência curva permanecem controles independentes. O relatório identifica explicitamente essas observações.

`beam_checks_approval` é limitado às disciplinas/escopos declarados e jamais representa declaração de segurança global da estrutura. `structural_safety_declaration`, `selected_solution` e `detailing_optimization` são null.

## Ocorrências e relações

Cada FAIL, INCONCLUSIVE ou REQUIRES_ENGINEERING_REVIEW gera ocorrência estruturada. As listas proven_nonconformities, pending_occurrences e engineering_review_occurrences permanecem distintas. FAIL de observação de modo não integra proven_nonconformities. Categorias descrevem grandezas e elementos envolvidos, sem determinar solução.

ID determinístico: pavimento + viga + disciplina + caminho/escopo da fonte + ID lógico do controle; valores, ordem da lista e SHA256 não definem a identidade. Duplicação é rejeitada. SHA256 acompanha a fonte como versão documental. IDs lógicos precisam permanecer estáveis nos adaptadores; novas convenções exigem versão explícita.

`provided_minus_required` somente para escalares explicitamente comparáveis na mesma unidade; `comparison` indica o sentido. Margem positiva de espaçamento máximo não significa atendimento: o sentido é provided_le_required. Não calcular diferenças entre dicionários, unidades distintas ou campos sem semântica confirmada.

Relações são evidências de mesma marca ou sobreposição física comprovada no mesmo vão/sistema. Não fundem ocorrências, não relacionam apenas por proximidade e não afirmam que uma correção única resolveria ambas. O futuro módulo recebe todas as verificações, inclusive PASS, para avaliar efeitos de uma alteração; nenhuma proposta é executada aqui.

## Validação real e limites

Reprodução: `py -3.11 -B analises/pranchas/validar_diagnostico_vigas.py`. Gera cinco JSONs próprios e cinco relatórios V501/V516/V517/V536/V565, sem alterar os goldens. Casos não possuem necessariamente todas as disciplinas executadas; ausência não comprova inaplicabilidade. A planta de apoios indiretos permanece pendente por decisão anterior do engenheiro.

A leitura de novos contratos exige adaptador explícito e testes; não há parser universal para resultados arbitrários. O piso dos fixtures é vinculado ao diretório TQS documentado. Geometria transversal, ancoragem curva, interferências e inventário de suspensão podem permanecer pendentes. Relatórios históricos antigos que dizem apoio direito não implementado são antecedentes preservados: o JSON integrado atualizado inclui esse apoio, conforme generalização posterior. Não modificar silenciosamente esse histórico nem usar suas limitações antigas para sobrescrever o resultado atual.
