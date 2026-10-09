# Auditoria prévia — suspensão e API de cortante

08/10/2026. Consultados dimensionar_cortante_viga, ResultadoCortante, Aco.fyd, APIs de reforço de furos, mapeamento de relações indiretas e consolidação TQS de reações. ResultadoCortante expõe somente asw_por_s (governante), vc e vrd2. A suspensão da calculadora de furos é específica de furos e não representa reação de apoio indireto de viga: não deve ser reaproveitada como outra hipótese física.

Extensão autorizada exclusivamente para expor a parcela de cortante: dois campos opcionais asw_por_s_calculado e asw_por_s_minimo, cm²/m, sem mudar assinatura, ordem inicial, atributos ou números existentes. A parcela calculada é max(0, parcela resistente antes do mínimo): taxa física não negativa; valores negativos não podem reduzir a suspensão. A governante anterior permanece calculada exatamente como antes. Campos adicionais não participam da comparação dataclass, preservando igualdade dos três atributos históricos. Serialização é aditiva; os goldens históricos não serão regenerados.

O assistant utiliza Aco.fyd para a resistência de cálculo e aplica o procedimento expressamente fornecido: fração da reação / tensão, com conversão MPa para kN/cm². Não replica equações de cortante. As primitivas de biela, mínimo, espaçamento, flexão, ancoragem e al não serão alteradas.

Não foi consultado o texto integral da edição aplicável da ABNT NBR 6118 nesta tarefa. O engenheiro referenciou o item 18.3.6; os critérios de 75%, distribuição e combinação são registrados como decisões fornecidas, sem inventar prescrições adicionais.

Mapeamento existente identifica relações com uma reação reportada da viga apoiada apontando à receptora. Não seleciona coordenada ou comprova natureza/totalidade/combinação. TQS preserva valores max/min por relatório: não converter automaticamente em reação total ou combinação. V516/V517 contêm reações a pilares, que não são reações de outras vigas sobre elas. Indicação especial junto à N1 não identifica autonomamente todos os dados da ligação.
