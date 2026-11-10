# Revisão de pavimentos com execução incremental

Aplicar ao iniciar ou retomar pavimentos com várias vigas. Este procedimento organiza o trabalho; não altera métodos resistentes, requisitos normativos ou escopo. Complementa [floor-operational-review](floor-operational-review.md). Usar os contratos e a entrada `floor_review.py` existentes; não criar outro motor ou uma arquitetura nova apenas para atender a este procedimento.

## 1. Preparação e critérios de liberação

Antes do primeiro lote resistente:

- Registrar no contexto do projeto os controles pedidos, exclusões, decisões vigentes, materiais, coeficientes e origem das seções. Distinguir decisão do usuário de adoção de engenharia. Não transportar automaticamente decisões de outro pavimento (por exemplo, fck, pele, furos ou seção adotada).
- Inventariar vigas, pranchas, formas, fontes TQS, vãos e encontros candidatos de suspensão. Criar identificadores estáveis por pavimento/viga/trecho/controle e por ligação apoiada→receptora. Total de encontros não é total de vigas.
- Identificar versões dos arquivos, registrar hashes na ingestão e guardar extrações estruturadas com referência à entidade/linha/página. Reutilizar extrações enquanto a fonte e o extrator aplicáveis forem os mesmos. DXF para entidades e medidas documentadas; PDF para leitura visual e conciliação, conforme as ferramentas disponíveis.
- Classificar as geometrias próprias: constantes, mudanças de seção/nível, balanços e geometrias especiais. Verificar a identidade do próprio elemento antes de atribuir a ele uma curva ou detalhe vizinho.
- Conciliar e registrar, por região, seção, níveis, faces, origem do eixo, faixas, ocorrências de barras, camadas e interfaces relevantes. Antes de calcular, resolver apenas os dados dos quais aquele controle depende; uma região ambígua não bloqueia automaticamente todas as vigas.

**Saída da preparação:** inventário completo e controles classificados entre liberados e dependentes de esclarecimento/método. Não exigir que toda a geometria especial esteja resolvida para executar os trechos regulares liberados. Não repetir uma interpretação física em cada chamada de cálculo: referenciar seu registro comprovado.

### PDF e DXF correspondentes

Quando ambos forem fornecidos, conferir identificação, revisão e abrangência antes de tratá-los como representações do mesmo documento. Hashes identificam cada arquivo, mas não comprovam equivalência entre formatos.

- **DXF como fonte principal de extração:** textos, marcas, quantidades, bitolas, entidades e coordenadas. Extrair uma vez e reutilizar a base validada. Distinguir cotas explícitas de medidas geométricas; comprovar unidade, escala e identidade do elemento. Coordenada precisa não prova a função da entidade nem transforma um desenho esquemático em geometria física confirmada.
- **PDF como conferência visual:** examinar inicialmente as representações relevantes e consultar de forma dirigida cortes, chamadas, símbolos e regiões ambíguas ou conflitantes. Usá-lo também como base das pranchas anotadas. Não repetir uma extração completa pelo PDF quando a extração DXF estiver válida e suficiente.
- **Conflito ou perda de conteúdo:** registrar as duas evidências e resolver a divergência antes do controle dependente. A prioridade operacional do DXF não lhe dá precedência técnica automática sobre o PDF. Se o DXF estiver incompleto, ilegível ou inadequado à extração, usar o PDF como alternativa e identificar a limitação e a origem dos dados.
- **Esforços:** usar as fontes TQS próprias; não inferir solicitações da armadura desenhada em qualquer dos formatos.

Guardar a associação entre a entidade DXF, a região correspondente do PDF e a extração consolidada. Reabrir apenas as regiões afetadas por revisão, falha do extrator ou dúvida documentada; não exigir nova leitura visual integral a cada lote.

## 2. Base única de resultados e retomada curta

Manter no projeto um índice autoritativo para localizar o resultado vigente de cada controle. Reutilizar a matriz/manifesto já existentes quando adequados; os nomes abaixo são conceitos, não uma exigência de novos formatos.

| Registro | Conteúdo mínimo |
|---|---|
| Contexto e decisões | Escopo, critérios adotados, origem, alcance e data das decisões |
| Índice de controles | ID, estado de execução, conclusão técnica, entrada/resultado vigente e dependências |
| Fila de exceções | Região/ligação, motivo, informação ou método necessário, próxima ação |
| Estado de retomada | Totais atuais, último lote, próxima ação e caminhos dos registros acima |

Separar **execução** de **conclusão**: controle não executado, entrada liberada aguardando execução, impedimento documental, impedimento de método, aguardando decisão e executado não significam PASS/FAIL. Inaplicabilidade exige comprovação. Uma viga com algum cálculo não equivale a uma viga integralmente verificada.

Cada resultado vigente aponta para entradas, versão do motor/adaptador, critérios e fontes. Resultados substituídos permanecem históricos com indicação do substituto; não deixar o leitor escolher entre vários suplementos. Arquivos brutos não precisam ser fundidos nem reescritos: o índice resolve qual prevalece.

Ao concluir um lote ou receber uma decisão relevante, atualizar o índice e sobrescrever o resumo de retomada. Manter esse resumo curto, preferencialmente até uma página; histórico extenso fica em registro separado, sem concatená-lo repetidamente ao resumo. Na retomada, ler o resumo, o contexto e os registros dos controles seguintes. Buscar no histórico apenas a dúvida concreta que não esteja nesses registros. Não carregar JSONs brutos extensos no contexto quando uma consulta por ID ou um resumo determinístico for suficiente.

## 3. Cálculo em lote e revisão das exceções

1. Validar um lote piloto pequeno que represente as famílias realmente presentes, verificando extração, unidades, coordenadas, camadas e saída. Reutilizar ferramentas validadas; testar adaptadores novos antes de ampliar sua execução.
2. Executar os controles regulares liberados em lotes pela entrada existente. Automatizar extração, máximos por domínio, chamadas ao Concretopy, comparações e atualização do índice. Cada viga conserva suas próprias entradas; sem transferência automática de seções, armaduras ou esforços por semelhança.
3. Reservar a leitura de engenharia para inconsistências, insuficiências e casos especiais. Compartilhar procedimentos entre famílias, sem compartilhar conclusões sem evidência própria.
4. Para uma exceção, registrar o obstáculo específico e fazer a consulta dirigida à fonte correspondente. Se continuar sem base para concluir, registrar o próximo dado/método necessário e avançar nos demais controles. Reabrir quando houver nova evidência, decisão ou método, não apenas porque começou outro lote. Isso não autoriza abandonar trabalho executável ou classificar associação ainda não feita como falta de informação do projeto.
5. Agrupar perguntas que dependem da mesma decisão de João, indicando alcance e efeito. Não perguntar novamente algo já decidido. Continuar o trabalho independente enquanto a decisão estiver pendente.

Na suspensão, completar o inventário de encontros e sua associação como tarefa explícita. Distinguir associação ainda não realizada, contato ambíguo, reação/critério pendente e cálculo executado. Manter resultados do cortante independente e da suspensão separados, com combinação rastreável. Inventário, direção de transferência e distribuição física devem estar comprovados antes do cálculo dependente.

## 4. Recalcular apenas o que foi afetado

Antes de repetir uma execução, identificar o que mudou: fonte, geometria, armadura/camadas, esforços, critério, motor ou adaptador. Se nada aplicável mudou e a verificação existente é válida, reutilizá-la. Mudanças devem invalidar inclusive resultados anteriormente favoráveis.

| Mudança | Ação |
|---|---|
| Armadura, camada ou altura útil | Refazer os controles dependentes daquela composição/região; verificar reflexos em cortante e suspensão |
| Seção, nível, face ou origem | Reavaliar mapeamento e todos os controles dependentes, incluindo encontros entre elementos afetados |
| Série de esforços ou coeficientes | Invalidar as consultas/comparações dependentes; preservar a série e a natureza originais |
| Regra comum, motor ou defeito de adaptação | Localizar todos os controles atingidos, executar a regressão pertinente e refazer esse conjunto |
| Texto, colunas ou apresentação | Reemitir os artefatos afetados a partir dos resultados existentes; sem recálculo resistente |

Após correção, executar a verificação dirigida e a regressão exigida pelo alcance da mudança. Não repetir toda a auditoria ou todo o pavimento sem dependência demonstrada. Uma alteração comum pode justificar revisão ampla; economia de tokens não justifica ignorar controles atingidos.

Registrar a justificativa de uma reexecução junto ao resultado. Usar hashes/assinaturas de entrada e dependências quando o pipeline já os oferecer; na ausência dessa automação, manter a invalidação explícita no índice. Não afirmar que cache ou invalidação automática estão implementados apenas porque este procedimento os descreve.

## 5. Fechamento e emissão sem retrabalho

Antes da emissão técnica, reconciliar inventário esperado × controles executados × inaplicáveis comprovados × pendências, por região e por ligação. Conferir que não ficaram entradas liberadas esquecidas na fila. Não anunciar encerramento integral com trabalho ainda não executado; quando a emissão com pendências for autorizada, distinguir trabalho faltante do auxiliar, impedimento documental, método e decisão do engenheiro.

Definir o padrão de entrega cedo, a partir da referência indicada por João. Verificar colunas, unidades, estados e campos necessários com uma ficha piloto antes de gerar todas as páginas. Quando houver referência anterior, ler o gerador/estrutura e uma amostra visual; não presumir que apenas a paleta de cores reproduz o padrão. Confirmar os dados disponíveis nas colunas antes da emissão, sem inventar valores para preencher campos.

Gerar relatório, pranchas e rastreabilidade da mesma versão dos resultados. Seleção editorial de apontamentos não altera seu estado técnico. Se houver checkboxes, usar IDs estáveis, estados iniciais explícitos e validar campos interativos conforme a skill de PDF; não presumir sua existência apenas pela aparência gráfica.

Separar QA resistente de QA documental. Após mudança somente gráfica, verificar os documentos/campos/links afetados e a preservação dos resultados. Renderizar e conferir os artefatos conforme a skill do formato; não regenerar PDFs já conferidos e inalterados apenas para repacotar o ZIP. Preservar revisões entregues e verificar a integridade do pacote final.

## 6. Controle do esforço do processo

Registrar por lote: quantidade esperada/executada, pendências por motivo, reexecuções e seus motivos, decisões novas e próxima ação. Usar esses registros para localizar retrabalho recorrente. Só apresentar consumo de tokens por etapa quando houver medição disponível; sem telemetria, identificar a estimativa como qualitativa e não prometer percentuais de economia.

Se houver delegação já autorizada, atribuir IDs e entregáveis delimitados, com um único responsável por consolidar o índice; agentes devem devolver resultados e exceções compactos, não copiar todo o histórico. Este procedimento não exige subagentes.
