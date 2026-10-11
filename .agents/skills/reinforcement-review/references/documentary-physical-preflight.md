# Validação documental e geometria física antes dos cálculos

Aplicar o [contrato da Etapa 1](../../../../tools/beam_model/STAGE1_CONTRACT.md) nas novas revisões com documentos incompletos, marcas repetidas ou geometria variável.

1. Separar posição documental, ocorrência física e representação. Reconciliar elevação/corte/tabela sem presumir ausência física por ausência de extração. Registrar cobertura e integridade.
2. Usar seção e limites por trecho, com origem e estado de evidência. Não preencher transições por escala gráfica ou por comprimento de distribuição dos estribos.
3. Preservar tokens B do VGESFS e conferir orientação e limites físicos; não classificar balanço como término em pilar.
4. Usar preflight por controle/região; executar só as dependências disponíveis. Resultado de hipótese deve permanecer condicional. Distinguir estado técnico de estado de execução.
5. Preservar ancoragem simplificada, envoltórias TQS e convenção confirmada da face externa do pilar terminal não cotado. Esta etapa não exige combinações concomitantes, seção T, verificação de pinos, trajetória curva ou interferência com armaduras de pilares.

V623 do Silva Jardim: N2, 4Ø16 C464, consta na tabela/corte; o usuário confirmou truncamento da elevação na plotagem. Registrar falha de integridade e posição longitudinal não verificável. Nunca converter isso em ausência da armadura positiva.

Auditoria e regressões: `analises/etapa1_leitura_geometria/`. Não editar pranchas ou gerar propostas de melhoria quando o escopo solicitado for somente esta etapa.

Para pavimentos completos, aplicar obrigatoriamente [Etapa 1.1](floor-operational-review.md), com forma, detalhamento, TQS e cabimento antes da resistência. Scripts históricos sem guarda não substituem a entrada protegida.
