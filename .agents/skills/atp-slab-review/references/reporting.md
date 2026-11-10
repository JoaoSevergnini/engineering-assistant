# Três entregáveis de ATP e revisão humana

## Documentos obrigatórios

| Documento | Finalidade | Referência final S07 1º pavimento |
|---|---|---|
| Pranchas gráficas de verificação | Comparação espacial resistência/solicitação e seleção editorial por região | [7309 POS H R02](../../../../analises/atp_s07_lajes_1pav/output/pdf/verificacoes_R02/ATP_S07_1PAV_7309_POS_H_Mr_Msol_R02.pdf) |
| Relatório de incompatibilidades e pendências | Fichas por prancha para conflitos confirmados, controles pendentes e pedidos de informação | [Incompatibilidades R01](../../../../analises/atp_s07_lajes_1pav/output/pdf/consolidado/ATP_S07_1PAV_incompatibilidades_pendencias_R01.pdf) |
| Relatório técnico complementar | Escopo, dados, decisões, métodos, cálculos, resultados e cobertura | [Relatório técnico R00](../../../../analises/atp_s07_lajes_1pav/output/pdf/consolidado/ATP_S07_1PAV_relatorio_armaduras_R00.pdf) |

Nenhum documento substitui os demais. Produzir o pacote preliminar com os
resultados disponíveis e explicitar campos/controles pendentes, sem esperar
automação perfeita. Sem dados para comparar, manter mapa/quadro de pendências
identificado, não inventar cálculo ou incompatibilidade. Registros estruturados
sustentam os PDFs, mas não substituem a entrega gráfica quando ela é possível.

A R02 governa a composição gráfica; não contém widgets de seleção. A adição
real desses campos está na [7309 R03](../../../../analises/atp_s07_lajes_1pav/output/pdf/verificacoes_R03/ATP_S07_1PAV_7309_POS_H_Mr_Msol_R03.pdf)
e em seu gerador. Preservar o layout R02 com a seleção editorial; não alegar que
a seleção já existia no arquivo R02. Ver reutilização, limites e QA em
[s07-1pav-deliverables](s07-1pav-deliverables.md).

## Conteúdo mínimo de cada PDF gráfico

| Item | Informação obrigatória |
|---|---|
| Base documental | Prancha original de armaduras, identificação, página e revisão; original preservado |
| Regiões | Delimitações, direção/face e ID único coerente entre mapa, quadro e dados |
| Armaduras | Bitola, espaçamento, As em cm²/m e marcas efetivamente calculadas; distinguir base, reforço, individual e composição comprovados, sem inferir função pela ordem da lista |
| Resistência | Valor calculado da região, base/unidade, função/resultado Concretopy e hipóteses pertinentes, ou pendência explícita |
| Indicador 1 | Média dos máximos do sinal relevante por linha de grelha distinta, recortada na região |
| Indicador 2 | Média dos três maiores máximos de três linhas distintas, ou indisponibilidade justificada |
| Linhas | Quantidade n de linhas válidas e abrangência da leitura; indicador 2 usa três somente quando disponíveis |
| Relações | η1 e η2 entre cada indicador e resistência, somente com bases compatíveis e denominador válido |
| Diferenciação visual | Estado de cada comparação, critério utilizado e pendências; sem rótulo de aprovação global |
| Quadro lateral | Por ID: base/reforço, As, Mr, Msol1/Msol2, eta1/eta2, n válido/esperado, cobertura, pico local, LP e pendências; folhas de continuação se necessário |
| Seleção por região | Campo “Incluir no relatório”, preferencialmente interativo, independente de eta/cor/resultado; preservar também decisão explícita de não inclusão quando houver |
| Legenda e rastreabilidade | Unidades, natureza, definição dos critérios, documentos/revisões, data/revisão da análise e ressalvas |

No rótulo local, apresentar ID e os valores que couberem de forma legível.
Transferir a configuração completa e informações adicionais para o quadro
lateral ou sua continuação, mantendo associação inequívoca. Não remover campos
obrigatórios por falta de espaço; dividir a entrega em vez de truncar valores
ou reduzir fontes até ficarem ilegíveis.

Conservar picos individuais por linha, posições e máximo absoluto nos registros
de suporte. Mostrar o máximo absoluto e alertas locais no quadro ou em folha
vinculada quando necessários à interpretação; a média não deve ocultar um pico
que supera a resistência.

## Dados suficientes, resultados parciais e pendências

É possível emitir uma comparação para as regiões com base gráfica/localização,
configuração, resistência e solicitações rastreáveis e compatíveis. Regiões
pendentes não impedem a emissão das demais e devem constar do mapa ou de quadro
específico no mesmo pacote gráfico.

- Sem resistência: publicar MR como “— / pendente”, motivo e dados disponíveis;
  não somar composições cuja atuação conjunta não foi comprovada.
- Sem demanda DXF associada: publicar “sem demanda associada / inconclusivo”,
  nunca M=0, η=0 ou comparação favorável.
- Menos de três linhas válidas: preservar indicador 1 quando aplicável; indicador 2
  e η2 ficam indisponíveis, com n e motivo explícitos.
- Leitura parcial: identificar linhas/trechos faltantes e limitar o alcance dos
  indicadores; não apresentar o subconjunto como cobertura completa.
- Sem geometria de uma ocorrência: incluí-la em quadro de pendências com marca,
  chamada/localização conhecida e fonte, sem inventar polígono.
- Sem prancha original ou sem dados suficientes para comparar: registrar o PDF
  devido, o impedimento e os controles afetados. Se houver base localizável,
  emitir mapa de pendências identificado como tal, sem chamá-lo de comparação
  resistente concluída.

Reconciliar inventário de regiões/ocorrências com mapa e quadros: cada item do
escopo deve aparecer como comparado, pendente, não examinado ou inaplicável
justificado. Não repetir o filtro dos comparativos históricos que publicava
somente faixas sem issues e com resistência disponível.

## Unidades, relações e critérios visuais

Aplicar [force-presentation](../../../../profile/force-presentation.md).
Apresentar normalmente Mk e MRd/γf equivalente em tf·m/m, mantendo γc/γs e
resultados brutos. MRd/γf não é resistência característica física da seção.
γf deve ser comprovado no novo projeto; não reproduzir automaticamente o 1,4
do arquivo de referência. Identificar igualmente materiais, h, cobrimento,
camadas, combinação/envoltória e fonte, sem herdar dados S07.

Usar Msol1/eta1 para o indicador 1 e Msol2/eta2 para o indicador 2, como na
prancha R02. Nos dados históricos, Msol2 corresponde a S3_mean_top3_lines_tfm_m
e eta2 ao campo eta3: alias de apresentação, sem renomear contratos ou perder
rastreabilidade. “Três” identifica as linhas do indicador, não seu número.
Na base característica compatível, η1=Msol1/(MRd/γf) e η2=Msol2/(MRd/γf), para a mesma
largura/direção/face. Em outra base comprovada, declarar a equação correspondente
e a impossibilidade de conversão quando houver. Não formar razão com base
incompatível, capacidade ausente, n insuficiente para Msol2 ou denominador nulo/não
válido. Ausência de razão é pendência identificada, não resultado favorável.

As médias são indicadores de análise; não são exigências normativas universais.
Distinguir resultado gráfico da comparação, resultado técnico do controle e
estado de execução. η1≤1 ou η2≤1, isoladamente, não comprova resistência local,
mínimos, ancoragem ou aprovação estrutural.

Preferir estados visuais explícitos, com cor e texto/símbolo:

| Estado da comparação identificada | Apresentação sugerida |
|---|---|
| Indicador supera resistência equivalente | Vermelho e texto “supera — indicador 1/2” |
| Indicador não supera resistência equivalente | Verde/azul e texto “não supera — indicador 1/2; revisão preliminar” |
| Comparação incompleta, sem resistência/demanda ou com hipótese pendente | Cinza/âmbar, padrão/contorno distinto e motivo |

Se Msol1 e Msol2 produzirem conclusões diferentes, mostrar ambas as razões/estados e
identificar qual indicador governa o mapa. Usar mapas/páginas separados quando
necessário; não fundir critérios em uma cor sem explicação. Diferenciar também
comparação por máximo local e qualquer outro critério utilizado. Conservar alerta
local mesmo que o mapa da média seja favorável.

Cores de material, hachuras e comentários existentes na prancha não são estados
da revisão. Não depender apenas da cor para distinguir resultados.

## Composição gráfica e conferência

Preferir manter o conteúdo vetorial da prancha via incorporação do PDF original,
com polígonos, contornos, textos e quadros vetoriais. Se a fonte for raster,
preservar a qualidade disponível e declarar a limitação, sem inventar vetorização.

Ampliar a folha para acrescentar quadro lateral, evitando comprimir o desenho.
Preservar proporção/orientação e escala quando possível; qualquer transformação
deve ser conhecida e não sustenta medição automática sem calibração.

Usar preenchimentos leves e contornos distinguíveis, rótulos deslocados e linhas
de chamada com ancoragem clara. Não cobrir chamadas, cotas, marcas, apoios ou
detalhes decisivos. Evitar sobreposição entre caixas e entre anotações e o
conteúdo original. A verificação de colisão de caixas dos scripts S07 não
comprova, sozinha, a legibilidade do desenho de fundo.

Antes de entregar, renderizar todas as páginas e inspecionar a visão geral,
os detalhes densos e o quadro lateral. Conferir:

- IDs e números iguais aos registros, com fontes e revisão corretas.
- Delimitações alinhadas, regiões pequenas identificáveis e pendências visíveis.
- Ausência de recortes, colisões, truncamentos, símbolos incorretos ou textos
  ilegíveis; fonte e contraste adequados à escala de revisão.
- Quadro completo, legendas/critério de cores explícitos e n/η corretamente
  associados ao indicador.
- Preservação das fontes originais e distinção das marcações anteriores.

Se não houver espaço, separar pranchas/direções/faces, acrescentar páginas de
detalhe ou continuação do quadro. Não resolver densidade escondendo pendências.
Utilizar a skill de PDF disponível para emissão e QA dos artefatos; o catálogo
de ferramentas não constitui um gerador já integrado ao 1A.

## Organização dos arquivos

No destino autorizado, manter emissão e revisão identificadas:

- output/pdf/verificacoes_<rev>/: pranchas por conjunto, direção e face, com
  ampliações/apêndices de pendências do mesmo conjunto.
- output/pdf/consolidado/: incompatibilidades_pendencias_<rev>.pdf e
  relatorio_armaduras_<rev>.pdf, com revisões independentes.
- Registros estruturados, evidências e escolhas do engenheiro em local referenciado.

Padrões de nome: ATP_<projeto>_<pavimento>_<prancha>_<face>_<direcao>_Mr_Msol_<rev>.pdf;
ATP_<projeto>_<pavimento>_incompatibilidades_pendencias_<rev>.pdf;
ATP_<projeto>_<pavimento>_relatorio_armaduras_<rev>.pdf.

Manter índice com arquivo/página/IDs, revisão da análise e das fontes, abrangência,
pendências e estado de revisão humana. IDs persistem nas páginas de mapa, quadro,
apêndice e fichas. Não presumir que o número de revisão dos três documentos seja
igual. Preservar PDFs revisados pelo engenheiro antes de regenerar qualquer saída.

## Relatório de incompatibilidades e pendências

Usar a referência R01, com identidade visual sóbria: cabeçalho de empreendimento/
pavimento, títulos por prancha, índice e navegação, fichas com evidências ampliadas,
rodapé de revisão/paginação e controles de seleção/comentário.

Separar três grupos, com títulos e situação explícitos:

1. **Incompatibilidades confirmadas:** conflito ou requisito demonstrado por
   evidência técnica/documental suficiente.
2. **Verificações pendentes de análise do engenheiro:** controle não encerrado,
   com objeto e ação de revisão definidos.
3. **Informações complementares necessárias:** dado/documento ainda necessário,
   motivo, localização e controles dependentes.

Não cadastrar neste relatório os casos de possível insuficiência ou indicadores
que superam resistência já apresentados nas pranchas e aguardando avaliação.
O índice pode remeter ao mapa, sem duplicar o caso, seus índices ou sua seleção.
O relatório técnico pode conservar seus quantitativos para rastreabilidade,
sem convertê-los em incompatibilidades definitivas.

Uma limitação de extração ou tarefa ainda não executada pelo agente não é
incompatibilidade do projeto. Registrar a restrição operacional na memória
técnica e a verificação específica ainda necessária no grupo pertinente.
Não transformar informação inconclusiva em conflito confirmado.

### Ficha de incompatibilidade confirmada

Cada ficha deve conter:

1. Código único e persistente.
2. Pranchas envolvidas e revisões.
3. Localização física, chamada e/ou regiões relacionadas.
4. Descrição técnica objetiva da diferença comprovada.
5. Critério ou informação documental utilizada, com origem e localizador.
6. Imagens ampliadas das regiões relevantes, preferencialmente lado a lado;
   identificar fonte, revisão e escala ou “sem escala”.
7. Providência ou esclarecimento necessário; não inventar solução executiva.
8. Checkbox “Incluir no relatório final”.
9. Checkbox “Não incluir”.
10. Campo de comentários do engenheiro, preferencialmente multilinha.

Preferir uma ficha por página quando a comparação gráfica exigir espaço; fichas
curtas podem compartilhar página sem perder campos/evidências. Diferenciar
visualmente as confirmadas das pendentes e das informações solicitadas, mantendo
a mesma disciplina de identificação e revisão.

Usar linguagem direta, técnica e dirigida a engenheiros estruturais. Explicitar
o que diverge e o que permanece compatível, sem atribuir consequência resistente
que não tenha sido demonstrada. Histórico já apreciado deve ser identificado
como tal, não reapresentado como incompatibilidade nova.

## Relatório técnico complementar

Usar a referência R00 para preservar a memória de cálculo e de interpretação,
sem substituir mapas ou fichas:

| Conteúdo | Registro esperado |
|---|---|
| Escopo/abrangência | Pavimentos, lajes, regiões/direções e exclusões |
| Documentos | Fontes, revisões, processamento, localizadores/hashes disponíveis |
| Decisões humanas | Autor, data, confirmação, justificativa e escopo; distinguir hipótese do dado lido |
| Critérios e hipóteses | Origem normativa/projeto/escritório, materiais, camadas, fatores, unidades e limites |
| Procedimentos | Extração, conciliação, interpretação geométrica, associação DXF e controle de qualidade |
| Resultados | Regiões, composições, resistências, indicadores, cobertura de linhas e quantitativos sem falsa contagem de falhas |
| Controles | Concluídos, inconclusivos, não executados, inaplicáveis justificados e dependências |
| Limitações/entregas | Efeito sobre a interpretação; arquivos/revisões/páginas dos mapas e fichas emitidos ou pendentes |

Usar síntese inicial, seções técnicas, tabelas repetindo cabeçalho e referências
cruzadas. Quantidades de regiões com eta>1 podem se sobrepor e não equivalem a
número de insuficiências confirmadas. Nunca transportar decisões, fórmulas de
mínimo, materiais, h, fator, aderência ou enquadramento da S07 para outro projeto
sem fonte e validação próprias.

## Estados técnicos e seleção editorial

Usar os pares de [contracts](contracts.md), sem acrescentar enum ao código 1A.
NOT_EXECUTED/NOT_EVALUATED indica controle não realizado;
EXECUTED_INCONCLUSIVE/INCONCLUSIVE indica execução sem conclusão suficiente.
Suspeita por falha de extração permanece inconclusiva.
PASS/FAIL exige evidência e se restringe ao critério; FAIL de escritório não é
reprovação normativa. NOT_APPLICABLE exige justificativa.
Falha parcial comprovada não desaparece porque outra parcela segue pendente.

**A seleção é independente do resultado técnico.** Eta>1, cor vermelha, PASS ou
FAIL não preenchem “Incluir”. A leitura de um campo vazio não é rejeição.

| Incluir | Não incluir | Decisão |
|---|---|---|
| Desmarcado | Desmarcado | Pendente; não presumir escolha |
| Marcado | Desmarcado | Selecionado pelo engenheiro |
| Desmarcado | Marcado | Exclusão explícita pelo engenheiro |
| Marcado | Marcado | Conflito; esclarecer e não emitir o item como decidido |

Aplicar essa regra às fichas e, quando usados os dois campos, às regiões dos
mapas. Se houver somente “Incluir”, desmarcado continua sem decisão explícita.
Preservar a opção “Não incluir” presente na R03 para distinguir exclusão de
ausência de revisão. Os dois campos devem representar uma decisão mutuamente
exclusiva; preferir controle do formulário que impeça seleção simultânea e
sempre validar a combinação ao recuperar os dados. A versão histórica utiliza
checkboxes independentes: a exclusão mútua ainda exige adaptação/validação,
não é funcionalidade comprovada desses geradores.

## Revisão humana em duas etapas

### Etapa preliminar

Gerar automaticamente os documentos pelos recursos compatíveis com as entradas,
no padrão estabelecido, registrando resultados disponíveis, suspeitas e pendências.
Não esperar que todos os controles estejam encerrados. Nas fichas, cadastrar como
confirmadas somente as incompatibilidades comprovadas; possíveis conflitos sem
evidência suficiente ficam no grupo de verificações pendentes.

Itens novos começam sem decisão. Reemissões recuperam escolhas existentes antes
de gerar campos, em vez de marcá-los Off indiscriminadamente.
Os PDFs são de revisão interna, não emissão pronta ao projetista.

### Etapa final

O engenheiro revisa pranchas/fichas, seleciona itens e comenta. O agente recupera
e confere as escolhas, resolve itens contraditórios e prepara a redação destinada
ao projetista somente após essa revisão. Não incluir automaticamente todos os FAIL.
Preservar os três documentos internos e emitir a seleção aprovada, sem substituir
a memória técnica por uma lista editorial de itens escolhidos.

Usar review_finding com ACCEPT/REJECT para registrar decisões atribuídas.
A aceitação de um apontamento não altera o resultado técnico nem aprova correção
executiva. A redação definitiva requer validação humana; não inferir aprovação
em nome do engenheiro a partir de uma caixa vazia ou de um arquivo recém-gerado.

## Preservação das escolhas entre revisões

Antes de substituir um PDF, conservar a cópia preenchida e registrar valores
canônicos de seus campos, comentários, IDs, fontes/revisões, autor e instante.
Relacionar região/ficha ao projeto, pavimento, prancha, direção/face e objeto
físico; não usar só coordenada de página ou índice de linha para transferir dados.

- Correspondência inequívoca e conteúdo inalterado: reaplicar seleção/comentários.
- Região ou fonte alterada, desdobrada, unida ou com ID renumerado: manter a
  decisão anterior no histórico e solicitar revalidação localizada.
- Mudança da decisão: registrar valor anterior, novo, autor, data e justificativa.
- Item retirado: conservar histórico e motivo; não apagar comentários.
- Divergência entre marcas do PDF e registro estruturado: manter ambas as fontes
  e resolver antes de considerar a decisão vigente.

A migração automática de decisões ainda não está implementada no contrato 1A
nem foi encontrada nos emissores inspecionados. Fazer essa reconciliação
operacionalmente; nunca apresentar regeneração com campos vazios como
preservação da revisão humana.

Após correção de dado técnico, seguir
[review-workflow](review-workflow.md#pendências-decisões-e-correções):
preservar originais/resultados anteriores, retirar dependentes do uso vigente,
reavaliar e atualizar mapas, fichas e memória técnica. Seleção anterior não
valida automaticamente o item corrigido; controles independentes conservam validade.

## Campos interativos e conferência funcional

Manter formulários editáveis na etapa de revisão; não achatar o único exemplar.
Identificar campos por item e finalidade, sem colisões de nome.
Preferir widgets reais para as seleções e campo de texto multilinha para comentários.

Além da conferência visual, validar árvore AcroForm/Fields e widgets de página,
valores /V e estados /AS quando aplicáveis, aparências /AP e persistência após
salvar/reabrir. Contagem de widgets ou uma caixa desenhada não prova formulário
válido. Testar marcar/desmarcar, gravar comentário e recuperar os valores;
verificar exclusividade e que ambos vazios não se tornam decisão automática.

Os scripts de QA S07 são referências de testes, não prova de importação de
escolhas, exclusividade ou migração entre revisões. Verificar o resultado em
leitor PDF compatível; registrar limitações sem presumir comportamento idêntico
em todos os visualizadores. Cópia estática pode acompanhar a emissão, mantendo
o formulário preenchido e o histórico como fonte da decisão.

## Síntese do padrão (transferida do SKILL.md em 10/11/2026)

Seguir [reporting](reporting.md) e as
[referências finais do 1º pavimento S07](s07-1pav-deliverables.md).
A prancha 7309 R02 governa o layout; a R03 registra a adição dos campos editoriais.
As fichas R01 de incompatibilidades e o relatório técnico R00 governam os outros
dois formatos. Não copiar suas hipóteses, valores ou decisões para outro projeto.

Nas pranchas, mostrar armadura efetivamente calculada (base/reforço), As, Mr,
Msol1/Msol2, eta1/eta2, n e cobertura, LP, pico local e pendências, com quadro
lateral. Preservar por região “Incluir no relatório”, independente da
classificação técnica; eta>1 nunca marca a seleção automaticamente.

Nas fichas, usar seleção “Incluir no relatório final”/“Não incluir” mutuamente
exclusiva e comentários do engenheiro, preferencialmente em campos PDF reais.
Ambas vazias significam decisão pendente; ambas marcadas são conflito, não
autorização de emissão. Não recadastrar insuficiências já apresentadas nos mapas
como incompatibilidades documentais.

Há geradores executados na S07 para os três formatos e para formulários, mas
ainda são scripts específicos, com gravações no nível superior. Coordenar os
recursos compatíveis e preservar o layout sem reconstruí-lo a cada ATP;
consultar o catálogo antes de executar. Não existe gerador genérico integrado
ao contrato 1A nem migração automática de decisões entre revisões.
Emitir primeiro o pacote preliminar. Somente após seleção, comentários e revisão
da redação pelo engenheiro preparar a emissão ao projetista. Preservar histórico
e revalidar escolhas em regiões alteradas.
