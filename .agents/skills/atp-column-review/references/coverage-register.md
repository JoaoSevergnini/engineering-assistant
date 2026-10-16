# Registro e cobertura da verificação

Esta referência mantém o contrato documental de **geometria** utilizado pelo
auxiliar de cobertura. Para comparações de armaduras e requisitos normativos,
usar os domínios de fontes e a separação de estados do
[contrato de revisão](review-contract.md). Não fabricar dados de formas para
adaptar uma verificação detalhe × norma a este formato histórico.

## Unidade de controle

Usar chave `(pilar, trecho, controle)`. Um trecho é um intervalo físico identificado,
por exemplo `T–1`, `1–2`, `bloco–T` ou `11–término-local`; não presumir que todos
os pilares tenham a mesma sequência. Controles típicos:

- `secao`: dimensões e contorno do concreto;
- `orientacao`: referência da seção e posição relativa das faces;
- `niveis`: referências correspondentes e datum;
- `comprimento_referencias`: diferença calculada entre referências;
- `comprimento_cotado`: leitura e confronto da cota direta do lance;
- `transicao`: mudança de seção ou deslocamento de faces;
- `termino`: extensão integral/parcial e relação com o elemento receptor;
- `posicao_traspasse`: posição da zona de emenda em relação ao maior topo de
  viga/laje incidente e à etapa de concretagem; ver [procedimento](lap-splice-position.md).

Definir controles aplicáveis ao escopo antes de avaliar. Não retirar um controle
porque faltam dados; classificá-lo como pendente. Inaplicabilidade precisa de
justificativa física/documental; ausência de documento não a comprova.

## Dados mínimos para rastreabilidade

Registrar valores da forma e do detalhe separadamente, com unidade, documento,
revisão e localização (página/região/ID do recorte). Manter leitura literal,
valor interpretado ou inferido e motivo da interpretação. Para níveis, guardar
original, transformação de datum, transportado e referência física. Para alturas,
guardar os dois níveis, intervalo calculado, cota direta lida e trecho a que cada
cota se refere. Valor não lido fica nulo, não zero e não calculado em seu lugar.

As evidências podem ser recortes locais ou localizadores precisos de um documento.
No relatório, fornecer vínculos utilizáveis. Verificar que o recorte contém a
identificação e a informação discutida. Uma evidência comum pode atender vários
pilares somente quando suas identificações e sua equivalência estão comprovadas.

## Estados por controle

| Estado | Significado |
|---|---|
| `COINCIDENTE` | Informação lida e confrontada para aquele controle específico. |
| `COINCIDE_REFERENCIAS` | Correspondência numérica entre referências; não valida cota direta, ligação ou documento com datum antigo. |
| `DIVERGENTE` | Conflito documental demonstrado, com fontes e valores identificados. |
| `PENDENTE` | Controle inconclusivo; registrar o dado/documento/esclarecimento necessário. |
| `NAO_EXAMINADO` | Controle ainda não executado; não incluí-lo como concluído. |
| `NAO_APLICAVEL` | Inaplicabilidade comprovada e justificada para esse controle. |

Uma dimensão pode coincidir e a orientação divergir. O intervalo pode coincidir
e a cota direta não ter sido lida. Grupo ambíguo não é aprovação individual.
Uma pendência não apaga uma divergência comprovada em outro controle.

Em `posicao_traspasse`, separar o resultado geométrico (início acima, coincidente
ou abaixo do maior topo; zona cruza o topo; dados insuficientes) da conclusão
sobre a adequação do detalhe. Abaixo do topo não recebe `DIVERGENTE` apenas por
uma prática usual: registrar o alerta e, sem critério de projeto/requisito
comprovado, manter a adequação `PENDENTE`, com motivo e solicitação de análise.
Acima do topo também não aprova comprimento resistente ou confinamento.

## Formato para o verificador de cobertura

Se houver matriz existente, preservá-la e adaptar seus campos ao contrato abaixo
sem inventar leituras para completar o formato. O auxiliar valida cobertura e
rastreabilidade mínima; **não interpreta desenhos nem aprova a engenharia**.

```json
{
  "escopo": "Geometria e níveis de pilares entre pavimentos",
  "inventario": [
    {"pilar": "P1", "trecho": "T–1", "controles": ["secao", "comprimento_referencias", "comprimento_cotado"]}
  ],
  "verificacoes": [
    {
      "pilar": "P1",
      "trecho": "T–1",
      "controle": "comprimento_referencias",
      "estado": "COINCIDE_REFERENCIAS",
      "dados_forma": {"inferior_m": "8.88", "superior_m": "13.96", "intervalo_calculado_m": "5.08"},
      "dados_detalhamento": {"inferior_m": "8.88", "superior_m": "13.96", "intervalo_calculado_m": "5.08"},
      "fontes_forma": [{"arquivo": "forma.pdf", "revisao": "R01", "localizacao": "página 1, P1, faixa local", "evidencia": "recortes/forma_P1.png"}],
      "fontes_detalhamento": [{"arquivo": "pilares.pdf", "revisao": "R00", "localizacao": "página 1, P1, T–1", "evidencia": "recortes/detalhe_P1.png"}]
    },
    {
      "pilar": "P1", "trecho": "T–1", "controle": "comprimento_cotado",
      "estado": "NAO_EXAMINADO", "motivo": "Cota direta ainda não lida."
    }
  ]
}
```

O exemplo é deliberadamente incompleto: falta o controle `secao`. O verificador
deve retornar cobertura incompleta, mesmo havendo uma referência coincidente.
Não usar estes números como dados ou padrão de outro empreendimento.

Executar com o Python disponível:

```text
python scripts/check_coverage.py caminho/matriz.json
```

Saída: resumo JSON; código 0 para cobertura classificada sem erros de contrato,
1 para contrato/cobertura incompletos e 2 para falha de leitura do arquivo.
Pendências justificadas permitem cobertura classificada, mas permanecem listadas
separadamente e não significam conclusão técnica. Os controles concluídos
explicitamente são contados à parte. `COINCIDE_REFERENCIAS` só é aceito em
`comprimento_referencias`. As listas de fontes são obrigatórias dos dois lados
para resultados coincidentes/divergentes; sem fonte suficiente, manter pendente.

Para resultado confrontado em `comprimento_cotado`, incluir no dado do detalhe
`"cota_direta_lida": {"valor": "508", "unidade": "cm"}` (ou m). Esse campo é
transcrição de leitura, nunca preenchimento pelo intervalo calculado. O auxiliar
verifica presença/unidade/valor positivo; a confirmação visual continua necessária.

## Texto dos apontamentos

Preferir: “Pilar/trecho, fonte e revisão A indicam X; fonte e revisão B indicam Y;
diferença Z; confirmar a referência/seção considerada e compatibilizar”.
Separar divergência global, desnível local e contradição interna. Não traduzir
a diferença documental em falta de resistência sem cálculo independente.
Na entrega, declarar quantos pilares e trechos foram inventariados, classificados,
concluídos, pendentes e não examinados, com exclusões físicas e de etapa.
