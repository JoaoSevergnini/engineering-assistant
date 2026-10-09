# Relações entre armaduras negativas

`negative_reinforcement_relations.py` é a camada semântica específica entre apoios consecutivos. Contratos operacionais e decisões confirmadas: [referência da Skill](../../.agents/skills/reinforcement-review/references/negative-reinforcement-relations.md).

Entradas: duas peças negativas com identidade/fonte/intervalo/camadas; apoios físicos consecutivos (ocorrências, faces e provenance); associação estrutural documentada; contexto e diagrama existente. O diagrama assinado e a associação às faces permitem inferir encontro ou transição; a geometria sozinha não prova o papel.

Saídas independentes: classificação, momento entre apoios, interseção física, controle de comprimento (30 cm ou 2lb), capacidade do grupo completo de menor bitola e demanda de todo o overlap, comparação local de massa e disposição localizada/vibrador. Continua sem solução selecionada ou otimização aplicada.

`interval_demand` consulta extremos e todos os vértices existentes. `compare_detailing_mass` exige limites necessários rastreáveis e parâmetros confirmados de porta-estribo; reutiliza seu verificador. `steel_mass.py` exige densidade explicitamente informada, área Concretopy e comprimento em metros. `local_overlap_disposition` preserva o resultado global e registra separadamente a exceção de pares individuais. Não altera a primitiva geral de espaçamento; não verifica todas as colisões do nó.

O adaptador V516/V517 mantém resultados anteriores em `regions`, `events`, `end_nodes` e `intermediate_continuity`. Acrescenta `negative_support_relations` e `event_interpretations`; nos términos correspondentes, `current_interpretation` aponta a interpretação atual. SUPERSEDED se refere à interpretação antiga, não a uma aprovação estrutural ou modificação física. N3/RIGHT recebe `current_verification` por ancoragem após apoio intermediário, com N4 como prova conservadora suficiente, sem crédito de N7 fisicamente presente; não calcular al misto.

Testes de contratos/regressões: `test_negative_reinforcement_relations.py`. Executar também toda a suíte existente e a suíte local do Concretopy.
