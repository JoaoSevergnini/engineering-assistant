# Verificação por trechos de seção constante — pavimento TIPO

O procedimento foi integrado ao fluxo atual, com seleção de cortante no trecho físico antes do cálculo de `a_l` e pesquisa de momentos ampliada somente depois desse cálculo. Os casos sintéticos executam os métodos existentes de flexão, cortante e suspensão. Na V611 real, foi possível selecionar os esforços dos três vãos livres; não foi possível concluir os cálculos resistentes com as informações longitudinais atualmente comprovadas. **A V611 não está aprovada.**

## 1. V611 — documentos e geometria efetivamente identificada

Forma: `051-SJ-EST-EX-010-PLB-TP-R01.pdf`, página 1, região V611/P28/P19/P10/P1, extração revisada em [V611_form_reviewed.json](../etapa1_1_integracao/V611_form_reviewed.json) e imagem [V611_full_form.png](../etapa1_1_integracao/V611_full_form.png). Origem física na face de P28 voltada a P19; sentido positivo P19 → P10 → P1. Coordenadas em metros, sem escala gráfica.

| Trecho físico | Apoios delimitadores | Intervalo físico / pesquisa de Vk (m) | b × h (cm) | Nível superior / inferior (cm) |
|---|---|---|---|---|
| V611-FORM-1 | P28–P19 | [0,000; 2,820] | 19 × 57 | 3808 / 3751 |
| V611-FORM-2 | P19–P10 | [3,520; 6,190] | 19 × 47 | 3808 / 3761 |
| V611-FORM-3 | P10–P1 | [6,890; 9,310] | 19 × 57 | 3808 / 3751 |

Os apoios P19 e P10 ocupam, respectivamente, [2,820; 3,520] e [6,190; 6,890] m. A mudança de altura está localizada nessas regiões, mas o ponto de transição não está cotado na leitura documental revisada. **Não há comprovação de uma mudança dentro de um mesmo vão livre da V611.** Não foi criado um `xt` no eixo dos pilares nem adotada seção média. Os intervalos dos apoios e das extremidades permanecem pendentes; offsets transversais ainda estão como informação existente, mas não extraída.

## 2. V611 — seleção real dos esforços

Foram utilizadas as séries características max/min preservadas de `VGESFS.LST`: Q mínimo nas linhas 609–611; Q máximo 617–619; M mínimo 613–615; M máximo 621–623. Originais em tf/tf.m convertidos pelo extrator existente para kN/kN.m. As séries e referências estão em [V611_tqs_raw.json](../silva_jardim_tipo/V611_tqs_raw.json) e no manifesto [entrada_v611.json](entrada_v611.json). Os LST originais não foram reabertos nesta execução; foram usados os extratos preservados.

A associação local/comum reutiliza duas âncoras por vão, com comprimentos VGESFS e excentricidades DEPEV de RELDTFPS conferidos contra os eixos da forma: P28 = −0,350; P19 = 3,170; P10 = 6,540; P1 = 9,660 m. Os valores e sinais das envoltórias não foram alterados. Nas faces, a interpolação linear existente utiliza amostras consecutivas, sem extrapolação.

| Trecho | Vk original governante (kN) | Valor absoluto de Vk (kN) | x de Vk (m) | Mk positivo / x (kN.m / m) | Mk negativo / x (kN.m / m) |
|---|---:|---:|---:|---|---|
| FORM-1 | −79,46647 | 79,46647 | 2,820 | +82,16344 / 0,000 | −95,39628 / 0,000 |
| FORM-2 | +105,19281 | 105,19281 | 3,520 | +68,72262 / 3,520 | −106,21966 / 6,190 |
| FORM-3 | −86,27361 | 86,27361 | 9,310 | +83,57970 / 9,310 | −99,21276 / 9,310 |

Os momentos desta tabela são os extremos **no intervalo físico**, ainda sem deslocamento. São resultados do modelo TQS, não uma confirmação independente de sua modelagem. Não há pesquisa ampliada real concluída nesta execução.

## 3. V611 — armaduras, altura útil e cálculos pendentes

Detalhamento preservado: [V611_detail.png](../silva_jardim_tipo/V611_detail.png) e [V611_detail.txt](../silva_jardim_tipo/V611_detail.txt), prancha de vigas 06302, página 1. A leitura identifica N1/N3/N5 = 3Ø16, N2/N4 = 3Ø20 e N6 = 1Ø16; a tabela conserva os comprimentos C. Os comprimentos totais das peças não comprovam seus extremos no eixo físico, considerando ganchos e apoios. Os intervalos longitudinais históricos continuam sem prova suficiente para associar uma composição resistente a cada região.

As indicações próximas às barras N2/N4/N6 fazem referência à segunda camada; é necessário consolidar sua associação longitudinal e o cabimento com o inventário completo. Nenhuma distribuição alternativa foi inventada. **Nenhuma dessas marcas foi usada em um cálculo resistente real da V611 nesta execução.**

O cobrimento de 2,5 cm vem de `/beam/cover/general = 0.025 m` no extrato TQS. Ø5 dos estribos N7/N8 vem do detalhamento. Foram registrados os intervalos transversais a partir das faces da forma e comprimentos impressos: N7/14 em [0; 2,82]; N7/10 em [3,52; 3,88]; N8/8 em [3,88; 5,43]; N7/10 em [5,43; 6,19]; N7/14 em [6,89; 9,31]. Os 36 + 155 + 76 cm apenas distribuem estribos no vão central; **não localizam a mudança de seção**.

Materiais documentais: fck = 40 MPa, aço CA-50A interpretado como fyk = 500 MPa pela regra já confirmada pelo engenheiro, γf = γc = 1,4. γs = 1,15 foi mantido como convenção explícita do escritório usada na V607, não como informação extraída do LST.

| Controle | Resultado real | Informação que impede a conclusão |
|---|---|---|
| Altura útil d | Não determinada | Extremos, composições e distribuição em camadas comprovados ao longo do trecho; necessários para obter o centroide resistente e selecionar d pelo critério existente |
| `a_l` de cada trecho | `INCONCLUSIVE / NOT_EXECUTED` | d e confirmação do escopo do método: estribos verticais, Vc = Vc0 e ausência de efeitos de força normal |
| Intervalo ampliado de momentos | Não determinado | `a_l` não calculado; posição das transições dentro dos apoios não comprovada |
| Flexão positiva/negativa e MRd | Não executadas | Composição física e cabimento insuficientemente comprovados; não há As/d resistentes liberados |
| Cortante resistente | Não executado | d não liberado, apesar de Vk e regiões de estribos terem sido selecionados |
| Suspensão na transição | Não executada | Ponto de transição, conexão/carga de suspensão aplicável e contextos adjacentes completos não comprovados |
| Região local da descontinuidade | Não verificada | Fora do método por trechos desta etapa; preservar análise local adicional |

O método público reutilizado é `Concretopy.calcular_al(concreto, b_cm, d_cm, vk_abs_kn, gamma_f, gamma_c)`, com argumentos nomeados. Retorna al em cm, forças em kN e os parâmetros/ramo de cálculo; seu escopo não inclui força normal nem substitui VRd2. Não houve chamada resistente com valores presumidos para liberar a V611. A guarda registra `al_scope` e `effective_depth` como pendências separadas.

Resultados reais e guardas: [resultado_v611.json](resultado_v611.json). As entradas preservam a origem de cada geometria, material, registro TQS e interpretação transversal.

Antes desta etapa, a V611 conservava a geometria e as séries registradas, mas não tinha a seleção operacional por seção com a separação entre Vk físico e momentos ampliados. Agora há três seleções físicas completas de Vk/Mk e bloqueios explícitos de al, d e resistência. Nenhum MRd real anterior foi substituído por resultado presumido. As pendências dos apoios e do tratamento local de descontinuidade continuam identificadas.

## 4. Demonstração sintética — duas alturas dentro do mesmo vão

**Dados de teste, não dados da V611.** Domínio comprovado da fixture [0; 4] m, transição x = 2 m, seções 19 × 57 e 19 × 47 cm, cobrimento 2,5 cm, estribos verticais de dois ramos Ø6,3/12 cm. N1 inferior e N2 superior, cada uma com 2Ø16 em primeira camada, As = 4,02124 cm² por face, ambas contínuas em [0; 4]. fck = 40 MPa, fyk = 500 MPa; γf/γc/γs = 1,4/1,4/1,15. O escopo sem efeitos de força normal é explícito na fixture.

| Seção | Intervalo físico e de Vk (m) | Valor absoluto de Vk / posição (kN / m) | d (cm) | al Concretopy (cm) | Intervalo ampliado de M (m) |
|---|---|---|---:|---:|---|
| G1, h = 57 | [0; 2] | 30 / 2,000 | 53,07 | 53,07000 | [0; 2,53070] |
| G2, h = 47 | [2; 4] | 200 / 2,100 | 43,07 | 31,10408 | [1,68896; 4] |

O pico de Vk = 200 kN fica à direita da transição: **não entra no al de G1**, mesmo que a pesquisa ampliada de momentos alcance x = 2,1 m. Para G1 o Concretopy recebeu Vk = 30, Vsd = 42 e Vc0 = 106,14149 kN; para G2 recebeu Vk = 200, Vsd = 280 e Vc0 = 86,14121 kN. Os retornos são respectivamente `vsd_le_vc0` e `vsd_gt_vc0`. A fórmula não foi reproduzida no fluxo.

| Seção / controle | Mk governante (kN.m) | x (m) | MSd (kN.m) | MRd (kN.m) | Utilização | Resultado |
|---|---:|---:|---:|---:|---:|---|
| G1 positiva, N1 | +40 | 2,100 | 56 | 89,47341 | 0,62588 | PASS de flexão |
| G1 negativa, N2 | −30 | 1,000 | 42 | 89,47341 | 0,46941 | PASS de flexão |
| G2 positiva, N1 | +40 | 2,100 | 56 | 71,98976 | 0,77789 | PASS de flexão |
| G2 negativa, N2 | −25 | 3,000 | 35 | 71,98976 | 0,48618 | PASS de flexão |

O momento de G1 em x = 2,1 m é pesquisado além da transição, mas a resistência utiliza **h = 57 cm de G1**. A geometria de G2 não substitui a seção analisada. A armadura utilizada permanece comprovadamente contínua na região necessária.

Como conferência de ordem de grandeza, para G1 o Concretopy retorna x = 4,73628 cm e braço z = 53,07 − 0,4x = 51,17549 cm. Com As = 4,02124 cm² e fyd = 434,78261 MPa, As·fyd·z/1000 = 89,47341 kN.m, consistente com o retorno resistente. Essa conferência não cria método resistente no software.

Cortante: G1 atende aos controles existentes; G2 **falha na armadura transversal**, com 5,19541 cm²/m existentes para 11,50260 cm²/m necessários. A compressão diagonal de G2 atende: Vsd = 280 kN < VRd2 = 530,27784 kN. O intervalo de pesquisa do cortante continua [2; 4], sem al. A demonstração detecta uma falha real dentro dos dados sintéticos; não produz aprovação da viga nem correção automática.

Entradas e retornos: [entrada_sintetico_dois_trechos.json](entrada_sintetico_dois_trechos.json) e [sintetico_dois_trechos.json](sintetico_dois_trechos.json).

## 5. Generalização sintética — três trechos

Mesmas armaduras e materiais da fixture anterior, com transições comprovadas em 1,5 e 3 m. O trecho central recebe influência das duas transições, uma única vez em cada extremidade.

| Seção | b × h (cm) | Intervalo físico / de Vk (m) | Valor absoluto de Vk (kN) | al (cm) | Pesquisa ampliada de M (m) | MRd por face (kN.m) | Cortante |
|---|---|---|---:|---:|---|---:|---|
| G1 | 19 × 57 | [0; 1,5] | 25 | 53,07000 | [0; 2,03070] | 89,47341 | PASS |
| G2 | 19 × 47 | [1,5; 3] | 200 | 31,10408 | [1,18896; 3,31104] | 71,98976 | FAIL de armadura |
| G3 | 19 × 67 | [3; 4] | 50 | 63,07000 | [2,36930; 4] | 106,95706 | PASS |

Os momentos positivos/negativos governantes são: G1 +26,14 em 2,03070 / −30 em 1; G2 +40 em 2,1 / −26,22082 em 1,18896; G3 +35,51167 em 2,36930 / −25 em 3, em kN.m/m. As seis verificações de flexão retornam PASS, sem eliminar a falha de cortante central.

Entradas e resultados: [entrada_sintetico_tres_trechos.json](entrada_sintetico_tres_trechos.json), [sintetico_tres_trechos.json](sintetico_tres_trechos.json).

## 6. Suspensão sintética na transição

Caso separado com reação característica total de 20 kN, aplicada em x = 2 m na transição 57 → 47 cm; o cortante das envoltórias foi fixado em +30/−20 kN para isolar esse controle. A distribuição utiliza a menor altura, **47 cm**, e ocupa [1,765; 2,235] m. A carga e os coeficientes permanecem os da fixture do método existente. Os subintervalos à esquerda/direita mantêm h = 57/47 cm nos cálculos de cortante.

Os valores e estados efetivamente retornados estão em [sintetico_suspensao.json](sintetico_suspensao.json), com entrada em [entrada_sintetico_suspensao.json](entrada_sintetico_suspensao.json). A aprovação da região local de descontinuidade permanece nula, mesmo que o controle de suspensão atenda. O teste adicional com espaçamento de 6 cm conserva o alerta já configurado no escritório e retorna `REQUIRES_ENGINEERING_REVIEW`, sem introduzir limite de armadura excessiva.

O controle foi efetivamente executado e retornou PASS. Pelo procedimento já implementado, a reação total de cálculo é 28 kN, a parcela considerada na suspensão é 21 kN e As,susp = 0,483 cm², distribuída à taxa de 1,02766 cm²/m. Os subintervalos [1,765; 2] e [2; 2,235] m retornaram PASS: taxa governante exigida de 2,66670 cm²/m e existente de 5,19541 cm²/m. O critério existente de combinação e armadura mínima foi preservado; esses valores não foram transferidos para a V611 real.

## 7. Regressão real V607

A mesma entrada histórica foi executada sem alterações: seção 14 × 37 cm, N1 = 2Ø10, As = 1,57080 cm², cobrimento 2,5 cm, estribo Ø5, d = 33,5 cm. Mk = 4,75622525 kN.m em x = 1,02 m; MSd = 6,65871535 kN.m. **MRd = 22,19306728728441 kN.m e utilização = 0,30003582937880474**, exatamente iguais aos valores anteriores. O controle positivo retorna PASS; isso não constitui aprovação integral da viga.

Fontes e demonstração original: [relatório V607](../verificacao_flexao_V607/relatorio.md). Reexecução desta etapa: [resultado_v607.json](resultado_v607.json). O arquivo histórico não foi sobrescrito.

## 8. Testes, preservação e alcance

A reprodução `python analises/trechos_secao_variavel/validar.py` executa as quatro suítes existentes, os casos reais e os casos sintéticos separados. A contagem e as saídas completas estão em [testes.json](testes.json); a comparação de hashes está em [preservacao.json](preservacao.json).

Foram descobertos 1.191 testes: 1.189 executados com sucesso e 2 ignorados pela indisponibilidade das fontes LST originais prevista na suíte do extrator. Por suíte: modelo físico 71, extrator 48 (2 ignorados), mapeamento 57 e verificações 1.015. Os hashes de 336 arquivos históricos/documentais e do Concretopy permaneceram iguais. A suíte inclui 48 testes do fluxo de pavimento e 31 de diagrama de momentos. Os testes direcionados passaram antes da inclusão da proteção adicional de unidade do domínio, depois coberta pela reexecução integral da suíte de verificações.

A intervenção ficou em `floor_review`, `input_preflight`, `moment_diagram`, `shear_diagram`, `shear_review` e `suspension_review`, com documentação operacional e testes nos módulos existentes. O motor resistente e sua fórmula de al permaneceram intactos. As exportações JSON omitem árvores documentais repetidas; cada arquivo indica as entradas integrais correspondentes, que conservam as referências de origem.

Os testes novos cobrem duas/três alturas, pico de momento além da transição, máximos positivo e negativo em posições distintas, al diferente entre trechos, pico de cortante próximo à transição, descontinuidade sem interpolação, interrupção longitudinal, suspensão na transição, posição de transição não comprovada, unidades de d, condições de aplicação de al, alerta existente de detalhamento e preservação dos dados de entrada. O teste de barra terminando em 2,05 m bloqueia seu uso na pesquisa necessária até 2,53070 m; não prolonga a barra nem busca outra marca sem prova.

O fluxo mantém uma exigência conservadora de continuidade de todas as marcas usadas até os limites da pesquisa ampliada. Isso pode exigir evidência adicional mesmo quando o pico isolado fica antes do término da barra. É uma pendência de prova, não uma nova prescrição normativa. Ancoragem, escalonamento e continuidade continuam sujeitos aos verificadores existentes.

Concretopy, métodos resistentes, históricos e PDFs foram preservados. Não foram geradas propostas de correção. Os critérios normativos citados nos resultados são retornos das interfaces existentes; o texto integral e a edição normativa não foram consultados nesta etapa. Nenhum requisito normativo novo foi introduzido.

Para concluir a V611: cotar as transições nos apoios; comprovar intervalos e composições longitudinais com camadas/cabimento; confirmar o escopo de al; documentar eventuais conexões e cargas de suspensão. As verificações locais de descontinuidade permanecem adicionais, fora desta implementação por trechos.
