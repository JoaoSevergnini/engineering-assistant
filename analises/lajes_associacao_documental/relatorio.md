# Etapa 9.2 — Associação documental e espacial

## Auditoria

A Etapa 9.1 separou contenção e associação, mas ainda impedia RELIABLE quando havia thin_border_review_flag. Além disso, examinava apenas interseções com o contorno candidato e descartava, para associação, todas as hipóteses de geometria não resolvidas. Foram reutilizados association_evidence, partition_domains, as etiquetas documentais, as hipóteses de barras/faixas e líderes já rastreados e a rede vetorial da Etapa 8. Nenhuma extração, ocorrência, quantitativo ou geometria original foi reescrita.

## Contextos auxiliares, sem corrigir contornos

1. Moldura em U com três lados externos vetorialmente completos, faces internas paralelas e apontador explícito da etiqueta: define uma janela auxiliar de associação. A abertura da moldura não vira limite estrutural comprovado. Na prancha, esse padrão recuperou o contexto interior de L605.
2. Dois pares opostos de faces de apoio, fechados por tampas vetoriais e com extremidades coincidentes: permitem avaliar continuidade além de uma fronteira candidata. São examinadas as quatro direções. Na prancha, D1187:0–D1194:0 sustentam o contexto inferior de L607 até o próximo alinhamento de apoios.

Esses contextos são evidências de atribuição documental, não novos contornos validados. O algoritmo não fixa L605, L607, marcas, coordenadas ou IDs de vetores. As dimensões são recuperadas dos segmentos. Não usa fecho convexo nem escolhe a laje mais próxima. Os padrões são experimentais: a janela pode incluir apoios ou vazios, devendo ser revisada quando houver concorrência documental.

Filtros experimentais: contato numérico de 0,001 pt; faces internas com sobreposição longitudinal ≥65% e afastamento ≤25% da menor dimensão da moldura; fronteira apoiada ≥80%; largura de cada faixa lateral ≤15% da fronteira. Esses parâmetros reconhecem padrões gráficos e não são tolerâncias estruturais. Sua generalização para outros escritórios ainda precisa ser testada.

## Confianças independentes

RELIABLE requer identidade/espessura documentais e suporte espacial consistente das entidades no contexto. Um alerta topológico isolado fica no campo issues.topological e não altera a associação. A confiança do contorno permanece CANDIDATE_NOT_CONFIRMED. A qualidade da geometria de atuação é registrada separadamente: hipóteses de barras/líderes permanecem hipóteses, sem seleção silenciosa ou criação de regiões físicas.

Os candidatos de geometria só são usados quando já possuem marcador de junção barra/faixa ou linha de chamada com destino sustentado. Rotas incompletas e alternativas sem suporte mantêm PROBABLE. Alternativas que indicam lajes diferentes, ou contextos concorrentes na mesma parcela, ficam INDETERMINATE. Uma ocorrência aceita pode atravessar contextos disjuntos de espessuras diferentes; cada parcela retém suas possibilidades e nenhuma altura útil única é atribuída.

## Resultado comparativo

| Associação | Etapa 9.1 | Etapa 9.2 |
|---|---:|---:|
| RELIABLE | 40 | 50 |
| PROBABLE | 8 | 6 |
| INDETERMINATE | 11 | 3 |

Transições: INDETERMINATE → INDETERMINATE: 3; INDETERMINATE → PROBABLE: 6; INDETERMINATE → RELIABLE: 2; PROBABLE → RELIABLE: 8; RELIABLE → RELIABLE: 40.

```json
{
  "occurrences": 59,
  "states": {
    "RELIABLE": 50,
    "INDETERMINATE": 3,
    "PROBABLE": 6
  },
  "changed": 16,
  "association_decisions_pending": 9,
  "geometry_reviews_pending_independently": 9,
  "multiple_slabs": 0,
  "different_thickness_domains": 0
}
```

Esses números descrevem a aplicação dos critérios experimentais, não uma taxa de acerto conferida independentemente. Não há novas confirmações humanas de associação nesta etapa.

## Casos obrigatórios

| Ocorrência | Posição | Associação | Laje / h | Interpretação e pendências |
|---|---|---|---|---|
| O019 | N25 | RELIABLE | L603 / 20.0 | Suporte documental e espacial consistente |
| O034 | N14 | RELIABLE | L603 / 20.0 | Suporte documental e espacial consistente; REINFORCEMENT em toda extensão confirmado pelo engenheiro preservado |
| O035 | N14 | RELIABLE | L603 / 20.0 | Suporte documental e espacial consistente; REINFORCEMENT em toda extensão confirmado pelo engenheiro preservado |
| O037 | N22 | PROBABLE | L607 / 20.0 | LEADER_SEARCH_INCOMPLETE |
| O038 | N22 | RELIABLE | L607 / 20.0 | Suporte documental e espacial consistente |
| O039 | N21 | RELIABLE | L607 / 20.0 | Suporte documental e espacial consistente |
| O040 | N21 | RELIABLE | L607 / 20.0 | Suporte documental e espacial consistente |
| O047 | N24 | RELIABLE | L607 / 20.0 | Suporte documental e espacial consistente |
| O050 | N25 | RELIABLE | L605 / 18.0 | Suporte documental e espacial consistente |
| O053 | N40 | RELIABLE | L605 / 18.0 | Suporte documental e espacial consistente; LAP_SPLICE confirmado pelo engenheiro preservado |
| O054 | N37 | RELIABLE | L605 / 18.0 | Suporte documental e espacial consistente |
| O055 | N35 | RELIABLE | L605 / 18.0 | Suporte documental e espacial consistente |
| O056 | N39 | RELIABLE | L605 / 18.0 | Suporte documental e espacial consistente |
| O057 | N41 | PROBABLE | L605 / 18.0 | SOME_GEOMETRY_ALTERNATIVES_LACK_ASSOCIATION_EVIDENCE |
| O058 | N36 | RELIABLE | L605 / 18.0 | Suporte documental e espacial consistente |
| O059 | N38 | RELIABLE | L605 / 18.0 | Suporte documental e espacial consistente |

O047/N24: a faixa original vai de y=959,0800 a 1006,7200 pt, enquanto o candidato L607 terminava em y=948,4000 pt. O descompasso é de contexto/contorno, não ausência de barra ou faixa: ambas já estavam extraídas. A continuidade entre faces laterais de apoio fornece associação a L607/h20 sem alterar a faixa ou o contorno.

N37/O054: os traços e a chamada já estavam associados; a ausência anterior de interseção era causada pelo contexto estreito de L605, e não por falta de extração. N41/O057: a associação candidata é L605/h18, mas permanecem alternativas de barras/faixas e uma alternativa sem suporte suficiente; a classificação é PROBABLE. N22/O037: destino de líder já extraído indica L607/h20, porém o rastreamento anterior atingiu limite de busca e a geometria continua inconclusiva. N21: grupos em lados opostos dos vazios recuperam suporte no contexto de apoios, sem classificar automaticamente os trechos externos como ancoragem.

## Pendências por natureza

- **O009/N18 — INDETERMINATE**: NO_ACTUATION_OR_SUPPORTED_GRAPHIC_HYPOTHESIS; SOME_GEOMETRY_ALTERNATIVES_LACK_ASSOCIATION_EVIDENCE.
- **O012/N17 — PROBABLE**: SOME_GEOMETRY_ALTERNATIVES_LACK_ASSOCIATION_EVIDENCE; LEADER_SEARCH_INCOMPLETE.
- **O014/N33 — INDETERMINATE**: NO_ACTUATION_OR_SUPPORTED_GRAPHIC_HYPOTHESIS; SOME_GEOMETRY_ALTERNATIVES_LACK_ASSOCIATION_EVIDENCE.
- **O016/N17 — PROBABLE**: LEADER_SEARCH_INCOMPLETE.
- **O028/N23 — INDETERMINATE**: NO_ACTUATION_OR_SUPPORTED_GRAPHIC_HYPOTHESIS; SOME_GEOMETRY_ALTERNATIVES_LACK_ASSOCIATION_EVIDENCE.
- **O037/N22 — PROBABLE**: LEADER_SEARCH_INCOMPLETE.
- **O048/N7 — PROBABLE**: SOME_GEOMETRY_ALTERNATIVES_LACK_ASSOCIATION_EVIDENCE.
- **O049/N7 — PROBABLE**: SOME_GEOMETRY_ALTERNATIVES_LACK_ASSOCIATION_EVIDENCE.
- **O057/N41 — PROBABLE**: SOME_GEOMETRY_ALTERNATIVES_LACK_ASSOCIATION_EVIDENCE.

Os alertas topológicos de L605 permanecem visíveis inclusive quando a associação é RELIABLE. A geometria estrutural e os contornos ainda não foram confirmados. Ausência de suporte geométrico não significa ausência física de armadura ou insuficiência resistente.

## Rastreabilidade e limites

O inventário completo preserva integralmente todas as camadas anteriores e acrescenta documentary_spatial_assignment. Segmentos, barras, faixas e geometrias originais mantêm coordenadas e estados históricos. spatial_context_partition é apenas uma interseção auxiliar: não substitui a região de atuação nem fornece geometria estrutural para cálculo. As parcelas externas originais não foram apagadas, nem declaradas ancoragem. Quantitativos não foram distribuídos ou somados.

N14, N40, as quatro classificações humanas locais e a inconsistência N38 estão preservadas. Não houve cálculo de altura útil, resistência ou dimensionamento. Antes de relacionar esforços, é necessário manter o vínculo com o domínio estrutural da planta de formas, a geometria de atuação e as alternativas ainda abertas.

[Mapa das associações](mapa_associacoes.png) · [Mapa de decisões pendentes](mapa_pendencias.png) · [Comparação das 59 ocorrências](comparacao_59.md) · [Inventário](associacoes.json) · [Contexto L605](L605_contexto.png) · [Apoios L607](L607_apoios.png)

## Valida??o executada

**205 testes aprovados**, incluindo 22 novos testes da Etapa 9.2. Os sint?ticos verificam moldura em U, rejei??o de molduras sem evid?ncias, continuidade entre apoios em diferentes orienta??es, remo??o do veto topol?gico, consenso/diverg?ncia entre hip?teses, m?ltiplas espessuras, aus?ncia de destino gr?fico e conflitos. As regress?es reais verificam todos os casos obrigat?rios, preserva??o integral dos dados/quantitativos e das confirma??es humanas, as 59 compara??es, determinismo e invari?ncia de cores/ordem. Nenhuma associa??o anteriormente RELIABLE foi rebaixada.

O comando de gera??o foi reexecutado com sucesso e os quatro mapas foram inspecionados quanto ? legibilidade, separa??o de pend?ncias e recorte visual. Isso n?o constitui confirma??o independente das associa??es nem valida??o estrutural dos contextos. [Registro dos testes e hashes do c?digo](validacao_testes.json).
