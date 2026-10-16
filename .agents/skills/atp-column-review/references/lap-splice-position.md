# Posição geométrica dos traspasses em pilares

## Critério de revisão e seu alcance

João orientou conferir a prática usual de posicionar o traspasse acima do topo
da viga/laje de topo mais alto que efetivamente chega ao pilar, considerando
a etapa de concretagem documentada. Usar essa referência para
identificar situações a esclarecer e incoerências entre lances. Ela não é, por
si só, uma prescrição normativa consultada nem uma preferência interna que
possa reprovar automaticamente um ATP.

A referência correta é o **maior nível de topo**, não a maior altura de seção
de viga, a viga mais próxima em planta ou o nível principal do pavimento.
Escadas, patamares, vigas invertidas e desníveis podem mudar essa referência.

Esta etapa não verifica comprimento necessário de emenda, percentual de barras
emendadas, solicitações, confinamento ou resistência do nó. A posição acima do
topo não demonstra atendimento desses controles. Eventual exigência normativa
ou de projeto deve ter fonte, edição/revisão e interpretação próprias.

## Procedimento por encontro de lance e grupo de barras

1. Identificar cada viga/laje que chega fisicamente ao pilar e suas faces de ligação.
   Confirmar incidência pela forma/corte; não incluir elemento apenas adjacente
   nem excluir viga de escada ou patamar por não coincidir com o nível principal.
2. Registrar nível de topo de cada elemento e sua referência física. Se o desenho
   apresentar fundo ou eixo, converter para topo apenas com geometria documentada.
   Manter níveis originais e eventuais transformações de datum separados.
3. Calcular `z_topo_max = max(z_topo_elementos_incidentes)` depois de conciliar as
   referências altimétricas. Se algum elemento incidente tiver topo desconhecido,
   não apresentar o máximo entre as conhecidas como máximo definitivo.
4. Identificar o grupo de barras que termina e o que inicia, leitura das marcas,
   continuidade e zona efetiva de sobreposição. Uma linha de pavimento, ponta de
   uma barra ou comprimento total da marca não demonstra, isoladamente, o início
   e o fim do traspasse. Avaliar separadamente emendas escalonadas entre grupos.
5. Registrar `z_inicio_traspasse` e `z_fim_traspasse`, com fonte e confiança da
   interpretação. Dados não legíveis ficam nulos. Não inferir a zona completa
   apenas pela seta de uma anotação; distinguir informação do usuário da leitura
   independente das pranchas.
6. Registrar a comparação com o topo global e, havendo etapas documentadas,
   com a referência pertinente à etapa da emenda. Comparar
   `delta_inicio = z_inicio_traspasse - z_referencia_confirmada`. Resultado positivo:
   início acima; zero: coincidente; negativo: início abaixo. Registrar a diferença
   com unidade, sem inventar afastamento mínimo ou tolerância. Com as duas pontas
   conhecidas, verificar também se a zona inteira está acima, abaixo ou cruza o topo.
   Sem o fim, não afirmar que toda a emenda está abaixo nem que sua extensão atende.
7. Comparar lances vizinhos do mesmo pilar e casos equivalentes documentados.
   Se um usa o topo local mais alto e outro o plano nominal mais baixo, registrar
   a diferença de critério e solicitar justificativa/compatibilização. Um lance
   coerente com essa referência não valida automaticamente os demais.

## Registro mínimo

Adicionar o controle `posicao_traspasse` ao inventário de cada encontro com
emenda, inclusive a emenda inicial bloco/pilar quando incluída no escopo.
Usar no registro:

- vigas/lajes incidentes e etapas: identificação, topo, datum, documento/revisão/localização;
- maior topo confirmado e eventuais incidências/cotas pendentes;
- grupos/marcas de barras e início/fim da sobreposição, com evidências;
- diferença de nível do início e relação da zona completa com o topo;
- origem do critério: orientação de revisão, requisito de projeto ou norma
  efetivamente consultada; conclusão geométrica separada da adequação;
- comparação com outros lances e esclarecimento necessário.

No contrato de cobertura, manter leituras da forma em `dados_forma` e do
traspasse em `dados_detalhamento`. Para posições inferidas a partir de barras,
registrar a construção geométrica e a fonte, sem tratar inferência como cota
literal. Se a referência da emenda for fornecida pelo usuário, identificar essa
origem e manter pendente sua confirmação documental quando ainda não feita.

## Apontamento para análise

Preferir: “No encontro indicado, o início do traspasse está na referência X e o
topo da viga incidente Y está em Z, diferença de ... cm. No lance vizinho o
posicionamento adota o topo local mais alto. Favor esclarecer o critério de
localização da emenda e verificar/compatibilizar o detalhamento desse encontro.”

Não declarar descumprimento normativo ou ordenar deslocamento das barras sem
comprovar o requisito aplicável e avaliar os controles dependentes. A mudança
de posição pode exigir revisão de comprimentos, esperas e armadura transversal;
a posição geométrica isolada não define uma correção pronta para execução.

## Incidência de lajes e concretagem em etapas

Incluir lajes incidentes no levantamento dos topos; não incluir paredes,
reservatórios ou elementos apenas próximos por sua cota superior isolada.
Para concretagem em etapas, obter cortes/detalhes/plano que demonstrem a junta,
o limite da etapa e sua relação com o pilar e as barras. Em reservatórios, a
primeira etapa frequentemente alcança a laje de fundo, mas essa hipótese não
dispensa comprovação da solução do projeto.

Registrar o maior topo incidente global e a referência pertinente à etapa da
emenda em campos distintos. Não apontar como erro uma emenda abaixo do topo da
etapa seguinte sem avaliar a sequência de execução. Sem sequência comprovada,
manter adequação inconclusiva e solicitar detalhe, preservando a leitura geométrica.
Comparar início/fim da sobreposição com a referência comprovada da etapa; rever
comprimentos e costura próprios. Este critério de revisão de João não deve ser
atribuído à norma como proibição universal sem texto que a fundamente.
