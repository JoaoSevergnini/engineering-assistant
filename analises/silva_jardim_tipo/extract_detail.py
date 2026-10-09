from pathlib import Path
import sys,json,re,statistics
ROOT=Path(r'\\srvmaster\PUBLICO\Joao Severgnini\Simon\engineering-assistant');sys.path.insert(0,str(ROOT/'tmp/pdf_deps'))
import pymupdf as fitz
OUT=ROOT/'analises/silva_jardim_tipo';SRC=Path('S:/PROJETOS EM EXECU\u00c7\u00c3O/24-212-TGD-SILVA JARDIM-POA-RS/APOIO/JO\u00c3O/TIPO')
GROUPS={1:{601:[85,40,2580,515],602:[85,520,2580,1030],603:[85,1030,1130,1550],604:[1160,1030,2210,1550],605:[2600,40,3030,490],606:[2610,510,3010,920],607:[3020,510,3320,920]},2:{608:[85,40,1130,565],609:[1150,40,1680,510],610:[1700,65,3130,690],611:[80,680,910,1100],612:[990,680,1415,1110],613:[1430,680,1850,1110],614:[1880,680,2310,1140],615:[2320,680,2740,1120],616:[85,1150,560,1630],617:[570,1150,1080,1630],618:[1080,1150,1400,1600],619:[1405,1150,1820,1630],620:[1840,1150,2280,1630]},3:{621:[80,40,540,455],622:[560,40,1070,455],623:[1080,40,1620,490],624:[1625,40,2110,455],625:[80,480,570,905],626:[635,480,1170,950],627:[80,940,580,1390],628:[600,940,1080,1390],629:[1310,480,2190,935]}}
POS={601:[2,3,6,8,14],602:[2,3,5,9,11,12,15,17,19],603:[2,3,5,7,9],604:[4,5,8,9,11],605:[3],606:[1,2],607:[1],608:[2,5,7,8],609:[3,4],610:[1,4,9,10,14,15],611:[1,3,5,6],612:[3],613:[1],614:[3,4],615:[1],616:[1,4,6],617:[1,4],618:[1],619:[2,3],620:[3,5],621:[3,4],622:[1,4],623:[2],624:[1,3],625:[1,4],626:[2,5],627:[1,4],628:[1,3],629:[5,6,7,8]}
SECOND={601:{2:1,5:1,9:1,14:1},602:{2:2,4:'all',7:2,12:2,14:2,15:2,17:1,18:1,21:2},603:{2:2,4:1,9:1,10:2},604:{1:2,4:2,7:2,11:2,12:2},605:{1:2,5:2},606:{1:2},609:{1:2,3:1,6:1},610:{6:1,9:1,12:2,15:1,17:1},611:{2:1,4:1,6:1},612:{1:1,2:1},613:{2:1,3:1},614:{1:1,2:1,4:1},615:{1:1,2:2},616:{5:1,6:1},617:{1:1,2:2},620:{1:1,7:1},621:{1:1},622:{1:1,3:2},623:{1:2},624:{3:1},625:{1:1,2:2},626:{3:2,6:1},627:{1:1,3:2},628:{3:1},629:{2:2,4:2,5:2,6:2,8:2}}
SKIN={610:[2],620:[4,8]};SPECIAL={624:[4],626:[1],628:[4]}
ALL={}
for sheet,beams in GROUPS.items():
 file=next(SRC.glob(f'*0630{sheet}*'));page=fitz.open(file)[0];drawings=page.get_drawings()
 all_lines=[]
 for block in page.get_text('dict')['blocks']:
  for line in block.get('lines',[]):all_lines.append({'text':''.join(s['text'] for s in line['spans']),'bbox':list(line['bbox'])})
 for number,box in beams.items():
  rect=fitz.Rect(box);tl=[l for l in all_lines if rect.contains(fitz.Rect(l['bbox']))]
  cross=min((l['bbox'][0] for l in tl if l['text'].strip()=='Corte A'),default=box[2])
  rows=[]
  for l in sorted(tl,key=lambda l:(l['bbox'][1],l['bbox'][0])):
   found=next((r for r in rows if abs(r['y']-l['bbox'][1])<.8),None)
   if found:found['parts'].append(l)
   else:rows.append({'y':l['bbox'][1],'parts':[l]})
  dark=[];light=[];black=[];vertical=[]
  for d in drawings:
   c=d['color']
   if c is None:continue
   for it in d['items']:
    if it[0]!='l':continue
    a,b=it[1:3]
    if not rect.contains(a) or not rect.contains(b):continue
    if c[0]==0 and c[1]==0 and c[2]>.5 and abs(a.x-b.x)<.01 and abs(a.y-b.y)>3 and a.x<cross-15:
     vertical.append({'x':a.x,'y0':min(a.y,b.y),'y1':max(a.y,b.y)})
    if c==(0,0,0) and abs(a.y-b.y)<.01 and abs(a.x-b.x)>15 and max(a.x,b.x)<cross-15:
     black.append({'x0':min(a.x,b.x),'x1':max(a.x,b.x),'y':a.y})
    if c[0]==0 and c[1]==0 and c[2]>.5 and abs(a.y-b.y)<.01 and abs(a.x-b.x)>15 and max(a.x,b.x)<cross-15:
     dark.append({'x0':min(a.x,b.x),'x1':max(a.x,b.x),'y':a.y})
    if c[0]==0 and c[1]>.4 and c[2]>.9 and abs(a.x-b.x)<.01 and abs(a.y-b.y)>1 and a.x<cross-15:
     light.append(a.x)
  origin=min(light) if light else None
  bars=[];stirrups=[]
  for row in rows:
   parts=sorted(row['parts'],key=lambda p:p['bbox'][0]);text=' '.join(l['text'] for l in parts)
   pattern=r'N(\d+)\s+(\d+)\s+\u00d8\s*(\d+(?:\.\d+)?)\s*(?:C=(\d+))?'
   for match in re.finditer(pattern,text):
    mark,n,phi,length=match.groups();mark=int(mark);n=int(n);phi=float(phi)
    # Find the original label's actual horizontal anchor, including split labels.
    candidate=[l for l in parts if re.match(rf'N{mark}(?:\s|$)',l['text'].strip())]
    if not candidate:continue
    occ=sum(1 for m in re.finditer(pattern,text[:match.start()]) if int(m.group(1))==mark); label=candidate[min(occ,len(candidate)-1)];x=(label['bbox'][0]+label['bbox'][2])/2;y=row['y'];eligible=[d for d in dark if d['x0']-2<=x<=d['x1']+2 and abs(d['y']-y)<13]
    if not eligible:continue
    seg=min(eligible,key=lambda d:abs(d['y']-y));function='positive' if mark in POS[number] else 'negative'
    if number==602 and mark==5:function='negative'
    if number==602 and mark==6:function='positive' if phi==10 else 'negative'
    if mark in SKIN.get(number,[]):function='skin'
    if mark in SPECIAL.get(number,[]):function='staple'
    n2=SECOND.get(number,{}).get(mark,0);n2=n if n2=='all' else min(n2,n)
    layers=[n-n2,n2] if n2 else [n]
    if number==604 and mark==9:layers=[0,0,n]
    entry={'mark':f'N{mark}','instance':len(bars)+1,'bars':n,'diameter_mm':phi,'layers':layers,'function':function,'face':'lower' if function=='positive' else 'upper','x_start_common':round((seg['x0']-origin)/.5664/100,4),'x_end_common':round((seg['x1']-origin)/.5664/100,4),'total_length_cm':int(length) if length else None,'source':{'pdf':file.name,'page':1,'label':label,'row_text':text,'segment_pdf':seg,'origin_pdf_x':origin,'coordinate_method':'graphical trace; 0.5664 PDF points/cm, drawing 1:50; not substituted for explicit dimension','layers':'manual visual interpretation with office rule and printed 2a/3aCAM'},'shape':'straight'}
    entry['termination_by_side']={};entry['bend_documents']={}
    for side,key in [('LEFT','x0'),('RIGHT','x1')]:
     vv=[v for v in vertical if abs(v['x']-seg[key])<.15 and min(abs(v['y0']-seg['y']),abs(v['y1']-seg['y']))<.15]
     if vv:
      v=max(vv,key=lambda v:v['y1']-v['y0']);leg=(v['y1']-v['y0'])/.5664
      entry['termination_by_side'][side]='HOOK';entry['bend_documents'][side]={'side':side,'orientation':'vertical','vertical_leg_cm':round(leg,2),'provenance':{'pdf':file.name,'page':1,'segment':v,'length_method':'PDF vector at scale1:50, rounded to nearest cm only after visual cross-check'}};entry['shape']='bent'
     else:entry['termination_by_side'][side]='STRAIGHT'
    if len(entry['bend_documents'])==1:
     side=next(iter(entry['bend_documents']));entry['end_bend']={'side':side.lower(),'length_cm':entry['bend_documents'][side]['vertical_leg_cm'],'source':entry['bend_documents'][side]['provenance']}
    bars.append(entry)
  for row in rows:
   parts=sorted(row['parts'],key=lambda p:p['bbox'][0]);txt=' '.join(l['text'] for l in parts)
   for match in re.finditer(r'N(\d+)\s+(\d+)\s+\u00d8\s*(\d+(?:\.\d+)?)\s+C/\s*(\d+)',txt):
    mark,n,phi,spacing=match.groups();label_candidates=[l for l in parts if re.match(rf'N{mark}(?:\s|$)',l['text'].strip())];occ=sum(1 for m in re.finditer(rf'N{mark}(?:\s|$)',txt[:match.start()]));label=label_candidates[min(occ,len(label_candidates)-1)];x=(label['bbox'][0]+label['bbox'][2])/2;y=row['y'];possible=[d for d in black if d['x0']-4<=x<=d['x1']+4 and abs(d['y']-y)<13]
    if possible:
     seg=min(possible,key=lambda d:abs(d['y']-y));stirrups.append({'mark':'N'+mark,'count':int(n),'diameter_mm':float(phi),'spacing_cm':int(spacing),'legs':2,'x_start_common':round((seg['x0']-origin)/.5664/100,4),'x_end_common':round((seg['x1']-origin)/.5664/100,4),'source':{'pdf':file.name,'page':1,'row':txt,'segment_pdf':seg,'leg_interpretation':'closed rectangular stirrup depicted; 2 vertical legs'}})
  ALL[f'V{number}']={'pdf':file.name,'bbox':box,'origin_pdf_x':origin,'cross_x':cross,'lightblue_x':sorted(set(light)),'bars':bars,'stirrups':stirrups,'pending':['graphical-coordinate verification against explicit dimensions; uncoted ends remain geometric interpretation']}
  print(f'V{number}', 'bars',len(bars),'stirrups',[(b['mark'],b['diameter_mm'],b['spacing_cm'],b['x_start_common'],b['x_end_common']) for b in stirrups])
(OUT/'drawing_inventory.json').write_text(json.dumps(ALL,ensure_ascii=False,indent=2),encoding='utf8')
