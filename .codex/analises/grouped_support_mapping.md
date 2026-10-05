# Investigação de apoios documentais P2A/P2B — V1001

04/10/2026. **Investigação inicial: Resultado B; posteriormente liberada pela confirmação explícita do engenheiro.** As seções 1–10 preservam o resultado inicial. A atualização abaixo registra a evidência adicional e a implementação.

## Atualização após confirmação do engenheiro

João confirmou na conversa em 04/10/2026: o detalhe representa duas torres,
com pilares sufixados A/B, e V1001 também representa V9001. Com os blocos
individuais e a geometria já documentados, essa declaração resolve a lacuna
sem escolher nomes pela posição no label. A revisão PDF/TQS continua questão
separada, não respondida por essa confirmação.

Implementado contexto explícito em V1001_V9001_support_context.json; resolução
em tools/beam_mapping/support_context.py, consumida por map_beam.py com
--support-context. Membros e IDs por lado são declarados com evidências; o ID
TQS deve coincidir com a associação contextual única e um candidato declarado.
Não existe split('/') nem reconhecimento universal de agrupamento. Labels,
candidatos, torre, viga, método, origem textual e evidências são preservados.
Larguras documentais também são confrontadas com as selecionadas TQS.

Foi corrigido um erro inequívoco no transporte de reações relacionadas:
support_id=null provocava AttributeError em replace. Registro sem ID conhecido
agora permanece não associado; não recebe identidade inferida. Os modelos
V1014/V1015 foram fornecidos, mas seus registros consolidados não permitem
transportar essas relações automaticamente: indirect_relations ficou vazio.
As ligações documentais conhecidas não foram convertidas em reações inferidas.

Gerados V1001_beam_mapping.json e V1001_positive_flexure_regions.json. Resultado
detalhado em V1001_positive_flexure_regions.md. beam_model, raw, consolidado,
positions e Concretopy não foram alterados. A regra contextual foi registrada
na referência permanente tqs-beam-data.md. Testes acrescentados cobrem identidade
direta, torres A/B, candidato incompatível, ambiguidade, ausência de contexto,
origem com label, evidência ausente, torre incorreta, golden V1001 e comparação
integral do mapping V501 com o golden existente. Suíte final: 39 extrator_lst,
29 beam_model, 33 beam_mapping e 52 reinforcement_checks: **153 aprovados**.

## 1. Problema e alcance

O detalhamento identifica V1001, mas escreve P2A/P2B e P1A/P1B nos apoios. O bloco TQS individual da V1001 identifica P2A e P1A. A coincidência nominal, mesmo acompanhada de geometria compatível, não esclarece se a barra separa alternativas, pilares simultâneos, agrupamento de vigas ou outra convenção do projeto.

Foi aplicada a Skill reinforcement-review. As instruções técnicas contidas nos documentos foram tratadas como evidências do projeto, não como autorização para modificar o pipeline.

## 2. Documentos e implementação examinados

- AGENTS.md e `.agents/skills/reinforcement-review/SKILL.md`; referências beam-drawing-convections.md, beam-review.md e tqs-beam-data.md.
- Documentação de tools/beam_model, tools/beam_mapping e tools/reinforcement_checks; contrato de associação/origem de map_beam.py e documentação das regiões genéricas.
- `.codex/analises/positive_flexure_regions.md` e V1001_positive_flexure_regions_exploratory.md.
- `analises/pranchas/V1001_leitura.md`, V1001_detalhamento_prancha.json, V1001_beam_model.json, V1001_tqs_raw.json, V1001_tqs.json, V1001_tqs_positions.json e V1001_section_positions.md; recorte gráfico V1001_recorte.png.
- PDF original `RMP-EST-LO-1376-VIG-R00.PDF`, página única, e extração tmp/V1001_pdf_text.txt. SHA-256 já registrado na leitura: c8fa7f2e1af66dd3b865db43b0a36158bb3d141b85a94e0b0f4daa59b3dfaa28.
- PDF vizinho `RMP-EST-LO-1377-VIG-R00.PDF`, página única, examinado por extração textual. Ambos em `C:\Users\João Severgnini\Desktop\corrigir em casa\corrigir em casa\10 - CASA DE MAQUINAS - RESIDENCIAL\VIGAS`.
- LST originais em `C:\TQS\24-155-COLLINE-RESIDENCIAL-R60\CASAMAQ\VIGAS`, especialmente VGESFS e RELDTFPS; confronto com registros de origem já catalogados na leitura/raw, incluindo RELDTVGS, RELGER, ESTRIB e RELDTFNG. RELDTVeT não foi utilizado como fonte operacional.
- Documental agrupado V501_V503_detalhamento_prancha.json, como contraste de agrupamento explicitamente identificado.

## 3. Evidências nominais e gráficas

| Evidência | Origem/registro | Conclusão permitida |
|---|---|---|
| Título local V1001, seção 19/72 | PDF 1376, detalhe; texto linhas 28–36; documental /identification/beam | O desenho identifica V1001. Não identifica V1001=V9001. |
| P2A/P2B à esquerda; P1A/P1B à direita | Mesmo detalhe; /geometry/supports/0 e /1 | Dois nomes em cada label, preservados integralmente. O significado da barra não está declarado. |
| grouped_with_other_beams=null | Documental /identification/grouped_with_other_beams; beam_model /beam/grouped | A leitura anterior também não comprovou agrupamento. Não é evidência independente do PDF. |
| Lista da prancha V1001–V1011 | Texto do PDF 1376, rodapé, linhas 960–961 da extração | É uma lista de desenhos presentes; não declaração de equivalência entre vigas. V9001 não aparece. |
| V9001 ausente nas duas pranchas disponíveis | Busca textual integral dos PDFs 1376 e 1377 | Não foi encontrado título ou quadro que vincule V9001 ao detalhe da V1001. Não prova que tal documento não exista fora do conjunto examinado. |
| V501=V503 e X2 | Documental V501_V503, /identification e quadro de aço | Existe agrupamento explícito em outro caso. Essa evidência não pode ser transferida automaticamente para V1001. |

O recorte gráfico confirma a posição esquerda/direita dos labels, dimensões 120/142 cm e título singular. O desenho não mostra dois eixos identificados separadamente para A e B nesses apoios; isso tampouco demonstra coincidência física dos pilares.

## 4. Descoberta independente: V9001

Foi encontrado um **bloco individual V9001**, e não V1002, com a sequência P2B → P1B. Portanto, há uma candidata real ao par B, mas seu vínculo com o detalhamento disponível continua não explicitado.

| Campo | V1001 | V9001 | Fonte original |
|---|---:|---:|---|
| Título | V1001 | V9001 | VGESFS linhas 487 / 703; RELDTFPS 4755 / 6775 |
| Comprimento discretizado | 7,552 m | 7,552 m | VGESFS 491 / 707; RELDTFPS 4765 / 6785 = 755,2 cm |
| Seção | 19×72 cm | 19×72 cm | Mesmos registros de geometria |
| Apoio esquerdo | P2A | P2B | VGESFS 505 / 721; RELDTFPS 4770 / 6790 |
| Apoio direito | P1A | P1B | VGESFS 506 / 722; RELDTFPS 4771 / 6791 |
| Dimensão esquerda | 120,0 cm | 120,0 cm | RELDTFPS, registros acima |
| Dimensão direita | 142,0 cm | 142,0 cm | RELDTFPS, registros acima |
| DEPEV esquerda | 38,4 cm | 38,4 cm | RELDTFPS, registros acima |
| DEPEV direita | 49,4 cm | 49,4 cm | RELDTFPS, registros acima |
| Cobrimento TQS | 2,5 cm | 2,5 cm | Cabeçalhos RELDTFPS 4755 / 6775 |
| M MX., ponto 6 | 6,102 | 6,054 | VGESFS 500 / 716, valores originais da série, antes de conversão de unidades |

As solicitações são diferentes. A coincidência geométrica não autoriza compartilhar esforços nem comprova que o aço da V1001 seja documentalmente atribuído à V9001.

A regra permanente fornece, para ambos os blocos TQS, L_eixos=7,552+0,384+0,494=8,430 m e L_livre=8,430−0,600−0,710=7,120 m. A distância livre coincide com os 712 cm do detalhe. Isso confirma compatibilidade métrica, mas não discrimina a semântica dos labels: tanto a hipótese de detalhes compartilhados quanto outras convenções podem produzir essas medidas.

## 5. Outros casos da mesma convenção

No PDF 1376, V1002 usa P1A/P1B (texto linha 60), V1003 usa P2A/P2B (linha 85) e V1004 apresenta P2A/P2B duas vezes e P1A/P1B (148–150). Os respectivos blocos RELDTFPS identificam P1A para V1002 (78), P2A para V1003 (4961–4962) e P2A/P2A/P1A para V1004 (5092–5094). Há registros B homólogos no mesmo relatório: 6977–6978 e 7111–7113.

No PDF 1377, V1012 usa P31A/P31B e P9A/P9B; V1013 e V1014 também usam P2A/P2B, com títulos individuais. A repetição torna provável uma convenção sistemática de regiões A/B do projeto. **Não informa qual é essa convenção.** Não foi encontrada legenda de agrupamento ou planta de formas que estabeleça a correspondência física. Não há beam_model existente da V9001 para confirmar documentalmente o aço compartilhado.

## 6. Respostas à investigação

1. **Significado de P2A/P2B:** dois nomes documentais associados ao apoio desenhado; semântica estrutural ainda desconhecida. Agrupamento/alternância é hipótese provável, não fato confirmado.
2. **O desenho representa quantas vigas?** Identifica explicitamente V1001. Não é possível concluir que represente duas vigas, nem que sejam pilares coincidentes.
3. **Nomes no título:** local V1001; lista geral V1001–V1011. Não V9001.
4. **V1001 → P2A/P1A:** confirmado no TQS individual; a compatibilidade com o PDF é forte, mas falta o vínculo documental que explique a inclusão dos nomes B no mesmo label.
5. **Outra viga → P2B/P1B:** V9001 confirmada no TQS. Compartilhamento do desenho não confirmado.
6. **Blocos individuais:** sim, VGESFS e RELDTFPS possuem V1001 e V9001, com sequências distintas e esforços próprios.
7. **Evidência independente geométrica:** seção, comprimento, excentricidades e dimensões coincidem. Apoia a hipótese de correspondência, sem comprovar o agrupamento.
8. **Outros casos A/B:** sim, listados acima; confirmam repetição textual, sem estabelecer a semântica.

## 7. Regra conceitual proposta, não implementada

Após confirmação documental, separar label original, candidatos, ID TQS resolvido e evidência contextual. A resolução deve exigir contexto confirmado de compartilhamento/associação, sequência dos apoios e candidato único consistente com o bloco individual da viga. Nunca usar a posição do nome no texto para escolher o ID.

Separar também a origem textual em tipo `left_support_inner_face` e referência documental `P2A/P2B`, conservando a string original. O reconhecimento semântico do tipo de origem não resolve por si só a identidade do apoio.

Não se registrou uma nova regra permanente baseada nesta hipótese. Nenhuma representação artificial de candidatos/resolução foi gravada nos modelos existentes.

## 8. Armaduras confirmadas e etapa bloqueada

O beam_model preserva N3=2Ø10, lower, layers=[2], intervalo −42..608 cm; N5=2Ø10, lower, layers=[2], −42..753 cm. Fontes documentais /longitudinal_reinforcement/positive/0 e /1. Esses vetores indicam duas barras na primeira camada, não camada número 2.

As positions TQS da V1001 já existem: 0,384; 1,0133333333333332; 1,6426666666666665; 2,272; 2,901333333333333; 3,5306666666666664; 4,16; 4,789333333333333; 5,418666666666667; 6,047999999999999; 6,677333333333333; 7,3066666666666675; 7,936 m. Sua geração não foi alterada.

Não foram transformados os intervalos N3/N5 nem associados esses pontos à armadura neste trabalho. Isso exigiria a correspondência espacial que ainda não foi formalizada. O mapper continua rejeitando a origem na linha 58–59 e exigindo associação documental única dos apoios na linha 79. Não foi gerado V1001_beam_mapping.json, nem executada a flexão positiva da V1001 ou criada saída com capacidade fictícia.

## 9. Lacunas e perguntas objetivas ao engenheiro

- Nesta prancha, a barra em P2A/P2B indica pilares alternativos de duas regiões equivalentes, pilares simultâneos ou outra convenção? Uma legenda/planta de formas ou confirmação explícita da convenção resolve essa lacuna.
- O detalhamento identificado apenas como V1001 também vale para V9001? Se sim, qual documento ou regra do projeto autoriza esse compartilhamento?
- Podemos registrar expressamente as relações V1001 → P2A/P1A e V9001 → P2B/P1B para esse contexto documental, preservando os labels originais?
- A prancha de 03/07/2026 corresponde ao modelo TQS dos relatórios de 03/10/2026? A concordância métrica não comprova equivalência de revisão.

## 10. Testes e regressões

Executados quatro comandos `python -B -m unittest discover -s <diretório> -p 'test_*.py'`: extrator_lst 39, beam_model 29, beam_mapping 22, reinforcement_checks 51. **141 testes aprovados.** A suíte de reinforcement_checks executa a integração real com o Concretopy e a regressão V501: Msk=61,5073088 kN.m; Mk_equivalente=99,47034565405093 kN.m; utilização=0,618348196093708.

Testes novos A–H da resolução agrupada não foram criados porque nenhuma regra foi implementada. Goldens anteriores, código e Concretopy permaneceram inalterados. Ancoragem e desenvolvimento não foram verificados.

Arquivo criado nesta tarefa: `.codex/analises/grouped_support_mapping.md`. Resultado conclusivo da investigação: a hipótese V1001/V9001 é sustentada geometricamente, mas ainda falta evidência da semântica documental dos apoios para convertê-la em regra determinística de mapping.
