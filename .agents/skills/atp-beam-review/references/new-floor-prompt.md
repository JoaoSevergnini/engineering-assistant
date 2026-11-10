# Modelo de pedido para ATP de vigas

As regras permanentes e a sequência estão na skill. O pedido informa apenas projeto, caminhos, exceções e a etapa da sessão. Usar uma sessão por etapa.

## Primeira sessão (etapa 0)

```text
Use a skill atp-beam-review. ATP das vigas do pavimento [PAVIMENTO] do projeto [PROJETO].
Etapa desta sessão: 0 (preparação).

Pasta de trabalho: [analises/<projeto>_vigas_<pavimento>/ ou pasta do projeto]
Contexto e decisões anteriores: [CAMINHO ou "não há"]
Formas e referências de apoios/blocos: [PASTA E PRANCHAS]
Detalhamentos (PDF e DXF): [PASTA E PRANCHAS]
Modelo TQS: [CAMINHO]
Norma de referência: [EDIÇÃO]
Elementos incluídos/excluídos: [DEFINIR]
Ampliações de escopo: [nenhuma | ancoragem | escalonamento | ...]
Premissas padrão (default-criteria.md §1: γf 1,4; esforços TQS + geometria do detalhamento; série VGESFS; furos fora; tolerância 110%): [manter o padrão | alterar: ...]
Premissas específicas deste pavimento: [INFORMAR ou "registrar a partir dos documentos e me perguntar"]
Padrão de entrega: [referência anterior, se houver]
```

## Sessões seguintes (etapas 1, 2 e 3)

```text
Use a skill atp-beam-review. Retome a ATP das vigas do pavimento [PAVIMENTO] do projeto [PROJETO]
pela retomada em [PASTA]/retomada.md. Etapa desta sessão: [1 | 2 | 3].
[Decisões novas desde a última sessão: ...]
[Etapa 3: seleção enviada em ...]
```

## Ao final de cada sessão

Pedir: índice e `retomada.md` atualizados; métricas da etapa (vigas e controles executados, pendências por motivo, scripts criados, reexecuções); dúvidas agrupadas para João.

Se o contexto da conversa passar de cerca de 60–70% antes do fim da etapa, pedir a atualização do índice e da `retomada.md` num ponto de parada natural (fim de um lote, não no meio de uma viga) e continuar em uma sessão nova com o modelo acima.
