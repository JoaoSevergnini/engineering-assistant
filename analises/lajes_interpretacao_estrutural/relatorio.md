# Etapa 6 — Interpretação estrutural documental das regiões

A camada derivada preserva integralmente as **35 regiões individuais e 119
composições** da Etapa 5. Registra as quatro classificações confirmadas por João,
produz hipóteses geométricas para revisão e mantém **44 das 48 sobreposições como
UNDETERMINED**. Não calcula aço ou resistência nem autoriza soma de contribuições.

## Resultado

| Classe final | Quantidade | Fonte/alcance |
|---|---:|---|
| SINGLE_DISTRIBUTED | 71 | Uma identidade gráfica; não comprova toda a identidade física |
| BASE_PLUS_REINFORCEMENT | 2 | C059 e C083, confirmação humana de João |
| LAP_SPLICE | 1 | C092, confirmação humana; soma independente bloqueada |
| GRAPHICAL_RESIDUAL | 1 | C073, confirmação humana; geometria original mantida |
| UNDETERMINED | 44 | Hipóteses automáticas insuficientes para conclusão |

Há **77 blocos consolidados de interpretação**, com todos os 119 IDs geométricos
referenciados uma única vez. Essa consolidação ainda não é uma composição resistente
utilizável: todos os blocos possuem `resistant_use_authorized=false` e
`effective_resistant_contributions=null`.

## Auditoria e preservação

Consultados `automatic.py`, `leaders.py`, `opening_groups.py`,
`distributed_regions.py`, seus testes, o inventário e relatório da Etapa 5 e as
entidades vetoriais/textuais das etapas anteriores. A implementação é aditiva:
`structural_regions.py` e `run_structural_regions.py`. Não altera inventário,
reconhecimento documental, partição, vigas, pilares ou Concretopy.

Reutilizados `partition`, `intersection`, `area`, `polygon`, `covered_edge`,
`center`, `contains` e a renderização PyMuPDF existente. O backend continua
restrito a retângulos ortogonais. Não foi adicionada biblioteca ou regra normativa.
As coordenadas continuam em pontos PDF e as áreas em pt², não em área de aço.

`stage6_provenance` contém os hashes dos arquivos de entrada e dos registros
humanos, além da igualdade exata das ocorrências, partição e registro N38 com
os respectivos dados anteriores. O SHA-256 do PDF foi verificado antes/depois:
`3eae69c055bc2b9e161c7767915f2682f9e7b53651dae073d046ecd0ddb45662`.
Nenhum PDF foi escrito ou modificado.

## Dados documentais das lajes e contornos

Foram detectados automaticamente nove nomes na região de detalhamento e pares
tipográficos de espessura (`h:`), com referências aos IDs e caixas dos textos:

| Laje | Espessura (cm) | Contorno nesta etapa |
|---|---:|---|
| L601 | 12 | Duas alternativas; associação pendente |
| L602 | 12 | Um candidato retangular preliminar |
| L603 | 20 | Pendente |
| L604 | 12 | Pendente |
| L605 | 18 | Pendente |
| L606 | 12 | Pendente |
| L607 | 20 | Quatro alternativas; associação pendente |
| L611 | 12 | Pendente |
| L612 | 12 | Pendente |

O nome e a espessura são dados textuais extraídos; o contorno é uma interpretação
geométrica experimental. Foram investigadas as três coordenadas envolventes mais
próximas em cada direção, descartando entidades de barras/eixos conhecidas,
exigindo quatro bordas integralmente suportadas por segmentos (tolerância de
continuidade de 0,25 pt), nome/espessura internos e ausência de outro nome interno.
Entidades de comprimento nulo não contribuem para a evidência.

Contornos concorrentes são mantidos, sem selecionar o menor pela proximidade.
O retângulo de L602 vai de (1109,5200; 175,1200) a (1184,2800; 454,0000) pt,
com IDs dos segmentos de suas quatro bordas. Ele intersecta R002/N28 em
20.849,0719 pt², cerca de 84,65% da envoltória dessa ocorrência. Essa fração é
geométrica; não limita fisicamente a barra ou transforma o contorno em planta de formas.

Para as outras oito lajes não foi atribuída nenhuma região. Em particular, N14
não foi associado a L603 só porque os respectivos textos estão próximos. O teste
sintético demonstra uma ocorrência cruzando duas lajes por interseção geométrica;
esse caso não foi comprovado na prancha real com os contornos atualmente aceitos.

Limitações do detector: não reconhece lajes não retangulares ou etiquetas externas
por linhas de chamada; pode confundir faces de vigas/contornos auxiliares. Um único
candidato não comprova sua natureza estrutural. O mapa expõe as alternativas de
L601/L607 e os nomes pendentes. Todos os contornos exigem conferência com formas.

## Hipóteses automáticas e confirmações humanas

O algoritmo guarda separadamente `automatic`, a classificação final e
`human_confirmation`. Não promove uma hipótese a comprovação estrutural.

Indícios implementados:

- Função base/reforço: mesma orientação, extensão relativa e sobreposição
  significativa; palavras BASE/REFORÇO são evidência auxiliar junto à barra
  representativa, não requisito obrigatório. O código pode manter UNKNOWN.
- Traspasse candidato: interseção localizada entre extremidades longitudinais
  de envoltórias com mesma direção e continuidade espacial. Registra também
  afastamento transversal das barras representativas e equivalência de
  bitola/espaçamento. A colinearidade não é presumida; a barra representativa
  pode estar desenhada em outra ordenada dentro da faixa. Indício não é emenda
  comprovada e não informa comprimento normativo.
- Residual candidato: faixa estreita, pequena proporção em relação a todos os
  membros, proximidade das extremidades de pelo menos duas distribuições e
  vizinhos contínuos com subconjuntos de membros. A área isolada não basta.

Os parâmetros de triagem estão em `criteria` no JSON: largura estreita 4 pt,
fração pequena 4%, distância às extremidades 4 pt, relação de áreas 1,5 para
função e sobreposição mínima de 30% do menor membro, entre outros critérios
legíveis no código. São escolhas experimentais para gerar candidatos, não
limites normativos ou comprovação de irrelevância. Não foram calibradas como
classificador validado; outras escalas/pranchas exigem revisão dos parâmetros.

São 12 propostas de base+reforço, 31 de traspasse e 13 de residual; categorias
podem coexistir na mesma célula e esses números não são acertos. C073 recebe
propostas concorrentes de traspasse e residual, mas sua classificação final é
residual pela confirmação humana. Esse caso demonstra por que uma trajetória
ou uma faixa pequena não resolve a interpretação automaticamente.

As quatro confirmações estão em `validacoes_engenheiro.json`, com origem
"João, solicitação Etapa 6, seção 5", assinatura dos polígonos/propriedades dos
contribuintes e hash do PDF. Os IDs C059/C083/C092/C073 constam como referências
de revisão nesse arquivo, não como condições do classificador. Uma mudança do
ID de exibição preserva a revisão; geometria ou documento diferente não a recebe
silenciosamente. Registros conflitantes ficam pendentes em `review_errors` e
registros não aplicados ficam em `unmatched_reviews`.

A confirmação de uma categoria numa célula não foi extrapolada para todas as
outras interseções das mesmas posições. Não há evidência suficiente para isso.

## Funções candidatas e contenção

Das 35 regiões: sete têm hipótese de BASE, cinco de REINFORCEMENT e 23 continuam
UNKNOWN. Nenhuma função global de ocorrência foi marcada como confirmação humana.
Foram feitos cinco ensaios de contenção **condicionados a essas funções candidatas**:

| Reforço candidato | Bases candidatas consideradas | Área coberta (pt²) | Descoberta (pt²) | Resultado gráfico |
|---|---|---:|---:|---|
| R026 / N10 | R021, R031 | 6120,0000 | 0 | Coberto |
| R027 / N10 | R020, R032 | 6120,0000 | 0 | Coberto |
| R034 / N14 | R032, R043 | 58999,4504 | 0 | Coberto pela união |
| R035 / N14 | R031, R044 | 59030,3148 | 0 | Coberto pela união |
| R053 / N40 | R050 | 2268,8070 | 2453,8824 | Parcialmente descoberto |

A união e diferença são obtidas pela mesma partição retangular, sem contar duas
vezes a área coberta por bases sobrepostas. Direções diferentes ou camadas conhecidas
incompatíveis não entram como bases compatíveis; camada desconhecida mantém o
resultado explicitamente provisório. Não foram aplicadas verificações às LOCALIZED.

R053 não é um apontamento de insuficiência: sua própria função como reforço é
apenas hipótese automática, sem palavra documental correspondente comprovada.
A parcela descoberta está registrada sem corrigir polígonos. É necessário revisar
a função de N40 e a interpretação de sua composição antes de qualquer conclusão.
Não há classificação de divergência real ou diferença gráfica definitivamente
estabelecida. Diferenças pequenas seriam apenas sinalizadas para revisão.

## Consolidação e proteção contra soma indevida

São agrupadas somente parcelas que compartilham uma borda com comprimento positivo,
mesma lista de identidades gráficas, mesma classificação e mesmo estado de validação.
Contato pontual ou repetição de posição em outro local não une regiões. A geometria
resultante é uma lista de retângulos originais, sem uma envoltória que preencha vazios.
Cada bloco preserva ocorrências, regiões individuais e composições originais, sem
duplicar membros e sem recalcular aço.

A consolidação é conservadora: não declara conjuntos resistentes equivalentes quando
a classificação residual deixa a composição efetiva desconhecida. Em C073 é ignorado
o significado resistente da sobreposição gráfica, mas não se inventa qual membro de
qual região vizinha deve substituir a célula. C092 mantém as duas posições e bloqueia
sua soma independente. Base+reforço confirmado mantém pendente o alcance físico e a
camada necessários para eventual uso futuro. Nenhuma região consolidada está
autorizada para verificação resistente nesta etapa.

## Entregáveis e validação visual

- [Inventário completo](inventario.json), [lajes](lajes.json),
  [classificações](classificacoes.json) e [tabela](classificacoes.md).
- [Contenção](contencao.json), [funções candidatas](funcoes_candidatas.json) e
  [regiões consolidadas](regioes_consolidadas.json).
- [Lajes preliminares](lajes_preliminares.png): nomes/espessuras e contornos/alternativas.
- [Base/reforço candidatos](base_reforco_candidatos.png): funções ainda não confirmadas.
- [Composição estrutural](composicao_estrutural.png), [traspasses](traspasses.png),
  [residuais](residuais.png) e [pendências](pendentes.png).
- Comparações original/interpretação: [C059](C059_confirmacao.png),
  [C083](C083_confirmacao.png), [C092](C092_confirmacao.png), [C073](C073_confirmacao.png).
- [R053 — contenção provisória](R053_contencao.png), com parcela descoberta destacada.

O original é renderizado como fundo separado das marcações, sem alterar o PDF.
Foram examinados visualmente o mapa de lajes, C059, C092 e a ampliação de contenção;
esta teve o enquadramento/legendas ajustados para eliminar colisões de texto.
A inspeção de apresentação não é uma nova validação independente das associações.

## Testes, pendências e próxima etapa

Os testes novos distinguem geometria sintética de regressões reais. Incluem pares
nome/espessura, contorno ausente/concorrente, rejeição de aresta de armadura,
travessia de duas lajes, cobertura por uma base/união de bases, parcela descoberta,
hipóteses de base+reforço/traspasse/residual, três membros, direções diferentes,
consolidação sem duplicação ou união por lacunas, confirmação humana, assinatura
desatualizada, conflito de revisões, mudança de ID e invariância de cor.
O resultado da execução está em `testes.txt`.

Prioridades seguintes: revisar as hipóteses (especialmente as concorrentes e N40),
confirmar funções e camadas por ocorrência, resolver contornos de L601/L607 e
obter a planta de formas para estabelecer domínio, apoios e aberturas. Só depois
definir identidade física e composição resistente efetiva com confirmação explícita.
As nove identificações textuais não significam nove lajes geometricamente resolvidas.

O registro N38 continua intacto: chamada 6x3 Ø12,5 C=182, confirmação de quatro
conjuntos de três barras, divergência documental sem correção automática. Ele não
participa das verificações de contenção ou da classificação das DISTRIBUTED.
Não houve cálculo resistente, ancoragem normativa, dimensionamento, esforços TQS,
otimização, sugestão de redução de aço ou geração de apontamentos de ATP.
