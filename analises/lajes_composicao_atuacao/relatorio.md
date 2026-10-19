# Etapa 10 — Regiões de atuação e composição

## Auditoria e reutilização

Reutilizados os 35 polígonos da Etapa 5, as 119 células originais, as relações com escopo da Etapa 7, os contornos candidatos da Etapa 8 e as atribuições da Etapa 9.2. Não houve nova extração, nova partição ou recorte por laje. Das 59 ocorrências, 35 têm envoltórias distribuídas sustentadas por barra/eixo; 15 localizadas têm traços, sem região de área comprovada; nove continuam pendentes. RELIABLE na associação não transforma hipótese de geometria em área física validada.

## Critérios

SINGLE_REINFORCEMENT registra uma ocorrência gráfica distribuída na direção/camada examinada. BASE_PLUS_REINFORCEMENT exige função conjunta confirmada localmente ou papéis humanos compatíveis de base/reforço com sobreposição vetorial. MULTIPLE_REINFORCEMENTS exige suporte explícito da combinação completa; não há caso comprovado nesta prancha. LAP_SPLICE é aplicado a domínio de traspasse confirmado localmente. As demais interseções ficam UNRESOLVED_COMPOSITION. Funções candidatas BASE/REFORÇO, dimensões pequenas e igualdade de marcas não autorizam composição adicional.

Os papéis humanos N13=base e N14=reforço em toda extensão sustentam relações de função nas interseções dos pares esquerdo e direito. A origem dessa confirmação é a solicitação da Etapa 10, seção 5; os dados externos são vinculados ao hash do PDF, ocorrências e geometrias. O algoritmo não contém regras por marca. Camadas exatas e independência para soma numérica continuam não autorizadas. Nenhum resultado calcula As/m, altura útil ou momento resistente.

## Resultados

```json
{
  "occurrences": 59,
  "area_regions": 35,
  "eligible_area_regions": 35,
  "localized_trace_only": 15,
  "pending_geometry": 9,
  "composition_records": 119,
  "original_geometric_cells": 119,
  "classifications": {
    "SINGLE_REINFORCEMENT": 70,
    "BASE_PLUS_REINFORCEMENT": 3,
    "MULTIPLE_REINFORCEMENTS": 0,
    "LAP_SPLICE": 1,
    "UNRESOLVED_COMPOSITION": 45
  },
  "documentary_lap_pending_cells": 4,
  "consolidated_blocks": 77
}
```

Todas as células retêm C original e um ID derivado estável. O agrupamento em blocos exige as mesmas ocorrências, direção/camada, função, evidências e continuidade geométrica. Partes desconectadas e ocorrências distintas de uma mesma marca não são fundidas. As áreas são em pt² da prancha, não áreas de aço.

## L603 — comparação N13/N14

| Base | Reforço | Área de sobreposição gráfica (pt²) | Área de células com somente essa N13 (pt²) | Células com terceiros ainda pendentes |
|---|---|---:|---:|---|
| O044/N13 | O035/N14 | 39895.018 | 95788.379 | C076 |
| O043/N13 | O034/N14 | 39874.159 | 95840.516 | C071 |

C083 preserva a confirmação local N13+N14 à esquerda. C088 recebe função conjunta sustentada pelos papéis confirmados e pela geometria à direita. C071/C076 preservam o subconjunto N13+N14 sustentado, mas ficam pendentes quanto à contribuição adicional de N15. C059 continua base+reforço confirmado localmente, sem ampliar essa confirmação para todas as ocorrências N15. A N14 permanece reforço também fora da interseção com N13; isso não comprova automaticamente sua composição com outras bases.

## L605 — N40 e traspasses

R053/N40 mantém o papel humano LAP_SPLICE. As quatro células que a contêm (C109, C110, C115 e C116) não recebem função de reforço nem soma adicional: ficam UNRESOLVED_COMPOSITION porque parceiro e zona exata do traspasse não foram confirmados. A borda laranja tracejada no mapa mostra o escopo da representação documental, não um comprimento de traspasse comprovado. C092 mantém LAP_SPLICE no domínio exato da confirmação anterior. C073 permanece residual gráfico confirmado, mapeado como composição não resistente pendente, sem exclusão de sua geometria.

## L607 — barras, faixas e apoios

N24/O033 e O047 mantêm suas regiões distribuídas integrais, inclusive fora do contorno candidato. A associação L607/h20 é documental/espacial. N21/O039/O040 e N22/O038 são traços localizados: não foi inventada área retangular nem contribuição distribuída. N22/O037 permanece pendente de geometria/rastreamento. Nenhuma parcela externa é declarada ancoragem ou contribuição resistente de apoio.

## Pendências e comparação com etapas anteriores

As nove pendências de associação/geometria da Etapa 9.2 permanecem: O009, O012, O014, O016, O028, O037, O048, O049, O057. Nenhuma produz área elegível. As 45 composições pendentes incluem sobreposições sem interpretação física, o residual confirmado e o escopo documental de N40 ainda não delimitado como zona de traspasse. Não se buscou reduzir esse número artificialmente.

Foram preservadas as 35 regiões e as 119 células. Em relação às quatro classificações humanas locais: duas base+reforço e um traspasse continuam nas mesmas geometrias; o residual permanece registrado com seu significado original e não vira contribuição. C088 é a nova composição base+reforço sustentada pela confirmação atual. As relações candidatas anteriores permanecem no histórico e não são promovidas por transitividade.

## Consulta e entregáveis

[Consulta interativa local](consulta_regioes.html) — clique na prancha ou busque C, R, O ou N para consultar membros e motivos. O arquivo usa somente a imagem e os dados locais, sem serviços externos.

[Mapa das composições](mapa_composicoes.png) · [Regiões individuais](regioes_individuais.png) · [L603 esquerda](L603_esquerda.png) · [L603 direita](L603_direita.png) · [L605/N40](L605_N40.png) · [L607](L607_tracos_e_faixas.png)

[Regiões de atuação](regioes_atuacao.json) · [Composições](composicoes.json) · [Blocos consolidados](blocos.json) · [Pendências](pendencias.json) · [Comparação rastreável com etapas anteriores](comparacao_etapas.json)

Consulta por coordenadas PDF: `python tools/slab_geometry_poc/run_acting_compositions.py --query X Y`. Pontos em fronteiras devolvem todas as células incidentes, sem seleção por proximidade.

## Limitações e próxima etapa

As envoltórias são interpretações gráficas sustentadas por entidades vetoriais, não geometria física integralmente confirmada. As 15 representações localizadas exigem modelo próprio de atuação para verificações futuras. A composição documental não autoriza soma numérica com camadas desconhecidas, regiões de apoio, duplicidade ou traspasse. A próxima etapa deve manter esses bloqueios, resolver ambiguidades relevantes e comprovar posicionamento/camadas antes de calcular altura útil ou composições resistentes. Não foi feita verificação normativa ou aprovação estrutural.

## Valida??o executada

**231 testes aprovados**, incluindo 26 novos da Etapa 10. Os sint?ticos cobrem base isolada, base+refor?o, mesma marca em ocorr?ncias distintas, m?ltiplas bases com validade espacial restrita, traspasse sem duplica??o, dire??es/camadas diferentes, conflito humano e geometria inconclusiva apesar de associa??o confi?vel. As regress?es reais verificam N13/N14 esquerda/direita, N40, L607, as nove pend?ncias, residual humano, coordenadas originais, uni?o dos blocos e determinismo. As 119 c?lulas possuem coordenadas originais id?nticas ?s anteriores. Sucesso computacional n?o significa valida??o estrutural.

A consulta CLI retornou C088/N13+N14 para o ponto PDF (1380,800). A l?gica JavaScript do HTML foi executada com DOM m?nimo simulado: busca C088, separa??o das duas N14, clique C088, nove pend?ncias e controle de zoom funcionaram. **A renderiza??o e a intera??o em navegador real n?o foram conferidas**, porque o navegador integrado n?o estava dispon?vel nesta sess?o. Os mapas est?ticos foram inspecionados; o HTML deve permanecer junto de prancha_original.png. [Registro dos testes](validacao_testes.json).
