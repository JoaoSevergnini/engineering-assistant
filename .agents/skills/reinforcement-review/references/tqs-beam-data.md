# Semântica dos dados de vigas do TQS

Referência permanente para as ferramentas de extração, consolidação e revisão de vigas.
Regra confirmada por João em 02/10/2026. Não constitui verificação estrutural.

## Comprimento do vão, DEPEV e distância entre apoios

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
Outros relatórios divergem nas excentricidades; o consenso permanece null.
Este exemplo não autoriza escolher essa fonte como preferencial.

## Seções de esforços e reações

A regra de comprimentos não define as abscissas das 13 seções de esforços.
Não assumir distribuição uniforme, origem em face/eixo ou deslocamento de pontos
apenas pelos índices. Manter positions=null enquanto faltar evidência suficiente.

Reações máximas/mínimas possuem unidade e origem próprias. Preservar variantes
entre relatórios, inclusive arredondamentos; não somar máximos nem fabricar uma
nova envoltória. O nome de uma viga receptora na reação identifica a ligação,
mas não o contorno da prancha, sua abscissa ou a combinação de carregamento.
