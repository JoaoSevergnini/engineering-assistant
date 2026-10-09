# Ancoragem positiva em apoios: orientação e tipo

Procedimento confirmado pelo engenheiro em 06/10/2026. Executar depois da revisão de geometria, regiões resistentes, flexão positiva e escalonamento no vão. A ancoragem não substitui essas verificações. Usar [contrato da ferramenta](../../../../tools/reinforcement_checks/support_anchorage.md).

## Contrato e geometria

Declarar `span_id`, `support_id`, `support_side=LEFT|RIGHT`, `support_type=END|INTERMEDIATE`, faces interna/externa, eixo, largura e fontes. O lado é relativo ao vão; um apoio intermediário pode ser RIGHT para um vão e LEFT para o seguinte. `SupportGeometry` centraliza distâncias e posições necessárias, com coordenadas em m e comprimentos em cm.

```text
LEFT:   apoio <--- | face interna | vão
RIGHT:  vão       | face interna | ---> apoio
```

Identificar as barras positivas que vêm do vão e alcançam a face interna pelos intervalos reais. Registrar marca, quantidade, bitola, camada/d, área, intervalo, penetração e origem. Chegar exatamente à face produz área presente, mas penetração zero; não é área ancorada. Atravessar a face externa identifica `CONTINUES_THROUGH_SUPPORT`, sem criar uma regra de emenda ou aprovação da continuidade. Distinguir terminação `STRAIGHT`, `HOOK` e `UNKNOWN`; uma dobra do lado oposto não prova silenciosamente a terminação deste lado. Usar evidência documental explícita.

## END — preservar o workflow existente

Consultar [apoio extremo](positive-end-support.md), [correção](positive-support-correction.md) e, quando o cenário for decidido, [grampos](positive-support-staples.md). Continuam válidos A/B/C, pares independentes de esforços previamente selecionados pelo assistant, `lb_ef=largura−cobrimento`, aderência física, cenário de gancho válido, lb_nec e cálculo inverso. LEFT/RIGHT não muda as equações. **A seleção dos esforços do outro lado deve ser feita sobre seus próprios dados; nunca espelhar esforços reais.**

Verificar existente antes de buscar alterações. Prolongamento, redistribuição e grampos usam a infraestrutura já validada, com recálculo completo e sem seleção automática. Os goldens reais END permanecem V536/V565 à esquerda; RIGHT também possui testes de contrato/simetria.

## INTERMEDIATE — esforços e demanda

`engineer_confirmed_intermediate_support_last_section_moment_v1`: usar a seção **terminal no sentido do apoio** existente no diagrama: último ponto em x crescente para RIGHT, primeiro para LEFT (clarificação expressa do engenheiro). Não extrapolar para o eixo nem usar seção do outro apoio. Preservar seção/x/Mk e fonte. O máximo considerado é o máximo positivo **amostrado**, não o máximo estrutural exato.

Chamar `calcular_armadura_positiva_apoio(tipo_apoio='intermediario')`. Concretopy fornece A quando há positivo e C independente conforme contrato atual; B é não aplicável. O Vk=0 dessa chamada é parâmetro sem uso para B, não uma declaração de cortante físico nulo. Não usar B1/B2 de END neste ramo. Registrar demanda, área efetiva e governantes.

### Com momento positivo

A seção terminal define a demanda; **a face interna** define a referência de ancoragem, para dentro do apoio.

Se o momento da seção terminal for o maior positivo amostrado, aplicar `engineer_confirmed_intermediate_support_positive_max_basic_lb_v1`: penetração de cada barra reta ≥ seu **lb básico**. Recalcular lb pela própria bitola/aderência via Concretopy. Alpha=1; não reduzir por excesso de área nem por gancho. Registrar lb_min/lb_nec separadamente como auditoria; não governam esta regra. Para composições de bitolas/aderências diferentes, a redução agregada de lb_nec não está definida, mas o lb básico individual continua calculável.

Se existir positivo, mas não for o máximo, calcular demanda, capacidade, lb básico e penetração, retornando `intermediate_positive_nonmaximum_length_rule_unresolved`. A regra exata de redução não está confirmada. Não aprovar ou gerar correção baseada em comprimento inventado.

### Sem momento positivo

`engineer_confirmed_intermediate_support_no_positive_moment_v1`: demanda por C; nenhuma chamada B1/B2. Para cada barra reta, executar três controles independentes:

- `RULE_BASE_SUPPORT_PENETRATION`: `max(10phi_cm, min(largura_apoio_cm,30))`, desde a face interna. `engineer_confirmed_intermediate_support_base_penetration_30cm_v1`. 30 cm limita apenas a preferência de levar à face externa; não limita os demais controles nem o comprimento final.
- `RULE_ZERO_MOMENT_AL_PLUS_10PHI`: desde o zero do ramo correspondente, exigir al+10phi.
- `RULE_FULL_UTILIZATION_AL_PLUS_LB`: desde Msk=Mk_equivalente da composição que chega ao apoio, exigir al+lb básico da própria barra.

Os dois últimos seguem `engineer_confirmed_intermediate_support_scaling_like_checks_v1`. Reutilizar `bar_scaling.locate_references` e `MomentDiagram.find_crossings`: todos os candidatos conservados, ramo orientado, sem extrapolação, platôs/múltiplos picos/ambiguidade bloqueados. Capacidade estritamente superior a toda demanda do ramo significa controle de utilização total `NOT_APPLICABLE`, não um crossing fabricado. Ausência de zero/dados continua inconclusiva.

Para al, consultar [Vk](../../../../tools/reinforcement_checks/al_shear_selection.md) e [d](../../../../tools/reinforcement_checks/al_effective_depth.md): máximo módulo discreto das duas envoltórias no domínio físico amostrado do vão, não pares END. Usar o centroide Concretopy da composição tracionada imediatamente antes da entrada na face interna. Neste evento de apoio, não há perda de barras nessa entrada: a composição presente do lado do vão alimenta o cálculo; nenhuma regra para outra composição/corte é inferida. O chamador deve confirmar explicitamente essa equivalência em `al_scope_confirmed=True`; caso contrário, bloquear somente os controles dependentes de al. Preservar esta definição do evento na auditoria. Usar al final limitado, não al_base.

O término necessário é o mais exigente no sentido do apoio, preservando todos os controles e empates. Não limitar esse término a 30 cm. Se ultrapassar a face externa, preservar a informação e exigir tratamento específico de continuidade; não aprovar emenda automaticamente.

## Correção, conclusão e limites

Correções somente após falha completa da configuração original. INTERMEDIATE: tentar primeiro prolongamento reto da própria barra; depois prolongar outras barras existentes coerentes; depois redistribuição limitada quando necessária. Recalcular demanda, capacidade e comprimentos e revalidar todas as regiões positivas pelo workflow existente. Não reutilizar automaticamente grampos/gancho de END. `selected_solution=null` até decisão do engenheiro.

`longitudinal_anchorage_passes`: true quando área e controles aplicáveis resolvidos atendem; false quando completos e falham; null quando há pendência real. Separar `transverse_geometry_resolved`, `node_interferences_verified` e `support_verified`. Um resultado longitudinal true não resolve estribos, negativas, dobras/pinos, interferências, tolerâncias nem aprova o nó/viga.

As fontes Concretopy registram A/B/C como referência ao item 18.3.2.4 da NBR 6118:2023 e lb/aderência nos trechos fornecidos. A norma integral não foi consultada nesta consolidação. O 10phi informado pelo engenheiro recebe `engineer_provided_normative_minimum_10phi`, sem atribuição de cláusula não auditada. Seleção terminal, limite-base de 30 cm, regra de lb básico no máximo, controles combinados e hierarquia de correção são decisões de engenharia, não transcrições normativas.

## Goldens

[V536 direita — fixture](../../../../analises/pranchas/validar_v536_apoio_direito.py): P7A, INTERMEDIATE/RIGHT, N2/N3 retas, S13 máximo positivo amostrado. Geometria transversal documental continua pendente. [Auditoria da generalização](../../../../.codex/analises/support_anchorage_generalization_audit.md) e [golden integrado atual](../../../../analises/pranchas/V536_positive_reinforcement_complete_golden.json). Os relatórios históricos e goldens individuais de apoio esquerdo, escalonamento e grampos permanecem preservados.
