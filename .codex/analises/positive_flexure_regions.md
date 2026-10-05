# Flexão positiva por regiões geométricas

04/10/2026. Implementação genérica de orquestração para um vão físico já mapeado,
várias marcas e configurações transversais. Não implementa ancoragem,
desenvolvimento, efetividade parcial, deslocamento de diagrama ou outras resistências.

## 1. Arquitetura e arquivos

Mantida a separação: beam_model documental; beam_mapping espacial;
reinforcement_checks orquestra; Concretopy calcula seção/resistência.

- `flexure_regions.py`: decomposição geométrica e composição por camada.
- `positive_flexure.py`: associação de pontos, chamadas Concretopy e resumo.
- `tqs_moments.py`: seleção auditada M MX., compartilhada com o golden V501.
- `materials.py`: regra CA-50 e leitura dos campos documentais já utilizados.
- Script específico V501 permanece fixture de integração/regressão; agora
  consome o seletor compartilhado, sem ser a função genérica por viga.

Nova saída real: `analises/pranchas/V501_positive_flexure_regions.json`.
Entradas: V501_V503_beam_model.json, V501_tqs.json, V501_tqs_positions.json,
V501_beam_mapping.json e V501_tqs_raw.json. Modelos/fontes não são modificados.
O JSON antigo V501_positive_flexure_check.json foi reexecutado para atualizar
o hash do interpretador compartilhado, preservando seu resultado numérico.
Não foram modificados beam_model, beam_mapping, parsers, consolidadores ou Concretopy.

## 2. Região resistente e domínio

Uma região reúne composição geométrica constante de marcas/camadas e uma
configuração transversal única: bw, h, cobrimento e diâmetro do estribo.
Regiões não resolvidas também são preservadas com seus motivos; não recebem
operandos por default silencioso. Terminologia: geometric_reinforcement,
sem chamar presença de barra efetiva.

Domínio físico padrão: **eixo esquerdo até eixo direito** do único vão mapeado.
V501: 0,000–8,430 m. Isso inclui S1/S13 dentro dos apoios, sem truncá-las ao
vão livre ou inventar estribos onde o detalhamento não definiu intervalo.
Os limites de barras fora do domínio não alteram seus registros originais;
a partição considera somente a interseção com o domínio analisado.

## 3. Convenção de limites

beam_mapping representa barras com **intervalos fechados**. Uma partição
universal semiaberta perderia a composição documental no encontro fim/início
de duas marcas. Por isso:

1. interiores entre eventos são inicialmente abertos;
2. no ponto exato de cada evento, calcula-se a composição fechada documental;
3. se coincide com a configuração do trecho direito, o ponto pertence à direita;
4. senão, se coincide com a esquerda, pertence à esquerda;
5. se difere de ambos, cria-se uma região pontual fechada, x_start=x_end.

`include_start`, `include_end` e `kind` são explícitos. Cada seção TQS tem
exatamente uma região proprietária. Não há epsilon, snapping ou tolerância.
Comparações usam Decimal dos números publicados; conversão m→cm também é
decimal, sem tolerância de engenharia.

Exemplo fim N1=início N2: os interiores contêm N1 ou N2; o ponto exato contém
N1+N2 e é preservado separadamente. Isso é composição **geométrica**, sem
afirmar ancoragem das duas marcas. No encontro de estribos diferentes, o ponto
tem configuração transversal não resolvida, não se escolhe um lado arbitrariamente.

## 4. Algoritmo por eventos

Pontos de quebra vêm somente dos inícios/finais documentais, limites do domínio
e mudanças transversais. Ordenam-se valores únicos; para cada par consecutivo,
a composição é determinada no interior matemático. O ponto médio usado para
consultar os intervalos não é discretização de esforços: nenhum ponto TQS novo
é criado. Trata-se de identificar o conjunto constante entre dois eventos.
Os pontos exatos são tratados conforme a regra acima.

Intervalo desconhecido não equivale a barra ausente: a possível contribuição
indeterminada bloqueia a composição. Função longitudinal não classificada
permanece candidata não resolvida; não é inferida pelo diâmetro ou posição.
Marcas duplicadas e intervalos invertidos são rejeitados explicitamente.

## 5. Camadas e limitações do contrato

O índice 1-based do vetor layers do beam_model representa a camada documental
a partir da face indicada. Para positivas suportadas, a face deve ser lower.
Assim [2] significa duas barras na primeira camada; [0,2] significa duas na
segunda. [3,1] significa três na primeira e uma na segunda.

Somente com essa identidade documental de camada e face comum são agregadas
quantidades. Duas marcas [2] Ø12,5 na face lower produzem quatro barras na camada
1; [2] e [0,2] permanecem em duas camadas. Bitola igual sozinha não permite fusão.
Face/camadas ausentes ou contagens inconsistentes deixam a composição não resolvida.
Contribuições por marca e fonte continuam visíveis em cada camada.

Concretopy CamadaArmaduraLongitudinal admite **uma bitola por camada**.
2Ø12,5+2Ø16 na mesma camada é preservado, mas bloqueado como composição não
suportada; não se usa área/bitola equivalente nem duas camadas artificiais.
Bitolas diferentes em camadas físicas diferentes são aceitas.
Lacunas de camadas (ex.: somente camada 2 ocupada) também são bloqueadas:
omitir a camada 1 no posicionamento automático deslocaria a camada 2 sem evidência.

## 6. Estribo, seção e cobrimento

Escolhida a opção A: subdividir nos limites das regiões de estribos.
Por padrão os operandos transversais usam seção retangular do beam_model,
cobrimento documental se disponível ou inferior TQS com essa origem explícita,
e estribo da região mapeada. Não se usa o estribo do governante global em todo vão.
Conflitos de seção PDF/TQS são reportados/bloqueados; não há tolerância presumida.

A API de decomposição/orquestração também admite regiões transversais
explicitamente fornecidas com proveniência, permitindo eventos de bw/h/cobrimento
quando esses dados existirem. Os modelos atuais não contêm perfil documental
dessas variações: não se extrapolam cortes sem abscissa nem se inventam mudanças.
Intervalos transversais desconhecidos impedem resolução, sem extrapolação.

## 7. Seções TQS e Msk

Consomem-se positions existentes. Associa-se cada ponto usando os flags de limite,
preservando section, x, value e provenance. Negativos continuam visíveis com
eligible_positive=false; maior valor >0 governa. Não há módulo, interpolação,
extrapolação ou máximo entre pontos.

Se não houver ponto: demand_not_sampled, região mantida com demanda/capacidade null.
Com pontos mas sem positivos: no_positive_demand, sem converter negativos.
Valor ausente em um ponto bloqueia a comparação daquela região; não é ignorado
para escolher um máximo incompleto. Série não identificada bloqueia todas as
chamadas dependentes, preservando regiões.

Reutiliza-se a seleção auditada do golden: VGESFS, rótulo M MX., vão correspondente,
valores normalizados, quantity=bending_moment, envelope=max, stage=model_input,
unit=kN.m e correspondência única. Não se assume max como Msk universal.
O nível característico Msk é confirmado pelo engenheiro neste fluxo.

## 8. Concretopy e saída

Para região resolvida com positivo amostrado, usa-se API pública
verificar_flexao_viga_retangular. Camadas recebem quantidades/bitolas documentais,
**d omitido**; Concretopy calcula áreas, posições, centroide, x, x/d e capacidade.
Coeficientes e materiais seguem as regras já auditadas: fck explícito MPa,
CA50/CA-50/CA-50A→fyk500, gamma_f documental, gamma_c/gamma_s/Es defaults públicos
registrados. Mínimo não é solicitado. Nenhuma equação resistente foi duplicada.

Retorno completo da dataclass conservado em concretopy_result. Somente se
hipóteses/capacidade válidas: Mk_equivalente≥Msk e utilization=Msk/Mk_equivalente.
MRd permanece separado. Há somente conversão kN.cm→kN.m, não recalcular MRd/gamma_f.
Recusa geométrica/modelo inválido é preservada com motivo e comparação null.

Cada região possui composição, configuração, pontos, governante, chamada, retorno,
capacidade, comparação, diagnósticos e proveniência. Materiais, série e interface
Concretopy têm referências compartilhadas, sem duplicar arquivos-fontes completos.
São auditáveis os intervalos originais, translação, camada/marca, geometria,
cobrimento, estribo, série, valores/positions e implementação/hash usados.

## 9. Resumo do vão e regressão V501

Resultado regional V501:

| Região | Intervalo (m) | Marcas | Estribo | Seções | Status |
|---|---|---|---|---|---|
| R1 | [0;0,07) | nenhuma | desconhecido | nenhuma | demand_not_sampled |
| R2 | [0,07;0,60) | N5 | desconhecido | 1 | no_positive_demand |
| R3 | [0,60;5,97) | N5 | Ø5 | 2–9 | checked |
| R4 | {5,97} | N5 | ambíguo Ø5/Ø6,3 | nenhuma | demand_not_sampled |
| R5 | (5,97;6,69) | N5 | Ø6,3 | 10–11 | checked |
| R6 | {6,69} | N5 | ambíguo Ø6,3/Ø5 | nenhuma | demand_not_sampled |
| R7 | (6,69;7,71] | N5 | Ø5 | 12 | checked |
| R8 | (7,71;8,22] | N5 | desconhecido | 13 | no_positive_demand |
| R9 | (8,22;8,43] | nenhuma | desconhecido | nenhuma | demand_not_sampled |

| Região verificada | Governante (kN.m) | Mk_equivalente (kN.m) | Utilização |
|---|---:|---:|---:|
| R3, S8 | 61,5073088 | 99,47034565405093 | 0,618348196093708 |
| R5, S10 | 50,80825365 | 99,27216676965328 | 0,5118076425982845 |
| R7, S12 | 15,0826277 | 99,47034565405093 | 0,15162938864670328 |

Golden reproduzido **exatamente** pela função genérica: S8,
x=4,789333333333333 m, Msk=61,5073088, Mk=99,47034565405093,
utilização=0,618348196093708. Nenhum desses números está hardcoded na produção.

Resumo: 9 regiões totais; 3 verificadas; 6 com operandos/composição não resolvidos;
4 sem ponto; 2 com apenas negativos; 6 não verificadas. Contagens de lacunas
são dimensões independentes e podem se sobrepor. Todas as chamadas concluídas
têm capacidade suficiente, mas **incomplete=true**. Esse campo não aprova o vão.
Se nenhuma chamada for concluída, all_checked_regions_capacity_sufficient=null,
evitando aprovação vazia. Não existe beam_ok.

## 10. Testes sintéticos e suíte

**141 testes aprovados:** 51 reinforcement_checks, 22 beam_mapping, 29 beam_model,
39 extrator_lst. Goldens anteriores e testes de model/mapping/extrator não alterados.

Casos A–I pedidos cobertos: marca única, duas/três sobreposições, intervalos iguais,
encontro fim/início, região sem ponto, negativos apenas, mudança de estribo e
bitolas diferentes na mesma camada. Casos adicionais: limites exatamente em seção,
geometria ambígua no limite, alterações de h/cobrimento, zero comprimento,
camadas distintas, intervalos/valores/materiais ausentes, série desconhecida,
duplicatas, gaps, proveniência, imutabilidade e API real com d automático.

## 11. Caso real adicional

Inventariados todos os beam_model atuais. V1001 possui N3/N5 positivas
(2Ø10 cada, primeira camada) com intervalos −42…608 e −42…753 cm.
É candidato real, mas a tentativa de mapping existente falha:
Convenção do detalhamento não suportada. A origem inclui sufixo P2A/P2B;
apoios documentais agrupados e IDs TQS individuais também requerem correspondência
explícita. Não se removeu texto ou associou nomes para forçar integração.
Ver `V1001_positive_flexure_regions_exploratory.md` para evidências e impedimentos.

V502 tem N6/N7 positivas, mas intervalos null. V501/V503 têm apenas N5 positiva.
Não há mapping complexo já aprovado com dados suficientes nesta etapa.
A validação atual combina sintéticos e regressão V501; nenhum caso real foi inventado.

## 12. Limitações e próximos passos

- Um vão físico já mapeado, sem balanços; não resolve offsets globais/múltiplos vãos.
- Intervalos desconhecidos, camadas sem identidade, bitolas mistas na mesma camada,
  lacunas de camada, variações sem dados e limites ambíguos permanecem bloqueados.
- Diferença 711/712 cm continua mismatch, sem escala ou tolerância.
- Ancoragem/desenvolvimento, decalagem, al/lb/10φ, efetividade parcial, negativo,
  cisalhamento, suspensão, torção e correções automáticas não implementados.
- Próximo caso recomendado: resolver explicitamente a convenção de origem e
  associação documental da V1001 no mapping; executar suas regiões reais.
- Futuro contrato de camadas físicas/bitolas mistas deve ser discutido separadamente,
  sem modificar Concretopy nesta tarefa.

Criados: flexure_regions.py, positive_flexure.py, tqs_moments.py,
test_flexure_regions.py, test_positive_flexure_regions.py,
V501_positive_flexure_regions.json e os dois relatórios desta etapa.
Modificados: v501_positive_flexure.py, materials.py, README de reinforcement_checks
e V501_positive_flexure_check.json (hash da implementação compartilhada).
