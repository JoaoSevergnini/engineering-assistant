# Revisão operacional de pavimento — Etapa 1.1

Para pavimentos completos, usar obrigatoriamente `tools/reinforcement_checks/floor_review.py` e o [contrato operacional](../../../../tools/reinforcement_checks/floor_review.md).

Seguir extração documental → reconciliação de detalhamento/cortes/tabela → modelo físico pela forma → associação ao eixo comum existente → camadas → preflight por controle → verificadores existentes → diagnóstico consolidado. Forma, detalhamento e TQS são obrigatórios. Fonte indisponível não significa informação ausente na prancha; ausência exige evidência de exame da região relevante.

Texto próximo às barras tem prioridade na distribuição em camadas; corte é complementar e divergências ficam conflitantes. Sem indicação explícita após exame, usar primeira camada como `INFERRED_EXPLICIT_CONVENTION`, critério do escritório. Antes da resistência, verificar cabimento conjunto das marcas com a rotina existente. Distribuição impossível permanece incompatível, sem redistribuição inventada.

Mudanças de seção, desníveis, faces, pilares, balanços e transições devem ser associados ao eixo físico existente a partir da forma. LST pode validar/complementar; distribuição de estribos não prova posição. Sem posição comprovada, registrar a cota/esclarecimento necessário na forma e impedir somente verificações dependentes. Não fabricar seção média, coordenadas de esforço, ausência de aço ou conformidade normativa.

Usar regras/verificadores já existentes para flexão, ancoragem, escalonamento, continuidade, cortante e suspensão. Manter envoltórias TQS. Adaptadores ausentes são pendências; scripts históricos não substituem a entrada protegida. Não modificar Concretopy, métodos resistentes, PDFs nem produzir propostas nesta etapa.

Consultar [relatório](../../../../analises/etapa1_1_integracao/relatorio_etapa1_1.md) e executar `python analises/etapa1_1_integracao/validate_stage.py` para regressão. A comparação real distingue extração histórica e comprovação nova da forma.
