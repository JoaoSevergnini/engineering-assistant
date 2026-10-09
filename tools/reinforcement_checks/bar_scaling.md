# Escalonamento positivo dentro de um vao

Procedimento operacional da Skill: [positive-bar-scaling.md](../../.agents/skills/reinforcement-review/references/positive-bar-scaling.md).
Este documento conserva o contrato de integracao das ferramentas.

`bar_scaling.check_bar_scaling(detail, tqs, positioned, mapping, raw, api,
interrupted_mark=..., cut_side=..., scope=...)` orquestra
as regioes geometricas, o diagrama linear e o Concretopy local.
Nao implementa resistencia a flexao, fbd, lb ou al.

`check_scaling_event` e o nucleo para modelos ja auditados; recebe mapping,
resultado regional, MomentDiagram, selecao de cortante e API. O adaptador
publico acima deve ser preferido para entradas TQS. Nao modifica entradas.

## Contrato e escopo

Uma marca interrompida dentro do vao livre de um unico vao fisico mapeado,
flexao positiva, barras retas nervuradas horizontais tracionadas, sem ganchos,
soldas, forma deslizante ou compressao especial. Modelo de al: estribos
verticais e Vc=Vc0. `scope` exige todos esses campos e provenance; nao ha
flag capaz de habilitar automaticamente regimes fora do escopo.

`before` e a composicao do lado voltado para o pico; `after` e a composicao
imediatamente alem do evento no sentido do corte. Para direita, esquerda/direita;
para esquerda, direita/esquerda. Usam-se os interiores das regioes adjacentes,
sem epsilon e sem alterar a presenca fechada no ponto documental. Marcas,
camadas, faces, bitolas, intervalos e fontes ficam preservados.

A diferenca before-after deve conter a marca solicitada; outros terminos coincidentes
sao avaliados individualmente com after fisico comum, sem ordem de remocao. Nao admitir
marcas simultaneamente iniciadas. A composicao deve ser constante entre referencias e corte; a geometria
transversal deve ser constante no trecho correspondente dentro do vao livre. Variacoes e eventos adicionais nessa extensao
sao explicitamente bloqueados nesta versao. A marca interrompida deve cobrir
as referencias. Uma marca em varias camadas nao e suportada para aderencia.

A capacidade remanescente usa somente after, na geometria do evento. Centros
fisicos das camadas sao obtidos via `calcular_alturas_uteis_camadas` da
composicao before e fornecidos explicitamente ao Concretopy para after;
remover barras nao desloca verticalmente as que permanecem. Os bloqueios da
composicao existente (incluindo lacunas de camadas) continuam vigentes.

## Referencias e comprimentos

- `MomentDiagram.find_crossings(Mk_eq_remaining)` preserva todos os cruzamentos.
- Um pico positivo unico, com ramos estritamente crescentes e decrescentes,
  identifica a representacao unimodal simples. Pode estar em um endpoint
  quando existe ramo de queda no sentido do corte; nao se extrapola o diagrama.
  Sua localizacao em relacao ao vao livre fica registrada. Um pico dentro do
  apoio e somente uma referencia de esforcos, sem verificacao de ancoragem ou
  inferencia da geometria transversal no apoio.
- Selecao direcional: crescente a esquerda, decrescente a direita. Cruzamento
  alem do corte produz comprimento negativo e bloqueia, sem alterar x_end.
- Platos, picos multiplos, ramo nao unimodal, gaps, cruzamento coincidente ou
  ambiguo e ausencia de cruzamento nao aprovam. Mesmo capacidade suficiente
  em todo o ramo nao recebe x_nec artificial: diagnostico especifico e null.
- O pico e `piecewise_linear_positive_peak`, nao maximo estrutural exato.
- A: comprimento orientado entre cruzamento e corte >= al + 10 phi.
- B: comprimento orientado entre pico e corte >= al + lb basico.

Coordenadas em m, comprimentos em cm. Cruzamentos mantem a representacao
Decimal fornecida pelo diagrama; comprimentos derivados usam precisao 50.
Nao se arredonda para a comparacao. Os dois testes usam o mesmo al.

## Cortante, d e aderencia

`tqs_shear.shear_from_tqs` audita VGESFS, vao, rotulos originais **Q MX. e
Q MN.**, nivel model_input, unidade kN, valores raw e correspondencia das
positions. Ambas as envoltorias caracteristicas integram o maximo em modulo;
nao se escolhe Q MX. so porque o momento adotado e M MX.

`select_span_shear` seleciona todos os governantes discretos, inclusive empates
entre sinais/series. Nenhuma interpolacao nem discretizacao adicional.
Considera todas as secoes do vao fisico, incluindo as internas aos apoios;
nao extrapola do dominio amostrado aos eixos. Serie incompleta bloqueia al.
Regra: `engineer_confirmed_al_shear_selection_v1`.

A regra [engineer_confirmed_al_effective_depth_v1](al_effective_depth.md)
seleciona o centroide das barras tracionadas participantes da composicao
imediatamente antes do corte. Reutiliza `d_equivalente_cm`, `as_por_camada_cm2`
e `d_por_camada_cm` do resultado de flexao dessa regiao no Concretopy. Se nao
houver resultado regional, chama a mesma API para a composicao anterior com
os centros fisicos preservados. O resultado registra cada contribuicao e sua
provenance. Nao recebe d manual de barra, grupo remanescente ou outra regiao.
Sem centroide/composicao/modelo validos retorna `d_for_al_unresolved`.
Esta regra e exclusiva do escalonamento no vao; nao define d para apoio.

A regra [engineer_confirmed_bond_condition_v1](../../.agents/skills/reinforcement-review/references/bond-condition.md)
usa o centro fisico da barra interrompida, nao d_for_al. A referencia concentra
limites, fronteiras e escopo; `classify_bond` implementa a classificacao.

`calcular_ancoragem` recebe a bitola e a area da marca interrompida (Barra do
Concretopy). As calculada=As efetiva representa ancoragem integral em fyd,
sem reducao por excesso de aco; nao e dimensionamento da area necessaria.
Nao se fornece comprimento disponivel a essa API. O workflow usa **lb_cm**;
lb_nec, lb_min e atende permanecem separados e nao decidem a condicao B.

## Resultados e reproducao

`overall.scaling_passes` so e booleano quando todas as dependencias e as duas
condicoes estao resolvidas. False significa verificacao completa com falha;
null significa inconclusiva. Diagnosticos identificam codigo e dependencia.
Comparacoes parciais A/B podem estar resolvidas sem conclusao global; examinar
sempre `overall.complete` e diagnosticos.

Golden:

```powershell
python -B tools/reinforcement_checks/v1001_scaling.py --concretopy-root ../concretopy --output tmp/V1001_N3_scaling_check_review.json
python -B -m unittest discover -s tools/reinforcement_checks -p 'test_*.py'
```

A CLI audita hashes e rejeita saida sobre entradas/contextos. Admite apenas
uma diferenca de serializacao comprovavel por hash: CRLF -> LF, explicitada
em `mapping_input_audit`, conservando ambos os hashes. Nao aceita simples
igualdade aproximada ou alteracao de conteudo. APIs/assinaturas/hashes do
Concretopy ficam registrados. Entradas/contextos sao protegidos, mas um
arquivo de saida existente pode ser regravado. Usar uma saida separada em tmp
para reproduzir; nao apontar --output para goldens historicos.
Essa precisao documental corrige a afirmacao anterior "Arquivos antigos nao
sao sobrescritos", mais ampla que a protecao implementada pela CLI.

Nao verifica apoio, grampos, negativos, suspensao, minimo, cisalhamento,
confinamento, revisao PDF/TQS ou aprovacao global do elemento.

## Caso real com duas camadas

V536=V565: N3 reta interrompida a esquerda, segunda camada; permanece N2,
primeira camada. Uma dobra externa documentada da remanescente e aceita
somente se a projecao horizontal coincide exatamente com seu intervalo,
a dobra fica fora do vao livre e possui lado, direcao, comprimento e fonte.
A dobra nao recebe credito, reducao de lb nem verificacao de ancoragem.
A marca interrompida continua obrigatoriamente reta. A composicao nao pode
mudar entre corte e referencias, inclusive na parte fora do vao livre.
Fixture/reproducao: analises/pranchas/reproduzir_v536_v565.py; resultados
V536_N3_scaling_check.json e V565_N3_scaling_check.json.

Identidade compartilhada: [eventos longitudinais](../../.agents/skills/reinforcement-review/references/longitudinal-termination-events.md).
