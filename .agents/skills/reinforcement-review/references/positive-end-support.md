# Armadura positiva em apoio extremo: verificação e alternativas

Workflow confirmado pelo engenheiro em 06/10/2026. Consultar após flexão/escalonamento no vão, para armadura positiva que realmente chega ao apoio END, LEFT ou RIGHT relativo ao vão. A generalização de orientação mantém os goldens reais à esquerda e acrescenta testes de contrato RIGHT; não aprova globalmente a viga. Para INTERMEDIATE, usar [procedimento específico](positive-support-anchorage.md), sem importar B1/B2 ou redução de gancho deste ramo.

## Responsabilidades e entradas

O engineering-assistant interpreta geometria/barras, seleciona esforços, monta alternativas e compara resultados. Concretopy calcula flexão, posições verticais pelo critério existente, demanda A/B/C, al limitado e ancoragem/lb/lb_min/lb_nec/As_corr/As_adicional. Não copiar suas equações nem contornar uma recusa da API.

Consultar [contrato das ferramentas](../../../../tools/reinforcement_checks/support_alternatives.md), [demanda Concretopy](../../../../../concretopy/docs/armadura_apoio.md), [ancoragem Concretopy](../../../../../concretopy/docs/ancoragem.md), [aderência](bond-condition.md), [leitura de prancha](beam-drawing-convections.md) e [sequência geral](beam-review.md).

Usar entradas previamente selecionadas/auditadas, com unidades/fontes: seção/cobrimento, largura longitudinal do apoio, materiais/gammas, positivos participantes e suas camadas, seção/d do vão, Mk negativo do apoio, máximo positivo do domínio amostrado adotado, cenário de gancho e Nd de cálculo quando aplicável. Não modificar automaticamente a seção/d do vão ao explorar uma configuração local de apoio: eventual alteração longitudinal da solução exige revisão própria no vão.

## Uso para correção de prancha — atualização de 06/10/2026

A busca genérica abaixo é preservada como ensaio/exploração local. Para recomendar
correção, seguir [positive-support-correction.md](positive-support-correction.md):
existente → prolongar barras → redistribuir → avaliar armadura complementar.
O novo workflow acrescenta cabimento simples e compatibilidade regional, sem mudar
os resultados do ensaio genérico ou certificar dobra/interferências complexas.

## Procedimento da exploração local

1. Identificar barras que chegam ao apoio usando seus intervalos mapeados, faces, função e camadas. Não incorporar barras que começam dentro do vão, negativas ou pele sem critério resistente próprio.
2. Determinar os esforços na seção/região explicitamente escolhida. V536/V565 usa S1 no eixo esquerdo por decisão do engenheiro; isso não é regra universal de seleção espacial nem máximo do vão do escalonamento.
3. Montar pares pelo procedimento `engineer_confirmed_end_support_effort_pairs_v1`: P1 Mk positivo com módulo da envoltória Vk mínima; P2 Mk=0 com Vk máximo em módulo no apoio selecionado. Sem momento positivo, omitir P1; não fabricar positivo. Conservar sinal original, série, seção/x e fontes. Os pares são decisão de engenharia, não transcrição da NBR nem prova de concomitância de casos de carga.
4. Calcular `lb_ef=L_apoio−cobrimento` pela decisão `engineer_confirmed_end_support_available_length_v1`. Manter separadamente projeção/posição efetivamente desenhada, desenvolvimentos e fontes. **A extremidade desenhada não substitui lb_ef geométrico.** Não somar o ramo vertical nem al ao comprimento desta API.
5. Verificar primeiro a configuração existente. Reconstruir as camadas físicas e chamar `calcular_armadura_positiva_apoio` independentemente para cada par. Selecionar a maior demanda entre chamadas, preservando empates e governantes A/B/C.
6. Verificar ancoragem dessa demanda com área real, bitola, aderência e gancho correspondentes. Registrar área, comprimento mínimo, comprimento necessário e área adicional separadamente.
7. Se a configuração completa falhar, explorar o espaço explícito configurável por `support_alternatives.explore_alternatives`. Sem geometria/entrada original resolvida, diagnosticar antes de buscar; se já atender, não gerar alterações desnecessárias.
8. Para **cada alternativa**, reconstruir camadas/posições/áreas e repetir todas as chamadas de flexão, apoio e ancoragem. Não reutilizar demanda, d, x, z, al ou lb da configuração anterior.
9. Apresentar alternativas válidas sem área adicional e motivos de rejeição. Preferir configurações simples e pouca área excedente, apresentando trade-offs. Não escolher silenciosamente uma solução final.
10. Somente depois avaliar a necessidade de armadura adicional específica, conforme [grampos complementares](positive-support-staples.md): **As_adicional não é automaticamente grampo**.

## Representação e bloqueios

Escopo inicial: mesma bitola nominal em todas as camadas de cada alternativa; quantidades inteiras positivas; camadas ordenadas da face tracionada para a comprimida. Não criar bitola equivalente. Posições podem ser explícitas ou resolvidas pelo Concretopy, com adesão explícita do chamador à convenção existente `concretopy_vigas_k5_k7`. A rotina não inventa regra de espaçamento ou cabimento.

Classificar aderência por **centro físico de cada camada**, segundo [regra confirmada](bond-condition.md), nunca pelo centroide global. Condições diferentes entre camadas ou bitolas mistas não são representáveis nesta ancoragem agregada: `NAO_AVALIAVEL_GEOMETRIA`, resultado inconclusivo. Posição ausente sem convenção autorizada, geometria inválida ou recusa do Concretopy também bloqueiam a candidata, com detalhe preservado.

Gancho válido é cenário explícito do chamador. V536 usa True/α=0,7 por decisão do engenheiro; não certifica automaticamente raio/pino, cobrimento local, confinamento, geometria completa ou tabela prática de dobra. Alterar bitola exige conferir novamente o gancho na revisão final.

## Resultados e decisão

`VALIDA_SEM_AREA_ADICIONAL` exige área suficiente, lb_ef≥lb_min e lb_ef≥lb_nec, `atende=True` e As_adicional=0. Falhas completas conservam `AREA_INSUFICIENTE`, `ANCORAGEM_INSUFICIENTE` e/ou `ABAIXO_LB_MIN`, sem esconder diagnósticos simultâneos. Configurações não avaliáveis têm `passes=null`; rejeições completas têm `passes=false`.

Ordenação de apresentação explícita, sem score: número de barras, camadas, área fornecida, excesso, margem de ancoragem (maior primeiro), bitola. A ordem não determina solução final. Todas as candidatas conservam `geometria_transversal_nao_verificada` mesmo quando o cálculo atende.

Rastrear composição, posições/áreas, flexão, d/x/z, pares e chamadas completas, governantes, al, aderência, gancho, lb/lb_min/lb_nec/lb_ef, margens, As_corr/As_adicional, diagnósticos, limitações e fontes/hashes/API.

## Goldens e limites

[Ensaio corrigido V536/V565](../../../../.codex/analises/V536_V565_left_support_anchorage_check.md): documental 21 cm; lb_ef geométrico 24−2,5=21,5 cm. Com 3Ø20 e cenário de gancho confirmado, V536 falha no comprimento e V565 atende pelo cálculo real. Valores são regressões, não regras por nome.

[Busca V536](../../../../.codex/analises/V536_support_alternatives.md) registra todas as alternativas e seus resultados. [Testes](../../../../tools/reinforcement_checks/test_support_alternatives.py) protegem recálculo integral e o controle V565.

Não implementa grampos, tabela/dimensionamento da dobra, espaçamento vertical de grampos, cabimento transversal completo, espaçamento livre, limites normativos de barras por camada, apoio direito, negativos, suspensão, cisalhamento completo ou aprovação global. Limites da busca são opções do chamador. Uma candidata numericamente válida ainda exige revisão geométrica e da solução longitudinal completa antes de detalhar.

A limitação de grampos acima descreve o avaliador genérico deste documento. A camada separada [support_staples](../../../../tools/reinforcement_checks/support_staples.md) agora estuda quantidade/área/comprimento sem alterar esse avaliador ou seus goldens; distribuição e detalhamento completo continuam pendentes.
