from pathlib import Path
import re,collections
s=Path(r'C:\TQS\TGD - SILVA JARDIM\24-212-TGD-SILVA JARDIM-R35\ESPACIAL')
for name in ['FOR0212.POR','PORTELS.POR','FOR0212.Lst','PORTELS.Lst','PORFOR.LST','PORFORELS.LST','PORLIS2.LST','PORALF.LST','CARRPOR.DAT','CARDWG2.LST','FOR0212.BPq','MENAVI.LST']:
 a=(s/name).read_bytes().decode('cp1252',errors='replace').splitlines();print('\nFILE',name,len(a),'lines')
 if name.endswith('.POR'):
  heads=[(i+1,l[:150]) for i,l in enumerate(a) if re.match(r'^[A-Z][A-Z0-9_ -]{1,15}',l)]
  print('HEADS',heads[:35],heads[-15:]);
  for i,l in enumerate(a):
   if re.match(r'^(BARRAS|COMB|CASO|SECO|MATER|CARG|TIT|FIM|PISO|VIGA|PILAR|PAV)',l):print(i+1,'\n'.join(a[i:i+4])[:450])
 elif name.endswith('.Lst'):
  hh=[l.strip('- ') for l in a if re.match(r'^-+[A-Z]',l)]
  print('SECTIONS',collections.Counter(re.sub(r'NC\.\s*\d+.*','NC',h) for h in hh))
  print('END','\n'.join(a[-20:]))
 else:
  print('\n'.join(a[:32]))
  if name in ['PORLIS2.LST','PORFOR.LST','PORFORELS.LST']:print('LATE','\n'.join(a[len(a)//2:len(a)//2+16]))
