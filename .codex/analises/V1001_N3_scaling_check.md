# V1001 — verificação do escalonamento da N3

05/10/2026. **As duas condições do escalonamento da N3 atendem.**
`complete=true`, `condition_A_passes=true`, `condition_B_passes=true`,
`scaling_passes=true`; diagnósticos vazios. Conclusão limitada ao evento e
às hipóteses registradas, sem aprovação global da viga.

## 1. Objetivo e implementação

Orquestrar as primitivas existentes para verificar duas condições independentes
de interrupção positiva no vão. Produção: `tools/reinforcement_checks/bar_scaling.py`
e `tqs_shear.py`. Fixture: `v1001_scaling.py`. Resultado:
`analises/pranchas/V1001_N3_scaling_check.json`.

V1001/N3/N5 são identificadores do fixture/golden; não existem regras por esses
nomes na produção. Reutilizados regiões geométricas, composição de camadas,
`check_positive_flexure`, `MomentDiagram`, auditoria M MX. e interpretação de
materiais. Resistência, área de barra, geometria das camadas, fbd/lb e al
permanecem no Concretopy. Nenhuma alteração foi feita nesse repositório.

## 2. Evento geométrico N3

N3: 2Ø10, reta, primeira camada inferior, intervalo documental −42 a 608 cm.
Mapping existente: x_comum=x_documental/100+0,600 m, portanto
**N3=[0,180; 6,680] m**. Analisada a interrupção à direita (`cut_side=right`).

O término **6,680 m** continua documental. Não foi ajustado para a seção 11
(6,677333333333333 m), limite de estribo, apoio ou zero do diagrama.
Vão livre: [0,600; 7,720] m; eixos físicos: [0; 8,430] m.

## 3. Composição antes e depois

| Estado no sentido do corte | Região | Marcas | Composição |
|---|---|---|---|
| Antes, limite do lado esquerdo | R3 | N3 + N5 | 4Ø10 na primeira camada inferior |
| Depois, limite do lado direito | R4 | N5 | 2Ø10 na primeira camada inferior |

A diferença before-after identifica N3; N5 permanece em [0,180; 8,130] m.
Usam-se os interiores das regiões adjacentes, sem epsilon. O ponto fechado
geométrico continua contendo N3+N5. JSON conserva marcas, faces, camadas,
bitolas, intervalos documentais/comuns e provenance.

## 4. Capacidade da N5

Seção no evento: bw=19 cm, h=72 cm, estribo N9 Ø5; cobrimento inferior TQS
2,5 cm, dado do modelo sem confirmação de execução. fck=40 MPa documental;
fyk=500 MPa pela regra CA-50 existente; gamma_f=1,4 documental;
gamma_c=1,4 e gamma_s=1,15 dos defaults públicos do Concretopy.

Chamada pública de flexão com **somente N5, 2Ø10**, conservando o centro
físico da camada anterior em d=68,5 cm; remover N3 não desloca N5.

| Retorno Concretopy | Resultado |
|---|---:|
| MRd remanescente | 46,276995622592885 kN.m |
| Mk equivalente remanescente | 33,054996873280636 kN.m |
| As N5 | 1,5707963267948966 cm² |
| Hipóteses resistentes válidas | true |

Capacidade regressada diretamente contra o golden anterior. Não se usa a
capacidade de N3+N5 para localizar x_nec. Chamada e dataclass ficam no JSON.

## 5. Diagrama Msk

VGESFS, registro original **M MX.**, vão 1, referência s541#/normalizacao,
linha 500. Treze pontos existentes, domínio [0,384; 7,936] m, doze segmentos
lineares. Série característica conforme o workflow do engenheiro; valores
confrontados com raw, fontes e posições preservados. Sem extrapolação,
suavização ou discretização adicional.

## 6. Seleção de x_nec

| Cruzamento Msk=Mk equivalente N5 | Ramo | Seleção |
|---|---|---|
| 2,1857211018870064 m | crescente, S3–S4 | preservado, incompatível com o lado |
| **5,709168751478622 m** | decrescente, S9–S10 | selecionado para corte à direita |

Selecionado pelo lado e ramo desde o pico positivo único; não pelo primeiro
ou último global. Todos os candidatos, bases, segmentos, coordenadas decimais
e motivo de seleção permanecem auditáveis. Os dois cruzamentos coincidem
com o golden existente, sem atualizar seus valores.

## 7. Início da queda

**S6: x_decay_start=3,5306666666666664 m, Msk=59,8401783 kN.m.**
Registrado como `piecewise_linear_positive_peak`: máximo da representação
adotada, sem afirmar máximo estrutural exato. Pico único e ramos unimodais.
Platô, máximos incompatíveis e ramo não identificável bloqueiam a seleção.

## 8. Máximo módulo de Vk do vão

Regra `engineer_confirmed_al_shear_selection_v1`. Consideradas as 13 seções
de **ambas** as envoltórias características, não apenas o lado do corte.
Rótulos originais VGESFS: **Q MX. / Q MN.**, grandeza física Vk.

| Campo governante | Resultado |
|---|---:|
| Série | Q MN., envelope min |
| Seção | 13 |
| x | 7,936 m |
| Vk com sinal | −113,39429395 kN |
| Vk_used=max(abs(Vk)) | **113,39429395 kN** |
| Amostras consideradas | 26, sem empate governante |

Q MX. tem máximo módulo 63,87071145 kN e não governa. A origem raw de
cada envoltória é auditada. Seção 13 permanece elegível por pertencer ao vão
físico, mesmo internamente ao apoio. Não se extrapola do domínio amostrado
aos eixos. O máximo de módulo em segmento linear ocorre nos endpoints:
nenhuma interpolação/discretização adicional foi criada. Empates são preservados.

## 9. d utilizado em al

Aplicada a decisão explícita do engenheiro **`engineer_confirmed_al_effective_depth_v1`**,
registrada em `tools/reinforcement_checks/al_effective_depth.md`:

```text
d_for_al = sum(As_i*d_i)/sum(As_i)
```

Conjunto de referência: barras tracionadas participantes da seção resistente
**imediatamente antes** da interrupção, aqui **N3+N5**.
Reutilizado o resultado de flexão de R3 já produzido pelo Concretopy,
sem recalcular posições/centroide independentemente.

| Contribuição anterior | As | Distância do centro à face comprimida |
|---|---:|---:|
| N3, 2Ø10 | 1,5707963267948966 cm² | 68,5 cm |
| N5, 2Ø10 | 1,5707963267948966 cm² | 68,5 cm |
| Conjunto resistente | 3,141592653589793 cm² | **d_equivalente=68,5 cm** |

**d_for_al=68,5 cm**. Coincide com d da camada porque todas as barras
anteriores estão na mesma camada; a seleção física é N3+N5.
Não se adotou d isolado de N3/N5, outra região ou célula de planilha.

Em múltiplas camadas, usa-se o centroide ponderado retornado pelo Concretopy,
conservando áreas, centros e composição. Sem resultado regional anterior,
a API é chamada para essa composição, sem fabricar demanda. Recusa do modelo
ou geometria/centroide não resolvido mantém `d_for_al_unresolved`.

A decisão resolve a pendência de regra identificada na auditoria anterior
(global vs grupos cumulativos), **somente para escalonamento no vão**.
Não define d para a futura ancoragem em apoio.

## 10. Cálculo de al

`Concretopy.calcular_al`, concreto 40 MPa, b=19 cm, d=68,5 cm,
Vk_abs=113,39429395 kN, gamma_f=gamma_c=1,4. Modelo da primitiva:
estribos verticais e Vc=Vc0, conforme hipóteses do workflow.

| Retorno da API | Valor |
|---|---:|
| Vsd | 158,75201153 kN |
| fctd | 1,7544106429277193 MPa |
| Vc0 | 137,0019271062256 kN |
| Branch | vsd_gt_vc0 |
| al_base | 249,98782942466133 cm |
| al_min | 34,25 cm |
| al_max | 68,5 cm |
| **al limitado utilizado** | **68,5 cm** |

al_base e al limitado estão separados. O mesmo **al limitado** alimenta A/B,
com o máximo módulo de Vk do vão e o centroide anterior. Não se recalcula
al em x_nec ou no pico. Equações de decalagem continuam no Concretopy.

## 11. Aderência

N3 horizontal, primeira camada inferior, sem forma deslizante documentada.
Geometria: **y=h−d_camada=72−68,5=3,5 cm**, centro da barra à face inferior.
Como h=72≥60 cm, fronteira boa/má=h−30=42 cm.
**3,5≤42: boa aderência**, pela `engineer_confirmed_bond_condition_v1`.
Fronteira pertence à boa. A classificação usa geometria, não função positiva.
O centro físico da barra e o centroide escolhido para al têm papéis distintos.

## 12. lb básico

`Concretopy.calcular_ancoragem`, Ø10 da marca interrompida, boa aderência,
materiais/coeficientes registrados. As calculada=As efetiva=área das duas
barras N3, obtida via Barra: ancoragem integral em fyd, sem redução por
excesso de aço. Sem comprimento disponível fornecido à primitiva.

**lb básico=27,5358445519597 cm**. A condição B usa `lb_cm`.
Resposta integral preserva fbd, lb_min, lb_nec e atende separados; atende da
primitiva não decide o escalonamento. Sem redução por dobra/gancho.

## 13. Condição A — al + 10φ

Bitola interrompida N3: φ=10 mm=1 cm; **10φ=10 cm**.

- Disponível: (6,680−5,709168751478621…)*100 = **97,083124852137875… cm**.
- Exigido: **68,5+10=78,5 cm**.
- Resultado A: **true**.
- Reserva: aproximadamente **18,5831 cm**.

Comprimento preserva a coordenada decimal operacional do cruzamento;
comparação não usa arredondamento editorial.

## 14. Condição B — al + lb

- Disponível: (6,680−3,5306666666666664)*100 = **314,93333333333336 cm**.
- Exigido: **68,5+27,5358445519597=96,0358445519597 cm**.
- Resultado B: **true**.
- Reserva: aproximadamente **218,8975 cm**.

A e B permanecem independentes; ambas usam o mesmo al.

## 15. As 17 respostas e conclusão

| Pergunta | Resposta |
|---|---|
| 1. Término geométrico N3 | 6,680 m |
| 2. Armadura que permanece | N5, 2Ø10, primeira camada inferior |
| 3. Mk equivalente | 33,054996873280636 kN.m |
| 4. Ponto de suficiência relevante | 5,709168751478622 m, ramo descendente |
| 5. Início da queda | S6, 3,5306666666666664 m |
| 6. Máximo módulo Vk | 113,39429395 kN, Q MN., S13 |
| 7. d utilizado e motivo | 68,5 cm, centroide tracionado anterior N3+N5, retornado pelo Concretopy |
| 8. al | 68,5 cm, limitado |
| 9. Aderência | Boa, y=3,5 cm |
| 10. lb básico | 27,5358445519597 cm |
| 11. Disponível A | 97,083124852137875… cm |
| 12. Exigido A | 78,5 cm |
| 13. A atende? | true |
| 14. Disponível B | 314,93333333333336 cm |
| 15. Exigido B | 96,0358445519597 cm |
| 16. B atende? | true |
| 17. Escalonamento aprovado? | Sim, para esse evento/escopo, scaling_passes=true |

Todas as dependências estão resolvidas, capacidade válida, referências únicas,
comprimentos positivos e duas condições atendidas. False é reservado a uma
verificação completa com falha; null continua representando casos inconclusivos.

## 16. Provenance e referências

JSON preserva modelos regionais em audit_context, composições, fontes e
transformações das barras, materiais, diagrama/candidatos/seleção, séries e
governantes de cortante, centroide anterior e suas contribuições, chamadas,
respostas completas, assinaturas e hashes das APIs locais. Entradas e
implementação possuem SHA-256. Ponteiros compartilhados resolvem e são testados.

Consultados AGENTS.md, skill reinforcement-review e referências de prancha,
revisão/TQS; beam_model, beam_mapping e reinforcement_checks; relatórios V1001,
moment_linear_interpolation; auditoria da planilha e concretopy_al_implementation;
API pública local de flexão, geometria, ancoragem e al.

O arquivo com nome exato `concretopy_longitudinal_anchorage_primitives.md`
não foi encontrado nos repositórios consultados. Seu contrato foi verificado
em `../concretopy/docs/ancoragem.md`, exports e `verificacoes/ancoragem.py`.
Não se atribui leitura a arquivo ausente.

Hash antigo do contexto V1001_V9001 difere somente por CRLF/LF: a normalização
CRLF→LF reproduz exatamente o hash registrado no mapping. `mapping_input_audit`
registra hashes real/esperado e `CRLF_to_LF_only_hash_match`; nenhum arquivo
primário/contexto foi regravado, nem se aceita alteração de conteúdo.

A/B, aderência, cortante e seleção de d são regras confirmadas do workflow.
Não foi consultado o texto normativo integral nesta implementação; referências
e limitações normativas das primitivas continuam documentadas pelo Concretopy.

## 17. Testes

Suíte integral executada com Python 3.10-32 e Concretopy local atual:
**223 testes aprovados** — 39 extrator_lst, 29 beam_model, 33 beam_mapping,
122 reinforcement_checks (80 anteriores + 42 novos).

Por diretório:
`python -B -m unittest discover -s tools/<diretorio> -p 'test_*.py'`.

Cobertos A–T solicitados: ambas passam, somente A falha, somente B falha,
ambas falham, corte à esquerda, ausência/seleção/ambiguidade de cruzamento,
platô, capacidade insuficiente/suficiente em todo ramo, governança positiva/
negativa/empates de cortante, aderência boa/má/fronteira, centroide anterior
não resolvido, recusa do Concretopy e intervalo inconsistente.

Complementos: múltiplas camadas com áreas/bitolas distintas para ambos os lados,
centroide diferente da barra cortada e remanescente, reutilização comprovada
sem recalcular flexão/geometria anterior, centroide inválido, lb básico separado
de lb_nec, bitola interrompida diferente da remanescente, apoio/gancho bloqueados,
múltiplos cortes, gaps, comprimentos negativos, mudança de configuração,
raw divergente, envoltória ausente, imutabilidade e ponteiros de provenance.

Preservadas as regressões V501 positive flexure, V1001 regional, grouped
support mapping, moment interpolation e capacidade/cruzamentos N5. Nenhum
golden anterior foi atualizado para acomodar mudança de resultado.

## 18. Limitações

Uma marca interrompida, um evento dentro do vão livre mapeado, flexão positiva,
representação unimodal simples, configuração constante entre referências e
corte, barras retas e hipóteses físicas explícitas. Sem apoio, grampos,
negativos, suspensão, múltiplas interrupções simultâneas ou ancoragem da
remanescente. Sem mínimo, cisalhamento, confinamento ou aprovação global.
Diferença histórica de revisão PDF/TQS permanece contexto conhecido.

A regra de d foi confirmada somente para escalonamento dentro do vão.
**A aprovação refere-se às condições A e B da N3 nesse evento.**
