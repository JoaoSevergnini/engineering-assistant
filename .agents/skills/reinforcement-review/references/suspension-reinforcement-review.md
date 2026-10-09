# Revisão independente de armadura de suspensão

Executar após [cortante](shear-reinforcement-review.md), com `tools/reinforcement_checks/suspension_review.py`. Verificar o detalhamento existente; selected_solution e detailing_optimization permanecem null. Não modificar o resultado independente de cortante ou concluir aprovação global da viga.

## Ligação e reação

A receptora é a viga de suporte; a apoiada transmite a reação. Identificar ambas, fonte confiável de transferência e aplicabilidade, geometria e projeção do eixo apoiado no sistema físico da receptora. Uma interseção ou estribo especial não comprova apoio indireto. `connections_from_mapping` reutiliza relações documentais do beam_mapping, sem selecionar max/min, completar x ou inventar reação.

Exigir reação TOTAL da viga apoiada sobre a receptora, fonte/atestação de totalidade, combinação, unidade kN, natureza CHARACTERISTIC/DESIGN e convenção explícita de sinal descendente. Preservar observação original e fontes; não usar reações da própria receptora nos pilares como entrada. Reação parcial, natureza/combinação desconhecidas, levantamento/uplift sem regra ou direção não comprovada -> INCONCLUSIVE. Conversão de unidades da fonte ocorre na normalização documental existente e deve ser rastreada, nunca presumida.

`engineer_confirmed_suspension_75_percent_reaction_v1`: considerar 75% da reação total de cálculo. Para Rk, majorar por gamma_f uma vez; para Rd, não majorar novamente. Concretopy `Aco.fyd(gamma_s)` fornece a tensão; converter MPa para kN/cm² por fator 0,1. Área em cm² = 0,75 Rd / fyd(kN/cm²). O assistant aplica o procedimento fornecido e não copia as equações de cortante do Concretopy.

## Distribuição física

`engineer_confirmed_suspension_symmetric_distribution_v1`: em região intermediária, L=h TOTAL da receptora, em cm; limites físicos em m: x_eixo ± h/200. Exigir fonte da projeção física do eixo, sem trocar por face/pilar/seção TQS. Região na extremidade em balanço: L=h/2, mas origem ainda não confirmada. Sem intervalo explícito fornecido com fonte, posicionamento e verificação regional são inconclusivos; a ferramenta não o inventa.

Reutilizar faces comprovadas de `shear_coverage` e geometrias mapeadas; para situação especial, exigir domínio físico explícito e fonte. Não truncar ou deslocar região que atravessa apoios, limites de vão ou mudança de seção. Uma análise parcial pode registrar falhas conhecidas, sem comprovar a região completa. Contextos de múltiplos vãos/seções precisam tratamento explícito; não aplicar uma seção fictícia comum.

Taxa de suspensão em cm²/m = área(cm²)/L(cm)*100. Área total e taxa não são a mesma grandeza.

## Cortante e combinação

Pesquisar maior |Vsk| de toda a região com `ShearDiagram.maximum`: ambas as séries originais da receptora, endpoints interpoláveis e vértices, sinais e todos os governantes. Sem extrapolação ou interpolação por gaps. Região incompleta mantém INCONCLUSIVE para dependências regionais; falha comprovada nos dados conhecidos continua FAIL.

Usar `design_shear` com o mesmo contexto/material/modelo/d da revisão independente e a API pública Concretopy. `ResultadoCortante.asw_por_s_calculado` é a parcela física de cortante antes do mínimo, limitada a zero; `asw_por_s_minimo` é o mínimo; `asw_por_s` é o governante histórico. Campos ausentes não autorizam substituir a parcela calculada pelo governante.

`engineer_confirmed_suspension_shear_without_minimum_v1`: somar suspensão à parcela calculada, não à governante. `engineer_confirmed_suspension_total_minimum_governance_v1`: taxa exigida = max(suspensão + cortante calculado, mínimo). Preservar quatro taxas e a chamada do Concretopy. Concretopy mantém todas as equações resistentes; exposição dos componentes é extensão aditiva autorizada, sem mudar os critérios anteriores de cálculo.

## Estribos reais e estados

Particionar a região nos limites reais das faixas; verificar cada subintervalo, sem médias compensatórias. Reusar check_drawn_region para área da própria bitola e ramos, espaçamento normativo, prática usual e porta-estribos. Asw/s fornecida é de estribos comprovados da viga, não de N12/negativa de laje adjacente. Peça ambígua ou ramos desconhecidos não fornecem crédito silencioso. Não inventar faixa em intervalo descoberto.

`engineer_confirmed_suspension_usual_stirrup_practices_v1`: reusar Ø5/6,3/8 usuais, espaçamento de seleção prática ≥8 cm e quatro ramos em viga com largura >40cm como prática usual, separadamente do smax normativo e compatibilidade física do porta-estribo. Ø maior/s<8 podem resultar REQUIRES_ENGINEERING_REVIEW, sem FAIL estrutural automático. Nenhuma seleção de solução executada.

Controles independentes: ligação; totalidade/natureza da reação; posicionamento/comprimento; cobertura TQS; área/taxa de suspensão; parcela calculada/mínima/total; área fornecida; smax; ramos; prática usual; cobertura documental; biela/porta-estribo. FAIL comprovado prevalece sobre INCONCLUSIVE. PASS estrutural com prática fora do usual conserva revisão de engenharia. Múltiplas reações com regiões sobrepostas: registrar a sobreposição, não somar nem ignorar; conclusão INCONCLUSIVE até regra de combinação, mantendo eventual FAIL comprovado individual.

Inventário vazio não prova inexistência: NOT_APPLICABLE apenas com inventário completo e fonte. V516/V517 são regressões, não hipótese automática de apoio indireto. Sem todos os dados, registrar pendências em resultado próprio, preservando cortante e longitudinais.

## Fontes normativas e exemplos

O engenheiro referenciou o item 18.3.6 da ABNT NBR 6118. Texto integral/edição aplicável não foram consultados nesta implementação; as decisões acima foram expressamente fornecidas pelo engenheiro e não recebem atribuição de cláusulas adicionais inventadas. Conferência normativa integral e particularidades de aplicação não comprovadas são pendências explícitas.

Exemplo completo reproduzível: `analises/pranchas/suspension_synthetic_fixture.json` -> `validar_suspensao.py` -> `suspension_synthetic_review.json`. São dados SINTÉTICOS, nunca reação do projeto real. Resultados V516/V517 têm auditoria de disponibilidade em arquivos próprios; não se alteram goldens históricos.

Antes de calcular suspensão, consultar [associação planta/LST/reação](indirect-support-identification.md). A leitura da planta pode permanecer pendente sem inventar a posição do encontro.
