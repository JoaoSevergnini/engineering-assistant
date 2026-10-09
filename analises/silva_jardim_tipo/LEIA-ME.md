# Revisão de armaduras — Silva Jardim TIPO

A entrega principal é **Relatorio_revisao_vigas_TIPO_FINAL.pdf**, com 20 páginas e registro individual de V601 a V629. As versões HTML e Markdown contêm o mesmo conteúdo, com recortes das pranchas. Nenhuma proposta de melhoria ou alteração nos PDFs de projeto foi executada.

As conclusões distinguem insuficiência de um ensaio, resultado conservador, requisito do escritório e pendência documental. Não há aprovação global das vigas.

## Arquivos de consulta

- `flexao_por_regiao.csv`: 333 regiões, incluindo não aplicáveis e inconclusivas.
- `cortante_por_faixa.csv`: 66 faixas dos vãos principais; balanços no JSON específico.
- `geometria_por_vao.csv`: apoios, seções e comprimentos livres.
- `ancoragem_positiva_extremos.csv`: extremos físicos, com lados em balanço separados.
- `ancoragem_negativa_extremos.csv`: geometria reta/dobra, critério do escritório e capacidade terminal.
- `revisao_consolidada.json`: dados atuais organizados para consulta.
- `diagnostico_por_viga.json`: consolidação formal por beam_diagnostic, preservando execução, falhas, pendências e revisão de engenharia.
- `source_manifest.json`: caminhos, tamanhos e SHA256 dos 4 PDFs e 13 LST lidos.

## Evidências e precedência

As extrações originais, recortes e adaptadores estão nesta pasta. As fontes originais do projeto não foram modificadas. Os arquivos `*_review.json` contêm o ensaio inicial por regiões; seu cortante com hipótese uniforme CA50 foi substituído por `shear_review_actual_steel.json`. A transcrição provisória da marca positiva da V623 foi corrigida no relatório: **N2 4 Ø16 C464**. Classificações END nos lados que continuam em balanço foram separadas na entrega final.

`anchorage_review.json`, `cantilever_review.json`, `executability_review.json` e `suspension_regional_review.json` conservam as etapas específicas. Os resultados condicionais de gancho e suspensão não aprovam o nó físico. O pacote ZIP contém a entrega de consulta; os LST/PDF originais e extrações extensas permanecem fora do pacote.
