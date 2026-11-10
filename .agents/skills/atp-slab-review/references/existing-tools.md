# Ferramentas existentes e limites de uso

Inventário conferido por leitura do código no incremento 1B. Não houve
reprocessamento S07 ou execução dos motores. Existência de função/teste não
equivale a validação geral. Não há CLI que execute uma ATP completa de lajes.

Caminhos abaixo são relativos à raiz do engineering-assistant:
A = analises/atp_s07_lajes_terreo; H = A/dxf_momentos;
V = A/dxf_momentos_verticais; G = tools/slab_geometry_poc.
CP é o repositório irmão ../concretopy, atualmente localizado em
\\srvmaster\PUBLICO\Joao Severgnini\Simon\concretopy, externo a este repositório.
Resolver sua localização no ambiente em vez de presumir P: disponível.

## Padrão atual de entregáveis — S07 1º pavimento

Consultar [s07-1pav-deliverables](s07-1pav-deliverables.md) para os três PDFs
finais, emissores R02/R03, fichas R01, relatório técnico R00, inputs, dependências,
QA e adaptações. Este é o padrão de apresentação vigente; a seção de PDFs do
térreo abaixo permanece como histórico de técnicas reaproveitáveis.

Os dois indicadores já foram calculados no 1º pavimento, e há geradores para
os três formatos e para seleção interativa. Ainda não há CLI genérica integrada,
exclusividade garantida das checkboxes nem migração automática das decisões.

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

## Scripts S07 — referência histórica, exigem adaptação

**Não importar diretamente os scripts abaixo.** Foram identificadas leituras,
cálculos, salvamentos de PDF/imagem e write_text no nível superior, sem proteção
integral por main. Importar para acessar uma função pode sobrescrever resultados.
Não fornecer comandos históricos como rotina pronta para outro projeto.

| Recursos reais | Entradas → saídas | Dependências, limites e uso |
|---|---|---|
| A/glyph_probe.py; decode.py: extract, canon; ocr.cjs, ocr_rot.cjs | PDF/vetores/templates/imagens → glifos, chamadas, TXT/TSV | PyMuPDF, NumPy, Pillow; Tesseract.js no OCR. Templates, camadas, cor e rotações do caso; estudar método, não reutilizar parâmetros cegamente |
| A/read_tables.py: extract, canon, row | PDF/templates/ocorrências → tabela e conciliações | PyMuPDF, NumPy, Pillow; zonas fixas, também altera ocorrências. Não é leitura pura nem pipeline inicial autônomo |
| A/regions_extract.py: row e auxiliares | Glifos/tabelas/vetores → ocorrencias_extraidas.json | PyMuPDF, NumPy, Pillow; barra/eixo/círculo em layers 8/3/6; H/V, candidatos por proximidade e retângulos nominais |
| A/consolidate.py | Ocorrências anteriores, tabelas e conferências → ocorrências corrigidas e triagens | Biblioteca padrão; recortes/coordenadas específicos e regravação. Referência de conciliação, não consolidador genérico |
| A/calculate.py: calc(fams,h,fck,offset), polygons | Ocorrências, PDF, zonas locais → regioes_capacidades.json e proveniencia_calculos.json | PyMuPDF, Shapely, CP; caminhos P:, h/material/cobrimento/base específicos. Homogeneização por resultante/centro e teste de escoamento; exige justificativa do domínio antes de adaptação |
| A/build_report.py; build_eight_sheets.py | Fontes e capacidades → relatório e oito pranchas | PyMuPDF, ReportLab, Pillow; layouts/fontes locais. Referência gráfica; não produz aprovação |
| H/gerar_mapa_negativos.py; gerar_mapa_media_picos.py | Componentes, calibração e geometrias → mapas, CSV/JSON | Shapely/Pillow e biblioteca padrão; média histórica ponderada e picos em manchas auxiliares são critérios diferentes |
| H/comparar_demanda_resistencia.py: lines, moment; gerar_comparativo_pdf.py | Capacidades e DXF preparado/alinhado → máximos, lacunas e comparativos | Shapely, bibliotecas gráficas do gerador; comparação histórica por máximo não equivale às médias finais |
| H/gerar_pranchas_comparacao_media.py: lines | Capacidades publicadas, componentes e alinhamento → médias por R, JSON/CSV e PDFs 7303/7307 | Shapely, ReportLab, PyMuPDF, Pillow; usa base como chave de linha, omite composições pendentes; não calcula média top 3 |
| V/preparar_vertical.py: find | entidades.json e textos.json → componentes, calibração, eixos e manchas | NumPy/Shapely; eixos canônicos, malha 17,5 e calibração locais. Não lê sozinho o DXF original |
| V/gerar_mapa_media_picos.py; gerar_pranchas_comparacao_media.py | Componentes verticais e capacidades → mapas e comparativos 7304/7308 | Adaptações verticais dos recursos anteriores; mesmas ressalvas de identidade, pendências e médias |

No térreo S07, a preparação inicial do parser DXF e parte do alinhamento horizontal não
estão integralmente persistidas em runner. Entidades JSON arquivadas não comprovam
existência de um importador genérico. As comparações finais são de negativas;
as positivas têm capacidades, sem comparação final correspondente concluída.

Consultar em modo de leitura inventario.json, ocorrencias_extraidas.json,
regioes_capacidades.json, proveniencia_calculos.json e comparacao_media_faixas.json
em H/V. Esses resultados exigem compatibilidade com suas entradas e hipóteses;
nunca constituem referência estrutural automaticamente correta para outra obra.

Conferências úteis:
V/7308_conferencia_cobertura.json registra N26 omitida no mapeamento e N28/N31
inclinadas pendentes. H/7307_conferencia_lacunas.json distingue suspeitas/vazio.
Não transferir “pendentes=0” para “todas as armaduras reconhecidas”.

## Referências para os PDFs gráficos padrão

Referência visual inspecionada:
[ATP_S07_7307_faixas_Mrk_Msol_media.pdf](../../../../analises/atp_s07_lajes_terreo/output/pdf/pranchas_regioes/ATP_S07_7307_faixas_Mrk_Msol_media.pdf).
O arquivo tem prancha-base vetorial, polígonos/rótulos de comparação e quadro
lateral. A inspeção constatou página única e ausência de imagens raster
embutidas; isso favorece ampliação, mas não dispensa revisão de legibilidade.
O padrão corrente dos três entregáveis está em
[reporting](reporting.md).

| Gerador histórico | O que pode servir de referência | Adaptação necessária |
|---|---|---|
| H/gerar_pranchas_comparacao_media.py | Referência histórica do térreo: show_pdf_page incorpora a prancha e a sobreposição ReportLab; drawpoly desenha contornos/anéis; num/arm/txt/fit, collision e placements organizam rótulos, chamadas, cores e quadro lateral. Salva PDF/JSON/CSV e renderiza QA | Procedimento no nível superior, pranchas/medidas/fontes e destinos específicos; apenas indicador 1, uma η e n; filtra issues e resistência ausente. Aproveitar técnicas gráficas, sem copiar o filtro; o padrão completo de dois indicadores, seleção e pendências está no 1º pavimento |
| V/gerar_pranchas_comparacao_media.py | Variante vertical com transformação de eixos, mesma composição vetorial e mrlabel para marcar hipótese de posição | Não copiar pranchas, transformações ou envelope horizontal de 20 mm. Conservar capacidade condicionada como tal; mesmas lacunas de indicador 2 e regiões pendentes |
| A/build_eight_sheets.py | drawpoly, fittext, collides e textos: todas as regiões resistentes cadastradas, capacidades/composições pendentes e determinadas chamadas sem faixa; painel, códigos, linhas de chamada e links internos código→quadro. Hash das fontes, manifesto e renderizações QA | Não compara solicitações; base Ø8 c/14 e seleção especial de N91 são do caso. Não truncar campos essenciais pelo fittext; generalizar pendências e parâmetros de layout. Complementa, não substitui o comparativo |
| H/gerar_comparativo_pdf.py | header/footer/wrap, quadros, evidências locais e mapas vetoriais sobre a fonte; útil para folhas de detalhe, máximo local e relatório complementar | Comparação histórica por máximos e médias de manchas MN é diferente dos dois indicadores por região. Não importar limiares, exclusões de apoios ou hipóteses S07 como padrão |
| A/build_report.py | Organização de diagnóstico, tabelas, ampliações e cobertura no relatório complementar | mapview rasteriza a prancha antes da sobreposição; preferir a incorporação vetorial dos geradores anteriores para os PDFs gráficos. Relatório não substitui as pranchas de verificação |

Esses recursos demonstram técnicas existentes, não API genérica pronta.
A emissão para um novo projeto exige entradas próprias e um caminho de produção
validado, sem importação dos scripts históricos com efeitos globais. Não basta
renomear o arquivo S07: selecionar materiais, h, camadas, coeficientes, fontes,
direções, indicadores e pendências a partir do novo projeto.

Os testes de presença de códigos, hashes e colisões de caixas dos históricos
são referências de QA, não comprovação de que anotações não encobrem o desenho.
Renderizar/inspecionar todas as páginas e detalhes conforme reporting.
A exigência documental não implementou gerador genérico; os emissores do térreo
não possuem o segundo indicador, já calculado nos scripts do 1º pavimento;
se não for possível emitir, registrar o impedimento e a entrega gráfica pendente,
sem declarar o relatório consolidado como substituto.

## tools/slab_geometry_poc — componentes experimentais separados do S07

O PoC usa outra família de pranchas, incluindo N26 diferente da N26/7308.
Não foram constatados imports desse fluxo nos scripts S07. Seus testes não
validam os cálculos resistentes ou a interpretação DXF do S07.

| Recursos/funções | Entradas → saídas | Uso, dependências e limitações |
|---|---|---|
| geometry.extract_page, parse_call; automatic.detect_layout, read_sheet, line_geometry | Página vetorial/textos → entidades, chamadas e associações | PyMuPDF na extração; heurísticas de layout e segmentos H/V; adaptar âncoras ao projeto |
| leaders.EndpointGraph, trace_leaders, resolve_trace | Entidades/ocorrências → líderes, destinos e alternativas | Auxilia leitura localizada; exploração limitada e ambiguidade explícita; não confirma semântica física |
| opening_groups.recognize_openings, reconstruct_localized | Vetores/líderes/perfil de convenção → candidatos de abertura e grupos | Retângulos e convenção documental específica; não dimensiona reforços nem generaliza o perfil SIM |
| distributed_regions.reconstruct, partition | Associações → regiões e células | Backend retangular alinhado aos eixos; não soma aço nem valida lajes |
| structural_regions; occurrence_relations.relation, propagate; acting_compositions.analyze, query | Regiões/evidências/relações → função, presença e composição documental | Mantém domínios, conflitos e confirmações; interseção não autoriza resistência conjunta |
| polygonal_slabs.reconstruct_slabs; complex_slab_contours.recognize; contour_validation.compare | Entidades/etiquetas/referência humana → contornos candidatos e métricas | Shapely; não é leitor definitivo das formas, não resolve automaticamente níveis/apoios |
| slab_assignment.partition_domains; refine_slab_assignment.refine; documentary_slab_assignment.analyze | Regiões, domínios e contextos → associações/espessuras | Shapely; RELIABLE documental não é validação completa do contorno ou da capacidade |
| steel_quantification.steel_rate; quantify_composition, quantify | Bitola/espaçamento, função e perfil → As/m e somas nominais elegíveis | Área delegada ao CP; sem d/MRd; perfis com hashes e confirmação. steel_rate isolada recebe callback de área e é reaproveitável com entradas compatíveis |
| run_sheet.py; run_* das etapas | PDF/inventários/perfis → JSON, tabelas e imagens | Runners geram arquivos, vários destinos e inputs padrão são do experimento; verificar main/args/OUT antes de uso |

G/README.md descreve a sequência e os testes sintéticos/replays; lê-lo antes de
selecionar uma etapa. Os runners dependem dos inventários anteriores, nem todos
aceitam destino arbitrário. Não executar seus defaults na pasta de um novo ATP.

Dependências por etapa: PyMuPDF em extração/renderização, funções geométricas
iniciais em biblioteca padrão e Shapely nas etapas poligonais. O arquivo
requirements-stage7.txt fixa Shapely 1.8.5.post1 no ambiente experimental.
Já o S07 usa STRtree com índices/predicate de API diferente. Não presumir
compatibilidade entre os ambientes ou instalar pacotes durante uma revisão
sem necessidade. Não foram executadas novas regressões no incremento 1B.

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
equivalente de A/calculate.py continua específica e condicionada à validade.

## Como escolher antes de executar

Conferir entrada e revisão, assinatura da função, unidades, dependências e
destino/efeitos de gravação. Preferir uso das APIs sem efeitos globais e registros
do projeto. Se o script precisar de adaptação, registrar isso e usar leitura
assistida ou solicitar desenvolvimento em tarefa própria, sem alterar históricos
como efeito incidental de uma ATP.

Somente o comando demonstrativo acima é apresentado como execução pronta.
Outras interfaces foram verificadas por leitura; não há receita universal
validada de execução para novos PDFs/DXFs.
