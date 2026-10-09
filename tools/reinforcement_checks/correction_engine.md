# Motor inicial de proposição de correções

`correction_engine.propose_corrections` recebe diagnóstico consolidado, ocorrência FAIL de anchorage_length, barra/extremidade e geometria de apoio END orientada com fonte. Preserva cópias dos dados. A identificação do problema precede a geração, a verificação geométrica, a reverificação estrutural, a comparação e a aprovação do engenheiro.

Prioridade desta integração: avaliar primeiro a dobra da extremidade existente. A prioridade não transforma uma dobra documental em resistência comprovada. Se faltam parâmetros, gerar candidata preliminar INCONCLUSIVE, sem inventar trajetória/pino/espaço do pilar. Alternativas secundárias são explícitas e configuráveis: bitola, quantidade, redistribuição, prolongamento de outras barras e nova posição. Os geradores de support_correction são reutilizados; o novo motor não os substitui.

## Geometria e resistência

`bend_geometry` verifica apenas um envelope elementar de dobra ortogonal de 90 graus no plano longitudinal-vertical. Entradas em cm/mm, limites de pino e trechos retos e fontes são fornecidos pelo chamador; não há tabela normativa nova. O envelope usa raio externo e cobrimentos; comprovação da posição dentro do apoio e das interferências é independente e exige evidência. Não modela automaticamente pilar, confinamento, raio mínimo normativo, tolerâncias ou cruzamentos. Outros formatos devem permanecer inconclusivos nesta versão e não ser convertidos implicitamente ao envelope de 90 graus.

Comprimento do arco/desenvolvimento é informação geométrica, nunca comprimento resistente equivalente. Resistência curva é controle separado, refeito por verificador aplicável com parâmetros comprovados. A API atual de apoio com gancho_valido não certifica sozinha essas condições. Uma resposta favorável sem fonte permanece INCONCLUSIVE. Não utilizar alfa favorável por simples presença da dobra.

## Reverificação e contratos

Callback reverify recebe cópia da candidata e devolve checks identificados, status, fonte, geometry_checks, pendências e auditoria completa. Todos os affected_checks precisam aparecer: ausência gera INCONCLUSIVE; controles inesperados/duplicados são rejeitados. O adaptador real reutiliza evaluate_detail_candidate e Concretopy para camadas, flexão regional, d/x/z/al, demandas por pares e ancoragem. Mudanças longitudinais ainda exigem escalonamentos correspondentes. Falha comprovada prevalece sobre outras pendências.

Cada alternativa guarda ID determinístico, ocorrência original, viga/pavimento, marca/extremidade, intervenção, geometria original/proposta, dimensões alteradas, unidades, controles afetados, reverificação completa, pendências, viabilidade geométrica/estrutural e grau de intervenção. engineer_approval=PENDING_ENGINEERING_APPROVAL; ready_for_detailing=False. A aprovação/aplicação futura utiliza detailing_change_contracts; não há seleção ou edição gráfica neste módulo.

Comparação objetiva sem score: validade comprovada; aproveitamento existente; simplicidade; posições alteradas; retrabalho; consumo racional. Preferências comerciais são configuráveis, não requisitos normativos. Não minimizar aço isoladamente. selected_solution=null.

## Caso real

`analises/pranchas/validar_v536_correction_engine.py` lê os novos diagnósticos e grava somente V536_N2_correction_engine.json/relatório próprio. Preserva o cenário histórico de gancho autorizado. Para novas candidatas secundárias, chama APIs com gancho_valido=False; não reaproveita alfa=0,7 sem prova. A N2 já tem dobra documental de 58 cm: a candidata prioritária estuda/revisa a dobra existente, não afirma criar um novo ganho resistente.

A configuração original conserva lb_nec=24,203000349699796 cm e disponível=21,5 cm. A extremidade física interpretada fica na face externa x=-0,120 m. Faltam espaço transversal do pilar, pino, trajetória, trechos retos/curvos, interferências e resistência curva. São avaliados três prolongamentos N3 e doze redistribuições no espaço explicitado no fixture; nenhuma é automaticamente aprovada. Escalonamentos modificados permanecem pendentes, claramente separados dos controles já recalculados.

## Decisão de escopo mais recente — correção por área

A decisão do engenheiro subsequente ao primeiro ensaio estabelece o perfil `engineer_confirmed_support_correction_scope_exclusions_v1`: pino de dobramento, trajetória curva dentro do pilar e interferências com sua armadura não são executados neste módulo. São registrados como NOT_EXECUTED_BY_SCOPE_DECISION, com estado técnico null. Não são PASS, não bloqueiam a busca e não se confundem com controles inconclusivos por dados ausentes. A vista antes das exclusões permanece em auditoria. O perfil não pode excluir flexão, área corrigida ou escalonamento.

A rotina vigente para V536 é `validar_v536_correction_scope.py`; grava resultados próprios scope_updated, sem sobrescrever o primeiro ensaio conservador. A prioridade atual é corrigir a configuração existente pela As_corr retornada pelo Concretopy para lb_ef, mantendo o cenário de gancho previamente confirmado para o ensaio. Candidatas principais recalculam área corrigida e resistência regional, distribuição e continuidade. Não se somam trechos horizontais e verticais como lb resistente.

O contrato acrescenta verification_register: executed_passed, executed_failed, not_executed_by_scope e inconclusive_missing_data; engineering_review permanece separado. Uma falha não é ocultada por inconclusão; atendimento à área não comprova todas as condições construtivas. geometric_feasibility se refere somente aos controles mantidos no escopo. construction_conditions_fully_proven=False e aprovação pelo engenheiro permanece pendente.

Grampos são calculados separadamente pela infraestrutura existente: alvo As_adicional calculada pelo Concretopy, dois ramos e lb básico da própria bitola. Contribuição conjunta só pode ser creditada com modelo resistente de transferência e distribuição física compatível comprovados. Pino, trajetória curva e interferência do pilar também ficam no registro de escopo, sem PASS; ausência de posição/distribuição e modelo conjunto continua inconclusiva. Nesta versão não há crédito conjunto nem seleção final.

O adaptador ainda não possui o mapeamento regional completo das marcas propostas necessário para reverificar os escalonamentos alterados. Registra esse controle como INCONCLUSIVE, mesmo quando apoio, área corrigida, flexão regional, cabimento e continuidade atendem. Não equivale a reprovação e não decorre das três verificações excluídas.
