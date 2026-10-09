# Implementação da revisão de armadura de suspensão

Data: 08/10/2026. Objetivo: verificar deterministicamente o detalhamento existente da receptora, sem otimização/redesenho e sem alterar conclusões positivas, negativas ou de cortante.

## Arquitetura e fontes consultadas

Consultados AGENTS, reinforcement-review, referências positivas/negativas/cortante, shear_review, shear_diagram, shear_coverage, suporte geométrico/mapeamento, modelos de detalhamento, consolidação/extrator TQS, APIs/resultados/materiais do Concretopy, documentos e validações V516/V517. Confirmadas as correções recentes da N12 e da cobertura nas faces dos pilares antes da implementação.

`suspension_review.py` é uma camada independente: identifica/requer provas da transferência e aplicação, valida reação total/natureza, distribui a região física, consulta diagrama existente e Concretopy, combina taxas e verifica cada faixa. Não altera nem soma novamente nos resultados de review_shear_spans. connections_from_mapping consome relações existentes com fontes, preservando reações max/min não selecionadas até confirmação de natureza/totalidade/combinação e posição.

## API do Concretopy

Auditoria anterior à alteração em suspension_concretopy_api_audit.md. Autorizada exclusivamente a exposição da parcela calculada de cortante: ResultadoCortante acrescenta asw_por_s_calculado=max(0, parcela antes do mínimo) e asw_por_s_minimo em cm²/m, opcionais na construção legada. Três atributos originais, construção posicional inicial, igualdade, valores e assinatura da função preservados. asdict tem serialização aditiva explícita. Não se alteraram equações, biela, smax, mínimo, flexão, lb ou al.

Reversão somente em memória confirmou por hash a alteração restrita dos dois fontes. 40 chamadas ao motor anterior reconstituído e ao atual, com fatores/bitolas/ângulos diferentes, produziram valores legados e exceções idênticos. A API Aco.fyd fornece a resistência do aço; o assistant aplica o procedimento da fração da reação e conversões expressamente fornecidas, sem copiar equações resistentes de cortante.

## Exemplo numérico completo — SINTÉTICO

Fixture persistente suspension_synthetic_fixture.json, reproduzida por validar_suspensao.py. Estes números não são reação de V516/V517.

| Grandeza | Valor / fonte |
|---|---|
| Viga apoiada / receptora | SUPPORTED / SUPPORT; transferência e aplicação explícitas da fixture |
| Reação original total | {'value': 100, 'unit': 'kN', 'nature': 'CHARACTERISTIC', 'is_total': True, 'total_source': 'synthetic all-actions support envelope', 'combination': 'synthetic C1', 'source': 'synthetic support reaction record', 'downward_sign': 1, 'supported_beam_id': 'SUPPORTED', 'receiving_beam_id': 'SUPPORT'} |
| Reação de cálculo | 140.000000 kN; gamma_f aplicado=1.4 |
| 75% considerado | 105.000000 kN |
| fyd | 434.782609 MPa = 43.478261 kN/cm²; Concretopy Aco.fyd |
| Área total de suspensão | 2.415000 cm² |
| Comprimento e região | L=52.0 cm (h da receptora); [1.74, 2.26] m, simétrica no eixo 2,000 m |
| Maior cortante da região | 100.000000 kN; série assinada max; governantes/endpoints preservados no JSON |
| Taxa de suspensão | 4.644231 cm²/m |
| Cortante calculado antes do mínimo | 2.550011 cm²/m |
| Taxa mínima | 2.666704 cm²/m |
| Taxa total exigida | 7.194242 cm²/m = max(suspensão + calculado, mínimo) |
| Estribo fornecido | Ø8 c/12, dois ramos; 8.377580 cm²/m |
| Margem de área | 1.183338 cm²/m |
| VRd2 / Vsd | 574.970400 / 140.000000 kN |
| Espaçamento normativo | 12 cm ≤ 28.020000 cm |
| Resultado localizado | PASS; não aprova a viga globalmente |

Caso crítico: a parcela calculada 2,550011 é inferior ao mínimo 2,666704. A soma correta resulta em 7,194242 cm²/m, e não suspensão+governante (7,310935 cm²/m). Outro teste reduz a reação até o mínimo governar; parcela negativa de cortante não subtrai suspensão.

Controles independentes do exemplo:

| Controle | Estado |
|---|---|
| indirect_support_identification | PASS |
| total_support_reaction | PASS |
| reaction_nature | PASS |
| geometric_position | PASS |
| distribution_length | PASS |
| shear_diagram_coverage | PASS |
| suspension_component | PASS |
| shear_calculated_component | PASS |
| minimum_component | PASS |
| total_required_rate | PASS |
| provided_stirrup_area | PASS |
| maximum_code_spacing | PASS |
| effective_legs | PASS |
| usual_practices | PASS |
| drawing_coverage | PASS |
| diagonal_compression | PASS |

## V516/V517 — disponibilidade real e regressão

V516 e V517: SUSPENSION_REVIEW=INCONCLUSIVE e suspension_passes=null, sem ligações completas comprovadas nos arquivos disponíveis. A indicação gráfica N1 é registrada como possível evidência, não como prova isolada. As reações extraídas dessas vigas são reações delas nos pilares; não podem ser usadas como reação transmitida por outra viga sobre elas.

Dados necessários: identidade e geometria da apoiada; confirmação de transferência/aplicabilidade; reação TOTAL com natureza característica/de cálculo, combinação, direção e fonte; projeção documental do eixo no sistema físico da receptora. A inexistência de registros completos não prova inexistência de apoio indireto: inventário permanece incompleto. Nenhuma reação foi inferida de Vk.

Cortante independente segue global_shear_approval=null nas duas vigas pelas pendências de estribos nos vãos extremos; quatro faixas N13/N1 verificadas anteriormente e classificação N12 foram mantidas. N12 é negativa de laje adjacente e não fornece Asw/s. Nenhum arquivo/resultado histórico real foi regenerado.

## Estados e limitações

As faixas intersectadas são verificadas individualmente, sem compensação por média. Controles de cortante e exigência combinada coexistem. Falhas conhecidas de biela, área de cortante ou espaçamento permanecem FAIL mesmo sem reação/diagrama completo. Faixa descoberta, ramos ou função ambíguos não recebem crédito. Práticas usuais fora da preferência são REVIEW, não FAIL automático. Porta-estribos físicos de quatro ramos continuam independentes.

Balanço: L=h/2 conhecido, origem não confirmada; sem intervalo explícito rastreável, posicionamento inconclusivo. Não truncar/deslocar região para caber. Mudança de seção não autoriza seção uniforme inventada; múltiplos contextos/vãos ainda exigem entrada/resolução própria. Sobreposição de regiões de reações diferentes é registrada e não somada/ignorada; mantém INCONCLUSIVE salvo falha individual já provada. Inventário vazio só é NOT_APPLICABLE com prova de completude. Nenhuma aprovação global da viga.

## Decisões e referência normativa

engineer_confirmed_suspension_75_percent_reaction_v1; engineer_confirmed_suspension_symmetric_distribution_v1; engineer_confirmed_suspension_shear_without_minimum_v1; engineer_confirmed_suspension_total_minimum_governance_v1; engineer_confirmed_suspension_usual_stirrup_practices_v1. O item 18.3.6 da ABNT NBR 6118 foi referido pelo engenheiro. Não foi consultado o texto integral/edição aplicável nesta etapa; os critérios fornecidos são rastreados como decisões confirmadas, sem atribuir exigências adicionais inventadas à norma.

## Arquivos criados/alterados

Criados:

- tools/reinforcement_checks/suspension_review.py: interpretação/orquestração e resultados independentes.
- tools/reinforcement_checks/suspension_review.md: contrato de entradas/saídas.
- tools/reinforcement_checks/test_suspension_review.py: 68 testes de contratos, estados, regiões e regressões.
- .agents/skills/reinforcement-review/references/suspension-reinforcement-review.md: procedimento consolidado.
- analises/pranchas/validar_suspensao.py: reprodução sem alterar goldens.
- analises/pranchas/suspension_synthetic_fixture.json e suspension_synthetic_review.json: exemplo completo.
- analises/pranchas/V516_suspension_review.json e V517_suspension_review.json: auditoria real dos dados pendentes.
- analises/pranchas/suspension_review_preservation.json e suspension_review_validation.json: hashes e validação.
- .codex/analises/suspension_concretopy_api_audit.md e suspension_review_implementation.md: auditorias.
- Concretopy/tests/test_shear_components.py: 14 testes próprios de exposição/compatibilidade.

Alterados:

- .agents/skills/reinforcement-review/SKILL.md: roteamento após cortante.
- tools/reinforcement_checks/README.md: descoberta da nova ferramenta.
- Concretopy/concretopy/resultados.py: dois campos opcionais.
- Concretopy/concretopy/verificacoes/cortante.py: exposição das parcelas já calculadas.
- Concretopy/docs/api_publica.md: contrato aditivo.

## Validação

945 testes assistant aprovados (39 extrator_lst +30 beam_model +34 beam_mapping +842 reinforcement_checks); 68 novos testes de suspensão. Concretopy: 427 aprovados, incluindo 14 novos. quick_validate: Skill válida. 231 arquivos existentes protegidos idênticos; apenas os quatro arquivos autorizados/intencionais acima diferem do baseline (demais arquivos são novos). Comparação antiga/nova em 40 chamadas passou. Goldens positivos, negativos, cortante, resultados e relatórios históricos preservados. git diff --check passou nos dois projetos.

selected_solution=null e detailing_optimization=null. Nenhuma otimização, redesenho ou correção automática executada.
