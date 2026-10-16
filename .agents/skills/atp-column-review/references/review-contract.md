# Contrato de revisão e integração das skills

## Identidade, dados e critérios

Identificar cada controle por `(pilar, trecho, controle)`. O trecho corresponde
a um intervalo físico com referências inferior e superior; índice de lance ou
pavimento é localizador, não definição suficiente da geometria. Um nó ou uma
emenda pode exigir registro próprio associado aos lances adjacentes.

Preservar fontes e leituras originais por domínio: `forma`, `detalhamento`,
`tqs` e `norma`, com documento/revisão, localização e evidência. Distinguir
valor documentado, inferência por convenção comprovada, hipótese de engenharia,
conflito e ausência. Dados ausentes ou conflitantes não viram zero nem entradas
confirmadas. Registrar a conversão de unidades e a hipótese quando houver.

O critério deve indicar origem, referência, edição/revisão e consulta efetiva.
No padrão existente, `NORMATIVE` identifica norma, `SOFTWARE_CRITERION` o
software, `OFFICE_STANDARD` o padrão interno e `ENGINEERING_ASSUMPTION` uma
hipótese. Requisito específico do projeto precisa de documento contratual ou
técnico identificado; não reclassificá-lo como norma. No ATP, um padrão interno
pode ser observação explicitamente separada, mas não fundamenta reprovação.

## Três informações independentes

1. **Comparação documental:** valores coincidentes, divergentes ou inconclusivos,
   sempre com o par de fontes e o controle a que se referem.
2. **Resultado técnico do controle:** usar `PASS`, `FAIL`, `INCONCLUSIVE`,
   `NOT_EVALUATED` e `NOT_APPLICABLE` ao integrar com os verificadores existentes.
   `PASS` se restringe ao requisito comprovado. Diferença para uma seleção TQS
   não é `FAIL` resistente; coincidência tampouco é `PASS` resistente.
3. **Execução:** manter separada do resultado, seguindo o diagnóstico existente:
   `NOT_EXECUTED`, `PARTIALLY_EXECUTED`, `EXECUTED_INCONCLUSIVE` ou
   `EXECUTED_COMPLETE`. Um controle concluído com falha pode ter execução
   completa. Preencher com a execução comprovada, sem deduzir esse estado apenas
   da quantidade de registros.

Adaptar explicitamente os resultados locais; não renomear contratos existentes
nem tentar alimentar o consolidador de vigas com registros de pilares.
As convenções compartilhadas de execução estão em
[diagnostic_update.md](../../../../tools/reinforcement_checks/diagnostic_update.md).

## Compatibilidade com a matriz histórica de geometria

A matriz e o auxiliar de cobertura de geometria conservam os estados
`COINCIDENTE`, `COINCIDE_REFERENCIAS`, `DIVERGENTE`, `PENDENTE`, `NAO_EXAMINADO`
e `NAO_APLICAVEL`. Não alterar dados antigos para padronização cosmética.

- `COINCIDENTE` comprova somente a comparação documental indicada.
- `COINCIDE_REFERENCIAS` comprova o intervalo calculado, sem aprovar cota direta.
- `DIVERGENTE` mantém o conflito documental demonstrado, sem atribuir
  automaticamente consequência resistente.
- `PENDENTE` conserva motivo e dependência; `NAO_EXAMINADO` registra falta de execução.
- `NAO_APLICAVEL` exige justificativa, assim como `NOT_APPLICABLE` nos motores.

Ao apresentar uma vista unificada, manter o estado original e acrescentar a
interpretação específica do controle, a execução e as fontes. Não apagar uma
falha comprovada porque outro controle está inconclusivo.

## Consolidação e cobertura

Separar contagens por etapa e controlar todos os identificadores do inventário.
TQS sem seleção, grupo ambíguo, forma não recebida e distribuição não definida
permanecem visíveis. Classificar registros não significa concluir controles.

Consolidar falhas, pendências e solicitações de revisão por ocorrência física;
não presumir que ocorrências próximas tenham causa ou correção comum.
Uma pendência de nó não invalida uma leitura independente de Ø, mas impede
concluir o item completo. Limites numéricos conhecidos não substituem execução
de controles ainda não examinados.

Soluções não solicitadas permanecem não selecionadas. Um apontamento ATP pode
pedir esclarecimento ou compatibilização sem produzir alteração pronta para
execução. Eventual correção autorizada exige reverificar os controles afetados.

## Revisão de pranchas comentadas

Confirmar com o autor o significado das cores e símbolos. A marcação é resultado
da revisão para o dado indicado, não aprovação automática de todo o pilar.
Distinguir informação original, comentário do engenheiro, proposta de correção
e revisão formal do projetista. Confrontar os comentários com os registros
anteriores, separando controle já concluído, pendência aprofundada e controle
não executado. Incorporar novos procedimentos somente depois de esclarecer
as referências físicas e o alcance da conclusão.
