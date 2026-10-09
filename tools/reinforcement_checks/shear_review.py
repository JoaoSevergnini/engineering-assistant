"""Shear-only orchestration. No resistant/normative equations or drawing edits."""
from copy import deepcopy
from dataclasses import asdict
from functools import lru_cache
from types import SimpleNamespace
from moment_diagram import dec
from shear_diagram import ShearDiagram
from shear_coverage import classify_piece,physical_coverage
from bar_scaling import api_provenance

RULES={
 'thirds':'engineer_confirmed_shear_reference_thirds_v1',
 'regions':'engineer_confirmed_refined_drawn_shear_region_check_v1',
 'diameters':'engineer_confirmed_usual_stirrup_diameters_v1',
 'spacing':'engineer_confirmed_usual_minimum_stirrup_spacing_v1',
 'legs':'engineer_confirmed_four_leg_stirrups_for_wide_beams_v1',
 'domain':'engineer_confirmed_tqs_shear_domain_v1',
 'depth':'engineer_confirmed_shear_effective_depth_max_layers_v1'}


def control(passes=None,**data):
 return {'status':'INCONCLUSIVE' if passes is None else 'PASS' if passes else 'FAIL','passes':passes,**data}

def practice(ok,reason=None,**data):
 return {'status':'PASS' if ok else 'REQUIRES_ENGINEERING_REVIEW','reason':reason,**data}

@lru_cache(None)
def _source(function):return api_provenance(function)

def public_shear_api():
 import concretopy
 from concretopy.verificacoes import dimensionar_cortante_viga
 from concretopy.normas import espacamento_max_estribo_vigas_cm
 from concretopy.detalhamento import calcular_espacamento_equivalente
 return SimpleNamespace(SecaoRetangular=concretopy.SecaoRetangular,Concreto=concretopy.Concreto,
  Aco=concretopy.Aco,Barra=concretopy.Barra,RompimentoBielaCompressao=concretopy.RompimentoBielaCompressao,
  dimensionar_cortante_viga=dimensionar_cortante_viga,
  espacamento_max_estribo_vigas_cm=espacamento_max_estribo_vigas_cm,
  calcular_espacamento_equivalente=calcular_espacamento_equivalente)


def select_shear_depth(regions):
 """Use returned physical centroid/As/layers, never recompute geometry."""
 candidates=[]
 for region in regions:
  for item in region.get('result',{}).get('regions',[]):
   result=item.get('concretopy',{})
   layers=item.get('configuration',{}).get('layers',[])
   if result.get('d_equivalente_cm') is None or not layers:continue
   area=sum(layer['count']*layer['area_unit_cm2'] for layer in layers) if all('area_unit_cm2' in x for x in layers) else result.get('as_total_cm2')
   if area is None:continue
   candidates.append({'layers':len(layers),'As_cm2':area,'d_cm':result['d_equivalente_cm'],
    'provenance':{'span':region['span'],'interval_m':[region['start_m'],region['end_m']],
      'marks':region.get('marks'),'configuration':deepcopy(item['configuration']),'concretopy':deepcopy(result)}})
 out={'rule':RULES['depth'],'candidates':candidates,'d_cm':None,'status':'INCONCLUSIVE',
  'selection':'maximum occupied layers, then maximum total As, then minimum returned centroid d'}
 if not candidates:return out
 selected=min(candidates,key=lambda c:(-c['layers'],-c['As_cm2'],c['d_cm']))
 out.update(status='PASS',d_cm=selected['d_cm'],selected=deepcopy(selected),
  governing=[deepcopy(c) for c in candidates if (c['layers'],c['As_cm2'],c['d_cm'])==(selected['layers'],selected['As_cm2'],selected['d_cm'])])
 return out


def section_with_depth(context,api,diameter):
 """Public SecaoRetangular subtype: preserve real section, override only d.

 Effective centroid is already selected externally from Concretopy flexure.
 No equivalent diameter, repositioning or resistant formula. Scope nk=mk=0.
 """
 selected=context.get('effective_depth')
 if not selected or selected.get('status')!='PASS' or not selected.get('selected'):
  raise ValueError('shear_effective_depth_unresolved')
 d=selected['d_cm'];section=deepcopy(context['section']);section['diametro_estribo_mm']=diameter
 if not 0<d<section['h']:raise ValueError('invalid_explicit_shear_depth')
 class ExplicitDepthSection(api.SecaoRetangular):
  def d(self,diametro_barra_mm=12.5):return d
 return ExplicitDepthSection(**section)


def _call(context,api,section,vk):
 return api.dimensionar_cortante_viga(section,api.Concreto(context['fck_mpa']),api.Aco(context['fyk_mpa']),vk,
  alfa_graus=90,nk=0,mk=0,**{k:context[k] for k in ('gamma_f','gamma_c','gamma_s')})


def design_shear(context,api,vk,diameter):
 out={'status':'INCONCLUSIVE','diagonal_compression':control(),'diagnostics':[],
  'units':{'forces':'kN','Asw_per_s':'cm2/m','spacing':'cm','d':'cm'}}
 try:
  if dec(vk)<0 or dec(diameter)<=0:raise ValueError('invalid_shear_or_stirrup_diameter')
  if context.get('axial_force_kn',0)!=0 or context.get('stirrup_angle_degrees',90)!=90:
   raise ValueError('axial_or_inclined_stirrup_context_not_supported')
  if any(dec(context[k])<=0 for k in ('gamma_f','gamma_c','gamma_s')):raise ValueError('invalid_partial_factor')
  section=section_with_depth(context,api,diameter)
  minimum=_call(context,api,section,0);vsd=vk*context['gamma_f']
  out.update(Vsk_abs_kn=vk,Vsd_kn=vsd,VRd2_kn=minimum.vrd2,Vc_kn=minimum.vc,
   d_cm=section.d(),minimum_Asw_per_s_cm2_m=minimum.asw_por_s,
   provenance={'api':deepcopy(_source(api.dimensionar_cortante_viga)),
    'minimum_call':{'Vk_kn':0,'result':asdict(minimum)},'effective_depth':deepcopy(context['effective_depth']),
    'physical_section':deepcopy(context['section']),'stirrup_diameter_mm':diameter,
    'explicit_depth_adapter':'SecaoRetangular subtype; original bw/h/cover retained; nk=mk=0; no equivalent diameter'})
  out['diagonal_compression']=control(minimum.vrd2>vsd,Vsk_abs_kn=vk,Vsd_kn=vsd,VRd2_kn=minimum.vrd2,
   utilization=vsd/minimum.vrd2,criterion='strict VRd2 > Vsd; Concretopy throws at equality')
  try:result=_call(context,api,section,vk)
  except api.RompimentoBielaCompressao:
   out.update(status='FAIL',required_Asw_per_s_cm2_m=None,governing_Asw_per_s_cm2_m=None,
    maximum_spacing_code_cm=None);out['diagnostics'].append('diagonal_compression_failure_not_resolved_by_more_stirrups');return out
  # Public normative call receives the ACTUAL design capacity and same d.
  geometry=SimpleNamespace(secao=section,vrd2_kn=result.vrd2)
  maximum=api.espacamento_max_estribo_vigas_cm(geometry,vsd)
  out.update(status='PASS',concretopy=asdict(result),required_Asw_per_s_cm2_m=result.asw_por_s,
   governing_Asw_per_s_cm2_m=result.asw_por_s,required_by_shear_separately_cm2_m=None,
   required_components_note='API returns governing value only; minimum obtained by independent zero-Vk call',
   requirement_governed_by='MINIMUM' if result.asw_por_s==minimum.asw_por_s else 'SHEAR',maximum_spacing_code_cm=maximum)
  out['provenance']['maximum_spacing_api']=deepcopy(_source(api.espacamento_max_estribo_vigas_cm))
  out['provenance']['maximum_spacing_capacity_basis']='same VRd2 and effective d as current shear call, not VigaRetangular default depth/gamma_c'
 except (ValueError,KeyError,TypeError) as e:out['diagnostics'].append(str(e))
 return out


def reference_options(context,api,vk,legs,diameters=(5,6.3,8)):
 options=[]
 if type(legs)!=int or legs<1:return {'status':'INCONCLUSIVE','reason':'reference_legs_unresolved','options':options}
 for phi in diameters:
  design=design_shear(context,api,vk,phi)
  item={'diameter_mm':phi,'legs':legs,'design':design,'status':design['status']}
  if design['status']=='PASS':
   area=legs*api.Barra(phi).area_cm2
   # Geometric Asw/s identity only, not a resistant equation.
   resistance_spacing=100*area/design['governing_Asw_per_s_cm2_m']
   maximum=min(resistance_spacing,design['maximum_spacing_code_cm'])
   item.update(max_spacing_by_resistance_cm=resistance_spacing,max_spacing_code_cm=design['maximum_spacing_code_cm'],
    max_spacing_cm=maximum,usual=maximum>=8 and phi in (5,6.3,8),practical_spacing_api_cm=api.calcular_espacamento_equivalente(design['governing_Asw_per_s_cm2_m']/legs,phi),
    status='PASS' if maximum>=8 and phi in (5,6.3,8) else 'REQUIRES_ENGINEERING_REVIEW')
  options.append(item)
 usual=any(o.get('usual') for o in options)
 state='PASS' if usual else 'FAIL' if any(o['design']['status']=='FAIL' for o in options) else 'INCONCLUSIVE' if any(o['design']['status']=='INCONCLUSIVE' for o in options) else 'REQUIRES_ENGINEERING_REVIEW'
 return {'status':state,'options':options,'usual_solution_exists':usual,
  'reasons':[] if usual else ['STIRRUP_SPACING_BELOW_USUAL_LIMIT','LARGER_STIRRUP_DIAMETER_REQUIRED'] if state=='REQUIRES_ENGINEERING_REVIEW' else [],
  'selected_solution':None}


def shear_reference_design(shear,context,api,*,span_id,legs,diameters=(5,6.3,8)):
 a,b=map(dec,shear.domain);step=(b-a)/3;thirds=[]
 for i in range(3):
  start=float(a+i*step);end=float(b if i==2 else a+(i+1)*step)
  demand=shear.maximum(start,end)
  options=reference_options(context,api,demand['Vsk_abs_kn'],legs,diameters) if demand['complete'] else {'status':'INCONCLUSIVE','options':[]}
  thirds.append({'region':i+1,'interval_m':[start,end],'demand':demand,'reference_options':options})
 return {'verification':'SHEAR_REFERENCE_DESIGN','span_id':span_id,'domain_m':deepcopy(shear.domain),
  'thirds':thirds,'rule':RULES['thirds'],'boundary_policy':'closed intervals; boundary may govern both neighbours; deterministic; drawing transitions unconstrained'}


def inverse_shear_capacity(context,api,diameter,provided):
 """Invert only the public calculation in LOAD space; no diagram discretizing."""
 section=section_with_depth(context,api,diameter);minimum=_call(context,api,section,0)
 out={'status':'INCONCLUSIVE','calls':[{'Vk_kn':0,'result':asdict(minimum)}],
  'method':'bisection of public Concretopy demand in Vk-space; analytic diagram crossings afterwards'}
 if provided<minimum.asw_por_s:
  out['reason']='provided_below_minimum_never_sufficient';return out
 low=0.;high=minimum.vrd2/context['gamma_f']*(1-1e-12)
 endpoint=_call(context,api,section,high);out['calls'].append({'Vk_kn':high,'result':asdict(endpoint)})
 if endpoint.asw_por_s<=provided:
  out['reason']='inverse_limit_governed_by_strict_diagonal_compression_not_stirrup_area';return out
 for _ in range(60):
  mid=(low+high)/2;result=_call(context,api,section,mid)
  out['calls'].append({'Vk_kn':mid,'result':asdict(result)})
  if result.asw_por_s<=provided:low=mid
  else:high=mid
 out.update(status='PASS',Vk_capacity_kn=low,upper_bound_kn=high)
 return out


def transition_check(shear,capacity,*,drawn_x,side,branch_domain=None):
 """Candidates are physical declines of |V| in the declared orientation."""
 out={'status':'INCONCLUSIVE','drawn_position_m':drawn_x,'side':side,'candidates':[],
  'theoretical_limit_m':None,'margin_cm':None,'drawing_changed':False}
 if side not in ('LEFT','RIGHT'):out['reason']='transition_side_unresolved';return out
 direction=1 if side=='LEFT' else -1
 a,b=branch_domain or shear.domain
 coverage=shear.maximum(a,b)
 if not coverage['complete']:out['reason']='transition_branch_gap_or_domain_unresolved';return out
 candidates=[]
 for crossing in shear.capacity_crossings(capacity):
  e=crossing['event']
  if e['status']!='crossing':
   if e.get('x_end_m',b)<a or e.get('x_start_m',a)>b:continue
   out['candidates'].append(crossing);out['reason']='capacity_plateau_ambiguous';return out
  x=e['x_m']
  if not a<=x<=b:continue
  signed=1 if crossing['signed_limit_kn']>=0 else -1
  compatible=any((1 if s['direction']=='increasing' else -1 if s['direction']=='decreasing' else 0)*signed*direction<0 for s in e['segments'])
  if compatible:candidates.append(crossing)
 out['candidates']=candidates
 counts={identity:sum(c['series_id']==identity for c in candidates) for identity,_ in shear.diagrams}
 if any(n>1 for n in counts.values()):out['reason']='multiple_compatible_crossings_in_same_branch';return out
 # A series with no crossing must already be sufficient throughout this branch.
 for identity,diagram in shear.diagrams:
  if counts[identity]==0:
   one=ShearDiagram([s for s in shear.series if s.get('series_id',s.get('envelope'))==identity]).maximum(a,b)
   if one['Vsk_abs_kn']>capacity:out['reason']='series_insufficient_throughout_branch';return out
 if not candidates:out.update(status='NOT_APPLICABLE',reason='all_series_sufficient_throughout_branch');return out
 selected=max(candidates,key=lambda c:direction*c['event']['x_m'])
 x=selected['event']['x_m']
 # Verify the suffix after the selected decline: a later rise must not be hidden.
 for identity,linear in shear.diagrams:
  positions={dec(b if direction==1 else a),*[q for q in linear.xs if (dec(x)<q<=dec(b) if direction==1 else dec(a)<=q<dec(x))]}
  if any(abs(linear.moment_at_x(float(q))['value_knm'])>capacity for q in positions):
   out['reason']='selected_decline_does_not_prove_sufficient_remaining_branch';return out
 margin=direction*(drawn_x-x)*100
 out.update(theoretical_limit_m=x,selected_candidates=[c for c in candidates if c['event']['x_m']==x],
  margin_cm=margin,status='PASS' if margin>=0 else 'FAIL',passes=margin>=0,
  reason='last required decline among applicable series in physical orientation; independent analytic series crossings')
 return out


def check_drawn_region(shear,context,api,region):
 classification=classify_piece(region)
 if classification['contributes_to_beam_shear'] is False:
  return {'verification':'SHEAR_DRAWN_REGION_CHECK','region':deepcopy(region),'classification':classification,
   'overall_structural_result':'NOT_APPLICABLE','checks':{},'engineering_review_required':False,
   'suspension_result':'NOT_EVALUATED','selected_solution':None,'detailing_optimization':None}
 out={'verification':'SHEAR_DRAWN_REGION_CHECK','region':deepcopy(region),'checks':{},
  'overall_structural_result':'INCONCLUSIVE','engineering_review_required':False,'limitations':[],
  'suspension_check_required':bool(region.get('indirect_support_evidence')),
  'suspension_result':'NOT_EVALUATED','selected_solution':None,'detailing_optimization':None,'rule':RULES['regions']}
 names=('diagonal_compression','shear_reinforcement','maximum_code_spacing','usual_minimum_spacing','usual_diameter','number_of_legs','stirrup_holder')
 out['checks']={name:control() for name in names}
 try:
  if not region.get('source'):raise ValueError('drawn_region_source_missing')
  a,b=region['interval_m'];demand=shear.maximum(a,b,allow_intersection=True);out['demand']=demand
  phi,spacing,legs=(region.get(k) for k in ('diameter_mm','spacing_cm','legs'))
  if phi is None or spacing is None or dec(phi)<=0 or dec(spacing)<=0:raise ValueError('stirrup_diameter_or_spacing_unresolved')
  out['checks']['usual_minimum_spacing']=practice(spacing>=8,'STIRRUP_SPACING_BELOW_USUAL_LIMIT',limit_cm=8,drawn_cm=spacing,rule=RULES['spacing'])
  out['checks']['usual_diameter']=practice(phi in (5,6.3,8),'LARGER_STIRRUP_DIAMETER_OUTSIDE_USUAL_SET',rule=RULES['diameters'])
  valid_legs=type(legs)==int and legs>0
  if not valid_legs:out['checks']['number_of_legs']=control(reason='effective_shear_legs_not_confirmed')
  else:
   out['checks']['number_of_legs']=practice(not (context['section']['bw']>40 and legs!=4),
    'WIDE_BEAM_OUTSIDE_USUAL_FOUR_LEGS',drawn_legs=legs,expected_usual_legs=4 if context['section']['bw']>40 else None,rule=RULES['legs'])
   area=api.Barra(phi).area_cm2
   out['provided']={'Asw_cm2':area*legs,'Asw_per_s_cm2_m':area*legs*100/spacing,
    'diameter_mm':phi,'spacing_cm':spacing,'legs':legs,'area_unit_cm2':area,
    'provenance':{'bar':'Concretopy.Barra.area_cm2','geometry':deepcopy(region['source'])}}
  if legs==4:
   holder=region.get('holder_compatibility')
   out['checks']['stirrup_holder']=control(holder['passes'],provenance=deepcopy(holder)) if holder and holder.get('provenance') and isinstance(holder.get('passes'),bool) else control(reason='four_leg_holder_physical_disposition_unresolved')
  elif valid_legs:out['checks']['stirrup_holder']={'status':'NOT_APPLICABLE','passes':None,'reason':'specific four-leg holder check not applicable; other longitudinal reviews preserved'}
  if demand['Vsk_abs_kn'] is None:raise ValueError('no_valid_shear_intersection')
  design=design_shear(context,api,demand['Vsk_abs_kn'],phi);out['design']=design
  out['checks']['diagonal_compression']=deepcopy(design['diagonal_compression'])
  if design['status']=='PASS':
   required=design['governing_Asw_per_s_cm2_m']
   if valid_legs:out['checks']['shear_reinforcement']=control(out['provided']['Asw_per_s_cm2_m']>=required,
    required_cm2_m=required,provided_cm2_m=out['provided']['Asw_per_s_cm2_m'])
   out['checks']['maximum_code_spacing']=control(spacing<=design['maximum_spacing_code_cm'],limit_cm=design['maximum_spacing_code_cm'],drawn_cm=spacing,
    provenance=design['provenance']['maximum_spacing_api'])
   if valid_legs and region.get('transition'):
    inverse=inverse_shear_capacity(context,api,phi,out['provided']['Asw_per_s_cm2_m']);out['inverse_capacity']=inverse
    if inverse['status']=='PASS':out['transition']=transition_check(shear,inverse['Vk_capacity_kn'],**region['transition'])
    else:out['transition']={'status':'INCONCLUSIVE','reason':inverse['reason'],'drawing_changed':False}
  required_checks=[out['checks'][n] for n in ('diagonal_compression','shear_reinforcement','maximum_code_spacing','number_of_legs','stirrup_holder')]
  out['overall_structural_result']='FAIL' if any(c['status']=='FAIL' for c in required_checks) else 'INCONCLUSIVE' if not demand['complete'] or any(c['status']=='INCONCLUSIVE' for c in required_checks) else 'PASS'
  out['engineering_review_required']=any(c['status']=='REQUIRES_ENGINEERING_REVIEW' for c in out['checks'].values())
  if not demand['complete']:out['limitations'].append('partial_TQS_coverage_only_known_intersection_checked')
 except (ValueError,KeyError,TypeError) as e:out['limitations'].append(str(e))
 return out


def review_shear_spans(spans,context,api):
 out={'shear_reference_design':[],'shear_drawn_regions':[],'structural_failures':[],
  'engineering_review_items':[],'inconclusive_items':[],'excluded_reinforcement':[],'coverage_reviews':[],'suspension_not_evaluated':True,
  'global_shear_approval':None,'selected_solution':None,'detailing_optimization':None,'provenance':{'rules':deepcopy(RULES),'context':deepcopy(context)}}
 for span in spans:
  try:shear=ShearDiagram(span['series'])
  except (ValueError,KeyError,TypeError) as error:
   out['inconclusive_items'].append({'span':span.get('span_id'),'reason':str(error)});continue
  reference=shear_reference_design(shear,context,api,span_id=span['span_id'],legs=span.get('reference_legs'))
  out['shear_reference_design'].append(reference)
  for third in reference['thirds']:
   options=third['reference_options']
   if options['status']=='REQUIRES_ENGINEERING_REVIEW':out['engineering_review_items'].append({'span':span['span_id'],'reference_third':third['region'],'reason':options.get('reasons')})
   if any(o.get('design',{}).get('diagonal_compression',{}).get('status')=='FAIL' for o in options.get('options',[])):
    out['structural_failures'].append({'span':span['span_id'],'reference_third':third['region'],'checks':['diagonal_compression']})
  regions=[]
  for piece in span.get('drawn_regions',[]):
   classification=classify_piece(piece)
   if classification['contributes_to_beam_shear'] is False:
    out['excluded_reinforcement'].append({'span_id':span['span_id'],'piece':deepcopy(piece),'classification':classification})
    continue
   if classification['status']=='INCONCLUSIVE':
    out['inconclusive_items'].append({'span':span['span_id'],'region':piece.get('id'),'reason':classification['reason']})
    continue
   regions.append(piece)
  for region in regions:
   check=check_drawn_region(shear,context,api,region);check['span_id']=span['span_id'];out['shear_drawn_regions'].append(check)
   if check['overall_structural_result']=='FAIL':out['structural_failures'].append({'span':span['span_id'],'region':region.get('id'),'checks':[k for k,c in check['checks'].items() if c['status']=='FAIL']})
   if check['overall_structural_result']=='INCONCLUSIVE':out['inconclusive_items'].append({'span':span['span_id'],'region':region.get('id'),'reason':'necessary_drawn_region_control_unresolved'})
   if check['engineering_review_required']:out['engineering_review_items'].append({'span':span['span_id'],'region':region.get('id'),'checks':[k for k,c in check['checks'].items() if c['status']=='REQUIRES_ENGINEERING_REVIEW']})
  coverage=physical_coverage(span,shear.domain,regions);coverage['span_id']=span['span_id']
  out['coverage_reviews'].append(coverage)
  if coverage['status']=='INCONCLUSIVE':
   out['inconclusive_items'].append({'span':span['span_id'],'reason':coverage.get('reason','required_physical_coverage_unresolved'),
    'uncovered_required_intervals_m':coverage['uncovered_required_intervals_m'],
    'overlapping_required_intervals_m':coverage['overlapping_required_intervals_m']})
 out['global_shear_approval']=False if out['structural_failures'] else None if out['inconclusive_items'] or not out['shear_drawn_regions'] else True
 return out
