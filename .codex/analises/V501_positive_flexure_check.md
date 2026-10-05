# Golden case V501/N5 — flexão positiva com Concretopy

Atualizado em 04/10/2026 após confirmação do aço pelo engenheiro responsável.
**Capacidade suficiente na seção governante analisada:** Mk_equivalente =
**99.47034565405093 kN.m** ≥ Msk = **61,5073088 kN.m**.
Utilização **0.618348196093708 (61.8348%)**.
Isso não constitui aprovação global da viga ou do detalhamento. O bloqueio
anterior por fyk foi resolvido por regra documental confirmada.

## Arquivos e arquitetura

Entradas em analises/pranchas: V501_V503_beam_model.json, V501_tqs.json,
V501_tqs_positions.json, V501_beam_mapping.json e V501_tqs_raw.json.
Detalhamento de origem: V501_V503_detalhamento_prancha.json.
Saída estruturada: V501_positive_flexure_check.json.

Orquestração em tools/reinforcement_checks/v501_positive_flexure.py; regra de
materiais em materials.py, independente de beam id. Concretopy carregado para
leitura/importação de ../concretopy, versão nominal 1.0.0; API pública
concretopy.verificacoes.flexao.verificar_flexao_viga_retangular.
JSON registra assinatura/caminho/hash da implementação e pyproject, hash do
interpretador, cinco entradas e hashes. Mapping/raw são auditados antes da chamada.
Não há equações resistentes locais. Concretopy não foi alterado.

## Regra de interpretação do aço

Regra **engineer_confirmed_ca50_fyk_500_v1**, fornecida por João:

- CA50 e CA-50 → classe normalizada CA-50, fyk=500 MPa.
- CA-50A → CA-50 com fyk=500 MPa, somente para resistência característica neste fluxo.
- Texto original, classe, fyk derivado, regra e proveniência conservados separadamente.
- Qualquer fonte operacional não reconhecida, mesmo junto de uma conhecida,
  bloqueia a verificação; ausência não utiliza fyk default.
- Somente esses aliases foram implementados. Não se pressupõe equivalência de
  outras propriedades de CA-50A.

| Texto original | Classe normalizada | fyk | Fonte | Pointer raw |
|---|---|---:|---|---|
| CA-50A | CA-50 | 500 MPa | RELDTFNG.LST, linha 9618 | /categorias/materiais/0/campos_explicitos/3 |
| CA50 | CA-50 | 500 MPa | RELDTFPS.LST, linha 12785 | /categorias/materiais/7/campos_explicitos/2 |

Cada observação preserva também a linha completa original. RELDTVeT permanece
em excluded_observations, sem uso operacional. O conflito textual antigo do
consolidado é histórico; **não existe conflito de fyk** entre as fontes
operacionais reconhecidas. Regra permanente em tqs-beam-data.md.
O antigo override --fyk-resolution foi removido para impedir bypass de classe
não reconhecida.

## N5, série e região

N5: **4 Ø12,5**, função positive, face lower, camadas **[3,1]**:
três barras na primeira camada e uma na segunda. Comprimento desenvolvido
815 cm, intervalo documental −53 a 762 cm, comum **0,070–8,220 m**.
Fonte documental /longitudinal_reinforcement/positive/0.
A N5 cobre geometricamente as 13 seções, de 0,384 a 7,936 m; positions foram
consumidas do mapping, sem recálculo. Ordem das camadas: face inferior tracionada
para a superior comprimida. Presença geométrica não comprova ancoragem ou
desenvolvimento, nem se generaliza para barras escalonadas.

Série auditada contra **M MX.**, VGESFS.LST, **linha 1373**, vão VGESFS 1,
s537#/normalizacao, raw /categorias/esforcos_ao_longo_dos_vaos/31.
quantity=bending_moment, envelope=max, stage=model_input, unit=kN.m.
Não se seleciona apenas pelo nome max: fonte/rótulo/vão e os 13 valores são
conferidos. A natureza característica **Msk** vem da confirmação de João neste
fluxo, registrada separadamente da evidência do relatório.

Maior momento **positivo**: **61,5073088 kN.m**, seção **8**,
**x=4,789333333333333 m**, original 6,272 tf.m. Seções negativas não governam.
Não há valor absoluto, interpolação, extrapolação ou máximos entre pontos.
A série min e demais séries continuam preservadas no mapping.

| Seção | x (m) | M MX. (kN.m) | Elegível positivo |
|---:|---:|---:|---|
| 1 | 0.384 | -22.03554255 | não |
| 2 | 1.0133333333333332 | 1.3337044 | sim |
| 3 | 1.6426666666666665 | 21.21178395 | sim |
| 4 | 2.272 | 37.58888945 | sim |
| 5 | 2.901333333333333 | 50.4650209 | sim |
| 6 | 3.5306666666666664 | 59.6832719 | sim |
| 7 | 4.16 | 59.10467955 | sim |
| 8 | 4.789333333333333 | 61.5073088 | sim |
| 9 | 5.418666666666667 | 58.83009335 | sim |
| 10 | 6.047999999999999 | 50.80825365 | sim |
| 11 | 6.677333333333333 | 36.1276986 | sim |
| 12 | 7.3066666666666675 | 15.0826277 | sim |
| 13 | 7.936 | -10.1793027 | não |

## Dados e entrada executada

| Operando | Valor | Fonte |
|---|---:|---|
| bw / h | 19 / 72 cm | beam_model /section, fonte documental |
| fck | 40 MPa | explicitamente MPa: RELDTFNG 9698, RELDTFPS 12781 |
| fyk | 500 MPa | regra confirmada e observações acima |
| Cobrimento inferior | 2,5 cm | TQS /beam/cover/bottom, s445, RELDTVGS 3772 |
| Estribo governante | Ø5 mm | R1/N6, intervalo comum 0,600–5,970 m |
| Es | 210.000 MPa | default público Aco.es |
| gamma_c / gamma_s | 1,4 / 1,15 | defaults da API de resistência |
| gamma_f | 1,4 | Gamaf explícito, RELDTFNG 9618 |

Fck kgf/cm² não foi utilizado. Cobrimento TQS é dado do modelo, sem preencher
cover_cm=null do PDF ou certificar execução. Gamma_f default da API é None;
1,4 veio do registro, não do dimensionador. Camadas enviadas sem d explícito,
acionando o posicionamento automático do Concretopy.

```json
{
  "geometry": {
    "bw": 19,
    "h": 72,
    "cobrimento": 2.5,
    "diametro_estribo_mm": 5,
    "unit": "cm (diâmetro em mm)"
  },
  "materials": {
    "fck_mpa": 40,
    "fyk_mpa": 500,
    "Es_mpa": 210000
  },
  "layers": [
    {
      "numero_barras": 3,
      "diametro_mm": 12.5,
      "d_cm": null
    },
    {
      "numero_barras": 1,
      "diametro_mm": 12.5,
      "d_cm": null
    }
  ],
  "coefficients": {
    "gamma_c": 1.4,
    "gamma_s": 1.15,
    "gamma_f": 1.4
  },
  "verificar_armadura_minima": false,
  "scope": "seção governante; estribo da região que contém esse ponto; não certifica todas as regiões com estribos distintos",
  "executed": true
}
```

## Retorno completo do Concretopy

Áreas, alturas úteis/centroide, linha neutra e resistência calculados somente
pelo Concretopy; todos os campos conservados no JSON.

```json
{
  "as_total_cm2": 4.908738521234052,
  "as_por_camada_cm2": [
    3.6815538909255388,
    1.227184630308513
  ],
  "d_por_camada_cm": [
    68.375,
    65.125
  ],
  "d_equivalente_cm": 67.5625,
  "linha_neutra_cm": 5.781594031605593,
  "x_sobre_d": 0.08557400971849166,
  "limite_x_sobre_d": 0.45,
  "ductilidade_atendida": true,
  "mrd_kncm": 13925.84839156713,
  "mk_equivalente_kncm": 9947.034565405093,
  "hipoteses_validas": true,
  "deformacoes_aco": [
    0.01,
    0.009480775977961474
  ],
  "camadas_escoadas": [
    true,
    true
  ],
  "as_min_cm2": null,
  "armadura_minima_atendida": null,
  "parametros": {
    "modelo": "bloco_retangular_camadas_escoadas_v1",
    "unidade_momento": "kN.cm",
    "unidade_tensao": "MPa",
    "gamma_c": 1.4,
    "gamma_s": 1.15,
    "gamma_f": 1.4,
    "fck": 40,
    "fyk": 500,
    "es": 210000,
    "fcd": 28.571428571428573,
    "fyd": 434.7826086956522,
    "alfa_c": 0.85,
    "lambda": 0.8,
    "ecu": 0.0035,
    "eyu": 0.01,
    "eyd": 0.002070393374741201,
    "eps_c_adotada": 0.0009236746175028279,
    "bw_cm": 19,
    "h_cm": 72,
    "cobrimento_cm": 2.5,
    "diametro_estribo_mm": 5
  },
  "avisos": [
    "Alturas úteis omitidas calculadas pelo critério da planilha VIGAS!K5:K7."
  ]
}
```

## Comparação e diagnósticos independentes

d das camadas: **68,375 cm** e **65,125 cm**; d equivalente **67,5625 cm**.
MRd=**139.2584839156713 kN.m**, gamma_f=**1,4**;
Mk_equivalente=**99.47034565405093 kN.m**.
Comparação exclusivamente Mk_equivalente ≥ Msk, nunca MRd com Msk.
Utilização Msk/Mk_equivalente = **0.618348196093708**.
Só se convertem momentos recebidos de kN.cm para kN.m (divisão por 100).

| Diagnóstico | Resultado |
|---|---|
| Capacidade na seção governante | suficiente |
| Hipóteses do modelo resistente | válidas |
| Ductilidade | atendida pelo critério da API |
| Armadura mínima | não solicitada; null |
| Ancoragem | não verificada; false |
| Desenvolvimento | não verificado; false |
| Livre PDF/TQS | mismatch preservado: 7,110 / 7,120 m |

A resistência corresponde ao estribo do ponto governante. Outras regiões têm
Ø6,3 e Ø5: não se certifica capacidade uniforme de todos os trechos,
espaçamento normativo ou efetividade por ancoragem. Diferença geométrica
permanece sem ajuste/tolerância. Nenhuma outra verificação foi implementada.

## Testes e alterações

**112 testes do engineering-assistant aprovados:** 22 reinforcement_checks,
22 beam_mapping, 29 beam_model, 39 extrator_lst.
Cobrem golden real numérico, API real com d automático, comparação/utilização,
diagnósticos separados, aliases equivalentes, fontes desconhecidas/ausentes,
exclusões, texto/proveniência e imutabilidade.
Nenhum teste de beam_model, beam_mapping ou extrator_lst foi alterado.

Criados: tools/reinforcement_checks/materials.py e test_materials.py.
Modificados: orquestrador, teste golden e README de reinforcement_checks;
.agents/skills/reinforcement-review/references/tqs-beam-data.md;
este relatório e analises/pranchas/V501_positive_flexure_check.json.
Concretopy, documentais, beam_model, modelos TQS e beam_mapping intactos.
