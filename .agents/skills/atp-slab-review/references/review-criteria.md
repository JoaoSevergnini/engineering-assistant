# Critérios de revisão de flexão de lajes

Procedimento de engenharia para execução assistida ou por ferramenta aplicável,
não catálogo de verificadores automáticos já implementados. Registrar resultado,
execução, evidências e origem do critério conforme [contratos](contracts.md).

## Origem e controles esperados

| ID | Controle | Unidade e dados principais |
|---|---|---|
| G01 | Identidade, contorno, espessura e nível: forma × armadura | Laje/zona; par de fontes e datum |
| G02 | Apoios, encontros e aberturas documentais | Encontro/abertura; faces e fontes |
| A01 | Cobertura positiva nas duas direções | Laje/direção; domínio e armaduras |
| A02 | Resistência e solicitações de flexão | Região/direção/face; seção, aço e diagrama |
| A03 | Negativa de borda sem continuidade | Borda/laje; As,min e vão livre |
| A04 | Negativa sobre viga entre lajes com positivo no apoio | Apoio/lado; As,min, vão e momento |
| A05 | Continuidade positiva | Encontro/conjuntos; demanda, geometria e Lb |
| A06 | Prolongamento/interrupção positiva e negativa | Conjunto/extremidade/ramo; demanda local e remanescente |
| A07 | Encontro com desnível e remissões | Encontro; níveis, esforços e detalhes |
| A08 | Reforços e detalhes de aberturas | Abertura; forma, armadura e detalhe genérico |

Abrir esses controles conforme o escopo; não os retirar da matriz porque faltam
dados. Desdobrar direção, lado ou controle de área/comprimento quando seus
resultados forem independentes.

As regras A01 e A03–A06 abaixo são critérios de revisão fornecidos pelo escritório
para esta skill. Não atribuí-los automaticamente à NBR 6118. Requisito normativo
exige norma/edição/formulação efetivamente consultadas; item não conhecido fica
pendente, sem inventar referência. Informações do projeto, software e hipóteses
devem ter registros próprios. O texto normativo não foi novamente consultado
nesta elaboração documental.

As,min permanece dependente do enquadramento e da norma aplicável comprovada,
ou de valor fornecido pelo engenheiro com origem explícita. Não substituir por
mínimo de vigas nem adotar um percentual universal sem fonte.

## A01 — Cobertura das positivas

Verificar toda a área estrutural da laje nas duas direções, independentemente da
magnitude e do sinal dos momentos. Excluir somente aberturas confirmadas do
domínio correspondente; apoiar a distinção laje/apoio/vazio nas formas.

Comparar domínio com regiões comprovadas de armadura, diferenciando cobertura
documental, falha de extração, abertura, detalhe especial, ausência comprovada e
informação inconclusiva. Lacuna entre polígonos extraídos é candidata à conferência,
não FAIL automático. Procurar chamadas e detalhes antes de concluir falta.

## A02 — Resistência à flexão e indicadores

Compatibilizar a solicitação local com a composição física da região/direção/face,
h, materiais, cobrimento e posição das barras. Região negativa exige resistência
compatível com sua demanda; os critérios mínimos de borda não a substituem.

Utilizar Concretopy quando seu domínio representar o arranjo. Conservar inputs,
largura b, As por metro, centros por família, resultados brutos e diagnósticos.
Arranjo equivalente só é admissível com justificativa das hipóteses, incluindo
escoamento das famílias reais; equivalência do resultante e do braço não prova
automaticamente equivalência de ductilidade e de todos os diagnósticos.

Comparar na base de cálculo aplicável; apresentar Mk e MRd/γf como resistência
equivalente, com γf comprovado e γc/γs preservados. Esta equivalência requer
Sd=γf·Sk demonstrável; combinações com fatores diferentes podem exigir retorno à
origem. Sem base compatível, não declarar suficiência. A geometria do DXF não
determina se o esforço é característico ou de cálculo.

Para lajes, apresentar normalmente tf·m/m; não confundir com momento total em
tf·m. Converter resultado de uma faixa de largura b para a largura de referência
correspondente antes da comparação. Seguir
[apresentação de esforços](../../../../profile/force-presentation.md).

### Dois indicadores por região, direção e sinal relevante

Para cada linha distinta i que atravessa a região, recortar o domínio da linha
pela região e obter p_i = máximo de |M| do sinal relevante nesse recorte.
Conservar o valor original com sinal e a posição do pico. Vários segmentos ou
interseções desconectadas da mesma linha contribuem uma única vez pelo maior
pico, sem duplicação.

- Indicador 1: média aritmética Σp_i/n das n linhas válidas, sem ponderação por
  comprimento ou área.
- Indicador 2: média aritmética dos três maiores p_i de três linhas distintas.
  Se n<3, deixar esse indicador indisponível e informar n; não renomear a média
  de uma ou duas linhas como média de três.
- Diagnóstico: picos individuais, IDs das linhas, posições, máximo absoluto,
  linhas esperadas/avaliadas e lacunas.

Uma linha integralmente conhecida no recorte, sem momento do sinal relevante,
pode contribuir zero somente se essa condição estiver comprovada. Linha não
extraída, identidade ambígua ou trecho relevante faltante não recebe zero.
Nesse caso, declarar indicador parcial do subconjunto conhecido ou indisponível,
indicando o denominador e a limitação; não apresentá-lo como cobertura integral.

As médias são indicadores de análise, não comprovação normativa universal.
Média inferior à resistência não elimina um pico local superior; conservar esse
alerta para avaliação do engenheiro. A ausência de diagrama não é momento nulo.
Para interrupções, empregar a distribuição local de A06.

## A03 — Negativas em bordas externas ou sem continuidade

Mesmo sem momento negativo solicitante comprovado, verificar:

- Área pelo critério do escritório: pelo menos 0,67 As,min.
- Extensão para dentro da laje: Lext = 0,15 × menor vão livre global da laje,
  medida a partir da face do apoio.

Obter o vão entre faces das vigas de apoio, não entre eixos, e não usar apenas
o menor trecho local de uma região de armadura. Sem vão/face ou As,min comprovados,
manter somente os subcontroles dependentes pendentes. Se houver negativo,
verificar também A02; se a demanda for desconhecida, não presumir que ela inexiste.

## A04 — Negativas sobre vigas entre duas lajes

Quando houver momento positivo no apoio entre lajes, mesmo sem negativo,
verificar negativa de pelo menos As,min integral pelo critério do escritório.

Calcular Lext=0,15×menor vão livre global individualmente para cada laje.
Medir a extensão de cada lado a partir da face do apoio voltada à respectiva
laje; vãos diferentes podem resultar em extensões diferentes. Registrar área
e extensão de cada lado separadamente. Demanda negativa existente exige A02.

## A05 — Continuidade das positivas nos apoios

Quando houver transmissão de momento positivo entre lajes adjacentes, verificar
continuidade resistente. Conjuntos iguais: preferir armadura contínua.
Conjuntos diferentes: admitir prolongamento de um deles, normalmente o menor
que, isoladamente, seja suficiente à solicitação correspondente.

Critério do escritório: comprimento físico comum de sobreposição ≥ 2 Lb.
Não confundir comprimento comum com soma das penetrações individuais.
Utilizar o comprimento básico de ancoragem, sem redução As,calc/As,ef.
A propriedade lb_cm do Concretopy é distinta de lb_nec_cm.

Com bitolas, materiais ou condições de aderência diferentes, registrar Lb de cada
conjunto e a decisão do engenheiro sobre o comprimento governante, quando não
estiver definida. Não selecionar automaticamente o menor Lb. Conferir geometria,
posição, demanda e contribuição resistente ao longo da ligação.

A preferência de continuidade não é otimização de aço. O critério 2 Lb não
substitui universalmente os requisitos normativos de emenda; avaliá-los
separadamente quando aplicáveis e consultados.

## A06 — Prolongamento e interrupção

Para cada conjunto de base ou complementar, positivo ou negativo:

1. Identificar sua região necessária pela demanda local.
2. Determinar a composição efetiva das demais armaduras que permanecem.
3. Obter sua resistência remanescente válida ao longo do ramo.
4. Localizar onde o conjunto pode deixar de ser necessário.
5. Verificar prolongamento físico ≥ 1 Lb além desse ponto, no sentido pertinente.

Critério de 1 Lb do escritório, com Lb básico sem redução pela relação de áreas.
Guardar ponto teórico, extremidade desenhada, sentido, comprimento disponível,
Lb, diagramas e composição remanescente. Não usar exclusivamente médias regionais,
comprimento desenvolvido ou um cruzamento isolado sem examinar o restante do ramo.

Se houver nova necessidade adiante, mudança de seção/composição ou cortes
coincidentes, avaliar a distribuição e a remanescente efetiva, sem atribuir a uma
barra que também termina uma contribuição permanente. Lacunas de diagrama
impedem concluir apenas as extensões afetadas. Políticas de vigas envolvendo
decalagem/10φ não são automaticamente regras desta revisão de lajes.

## A07 — Encontros com desníveis

Confrontar níveis superiores/inferiores, apoios por vigas/cintas, esforços e
detalhes. Momento próximo de zero pode sugerir articulação, mas isoladamente não
comprova condição de ligação ou ausência de transmissão.

Sem continuidade comprovada e com comportamento compatível, examinar bordas.
Havendo transmissão de momento, procurar detalhamento de continuidade aplicável.
“VER ARMADURA NAS VIGAS” exige consultar a viga/prancha correspondente antes de
apontar ausência. Se a remissão não puder ser resolvida, registrar documento e
localização faltantes; não inventar barras nem concluir inexistência.

Não incluir análise global da concepção, rigidez dos apoios ou deformações.

## A08 — Aberturas

Conferir correspondência entre forma e armadura; presença de reforços no entorno
e de detalhes genéricos de corte e dobra. Distinguir reforços localizados de
faixas distribuídas e verificar a abrangência do detalhe referenciado.

Não exigir dimensionamento específico dos reforços nem verificação completa de
todas as barras interrompidas nesta versão. Exclusão de um vazio do domínio
não comprova que seu entorno foi verificado.
