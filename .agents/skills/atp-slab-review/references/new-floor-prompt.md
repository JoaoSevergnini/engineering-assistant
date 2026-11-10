# Modelo de pedido para ATP de lajes

As regras permanentes, as fases e os critérios estão na skill. O pedido informa
apenas projeto, caminhos, premissas conhecidas, exceções e a fase da sessão.
Usar uma sessão por fase (seção 3 do SKILL.md).

## Primeira sessão (fase 0)

```text
Use a skill atp-slab-review. ATP das lajes do pavimento [PAVIMENTO] do projeto [PROJETO].
Fase desta sessão: 0 (preparação). [Se couber no contexto: seguir também com a fase 1.]

Pasta de trabalho: [analises/<projeto>_lajes_<pavimento>/ ou pasta do projeto]
Contexto e decisões anteriores: [CAMINHO ou "não há"]
Formas: [PASTA E PRANCHAS]; planta do modelo TQS em DXF: [CAMINHO ou "não há"]
Armaduras positivas e negativas (PDF e DXF): [PASTA E PRANCHAS]
Diagramas de momentos H/V (DXF): [CAMINHO]
Detalhes complementares: [CAMINHO ou "não há"]
Norma de referência: [EDIÇÃO]
Lajes/regiões incluídas e excluídas: [DEFINIR]
Referência de apresentação: [padrão da skill | outro, indicar]

Premissas já conhecidas (confirmar nos documentos; perguntar em bloco o restante):
- Camadas H/V em positivas e negativas, contadas da face tracionada: [ ]
- Reforços positivos intercalados com a base ou sobrepostos: [ ]
- Natureza e unidade dos momentos DXF; filtro e isocurva: [ ]
- γf para MRd/γf: [ ]
- Materiais, cobrimento, agregado máximo, conformação do aço: [ ]
- Sequência de concretagem e faixas de segunda etapa: [ ]
- Referência altimétrica do modelo: [ ]
- Enquadramento das lajes em uma ou duas direções: [ ]
- Escopo de aberturas e furos: [ ]
- Tolerância editorial para η: [ ou "não há"]
```

## Sessões seguintes (fases 1 a 5)

```text
Use a skill atp-slab-review. Retome a ATP das lajes do pavimento [PAVIMENTO] do projeto
[PROJETO] pela retomada em [PASTA]/retomada.md. Fase desta sessão: [1 | 2 | 3 | 4 | 5].
[Decisões novas desde a última sessão: ...]
[Fase 5: PDFs com as escolhas e comentários em ...]
```

## Ao final de cada sessão

Pedir: índice e `retomada.md` atualizados; métricas da fase (lajes, regiões e
controles executados, pendências por motivo, scripts criados, reexecuções);
dúvidas agrupadas para João.

Se o contexto da conversa passar de cerca de 60–70% antes do fim da fase,
pedir a atualização do índice e da `retomada.md` num ponto de parada natural e
continuar em uma sessão nova com o modelo acima.
