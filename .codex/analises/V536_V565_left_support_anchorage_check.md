# V536/V565 — golden corrigido de ancoragem positiva esquerda

06/10/2026. A decisão do engenheiro corrigiu o comprimento disponível para **lb_ef=L_apoio−cobrimento=24,0−2,5=21,5 cm**. A posição documental da N2 continua em −21 cm da face interna (x comum −0,090 m), sem alteração da prancha/fixture. A projeção desenhada de **21 cm** e a disponibilidade geométrica de **21,5 cm** são informações distintas.

A 3Ø20 da V536 continua falhando por comprimento. A 3Ø20 da V565 atende à verificação de área/ancoragem neste cenário. Ambas têm área suficiente. O crédito de gancho α=0,7 e os pares na S1 são decisões expressas do engenheiro.

## Geometria, materiais e fontes

Seção 19×72 cm, apoio longitudinal 24 cm; C40/CA50, γf=γc=1,4, γs=1,15; cobrimento TQS 2,5 cm, estribo-paramétrico Ø5. Resolução de materiais/seção e ausência de crédito à mesa são mantidas da [auditoria do escalonamento](V536_V565_N3_scaling_check.md). V536/P11A e V565/P12B compartilham detalhamento, mas têm esforços próprios. PDF página 1, caminho integral/SHA-256 no [documental](../../analises/pranchas/V536_V565_detalhamento_prancha.json); esforços VGESFS na pasta TQS fornecida. Não se certificou equivalência de revisão somente pelo nome da pasta.

Somente N2, 3Ø20 na primeira camada, chega ao apoio esquerdo; N3 começa 42 cm dentro do vão. N1 superior e N5 de pele não participam da composição positiva adotada. N2 tem dobra esquerda vertical de 58 cm; esse ramo não é somado a lb_ef. As=9,424777961 cm². d apoio=68 cm; d vão=66 cm da configuração N2+N3 auditada na região de maior momento. d apoio não é o centroide anterior ao corte da N3.

Origem documental: face interna esquerda; origem comum: eixo esquerdo; face interna x=0,120 m. Geometria/vãos/mapping e intervalos documentais permanecem inalterados.

## Pares e demanda Concretopy

Na S1 x=0, P1 usa Mk positivo com |Vk da envoltória mínima|. P2 usa Mk=0 com máximo módulo selecionado de Vk. Não se usa o máximo de todo o vão do escalonamento, nem se afirma concomitância de casos de carga.

| Viga/par | Mk (kN.m) | Vk usado (kN) | d (cm) | x (cm) | z (cm) | al final (cm) | As A | As B | As C | Governante |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| V536/positive_moment_min_shear | 22.820075 | 33.538743 | 68.000000 | 11.100661 | 62.449670 | 68.000000 | 2.448720 | 2.256585 | 5.917168 | C |
| V536/zero_moment_max_abs_shear | 0.000000 | 123.603017 | 68.000000 | 11.100661 | 62.449670 | 68.000000 | - | 3.980017 | 5.917168 | C |
| V565/positive_moment_min_shear | 19.662333 | 25.516903 | 68.000000 | 11.100661 | 62.449670 | 68.000000 | 2.448720 | 1.835464 | 5.200058 | C |
| V565/zero_moment_max_abs_shear | 0.000000 | 113.982693 | 68.000000 | 11.100661 | 62.449670 | 68.000000 | - | 3.670243 | 5.200058 | C |

Áreas em cm². Chamadas independentes; demanda máxima entre chamadas, preservando empates. C1 governa, utilizando o dimensionamento do máximo positivo amostrado S13 x=3,276 m (não máximo estrutural exato) e d do vão independente. Todos os intermediários de A/B/C, al_base/al limitado, Vsd/Vc0 e dimensionamentos permanecem nos JSONs.

## Ancoragem corrigida

Boa aderência da N2 pelo centro físico y=72−68=4 cm, abaixo da fronteira de 42 cm; não se usa y da N3 nem centroide de várias camadas. Concretopy calcula fbd/lb/min/necessário, com gancho válido=True informado pelo engenheiro. Não se reaplica a condição al+lb do escalonamento nesta verificação de apoio.

| Viga | As efetiva | As apoio | lb básico | lb mínimo | lb necessário | lb_ef | Margem (cm) | As_corr | As adicional | Atende |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| V536 | 9.424778 | 5.917168 | 55.071689 | 20.000000 | 24.203000 | 21.500000 | -2.703000 | 10.609670 | 1.184892 | False |
| V565 | 9.424778 | 5.200058 | 55.071689 | 20.000000 | 21.269804 | 21.500000 | 0.230196 | 9.323869 | 0.000000 | True |

Comparações feitas sem arredondar números antes da decisão. A mudança da V565 decorre exclusivamente da entrada geométrica corrigida; não houve modificação das equações do Concretopy nem dos esforços/camadas originais. As_corr/As_adicional são resultados matemáticos mantendo a configuração, não dimensões de grampo.

## Reprodução, rastreabilidade e limitações

[Script atualizado](../../analises/pranchas/validar_v536_v565_apoio_esquerdo.py), [JSON V536](../../analises/pranchas/V536_left_support_anchorage_check.json) e [JSON V565](../../analises/pranchas/V565_left_support_anchorage_check.json) conservam contexto, dados documentais separados, fontes dos esforços, hashes, chamadas/respostas e decisões. O [ensaio anterior de 21 cm](V536_V565_left_support_anchorage_check_21cm_historical.md) foi preservado como histórico superado.

A busca e a validação atual estão no [relatório de alternativas](V536_support_alternatives.md). Cabimento transversal completo, espaçamentos, raio/pino/cobrimento/confinamento do gancho e reforços adicionais específicos não foram certificados. A aprovação numérica da V565 não é aprovação global ou detalhamento pronto. O cenário de gancho foi fornecido pelo engenheiro, sem geometria automaticamente inspecionada.

Os contratos consultados fazem referência à NBR 6118:2023; não foi consultado novamente o texto integral da norma nem inventado critério normativo de escolha dos pares ou de lb_ef. Essas seleções são decisões de engenharia registradas.
