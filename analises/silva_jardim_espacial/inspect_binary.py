from pathlib import Path
import struct,re,collections,json,zipfile,xml.etree.ElementTree as ET
s=Path(r'C:\TQS\TGD - SILVA JARDIM\24-212-TGD-SILVA JARDIM-R35\ESPACIAL');o=Path(r'\\srvmaster\PUBLICO\Joao Severgnini\Simon\engineering-assistant\analises\silva_jardim_espacial')
for name in ['FOR0212','PORTELS']:
 b=(s/(name+'.RSX')).read_bytes();h=struct.unpack('<15i',b[:60]);print(name,'header',h,'size',len(b),'expected',(h[12]+h[13]+h[14]),'nblocks',(len(b)-60)/(h[12]+h[13]+h[14]));print('dispnode1',struct.unpack_from('<6d',b,60));print('bar1',struct.unpack_from('<12d',b,60+h[12]));print('reaction1',struct.unpack_from('<6d',b,60+h[12]+h[13]));
 a=(s/(name+'.POR')).read_bytes().decode('cp1252').splitlines()
 cases=[(i+1,int(l.split()[1]),a[i+1].strip()) for i,l in enumerate(a) if l.startswith('CASO ')]
 comb=[(i+1,int(l.split()[1]),a[i+1].strip()) for i,l in enumerate(a) if l.startswith('COMBIN ')]
 print('cases',len(cases),'comb',len(comb),comb[0],comb[-1],'families',collections.Counter(l.split('/',1)[0].split(None,1)[1] for _,_,l in comb))
 for c in comb[:1]:i=c[0]-1;print('firstcomb','\n'.join(a[i:i+7]))
 print('envtail','\n'.join(a[-5:]))
(o/'rsx_structure_initial.json').write_text(json.dumps({'note':'Reconhecimento empírico; validar semântica por comparação com listagens e documentação.'},ensure_ascii=False),encoding='utf-8')
with zipfile.ZipFile(s/'PORLID2.XLSX') as z:
 ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
 print('XLSX sheets',z.read('xl/workbook.xml').decode()[:1700])
 strings=ET.fromstring(z.read('xl/sharedStrings.xml'));st=[''.join(si.itertext()) for si in strings]
 print('XLSX strings',st[:18])
for name in ['PORLIS2.LST','PORLID2.DAT','PORLID3.DAT']:
 a=(s/name).read_bytes().decode('cp1252').splitlines();print(name,'NUL',sum(l.count(chr(0)) for l in a),'vigaheading',[l for l in a if 'vigas' in l.lower()][:8])
