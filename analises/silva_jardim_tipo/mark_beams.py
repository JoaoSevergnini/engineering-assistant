from pathlib import Path
import sys,json,csv,collections,zipfile,hashlib,math
ROOT=Path(r'\\srvmaster\PUBLICO\Joao Severgnini\Simon\engineering-assistant')
sys.path.insert(0,str(ROOT/'tmp/pdf_deps'))
import fitz
P=ROOT/'analises/silva_jardim_tipo'
OUT=P/'pranchas_marcadas'; OUT.mkdir(exist_ok=True)
SRC=Path(r'S:\PROJETOS EM EXECUÇÃO\24-212-TGD-SILVA JARDIM-POA-RS\APOIO\JOÃO\TIPO')
def read(n):return json.loads((P/n).read_text(encoding='utf-8-sig'))
def rows(n):
 with (P/n).open(encoding='utf-8-sig') as f:return list(csv.DictReader(f,delimiter=';'))
D=read('drawing_inventory.json');A=read('anchorage_review.json');E=read('executability_review.json');J=read('suspension_regional_review.json')
F=rows('flexao_por_regiao.csv');C=rows('cortante_por_faixa.csv');AP=rows('ancoragem_positiva_extremos.csv');AN=rows('ancoragem_negativa_extremos.csv')
issues={v:[] for v in D};colors={'R':(0.78,0.1,0.13),'A':(0.73,0.42,0.02),'B':(0.06,0.32,0.65)}
def add(v,cat,title,text,points):
 b=D[v]['bbox']; pts=[(max(b[0]+4,min(b[2]-4,x)),max(b[1]+4,min(b[3]-4,y))) for x,y in points]
 issues[v].append(dict(id=v+'-'+str(len(issues[v])+1).zfill(2),category=cat,title=title,text=text,points=pts,pdf=D[v]['pdf']))
def bar(v,mark,instance=None):
 a=[b for b in D[v]['bars'] if b['mark']==mark and (instance is None or b['instance']==instance)]
 return a[0] if a else None
def segpoint(v,x,func='positive'):
 bs=[b for b in D[v]['bars'] if b['function']==func and b['x_start_common']-0.15<=x<=b['x_end_common']+0.15]
 y=bs[0]['source']['segment_pdf']['y'] if bs else (D[v]['bbox'][1]+D[v]['bbox'][3])/2
 return D[v]['origin_pdf_x']+x*56.64,y
# Cisalhamento: coordenada apontada na linha de distribuição dos estribos.
for r in C:
 if r['resultado']=='PASS' or not r['Asw_s_exigida_cm2_m']:continue
 v=r['viga'];lo=float(r['inicio_m']);hi=float(r['fim_m']); x=(lo+hi)/2
 ss=D[v]['stirrups'];s=next((s for s in ss if s['x_start_common']-.2<=x<=s['x_end_common']+.2),ss[0])
 y=s['source']['segment_pdf']['y'];p=(D[v]['origin_pdf_x']+x*56.64,y)
 area=float(r['Asw_s_fornecida_cm2_m']);req=float(r['Asw_s_exigida_cm2_m']);sp=float(r['espacamento_cm']);mx=float(r['smax_cm'])
 text=f"Vão {r['vao']}, x={lo:.2f} a {hi:.2f} m: Ø{r['bitola_mm']} c/{sp:g}. Asw/s fornecida {area:.3f}; exigida {req:.3f} cm²/m. Vk={float(r['Vsk_kn']):.2f} kN."
 if sp>mx:text+=f' Espaçamento {sp:g} > máximo calculado {mx:.2f} cm.'
 add(v,'R','Cortante / estribos',text+' Resultado desfavorável no cálculo da revisão; ver memória e hipóteses no relatório.',[p])
# Flexão: reunir regiões repetidas, conservar o resultado mais crítico.
groups=collections.defaultdict(list)
for r in F:
 if r['resultado_ensaio']!='PASS' and r['utilizacao'] and float(r['utilizacao'])>1:groups[(r['viga'],r['vao'],r['sinal'])].append(r)
for (v,span,sign),rs in groups.items():
 r=max(rs,key=lambda r:float(r['utilizacao']));x=(float(r['inicio_m'])+float(r['fim_m']))/2
 add(v,'A','Flexão: conferir demanda e composição',f"Vão {span}, {'negativa' if sign=='NEGATIVE' else 'positiva'} ({r['marcas']}): Msk={float(r['Msk_knm']):.3f}; capacidade equivalente Mk={float(r['Mk_equivalente_knm']):.3f} kN.m. Ensaio conservador de seção retangular. Confirmar seção efetiva, camadas e vínculo antes de concluir insuficiência.",[segpoint(v,x,'negative' if sign=='NEGATIVE' else 'positive')])
# Ancoragem negativa: agrupamento por apoio, marcado nas próprias terminações das barras.
ng=collections.defaultdict(list)
for r in AN:
 if r['dobra_resultado']=='FAIL' or r['reta_resultado']=='FAIL' or r['resistencia_curva']=='INCONCLUSIVE':ng[(r['viga'],r['apoio'])].append(r)
for (v,sup),rs in ng.items():
 end=next((e for e in A[v]['negative_ends'] if e['support']['support_id']==sup),None)
 pts=[];texts=[];bad=False
 for r in rs:
  b=None;side=end['support']['support_side'] if end else 'LEFT'
  if end:
   mm=next((m for m in end['marks'] if m['bar'].split('@')[0]==r['marca']),None)
   if mm:b=bar(v,r['marca'],int(mm['bar'].split('@')[1]))
  if not b:b=bar(v,r['marca'])
  if b:
   seg=b['source']['segment_pdf']; pts.append((seg['x0'] if side=='LEFT' else seg['x1'],seg['y']))
  if r['modo']=='VERTICAL_BEND' and r['dobra_resultado']=='FAIL':
   bad=True;texts.append(f"{r['marca']}: perna {float(r['perna_lida_cm']):.1f} < {float(r['perna_exigida_escritorio_cm']):.1f} cm")
  elif r['modo']!='VERTICAL_BEND' and r['reta_resultado']=='FAIL':texts.append(f"{r['marca']}: reta {float(r['projecao_cm']):.2f} / lb {float(r['lb_basico_cm']):.2f} cm (limítrofe)")
 if not pts:continue
 text=f"Apoio {sup}. "+'; '.join(texts)+'. ' if texts else f'Apoio {sup}. '
 text+='Critério de ancoragem da revisão/escritório; confirmar geometria das dobras, confinamento, interferência com pilar e resistência da curva. Não é aprovação normativa do nó.'
 add(v,'R' if bad else 'A','Terminações da armadura negativa',text,pts)
# Ancoragem positiva: apenas apoios END físicos, excluindo balanços.
for r in AP:
 if r['ensaio_sem_credito_gancho']=='True' and r['ensaio_com_gancho_condicional']=='True':continue
 v=r['viga'];sup=r['apoio'];side=r['lado']
 if not r['As_apoio_cm2']:continue
 support=next((s for s in A[v]['supports'] if s['geometry']['support_id']==sup and s['geometry']['support_side']==side),None)
 if not support:continue
 g=support['geometry'];x=g['internal_face_m'];pts=[]
 for ob in support.get('longitudinal_bars',[]):
  b=ob['bar'];seg=b['source']['segment_pdf'];pts.append((seg['x0'] if side=='LEFT' else seg['x1'],seg['y']))
 if not pts:pts=[segpoint(v,x)]
 conditional=r['ensaio_com_gancho_condicional']=='True'
 text=f"{sup}: As requerida/presente = {float(r['As_apoio_cm2']):.2f}/{float(r['As_presente_cm2']):.2f} cm²; lb necessário/geometria = {float(r['lb_nec_cm']):.1f}/{float(r['lb_geom_cm']):.1f} cm. "
 text+=('Ensaio só atende com crédito condicional do gancho: comprovar dobra e nó.' if conditional else 'Ensaio de ancoragem desfavorável mesmo no cenário condicional de gancho; conferir nó e hipóteses no relatório.')
 if v in ['V624','V628']:text+=' Há 3Ø8 N4 existentes; avaliar contribuição conjunta e posição dos grampos.'
 add(v,'A','Ancoragem positiva no apoio',text,pts)
# Cortes das barras positivas: condição A e B são independentes.
for v,aa in A.items():
 for r in aa.get('positive_cuts',[]):
  if r.get('overall',{}).get('scaling_passes') is not False:continue
  m=r['interrupted_mark'];b=bar(v,m.split('@')[0],int(m.split('@')[1]));seg=b['source']['segment_pdf'];side=r['cut_side'].upper()
  ca=r['condition_A'];cb=r['condition_B']
  add(v,'A','Interrupção de barra positiva',f"{m.split('@')[0]}, corte {'esquerdo' if side=='LEFT' else 'direito'}: condição A, disponível {ca['available_length_cm']:.1f} / exigido {ca['required_length_cm']:.1f} cm; condição B, {cb['available_length_cm']:.1f}/{cb['required_length_cm']:.1f} cm. Conferir decalagem e composição resistente; ensaio conservador, sem crédito integral das mesas.",[(seg['x0'] if side=='LEFT' else seg['x1'],seg['y'])])
# Construtibilidade: destacar a faixa mais restritiva; demais faixas permanecem na memória.
for v,rs in E.items():
 if not rs:continue
 r=max(rs,key=lambda r:r['necessary_width_cm']-r['inside_stirrup_cm']);x=sum(r['interval_m'])/2
 text=f"Sobreposição interpretada: {', '.join(r['marks'])}, camada {r['layer']}, x={r['interval_m'][0]:.2f} a {r['interval_m'][1]:.2f} m. Largura necessária {r['necessary_width_cm']:.1f} / livre {r['inside_stirrup_cm']:.1f} cm. Confirmar camadas efetivamente simultâneas, largura do nó e passagem do concreto. {len(rs)} faixas a conferir na memória; não é falha executiva comprovada."
 if v=='V610':text+=' Barras em níveis distintos: não somar automaticamente na mesma camada.'
 add(v,'A','Executabilidade / sobreposição',text,[segpoint(v,x,'negative' if r['sign']=='NEGATIVE' else 'positive')])
# Suspensão: só pendências e resultados desfavoráveis; os ensaios favoráveis continuam condicionados no relatório.
for r in J:
 v=r['receiver'];sender=r['sender'];status=r.get('overall_result');x=r.get('connection',{}).get('projected_axis_m')
 if status=='PASS' and v!='V621':continue
 if x is None:x=0
 b=D[v]['bbox']; y=b[1]+(b[3]-b[1])*.42
 txt=f'Nó {sender} -> {v}. '
 if status=='FAIL':
  nums=[s for s in r.get('subintervals',[]) if s.get('overall_result')=='FAIL']
  if nums:
   z=nums[0];txt+=f"Asw/s existente {z['provided']['Asw_per_s_cm2_m']:.3f} / total exigida {z['asw_per_s_total_required']:.3f} cm²/m. "
  txt+='Resultado desfavorável para o ensaio de suspensão adotado.'
 elif v=='V611':txt+='Faixa de distribuição cruza mudança de altura 57/47 cm; suspensão inconclusiva.'
 elif v=='V621':txt+='Faixas de suspensão de V606 e V607 se sobrepõem: conferir demanda conjunta e concomitância.'
 else:txt+='Transferência em região especial; confirmar caminho de carga, origem dos esforços e distribuição.'
 txt+=' Hipótese: 75% da reação característica; máximos separados, sem confirmação da combinação simultânea.'
 add(v,'R' if status=='FAIL' else 'B','Suspensão / apoio indireto',txt,[(D[v]['origin_pdf_x']+x*56.64,y)])
# Questões documentais e geometria especial.
v='V623';b=D[v]['bbox'];add(v,'R','Armadura N2 sem posição longitudinal identificada','N2 = 4Ø16 C=464 consta na relação e na seção A, porém sua posição longitudinal/cotas não foi identificada na elevação. Positiva inconclusiva: confirmar posição, camadas e ancoragens. A marcação indica lacuna documental, não ausência física comprovada.',[(D[v]['cross_x']+20,200),(D[v]['origin_pdf_x']+110,b[1]+(b[3]-b[1])*.78)])
for v,txt,x in [('V610','Alturas 129,5 / 47 / 122 cm no primeiro vão; conferir transições, forma e níveis das armaduras. Seções distintas não podem ser substituídas por uma seção uniforme.',2),('V611','Trecho intermediário h=47 cm entre x=3,88 e 5,43 m. Conferir a transição com h=57 cm e os encontros com V602/V603.',4.65),('V626','Prolongamento esquerdo físico de 32 cm, h=47 cm, recebe V610 (~140 kN). Conferir nó, suspensão, torção e ancoragens; não tratar esta face como apoio extremo de pilar.',-.16)]:
 add(v,'B','Geometria e nó especial',txt,[segpoint(v,x)])
for v in ['V617','V620','V622','V625','V627','V629']:
 b=D[v]['bbox'];right=max(s['x_end_common'] for s in D[v]['stirrups'])
 add(v,'B','Continuação em balanço','Prolongamento físico direito de 70 cm: conferir armadura superior, terminação e ligação no apoio. Esta extremidade não foi tratada como END de pilar nos ensaios de ancoragem.',[segpoint(v,right,'negative')])
(P/'marcacoes_vigas_manifesto.json').write_text(json.dumps(issues,ensure_ascii=False,indent=2),encoding='utf-8')
print('Manifesto',sum(map(len,issues.values())),'ocorrências', {v:len(a) for v,a in issues.items()})


# Renderização vetorial: os desenhos originais continuam pesquisáveis e ampliáveis.
def wrap(text,width,size=11):
 words=text.split();lines=[];line=''
 for w in words:
  trial=(line+' '+w).strip()
  if fitz.get_text_length(trial,fontname='helv',fontsize=size)>width and line:lines.append(line);line=w
  else:line=trial
 if line:lines.append(line)
 return lines

def textlines(page,x,y,text,width,size=11,color=(.15,.15,.15)):
 lines=wrap(text,width,size)
 for line in lines:
  page.insert_text((x,y),line,fontname='helv',fontsize=size,color=color);y+=size*1.35
 return y

def marks(page,items,transform=lambda p:p,small=False):
 used=[];fs=7 if small else 9;h=fs+7
 for item in items:
  col=colors[item['category']]
  for pt in item['points']:
   x,y=transform(pt); tag=item['id'];w=fitz.get_text_length(tag,fontname='hebo',fontsize=fs)+10
   tx=min(page.rect.width-w-8,max(8,x+13));ty=max(58 if not small else 12,y-24)
   box=fitz.Rect(tx,ty,tx+w,ty+h)
   for attempt in range(35):
    if not any(box.intersects(z) for z in used):break
    ty+=h+3
    if ty+h>page.rect.height-15:ty=max(12,y-60-attempt*5);tx=max(8,x-w-12)
    box=fitz.Rect(tx,ty,tx+w,ty+h)
   used.append(box)
   page.draw_circle((x,y),3.3 if small else 4,color=col,fill=(1,1,1),width=1)
   page.draw_line((x,y),(box.x0,box.y1-h/2),color=col,width=.7)
   page.draw_rect(box,color=col,fill=(1,1,1),width=.8)
   page.insert_text((box.x0+5,box.y1-4),tag,fontname='hebo',fontsize=fs,color=col)
   an=page.add_rect_annot(box);an.set_colors(stroke=col);an.set_border(width=0)
   an.set_info(title='Revisão de armaduras',subject=item['title'],content=tag+' | '+item['title']+'\n'+item['text']);an.update()

docs={name:fitz.open(str(SRC/name)) for name in sorted({d['pdf'] for d in D.values()})}
review=fitz.open();index={}; counts=collections.Counter()
for v in sorted(D):
 source=docs[D[v]['pdf']];clip=fitz.Rect(D[v]['bbox']);items=issues[v]
 width=1191;drawh=min(395,max(225,1127*clip.height/clip.width));drawtop=92;ledger=drawtop+drawh+42
 colwidth=550; blocks=[]
 for i in items:
  lines=wrap(i['text'],colwidth-16,11);bh=34+len(lines)*14.85
  blocks.append((i,bh))
 left=blocks[::2];right=blocks[1::2];height=max(842,ledger+max(sum(b[1] for b in left),sum(b[1] for b in right))+75)
 page=review.new_page(width=width,height=height)
 page.insert_text((32,34),v+' | Revisão sobre o detalhamento',fontname='hebo',fontsize=21,color=(.1,.18,.27))
 page.insert_text((32,54),D[v]['pdf']+' | prancha original, página 1 | revisão de 09/10/2026',fontsize=10)
 labels=[('R','Vermelho: divergência documental / ensaio desfavorável'),('A','Âmbar: conferir hipóteses, nó ou geometria'),('B','Azul: região especial / análise inconclusiva')]
 xx=32
 for cat,label in labels:
  page.draw_rect(fitz.Rect(xx,67,xx+8,75),color=colors[cat],fill=colors[cat]);page.insert_text((xx+13,75),label,fontsize=9,color=colors[cat]);xx+=415 if cat=='R' else 365
 dest=fitz.Rect(32,drawtop,width-32,drawtop+drawh)
 scale=min(dest.width/clip.width,dest.height/clip.height);ox=dest.x0+(dest.width-clip.width*scale)/2;oy=dest.y0+(dest.height-clip.height*scale)/2
 page.show_pdf_page(dest,source,0,clip=clip)
 marks(page,items,lambda p:(ox+(p[0]-clip.x0)*scale,oy+(p[1]-clip.y0)*scale))
 page.draw_line((32,ledger-19),(width-32,ledger-19),color=(.7,.75,.8))
 for ci,group in enumerate([left,right]):
  x=32+ci*577;y=ledger
  for item,bh in group:
   col=colors[item['category']];counts[item['category']]+=1
   page.insert_text((x,y),item['id']+' | '+item['title'],fontname='hebo',fontsize=11,color=col)
   textlines(page,x+5,y+17,item['text'],colwidth-16,11);y+=bh
 if not items:textlines(page,32,ledger,'Sem ocorrência específica destacada nesta viga. Isso não representa aprovação global: os limites da revisão e as verificações condicionais permanecem no relatório.',1100,12)
 foot='x em metros a partir da primeira face interna de apoio; lb em cm; As em cm². Critérios e memória: Relatorio_revisao_vigas_TIPO_FINAL.pdf.'
 page.insert_text((32,height-39),foot,fontsize=9,color=(.35,.35,.35))
 page.insert_text((32,height-23),'Marcas de revisão, sem propostas de alteração. Texto normativo integral não consultado. Originais preservados. | '+str(len(review))+'/29',fontsize=9,color=(.35,.35,.35))
 index[v]=len(review)-1
 # Versão em imagem para consulta rápida. O PDF preserva melhor a leitura ao ampliar.
 pix=page.get_pixmap(matrix=fitz.Matrix(2400/width,2400/width),alpha=False)
 pix.save(str(OUT/(v+'_marcada.png')))
 print(v,len(items),'marcas, página',round(height),flush=True)
main=OUT/'Vigas_TIPO_revisao_marcada.pdf'
review.save(str(main),garbage=4,deflate=True)
for name,doc in docs.items():
 beamlist=[v for v in sorted(D) if D[v]['pdf']==name]
 marks(doc[0],[item for v in beamlist for item in issues[v]],small=True)
 for v in beamlist:doc.insert_pdf(review,from_page=index[v],to_page=index[v])
 doc.set_metadata({'title':'Revisão de armaduras - '+name,'subject':'Marcações vinculadas ao relatório; sem alteração do detalhamento original','author':'Revisão técnica de apoio a João'})
 doc.save(str(OUT/(Path(name).stem+'_MARCADO.pdf')),garbage=4,deflate=True)
(P/'marcacoes_vigas_manifesto.json').write_text(json.dumps(issues,ensure_ascii=False,indent=2),encoding='utf-8')
readme='''REVISÃO MARCADA - VIGAS TIPO - SILVA JARDIM

Vigas_TIPO_revisao_marcada.pdf: uma página de revisão por viga (29 páginas), com recorte vetorial, marcações e comentários na mesma página.
Arquivos *_MARCADO.pdf: a primeira página conserva a prancha completa com etiquetas; as páginas seguintes apresentam as revisões individuais correspondentes. As etiquetas possuem comentários PDF clicáveis.
Vxxx_marcada.png: as mesmas páginas em imagem.

Vermelho: divergência documental ou resultado desfavorável no critério de cálculo indicado; isso não equivale automaticamente a uma reprovação normativa de toda a viga.
Âmbar: interpretação, composição de armaduras, geometria ou hipóteses a conferir.
Azul: geometria especial, transferência de cargas ou verificação inconclusiva.

As ocorrências remetem à memória do relatório Relatorio_revisao_vigas_TIPO_FINAL.pdf, incluído no pacote. Não foram propostas melhorias nem modificadas armaduras. PDFs originais preservados.
Há agrupamentos por apoio/região; as demais faixas de executabilidade e resultados favoráveis condicionais estão na memória. Ausência de etiqueta não significa aprovação global.
As coordenadas x são relativas à primeira face interna de apoio; as marcas são locais à viga. Texto normativo integral não consultado.
'''
(OUT/'LEIA-ME.txt').write_text(readme,encoding='utf-8')
(OUT/'manifesto_marcacoes.json').write_text(json.dumps(issues,ensure_ascii=False,indent=2),encoding='utf-8')
archive=P/'Vigas_TIPO_marcadas.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
 for f in sorted(OUT.iterdir()):z.write(f,f.name)
 z.write(P/'Relatorio_revisao_vigas_TIPO_FINAL.pdf','Relatorio_revisao_vigas_TIPO_FINAL.pdf')
# Verificações de integridade, legibilidade textual e cobertura.
check=fitz.open(str(main));assert len(check)==29
for v,pi in index.items():
 txt=check[pi].get_text()
 for item in issues[v]:assert item['id'] in txt,(v,item['id'])
for name in docs:
 original=hashlib.sha256((SRC/name).read_bytes()).hexdigest()
 manifest=read('source_manifest.json')
 # Registrar hashes correntes sem modificar os arquivos fonte.
 print('Fonte preservada',name,original)
print('FINAL',counts,'PDF',main.stat().st_size,'ZIP',archive.stat().st_size)

