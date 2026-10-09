# Consolidação das verificações estruturais por viga

Módulo exclusivo de diagnóstico: não recalcula, não dimensiona, não seleciona correções e não altera o desenho. O Concretopy permaneceu intacto. Estados, fontes e resultados históricos foram preservados.

## Arquitetura e arquivos

Criados: tools/reinforcement_checks/beam_diagnostic.py (contrato/agregação/ocorrências/relações/Markdown); beam_diagnostic_adapters.py (adaptação explícita); test_beam_diagnostic.py; beam_diagnostic.md; analises/pranchas/validar_diagnostico_vigas.py; cinco *_beam_diagnostic.json e cinco *_beam_diagnostic.md; beam_diagnostic_validation.json; referência da Skill beam-diagnostic.md. Atualizados: SKILL.md e README das verificações. Esta auditoria não modifica relatórios anteriores.

## Fontes consultadas

AGENTS e Skill; referências de escalonamento, apoio positivo, negativa, nós extremos, cortante, suspensão e identificação indireta; módulos positive_flexure, longitudinal_review, support_geometry, shear_review, suspension_review; contratos beam_model; API pública Concretopy; JSONs V501/V516/V517/V536/V565 e relatórios reais. As fórmulas resistentes não foram copiadas.

## Regras e contrato para correção futura

Identidade estrita por viga/pavimento/origem-direção-unidade; fontes versionadas por SHA256. Controles normalizados conservam localização, marcas, demanda, fornecido, unidade, critério, evidência e dados ausentes. IDs determinísticos por identidade/escopo da fonte/ID lógico, independentes dos valores e da ordenação. FAIL prevalece sem apagar INCONCLUSIVE ou revisão do engenheiro. Módulo ausente/cobertura incompleta gera pendência; NOT_APPLICABLE exige prova. Relações por marcas ou sobreposição comprovada não fundem ocorrências nem provam solução comum.

Uma futura correção recebe ocorrências e controles associados, incluindo PASS, contexto físico e fontes. Nenhuma proposta é gerada aqui. selected_solution=null, detailing_optimization=null e structural_safety_declaration=null.

## Casos reais

| Viga | Positiva | Negativa | Ancoragem | Cortante | Suspensão | Consolidado | Falhas |
|---|---|---|---|---|---|---|---|
| V501 | INCONCLUSIVE | INCONCLUSIVE | INCONCLUSIVE | INCONCLUSIVE | INCONCLUSIVE | INCONCLUSIVE | 0 |
| V516 | INCONCLUSIVE | FAIL | FAIL | INCONCLUSIVE | INCONCLUSIVE | FAIL | 4 |
| V517 | INCONCLUSIVE | FAIL | FAIL | INCONCLUSIVE | INCONCLUSIVE | FAIL | 4 |
| V536 | INCONCLUSIVE | INCONCLUSIVE | FAIL | INCONCLUSIVE | INCONCLUSIVE | FAIL | 1 |
| V565 | INCONCLUSIVE | INCONCLUSIVE | INCONCLUSIVE | INCONCLUSIVE | INCONCLUSIVE | INCONCLUSIVE | 0 |

## Falhas comprovadas

| Viga | Controle | Marcas | Necessário | Fornecido | Unidade |
|---|---|---|---|---|---|
| V516 | vertical_bend_geometry | ['N4'] | 48.7 | 40 | cm |
| V516 | al_plus_lb | ['N8'] | 126.67384157702772 | 79.0 | cm |
| V516 | flexural_capacity | ['N7', 'N8', 'N9'] | 168.9881928 | 160.31741548190314 | kN.m |
| V516 | vertical_bend_geometry | ['N7'] | 48.7 | 45 | cm |
| V517 | al_plus_lb | ['N8'] | 126.67384157702772 | 79.0 | cm |
| V517 | vertical_bend_geometry | ['N4'] | 48.7 | 40 | cm |
| V517 | flexural_capacity | ['N7', 'N8', 'N9'] | 162.3785107 | 160.31741548190314 | kN.m |
| V517 | vertical_bend_geometry | ['N7'] | 48.7 | 45 | cm |
| V536 | anchorage_length | ['N2'] | 24.203000349699796 | 21.5 | cm |

## Pendências e limites

V501 não possui todas as disciplinas e conserva regiões sem demanda amostrada/geometria documental resolvida. V516/V517 conservam flexão positiva não fornecida nesta consolidação, cobertura física de estribos nos vãos extremos não comprovada, geometria transversal/ancoragem curva e inventário de suspensão pendentes. A planta de apoios indiretos segue adiada. V536 conserva limitações documentais e do nó; alternativas não selecionadas não corrigem sua falha original. V565 não apresenta falha comprovada nos registros fornecidos, mas não possui revisão integral das cinco disciplinas.

As regiões de capacidade utilizam exclusivamente comparações já calculadas; cabimento/hipóteses/ductilidade existentes são controles separados. Modelos amostrados não substituem automaticamente geometria documental pendente. Adaptadores são específicos dos contratos lidos; não garantem inventário universal de todos os controles possíveis. Continuidade legada não constitui revisão nova: eventos explicitamente SUPERSEDED ficam na auditoria e relações posteriores são utilizadas; a cobertura negativa completa permanece false no envelope.

Impossibilidade reta no modo VERTICAL_BEND é preservada como FAIL de observação não governante, com prova explícita do modo; falhas da dobra continuam governantes. O contrato rejeita tentativas de retirar arbitrariamente outras falhas da agregação. Ausência de posição no controle normalizado permanece explícita; não se inventa coordenada.

Os relatórios históricos que diziam apoio direito positivo não implementado são antecedentes preservados. O JSON integrado atualizado é posterior e contém a generalização; o diagnóstico usa esse resultado sem reescrever o histórico.

## Testes e preservação

47 testes novos: estados/agregação, mistura de identidades/coordenadas, ocorrência por barra/região, fontes/unidades, determinismo, serialização, ausência de fórmulas/importação Concretopy, proteções de inaplicabilidade/observações de modo e cinco casos reais. Os cinco diagnósticos persistidos são reproduzidos integralmente. 141 arquivos históricos/Concretopy protegidos por SHA256 continuam iguais. Contagem e saídas finais das suítes são registradas abaixo após conclusão.

Validação final: **1015 testes engineering-assistant aprovados** (39 extrator + 30 beam_model + 57 beam_mapping + 889 reinforcement_checks), incluindo **47 novos**. **427 testes Concretopy aprovados**. quick_validate: Skill válida. git diff --check: aprovado nos dois projetos. Ponteiros de fonte resolvidos e cinco JSONs reproduzidos integralmente. Logs e hashes estão em analises/pranchas/beam_diagnostic_validation.json. Nenhuma mudança no Concretopy ou nos arquivos históricos protegidos.
