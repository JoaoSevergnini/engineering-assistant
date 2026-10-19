# Etapa 7 — Relações entre ocorrências e contornos poligonais

A nova camada preserva integralmente as etapas anteriores e organiza **80 relações**:
39 candidatas automáticas, 37 interseções geométricas observadas e quatro relações
com confirmação humana de alcance local. As **44 composições indeterminadas continuam
indeterminadas**, porque nenhuma das confirmações disponíveis demonstra o alcance
global de uma relação. Não houve soma de aço ou verificação resistente.

Nos contornos, passaram de uma para **três lajes com candidato preliminar selecionável**:
L602, L604 e L606. Foi reconstruído também um candidato não retangular para L605,
mas sua forma de faixa perimetral em U sugere possível face de borda/viga; ele foi
mantido para revisão, **sem atribuição automática de armaduras a L605**.
Nenhum contorno foi confirmado pelo engenheiro ou substitui a planta de formas.

## 1. Auditoria, código e dados preservados

Inspecionados `distributed_regions.py`, `structural_regions.py`, seus runners,
testes e relatórios, as 35 regiões, 119 células e 77 blocos da Etapa 6, bem como as
entidades vetoriais/textuais e os grupos localizados anteriores.

Código novo: `occurrence_relations.py`, `polygonal_slabs.py`, `run_relations.py` e
`test_occurrence_relations.py`. Foram reaproveitados a partição existente,
`coverage`, `adjacent`, `line_geometry`, `distribution_axes`, os pares de função,
as evidências e a renderização anteriores. Não foram reescritos reconhecimento de
barras/faixas, inventários ou partição das armaduras. Vigas, pilares e Concretopy
não foram modificados.

O inventário completo acrescenta `occurrence_relation_analysis` e
`stage7_provenance`, mantendo todos os campos anteriores por igualdade exata.
Os IDs R/O/C e as coordenadas originais foram preservados. Novos IDs Q identificam
relações, P contornos candidatos e V blocos interpretados. Os hashes das entradas
estão no inventário. O PDF foi verificado antes/depois, sem escrita ou alteração:
`3eae69c055bc2b9e161c7767915f2682f9e7b53651dae073d046ecd0ddb45662`.

## 2. Modelo de relações

Os nós são ocorrências gráficas com referência à posição, ao ID textual e à região
individual. Sua identidade física permanece um campo de interpretação, não uma
consequência de igualdade de marca, diâmetro ou espaçamento.

Cada relação registra membros, tipo, geometria de validade, fontes/evidências,
orientação e camada dos membros, estado de confirmação, origem, e bloqueios de soma
resistente e de transitividade. Uma relação com múltiplas bases é um **hipervínculo**,
sem afirmar que todas as bases coexistem em toda a área do reforço.

| Tipo | Total | Observação |
|---|---:|---|
| REINFORCES | 7 | Cinco hipóteses globais condicionais + duas confirmações locais |
| LAPS_WITH | 25 | 24 candidatos + C092 confirmado localmente |
| GRAPHICAL_INTERSECTION | 38 | 37 interseções observadas + residual C073 confirmado |
| SAME_PHYSICAL_REPRESENTATION | 0 | Nenhuma identidade física compartilhada comprovada nesta prancha |
| UNDETERMINED | 10 | Repetições documentais em locais distintos sem identidade física estabelecida |

As 39 candidatas incluem os dez vínculos documentais UNDETERMINED. Uma mesma dupla
pode ter interseção gráfica observada e hipótese de traspasse; não são conclusões
físicas concorrentes já confirmadas. `GRAPHICAL_INTERSECTION` não significa erro de
desenho nem autoriza adição resistente.

Para REINFORCES são reutilizadas funções candidatas e cobertura da união de bases.
Para LAPS_WITH exige-se que a própria dupla apareça na evidência de interseção de
extremidades longitudinais, e não apenas numa célula com três armaduras onde outra
dupla apresenta esse indício. São preservados afastamento das barras, extremos,
orientação, extensão, diâmetros, espaçamentos, nominal C e contexto das células.
Esses candidatos não demonstram emenda ou comprimento normativo.

BASE/REFORÇO continuam evidências auxiliares associadas à geometria, sem condição
obrigatória. Cor não participa das decisões ou da geração dos IDs de relações.
Na API, SAME_PHYSICAL_REPRESENTATION só pode receber identidade física compartilhada
confirmada com evidência específica de revisão. Mesmas entidades vetoriais e
propriedades podem gerar uma hipótese de duplicação; ainda não confirmam a física.
Ambas as representações são mantidas e não se deduz identidade por repetição de N.

## 3. Confirmações humanas e propagação

| Caso | Ocorrências/regiões | Relação registrada | Alcance confirmado |
|---|---|---|---|
| C059 | O032/N15/R032 e O034/N14/R034 | REINFORCES | Polígono original C059 |
| C083 | O034/N14/R034 e O043/N13/R043 | REINFORCES | Polígono original C083 |
| C092 | O041/N1/R041 e O043/N13/R043 | LAPS_WITH | Polígono original C092 |
| C073 | O032/N15/R032, O036/N26/R036 e O043/N13/R043 | GRAPHICAL_INTERSECTION, significado residual | Polígono original C073 |

Fonte: confirmações de João registradas na Etapa 6. A atribuição direcional
reforço/base nesses casos usa as funções geométricas candidatas; não extrapola
uma confirmação humana de função global para todas as representações.

Uma relação só alcança uma célula se os membros efetivamente presentes forem
compatíveis e a interseção com o domínio de validade for positiva. Para REINFORCES,
o reforço e ao menos uma das bases têm de estar presentes; o registro da célula
lista apenas as bases ativas naquela sub-região. Isso permite R034 com as bases
R032 e R043 sem fingir que ambas existem em toda a envoltória de N14.

Uma classificação integral exige cobertura integral da célula pelo domínio da
relação. Alcance parcial é registrado geometricamente sem promover toda a célula.
Orientações ou camadas conhecidas incompatíveis bloqueiam relações de reforço ou
traspasse. Confirmações conflitantes produzem pendência na camada derivada, mantendo
intacta a classificação humana original da Etapa 6.

**Não há transitividade.** A reforça B e B tem traspasse com C não cria A reforça C.
A confirmação de C059/C083 não certifica automaticamente toda a união das bases
de R034, particularmente onde há três membros. C092 não é ampliado para outras
interseções de N1/N13. Em C073 mantém-se a região residual sem inventar quais
contribuintes devem substituí-la em uma composição resistente.

Resultado real: quatro confirmações preservadas, zero células novas classificadas
por propagação confirmada e zero conflitos materiais entre as confirmações atuais.
Os testes sintéticos mostram a propagação sobre múltiplas células dentro de um
domínio explicitamente confirmado; isso não comprova esse alcance no projeto real.

## 4. Reconstrução dos contornos

Foi instalado **Shapely 1.8.5.post1** apenas em `tmp/slab_spatial_deps`, compatível
com o Python 3.10 de 32 bits utilizado. O Python global não foi modificado. A versão
está fixada em `requirements-stage7.txt`. Foram usados noding por união geométrica,
`polygonize_full`, interseção e união, conforme o
[manual oficial do Shapely](https://shapely.readthedocs.io/en/1.8.3/manual.html).
Essa biblioteca resolve operações geométricas; não reconhece o significado estrutural.

O procedimento tem três frentes complementares:

1. **Faces com apoio de hachuras:** contatos repetidos de extremidades de hachuras
   com segmentos de contorno; fechamentos curtos precisam de duas faces já apoiadas,
   sem propagação em cadeia desse apoio. Foram encontrados 85 segmentos apoiados,
   que produziram 19 faces geométricas, uma ponta pendente e nenhum anel inválido.
2. **Perímetros sem hachura:** investigação de linhas ortogonais após excluir barras,
   faixas e líderes aceitos, e eixos com setas reconhecidos pelo código existente.
   Uma face precisa de contexto adicional de bordas apoiadas ou de uma linha explícita
   conectando a etiqueta da laje ao interior da face. Fechamento/ortogonalidade
   isolados são insuficientes. Essa rede produziu 87 faces e 108 pontas pendentes;
   isso não significa 87 lajes. As pontas expõem a incompletude da rede.
3. **Preservação de alternativas:** os contornos retangulares da Etapa 6 continuam
   candidatos independentes. Nenhum é descartado porque outra área é menor ou um
   texto está mais próximo. Um mesmo candidato contendo vários nomes é ambíguo.

As etiquetas externas são tratadas por segmentos que têm uma extremidade junto ao
texto e penetram no polígono com a outra extremidade no interior. As fontes reais
são D1886:0 (L604), D1887:0 (L606) e D1888:0 (L605). São evidências gráficas explícitas,
mas não prova de que a linha termina no domínio da laje em vez de uma viga.

Há ainda uma investigação alternativa de topologia com tolerância de 0,001 pt,
agrupando coordenadas sem encadeamento e preservando cada coordenada de origem e
deslocamento no inventário. Nesta prancha os 85 segmentos apoiados não precisaram
de ajuste: **zero movimentos**. A partição de armaduras não sofre snapping ou reparo.

Os limites de hachuras (3–45 pt), contato (0,25 pt), fechamentos curtos (até 30 pt),
conexão da etiqueta (4 pt) e apoio parcial de bordas são critérios experimentais
em unidades da prancha. Não são regras universais; outras escalas exigem avaliação.
Não se presume que centro de viga seja limite de laje.

### Resultado por laje

| Laje | h (cm) | Resultado da Etapa 7 |
|---|---:|---|
| L601 | 12 | Duas alternativas preservadas; não atribuída |
| L602 | 12 | Um candidato preliminar selecionável, herdado da Etapa 6 |
| L603 | 20 | Sem contorno suficientemente apoiado |
| L604 | 12 | Novo candidato fechado ligado ao nome por D1886:0 |
| L605 | 18 | Polígono em U; possível face de borda/viga, associação bloqueada |
| L606 | 12 | Novo candidato fechado ligado ao nome por D1887:0 |
| L607 | 20 | Quatro alternativas preservadas; não atribuída |
| L611 | 12 | Pendente |
| L612 | 12 | Pendente |

L604 e L606 têm áreas gráficas de aproximadamente 8.659,1160 pt² e 8.659,1164 pt².
L605 tem um candidato de 16.053,4977 pt², com preenchimento de cerca de 17,3% de
sua envoltória convexa. A concavidade de faixa estreita, combinada com etiqueta
externa que termina nessa faixa, acionou revisão de possível face perimetral.
Esse indício não rejeita lajes em U: mantém o candidato e impede sua seleção automática.

Foi corrigida durante a investigação uma seleção inicial demasiado permissiva de
L605 como laje. O inventário final distingue **quatro nomes com um candidato
geométrico único** de **três contornos preliminares selecionáveis**. Não se apresenta
o candidato não retangular de L605 como contorno estrutural validado.

## 5. Aberturas e associação às lajes

O backend preserva anéis internos de faces poligonais. Eles são identificados como
vazios gráficos cuja natureza estrutural ainda não está comprovada. As aberturas
da Etapa 4 ficam como referências auxiliares de interseção; não são subtraídas
automaticamente nem se presume inventário completo dos vazios.

Nos três contornos selecionáveis, há três ocorrências com associação preliminar:

- R002/O002/N28 — L602; interseção 20.849,0719 pt².
- R051/O051/N34 — L604; interseção 8.468,8084 pt².
- R052/O052/N34 — L606; interseção 8.468,8084 pt².

As duas ocorrências de N34 continuam locais e distintas. Interseções com contornos
concorrentes ou suspeitos são armazenadas como `ALTERNATIVE_ONLY_NOT_ASSIGNED`,
incluindo N40 com o candidato de L605. Nenhuma região foi atribuída a L603/L607 por
proximidade do nome. Não foi comprovada travessia de duas lajes na prancha real;
esse comportamento foi verificado apenas por teste sintético.

Essas operações não recortam fisicamente as barras nem convertem a área do polígono
em área de aço. Todos os contornos, inclusive os selecionáveis, continuam preliminares.

## 6. Contenção e R053/N40

Foram reaproveitadas as cinco verificações de contenção, agora vinculadas às relações
REINFORCES candidatas. R026/R027 são cobertos por duas bases candidatas cada;
R034 é coberto pela união de R032 e R043, e R035 pela união de R031 e R044.
As parcelas de cobertura são contadas uma única vez mesmo onde as bases se sobrepõem.

Para R053/N40, a relação com R050 continua **candidata**: 2.268,8070 pt² cobertos e
2.453,8824 pt² descobertos. Não há confirmação de sua função como reforço nem de
seu domínio estrutural. O novo candidato suspeito de L605 não resolve essa incerteza.
O inventário marca `function_confirmed=false` e `structural_insufficiency_proved=false`.
Não há classificação de erro estrutural ou sugestão de alteração da armadura.

## 7. Consolidação e comparação

As regiões derivadas só são unidas se houver borda comum com comprimento positivo,
mesmas identidades gráficas, relações aplicáveis e membros ativos, classe, orientação,
estado de validação e contexto preliminar de laje. Não há união por proximidade,
mesma marca ou contato pontual. O conjunto de polígonos resultante mantém referências
a todas as células e ocorrências; nenhuma contribuição é inventada ou somada.

| Indicador | Etapa 6 | Etapa 7 |
|---|---:|---:|
| Regiões individuais preservadas | 35 | 35 |
| Composições geométricas preservadas | 119 | 119 |
| Blocos derivados | 77 | 77 |
| Relações candidatas entre ocorrências | Não modeladas como vínculos | 39 |
| Relações com confirmação humana local | Quatro confirmações de células | 4 |
| Composições de sobreposição indeterminadas | 44 | 44 |
| Novas células classificadas por alcance confirmado | — | 0 |
| Lajes com contorno único preliminar selecionável | 1 | 3 |
| Lajes com contorno confirmado pelo engenheiro | 0 | 0 |
| Ocorrências associadas preliminarmente a contorno único | 1 | 3 |
| Lajes com contornos concorrentes | 2 | 2 |
| Candidato suspeito de face perimetral bloqueado | Não discriminado | 1 |
| Conflitos entre confirmações disponíveis | 0 | 0 |

O ganho principal é de modelo e rastreabilidade, não redução artificial de pendências.
Não foram criadas novas conclusões físicas para as 44 células sem confirmação de alcance.

## 8. Entregáveis e revisão visual

- [Inventário completo](inventario.json), [relações](relacoes.json) e [tabela](relacoes.md).
- [Regiões interpretadas](regioes_interpretadas.json), [blocos derivados](regioes_consolidadas.json).
- [Lajes/contornos/evidências](lajes.json), [contenção](contencao.json),
  [ambiguidades e pendências](ambiguidades.json) e [indicadores](indicadores.json).
- Mapas separados: [relações](relacoes.png), [base+reforço](base_reforco.png),
  [traspasses](traspasses.png), [residuais](residuais.png),
  [indeterminadas](indeterminadas.png), [contornos](contornos.png) e
  [associação às lajes](associacao_lajes.png).
- [Comparação Etapas 6/7](comparacao_6_7.png), com confirmações locais e contornos.
- Ampliações: [C059](C059_relacao.png), [C083](C083_relacao.png),
  [C092](C092_relacao.png), [C073](C073_relacao.png) e
  [R053/N40](R053_reavaliacao.png).

Azul identifica dados documentais/envoltórias; tracejado indica interpretação
candidata. As confirmações locais são destacadas por categoria, sem transformar
toda a envoltória em relação humana confirmada. No mapa de contornos, verde indica
candidato preliminar selecionável e laranja indica concorrência ou suspeita.

Foram inspecionados os contornos e a ampliação C073, com exame numérico do polígono
de L605, que levou ao bloqueio descrito acima. Revisão de apresentação não é uma
confirmação independente de contorno ou de novas relações. O PDF original é fundo
renderizado separado; as marcações são apenas nos PNGs.

## 9. Testes e conclusão técnica

Os testes novos separam casos sintéticos de regressões reais. Cobrem reforço sobre
uma base/união de duas, membros ativos em sub-regiões, traspasse e residual, domínio
parcial, três membros, incompatibilidade de direção/camada, conflito com confirmação
anterior, proibição de transitividade, identidade física com evidência específica,
repetição de marca em locais diferentes, polígonos côncavos/com anéis internos,
contornos concorrentes, etiqueta externa com líder, travessia de duas lajes,
determinismo, cor, preservação de todas as camadas e regressão L605 suspeita.
O resultado da suíte completa está em `testes.txt`.

Na prancha real, foi demonstrada a geração de vínculos com escopo e o reconhecimento
de dois novos contornos preliminares por evidência de líderes das etiquetas.
Não foi demonstrado alcance global de nenhuma das quatro relações humanas ou
contorno estrutural definitivo de uma laje não retangular. O teste sintético de
polígono em L e de vazios demonstra o backend geométrico, não confiabilidade universal.

Próxima etapa recomendada: confirmar explicitamente o alcance de relações inteiras
(especialmente R034 com R032/R043 e seus encontros de três membros), revisar as
hipóteses de emenda por dupla, conferir L604/L606 e esclarecer o término do líder
de L605. Obter a planta de formas para resolver L601/L603/L607/L611/L612, faces de
apoio, aberturas e camadas antes de autorizar qualquer composição resistente.

N38 permanece intocada: chamada original 6x3 Ø12,5 C=182, confirmação de quatro
conjuntos de três e divergência documental preservada. Não participa desta
contenção DISTRIBUTED. Não foram feitos cálculos resistentes, ancoragem normativa,
TQS, dimensionamento, otimização, redução de armaduras ou apontamentos de ATP.
