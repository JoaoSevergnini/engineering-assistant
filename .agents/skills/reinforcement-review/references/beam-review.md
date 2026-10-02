# Procedimento de revisão de detalhamento de vigas

## 1. Objetivo

Este documento descreve o procedimento atualmente utilizado por João
para revisar o detalhamento de armaduras de vigas de concreto armado.

O objetivo da revisão é verificar a compatibilidade entre:

- geometria da estrutura;
- detalhamento apresentado na prancha;
- esforços provenientes do modelo estrutural;
- armaduras detalhadas;
- critérios normativos;
- resultados das ferramentas independentes de verificação.

Este documento descreve o processo de revisão.

As convenções utilizadas para interpretar graficamente as pranchas estão
registradas em `beam-drawing-conventions.md`.

---

## 2. Fontes utilizadas durante a revisão

A revisão normalmente utiliza simultaneamente quatro fontes principais.

### 2.1 Prancha de detalhamento de vigas

Utilizada para identificar o que efetivamente foi detalhado para execução.

Informações relevantes incluem:

- identificação das vigas;
- geometria indicada;
- identificação dos apoios;
- armaduras longitudinais;
- armaduras transversais;
- camadas de armadura;
- comprimentos e extensões das barras;
- ancoragens;
- grampos;
- armaduras de suspensão;
- armaduras de pele;
- cortes;
- detalhes especiais.

A armadura presente na prancha é o objeto principal da revisão.

Não assumir que a armadura detalhada é igual à armadura calculada pelo TQS.

### 2.2 Planta baixa estrutural ou modelo RVT

Utilizados como referência para verificar a geometria da estrutura.

Verificar principalmente:

- seção das vigas;
- mudanças de seção;
- comprimento dos vãos;
- posição e identificação dos apoios;
- dimensões dos apoios;
- desníveis;
- continuidade entre elementos;
- condições geométricas especiais;
- vigas apoiadas indiretamente em outras vigas.

### 2.3 Módulo de edição de armaduras de vigas do TQS

Utilizado principalmente para consultar:

- envoltória de momentos fletores;
- esforços cortantes;
- torção;
- esforço normal;
- dados dos apoios;
- reações;
- armaduras calculadas pelo TQS;
- comportamento dos esforços ao longo da viga.

Os resultados do TQS são uma fonte de informação para a revisão e não
substituem a verificação independente.

A armadura calculada pelo TQS pode ser utilizada como referência, mas
uma diferença entre a armadura do TQS e a armadura detalhada não
caracteriza automaticamente um erro.

### 2.4 Planilha de verificação

A planilha de verificação é utilizada para realizar cálculos independentes.

Atualmente possui verificações relacionadas a:

- flexão;
- armadura mínima;
- disposição das barras;
- espaçamento entre barras;
- comprimento de ancoragem;
- decalagem do diagrama;
- ancoragem de armadura positiva em apoio de extremidade;
- necessidade de grampos;
- esforço cortante;
- resistência da biela comprimida;
- espaçamento máximo de estribos;
- armadura de suspensão em apoios indiretos.

Enquanto os cálculos da planilha não forem reproduzidos e validados por
ferramentas próprias, seus resultados devem continuar sendo utilizados
como referência independente.

---

## 3. Unidade de revisão

A revisão é realizada viga por viga.

Normalmente são revisadas conjuntamente as vigas pertencentes a um mesmo
pavimento, pois as entregas podem ocorrer de forma parcial por pavimento.

Regiões críticas podem receber análise adicional durante o fluxo normal.

Casos especiais que exigem análise mais extensa podem ser separados para
avaliação posterior.

---

## 4. Sequência geral de revisão de uma viga

A sequência normalmente utilizada é:

1. verificar geometria;
2. identificar condições especiais, incluindo apoios indiretos;
3. verificar armaduras positivas de todos os vãos;
4. verificar ancoragem das armaduras positivas;
5. verificar armaduras negativas de todos os apoios;
6. verificar ancoragem e extensão das armaduras negativas;
7. verificar armaduras de cisalhamento;
8. verificar armadura de suspensão quando aplicável;
9. verificar outros detalhes especiais;
10. registrar as correções necessárias na prancha.

A sequência pode ser adaptada quando as características da viga exigirem.

---

## 5. Verificação da geometria

Antes de verificar as armaduras, comparar o detalhamento da viga com a
planta baixa estrutural ou com o modelo RVT.

Verificar:

- identificação da viga;
- seção de cada vão;
- mudanças de seção;
- comprimento dos vãos;
- identificação dos apoios;
- dimensões dos apoios;
- desníveis;
- continuidade com outras vigas;
- vigas apoiadas indiretamente;
- detalhes geométricos especiais.

Uma divergência geométrica deve ser identificada antes da verificação das
armaduras, pois pode alterar os dados utilizados nos cálculos.

Quando houver divergência entre fontes, não escolher automaticamente uma
delas como correta. Identificar a divergência e determinar qual representa
a geometria vigente do projeto.

---

## 6. Verificação das armaduras positivas

A verificação é realizada vão por vão.

### 6.1 Dados do detalhamento

Identificar na prancha:

- número de barras;
- diâmetro;
- número de camadas;
- quantidade de barras por camada;
- extensão das barras;
- forma das barras;
- condições de ancoragem nos apoios.

### 6.2 Dados para cálculo

Fornecer à ferramenta de verificação:

- largura da seção;
- altura da seção;
- fck;
- cobrimento;
- diâmetro dos estribos;
- número de barras por camada;
- diâmetro das barras.

### 6.3 Momento resistente

Calcular o momento resistente da configuração efetivamente detalhada.

Comparar:

`MRd >= MSd`

onde `MSd` é obtido da envoltória de momentos do modelo estrutural para a
região analisada.

Também verificar a condição de armadura mínima aplicável.

No procedimento atualmente utilizado, quando a armadura correspondente
ao momento mínimo não é atendida, também é avaliado o critério utilizado
por João de comparação com pelo menos duas vezes o momento solicitante.

Esse critério deve ser tratado como critério do procedimento de revisão,
e não atribuído automaticamente à NBR 6118 sem verificação normativa
específica.

---

## 7. Ancoragem da armadura positiva

Após validar a resistência à flexão, verificar a ancoragem das barras nos
apoios.

Em apoios de extremidade, utilizar:

- dimensão do apoio;
- número de barras que chegam ao apoio;
- diâmetro das barras;
- esforço cortante;
- momento positivo no apoio, quando houver;
- demais parâmetros requeridos pela ferramenta de verificação.

A ferramenta deve indicar se a ancoragem disponível é suficiente e se há
necessidade de grampos.

Quando houver necessidade de grampos, avaliar se outra configuração de
armadura longitudinal pode produzir uma solução mais eficiente e reduzir
ou eliminar os grampos.

Não considerar automaticamente que a ausência de grampo na prancha é um
erro. Primeiro determinar se o grampo é necessário.

---

## 8. Verificação das armaduras negativas

Após verificar todas as armaduras positivas, verificar as armaduras
negativas nos apoios.

Utilizar processo equivalente ao da flexão positiva:

- identificar a configuração detalhada;
- determinar o momento resistente;
- comparar com o momento solicitante;
- verificar armadura mínima quando aplicável;
- verificar disposição das barras;
- verificar espaçamento entre barras.

Em apoios intermediários, avaliar a possibilidade de escalonar as
armaduras quando isso produzir um detalhamento adequado e mais eficiente.

Quando houver mais de uma camada, analisar separadamente a contribuição
e a extensão de cada camada quando isso for relevante para o detalhamento.

---

## 9. Extensão e ancoragem das armaduras negativas

Verificar cada camada de armadura negativa separadamente quando houver
escalonamento ou múltiplas camadas.

A análise considera:

- diagrama de momentos;
- posição em que determinada parcela da armadura deixa de ser necessária;
- decalagem do diagrama;
- comprimento de ancoragem;
- condições de aderência;
- extensão efetivamente detalhada.

A verificação deve considerar o item 18.3.2.1 da NBR 6118:2023, conforme
o procedimento atualmente adotado.

Os valores de decalagem do diagrama e comprimentos de ancoragem são
atualmente obtidos através da planilha de verificação.

Os pontos de referência para início da ancoragem são determinados a partir
do diagrama de momentos do TQS.

Não inferir esses pontos apenas pelo máximo momento do vão. A distribuição
dos esforços ao longo da viga é necessária.

---

## 10. Verificação da armadura de cisalhamento

Após a análise das armaduras longitudinais, verificar os estribos.

Obter do modelo estrutural os esforços cortantes relevantes.

Fornecer à ferramenta de verificação:

- geometria da seção;
- fck;
- cobrimento;
- esforço cortante;
- número de ramos do estribo.

A ferramenta de verificação deve fornecer, conforme aplicável:

- arranjos possíveis para diferentes bitolas;
- espaçamento necessário;
- armadura mínima;
- espaçamento máximo;
- resistência da biela comprimida.

Verificar:

`VRd2 > VSd`

e comparar os espaçamentos calculados com os estribos efetivamente
detalhados.

Além da resistência, considerar a possibilidade física de montagem das
armaduras e concretagem da seção.

Quando houver diferentes regiões de estribos, analisar cada região
separadamente.

Não assumir que uma região com estribos diferentes corresponde
necessariamente a uma mudança na demanda de cisalhamento. Ela pode estar
associada a outro mecanismo, como armadura de suspensão.

---

## 11. Apoios indiretos e armadura de suspensão

Quando uma viga se apoia em outra viga, ocorre uma condição de apoio
indireto que deve ser identificada durante a revisão.

Nas pranchas do escritório, uma viga que se apoia na viga detalhada pode
ser representada na elevação através de um contorno retangular tracejado.

A identificação da viga apoiada deve ser confirmada pela planta baixa
estrutural ou por outra fonte geométrica quando seu nome não estiver
indicado diretamente no detalhe.

### 11.1 Identificação da armadura detalhada

Quando houver uma concentração localizada de estribos associada
graficamente à região de uma viga apoiada, essa armadura pode representar
a armadura de suspensão do apoio indireto.

A interpretação gráfica deve seguir as convenções registradas em
`beam-drawing-conventions.md`.

Distinguir sempre:

- existência do apoio indireto;
- existência de armadura de suspensão detalhada;
- necessidade calculada de armadura de suspensão;
- suficiência da armadura detalhada.

Essas quatro informações não são equivalentes.

### 11.2 Verificação da armadura de suspensão

Quando houver apoio indireto, avaliar a armadura de suspensão de acordo
com o procedimento adotado e com o item 18.3.6 da NBR 6118:2023.

Fornecer à ferramenta:

- reação da viga apoiada;
- parcela da reação que deve ser suspensa;
- geometria da região;
- comprimento disponível para distribuição da armadura;
- número de ramos considerado.

O comprimento de distribuição é relacionado à altura da viga que recebe
o apoio, conforme o procedimento utilizado na planilha.

A ferramenta retorna os arranjos possíveis de estribos para a suspensão.

Comparar o resultado com o detalhamento da prancha.

A existência de armadura de suspensão detalhada não demonstra que sua
quantidade seja suficiente.

Da mesma forma, a ausência de armadura de suspensão detalhada não
caracteriza automaticamente erro antes da avaliação da condição de apoio.

---

## 12. Continuidade entre vigas

Quando existir continuidade estrutural entre vigas com identificações
diferentes, essa continuidade deve ser considerada durante a revisão.

Verificar:

- continuidade das armaduras;
- compatibilidade das barras entre os elementos;
- ancoragens;
- interrupções inadequadas;
- mudanças de seção;
- detalhes necessários na região de transição.

Quando necessário, indicar graficamente na correção como as armaduras
devem continuar entre os elementos.

---

## 13. Pavimentos ou regiões simétricas

Quando existirem pavimentos ou regiões estruturalmente equivalentes,
procurar compatibilizar as armaduras de vigas correspondentes quando isso
for tecnicamente adequado.

Não forçar igualdade de detalhamento quando os esforços, geometrias ou
condições de apoio forem diferentes.

---

## 14. Problemas recorrentes

Durante a revisão, prestar atenção especial a:

- ancoragens inadequadas;
- interrupção inadequada de armaduras negativas;
- simplificações de detalhamento antieconômicas;
- armadura em excesso;
- grampos desnecessários;
- falta de grampos quando necessários;
- incompatibilidade entre seção detalhada e planta baixa;
- erros em mudanças de seção;
- falta ou insuficiência de armadura de suspensão;
- continuidade inadequada entre vigas;
- espaçamento inadequado entre barras;
- excesso de camadas;
- arranjos que dificultem a concretagem.

Essa lista deve ser ampliada conforme novos padrões de erro forem
identificados em revisões reais.

---

## 15. Registro das correções

As correções são normalmente indicadas diretamente no PDF da prancha.

Quando possível:

- indicar graficamente a solução correta;
- utilizar comentários curtos e objetivos;
- explicar o motivo quando necessário;
- evitar repetir longas explicações para erros recorrentes.

Quando um mesmo erro aparecer repetidamente, considerar que o problema
pode estar relacionado a:

- desconhecimento do critério;
- interpretação incorreta do padrão;
- procedimento de detalhamento;
- instrução insuficiente.

Nesses casos, além de corrigir a prancha, avaliar a necessidade de orientar
a pessoa responsável pelo detalhamento.

---

## 16. Princípio de revisão

Distinguir sempre:

1. o que foi detalhado;
2. o que o TQS calculou;
3. o que a verificação independente demonstra;
4. o que a norma exige;
5. o que representa uma preferência ou padrão de detalhamento do escritório.

Uma diferença entre essas fontes deve gerar investigação, não uma conclusão
automática de erro.

O objetivo da revisão não é reproduzir o detalhamento automático do TQS.

O objetivo é verificar se o detalhamento efetivamente produzido é
estruturalmente adequado, normativamente aceitável, executável e coerente
com o projeto.