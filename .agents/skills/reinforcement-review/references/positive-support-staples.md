# Grampos complementares de ancoragem positiva

Consultar após [correção orientada pelo detalhamento](positive-support-correction.md), quando estudar uma solução complementar de ancoragem no apoio extremo END, LEFT/RIGHT relativo ao vão. O engenheiro pode solicitar comparação com grampo mesmo quando existe prolongamento válido; preservar essa alternativa e a hierarquia anterior. Não substituir N2/N3 nem aprovar globalmente a viga.

## Procedimento confirmado

1. Verificar configuração existente por pares independentes Mk/Vk, maior demanda As_apoio e lb_ef geométrico conforme [apoio positivo](positive-end-support.md). Recuperar As_efetiva, As_corr e As_adicional pela API real. Existente atendente → NENHUMA_CORRECAO, sem grampos.
2. Usar **As_grampo_necessaria=As_adicional** como demanda inicial do estudo, decisão `engineer_confirmed_support_staple_area_target_v1`. Isso não é detalhamento automático nem autoriza tratar uma composição mista como barras equivalentes.
3. Receber bitolas específicas de grampos: padrão usual **[6.3,8,10] mm**, configurável pelo chamador, independente da série da armadura principal. Peça em U com **dois ramos longitudinais resistentes paralelos** e um trecho conector na extremidade. As_por_grampo=2*As_barra Concretopy; quantidade=ceil(As_necessaria/As_por_grampo), sem hardcode de quantidade.
4. Determinar aderência dos ramos pela posição física segundo [aderência](bond-condition.md), ou cenário expressamente confirmado pelo engenheiro. Sem definição, registrar hipótese/pendência, nunca herdar classificação da armadura principal.
5. Para cada bitola, obter **lb básico da própria barra** no Concretopy. Aplicar decisão `engineer_confirmed_support_staple_length_v1`:

   **L_long=max(2*lb_grampo+lb_ef,60 cm)** para **cada ramo longitudinal**.

   Decisão `engineer_confirmed_support_staple_u_geometry_v1`: **L_transversal=b_viga−2*cobrimento−1 cm**. Registrar b, cobrimento e os dois comprimentos. Pode registrar **L_geometrico_nominal=2*L_long+L_transversal**, que não é comprimento de corte/C de fabricação: descontos/acréscimos das dobras ainda não estão formalizados.

   A descrição do engenheiro é U no plano vertical longitudinal; o trecho conector usa b conforme decisão explícita. Isso não define coordenadas nem posições dos ramos: não deduzir distribuição vertical pela largura.

   Comprimentos em cm. lb_ef é L_apoio−cobrimento, distinto da extremidade documental. Não usar lb_nec, reduzir por gancho ou somar al. A expressão é procedimento do engenheiro, **não prescrição atribuída à NBR**; neste workflow substitui a antiga referência 95φ/100φ.
Quantidade usual até **3 grampos**, decisão `engineer_confirmed_support_staple_usual_quantity_v1`. n≤3 → quantidade_usual=true; n>3 → quantidade_usual=false e requer_avaliacao_especial=true. Essa preferência de detalhamento não invalida estruturalmente a candidata, não é limite normativo e pode indicar conveniência de outra estratégia.
6. Distribuição vertical confirmada (`engineer_confirmed_support_staple_vertical_distribution_v1`): **de baixo para cima**, partindo da região positiva em direção ao topo, com **2,0 cm LIVRES** entre grampos consecutivos. Para n peças da mesma bitola: altura_ocupada=n*phi_cm+(n−1)*2 cm; entre eixos=2+phi_cm. Uma peça ocupa phi_cm, sem intervalo. Não duplicar a altura pelos dois ramos: a expressão confirmada representa as faces externas extremas da pilha.
   Registrar distribuicao_vertical_definida=true e interferencias_do_no_verificadas=false. Não emitir diagnóstico de espaçamento indefinido. Conferir altura ocupada no envelope entre cobrimentos como condição necessária; isso não localiza o primeiro grampo. Para cabimento posicionado, o chamador fornece janela vertical bottom_cm/top_cm (faces externas, referência face inferior) com provenance. Sem janela, registrar posição inicial/limite disponíveis pendentes, mantendo cálculo da altura e controle do envelope. Não derivar automaticamente a posição inicial do centro de N2/N3 nem aplicar espaçamento longitudinal como espaçamento vertical.
   Cabimento horizontal explícito pode reutilizar ferramenta existente; ambos os controles elementares não verificam interferências/dobras/nó. ready_for_detailing permanece false enquanto tais dependências não estiverem verificadas.
7. Comparar sem score: alteração do desenho, aço/área adicional, número de peças/barras prolongadas, comprimentos conhecidos e pendentes, cabimento, preservação/flexão positiva, ancoragem, dobra e interferências. Manter **selected_solution=null** até decisão explícita.

## Ferramenta, rastreabilidade e limites

Usar [support_staples](../../../../tools/reinforcement_checks/support_staples.md), que chama a infraestrutura atual. Concretopy mantém demanda/resistência/al/fbd/lb/cálculo inverso; assistant interpreta, gera e compara. Não copiar equações resistentes.

Registrar composição principal, chamada/pares governantes, alvo de área e fonte, bitola/área por ramo/peça, quantidade/ramos e sua decisão, excesso, condição de aderência/origem, lb próprio completo, lb_ef geométrico, dois termos/governante, cabimento/distribuição e pendências. Não apresentar comprimento nominal como C desenvolvido/corte da peça: forma conceitual definida não resolve os ajustes de dobra. Não afirmar ancoragem conjunta aprovada apenas porque As fornecida é suficiente e comprimento calculado: geometria e transferência de força ainda precisam ser verificadas.

Golden V536: N2=3Ø20 primeira camada e N3=3Ø20 escalonada preservadas; **dois ramos resistentes/peça e boa aderência** confirmados para este ensaio. [Auditoria atual da distribuição](../../../../.codex/analises/V536_V565_support_staples_vertical_distribution.md) compara grampos com prolongar 1Ø20 N3. Os valores são exemplos calculados, não regras por nome. V565 atende com existente e não recebe grampo.

Automatiza espaçamento livre vertical e altura ocupada; não automatiza posição inicial no nó, raio/pino, forma completa da dobra, confinamento, interferências com negativas, pacotes/tolerâncias, comprimento de fabricação ou aprovação global. As decisões desta referência atualizam somente a antiga indicação de procedimento futuro; não alteram as regras ou resultados anteriores.

A [auditoria exploratória anterior](../../../../.codex/analises/V536_V565_support_staples.md) usou uma série maior; ela é histórica e não define as bitolas usuais atuais. Os JSONs exploratórios foram preservados separadamente.

A restrição histórica ao apoio esquerdo pertence à primeira versão. Esta atualização generaliza a orientação geométrica END, conservando resultados reais V536/V565 à esquerda. Para INTERMEDIATE, consultar [ancoragem positiva em apoios](positive-support-anchorage.md); nenhum grampo é gerado automaticamente por esse ramo.
