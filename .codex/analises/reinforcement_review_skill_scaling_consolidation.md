# Consolidação do escalonamento positivo na skill reinforcement-review

05/10/2026. **Procedimento consolidado sem alterar verificações estruturais,
Concretopy ou resultados históricos.** A navegação parte de AGENTS.md para
SKILL.md, referências operacionais, ferramentas existentes e API pública local.

## 1. Arquivos lidos

- `AGENTS.md` e `.agents/skills/reinforcement-review/SKILL.md`.
- Todas as referências de vigas existentes na skill: `beam-review.md`,
  `beam-drawing-convections.md` e `tqs-beam-data.md`.
- `tools/reinforcement_checks/README.md`, `bar_scaling.md`,
  `al_shear_selection.md` e `al_effective_depth.md`. A documentação anterior de
  `engineer_confirmed_bond_condition_v1` estava em `bar_scaling.md`; não existia
  referência específica de aderência nessa skill.
- Relatórios `V1001_N3_scaling_check.md` e `V536_V565_N3_scaling_check.md`.
- Implementações `bar_scaling.py`, `tqs_shear.py`, `moment_diagram.py`,
  `flexure_regions.py` e `positive_flexure.py`; contrato de gravação da CLI
  `v1001_scaling.py` conferido para a orientação de reprodução.
- Concretopy local: `docs/api_publica.md`, `docs/ancoragem.md` e
  `docs/hipoteses_e_limites.md`, incluindo flexão, posições das camadas,
  ancoragem e decalagem al. Não se atribui leitura a uma documentação ausente.
- Skill auxiliar `skill-creator/SKILL.md` e seu `quick_validate.py`.

## 2. Estrutura documental escolhida

O SKILL funciona como entrada e orientação curta do novo procedimento;
os detalhes ficam em referências lidas quando houver um corte positivo no vão.
As outras etapas de revisão e orientações gerais existentes foram preservadas.

```text
AGENTS.md
  reinforcement-review/SKILL.md
    references/beam-review.md
    references/beam-drawing-convections.md
    references/tqs-beam-data.md
    references/positive-bar-scaling.md
      tools/reinforcement_checks/al_shear_selection.md
      tools/reinforcement_checks/al_effective_depth.md
      references/bond-condition.md
      tools/reinforcement_checks/README.md e bar_scaling.md
        ferramentas existentes e Concretopy/docs
```

Relatórios/goldens são exemplos e auditoria, não pré-requisitos para redescobrir
regras. Uma nova sessão encontra evento, seleção das referências, entradas,
chamada pública, resultado e limites na cadeia acima.

## 3. Mudanças no SKILL

Atualizada a sequência para explicitar interpretação de positivos, composição
regional, resistência, escalonamento no vão quando houver interrupção e só depois
ancoragem nos apoios. Inserida seção curta 6.1 com gatilho, referência operacional,
ferramenta pública, bloqueios/conclusão null, provenance e distinção de apoio.

O índice final agora aponta também para revisão geral e convenções de prancha,
além da semântica TQS e do escalonamento. Preservado integralmente o frontmatter,
sem alterar nome, descrição ou política de invocação. Nenhuma fórmula resistente
foi acrescentada ao SKILL.

## 4. Referências criadas/alteradas

| Arquivo | Mudança |
|---|---|
| `.agents/skills/reinforcement-review/references/positive-bar-scaling.md` | Criado: procedimento completo, ferramentas, contratos, A/B, bloqueios, provenance e exemplos validados |
| `.agents/skills/reinforcement-review/references/bond-condition.md` | Criado: fonte específica da regra horizontal confirmada, geometria da barra interrompida, fronteiras e escopo |
| `.agents/skills/reinforcement-review/references/beam-review.md` | Sequência operacional, encaminhamento para corte positivo e correção de links para o nome real do arquivo de convenções |
| `tools/reinforcement_checks/README.md` | Descoberta do procedimento consolidado, regras específicas e goldens; status implementado da seleção de Vk |
| `tools/reinforcement_checks/al_shear_selection.md` | Status histórico explicitamente superado; seleção discreta de ambas as envoltórias/empates e limites do vão amostrado |
| `tools/reinforcement_checks/al_effective_depth.md` | Links para procedimento e distinção entre centroide para al e centro da barra para aderência |
| `tools/reinforcement_checks/bar_scaling.md` | Link operacional, regra de aderência substituída por referência cruzada; precisão da proteção de saídas e comando de reprodução separado |

Não houve exclusão/movimentação de relatórios, goldens, fontes ou provenance.
A única remoção de repetição de regra foi o bloco de fronteiras de aderência do
contrato de ferramentas, agora concentrado em `bond-condition.md` e ligado por
identificador. Os contratos técnicos de integração foram mantidos.

## 5. Regras consolidadas

- Evento por uma marca positiva reta interrompida, em um vão físico mapeado,
  corte left/right, composição before/after orientada ao percurso do corte.
- Capacidade somente da remanescente after, via Concretopy; centros físicos
  preservados ao retirar barras. Capacidade anterior não localiza x_nec.
- Msk VGESFS/M MX., 13 pontos, interpolação consecutiva linear sem extrapolação
  ou discretização artificial; todos os candidatos preservados, seleção pelo ramo.
- `piecewise_linear_positive_peak`, interno ou endpoint com ramo de queda no
  sentido analisado; sem afirmar máximo estrutural exato. Platôs, ambiguidades,
  gaps, ramos não unimodais e ausência de cruzamento permanecem bloqueados.
- Vk: `engineer_confirmed_al_shear_selection_v1`, máximo módulo discreto de
  todo o vão físico amostrado, Q MX./Q MN., com todos os governantes/empates.
- d: `engineer_confirmed_al_effective_depth_v1`, centroide tracionado anterior
  por áreas/posições Concretopy, somente para escalonamento no vão.
- al final limitado via Concretopy, separado de al_base, igual para A e B.
- Aderência: `engineer_confirmed_bond_condition_v1`, centro físico da barra
  interrompida; nunca d_for_al em lugar da posição dessa barra.
- lb básico da interrompida, via Concretopy, sem crédito de gancho/dobra,
  sem substituir por lb_nec/lb_min. O booleano da primitiva não decide B.
- A: disponível desde x_nec ≥ al+10φ da interrompida.
  B: disponível desde o pico da representação ≥ al+lb básico da interrompida.
  Comprimentos orientados, unidades e comparação sem arredondamento registrados.
- true somente com dependências resolvidas e A/B atendidas; false para
  verificação completa com falha; null para inconclusivo. A/B permanecem separadas.
- Rastreabilidade de cada entrada, transformação, referência, chamada/retorno,
  diagnóstico e decisão. Não se substitui a auditoria de hashes do chamador
  por uma simples chamada em memória ao adaptador.

Conservadas as particularidades já validadas: referência de pico no apoio não
habilita verificação desse apoio; remanescente com dobra externa documentada
conserva somente seu segmento reto no cálculo, sem crédito de ancoragem.
Não foram criadas flags ou procedimentos para regimes adicionais.

## 6. Goldens vinculados

- V1001/N3: direita, before N3+N5/after N5, uma camada, dois cruzamentos globais,
  ramo descendente selecionado, pico interno, d_for_al=68,5 cm e resultado true.
- V536/N3 e V565/N3: esquerda, before N2+N3/after N2, duas camadas, d N2=68 cm,
  d N3=64 cm, áreas iguais e centroide=66 cm; pico endpoint; esforços próprios
  para cada membro do detalhe compartilhado; resultados true.

Links relativos para os relatórios, os três JSONs e os testes correspondentes
estão na referência. Nenhum valor do exemplo foi convertido em regra por marca
ou viga. Os testes preservam também V501, V1001 regional, grouped mapping e
moment interpolation.

## 7. Limitações preservadas

Sem ancoragem em apoios, grampos, negativas, suspensão, cisalhamento completo,
armadura mínima, barras comprimidas, benefício de ganchos/dobras, múltiplos
cortes simultâneos ou aprovação global da viga. Uma marca interrompida em várias
camadas, camadas com bitolas misturadas/lacunas e hipóteses de concreto/armadura
não suportadas continuam bloqueadas conforme a implementação.

Posições automáticas Concretopy e cobrimento TQS são dados do procedimento/modelo,
não cotas medidas ou confirmação de execução. Mantidas pendências de definição
da região de apoio e de regras próprias para sua verificação. Escalonamento
atendido não substitui a ancoragem: uma barra pode passar no corte e falhar no apoio.

## 8. Contradições e diferenças históricas encontradas

1. `al_shear_selection.md` dizia “selecao automatica e verificacao N3 nao
   implementadas”; o README repetia esse estado histórico antes de uma seção
   posterior sobre a implementação. A fonte mais recente é o pipeline validado
   e os goldens de 05/10/2026. Status atualizado com nota explícita de superação,
   preservando a regra e a pendência dos apoios. Não há alteração física.
2. `beam-review.md` referia `beam-drawing-conventions.md`, mas o arquivo existente
   chama-se `beam-drawing-convections.md`. Links corrigidos sem renomear o arquivo.
3. `bar_scaling.md` afirmava “Arquivos antigos nao sao sobrescritos”. A CLI
   `v1001_scaling.py` protege entradas/contextos, mas `write_text` pode substituir
   uma saída existente. Corrigida a afirmação com nota explícita e exemplo de
   saída em tmp. Nenhum golden foi regravado. Trata-se de comportamento de I/O,
   não de mudança estrutural ou nova proteção implementada.
4. O relatório V1001 preserva o estado inicial e 223 testes; o caso V536/V565
   acrescenta endpoint/dobra externa sem crédito e registra 232. A consolidação
   usa esse estado validado mais recente, sem reescrever a auditoria anterior.
   A regra de centroide é a mesma, agora exemplificada em duas camadas.
5. A obtenção pela planilha mencionada para negativas em `beam-review.md` não foi
   convertida para este workflow. Negativas continuam fora do escopo; não há
   generalização automática da nova referência.

Não foi encontrada contradição que exija escolha de nova regra técnica.
As correções acima são de status, navegação ou descrição objetiva do comportamento
existente. Se uma futura divergência exigir mudança física/regra, deverá retornar
para decisão do engenheiro antes de alterar cálculo ou conclusão.

## 9. Testes e validação documental

Suíte integral executada com Python 3.10-32 e Concretopy local atual:

| Diretório | Testes | Resultado |
|---|---:|---|
| extrator_lst | 39 | OK |
| beam_model | 30 | OK |
| beam_mapping | 34 | OK |
| reinforcement_checks | 129 | OK |
| **Total** | **232** | **OK** |

Comando por diretório: `python -B -m unittest discover -s tools/<diretorio>
-p 'test_*.py'`. Nenhum teste novo foi necessário para edição documental;
o número permanece 232. Logs da execução estão em `tmp/scaling_consolidation_*_tests.txt`.

Conferidos **48 links locais**, sem alvo inexistente, incluindo os contratos
Concretopy no repositório irmão. `git diff --check` passou. Frontmatter comparado
com HEAD: idêntico; name/description e a navegação do novo procedimento conferidos.

Limitação da validação auxiliar: `skill-creator/scripts/quick_validate.py`
foi tentado em Python 3.10-32 e 3.11 e não iniciou por `ModuleNotFoundError: yaml`.
Não se afirma aprovação desse validador. Não foram instaladas dependências para
esta tarefa documental; a suíte estrutural e a checagem de links/hashes concluíram.

## 10. Confirmação de preservação dos resultados

Comparados SHA-256 antes/depois de **116 arquivos protegidos**, abrangendo
fontes Python das ferramentas, JSONs documentais/goldens em analises/pranchas,
os dois relatórios históricos e fontes Python/documentação pública do Concretopy.
**Nenhuma diferença.** Nenhum resultado físico foi recalculado para substituir
um golden; as execuções de teste verificaram os casos sem regravar seus artefatos.

Auditoria reproduzível: [reinforcement_review_skill_scaling_consolidation_audit.json](reinforcement_review_skill_scaling_consolidation_audit.json),
com contagens, links, limitações do validador e hashes protegidos antes/depois.
Esta tarefa alterou somente documentação e criou referências/artefatos de
consolidação; não implementou novas verificações nem modificou Concretopy.
