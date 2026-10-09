from pathlib import Path
import collections,json,re,datetime
p=Path(r'C:\TQS\TGD - SILVA JARDIM\24-212-TGD-SILVA JARDIM-R35\ESPACIAL')
for n in ['CARDWG2.LST','CRITPOR.DAT','PORLID2.DAT']:
 a=(p/n).read_bytes().decode('cp1252',errors='replace').splitlines()
 if n=='CARDWG2.LST':print('CARDWG tags',collections.Counter(l.split(',')[0] for l in a));print('plantas',[l for l in a if l.startswith('PLANTA')][5:11])
 if n=='CRITPOR.DAT':print('CRIT', '\n'.join(a[:12]));print('tail', '\n'.join(a[-8:]))
 if n=='PORLID2.DAT':print('PORLID last','\n'.join(a[-22:]));print('PORLID aroundcase101','\n'.join(a[294:310]))
