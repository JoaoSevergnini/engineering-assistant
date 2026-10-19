# Prova de conceito: geometria de armadura de laje

## Experimento original N26

Experimento isolado, sem verificações resistentes. Entrada: uma prancha vetorial;
seleção humana fixa de uma ocorrência N26. Não é uma skill nem um extrator geral.

Depende de PyMuPDF. Nesta execução foi reutilizada a instalação existente em
`tmp/pdf_deps` (1.19.6); nenhuma biblioteca foi instalada. O runner também aceita
uma instalação acessível no ambiente Python. A API vetorial pode variar entre versões:
revalidar a extração e as imagens quando o motor mudar.

Na raiz do repositório, em PowerShell:

```powershell
python tools/slab_geometry_poc/run_case.py 'C:/Users/João Severgnini/Desktop/LAJES SIMON_RH - PAV TIPO/LAJES/RMP-EST-LO-1422-LAJ-R00.PDF'
python -m unittest discover -s tools/slab_geometry_poc -v
```

`geometry.py`: extração de textos/caminhos, parser local, reconhecimento limitado
de setas e enumeração das associações. Coordenadas em pontos PDF, origem superior
esquerda, y crescente para baixo. Somente barra horizontal reta e eixo vertical.
Cor, expressões BASE/REFORÇO e ordem dos caminhos não decidem a associação.

`run_case.py`: seleção explícita N26; escala da planta 1:50; zona da linha da tabela
declarada após leitura visual dos cabeçalhos; reutilização de
`tools/beam_model/pdf_observations.extract_zones`; JSON bruto, JSON interpretado e
imagens PNG. Renderiza a composição em memória, sem salvar outro PDF.

`test_geometry.py`: testes sintéticos e replay do inventário vetorial real entregue.
O replay é uma regressão da interpretação; não prova a validade em outras pranchas.
Executar o runner antes dos testes se os artefatos reais não estiverem presentes.

Resultados e limitações: `analises/lajes_geometria_poc/relatorio.md`.

## Leitura automática da prancha

```powershell
python -B tools/slab_geometry_poc/run_sheet.py 'C:/Users/João Severgnini/Desktop/LAJES SIMON_RH - PAV TIPO/LAJES/RMP-EST-LO-1422-LAJ-R00.PDF' --validation analises/lajes_geometria_automatico/conferencia_visual_assistente.json
python -B -m unittest discover -s tools/slab_geometry_poc -v
```

Sem `--validation`, a leitura funciona normalmente e todas as revisões ficam
PENDING. O arquivo opcional é um registro separado de conferência, nunca uma
entrada para escolher geometrias ou alterar a classificação automática. Para a
revisão de João, copiar `validacao_manual_modelo.json` para outro nome, preencher
reviewer/method/status/selected_pair/notes e apontar essa cópia com `--validation`.
O hash do documento e os IDs das geometrias completas selecionadas são conferidos;
mudança incompatível causa erro em vez de reutilizar uma revisão silenciosamente.

`automatic.py` acrescenta inventário de chamadas, união cautelosa de continuações
textuais, multiplicidades impressas, fragmentos colineares, reconhecimento de eixos
e classificação por evidências. Reutiliza `geometry.arrow_wings` inclusive por
rotação de eixos horizontais. Não altera `geometry.associate`, o runner ou os testes
originais N26. `run_sheet.py` reutiliza `extract_page` e o leitor existente de tabela.

O recorte principal e a tabela são inferidos de âncoras textuais da família desta
prancha; não há seleção de marcas ou caixas por ocorrência. Outros layouts exigem
adaptação explícita de `detect_layout`; ausência das âncoras produz erro. Não se
promete reconhecimento universal de escritórios. O motor não usa cor, BASE,
REFORÇO, classe de aço, igualdade C/projeção ou ordem de caminhos como condição de
reconhecimento. Projeção maior que C em mais de 5% exige revisão por possível
contradição, sem declarar erro da prancha.

Saídas em `analises/lajes_geometria_automatico`: inventário com candidatos e
alternativas, extração bruta, CSV/Markdown, prancha anotada, ampliações de todas as
chamadas e modelo de revisão. Regiões são envoltórias gráficas, sem uso resistente.
O CSV usa separador `;` e UTF-8 com BOM. Os JSONs usam UTF-8.

`test_automatic.py` contém testes sintéticos. `test_automatic_real.py` contém replay
da prancha real, reextração do PDF quando disponível, invariância de cores/ordem e
compatibilidade exata da região N26. As contagens congeladas são regressões, não
inventário de referência independente nem evidência de taxa de acerto.

## Etapa 3: líderes e armaduras localizadas

```powershell
python -B tools/slab_geometry_poc/run_leaders.py 'C:/Users/João Severgnini/Desktop/LAJES SIMON_RH - PAV TIPO/LAJES/RMP-EST-LO-1422-LAJ-R00.PDF' --validation analises/lajes_geometria_lideres/conferencia_visual_assistente.json
python -B -m unittest discover -s tools/slab_geometry_poc -v
```

O novo runner reextrai a folha completa e compara todas as ocorrências com o
inventário da etapa 2, exigindo hash idêntico do PDF e mesmos IDs. Não sobrescreve
os resultados anteriores. Sem `--validation`, as novas associações ficam PENDING.
As conferências anteriores são transportadas somente para associações completas
cuja geometria permaneceu idêntica. Revisões anteriores de casos alterados ficam
em `prior_validation`, sem serem reaplicadas à nova geometria.

`leaders.py` reutiliza `read_sheet`, união de fragmentos, setas, marcadores,
interseção barra/eixo e envoltória. O grafo adicional conecta apenas extremidades
coincidentes dos segmentos brutos, seguindo cotovelos e pontas de seta ou marcador
circular. Cruzamentos interiores são registrados, sem mudança de trajetória.
Mais de um destino ou rota terminal, inclusive rota sem destino resolvido,
impede aceitação automática. Limites de exploração também bloqueiam aceitação.

Tipos de representação:

- `DISTRIBUTED`: barra e faixa com evidência suficiente; envoltória gráfica.
- `LOCALIZED`: barra ou traços paralelos diretamente visados; sem polígono imposto.
- `INCONCLUSIVE`: geometria ainda insuficiente ou ambígua.

Linhas localizadas próximas e com extremos iguais podem formar um conjunto gráfico.
Isso não conta barras físicas, não resolve o significado de 2x3/6x3 e não inclui
automaticamente grupos simétricos ou bordas opostas de aberturas. As entidades brutas
não são movidas: quando a ponta não coincide exatamente com a linha, são guardados
o ponto original e a interseção limitada da direção terminal com a candidata.
As tolerâncias experimentais ficam em `leader_criteria` no inventário.

Resultados: `analises/lajes_geometria_lideres`, incluindo relatório comparativo,
JSON com trajetórias/alternativas, tabela CSV/Markdown e 59 ampliações. Cores das
marcações são apenas apresentação; o leitor não consulta a cor do PDF.

Testes novos: `test_leaders.py` (sintéticos) e `test_leaders_real.py` (regressões da
folha real). Os testes das etapas anteriores continuam disponíveis e inalterados.

## Etapa 4: aberturas e grupos físicos localizados

```powershell
python -B tools/slab_geometry_poc/run_opening_groups.py 'C:/Users/João Severgnini/Desktop/LAJES SIMON_RH - PAV TIPO/LAJES/RMP-EST-LO-1422-LAJ-R00.PDF' --convention tools/slab_geometry_poc/conventions/sim_opening_edge_v1.json
python -B -m unittest discover -s tools/slab_geometry_poc -v
```

O runner consome o inventário da etapa 3, reextrai o PDF e exige igualdade das
entidades/coordenadas antes de usar os IDs existentes. Não reclassifica chamadas,
não reprocessa armaduras distribuídas e não sobrescreve entregas anteriores.
O enriquecimento fica em `localized_reconstruction`, no novo inventário, com
artefatos separados em `analises/lajes_grupos_fisicos`.

`opening_groups.py` usa `line_geometry` e os traços/líderes já associados. Propõe
contornos retangulares a partir de diagonais X, exige os quatro lados e pares de
reforços junto a pelo menos dois lados. Retângulo ou retângulo/X isolado é
inconclusivo. A seleção de abertura exige orientação, transposição dos extremos
e posição exterior junto à borda; não utiliza a menor distância. Linhas contínuas
podem atender mais de uma abertura alinhada sem duplicação de grupo.

A convenção é uma entrada explícita, com escritório, hash do PDF, regra e fontes:
`conventions/sim_opening_edge_v1.json`. A confirmação de João fundamenta os números
de barras/camadas; o detalhe da prancha fundamenta a convenção gráfica. Sem
`--convention`, sem fonte confirmada ou em outro documento/escritório, a distribuição
vertical permanece desconhecida. O perfil não é regra geral para outros projetos.

Para 2x3, o alvo indicado pelo líder pode ser ligado ao par da borda oposta somente
com evidência geométrica única e convenção aplicável. Não encontrar esse par não
cria um grupo fictício; a localização pendente é registrada. Em 6x3, a semântica
dos fatores e as camadas ficam desconhecidas. Os traços diretamente visados
permanecem registrados sem distribuir aritmeticamente as 18 barras.

Os IDs físicos usam posição + geometria, permitindo várias chamadas apontarem
para o mesmo grupo. A identidade vale para o layout desenhado, sem multiplicar
pavimentos TIPO 1 & 2. Um grupo não é um traço e não é uma chamada. A criação de
grupo sem líder direto exige também comprovação da borda oposta e a convenção.

`specific_overrides` do perfil admite evidência documental específica por
`occurrence_id`. Qualquer conflito bloqueia a aplicação da regra, guarda as duas
interpretações e exige revisão. Não se promete descoberta automática da semântica
de todo detalhe específico. `validation` permanece separado da inferência.

Saídas: aberturas/candidatas, representações localizadas, grupos físicos com origem
dos dados, CSV, tabela com links, mapa de aberturas, detalhe SIM e 15 ampliações.
Testes novos: `test_opening_groups.py` e `test_opening_groups_real.py`. Não há
verificações resistentes nem geometria 3D comprovada.
# Etapa 5: regiões e composição geométrica

`distributed_regions.py` reutiliza as envoltórias DISTRIBUTED sem modificar o
inventário anterior. Backend restrito a retângulos alinhados aos eixos, sem Shapely.
Não soma aço, não atribui lajes e não recorta aberturas. Mesma posição documental
não implica identidade física; fontes vetoriais idênticas permitem agrupar chamadas.

```powershell
python -B tools/slab_geometry_poc/run_regions.py --pdf 'C:/caminho/RMP-EST-LO-1422-LAJ-R00.PDF'
python -B -m unittest discover -s tools/slab_geometry_poc -p 'test_*.py'
```

Saída padrão: `analises/lajes_regioes_distribuidas`, com inventário enriquecido,
JSONs de regiões individuais/composições/identidades/interseções, mapas PNG e
`consulta.html` selecionável, independente de rede. Relatório distingue dados
extraídos, operações geométricas e pendências. N38 fica em controle documental
separado, preservando a chamada 6x3 e a confirmação de João de quatro grupos de três.

# Etapa 6: interpretação documental conservadora

```powershell
python -B tools/slab_geometry_poc/run_structural_regions.py
```

Entradas padrão: inventário da Etapa 5, entidades vetoriais/textuais da Etapa 3 e
`analises/lajes_interpretacao_estrutural/validacoes_engenheiro.json`. A saída fica
nessa última pasta, sem modificar etapas anteriores. Parâmetros `--inventory`,
`--entities`, `--reviews` e `--out` permitem outras entradas/destinos.

`structural_regions.py` extrai etiquetas de lajes/espessuras, investiga contornos
retangulares, gera propostas de interpretação e ensaia contenção de reforços
candidatos na união de bases candidatas. Propostas permanecem UNDETERMINED sem
confirmação. Contornos concorrentes não são resolvidos por proximidade.

Revisões manuais são vinculadas ao hash do documento e a `fingerprint(composition)`;
use o fingerprint exportado em `classificacoes.json` ao registrar uma revisão.
Campos: `fingerprint`, `source_sha256`, `classification`, `reviewer`, `source` e
escopo/notas. `reference_composition_id` serve apenas à navegação humana.
Uma revisão inválida/desatualizada não é aplicada e conflitos ficam pendentes.
As quatro revisões iniciais vêm da confirmação explícita de João na Etapa 6.

A consolidação preserva retângulos originais adjacentes e todas as referências.
Não significa autorização de uso resistente. Camadas e identidade física continuam
pendentes; não há áreas de aço, momentos, verificação normativa de emendas ou ATP.

# Etapa 7: relações com domínio válido e contornos poligonais

```powershell
python -m pip install --target tmp/slab_spatial_deps --only-binary=:all: -r tools/slab_geometry_poc/requirements-stage7.txt
python -B tools/slab_geometry_poc/run_relations.py
python -B -m unittest discover -s tools/slab_geometry_poc -p 'test_*.py'
```

Shapely 1.8.5.post1 foi testado isoladamente no Python 3.10/Windows de 32 bits deste
repositório; não modifica o Python global. Outras combinações de plataforma/Python
precisam de versão/wheel compatível e nova validação. As etapas anteriores continuam
sem essa dependência; os módulos/testes da Etapa 7 requerem a instalação indicada.

`occurrence_relations.py` constrói relações entre ocorrências, inclusive uma única
REINFORCES com múltiplas bases. `propagate` respeita domínio geométrico, membros
ativos, direção/camada e conflitos; não faz fechamento transitivo. `relation` permite
construir relações com evidências e estado explícitos; uma confirmação humana de
identidade física exige fonte específica. Nenhuma relação autoriza soma resistente.

`polygonal_slabs.py` usa faces planas, apoio de hachuras e conexões explícitas das
etiquetas, preservando alternativas. Uma face perimetral estreita/concava pode ficar
bloqueada para revisão, como L605. Não é leitor definitivo de planta de formas.

Entrada padrão: inventário da Etapa 6 e entidades da Etapa 3. Parâmetros
`--inventory`, `--entities`, `--out`. Saída: `analises/lajes_relacoes_contornos`, com
inventários, mapas separados, ampliações e comparação. As camadas anteriores,
confirmações locais e N38 ficam intactas. O relatório explicita limites de validade.

## Revisão independente dos contornos após a Etapa 7

```powershell
python -B tools/slab_geometry_poc/review_slab_contours.py
```

O experimento trata nome+espessura como bloco documental para recuperar os
apontadores de L611/L612 e consulta faces fechadas internas. Gera mapas e
`analises/lajes_revisao_contornos/revisao.json` sem substituir inventários anteriores.
Interseções de armaduras continuam preliminares; L603 fica pendente e L605 requer
revisão do contorno em U. Não altera o reconhecimento principal ou a partição.

## L603: contorno informado pelo engenheiro

```powershell
python -B tools/slab_geometry_poc/confirmed_slab_outline.py
```

Entrada manual: `analises/lajes_l603_confirmada/confirmacao_joao_L603.json`, com
traçado visual da imagem vermelha fornecida por João e âncoras no PDF. Registra
separadamente topologia confirmada e precisão métrica ainda aproximada. Produz
interseções e mapas nessa pasta, sem substituir as camadas automáticas anteriores
ou autorizar soma resistente. Margem de borda é exploratória e explicitamente
documentada. Não é uma reconstrução automática do contorno de L603.

## Etapa 8: contornos complexos sem coordenadas de referência no reconhecimento

```powershell
python -B tools/slab_geometry_poc/run_complex_contours.py
python -B -m unittest discover -s tools/slab_geometry_poc -p 'test_*.py'
```

Saída: `analises/lajes_contornos_complexos`. A função `recognize` de
`complex_slab_contours.py` usa somente entidades vetoriais, exclusões documentais
de armaduras/anotações e etiquetas de laje. Preserva entidades que atravessam a
janela textual (mínimo experimental de 80% dentro), em vez de descartar o segmento
inteiro. Não insere fechamentos, não usa fecho convexo para construir o perímetro
e não fixa nome, ID ou vértices de L603. Todos os resultados são candidatos.

`contour_validation.py` só compara candidatos já produzidos. A referência manual
é carregada pelo runner depois de salvar `candidatos_automaticos.json`, para
gerar métricas e imagens comparativas. Para executar sem referência em saída nova:

```powershell
python -B tools/slab_geometry_poc/run_complex_contours.py --skip-reference --out analises/lajes_contornos_sem_referencia
```

O relatório detalha o erro de recorte do contexto, a regressão das oito outras
lajes e as divergências locais da L603. A correspondência com a referência humana
aproximada não é validação automática, e não autoriza cálculos resistentes.

## Etapa 9: associação a domínios e espessuras documentais

```powershell
python -B tools/slab_geometry_poc/run_slab_assignment.py
python -B -m unittest discover -s tools/slab_geometry_poc -p 'test_slab_assignment.py'
```

Saída: `analises/lajes_associacao_espessuras`. `slab_assignment.py` particiona
polígonos distribuídos e traços localizados pelos contornos candidatos da Etapa 8.
Mantém parcelas descobertas e domínios concorrentes, com identidade da ocorrência
e referência ao quantitativo original, sem alocação ou soma de barras por laje.
As etiquetas documentais fornecem nome e espessura com proveniência. Contornos
candidatos produzem associações PROBABLE; RELIABLE exige domínio confirmado.
Parcelas sem domínio ou concorrentes ficam INDETERMINATE.

`confirmacoes_engenheiro.json` registra N14 como reforço em toda a ocorrência
e R053/N40 como traspasse, com escopo, origem humana, identidade e hashes.
O módulo não contém regras por marca; as camadas anteriores são preservadas.
O relatório distingue testes sintéticos de cruzamento entre espessuras e os
resultados reais, que não apresentaram ocorrência em múltiplos domínios candidatos.
Não calcula altura útil ou resistência.

## Etapa 9.1: confiança da associação separada da confiança do contorno

```powershell
python -B tools/slab_geometry_poc/run_refined_assignment.py
python -B -m unittest discover -s tools/slab_geometry_poc -p 'test_refined_assignment.py'
```

Saída: `analises/lajes_associacao_refinada`. Consome o inventário congelado da
Etapa 9 e acrescenta `refined_slab_assignment`, sem alterar qualquer camada
anterior. Associação RELIABLE exige etiqueta documental de nome/espessura e
suporte interior das entidades aceitas (barra e eixo, ou traços localizados).
Não exige contenção integral nem confirmação completa do contorno. A confiança
do contorno é registrada separadamente; RELIABLE não é validação humana.

Parcelas externas permanecem sem laje/espessura atribuída, com semântica
desconhecida, sem interpretação automática de ancoragem. As geometrias, os
quantitativos e as confirmações humanas são preservados integralmente. O mapa
destaca apenas ocorrências que ainda exigem decisão específica; o relatório
compara individualmente as 59 classificações. Não infere altura útil.

## Etapa 9.2: contextos documentais e espaciais independentes do contorno

```powershell
python -B tools/slab_geometry_poc/run_documentary_assignment.py
python -B -m unittest discover -s tools/slab_geometry_poc -p 'test_documentary_assignment.py'
```

Saída: `analises/lajes_associacao_documental`. Consome o inventário da Etapa 9.1
intacto e acrescenta `documentary_spatial_assignment`. Reutiliza os testes de
interseção barra/faixa e a partição existentes. `documentary_slab_context.py`
reconhece contextos auxiliares a partir de molduras em U com faces duplas e
apontador documental, ou de continuidade entre pares opostos de faces de apoio
com tampas vetoriais. Não altera os contornos nem utiliza IDs de lajes/marcas,
cores ou coordenadas de regressão como regras.

Os contextos servem à atribuição da laje/espessura, não à validação de domínios
estruturais. Um alerta topológico isolado não impede RELIABLE. Hipóteses
anteriores de barras e líderes são preservadas e avaliadas sem selecionar
silenciosamente uma delas; consenso sobre a laje é distinto da qualidade da
geometria de atuação. Concorrências de lajes/espessuras e rotas incompletas
continuam explícitas. Os mapas separam associações de decisões pendentes.

O relatório contém a comparação das 59 ocorrências, a origem dos problemas
documentais/espaciais/topológicos e as limitações dos padrões experimentais.
Quantitativos e confirmações humanas permanecem intactos. Não se atribui altura
útil, não se aprova armadura e não se autoriza uso resistente dos resultados.

## Etapa 10: presença e composição documental das regiões de atuação

```powershell
python -B tools/slab_geometry_poc/run_acting_compositions.py
python -B tools/slab_geometry_poc/run_acting_compositions.py --query 1380 800
python -B -m unittest discover -s tools/slab_geometry_poc -p 'test_acting_compositions.py'
```

Saída: `analises/lajes_composicao_atuacao`. Preserva os 35 polígonos e as 119
células anteriores. `acting_compositions.py` acrescenta presença por ocorrência,
direção/camada, função documental, conjuntos conjuntamente sustentados e
pendências. Os 15 conjuntos localizados continuam somente traços; nove
ocorrências continuam sem área elegível. Não recorta armaduras pelos contornos
de laje nem usa os contextos da Etapa 9.2 como geometrias estruturais.

O perfil externo `confirmacoes_engenheiro.json` registra N13 como base, vinculada
ao documento e às geometrias. N14 como reforço e N40 como traspasse permanecem
nas confirmações anteriores. Pares confirmados de base/reforço só se aplicam à
interseção de suas ocorrências; um terceiro membro não é promovido por
transitividade. O escopo documental N40 não define parceiro/zona exata de
traspasse: suas células permanecem pendentes e a adição independente bloqueada.

`consulta_regioes.html` permite consultar células e buscar por C/R/O/N, usando
a imagem `prancha_original.png` da mesma pasta, sem serviço externo. A consulta
CLI retorna todos os domínios incidentes em uma fronteira. Os mapas estáticos
e ampliações distinguem função conjunta, traspasse local e pendências. Os IDs
derivados independem da classificação, das cores e da ordem de entrada.

Nenhuma classificação autoriza soma numérica de armaduras ou validação
estrutural. Não se calculam As/m, altura útil, momento ou conformidade normativa.

## Etapa 11: quantificação nominal das armaduras positivas

```powershell
python -B tools/slab_geometry_poc/run_steel_quantification.py --concretopy-root ../concretopy
python -B -m unittest discover -s tools/slab_geometry_poc -p 'test_steel_quantification.py'
```

Saída: `analises/lajes_quantificacao_positiva`. `steel_quantification.py` reutiliza
`concretopy.Barra.area_cm2` e multiplica por `100/s`, sem arredondar internamente.
As taxas individuais dependem de bitola/espaçamento documentais, não da quantidade
impressa ou da qualidade do contorno. Sem espaçamento, As/m permanece pendente.
As classes da Etapa 10 não são alteradas: somas nominais só são autorizadas para
combinações conjuntamente sustentadas, sem traspasse, duplicidade ou conflito de
direção/camada. Todas as camadas anteriores permanecem intactas.

O perfil `criterios_documentais.json`, vinculado ao PDF, registra a instrução do
engenheiro: base/reforço positivos intercalados na mesma camada física. Mantém
as bitolas e centros próprios; não empilha o reforço nem generaliza essa regra
para os reforços localizados de furos. O cobrimento de 2 cm foi lido no detalhe
geral e na nota de unidades, com proveniência explícita. Centros e alturas úteis
continuam nulos, sem posições verticais inventadas. Espessuras confiáveis distintas
recebem casos separados, sem d único.

O relatório audita o Concretopy local: a API atual de camadas iguais e quantidades
inteiras não aceita diretamente densidades fracionárias/bitolas intercaladas no
mesmo nível. A estrutura preparada não é uma chamada de flexão executável e não
utiliza o empilhamento automático de vigas. Nenhuma adaptação do motor foi feita.
Não são calculadas resistência, suficiência estrutural ou conformidade normativa.

