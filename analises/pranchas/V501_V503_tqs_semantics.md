# V501/V503 — atualização de semântica TQS

## Regra permanente e campos

A regra foi registrada antes de qualquer alteração de código em
[../../.agents/skills/reinforcement-review/references/tqs-beam-data.md](../../.agents/skills/reinforcement-review/references/tqs-beam-data.md)
e vinculada à Skill reinforcement-review. A regra de comprimento deixou de ser
uma hipótese: foi confirmada por João. Isso não resolve conflitos entre fontes.

| Operando | Registro raw / campo | Campo consolidado, em m |
|---|---|---|
| L_TQS | geometria_tabular / comprimento | beam.spans[i].geometry.length |
| DEPEV esq./dir. | apoio / excentricidade | beam.supports[j].eccentricity |
| b esq./dir. | apoio / largura | beam.supports[j].width |

A ligação esquerda/direita usa span.support_ids. DEPEV também aparece nas linhas
reacao_apoio / depev, mas sem unidade normalizada; não foi usado como atalho.

## Extensão mínima implementada

Schema consolidado 1.1, aditivo; schema documental continua 1.0:

- geometry.support_axis_length = length + eccentricity_left + eccentricity_right;
- geometry.clear_span_length = support_axis_length - width_left/2 - width_right/2;
- beam.support_reactions: observações max/min por relatório, unidade kN, nome e
  identificador do apoio, número documental quando disponível e fontes.

Todos os campos anteriores foram preservados. Os derivados recebem a união das
referências dos operandos em provenance. Dados ausentes ou conflitantes produzem
null e warning com os operandos. Reações distintas ficam como variantes por fonte;
não se escolheu uma nova envoltória, não se somaram máximos e não se trocaram sinais.

## V501 e V503: resultado geométrico

As duas vigas têm length=7,552 m, largura=0,19 m e altura=0,72 m.
Com os operandos de RELDTFPS/RELDTFNG:

```text
L_eixos = 7,552 + 0,384 + 0,494 = 8,430 m
L_livre = 8,430 - 1,20/2 - 1,42/2 = 7,120 m
Detalhamento documental: 7,110 m
Diferença TQS - detalhamento: +0,010 m
```

Fontes precisas: RELDTFPS 12761/12766/12767 (V501) e 15271/15276/15277 (V503).
O valor livre é coerente com os intervalos 0–712 cm de RELGER 54/178.
A diferença de 1 cm não foi eliminada nem incorporada ao detalhamento.

**No consenso integral, support_axis_length e clear_span_length permanecem null.**
As excentricidades variam: esquerda 0,384 / 0,38 / 0,004 m; direita 0,494 / 0,49 / 0 m,
segundo os diferentes relatórios e sua normalização literal. A regra confirmada não
justifica escolher uma fonte nem corrigir unidades impressas de outra.
É necessário resolver essa política documental para publicar um único resultado
geométrico numérico no consenso. O cálculo acima é identificado por fonte e testado.

## Investigação separada das 13 abscissas

Consultados os blocos V501/V503 dos 11 relatórios disponíveis no raw, seus cabeçalhos,
linhas de seção/ponto, índices, referências de eixo/face e ocorrências de abscissa.

- VGESFS 1367–1375 / 1656–1664 e RELDTVGS 3793–3802 / 4561–4570 fornecem 13 valores
  por série e índices 1…13, sem vetor de distâncias.
- RELGER 43/167 fornece apenas Abcis.=440 para o máximo positivo. Essa ocorrência
  não declara a origem física da série completa, nem define os demais pontos.
- RELDTFPS distingue eixo/face e esquerda/direita, mas não publica nesse bloco as
  13 coordenadas; as faixas de ESTRIB/RELGER são outras entidades documentais.
- A regra L_eixos/L_livre não demonstra que os 13 pontos sejam uniformes, nem
  define sua origem no eixo físico, eixo efetivo ou face.

**positions=null foi mantido.** Não foram implementados L/12, offset presumido ou
coincidência do máximo com uma seção para reconstruir a malha. O próximo dado
necessário é uma especificação do formato TQS ou exportação do modelo com a
abscissa física de cada seção e sua referência. Só depois cabe normalizar coordenadas.
Nenhuma coordenada foi criada com base no comprimento derivado.

## Reações e vigas apoiadas

V501 e V503 possuem seis observações cada: dois apoios em RELDTVGS, RELGER e VGESFS.
Os valores arredondados do RELDTVGS permanecem separados dos demais. As fontes e
conversões literais já existentes no raw são usadas sem reler texto no consolidador.

V541→V501, V542→V501, V559→V503 e V560→V503 agora têm raw e consolidado gerados
pelo pipeline. O campo reported_support_name conserva a ligação nominal; não foi
atribuída uma reação a IB1/IB2 ou N7, pois falta posição/identificação documental.
A convenção de sinais de transferência e a combinação de ações também não foram inferidas.

## Correção do parser

A expressão genérica de VGESFS agora reconhece cabeçalhos Q/M/MT MN./MX. e exige
13 células numéricas antes de normalizar uma série. Mensagens M(-)=... VAO=... PONTO=...
continuam preservadas como registros documentais, sem conversão indevida de PONTO=.
A correção não depende de número de viga. Testes cobrem mensagem local, série válida,
série malformada e os arquivos reais V542/V560.

## Validação e entregas

64 testes passaram: 35 no pipeline LST e 29 em beam_model, sem testes ignorados nesta
execução. Os testes antigos não foram alterados. V504, V502 e V501/V503 continuam
cobertos. O teste de conversão novo foi corrigido por erro no valor esperado antes
da execução final aprovada.

Alterados: referência permanente, link da Skill, extrair_viga_lst.py,
consolidar_viga.py, CONSOLIDACAO.md; criado test_tqs_semantics.py.
Regenerados: V501/V503_tqs.json, V541/V559_tqs.json, V504.json.
Criados: V542/V560_tqs_raw.json e V542/V560_tqs.json; este relatório.
O relatório de mapeamento anterior é histórico e aponta para esta atualização.
Os JSONs documentais existentes e os modelos de detalhamento não foram modificados.
Nenhuma verificação de flexão, cisalhamento, ancoragem ou suspensão foi implementada.
