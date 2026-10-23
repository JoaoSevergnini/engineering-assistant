# PDFs gráficos, resultados e revisão humana

## Dois níveis de entrega

1. **PDFs gráficos de verificação — obrigatórios:** principal instrumento de
   revisão visual do engenheiro. Produzir por prancha ou conjunto de regiões
   analisadas sempre que houver dados suficientes, conforme o padrão abaixo.
2. **Relatório consolidado — complementar:** apontamentos preliminares,
   pendências, limitações e cobertura do pavimento, com referências aos PDFs.
   Não substitui a entrega gráfica.

Referência visual/funcional:
[ATP_S07_7307_faixas_Mrk_Msol_media.pdf](../../../../analises/atp_s07_lajes_terreo/output/pdf/pranchas_regioes/ATP_S07_7307_faixas_Mrk_Msol_media.pdf).
Preservar seu conceito: prancha original como base, polígonos de regiões,
rótulos de comparação e painel lateral. Não copiar valores ou hipóteses da S07.
Os [geradores históricos](existing-tools.md#referências-para-os-pdfs-gráficos-padrão)
são referências que exigem adaptação, não comandos prontos para outra obra.

Registros em tabela/JSON/Markdown podem iniciar a análise e sustentar a emissão,
mas não substituem os PDFs obrigatórios quando os dados já permitem produzi-los.
Não é necessário concluir todo o pavimento para entregar pranchas verificáveis.

## Conteúdo mínimo de cada PDF gráfico

| Item | Informação obrigatória |
|---|---|
| Base documental | Prancha original de armaduras, identificação, página e revisão; original preservado |
| Regiões | Delimitações, direção/face e ID único coerente entre mapa, quadro e dados |
| Armaduras | Bitola, espaçamento, As em cm²/m e marcas de cada família/conjunto; distinguir individual de composição |
| Resistência | Valor calculado da região, base/unidade, função/resultado Concretopy e hipóteses pertinentes, ou pendência explícita |
| Indicador 1 | Média dos máximos do sinal relevante por linha de grelha distinta, recortada na região |
| Indicador 2 | Média dos três maiores máximos de três linhas distintas, ou indisponibilidade justificada |
| Linhas | Quantidade n de linhas válidas e abrangência da leitura; indicador 2 usa três somente quando disponíveis |
| Relações | η1 e η3 entre cada indicador e resistência, somente com bases compatíveis e denominador válido |
| Diferenciação visual | Estado de cada comparação, critério utilizado e pendências; sem rótulo de aprovação global |
| Quadro lateral | Resultados por ID, configurações, valores, n, relações e pendências; folhas de continuação se necessário |
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
  e η3 ficam indisponíveis, com n e motivo explícitos.
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

Definir no PDF S1 como indicador 1 e S3 como indicador 2, ou usar nomes completos.
Na base característica compatível, η1=S1/(MRd/γf) e η3=S3/(MRd/γf), para a mesma
largura/direção/face. Em outra base comprovada, declarar a equação correspondente
e a impossibilidade de conversão quando houver. Não formar razão com base
incompatível, capacidade ausente, n insuficiente para S3 ou denominador nulo/não
válido. Ausência de razão é pendência identificada, não resultado favorável.

As médias são indicadores de análise; não são exigências normativas universais.
Distinguir resultado gráfico da comparação, resultado técnico do controle e
estado de execução. η1≤1 ou η3≤1, isoladamente, não comprova resistência local,
mínimos, ancoragem ou aprovação estrutural.

Preferir estados visuais explícitos, com cor e texto/símbolo:

| Estado da comparação identificada | Apresentação sugerida |
|---|---|
| Indicador supera resistência equivalente | Vermelho e texto “supera — indicador 1/3” |
| Indicador não supera resistência equivalente | Verde/azul e texto “não supera — indicador 1/3; revisão preliminar” |
| Comparação incompleta, sem resistência/demanda ou com hipótese pendente | Cinza/âmbar, padrão/contorno distinto e motivo |

Se S1 e S3 produzirem conclusões diferentes, mostrar ambas as razões/estados e
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

No destino autorizado do projeto, preferir:

- output/pdf/verificacoes/: PDFs gráficos por prancha/conjunto, direção e face.
- output/pdf/consolidado/: relatório complementar do pavimento, se emitido em PDF.
- Registros estruturados/evidências em local referenciado, com vínculo aos PDFs.

Padrão sugerido de nome:
ATP_<projeto>_<pavimento>_<prancha-ou-conjunto>_<face>_<direcao>_Mr_Msol_<rev-analise>.pdf.
Usar direção e face definidas no projeto; separar POS/NEG e H/V quando necessário
à legibilidade. Identificar índice/abrangência se o conjunto ocupar vários arquivos.
A revisão da análise é distinta da revisão da fonte e ambas devem constar na entrega.

Um PDF pode conter visão geral, quadros de continuação, pendências e ampliações
do mesmo conjunto. Manter o mesmo ID de região em todas as páginas. Folhas
separadas por indicador ou máximo local devem identificar explicitamente seu
critério. Um índice do pacote relaciona prancha/revisão, direção/face, regiões,
arquivo, revisão da análise e pendências.

## Registro preliminar, estados e relatório complementar

Para cada controle, registrar projeto/pavimento, laje/encontro, região, direção,
face e conjunto físico; critério/origem/referência e consulta efetiva; dados,
unidades, hipóteses; execução/resultado; documentos/revisões/localizadores;
evidências; cálculo bruto; pendências e revisão necessária. Usar os IDs de
[review-criteria](review-criteria.md) e os pares de [contracts](contracts.md).

NOT_EXECUTED/NOT_EVALUATED indica controle não realizado.
EXECUTED_INCONCLUSIVE/INCONCLUSIVE indica execução sem conclusão suficiente.
Suspeita por falha de extração permanece inconclusiva. PASS/FAIL exige evidência
e se restringe ao critério; FAIL de escritório não é reprovação normativa.
NOT_APPLICABLE exige justificativa. FAIL parcial comprovado não deve desaparecer
porque outra parcela segue pendente.

Conservar separadas comparação documental, conclusão técnica e execução.
O relatório consolidado reúne apontamentos preliminares, pendências, limitações
e contagens de controles esperados/executados/concluídos/inconclusivos/não
examinados/inaplicáveis. Remeter ao arquivo gráfico, página e ID correspondente.
Registrar PDFs ainda não emitidos e motivos; o relatório não encerra essa obrigação.

## Seleção humana dos apontamentos e correções

Submeter ao engenheiro falhas comprovadas, possíveis inconformidades e pedidos
de esclarecimento. Não incluir automaticamente todos os FAIL no relatório final.
A obrigação de entregar mapas não elimina esse filtro: os mapas preliminares
mostram o escopo e os resultados; os apontamentos da emissão final dependem de
seleção e redação aprovadas.

Usar review_finding com ACCEPT/REJECT, autor, data e justificativa, delimitando
seleção/redação. Aceitação não altera resultado técnico nem aprova correção
executiva. Não inventar aprovação em nome do engenheiro. Se a leitura for
incompleta, escrever “não identificada nesta leitura; conferência pendente”,
não “não existe no projeto”.

Após correção, seguir
[review-workflow](review-workflow.md#pendências-decisões-e-correções):
preservar originais/resultados anteriores, retirar os dependentes do uso vigente,
reavaliá-los e atualizar PDFs, quadros, índice e relatório afetados.
ACCEPT anterior não valida automaticamente o item corrigido. A propagação ainda
é operacional, sem mecanismo automático no 1A. Resultados independentes conservam
validade. Nenhuma rodada ou mapa favorável constitui aprovação global.
