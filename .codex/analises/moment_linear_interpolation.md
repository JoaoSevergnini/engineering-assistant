# Diagrama característico Msk — interpolação linear

04/10/2026. Regra explícita do engenheiro implementada; golden real V1001.
Não avalia corte de N3, ancoragem, desenvolvimento ou decalagem normativa.

## 1. Decisão e arquitetura

João confirmou que as ferramentas TQS deste fluxo trabalham com 13 pontos;
os relatórios disponíveis não contêm série mais refinada a buscar. Para esforços
entre pontos consecutivos da mesma série, adota-se interpolação estritamente
linear, sem extrapolação. Regra permanente:
`engineer_confirmed_tqs_linear_interpolation_v1`, registrada em
`.agents/skills/reinforcement-review/references/tqs-beam-data.md`.

Isso é decisão do processo, não descrição de algoritmo interno do TQS.
`tools/reinforcement_checks/moment_diagram.py` representa/interroga os esforços.
`v1001_moment_interpolation.py` é fixture de integração, consumindo a API genérica
e a configuração auditada pela infraestrutura de regiões existente. Cálculo
resistente permanece no Concretopy. beam_model e beam_mapping não foram alterados.
Verificações discretas anteriores continuam intactas.

## 2. Entradas e dados primários

Arquivos em analises/pranchas: V1001_beam_model.json, V1001_tqs.json,
V1001_tqs_positions.json, V1001_beam_mapping.json e V1001_tqs_raw.json.
Saída nova: **V1001_moment_linear_interpolation.json**. CLI confere hashes do
mapping, contexto/entradas relacionadas e raw; registra hashes dos módulos,
interface/implementação Concretopy e entradas.

Série reutiliza audited_moment_series: fonte VGESFS.LST, rótulo original
M MX., vão 1, quantity=bending_moment, envelope=max, stage=model_input,
unit=kN.m, valores confrontados com raw. Referência s541#/normalizacao,
registro original linha 500. A natureza característica vem da política do
engenheiro. Não se seleciona pelo nome max isoladamente.

Os pontos primários mantêm section, position, value, tipo tqs_section e
provenance por posição/valor/série. Não foram substituídos pelos pontos derivados.

## 3. Segmentos e fórmula

`MomentDiagram(points, provenance)` exige pelo menos dois pontos em sequência
estritamente crescente. Não ordena silenciosamente entradas, não aceita x
duplicado (mesmo com valores iguais), valores não finitos ou comprimentos de
série incompatíveis. Número de pontos genérico: n pontos geram n−1 segmentos;
V1001 gera 12 segmentos a partir dos 13 pontos existentes.

Cada segmento conserva IDs das duas seções, extremos x/M, inclinação, status
e dois pontos-base. Para x_i < x < x_j:

```text
M(x) = M_i + (M_j − M_i) · (x − x_i)/(x_j − x_i)
```

Não se utiliza spline, suavização, módulo dos momentos, reconstrução de cargas
ou discretização incremental. O diagrama independe dos intervalos N3/N5.

## 4. Consulta, domínio, gaps e precisão

`moment_at_x(x)` retorna valor, tipo de fonte, segmento(s), pontos-base e regra.
Se x coincide exatamente com seção, retorna o número documental original,
sem interpolação; em uma seção interna registra ambos os segmentos adjacentes.
Ponto intermediário recebe source_type=linear_interpolation.

Domínio V1001: **[0,384; 7,936] m**, não [0; 8,430] m dos eixos físicos.
Fora dele: outside_sampled_domain, sem valor. Momento null em um extremo torna
o segmento unresolved_missing_value. Não se salta o gap. Seção conhecida
permanece consultável mesmo quando seu segmento vizinho tem momento ausente.

Comparações exatas sem epsilon. Decimal(str(valor publicado)), contexto local
de **50 dígitos**, sem arredondamento editorial intermediário. Não se afirma
aritmética racional exata: divisões periódicas usam essa precisão explícita.
Valores derivados no JSON têm número float interoperável e string decimal
operacional; esta última conserva a precisão além do limite binary64. Os valores
primários permanecem os números originais. Relatórios podem arredondar exibição.

## 5. Cruzamentos analíticos

Para extremos diferentes e limite dentro do intervalo de momentos:

```text
x_cross = x1 + (M_limit − M1) · (x2 − x1)/(M2 − M1)
```

Limite igual a extremo usa a coordenada original exata. `find_crossings` retorna
todos os eventos ordenados, direção crescente/decrescente/constante, pontos-base,
segmentos e provenance. Eventos na seção compartilhada são deduplicados por x
Decimal exato, preservando ambos os segmentos. Segmento constante no limite
retorna coincident_segment com intervalo, nunca um único x. Constante diferente
ou limite fora da faixa não gera cruzamento. Pontos no extremo de um segmento
coincidente são agregados ao intervalo correspondente.

Gaps são enumerados e tornam a busca incomplete_missing_values: ausência de
cruzamento em segmentos avaliáveis não equivale a ausência global comprovada.
Sem gaps, retorno vazio declara ausência no domínio amostrado. Limites zero e
negativos são permitidos; sinais são preservados, sem interpretação normativa.

## 6. Golden S11 → S12 e término de N3

| Ponto | x (m) | Msk (kN.m) | Tipo |
|---|---:|---:|---|
| S11 | 6,677333333333333 | +3,16754795 | TQS_SAMPLE_POINT |
| S12 | 7,3066666666666675 | −26,0072358 | TQS_SAMPLE_POINT |
| Fim geométrico N3 | 6,680 | +3,0439259849576117 | evento de armadura + LINEAR_INTERPOLATED_POINT |
| Zero entre S11/S12 | 6,745660952380952 | 0 | cruzamento linear analítico |

Inclinação SEG11 ≈ −46,35823689088974457 kN.m/m. Decimal operacional do momento
no fim N3: `3.0439259849576118950705125256135419773337713732008`.
Decimal do zero: `6.7456609523809521742857142857142857142857142857143`.

A consulta do fim de N3 é obtida da coordenada mapeada, não de um literal usado
para forçar o resultado. Conserva separadamente reinforcement_event_point, marca,
fim geométrico, intervalo/mapping e source_type=linear_interpolation com bases
S11/S12. O x do evento não é um ponto TQS.

Há também zero crescente entre S2/S3 em x≈1,2552876785475904 m.

## 7. Capacidade isolada N5 pelo Concretopy

Configuração documental aplicável imediatamente à esquerda do fim N3: região
R3; bw=19 cm, h=72 cm, estribo N9 Ø5 mm; cobrimento inferior TQS=2,5 cm
(dado do modelo, não confirmação de execução/PDF). Material auditado fck=40 MPa,
CA-50/CA-50A normalizado fyk=500 MPa; Es=210000 MPa; gamma_f=1,4 documental;
gamma_c=1,4 e gamma_s=1,15 conforme defaults explícitos da API.

Composição isolada da N5: **2Ø10 na primeira camada**, derivada de layers=[2].
N5 cobre geometricamente o evento. Não se inclui N3 nessa chamada, nem se
presume efetividade por ancoragem. d omitido para posicionamento automático.
API verificar_flexao_viga_retangular, sem equações resistentes locais.

| Retorno N5 | Valor |
|---|---:|
| As total/única camada | 1,5707963267948966 cm² |
| d camada/equivalente | 68,5 cm |
| Linha neutra | 1,8501100901137897 cm |
| x/d | 0,02700890642501883 |
| Limite x/d retornado | 0,45 |
| MRd | 46,276995622592885 kN.m |
| Mk equivalente | 33,054996873280636 kN.m |

Dataclass completa preservada, incluindo As por camada, d, deformações,
camadas escoadas, hipóteses, ductilidade, parâmetros e avisos. MRd/Mk originais
também estão em kN.cm. Hipóteses válidas=true; ductilidade=true; mínimo=null,
não solicitado; ancoragem=false; desenvolvimento=false; bar_cut_checked=false.

## 8. Todos os cruzamentos com Mk equivalente N5

| x (m, float interoperável) | Segmento | Direção | M_limit (kN.m) |
|---:|---|---|---:|
| 2,1857211018870064 | S3 → S4 | crescente | 33,054996873280636 |
| 5,709168751478622 | S9 → S10 | decrescente | 33,054996873280636 |

Decimais operacionais:

```text
2.1857211018870062755858610411173450428745680077234
5.7091687514786212464603828583986898228401253752863
```

Não há seleção automática de x_nec. Os eventos são propriedades do diagrama
linear com o limite constante calculado na configuração indicada. Não demonstram
que a configuração seja válida em todo o vão ou que N3 possa ser cortada ali.

## 9. Máximo discreto e máximo da representação

Maior positivo documental: **S6**, x=3,5306666666666664 m,
Msk=59,8401783 kN.m. É também o máximo positivo da representação linear
completa, pois cada segmento fica entre seus extremos. Isso não é afirmação
sobre o máximo exato do diagrama estrutural real. Ambos os níveis são registrados
separadamente; gaps impedem declarar o máximo global da representação.

## 10. Testes e regressões

28 testes novos cobrem crescimento, queda, mudança de sinal, endpoints,
domínio, gaps, duplicatas, ordem, cruzamentos interiores/extremos/coincidentes,
constantes, múltiplos eventos, deduplicação, precisão, sequência genérica, golden
S11/S12, fim N3, 13 valores originais, capacidade real N5, cruzamentos e máximo.

Suíte completa: 39 extrator_lst + 29 beam_model + 33 beam_mapping +
80 reinforcement_checks = **181 testes aprovados**. V501 e V1001 anteriores
continuam cobertos pelas regressões existentes, sem alteração de seus goldens.
V501: Msk=61,5073088; Mk=99,47034565405093 kN.m; utilização=0,618348196093708.
V1001 anterior: Msk=59,8401783; Mk N3+N5=65,387969862408 kN.m;
utilização=0,9151557759924052.

## 11. Limitações e próximo passo

Sem ancoragem, al, lb, 10φ, decalagem normativa, corte validado, efetividade
parcial, flexão negativa, cisalhamento, suspensão ou torção. Relações indiretas
e equivalência de revisão PDF/TQS permanecem as lacunas já documentadas.
O próximo passo poderá consumir os eventos/interrogações para estudar
escalonamento com regras normativas e desenvolvimento explicitamente definidos;
nenhuma dessas decisões foi antecipada nesta tarefa.

Criados: moment_diagram.py, v1001_moment_interpolation.py, test_moment_diagram.py,
V1001_moment_linear_interpolation.json e este relatório. Modificados:
tqs-beam-data.md e tools/reinforcement_checks/README.md. Concretopy, beam_mapping,
parsers, modelos primários e resultados anteriores não foram alterados.
