# V536/V565 — revisão da geometria usual dos grampos

06/10/2026. Novas decisões incorporadas ao procedimento corrente, sem alteração do Concretopy ou dos resultados anteriores de apoio/escalonamento/correção principal. O [relatório anterior](V536_V565_support_staples.md) permanece histórico; sua série maior era exploratória. JSONs daquela execução foram arquivados como V536/V565_support_staples_exploratory_historical.json antes da atualização autorizada dos goldens de grampos.

## Leitura e alterações

Lidos AGENTS.md, reinforcement-review/SKILL.md, positive-support-staples.md, support_staples.py/testes/contrato, relatório anterior, JSONs V536/V565 e implementação pública de ancoragem do Concretopy. Mantidas demanda pelas chamadas de apoio existentes, materiais/aderência, lb próprio pela API real, dois ramos, lb_ef geométrico, comparação com N3 e selected_solution=null.

Atualizados support_staples.py/test_support_staples.py, fixture validar_v536_v565_grampos.py, dois goldens correntes e documentação SKILL.md/positive-support-staples.md/support_staples.md/README.md. Criados dois JSONs históricos, esta auditoria e validação específica da revisão. Implementações support_alternatives.py, support_correction.py e bar_scaling.py continuam intactas.

## Procedimento do engenheiro

Peça em **U**, dois ramos longitudinais paralelos resistentes e um conector na extremidade. As_por_grampo=2*As_barra obtida do Concretopy; quantidade=ceil(As_necessaria/As_por_grampo). Série usual própria padrão **[6.3,8,10] mm**, configurável pelo chamador e independente da série principal. Os testes anteriores com Ø12,5/Ø20 permanecem como entradas customizadas, sem torná-las usuais.

Para **cada ramo longitudinal**, L_long=max(2*lb_grampo+lb_ef,60 cm). Mesmo lb básico e expressão anteriores, sem lb_nec/alpha/al. `L_grampo_min_cm` permanece como alias compatível de L_long, não comprimento total da peça.

Conector: **L_transversal=b−2*cobrimento−1 cm**. Comprimento geométrico nominal opcional=2*L_long+L_transversal. Não é comprimento de corte/C de fabricação/desenvolvido definitivo: ajustes das dobras não estão formalizados. `fabrication_cut_length_cm=null`.

Descrição fornecida pelo engenheiro: U no plano vertical longitudinal. A expressão do conector usa a largura b. Essas informações estão preservadas separadamente; não bastam para deduzir coordenadas no plano ou posições verticais. Nenhuma representação espacial, dobra ou distribuição foi inferida silenciosamente.

Quantidade usual máxima=3, preferência de detalhamento, **não limite resistente nem regra normativa**. n≤3 → quantidade_usual=true/requer_avaliacao_especial=false; n>3 → inverso e alerta de avaliação cuidadosa/outras estratégias, sem declarar falha estrutural somente pela quantidade. Os identificadores de regras e fontes ficam no resultado.

## V536 — configuração original e alvo

N2=3Ø20 primeira camada chegando ao apoio, N3=3Ø20 segunda camada escalonada. As_efetiva=9.424777961 cm²; As_apoio=5.917167968 cm²; As_corr=10.609669967 cm²; As_adicional/As_grampo_necessaria=1.184892006 cm². Valores recuperados pela API real, não hardcoded no módulo.

N2 possui lb_nec=24.203000350 cm contra lb_ef=21.500 cm, portanto ancoragem original=False. lb_ef=24−2,5=21,5 cm, independente da projeção documental original21 cm. Demanda, paresS1, gancho confirmado/alpha0,7, seção19×72 e C40/CA50 mantidos.

Boa aderência e dois ramos resistentes por peça são as decisões já confirmadas. N2/N3 permanecem como configuração principal; grampos não são inseridos como substitutos automáticos das barras existentes.

| Ø mm | Grampos | Área por ramo cm² | Área por grampo cm² | Área total cm² | Excesso cm² | Quantidade usual | Avaliação especial |
|---|---:|---:|---:|---:|---:|---|---|
| 6.3 | 2 | 0.311724531 | 0.623449062 | 1.246898124 | 0.062006118 | True | False |
| 8 | 2 | 0.502654825 | 1.005309649 | 2.010619298 | 0.825727293 | True | False |
| 10 | 1 | 0.785398163 | 1.570796327 | 1.570796327 | 0.385904321 | True | False |

Área necessária comum=1.184892006 cm². Todas fornecem área suficiente, e todas estão dentro da quantidade usual. A quantidade veio do inteiro superior sobre as áreas reais.

| Ø mm | lb básico cm | lb_ef cm | L_long por ramo cm | Governante | b cm | Cobrimento cm | L_transversal cm | L geométrico nominal cm |
|---|---:|---:|---:|---|---:|---:|---:|---:|
| 6.3 | 17.347582068 | 21.500 | 60.000000000 | MINIMO_60_CM | 19.000 | 2.500 | 13.000 | 133.000000000 |
| 8 | 22.028675642 | 21.500 | 65.557351283 | ANCORAGEM | 19.000 | 2.500 | 13.000 | 144.114702566 |
| 10 | 27.535844552 | 21.500 | 76.571689104 | ANCORAGEM | 19.000 | 2.500 | 13.000 | 166.143378208 |

Na Ø6,3, piso60 cm governa; nas Ø8/Ø10, 2lb+lb_ef governa. O conector é calculado em todas: **19−2*2,5−1=13 cm**. Não foi adotado13 como constante na produção. Comprimentos nominais não são corte: nenhuma candidata tem C final.

## Distribuição e comparação para decisão

**distribuicao_vertical_verificada=false, distribution_verified=false, cabimento=null e ready_for_detailing=false** em todas as candidatas reais. Forma conceitual conhecida não resolve como múltiplas peças são posicionadas na altura. Não se aplica o espaçamento de barras positivas como regra vertical dos grampos. Ancoragem conjunta/transferência da força, raio/pino, dobras e interferências com N1/estribos continuam pendentes.

| Alternativa | Área adicional que chega ao apoio cm² | Alteração | Comprimento conhecido | Cabimento | Flexão positiva | Ancoragem |
|---|---:|---|---|---|---|---|
| 2 grampos Ø6,3 | 1.246898 | Nova marca; N2/N3 preservadas | 60 cm por ramo; conector13 cm; nominal133 cm/peça | Pendente | Principal preservada/verificada | Área/comprimentos calculados; conjunto pendente |
| 2 grampos Ø8 | 2.010619 | Nova marca; N2/N3 preservadas | 65.557351 cm por ramo; conector13 cm | Pendente | Principal preservada/verificada | Área/comprimentos calculados; conjunto pendente |
| 1 grampo Ø10 | 1.570796 | Nova marca; N2/N3 preservadas | 76.571689 cm por ramo; conector13 cm | Pendente | Principal preservada/verificada | Área/comprimentos calculados; conjunto pendente |
| Prolongar 1Ø20 N3 | 3.141593 | Uma barra existente ganha prolongamento; demais preservadas | 63.000 cm adicionais horizontais, dobra nova pendente | True nos controles atuais | True regionalmente | True pelo cenário e APIs atuais |

Prolongar 1Ø20 N3 permanece visível e válido nas verificações modeladas, sem supressão para coincidir com a preferência prática por grampos. Aumento de área no apoio não equivale a consumo de aço total: massa/C de fabricação continuam pendentes. Não criar score ou selecionar automaticamente. **selected_solution=null**. O próximo passo da hierarquia anterior permanece PROLONGAR_ARMADURA_EXISTENTE; este estudo comparativo foi solicitado expressamente.

## Controle V565

Reexecução pela API real: ancoragem existente=True, As_grampo_necessaria=0, **NENHUMA_CORRECAO**, nenhuma candidata de grampo/prolongamento/redistribuição. Não houve hardcode de aprovação por nome.

## Testes e validação

49 testes do módulo, preservando os31 anteriores compatíveis e acrescentando18: Ø6,3/Ø8/Ø10, área de dois ramos, preferência de três/acima3 sem rejeição resistente, conector calculado, padrão/customização, comprimento longitudinal anterior, nominal distinto de corte, U/posição pendente, geometria inválida parcial, dois ramos obrigatórios, provenance, golden atualizado/controle/comparação. **344 testes engineering-assistant aprovados** (39 extrator,30 beam_model,34 beam_mapping,241 reinforcement_checks); **405 testes Concretopy aprovados**; quick_validate válido; **git diff --check aprovado**. **70 arquivos protegidos inalterados**, incluindo Concretopy e implementações/goldens anteriores de apoio/escalonamento/correção principal. Registro: V536_V565_support_staples_geometry_validation.json.

## Artefatos e limites

[Implementação](../../tools/reinforcement_checks/support_staples.py), [contrato](../../tools/reinforcement_checks/support_staples.md), [Skill](../../.agents/skills/reinforcement-review/references/positive-support-staples.md), [fixture](../../analises/pranchas/validar_v536_v565_grampos.py), [V536 atual](../../analises/pranchas/V536_support_staples.json), [V565 atual](../../analises/pranchas/V565_support_staples.json), [V536 histórico](../../analises/pranchas/V536_support_staples_exploratory_historical.json), [V565 histórico](../../analises/pranchas/V565_support_staples_exploratory_historical.json).

Não modifica armaduras principais ou prancha, não aprova globalmente a viga, não dimensiona automaticamente distribuição vertical, ajustes de dobra, interferências, confinamento, fabricação ou apoio direito. Preferências de bitolas/quantidade e dimensões nominais são procedimentos confirmados do engenheiro e não prescrições atribuídas à NBR. Concretopy permanece exclusivamente responsável por cálculos resistentes, materiais/área e ancoragem básica.
