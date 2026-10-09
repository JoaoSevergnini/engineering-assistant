# Apoios indiretos: planta, relação LST e reação

A geometria da planta identifica encontros e posições; os LST da viga apoiada confirmam a direção de transferência e a reação daquele apoio. Não decidir direção por altura, largura, continuidade ou aparência. Cruzamento gráfico não comprova apoio nem igualdade de cotas.

`tools/beam_mapping/indirect_supports.py` consome modelos do consolidador existente (`lst_relations`) e encontros explicitamente associados à planta (`associate`). Não introduz parser especulativo. Fontes e variantes max/min dos relatórios reais permanecem separadas. Metadados devem comprovar natureza, totalidade, convenção de sinal, caso/combinação e seleção de envoltória. Não somar casos distintos nem estimar reação a partir do cortante.

Entrada de encontro: `beams`, `supported_beam`, `supporting_beam`, `supported_beam_support_id`, `point` (duas coordenadas físicas), `axis_position_m` na receptora, `same_elevation_confirmed` e `source`. A associação à planta é interpretação explícita, verificada contra a direção documental; não constitui direção inferida graficamente. Tolerâncias, extração automática CAD e projeção de eixos permanecem fora desta etapa.

Metadados de reação são associados pela chave `(supported_beam, support_id, file)`: `source`, `is_total`, `nature` CHARACTERISTIC/DESIGN, `load_case`, `downward_sign`, `selected_envelope` max/min. Múltiplas observações exigem `governing_selection_source` comprovando a seleção; as demais observações continuam no resultado. Ausência/contradição resulta INCONCLUSIVE.

A leitura da planta DIFERENCIADO foi adiada expressamente pelo engenheiro nesta execução. Registrar a pendência; não apresentar o inventário LST como inventário completo de encontros geométricos do pavimento. `analises/pranchas/indirect_supports_lst_inventory.json` é um inventário documental, sem liberação para dimensionar suspensão.

Somente uma associação CONFIRMED pode ser preparada para `suspension_review`; são necessários ainda geometria/seção da receptora e da apoiada, aplicabilidade, domínio físico, diagrama de cortante e estribos reais. Um registro CONFIRMED não aprova suspensão: consultar [procedimento de suspensão](suspension-reinforcement-review.md). Geometria ausente impede posicionar x±h/2; não substituir por seção TQS, pilar ou face.
