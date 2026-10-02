# Convenções de leitura de pranchas de vigas

## 1. Objetivo

Este documento registra convenções utilizadas nas pranchas de
detalhamento de vigas do escritório.

Seu objetivo é auxiliar na interpretação das representações gráficas e
evitar que informações ausentes sejam tratadas incorretamente como
incertezas quando o padrão de detalhamento permite uma interpretação
confiável.

Estas convenções descrevem como interpretar a prancha.

Elas não determinam se a armadura representada está estruturalmente
correta.

---

## 2. Princípio geral

Durante a leitura da prancha, diferenciar:

### Informação explícita

Informação escrita diretamente na prancha.

Exemplos:

- identificação da viga;
- seção;
- número de barras;
- bitola;
- comprimento;
- espaçamento de estribos;
- cotas;
- identificação da posição.

Classificação sugerida:

`explicit`

### Informação interpretada graficamente

Informação obtida pela posição, representação ou associação gráfica dos
elementos.

Exemplos:

- barra localizada na face superior;
- barra localizada na face inferior;
- associação entre chamada e barra;
- associação entre corte e elevação;
- região de distribuição de estribos.

Classificação sugerida:

`graphically_interpreted`

### Informação interpretada pelo padrão do escritório

Informação que não está necessariamente escrita, mas pode ser determinada
a partir de uma convenção conhecida do detalhamento utilizado pelo
escritório.

Exemplos:

- ausência de indicação de segunda camada significando primeira camada;
- ausência de armadura de pele quando nenhuma chamada ou representação
  correspondente existe;
- ausência de grampo detalhado quando nenhuma chamada de grampo existe;
- contorno retangular tracejado representando uma viga apoiada;
- concentração localizada de estribos associada a uma viga apoiada
  representando armadura de suspensão.

Classificação sugerida:

`interpreted_by_office_standard`

### Informação incerta

Utilizar somente quando nem a informação explícita, nem a representação
gráfica, nem uma convenção conhecida do escritório permitirem uma
conclusão confiável.

Classificação sugerida:

`uncertain`

Não utilizar `uncertain` apenas porque determinada informação não está
escrita literalmente.

---

## 3. Armaduras longitudinais

As armaduras longitudinais devem ser interpretadas a partir da combinação
entre:

- chamada da posição;
- representação da barra;
- posição vertical no detalhe;
- cortes;
- cotas;
- indicação de camadas.

A classificação de uma barra como positiva ou negativa deve considerar
sua posição gráfica no detalhamento.

Não utilizar apenas:

- bitola;
- número da posição;
- ordem no quadro de aço;
- armadura calculada pelo TQS.

Como regra geral:

- armaduras representadas na região inferior correspondem às armaduras
  positivas;
- armaduras representadas na região superior correspondem às armaduras
  negativas.

Casos especiais devem ser avaliados individualmente.


---

## 4. Camadas de armadura

Quando uma armadura longitudinal não possuir indicação explícita de
segunda ou terceira camada, considerar que ela pertence à primeira camada,
desde que o corte e a representação gráfica sejam compatíveis com essa
interpretação.

Classificar essa informação como:

`interpreted_by_office_standard`

e não como informação explícita.

Quando existirem barras em outras camadas, o detalhamento possui indicação
específica de camada.

Podem aparecer indicações como:

- `2aCAM`;
- `3aCAM`;
- ou representação equivalente utilizada pelo escritório.

Exemplo:

`N5 4 Ø 12.5`
`(1 Ø 2aCAM)`

deve ser interpretado como:

- 4 barras Ø12,5 no total;
- 1 barra na segunda camada;
- 3 barras na primeira camada.

Os cortes também devem ser utilizados para confirmar a disposição das
barras.

Não determinar o número de camadas apenas pela quantidade total de barras.

Quando o corte mostrar uma única fileira de barras e não houver indicação
de camada adicional, considerar uma única camada.

---

## 5. Associação entre posições de armadura e regiões da viga

Uma posição de armadura longitudinal pode atravessar mais de um vão,
mais de um apoio ou participar de diferentes regiões de verificação.

Não associar obrigatoriamente uma posição de armadura a um único vão.

Distinguir:

- posição de armadura: barra ou conjunto de barras definido na prancha;
- extensão longitudinal: intervalo ao longo da viga em que a posição existe;
- seção de verificação: posição longitudinal em que se deseja determinar
  a armadura resistente;
- configuração resistente: conjunto de posições de armadura que atravessam
  determinada seção.

Para uma determinada coordenada longitudinal x, a armadura existente deve
ser obtida pela combinação de todas as posições de armadura cuja extensão
longitudinal contém x.

Exemplo conceitual:

- N2 existe entre x = a e x = b;
- N3 existe entre x = c e x = d.

Se uma seção x pertence simultaneamente aos intervalos de N2 e N3,
ambas as posições participam da configuração de armadura naquela seção.

A divisão da viga em vãos não deve interromper artificialmente uma posição
de armadura que atravessa um apoio.

Quando não for possível determinar com segurança a extensão longitudinal
de uma posição a partir da prancha, registrar essa informação como incerta
em vez de inferir uma coordenada não indicada.

---

## 6. Armadura de pele

Quando existir armadura de pele, ela deve aparecer identificada ou
representada no detalhamento.

A identificação pode ocorrer através de:

- indicação `PELE`;
- chamada específica;
- representação de barras longitudinais laterais no corte;
- outra indicação gráfica equivalente utilizada no padrão do escritório.

Exemplo:

`N8 2x3 Ø8`

associado à indicação `PELE` deve ser interpretado como:

- armadura de pele;
- 3 barras em cada face lateral;
- 6 barras no total por viga.

Quando:

- não existir chamada de armadura de pele; e
- o corte não apresentar barras longitudinais laterais intermediárias,

considerar:

`skin_reinforcement_detailed = false`

Essa conclusão se refere exclusivamente ao que está detalhado.

Não concluir a partir disso que a armadura de pele não seja necessária.
A necessidade deve ser determinada durante a verificação estrutural e
normativa.

---

## 7. Grampos de ancoragem

Quando existirem grampos adicionais para ancoragem das armaduras
longitudinais, eles devem possuir representação ou chamada específica no
detalhamento.

Quando nenhuma representação correspondente existir, considerar:

`anchorage_staples_detailed = false`

Isso significa:

"não existem grampos detalhados na prancha".

Não significa:

"grampos não são necessários".

A necessidade de grampos deve ser determinada posteriormente durante a
verificação da ancoragem da armadura positiva no apoio.

---

## 8. Representação de vigas apoiadas

Na elevação de uma viga, contornos retangulares tracejados representam
vigas que se apoiam na viga detalhada.

Esses elementos indicam regiões de apoio indireto.

Quando houver mais de uma viga apoiada, podem existir múltiplos contornos
tracejados ao longo da elevação.

Interpretar:

`dashed_beam_outline = indirect_supported_beam`

ou representação equivalente na estrutura de dados utilizada.

A posição longitudinal do contorno indica aproximadamente a região em que
a reação da viga apoiada é transferida para a viga detalhada.

O contorno tracejado identifica a existência da viga apoiada, mas não
necessariamente sua identificação.

Quando o nome da viga apoiada não estiver indicado no detalhe, sua
identificação deve ser obtida ou confirmada através de:

- planta baixa estrutural;
- modelo RVT;
- modelo estrutural;
- outra fonte geométrica confiável.

Não atribuir automaticamente um nome à viga apoiada somente a partir da
posição do contorno tracejado.

---

## 9. Apoios indiretos e armadura de suspensão

Quando uma viga representada por contorno retangular tracejado se apoia na
viga detalhada, existe uma condição de apoio indireto.

A existência do apoio indireto e a existência de armadura de suspensão
devem ser tratadas como informações relacionadas, porém distintas.

### 9.1 Identificação da armadura de suspensão

Quando houver uma concentração localizada de estribos associada
graficamente à região de uma viga apoiada representada por contorno
tracejado, essa armadura deve ser interpretada como armadura de suspensão.

Essa armadura pode possuir:

- bitola diferente dos estribos gerais;
- espaçamento diferente;
- quantidade específica;
- região de distribuição própria.

Exemplo observado no padrão do escritório:

uma região localizada de estribos `N7 Ø6.3 c/15`, posicionada junto ao
contorno tracejado de uma viga apoiada, representa armadura de suspensão.

Quando a função não estiver escrita literalmente, mas a associação gráfica
com o apoio indireto estiver clara, classificar como:

`interpreted_by_office_standard`

e registrar:

`suspension_reinforcement_detailed = true`

### 9.2 Associação espacial

A armadura de suspensão deve ser associada ao apoio indireto pela
proximidade e correspondência gráfica entre:

- posição do contorno tracejado;
- região de distribuição da armadura transversal;
- chamadas e cotas da região.

Não associar automaticamente uma região especial de estribos a todos os
apoios indiretos existentes na viga.

Cada apoio indireto deve ser analisado individualmente.

Pode existir apoio indireto sem que uma armadura especial de suspensão
esteja claramente detalhada.

### 9.3 Limite da interpretação documental

A identificação de uma armadura como armadura de suspensão significa
somente que essa é a função atribuída à armadura representada.

Não significa que:

- sua área seja suficiente;
- seu espaçamento seja adequado;
- seu comprimento de distribuição seja adequado;
- toda a reação esteja corretamente suspensa.

Essas verificações pertencem à etapa de revisão estrutural.

Da mesma forma:

`suspension_reinforcement_detailed = false`

não significa automaticamente:

`suspension_reinforcement_required = false`

A necessidade deve ser verificada separadamente.

---

## 10. Estribos

A leitura dos estribos deve procurar identificar:

- posição;
- bitola;
- espaçamento;
- quantidade;
- região de distribuição;
- número de ramos quando puder ser determinado;
- mudanças de espaçamento;
- detalhes especiais de forma;
- possível função especial.

Uma chamada como:

`N6 39 Ø5 C/14`

deve ser interpretada de acordo com o padrão gráfico da prancha,
distinguindo:

- posição: N6;
- quantidade: 39;
- bitola: 5 mm;
- espaçamento: 14 cm.

Quando houver mais de uma região de estribos, manter as regiões separadas.

Não combinar automaticamente regiões com espaçamentos diferentes.

Uma região localizada de estribos diferente dos estribos gerais não deve
ser automaticamente interpretada como consequência de maior esforço
cortante.

Verificar se a região está associada a:

- apoio indireto;
- armadura de suspensão;
- mudança de geometria;
- outro detalhe especial.

---

## 11. Apoios principais

Identificar os apoios principais utilizando conjuntamente:

- elevação da viga;
- nomes indicados;
- cotas;
- posição relativa;
- planta baixa estrutural, quando disponível.

Quando uma prancha apresentar vigas agrupadas, como:

`V501=V503`

podem aparecer simultaneamente nomes correspondentes aos apoios das duas
vigas.

Exemplo:

`P2A/P2B`

pode representar apoios correspondentes às vigas agrupadas.

Não associar automaticamente um dos nomes a uma viga específica apenas
pela ordem de escrita quando a prancha não permitir essa associação.

Quando necessário, utilizar a planta baixa ou outra fonte geométrica para
resolver a correspondência.

---

## 12. Geometria da viga e regiões de distribuição de armaduras

Não utilizar automaticamente o comprimento de uma região de distribuição
de estribos como comprimento geométrico do vão.

Distinguir:

- geometria estrutural da viga;
- distância entre faces dos apoios;
- distância entre eixos dos apoios;
- região de distribuição de estribos;
- extensão das armaduras longitudinais;
- regiões de armaduras especiais.

Quando uma cota associada à distribuição de estribos coincidir graficamente
com as faces dos apoios, essa informação pode auxiliar na reconstrução da
geometria da viga.

Nesse caso, a geometria obtida deve permanecer identificada como informação
derivada da interpretação gráfica, e não como dimensão geométrica
explicitamente indicada na prancha.

Quando houver regiões diferentes de distribuição de estribos dentro de um
mesmo vão, essas regiões não devem ser interpretadas como vãos distintos.

Da mesma forma, armaduras de suspensão, mudanças de espaçamento de estribos
ou outras regiões especiais de detalhamento não alteram, por si só, a
geometria estrutural da viga.

---

## 13. Vigas apoiadas indiretamente e armadura de suspensão

Na elevação do detalhamento de vigas, elementos retangulares verticais tracejados
que interceptam a viga principal representam vigas que se apoiam indiretamente
sobre a viga detalhada.

Esses elementos não devem ser interpretados como apoios principais da viga
detalhada.

Quando houver uma região localizada de estribos associada espacialmente a uma
dessas vigas apoiadas, essa região pode representar armadura de suspensão.

A associação deve considerar conjuntamente:
- a presença da viga apoiada indicada pelo contorno tracejado;
- a posição longitudinal da região localizada de estribos;
- a correspondência espacial entre ambos.

Quando essa correspondência puder ser estabelecida de forma inequívoca no
desenho, classificar a região como armadura de suspensão e associá-la ao
respectivo apoio indireto.

Não classificar uma região como armadura de suspensão apenas por apresentar
bitola ou espaçamento diferente dos demais estribos.

Quando a correspondência espacial não puder ser determinada com segurança,
manter a função como indeterminada.

---

## 14. Vigas agrupadas

Uma chamada como:

`V501=V503`

indica que as vigas compartilham o detalhamento apresentado.

Quando o quadro de aço apresentar uma multiplicidade para o grupo, as
quantidades totais podem representar mais de uma viga.

Não atribuir automaticamente a uma única viga a quantidade total
multiplicada do quadro.

Para interpretar uma viga individual, priorizar as chamadas locais do
detalhamento.

As diferenças de identificação dos apoios entre as vigas agrupadas devem
ser resolvidas através da geometria do projeto quando necessário.

---

## 15. Cortes

Os cortes devem ser utilizados para complementar a leitura da elevação.

Eles podem ajudar a identificar:

- quantidade de barras por fileira;
- número de camadas;
- posição das barras;
- armadura de pele;
- geometria dos estribos;
- disposição física das armaduras.

Um corte representa uma região específica da viga.

Não assumir que todos os cortes representam todas as regiões da viga.

Quando houver mudança de armadura ao longo da viga, verificar a posição
do corte antes de utilizá-lo para interpretar outra região.

Exemplo:

um corte pode apresentar quatro barras superiores em determinada região,
mesmo que existam armaduras adicionais próximas aos apoios que não
atravessem a posição daquele corte.

---

## 16. Coordenadas longitudinais

Quando for útil para estruturar os dados da prancha, pode ser definido um
sistema de coordenadas longitudinal ao longo da viga.

Uma convenção possível é:

- origem `x = 0` na face interna do apoio esquerdo;
- valores positivos no sentido do apoio direito;
- valores negativos para barras que penetram no apoio esquerdo.

Essa coordenada pode ser utilizada para representar:

- início de barras;
- fim de barras;
- regiões de estribos;
- posição de apoios indiretos;
- regiões de armadura de suspensão;
- posição de cortes.

As coordenadas somente devem ser registradas quando puderem ser obtidas
de forma confiável através das cotas e da representação gráfica.

Não assumir espaçamentos ou posições não cotadas apenas para completar o
modelo de dados.

---

## 17. Ausência de representação

Durante a leitura da prancha, diferenciar:

`não identificado`

de:

`não detalhado`.

Quando o padrão do escritório exigir representação explícita de um
elemento quando ele existe, sua ausência pode ser utilizada para concluir
que o elemento não foi detalhado.

Exemplos atualmente conhecidos:

- armadura de pele;
- grampos adicionais;
- armadura de suspensão;
- camadas adicionais.

Essa conclusão se refere somente ao conteúdo da prancha.

Nunca transformar automaticamente:

`não detalhado`

em:

`não necessário`.

---

## 18. Informações que não devem ser inferidas

Não inferir sem evidência suficiente:

- necessidade estrutural de uma armadura;
- condição de vínculo do modelo;
- esforços solicitantes;
- comprimento de ancoragem necessário;
- necessidade de grampos;
- necessidade de armadura de suspensão;
- necessidade de armadura de pele;
- armadura mínima;
- momento resistente;
- capacidade ao cisalhamento;
- suficiência de uma armadura de suspensão;
- identidade de uma viga apoiada quando ela não estiver indicada ou
  confirmada por outra fonte.

Essas informações pertencem à etapa de verificação ou à compatibilização
com outras fontes e não à leitura documental da prancha.

---

## 19. Evolução das convenções

Este documento deve evoluir a partir de exemplos reais.

Quando uma nova prancha apresentar uma representação ainda não
documentada:

1. identificar como João interpreta essa representação;
2. verificar se é uma convenção recorrente do escritório ou um caso
   específico;
3. registrar a convenção somente quando houver confiança suficiente;
4. adicionar exemplos quando eles ajudarem a evitar ambiguidades.

Não transformar uma característica observada em uma única prancha em
regra geral sem confirmação.

Quando uma interpretação tiver sido confirmada por João como padrão do
escritório, ela pode passar a ser utilizada nas análises seguintes como
`interpreted_by_office_standard`.