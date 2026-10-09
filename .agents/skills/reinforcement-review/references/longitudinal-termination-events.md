# Eventos de término de armadura longitudinal

Regra confirmada: `engineer_confirmed_independent_longitudinal_mark_termination_v1`.

Múltiplas barras podem possuir a mesma coordenada de término por simplificação do detalhamento. A coincidência geométrica não transforma essas barras em um único evento de interrupção. Cada marca deve ser verificada independentemente quanto à necessidade de prolongamento e ancoragem.

A identidade é `(bar_mark, cut_side, actual_end)`, não apenas x. Antes/depois são relativos ao sentido do corte. A composição anterior contém todas as barras fisicamente existentes imediatamente antes. A remanescente é a composição física imediatamente após **todos** os términos documentados naquela coordenada. Não manter outra barra coincidente ficticiamente na remanescente e não criar sequência ou prioridade de remoção. A identificação compartilhada está em `tools/reinforcement_checks/termination_event.py`.

Cada marca conserva quantidade, bitola, camadas, posição documental e provenance. O centroide anterior para al e a capacidade remanescente seguem as regras existentes; lb e 10φ pertencem à marca analisada. Marcas de mesma bitola podem apresentar requisitos iguais; isso não é imposto. Bitolas distintas podem produzir posições requeridas diferentes mesmo com posição desenhada igual.

Separar `provided_end_position_m` de `required_end_position_m`. Cada controle conserva referência, comprimento disponível/exigido, posição requerida e margem. A posição requerida global permanece null se algum controle não puder ser concluído. Nenhum crossing deve ser inventado. Antes do escalonamento junto a apoio intermediário, aplicar [classificação estrutural](intermediate-support-longitudinal-verification.md): prova de remanescente suficiente em todo o ramo e necessidade anterior conduz à ancoragem 1,0 lb desde a face. Sem essas provas, a ausência de crossing não aprova nem dispensa a marca. O núcleo SCALING isolado conserva seus bloqueios.

Entradas com reposição/início simultâneo, marca selecionada não efetivamente interrompida, identidade duplicada ou composição/geometria não representável continuam bloqueadas explicitamente. Esta generalização não resolve hipóteses físicas ausentes nem altera resistência, interpolação, orientação, aderência, al ou lb.

Aplicar junto aos procedimentos [positivo](positive-bar-scaling.md) e [negativo](negative-longitudinal-review.md). Regressão real: V516/V517, N8 e N9 em 12,840 m; detalhes numéricos no relatório correspondente.
