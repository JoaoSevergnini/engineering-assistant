# Candidato real adicional: V1001

04/10/2026. Investigação documental, sem resultado resistente ou correção automática.

Após testes sintéticos e regressão V501, foram inventariados todos os beam_model
existentes em analises/pranchas. V1001 é um candidato real com duas marcas
positivas e intervalos distintos:

| Marca | Composição documental | Camada | Intervalo documental (cm) |
|---|---|---|---|
| N3 | 2 Ø10 | primeira, layers=[2], face lower | −42 a 608 |
| N5 | 2 Ø10 | primeira, layers=[2], face lower | −42 a 753 |

Fontes: V1001_beam_model.json e V1001_detalhamento_prancha.json,
/longitudinal_reinforcement/positive/0 e /positive/1. Existem também
V1001_tqs.json, V1001_tqs_raw.json e V1001_tqs_positions.json.

Tentou-se gerar o mapping usando a ferramenta existente, sem alterar dados:
`map_beam(V1001_beam_model, V1001_tqs, V1001_tqs_positions)`.
Resultado: **ValueError: Convenção do detalhamento não suportada.**

Origem textual do beam_model: `face interna do apoio esquerdo P2A/P2B`;
o mapping atual aceita a convenção exata `face interna do apoio esquerdo`.
Além disso, os IDs documentais dos apoios são P2A/P2B e P1A/P1B, enquanto
span.support_ids TQS são P2A e P1A. A associação nominal requer tratamento
explícito antes de usar essa viga como integração espacial aprovada.

Não foram removidos sufixos ou divididos IDs silenciosamente, nem modificados
beam_model/beam_mapping para passar a integração. Não se montou mapping artificial,
nem se calculou capacidade ou demanda regional da V1001 a partir de coordenadas
inventadas. A atualização do contrato de compatibilização deve preceder o teste.

V502 também tem duas positivas (N6/N7), mas seus intervalos documentais são null;
isso impede a decomposição determinística real. V501/V503 têm somente N5 positiva.
Portanto, a lógica nova foi validada por sobreposições sintéticas e regressão
real V501; V1001 é o próximo candidato, com impedimentos identificados acima.
