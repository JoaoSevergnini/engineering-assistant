# V536=V565 — escalonamento da N3 em duas camadas

05/10/2026. **As condições A e B do corte esquerdo da N3 atendem nas duas vigas**, com os dados e hipóteses descritos abaixo. `complete=true` e `scaling_passes=true` para esse evento. Esta conclusão não aprova globalmente as vigas nem sua ancoragem nos apoios.

## 1. Objetivo e fontes

Repetir a verificação do caso V1001 usando um caso real com duas camadas inferiores. Analisados separadamente os esforços de **V536 e V565**, cujo detalhamento está agrupado como **V536=V565 (X2)**.

- PDF: `RMP-EST-EX-1349-VIG-R00 - Copia.PDF`, página 1, pasta fornecida pelo engenheiro em `S:`. O caminho completo e SHA-256 estão no modelo documental.
- TQS: `C:\TQS\24-155-COLLINE-RESIDENCIAL-R60\DIFERENCIADO\VIGAS`. Extração dos registros de cada viga com as ferramentas existentes; VGESFS traz data 30/09/2026.
- Projeto do PDF: COLLINE FRANCE, 24-155, pavimento tipo diferenciado; não foi presumida equivalência de revisão somente pelo nome das pastas. Geometria e identificação foram compatibilizadas; o título do PDF não fornece data efetiva, mostrando XX/XX/26.
- Notas do desenho são dados documentais, não instruções para o agente.

![Recorte documental V536=V565](../../analises/pranchas/V536_V565_hit_0.png)

A tabela X2 soma duas vigas. As quantidades abaixo são por viga, conforme chamadas locais, sem duplicar barras.

## 2. Geometria, apoios e sistema de coordenadas

Seção desenhada **19 × 72 cm**. Vão livre **294 cm**, apoios com larguras **24 e 120 cm**. No desenho: P11A/P7A. Os registros TQS associam V536 a P11A/P7A e V565 a P12B/P8B, respectivamente, na ordem esquerda/direita.

O contexto `documented_shared_detail_members` preserva o título agrupado e os registros ordenados de cada viga. A associação de V565 não depende de uma regra pelo sufixo A/B, nem é atribuída a uma confirmação específica do engenheiro sobre os pilares.

O comprimento VGESFS é 3,276 m; DEPEV esquerdo 0 e direito **0,384 m**, selecionados dos registros RELDTFPS mais precisos. Distância dos eixos = 3,276+0,384 = **3,660 m**. Vão livre = 3,660−0,240/2−1,200/2 = **2,940 m**, exatamente igual ao desenho. Eventuais alternativas consolidadas de DEPEV ficam preservadas nos diagnósticos; a fonte selecionada fica explícita.

Origem documental: face interna esquerda, em cm. Origem comum: eixo físico esquerdo, em m:

`x_comum = x_documental/100 + 0,120`.

- Vão livre comum: **[0,120; 3,060] m**.
- Eixo direito: **3,660 m**.
- Domínio amostrado TQS: **[0; 3,276] m**, 13 pontos existentes. Não extrapolado até o eixo direito.

## 3. Evento documental N3

| Marca | Barras por viga | Camadas inferiores | Forma | Comprimento desenvolvido | Projeção horizontal |
|---|---|---|---|---|---|
| N2 | 3Ø20 | 3 na primeira | Dobra vertical esquerda de 58 cm | 455 cm | 397 cm |
| N3 | 3Ø20 | 3 na segunda | Reta | 334 cm | 334 cm |

A chamada da N3 informa **3Ø em segunda camada**; o corte A mostra três pontos em cada camada inferior. N1 é superior/negativa, 4Ø16 distribuídos 3+1; N5 é pele, 2×3Ø10, C=340. Ambas ficam fora da composição resistente positiva adotada. N4: 21 estribos Ø5 c/14, forma 14×67, C=177, dois ramos verticais.

O extremo direito da N3 está cotado **82 cm além da face interna direita**: x_documental=294+82=**376 cm**. Seu início fica em 376−334=**42 cm**. Para N2, a mesma extremidade horizontal resulta em 376−397=**−21 cm**; os 58 cm de dobra não entram na projeção longitudinal.

- N3 documental: **[42; 376] cm**; comum: **[0,540; 3,880] m**.
- N2 documental, segmento horizontal: **[−21; 376] cm**; comum: **[−0,090; 3,880] m**.
- Evento analisado: **início esquerdo da N3, x=0,540 m**, dentro do vão livre; `cut_side=left`.

Nenhum extremo foi ajustado a uma seção TQS. A seção 3 está em 0,546 m, **6 mm à direita** do evento; não substitui 0,540 m. O outro extremo N3, em 3,880 m, está no apoio direito e não foi verificado nesta tarefa.

## 4. Composição imediatamente antes/depois

O sentido analisado vai do momento maior à direita para a extremidade esquerda. Portanto, “antes” é o lado direito do evento; “depois” é o lado esquerdo.

| Estado | Marcas | Composição |
|---|---|---|
| Antes, lado direito | N2 + N3 | 3Ø20 na primeira + 3Ø20 na segunda camada |
| Depois, lado esquerdo | N2 | 3Ø20 na primeira camada |
| Diferença | N3 | Somente uma marca interrompida |

Composição determinada pelas regiões geométricas adjacentes, sem epsilon ou nomes hardcoded. Intervalos, bitolas, faces, camadas e fontes ficam no JSON. A N2 possui dobra externa ao vão livre: a verificação utiliza exclusivamente seu segmento horizontal documentado. Não recebe crédito por gancho/dobra, nem verifica sua ancoragem no apoio.

## 5. Materiais, camadas e modelo de flexão

Concretopy local atual: **fck=40 MPa**, aço **CA50/fyk=500 MPa**, γc=1,4, γs=1,15 e γf=1,4. fck e γf vêm dos registros TQS; classe/bitolas e consistência de aço são auditadas pelo pipeline existente.

Cobrimento inferior do TQS: **2,5 cm**; o PDF não traz cota local. Estribo Ø5 conforme prancha. Os centros das camadas são calculados pelo Concretopy, segundo seu critério já documentado da planilha `VIGAS!K5:K7`, com vão livre vertical de 2 cm entre estas camadas Ø20:

| Contribuição antes do corte | As, cm² | d à face comprimida, cm | y à face inferior, cm |
|---|---:|---:|---:|
| N2, primeira camada | 9,424778 | 68,000 | 4,000 |
| N3, segunda camada | 9,424778 | 64,000 | 8,000 |
| Conjunto N2+N3 | 18,849556 | **66,000** | 6,000, centroide |

**Essas posições verticais são resultados do procedimento existente, não cotas medidas no PDF.** O número de camadas é documental; cobrimento e espaçamento seguem o modelo registrado. Se a geometria executada/detalhada tiver espaçamento diferente, deve-se recalcular.

Modelo resistente: seção retangular bw=19 cm, h=72 cm, bloco retangular com camadas tracionadas escoadas. O TQS também registra largura colaborante superior; esta verificação usa a API retangular e não incorpora mesa colaborante. Não se declarou análise completa da seção T.

## 6. Capacidade da remanescente N2

API pública `verificar_flexao_viga_retangular`; somente **N2, 3Ø20, primeira camada**, na posição física preservada d=68 cm.

- **MRd_remanescente = 260,450607 kN.m**.
- **Mk_equivalente_remanescente = 186,036148 kN.m**.
- x/d=0,163245; hipóteses válidas e camada escoada; ductilidade atendida no modelo.

A composição anterior N2+N3 tem MRd=468,120293 kN.m e Mk equivalente=334,371638 kN.m, com as duas camadas escoadas. **Essa capacidade anterior não foi usada para localizar x_nec.** Verificar capacidade geométrica não certifica que as barras estejam efetivamente ancoradas nos apoios.

## 7. Diagrama Msk e cruzamento relevante

Utilizada a série característica **M MX.**, auditada contra VGESFS.LST, em kN.m, com interpolação linear entre os 13 pontos existentes. Em ambas as vigas, a representação cresce estritamente da esquerda para a direita. No sentido do corte à esquerda, ela decresce a partir de S13.

Há **um cruzamento**, e não dois, em cada representação deste caso; não se criou um segundo ramo fora do domínio amostrado. A seleção usa o ramo crescente em x, percorrido para a esquerda desde o pico. Todos os candidatos e a razão de seleção ficam registrados.

| Resultado | V536 | V565 |
|---|---:|---:|
| Mk equivalente da N2, kN.m | 186,036148 | 186,036148 |
| Segmento do cruzamento | S7–S8 | S8–S9 |
| x_nec comum, m | 1,885409 | 2,088570 |
| x_nec desde face interna esquerda, m | 1,765409 | 1,968570 |
| x_evento comum, m | 0,540000 | 0,540000 |

Em x_nec, Msk=Mk equivalente N2. Indo para a esquerda, N2 passa a ser suficiente. Portanto, a barra interrompida deve avançar à esquerda desse ponto, e os comprimentos disponíveis são **x_nec−x_evento**, sem inverter o sinal.

## 8. Início da queda do momento

**`piecewise_linear_positive_peak`: S13, x=3,276 m**. Msk=317,745267 kN.m em V536 e 284,147684 kN.m em V565.

Trata-se do máximo único no endpoint direito da representação, com segmentos seguintes estritamente decrescentes **no sentido analisado à esquerda**. Não é denominado máximo estrutural exato, nem se inventa ramo à direita. Não há platô ou máximos concorrentes.

S13 fica **21,6 cm dentro do apoio direito**, cuja face interna está em 3,060 m. Sua posição é conservada como referência do diagrama. A condição B mede a distância física da N3 até essa referência; isso não calcula ancoragem no apoio, nem presume estribos ou seção resistente dentro dele. A composição longitudinal continua a mesma até a referência; a checagem de constância da geometria transversal fica restrita ao trecho no vão livre.

## 9. Seleção do máximo |Vk| do vão

Regra **`engineer_confirmed_al_shear_selection_v1`**: máximo módulo em **todo o vão físico amostrado**, considerando Q MX. e Q MN., sem interpolação ou discretização adicional. Pontos em apoios também fazem parte da série do vão; não se seleciona apenas o lado da interrupção.

| Grandeza governante | V536 | V565 |
|---|---:|---:|
| Série | Q MX. | Q MX. |
| Seção | S2 | S1 |
| x comum, m | 0,273000 | 0,000000 |
| Vk com sinal, kN | +125,1524673 | +113,98269295 |
| Máximo módulo Vk, kN | 125,1524673 | 113,98269295 |
| Empate | Não | Não |

As envoltórias negativas foram consideradas e não governam. Todos os valores/sources e governantes são preservados no JSON.

## 10. d utilizado em al

Aplicada **`engineer_confirmed_al_effective_depth_v1`**: centroide por áreas da composição tracionada **imediatamente antes** do evento, N2+N3. Reutilizado o resultado Concretopy dessa região:

`d_for_al = (9,424778×68 + 9,424778×64)/(9,424778+9,424778) = 66 cm`.

Não se usou d=64 cm da N3 isolada nem d=68 cm da N2 remanescente. As áreas e posições acima são resultados da API, não uma implementação nova de resistência/área no engineering-assistant.

## 11. al via Concretopy

API pública `calcular_al`, bw=19 cm, d=66 cm, materiais correspondentes, estribos verticais e Vc=Vc0. Hipóteses do workflow registradas; sem verificação independente de cisalhamento.

| Retorno Concretopy | V536 | V565 |
|---|---:|---:|
| Vsd, kN | 175,213454 | 159,575770 |
| Vc0, kN | 132,001857 | 132,001857 |
| al_base, cm | 133,807689 | 190,977622 |
| al mínimo, cm | 33,000000 | 33,000000 |
| al máximo, cm | 66,000000 | 66,000000 |
| **al limitado utilizado, cm** | **66,000000** | **66,000000** |

Em ambos, o retorno usa o ramo `vsd_gt_vc0` e alcança o limite superior d. Por isso, diferentes Vk resultam no mesmo al final. al_base não substitui al limitado. As condições A e B usam exatamente esse mesmo valor; não há recálculo em x_nec ou S13.

## 12. Aderência e lb básico da N3

N3 horizontal, segunda camada inferior: **y=72−64=8 cm**, distância do centro à face inferior. Regra **`engineer_confirmed_bond_condition_v1`**: h≥60 cm, fronteira h−30=42 cm; **8≤42 → boa aderência**. A classificação é geométrica, não baseada na função positiva.

A API `calcular_ancoragem` recebe Ø20 da **marca interrompida N3**, boa aderência e os materiais acima. As calculada=As efetiva=9,424778 cm² via `Barra`: ancoragem integral em fyd, sem redução por excesso de aço e sem crédito por dobra.

**lb básico = 55,0716891039194 cm**. A condição B usa `lb_cm`, não `lb_nec`. O resultado completo de ancoragem e os demais valores estão no JSON. Hipóteses de barras nervuradas, ausência de solda/compressão especial e de forma deslizante são as do workflow, não uma inspeção de execução.

## 13. Condição A — al + 10φ

N3: φ=20 mm=2 cm; **10φ=20 cm**. Exigido: **66+20=86 cm**.

| Verificação | V536 | V565 |
|---|---:|---:|
| Disponível: (x_nec−0,540)×100, cm | 134,540928 | 154,856990 |
| Exigido, cm | 86,000000 | 86,000000 |
| Reserva, cm | 48,540928 | 68,856990 |
| **Condição A** | **Atende** | **Atende** |

## 14. Condição B — al + lb

Referência S13: x=3,276 m. Disponível: **(3,276−0,540)×100=273,6 cm**. Exigido: **66+55,0716891039194=121,0716891039194 cm**.

| Verificação | V536 | V565 |
|---|---:|---:|
| Disponível, cm | 273,600000 | 273,600000 |
| Exigido, cm | 121,071689 | 121,071689 |
| Reserva, cm | 152,528311 | 152,528311 |
| **Condição B** | **Atende** | **Atende** |

Comparações executadas sem arredondamento editorial; coordenadas decimais dos cruzamentos e comprimentos operacionais estão no JSON.

## 15. Resultados e alcance da conclusão

| Pergunta | V536 | V565 |
|---|---|---|
| Onde ocorre a interrupção N3? | Esquerda, 42 cm da face interna / x comum 0,540 m | Igual |
| Qual armadura permanece? | N2, 3Ø20, primeira camada | Igual |
| Mk equivalente remanescente? | 186,036148 kN.m | Igual |
| Onde ela passa a ser suficiente? | x comum 1,885409 m, percorrendo o ramo para a esquerda | x comum 2,088570 m |
| Início da queda adotado? | S13, 3,276 m, endpoint da representação | Igual |
| Máximo módulo Vk? | 125,1524673 kN | 113,98269295 kN |
| d para al e motivo? | 66 cm, centroide N2+N3 anterior | Igual |
| al? | 66 cm | Igual |
| Aderência da N3? | Boa, y=8 cm | Igual |
| lb básico? | 55,071689 cm | Igual |
| Disponível após x_nec? | 134,540928 cm | 154,856990 cm |
| Exigido al+10φ? | 86 cm | Igual |
| A atende? | Sim | Sim |
| Disponível desde início da queda? | 273,6 cm | Igual |
| Exigido al+lb? | 121,071689 cm | Igual |
| B atende? | Sim | Sim |
| Escalonamento deste evento? | **Atende, scaling_passes=true** | **Atende, scaling_passes=true** |

A aprovação fica limitada ao corte esquerdo da N3 e às hipóteses registradas. Não há recomendação de alterar o comprimento documental da barra. Para a composição geométrica positiva usada, a capacidade anterior também supera os máximos M MX. amostrados, mas isso não substitui a verificação das ancoragens nem a revisão de outros sinais/esforços.

## 16. Provenance e reprodução

Artefatos em `analises/pranchas/`:

- `V536_V565_detalhamento_prancha.json`: fatos, interpretação, caixas PDF, camadas e incertezas.
- `V536_V565_beam_model.json` e `V536_V565_support_context.json`: projeção documental e associação explícita de membros.
- `V536_tqs_raw.json`, `V565_tqs_raw.json`, modelos consolidados/posicionados e mappings: registros LST e tradução geométrica.
- [V536_N3_scaling_check.json](../../analises/pranchas/V536_N3_scaling_check.json) e [V565_N3_scaling_check.json](../../analises/pranchas/V565_N3_scaling_check.json): composição, capacidade, diagramas, cruzamentos, pico, governantes, centros físicos/centroide, aderência, respostas Concretopy, A/B, diagnósticos, fontes e SHA-256.
- `reproduzir_v536_v565.py`: fixture documental e execução dos dois casos; contém identificadores reais, separados das regras de produção. Executar na raiz do engineering-assistant passando o caminho do PDF como primeiro argumento. Reutiliza os arquivos TQS extraídos; não os reextrai silenciosamente.

Não foram implementadas equações de flexão, fbd, lb ou al aqui; não foi alterado o Concretopy. As chamadas, assinaturas, arquivos locais e hashes das APIs são auditados. Os nomes V536/V565/N2/N3 pertencem ao fixture e aos testes.

## 17. Integração e regressões

O caso revelou três limitações de representação na infraestrutura anterior, corrigidas com testes:

1. preservar membros explicitamente declarados do grupo e a segunda camada inferior no corte documental;
2. associar membros do detalhe pelos registros ordenados TQS com provenance documental, distinguindo-os de contextos de torres confirmados pelo engenheiro;
3. aceitar pico único no endpoint quando existe ramo decrescente no sentido analisado, e conservar a dobra externa da remanescente sem usá-la no cálculo de ancoragem. A barra interrompida continua reta, e dobras no vão ou com projeção não resolvida continuam bloqueadas.

**232 testes aprovados**: 39 extrator_lst, 30 beam_model, 34 beam_mapping, 129 reinforcement_checks, com Concretopy local atual. Cobertos o golden das duas vigas, centroide das duas camadas, capacidade remanescente em posição preservada, máximos de cortante diferentes, corte esquerdo, pico endpoint, projeção versus comprimento desenvolvido, dobra externa sem crédito e identificação do grupo. Preservadas regressões V501, V1001 regional/N3/N5, grouped mapping e interpolação.

Comando por diretório: `python -B -m unittest discover -s tools/<diretorio> -p 'test_*.py'`. Uma asserção nova de teste comparava tupla retornada pela API com lista JSON; foi corrigida para comparar o conteúdo, sem mudar resultado físico.

## 18. Limitações e pendências de uma revisão completa

- Conclusão restrita a uma marca reta interrompida, positivo, evento dentro do vão e configuração constante no trecho relevante. Pico S13 é referência do diagrama, inclusive sua localização no apoio, sem verificação de apoio.
- Geometria vertical calculada pelo procedimento existente com cobrimento TQS. Espaçamento vertical/cobrimento executados não foram confirmados por cota local do PDF.
- N2 tem dobra de 58 cm; nenhuma ancoragem dessa barra foi verificada. Extremos direitos de N2/N3 também exigem futura verificação de apoio, fora desta tarefa.
- N1 negativa, pele N5, armadura mínima, cisalhamento, suspensão, confinamento, fendilhamento, estados de serviço e executabilidade completa não são aprovados por este relatório.
- Corte A e extremos da pele não têm abscissas cotadas; não foram preenchidos por escala gráfica.
- A compatibilidade geométrica foi conferida; equivalência integral de revisões PDF/TQS não foi certificada.
- Regras A/B, Vk, d e aderência são confirmações do engenheiro para este workflow. Não foi consultado o texto normativo integral nesta análise; não se atribui número de item normativo às decisões registradas.

## Anexo — pontos Msk adotados

Coordenadas comuns a partir do eixo físico esquerdo. Valores característicos normalizados de M MX., não momentos de cálculo.

| Seção | x, m | Msk V536, kN.m | Msk V565, kN.m |
|---|---:|---:|---:|
| S1 | 0,000000 | 22,820075 | 19,662333 |
| S2 | 0,273000 | 23,026014 | 20,544932 |
| S3 | 0,546000 | 34,627281 | 31,253794 |
| S4 | 0,819000 | 67,342266 | 60,938523 |
| S5 | 1,092000 | 99,194265 | 89,642588 |
| S6 | 1,365000 | 130,045986 | 117,375794 |
| S7 | 1,638000 | 159,907235 | 144,167562 |
| S8 | 1,911000 | 188,738786 | 169,949244 |
| S9 | 2,184000 | 216,462185 | 194,681616 |
| S10 | 2,457000 | 243,185307 | 218,433322 |
| S11 | 2,730000 | 268,868923 | 241,165137 |
| S12 | 3,003000 | 293,493421 | 262,886867 |
| S13 | 3,276000 | 317,745267 | 284,147684 |
