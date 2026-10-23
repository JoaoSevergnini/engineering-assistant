# ATP S07 - lajes do térreo - rodada inicial de 19/10/2026

Documento de trabalho: output/pdf/ATP_S07_lajes_terreo_mapa_preliminar.pdf (98 páginas).

## Orientações de João nesta conversa
- Horizontal na primeira camada, vertical na segunda.
- Reforços positivos intercalados com a base na mesma camada física.
- Gamma f = 1,4 autorizado também para as resistências equivalentes de lajes.
- Nas sobreposições negativas de apoios distintos, apresentar capacidades individuais; soma pendente de ancoragem.
- Somente PDFs disponíveis.

## Estado
Rodada preliminar, sem aprovação global, sem comparação com solicitações e sem revisão normativa integral. 747 ocorrências candidatas; 662 com espaçamento; 647 com região nominal; 15 associações ainda pendentes. 1049 regiões após partição por composição, espessura e materiais. Nas 319 regiões de composição pendente, o momento composto não é publicado; o PDF apresenta capacidades individuais. Há 73 regiões verticais com hipótese provisória de envelope horizontal de 20 mm.

O resultado oficial é de concretopy.verificar_flexao_viga_retangular. A homogeneização conserva o resultante tracionado e seu centro, diferencia CA60/CA50, normaliza a largura e verifica o escoamento das famílias reais. Gamma c=1,4, gamma s=1,15. Cobrimento físico 3 cm; parametrização geométrica 2,5 cm + argumento de 5 mm no motor, sem estribos físicos nas lajes e sem empilhamento automático. Fontes e resultados brutos preservados.

## Registros principais
- inventario.json: revisões, arquivos, páginas e assinaturas das fontes.
- ocorrencias_extraidas.json: chamadas, bitolas, espaçamentos, coordenadas e pendências.
- regioes_capacidades.json: polígonos, composições, hipóteses e resultados brutos.
- proveniencia_calculos.json e auditoria_equilibrio.json: origem e conferência auxiliar.
- conferencias_visuais_locais_vigentes.json: conferências locais por coordenada.
- cobertura_posicoes_tabela.json: posições da tabela ainda sem conciliação de chamada, sem apontar ausência no projeto.
- geometrias_bloqueadas_triagem.json: associações bloqueadas por incoerência de leitura entre quantidade, espaçamento e faixa.
- notas_armaduras_localizadas_furos.json: notas do detalhe de furos, separadas de faixas distribuídas.
- validacao_pdf.json: paginação, enquadramento, assinatura do PDF e estabilidade das fontes.

## Pendências
Não está concluída a individualização completa de L1/L8, nem a conciliação integral dos contornos, aberturas, apoios, níveis, juntas, materiais por etapa e camadas locais. Não interpretar os retângulos nominais como polígonos executivos de lajes. Candidatas por proximidade exigem revisão específica. A chamada N91 da 7301 não informa espaçamento no rótulo consultado; não se arbitrou As/m. Armaduras localizadas sem faixa definida não foram distribuídas artificialmente por metro.

Continuar a leitura das 15 associações, as posições de tabelas pendentes e os contornos físicos, antes de emitir mapa definitivo. Não tratar essas tarefas ainda não realizadas pelo assistente como dados ausentes do projetista. Ancoragens, cortes, emendas, mínimos de lajes, ELS, cisalhamento/punção e solicitações ainda não foram verificados.

Os arquivos recebidos, o contexto original do ATP, as skills e o Concretopy não foram alterados. A auditoria de assinatura confirmou estabilidade das dez pranchas durante esta rodada. Esta pasta guarda dados locais da revisão; não houve atualização automática de regras permanentes.

## Oito pranchas reapresentadas - solicitação posterior
Criados oito PDFs de uma página, 7301-7308, em output/pdf/pranchas_regioes. Desenho original preservado em escala, com legenda lateral acrescentada. Mesmos 1049 polígonos e resultados do relatório anterior, sem novo cálculo. Regiões com espaço recebem a configuração completa; demais recebem código ligado à legenda. Mrk é o rótulo de apresentação solicitado para |MRd|/1,4. Campos compostos pendentes: As/m -- e Mrk --. Base -- indica ausência de individualização de uma base no registro anterior, e não ausência física de barras. Conferências em validacao_oito_pranchas.json; todas as páginas renderizadas e inspecionadas, sem colisão entre rótulos, códigos faltantes ou alteração dos dados-fonte. As hipóteses e pendências técnicas anteriores permanecem.

