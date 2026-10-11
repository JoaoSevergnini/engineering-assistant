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

def suspension_area(force_kn,context,api,*,factor):
 """Shared force/steel conversion; the calling procedure supplies its factor."""
 gf,gs,fy=map(number,(context['gamma_f'],context['gamma_s'],context['fyk_mpa']))
 factor=number(factor)
 if min(gf,gs,fy,factor)<=0:raise ValueError('invalid_material_or_partial_factor')
 fyd=api.Aco(fy).fyd(gs)
 return dict(as_suspension_cm2=abs(number(force_kn))*gf*factor/(fyd*.1),
             gamma_f=gf,gamma_s=gs,factor=factor,fyd_mpa=fyd,fyd_kn_cm2=fyd*.1,
             steel_api=api_provenance(api.Aco.fyd))

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
  applied=gf if reaction['nature']=='CHARACTERISTIC' else 1.0
  rd=r*applied;considered=.75*rd
  steel=suspension_area(r,{**context,'gamma_f':applied},api,factor=.75)
  area=steel['as_suspension_cm2'];fyd=steel['fyd_mpa']
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
  if context.get('suspension_distribution_height'):
   import sys
   from pathlib import Path
   sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'beam_model'))
   from input_evidence import validate_fact, PROVED
   selected=validate_fact(context['suspension_distribution_height'],'cm')
   if selected['state'] not in PROVED:raise ValueError('suspension_distribution_height_unproved')
   h=number(selected['value']);out['height_selection']=deepcopy(selected)
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
  contexts=span.get('section_contexts', [])
  events=sorted({a,b,*[dec(x) for s in contexts for x in s['interval_m'] if a<dec(x)<b]})
  if contexts and all(sum(dec(s['interval_m'][0])<=(x+y)/2<=dec(s['interval_m'][1]) and bool(s.get('source'))
                          for s in contexts)==1 for x,y in zip(events,events[1:])):
   return control(True,physical_domain_m=domain,span_id=span.get('span_id'),provenance=deepcopy(source),
                  local_section_contexts=deepcopy(contexts),local_discontinuity_approval=None),span
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
  local_sections=span.get('section_contexts', [])
  if demand['Vsk_abs_kn'] is not None and not local_sections:
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
  events=sorted({dec(a),dec(b),*[dec(x) for r,_ in regions for x in r['interval_m'] if a<x<b],
                 *[dec(x) for s in local_sections for x in s['interval_m'] if a<x<b]})
  for x,y in zip(events,events[1:]):
   mid=(x+y)/2;active=[(r,c) for r,c in regions if dec(r['interval_m'][0])<mid<dec(r['interval_m'][1])]
   item={'interval_m':[float(x),float(y)],'checks':{'drawing_coverage':control()},'overall_result':'INCONCLUSIVE'}
   if len(active)!=1:
    item['checks']['drawing_coverage']=control(reason='stirrup_coverage_missing_or_ambiguous',active_regions=[r.get('id') for r,c in active]);out['subintervals'].append(item);continue
   r,classification=active[0];item['piece']=deepcopy(r);item['classification']=classification
   local_context=context
   if local_sections:
    candidates=[s for s in local_sections if dec(s['interval_m'][0])<=x<y<=dec(s['interval_m'][1]) and s.get('source')]
    if len(candidates)!=1:
     item['checks']['local_section']=control(reason='unique_local_section_context_required');out['subintervals'].append(item);continue
    local_context=candidates[0]['context'];item['physical_section']=deepcopy(candidates[0])
   if classification['status']!='PASS' and not (r.get('physical_function')=='CONVENTIONAL_SHEAR_STIRRUP' and r.get('source')):
    item['checks']['drawing_coverage']=control(reason='reinforcement_function_unresolved');out['subintervals'].append(item);continue
   item['checks']['drawing_coverage']=control(True)
   segment=deepcopy(r);segment['interval_m']=[float(x),float(y)];segment.pop('transition',None)
   independent=check_drawn_region(shear,local_context,api,segment);item['independent_shear_check']=independent
   c=independent['checks'];ic=item['checks']
   ic['independent_shear_reinforcement']=deepcopy(c['shear_reinforcement'])
   for k in ('diagonal_compression','maximum_code_spacing','number_of_legs','stirrup_holder'):ic[k]=deepcopy(c[k])
   item['provided']=deepcopy(independent.get('provided'))
   item['usual_checks']={k:deepcopy(c[k]) for k in ('usual_diameter','usual_minimum_spacing')}
   # Entire suspension region maximum, not a lower maximum from a neighbouring segment.
   design=design_shear(local_context,api,demand['Vsk_abs_kn'],r['diameter_mm']) if demand['Vsk_abs_kn'] is not None else {'status':'INCONCLUSIVE'}
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
  if local_sections:
   statuses=[i['checks'].get('diagonal_compression',control()) for i in out['subintervals']]
   checks['diagonal_compression']={'status':state({str(j):v for j,v in enumerate(statuses)}) if statuses else 'INCONCLUSIVE'}
   out['local_discontinuity_approval']=None
  usual=[v for i in out['subintervals'] for v in i.get('usual_checks',{}).values()]
  checks['usual_practices']={'status':state({str(j):v for j,v in enumerate(usual)}) if usual else 'INCONCLUSIVE','rule':RULES['usual']}
  all_checks={**checks,**{f'segment_{j}':{'status':i['overall_result']} for j,i in enumerate(out['subintervals'])}}
  out['overall_result']=state(all_checks)
  out['suspension_passes']=False if out['overall_result']=='FAIL' else True if out['overall_result'] in ('PASS','REQUIRES_ENGINEERING_REVIEW') else None
 except (ValueError,KeyError,TypeError) as e:out['diagnostics'].append(str(e))
 # Preserve proven failures even if a later dependency failed to resolve.
 all_checks={**checks,**{f'segment_{j}':{'status':i['overall_result']} for j,i in enumerate(out['subintervals'])}}
 out['overall_result']=state(all_checks)
 out['engineering_review_required']=out['overall_result'] in ('FAIL','REQUIRES_ENGINEERING_REVIEW')
 out['suspension_passes']=False if out['overall_result']=='FAIL' else True if out['overall_result'] in ('PASS','REQUIRES_ENGINEERING_REVIEW') else None
 return out

def classify_bottom_change(left,right):
 """Bottom elevations, never section height, identify the suspended side."""
 from input_evidence import validate_fact
 out=dict(status='INCONCLUSIVE',suspended_side=None,section_ids=[left['id'],right['id']],pending=[])
 try:
  levels=[validate_fact(s['geometry']['bottom_level_cm'],'cm') for s in (left,right)]
  if any(v['state']!='DOCUMENTED_CONFIRMED' for v in levels):raise ValueError('documented_bottom_levels_required')
  lo,hi=map(lambda v:dec(v['value']),levels);out['bottom_levels']=deepcopy(levels)
  out.update(status='NOT_APPLICABLE' if lo==hi else 'PASS',suspended_side=None if lo==hi else 'LEFT' if lo<hi else 'RIGHT')
 except (ValueError,KeyError,TypeError) as error:out['pending'].append(str(error))
 return out

def review_bottom_step(left,right,transition,context,diagrams,regions,api):
 """Engineer-defined extra shear suspension, entirely on the lower-bottom side."""
 from input_evidence import validate_fact
 out=dict(verification='BOTTOM_STEP_SUSPENSION',classification=classify_bottom_change(left,right),
          status='INCONCLUSIVE',pending=[],subintervals=[],local_discontinuity_approval=None)
 out['pending']+=out['classification']['pending']
 if out['classification']['status']=='NOT_APPLICABLE':
  out.update(status='NOT_APPLICABLE',reason='coincident_bottoms_no_extra_suspension');return out
 if out['classification']['status']!='PASS':return out
 side=out['classification']['suspended_side'];section=left if side=='LEFT' else right
 out.update(suspended_section_id=section['id'],suspended_side=side,adjacent_heights_cm=[s['geometry']['height_cm'] for s in (left,right)])
 try:
  position=validate_fact(transition['position_m'],'m');height=validate_fact(section['geometry']['height_cm'],'cm')
  gn=validate_fact(transition['gamma_n'])
  if gn['unit'] not in (None,'1'):raise ValueError('gamma_n_must_be_dimensionless')
  if any(v['state']!='DOCUMENTED_CONFIRMED' for v in (position,height)) or gn['state'] not in ('DOCUMENTED_CONFIRMED','INFERRED_EXPLICIT_CONVENTION'):
   raise ValueError('proved_transition_height_and_gamma_n_required')
  x=number(position['value']);h=number(height['value'])
  if h<=0 or number(gn['value'])<=0:raise ValueError('positive_height_and_gamma_n_required')
  faces=[validate_fact(left['x_end_m'],'m'),validate_fact(right['x_start_m'],'m')]
  if any(f['state']!='DOCUMENTED_CONFIRMED' or f['value']!=x for f in faces):raise ValueError('transition_not_at_proved_adjacent_faces')
  interval=[x-h/200,x] if side=='LEFT' else [x,x+h/200]
  out.update(position_m=deepcopy(position),distribution_interval_m=interval,distribution_length_cm=h/2,gamma_n=deepcopy(gn))
  if not section['x_start_m']['value']<=interval[0]<interval[1]<=section['x_end_m']['value']:
   raise ValueError('full_unilateral_distribution_outside_constant_section')
  sides={};side_values={};out['transition_shear_sides']=sides
  for label in ('LEFT','RIGHT'):
   diagram=diagrams.get(label)
   if diagram is None:raise ValueError('both_registered_local_shear_diagrams_required')
   explicit=transition.get('shear_sides',{}).get(label)
   values=[]
   for identity,linear in diagram.diagrams:
    if explicit:
     v=validate_fact(explicit.get(identity,{}),'kN')
     if v['state']!='DOCUMENTED_CONFIRMED':raise ValueError('documented_one_sided_characteristic_shear_required')
     value=number(v['value']);origin=deepcopy(v)
    else:
     query=linear.moment_at_x(x)
     if query['status']!='resolved':raise ValueError('one_sided_shear_required_at_discontinuity:'+label)
     value=query['value_knm'];origin=query
    values.append(dict(envelope=identity,Vk_original_kn=value,Vk_abs_kn=abs(value),position_m=x,side=label,source=origin))
   sides[label]=values;side_values[label]={v['envelope']:v for v in values}
  out['transition_shear_sides']=sides
  governing=max(sides[side],key=lambda v:v['Vk_abs_kn']);out['governing_shear']=deepcopy(governing)
  out['mechanism']='shear from the lower-bottom section; opposite-side values preserved, never global span maximum'
  calculation=suspension_area(governing['Vk_abs_kn'],context,api,factor=gn['value'])
  out['additional_area']=calculation;rate=calculation['as_suspension_cm2']/(h/2)*100
  out['additional_rate_cm2_m']=rate
  # Build only the required one-sided interval; no interpolation across the jump.
  regional=[]
  for original,(identity,linear) in zip(diagrams[side].series,diagrams[side].diagrams):
   from moment_diagram import MomentDiagram
   endpoint=dict(section='TRANSITION-'+side,x_m=x,value_knm=side_values[side][identity]['Vk_original_kn'],provenance=side_values[side][identity])
   pts=[deepcopy(p) for p in linear.points if (p['x_m']<x if side=='LEFT' else p['x_m']>x)]+[endpoint]
   one=MomentDiagram(sorted(pts,key=lambda p:p['x_m']),dict(discontinuities_m=[j for j in linear.provenance.get('discontinuities_m',[]) if j!=x],original=linear.provenance))
   xs=sorted({interval[0],interval[1],*[float(q) for q in linear.xs if interval[0]<q<interval[1]]});values=[]
   for q in xs:
    if q==x:values.append(side_values[side][identity]['Vk_original_kn'])
    else:
     query=one.moment_at_x(q)
     if query['status']!='resolved':raise ValueError('usual_shear_region_gap_or_jump')
     values.append(query['value_knm'])
   regional.append(dict(quantity='shear',unit='kN',envelope=identity,positions=xs,values=values,sections=list(range(len(xs))),
       provenance=dict(original=deepcopy(original),one_sided_endpoint=side_values[side][identity])))
  shear=ShearDiagram(regional);demand=shear.maximum(*interval);out['usual_shear_demand']=demand
  relevant=[r for r in regions if max(r['interval_m'][0],interval[0])<min(r['interval_m'][1],interval[1])]
  events=sorted({*interval,*[max(interval[0],min(interval[1],q)) for r in relevant for q in r['interval_m']]})
  coverage=True
  for a,b in zip(events,events[1:]):
   matches=[r for r in relevant if r['interval_m'][0]<=(a+b)/2<=r['interval_m'][1]]
   item=dict(interval_m=[a,b],status='INCONCLUSIVE');out['subintervals'].append(item)
   if len(matches)!=1:
    coverage=False;item['pending']='unique_proved_stirrup_coverage_required';continue
   piece=deepcopy(matches[0]);piece['interval_m']=[a,b]
   if piece.get('position_state')!='DOCUMENTED_CONFIRMED' or not piece.get('source'):
    coverage=False;item['pending']='stirrup_extent_not_proved';continue
   independent=check_drawn_region(shear,context,api,piece,demand_interval_m=interval)
   item['independent_shear_check']=independent
   item['checks']=deepcopy(independent.get('checks',{}))
   item['status']=state(item['checks']) if item['checks'] else 'INCONCLUSIVE'
   design=independent.get('design',{});usual=design.get('governing_Asw_per_s_cm2_m');provided=independent.get('provided',{}).get('Asw_per_s_cm2_m')
   item.update(usual_rate_cm2_m=usual,additional_rate_cm2_m=rate,total_required_rate_cm2_m=None,provided=deepcopy(independent.get('provided')))
   if usual is None or provided is None:coverage=False;item['pending']='usual_shear_or_effective_stirrups_unresolved';continue
   total=usual+rate;item['total_required_rate_cm2_m']=total
   checks=deepcopy(independent['checks']);checks['additional_suspension']=control(provided>=total,required_cm2_m=total,provided_cm2_m=provided)
   if classify_piece(piece).get('contributes_to_beam_shear') is not True:
    coverage=False;item['pending']='effective_beam_stirrup_function_required';continue
   item['checks']=checks;item['status']=state(checks)
  if not coverage:out['pending'].append('full_adensamento_coverage_not_proved')
  states={str(i):dict(status=v['status']) for i,v in enumerate(out['subintervals'])}
  if out['pending']:states['documentary']=control(reason=';'.join(out['pending']))
  out['status']=state(states) if states else 'INCONCLUSIVE'
  out['engineering_review_required']=out['status'] in ('FAIL','REQUIRES_ENGINEERING_REVIEW')
 except (ValueError,KeyError,TypeError) as error:out['pending'].append(str(error))
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
