from pathlib import Path
import re,collections,json
s=Path(r'C:\TQS\TGD - SILVA JARDIM\24-212-TGD-SILVA JARDIM-R35\ESPACIAL');o=Path(r'\\srvmaster\PUBLICO\Joao Severgnini\Simon\engineering-assistant\analises\silva_jardim_espacial')
for name in ['FOR0212.Lst','PORTELS.Lst']:
 a=(s/name).read_bytes().decode('cp1252').splitlines();hh=[l for l in a if re.match(r'^-+[A-Z]',l)];print(name,len(a),'headings',len(hh));print(collections.Counter(re.sub(r'NC\.\s*\d+.*','NC',h.strip('- ')) for h in hh));print('cases',sorted(set(int(x) for l in hh for x in re.findall(r'NC\.\s*(\d+)',l))));print('bars mentions',[ (i+1,l) for i,l in enumerate(a) if re.search('BARRAS|DESLOCAMENTOS|ESFOR',l)][:8])
for name in ['FOR0212.POR','PORTELS.POR']:
 a=(s/name).read_bytes().decode('cp1252').splitlines();hs=[(i+1,l) for i,l in enumerate(a) if re.match('^(CASO |COMBIN |ENVOLT|GERAIS)',l)];print(name,'cases',sum(l.startswith('CASO ') for _,l in hs),'comb',sum(l.startswith('COMBIN ') for _,l in hs),'env',hs[-1]);print('firstcomb','\n'.join(a[next(i for i,l in enumerate(a) if l.startswith('COMBIN')):][:8]));print('tail','\n'.join(a[-15:]))
for name in ['PORLIS2.LST','PORFOR.LST','PORFORELS.LST']:
 a=(s/name).read_bytes().decode('cp1252').splitlines();print(name)
 for i,l in enumerate(a):
  if re.search('Esforços em vigas|Nós e barras|Barras nas|Piso.*TIPO|V601|Planta TIPO|Número de combina|Envoltória de carreg|Transferência de esforços',l):print(i+1,'\n'.join(a[max(0,i-1):i+8]))
for p in [Path(r'C:\TQSW'),Path(r'C:\TQS\EXEC'),Path(r'C:\TQSW\EXEC')]:print('INSTALL',p,p.exists())
