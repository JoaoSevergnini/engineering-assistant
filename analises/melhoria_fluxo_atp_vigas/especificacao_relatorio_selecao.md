# Relatório ATP: conteúdo, índices e seleção antes da emissão

Proposta atualizada em16/10/2026 conforme pedido de João. Define apresentação e sequência de revisão; não modifica os resultados resistentes nem gera uma nova emissão doS07 nesta etapa.

## Três etapas

1. Verificar inconformidades. Executar o escopo técnico e registrar resultados, divergências documentais e pendências. Cada registro tem identificação estável, viga/trecho/apoio/lado, categoria, dados, fonte, evidência, conclusão e limitações. Ainda não redigir a versão final nem criar marcações nas pranchas.
2. Avaliar os itens da emissão. Apresentar seções selecionáveis e lista completa dos apontamentos com caixas de seleção. João define os itens a incorporar e pode registrar observações. A seleção altera a emissão, não altera a conclusão técnica, não apaga resultados e não aprova um controle. A demonstração interativa contém apenas quatro exemplos; não representa a seleção completa doS07.
3. Redigir os apontamentos e construir o relatório. Consumir a seleção expressamente enviada por João, a versão dos resultados e as fontes correspondentes. Gerar textos, fichas e quadros; marcações em pranchas, quando fizerem parte da entrega, devem ocorrer em cópias. A emissão identifica seu escopo e suas limitações. Não tratar uma caixa previamente marcada como decisão já enviada.

Os itens não selecionados continuam no registro interno. Uma mudança técnica posterior reabre a seleção dos itens afetados; uma mudança de texto não exige recalcular capacidades.

## Seção própria de geometria

A conferência deve confrontar dados reais da forma e do detalhamento, não apenas apresentar a seção adotada no cálculo. Organizar em três quadros para evitar tabelas ilegíveis:

- Inventário: vigas presentes nos dois documentos, somente na forma ou somente no detalhamento.
- Seções e níveis por trecho: b×h da forma, b×h do detalhe, topo/fundo em cada documento, mudanças de altura, resultado e fonte.
- Vãos e apoios: apoios inicial/final, referências das faces, comprimento indicado/obtido em cada documento, diferença e resultado. Separar distância entre eixos, vão entre faces e faixa de estribos; são grandezas distintas.

O TQS aparece como referência de associação dos esforços, separado da comparação forma×detalhamento. Registrar explicitamente as regiões não conferidas. Uma tabela de geometria não autoriza preencher como conformes os vãos ainda não analisados. NoS07, a conferência integral ainda está aberta; o novo quadro deve tornar isso visível.

## Índices nas verificações

Flexão positiva e negativa: índice de utilização ηM=100×Msk/(MRd/γf), usando módulos, com identificação do lado e da região. MRd/γf é resistência equivalente para comparação, não resistência característica do material. Cada lado do apoio conserva a própria demanda.

Exemplo:ηM=120% significa solicitação20% acima da resistência. Não significa automaticamente20% de armadura faltante. A resistência depende da seção, materiais, d, camadas e comportamento da seção.

Para quantificar déficit de aço na flexão, é necessário obter As necessária por dimensionamento oficial compatível com a configuração. Somente então apresentar100×max(As,necessária/As,existente−1,0), indicando as hipóteses. Não produzir As necessária por regra de três entre momentos.

Cortante: apresentar100×(Asw/s necessário)/(Asw/s existente) como utilização da armadura transversal. A taxa necessária inclui o mínimo quando governante. Apresentar separadamente100×Vsk/(VRd2/γf) como utilização da biela. Não denominar Vsk/VRd2 de utilização resistente de todo o mecanismo de cortante. Vsk/Vrk global só deve ser preenchido se a resistência pertinente do conjunto tiver sido efetivamente calculada pelo motor.

Índice100% corresponde à igualdade do controle apresentado; decisão segue os valores completos e o critério do controle, inclusive eventual desigualdade estrita da biela. Denominador nulo, dado ausente ou configuração não verificada produz campo não calculado, com motivo. Mínimos, espaçamentos e validade do detalhe continuam separados do índice.

## Memória de suspensão

Usar dois quadros ligados pela identificação da ligação e da região:

| Quadro | Colunas |
|---|---|
| Esforços e distribuição | Apoiada→receptora;Rk total característico(tf);parcela considerada(%);Vk usado na região(tf);origem do cortante regional ou limite conservador;início/fim da região;método de distribuição;comprimento efetivamente usado(m). |
| Parcelas de armadura | As de suspensão(cm²);Asw/s de suspensão(cm²/m);Asw/s de cortante calculado(cm²/m);soma das duas parcelas;Asw/s mínimo;Asw/s necessário adotado;Asw/s existente;índice de utilização;resultado e pendências. |

A soma deve ser explícita:taxa combinada=taxa de cortante calculado+taxa de suspensão. A taxa necessária adotada é o maior entre essa soma e o mínimo transversal. Não somar o mínimo uma segunda vez à parcela de suspensão.

Distinguir comprimento máximo permitido de distribuição e comprimento efetivamente utilizado com estribos. Apresentar separadamente a parcela na viga apoiada quando for necessária para completar a transferência. Verificar100% do tirante, não encerrar a ligação apenas pelo atendimento de75% na receptora. Sobreposições de regiões exigem a combinação registrada correspondente.

Exemplo real arquivado,V31→V12,C35,parcela75% na receptora:
- Rk=24,46tf;Vk regional≈35,01tf;região0,000–0,825m;L=0,825m.
- As de suspensão=5,792876cm²;taxa de suspensão=7,021668cm²/m.
- Taxa de cortante calculado=1,775651cm²/m;soma=8,797319cm²/m.
- Mínimo=3,081564cm²/m;necessário adotado=8,797319cm²/m;existente=10,053096cm²/m.
- A parcela25% naV31 consta em verificação própria. A área atende numericamente;emenda/ancoragem das peças de estribo continuam a verificar. Não promover este exemplo a aprovação integral da ligação.

Origem:arquivos oficiais já arquivados,suspensao_V31_V12_V41_V13.json e verificacoes_globais_concretopy.json da rodada05. Os valores acima são apresentação dos resultados existentes, não novo cálculo resistente.

## Seleção da emissão

Dois níveis de seleção:
- Seções:geometria,positiva,negativa,cortante,suspensão,pendências e demais conteúdos do escopo.
- Apontamentos:seleção individual por identificação,viga,localização,problema e conclusão técnica.

O registro de seleção deve conter identificação da revisão técnica,assinatura das fontes,seções escolhidas,identificadores dos apontamentos,observações e envio expresso das escolhas. Preservar a trilha dos itens não emitidos. Relatório de falhas selecionadas e relatório global de verificações devem ter seus respectivos escopos identificados.

A seleção interativa apresentada nesta conversa é uma demonstração funcional de preferências,com seis seções e quatro exemplos. Ela permite enviar as escolhas ao chat para revisão. Ainda não substitui o cadastro completo de apontamentos nem está conectada à emissão automática doPDF.


## Preferências encaminhadas pela seleção interativa — 16/10/2026

Selecionadas as seis seções: geometria forma×detalhamento; flexão positiva e mínimos; flexão negativa por lado e mínimos; cortante e espaçamentos; suspensão com esforços, extensão e parcelas; pendências para decisão.

Os quatro exemplos também permanecem selecionados: divergência de altura daV42; resistência negativa daV43/P723; armadura de cortante daV18; emenda/ancoragem das peças de estribo na ligaçãoV31–V12. São exemplos, não o inventário completo doS07. Nenhuma observação adicional foi enviada.

Aplicação no fluxo:1)verificar e registrar os resultados técnicos;2)apresentar a lista completa de seções e apontamentos para seleção;3)redigir os apontamentos e construir a emissão a partir da seleção completa enviada. Esta escolha de demonstração não autoriza emitir um relatório global reduzido aos quatro exemplos. Resultados técnicos e itens não emitidos permanecem preservados; exclusões da emissão são registradas separadamente.

Registro estruturado:preferencias_relatorio_confirmadas.json. Os índices de utilização, a seção própria de geometria e as parcelas de suspensão seguem a especificação de apresentação já proposta. A proposta continua separada da skill ativa e do gerador automático dePDF.
