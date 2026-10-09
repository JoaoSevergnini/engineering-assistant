# Correção positiva no apoio orientada pelo detalhamento

Workflow confirmado pelo engenheiro em 06/10/2026. Consultar quando a ancoragem positiva em apoio extremo END, LEFT ou RIGHT, falhar. A [busca genérica](positive-end-support.md) é preservada como exploração numérica; isoladamente, não recomenda alteração de prancha.

## Sequência vigente

1. Identificar positivos chegando ao apoio e interrompidos no vão: marca, quantidade, bitola, camada física, centro, intervalo e fonte. Verificar a configuração EXISTENTE com demanda por pares, lb_ef geométrico, aderência e cenário de gancho conforme [apoio positivo](positive-end-support.md).
2. Conferir cabimento e compatibilidade regional com flexão positiva. Se atende, parar: `NENHUMA_CORRECAO`, sem gerar alterações.
3. Em armadura escalonada, procurar primeiro **PROLONGAMENTO** de barras existentes. Testar quantidades individuais de uma marca até sua quantidade total, conservando centros/bitolas e as barras não prolongadas. Registrar marca de origem, parcela prolongada, intervalo original/proposto e mudança de terminação. Não retirar capacidade das regiões originais do vão.
4. Recalcular camadas reais, flexão, d/x/z, al, demandas independentes A/B/C e ancoragem para cada proposta; conferir todas as camadas e regiões positivas. Se existem prolongamentos adequados, apresentá-los para decisão e não gerar redistribuições desnecessárias.
5. Somente sem prolongamento adequado, estudar **REDISTRIBUICAO** simples: primeira camada de bitola menor chegando ao apoio; segunda maior conservando perfil longitudinal. Série explícita/configurável, normalmente diferença de 1 ou 2 posições na série, `max_steps=2` configurável. Essa é preferência de detalhamento, não requisito da NBR. Registrar composição original/proposta, barras alteradas e regiões rechecadas. Recalcular também d do vão na composição proposta, sem preservar indevidamente o centroide antigo.
6. Sem solução simples comprovada, indicar `AVALIAR_ARMADURA_COMPLEMENTAR`. Para estudar grampos, seguir [procedimento complementar](positive-support-staples.md): quantidades/áreas/lb/comprimento, sem inventar distribuição. Não converter As_adicional automaticamente em detalhamento. Se a compatibilidade original está ausente ou a flexão original é insuficiente, indicar a pendência; armadura complementar de ancoragem não resolve automaticamente essa dependência.

## Cabimento confirmado e primitivas

Regra `engineer_confirmed_positive_bar_clear_spacing_v1`: **a_livre_min=max(2 cm,phi_cm)**. Largura interna considera b, cobrimento e Ø do estribo. A ferramenta reutiliza `concretopy.normas.espacamento_min_arm_long_viga` e `concretopy.detalhamento.arranjos.numero_barras_maximo_camada`. Com o parâmetro de compatibilidade padrão 16 mm, o termo de agregado da primitiva é 1,92 cm, não governante; não é adoção do agregado do projeto nem uma conferência normativa adicional. A [auditoria prévia](../../../../.codex/analises/support_correction_geometry_primitives_audit.md) documenta a compatibilidade e a dependência dos submódulos, não congelada na fachada pública.

Por camada, registrar largura disponível/necessária, bitolas físicas, folgas mínimas/adotadas e folga uniforme possível. Bitolas distintas não são substituídas por média: geometria é explícita, com maior mínimo exigido pelo par vizinho. Mistura de bitolas dentro de uma mesma camada resistente continua bloqueada pela representação de flexão atual. Camadas distintas podem usar bitolas distintas nas regiões do vão.

`cabimento_transversal=true/false/null`: falso rejeita; null audita sem recomendar. O controle simples de folgas não confere pacotes, tolerâncias, interferência detalhada com negativos ou cruzamentos no nó.

Posicionamento vertical: reutilizar a API pública `calcular_alturas_uteis_camadas` e centros auditados. Prolongar N3 não muda seu d de segunda camada. Redistribuir bitolas exige resolver novamente cada centro e o centroide pelo Concretopy; nunca usar bitola equivalente ou d antigo por conveniência.

## Compatibilidade longitudinal e decisão

Usar `flexure_regions.decompose_regions` e `MomentDiagram.moment_at_x`, sobre diagrama TQS previamente auditado. Verificar demanda nos vértices piecewise-linear e limites de cada região de composição, sem extrapolar, suavizar ou duplicar interpolação. Resistência exclusivamente por Concretopy. Se o chamador usa uma seção resistente uniforme em todo domínio amostrado, registrar essa hipótese; isso não comprova distribuição de estribos nos apoios.

Prolongamento preserva contagens/bitolas/centros e intervalos de toda barra original. Rechecar regiões e comparar capacidades originais/propostas. Redistribuição reavalia todas as regiões pertinentes, não somente pico; uma proposta localmente ancorável pode falhar na flexão positiva do vão.

Separar `technically_valid` e `recomendavel_como_correcao`. A segunda aplica também a hierarquia/preferência explícita, sem score. Ambas se referem às verificações modeladas. Todas conservam `ready_for_detailing=false` enquanto não houver revisão da dobra/interferências e aprovação do engenheiro; cenário de gancho válido não é inspeção automática. Não converter candidata recomendável para análise em prancha pronta.

## Ferramentas e goldens

[Contrato e implementação](../../../../tools/reinforcement_checks/support_correction.md), [fixture V536/V565](../../../../analises/pranchas/validar_v536_v565_correcao_apoio.py), [auditoria real](../../../../.codex/analises/V536_V565_detail_oriented_support_correction.md).

V536: N2 3Ø20 em primeira camada; prolongar 1, 2 ou 3 barras N3 Ø20 em segunda camada. Resultados devem ser calculados, sem forçar grampos para concordar com a preferência prática informada. Se o prolongamento simples passar, conservá-lo no relatório e registrar a decisão do engenheiro separadamente. V565: manter 3Ø20 existente se atender integralmente com lb_ef=21,5 cm.

Não alterar os goldens anteriores de escalonamento/apoio/busca genérica para executar esta análise. O fixture produz novas saídas específicas.

Para INTERMEDIATE, consultar [ancoragem em apoios](positive-support-anchorage.md): extensão reta antes de outras alterações; não importar grampos/gancho END automaticamente. A documentação histórica restrita ao lado esquerdo descreve a primeira versão, superada apenas em orientação por esta atualização.

Perfil vigente do motor de corre��es: consultar [correction_engine.md](../../../../tools/reinforcement_checks/correction_engine.md), se��o de decis�o de escopo mais recente. �rea corrigida e flex�o/distribui��o/escalonamento/continuidade s�o controles independentes. Pino, trajet�ria curva e interfer�ncia com armadura do pilar s�o n�o executados por decis�o de projeto; n�o s�o PASS nem bloqueantes. Cr�dito aos grampos exige modelo resistente e geom�trico compat�vel. Aprova��o final permanece do engenheiro.
