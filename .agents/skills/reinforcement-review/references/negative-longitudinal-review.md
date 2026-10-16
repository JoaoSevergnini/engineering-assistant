# Revisão da armadura longitudinal negativa

## Sequência operacional

Após a positiva, revisar: (1) geometria e apoios; (2) barras negativas e função documental; (3) camadas físicas; (4) regiões longitudinais; (5) resistência regional; (6) interrupções sucessivas; (7) término para dentro do vão; (8) continuidade em apoio intermediário; (9) nó extremo/balanço, se aplicável; (10) pendências de geometria e conclusão por controle.

Usar `tools/reinforcement_checks/longitudinal_review.py` e `negative_detailing.py`, com o [contrato das ferramentas](../../../../tools/reinforcement_checks/longitudinal_review.md). Reutilizar `flexure_regions`, `moment_diagram`, `SupportGeometry`, controles orientados de `support_anchorage` e APIs públicas do Concretopy. Não criar uma cópia negativa dos motores positivos nem duplicar resistência, fbd, lb ou al.

## Esforços e camadas

Selecionar a envoltória característica negativa TQS auditada, preservando valores com sinal e origem. A vista resistente negativa é −M, não abs(M): um momento positivo não pode virar demanda negativa. Interpolar linearmente entre pontos existentes, sem extrapolação ou suavização. O ramo conectado ao terminal pode incluir o ponto adjacente de sinal oposto para localizar o zero por interpolação. Não transportar o pico amostrado para eixo/face de apoio.

A negativa traciona TOP e comprime BOTTOM; d é medido desde a face inferior comprimida até o centro da barra. Ordenar camadas fisicamente desde a face tracionada, sem prioridade por marca/ordem textual. Converter explicitamente a origem das coordenadas. Sem centros documentais, a convenção automática do Concretopy exige confirmação da ordem a partir da face tracionada. Manter posições fixas após retirar barras; não recolocar uma camada remanescente junto à face. Suportar três ou mais camadas e marcas distribuídas entre camadas. Registrar `engineer_confirmed_reinforcement_layer_face_order_v1`.

Verificar cada região, seus extremos e vértices TQS, incluindo limites de composição. Registrar MRd, Mk equivalente, momento original, magnitude negativa, d/camadas, utilização, validade das hipóteses e provenance. Armadura mínima e aprovação completa do nó não são demonstradas somente por essa comparação.

## Tipos de verificação

Antes de tratar uma marca que atravessa apoio intermediário como corte no vão, aplicar [classificação estrutural após apoio](intermediate-support-longitudinal-verification.md). Remanescente suficiente em todo o ramo e necessidade no lado anterior demonstrada encaminham à ancoragem física 1,0 lb, não aos controles abaixo.

**SCALING:** identificar antes/depois no sentido do corte e recalcular a capacidade apenas da composição remanescente. Verificar separadamente:

- desde o pico/início da decadência piecewise-linear: al + lb básico da barra interrompida;
- desde o crossing da capacidade remanescente no ramo: al + 10φ da barra interrompida.

Repetir por interrupção sucessiva, inclusive terceira camada seguida da segunda. Preservar todos os crossings e a seleção por ramo/lado. Pico endpoint é permitido quando existe decadência no sentido do corte. Platô, ramo incompatível ou crossing inexistente/ambíguo bloqueiam o controle dependente; não escolher candidato global arbitrariamente.

**SPAN_TERMINATION:** verificar al + lb desde o crossing da capacidade da composição levada até esse término, conforme esclarecimento do engenheiro; verificar al + 10φ desde o zero negativo do ramo. Governar pela posição final mais exigente no sentido do corte, sem comprimento extra arbitrário. Se a capacidade superar estritamente todo o ramo e não existir ponto de plena utilização, o controle de crossing é NOT_APPLICABLE; não fabricar referência. O zero continua obrigatório. Regra `engineer_confirmed_negative_reinforcement_span_termination_v1`.

Cada evento avalia uma marca, inclusive com múltiplas camadas. Marcas distintas podem terminar na mesma coordenada: seguir [eventos independentes](longitudinal-termination-events.md), usando a composição física posterior sem sequência artificial de cortes.

## al e aderência

Referenciar [seleção de Vk](../../../../tools/reinforcement_checks/al_shear_selection.md) e [centroide anterior](../../../../tools/reinforcement_checks/al_effective_depth.md). Para eventos no vão, usar máximo |Vk| de todo o domínio físico amostrado, ambas as envoltórias pertinentes; d é o centroide resistente imediatamente antes do corte, medido da face comprimida. Concretopy calcula al e retorna o valor final limitado. Registrar `engineer_confirmed_negative_al_same_as_positive_v1`. Outros contextos de Vk exigem decisão própria.

Nesta revisão, a decisão `engineer_confirmed_negative_beam_reinforcement_poor_bond_v1` impõe **má aderência para as negativas**, independentemente da posição y. É política específica do engenheiro; não aplicar a classificação geométrica positiva nem atribuir essa escolha à NBR. Usar Concretopy para lb básico da própria bitola; não substituir por lb_nec nem reduzir por área/gancho nos controles al + lb.

## Função das barras e continuidade

Porta-estribo exige função documental e ausência de demanda negativa no seu intervalo. Cruzar o intervalo com estribos reais e aplicar max(6,3 mm, bitola regional do estribo). Se atravessar bitolas de estribo distintas, apresentar regiões e pedir definição; não usar máximo global. Regra `engineer_confirmed_beam_stirrup_holder_diameter_v1`. PELE exige indicação explícita ou provenance equivalente; barra superior sem função resolvida permanece UNKNOWN.

No apoio intermediário, preferir continuidade física quando possível. Exigir evidência de trajetória, bitola, camada, identidade documental e intervalo atravessando o apoio. Verificar independentemente RIGHT do vão esquerdo e LEFT do vão direito, com seus próprios diagramas/controles. Continuidade não prova ancoragem nem permite espelhar esforços. Não adicionar extensão arbitrária. Regra `engineer_confirmed_negative_intermediate_support_extension_v1`.

## Nó extremo e balanço

Para apoio END em pilar, executar [revisão explícita do apoio extremo](negative-end-support.md), que separa demanda S1/S13, resistência, ancoragem reta, dobra vertical, espaçamento mínimo, vibrador e interferência transversal. A regra geométrica existente é preservada e recebe a decisão `engineer_confirmed_negative_end_support_vertical_bend_v1`. Sem otimização.

No nó extremo em pilar sem espaço para ancoragem reta, estudar geometricamente a perna de dobra `min(h − cobrimento − φ_estribo, 2*lb básico)`. Regra `engineer_confirmed_negative_end_frame_node_bend_v1`. A ferramenta separa espaço/penetração reta, definição geométrica da dobra e verificação resistente. Não inventar C de fabricação, pino, raio ou crédito α=0,7. Geometria definida não aprova ancoragem da dobra.

Somente no balanço único engastado em pilar confirmado, exigir ancoragem reta 1,5*lb básico, sem redução por excesso de área ou gancho; se impossível, estudar a dobra com conclusão resistente pendente. Regra `engineer_confirmed_single_cantilever_negative_anchorage_1_5lb_v1`. Não estender a balanço contínuo, console, Gerber ou apoio em outra viga.

Na extremidade livre desse balanço, a sobra `h − 2*cobrimento − φ_estribo` é a **perna vertical da dobra**, conforme esclarecimento do engenheiro, não projeção longitudinal. Comparar com comprimento documental dessa perna e manter controles longitudinais independentes. Regra `engineer_confirmed_cantilever_free_end_negative_tail_v1`.

## Conclusão e regressões

True exige todas as dependências resolvidas e controles aplicáveis atendidos; False representa verificação completa com falha; null representa pendência. NOT_APPLICABLE permanece identificado. Preservar geometria documental, origem dos esforços, composição antes/depois, capacidade, referências, Vk, d, al, lb e motivos. `selected_solution=null`; não propor correção automática ou grampos positivos para negativas.

Golden inicial: [V1001 negativa](../../../../analises/pranchas/V1001_negative_reinforcement_golden.json), gerado por `validar_v1001_negativo.py`: ramo negativo direito, N7/N8, duas camadas, corte esquerdo da N8. Os nomes e números são exemplos/regressão, nunca regras de produção. O golden não cobre a outra região negativa, continuidade entre vãos ou aprovação do nó. Goldens positivos permanecem intactos.

## Solicitação terminal junto ao apoio

`engineer_confirmed_negative_support_terminal_section_demand_v1`: apoio LEFT do vão usa diretamente S1; apoio RIGHT usa diretamente S13. Preservar x e momento original com sinal fornecidos pelo TQS e provenance da seção. Não transportar/interpolar/extrapolar o momento para face/eixo pelo DEPEV. Momento positivo não vira demanda negativa por abs(). `negative_support_terminal_demand` registra essa seleção sem alterar o diagrama.

## Relações entre apoios consecutivos

Antes de representar encontros de peças distintas como uma composição mista, consultar [relações negativas](negative-reinforcement-relations.md). A revisão separa continuidade física, encontro de detalhamento, transição resistente e peças independentes. Controles de encontro usam o grupo completo de menor bitola isolado; eventos SCALING verdadeiros preservam a regra anterior. A exceção de espaçamento é localizada, com identificação dos pares; não altera a primitiva geral.

### Máximo no apoio — esclarecimento de 15/10/2026

João confirmou usar o máximo negativo no apoio para capacidade resistente, sem interpolação redutora à face interna. A seleção terminal S1/S13 acima é o ponto de partida do formato TQS atual; se houver outros pontos fornecidos dentro do mesmo apoio, comparar os valores negativos e preservar o governante. Conferir os lados adjacentes somente com identidade física comprovada; registrar lados/composições separadamente enquanto não conciliados. Não usar máximo global de outro apoio nem extrapolar o diagrama. Esta orientação trata da solicitação, preservando Concretopy como fonte oficial da resistência.
