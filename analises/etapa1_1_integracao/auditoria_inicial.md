# Auditoria inicial — Etapa 1.1

Registro anterior às alterações da Etapa 1.1, em 10/10/2026.

O eixo existente é `physical_geometry.coordinate_system`, em metros. `extend` mantém o modelo `longitudinal_beam_detail` e normaliza segmentos e ocorrências; `project_segments` e `project_occurrences` adaptam esses dados aos verificadores. Não é necessário outro modelo longitudinal.

`section_positions.fill_positions` posiciona as 13 seções VGESFS em cada vão usando comprimento e DEPEV. Essas posições são locais ao eixo físico esquerdo do vão. `map_beam` associa um único vão, incluindo faces/centros dos apoios, converte cm para m e recusa múltiplos vãos/balanços. A Etapa 1 exige `force_position_mapping`, mas ainda não oferece registro comprovado por vão no fluxo de pavimento.

Segmentos contêm limites, seção, níveis e deslocamento lateral com fatos rastreáveis. Ocorrências possuem identidade distinta da marca, quantidade, bitola, camadas e limites. `flexure_regions.decompose_regions` já particiona eventos longitudinais e transversais. `longitudinal_review.check_physical_flexure` utiliza seções constantes locais e `input_preflight`; as transições pontuais continuam inconclusivas. `execute_control` oferece callback protegido para os demais controles. `support_correction.transverse_fit` já contém a verificação de cabimento: será reutilizada sem copiar equações.

As camadas históricas dos quatro casos são hipóteses, não extrações comprovadas de textos próximos. A N2 da V623 existe na reconciliação, mas não possui limites longitudinais comprovados. V610/V611/V626 possuem trechos não localizados; não há seção média admissível.

Os scripts históricos não são entradas do novo fluxo. Somente `regressao_real.py` da Etapa 1 e os testes específicos chamam o preflight; os demais chamadores históricos continuam sujeitos ao contrato legado. A entrega incluirá inventário por arquivo/linha dos chamadores sem guarda.

A unidade S: dos PDFs originais não está montada; o projeto Silva Jardim também não está no C:/TQS disponível. No workspace há PDFs de relatórios e pranchas marcadas, sem planta de formas original identificada. Isso significa **fonte indisponível nesta sessão**, não informação ausente na prancha. Os JSONs preservados permitem regressão documental, sem comprovação nova da forma.

Implementação prevista: interpretação da forma no contrato físico existente; registro local→comum por vão, sem alterar esforços/envoltórias; interpretação de camadas com conflito e convenção explícita; fluxo de pavimento obrigatório, guarda por controle e consolidação existente. Nenhuma alteração no Concretopy, scripts históricos ou PDFs.
