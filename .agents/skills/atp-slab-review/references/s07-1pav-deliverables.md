# Padrões inspecionados na ATP S07 — 1º pavimento

Referência de apresentação e operação, não fonte de hipóteses gerais de engenharia.
Os arquivos citados estão em analises/atp_s07_lajes_1pav, área de trabalho local
fora do git (AGENTS.md, seção 16); se não estiverem acessíveis, as descrições
deste arquivo e de [reporting](reporting.md) definem o padrão.
Arquivos localizados e inspecionados no incremento documental de 24/10/2026:

| Referência | Papel e constatação |
|---|---|
| [7309 POS H R02](../../../../analises/atp_s07_lajes_1pav/output/pdf/verificacoes_R02/ATP_S07_1PAV_7309_POS_H_Mr_Msol_R02.pdf) | Padrão gráfico: prancha-base, caixas próximas, quadro lateral e apêndices; 11 páginas, sem campos de formulário |
| [Incompatibilidades R01](../../../../analises/atp_s07_lajes_1pav/output/pdf/consolidado/ATP_S07_1PAV_incompatibilidades_pendencias_R01.pdf) | Índice por prancha, fichas com imagens comparativas, pendências e comentários; 18 páginas e 75 campos AcroForm/widgets no arquivo inspecionado |
| [Relatório técnico R00](../../../../analises/atp_s07_lajes_1pav/output/pdf/consolidado/ATP_S07_1PAV_relatorio_armaduras_R00.pdf) | Memória de escopo, fontes, decisões, geometria, resistência, DXF, quantitativos e cobertura; 8 páginas |
| [7309 POS H R03](../../../../analises/atp_s07_lajes_1pav/output/pdf/verificacoes_R03/ATP_S07_1PAV_7309_POS_H_Mr_Msol_R03.pdf) | Evolução funcional: 178 checkboxes, dois por região, inicialmente Off. Complementa o layout R02; não o substitui como referência solicitada |

Essas contagens descrevem apenas os arquivos inspecionados; não são critérios
de quantidade de páginas/campos para outro projeto. A formatação do térreo
7307 continua referência histórica secundária. O padrão corrente é o conjunto
do 1º pavimento, definido em [reporting](reporting.md).

## Geradores efetivamente encontrados

Caminhos relativos a analises/atp_s07_lajes_1pav. Não importar esses arquivos:
executam leitura, criação de diretórios, gravações e emissão no nível superior.
Não foram executados nesta padronização.

| Gerador | Entradas e saídas | Reaproveitamento e limitações |
|---|---|---|
| emitir_pdfs_R02.py | inventario.json, regioes_capacidades.json, comparacao_faixas.json, ocorrencias_pendentes.json, tabelas, ocorrências, mínimos, glifos/OCR, alinhamento e contornos → mapas em verificacoes_R02, qa_rotulos_R02.json e entregas_pdf_R02.json | Referência principal do layout. Funções txt, wrapped, state, polys, configure; posicionamento por obstáculos/ocupação da imagem; mapa vetorial, caixas, quadro e apêndices. Não cria widgets, não tem configuração genérica de projeto |
| emitir_pdfs_R03.py | Mesma família de inputs → mapas verificacoes_R03, widgets e QA/manifestações R03 | Acrescenta seleção INCLUIR/NAO_INCLUIR por região. Usa fitz.Widget, sem exigir desenho manual da caixa. Inicializa campos; não recupera escolhas de revisão anterior |
| emitir_relatorio_incompatibilidades_R01.py | inventário, regiões, ocorrências pendentes e imagens em etapa_complementar/relatorio_evidencias, além de narrativa cadastrada no script → relatório R01, renders/atlases QA e manifesto | Funções page, text, controls, card, img, label: cabeçalho, fichas, imagens e campos. Narrativa, índice e conflitos são específicos do caso; não é detector automático de incompatibilidades |
| emitir_pdfs.py | Inventário, dados de armaduras/cálculos/comparações/mínimos e textos técnicos → mapas iniciais e relatorio_armaduras_R00.pdf | Origem efetiva do relatório técnico solicitado. Parte ReportLab usa P, para, head, table e foot; tabelas com repetição de cabeçalho, paginação e memória técnica. Rodar o script também emite mapas, não só o relatório; textos/contagens estão acoplados ao caso |

Dependências declaradas nos geradores: PyMuPDF, Shapely/STRtree, NumPy,
ReportLab e Pillow conforme o emissor; pypdf no relatório/QA dos formulários.
Os scripts apontam para tmp/s07_pdf_deps e fontes Arial do Windows. A presença
da pasta não garante compatibilidade de versão/arquitetura com todo Python
disponível; conferir o ambiente antes de emitir, sem instalar por presunção.

O código de posicionamento R02/R03 usa glifos, OCR, obstáculos de carimbo/tabelas,
rótulos de laje e ocupação raster para escolher caixas; o PDF-base permanece
incorporado por show_pdf_page. Preservar essa finalidade sem fixar larguras de
painel, fontes/tamanhos, coordenadas, limites de registros ou contornos da S07.
Uma heurística de melhor posição não prova ausência de colisões: renderizar e
conferir especialmente os detalhes densos.

state classifica pela disponibilidade e pelos dois indicadores; não é seleção
editorial. Leitura parcial e pico local têm sinalizadores próprios.
configure e a apresentação B/R dos emissores inferem função pela ordem das
famílias em certos trechos. Em outro projeto, vincular marcas/famílias/funções
explicitamente; não assumir que primeira família é base ou que só há um reforço.

## Campos de dados e convenções de apresentação

Os geradores usam comparacao_faixas.json: MRk_eq_tfm_m,
S1_mean_line_peaks_tfm_m, S3_mean_top3_lines_tfm_m, eta1, eta3,
n_valid_lines, n_expected_native_axes, demand_scope, max_local_tfm_m e eta_local.
Na apresentação aprovada, Msol2 é a média top 3 e eta2 é o campo histórico eta3.
Preservar esse mapeamento sem renomear os dados existentes por cosmética.

n_expected_native_axes se refere ao domínio nativo reconstruído; não comprova
inventário integral de linhas físicas. Preservar o denominador e LP.
Leitura parcial não se torna completa porque o indicador não supera resistência.
Não transpor filtros de magnitude, escalas ou número de eixos da S07.

As regiões referenciam geometry_pdf, marks, families, As_cm2_m, h_cm, fck_MPa,
capacity, issues, overlap_region_ids, variable_length_envelope e slabs_candidates.
O contrato mínimo do 1A não representa todos esses campos nem é entrada direta
desses emissores: é necessário manter registro/adaptador explícito compatível.

## Formulários e QA disponíveis

- conferir_emissao_R02.py e conferir_R02.py: referências de conferência da emissão,
  layout e integridade. Ler as condições concretas antes de aproveitar asserts.
- conferir_formularios_R03.py: verifica campos canônicos com pypdf, widgets,
  aparências, quantidade esperada pelo caso e estado inicial Off; testa
  marcar/desmarcar e leitura após serialização em memória.
- O próprio emitir_relatorio_incompatibilidades_R01.py confere árvore de campos,
  widgets, aparências e valores; produz manifesto e renders para revisão visual.

A inspeção confirmou widgets reais e comentários multilinha no relatório.
A R03 de pranchas e a R01 de fichas usam duas checkboxes independentes; não foi
encontrada exclusividade implementada por grupo de opção ou ações no gerador.
Contagem, aparência e teste de toggle não provam exclusão mútua nem migração
de seleções. Exigir as regras de decisão e validação de reporting.

## Configuração para um novo projeto

1. Definir projeto, pavimento, fontes/revisões, destino, IDs e revisões das três
   emissões. Separar documentos internos de revisão da emissão ao projetista.
2. Preparar dados próprios compatíveis de regiões, armaduras efetivas, capacidades,
   indicadores, cobertura e pendências, com correspondência explícita ao contrato
   ou registros complementares. Não preencher dados ausentes por padrões S07.
3. Recuperar PDFs preenchidos, escolhas, comentários e histórico antes de gerar
   uma nova revisão. Resolver correspondência física/documental dos itens.
4. Utilizar os emissores como base de apresentação em execução isolada com destino
   do projeto; parametrizar/adaptar localmente entradas, narrativa e layout quando
   necessário, preservando originais. Não executar defaults S07 para outra obra,
   nem importar scripts só para chamar uma função.
5. Gerar os três tipos e coordenar os passos compatíveis automaticamente.
   Se faltar adaptação, registrar a necessidade localizada; não reconstruir todo
   o formato nem alegar que existe CLI genérica pronta.
6. Conferir renderização, campos, dados, pendências e revisão humana conforme
   reporting. Somente após seleção/comentários preparar o relatório ao projetista.

Preservar: base vetorial, caixas próximas com chamadas, B/R comprovados, quadro
lateral, LP/picos/pendências, índice e fichas comparativas, seleções/comentários,
memória técnica e QA. Substituir: nomes, datas, fontes, revisões, casos, figuras,
geometrias, h, materiais, cobrimento, camadas, coeficientes, enquadramentos,
normas/edições efetivamente aplicáveis, filtros e contagens do projeto.

## Funcionalidades ainda não generalizadas

Não existe CLI de emissão dos três tipos para projeto arbitrário, catálogo
automático de incompatibilidades confirmadas, importação/migração automática das
decisões, exclusão mútua comprovada dos pares ou gerador final ao projetista que
selecione itens aprovados a partir dos formulários. O 1A registra decisões, mas
não lê/grava AcroForms. Nenhum desses mecanismos foi implementado nesta etapa.

A geração S07 já executada é evidência de apresentação e operação dos documentos,
não de motor geral integrado. Os procedimentos de preservação, seleção e
conferência devem ser cumpridos operacionalmente até existir automação validada.
