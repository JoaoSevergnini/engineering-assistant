# Relatório técnico — procedimento de revisão de armaduras de lajes

**Projeto:** ATP S07 — Terra All Resort, Porto Belo–SC.  
**Auditoria documental:** 23/10/2026.  
**Finalidade:** registrar o fluxo efetivamente implementado nesta conversa para subsidiar uma futura skill. Não constitui nova verificação resistente ou emissão de ATP.

## Como interpretar este documento

O relatório distingue **implementado e executado no S07**, **conferido localmente**, **pendente/não validado** e **proposto para formalização**. Código existente, resultado numérico e arquivo chamado “validação” não equivalem a validação geral.

Foram lidos scripts, resultados e registros de conferência, sem reexecutar cálculos ou geradores. As contagens são as dos artefatos arquivados. Nenhuma funcionalidade ou skill foi criada/modificada nesta tarefa.

**Caminhos usados no relatório:**

- `REPO` = `\\srvmaster\PUBLICO\Joao Severgnini\Simon\engineering-assistant`.
- `A` = `REPO/analises/atp_s07_lajes_terreo`.
- `H` = `A/dxf_momentos`; `V` = `A/dxf_momentos_verticais`.
- `CP` = `\\srvmaster\PUBLICO\Joao Severgnini\Simon\concretopy`, repositório externo ao `engineering-assistant`.
- `ATP` = `S:/PROJETOS EM EXECUÇÃO/25-208-WERT-ATP TERRA ALL RESORT-PORTO BELO-SC/PRANCHAS/APOIO/JOAO/ATP S07`.

Os scripts ainda usam caminhos absolutos `P:\Joao Severgnini\Simon\...`. O acesso por UNC nesta auditoria não os tornou portáteis.

## 1. Objetivo e escopo

### 1.1 Verificações e produtos efetivamente realizados

1. Inventário das formas 7202/7214 e detalhamentos 7301–7308, com nomes/revisões, dimensões, páginas e SHA-256.
2. Leitura assistida das chamadas e tabelas em PDFs vetoriais, cujos textos principais estavam convertidos em traços.
3. Reconstrução de ocorrências e retângulos nominais de atuação; conciliação parcial por marca, diâmetro, comprimento e tabela.
4. Composição regional de positivas de base/reforço e tratamento conservador de sobreposições negativas.
5. Associação com materiais, espessuras e camadas; cálculo de As/m e resistência nominal à flexão pelo Concretopy.
6. Relatório preliminar de 98 páginas e oito pranchas anotadas com regiões, armaduras, As/m e resistência equivalente.
7. Leitura dos DXFs de momentos horizontal/vertical, posteriormente fornecidos.
8. Mapas auxiliares de manchas negativas e médias de picos por linha.
9. Comparação final pela média nas negativas horizontais 7303/7307 e verticais 7304/7308.
10. Conferências pontuais de cobertura, incluindo suspeitas na 7307 e omissão de armadura no mapeamento da 7308.

A laje principal foi interpretada como praticamente contínua, com 20 cm, concretada depois dos blocos e com exceções locais, conforme João. A primeira concretagem dos reservatórios até +9,28 m permaneceu condicionante documental, sem modelo resistente completo da junta.

### 1.2 Tipos de armadura e situações atendidos

- Distribuídas retas horizontais/verticais reconhecidas no layout deste projeto.
- Positivas com base Ø8 c/14 e reforços locais intercalados na mesma camada, por orientação de João.
- Diferentes diâmetros e a parametrização CA60 para Ø5/CA50 para demais bitolas.
- Negativas isoladas; sobreposições com capacidades individuais e soma pendente.
- Divisões locais por concreto e espessura explicitamente delimitadas.
- Momentos negativos recuperados de amplitudes gráficas, inclusive abaixo do filtro de rótulos quando o traçado permaneceu disponível.

**As resistências positivas foram calculadas, mas não houve comparação final das positivas com solicitações nesta conversa.** Os PDFs finais de demanda/resistência são de negativas.

### 1.3 O que não foi concluído

Revisão normativa integral da NBR 6118:2023; mínimos próprios de lajes; ELS/fissuração/flechas; punção; cortante; fadiga; desenvolvimento de ancoragens/emendas/cortes; juntas; cabimento e interferências gerais; resistência conjunta com blocos/apoios; tratamento de momentos torçores; validação de cargas, combinações, redistribuições e modelo TQS.

As formas foram consultadas e houve checklist, mas contornos, aberturas, níveis, apoios e individualização completa de L1/L8 não ficaram integralmente conciliados. Não foi comprovada a última emissão coordenada de todo o conjunto.

Padrões internos não foram usados como exigências de aprovação do ATP. Este relatório não consulta novamente o texto normativo e não atribui respaldo normativo geral à média escolhida para esta rodada.

## 2. Ferramentas existentes

### 2.1 Preexistentes efetivamente reutilizadas

| Componente | Caminho/interface confirmado | Uso |
|---|---|---|
| Concretopy | `CP/concretopy/verificacoes/flexao.py`: `verificar_flexao_viga_retangular` | Modelo retangular aplicado à faixa equivalente de laje. |
| Armaduras | `CP/concretopy/armaduras.py`: `Barra`, `CamadaArmaduraLongitudinal` | Área da barra e camada explícita. |
| Materiais | `CP/concretopy/materiais.py`: `Concreto`, `Aco` | Materiais da verificação. |
| Seção | `CP/concretopy/secoes.py`: `SecaoRetangular` | Seção equivalente. |
| PyMuPDF (`fitz`) | Biblioteca instalada | `open`, `get_drawings`, `get_text`, `get_pixmap`, `show_pdf_page`, links e salvamento. |
| Shapely | Biblioteca instalada | `Polygon`, `box`, `Point`, `LineString`, `shape`, `unary_union`, `affine_transform`, `STRtree`. |
| NumPy | Biblioteca instalada | Glifos, calibração e ajustes numéricos. |
| Pillow | `Image`, `ImageDraw`, `ImageFilter`, fontes | Glifos, recortes, mapas e conferência visual. |
| ReportLab | `canvas`, `pdfmetrics`, `TTFont` | PDFs, tabelas, sobreposições e legendas. |
| Tesseract.js | Chamado pelos `.cjs` locais | OCR auxiliar normal e girado. |
| Instruções | `REPO/AGENTS.md`, `profile/force-presentation.md`, `.agents/skills/reinforcement-review/SKILL.md` | Princípios de ATP, unidades/natureza e separação de controles. |

O SHA-256 arquivado de `flexao.py` é `d03a9cc1f513759ef489572e5d0b9709b63efcec6e31a1ff489f7d6ccb0f5cd8`; nesta auditoria, o arquivo apresentou o mesmo hash. Isso não congela a versão de todas as dependências.

### 2.2 Desenvolvidas/adaptadas durante o S07

Caminhos relativos a `A`:

| Script | Funções/responsabilidade verificadas |
|---|---|
| `glyph_probe.py` | Exploração e agrupamento inicial de glifos; auxiliar `root`. |
| `ocr.cjs`, `ocr_rot.cjs` | OCR auxiliar, saídas TXT/TSV. |
| `decode.py` | `extract`, `canon`: caminhos → glifos → chamadas candidatas. |
| `read_tables.py` | `extract`, `canon`, `row`: tabela e conciliação de marca/φ/C. Também altera ocorrências e separa notas. |
| `regions_extract.py` | `extract`, `canon`, `row`, auxiliares `point`/`bt`: chamada–barra–círculo–eixo e retângulo nominal. |
| `consolidate.py` | Execução direta: reaplica conferências, concilia marcas e faz triagem quantidade/espaçamento/faixa. |
| `calculate.py` | `polygons`, `calc(fams,h,fck,offset)`: composição, seção, d e Concretopy. |
| `build_report.py` | `start`, `end`, `wrapped`, `mapview`: relatório de 98 páginas. |
| `build_eight_sheets.py` | `num`, `arm`, `texts`, `color`, `drawpoly`, `fittext`, `collides`: oito pranchas. Adaptado para rótulos fora da região. |
| `dxf_momentos/gerar_mapa_negativos.py` | Mapa horizontal histórico com média ponderada pela extensão de segmentos. |
| `dxf_momentos/gerar_mapa_media_picos.py` | Média aritmética de picos por linha em manchas MN. |
| `dxf_momentos/comparar_demanda_resistencia.py` | `lines`, `moment`: comparação histórica por máximo e lacunas. |
| `dxf_momentos/gerar_comparativo_pdf.py` | Relatório histórico de máximos locais, mapas/tabelas. |
| `dxf_momentos/gerar_pranchas_comparacao_media.py` | `lines`, desenho/texto e `collision`: médias dentro das R; PDFs 7303/7307. |
| `dxf_momentos_verticais/preparar_vertical.py` | `find` e execução direta: componentes, calibração, eixos locais e manchas. |
| `dxf_momentos_verticais/gerar_mapa_media_picos.py` | Adaptação vertical; auxiliares `xy`/`cxy`. |
| `dxf_momentos_verticais/gerar_pranchas_comparacao_media.py` | Adaptação 7304/7308; `mrlabel` marca hipótese de camada. |

São scripts do caso, predominantemente procedurais. Não há classes próprias de aplicação ou API genérica consolidada. Importar os arquivos pode executar cálculos/sobrescritas por haver código no nível superior.

### 2.3 Operações executadas sem script próprio consolidado

Inventário/renderização inicial; parser ASCII dos dois DXFs; preparação horizontal de componentes/calibração; ajuste do alinhamento; parte das auditorias; triagens/recortes de cobertura foram executados por comandos Python durante a conversa.

Os dados e registros persistem, mas não se localizou importador DXF genérico nem runner que reproduza tudo do zero. `entidades.json`, `textos.json`, `alinhamento_pdf.json` e similares não devem ser apresentados como prova de que exista uma função de preparação integral persistida.

### 2.4 Ferramentas preexistentes não integradas a esta execução

`REPO/tools/slab_geometry_poc/` contém `geometry.py`, `automatic.py`, `leaders.py`, `distributed_regions.py`, `occurrence_relations.py`, `acting_compositions.py`, `steel_quantification.py`, `slab_assignment.py`, `documentary_slab_assignment.py`, `complex_slab_contours.py` e testes. O Git registra trabalho nessa pasta em 18/10/2026, anterior à rodada S07.

Seu README descreve outra família de pranchas, inclusive um experimento N26 diferente da N26/7308. Não foram encontrados imports desse pacote nos scripts locais do S07. **Seus testes não validam automaticamente o cálculo resistente/DXF desta conversa.** Integração futura é proposta, não etapa executada. Igual distinção vale para os verificadores de vigas e o orquestrador de pavimento do repositório.

## 3. Fluxo de execução

A sequência real foi iterativa, com correções visuais e reprocessamentos. Não existe hoje um comando único equivalente.

### 3.1 Contexto e inventário

**Entradas:** `ATP/DOCUMENTACAO ATP/CONTEXTO ATP S07.md`, formas em `ARQUIVOS RECEBIDOS/FORMAS`, detalhamentos em `ARQUIVOS RECEBIDOS/TÉRREO` e orientações de João.

**Ferramentas:** comandos locais, PyMuPDF, hashes, renderização/OCR.

**Saídas:** `inventario.json`, `*.png`, `*_words.json`, `*.txt`, `*_annots.json`, leituras OCR.

**Extraído:** documentos/revisões, páginas, tamanhos, hashes e limitações do texto vetorial. `get_text()` não fornecia as chamadas principais.

**Intervenções:** selecionar fontes; confirmar montagem H primeiro/V segundo, reforço intercalado, γf=1,4 e negativas sem soma pendente. Ler materiais/cobrimentos nas pranchas.

**Ambiguidades:** não presumir revisão coordenada pelo nome; +9,37 m global não resolve desníveis locais; comentários do revisor não equivalem a emissão do projetista. Essas decisões não foram todas automatizadas.

### 3.2 Chamadas e tabelas

**Entradas:** PDFs, inventário, `training_glyphs.json`, `glyphs_7301.json`, imagens.

**Ferramentas:** `glyph_probe.py`, `decode.py`, OCR `.cjs`, `read_tables.py`.

**Saídas:** `*_glyphs.json`, `*_glyph_lines.json`, `tabelas_aco_extraidas.json`, TXT/TSV e conciliações.

Glifos são normalizados em 64×64, comparados a exemplos locais por vetores NumPy em 0°/90°, com N como semente de chamada. A tabela usa zonas fixas de coordenadas deste layout.

**Intervenções:** exemplos rotulados; leitura visual de marcas/bitolas/espaçamentos. Há 29 conferências visuais vigentes e 15 correções finais de marcas; uma etapa anterior de tabela tem 30 correções e 64 pendências. Não são contagens equivalentes nem índices de acerto global.

**Erros:** candidatos ambíguos não recebem automaticamente solução definitiva. Entretanto, N26/7308 demonstrou omissão silenciosa: lista de pendentes vazia não comprova extração completa.

### 3.3 Associação geométrica

**Entradas:** glifos, tabelas e caminhos PDF. **Ferramenta:** `regions_extract.py`. **Saída:** `ocorrencias_extraidas.json`.

O extrator procura barra na camada 8, eixo de distribuição na 3 e círculo na 6; une fragmentos colineares e associa o eixo perpendicular. A alternativa de proximidade fica marcada `NEAREST_CIRCLE_AND_PERPENDICULAR_AXIS_REQUIRES_VISUAL_REVIEW`.

Cada O contém marca, φ/s, As individual, textos bruto superior/inferior, caixa da chamada, orientação, candidatos e `region_pdf`. O retângulo é envoltória nominal da barra/eixo, não contorno físico ou comprimento eficaz ancorado.

**Erros/decisões:** `PENDING_BAR_GEOMETRY`, `PENDING_BAR_AMBIGUITY`, `PENDING_DISTRIBUTION_AXIS_*`; revisão visual de candidatos. Listas de diâmetros e faixa 5–40 cm de espaçamento são filtros do extrator, não prescrições normativas.

### 3.4 Consolidação

**Entradas:** ocorrências atuais/anteriores, tabelas, conferências visuais. **Ferramentas:** `read_tables.py`, `consolidate.py` e ajustes locais.

**Saídas:** ocorrências revisadas; `conferencias_visuais_locais_vigentes.json`, `conciliacao_marcas_final.json`, `triagem_quantidade_faixa.json`, `geometrias_bloqueadas_triagem.json`, `notas_armaduras_localizadas_furos.json`, cobertura da tabela.

Correções são reaplicadas por prancha/proximidade da chamada após mudanças de IDs. A triagem compara quantidade impressa com extensão/espaçamento: sete alertas atuais, com gatilho heurístico de 16%, sem significado normativo. Duas geometrias foram bloqueadas para conciliação, sem declarar erro do projetista.

Há dependências de preparação circulares: leitura de tabela também lê ocorrências já existentes. A sequência de primeira execução e os ajustes não estão encapsulados em runner.

### 3.5 Partição e cálculo

**Entradas:** PDFs, inventário e ocorrências consolidadas. **Ferramenta:** `calculate.py:calc`.

**Saídas:** `regioes_capacidades.json`, `proveniencia_calculos.json`; auditoria auxiliar em `auditoria_equilibrio.json`.

Partição por composição/concreto/h/camada, com 1.049 células, 438 configurações únicas, 319 composições pendentes e 73 hipóteses verticais de envelope de 20 mm. Polígonos especiais foram definidos localmente, não por associação universal com formas.

O motor pode lançar exceção ou devolver momento nulo; o wrapper retira capacidade publicada sem escoamento real ou com composição ambígua. Não há captura geral por ocorrência, transação de execução ou manifesto imutável.

### 3.6 PDFs resistentes

**Entradas:** R, ocorrências, fontes e proveniência. **Ferramentas:** `build_report.py`, `build_eight_sheets.py`.

**Saídas:** `output/pdf/ATP_S07_lajes_terreo_mapa_preliminar.pdf` (98 páginas) e oito `output/pdf/pranchas_regioes/ATP_S07_730x_regioes_As_Mrk.pdf`.

As fontes recebem polígonos, configuração, As/m e Mrk. Após a ocorrência R031/R034, rótulos passaram a poder ultrapassar a região, sem colisão entre caixas e com chamadas. A revisão de layout não alterou as resistências.

### 3.7 DXFs e alinhamento

**Entradas:** `ARP0002.DXF` e `ARPV0002.DXF`, na pasta TÉRREO. **Ferramentas:** parser local por pares código/valor, comandos de ajuste e `V/preparar_vertical.py`.

**Saídas H/V:** `inventario.json`, `entidades.json`, `textos.json`, `componentes_negativos.json`, `calibracao_amplitude.json`, `regioes_negativas_geometria.json`, `alinhamento_pdf.json`.

Não foi usada API TQS/modelo original. O alinhamento foi comprovado por 409 vértices de apoio na parte superior e 171 na inferior. Transformações e pares estão arquivados; são escalas por eixo e translação, não registro geral com rotação/cisalhamento arbitrários.

### 3.8 Comparação e evolução do critério

1. Mapa inicial: média gráfica ponderada pela extensão dos segmentos.
2. Comparativo histórico: máximo local, com tratamento de apoios poligonais; 117 células sinalizadas nesse critério.
3. Estado final autorizado: média aritmética dos picos por linha dentro de cada faixa R, sem exclusão de apoios e sem criar regiões oficiais a partir de MN/MNV.

**Ferramentas finais:** `H/V/gerar_pranchas_comparacao_media.py`. **Saídas:** `comparacao_media_faixas.json/.csv` e PDFs `ATP_S07_7303/7307/7304/7308_faixas_Mrk_Msol_media.pdf`.

Somente células sem `issues` e com momento publicado entram nos PDFs finais, por orientação de João. Omissão do cálculo não significa inexistência da armadura.

### 3.9 Cobertura posterior

Triagem de negativos fora das faixas e recortes visuais: P790/PC45C na 7307; N26 omitida e N28/N31 inclinadas na 7308. Os comandos não foram integralmente persistidos como ferramenta; JSONs e imagens são conferências locais, não um verificador geral de ausência de armadura.

## 4. Interpretação do detalhamento

### 4.1 Marca, ocorrência, região e mancha

- **Marca N:** posição de tabela, que pode reaparecer e não é identidade física universal entre pranchas.
- **Ocorrência O:** chamada localizada, com caixa PDF e geometria candidata.
- **Região R:** célula da partição por composição/seção/material/camada. “Oficial”, nos últimos PDFs, significa referência de comparação adotada na rodada, não região emitida pelo projetista.
- **Mancha MN/MNV:** agrupamento gráfico de sinal negativo. É auxiliar e não define novas faixas de armadura.

IDs R são atribuídos após ordenação geométrica. Outra extração/partição pode renumerá-los; identidade estável entre versões não está implementada.

### 4.2 Regiões de atuação

A direção e extensão gráfica da barra são combinadas com o eixo perpendicular de distribuição e seu círculo. Isso produz a envoltória nominal. Comprimento total C, ganchos, projeção reta e comprimento eficaz de ancoragem não são intercambiáveis.

Interseções/diferenças Shapely criam células de famílias constantes, subdivididas por h/fck. Existem filtros de área e operações `buffer` pequenas para união; são heurísticas dependentes de escala, não controles normativos.

A tentativa de recortar aberturas em `calculate.py` procura pares de diagonais na camada PDF 1. Na conferência de PC45C, a abertura efetiva foi localizada na camada 2. Portanto, **a exclusão de aberturas não está demonstrada como completa**. Não exigir armadura dentro de um vazio por falha de extração.

### 4.3 Base e reforço positivo

No código, base corresponde à família `(8,14)`, face positiva e h=20 cm, conforme orientação específica do S07. `base_lap_count` registra ocorrências sobrepostas, mas a família base entra uma só vez na composição.

Demais famílias reconhecidas são reforços nas interseções correspondentes. Não existe classificador universal de BASE/REFORÇO por semântica de chamada. A distinção mistura convenção documental e orientação do engenheiro.

### 4.4 Intercalação na mesma camada

João confirmou reforços positivos intercalados com a base, sem camada acima dela. Cada família mantém As/m e centro próprio a φ/2 do interior do cobrimento. Sua representação equivalente conserva resultante e centro, evitando tratar as famílias intercaladas como camadas sobrepostas.

Isso não verifica espaçamento livre, alinhamento real dos centros, cabimento e interferências com a direção ortogonal. O agregado máximo de 16 mm pertence ao contexto, mas não foi aplicado em um controle automatizado de espaçamento neste fluxo.

### 4.5 Traspasses e sobreposições

Tratamento implementado:

1. Deduplicação de ocorrências exatas com mesma marca, φ, s e geometria arredondada.
2. Base Ø8 c/14 repetida não duplica a contribuição.
3. Mesma marca/família repetida dentro da célula não é somada novamente.
4. Famílias iguais com marcas distintas podem receber ambiguidade.
5. Nas negativas, múltiplos grupos distintos em sobreposição recebem capacidades individuais; soma publicada fica pendente de composição/ancoragem.

**Isso não é reconhecimento automático de traspasse nem verificação de emenda.** Não está implementada prova geral de identidade física da barra ou simultaneidade de grupos. A união espacial de células compatíveis pode reunir marcas diferentes sem somar suas taxas: não inferir reforço adicional pela lista de marcas.

### 4.6 Espessuras e materiais

`calculate.py` usa polígonos especiais definidos por coordenadas PDF:

| Região delimitada no caso | h usado |
|---|---:|
| Laje principal remanescente | 20 cm |
| L2/L3/L6/L7 | 15 cm |
| L4/L5 | 20 cm |
| LF701–LF704 | 30 cm |
| LT701–LT704 e zona superior ainda a conciliar | 12 cm |

Os interiores especiais foram definidos sobretudo na parte 1. O remanescente recebe `L1/L8 - localizar no mapa` ou `L9`; isso não individualiza automaticamente cada laje da forma.

O preenchimento verde da camada 12 foi usado como C35 e o remanescente da faixa como C40, conforme a legenda lida. **A cor foi usada para material neste caso**, sem provar identidade física de barras. Essa convenção não deve ser transportada a outro projeto sem conferir a legenda.

## 5. Cálculo resistente

### 5.1 Integração efetiva com o Concretopy

`calculate.py:calc(fams,h,fck,offset)` usa `Barra`, `Aco`, `Concreto`, `SecaoRetangular`, `CamadaArmaduraLongitudinal` e `verificar_flexao_viga_retangular`.

A chamada passa uma camada equivalente com d explícito e:

- γc=1,4; γs=1,15; γf=1,4.
- `verificar_armadura_minima=False`.
- Aço de referência CA50 para a seção equivalente.
- Seção retangular de largura normalizada.

Não foi chamado um verificador completo de placas/lajes. O modelo de flexão retangular foi aplicado a uma faixa equivalente.

### 5.2 Área de aço

Com φ em mm e s em cm:

`Aφ = π·(φ/10)²/4 [cm²]`  
`As,i = Aφ·100/s [cm²/m]`.

Somam-se famílias cuja composição foi admitida, respeitando não duplicações. Valores numéricos internos de uma composição pendente não autorizam publicar resistência composta.

### 5.3 Altura útil

Com h, cobrimento e offset em cm:

`d_i = h − 3,0 − offset − φ_i/20`.

- H: `offset=0`, primeira camada.
- V: maior diâmetro horizontal intersectante convertido de mm para cm.
- Sem envelope horizontal mapeado: `offset=2,0 cm`, hipótese `HYPOTHESIS_20MM_HORIZONTAL_ENVELOPE_NO_LOCAL_MAPPING`.

O envelope vem da interseção com faixas do detalhamento horizontal correspondente. Não é reconstrução tridimensional de todos os contatos.

A seção é parametrizada como `SecaoRetangular(width,h,2.5,5)`: 2,5 cm mais o argumento numérico de 5 mm mantém 3 cm internos no modelo. **Não se adotaram estribos físicos nas lajes.** O d explícito governa a camada; o empilhamento automático do motor não foi usado para essas famílias.

### 5.4 Diferentes diâmetros e classes

O código atribui fyk=600 MPa a φ=5 mm e 500 MPa aos demais. É uma regra da entrada deste caso, a conferir no projeto, não prescrição universal.

Definindo pesos `W_i = As,i·fyd,i`:

`As,eq = Σ(As,i·fyd,i)/fyd,CA50`  
`d_eq = Σ(W_i·d_i)/ΣW_i`.

A equivalência conserva resultante e centro, condicionada ao escoamento das famílias reais. Não demonstra compatibilidade em qualquer situação arbitrária.

Para atender ao número inteiro de barras da interface:

`n = max(20, ceil(As,eq/Abarra_ref))`  
`b* = n·Abarra_ref·100/As,eq [cm]`.

Escolhe-se uma barra de referência, calcula-se a seção com largura b* e renormaliza-se a resposta para um metro. n não é quantidade executiva e b* não cria nova faixa oficial.

### 5.5 Modelo, unidades e saída

O motor consultado usa bloco retangular e camadas tracionadas escoadas. Geometria em cm, tensões em MPa, retorno `mrd_kncm` em kN·cm. Inclui linha neutra, x/d, deformações, diagnósticos e campos de ductilidade.

`MRd [tf·m/m] = mrd_kncm·(100/b*)/980,665`  
`Mrk [tf·m/m] = MRd/1,4`.

Mrk é o rótulo solicitado para **resistência equivalente de comparação**, não resistência característica calculada retirando γc/γs. Solicitação já característica não sofre nova divisão por γf.

O wrapper confere o escoamento das famílias reais com a linha neutra/deformação retornadas. Sem essa condição, anula MRd/M equivalente publicados. Nas composições ambíguas, também anula esses campos, embora o resultado bruto possa conservar cálculo candidato. **Não usar esse número bruto para contornar uma pendência.**

A execução registrou escoamento real atendido nas 1.049 células; isso não valida identificação/geometria de entrada. Mínimos foram desativados e ductilidade não foi convertida em aprovação geral da laje.

## 6. Momentos solicitantes

### 6.1 Extração e origem

O parser local lê DXF ASCII por pares código/valor, separando ENTITIES e preservando tipo/camada/propriedades. Foram usados LINE, TEXT, POLYLINE, VERTEX, SEQEND e CIRCLE. Rótulos de momento são textos legíveis.

A legenda confirma `tfm/m`, direção e filtro 1,620. João corrigiu o filtro inicialmente informado de 1,85 para 1,62 e isocurva configurada 1,80; os rótulos da isocurva são 1,81. Ela não foi tratada como linha de momento zero.

A natureza característica foi confirmada para H e mantida para V no pedido de repetir o procedimento; não está explicitada no DXF. Não se recuperaram cargas, combinação/envoltória, redistribuições ou compatibilidade completa entre revisão do modelo e detalhe.

### 6.2 Sinal, componentes e amplitudes

As camadas 214/224 foram associadas às negativas por comparação com rótulos conhecidos. Seus números são convenção deste arquivo, não especificação universal de DXF.

Agruparam-se segmentos por extremidades coincidentes. H usa eixo Y e percurso X. V usa eixos canônicos `u=Y_DXF`, `v=−X_DXF`, retornando a X/Y reais na apresentação.

| Direção | Escala desenho/(tf·m/m) | Pares associados / usados | Maior desvio observado |
|---|---:|---:|---:|
| H | 1,2231103179874525 | 1.769 / 1.763 | 0,01812 tf·m/m |
| V | 1,2231341157888926 | 1.758 / 1.751 | 0,01949 tf·m/m |

Pares excluídos do ajuste não estão automaticamente resolvidos. Calibração comprova escala no conjunto conferido, não exatidão do modelo ou de todos os eixos.

Em V, onze componentes tiveram eixos locais corrigidos por textos/vértices e geometria estrutural ou estimativa do rótulo. `auditoria_eixos_locais.json` registra 1.309 componentes associados a rótulos e nenhuma correção efetivamente usada pela via alternativa de eixo vizinho inferido. Essa via existe no código, mas não tem uso validado demonstrado no caso.

A preparação H arquivada usa referência regular de malha. A conferência posterior revelou trechos locais próximos de Y=10957 fora desse arredondamento. Não foi localizada reauditoria H persistida equivalente à correção V. Não afirmar que todos os eixos H foram corrigidos.

### 6.3 Valores sem rótulo e filtro

João autorizou usar 1,61 quando faltasse magnitude ou recuperar a amplitude. Como o traçado preservou amplitudes, inclusive abaixo de 1,62, a substituição não foi necessária: os resultados registram `assumed_1_61_count=0`.

Sem rótulo não significa zero. O procedimento não recupera traçado completamente suprimido nem cria amostra nula para onde não existe informação.

### 6.4 Coordenadas e associação com as faixas

Transformações arquivadas:

`x_pdf = sx·X_DXF + tx`  
`y_pdf = sy·Y_DXF + ty`.

O sinal de sy acomoda a origem superior esquerda do PDF. Os polígonos R são levados ao DXF e, em V, ao sistema canônico para o recorte.

`H/V/alinhamento_pdf.json` guarda parâmetros e pares. Foram conferidos 409/171 vértices por parte, com resíduos finais da ordem de 0,08–0,09 ponto PDF, abaixo de 0,12. Isso comprova registro gráfico dos apoios associados, não todos os limites de faixas/vazios.

Não foram carregados IDs de nós/barras TQS, conectividade, áreas tributárias ou vínculos. A “linha” da média é do diagrama exportado, não uma entidade de grelha com identidade estrutural comprovada.

### 6.5 Critério atualmente implementado — definição precisa

**A média executada é a média aritmética dos picos por linha dentro da faixa R. Não é a média aritmética de todos os valores disponíveis da região.** A expressão “média dos valores da região” deve ser qualificada desse modo para documentar fielmente o código.

Para cada R:

1. Projetar cada segmento negativo no eixo físico da sua linha.
2. Intersectá-lo com o polígono R.
3. Recuperar o momento nos extremos do trecho recortado por interpolação linear das amplitudes originais.
4. Tomar o maior módulo negativo dentro de R para a linha: `p_l = max |Mk|`.
5. Vários trechos/componentes na mesma coordenada de eixo contribuem uma só vez, com o maior pico.
6. Calcular `Msol,R = Σ p_l / N_R`.

Não há ponderação por área/comprimento/nós/aço. Linhas parcialmente contidas participam somente pelo trecho interno. Linhas sem trecho negativo associado não entram como zero. **Apoios não são excluídos da média final**; essa exclusão pertencia ao comparativo histórico por máximo.

Se N=0, Msol e η ficam nulos e aparecem como `--`, não como atendimento. Limiares numéricos de segmento/amplitude são heurísticas de processamento, não limites normativos.

### 6.6 Médias distintas e evolução

- O mapa inicial usou média ponderada pela extensão dos segmentos.
- O mapa MN/MNV posterior usa média dos picos por linha na mancha auxiliar.
- O PDF final recalcula a média dos picos por linha dentro da faixa R.
- A média dos textos rotulados é outra coluna auxiliar, enviesada pelo filtro.

As médias podem diferir legitimamente, pois populações e recortes não são iguais. MN/MNV não geram regiões oficiais dos últimos PDFs.

### 6.7 Limitações do critério

A média reduz o peso dos picos, mas não prova redistribuição, equilíbrio de faixas, ductilidade, largura colaborante ou suficiência local. Refinamento/espaçamento das linhas influencia a média não ponderada; excluir linhas sem negativo altera sua população.

O critério foi autorizado por João para esta rodada, com limitações reconhecidas. Não se implementou aceitação normativa geral que substitua máximos locais pela média. Se a futura skill usar a média de **todas** as amostras da região, isso será alteração funcional/metodológica a definir depois, não o estado atual.

## 7. Resultados e visualização

### 7.1 Dados produzidos

| Arquivo | Conteúdo |
|---|---|
| `A/inventario.json` | Prancha/fontes, páginas, dimensões e hashes. |
| `A/ocorrencias_extraidas.json` | Chamadas O, textos, φ/s, As individual, caixa, orientação e geometria candidata. |
| `A/regioes_capacidades.json` | R em GeoJSON PDF; face/direção, laje, h/fck, famílias, ocorrências, offset/hipótese, pendências, capacidades individuais e resposta Concretopy bruta/normalizada. |
| `A/proveniencia_calculos.json` | Interface/caminho/hash do motor, parâmetros, 1.049 células e 438 configurações. |
| `H/V/entidades.json`, `textos.json` | Dados extraídos dos DXFs. |
| `H/V/componentes_negativos.json` | Componentes, segmentos e eixo/base; V em coordenadas canônicas. |
| `H/V/regioes_negativas_*resultados.json` | Manchas auxiliares, geometrias e médias/picos de cada geração. |
| `H/V/comparacao_media_faixas.json` | R, As, Mrk, Msol, n_linhas, picos individuais, η e estado; V também preserva offset/hipótese. |
| `H/V/comparacao_media_faixas.csv` | Resumo da comparação por R. |
| Manifestos/validações | Páginas, códigos, posicionamento dos rótulos, exclusões e integridade conforme cada rodada. |

Não existe schema formal versionado ou dataclass de domínio própria. Alguns nomes são herdados: nos mapas de média de picos, `weighted_sum`/`length` representam soma de picos/contagem de linhas.

### 7.2 Índice de utilização

`η = Msol,médio / Mrk = Msol,médio / (MRd/1,4)`.

Os PDFs mostram módulos; os picos individuais no JSON mantêm sinal negativo. Classificação com valores completos, antes do arredondamento:

- `MEDIA_SUPERA_RESISTENCIA`: Msol > Mrk;
- `MEDIA_NAO_SUPERA_RESISTENCIA`: Msol ≤ Mrk;
- `SEM_DEMANDA_ASSOCIADA`: sem amostra negativa associada dentro da R.

Não há banda geral de incerteza no classificador final. Valores arredondados iguais podem ter cores diferentes. O tratamento de limiar gráfico do comparativo histórico por máximos não foi incorporado automaticamente à média final.

Verde significa apenas média não superior à capacidade nominal no critério escolhido, não aprovação da laje. `issues` ou momento não publicado impedem inclusão no PDF final.

### 7.3 Contagens finais arquivadas

| Prancha | R publicadas | Média supera | Não supera | Sem demanda | R omitidas |
|---|---:|---:|---:|---:|---:|
| 7303 — negativa H | 147 | 20 | 96 | 31 | 102 |
| 7307 — negativa H | 59 | 19 | 38 | 2 | 50 |
| 7304 — negativa V | 125 | 36 | 72 | 17 | 83 |
| 7308 — negativa V | 52 | 14 | 28 | 10 | 78 |

São contagens do banco produzido, não quantidade de falhas/apoios independentes. N26 omitida e inclinadas não conciliadas impedem considerar o quadro da 7308 um inventário integral revisado.

### 7.4 Construção do PDF

A prancha original é incorporada como vetor, acrescentando cabeçalho e painel lateral. ReportLab produz polígonos/cores/configuração/As/Mrk/Msol/n/η; PyMuPDF combina e salva as páginas.

Caixas podem ultrapassar a R; posições radiais são buscadas evitando colisão entre rótulos, com chamadas quando necessário. Essa verificação não prova que nenhum conteúdo importante da fonte ficou oculto: renderização e leitura visual continuam necessárias.

**Arquivos finais, em `A/output/pdf/pranchas_regioes`:**

- `ATP_S07_7301_regioes_As_Mrk.pdf` até `ATP_S07_7308_regioes_As_Mrk.pdf` — oito mapas resistentes.
- `ATP_S07_7303_faixas_Mrk_Msol_media.pdf`.
- `ATP_S07_7307_faixas_Mrk_Msol_media.pdf`.
- `ATP_S07_7304_faixas_Mrk_Msol_media.pdf`.
- `ATP_S07_7308_faixas_Mrk_Msol_media.pdf`.

Em V, `Mrk*` conserva o envelope horizontal provisório de 20 mm: dez faixas publicadas da 7304 e seis da 7308. A estrela não converte hipótese em dado comprovado.

## 8. Validações realizadas

### 8.1 Conferências manuais/locais com evidência

| Conferência | Registro | Alcance |
|---|---|---|
| Espaçamentos, marcas e caixas específicos | `conferencias_visuais_locais*.json`, recortes e conciliações | Correções locais; não certificação das 747 ocorrências. |
| N16/N18 em P728/PC2C | `sobreposicao_N16_N18.png` e orientação de João | Manter capacidades individuais e soma pendente; ancoragem não validada. |
| R031/R034 da 7301 | Dados e imagens do layout | Falta era de rótulo completo, não de cálculo; permitiu-se caixa fora do polígono. |
| P701, P785, PC40C, P740/P746 | Recortes do comparativo histórico | Conferência de chamadas e posição de pontos; não fechamento de seção/nó. |
| Lacunas 7307 | `H/7307_conferencia_lacunas.json` | P790: intervalo nominal ≈40 cm entre N29/N30. PC45C: trecho acima da abertura, largura ≈66 cm. Participação de blocos pendente. |
| Vazios aparentes 7308 | `V/7308_conferencia_cobertura.json` e imagem | N26 existe e foi omitida do levantamento; N28/N31 inclinadas exigem conciliação. Não confirmou ausência física nos principais vazios. |

Não foi localizado memorial independente de cálculo manual completo de resistência de cada configuração. Conferência manual de leitura e soma aritmética não equivalem a validação resistente independente.

### 8.2 Conferências aritméticas explicitadas na conversa

| Caso | População | Valores arquivados |
|---|---|---|
| 7303-R107, N12 Ø10 c/15 | 10 picos por linha dentro da faixa | Soma dos módulos 27,359593; média 2,735959 tf·m/m; Mrk 2,658220; η=1,029245. |
| 7308-R105, N20 Ø12,5 c/13 | 18 picos por linha dentro da faixa | Soma 83,972015; média 4,665112 tf·m/m; Mrk 4,232834; η=1,102125. |
| Mancha MN214 | 15 picos por linha na mancha | Média 3,110458 tf·m/m. A antiga média ponderada dos segmentos era 1,382647 e a média só dos 16 rótulos, 3,305625. |

Demonstram a população e o cálculo das médias nesses casos, não a correção universal das faixas/eixos. MN214 e R214 não são a mesma identidade.

### 8.3 Verificações automatizadas registradas

- `auditoria_equilibrio.json`: 1.049 células, diferença relativa máxima registrada ≈`7,43×10⁻16`, escoamento real verdadeiro. É conferência auxiliar numérica da mesma idealização, não análise física independente de laje.
- `validacao_pdf.json`: 98 páginas, lista de textos fora de página vazia, hash, fontes sem mudança registrada e folha de contato renderizada.
- `validacao_oito_pranchas.json`/manifesto: oito folhas, códigos presentes e ausência de colisão entre caixas. Alguns nomes de contadores são herdados da antiga regra de rótulo dentro da região.
- `H/validacao_pranchas_media.json`: 147/59 rótulos, exclusão de 102/50 células, preservação das capacidades publicadas, sem colisões.
- `V/validacao_pranchas_media.json`: 125/52 rótulos, exclusões 83/78, indicação das 10/6 hipóteses, sem colisões e fonte resistente preservada.
- Calibração de amplitudes, ajuste de alinhamento e somas de picos individuais, com resíduos/dados arquivados.
- Hashes de fontes e do banco resistente foram conferidos durante as gerações; nem todo comando dessas auditorias foi preservado como teste executável.

**Não foi identificada suíte `unittest`/`pytest` própria dos scripts S07.** Asserções em geradores e JSONs de auditoria não equivalem a testes unitários/integração/regressão com referência independente. A existência dos testes de `tools/slab_geometry_poc` não comprova execução ou integração com este fluxo.

### 8.4 Casos reais analisados

- Oito detalhamentos e duas formas do mesmo ATP.
- 747 candidatas; 662 com espaçamento; 647 com retângulo/espaçamento; 15 distribuídas sem retângulo resolvido.
- 1.049 células: 121/119/249/208/51/62/109/130 nas pranchas 7301–7308.
- Dois DXFs da mesma família de exportação.
- Quatro PDFs finais de negativas pela média, limitados ao banco disponível.

Não houve demonstração em múltiplos empreendimentos, outros emissores de DXF ou famílias gráficas diferentes.

### 8.5 Comportamentos não validados

Reconhecimento exaustivo de chamadas e aberturas; barras inclinadas/curvas/localizadas arbitrárias; identidade de emendas; ancoragem; camadas em todos os encontros; L1/L8 integral; DXFs com blocos aninhados/outras entidades/unidades; eixos locais H em geral; validade estrutural da média em substituição a máximos; completude de cobertura em exportação filtrada.

## 9. Limitações e pendências

### 9.1 Falhas de interpretação demonstradas

1. **N26/7308:** a fonte mostra 38 Ø12,5 c/11, C=618 em PC51C, sem incorporação ao levantamento anterior. Não houve revisão completa posterior do banco/PDF incorporando-a. Corrigir antes de considerar o inventário integral.
2. **N28/N31 inclinadas:** geometria de faixa e contribuição na direção vertical pendentes. Presença na fonte não prova suficiência; ausência de polígono não prova falta de aço.
3. **Abertura em outra camada:** a regra automática de diagonais na camada 1 não capturou a abertura de PC45C na camada 2. Cobertura de aberturas permanece incompleta.
4. **Tabela e geometrias bloqueadas:** itens sem associação podem ser falha do assistente. Não atribuir automaticamente ausência de informação/armadura ao projetista.

### 9.2 Pendências de engenharia

- Base/reforço intercalados seguem orientação, sem verificação geral de distribuição física.
- Maior φ horizontal intersectante/envelope 20 mm são aproximações de camada.
- h/fck dependem de coordenadas/legendas específicas; blocos, bordas e etapas não foram verificados como conjunto resistente completo.
- Sobreposição não comprova reforço/emenda; a envoltória nominal não desconta falta de ancoragem.
- DXFs não comprovam combinação, revisão e simultaneidade entre direções.
- A média pode ocultar demanda localizada; sua adoção foi decisão desta rodada.
- Os apontamentos 7307 dependem também de armaduras dos blocos/encontros; não provam ausência de todo aço existente.

### 9.3 Reprodutibilidade e manutenção

- Caminhos, pranchas, tabelas, camadas, coordenadas e limiares fixos.
- Preparação DXF/alinhamento parcialmente por comandos locais; intermediários são requisitos de execução.
- Ausência de schema versionado, validação geral de entradas e manifesto imutável por execução.
- IDs podem mudar; correções por proximidade não são identidade física robusta.
- Reexecução sobrescreve nomes estáveis e pode perder ajustes; não há transação de ponta a ponta.
- O Git consultado mostra `analises/atp_s07_lajes_terreo/` como **não rastreada**. Os arquivos existem, mas não há histórico de commits desse fluxo nesse estado.
- Versões completas de bibliotecas/fontes/ambiente não foram congeladas.

### 9.4 Inconsistências documentais encontradas nesta auditoria

**Documentadas, sem correção de código/dados nesta tarefa:**

- `H/LEITURA_DO_MAPA.md` descreve o primeiro mapa ponderado, não o método de todos os produtos posteriores.
- O campo `method` do JSON de manchas verticais ainda menciona coordenada Y do eixo. `line_peaks` usa corretamente `x_DXF`; o texto de metadado ficou desatualizado.
- O CSV de resumo das manchas em `V/gerar_mapa_media_picos.py` tem colunas `centro_x_DXF`/`centro_y_DXF`, mas escreve centroides dos polígonos canônicos. Não são X/Y reais. O JSON guarda `actual_DXF_geometry` e a figura aplica `cxy`; não concluir que toda a imagem esteja girada, mas não usar os centros desse CSV sem transformação.
- Asserção de ausência de um ID MN específico no PDF é controle estreito. A seleção efetiva de R e inspeção geométrica são evidências mais relevantes do que esse teste isolado.

### 9.5 Decisões do engenheiro

Permanecem decisões de João: documentos vigentes; seção especial; participação de armaduras de etapa; natureza física de sobreposição; ancoragem; contribuição de inclinadas; faixa de redistribuição; origem/natureza da demanda; definição e aceitação da média; materiais ausentes e conclusão do ATP.

Hipótese usada para prosseguir deve permanecer identificada. Execução em um caso não transforma a solução em regra universal.

## 10. Recomendações para formalização da skill

Esta seção contém **propostas**, não funcionalidades ou arquivos implementados nesta tarefa.

### 10.1 O que deve ficar no SKILL.md

1. Gatilho e escopo: revisão assistida de distribuídas de laje, interpretação e comparação no escopo autorizado.
2. Limites de conclusão: identidade física/cobertura, h/fck/c/camada e origem da demanda precisam estar explicitados ou permanecer pendentes.
3. Separação entre ocorrência, faixa de armadura e mancha de momento; regiões auxiliares não criam faixas oficiais.
4. Ordem de trabalho: inventário/contexto → leitura/conciliação → faixa/seção/camada → composição → Concretopy → origem/alinhamento da demanda → agregação escolhida → η/relatório.
5. Não somar traspasses/sobreposições sem evidência; não transformar ausência de cálculo/mapeamento em ausência física.
6. Referenciar `profile/force-presentation.md`, sem duplicar toda regra de unidade/natureza; conservar MRd e a distinção equivalente.
7. Rastreabilidade, evidência de validação e estado parcial explícitos; resultado parcial não aprova laje.
8. Encaminhar detalhes às referências; não fixar parâmetros do S07 como requisitos gerais.

O nome da nova skill ainda deve ser definido. Não existe uma skill pronta de lajes criada por esta conversa.

### 10.2 Referências recomendadas

| Tema de referência futura | Conteúdo |
|---|---|
| Interpretação documental | Marca/O/R, barra/círculo/eixo, envoltória e exemplos ambíguos. |
| Composições e traspasses | Base/reforço intercalados, deduplicação, identidade física e bloqueios de soma. |
| Seções/camadas | Origem h/fck/c, d explícito, envelope ortogonal e hipóteses. |
| Adaptador Concretopy | Equações/unidades, resultante equivalente, largura normalizada, escoamento e Mrk. |
| DXF | Convenções de exportação, sinal, calibração, eixos locais, natureza e alinhamento. |
| Agregação de demanda | Média de amostras × média ponderada × média de picos por linha; população/recorte/limitações. |
| Resultados e visualização | Schema, null/--, η, omissões, cores e limites de conclusão. |
| Validação e regressões | Evidências S07, N26 omitida, abertura em outra camada, inclinadas, R107/R105. |

São temas propostos, não caminhos/arquivos existentes. Casos ATP devem permanecer evidência de projeto/teste, sem universalizar suas decisões.

### 10.3 O que deve permanecer em Python

Leitura de PDF/DXF; geometria/interseções/partições; As/d; chamada e proveniência Concretopy; calibração/alinhamento; recorte de diagramas; cálculo de picos/médias/η; geração e conferência de PDFs.

Em tarefa futura, antes de classificá-los como reutilizáveis:

- separar importação de execução com efeitos laterais;
- parametrizar fontes/layouts/eixos sem esconder decisões;
- preservar dados brutos e revisões/correções versionadas;
- consolidar o parser/alinhamento hoje executados por comandos locais;
- criar contratos de dados e origem de parâmetros;
- nomear distintamente cada política de agregação;
- corrigir/revalidar N26, inclinadas, aberturas e metadados antes de congelar referências;
- avaliar compatibilidade com `tools/slab_geometry_poc`, sem transferir automaticamente sua validação.

### 10.4 O que não deve virar decisão silenciosa do código

Documento vigente; seção física; participação de etapas/blocos; significado de sobreposição; ancoragem; contribuição de barras inclinadas; distribuição/redistribuição de esforços; definição e aceitação da média; conclusão técnica.

### 10.5 Evidências propostas para futura validação

Testes sintéticos de As/composição/deduplicação/d; regressão documental com inventário independente revisado; pares de calibração e eixos locais; transformação de ida/volta; linha parcialmente contida; uma contribuição por linha; ausência de amostra distinta de zero; preservação de pendências; rótulos sem colisão; comparação independente de seções selecionadas; e casos negativos de omissão/abertura/inclinada.

Esses testes ainda não constituem uma suíte implementada S07. O estado atual documenta um procedimento assistido com rastreabilidade parcial, não um verificador automático geral validado de lajes.

## Evidências prioritárias para consulta

- `A/README.md`, `cobertura.json`, `proveniencia_calculos.json`, `auditoria_equilibrio.json`.
- `A/decode.py`, `read_tables.py`, `regions_extract.py`, `consolidate.py`, `calculate.py`.
- `A/build_report.py`, `build_eight_sheets.py`.
- `H/gerar_pranchas_comparacao_media.py`, `comparacao_media_faixas.json`, `calibracao_amplitude.json`, `alinhamento_pdf.json`.
- `V/preparar_vertical.py`, `gerar_pranchas_comparacao_media.py`, `comparacao_media_faixas.json`, `auditoria_eixos_locais.json`.
- `H/7307_conferencia_lacunas.json`; `V/7308_conferencia_cobertura.json`.
- `H/V/validacao_pranchas_media.json`; renderizações em `A/tmp/pdfs`.
- `CP/concretopy/verificacoes/flexao.py`; `REPO/tools/slab_geometry_poc/README.md`.

**Encerramento desta tarefa:** somente documentação. Nenhuma skill, motor, cálculo ou funcionalidade nova foi implementada; os artefatos anteriores foram preservados.
