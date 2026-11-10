# Relatório, seleção e emissão da ATP de vigas

Consolida a especificação aprovada por João em 16/10/2026 (`analises/melhoria_fluxo_atp_vigas/`). Define apresentação e sequência; não modifica resultados resistentes. Aplicar a [Apresentação de esforços](../../../../profile/force-presentation.md).

## Conteúdo do relatório

- Quadro por viga: geometria, positiva, negativa, mínimo, cortante e suspensão.
- Ficha local: região/apoio/lado, seção, armadura, d, solicitação, resistência ou taxa exigida, resultado e origem do cálculo.
- Resultado técnico separado da execução: atende, não atende, inconclusivo, não se aplica; e executado, a concluir pelo assistente, aguarda informação/decisão.
- Pendência com localização, informação ou verificação faltante, motivo, efeito e responsável. Falta de leitura não é ausência na prancha.
- Legenda com termos por extenso; abreviações explicadas uma vez.
- "Área suficiente" deve indicar qual parcela foi comprovada. Se faltar o funcionamento das peças ou o complemento do tirante, a ligação continua inconclusiva.
- Um relatório vigente e o histórico das revisões; não multiplicar PDFs de trabalho.

O fechamento tem dois registros: cobertura dos controles solicitados e atendimento técnico. Uma ATP pode estar concluída com falhas e pendências documentais identificadas; não pode ser declarada concluída com leituras ou cálculos autorizados ainda não executados pelo assistente.

## Geometria forma × detalhamento

Confrontar dados reais da forma e do detalhamento, não apenas a seção adotada no cálculo. Três quadros:

- **Inventário:** vigas nos dois documentos, só na forma ou só no detalhamento.
- **Seções e níveis por trecho:** b×h da forma e do detalhe, topo/fundo em cada documento, mudanças de altura, resultado e fonte.
- **Vãos e apoios:** apoios inicial/final, faces de referência, comprimento indicado/obtido em cada documento, diferença e resultado. Distância entre eixos, vão entre faces e faixa de estribos são grandezas distintas.

O TQS aparece como referência de associação dos esforços, separado da comparação forma×detalhamento. Registrar as regiões não conferidas; a tabela não autoriza preencher como conformes vãos não analisados.

## Índices

- **Flexão** (positiva e negativa): ηM = 100 × Msk / (MRd/γf), em módulo, com lado e região. MRd/γf é resistência equivalente para comparação. Cada lado do apoio conserva a própria demanda. ηM = 120% significa solicitação 20% acima da resistência, **não** 20% de armadura faltante.
- **Déficit de aço:** só com As necessária obtida por dimensionamento oficial compatível com a configuração: 100 × max(As,nec/As,exist − 1; 0), com as hipóteses. Nunca por regra de três entre momentos.
- **Cortante:** 100 × (Asw/s necessário)/(Asw/s existente) como utilização da armadura transversal; a taxa necessária inclui o mínimo quando governante. **Biela** separada: 100 × Vsk/(VRd2/γf). Não chamar Vsk/VRd2 de utilização de todo o mecanismo. Vsk/Vrk global só se a resistência do conjunto tiver sido calculada pelo motor.
- **Tolerância editorial:** 100% < η ≤ 110% só em flexão, taxa de estribos e suspensão; nunca em biela, mínimo e geometria. Item em cor própria e conclusão técnica preservada ([critérios padrão](default-criteria.md) §2).
- 100% corresponde à igualdade do controle; a decisão segue os valores completos e o critério do controle (inclusive desigualdade estrita da biela). Denominador nulo, dado ausente ou configuração não verificada: campo não calculado, com motivo. Mínimos, espaçamentos e validade do detalhe ficam separados do índice.

## Memória de suspensão

Dois quadros ligados pela identificação da ligação e da região:

| Quadro | Colunas |
|---|---|
| Esforços e distribuição | Apoiada→receptora; Rk total característico (tf); parcela considerada (%); Vk usado na região (tf); origem do cortante regional ou limite conservador; início/fim da região; método de distribuição; comprimento efetivamente usado (m) |
| Parcelas de armadura | As de suspensão (cm²); Asw/s de suspensão (cm²/m); Asw/s de cortante calculado (cm²/m); soma; Asw/s mínimo; Asw/s necessário adotado; Asw/s existente; índice de utilização; resultado e pendências |

Taxa combinada = taxa de cortante calculado + taxa de suspensão; taxa necessária adotada = maior entre essa soma e o mínimo. Não somar o mínimo outra vez à suspensão. Distinguir comprimento máximo permitido de comprimento efetivamente usado. Apresentar separadamente a parcela na viga apoiada quando necessária; verificar 100% do tirante, não encerrar a ligação com 75% na receptora. Sobreposição de regiões exige a combinação registrada: somar as taxas de suspensão no trecho sobreposto ([critérios padrão](default-criteria.md) §5).

Exemplo (S07, V31→V12, parcela 75% na receptora): Rk = 24,46 tf; Vk regional ≈ 35,01 tf; região 0,000–0,825 m; As susp. = 5,79 cm²; taxa susp. = 7,02 cm²/m; cortante = 1,78 cm²/m; soma = 8,80 cm²/m; mínimo = 3,08 cm²/m; existente = 10,05 cm²/m. A parcela de 25% na V31 tem verificação própria; emenda/ancoragem das peças de estribo continuam a verificar. É exemplo de apresentação, não aprovação da ligação.

## Seleção (etapa 2)

Dois níveis: **seções** (geometria, positiva, negativa, cortante, suspensão, pendências e demais conteúdos do escopo) e **apontamentos** (seleção individual por ID, viga, localização, problema e conclusão técnica). Apresentar a lista completa, com caixas de seleção ou lista equivalente; uma demonstração parcial não substitui a lista completa.

### Entrega padrão da etapa 2 (definida por João em 09/11/2026)

A lista de seleção é entregue como **relatório PDF + pranchas anotadas**, no formato das referências do S07 1PAV (`analises/atp_s07_vigas_1pav/output/pdf/ATP_S07_1PAV_RESULTADOS_E_PENDENCIAS_R01.pdf` e `PRANCHAS_ANOTADAS_PONTUAIS_R01/`). A lista em markdown (`selecao_etapa2.md`) continua como registro auxiliar, não como entrega.

1. **Relatório de verificações de todas as vigas** (`<TAG>_VERIFICACOES_SELECAO_ETAPA2_Rxx.pdf`, A4 paisagem): abertura (abrangência, fontes, premissas, convenções, índices, escopo e limites, instruções de uso); quadro geral por viga com link para a ficha; registros gerais (LIM/DOC sem viga); ficha por viga com geometria e registros documentais, flexão positiva e negativa (uma linha por região, inclusive "sem demanda"), armadura mínima (região governante), cortante (uma linha por faixa, com estribo desenhado, Vk, VRd2/γf, biela, Asw/s nec./exist., ηAsw) e suspensão com a viga como receptora.
   - Cada apontamento selecionável (todo item da lista da etapa 2, numerado AP-001… na ordem de `selecao_etapa2.json`) tem na primeira linha do controle uma coluna **"Rel."** com checkbox interativo (`AP-nnn_rel`, desmarcado) e uma coluna **"Comentário (etapa 3)"** com campo de texto multilinha (`AP-nnn_com`). O nome do campo leva o código AP; o rótulo leva o ID estável. Linhas que não são apontamentos não têm campos.
   - Cada AP aparece uma única vez no relatório (campos com o mesmo nome ficariam ligados).
2. **Pranchas anotadas** (cópias, `PRANCHAS_ANOTADAS_ETAPA2_Rxx/<TAG>_<folha>_ANOTADA_ETAPA2_Rxx.pdf`): página 1 = prancha original com marcador e código AP clicável em cada apontamento (barra colorida = faixa avaliada); páginas seguintes = elevação ampliada de cada viga (vetorial, recortada da própria prancha) com marcadores e **quadros**. Todo quadro de incompatibilidade indica **solicitação característica / resistência equivalente** da viga em questão:
   - flexão: `Mk / (MRd/γf)` em tf·m e ηM, com As, d, seção, x; seção T identificada com o valor retangular;
   - mínimo: `As,exist / As,mín` e `Mk / (MRd/γf)`;
   - cortante: `Vk / (VRd2/γf)` (biela) e `Asw/s nec. / exist.` (ηAsw), com estribo e faixa. O motor compara a armadura por taxa; não apresentar VRd3/γf sem que o motor o tenha calculado (ver Índices);
   - suspensão: `Rk`, As,susp e `Asw/s nec. (cortante + suspensão) / exist.` com η; D26 identificado; suspensão especial com a referência de 100% da reação;
   - geometria e documentais: a constatação.
   Cores: vermelho = não atende; âmbar = tolerância 100% < η ≤ 110% ou revisão de João; azul = geometria/documental.
3. **Leitura de volta:** João marca e comenta no PDF e o devolve. `emitir_etapa2.py --ler <pdf>` lê os campos e grava `selecao_lida.json`; `--registrar` grava `selecao_enviada` em `selecao_etapa2.json` somente quando João declarar a seleção enviada. Os comentários alimentam a redação da etapa 3.

Gerador: [`scripts/emitir_etapa2.py`](../scripts/emitir_etapa2.py) (PyMuPDF; contrato de entrada no cabeçalho). Valores vêm do índice, sem recalcular; VRd2/γf é obtido pela razão do próprio motor (Vk/ηbiela). Apontamentos sem detalhamento (sem posição em prancha) aparecem só no relatório e são listados em `assinatura.json`.

O registro da seleção contém: identificação da revisão técnica, assinatura das fontes, seções escolhidas, IDs dos apontamentos, observações e envio expresso. A seleção altera a emissão, não altera a conclusão técnica, não apaga resultados e não aprova controles. Caixa previamente marcada não é decisão enviada. Itens não selecionados permanecem no registro interno. Mudança técnica posterior reabre a seleção dos itens afetados; mudança de texto não exige recalcular.

## Emissão (etapa 3)

Redigir apenas a partir da seleção enviada, da versão dos resultados e das fontes. Marcações em pranchas são feitas em cópias. A emissão identifica escopo e limitações; relatório de falhas selecionadas e relatório global de verificações têm escopos identificados. Checkboxes interativos usam IDs estáveis e estados iniciais explícitos, validados conforme a skill de PDF.
