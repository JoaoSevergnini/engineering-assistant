# Etapa 9 — Associação geométrica a lajes e espessuras

## Auditoria e método

Reutilizados os 35 polígonos da Etapa 5, os grupos e traços localizados da Etapa 4 e os nove contornos candidatos da Etapa 8. Nenhum reconhecimento documental, contorno ou partição anterior foi alterado. Shapely executa interseção e diferença, preservando os pontos originais; novos vértices são interseções geométricas derivadas. Não há seleção por centroide, proximidade de etiqueta, cor, BASE ou REFORÇO.

Cada ocorrência distribuída é particionada por domínio candidato; a extensão longitudinal continua vinculada à barra e a transversal ao eixo de distribuição. Comprimento nominal C não foi convertido em projeção. Grupos localizados são associados por comprimento dos traços, sem envoltória fictícia. Contatos sem área não associam regiões distribuídas; traços exatamente sobre uma borda continuam sujeitos à incerteza do contorno.

Nome e espessura são dados documentais: suas etiquetas, IDs, coordenadas e textos de espessura estão no inventário de domínios. Os recortes são interpretações geométricas. Todas as associações reais são provisórias: RELIABLE exige contorno confirmado; PROBABLE identifica interseção com candidato único; INDETERMINATE registra partes descobertas, domínios concorrentes ou geometria não comprovada. A classe da ocorrência adota a pior classe de suas parcelas. Não foi realizada nova confirmação humana das associações.

## Resultados

```json
{
  "occurrences": 59,
  "states": {
    "INDETERMINATE": 47,
    "PROBABLE": 12
  },
  "with_slab_intersection": 48,
  "multiple_slabs": 0,
  "different_thickness_domains": 0,
  "without_actuation_geometry": 9
}
```

Há interseções em 34 ocorrências DISTRIBUTED e 14 LOCALIZED. Doze ocorrências têm somente parcelas PROBABLE; 36 combinam parcelas prováveis com partes descobertas e ficam globalmente INDETERMINATE. O047/N24 e O054/N37 têm geometria recuperada, mas nenhuma interseção com os domínios candidatos. Outras nove não possuem geometria de atuação comprovada. Nenhuma associação é RELIABLE porque nenhum contorno utilizado está confirmado. Não houve ocorrência em múltiplos domínios nesta execução real; o cruzamento de espessuras foi demonstrado apenas em testes sintéticos.
As parcelas mantêm referência à chamada e ao grupo físico original. quantity_allocation é nulo: não se distribuem barras ou quantitativos por laje, nem se somam ocorrências repetidas. Medidas em pt²/pt descrevem geometria da prancha, não área de aço ou dimensão física calibrada.

## Classificações preservadas

N14/R034 e R035: função REINFORCEMENT confirmada pelo engenheiro em toda a extensão das respectivas ocorrências. R053/N40: interpretação LAP_SPLICE confirmada pelo engenheiro; parceiro e extensão efetiva do traspasse continuam pendentes. O candidato anterior de N40 como reforço permanece apenas como histórico e é superado pela camada humana atual. Não se aplica a ele a conclusão anterior de contenção como se fosse reforço. As confirmações são dados externos, vinculados ao hash do PDF, ocorrência e geometria, sem regras de produção por marca.

As quatro confirmações locais C059, C083, C092 e C073 e a inconsistência documental N38 permanecem integralmente no inventário anterior. Nenhuma classificação foi propagada a outras células por esta etapa.

## Pendências e próxima etapa

Conferir os contornos candidatos, em especial a faixa estreita de L605 e os anéis internos gráficos, que ainda não comprovam vazios estruturais. Parcelas fora dos domínios são preservadas: não significam ausência de laje nem falha resistente. Várias lajes possíveis na ocorrência não equivalem a uma associação confirmada; consultar os motivos e os polígonos de cada parcela. As nove representações sem geometria suficientemente comprovada não recebem laje pela posição de seu texto.

Recomenda-se conferir os recortes com a planta de formas e revisar as associações listadas abaixo. Espessura documental não fornece altura útil: cobrimento, camada e posição efetiva continuam necessários. Não houve cálculo resistente, soma de contribuições ou alteração do PDF.

[Mapa distribuídas](mapa_distribuidas.png) · [Mapa localizadas](mapa_localizadas.png) · [Múltiplas lajes](multiplas_lajes.md) · [Pendências](pendencias.md) · [Inventário](associacoes.json)

## Valida??o executada

Su?te completa: **166 testes aprovados**, incluindo 15 novos testes da Etapa 9. Testes sint?ticos cobrem cruzamento entre espessuras, contatos, concorr?ncia, an?is internos, tra?os verticais e invari?ncia ? ordem/cor. Regress?es reais verificam conserva??o de ?rea/comprimento, 59 ocorr?ncias, proveni?ncia, confirma??es humanas, determinismo e preserva??o integral das camadas anteriores. Esses testes n?o substituem confer?ncia geom?trica independente pelo engenheiro. [Registro da execu??o](validacao_testes.json).
