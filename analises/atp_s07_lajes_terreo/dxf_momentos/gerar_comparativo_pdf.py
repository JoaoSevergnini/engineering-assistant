from pathlib import Path
import json,math,csv,io,collections,hashlib
import fitz
from shapely.geometry import shape,Point
from shapely.affinity import affine_transform
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor,Color,white
from PIL import Image,ImageDraw,ImageFont
r=Path(__file__).parent;root=r.parent;tmp=root/'tmp/pdfs';dest=root/'output/pdf';dest.mkdir(exist_ok=True)
d=json.loads((r/'comparacao_resultados.json').read_text(encoding='utf8'));rows=d['rows'];caps=json.loads((root/'regioes_capacidades.json').read_text(encoding='utf8'));caplookup={s['id']:s for s in caps};inv=json.loads((root/'inventario.json').read_text(encoding='utf8'))
assert hashlib.sha256((root/'regioes_capacidades.json').read_bytes()).hexdigest()==d['source_capacities_sha256']
for s in rows:
 if not s['n_intersections']:s['eta_peak']=None;s['eta_mean_reference']=None
 if s['assessment'] in ['INDICIO_INSUFICIENCIA_LOCAL','DEMANDA_LOCAL_NAO_SUPERA_CAPACIDADE'] and abs(s['mmax_outside_support']-s['Mrk_eq'])<.02:s['assessment']='PROXIMO_LIMIAR_GRAFICO'
colors={'INDICIO_INSUFICIENCIA_LOCAL':'#c73535','DEMANDA_LOCAL_NAO_SUPERA_CAPACIDADE':'#148065','PENDENTE_CAPACIDADE':'#d68b17','PENDENTE_SOBREPOSICAO_PRANCHAS':'#986624','SEM_DEMANDA_NEGATIVA_INTERSECTADA':'#8091a1','PROXIMO_LIMIAR_GRAFICO':'#b77b12'}
short={'INDICIO_INSUFICIENCIA_LOCAL':'INDÍCIO LOCAL','DEMANDA_LOCAL_NAO_SUPERA_CAPACIDADE':'NÃO SUPERA','PENDENTE_CAPACIDADE':'CAP. PENDENTE','PENDENTE_SOBREPOSICAO_PRANCHAS':'DUPLA PRANCHA','SEM_DEMANDA_NEGATIVA_INTERSECTADA':'SEM INTERSEÇÃO','PROXIMO_LIMIAR_GRAFICO':'LIMIAR GRÁFICO'}
pdfmetrics.registerFont(TTFont('Arial','C:/Windows/Fonts/arial.ttf'));pdfmetrics.registerFont(TTFont('ArialB','C:/Windows/Fonts/arialbd.ttf'))
def fmt(v):return '--' if v is None else f'{v:.2f}'.replace('.',',')
def text(c,x,y,t,size=10,b=False,color='#23394b'):
 c.setFont('ArialB' if b else 'Arial',size);c.setFillColor(HexColor(color));c.drawString(x,y,t)
def fit(c,x,y,t,width,size=9,b=False,color='#23394b'):
 f='ArialB' if b else 'Arial';w=pdfmetrics.stringWidth(t,f,size)
 text(c,x,y,t,min(size,size*width/w) if w else size,b,color)
def wrap(c,x,y,t,width,size=10,leading=15):
 words=t.split();line=''
 for word in words:
  z=(line+' '+word).strip()
  if pdfmetrics.stringWidth(z,'Arial',size)>width and line:text(c,x,y,line,size);y-=leading;line=word
  else:line=z
 if line:text(c,x,y,line,size);y-=leading
 return y
W,H=1190.55,841.89
buf=io.BytesIO();c=canvas.Canvas(buf,pagesize=(W,H))
def header(title,sub='ATP S07 | térreo | flexão negativa horizontal | comparação preliminar'):
 c.setFillColor(HexColor('#153d51'));c.rect(0,H-83,W,83,fill=1,stroke=0);text(c,35,H-35,title,23,True,'#ffffff');text(c,35,H-61,sub,11,False,'#ffffff')
def footer():text(c,35,21,'19/10/2026 | Fonte: TQS/DXF + capacidades Concretopy arquivadas | sem aprovação global das lajes',9)
header('Solicitação × resistência das faixas negativas')
y=H-115
y=wrap(c,35,y,'Resultado: há indícios de insuficiência nominal à flexão nas faixas mapeadas. A conclusão é preliminar, condicionada à conferência das faixas reais, materiais/etapas e ancoragens. Regiões sem capacidade publicada ou com dupla representação não foram aprovadas nem reprovadas.',W-70,13,19)
y-=20
counts=collections.Counter(s['assessment'] for s in rows)
for label,key in [('Demanda local acima da capacidade nominal','INDICIO_INSUFICIENCIA_LOCAL'),('Demanda local não supera a capacidade nominal','DEMANDA_LOCAL_NAO_SUPERA_CAPACIDADE'),('Capacidade composta pendente','PENDENTE_CAPACIDADE'),('Sobreposição entre as duas pranchas','PENDENTE_SOBREPOSICAO_PRANCHAS'),('Próximo do limite da precisão gráfica','PROXIMO_LIMIAR_GRAFICO'),('Sem interseção de demanda negativa extraída','SEM_DEMANDA_NEGATIVA_INTERSECTADA')]:
 c.setFillColor(HexColor(colors[key]));c.rect(35,y-3,14,14,fill=1,stroke=0);text(c,60,y,label,12);text(c,550,y,str(counts[key]),13,True);y-=28
y-=10
y=wrap(c,35,y,f"Total: {len(rows)} células resistentes (249 da 7303 e 109 da 7307). Células de partição não equivalem a apoios ou falhas independentes. Também foram identificadas {len(d['gaps'])} manchas com |Mk| ≥ 1,62 fora das capacidades mapeadas e dos apoios retangulares extraídos; são pendências documentais, não ausência de aço comprovada.",W-70,11,16)
y-=15;text(c,35,y,'Exemplos conferidos visualmente no detalhamento original',13,True);y-=28
text(c,35,y,'Faixa / entorno',11,True);text(c,350,y,'Mmed ref.',11,True);text(c,490,y,'Mlocal máx.',11,True);text(c,630,y,'Mrk = MRd/1,4',11,True);text(c,800,y,'η local',11,True);y-=23
for ident,place in [('7303-R034','P701'),('7307-R057','P785'),('7307-R036','PC40C'),('7303-R150','P740 / P746')]:
 s=next(s for s in rows if s['id']==ident);text(c,35,y,ident+' | '+place,11);text(c,350,y,fmt(s['Mmean_reference_max']),11);text(c,490,y,fmt(s['mmax_outside_support']),11);text(c,630,y,fmt(s['Mrk_eq']),11);text(c,800,y,fmt(s['eta_peak']),11,True,'#b82d2d');y-=24
y-=10;wrap(c,35,y,'Momentos em módulo [tf·m/m]. Mmed ref. é a maior média MN que intercepta a faixa, apenas referência espacial; não é média recalculada da faixa. A decisão local usa o máximo efetivo dentro da célula resistente, fora dos apoios retangulares extraídos. Picos sobre apoios estão preservados no CSV.',W-70,10,15)
footer();c.showPage()
header('Método, rastreabilidade e limites da conclusão')
y=H-115
paragraphs=[
'1. Solicitações: ARP0002.DXF, momentos horizontais característicos, unidade tf·m/m, conforme confirmação de João. Filtro 1,62; isocurva configurada em 1,80 (rótulos 1,81). O filtro não foi tratado como ausência de solicitação. A média MN é a média aritmética dos picos por linha, conforme o mapa anterior.',
'2. Leitura gráfica: amplitudes calibradas em 1.763 rótulos; desvio máximo observado 0,0182 tf·m/m. Trechos sem número foram recuperados pela amplitude, sem atribuição de 1,61. Essa calibração não comprova exatidão do modelo. Comparações a menos de 0,02 tf·m/m do limite foram separadas como limiar gráfico, sem criar tolerância normativa.',
'3. Registro geométrico: 409 vértices de apoios na 7303 e 171 na 7307; resíduos máximos inferiores a 0,12 ponto. Transformações e pares de coordenadas estão arquivados em alinhamento_pdf.json. A validação comprova o alinhamento gráfico dos apoios, não a geometria executiva de todas as armaduras.',
'4. Resistências: resultados anteriores de concretopy.verificar_flexao_viga_retangular, preservados sem novo cálculo. Mrk é resistência equivalente MRd/1,4, não resistência característica da seção. γc = 1,4; γs = 1,15; cobrimento físico adotado 3 cm; direção horizontal na primeira camada. Materiais, espessuras e composições de cada célula foram mantidos.',
'5. Cruzamento local: cada segmento negativo é projetado no eixo de sua linha e cortado pelos polígonos resistentes. Interpola-se linearmente a amplitude entre os extremos do próprio segmento. Registra-se o máximo local. η = |Mk,local| / (MRd/1,4). O gráfico mostra também Mmed da mancha MN para comparação com a imagem solicitada; essa média pode ocultar insuficiência localizada.',
'6. Sobreposições: nenhuma soma das capacidades negativas pendentes de ancoragem foi admitida. Quando as duas pranchas fornecem cobertura espacial coincidente, a célula é marcada como dupla prancha, sem soma, escolha automática da maior capacidade ou conclusão local definitiva.',
'7. Apoios: o máximo usado no índice local exclui apenas os polígonos fechados das camadas 225 e 207 do DXF. O máximo completo é mantido no CSV. Essa exclusão geométrica não resolve encontros com blocos, apoios curvos, vigas ou regiões espessas. Não se redistribuíram picos nem se assumiu largura colaborante.',
'8. Alcance: as capacidades anteriores têm estado de geometria nominal a revisar. Indício local significa demanda gráfica superior à capacidade nominal arquivada, não falta de armadura executiva definitivamente comprovada. A confirmação exige rever a faixa física, seção, etapa de concretagem, armaduras disponíveis/ancoradas e critério de solicitação. Não se fizeram mínimos normativos, ELS, punção, cortante, emendas ou aprovação global.'
]
for t in paragraphs:y=wrap(c,35,y,t,W-70,11,16);y-=16
footer();c.showPage()
# Evidence crops of the four manually checked locations.
header('Pontos críticos conferidos na prancha original')
for k,ident in enumerate(['7303-R034','7307-R057','7307-R036','7303-R150']):
 x=35+(k%2)*570;y=H-120-(k//2)*320
 c.drawImage(str(tmp/('check_'+ident+'.png')),x,y-265,width=530,height=265,preserveAspectRatio=True,anchor='c')
 s=next(s for s in rows if s['id']==ident);text(c,x,y+8,ident+' | '+', '.join(s['marks'])+' | Mlocal '+fmt(s['mmax_outside_support'])+' / Mrk '+fmt(s['Mrk_eq']),11,True)
footer();c.showPage()
# Exhaustive regional table, preserving every original R identifier.
for start in range(0,len(rows),42):
 header('Quadro por faixa resistente - '+str(start+1)+' a '+str(min(start+42,len(rows))))
 y=H-110;xs=[35,137,245,335,421,503,570,710,890]
 titles=['Faixa','Posições','As/m','Mmed ref.','Mlocal','Mrk','η local','Estado','MN associadas (resumo)']
 for x,t in zip(xs,titles):text(c,x,y,t,10,True)
 y-=22
 for j,s in enumerate(rows[start:start+42]):
  if j%2==0:c.setFillColor(HexColor('#f0f4f6'));c.rect(30,y-4,W-60,14,fill=1,stroke=0)
  vals=[s['id'],','.join(s['marks']),fmt(s['As_cm2_m']) if not s['issues'] else '--',fmt(s['Mmean_reference_max']) if s['n_intersections'] else '--',fmt(s['mmax_outside_support']) if s['n_intersections'] else '--',fmt(s['Mrk_eq']),fmt(s['eta_peak']),short[s['assessment']],','.join(z.replace('MN','') for z in s['mn_ids'])]
  widths=[98,104,85,82,78,63,135,174,250]
  for x,t,w in zip(xs,vals,widths):fit(c,x,y,t,w,8.8,color=colors[s['assessment']] if x==710 else '#23394b')
  y-=15.1
 text(c,35,54,'As/m [cm²/m]; momentos em módulo [tf·m/m]. Mlocal: máximo fora dos apoios retangulares extraídos. --: pendente ou sem leitura.',9)
 footer();c.showPage()
for start in range(0,len(d['gaps']),40):
 header('Pendências de cobertura - sem resistência mapeada')
 y=H-112;xs=[35,105,240,370,600]
 for x,t in zip(xs,['ID','|Mk| máximo','DXF X','DXF Y','MN associadas']):text(c,x,y,t,11,True)
 y-=25
 for g in d['gaps'][start:start+40]:
  vals=[g['id'],fmt(g['peak']),fmt(g['point'][0]),fmt(g['point'][1]),', '.join(g['mn_ids'])]
  for x,t in zip(xs,vals):fit(c,x,y,t,240,10)
  y-=15
 wrap(c,35,80,'Essas manchas indicam ausência de capacidade na base mapeada pelo assistente. Não comprovam ausência física de armadura nas pranchas. Conferir chamadas ainda não conciliadas, limites de faixa e seção antes de apontar falta ao projetista.',W-70,10,15)
 footer();c.showPage()
c.save();report=fitz.open(stream=buf.getvalue(),filetype='pdf')
# Original vector plans with capacity-region status overlays and full comparison panel.
for n in ['7303','7307']:
 entry=next(e for e in inv if e['sheet']==n);src=fitz.open(entry['path']);sp=src[0];sw,sh=sp.rect.width,sp.rect.height;pw=1400 if n=='7303' else 1100;WW,HH=sw+pw,sh+75
 mapdoc=fitz.open();page=mapdoc.new_page(width=WW,height=HH);page.show_pdf_page(fitz.Rect(0,75,sw,sh+75),src,0)
 ob=io.BytesIO();cc=canvas.Canvas(ob,pagesize=(WW,HH));text(cc,30,HH-28,'ATP S07 | '+n+' | solicitações características × resistências equivalentes',23,True);text(cc,30,HH-53,'Vermelho: indício local | verde: não supera no cruzamento | amarelo: pendente | roxo: cobertura não mapeada | cinza: sem interseção',12)
 def drawpoly(pg,col,alpha):
  def rings(p):return [p.exterior]+list(p.interiors)
  def pp(p):
   path=cc.beginPath()
   for ring in rings(p):
    pts=list(ring.coords);path.moveTo(pts[0][0],HH-75-pts[0][1])
    for x,y in pts[1:]:path.lineTo(x,HH-75-y)
    path.close()
   cc.setFillColor(Color(*[v/255 for v in bytes.fromhex(col[1:])],alpha=alpha));cc.setStrokeColor(HexColor(col));cc.setLineWidth(.35);cc.drawPath(path,fill=1,stroke=1,fillMode=0)
  if pg.geom_type=='Polygon':pp(pg)
  elif hasattr(pg,'geoms'):
   for p in pg.geoms:
    if p.geom_type=='Polygon':pp(p)
 rs=[s for s in rows if s['sheet']==n];occupied=[];placements=[]
 for s in rs:drawpoly(shape(caplookup[s['id']]['geometry']),colors[s['assessment']],.17)
 f=d['alignment'][n]
 for g in d['gaps']:
  pg=affine_transform(shape(g['geometry']),[f['sx'],0,0,f['sy'],f['tx'],f['ty']]);clip=pg.intersection(__import__('shapely').geometry.box(150,350,2150,sh-90))
  if not clip.is_empty:drawpoly(clip,'#842ca0',.23)
 # Collision-free R codes with leaders; values are in the right-hand panel.
 for s in sorted(rs,key=lambda z:shape(caplookup[z['id']]['geometry']).area):
  pg=shape(caplookup[s['id']]['geometry']);a=pg.representative_point();cx,cy=a.x,a.y;bw,bh=26,11;rect=None
  for rad in [0,10,18,28,42,60,85,115,155,205]:
   for ang in ([0] if rad==0 else range(0,360,30)):
    x=cx+rad*math.cos(math.radians(ang));y=cy+rad*math.sin(math.radians(ang));bb=(x-bw/2,y-bh/2,x+bw/2,y+bh/2)
    if bb[0]>80 and bb[2]<2200 and bb[1]>90 and bb[3]<sh-60 and not any(bb[0]<q[2]+1 and bb[2]>q[0]-1 and bb[1]<q[3]+1 and bb[3]>q[1]-1 for q in occupied):rect=bb;break
   if rect:break
  if rect is None:raise RuntimeError(s['id'])
  occupied.append(rect);x0,y0,x1,y1=rect;col=colors[s['assessment']]
  if rad:cc.setStrokeColor(HexColor(col));cc.setLineWidth(.4);cc.line(cx,HH-75-cy,min(max(cx,x0),x1),HH-75-min(max(cy,y0),y1))
  cc.setFillColor(white);cc.setStrokeColor(HexColor(col));cc.roundRect(x0,HH-75-y1,bw,bh,1,fill=1,stroke=1);text(cc,x0+2,HH-75-y0-8,s['id'].split('-')[1],6.6,True,col)
  if s['assessment']=='INDICIO_INSUFICIENCIA_LOCAL':
   x,y=s['peak_outside_point'];x=x*f['sx']+f['tx'];y=y*f['sy']+f['ty'];cc.setStrokeColor(HexColor('#bf0000'));cc.setLineWidth(.7);cc.circle(x,HH-75-y,3,fill=0,stroke=1)
 panelx=sw+15;cols=4 if n=='7303' else 3;cw=(pw-30)/cols;rr=math.ceil(len(rs)/cols);rh=(sh-160)/rr
 text(cc,panelx,HH-105,'Momentos em módulo [tf·m/m] | Mrk = MRd/1,4 | η = Mlocal/Mrk',12,True)
 text(cc,panelx,HH-125,'Mmed: maior média MN associada (referência); Mlocal: pico dentro da faixa, fora dos apoios extraídos.',10)
 text(cc,panelx,HH-142,'As/m [cm²/m]. Sem soma resistente para negativas pendentes. Círculo vermelho: ponto de Mlocal.',10)
 for i,s in enumerate(rs):
  col=i//rr;row=i%rr;x=panelx+col*cw;y=HH-177-row*rh
  if row%2==0:cc.setFillColor(HexColor('#f1f4f6'));cc.rect(x-3,y-rh+11,cw-7,rh,fill=1,stroke=0)
  texts=[s['id']+' | '+short[s['assessment']], 'Mmed '+(fmt(s['Mmean_reference_max']) if s['n_intersections'] else '--')+' | Mlocal '+(fmt(s['mmax_outside_support']) if s['n_intersections'] else '--')+' | Mrk '+fmt(s['Mrk_eq']), 'As/m '+(fmt(s['As_cm2_m']) if not s['issues'] else '--')+' | η '+fmt(s['eta_peak'])+' | '+','.join(s['marks']), 'MN '+','.join(v.replace('MN','') for v in s['mn_ids'])]
  for j,t in enumerate(texts):fit(cc,x,y-j*7.4,t,cw-12,7.4,j==0,colors[s['assessment']] if j==0 else '#23394b')
 cc.showPage();cc.save();ov=fitz.open(stream=ob.getvalue(),filetype='pdf');page.show_pdf_page(page.rect,ov,0)
 report.insert_pdf(mapdoc,start_at=3+(0 if n=='7303' else 1))
 # Inspect all maps at readable resolution and export convenience images.
 page.get_pixmap(matrix=fitz.Matrix(.42,.42)).save(str(tmp/('comparativo_'+n+'_geral.png')))
 page.get_pixmap(matrix=fitz.Matrix(1.2,1.2),clip=fitz.Rect(sw+10,150,sw+700,650)).save(str(tmp/('comparativo_'+n+'_legenda.png')))
 page.get_pixmap(matrix=fitz.Matrix(.9,.9)).save(str(r/('ATP_S07_'+n+'_comparativo_momentos.png')))
report.set_metadata(dict(title='ATP S07 - comparação preliminar de momentos negativos e resistências - 7303 / 7307',author='Auxiliar de engenharia de João',subject='Solicitações características TQS e resistências equivalentes Concretopy arquivadas; sem aprovação global.'))
file=dest/'ATP_S07_comparativo_momentos_resistencias_7303_7307.pdf';report.save(file,deflate=True,garbage=4);report.close()
with (r/'comparacao_faixas_resistentes.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f,delimiter=';');w.writerow(['faixa','prancha','posicoes','MN','As_cm2_m','Mmed_MN_ref_tfm_m','Mmax_fora_apoios_tfm_m','Mmax_incl_apoios_tfm_m','Mrk_MRd_div_1_4','eta_local','estado','DXF_X_pico','DXF_Y_pico'])
 for s in rows:w.writerow([s['id'],s['sheet'],','.join(s['marks']),','.join(s['mn_ids']),s['As_cm2_m'] if not s['issues'] else None,s['Mmean_reference_max'],s['mmax_outside_support'],s['mmax'],s['Mrk_eq'],s['eta_peak'],s['assessment'],*(s['peak_outside_point'] or [None,None])])
qa=fitz.open(file);missing=[]
for s in rows:
 if not any(s['id'] in p.get_text() for p in qa):missing.append(s['id'])
assert not missing
for i,p in enumerate(qa):
 if i not in [3,4]:p.get_pixmap(matrix=fitz.Matrix(.75,.75)).save(str(tmp/f'comparativo_p{i+1:02d}.png'))
summary=dict(collections.Counter(s['assessment'] for s in rows));(r/'comparacao_validacao.json').write_text(json.dumps(dict(pages=len(qa),all_region_codes_present=True,capacity_source_unchanged=True,summary=summary),indent=2),encoding='utf8');print('PDF',file,'PAGES',len(qa),'SUMMARY',summary)
