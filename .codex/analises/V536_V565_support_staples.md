# V536/V565 — armadura complementar por grampos

06/10/2026. Estudo solicitado pelo engenheiro, sem escolha automática. **V536 necessita inicialmente 1.184892 cm² complementares no procedimento atual; V565 não recebe grampos.** O prolongamento de 1Ø20 N3 continua válido nas verificações anteriores e permanece na comparação. Não se modificaram N2/N3, esforços ou goldens precedentes.

## 1. Leitura, arquitetura e decisões

Lidos AGENTS.md; Skill reinforcement-review e referências de vigas, desenho, escalonamento, apoio positivo, correção e aderência; support_alternatives/support_correction, contratos e testes; auditorias/goldens V536/V565 de apoio, alternativas, escalonamento e correção orientada pelo detalhamento; API pública local Concretopy e documentação de flexão/apoio/al/ancoragem.

Novo [support_staples.py](../../tools/reinforcement_checks/support_staples.py) é uma camada separada de orquestração. Executa novamente a avaliação existente por APIs reais, preserva a hierarquia anterior e permite comparação explicitamente solicitada mesmo existindo prolongamento adequado. Não altera Concretopy, support_alternatives.py, support_correction.py, bar_scaling.py ou os resultados físicos anteriores.

Decisões confirmadas pelo engenheiro nesta tarefa:

- As_grampo_necessaria=As_adicional calculada pelo Concretopy.
- Cada grampo possui **dois ramos resistentes**: As unitária por peça=2×área da barra Concretopy. A quantidade é arredondada para inteiro superior.
- **Boa aderência** para os ramos longitudinais dos grampos deste ensaio. É cenário confirmado, não posição geométrica automaticamente inspecionada.
- **L_grampo_min=max(2×lb_grampo+lb_ef,60 cm)**, com lb básico da própria bitola. Não se usa lb_nec, redução por gancho ou soma de al. A regra é procedimento do engenheiro, não atribuição à NBR; substitui 95φ/100φ neste workflow.

Auditoria textual de referências e ferramentas não encontrou regra explícita de distância vertical livre entre grampos, nem implementação vigente de 95φ/100φ a remover. Nenhum espaçamento vertical foi inventado. A documentação anterior que dizia 'grampos futuros' continua correta para os módulos anteriores e agora remete à camada separada; relatórios históricos não foram reescritos.

## 2. Por que N2 atual não ancora na V536

Seção 19×72 cm; apoio esquerdo 24 cm; cobrimento 2,5 cm; C40/CA50; N2=3Ø20 primeira camada, d=68 cm, chegando ao apoio; N3=3Ø20 segunda camada, d=64 cm, escalonada conforme original. Mantidos pares independentes S1: momento positivo e módulo da envoltória mínima de cortante; momento zero e máximo módulo de cortante. A maior demanda entre chamadas é adotada; não se afirma concomitância das envoltórias. Cenário original de gancho válido/alpha=0,7 mantido.

| Grandeza V536/N2 existente | Resultado |
|---|---:|
| As efetiva (cm²) | 9.424777961 |
| As apoio (cm²) | 5.917167968 |
| lb básico N2 (cm) | 55.071689104 |
| lb_min N2 (cm) | 20.000000000 |
| lb_nec N2 (cm) | 24.203000350 |
| lb_ef geométrico (cm) | 21.500000000 |
| Margem (cm) | -2.703000350 |
| As_corr (cm²) | 10.609669967 |
| As adicional / alvo dos grampos (cm²) | 1.184892006 |

Área principal suficiente, mas 21,5 cm disponíveis são inferiores a 24,203000 cm necessários: ancoragem original=False. Projeção documental conhecida da N2=21 cm; **lb_ef=24−2,5=21,5 cm** é uma informação geométrica diferente. Não se deslocou a extremidade desenhada da N2 nem se substituiu esse comprimento por seção TQS.

## 3. Alternativas de grampos — solução A

Todas mantêm N2/N3 e fornecem área complementar suficiente no cenário de dois ramos/boa aderência. Série [10,12,5,16,20,25] mm explicitamente exploratória/configurável; não certifica que toda bitola é adequada à dobra/nó real. As necessária=1.184892006 cm² e lb_ef=21,5 cm são comuns.

| Ø mm | Peças | As por ramo cm² | As fornecida cm² | Excesso cm² | lb próprio cm | 2lb+lb_ef cm | L mínimo cm | Governante | Cabimento / distribuição |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| 10 | 1 | 0.785398 | 1.570796 | 0.385904 | 27.535845 | 76.571689 | 76.571689 | ANCORAGEM | null / False |
| 12.5 | 1 | 1.227185 | 2.454369 | 1.269477 | 34.419806 | 90.339611 | 90.339611 | ANCORAGEM | null / False |
| 16 | 1 | 2.010619 | 4.021239 | 2.836347 | 44.057351 | 109.614703 | 109.614703 | ANCORAGEM | null / False |
| 20 | 1 | 3.141593 | 6.283185 | 5.098293 | 55.071689 | 131.643378 | 131.643378 | ANCORAGEM | null / False |
| 25 | 1 | 4.908739 | 9.817477 | 8.632585 | 68.839611 | 159.179223 | 159.179223 | ANCORAGEM | null / False |

Em cada bitola, área unitária e lb foram obtidos do Concretopy. A chamada de ancoragem usa áreas unitárias iguais e registra o retorno integral; o comprimento do grampo usa somente o lb básico retornado. Não se reutiliza o lb da N2, não se copia a equação resistente e não se arredondam valores antes das decisões.

`complete_calculation=true` refere-se à quantidade/área/lb/comprimento. **Todas têm distribuicao_geometrica_nao_verificada e ready_for_detailing=false.** Cabimento=null significa falta de posicionamento, não reprovação por falta de largura. Nenhuma candidata recebeu automaticamente o espaçamento das barras positivas como espaçamento vertical dos grampos.

A rotina admite ocupação horizontal explícita e reutiliza transverse_fit; mesmo com esse controle, distribuição vertical, forma/raio/pino de dobra, confinamento, interferências com N1/estribos e transferência da força complementar continuam dependentes do detalhe real. Não se soma a área dos grampos de outra bitola à N2 em ancoragem agregada para afirmar aprovação conjunta: `combined_anchorage_passes=null` até verificações compatíveis.

## 4. Prolongamento de 1Ø20 N3 — solução B

Recalculado, não escondido: N2 3Ø20 primeira camada + 1Ø20 da N3 segunda camada chegam ao apoio; as outras duas barras N3 conservam o início original. Todos os centros/bitolas e armadura originalmente necessária no vão são preservados. Intervalo prolongado começa x=−0,090 m em vez de +0,540 m, **acréscimo horizontal=63 cm** para uma barra. N3 originalmente reta tem C=334 cm; nova forma/dobra e C desenvolvido ainda não foram dimensionados.

As efetiva=12,566371 cm²; d=67 cm; x=14,800881 cm; z=59,599560 cm; As apoio=5,917168 cm²; lb_nec=20 cm; lb_ef=21,5 cm; margem=1,5 cm; As adicional=0. Ancoragem=True, cabimento=True no modelo simples de camadas, flexão positiva=True em todas as regiões amostradas. Não basta pico: o workflow reexecuta composição/regiões/diagrama e API Concretopy. Nova terminação segue cenário de gancho válido para cálculo; sua geometria exige revisão. As alternativas de prolongar 2 e 3 barras também continuam disponíveis no JSON, sem escolha silenciosa.

## 5. Comparação objetiva sem score

| Critério | A: manter N2/N3 + grampo | B: prolongar 1Ø20 N3 |
|---|---|---|
| Alteração do desenho | Nova marca complementar; principais preservadas | Uma barra N3 ganha prolongamento/terminação; duas permanecem originais |
| Quantidade | 1 peça de dois ramos em cada bitola ensaiada | 1 barra existente prolongada |
| Área adicional local | 1,570796..9,817477 cm² conforme bitola | 3,141593 cm² chegam adicionalmente ao apoio; não é nova área na região interna |
| Comprimento | Mínimo calculado 76,571689..159,179223 cm | 63 cm a mais de projeção horizontal; não inclui nova dobra |
| Aço adicional total/massa | Pendente: forma e C de fabricação desconhecidos | Pendente: desenvolvimento da nova dobra desconhecido |
| Cabimento | null: distribuição ainda não definida | True no controle simples por camada |
| Flexão positiva principal | Preservada: mesma N2/N3; verificação regional original True | Recalculada regionalmente True, sem reduzir armadura/capacidade original |
| Ancoragem | Alvo de área e comprimento calculados; ancoragem conjunta/geometria pendentes | True pelo cenário/API e controles modelados |
| Dobra | Necessária; forma/raio/pino não definidos | Nova terminação/gancho ainda deve ser detalhada |
| Interferências | Nó/negativas/estribos não conferidos | Nó/negativas/estribos não conferidos |
| Solução pronta | Não | Não: revisão da dobra/nó ainda necessária |

Comparar área na seção e aço total são avaliações diferentes: não se inferiu massa pela área adicional isolada. O comprimento mínimo do procedimento não foi apresentado como C desenvolvido ou como comprimento por ramo sem definição da forma. A preferência prática anterior do engenheiro por grampos permanece separada do resultado computacional, que conserva PROLONGAR_ARMADURA_EXISTENTE como próximo passo da hierarquia. Este estudo de grampos foi solicitado expressamente; **selected_solution=null**.

## 6. Controle V565

A avaliação real retorna As apoio=5.200058005 cm², lb_nec=21.269804473 cm e lb_ef=21,5 cm, ancoragem=True, As adicional=0. Portanto **NENHUMA_CORRECAO**, zero grampos, zero prolongamentos/redistribuições e nenhuma escolha automática. Não foi hardcoded o atendimento pelo nome da viga.

## 7. Provenance e artefatos

[Fixture reexecutável](../../analises/pranchas/validar_v536_v565_grampos.py), [V536 JSON](../../analises/pranchas/V536_support_staples.json), [V565 JSON](../../analises/pranchas/V565_support_staples.json), [contrato](../../tools/reinforcement_checks/support_staples.md), [referência da Skill](../../.agents/skills/reinforcement-review/references/positive-support-staples.md).

JSON conserva contexto/materiais/pares/fontes, composição documental, cálculo anterior integral e prolongamentos, API/hashes Concretopy, área adicional original, decisões de ramos/aderência, área por barra/peça, quantidade/excesso, lb próprio completo, comprimento/regra/governantes, comparação e pendências. Não cria números resistentes órfãos nem altera relatórios anteriores.

## 8. Validação e arquivos

31 testes novos de contratos/orquestração e integrações reais: fórmula do procedimento, piso60/ancoragem/empate, lb próprio por bitola, básico distinto de mínimo, dois ramos/quantidade/inteiro superior/excesso, zero demanda, ramos e geometria desconhecidos, cenários e aderência física/conflito, cabimento horizontal/falha/ocupação inconsistente, busca configurável/hierarquia, V536 golden/V565 sem grampo, comparação N3, imutabilidade e recusa da API.

Suíte completa: **326 testes engineering-assistant aprovados** (39 extrator, 30 beam_model, 34 beam_mapping, 223 reinforcement_checks), incluindo os 31 novos; **405 testes Concretopy aprovados**; quick_validate: **Skill is valid!**; **git diff --check aprovado**. Hashes: **70 arquivos protegidos inalterados**, incluindo Concretopy, implementações anteriores e goldens anteriores. Registro: V536_V565_support_staples_validation.json. Nenhuma fórmula do Concretopy foi replicada nos testes.

Criados: support_staples.py, test_support_staples.py, support_staples.md, positive-support-staples.md, validar_v536_v565_grampos.py, dois JSONs específicos, este relatório e registro de validação. Alterados somente os roteamentos documentais SKILL.md, positive-end-support.md, positive-support-correction.md e README.md das ferramentas. Concretopy e implementações anteriores preservados.

## 9. Limitações

Não aprova globalmente a viga ou altera prancha. Não inventa distribuição vertical, não automatiza raio/pino/confinamento, interferências, pacotes, tolerâncias, fabricação/massa, apoio direito, negativas/suspensão/cisalhamento ou regime de barras fora do contexto auditado. Boa aderência e dois ramos são decisões explícitas deste ensaio; generalização exige entradas do chamador. Área/quantidade/comprimento atendidos não bastam para declarar detalhamento ou ancoragem conjunta completos.
