---
name: atp-column-review
description: >
  Auxilia na avaliação técnica de pilares de projetos de terceiros (ATP),
  comparando formas, detalhamento e resultados TQS: geometria, níveis,
  armaduras longitudinais e taxas, esperas e armaduras transversais.
  Usar para revisão do projeto existente; não realiza a verificação completa
  da capacidade resistente dos pilares nem a otimização do detalhamento.
---

# Pilares em ATP

## 1. Objetivo e escopo

Avaliar o projeto recebido por pilar, trecho e controle. Abranger, conforme a
solicitação, coerência entre documentos, comparação da seleção longitudinal
TQS com o detalhamento, compatibilidade das esperas e controles normativos
de detalhamento longitudinal, transversal, emendas e ancoragens.
A comparação de áreas não verifica capacidade.

No modo atual, a verificação da armadura detalhada aos esforços cabe ao
engenheiro responsável. Não implementar nem executar dimensionamento ou
verificação resistente a partir de esforços extraídos do TQS neste fluxo.
Dados dependentes de esforços são solicitados ao engenheiro ou mantidos
inconclusivos; isso não impede concluir controles geométricos independentes.

Para ATP, separar requisito normativo, requisito documentado do projeto,
critério do software e recomendação de engenharia. Preferências internas do
escritório, padronização e economia não são critérios de reprovação do projeto
de terceiros. Uma orientação de revisão pode motivar esclarecimento sem
constituir requisito normativo.

## 2. Entradas e preparação

- Registrar documentos, revisões, processamento TQS, materiais, edição da
  norma adotada e pasta autorizada para a documentação. Não presumir que
  processamento e desenhos representam a mesma revisão.
- Definir pavimentos, trechos físicos, fundações, nós e prolongamentos incluídos.
  Explicitar exclusões; o primeiro lance de um pilar pode nascer acima do térreo.
- Reconciliar inventários das formas, detalhamento e TQS, quando este fizer
  parte da tarefa. Manter pilares presentes em apenas uma fonte e todos os IDs
  de grupos repetidos. Multiplicador contraditório exige confirmação.
- Definir os controles esperados e suas dependências antes da classificação.
  Dado ausente bloqueia apenas os controles que dele dependem.

## 3. Procedimento de revisão

Seguir o fluxo aplicável à tarefa:

Inventário e revisões → leitura documental independente → geometria por trecho
→ comparação das armaduras → verificações normativas específicas
→ diagnóstico por controle → apontamentos e pendências.

Definir a cobertura pelos controles do [checklist de revisão](references/review-checklist.md).
Existência de um procedimento na skill não significa que foi aplicado ao projeto.

Ler apenas as referências necessárias:

| Etapa | Procedimento |
|---|---|
| Geometria, níveis, comprimentos, transições e términos | [Geometria e níveis](references/geometry-review.md) |
| Localização dos traspasses em relação às vigas incidentes | [Posição dos traspasses](references/lap-splice-position.md) |
| Seleção longitudinal TQS, armadura detalhada, áreas e taxas | [Comparação longitudinal](references/longitudinal-comparison.md) |
| Diâmetros e distribuição das barras longitudinais na seção | [Detalhamento longitudinal](references/longitudinal-detailing-review.md) |
| Comprimento de esperas, ancoragens e emendas | [Aderência e traspasses](references/bond-and-lap-length-review.md) |
| Esperas: quantidade/bitola, posição e continuidade documental entre lances | [Esperas](references/starter-bars-review.md) |
| Diâmetro, espaçamento, continuidade e requisitos condicionais dos estribos | [Armaduras transversais](references/transverse-reinforcement-review.md) |
| Estados, evidências e integração com outras skills | [Contrato de revisão](references/review-contract.md) |
| Matriz documental de geometria e controle de cobertura | [Registro e cobertura](references/coverage-register.md) |

## 4. Leitura e dependências

Registrar separadamente o que cada documento informa. Distinguir marca,
ocorrência física e representação em elevação, corte ou tabela; a repetição
gráfica não duplica barras. OCR e extração preliminar auxiliam a leitura;
confirmar visualmente os dados que sustentam conclusões e ampliar ambiguidades.

Preservar valores originais, unidades, transformações e fontes. Não substituir
uma cota não lida por um valor calculado, nem completar o desenho com o valor
esperado do TQS. Uma correção de leitura deve atualizar registros, apontamentos
e entregas afetadas, mantendo histórico sem perpetuar a conclusão descartada.

## 5. Ferramentas e compatibilidade

Usar cálculos determinísticos para áreas, taxas, diferenças de nível e limites
normativos após comprovar as entradas. Investigar os arquivos TQS disponíveis;
formatos de vigas não comprovam a semântica dos arquivos de pilares.

O auxiliar [check_coverage.py](scripts/check_coverage.py) mantém seu
contrato de geometria descrito em Registro e cobertura. Não enviar diretamente
matrizes de armaduras para esse contrato nem inventar fontes de formas para
verificações que utilizam detalhe e norma. O código de saída zero comprova
cobertura classificada, inclusive com pendências, e não aprovação técnica.

A skill `reinforcement-review` possui métodos especializados de vigas.
Reutilizar princípios documentais e ferramentas apenas com domínio e entradas
compatíveis; não transferir motores de vigas para flexocompressão de pilares.
Nos ATPs de vigas, usar essa skill sob a mesma distinção de critérios, sem
aplicar automaticamente padrões internos ou etapas de otimização.

## 6. Resultado da revisão

Entregar, no formato solicitado e na pasta autorizada:

- matriz por pilar/trecho/controle, com leituras, fontes, critérios, resultados
  específicos e pendências;
- apontamentos com localização, conflito ou requisito, evidência e informação
  necessária à compatibilização;
- cobertura por etapa, distinguindo inventariado, executado, concluído,
  inconclusivo, não examinado e inaplicável justificado;
- contexto de continuidade com decisões, revisões e dependências em aberto.

Para planilhas, relatórios e PDFs, utilizar a skill de artefato disponível;
esta skill define o conteúdo de engenharia, não um segundo fluxo de exportação.
Antes de dizer “todos verificados”, reconciliar cada ID e controle solicitado.
Executar controles ainda não examinados; documento ausente gera pendência
concreta, sem encerrar silenciosamente o controle.

## 7. Limites e evolução

Concluir separadamente coerência documental, comparação de seleção e controles
normativos efetivamente executados. Coincidência com TQS ou atendimento de Ø e s
não demonstra capacidade, emendas, confinamento, estabilidade ou segurança global.

Capacidade dos pilares permanece fora do modo atual, sob responsabilidade
do engenheiro. Uma futura ampliação exige autorização explícita, procedimento
próprio e validação; não incorporar um motor resistente por inferência deste
checklist nem converter a seleção automática em armadura exigida por norma.

Manter dados e apontamentos do empreendimento na sua documentação. Incorporar
apenas procedimentos reutilizáveis demonstrados; consultar a edição normativa
aplicável em cada trabalho, sem adotar permanentemente a edição de um caso.
