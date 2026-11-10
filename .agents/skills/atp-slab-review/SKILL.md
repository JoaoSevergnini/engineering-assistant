---
name: atp-slab-review
description: >-
  Conduz a ATP preliminar de armaduras de flexão de lajes de concreto armado:
  formas, detalhamento, momentos DXF, resistência, cobertura e continuidade,
  com rastreabilidade e revisão humana. Coordena ferramentas existentes e
  leitura assistida; a automação é parcial e não constitui aprovação global.
---

# ATP de armaduras de flexão de lajes

A ATP é conduzida por fases, uma sessão por fase. Ler apenas as referências
indicadas para a fase em execução (seção 4); não ler todas as referências no
início da sessão.

## 1. Escopo e entregas

Revisar o projeto existente quanto a segurança, dimensionamento, cobertura,
continuidade e detalhamento de flexão. Emitir três entregáveis obrigatórios:
pranchas gráficas com seleção por região; relatório de incompatibilidades e
pendências por prancha; relatório técnico complementar de rastreabilidade.
Produzi-los com os dados disponíveis, explicitando o que não pôde ser verificado;
nenhum substitui os demais. Produzir apontamentos preliminares para seleção do
engenheiro. Executar as etapas possíveis, procurar
fontes adicionais para ambiguidades e solicitar confirmação humana quando
necessário; uma pendência bloqueia somente os controles dependentes.

O procedimento não é um verificador automático implementado. Cálculos e
geometria dependem de ferramentas compatíveis, adaptação validada ou avaliação
assistida, conforme o [catálogo de ferramentas](references/existing-tools.md).
Não existe comando único para ATP completa.

Padrão dos entregáveis: layout da prancha 7309 R02, campos editoriais da R03,
fichas R01 e relatório técnico R00 do 1º pavimento S07, descritos em
[reporting](references/reporting.md) e
[s07-1pav-deliverables](references/s07-1pav-deliverables.md). Não copiar suas
hipóteses, valores ou decisões para outro projeto.

## 2. Regras fixas

Aplicar a [convenção de esforços](../../../profile/force-presentation.md):
solicitações características e resistências equivalentes MRd/γf, com coeficiente
comprovado, normalmente em tf·m/m para lajes. Preservar resultados originais.
Sem conversão de natureza demonstrável, manter a natureza conhecida e declarar
a limitação. Não adotar γf=1,4 universalmente.

- Formas são a referência principal da geometria. Envoltória gráfica de
  armadura não é contorno estrutural; mudança de espessura não cria outra laje.
- Leitura não extraída não comprova falta no projeto. Diagrama não encontrado
  não significa momento zero. Procurar detalhes e remissões antes de apontar falta.
- Reforços positivos podem estar intercalados com a base; não empilhar
  automaticamente camadas nem somar sobreposições gráficas.
- Médias de momentos são indicadores, sem aprovação normativa automática.
  Interrupções usam distribuição local e resistência remanescente.
- Distinguir norma, requisito do projeto, critério do software, critério do
  escritório e hipótese. FAIL identifica o critério, não reprovação normativa.
- Registrar confirmação/correção com origem, autor e justificativa, preservando
  a leitura original. Após correção, retirar os resultados dependentes de uso
  vigente até reavaliação; não há propagação automática no código.
- ACCEPT/REJECT decide o destino de um apontamento, sem reescrever resultado
  técnico. Não incluir automaticamente todos os FAIL no relatório final.
- A seleção editorial é independente do resultado técnico: eta>1 nunca marca a
  seleção automaticamente; campos vazios são decisão pendente.
- Não importar scripts históricos S07 com cálculos/gravações no nível superior.
  Escolher uso conforme existing-tools; não reprocessar fontes por efeito de import.
- Não transferir premissas ou decisões de outro pavimento ou projeto; cada
  decisão vale para o escopo em que foi registrada.

## 3. Fases e continuidade

| Fase | Etapas do [fluxo](references/review-workflow.md) | Entrega que encerra a fase |
|---|---|---|
| 0. Preparação | Etapa 1 e premissas (seção 6) | Inventário e revisões conciliados; premissas confirmadas ou pendentes identificadas; matriz G01–A08 aberta; destino e revisões dos três PDFs |
| 1. Geometria | Etapa 2 | Cadastro de lajes e zonas (nome, h, nível, aberturas, apoios e faces) na precisão da seção 5; conflitos G01–G02 |
| 2. Armaduras e regiões | Etapas 3–4 | Ocorrências com fonte; regiões de composição comprovadas, alternativas e pendências de leitura |
| 3. Verificação | Etapas 5–7 | Resistências, indicadores DXF e controles A01–A08 executados ou com pendência objetiva; cobertura reconciliada |
| 4. Pacote preliminar | Etapa 8, etapa preliminar | Três PDFs preenchíveis, da mesma versão dos resultados, conferidos |
| 5. Emissão final | Etapa 8, etapa final | Escolhas e comentários recuperados; apontamentos selecionados preparados para o projetista |

- Executar cada fase em sessão própria, retomando por `retomada.md` e pelo
  índice, não pelo histórico da conversa. Fases curtas podem ser agrupadas.
- Dentro da fase, prosseguir sem pedir autorização entre tarefas: o pedido da
  fase autoriza suas leituras, cálculos, registros e emissões internas. Executar
  automaticamente os passos compatíveis; revisão humana dos apontamentos não
  implica pedir autorização para cada tarefa rotineira.
- Encerrar a resposta somente com a entrega da fase cumprida ou diante de decisão
  que bloqueie todo o trabalho restante da fase. Atualizações breves durante o
  trabalho não encerram a rodada.
- Perguntar somente quando a resposta mudar uma conclusão técnica, agrupando as
  dúvidas relacionadas; enquanto aguarda, avançar nos controles independentes.
  Não perguntar o que já consta em `premissas.json`.
- As etapas podem avançar por laje/região/direção; não esperar a solução de todo
  o pavimento para concluir um controle local independente.
- Ao encerrar a fase: atualizar índice e `retomada.md` e registrar as métricas
  da seção 7.

## 4. Leitura por fase

| Fase | Ler | Somente se necessário |
|---|---|---|
| 0 | [review-workflow](references/review-workflow.md): Preparação, Etapa 1; [review-criteria](references/review-criteria.md): Origem e controles esperados; [modelo de pedido](references/new-floor-prompt.md) | [contracts](references/contracts.md), se os registros usarem tools/slab_review |
| 1 | review-workflow: Etapa 2 | [existing-tools](references/existing-tools.md), ao escolher ferramenta |
| 2 | review-workflow: Etapas 3–4 | existing-tools |
| 3 | review-workflow: Etapas 5–7, Pendências; review-criteria: A01–A08; existing-tools: Concretopy | [historical-tools](references/historical-tools.md), ao avaliar reaproveitamento do térreo ou do PoC |
| 4 | [reporting](references/reporting.md); [s07-1pav-deliverables](references/s07-1pav-deliverables.md) | skill de PDF |
| 5 | reporting: Estados técnicos e seleção editorial; Revisão humana; Preservação das escolhas; Campos interativos | — |

## 5. Precisão da geometria

Determinar contornos e referências com a precisão necessária aos controles que
os utilizam: associar regiões de armadura e linhas de grelha às lajes,
identificar bordas, encontros e aberturas, e obter vãos livres entre faces
quando A03/A04 os exigirem. Refinar localmente onde a precisão altera uma
conclusão; não fazer rodadas de refinamento geral dos contornos. Contornos
candidatos continuam candidatos até o confronto com as formas. Origem: decisão
de João no 2º pavimento S07, adotada como regra do procedimento em 10/11/2026;
não há tolerância numérica definida.

Se a ATP de vigas do mesmo pavimento já tiver registrado geometria das formas
(ou vice-versa), reutilizá-la depois de conferir fonte, revisão e alcance.

## 6. Premissas da fase 0

Procurar cada item nos documentos; reunir em uma única consulta a João o que não
estiver documentado. Registrar em `premissas.json` valor, origem, data e alcance.
Itens recorrentes nas ATPs de lajes:

- fontes disponíveis: DXF/DWG das pranchas; planta do modelo TQS em DXF e sua
  origem; diagramas H/V e processamento;
- ordem das camadas H/V em positivas e negativas, contada da face tracionada;
  reforços intercalados com a base ou sobrepostos;
- diagramas: unidade, natureza (característica ou de cálculo), sinal, filtro
  mínimo e isocurva; existência de diagramas sem filtro;
- γf comprovado para MRd/γf;
- materiais, cobrimento, agregado máximo e conformação superficial do aço;
- sequência de concretagem de vigas e lajes; faixas de segunda etapa;
- referência altimétrica do modelo e cota das lajes sem desnível indicado;
- seções especiais de borda e sua representação no modelo TQS;
- avaliação dos momentos volventes no dimensionamento, quando um critério de
  ancoragem dos positivos depender dela;
- enquadramento das lajes em uma ou duas direções para os mínimos;
- escopo de aberturas e furos;
- tratamento de negativas sobrepostas de apoios distintos;
- tolerância editorial para η, se houver.

## 7. Economia de contexto e de chamadas

O custo de uma sessão cresce com o número de chamadas multiplicado pelo tamanho
do contexto, e cada imagem aberta permanece no contexto. No 2º pavimento S07
houve 94,5 milhões de tokens, 300 comandos, 200 imagens abertas, 38 scripts no
pavimento, contornos refeitos em sete versões e cerca de quinze retomadas por
interrupção. Aplicar:

1. **Premissas uma vez:** materiais, h, cobrimento, camadas, γf e decisões ficam
   em `premissas.json`; scripts leem esse arquivo, sem valores fixos no código.
2. **Um script por função:** estender o script existente do pavimento; a revisão
   (R01, R02...) identifica os arquivos de saída, não cópias do script.
3. **Saída curta:** no terminal, até cerca de 30 linhas (totais e IDs das
   exceções); o detalhe vai para arquivo.
4. **Consulta dirigida:** não abrir JSON, TSV ou markdown grandes inteiros;
   consultar por ID com um script curto.
5. **Imagens sob demanda:** conferir primeiro por verificação automática (IDs,
   contagens, colisões, campos de formulário). Inspecionar cada página emitida uma
   vez por revisão, conforme reporting; após alteração, reinspecionar somente as
   páginas e recortes afetados. Para leitura de pranchas, abrir recortes ampliados
   da região em dúvida, não a prancha inteira repetidas vezes.
6. **Sessão por fase:** não ramificar a conversa para trabalho em lote; agentes
   auxiliares recebem IDs e entradas e devolvem resultado compacto.
7. **Registrar o esforço:** ao fim de cada fase, anotar lajes, regiões e controles
   executados, scripts criados, reexecuções e motivos, para comparar com o S07.

## 8. Arquivos

Conforme o `AGENTS.md` (seção 16), resultados de projeto não são versionados
neste repositório e dados de obra não ficam na skill. Enquanto a pasta do
projeto não estiver definida, trabalhar em `analises/<projeto>_lajes_<pavimento>/`,
fora do git:

```
inventario.json        fontes, caminhos, revisões, abrangência e hashes
premissas.json         escopo, materiais, camadas, coeficientes, decisões (origem e data)
indice_controles.json  controles por objeto: execução, resultado, entrada vigente, dependências
retomada.md            resumo de retomada (até uma página, sobrescrito)
geometria/             cadastro de lajes, zonas, apoios e alinhamentos
armaduras/             ocorrências, regiões e composições
diagramas/             leitura e calibração dos DXF de momentos
scripts/               scripts do pavimento (poucos, um por função)
resultados/            resultados brutos das ferramentas
output/pdf/            emissões, conforme reporting (Organização dos arquivos)
```

## 9. Iniciar uma nova ATP

Usar o [modelo de pedido](references/new-floor-prompt.md). Identificar pasta do
projeto/destino, pavimento e documentos disponíveis; se constarem das fontes,
utilizá-los sem pedir transcrição. Começar pelas leituras e verificações
independentes possíveis. Recuperar decisões anteriores antes de emitir.

## 10. Exclusões

Punção, deformações das lajes, rigidez global dos apoios, revisão completa da
concepção estrutural e otimização de quantitativos de aço. A revisão de aberturas
não inclui dimensionamento específico dos reforços ou verificação completa de
barras interrompidas. Nenhuma conclusão preliminar aprova globalmente o projeto.
