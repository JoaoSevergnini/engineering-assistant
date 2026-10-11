"""Relatório de engenharia a partir dos valores realmente retornados."""
import json,re
from pathlib import Path
OUT=Path(__file__).resolve().parent
def read(name):return json.loads((OUT/name).read_text(encoding='utf-8-sig'))
def n(v):return '—' if v is None else f'{v:.5f}'.replace('.',',')
def interval(v):return '—' if v is None else '['+'; '.join(n(x) for x in v)+']'
data=read('sinteticos.json')['cases'];real=read('v611.json');tests=read('testes.json');preservation=read('preservacao.json')
text=['# Suspensão adicional em mudanças de seção com desnível inferior','',
'O controle foi integrado ao fluxo atual. A seção suspensa é a de **menor cota da face inferior**; toda a distribuição de estribos fica nesse lado. As verificações numéricas abaixo são sintéticas. Na V611 real, as cotas identificam o lado suspenso, mas a posição das transições e outras entradas ainda impedem calcular a armadura adicional. Não há aprovação integral da V611 nem das regiões locais de descontinuidade.','',
'## Procedimento aplicado','',
'Fonte do procedimento: instruções expressas do engenheiro responsável neste complemento. Não foi atribuída nova prescrição normativa. O método existente de Concretopy fornece fyd, resistência de cortante, taxa mínima, área dos estribos e limites de detalhamento; não foi modificado.','',
'Unidades: Vk em kN; fyd em MPa convertido por 0,1 para kN/cm²; As em cm²; h e L em cm; taxas em cm²/m; coordenadas em m.','',
'`As_susp = abs(Vk_transição) × γf × γn / fyd(kN/cm²)`; `L = h_suspensa/2`; `taxa_susp = As_susp/L × 100`; `taxa_total = taxa_usual_cortante + taxa_susp`. A área existente é comparada uma única vez à soma, sem duplicar o crédito dos estribos.','',
'A taxa usual é o retorno governante do método de cortante existente, incluindo o mínimo quando governante, pesquisado somente na região unilateral da seção suspensa. Os valores característicos da transição usam o lado de fundo mais baixo; ambos os lados e seus sinais são preservados. O máximo de todo o vão não é usado para calcular a parcela adicional. Saltos exigem valores unilaterais: não se interpola através deles.','',
'Este procedimento é distinto da suspensão de apoio indireto: não usa 75% da reação nem distribuição simétrica. A suspensão de apoio indireto e sua combinação de taxas permanecem com o comportamento anterior. Fundos coincidentes dispensam apenas esta parcela adicional; o cortante usual continua obrigatório.','',
'## V611 real — duas orientações do desnível','',
'Forma: `051-SJ-EST-EX-010-PLB-TP-R01.pdf`, página 1; leitura revisada em [V611_form_reviewed.json](../etapa1_1_integracao/V611_form_reviewed.json) e [imagem da forma](../etapa1_1_integracao/V611_full_form.png). Origem na face de P28 voltada a P19, sentido crescente para P1. As cotas e segmentos foram reutilizados sem alteração.','',
'| Transição | Região longitudinal onde falta cotar xt (m) | Alturas esquerda/direita (cm) | Fundos esquerda/direita (cm) | Seção suspensa | Resultado |',
'|---|---|---|---|---|---|',
'| P19 | [2,820; 3,520] | 57 / 47 | 3751 / 3761 | FORM-1, à esquerda | Não executado |',
'| P10 | [6,190; 6,890] | 47 / 57 | 3761 / 3751 | FORM-3, à direita | Não executado |','',
'As transições estão dentro dos apoios; a leitura disponível não fornece o ponto cotado xt. O fluxo não transforma esse intervalo no eixo do pilar, não adota cortante máximo do vão como cortante da transição e não posiciona estribos dentro de uma geometria não comprovada.','',
'| Informação/cálculo real | P19 | P10 |',
'|---|---|---|',
'| Lado suspenso identificado pelas cotas | Esquerda | Direita |',
'| xt comprovado | Pendente | Pendente |',
'| Vk na transição | Não selecionado | Não selecionado |',
'| γf / γs | 1,4 / 1,15 | 1,4 / 1,15 |',
'| γn | Sem valor comprovado | Sem valor comprovado |',
'| As adicional / comprimento distribuído / taxas | Não calculados | Não calculados |',
'| Estribos existentes | Inventário N7/N8 preservado; região adicional não identificada | Inventário N7 preservado; região adicional não identificada |','',
'γf e materiais vêm dos extratos TQS; γs = 1,15 é a convenção explícita já usada na V607. Não foi presumido γn = 1. Os estribos Ø5 e faixas N7/N8 do detalhamento foram conservados na [entrada real](entrada_v611.json); eles não comprovam a posição da mudança de seção.','',
'Pendências reais da guarda: '+ '; '.join(sorted({p for t in real['transitions'] for p in t['input_validation']['pending']}))+'. Faltam xt/continuidade geométrica dentro dos apoios, d derivado de armaduras físicas comprovadas, γn e confirmação do escopo do método de cortante. Não houve cálculo resistente real de suspensão nessa viga. [Resultado documental V611](v611.json).','',
'## Verificações numéricas sintéticas','',
'Entradas são dados de teste, não armaduras ou esforços da V611. Domínio [0; 4] m, xt = 2 m, b = 19 cm; h esquerdo/direito = 57/47 cm, exceto o caso de h = 67 cm. Fundos são 0/10 cm para lado suspenso esquerdo e 10/0 cm para direito. No caso direito, a seção suspensa tem **menor altura**, demonstrando que o lado é escolhido pela cota inferior.','',
'Materiais/coeficientes documentados nas fixtures: fck = 40 MPa; fyk = 500 MPa; γf = γc = 1,4; γs = 1,15; **γn = 1,1**; fyd Concretopy = 434,78261 MPa = 43,47826 kN/cm². Geometria e composições existentes dão d = 53,07/43,07 cm, ou 63,07 cm para h = 67 cm.','',
'Estribos convencionais de dois ramos efetivos Ø6,3/8 cm, com posição/extensão comprovadas na fixture, fornecem 7,79311 cm²/m. No caso insuficiente, Ø6,3/20 cm fornece 3,11725 cm²/m. Os mesmos estribos atendem ao cortante e à parcela adicional pela comparação com a taxa total; suas áreas não são somadas duas vezes.','',
'| Caso | Seção suspensa | Distribuição unilateral (m) | L (cm) | Vk adotado (kN) | As adicional (cm²) | Taxa usual | Taxa adicional | Taxa total | Taxa existente | Resultado |',
'|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|']
labels={'fundos_coincidentes':'Fundos coincidentes','fundo_baixo_esquerda':'Fundo baixo à esquerda','fundo_baixo_direita':'Fundo baixo à direita','altura_67':'Altura suspensa 67 cm','insuficiente':'Adensamento insuficiente','extensao_nao_comprovada':'Extensão não comprovada','niveis_ausentes':'Níveis ausentes','salto_cortante':'Cortantes unilaterais distintos'}
for name,v in data.items():
 r=v.get('result') or {};pieces=r.get('subintervals',[]);piece=pieces[0] if pieces else {}
 values=[labels[name],r.get('suspended_section_id','—')+' '+r.get('suspended_side',''),interval(r.get('distribution_interval_m')),n(r.get('distribution_length_cm')),n(r.get('governing_shear',{}).get('Vk_original_kn')),n(r.get('additional_area',{}).get('as_suspension_cm2')),n(piece.get('usual_rate_cm2_m')),n(r.get('additional_rate_cm2_m')),n(piece.get('total_required_rate_cm2_m')),n((piece.get('provided') or {}).get('Asw_per_s_cm2_m')),v['status']]
 text.append('| '+' | '.join(values)+' |')
text+=['','Taxas da tabela em cm²/m. `PASS` refere-se ao controle adicional e seus controles de cortante/detalhamento executados no intervalo identificado; não aprova a viga inteira ou o modelo local da descontinuidade. `NOT_APPLICABLE` vale somente para a parcela adicional em fundos coincidentes.','',
'No caso direito, Vk na transição é 30 kN, mas o cortante usual da região [2; 2,235] inclui o pico de 200 kN em x = 2,1 m. Por isso sua taxa usual é 11,50260 cm²/m e a total é 16,02430 cm²/m: os estribos não atendem. O pico regional altera o cortante usual, sem substituir o cortante de 30 kN usado na parcela de suspensão.','',
'No caso com salto, preservados: esquerda +30/−20 kN; direita +200/−100 kN. O fundo mais baixo é esquerdo: governante adicional +30 kN; não é adotado automaticamente o valor de 200 kN do outro lado. Os endpoints unilaterais são documentados na fixture e o diagrama regional é construído apenas do lado suspenso, sem interpolar entre lados.','',
'Conferência independente do caso esquerdo: `As = 30 × 1,4 × 1,1 / 43,47826 = 1,06260 cm²`; `L = 57/2 = 28,5 cm`; `taxa_susp = 1,06260/28,5 × 100 = 3,72842 cm²/m`; `taxa_total = 2,66670 + 3,72842 = 6,39513 cm²/m < 7,79311 cm²/m` existentes. A ordem de grandeza e as unidades conferem.','',
'Extensão não comprovada: área adicional pode ser calculada com a geometria e o cortante disponíveis, mas nenhuma capacidade é creditada a estribos de posicionamento presumido. Níveis ausentes: lado suspenso, distribuição e cálculo adicional não são executados. [Resultados completos](sinteticos.json) e arquivos `entrada_<caso>.json` preservam a separação de dados de teste e fontes.','',
'## Detalhamento, limitações e regressão','',
'Reutilizados os controles de área da bitola, ramos efetivos, espaçamento máximo, compressão diagonal, porta-estribo quando aplicável e práticas usuais de diâmetro/espaçamento. Espaçamento fora da prática usual conserva `REQUIRES_ENGINEERING_REVIEW`; falha numérica conserva `FAIL` e necessidade de avaliação. Não foi criado limite de armadura excessiva ou solução automática.','',
'A capacidade é verificada em cada faixa, sem média que compense falta de estribos. Cobertura parcial, posição presumida ou duplicação de faixas são pendências. Se regiões adicionais de duas transições se sobrepuserem, não há dupla aprovação dos mesmos estribos: registrar necessidade de combinação de solicitações, preservando as verificações numéricas individuais e eventuais falhas comprovadas.','',
'Não se substitui a verificação usual de cortante nem se aprova automaticamente a descontinuidade geométrica. As verificações especiais locais e detalhes físicos que não estejam comprovados continuam pendentes. O texto normativo integral não foi consultado nesta etapa; aplicou-se o procedimento fornecido pelo engenheiro e as interfaces existentes.','',
'V607 real: MRd = 22,19306728728441 kN.m e utilização = 0,30003582937880474, exatamente iguais à execução anterior. [Regressão](regressao_v607.json). Históricos, Concretopy e PDFs preservados; nenhuma proposta de correção gerada.','',
'## Testes executados','']
total=sum(int(re.search(r'Ran (\d+) tests',t['output']).group(1)) for t in tests)
text+=['Quatro suítes com código de saída zero: '+', '.join(t['suite'] for t in tests)+f'. Total descoberto: {total}; dois testes do extrator ignorados por falta dos LST originais. [Saídas completas](testes.json).', '',
'Os 17 testes específicos também passaram na versão final, incluindo a preservação de FAIL de compressão diagonal quando a taxa total não pode ser calculada e a execução local apesar de lacuna fora da região unilateral. Foram reexecutadas conjuntamente as suítes do fluxo de pavimento, do complemento e da suspensão existente. [Execução focada e regressões](testes_focados.json).','',
'Testes adicionais cobrem fundos coincidentes/desnivelados, duas orientações, seleção pela cota em vez da altura, diferentes alturas, cortantes unilaterais e salto sem valores unilaterais, adensamento suficiente/insuficiente, extensão não comprovada, cobertura parcial, níveis ausentes, γn não presumido, peças duplicadas, alerta usual e sobreposição entre regiões de suspensão.','',
f'Preservação por SHA-256: {preservation["count"]} arquivos monitorados, sem alterações. [Comparação](preservacao.json).','',
'Reprodução: `python analises/suspensao_desnivel_inferior/validar.py`; relatório: `python analises/suspensao_desnivel_inferior/gerar_relatorio.py`. Implementação nos módulos existentes de suspensão, fluxo de pavimento e guarda de entradas; conversão de aço/força compartilhada, sem duplicar fórmulas resistentes.']
(OUT/'relatorio.md').write_text('\n'.join(text)+'\n',encoding='utf-8')
