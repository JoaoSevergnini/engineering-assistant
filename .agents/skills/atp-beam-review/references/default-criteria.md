# Critérios padrão da ATP de vigas

Critérios decididos por João na ATP 25-208 S05 3PAV e adotados por ele como padrão do assistente em 09/11/2026. A origem de cada item está entre parênteses: decisão (D) ou adoção (A) registrada em `premissas.json` daquele pavimento.

Estes critérios valem em toda ATP de vigas, salvo instrução contrária de João no projeto. Não são decisões transplantadas de outro projeto (SKILL §1). Registrar em `premissas.json` de cada pavimento os critérios aplicados, com a origem "critério padrão (default-criteria.md)" e o alcance.

Alguns itens são critérios de João, e não exigências normativas. Eles aparecem identificados como tal e não devem ser atribuídos à norma.

## 1. Premissas padrão a confirmar no início

Na etapa 0, apresentar a João estas premissas com o valor padrão e registrar a resposta. Se não houver resposta, prosseguir com o padrão, identificado como tal.

| Premissa | Padrão |
|---|---|
| Coeficiente de majoração (D04) | γf = 1,4 uniforme (Sd = 1,4·Sk) em flexão, cortante e suspensão |
| Origem dos dados (D05, D11) | Esforços do TQS; geometria (seções, vãos, níveis) do detalhamento; a forma da revisão indicada é a referência da comparação; divergência forma × detalhamento vira apontamento GEOM |
| Série de esforços (D07) | VGESFS original, não a série corrigida por excentricidade do RELDTVGS |
| Furos (D14) | Fora do processo: seção plena nas verificações regionais; a conclusão não cobre furos nem os seus reforços, e a limitação aparece no relatório |
| Tolerância editorial (D13) | Ver §2 |

## 2. Tolerância editorial de 10% (D13, D02)

- Índice 100% < η ≤ 110% é tolerado somente no cálculo de armaduras: flexão (ηM), taxa de estribos (ηAsw) e suspensão.
- A tolerância não se aplica a biela, armadura mínima e geometria.
- Na seleção e na emissão, o item tolerado aparece com cor própria (âmbar, [reporting](reporting.md)). João decide se vai ao relatório.
- É critério editorial. A conclusão técnica não muda: o item continua "não atende" no registro interno.

## 3. Flexão

1. **Largura colaborante (D15):** usar o menor valor por vão entre B COLAB (VGESFS) e Mesa Final (RELDTVGS).
2. **Quando a mesa entra (D06, D16):**
   - A mesa só contribui quando está na zona comprimida.
   - Momento positivo: mesa só se o topo da laje for faceado com o topo da viga.
   - Momento negativo: mesa só se o fundo da laje for faceado com o fundo da viga (seção T espelhada no Concretopy).
   - A posição da mesa (superior ou inferior, um ou dois lados) segue o TIPO SECAO do TQS.
   - O faceamento é comprovado pelos níveis da forma. Sem comprovação, usar a seção retangular b_w × h e registrar a mesa como não considerada.
3. **Laje da mesa (D28):** conferir na forma se existe a laje que o TQS usa como mesa. Sem laje na forma, usar a seção retangular, mesmo que o TQS indique mesa.
4. **Mínimo sem demanda (D19, critério de João):** quando a armadura existente dá MRd ≥ 2·Md na região (equivalente a MRd/γf ≥ 2·Mk), o critério de armadura mínima não precisa ser atendido. O controle registra a dispensa e os dois valores. Base normativa não conferida.
5. **Quantidade divergente (D20):** vale a armadura que vai para fabricação, representada no rebatimento abaixo da elevação. A indicação divergente da elevação vira apontamento documental.
6. **Sem demanda do sinal (A18, A30):** o controle é NAO_SE_APLICA, com a comprovação registrada pela envoltória do TQS:
   - positivo de balanço sem Mk > 0 em nenhuma seção;
   - sub-região negativa sem barra negativa e com Mk,min ≥ 0 em todo o intervalo, por interpolação linear entre seções e sem extrapolar.

## 4. Cortante

1. **Ramo sem porta-estribo (D29):** ramo de estribo sem barra longitudinal no canto, no próprio corte, é não conformidade de detalhamento. O controle de cortante fica NAO_ATENDE por detalhamento. Asw/s e biela são registrados separadamente, mesmo quando atendem.
2. **Altura útil (A08):** d do cortante = o menor d entre as composições tracionadas presentes na faixa (positiva e negativas).
   - O d de cada composição é o centróide ponderado pelas quantidades, com as alturas do Concretopy (`calcular_alturas_uteis_camadas`).
   - Camada documental vazia na faixa (barra de 2ª camada sem barra de 1ª) preserva a posição física da 2ª camada.
   - Na ATP, este critério substitui a seleção `engineer_confirmed_shear_effective_depth_max_layers_v1` da [revisão de cortante](../../reinforcement-review/references/shear-reinforcement-review.md), que continua valendo para a revisão interna. Confirmado por João em 09/11/2026: na ATP vale o menor d.
3. **Arredondamento de desenho nas faixas (A24, A27):**
   - Junção ou sobreposição ≤ 1,5 cm entre faixas consecutivas segue a faixa vizinha; a sobreposição é cortada no ponto médio.
   - Trecho ≤ 6 cm entre a extremidade do domínio físico e a primeira ou a última faixa (cobrimento) segue a faixa vizinha.
   - Sub-região de até 3 cm, a até 6 cm de uma extremidade, criada pela partição em eventos de barra, segue a sub-região adjacente da mesma faixa quanto ao porta-estribo.
   - Lacunas maiores não são absorvidas: exigem leitura dirigida.

## 5. Suspensão

1. **Aplicabilidade (D21):**
   - A suspensão se aplica a todo apoio viga sobre viga.
   - Quando o fundo da apoiada fica abaixo do fundo da receptora, a ligação exige armadura de suspensão especial, calculada para 100% da reação e localizada exatamente no encontro entre as vigas.
   - Registrar os níveis e a tolerância usados na comparação dos fundos.
   - O método de verificação da armadura especial não é padrão: perguntar a João em cada projeto. No 25-208, a verificação ficou com ele (D27).
2. **Duas apoiadas no mesmo ponto, uma de cada lado da receptora (D22):** somar as duas reações na mesma região de suspensão.
3. **Regiões de encontros diferentes que se sobrepõem (D26):** somar as taxas de suspensão no trecho de sobreposição. Cada encontro conserva a própria região fora da sobreposição.
4. **Ponta de balanço (D23):** L = h/2, medido da face da extremidade do balanço para dentro do balanço.

## 6. Geometria e documentação

1. **Elemento em um só documento (D10):** elemento presente num documento (forma, detalhamento) e ausente no outro é inconformidade do relatório. Os controles resistentes que dependem do documento ausente ficam sem execução, com esse motivo.
2. **Identidade pela posição (D09):** a viga é identificada por apoios e posição. Título divergente na prancha vira apontamento documental.
3. **Vigas agrupadas (D17):** a segunda viga do grupo usa o mesmo detalhamento, com os esforços TQS próprios, quando:
   - o TQS confirma vãos e seções iguais (±2 cm);
   - a forma confirma os apoios.
   
   Complementa as [convenções de prancha](../../reinforcement-review/references/beam-drawing-convections.md) §11 e §14.
4. **Posições medidas no DXF (D18):** as posições longitudinais medidas no DXF do detalhamento (faces, limites de barras e faixas) valem como comprovação, desde que a escala seja conferida por textos de comprimento (por exemplo, comprimento da barra × escala = texto).
   - No `floor_review`, o fato entra como `DOCUMENTED_CONFIRMED`, com a natureza preservada na proveniência ("medida geométrica DXF, escala 1:n, não é cota explícita") e a referência a este critério.
5. **Apoio deslocado entre detalhamento e TQS (D25):** quando a seção terminal do TQS cai antes da face desenhada, de modo que o negativo do lado fica sem região de cálculo:
   - registrar a divergência como apontamento GEOM;
   - verificar com o máximo negativo do TQS no fim do vão contra as barras na face desenhada.
6. **Detalhamento desatualizado em relação à revisão da forma (D32, D34):** quando o detalhamento e o modelo não incorporam a revisão vigente da forma (seções, apoios):
   - Emitir um único apontamento GEOM, com a diferença de geometria e a indicação "as armaduras devem ser revisadas de acordo com a revisão correta".
   - As não conformidades de flexão, cortante, mínimo e suspensão do trecho não são apontadas separadamente.
   - Fazer uma avaliação de risco (sensibilidade não promovida a vigente) com a menor seção da forma no trecho e as mesmas barras, estribos, faces e esforços TQS.
   - O resultado vigente continua o do detalhamento.
7. **Troca de seção dentro do vão (A31, A32):** quando detalhamento e forma concordam numa troca de seção dentro do vão e o TQS usa seção única:
   - verificar flexão, mínimo e cortante por trecho, com a seção do trecho;
   - na suspensão, usar o h no ponto do encontro.
   - A seção do trecho é lida no contorno da elevação: par de horizontais cuja distância coincide (±1 cm) com um rótulo de seção do vão.
   - Assinalar esses vãos no inventário da etapa 0.
