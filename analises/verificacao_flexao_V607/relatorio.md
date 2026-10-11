# V607 — verificação real de flexão positiva

**Resultado: atende à resistência à flexão positiva no vão livre, com utilização de 30,0%.** A verificação foi executada com o fluxo atual e o Concretopy existente, após `input_preflight = RUNNABLE`. Não foram criados módulos nem modificados métodos resistentes ou PDFs.

## Geometria e documentação

A V607 liga V619 a V621. A planta de formas original `051-SJ-EST-EX-010-PLB-TP-R01.pdf`, página 1, foi examinada visualmente na região da escada: identifica V607 **14/37** e a cadeia de cotas **19 + 204 + 19 cm**. Não há mudança de seção indicada no vão livre examinado. O detalhamento `051-SJ-EST-LO-06301-VIG-TIP-R00.PDF`, página 1, identifica a mesma seção e os mesmos apoios.

| Informação | Valor utilizado | Origem |
|---|---:|---|
| Seção retangular | 14 × 37 cm | Forma, identificação V607; elevação e corte A do detalhamento |
| Vão livre | 2,04 m | Cota 204 da forma, entre faces de V619 e V621 |
| Largura longitudinal de cada apoio | 19 cm | Cotas da forma e detalhamento |
| Distância entre eixos | 2,23 m | 2,04 + 0,095 + 0,095; compatível com VGESFS.LST |
| Cobrimento | 2,5 cm | `V607_tqs.json`, `/beam/cover/general = 0.025 m`; dimensão interna do estribo 9 × 32 cm é coerente com a seção |
| Estribo N3 | Ø5 mm | Elevação, desenho do estribo e tabela de aço: 11 peças, C=97 cm |
| Concreto | fck = 40 MPa | RELDTFNG.LST, linha 1713, e RELDTFPS.LST, linha 3305: campo explícito em MPa |
| Aço longitudinal | fyk = 500 MPa | Classe CA50/CA-50A dos LST; interpretação já estabelecida em `materials.interpret_steel`, confirmada por João no fluxo |
| γf e γc | 1,4 e 1,4 | Campos `gamaf` e `gamac` dos registros de materiais TQS preservados em `V607_tqs_raw.json` |
| γs | 1,15 | Critério resistente mantido do fluxo histórico; não identificado como campo documental extraído do LST |

Os PDFs originais de armaduras e os LST não estão acessíveis nesta sessão. Foram utilizados o recorte original preservado, o texto extraído e os JSONs TQS com referências aos arquivos e linhas. A forma original está acessível e foi examinada agora. Essa distinção é relevante para rastreabilidade: não houve nova leitura dos LST originais.

## Armaduras e altura útil

O detalhamento e a tabela de aço coincidem:

| Posição | Armadura | Comprimento nominal | Distribuição |
|---|---|---:|---|
| N1, inferior | 2 Ø10 | 274 cm = 234 + 20 + 20 | Uma camada inferior, confirmada pelo corte A |
| N2, superior | 2 Ø6,3 | 264 cm = 234 + 15 + 15 | Uma camada superior, confirmada pelo corte A |

Fonte da tabela: texto preservado da prancha 06301, linhas 1129–1147. A elevação mostra as duas barras N1 percorrendo todo o vão livre; não há interrupções ou reforços inferiores adicionais nessa região. A N2 não foi contabilizada como armadura comprimida na resistência positiva.

O intervalo de barras no arquivo de entrada foi **recortado ao domínio verificado [0; 2,04] m**. Seus limites representam cobertura comprovada do vão livre, não coordenadas dos extremos físicos ou dos ganchos. Portanto, este cálculo não certifica ancoragem.

Área inferior: **As = 2 × π × 1,0² / 4 = 1,5708 cm²**.

Altura útil calculada pelo posicionamento nominal do Concretopy existente:

**d = h − c − Øestribo − Ølongitudinal/2 = 37 − 2,5 − 0,5 − 0,5 = 33,5 cm.**

A existência de uma camada é documental, pelo corte A. A posição do centro das barras usa cobrimento e tangência nominal ao estribo; não é uma medição vertical do PDF. O resultado é coerente com o d=33,5 cm registrado pelo TQS para esta viga.

Antes do cálculo resistente, o verificador existente confirmou o cabimento: largura interna disponível **8,0 cm**, largura requerida por duas Ø10 com afastamento mínimo adotado de 2 cm **4,0 cm**. Há espaço para a camada considerada. A rotina mantém seu parâmetro de agregado de 16 mm; o TQS registra 15 mm, diferença que não altera o afastamento de 2 cm deste caso.

## Esforço solicitante

Foi mantida a envoltória **M MX., estágio model_input**, de VGESFS.LST, linha **234**, referência `s430#/normalizacao`. A seção 7 informa **0,485 tf·m**, convertida pelo extrator existente com 1 tf = 9,80665 kN:

**Mk,max = 0,485 × 9,80665 = 4,75622525 kN·m.**

O eixo local TQS começa no eixo de V619. O eixo físico usado no cálculo começa na face interna desse apoio. A transformação comprovada é **x físico = x TQS − 0,095 m**. O comprimento 2,23 m e DEPEV=0 em ambos os apoios foram confrontados com as cotas da forma. A seção 7 fica em x TQS=1,115 m, isto é, **x físico=1,020 m**, no meio do vão livre.

**MSd = γf × Mk,max = 1,4 × 4,75622525 = 6,65871535 kN·m.**

O máximo governante é um ponto originalmente fornecido pelo TQS. A interpolação linear existente nas faces de apoio não altera esse máximo. A série de entrada para dimensionamento positivo do RELDTFPS tem máximo 0,49 tf·m; ela não foi misturada à envoltória VGESFS. Se usada apenas como sensibilidade, produziria MSd=6,72736 kN·m e utilização de 30,31%, mantendo o atendimento.

## Resistência e resultado

O verificador resistente existente retornou:

| Grandeza | Resultado |
|---|---:|
| fcd = fck/γc | 28,571 MPa |
| fyd = fyk/γs | 434,783 MPa |
| As | 1,5708 cm² |
| d | 33,5 cm |
| Profundidade da linha neutra x | 2,5109 cm |
| x/d | 0,07495 |
| Limite x/d utilizado pelo método | 0,45 |
| MRd | **22,1931 kN·m** |
| MRd/γf, resistência equivalente característica | 15,8522 kN·m |
| MSd/MRd | **0,3000** |
| Hipóteses do modelo e ductilidade | Atendidas, segundo o método existente |

Conferência independente por equilíbrio, com os próprios parâmetros do método (αc=0,85 e λ=0,8):

T = As × fyd = **68,2955 kN**; x = T/(αc × fcd × bw × λ) = **2,5109 cm**; z = d − 0,4x = **32,4957 cm**; MRd = T × z = **22,1931 kN·m**. As conversões de MPa para kN/cm² e de cm para m foram consideradas. Essa conferência reproduz a resistência retornada, sem alterar o método.

A API resistente existente também foi chamada com `verificar_armadura_minima=True`, após a confirmação das entradas pela guarda. Retornou **As,min=0,92722 cm²**, inferior a As=1,5708 cm²: armadura mínima atendida segundo o critério implementado. O resultado regional automático não calcula esse item; a chamada complementar está registrada separadamente em `armadura_minima.json`. Não foi consultado texto normativo nesta demonstração; o valor é identificado como resultado do critério existente no Concretopy, sem atribuição de item normativo.

**Conclusão estrutural:** a armadura inferior N1 atende à flexão positiva no vão livre da V607, com MSd=6,66 kN·m < MRd=22,19 kN·m. A distribuição cabe fisicamente, e as verificações de armadura mínima e ductilidade do método existente atendem. Não falta informação que impeça este cálculo local, sob o γs=1,15 mantido do fluxo. A conclusão não abrange flexão negativa nos apoios, ancoragem, cisalhamento, torção, serviço ou aprovação global da viga/pavimento.

## Registro da execução

Entrada rastreável: [entrada.json](entrada.json). Saída efetiva do fluxo: [resultado.json](resultado.json). Verificação complementar: [armadura_minima.json](armadura_minima.json). O controle positivo resultou `RUNNABLE / EXECUTED_COMPLETE / PASS`. Os demais controles permanecem fora desta conclusão, mesmo quando o fluxo registra pendências para eles.

Reprodução a partir da raiz do repositório:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python tools/reinforcement_checks/floor_review.py analises/verificacao_flexao_V607/entrada.json --output analises/verificacao_flexao_V607/resultado.json
```

Somente arquivos de análise desta demonstração foram acrescentados. Os arquivos históricos e o Concretopy foram preservados.
