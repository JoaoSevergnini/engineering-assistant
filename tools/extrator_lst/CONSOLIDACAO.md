# Modelo consolidado de viga — versão 1.0

Esta etapa lê exclusivamente o JSON documental produzido por `extrair_viga_lst.py`. Não abre LST, não interpreta suas linhas novamente, não dimensiona e não executa verificações estruturais. O extrator e seus testes anteriores foram preservados.

## Fluxo

```powershell
python extrair_viga_lst.py "C:\TQS\24-155-COLLINE-RESIDENCIAL-R60\DIFERENCIADO\VIGAS" --viga V504 --saida V504_raw.json
python consolidar_viga.py V504_raw.json --saida V504.json
python -m unittest test_consolidar_viga
python -m unittest test_extrair_viga_lst
```

A consolidação recusa entrada e saída iguais. Uma saída consolidada existente é sobrescrita. A entrada permanece intacta. O arquivo `V504_raw.json` entregue é exatamente a saída documental anterior, apenas renomeada.

## Consumo por código

```python
from consolidar_viga import load_beam

beam = load_beam('V504.json')
height = beam.spans[0].geometry.height   # 0.32 m
length = beam.spans[0].geometry.length  # 1.206 m, geometria geral de referência
left, right = beam.spans[0].support_ids # V544, P1A
fck = beam.materials.concrete.fck       # None: consultar warnings
```

Para acessar avisos e rastreabilidade, use `json.load` sobre o documento completo. A API `consolidate(raw_dict)` retorna o modelo completo como dicionário, sem I/O e sem alterar a entrada. `load_beam` oferece apenas a conveniência de acesso por atributos; não resolve pendências.

## Contrato

- `beam.id`, `beam.number`: identificação documental.
- `beam.materials`: concreto (`fck`), aço (`grade`) e dimensão máxima do agregado (`aggregate_max_size`), quando extraídos.
- `beam.cover`: `general`, `top`, `bottom`, `compression_reinforcement`, `additional_top`, `beam_parameter`, `soil_contact_parameter` e `unspecified_face`. Parâmetros de cobrimento não são automaticamente valores efetivos de uma face.
- `beam.spans`: vãos da geometria de referência. Cada um contém `id`, `geometry`, `support_ids`, `report_span_ids` e `internal_forces`.
- `geometry`: `length`, `width`, `height`, larguras das mesas, espessuras das lajes, distâncias entre faces e eixo e `section_type` (código TQS, sem interpretação normativa).
- `beam.supports`: apoios identificados pelo nome, largura, excentricidade e demais dimensões disponíveis nas tabelas normalizadas. Códigos de continuidade e alavanca são preservados. A ordenação dessa lista é pelo identificador; a ligação esquerda/direita é dada por `span.support_ids`.
- `internal_forces`: séries com `quantity` (`shear`, `bending_moment`, `torsion`), `envelope`, `stage`, `unit`, `sections`, `values` e `sources`. `positions` fica null: a extração não documenta abscissas por seção. Não se pressupõe espaçamento uniforme.
- `unassigned_forces`: séries sem associação documental segura a um vão físico, mantendo valores e fontes.
- `warnings`: pendências e divergências documentais; não são avisos de segurança estrutural nem reprodução dos avisos TQS.

Unidades comuns: comprimentos em **m**, tensões em **MPa**, forças em **kN** e momentos em **kN.m**. Valores são números diretamente utilizáveis. Conversões vêm de `normalizado` da primeira etapa. Não são criadas conversões para campos sem unidade. `null` significa ausente, sem unidade utilizável ou conflito não resolvido; os dois últimos casos geram warnings. Zero continua zero.

## Fontes e rastreabilidade

`provenance` relaciona um JSON Pointer do modelo às referências de origem. Exemplo:

```text
/beam/spans/0/geometry/height -> [sNNN#/normalizacao/campos/altura, ...]
```

O prefixo identifica um registro em `sources`, que contém `file`, `lines` (inclusivas, base 1) e `raw_pointer`. O fragmento após `#` identifica o campo dentro desse registro documental. Concatene `raw_pointer` com o fragmento para localizar o dado no JSON raw. `raw#/viga` aponta diretamente para a identificação da extração.

As referências das séries valem para seus metadados e vetores; cada elemento corresponde à mesma posição em `normalizacao.valores` e `normalizacao.secoes`. Propriedades conflitantes conservam referências de todas as alternativas em `warnings`. `raw_document` identifica o JSON de entrada por nome e SHA-256; `source_files` conserva os hashes dos LST utilizados. Nenhuma linha original é copiada ao modelo consolidado.

## Critérios de consolidação

1. **Geometria de referência:** RELDTVGS e VGESFS contêm tabelas gerais de geometria, antes das etapas de dimensionamento/detalhamento. Têm igual prioridade. A preferência é específica para representar essa geometria de entrada, não para declarar uma geometria final ou corrigir outro relatório. Divergências entre essas duas fontes deixam a propriedade null. Diferenças nas fontes de outras etapas ficam em warnings com os valores alternativos e a resolução `preferred_reference_geometry`.
2. **Sem prioridade universal de arquivos:** materiais, cobrimentos e apoios são consolidados por concordância da propriedade. Não existe votação por maioria. A única tolerância numérica (1e-10 absoluto) evita ruído de representação de ponto flutuante; não absorve arredondamentos impressos.
3. **Identidade dos vãos:** as tabelas gerais devem concordar na sequência de identificadores. Tabelas detalhadas só são associadas por ordem quando apresentam dois registros extremos de comprimento zero, a mesma quantidade de vãos positivos e a mesma sequência de apoios únicos, em quantidade n+1. A associação e suas fontes ficam em `report_span_ids` e `provenance`. Não se usa a regra cega “índice menos um”. Resumos FLEXPS/FLEXNG/ESTRIB precisam ter exatamente a mesma sequência de números da referência. Sem essas evidências, a associação fica pendente. Vãos de comprimento zero permanecem no raw; séries não nulas nesses registros ficam em `unassigned_forces` com aviso.
4. **Materiais:** CA50 e CA-50 são normalizações de pontuação. CA-50A não é automaticamente igual a CA-50. 400 kgf/cm² e 40 MPa não são tratados como numericamente equivalentes. Não se interpretam convenções históricas de unidade sem evidência documental adicional.
5. **Cobrimento:** parâmetros geral, de face, adicional e específico da viga não são misturados. O zero do parâmetro da viga não é interpretado como “herdar geral”. Um `c` de cabeçalho permanece sem face identificada; não prevalece sobre os campos explicitamente intitulados superior/inferior.
6. **Esforços:** fases diferentes permanecem separadas. `model_input` reúne as séries de entrada de VGESFS/RELDTVGS; as demais etapas identificam a leitura de flexão positiva/negativa, eliminação de momentos positivos e fases inicial/final em módulo do cisalhamento. Séries idênticas na mesma fase agregam fontes; séries diferentes na mesma fase permanecem como variantes e geram warning. Não são selecionados máximos absolutos nem produzidas novas envoltórias. Lacunas permanecem null e sinais são mantidos como publicados.

## Resultado da V504

Um vão de referência com 1,206 m e seção 0,14 x 0,32 m, apoiado em V544 e P1A. O vão 2 dos relatórios detalhados é associado ao vão físico 1 pelas evidências descritas acima. Há 14 séries de esforços, após agrupar as cópias idênticas de VGESFS e RELDTVGS.

O modelo registra oito avisos documentais: fck, classe de aço, cobrimento sem face, três propriedades geométricas com valores distintos em outras etapas, registros de comprimento zero e excentricidade do apoio. O cobrimento superior/inferior explícito é 0,025 m. fck, classe de aço, cobrimento sem face e excentricidade de P1A permanecem null.

## Escopo inicial e limites

Este modelo inclui as propriedades estruturadas acima. Reações, armaduras, ancoragens, critérios de cálculo e mensagens TQS continuam disponíveis no raw para futuras etapas. Campos não normalizados pelo extrator não são reinterpretados aqui. Assim, a consolidação depende da cobertura documental da primeira camada; não promete interpretar toda sintaxe de outras versões TQS.

Se as tabelas gerais estiverem ausentes ou tiverem topologias conflitantes, a lista de vãos fica vazia com aviso e séries não associadas são preservadas. Não se usa um relatório qualquer como substituto implícito.

Os testes da consolidação são inteiramente sintéticos, em memória ou em diretório temporário. Não importam o extrator e não dependem da pasta TQS, dos LST reais ou do V504_raw.json. Cobrem conflitos, fontes, unidades, ausência de dados, preservação da entrada, múltiplos vãos, numerações diferentes, etapas de esforços, lacunas e CLI. Os testes documentais existentes continuam separados e inalterados.


## Extensao aditiva 1.1 ? comprimentos e reacoes

Referencia permanente: [tqs-beam-data.md](../../.agents/skills/reinforcement-review/references/tqs-beam-data.md).
A entrada documental continua schema 1.0. Campos antigos conservam sua semantica.

- `beam.spans[i].geometry.length`: L_TQS original, nao e vao livre.
- `support_axis_length`: length + eccentricity_left + eccentricity_right, em m.
- `clear_span_length`: support_axis_length - width_left/2 - width_right/2, em m.
- `beam.support_reactions`: observacoes por relatorio com support_id,
  reported_support_name, report_support_number, unit=kN, max, min, file e sources.
  max/min pertencem a mesma linha documental, nao a uma combinacao inferida.

A ordem esquerda/direita usa support_ids; width e a dimensao longitudinal do apoio.
Ausencia/conflito em operandos mantem derivados null e gera derived_geometry_unresolved
com os operandos e suas fontes. Campos com comprimento derivado negativo ficam null
com invalid_derived_geometry. L_TQS e propriedades documentais nao sao substituidos.
A proveniencia dos derivados e a uniao das referencias dos operandos; a formula
consta em policies e, para pendencias, no warning.

Reacoes distintas, inclusive arredondadas, ficam separadas com reaction_variants.
Nao se cria uma envoltoria nem se somam maximos. support_id e null quando o nome
nao pode ser ligado a um apoio consolidado; reported_support_name permanece.
Valores sem unidade normalizada ficam null com warning. Nao se usa DEPEV sem unidade
das tabelas de reacoes para contornar conflito de eccentricity.
As posicoes das 13 secoes continuam null; a regra de vao nao define abscissas.

V501/V503: os operandos de RELDTFPS/RELDTFNG resultam 8,430 m entre eixos e 7,120 m
livres, 0,010 m acima do documental da prancha. Como outros relatorios divergem nas
excentricidades, os campos derivados do consenso integral permanecem null.
Nenhuma prioridade de fonte foi acrescentada para ocultar essa divergencia.
