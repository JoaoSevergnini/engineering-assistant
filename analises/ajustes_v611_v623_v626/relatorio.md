# Ajustes pontuais — V611, V623 e V626

O sistema distingue agora falta de método resistente, falha documental e dificuldade de posicionamento TQS. Os ajustes reutilizam a guarda, a reconciliação documental e o eixo comum existentes. Nenhum método resistente, PDF, LST ou arquivo histórico foi alterado.

## V611 — transições de altura

**Problema:** a pendência de geometria não explicava que, mesmo após cotar a transição, seu procedimento resistente ainda depende de desenvolvimento pelo engenheiro.

**Alteração:** os controles dependentes da região de transição recebem `implementation=NOT_IMPLEMENTED` na limitação de método, mantendo `INCONCLUSIVE / NOT_EXECUTED`. A informação documental continua separada: a posição exata da mudança dentro dos apoios ainda precisa ser cotada. Não foi criada seção média ou aproximação resistente.

**Evidência:** planta de formas 051-SJ-EST-EX-010-PLB-TP-R01, página 1; leitura geométrica preservada em `V611_form_reviewed.json`. Origem do eixo: face interna de P28, sentido P19–P10–P1.

| Região no eixo comum (m) | Seção / comportamento | Situação |
|---|---|---|
| 0–2,82 | 19 × 57 cm, vão livre P28–P19 | Método de seção constante disponível |
| 2,82–3,52 | Mudança 57→47 dentro de P19 | Método não implementado; posição exata também pendente |
| 3,52–6,19 | 19 × 47 cm, vão livre P19–P10 | Método de seção constante disponível |
| 6,19–6,89 | Mudança 47→57 dentro de P10 | Método não implementado; posição exata também pendente |
| 6,89–9,31 | 19 × 57 cm, vão livre P10–P1 | Método de seção constante disponível |

**O que pode ser verificado:** trechos constantes independentes, desde que suas próprias entradas estejam comprovadas. Um teste com o motor real confirma que a pendência de uma transição não bloqueia a região independente.

**Pendência real:** esta execução não aprovou a flexão da V611. Os arquivos históricos ainda têm extremos longitudinais das barras sem comprovação, camadas não interpretadas para esses lotes e entradas resistentes não preenchidas. Essas faltas são distintas da ausência de método nas transições. O registro de ausência de cota vem do exame documental anterior; não foi promovido de uma mera falha de extração.

## V623 — falha de plotagem da N2

**Problema:** a quantidade da tabela/corte podia ser confundida com informação suficiente para verificar a distribuição longitudinal.

**Alteração:** uma falha de plotagem longitudinal comprovada na reconciliação suspende a revisão estrutural completa da viga, inclusive verificações de outra face. A guarda impede os cálculos; o diagnóstico exige corrigir ou reemitir a prancha. Não há FAIL resistente nem proposta de alteração de armaduras.

**Evidência:** reconciliação preservada da prancha 051-SJ-EST-LO-06303-VIG-TIP-R00, página 1, e confirmação documental do engenheiro. A N2 permanece como **4 Ø16, C=464 cm na tabela**, com quatro barras no corte A; seus extremos e sua continuidade longitudinal permanecem não comprovados. Nenhum intervalo foi reconstruído a partir desses dados.

**Situação atual:** todos os controles do caso real ficam `INCONCLUSIVE / NOT_EXECUTED`, com causa documental e N2 identificada como afetada. A reemissão deve tornar legíveis posição, extensão, interrupções e demais indicações longitudinais. Ausência de extração isolada não é classificada como falha de plotagem.

## V626 — balanço esquerdo e série TQS

**Problema:** aplicar uma convenção de extremidade à primeira seção do arquivo inteiro confundiria o balanço com o vão adjacente.

**Alteração:** o posicionador existente aceita a orientação comprovada e os limites físicos por vão. Para a série correspondente ao balanço LEFT, a primeira seção representa a face livre; para RIGHT, a última. Confere identidade do vão, ordem das seções e comprimento com a forma, preservando valores, sinais e envoltórias. Balanço único também exige orientação comprovada. A transformação ao eixo comum continua sendo feita pelo registro existente.

**Evidência real:** a forma confirma o prolongamento no sentido negativo do eixo comum junto a P31. O VGESFS preservado identifica **1B, comprimento 0,949 m, linha 814**. Entretanto, as séries de Q mínimo, M mínimo, Q máximo, M máximo e torção das linhas **819, 822, 825, 828 e 831 pertencem todas ao vão 2**. O modelo documental do balanço 1B não contém uma série de esforços VGESFS correspondente.

**Pendência objetiva:** `cantilever_force_series_unavailable: span=1`. É necessário disponibilizar e examinar a série do balanço 1B no LST original; a série do vão 2 não foi substituída. Também precisa ser esclarecida a compatibilidade do comprimento: a leitura física anterior indica 0,53 m entre a face livre e o eixo de P31, enquanto o VGESFS informa 0,949 m. Não foi escolhida uma interpretação para eliminar essa diferença. Não houve cálculo resistente nem aprovação do balanço.

Foram encontrados também os tokens de balanço V617/2B, V620/2B, V622/2B, V625/2B, V627/2B e V629/4B nos extratos do pavimento. São candidatos documentais registrados em `balancos_reais.json`; suas orientações e comprimentos não foram certificados nesta rodada. Nenhum encontro entre vigas foi usado como prova de transferência de esforços.

## Verificações estruturais reais

**V607:** repetição do cálculo positivo pelo fluxo atual após a guarda: MRd = **22,193067 kN·m**, MSd = **6,658715 kN·m**, utilização = **30,003583%**, resultado PASS. MRd e utilização são exatamente iguais aos da execução anterior. A conclusão continua limitada à flexão positiva no vão livre.

**V611, V623 e V626:** os resultados desta rodada são os enquadramentos e as pendências descritos acima; não são aprovações resistentes. Os extratos TQS/detalhamento são os arquivos preservados, sem nova leitura dos originais LST indisponíveis.

## Testes automatizados

| Suíte | Testes encontrados | Resultado |
|---|---:|---|
| beam_model | 71 | Sem falhas |
| extrator_lst | 48 | Sem falhas; 2 ignorados por indisponibilidade dos relatórios locais originais |
| beam_mapping | 57 | Sem falhas |
| reinforcement_checks | 999 | Sem falhas |
| Total | **1.175** | **1.173 executados; 2 ignorados** |

Foram acrescentados nove testes: isolamento da transição; suspensão documental de controles independentes; distinção entre falha de extração e plotagem; balanços LEFT/RIGHT e únicos; orientação ausente; comprimento divergente; série de outro vão; série ausente; múltiplos balanços com séries próprias. Os casos sintéticos demonstram comportamento do código, não segurança das vigas reais.

Alterações localizadas em `input_preflight.py`, `floor_review.py`, `section_positions.py`, seus testes existentes e documentação operacional. A reprodução compara hashes de **327 arquivos históricos/fontes/Concretopy**, todos preservados.

Registros: [resumo.json](resumo.json), [testes.json](testes.json), [preservacao.json](preservacao.json), [resultado V611/V623](resultado_v611_v623.json), [balanços reais](balancos_reais.json) e [regressão V607](resultado_v607.json). Reprodução: `python analises/ajustes_v611_v623_v626/validar.py`.
