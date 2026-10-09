# Exploração de armadura positiva no apoio extremo

`support_alternatives.py` é orquestração do engineering-assistant sobre as APIs públicas atuais do Concretopy. Não interpreta LST nem escolhe automaticamente região de apoio. Recebe contexto auditado e configurações físicas; não contém nomes de vigas/marcas ou números do golden em produção.

## Interfaces

- `available_length(L_apoio, cover, provenance)`: lb_ef geométrico segundo decisão do engenheiro; projeção documental permanece entrada de auditoria separada.
- `effort_pairs(Mk_positive_kncm, Vk_min_signed_kn, Vk_max_abs_kn, provenance)`: P1 positivo/módulo da envoltória mínima quando positivo existe; P2 zero/máximo módulo selecionado. Não garante concomitância.
- `generate_alternatives(diameters_mm, min_bars, max_bars, max_layers, position_rule=None, explicit_depths_cm=None, provenance=None)`: mesma bitola por configuração, partições ordenadas de quantidades por camadas. Não aplica limite normativo de barras/camada. Profundidades explícitas são mapa por bitola para centros ordenados. Sem posição ou convenção, conserva candidata não avaliável.
- `evaluate_configuration(context, configuration, api)`: posição Concretopy → flexão real → aderência por camada → chamadas independentes de apoio → maior demanda/empates → ancoragem com área real. Registra resultados completos, métricas, proveniência/API/hashes, diagnósticos e limites. Nunca reutiliza cálculos resistentes de outra configuração.
- `explore_alternatives(context, existing, api, search=...)`: verifica existente primeiro; busca somente se ela está completa e falha. Lista válidas por critérios objetivos documentados, com `selected_solution=None`.

## Dados

`configuration={id, layers:[{count,diameter_mm,d_cm}], position_rule, provenance}`. `d_cm` em cm da face comprimida. `position_rule='concretopy_vigas_k5_k7'` autoriza o posicionamento público existente; d explícito é preservado. Bitolas mistas e condições mistas de aderência são bloqueadas porque a ancoragem agregada atual não as representa.

Contexto: `support_side='LEFT'|'RIGHT'`, `support_type='END'` (aliases legados left/right/extremo aceitos), `horizontal=True`, `sliding_formwork=False`, `section={bw,h,cobrimento,diametro_estribo_mm}`, `support_length_cm`, `cover_cm`, `length_provenance`, `fck_mpa`, `fyk_mpa`, `gamma_f/c/s`, `mk_positive_max_span_kncm`, `mk_negative_support_kncm`, `d_span_cm`, `nd_tracao_kn`, `gancho_valido`, `pairs`, `provenance`. Opcionais: seção independente `section_span` e d' explícitos nas dimensões exigidas pelo Concretopy. Nd já é de cálculo. Todas as origens/interpretações de esforços pertencem ao chamador.

Unidades: cm, mm, cm², MPa, kN, kN.cm. Converter momentos TQS kN.m antes das chamadas, preservando original. Material e geometria do vão permanecem independentes da alternativa local.

## Resultado

`complete`, `passes` (null se inconclusivo), `status`, `diagnostics` cumulativos, `flexure`, `resolved_layers`, `bond_by_layer`, `states[{pair,result}]`, `governing_pairs`, `available_length`, `anchorage`, `metrics`, `api_provenance`, `limitations`. `VALIDA_SEM_AREA_ADICIONAL` cobre área/ancoragem desta rotina, não detalhamento pronto.

Sempre registra `geometria_transversal_nao_verificada` e `gancho_geometria_nao_verificada`. Recusas geométricas básicas do Concretopy são conservadas, sem afirmar que esses controles conferem espaçamento livre ou cabimento completo. Diagnóstico adicional de área não dimensiona grampo.

## Reprodução e regressões

```powershell
python -B analises/pranchas/validar_v536_v565_apoio_esquerdo.py
python -B -m unittest discover -s tools/reinforcement_checks -p 'test_support_alternatives.py'
```

O script é fixture real, não parser genérico. Escreve somente resultados de apoio autorizados; não regrava dados documentais ou goldens de escalonamento. Testes importam `load_case` sem escrever artefatos e comparam resultados recalculados às saídas persistidas.

[Procedimento da Skill](../../.agents/skills/reinforcement-review/references/positive-end-support.md) contém regras, preferências e limites; [Concretopy](../../../concretopy/docs/armadura_apoio.md) mantém toda a física.

Generalização de orientação: forças de cada apoio são selecionadas independentemente pelo chamador. Para INTERMEDIATE, utilizar [support_anchorage](support_anchorage.md), nunca este cálculo END como substituto.
