---
name: atp-slab-review
description: >-
  Conduz a ATP preliminar de armaduras de flexão de lajes de concreto armado:
  formas, detalhamento, momentos DXF, resistência, cobertura e continuidade,
  com rastreabilidade e revisão humana. Coordena ferramentas existentes e
  leitura assistida; a automação é parcial e não constitui aprovação global.
---

# ATP de armaduras de flexão de lajes

## Escopo e modo de trabalho

Revisar o projeto existente quanto a segurança, dimensionamento, cobertura,
continuidade e detalhamento de flexão. Emitir três entregáveis obrigatórios:
pranchas gráficas com seleção por região; relatório de incompatibilidades e
pendências por prancha; relatório técnico complementar de rastreabilidade.
Produzi-los com os dados disponíveis, explicitando o que não pôde ser verificado;
nenhum substitui os demais. Produzir apontamentos preliminares para seleção do
engenheiro. Executar as etapas possíveis, procurar
fontes adicionais para ambiguidades e solicitar confirmação humana quando
necessário; uma pendência bloqueia somente os controles dependentes.

O incremento 1B documenta o procedimento operacional. O código de
tools/slab_review permanece no incremento 1A: contratos, estados, dependências
e decisões humanas. O procedimento completo não é um verificador automático
implementado. Cálculos e geometria dependem de ferramentas compatíveis,
adaptação validada ou avaliação assistida, conforme o catálogo abaixo.

## Referências por tarefa

| Momento da revisão | Consultar |
|---|---|
| Iniciar projeto, executar as oito etapas e tratar pendências | [Fluxo operacional](references/review-workflow.md) |
| Definir controles, critérios, bases resistentes e indicadores | [Critérios de revisão](references/review-criteria.md) |
| Escolher ferramenta e verificar entradas, dependências e efeitos | [Ferramentas existentes](references/existing-tools.md) |
| Emitir os três documentos e conduzir a revisão preliminar/final | [Entregas e revisão humana](references/reporting.md) |
| Reaproveitar layout, formulários e geradores da ATP S07 1º pavimento | [Referências inspecionadas e reutilização](references/s07-1pav-deliverables.md) |
| Criar registros Python, estados e decisões do incremento 1A | [Contratos](references/contracts.md) |

Aplicar a [convenção de esforços](../../../profile/force-presentation.md):
solicitações características e resistências equivalentes MRd/γf, com coeficiente
comprovado, normalmente em tf·m/m para lajes. Preservar resultados originais.
Sem conversão de natureza demonstrável, manter a natureza conhecida e declarar
a limitação. Não adotar γf=1,4 universalmente.

## Fluxo de execução

1. Inventariar formas, positivas, negativas, DXFs e detalhes complementares;
   conciliar revisões e definir escopo/controles esperados.
2. Reconstruir geometria pelas formas: lajes, zonas de espessura, níveis,
   aberturas, faces de apoios e encontros.
3. Identificar armaduras e remissões, distinguindo marca, ocorrência e conjunto
   físico; confirmar face, direção, distribuição e posição vertical.
4. Determinar regiões de atuação/composição com evidências de independência e
   atuação conjunta; conservar ambiguidades e capacidades individuais.
5. Calcular resistência pelo Concretopy quando as entradas e o modelo forem
   aplicáveis; preservar diagnósticos. Arranjo não representável exige método
   equivalente justificado, sem contornar validações do motor.
6. Reconstruir momentos nas linhas de grelha com escala/sinal/natureza e
   alinhamento comprovados; preservar valores locais e lacunas. Obter os dois
   indicadores regionais quando possível, sem exigir interpolação entre linhas.
7. Executar independentemente os controles de cobertura, flexão, bordas,
   continuidade, interrupções, desníveis e aberturas.
8. Emitir pranchas gráficas com resultados e seleção por região; fichas de
   incompatibilidades confirmadas, pendências e pedidos de informação separados;
   relatório técnico de rastreabilidade e cobertura. Após revisão humana,
   preservar escolhas/comentários e preparar somente os apontamentos selecionados
   para o relatório destinado ao projetista.

As etapas podem avançar por laje/região/direção; não esperar a solução de todo
o pavimento para concluir um controle local independente.

## Invariantes operacionais

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
- Não importar scripts históricos S07 com cálculos/gravações no nível superior.
  Escolher uso conforme existing-tools; não reprocessar fontes por efeito de import.

## Padrão dos três entregáveis

Seguir [reporting](references/reporting.md) e as
[referências finais do 1º pavimento S07](references/s07-1pav-deliverables.md).
A prancha 7309 R02 governa o layout; a R03 registra a adição dos campos editoriais.
As fichas R01 de incompatibilidades e o relatório técnico R00 governam os outros
dois formatos. Não copiar suas hipóteses, valores ou decisões para outro projeto.

Nas pranchas, mostrar armadura efetivamente calculada (base/reforço), As, Mr,
Msol1/Msol2, eta1/eta2, n e cobertura, LP, pico local e pendências, com quadro
lateral. Preservar por região “Incluir no relatório”, independente da
classificação técnica; eta>1 nunca marca a seleção automaticamente.

Nas fichas, usar seleção “Incluir no relatório final”/“Não incluir” mutuamente
exclusiva e comentários do engenheiro, preferencialmente em campos PDF reais.
Ambas vazias significam decisão pendente; ambas marcadas são conflito, não
autorização de emissão. Não recadastrar insuficiências já apresentadas nos mapas
como incompatibilidades documentais.

Há geradores executados na S07 para os três formatos e para formulários, mas
ainda são scripts específicos, com gravações no nível superior. Coordenar os
recursos compatíveis e preservar o layout sem reconstruí-lo a cada ATP;
consultar o catálogo antes de executar. Não existe gerador genérico integrado
ao contrato 1A nem migração automática de decisões entre revisões.
Emitir primeiro o pacote preliminar. Somente após seleção, comentários e revisão
da redação pelo engenheiro preparar a emissão ao projetista. Preservar histórico
e revalidar escolhas em regiões alteradas.

## Iniciar uma nova ATP

Identificar pasta do projeto/destino, pavimento e documentos disponíveis; se
constarem das fontes, utilizá-los sem pedir transcrição. Registrar inventário e
abrir a matriz de controles de review-criteria. Começar pelas leituras e
verificações independentes possíveis. Manter dados, evidências e decisões em
analises/<projeto> ou no destino indicado; não guardar dados de obra na skill.
Preparar as entradas de apresentação indicadas em s07-1pav-deliverables, definir
as revisões/destinos dos três PDFs e recuperar decisões anteriores antes de emitir.
Executar automaticamente os passos compatíveis; revisão humana dos apontamentos
não implica pedir autorização para cada tarefa rotineira. Não existe comando
único para ATP completa.

## Exclusões

Punção, deformações das lajes, rigidez global dos apoios, revisão completa da
concepção estrutural e otimização de quantitativos de aço. A revisão de aberturas
não inclui dimensionamento específico dos reforços ou verificação completa de
barras interrompidas. Nenhuma conclusão preliminar aprova globalmente o projeto.
