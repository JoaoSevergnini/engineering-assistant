# Compatibilização geométrica V501 / V503

Data: 2026-10-04. Etapa exclusivamente geométrica/documental. Não avalia
suficiência das armaduras. Resultado: o intervalo físico de cada posição
longitudinal e suas seções TQS abrangidas são determinados separadamente para
V501 e V503, preservando a incompatibilidade de 1 cm entre as faces direitas.

## Entradas, ferramenta e rastreabilidade

Foi aplicada a Skill `reinforcement-review`, suas convenções de detalhamento e
`tqs-beam-data.md`, além das instruções AGENTS e documentação das ferramentas.
As regras confirmadas pelo engenheiro são entradas desta análise, não hipóteses
deduzidas da quantidade de pontos ou de coincidências de números.

Entradas em `analises/pranchas/`:

- `V501_V503_beam_model.json`: detalhamento compartilhado, quantidades por viga.
- `V501_tqs.json` e `V503_tqs.json`: consolidados originais independentes.
- `V501_tqs_positions.json` e `V503_tqs_positions.json`: produzidos pela ferramenta
  existente `tools/extrator_lst/section_positions.py`, a partir dos respectivos
  consolidados e raw. Cinco séries VGESFS posicionadas por viga.
- `V541_tqs.json`, `V542_tqs.json`, `V559_tqs.json`, `V560_tqs.json`: relações
  de apoio e reações VGESFS, sem posição no detalhamento.

Ferramenta nova: `tools/beam_mapping/map_beam.py`. Saídas separadas:
`analises/pranchas/V501_beam_mapping.json` e `V503_beam_mapping.json`.
Cada saída contém caminhos e SHA-256 das entradas, operands geométricos com
valor/unidade/pointer/relatório/linhas, catálogos de fontes e warnings herdados.
Cada esforço aponta à série, ao valor e à posição no modelo posicionado.
Cada barra conserva sua fonte documental e identifica a translação aplicada.

Não foram modificados parsers, consolidadores, schemas existentes, esforços ou
detalhamento. Os arquivos com positions são novos produtos da ferramenta já
existente, não uma geração paralela de posições dentro do mapping.

## Sistema de coordenadas e transformação

Sistema comum em metros: origem no eixo físico do apoio esquerdo; x positivo
para a direita. O detalhamento está em centímetros a partir da face interna
esquerda. Assim, `x_common = x_detail_cm/100 + b_esq/2`.

Para ambos os casos, `b_esq=1,200 m`, portanto a translação é **+0,600 m**.
A validação documental vem da convenção explícita do beam_model e das dimensões
dos apoios selecionadas em RELDTFPS. Numericamente, x_detail=0 chega a 0,600 m;
x_detail=711 cm chega a 7,710 m. Não há translação adicional por DEPEV.

A ordem dos apoios vem de `span.support_ids`, não da ordem de `beam.supports`
(que neste caso lista primeiro o apoio direito). Os nomes são confrontados com
`written_names` dos apoios esquerdo/direito do detalhamento agrupado.

| Propriedade | V501 | V503 | Significado |
|---|---:|---:|---|
| Apoio esquerdo | P2A | P2B | eixo de origem |
| Apoio direito | P1A | P1B | direção positiva |
| L_TQS | 7,552 m | 7,552 m | intervalo S1–S13 |
| DEPEV esquerdo | 0,384 m | 0,384 m | eixo esquerdo até S1 |
| DEPEV direito | 0,494 m | 0,494 m | S13 até eixo direito |
| Largura longitudinal esquerda | 1,200 m | 1,200 m | largura física do apoio |
| Largura longitudinal direita | 1,420 m | 1,420 m | largura física do apoio |
| Distância entre eixos | 8,430 m | 8,430 m | 0,384 + 7,552 + 0,494 |
| Distância livre TQS | 7,120 m | 7,120 m | 8,430 − 0,600 − 0,710 |
| Distância livre detalhada | 7,110 m | 7,110 m | beam_model, /spans/0 |
| Diferença absoluta | 0,010 m | 0,010 m | **mismatch**, sem tolerância |

Os DEPEV consensuais originais são null por conflito entre relatórios. O mapping
seleciona expressamente as alternativas RELDTFPS já normalizadas no consolidado;
não preenche os null nos modelos originais nem apaga as alternativas divergentes.
Ausência/conflito dentro da fonte escolhida impede a saída; não há fallback.

## Eixos, faces e esquema

| Referência | Coordenada comum (m), ambas as vigas |
|---|---:|
| Eixo esquerdo | 0,000 |
| S1 | 0,384 |
| Face interna esquerda | 0,600 |
| Face direita do detalhamento | 7,710 |
| Face direita TQS | 7,720 |
| S13 | 7,936 |
| Eixo direito | 8,430 |

```text
Esquema sem escala; coordenadas em m:

eixo E    S1   face E                             face D detalhe / TQS    S13   eixo D
  |-------o------|========================================||---------------o------|
0,000   0,384  0,600                                 7,710 / 7,720      7,936  8,430
  <0,384>                                                          <---0,494--->
          <------------------ L_TQS = 7,552 ------------------------->
                 <------- livre detalhado = 7,110 ------->
                 <-------- livre TQS = 7,120 ------------->

S1--S2--S3--S4--S5--S6--S7--S8--S9--S10--S11--S12--S13
```

S1 e S13 ficam dentro dos apoios físicos, fora do intervalo livre entre faces.
Isso decorre das coordenadas confirmadas; não foram deslocadas nem limitadas
às faces. A separação entre as duas faces direitas permanece explicitamente
0,010 m. Os eixos dos apoios não são inferidos a partir do comprimento PDF.

## As 13 seções consumidas

Valores abaixo exibidos com seis casas somente para leitura. Os JSON preservam
os números completos recebidos de section_positions.py, incluindo representação
binária de floats; não há arredondamento, snapping ou recálculo no mapping.

| Seção | V501 x (m) | V503 x (m) |
|---:|---:|---:|
| 1 | 0,384000 | 0,384000 |
| 2 | 1,013333 | 1,013333 |
| 3 | 1,642667 | 1,642667 |
| 4 | 2,272000 | 2,272000 |
| 5 | 2,901333 | 2,901333 |
| 6 | 3,530667 | 3,530667 |
| 7 | 4,160000 | 4,160000 |
| 8 | 4,789333 | 4,789333 |
| 9 | 5,418667 | 5,418667 |
| 10 | 6,048000 | 6,048000 |
| 11 | 6,677333 | 6,677333 |
| 12 | 7,306667 | 7,306667 |
| 13 | 7,936000 | 7,936000 |

São preservadas separadamente as cinco séries: momento max/min, cortante
max/min e torção max, todas stage=model_input, unidades kN.m ou kN. Cada ponto
contém quantity, envelope, stage, unit, section, position, value e provenance.
Não se escolhe Msd nem se altera sinal, valor ou majoração. As nove séries do
consolidado sem correspondência posicionada ficam em `unmapped_tqs_series`,
incluindo metadados e fontes; não recebem coordenadas por analogia.

## Armaduras longitudinais e cobertura

Funções abaixo são as classificações explícitas do beam_model, não inferências
pela posição, diâmetro ou esforços. Todos os intervalos são fechados.
Camadas são preservadas como vetores do modelo; não se determina altura útil.

| Marca | Função documental | Barras × Ø (mm) | Camadas | Intervalo detalhe (cm) | Intervalo comum (m) | Seções abrangidas V501 / V503 |
|---|---|---|---|---|---|---|
| N1 | negative | 2 × 16 | [2] | −62 a 403 | −0,020 a 4,630 | 1–7 / 1–7 |
| N2 | negative | 2 × 16 | [1,1] | −62 a 198 | −0,020 a 2,580 | 1–4 / 1–4 |
| N3 | negative | 2 × 20 | [2] | 306 a 791 | 3,660 a 8,510 | 7–13 / 7–13 |
| N4 | negative | 2 × 20 | [1,1] | 488 a 789 | 5,480 a 8,490 | 10–13 / 10–13 |
| N5 | positive | 4 × 12,5 | [3,1] | −53 a 762 | 0,070 a 8,220 | 1–13 / 1–13 |

N3/N4 ultrapassam o eixo direito; seus intervalos são transportados integralmente,
sem truncamento, interpretação de ancoragem ou validação de extensão necessária.
Cada barra inclui `covered_tqs_points` com todos os esforços das seções abrangidas.
Não se interpola entre pontos e não se busca máximo entre seções discretizadas.

Pele N8: 6 barras Ø8, três por face, intervalo detalhado −24 a 736 cm;
intervalo comum 0,360 a 7,960 m, seções 1–13. Preservada separadamente.
Regiões de estribos também têm translação exclusivamente geométrica:
R1/N6: 0,600–5,970 m, seções 2–9; R2/N7: 5,970–6,690 m, seções 10–11;
R3/N6: 6,690–7,710 m, seção 12. A ligação documental N7/IB1 permanece no
detalhamento, sem identificar qual viga/reação corresponde a IB1.

## Diferenças entre os dois mappings

A igualdade geométrica resulta de operandos lidos independentemente para as duas
vigas; não foi deduzida do agrupamento do detalhamento. Há arquivos, hashes,
apoios, fontes, esforços e relações de reação próprios.

Exemplo na seção 8, x=4,789333… m: momento max/model_input é
**61,5073088 kN.m em V501** e **62,3114541 kN.m em V503**.
Ambos são disponibilizados para N3 e N5, cujos intervalos abrangem S8; nenhum é
escolhido para representar a outra viga. Não há média ou envelope conjunto.

## Apoios indiretos e reações transportadas

| Viga apoiada → receptora | Máximo (kN) | Mínimo (kN) | Fonte documental |
|---|---:|---:|---|
| V541 → V501 | 28,50793155 | 22,3983886 | VGESFS.LST, linha 828, raw /categorias/apoios/20 |
| V542 → V501 | 38,11844855 | 7,10982125 | VGESFS.LST, linha 1358, raw /categorias/apoios/20 |
| V559 → V503 | 28,56677145 | 22,3983886 | VGESFS.LST, linha 954, raw /categorias/apoios/20 |
| V560 → V503 | 39,05988695 | 8,6886919 | VGESFS.LST, linha 1647, raw /categorias/apoios/20 |

Esses são resultados do software, transportados sem interpretação de combinação
ou cálculo de suspensão. Em cada relação, x, drawing_indirect_support_id e
reinforcement_mark são null. IB1/IB2 e a associação documental IB1/N7 permanecem
em contexto separado; não há ligação automática às quatro relações acima.

## Evidências documentais essenciais

Linhas são as registradas pelos modelos raw/consolidados; relatórios pertencem
ao pavimento DIFERENCIADO do projeto, conforme `source_files` dos arquivos raw.
O mapping não relê os LST nem substitui os números já extraídos.

| Dado | V501: relatório / linha / referência | V503: relatório / linha / referência |
|---|---|---|
| L_TQS 7,552 m | VGESFS / 1364 / s532#/normalizacao/campos/comprimento | VGESFS / 1653 / s537#/normalizacao/campos/comprimento |
| Esquerda: largura 1,200, DEPEV 0,384 m | RELDTFPS / 12766 / s157, /normalizacao/campos/largura e excentricidade | RELDTFPS / 15276 / s157, mesmos campos |
| Direita: largura 1,420, DEPEV 0,494 m | RELDTFPS / 12767 / s158, /normalizacao/campos/largura e excentricidade | RELDTFPS / 15277 / s158, mesmos campos |
| Série momento max | VGESFS / 1373 / s537#/normalizacao | VGESFS / 1662 / s542#/normalizacao |
| Livre 711 cm, origem face esquerda | V501_V503_beam_model.json /spans/0 e /coordinate_system | mesmo detalhamento, sem inferir igualdade dos esforços |
| Intervalos N1–N4 | documental /longitudinal_reinforcement/negative/0…3 | mesmo documental |
| Intervalo N5 | documental /longitudinal_reinforcement/positive/0 | mesmo documental |

A dimensão mostrada nos apoios do detalhamento é 120/142 cm; os respectivos
nomes escritos estão em /supports/0 e /supports/1 do documental. A translação
usa dimensão longitudinal TQS selecionada, não `width_cm=null` do beam_model.
O null documental não foi preenchido nem reinterpretado como zero.

## Dados não mapeáveis e inconsistências preservadas

- Face direita PDF a 7,710 m versus TQS a 7,720 m: mismatch explícito. Nenhum
  critério de tolerância/aceitação foi definido.
- Conflitos de DEPEV entre fontes continuam nos warnings. A fonte RELDTFPS é
  uma política confirmada pelo engenheiro, não resolução geral do consolidador.
- Nove séries originais por viga não possuem positions utilizáveis nesta etapa.
- Coordenadas de IB1/IB2, identificação individual das vigas apoiadas no PDF e
  vinculação reação–IB–barra não estão documentadas.
- Coordenada do Corte A, cobrimento documental, espaçamento vertical da pele,
  offsets do primeiro/último estribo e natureza/vínculos dos apoios permanecem
  conforme incertezas do detalhamento. Cortes não são extrapolados ao vão.
- Materiais TQS originais ainda contêm conflitos/null; não foram resolvidos
  nesta ferramenta geométrica, mesmo havendo política futura de fck em MPa.
- Primeira versão rejeita múltiplos vãos/balanços e convenções diferentes de
  origem/sentido/unidade: requer extensão explícita antes desses casos.

## Hipóteses não adotadas

Não se assumiu que L_TQS é distância entre eixos ou distância livre; que DEPEV
é offset da face; que 711=712; que o agrupamento implica esforços iguais; que
seção fora do vão livre é inválida; que comprimento desenvolvido determina
intervalo longitudinal; que barras sem função explícita são positivas/negativas;
que IB1/IB2 representam a ordem das reações; que N7 recebe reação específica;
que max/min publicados já representam solicitação de cálculo adequada.
Não há escala, distribuição de erro, extensão/truncamento de barras, alteração
de detalhamento, interpolação, capacidade resistente ou cálculo estrutural.

## Testes e limites para a próxima etapa

Executados: 22 testes unitários/regressão em tools/beam_mapping, 39 testes em
tools/extrator_lst e 29 em tools/beam_model: **90 testes aprovados**. A suíte nova cobre
translação, faces, ordem de apoios, preservação de posições e esforços, intervalos
reais, bordas exatas, intervalos vazios/desconhecidos, independência V501/V503,
reações sem associação inventada, rejeições e imutabilidade das entradas.

Antes de iniciar verificações estruturais será necessário definir explicitamente:

1. tratamento de engenharia da divergência 711/712 cm, sem presumir aceitação;
2. séries, estágio, unidades e critérios de combinação/majoração de esforços
   pertinentes a cada verificação, preservando alternativas;
3. materiais de cálculo e fonte escolhida, cobrimentos/camadas/altura útil com
   evidência documental suficiente;
4. posições e identificação das ligações indiretas, caso sejam necessárias para
   verificações locais, e associação explícita às regiões de detalhamento;
5. representação de múltiplos vãos e coordenadas globais para expandir o escopo.

O critério desta etapa foi atendido: N1–N5 têm intervalos físicos e cobertura
discreta determinados para cada viga, com seus próprios esforços. Isso não
constitui aprovação de nenhuma armadura ou conclusão de segurança estrutural.

## Arquivos desta etapa

Criados:

- `tools/beam_mapping/map_beam.py`
- `tools/beam_mapping/test_map_beam.py`
- `tools/beam_mapping/README.md`
- `analises/pranchas/V501_tqs_positions.json`
- `analises/pranchas/V503_tqs_positions.json`
- `analises/pranchas/V501_beam_mapping.json`
- `analises/pranchas/V503_beam_mapping.json`
- `.codex/analises/V501_V503_beam_mapping.md`

Nenhum arquivo-fonte preexistente foi modificado nesta etapa. A execução de
Python/testes também produz caches `__pycache__`, sem alteração de código-fonte.
