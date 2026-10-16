# Compatibilização das skills ATP — 13/10/2026

## Inventário e comparação

Foi localizada uma skill específica de ATP: `atp-column-review`. Sua descrição
e entrada cobriam apenas geometria e níveis. Os procedimentos já executados de
comparação longitudinal, esperas e armaduras transversais ainda não estavam
consolidados em referências reutilizáveis.

Foram comparadas as entradas de `reinforcement-review` e `structural-conception`,
os contratos documentais de `tools/beam_model/STAGE1_CONTRACT.md` e os estados
de `tools/reinforcement_checks/diagnostic_update.md`. As entradas de
`structural-verification` e `project-management` estão vazias; não foram
consideradas procedimentos disponíveis nem preenchidas nesta revisão.

## Alterações aplicadas

- `atp-column-review/SKILL.md`: objetivo, entradas, fluxo, referências por etapa,
  ferramentas, entregas e limites; descrição atualizada para os controles já
  trabalhados, com exclusão explícita de capacidade resistente completa.
- `references/geometry-review.md`: procedimento geométrico anterior preservado
  em referência específica, incluindo cotas diretas, referências globais/locais,
  términos e posição dos traspasses. A referência de traspasses foi preservada.
- `references/longitudinal-comparison.md`: correspondência TQS/detalhe,
  quantidades por bitola, área e taxa, sem aprovação resistente pela área.
- `references/starter-bars-review.md`: comparação das esperas com o primeiro
  trecho físico, sem presumir nascimento no térreo.
- `references/transverse-reinforcement-review.md`: controle independente de
  diâmetro, espaçamento, exceções, continuidade nos nós e remissões; consulta
  da edição normativa de cada projeto, sem fixar seus limites numéricos.
- `references/review-contract.md`: dados e origem dos critérios, comparação
  documental, resultado técnico e execução separados; integração explícita com
  os estados anteriores, sem alterar motores ou esquemas de vigas.
- `references/coverage-register.md`: indicação explícita do alcance geométrico
  do contrato histórico e encaminhamento para o contrato de revisão.
- `reinforcement-review/SKILL.md`: seção 1.1 distingue revisão interna de ATP,
  impede que preferências internas fundamentem reprovação e encaminha pilares
  à skill específica. Uma linha com codificação mista foi normalizada para UTF-8.

O `AGENTS.md`, a skill de concepção, os métodos resistentes, os scripts de
extração e o verificador geométrico não foram alterados. Dados, contagens,
níveis e caminhos do empreendimento não foram incorporados às skills.

## Verificação

- Validador oficial `skill-creator/scripts/quick_validate.py`: válido para ATP,
  revisão de armaduras e concepção estrutural. A biblioteca YAML foi instalada
  apenas na pasta temporária da revisão, sem alterar dependências do projeto.
- Referências locais conferidas em todas as skills com conteúdo. Links das
  referências novas resolvem para o repositório e para os recursos existentes.
- Contrato geométrico exercitado com três situações sintéticas: pendência
  justificada permite cobertura classificada sem controle confrontado; controle
  não examinado e registro ausente impedem cobertura completa.
- Script geométrico e referências anteriores preservados; diff da revisão de
  armaduras limitado à integração ATP e à correção de codificação.

Esta validação comprova estrutura, vínculos e compatibilidade documental.
Não valida um motor resistente de pilares, que permanece fora do escopo,
nem transforma os controles feitos no ATP em aprovação integral.

## Continuidade

Utilizar a skill ATP nas próximas revisões de pilares e avaliar os procedimentos
com os novos casos reais. Uma futura verificação resistente exige contrato de
solicitações/seções/barras e método próprio validado. Não transferir diretamente
Concretopy ou regras de vigas para flexocompressão de pilares. As skills vazias
dependem de desenvolvimento próprio quando essas atividades forem solicitadas.


Pendência anterior encontrada na varredura: codificação mista em .agents\skills\reinforcement-review\references\positive-support-correction.md. Os vínculos foram conferidos preservando esses bytes; essas referências antigas não foram reescritas nesta revisão.
