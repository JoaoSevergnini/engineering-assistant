from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tmp/pdf_deps'))
sys.path.insert(0,str(ROOT/'tools/beam_model'))
from pdf_observations import extract_zones
p=Path(r'S:\PROJETOS EM EXECUÇÃO\24-212-TGD-SILVA JARDIM-POA-RS\APOIO\JOÃO\TIPO\051-SJ-EST-LO-06303-VIG-TIP-R00.PDF')
zones=[dict(id='V623-TABLE',page=0,bbox=[2370,241,2580,283],view='STEEL_SCHEDULE',marks=['N1','N2','N3','N4'],quantity_scope='POSITION_TOTAL',integrity='INTACT',columns=['mark','diameter_mm','quantity','nominal_length_cm','total_length_cm'])]
r=extract_zones(p,zones)
Path(__file__).with_name('V623_pdf_table_observations.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
n2=[o for o in r['observations'] if o['mark']=='N2']
assert len(n2)==1 and (n2[0]['quantity'],n2[0]['diameter_mm'],n2[0]['nominal_length_cm'])==(4,16,464)
print(json.dumps(dict(observations=len(r['observations']),N2=n2[0]['mark'],quantity=n2[0]['quantity'],diameter_mm=n2[0]['diameter_mm'],length_cm=n2[0]['nominal_length_cm'])))
