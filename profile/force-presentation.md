# Apresentação de esforços — preferência permanente de João

Solicitada expressamente em 15/10/2026. Aplicar por padrão a todos os projetos, respostas, relatórios, tabelas e gráficos do assistente, inclusive ATP e revisão de armaduras, salvo orientação específica posterior de João.

## Unidades e base de comparação

- Forças, reações e cortantes: tf. Momentos fletores e torsores: tf·m. Cargas distribuídas: tf/m, tf/m² ou unidade correspondente à grandeza.
- Apresentar solicitações na base característica, preservando sinal, combinação/envoltória e origem TQS. Identificar Sk, Mk, Vk, Nk ou Rk conforme a grandeza. Uma combinação não se transforma em ação característica individual apenas pela troca do rótulo.
- Comparar com resistência equivalente na mesma base: Rk,eq = Rd/γf; para momentos, Mk,eq = MRd/γf. Identificar explicitamente como resistência equivalente para comparação. Isso não é resistência característica do material ou da seção calculada com fck/fyk sem coeficientes de segurança.
- A verificação de segurança continua na base de cálculo aplicável, com os coeficientes das ações e dos materiais. Não retirar γc/γs das resistências. A apresentação equivalente conserva a razão Sd/Rd = Sk/Rk,eq quando Sd = γf Sk.
- Converter Sd para Sk somente com origem e γf documentados. Não adotar 1,4 universalmente. Havendo fatores diferentes por ação/combinação, recuperar a base característica na origem ou decompor os termos comprovados. Sem conversão demonstrável, identificar o resultado como de cálculo em tf/tf·m e registrar a impossibilidade de obter a base característica; nunca trocar o rótulo ou inventar o fator.
- Se o dado já for característico, não dividir novamente por γf. Não multiplicar uma resistência de cálculo por γc/γs para chamá-la de característica.

## Conversões e registro

- 1 tf = 9,80665 kN; 1 tf·m = 9,80665 kN·m = 980,665 kN·cm.
- Conversão de unidade e conversão de natureza são operações distintas. Exemplo com γf comprovado de 1,4: Mk[tf·m] = Msd[kN·m]/(1,4 × 9,80665); Mk,eq[tf·m] = MRd[kN·m]/(1,4 × 9,80665).
- Não dividir áreas de aço, comprimentos ou espaçamentos por γf. Manter as unidades adequadas dessas grandezas e as tensões dos materiais em MPa.
- Preservar precisão interna e resultados originais das ferramentas, inclusive unidades, natureza e coeficientes. Converter na camada de apresentação; não reescrever arquivos brutos nem modificar motores resistentes apenas para mudar a convenção.
- Informar unidade e natureza nos cabeçalhos; registrar γf aplicável e a definição da resistência equivalente junto à comparação. Limites superiores resistentes continuam identificados como limites, não como capacidade efetiva.
- Usar normalmente duas casas decimais nos esforços apresentados, ampliando quando necessário. Decidir atendimento com valores completos, nunca com os números arredondados.
- Documentos históricos conservam sua convenção original. Uma reapresentação deve ser identificada como conversão, preservar a origem e não sugerir uma nova verificação estrutural.

## Origem do resultado oficial — orientação de 15/10/2026

Nas verificações de capacidade resistente das vigas, o resultado oficial apresentado a João deve ser o obtido pelo Concretopy, com identificação da função/modelo empregado, dados de entrada, unidade, natureza e registro bruto que o sustenta. A preferência de unidade/base de apresentação permanece aplicável ao resultado do motor.

Para flexão positiva, considerar a armadura inferior tracionada, sem contribuição resistente das barras superiores, salvo orientação específica posterior de João. Não usar limite superior com aço superior como capacidade oficial. Na negativa, identificar a armadura tracionada pertinente; não aplicar a regra da positiva de modo a excluir as barras superiores tracionadas.

Cálculos independentes, fórmulas auxiliares e limites algébricos são conferências complementares. Separá-los da tabela e da conclusão oficial e informar explicitamente origem, método, entradas, finalidade e limites. Nunca atribuir ao Concretopy resultado obtido fora dele, nem substituí-lo silenciosamente por outra verificação. Divergência com o motor deve ser registrada e investigada; não declarar aprovação oficial enquanto uma inconsistência relevante permanecer sem solução.

Se o Concretopy não tiver sido efetivamente executado para o controle/configuração, registrar a verificação oficial como não realizada ou pendente; não preencher sua ausência com uma conta independente identificada como oficial. Resultados arquivados podem ser utilizados com rastreabilidade e identificação das entradas, sem sugerir novo processamento. Mudanças de entrada exigem nova execução do motor.

## Momento negativo no apoio — orientações de João em15 e16/10/2026

Usar o máximo negativo fornecido pelo TQS na região de cada extremidade do próprio vão, sem reduzir/interpolar a solicitação para a face interna. Preservar sinal, envoltória, posição e fonte. Consultar as seções terminais S1/S13 e outros pontos comprovadamente dentro do apoio, selecionando o máximo daquele lado.

Em vigas contínuas, verificar separadamente os dois lados de cada apoio: fim do vão anterior e início do vão seguinte. Não substituir os dois valores pelo maior entre eles, mesmo que o pilar e a armadura sejam iguais. Associar cada demanda à seção e à armadura correspondentes ao próprio lado. Isso também se aplica à continuidade entre vigas com nomes documentais diferentes.

Exemplo confirmado por João: V43/P723, fim do trecho3: Mk=-8,697tf·m; início do trecho4: Mk=-12,707tf·m. Não repetir12,707tf·m nos dois lados. A orientação de16/10 esclarece e substitui a interpretação anterior que unificava o apoio compartilhado. Não atribuir essa escolha do engenheiro a requisito normativo não consultado.
