# Etapa 8 — Reconhecimento automático de contornos complexos

**Foi recuperado automaticamente um candidato não convexo para L603**, a partir
das entidades vetoriais e das etiquetas documentais, sem ler as coordenadas da
referência no reconhecimento. O candidato apresenta **IoU de 97,69%** com a
digitalização da referência humana. A maior divergência exterior local é, porém,
**42,95 pt**; não se conclui validação automática por boa aparência ou boa IoU.

Os nove nomes de lajes têm um candidato topológico único neste procedimento.
Os outros oito contornos são geometricamente idênticos aos da revisão anterior.
L605 continua com suspeita de faixa perimetral, e todos os contornos automáticos
permanecem candidatos, sem autorização de uso resistente.

## 1. Auditoria e separação da referência

Foram inspecionados `polygonal_slabs.py`, `review_slab_contours.py`, as rotinas de
registro humano, inventários, testes e imagens anteriores. A imagem
`../lajes_l603_confirmada/L603_contorno_confirmado.png` foi examinada como referência
visual. Para os indicadores utilizou-se o polígono da digitalização que gerou essa
imagem; sua precisão métrica continua aproximada, conforme o registro anterior.

Novos módulos:

- `complex_slab_contours.py`: reconhecimento a partir dos dados vetoriais e
  inventário documental; não lê imagem, arquivo de referência ou coordenadas humanas.
- `contour_validation.py`: comparação geométrica posterior, sem retroalimentar
  seleção ou ajuste de candidatos.
- `run_complex_contours.py`: execução, auditoria comparativa, imagens e proveniência.
- `test_complex_slab_contours.py`: testes sintéticos e regressões reais separados.

Reutilizados seleção de entidades aceitas, reconhecimento de eixos/setas,
evidências de hachuras, blocos nome+espessura e apontadores documentais, operações
Shapely e renderização PyMuPDF existentes. Nenhuma dependência nova foi instalada.
Os módulos de vigas, pilares e Concretopy não foram alterados.

`candidatos_automaticos.json` é gravado **antes** de carregar a referência de
validação. A função `recognize(inventory, data)` não recebe referência. Os testes
também renomeiam L603 e invalidam metadados de contornos anteriores sem alterar
a geometria recuperada, e bloqueiam o registro humano durante o reconhecimento.
Não há condição especial por nome, ID ou vértices da L603 no algoritmo.

## 2. Causas dos erros anteriores

### Descarte de segmentos inteiros na borda da região de análise

A região de detalhamento vinha dos títulos/textos da prancha e terminava em
**x = 1884,4935 pt**. O critério antigo exigia que ambas as extremidades de cada
segmento estivessem dentro dessa janela.

O segmento **D1160:0**, de (1789,5599; 750,7600) a (1887,6000; 750,7600) pt,
está aproximadamente **96,83% dentro da janela**. Sua extremidade ultrapassa o
limite em apenas 3,11 pt. O critério descartava a linha completa, incluindo o
trecho que encontra a face vertical x = 1876,7999 pt e fecha o degrau direito de L603.
**D1162:0** apresenta a mesma condição na face paralela.

Isso não era ausência dessa informação no PDF. Era uma perda produzida pelo filtro
de contexto. A normalização de coordenadas ou fechamento de pequenas lacunas não
recuperava uma linha que já havia sido retirada da rede. A investigação inicial
de aproximações de extremidades não gerou uma solução suficiente e não foi
incorporada como remendo ao candidato entregue.

### Critério excessivo de hachura por perímetro

Mesmo numa face fechada, a regra anterior de exigir 20% de apoio de hachuras podia
descartar contornos com longos trechos de borda sem hachura. L603 apresenta cerca de
**18,77% de perímetro com esse apoio** no reconhecimento atual. Um percentual fixo
de hachura não determina se o restante de uma cadeia vetorial contínua é válido.

A nova camada mantém evidência positiva de hachura, cadeia fechada de segmentos
selecionados e vínculo com etiqueta/apontador; não promove isso a confirmação
estrutural. Faces sem evidência adicional não são aceitas apenas por fechamento.

### Etiquetas e perímetros não retangulares

Foi mantido o tratamento conjunto de nome e espessura introduzido na revisão,
necessário para os apontadores de L611/L612. Também foi mantida a capacidade
poligonal já disponível: o principal bloqueio de L603 não era incapacidade do
Shapely de lidar com não convexidade, mas a rede incompleta e os filtros.

## 3. Técnica aplicada

1. Selecionar entidades completas com pelo menos **80% do comprimento no contexto**.
   O limite é um parâmetro experimental de layout (`minimum_inside_fraction`),
   não tolerância estrutural. Linhas longas de quadro, tabela ou malha que apenas
   cruzam a janela são filtradas. Cada linha que cruza a janela fica auditada.
2. Preservar as coordenadas integrais dessas entidades. Não recortar a linha no
   limite textual e não inserir fechamentos artificiais.
3. Excluir barras, faixas e líderes aceitos e eixos de anotação reconhecidos. Uma
   linha com apoio independente de hachura pode ser mantida como borda candidata,
   com a evidência registrada; cor não é condição de identificação.
4. Formar o grafo planar por união e interseção dos segmentos, e recuperar suas
   faces fechadas. Conservar reentrâncias, pequenos recortes e anéis internos.
   Não usar retângulo envolvente, fecho convexo ou simplificação para construir
   a geometria. O fecho convexo serve somente ao indicador de concavidade.
5. Vincular faces ao texto documental interno ou ao apontador explícito do bloco
   nome+espessura. Hachura/contexto ou apontador constituem evidência adicional;
   fechamento isolado não basta. Múltiplas etiquetas/candidatos mantêm ambiguidade.

O candidato L603 tem **129 vértices exteriores**, incluindo nós colineares de
interseção, e **dois anéis internos gráficos**. Não foram introduzidos segmentos
de fechamento, snapping ou deslocamentos. A área gráfica é 745.214,1165 pt²;
não é área de aço, nem área física de laje definitivamente conferida.
Os anéis internos vêm da própria rede, não da subtração automática de aberturas
de um inventário presumido completo. Sua natureza estrutural exige conferência.

Uma entidade de barra que cruza a janela, D1543:0, também aparece na auditoria de
contexto, mas é removida pela identificação prévia de armadura antes da rede de
bordas. Preservar uma entidade no contexto não significa utilizá-la como perímetro.

## 4. Verificação da melhoria e correspondência geométrica

Uma execução de ablação aplica a mesma técnica com critério de contexto de 100%,
reproduzindo o descarte anterior. Nessa execução L603 permanece sem candidato;
com preservação de entidades cruzando a janela, aparece a face fechada. Isso
está documentado em `comparacao_etapas.json` e em teste de regressão real.

| Indicador de L603 | Resultado |
|---|---:|
| IoU, incluindo os anéis internos automáticos | 97,6941% |
| IoU considerando apenas perímetros exteriores | 97,7796% |
| Diferença relativa de área automática − referência | +0,5840% |
| Área de diferença simétrica | 17.333,5619 pt² |
| Distância de Hausdorff dos perímetros exteriores | 42,9541 pt |
| Perímetro automático na faixa de 8 pt da referência | 97,3035% |
| Perímetro da referência na faixa de 8 pt do automático | 99,2655% |

Esses indicadores medem **correspondência com uma digitalização aproximada da
imagem humana**, não taxa de acerto em projetos. A margem de 8 pt foi herdada da
avaliação da digitalização; não é um limite normativo, precisão de levantamento
ou tolerância de aceitação do algoritmo.

A maior divergência fica perto de x = 1540 pt, y = 484,6 pt, num recorte estreito
do topo direito. A rede automática acompanha um recorte que não foi desenhado
da mesma forma na referência simplificada. Não é possível atribuir a diferença
inteiramente ao algoritmo ou à digitalização humana sem revisão desse trecho.
O recorte **não foi removido para melhorar IoU**. Os dois anéis gráficos internos
também explicam parte da diferença, pois a referência anterior não confirmou
um inventário completo de aberturas.

## 5. Regressões e lajes identificadas

| Laje | Candidatos atuais | Comparação com a revisão anterior | Pendência |
|---|---:|---|---|
| L601 | 1 | Geometria exatamente preservada | Confirmar a face interna como limite estrutural |
| L602 | 1 | Geometria exatamente preservada | Confirmar limite estrutural |
| L603 | 1 | Antes não havia face automática | Rever recorte do topo direito, anéis e alinhamento da referência |
| L604 | 1 | Geometria exatamente preservada | Conferir domínio apontado pela etiqueta externa |
| L605 | 1 | Geometria exatamente preservada | Faixa em U: não decidir laje/viga pela forma ou pouca área |
| L606 | 1 | Geometria exatamente preservada | Conferir domínio apontado pela etiqueta externa |
| L607 | 1 | Geometria exatamente preservada | Confirmar faces e interfaces com L603 |
| L611 | 1 | Geometria exatamente preservada | Confirmar faixa e interface estrutural |
| L612 | 1 | Geometria exatamente preservada | Confirmar faixa e interface estrutural |

Oito geometrias preservadas são comparadas com `lajes_revisao_contornos`, a revisão
vetorial mais recente, não com os retângulos concorrentes históricos da Etapa 6.
Esses retângulos e os demais inventários anteriores continuam preservados.

**Zero etiquetas com ambiguidade topológica nesta execução não significa zero
ambiguidades de engenharia.** Todos os nove contornos são candidatos automáticos.
A confirmação humana anterior da topologia de L603 permanece na referência,
sem ser copiada automaticamente para a nova geometria recuperada.

As 35 regiões individuais, 119 células e relações/reforços/traspasses anteriores,
N26 e a inconsistência N38 estão intactos no inventário enriquecido. Não foi feita
nova composição resistente, redistribuição de barras ou associação por proximidade.

## 6. Artefatos para validação

- [Comparação referência/automático da L603](comparacao_L603.png).
- [Mapa de diferenças](diferencas_L603.png).
- [Maior divergência local](maior_divergencia.png).
- [Borda recuperada e limite antigo da janela](borda_recuperada.png).
- [Mapa dos nove candidatos](contornos_candidatos.png).
- [Candidatos automáticos independentes da referência](candidatos_automaticos.json).
- [Métricas e referência utilizada](comparacao_referencia.json).
- [Ablação e regressões por laje](comparacao_etapas.json).
- [Inventário enriquecido e proveniência](inventario.json).

As imagens foram examinadas visualmente, incluindo a borda direita recuperada e
o recorte de maior divergência. Azul identifica o candidato automático; vermelho
identifica a referência. Os hashes do PDF, dos dados vetoriais, do inventário de
entrada e da referência numérica/visual estão registrados nos artefatos apropriados.
O PDF original não foi modificado; as marcações são imagens auxiliares.

## 7. Testes, limitações e próxima etapa

A suíte completa passou: **151 testes em 79,615 s**, incluindo os 139 anteriores
e 12 novos. Os testes novos verificam entidade atravessando o contexto, ausência
de fechamento artificial, polígono não convexo e reentrância, rejeição de retângulo
de anotação ou de barras, reprodução do erro anterior, preservação exata das outras
oito lajes, métricas com divergência local, invariância de cor/ordem, independência
da referência e mudança do nome da laje sem mudança de geometria. Ver `testes.txt`.

O método atual ainda investiga bordas ortogonais. Contornos com trechos inclinados
ou curvos, textos sobre limites, novos padrões de hachura, cotas não reconhecidas
e bordas significativamente fora da janela exigem novos critérios e testes.
O parâmetro de 80% pode excluir uma entidade estrutural longa em outro layout;
não foi demonstrada generalização para outras pranchas/escritórios.

Recomenda-se revisar o recorte de maior divergência e as interfaces L603/L607,
conferir os dois anéis internos e confirmar a natureza de L605. A planta de formas
continua necessária para validar limites físicos e apoios antes de utilizar esses
domínios em verificações estruturais. Não houve cálculo de momento resistente,
ancoragem normativa, dimensionamento ou geração de apontamentos de ATP.
