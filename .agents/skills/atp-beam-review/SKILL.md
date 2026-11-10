---
name: atp-beam-review
description: >-
  Conduz a Avaliação Técnica de Projeto (ATP) de vigas de concreto armado de
  terceiros, por pavimento: geometria forma×detalhamento, flexão positiva e
  negativa, armaduras mínimas, cortante, estribos e suspensão, com resultados
  oficiais do Concretopy, cobertura rastreável, seleção de apontamentos e
  emissão. Não usar para revisão interna, correção ou otimização de vigas do
  escritório (usar reinforcement-review).
---

# ATP de vigas

Esta skill organiza a ATP. As regras técnicas de cada controle ficam nas referências compartilhadas de [reinforcement-review](../reinforcement-review/SKILL.md) e não são repetidas aqui. Não ler o `SKILL.md` da reinforcement-review para executar uma ATP; ler apenas as referências indicadas na seção 4.

## 1. Escopo e critérios

**Escopo padrão:** comparar presença, seções, vãos, níveis e apoios entre forma e detalhamento; verificar flexão positiva e negativa, armaduras mínimas, cortante, espaçamentos dos estribos e suspensão.

**Somente se expressamente incluídos:** ancoragem longitudinal, escalonamento, torção, ELS, otimização e verificação especial de vigas-parede. A exclusão limita a conclusão; não significa que esses controles sejam dispensáveis numa verificação estrutural completa. O funcionamento das peças que fornecem o estribo considerado continua relevante para cortante e suspensão.

**Critérios:** a conclusão de conformidade se apoia em requisitos normativos e em requisitos documentados do projeto. Padrões internos do escritório, critérios do software, preferências e otimização entram apenas como observações identificadas, fora da conclusão. Se um resultado misturar requisitos e preferências sem permitir separação, manter a conclusão dependente inconclusiva e indicar o critério a esclarecer. Executar somente as etapas solicitadas e preservar os resultados originais das ferramentas e a origem dos critérios. Norma: a edição indicada no pedido ou no contexto do projeto; não inventar itens ou limites.

**Por projeto:** não transplantar simplificações ou decisões de outros projetos ou pavimentos (por exemplo, fck uniforme, exclusão de barras de etapa, hierarquia documental, seção adotada). Cada decisão vale para o escopo em que foi registrada. A exceção são os [critérios padrão](references/default-criteria.md), que João adotou para toda ATP: eles valem salvo instrução contrária, e as premissas do §1 desse arquivo são confirmadas na etapa 0.

## 2. Regras fixas

Resumo para não esquecer; o detalhe está nas referências da seção 4 e em [Apresentação de esforços](../../../profile/force-presentation.md).

- Resultado oficial de capacidade: **Concretopy**, com função, entradas e arquivo de resultado identificados. Conferências independentes ficam separadas e identificadas. Sem execução do motor, a verificação oficial está pendente.
- Apresentação: solicitações características em tf e tf·m; resistências como equivalente Rd/γf identificado; γf somente quando comprovado.
- Flexão positiva: somente a armadura inferior tracionada, sem contribuição das barras superiores.
- Flexão negativa: máximo negativo do TQS **de cada lado** do apoio, sem redução à face interna; os dois lados são verificados separadamente.
- Camadas: texto junto às barras prevalece sobre o corte; divergência é conflito. Sem indicação após exame da região, primeira camada como convenção identificada (`INFERRED_EXPLICIT_CONVENTION`). Verificar cabimento conjunto antes da resistência.
- Cortante: faixas reais da prancha, máximo |Vk| dentro da própria faixa, limites nas faces físicas do sólido de apoio (pilar, bloco, viga). Biela separada da taxa de armadura.
- Suspensão: somente com ligação e reação comprovadas; completar 100% da transferência (incluindo a parcela na viga apoiada, quando necessária); combinar cortante e suspensão sem somar o mínimo duas vezes.
- Esforços vêm do TQS; nunca inferir solicitação a partir da armadura desenhada. Usar os esforços TQS com as seções do detalhamento somente quando essa premissa estiver autorizada no contexto do projeto (é a premissa padrão a confirmar); divergências forma–detalhamento são registradas.
- Critérios padrão de João (mesa colaborante, mínimo sem demanda, porta-estribo, d do cortante, suspensão, tolerância editorial, geometria): [default-criteria](references/default-criteria.md).
- Estado de execução ≠ conclusão técnica. Controle não executado, pendente ou sem método não é PASS nem NOT_APPLICABLE. Trabalho ainda não feito pelo assistente não é falta de informação do projeto.

## 3. Fluxo em etapas

Executar cada etapa em uma **sessão própria**, retomando pelo resumo de retomada e pelo índice, não pelo histórico da conversa. Detalhes e condições de avanço em [workflow](references/workflow.md).

| Etapa | Trabalho | Encerra quando |
|---|---|---|
| 0. Preparação | Premissas e decisões, inventário, hashes, extração (DXF primeiro), cadastro físico, associação TQS, liberação por controle, piloto | Inventário completo; controles liberados ou com pendência específica; piloto validado |
| 1. Verificação | Cálculo em lote dos controles liberados, fila de exceções, diagnóstico por viga, cobertura técnica | Todo controle do escopo executado ou com pendência objetiva |
| 2. Seleção | Lista completa de apontamentos. Entrega padrão: relatório PDF das verificações de todas as vigas, com checkbox "Rel." e campo de comentário por apontamento, e pranchas anotadas com quadros Sk / Rk,eq ([reporting](references/reporting.md), "Entrega padrão da etapa 2") | Seleção enviada por João |
| 3. Emissão | Redação dos apontamentos selecionados, relatório, fichas e pranchas anotadas | Artefatos conferidos, gerados da mesma versão dos resultados |

Uma viga com entradas completas pode avançar enquanto outra aguarda decisão. Agrupar as dúvidas que dependem de João, cedo, após examinar as pranchas pertinentes.

## 4. Leitura por controle

Ler apenas o que o controle em execução exige. Arquivos grandes: ler as seções indicadas, não o arquivo inteiro. Em todo controle, aplicar também a seção correspondente dos [critérios padrão](references/default-criteria.md), que prevalecem na ATP sobre as referências compartilhadas quando divergem.

| Controle | Referências (em `../reinforcement-review/references/`) | Ferramentas |
|---|---|---|
| Preparação e geometria | [workflow](references/workflow.md); [floor-operational-review](../reinforcement-review/references/floor-operational-review.md); [documentary-physical-preflight](../reinforcement-review/references/documentary-physical-preflight.md); [contrato floor_review](../../../tools/reinforcement_checks/floor_review.md) (Manifesto, Invariantes); [convenções de prancha](../reinforcement-review/references/beam-drawing-convections.md) §2–5, §10–12, §15–17 | `floor_review.py` |
| Esforços TQS | [dados TQS](../reinforcement-review/references/tqs-beam-data.md): seções de esforços, interpolação e reações | `extrator_lst` |
| Flexão positiva, negativa e mínimas | [revisão longitudinal negativa](../reinforcement-review/references/negative-longitudinal-review.md): sequência, esforços e camadas, tipos de verificação, solicitação terminal, máximo no apoio | `floor_review` (adaptador de flexão), `longitudinal_review` |
| Cortante e estribos | [revisão de cortante](../reinforcement-review/references/shear-reinforcement-review.md) | `shear_diagram`, `shear_review`, `shear_coverage` |
| Suspensão | [apoios indiretos](../reinforcement-review/references/indirect-support-identification.md); [revisão de suspensão](../reinforcement-review/references/suspension-reinforcement-review.md); convenções de prancha §9 e §13 | `suspension_review` |
| Diagnóstico por viga | [diagnóstico consolidado](../reinforcement-review/references/beam-diagnostic.md) | `beam_diagnostic` |
| Relatório, seleção e emissão | [reporting](references/reporting.md) | skill de PDF |

Ampliações de escopo usam as referências correspondentes da reinforcement-review (ancoragem positiva e negativa, escalonamento, relações entre negativas), somente quando incluídas no pedido.

## 5. Economia de contexto e de chamadas

O custo de uma sessão cresce com o número de chamadas multiplicado pelo tamanho do contexto. Nos pavimentos 1PAV e 2PAV do S07 houve de 2.000 a 3.200 chamadas por pavimento, com contexto mediano de cerca de 220 mil tokens, e 162 e 548 scripts avulsos. Aplicar:

1. **Premissas uma vez:** materiais, coeficientes, cobrimento, origem das seções e decisões ficam no arquivo de premissas do pavimento; scripts leem esse arquivo. Não escrever fck, γ, cobrimento ou h no código de cada script.
2. **Lote, não script por viga:** um script parametrizado que percorre as vigas e atualiza o índice. Estender o script existente do pavimento em vez de criar variantes (`_v2`, `patch_`, `complementar_`).
3. **Saída curta:** no terminal, até cerca de 30 linhas (totais por estado e IDs das exceções); o detalhe vai para arquivo.
4. **Consulta dirigida:** não abrir JSON ou markdown grandes inteiros; consultar por ID com um script curto.
5. **Imagens sob demanda:** extrair do DXF; gerar e abrir recortes do PDF apenas para exceções e conferências dirigidas.
6. **Sessão por etapa:** encerrar a etapa atualizando o índice e o resumo de retomada (até uma página, sobrescrito). Não ramificar (fork) a conversa para trabalho em lote; agentes auxiliares recebem IDs e entradas e devolvem resultado compacto.
7. **Registrar o esforço:** ao fim de cada etapa, anotar vigas e controles executados, scripts criados, reexecuções e motivos, para comparar com o S07.

## 6. Arquivos

Conforme o `AGENTS.md` (seção 16), resultados de projeto não são versionados neste repositório. Enquanto a pasta do projeto não estiver definida, trabalhar em `analises/<projeto>_vigas_<pavimento>/`, fora do git, com esta organização:

```
00_entrada/            cópias das revisões recebidas e hashes
premissas.json         escopo, materiais, coeficientes, decisões (origem e data)
indice_controles.json  estado de execução, conclusão, resultado vigente, dependências
retomada.md            resumo de retomada (até uma página)
dados/                 extrações estruturadas
scripts/               scripts do pavimento (poucos e parametrizados)
resultados/            resultados brutos das ferramentas
emissao_Rxx/           artefatos emitidos por revisão
```

## 7. Iniciar uma nova ATP

Usar o [modelo de pedido](references/new-floor-prompt.md), que indica projeto, caminhos, exceções e a etapa da sessão.

## 8. Exclusões

- Não editar PDFs nem propor correções durante as etapas 0 e 1; a emissão autorizada é a etapa 3.
- Não otimizar, redesenhar ou selecionar armaduras.
- Não modificar Concretopy, motores resistentes ou contratos das ferramentas para atender a um caso.
- Pilares: [atp-column-review](../atp-column-review/SKILL.md). Lajes: [atp-slab-review](../atp-slab-review/SKILL.md). Revisão interna e correção de vigas: [reinforcement-review](../reinforcement-review/SKILL.md).
