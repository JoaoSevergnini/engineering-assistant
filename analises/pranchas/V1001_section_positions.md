# V1001 — ensaio de preenchimento de positions

Executado em 04/10/2026 com o padrão confirmado por João. Saída:
[V1001_tqs_positions.json](V1001_tqs_positions.json). Não sobrescreve o modelo
anterior nem altera os esforços. Schema consolidado permanece 1.1.

## Dados e coordenadas

- Comprimento discretizado: **7,552 m**, VGESFS.LST:491, geometria do vão 1.
- Apoio esquerdo: **P2A**, identificado pela sequência `support_ids`.
- DEPEV esquerdo: **38,4 cm = 0,384 m**, RELDTFPS.LST:4770.
- DEPEV direito: **49,4 cm**, RELDTFPS.LST:4771, utilizado na conferência geométrica.
- Origem local: eixo físico do apoio esquerdo; x cresce para o apoio direito.
- Unidade de `positions`: **m**, conforme `units.length` do modelo.

```text
L13 = 7,552 m
Delta_x = 7,552/12 = 0,629333333... m
x_i = 0,384 + (i-1)*7,552/12
x_1 = 0,384 m
x_13 = 7,936 m
L_eixos = 0,384 + 7,552 + 0,494 = 8,430 m
L_livre = 8,430 - 1,20/2 - 1,42/2 = 7,120 m
```

| Seção | positions (m), apresentado com 6 casas |
|---:|---:|
| 1 | 0,384000 |
| 2 | 1,013333 |
| 3 | 1,642667 |
| 4 | 2,272000 |
| 5 | 2,901333 |
| 6 | 3,530667 |
| 7 | 4,160000 |
| 8 | 4,789333 |
| 9 | 5,418667 |
| 10 | 6,048000 |
| 11 | 6,677333 |
| 12 | 7,306667 |
| 13 | 7,936000 |

## Séries e rastreabilidade

Preenchidas as cinco séries do VGESFS: momento máximo/mínimo, cortante
máximo/mínimo e torção máxima (`VGESFS.LST:494–502`). A saída do ensaio
contém somente essas séries em `internal_forces`. Valores, sinais e lacunas
foram preservados; não houve majoração nem interpolação de esforços.

Cada campo `positions` possui proveniência para o comprimento do VGESFS,
o DEPEV do RELDTFPS e a série de esforços correspondente. A origem e a unidade
estão explicitadas em `policies.section_positions`.

Os demais campos, fontes e warnings foram herdados do consolidado anterior.
Assim, materiais e excentricidades consensuais ainda podem aparecer como null:
este ensaio aplica as fontes escolhidas às posições sem migrar integralmente
a consolidação de geometria, materiais e reações. Não consome RELDTVeT para
gerar coordenadas. Os registros históricos continuam preservados.

Ferramenta de ensaio reutilizável:

```powershell
python tools/extrator_lst/section_positions.py analises/pranchas/V1001_tqs.json analises/pranchas/V1001_tqs_raw.json --output analises/pranchas/V1001_tqs_positions.json
```

A ferramenta recusa fonte escolhida ausente/conflitante, unidade incompatível,
seções fora da ordem 1…13 e gravação sobre uma entrada. A origem é local a cada
vão; não há transformação para um sistema global de viga com vários vãos.

## Validação

**39 testes passaram** no conjunto de ferramentas LST, incluindo quatro novos
testes: 13 coordenadas da V1001, proveniência e preservação das entradas;
ausência da fonte escolhida sem fallback; ordem inválida das seções; e ligação
inválida do vão. Nenhuma verificação estrutural foi executada.

Criados: este relatório, `V1001_tqs_positions.json`,
`tools/extrator_lst/section_positions.py` e `test_section_positions.py`.
Atualizada a referência permanente para registrar a autorização do ensaio.
Extrator e consolidador existentes permanecem sem alteração.
