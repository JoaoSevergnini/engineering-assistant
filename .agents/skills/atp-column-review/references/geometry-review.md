# Geometria e níveis dos pilares

## Preparar a comparação

- Identificar conjunto recebido, emissões, revisões e recortes utilizados.
  Preservar originais e histórico; anotação de revisão não comprova nova emissão.
- Definir o escopo físico: pavimentos, trechos entre referências, blocos/fundação,
  transições, ligações e prolongamentos. Se trabalhar inicialmente apenas entre
  pavimentos, declarar a exclusão dos trechos de fundação no resultado.
- Inventariar as ocorrências a partir **das formas e do detalhamento**, conciliando
  as duas listas. Um pilar presente só em uma fonte é uma ocorrência a resolver,
  não uma exclusão silenciosa. Desdobrar cada identificação de grupos repetidos;
  quantidade contraditória no título permanece pendente.
- Construir a matriz de controles esperados antes de atribuir resultados.
  Para os campos e o controle determinístico de cobertura, ler
  [Registro e cobertura](coverage-register.md).

## Ler e confrontar cada pilar e trecho

1. **Seção do trecho correto.** Distinguir seção que chega à forma, seção superior
   `(sup)`, nascimento e morte. Ler o contorno e as dimensões do concreto;
   dimensões de estribos não são dimensões do pilar. Comparar orientação e faces
   quando influírem na correspondência; não tratar rotação/espelhamento como
   equivalente sem comprovar a convenção do desenho. Em seções especiais,
   conferir raios, cotas parciais e dimensões totais.
2. **Referências de nível.** Identificar acabamento, plano estrutural, topo/fundo
   de viga/cinta, patamar e nível local de nascimento/término. Usar a referência
   física correspondente ao trecho; não substituir níveis locais pelos principais.
3. **Mudança de referência global.** Registrar origem e confirmação da diferença.
   Manter o valor original e o transportado em campos separados. Uma translação
   constante pode explicar níveis principais e coincidir numericamente, mas não
   comprova desníveis locais revisados nem corrige as pranchas recebidas.
4. **Comprimentos.** Separar: diferença calculada entre referências, cota direta
   escrita do lance, extensão total/parcial e comprimento de barra. Confrontar
   a cota direta com os níveis do próprio detalhe e com os níveis correspondentes
   da forma. Sem leitura da cota direta, registrar esse controle como não examinado
   ou pendente; não preencher a cota com o resultado da subtração. Uma cota parcial
   até o pavimento não aprova o término integral.
5. **Transições e términos.** Verificar referência e trecho da mudança de seção,
   deslocamento das faces, morte parcial e porção que continua dentro/acima de
   vigas. Se a ligação ou referência não estiver definida, manter pendente apenas
   o controle dependente e seguir com os demais pilares/controles.


6. **Posição dos traspasses.** Em cada encontro de lance, identificar as vigas
   que efetivamente chegam ao pilar e seus níveis de topo, inclusive vigas de
   escada/patamares e desníveis. Confrontar o início e o fim da sobreposição das
   barras com o maior topo incidente; não usar automaticamente o nível nominal
   do pavimento. Ler [Posição dos traspasses](lap-splice-position.md)
   para registrar a zona de emenda, critério de localização e comparação entre
   lances. Posição abaixo do maior topo é um alerta para análise e esclarecimento,
   não uma infração normativa automaticamente demonstrada.

Registrar a leitura de cada fonte independentemente. Não preencher a seção,
nível ou cota da forma copiando o valor esperado do detalhamento; localizar pelo
valor esperado é diferente de confirmar a leitura. OCR é auxílio de localização
ou extração preliminar, não evidência suficiente de um apontamento. Confirmar
visualmente os dados utilizados e ampliar novamente cotas pequenas/ambíguas.
Um erro de leitura corrigido deve atualizar matriz, apontamento e contexto;
preservar o histórico sem perpetuar a conclusão descartada.


## Término das barras e dependências de nível

Em cada término ou morte parcial, identificar por grupo/marca quais barras
continuam e quais terminam; registrar o topo físico das barras separadamente
do topo do concreto, do nível de pavimento e da cota direta do lance. Relacionar
cada grupo à porção da seção e à região/legenda da forma correspondente.
Se o controle exigir cobrimento, ancoragem ou comprimento desenvolvido,
consultar seu requisito próprio; a comparação geométrica de níveis não os aprova.

Conferir as notas de corte/ajuste conforme a forma e sua abrangência efetiva.
Uma nota existente para um grupo não resolve outro grupo nem outro pilar por
analogia. Ausência de indicação necessária é apontamento documental distinto
de insuficiência resistente demonstrada.

Ao mudar uma referência, confrontar em conjunto níveis das fontes, diferença
calculada, cota do lance, término dos grupos e comprimentos das marcas.
Uma cota pode estar correta apesar do rótulo de nível errado; outro caso pode
exigir corrigir ambos. Registrar somente as alterações comprovadas e as
informações que o projetista precisa rever, sem gerar comprimentos de barras
por subtração isolada. Não adotar níveis divergentes do detalhe para validar a
correção proposta a partir das formas.

Comparar casos fisicamente equivalentes quanto ao controle em análise para
identificar incoerência de critérios. Equivalência de níveis e ligações não
implica mesma bitola, área de aço ou solicitação, e não autoriza padronização.

Distinguir incoerência representada de dúvida efetiva de execução. Registrar
o julgamento do engenheiro sobre incluir ou não um apontamento no relatório,
com motivo, sem apagar a leitura conflitante nem presumir convenção comprovada.
A decisão de não apontar um caso específico não é dispensa geral de conferir
orientação ou condição resistente em outros casos.

## Presença documental nos dois sentidos

Confrontar forma → detalhe e detalhe → forma por ID, pavimento e trecho. Registrar
pilar sem detalhamento correspondente e detalhe sem ocorrência na forma vigente.
Antes de apontar, esclarecer nascimento/morte, transição, divisão entre pranchas
e revisão. Multiplicador deve corresponder aos IDs físicos das formas, não à
quantidade de nomes extraída do título por algoritmo.
