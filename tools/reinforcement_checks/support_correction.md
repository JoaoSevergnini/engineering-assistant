# Correção de apoio positiva orientada pelo detalhamento

`support_correction.py` acrescenta hierarquia sem modificar `support_alternatives.py` ou Concretopy. Usa o avaliador local existente e verifica camadas/continuidade/flexão por regiões antes de recomendar uma candidata.

## Interfaces

- `transverse_fit(section,layers,api)` reutiliza mínimo de espaçamento e máximo uniforme Concretopy. Reporta geometria explícita; `diameters_mm` opcional permite conferir uma camada com bitolas distintas sem média, mas não habilita flexão dessa mistura.
- `configuration_from_bars(bars,x,label)` compõe camadas usando `flexure_regions.compose_layers` e centros explícitos. Camadas ausentes/mistas/sem centro bloqueiam a representação local.
- `check_longitudinal(bars,context,diagram,api)` usa `decompose_regions` e consultas `moment_at_x` nos limites/vértices de cada região; Concretopy para capacidades. Diagrama sem dados completos, intervalos ou hipóteses de seção ausentes deixam compatibilidade null. Rechecagem abrange todo domínio amostrado, sem extrapolação.
- `extension_candidates(bars,support_x,target_x,support_side="LEFT")` enumera 1..quantidade total por marca interrompida, conservando remanescente em intervalo original e camada/centro de origem. Uma marca por alternativa, sem generalização para várias interrupções simultâneas.
- `redistribution_candidates(...,series,max_steps=2,counts=(2,3))` espaço explícito de duas marcas/camadas. Primeira menor, segunda maior; preserva perfis longitudinais e reutiliza posições públicas Concretopy. Counts e passos são preferências de busca, não limites normativos.
- `evaluate_detail_candidate(...)` reconstrói apoio, recalcula contexto/d do vão para redistribuição, reavalia regionalmente e separa validade de preferência. Todas as respostas locais completas são mantidas. Prolongamentos têm prova de conservação de barras e comparação de capacidades.
- `correction_workflow(context,bars,diagram,api,redistribution_search=...)` existente → prolongamentos → redistribuições → próxima avaliação complementar. Não gera redistribuições quando existem prolongamentos adequados nem altera configuração existente válida. `selected_solution=None`.

## Entradas e saída

Reutiliza contexto do avaliador genérico, acrescido de `support_reference_x_m`, `extension_target_x_m` e `longitudinal_provenance` (seção resistente/diagrama/centros/fontes e hipóteses). Cada barra segue o modelo mapeado positivo: marca, bars, diameter_mm, vetor físico layers, face/function, x_start_common/x_end_common e d_cm explícito. Esforços já auditados/selecionados; dados originais não são mutados.

Propostas prolongadas conservam campos documentais como provenance histórica; `proposal_geometry`/`changes` identificam novo intervalo. Não geram novo C desenvolvido ou desenho da dobra. Para redistribuições, as duas composições e passos ficam explícitos.

Resultados: `existing`, `extensions`, `redistributions`, `original_composition`, `recommended_ids`, `next_step`, diagnósticos e `selected_solution`. Cada candidata conserva origem EXISTENTE/PROLONGAMENTO/REDISTRIBUICAO, alterações, support_check, fit por camada, longitudinal_check por região, métricas de d/x/z/As/lb/min/necessário/efetivo/margem/adicional, preservação, validade, recomendabilidade, razões e limites. `next_step=None` para pendências que impedem conclusão; não confundir com necessidade comprovada de grampos.

Folgas/pacotes/interferências/tolerâncias do nó não são integralmente certificados; `ready_for_detailing=False`. No novo wrapper, o cabimento simples é verificado; o campo de limitação transversal do resultado genérico é atualizado somente na cópia desta avaliação, sem modificar o avaliador ou goldens genéricos.

[Workflow da Skill](../../.agents/skills/reinforcement-review/references/positive-support-correction.md), [auditoria de primitivas](../../.codex/analises/support_correction_geometry_primitives_audit.md).

```powershell
python -B analises/pranchas/validar_v536_v565_correcao_apoio.py
python -B -m unittest discover -s tools/reinforcement_checks -p 'test_support_correction.py'
```

Orientação atual: LEFT/RIGHT relativo ao vão; enumeração RIGHT reutiliza a divisão física LEFT por transformação exclusivamente geométrica, sem transformar/selecionar esforços. Para apoio INTERMEDIATE, usar [support_anchorage](support_anchorage.md), que aplica A/C e controles próprios, sem o cálculo B de END.
