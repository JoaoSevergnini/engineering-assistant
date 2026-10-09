# Escalonamento de armadura longitudinal positiva no vão

Procedimento operacional consolidado em 05/10/2026 a partir da implementação
validada e dos goldens V1001, V536 e V565. Regra de workflow:
`engineer_confirmed_positive_bar_scaling_v1`. Não é transcrição normativa.
Não ampliar o escopo nem alterar primitivas para completar um caso não suportado.

## Leitura e responsabilidades

Consultar este procedimento quando uma marca positiva termina dentro do vão,
depois da verificação regional de flexão e antes da ancoragem nos apoios.
A sequência completa está em [beam-review.md](beam-review.md).

| Assunto | Referência operacional |
|---|---|
| Leitura de marcas, cotas, camadas e grupos | [Convenções de prancha](beam-drawing-convections.md) |
| Geometria, fontes TQS e interpolação | [Semântica TQS](tqs-beam-data.md) |
| Vk de todo o vão | [engineer_confirmed_al_shear_selection_v1](../../../../tools/reinforcement_checks/al_shear_selection.md) |
| Centroide anterior para al | [engineer_confirmed_al_effective_depth_v1](../../../../tools/reinforcement_checks/al_effective_depth.md) |
| Centro da barra interrompida para aderência | [engineer_confirmed_bond_condition_v1](bond-condition.md) |
| Contrato das ferramentas | [README](../../../../tools/reinforcement_checks/README.md), [bar_scaling.md](../../../../tools/reinforcement_checks/bar_scaling.md) |
| Primitivas e unidades | Concretopy local: [API pública](../../../../../concretopy/docs/api_publica.md) e [ancoragem/decalagem](../../../../../concretopy/docs/ancoragem.md) |

O engineering-assistant interpreta, mapeia, seleciona composições/referências/Vk/d,
compõe os comprimentos e relata diagnósticos. Concretopy calcula geometria das
camadas, áreas, resistência à flexão, fbd, lb e al. Não reproduzir suas equações
na skill ou em cálculos alternativos para contornar uma recusa da API.

## 1. Preparar as entradas

1. Conferir a geometria e identificar um único vão físico sem balanços,
   com apoios/faces conhecidos e mapeamento compatível. Usar
   [beam_model](../../../../tools/beam_model/consolidar_detalhamento.py),
   [beam_mapping](../../../../tools/beam_mapping/map_beam.py) e os modelos TQS
   raw, consolidado e posicionado produzidos por
   [extrator_lst](../../../../tools/extrator_lst/section_positions.py).
2. Interpretar positivos, preservando marcas, quantidades, bitolas, face inferior,
   índices físicos das camadas, formas, intervalos e fontes. Não usar comprimento
   desenvolvido de barra dobrada como projeção longitudinal. Grupos de vigas
   compartilham desenho, mas cada membro usa sua identidade e seus esforços.
3. Construir regiões com `flexure_regions.decompose_regions` e verificar flexão
   com `positive_flexure.check_positive_flexure`, conforme o README das ferramentas.
   Não transformar regiões sem demanda amostrada em capacidade aprovada.
4. Selecionar uma marca reta interrompida e `cut_side="left"` ou `"right"`.
   O evento deve estar estritamente entre as faces internas e dentro do domínio
   amostrado de momentos. Manter seu x documental, sem ajustar a seção TQS,
   apoio, estribo ou zero do diagrama. Registrar as origens e a tradução do mapping.

Escopo atual: positivo, seção retangular, barra interrompida horizontal nervurada
tracionada, uma marca por evento, sem gancho/solda/compressão especial/forma
deslizante; estribos verticais e Vc=Vc0. Confirmar ou registrar a origem das
hipóteses, sem apresentar ausência documental como inspeção da execução.
Uma marca interrompida distribuída em várias camadas não é suportada.
Camadas com bitolas distintas na mesma camada ou lacunas de índices são
bloqueadas; não criar uma barra equivalente nem renumerar as posições físicas.

**Exceção já validada para a remanescente:** uma dobra externa ao vão livre
pode ser conservada apenas como contexto, com segmento horizontal documentado,
projeção exatamente igual à extensão em x, lado/direção/comprimento da dobra e
fonte. A dobra deve ficar na face interna ou para fora do vão livre no lado
correspondente. A marca interrompida continua reta. Registrar
`external_bends_not_checked`; não dar crédito de ancoragem nem reduzir lb.
Isso não habilita a verificação de barras dobradas/ganchos nos apoios.

## 2. Determinar o evento e as composições

Usar os interiores das duas regiões adjacentes ao evento, sem epsilon.
A presença fechada das barras no ponto documental permanece preservada.

| Lado do corte | Extremidade física usada | composition_before | composition_after |
|---|---|---|---|
| right | x_end da barra | lado esquerdo, voltado ao pico | lado direito, além do corte |
| left | x_start da barra | lado direito, voltado ao pico | lado esquerdo, além do corte |

`interrupted` identifica a marca solicitada dentro de `before − after`;
`remaining = after`, após todos os términos documentados na coordenada. Seguir
[eventos independentes](longitudinal-termination-events.md), sem ordem de remoção.
Marcas simultaneamente iniciadas continuam fora do escopo. Antes/depois são relativos ao sentido do corte, não à ordem
absoluta de x. Conservar barras e fontes, não somente uma área agregada.

## 3. Capacidade da armadura remanescente

Chamar a API pública `Concretopy.verificar_flexao_viga_retangular` com **somente
after**, na geometria do evento. Reutilizar os centros físicos obtidos para
before e informar esses d ao Concretopy: remover uma marca não desloca as barras
que permanecem. Obter `MRd_remaining` e `Mk_equivalente_remaining`.

No JSON, os campos são `remaining_capacity.MRd_knm` e
`remaining_capacity.Mk_equivalent_knm`. Concretopy retorna kN.cm; o adaptador
converte para kN.m dividindo por 100. O γf vem da fonte auditada; não comparar
Msk com MRd diretamente. Exigir capacidade positiva e hipótese resistente válida.
A capacidade anterior fica como auditoria e para o centroide de al; **não localiza
x_nec**. Ductilidade e mínimo são diagnósticos próprios, não aprovação global.

## 4. Diagrama, pico e x_nec

`moment_diagram.diagram_from_tqs` audita a série característica positiva adotada
**VGESFS/M MX.**, com 13 seções, positions existentes, unidade kN.m e nível
`model_input`. Usar interpolação linear apenas entre pontos consecutivos válidos.
Sem extrapolação, suavização, conexão sobre gaps ou discretização artificial.
A verificação regional de flexão permanece discreta; a interpolação é a camada
específica usada para localizar as referências do escalonamento.

Encontrar **todos** os cruzamentos `Msk(x)=Mk_equivalente_remaining` com
`MomentDiagram.find_crossings`. Selecionar pela geometria do ramo:

- right: ramo decrescente à direita do pico, percorrido para a direita;
- left: ramo crescente em x à esquerda do pico, percorrido para a esquerda.

`x_nec` é onde a remanescente passa a ser suficiente nesse percurso. Não escolher
primeiro/último cruzamento global. Conservar candidatos, pontos-base, segmentos,
coordenada decimal e motivo da seleção.

Registrar `piecewise_linear_positive_peak` com x, Msk, seção e provenance.
É o máximo da representação adotada, **não o máximo estrutural exato**. O modelo
atual exige pico positivo único e ramos estritamente crescentes/decrescentes
onde existem. Pode ser interno ou endpoint com ramo de queda no sentido do corte.
O evento deve estar do lado correspondente do pico, não sobre ele.

Se o pico estiver dentro de um apoio, preservar a localização como referência
de esforços, sem inferir detalhamento transversal nem verificar ancoragem nesse
apoio. A barra deve cobrir as referências; a composição before deve permanecer
constante entre referências e corte, inclusive fora do vão livre. A geometria
transversal deve ser constante no trecho correspondente dentro do vão livre,
e resolvida/igual dos dois lados do evento.

Platô, múltiplos máximos, ramo não unimodal, gaps, cruzamento coincidente,
ambiguidade ou ausência de cruzamento bloqueiam a conclusão. A implementação
não cria x_nec quando a remanescente é suficiente ou insuficiente em todo o ramo:
registrar `remaining_sufficient_entire_branch` ou
`remaining_insufficient_entire_branch`, mantendo o resultado inconclusivo.
Não selecionar outro ramo ou deslocar a extremidade para evitar comprimento negativo.

## 5. Selecionar Vk, d, al e lb

Aplicar as referências específicas da tabela inicial, que são as fontes das
regras completas, sem substituí-las por valores dos exemplos:

- **Vk:** `tqs_shear.shear_from_tqs` audita **Q MX. e Q MN.** e seleciona
  `max(abs(Vk_i))` de todo o vão físico amostrado. Inclui pontos internos aos
  apoios; não extrapola aos eixos. Em segmento linear, o máximo módulo ocorre
  nos endpoints: não interpolar nem criar amostras para esse máximo.
  Conservar todos os empates, série, seção, x, sinal, magnitude e fontes.
- **d para al:** centroide por áreas das barras tracionadas participantes
  **imediatamente antes** do evento, segundo `al_effective_depth.md`.
  Reutilizar áreas/posições/centroide do Concretopy; não usar automaticamente
  a barra cortada, a remanescente, primeira/última camada ou outra região.
  Sem geometria/modelo/centroide válido, `d_for_al_unresolved`: conservar
  grandezas independentes e bloquear somente as conclusões dependentes.
- **al:** `Concretopy.calcular_al`, com Vk característico em módulo, d selecionado,
  seção/material/coeficientes correspondentes. Usar **`al_cm` final limitado**,
  não `al_base_cm`; preservar Vsd, Vc0, base, limites e branch retornados.
- **Aderência:** usar o centro da **barra interrompida**, segundo
  [bond-condition.md](bond-condition.md). Não confundir seu d físico com d_for_al.
- **lb:** `Concretopy.calcular_ancoragem` com bitola/aderência/material da
  **interrompida**. No workflow atual, As calculada=As efetiva=área dessa marca
  obtida via `Barra`, para ancoragem integral em fyd, sem redução por excesso.
  Não fornecer comprimento disponível à primitiva. Utilizar **`lb_cm` básico**,
  não lb_nec, lb_min ou redução por dobra; `anchorage_result.atende` não decide B.

O mesmo al do evento alimenta A e B. Não recalcular al em x_nec, corte ou pico.
As regras de Vk/d deste escalonamento não definem a futura ancoragem em apoio;
a região espacial de apoio ainda precisa de procedimento próprio.

## 6. Comparar as duas condições independentes

Coordenadas comuns em m; comprimentos em cm; bitola em mm:

```text
phi_cm = phi_mm_interrupted / 10
ten_phi_cm = 10 * phi_cm

right: L_available_A = (x_bar_end - x_nec) * 100
       L_available_B = (x_bar_end - x_decay_start) * 100
left:  L_available_A = (x_nec - x_bar_start) * 100
       L_available_B = (x_decay_start - x_bar_start) * 100

L_required_A = al_cm + ten_phi_cm
L_required_B = al_cm + lb_basic_cm
passes_A = L_available_A >= L_required_A
passes_B = L_available_B >= L_required_B
```

`x_decay_start` é o `piecewise_linear_positive_peak` selecionado. Comprimentos
negativos indicam inconsistência e bloqueiam. Conservar a coordenada decimal do
cruzamento e comparar sem arredondamento editorial. Reportar A e B separadamente,
com referência, disponível, parcelas, exigido e resultado.

## 7. Executar e interpretar o resultado

Entradas: `detail` (beam_model), `tqs` consolidado, `positioned` TQS,
`mapping` geométrico, `raw` TQS e `api` do Concretopy local que exporta calcular_al.
Preferir o adaptador público existente, importado de `tools/reinforcement_checks`:

```python
from bar_scaling import check_bar_scaling

result = check_bar_scaling(
    detail, tqs, positioned, mapping, raw, api,
    interrupted_mark=mark, cut_side=side, scope=scope,
)
```

Não há CLI genérica em bar_scaling.py. `scope` deve explicitar os campos do
contrato, com tipos corretos e provenance das hipóteses:

```python
scope = {
    'flexure': 'positive', 'horizontal': True, 'hooks': False,
    'welds': False, 'special_longitudinal_compression': False,
    'sliding_formwork': False, 'ribbed': True,
    'vertical_stirrups': True, 'vc_model': 'Vc0',
    'provenance': evidence_of_scope,
}
```

A importação deve apontar explicitamente para a biblioteca local atual, conforme
o README. O adaptador reutiliza flexão/regiões, diagrama e cortante auditados.
`check_scaling_event` é o núcleo para entradas já auditadas; não usá-lo para
contornar validações TQS. Ao persistir resultado, registrar caminhos/hashes das
entradas e implementação/API; escrever saída separada, sem sobrescrever fontes
ou goldens. O adaptador em memória não substitui a auditoria de hashes do chamador.

| Estado | Significado |
|---|---|
| `scaling_passes=true` | Dependências resolvidas, sem diagnósticos bloqueantes, A e B atendem |
| `scaling_passes=false` | Verificação completa, ao menos uma condição falha |
| `scaling_passes=null` | Inconclusiva por entrada, regra, geometria ou modelo pendente |

Conferir `overall.complete`, os resultados individuais e `diagnostics`.
Uma comparação parcial A/B pode estar resolvida sem conclusão global.
Não converter null em reprovação nem ocultar uma dependência pendente.

## 8. Rastreabilidade mínima da entrega

Entregar resultado auditável com barra/lado/extremidade documental e comum;
composição before/after/remaining, marcas/bitolas/camadas/faces/intervalos/fontes;
MRd/Mk remanescente e resposta/chamada de flexão; diagrama, pico, todos os
cruzamentos, bases, x_nec e razão da seleção; ambas as séries de Vk e todos os
governantes/empates; centroide anterior e contribuições de d; centro da barra e
aderência; chamadas/respostas completas de al/ancoragem; comprimentos A/B,
parcelas/referências/resultados; conclusão, diagnósticos e provenance.

Distinguir geometria calculada pelo critério de camadas do Concretopy de cotas
lidas no PDF. Cobrimento TQS não confirma execução. Preservar diferenças de
revisão, conflito de materiais/geometria e origens das hipóteses. Os dados
primários/documentais não são alterados para obter um resultado favorável.

## 9. Exemplos e regressões, não regras por identificador

| Golden | Corte/composição | Diagrama | d_for_al | Escalonamento |
|---|---|---|---|---|
| V1001 / N3 | direita; antes N3+N5, depois N5; uma camada | dois cruzamentos globais, descendente selecionado; pico interno | 68,5 cm | true |
| V536 / N3 | esquerda; antes N2+N3, depois N2; duas camadas | um cruzamento; pico no endpoint direito | 66 cm | true |
| V565 / N3 | mesmo desenho; esforços próprios | um cruzamento; pico no endpoint direito | 66 cm | true |

Em V536/V565, N2 tem d=68 cm, N3 d=64 cm e áreas iguais: centroide 66 cm.
Não generalizar esses valores. Detalhes completos ficam nos relatórios e JSONs:
[V1001](../../../../.codex/analises/V1001_N3_scaling_check.md),
[V536/V565](../../../../.codex/analises/V536_V565_N3_scaling_check.md),
[JSON V1001](../../../../analises/pranchas/V1001_N3_scaling_check.json),
[JSON V536](../../../../analises/pranchas/V536_N3_scaling_check.json),
[JSON V565](../../../../analises/pranchas/V565_N3_scaling_check.json).

Regressões existentes: [test_bar_scaling.py](../../../../tools/reinforcement_checks/test_bar_scaling.py)
e [test_v536_v565_scaling.py](../../../../tools/reinforcement_checks/test_v536_v565_scaling.py).
Reproduzir testes sem regravar goldens. Fixtures de caso real não são interfaces
genéricas nem autorização para modificar os artefatos históricos.

## 10. Limites da conclusão

Bloquear entradas/modelos inconsistentes, hipóteses não suportadas, capacidade
remanescente inválida, composições/posições desconhecidas, mudanças de configuração,
marca sem cobertura das referências, Vk/d/aderência/al/lb não resolvidos,
referências ambíguas e intervalos/comprimentos inconsistentes, conforme os
códigos e dependências retornados pela implementação. Não inventar fallback.

Esta etapa **não verifica** ancoragem nos apoios, grampos, negativas, suspensão,
cisalhamento completo, armadura mínima, barras comprimidas, benefício de
ancoragem de ganchos/dobras, reposições simultâneas, confinamento ou
aprovação global da viga. A regra de d vale somente para escalonamento no vão.
**Uma barra pode atender ao corte no vão e falhar na ancoragem em um apoio.**
Prosseguir depois com essa verificação própria, sem declarar a viga aprovada.

O procedimento próprio de ancoragem em apoio agora está em [positive-support-anchorage.md](positive-support-anchorage.md). Esta referência de corte no vão continua sem aprovar apoios; as reutilizações de Vk/d para controles equivalentes INTERMEDIATE exigem o evento explicitamente definido naquela referência.
