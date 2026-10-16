# S07 — momentos negativos no apoio — revisão da extração

15/10/2026. Correção por orientação explícita de João: usar o máximo negativo no apoio, sem redução para a face interna. O procedimento anterior interpolava o diagrama nas faces do modelo; essas solicitações e os totais de atendimento associados deixam de ser a referência vigente.

Foram revistas 136 consultas existentes. Para cada extremidade foram consultadas ambas as envoltórias características TQS, incluindo diretamente S1 à esquerda ou S13 à direita e os demais pontos fornecidos dentro da região local do apoio no modelo, quando presentes. Selecionou-se o valor mais negativo; um valor positivo não foi convertido em demanda negativa por módulo. Não houve extrapolação nem criação de esforço não fornecido pelo TQS. Máximo aqui significa máximo dos dados disponíveis nessa região; a discretização do arquivo limita a resolução. Em apoios compartilhados, os resultados de ambos os lados devem ser conciliados após comprovar identidade física, composição e continuidade; não se transfere capacidade de um lado para outro.

**Resistência oficial:** saídas já arquivadas do Concretopy, função `verificar_flexao_viga_retangular`, modelo `bloco_retangular_camadas_escoadas_v1`, registradas em `controles_independentes.json`, `spans[].negative_faces[].scenarios[].MRd_outer_knm`. Sem nova execução resistente: nesta revisão mudou a extração da solicitação e foi refeita a comparação com as capacidades existentes. Não foram usados limites algébricos independentes como resistência oficial. Capacidades equivalentes MRd/γf com γf=1,4 e 1 tf=9,80665 kN.

A tabela verifica apenas a composição externa arquivada. Resultado desfavorável dessa composição não comprova falta de armadura quando há aço intermediário de posição pendente. Geometria, camadas, faces físicas, etapas de concretagem e demais pendências permanecem aplicáveis. Não há aprovação global.

| Viga/modelo/vão | Apoio/lado | Mk anterior na face (tf·m) | Mk no apoio (tf·m) | Capacidade Concretopy equivalente C35/C40 (tf·m) | Comparação da composição externa C35/C40 |
|---|---|---:|---:|---:|---|
| V1/V1/1 | P701/left | 9,94 | 11,13 | 12,05/12,14 | Atende/Atende |
| V1/V1/1 | P702/right | 9,85 | 11,14 | 12,05/12,14 | Atende/Atende |
| V2/V2/1 | P704/left | 8,72 | 9,85 | 10,78/10,87 | Atende/Atende |
| V2/V2/1 | P705/right | 12,18 | 13,40 | 12,43/12,55 | Não atende/Não atende |
| V2/V2/2 | P705/left | 11,17 | 12,35 | 12,43/12,55 | Atende/Atende |
| V2/V2/2 | P706/right | 11,45 | 12,71 | 12,43/12,55 | Não atende/Não atende |
| V2/V2/3 | P706/left | 12,82 | 14,11 | 12,43/12,55 | Não atende/Não atende |
| V2/V2/3 | P707/right | 9,91 | 11,42 | 10,78/10,87 | Não atende/Não atende |
| V4/V4/1 | P746/left | 10,86 | 11,59 | 23,91/24,27 | Atende/Atende |
| V4/V4/1 | P747/right | 10,11 | 10,32 | 20,32/20,57 | Atende/Atende |
| V14/V14/1 | PC26C/left | 0,48 | 0,58 | 5,46/5,50 | Atende/Atende |
| V14/V14/1 | PC24C/right | 2,67 | 3,20 | 5,46/5,50 | Atende/Atende |
| V14/V14/2 | PC24C/left | 0,48 | 0,56 | 5,46/5,50 | Atende/Atende |
| V14/V14/2 | PC20C/right | 0,51 | 0,61 | 5,46/5,50 | Atende/Atende |
| V14/V14/3 | PC20C/left | 3,05 | 3,66 | 5,46/5,50 | Atende/Atende |
| V14/V14/3 | V43/right | 0,00 | 0,01 | 5,46/5,50 | Atende/Atende |
| V15/V15/1 | P757/left | 15,09 | 16,85 | 6,84/6,86 | Não atende/Não atende |
| V15/V15/1 | P756/right | 19,38 | 21,59 | 23,91/24,27 | Atende/Atende |
| V15/V15/2 | P756/left | 25,79 | 29,23 | 23,91/24,27 | Não atende/Não atende |
| V15/V15/2 | P760/right | 21,17 | 23,72 | 10,96/11,02 | Não atende/Não atende |
| V15/V15/3 | P760/left | 20,90 | 22,87 | 10,96/11,02 | Não atende/Não atende |
| V15/V15/3 | P758/right | 24,94 | 28,49 | 30,20/30,84 | Atende/Atende |
| V15/V15/4 | P758/left | 26,67 | 30,38 | 30,20/30,84 | Não atende/Atende |
| V15/V15/4 | P761/right | 16,21 | 18,08 | 23,91/24,27 | Atende/Atende |
| V16/V16/1 | PC40C/left | 8,46 | 9,40 | 10,96/11,02 | Atende/Atende |
| V16/V16/1 | PC41C/right | 11,99 | 13,77 | 10,96/11,02 | Não atende/Não atende |
| V17/V17/1 | V23/left | 0,69 | 0,30 | 4,42/4,43 | Atende/Atende |
| V17/V17/1 | V901/right | 6,19 | 7,01 | 20,24/20,49 | Atende/Atende |
| V17/V17/2 | V901/left | 6,13 | 7,01 | 20,24/20,49 | Atende/Atende |
| V17/V17/2 | V902/right | 5,49 | 6,21 | 20,24/20,49 | Atende/Atende |
| V17/V17/3 | V902/left | 5,50 | 6,21 | 20,24/20,49 | Atende/Atende |
| V17/V17/3 | V903/right | 6,01 | 6,86 | 27,21/27,70 | Atende/Atende |
| V17/V17/4 | V903/left | 6,06 | 6,86 | 27,21/27,70 | Atende/Atende |
| V17/V17/4 | V904/right | 6,19 | 7,02 | 27,21/27,70 | Atende/Atende |
| V17/V17/5 | V904/left | 6,19 | 7,02 | 27,21/27,70 | Atende/Atende |
| V17/V17/5 | V905/right | 6,57 | 7,49 | 19,84/20,09 | Atende/Atende |
| V17/V17/6 | V905/left | 6,66 | 7,50 | 19,84/20,09 | Atende/Atende |
| V17/V17/6 | V42/right | 0,39 | 0,38 | 4,42/4,43 | Atende/Atende |
| V21/V21/1 | PC54C/left | 0,00 | 0,00 | 4,39/4,40 | Atende/Atende |
| V21/V21/1 | PC55C/right | 22,29 | 23,76 | 19,57/19,90 | Não atende/Não atende |
| V21/V21/2 | PC55C/left | 21,96 | 23,44 | 19,57/19,90 | Não atende/Não atende |
| V21/V21/2 | PC56C/right | 16,55 | 17,70 | 19,57/19,90 | Atende/Atende |
| V21/V21/3 | PC56C/left | 16,05 | 17,32 | 19,57/19,90 | Atende/Atende |
| V21/V21/3 | PC57C/right | 18,55 | 19,79 | 19,57/19,90 | Não atende/Atende |
| V21/V21/4 | PC57C/left | 18,49 | 19,79 | 19,57/19,90 | Não atende/Atende |
| V21/V21/4 | PC59C/right | 11,02 | 12,05 | 10,74/10,82 | Não atende/Não atende |
| V21/V21/5 | PC59C/left | 11,12 | 12,05 | 10,74/10,82 | Não atende/Não atende |
| V21/V21/5 | PC60C/right | 12,92 | 13,81 | 10,74/10,82 | Não atende/Não atende |
| V21/V21/6 | PC60C/left | 12,50 | 13,48 | 10,74/10,82 | Não atende/Não atende |
| V21/V21/6 | V22/right | 0,00 | 0,00 | 2,22/2,23 | Atende/Atende |
| V22/V22/2 | PC62C/left | 0,72 | 1,28 | 3,45/3,46 | Atende/Atende |
| V22/V22/2 | PC61C/right | 9,45 | 10,47 | 12,43/12,55 | Atende/Atende |
| V22/V22/3 | PC61C/left | 9,44 | 10,76 | 12,43/12,55 | Atende/Atende |
| V22/V22/3 | PC58C/right | 0,00 | 0,00 | 2,23/2,23 | Atende/Atende |
| V25/V25/2 | P745/left | 7,69 | 8,96 | 10,78/10,87 | Atende/Atende |
| V25/V25/2 | P730/right | 14,99 | 16,62 | 10,78/10,87 | Não atende/Não atende |
| V25/V25/3 | P730/left | 6,04 | 6,92 | 10,78/10,87 | Atende/Atende |
| V25/V25/3 | P727/right | 5,74 | 6,50 | 5,56/5,59 | Não atende/Não atende |
| V25/V25/4 | P727/left | 12,11 | 13,32 | 5,56/5,59 | Não atende/Não atende |
| V25/V25/4 | P708/right | 7,95 | 8,31 | 5,13/5,15 | Não atende/Não atende |
| V25/V25/5 | P708/left | 3,21 | 2,47 | 5,13/5,15 | Atende/Atende |
| V25/V25/5 | P701/right | 0,53 | 0,66 | 3,33/3,33 | Atende/Atende |
| V26/V26/1 | PC25C/left | 0,53 | 0,57 | 5,46/5,50 | Atende/Atende |
| V26/V26/1 | PC21C/right | 2,77 | 3,52 | 5,46/5,50 | Atende/Atende |
| V26/V26/2 | PC21C/left | 1,50 | 2,19 | 5,46/5,50 | Atende/Atende |
| V26/V26/2 | PC19C/right | 0,55 | 0,69 | 5,46/5,50 | Atende/Atende |
| V26/V26/3 | PC19C/left | 1,38 | 1,73 | 5,46/5,50 | Atende/Atende |
| V26/V26/3 | V25/right | 0,00 | 0,03 | 5,46/5,50 | Atende/Atende |
| V28/V28/1 | PC34C/left | 14,43 | 16,55 | 10,96/11,02 | Não atende/Não atende |
| V28/V28/1 | PC28C/right | 13,12 | 15,34 | 16,58/16,74 | Atende/Atende |
| V28/V28/2 | PC28C/left | 14,60 | 16,07 | 16,58/16,74 | Atende/Atende |
| V28/V28/2 | V15/right | 0,00 | 0,00 | 4,43/4,44 | Atende/Atende |
| V29/V29/1 | P753/left | 0,00 | 1,13 | 7,94/7,94 | Atende/Atende |
| V29/V29/1 | P740/right | 0,00 | 1,16 | 7,94/7,94 | Atende/Atende |
| V31/V31/1B | None/left | 0,47 | 0,47 | 7,94/7,94 | Atende/Atende |
| V31/V31/1B | P746/right | 17,34 | 17,34 | 7,94/7,94 | Não atende/Não atende |
| V32/V32/1 | PC35C/left | 12,15 | 14,41 | 10,96/11,02 | Não atende/Não atende |
| V32/V32/1 | PC29C/right | 9,56 | 12,10 | 16,58/16,74 | Atende/Atende |
| V32/V32/2 | PC29C/left | 11,14 | 13,10 | 16,58/16,74 | Atende/Atende |
| V32/V32/2 | V15/right | 0,00 | 0,25 | 4,43/4,44 | Atende/Atende |
| V34/V34/1 | P760/left | 25,98 | 29,38 | 16,51/16,67 | Não atende/Não atende |
| V34/V34/1 | P747/right | 24,09 | 26,17 | 23,81/24,16 | Não atende/Não atende |
| V39/V39/1 | P754/left | 0,00 | 1,24 | 7,94/7,94 | Atende/Atende |
| V39/V39/1 | P743/right | 0,00 | 1,26 | 7,94/7,94 | Atende/Atende |
| V41/V41/1B | None/left | 0,13 | 0,13 | 7,94/7,94 | Atende/Atende |
| V41/V41/1B | P744/right | 4,06 | 4,06 | 7,94/7,94 | Atende/Atende |
| V43/V43/2 | P748/left | 7,20 | 8,22 | 8,22/8,27 | Não atende/Atende |
| V43/V43/2 | P737/right | 14,38 | 15,78 | 12,43/12,55 | Não atende/Não atende |
| V43/V43/3 | P737/left | 7,89 | 8,84 | 12,43/12,55 | Atende/Atende |
| V43/V43/3 | P723/right | 7,73 | 8,70 | 8,22/8,27 | Não atende/Não atende |
| V43/V43/4 | P723/left | 11,64 | 12,71 | 8,22/8,27 | Não atende/Não atende |
| V43/V43/4 | P714/right | 10,52 | 11,75 | 8,22/8,27 | Não atende/Não atende |
| V43/V43/5 | P714/left | 5,29 | 5,92 | 8,22/8,27 | Atende/Atende |
| V43/V43/5 | P707/right | 0,88 | 1,34 | 4,41/4,42 | Atende/Atende |
| V5/V5/1 | P741/left | 7,40 | 8,66 | 8,18/8,27 | Não atende/Não atende |
| V5/V5/1 | P742/right | 8,31 | 10,90 | 11,37/11,56 | Atende/Atende |
| V11/V11/1 | P752/left | 1,57 | 3,20 | 5,54/5,55 | Atende/Atende |
| V11/V11/1 | P754/right | 0,94 | 0,82 | 5,75/5,76 | Atende/Atende |
| V18/V18/1 | V23/left | 0,00 | 0,00 | 2,23/2,23 | Atende/Atende |
| V18/V18/1 | PC45C/right | 17,10 | 18,45 | 12,43/12,55 | Não atende/Não atende |
| V18/V18/2 | PC45C/left | 16,20 | 18,41 | 12,43/12,55 | Não atende/Não atende |
| V18/V18/2 | PC46C/right | 7,84 | 9,25 | 8,50/8,56 | Não atende/Não atende |
| V19/V19/1 | PC47C/left | 7,82 | 9,15 | 10,78/10,87 | Atende/Atende |
| V19/V19/1 | PC48C/right | 10,32 | 12,25 | 10,78/10,87 | Não atende/Não atende |
| V20/V20/1 | PC49C/left | 10,64 | 12,60 | 10,78/10,87 | Não atende/Não atende |
| V20/V20/1 | PC50C/right | 6,92 | 8,20 | 10,78/10,87 | Atende/Atende |
| V27/V27/1 | P750/left | 7,58 | 7,94 | 10,56/10,67 | Atende/Atende |
| V27/V27/1 | P739/right | 1,49 | 2,34 | 5,50/5,53 | Atende/Atende |
| V30/V30/1 | PC2C/left | 7,99 | 10,26 | 6,26/6,28 | Não atende/Não atende |
| V30/V30/1 | P710/right | 7,47 | 9,58 | 10,03/10,09 | Atende/Atende |
| V33/V33/1 | P794/left | 15,89 | 16,07 | 8,47/8,52 | Não atende/Não atende |
| V33/V33/1 | V19/right | 0,00 | 0,00 | 8,47/8,52 | Atende/Atende |
| V35/V35/1 | PC36C/left | 8,34 | 10,14 | 8,22/8,27 | Não atende/Não atende |
| V35/V35/1 | PC30C/right | 18,95 | 21,95 | 10,78/10,87 | Não atende/Não atende |
| V35/V35/2 | PC30C/left | 19,95 | 22,81 | 10,78/10,87 | Não atende/Não atende |
| V35/V35/2 | V15/right | 0,02 | 0,00 | 3,33/3,33 | Atende/Atende |
| V36/V36/1 | V5/left | 0,56 | 0,07 | 2,23/2,23 | Atende/Atende |
| V36/V36/1 | P735/right | 19,98 | 22,91 | 10,78/10,87 | Não atende/Não atende |
| V37/V37/1 | P725/left | 16,92 | 18,72 | 10,78/10,87 | Não atende/Não atende |
| V37/V37/1 | P712/right | 14,88 | 17,05 | 16,15/16,36 | Não atende/Não atende |
| V38/V38/1 | P752/left | 7,76 | 10,39 | 10,56/10,67 | Atende/Atende |
| V38/V38/1 | P742/right | 1,40 | 2,44 | 3,30/3,31 | Atende/Atende |
| V40/V40/1 | P796/left | 15,53 | 17,70 | 8,47/8,52 | Não atende/Não atende |
| V40/V40/1 | V20/right | 0,00 | 0,00 | 8,47/8,52 | Atende/Atende |
| V44/V44/1 | P738/left | 2,94 | 3,58 | 6,81/6,84 | Atende/Atende |
| V44/V44/1 | P731/right | 26,68 | 30,79 | 10,91/10,98 | Não atende/Não atende |
| V45/V45/1 | P750/left | 1,10 | 1,29 | 3,31/3,32 | Atende/Atende |
| V45/V45/1 | P753/right | 2,63 | 2,42 | 3,44/3,45 | Atende/Atende |
| V46/V46/1 | P747/left | 8,83 | 9,33 | 12,43/12,55 | Atende/Atende |
| V46/V46/1 | P751/right | 1,35 | 1,21 | 4,41/4,42 | Atende/Atende |
| V47/V47/1 | P751/left | 10,35 | 14,82 | 12,38/12,50 | Não atende/Não atende |
| V47/V47/1 | P741/right | 1,28 | 1,88 | 3,31/3,32 | Atende/Atende |
| V48/V48/1 | P767/left | 16,53 | 19,55 | 6,77/6,81 | Não atende/Não atende |
| V48/V48/1 | P758/right | 12,04 | 13,38 | 10,78/10,87 | Não atende/Não atende |
| V24/V23/3 | P785/left | 10,82 | 11,64 | 18,42/18,51 | Atende/Atende |
| V24/V23/3 | P778/right | 7,63 | 8,56 | 18,42/18,51 | Atende/Atende |
