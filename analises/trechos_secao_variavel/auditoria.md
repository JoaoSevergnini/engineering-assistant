# Auditoria anterior à implementação

- `concretopy.verificacoes.decalagem.calcular_al(*, concreto, b_cm, d_cm, vk_abs_kn, gamma_f=1.4, gamma_c=1.4)` já é público. Retorna `ResultadoDecalagemAl`, com entradas, Vsd/Vc0 em kN e al em cm. Escopo: estribos verticais, Vc=Vc0, sem efeitos de força normal; concreto 20–90 MPa. Não verifica VRd2. O chamador fornece Vk e d. Não será criada fórmula alternativa ou alterado o Concretopy.
- `physical_geometry.segments` contém intervalos em m e fatos de largura, altura, níveis, offsets, cobrimento e estribo. `form_geometry.apply_form` conserva fonte e pendências. Transições sem cota não podem ser convertidas em pontos.
- `section_positions.fill_positions` identifica as séries VGESFS; `common_axis_registration.register_span` relaciona posições locais ao eixo físico por duas âncoras comprovadas. Max/min e sinais são preservados.
- `MomentDiagram` e `ShearDiagram` já interpolam linearmente sem extrapolação. A seleção deve usar limites e vértices. Falta explicitar descontinuidades informadas, para impedir interpolação através delas.
- `longitudinal_review.check_flexure_regions` / `support_correction.check_longitudinal` executam flexão positiva/negativa com Concretopy. `physical_geometry.project_occurrences` e `flexure_regions.decompose_regions` associam barras e composições aos intervalos. Nenhuma barra será prolongada pelo al.
- `shear_review.check_drawn_region` verifica as peças transversais e `select_shear_depth` já define a escolha de d. `suspension_review.review_connection`, `reaction_area` e `distribution` já calculam suspensão; falta distribuição com menor altura e contextos distintos por subtrecho na transição.
- `floor_review` é a entrada operacional guardada por `input_preflight`. A integração será acionada pelo caso ou automaticamente por mudança de geometria nessa entrada, preservando a execução V607 e os chamadores históricos.

Menor intervenção escolhida: seleção/orquestração no `floor_review` existente; propósito específico para al na guarda existente; consulta de extremos no diagrama existente; proteção de descontinuidades; parâmetros explícitos de distribuição e contextos locais na suspensão. Sem módulos resistentes novos, nova arquitetura ou adaptador genérico.

Dados reais V611: três vãos livres de seção constante, com transições dentro de P19/P10 ainda não cotadas. As barras históricas não têm seus extremos físicos comprovados. Será feita a seleção de esforços possível; cálculos dependentes desses dados permanecerão pendentes.
