# Contratos do incremento 1A

Código em tools/slab_review; biblioteca padrão, Python 3.10+. Dataclasses frozen
e coleções tuple preservam os registros quando usados conforme a tipagem.
Os dados do empreendimento permanecem em analises/<projeto>; o exemplo fornecido
é demonstração de comportamento, não cadastro válido para cálculo.

## Estrutura

| Módulo | Contratos |
|---|---|
| common.py | Document, Evidence, EngineerDecision, Criterion e enums |
| models.py | GeometryReference, Slab, ThicknessRegion, ReinforcementOccurrence, GridLine |
| review.py | Dependency, DependencyAssessment, Control e operações de revisão |
| example_s07.py | build_example e CLI de demonstração |
| test_contracts.py | testes independentes dos arquivos originais |

Document guarda caminho sem abrir o arquivo. Revisão e SHA-256 são opcionais;
hash informado precisa de 64 caracteres hexadecimais. O cadastro não verifica
se a fonte existe ou representa a última revisão.

Evidence guarda document_id, página 1-based/localização opcionais, observed,
interpreted, unidade, método e confirmação original. Valores são escalares;
geometria é uma referência. None significa desconhecido; zero e False não são
substituídos por ausência. effective_value e effective_confirmation apresentam
a interpretação vigente com as decisões humanas, mantendo os campos originais.

Uma evidência sem documento exige decisão humana atribuída. Dado manual pode
ter observed=None e uma decisão PROVIDE. Autor, instante ISO com fuso e
justificativa são obrigatórios. As decisões não provam que o autor foi
autenticado por um serviço; são registros fornecidos pelo operador.

Slab usa thickness_cm uniforme OU thickness_regions, sem dividir artificialmente
a identidade da laje. A geometria e os níveis podem permanecer desconhecidos.
top_level_m refere-se à face superior; nenhum cálculo de nível foi implementado.

ReinforcementOccurrence guarda marca, direção declarada (ou desconhecida),
bitola em mm, espaçamento em cm, fonte, geometria e confirmação.
GridLine recebe ID persistente, direção, referência geométrica, fonte e referência
opcional aos momentos. Não resolve identidade automaticamente e não interpreta
o arquivo de momentos.

IDs são referências explícitas. O chamador mantém seus catálogos e garante sua
existência/unicidade entre registros. Não há importador JSON, reconciliador de
revisões ou validador global de referências neste incremento.

## Controles e dependências

Cada Control possui objeto, critério com origem/referência/edição, dependências,
execução, resultado técnico, IDs de evidências, pendências e notas do engenheiro.
source_consulted de Criterion é declaração do operador, não consulta automática.

| Execução | Resultados admitidos |
|---|---|
| NOT_EXECUTED | NOT_EVALUATED |
| PARTIALLY_EXECUTED | NOT_EVALUATED, INCONCLUSIVE, FAIL |
| EXECUTED_INCONCLUSIVE | INCONCLUSIVE |
| EXECUTED_COMPLETE | PASS, FAIL, NOT_APPLICABLE |

PASS/FAIL requer evidência. Inconclusivo e inaplicável exigem motivo.
Controle completo não mantém pendência bloqueante. FAIL parcial conserva uma
falha comprovada enquanto outra parcela do mesmo controle segue pendente.
Uma suspeita por extração incompleta deve ser INCONCLUSIVE, com motivo.

assess_dependencies(control, availability) recebe mapa de chave para bool.
Chave ausente é indisponível. ready=True significa apenas entradas liberadas.
A disponibilidade é decisão explícita do chamador; não é inferida de valores
preenchidos, da confirmação de outro campo ou de outro controle.

record_outcome registra resultado fornecido pelo chamador e devolve novo Control.
Bloqueia PASS/FAIL completo com dependências ausentes. NOT_APPLICABLE exige
justificativa própria; não é deduzido de documento faltante. Para controle
bloqueado ainda não executado, conservar NOT_EXECUTED/NOT_EVALUATED, registrar
pending e consultar DependencyAssessment.missing.

review_evidence acrescenta CONFIRM/CORRECT/PROVIDE, rejeitando alvo errado,
ID de decisão repetido ou ação incompatível. review_finding acrescenta
ACCEPT/REJECT sem reescrever resultado técnico ou execução. A última decisão
representa a disposição atual do apontamento; as anteriores permanecem.

Uma correção não propaga automaticamente alterações para Slab/Occurrence/GridLine
nem invalida resultados antigos. Atualizar explicitamente as entidades e reexaminar
somente controles dependentes. Retornar novo objeto preserva a versão anterior;
persistência, versionamento de resultados e conflitos entre revisores ficam para
incrementos posteriores.

## Exemplo e testes

Na raiz do repositório, sem dependências externas:

~~~powershell
python -B -m tools.slab_review.example_s07
python -B -m unittest discover -s tools/slab_review -p "test_*.py" -v
~~~

O exemplo imprime JSON em stdout e não grava arquivos. build_example retorna
dataclasses; to_data produz projeção JSON dos campos armazenados, incluindo fontes
e decisões. Propriedades calculadas (effective_value, effective_confirmation,
ready) são consultadas nos objetos Python.

A chamada N26/7308 e os nomes de documentos são representativos do S07.
A interpretação inicial 12.0 mm e as decisões atribuídas ao engenheiro fictício
são simuladas, não dados históricos nem confirmação de João. A laje e a linha de
grelha têm IDs DEMO e não afirmam associação estrutural real.

O confronto demonstrativo da bitola termina em PASS. Cobertura e flexão permanecem
não executadas por falta de contorno, espessura e diagrama. A rejeição de uma
alegação de ausência não altera esses estados. Nenhuma resistência ou conformidade
normativa é calculada.

## Uso no procedimento operacional 1B

O código e os contratos acima permanecem os do incremento 1A. O procedimento
assistido completo está em [review-workflow](review-workflow.md); a origem dos
critérios em [review-criteria](review-criteria.md) e a seleção humana de
apontamentos em [reporting](reporting.md). Nenhum desses documentos acrescenta
cálculos ou automatização aos contratos.

Após correção de uma informação utilizada em resultado, os controles e entregas
dependentes devem ficar fora do uso vigente até reavaliação. A propagação é
operacional, não automática: preservar a versão anterior, relacionar o dado aos
controles afetados e atualizar os consumidores explicitamente. Não alterar os
enums para representar histórico nem manter aprovação anterior como se validasse
a entrada corrigida. Controles comprovadamente independentes permanecem válidos.
