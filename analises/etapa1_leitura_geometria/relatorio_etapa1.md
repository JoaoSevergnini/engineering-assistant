# Relatório — Etapa 1: leitura documental e geometria física das vigas

Projeto: 24-212 — TGD Silva Jardim, pavimento TIPO. Data: 09/10/2026.

Foram implementados os contratos documentais e físicos, a identificação dos balanços no VGESFS e a validação local das entradas dos controles. Os contratos antigos e os métodos resistentes existentes foram preservados. Esta entrega é de infraestrutura de revisão: não constitui nova aprovação estrutural das vigas.

## Auditoria e arquitetura

A [auditoria inicial](auditoria_inicial.md) foi registrada antes da implementação. A ligação documental → modelo longitudinal era a principal lacuna: o contrato usava uma posição por marca e seção geral, enquanto os scripts do caso tratavam ocorrências repetidas e mudanças de altura separadamente. A regex do extrator não reconhecia linhas geométricas cujo número de vão terminava em B.

A extensão foi incorporada ao modelo longitudinal existente. O [contrato detalhado](../../tools/beam_model/STAGE1_CONTRACT.md) descreve campos, versões, critérios e integrações.

| Componente | Resultado |
|---|---|
| `input_evidence.py` | seis estados de evidência, unidades, origens de critérios, comprovação e conflitos |
| `pdf_observations.py` | leitura por zonas, rótulos e tabela TQS declarada; texto, página, caixas e SHA256; linhas não reconhecidas preservadas |
| `documentary_reconciliation.py` | conciliação por representação/marca/ocorrência; comparações por significado da quantidade; sem fonte prioritária presumida |
| `physical_geometry.py` | trechos, níveis, offsets, ocorrências, intervalos, camadas, classificação de vãos e adaptadores aos contratos existentes |
| `consolidar_detalhamento.py` | extensão opcional documental 1.3 → modelo 1.1; validação por replay; compatibilidade antiga |
| `extrair_viga_lst.py` / `consolidar_viga.py` | tokens B preservados e classificação propagada com origem |
| `input_preflight.py` | dependências por controle/intervalo; guarda de execução; preparação de lotes constantes |
| `longitudinal_review.py` | caminho físico integrado para flexão positiva/negativa, usando o motor existente |
| diagnóstico / correction engine | evidências anexáveis e guarda opcional das entradas; sem geração de propostas nesta etapa |
| Skill reinforcement-review | referência e orientação para o procedimento da Etapa 1 |

O mapeador legado continua restrito a um vão. Os novos lotes físicos exigem eixo comum explicitamente declarado e comprovação do registro dos esforços. Não foi criado um segundo modelo resistente nem foram liberados casos que o mapeador antigo não suporta.

## Conciliação documental e geometria

A marca identifica a posição no desenho; a ocorrência identifica um grupo físico distinto; a representação identifica cada menção em elevação, corte ou tabela. A representação não acrescenta barras. Quantidade total de posição, quantidade de ocorrência e contagem em corte são comparadas separadamente. Somar ocorrências contra o total da tabela exige inventário comprovadamente completo.

Falta de extração, ausência de representação numa leitura completa, divergência documental e falha de integridade têm registros distintos. Nenhum deles é automaticamente convertido em ausência física de armadura. Revisão desatualizada exige prova; data antiga isoladamente não basta.

Os trechos guardam largura/altura, forma da seção, níveis, deslocamento lateral, limites e origem. Não se cria seção média. Transições sem cotas ou referência física suficiente permanecem não localizadas. A consulta de barras distingue presença, ausência comprovada e posição indeterminada; mantém camadas e ocorrências separadas. Continuidade, emendas e extensões não documentadas não são completadas por hipótese silenciosa.

A convenção confirmada para o término não cotado na face externa do pilar terminal foi reutilizada, com origem `OFFICE_STANDARD`. Cota explícita prevalece. Apoios internos não resolvidos permanecem pendentes. Sobreposição gráfica não foi convertida em colisão.

## Casos reais: antes e depois

A comparação abaixo se refere aos contratos e inventários anteriores. Não substitui ou reescreve as conclusões dos relatórios históricos.

| Caso | Situação na entrada anterior | Resultado desta etapa |
|---|---|---|
| V623 | inventário gráfico com N3 e duas ocorrências N1; N2 não estava nesse inventário | N2 registrado como posição existente, 4Ø16 C464; perda da elevação por truncamento confirmada pelo usuário; intervalo/cortes/extensões/camadas longitudinais permanecem pendentes |
| V623 — tabela | informação já conhecida na revisão, sem leitor documental reutilizável de tabela | leitura independente do PDF extraiu quatro linhas; N2 = 4, Ø16, C464, com caixa, página, texto e SHA256 |
| V623 — N1 | repetição da marca em duas peças físicas | duas ocorrências mantidas, sem duplicação por tabela/corte e sem colapso em uma barra contínua |
| V610 | alturas locais 129,5 / 47 / 122 tratadas no script do caso | alturas registradas separadamente; limites e níveis ainda não comprovados no novo contrato; nenhum cálculo com altura média |
| V611 | região local com altura 47 e restante 57 | regiões distintas registradas; a distribuição de estribos não foi usada isoladamente para comprovar as coordenadas da transição |
| V626 | balanço esquerdo e seção local 47, trecho principal 57 | token 1B recuperado; lado esquerdo confirmado visualmente na elevação, relativo a P31; limites físicos ainda pendentes; não tratado como término em pilar |
| V606 | seção constante e coordenadas gráficas do inventário | seção constante preservada; coordenadas gráficas continuam hipóteses, não cotas resistentes comprovadas |
| V617/V620/V622/V625/V627/V629 | B ausente da normalização geométrica | 2B/4B reconhecidos; lado direito conferido visualmente; extensão física registrada como pendente de comprovação no eixo comum |

Os sete registros B foram recuperados do VGESFS original, com linha/texto de origem. O comprimento tabular do TQS não foi equiparado automaticamente ao comprimento físico da extensão. A orientação qualitativa pôde ser conferida nas elevações; isso não fornece, por si só, as abscissas de suas faces.

Nos cinco casos migrados, os intervalos gráficos antigos foram classificados como hipóteses e as camadas manuais ainda sem associação suficientemente comprovada foram mantidas como hipóteses. As verificações locais que dependem desses dados permanecem pendentes. Não houve recálculo numérico nem nova liberação resistente dessas vigas.

Artefatos: `Vxxx_document_stage1.json`, `Vxxx_model_stage1.json`, `Vxxx_tqs_stage1.json`, [comparativo real](comparativo_real.json), [balanços reais](balancos_reais.json) e [extração da tabela V623](V623_pdf_table_observations.json).

## Integração dos controles

O preflight separa controles executáveis e pendentes por intervalo e dependência. Mantém envoltórias TQS, sem exigir combinações concomitantes. Seção T não entra silenciosamente no motor retangular. Ancoragem simplificada permanece no escopo; pinos, trajetória curva e interferência com armaduras de pilares não se tornaram requisitos obrigatórios.

Flexão tem uma entrada integrada que prepara a seção constante local e chama o verificador anterior. Ancoragem, cisalhamento, escalonamento e suspensão podem usar `execute_control` com seus verificadores existentes. A guarda não chama o cálculo quando faltam suas entradas. Diagnóstico preserva evidências e estados técnicos/de execução. Hipóteses exigem opção explícita e produzem resultado condicional.

Os argumentos novos são opcionais para preservar compatibilidade. Portanto, scripts históricos que continuarem chamando diretamente os verificadores antigos não adquirem automaticamente a proteção do novo preflight. A migração de chamadores deve ser deliberada.

## Testes e preservação

Resultado: **1.134 testes aprovados** nas quatro suítes; **69 testes novos** sobre a linha de base de 1.065.

| Suíte | Testes |
|---|---:|
| beam_model | 71 |
| extrator_lst | 42 |
| beam_mapping | 57 |
| reinforcement_checks | 964 |

Foram testados documentos completos/incompletos/divergentes; quantidades de diferentes escopos; bitolas, comprimento nominal e formas; revisão desatualizada comprovada; truncamento; ocorrências repetidas; limites desconhecidos; camadas conflitantes; níveis incompatíveis; seção variável; B, orientação e conflitos; independência local dos controles; bloqueio de chamadas sem entradas; convenção de face externa; diagnóstico e guarda de correções.

Um teste de integração comparou o resultado completo da flexão negativa de uma seção constante com o motor anterior: igualdade do resultado numérico. Os casos sintéticos estão identificados como tais; as regressões reais preservam as lacunas documentais. Os testes de leitura B também conferem o VGESFS original disponível nesta máquina.

Execução e saídas: [test_results.json](test_results.json), `run_tests.py`, `regressao_real.py` e `regressao_pdf_real.py`. Após ajustes finais de identidade/proveniência, foram repetidas as suítes diretamente afetadas: beam_model e testes novos de preflight/integração física, novamente aprovados.

Os inventários históricos usados pela migração tiveram SHA256 conferido antes/depois em [historical_inputs_preserved.json](historical_inputs_preserved.json). Pranchas, relatórios históricos e Concretopy não foram alterados. As alterações anteriores existentes no código foram preservadas; a implementação foi acrescentada aos seus contratos.

## Limites e próximos passos

O leitor PDF ainda requer zonas e colunas identificadas. Não implementa reconhecimento universal de todas as tabelas, associação automática de cada ponto em corte a uma marca ou recuperação do conteúdo perdido na plotagem. Formas de barra podem ser reconciliadas quando registradas de maneira comparável; não há reconstrução automática completa das dobras.

Os contratos aceitam cotas e trechos comprovados, mas esta etapa não certificou as coordenadas de transição, níveis e camadas de todas as vigas reais. O tipo B também exige completar o registro das faces físicas no eixo comum. Esses dados devem ser resolvidos para reduzir as pendências sem introduzir precisão aparente.

Para a Etapa 2, priorizar: extração/validação de cadeias de cotas e faces na forma/elevação; associação de cortes, camadas e ocorrências; ampliação da leitura das tabelas com revisão de cobertura; migração dos chamadores históricos para as entradas protegidas; registro explícito dos eixos e offsets entre trechos e esforços. Essas são melhorias das ferramentas e da qualidade das entradas, não propostas de alteração do detalhamento.
