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
Quando PDF e DXF correspondentes estiverem disponíveis, aplicar a [prioridade de extração e conferência entre formatos](incremental-floor-workflow.md#pdf-e-dxf-correspondentes): DXF para extração estruturada reutilizável e PDF para validação visual dirigida, após conferir revisão e abrangência. Divergências entre representações continuam conflitantes até conciliação; a prioridade operacional não estabelece superioridade técnica automática.

## Orientações transferidas do SKILL.md (06/11/2026)

Nas novas revisões, aplicar [documentary-physical-preflight](documentary-physical-preflight.md) para conciliação de documentos, ocorrências físicas, geometria por trecho e liberação local das entradas. Este procedimento preserva os métodos resistentes existentes e a compatibilidade dos contratos antigos. Restrições específicas da Etapa 1 prevalecem sobre requisitos de módulos posteriores: não tornar obrigatórios pinos, trajetórias curvas, interferência com armaduras de pilares ou combinações concomitantes.
