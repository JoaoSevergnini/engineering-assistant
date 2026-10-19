# Etapa 11 — Quantificação nominal das armaduras positivas

## Auditoria e método

Reutilizados os 59 registros, 35 regiões distribuídas, 119 células e confirmações da Etapa 10, sem alterar geometrias, classes, diâmetros, espaçamentos ou quantitativos. A área circular da barra é obtida da propriedade pública Concretopy.Barra.area_cm2. A única operação adicional é multiplicar por 100/s, com s em cm. Não se usam quantidade impressa, comprimento nominal ou dimensões da envoltória como substitutos do espaçamento.

`As/m = [π (φ/10)²/4] × (100/s)`, em cm²/m. Valores internos são preservados sem arredondamento; apenas as tabelas e mapas usam duas casas decimais.

## Resultado

```json
{
  "occurrences": 59,
  "individual_rates_calculated": 38,
  "rates_pending": 21,
  "composition_records": 119,
  "composition_quantification": {
    "INDIVIDUAL_NOMINAL_AREA": 70,
    "PENDING_COMPOSITION": 41,
    "CONFIRMED_JOINT_NOMINAL_AREA": 3,
    "NON_ADDITIVE_LAP": 5
  },
  "nominal_joint_totals_authorized": 3,
  "effective_depth_calculated": 0,
  "flexural_resistance_calculated": 0
}
```

Há 38 taxas individuais calculáveis: 35 ocorrências distribuídas com área sustentada e três chamadas com espaçamento, mas geometria pendente (N18/O009, N33/O014 e N41/O057). Estas três taxas não validam região de atuação ou composição. As 21 ocorrências sem espaçamento indicado permanecem sem As/m; quantidade total de barras não foi convertida artificialmente em taxa.

Das 119 células, 70 possuem valor individual nominal; três têm soma nominal autorizada pela função conjunta e pela regra atual de camada intercalada; cinco não admitem soma por traspasse documental/local; as outras 41 permanecem sem total composto. As classificações originais são preservadas separadamente. Não se soma o conjunto inteiro de células como quantitativo da prancha.

## Exemplos numéricos

| Ocorrência / região | Armadura | As individual ou total (cm²/m) | Fundamento |
|---|---|---:|---|
| O043 | N13 Ø8 c/14 | 3.59 | Taxa individual documental |
| O044 | N13 Ø8 c/14 | 3.59 | Taxa individual documental |
| O034 | N14 Ø5 c/14 | 1.40 | Taxa individual documental |
| O035 | N14 Ø5 c/14 | 1.40 | Taxa individual documental |
| C059 | N14 + N15 | 4.99 | Função conjunta sustentada no domínio existente; soma nominal |
| C083 | N13 + N14 | 4.99 | Função conjunta sustentada no domínio existente; soma nominal |
| C088 | N13 + N14 | 4.99 | Função conjunta sustentada no domínio existente; soma nominal |

C083 e C088 correspondem a N13+N14, esquerda e direita. C059 corresponde à confirmação local N15+N14, com as mesmas bitolas/espaçamentos; não foi renomeada como N13. A N14 foi quantificada individualmente, embora não haja célula somente N14 na partição real; não foi criada uma região isolada fictícia. Nas parcelas triplas C071/C076, as taxas individuais estão disponíveis, mas o total integral continua nulo. C092 e as quatro células com N40 não recebem soma.

## Mesma camada física não significa mesmo centro

A regra fornecida pelo engenheiro nesta Etapa 11 é registrada em criterios_documentais.json e vinculada ao hash deste PDF: base e reforço positivos são intercalados na mesma camada física. Não se cria camada adicional para o reforço. Cada componente mantém diâmetro e espaçamento próprios. A regra não é aplicada às armaduras localizadas de furos, que podem ter distribuição superior/inferior distinta, nem a outro documento sem perfil explícito.

Os centros não foram igualados: os raios de Ø8 e Ø5 são 0,40 e 0,25 cm. Se posteriormente for comprovada a mesma referência de superfície de cobrimento para ambos, seus centros poderão diferir; essa condição ainda não foi usada para calcular d. Não se adotou uma bitola equivalente nem centro único para a composição.

## Espessuras, cobrimento e altura útil

A espessura vem das etiquetas documentais e de associações RELIABLE, independentemente da qualidade completa do contorno. Associações PROBABLE mantêm espessuras candidatas, sem promovê-las a valores confiáveis. Casos de espessuras distintas têm entradas separadas por laje/espessura e nenhum d único. Nenhuma ocorrência real desta prancha recebeu duas espessuras confiáveis; a separação de casos foi verificada sinteticamente. As referências espaciais continuam em pontos PDF, sem serem tratadas como centímetros físicos.

Foi identificado cobrimento documental de **2,0 cm** no detalhe “COBRIMENTO ARMADURA LAJES MACIÇAS”: cota positiva T166:0, etiqueta T156:0, título T152:0 e unidade geral em centímetros T265:0. A leitura combina textos extraídos e inspeção do desenho; é interpretação documental do assistente, não confirmação humana nova nem comprovação de execução. O valor não foi inventado ou adotado por norma. Seu escopo é o detalhe geral de lajes maciças, sem comprovar o centro de cada bitola/direção.

[Detalhe original de cobrimento](detalhe_cobrimento_original.png) · [Nota original de unidades](nota_unidades_original.png)

A distância do centro à face tracionada e d permanecem nulos. Falta confirmar a referência vertical específica e a ordem em relação à armadura ortogonal. O perfil de mesma camada entre base/reforço não resolve essa relação entre direções. Para ocorrências sem laje confiável ou sem geometria sustentada, essas pendências também ficam explícitas. A ausência desses dados não impede o cálculo nominal de As/m.

## Preparação para o Concretopy

O código local do Concretopy foi inspecionado, sem alterações: armaduras.py, verificacoes/flexao.py, secoes.py, detalhamento/arranjos.py e unidades.py. Sua propriedade Barra.area_cm2 foi efetivamente reutilizada; nenhuma função de flexão foi executada.

A entrada preparada usa geometria da seção em cm, diâmetros em mm, tensões em MPa, forças em kN e momentos em kN·cm. A referência de largura é 100 cm. A densidade 100/s pode ser fracionária e não é numero_barras de uma faixa finita; por isso esse argumento da API fica nulo. Os parâmetros de materiais não foram inventados.

A interface CamadaArmaduraLongitudinal representa barras iguais e exige quantidade inteira. O posicionamento automático empilha os grupos com afastamento vertical; mesmo com d explícito, o verificador de flexão rejeita envelopes verticais sobrepostos entre camadas. Portanto, enviar Ø8 e Ø5 intercalados como duas camadas distorce o modelo ou é rejeitado. SecaoRetangular também tem padrão de estribo de viga, que não deve ser importado silenciosamente para lajes.

A etapa seguinte precisará de contrato/modelo que represente famílias de bitolas distintas na mesma camada física, com centros próprios e interpretação lateral adequada. Não basta desligar validações nem reutilizar o empilhamento de vigas. Essa adaptação foi somente documentada; não foi implementada, e o pacote Concretopy e os módulos de vigas/pilares permanecem intactos. [Auditoria com hashes](auditoria_concretopy.json).

## Entregáveis e limites

[Propriedades das ocorrências](ocorrencias.json) · [Composições confirmadas e pendentes](composicoes.json) · [Tabela das 59 ocorrências](ocorrencias.md) · [Diagnóstico gráfico](mapa_quantificacao.png) · [N13/N14 esquerda](L603_esquerda_As.png) · [N13/N14 direita](L603_direita_As.png)

Os registros distinguem taxa documental, elegibilidade geométrica, espessura confiável, soma nominal e resistência. N14 continua reforço; N40 continua traspasse sem adição independente; as nove pendências anteriores permanecem preservadas. Não há conclusão de suficiência, conformidade, necessidade de reforço, altura útil ou resistência à flexão.

## Valida??o executada

**259 testes aprovados**, incluindo 28 novos da Etapa 11. Os testes sint?ticos verificam convers?es mm/cm e espa?amentos variados, precis?o, entradas inv?lidas, mesma camada com bitolas distintas, preserva??o de centros desconhecidos, duplicidades, dire??es/camadas incompat?veis, composi??es completas e pendentes. As regress?es da prancha verificam N13/N14 e os tr?s totais nominais, N40/C092 sem soma, chamadas sem espa?amento, taxas com geometria/associa??o pendente, preserva??o integral das camadas anteriores e aus?ncia de chamadas de flex?o/altura ?til. Cen?rios modificados de cobrimento ausente ou duas espessuras usam c?pias sint?ticas dos dados reais; n?o comprovam essas situa??es nesta prancha.

Os tr?s mapas de diagn?stico, o detalhe de cobrimento e a nota de unidades foram inspecionados visualmente. Sucesso computacional e leitura documental n?o constituem valida??o estrutural. [Registro dos testes e hashes](validacao_testes.json).
