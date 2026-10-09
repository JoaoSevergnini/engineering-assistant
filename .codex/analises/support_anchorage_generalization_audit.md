# Auditoria — generalização da ancoragem positiva em apoios

Data: 06/10/2026. Objetivo: fechar orientação relativa ao vão e separar END/INTERMEDIATE, preservando integralmente o comportamento estrutural dos ensaios anteriores. Nenhuma solução de detalhamento foi selecionada.

## Fontes auditadas

AGENTS.md; reinforcement-review/SKILL.md; referências beam-review, convenções de prancha/TQS, positive-bar-scaling, positive-end-support, positive-support-correction, positive-support-staples e bond-condition; README e contratos de reinforcement_checks; flexure_regions, positive_flexure, moment_diagram, bar_scaling, tqs_shear e support_alternatives/correction/staples; regras al_shear_selection/al_effective_depth. Goldens e auditorias individuais V536/V565 de flexão/escalonamento, apoio, exploração, correção orientada e grampos; golden integrado anterior.

Concretopy local: documentação pública api_publica.md, armadura_apoio.md, ancoragem.md; implementações públicas de flexão, armadura_apoio, ancoragem e calcular_al/resultados. A API de apoio já aceita intermediario e desativa B; não foi encontrada lacuna determinística impeditiva. **Concretopy não foi alterado.**

## Arquitetura e contratos

`support_geometry.py`: SupportGeometry centraliza faces/eixo/largura, sentido para dentro do apoio/vão, distâncias em cm e coordenadas em m, penetração e término necessário. Sem equações resistentes. LEFT/RIGHT é relativo ao vão, não propriedade absoluta do apoio físico. Identidade e provenance são obrigatórias.

`support_anchorage.py`: uma orquestração comum identifica barras geometricamente presentes, declara terminação/continuidade, chama Concretopy e preserva respostas/critério governante. END encaminha ao avaliador existente. INTERMEDIATE possui os dois ramos confirmados. A/B/C, resistência, d/x/z, lb/lb_min/lb_nec, al e redução/inversão permanecem no Concretopy. Composições e consultas de regiões/crossings reutilizam as ferramentas existentes.

Correções END mantêm geradores/workflow anteriores, agora orientados LEFT/RIGHT. A transformação de coordenadas usada na enumeração RIGHT transforma somente geometria; **não espelha esforços reais**. As comparações de grampos conservam aço/comprimentos e aceitam a orientação nova. INTERMEDIATE tenta extensão reta própria, depois prolongamento físico de outras barras existentes e redistribuição configurada; recalcula com novas chamadas e validação regional. Não aplica grampos END automaticamente. Candidatas sem cabimento/compatibilidade comprovados não se tornam prontas para detalhamento.

`selected_solution=null`; inconclusivo permanece null. Área presente na face é distinta de área ancorada. Uma barra que termina exatamente na face tem penetração zero; a verificação geométrica falha, sem chamar a API inversa com comprimento zero. Uma barra que atravessa a face externa é continuidade física, não terminação, e recebe pendência de regra específica de continuidade/emenda.

## Decisões consolidadas e fontes normativas

| Contexto | Demanda | Comprimento/controles |
|---|---|---|
| END, LEFT/RIGHT | A/B/C, pares independentes já confirmados | lb_ef=largura−cobrimento; lb_nec e gancho válido conforme cenário |
| INTERMEDIATE com positivo terminal máximo | A e C pelo contrato Concretopy; B inaplicável | lb básico individual desde face interna, alpha=1 para reta, sem redução por área ou gancho |
| INTERMEDIATE com positivo terminal não máximo | A/C e valores de auditoria calculáveis | decisão exata de redução pendente; conclusão longitudinal null |
| INTERMEDIATE sem positivo terminal | C; sem B1/B2 | base + controle desde zero + controle desde utilização total, todos independentes |

A seção terminal é a última **no sentido do apoio**: primeiro ponto em x crescente para LEFT, último para RIGHT. Esta clarificação foi confirmada expressamente pelo engenheiro, sem extrapolar nem usar dados do outro apoio.

IDs de decisões: engineer_confirmed_support_side_orientation_v1; engineer_confirmed_intermediate_support_last_section_moment_v1; engineer_confirmed_intermediate_support_positive_max_basic_lb_v1; engineer_confirmed_intermediate_support_no_positive_moment_v1; engineer_confirmed_intermediate_support_base_penetration_30cm_v1; engineer_confirmed_intermediate_support_scaling_like_checks_v1.

Sem positivo: base=max(10phi_cm,min(largura_cm,30)); desde zero exigir al+10phi; desde Msk=Mk_eq da composição que chega exigir al+lb básico da própria barra. Seleção de referências reutiliza bar_scaling.locate_references, com candidatos integrais, ramo orientado e bloqueios existentes. Capacidade superior à demanda inteira do ramo => utilização total NOT_APPLICABLE, sem crossing fictício. Governa o término mais exigente; 30 cm não limita os controles adicionais.

Para al desses controles, a entrada na face interna é o evento analisado: composição tracionada imediatamente antes, do lado do vão, calculada pelo Concretopy. Essa definição não equivale a presumir o d de qualquer barra cortada isoladamente. O chamador confirma a equivalência semântica do evento com `al_scope_confirmed=True`; ausência de confirmação bloqueia al, não impede os demais cálculos. Vk é máximo módulo discreto das duas séries do vão, preservando domínio, pontos e empates; não B1/B2.

Fontes públicas Concretopy suportam a referência A/B/C ao item 18.3.2.4 da NBR 6118:2023 e os trechos fornecidos de aderência/ancoragem (9.3 e 9.4). A norma integral não foi consultada nesta etapa. Não se afirma uma nova auditoria independente desses itens. O mínimo 10phi informado pelo engenheiro é registrado como `engineer_provided_normative_minimum_10phi`, sem cláusula inventada. Seleção terminal, base preferencial de 30 cm, lb básico no máximo e composição dos controles são decisões/procedimentos do engenheiro, não transcrições da NBR.

## V536 — apoio direito P7A

A geometria vem do detalhamento/mapping; largura 120 cm e face externa são obtidas da fonte documental, não usadas para substituir a penetração real. A terminação direita reta de N2/N3 é cenário documental auditado; a dobra esquerda N2 é preservada na origem e não vira gancho fictício à direita.

| Grandeza | Resultado |
|---|---:|
| Tipo/lado relativo ao vão | INTERMEDIATE / RIGHT |
| Face interna / eixo / face externa | 3,060 / 3,660 / 4,260 m |
| Última seção amostrada | S13, x=3,276 m |
| Msk positivo terminal = máximo amostrado | 317,745266650 kN.m |
| Momento negativo terminal da série M MN. | −144,334274700 kN.m |
| Composição presente | N2 3Ø20, d=68 cm; N3 3Ø20, d=64 cm |
| Centroide da composição | d=66 cm |
| Término documental de ambas | 3,880 m |
| Penetração calculada desde face interna | 82,000 cm |
| Área efetiva na face | 18,849555922 cm² |
| Área requerida; critério governante | 17,751503903 cm²; A |
| lb básico individual, boa aderência | 55,071689104 cm |
| lb_min | 20,000 cm |
| lb_nec, auditoria agregada uniforme | 51,863572178 cm |
| Exigência utilizada | lb básico, não lb_nec |
| Margem longitudinal básica | 26,928310896 cm |
| Ancoragem longitudinal | true |
| Correção necessária / candidatas | false / nenhuma |
| Geometria transversal resolvida | false |
| Interferências do nó verificadas | false |
| Apoio completamente verificado | null |

Penetração calculada de coordenadas, não hardcoded. Boa aderência vem dos centros reais das camadas, não de função positive ou centroide global. Chamada de ancoragem reta alpha=1; nenhum benefício de gancho. Não se usa distância até o eixo, largura inteira ou lb_ef END como comprimento disponível desta comparação.

## Golden integrado e regressões

`V536_positive_reinforcement_complete_golden.json` agora contém resposta real do apoio direito. O integrado anterior foi arquivado intacto em `V536_positive_reinforcement_complete_before_support_generalization.json`; o relatório histórico anterior não foi reescrito.

SPAN: flexão/regiões amostradas e escalonamento N3 permanecem atendidos. LEFT END: N2 original permanece com lb_nec=24,203000350 cm > lb_ef=21,5 cm; As_adicional=1,184892006 cm². Prolongar 1/2/3 barras N3 permanece no relatório; grampos e busca genérica preservados, sem solução selecionada. V565 mantém seu controle original aprovado com 21,5 cm, sem correção desnecessária.

RIGHT: ancoragem longitudinal atende, sem correção. Não elimina unresolved_transverse_geometry. O trecho 3,276..3,660 m permanece não amostrado e sem extrapolação. O integrado continua com falha original esquerda e aprovação positiva global null.

145 arquivos previamente protegidos, incluindo toda base Concretopy e os goldens/relatórios históricos existentes, foram comparados por SHA256: **nenhuma alteração**. Somente o integrado atual foi excluído desse congelamento, conforme autorização de atualizá-lo. Fontes documentais originais não foram alteradas.

## Contradições e limites

As referências antigas declaravam escopo somente “apoio extremo esquerdo” e o integrado dizia RIGHT NAO_IMPLEMENTADO. Trata-se de escopo da primeira versão, superado por esta generalização autorizada; isso foi indicado nas referências, preservando auditorias históricas. Não surgiu conflito de resultado físico END ou mudança de decisão normativa.

Permanecem pendentes: comprimento reduzido no intermediário positivo não máximo; regras de gancho/continuidade/emenda para INTERMEDIATE; geometria transversal documental do apoio direito; verificação completa de nó, negativas, estribos/interferências, raios/pinos e tolerâncias; trecho final não amostrado; escolha final da correção esquerda. Não há aprovação global de viga. O cabimento uniforme de auditoria não sana a lacuna documental estrita.

## Arquivos desta etapa

Criados: tools/reinforcement_checks/support_geometry.py, support_anchorage.py, support_anchorage.md e test_support_anchorage.py; referência positive-support-anchorage.md; fixture validar_v536_apoio_direito.py; V536_right_support_anchorage_check.json; arquivo anterior do integrado; support_anchorage_generalization_validation.json; esta auditoria.

Alterados: support_alternatives.py/.md, support_correction.py/.md, support_staples.py; testes test_support_alternatives.py e test_v536_positive_complete.py; validar_v536_positivo_completo.py e seu golden atual; reinforcement_checks/README.md, al_shear_selection.md, al_effective_depth.md; SKILL.md e referências beam-review, positive-end-support, positive-support-correction, positive-support-staples e positive-bar-scaling. As demais alterações preexistentes da árvore Git não pertencem a esta tarefa.

## Validação

- Engineering-assistant: **449 testes aprovados**, sendo extrator_lst 39, beam_model 30, beam_mapping 34 e reinforcement_checks 346.
- **76 testes novos** de geometria/barras, orientação, critérios A/C/B inaplicável, ramo/crossings, controles básicos e al, pendências, correção reta e golden real. Não duplicam fórmulas resistentes; usam contratos e APIs reais. A rejeição histórica de support_side=right foi substituída por rejeição de lado inválido, por evolução deliberada do escopo.
- Concretopy local: **405 testes aprovados**, sem alteração.
- quick_validate da reinforcement-review: **Skill is valid!**
- git diff --check: sem erros; arquivos novos também conferidos quanto a espaços finais.
- Evidências: [validation JSON](../../analises/pranchas/support_anchorage_generalization_validation.json), tmp/support_suite_results.json e tmp/support_generalization_baseline.json.

Nenhum resultado físico dos goldens individuais mudou; o resultado novo é a verificação real do apoio direito no integrado.
