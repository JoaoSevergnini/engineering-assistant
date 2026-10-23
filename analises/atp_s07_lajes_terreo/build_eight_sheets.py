from pathlib import Path
import json,math,hashlib,collections,colorsys
from io import BytesIO
import fitz
from shapely.geometry import shape,box,Point
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color,white,HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image,ImageDraw
root=Path(r'P:\Joao Severgnini\Simon\engineering-assistant\analises\atp_s07_lajes_terreo');dest=root/'output/pdf/pranchas_regioes';dest.mkdir(parents=True,exist_ok=True)
rs=json.loads((root/'regioes_capacidades.json').read_text(encoding='utf8'));occ=json.loads((root/'ocorrencias_extraidas.json').read_text(encoding='utf8'));inv=json.loads((root/'inventario.json').read_text(encoding='utf8'));rhash=hashlib.sha256((root/'regioes_capacidades.json').read_bytes()).hexdigest()
pdfmetrics.registerFont(TTFont('Arial',r'C:\Windows\Fonts\arial.ttf'));pdfmetrics.registerFont(TTFont('ArialB',r'C:\Windows\Fonts\arialbd.ttf'))
NAVY=HexColor('#143A50');ORANGE=HexColor('#A55B00');GREY=HexColor('#45515C')
def num(v):return '--' if v is None else f'{v:.2f}'.replace('.',',')
def arm(f):return 'Ø'+f'{f[0]:g}'.replace('.',',')+' c/'+f'{f[1]:g}'.replace('.',',')
def texts(r):
 ff=[tuple(f) for f in r['families']];base=(8.,14.) in ff and r['face']=='POS' and r['base_lap_count']>0
 b='Ø8 c/14' if base else '--';removed=False;other=[]
 for f in ff:
  if base and f==(8.,14.) and not removed:removed=True;continue
  other.append(arm(f))
 reforco=(' ; ' if r['issues'] else ' + ').join(other) or '--'
 if r['face']=='NEG':ref_label='Negativa: '
 elif not base:ref_label='Arm./ref.: '
 else:ref_label='Reforço: '
 val=None if r['issues'] else r['result']['M_equivalent_tfm_m'];As=None if r['issues'] or val is None else r['result']['As_cm2_m'];star='*' if r['offset_source'].startswith('HYPOTHESIS') and val is not None else ''
 return ['Base: '+b,ref_label+reforco,'As/m: '+num(As)+' | Mrk: '+num(val)+star]
def color(r):
 if r['issues']:return ORANGE
 signature=str(sorted(r['families'])).encode();v=int(hashlib.sha256(signature).hexdigest()[:4],16)/65535
 rgb=colorsys.hsv_to_rgb(.55+.20*v,.62,.69 if r['face']=='POS' else .60);return Color(*rgb)
def drawpoly(c,g,transform,fill,alpha=.10):
 polys=[g] if g.geom_type=='Polygon' else [z for z in getattr(g,'geoms',[]) if z.geom_type=='Polygon']
 c.setFillColor(Color(fill.red,fill.green,fill.blue,alpha=alpha));c.setStrokeColor(Color(fill.red,fill.green,fill.blue,alpha=.75));c.setLineWidth(.6)
 for poly in polys:
  p=c.beginPath()
  for ring in [poly.exterior,*poly.interiors]:
   coords=list(ring.coords);xx,yy=transform(*coords[0]);p.moveTo(xx,yy)
   for x,y in coords[1:]:xx,yy=transform(x,y);p.lineTo(xx,yy)
   p.close()
  c.drawPath(p,fill=1,stroke=1,fillMode=0)
def fittext(c,t,x,y,maxw,size=7,font='Arial',col=NAVY):
 while pdfmetrics.stringWidth(t,font,size)>maxw and size>5.8:size-=.2
 if pdfmetrics.stringWidth(t,font,size)>maxw:
  while t and pdfmetrics.stringWidth(t+'...',font,size)>maxw:t=t[:-1]
  t+='...'
 c.setFont(font,size);c.setFillColor(col);c.drawString(x,y,t)
outputs=[];qa=[]
for e in inv[2:]:
 n=e['sheet'];source=Path(e['path']);digest=hashlib.sha256(source.read_bytes()).hexdigest()
 if digest!=e['sha256']:raise RuntimeError('Fonte mudou: '+n)
 src=fitz.open(source);original=src[0];sw,sh=original.rect.width,original.rect.height;regions=[r for r in rs if r['sheet']==n]
 pending=[o for o in occ if o['sheet']==n and o.get('spacing_cm') is not None and not o.get('region_pdf')]
 # Explicitly include the N91 call with missing spacing, already noted in the previous report.
 pending += [o for o in occ if o['sheet']==n and n=='7301' and o['mark']=='N91' and o.get('spacing_cm') is None]
 entries=[('R',r) for r in regions]+[('P',o) for o in pending];rowh=33.;top=158.;bottom=36.;rows=math.floor((sh-top-bottom)/rowh);cols=max(1,math.ceil(len(entries)/rows));cw=270.;pw=cols*cw+40;W=sw+pw;H=sh
 target=fitz.open();page=target.new_page(width=W,height=H);page.show_pdf_page(fitz.Rect(0,0,sw,sh),src,0)
 buf=BytesIO();c=canvas.Canvas(buf,pagesize=(W,H));c.setFillColor(Color(1,1,1,alpha=.27));c.rect(0,0,sw,sh,fill=1,stroke=0)
 # Regional polygons are unchanged from the last report.
 for r in regions:drawpoly(c,shape(r['geometry']),lambda x,y:(x,H-y),color(r))
 # Side legend - every region has an entry with complete adopted configuration and values.
 c.setFillColor(HexColor('#F5F8FA'));c.rect(sw,0,pw,H,fill=1,stroke=0);c.setStrokeColor(NAVY);c.setLineWidth(1);c.line(sw,0,sw,H)
 c.setFillColor(NAVY);c.rect(sw,H-42,pw,42,fill=1,stroke=0);c.setFillColor(white);c.setFont('ArialB',15);c.drawString(sw+18,H-27,'ATP S07 | '+n+' | REGIÕES E ARMADURAS')
 notes=[
 'As/m em cm²/m | Mrk em tf·m/m = |MRd|/1,4 (resistência equivalente, não resistência característica).',
 'h e d em cm; concreto C35/C40 conforme a região do relatório anterior. Valores resistentes em módulo.',
 'Base, reforço e regiões reapresentados sem novo cálculo. Negativas sem base contínua: Base --.',
 'Base -- também indica base não individualizada no relatório; não significa ausência física de armadura.',
 'Pendências / sobreposições com soma não verificada: As/m -- e Mrk --. Armaduras não são somadas nesses casos.',
 '* Posição vertical provisória: envelope horizontal de 20 mm. Demais hipóteses e limites do relatório permanecem.',
 'Rxxx corresponde ao mesmo código do relatório. Pxx marca chamada cuja faixa não foi fechada; sem polígono inventado.',
 'Regiões pequenas: código no desenho e configuração completa nesta legenda. Campos não calculados: --.',
 'Cópia de trabalho - capacidade nominal de seção; não verifica esforços, ancoragem, emendas, ELS ou aprovação da laje.'
 ]
 y=H-56
 for note in notes:fittext(c,note,sw+18,y,pw-36,7.2);y-=9.2
 entry_targets={};legend_boxes=[]
 for j,(kind,item) in enumerate(entries):
  col=j//rows;row=j%rows;x=sw+18+col*cw;y=H-top-row*rowh;eid=item['id'].split('-')[1] if kind=='R' else 'P'+str(j-len(regions)+1).zfill(2);entry_targets[eid]=(x,H-y)
  if row%2==0:c.setFillColor(white);c.rect(x-4,y-29,cw-8,rowh,fill=1,stroke=0)
  if kind=='R':
   r=item;txt=texts(r);value=txt[2].replace('As/m: ','As/m ').replace('Mrk: ','Mrk ');colr=color(r)
   line0=eid+' | '+value
   line1=txt[0];line2=txt[1]
   meta=f"h={r['h_cm']} | C{r['fck_MPa']} | "+','.join(r['marks'])
   if r['issues']:meta='Soma pendente | '+','.join(r['marks'])
  else:
   o=item;colr=ORANGE;line0=eid+' | As/m -- | Mrk --';line1='Base: --';line2='Armadura: Ø'+f"{o['diameter_mm']:g}".replace('.',',')+(' c/'+f"{o['spacing_cm']:g}".replace('.',',') if o.get('spacing_cm') else '; espaçamento --');meta='Faixa pendente | '+o['id']+' | '+o['mark']
  for yy,t,size,font in [(y,line0,8,'ArialB'),(y-8,line1,7.1,'Arial'),(y-16,line2,7.1,'Arial'),(y-24,meta,6.3,'Arial')]:fittext(c,t,x,yy,cw-18,size,font,colr if yy==y else NAVY)
  legend_boxes.append(dict(code=eid,x=x,y_pdf=H-y,row=row,col=col))
 c.setFont('Arial',7);c.setFillColor(NAVY);c.drawString(sw+18,18,'19/10/2026 | ATP S07 | mesmas regiões e resultados do relatório preliminar | Concretopy')
 # Place complete labels across region boundaries, using leaders when displaced.
 occupied=[];placements=[]
 def collides(b):return any(b[0]<q[2]+1.8 and b[2]>q[0]-1.8 and b[1]<q[3]+1.8 and b[3]>q[1]-1.8 for q in occupied)
 plan_bounds=(150,330,2110,sh-140) if int(n)<7305 else (170,340,2110,1600)
 for r in sorted(regions,key=lambda z:shape(z['geometry']).area):
  geom=shape(r['geometry']);eid=r['id'].split('-')[1];rp=geom.representative_point();center=(rp.x,rp.y);ct=color(r);detail=texts(r);full=[eid+' | '+detail[2],detail[0],detail[1]];font=6.1;leading=7.1
  bw=max(pdfmetrics.stringWidth(t,'ArialB' if i==0 else 'Arial',font) for i,t in enumerate(full))+7;bh=25
  cx,cy=center;fullrect=(cx-bw/2,cy-bh/2,cx+bw/2,cy+bh/2)
  compact=False;rect=None;leader=False
  # Complete labels may cross region boundaries; keep labels mutually disjoint.
  lines=full
  for radius in [0,16,28,42,60,82,108,138,174,216,264,320]:
   for angle in ([0] if radius==0 else range(0,360,20)):
    px=cx+radius*math.cos(math.radians(angle));py=cy+radius*math.sin(math.radians(angle));bb=(px-bw/2,py-bh/2,px+bw/2,py+bh/2)
    if bb[0]>80 and bb[2]<sw-30 and bb[1]>80 and bb[3]<sh-70 and not collides(bb):
     rect=bb;leader=radius>0;break
   if rect is not None:break
  if rect is None:raise RuntimeError('Sem espaço para rótulo completo '+r['id'])
  occupied.append(rect);x0,y0,x1,y1=rect
  if leader:
   ex=min(max(cx,x0),x1);ey=min(max(cy,y0),y1);c.setStrokeColor(ct);c.setLineWidth(.35);c.line(cx,H-cy,ex,H-ey);c.setFillColor(ct);c.circle(cx,H-cy,.8,fill=1,stroke=0)
  c.setFillColor(Color(1,1,1,alpha=.94));c.setStrokeColor(ct);c.setLineWidth(.35);c.roundRect(x0,H-y1,x1-x0,y1-y0,1.1,fill=1,stroke=1)
  for i,t in enumerate(lines):c.setFont('ArialB' if i==0 else 'Arial',font);c.setFillColor(ct if i==0 else NAVY);c.drawCentredString((x0+x1)/2,H-y0-6.5-i*leading,t)
  placements.append(dict(id=r['id'],code=eid,rect=list(rect),anchor=list(center),full=not compact,leader=leader))
 for j,o in enumerate(pending,1):
  a,b,cc,d=o['label_rect'];cx=(a+cc)/2;cy=(b+d)/2;eid='P'+str(j).zfill(2);c.setStrokeColor(ORANGE);c.setFillColor(ORANGE);c.setLineWidth(.8);c.circle(cx,H-cy,6,fill=0,stroke=1)
  bw=pdfmetrics.stringWidth(eid,'ArialB',6)+5;bh=10;rect=None
  for rad in [12,20,32,50,75]:
   for ang in range(0,360,30):
    px=cx+rad*math.cos(math.radians(ang));py=cy+rad*math.sin(math.radians(ang));bb=(px-bw/2,py-bh/2,px+bw/2,py+bh/2)
    if not collides(bb):rect=bb;break
   if rect:break
  if rect is None:raise RuntimeError('Sem espaço para pendência '+o['id'])
  occupied.append(rect);x0,y0,x1,y1=rect;c.line(cx,H-cy,(x0+x1)/2,H-(y0+y1)/2);c.setFillColor(white);c.rect(x0,H-y1,bw,bh,fill=1,stroke=0);c.setFillColor(ORANGE);c.setFont('ArialB',6);c.drawCentredString((x0+x1)/2,H-y0-7,eid)
  placements.append(dict(id=o['id'],code=eid,rect=list(rect),anchor=[cx,cy],pending=True))
 c.showPage();c.save();overlay=fitz.open(stream=buf.getvalue(),filetype='pdf');page.show_pdf_page(page.rect,overlay,0)
 # Links from each plan code to its legend entry.
 for pl in placements:
  x,y=entry_targets[pl['code']];page.insert_link(dict(kind=fitz.LINK_GOTO,from_=fitz.Rect(pl['rect']),page=0,to=fitz.Point(x,y),zoom=2)) if False else None
 # PyMuPDF link schema uses the literal key `from`.
 for pl in placements:
  x,y=entry_targets[pl['code']];page.insert_link({'kind':fitz.LINK_GOTO,'from':fitz.Rect(pl['rect']),'page':0,'to':fitz.Point(x,y),'zoom':2})
 target.set_metadata(dict(title=f'ATP S07 - {n} - regiões, armaduras, As/m e Mrk',author='Auxiliar de engenharia - revisão de João',subject='Reapresentação das regiões nominais do relatório preliminar. Mrk=MRd/1,4.'))
 file=dest/f'ATP_S07_{n}_regioes_As_Mrk.pdf';target.save(file,garbage=4,deflate=True);target.close()
 # All-region extraction check and visual render.
 check=fitz.open(file);text=check[0].get_text();missing=[pl['code'] for pl in placements if pl['code'] not in text]
 if missing:raise RuntimeError('Rótulos ausentes '+str(missing))
 check[0].get_pixmap(matrix=fitz.Matrix(.35,.35)).save(str(dest/f'QA_{n}_geral.png'))
 check[0].get_pixmap(matrix=fitz.Matrix(1,1),clip=fitz.Rect(sw,0,min(W,sw+600),650)).save(str(dest/f'QA_{n}_legenda.png'))
 # Crop a populated piece of the plan at true native resolution.
 clip=fitz.Rect(250,600,1050,1200) if int(n)<7305 else fitz.Rect(220,380,1020,980)
 check[0].get_pixmap(matrix=fitz.Matrix(1.4,1.4),clip=clip).save(str(dest/f'QA_{n}_regioes.png'))
 qa.append(dict(sheet=n,path=str(file),source_sha256=digest,width=W,height=H,pages=len(check),regions=len(regions),pending_calls=len(pending),full_in_region_labels=sum(pl.get('full',False) for pl in placements),compact_labels=sum(not pl.get('full',False) for pl in placements),all_codes_in_pdf=not missing,placements=placements,legend_entries=legend_boxes))
 outputs.append(str(file));print(n,len(regions),'full labels',sum(pl.get('full',False) for pl in placements),'panel columns',cols,'MB',round(file.stat().st_size/1e6,2),flush=True)
(root/'pranchas_regioes_manifesto.json').write_text(json.dumps(dict(region_source_sha256=rhash,region_data_changed=False,outputs=outputs,qa=qa),indent=2,ensure_ascii=False),encoding='utf8')
print('DONE',len(outputs))
