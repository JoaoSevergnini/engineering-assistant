# V536 — golden integrado da armadura positiva

06/10/2026. Golden de regressão do workflow positivo atualmente implementado. **No modelo amostrado, a resistência à flexão e o escalonamento N3 atendem. A N2 original falha na ancoragem do apoio esquerdo. Existem prolongamentos válidos nos controles modelados e grampos calculados para comparação, mas nenhuma correção foi escolhida.** Aprovação completa da armadura positiva permanece inconclusiva: apoio direito, cobertura final do diagrama, geometria nos apoios e detalhamento do nó ainda possuem pendências.

O caso é um golden para preservar tanto aprovações quanto falhas reais; não foi ajustado para fazer a viga passar. Ele reúne as etapas disponíveis sem implementar regra estrutural nova ou alterar Concretopy. Não verifica negativos/cisalhamento/suspensão/armadura mínima ou aprova globalmente a viga.

## 1. Fontes e reprodução

Detalhamento agrupado V536=V565 já auditado em RMP-EST-EX-1349-VIG-R00 - Copia.PDF, primeira página; esforços específicos V536 na pasta TQS DIFERENCIADO/VIGAS do projeto24-155-COLLINE-RESIDENCIAL-R60. A identificação agrupada não faz as vigas terem os mesmos esforços. O fixture usa os JSONs auditados, hashes do mapping/raw e API pública local Concretopy; não reinterpreta o desenho automaticamente.

[Fixture reexecutável](../../analises/pranchas/validar_v536_positivo_completo.py), [golden JSON integrado](../../analises/pranchas/V536_positive_reinforcement_complete_golden.json), [testes](../../tools/reinforcement_checks/test_v536_positive_complete.py).

```powershell
python -B analises/pranchas/validar_v536_positivo_completo.py
python -B -m unittest discover -s tools/reinforcement_checks -p test_v536_positive_complete.py
```

O fixture escreve somente seu golden integrado. Todas as fontes e goldens individuais anteriores são somente leitura. Resistência/material/áreas/d/x/z/al/lb/demandas/cálculo inverso permanecem no Concretopy. Não foram copiadas equações resistentes nem recalculada interpolação fora da infraestrutura existente.

## 2. Geometria e armadura existente

Seção19×72 cm, C40/CA50, cobrimento TQS2,5 cm e estribo documentalØ5 no vão livre. Apoio esquerdo P11A24 cm; direito P7A120 cm; vão livre294 cm. Coordenada comum a partir do eixo esquerdo: faces internas0,120 e3,060 m; eixo direito3,660 m. Diagrama característico de13 seções amostra0..3,276 m; sem extrapolação/suavização/discretização artificial.

| Marca | Quantidade | Camada inferior | d cm | Intervalo comum m | Comprimento documental |
|---|---|---:|---:|---|---|
| N2 | 3Ø20 | 1 | 68 | −0,090..3,880 | C455 cm; projeção397 cm; dobra esquerda58 cm |
| N3 | 3Ø20 | 2 | 64 | 0,540..3,880 | Reta C334 cm |

N1 negativa e N5 pele não são somadas à composição positiva. N2/N3 possuem centros documentados/consolidados, não bitola equivalente. O centroide de N2+N3 é66 cm. O término/interrupção N3 à esquerda permanece em0,540 m; não é deslocado para seção TQS ou face de apoio.

## 3. Momento resistente por regiões — modelo amostrado

Reutilizado check_longitudinal: todas as regiões de composição, consultas nos limites e vértices do diagrama linear, capacidade pela API Concretopy. Contexto uniforme de seção/camadas do ensaio anterior expressamente preservado; não é comprovação automática dos estribos dentro dos apoios.

| Região m | Composição | d cm | MRd kN.m | Mk equivalente kN.m | Msk regional kN.m | Utilização | Atende |
|---|---|---:|---:|---:|---:|---:|---|
| 0.000..0.540 | N2 | 68.000 | 260.450607 | 186.036148 | 34.372308 | 0.184761 | True |
| 0.540..3.276 | N2+N3 | 66.000 | 468.120293 | 334.371638 | 317.745267 | 0.950276 | True |

Comparação caracteriza Msk com Mk equivalente, não com MRd diretamente. O maior momento amostrado é317.745266650 kN.m emS13,x3,276 m, dentro do apoio direito. É máximo da representação piecewise-linear adotada, não máximo estrutural exato. A presença desse ponto não comprova ancoragem ou geometria resistente do nó direito.

### Verificação documental estrita preservada

Executado também check_positive_flexure com as regiões transversais efetivamente documentadas. Não se extrapola a distribuição de estribos para os pilares.

| Região | Intervalo m | Estado | Pendência |
|---|---|---|---|
| R1 | 0.000..0.120 | unresolved | unresolved_transverse_geometry |
| R2 | 0.120..0.540 | checked | Sem bloqueio |
| R3 | 0.540..3.060 | checked | Sem bloqueio |
| R4 | 3.060..3.660 | unresolved | unresolved_transverse_geometry |

Duas regiões do vão livre são verificadas e atendem. As regiões internas aos apoios permanecem não resolvidas por geometria transversal. Isso não é sobrescrito pelo modelo uniforme usado na auditoria anterior. A última amostra3,276 m precede o eixo direito3,660 m: não se fabrica demanda para o trecho remanescente de0,384 m.

## 4. Escalonamento N3 à esquerda

Antes do evento, no sentido do corte: N2+N3; depois: N2. Capacidade remanescente N2: MRd=260.450607394 kN.m e Mk equivalente=186.036148139 kN.m. x_nec=1.885409281 m, selecionado no ramo correspondente ao corte esquerdo. Referência do início da queda no sentido do corte: piecewise_linear_positive_peak,S13,x3,276 m.

Máximo módulo de Vk de todo o vão físico amostrado: **125.152467300 kN**, S2,x0,273 m, envoltória máxima/sinal positivo. Essa seleção é independente dos paresS1 do apoio. d_for_al=66.000 cm, centroide resistente imediatamente antes do corte. Concretopy: al=66.000 cm. N3:y8 cm da face inferior, boa aderência; lb básico=55.071689104 cm;10φ=20 cm.

| Condição | Referência | Disponível cm | Exigido cm | Atende |
|---|---|---:|---:|---|
| A: al+10φ | x_nec | 134.540928139 | 86.000000000 | True |
| B: al+lb básico | Pico piecewise-linear | 273.600000000 | 121.071689104 | True |

**scaling_passes=true**, mantendo A/B independentes. Não substitui ancoragem em apoio.

## 5. Apoio esquerdo e ancoragem N2

S1 no eixo esquerdo, conforme procedimento do engenheiro. P1: Mk positivo com módulo da envoltória mínima Vk; P2: Mk=0 com máximo módulo Vk. Chamadas independentes; não se afirma concomitância. Vão e seus d/demanda permanecem entradas próprias.

| Chamada | Mk kN.m | Vk módulo kN | As necessária cm² | Condição governante |
|---|---:|---:|---:|---|
| positive_moment_min_shear | 22.820075 | 33.538743 | 5.917167968 | C |
| zero_moment_max_abs_shear | 0.000000 | 123.603017 | 5.917167968 | C |

Maior demanda=5.917167968 cm², com empates preservados. N2 fornece9.424777961 cm²; d=68.000000,x=11.100661,z=62.449670 cm. Gancho=True/alpha0,7 no cenário já confirmado, sem inspeção automática da geometria; boa aderência pelo centro físico da primeira camada.

lb_ef geométrico=24−2,5=**21.500 cm**, distinto da projeção documental21 cm. lb básico=55.071689104 cm; lb_min=20.000000 cm; lb_nec=24.203000350 cm; margem=-2.703000350 cm. **Área atende, ancoragem não atende.** As_corr=10.609669967 cm² e As_adicional=1.184892006 cm² vêm do cálculo inverso Concretopy; não são automaticamente um grampo detalhado.

## 6. Alternativas de ancoragem

### Busca genérica preservada

Recalculadas **100 alternativas**, mesma série/configurações do ensaio anterior. **32** atendem localmente sem área adicional. O golden aplica ainda o controle transversal reutilizado, sem alterar o avaliador genérico: **16** dessas candidatas locais falham no cabimento simples. Nenhuma alternativa genérica prova sozinha coerência longitudinal ou está pronta para prancha.

Exemplos históricos locais válidos mas não distribuíveis em uma camada:4Ø20 requer14 cm;5Ø16 requer16 cm;6Ø12,5 requer17,5 cm, contra13 cm internos. Não confundir resultado matemático local com recomendação de correção.

### Prolongar a N3 existente antes de redistribuir

Preservadas bitolas/centros e quantidade total da região interna. Testadas1,2,3 barras N3 até o início documental da N2, com reconstrução de camadas e recálculo completo d/x/z/al/A/B/C/ancoragem/flexão/cabimento. Demanda de apoio continua5.917167968 cm², calculada novamente, não copiada por conveniência.

| Composição no apoio | d cm | x cm | z cm | As efetiva cm² | lb_nec cm | Margem cm | As adicional cm² | Cabimento | Flexão regional |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| N2+1Ø20 N3 | 67.000000 | 14.800881 | 59.599560 | 12.566371 | 20.000000 | 1.500000 | 0.000000 | True | True |
| N2+2Ø20 N3 | 66.400000 | 18.501101 | 57.149450 | 15.707963 | 20.000000 | 1.500000 | 0.000000 | True | True |
| N2+3Ø20 N3 | 66.000000 | 22.201321 | 54.899339 | 18.849556 | 20.000000 | 1.500000 | 0.000000 | True | True |

Ancoragem atende em todas pelo cenário/APIs atuais. Para1Ø20 N3, acréscimo horizontal63 cm, de0,540 a−0,090 m; nova dobra/C de fabricação ainda precisam ser definidos. As duas barras N3 não prolongadas conservam o intervalo original. Como existem prolongamentos adequados, o workflow não gera redistribuições desnecessárias. Resultado calculado=PROLONGAR_ARMADURA_EXISTENTE; nenhuma candidata selecionada automaticamente.

## 7. Grampos complementares

Estudo comparativo explicitamente solicitado mesmo existindo prolongamento válido. N2/N3 principais são preservadas. As necessária inicial=As_adicional original=1.184892006 cm². Boa aderência e dois ramos resistentes por peça confirmados. U com L_long=max(2lb próprio+lb_ef,60 cm) **por ramo**, conector=b−2c−1=13 cm; nominal2L_long+13 não é C de fabricação. Série própria6,3/8/10, independente da principal.

| Ø mm | Peças | As ramo cm² | As peça cm² | As total cm² | Excesso cm² | lb básico cm | L_long cm | Governante | Conector cm | Altura ocupada cm |
|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|
| 6.3 | 2 | 0.311725 | 0.623449 | 1.246898 | 0.062006 | 17.347582 | 60.000000 | MINIMO_60_CM | 13.000 | 3.260 |
| 8 | 2 | 0.502655 | 1.005310 | 2.010619 | 0.825727 | 22.028676 | 65.557351 | ANCORAGEM | 13.000 | 3.600 |
| 10 | 1 | 0.785398 | 1.570796 | 1.570796 | 0.385904 | 27.535845 | 76.571689 | ANCORAGEM | 13.000 | 1.000 |

Todas fornecem área suficiente e quantidade usual≤3. Distribuição **vertical,de baixo para cima,2 cm LIVRES**; distância entre eixos=2+phi_cm; altura ocupada=n*phi_cm+(n−1)*2 cm. Distribuicao_vertical_definida=true, interferencias_do_no_verificadas=false. Alturas cabem no envelope necessário entre cobrimentos67 cm, mas posição inicial/faixa real ainda não foram documentadas. Cabimento posicionado=null; ready_for_detailing=false. Não foram inventadas posições ou distância inicial às barras principais.

Ancoragem conjunta/transferência de força, raio/pino, dobras e interferências ainda pendentes. Não somar áreas de bitolas distintas numa ancoragem agregada para declarar correção aprovada. Acima3 peças exige avaliação especial, sem rejeição estrutural somente pela quantidade.

## 8. Comparação para decisão do engenheiro

| Alternativa | Mudança na prancha | Área adicional local cm² | Comprimento conhecido | Situação |
|---|---|---:|---|---|
| Prolongar1Ø20 N3 | Uma barra existente ganha prolongamento/terminação | 3,141593 no apoio; mantém área interna | +63 cm horizontais; dobra nova pendente | Atende ancoragem/flexão/cabimento modelados |
| 2 gramposØ6,3 | Nova marca complementar; N2/N3 preservadas | 1,246898 | 60 cm por ramo;conector13 | Área/comprimento/distribuição definidos;nó pendente |
| 2 gramposØ8 | Nova marca complementar;N2/N3 preservadas | 2,010619 | 65,557351 cm por ramo;conector13 | Área/comprimento/distribuição definidos;nó pendente |
| 1 grampoØ10 | Nova marca complementar;N2/N3 preservadas | 1,570796 | 76,571689 cm por ramo;conector13 | Área/comprimento/distribuição definidos;nó pendente |

Sem score ou seleção automática. A preferência prática anterior do engenheiro por grampos é registrada separadamente do prolongamento computacionalmente válido; nenhuma alternativa foi escondida. Comparar área local não determina massa/consumo total: C de fabricação/dobras permanecem pendentes. **selected_solution=null**.

## 9. Apoio direito e conclusão completa

Apoio P7A120 cm, eixo3,660 m; positivoN2/N3 chega documentalmente a3,880 m. A rotina atual não verifica armadura/ancoragem de apoio direito: **NAO_IMPLEMENTADO**, não 'atende'. Não se espelham automaticamente os pares ou o cenário de gancho do apoio esquerdo. O modelo estrito também mantém geometria resistente interna ao apoio não resolvida, e não extrapola o diagrama até seu eixo.

Portanto: **falha conhecida na configuração original à esquerda**, alternativas disponíveis e pendências remanescentes. `verified_original_checks_pass=false`; `complete_positive_approval=false`; `positive_reinforcement_approved=null`. Isso distingue falha verificada de incompletude e evita declarar a viga aprovada. Este é o golden integrado do momento positivo **no escopo atualmente implementado**, com pendências explícitas como parte do contrato de regressão.

## 10. Provenance e validação

JSON mantém respostas integrais de cada etapa, composições/intervalos originais, diagrama/amostras, materiais/contextos, chamadas Concretopy e hashes, pares/empates, candidatos e filtros, regras do engenheiro e fontes. Checa hashes de mapping/raw antes de calcular. Não cria equações resistentes no assistant ou muda decisões anteriores.

12 testes novos com API real: contrato integrado persistido, capacidades/escala/crossing/A/B contra goldens, ancoragem corrigida, busca genérica e rejeições de cabimento, recálculo/preservação de prolongamentos, grampos correntes, falta de cobertura/apoio direito, hipótese distinta de geometria documental, ausência de seleção automática e imutabilidade das fontes. **373 testes engineering-assistant aprovados** (39 extrator,30 beam_model,34 beam_mapping,270 reinforcement_checks), incluindo12 novos testes integrados; **405 testes Concretopy aprovados**; quick_validate e git diff --check aprovados. 70 arquivos protegidos inalterados; Concretopy, implementações anteriores e goldens individuais preservados. Registro: V536_positive_reinforcement_complete_validation.json.
