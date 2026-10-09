"""Deterministic suspension verification, separate from independent beam shear."""
from copy import deepcopy
from math import isfinite
from shear_diagram import ShearDiagram
from shear_review import public_shear_api,design_shear,check_drawn_region,control
from shear_coverage import classify_piece,physical_coverage
from bar_scaling import api_provenance
from moment_diagram import dec

RULES={
 'reaction':'engineer_confirmed_suspension_75_percent_reaction_v1',
 'distribution':'engineer_confirmed_suspension_symmetric_distribution_v1',
 'shear':'engineer_confirmed_suspension_shear_without_minimum_v1',
 'minimum':'engineer_confirmed_suspension_total_minimum_governance_v1',
 'usual':'engineer_confirmed_suspension_usual_stirrup_practices_v1'}
CONTROLS=('indirect_support_identification','total_support_reaction','reaction_nature',
 'geometric_position','distribution_length','shear_diagram_coverage','suspension_component',
 'shear_calculated_component','minimum_component','total_required_rate',
 'provided_stirrup_area','maximum_code_spacing','effective_legs','usual_practices','drawing_coverage')

def number(value):return float(dec(value))
def state(checks):
 values=[v['status'] for v in checks.values()]
 if 'FAIL' in values:return 'FAIL'
 if 'INCONCLUSIVE' in values:return 'INCONCLUSIVE'
 if 'REQUIRES_ENGINEERING_REVIEW' in values:return 'REQUIRES_ENGINEERING_REVIEW'
 return 'PASS'

def identify(connection,receiving_beam):
 try:
  if not connection.get('id') or connection.get('type')!='BEAM_ON_BEAM':raise ValueError('indirect_support_not_confirmed')
  if connection.get('receiving_beam_id')!=receiving_beam or not connection.get('supported_beam_id') or connection['supported_beam_id']==receiving_beam:raise ValueError('beam_roles_unresolved')
  if connection.get('transfer_confirmed') is not True or not connection.get('transfer_source'):raise ValueError('reaction_transfer_unproven')
  if connection.get('suspension_applicable') is not True or not connection.get('applicability_source'):raise ValueError('suspension_application_unproven')
  geometry=connection['supported_geometry']
  if not geometry.get('source') or number(geometry['height_cm'])<=0 or number(geometry['width_cm'])<=0:raise ValueError('supported_beam_geometry_unresolved')
  return control(True,provenance=deepcopy(connection))
 except (ValueError,KeyError,TypeError) as e:return control(reason=str(e))

def reaction_area(reaction,context,api,connection):
 out={'reaction':deepcopy(reaction),'total_support_reaction':control(),'reaction_nature':control(),
  'suspension_component':control(),'as_suspension_cm2':None}
 try:
  if not isinstance(reaction,dict) or not reaction.get('source'):raise ValueError('total_reaction_missing')
  if reaction.get('nature') not in ('CHARACTERISTIC','DESIGN'):raise ValueError('reaction_nature_unresolved')
  out['reaction_nature']=control(True,nature=reaction['nature'])
  if reaction.get('is_total') is not True or not reaction.get('total_source') or not reaction.get('combination'):raise ValueError('total_reaction_or_combination_unproven')
  if reaction.get('supported_beam_id')!=connection.get('supported_beam_id') or reaction.get('receiving_beam_id')!=connection.get('receiving_beam_id'):raise ValueError('reaction_beam_roles_mismatch')
  if reaction.get('unit')!='kN':raise ValueError('reaction_unit_requires_explicit_normalization_to_kN')
  sign=reaction.get('downward_sign')
  if type(sign) not in (int,float) or sign not in (-1,1):raise ValueError('reaction_direction_unresolved')
  original=number(reaction['value']);r=sign*original
  if r<0:raise ValueError('uplift_suspension_not_formalized')
  out['total_support_reaction']=control(True,total_kn=r,original_signed_kn=original,downward_sign=sign,provenance=deepcopy(reaction))
  gf=number(context['gamma_f']);gs=number(context['gamma_s']);fy=number(context['fyk_mpa'])
  if min(gf,gs,fy)<=0:raise ValueError('invalid_material_or_partial_factor')
  fyd=api.Aco(fy).fyd(gs);applied=gf if reaction['nature']=='CHARACTERISTIC' else 1.0
  rd=r*applied;considered=.75*rd;area=considered/(fyd*.1)
  out.update(total_characteristic_kn=r if applied!=1 or reaction['nature']=='CHARACTERISTIC' else None,
   total_design_kn=rd,considered_design_kn=considered,gamma_f_applied=applied,fyd_mpa=fyd,
   fyd_kn_cm2=fyd*.1,as_suspension_cm2=area,
   provenance={'rule':RULES['reaction'],'steel_api':api_provenance(api.Aco.fyd),
    'conversion':'1 MPa = 0.1 kN/cm2; area = considered_design_kn / fyd_kn_cm2'})
  out['suspension_component']=control(True,area_cm2=area,rule=RULES['reaction'])
 except (ValueError,KeyError,TypeError) as e:out['diagnostic']=str(e)
 return out

def distribution(connection,context):
 out={'geometric_position':control(),'distribution_length':control(),'interval_m':None,'length_cm':None,
  'placement':connection.get('placement'),'rule':RULES['distribution']}
 try:
  h=number(context['section']['h'])
  if h<=0:raise ValueError('receiving_beam_height_unresolved')
  kind=connection.get('placement')
  if kind not in ('INTERIOR','CANTILEVER_END'):raise ValueError('distribution_situation_unresolved')
  length=h if kind=='INTERIOR' else h/2
  out.update(length_cm=length,height_of_receiving_beam_cm=h)
  out['distribution_length']=control(True,length_cm=length,rule=RULES['distribution'])
  if kind=='INTERIOR':
   if not connection.get('axis_source'):raise ValueError('projected_supported_axis_unresolved')
   x=dec(connection['projected_axis_m']);a,b=x-dec(h)/200,x+dec(h)/200
   out['provenance']={'projected_axis_m':float(x),'source':deepcopy(connection['axis_source'])}
  else:
   if not connection.get('explicit_interval_source'):raise ValueError('cantilever_distribution_origin_unconfirmed')
   a,b=map(dec,connection['explicit_interval_m'])
   if abs((b-a)*100-dec(length))>dec(1e-8):raise ValueError('explicit_distribution_length_mismatch')
   out['provenance']={'explicit_interval':deepcopy(connection['explicit_interval_source'])}
  if a>=b:raise ValueError('distribution_interval_invalid')
  out['interval_m']=[float(a),float(b)];out['geometric_position']=control(True,provenance=deepcopy(out['provenance']))
 except (ValueError,KeyError,TypeError) as e:out['diagnostic']=str(e)
 return out

def inspect_geometry(interval,spans):
 candidates=[];out=control(reason='distribution_crosses_span_support_or_unknown_geometry',candidates=[])
 a,b=map(dec,interval)
 for span in spans:
  try:
   diagram=ShearDiagram(span['series']);coverage=physical_coverage(span,diagram.domain,[])
   domain=coverage['BEAM_STIRRUP_COVERAGE_DOMAIN'];source=coverage['support_geometry']
   if domain is None and span.get('explicit_physical_domain_source'):
    domain=span['explicit_physical_beam_domain_m'];source=span['explicit_physical_domain_source']
   if domain and dec(domain[0])<=a<b<=dec(domain[1]):candidates.append((span,domain,source))
  except (ValueError,KeyError,TypeError):continue
 out['candidates']=[{'span_id':s.get('span_id'),'physical_domain_m':d,'source':deepcopy(p)} for s,d,p in candidates]
 if len(candidates)!=1:return out,None
 span,domain,source=candidates[0]
 if any(a<dec(x)<b for x in span.get('section_changes_m',[])):
  out['reason']='distribution_crosses_section_change';return out,span
 return control(True,physical_domain_m=domain,span_id=span.get('span_id'),provenance=deepcopy(source)),span

def review_connection(connection,receiving_beam,spans,context,api):
 out={'verification':'SUSPENSION_REINFORCEMENT_CHECK','connection':deepcopy(connection),
  'checks':{name:control() for name in CONTROLS},'subintervals':[],'excluded_reinforcement':[],
  'diagnostics':[],'overall_result':'INCONCLUSIVE','suspension_passes':None,
  'selected_solution':None,'detailing_optimization':None,'provenance':{'rules':deepcopy(RULES),'context':deepcopy(context)}}
 checks=out['checks'];checks['indirect_support_identification']=identify(connection,receiving_beam)
 area=reaction_area(connection.get('reaction'),context,api,connection);out['suspension']=area
 for key in ('total_support_reaction','reaction_nature','suspension_component'):checks[key]=area[key]
 dist=distribution(connection,context);out['distribution']=dist
 for key in ('geometric_position','distribution_length'):checks[key]=dist[key]
 interval=dist['interval_m']
 if not interval:
  out['overall_result']=state(checks);return out
 geometry,span=inspect_geometry(interval,spans);out['physical_geometry']=geometry
 if geometry['status']!='PASS':checks['geometric_position']=geometry
 # Even crossing a boundary: preserve failures from known intersection, never truncate required region.
 if span is None:
  intersections=[]
  for candidate in spans:
   try:
    d=ShearDiagram(candidate['series']);a,b=interval
    if max(a,d.domain[0])<min(b,d.domain[1]):intersections.append(candidate)
   except (ValueError,KeyError,TypeError):continue
  if len(intersections)==1:span=intersections[0]
 if span is None:
  out['diagnostics'].append('distribution_requires_multiple_span_or_geometry_contexts');return out
 if geometry.get('reason')=='distribution_crosses_section_change':
  # The force diagram remains readable; a uniform resisting section is not proven.
  try:
   demand=ShearDiagram(span['series']).maximum(*interval);out['shear_demand']=demand
   checks['shear_diagram_coverage']=control(True) if demand['complete'] else control(reason='partial_shear_region_coverage')
  except (ValueError,KeyError,TypeError) as e:out['diagnostics'].append(str(e))
  out['diagnostics'].append('section_contexts_required_before_regional_resistance_calculation');return out
 try:
  shear=ShearDiagram(span['series']);demand=shear.maximum(*interval);out['shear_demand']=demand
  checks['shear_diagram_coverage']=control(demand['complete'],provenance=deepcopy(demand)) if demand['complete'] else control(reason='partial_shear_region_coverage',provenance=deepcopy(demand))
  rate=area['as_suspension_cm2']/dist['length_cm']*100 if area['as_suspension_cm2'] is not None and checks['indirect_support_identification']['status']=='PASS' else None
  out['asw_per_s_suspension']=rate
  # Concrete capacity and demand remain checkable even when no stirrup is documented.
  if demand['Vsk_abs_kn'] is not None:
   regional=design_shear(context,api,demand['Vsk_abs_kn'],context['section']['diametro_estribo_mm'])
   out['regional_shear_design']=regional
   checks['diagonal_compression']=deepcopy(regional['diagonal_compression'])
   components=regional.get('concretopy',{})
   calc,minimum=components.get('asw_por_s_calculado'),components.get('asw_por_s_minimo')
   out.update(asw_per_s_shear_calculated=calc,asw_per_s_shear_minimum=minimum,
    asw_per_s_total_required=max(rate+calc,minimum) if rate is not None and calc is not None and minimum is not None else None)
  if rate is not None:checks['suspension_component']=control(True,asw_per_s_cm2_m=rate,rule=RULES['reaction'],conversion='cm2 / cm * 100 -> cm2/m')
  regions=[]
  for piece in span.get('drawn_regions',[]):
   classification=classify_piece(piece)
   if classification['contributes_to_beam_shear'] is False:
    out['excluded_reinforcement'].append({'piece':deepcopy(piece),'classification':classification});continue
   regions.append((piece,classification))
  a,b=interval
  events=sorted({dec(a),dec(b),*[dec(x) for r,_ in regions for x in r['interval_m'] if a<x<b]})
  for x,y in zip(events,events[1:]):
   mid=(x+y)/2;active=[(r,c) for r,c in regions if dec(r['interval_m'][0])<mid<dec(r['interval_m'][1])]
   item={'interval_m':[float(x),float(y)],'checks':{'drawing_coverage':control()},'overall_result':'INCONCLUSIVE'}
   if len(active)!=1:
    item['checks']['drawing_coverage']=control(reason='stirrup_coverage_missing_or_ambiguous',active_regions=[r.get('id') for r,c in active]);out['subintervals'].append(item);continue
   r,classification=active[0];item['piece']=deepcopy(r);item['classification']=classification
   if classification['status']!='PASS' and not (r.get('physical_function')=='CONVENTIONAL_SHEAR_STIRRUP' and r.get('source')):
    item['checks']['drawing_coverage']=control(reason='reinforcement_function_unresolved');out['subintervals'].append(item);continue
   item['checks']['drawing_coverage']=control(True)
   segment=deepcopy(r);segment['interval_m']=[float(x),float(y)];segment.pop('transition',None)
   independent=check_drawn_region(shear,context,api,segment);item['independent_shear_check']=independent
   c=independent['checks'];ic=item['checks']
   ic['independent_shear_reinforcement']=deepcopy(c['shear_reinforcement'])
   for k in ('diagonal_compression','maximum_code_spacing','number_of_legs','stirrup_holder'):ic[k]=deepcopy(c[k])
   item['provided']=deepcopy(independent.get('provided'))
   item['usual_checks']={k:deepcopy(c[k]) for k in ('usual_diameter','usual_minimum_spacing')}
   # Entire suspension region maximum, not a lower maximum from a neighbouring segment.
   design=design_shear(context,api,demand['Vsk_abs_kn'],r['diameter_mm']) if demand['Vsk_abs_kn'] is not None else {'status':'INCONCLUSIVE'}
   item['regional_shear_design']=design
   if design.get('diagonal_compression',{}).get('status')=='FAIL':ic['diagonal_compression']=deepcopy(design['diagonal_compression'])
   raw=design.get('concretopy',{});calc=raw.get('asw_por_s_calculado');minimum=raw.get('asw_por_s_minimo')
   item.update(asw_per_s_suspension=rate,asw_per_s_shear_calculated=calc,asw_per_s_shear_minimum=minimum,asw_per_s_total_required=None)
   ic['shear_calculated_component']=control(calc is not None and calc>=0) if calc is not None else control(reason='Concretopy_shear_calculated_component_unavailable')
   ic['minimum_component']=control(True) if minimum is not None else control(reason='Concretopy_minimum_component_unavailable')
   ic['total_required_rate']=control();ic['provided_stirrup_area']=control()
   if rate is not None and calc is not None and minimum is not None:
    required=max(rate+calc,minimum);item['asw_per_s_total_required']=required
    item['combination_provenance']={'rule':RULES['minimum'],'expression':'max(suspension + shear_calculated, shear_minimum)'}
    ic['total_required_rate']=control(True)
    provided=independent.get('provided',{}).get('Asw_per_s_cm2_m')
    if provided is not None:ic['provided_stirrup_area']=control(provided>=required,provided_cm2_m=provided,required_cm2_m=required,margin_cm2_m=provided-required)
   if design.get('maximum_spacing_code_cm') is not None:
    ic['maximum_code_spacing']=control(r['spacing_cm']<=design['maximum_spacing_code_cm'],limit_cm=design['maximum_spacing_code_cm'],drawn_cm=r['spacing_cm'])
   item['overall_result']=state(ic);out['subintervals'].append(item)
  # Aggregate independent controls, never average provided rates.
  aliases={'effective_legs':'number_of_legs'}
  for key in ('shear_calculated_component','minimum_component','total_required_rate','provided_stirrup_area','maximum_code_spacing','effective_legs','drawing_coverage'):
   values=[i['checks'].get(aliases.get(key,key),control()) for i in out['subintervals']]
   status=state({str(j):v for j,v in enumerate(values)}) if values else 'INCONCLUSIVE'
   checks[key]={'status':status,'passes':True if status=='PASS' else False if status=='FAIL' else None}
  usual=[v for i in out['subintervals'] for v in i.get('usual_checks',{}).values()]
  checks['usual_practices']={'status':state({str(j):v for j,v in enumerate(usual)}) if usual else 'INCONCLUSIVE','rule':RULES['usual']}
  all_checks={**checks,**{f'segment_{j}':{'status':i['overall_result']} for j,i in enumerate(out['subintervals'])}}
  out['overall_result']=state(all_checks)
  out['suspension_passes']=False if out['overall_result']=='FAIL' else True if out['overall_result'] in ('PASS','REQUIRES_ENGINEERING_REVIEW') else None
 except (ValueError,KeyError,TypeError) as e:out['diagnostics'].append(str(e))
 # Preserve proven failures even if a later dependency failed to resolve.
 all_checks={**checks,**{f'segment_{j}':{'status':i['overall_result']} for j,i in enumerate(out['subintervals'])}}
 out['overall_result']=state(all_checks)
 out['suspension_passes']=False if out['overall_result']=='FAIL' else True if out['overall_result'] in ('PASS','REQUIRES_ENGINEERING_REVIEW') else None
 return out

def review_suspension(connections,*,receiving_beam,spans,context,api=None,inventory_complete=False,inventory_source=None):
 api=api or public_shear_api()
 results=[review_connection(c,receiving_beam,spans,context,api) for c in connections]
 for i,a in enumerate(results):
  for b in results[i+1:]:
   aa,bb=a['distribution']['interval_m'],b['distribution']['interval_m']
   if aa and bb and max(aa[0],bb[0])<min(aa[1],bb[1]):
    for current,other in ((a,b),(b,a)):
     current['checks']['overlapping_suspension_regions']=control(reason='multiple_supported_beams_combination_unconfirmed',other_connection=other['connection'].get('id'))
     current['diagnostics'].append('overlap_not_summed_or_ignored')
     if current['overall_result']!='FAIL':current['overall_result']='INCONCLUSIVE';current['suspension_passes']=None
 out={'verification':'SUSPENSION_REVIEW','receiving_beam_id':receiving_beam,'connections':results,
  'inventory':{'complete':inventory_complete,'source':deepcopy(inventory_source)},'selected_solution':None,'detailing_optimization':None,
  'independent_shear_results_modified':False,'provenance':{'rules':deepcopy(RULES)}}
 statuses=[r['overall_result'] for r in results]
 out['overall_result']='FAIL' if 'FAIL' in statuses else 'INCONCLUSIVE' if not inventory_complete or not inventory_source or 'INCONCLUSIVE' in statuses else 'REQUIRES_ENGINEERING_REVIEW' if 'REQUIRES_ENGINEERING_REVIEW' in statuses else 'PASS' if results else 'NOT_APPLICABLE'
 out['suspension_passes']=False if out['overall_result']=='FAIL' else True if out['overall_result'] in ('PASS','NOT_APPLICABLE','REQUIRES_ENGINEERING_REVIEW') else None
 return out

def connections_from_mapping(mapping):
 """Discover evidence-backed candidates, without selecting/totalizing reactions."""
 candidates=[]
 for relation in mapping.get('indirect_relations',[]):
  candidates.append({'id':relation.get('drawing_indirect_support_id') or f"{relation.get('supported_beam')}->{relation.get('receiving_beam')}",
   'type':'BEAM_ON_BEAM','supported_beam_id':relation.get('supported_beam'),'receiving_beam_id':relation.get('receiving_beam'),
   'transfer_confirmed':bool(relation.get('source_records') and relation.get('reaction')),
   'transfer_source':deepcopy(relation.get('source_records')),'projected_axis_m':relation.get('x'),
   'unresolved_reaction_observation':deepcopy(relation.get('reaction')),
   'diagnostic':'total/nature/combination and drawing-axis mapping must be proved before calculation'})
 return candidates
