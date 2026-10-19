# Etapa 5 — Regiões gráficas e sobreposições

Foram reconstruídas **35 regiões individuais**, particionadas em **119 regiões de
composição retangulares**, das quais **48 apresentam mais de uma identidade gráfica**.
O máximo encontrado foi de três identidades simultâneas. Nenhuma das 35 envoltórias
DISTRIBUTED foi rejeitada nos critérios implementados. Esses números são cobertura
do inventário experimental anterior, **não taxa de acerto**. Não existe inventário
independente de regiões de composição conferido pelo engenheiro.

## Auditoria e método

Entradas: `../lajes_grupos_fisicos/inventario.json`, relatórios anteriores e a prancha
RMP-EST-LO-1422-LAJ-R00.PDF. O SHA-256 do PDF, o caminho e o hash do inventário estão
em `inventario.json`, campo `stage5_provenance`. O PDF permaneceu idêntico após a execução.
Todas as 59 ocorrências anteriores e toda a reconstrução localizada foram preservadas
integralmente. Não foram alterados classificadores, módulos de vigas/pilares ou Concretopy.

Reutilizadas `automatic.graphic_envelope` e `bar_axis_intersection`, entidades e
envoltórias anteriores e renderização PyMuPDF via `run_sheet`. A origem é distinguida
entre `associations[0]` e `leader_association`; uma seleção múltipla não é resolvida
pela proximidade. Shapely não foi encontrado no Python utilizado, incluindo
`tmp/pdf_deps`. Não foi instalada dependência nova.

As 35 envoltórias são retangulares e alinhadas aos eixos PDF. Por isso foi implementado
um backend restrito: subdivisão pelos valores X/Y originais dos limites, determinação
do conjunto de ocorrências em cada célula, fusão horizontal e depois vertical de células
com o mesmo conjunto. Não há arredondamento, snapping, reparação de polígonos ou descarte
de faixas estreitas. Partes desconectadas ou decomposições retangulares de uma mesma
composição mantêm identificadores distintos; 119 não significa 119 combinações únicas.

Antes da partição são verificados: anel retangular simples e finito, orientação real
das linhas, perpendicularidade/interseção interior e igualdade entre envoltória
armazenada e envoltória reconstruída (tolerância de comparação 1e-7 pt, sem modificar
coordenadas). Geometria incompleta ou contraditória fica em `pending`, sem polígono.
O backend rejeita polígonos inclinados, côncavos ou com furos; sua extensão exige
outra implementação geométrica e novos testes.

## Dados extraídos e interpretação

- **Extraídos do PDF nas etapas anteriores:** textos e coordenadas, bitolas,
  espaçamentos e C nominal, segmentos e identificadores vetoriais das barras/eixos,
  setas e marcadores. Esses dados não são nova leitura independente nesta etapa.
- **Reconstruídos geometricamente:** envoltórias, dimensões longitudinal/transversal,
  polígonos da partição e interseções com aberturas. Coordenadas em pontos PDF,
  origem no canto superior esquerdo, Y crescente para baixo; áreas em pt².
- **Contexto documental:** título da prancha de armadura positiva horizontal.
  A camada física individual permanece desconhecida; não se deduz uma distribuição
  superior/inferior pela interseção das envoltórias.
- **Confirmação independente do engenheiro:** apenas a informação da N38 fornecida
  expressamente por João na solicitação. As novas composições têm zero validações
  independentes registradas. Não foram recalculados comprimentos físicos ou aço.

O comprimento nominal C não define o polígono: a extensão longitudinal vem dos
extremos da barra representativa e a transversal dos extremos do eixo de distribuição.
Dobras e ancoragens não foram acrescentadas. Não se afirma que esse retângulo seja
a região física efetiva integral da armadura.

## Identidade e contribuição

Posição documental, ocorrência, região individual e região de composição possuem
campos próprios. Repetições de N14, N15, N25 e outras posições permanecem separadas
quando correspondem a entidades/localizações diferentes. Chamadas com as mesmas
propriedades documentais e os mesmos IDs vetoriais de barra/eixo recebem uma única
identidade gráfica: uma chamada duplicada não aumenta essa contagem.

Isso não comprova identidade física em diferentes representações ou detalhes.
Mesmo uma coincidência geométrica com fontes diferentes não autoriza somar aço.
Possíveis duplicações de uma mesma posição em uma composição ficam em
`possible_duplicate_pairs`. Todas as composições têm
`physical_addition_authorized=false`; não há área de aço ou número de contribuições
físicas independentes calculado. Conjuntos por direção/camada são separados e a
camada é desconhecida. Expressões BASE/REFORÇO e cores não participam da partição.
As 15 LOCALIZED estão excluídas deste processamento.

## Resultados e limites estruturais

A união gráfica tem área **1.051.133,9042 pt²**. Esse valor não é área de laje.
As verificações de conservação de área confirmam que, para cada ocorrência, a soma
das parcelas que a contêm reproduz a área original; parcelas distintas não se
sobrepõem em área. Isso valida operações geométricas, não a associação documental.

Cinco interseções positivas com possíveis aberturas: R019/H10, R036/H12, R036/H13,
R043/H14 e R044/H15. `intersecoes_aberturas.json` registra polígonos, áreas e
validação pendente dos contornos. Não houve subtração e não se presume que todos
os vazios estejam reconhecidos. Contato apenas por borda não conta como área.

A inspeção da prancha mostra hachuras, contornos e nomes de lajes, mas eles não
fornecem nesta etapa um domínio estrutural conferido. Nenhuma região foi atribuída
a L603/L607 ou outra laje. Regiões permanecem em coordenadas da prancha; seus limites
não substituem a planta de formas. Faixas estreitas de sobreposição são preservadas
e podem refletir o detalhamento ou imprecisão gráfica, exigindo conferência.

## Visualização e conferência

- [Regiões individuais](regioes_individuais.png): envelopes com IDs Rnnn.
- [Composições](composicoes.png): partição com IDs Cnnn.
- [Consulta interativa local](consulta.html): selecione um polígono e consulte
  posições, ocorrências, fontes, direção, bitola e espaçamento. O original está
  incorporado, sem dependências externas. O painel JSON explicita as incertezas.
- [Tabela de composições](composicoes.md): ligação entre polígonos e ocorrências.
- Imagens `C*_sobreposicao.png`: ampliações das maiores interseções e de casos
  com três identidades. C073, por exemplo, contém O032/N15, O036/N26 e O043/N13.
- [Pendências anteriores](pendencias.png): caixas das nove ocorrências não
  ASSOCIATED do inventário anterior, sem criar envoltórias para elas. Não são
  nove DISTRIBUTED rejeitadas: nenhuma das 35 apresentou geometria pendente.
- [Original sem marcações](original.png), renderizado separadamente.

Foi inspecionado visualmente o mapa geral e uma ampliação C073 para avaliar a
legibilidade; o enquadramento das ampliações foi aumentado para fornecer contexto.
Essa revisão de apresentação não confirma individualmente as 48 sobreposições.
Os inventários preservam os campos de validação anteriores; as novas composições
estão explicitamente pendentes. A consulta HTML deve ser conferida no navegador
do revisor; não houve ensaio automatizado de interação no navegador.

## N38 — consistência documental

`consistencia_N38.json` preserva a chamada original N38 6x3 Ø12,5 C=182,
inclusive os fatores [6,3] e quantidade textual 18. Registra separadamente a
confirmação de João: quatro conjuntos de três, total 12. A divergência permanece
aberta e identificada; não corrige o PDF, não cria grupos novos nem altera a
reconstrução localizada da Etapa 4. Não participa da partição DISTRIBUTED.

## Testes e próxima etapa

Os novos testes distinguem topologia sintética, regressões reais e mutações
sintéticas de registros reais. Cobrem interseção parcial, contenção, adjacência,
três regiões, determinismo, coordenadas, anéis inválidos/incompletos, repetição de
posição, duplicação de chamada com mesmas fontes, direção vertical, independência
de cor, conservação de área, preservação N26/inventários e divergência N38.
Executar todos conforme README; resultados da execução constam em `testes.txt`.

Próxima etapa recomendada: conferir manualmente amostras de sobreposições largas
e estreitas e todas as possíveis duplicações; registrar seleção/aceitação por ID.
Depois registrar planta de formas, transformação de coordenadas/escala e contornos
estruturais/aberturas conferidos antes de recortar regiões ou atribuir lajes.
Confirmar camada e identidade física antes de qualquer composição resistente.
Não foram feitas verificações resistentes, dimensionamento ou apontamentos de ATP.
