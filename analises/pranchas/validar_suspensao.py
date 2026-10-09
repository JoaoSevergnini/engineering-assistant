"""Reproduce synthetic suspension and audit availability in real V516/V517 inputs."""
from pathlib import Path
from copy import deepcopy
import json,sys,hashlib
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'analises/pranchas'
sys.path[:0]=[str(ROOT/'tools/reinforcement_checks'),str(ROOT.parent/'concretopy')]
from suspension_review import review_suspension,connections_from_mapping
from shear_review import public_shear_api

def load(path):return json.loads(path.read_text(encoding='utf8'))
def write(name,result):
 (OUT/name).write_text(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf8')

def run():
 api=public_shear_api();fixture=load(OUT/'suspension_synthetic_fixture.json')
 synthetic=review_suspension(fixture['connections'],receiving_beam=fixture['receiving_beam'],spans=fixture['spans'],
  context=fixture['context'],api=api,inventory_complete=fixture['inventory_complete'],inventory_source=fixture['inventory_source'])
 synthetic['fixture_source']={'type':'SYNTHETIC','path':'suspension_synthetic_fixture.json','sha256':hashlib.sha256((OUT/'suspension_synthetic_fixture.json').read_bytes()).hexdigest()}
 write('suspension_synthetic_review.json',synthetic)
 print('SYNTHETIC',synthetic['overall_result'])
 for beam in ('V516','V517'):
  shear_path=OUT/f'{beam}_shear_reinforcement_review.json';case=load(shear_path);tqs_path=OUT/f'{beam}_tqs.json';tqs=load(tqs_path)
  candidates=[];mapping_sources=[]
  for path in sorted(OUT.glob('*beam_mapping.json')):
   mapping=load(path)
   if mapping.get('beam_id')==beam:
    candidates.extend(c for c in connections_from_mapping(mapping) if c['receiving_beam_id']==beam)
    mapping_sources.append({'path':path.name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
  result=review_suspension(candidates,receiving_beam=beam,spans=case['geometry_and_drawn_regions'],
   context=case['provenance']['context'],api=api,inventory_complete=False,
   inventory_source={'type':'available audited files only; indirect connection inventory not proven complete','files':[shear_path.name,tqs_path.name]})
  result['documentary_audit']={'mapping_sources':mapping_sources,
   'possible_graphical_traces':[deepcopy(r['region']) for r in case['shear_drawn_regions'] if r['region'].get('indirect_support_evidence')],
   'own_support_reactions':deepcopy(tqs['beam'].get('support_reactions',[])),
   'interpretation':'own beam reactions to pillars are not a supported-beam reaction on this receiving beam; N1 graphic trace alone does not prove transfer, total reaction or supported identity',
   'missing_data':['supported beam identity and connection/applicability evidence','total supported-beam reaction with nature, combination, direction and provenance','projected supported axis in receiving coordinates','supported beam geometry'],
   'inputs':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (shear_path,tqs_path)},
   'independent_shear_approval_preserved':case['global_shear_approval']}
  write(f'{beam}_suspension_review.json',result);print(beam,result['overall_result'],'proven connections',len(candidates))
 return synthetic
if __name__=='__main__':run()
