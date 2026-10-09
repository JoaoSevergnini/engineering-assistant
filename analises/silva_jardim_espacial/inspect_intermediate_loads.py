from pathlib import Path
import json
s=Path(r'C:\TQS\TGD - SILVA JARDIM\24-212-TGD-SILVA JARDIM-R35\ESPACIAL');o=Path(r'\\srvmaster\PUBLICO\Joao Severgnini\Simon\engineering-assistant\analises\silva_jardim_espacial')
a=(s/'FOR0212.POR').read_bytes().decode('cp1252').splitlines()
i=next(i for i,l in enumerate(a) if l.startswith('CARREG'))
print('FIRST BLOCK',i+1,'\n'.join(a[i:i+35]))
for bar in [1605,1682,1684,1556]:
 hits=[]
 # Only scan first case's CARREG section, before the next CASO.
 end=next(j for j in range(i+1,len(a)) if a[j].startswith('CASO'))
 for j in range(i+1,end):
  tok=a[j].split()
  if tok and tok[0]==str(bar):hits.append((j+1,a[max(i,j-1):j+7]))
 print('BAR',bar,'matches',len(hits),'samples',hits[:3])
# Inspect full first block for record-key structure and attached records.
print('LAST BLOCK LINES','\n'.join(a[end-20:end]))
