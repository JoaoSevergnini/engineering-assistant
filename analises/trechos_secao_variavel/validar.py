"""Casos reais e sintéticos separados; resultados novos, históricos imutáveis."""
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT/'tools'/p) for p in ('reinforcement_checks','beam_model','beam_mapping','extrator_lst')]+[str(ROOT.parent/'concretopy')]
from floor_review import review_floor
from input_evidence import fact
from materials import documented_fields, interpret_steel
from test_floor_review import FloorTests
from test_suspension_review import connection
import concretopy as api

def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def compact(v):
    # Remove only echoed source trees; the exact input and API receipts remain separate.
    omit={'model','registered_spans','diagnosis','provenance','base_points','series','mapping_provenance','local_context','context'}
    if isinstance(v,dict):return {k:compact(x) for k,x in v.items() if k not in omit}
    if isinstance(v,list):return [compact(x) for x in v]
    return v
def write(n,v):
    if n.startswith(('resultado_','sintetico_')) or n=='resumo.json':
        v=dict(traceability=dict(inputs='entrada_v611.json / entrada_sintetico_*.json / ../verificacao_flexao_V607/entrada.json',
            note='Árvores documentais repetidas omitidas nesta exportação; entradas preservam fontes, fatos e séries integrais.'),result=compact(v))
    (OUT/n).write_text(json.dumps(v,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
def hashes():
    roots=[ROOT/'analises'/p for p in ('silva_jardim_tipo','etapa1_leitura_geometria','etapa1_1_integracao','verificacao_flexao_V607','ajustes_v611_v623_v626')]+[ROOT.parent/'concretopy/concretopy',ROOT.parent/'arquivos']
    return {str(p):hashlib.sha256(p.read_bytes()).hexdigest() for r in roots for p in r.rglob('*') if p.is_file() and '__pycache__' not in p.parts}

before=hashes()
spec=read(ROOT/'analises/etapa1_1_integracao/real_replay_manifest.json')
spec['floor']='TIPO-trechos-V611';spec['beams']=[b for b in spec['beams'] if b['beam_id']=='V611']
b=spec['beams'][0]
raw=read(ROOT/'analises/silva_jardim_tipo/V611_tqs_raw.json')
fck,fc_source=documented_fields(raw,'fck','MPa')
gf,gf_source=documented_fields(raw,'gamaf')
gc,gc_source=documented_fields(raw,'gamac')
steel=interpret_steel(raw)
material_source=dict(extraction='analises/silva_jardim_tipo/V611_tqs_raw.json',fck=fc_source,gamma_f=gf_source,gamma_c=gc_source,steel=steel)
b['context']=dict(fck_mpa=fck,fyk_mpa=steel['derived_fyk_mpa'],gamma_f=gf,gamma_c=gc,gamma_s=1.15,
    horizontal=True,sliding_formwork=False,longitudinal_provenance=material_source,
    gamma_s_provenance=dict(origin='OFFICE_STANDARD',reference='mesma convenção explícita da regressão V607; não extraído do LST'))
b['control_inputs']={c:dict(materials=fact(material_source,state='DOCUMENTED_CONFIRMED',provenance=[material_source])) for c in ('positive_flexure','negative_flexure','shear','suspension')}
domains=[]
for i,s in enumerate(b['form']['segments'][:3],1):
    s['detail_geometry']=dict(cover_cm=fact(2.5,state='DOCUMENTED_CONFIRMED',unit='cm',provenance=[dict(extraction='analises/silva_jardim_tipo/V611_tqs.json',pointer='/beam/cover/general',original_m=.025)]),
        stirrup_diameter_mm=fact(5,state='DOCUMENTED_CONFIRMED',unit='mm',provenance=[dict(extraction='analises/silva_jardim_tipo/V611_detail.txt',image='analises/silva_jardim_tipo/V611_detail.png',marks=['N7','N8'])]))
    ends=[s['fields'][k]['fact'] for k in ('x_start_m','x_end_m')]
    domains.append(dict(span_id=i,interval_m=fact([x['value'] for x in ends],state='DOCUMENTED_CONFIRMED',unit='m',provenance=[dict(faces=ends,reference='vão livre; não atravessar apoio de geometria pendente')])) )
regions=[]
for name,a,z,spacing in [('N7-1',0,2.82,14),('N7-2',3.52,3.88,10),('N8',3.88,5.43,8),('N7-3',5.43,6.19,10),('N7-4',6.89,9.31,14)]:
    regions.append(dict(id=name,interval_m=[a,z],diameter_mm=5,spacing_cm=spacing,legs=2,physical_function='CONVENTIONAL_SHEAR_STIRRUP',
        source=dict(extraction='analises/silva_jardim_tipo/V611_detail.txt',image='analises/silva_jardim_tipo/V611_detail.png',basis='comprimentos impressos 282;36+155+76=267;242 cm, a partir das faces dos vãos livres da forma; não prova transições')))
b['section_checks']=dict(domains=domains,drawn_stirrup_regions=regions)
write('entrada_v611.json',spec)
real=review_floor(spec,api=api);write('resultado_v611.json',real)
sections=real['beams'][0]['section_checks']['sections']
assert len(sections)==3 and all(s['shear_selection']['complete'] for s in sections)
assert all(s['al']['execution_state']=='NOT_EXECUTED' for s in sections)

v607spec=read(ROOT/'analises/verificacao_flexao_V607/entrada.json')
v607=review_floor(v607spec,api=api);write('resultado_v607.json',v607)
old=read(ROOT/'analises/verificacao_flexao_V607/resultado.json')['beams'][0]['controls'][0]['result']['regions'][0]
new=v607['beams'][0]['controls'][0]['result']['regions'][0]
assert new['MRd_knm']==old['MRd_knm'] and new['utilization']==old['utilization']

synthetic={}
for name,bounds,heights in [('dois_trechos',(0,2,4),(57,47)),('tres_trechos',(0,1.5,3,4),(57,47,67)),('suspensao',(0,2,4),(57,47))]:
    fixture=FloorTests();fixture.setUp()
    try:
        fixture.section_case(bounds,heights)
        if name=='suspensao':
            for series in fixture.case['positioned_tqs']['beam']['spans'][0]['internal_forces']:
                if series['quantity']=='shear':series['values']=[30 if series['envelope']=='max' else -20]*6
            c=connection(20);c['receiving_beam_id']=fixture.case['beam_id'];c['reaction']['receiving_beam_id']=fixture.case['beam_id']
            fixture.case['section_checks'].update(suspension_connections=[c],
                suspension_inventory_source={'fixture':'complete synthetic supported-beam inventory'})
        result=fixture.run_case(api=api)
        write('entrada_sintetico_'+name+'.json',dict(case_type='SYNTHETIC',spec=fixture.spec))
        if name=='suspensao':assert result['section_checks']['suspension'][0]['execution_state']=='EXECUTED_COMPLETE'
        write('sintetico_'+name+'.json',dict(case_type='SYNTHETIC',result=result))
        synthetic[name]=result['section_checks']
    finally:fixture.doCleanups()

tests=read(OUT/'testes.json') if '--reuse-tests' in sys.argv else []
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONIOENCODING='utf-8')
for suite in (() if '--reuse-tests' in sys.argv else ('beam_model','extrator_lst','beam_mapping','reinforcement_checks')):
    cmd=[sys.executable,'-m','unittest','discover','-s','tools/'+suite,'-p','test_*.py','-q']
    p=subprocess.run(cmd,cwd=ROOT,env=env,capture_output=True,text=True,encoding='utf-8')
    tests.append(dict(suite=suite,command=cmd,exit_code=p.returncode,output=p.stdout+p.stderr))
    print(suite,p.returncode,flush=True)
write('testes.json',tests)
after=hashes();write('preservacao.json',dict(unchanged=before==after,count=len(before),changed=[p for p,v in before.items() if after.get(p)!=v]))
assert before==after and all(t['exit_code']==0 for t in tests)
write('resumo.json',dict(V607=dict(MRd_knm=new['MRd_knm'],utilization=new['utilization'],unchanged=True),
    V611=[dict(segment_id=s['segment_id'],physical_interval_m=s['physical_interval_m'],Vk=s['shear_selection']['governing'],moments=s['physical_moment_extrema'],al=s['al'],depth=s['effective_depth']) for s in sections],
    synthetic=synthetic))
