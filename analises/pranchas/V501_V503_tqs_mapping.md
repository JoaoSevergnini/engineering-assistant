> Historical analysis: superseded where indicated by [TQS semantics update](V501_V503_tqs_semantics.md). The permanent length rule is now confirmed; reactions are consolidated and the VAO/PONTO parser failure is fixed. Hashes below refer to the previous outputs.

# V501/V503 ? compatibilidade entre detalhamento e TQS

An?lise documental de 02/10/2026. Sem verifica??o estrutural, altera??o de sinais,
modifica??o do detalhamento ou novo schema. O agrupamento da prancha n?o implica
igualdade de solicita??es: V501 e V503 foram extra?das e consolidadas separadamente.

## Ferramentas e fontes

Reutilizados `tools/extrator_lst/extrair_viga_lst.py` e `consolidar_viga.py`, sem
altera??es. Examinados seus README, CONSOLIDACAO e c?digo; o `tools/beam_model`
existente fornece o outro modelo, tamb?m sem altera??es nesta etapa.
Pasta LST: `C:\TQS\24-155-COLLINE-RESIDENCIAL-R60\DIFERENCIADO\VIGAS`.
13 arquivos lidos, 11 blocos extra?dos por viga; CONVF2 e RESESTERR vazios.

Principais fontes: VGESFS e RELDTVGS (geometria, apoios, esfor?os e rea??es);
RELDTFPS/RELDTFNG (geometria detalhada, excentricidades, s?ries de flex?o e refer?ncia
textual aos eixos/faces); RELDTVeT (etapas de cortante/tor??o); RELGER (legenda DEPEV,
rea??es, abscissa de m?ximo e intervalos); ESTRIB (intervalos e comprimento distinto).
FLEXPS/FLEXNG acrescentam resumos e comprimentos arredondados. ORDCON/RELPREDI
permanecem no invent?rio/raw, sem novas correspond?ncias adotadas neste relat?rio.
As linhas citadas abaixo s?o f?sicas, base 1. Os JSONs mant?m hashes e ponteiros.

## Correspond?ncias confirmadas

| Propriedade | Detalhamento | V501 TQS | V503 TQS |
|---|---|---|---|
| Identifica??o | V501=V503, quantidades por viga | V501 | V503 |
| Se??o | 19 ? 72 cm | 0,19 ? 0,72 m | 0,19 ? 0,72 m |
| V?os f?sicos | 1 | 1 | 1 |
| Apoio esquerdo | P2A/P2B | P2A | P2B |
| Apoio direito | P1A/P1B | P1A | P1B |
| Dimens?es escritas dos apoios | 120 / 142 cm | 1,20 / 1,42 m | 1,20 / 1,42 m |
| Comprimento | livre: 711 cm | refer?ncia: 7,552 m | refer?ncia: 7,552 m |

A correspond?ncia dos pares de nomes pode agora ser estabelecida pela identifica??o
expl?cita do bloco TQS, n?o pela ordem dos nomes na prancha. Esta conclus?o fica
somente neste relat?rio; o beam_model n?o foi regravado. Fontes: VGESFS 1360?1379
(V501), 1649?1668 (V503); RELDTVGS 3774?3782 e 4542?4550.
A ordem do v?o ? P2?P1, compat?vel com esquerda?direita na prancha; a lista global
`beam.supports` ? ordenada por nome e n?o deve ser usada para deduzir orienta??o.
Usar `beam.spans[0].support_ids`.

O v?o 1 geral corresponde ao v?o interno 2 nos relat?rios detalhados. Os registros
extremos de comprimento zero s?o documentais, n?o balan?os nem v?os adicionais.

## Correspond?ncias prov?veis

A diferen?a principal de comprimento ? compat?vel com refer?ncias geom?tricas
distintas: eixo efetivo de apoio, eixo do pilar e face. H? evid?ncia textual al?m
da coincid?ncia num?rica, descrita abaixo, mas n?o uma transforma??o completa
validada para os 13 pontos. A equival?ncia de revis?o entre a prancha R00 e os
relat?rios de 30/09/2026 tamb?m precisa ser confirmada.

## Diverg?ncias

- V?o livre documental: 711 cm; os intervalos do RELGER indicam 0?712 cm
  (V501 linhas 54/57; V503 178/181). Diferen?a de 1 cm, n?o absorvida por toler?ncia.
- Comprimento de refer?ncia 755,2 cm; ESTRIB imprime 843 cm e intervalos 60?772 cm
  (V501 690?695; V503 853?858). N?o s?o intercambi?veis automaticamente.
- Cada consolidado TQS registra 8 warnings: fck 39,2266/40 MPa, a?o CA-50A/CA-50,
  comprimento/largura/altura divergentes entre etapas, registros de comprimento zero
  e duas excentricidades conflitantes. fck, a?o e excentricidades ficam null.
- RELDTVeT imprime cabe?alho em cm com n?meros compat?veis com outra escala:
  o pipeline preserva a convers?o literal (0,076 / 0,002 / 0,007 m) como alternativa,
  preferindo a geometria geral documentada. N?o corrigido nesta an?lise.
- V501 e V503 t?m s?ries e rea??es diferentes apesar do detalhamento agrupado.

## Sistema de coordenadas

**Detalhamento:** x em cm, origem na face interna esquerda, positivo para a direita;
S1 = [0,711]. Coordenadas negativas de barras dentro do apoio s?o permitidas.
As faces externas dos apoios e as posi??es dos contornos IB1/IB2 est?o desconhecidas.

**TQS consolidado:** comprimento em m; se??es numeradas 1?13, mas todas as s?ries
possuem `positions=null`. O n?mero da se??o n?o ? uma abscissa. N?o h? sistema global
x estruturado nem declara??o de espa?amento uniforme no modelo.

**Evid?ncias nos LST:**

1. RELGER linha 31 define DEPEV como dist?ncia do eixo do pilar ao eixo efetivo de
   apoio da viga. RELDTFPS 12765?12767 / 15275?15277 fornece bp=120/142 cm e
   exc=38,4/49,4 cm. As tabelas gerais arredondam exc para 0,38/0,49 m.
2. RELDTFPS 12868/12902 e 15386/15420 chama os momentos extremos de momentos no
   ?Eixo do pilar? e distingue a face nas linhas seguintes. Seus valores correspondem
   aos extremos das s?ries, corroborando a orienta??o, mas o texto n?o distingue ali
   eixo f?sico de eixo efetivo com precis?o suficiente para automatizar a origem.
3. A tabela de corre??o dos v?os em RELDTVGS 3821?3825 / 4589?4593 mant?m 7,552 m;
   n?o fornece um deslocamento global nem abscissas de cada ponto.
4. RELGER 43/167 cont?m `Abcis.=440` para o m?ximo positivo; essa abscissa isolada
   n?o define os outros 12 pontos nem sua origem. ESTRIB utiliza outros intervalos.

**Hip?tese geom?trica para confirma??o, n?o aplicada:** se as excentricidades
representam deslocamentos dos eixos efetivos para dentro do v?o, as dist?ncias
face?eixo efetivo seriam 120/2?38,4=21,6 cm e 142/2?49,4=21,6 cm. Ent?o:

- dist?ncia entre eixos f?sicos: 755,2+38,4+49,4=843,0 cm;
- livre entre faces: 755,2?21,6?21,6=712,0 cm;
- origem no eixo efetivo esquerdo: `x_TQS_cm = x_detalhamento_cm + 21,6`;
- origem no eixo f?sico esquerdo: `x_eixo_pilar_cm = x_detalhamento_cm + 60`.

A legenda DEPEV, os bp/exc e o intervalo 712 d?o suporte ? hip?tese, mas n?o
confirmam o sentido alg?brico das excentricidades nem o posicionamento de todas as
se??es. Al?m disso, 712 n?o ? 711. Portanto **n?o foi estabelecida uma transforma??o
confi?vel para aplica??o computacional**. Nenhum offset, escala, interpola??o ou
uniformiza??o foi implementado. Em particular, n?o se adotou `(i?1)*L/12`.
H? um ?nico v?o em cada caso; extrapolar uma f?rmula a vigas de v?rios v?os exige
origens locais, offsets por apoio/v?o e orienta??o explicitamente documentados.

## Esfor?os dispon?veis

Cada viga possui 14 s?ries de 13 posi??es l?gicas, nenhuma s?rie n?o atribu?da ao
v?o. Treze valores num?ricos por s?rie, exceto M negativo de entrada da flex?o
positiva: somente 2 extremos preenchidos e 11 null. Todas as abscissas s?o null.
As cinco s?ries `model_input` s?o caracter?sticas conforme RELDTVGS 3792/4560;
n?o devem ser chamadas de esfor?os de c?lculo nem misturadas com outras etapas.

Unidades originais: tf e tf?m nas entradas gerais; tf?cm na flex?o detalhada.
Convers?o existente: 1 tf=9,80665 kN; 1 tf?cm=0,0980665 kN?m, sem troca de sinal.
A tabela abaixo identifica cada s?rie, fase e linhas de origem para as duas vigas.

| Grandeza / envelope | Etapa | Unidade consolidada | V501: fonte/linha | V503: fonte/linha |
|---|---|---|---|---|
| bending_moment / max | model_input | kN.m | RELDTVGS.LST:3800; VGESFS.LST:1373 | RELDTVGS.LST:4568; VGESFS.LST:1662 |
| bending_moment / min | model_input | kN.m | RELDTVGS.LST:3796; VGESFS.LST:1369 | RELDTVGS.LST:4564; VGESFS.LST:1658 |
| bending_moment / negative | negative_flexure_after_positive_removal | kN.m | RELDTFNG.LST:9630 | RELDTFNG.LST:11690 |
| bending_moment / negative | negative_flexure_input | kN.m | RELDTFNG.LST:9624 | RELDTFNG.LST:11684 |
| bending_moment / negative | positive_flexure_input | kN.m | RELDTFPS.LST:12755 | RELDTFPS.LST:15265 |
| bending_moment / positive | positive_flexure_input | kN.m | RELDTFPS.LST:12756 | RELDTFPS.LST:15266 |
| shear / max | model_input | kN | RELDTVGS.LST:3798; VGESFS.LST:1371 | RELDTVGS.LST:4566; VGESFS.LST:1660 |
| shear / max | shear_final_absolute | kN | RELDTVeT.LST:10223 | RELDTVeT.LST:12890 |
| shear / max | shear_initial_absolute | kN | RELDTVeT.LST:10184 | RELDTVeT.LST:12851 |
| shear / max | shear_torsion_input | kN | RELDTVeT.LST:10151 | RELDTVeT.LST:12818 |
| shear / min | model_input | kN | RELDTVGS.LST:3794; VGESFS.LST:1367 | RELDTVGS.LST:4562; VGESFS.LST:1656 |
| shear / min | shear_torsion_input | kN | RELDTVeT.LST:10152 | RELDTVeT.LST:12819 |
| torsion / max | model_input | kN.m | RELDTVGS.LST:3802; VGESFS.LST:1375 | RELDTVGS.LST:4570; VGESFS.LST:1664 |
| torsion / max | shear_torsion_input | kN.m | RELDTVeT.LST:10171 | RELDTVeT.LST:12838 |

Sinais preservados: M de entrada admite valores negativos nos extremos e positivos
no interior; Q admite positivos e negativos; MT,max tamb?m cont?m ambos os sinais.
O esquema n?o explicita eixos locais ou regra vetorial de sinais. Assim, n?o se
atribuiu sinal f?sico adicional ? tor??o. A fase de flex?o positiva imprime magnitudes
positivas para M,neg; as fases `shear_*_absolute` imprimem m?dulos. S?o dados das
respectivas etapas, n?o mudan?as de sinal feitas na integra??o. Esfor?o normal n?o
foi encontrado como s?rie nos blocos consultados e n?o ? suportado pela classifica??o
atual do consolidador; aus?ncia n?o significa N=0.

## Rea??es e apoios indiretos

O schema consolidado atual **n?o inclui rea??es**. Elas existem normalizadas nos
raw (`normalizacao.tipo=reacao_apoio`) e nos LST. Valores abaixo de VGESFS, em tf,
na ordem m?ximo/m?nimo, sem transformar o sinal de rea??o em carga na viga receptora:

| Viga | Apoio | M?ximo | M?nimo | VGESFS linha |
|---|---|---:|---:|---:|
| V501 | P2A | 7,174 | 4,071 | 1378 |
| V501 | P1A | 10,789 | 4,163 | 1379 |
| V503 | P2B | 7,216 | 4,051 | 1667 |
| V503 | P1B | 11,160 | 4,540 | 1668 |

RELDTVGS 3829?3830 / 4597?4598 imprime valores arredondados; variantes permanecem
nas fontes, n?o foram escolhidas ou fundidas silenciosamente. Essas rea??es s?o
nos apoios principais da viga estudada, n?o rea??es dos contornos IB1/IB2.

A busca nominal em outros blocos identificou liga??es expl?citas:

| Viga apoiada | Viga receptora, apoio n? 2 | M?ximo (tf) | M?nimo (tf) | VGESFS linha | RELDTVGS geometria / rea??o |
|---|---|---:|---:|---:|---|
| V541 | V501 | 2,907 | 2,284 | 828 | 2332 / 2380 |
| V542 | V501 | 3,887 | 0,725 | 1358 | 3716 / 3764 |
| V559 | V503 | 2,913 | 2,284 | 954 | 2728 / 2776 |
| V560 | V503 | 3,983 | 0,886 | 1647 | 4484 / 4532 |

Essas rela??es s?o seguras **entre identifica??es do TQS**, corroboradas pelo campo
Continua=VIGA do RELDTVGS. N?o h? coordenada na viga receptora nessas linhas.
Dois elementos por receptora s?o compat?veis com dois contornos, mas a correspond?ncia
V541/V542 ou V559/V560 com IB1/IB2 n?o est? confirmada. Nenhuma rea??o foi atribu?da
a N7 por proximidade ou magnitude. Tamb?m n?o h? combina??o identificada que permita
somar os m?ximos como um ?nico caso de carregamento.

O pipeline adicional gerou raw de V541 e V559. Para V542/V560, falhou em
`extrair_viga_lst.py:127`: a express?o de s?rie captura linhas locais
`M(-) = ... VAO= 2 PONTO= 6` (VGESFS 1346/1353 e 1635/1642), e tenta converter
`PONTO=` em float. As rea??es dessas duas vigas acima foram lidas diretamente das
linhas citadas, n?o de um JSON gerado com sucesso. Nenhum arquivo parcial foi adotado.

## Informa??es ausentes e pr?ximas altera??es a avaliar

1. Confirmar revis?o geom?trica e resolver 711 versus 712 cm sem corrigir a prancha
   automaticamente; esclarecer eixo efetivo/f?sico e sinais das excentricidades.
2. Obter defini??o das abscissas das 13 se??es e da origem de `Abcis.=440`.
   Os LST consultados trazem ?ndices e uma abscissa de m?ximo, n?o uma tabela completa.
   Somente ap?s documentar essa conven??o avaliar normaliza??o no extrator e propaga??o
   de `positions` no consolidador. N?o preencher pontos por coincid?ncia num?rica.
3. Incorporar futuramente rea??es no consolidador: dados j? existem normalizados no raw.
   Documentar extens?o do schema antes de implement?-la, preservando unidade, etapa,
   envelope, v?nculo com apoio, variantes e proveni?ncia.
4. Corrigir genericamente o reconhecimento de s?ries no extrator, distinguindo s?ries
   de 13 valores de mensagens locais `VAO/PONTO`, com regress?es V542/V560; n?o criar
   exce??es por n?mero de viga. Isso ? necess?rio para extrair suas rea??es pelo pipeline.
5. Modelar futuramente rela??es entre vigas a partir dos apoios nominais j? extra?dos,
   conservando a identidade da viga de origem. A posi??o na receptora e associa??o a
   IB1/IB2 exigem outra evid?ncia geom?trica; n?o constam das linhas de rea??o.
6. Resolver materiais/excentricidades conflitantes e documentar a conven??o f?sica
   dos sinais antes de qualquer uso resistente. N?o selecionar etapas incompat?veis.

Nenhuma altera??o de parser, consolidador, schema, beam_model ou teste foi feita.
N?o foi criada ferramenta de integra??o. Leitura de valores em se??es de ancoragem
serviu apenas para identificar eixos/faces; nenhum c?lculo de ancoragem foi realizado.

## Valida??o e arquivos

27 testes de `tools/extrator_lst` e 29 de `tools/beam_model`: **56 passaram, sem skips**.
Incluem V504 documental, consolida??o TQS, V502 e V501/V503 beam_model. A falha de
extra??o adicional V542/V560 n?o ? coberta pela su?te atual e permanece documentada.

Criados: V501_tqs_raw.json, V501_tqs.json, V503_tqs_raw.json, V503_tqs.json,
V541_tqs_raw.json, V559_tqs_raw.json e este relat?rio. Os consolidados usam o schema
`consolidated_beam` 1.0 existente. Raw e consolidado conservam hashes/proveni?ncia.

### Impress?es digitais dos modelos comparados

- `V501_V503_beam_model.json`: `a454b67725ad2b57d43eb67db043697adbfd99f64c4e46b01252187fc1868506`
- `V501_tqs.json`: `4c4e72fc7e422b373e17df81926a2d0f3cd073dc28d7528c7703c1d494d3d307`
- `V503_tqs.json`: `1217c4c5fadbebeb2372ba70d041781bc41cc32a85e34192a6d7b339344bd93a`
