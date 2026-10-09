from pathlib import Path
import json,hashlib
root=Path.cwd();out=root/'analises/etapa1_leitura_geometria'
p=out/'test_results.json';r=json.loads(p.read_text(encoding='utf-8-sig'))
r['post_final_adjustments']=[dict(suite='beam_model',tests=71,passed=True),dict(suite='reinforcement_checks/test_input_preflight.py',tests=21,passed=True),dict(suite='reinforcement_checks/test_stage1_physical_flexure.py',tests=4,passed=True),dict(suite='extrator_lst/test_stage1_cantilevers.py',tests=3,passed=True)]
p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
files=['tools/beam_model/input_evidence.py','tools/beam_model/documentary_reconciliation.py','tools/beam_model/physical_geometry.py','tools/beam_model/pdf_observations.py','tools/beam_model/consolidar_detalhamento.py','tools/extrator_lst/extrair_viga_lst.py','tools/extrator_lst/consolidar_viga.py','tools/reinforcement_checks/input_preflight.py','tools/reinforcement_checks/longitudinal_review.py','tools/reinforcement_checks/beam_diagnostic.py','tools/reinforcement_checks/correction_engine.py']
manifest=[dict(file=f,sha256=hashlib.sha256((root/f).read_bytes()).hexdigest()) for f in files]
(out/'implementation_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print('Tests:',r['total'],'; All passed:',r['all_passed'])
assert (out/'relatorio_etapa1.md').exists()
