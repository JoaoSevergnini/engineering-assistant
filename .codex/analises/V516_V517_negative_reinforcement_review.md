# Revisão das armaduras negativas — V516=V517

> Atualização vigente: seção 16 — relações entre apoios consecutivos. Os diagnósticos históricos de N3/RIGHT, N4/RIGHT e N7/LEFT são SUPERSEDED pelos controles ali documentados; as demais falhas permanecem.

Data: 06/10/2026. Ensaio real com quatro vãos, três posições intermediárias e duas posições de extremidade. Detalhamento compartilhado; esforços tratados individualmente.

## Conclusão

**Há falhas comprovadas nos pontos verificados de ambas as vigas:** capacidade de flexão insuficiente à esquerda do P1 e comprimento insuficiente da N8 à esquerda para al+lb. As dobras das extremidades também não atingem a referência geométrica do procedimento confirmado. A revisão negativa completa permanece inconclusiva por controles ainda não representados/resolvidos; isso não elimina as falhas já identificadas. Não foi escolhida uma correção.

## 1. Fontes e interpretação

PDF RMP-EST-EX-1348-VIG-R00 - Copia.PDF, página 1, detalhe V516=V517, em S:/PROJETOS EM EXECUÇÃO/24-155-INTEGRA-MIGUEL PEREIRA-RJ/APOIO/JOÃO/05 - TIPO DIFERENCIADO - RESIDENCIAL/VIGAS. Relatórios TQS individuais da pasta C:/TQS/24-155-COLLINE-RESIDENCIAL-R60/DIFERENCIADO/VIGAS. Fontes e hashes estão nos JSON. Notas do documento foram tratadas como dados de projeto, não instruções ao agente.

Usaram-se AGENTS.md, reinforcement-review, referências de desenho/TQS/negativa, contratos das ferramentas e APIs públicas do Concretopy. Seção 19×52 cm, C40, CA50 fyk=500 MPa, cobrimento TQS 2,5 cm; gammas f/c/s=1,4/1,4/1,15 (gamma_s é default público). Seções com mesa superior foram verificadas pela alma retangular para momento negativo: a mesa superior está no lado tracionado, não recebeu crédito de compressão.

A armadura desenhada é a fonte da configuração resistente. RELDTFNG contém arranjos/bitolas diferentes do PDF — por exemplo, no P1 há posições Ø25 no TQS, enquanto a prancha tem N7/N8/N9 Ø20. Não se substituiu a prancha pelo detalhamento calculado. Compatibilidade geométrica não comprova equivalência completa de revisão entre fontes.

## 2. Geometria e limitações da infraestrutura

O consolidado possui quatro vãos e apenas quatro nomes de apoios, porque deduplica P2. As linhas sequenciais de RELDTFPS e a elevação mostram cinco posições: P5, P2, P2, P1 e P6. As duas posições P2 não foram fundidas nem tratadas como nomes de pilares diferentes; receberam IDs de ocorrência.

O posicionador geral exige support_ids, que vieram null, e o mapper geral aceita somente um vão. O adaptador específico do ensaio conserva os consolidados originais e cria vistas locais de cada vão, vinculadas às cinco linhas ordenadas documentais. Reutiliza fill_positions para posições locais e soma offsets de eixos explicitamente derivados de comprimentos+DEPEV. Não é uma generalização silenciosa do mapper nem uma migração dos modelos originais.

| Posição | V516 / V517 | Eixo global (m) | Largura longitudinal (cm) | DEPEV (cm) | Tipo |
|---|---|---:|---:|---:|---|
| 1 | P5A / P5B | 0,000 | 24,000 | 0,000 | END |
| 2 | P2A / P2B | 2,080 | 22,000 | 0,000 | INTERMEDIATE |
| 3 | P2A / P2B | 6,620 | 22,000 | 0,000 | INTERMEDIATE |
| 4 | P1A / P1B | 11,000 | 142,000 | 55,400 | INTERMEDIATE |
| 5 | P6A / P6B | 13,680 | 24,000 | 0,000 | END |

| Vão | Intervalo amostrado global (m) | Comprimento livre (cm) |
|---|---|---:|
| 1 | 0,000–2,080 | 185,000 |
| 2 | 2,080–6,620 | 432,000 |
| 3 | 6,620–10,446 | 356,000 |
| 4 | 11,554–13,680 | 185,000 |

Os livres 185/432/356/185 cm conferem com o PDF. DEPEV do P1=55,4 cm fecha eixos em 11,000 m e 13,680 m. Não há dados entre S13 do vão 3 em 10,446 m e S1 do vão 4 em 11,554 m: não se interpolou esse gap nem se atribuiu ao eixo P1 o momento de outro ponto.

## 3. Armaduras negativas documentais

| Marca | Quantidade/bitola | Camada física de referência | Intervalo global (m) | Dobra escrita |
|---|---|---|---|---|
| N4 | 3Ø16 | primeira | -0,095–5,015 | 40,000 cm |
| N3 | 1Ø16 | segunda | 0,480–3,670 | sem dobra |
| N7 | 2Ø20 | primeira | 3,635–13,775 | 45,000 cm |
| N8 | 1Ø20 | primeira | 5,830–12,840 | sem dobra |
| N9 | 1Ø20 | segunda | 8,940–12,840 | sem dobra |

Coordenadas N4/N7: projeções 511/1014 cm e extremidade dentro da face externa do pilar com cobrimento 2,5 cm, **hipótese autorizada pelo engenheiro nesta sessão**. N3: início 36 cm depois da face interna esquerda e comprimento 319 cm. N8/N9: término 72 cm antes da face interna P6; comprimentos 701/390 cm. As extremidades documentais foram preservadas, sem aproximação para seção TQS. N10 explicitamente PELE e barras positivas não foram computadas como negativas.

Estribos regionais: Ø8 nos vãos extremos; Ø5 nos intermediários; Ø8 na região especial de 52 cm do vão 3 (8,64–9,16 m), conservando a distinção da região especial. Na parte amostrada dentro de pilares, a extensão desses diâmetros é hipótese de auditoria; a geometria estrita do nó não foi demonstrada. Posições das camadas usam a convenção do Concretopy, não cotas verticais extraídas do PDF.

## 4. Sobreposição N4/N7 — esclarecimento do engenheiro

O engenheiro confirmou que, nessa sobreposição, as barras já são caudas de ancoragem, podendo ficar encostadas ou uma imediatamente abaixo da outra. Essa disposição foi aceita como julgamento de detalhamento; não foi exigida uma camada resistente convencional com cinco barras e não foi dada capacidade igual à soma N4+N7.

O M MN. ainda apresenta momentos negativos pequenos no intervalo. Como conferência de referência, foram calculadas separadamente N4 e N7 em suas posições isoladas originais; ambas superam a solicitação do trecho, sem somar áreas. Isso é coerente com não depender da ação conjunta. A resposta não define centros exatos no trecho misto; portanto o centroide anterior requerido em alguns eventos al continua pendente. A pendência numérica não significa rejeitar a disposição de caudas aceita pelo engenheiro.

## 5. Resistência regional à flexão negativa

Foram consultados extremos de composição, vértices e limites de regiões de estribos, com Msk assinado e vista −M; nunca abs(M) para converter momento positivo em negativo. d é medido desde a face inferior comprimida. As camadas remanescentes não foram reposicionadas ao remover barras.

| Viga / vão | Intervalo (m) | Composição | Mk eq. (kNm) | Maior magnitude negativa (kNm) | Resultado |
|---|---|---|---:|---:|---|
| V516 / 1 | 0,000–0,480 | N4 | 84,405 | 31,166 | atende |
| V516 / 1 | 0,480–2,080 | N4+N3 | 107,926 | 85,504 | atende |
| V516 / 2 | 2,080–3,635 | N4+N3 | 108,676 | 75,835 | atende |
| V516 / 2 | 3,635–3,670 | N4+N3+N7 | — | — | caudas aceitas; sem crédito à soma |
| V516 / 2 | 3,670–5,015 | N4+N7 | — | — | caudas aceitas; sem crédito à soma |
| V516 / 2 | 5,015–5,830 | N7 | 87,886 | 50,366 | atende |
| V516 / 2 | 5,830–6,620 | N7+N8 | 127,497 | 90,466 | atende |
| V516 / 3 | 6,620–8,640 | N7+N8 | 127,497 | 107,530 | atende |
| V516 / 3 | 8,640–8,940 | N7+N8 | 126,619 | 24,290 | atende |
| V516 / 3 | 8,940–9,160 | N7+N8+N9 | 159,147 | 42,053 | atende |
| V516 / 3 | 9,160–10,446 | N7+N8+N9 | 160,317 | 168,988 | não atende |
| V516 / 4 | 11,554–12,840 | N7+N8+N9 | 159,147 | 60,419 | atende |
| V516 / 4 | 12,840–13,680 | N7 | 87,301 | 17,064 | atende |
| V517 / 1 | 0,000–0,480 | N4 | 84,405 | 32,833 | atende |
| V517 / 1 | 0,480–2,080 | N4+N3 | 107,926 | 87,858 | atende |
| V517 / 2 | 2,080–3,635 | N4+N3 | 108,676 | 76,374 | atende |
| V517 / 2 | 3,635–3,670 | N4+N3+N7 | — | — | caudas aceitas; sem crédito à soma |
| V517 / 2 | 3,670–5,015 | N4+N7 | — | — | caudas aceitas; sem crédito à soma |
| V517 / 2 | 5,015–5,830 | N7 | 87,886 | 49,808 | atende |
| V517 / 2 | 5,830–6,620 | N7+N8 | 127,497 | 89,025 | atende |
| V517 / 3 | 6,620–8,640 | N7+N8 | 127,497 | 105,784 | atende |
| V517 / 3 | 8,640–8,940 | N7+N8 | 126,619 | 21,472 | atende |
| V517 / 3 | 8,940–9,160 | N7+N8+N9 | 159,147 | 38,565 | atende |
| V517 / 3 | 9,160–10,446 | N7+N8+N9 | 160,317 | 162,379 | não atende |
| V517 / 4 | 11,554–12,840 | N7+N8+N9 | 159,147 | 64,587 | atende |
| V517 / 4 | 12,840–13,680 | N7 | 87,301 | 20,457 | atende |

**Região governante:** vão 3, à esquerda do P1, composição 3Ø20 na primeira camada + 1Ø20 na segunda. d equivalente=47,0 cm; MRd=224,444382 kNm; Mk eq.=160,317415 kNm. S13 em x=10,446 m demanda 168,988193 kNm na V516 e 162,378511 kNm na V517. Utilizações aproximadas 1,0541 e 1,0129. Ambas excedem a capacidade.

Sensibilidade geométrica: se fosse adotado Ø8 em vez de Ø5 como estribo nessa região, Concretopy retorna d=46,7 cm e Mk eq.=159,146636 kNm; a insuficiência permanece. Essa alternativa não foi usada para alterar a geometria documental.

## 6. Vk para al e aderência

| Vão | máximo abs(Vk), V516 (kN) | máximo abs(Vk), V517 (kN) |
|---|---:|---:|
| 1 | 66,970 | 68,578 |
| 2 | 54,751 | 53,593 |
| 3 | 104,804 | 103,401 |
| 4 | 47,896 | 50,034 |

Seleção discreta sobre ambas as envoltórias de cada vão, conservando seção/série/sinal e provenance. Não usar Vk local do corte nem refletir a outra viga. al é o valor final limitado da API, usando o centroide da composição imediatamente anterior ao evento. Aderência das negativas: POOR pela decisão do engenheiro; lb básico próprio Ø16=62,939073 cm e Ø20=78,673842 cm. Não houve redução por área ou gancho.

## 7. Controles independentes de escalonamento

| Viga | Marca / lado | d para al (cm) | Controle | Disponível (cm) | Exigido (cm) | Atende |
|---|---|---:|---|---:|---:|---|
| V516 | N3 / LEFT | 47,000 | al_plus_lb | 160,000 | 109,939 | sim |
| V516 | N3 / LEFT | 47,000 | al_plus_10phi | 158,352 | 63,000 | sim |
| V516 | N8 / LEFT | 48,000 | al_plus_lb | 79,000 | 126,674 | não |
| V516 | N8 / LEFT | 48,000 | al_plus_10phi | 74,147 | 68,000 | sim |
| V516 | N9 / LEFT | 46,700 | al_plus_lb | 150,600 | 125,374 | sim |
| V516 | N9 / LEFT | 46,700 | al_plus_10phi | 109,580 | 66,700 | sim |
| V517 | N3 / LEFT | 47,000 | al_plus_lb | 160,000 | 109,939 | sim |
| V517 | N3 / LEFT | 47,000 | al_plus_10phi | 154,948 | 63,000 | sim |
| V517 | N8 / LEFT | 48,000 | al_plus_lb | 79,000 | 126,674 | não |
| V517 | N8 / LEFT | 48,000 | al_plus_10phi | 76,838 | 68,000 | sim |
| V517 | N9 / LEFT | 46,700 | al_plus_lb | 150,600 | 125,374 | sim |
| V517 | N9 / LEFT | 46,700 | al_plus_10phi | 115,735 | 66,700 | sim |

N3 esquerda: ramo de decadência do P2 na primeira posição intermediária, pico endpoint x=2,080 m. O ramo foi limitado ao primeiro mínimo em magnitude, evitando incluir a subida relativa ao apoio oposto. Crossing remanescente x=2,063525 m (V516) / 2,029483 m (V517). Os dois controles atendem.

N8 esquerda: pico x=6,620 m e extremidade real x=5,830 m. al=48,0 cm e lb=78,673842 cm: exigido 126,673842 cm; disponível 79 cm; déficit **47,673842 cm** no controle al+lb. O controle al+10φ atende: crossings 6,571467 m / 6,598383 m e exigido 68 cm. A posição final exigida por al+lb nesse cenário seria x=5,353262 m, mantida separadamente da extremidade original; isso não seleciona uma correção.

N9 esquerda: pico amostrado x=10,446 m; crossing remanescente 10,035795 m / 10,097355 m. Usou-se Ø8 na posição do evento, d anterior=46,7 cm. Ambos os controles atendem. **O escalonamento da N9 atender não aprova a composição N7+N8+N9 à flexão**, que falha junto ao P1. A extensão do contexto Ø8 ao percurso do controle é conservadora e explicitada; a resistência regional usa os estribos de cada trecho.

Eventos N3 direita, N4 direita e N7 esquerda permanecem numericamente pendentes por centroide/posições não definidos no trecho de caudas mistas. lb básico foi calculado independentemente. N8 e N9 terminam juntas em x=12,840 m e possuem eventos independentes. À direita de P1, a classificação agora é ancoragem após apoio intermediário, pois N7 atende todo o lóbulo negativo adjacente; ver seção 12. Não se simulam cortes sucessivos.

## 8. Apoios intermediários

| Posição | Marcas que atravessam documentalmente | Continuidade física | Controles independentes completos |
|---|---|---|---|
| P2, eixo 2,080 m | N4 e N3 | confirmada pela peça contínua desenhada | pendentes |
| P2, eixo 6,620 m | N7 e N8 | confirmada | pendentes; falha N8 esquerda já comprovada |
| P1, eixo 11,000 m | N7, N8 e N9 | confirmada | pendentes; flexão do lado esquerdo falha |

Usaram-se RIGHT do vão à esquerda e LEFT do vão à direita, com IDs de ocorrência e faces físicas comuns. Intervalos, bitolas, camada de referência e peça/traçado documental foram preservados. O resultado de continuidade resistente ficou null: atravessar o apoio não substitui verificar as duas extensões, a ancoragem e os eventos aplicáveis. Não foi adicionada extensão arbitrária ou inventada emenda.

## 9. Apoios de extremidade e dobras

P5 e P6 são apoios END em pilares, com 24 cm. Espaço reto geométrico do cenário básico: 24−2,5=21,5 cm, inferior ao lb básico das barras. Concretopy fornece lb; a regra geométrica do engenheiro fornece a proposta de perna de dobra min(h−c−φ_estribo,2lb).

| Apoio / marca | φ estribo (mm) | Dobra escrita (cm) | Referência geométrica (cm) | Diferença (cm) | Geometria atende | Resistência da dobra |
|---|---:|---:|---:|---:|---|---|
| P5 / N4 | 8 | 40,0 | 48,7 | −8,7 | não | não concluída |
| P6 / N7 | 8 | 45,0 | 48,7 | −3,7 | não | não concluída |

Não foi dado crédito automático α=0,7. C de fabricação, raios/pinos, interferências e resistência completa da dobra permanecem não verificados. Os valores 40/45 cm são os trechos escritos na prancha; comparação não significa aprovação normativa do nó. O ensaio é de nó extremo em pilar; o nome do pilar não comprova vínculo rotacional rígido. Não é caso de balanço único, logo as regras 1,5lb e sobra da extremidade livre não se aplicam.

## 10. Provenance, limitações e arquivos

Cada resultado tem diagramas originais com sinal, séries cortantes e seções governantes, fontes LST/linhas, hipóteses, chamadas Concretopy, posições documentais e referências dos controles. O adaptador registra a origem local e o offset global. Não houve extrapolação de esforços para preencher pilares/gaps. Não foram modificados Concretopy, motores estruturais existentes ou goldens anteriores.

JSONs: V516_negative_reinforcement_review.json e V517_negative_reinforcement_review.json; TQS raw/consolidado independente e quatro vistas posicionadas por viga. Reprodutor: validar_v516_v517_negativo.py. Testes: test_v516_v517_negative.py. Imagem de leitura: V516_V517_hit_1_0.png.

Limites: equivalência completa de revisão entre PDF e TQS não comprovada; distribuição exata das caudas mistas não definida;  controles completos de prolongamento por apoio ainda pendentes; geometria de estribos dentro dos pilares, nós/dobras e fabricação não verificados. Não dimensionar correção ou grampos automaticamente. selected_solution=null, global_negative_approval=null e known_regional_flexure_failure=true.

## 11. Validação

Ver validação da classificação na seção 13 e validação atual de apoios extremos na seção 15. Os 23 testes de términos independentes permanecem na suíte. Evidências e arquivos em V516_V517_negative_review_validation.json.

## 12. Classificação estrutural após P1 — N8/N9 independentes
O objetivo desta etapa é **VERIFICAÇÃO ESTRUTURAL do detalhamento existente**, sem otimização, proposta de encurtamento ou redesenho. A decisão `engineer_confirmed_intermediate_support_anchorage_when_not_required_v1` corrige a interpretação anterior: N8/N9 necessárias à esquerda de P1, mas dispensáveis no lóbulo negativo à direita, recebem somente ancoragem básica a partir da face física. A conclusão anterior de al+10φ inconclusivo para esse lado foi superada por esta classificação, não por alteração dos crossings. O histórico da implementação coincidente permanece em sua auditoria própria.
A camada `intermediate_support_review` comprova a remanescente em todas as regiões e vértices piecewise-linear do lóbulo conectado ao apoio, via `check_longitudinal` e Concretopy. Prova independente do lado anterior compara a composição original sem cada marca selecionada, mantendo as demais em suas posições originais. É uma comparação de necessidade, não uma sequência física de cortes. A remanescente do lado adjacente é o after físico N7, sem nenhuma das duas marcas que terminam juntas.
P1: eixo x=11,000 m; largura física 142 cm; face esquerda x=10,290 m; face direita x=11,710 m. Do vão 4, `SupportGeometry.internal_face_m` é a face direita. DEPEV=55,4 cm permanece na origem dos esforços; S1 x=11,554 m não é a origem da ancoragem. Não se transportou/interpolou/extrapolou momento até face/eixo.

### V516 — N8 / término RIGHT / P1 / vão adjacente 4
Classificação: **ANCHORAGE_BEYOND_INTERMEDIATE_SUPPORT**. Motivo: `BAR_NOT_REQUIRED_IN_ADJACENT_SPAN`; remanescente suficiente em todo o lóbulo adjacente. Necessária no vão anterior: **true**, demonstrada pela comparação independente sem esta marca. Necessária no adjacente: **false**.

| Grandeza | Resultado |
|---|---|
| Marca / quantidade / bitola | N8; 1Ø20 mm |
| Camadas físicas desde face superior | [1] |
| Composição imediatamente antes / após o término | N7+N8+N9 / N7 = 2Ø20 |
| MRd remanescente (kNm) | 122.221132129 |
| Mk_equivalente remanescente (kNm) | 87.300808664 |
| Máxima demanda negativa adjacente relevante (kNm) | 60.418770650 |
| Domínio completo comprovado do lóbulo adjacente (m) | [11.554, 13.68] |
| Domínio da prova no vão anterior (m) | [8.214166666666667, 10.446] |
| Solicitação terminal TQS S1 | x=11.554 m; Msk=-60.418770650 kNm |
| Face física de referência | right; x=11.710 m; SupportGeometry.internal_face_m |
| Término desenhado (m) | 12.840 |
| Ancoragem disponível desde face (cm) | 113.000000 |
| Condição de aderência | POOR |
| lb básico Concretopy (cm) | 78.673841577 |
| Ancoragem exigida = 1,0 lb (cm) | 78.673841577 |
| Margem (cm) | 34.326158423 |
| Posição requerida deste controle (m) | 12.496738416 |
| Resultado | PASS |

Crossing, d para al, Vk para al, al, al+lb e al+10φ **não se aplicam a esta classificação**. Nenhuma referência artificial foi gerada; S1 é mantida apenas para solicitação terminal. A posição requerida é resultado de verificação, não proposta de alteração do desenho.

### V516 — N9 / término RIGHT / P1 / vão adjacente 4
Classificação: **ANCHORAGE_BEYOND_INTERMEDIATE_SUPPORT**. Motivo: `BAR_NOT_REQUIRED_IN_ADJACENT_SPAN`; remanescente suficiente em todo o lóbulo adjacente. Necessária no vão anterior: **true**, demonstrada pela comparação independente sem esta marca. Necessária no adjacente: **false**.

| Grandeza | Resultado |
|---|---|
| Marca / quantidade / bitola | N9; 1Ø20 mm |
| Camadas físicas desde face superior | [0, 1] |
| Composição imediatamente antes / após o término | N7+N8+N9 / N7 = 2Ø20 |
| MRd remanescente (kNm) | 122.221132129 |
| Mk_equivalente remanescente (kNm) | 87.300808664 |
| Máxima demanda negativa adjacente relevante (kNm) | 60.418770650 |
| Domínio completo comprovado do lóbulo adjacente (m) | [11.554, 13.68] |
| Domínio da prova no vão anterior (m) | [8.214166666666667, 10.446] |
| Solicitação terminal TQS S1 | x=11.554 m; Msk=-60.418770650 kNm |
| Face física de referência | right; x=11.710 m; SupportGeometry.internal_face_m |
| Término desenhado (m) | 12.840 |
| Ancoragem disponível desde face (cm) | 113.000000 |
| Condição de aderência | POOR |
| lb básico Concretopy (cm) | 78.673841577 |
| Ancoragem exigida = 1,0 lb (cm) | 78.673841577 |
| Margem (cm) | 34.326158423 |
| Posição requerida deste controle (m) | 12.496738416 |
| Resultado | PASS |

Crossing, d para al, Vk para al, al, al+lb e al+10φ **não se aplicam a esta classificação**. Nenhuma referência artificial foi gerada; S1 é mantida apenas para solicitação terminal. A posição requerida é resultado de verificação, não proposta de alteração do desenho.

### V517 — N8 / término RIGHT / P1 / vão adjacente 4
Classificação: **ANCHORAGE_BEYOND_INTERMEDIATE_SUPPORT**. Motivo: `BAR_NOT_REQUIRED_IN_ADJACENT_SPAN`; remanescente suficiente em todo o lóbulo adjacente. Necessária no vão anterior: **true**, demonstrada pela comparação independente sem esta marca. Necessária no adjacente: **false**.

| Grandeza | Resultado |
|---|---|
| Marca / quantidade / bitola | N8; 1Ø20 mm |
| Camadas físicas desde face superior | [1] |
| Composição imediatamente antes / após o término | N7+N8+N9 / N7 = 2Ø20 |
| MRd remanescente (kNm) | 122.221132129 |
| Mk_equivalente remanescente (kNm) | 87.300808664 |
| Máxima demanda negativa adjacente relevante (kNm) | 64.586596900 |
| Domínio completo comprovado do lóbulo adjacente (m) | [11.554, 13.68] |
| Domínio da prova no vão anterior (m) | [8.214166666666667, 10.446] |
| Solicitação terminal TQS S1 | x=11.554 m; Msk=-64.586596900 kNm |
| Face física de referência | right; x=11.710 m; SupportGeometry.internal_face_m |
| Término desenhado (m) | 12.840 |
| Ancoragem disponível desde face (cm) | 113.000000 |
| Condição de aderência | POOR |
| lb básico Concretopy (cm) | 78.673841577 |
| Ancoragem exigida = 1,0 lb (cm) | 78.673841577 |
| Margem (cm) | 34.326158423 |
| Posição requerida deste controle (m) | 12.496738416 |
| Resultado | PASS |

Crossing, d para al, Vk para al, al, al+lb e al+10φ **não se aplicam a esta classificação**. Nenhuma referência artificial foi gerada; S1 é mantida apenas para solicitação terminal. A posição requerida é resultado de verificação, não proposta de alteração do desenho.

### V517 — N9 / término RIGHT / P1 / vão adjacente 4
Classificação: **ANCHORAGE_BEYOND_INTERMEDIATE_SUPPORT**. Motivo: `BAR_NOT_REQUIRED_IN_ADJACENT_SPAN`; remanescente suficiente em todo o lóbulo adjacente. Necessária no vão anterior: **true**, demonstrada pela comparação independente sem esta marca. Necessária no adjacente: **false**.

| Grandeza | Resultado |
|---|---|
| Marca / quantidade / bitola | N9; 1Ø20 mm |
| Camadas físicas desde face superior | [0, 1] |
| Composição imediatamente antes / após o término | N7+N8+N9 / N7 = 2Ø20 |
| MRd remanescente (kNm) | 122.221132129 |
| Mk_equivalente remanescente (kNm) | 87.300808664 |
| Máxima demanda negativa adjacente relevante (kNm) | 64.586596900 |
| Domínio completo comprovado do lóbulo adjacente (m) | [11.554, 13.68] |
| Domínio da prova no vão anterior (m) | [8.214166666666667, 10.446] |
| Solicitação terminal TQS S1 | x=11.554 m; Msk=-64.586596900 kNm |
| Face física de referência | right; x=11.710 m; SupportGeometry.internal_face_m |
| Término desenhado (m) | 12.840 |
| Ancoragem disponível desde face (cm) | 113.000000 |
| Condição de aderência | POOR |
| lb básico Concretopy (cm) | 78.673841577 |
| Ancoragem exigida = 1,0 lb (cm) | 78.673841577 |
| Margem (cm) | 34.326158423 |
| Posição requerida deste controle (m) | 12.496738416 |
| Resultado | PASS |

Crossing, d para al, Vk para al, al, al+lb e al+10φ **não se aplicam a esta classificação**. Nenhuma referência artificial foi gerada; S1 é mantida apenas para solicitação terminal. A posição requerida é resultado de verificação, não proposta de alteração do desenho.

### Provenance e limites

Regra nova, identidade independente, composição, provas regionais, diagramas assinados, fontes/camadas, chamadas Concretopy e face física estão em `/events/*/result`. Consultar `adjacent_need_evidence`, `previous_need_evidence`, `capacity_remaining`, `support_geometry`, `support_terminal_demand`, `anchorage_reference_face`, `anchorage` e `checks/basic_lb_beyond_support`. A regra S1/S13 mantém `engineer_confirmed_negative_support_terminal_section_demand_v1`.

Os casos anteriores SCALING permanecem: N3/LEFT atende; N8/LEFT falha al+lb; N9/LEFT atende. A falha regional junto a P1 persiste nas duas vigas. Caudas mistas N4/N7, controles completos de continuidade e ancoragem resistente das dobras permanecem pendentes; este PASS local não aprova a viga nem o nó. Geometria/capacidade/ramo não comprovados continuam INCONCLUSIVE. `selected_solution=null`, `detailing_optimization=null`, `global_negative_approval=null`.

## 13. Validação da classificação estrutural — etapa anterior

Na etapa anterior, 23 testes novos do classificador e 4 regressões reais adicionais passaram, preservando os 23 testes de términos coincidentes. Suíte daquela etapa: 39 extrator_lst + 30 beam_model + 34 beam_mapping + 516 reinforcement_checks = **619 aprovados**. Concretopy: **405 aprovados**. quick_validate da Skill válido; git diff --check limpo. SHA-256 de 173 arquivos protegidos: nenhuma alteração. Concretopy, goldens positivos e históricos não relacionados intactos. Comparação dos dados físicos anteriores V516/V517 confirmou geometria, regiões, apoios, nós, continuidade e controles SCALING invariantes; somente N8/N9 RIGHT receberam o controle semanticamente correto. Evidências em V516_V517_negative_review_validation.json e tmp/support_suite_results.json.

## 14. Apoios extremos em pilares — verificação estrutural explícita
Esta etapa verifica autonomamente o **detalhamento existente**, sem redução de bitolas, troca de quantidades, encurtamento, economia ou redesenho. `review_negative_end_support` identifica END/COLUMN e as marcas realmente presentes na face; cada marca conserva identidade física, camadas e demais usos. Os resultados novos são adicionados em `/end_nodes/*/verification`; o ensaio legado em `/end_nodes/*/result` permanece inalterado.
A solicitação terminal usa diretamente S1 para LEFT e S13 para RIGHT, segundo `engineer_confirmed_negative_support_terminal_section_demand_v1`, sem transportar momento ao eixo/face. Capacidade via Concretopy, com d desde a face inferior comprimida. Necessidade terminal foi comprovada por composição sem a marca: nenhum outro grupo negativo chega a essas faces. Isso não significa que a peça possa ser reduzida; N7 participa de outras regiões e a insuficiência junto a P1 permanece.
Regra geométrica `engineer_confirmed_negative_end_support_vertical_bend_v1`: perna vertical mínima=min(h_total−cobrimento−φ_estribo,2lb_básico). Reutiliza a expressão do nó existente por primitiva compartilhada; lb básico Concretopy da própria bitola, POOR e sem redução por área/gancho. A altura total é 52 cm, não d. Os 40/45 cm são as **pernas verticais escritas** na prancha auditada (página 1); comprimento, orientação e lado são documentados separadamente. Não se somam horizontal+vertical e não se dá crédito automático α=0,7.

### V516 — V516/support-1/P5A / N4 / LEFT

| Controle / grandeza | Resultado |
|---|---|
| Peça física | 3Ø16; marca N4; trajetória N4-single-drawn-piece |
| Intervalo documental (m) | -0.095 a 5.015 |
| Tipo de apoio / elemento | END / COLUMN |
| Eixo / face interna / externa (m) | 0.000 / 0.120 / -0.120 |
| Seção terminal TQS | S1, x=0.000 m, Msk original=-31.165533700 kNm |
| d resistente desde face comprimida inferior (cm) | 47.900000 |
| MRd / Mk_equivalente (kNm) | 118.167324258 / 84.405231613 |
| Necessária na solicitação terminal | true |
| Resistência terminal à flexão | PASS |
| Espaço reto geométrico dentro do apoio (cm) | 21.500000 |
| Projeção horizontal documental (cm) | 21.500000 |
| lb básico POOR (cm) | 62.939073262 |
| Reta geometricamente possível | false |
| Modo de ancoragem observado | VERTICAL_BEND |
| Altura total / cobrimento / estribo | 52 cm / 2.5 cm / Ø8 mm |
| Limite h−c−φ_estribo (cm) | 48.700000 |
| 2lb básico (cm) | 125.878146523 |
| Perna vertical requerida (cm) | 48.700000 |
| Perna vertical escrita na prancha (cm) | 40.000000 |
| Margem da perna vertical (cm) | -8.700000 |
| Geometria da perna vertical | FAIL |

| Controle independente | Status | Motivo |
|---|---|---|
| minimum_bar_spacing | INCONCLUSIVE | documentary_transverse_centers_missing |
| vibrator_access_spacing | INCONCLUSIVE | documentary_transverse_centers_missing |
| column_interference_spacing | INCONCLUSIVE | column_perpendicular_dimension_missing |
| curved_anchorage_resistance | INCONCLUSIVE | Curved anchorage resistance, pin/radius and node confinement not represented; no alpha=0.7 credit |

A flexão terminal **PASS** não aprova a dobra, cuja geometria é **FAIL**. Resistência da ancoragem curva, pinos/raios, confinamento e fabricação não foram comprovados. Nenhuma posição de seção TQS foi usada como origem da perna vertical.

### V516 — V516/support-5/P6A / N7 / RIGHT

| Controle / grandeza | Resultado |
|---|---|
| Peça física | 2Ø20; marca N7; trajetória N7-single-drawn-piece |
| Intervalo documental (m) | 3.635 a 13.775 |
| Tipo de apoio / elemento | END / COLUMN |
| Eixo / face interna / externa (m) | 13.680 / 13.560 / 13.800 |
| Seção terminal TQS | S13, x=13.680 m, Msk original=-17.063571000 kNm |
| d resistente desde face comprimida inferior (cm) | 47.700000 |
| MRd / Mk_equivalente (kNm) | 122.221132129 / 87.300808664 |
| Necessária na solicitação terminal | true |
| Resistência terminal à flexão | PASS |
| Espaço reto geométrico dentro do apoio (cm) | 21.500000 |
| Projeção horizontal documental (cm) | 21.500000 |
| lb básico POOR (cm) | 78.673841577 |
| Reta geometricamente possível | false |
| Modo de ancoragem observado | VERTICAL_BEND |
| Altura total / cobrimento / estribo | 52 cm / 2.5 cm / Ø8 mm |
| Limite h−c−φ_estribo (cm) | 48.700000 |
| 2lb básico (cm) | 157.347683154 |
| Perna vertical requerida (cm) | 48.700000 |
| Perna vertical escrita na prancha (cm) | 45.000000 |
| Margem da perna vertical (cm) | -3.700000 |
| Geometria da perna vertical | FAIL |

| Controle independente | Status | Motivo |
|---|---|---|
| minimum_bar_spacing | INCONCLUSIVE | documentary_transverse_centers_missing |
| vibrator_access_spacing | INCONCLUSIVE | documentary_transverse_centers_missing |
| column_interference_spacing | INCONCLUSIVE | column_perpendicular_dimension_missing |
| curved_anchorage_resistance | INCONCLUSIVE | Curved anchorage resistance, pin/radius and node confinement not represented; no alpha=0.7 credit |

A flexão terminal **PASS** não aprova a dobra, cuja geometria é **FAIL**. Resistência da ancoragem curva, pinos/raios, confinamento e fabricação não foram comprovados. Nenhuma posição de seção TQS foi usada como origem da perna vertical.

### V517 — V517/support-1/P5B / N4 / LEFT

| Controle / grandeza | Resultado |
|---|---|
| Peça física | 3Ø16; marca N4; trajetória N4-single-drawn-piece |
| Intervalo documental (m) | -0.095 a 5.015 |
| Tipo de apoio / elemento | END / COLUMN |
| Eixo / face interna / externa (m) | 0.000 / 0.120 / -0.120 |
| Seção terminal TQS | S1, x=0.000 m, Msk original=-32.832664200 kNm |
| d resistente desde face comprimida inferior (cm) | 47.900000 |
| MRd / Mk_equivalente (kNm) | 118.167324258 / 84.405231613 |
| Necessária na solicitação terminal | true |
| Resistência terminal à flexão | PASS |
| Espaço reto geométrico dentro do apoio (cm) | 21.500000 |
| Projeção horizontal documental (cm) | 21.500000 |
| lb básico POOR (cm) | 62.939073262 |
| Reta geometricamente possível | false |
| Modo de ancoragem observado | VERTICAL_BEND |
| Altura total / cobrimento / estribo | 52 cm / 2.5 cm / Ø8 mm |
| Limite h−c−φ_estribo (cm) | 48.700000 |
| 2lb básico (cm) | 125.878146523 |
| Perna vertical requerida (cm) | 48.700000 |
| Perna vertical escrita na prancha (cm) | 40.000000 |
| Margem da perna vertical (cm) | -8.700000 |
| Geometria da perna vertical | FAIL |

| Controle independente | Status | Motivo |
|---|---|---|
| minimum_bar_spacing | INCONCLUSIVE | documentary_transverse_centers_missing |
| vibrator_access_spacing | INCONCLUSIVE | documentary_transverse_centers_missing |
| column_interference_spacing | INCONCLUSIVE | column_perpendicular_dimension_missing |
| curved_anchorage_resistance | INCONCLUSIVE | Curved anchorage resistance, pin/radius and node confinement not represented; no alpha=0.7 credit |

A flexão terminal **PASS** não aprova a dobra, cuja geometria é **FAIL**. Resistência da ancoragem curva, pinos/raios, confinamento e fabricação não foram comprovados. Nenhuma posição de seção TQS foi usada como origem da perna vertical.

### V517 — V517/support-5/P6B / N7 / RIGHT

| Controle / grandeza | Resultado |
|---|---|
| Peça física | 2Ø20; marca N7; trajetória N7-single-drawn-piece |
| Intervalo documental (m) | 3.635 a 13.775 |
| Tipo de apoio / elemento | END / COLUMN |
| Eixo / face interna / externa (m) | 13.680 / 13.560 / 13.800 |
| Seção terminal TQS | S13, x=13.680 m, Msk original=-20.456671900 kNm |
| d resistente desde face comprimida inferior (cm) | 47.700000 |
| MRd / Mk_equivalente (kNm) | 122.221132129 / 87.300808664 |
| Necessária na solicitação terminal | true |
| Resistência terminal à flexão | PASS |
| Espaço reto geométrico dentro do apoio (cm) | 21.500000 |
| Projeção horizontal documental (cm) | 21.500000 |
| lb básico POOR (cm) | 78.673841577 |
| Reta geometricamente possível | false |
| Modo de ancoragem observado | VERTICAL_BEND |
| Altura total / cobrimento / estribo | 52 cm / 2.5 cm / Ø8 mm |
| Limite h−c−φ_estribo (cm) | 48.700000 |
| 2lb básico (cm) | 157.347683154 |
| Perna vertical requerida (cm) | 48.700000 |
| Perna vertical escrita na prancha (cm) | 45.000000 |
| Margem da perna vertical (cm) | -3.700000 |
| Geometria da perna vertical | FAIL |

| Controle independente | Status | Motivo |
|---|---|---|
| minimum_bar_spacing | INCONCLUSIVE | documentary_transverse_centers_missing |
| vibrator_access_spacing | INCONCLUSIVE | documentary_transverse_centers_missing |
| column_interference_spacing | INCONCLUSIVE | column_perpendicular_dimension_missing |
| curved_anchorage_resistance | INCONCLUSIVE | Curved anchorage resistance, pin/radius and node confinement not represented; no alpha=0.7 credit |

A flexão terminal **PASS** não aprova a dobra, cuja geometria é **FAIL**. Resistência da ancoragem curva, pinos/raios, confinamento e fabricação não foram comprovados. Nenhuma posição de seção TQS foi usada como origem da perna vertical.

### Disposição transversal e interferência — dados disponíveis

A regra `engineer_confirmed_negative_reinforcement_vibrator_clearance_v1` exige ao menos um vão livre entre barras adjacentes ≥4,0 cm; não exige 4 cm em todos os vãos. A rotina recebe centros reais por marca/camada/bitola, calcula todos os vãos e compara os demais com a primitiva existente `Concretopy.normas.espacamento_min_arm_long_viga`. O parâmetro default de agregado 16 mm é identificado como o contrato atual, não como certificação do agregado real ou de toda a norma. Não se presume distribuição uniforme a partir da quantidade de barras.

A seção e o cobrimento conhecidos permitem registrar b−2c=14,0 cm e largura interna ao estribo Ø8=12,4 cm. Isso não fornece os centros transversais desenhados. Logo, mínimo e corredor ficam **INCONCLUSIVE** nestes goldens, sem bloquear a geometria das pernas verticais.

A hipótese `engineer_confirmed_column_interference_effective_cover_v1` implementa c_eff=c_real+2,5 cm **apenas** para o ensaio transversal, quando a dimensão perpendicular documentada do pilar equivale à largura da viga. Registrar b_useful=b−2c_eff e, separadamente, o desconto do estribo físico. Não mudar seção resistente, d, MRd ou lb; testar os mesmos centros, sem deslocá-los.

Os 24 cm de RELDTFPS são dimensão **longitudinal do apoio**, não perpendicular. Os modelos/fontes atualmente utilizados não fornecem dimensão transversal de P5/P6 vinculada a estas faces. Portanto **column_interference_spacing=INCONCLUSIVE**, e não c_eff aplicado por suposição. Igualdade geométrica é exata por default; nenhuma tolerância geral foi criada. Tolerância não nula exige entrada e provenance explícitas do chamador.

### Limites e preservação

Geometria da perna vertical não prova resistência da curva. Permanecem fora do escopo nó completo, raios/pinos, interferência detalhada com armadura do pilar, caminhos de vibrador alinhados entre camadas, tolerâncias de montagem e otimização. Nenhum grampo negativo foi implementado.

A preferência futura do engenheiro por menor bitola capaz de atender numa camada foi documentada, condicionada à resistência, espaçamentos, vibrador, interferência, ancoragem e uso global da peça; **não foi executada**. N7 permanece a peça existente 2Ø20. selected_solution=null e detailing_optimization=null em todos os resultados novos. Não há aprovação global das vigas.

As insuficiências de flexão N7+N8+N9 à esquerda de P1 e al+lb da N8/LEFT permanecem exatamente como verificadas anteriormente. N8/N9 à direita de P1 continuam em ANCHORAGE_BEYOND_INTERMEDIATE_SUPPORT com os mesmos comprimentos/resultados. Identidades, términos coincidentes e controles anteriores não foram modificados.

Provenance dos controles novos: `/end_nodes/*/verification/terminal_demand`, `capacity`, `physical_bar`, `geometry`, `anchorage`, `checks/vertical_bend_geometry/provenance`, `transverse_disposition` e demais `checks`. Fonte das pernas: `bend_documents` explicitamente associada a marca/lado/orientação/fonte da prancha. O resultado legado do nó continua integralmente preservado.

## 15. Validação final — apoio extremo

40 novos testes do módulo e 4 regressões reais adicionais; todos os anteriores preservados. Suíte completa: 39 extrator_lst + 30 beam_model + 34 beam_mapping + 560 reinforcement_checks = **663 aprovados**. Concretopy: **405 aprovados**, sem alteração. quick_validate da Skill válido; git diff --check limpo. Comparação SHA-256 de **174 arquivos protegidos**, incluindo Concretopy e goldens históricos não relacionados: nenhum mudou. Comparação exata dos casos anteriores V516/V517 confirmou regiões, eventos, dados geométricos, apoios intermediários e resultados legados dos nós invariantes. Apenas controles novos foram adicionados em verification. Evidências em V516_V517_negative_review_validation.json e tmp/support_suite_results.json; arquitetura/arquivos em negative_end_support_review_implementation.md.

## 16. RELAÇÕES ENTRE ARMADURAS NEGATIVAS DE APOIOS CONSECUTIVOS

Atualização de 07/10/2026. Objetivo: verificar e interpretar o detalhamento existente. Nenhuma otimização global, redesenho ou solução aplicada. Os cálculos/diagnósticos anteriores continuam como histórico; as interpretações indicadas abaixo são **SUPERSEDED** por controles agora definidos pelo engenheiro.

### N4/N7 — encontro de detalhamento

Apoios associados: ocorrências 2 e 3, eixos x=2,080 e 6,620 m; ambos possuem rótulo P2A na V516 ou P2B na V517. São ocorrências físicas distintas, separadas pela geometria do vão, não confundidas pela repetição do nome. Intervalo do diagrama entre faces internas: [2,190;6,510] m.

N4=3Ø16, intervalo documental [-0,095;5,015] m. N7=2Ø20, intervalo [3,635;13,775] m. Fonte: peças únicas da prancha RMP-EST-EX-1348, página 1, com hipóteses geométricas já autorizadas e preservadas.

Classificação **DETAILING_OVERLAP**: peças distintas associadas às regiões negativas dos apoios; encontro de caudas previamente confirmado pelo engenheiro; diagrama assinado contém trecho positivo entre os apoios. Portanto não é transição resistente em momento permanentemente negativo. A geometria de interseção, sozinha, não determinou a classificação.

Interseção física: **[3,635;5,015] m**, comprimento **138,0 cm**. Controle de comprimento: 30,0 cm, margem **108,0 cm — PASS**. O limite de 80 cm não é comprimento requerido de overlap. Regra de traspasse 2lb não se aplica a esse encontro.

Áreas pela API Barra: N4=6,031858 cm²; N7=6,283185 cm². N4 possui menor As total e menor bitola neste caso; isso é coincidência dos dados, não equivalência geral dos dois critérios.

Para resistência do encontro, utilizar **N4 completa (3Ø16), isolada**, d=48,2 cm da posição própria de referência já utilizada nas verificações isoladas do vão: seção 19x52, cobrimento 2,5, estribo regional Ø5, ordem da camada superior e posicionamento convencional retornado pelo Concretopy. Isso não inventa a disposição conjunta/transversal N4+N7. Não há soma de áreas, centroide misto ou crédito apenas de 1Ø16.

| Viga | MRd N4 (kNm) | Mk equivalente N4 (kNm) | Máxima demanda negativa no encontro (kNm) | x governante (m) | Resistência |
|---|---:|---:|---:|---:|---|
| V516 | 118.954088 | 84.967206 | 15.671761 | 5.015 | PASS |
| V517 | 118.954088 | 84.967206 | 15.333108 | 5.015 | PASS |

A demanda foi pesquisada em todo o intervalo, incluindo as duas extremidades interpoladas e todos os vértices TQS internos. Os valores positivos não foram convertidos em negativos. O x=5,015 m é documental; não foi movido até a seção TQS mais próxima. Nenhuma extrapolação ou interpolação de gaps.

### Comprimentos necessários e comparação local de massa

Os limites estruturalmente necessários individuais de N4/RIGHT e N7/LEFT não estão resolvidos por controles independentes prévios com geometria suficiente. As pontas desenhadas NÃO substituem esses limites. Logo, **required_end/start=null**, **gap estrutural não resolvido** e **economic_comparison.applicable=null**; não inferir gap=-138 cm para esta comparação usando apenas os endpoints fornecidos.

O encontro já possui 138 cm fisicamente: o déficit geométrico para 30 cm é zero. Isso não basta para calcular a comparação entre duas alternativas baseadas nos comprimentos estruturalmente necessários. A quantidade, comprimento e política de comprimento mínimo do porta-estribo não estão confirmados nas referências atuais: somente sua função, demanda nula e bitola regional mínima estão formalizadas. Nenhuma peça fictícia ou massa foi criada.

A infraestrutura implementada calcula massa local quando esses dados são fornecidos e rastreáveis: menor As total, comprimento por barra gap+30 quando não há overlap, somente déficit quando já existe encontro, quantidade completa e densidade explicitamente informada. Menor massa nunca aprova uma falha resistente; não há desempate automático nem escolha final.

### N7 — continuidade física P2/P1

Ocorrências 3 e 4: P2 em x=6,620 m e P1 em x=11,000 m. Faces do trecho: x=6,730 a 10,290 m. N7 conserva a mesma marca, trajetória documental única, quantidade 2, bitola Ø20, camada própria e intervalo [3,635;13,775] m. Não existe término entre esses apoios.

Classificação **CONTINUOUS_NEGATIVE_REINFORCEMENT**, por identidade da peça e geometria. Não houve divisão fictícia ou resistência adicional de continuidade. Os resultados regionais existentes continuam sendo os controles resistentes.

**Divergência factual registrada:** os dados TQS atuais não comprovam que o momento permaneça negativo em todo o vão 3. Na V516 existe Msk=+5,383851 kNm em x=8,214167 m; o diagrama também muda de sinal na V517. A preferência geral do engenheiro por continuidade quando o momento não zera permanece documentada, mas não foi usada para falsificar o comportamento deste exemplo. A identidade física de N7 independe disso, e sua classificação continua válida. Não há impacto sobre a regra de resistência ou demanda terminal.

A falha N7+N8+N9 à esquerda de P1 continua: Mk equivalente=160,317415 kNm contra 168,988193 kNm (V516) e 162,378511 kNm (V517). Continuidade não elimina essa insuficiência.

### Reavaliação individual dos términos antigos

| Evento | Interpretação histórica | Verificação atual | Situação |
|---|---|---|---|
| N3/RIGHT | SCALING bloqueado por centroide misto | ANCHORAGE_BEYOND_INTERMEDIATE_SUPPORT | PASS nas duas vigas; histórico SUPERSEDED |
| N4/RIGHT | término bloqueado por centroide N4+N7 | DETAILING_OVERLAP com N7 | Comprimento/resistência PASS; geometria conjunta pendente; histórico SUPERSEDED |
| N7/LEFT | término bloqueado por centroide N4+N7 | DETAILING_OVERLAP com N4 | Comprimento/resistência PASS; geometria conjunta pendente; histórico SUPERSEDED |

**N3/RIGHT:** a revisão adicional demonstra necessidade no vão anterior e suficiência de N4 isolada em todo o ramo adjacente. N4 com estribo Ø8 fornece Mk=84,405232 kNm no lado anterior; a demanda terminal supera essa capacidade, comprovando a necessidade de N3. No vão adjacente N4 fornece Mk=84,967206 kNm e atende ao ramo inteiro. O motor existente de apoio intermediário comprova ambas as situações com seus diagramas próprios, sem procurar crossing artificial.

Composição documental no término: N3+N4+N7; remanescente físico N4+N7. A prova conservadora considera somente N4 para resistência remanescente; N7 permanece documentada e não recebe crédito. Não há remoção sequencial fictícia nem composição física intermediária proposta. Os campos de subset da prova são separados da composição documental e preservam a origem da regra do encontro.

Ancoragem N3 medida desde a **face direita física do apoio da ocorrência 2, x=2,190 m**, até x=3,670 m: disponível=148,000 cm; lb básico Ø16 POOR=62,939073 cm; margem=85,060927 cm; posição requerida=2,819391 m. **PASS** para ambas. Não usar S1 como origem, não calcular al+lb ou al+10phi nesse lado. O antigo requisito de centroide misto foi eliminado por identificação do fenômeno correto, não por fabricação de d.

**N4/RIGHT e N7/LEFT:** são limites do encontro entre caudas, não uma composição mista resistente convencional obrigatória. Os controles atuais são comprimento de 30 cm e resistência do grupo completo de menor bitola. Não se atribui PASS global aos términos: disposição física e massa local permanecem independentes/pendentes.

Os resultados históricos de `events/result` e `regions/result` são conservados. Consultar `events/current_interpretation`, `events/current_verification` da N3, `event_interpretations` e `negative_support_relations` para a interpretação vigente. Os dois resultados regionais antigos do encontro são referências históricas sem soma creditada; a resistência vigente do encontro está no novo controle isolado completo. SCALING genuíno em outras regiões não foi modificado.

### Espaçamento localizado, vibrador e limites restantes

Para pares individuais explicitamente envolvidos em encontro/traspasse, a exceção do mínimo usual é local e não altera Concretopy ou minimum_bar_spacing geral. Acomodações físicas continuam exigidas. O corredor >=4 cm pode estar em outro espaço do arranjo global; não é imposto entre o par sobreposto.

No caso real não existem centros transversais individuais documentados do encontro. **local_spacing_geometry=INCONCLUSIVE** e **vibrator_access_spacing=INCONCLUSIVE**. Não foram criadas posições, camadas novas ou distribuição uniforme. Permanecem fora da prova completa colisões entre camadas, interferências do nó, tolerâncias e fabricação. **ready_for_detailing=false**.

As pendências artificiais de centroide foram superadas nos três términos acima. Permanecem os dados de limites estruturais para a comparação econômica, porta-estribo e distribuição conjunta. Não há aprovação global das vigas; falhas regionais/P1, N8/LEFT e dobras P5/N4 e P6/N7 continuam preservadas. N8/N9 RIGHT continuam independentes, PASS na ancoragem básica desde a face de P1, sem retorno a SCALING.

### Provenance e arquitetura

Camada semântica: `negative_reinforcement_relations.py`; massa única com densidade explícita: `steel_mass.py`. Reutilizados `moment_diagram`, `prepare_reinforcement`, `composition_capacity`, `basic_anchorage`, `negative_detailing.check_stirrup_holder`, `transverse_disposition` e `check_intermediate_bar_event`. Nenhuma equação de resistência/ancoragem/interpolação foi copiada.

Decisões: engineer_confirmed_negative_continuity_preference_v1; engineer_confirmed_negative_detailing_overlap_v1; engineer_confirmed_negative_detailing_overlap_weight_choice_v1; engineer_confirmed_negative_detailing_overlap_max_gap_v1; engineer_confirmed_negative_lap_transition_v1; engineer_confirmed_negative_overlap_capacity_v1; engineer_confirmed_negative_overlap_local_spacing_v1. São procedimentos do engenheiro, não atribuições à NBR. Preservadas as decisões anteriores, inclusive S1/S13 e ancoragem após apoio intermediário.

JSON: `/negative_support_relations/*/provenance`, `moment_between_supports`, `physical_overlap`, `isolated_capacity`, `overlap_demand`, `overlap_flexural_capacity`, `economic_comparison`, `transverse_audit`; N3 em `/events/1/current_verification`, com provas anterior/adjacente, composição documental, subset conservador e face física.

selected_solution=null; detailing_optimization=null. Nenhuma proposta de encurtar, trocar barras, marcas ou corrigir automaticamente foi aplicada.

## 17. Validação final — relações entre apoios

**74 novos testes** de classificação, massa, traspasse, capacidade completa, gaps, exceção local e regressões reais. Suíte completa: 39 extrator_lst + 30 beam_model + 34 beam_mapping + 634 reinforcement_checks = **737 aprovados**. Concretopy: **405 aprovados**, sem alteração. quick_validate: Skill válida. git diff --check limpo.

Comparação SHA-256 de **195 arquivos protegidos**: nenhum mudou. Comparação exata confirma todas as regiões/composições, diagramas, geometria, resultados históricos de eventos, apoios intermediários e controles extremos anteriores inalterados em V516/V517; foram adicionadas relações e interpretações atuais. Goldens positivos e negativos históricos não relacionados permaneceram idênticos. Evidências em V516_V517_negative_review_validation.json e tmp/negative_relations_baseline.json.

## 18. Revisão independente de armadura transversal ao cortante

Esta etapa verifica o detalhamento existente. Não verifica suspensão, não transfere reações nem propõe alterações. A referência por terços não define fronteiras obrigatórias das faixas desenhadas.

Atualização em 08/10/2026: classificação anterior de N12 e exigência de estribos no interior de pilares corrigidas segundo decisões explícitas do engenheiro. N12 é negativa de laje adjacente em desnível, não estribo da viga. Os resultados de referência por terços e os controles das faixas convencionais abaixo permaneceram numericamente invariantes.

### Altura útil e procedimento

Nas duas vigas: d=46,7 cm, proveniente da composição física N7+N8+N9, duas camadas, As=12,566371 cm². Regra confirmada: maior número de camadas, maior As em empate e menor d no último desempate. Áreas e centroides foram reutilizados dos resultados longitudinais do Concretopy. Não há bitola equivalente.

O adaptador expõe esse d à interface da seção, preservando seção real 19×52 cm, cobrimento e materiais. Escopo: estribos verticais e Nk=Mk=0. O Concretopy calcula VRd2, Vc e Asw/s governante; o mínimo vem de chamada independente com Vk=0. A API não expõe separadamente a parcela resistente antes da governância pelo mínimo: esse campo permanece null.

A comparação de smax no Concretopy foi corrigida com autorização explícita: Vsd≤0,67VRd2 usa min(0,6d,30cm); acima usa min(0,3d,20cm). O critério foi fornecido pelo engenheiro, sem alegar consulta integral da norma. A chamada usa o mesmo d/VRd2 do cálculo de cortante.

Máximos consideram ambas as envoltórias características, endpoints consultáveis e vértices internos, preservando sinal e governantes empatados. Sem extrapolação, interpolação através de gaps ou transporte a faces/eixos. Biela, área, smax, ramos e prática usual têm estados independentes.

### V516: referência por terços

| Vão/terço | Intervalo m | máximo módulo Vk kN | Asw/s cm²/m | Ø5 s máximo/prático cm | Ø6,3 s máximo/prático cm | Ø8 s máximo/prático cm |
|---|---|---:|---:|---|---|---|
| 1/1 | [0.0, 0.6933333333333334] | 66.744060 | 2.666704 | 14.726008/14.000000 | 23.379011/20.000000 | 28.020000/33.000000 |
| 1/2 | [0.6933333333333334, 1.3866666666666667] | 63.547092 | 2.666704 | 14.726008/14.000000 | 23.379011/20.000000 | 28.020000/33.000000 |
| 1/3 | [1.3866666666666667, 2.08] | 66.969613 | 2.666704 | 14.726008/14.000000 | 23.379011/20.000000 | 28.020000/33.000000 |
| 2/1 | [2.08, 3.5933333333333333] | 50.102175 | 2.666704 | 14.726008/14.000000 | 23.379011/20.000000 | 28.020000/33.000000 |
| 2/2 | [3.5933333333333333, 5.1066666666666665] | 43.472879 | 2.666704 | 14.726008/14.000000 | 23.379011/20.000000 | 28.020000/33.000000 |
| 2/3 | [5.1066666666666665, 6.62] | 54.750527 | 2.666704 | 14.726008/14.000000 | 23.379011/20.000000 | 28.020000/33.000000 |
| 3/1 | [6.62, 7.895333333333333] | 78.619913 | 2.666704 | 14.726008/14.000000 | 23.379011/20.000000 | 28.020000/33.000000 |
| 3/2 | [7.895333333333333, 9.170666666666667] | 91.466625 | 2.666704 | 14.726008/14.000000 | 23.379011/20.000000 | 28.020000/33.000000 |
| 3/3 | [9.170666666666667, 10.446] | 104.803669 | 2.918030 | 13.457679/12.000000 | 21.365411/20.000000 | 28.020000/33.000000 |
| 4/1 | [11.554, 12.262666666666666] | 37.883089 | 2.666704 | 14.726008/14.000000 | 23.379011/20.000000 | 28.020000/33.000000 |
| 4/2 | [12.262666666666666, 12.971333333333334] | 40.942764 | 2.666704 | 14.726008/14.000000 | 23.379011/20.000000 | 28.020000/33.000000 |
| 4/3 | [12.971333333333334, 13.68] | 47.895679 | 2.666704 | 14.726008/14.000000 | 23.379011/20.000000 | 28.020000/33.000000 |

Dois ramos convencionais neste cenário de referência; não se atribui essa eficácia à N12. O espaçamento máximo contínuo e o prático conservador da API são distintos. Nenhuma opção foi selecionada.

### V516: faixas reais

| Vão/marca | Intervalo m | Ø mm / s cm / ramos | Vk assinado kN; série; x m | Vsd kN | Asw/s exigida / fornecida cm²/m | Área | smax | Resultado |
|---|---|---|---|---:|---|---|---|---|
| 2/N13 | [2.19, 6.51] | 5 / 14 / 2 | -53.615720; min; 6.510000 | 75.062009 | 2.666704 / 2.804993 | PASS | PASS | PASS |
| 3/N13 | [6.73, 8.64] | 5 / 14 / 2 | 78.000756; max; 6.730000 | 109.201059 | 2.666704 / 2.804993 | PASS | PASS | PASS |
| 3/N1 | [8.64, 9.16] | 8 / 12 / 2 | -90.083420; min; 9.160000 | 126.116789 | 2.666704 / 8.377580 | PASS | PASS | PASS |
| 3/N13 | [9.16, 10.29] | 5 / 10 / 2 | -104.803669; min; 10.127167 | 146.725136 | 2.918030 / 3.926991 | PASS | PASS | PASS |

Todos os controles calculáveis de biela atendem: VRd2=574,970400 kN. Asw/s mínimo=2,666704 cm²/m; smax=28,02 cm. N13/N1 convencionais atendem aos controles calculados. N1 foi verificada somente para cortante: isso não aprova suspensão.

N12 é ADJACENT_SLAB_NEGATIVE_REINFORCEMENT, para continuidade da negativa entre lajes adjacentes em desnível. Sua identidade, geometria e evidências foram preservadas em excluded_reinforcement; não recebe Asw/s, ramos ou dimensionamento de estribo. Não existe estribo resistente de viga documentalmente comprovado nos vãos extremos nesta leitura.

Os oito intervalos antes pendentes foram confrontados com faces e larguras documentadas dos pilares: WITHIN_SUPPORT / NOT_APPLICABLE para cobertura por estribos da viga. A geometria e o domínio TQS estão discriminados abaixo.

Pendências reais: UNCOVERED_REQUIRED_REGION nos vãos 1 [0,120;1,970] m e 4 [11,710;13,560] m. N12 não fornece cobertura resistente. Vãos 2 e 3: cobertura física comprovada pelas faixas N13/N1.

`global_shear_approval=null`: não há falha estrutural comprovada nos controles resolvidos, mas faltam estribos de viga documentados nos dois trechos físicos extremos. Não há inconclusão por ramos de N12 nem exigência de estribos dentro de pilares.

### V517: referência por terços

| Vão/terço | Intervalo m | máximo módulo Vk kN | Asw/s cm²/m | Ø5 s máximo/prático cm | Ø6,3 s máximo/prático cm | Ø8 s máximo/prático cm |
|---|---|---:|---:|---|---|---|
| 1/1 | [0.0, 0.6933333333333334] | 66.822513 | 2.666704 | 14.726008/14.000000 | 23.379011/20.000000 | 28.020000/33.000000 |
| 1/2 | [0.6933333333333334, 1.3866666666666667] | 62.664493 | 2.666704 | 14.726008/14.000000 | 23.379011/20.000000 | 28.020000/33.000000 |
| 1/3 | [1.3866666666666667, 2.08] | 68.577903 | 2.666704 | 14.726008/14.000000 | 23.379011/20.000000 | 28.020000/33.000000 |
| 2/1 | [2.08, 3.5933333333333333] | 48.601757 | 2.666704 | 14.726008/14.000000 | 23.379011/20.000000 | 28.020000/33.000000 |
| 2/2 | [3.5933333333333333, 5.1066666666666665] | 42.050915 | 2.666704 | 14.726008/14.000000 | 23.379011/20.000000 | 28.020000/33.000000 |
| 2/3 | [5.1066666666666665, 6.62] | 53.593342 | 2.666704 | 14.726008/14.000000 | 23.379011/20.000000 | 28.020000/33.000000 |
| 3/1 | [6.62, 7.895333333333333] | 77.972674 | 2.666704 | 14.726008/14.000000 | 23.379011/20.000000 | 28.020000/33.000000 |
| 3/2 | [7.895333333333333, 9.170666666666667] | 86.631946 | 2.666704 | 14.726008/14.000000 | 23.379011/20.000000 | 28.020000/33.000000 |
| 3/3 | [9.170666666666667, 10.446] | 103.401318 | 2.810593 | 13.972108/12.000000 | 22.182119/20.000000 | 28.020000/33.000000 |
| 4/1 | [11.554, 12.262666666666666] | 41.894009 | 2.666704 | 14.726008/14.000000 | 23.379011/20.000000 | 28.020000/33.000000 |
| 4/2 | [12.262666666666666, 12.971333333333334] | 47.611286 | 2.666704 | 14.726008/14.000000 | 23.379011/20.000000 | 28.020000/33.000000 |
| 4/3 | [12.971333333333334, 13.68] | 50.033528 | 2.666704 | 14.726008/14.000000 | 23.379011/20.000000 | 28.020000/33.000000 |

Dois ramos convencionais neste cenário de referência; não se atribui essa eficácia à N12. O espaçamento máximo contínuo e o prático conservador da API são distintos. Nenhuma opção foi selecionada.

### V517: faixas reais

| Vão/marca | Intervalo m | Ø mm / s cm / ramos | Vk assinado kN; série; x m | Vsd kN | Asw/s exigida / fornecida cm²/m | Área | smax | Resultado |
|---|---|---|---|---:|---|---|---|---|
| 2/N13 | [2.19, 6.51] | 5 / 14 / 2 | -52.946103; min; 6.510000 | 74.124545 | 2.666704 / 2.804993 | PASS | PASS | PASS |
| 3/N13 | [6.73, 8.64] | 5 / 14 / 2 | 77.353517; max; 6.730000 | 108.294924 | 2.666704 / 2.804993 | PASS | PASS | PASS |
| 3/N1 | [8.64, 9.16] | 8 / 12 / 2 | -85.253991; min; 9.160000 | 119.355588 | 2.666704 / 8.377580 | PASS | PASS | PASS |
| 3/N13 | [9.16, 10.29] | 5 / 10 / 2 | -102.902301; min; 10.290000 | 144.063222 | 2.772362 / 3.926991 | PASS | PASS | PASS |

Todos os controles calculáveis de biela atendem: VRd2=574,970400 kN. Asw/s mínimo=2,666704 cm²/m; smax=28,02 cm. N13/N1 convencionais atendem aos controles calculados. N1 foi verificada somente para cortante: isso não aprova suspensão.

N12 é ADJACENT_SLAB_NEGATIVE_REINFORCEMENT, para continuidade da negativa entre lajes adjacentes em desnível. Sua identidade, geometria e evidências foram preservadas em excluded_reinforcement; não recebe Asw/s, ramos ou dimensionamento de estribo. Não existe estribo resistente de viga documentalmente comprovado nos vãos extremos nesta leitura.

Os oito intervalos antes pendentes foram confrontados com faces e larguras documentadas dos pilares: WITHIN_SUPPORT / NOT_APPLICABLE para cobertura por estribos da viga. A geometria e o domínio TQS estão discriminados abaixo.

Pendências reais: UNCOVERED_REQUIRED_REGION nos vãos 1 [0,120;1,970] m e 4 [11,710;13,560] m. N12 não fornece cobertura resistente. Vãos 2 e 3: cobertura física comprovada pelas faixas N13/N1.

`global_shear_approval=null`: não há falha estrutural comprovada nos controles resolvidos, mas faltam estribos de viga documentados nos dois trechos físicos extremos. Não há inconclusão por ramos de N12 nem exigência de estribos dentro de pilares.

### Transições, proveniência e limitações

A capacidade inversa é obtida por chamadas reais ao Concretopy, sem copiar equações resistentes. Os crossings usam o diagrama linear existente, separado para +Vk e −Vk e selecionado por ramo/orientação. Não se discretiza x. Nos ramos declarados das faixas N13, capacidades características de referência: 103,328229 kN (Ø5 c/14) e 117,973430 kN (Ø5 c/10). A demanda é integralmente inferior: não há crossing governante, diagnóstico NOT_APPLICABLE, sem fronteira fictícia. As transições documentais 8,640/9,160 m permanecem intactas.

Os JSON próprios preservam séries, governantes, fontes TQS/prancha, assinaturas e hashes das APIs, parâmetros, chamadas e diagnósticos. Regras consolidadas em shear-reinforcement-review.md e shear_review.md. Suspensão permanece NOT_EVALUATED. REVIEW de prática usual não equivale a FAIL estrutural. selected_solution/detailing_optimization continuam null. Não há aprovação global da viga.

## 19. Validação da etapa de cortante

Histórico da execução inicial em 07/10/2026 (antes desta correção):

842 testes assistant aprovados: 39 extrator_lst, 30 beam_model, 34 beam_mapping, 739 reinforcement_checks. Incluem 105 novos testes de contratos, diagramas, faixas, opções, controles independentes, ramos e goldens. Concretopy: 413 aprovados, incluindo oito novos testes próprios de smax. quick_validate: Skill válida.

199 arquivos protegidos permanecem idênticos ao baseline. A única alteração preexistente no Concretopy foi comprovada por hash após reversão em memória da comparação autorizada. Não mudaram os goldens longitudinais/positivos e históricos não relacionados. Permanecem a falha regional junto a P1, N8/LEFT al+lb e as falhas de dobra de N4/N7.


### Correção funcional e geométrica — 08/10/2026

Decisões: engineer_confirmed_n12_adjacent_slab_negative_reinforcement_v1 e engineer_confirmed_stirrups_terminate_at_column_faces_v1. Função é interpretada por evidências documentais, confirmação do engenheiro e geometria; não por nome, Ø8 ou c/20 isoladamente. Peça ambígua continua inconclusiva e não fornece cobertura.

A classificação está em shear_coverage.classify_piece; a partição física em physical_coverage; review_shear_spans mantém cálculos existentes e exclui peças não aplicáveis. O adaptador fornece os apoios físicos existentes e fontes de identificação como pilares. Não foi adotado deslocamento fixo ou DEPEV como face.

| Vão | Domínio TQS m | Eixo esquerdo / largura m | Face interna esquerda m | Eixo direito / largura m | Face interna direita m | Cobertura obrigatória m |
|---|---|---|---:|---|---:|---|
| 1 | [0.0, 2.08] | 0.0 / 0.24 | 0.12 | 2.08 / 0.22 | 1.97 | [0.12, 1.97] |
| 2 | [2.08, 6.62] | 2.08 / 0.22 | 2.19 | 6.62 / 0.22 | 6.51 | [2.19, 6.51] |
| 3 | [6.62, 10.446] | 6.62 / 0.22 | 6.73 | 11.0 / 1.42 | 10.29 | [6.73, 10.29] |
| 4 | [11.554, 13.68] | 11.0 / 1.42 | 11.71 | 13.68 / 0.24 | 13.56 | [11.71, 13.56] |

Geometria compartilhada V516/V517; esforços individuais preservados. P1: eixo 11,000 m, largura longitudinal 1,420 m, faces 10,290/11,710 m e DEPEV documental 0,554 m. Terminais TQS adjacentes 10,446/11,554 m permanecem distintos das faces físicas. Não se transportou esforço para face/eixo.

| Vão | Intervalo anteriormente pendente m | Pilar/faces m | Classificação | Exigência de cobertura |
|---|---|---|---|---|
| 1 | [0.0, 0.12] | P5A [-0.12;0.12] | WITHIN_SUPPORT | NOT_APPLICABLE |
| 1 | [1.97, 2.08] | P2A [1.97;2.19] | WITHIN_SUPPORT | NOT_APPLICABLE |
| 2 | [2.08, 2.19] | P2A [1.97;2.19] | WITHIN_SUPPORT | NOT_APPLICABLE |
| 2 | [6.51, 6.62] | P2A [6.51;6.73] | WITHIN_SUPPORT | NOT_APPLICABLE |
| 3 | [6.62, 6.73] | P2A [6.51;6.73] | WITHIN_SUPPORT | NOT_APPLICABLE |
| 3 | [10.29, 10.446] | P1A [10.29;11.71] | WITHIN_SUPPORT | NOT_APPLICABLE |
| 4 | [11.554, 11.71] | P1A [10.29;11.71] | WITHIN_SUPPORT | NOT_APPLICABLE |
| 4 | [13.56, 13.68] | P6A [13.56;13.8] | WITHIN_SUPPORT | NOT_APPLICABLE |

Demais trechos físicos: vão 1 [0,120;1,970] e vão 4 [11,710;13,560] são UNCOVERED_REQUIRED_REGION / INCONCLUSIVE. Vão 2 [2,190;6,510] e vão 3 [6,730;10,290] são REQUIRED_BEAM_COVERAGE / PASS, com as quatro faixas reais tabeladas na seção 18. Nenhuma faixa foi prolongada. A ausência de estribos comprovados não é automaticamente uma reprovação estrutural: permanece uma pendência documental necessária.

Concretopy permaneceu idêntico durante esta rodada, incluindo a correção anterior de smax e seus oito testes. A autorização expressa foi dada pelo engenheiro em 07/10/2026 e reafirmada nesta solicitação; a origem técnica do critério é a informação normativa fornecida pelo engenheiro, sem consulta integral do texto normativo nesta tarefa. Não há nova alteração ou reversão.

Validação atual: 877 testes assistant aprovados (39+30+34+774), incluindo 35 novos testes de cobertura/classificação; 140 testes de cortante ao todo. Concretopy: 413 aprovados. quick_validate: Skill válida. 174 arquivos protegidos iguais ao baseline; dentre esses, todos os arquivos anteriores do Concretopy e goldens não relacionados. Prefixo longitudinal do relatório mantido byte a byte. Os hashes de regressão da referência por terços e dos controles completos N13/N1 são iguais aos da execução anterior.

selected_solution e detailing_optimization permanecem null. Suspensão continua NOT_EVALUATED. Nenhuma alteração automática de armadura foi proposta ou executada.
