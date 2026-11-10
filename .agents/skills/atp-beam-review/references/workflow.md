# Fluxo da ATP de vigas por etapas

Versão para ATP do [workflow incremental geral](../../reinforcement-review/references/incremental-floor-workflow.md). Para ATP, ler este arquivo em vez do geral. Este fluxo organiza o trabalho; não altera métodos resistentes, requisitos normativos ou escopo. Usar os contratos e a entrada `floor_review.py` existentes; não criar outro motor apenas para atender ao fluxo.

## Registros do pavimento

| Registro | Conteúdo mínimo |
|---|---|
| `premissas.json` | Escopo pedido e exclusões; norma e edição; materiais, coeficientes, cobrimento, origem das seções; decisões com origem, alcance e data. Distinguir decisão de João de adoção de engenharia. |
| `indice_controles.json` | Por controle: ID estável (pavimento/viga/trecho/controle; ligação apoiada→receptora), estado de execução, conclusão técnica, entrada e resultado vigentes, versão do motor/adaptador, dependências. |
| Fila de exceções (no índice ou separada) | Região/ligação, obstáculo, informação ou método necessário, próxima ação, responsável. |
| `retomada.md` | Até uma página, sobrescrita: totais atuais, último lote, próxima ação, caminhos dos registros. Histórico extenso vai para arquivo separado. |

**Estados de execução** (não são conclusão): não executado; liberado aguardando execução; impedimento documental; impedimento de método; aguardando decisão; executado. Inaplicabilidade exige comprovação. Uma viga com algum cálculo não é uma viga integralmente verificada.

Resultados substituídos permanecem como histórico com indicação do substituto; o índice indica qual prevalece, sem reescrever arquivos brutos.

## Etapa 0 — Preparação

1. Registrar premissas e decisões em `premissas.json`. Não transportar decisões de outro pavimento. Aplicar os [critérios padrão](default-criteria.md) e apresentar a João as premissas do §1 com o valor padrão, junto com a primeira rodada de dúvidas. Registrar cada critério aplicado com a origem "critério padrão".
   Assinalar no inventário os vãos com troca de seção dentro do vão (critérios padrão §6.7).
2. Copiar as revisões recebidas para `00_entrada/` e registrar hashes. Conferir identificação, revisão e abrangência de PDF e DXF correspondentes antes de tratá-los como o mesmo documento; hash identifica o arquivo, não prova equivalência entre formatos.
3. **Extração:** DXF como fonte principal de textos, marcas, quantidades, bitolas, entidades e coordenadas, extraído uma vez e reutilizado enquanto fonte e extrator forem os mesmos. Distinguir cota explícita de medida geométrica; comprovar unidade, escala e identidade. Coordenada precisa não prova a função da entidade. PDF para conferência visual dirigida (cortes, chamadas, símbolos, regiões ambíguas) e base das pranchas anotadas. Se o DXF estiver incompleto ou inadequado, usar o PDF e registrar a limitação. Divergência entre formatos é conflito até conciliação; a prioridade operacional do DXF não lhe dá precedência técnica.
4. **Inventário:** vigas, pranchas, formas, fontes TQS, vãos e encontros candidatos de suspensão, nas duas direções. Total de encontros não é total de vigas.
5. **Cadastro físico:** associar vigas por apoios e posição (nome igual não prova correspondência). Por região: seção, níveis, faces, origem do eixo, faixas, ocorrências de barras, camadas e interfaces. Classificar geometrias: constantes, mudanças de seção/nível, balanços, especiais. Verificar a identidade do próprio elemento antes de atribuir curva ou detalhe vizinho. Guardar a associação entre entidade DXF, região do PDF e extração consolidada.
6. **Liberação por controle:** resolver apenas os dados de que cada controle depende. Região ambígua bloqueia só os controles dependentes, não o pavimento.
7. **Piloto:** validar um lote pequeno que represente as famílias presentes (seção usual, camadas, apoio contínuo com valores diferentes nos dois lados, mudança de altura, apoio indireto), conferindo extração, unidades, coordenadas, camadas, d e saída. O piloto verifica a aplicação do motor; não ajusta o motor para reproduzir um número escolhido.

**Saída:** inventário completo, controles classificados entre liberados e dependentes, piloto validado, índice e retomada atualizados. Não repetir interpretações físicas em cada chamada de cálculo: referenciar o registro comprovado.

## Etapa 1 — Verificação

1. Executar os controles liberados em lote pela entrada existente, com um script parametrizado que lê `premissas.json` e atualiza o índice. Automatizar extração, máximos por domínio, chamadas ao Concretopy e comparações. Cada viga conserva suas próprias entradas; sem transferir seções, armaduras ou esforços por semelhança.
2. Reservar a leitura de engenharia para inconsistências, insuficiências e casos especiais. Compartilhar procedimentos entre famílias, não conclusões sem evidência própria.
3. Para cada exceção, registrar o obstáculo e fazer consulta dirigida à fonte. Sem base para concluir, registrar o próximo dado ou método necessário e seguir com os demais controles. Reabrir só com nova evidência, decisão ou método.
4. Agrupar perguntas que dependem da mesma decisão de João, com alcance e efeito; não perguntar de novo o que já foi decidido. Continuar o trabalho independente enquanto a decisão estiver pendente.
5. **Suspensão:** completar o inventário de encontros e sua associação como tarefa explícita. Distinguir associação ainda não feita, contato ambíguo, reação/critério pendente e cálculo executado. Manter cortante independente e suspensão separados, com combinação rastreável.
6. Consolidar o diagnóstico por viga a partir dos resultados existentes.
7. **Cobertura:** reconciliar inventário esperado × controles executados × inaplicáveis comprovados × pendências, por região e por ligação. Não deixar entradas liberadas esquecidas na fila.

**Saída:** todo controle do escopo executado ou com pendência objetiva justificada; registro técnico de inconformidades com identificação estável, localização, dados, fonte, evidência, conclusão e limitações. Ainda não redigir a versão final nem anotar pranchas.

## Etapa 2 — Seleção

Gerar a lista completa (`selecao_etapa2.json`) e a entrega padrão com `scripts/emitir_etapa2.py <pasta>`: relatório PDF das verificações de todas as vigas, com checkbox "Rel." e comentário por apontamento, e pranchas anotadas com quadros de solicitação característica / resistência equivalente, conforme [reporting](reporting.md) ("Entrega padrão da etapa 2"). Conferir visualmente amostras do relatório e das pranchas (posição dos marcadores, quadros legíveis, campos interativos) antes de entregar. Ao receber o PDF preenchido, ler os campos com `--ler` e registrar com `--registrar` somente após o envio expresso de João. A seleção altera a emissão, não a conclusão técnica. Encerrar a sessão após o envio da seleção.

## Etapa 3 — Emissão

Consumir a seleção expressamente enviada, a versão dos resultados e as fontes. Definir o padrão de entrega a partir da referência indicada por João e validar uma ficha piloto (colunas, unidades, estados, campos) antes de gerar todas as páginas. Gerar relatório, fichas e pranchas anotadas (em cópias) da mesma versão dos resultados. QA resistente e QA documental são separados; após mudança só gráfica, conferir os artefatos afetados sem recalcular e sem regenerar PDFs já conferidos e inalterados.

Não anunciar encerramento integral com trabalho ainda não executado. Se a emissão com pendências for autorizada, distinguir trabalho faltante do assistente, impedimento documental, método e decisão do engenheiro.

## Recalcular apenas o afetado

Antes de repetir uma execução, identificar o que mudou. Se nada aplicável mudou e o resultado existente é válido, reutilizá-lo. Mudanças invalidam inclusive resultados antes favoráveis.

| Mudança | Ação |
|---|---|
| Armadura, camada ou altura útil | Refazer os controles da composição/região; verificar reflexos em cortante e suspensão |
| Seção, nível, face ou origem | Reavaliar mapeamento e todos os controles dependentes, inclusive encontros entre elementos afetados |
| Série de esforços ou coeficientes | Invalidar consultas e comparações dependentes; preservar série e natureza originais |
| Regra comum, motor ou adaptador | Localizar todos os controles atingidos, rodar a regressão pertinente e refazer esse conjunto |
| Texto, colunas ou apresentação | Reemitir os artefatos afetados, sem recálculo resistente |

Registrar a justificativa da reexecução junto ao resultado. Economia de tokens não justifica ignorar controles atingidos. Cache e invalidação automática não estão implementados: manter a invalidação explícita no índice.

## Ao encerrar cada etapa

Atualizar índice e `retomada.md`; registrar vigas e controles executados, pendências por motivo, scripts criados, reexecuções e motivos, decisões novas e próxima ação. Só apresentar consumo de tokens quando houver medição.
