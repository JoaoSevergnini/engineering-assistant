from pathlib import Path
import struct,re
s=Path(r'C:\TQS\TGD - SILVA JARDIM\24-212-TGD-SILVA JARDIM-R35\ESPACIAL')
a=(s/'PORLIS2.LST').read_bytes().decode('cp1252').splitlines();i=a.index('P1');print('\n'.join(a[i:i+14]))
p=(s/'FOR0212.POR').read_bytes().decode('cp1252').splitlines();i=next(i for i,l in enumerate(p) if l.startswith('BARRAS'));bars={int(l.split()[0]):l for l in p[i+1:i+3758]};b=(s/'FOR0212.RSX').read_bytes();h=struct.unpack('<15i',b[:60])
for n in [276,1556,1605,1606,1669]:
 print('BAR',n,bars[n]);print('RSX',struct.unpack_from('<12d',b,60+h[11]+(n-1)*96))
a=(s/'PORFOR.LST').read_bytes().decode('cp1252').splitlines()
print('\n'.join(a[125:151]));print('floor5', '\n'.join(a[1964:2001]))
print('CBNLfirst',next(l for l in (s/'FOR0212.Lst').read_bytes().decode('cp1252').splitlines() if 'CBNL' in l))
