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
continuidade e detalhamento de flexão. A entrega principal são PDFs gráficos de
comparação resistência × solicitação por prancha ou conjunto de regiões, sempre
que houver dados suficientes. O relatório consolidado é complementar e não
substitui esses PDFs. Produzir controles e apontamentos preliminares para seleção
do engenheiro. Executar as etapas possíveis, procurar
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
| Produzir os PDFs gráficos obrigatórios, classificar e preparar o relatório complementar | [Entregas e revisão humana](references/reporting.md) |
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
8. Produzir PDFs gráficos de verificação sobre as pranchas originais, com regiões,
   IDs, armaduras, resistências, dois indicadores de solicitação, n de linhas,
   relações compatíveis, diferenciação visual e quadro lateral de resultados e
   pendências. Consolidar cobertura e apontamentos em relatório complementar e
   submetê-los à seleção e redação final do engenheiro.

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

## Entrega gráfica padrão

Seguir [reporting](references/reporting.md): usar como referência de composição
a prancha ATP_S07_7307_faixas_Mrk_Msol_media.pdf, sem copiar dados, fatores,
materiais, espessuras ou a omissão histórica de regiões sem resistência publicada.
O novo padrão inclui os dois indicadores e pendências explícitas.

Preservar a base original e preferir sobreposições vetoriais legíveis. Separar
pranchas, direções, faces ou critérios quando necessário. Cores identificam o
critério de comparação, não aprovação estrutural; médias favoráveis não eliminam
alertas locais. Campo sem dado fica pendente, nunca zero.

O pacote tools/slab_review ainda não possui gerador integrado desses PDFs.
Consultar [existing-tools](references/existing-tools.md#referências-para-os-pdfs-gráficos-padrão)
para os geradores históricos que exigem adaptação. A obrigação de entrega não
autoriza importar/executar históricos com efeitos globais nem declarar um PDF
inexistente como produzido. Se a emissão não for possível, registrar o impedimento
e o PDF devido; o relatório sozinho não cumpre a entrega gráfica.

## Iniciar uma nova ATP

Identificar pasta do projeto/destino, pavimento e documentos disponíveis; se
constarem das fontes, utilizá-los sem pedir transcrição. Registrar inventário e
abrir a matriz de controles de review-criteria. Começar pelas leituras e
verificações independentes possíveis. Manter dados, evidências e decisões em
analises/<projeto> ou no destino indicado; não guardar dados de obra na skill.
Não existe comando único para ATP completa.

## Exclusões

Punção, deformações das lajes, rigidez global dos apoios, revisão completa da
concepção estrutural e otimização de quantitativos de aço. A revisão de aberturas
não inclui dimensionamento específico dos reforços ou verificação completa de
barras interrompidas. Nenhuma conclusão preliminar aprova globalmente o projeto.
