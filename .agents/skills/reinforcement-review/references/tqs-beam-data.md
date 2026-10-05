# Semântica dos dados de vigas do TQS

Referência permanente para as ferramentas de extração, consolidação e revisão de vigas.
Regra confirmada por João em 02/10/2026. Não constitui verificação estrutural.

## Comprimento do vão, DEPEV e distância entre apoios

### Contexto confirmado de duas torres

Confirmado por João em 04/10/2026: o detalhe V1001 da prancha
RMP-EST-LO-1376-VIG-R00 também representa V9001. Labels P2A/P2B e P1A/P1B
representam apoios correspondentes de duas torres, com sufixos A/B. Os blocos
individuais TQS confirmam V1001 → P2A/P1A e V9001 → P2B/P1B; esforços são
independentes. Registrar contexto por grupo com labels originais, candidatos,
membros, IDs por lado e evidências. Não inferir agrupamento de qualquer texto
com barra, nem escolher o primeiro nome. A origem documental pode incluir o
label: separar tipo face interna esquerda e referência, mantendo a string
original. Offset permanece b_esq/2, sem DEPEV adicional. Essa confirmação não
comprova equivalência de revisão entre PDF e TQS.


Nos arquivos LST do TQS, o comprimento do vão utilizado em conjunto com
as excentricidades dos apoios (`DEPEV`) permite determinar a distância
entre os eixos dos apoios.

Para um vão com apoio esquerdo e direito:

L_eixos = L_TQS + DEPEV_esq + DEPEV_dir

onde:

- `L_TQS` é o comprimento do vão informado pelo TQS;
- `DEPEV_esq` é a excentricidade do apoio esquerdo;
- `DEPEV_dir` é a excentricidade do apoio direito;
- `L_eixos` é a distância entre os eixos dos dois apoios.

Conhecendo as dimensões dos apoios na direção longitudinal da viga:

L_livre = L_eixos - b_esq/2 - b_dir/2

portanto:

L_livre = L_TQS + DEPEV_esq + DEPEV_dir - b_esq/2 - b_dir/2

A distância livre entre as faces internas dos apoios é a grandeza que
deve ser comparada com o comprimento do vão indicado no detalhamento
de armaduras.

As dimensões `b_esq` e `b_dir` correspondem às dimensões dos apoios na
direção longitudinal da viga.

Não interpretar `L_TQS` isoladamente como comprimento livre entre faces
nem como distância entre os eixos físicos dos apoios.

Pequenas divergências entre o comprimento livre calculado a partir dos
dados do TQS e o indicado no detalhamento devem ser registradas e não
corrigidas silenciosamente.

## Campos documentais existentes

- `geometria_tabular.campos.comprimento` → `beam.spans[i].geometry.length`, em m.
- `apoio.campos.excentricidade` → `beam.supports[j].eccentricity`, em m: DEPEV.
- `apoio.campos.largura` → `beam.supports[j].width`, em m: dimensão longitudinal b.
- `reacao_apoio.campos.depev` também preserva DEPEV, mas atualmente não possui
  unidade normalizada; não converter por pressuposição no consolidador.
- A ordem esquerda/direita vem de `span.support_ids`, não da lista global de apoios.

## Conflitos e limites

A regra não escolhe fontes nem elimina conflitos documentais. Operandos ausentes,
sem unidade utilizável ou conflitantes impedem o valor derivado, que fica null.
Não substituir null por zero nem selecionar a fonte com mais casas decimais.
A proveniência deve identificar todos os operandos, inclusive conflitos.

Para V501/V503, especificamente em RELDTFPS/RELDTFNG: L_TQS=7,552 m,
DEPEV=0,384/0,494 m, b=1,20/1,42 m resultam L_eixos=8,430 m e L_livre=7,120 m.
O documental da prancha indica 7,110 m: diferença +0,010 m, preservada.
Outros relatórios divergem nas excentricidades; nos modelos gerados antes da
política de 04/10/2026, o consenso permanece null. A preferência por RELDTFPS
agora decorre da decisão explícita do engenheiro abaixo, não deste exemplo.

## Fontes e escopo definidos pelo engenheiro em 04/10/2026

Estas decisões orientam a evolução das ferramentas. Não significam que os
parsers, consolidadores ou JSONs existentes já tenham sido atualizados.

- **Comprimento discretizado:** utilizar o comprimento do vão fornecido por
  VGESFS (`L_TQS`, correspondente ao campo atual `geometry.length`). Ele já
  representa a distância entre a primeira e a última das 13 seções.
- **Demais dados de geometria e DEPEV:** seguir RELDTFPS, que apresenta a geometria em cm.
  A escolha decorre da orientação do engenheiro; não de uma regra automática
  de selecionar a fonte com mais casas decimais. Manter a proveniência e
  registrar ausência/conflito na fonte escolhida, sem fallback silencioso.
- **Concreto:** utilizar os valores de fck explicitamente publicados em MPa.
  Não substituir esse valor por conversão de uma apresentação em kgf/cm².
  Se não houver valor explícito em MPa, registrar a informação pendente.
  A interpretação do aço segue a regra específica abaixo.
- **RELDTVeT:** não utilizar, a princípio, como fonte dos dados operacionais
  para integração/verificação. Os registros já extraídos permanecem como
  histórico documental; não precisam ser apagados nem corrigidos.
- **Solicitações:** utilizar VGESFS, preservando unidades, sinais, natureza
  documental dos esforços e ligação aos vãos. A escolha da fonte não autoriza
  majoração automática, interpolação ou fabricação de combinações.
- **Reações e ligações entre vigas:** utilizar VGESFS. O caractere nulo pode
  ser desconsiderado na identificação dos nomes; preservar texto original
  para rastreabilidade. Extrair viga de origem, apoio/receptora e reações
  máximas/mínimas como publicados. Não somar máximos nem presumir que uma
  ligação nominal identifica automaticamente um contorno do PDF.
- **Suspensão:** o resultado de dimensionamento do TQS não é necessário no
  escopo atual. O dado de interesse é a reação transmitida entre vigas.
  A suspensão será verificada posteriormente por ferramenta independente.
- **PDF e TQS:** desenvolver primeiro duas camadas independentes: obtenção
  de geometria/solicitações/reações do TQS e interpretação do detalhamento
  do PDF. Não usar igualdade entre armadura calculada e desenhada como
  objetivo ou critério de aceitação nesta etapa. Divergências são esperadas
  na futura ferramenta que apontará correções no PDF.
- **Verificações:** flexão, cisalhamento, ancoragem, suspensão e demais
  decisões resistentes pertencem à etapa posterior, usando os dados coletados.

A origem das séries e a diferença entre `L_TQS`, `L_eixos` e `L_livre` devem
continuar explícitas. A nova política não autoriza renomear ou reinterpretar
silenciosamente o campo existente `geometry.length`.

## Seções de esforços e reações

### Aço CA-50: resistência característica confirmada

Regra fornecida pelo engenheiro responsável em 04/10/2026 para este fluxo:
CA50 e CA-50 são grafias da classe normalizada CA-50, com fyk=500 MPa.
A designação CA-50A encontrada nos relatórios também corresponde, para fins
de resistência característica, a CA-50 com fyk=500 MPa. Esta regra não define
equivalência de outras propriedades ou de classes não reconhecidas.

Preservar texto original, classe normalizada, fyk derivado, regra e proveniência.
Fontes reconhecidas equivalentes não geram conflito de fyk. Qualquer designação
operacional não reconhecida/materialmente diferente bloqueia a verificação;
não selecionar apenas uma fonte reconhecida nem usar fyk default.
RELDTVeT permanece excluído operacionalmente e preservado como histórico.
Implementação reutilizável: `tools/reinforcement_checks/materials.py`, regra
`engineer_confirmed_ca50_fyk_500_v1`, somente aliases CA50/CA-50/CA-50A.
Consolidados antigos podem conservar conflitos textuais históricos; isso não
constitui conflito do fyk interpretado pela nova regra.

### Seções de esforços ao longo do vão

Regra fornecida e confirmada pelo engenheiro responsável em 03/10/2026.

O TQS apresenta os esforços de cada vão em 13 seções. Essas 13 seções são
definidas a partir do sistema local do vão identificado pelo TQS como `X=0`.

A primeira seção está afastada do eixo do primeiro apoio pela excentricidade
desse apoio (`DEPEV`). A última seção está afastada do eixo do segundo apoio
pela excentricidade desse apoio (`DEPEV`).

Complemento confirmado pelo engenheiro em 04/10/2026: as extremidades ficam
para dentro dos eixos dos apoios ou coincidem com eles. A primeira seção fica
à direita do eixo do primeiro apoio, definido como `x=0`; a última seção fica
à esquerda do eixo do segundo apoio.
Portanto, a origem no eixo do primeiro apoio está confirmada e não deve ser
confundida com a origem auxiliar na seção 1 usada no relatório investigativo.

Correção e esclarecimento confirmados pelo engenheiro em 04/10/2026: a última
seção fica a uma distância `length + DEPEV_esq` do eixo do primeiro apoio.
O comprimento fornecido por VGESFS já é o intervalo procurado entre as seções
1 e 13: `length = L_TQS = L_13`. A menção anterior ao eixo direito em
`x=length` foi corrigida; esse eixo fica em `x=L_eixos`.

Com origem no eixo físico do primeiro apoio e sentido positivo para o segundo:

```text
x_secao_1 = DEPEV_esq
x_secao_13 = DEPEV_esq + length = L_eixos - DEPEV_dir
L_13 = length = L_TQS (comprimento do vao em VGESFS)
Delta_x = L_13 / 12
x_secao_i = DEPEV_esq + (i - 1) * Delta_x
```

Para V501/V503: length=755,2 cm; DEPEV_esq=38,4 cm; DEPEV_dir=49,4 cm.
Assim, x_secao_1=38,4 cm, x_secao_13=793,6 cm, L_eixos=843,0 cm e
Delta_x=62,933333... cm. O DEPEV direito fecha a posição do eixo direito;
não deve ser subtraído novamente do length para definir L_13.

Essas equações registram a semântica, não uma implementação de `positions`.

As demais seções são obtidas dividindo o comprimento compreendido entre a
primeira e a última seção em 12 partes iguais. Portanto existem 13 pontos
igualmente espaçados, incluindo as duas extremidades do intervalo discretizado.

Importante:

- A identificação do comprimento de VGESFS como L_13 foi confirmada pelo
  engenheiro em 04/10/2026; não generalizar por nome a outros campos de length.
- Não assumir que a distância entre eixos dos apoios seja o comprimento
  discretizado.
- Não alterar ou reinterpretar a regra já registrada para `L_TQS`, `DEPEV`,
  distância entre eixos e distância livre.
- A semântica está confirmada. Em 04/10/2026, João autorizou o primeiro ensaio
  de preenchimento de `positions` na V1001. `tools/extrator_lst/section_positions.py`
  produz saída separada, somente com séries VGESFS e coordenadas locais em m,
  usando DEPEV de RELDTFPS. A implementação geral no consolidador ainda não
  foi alterada; modelos anteriores conservam seus `positions=null`.
- A uniformidade decorre da confirmação do engenheiro, não da mera existência
  de 13 valores. A identificação do comprimento físico e da origem de `X=0`
  nas fontes deve permanecer explícita; conflitos de DEPEV não são resolvidos
  por esta regra.

### Interpolação linear entre seções — decisão do engenheiro

Regra permanente `engineer_confirmed_tqs_linear_interpolation_v1`, confirmada
por João em 04/10/2026. As ferramentas TQS utilizadas neste fluxo trabalham
com 13 pontos discretos; não há, nos relatórios disponíveis deste processo,
série mais refinada a buscar. Para verificações que necessitem esforços entre
as seções discretas fornecidas pelo TQS, adota-se interpolação linear entre
pontos consecutivos da mesma série de esforços. Não se realiza extrapolação
além do domínio amostrado. Não interpolar sobre valores ausentes nem conectar
pontos não consecutivos para atravessar gaps.

Os valores originais permanecem primários. Preservar sinais, unidade, série,
posição, dois pontos-base, método/regra e proveniência. Nos endpoints retornar
o valor documental sem recálculo. Esta é uma regra do fluxo definida pelo
engenheiro, não uma afirmação sobre algoritmo interno do TQS. Não autoriza
ancoragem, decalagem normativa ou validação de corte de barras. Implementação
em tools/reinforcement_checks/moment_diagram.py; capacidade continua no Concretopy.


### Reações

Reações máximas/mínimas possuem unidade e origem próprias. Preservar variantes
entre relatórios, inclusive arredondamentos; não somar máximos nem fabricar uma
nova envoltória. O nome de uma viga receptora na reação identifica a ligação,
mas não o contorno da prancha, sua abscissa ou a combinação de carregamento.
