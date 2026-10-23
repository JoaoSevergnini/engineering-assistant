from pathlib import Path
import json,math,collections,hashlib
from io import BytesIO
import fitz
from PIL import Image,ImageEnhance
from shapely.geometry import shape,box
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor,Color,white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
out=Path(r'P:\Joao Severgnini\Simon\engineering-assistant\analises\atp_s07_lajes_terreo');dest=out/'output'/'pdf';dest.mkdir(parents=True,exist_ok=True)
rs=json.loads((out/'regioes_capacidades.json').read_text(encoding='utf8'));oo=json.loads((out/'ocorrencias_extraidas.json').read_text(encoding='utf8'));inv=json.loads((out/'inventario.json').read_text(encoding='utf8'));prov=json.loads((out/'proveniencia_calculos.json').read_text(encoding='utf8'))
pdfmetrics.registerFont(TTFont('Arial',r'C:\Windows\Fonts\arial.ttf'));pdfmetrics.registerFont(TTFont('ArialB',r'C:\Windows\Fonts\arialbd.ttf'))
W,H=1190.55,841.89;c=canvas.Canvas(str(dest/'ATP_S07_lajes_terreo_mapa_preliminar.pdf'),pagesize=(W,H));c.setTitle('ATP S07 - Lajes do térreo - mapa preliminar de armaduras e capacidades nominais');page=0
NAVY=HexColor('#163349');BLUE=HexColor('#087CA7');PURPLE=HexColor('#7550A3');ORANGE=HexColor('#A65B00')
def start(title,sub=''):
 global page
 page+=1;c.setFillColor(NAVY);c.rect(0,H-69,W,69,fill=1,stroke=0);c.setFillColor(white);c.setFont('ArialB',18);c.drawString(30,H-32,title);c.setFont('Arial',9);c.drawString(30,H-51,sub[:190]);c.setFillColor(NAVY);c.setFont('Arial',8);c.drawString(30,20,'TERRA ALL RESORT | ATP S07 | 19/10/2026 | PRELIMINAR - capacidades nominais, sem aprovação das lajes');c.drawRightString(W-30,20,f'{page}');c.setStrokeColor(HexColor('#BCC8CF'));c.line(30,32,W-30,32)
def end():c.showPage()
def wrapped(text,x,y,width,size=11,leading=16,font='Arial'):
 c.setFillColor(NAVY);c.setFont(font,size);words=text.split();line=''
 for w in words:
  if pdfmetrics.stringWidth(line+' '+w,font,size)>width and line:c.drawString(x,y,line);y-=leading;line=w
  else:line=(line+' '+w).strip()
 if line:c.drawString(x,y,line);y-=leading
 return y
start('Lajes do térreo - faixas e capacidades nominais','Formas 7202 R03 / 7214 R01 | Detalhamentos 7301-7308 | PDF de trabalho para revisão técnica')
y=H-112
for title,txt in [
 ('Objetivo','Identificar as faixas desenhadas, suas composições nominais e As por metro, com momentos resistentes calculados pelo Concretopy. Este documento registra uma rodada preliminar: a leitura de todas as faixas e a compatibilidade física integral entre forma e detalhamento ainda não estão encerradas.'),
 ('O que os mapas mostram','As regiões coloridas representam presença nominal de barras e hipóteses geométricas de seção. Os valores são resistências de seções com aço mobilizado, sem verificação do desenvolvimento dessa resistência junto a cortes, ancoragens e emendas. Não são envoltórias resistentes efetivas ao longo de toda a extensão das barras.'),
 ('Convenção de leitura','Em cada rótulo: Rxxx identifica a região na prancha; a segunda linha mostra As [cm²/m] | M_eq [tf·m/m]. M_eq = |MRd|/1,4 é resistência equivalente para comparação. O sinal da flexão é informado pelo tipo POS/NEG; os números resistentes são módulos. As tabelas preservam também |MRd| de cálculo.'),
 ('Pendências explícitas',f'Foram extraídas {len(oo)} ocorrências candidatas, das quais {sum(o["spacing_cm"] is not None for o in oo)} têm espaçamento legível e {sum(o["spacing_cm"] is not None and o["region_pdf"] is not None for o in oo)} têm uma envoltória nominal associada. São {len(rs)} regiões após divisões e uniões geométricas. Há {sum(bool(r["issues"]) for r in rs)} regiões com composição não fechada: o momento composto fica em branco; as capacidades individuais constam em quadro próprio. A contagem não é uma medição de acerto nem prova de cobertura integral.'),
 ('Limite do resultado','Não foram comparados momentos solicitantes, flechas, fissuração, punção, cisalhamento, mínimos de lajes, ancoragens ou traspasses. Não há aprovação normativa ou resistente global. O texto da NBR 6118:2023 não foi efetivamente consultado nesta rodada; os coeficientes e o modelo do motor estão identificados, sem certificação da implementação normativa completa.')]:
  y=wrapped(title,40,y,W-80,13,18,'ArialB');y=wrapped(txt,40,y-2,W-80,11,16)-18
end()
start('Premissas, origem e método','Dados do projeto, orientações de João e hipóteses do processamento são identificados separadamente')
y=H-106
paragraphs=[
'DADOS DAS PRANCHAS: cobrimento positivo e negativo de lajes = 3,0 cm nas formas. Espessura geral h=20 cm; elevadores L2/L3/L6/L7 h=15 cm, L4/L5 h=20 cm; fundos LF701-LF704 h=30 cm; tampas LT701-LT704 h=12 cm. As referências locais foram lidas nas pranchas, sem aplicar +9,37 m aos desníveis. O agregado de 16 mm vem da informação de João e não interfere diretamente nesta resistência à flexão.',
'MATERIAIS: verde nativo da legenda das pranchas de armaduras = C35; zona não sombreada da planta = C40. Não se usaram os retângulos ciano anotados por João como fonte de geometria ou de material. Tabelas de aço: Ø5 CA60, demais bitolas utilizadas CA50. A conciliação completa de materiais por etapa, encontro e forma continua pendente; as tabelas mostram o fck aplicado a cada região.',
'ORIENTAÇÕES DE JOÃO NESTA CONVERSA: horizontal na primeira camada; vertical na segunda; reforços positivos intercalados com a base na mesma camada física. γf=1,4 autorizado para apresentar as resistências equivalentes das lajes. A concretagem inicial na região dos reservatórios até +9,28 m é contexto, sem aprovação de continuidade ou de juntas.',
'ALTURA ÚTIL: horizontal d=h-3,0-φ/20, com φ em mm. Para a vertical, desconta-se ainda o maior diâmetro horizontal conhecido que intersecta a região. Esta envoltória é conservadora dentro da região reconstruída e não comprova a montagem local. Onde não houve associação horizontal, adotou-se provisoriamente um envelope de 20 mm; essas regiões são marcadas com asterisco. Barras localizadas de furos ainda não estão integralmente conciliadas com essa ordem vertical.',
'COMPOSIÇÃO: As individual = área circular da barra x 100/s, com s em cm. Base Ø8 c/14 em h=20 é contada uma vez nos traspasses, mesmo com mais de uma chamada. Famílias de reforço distintas são somadas nominalmente. Sobreposição de famílias iguais com marcas diferentes é pendência; não recebe momento composto. Por orientação de João, sobreposições de negativas de apoios distintos têm capacidades individuais, com soma pendente da verificação de ancoragem, inclusive quando as bitolas ou os espaçamentos diferem. Famílias locais sem espaçamento não foram espalhadas artificialmente em uma faixa de 1 m.',
'CONCRETOPY: verificar_flexao_viga_retangular, bloco retangular com camadas tracionadas escoadas. Para representar taxas contínuas e barras intercaladas de bitolas distintas, preservam-se o resultante de tração e seu centro: As equivalente CA50 = Σ(As_i fyd_i)/fyd_CA50 e d_eq = Σ(As_i fyd_i d_i)/Σ(As_i fyd_i). A largura normalizada permite número inteiro de barras; o momento é convertido novamente para 1 m. O escoamento das famílias reais foi conferido separadamente.',
'PARÂMETROS DO MOTOR: γc=1,4; γs=1,15; γf=1,4 apenas na apresentação equivalente. O argumento geométrico do motor usa 2,5 cm + 5 mm para manter a referência efetiva de 3,0 cm, com d explícito; não representa estribos físicos nas lajes. Não se usou empilhamento automático de vigas nem se alterou o Concretopy. A armadura da face comprimida foi excluída.',
'RASTREABILIDADE: inventario.json contém arquivos, revisões e SHA-256; ocorrencias_extraidas.json contém chamadas, caixas PDF e diagnósticos; regioes_capacidades.json preserva polígonos, referências, famílias e resultados brutos; proveniencia_calculos.json identifica motor, parâmetros e assinatura. Os polígonos são coordenadas PDF, não levantamento executivo ou contornos de lajes certificados.'
]
for t in paragraphs:y=wrapped(t,40,y,W-80,10,14)-12
end()
start('Documentos e roteiro de conferência','Critérios de ATP: separar requisitos comprovados, recomendações e leitura ainda não concluída')
y=H-105
for e in inv:
 y=wrapped(e['sheet']+' | '+Path(e['path']).name+' | SHA-256 '+e['sha256'][:16]+'...',40,y,W-80,10,15)
y-=25
for t in [
'1. Identificação e revisão: conferir pavimento, partes 1/2, lajes L1-L9, LT701-LT704 e LF701-LF704, correspondência entre prancha e forma e existência de chamadas sem elemento correspondente.',
'2. Geometria: contornos, espessuras, rebaixos, rampas, níveis locais, juntas e aberturas; compatibilizar com as formas 7202/7214. O rótulo L1/L8 das tabelas conserva a região geral da parte 1; a fronteira completa entre essas identificações ainda não foi individualizada nesta rodada.',
'3. Apoios e etapas: vigas, blocos, pilares e paredes; faces físicas, caminhos de carga, concretagem posterior aos blocos e etapa dos reservatórios. A continuidade desenhada não demonstra isoladamente continuidade resistente da junta.',
'4. Armaduras: cada chamada, bitola, classe, espaçamento, direção física, camada, extensão e eixo de distribuição. Distinguir base, reforço, traspasse, contorno de abertura e armadura localizada. Conferir candidatos extraídos nas ampliações.',
'5. Capacidades: conferir As, d e materiais por região, depois as solicitações com origem/natureza comprovadas. Em etapa posterior: mínimos próprios de lajes, desenvolvimento de barras, ELS, cisalhamento/punção e demais verificações acordadas.',
'CLASSIFICAÇÕES: divergência confirmada exige duas informações compatíveis em identidade e contraditórias; hipótese é uma entrada provisória; informação ausente exige busca concluída sem o dado; verificação não realizada inclui leituras ainda pendentes do assistente. Nenhuma pendência de leitura deste PDF foi automaticamente atribuída ao projetista.'
]:y=wrapped(t,40,y,W-80,11,16)-13
end()
# Per drawing: overview, enlarged tiles and exhaustive regional table.
for e in inv[2:]:
 n=e['sheet'];regs=[r for r in rs if r['sheet']==n];oc=[o for o in oo if o['sheet']==n];source=fitz.open(e['path']);p=source[0];part=1 if int(n)<7305 else 2;face='POSITIVA' if n in ['7301','7302','7305','7306'] else 'NEGATIVA';direction='HORIZONTAL' if n in ['7301','7303','7305','7307'] else 'VERTICAL';color=BLUE if face=='POSITIVA' else PURPLE
 bounds=fitz.Rect(130,110,2110,2240) if part==1 else fitz.Rect(180,340,2100,1590)
 def mapview(clip,full=False):
  area=(35,54,W-70,H-142);ax,ay,aw,ah=area;sc=min(aw/clip.width,ah/clip.height);dx=ax+(aw-clip.width*sc)/2;dy=ay+(ah-clip.height*sc)/2
  pix=p.get_pixmap(matrix=fitz.Matrix(1.4,1.4),clip=clip,annots=False);im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples);im=Image.blend(im,Image.new('RGB',im.size,'white'),.40)
  c.drawImage(ImageReader(im),dx,dy,width=clip.width*sc,height=clip.height*sc)
  clip_poly=box(*clip);visible=[];occupied=[]
  def pt(x,y):return dx+(x-clip.x0)*sc,dy+(clip.y1-y)*sc
  for r in regs:
   geom=shape(r['geometry']).intersection(clip_poly)
   if geom.is_empty or geom.area<2:continue
   geoms=[geom] if geom.geom_type=='Polygon' else list(getattr(geom,'geoms',[]))
   fill=ORANGE if r['issues'] else color;opacity=.12 if full else .16
   c.setFillColor(Color(fill.red,fill.green,fill.blue,alpha=opacity));c.setStrokeColor(Color(fill.red,fill.green,fill.blue,alpha=.65));c.setLineWidth(.45)
   for poly in geoms:
    if poly.geom_type!='Polygon':continue
    path=c.beginPath()
    for ring in [poly.exterior,*poly.interiors]:
     coords=list(ring.coords);xx,yy=pt(*coords[0]);path.moveTo(xx,yy)
     for x,y in coords[1:]:xx,yy=pt(x,y);path.lineTo(xx,yy)
     path.close()
    c.drawPath(path,fill=1,stroke=1,fillMode=0)
   visible.append((r,geom))
  if not full:
   # Deterministic placement: full label only when it fits the visible polygon; no collisions.
   for r,geom in sorted(visible,key=lambda z:z[1].area):
    val=r['result']['M_equivalent_tfm_m'];lines=[r['id'].split('-')[1],('INDIV. / QUADRO' if val is None else f"{r['result']['As_cm2_m']:.2f} | {val:.2f}")];font=6.5;width=max(pdfmetrics.stringWidth(t,'ArialB',font) for t in lines)+5;height=19
    center=geom.representative_point();px,py=pt(center.x,center.y);rect=(px-width/2,py-height/2,px+width/2,py+height/2)
    def overlap(a,b):return a[0]<b[2]+2 and a[2]>b[0]-2 and a[1]<b[3]+2 and a[3]>b[1]-2
    if rect[0]<dx or rect[2]>dx+clip.width*sc or rect[1]<dy or rect[3]>dy+clip.height*sc or any(overlap(rect,z) for z in occupied):continue
    # Very small fragments use a compact ID, linked to the table; keep labels readable.
    if geom.area*sc*sc<width*height*.7:lines=lines[:1];height=10;rect=(px-width/2,py-height/2,px+width/2,py+height/2)
    occupied.append(rect);c.setFillColor(Color(1,1,1,alpha=.93));c.roundRect(rect[0],rect[1],width,height,2,fill=1,stroke=0);c.setFillColor(ORANGE if r['issues'] else NAVY);c.setFont('ArialB',font)
    for j,t in enumerate(lines):c.drawCentredString(px,rect[3]-7.5-j*8,t)
  # Missing distributed geometry is explicitly marked by its occurrence ID at the label.
  for o in oc:
   if o['spacing_cm'] is None or o['region_pdf'] is not None:continue
   a,b,cc,d=o['label_rect'];cx=(a+cc)/2;cy=(b+d)/2
   if clip.contains(fitz.Point(cx,cy)):
    px,py=pt(cx,cy);c.setStrokeColor(ORANGE);c.setLineWidth(1);c.circle(px,py,7,fill=0,stroke=1);c.setFillColor(ORANGE);c.setFont('ArialB',6);c.drawString(px+8,py+3,o['id'].split('-')[1])
 start(f'{n} | {face} {direction} | parte {part}',f'{len(regs)} regiões nominais | Azul/roxo: presença nominal | Laranja: composição ou associação pendente | Ver ampliações e tabelas')
 mapview(bounds,True);end()
 nx=2;ny=3 if part==1 else 2
 for j in range(ny):
  for i in range(nx):
   clip=fitz.Rect(bounds.x0+i*bounds.width/nx,bounds.y0+j*bounds.height/ny,bounds.x0+(i+1)*bounds.width/nx,bounds.y0+(j+1)*bounds.height/ny)
   start(f'{n} | ampliação {j*nx+i+1}/{nx*ny} | {face} {direction}','Rótulo: região / As [cm²/m] | M_eq = |MRd|/1,4 [tf·m/m]. Sem rótulo legível: localizar pela tabela e pelas marcas de origem.')
   mapview(clip);end()
 # tabular region schedule, 44 rows/page
 for k in range(0,len(regs),43):
  subset=regs[k:k+43];start(f'{n} | quadro de regiões {k+1}-{k+len(subset)} de {len(regs)}','As nominal [cm²/m] | h, d [cm] | fck [MPa] | módulos MRd e M_eq [tf·m/m]. Valores não comprovam ancoragem ou suficiência às solicitações.')
  cols=[35,85,270,570,615,660,710,780,850,930];headers=['Região','Laje / região','Marcas que incidem','h','fck','d_eq','As/m','|MRd|','M_eq','Observação']
  y=H-99;c.setFillColor(NAVY);c.setFont('ArialB',8)
  for x,t in zip(cols,headers):c.drawString(x,y,t)
  y-=15
  for idx,r in enumerate(subset):
   if idx%2==0:c.setFillColor(HexColor('#EEF3F6'));c.rect(30,y-4,W-60,15.4,fill=1,stroke=0)
   rr=r['result'];v=rr['M_equivalent_tfm_m'];marks=','.join(r['marks']);marks=(marks[:52]+'...') if len(marks)>55 else marks
   note='Ver capacidades individuais' if r['issues'] else ('* envelope H=20 mm' if r['offset_source'].startswith('HYPOTHESIS') else 'Nominal / conferir faixa')
   values=[r['id'].split('-')[1],r['slab'][:30],marks,str(r['h_cm']),str(r['fck_MPa']),f"{rr['d_equivalent_cm']:.2f}",'-' if r['issues'] else f"{rr['As_cm2_m']:.2f}",'-' if v is None else f"{rr['MRd_tfm_m']:.2f}",'-' if v is None else f"{v:.2f}",note]
   c.setFillColor(ORANGE if r['issues'] else NAVY);c.setFont('Arial',7.5)
   for x,t in zip(cols,values):c.drawString(x,y,t)
   y-=15.4
  end()

# Individual capacities required by João in overlaps. Never publish the hypothetical sum as effective resistance.
individual_rows=[]
for r in rs:
 for ic in r.get('individual_capacities',[]):individual_rows.append((r,ic))
for k in range(0,len(individual_rows),42):
 subset=individual_rows[k:k+42];start(f'Sobreposições | capacidades individuais {k+1}-{k+len(subset)} de {len(individual_rows)}','Orientação de João: soma pendente de ancoragem. Valores por família não são somáveis automaticamente. M_eq=|MRd|/1,4 [tf·m/m].')
 xs=[35,100,165,230,365,430,490,565,650,755,870];heads=['Prancha','Região','Marca','Armadura','h','fck','d','As/m','|MRd|','M_eq','Estado da composição'];y=H-100;c.setFillColor(NAVY);c.setFont('ArialB',8)
 for x,t in zip(xs,heads):c.drawString(x,y,t)
 y-=17
 for j,(r,ic) in enumerate(subset):
  z=ic['capacity'];v=z['M_equivalent_tfm_m']
  if j%2==0:c.setFillColor(HexColor('#F6F1E7'));c.rect(30,y-4,W-60,15.4,fill=1,stroke=0)
  vals=[r['sheet'],r['id'].split('-')[1],ic['mark'],f"Ø{ic['diameter_mm']:g} c/{ic['spacing_cm']:g}",str(r['h_cm']),str(r['fck_MPa']),f"{z['d_equivalent_cm']:.2f}",f"{z['As_cm2_m']:.2f}",'-' if v is None else f"{z['MRd_tfm_m']:.2f}",'-' if v is None else f"{v:.2f}",'Soma pendente / ancoragem']
  c.setFillColor(NAVY);c.setFont('Arial',8)
  for x,t in zip(xs,vals):c.drawString(x,y,t)
  y-=15.4
 end()
# unresolved rows: distinguish local from unread distributed.
pending=[o for o in oo if o['spacing_cm'] is not None and o['region_pdf'] is None]
for k in range(0,len(pending),28):
 sub=pending[k:k+28];start('Faixas distribuídas ainda sem região fechada',f'{len(pending)} ocorrências candidatas no conjunto. Círculos laranja nas ampliações. As individual não autoriza composição nem capacidade regional.')
 y=H-105
 for o in sub:
  text=f"{o['id']} | {o['mark']} Ø{o['diameter_mm']:g} c/{o['spacing_cm']:g} | As individual {o['As_individual_cm2_m']:.2f} cm²/m | {o['geometry_status']}"
  y=wrapped(text,40,y,W-80,9,14)-8
 end()

coverage=json.loads((out/'cobertura_posicoes_tabela.json').read_text(encoding='utf8'))
missing=[(n,t) for n,v in coverage.items() for t in v['missing_rows']]
start('Conciliação do quadro de aço | posições ainda sem chamada fechada','As posições abaixo existem no quadro de aço. Sua associação à planta não foi encerrada pelo assistente; não se aponta ausência de detalhamento.')
y=H-108
for n,t in missing:
 note='Detalhe localizado de furos, registrado separadamente' if n=='7305' and t['mark'] in ['N32','N33'] else 'Chamada / identidade ainda a conciliar'
 text=f"{n} | {t['mark']} | quadro: {t['quantity']} barras Ø{t['diameter_mm']:g}, C={t['C_cm']:g} cm | {note}"
 y=wrapped(text,40,y,W-80,10,15)-9
end()
start('Limitações, próximos controles e rastreabilidade','Não confundir leitura ainda não concluída pelo assistente com dado ausente no projeto')
y=H-108
for t in [
'LEITURA GEOMÉTRICA A CONCLUIR: as envoltórias foram obtidas de traços, círculos e eixos; as correspondências de proximidade precisam de revisão visual específica. As tabelas principais utilizam a direção física reconstruída junto ao título da folha. Barras localizadas permanecem separadas das taxas distribuídas.',
'CASO DOCUMENTAL LOCAL: a chamada N91 na 7301 indica 7Ø8 C=VAR, sem espaçamento na chamada consultada. Não foi arbitrada uma taxa As/m. Isso não demonstra, isoladamente, falta de definição da montagem no conjunto completo; a faixa e a distribuição devem ser conciliadas antes de atribuir capacidade por metro.',
'CONTORNOS E ABERTURAS: foram retirados alguns retângulos identificados por duas diagonais, mas a identificação não cobre todas as aberturas, contornos poligonais, chanfros ou recortes. O mapa é de presença nominal de armadura, não uma planta executiva com área líquida certificada. Não usar os polígonos para quantitativos ou locação.',
'REGIÕES ESPECIAIS: as caixas locais de LT/LF/elevadores representam referências de seção lidas no desenho e precisam de conciliação integral de contorno, apoio, nível e material com as formas. Fragmentos fora dessas caixas não demonstram transição física para h=20. A identificação L1/L8 deve ser individualizada antes da emissão final.',
'BARRAS LOCALIZADAS: chamadas sem espaçamento, reforços diagonais de furos, contornos e peças em U não receberam uma taxa inventada por metro. Deve-se definir sua faixa efetiva e função antes de calcular uma resistência regional por metro. Quantidade total de barras e comprimento nominal não substituem essa definição.',
'RESISTÊNCIA EFETIVA: a seção pode mobilizar o valor tabulado somente onde a armadura estiver adequadamente desenvolvida. Ancoragem, corte, traspasse, junta de concretagem e redistribuição de esforços não foram verificados. Nenhuma região foi classificada como suficiente ou insuficiente frente a solicitações.',
'ESTADO DOS APONTAMENTOS: não se emite divergência confirmada de lajes nesta rodada apenas com base na extração. Hipóteses incluem a posição vertical pela envoltória horizontal e associações geométricas candidatas. As pendências são de análise e conciliação; eventual informação ausente no projeto será identificada após consulta específica.',
'PROCEDIMENTOS: aplicados os princípios gerais da skill reinforcement-review: origem dos dados, composição por região, separação de ATP e padrões internos, Concretopy oficial e resultados brutos. Procedimentos específicos de vigas e pilares, ancoragens e apoios não foram transferidos às lajes. A skill PDF orientou a geração e a inspeção visual.',
'CONFERÊNCIA DOS RESULTADOS: auditoria auxiliar independente do equilíbrio preservou a origem oficial Concretopy e confirmou a transformação da largura e do resultante. Não constitui teste normativo da biblioteca. Registros e conferências visuais locais estão arquivados na pasta da análise.',
'PRÓXIMA ETAPA: conferir todas as associações candidatas e as pendências geométricas; fechar contornos, classes/etapas e camadas; resolver sobreposições; emitir mapa nominal definitivo. Depois, definir o escopo de solicitações, mínimos, ELS, punção/cisalhamento e desenvolvimento das armaduras.'
]:y=wrapped(t,40,y,W-80,10,14)-16
end();c.save()
print(str(dest/'ATP_S07_lajes_terreo_mapa_preliminar.pdf'));print('pages',page)
# Compact handoff + machine-readable coverage and audit.
summary=dict(pages=page,regions=len(rs),candidate_occurrences=len(oo),distributed_occurrences=sum(o['spacing_cm'] is not None for o in oo),distributed_with_rectangle=sum(o['spacing_cm'] is not None and o['region_pdf'] is not None for o in oo),unresolved_distributed=len(pending),ambiguous_composition_regions=sum(bool(r['issues']) for r in rs),vertical_hypothesis_regions=sum(r['offset_source'].startswith('HYPOTHESIS') for r in rs),all_real_yield=all(r['result'].get('all_real_families_yield') for r in rs),preliminary=True,approval=False)
(out/'cobertura.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding='utf8');print(summary)
