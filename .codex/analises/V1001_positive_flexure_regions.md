# V1001 — mapping confirmado e flexão positiva por regiões

04/10/2026. Contexto de duas torres confirmado pelo engenheiro. Verificação
limitada à composição geométrica e capacidade à flexão positiva nos pontos TQS
existentes. Não aprova viga/detalhamento nem autoriza corte de N3.

## 1. Entradas e resolução dos apoios

Entradas em analises/pranchas: V1001_beam_model.json, V1001_tqs.json,
V1001_tqs_positions.json, V1001_tqs_raw.json e V1001_V9001_support_context.json.
Modelos relacionados V1014_tqs.json/V1015_tqs.json também foram fornecidos ao
mapper. Saídas: V1001_beam_mapping.json e V1001_positive_flexure_regions.json.

O engenheiro confirmou que o detalhe V1001 também representa V9001 nas duas
torres. Os blocos individuais VGESFS/RELDTFPS fornecem V1001 → P2A/P1A e
V9001 → P2B/P1B. A resolução usa contexto explícito e sequência TQS, com
labels/candidatos/evidências preservados. Não escolhe o primeiro nome e não
altera o beam_model. Apenas V1001 foi verificada; esforços V9001 não foram usados.

| Lado | Label documental | Candidatos declarados | ID TQS V1001 |
|---|---|---|---|
| Esquerdo | P2A/P2B | P2A, P2B | P2A |
| Direito | P1A/P1B | P1A, P1B | P1A |

Origem original: `face interna do apoio esquerdo P2A/P2B`; tipo interpretado:
left_support_inner_face; referência P2A/P2B; apoio resolvido P2A. Origem comum:
eixo esquerdo, x positivo para a direita, em metros.

## 2. Geometria e transformação

L_TQS=7,552 m; DEPEV esquerda/direita=0,384/0,494 m; dimensões longitudinais
1,20/1,42 m. Seleção de fontes conserva a política VGESFS/RELDTFPS.

```text
eixo E      S1     face E                          face D   S13    eixo D
0,000       0,384  0,600                           7,720    7,936  8,430 m
|------------|------|================================|--------|------|
                      vão livre 7,120 m

x_comum = x_detail_cm/100 + 0,600
N3:             [0,180 ------------------ 6,680]
N5:             [0,180 ---------------------------------- 8,130]
N9 Ø5:                 [0,600 ------------------- 7,720]
```

Vão livre documental e TQS=7,120 m; diferença=0; status exact. Não houve
escala, ajuste de barras ou offset DEPEV adicional. Igualdade métrica não prova
identidade de revisão: PDF 03/07/2026 e relatórios 03/10/2026.

N3: 2Ø10, lower, layers=[2], −42..608 cm → 0,180..6,680 m.
N5: 2Ø10, lower, layers=[2], −42..753 cm → 0,180..8,130 m.
Ambas ocupam a primeira camada documental; a lógica genérica compõe 4Ø10
na sobreposição e 2Ø10 após N3. Não há regra específica por marca.

## 3. Regiões e pontos discretos

Intervalos documentais permanecem fechados. A convenção genérica atribui o
limite à região compatível: x=6,680 pertence à composição N3+N5. Sem epsilon.

| Região | Intervalo comum (m) | Armadura | Pontos TQS | Resultado |
|---|---|---|---|---|
| R1 | [0; 0,180) | nenhuma positiva documentada | nenhum | demand_not_sampled; geometria não resolvida |
| R2 | [0,180; 0,600) | N3+N5, 4Ø10 | S1 | somente negativo; estribo desconhecido |
| R3 | [0,600; 6,680] | N3+N5, 4Ø10 | S2–S11 | capacidade comparada |
| R4 | (6,680; 7,720] | N5, 2Ø10 | S12 | somente negativo |
| R5 | (7,720; 8,130] | N5, 2Ø10 | S13 | somente negativo; estribo desconhecido |
| R6 | (8,130; 8,430] | nenhuma positiva documentada | nenhum | demand_not_sampled; geometria não resolvida |

| Seção | x comum (m, exibido arredondado) | Msk série M MX. (kN.m) | Região |
|---|---:|---:|---|
| 1 | 0,384000 | −37,54966285 | R2 |
| 2 | 1,013333 | −9,414384 | R3 |
| 3 | 1,642667 | 15,07282105 | R3 |
| 4 | 2,272000 | 35,9119523 | R3 |
| 5 | 2,901333 | 53,10300975 | R3 |
| 6 | 3,530667 | 59,8401783 | R3 |
| 7 | 4,160000 | 56,10384465 | R3 |
| 8 | 4,789333 | 50,23946795 | R3 |
| 9 | 5,418667 | 39,9130655 | R3 |
| 10 | 6,048000 | 25,05599075 | R3 |
| 11 | 6,677333 | 3,16754795 | R3 |
| 12 | 7,306667 | −26,0072358 | R4 |
| 13 | 7,936000 | −59,63423865 | R5 |

Posições completas preservadas no JSON, sem arredondamento operacional.
S11 fica 0,002666666666667 m antes do término geométrico de N3. Não se
interpola até esse término nem se avalia corte/ancoragem.

## 4. Seleção auditada e chamada real Concretopy

Reutilizado audited_moment_series: VGESFS, registro original M MX., vão 1,
quantity bending_moment, envelope max, stage model_input, unidade kN.m e
valores normalizados conferidos com o raw. A natureza característica Msk é a
política confirmada pelo engenheiro; não é deduzida apenas do nome max.
VGESFS linha 500; provenance normalizada s541#/normalizacao. Governante R3:
S6, x=3,5306666666666664 m, Msk=59,8401783 kN.m. Negativos são preservados,
mas inelegíveis. Não há interpolação ou extrapolação.

Entrada real R3: seção retangular bw=19 cm, h=72 cm; cobrimento inferior
TQS=2,5 cm; estribo N9 Ø5 mm; fck=40 MPa; CA-50 normalizado fyk=500 MPa;
uma camada 4Ø10, d omitido. Es=210000 MPa, gamma_c=1,4 e gamma_s=1,15
como defaults explícitos da API; gamma_f=1,4 documental. Armadura mínima
não solicitada. Materiais e coeficientes mantêm provenance no JSON.

API: verificar_flexao_viga_retangular, do repositório irmão concretopy.
Não alterado. Nenhuma equação resistente local. O posicionamento automático
da biblioteca forneceu d=68,5 cm. Resultado integral em
/regions/2/concretopy_result, chamada em /regions/2/concretopy_call.

## 5. Capacidade e diagnósticos independentes

| Resultado Concretopy R3 | Valor |
|---|---:|
| As total/única camada | 3,141592653589793 cm² |
| d camada e equivalente | 68,5 cm |
| Linha neutra x | 3,7002201802275794 cm |
| x/d | 0,05401781285003766 |
| Limite x/d retornado | 0,45 |
| MRd | 91,54315780737119 kN.m |
| Mk equivalente | 65,387969862408 kN.m |
| Utilização Msk/Mk | 0,9151557759924052 |

Mk equivalente ≥ Msk: capacidade suficiente **somente para a solicitação
positiva analisada em R3**. Hipóteses válidas=true; ductilidade=true; mínimo=null
(não solicitado); anchorage_checked=false; reinforcement_development_checked=false.
O aviso de d automático, deformações, camadas escoadas e parâmetros completos
foram preservados no JSON, incluindo MRd e Mk originais em kN.cm.

R4 não recebe chamada Concretopy porque não há Msk positivo elegível. Sua
composição 2Ø10 foi resolvida geometricamente, mas não foi inventada demanda.
Resumo: 6 regiões, 1 verificada, 4 com bloqueadores, 2 sem pontos, 3 sem demanda
positiva, 5 não verificadas; incomplete=true. O campo all_checked_regions_capacity_sufficient
é true apenas para a única comparação concluída; não significa aprovação do vão.

## 6. Provenance, limitações e testes

Contexto registra confirmação do engenheiro, labels, candidatos, IDs por membro,
arquivos e linhas LST. Mapping registra operandos, origem, fontes e hashes das
entradas/contexto. Verificação registra ponteiros documentais por marca, intervalos
originais, transformação, pontos, série, governante, materiais e hashes da API
Concretopy e dos módulos de orquestração. Não duplica arquivos-fonte completos.

Relações documentais V1014/V1015 → V1001 continuam conhecidas pela investigação,
mas indirect_relations ficou vazio: os registros consolidados relacionados não
fornecem IDs utilizáveis para o transporte automático. Corrigida somente a falha
de execução de replace em support_id=null; não foi inferida reação ou associação.
Não modificados parsers/consolidadores. Essa lacuna não altera a flexão positiva
discreta verificada, mas continua pendente para futura análise de apoios indiretos.

Suíte integral executada: 39 extrator_lst + 29 beam_model + 33 beam_mapping +
52 reinforcement_checks = **153 testes aprovados**. Inclui casos de resolução
A/B, bloqueios de ambiguidade/ausência de contexto, golden real V1001, chamada
Concretopy real, exclusão dos negativos, intervalo N3/N5, diagnósticos e comparação
integral do mapping V501 anterior. Regressão V501 preservada exatamente:
Msk=61,5073088; Mk=99,47034565405093 kN.m; utilização=0,618348196093708.

Não implementados ancoragem, desenvolvimento, deslocamento do diagrama,
escalonamento normativo, interpolação ou outras resistências. O término de N3
representa presença geométrica desenhada; não é conclusão sobre onde pode ser cortada.
