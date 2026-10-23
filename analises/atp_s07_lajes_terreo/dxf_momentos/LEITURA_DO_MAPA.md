# ARP0002 — mapa preliminar dos momentos negativos horizontais

Fonte original preservada; hash em inventario.json. Natureza característica confirmada por João; unidade tf·m/m. Filtro 1,62; isocurva configurada 1,80 (textos no DXF indicam 1,81).

O mapa identifica 457 manchas gráficas, incluindo pequenas ilhas e trechos próximos de zero. Os IDs MN são exclusivos deste mapa; não são as regiões R das pranchas de armadura. Não foi realizada associação com as capacidades nem verificação de segurança.

Reconstrução: entidades LINE das camadas 214 e 224, correspondentes aos trechos negativos (sinal conferido por associação com textos negativos). Os componentes vetoriais foram projetados sobre os eixos horizontais dos diagramas. O eixo foi inferido pela malha geométrica de 17,5 unidades DXF. Os limites transversais são as meias distâncias entre linhas disponíveis; portanto são discretizações gráficas aproximadas, não isocurvas de momento zero comprovadas entre linhas. Não se deve usar esta geometria para comprimento final de armaduras ou ancoragem.

Amplitude: escala ajustada 1,2231103179874525 unidades de desenho por tf·m/m. Há 1.769 associações diretas texto-vértice, das quais 1.763 consistentes usadas na calibração, com desvio máximo 0,01812 tf·m/m. Seis associações discrepantes não integraram o ajuste. A calibração verifica a escala gráfica, não a exatidão do modelo TQS. Valores não rotulados permanecem estimativas gráficas, com precisão limitada pelo desenho; duas casas decimais são apenas a apresentação.

Média indicada: soma das amplitudes médias de cada segmento negativo multiplicadas por sua extensão horizontal Δx, dividida pela soma de Δx, conservando o sinal negativo. Não é média ponderada por área nem média só dos picos. O resultado depende da discretização do desenho. A coluna média dos rótulos no CSV é uma informação distinta, condicionada à associação espacial e enviesada pelo filtro de exibição. O pico gráfico foi registrado separadamente; a média não pode substituir o pico numa futura verificação resistente.

Não houve substituição por −1,61: o desenho preserva as amplitudes também abaixo do filtro. Não houve divisão por γf. Não houve conversão em resistência ou aprovação das lajes.

Arquivos: PNG em alta resolução, prévia PNG, tabela CSV com sinal e unidade, e JSON com geometrias e resultados. O eixo X/Y é o original do DXF. Fonte nunca alterada.
