# Implementação — relações entre armaduras negativas consecutivas

Escopo: interpretação e verificação do desenho existente, sem otimização aplicada. A análise arquitetural foi apresentada antes de codificar. Criada camada semântica específica acima dos motores determinísticos; os motores existentes e Concretopy não foram alterados.

## Fontes consultadas

AGENTS.md; reinforcement-review/SKILL.md; referências negativas de revisão longitudinal, términos independentes, apoios intermediários e apoios extremos; README das ferramentas; negative_detailing.py; longitudinal_review.py; intermediate_support_review.py; negative_end_support_review.py; moment_diagram.py; support_geometry.py; support_correction.py; bar_scaling e testes existentes; Concretopy docs/api_publica.md e docs/ancoragem.md, armaduras.py e contratos atuais. Relatório/goldens V516/V517 e adaptador validar_v516_v517_negativo.py. Skill-creator consultada para atualização/quick_validate.

A busca de massa linear não localizou primitiva existente no assistant/Concretopy: steel_mass.py usa a área pública de Barra, conversão de unidades e densidade explicitamente informada pelo chamador; sem tabela ou valor padrão oculto. Porta-estribo possui regra documentada de bitola e verificação de função/demanda; não possui quantidade/comprimento genéricos confirmados. Essas informações não foram inventadas.

## Arquitetura e contratos

review_negative_relation identifica apoios por ocorrências consecutivas/faces físicas, exige fonte e associação resistente, comprova identidade contínua ou examina todo o momento entre apoios. O papel de peças distintas é inferido do sinal e da presença nas faces; evidência explicitamente incompatível bloqueia conclusão. Sem suporte documental, interseção não classifica.

interval_demand usa somente consultas do diagrama existente em extremos/vértices. compare_detailing_mass separa limites requeridos, comprimento desenhado, gap de aplicabilidade, área total, massa e dados do holder. local_overlap_disposition mantém resultado global e aplica exceção somente a pares individuais explicitamente identificados entre os dois grupos. Corredor global de vibrador independente do par; ausência de coordenadas é inconclusiva.

Comprimentos distintos: 80 cm aplicabilidade; 30 cm encontro; 2lb básico da menor bitola para transição em momento negativo contínuo. Resistência usa grupo completo de menor bitola isolado, nunca uma barra única, soma ou centroide misto. Empates não recebem prioridade arbitrária. Controles independentes e geometria/fabricação incompletas não recebem aprovação automática.

## Resultado real e histórico

Ver seção 16 do relatório V516_V517_negative_reinforcement_review.md. N4/N7: DETAILING_OVERLAP de 138 cm, 30 cm PASS, resistência de N4=3Ø16 PASS em ambas. MRd=118,954088 kNm e Mk=84,967206 kNm; demanda 15,671761/15,333108 kNm. Menor área e menor bitola são N4 por dados da API. Centros transversais e limites estruturais para comparação econômica continuam sem definição, como a quantidade/comprimento do holder.

N7 P2/P1: CONTINUOUS_NEGATIVE_REINFORCEMENT comprovada fisicamente. A descrição de momento sempre negativo diverge dos pontos reais, que possuem pequeno trecho positivo; registrado explicitamente sem alterar diagrama ou resistência.

N3/RIGHT não exige SCALING: motor existente comprova necessidade no vão anterior e suficiência de N4 isolada em todo o ramo adjacente. N7 permanece documentalmente presente sem crédito na prova conservadora. Ancoragem desde face x=2,190 até3,670: disponível148cm, lb62,939073cm, margem85,060927cm PASS nas duas. Sem al/centroide misto. N4/RIGHT e N7/LEFT remetem aos controles do encontro. Todos os três diagnósticos antigos são SUPERSEDED, preservados como histórico.

Não confundir pendências eliminadas de interpretação com centros físicos conhecidos: o arranjo conjunto e o nó continuam inconclusivos. Falha N7+N8+N9 junto P1, N8/LEFT al+lb, N8/N9 RIGHT, dobras extremas e positivos preservados. Nenhuma correção sugerida/aplicada; selected_solution e detailing_optimization null.

## Arquivos desta alteração

Criados:

- tools/reinforcement_checks/negative_reinforcement_relations.py
- tools/reinforcement_checks/negative_reinforcement_relations.md
- tools/reinforcement_checks/steel_mass.py
- tools/reinforcement_checks/test_negative_reinforcement_relations.py
- .agents/skills/reinforcement-review/references/negative-reinforcement-relations.md
- .codex/analises/negative_reinforcement_relations_implementation.md

Alterados:

- analises/pranchas/validar_v516_v517_negativo.py
- analises/pranchas/V516_negative_reinforcement_review.json
- analises/pranchas/V517_negative_reinforcement_review.json
- analises/pranchas/V516_V517_negative_review_validation.json
- .agents/skills/reinforcement-review/SKILL.md
- .agents/skills/reinforcement-review/references/negative-longitudinal-review.md
- tools/reinforcement_checks/README.md
- .codex/analises/V516_V517_negative_reinforcement_review.md

## Validação

74 testes novos, 737 testes assistant aprovados ({'extrator_lst': 39, 'beam_model': 30, 'beam_mapping': 34, 'reinforcement_checks': 634}), 405 Concretopy aprovados; quick_validate válido; git diff --check limpo. 195 hashes de arquivos protegidos invariantes, incluindo árvore fonte/docs/testes Concretopy e goldens históricos não relacionados. Comparação estrutural exata das duas vigas confirmou resultados anteriores preservados. Evidências na validação JSON e tmp/negative_relations_baseline.json.

## Limitações

Sem otimização/redesenho, novas marcas/camadas, dados inventados ou aprovação global. Centros transversais documentais e verificação de colisões/interferências entre camadas/nó/fabricação não completos. Quantidade/comprimento/política mínima de porta-estribo devem vir do chamador com fonte; massa exige densidade explícita. Empates de grupos com mesma bitola não autorizam escolher arbitrariamente capacidade; requerem resolução. Limites requeridos não podem ser substituídos por endpoints documentais.
