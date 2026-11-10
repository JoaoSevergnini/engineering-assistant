# Ferramentas existentes e limites de uso

Inventário conferido por leitura do código no incremento 1B. Não houve
reprocessamento S07 ou execução dos motores. Existência de função/teste não
equivale a validação geral. Não há CLI que execute uma ATP completa de lajes.

Caminhos abaixo são relativos à raiz do engineering-assistant.
CP é o repositório irmão ../concretopy, atualmente localizado em
\\srvmaster\PUBLICO\Joao Severgnini\Simon\concretopy, externo a este repositório.
Resolver sua localização no ambiente em vez de presumir P: disponível.

## Padrão atual de entregáveis — S07 1º pavimento

Consultar [s07-1pav-deliverables](s07-1pav-deliverables.md) para os três PDFs
finais, emissores R02/R03, fichas R01, relatório técnico R00, inputs, dependências,
QA e adaptações. Este é o padrão de apresentação vigente; os geradores de PDF
do térreo permanecem como histórico de técnicas reaproveitáveis em
[ferramentas históricas](historical-tools.md).

Os dois indicadores já foram calculados no 1º pavimento, e há geradores para
os três formatos e para seleção interativa. Ainda não há CLI genérica integrada,
exclusividade garantida das checkboxes nem migração automática das decisões.

## Scripts do 2º pavimento S07 — base mais recente

A ATP do 2º pavimento (analises/atp_s07_lajes_2pav, área de trabalho local fora
do git) produziu o conjunto mais recente de scripts por função: leitura e
calibração dos diagramas (ler_diagramas_2pav, calibrar_diagramas_2pav,
refinar_calibracao_2pav), extração de armaduras e domínios
(extrair_armaduras_2pav, reconstruir_dominios_2pav), contornos das formas
(extrair_contornos_*), comparações por faixa com Concretopy
(comparar_{H,V,NEG_H,NEG_V}_individual_condicional, verificar_faixas_R03) e
emissão/QA (emitir_verificacoes_faixas_R04, verificar_pdfs_faixas_R04).
Esses scripts não foram inspecionados nesta reorganização: contêm caminhos,
premissas e parâmetros do 2º pavimento, e vários têm versões sucessivas.

Para um novo pavimento, copiar para scripts/ do pavimento somente o script da
função necessária, ler seu funcionamento, substituir caminhos e premissas pela
leitura do premissas.json e manter um script por função. Não importar nem
executar no local de origem. Não são ferramentas validadas para outro projeto.

## Seleção operacional

| Classe | Como utilizar |
|---|---|
| Direto, com entradas compatíveis | Funções de registro do 1A; área de barra e APIs Concretopy no domínio comprovado |
| Exige adaptação/verificação local | Geometria/quantificação do PoC, representação resistente de lajes, diagnósticos de vigas |
| Experimental/histórico | Reconhecimento por layout, contornos candidatos e scripts locais S07; primeiro inspecionar, depois decidir uso |
| Não implementado como fluxo geral para outro projeto | Emissão genérica dos três documentos, migração de decisões, catálogo de incompatibilidades e verificações integrais; o 1º pavimento S07 tem implementações específicas, inclusive dos dois indicadores |

O agente pode avançar por leitura assistida e cálculos aplicáveis sem esperar
automação completa. Uma ferramenta inadequada gera mudança de método ou pendência
local, não reprovação estrutural.

## tools/slab_review — uso direto para registro

| Recurso | Entradas → saídas | Uso e limites |
|---|---|---|
| common.py: Document, Evidence, Criterion, EngineerDecision, to_data | Dados explícitos → dataclasses e projeção JSON | Proveniência e estados; não abre documentos, autentica autor ou consulta norma |
| models.py: Slab, ThicknessRegion, ReinforcementOccurrence, GridLine, GeometryReference | IDs, valores e referências → entidades de lajes | Espessura uniforme ou zonas; geometria/momentos externos, sem reconhecimento ou composição física |
| review.py: assess_dependencies | Control e mapa bool → dependências ausentes/ready | Uso direto; disponibilidade informada pelo chamador, não inferida |
| review.py: record_outcome | Resultado informado e disponibilidade → novo Control | Valida estados/entradas; não verifica a engenharia nem persiste histórico automaticamente |
| review.py: review_evidence, review_finding | Registro e decisão atribuída → novo registro | Preserva leitura; ACCEPT/REJECT não muda resultado técnico |
| example_s07.py: build_example | Cenário interno → registros/JSON demonstrativos | Sem PDF/DXF e sem validade estrutural; não copiar decisões fictícias para um projeto |

Dependência: biblioteca padrão Python 3.10+. Uso da demonstração, já executada no
1A, a partir da raiz:

~~~powershell
python -B -m tools.slab_review.example_s07
~~~

O comando apenas imprime JSON. Não é comando de ATP. O contrato completo e o
comando de testes estão em [contracts](contracts.md); esta etapa documental
não reexecutou testes de engenharia.

## Ferramentas históricas e experimentais

Os scripts do térreo S07, os geradores históricos de PDF do térreo e o
tools/slab_geometry_poc estão descritos em
[ferramentas históricas e experimentais](historical-tools.md). Não foram usados
nos fluxos do 1º e do 2º pavimento; consultar somente ao avaliar reaproveitamento.

## tools/reinforcement_checks — princípios/primitivas de vigas

| Recurso | Entradas → saídas | Condição de reaproveitamento |
|---|---|---|
| moment_diagram.MomentDiagram: moment_at_x, find_crossings | Pontos x_m/value_knm e proveniência → diagrama linear, consultas/cruzamentos | Biblioteca padrão e módulo local tqs_moments; contrato de vigas em kN·m. Exige adaptação de origem/unidade para tf·m/m de lajes, sem reclassificar por nome de campo |
| longitudinal_review.composition_capacity, check_bar_event, basic_anchorage | Barras/contexto/diagramas/API → capacidades/eventos/Lb | CP e módulos locais; políticas de vigas, aderência e 10φ/decalagem não transferíveis automaticamente |
| negative_reinforcement_relations.review_negative_relation | Dois conjuntos, contexto, diagrama e evidências → classificação e verificações | CP/módulos locais; apenas referência de continuidade, não verificador de 2 Lb de lajes pronto |
| floor_review.review_floor | Especificação documental/TQS de vigas → revisão por viga/pavimento | Orquestração específica de vigas; não é entrada principal para ATP de lajes |
| diagnostic_update.md | Convenções de execução/resultado → orientação | Reutilizar a separação de estados, sem alimentar contratos de vigas com objetos de lajes |

## Concretopy — APIs existentes, chamadas condicionadas ao domínio

Inspeção realizada no código local; conferir novamente a versão quando calcular.

| Interface em CP/concretopy | Entradas → saídas | Limites e utilização |
|---|---|---|
| armaduras.Barra(diametro_mm).area_cm2 | mm → cm² | Primitiva diretamente reutilizável; verificar entrada positiva/finita no chamador |
| armaduras.CamadaArmaduraLongitudinal(numero_barras, barra, d_cm) | Quantidade inteira, barra igual e d explícito/opcional → camada | Não recebe densidade fracionária 100/s diretamente; camadas distintas com envelopes verticais sobrepostos são rejeitadas |
| secoes.SecaoRetangular(bw,h,cobrimento,diametro_estribo_mm) | Geometria em cm, estribo em mm → seção | Padrão de estribo de viga; representar cobrimento físico de laje explicitamente, sem criar estribo fictício no projeto |
| materiais.Concreto, Aco | fck/fyk em MPa → materiais | Não inferir classe de aço apenas da bitola fora de uma convenção confirmada do caso |
| verificacoes.flexao.verificar_flexao_viga_retangular | Seção, concreto, aço único, camadas, γc/γs e γf opcional → ResultadoVerificacaoFlexao | MRd em kN·cm; modelo de camadas tracionadas escoadas, fck 20–90 MPa no código inspecionado. Diagnósticos independentes; mínimo opcional é de vigas |
| verificacoes.ancoragem.calcular_ancoragem e CondicoesAncoragem | Materiais, bitola, áreas, aderência explícita e coeficientes → comprimentos em cm e diagnósticos | Retorna lb_cm básico e lb_nec_cm reduzível. Utilizar lb_cm para as regras de escritório 1 Lb/2 Lb; não é verificador universal de traspasse |

γf na API de verificação de flexão apenas solicita MRd/γf; não determina a
natureza do esforço do DXF. O posicionamento automático de camadas segue
convenções de vigas; não o usar silenciosamente em lajes.

Não há aqui adaptador geral integrado que resolva famílias intercaladas, materiais
mistos, mínimos de lajes ou a composição S07. Uma chamada isolada aplicável pode
ser coordenada pelo agente com memória de cálculo e supervisão; a solução
equivalente de analises/atp_s07_lajes_terreo/calculate.py continua específica e condicionada à validade.

## Como escolher antes de executar

Conferir entrada e revisão, assinatura da função, unidades, dependências e
destino/efeitos de gravação. Preferir uso das APIs sem efeitos globais e registros
do projeto. Se o script precisar de adaptação, registrar isso e usar leitura
assistida ou solicitar desenvolvimento em tarefa própria, sem alterar históricos
como efeito incidental de uma ATP.

Somente o comando demonstrativo acima é apresentado como execução pronta.
Outras interfaces foram verificadas por leitura; não há receita universal
validada de execução para novos PDFs/DXFs.
