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
→ armaduras positivas
→ ancoragem das positivas
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

## 7. Apoio de extremidade da armadura positiva

Quando a armadura positiva chegar a um apoio de extremidade:

- verificar comprimento disponível;
- verificar barras que efetivamente chegam ao apoio;
- considerar esforço cortante;
- considerar momento positivo no apoio quando houver;
- verificar comprimento de ancoragem necessário;
- verificar necessidade de grampos.

Utilizar a ferramenta de cálculo de apoio de extremidade quando
disponível.

---

## 8. Armaduras negativas

Para todos os apoios:

1. identificar armadura detalhada;
2. obter momento solicitante;
3. verificar momento resistente;
4. verificar armadura mínima;
5. verificar distribuição entre camadas;
6. verificar ancoragem;
7. verificar possibilidade de escalonamento.

Utilizar o diagrama de solicitações para determinar regiões onde
barras podem ser interrompidas.

Considerar os comprimentos de ancoragem e deslocamentos de diagrama
aplicáveis.

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

## Refer?ncia de dados TQS

Para extrair, consolidar ou compatibilizar dados LST de vigas, consultar
[Sem?ntica dos dados de vigas TQS](references/tqs-beam-data.md).
