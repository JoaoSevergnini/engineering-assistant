"""Reprodução pontual dos casos e regressão, sem sobrescrever históricos."""
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT/'tools'/p) for p in ('reinforcement_checks','beam_model','beam_mapping','extrator_lst')] + [str(ROOT.parent/'concretopy')]
from floor_review import review_floor
from section_positions import fill_positions
import concretopy as api

def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def write(n,v): (OUT/n).write_text(json.dumps(v,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
def hashes():
    roots=[ROOT/'analises/silva_jardim_tipo',ROOT/'analises/etapa1_leitura_geometria',ROOT/'analises/etapa1_1_integracao',ROOT/'analises/verificacao_flexao_V607',ROOT.parent/'concretopy/concretopy',ROOT.parent/'arquivos']
    return {str(p):hashlib.sha256(p.read_bytes()).hexdigest() for r in roots for p in r.rglob('*') if p.is_file() and '__pycache__' not in p.parts}

before=hashes()
spec=read(ROOT/'analises/etapa1_1_integracao/real_replay_manifest.json')
spec['beams']=[b for b in spec['beams'] if b['beam_id'] in ('V611','V623')]
for b in spec['beams']:
    if b['beam_id']=='V611':
        b['jobs']=[dict(id='V611-transition-'+str(i),control='positive_flexure',span_id=1,interval_m=t['physical_interval_m'],inputs={}) for i,t in enumerate(b['form']['transitions'])]
write('entrada_v611_v623.json',spec)
result=review_floor(spec,api=api);write('resultado_v611_v623.json',result)
v611,v623=result['beams']
assert v623['documentary_review']['suspended'] and v623['documentary_review']['affected_marks']==['N2']
assert all(c['status']=='INCONCLUSIVE' and c['execution_state']=='NOT_EXECUTED' for c in v623['controls'])
assert next(p for p in v623['model']['documentary_reconciliation']['positions'] if p['mark']=='N2')['representations']
assert all('transition_resistant_method_not_implemented' in c['input_validation']['pending'] for c in v611['controls'] if c['job_id'].startswith('V611-transition'))

v607spec=read(ROOT/'analises/verificacao_flexao_V607/entrada.json')
v607=review_floor(v607spec,api=api);write('resultado_v607.json',v607)
old=read(ROOT/'analises/verificacao_flexao_V607/resultado.json')['beams'][0]['controls'][0]['result']['regions'][0]
new=v607['beams'][0]['controls'][0]['result']['regions'][0]
assert new['MRd_knm']==old['MRd_knm'] and new['utilization']==old['utilization']
assert v607['beams'][0]['controls'][0]['status']=='PASS'

model=read(ROOT/'analises/etapa1_leitura_geometria/V626_tqs_stage1.json')
raw=read(ROOT/'analises/silva_jardim_tipo/V626_tqs_raw.json')
form=read(ROOT/'analises/etapa1_1_integracao/V626_form_reviewed.json')
context={'1':{k:form['spans'][0][k] for k in ('orientation','physical_bounds')}}
try:
    fill_positions(model,raw,cantilever_contexts=context)
    raise AssertionError('Missing real cantilever series must not be positioned')
except ValueError as error:
    pending=str(error)
assert 'cantilever_force_series_unavailable' in pending
inventory=[]
for p in (ROOT/'analises/silva_jardim_tipo').glob('*_tqs_raw.json'):
    data=read(p)
    for row in data['categorias'].get('geometria',[]):
        if row['origem']['arquivo'].upper()=='VGESFS.LST' and any(t.endswith('B') and t[:-1].isdigit() for t in row.get('tokens',[])):
            inventory.append(dict(beam=p.stem.removesuffix('_tqs_raw'),record=row['origem'],tokens=row['tokens'],form_orientation_validated_in_this_run=p.stem.startswith('V626')))
write('balancos_reais.json',dict(V626=dict(context=context,pending=pending,
    VGESFS_geometry_length_m=model['beam']['spans'][0]['geometry']['length'],form_free_to_support_axis_m=.53,
    series_in_preserved_VGESFS=[dict(line=r['origem']['linha_inicial'],span=(r.get('normalizacao')or{}).get('vao_original')) for r in raw['categorias']['esforcos_ao_longo_dos_vaos'] if r['origem']['arquivo'].upper()=='VGESFS.LST'],
    structural_verdict=None),other_cantilever_candidates=inventory))

env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONIOENCODING='utf-8')
tests=[]
for suite in ('beam_model','extrator_lst','beam_mapping','reinforcement_checks'):
    cmd=[sys.executable,'-m','unittest','discover','-s','tools/'+suite,'-p','test_*.py','-q']
    p=subprocess.run(cmd,cwd=ROOT,env=env,capture_output=True,text=True,encoding='utf-8')
    tests.append(dict(suite=suite,command=cmd,exit_code=p.returncode,output=p.stdout+p.stderr))
    print(suite,p.returncode,flush=True)
write('testes.json',tests)
after=hashes();write('preservacao.json',dict(unchanged=before==after,count=len(before),changed=[p for p,v in before.items() if after.get(p)!=v]))
assert before==after and all(t['exit_code']==0 for t in tests)
write('resumo.json',dict(V607=dict(MRd_knm=new['MRd_knm'],utilization=new['utilization'],unchanged=True),
    V611=dict(regional_method_scope=v611['regional_method_scope'],structural_approval=None),
    V623=v623['documentary_review'],V626=dict(pending=pending,structural_approval=None)))
