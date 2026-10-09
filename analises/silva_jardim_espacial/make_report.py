from pathlib import Path
import sys,json,csv,html,collections,zipfile,datetime,re
ROOT=Path(r'\\srvmaster\PUBLICO\Joao Severgnini\Simon\engineering-assistant');P=ROOT/'analises/silva_jardim_espacial';S=Path(r'C:\TQS\TGD - SILVA JARDIM\24-212-TGD-SILVA JARDIM-R35\ESPACIAL')
sys.path.insert(0,str(ROOT/'tmp/pdf_deps'))
import fitz
I=json.loads((P/'inventario_com_hashes.json').read_text(encoding='utf-8'));D=json.loads((P/'modelo_e_combinacoes.json').read_text(encoding='utf-8'));V=json.loads((P/'validacao_extracao_rsx.json').read_text(encoding='utf-8'))
# Conteúdo atribuído a partir da leitura efetiva; formatos opacos permanecem explícitos.
CAT={
'FOR0212.POR':('Alta','Entrada do modelo principal: nós, materiais, seções, barras, restrições, cargas nodais e nas barras, 20 casos, 80 combinações e envoltória de 38 IDs. Unidades declaradas TF e M.','Não: FORCAS/CARREG são cargas aplicadas, não solicitações internas calculadas.','Texto lido e catalogado; cabeçalhos e componentes preservados.'),
'PORTELS.POR':('Alta','Entrada do modelo ELS: mesma contagem de nós/barras; 20 casos e 22 combinações (20 ELS e 2 FOGO).','Não; contém cargas e definições.','Texto lido e catalogado. IDs de combinação pertencem a este modelo.'),
'FOR0212.RSX':('Alta','Base binária de resultados: 100 registros, cada um com deslocamentos nodais, 12 valores por barra e 6 reações por apoio.','Sim: 3.757 barras, duas extremidades por caso/combinação.','Estrutura binária decodificada e conferida; piloto de vigas extraído.'),
'PORTELS.RSX':('Alta','Base binária ELS, com 42 registros e a mesma estrutura geométrica de contagem.','Sim: resultados por barra e caso/combinação.','Reações conferidas contra a listagem; piloto de vigas extraído.'),
'PORFOR.LST':('Alta','Relatório de geração do modelo principal: critérios efetivos, pisos/cotas, casos, combinações, transferência e relações viga–barra/pilar–barra.','Não há tabela completa de solicitações de vigas; fornece a associação nominal aos elementos.','1.550 associações viga–barra extraídas; cinco pisos TIPO identificados.'),
'PORFORELS.LST':('Alta','Relatório de geração ELS: critérios, pisos, associações e combinações; informa transferência para vigas/pilares desativada nesta execução.','Sem tabela completa de esforços das vigas.','Conteúdo conferido; mantém identidade do modelo ELS separada.'),
'FOR0212.Lst':('Alta','Listagem de processamento principal; reações FX/FY/FZ/MX/MY/MZ por nó de apoio, para NC e CBNL; somas de reações e forças externas.','Sim para apoios; não contém tabela de esforços nas barras nesta emissão.','7.600 linhas nó–caso lidas; base para validar RSX.'),
'PORTELS.Lst':('Alta','Listagem ELS com reações por apoio para NC e CB, e balanço de forças.','Sim para apoios; sem tabela de barras nesta emissão.','3.192 linhas nó–caso lidas; base para validar RSX.'),
'PORLIS2.LST':('Alta','Relatório nominal: pilares por piso/lance/barra/caso, My/Mz/N nas extremidades e DeslXY; forças de fundação; cargas nas vigas de transição. A seleção publicada é o caso 1.','Sim, pilares elemento por elemento; cargas pontuais de transição. Não há diagramas completos de vigas nem todas as combinações.','612 linhas de lances de pilares comparadas com RSX.'),
'CARRPOR.DAT':('Alta','Definições de carregamentos e combinações: tipos de ação, gamma favorável/desfavorável, psi0/psi1/psi2, flags de não linearidade, composição e seleção. Declara 26 casos e 100 combinações na configuração.','Não; definições e critérios.','Texto comentado. Configuração não se confunde com os casos efetivamente gerados em cada POR.'),
'CRITPOR.DAT':('Alta','Critérios de análise: propriedades, rigidezes, offsets, transferência, parâmetros de vento e demais opções.','Não.','Texto legível; valores efetivos devem ser cruzados com PORFOR/PORFORELS, evitando interpretar zeros de herança como propriedades nulas.'),
'PBETAD.DAT':('Média','84 pilares, 80 combinações; por pilar e lance registra índice/ID da combinação, BetaDPu/BetaDVu, PUtotal/PUpermanente e VUtotal/VUpermanente.','Sim, grandezas PU/VU por pilar/lance/combinação; não é o vetor completo de esforços de vigas.','Campos identificados por comentários; unidades e aplicação dos coeficientes ainda precisam de confirmação.'),
'CARDWG2.LST':('Alta','Geometria para planta de cargas: 20 plantas/pisos, 706 registros PILAR, dimensões e polígonos XY.','Não; geometria de pilares.','Tags identificadas: PLANTA/PISO/PILAR/NP/XY. Útil para obter dimensões reais dos nós de pórtico.'),
'PORLID2.DAT':('Média','Configuração da planta de cargas: 148 entradas selecionáveis e flags; primeiros 100 casos/combinações e 48 entradas de máximos/mínimos de componentes por grupos.','Não; nomes e seleção, sem valores numéricos de esforços por elemento.','Texto lido; 148 entradas não equivalem a 148 combinações resolvidas.'),
'PORLID3.DAT':('Média','Configuração análoga da planta de cargas.','Não.','Conteúdo comparável a PORLID2; conservar identidade/arquivo.'),
'PORLID2.XLSX':('Média / histórico','Planilha com resultados nominais de pilares, grupos A/B/C e colunas Fz/Fx/Fy/Mx/My associadas a extremos Fz.','Sim, valores por pilar; organização por extremos/grupos, sem identificação completa da combinação governante observada.','Data 07/08/2026; workbook registra caminho R27. Não usar como resultado atual R35 sem conferir origem.'),
'PORALF.LST':('Alta','Estabilidade global: hipóteses, gammaF/gammaF3, gammaZ/FAVt, ações horizontais e parâmetros de transferência.','Resultados globais; não fornece o vetor por barra.','Ajuda a interpretar amplificações e a distinguir saída bruta do pórtico de esforços transferidos ao dimensionamento.'),
'PORALF.HTM':('Alta','Estabilidade global e deslocamentos laterais, casos/combinações e tabelas por piso/direção; apresenta norma configurada para imperfeições como NBR-6118:2014.','Valores globais/por piso, sem solicitações individuais completas das vigas.','HTML lido; indicação de norma é configuração publicada, não validação normativa desta inspeção.'),
'PGLOERR.HTM':('Alta','Resumo do processamento global e categorias de erros/avisos. Publica erros graves e 1.569 avisos leves/787 médios.','Não; diagnóstico global.','Exige localização posterior no visualizador: categorias globais não comprovam ocorrência nas vigas TIPO.'),
'MENAVI.LST':('Média','Avisos de nós/distribuição de cargas das vigas 150 e 352; mensagem sobre gravação de momentos de vigas nos pilares.','Não; mensagens.','Útil para verificar hipóteses/modelagem; não transportar avisos automaticamente a V601–V629.'),
'PILAR.LST':('Média','Listagem da interface com processamento de pilares, identificações e mensagens.','Não foi encontrada tabela completa de esforços por combinação.','Texto inspecionado; usar PORLIS2/RSX para valores.'),
'CARPIL.LST':('Média','Mensagens do processamento PILAR.LDF e da planta de cargas em pilares.','Sem vetor completo de esforços calculados identificado.','Texto inspecionado; relatório de mensagens, não substitui base de resultados.'),
'CONTPOR.DAT':('Média','Condições especiais de contorno; declara zero definições de torção e demais contagens/configurações.','Não.','Texto legível; zero definições especiais não prova ausência de torção nas barras.'),
'PORGZTP.DAT':('Média','Parâmetros auxiliares relacionados à transferência/amplificação: quatro valores/flags.','Não.','Cruzar com relatório efetivo; sem atribuir significado de cada campo apenas pelo nome.'),
'PORGZTV.DAT':('Média','Parâmetros auxiliares análogos para transferência.','Não.','Mesma cautela de interpretação de campos.'),
'ESPECTRO.DAT':('Condicional','Tabela nomeada Default, com pares numéricos para definição de espectro.','Não; entrada de ação dinâmica.','Não demonstra que análise dinâmica correspondente foi efetivamente usada nesta execução.'),
'RESDES.HTM':('Média','Resumo estrutural: quantitativos por piso, aço, concreto, formas, fck, índices, custos e outros totais.','Não.','HTML lido; útil para materiais/quantitativos, não para solicitações.'),
'RESEST1.TXT':('Baixa','Relação de plantas/cabeçalho do resumo estrutural.','Não.','Texto legível.'),
'RESEST2.TXT':('Média','Quantitativos por piso e bitola/material.','Não.','Texto legível; não identifica as barras resistentes de uma viga.'),
'RESEST3.TXT':('Média','Resumo total de materiais.','Não.','Texto legível.'),
'RESEST4.TXT':('Média','Índices de consumo e espessura média.','Não.','Texto legível.'),
'RESEST5.TXT':('Baixa','Custos por piso/material.','Não.','Texto legível.'),
'RESEST7.TXT':('Baixa','Contagem de furos por tipo de elemento e piso.','Não.','Texto legível.'),
'RESEST8.TXT':('Baixa','Carbono incorporado por piso/insumo/material.','Não.','Texto legível.'),
'CARDWG.LST':('Baixa','Log do processamento de plantas do edifício.','Não.','Identifica plantas e diretórios.'),
'PORVIG.LST':('Baixa','Log de processamento de plantas para integração com vigas.','Não.','Identifica fontes; não apresenta solicitações por combinação.'),
}
for model in ['FOR0212','PORTELS']:
 for ext,desc in [('RPF','Geometria/metadados auxiliares do visualizador; cabeçalho TQS Modelador / Novo RPF.'),('POD','Arquivo binário auxiliar de identificação/organização do pórtico; conteúdo sem decodificação semântica completa.'),('BPq','Tabela textual de barras, NOi/NOf, tipo, campo Gama e comprimento; útil para barras muito curtas e diagnóstico geométrico.')]:
  CAT[model+'.'+ext]=('Média',desc,'Nenhum vetor de esforços por combinação confirmado neste arquivo.','Inspeção de cabeçalho/estrutura; não substitui RSX.')
CAT['FOR0212.POP']=('Condicional','Auxiliar binário do processamento principal.','Não confirmado.','Não decodificado semanticamente.')
CAT['FOR0212.EDI']=('Média','Auxiliar binário com referências às pastas/pavimentos do edifício.','Não confirmado.','Usar o mapa textual de PORFOR antes de depender deste formato.')
# Catálogo completo, incluindo formatos históricos/opacos e arquivos vazios.
ALL=[]
for i in I:
 n=i['file'];base=Path(n).name;ex=Path(n).suffix.upper()
 if n in CAT:r=CAT[n]
 elif i['bytes']==0:r=('Sem dados','Arquivo vazio.','Não.','Sem conteúdo nesta execução.')
 elif n.lower().startswith('tqsdesktopb\\'):r=('Baixa','Cache binário de miniatura (nomes terminados em .xml, sem XML textual).','Não confirmado; sem utilidade para extrair esforços.','Não interpretar extensão como conteúdo XML.')
 elif ex=='.E3D':r=('Histórico / geometria','Arquivo binário de visualização 3D; versões históricas R01–R34 e estudos com nomes próprios.','Esforços não confirmados por leitura deste formato.','Geometria/visualização exige leitor apropriado. Não assumir que o último E3D é a fonte operacional R35.')
 elif ex in ['.DWG','.BAK']:r=('Média / histórico','Desenho binário ou cópia de segurança; conteúdo dependente de leitor CAD/TQS.','Valores em desenhos não foram decodificados nesta inspeção.','Não usar backup como resultado atual sem comparação.')
 elif re.match(r'C\d{7}\.TMP$',n):r=('Média','Arquivo temporário binário com caminho de um pavimento/VIGAS e registros auxiliares.','Não confirmado.','Vínculo documental legível; registros numéricos não interpretados.')
 elif n.startswith('RESEST_arquivos'):r=('Baixa','Imagem de apoio ao resumo estrutural.','Não.','Sem base de esforços elemento por elemento.')
 else:r=('Condicional','Auxiliar de critérios, visualização, índices ou processamento; conteúdo parcial/opaco.','Não confirmado.','Consultar leitor/descrição antes de usar como fonte numérica.')
 ALL.append(dict(arquivo=n,bytes=i['bytes'],modificado=i['modified'],utilidade=r[0],conteudo=r[1],esforcos_por_elemento=r[2],verificacao=r[3],sha256=i['sha256']))
with (P/'catalogo_arquivos.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(ALL[0]),delimiter=';');w.writeheader();w.writerows(ALL)
# Relatório HTML/PDF + versão textual.
parts=[]
def p(t):parts.append('<p>'+t+'</p>')
def h(t):parts.append('<h2>'+t+'</h2>')
def table(head,rs):parts.append('<table><tr>'+''.join('<th>'+html.escape(x)+'</th>' for x in head)+'</tr>'+''.join('<tr>'+''.join('<td>'+html.escape(str(x))+'</td>' for x in row)+'</tr>' for row in rs)+'</table>')
parts.append('<h1>Arquivos do modelo TQS — ESPACIAL</h1>');p('<b>Silva Jardim · R35 · inspeção em 09/10/2026</b>')
p('Diretório inspecionado: '+html.escape(str(S))+'. Foram inventariados <b>163 arquivos, incluindo subpastas, totalizando 179.524.640 bytes</b>. Nenhum arquivo de projeto foi alterado. Esta investigação identifica fontes de dados; não recalcula nem aprova a estrutura.')
h('1. Resultado principal')
p('<b>Há esforços por elemento e por combinação disponíveis nos arquivos FOR0212.RSX e PORTELS.RSX.</b> Foi possível decodificar a organização dos registros e extrair um piloto das vigas V606 e V623, no piso físico 5. A identidade das barras vem do relatório PORFOR.LST; as definições dos casos/combinações vêm dos respectivos arquivos POR.')
p('A leitura não ficou restrita à identificação das extensões: os resultados binários foram comparados às listagens textuais. O modelo principal contém <b>20 casos básicos + 80 combinações = 100 registros</b>; o modelo ELS contém <b>20 casos básicos + 22 combinações = 42 registros</b>. Ambos possuem 2.751 nós, 3.757 barras e 76 apoios.')
p('Cada registro binário inclui seis componentes por nó, doze componentes por barra (seis em cada extremidade) e seis componentes por apoio. Os arquivos POR contêm <b>entrada e cargas aplicadas</b>; os esforços internos calculados estão na base RSX. FORCAS não deve ser interpretado como esforço interno da barra.')
h('2. Fontes prioritárias para integrar combinações separadas')
for title,names in [('Resultados, geometria e identidade',['FOR0212.RSX','PORTELS.RSX','FOR0212.POR','PORTELS.POR','PORFOR.LST','PORFORELS.LST','CARDWG2.LST']),('Combinações, critérios e validação',['CARRPOR.DAT','CRITPOR.DAT','FOR0212.Lst','PORTELS.Lst','PORLIS2.LST','PORALF.LST','PORALF.HTM'])]:
 parts.append('<h3>'+title+'</h3>');table(['Arquivo','Conteúdo confirmado','Esforços por elemento / limite'],[(n,CAT[n][1],CAT[n][2]+' '+CAT[n][3]) for n in names])
h('3. Demais arquivos úteis e auxiliares')
names=['PBETAD.DAT','PORLID2.DAT','PORLID3.DAT','PORLID2.XLSX','PGLOERR.HTM','MENAVI.LST','PILAR.LST','CARPIL.LST','CONTPOR.DAT','PORGZTP.DAT','PORGZTV.DAT','ESPECTRO.DAT','RESDES.HTM']
table(['Arquivo','Conteúdo / finalidade','Esforços e ressalvas'],[(n,CAT[n][1],CAT[n][2]+' '+CAT[n][3]) for n in names])
table(['Família','Conteúdo / utilidade','Situação'],[
 ('FOR0212/PORTELS.RPF e .POD','Auxiliares binários de geometria/visualização/organização.','Cabeçalhos/estrutura inspecionados; sem semântica completa de resultados.'),
 ('FOR0212/PORTELS.BPq','Nós de extremidade, tipo e comprimento das barras; diagnóstico geométrico.','Não são esforços; não interpretar o campo Gama como gamma_f sem documentação.'),
 ('FOR0212.EDI/.POP; COORD.TMP; C0010100…C0161400.TMP','Vínculos aos pavimentos, identificação e auxiliares de cálculo.','Conteúdo parcial; PORFOR já oferece mapa textual utilizável.'),
 ('CRITPOR2.DAT / EAGCRIT.DAT / EAGPOR2.DAT / EAGPORPARVIS.DAT','Critérios binários e parâmetros auxiliares de visualização.','Não interpretados como forças ou combinações numéricas.'),
 ('*.E3D','Histórico de visualização/modelo, incluindo estudos e revisões R01–R34.','Binários; esforços não confirmados. Não há E3D com nome R35 no inventário.'),
 ('CARPIL.DWG / RESDESDWG.DWG e respectivos .BAK','Desenhos e cópias de segurança associados aos relatórios.','Não extraídos pelo leitor de DWG nesta investigação; preferir os textos atuais.'),
 ('RESEST1…8.TXT','Relação de plantas, quantitativos, índices, custos, furos e carbono.','RESEST6 vazio; demais conteúdos constam individualmente no CSV.'),
 ('ERROS.DAT/.IND','Base e índices binários de avisos/erros.','Detalhes por elemento dependem de leitura específica; PGLOERR é resumo global.'),
 ('CARDWG.LST / PORVIG.LST','Logs de processamento e referências de plantas.','Sem tabela completa de esforços.'),
 ('tqsdesktopb e RESEST_arquivos','Miniaturas/cache e imagens auxiliares.','Sem utilidade numérica confirmada para esforços.'),
 ('Arquivos vazios','PORGAMZ.LST, PORTRN.LST, RESESTERR.LST, RESEST6.TXT e EAGPOR_FOR0212.POR.DWG.','Não oferecem dados nesta cópia.')])
p('O <b>catalogo_arquivos.csv</b> relaciona individualmente os 163 arquivos, com tamanho, data, conteúdo identificado, disponibilidade de esforços, limitações e SHA256. Extensão binária ou nome sugestivo, isoladamente, não comprovam conteúdo.')
h('4. O que foi extraído e como foi conferido')
table(['Controle','Modelo principal','Modelo ELS'],[
 ('Arquivo / registros','FOR0212.RSX / 100','PORTELS.RSX / 42'),('Tamanho da base (bytes)','49.636.860','20.847.516'),('Cabeçalho / bloco por registro','60 / 496.368 bytes','60 / 496.368 bytes'),('Deslocamentos por registro','2.751 × 6 valores de 8 bytes','2.751 × 6 valores de 8 bytes'),('Esforços por registro','3.757 × 12 valores de 8 bytes','3.757 × 12 valores de 8 bytes'),('Reações por registro','76 × 6 valores de 8 bytes','76 × 6 valores de 8 bytes'),('Componentes de reação comparados','45.600','19.152'),('Maior diferença com impressão de duas casas',f"{V[0]['max_desvio_reacoes']:.8f}",f"{V[1]['max_desvio_reacoes']:.8f}")])
p('Os tamanhos fecham exatamente, sem bytes remanescentes. Foram comparadas todas as reações publicadas: 7.600 linhas nó–caso no principal e 3.192 no ELS. A tolerância adotada foi 0,00501 na unidade impressa, compatível com impressão em duas casas e pequenas diferenças de representação numérica. Esta conferência valida a extração desses dados, não a correção física do modelo.')
p('Adicionalmente, foram comparados <b>612 registros de lances de pilares</b>, com N, My e Mz nas duas extremidades: 3.672 componentes, maior diferença de 0,00499446. A leitura reproduziu os valores da listagem PORLIS2 para o caso 1. Para o fim da barra, a listagem de pilares usa o sinal oposto ao registro de ação nodal do RSX. Isso exige um contrato explícito de sinais antes de alimentar as ferramentas de dimensionamento.')
p('A interpretação de sistema local foi comprovada para N/My/Mz nos pilares examinados. O piloto conserva os doze valores como C1…C12 para não antecipar normalizações: C1/C7 correspondem ao axial, C5/C11 e C6/C12 aos momentos locais conferidos; a associação completa dos cortantes e torção, orientação local e sinais de diagrama deve ser validada com consultas do visualizador de vigas. Unidades de referência publicadas: tf para forças e tf·m para momentos; não foram aplicados majoradores nem conversões adicionais.')
h('5. Identidade das vigas TIPO e combinação governante')
p('O pavimento TIPO representa <b>cinco pisos físicos</b> no pórtico: 5, 6, 7, 8 e 9. As vigas com o mesmo nome aparecem em cotas e com IDs de barras distintos. Portanto, a chave deve incluir modelo + piso + viga + barra + caso + extremidade. Usar apenas V606, por exemplo, não identifica um único resultado.')
table(['Piso físico','Cota (m)','Projeto/planta','Redutor publicado'],[(5,'35,28','0500 / TIPO','0,40'),(6,'38,08','0500 / TIPO','0,20'),(7,'40,88','0500 / TIPO','0,00'),(8,'43,68','0500 / TIPO','0,00'),(9,'46,48','0500 / TIPO','0,00')])
p('Exemplos do piso 5: V601 → barras 1556,1559,1561,1563,1565,1567,1569,1571; V606 → 1605; V623 → 1682,1684. No piso 6, V606 → 1798; no piso 7 → 1991; no piso 8 → 2184; no piso 9 → 2377. A correspondência fina das barras auxiliares, offsets, nós e trechos físicos ainda precisa ser mapeada; a relação PORFOR sozinha não descreve todas as regiões de dimensionamento.')
p('Modelo principal: combinações 21–100, sendo 38 ELU1, 38 ELU2, 2 FOGO e 2 COMBFLU. Modelo ELS: combinações 21–42, sendo 20 ELS e 2 FOGO. <b>O ID 21 tem significados distintos:</b> no principal é ELU1/PERM/PP+PERM+EMPU; no ELS é FOGO/PERMVAR/PP+PERM+EMPU+0.3ACID. Não unir os catálogos pelo número isolado.')
p('A envoltória principal publicada para transferência às vigas reúne 38 combinações: 21–39 e 61–79. Isso precisa ser preservado ao comparar o pórtico com VGESFS. As demais combinações podem existir na base sem integrar a envoltória de vigas transferida nesta execução.')
p('A definição de combinação 23 no principal contém PP, PERM e EMPU com fatores 1,0, ACID com fator 1,0 e VENT1 com fator 0,6. Esses fatores pertencem ao arquivo de análise: não comprovam, por si só, a ausência de amplificações/normalizações em outras etapas. PORALF publica gammaF/gammaF3 = 1,27; PORFOR documenta GAMAZ e critérios de transferência. Parte das combinações é identificada como CBNL na listagem. Não reconstruir seus resultados por superposição linear dos casos sem validar o procedimento do TQS.')
h('6. Arquivos de exemplo entregues')
table(['Arquivo gerado','Conteúdo'],[
 ('catalogo_arquivos.csv','163 fontes individualizadas; utilidade, conteúdo, esforços, datas e hashes.'),
 ('catalogo_casos_combinacoes.csv','142 entradas: casos/combinações dos dois modelos, títulos, linhas e componentes.'),
 ('mapa_vigas_barras.csv','1.550 associações de viga/piso/barra, com linha-fonte.'),
 ('reacoes_por_caso.csv','10.792 registros de apoio/caso dos dois modelos; componentes e desvio da listagem.'),
 ('piloto_esforcos_v606_v623_piso5.csv','426 linhas: V606 (1 barra) e V623 (2 barras), 100+42 casos/combinações; doze valores brutos por barra.'),
 ('modelo_e_combinacoes.json','Nós, barras, catálogo e envoltória; fontes textuais preservadas.'),
 ('validacao_extracao_rsx.json','Dimensões binárias, contagens e controles de comparação.'),
 ('extract_and_validate.py','Leitor local reproduzível para os arquivos desta cópia; sem gravação na pasta TQS.')])
p('Exemplo real, V606 / piso 5 / barra 1605 / principal / caso 1: C1=-0,08838467 tf; C3=4,42697239 tf; C5=-0,14562112 tf·m; C7=0,08838467 tf; C9=4,19090748 tf; C11=0,89499760 tf·m. São valores das extremidades da barra, não a envoltória das 13 seções de VGESFS. O piloto é evidência de acesso aos dados, sem verificação resistente nova.')
h('7. Cuidados que afetam a próxima etapa')
p('<b>Planilha histórica:</b> PORLID2.XLSX foi modificada em 07/08/2026 e contém referência interna a um diretório R27. Apresenta grupos A/B/C e esforços de pilares associados a extremos de Fz. Precisa de confirmação de origem para qualquer uso na R35; não deve substituir RSX atual ou combinar máximos independentes.')
p('<b>Histórico 3D:</b> o último arquivo E3D pelo horário tem nome R34; os resultados de processamento principal/ELS são de 08/10/2026. O nome do diretório R35 não atualiza automaticamente todos os arquivos herdados.')
p('<b>Avisos existentes:</b> PGLOERR informa categorias de erros graves, incluindo mensagens de ancoragem, tração, cisalhamento/torção, espaçamento e deslocamento horizontal. O resumo não localiza todos esses avisos por elemento. MENAVI cita vigas 150/352. Esta investigação não atribui essas mensagens às vigas TIPO nem revisa sua validade; elas devem acompanhar a validação futura do modelo.')
p('<b>Esforços ao longo da barra:</b> os registros identificados no RSX são de extremidades. Para diagramas e seções intermediárias, será necessário combinar geometria, cargas, convenção local e formulação do elemento, ou obter os diagramas por exportação/consulta TQS. Não interpolar linearmente momentos quando houver cargas distribuídas ou pontos internos.')
p('<b>Concomitância e suspensão:</b> a base permite selecionar o mesmo caso para a viga apoiada e a receptora. A reação transmitida entre vigas precisa ser obtida por equilíbrio do nó/encontro, considerando todas as barras e cargas relevantes; as reações de fundação do RSX não substituem essa transferência.')
p('<b>Validação restante:</b> conferir em vigas selecionadas, no visualizador TQS, os seis componentes e sua orientação; relacionar extremidades nodais às faces físicas; confirmar natureza e fatores de resultados e transferência; comparar com VGESFS; verificar se o detalhamento TIPO representa envoltória dos cinco pisos. A estrutura binária reconhecida deve ser testada antes de reutilização em outra versão de TQS.')
h('8. Documentação externa consultada')
p('A documentação oficial descreve o POR como arquivo de dados do pórtico, com resultados de deslocamentos, esforços nas barras e reações obtidos pelo resolvedor. A identificação específica e a decodificação dos RSX desta pasta foram verificadas localmente; não foi localizada uma especificação pública do seu layout binário.')
p('<a href="https://docs.tqs.com.br/Docs/Details?id=3150&language=pt-BR">TQS — Pórtico espacial / processamento</a>. <a href="https://docs.tqs.com.br/Docs/Details?id=3156&language=pt-BR">TQS — Transferência de esforços</a>. Essas fontes sustentam a distinção entre análise e transferência; não substituem as comparações numéricas desta inspeção.')
body='\n'.join(parts);css='body{font-family:sans-serif;font-size:10pt;color:#17283a}h1{font-size:22pt;color:#143c58}h2{font-size:14pt;color:#143c58;margin-top:18pt}h3{font-size:11pt}p{line-height:1.3}table{border-collapse:collapse;width:100%;margin:8pt 0}td,th{border:0.5pt solid #bac8d2;padding:5pt;vertical-align:top;font-size:8.5pt}th{font-weight:bold}a{color:#17567a}'
full='<html><head><meta charset="utf-8"><title>Inspeção ESPACIAL TQS</title><style>'+css+'</style></head><body>'+body+'</body></html>'
(P/'Relatorio_arquivos_ESPACIAL.html').write_text(full,encoding='utf-8')
plain=body.replace('</p>','\n\n').replace('</h2>','\n\n').replace('</h1>','\n\n').replace('</h3>','\n\n').replace('</tr>','\n').replace('</td>',' | ').replace('</th>',' | ')
import re
(P/'Relatorio_arquivos_ESPACIAL.txt').write_text(html.unescape(re.sub('<[^>]+>','',plain)),encoding='utf-8')
story=fitz.Story(html=body,user_css=css);doc=fitz.open();writer=fitz.DocumentWriter(str(P/'Relatorio_arquivos_ESPACIAL_sem_rodape.pdf'));more=True
while more:
 dev=writer.begin_page(fitz.Rect(0,0,595,842));more,_=story.place(fitz.Rect(36,35,559,802));story.draw(dev);writer.end_page()
writer.close();doc=fitz.open(str(P/'Relatorio_arquivos_ESPACIAL_sem_rodape.pdf'))
for idx,page in enumerate(doc):page.insert_text((36,824),'Silva Jardim R35 | Fontes ESPACIAL | 09/10/2026 | '+str(idx+1)+'/'+str(len(doc)),fontsize=8,color=(.3,.4,.5))
doc.save(str(P/'Relatorio_arquivos_ESPACIAL.pdf'),garbage=4,deflate=True)
# Visualizações para controle de apresentação.
for idx in [0,min(3,len(doc)-1),len(doc)-1]:doc[idx].get_pixmap(matrix=fitz.Matrix(1.4,1.4),alpha=False).save(str(P/f'preview_{idx+1}.png'))
files=['Relatorio_arquivos_ESPACIAL.pdf','Relatorio_arquivos_ESPACIAL.html','Relatorio_arquivos_ESPACIAL.txt','catalogo_arquivos.csv','catalogo_casos_combinacoes.csv','mapa_vigas_barras.csv','reacoes_por_caso.csv','piloto_esforcos_v606_v623_piso5.csv','modelo_e_combinacoes.json','validacao_extracao_rsx.json','inventario_com_hashes.json','extract_and_validate.py']
with zipfile.ZipFile(P/'Relatorio_ESPACIAL_e_extracoes.zip','w',zipfile.ZIP_DEFLATED) as z:
 for n in files:z.write(P/n,n)
print('REPORT',len(doc),'pages','ZIP',(P/'Relatorio_ESPACIAL_e_extracoes.zip').stat().st_size)


