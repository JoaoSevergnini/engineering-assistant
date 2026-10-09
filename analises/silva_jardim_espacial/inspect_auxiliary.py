from pathlib import Path
import re,html,zipfile,xml.etree.ElementTree as ET,datetime,json
p=Path(r'C:\TQS\TGD - SILVA JARDIM\24-212-TGD-SILVA JARDIM-R35\ESPACIAL')
for n in ['CARRPOR.DAT','CRITPOR.DAT','PORLID2.DAT','PILAR.LST','CARPIL.LST','CONTPOR.DAT']:
 a=(p/n).read_bytes().decode('cp1252',errors='replace').splitlines(); print('\n',n)
 if n=='PORLID2.DAT':print('\n'.join(a[442:480]));print('end','\n'.join(a[-20:]))
 elif n=='CARRPOR.DAT':
  for i,l in enumerate(a):
   if re.search('ombina|gras|Número de grupos|Tipo de combinação',l): print(i+1,l)
 elif n=='CRITPOR.DAT':print('\n'.join(a[:30]));print('\n'.join(l for l in a if re.search('norma|model|Gama|transfer|FCK',l,re.I)))
 else:print('\n'.join(a[:18]))
for n in ['RESDES.HTM','PORALF.HTM','PGLOERR.HTM']:
 a=(p/n).read_bytes().decode('cp1252',errors='replace');a=re.sub(r'<(script|style)\b.*?</\1>','',a,flags=re.S|re.I);a=html.unescape(re.sub('<[^>]+>',' ',a));a=re.sub(r'\s+',' ',a); print('\nHTML',n,a[:1700]); print('fields',list(dict.fromkeys(re.findall(r'.{0,35}(?:[Ee]rro|[Aa]viso|[Ee]sforço|[Dd]eslocamento|[Pp]ilar|[Cc]ombinação|[Mm]odelo).{0,90}',a)))[:8])
n='PORLID2.XLSX'
with zipfile.ZipFile(p/n) as z:
 ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'};st=[''.join(t.itertext()) for t in ET.fromstring(z.read('xl/sharedStrings.xml'))];sheet=ET.fromstring(z.read('xl/worksheets/sheet1.xml'));print('XLSXdim',sheet.find('m:dimension',ns).attrib,'date',datetime.datetime.fromtimestamp((p/n).stat().st_mtime));print('groups',[x for x in st if 'Grupo ' in x]);print('firstrows',[[st[int(c.find('m:v',ns).text)] if c.get('t')=='s' else (c.find('m:v',ns).text if c.find('m:v',ns) is not None else '') for c in row] for row in sheet.findall('m:sheetData/m:row',ns)[:5]])
print('E3Dlast',sorted([(f.stat().st_mtime,f.name,f.read_bytes()[:35]) for f in p.glob('*.E3D')])[-1])
