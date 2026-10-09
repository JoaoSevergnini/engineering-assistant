# Flexão positiva: golden e regiões geométricas

Camada pequena de orquestração, separada de beam_mapping. Consome modelos
existentes e usa exclusivamente a API pública do Concretopy para áreas, alturas
úteis, equilíbrio, resistência e diagnósticos. Nenhuma equação resistente local.

```powershell
python -B tools/reinforcement_checks/v501_positive_flexure.py --concretopy-root ../concretopy --output analises/pranchas/V501_positive_flexure_check.json
python -B -m unittest discover -s tools/reinforcement_checks -p "test_*.py" -v
```

Concretopy não está instalado no Python atual; a CLI recebe explicitamente a raiz
do repositório local, sem instalar/copiar/alterar a biblioteca. O teste de integração
usa o repositório irmão `../concretopy`. API: `check_case(detail,tqs,positioned,
mapping,raw,api)`.

A origem da série é auditada no raw existente: VGESFS, registro M MX., vão,
valores normalizados, envelope max, stage model_input, kN.m. A natureza Msk é
declarada pelo engenheiro no pedido deste golden case. Não basta nome max. Valores
negativos são excluídos da governança; não há interpolação ou valor absoluto.

N5 precisa conservar sua composição documental e cobrir as 13 seções. Isso não
comprova desenvolvimento/ancoragem. A seção resistente usa o estribo documental
da região do ponto governante; não afirma capacidade uniforme nas outras regiões.
Fck é selecionado somente entre campos com unidade original MPa. RELDTVeT é
excluído. Cobrimento inferior TQS é identificado como dado do modelo, não como
confirmação de execução. Gamma_f é obtido explicitamente dos registros autorizados;
gamma_c/gamma_s e Es usam defaults públicos registrados do Concretopy.

`materials.py` interpreta CA50/CA-50/CA-50A como CA-50, fyk=500 MPa, pela regra
confirmada `engineer_confirmed_ca50_fyk_500_v1`. Independente de beam id,
preserva texto original, classe normalizada, fyk, regra e proveniência de cada
observação. A equivalência CA-50A é limitada à resistência característica neste
fluxo. Qualquer designação operacional desconhecida, mesmo junto de uma conhecida,
ou ausência de classe bloqueia a verificação, sem usar Aco.fyk default.
RELDTVeT continua excluído, com observações preservadas separadamente.
Conflitos textuais históricos não são apagados do consolidado; não geram conflito
do fyk derivado. Não existe tabela de outras classes. O antigo override
`--fyk-resolution` foi removido para impedir bypass de classe desconhecida.

Resultado mantém a dataclass completa do Concretopy e converte exclusivamente
kN.cm para kN.m (divisão por 100). Utilização usa Mk equivalente recebido, nunca
MRd diretamente. Ductilidade, hipóteses resistentes, mínimo e ancoragem são campos
independentes. Mínimo não é solicitado nesta etapa.

CLI audita hashes do mapping e raw, registra hashes dos inputs e da implementação
Concretopy e interpretador de materiais. Não altera modelos/fontes ou Concretopy.
O golden real usa o aço derivado dos artefatos pela regra confirmada, executa
a API real com d omitido e verifica capacidade, utilização e diagnósticos.
Os testes de materiais cobrem aliases equivalentes, origem preservada, ausente,
desconhecido, exclusão de RELDTVeT e imutabilidade.

## Diagrama linear de Msk (regra confirmada em 04/10/2026)

`moment_diagram.MomentDiagram(points, provenance)` recebe qualquer sequência
estritamente crescente com pelo menos dois pontos. `diagram_from_tqs` reutiliza
a auditoria M MX. e as positions existentes. Métodos: `moment_at_x(x)`,
`find_crossings(M_limit)`, `positive_maximum()` e `as_dict()`.
Sem extrapolação, sem gaps conectados, com endpoints documentais exatos.
Usa Decimal com precisão explícita 50; resultados derivados conservam strings
decimais operacionais e números float compatíveis com os modelos existentes.
Cruzamentos são analíticos, ordenados e deduplicados por coordenada exata;
segmentos coincidentes retornam intervalos. Gaps tornam a busca incompleta.

Golden independente: `python -B tools/reinforcement_checks/v1001_moment_interpolation.py
--concretopy-root ../concretopy --output analises/pranchas/V1001_moment_linear_interpolation.json`.
Consulta o término documental de N3 e chama Concretopy para N5 isolada na
configuração auditada à esquerda do evento. Não altera o algoritmo discreto
anterior das regiões, nem escolhe corte normativo ou avalia ancoragem.

## Verificação genérica por regiões de um vão mapeado


```powershell
python -B tools/reinforcement_checks/positive_flexure.py --detail analises/pranchas/V501_V503_beam_model.json --tqs analises/pranchas/V501_tqs.json --positioned analises/pranchas/V501_tqs_positions.json --mapping analises/pranchas/V501_beam_mapping.json --raw analises/pranchas/V501_tqs_raw.json --concretopy-root ../concretopy --output analises/pranchas/V501_positive_flexure_regions.json
```

`flexure_regions.decompose_regions(bars, domain, transverse_regions=None)` é
função geométrica pura: eventos de início/fim, domínio físico explícito e mudanças
transversais. `positive_flexure.check_positive_flexure(...)` orquestra cada região.
`tqs_moments.audited_moment_series` é compartilhada com o golden; campos materiais
documentais são compartilhados em materials.py. O script V501 permanece fixture
de integração/regressão, sem ser arquitetura definitiva da função genérica.

Domínio padrão: eixo esquerdo até eixo direito do único vão físico mapeado,
incluindo as seções TQS internas aos apoios. Não se extrapola estribo para os apoios.
Regiões sem operandos transversais conhecidos permanecem não resolvidas.

### Limites e camadas

Intervalos documentais de barras continuam fechados. Os interiores entre eventos
são inicialmente abertos. Cada limite é incluído na região direita se a configuração
fechada coincide; senão na esquerda se coincide; senão cria região pontual fechada.
`include_start/include_end` são explícitos. Cada seção pertence a uma única região,
sem epsilon. No encontro fim/início de marcas, o ponto pode conter ambas. No
encontro de estribos diferentes, a geometria do ponto fica não resolvida.

O índice 1-based do vetor layers do beam_model representa a camada a partir da
mesma face inferior. Somam-se quantidades apenas com essa identidade documental,
face lower e mesma bitola. Camadas sem posição/face conhecida não são fundidas.
Bitolas diferentes na mesma camada e lacunas de camadas são preservadas e bloqueadas:
Concretopy admite uma bitola por camada e não se pode colapsar índices físicos
para gerar d automático. Não há área/bitola equivalente.

Por padrão, limites dos estribos do mapping subdividem a configuração transversal,
com seção retangular e cobrimento documentado ou inferior TQS. A API aceita também
regiões transversais explicitamente fornecidas com proveniência, para dados de
seção/cobrimento por trecho; não infere variações de cortes sem abscissa.
Intervalos desconhecidos não viram ausência. Função longitudinal não classificada
permanece candidata não resolvida, impedindo composição falsa.

### Resultado

Conserva composição por camada/marca, geometria, pontos (inclusive negativos),
governança positiva, chamada e dataclass Concretopy completa, MRd/Mk e utilização,
diagnósticos separados e proveniência. Referências compartilhadas evitam repetir
arquivos-fontes. `demand_not_sampled` preserva região sem ponto; `no_positive_demand`
preserva negativos sem fabricar solicitação. Dados ausentes/arranjos não suportados
impedem somente chamadas dependentes. Não há cálculo resistente/interpolação local.

Resumo enumera verificadas, não resolvidas, sem pontos, sem positivos e não
verificadas. `all_checked_regions_capacity_sufficient` refere-se somente às
chamadas concluídas; é null se nenhuma foi concluída, e nunca significa vão aprovado.
`incomplete` e diagnósticos de cada região expõem todas as lacunas.

## Selecao de Vk para decalagem (regra confirmada)

A referencia [engineer_confirmed_al_shear_selection_v1](al_shear_selection.md)
registra os dois contextos: maximo |Vk| de todo o vao para escalonamento;
maximo |Vk| da regiao do apoio para ancoragem local. A definicao espacial da
regiao de apoio permanece pendente. Para escalonamento, `tqs_shear.py` ja
implementa a selecao auditada de todo o vao; esse status sucede o registro
historico anterior a integracao, conforme a nota de atualizacao da referencia.

## Escalonamento positivo no vao (05/10/2026)

Implementacao generica e contrato em [bar_scaling.md](bar_scaling.md).
`bar_scaling.py` orquestra composicoes, cruzamentos direcionais e condicoes
A (al+10phi) e B (al+lb basico); `tqs_shear.py` audita Q MX./Q MN. e
seleciona o maximo modulo discreto de todo o vao. Calculos fisicos continuam
exclusivamente no Concretopy. `v1001_scaling.py` aplica o golden real N3.

Esta implementacao sucede o estado documental anterior da selecao de Vk,
sem implementar a regiao de apoio. A selecao de d segue
[engineer_confirmed_al_effective_depth_v1](al_effective_depth.md): centroide
tracionado da composicao imediatamente antes do corte, reutilizado do Concretopy.
O golden N3 conclui A/B/final true, conforme relatorio
[da V1001](../../.codex/analises/V1001_N3_scaling_check.md).

## Procedimento operacional consolidado na Skill

Para executar uma revisao de corte positivo dentro do vao, consultar
[positive-bar-scaling.md](../../.agents/skills/reinforcement-review/references/positive-bar-scaling.md).
A referencia concentra sequencia, evento/orientacao, capacidade remanescente,
cruzamentos/pico, A/B, conclusao, provenance e bloqueios do escopo validado.
As regras especificas permanecem em [Vk](al_shear_selection.md),
[d para al](al_effective_depth.md) e
[aderencia](../../.agents/skills/reinforcement-review/references/bond-condition.md).

Goldens de uma/duas camadas: [V1001](../../.codex/analises/V1001_N3_scaling_check.md)
e [V536/V565](../../.codex/analises/V536_V565_N3_scaling_check.md).
Nao regravar seus resultados para consultar ou testar o procedimento.
Escalonamento atendido nao substitui ancoragem nos apoios nem aprova a viga.

## Apoio extremo esquerdo e alternativas (06/10/2026)

`support_alternatives.py` verifica a configuração existente e explora bitolas,
quantidades e camadas configuráveis, com recálculo integral por APIs públicas
Concretopy. Contrato em [support_alternatives.md](support_alternatives.md);
procedimento em [positive-end-support.md](../../.agents/skills/reinforcement-review/references/positive-end-support.md).
O fixture V536/V565 usa S1 e lb_ef=24-2,5=21,5 cm, conservando documental 21 cm.
Esta decisão sucede a hipótese anterior de comprimento do ensaio, sem alterar
a posição documental nem o escalonamento. Cabimento transversal/gancho não
são certificados; As_adicional não equivale a grampo.

## Correção orientada pelo detalhamento (06/10/2026)

`support_correction.py` preserva a busca genérica e acrescenta a hierarquia
existente/prolongamento/redistribuição, cabimento por primitivas Concretopy e
compatibilidade regional pelo diagrama/region decomposition existentes.
[Contrato](support_correction.md) e
[procedimento da Skill](../../.agents/skills/reinforcement-review/references/positive-support-correction.md).
Não dimensiona grampos nem escolhe silenciosamente uma solução final.

## Grampos complementares no apoio (06/10/2026)

`support_staples.py` envolve a correção existente sem alterar seus goldens.
Usa As_adicional como alvo inicial, área/ancoragem básica por Concretopy e
max(2*lb_grampo+lb_ef,60 cm) por decisão do engenheiro. Ramos resistentes e
aderência têm fonte explícita; sem distribuição formalizada não produz
solução pronta. Preserva prolongamentos válidos e selected_solution=null.
[Contrato](support_staples.md), [Skill](../../.agents/skills/reinforcement-review/references/positive-support-staples.md)
e [auditoria V536/V565](../../.codex/analises/V536_V565_support_staples.md).

### Atualização da geometria usual dos grampos

U de dois ramos; L_long=max(2*lb+lb_ef,60 cm) por ramo e conector
L_transversal=b−2*cobrimento−1 cm. Série própria [6.3,8,10] configurável;
preferência de até três peças, acima disso avaliação especial sem reprovação
automática. Comprimento nominal não é corte/C de fabricação; distribuição
vertical permanece pendente. [Auditoria atual](../../.codex/analises/V536_V565_support_staples_geometry_update.md).

### Distribuição vertical dos grampos confirmada

De baixo para cima, 2 cm livres (eixos=2+phi_cm), altura ocupada
n*phi_cm+(n−1)*2. Controle de envelope e janela vertical explícita com fonte;
posição inicial não inferida. Distribuição definida não significa interferências
verificadas ou prancha pronta. [Auditoria](../../.codex/analises/V536_V565_support_staples_vertical_distribution.md).

## Golden integrado positivo V536

[Fixture](../../analises/pranchas/validar_v536_positivo_completo.py) e
[relatório](../../.codex/analises/V536_positive_reinforcement_complete_golden.md)
recalculam resistência/regiões, escalonamento, apoio/ancoragem esquerda,
busca genérica, correção orientada pelo desenho e grampos. JSON único com
respostas/provenance integrais, testes de regressão contra goldens individuais
e fontes somente leitura. O golden preserva falha real da N2 no apoio,
alternativas sem seleção e pendências: geometria documental
nos apoios, trecho final não amostrado e nó. Golden validado não significa
armadura positiva ou viga globalmente aprovadas.

## Ancoragem positiva END/INTERMEDIATE, LEFT/RIGHT

[Contrato](support_anchorage.md), [orientação](support_geometry.py) e [orquestração](support_anchorage.py). END preserva A/B/C e correções existentes; INTERMEDIATE usa seção terminal orientada e A/C, com regras distintas para presença/ausência de positivo. O [novo fixture direito V536](../../analises/pranchas/validar_v536_apoio_direito.py) atualiza o integrado com ancoragem longitudinal real, mantendo pendência transversal e nó. As limitações históricas de primeira versão ao lado esquerdo estão superadas em orientação, sem alteração dos goldens individuais. [Auditoria](../../.codex/analises/support_anchorage_generalization_audit.md).

## Revisão longitudinal negativa

Consultar [longitudinal_review.md](longitudinal_review.md) e a
[referência operacional da Skill](../../.agents/skills/reinforcement-review/references/negative-longitudinal-review.md).
A generalização reutiliza regiões, esforços/interpolação, orientação e Concretopy;
preserva os defaults positivos e não altera os goldens anteriores.

Términos longitudinais coincidentes: consultar [eventos independentes por marca](../../.agents/skills/reinforcement-review/references/longitudinal-termination-events.md). Usar a composição física posterior, sem sequência artificial; separar término desenhado e posição requerida.

Classificação estrutural no apoio intermediário: `intermediate_support_review.check_intermediate_bar_event` recebe a geometria do apoio relativo ao vão adjacente e as barras/contextos/diagramas dos dois lados. Prova regional precede o cálculo; reutiliza SCALING ou verifica lb básico desde a face física. [Procedimento e limitações](../../.agents/skills/reinforcement-review/references/intermediate-support-longitudinal-verification.md). Não otimiza detalhamento.

## Revisão negativa de apoio extremo

`negative_end_support_review.review_negative_end_support` descobre marcas que chegam à face END/COLUMN; `check_negative_end_support` separa flexão terminal, reta, dobra vertical e disposição transversal. Reutiliza o nó existente e a primitiva geométrica compartilhada `negative_end_vertical_bend_limits`, sem novo motor resistente. Centros transversais/cota perpendicular ausentes não são estimados. Contratos, fontes de dobra por lado e regras: [apoio negativo extremo](../../.agents/skills/reinforcement-review/references/negative-end-support.md). Sem otimização; selected_solution e detailing_optimization null.

## Relações negativas entre apoios consecutivos

[negative_reinforcement_relations](negative_reinforcement_relations.md) classifica peças físicas, encontro, transição e continuidade, preservando os motores existentes. [Procedimento e regras confirmadas](../../.agents/skills/reinforcement-review/references/negative-reinforcement-relations.md). Massa local em `steel_mass.py` com densidade explícita e área Concretopy; sem escolha automática de correção.

## Cortante por faixas desenhadas e referência por terços

[shear_review](shear_review.md) e [procedimento da Skill](../../.agents/skills/reinforcement-review/references/shear-reinforcement-review.md): diagramas próprios Vk, Concretopy, Asw/s e smax separados, ramos reais e prática usual. Sem suspensão/redesenho. Golden V516/V517 em arquivos próprios de cortante; longitudinais são entradas read-only.

## Suspensão independente após cortante

[suspension_review](suspension_review.md): reação total da viga apoiada sobre a receptora, região simétrica, combinação sem dupla contagem do mínimo, faixas reais e estados independentes. Reutiliza Concretopy e a infraestrutura shear_*, sem alterar goldens de cortante/longitudinais ou selecionar solução. [Referência da Skill](../../.agents/skills/reinforcement-review/references/suspension-reinforcement-review.md).

## Diagnóstico consolidado

beam_diagnostic.py reúne resultados já calculados; beam_diagnostic_adapters.py adapta os contratos históricos explicitamente. Consultar [contrato](beam_diagnostic.md). Nenhuma fórmula resistente, alteração de armadura ou seleção automática.

Diagn�stico 1.1, estados independentes de execu��o e contratos futuros: [diagnostic_update.md](diagnostic_update.md).

Motor inicial de propostas a partir de diagn�stico: [correction_engine.md](correction_engine.md). N�o seleciona solu��es nem edita PDF.

Procedimento documental e geométrico opcional: [STAGE1_CONTRACT](../beam_model/STAGE1_CONTRACT.md), com preflight local e entrada física de flexão. Relatório e regressões em [Etapa 1](../../analises/etapa1_leitura_geometria/relatorio_etapa1.md). As chamadas antigas mantêm sua compatibilidade; usar os adaptadores explícitos para obter a validação das novas evidências.
