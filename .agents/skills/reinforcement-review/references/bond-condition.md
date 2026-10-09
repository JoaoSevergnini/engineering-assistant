# Aderência de barras horizontais no escalonamento positivo

Identificador: `engineer_confirmed_bond_condition_v1`.
Autoridade: regra expressamente confirmada pelo engenheiro para barras horizontais,
validada em V1001 e V536/V565 e em testes de boa/má aderência/fronteira.
Consolidação documental: 05/10/2026. Não se atribui nova interpretação normativa.

## Regra e geometria

Usar **y em cm, do centro da barra até a face inferior**, e h em cm:

| Altura | Boa aderência | Má aderência |
|---|---|---|
| h < 60 cm | y ≤ 30 cm | y > 30 cm |
| h ≥ 60 cm | y ≤ h − 30 cm | y > h − 30 cm |

A fronteira pertence à boa aderência. Para flexão positiva, `y=h−d_camada`,
usando o centro físico da **barra interrompida**, obtido da geometria/camadas
Concretopy da composição anterior. Não usar d_for_al: esse é o centroide do
conjunto anterior e pode ser diferente do d da barra cortada.
Não classificar como boa simplesmente porque a barra é positiva ou inferior.

Preservar h, y, camada, sua posição física, origem dessa geometria, fronteira,
classificação, regra e provenance da marca. Exigir posição válida `0 < y < h`.
Se posição/condições não estiverem resolvidas, não inventar aderência.

## Ferramenta e integração

Implementação existente:
[bar_scaling.classify_bond](../../../../tools/reinforcement_checks/bar_scaling.py).
Retorna `good`/`poor` e `boa_aderencia`, com fronteira/entradas/regra.
O workflow fornece o booleano explicitamente a `Concretopy.CondicoesAncoragem`;
o Concretopy calcula fbd e lb e não deduz geometria ou aderência da função da barra.
Contrato público: [ancoragem](../../../../../concretopy/docs/ancoragem.md).

Escopo validado: barra horizontal, sem forma deslizante. Barras inclinadas,
formas deslizantes e combinações de regimes ficam fora deste workflow;
não introduzir precedência ou resolver conflitos por analogia.
O campo de hipótese deve registrar a fonte; ausência de documentação de forma
deslizante não é confirmação de inspeção da concretagem.

## Exemplos de geometria, não valores universais

- V1001/N3: h=72 cm, d_camada=68,5 cm, y=3,5 cm, fronteira 42 cm: boa.
- V536/V565/N3: h=72 cm, d_camada=64 cm, y=8 cm: boa. O centroide
  anterior d_for_al=66 cm não é usado para obter y da N3.

Procedimento completo: [positive-bar-scaling.md](positive-bar-scaling.md).
