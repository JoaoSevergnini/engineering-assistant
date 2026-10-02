# Leitura gráfica da V502

Fonte: página 1 de `RMP-EST-EX-1348-VIG-R00 - Copia.PDF`. Foram aplicadas as versões atualizadas de `beam-drawing-convections.md` e `beam-review.md`. A leitura usa exclusivamente a prancha e as convenções do escritório: não foram consultados resultados do TQS, nem realizadas verificações estruturais.

## Geometria

- Identificação explícita: **V502**, sem agrupamento indicado.
- Seção escrita: **19/202 cm**.
- Apoios, da esquerda para a direita: **V548, P307, P308 e P309**.
- Dimensões indicadas ao longo da viga: **19 cm** em V548 e **40 cm** em cada um dos três pilares.
- As regiões cotadas de estribos são **759, 245, 614 e 202 cm**. Por associação gráfica com as faces dos apoios, correspondem a três trechos entre apoios e ao prolongamento além de P309. O trecho final é um balanço na representação geométrica; não foi inferida condição de vínculo do modelo.

O Corte A mostra a alma retangular alta e projeções laterais em níveis distintos. As dimensões dessas projeções não estão cotadas. Não há cota local de cobrimento.

Para as coordenadas derivadas no JSON, x=0 foi colocado na face direita de V548. P307 ocupa x=759 a 799; P308, x=1044 a 1084; P309, x=1698 a 1738; a extremidade direita fica em x=1940 cm. Esses números são obtidos pelo encadeamento das cotas e não são abscissas escritas na prancha.

## Armaduras superiores — negativas pela posição gráfica

| Posição | Chamada explícita | Camada | Forma e região |
|---|---|---|---|
| N1 | 2 Ø10, C=185 cm | 2 na primeira, pelo padrão | Horizontal 165 cm e dobra esquerda de 20 cm para baixo; junto de V548 |
| N2 | 3 Ø16, C=1200 cm | 3 na primeira, padrão e corte | Reta; inicia 101 cm após a face direita de V548 e atravessa P307/P308 |
| N3 | 1 Ø16, C=833 cm | 1 na segunda, explícita | Reta; atravessa P307/P308 e termina 131 cm à direita da face direita de P308 |
| N4 | 3 Ø16, C=956 cm | 3 na primeira, pelo padrão | Horizontal 764 cm e dobra direita de 192 cm para baixo; região de P309/extremidade direita |
| N5 | 1 Ø16, C=526 cm | 1 na segunda, explícita | Reta; reforço superior da região direita |

## Armaduras inferiores — positivas pela posição gráfica

| Posição | Chamada explícita | Camada | Forma e região |
|---|---|---|---|
| N6 | 4 Ø10, C=852 cm | 4 na primeira, padrão e corte | Horizontal 817 cm e dobra esquerda de 35 cm para cima; primeiro vão até a região de P307 |
| N7 | 4 Ø12,5, C=1200 cm | 1 na segunda, explícita; 3 na primeira, pelo padrão | Horizontal 1176 cm e dobra direita de 24 cm para cima; região de P307 até a extremidade direita |

As chamadas de segunda camada são `(1 Ø 2aCAM)`. A classificação superior/inferior foi feita pela representação e associação com a elevação, não pela bitola ou quadro de aço.

## Armadura de pele

Todas as quatro posições estão explicitamente identificadas como **PELE**, com **2×9 Ø8**: nove barras por face lateral, 18 barras por posição, distribuídas em trechos diferentes.

| Posição | Comprimento por barra | Região e particularidade |
|---|---:|---|
| N10 | 813 cm | V548 até P307; trecho 800 cm e retorno esquerdo de 13 cm |
| N11 | 293 cm | Região P307–P308; extremidade 16 cm antes da face direita de P308 |
| N12 | 662 cm | Região P308–P309; extremidade 24 cm após a face esquerda de P309 |
| N13 | 223 cm | Região de P309 até a extremidade direita |

Não se somaram as quatro posições como se todas atravessassem uma mesma seção. O espaçamento vertical da pele não está cotado.

## Estribos

| Região | Chamada explícita | Comprimento da região |
|---|---|---:|
| V548–P307 | N9 — 55 Ø5 c/14 | 759 cm |
| P307–P308 | N9 — 18 Ø5 c/14 | 245 cm |
| P308–P309 | N9 — 44 Ø5 c/14 | 614 cm |
| Após P309 | N9 — 15 Ø5 c/14 | 202 cm |

O detalhe da forma escreve **N9 — 132 Ø5 C=437 cm**, com cotas **14 e 197 cm**. São visíveis dois segmentos verticais laterais do estribo. As regiões foram mantidas separadas, embora tenham a mesma bitola e espaçamento.

Não foram inferidos afastamentos do primeiro/último estribo às faces nem comprimentos e ângulos de ganchos sem cotas próprias.

## Grampos e apoios indiretos

**N8 — 2×1 Ø10 C=213 cm** aparece com forma de grampo em U, aberto para a esquerda, cota longitudinal de **100 cm** e ligação de **13 cm**. Há uma chamada `2×1 Ø10` junto da região superior da extremidade direita na elevação. Registra-se `anchorage_staples_detailed = true`. A camada exata de cada grampo e a associação barra a barra não estão individualizadas por texto.

Há **dois contornos retangulares tracejados**:

1. No primeiro vão V548–P307, antes de P307.
2. No terceiro vão P308–P309, próximo de P308.

Conforme o item 7 atualizado das convenções, representam **vigas apoiadas na V502**. Seus nomes e abscissas exatas não estão indicados.

Foi examinada a armadura transversal junto de cada contorno: **não existe chamada nem concentração específica de suspensão nesses pontos**. A N9 mantém Ø5 c/14 nas regiões gerais. Registra-se `suspension_reinforcement_detailed = false` em cada um desses apoios indiretos, por interpretação do padrão do escritório. Isso significa ausência de suspensão específica detalhada, não ausência de necessidade. Não foi analisada a armadura da viga V548, que serve de apoio principal à V502.

## Corte A

O corte está no primeiro vão e apresenta:

- **3 barras superiores na primeira camada**, associadas à N2;
- **1 barra superior na segunda camada**, associada à N3;
- **4 barras inferiores na primeira camada**, associadas à N6;
- **9 barras de pele por face**, associadas à N10 nessa região.

A associação às posições vem do cruzamento entre corte, elevação e extensões das barras; os pontos do corte não são rotulados individualmente. O corte não foi estendido às regiões de N4, N5, N7 e N8.

## Coordenadas que puderam ser determinadas

| Posição | x inicial | x final | Base da derivação |
|---|---:|---:|---|
| N2 | 101 | 1301 | 101 + 1200 |
| N3 | 382 | 1215 | Face direita de P308 em 1084; fim=1084+131; início=fim−833 |
| N11 | 775 | 1068 | Fim=1084−16; início=fim−293 |
| N12 | 1060 | 1722 | Face esquerda de P309 em 1698; fim=1698+24; início=fim−662 |

Valores em cm, derivados das cotas e das associações gráficas. Nas demais posições, registrei a região e as dimensões da forma sem completar afastamentos não cotados para criar coordenadas absolutas.

## Rastreabilidade e limites

O JSON contém 263 campos classificados como `explicit`, `graphically_interpreted`, `interpreted_by_office_standard` ou `uncertain`, com fontes no PDF ou nos itens das referências. As caixas de localização do PDF usam pontos, com origem no canto superior esquerdo.

Permanecem não determinados: nomes das vigas apoiadas, posições longitudinais sem cotas suficientes, abscissa exata de A-A, cobrimento local, dimensões das projeções laterais, detalhes não cotados de ganchos e condições de vínculo. Não foram calculados esforços, necessidade, capacidade ou suficiência de armaduras.
