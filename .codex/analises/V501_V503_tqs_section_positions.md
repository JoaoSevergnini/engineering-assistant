# V501/V503 — investigação documental das 13 seções de esforços

Data: 03/10/2026. V501 é o caso principal; V503 foi conferida separadamente nos seus próprios registros. Esta investigação trata exclusivamente de geometria e semântica documental. Não executa verificações estruturais, não interpola esforços e não modifica o pipeline.

## Atualização confirmada pelo engenheiro em 04/10/2026

Esta atualização substitui as pendências de origem, sentido e identificação
de length na conclusão investigativa abaixo. O restante permanece como registro
das hipóteses e evidências examinadas em 03/10/2026.

- A origem x=0 é o eixo físico do primeiro apoio; os afastamentos ficam para
  dentro do vão ou coincidem com os eixos.
- O comprimento de VGESFS é **L_13=length=755,2 cm** nestes dois casos,
  confirmado pelo engenheiro, não apenas inferido da abscissa do máximo.
- A seção 1 fica em x=DEPEV_esq; a seção 13 em x=DEPEV_esq+length.
- A expressão anterior que colocou o eixo direito em x=length foi corrigida.
  O eixo direito fica em x=length+DEPEV_esq+DEPEV_dir.
- Utilizar RELDTFPS para DEPEV e demais dados geométricos, VGESFS para
  comprimento discretizado, solicitações e reações; não utilizar RELDTVeT
  como fonte operacional atual. Os dados históricos não foram apagados.

Para V501 e V503, com valores próprios documentalmente conferidos:

```text
L_13 = 755,2 cm
Delta_x = 755,2/12 = 62,933333... cm
x_i = 38,4 + (i-1)*755,2/12
x_1 = 38,4 cm
x_13 = 793,6 cm
x_eixo_direito = 793,6 + 49,4 = 843,0 cm
```

A tabela H1 abaixo usa origem auxiliar na seção 1: somar 38,4 cm para obter
as coordenadas no sistema confirmado com origem no eixo físico esquerdo.
Sua seção 8 fica, portanto, em **x=478,933333 cm** nesse sistema. A origem e
a apresentação de `Abcis.=440` no RELGER continuam não esclarecidas; esse
campo não deve substituir a regra confirmada nem ser tratado como abscissa
no mesmo sistema automaticamente.

As perguntas 1 e 3 do item 9, bem como a parte da pergunta 2 relativa à origem
das 13 seções, estão respondidas. A política de fonte de DEPEV também foi
definida. A confirmação semântica não preenche `positions`: código, schemas
e JSONs continuam sem alteração nesta atualização documental.

## Registro histórico da investigação de 03/10/2026

**Resultado:** 755,2 cm é o candidato mais bem sustentado para o intervalo seção 1–seção 13 nestes casos. Com as seções deslocadas para dentro do vão pelos DEPEV de RELDTFPS/RELDTFNG, esse intervalo decorre geometricamente das duas regras confirmadas. A aplicação ao modelo consolidado permanece pendente: o sentido dos afastamentos e a referência de `X=0` precisam ser explicitados, e a seleção entre DEPEV conflitantes não foi autorizada. A proximidade com `Abcis.=440` é evidência adicional, não prova independente da origem.

## 1. Regra permanente registrada antes da investigação

Atualizada a referência [tqs-beam-data.md](../../.agents/skills/reinforcement-review/references/tqs-beam-data.md), seção “Seções de esforços ao longo do vão”, com a regra fornecida e confirmada pelo engenheiro responsável:

- O TQS apresenta 13 seções por vão, no sistema local identificado como `X=0`.
- A seção 1 está afastada do eixo do primeiro apoio pelo seu DEPEV; a seção 13 está afastada do eixo do segundo apoio pelo seu DEPEV.
- O intervalo entre as seções 1 e 13 é dividido em 12 partes iguais, incluindo os extremos.
- A regra não identifica automaticamente qual `length` representa esse intervalo; não equipara o intervalo à distância entre eixos e não modifica a regra anterior de comprimentos.
- A uniformidade agora é conhecimento confirmado pelo engenheiro. A referência física, o comprimento utilizado e os conflitos documentais ainda precisam ser resolvidos antes da transformação no pipeline.

Foi substituída a antiga proibição de supor uniformidade sem evidência pela nova regra confirmada, mantendo a exigência de `positions=null`. A regra anterior continua exatamente:

```text
L_eixos = L_TQS + DEPEV_esq + DEPEV_dir
L_livre = L_eixos - b_esq/2 - b_dir/2
```

Nenhuma regra normativa foi utilizada nesta investigação.

## 2. Fontes, rastreabilidade e estado dos modelos

Pasta de origem: `C:\TQS\24-155-COLLINE-RESIDENCIAL-R60\DIFERENCIADO\VIGAS`. Foram lidos os raw existentes, os consolidados existentes e os LST de origem em CP1252. Todos os 13 hashes do inventário de cada raw coincidem com os arquivos de origem atuais, inclusive os dois arquivos vazios. As linhas citadas são físicas, base 1.

| Relatório | Bloco V501 | Bloco V503 |
|---|---|---|
| VGESFS.LST | 1360–1380 | 1649–1669 |
| RELDTVGS.LST | 3768–3833 | 4536–4601 |
| RELDTFPS.LST | 12751–12943 | 15261–15461 |
| RELDTFNG.LST | 9616–9776 | 11676–11836 |
| RELDTVeT.LST | 10137–10328 | 12804–12995 |
| ESTRIB.LST | 687–696 | 850–859 |
| FLEXPS.LST | 558–566 | 676–684 |
| FLEXNG.LST | 635–644 | 761–770 |
| RELGER.LST | 35–63 | 159–187 |

ORDCON e RELPREDI também foram examinados nos trechos preservados; não foi encontrada neles uma tabela de coordenadas das 13 seções. CONVF2 e RESESTERR estão vazios.

Nos dois consolidados, schema 1.1:

- `/beam/spans/0/geometry/length = 7.552 m`.
- V501: `/beam/spans/0/support_ids = [P2A,P1A]`; V503: `[P2B,P1B]`.
- A lista global de apoios está ordenada por nome: índice 0 é o direito e índice 1 o esquerdo. Não usar essa lista para inferir orientação.
- Larguras longitudinais: 1,20 m à esquerda e 1,42 m à direita.
- Ambas as excentricidades consensuais são null; `support_axis_length` e `clear_span_length` também são null.
- Há 14 séries atribuídas ao vão em cada modelo; todas permanecem com `positions=null`. As seções têm índices 1…13. O vão geral 1 corresponde ao vão interno 2 nos relatórios detalhados; as linhas internas 1 e 3 com comprimento zero são registros documentais.

Proveniência de `length`: V501 `s035`, `s153`, `s449`, `s532`; V503 `s035`, `s153`, `s454`, `s537`, todos em `#/normalizacao/campos/comprimento`. Esses IDs são locais a cada consolidado; `sources[id].raw_pointer` leva ao registro documental.

## 3. Inventário dos comprimentos e referências

“Confirmado” abaixo significa significado explicitado pelo relatório ou derivação pelas regras confirmadas, com indicação da fonte utilizada. Não significa consenso resolvido. “Provável” indica associação sustentada, mas não declarada de forma completa. “Desconhecido” indica referência física/unidade não resolvida.

### 3.1 Geometria, apoios e comprimentos de referência

| Grandeza / valor | Unidade | Fonte V501 | Fonte V503 | Significado e estado |
|---|---|---|---|---|
| `Comprim.=7,552` | m | VGESFS:1364; RELDTVGS:3777 | VGESFS:1653; RELDTVGS:4545 | Comprimento tabular do vão; confirmado como campo de origem do `geometry.length`. Ser L13 é hipótese em avaliação |
| `l=755,2` | cm | RELDTFPS:12761; RELDTFNG:9636 | RELDTFPS:15271; RELDTFNG:11696 | Comprimento tabular detalhado; mesma grandeza numérica de 7,552 m; confirmado documentalmente |
| `bp=120,0; exc=38,4`, apoio esquerdo | cm | RELDTFPS:12766; RELDTFNG:9641 | RELDTFPS:15276; RELDTFNG:11701 | Largura longitudinal e excentricidade de P2A/P2B; valores explícitos, conflitantes com outras fontes |
| `bp=142,0; exc=49,4`, apoio direito | cm | RELDTFPS:12767; RELDTFNG:9642 | RELDTFPS:15277; RELDTFNG:11702 | Largura longitudinal e excentricidade de P1A/P1B; valores explícitos, conflitantes com outras fontes |
| `DimensaoI=1,20; Excentr.=0,38` | m | RELDTVGS:3781 | RELDTVGS:4549 | Apoio esquerdo geral; confirmado; 0,38 não foi substituído por 0,384 |
| `DimensaoI=1,42; Excentr.=0,49` | m | RELDTVGS:3782 | RELDTVGS:4550 | Apoio direito geral; confirmado; 0,49 não foi substituído por 0,494 |
| `Largura=1,20/1,42; DEPEV=0,38/0,49` | m para largura; DEPEV no formato da tabela, sem unidade normalizada no raw | VGESFS:1378–1379; RELGER:60–61 | VGESFS:1667–1668; RELGER:184–185 | Reações com geometria dos apoios. Legenda RELGER:31 define DEPEV como distância do eixo do pilar ao eixo efetivo de apoio; não declara ali sinal/origem global |
| `bp=120,0/142,0; exc=0,4/0,0` | cm impressos | RELDTVeT:10165–10166 | RELDTVeT:12832–12833 | Normalização literal 0,004/0 m para DEPEV. Conflito confirmado; interpretação física desses valores desconhecida |
| `l=7,6; b=0,2; h=0,7` | cm impressos | RELDTVeT:10141–10144 | RELDTVeT:12808–12811 | Raw converte `l` para 0,076 m. Unidade/escala suspeita, incompatível com demais fontes; não corrigida |
| `L=7,55` | m | RELGER:38 | RELGER:162 | Comprimento resumido do vão; provável apresentação com menos casas de 7,552; não equivalência adotada |
| `COMPRIMENTO=7,55` | m | FLEXPS:561; FLEXNG:638 | FLEXPS:679; FLEXNG:764 | Comprimento em resumos de flexão; confirmado como campo, provável apresentação com menos casas |
| `Compr.Orig.=7,552; Exc.Esq.=0; Exc.Dir.=0; Compr.Novo=7,552` | m | RELDTVGS:3821–3824 | RELDTVGS:4589–4592 | Correção por excentricidades dos apoios internos; confirmado para essa etapa. Os zeros não substituem DEPEV de extremidade |
| `Comprimento=7,55; Dist.[a]Sup.=7,55; Dist.[a]Inf.=0` | m | RELDTVGS:3809–3813 | RELDTVGS:4577–4581 | Campos da etapa de mesa colaborante; significado de etapa confirmado; não declarados como intervalo das 13 seções |
| `l,vão=7,55` após retirada de excentricidades | cm impressos | RELDTVeT:10189–10190 | RELDTVeT:12856–12857 | Etapa de alteração de comprimentos e cargas; unidade suspeita. Não é evidência para assumir 7,55 cm ou corrigir para m automaticamente |
| `l=755,2; exc.=0/0` na flexão positiva | cm | RELDTFPS:12825 | RELDTFPS:15343 | Parâmetros de etapa local, explicitamente distintos dos exc de geometria dos apoios. Não provam DEPEV global zero |

O consolidado seleciona 7,552 m pela política existente de geometria de referência, mantendo alternativas 7,55 m, 8,43 m e 0,076 m em warnings. Esta investigação não altera essa política.

### 3.2 Eixos, faces e intervalos

| Grandeza / valor | Unidade | Fonte V501 | Fonte V503 | Significado e estado |
|---|---|---|---|---|
| `L_eixos=843,0` | cm | Derivado de RELDTFPS:12761,12766,12767; corroborado por RELDTFNG:9636,9641,9642 | Derivado de RELDTFPS:15271,15276,15277; RELDTFNG:11696,11701,11702 | 755,2+38,4+49,4. Confirmado por regra permanente **para essas fontes**, não valor consensual |
| `L_livre=712,0` | cm | Mesmo conjunto acima | Mesmo conjunto acima | 843−120/2−142/2. Confirmado por regra permanente para essas fontes |
| `L_eixos=842,2; L_livre=711,2` | cm | Derivado de RELDTVGS:3777,3781,3782 | Derivado de RELDTVGS:4545,4549,4550 | 755,2+38+49; menos 131. Variante por fonte, não absorvida por tolerância |
| `L_eixos=755,6; L_livre=624,6` | cm | Conta condicional: 755,2 mais DEPEV literais 0,4/0 do RELDTVeT | Idem, com dados próprios de V503 | **Mistura entre fontes/etapas**, usada só para demonstrar incompatibilidade, não como geometria adotada |
| `COMPRIMENTO=8,43` | m | ESTRIB:690 | ESTRIB:853 | Campo explícito do relatório. Coincidência com L_eixos derivado é forte evidência de referência aos eixos, mas o rótulo isolado não a declara |
| `INIC.-FIM=60–297; 297–534; 534–772` | cm | ESTRIB:691–695 | ESTRIB:854–858 | Faixas de estribos; confirmado. Intervalo conjunto de 712 cm. Referência ao eixo esquerdo é provável, pela concordância com 120/2 e 843−142/2 |
| `Xi–Xf=0–712`, cisalhamento e torção | cm na indicação `[tf,cm]` | RELGER:53–57 | RELGER:177–181 | Intervalos das verificações resumidas; confirmado. Referência à face interna esquerda é provável por comparação com ESTRIB, não explicitada como sistema das seções |
| `Ini=60,0; Fim=772,0` | cm | RELDTVeT:10251–10254 | RELDTVeT:12918–12921 | Limites de distribuição de estribos; confirmado documentalmente |
| `60,0–297,3; 297,3–534,7; 534,7–772,0` | cm | RELDTVeT:10257–10264 | RELDTVeT:12924–12931 | Subdivisão da faixa de estribos. Compatível numericamente com terços de 712 cm; não representa por isso a malha de 13 esforços |
| Livre documental da prancha=711 | cm | `analises/pranchas/V501_V503_detalhamento_prancha.json`, geometria já interpretada; ver `V501_V503_leitura.md` | Mesmo documental agrupado, somente referência gráfica | Valor de detalhamento, não medição independente do TQS. Diferença de 1 cm para 712 permanece |

### 3.3 Outras abscissas e comprimentos locais

| Valor | Unidade | Fonte V501 | Fonte V503 | Significado e estado |
|---|---|---|---|---|
| `Abcis.=440` | Não repetida na célula; provavelmente cm pelo formato | RELGER:43 | RELGER:167 | Abscissa publicada do máximo positivo. Origem, arredondamento/truncamento e vínculo a um índice: desconhecidos |
| `Ptos de Mk[-]=4; Comp.vão.com M[-]=251,7` | cm para comprimento | RELDTFNG:9662,9665 | RELDTFNG:11722,11725 | Extensão utilizada no recálculo da mesa colaborante na região negativa. Significado de etapa confirmado; não é rótulo de L13 |
| Cargas: `Dist.=350,40 / 633,40; Larg.=19 / 14` | m impressos | RELDTVeT:10159–10160 | RELDTVeT:12826–12827 | Distâncias e larguras de cargas concentradas, com unidade suspeita. Não convertidas em posições de esforço |
| Cargas após retirada: `Dist.=312 / 595` | cm | RELDTVeT:10193–10194 | RELDTVeT:12860–12861 | Distâncias da etapa alterada. Os números diferem dos anteriores em 38,4 **somente se** os números anteriores forem lidos em cm; isso é indício, não correção autorizada |
| Faixas de pesquisa `306,6–394,1` e `592,1–674,6`; comprimentos `87,5 / 82,5` | cm | RELDTVeT:10235–10247 | RELDTVeT:12902–12914 | Regiões de pesquisa/distribuição de armadura junto de cargas; não intervalo das 13 seções |
| Barras positivas antes da compatibilização: `x,i=80; cmp=647` e `x,i=−27; cmp=810` | cm | RELDTFPS:12852–12853 | V503 tem **78/648** e −27/810 em 15370–15371 | Coordenadas/comprimentos de posições de barras; não foram equiparados a origem/extremo das séries |
| Barras positivas após compatibilização: `x,i=−20; cmp=795` | cm | RELDTFPS:12932–12938 | RELDTFPS:15450–15456 | Barra agrupada final, não comprimento do vão nem L13 |
| Barras superiores: `X,i=−78,6; cmp=400,8`; à direita `−344,4/282,7` e `−463,4/400,8` | cm | RELDTFNG:9748,9752,9753 | RELDTFNG:11808,11812,11813 | Coordenadas locais de detalhamento, incluindo outra referência no apoio direito; não usadas para reconstruir a malha |
| `FC SP Eixo=36; FC LT Eixo=9,5`; `EspessIn/Su=22 / 24` | cm, ou equivalentes em m no geral | RELDTFNG:9636; RELDTVGS:3781–3782 | RELDTFNG:11696; RELDTVGS:4549–4550 | Dimensões transversais/seccionais. Não são comprimentos longitudinais candidatos a L13 |

Comprimentos de ancoragem, dobras, reduções de cortante e dimensões transversais permanecem dados de suas etapas. Não se procurou fechar a malha somando esses campos ao vão.

## 4. Esquema geométrico da hipótese principal

A nova regra fornece afastamentos. Para desenhar as seções entre os apoios, a hipótese principal coloca a seção 1 **à direita** do eixo esquerdo e a seção 13 **à esquerda** do eixo direito. Esses sentidos são explicitados aqui; a redação recebida não forneceu sinais algébricos nem definiu que `X=0` coincide com o eixo físico ou com a seção 1.

Com os dados de RELDTFPS/RELDTFNG e uma coordenada auxiliar **q** no eixo físico esquerdo (não o `X` do TQS):

```text
q (cm):  0       38,4    60                         772    793,6     843
         |        |      |                           |       |       |
         E        S1     FE                          FD      S13      D
         |--38,4-->|                                      <--49,4----|
                  |------------- L13 = 755,2 ---------------|
         |---------------- L_eixos = 843 ----------------------------|
                         |-------- L_livre = 712 -------|

E/D = eixos físicos dos apoios esquerdo/direito
FE = face interna esquerda: q=120/2=60
FD = face interna direita: q=843-142/2=772
S1: q=DEPEV_esq=38,4
S13: q=L_eixos-DEPEV_dir=793,6

Malha entre S1 e S13, 12 intervalos iguais (esquema sem escala):
S1--S2--S3--S4--S5--S6--S7--S8--S9--S10--S11--S12--S13
```

S1 está 21,6 cm antes de FE; S13 está 21,6 cm depois de FD. Portanto o intervalo dos esforços, nesta hipótese, inclui partes internas dos apoios e não coincide com o intervalo livre:

```text
L13 = 843 - 38,4 - 49,4 = 755,2 cm
L13 = L_livre + (120/2-38,4) + (142/2-49,4)
    = 712 + 21,6 + 21,6 = 755,2 cm
```

Esse fechamento é **por fonte**. Não substitui o consenso null, não força a prancha de 711 cm a fechar e não decide qual fonte de DEPEV deve ser utilizada.

Se ambos os afastamentos fossem para fora dos apoios, o intervalo seria 930,8 cm; sentidos mistos produziriam 854,0 ou 832,0 cm. São possibilidades algébricas quando se omitem sinais, sem evidência positiva nos blocos examinados. Não foram promovidas a hipóteses documentais de trabalho nem implementadas. A pergunta sobre os sentidos dos afastamentos permanece explícita no item 9.

## 5. Hipóteses de L13 e tabelas de demonstração

Para todas as tabelas, a origem **x=0 é a seção 1 apenas nesta demonstração**. Isso não estabelece a origem `X=0` do TQS.

```text
L13 = distância entre seção 1 e seção 13
Δx = L13/12
x_i = (i-1)*Δx, i=1...13
```

### 5.1 Candidatos físicos

| Hipótese | Campo/combinação | L13 (cm) | Δx (cm) | Avaliação |
|---|---|---:|---:|---|
| H1 | 843−38,4−49,4, coincidente com `length=7,552 m` | 755,2 | 62,933333… | Fecha o esquema com afastamentos para dentro; candidata principal por fonte |
| H2 | `COMPRIMENTO=8,43 m` de ESTRIB tomado diretamente como L13 | 843,0 | 70,250000 | Não fecha com DEPEV não nulos e eixos separados por 843; rejeitada como intervalo discretizado nesta geometria |
| H3 | 772−60 de ESTRIB ou 712−0 de RELGER tomado diretamente como L13 | 712,0 | 59,333333… | Coloca extremos nas faces, não nos eixos efetivos definidos pelos DEPEV; rejeitada como intervalo das seções nesta geometria |

Tabela V501, valores em cm arredondados a seis casas apenas para apresentação:

| Seção i | H1: 755,2/12 | H2: 843/12 | H3: 712/12 |
|---:|---:|---:|---:|
| 1 | 0,000000 | 0,000000 | 0,000000 |
| 2 | 62,933333 | 70,250000 | 59,333333 |
| 3 | 125,866667 | 140,500000 | 118,666667 |
| 4 | 188,800000 | 210,750000 | 178,000000 |
| 5 | 251,733333 | 281,000000 | 237,333333 |
| 6 | 314,666667 | 351,250000 | 296,666667 |
| 7 | 377,600000 | 421,500000 | 356,000000 |
| 8 | 440,533333 | 491,750000 | 415,333333 |
| 9 | 503,466667 | 562,000000 | 474,666667 |
| 10 | 566,400000 | 632,250000 | 534,000000 |
| 11 | 629,333333 | 702,500000 | 593,333333 |
| 12 | 692,266667 | 772,750000 | 652,666667 |
| 13 | 755,200000 | 843,000000 | 712,000000 |

**Teste de fechamento:** mantendo S1 em q=38,4, H2 colocaria S13 em q=881,4, 38,4 cm além do eixo direito, em vez de 49,4 cm antes dele. H3 colocaria S13 em q=750,4, a 92,6 cm do eixo direito. Somente H1 termina em q=793,6 no esquema principal.

### 5.2 Precisão publicada e variantes de DEPEV

H4 usa literalmente os 7,55 m publicados nos resumos. H5 fixa os 843 cm do ESTRIB e subtrai os DEPEV gerais 38/49 cm. **H5 mistura fontes** e é apresentada como diagnóstico de conflito, não como opção a selecionar. As diferenças entre 755,0, 755,2 e 756,0 foram preservadas; a composição de H5 não autoriza selecionar esse resultado.

| Seção i | H4: L13=755,0 cm; Δx=62,916666… | H5: L13=843−38−49=756,0 cm; Δx=63,000000 |
|---:|---:|---:|
| 1 | 0,000000 | 0,000000 |
| 2 | 62,916667 | 63,000000 |
| 3 | 125,833333 | 126,000000 |
| 4 | 188,750000 | 189,000000 |
| 5 | 251,666667 | 252,000000 |
| 6 | 314,583333 | 315,000000 |
| 7 | 377,500000 | 378,000000 |
| 8 | 440,416667 | 441,000000 |
| 9 | 503,333333 | 504,000000 |
| 10 | 566,250000 | 567,000000 |
| 11 | 629,166667 | 630,000000 |
| 12 | 692,083333 | 693,000000 |
| 13 | 755,000000 | 756,000000 |

H4, com DEPEV 38,4/49,4, implica eixos separados por 842,8 cm, 0,2 cm abaixo dos 843,0 da geometria detalhada. Não é um segundo comprimento físico demonstrado.

Usar coerentemente **a fonte geral**, em vez de fixar ESTRIB, produz `L_eixos=842,2` e `L13=842,2−38−49=755,2 cm`: a mesma tabela de H1, mas faces e deslocamentos ligeiramente distintos (`L_livre=711,2 cm`, afastamentos face–seção de 22 cm). Essa igualdade de L13 é uma consequência algébrica da regra anterior, não resolução dos DEPEV.

Fixar o intervalo livre publicado 712 e somar os afastamentos face–seção derivados dos DEPEV gerais produz novamente 756,0 cm. Isso mistura fontes como H5. **754,4 cm não resulta dessas combinações**: seria erro aritmético usar 843−38−49=754,4.

Os 711 cm da prancha não são um candidato independente a L13: são comprimento livre documental. Fixá-los e somar 21,6+21,6 produz 754,2 cm, mas conflita com a geometria TQS detalhada; não foi usado para definir a malha do TQS.

O `l=7,6 cm` literal de RELDTVeT também não é candidato geométrico plausível: conflita com dimensões dos apoios e demais comprimentos. Não se criou tabela de esforço baseada nessa unidade suspeita.

## 6. Confronto com abscissas, intervalos e outras evidências

### 6.1 Máximo positivo e `Abcis.=440`

Na V501, `VGESFS:1373` e `RELDTVGS:3800` têm o maior valor da série positiva na **seção 8**: 6,272 tf·m. RELGER:43 imprime máximo 6,3 tf·m e `Abcis.=440`.

Na H1, `x8=7×755,2/12=440,533333 cm`. Essa proximidade favorece uma origem na seção 1, mas **não é igualdade exata** e não prova truncamento. Arredondamento ao inteiro mais próximo produziria 441, não 440. H4 também produz 440,416667, que poderia ser apresentado como 440. Portanto a abscissa inteira, isoladamente, não distingue a precisão 7,55/7,552 nem explica o método de apresentação.

Se H1 for aplicada e o relatório usar origem no eixo físico esquerdo, `q8=38,4+440,533333=478,933333 cm`. Se usar a face interna esquerda, `u8=q8−60=418,933333 cm`. Nenhum desses valores coincide com 440. Isso favorece, sem comprovar, a origem na seção 1 para essa célula.

Com a mesma origem demonstrativa na seção 1, H2 dá x8=491,75 e H3 dá x8=415,333333. São menos compatíveis com 440. Entretanto não é permitido rejeitar um candidato apenas por essa diferença sem verificar que o máximo do RELGER é o mesmo ponto amostrado e usa a mesma origem. A rejeição geométrica de H2/H3 decorre do teste com DEPEV, não de forçar o máximo a um índice.

### 6.2 Regiões negativas de 251,7 cm

H1 dá quatro intervalos de 62,933333 cm = 251,733333 cm, compatível com a apresentação 251,7 em RELDTFNG:9662/9665. As séries negativas têm quatro valores negativos em cada extremidade, separados da região positiva. O rótulo “Ptos=4” não explicita se o algoritmo mede quatro intervalos, três distâncias entre pontos ou uma região prolongada até o próximo ponto. Assim, a coincidência é corroborativa, não prova da coordenada de corte ou de sua definição algorítmica. Nenhum zero de esforço foi interpolado.

H2 produziria quatro intervalos de 281 cm; H3, 237,333333 cm. H4 produz 251,666667 cm, também apresentável como 251,7. Esse campo não distingue sozinho 755,0 de 755,2.

### 6.3 ESTRIB e RELGER representam outro intervalo

Na H1, eixo esquerdo q=0, faces q=60/772 e eixos separados por 843 fecham com ESTRIB. RELGER 0–712 corresponde ao mesmo intervalo livre se sua origem for a face esquerda: `u=q−60`. Essa tradução é **provável por geometria**, não uma regra geral de coordenadas publicada nesses rótulos.

Para a malha demonstrativa de H1, `x=q−38,4`. Portanto as faces ficam em **x=21,6 e x=733,6**, enquanto as seções extremas ficam em **x=0 e x=755,2**. Não se deve recortar a malha para 0–712 nem usar o intervalo de estribos para preencher as seções.

As fronteiras 297,3/534,7 do relatório detalhado e 297/534 do ESTRIB são faixas de distribuição distintas das seções de esforços. Nem a subdivisão em terços, nem a coincidência de alguns números autoriza equipará-las à malha de 12 partes. Os valores inteiros do ESTRIB também diferem de arredondamento usual de 534,7, que daria 535; sua apresentação não foi explicada por uma política inventada.

### 6.4 Termos “eixo do pilar” nos extremos

RELDTFPS:12868/12902 atribui aos “eixos do pilar” os momentos −1299,0/−2039,3 tf·cm e máximos −224,7/−103,8 tf·cm, que correspondem aos valores extremos das séries. O relatório distingue a “face do pilar” nas linhas seguintes. Essa terminologia **não distingue claramente eixo físico e eixo efetivo**, apesar de DEPEV não nulo. A nova regra do engenheiro esclarece o afastamento da seção em relação ao eixo, mas o texto do relatório, isoladamente, não resolve o rótulo. Não se forçou S1/S13 a serem os eixos físicos por causa dessa expressão.

## 7. Conferência independente com V503

Os dados geométricos foram conferidos nos registros da V503, não copiados por igualdade de detalhamento:

- VGESFS:1653 e RELDTVGS:4545: L=7,552 m.
- RELDTFPS:15271,15276,15277 e RELDTFNG:11696,11701,11702: l=755,2 cm, DEPEV=38,4/49,4 cm e bp=120/142 cm.
- ESTRIB:853,856–858: 8,43 m, intervalo conjunto 60–772 cm.
- RELGER:178/181: 0–712 cm; RELDTVGS:4549–4550: variantes 0,38/0,49 m; RELDTVeT:12832–12833: variantes literais 0,4/0 cm.
- `L_eixos=843`, `L_livre=712` e H1 `L13=755,2`, `Δx=62,933333… cm` repetem o fechamento por fonte. A tabela geométrica H1 é igual pela conferência dos dados, não pelo agrupamento da prancha.
- VGESFS:1662 e RELDTVGS:4568: máximo positivo na seção 8, **6,354 tf·m**, diferente dos 6,272 da V501. RELGER:167 publica 6,4 tf·m e `Abcis.=440`; a mesma ressalva de origem/apresentação se aplica.
- RELDTFNG:11722/11725 registra novamente 251,7 cm; apoios são P2B/P1B. RELDTFPS:15386/15420 usa o termo “eixo do pilar” para valores extremos próprios, com a mesma ambiguidade semântica.

**A mesma interpretação geométrica é compatível por fonte com as duas vigas**, com os mesmos limites de confirmação. As solicitações, reações e alguns comprimentos de barras são diferentes; nenhuma igualdade de esforços foi presumida.

## 8. Inconsistências e limite da conclusão

1. DEPEV detalhado 38,4/49,4 cm, geral 38/49 cm e literal RELDTVeT 0,4/0 cm não formam consenso. Permanecem preservados e null nos campos consensuais.
2. `length=7,552 m`, resumos 7,55 m, ESTRIB 8,43 m e intervalos livres 712 cm designam referências/etapas distintas. Não se deve selecionar um deles só por precisão ou nome.
3. Unidades de RELDTVeT são incoerentes com a ordem de grandeza geométrica. O parser mantém a conversão literal e ressalva; isso é limitação documental, não um erro inequívoco de parser identificado nesta investigação.
4. Há diferença de 1 cm entre a leitura anterior da prancha e o livre detalhado do TQS. A prancha não foi alterada.
5. `Abcis.=440` não declara localmente unidade, origem ou algoritmo de apresentação, e 440,533 não é 440 por arredondamento usual ao inteiro.
6. As células nomeadas “eixo do pilar” não distinguem o eixo físico do efetivo.
7. A expressão “afastada pelo DEPEV” confirma o módulo, mas não fornece explicitamente os sinais algébricos ou a coordenada do eixo esquerdo no sistema `X=0`.

**Conclusão geométrica condicional demonstrada:** se S1/S13 são os eixos efetivos deslocados para dentro do vão, então:

```text
L13 = L_eixos - DEPEV_esq - DEPEV_dir
    = (L_TQS + DEPEV_esq + DEPEV_dir) - DEPEV_esq - DEPEV_dir
    = L_TQS
```

Para o conjunto detalhado de V501 e V503, isso dá **L13=755,2 cm**, que deve ser dividido em 12 **nessa hipótese por fonte**. É a interpretação mais sustentada pela geometria, pela abscissa do máximo e pelo campo 251,7. **Não se declara ainda uma transformação numérica global validada para `internal_forces[].positions`**: faltam confirmar os sentidos e o vínculo entre a origem demonstrativa e `X=0`, além da política de fontes. Nenhuma fonte conflitante foi escolhida silenciosamente.

## 9. Perguntas objetivas ao engenheiro

1. Para V501/V503, confirma que a seção 1 está **para dentro do vão**, à direita do eixo de P2A/P2B, e a seção 13 também **para dentro**, à esquerda do eixo de P1A/P1B, coincidindo com os respectivos eixos efetivos de apoio?
2. Onde fica exatamente `X=0` do TQS: na seção 1/eixo efetivo, no eixo físico do primeiro apoio ou em outro ponto? `Abcis.=440` do RELGER utiliza essa mesma origem? O valor é truncado, arredondado ou calculado para um máximo em posição diferente da seção 8?
3. Os campos `l=755,2 cm` de RELDTFPS/RELDTFNG e `Comprim.=7,552 m` de VGESFS/RELDTVGS representam o intervalo seção 1–13? Esta confirmação amarra o campo ao conceito, sem definir preferência entre fontes de DEPEV.

As respostas não foram pressupostas. Resolver a política de DEPEV e generalizar para outros vãos/relatórios são etapas posteriores.

## 10. Preservação dos arquivos e entrega

Não foram modificados parsers, consolidadores, schemas, raw, modelos TQS ou modelos de detalhamento. Não foram criados `beam_mapping`, coordenadas no pipeline nem verificações de resistência. As tabelas numéricas deste Markdown são apenas demonstrações geométricas, calculadas com Python sem alterar esforços.

Hashes dos quatro arquivos TQS examinados:

| Arquivo | SHA-256 |
|---|---|
| V501_tqs_raw.json | `654b79ee817853e6cac8d4e49217b05a4474108af8e61f04a7f23f86527fb344` |
| V501_tqs.json | `0cf0847d245630e5ac2ab6036e3264d2983e735a1a4940072ac93b50bb9c6067` |
| V503_tqs_raw.json | `652be473673addd72d730ac0e68913b64c010d0a7562d1a4484c9ac7c505b12b` |
| V503_tqs.json | `11a781d63747028e8af4256046e001b6d847151cea340412916c34340d119304` |

Os hashes também foram comparados antes/depois para os modelos de detalhamento V501/V503 e os arquivos Python de ferramentas/testes. Não foi necessário executar verificações estruturais ou regenerar modelos para esta entrega documental.

Arquivos desta etapa:

- **Atualizado:** `.agents/skills/reinforcement-review/references/tqs-beam-data.md`.
- **Criado:** `.codex/analises/V501_V503_tqs_section_positions.md` (este relatório).
