# Leitura do detalhamento V501=V503

Fonte geométrica: página 1 de `RMP-EST-EX-1348-VIG-R00 - Copia.PDF`. Leitura manual do PDF renderizado, com as convenções de `beam-drawing-convections.md` e o procedimento `beam-review.md`. Não foram usados resultados do TQS, nem efetuadas verificações estruturais.

As quantidades abaixo são **por viga**. O quadro de aço V501=V503 (X2) contém os totais do grupo.

## Geometria e apoios

A seção escrita é **19/72 cm**. Há um trecho entre os apoios indicados como **P2A/P2B**, à esquerda, e **P1A/P1B**, à direita. As dimensões indicadas junto aos apoios são 120 e 142 cm. A correspondência individual de cada nome com V501 ou V503 não está confirmada pela prancha; não foi atribuída por ordem dos nomes, conforme a referência, item 9.

As três regiões consecutivas de estribos medem 537, 72 e 102 cm. A associação de suas extremidades às faces internas dos apoios permite obter **711 cm entre faces**, por soma. Esse número não aparece como uma cota única na prancha.

## Armaduras longitudinais

| Posição | Associação gráfica | Chamada por viga | Camadas | Forma |
|---|---|---|---|---|
| N1 | Superior / negativa, região esquerda | 2 Ø16, C=465 cm | 2 na primeira, pelo padrão | Reta; cota 62 cm para dentro do apoio esquerdo |
| N2 | Superior / negativa, região esquerda | 2 Ø16, C=260 cm | 1 na segunda, explícita; 1 na primeira, pelo padrão | Reta; cota 62 cm para dentro do apoio esquerdo |
| N3 | Superior / negativa, região direita | 2 Ø20, C=485 cm | 2 na primeira, pelo padrão | Reta; cota 80 cm para dentro do apoio direito |
| N4 | Superior / negativa, região direita | 2 Ø20, C=301 cm | 1 na segunda, explícita; 1 na primeira, pelo padrão | Reta; cota 78 cm para dentro do apoio direito |
| N5 | Inferior / positiva | 4 Ø12,5, C=815 cm | 1 na segunda, explícita; 3 na primeira, padrão e corte | Reta; cota 51 cm para dentro do apoio direito |
| N8 | Pele nas duas faces laterais | 2×3 Ø8, C=760 cm | 3 por face, associadas ao Corte A | Reta; cota 24 cm para dentro do apoio esquerdo |

Diâmetros, quantidades e comprimentos são explícitos. A associação superior/inferior vem da representação da armadura. As camadas não escritas foram interpretadas conforme o item 4 da referência, sem tratá-las como informação explícita.

Origem longitudinal adotada apenas para organizar as cotas: face interna do apoio esquerdo, x crescente para a direita. As coordenadas abaixo são **derivadas por associação gráfica e aritmética das cotas**, não cotas impressas:

| Posição | x inicial (cm) | x final (cm) |
|---|---:|---:|
| N1 | -62 | 403 |
| N2 | -62 | 198 |
| N3 | 306 | 791 |
| N4 | 488 | 789 |
| N5 | -53 | 762 |
| N8 | -24 | 736 |

As fórmulas estão registradas no JSON. Não são comprimentos de ancoragem necessários nem resultados de dimensionamento.

## Estribos

| Região, da esquerda para a direita | Chamada explícita | Comprimento da região |
|---|---|---:|
| R1 | N6 — 39 Ø5 c/14 | 537 cm |
| R2 | N7 — 5 Ø6,3 c/15 | 72 cm |
| R3 | N6 — 8 Ø5 c/14 | 102 cm |

A forma registra **N6 — 47 Ø5 C=177 cm** e **N7 — 5 Ø6,3 C=178 cm**, com cotas de 14 e 67 cm. As três regiões permanecem separadas. Os afastamentos do primeiro e último estribo às faces não estão cotados.

A N7 ocupa um intervalo localizado apontado por seta, próximo de um contorno tracejado da elevação. Sua função não está escrita: foi mantida como armadura transversal local, **sem afirmar que seja suspensão**. Também não é seguro declarar ausência de suspensão enquanto essa representação localizada permanecer sem função confirmada.

## Corte A e detalhes especiais

O Corte A mostra quatro pontos superiores, três pontos na primeira fileira inferior, um ponto acima dessa fileira e três pontos laterais intermediários em cada face. A posição do corte coincide graficamente com a superposição de N1 e N3. Não representa as regiões extremas com N2 e N4.

Não há chamada ou representação de grampo adicional: `anchorage_staples_detailed = false`, classificado como `interpreted_by_office_standard`. Isso não é uma conclusão sobre necessidade de grampos.

A pele está explicitamente detalhada como N8. Todas as formas das barras longitudinais do grupo são retas. Existem dois contornos verticais tracejados na elevação sem identificação suficiente; não foram convertidos automaticamente em apoios adicionais.

## Entrega

- `V501_V503_detalhamento_prancha.json`: 156 campos classificados, com fontes e justificativas, inclusive incertezas.
- `V501_V503_recorte.jpg`: evidência gráfica do grupo.
- `V501_V503_corte_A.jpg`: ampliação do corte.

As classificações são `explicit`, `interpreted_graphically`, `interpreted_by_office_standard` e `uncertain`. As fontes incluem caixas de localização no PDF e itens das referências utilizadas. Os arquivos anteriores da V504 não foram modificados.
