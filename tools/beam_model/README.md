# Modelo longitudinal do detalhamento

Transforma JSON documental `beam_reinforcement_drawing_interpretation`, versao 1.2,
em `longitudinal_beam_detail`, versao 1.0. Somente biblioteca padrao Python.
Nao acessa PDF ou LST e nao executa verificacoes estruturais.
Outros esquemas documentais exigem adaptador explicito; nao sao aceitos silenciosamente.

Executar a partir da raiz do repositorio:

```powershell
python tools/beam_model/consolidar_detalhamento.py analises/pranchas/V502_detalhamento_prancha.json --output analises/pranchas/V502_beam_model.json
python -m unittest discover -s tools/beam_model -p "test_*.py" -v
```

A entrada nunca e gravada. Saida com mesmo caminho/arquivo da entrada e rejeitada.
O SHA-256 do documental fica em `document_sha256`. Cada entidade possui
`source.document_model` e `source.json_pointer`, resolvido no arquivo documental.
Nao sao repetidos blocos de evidencias, classificacoes ou justificativas.

## Estrutura

- `beam`, `section`, `coordinate_system`: identidade, secao e origem documental.
- `supports`: apoios principais com largura e faces; natureza e vinculo desconhecidos ficam null.
- `spans`, `overhangs`: geometria independente da distribuicao de estribos.
- `longitudinal_reinforcement`: uma entrada por posicao, mesmo atravessando apoios.
- `skin_reinforcement`: posicoes separadas, barras por face e numero de faces.
- `stirrup_regions`: uma entrada por distribuicao; a mesma marca pode se repetir.
- `indirect_supports`, `suspension_reinforcement`: vigas apoiadas e associacoes documentadas.
- `anchorage_staples`: grampos preservados separadamente, sem verificar ancoragem.
- `sections`: observacoes locais dos cortes, sem extrapolar sua validade.
- `uncertainties`: codigos agrupados por entidades afetadas.

Comprimentos e coordenadas em cm; diametros em mm. `layers=[3,1]` significa
3 barras na primeira camada e 1 na segunda; `[0,1]` so na segunda.
O numero de faces da pele e a divisao exata da quantidade total pelas barras por face.
Nao se somam marcas de pele entre regioes diferentes.

As coordenadas usam exclusivamente os intervalos ja presentes no documental.
Na V502 a origem e a face direita/interna de V548 e x cresce para a direita.
Comprimento desenvolvido e comprimentos de distribuicao nao preenchem coordenadas
ou comprimentos geometricos ausentes. null significa desconhecido, nao zero.
A geometria herdada conserva as limitacoes da interpretacao documental original.

Funcoes longitudinais vem do campo `group`. Pele e grampos vem de suas categorias
documentais. Funcao de estribos exige campo explicito `function`; nao e deduzida da
bitola, espacamento ou ausencia de suspensao. Ramos podem vir da forma global somente
quando sua marca coincide. Tipos de apoio nao sao deduzidos de prefixos de nomes.

## API e limites

`transform(raw, document_model)` retorna um dicionario; `validate(model, raw)` verifica
invariantes e compara com a projecao permitida da origem. O argumento raw e necessario
para auditar fidelidade, alem da consistencia interna. A auditoria nao comprova a
correcao da leitura original da prancha.

`reinforcement_at(model, x_cm)` retorna marcas `present`, `absent` e `indeterminate`,
com `complete=false` quando existem extensoes indeterminadas. Considera intervalos
fechados de barras longitudinais e pele; nao inclui grampos. Trata exclusivamente
presenca geometrica: nao significa barra efetiva ou ancorada para resistencia.

A ausencia documentada de suspensao e representada por `detailed=false` e `marks=[]`.
Ausencia de informacao e null. Nao existem conclusoes sobre necessidade ou suficiencia.

## V502 e testes

Fixture: JSON documental existente em `analises/pranchas/`, sem modifica-lo.
Os testes verificam identidade/secao, geometria, N2 unica atravessando apoios,
camadas N3/N5/N7, pele separada, N9, corte, apoios indiretos, suspensao,
independencia entre vao e regiao de estribos, intervalos desconhecidos,
rejeicao de duplicatas/unidades/camadas invalidas, fidelidade e preservacao da entrada.

Incertezas preservadas: limites de diversas barras/grampos, posicao dos cortes,
identidade e posicao das vigas apoiadas, cobrimento, projecoes da secao, natureza e
vinculo dos apoios, espacamento vertical de pele, funcao dos estribos e associacao
dos grampos. Nenhuma delas e resolvida consultando outras fontes nesta etapa.

## Adaptador documental 1.1 (vao unico e vigas agrupadas)

`legacy_document.py` aceita o esquema anterior de vao unico, mantendo os JSON
Pointers no arquivo original. V501/V503 compartilham o modelo, com quantidades
por viga e pares de nomes de apoios sem correspondencia individual presumida.
A origem documentada permite posicionar as faces internas em 0 e no comprimento
livre documental; as faces externas ficam null porque `dimension_shown` nao
explicita a direcao longitudinal. As dimensoes escritas sao preservadas separadamente.

```powershell
python tools/beam_model/consolidar_detalhamento.py analises/pranchas/V501_V503_detalhamento_prancha.json --output analises/pranchas/V501_V503_beam_model.json
```

A revisao documental da V501/V503 identifica dois apoios indiretos: IB1 e o
contorno espacialmente associado a N7 e IB2 e o outro contorno. Esses IDs nao
indicam ordem longitudinal. N7 e `suspension`, por associacao documental,
e referencia IB1. Nome, coordenadas e limites das vigas apoiadas continuam null;
a regiao de estribos de 72 cm nao substitui a largura da viga apoiada.
A existencia de suspensao em IB2 permanece null, sem presumir ausencia.
O adaptador consome campos documentais; nao classifica pela bitola/espacamento.
Documentais antigos sem associacao continuam com observacoes nao resolvidas.

`stirrup_shape_observation` conserva os dois ramos desenhados e dimensoes da
forma comum, sem atribuir a cada marca uma associacao nao estruturada na fonte.
Corte A conserva as duas camadas inferiores e a associacao superior N1/N3.
Os testes adicionais usam o documental V501/V503 e preservam os testes V502.
