# Altura util para al no escalonamento dentro do vao

Identificador: `engineer_confirmed_al_effective_depth_v1`.
Autoridade: decisao explicita de Joao Severgnini em 2026-10-05, nesta conversa.
Escopo: decalagem al em verificacao de escalonamento longitudinal no vao.
Nao estender automaticamente para futura ancoragem em apoio.

Utilizar a distancia da face comprimida ao centroide das barras longitudinais
tracionadas que participam da resistencia a flexao na composicao imediatamente
**antes** da interrupcao, no sentido analisado:

```text
d_for_al = sum(As_i * d_i) / sum(As_i)
```

As_i e a area da contribuicao tracionada i; d_i e a distancia do centro dessa
contribuicao a face comprimida. Conservar marcas, camadas, areas, posicoes,
composicao de referencia e provenance. Nao incluir armaduras negativas, pele,
grampos ou contribuintes que nao participam da flexao positiva analisada.

Reutilizar preferencialmente `d_equivalente_cm`, `as_por_camada_cm2` e
`d_por_camada_cm` retornados pelo Concretopy para a composicao anterior.
Se essa regiao nao tiver sido verificada por ausencia de demanda amostrada,
chamar a mesma API de flexao para essa composicao; nao fabricar solicitacao,
nao inferir d de outra regiao e nao duplicar resistencia ou posicionamento.

Todas as barras na mesma camada: o centroide coincide com d dessa camada.
Multiplas camadas: usar o centroide ponderado das areas, nao primeira/ultima
camada, barra interrompida isolada, remanescente isolada, h-c ou valor manual
de planilha. A selecao independe do d usado para a capacidade remanescente.

A API `calcular_al` recebe esse unico d explicito em todas as etapas.
O mesmo al alimenta A (al+10phi) e B (al+lb basico). Se composicao, geometria,
areas/centros ou modelo tracionado nao estiverem resolvidos, reportar
`d_for_al_unresolved` e manter inconclusivas as conclusoes dependentes.

Na V1001, imediatamente antes do termino direito de N3, N3+N5 formam 4Ø10
na primeira camada inferior. O resultado de flexao R3 do Concretopy fornece
As=3,141592653589793 cm2 e d_equivalente=68,5 cm. Essa e a correspondencia
fisica utilizada para d_for_al; a coincidencia com d de N3/N5 isoladas decorre
da camada unica, nao de uma regra por marca.

Implementacao: `bar_scaling.py`. Fonte da equacao do centroide: decisao do
engenheiro; calculo reutilizado: Concretopy flexao. A regra resolve a pendencia
de selecao de d identificada pela auditoria anterior, somente para este escopo.

Procedimento operacional e exemplos de uma/duas camadas:
[positive-bar-scaling.md](../../.agents/skills/reinforcement-review/references/positive-bar-scaling.md).
A classificacao de aderencia usa a posicao da barra interrompida, nao este
centroide: [bond-condition.md](../../.agents/skills/reinforcement-review/references/bond-condition.md).

Para controles longitudinais equivalentes de apoio INTERMEDIATE sem positivo, consultar [support_anchorage.md](support_anchorage.md): evento explícito de entrada na face interna e composição anterior, confirmação do chamador, máximo módulo das duas séries do vão. Esta extensão não altera o cálculo B dos apoios END nem cria regra de redução de ancoragem.
