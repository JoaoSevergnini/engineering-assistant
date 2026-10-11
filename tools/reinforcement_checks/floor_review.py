"""Mandatory documentary/physical pipeline for complete-floor reviews.

Existing checkers are injected as explicit adapters: adapter(payload) -> result.
No adapter is invoked before preflight. Historical scripts remain unchanged.
"""
from copy import deepcopy
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
for part in ('beam_model', 'beam_mapping', 'extrator_lst'):
    sys.path.insert(0, str(ROOT / 'tools' / part))
from input_evidence import fact
from consolidar_detalhamento import transform
from documentary_reconciliation import reconcile
from pdf_observations import extract_zones
from physical_geometry import project_occurrences
from form_geometry import apply_form
from common_axis_registration import register_span
from input_preflight import CONTROLS, preflight, execute, prepare_local_batches
from layer_interpretation import interpret_layers, local_layer_fit
from beam_diagnostic import consolidate, aggregate

STAGES = ('DOCUMENTARY_EXTRACTION', 'RECONCILIATION', 'FORM_PHYSICAL_MODEL', 'COMMON_AXIS_REGISTRATION',
          'LAYER_INTERPRETATION', 'INPUT_PREFLIGHT', 'EXISTING_CHECKERS', 'DIAGNOSTIC_CONSOLIDATION')


def flexure_adapter(payload):
    """Use existing resistant engine with the proved local section and TQS envelope."""
    from moment_diagram import MomentDiagram
    from longitudinal_review import check_flexure_regions
    from input_preflight import overlaps
    job, model, span = payload['job'], payload['model'], payload['registered_span']
    sign = 'POSITIVE' if job['control'] == 'positive_flexure' else 'NEGATIVE'
    series = moment_series(span, sign)
    diagram = MomentDiagram([dict(section=i+1, x_m=x, value_knm=v, source_type='tqs_section',
        provenance=dict(series=series, span_id=span['id'])) for i,(x,v) in enumerate(zip(series['positions'], series['values']))],
        dict(policy='TQS_ENVELOPES', series=series, discontinuities_m=series.get('discontinuities_m', [])))
    a,z = job['interval_m']
    section = next(s for s in model['physical_geometry']['segments'] if s['x_start_m']['value'] <= a and s['x_end_m']['value'] >= z)
    geo = section['geometry']
    context = deepcopy(job['context'])
    context.pop('section_span', None)
    context['section'] = {k: geo[v]['value'] for k,v in dict(bw='width_cm',h='height_cm',cobrimento='cover_cm',diametro_estribo_mm='stirrup_diameter_mm').items()}
    context.update(layer_order_basis='from_tension_face', layer_order_provenance=[b['layers'] for b in model['physical_geometry']['occurrences']])
    function = 'positive' if sign=='POSITIVE' else 'negative'
    bars = [b for b in payload['bars'] if b['function']==function and overlaps(b['x_start_common'],b['x_end_common'],a,z)]
    return check_flexure_regions(bars, context, diagram, payload['api'], flexure_sign=sign,
                                domain=job.get('moment_search_interval_m', [a,z]))


def review_constant_sections(model, registered, case, api):
    """Engineer's physical-Vk / expanded-M procedure, using existing checkers."""
    from dataclasses import asdict
    from input_evidence import validate_fact, PROVED
    from moment_diagram import MomentDiagram
    from shear_diagram import ShearDiagram
    from shear_review import select_shear_depth, public_shear_api, check_drawn_region, RULES
    from bar_scaling import api_provenance
    settings=deepcopy(case.get('section_checks', {})); sections=[]; bars=project_occurrences(model)
    inputs_by_control=case.get('control_inputs', {})
    out=dict(sections=sections, local_discontinuity_approval=None, beam_approval=None,
             pending_transitions=deepcopy(model.get('form_interpretation', {}).get('transitions', [])),pending_segments=[])
    def proved(item, unit=None):
        try:return bool(item) and validate_fact(item,unit)['state'] in PROVED
        except (ValueError,TypeError,KeyError):return False
    def evidence(value, source):return fact(value,state='DOCUMENTED_CONFIRMED',provenance=[source])
    if 'domains' not in settings:
        settings['domains']=[]
        for span in model['physical_geometry'].get('spans', []):
            bounds=span.get('physical_bounds', {})
            if all(bounds.get(k,{}).get('state')=='DOCUMENTED_CONFIRMED' for k in ('x_start_m','x_end_m')):
                settings['domains'].append(dict(span_id=span['id'],interval_m=fact([bounds[k]['value'] for k in ('x_start_m','x_end_m')],
                    state='DOCUMENTED_CONFIRMED',unit='m',provenance=[dict(physical_span=span)])))
    for segment in model['physical_geometry']['segments']:
        if segment['geometry_type']!='CONSTANT' or not all(proved(segment[k]) for k in ('x_start_m','x_end_m')):
            out['pending_segments'].append(dict(segment_id=segment['id'],geometry_type=segment['geometry_type'],
                x_start_m=deepcopy(segment['x_start_m']),x_end_m=deepcopy(segment['x_end_m']),reason='constant_section_with_proved_bounds_required'));continue
        a,z=[segment[k]['value'] for k in ('x_start_m','x_end_m')];sid=segment['id']
        item=dict(segment_id=sid,physical_interval_m=[a,z],geometry=deepcopy(segment['geometry']),
                  provenance=deepcopy(segment['provenance']),diagnostics=[],physical_flexure=[],expanded_flexure=[],shear_checks=[])
        sections.append(item)
        domains=[d for d in settings.get('domains', []) if proved(d.get('interval_m'),'m') and
                 d['interval_m']['value'][0]<=a<z<=d['interval_m']['value'][1]]
        if len(domains)!=1:
            item['diagnostics'].append('unique_documented_applicable_domain_required');continue
        domain=domains[0];span=registered.get(str(domain['span_id']))
        item['applicable_domain']=deepcopy(domain)
        if not span:
            item['diagnostics'].append('registered_TQS_span_required');continue
        span=deepcopy(span)
        jumps=domain.get('discontinuities_m', [])
        if any(not proved(j,'m') for j in jumps):
            item['diagnostics'].append('discontinuity_position_unproved');continue
        for s in span['internal_forces']:
            if s.get('quantity')=='shear':s['discontinuities_m']=s.get('discontinuities_m', [])+[j['value'] for j in jumps]
        context=deepcopy(settings.get('contexts', {}).get(sid,case.get('context', {})))
        context.pop('section_span',None)
        context['section']={k:segment['geometry'][v]['value'] for k,v in dict(bw='width_cm',h='height_cm',cobrimento='cover_cm',diametro_estribo_mm='stirrup_diameter_mm').items()}
        context.setdefault('longitudinal_provenance',dict(physical_segment=deepcopy(segment)))
        inputs_by_control=case.get('control_inputs', {})
        mapping=evidence(True,span['internal_forces'][0]['mapping_provenance']) if span['internal_forces'][0].get('mapping_provenance') else fact()
        try:
            ss=[{**deepcopy(s),'provenance':dict(series=deepcopy(s))} for s in span['internal_forces'] if
                s.get('quantity')=='shear' and s.get('stage')=='model_input' and s.get('unit')=='kN' and s.get('envelope') in ('max','min') and s.get('sources')]
            if len(ss)!=2 or {s['envelope'] for s in ss}!={'max','min'}:raise ValueError('both_unique_TQS_shear_envelopes_required')
            shear=ShearDiagram(ss);selected=shear.maximum(a,z);item['shear_selection']=selected
        except (ValueError,KeyError,TypeError) as error:
            item['diagnostics'].append(str(error));continue
        moment_diagrams={}
        for control,sign in (('positive_flexure','POSITIVE'),('negative_flexure','NEGATIVE')):
            try:
                series=moment_series(span,sign)
                diagram=MomentDiagram([dict(section=i+1,x_m=x,value_knm=v,provenance=dict(series=series)) for i,(x,v) in enumerate(zip(series['positions'],series['values']))],dict(series=series,discontinuities_m=series.get('discontinuities_m', [])))
                moment_diagrams[control]=diagram
                item.setdefault('physical_moment_extrema', {})[control]=diagram.extrema(a,z)
            except (ValueError,KeyError,TypeError) as error:item['diagnostics'].append(str(error))
        physical_jobs=[];depth_candidates=[]
        def flexure_job(control, interval, search=None):
            sign='POSITIVE' if control=='positive_flexure' else 'NEGATIVE'
            inputs=deepcopy(inputs_by_control.get(control, {}))
            inputs['force_position_mapping']=mapping
            diagram=moment_diagrams.get(control)
            selection=diagram.extrema(*(search or interval)) if diagram else None
            inputs['moment_envelope']=evidence(selection,dict(span_id=span['id'])) if selection and selection['complete'] else fact()
            fit=local_layer_fit(model,interval,control,api) if api else dict(fits=None,diagnostics=['API_unavailable'])
            inputs['layer_fit']=evidence(fit['fits'],fit) if fit['fits'] is not None else fact()
            job=dict(id=sid+'-'+control,control=control,span_id=span['id'],interval_m=interval,context=context)
            if search:job['moment_search_interval_m']=search
            plan=preflight(model,region_id=job['id'],interval_m=interval,control=control,inputs=inputs)
            if not api:_pending(plan,'resistant_API_unavailable')
            if any(context.get(k) is None for k in ('fck_mpa','fyk_mpa','gamma_f','gamma_c','gamma_s')):_pending(plan,'resistant_context_unavailable')
            function='positive' if sign=='POSITIVE' else 'negative'
            own=[b for b in bars if b['function']==function and b['x_start_common'] is not None and b['x_end_common'] is not None and
                 b['x_start_common']<interval[1] and b['x_end_common']>interval[0]]
            if search and any(b['x_start_common']>search[0] or b['x_end_common']<search[1] for b in own):
                _pending(plan,'longitudinal_continuity_not_proved_for_expanded_search')
            result=execute(plan,flexure_adapter,dict(model=model,job=job,registered_span=span,bars=own,api=api))
            return dict(control=control,physical_interval_m=interval,moment_search_interval_m=search or interval,
                        selected_moments=selection,marks=[b['mark'] for b in own],**result)
        # Physical flexure supplies the existing, evidence-backed selection of d.
        for control,sign in (('positive_flexure','POSITIVE'),('negative_flexure','NEGATIVE')):
            for region in prepare_local_batches(model,flexure_sign=sign)['regions']:
                ra,rb=max(a,region['x_start_m']),min(z,region['x_end_m'])
                if ra>=rb:continue
                baseline=flexure_job(control,[ra,rb]);item['physical_flexure'].append(baseline);physical_jobs.append((control,[ra,rb]))
                if baseline['result']:
                    depth_candidates.append(dict(span=span['id'],start_m=ra,end_m=rb,result=baseline['result'],marks=baseline['marks']))
        explicit=settings.get('effective_depths', {}).get(sid)
        if explicit is not None:
            try:
                explicit=validate_fact(explicit,'cm')
                if explicit['state'] not in PROVED or type(explicit['value']) not in (int,float) or not 0<explicit['value']<context['section']['h']:
                    raise ValueError('proved_physical_effective_depth_required')
                depth_fact=explicit;depth=dict(status='PASS',d_cm=explicit['value'],selected=dict(provenance=explicit))
            except (ValueError,KeyError,TypeError) as error:
                item['diagnostics'].append(str(error));depth_fact=fact(unit='cm',provenance=[dict(invalid_depth=explicit)])
                depth=dict(status='INCONCLUSIVE',d_cm=None,selected=None)
        else:
            depth=select_shear_depth(depth_candidates)
            if not item['physical_flexure'] or any(e['execution_state']=='NOT_EXECUTED' for e in item['physical_flexure']):
                depth.update(status='INCONCLUSIVE',d_cm=None,selected=None,reason='all_physical_layer_compositions_required_for_depth_selection')
            depth_fact=fact(depth['d_cm'],state='INFERRED_EXPLICIT_CONVENTION',provenance=[depth],
                criterion=dict(origin='OFFICE_STANDARD',reference=RULES['depth']),unit='cm') if depth['d_cm'] is not None else fact(unit='cm',provenance=[depth])
        context['effective_depth']=depth;item['effective_depth']=deepcopy(depth_fact)
        al_inputs=deepcopy(inputs_by_control.get('shear', {}))
        al_inputs.update(force_position_mapping=mapping,effective_depth=depth_fact,
            shear_envelope=evidence(selected,dict(series=ss)) if selected['complete'] else fact(provenance=[selected]))
        al_inputs['al_scope']=evidence(True,context['al_scope_provenance']) if context.get('al_scope_confirmed') is True and context.get('al_scope_provenance') and context.get('stirrup_angle_degrees')==90 and context.get('axial_force_kn')==0 else fact()
        plan=preflight(model,region_id=sid+'-al',interval_m=[a,z],control='shear',inputs=al_inputs,al_only=True)
        if not api:_pending(plan,'resistant_API_unavailable')
        if any(context.get(k) is None for k in ('fck_mpa','gamma_f','gamma_c')):_pending(plan,'al_context_unavailable')
        def calculate_al():
            try:
                value=api.calcular_al(concreto=api.Concreto(context['fck_mpa']),b_cm=context['section']['bw'],d_cm=depth['d_cm'],
                    vk_abs_kn=selected['Vsk_abs_kn'],gamma_f=context['gamma_f'],gamma_c=context['gamma_c'])
                return dict(status='PASS',parameters=asdict(value),api=api_provenance(api.calcular_al),physical_interval_m=[a,z])
            except (ValueError,KeyError,TypeError) as error:return dict(status='INCONCLUSIVE',diagnostics=[str(error)])
        item['al']=execute(plan,calculate_al)
        search=None
        if item['al']['status']=='PASS':
            shift=item['al']['result']['parameters']['al_cm']/100
            neighbours=[s for s in model['physical_geometry']['segments'] if s['id']!=sid and s['geometry_type']=='CONSTANT' and
                        all(proved(s[k]) for k in ('x_start_m','x_end_m')) and domain['interval_m']['value'][0]<=s['x_start_m']['value']<s['x_end_m']['value']<=domain['interval_m']['value'][1]]
            left=any(abs(s['x_end_m']['value']-a)<1e-8 for s in neighbours)
            right=any(abs(s['x_start_m']['value']-z)<1e-8 for s in neighbours)
            lo,hi=domain['interval_m']['value'];search=[max(lo,a-shift if left else a),min(hi,z+shift if right else z)]
            # Documented effort discontinuities bound influence; never cross them.
            for jump in jumps:
                x=jump['value']
                if a<x<z:
                    search=None;item['diagnostics'].append('physical_segment_crosses_effort_discontinuity');break
                if x<=a:search[0]=max(search[0],x)
                if x>=z:search[1]=min(search[1],x)
            for transition in out['pending_transitions']:
                bounds=transition.get('physical_interval_m')
                if bounds and transition.get('position_state')!='PROVED' and max(domain['interval_m']['value'][0],bounds[0])<min(domain['interval_m']['value'][1],bounds[1]) and (bounds[0]<=z<=bounds[1] or bounds[0]<=a<=bounds[1]):
                    search=None;item['diagnostics'].append('transition_position_unproved_for_expanded_search')
        item['moment_search_interval_m']=search
        if search:
            item['expanded_moment_extrema']={c:d.extrema(*search) for c,d in moment_diagrams.items()}
            for control,interval in physical_jobs:
                local=[search[0] if interval[0]==a else interval[0],search[1] if interval[1]==z else interval[1]]
                item['expanded_flexure'].append(flexure_job(control,interval,local))
        else:item['diagnostics'].append('expanded_moment_search_pending_al_or_geometry')
        pieces=[]
        for original in settings.get('drawn_stirrup_regions', []):
            ra,rb=original['interval_m'];ra,rb=max(a,ra),min(z,rb)
            if ra<rb:pieces.append({**deepcopy(original),'interval_m':[ra,rb]})
        events=sorted({a,z,*[x for p in pieces for x in p['interval_m']]})
        complete=bool(pieces) and all(sum(p['interval_m'][0]<=(x+y)/2<=p['interval_m'][1] for p in pieces)==1 for x,y in zip(events,events[1:]))
        for piece in pieces:
            inputs=deepcopy(al_inputs);inputs['stirrup_regions']=evidence(pieces,dict(physical_interval_m=[a,z]))
            plan=preflight(model,region_id=sid+'-shear-'+piece['id'],interval_m=piece['interval_m'],control='shear',inputs=inputs)
            if not complete:_pending(plan,'complete_unambiguous_stirrup_coverage_required')
            if not api:_pending(plan,'resistant_API_unavailable')
            check=execute(plan,check_drawn_region,shear,context,public_shear_api() if api else None,piece,demand_interval_m=[a,z])
            item['shear_checks'].append(dict(physical_interval_m=piece['interval_m'],shear_search_interval_m=[a,z],**check))
        if not complete:item['diagnostics'].append('complete_unambiguous_stirrup_coverage_required')
        item['local_context']=context
    # Additional suspension of shear at lower-bottom steps, not indirect support.
    from suspension_review import classify_bottom_change,review_bottom_step
    out['bottom_step_suspension']=[]
    physical={s['id']:s for s in model['physical_geometry']['segments']}
    ordered=sorted(sections,key=lambda s:s['physical_interval_m'][0])
    for left_item,right_item in zip(ordered,ordered[1:]):
        left,right=[physical[s['segment_id']] for s in (left_item,right_item)]
        classification=classify_bottom_change(left,right)
        identity=left['id']+'--'+right['id']
        report=dict(transition_id=identity,classification=classification,local_discontinuity_approval=None)
        if classification['status']=='NOT_APPLICABLE':
            application=fact(state='NOT_APPLICABLE',provenance=[classification])
            plan=preflight(model,region_id=identity,interval_m=left_item['physical_interval_m'],control='shear',applicability=application)
            report.update(execute(plan,None),reason='coincident_bottoms_no_extra_suspension')
            out['bottom_step_suspension'].append(report);continue
        transition=deepcopy(next((t for t in settings.get('height_change_transitions',[]) if t.get('left_segment_id')==left['id'] and t.get('right_segment_id')==right['id']),{}))
        x=left['x_end_m']['value']
        if x==right['x_start_m']['value']:
            transition.setdefault('position_m',fact(x,state='DOCUMENTED_CONFIRMED',unit='m',provenance=[dict(adjacent_form_faces=[left['x_end_m'],right['x_start_m']])]))
        else:
            report['position_pending_interval_m']=[x,right['x_start_m']['value']]
            transition.setdefault('position_m',fact(unit='m'))
        transition.setdefault('gamma_n',settings.get('gamma_n',fact()))
        side=classification.get('suspended_side');target=left_item if side=='LEFT' else right_item
        interval=target['physical_interval_m'];ctx=target.get('local_context',{})
        inputs=deepcopy(inputs_by_control.get('shear',{}))
        inputs.update(effective_depth=target.get('effective_depth',fact(unit='cm')),
            shear_envelope=evidence(target.get('shear_selection'),dict(section=target['segment_id'])) if target.get('shear_selection',{}).get('complete') else fact(),
            stirrup_regions=evidence(settings.get('drawn_stirrup_regions'),dict(inventory='documented physical stirrup regions')) if settings.get('drawn_stirrup_regions') else fact(),
            force_position_mapping=evidence(True,dict(registrations=[registered.get(str(s.get('applicable_domain',{}).get('span_id')),{}).get('internal_forces',[]) for s in (left_item,right_item)])) if all(registered.get(str(s.get('applicable_domain',{}).get('span_id')),{}).get('internal_forces',[{}])[0].get('mapping_provenance') for s in (left_item,right_item)) else fact(),
            transition_geometry=evidence(dict(classification=classification,position=transition['position_m']),dict(form_faces=[left,right])) if classification['status']=='PASS' and proved(transition['position_m'],'m') and transition['position_m']['value']==x==right['x_start_m']['value'] else fact(),
            gamma_n=transition['gamma_n'],shear_method_scope=evidence(True,ctx['al_scope_provenance']) if ctx.get('al_scope_confirmed') is True and ctx.get('axial_force_kn')==0 and ctx.get('stirrup_angle_degrees')==90 and ctx.get('al_scope_provenance') else fact())
        if transition.get('shear_sides'):
            records=[v for side_values in transition['shear_sides'].values() for v in side_values.values()]
            if records and all(proved(v,'kN') for v in records):inputs['shear_envelope']=evidence(transition['shear_sides'],dict(selection='documented one-sided records; regional coverage checked by existing diagram'))
        diagrams={};diagram_pending=[]
        for label,s in (('LEFT',left_item),('RIGHT',right_item)):
            span=registered.get(str(s.get('applicable_domain',{}).get('span_id')))
            if span:
                ss=[{**deepcopy(v),'provenance':dict(series=deepcopy(v))} for v in span['internal_forces'] if v.get('quantity')=='shear' and v.get('stage')=='model_input' and v.get('envelope') in ('min','max')]
                for v in ss:v['discontinuities_m']=v.get('discontinuities_m',[])+[j['value'] for j in s['applicable_domain'].get('discontinuities_m',[])]
                try:
                    if len(ss)!=2 or {v['envelope'] for v in ss}!={'min','max'} or any(not v.get('sources') for v in ss):raise ValueError('both_documented_characteristic_shear_envelopes_required')
                    diagrams[label]=ShearDiagram(ss)
                except (ValueError,KeyError,TypeError) as error:diagram_pending.append(str(error))
        if len(diagrams)==2:
            inputs['shear_envelope']=evidence({k:d.series for k,d in diagrams.items()},dict(selection='registered local envelopes; transition and unilateral regional coverage validated by checker'))
        plan=preflight(model,region_id=identity,interval_m=interval,control='shear',inputs=inputs,height_change_suspension=True)
        if not api:_pending(plan,'resistant_API_unavailable')
        if diagram_pending:_pending(plan,*diagram_pending)
        report.update(execute(plan,review_bottom_step,left,right,transition,ctx,diagrams,settings.get('drawn_stirrup_regions',[]),public_shear_api() if api else None))
        out['bottom_step_suspension'].append(report)
    # A physical piece is credited once; overlapping extra demands need a
    # documented combination, not two independent approvals of the same steel.
    for i,e in enumerate(out['bottom_step_suspension']):
        a=e.get('result',{}).get('distribution_interval_m') if e.get('result') else None
        if not a:continue
        for other in out['bottom_step_suspension'][i+1:]:
            b=other.get('result',{}).get('distribution_interval_m') if other.get('result') else None
            if b and max(a[0],b[0])<min(a[1],b[1]):
                for entry in (e,other):
                    entry['result']['pending'].append('overlapping_suspension_regions_combination_unproved')
                    if entry['status']!='FAIL':
                        entry.update(status='INCONCLUSIVE',execution_state='EXECUTED_INCONCLUSIVE')
                        entry['result']['status']='INCONCLUSIVE'
    # Suspension at transitions remains a separate guard and existing checker.
    out['suspension']=[]
    from suspension_review import review_suspension
    for connection in settings.get('suspension_connections', []):
        x=connection.get('projected_axis_m');adjacent=[s for s in sections if s['physical_interval_m'][0]<=x<=s['physical_interval_m'][1]] if x is not None else []
        if len(adjacent)!=2 or adjacent[0].get('applicable_domain')!=adjacent[1].get('applicable_domain') or any('local_context' not in s or
                not all(proved(s['geometry'][k]) for k in ('width_cm','height_cm','cover_cm','stirrup_diameter_mm')) or not proved(s.get('effective_depth')) for s in adjacent):
            out['suspension'].append(dict(connection_id=connection['id'],status='INCONCLUSIVE',execution_state='NOT_EXECUTED',pending=['two_proved_adjacent_section_contexts_required']));continue
        contexts=[dict(interval_m=s['physical_interval_m'],context=s['local_context'],source=s['provenance']) for s in sections if s.get('applicable_domain')==adjacent[0]['applicable_domain'] and s.get('local_context')]
        ctx=deepcopy(adjacent[0]['local_context']);ctx['suspension_distribution_height']=fact(min(s['geometry']['height_cm']['value'] for s in adjacent),state='DOCUMENTED_CONFIRMED',unit='cm',
            provenance=[dict(sections=[s['segment_id'] for s in adjacent],geometry=[s['geometry']['height_cm'] for s in adjacent],procedure='responsible engineer: minimum adjacent height')])
        from suspension_review import distribution
        dist=distribution(connection,ctx)
        if not dist['interval_m']:
            out['suspension'].append(dict(connection_id=connection['id'],status='INCONCLUSIVE',execution_state='NOT_EXECUTED',pending=[dist.get('diagnostic')]));continue
        span=registered[str(adjacent[0]['applicable_domain']['span_id'])]
        ss=[{**deepcopy(s),'provenance':dict(series=deepcopy(s))} for s in span['internal_forces'] if s.get('quantity')=='shear' and s.get('stage')=='model_input' and s.get('envelope') in ('max','min')]
        for s in ss:s['discontinuities_m']=s.get('discontinuities_m', [])+[j['value'] for j in adjacent[0]['applicable_domain'].get('discontinuities_m', [])]
        physical_domain=adjacent[0]['applicable_domain']['interval_m']
        spans=[dict(span_id=span['id'],series=ss,drawn_regions=settings.get('drawn_stirrup_regions', []),section_changes_m=[x],section_contexts=contexts,
                    explicit_physical_beam_domain_m=physical_domain['value'],explicit_physical_domain_source=physical_domain)]
        inputs=deepcopy(inputs_by_control.get('suspension', {}))
        plans=[preflight(model,region_id=connection['id']+'-'+s['segment_id'],interval_m=s['physical_interval_m'],control='suspension',inputs=inputs) for s in adjacent]
        plan=plans[0];_pending(plan,*plans[1]['pending']) if plans[1]['pending'] else None
        if not api:_pending(plan,'resistant_API_unavailable')
        def check_suspension():
            result=review_suspension([connection],receiving_beam=case['beam_id'],spans=spans,context=ctx,
                api=public_shear_api() if api else None,inventory_complete=True,inventory_source=settings.get('suspension_inventory_source'))
            return {**result,'status':result['overall_result']}
        result=execute(plan,check_suspension)
        out['suspension'].append(dict(connection_id=connection['id'],**result))
    if not settings.get('suspension_inventory_source'):out['suspension_inventory_pending']=True
    return out


def moment_series(span, sign):
    candidates = [s for s in span['internal_forces'] if s.get('quantity')=='bending_moment' and
        s.get('envelope')==('max' if sign=='POSITIVE' else 'min') and s.get('unit')=='kN.m' and
        s.get('stage')=='model_input' and s.get('sources')]
    if len(candidates)!=1 or any(v is None for v in candidates[0]['values']):
        raise ValueError('unique_existing_characteristic_moment_envelope_required')
    return candidates[0]


def longitudinal_inventory(model):
    """Expose physical intervals/events to existing checkers without new code rules."""
    return [dict(occurrence_id=b['occurrence_id'], documentary_mark=b['mark'],
        x_start_m=deepcopy(b['x_start_m']), x_end_m=deepcopy(b['x_end_m']),
        continuity=deepcopy(b.get('continuity')), extensions=deepcopy(b.get('extensions', [])),
        laps=deepcopy(b.get('laps', [])), termination=deepcopy(b.get('termination', {})),
        longitudinal_position_proved=all(b[k]['state']=='DOCUMENTED_CONFIRMED' for k in ('x_start_m','x_end_m')),
        normative_verdict=None) for b in model['physical_geometry']['occurrences']]


def document_receipt(source):
    """Raw document with zones, or preserved extraction with hash/provenance.

    An unavailable raw file can be replayed, but is never described as examined now.
    """
    if not source:
        return dict(available=False, reason='SOURCE_NOT_PROVIDED', observations=[], coverage=[])
    if source.get('path') and Path(source['path']).is_file():
        path = Path(source['path'])
        sha = hashlib.sha256(path.read_bytes()).hexdigest()
        if source.get('sha256') and source['sha256'] != sha:
            raise ValueError('document_hash_mismatch')
        extracted = extract_zones(path, source['zones']) if source.get('zones') else dict(observations=[], coverage=[])
        return dict(available=True, mode='PRESERVED_INPUT_FILE' if path.suffix.lower()=='.json' else 'RAW_SOURCE', path=str(path), sha256=sha, **extracted)
    archive = source.get('extraction_archive')
    if archive and Path(archive).is_file() and source.get('archive_sha256'):
        content = Path(archive).read_bytes()
        if hashlib.sha256(content).hexdigest() != source['archive_sha256']:
            raise ValueError('extraction_archive_hash_mismatch')
        data = json.loads(content.decode('utf-8-sig'))
        if not data.get('provenance') or not data.get('source_sha256'):
            raise ValueError('archived_extraction_source_identity_required')
        return dict(available=True, mode='PRESERVED_EXTRACTION_RAW_UNAVAILABLE', archive=str(archive),
                    archive_sha256=source['archive_sha256'], **data)
    return dict(available=False, reason='SOURCE_UNAVAILABLE_IN_SESSION', reference=deepcopy(source), observations=[], coverage=[])


def _pending(plan, *reasons):
    plan['pending'] = sorted(set(plan['pending']) | set(reasons))
    plan['readiness'] = 'PENDING'


def review_beam(case, *, floor, receipts, adapters=None, api=None):
    adapters = dict(adapters or {})
    if api is not None:
        adapters.setdefault('positive_flexure', flexure_adapter)
        adapters.setdefault('negative_flexure', flexure_adapter)
    name = case['beam_id']
    model = transform(case['document'], name + '-floor-document.json') if 'document' in case else deepcopy(case['model'])
    if not model.get('physical_geometry'):
        raise ValueError('stage1_physical_extension_required')
    ext = case.get('document', {}).get('physical_extension', {})
    observations = ext.get('observations', case.get('observations', []))
    coverage = ext.get('coverage', case.get('coverage', []))
    extraction = case.get('detailing_extraction', {})
    # Beam-specific extraction avoids mixing identical marks from different beams.
    if extraction:
        extraction = document_receipt(extraction)
        observations = observations + extraction.get('observations', [])
        coverage = coverage + extraction.get('coverage', [])
    if observations or coverage:
        model['documentary_reconciliation'] = reconcile(observations, coverage,
            expected_marks=sorted({b['mark'] for b in model['physical_geometry']['occurrences']}))
    form_available = receipts['form']['available'] and bool(case.get('form'))
    if form_available:
        model = apply_form(model, case['form'])
    else:
        model['form_interpretation'] = dict(pending=[dict(documentary_state='NOT_EXAMINED',
            reason='Form source or beam-specific form interpretation unavailable; not proof of absence on drawing')])
    model = interpret_layers(model, case.get('layer_observations', {}))
    plotting = [dict(mark=p['mark'], evidence=i) for p in model.get('documentary_reconciliation', {}).get('positions', [])
                for i in p.get('issues', []) if i['code']=='PLOTTING_INTEGRITY' and i.get('view')=='ELEVATION']
    registered, registration_pending = {}, []
    for span in case.get('positioned_tqs', {}).get('beam', {}).get('spans', []):
        registration = case.get('registrations', {}).get(str(span['id']))
        if not registration:
            registration_pending.append(dict(span_id=span['id'], reason='Provar associação do eixo local TQS ao eixo comum na forma.'))
            continue
        try:
            registered[str(span['id'])] = register_span(span, registration, model['physical_geometry']['coordinate_system'])
        except ValueError as error:
            registration_pending.append(dict(span_id=span['id'], reason=str(error)))
    jobs = deepcopy(case.get('jobs', []))
    if registered:
        for control, sign in (('positive_flexure','POSITIVE'), ('negative_flexure','NEGATIVE')):
            if any(j['control']==control for j in jobs):
                continue
            for span_id, span in registered.items():
                for region in prepare_local_batches(model, flexure_sign=sign)['regions']:
                    a,z = region['x_start_m'],region['x_end_m']
                    positions = span['internal_forces'][0]['positions']
                    a,z = max(a,min(positions)),min(z,max(positions))
                    if a >= z:
                        continue
                    jobs.append(dict(id=f'{name}-{control}-{span_id}-{region["region_id"]}', control=control,
                        span_id=span_id, interval_m=[a,z], context=case.get('context', {}),
                        inputs=deepcopy(case.get('control_inputs', {}).get(control, {}))))
    if len({j['id'] for j in jobs}) != len(jobs) or any(j['control'] not in CONTROLS for j in jobs):
        raise ValueError('unique_job_identity_and_known_control_required')
    # Missing controls are recorded; empty job lists cannot yield floor approval.
    present = {j['control'] for j in jobs}
    for control in CONTROLS:
        if control not in present:
            jobs.append(dict(id=name+'-'+control+'-unplanned', control=control, interval_m=case['review_interval_m'], inputs={}))
    executions, plans = [], []
    for job in jobs:
        control = job['control']
        inputs = deepcopy(job.get('inputs', {}))
        span = registered.get(str(job.get('span_id')))
        if control in ('positive_flexure', 'negative_flexure', 'scaling', 'shear'):
            inputs['force_position_mapping'] = fact(True, state='DOCUMENTED_CONFIRMED', provenance=[dict(span_id=span['id'], registration=span['internal_forces'][0]['mapping_provenance'])]) if span else fact()
        if control in ('positive_flexure','negative_flexure') and span:
            try:
                series = moment_series(span, 'POSITIVE' if control=='positive_flexure' else 'NEGATIVE')
                inputs['moment_envelope'] = fact(series, state='DOCUMENTED_CONFIRMED', provenance=[series])
            except ValueError as error:
                inputs['moment_envelope'] = fact(provenance=[dict(reason=str(error))])
        fit = None
        if control in ('positive_flexure', 'negative_flexure', 'scaling') or job.get('uses_layers_for_resistance'):
            fit = dict(fits=None, diagnostics=['documentary_plotting_failure_beam_review_suspended']) if plotting else local_layer_fit(model, job['interval_m'], control, api) if api is not None else dict(fits=None, diagnostics=['fit_API_unavailable'])
            inputs['layer_fit'] = fact(fit['fits'], state='DOCUMENTED_CONFIRMED', provenance=[fit]) if fit['fits'] is not None else fact(provenance=[fit])
        plan = preflight(model, region_id=job['id'], interval_m=job['interval_m'], control=control, inputs=inputs,
                         applicability=job.get('applicability'), uses_layers_for_resistance=job.get('uses_layers_for_resistance', False))
        unavailable = [role+'_source_unavailable' for role in ('form','detailing','tqs') if not receipts[role]['available']]
        if not form_available:
            unavailable.append('beam_form_interpretation_unavailable')
        if unavailable:
            _pending(plan, *unavailable)
        adapter = adapters.get(job.get('adapter', control))
        if adapter is None and plan['readiness'] != 'NOT_APPLICABLE':
            _pending(plan, 'existing_checker_adapter_unavailable')
        if adapter is flexure_adapter and not job.get('context'):
            _pending(plan, 'resistant_context_unavailable')
        payload = dict(model=model, job=job, inputs=inputs, registered_span=span,
                       bars=project_occurrences(model), layer_fit=fit, api=api)
        result = execute(plan, adapter, payload)
        executions.append(dict(job_id=job['id'], control=control, layer_fit=fit, **result))
        plans.append(plan)
    ctx = dict(beam_id=name, floor=floor, coordinate_system=model['physical_geometry']['coordinate_system'])
    modules = []
    for execution, plan in zip(executions, plans):
        # Scaling diagnostics belong to flexure; identity remains control-specific.
        discipline = execution['control'] if execution['control'] != 'scaling' else 'negative_flexure' if next(j for j in jobs if j['id']==execution['job_id']).get('flexure_sign')=='NEGATIVE' else 'positive_flexure'
        modules.append(dict(**ctx, discipline=discipline, source='floor_review/'+execution['job_id'], version='etapa1.1',
            complete=execution['execution_state']=='EXECUTED_COMPLETE',
            checks=[dict(check_id=execution['job_id'], check_type=execution['control'], status=execution['status'],
                physical_interval=plan['interval_m'], reason='; '.join(plan['pending']) or 'existing_checker_result',
                missing_information=plan['pending'], evidence=dict(input_validation=plan, execution=execution))]))
        fit = execution.get('layer_fit')
        if form_available and fit and fit['fits'] is not None:
            modules.append(dict(**ctx, discipline=discipline, source='floor_review/'+execution['job_id']+'/fit', version='etapa1.1',
                complete=True, checks=[dict(check_id=execution['job_id']+'/fit', check_type='transverse_fit',
                    status='PASS' if fit['fits'] else 'FAIL', physical_interval=plan['interval_m'], evidence=fit,
                    reason='Existing transverse_fit; no alternative layer distribution invented')]))
    boundary_pending = []
    for control, sign in (('positive_flexure','POSITIVE'), ('negative_flexure','NEGATIVE')):
        for region in prepare_local_batches(model, flexure_sign=sign)['regions']:
            a,z = region['x_start_m'],region['x_end_m']
            if a != z:
                continue
            note = dict(control=control, region_id=region['region_id'], interval_m=[a,z],
                        reason='transition_resistant_method_not_implemented', implementation='NOT_IMPLEMENTED', execution_state='NOT_EXECUTED')
            boundary_pending.append(note)
            modules.append(dict(**ctx, discipline=control, source='floor_review/boundary/'+control+'/'+region['region_id'],
                version='etapa1.1', complete=False, checks=[dict(check_id=region['region_id'], check_type='geometric_position',
                    status='INCONCLUSIVE', physical_interval=[a,z], reason=note['reason'], evidence=note)]))
    regional_scope = [dict(segment_id=s['id'], interval_m=[s['x_start_m']['value'],s['x_end_m']['value']],
                           implementation='EXISTING_CONSTANT_SECTION_METHOD' if s['geometry_type']=='CONSTANT' else 'NOT_IMPLEMENTED' if s['geometry_type'] in ('VARIABLE','TRANSITION') else 'UNRESOLVED_GEOMETRY',
                           structural_verdict=None) for s in model['physical_geometry']['segments']]
    regional_scope += [dict(interval_m=t['physical_interval_m'], implementation='NOT_IMPLEMENTED',
                            position_state=t.get('position_state'), clarification=t.get('clarification'), structural_verdict=None)
                      for t in model.get('form_interpretation', {}).get('transitions', []) if t.get('physical_interval_m')]
    section_checks = None
    profiles={tuple(s['geometry'][k]['value'] for k in ('width_cm','height_cm','top_level_cm','bottom_level_cm','lateral_offset_cm'))
              for s in model['physical_geometry']['segments'] if s['geometry_type']=='CONSTANT'}
    if case.get('section_checks') or len(profiles)>1:
        if plotting or not form_available or not all(receipts[r]['available'] for r in ('form','detailing','tqs')):
            section_checks=dict(status='INCONCLUSIVE',execution_state='NOT_EXECUTED',pending=['documentary_sources_or_integrity_required'])
        else:
            section_checks=review_constant_sections(model,registered,case,api)
    section_executions=[]
    if section_checks and section_checks.get('sections'):
        for section in section_checks['sections']:
            checks=[('shear',section['al'])] if 'al' in section else []
            checks += [(e['control'],e) for e in section.get('expanded_flexure', [])]
            checks += [('shear',e) for e in section.get('shear_checks', [])]
            for index,(discipline,e) in enumerate(checks):
                identifier=section['segment_id']+'-'+discipline+'-'+str(index)
                section_executions.append(e);plans.append(e['input_validation'])
                modules.append(dict(**ctx,discipline=discipline,source='floor_review/sections/'+identifier,version='engineer_section_procedure',
                    complete=e['execution_state']=='EXECUTED_COMPLETE',checks=[dict(check_id=identifier,check_type='section_procedure',
                    status=e['status'],physical_interval=e.get('physical_interval_m',section['physical_interval_m']),
                    reason='; '.join(e['input_validation']['pending']) or 'existing_checker_result',evidence=e)]))
            if section.get('diagnostics'):
                modules.append(dict(**ctx,discipline='positive_flexure',source='floor_review/sections/'+section['segment_id']+'/pending',version='engineer_section_procedure',
                    complete=False,checks=[dict(check_id=section['segment_id']+'-pending',check_type='section_procedure',status='INCONCLUSIVE',
                    physical_interval=section['physical_interval_m'],reason='; '.join(section['diagnostics']),evidence=section['diagnostics'])]))
        for index,e in enumerate(section_checks.get('suspension', [])+section_checks.get('bottom_step_suspension', [])):
            if e['status']=='NOT_APPLICABLE':continue
            section_executions.append(e)
            if e.get('input_validation'):plans.append(e['input_validation'])
            identifier='section-suspension-'+str(index)
            modules.append(dict(**ctx,discipline='suspension',source='floor_review/sections/'+identifier,version='engineer_section_procedure',
                complete=e['execution_state']=='EXECUTED_COMPLETE',checks=[dict(check_id=identifier,check_type='section_suspension',status=e['status'],
                reason='existing_suspension_method_with_local_sections',evidence=e)]))
    diagnosis = consolidate(ctx, modules, input_validation=plans)
    all_executions=executions+section_executions
    diagnosis['execution_state'] = 'NOT_EXECUTED' if all(e['execution_state']=='NOT_EXECUTED' for e in all_executions) else 'PARTIALLY_EXECUTED' if any(e['execution_state']=='NOT_EXECUTED' for e in all_executions) else 'EXECUTED_INCONCLUSIVE' if any(e['status']=='INCONCLUSIVE' for e in all_executions) else 'EXECUTED_COMPLETE'
    return dict(beam_id=name, model=model, stages=list(STAGES), registered_spans=registered,
                section_checks=section_checks,
                regional_method_scope=regional_scope,
                documentary_review=dict(suspended=bool(plotting), affected_marks=sorted({p['mark'] for p in plotting}),
                    required_action='Correct/reissue longitudinal detailing before complete structural review.' if plotting else None, evidence=plotting),
                registration_pending=registration_pending, boundary_pending=boundary_pending, controls=executions, diagnosis=diagnosis,
                longitudinal_inventory=longitudinal_inventory(model),
                positive_batches=prepare_local_batches(model), negative_batches=prepare_local_batches(model, flexure_sign='NEGATIVE'))


def review_floor(spec, *, adapters=None, api=None):
    if not spec.get('floor') or not spec.get('beams'):
        raise ValueError('floor_identity_and_beam_inventory_required')
    names = [b['beam_id'] for b in spec['beams']]
    if len(set(names)) != len(names):
        raise ValueError('duplicate_floor_beam')
    receipts = {role: document_receipt(spec.get('sources', {}).get(role)) for role in ('form', 'detailing', 'tqs')}
    beams = [review_beam(case, floor=spec['floor'], receipts=receipts, adapters=adapters, api=api) for case in spec['beams']]
    return dict(schema_version='1.1', floor=spec['floor'], stages=list(STAGES), documents=receipts, beams=beams,
                overall_status=aggregate(b['diagnosis']['overall_status'] for b in beams),
                beam_inventory_complete=spec.get('beam_inventory_complete', False),
                floor_approval=None, correction_generation_enabled=False, pdf_modification_enabled=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--preflight-only', action='store_true', help='Do not load the resistant API; retain pending execution explicitly.')
    args = parser.parse_args()
    if args.output.resolve() == args.manifest.resolve() or args.output.suffix.lower() != '.json':
        raise ValueError('distinct_JSON_output_required')
    api = None
    if not args.preflight_only:
        sys.path.insert(0, str(ROOT.parent/'concretopy'))
        import concretopy as api
    result = review_floor(json.loads(args.manifest.read_text(encoding='utf-8-sig')), api=api)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False)+'\n', encoding='utf-8')


if __name__ == '__main__':
    main()
