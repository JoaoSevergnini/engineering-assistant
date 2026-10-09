# V536 — exploração de alternativas positivas no apoio esquerdo

06/10/2026. Implementada uma rotina de orquestração no engineering-assistant; **Concretopy não foi alterado**. A configuração existente é avaliada primeiro. Cada candidata é reconstruída e submetida às APIs reais de posicionamento/flexão, demanda de apoio para cada par e ancoragem. Não se reutilizam d/x/z/demanda/lb da configuração original.

## Arquitetura e decisões

[Orquestrador](../../tools/reinforcement_checks/support_alternatives.py), [contrato](../../tools/reinforcement_checks/support_alternatives.md), [procedimento da Skill](../../.agents/skills/reinforcement-review/references/positive-end-support.md). Representação explícita por camadas `{count,diameter_mm,d_cm}`; mesma bitola por configuração, sem bitola equivalente. Posições explícitas ou convenção pública Concretopy VIGAS!K5:K7 autorizada pelo chamador. Aderência por centro físico de cada camada; condições mistas bloqueiam a ancoragem agregada. Biblioteca mantém integralmente a física.

Pares de engenharia: P1 positivo/|Vk mínimo|, P2 zero/máximo módulo. S1 no eixo esquerdo, esforços positivos/negativos/peak e fontes do [golden corrigido](V536_V565_left_support_anchorage_check.md). lb_ef=L_apoio−cobrimento=21,5 cm, distinto dos 21 cm documentais. Materiais C40/CA50, seção 19×72, d vão=66 cm, Nd=0 como hipótese, gancho válido=True/α=0,7 como cenário do engenheiro. Esforços e geometria do vão permanecem independentes da configuração local proposta. Não se certifica a solução longitudinal ao longo do vão.

Espaço explícito: bitolas **10; 12,5; 16; 20; 25 mm**, **2 a 6 barras**, **até 2 camadas**. Quantidades/camadas são limites de busca, não normativos. Geradas todas as partições ordenadas positivas dessas quantidades, incluindo configurações de controle iguais à existente. Nenhuma é selecionada como solução final.

## Resultado e critérios de comparação

Foram testadas **100 configurações**, com **32 válidas sem área adicional**. Estados principais: `{'AREA_INSUFICIENTE': 31, 'ANCORAGEM_INSUFICIENTE': 17, 'ABAIXO_LB_MIN': 13, 'VALIDA_SEM_AREA_ADICIONAL': 32, 'NAO_AVALIAVEL_GEOMETRIA': 7}`. Diagnósticos cumulativos podem mostrar várias causas simultâneas. Configurações bloqueadas têm passes=null; falhas completas, false.

Ordenação transparente de apresentação: barras, camadas, área fornecida, excesso, margem (maior primeiro), bitola; sem score. O critério não substitui julgamento de engenharia. Menos barras pode significar maior excesso de área: 4Ø20, 5Ø16 e 6Ø12,5 ilustram esse trade-off. **Todas conservam geometria_transversal_nao_verificada e gancho_geometria_nao_verificada.**

## Todas as configurações testadas

Camadas indicadas da face inferior para cima, por exemplo 4+2Ø12,5. As/áreas em cm²; comprimentos em cm. A tabela conserva também rejeições; JSON contém todas as respostas e intermediários.

| Configuração | As efetiva | As apoio | lb mínimo | lb necessário | Margem | As adicional | Estado / motivos |
|---|---:|---:|---:|---:|---:|---:|---|
| 2Ø10 (1 camada(s)) | 1.570796 | 5.917168 | 10.000000 | 72.609001 | -51.109001 | 4.346372 | AREA_INSUFICIENTE; AREA_INSUFICIENTE; ANCORAGEM_INSUFICIENTE; AREA_ADICIONAL_NECESSARIA |
| 2Ø12.5 (1 camada(s)) | 2.454369 | 5.917168 | 12.500000 | 58.087201 | -36.587201 | 4.176674 | AREA_INSUFICIENTE; AREA_INSUFICIENTE; ANCORAGEM_INSUFICIENTE; AREA_ADICIONAL_NECESSARIA |
| 2Ø16 (1 camada(s)) | 4.021239 | 5.917168 | 16.000000 | 45.380626 | -23.880626 | 4.466497 | AREA_INSUFICIENTE; AREA_INSUFICIENTE; ANCORAGEM_INSUFICIENTE; AREA_ADICIONAL_NECESSARIA |
| 2Ø20 (1 camada(s)) | 6.283185 | 5.917168 | 20.000000 | 36.304501 | -14.804501 | 4.326485 | ANCORAGEM_INSUFICIENTE; ANCORAGEM_INSUFICIENTE; AREA_ADICIONAL_NECESSARIA |
| 2Ø25 (1 camada(s)) | 9.817477 | 5.917168 | 25.000000 | 29.043600 | -7.543600 | 3.444610 | ABAIXO_LB_MIN; ABAIXO_LB_MIN; ANCORAGEM_INSUFICIENTE; AREA_ADICIONAL_NECESSARIA |
| 1+1Ø10 (2 camada(s)) | 1.570796 | 5.917168 | 10.000000 | 72.609001 | -51.109001 | 4.346372 | AREA_INSUFICIENTE; AREA_INSUFICIENTE; ANCORAGEM_INSUFICIENTE; AREA_ADICIONAL_NECESSARIA |
| 1+1Ø12.5 (2 camada(s)) | 2.454369 | 5.917168 | 12.500000 | 58.087201 | -36.587201 | 4.176674 | AREA_INSUFICIENTE; AREA_INSUFICIENTE; ANCORAGEM_INSUFICIENTE; AREA_ADICIONAL_NECESSARIA |
| 1+1Ø16 (2 camada(s)) | 4.021239 | 5.917168 | 16.000000 | 45.380626 | -23.880626 | 4.466497 | AREA_INSUFICIENTE; AREA_INSUFICIENTE; ANCORAGEM_INSUFICIENTE; AREA_ADICIONAL_NECESSARIA |
| 1+1Ø20 (2 camada(s)) | 6.283185 | 5.917168 | 20.000000 | 36.304501 | -14.804501 | 4.326485 | ANCORAGEM_INSUFICIENTE; ANCORAGEM_INSUFICIENTE; AREA_ADICIONAL_NECESSARIA |
| 1+1Ø25 (2 camada(s)) | 9.817477 | 5.917168 | 25.000000 | 29.043600 | -7.543600 | 3.444610 | ABAIXO_LB_MIN; ABAIXO_LB_MIN; ANCORAGEM_INSUFICIENTE; AREA_ADICIONAL_NECESSARIA |
| 3Ø10 (1 camada(s)) | 2.356194 | 5.917168 | 10.000000 | 48.406001 | -26.906001 | 3.560973 | AREA_INSUFICIENTE; AREA_INSUFICIENTE; ANCORAGEM_INSUFICIENTE; AREA_ADICIONAL_NECESSARIA |
| 3Ø12.5 (1 camada(s)) | 3.681554 | 5.917168 | 12.500000 | 38.724801 | -17.224801 | 2.949490 | AREA_INSUFICIENTE; AREA_INSUFICIENTE; ANCORAGEM_INSUFICIENTE; AREA_ADICIONAL_NECESSARIA |
| 3Ø16 (1 camada(s)) | 6.031858 | 5.917168 | 16.000000 | 30.253750 | -8.753750 | 2.455878 | ANCORAGEM_INSUFICIENTE; ANCORAGEM_INSUFICIENTE; AREA_ADICIONAL_NECESSARIA |
| 3Ø20 (1 camada(s)) | 9.424778 | 5.917168 | 20.000000 | 24.203000 | -2.703000 | 1.184892 | ANCORAGEM_INSUFICIENTE; ANCORAGEM_INSUFICIENTE; AREA_ADICIONAL_NECESSARIA |
| 3Ø25 (1 camada(s)) | 14.726216 | 5.917168 | 25.000000 | 25.000000 | -3.500000 | 0.000000 | ABAIXO_LB_MIN; ABAIXO_LB_MIN; ANCORAGEM_INSUFICIENTE |
| 1+2Ø10 (2 camada(s)) | 2.356194 | 5.917168 | 10.000000 | 48.406001 | -26.906001 | 3.560973 | AREA_INSUFICIENTE; AREA_INSUFICIENTE; ANCORAGEM_INSUFICIENTE; AREA_ADICIONAL_NECESSARIA |
| 1+2Ø12.5 (2 camada(s)) | 3.681554 | 5.917168 | 12.500000 | 38.724801 | -17.224801 | 2.949490 | AREA_INSUFICIENTE; AREA_INSUFICIENTE; ANCORAGEM_INSUFICIENTE; AREA_ADICIONAL_NECESSARIA |
| 1+2Ø16 (2 camada(s)) | 6.031858 | 5.917168 | 16.000000 | 30.253750 | -8.753750 | 2.455878 | ANCORAGEM_INSUFICIENTE; ANCORAGEM_INSUFICIENTE; AREA_ADICIONAL_NECESSARIA |
| 1+2Ø20 (2 camada(s)) | 9.424778 | 5.917168 | 20.000000 | 24.203000 | -2.703000 | 1.184892 | ANCORAGEM_INSUFICIENTE; ANCORAGEM_INSUFICIENTE; AREA_ADICIONAL_NECESSARIA |
| 1+2Ø25 (2 camada(s)) | 14.726216 | 5.917168 | 25.000000 | 25.000000 | -3.500000 | 0.000000 | ABAIXO_LB_MIN; ABAIXO_LB_MIN; ANCORAGEM_INSUFICIENTE |
| 2+1Ø10 (2 camada(s)) | 2.356194 | 5.917168 | 10.000000 | 48.406001 | -26.906001 | 3.560973 | AREA_INSUFICIENTE; AREA_INSUFICIENTE; ANCORAGEM_INSUFICIENTE; AREA_ADICIONAL_NECESSARIA |
| 2+1Ø12.5 (2 camada(s)) | 3.681554 | 5.917168 | 12.500000 | 38.724801 | -17.224801 | 2.949490 | AREA_INSUFICIENTE; AREA_INSUFICIENTE; ANCORAGEM_INSUFICIENTE; AREA_ADICIONAL_NECESSARIA |
| 2+1Ø16 (2 camada(s)) | 6.031858 | 5.917168 | 16.000000 | 30.253750 | -8.753750 | 2.455878 | ANCORAGEM_INSUFICIENTE; ANCORAGEM_INSUFICIENTE; AREA_ADICIONAL_NECESSARIA |
| 2+1Ø20 (2 camada(s)) | 9.424778 | 5.917168 | 20.000000 | 24.203000 | -2.703000 | 1.184892 | ANCORAGEM_INSUFICIENTE; ANCORAGEM_INSUFICIENTE; AREA_ADICIONAL_NECESSARIA |
| 2+1Ø25 (2 camada(s)) | 14.726216 | 5.917168 | 25.000000 | 25.000000 | -3.500000 | 0.000000 | ABAIXO_LB_MIN; ABAIXO_LB_MIN; ANCORAGEM_INSUFICIENTE |
| 4Ø10 (1 camada(s)) | 3.141593 | 5.917168 | 10.000000 | 36.304501 | -14.804501 | 2.775575 | AREA_INSUFICIENTE; AREA_INSUFICIENTE; ANCORAGEM_INSUFICIENTE; AREA_ADICIONAL_NECESSARIA |
| 4Ø12.5 (1 camada(s)) | 4.908739 | 5.917168 | 12.500000 | 29.043600 | -7.543600 | 1.722305 | AREA_INSUFICIENTE; AREA_INSUFICIENTE; ANCORAGEM_INSUFICIENTE; AREA_ADICIONAL_NECESSARIA |
| 4Ø16 (1 camada(s)) | 8.042477 | 5.917168 | 16.000000 | 22.690313 | -1.190313 | 0.445259 | ANCORAGEM_INSUFICIENTE; ANCORAGEM_INSUFICIENTE; AREA_ADICIONAL_NECESSARIA |
| 4Ø20 (1 camada(s)) | 12.566371 | 5.917168 | 20.000000 | 20.000000 | 1.500000 | 0.000000 | VALIDA_SEM_AREA_ADICIONAL |
| 4Ø25 (1 camada(s)) | 19.634954 | 5.917168 | 25.000000 | 25.000000 | -3.500000 | 0.000000 | ABAIXO_LB_MIN; ABAIXO_LB_MIN; ANCORAGEM_INSUFICIENTE |
| 1+3Ø10 (2 camada(s)) | 3.141593 | 5.917168 | 10.000000 | 36.304501 | -14.804501 | 2.775575 | AREA_INSUFICIENTE; AREA_INSUFICIENTE; ANCORAGEM_INSUFICIENTE; AREA_ADICIONAL_NECESSARIA |
| 1+3Ø12.5 (2 camada(s)) | 4.908739 | 5.917168 | 12.500000 | 29.043600 | -7.543600 | 1.722305 | AREA_INSUFICIENTE; AREA_INSUFICIENTE; ANCORAGEM_INSUFICIENTE; AREA_ADICIONAL_NECESSARIA |
| 1+3Ø16 (2 camada(s)) | 8.042477 | 5.917168 | 16.000000 | 22.690313 | -1.190313 | 0.445259 | ANCORAGEM_INSUFICIENTE; ANCORAGEM_INSUFICIENTE; AREA_ADICIONAL_NECESSARIA |
| 1+3Ø20 (2 camada(s)) | 12.566371 | 5.917168 | 20.000000 | 20.000000 | 1.500000 | 0.000000 | VALIDA_SEM_AREA_ADICIONAL |
| 1+3Ø25 (2 camada(s)) | 19.634954 | 5.917168 | 25.000000 | 25.000000 | -3.500000 | 0.000000 | ABAIXO_LB_MIN; ABAIXO_LB_MIN; ANCORAGEM_INSUFICIENTE |
| 2+2Ø10 (2 camada(s)) | 3.141593 | 5.917168 | 10.000000 | 36.304501 | -14.804501 | 2.775575 | AREA_INSUFICIENTE; AREA_INSUFICIENTE; ANCORAGEM_INSUFICIENTE; AREA_ADICIONAL_NECESSARIA |
| 2+2Ø12.5 (2 camada(s)) | 4.908739 | 5.917168 | 12.500000 | 29.043600 | -7.543600 | 1.722305 | AREA_INSUFICIENTE; AREA_INSUFICIENTE; ANCORAGEM_INSUFICIENTE; AREA_ADICIONAL_NECESSARIA |
| 2+2Ø16 (2 camada(s)) | 8.042477 | 5.917168 | 16.000000 | 22.690313 | -1.190313 | 0.445259 | ANCORAGEM_INSUFICIENTE; ANCORAGEM_INSUFICIENTE; AREA_ADICIONAL_NECESSARIA |
| 2+2Ø20 (2 camada(s)) | 12.566371 | 5.917168 | 20.000000 | 20.000000 | 1.500000 | 0.000000 | VALIDA_SEM_AREA_ADICIONAL |
| 2+2Ø25 (2 camada(s)) | 19.634954 | 5.917168 | 25.000000 | 25.000000 | -3.500000 | 0.000000 | ABAIXO_LB_MIN; ABAIXO_LB_MIN; ANCORAGEM_INSUFICIENTE |
| 3+1Ø10 (2 camada(s)) | 3.141593 | 5.917168 | 10.000000 | 36.304501 | -14.804501 | 2.775575 | AREA_INSUFICIENTE; AREA_INSUFICIENTE; ANCORAGEM_INSUFICIENTE; AREA_ADICIONAL_NECESSARIA |
| 3+1Ø12.5 (2 camada(s)) | 4.908739 | 5.917168 | 12.500000 | 29.043600 | -7.543600 | 1.722305 | AREA_INSUFICIENTE; AREA_INSUFICIENTE; ANCORAGEM_INSUFICIENTE; AREA_ADICIONAL_NECESSARIA |
| 3+1Ø16 (2 camada(s)) | 8.042477 | 5.917168 | 16.000000 | 22.690313 | -1.190313 | 0.445259 | ANCORAGEM_INSUFICIENTE; ANCORAGEM_INSUFICIENTE; AREA_ADICIONAL_NECESSARIA |
| 3+1Ø20 (2 camada(s)) | 12.566371 | 5.917168 | 20.000000 | 20.000000 | 1.500000 | 0.000000 | VALIDA_SEM_AREA_ADICIONAL |
| 3+1Ø25 (2 camada(s)) | 19.634954 | 5.917168 | 25.000000 | 25.000000 | -3.500000 | 0.000000 | ABAIXO_LB_MIN; ABAIXO_LB_MIN; ANCORAGEM_INSUFICIENTE |
| 5Ø10 (1 camada(s)) | 3.926991 | 5.917168 | 10.000000 | 29.043600 | -7.543600 | 1.990177 | AREA_INSUFICIENTE; AREA_INSUFICIENTE; ANCORAGEM_INSUFICIENTE; AREA_ADICIONAL_NECESSARIA |
| 5Ø12.5 (1 camada(s)) | 6.135923 | 5.917168 | 12.500000 | 23.234880 | -1.734880 | 0.495121 | ANCORAGEM_INSUFICIENTE; ANCORAGEM_INSUFICIENTE; AREA_ADICIONAL_NECESSARIA |
| 5Ø16 (1 camada(s)) | 10.053096 | 5.917168 | 16.000000 | 18.152250 | 3.347750 | 0.000000 | VALIDA_SEM_AREA_ADICIONAL |
| 5Ø20 (1 camada(s)) | 15.707963 | 5.917168 | 20.000000 | 20.000000 | 1.500000 | 0.000000 | VALIDA_SEM_AREA_ADICIONAL |
| 5Ø25 (1 camada(s)) | 24.543693 | 5.917168 | 25.000000 | 25.000000 | -3.500000 | 0.000000 | ABAIXO_LB_MIN; ABAIXO_LB_MIN; ANCORAGEM_INSUFICIENTE |
| 1+4Ø10 (2 camada(s)) | 3.926991 | 5.917168 | 10.000000 | 29.043600 | -7.543600 | 1.990177 | AREA_INSUFICIENTE; AREA_INSUFICIENTE; ANCORAGEM_INSUFICIENTE; AREA_ADICIONAL_NECESSARIA |
| 1+4Ø12.5 (2 camada(s)) | 6.135923 | 5.917168 | 12.500000 | 23.234880 | -1.734880 | 0.495121 | ANCORAGEM_INSUFICIENTE; ANCORAGEM_INSUFICIENTE; AREA_ADICIONAL_NECESSARIA |
| 1+4Ø16 (2 camada(s)) | 10.053096 | 5.917168 | 16.000000 | 18.152250 | 3.347750 | 0.000000 | VALIDA_SEM_AREA_ADICIONAL |
| 1+4Ø20 (2 camada(s)) | 15.707963 | 5.917168 | 20.000000 | 20.000000 | 1.500000 | 0.000000 | VALIDA_SEM_AREA_ADICIONAL |
| 1+4Ø25 (2 camada(s)) | - | - | - | - | - | - | NAO_AVALIAVEL_GEOMETRIA; configuration_not_evaluable: concretopy_flexure_hypotheses_or_ductility_invalid |
| 2+3Ø10 (2 camada(s)) | 3.926991 | 5.917168 | 10.000000 | 29.043600 | -7.543600 | 1.990177 | AREA_INSUFICIENTE; AREA_INSUFICIENTE; ANCORAGEM_INSUFICIENTE; AREA_ADICIONAL_NECESSARIA |
| 2+3Ø12.5 (2 camada(s)) | 6.135923 | 5.917168 | 12.500000 | 23.234880 | -1.734880 | 0.495121 | ANCORAGEM_INSUFICIENTE; ANCORAGEM_INSUFICIENTE; AREA_ADICIONAL_NECESSARIA |
| 2+3Ø16 (2 camada(s)) | 10.053096 | 5.917168 | 16.000000 | 18.152250 | 3.347750 | 0.000000 | VALIDA_SEM_AREA_ADICIONAL |
| 2+3Ø20 (2 camada(s)) | 15.707963 | 5.917168 | 20.000000 | 20.000000 | 1.500000 | 0.000000 | VALIDA_SEM_AREA_ADICIONAL |
| 2+3Ø25 (2 camada(s)) | 24.543693 | 5.917168 | 25.000000 | 25.000000 | -3.500000 | 0.000000 | ABAIXO_LB_MIN; ABAIXO_LB_MIN; ANCORAGEM_INSUFICIENTE |
| 3+2Ø10 (2 camada(s)) | 3.926991 | 5.917168 | 10.000000 | 29.043600 | -7.543600 | 1.990177 | AREA_INSUFICIENTE; AREA_INSUFICIENTE; ANCORAGEM_INSUFICIENTE; AREA_ADICIONAL_NECESSARIA |
| 3+2Ø12.5 (2 camada(s)) | 6.135923 | 5.917168 | 12.500000 | 23.234880 | -1.734880 | 0.495121 | ANCORAGEM_INSUFICIENTE; ANCORAGEM_INSUFICIENTE; AREA_ADICIONAL_NECESSARIA |
| 3+2Ø16 (2 camada(s)) | 10.053096 | 5.917168 | 16.000000 | 18.152250 | 3.347750 | 0.000000 | VALIDA_SEM_AREA_ADICIONAL |
| 3+2Ø20 (2 camada(s)) | 15.707963 | 5.917168 | 20.000000 | 20.000000 | 1.500000 | 0.000000 | VALIDA_SEM_AREA_ADICIONAL |
| 3+2Ø25 (2 camada(s)) | 24.543693 | 5.917168 | 25.000000 | 25.000000 | -3.500000 | 0.000000 | ABAIXO_LB_MIN; ABAIXO_LB_MIN; ANCORAGEM_INSUFICIENTE |
| 4+1Ø10 (2 camada(s)) | 3.926991 | 5.917168 | 10.000000 | 29.043600 | -7.543600 | 1.990177 | AREA_INSUFICIENTE; AREA_INSUFICIENTE; ANCORAGEM_INSUFICIENTE; AREA_ADICIONAL_NECESSARIA |
| 4+1Ø12.5 (2 camada(s)) | 6.135923 | 5.917168 | 12.500000 | 23.234880 | -1.734880 | 0.495121 | ANCORAGEM_INSUFICIENTE; ANCORAGEM_INSUFICIENTE; AREA_ADICIONAL_NECESSARIA |
| 4+1Ø16 (2 camada(s)) | 10.053096 | 5.917168 | 16.000000 | 18.152250 | 3.347750 | 0.000000 | VALIDA_SEM_AREA_ADICIONAL |
| 4+1Ø20 (2 camada(s)) | 15.707963 | 5.917168 | 20.000000 | 20.000000 | 1.500000 | 0.000000 | VALIDA_SEM_AREA_ADICIONAL |
| 4+1Ø25 (2 camada(s)) | 24.543693 | 5.917168 | 25.000000 | 25.000000 | -3.500000 | 0.000000 | ABAIXO_LB_MIN; ABAIXO_LB_MIN; ANCORAGEM_INSUFICIENTE |
| 6Ø10 (1 camada(s)) | 4.712389 | 5.917168 | 10.000000 | 24.203000 | -2.703000 | 1.204779 | AREA_INSUFICIENTE; AREA_INSUFICIENTE; ANCORAGEM_INSUFICIENTE; AREA_ADICIONAL_NECESSARIA |
| 6Ø12.5 (1 camada(s)) | 7.363108 | 5.917168 | 12.500000 | 19.362400 | 2.137600 | 0.000000 | VALIDA_SEM_AREA_ADICIONAL |
| 6Ø16 (1 camada(s)) | 12.063716 | 5.917168 | 16.000000 | 16.000000 | 5.500000 | 0.000000 | VALIDA_SEM_AREA_ADICIONAL |
| 6Ø20 (1 camada(s)) | 18.849556 | 5.917168 | 20.000000 | 20.000000 | 1.500000 | 0.000000 | VALIDA_SEM_AREA_ADICIONAL |
| 6Ø25 (1 camada(s)) | - | - | - | - | - | - | NAO_AVALIAVEL_GEOMETRIA; configuration_not_evaluable: Barras da camada não cabem na largura interna da seção. |
| 1+5Ø10 (2 camada(s)) | 4.712389 | 5.917168 | 10.000000 | 24.203000 | -2.703000 | 1.204779 | AREA_INSUFICIENTE; AREA_INSUFICIENTE; ANCORAGEM_INSUFICIENTE; AREA_ADICIONAL_NECESSARIA |
| 1+5Ø12.5 (2 camada(s)) | 7.363108 | 5.917168 | 12.500000 | 19.362400 | 2.137600 | 0.000000 | VALIDA_SEM_AREA_ADICIONAL |
| 1+5Ø16 (2 camada(s)) | 12.063716 | 5.917168 | 16.000000 | 16.000000 | 5.500000 | 0.000000 | VALIDA_SEM_AREA_ADICIONAL |
| 1+5Ø20 (2 camada(s)) | 18.849556 | 5.917168 | 20.000000 | 20.000000 | 1.500000 | 0.000000 | VALIDA_SEM_AREA_ADICIONAL |
| 1+5Ø25 (2 camada(s)) | - | - | - | - | - | - | NAO_AVALIAVEL_GEOMETRIA; configuration_not_evaluable: concretopy_flexure_hypotheses_or_ductility_invalid |
| 2+4Ø10 (2 camada(s)) | 4.712389 | 5.917168 | 10.000000 | 24.203000 | -2.703000 | 1.204779 | AREA_INSUFICIENTE; AREA_INSUFICIENTE; ANCORAGEM_INSUFICIENTE; AREA_ADICIONAL_NECESSARIA |
| 2+4Ø12.5 (2 camada(s)) | 7.363108 | 5.917168 | 12.500000 | 19.362400 | 2.137600 | 0.000000 | VALIDA_SEM_AREA_ADICIONAL |
| 2+4Ø16 (2 camada(s)) | 12.063716 | 5.917168 | 16.000000 | 16.000000 | 5.500000 | 0.000000 | VALIDA_SEM_AREA_ADICIONAL |
| 2+4Ø20 (2 camada(s)) | 18.849556 | 5.917168 | 20.000000 | 20.000000 | 1.500000 | 0.000000 | VALIDA_SEM_AREA_ADICIONAL |
| 2+4Ø25 (2 camada(s)) | - | - | - | - | - | - | NAO_AVALIAVEL_GEOMETRIA; configuration_not_evaluable: concretopy_flexure_hypotheses_or_ductility_invalid |
| 3+3Ø10 (2 camada(s)) | 4.712389 | 5.917168 | 10.000000 | 24.203000 | -2.703000 | 1.204779 | AREA_INSUFICIENTE; AREA_INSUFICIENTE; ANCORAGEM_INSUFICIENTE; AREA_ADICIONAL_NECESSARIA |
| 3+3Ø12.5 (2 camada(s)) | 7.363108 | 5.917168 | 12.500000 | 19.362400 | 2.137600 | 0.000000 | VALIDA_SEM_AREA_ADICIONAL |
| 3+3Ø16 (2 camada(s)) | 12.063716 | 5.917168 | 16.000000 | 16.000000 | 5.500000 | 0.000000 | VALIDA_SEM_AREA_ADICIONAL |
| 3+3Ø20 (2 camada(s)) | 18.849556 | 5.917168 | 20.000000 | 20.000000 | 1.500000 | 0.000000 | VALIDA_SEM_AREA_ADICIONAL |
| 3+3Ø25 (2 camada(s)) | - | - | - | - | - | - | NAO_AVALIAVEL_GEOMETRIA; configuration_not_evaluable: concretopy_flexure_hypotheses_or_ductility_invalid |
| 4+2Ø10 (2 camada(s)) | 4.712389 | 5.917168 | 10.000000 | 24.203000 | -2.703000 | 1.204779 | AREA_INSUFICIENTE; AREA_INSUFICIENTE; ANCORAGEM_INSUFICIENTE; AREA_ADICIONAL_NECESSARIA |
| 4+2Ø12.5 (2 camada(s)) | 7.363108 | 5.917168 | 12.500000 | 19.362400 | 2.137600 | 0.000000 | VALIDA_SEM_AREA_ADICIONAL |
| 4+2Ø16 (2 camada(s)) | 12.063716 | 5.917168 | 16.000000 | 16.000000 | 5.500000 | 0.000000 | VALIDA_SEM_AREA_ADICIONAL |
| 4+2Ø20 (2 camada(s)) | 18.849556 | 5.917168 | 20.000000 | 20.000000 | 1.500000 | 0.000000 | VALIDA_SEM_AREA_ADICIONAL |
| 4+2Ø25 (2 camada(s)) | - | - | - | - | - | - | NAO_AVALIAVEL_GEOMETRIA; configuration_not_evaluable: concretopy_flexure_hypotheses_or_ductility_invalid |
| 5+1Ø10 (2 camada(s)) | 4.712389 | 5.917168 | 10.000000 | 24.203000 | -2.703000 | 1.204779 | AREA_INSUFICIENTE; AREA_INSUFICIENTE; ANCORAGEM_INSUFICIENTE; AREA_ADICIONAL_NECESSARIA |
| 5+1Ø12.5 (2 camada(s)) | 7.363108 | 5.917168 | 12.500000 | 19.362400 | 2.137600 | 0.000000 | VALIDA_SEM_AREA_ADICIONAL |
| 5+1Ø16 (2 camada(s)) | 12.063716 | 5.917168 | 16.000000 | 16.000000 | 5.500000 | 0.000000 | VALIDA_SEM_AREA_ADICIONAL |
| 5+1Ø20 (2 camada(s)) | 18.849556 | 5.917168 | 20.000000 | 20.000000 | 1.500000 | 0.000000 | VALIDA_SEM_AREA_ADICIONAL |
| 5+1Ø25 (2 camada(s)) | - | - | - | - | - | - | NAO_AVALIAVEL_GEOMETRIA; configuration_not_evaluable: concretopy_flexure_hypotheses_or_ductility_invalid |

## Candidatas válidas — geometria e auditoria resistente

Todas têm As_adicional=0, gancho válido=True no cenário e boa aderência em suas camadas. lb_ef=21,5 cm. A tabela anterior contém As/demanda/lb/min/necessário/margem/adicional. Aqui estão os demais valores e governantes; detalhes das chamadas completas permanecem no JSON.

| Configuração | Centros d por camada | d centroide | x | z | Excesso de área | As_corr | A/B/C governante por par | Pares governantes globais |
|---|---|---:|---:|---:|---:|---:|---|---|
| 4Ø20 (1 camada(s)) | 68.000000 | 68.000000 | 14.800881 | 60.599560 | 6.649203 | 10.609670 | positive_moment_min_shear:C; zero_moment_max_abs_shear:C | positive_moment_min_shear, zero_moment_max_abs_shear |
| 1+3Ø20 (2 camada(s)) | 68.000000, 64.000000 | 65.000000 | 14.800881 | 57.599560 | 6.649203 | 10.609670 | positive_moment_min_shear:C; zero_moment_max_abs_shear:C | positive_moment_min_shear, zero_moment_max_abs_shear |
| 2+2Ø20 (2 camada(s)) | 68.000000, 64.000000 | 66.000000 | 14.800881 | 58.599560 | 6.649203 | 10.609670 | positive_moment_min_shear:C; zero_moment_max_abs_shear:C | positive_moment_min_shear, zero_moment_max_abs_shear |
| 3+1Ø20 (2 camada(s)) | 68.000000, 64.000000 | 67.000000 | 14.800881 | 59.599560 | 6.649203 | 10.609670 | positive_moment_min_shear:C; zero_moment_max_abs_shear:C | positive_moment_min_shear, zero_moment_max_abs_shear |
| 5Ø16 (1 camada(s)) | 68.200000 | 68.200000 | 11.840705 | 62.279648 | 4.135929 | 8.487736 | positive_moment_min_shear:C; zero_moment_max_abs_shear:C | positive_moment_min_shear, zero_moment_max_abs_shear |
| 5Ø20 (1 camada(s)) | 68.000000 | 68.000000 | 18.501101 | 58.749450 | 9.790795 | 10.609670 | positive_moment_min_shear:C; zero_moment_max_abs_shear:C | positive_moment_min_shear, zero_moment_max_abs_shear |
| 1+4Ø16 (2 camada(s)) | 68.200000, 64.600000 | 65.320000 | 11.840705 | 59.399648 | 4.135929 | 8.487736 | positive_moment_min_shear:C; zero_moment_max_abs_shear:C | positive_moment_min_shear, zero_moment_max_abs_shear |
| 2+3Ø16 (2 camada(s)) | 68.200000, 64.600000 | 66.040000 | 11.840705 | 60.119648 | 4.135929 | 8.487736 | positive_moment_min_shear:C; zero_moment_max_abs_shear:C | positive_moment_min_shear, zero_moment_max_abs_shear |
| 3+2Ø16 (2 camada(s)) | 68.200000, 64.600000 | 66.760000 | 11.840705 | 60.839648 | 4.135929 | 8.487736 | positive_moment_min_shear:C; zero_moment_max_abs_shear:C | positive_moment_min_shear, zero_moment_max_abs_shear |
| 4+1Ø16 (2 camada(s)) | 68.200000, 64.600000 | 67.480000 | 11.840705 | 61.559648 | 4.135929 | 8.487736 | positive_moment_min_shear:C; zero_moment_max_abs_shear:C | positive_moment_min_shear, zero_moment_max_abs_shear |
| 1+4Ø20 (2 camada(s)) | 68.000000, 64.000000 | 64.800000 | 18.501101 | 55.549450 | 9.790795 | 10.609670 | positive_moment_min_shear:C; zero_moment_max_abs_shear:C | positive_moment_min_shear, zero_moment_max_abs_shear |
| 2+3Ø20 (2 camada(s)) | 68.000000, 64.000000 | 65.600000 | 18.501101 | 56.349450 | 9.790795 | 10.609670 | positive_moment_min_shear:C; zero_moment_max_abs_shear:C | positive_moment_min_shear, zero_moment_max_abs_shear |
| 3+2Ø20 (2 camada(s)) | 68.000000, 64.000000 | 66.400000 | 18.501101 | 57.149450 | 9.790795 | 10.609670 | positive_moment_min_shear:C; zero_moment_max_abs_shear:C | positive_moment_min_shear, zero_moment_max_abs_shear |
| 4+1Ø20 (2 camada(s)) | 68.000000, 64.000000 | 67.200000 | 18.501101 | 57.949450 | 9.790795 | 10.609670 | positive_moment_min_shear:C; zero_moment_max_abs_shear:C | positive_moment_min_shear, zero_moment_max_abs_shear |
| 6Ø12.5 (1 camada(s)) | 68.375000 | 68.375000 | 8.672391 | 64.038804 | 1.445940 | 6.631044 | positive_moment_min_shear:C; zero_moment_max_abs_shear:C | positive_moment_min_shear, zero_moment_max_abs_shear |
| 6Ø16 (1 camada(s)) | 68.200000 | 68.200000 | 14.208845 | 61.095577 | 6.146548 | 8.487736 | positive_moment_min_shear:C; zero_moment_max_abs_shear:C | positive_moment_min_shear, zero_moment_max_abs_shear |
| 6Ø20 (1 camada(s)) | 68.000000 | 68.000000 | 22.201321 | 56.899339 | 12.932388 | 10.609670 | positive_moment_min_shear:C; zero_moment_max_abs_shear:C | positive_moment_min_shear, zero_moment_max_abs_shear |
| 2+4Ø12.5 (2 camada(s)) | 68.375000, 65.125000 | 66.208333 | 8.672391 | 61.872138 | 1.445940 | 6.631044 | positive_moment_min_shear:C; zero_moment_max_abs_shear:C | positive_moment_min_shear, zero_moment_max_abs_shear |
| 3+3Ø12.5 (2 camada(s)) | 68.375000, 65.125000 | 66.750000 | 8.672391 | 62.413804 | 1.445940 | 6.631044 | positive_moment_min_shear:C; zero_moment_max_abs_shear:C | positive_moment_min_shear, zero_moment_max_abs_shear |
| 4+2Ø12.5 (2 camada(s)) | 68.375000, 65.125000 | 67.291667 | 8.672391 | 62.955471 | 1.445940 | 6.631044 | positive_moment_min_shear:C; zero_moment_max_abs_shear:C | positive_moment_min_shear, zero_moment_max_abs_shear |
| 1+5Ø12.5 (2 camada(s)) | 68.375000, 65.125000 | 65.666667 | 8.672391 | 61.330471 | 1.445940 | 6.631044 | positive_moment_min_shear:C; zero_moment_max_abs_shear:C | positive_moment_min_shear, zero_moment_max_abs_shear |
| 5+1Ø12.5 (2 camada(s)) | 68.375000, 65.125000 | 67.833333 | 8.672391 | 63.497138 | 1.445940 | 6.631044 | positive_moment_min_shear:C; zero_moment_max_abs_shear:C | positive_moment_min_shear, zero_moment_max_abs_shear |
| 1+5Ø16 (2 camada(s)) | 68.200000, 64.600000 | 65.200000 | 14.208845 | 58.095577 | 6.146548 | 8.487736 | positive_moment_min_shear:C; zero_moment_max_abs_shear:C | positive_moment_min_shear, zero_moment_max_abs_shear |
| 5+1Ø16 (2 camada(s)) | 68.200000, 64.600000 | 67.600000 | 14.208845 | 60.495577 | 6.146548 | 8.487736 | positive_moment_min_shear:C; zero_moment_max_abs_shear:C | positive_moment_min_shear, zero_moment_max_abs_shear |
| 2+4Ø16 (2 camada(s)) | 68.200000, 64.600000 | 65.800000 | 14.208845 | 58.695577 | 6.146548 | 8.487736 | positive_moment_min_shear:C; zero_moment_max_abs_shear:C | positive_moment_min_shear, zero_moment_max_abs_shear |
| 3+3Ø16 (2 camada(s)) | 68.200000, 64.600000 | 66.400000 | 14.208845 | 59.295577 | 6.146548 | 8.487736 | positive_moment_min_shear:C; zero_moment_max_abs_shear:C | positive_moment_min_shear, zero_moment_max_abs_shear |
| 4+2Ø16 (2 camada(s)) | 68.200000, 64.600000 | 67.000000 | 14.208845 | 59.895577 | 6.146548 | 8.487736 | positive_moment_min_shear:C; zero_moment_max_abs_shear:C | positive_moment_min_shear, zero_moment_max_abs_shear |
| 1+5Ø20 (2 camada(s)) | 68.000000, 64.000000 | 64.666667 | 22.201321 | 53.566006 | 12.932388 | 10.609670 | positive_moment_min_shear:C; zero_moment_max_abs_shear:C | positive_moment_min_shear, zero_moment_max_abs_shear |
| 2+4Ø20 (2 camada(s)) | 68.000000, 64.000000 | 65.333333 | 22.201321 | 54.232673 | 12.932388 | 10.609670 | positive_moment_min_shear:C; zero_moment_max_abs_shear:C | positive_moment_min_shear, zero_moment_max_abs_shear |
| 3+3Ø20 (2 camada(s)) | 68.000000, 64.000000 | 66.000000 | 22.201321 | 54.899339 | 12.932388 | 10.609670 | positive_moment_min_shear:C; zero_moment_max_abs_shear:C | positive_moment_min_shear, zero_moment_max_abs_shear |
| 4+2Ø20 (2 camada(s)) | 68.000000, 64.000000 | 66.666667 | 22.201321 | 55.566006 | 12.932388 | 10.609670 | positive_moment_min_shear:C; zero_moment_max_abs_shear:C | positive_moment_min_shear, zero_moment_max_abs_shear |
| 5+1Ø20 (2 camada(s)) | 68.000000, 64.000000 | 67.333333 | 22.201321 | 56.232673 | 12.932388 | 10.609670 | positive_moment_min_shear:C; zero_moment_max_abs_shear:C | positive_moment_min_shear, zero_moment_max_abs_shear |

As alternativas Ø25 com área suficiente são frequentemente impedidas por lb mínimo, e algumas configurações são bloqueadas pelo modelo de flexão/ductilidade. Recusas do Concretopy são preservadas. A verificação elementar de largura da biblioteca não é certificação de espaçamento livre ou cabimento transversal completo.

## Testes e preservação

**262 testes do engineering-assistant passaram**: extrator_lst 39, beam_model 30, beam_mapping 34 e reinforcement_checks 159. São 232 existentes mais **30 novos**. Testes novos verificam geração configurável, uma/várias camadas, posição explícita/automática, d/x/z recalculados, chamadas independentes, maior demanda e empate, ausência de positivo artificial, lb e lb_min por bitola, aderência/fronteira/condições mistas, área/comprimento/mínimo, diagnósticos simultâneos, solução sem adicional, nenhuma solução, geometrias bloqueadas, limitações, V536 golden com todas as 100 alternativas e controle V565 em 21,5 cm. Testes de contrato não duplicam equações resistentes do Concretopy.

**405 testes do Concretopy passaram**, executados com Python 3.11/pytest em diretório temporário do workspace, `-B` e `-p no:cacheprovider`. Skill validada pelo `quick_validate.py`. Hashes antes/depois comprovam preservação do Concretopy e dos dados documentais/goldens de escalonamento. Resultados de apoio foram corrigidos deliberadamente conforme decisão do engenheiro, não preservados como se a entrada de 21 cm ainda valesse. `git diff --check` executado ao concluir.

## Arquivos e reprodução

Criados: `tools/reinforcement_checks/support_alternatives.py`, `support_alternatives.md`, `test_support_alternatives.py`; referência `positive-end-support.md`; este relatório; arquivo histórico de 21 cm; auditoria `V536_support_alternatives_validation.json`.

Alterados: `reinforcement-review/SKILL.md`, `references/beam-review.md`, `tools/reinforcement_checks/README.md`, `al_shear_selection.md`; script `validar_v536_v565_apoio_esquerdo.py`; resultados V536/V565 de apoio; relatório corrigido de apoio. Dados primários/documentais, resultados N3 de escalonamento e Concretopy não foram modificados.

```powershell
python -B analises/pranchas/validar_v536_v565_apoio_esquerdo.py
python -B -m unittest discover -s tools/reinforcement_checks -p 'test_support_alternatives.py'
```

[JSON com todas as alternativas](../../analises/pranchas/V536_left_support_anchorage_check.json), [controle V565](../../analises/pranchas/V565_left_support_anchorage_check.json), [testes e hashes](../../analises/pranchas/V536_support_alternatives_validation.json). Importar `load_case` nos testes não regrava goldens.

## Limitações e decisões ainda necessárias

Nenhuma candidata está pronta para detalhar somente por este cálculo. Para cada uma, revisar cabimento/espaçamento livre, interferências, raio/pino, cobrimento/confinamento e geometria completa do gancho da nova bitola. Não se aplicou tabela prática de dobra. Não foram dimensionados grampos ou seus comprimentos/espaçamentos, apoio direito, negativos, suspensão, cisalhamento completo, limites normativos de barras por camada ou aprovação global.

A demanda do vão usada em C permanece uma entrada independente auditada; a mudança local de armadura no apoio não é automaticamente alteração da armadura resistente em todo o vão. A escolha definitiva precisa conferir continuidade e compatibilidade com N2/N3. As_adicional do Concretopy não representa área de grampo. **selected_solution=null** em todas as saídas de exploração; o engenheiro pode comparar as alternativas e decidir após revisão física.

Contradições históricas foram identificadas e documentadas: a projeção documental de 21 cm deixou de ser o comprimento da verificação pela nova decisão; a definição espacial genérica de apoio em al_shear_selection continua pendente, com S1 explicitamente confirmada apenas neste ensaio. As fórmulas/itens normativos pertencem aos contratos Concretopy consultados; não houve nova interpretação da NBR.
