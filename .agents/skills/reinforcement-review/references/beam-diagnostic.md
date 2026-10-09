# Diagnóstico consolidado das armaduras de vigas

Depois das revisões independentes de positiva, negativa, ancoragem, cortante e suspensão, executar o [consolidador](../../../../tools/reinforcement_checks/beam_diagnostic.md). Usar resultados existentes, sem recalcular resistência, reinterpretar diagramas ou selecionar correções.

1. Comprovar identidade da viga/pavimento e coordenadas físicas comuns.
2. Adaptar explicitamente os contratos existentes; separar original vigente, histórico substituído e alternativas não selecionadas.
3. Preservar estados, valores, unidades, fontes, critérios, localização e pendências.
4. Gerar ocorrências distintas de falhas, inconclusões e revisão do engenheiro; relacioná-las por marcas/regiões comprovadas, sem fundir ou presumir solução comum.
5. Consolidar cada disciplina e o conjunto, com FAIL prevalecendo sem esconder INCONCLUSIVE. Módulo ausente não é NOT_APPLICABLE; inaplicabilidade exige evidência.
6. Gerar JSON e relatório equivalentes. Não declarar segurança global da estrutura.

Ferramentas: `beam_diagnostic.consolidate`, `beam_diagnostic.markdown` e adaptadores explícitos `beam_diagnostic_adapters`. Casos reais: `analises/pranchas/validar_diagnostico_vigas.py`. Contrato para correção futura: ocorrências estruturadas, controles relacionados e fontes versionadas. Nesta etapa selected_solution/detailing_optimization continuam null; não aplicar automaticamente as alternativas exploratórias registradas em tarefas anteriores.

Para a vista atualizada de execução, interpretação de pontas sem cota e contratos de correções futuras, consultar [diagnostic_update.md](../../../../tools/reinforcement_checks/diagnostic_update.md). Usar attach_execution após consolidate. Não gerar soluções nem alterar pranchas ao consolidar diagnósticos.
