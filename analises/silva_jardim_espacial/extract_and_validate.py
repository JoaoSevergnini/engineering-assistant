from pathlib import Path
import json,csv,re,struct,hashlib,datetime,collections,math
ROOT=Path(r'\\srvmaster\PUBLICO\Joao Severgnini\Simon\engineering-assistant');OUT=ROOT/'analises/silva_jardim_espacial';SRC=Path(r'C:\TQS\TGD - SILVA JARDIM\24-212-TGD-SILVA JARDIM-R35\ESPACIAL')
def txt(name):return (SRC/name).read_bytes().decode('cp1252',errors='replace').splitlines()
def save(name,data):(OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
def csvsave(name,rs):
 with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rs[0]),delimiter=';');w.writeheader();w.writerows(rs)
inv=json.loads((OUT/'inventario.json').read_text(encoding='utf-8'))
for r in inv:
 f=SRC/r['file'];r['modified']=datetime.datetime.fromtimestamp(f.stat().st_mtime).isoformat(timespec='seconds');r['sha256']=hashlib.sha256(f.read_bytes()).hexdigest()
save('inventario_com_hashes.json',inv)
MAP=[];floor=None
for ln,l in enumerate(txt('PORFOR.LST'),1):
 m=re.search(r'Viga\s+Barras - Piso\s+(\d+)',l)
 if m:floor=int(m[1])
 m=re.match(r'^(V\d+)\s+([\d ]+)\s*$',l)
 if m and floor is not None:
  for order,b in enumerate(m[2].split(),1):MAP.append(dict(piso=floor,viga=m[1],ordem_na_lista=order,barra=int(b),fonte='PORFOR.LST',linha=ln))
csvsave('mapa_vigas_barras.csv',MAP)
DATA={};REACTIONS=[];COMBS=[];PILOT=[];VALID=[]
for name in ['FOR0212','PORTELS']:
 a=txt(name+'.POR');nodes={};bars={};cases=[];comb=[];env=[]
 for i,l in enumerate(a):
  if l.startswith('NOS '):
   n=int(l.split()[1]);nodes={int(q.split()[0]):list(map(float,q.split()[1:4])) for q in a[i+1:i+1+n]}
  if l.startswith('BARRAS '):
   n=int(l.split()[1]);bars={int(q.split()[0]):{'nodes':[int(x) for x in q.split()[1:3]],'line':i+j+2,'original':q} for j,q in enumerate(a[i+1:i+1+n])}
  if l.startswith('CASO '):
   caseid=int(l.split()[1]);title=a[i+1].split(None,1)[1].strip();cases.append(dict(modelo=name,id=caseid,tipo='CASO',titulo=title,linha=i+1,componentes=[]))
  if l.startswith('COMBIN '):
   caseid=int(l.split()[1]);parts=a[i+1].split(None,1);n=int(parts[0]);title=parts[1].strip();components=[{'case':int(q.split()[0]),'factor':float(q.split()[1]),'line':i+j+3} for j,q in enumerate(a[i+2:i+2+n])]
   comb.append(dict(modelo=name,id=caseid,tipo='COMBINACAO',titulo=title,linha=i+1,componentes=components,cabecalho_original=l))
  if l.startswith('ENVOLT'):
   n=int(l.split()[1]);env=[int(q.strip()) for q in a[i+1:i+1+n]]
 catalog=cases+comb;assert [r['id'] for r in catalog]==list(range(1,len(catalog)+1))
 buf=(SRC/(name+'.RSX')).read_bytes();h=struct.unpack('<15i',buf[:60]);step=sum(h[11:14]);assert h[1]==len(nodes) and h[2]==len(bars);assert len(buf)==60+len(catalog)*step
 def values(case,b):return struct.unpack_from('<12d',buf,60+(case-1)*step+h[11]+(b-1)*96)
 # Comparação das reações binárias com todas as tabelas disponíveis, incluindo CBNL.
 obs={};context=None
 for ln,l in enumerate(txt(name+'.Lst'),1):
  if 'REACOES DOS APOIOS' in l:
   m=re.search(r'NC\.\s*(\d+)',l);m2=re.search(r'(?:CBNL|CB\.)\s*(\d+)',l)
   context=int(m[1]) if m else 20+int(m2[1]) if m2 else None
  elif context:
   m=re.match(r'^\s*(\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s*$',l)
   if m:obs[(context,int(m[1]))]=(list(map(float,m.groups()[1:])),ln)
 diffs=[]
 for (case,node),(published,ln) in obs.items():
  assert 1<=case<=len(catalog) and 1<=node<=h[4]
  raw=struct.unpack_from('<6d',buf,60+(case-1)*step+h[11]+h[12]+(node-1)*48);dif=max(abs(x-y) for x,y in zip(raw,published));diffs.append(dif)
  REACTIONS.append(dict(modelo=name,caso=case,titulo=catalog[case-1]['titulo'],no=node,FX_tf=raw[0],FY_tf=raw[1],FZ_tf=raw[2],MX_tfm=raw[3],MY_tfm=raw[4],MZ_tfm=raw[5],linha_lst=ln,desvio_max_arredondamento=dif))
 assert len(obs)==len(catalog)*h[4],(name,len(obs));assert max(diffs)<.00501
 val=dict(modelo=name,header=list(h),record_bytes=step,registros=len(catalog),nos=len(nodes),barras=len(bars),apoios=h[4],comparacoes_reacoes=len(obs)*6,max_desvio_reacoes=max(diffs),arquivo_completo_sem_resto=True)
 # Comprovação do significado N/My/Mz usando todos os pilares da listagem nominal (caso 1).
 if name=='FOR0212':
  lines=txt('PORLIS2.LST');start=next(i for i,l in enumerate(lines) if l.startswith('Esforços em pilares'));end=len(lines);pd=[];pcount=0
  for l in lines[start:end]:
   tok=re.sub(r'^\s*\d+ø\s*','',l).split()
   if len(tok)!=11:continue
   try:
    floor,b,c=map(int,tok[:3]);v=list(map(float,tok[3:]));raw=values(c,b)
   except ValueError:continue
   expected=[raw[4],raw[5],raw[0],-raw[10],-raw[11],-raw[6]];published=[v[0],v[1],v[2],v[4],v[5],v[6]]
   pd.extend(abs(x-y) for x,y in zip(expected,published));pcount+=1
  assert pd and max(pd)<.00501;val.update(lances_pilares_comparados=pcount,componentes_N_My_Mz_comparados=len(pd),max_desvio_pilares=max(pd),sinal_fim='A listagem de pilares inverte os componentes finais da ação nodal da barra.')
 # Piloto de esforços em vigas do TIPO, piso físico 5. Apenas fins; sem interpolar diagrama ou majorar.
 for m in MAP:
  if m['piso']!=5 or m['viga'] not in ['V606','V623']:continue
  b=m['barra'];nd=bars[b]['nodes']
  for c in catalog:
   raw=values(c['id'],b);assert all(math.isfinite(v) for v in raw)
   r=dict(modelo=name,piso=5,cota_m=35.28,viga=m['viga'],barra=b,no_i=nd[0],no_f=nd[1],caso=c['id'],tipo=c['tipo'],titulo=c['titulo'])
   r.update({f'C{k+1}_{"tf" if k%6<3 else "tfm"}':v for k,v in enumerate(raw)});PILOT.append(r)
 for c in catalog:COMBS.append(dict(modelo=name,id=c['id'],tipo=c['tipo'],titulo=c['titulo'],linha_por=c['linha'],componentes=' + '.join(f"{z['factor']:g}*caso{z['case']}" for z in c['componentes'])))
 DATA[name]=dict(catalog=catalog,envelope_ids=env,nodes=nodes,bars=bars,validation=val);VALID.append(val)
save('modelo_e_combinacoes.json',DATA);save('validacao_extracao_rsx.json',VALID)
csvsave('catalogo_casos_combinacoes.csv',COMBS);csvsave('reacoes_por_caso.csv',REACTIONS);csvsave('piloto_esforcos_v606_v623_piso5.csv',PILOT)
print('VALIDACAO',json.dumps(VALID,ensure_ascii=False));print('PILOTO',len(PILOT),'linhas','MAPA',len(MAP),'associações')


