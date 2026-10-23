from pathlib import Path
import json,csv,math,collections,re
from shapely.geometry import shape,Point,box
from shapely.strtree import STRtree
from PIL import Image,ImageDraw,ImageFont
r=Path(__file__).parent
cs=json.loads((r/'componentes_negativos.json').read_text(encoding='utf8'))
g=json.loads((r/'regioes_negativas_geometria.json').read_text(encoding='utf8'))
cal=json.loads((r/'calibracao_amplitude.json').read_text(encoding='utf8'));scale=cal['scale']
es=json.loads((r/'entidades.json').read_text(encoding='utf8'));ts=json.loads((r/'textos.json').read_text(encoding='utf8'))
polys=sorted([shape(p) for p in g['polygons']],key=lambda p:(-p.centroid.y,p.centroid.x));tree=STRtree(polys)
st=[dict(id=f'MN{i+1:03d}',geometry=p.__geo_interface__,weighted_sum=0.,length=0.,peak=0.,texts=[]) for i,p in enumerate(polys)]
line_peaks=collections.defaultdict(dict)
for c in cs:
 ss=c['segments'];pts=[p for a,b,l in ss for p in [a,b]];x0=min(p[0] for p in pts);x1=max(p[0] for p in pts)
 if x1-x0<=.02 or max(p[1] for p in pts)-c['base']<=.0002:continue
 ix=int(tree.nearest(Point((x0+x1)/2,c['base'])))
 peak=max(max(0,(v[1]-c['base'])/scale) for v in pts)
 line_peaks[ix][c['base']]=max(line_peaks[ix].get(c['base'],0),peak)
for ix,s in enumerate(st):
 peaks=line_peaks[ix];s['line_peaks']=[{'y_DXF':y,'Mk_peak_tfm_m':-v} for y,v in sorted(peaks.items())]
 s['n_lines']=len(peaks);s['weighted_sum']=sum(peaks.values());s['length']=len(peaks);s['peak']=max(peaks.values(),default=0)
for t in ts:
 z=re.match(r'^-(\d+\.\d+)tfm/m$',t['text'])
 if not z:continue
 m=float(z[1]);x=float(t['x'])+len(t['text'])*5.25;base=round((float(t['y'])-1.3125-m*scale)/17.5)*17.5
 pt=Point(x,base);ix=int(tree.nearest(pt))
 if polys[ix].distance(pt)<5:st[ix]['texts'].append(m)
for s in st:
 s['mean_line_peaks_signed_tfm_m']=-s['weighted_sum']/s['length'] if s['length'] else None
 s['peak_graphic_signed_tfm_m']=-s['peak'];s['mean_labels_signed_tfm_m']=-sum(s['texts'])/len(s['texts']) if s['texts'] else None;s['n_labels']=len(s['texts']);s['assumed_1_61_count']=0
(r/'regioes_negativas_media_picos_resultados.json').write_text(json.dumps(dict(source='ARP0002.DXF',nature='caracteristico',unit='tf.m/m',method='Media aritmetica dos picos negativos por linha de diagrama; uma contribuicao por coordenada Y de eixo em cada regiao; sem ponderacao por comprimento ou area.',calibration=cal,regions=st),ensure_ascii=False,indent=2),encoding='utf8')
with (r/'regioes_negativas_media_picos.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f,delimiter=';');w.writerow(['regiao','Mk_media_picos_linhas_tfm_m','Mk_pico_grafico_tfm_m','media_rotulos_tfm_m','n_rotulos','n_linhas','centro_x_DXF','centro_y_DXF'])
 for s,p in zip(st,polys):w.writerow([s['id'],s['mean_line_peaks_signed_tfm_m'],s['peak_graphic_signed_tfm_m'],s['mean_labels_signed_tfm_m'],s['n_labels'],s['n_lines'],p.centroid.x,p.centroid.y])
W,H=6500,6500;im=Image.new('RGB',(W,H),'white');dr=ImageDraw.Draw(im)
fontpath='C:/Windows/Fonts/arial.ttf';bold='C:/Windows/Fonts/arialbd.ttf'
def ft(n,b=False):return ImageFont.truetype(bold if b else fontpath,n)
def txt(x,y,t,n=24,fill='#203448',b=False):dr.text((x,y),t,font=ft(n,b),fill=fill)
S=.65;X0=16900;YTOP=17000
# Map uses the original DXF axis orientation.
def xy(x,y):return (90+(float(x)-X0)*S,290+(YTOP-float(y))*S)
def color(s):
 v=min(1,abs(s['mean_line_peaks_signed_tfm_m'] or 0)/8);return (int(255-95*v),int(231-195*v),int(225-185*v))
for e in es:
 d=dict(e['pairs'])
 if e['type']=='LINE' and d.get(8) in ['213','214','223','224']:dr.line([xy(d[10],d[20]),xy(d[11],d[21])],fill='#dce1e5',width=1)
for s,p in zip(st,polys):
 dr.polygon([xy(x,y) for x,y in p.exterior.coords],fill=color(s),outline='#c17a70')
 for ring in p.interiors:dr.polygon([xy(x,y) for x,y in ring.coords],fill='white')
# Supporting geometry and names, preserving the DXF coordinates.
for i,e in enumerate(es):
 d=dict(e['pairs']);layer=d.get(8)
 if e['type']=='POLYLINE' and layer in ['225','207','201']:
  pts=[];j=i+1
  while es[j]['type']=='VERTEX':
   v=dict(es[j]['pairs']);pts.append(xy(v[10],v[20]));j+=1
  if len(pts)>1:dr.line(pts,fill='#657b8d',width=2)
 if e['type']=='LINE' and layer=='241':dr.line([xy(d[10],d[20]),xy(d[11],d[21])],fill='#b4b4b4',width=1)
for t in ts:
 if t['layer']=='254':
  x,y=xy(t['x'],t['y']);txt(x,y,t['text'],13,fill='#496070')
occupied=[]
def overlap(b):return any(b[0]<q[2]+2 and b[2]>q[0]-2 and b[1]<q[3]+2 and b[3]>q[1]-2 for q in occupied)
# Give the small regions first access to nearby free label positions.
for i in sorted(range(len(st)),key=lambda i:polys[i].area):
 s=st[i];p=polys[i];anchor=p.representative_point();cx,cy=xy(anchor.x,anchor.y);bw,bh=110,39;rect=None
 for radius in [0,22,40,60,84,112,146,184,228,280,350,430]:
  for ang in ([0] if radius==0 else range(0,360,20)):
   px=cx+radius*math.cos(math.radians(ang));py=cy+radius*math.sin(math.radians(ang));bb=(px-bw/2,py-bh/2,px+bw/2,py+bh/2)
   if bb[0]>20 and bb[2]<3470 and bb[1]>270 and bb[3]<5900 and not overlap(bb):rect=bb;break
  if rect:break
 if rect is None:raise RuntimeError('label placement '+s['id'])
 occupied.append(rect);a,b,c,d=rect;ex=min(max(cx,a),c);ey=min(max(cy,b),d)
 if not(a<=cx<=c and b<=cy<=d):dr.line([(cx,cy),(ex,ey)],fill='#92392f',width=1);dr.ellipse((cx-2,cy-2,cx+2,cy+2),fill='#92392f')
 dr.rounded_rectangle(rect,radius=3,fill='white',outline='#92392f',width=1)
 val=s['mean_line_peaks_signed_tfm_m'];v=f'{val:.2f}'.replace('.',',') if abs(val)>=.005 else '|Mk|<0,01'
 txt(a+4,b+2,s['id'],16,b=True);txt(a+4,b+20,v,15,fill='#9e2f29')
txt(70,35,'ATP S07 | TÉRREO | MOMENTOS HORIZONTAIS NEGATIVOS',42,b=True)
txt(70,100,'Mk característico [tf·m/m] | origem: ARP0002.DXF | regiões reconstruídas dos diagramas',27)
txt(70,145,'Rótulo: região e média dos picos por linha. Limites aproximados entre linhas do diagrama; sem verificação resistente.',25)
txt(70,190,'Cinza: diagramas/isocurvas de referência. Vermelho: regiões com sinal negativo identificado.',25)
left=3550;txt(left,280,'MÉDIAS DOS PICOS POR LINHA [tf·m/m]',29,b=True)
txt(left,325,'Média aritmética: um pico negativo por linha em cada região.',22)
txt(left,360,'Amplitude calibrada; linhas e picos individuais registrados no JSON.',22)
rows=115;cw=700;rh=42
for i,s in enumerate(st):
 col=i//rows;row=i%rows;x=left+col*cw;y=430+row*rh
 if row%2==0:dr.rectangle((x-4,y-2,x+cw-20,y+rh-3),fill='#f1f4f6')
 dr.rectangle((x,y+5,x+19,y+24),fill=color(s),outline='#9b6c65')
 v=s['mean_line_peaks_signed_tfm_m'];label=f'{v:.2f}'.replace('.',',') if abs(v)>=.005 else '|Mk|<0,01'
 txt(x+28,y,s['id']+'   '+label,23,b=True)
 txt(x+330,y,'n='+str(s['n_lines']),21)
txt(left,5400,'LEITURA E LIMITES',28,b=True)
notes=['457 manchas negativas, incluindo regiões pequenas e de baixa magnitude.','Cada linha contribui uma vez, com o maior módulo dentro da região.','Escala validada em 1.763 rótulos: desvio máximo observado de 0,02 tf·m/m.','Não foi necessário adotar 1,61: as amplitudes estão disponíveis.','Valores são estimativas gráficas; não substituem os resultados nodais do TQS.','A média não substitui o pico na comparação com a resistência.','Sinal negativo mantido. Não houve divisão por γf.','n = número de linhas de diagrama que contribuíram para a média.','O contorno não corresponde à isocurva de 1,80: representa o sinal negativo.']
for j,t in enumerate(notes):txt(left,5460+j*48,t,23)
txt(70,6160,'Método: projeção dos intervalos negativos nos eixos das linhas; faixas tributárias até a meia distância entre linhas.',25)
txt(70,6210,'Média = Σ[pico negativo de cada linha na região] / número de linhas. Sem ponderação por área ou comprimento.',25)
txt(70,6260,'Origem dos esforços: resultado TQS exportado em DXF; natureza característica confirmada por João. Leitura preliminar — 19/10/2026.',23)
im.save(r/'ATP_S07_momentos_negativos_media_picos_linhas.png',optimize=True)
preview=im.copy();preview.thumbnail((1500,1500));preview.save(r/'preview_media_picos.png')
print('regions',len(st),'global_line_peak_mean',-sum(s['weighted_sum'] for s in st)/sum(s['length'] for s in st),'labels_assigned',sum(s['n_labels'] for s in st),'maxpeak',max(s['peak'] for s in st))

with (r/'picos_por_linha_regioes_negativas.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f,delimiter=';');w.writerow(['regiao','eixo_y_DXF','Mk_pico_caracteristico_tfm_m'])
 for s in st:
  for line in s['line_peaks']:w.writerow([s['id'],line['y_DXF'],line['Mk_peak_tfm_m']])
print('MN214',next(s for s in st if s['id']=='MN214'))
