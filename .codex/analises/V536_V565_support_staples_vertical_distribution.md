# V536/V565 — distribuição vertical final dos grampos

06/10/2026. Implementada decisão engineer_confirmed_support_staple_vertical_distribution_v1: múltiplos grampos empilhados **de baixo para cima**, da região positiva ao topo, com **2 cm LIVRES**. Distância de eixos=2+phi_cm; altura ocupada=n*phi_cm+(n−1)*2 cm, entre faces externas extremas dos ramos. Não multiplicar altura por dois ramos, não usar2 cm entre eixos. Procedimento do engenheiro, não atribuído à NBR.

Mantidos dois ramos resistentes, área e lb próprios via Concretopy, L_long=max(2lb+lb_ef,60), conector=b−2c−1, série própria6,3/8/10 e preferência usual≤3. Acima3 exige avaliação especial, não falha resistente automática. N2/N3 e prolongamento1Ø20 continuam preservados; selected_solution=null. V565 recalculada sem grampos/NENHUMA_CORRECAO.

## Campos e cabimento elementar

Distribuicao_vertical_definida=true. Interferencias_do_no_verificadas=false e ready_for_detailing=false. A antiga pendência por espaçamento indefinido foi removida das candidatas correntes.

A ferramenta calcula altura ocupada e verifica limite necessário no envelope entre faces de cobrimento (h−2c). Não equivale a altura efetivamente livre do nó. Para afirmar cabimento posicionado, exige janela vertical explícita com fonte: bottom_cm/top_cm, ambas faces externas disponíveis, medidas desde a face inferior. Conferem-se intervalo válido/envelope, primeira/última coordenada de eixo, face superior da pilha e altura disponível. Não se inventa centro inicial ou distância à N2/N3. Janela ausente mantém somente posicionamento/cabimento localizado pendentes, não a regra de distribuição.

| Ø mm | Peças | Livre cm | Eixos cm | Altura ocupada cm | Cabe no envelope necessário | Cabe na posição real | Nó verificado |
|---|---:|---:|---:|---:|---|---|---|
| 6.3 | 2 | 2.00 | 2.63 | 3.26 | True | null | False |
| 8 | 2 | 2.00 | 2.80 | 3.60 | True | null | False |
| 10 | 1 | 2.00 | 3.00 | 1.00 | True | null | False |

V536: envelope necessário=72−2*2,5=67 cm. Alturas calculadas estão abaixo desse limite. Isso não autoriza escolher automaticamente a altura inicial da pilha ou afirmar ausência de interferências. Janela física inicial/topo ainda não consta dos dados auditados. Caso o engenheiro a forneça, o controle posicionado está implementado e testado. Para uma peça, não existe vão livre entre peças; a propriedade de espaçamento informa a regra para peças consecutivas e altura ocupada=phi_cm.

Interferência detalhada com positivas, negativas, estribos, raios/pinos, tolerâncias, demais elementos do nó, ancoragem conjunta e C de fabricação continuam fora do controle elementar. Cabimento vertical False rejeita o cabimento geral; True na janela não aprova o nó.

## Arquivos e testes

Alterados support_staples.py, test_support_staples.py, resultados V536/V565 e referências correntes SKILL.md/positive-support-staples.md/support_staples.md/README.md. Relatórios históricos não reescritos. Criados este relatório e registro de validação específico.

66 testes do módulo:49 anteriores compatíveis e17 novos. Cobrem2Ø6,3/Ø8/Ø10,3 peças,uma peça,altura e diferença livre/eixos,ordem ascendente,janela que cabe/não cabe/igualdade,limite necessário distinto de posicionamento,janela sem fonte/fora do cobrimento,mais3 especial,ausência do diagnóstico obsoleto e integração sem aprovação do nó. **361 testes engineering-assistant e405 testes Concretopy aprovados**; quick_validate e git diff --check aprovados. 70 arquivos protegidos inalterados, incluindo Concretopy e goldens anteriores de apoio/escalonamento/correção principal. Registro: V536_V565_support_staples_vertical_validation.json.

[Contrato](../../tools/reinforcement_checks/support_staples.md), [Skill](../../.agents/skills/reinforcement-review/references/positive-support-staples.md), [V536](../../analises/pranchas/V536_support_staples.json), [V565](../../analises/pranchas/V565_support_staples.json). A comparação corrente mantém as três candidatas de grampo e os prolongamentos válidos, sem score ou escolha automática.
