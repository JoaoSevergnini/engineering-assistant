# Proposta de fluxo de ATP de vigas por pavimento

Registro de 16/10/2026. Base: trabalho do S07 e orientações de João. Proposta para discussão; não altera a skill ativa, os motores resistentes nem as premissas de outros projetos.

O principal ganho de prazo é estabilizar as entradas e a associação física antes dos cálculos em lote. Reduzir verificações necessárias não resolve o retrabalho causado por entradas incorretas. O histórico permite identificar causas; não foi medida a duração de cada atividade, portanto não se estima uma economia percentual de tempo.

## Recapitulação do S07

| Etapa realizada | Resultado e aprendizado |
|---|---|
| Leitura do contexto, formas e detalhamentos | Inventário V1–V50 e delimitação dos controles. Forma de blocos7201 tornou-se necessária para interpretar faixas e apoios. |
| Correspondência entre projeto e TQS | Nomes inicialmente divergentes exigiram associação por apoios e posição. A atualização do modelo resolveu parte do problema; V24 ainda contém um trecho do modeloV23. |
| Primeiras verificações de seção | Ajudaram a localizar insuficiências, mas usaram premissas e composições que depois precisaram ser corrigidas. Não substituíram a revisão física por região. |
| Definição dos critérios de apresentação e cálculo | Concretopy oficial; solicitações características em tf/tf·m; resistências equivalentes Rd/γf; barras pertinentes, cobrimento e d explícitos. |
| Conciliação de etapas, níveis e apoios | Exclusão autorizada das barras do topo da primeira concretagem; C35 uniforme como simplificação específica; faces de blocos quando interceptantes; pilares nos apoios daV15 com blocos abaixo da viga. |
| Cortante e suspensão | Faixas reais, estribos externos, origem dos balanços, sentido da transferência e parcela complementar do tirante passaram a ser tratados explicitamente. |
| Consolidação do relatório | Fichas por viga, resultados oficiais e pendências identificadas. A revisão dos negativos eliminou a unificação indevida dos dois lados:190 consultas,45 solicitações corrigidas e14 extremidades com resultado resistente alterado em C35. |

O relatório atual reúne resultados de todas as vigas, mas não encerra toda aATP: comparação integral de cotas e determinados controles locais permanecem abertos. A qualidade da apresentação e o encerramento técnico devem ter critérios distintos.

## O que é indispensável e o que pode ser reduzido

| Indispensável | Retrabalho dispensável ou condicionado |
|---|---|
| Inventário completo e revisões identificadas | Reabrir e extrair integralmente documentos que não mudaram. |
| Associação forma–detalhamento–TQS por identidade física | Usar igualdade de nomes como única prova de correspondência. |
| Seção, níveis, apoios e limites das regiões relevantes | Tratar a soma das faixas de estribos como a própria geometria da viga. |
| Marcas, bitolas, camadas, função das barras e d rastreável | Solicitar altura de barra que já foi expressamente excluída do cálculo. |
| Origem, unidade, natureza e posição dos esforços | Transcrição manual extensa quando a listagem pode ser extraída e conferida. |
| Máximo negativo de cada lado individualmente | Unificar demandas em um pilar e depois repetir a maior nos dois lados. |
| Resistência oficial e armadura mínima, separadas | Uma calculadora resistente alternativa para preencher todas as linhas do relatório oficial. Conferências independentes representativas continuam úteis. |
| Cortante nas faixas reais, biela, área e espaçamentos | Repetir a falha de cobertura medida até a face errada. Redução de cortante não é automática. |
| Suspensão com ligação, reação e distribuição comprovadas | Aprovar a ligação porque 75% atende e deixar sem comprovação a parcela restante. |
| Pendências localizadas e controle da cobertura da revisão | Emitir um PDF a cada dúvida ou reenviar perguntas já respondidas. |

Para o mesmo escopo do S07, ancoragem longitudinal, escalonamento, torção, ELS, otimização e verificação especial de vigas-parede não devem ser acrescentados automaticamente. São ampliações de escopo; sua exclusão limita a conclusão e não significa que sejam dispensáveis em uma verificação estrutural completa. O funcionamento das peças que fornecem o próprio estribo considerado continua relevante para cortante/suspensão.

Não é necessário calcular dois fck por padrão. Usar o material aplicável ou a simplificação autorizada; cenários adicionais apenas quando uma incerteza ou decisão justificar. Também não se devem dispensar controles físicos porque uma conta conservadora de resistência atende.

## Fluxo proposto para o próximo pavimento

| Passo | Trabalho | Condição para avançar |
|---|---|---|
| 1. Escopo e pacote de entrada | Contexto, edição normativa, formas, detalhes, apoios/blocos quando pertinentes, TQS e exclusões. Preservar uma cópia das revisões recebidas. | Documentos e critérios identificados; faltas iniciais localizadas. |
| 2. Cadastro físico do pavimento | Inventário nas duas direções; vigas por apoios e posição; vãos, seções, níveis, faces, transições e eixo de referência. Associar trechos TQS. | Cada região necessária ao controle tem identidade e geometria demonstradas ou pendência específica. |
| 3. Leitura das armaduras | Marcas e função; inferior/superior; camadas; comprimentos e mudanças de composição; estribos, ramos e faixas. Separar desenho original de anotações. | Entrada resistente coerente com a região; conflitos reconciliados ou explicitados. |
| 4. Conferência das entradas antes do lote | Examinar exemplos representativos das situações existentes: seção usual, camadas, apoio contínuo com valores diferentes dos dois lados, mudança de altura e apoio indireto. Conferir conversões e d. | Extração e associação corretas. Isso verifica a aplicação do motor; não ajusta o motor para reproduzir um número escolhido. |
| 5. Execução por dependência | Flexão positiva e negativa/mínimos, cortante e suspensão. Usar os verificadores existentes; bloquear apenas os controles dependentes de informação não resolvida. | Resultado por região e por controle, com fonte. Alteração de entrada reabre somente os controles afetados. |
| 6. Cobertura e emissão | Conferir se todas as vigas, regiões, lados de apoio, faixas e ligações do escopo têm resultado ou pendência. Gerar quadro, fichas e lista de decisões. | Nenhuma omissão oculta. Trabalho do assistente não concluído aparece como tal. |

Essa sequência é por dependência, não uma exigência de esperar a leitura de todo o pavimento para iniciar qualquer cálculo. Uma viga com entradas completas pode avançar enquanto outra aguarda decisão.

## Regras que precisam estar resolvidas cedo

1. Hierarquia documental em conflitos entre elevação, marcas, cortes e tabela. A preferência aprovada no S07 não deve ser transferida silenciosamente para um novo projeto.
2. Materiais, cobrimento, agregados e vibrador; etapas de concretagem e barras consideradas na seção final. Buscar primeiro nos documentos e no contexto.
3. Origem dos esforços, coeficientes demonstrados e permissões para usar seções documentais diferentes do modelo.
4. Correspondência física, origens de balanços e faces de apoio. Fundações só são necessárias quando interferirem na região estudada.
5. Reações por caso de gravidade/vento quando necessárias para esclarecer o sentido da transferência. A interpretação de João auxilia a classificação; sinal isolado não substitui a avaliação do vínculo físico.
6. Critérios para situações especiais e itens reservados a João. Perguntas devem informar elemento, dado contraditório, evidência e efeito na conclusão.

## Como incorporar ao assistente

| Camada | Conteúdo |
|---|---|
| Perfil permanente | Unidades/base, origem oficial Concretopy e orientação de negativos por lado, já estabelecidas. |
| Skill existente | Sequência de ATP, dados mínimos por controle, tratamento de pendências, cobertura e padrão de conclusão. Reutilizar reinforcement-review; evitar uma segunda skill concorrente. |
| Contexto do projeto | fck adotado, concretagens, precedência documental, decisões sobre barras/apoios e exclusões. |
| Ferramentas | Extração, cadastro físico, consultas locais, chamadas oficiais e emissão. Reutilizar o fluxo operacional de pavimento existente. |

Há um ponto de implementação real a resolver antes de chamar o processo de integrado: no S07, as verificações de seção foram arquivadas separadamente, enquanto a auditoria do integrador permaneceu inconclusiva e seus controles aparecem como não executados. A integração atual não demonstra a conclusão dessas chamadas. É necessário conectar as entradas físicas e os resultados válidos ao fluxo de pavimento, ou registrar claramente execução externa e suas dependências, preservando as guardas. Não preencher entradas fictícias para obter aprovação.

A prioridade de desenvolvimento é um cadastro de entradas e decisões com dependências, seguido de uma execução única e reproduzível dos controles autorizados. Evitar scripts sucessivos que alteram o mesmo arquivo e podem restaurar premissas antigas ou apagar resultados complementares. Uma mudança de texto/unidade não deve disparar novo cálculo; mudança de armadura, seção, material, d ou solicitação deve invalidar os resultados dependentes.

A primeira validação do fluxo deve reutilizar os casos documentados do S07:V43/P723, associaçãoV23/V24, transiçõesV49/V50, faixas junto aos blocos, seleção de armadura externa e ligações de suspensão com 75/25. Não transformar simplificações particulares desses exemplos em regras gerais.

## Padrão proposto do relatório

- Quadro por viga com geometria, positiva, negativa, mínimo, cortante e suspensão.
- Ficha com região/apoio/lado, seção, armadura, d, solicitação, resistência/taxa exigida, resultado e origem.
- Legenda: longitudinal e transversal por extenso; abreviações explicadas uma vez.
- Resultado técnico separado da execução:atende,não atende,inconclusivo,não se aplica; e executado,a concluir pelo assistente,aguarda informação/decisão.
- A expressão“área suficiente” deve indicar qual parcela foi comprovada. Se faltar funcionamento das peças ou complemento do tirante, a ligação continua inconclusiva.
- Pendência com localização, informação/verificação faltante, motivo, efeito e responsável. Falta de leitura não é ausência na prancha.
- Um relatório vigente e histórico das revisões. Emitir alterações relevantes, sem multiplicar PDFs de trabalho.

O fechamento deve ter dois registros: cobertura dos controles solicitados e atendimento técnico. UmaATP pode estar concluída com falhas e pendências documentais precisamente identificadas; não pode ser declarada concluída enquanto houver leituras ou cálculos autorizados ainda não executados pelo assistente.

## Próxima aplicação

Usar o prompt separado,prompt_atp_novo_pavimento.md. O prompt informa o projeto,os caminhos e as exceções. As regras permanentes e a sequência devem ficar na skill; não depender da repetição de um texto longo em cada pedido.

Referências consultadas:reinforcement-review/SKILL.md;references/floor-operational-review.md;references/documentary-physical-preflight.md;profile/force-presentation.md;auditoria_floor_review.json;revisao_negativos_por_lado.json e pendencias_verificacao.md da rodada05 do S07.


## Atualização solicitada por João — seleção antes da emissão

Adotar a separação em três etapas:verificar inconformidades;avaliar os itens a incorporar;redigir apontamentos e emitir. Incluir seção própria de geometria forma×detalhamento,índices de utilização corretamente definidos e memória de suspensão comVk,comprimento e parcelas de aço. O percentual de utilização de momento não é percentual de aço faltante. Especificação detalhada emespecificacao_relatorio_selecao.md. Demonstração interativa não equivale à seleção completa doS07 nem à emissão automática.


## Preferências encaminhadas pela seleção interativa — 16/10/2026

Selecionadas as seis seções: geometria forma×detalhamento; flexão positiva e mínimos; flexão negativa por lado e mínimos; cortante e espaçamentos; suspensão com esforços, extensão e parcelas; pendências para decisão.

Os quatro exemplos também permanecem selecionados: divergência de altura daV42; resistência negativa daV43/P723; armadura de cortante daV18; emenda/ancoragem das peças de estribo na ligaçãoV31–V12. São exemplos, não o inventário completo doS07. Nenhuma observação adicional foi enviada.

Aplicação no fluxo:1)verificar e registrar os resultados técnicos;2)apresentar a lista completa de seções e apontamentos para seleção;3)redigir os apontamentos e construir a emissão a partir da seleção completa enviada. Esta escolha de demonstração não autoriza emitir um relatório global reduzido aos quatro exemplos. Resultados técnicos e itens não emitidos permanecem preservados; exclusões da emissão são registradas separadamente.

Registro estruturado:preferencias_relatorio_confirmadas.json. Os índices de utilização, a seção própria de geometria e as parcelas de suspensão seguem a especificação de apresentação já proposta. A proposta continua separada da skill ativa e do gerador automático dePDF.
