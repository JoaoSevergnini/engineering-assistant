# ATP S07 — Vigas do térreo: levantamento e sequência

Data: 14/10/2026. Etapa: abertura documental e planejamento. Decisão e revisão final: João.

## Escopo

ATP de terceiros segundo a ABNT NBR 6118:2023: coerência entre formas e detalhamento; inventário nos dois sentidos; resistência à flexão positiva e negativa nos máximos pertinentes e armadura mínima; cortante, mínimo transversal e espaçamentos; suspensão em apoios indiretos. A menção a armadura positiva no item de momento negativo foi interpretada como armadura negativa.

Não aplicar padrões internos, otimização, mínimo prático de estribos de 8 cm, bitolas usuais ou número usual de ramos como critérios de conformidade. Não ampliar automaticamente esta etapa a escalonamento, ancoragem, emendas, ELS ou torção; eventual dependência ou caso fora do método fica explicitamente pendente. Resultado favorável nestes controles não aprova globalmente a viga.

## Documentos consultados

Contexto: DOCUMENTACAO ATP/CONTEXTO ATP S07.md, lido integralmente. Skill: reinforcement-review, incluindo fluxo operacional de pavimento, validação física, cortante e suspensão. Norma disponível: DOCUMENTACAO ATP/NBR_6118_2023 - CONCRETO NOVA.pdf; itens 18.3.3.2 e 18.3.6 consultados visualmente nesta abertura (páginas impressas 150–152). Os itens de dimensionamento e mínimos resistentes serão consultados antes dos respectivos cálculos; não estão todos auditados nesta abertura.

| Pasta | Prancha/revisão recebida | Conteúdo conferido visualmente |
|---|---|---|
| FORMAS | 7202 R03 | Formas do térreo, parte 1; reservatórios, níveis locais e etapas de concretagem |
| FORMAS | 7214 R01 | Formas do térreo, parte 2; continuidade junto ao eixo D e região em +8,88 m |
| TÉRREO | 7401 R00 | V1–V20; grupos V7=V8=V9=V10, V12=V13 e V19=V20 |
| TÉRREO | 7402 R00 | V21–V32 e V39 no grupo V29=V39 |
| TÉRREO | 7403 R01 | V33–V38 e V40–V50 |
| TÉRREO | 7404 R00 | Elementos PAR dos reservatórios e mísulas; representação própria |

Cada PDF tem uma página. Arquivos completos, caminhos e hashes constam em inventario_pranchas.json. A pasta existente chama-se FORMAS. Títulos e existência não comprovam a última emissão do projetista nem a cobertura integral.

A leitura dos títulos das 7401–7403 indica V1–V50; conciliação individual com a forma ainda não executada. Na 7404 foram lidos títulos PAR701, PAR702, PAR703, PAR704=PAR705=PAR709=PAR710, PAR707 e PAR708. Conferir remissões, todas as ocorrências e a representação de PAR706 antes de concluir falta de detalhamento. Classificar a função dos PAR e das vigas muito altas/curtas antes de aplicar método de viga usual.

As demais pranchas 7301–7308 também existem no TÉRREO, mas não integram o conjunto principal de vigas indicado por João; usar apenas se houver remissão pertinente.

## Premissas e decisões anteriores preservadas

- Nível principal do térreo: +9,18 m. Topos e fundos locais devem ser individualizados; não aplicar translação uniforme.
- P791: topo local +8,88 m, confirmado por João; a interpretação anterior em +9,18 m foi descartada.
- P799: manter a correção de 8,88 para 9,18 no contexto do lance/espera e o intervalo correto de 478 cm. P807C: referência da espera em 9,18 e correção de 508 para 478 cm. Essas correções não mudam automaticamente todos os níveis locais da forma.
- V49: topo local +9,55 m no encontro com P749. Referências +9,28/+14,72/+9,55 dos casos anteriores são locais, não substituem os níveis principais.
- Reservatórios: primeira concretagem até +9,28 m para P702/P703/P704/P709/P710/P711, conforme confirmação registrada de João.
- As formas indicam regiões/limites de primeira e segunda etapa, faixa de concretagem em segunda etapa e concretos de 40 e 35 MPa. Os detalhes assinalam em rosa regiões de primeira etapa. Reconciliar os limites por trecho e por altura antes de escolher materiais; não impor um fck único ao térreo. A confirmação de C40 dos blocos não é comprovação do concreto de todas as vigas.
- Dimensão máxima do agregado registrada: 16 mm. Para o mínimo longitudinal entre estribos, ainda é necessário conhecer o equipamento/procedimento de adensamento aplicável.

## Fontes TQS localizadas

Modelo: C:/TQS/25-208-ATP___24-1454-WERT-WPBGR RESIDENCE-PE-MU2-S07-ATP2___2aFASE-Calc01/TÉRREO.

TÉRREO.LST: geometria/modelador, processamento de 12/10/2026, referência principal 9,18 m. Na subpasta VIGAS: VGESFS.LST (momentos, cortantes e reações), RELDTVGS.LST (legendas e resultados de dimensionamento/detalhamento), NOMVIG.DAT e arquivos de projeto. VGESFS e RELDTVGS foram consultados por amostra, sem normalização completa das unidades ou validação da correspondência de todas as vigas. Não inferir solicitações da quantidade de aço desenhada.

**Pendência inicial comprovada na amostra V1:** forma 7202 R03 e detalhe 7401 R00 indicam 30×55 cm; VGESFS.LST informa largura 0,300 e altura 0,500 m. Os documentos coincidem entre si nessa seção, mas o modelo amostrado difere em altura. Resolver identidade/revisão/geometria do modelo antes da conclusão resistente de V1. Isto não demonstra, sozinho, insuficiência de aço.

## Sequência proposta

1. **Consolidar documentos e ocorrências.** Individualizar todas as vigas das duas formas, detalhamentos agrupados e elementos PAR. Produzir conjuntos forma→detalhe e detalhe→forma, incluindo remissões, duplicidades e elementos especiais. Não contar apenas o número de desenhos.
2. **Conferir geometria por viga e trecho.** Seções, vãos livres/eixos, apoios e faces, orientação, mudanças de seção, topo/fundo, desníveis e continuidade entre 7202/7214. Associar etapas e materiais aos trechos físicos. Priorizar V42/P791/P797/P807C, V49/V50, reservatórios e cruzamentos das etapas; usar V1 como piloto de conciliação documental/modelo.
3. **Conciliar o modelo e preparar as entradas.** Validar identidade, revisão, geometria, materiais, coeficientes, unidades, natureza característica/de cálculo e posições dos esforços. Preservar sinais e envoltórias. Relacionar barras reais, camadas e altura útil às seções verificadas; sem distribuição comprovada, não adotar primeira camada por convenção interna. Usar o fluxo floor_review com liberação por controle, sem aprovação pela simples presença de dados.
4. **Flexão positiva e negativa.** Para cada vão/região pertinente, comparar capacidade da composição efetivamente presente na seção de máximo solicitante com a solicitação de cálculo; conferir mínimo da seção/face aplicável. Em seções ou composições variáveis, verificar os máximos próprios, sem transportar o aço de outra região. Limitar a conclusão aos controles solicitados; não declarar ancoragem/escalonamento aprovados.
5. **Cortante.** Nas faixas reais de estribos, selecionar o máximo próprio da solicitação e verificar compressão diagonal, resistência transversal, mínimo, número de ramos, espaçamento longitudinal máximo e espaçamento transversal entre ramos. Conferir mínimo longitudinal pela passagem do vibrador/adensamento (18.3.3.2), mantendo pendência se faltar a informação; não impor 8 cm.
6. **Suspensão.** Provar quem apoia quem e obter reação total com natureza/unidade/combinação. Classificar faces e situação pendurada ou não; dimensionar suspensão e distribuição conforme 18.3.6, combinando com armadura de cisalhamento/torção pertinente sem duplicar área. Não aplicar 75% automaticamente: o procedimento da skill exige compatibilização com o caso normativo, incluindo eventual parcela na viga apoiada e condições para redução.
7. **Consolidar por viga e controle.** Registrar OK, corrigir, verificar/inconclusivo ou caso especial; fonte, região, item normativo efetivamente consultado e dependência. Manter separadas falhas geométricas, falhas resistentes e pendências. Não editar PDFs ou gerar propostas nesta abertura.

## Resultado desta etapa

Levantamento das seis pranchas e sequência definidos. Nenhuma verificação numérica de resistência concluída; nenhuma viga aprovada. Próxima entrega: matriz individual forma×detalhe e geometria por trecho, com etapas/níveis, antes dos cálculos dependentes.
