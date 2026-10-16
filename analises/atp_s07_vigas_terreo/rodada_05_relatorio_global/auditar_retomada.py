from pathlib import Path
import json,hashlib,re
from pypdf import PdfReader
import pypdfium2 as pdfium
O=Path(r'\\srvmaster\PUBLICO\Joao Severgnini\Simon\engineering-assistant\analises\atp_s07_vigas_terreo\rodada_05_relatorio_global');D=json.loads((O/'verificacoes_globais_concretopy.json').read_text(encoding='utf8'));F=json.loads((O/'inventario_fontes_atual.json').read_text(encoding='utf8'));audit={'sources':[]}
for f in F:
 p=Path(f.get('snapshot_path',f['path']));expected=f.get('snapshot_sha256',f.get('sha256_current',f['sha256']));actual=hashlib.sha256(p.read_bytes()).hexdigest();audit['sources'].append({'sheet':f['prancha'],'unchanged':actual==expected,'sha256':actual})
T=json.loads((O/'tqs_operacional_atual.json').read_text(encoding='utf8'));tp=Path(T['V1']['source']);audit['model_unchanged']=hashlib.sha256(tp.read_bytes()).hexdigest()==D['source_model_sha256'];assert audit['model_unchanged'];assert all(q['unchanged'] for q in audit['sources']),audit['sources']
md=(O/'relatorio_global_vigas_S07.md').read_text(encoding='utf8');audit['50_beam_sheets']=len(re.findall(r'^### V\d+\s*$',md,re.M))==50;assert audit['50_beam_sheets'];audit['intervals']=len(D['results']);assert audit['intervals']==95
pdf=PdfReader(O/'relatorio_global_vigas_S07.pdf');audit['pdf_pages']=len(pdf.pages);audit['pdf_sha256']=hashlib.sha256((O/'relatorio_global_vigas_S07.pdf').read_bytes()).hexdigest();audit['positive_fail_beams']=sorted({x['beam_id'] for x in D['results'] if x['positive'].get('regional_capacity_passes',x['positive']['scenarios'][0]['capacity_passes']) is False},key=lambda b:int(b[1:]));audit['shear_fail_beams']=sorted({x['beam_id'] for x in D['results'] if any(q['scenarios'][0]['adopted_area_passes'] is False for q in x['shear'])},key=lambda b:int(b[1:]));assert len(audit['positive_fail_beams'])==8,audit
texts=[p.extract_text() for p in pdf.pages];targets={0,len(pdf.pages)-1}
for b in ['V12','V13','V24','V49','V50']:
 targets.update(i for i,t in enumerate(texts) if re.search(r'(?m)^'+b+r'\s*$',t))
for i,t in enumerate(texts):
 if 'Ligações entre vigas' in t or 'DISTRIBUICAO UNIFORME NAO ATENDE' in t:targets.add(i)
renderer=pdfium.PdfDocument(str(O/'relatorio_global_vigas_S07.pdf'))
for i in sorted(targets):renderer[i].render(scale=1.3).to_pil().save(O/'evidencias'/('revisao_retomada_pagina_'+str(i+1)+'.png'))
audit['rendered_pages']=[i+1 for i in sorted(targets)];(O/'auditoria_retomada.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf8')
section=md.split('## 7.')[1].split('## 8.')[0];(O/'pendencias_verificacao.md').write_text('# ATP S07 - Pendencias da revisao retomada\n\nEmissao16/10/2026. Nao representa aprovacao global.\n\n## 7.'+section,encoding='utf8')
print(json.dumps(audit,ensure_ascii=True))
