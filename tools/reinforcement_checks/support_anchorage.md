# Contrato — ancoragem positiva em apoios

Usar `support_geometry.SupportGeometry` e `support_anchorage.check_support(context,bars,diagram,api,geometry=...,shear=...,generate_corrections=True)`.

A referência operacional das decisões está em [positive-support-anchorage.md](../../.agents/skills/reinforcement-review/references/positive-support-anchorage.md). Esta ferramenta orquestra; Concretopy calcula resistência, demanda A/B/C, ancoragem e al. Não há equações resistentes copiadas.

## Entradas

Geometria explícita: identificação de vão/apoio, LEFT/RIGHT, END/INTERMEDIATE, faces/eixo em m, largura em cm e provenance; `as_dict()` conserva direções. Aceitam-se aliases antigos left/right/extremo/intermediario somente nas fronteiras dos contratos legados. `SupportGeometry` rejeita faces/largura/eixo inconsistentes, intervalos invertidos e comprimentos negativos.

`bars` segue beam_mapping: função positive, face lower, mark/bars/diameter_mm/layers/d_cm/x_start_common/x_end_common/source. Manter os campos documentais intactos. A terminação explícita por lado pode ser fornecida em `termination_by_side` com `termination_provenance`; ausência de evidência permanece UNKNOWN. Continuações físicas são preservadas, sem regra nova de emenda.

`context` reutiliza seção/material/gammas/cover, seção/d do vão, Nd de cálculo, Mk negativo da seção terminal com fonte, hipóteses horizontal/sliding_formwork e provenance. INTERMEDIATE lê positivo/máximo diretamente do diagrama auditado, sem pares END. Para os controles sem positivo, `shear` é o resultado auditado de `shear_from_tqs` ou `select_span_shear` com as duas envoltórias, e `al_scope_confirmed=True` exige confirmação do evento de entrada na face/composição anterior. Sem confirmação ou cortante, calcular o restante e manter al dependente inconclusivo.

`correction_search`, quando fornecido, usa limites explícitos de `redistribution_candidates`: series, max_steps, counts. Não são limites normativos. END pode encaminhar ao correction_workflow existente; grampos continuam escolha explícita por `staple_workflow`, não consequência automática de As_adicional. INTERMEDIATE tenta primeiro própria extensão reta, depois geradores existentes de prolongamento e redistribuição, com chamadas novas e validação regional. Sem cabimento/compatibilidade comprovados, uma candidata não é recomendação pronta.

## Saída

Identidade/geometria, seção terminal, classificação, critérios e respostas integrais Concretopy, barras presentes/penetrantes/ancoradas, aderência física individual, terminação, lb básico/min/nec, penetração, controles e provenance, área suficiente, ancoragem longitudinal, pendências do nó e correções não selecionadas. `selected_solution=None`; `ready_for_detailing=False` enquanto o nó não for verificado.

Nos controles sem positivo, a raiz contém a regra mais exigente de cada família e `by_mark` com cada marca; `longitudinal_bars[].controls` é a auditoria individual completa. A posição final e empates estão por marca. lb_nec agregado somente para bitola/aderência uniformes; para outras composições não há distribuição silenciosa da demanda por camada. O lb básico individual não depende dessa redução.

False é falha executada; None é falta de regra/dado. Continuidade/gancho desconhecidos e momento positivo não máximo bloqueiam a conclusão de comprimento. A inexistência legítima de utilização total por capacidade superior à demanda inteira do ramo é NOT_APPLICABLE com passes=True somente para esse controle, sem ponto artificial.

## Execução e regressões

```powershell
python -B analises/pranchas/validar_v536_apoio_direito.py
python -B analises/pranchas/validar_v536_positivo_completo.py
python -B -m unittest discover -s tools/reinforcement_checks -p 'test_*.py'
```

Fixtures escrevem apenas suas saídas específicas/atual integrado. Arquivo `V536_positive_reinforcement_complete_before_support_generalization.json` preserva o integrado anterior. Não executar fixtures que regravem goldens individuais históricos durante esta validação.
