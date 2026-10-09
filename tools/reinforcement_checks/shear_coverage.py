"""Documentary function and physical stirrup coverage, independent of TQS."""
from copy import deepcopy
from math import isfinite
from moment_diagram import dec

COLUMN_RULE='engineer_confirmed_stirrups_terminate_at_column_faces_v1'
SLAB_RULE='engineer_confirmed_n12_adjacent_slab_negative_reinforcement_v1'
SLAB='ADJACENT_SLAB_NEGATIVE_REINFORCEMENT'
STIRRUP='CONVENTIONAL_SHEAR_STIRRUP'

def classify_piece(piece):
 """Identity alone never determines function; retain documentary evidence."""
 role=piece.get('physical_function');source=piece.get('source')
 evidence=piece.get('classification_evidence') or {}
 if role==SLAB and source and evidence.get('geometry') and evidence.get('function_confirmation'):
  return {'status':'NOT_APPLICABLE','classification':SLAB,'contributes_to_beam_shear':False,
   'rule':SLAB_RULE,'provenance':deepcopy(evidence)}
 # Existing drawn-stirrup contract is explicit positive legs plus documentary source.
 if source and role in (None,STIRRUP) and type(piece.get('legs'))==int and piece['legs']>0:
  return {'status':'PASS','classification':STIRRUP,'contributes_to_beam_shear':True,'provenance':deepcopy(source)}
 return {'status':'INCONCLUSIVE','classification':'UNRESOLVED_REINFORCEMENT_FUNCTION',
  'contributes_to_beam_shear':None,'reason':'documentary_function_requires_interpretation','provenance':deepcopy(source)}

def physical_coverage(span,tqs_domain,regions):
 """Coverage is required only between proven column faces, never inferred offsets."""
 out={'TQS_SHEAR_DOMAIN':list(tqs_domain),'BEAM_STIRRUP_COVERAGE_DOMAIN':None,
  'status':'INCONCLUSIVE','rule':COLUMN_RULE,'support_geometry':deepcopy(span.get('support_geometry')),
  'intervals':[],'uncovered_required_intervals_m':[],'overlapping_required_intervals_m':[]}
 try:
  geo=span['support_geometry'];left,right=geo['left'],geo['right']
  for support in (left,right):
   if support.get('type')!='COLUMN' or not support.get('type_source') or not support.get('source'):
    raise ValueError('column_geometry_applicability_unproven')
   a,x,b,w=[dec(support[k]) for k in ('left_face_m','axis_m','right_face_m','width_m')]
   if not all(isfinite(float(z)) for z in (a,x,b,w)) or not a<x<b or w<=0 or abs((b-a)-w)>dec(1e-9):
    raise ValueError('inconsistent_support_faces')
  a,b=dec(left['right_face_m']),dec(right['left_face_m'])
  if a>=b:raise ValueError('invalid_physical_span')
 except (KeyError,ValueError,TypeError) as error:
  out['reason']=str(error);out['intervals']=[{'interval_m':list(tqs_domain),'classification':'GEOMETRY_INCONCLUSIVE','status':'INCONCLUSIVE'}];return out
 out['BEAM_STIRRUP_COVERAGE_DOMAIN']=[float(a),float(b)]
 low=min(dec(tqs_domain[0]),a);high=max(dec(tqs_domain[1]),b)
 events={low,high,a,b}
 for support in (left,right):
  for key in ('left_face_m','right_face_m'):
   z=dec(support[key])
   if low<z<high:events.add(z)
 for region in regions:
  for value in region['interval_m']:
   z=dec(value)
   if low<z<high:events.add(z)
 for x,y in zip(sorted(events),sorted(events)[1:]):
  mid=(x+y)/2;entry={'interval_m':[float(x),float(y)]}
  if a<mid<b:
   active=[r for r in regions if dec(r['interval_m'][0])<mid<dec(r['interval_m'][1])]
   entry.update(classification='REQUIRED_BEAM_COVERAGE' if active else 'UNCOVERED_REQUIRED_REGION',status='PASS' if len(active)==1 else 'INCONCLUSIVE',regions=[r.get('id') for r in active])
   if not active:out['uncovered_required_intervals_m'].append(entry['interval_m'])
   elif len(active)>1:out['overlapping_required_intervals_m'].append(entry['interval_m'])
  else:
   support=next((s for s in (left,right) if dec(s['left_face_m'])<mid<dec(s['right_face_m'])),None)
   entry.update(classification='WITHIN_SUPPORT' if support else 'GEOMETRY_INCONCLUSIVE',status='NOT_APPLICABLE' if support else 'INCONCLUSIVE',support=deepcopy(support))
  out['intervals'].append(entry)
 out['status']='PASS' if all(i['status'] in ('PASS','NOT_APPLICABLE') for i in out['intervals']) else 'INCONCLUSIVE'
 return out

