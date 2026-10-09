# Grampos complementares no apoio positivo

`support_staples.py` envolve o workflow orientado pelo detalhamento sem alterar `support_correction.py`, `support_alternatives.py`, Concretopy ou seus goldens. Não substitui a composição principal, não seleciona solução e não gera desenho executivo.

## Interfaces e decisões

- `staple_length(lb_grampo_cm, lb_ef_cm)`: decisão `engineer_confirmed_support_staple_length_v1`, **L_long=max(2*lb_grampo+lb_ef,60 cm)** por ramo longitudinal; L_grampo_min_cm é alias mantido para compatibilidade. Usa lb básico da própria barra, sem alpha, al ou 95φ/100φ. Preserva ambos os termos se empatam.
- `quantity_for_area(required_cm2,unit_bar_cm2,contributing_legs=None)`: inteiro superior pela área de cada peça. Sem número de ramos explícito, somente quantidade equivalente de barras; quantidade de peças/área fornecida ficam null. Zero demanda retorna zero peças.
- `evaluate_staple(context,required_area_cm2,lb_ef_cm,diameter_mm,api,...)`: área pela `Barra` Concretopy, aderência física por `classify_bond` ou cenário explícito com origem, `calcular_ancoragem` com áreas unitárias iguais, e uso exclusivo de `lb_cm`. Preserva resultado completo/API/hashes. `contributing_legs` exige provenance.
- `staple_workflow(...)`: reexecuta a configuração existente e a hierarquia de correção. Recupera `As_adicional` como demanda inicial complementar (`engineer_confirmed_support_staple_area_target_v1`), nunca reimplementa cálculo inverso. Existente ancorada não gera grampos. Prolongamento adequado conserva prioridade; `study_with_valid_extension=True` permite comparação expressamente solicitada sem substituir o próximo passo anterior.

Bitolas e cenários de aderência são configuráveis. `bond_scenario` aceita centro físico, horizontal=True/forma deslizante=False, ou booleano com status confirmed/hypothesis e provenance. Hipótese não se torna decisão confirmada. Não inferir aderência da N2 ou do nome grampo.

## Geometria e resultado

Geometria nominal explícita de U: dois ramos longitudinais paralelos e um conector. `staple_geometry(L_long_cm,b_cm,cover_cm)` calcula L_transversal=b−2*cobrimento−1 cm e L_geometrico_nominal=2*L_long+L_transversal, regra do engenheiro, não NBR. Valores inválidos bloqueiam somente a geometria dependente; quantidade/área/lb já calculados são conservados. Descrição de plano vertical longitudinal e dimensão do conector pela largura não determinam coordenadas; elas continuam não verificadas. `fabrication_cut_length_cm=None`: nominal não é corte/C desenvolvido.

`DEFAULT_STAPLE_DIAMETERS_MM=(6.3,8,10)` é a série usual independente para grampos; `staple_workflow` a usa quando o chamador omite diameters_mm. Lista customizada substitui o padrão, sem herdar bitolas principais. `usual_quantity(n,usual_max=3)` registra quantidade_usual/requer_avaliacao_especial; >3 é preferência de detalhamento, não diagnóstico de falha estrutural. O avaliador de U exige dois ramos quando quantidade resolvida; legacy contributing_legs=None conserva diagnóstico inconclusivo.

`vertical_distribution(n,phi,section=None,window=None)` implementa regra do engenheiro: orientação vertical, de baixo para cima, 2 cm LIVRES; eixos=2+phi_cm, altura=n*phi_cm+(n−1)*2. Campos distinguem distribuicao_vertical_definida de distribuicao_vertical_verificada, cabimento_vertical_envelope, cabimento_vertical e interferencias_do_no_verificadas. Quantidade acima3 mantém alerta especial, sem falha estrutural automática.

`section` permite comparar altura ocupada com h−2*cobrimento: limite geométrico necessário entre faces de cobrimento, não posicionamento nem espaço comprovadamente livre de armaduras. `window={bottom_cm,top_cm,provenance}` informa as faces externas disponíveis, desde a face inferior. Deve estar no envelope se a seção é conhecida. Calcula primeira/última coordenada de centro e face superior da pilha; cabimento True/False nessa janela, sem epsilon. Sem janela, cabimento posicionado=null, diagnóstico específico de posição inicial/limite pendentes; não falta regra de espaçamento. Janela inválida/sem fonte não aprova o posicionamento. `evaluate_staple` recebe vertical_window ou context.staple_vertical_window. O workflow transmite este contexto sem inferir a janela.

`distribution` continua sendo somente ocupação horizontal explícita principal+grampos e reutiliza transverse_fit. Cabimento vertical False rejeita cabimento geral; passar apenas um dos controles não aprova o nó. distribution_verified refere-se ao conjunto geométrico completo e continua False; ready_for_detailing=False e interferencias_do_no_verificadas=False. Pendentes interferências com positivos/negativos/estribos, raios/pinos, tolerâncias e demais elementos. Não emitir distribuicao_geometrica_nao_verificada pela antiga ausência de espaçamento.

`complete_calculation` refere-se somente a quantidade/área/lb/comprimento com hipóteses resolvidas. **Não significa ancoragem conjunta ou detalhamento aprovado**. Não somar área de outra bitola à N2 em uma chamada agregada para declarar que a composição mista ancora: `combined_anchorage_passes=None` enquanto não existir representação/verificação da geometria completa. Um problema abaixo de lb_min não é resolvido automaticamente adicionando área.

Saída: configuração principal preservada, cálculo anterior completo, As necessária/fornecida/excesso, bitola/quantidade/ramos, aderência, lb próprio, lb_ef, expressão e mínimo/termo governante, cabimento/distribuição, diagnósticos/fontes e comparação com prolongamentos. `selected_solution=None` sempre. Comprimento mínimo do procedimento não é automaticamente comprimento C de fabricação ou massa de aço; dobras/desenvolvimento de cada peça ainda exigem geometria.

## Golden e reprodução

V536: dois ramos resistentes/peça e boa aderência confirmados pelo engenheiro em 06/10/2026. Série usual [6.3,8,10] configurável, não catálogo normativo ou certificação da dobra/nó. A série anterior mais ampla pertence ao estudo exploratório histórico. V565: ancoragem existente atende, não gera grampos. Mantidos todos os prolongamentos adequados, inclusive 1Ø20 N3.

```powershell
python -B analises/pranchas/validar_v536_v565_grampos.py
python -B -m unittest discover -s tools/reinforcement_checks -p test_support_staples.py
```

[Procedimento da Skill](../../.agents/skills/reinforcement-review/references/positive-support-staples.md), [auditoria atual](../../.codex/analises/V536_V565_support_staples_vertical_distribution.md). Não regravar goldens anteriores.
