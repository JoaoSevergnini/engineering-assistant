# Auditoria — primeira revisão longitudinal negativa

Data: 2026-10-06. Implementação orientada por decisões do engenheiro, mantendo Concretopy e resultados positivos existentes.

## 1. Pedido e esclarecimentos

Implementar interpretação negativa, resistência regional, cortes sucessivos, término no vão, porta-estribo, continuidade e cenários geométricos de nó/balanço. O engenheiro esclareceu: no término para dentro do vão, al+lb parte do crossing da capacidade da composição levada ao término; na extremidade livre do balanço, a sobra é a perna vertical da dobra. Nenhuma seleção de correção foi autorizada automaticamente; selected_solution permanece null.

## 2. Fontes lidas

AGENTS.md; reinforcement-review/SKILL.md; referências beam-review, beam-drawing-convections, tqs-beam-data e procedimentos positivos de escalonamento/apoio/aderência/correção; regras al_shear_selection/al_effective_depth; ferramentas flexure_regions, positive_flexure, bar_scaling, moment_diagram, tqs_moments/tqs_shear, support_anchorage, support_geometry e support_correction; auditoria anterior de generalização de apoio e goldens positivos. Concretopy: documentação pública api_publica, ancoragem, hipóteses/limites, flexão/camadas, materiais e al; implementação pública e testes pertinentes. Skill-creator foi aplicada à atualização documental.

Auditaram-se dados negativos de V1001, V501/V503, V536/V565 e V502. V536 não foi forçada como golden negativo: a N1 tem dados geométricos longitudinais não suficientemente resolvidos para esse ensaio. V1001 possui N7/N8 documentadas, duas camadas e um corte simples verificável.

## 3. Arquitetura escolhida

Generalização controlada dos motores existentes. Defaults continuam POSITIVE. A vista negativa transforma M em −M, preservando o original; nunca usa abs(M) para converter o ramo de sinal oposto em demanda negativa. O componente longitudinal interpreta faces/camadas/eventos; o componente de detalhes aplica políticas específicas. Concretopy calcula áreas, posições convencionais, capacidade, fbd, lb e al. Não foram criados motores duplicados negative_flexure ou negative_bar_scaling.

## 4. Reutilização

flexure_regions: composições e intervalos por função/face. support_correction: configuração e flexão regional em limites/vértices. moment_diagram/tqs_moments: auditoria, consultas e vista de sinal. bar_scaling.locate_references: candidatos, pico e ramo. support_geometry: orientação comum e apoio físico. support_anchorage: distâncias, posições finais e controles tri-state. tqs_shear: máximo absoluto discreto com empates preservados. APIs públicas Concretopy, sem equações resistentes novas no assistant.

## 5. Camadas e resistência

Negativa: TOP tracionada, BOTTOM comprimida; d desde a face inferior. Coordenadas documentais TOP/BOTTOM/COMPRESSION_FACE são convertidas explicitamente. Ordem física não depende da marca. Marcas com várias camadas e três ou mais camadas são suportadas; retirada de uma camada não reposiciona as restantes. Convenção automática exige origem/ordem confirmada e usa calcular_alturas_uteis_camadas; mistura de bitolas não representável sem centros explícitos fica pendente.

A flexão é regional, consultando extremos, mudanças de composição e vértices do diagrama linear. Resultados preservam MRd, Mk equivalente, momento original e magnitude, utilização e validade. Não demonstram armadura mínima ou aprovação global.

## 6. Interrupção e término

SCALING: al+lb desde o pico/início da decadência e al+10φ desde o crossing da capacidade remanescente. Cada corte recalcula antes/depois/capacidade, incluindo interrupções sucessivas. SPAN_TERMINATION: al+lb desde o crossing da capacidade levada ao término e al+10φ desde o zero negativo. O contrato inicial é uma marca por evento, inclusive multilayer. Não há extensão adicional arbitrária.

Todos os crossings são preservados. Seleção por ramo/lado, sem extrapolar. Platô, ramo indefinido, crossing ausente/ambíguo bloqueiam dependência. No término, capacidade estritamente superior a todo o ramo sem ponto de plena utilização identifica somente esse controle como NOT_APPLICABLE, com razão explícita; zero continua obrigatório. Não converter pendência em falha ou aprovar sem entradas.

## 7. al, Vk e aderência

Seleção de Vk e centroide anterior reutilizam o procedimento positivo para evento de corte no vão; a autorização de contexto é explícita. Usar ambas as envoltórias no domínio físico amostrado, sem criar discretização. d para al vem do centroide Concretopy imediatamente antes do evento e da face comprimida correta. Usar al final limitado.

A política negativa confirmada impõe POOR independentemente de y. Concretopy calcula lb básico da própria barra, sem redução por área/gancho. lb continua disponível se a geometria vertical estiver pendente; al/conclusão dependentes permanecem null.

## 8. Porta-estribo e pele

Porta-estribo exige função/provenance e ausência de demanda negativa. Cruzamento espacial com estribos aplica max(6,3 mm, bitola regional); mudanças regionais retornam decisão pendente. Não usar máximo global. Pele exige indicação explícita ou fonte equivalente; função isolada sem prova não basta. UNKNOWN permanece UNKNOWN.

## 9. Continuidade

Apoio intermediário: RIGHT do vão esquerdo e LEFT do direito, faces comuns e identidades físicas compatíveis. Exigir documentação, bitola, trajetória, camada e intervalo cruzando apoio. Receber controles independentes calculados com os diagramas próprios. Extensões podem diferir. Não assumir emenda, atravessamento, identidade ou aprovação pelo simples desejo de continuidade.

## 10. Nó extremo e balanço

Nó em pilar: ensaio reto integral com lb básico, sem crédito de redução. Sem espaço, a proposta geométrica de perna é min(h−c−φ_estribo,2lb); resistência da dobra continua null. Não inventar C, pino, raio ou α=0,7. Esse ensaio não dimensiona completamente o nó.

Balanço único engastado em pilar confirmado: reta 1,5lb básico, sem redução por área; impossível geometricamente leva a estudo da dobra, ainda sem aprovação resistente automática. Não generalizar para balanço contínuo, Gerber, console ou outro apoio. Na extremidade livre, verificar a perna de dobra h−2c−φ_estribo com valor documental; conservar controles longitudinais independentes, sem somar projeções ortogonais.

## 11. Regras e normas

IDs confirmados: engineer_confirmed_reinforcement_layer_face_order_v1; engineer_confirmed_negative_beam_reinforcement_poor_bond_v1; engineer_confirmed_negative_al_same_as_positive_v1; engineer_confirmed_negative_reinforcement_span_termination_v1; engineer_confirmed_beam_stirrup_holder_diameter_v1; engineer_confirmed_negative_intermediate_support_extension_v1; engineer_confirmed_negative_end_frame_node_bend_v1; engineer_confirmed_single_cantilever_negative_anchorage_1_5lb_v1; engineer_confirmed_cantilever_free_end_negative_tail_v1.

Essas políticas são decisões do engenheiro, não transcrições da NBR. O modelo resistente/aderência/ancoragem é o das APIs documentadas do Concretopy. A referência antiga cita NBR 6118:2023, item 18.3.2.1, mas o texto normativo integral não foi consultado nesta tarefa; não se afirma conformidade normativa completa nem se inventam novos itens.

## 12. Golden real V1001

Fontes read-only: beam_model/mapping, TQS original/posicionado/raw e contexto material/seção da auditoria positiva anterior. Seção 19×72 cm, C40/CA50, cobrimento 2,5 cm, estribo Ø5 e gammas 1,4/1,4/1,15. Ramo negativo direito conectado ao terminal amostrado: 5,4186667 a 7,936 m, preservando o ponto adjacente positivo para interpolar o zero. Não extrapolado até eixo/face.

N7 = 3Ø16 na primeira camada, intervalo 4,59–8,34 m, d=68,2 cm. N8 = 3Ø16 na segunda, intervalo 6,00–8,35 m, d=64,6 cm. A ordem é documental; centros são da convenção pública Concretopy, não cotas explícitas extraídas do PDF. Seção/estribo uniformes no ramo são hipótese de auditoria reaproveitada e indicada; geometria transversal estrita na região de apoio permanece pendente.

| Região | MRd (kNm) | Mk equivalente (kNm) | Msk governante (kNm) | Resultado |
|---|---:|---:|---:|---|
| N7 | 171,405027 | 122,432162 | −10,512479 | atende |
| N7+N8 | 318,463539 | 227,473956 | −194,936589 | atende |

## 13. Escalonamento N8

Corte esquerdo documental em x=6,000 m; antes N7+N8, depois N7. Crossing remanescente x=7,289867624 m. Pico endpoint piecewise-linear em S13, x=7,936 m e Msk=−194,9365887 kNm; não é máximo estrutural exato.

Vk governante: Q MN., S13, x=7,936 m, Vk=−113,39429395 kN; magnitude 113,39429395 kN, de 26 amostras nas duas envoltórias do vão físico 0–8,43 m. É máximo do domínio amostrado, não esforço extrapolado em ponto ausente.

d anterior para al=66,4 cm (centroide N7+N8). al final=66,4 cm. N8 em má aderência por decisão específica; fbd=2,763196763 MPa, lb básico=62,939073262 cm, 10φ=16 cm.

| Controle | Referência x (m) | Disponível (cm) | Exigido (cm) | Atende |
|---|---:|---:|---:|---|
| al+lb | 7,936000000 | 193,600000 | 129,339073 | sim |
| al+10φ | 7,289867624 | 128,986762 | 82,400000 | sim |

Posição final exigida pelo primeiro: 6,642609267 m. Pelo segundo: 6,465867624 m, governante no sentido LEFT. Corte real 6,000 m permanece intacto e satisfaz ambos. Resultado do evento=true, resultado da resistência regional=true; aprovação negativa global=null, selected_solution=null.

## 14. Provenance

Cada entrada real mantém hashes dos JSON-fonte. Geometria vem de mapping/detalhamento; Msk e Vk de séries TQS auditadas; referências de consulta/crossing linear; camadas de ordem documental e posição Concretopy; MRd/Mk/d, al e ancoragem têm chamadas e origem API/contexto. JSON não substitui extremidade por seção TQS. A seleção limitada ao ramo serve somente para escolher referências existentes, nunca altera a extremidade física ou extrapola esforço.

## 15. Skill e contradição histórica

SKILL seção negativa aponta à referência negative-longitudinal-review.md, ligada ao contrato das ferramentas e APIs. beam-review apontava a planilha como meio atual; o texto foi atualizado explicitamente para registrar sua natureza histórica e a API atual. A antiga proibição de estender regras positivas às negativas continua semanticamente preservada: agora existe política negativa própria confirmada, com motores comuns. Não se alteraram relatórios históricos nem decisões positivas.

## 16. Testes

99 testes novos: sinais/origens, primeira/múltiplas camadas, posições fixas, regiões, cortes sucessivos, controles/crossings/zero/pico, pendências parciais, má aderência, porta-estribo/regiões, continuidade, nós/balanços e golden real. Sem fórmulas resistentes copiadas nos testes.

Suíte completa assistant: 39 extrator_lst + 30 beam_model + 34 beam_mapping + 445 reinforcement_checks = **548 aprovados** (449 anteriores + 99 novos). Concretopy: **405 aprovados**. Skill quick_validate: passou. git diff --check: passou. Evidência estruturada em negative_longitudinal_reinforcement_validation.json.

## 17. Preservação e arquivos

150 arquivos protegidos conferidos por SHA-256: nenhum mudou. Incluem Concretopy, todos os JSON/goldens existentes e relatórios históricos. V501, V1001 positivo, V536/V565 positivo integrado, apoio/alternativas/correção/grampos, mapping e interpolação permanecem protegidos. Nenhum arquivo Concretopy foi alterado.

Arquivos desta etapa:

- `tools/reinforcement_checks/flexure_regions.py`
- `tools/reinforcement_checks/support_correction.py`
- `tools/reinforcement_checks/tqs_moments.py`
- `tools/reinforcement_checks/moment_diagram.py`
- `tools/reinforcement_checks/support_geometry.py`
- `tools/reinforcement_checks/longitudinal_review.py`
- `tools/reinforcement_checks/negative_detailing.py`
- `tools/reinforcement_checks/test_longitudinal_negative.py`
- `tools/reinforcement_checks/longitudinal_review.md`
- `tools/reinforcement_checks/README.md`
- `.agents/skills/reinforcement-review/SKILL.md`
- `.agents/skills/reinforcement-review/references/beam-review.md`
- `.agents/skills/reinforcement-review/references/negative-longitudinal-review.md`
- `analises/pranchas/validar_v1001_negativo.py`
- `analises/pranchas/V1001_negative_reinforcement_golden.json`
- `analises/pranchas/negative_longitudinal_reinforcement_validation.json`
- `.codex/analises/negative_longitudinal_reinforcement_implementation_audit.md`

## 18. Pendências e limites

Golden cobre somente o ramo negativo direito da V1001 e corte N8. Não cobre o lóbulo esquerdo, outro vão adjacente, continuidade real sobre o apoio, fabricação/ancoragem completa de dobra ou aprovação global. Interferências, pinos/raios, emendas, mínimos, mudança regional de seção/estribo e cabimento estrito no nó exigem dados/verificação própria. Uma marca por evento, reta no segmento de corte; cenários não representáveis retornam diagnóstico. Não gerar grampos negativos nem selecionar solução automaticamente.
