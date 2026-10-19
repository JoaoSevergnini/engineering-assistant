# Etapa 9.1 — Associação independente de contenção integral

## Auditoria e alteração do critério

A Etapa 9 classificava a ocorrência pela pior classe de suas parcelas. Uma parcela NO_DOMAIN tornava toda a associação INDETERMINATE, mesmo quando barra, faixa e etiqueta sustentavam uma única laje. Isso confundia extensão externa da armadura com incerteza sobre sua laje. A revisão utiliza a partição e as entidades existentes, sem recalcular ou modificar seus polígonos.

A camada derivada separa association_confidence, contour_confidence e os estados históricos das parcelas. RELIABLE significa associação automática sustentada por dados documentais e entidades geométricas interiores; não significa contorno confirmado, validação humana ou aptidão para cálculo resistente. Os nove contornos continuam candidatos. PROBABLE preserva uma hipótese com suporte parcial ou alerta topológico. INDETERMINATE registra ausência de suporte suficiente ou concorrência no mesmo trecho.

## Evidências utilizadas

Para distribuídas: interseção de área, comprimentos interiores da barra e do eixo transversal, e cruzamento de ambos dentro do domínio. Para RELIABLE são necessários os dois comprimentos positivos e o cruzamento interior, além de etiqueta documental de laje/espessura e ausência de alerta topológico. Uma interseção apenas da envoltória não basta. Para localizadas: interseção interior de cada traço contínuo aceito, sem pontes inventadas entre grupos. Suporte incompleto mantém PROBABLE. Nenhum critério usa distância ao texto, centroide, cor ou palavras BASE/REFORÇO.

Não foi aplicado limite de área para descartar pequenas diferenças. Os trechos externos continuam nos segmentos originais, com domínio e espessura não atribuídos. Não são automaticamente ancoragem; a associação da ocorrência à laje não transfere a espessura para esses trechos. A continuidade considerada é a das entidades já extraídas, não uma comprovação da continuidade física das barras.

## Comparação

| Estado | Etapa 9 | Etapa 9.1 |
|---|---:|---:|
| RELIABLE | 0 | 40 |
| PROBABLE | 12 | 8 |
| INDETERMINATE | 47 | 11 |

Transições: INDETERMINATE → INDETERMINATE: 11; INDETERMINATE → PROBABLE: 7; INDETERMINATE → RELIABLE: 29; PROBABLE → PROBABLE: 1; PROBABLE → RELIABLE: 11.

```json
{
  "occurrences": 59,
  "states": {
    "RELIABLE": 40,
    "INDETERMINATE": 11,
    "PROBABLE": 8
  },
  "changed": 47,
  "requires_engineer_decision": 19,
  "with_slab_intersection": 48,
  "multiple_slabs": 0,
  "different_thickness_domains": 0
}
```

A contagem de associações sustentadas não é taxa de acerto: não houve nova conferência independente de cada associação. A mudança decorre de separar o critério de associação do critério de contenção.

## Casos que exigem decisão

Os destaques do mapa são apenas as ocorrências abaixo. Os demais contornos continuam sujeitos à revisão geométrica geral, sem que isso torne automaticamente pendente a identidade da laje atendida.

- **O009/N18 — INDETERMINATE**: Geometria de atuação não comprovada.

- **O012/N17 — INDETERMINATE**: Geometria de atuação não comprovada.

- **O014/N33 — INDETERMINATE**: Geometria de atuação não comprovada.

- **O016/N17 — INDETERMINATE**: Geometria de atuação não comprovada.

- **O028/N23 — INDETERMINATE**: Geometria de atuação não comprovada.

- **O037/N22 — INDETERMINATE**: Geometria de atuação não comprovada.

- **O039/N21 — PROBABLE**: Parte dos grupos/traços não possui suporte interior no domínio.

- **O040/N21 — PROBABLE**: Parte dos grupos/traços não possui suporte interior no domínio.

- **O047/N24 — INDETERMINATE**: Geometria extraída sem interseção com os domínios candidatos.

- **O048/N7 — INDETERMINATE**: Geometria de atuação não comprovada.

- **O049/N7 — INDETERMINATE**: Geometria de atuação não comprovada.

- **O050/N25 — PROBABLE**: Contorno candidato com alerta topológico (faixa estreita); Suporte parcial da barra ou eixo de distribuição.

- **O053/N40 — PROBABLE**: Contorno candidato com alerta topológico (faixa estreita); Suporte parcial da barra ou eixo de distribuição.

- **O054/N37 — INDETERMINATE**: Geometria extraída sem interseção com os domínios candidatos.

- **O055/N35 — PROBABLE**: Contorno candidato com alerta topológico (faixa estreita); Suporte parcial da barra ou eixo de distribuição.

- **O056/N39 — PROBABLE**: Contorno candidato com alerta topológico (faixa estreita); Suporte parcial da barra ou eixo de distribuição.

- **O057/N41 — INDETERMINATE**: Geometria de atuação não comprovada.

- **O058/N36 — PROBABLE**: Contorno candidato com alerta topológico (faixa estreita).

- **O059/N38 — PROBABLE**: Contorno candidato com alerta topológico (faixa estreita).

## Múltiplas lajes, espessuras e preservação

A mesma ocorrência pode manter várias associações em domínios disjuntos, inclusive com espessuras diferentes. Cada parcela conserva suas opções documentais de espessura. Espessuras distintas na mesma parcela concorrente impedem resolução automática. Não se cria uma altura útil única nem se duplicam barras. Nenhuma ocorrência desta prancha intersectou dois domínios candidatos; a capacidade foi validada em testes sintéticos.

N14 permanece reforço em toda a extensão das duas ocorrências, e R053/N40 permanece traspasse por confirmação do engenheiro. As quatro confirmações locais, a inconsistência N38, os quantitativos, os grupos e todas as geometrias anteriores foram preservados. O inventário completo inclui a camada original da Etapa 9 intacta e uma nova camada refined_slab_assignment.

## Entregáveis e próximos passos

[Mapa de conferência](mapa_conferencia.png) · [Comparação individual das 59 ocorrências](comparacao_59.md) · [Inventário derivado](associacoes.json) · [Pendências](pendencias.json) · [L605](pendencias_L605.png) · [N21](pendencias_N21.png)

Priorizar revisão do contorno L605, dos grupos N21 em L607, da faixa O047/N24 e das geometrias ainda inconclusivas. A falta de interseção não prova ausência de laje ou falha estrutural. Não foram executadas verificações resistentes ou inferências de altura útil.

## Valida??o executada

**183 testes aprovados**, incluindo 17 novos da Etapa 9.1. Os testes sint?ticos cobrem trechos externos, suporte insuficiente da faixa, dom?nios concorrentes, m?ltiplas espessuras, tra?os verticais, grupos desconectados e independ?ncia da cor/dist?ncia das etiquetas. As regress?es reais verificam as 59 ocorr?ncias, N26, N14/N40, determinismo e igualdade integral das geometrias, parcelas externas, quantitativos e camadas anteriores (incluindo N38). As tr?s imagens foram inspecionadas visualmente quanto ? legibilidade das marca??es; isso n?o representa confirma??o independente das 59 associa??es. [Registro da execu??o](validacao_testes.json).
