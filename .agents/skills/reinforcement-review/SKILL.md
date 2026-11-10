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

## Execução eficiente de pavimentos e retomadas

Ao iniciar ou retomar pavimentos com várias vigas, aplicar [execução incremental](references/incremental-floor-workflow.md): preparação com liberação por controle, índice único de resultados vigentes, cálculo em lote, fila de exceções, invalidação por dependência e emissão a partir da mesma base. Ler somente as referências técnicas dos controles incluídos no escopo. Reutilizar resultados válidos e decisões documentadas; não repetir extrações, auditorias ou cálculos sem mudança ou dúvida identificada. Trabalho ainda não executado permanece distinto de impedimento técnico e não permite anunciar encerramento integral.

## 1.1 Tipo de revisão

Esta skill trata da revisão interna e da correção de vigas, em que padrões do escritório e estudos de simplificação podem fazer parte do escopo.

Para ATP de vigas de terceiros, usar [ATP de vigas](../atp-beam-review/SKILL.md), que reutiliza as referências técnicas desta skill. Para pilares em ATP, usar [Pilares em ATP](../atp-column-review/SKILL.md); os motores e regras de vigas desta skill não verificam automaticamente flexocompressão, emendas ou confinamento de pilares.

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

Quando uma marca positiva termina dentro do vão, seguir [Escalonamento positivo](references/positive-bar-scaling.md) após construir as regiões e verificar a flexão positiva, antes de tratar a ancoragem nos apoios. **Escalonamento não substitui ancoragem nos apoios.**

---

## 7. Apoios da armadura positiva

Para qualquer apoio, seguir [Ancoragem positiva em apoios](references/positive-support-anchorage.md), que encaminha ao [apoio extremo](references/positive-end-support.md), à [correção orientada pelo detalhamento](references/positive-support-correction.md) e aos [grampos complementares](references/positive-support-staples.md).

---

## 8. Armaduras negativas

Seguir [Revisão longitudinal negativa](references/negative-longitudinal-review.md): máximo negativo TQS de cada lado do apoio, sem redução à face; marcas sobre apoio intermediário ([classificação](references/intermediate-support-longitudinal-verification.md)); ancoragens; e [apoios extremos em pilares](references/negative-end-support.md).

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

O resultado oficial da capacidade resistente vem do **Concretopy**; contas independentes são conferências separadas e identificadas. Apresentar os esforços conforme a [convenção permanente de João](../../../profile/force-presentation.md) (tf/tf·m característicos, resistências equivalentes Rd/γf, positiva sem barras superiores). Vsd, MRd e VRd2 continuam grandezas de cálculo nas etapas de cálculo; converter somente a apresentação.

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

## Referências por controle

Ler somente as referências dos controles incluídos no escopo. Cada referência contém, ao final, as orientações transferidas deste arquivo em 06/11/2026.

| Controle | Referência |
|---|---|
| Pavimentos completos (obrigatório: `floor_review.py`) | [floor-operational-review](references/floor-operational-review.md); [execução incremental](references/incremental-floor-workflow.md) |
| Validação documental e geometria física (Etapa 1) | [documentary-physical-preflight](references/documentary-physical-preflight.md) |
| Dados LST/TQS | [Semântica dos dados de vigas TQS](references/tqs-beam-data.md) |
| Processo geral e leitura documental (inclui concretagens em etapas) | [Revisão de vigas](references/beam-review.md); [Convenções de prancha](references/beam-drawing-convections.md) |
| Escalonamento positivo | [Escalonamento positivo](references/positive-bar-scaling.md); [aderência](references/bond-condition.md) |
| Ancoragem positiva em apoios | [Ancoragem positiva em apoios](references/positive-support-anchorage.md) |
| Negativas, apoios intermediários e extremos | [Revisão longitudinal negativa](references/negative-longitudinal-review.md); [apoio intermediário](references/intermediate-support-longitudinal-verification.md); [apoio negativo de extremidade](references/negative-end-support.md) |
| Términos longitudinais coincidentes | [eventos independentes por marca](references/longitudinal-termination-events.md) |
| Relações entre negativas de apoios consecutivos | [relações de armaduras negativas](references/negative-reinforcement-relations.md) |
| Cortante (inclui limite físico em blocos) | [revisão de cortante](references/shear-reinforcement-review.md) |
| Apoios indiretos e suspensão | [planta, direção e reações LST](references/indirect-support-identification.md); [revisão de suspensão](references/suspension-reinforcement-review.md) |
| Diagnóstico consolidado por viga | [diagnóstico consolidado](references/beam-diagnostic.md) |
