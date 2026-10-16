# ATP S07 — vigas do térreo — rodada 02, modelo atualizado

Data: 15/10/2026. Esta rodada substitui os esforços, associações TQS e resultados resistentes da rodada 01 para o modelo examinado. A rodada anterior permanece como histórico. **A revisão integral do pavimento ainda não está encerrada.**

## Resultado principal e cobertura

Foram encontrados V1–V50 no modelo atualizado, além de nove PAR e sete elementos adicionais de modelagem. Há 66 registros, 121 vãos de cálculo e 605 séries de 13 ordenadas. Todas as 605 séries foram conferidas numericamente em RELDTVGS.LST. A disponibilidade das 20 identificações antes ausentes foi resolvida; isso não equivale à aprovação de todos os vãos e regiões.

**V16 mantém insuficiência positiva e passa a apresentar insuficiência negativa junto ao PC41C. V21 mantém o alerta de cortante do primeiro vão pelo modelo I.** As demais diferenças produzidas pela triagem são solicitações de revisão regional, sem emissão automática de reprovação normativa.

Cobertura efetiva desta rodada:

- Presença nominal nas formas/detalhamentos: V1–V50 e nove PAR, reaproveitada após confirmação de que os seis PDFs não mudaram.
- Fontes e esforços: reextração integral do modelo novo, preservando valores originais, unidades, linha, nome, identificação interna e hash.
- Flexão e cortante: 42 vigas, 82 intervalos de cálculo com triagem de seções; não são 82 vãos físicos integralmente aprovados. Os balanços/segmentos auxiliares sem registro documental integral permanecem separados.
- Flexão negativa nas faces representadas no modelo: demanda e composição de cada extremidade calculadas separadamente para as seções com leitura disponível. Os máximos dentro dos pilares não foram automaticamente tratados como momentos na face.
- Revisão física regional pelo procedimento operacional da skill: V16, com barras, faces e eixo documentados. O manifesto das demais vigas conserva a ausência de registro físico completo; domínios de planejamento não são usados como coordenadas reais.
- Suspensão: 41 relações nomeadas no modelo, das quais cinco são ligações de excentricidade com pilares. Permanecem 36 relações a classificar e verificar localmente; o inventário não aprova a armadura.
- Método especial: V3, V6, V7–V10, V12 e V13, além dos nove PAR. Não foram aprovados pelo verificador de viga usual.

## Fontes e premissas

Modelo: `C:\TQS\25-208-ATP___24-1454-WERT-WPBGR RESIDENCE-PE-MU2-S07-ATP2___2aFASE-Calc01\TÉRREO\VIGAS\VGESFS.LST`. VGESFS.LST processado em 15/10/2026 aproximadamente às 10h31; SHA-256 `e6faa302a961c18472bbcf9c5a0fa907b10c1e08b9505f70a6106f68f019f44b`. A fonte permaneceu estável durante esta rodada.

Pranchas consultadas/reutilizadas, todas com hash idêntico ao levantamento anterior:

| Prancha | Revisão | Conteúdo |
|---|---|---|
| 7202 | R03 | FORMAS |
| 7214 | R01 | FORMAS |
| 7401 | R00 | TÉRREO |
| 7402 | R00 | TÉRREO |
| 7403 | R01 | TÉRREO |
| 7404 | R00 | TÉRREO |

As solicitações são características, conforme legenda de RELDTVGS.LST, em tf e tf·m. Conversão: 1 tf = 9,80665 kN; majoração γf = 1,4. A verificação utiliza seções do detalhamento, como autorizado por João; diferenças de seção/apoios do modelo são conservadas com origem e não transformadas automaticamente em divergências forma×detalhamento.

Materiais: aço CA-50, fyk = 500 MPa, γs = 1,15; γc = 1,4. Formas distinguem C40 na primeira concretagem e C35 na segunda. Nas triagens mantêm-se os dois cenários homogêneos como sensibilidade; eles não substituem o bloco comprimido real com concretagem em etapas. Barras na interface da primeira concretagem mantêm sua posição intermediária: não são transferidas à camada externa.

Preservados os esclarecimentos do contexto: pavimento principal +9,18 m; P791 com topo local +8,88 m; V49 com topo local +9,55 m; correções de P799/P807C não propagadas indiscriminadamente a níveis locais; primeira concretagem dos reservatórios até +9,28 m conforme registro. “2aFASE” designa a etapa do ATP, não uma etapa de carregamento/concretagem.

Os relatórios automáticos TQS contêm referências à NBR 6118:2014 em alguns procedimentos. Nesta revisão, as solicitações são usadas como resultados do modelo; a aprovação automática TQS não comprova atendimento à edição 2023.

Norma efetivamente consultada: exemplar local **ABNT NBR 6118:2023**, em DOCUMENTACAO ATP. Referências utilizadas: 17.3.5.2.1 (mínimos longitudinais, p.131), 17.4.1.1.1 (mínimo transversal), 17.4.1.2.1 (reduções junto aos apoios), 17.4.2.1/17.4.2.2 (ELU ao cortante/modelo I, p.136 e sequência), 18.3.3.2 (espaçamentos), 18.3.6 (suspensão, p.152), 22.4.1 (vigas-parede, p.184). Não se aplicaram preferências internas de bitola, espaçamento mínimo fixo de 8 cm ou número de ramos por largura.

Para mínimos longitudinais, foi verificado Md,min = 0,8 W0 fctk,sup e As ≥ 0,0015 Ac, sem impor ao d/h real a hipótese de uma tabela. O mínimo de espaçamento longitudinal de estribos depende de passagem do vibrador/adensamento: não foi inventado um limite numérico universal.

## Associação entre pranchas e modelo

- V1–V50 têm registros com esses nomes. A associação conserva também a cadeia de apoios; igualdade de nome, isoladamente, não é prova de identidade física.
- V23 do detalhe: modelo V23, vãos 1 e 2, PC54C–P799–P785.
- V24 do detalhe: primeiro vão P785–P778 no **modelo V23, vão 3**; demais vãos no modelo V24, vãos 1–3. Não omitir esse primeiro vão nem contar como pertencente ao detalhe V23.
- V17: V901–V905 ligam ao mesmo pilar em ambas as extremidades e representam a transferência aos P786–P790. Foram retiradas do inventário de apoios indiretos físicos.
- V26: modelo PC25C–PC21C–PC19C–V25; o detalhe mantém os rótulos incompatíveis PC26C/PC24C/PC20C. O vínculo físico usa a forma e a posição, conservando a divergência documental.
- V40: forma e modelo chegam a V20; detalhe 7403 escreve V19. A correção do modelo não corrige a prancha recebida.
- V51 (PC41C–PC35C) e V910 (PC40C–PC34C), ambas 40×20 no modelo, não têm identificação correspondente de viga nas formas examinadas. Situam-se na região de laje L8 de 20 cm. Sua função de modelagem permanece a confirmar; não se emitiu apontamento de “viga física sem detalhamento” apenas pela existência dessas barras.
- Balanços e pequenos segmentos remanescentes de V22/V25/V31/V41/V43 exigem associação física específica; sua presença no LST não autoriza extrapolar armadura de outro trecho.

## V16 — resultados refeitos

Fontes: 7401 R00, elevação/corte A/tabela; forma 7214 R01. Apoios PC40C–PC41C, seção 40×50 cm, vão livre 730 cm, apoios 70 cm. Eixo comum entre apoios 8,00 m; trecho TQS 7,60 m com DEPEV de 0,20 m por lado. Faces internas em x = 0,35 e 7,65 m.

N4: 4Ø12,5, C850, positiva; N2/N3: 4Ø16 em cada extremidade, C300; N1: 4Ø10 central, C290. N2 termina em x=2,75 m; N3 inicia em x=5,25 m; N1 ocupa x=2,55–5,45 m. Essas posições foram mantidas na nova rodada.

| Controle | Demanda de cálculo | Resistência/fornecido | Resultado |
|---|---:|---:|---|
| Flexão positiva | 209,76 kN·m | 93,88 em C35 / 94,22 em C40 | Insuficiente |
| Negativa junto ao PC40C | 116,10 kN·m | 150,41 kN·m em C35 | Atende ao momento verificado |
| Negativa junto ao PC41C | 164,63 kN·m | 150,41 kN·m em C35 | Insuficiente |
| Mínimos longitudinais nas regiões verificadas | Md,min e 0,15% Ac | N4 e negativas de extremidade | Atendem; não compensam a insuficiência ao momento |
| Cortante e espaçamentos máximos | Vsd = 211,46 kN | 4 ramos Ø6,3 c20; 6,23 cm²/m | Atendem numericamente em C35/C40 |
| Espaçamento mínimo dos estribos | Passagem/adensamento | Equipamento não documentado | Pendente operacional |
| Suspensão | Apoios diretos nos dois pilares; nenhuma viga apoiada em V16 nas 66 cadeias | Não aplicável ao trecho examinado | Não aplicável |

Conferência independente: T = As fyd; a = T/(0,85 fcd bw); z = d−a/2; MRd = Tz. Para a positiva, As = 4,9087 cm² e d = 45,245 cm. Para a negativa, As = 8,0425 cm² e d = 45,07 cm. O cálculo independente coincide com o motor da skill.

Positiva: mesmo um limite superior deliberadamente favorável, atribuindo a **todo** o aço presente no pico (N4 + N1), tensão de 500 MPa e braço de 50 cm, chega a 201,26 kN·m, inferior à demanda 209,76. O déficit não decorre de ignorar uma pequena contribuição da armadura superior.

Negativa no PC41C: o limite T·d de N3 com fyd, ainda sem descontar a posição da resultante comprimida, é 157,60 kN·m, inferior aos 164,63 solicitantes. Considerar a armadura comprimida não supera esse limite da força de tração; N1 não alcança essa face.

Nos estribos, os dois anéis sobrepostos N5 têm largura desenhada de 22 cm e quatro ramos efetivos, conforme corte A. Isso limita os intervalos entre ramos a menos de 22 cm, abaixo dos limites aplicáveis. Não se confundiu a largura total de 40 cm com o intervalo entre ramos.

**Histórico substituído:** positiva anterior Msd=232,49 kN·m → nova 209,76 kN·m, permanecendo insuficiente. A conclusão anterior de atendimento das duas negativas não vale para esta rodada: a extremidade PC41C agora é insuficiente.

## V21 — primeiro vão

Modelo V21, vão 1, PC54C–PC55C; 7402: seção 30×50 cm, N21 188Ø8 c17, dois ramos de altura total; Asw/s = 5,9136 cm²/m. d = 44,7 cm para a camada longitudinal Ø20. As faces abaixo usam larguras/DEPEV do modelo; o registro documental completo dessas faces permanece pendente.

| Consulta | Vsd (kN) | Asw/s requerida C35 | Asw/s requerida C40 | Fornecida (cm²/m) |
|---|---:|---:|---:|---:|
| Entre faces | 273,93 | 8,28 | 7,59 | 5,91 |
| Sensibilidade a d/2 | 248,02 | 6,80 | 6,11 | 5,91 |

**Solicitar revisão do cortante do primeiro vão.** O resultado do modelo I permanece inferior ao necessário, inclusive na sensibilidade indicada. A consulta em d/2 não é autorização genérica para reduzir cargas concentradas ou alterar condições de apoio. Fechar a classificação das cargas, reduções aplicáveis, d e materiais locais antes da conclusão normativa integral. Não se dimensionou nem se escolheu armadura substituta.

## Outros resultados de triagem — não converter diretamente em reprovação

A tabela registra a demanda negativa em faces **representadas no TQS**, comparada à resistência apenas da composição externa lida no detalhe. Exige conferência da face documental, da composição completa e da posição real de barras intermediárias. Números C35/C40 são sensibilidades; o menor deles não é automaticamente o material correto. Seguem os casos em que ambas as sensibilidades ficaram abaixo da demanda na triagem:

| Viga | Vão TQS | Extremidade/apoio | Msd na face (kN·m) | MRd da composição externa C35 (kN·m) |
|---|---|---|---:|---:|
| V2 | 3 | P706 | 176,00 | 170,70 |
| V15 | 1 | P757 | 207,21 | 93,88 |
| V15 | 2 | P756 | 354,06 | 328,22 |
| V15 | 2 | P760 | 290,63 | 150,41 |
| V15 | 3 | P760 | 286,89 | 150,41 |
| V25 | 2 | P730 | 205,86 | 148,01 |
| V25 | 3 | P727 | 78,74 | 76,40 |
| V25 | 4 | P727 | 166,24 | 76,40 |
| V25 | 4 | P708 | 109,09 | 70,41 |
| V28 | 1 | PC34C | 198,18 | 150,41 |
| V32 | 1 | PC35C | 166,85 | 150,41 |
| V34 | 1 | P760 | 356,66 | 226,67 |
| V43 | 2 | P737 | 197,48 | 170,70 |
| V43 | 4 | P723 | 159,87 | 112,80 |
| V43 | 4 | P714 | 144,41 | 112,80 |
| V18 | 1 | PC45C | 234,82 | 170,70 |
| V18 | 2 | PC45C | 222,47 | 170,70 |
| V30 | 1 | PC2C | 109,72 | 85,92 |
| V33 | 1 | P794 | 218,17 | 116,26 |
| V35 | 1 | PC36C | 114,46 | 112,80 |
| V35 | 1 | PC30C | 260,22 | 148,01 |
| V35 | 2 | PC30C | 273,92 | 148,01 |
| V36 | 1 | P735 | 274,26 | 148,01 |
| V37 | 1 | P725 | 232,25 | 148,01 |
| V40 | 1 | P796 | 213,27 | 116,26 |
| V44 | 1 | P731 | 366,36 | 149,81 |
| V48 | 1 | P767 | 226,96 | 92,99 |
| V48 | 1 | P758 | 165,36 | 148,01 |

Positivas/cortantes e mínimos de todas as seções triadas permanecem nos JSONs, inclusive resultados favoráveis. Os casos com seção variável V23/V24/V42/V49/V50 usam também limites conservadores h50: **uma falha desse limite não prova insuficiência da seção maior**. Em V18, V23, V30 e outras vigas com reforços interrompidos, a triagem com a quantidade mínima ao longo do vão pode omitir barras atuantes no pico; confirmar a composição local antes de emitir apontamento resistente.

V11: a triagem da camada superior isolada 3Ø10 não satisfaz o mínimo da seção 24×80, porém há barras intermediárias. Não se concluiu falta de armadura mínima sem reconstituir suas alturas e funções. O mesmo cuidado vale para a primeira concretagem das demais vigas.

## Divergências documentais mantidas e novas

| Caso | Evidência e providência |
|---|---|
| V26 | Apoios do detalhe PC26C/PC24C/PC20C não representam a cadeia PC19C/PC21C/PC25C da forma. Compatibilizar os rótulos. |
| V3/V6 | Resumo inferior 2Ø20 versus posição N1/corte com 4Ø16. Compatibilizar a representação; não foi provada falta física de aço. |
| V22 | Resumo superior 2Ø16 versus posição N1 2Ø12,5. Compatibilizar. |
| V42 | Detalhe contém trecho h110; forma tem rótulos h80/h50. A posição exata da transição e a incidência em P791/P784 continuam pendentes, considerando P791 a +8,88. |
| V19/V20 — nova conferência | Resumo inferior 4Ø12,5 versus N3 2Ø16 + N4 1Ø16. Quantidades/bitolas e extensão devem ser conciliadas. |
| V40 — nova conferência | Apoio final escrito V19 na 7403 versus encontro com V20 na forma 7214. Modelo atualizado também apoia em V20. |

Não foi emitida declaração geral de que todos os vãos e transições forma×detalhamento coincidem. A presença nominal e a coincidência de rótulos de seção são controles distintos da conferência dimensional integral.

## Suspensão e elementos especiais

Reações e fontes das 41 relações estão no inventário. As cinco relações V17→V901…V905 são transferências aos próprios pilares. As outras 36 requerem classificação do encontro, níveis superior/inferior, condição pendurada ou não pendurada, região normativa e armadura existente cumulativa com cisalhamento.

Foi calculado somente um valor de referência Rsd/fyd para cada reação extrema, sem aplicar indiscriminadamente 75% e sem tratá-lo como dimensionamento final. Em 18.3.6, a parcela mínima de 75% na receptora depende da condição de viga não pendurada e não equivale a reduzir universalmente a reação. A redução geométrica também depende da condição descrita na norma.

Há inversão de sinal de reação em V12→V31, V13→V41, V17→V23, V17→V42, V35→V15 e V36→V5. Preservar os sinais e avaliar o caminho de carga; dimensionar suspensão apenas com o valor positivo selecionado apagaria parte da envoltória.

V3/V6/V7–V10/V12/V13 têm relações de vão/altura compatíveis com investigação de viga-parede (22.4.1), com h165 e comprimentos de cálculo entre 2,11 e 3,02 m. Não se transplantou para elas o mecanismo de viga esbelta. Os nove PAR exigem leitura própria do caminho de cargas, bielas/tirantes/nós e armaduras; ausência de PAR706 foi conferida como ausência em ambos os conjuntos, não viga faltante.

## Matriz por viga — cobertura e pendência

“Triagem” significa cálculo da seção selecionada, não aprovação de toda a viga. Nenhuma viga recebeu aprovação global nesta rodada.

| Viga | Seções no detalhe (cm) | Intervalos triados | Estado principal |
|---|---|---:|---|
| V1 | 30×55 | 1 | Triagem; fechar composição, faces e controles locais |
| V2 | 30×50 | 3 | Triagem; fechar composição, faces e controles locais |
| V3 | 24×165 | 0 | Método de viga-parede pendente |
| V4 | 40×50 | 1 | Triagem; fechar composição, faces e controles locais |
| V5 | 19×50 | 1 | Triagem; fechar composição, faces e controles locais |
| V6 | 24×165 | 0 | Método de viga-parede pendente |
| V7 | 19×165 | 0 | Método de viga-parede pendente |
| V8 | 19×165 | 0 | Método de viga-parede pendente |
| V9 | 19×165 | 0 | Método de viga-parede pendente |
| V10 | 19×165 | 0 | Método de viga-parede pendente |
| V11 | 24×80 | 1 | Triagem; fechar composição, faces e controles locais |
| V12 | 24×165 | 0 | Método de viga-parede pendente |
| V13 | 24×165 | 0 | Método de viga-parede pendente |
| V14 | 19×50 | 3 | Triagem; fechar composição, faces e controles locais |
| V15 | 40×50 | 4 | Triagem; fechar composição, faces e controles locais |
| V16 | 40×50 | 1 | Insuficiente: positiva e negativa PC41C |
| V17 | 40×50 | 6 | Triagem; fechar composição, faces e controles locais |
| V18 | 30×50 | 2 | Triagem; fechar composição, faces e controles locais |
| V19 | 30×50 | 1 | Triagem; fechar composição, faces e controles locais; compatibilizar documento |
| V20 | 30×50 | 1 | Triagem; fechar composição, faces e controles locais; compatibilizar documento |
| V21 | 30×50 | 6 | Triagem; fechar composição, faces e controles locais |
| V22 | 30×50 | 2 | Triagem; fechar composição, faces e controles locais; compatibilizar documento |
| V23 | 30×80 / 30×50 | 2 | Triagem conservadora; transições/alturas pendentes |
| V24 | 30×80 / 30×50 | 4 | Triagem conservadora; transições/alturas pendentes |
| V25 | 30×50 | 4 | Triagem; fechar composição, faces e controles locais |
| V26 | 19×50 | 3 | Triagem; fechar composição, faces e controles locais; compatibilizar documento |
| V27 | 24×50 | 1 | Triagem; fechar composição, faces e controles locais |
| V28 | 40×50 | 2 | Triagem; fechar composição, faces e controles locais |
| V29 | 19×165 | 1 | Triagem; fechar composição, faces e controles locais |
| V30 | 24×60 | 1 | Triagem; fechar composição, faces e controles locais |
| V31 | 19×165 | 1 | Triagem; fechar composição, faces e controles locais |
| V32 | 40×50 | 2 | Triagem; fechar composição, faces e controles locais |
| V33 | 30×50 | 1 | Triagem; fechar composição, faces e controles locais |
| V34 | 40×50 | 1 | Triagem; fechar composição, faces e controles locais |
| V35 | 30×50 | 2 | Triagem; fechar composição, faces e controles locais |
| V36 | 30×50 | 1 | Triagem; fechar composição, faces e controles locais |
| V37 | 30×50 | 1 | Triagem; fechar composição, faces e controles locais |
| V38 | 24×50 | 1 | Triagem; fechar composição, faces e controles locais |
| V39 | 19×165 | 1 | Triagem; fechar composição, faces e controles locais |
| V40 | 30×50 | 1 | Triagem; fechar composição, faces e controles locais; compatibilizar documento |
| V41 | 19×165 | 1 | Triagem; fechar composição, faces e controles locais |
| V42 | 30×80 / 30×50 / 30×110 | 7 | Triagem conservadora; transições/alturas pendentes |
| V43 | 30×50 | 4 | Triagem; fechar composição, faces e controles locais |
| V44 | 40×50 | 1 | Triagem; fechar composição, faces e controles locais |
| V45 | 24×50 | 1 | Triagem; fechar composição, faces e controles locais |
| V46 | 30×50 | 1 | Triagem; fechar composição, faces e controles locais |
| V47 | 30×50 | 1 | Triagem; fechar composição, faces e controles locais |
| V48 | 30×50 | 1 | Triagem; fechar composição, faces e controles locais |
| V49 | 24×50 / 24×87 | 1 | Triagem conservadora; transições/alturas pendentes |
| V50 | 24×50 / 24×87 | 1 | Triagem conservadora; transições/alturas pendentes |

## Trabalho necessário para fechamento integral

1. Corrigir/conciliar as divergências entre representações antes de certificar a composição física dependente.
2. Registrar os eixos, faces, vãos e transições das demais vigas; comparar dimensões forma×detalhamento sem usar comprimento de corte ou faixa de estribos como cota de geometria.
3. Reconstituir a composição atuante em cada pico positivo/negativo, incluindo barras intermediárias em sua posição real e compatibilidade de deformações quando necessária. Fechar mínimos nas seções reais.
4. Particionar estribos por bitola, ramos e extensão documentada; verificar cada região, compressão diagonal, mínimo, espaçamentos máximos longitudinal/transversal e condição de adensamento.
5. Fechar as 36 ligações físicas candidatas à suspensão, sem somar a mesma armadura duas vezes entre suspensão e cortante.
6. Verificar as oito vigas curtas e nove PAR pelo método estrutural apropriado.

Essas pendências são limites da revisão realizada; não são reprovações normativas presumidas. A rodada não inclui seleção de nova armadura, alteração do modelo, alteração de PDFs, ancoragem, escalonamento ou verificação de ELS.

## Rastreabilidade dos arquivos

- `tqs_operacional.json`: esforços novos e geometria de origem; nenhuma série da rodada anterior foi usada como solicitação vigente.
- `proveniencia.json`, `validacao_extracao.json`, `validacao_rodada.json`: hashes, datas e validação cruzada.
- `matriz_vigas.json`: pranchas, existência, associações e cobertura por controle.
- `triagem_secoes_criticas.json`: 42 vigas/82 intervalos e sensibilidades completas.
- `verificacao_faces_modelo.json`: negativas por extremidade, faces e solicitações com sua origem.
- `V16_resultado_resumido.json`, `V16_conferencia_independente.json`: resultados regionais e conferência independente.
- `V21_cortante_primeiro_vao.json`: duas consultas de cortante e resultados de dimensionamento.
- `inventario_apoios_indiretos.json`: reações, sinais, referência de tirante e classificação pendente.

Resultado operacional completo e manifesto preservados no diretório de trabalho `\\srvmaster\PUBLICO\Joao Severgnini\Simon\engineering-assistant\analises\atp_s07_vigas_terreo\rodada_02_modelo_atualizado`. O resultado completo é volumoso e não foi duplicado na documentação do projeto; os resultados resumidos rastreáveis acompanham este relatório.
