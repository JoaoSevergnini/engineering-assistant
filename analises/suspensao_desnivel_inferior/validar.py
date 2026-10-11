"""Reprodução separada de suspensão por desnível inferior; sem editar históricos."""
import hashlib,json,os,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT/'tools'/p) for p in ('reinforcement_checks','beam_model','beam_mapping','extrator_lst')]+[str(ROOT.parent/'concretopy')]
from floor_review import review_floor
from test_bottom_step_suspension import BottomStepTests,proved
import concretopy as api

def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(n,v):(OUT/n).write_text(json.dumps(v,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
def compact(v):
 if isinstance(v,dict):return {k:compact(x) for k,x in v.items() if k not in ('provenance','series','base_points','model','registered_spans','diagnosis','local_context','context')}
 if isinstance(v,list):return [compact(x) for x in v]
 return v
def hashes():
 roots=[ROOT/'analises'/p for p in ('silva_jardim_tipo','etapa1_leitura_geometria','etapa1_1_integracao','verificacao_flexao_V607','ajustes_v611_v623_v626','trechos_secao_variavel')]+[ROOT.parent/'concretopy/concretopy',ROOT.parent/'arquivos']
 return {str(p):hashlib.sha256(p.read_bytes()).hexdigest() for r in roots for p in r.rglob('*') if p.is_file() and '__pycache__' not in p.parts}

before=hashes()
real_input=read(ROOT/'analises/trechos_secao_variavel/entrada_v611.json')
write('entrada_v611.json',real_input)
real=review_floor(real_input,api=api)
steps=real['beams'][0]['section_checks']['bottom_step_suspension']
assert [s['classification']['suspended_side'] for s in steps]==['LEFT','RIGHT']
assert all(s['execution_state']=='NOT_EXECUTED' for s in steps)
write('v611.json',dict(case_type='REAL',input='entrada_v611.json',transitions=compact(steps)))

cases={}
for name,kwargs in [('fundos_coincidentes',dict(left_bottom=0,right_bottom=0)),('fundo_baixo_esquerda',{}),('fundo_baixo_direita',dict(left_bottom=10,right_bottom=0)),('altura_67',dict(heights=(67,47))),('insuficiente',dict(spacing=20)),('extensao_nao_comprovada',{}),('niveis_ausentes',{}),('salto_cortante',{})]:
 test=BottomStepTests();test.setUp()
 try:
  archive=Path(test.fixture.spec['sources']['form']['extraction_archive'])
  persistent=OUT/'synthetic_extraction.json';persistent.write_bytes(archive.read_bytes())
  for source in test.fixture.spec['sources'].values():source['extraction_archive']=str(persistent)
  test.setup_step(**kwargs)
  if name=='extensao_nao_comprovada':test.case['section_checks']['drawn_stirrup_regions'][0]['position_state']='ENGINEERING_ASSUMPTION'
  if name=='niveis_ausentes':test.case['form']['segments'][0]['fields'].pop('bottom_level_cm')
  if name=='salto_cortante':
   test.case['section_checks']['domains'][0]['discontinuities_m']=[proved(2,'m')]
   test.case['section_checks']['effective_depths']={'G1':proved(53.07,'cm'),'G2':proved(43.07,'cm')}
   test.case['section_checks']['height_change_transitions']=[dict(left_segment_id='G1',right_segment_id='G2',shear_sides={'LEFT':{'max':proved(30,'kN'),'min':proved(-20,'kN')},'RIGHT':{'max':proved(200,'kN'),'min':proved(-100,'kN')}})]
  write('entrada_'+name+'.json',dict(case_type='SYNTHETIC',spec=test.fixture.spec))
  cases[name]=compact(test.step())
 finally:test.doCleanups()
write('sinteticos.json',dict(case_type='SYNTHETIC',input_files='entrada_<nome>.json',cases=cases))

old=read(ROOT/'analises/verificacao_flexao_V607/resultado.json')['beams'][0]['controls'][0]['result']['regions'][0]
replay=review_floor(read(ROOT/'analises/verificacao_flexao_V607/entrada.json'),api=api)
new=replay['beams'][0]['controls'][0]['result']['regions'][0]
assert (old['MRd_knm'],old['utilization'])==(new['MRd_knm'],new['utilization'])
write('regressao_v607.json',dict(case_type='REAL',unchanged=True,MRd_knm=new['MRd_knm'],utilization=new['utilization']))
tests=read(OUT/'testes.json') if '--reuse-tests' in sys.argv else [];env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONIOENCODING='utf-8')
for suite in (() if '--reuse-tests' in sys.argv else ('beam_model','extrator_lst','beam_mapping','reinforcement_checks')):
 cmd=[sys.executable,'-m','unittest','discover','-s','tools/'+suite,'-p','test_*.py','-q']
 p=subprocess.run(cmd,cwd=ROOT,env=env,capture_output=True,text=True,encoding='utf-8')
 tests.append(dict(suite=suite,command=cmd,exit_code=p.returncode,output=p.stdout+p.stderr));print(suite,p.returncode,flush=True)
write('testes.json',tests)
after=hashes();write('preservacao.json',dict(unchanged=before==after,count=len(before),changed=[p for p,v in before.items() if after.get(p)!=v]))
assert before==after and all(t['exit_code']==0 for t in tests)
