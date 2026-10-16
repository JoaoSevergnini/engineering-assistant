# Seleção longitudinal TQS × detalhamento

## Entradas e correspondência

Reconciliar pilar, trecho físico, pavimentos, revisão e processamento. Desdobrar
grupos sem esconder indivíduos. Pilar fora do TQS, lance sem dimensionamento
e resultado não extraído são situações diferentes; registrar a causa conhecida.
Ausência na extração parcial não comprova ausência no processamento.

Investigar os formatos recebidos e documentar o significado e as unidades dos
campos. Em relatórios de pilares que efetivamente apresentem `N_AS`/`FI_AS`,
`AS` e `RO_AS`, distinguir quantidade/bitola selecionadas, área reportada e taxa
reportada. Não usar outro campo de taxa sem comprovar sua semântica. Preservar
texto/valor original e conversão; o leitor LST de vigas não é leitor de pilares.

## Leitura das barras e da seção

Ler quantidade e diâmetro por marca da legenda do trecho, conferindo elevação,
corte e tabela quando houver ambiguidade. A mesma marca em representações
distintas não acrescenta barras. Grupos de mesma bitola podem ser somados para
a comparação nominal; conservar marcas e comprimentos para verificar a
composição física ao longo da altura posteriormente.

Não somar esperas de outro lance, estribos ou duplicações gráficas na emenda à
armadura nominal do corpo do pilar. Marcas com comprimentos diferentes podem
não atuar simultaneamente em toda a altura. Uma divergência entre corte e
tabela permanece conflitante, sem dar prioridade automática a uma representação.

Usar a seção de concreto do próprio detalhamento para sua taxa. Comparar
separadamente geometria TQS × detalhe; não substituir a área detalhada pela
área do modelo para forçar coincidência. Registrar diferenças pequenas sem
inventar tolerância normativa. Parâmetros negativos de seções especiais TQS
podem codificar tipos de seção: não tratá-los como dimensões negativas de concreto.

Em contornos curvos, comprovar raios, cotas e orientação. Se a área exigir
idealização geométrica ainda não conciliada com o modelo, explicitar a hipótese
e manter a comparação do contorno pendente. Não preencher área desconhecida
com o retângulo envolvente como se fosse área confirmada.

## Cálculo e interpretação

Com diâmetros em mm e áreas em cm²:

- `As_nominal = π/400 × Σ(n × Ø²)`;
- `taxa_detalhada = As_detalhada / Ac_detalhada`;
- retângulo: `Ac = b × h`, com b e h em cm;
- círculo: `Ac = πD²/4`, com D em cm.

Preservar a taxa TQS reportada e seu arredondamento; uma taxa nominal recalculada
é campo distinto. Comparar valores completos e arredondar apenas a apresentação.
Diferenças de arredondamento, área de seção, quantidade e bitola precisam de
interpretações distintas. As maior não demonstra atendimento aos esforços.

## Entrega e controles

Manter registro por pilar/trecho com seleção, armadura detalhada, ambas as
seções, áreas, taxas, fontes e pendências. Separar comparação de armaduras,
comparação de seções e capacidade não avaliada.

Quando solicitado, apresentar matriz com um par TQS/Detalhado por pilar e um
lance por linha, mantendo a mesma ordem nas abas de taxas e armaduras.
Usar números tipados nas taxas e texto `10 ø12.5` nas armaduras. Campo sem
resultado fica vazio ou recebe indicação textual clara; lance inexistente não
vira zero. Cor para taxa detalhada inferior à TQS usa valores completos e não
significa reprovação resistente.

Verificar correspondência de todas as chaves e cálculos com uma conferência
independente. Correção de leitura deve alcançar todas as matrizes dependentes.
