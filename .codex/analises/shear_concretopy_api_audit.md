# Lacunas da API de cortante — auditoria prévia à integração

Data: 07/10/2026. Fontes: concretopy.verificacoes.dimensionar_cortante_viga; concretopy.normas.espacamento_max_estribo_vigas_cm; VigaRetangular.vrd2_kn; criterio do item 18.3.3.2 confirmado pelo engenheiro nesta tarefa.

## Comparação do espaçamento máximo

A API existente testa VRd2 >= 0,67*Vsd. O critério fornecido pelo engenheiro é Vsd <= 0,67*VRd2 para o ramo 0,6d/30cm; acima disso, 0,3d/20cm. Para qualquer caso estruturalmente válido Vsd < VRd2, a comparação implementada fica verdadeira e o ramo restritivo não é alcançado. O defeito é determinístico e foi documentado antes de qualquer alteração. Não copiar a correção da equação para o assistant. Correção pontual no Concretopy depende da autorização solicitada nesta tarefa; enquanto não resolvida, conservar o retorno bruto como auditoria e marcar a certificação normativa pendente.

Também há divergência de d/coefficientes: a função normativa usa VigaRetangular.vrd2_kn com bitola longitudinal default e gamma_c default, enquanto o dimensionamento aceita outra bitola e gamma_c. A integração deve fornecer a própria VRd2 retornada pela chamada de cortante e a altura útil usada nessa mesma chamada, sem recalcular resistencia no assistant.

## Altura útil explícita

O dimensionamento público recebe bitola longitudinal e calcula SecaoRetangular.d(bitola). Não possui argumento d_cm para um centroide de múltiplas camadas. O engenheiro confirmou selecionar a região com maior número de camadas; desempate solicitado. Não inventar bitola equivalente. É possível usar um adaptador de SecaoRetangular que preserve a geometria física e forneça d explicitamente selecionado na chamada pública; isto deve ser documentado e testado contra os valores retornados das verificações de flexão existentes. Não duplicar o posicionamento/centroide nem equações de cortante.

## Retorno e inversão

ResultadoCortante contém apenas asw_por_s (governante, cm²/m), vc e vrd2 (kN). Não retorna separadamente parcela solicitante, mínimo, Vsd ou capacidade Vk inversa. Obter mínimo por chamada independente a Vk=0, sem copiar fórmula. Vsd vem da majoracao caracteristica gamma_f do contrato. Para transição diagnóstica, admite-se inversão numérica da chamada pública no espaço de Vk, seguida de crossing ANALÍTICO no diagrama existente; não discretizar o eixo x ou reimplementar equação resistente. Preservar todas as chamadas e os limites da inversão.

## Dados reais

Prancha V516/V517 relida: N13=Ø5 c/14 no vão 2 e trecho inicial do vão3; N13=Ø5 c/10 no final do vão3; N1=Ø8 c/12 no trecho52cm. N12=Ø8 c/20 nos vãos extremos possui geometria não convencional (pernas47/27cm e prolongamentos64cm). O engenheiro esclareceu que a peça serve à flexão de lajes adjacentes. Não inferir dois ramos resistentes convencionais para cortante sem regra específica; conservar a peça e a classificação funcional, com Asw/s resistente inconclusivo.
## Autorização e alteração pontual

O engenheiro autorizou explicitamente nesta tarefa corrigir exclusivamente a comparação de smax no Concretopy. Alteração: `vd_kn <= 0.67 * viga.vrd2_kn`. Adicionados oito testes independentes de fronteira/limites em tests/test_shear_spacing.py. Nenhuma equação de resistência ao cortante, área mínima, flexão, ancoragem ou decalagem foi alterada. As demais lacunas são tratadas por adaptação/orquestração no assistant.

Seleção de altura útil confirmada: máximo número de camadas; em empate maior As total; em novo empate menor d. Reutilizar valores retornados pela flexão regional. Registrar engineer_confirmed_shear_effective_depth_max_layers_v1, com a seleção e todos os candidatos. N12 foi confirmada pelo engenheiro como peça não convencional que atende flexão de lajes adjacentes; não atribuir automaticamente Asw/s convencional.

## Esclarecimento posterior — 08/10/2026

O tratamento anterior de N12 como peça de cortante com ramos pendentes foi superado pela decisão expressa: armadura NEGATIVA das lajes adjacentes, para continuidade em desnível, excluída do cortante da viga. Isso não documenta estribos nos vãos extremos. A exigência de continuidade dentro dos pilares também foi superada: cobertura obrigatória somente entre faces comprovadas. Auditoria histórica acima preservada.

O engenheiro reafirmou a autorização da correção pontual de smax realizada em 07/10/2026. Mantida a comparação e os oito testes; nenhuma nova mudança no Concretopy. Autorização administrativa e critério técnico fornecido são fontes distintas.
