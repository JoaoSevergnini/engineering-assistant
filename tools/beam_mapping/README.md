# Mapeamento geométrico de vigas

Contextos confirmados de duas torres: `--support-context caminho.json` ou
`support_context=` na API. Declarar membros, apoios por lado, labels/candidatos
e evidências. Não se infere grupo usando `/`. O original documental e a resolução
ficam preservados; o beam_model não é modificado. Exemplo:
`analises/pranchas/V1001_V9001_support_context.json`.

Consome `longitudinal_beam_detail`, TQS consolidado original e uma cópia TQS
com `positions` produzida por `section_positions.py`. Não lê PDF/LST, não gera
positions, não interpola esforços nem executa verificações estruturais.
Somente biblioteca padrão Python.

```powershell
python tools/beam_mapping/map_beam.py analises/pranchas/V501_V503_beam_model.json analises/pranchas/V501_tqs.json analises/pranchas/V501_tqs_positions.json --related-model analises/pranchas/V541_tqs.json --related-model analises/pranchas/V542_tqs.json --output analises/pranchas/V501_beam_mapping.json
python -m unittest discover -s tools/beam_mapping -p "test_*.py" -v
```

API: `map_beam(detail, tqs, positioned, related_models=())` retorna novo objeto;
entradas não são alteradas. CLI registra caminhos e SHA-256 de todas as entradas
e rejeita saída sobre qualquer entrada.

Primeira versão admite um vão sem balanços, origem documental na face interna
esquerda, centímetros e sentido para a direita. Casos com múltiplos vãos são
rejeitados até existir política explícita de offsets globais. Apoios são
selecionados pela ordem `span.support_ids`, nunca pela ordem da lista de apoios;
nomes precisam corresponder aos nomes documentais do apoio esquerdo/direito.

Comprimento é selecionado das referências VGESFS existentes no consolidado;
larguras e DEPEV das referências RELDTFPS, inclusive alternativas documentadas
em warnings. A seleção é explícita em `selected_geometry_operands`, com unidade,
valor, pointer, relatório e linhas. Conflitos na própria fonte escolhida impedem
o mapeamento. Warnings originais e catálogos de fontes são preservados.

`x_common = x_detail_cm/100 + b_left_m/2`. Não há offset adicional DEPEV.
As duas faces direitas são preservadas. Comparação decimal dos valores
publicados: igualdade exata resulta em `exact`, qualquer diferença em `mismatch`.
Isso não constitui tolerância de engenharia nem critério de aceitação.
Geometria necessária ausente é rejeitada; intervalo de armadura ausente tem
status `unresolved` e cobertura null, distinto de intervalo conhecido vazio `[]`.

Cada posição longitudinal conserva os campos originais (marca, função, diâmetro,
quantidade, camadas, coordenadas em cm e fonte), acrescenta intervalo comum em m
e seções contidas no intervalo fechado. `covered_tqs_points` contém todos os
esforços discretos dessas seções, com quantity/envelope/stage/unit/section/position/
value/proveniência. Não há escolha de série governante. A comparação usa Decimal
dos números serializados, sem arredondar/snapping positions existentes.

`force_series` preserva integralmente séries posicionadas; `unmapped_tqs_series`
preserva séries do original sem correspondência posicionada. Não se atribui a
essas séries uma posição por analogia. `tqs_sections` não contém pontos novos.
Pele e regiões de estribos são transportadas em listas separadas; a cobertura
de estribos é somente relação geométrica de região, sem capacidade calculada.

`indirect_relations` transporta reações VGESFS de modelos relacionados cujo
apoio documental é a viga analisada. NUL no nome é desconsiderado na comparação;
registro original permanece intacto. Coordenada, IB e marca ficam null; relações
documentais do detalhamento ficam separadas em `drawing_indirect_supports`.
Nenhuma reação é atribuída a N7/IB1/IB2 por proximidade ou ordem.
