import json,math,re,statistics
from pathlib import Path
p=Path(r'P:\Joao Severgnini\Simon\engineering-assistant\analises\atp_s07_lajes_terreo');new=json.loads((p/'ocorrencias_extraidas.json').read_text(encoding='utf8'));old=json.loads((p/'ocorrencias_antes_conciliacao_completa.json').read_text(encoding='utf8'));manual=json.loads((p/'conferencias_visuais_locais.json').read_text(encoding='utf8'));oldmap={o['id']:o for o in old};applied=[]
for l in manual:
 prev=oldmap[l['id']];m=next((o for o in new if o['sheet']==prev['sheet'] and math.dist(o['label_rect'][:2],prev['label_rect'][:2])<.1),None)
 if not m:continue
 for k in ['mark','spacing_cm','region_pdf']:
  if k in l['changes']:m[k]=l['changes'][k]
 if 'region_pdf' in l['changes']:m['bar_rotation']=prev['bar_rotation'];m['association']=prev['association'];m['geometry_status']=prev['geometry_status']
 if m['spacing_cm']:m['As_individual_cm2_m']=math.pi*(m['diameter_mm']/10)**2/4*100/m['spacing_cm']
 applied.append(dict(id=m['id'],previous_id=l['id'],changes=l['changes']))
local=[o for o in new if o['sheet']=='7305' and 685<o['label_rect'][0]<705 and o['label_rect'][1]>1540];new=[o for o in new if o not in local]
tables=json.loads((p/'tabelas_aco_extraidas.json').read_text(encoding='utf8'));corr=[]
for o in new:
 mm=re.search(r'C=(\d+(?:\.\d+)?)',o['top']) or re.search(r'C=(\d+(?:\.\d+)?)',o['bottom'])
 if not mm:continue
 L=float(mm[1]);tab=tables[o['sheet']];row=next((t for t in tab if t['mark']==o['mark']),None)
 if row and row['diameter_mm']==o['diameter_mm'] and abs(row['C_cm']-L)<1:continue
 candidates=[t for t in tab if t['diameter_mm']==o['diameter_mm'] and abs(t['C_cm']-L)<1]
 if len(candidates)==1:corr.append(dict(id=o['id'],previous=o['mark'],corrected=candidates[0]['mark'],C_cm=L));o['mark']=candidates[0]['mark']
(p/'notas_armaduras_localizadas_furos.json').write_text(json.dumps(local,indent=2),encoding='utf8');(p/'ocorrencias_extraidas.json').write_text(json.dumps(new,indent=2,ensure_ascii=False),encoding='utf8');(p/'conferencias_visuais_locais_vigentes.json').write_text(json.dumps(applied,indent=2),encoding='utf8');(p/'conciliacao_marcas_final.json').write_text(json.dumps(corr,indent=2),encoding='utf8')
print('occ',len(new),'sp',sum(o['spacing_cm'] is not None for o in new),'pending',[(o['id'],o['top']) for o in new if o['spacing_cm'] and not o['region_pdf']])
# Independent documentary screen: distribution span / spacing / printed count.
scales={};flags=[]
for n in tables:
 vals=[]
 for o in new:
  if o['sheet']==n and o['bar_candidates'] and 'C=1200' in o['top']:
   ll,yy,rr=o['bar_candidates'][0];vals.append(1200/(rr-ll))
 scales[n]=statistics.median(vals) if vals else (2.645833333 if int(n)<7305 else 2.4)
for o in new:
 if not o['region_pdf'] or not o['spacing_cm']:continue
 q=re.match(r'(\d+)N',o['top']);r=o['region_pdf']
 if not q or int(q[1])<5:continue
 q=int(q[1]);length=(r[3]-r[1] if o['bar_rotation']==0 else r[2]-r[0])*scales[o['sheet']];pred=length/o['spacing_cm'];ratio=pred/q
 if abs(ratio-1)>.16:flags.append(dict(id=o['id'],mark=o['mark'],printed_count=q,distribution_pitch_count=pred,ratio=ratio,region=r,top=o['top']))
(p/'triagem_quantidade_faixa.json').write_text(json.dumps(dict(scales=scales,flags=flags),indent=2),encoding='utf8');print('scales',scales,'flags',len(flags));print([(f['id'],f['mark'],round(f['ratio'],2)) for f in flags])
