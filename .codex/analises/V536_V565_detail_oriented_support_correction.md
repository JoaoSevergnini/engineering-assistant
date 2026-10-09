# V536/V565 — correção positiva no apoio orientada pelo detalhamento

06/10/2026. **O resultado computacional da V536 é PROLONGAR_ARMADURA_EXISTENTE:** levar 1, 2 ou 3 barras Ø20 da N3 até o apoio, preservando a segunda camada, passou nas verificações modeladas. Uma barra é a menor alteração entre as três candidatas, mas nenhuma solução foi escolhida automaticamente. **V565 retorna NENHUMA_CORRECAO**, mantendo a configuração existente.

A preferência prática do engenheiro por grampos permanece registrada separadamente. Ela não foi utilizada para forçar o resultado, esconder prolongamentos válidos ou inventar impedimentos geométricos. Nenhum grampo foi implementado ou dimensionado. As candidatas não são detalhamento pronto: dobra e interferências do nó permanecem pendentes de revisão.

## 1. Fontes, arquitetura e primitivas

Leitura prévia: AGENTS.md; Skill reinforcement-review e referências de vigas/prancha, escalonamento, apoio e aderência; support_alternatives.py/contrato/testes; goldens/relatórios de apoio V536/V565, busca genérica e escalonamento N3; Concretopy atual para flexão, posição de camadas, apoio, al e ancoragem. Não foi consultado novamente o texto integral da norma ou atribuída à NBR a hierarquia/preferência de correção.

Novo [support_correction.py](../../tools/reinforcement_checks/support_correction.py) envolve o avaliador local já validado, sem modificar `support_alternatives.py`. Demandas A/B/C, resistência, d/x/z, al e ancoragem permanecem no Concretopy. [Contrato](../../tools/reinforcement_checks/support_correction.md) e [workflow da Skill](../../.agents/skills/reinforcement-review/references/positive-support-correction.md).

A [auditoria anterior à implementação](support_correction_geometry_primitives_audit.md) identificou as primitivas de espaçamento/capacidade por camada. A regra do engenheiro a_livre_min=max(2 cm,phi_cm) é compatível com a primitiva Concretopy para a série: o termo de agregado=1,92 cm do parâmetro padrão de compatibilidade 16 mm não governa. Não se adotou 16 mm como agregado do projeto; o TQS auditado indica 15 mm, também não governante. Dependência de submódulos não congelados foi identificada e protegida por testes. Nenhuma regra foi duplicada no assistant ou modificada no Concretopy.

Centros existentes são preservados: Ø20, d1=68 e d2=64 cm. Novas bitolas de redistribuição reutilizam a API pública de posição de camadas. Cabimento é explicitado por camada, sem bitola média/equivalente.

## 2. Situação existente e contexto geométrico

Detalhamento agrupado V536=V565, quantidades por viga, seção 19×72 cm, apoio longitudinal esquerdo 24 cm. N2 3Ø20 primeira camada chega ao apoio; N3 3Ø20 segunda camada começa x=0,540 m, 42 cm dentro do vão livre. Nas regiões internas ambas participam da resistência positiva. N2 tem início documental −21 cm da face interna (x comum −0,090 m); N3 é reta no desenho original.

Comprimento da verificação **lb_ef=24−2,5=21,5 cm**, independente da posição documental original. A proposta de prolongamento usa como alvo longitudinal o início da N2 já auditado, sem alterar a fonte; a regra geométrica de lb_ef é mantida. O novo comprimento desenvolvido e a dobra da parcela N3 prolongada não foram dimensionados.

Materiais C40/CA50; γf=γc=1,4, γs=1,15; cobrimento-paramétrico 2,5 cm, estribo Ø5. Mesmos esforços/pares da [auditoria corrigida](V536_V565_left_support_anchorage_check.md): S1 no eixo esquerdo, P1 Mk positivo com |Vk mínimo|, P2 Mk=0 com Vk máximo em módulo. Origem dos esforços e hipóteses permanecem nos novos JSONs. O cenário de gancho=True/α=0,7 é mantido para estudar a terminação proposta; não é verificação automática da dobra de uma N3 originalmente reta.

| Viga existente | As efetiva (cm²) | As apoio (cm²) | lb_nec (cm) | lb_ef (cm) | Margem (cm) | Área atende | Ancoragem atende | Cabimento | Flexão regional |
|---|---:|---:|---:|---:|---:|---|---|---|---|
| V536 / N2 3Ø20 | 9.424778 | 5.917168 | 24.203000 | 21.500000 | -2.703000 | True | False | True | True |
| V565 / N2 3Ø20 | 9.424778 | 5.200058 | 21.269804 | 21.500000 | 0.230196 | True | True | True | True |

## 3. Prolongamentos N3 na V536

A marca é individualizada sem perda de provenance: parcela prolongada e parcela restante conservam a origem N3. Ambas preservam Ø20 e centro d=64 cm. A parcela restante mantém início original; a prolongada passa a começar no alvo de apoio. Nas regiões onde N3 existia originalmente, a soma de barras permanece 3. Nenhuma barra N2/N3 original é retirada ou reposicionada.

| Composição no apoio | d (cm) | x (cm) | z (cm) | As efetiva | As apoio | lb básico | lb_min | lb_nec | lb_ef | Margem | As_corr | As adicional | Recomendável para análise |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| N2 + 1 barra(s) N3 | 67.000000 | 14.800881 | 59.599560 | 12.566371 | 5.917168 | 55.071689 | 20.000000 | 20.000000 | 21.500000 | 1.500000 | 10.609670 | 0.000000 | True |
| N2 + 2 barra(s) N3 | 66.400000 | 18.501101 | 57.149450 | 15.707963 | 5.917168 | 55.071689 | 20.000000 | 20.000000 | 21.500000 | 1.500000 | 10.609670 | 0.000000 | True |
| N2 + 3 barra(s) N3 | 66.000000 | 22.201321 | 54.899339 | 18.849556 | 5.917168 | 55.071689 | 20.000000 | 20.000000 | 21.500000 | 1.500000 | 10.609670 | 0.000000 | True |

As em cm². Duas chamadas independentes por candidata; C governa ambas, com empates entre pares preservados. Os objetos completos A/B/C, al_base/al final/Vc0/Vsd/Fsd, aderência por centro físico e cálculos de ancoragem ficam no JSON. Não foram copiados da configuração existente: d/x/z e al mudam com a composição efetiva do apoio. A composição do vão no pico permanece N2+N3, com d=66 cm, pois o prolongamento não altera essa região.

## 4. Cabimento transversal

Largura interna b−2(c+φ_estribo)=**19−2(2,5+0,5)=13 cm**. Para Ø20, a_livre mínimo/adotado=**2 cm**. Três barras exigem 10 cm, duas 6 cm e uma 2 cm. Para camada de uma barra não há intervalo entre barras; o mínimo por barra é registrado, sem inventar uma folga medida entre barras inexistentes.

| Candidata | Camada | Barras | Largura disponível (cm) | Largura necessária (cm) | Folgas mínimas/adotadas (cm) | Folga uniforme possível (cm) | Cabe |
|---|---:|---|---:|---:|---|---:|---|
| existing | 1 | 3Ø20 | 13.000000 | 10.000000 | [2.0, 2.0] | 3.500000 | True |
| extend_N3_1 | 1 | 3Ø20 | 13.000000 | 10.000000 | [2.0, 2.0] | 3.500000 | True |
| extend_N3_1 | 2 | 1Ø20 | 13.000000 | 2.000000 | [] | - | True |
| extend_N3_2 | 1 | 3Ø20 | 13.000000 | 10.000000 | [2.0, 2.0] | 3.500000 | True |
| extend_N3_2 | 2 | 2Ø20 | 13.000000 | 6.000000 | [2.0] | 9.000000 | True |
| extend_N3_3 | 1 | 3Ø20 | 13.000000 | 10.000000 | [2.0, 2.0] | 3.500000 | True |
| extend_N3_3 | 2 | 3Ø20 | 13.000000 | 10.000000 | [2.0, 2.0] | 3.500000 | True |

O restante de N3 ainda dentro do vão também foi incluído na composição/cabimento regional. Não se verifica somente o apoio com menos barras: a região interna conserva as três barras da segunda camada, que também cabem por esse critério.

A busca genérica histórica não era uma recomendação de prancha. Exemplos de uma camada anteriormente válidos na ancoragem são rejeitados pelo novo critério simples: **4Ø20 exige 14 cm; 5Ø16 exige 16 cm; 6Ø12,5 exige 17,5 cm**, acima dos 13 cm internos. Isso explica o problema de distribuir aquelas alternativas em uma camada; não invalida automaticamente prolongar a segunda camada existente.

## 5. Compatibilidade com flexão positiva

Reutilizados `flexure_regions.compose_layers/decompose_regions` e `MomentDiagram.moment_at_x`, com API Concretopy para cada região. Verificados todos os vértices da representação linear presentes na região e valores nos limites das mudanças de composição, inclusive quando não coincidirem com uma seção TQS. Não se cria discretização extra, extrapolação ou nova equação de interpolação/resistência.

Domínio amostrado 0..3,276 m; inclui pontos nos apoios. A seção resistente uniforme e os parâmetros de camadas são hipótese explícita do ensaio anterior, reaproveitada: não se presume distribuição de estribos verificada dentro dos pilares. O pico S13 não é declarado máximo estrutural exato. A compatibilidade refere-se a esse modelo/diagrama adotado.

| Candidata | Região (m) | Marcas propostas | Msk regional (kN.m) | Mk equivalente (kN.m) | Flexão atende | Cabimento regional |
|---|---|---|---:|---:|---|---|
| existing | 0.000..0.540 | N2 | 34.372308 | 186.036148 | True | True |
| existing | 0.540..3.276 | N2,N3 | 317.745267 | 334.371638 | True | True |
| extend_N3_1 | 0.000..0.540 | N2,N3__extended_1 | 34.372308 | 238.369407 | True | True |
| extend_N3_1 | 0.540..3.276 | N2,N3__extended_1,N3__remaining_2 | 317.745267 | 334.371638 | True | True |
| extend_N3_2 | 0.000..0.540 | N2,N3__extended_2 | 34.372308 | 287.814570 | True | True |
| extend_N3_2 | 0.540..3.276 | N2,N3__extended_2,N3__remaining_1 | 317.745267 | 334.371638 | True | True |
| extend_N3_3 | 0.000..3.276 | N2,N3__extended_3 | 317.745267 | 334.371638 | True | True |

Além da demanda, a prova de conservação de contagens/bitolas/centros/intervalos e a comparação de capacidades originais/propostas confirmam que nenhum prolongamento reduziu a capacidade positiva existente. Respostas e comparações por região são rastreáveis no JSON. Os goldens originais de escalonamento N3 permanecem intactos. Prolongar parte de N3 altera o evento de corte dessa parcela; não se afirma que seu golden antigo seja um novo detalhamento automaticamente aprovado. As barras não prolongadas conservam os dados originais do corte, sem redimensioná-lo nesta etapa.

## 6. Redistribuições

**Nenhuma redistribuição foi gerada no golden V536**, porque os prolongamentos adequados satisfazem a etapa anterior da hierarquia. Esse desvio está registrado em redistribution_reason; não se buscou uma alteração mais extensa para substituir desnecessariamente a armadura existente.

A infraestrutura de redistribuição foi implementada/testada para um perfil simples de duas marcas/camadas, preservando intervalos: primeira menor chegando ao apoio, segunda maior mantendo perfil escalonado. Série explícita [10;12,5;16;20;25], limite padrão 2 passos configurável, quantidades explícitas [2;3] neste fixture. Ao redistribuir, reconstroem-se centros por Concretopy, d do vão no pico, todas as regiões e todos os cálculos de apoio/ancoragem. Mistura dentro de uma mesma camada resistente não é habilitada por geometria explícita de bitolas.

Os testes cobrem passos 1/2 e preferência configurável acima, composição menor/maior que falha no vão apesar da avaliação local, e configuração que atende à flexão/ancoragem mas não cabe transversalmente. Sem solução simples/coerente, o próximo passo retornado é avaliar armadura complementar. Não foram geradas combinações artificiais ilimitadas nem dimensionados grampos.

## 7. Próximo passo e decisão do engenheiro

| Viga | Próximo passo calculado | Alternativas de correção | Solução final selecionada |
|---|---|---|---|
| V536 | PROLONGAR_ARMADURA_EXISTENTE | extend_N3_1, extend_N3_2, extend_N3_3 | null |
| V565 | NENHUMA_CORRECAO | Nenhuma alteração | null |

**Decisão do engenheiro, separada:** foi informada preferência prática por grampos para V536, pois as alternativas genéricas não se distribuíam adequadamente em uma camada. **Resultado do modelo atual:** o prolongamento de parte da segunda camada existente cabe e atende às verificações realizadas. Isso não foi suprimido. Antes da decisão final, revisar se a terminação/dobra e o nó real permitem essa proposta; se não permitirem, registrar a restrição real e reavaliar a hierarquia.

`technically_valid=true` e `recomendavel_como_correcao=true` significam candidata coerente **para análise do engenheiro no cenário modelado**, não autorização de alteração da prancha. `ready_for_detailing=false` e `selected_solution=null` permanecem. Uma barra N3 é a menor intervenção de quantidade entre os prolongamentos, não uma escolha final silenciosa.

Para V565, existente com área/ancoragem/cabimento/flexão atendentes → nenhuma candidata gerada. Mesmo nessa situação, não se certifica aprovação global ou dobra executada.

## 8. Provenance, testes e preservação

[Script real](../../analises/pranchas/validar_v536_v565_correcao_apoio.py), [JSON V536](../../analises/pranchas/V536_support_correction.json), [JSON V565](../../analises/pranchas/V565_support_correction.json). Marcas/quantidades/camadas/centros/intervalos/fontes originais, mudanças propostas, pares, respostas Concretopy, cabimento, regiões/diagrama e comparação de capacidades são preservados. Novo C desenvolvido não é inventado; campos documentais de parcelas prolongadas são identificados como origem histórica, separados de proposal_geometry/changes.

**295 testes do engineering-assistant passaram:** 39 extrator_lst + 30 beam_model + 34 beam_mapping + 192 reinforcement_checks. Inclui os 262 anteriores e **33 testes novos**, com controles reais, contratos, folgas para as cinco bitolas, cabimento, prolongamentos 1/2/3, camadas físicas/d/x/z/al recalculados, conservação de capacidade, todos os limites/vértices regionais, redistribuição, ausência de prova, prioridade/nenhuma correção, fallback complementar e limites de detalhamento.

**405 testes do Concretopy passaram**, sem cache e sem bytecode (`Python 3.11 -B`, pytest `-p no:cacheprovider` com dependências temporárias do workspace). `quick_validate` da Skill passou. `git diff --check` passou. Hashes antes/depois de **67 arquivos protegidos** comprovaram: Concretopy inteiro protegido sem alteração; support_alternatives.py intacto; goldens anteriores de apoio/escalonamento e dados documentais intactos. Resultados desta camada foram escritos separadamente.

## 9. Arquivos criados/alterados e limites

Criados: `tools/reinforcement_checks/support_correction.py`, `support_correction.md`, `test_support_correction.py`; `references/positive-support-correction.md`; `analises/pranchas/validar_v536_v565_correcao_apoio.py`; V536/V565_support_correction.json; este relatório; auditoria prévia de primitivas; V536_V565_support_correction_validation.json.

Alterados: `reinforcement-review/SKILL.md`, `references/positive-end-support.md` e `tools/reinforcement_checks/README.md`, para encaminhar a correção à hierarquia nova sem eliminar a busca exploratória.

Não implementa grampos, comprimentos/bitolas/espaçamentos de grampos, tabela prática ou dimensionamento de dobra, pacotes, tolerâncias, interferências detalhadas com negativas, cruzamentos complexos no nó, apoio direito, negativos, suspensão ou aprovação global. O cabimento simples usa os parâmetros de seção adotados; confirmação de cobrimento/estribo efetivo e geometria completa no apoio permanece parte da revisão física. A continuação proposta não produz automaticamente uma nova prancha executiva.
