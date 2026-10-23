from pathlib import Path
import json,math,collections,hashlib,csv,io
from shapely.geometry import shape,Point,LineString
from shapely.affinity import affine_transform
from shapely.strtree import STRtree
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor,Color,white
import fitz
from PIL import Image,ImageDraw
r=Path(__file__).parent;root=r.parent;tmp=root/'tmp/pdfs';dest=root/'output/pdf/pranchas_regioes'
source=root/'regioes_capacidades.json';sha=hashlib.sha256(source.read_bytes()).hexdigest();allcaps=json.loads(source.read_text(encoding='utf8'))
caps=[s for s in allcaps if s['sheet'] in ['7304','7308'] and not s['issues'] and s['result'].get('M_equivalent_tfm_m') is not None]
fits=json.loads((r/'alinhamento_pdf.json').read_text());scale=json.loads((r/'calibracao_amplitude.json').read_text())['scale'];inv=json.loads((root/'inventario.json').read_text(encoding='utf8'))
polys=[]
for s in caps:
 f=fits[s['sheet']];actual=affine_transform(shape(s['geometry']),[1/f['sx'],0,0,1/f['sy'],-f['tx']/f['sx'],-f['ty']/f['sy']]);polys.append(affine_transform(actual,[0,1,-1,0,0,0]))
tree=STRtree(polys);peaks=[{} for s in caps]
def lines(g):
 if g.is_empty:return []
 if g.geom_type=='LineString':return [g]
 return [z for q in g.geoms for z in lines(q)] if hasattr(g,'geoms') else []
for c in json.loads((r/'componentes_negativos.json').read_text()):
 base=c['base']
 for a,b,l in c['segments']:
  if abs(a[0]-b[0])<1e-6:continue
  ma=max(0,(a[1]-base)/scale);mb=max(0,(b[1]-base)/scale)
  if max(ma,mb)<=.0002:continue
  line=LineString([(a[0],base),(b[0],base)])
  for ii in tree.query(line,predicate='intersects'):
   i=int(ii)
   for seg in lines(line.intersection(polys[i])):
    if seg.length<.01:continue
    peak=max(ma+(mb-ma)*(x-a[0])/(b[0]-a[0]) for x,y in seg.coords)
    peaks[i][base]=max(peaks[i].get(base,0),peak)
records=[]
for s,pp in zip(caps,peaks):
 mr=s['result']['M_equivalent_tfm_m'];ms=sum(pp.values())/len(pp) if pp else None
 rec=dict(id=s['id'],sheet=s['sheet'],marks=s['marks'],families=s['families'],As_cm2_m=s['result']['As_cm2_m'],Mrk_eq_tfm_m=mr,Msol_mean_tfm_m=ms,n_lines=len(pp),line_peaks=[dict(x_DXF=-k,Mk_negative_tfm_m=-v) for k,v in sorted(pp.items())],eta=ms/mr if ms is not None else None)
 rec['offset_source']=s['offset_source'];rec['hypothesis']=s['offset_source'].startswith('HYPOTHESIS');rec['horizontal_offset_cm']=s['horizontal_offset_cm']
 rec['status']='SEM_DEMANDA_ASSOCIADA' if ms is None else 'MEDIA_SUPERA_RESISTENCIA' if ms>mr else 'MEDIA_NAO_SUPERA_RESISTENCIA'
 records.append(rec)
lookup={s['id']:s for s in caps}
pdfmetrics.registerFont(TTFont('Arial','C:/Windows/Fonts/arial.ttf'));pdfmetrics.registerFont(TTFont('ArialB','C:/Windows/Fonts/arialbd.ttf'))
C={'MEDIA_SUPERA_RESISTENCIA':'#be3232','MEDIA_NAO_SUPERA_RESISTENCIA':'#13745f','SEM_DEMANDA_ASSOCIADA':'#687785'}
def num(v):return '--' if v is None else f'{v:.2f}'.replace('.',',')
def mrlabel(s):return num(s['Mrk_eq_tfm_m'])+('*' if s['hypothesis'] else '')
def arm(s):return ' + '.join('Ø'+f'{a:g}'.replace('.',',')+' c/'+f'{b:g}'.replace('.',',') for a,b in s['families'])
def txt(c,x,y,t,size=9,b=False,col='#17384b'):
 c.setFont('ArialB' if b else 'Arial',size);c.setFillColor(HexColor(col));c.drawString(x,y,t)
def fit(c,x,y,t,w,size=8,b=False,col='#17384b'):
 width=pdfmetrics.stringWidth(t,'ArialB' if b else 'Arial',size);txt(c,x,y,t,min(size,size*w/width) if width else size,b,col)
qa=[]
for n in ['7304','7308']:
 rs=[s for s in records if s['sheet']==n];entry=next(e for e in inv if e['sheet']==n);src=fitz.open(entry['path']);sp=src[0];sw,sh=sp.rect.width,sp.rect.height;top=85;pw=1050 if n=='7304' else 780;W,H=sw+pw,sh+top
 target=fitz.open();page=target.new_page(width=W,height=H);page.show_pdf_page(fitz.Rect(0,top,sw,sh+top),src,0)
 buf=io.BytesIO();c=canvas.Canvas(buf,pagesize=(W,H))
 txt(c,30,H-28,'ATP S07 | '+n+' | armadura negativa vertical: resistência × solicitação média',23,True)
 txt(c,30,H-51,'Msol = média aritmética dos picos negativos por linha, recortados na faixa R | Mrk = MRd/1,4 | módulos em tf·m/m',12)
 txt(c,30,H-70,'Vermelho: média supera resistência | verde: média não supera | cinza: sem demanda associada | somente faixas com resistência publicada',11)
 # Tone original strokes gently; full labels may cross region boundaries.
 c.setFillColor(Color(1,1,1,alpha=.14));c.rect(0,0,sw,sh,fill=1,stroke=0)
 def drawpoly(pg,col):
  ps=[pg] if pg.geom_type=='Polygon' else [z for z in pg.geoms if z.geom_type=='Polygon']
  for p in ps:
   path=c.beginPath()
   for ring in [p.exterior,*p.interiors]:
    pts=list(ring.coords);path.moveTo(pts[0][0],H-top-pts[0][1])
    for x,y in pts[1:]:path.lineTo(x,H-top-y)
    path.close()
   rgb=bytes.fromhex(col[1:]);c.setFillColor(Color(*[x/255 for x in rgb],alpha=.16));c.setStrokeColor(HexColor(col));c.setLineWidth(.5);c.drawPath(path,fill=1,stroke=1,fillMode=0)
 for s in rs:drawpoly(shape(lookup[s['id']]['geometry']),C[s['status']])
 occupied=[];placements=[]
 def collision(b):return any(b[0]<q[2]+2 and b[2]>q[0]-2 and b[1]<q[3]+2 and b[3]>q[1]-2 for q in occupied)
 for s in sorted(rs,key=lambda z:shape(lookup[z['id']]['geometry']).area):
  pg=shape(lookup[s['id']]['geometry']);a=pg.representative_point();cx,cy=a.x,a.y;code=s['id'].split('-')[1];col=C[s['status']]
  label=[code+' | Mrk '+mrlabel(s)+' | Msol '+num(s['Msol_mean_tfm_m']),arm(s)+' | As/m '+num(s['As_cm2_m']), 'n='+str(s['n_lines'])+' linhas | η '+num(s['eta'])]
  fs=6.4;lead=7.7;bw=max(pdfmetrics.stringWidth(t,'ArialB' if j==0 else 'Arial',fs) for j,t in enumerate(label))+8;bh=28;rect=None
  for radius in [0,18,30,46,65,90,120,155,195,245,305,375]:
   for angle in ([0] if radius==0 else range(0,360,20)):
    px=cx+radius*math.cos(math.radians(angle));py=cy+radius*math.sin(math.radians(angle));bb=(px-bw/2,py-bh/2,px+bw/2,py+bh/2)
    if bb[0]>65 and bb[2]<2200 and bb[1]>90 and bb[3]<sh-70 and not collision(bb):rect=bb;break
   if rect:break
  if rect is None:raise RuntimeError('Espaço '+s['id'])
  occupied.append(rect);x0,y0,x1,y1=rect
  if radius:
   c.setStrokeColor(HexColor(col));c.setLineWidth(.45);c.line(cx,H-top-cy,min(max(cx,x0),x1),H-top-min(max(cy,y0),y1));c.setFillColor(HexColor(col));c.circle(cx,H-top-cy,.8,fill=1,stroke=0)
  c.setFillColor(Color(1,1,1,alpha=.97));c.setStrokeColor(HexColor(col));c.roundRect(x0,H-top-y1,bw,bh,1.2,fill=1,stroke=1)
  for j,t in enumerate(label):
   c.setFont('ArialB' if j==0 else 'Arial',fs);c.setFillColor(HexColor(col if j==0 else '#17384b'));c.drawCentredString((x0+x1)/2,H-top-y0-7.1-j*lead,t)
  placements.append(dict(id=s['id'],rect=list(rect),anchor=[cx,cy]))
 cols=3 if n=='7304' else 2;rr=math.ceil(len(rs)/cols);cw=(pw-35)/cols;rh=(sh-320)/rr;px=sw+18
 counts=collections.Counter(s['status'] for s in rs)
 txt(c,px,H-118,'COMPARAÇÃO POR FAIXA OFICIAL DE ARMADURA',14,True)
 txt(c,px,H-143,str(len(rs))+' faixas | média supera: '+str(counts['MEDIA_SUPERA_RESISTENCIA'])+' | não supera: '+str(counts['MEDIA_NAO_SUPERA_RESISTENCIA'])+' | sem demanda: '+str(counts['SEM_DEMANDA_ASSOCIADA']),10)
 notes=['Média calculada com um pico por linha vertical dentro da faixa R, sem ponderação por comprimento ou área.','As manchas MNV são apenas auxiliares; os limites oficiais são as faixas R de armadura existentes.','Faixas sem resistência publicada, inclusive somas pendentes de ancoragem, foram omitidas.','Msol -- significa ausência de demanda associada; não significa momento zero. As/m em cm²/m.','Critério desta rodada: comparação pela média. * Mrk depende da hipótese provisória de envelope horizontal de 20 mm.']
 for j,t in enumerate(notes):fit(c,px,H-168-j*15,t,pw-38,9.3)
 for j,s in enumerate(rs):
  co=j//rr;ro=j%rr;x=px+co*cw;y=H-270-ro*rh;col=C[s['status']]
  if ro%2==0:c.setFillColor(HexColor('#f0f4f6'));c.rect(x-3,y-rh+13,cw-8,rh,fill=1,stroke=0)
  lines0=[s['id']+' | Mrk '+mrlabel(s)+' | Msol '+num(s['Msol_mean_tfm_m']),arm(s)+' | As/m '+num(s['As_cm2_m']), 'n='+str(s['n_lines'])+' | η '+num(s['eta'])+' | '+','.join(s['marks'])]
  for k,t in enumerate(lines0):fit(c,x,y-k*10,t,cw-14,8.5,k==0,col if k==0 else '#17384b')
 txt(c,px,37,'Origem: ARPV0002.DXF característico + Concretopy arquivado | 19/10/2026',8)
 txt(c,px,23,'Análise média preliminar; geometria, seção e ancoragem permanecem sujeitas à revisão.',8)
 c.showPage();c.save();ov=fitz.open(stream=buf.getvalue(),filetype='pdf');page.show_pdf_page(page.rect,ov,0)
 target.set_metadata(dict(title='ATP S07 - '+n+' - resistência e solicitação média por faixa',author='Auxiliar de engenharia de João',subject='Média dos picos por linha dentro das regiões resistentes existentes; sem divisão em manchas MN.'))
 file=dest/f'ATP_S07_{n}_faixas_Mrk_Msol_media.pdf';target.save(file,garbage=4,deflate=True);target.close()
 check=fitz.open(file);text=check[0].get_text();assert all(s['id'] in text for s in rs);assert 'MNV001' not in text
 check[0].get_pixmap(matrix=fitz.Matrix(.4,.4)).save(str(tmp/f'media_oficial_{n}_geral.png'))
 check[0].get_pixmap(matrix=fitz.Matrix(1.4,1.4),clip=fitz.Rect(sw,90,sw+720,650)).save(str(tmp/f'media_oficial_{n}_legenda.png'))
 check[0].get_pixmap(matrix=fitz.Matrix(1.6,1.6),clip=fitz.Rect(170,390 if n=='7304' else 420,950,950 if n=='7304' else 980)).save(str(tmp/f'media_oficial_{n}_regioes.png'))
 qa.append(dict(sheet=n,path=str(file),pages=len(check),counts=dict(counts),placements=placements,all_codes_present=True,official_geometry='existing_R_capacity_regions_only'))
 print(n,'regions',len(rs),dict(counts),flush=True)
assert hashlib.sha256(source.read_bytes()).hexdigest()==sha
(r/'comparacao_media_faixas.json').write_text(json.dumps(dict(method='Média aritmética dos maiores picos negativos de cada linha DXF dentro de cada faixa R existente; sem exclusão de apoios; sem ponderação por área ou comprimento; somente capacidades publicadas; sem células MNV; hipóteses de segunda camada preservadas.',capacity_sha256=sha,rows=records,qa=qa),ensure_ascii=False,indent=2),encoding='utf8')
with (r/'comparacao_media_faixas.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f,delimiter=';');w.writerow(['faixa','prancha','As_cm2_m','Mrk_MRd_div1_4_tfm_m','Msol_media_tfm_m','n_linhas','eta_media','estado'])
 for s in records:w.writerow([s['id'],s['sheet'],s['As_cm2_m'],s['Mrk_eq_tfm_m'],s['Msol_mean_tfm_m'],s['n_lines'],s['eta'],s['status']])
