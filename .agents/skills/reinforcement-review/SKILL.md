---
name: reinforcement-review
description: >
  Auxilia na revisão técnica de detalhamentos de armaduras de elementos
  estruturais, comparando geometria, esforços, dimensionamento,
  detalhamento e critérios de execução. Utilizar inicialmente para
  revisão de vigas, expandindo posteriormente para lajes e outros elementos.
---

# Reinforcement Review

## 1. Objetivo

Auxiliar João na revisão técnica de detalhamentos de armaduras.

A revisão não consiste apenas em verificar se a quantidade de aço
detalhada é superior à calculada.

Devem ser avaliados simultaneamente:

- geometria;
- condições de apoio;
- esforços solicitantes;
- resistência;
- armadura mínima;
- ancoragem;
- continuidade;
- disposição das barras;
- número de camadas;
- espaçamentos;
- cisalhamento;
- armaduras especiais;
- construtibilidade;
- coerência global do detalhamento.

O processo deve utilizar, quando disponíveis:

1. planta estrutural;
2. prancha de detalhamento;
3. resultados do TQS;
4. ferramentas de cálculo;
5. critérios de detalhamento do escritório;
6. requisitos normativos aplicáveis.

---

## 2. Princípio de revisão

Trabalhar elemento por elemento.

Para vigas, seguir preferencialmente:

Geometria
→ interpretação das armaduras positivas e regiões de composição
→ resistência à flexão positiva
→ escalonamento positivo dentro do vão, quando houver interrupção
→ ancoragem das positivas nos apoios
→ armaduras negativas
→ ancoragem das negativas
→ cisalhamento
→ armadura de suspensão
→ detalhes especiais
→ construtibilidade
→ revisão global.

Não considerar uma viga aprovada apenas porque o TQS conseguiu
dimensioná-la.

Não considerar o detalhamento produzido automaticamente pelo TQS
como necessariamente adequado.

---

## 3. Separação entre dados e conclusões

Durante a revisão, distinguir:

### Dados do projeto
Geometria, materiais, condições de apoio e demais premissas.

### Solicitações
Esforços obtidos do modelo estrutural.

### Armadura detalhada
Informações efetivamente apresentadas na prancha.

### Verificação
Resultado obtido através das ferramentas de cálculo.

### Julgamento de engenharia
Avaliação de continuidade, construtibilidade, simplificação,
detalhes especiais e demais decisões.

Não inferir esforços a partir do detalhamento quando os resultados
do modelo estiverem disponíveis.

---

# REVISÃO DE VIGAS

## 4. Sequência

Revisar cada viga individualmente.

Casos especiais que exigirem investigação mais extensa podem ser
identificados e separados para análise posterior, evitando interromper
desnecessariamente o fluxo de revisão das demais vigas.

---

## 5. Geometria

Antes de verificar armaduras:

1. comparar a geometria da viga com a planta estrutural;
2. verificar seção;
3. verificar dimensões dos vãos;
4. verificar desníveis;
5. verificar condições de apoio;
6. identificar mudanças de seção;
7. identificar situações especiais.

Não prosseguir com verificações numéricas utilizando uma geometria
que não represente corretamente o modelo.

---

## 6. Armaduras positivas

Para todos os vãos:

1. identificar as barras detalhadas;
2. identificar número de barras;
3. identificar bitolas;
4. identificar camadas;
5. obter o momento solicitante aplicável;
6. calcular/verificar o momento resistente da configuração;
7. verificar armadura mínima;
8. verificar espaçamento entre barras;
9. verificar executabilidade;
10. verificar ancoragem nos apoios.

Comparar:

M resistente ≥ M solicitante

utilizando a ferramenta de cálculo aplicável.

Não avaliar apenas área total de aço quando a posição das barras e
a altura útil forem relevantes.

---

## 6.1 Escalonamento positivo dentro do vão

Quando uma marca positiva termina dentro do vão, executar o procedimento
[Escalonamento positivo](references/positive-bar-scaling.md) após construir as
regiões e verificar a flexão positiva, antes de tratar ancoragem nos apoios.
Usar `tools/reinforcement_checks/bar_scaling.check_bar_scaling`, que reutiliza
regiões, diagrama TQS e Concretopy; não recalcular resistência, fbd, lb ou al.

Identificar lado do corte, composições antes/depois, capacidade remanescente,
referências do diagrama e entradas de al/lb; preservar separadamente condições
A/B, diagnósticos e provenance. Consultar as regras de Vk, d e aderência
indicadas na referência. Geometria/composição/modelo não resolvido, ramo/cruzamento
ambíguo ou caso fora do escopo bloqueiam a conclusão (`scaling_passes=null`).

**Escalonamento não substitui ancoragem nos apoios.** Atender ao corte no vão
não aprova a viga nem demonstra ancoragem suficiente em um apoio.

---

## 7. Apoios da armadura positiva

Para qualquer apoio, começar por [Ancoragem positiva em apoios](references/positive-support-anchorage.md): END/INTERMEDIATE, LEFT/RIGHT relativo ao vão, seção terminal e controles aplicáveis.
Quando a armadura positiva chegar ao apoio extremo END, consultar
[Apoio positivo](references/positive-end-support.md) e, para corrigir falha,
[Correção orientada pelo detalhamento](references/positive-support-correction.md).
Verificar existente; depois prolongar barras escalonadas mantendo camada/bitola;
só sem prolongamento adequado estudar redistribuição simples com recálculo completo.
Conferir cabimento com a regra confirmada max(2 cm, diâmetro) e compatibilidade
com flexão em todas as regiões. Diferença de uma ou duas posições na série de
bitolas é preferência de detalhamento, não prescrição da NBR.

A busca genérica permanece exploratória; não recomenda isoladamente alteração
de prancha. Separar validade calculada, recomendação para análise e decisão do
engenheiro. Para estudar armadura complementar, consultar
[Grampos complementares](references/positive-support-staples.md): demanda inicial
As_adicional, peça em U de dois ramos, L_long=max(2*lb+lb_ef,60 cm) por ramo
com lb básico da própria bitola, e conector b−2*cobrimento−1 cm.
Bitolas usuais próprias Ø6,3/Ø8/Ø10, configuráveis; acima de três peças requer
avaliação especial, sem reprovação estrutural automática. São decisões do engenheiro. Distribuir verticalmente de baixo para cima com 2 cm livres entre peças;
conferir altura ocupada separadamente das interferências do nó.
Não converter área calculada em detalhamento pronto.
Preservar prolongamentos válidos na comparação e selected_solution=null.
Para regressão integrada, consultar o
[golden positivo V536 atualizado](../../../.codex/analises/support_anchorage_generalization_audit.md):
resultados por etapa, falha original de ancoragem e pendências explícitas;
não usar o nome golden como aprovação global.
A posição desenhada não substitui lb_ef=L_apoio-cobrimento. Gancho/interferências
no nó ainda exigem revisão. A limitação anterior ao extremo esquerdo foi superada em orientação; INTERMEDIATE segue regras próprias, sem aplicar grampos/gancho END automaticamente.

---

## 8. Armaduras negativas

Após a positiva, consultar [Revisão longitudinal negativa](references/negative-longitudinal-review.md).
Identificar função das barras, camadas desde a face superior e regiões; verificar
resistência regional, escalonamentos sucessivos, término no vão, continuidade,
nó extremo e balanço somente quando aplicáveis. Usar `longitudinal_review` e
`negative_detailing`, reutilizando regiões, interpolação e Concretopy.
Preservar momentos originais com sinal; negativa comprime a face inferior.
Nas marcas que atravessam apoio intermediário, primeiro [classificar a necessidade no vão adjacente](references/intermediate-support-longitudinal-verification.md): SCALING, ancoragem básica desde a face física, ou INCONCLUSIVE. Provar suficiência da remanescente em todo o ramo; crossing ausente isoladamente não determina a classificação. Esta etapa verifica o desenho existente, sem otimização.
Separar os controles al+lb e al+10φ quando aplicáveis, má aderência confirmada, geometria da dobra
e resistência de ancoragem. Dados/ramo/continuidade não resolvidos mantêm null.
Não transportar automaticamente as regras ou grampos positivos para negativas.
Nos apoios extremos em pilares, seguir [apoio negativo de extremidade](references/negative-end-support.md): resistência terminal S1/S13, ancoragem física, perna vertical documentada e controles transversais independentes. Não somar os trechos da dobra como lb reto nem aplicar α=0,7. Verificar um corredor livre ≥4 cm, conservando os mínimos existentes. Sem dimensão transversal do pilar/centros das barras, registrar o controle pendente; não modificar d ou a seção resistente pelo cobrimento lateral efetivo.

---

## 9. Apoio de extremidade em outra viga

Quando uma viga possuir outra viga como apoio de extremidade e a
ligação for considerada articulada segundo o modelo adotado, verificar
o detalhamento conforme o padrão vigente do escritório.

No procedimento atualmente utilizado por João, esses casos são
detalhados apenas com porta-estribo, respeitando o critério de bitola
adotado pelo escritório.

Não generalizar essa regra para situações cujo modelo estrutural
represente transmissão de momento.

---

## 10. Cisalhamento

Para cada região relevante:

1. obter Vsd;
2. verificar resistência da biela comprimida;
3. verificar armadura transversal necessária;
4. verificar armadura transversal mínima;
5. verificar número de ramos;
6. verificar espaçamento máximo;
7. escolher arranjo executável;
8. verificar passagem adequada do concreto.

Confirmar que:

Vrd2 > Vsd

segundo o modelo de cálculo aplicável.

Não aceitar automaticamente o detalhamento do TQS quando ele produzir
arranjos pouco executáveis ou antieconômicos.

---

## 11. Apoios indiretos

Identificar vigas apoiadas em outras vigas.

Quando aplicável:

- obter reação de apoio;
- definir parcela da reação a ser suspensa;
- definir região de distribuição;
- dimensionar armadura de suspensão;
- verificar compatibilidade com os demais estribos.

Evitar duplicação desnecessária de armaduras quando regiões de
cisalhamento e suspensão puderem ser tratadas de forma compatível.

---

## 12. Detalhes especiais

Identificar situações que exijam tratamento específico, incluindo:

- apoio parcial em pilar;
- viga passando externamente ao pilar;
- mudança de direção;
- vigas penduradas;
- mudanças de seção;
- continuidade entre vigas distintas;
- regiões com concentração elevada de armaduras.

Aplicar referências específicas quando disponíveis.

Quando não houver critério documentado, sinalizar para análise de João.

---

## 13. Construtibilidade

Avaliar:

- espaçamento entre barras;
- espaçamento dentro dos pilares;
- número de barras por camada;
- quantidade de camadas;
- passagem de concreto;
- possibilidade de montagem;
- excesso de barras de pequeno diâmetro;
- sobreposição de armaduras;
- interferência entre armaduras de vigas que se encontram.

Uma solução resistente pode ainda ser inadequada do ponto de vista
construtivo.

---

## 14. Continuidade e padronização

Quando houver continuidade entre vigas diferentes:

- verificar se a continuidade das armaduras está adequadamente representada;
- evitar interrupções incompatíveis;
- indicar explicitamente a continuidade necessária na correção.

Quando existirem pavimentos ou regiões simétricas:

- comparar vigas correspondentes;
- procurar compatibilizar os detalhamentos quando tecnicamente possível.

Evitar diferenças desnecessárias entre elementos equivalentes.

---

## 15. Otimização

Durante a revisão, procurar também:

- armaduras excessivas;
- escalonamentos desnecessariamente complexos;
- simplificações antieconômicas;
- excesso de barras de pequeno diâmetro;
- detalhamentos que possam ser simplificados sem prejuízo técnico.

O objetivo não é apenas encontrar falta de armadura.

Uma revisão também deve identificar detalhamentos excessivamente
conservadores ou difíceis de executar.

---

## 16. Erros recorrentes

Dar atenção especial a:

- problemas de ancoragem de armaduras negativas;
- armaduras em excesso;
- simplificações antieconômicas;
- ausência de grampos quando necessários;
- erros associados a mudanças de seção;
- armaduras geradas pelo TQS que não representem adequadamente a
  situação real do elemento.

As referências específicas podem registrar outros padrões recorrentes.

---

## 17. Registro da correção

Quando identificar uma correção:

1. indicar claramente no PDF o que deve ser alterado;
2. mostrar, quando possível, a solução esperada;
3. explicar o motivo quando ele não for evidente;
4. evitar comentários excessivos para alterações simples.

Quando o mesmo erro se repetir diversas vezes, sinalizar o padrão
recorrente para João.

O problema pode indicar necessidade de:

- orientação ao responsável;
- alteração do procedimento;
- atualização do padrão de detalhamento;
- criação de uma verificação automatizada.

---

## 18. Resultado da revisão

Ao concluir a análise de uma viga, classificar os pontos encontrados
preferencialmente como:

- OK;
- corrigir;
- verificar;
- caso especial.

Não declarar uma verificação numérica como concluída quando os dados
necessários não estiverem disponíveis.

Indicar claramente quais informações faltam.

---

# AUTOMAÇÃO

## 19. Dados do TQS

Sempre que arquivos do TQS estiverem disponíveis, procurar obter dados
diretamente deles antes de solicitar transcrição manual.

Dados de interesse incluem:

- identificação da viga;
- pavimento;
- geometria;
- vãos;
- apoios;
- condições de apoio;
- esforços de flexão;
- esforços cortantes;
- reações;
- resultados de dimensionamento;
- armaduras calculadas;
- demais informações úteis à revisão.

Não assumir previamente qual arquivo contém cada informação.

Investigar e documentar os formatos disponíveis.

---

## 20. Cálculos determinísticos

Sempre que possível, verificações numéricas repetitivas devem ser realizadas
por ferramentas determinísticas e não por estimativas do modelo de linguagem.

Isso inclui potencialmente:

- momento resistente;
- armadura mínima;
- espaçamento;
- comprimento de ancoragem;
- cisalhamento;
- Vrd2;
- espaçamento máximo de estribos;
- armadura de suspensão;
- verificação de apoio de extremidade;
- grampos.

A planilha de verificação utilizada por João deve ser considerada uma
referência inicial para esses cálculos.

Antes de substituir a planilha por uma implementação própria, validar os
resultados da nova ferramenta contra casos conhecidos.

---

## 21. Papel do auxiliar

O auxiliar deve procurar reduzir o trabalho mecânico de revisão sem
substituir o julgamento de engenharia.

Priorizar automação de:

extração
→ organização
→ cálculo
→ comparação
→ identificação de inconsistências.

Manter João no processo para:

interpretação
→ casos especiais
→ decisões de detalhamento
→ validação final.

## Referências operacionais de vigas

Para extrair, consolidar ou compatibilizar dados LST de vigas, consultar
[Semântica dos dados de vigas TQS](references/tqs-beam-data.md).

Para o processo geral e a leitura documental, consultar
[Revisão de vigas](references/beam-review.md) e
[Convenções de prancha](references/beam-drawing-convections.md).
Para cortes positivos no vão, consultar
[Escalonamento positivo](references/positive-bar-scaling.md), que encaminha
às regras de Vk, centroide anterior, aderência e ferramentas existentes.

Para ancoragem positiva em apoios END/INTERMEDIATE, LEFT/RIGHT relativo ao vão,
consultar [Ancoragem positiva em apoios](references/positive-support-anchorage.md).
Separar demanda, ancoragem longitudinal e verificação completa do nó; gerar
correções somente após falha resolvida, preservando inconclusivos.

Para negativas, consultar [Revisão longitudinal negativa](references/negative-longitudinal-review.md),
com regras próprias de cortes, término, continuidade, nós e balanço.

Términos longitudinais coincidentes: consultar [eventos independentes por marca](references/longitudinal-termination-events.md). Usar a composição física posterior, sem sequência artificial; separar término desenhado e posição requerida.

### Relações entre negativas de apoios consecutivos

Após a revisão regional, executar [relações de armaduras negativas](references/negative-reinforcement-relations.md): identidade física -> comportamento do momento -> CONTINUOUS / DETAILING_OVERLAP / REINFORCEMENT_LAP_TRANSITION / INDEPENDENT (ou INCONCLUSIVE) -> comprimento -> comparação local de massa, quando comprovada -> resistência de toda a sobreposição -> construtibilidade. Usar `negative_reinforcement_relations`, sem modificar os motores de flexão ou SCALING.

Manter distintos: 80 cm limita o gap para comparação econômica; 30 cm é ultrapassagem de detalhamento; 2lb é transição resistente. Menor As total escolhe a candidata ao prolongamento; menor bitola define lb; o grupo completo de menor bitola, isolado, verifica resistência do encontro. Não somar grupos ou criar centroide misto. A exceção de espaçamento é local; continuidade não substitui resistência. Preservar histórico SUPERSEDED e pendências físicas reais. Sem limites estruturais, dados de porta-estribo ou centros físicos, bloquear apenas os controles dependentes. `selected_solution` e `detailing_optimization` permanecem null.

### Armadura transversal ao cortante

Executar [revisão de cortante](references/shear-reinforcement-review.md): séries Vk/domínio TQS -> referência por terços -> faixas reais da prancha -> máximo próprio da faixa -> Concretopy -> controles independentes de VRd2, Asw/s e smax -> prática usual -> ramos/porta-estribo -> conclusão específica. Usar `shear_diagram` e `shear_review`, preservando os motores longitudinais.

Terços são referência, não fronteiras obrigatórias do desenho. Selecionar d de centroides regionais existentes: máximo número de camadas, maior As em empate e menor d em novo empate. Preservar sinal, série, gaps e limites documentais. Não inferir ramos de peças não convencionais, estender faixas para nós sem fonte ou converter REVIEW em FAIL. Suspensão fica NOT_EVALUATED; selected_solution/detailing_optimization null. Aprovação de cortante não significa aprovação global da viga.

Na revisão de cortante, classificar primeiro a função documental da peça: negativa de laje adjacente não fornece Asw/s da viga. Separar domínio TQS de cobertura física entre faces comprovadas dos pilares; dentro destes a exigência de estribos da viga é NOT_APPLICABLE. Falta de estribos no trecho físico da viga e geometria ambígua continuam inconclusivas. Consultar a referência de cortante e `shear_coverage`; não inferir função pela marca ou prolongar faixas.

### Suspensão após a revisão independente de cortante

Executar [revisão de suspensão](references/suspension-reinforcement-review.md) na viga receptora somente a partir de ligação e reação total comprovadas. Usar `suspension_review`, preservando o cortante independente. Interpretar fontes -> classificar ligação -> validar reação/natureza -> distribuir fisicamente -> máximo próprio da região -> Concretopy sem mínimo -> combinar taxas -> verificar todas as faixas reais. Dados ausentes, origem do balanço não confirmada e sobreposições sem regra conservam INCONCLUSIVE; falhas conhecidas não são ocultadas. Não selecionar armadura ou redesenhar. A marca N12 do caso real continua excluída como negativa de laje adjacente.

Para identificar apoios indiretos antes da suspensão, consultar [planta, direção e reações LST](references/indirect-support-identification.md); geometria não determina direção da transferência de carga.

### Diagnóstico consolidado por viga

Após as revisões independentes, seguir [diagnóstico consolidado](references/beam-diagnostic.md). Usar resultados existentes com identidade/pavimento/coordenadas comprovados; separar falhas, pendências e revisão de engenharia. Não recalcular nem selecionar correções. Módulo ausente é pendência, não inaplicabilidade comprovada.

Na consolida��o, separar execu��o de resultado t�cnico conforme [beam-diagnostic](references/beam-diagnostic.md). Pontas sem cota exigem conven��o geom�trica rastre�vel; propostas e refer�ncias gr�ficas s�o contratos futuros, sem otimiza��o ou edi��o autom�tica.

## Validação documental e geometria física — Etapa 1

Nas novas revisões, aplicar [documentary-physical-preflight](references/documentary-physical-preflight.md) para conciliação de documentos, ocorrências físicas, geometria por trecho e liberação local das entradas. Este procedimento preserva os métodos resistentes existentes e a compatibilidade dos contratos antigos. Restrições específicas da Etapa 1 prevalecem sobre requisitos de módulos posteriores: não tornar obrigatórios pinos, trajetórias curvas, interferência com armaduras de pilares ou combinações concomitantes.
