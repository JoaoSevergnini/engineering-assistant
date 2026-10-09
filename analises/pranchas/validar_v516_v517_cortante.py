"""Shear-only real adapter. Longitudinal goldens are read-only inputs."""
from pathlib import Path
from decimal import Decimal as D
from copy import deepcopy
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'analises/pranchas'
sys.path[:0]=[str(ROOT/'tools/reinforcement_checks'),str(ROOT.parent/'concretopy')]
from shear_review import select_shear_depth,review_shear_spans,public_shear_api


def add(a,b):return float(D(str(a))+D(str(b)))
def run(beam):
 path=OUT/(beam+'_negative_reinforcement_review.json');case=json.loads(path.read_text(encoding='utf8'))
 depth=select_shear_depth(case['regions'])
 if depth['status']!='PASS':raise ValueError('audited_longitudinal_depth_selection_unresolved')
 parameters=depth['selected']['provenance']['concretopy']['parametros']
 ctx={'section':{'bw':parameters['bw_cm'],'h':parameters['h_cm'],'cobrimento':parameters['cobrimento_cm'],'diametro_estribo_mm':parameters['diametro_estribo_mm']},
  'fck_mpa':parameters['fck'],'fyk_mpa':parameters['fyk'],'gamma_f':parameters['gamma_f'],'gamma_c':parameters['gamma_c'],'gamma_s':parameters['gamma_s'],
  'effective_depth':depth,'provenance':{'longitudinal_input':str(path),'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}}
 supports=case['ordered_supports']
 source={'document':case['document'],'page':1,'rendering':'V516_V517_hit_1_0.png','reading':'text labels and physical shapes reread in source PDF; real drawing governs, not TQS generated reinforcement'}
 descriptions=[('N12',8,20,10,None,'ADJACENT_SLAB_NEGATIVE_REINFORCEMENT'),('N13',5,14,31,2,'CONVENTIONAL_SHEAR_STIRRUP')]
 spans=[]
 for i,span in enumerate(case['spans']):
  start=supports[i]['right_face_m'];end=supports[i+1]['left_face_m']
  def region(mark,phi,spacing,count,legs,a,b,*,role='CONVENTIONAL_SHEAR_STIRRUP',special=False):
   return {'id':f'{beam}/span-{i+1}/{mark}/{a}-{b}','mark':mark,'diameter_mm':phi,'spacing_cm':spacing,
    'drawn_count':count,'legs':legs,'interval_m':[a,b],'physical_function':role,
    'source':{**deepcopy(source),'label':f'{count} {mark} diameter{phi} C/{spacing}',
       'geometry':'rectangular 14x47cm gives two drawn vertical legs' if legs==2 else
                  'asymmetric vertical segments47/27cm and horizontal64cm: continuity of adjacent slab negative reinforcement across level difference',
       'coordinate_source':deepcopy(supports[i:i+2]),'local_length_cm':float((D(str(b))-D(str(a)))*100)},
    'classification_evidence':{'geometry':'asymmetric47/27cm with horizontal64cm segments in source drawing','function_confirmation':{'rule':'engineer_confirmed_n12_adjacent_slab_negative_reinforcement_v1','source':'engineer clarification 2026-10-08: adjacent slab negative continuity across level difference'}} if role=='ADJACENT_SLAB_NEGATIVE_REINFORCEMENT' else None,
    'indirect_support_evidence':{'drawing':'special52cm region spatially associated with dashed supported-beam trace','policy':'suspension remains NOT_EVALUATED'} if special else None}
  if i in (0,3):drawn=[region('N12',8,20,10,None,start,end,role='ADJACENT_SLAB_NEGATIVE_REINFORCEMENT')]
  elif i==1:drawn=[region('N13',5,14,31,2,start,end)]
  else:
   first=add(start,1.91);second=add(first,.52)
   drawn=[region('N13',5,14,14,2,start,first),region('N1',8,12,5,2,first,second,special=True),region('N13',5,10,12,2,second,end)]
   assert first==8.64 and second==9.16
   # Caller declares physical support branches; no guessed global crossing.
   points=span['diagram']['points'];mid=points[5]['x_m']
   drawn[0]['transition']={'drawn_x':start,'side':'LEFT','branch_domain':[span['sampled_domain_m'][0],mid]}
   drawn[-1]['transition']={'drawn_x':end,'side':'RIGHT','branch_domain':[mid,span['sampled_domain_m'][1]]}
  spans.append({'span_id':i+1,'series':deepcopy(span['shear']['series']),'drawn_regions':drawn,
    'reference_legs':2,'reference_geometry_provenance':'explicit reference scenario based on conventional N13 rectangular14x47, never equivalent resistant credit for N12',
    'sampled_domain_m':span['sampled_domain_m'],'physical_clear_domain_m':[start,end],
    'support_geometry':{side:{**deepcopy(supports[j]),'type':'COLUMN','type_source':{'drawing':deepcopy(case['document']),'geometry':'column outlines and dimensions audited in beam drawing, confirmed column-face coverage by engineer 2026-10-08'}} for side,j in (('left',i),('right',i+1))}})
 result=review_shear_spans(spans,ctx,public_shear_api())
 result.update(beam_id=beam,drawing_group=case['drawing_group'],document=case['document'],
  geometry_and_drawn_regions=spans,effective_depth_selection=depth,
  longitudinal_results_modified=False,inputs={path.name:hashlib.sha256(path.read_bytes()).hexdigest()},
  assumptions=['same audited rectangular beam section; shear effective depth selected from returned physical centroids by engineer rule',
   'reference legs2 is conventional rectangular reference, not inferred N12 effectiveness',
   'N12 is adjacent slab negative reinforcement, excluded from beam stirrup checks',
   'beam stirrup coverage applies between proven physical column faces, independent of TQS domain'])
 (OUT/(beam+'_shear_reinforcement_review.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf8')
 print(beam,'depth',depth['d_cm'],'selected',depth['selected']['provenance']['marks'],'global',result['global_shear_approval'])
 for r in result['shear_drawn_regions']:
  print(r['span_id'],r['region']['mark'],r['region']['interval_m'],r['demand']['Vsk_abs_kn'],r.get('design',{}).get('governing_Asw_per_s_cm2_m'),r.get('provided',{}).get('Asw_per_s_cm2_m'),r['overall_structural_result'])
 return result
if __name__=='__main__':
 for beam in ('V516','V517'):run(beam)
