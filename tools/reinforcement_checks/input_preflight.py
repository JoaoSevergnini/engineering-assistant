"""Local pre-calculation readiness, preserving technical/execution states.

Callbacks reuse existing checkers. This module does not calculate resistance.
"""
from copy import deepcopy
import sys
from pathlib import Path

MODEL_TOOLS = Path(__file__).resolve().parents[1] / 'beam_model'
if str(MODEL_TOOLS) not in sys.path:
    sys.path.insert(0, str(MODEL_TOOLS))
from input_evidence import validate_fact, PROVED
from physical_geometry import project_occurrences, project_segments

CONTROLS = ('positive_flexure', 'negative_flexure', 'anchorage', 'shear', 'scaling', 'suspension')
GEOMETRY_DEPENDENCIES = {
    'positive_flexure': ('width_cm','height_cm','cover_cm','stirrup_diameter_mm'),
    'negative_flexure': ('width_cm','height_cm','cover_cm','stirrup_diameter_mm'),
    'anchorage': (),
    'shear': ('width_cm','height_cm','cover_cm','stirrup_diameter_mm'),
    'scaling': ('width_cm','height_cm','cover_cm','stirrup_diameter_mm'),
    'suspension': (),
}
EXTERNAL_DEPENDENCIES = {
    'positive_flexure': ('materials','moment_envelope','force_position_mapping','layer_order'),
    'negative_flexure': ('materials','moment_envelope','force_position_mapping','layer_order'),
    'anchorage': ('materials','anchorage_demand','support_faces','bar_termination','anchorage_scope'),
    'shear': ('materials','shear_envelope','force_position_mapping','stirrup_regions','effective_depth'),
    'scaling': ('materials','moment_envelope','shear_envelope','force_position_mapping','bar_cut','scaling_scope','layer_order'),
    'suspension': ('materials','supported_reaction','indirect_support','suspension_bars'),
}


def overlaps(a, b, c, d):
    return (a is None or a < d) and (b is None or b > c)


def preflight(model, *, region_id, interval_m, control, inputs=None, allow_assumptions=False, applicability=None):
    if control not in CONTROLS:
        raise ValueError('unknown_preflight_control')
    a, z = interval_m
    if a >= z:
        raise ValueError('positive_control_interval_required')
    inputs = inputs or {}
    accepted = PROVED + (('ENGINEERING_ASSUMPTION',) if allow_assumptions else ())
    required, pending, assumptions = {}, [], []
    def need(name, item):
        item = validate_fact(item)
        required[name] = deepcopy(item)
        if item['state'] not in accepted or item['value'] is None:
            pending.append(name)
        elif name in ('physical_inventory_complete','anchorage_scope','scaling_scope') and item['value'] is not True:
            pending.append(name)
        elif item['state'] == 'ENGINEERING_ASSUMPTION':
            assumptions.append(name)
    if applicability is not None:
        item = validate_fact(applicability)
        if item['state'] == 'NOT_APPLICABLE' and item['provenance']:
            return dict(region_id=region_id, interval_m=list(interval_m), control=control, readiness='NOT_APPLICABLE', pending=[], assumptions=[], evidence=dict(applicability=item))
    segments = model.get('physical_geometry', {}).get('segments', [])
    relevant = [s for s in segments if overlaps(s['x_start_m']['value'] if s['x_start_m']['state'] in PROVED else None,
                                               s['x_end_m']['value'] if s['x_end_m']['state'] in PROVED else None, a,z)]
    if GEOMETRY_DEPENDENCIES[control]:
        # Exactly one proved constant segment must contain this entire batch.
        contained = [s for s in relevant if s['x_start_m']['state'] in PROVED and s['x_end_m']['state'] in PROVED and s['x_start_m']['value'] <= a and s['x_end_m']['value'] >= z and s['geometry_type'] == 'CONSTANT']
        if len(relevant) != 1 or len(contained) != 1:
            pending.append('unique_constant_physical_segment')
        else:
            need('geometry.section_shape',contained[0]['geometry']['section_shape'])
            if contained[0]['geometry']['section_shape']['value'] not in ('RECTANGULAR','rectangular'):
                pending.append('unsupported_section_shape')
            for k in GEOMETRY_DEPENDENCIES[control]:
                need('geometry.' + k, contained[0]['geometry'][k])
    for k in EXTERNAL_DEPENDENCIES[control]:
        from input_evidence import fact
        need(k, inputs.get(k, fact()))
    bars = model.get('physical_geometry', {}).get('occurrences', [])
    if control in ('positive_flexure','negative_flexure','scaling'):
        function = 'positive' if control == 'positive_flexure' else 'negative' if control == 'negative_flexure' else None
        local = [b for b in bars if b.get('function') in (function, None) or function is None]
        local = [b for b in local if overlaps(b['x_start_m']['value'] if b['x_start_m']['state'] in PROVED else None,
                                              b['x_end_m']['value'] if b['x_end_m']['state'] in PROVED else None,a,z)]
        if not local:
            pending.append('physical_occurrence_inventory')
        for b in local:
            for k in ('quantity','diameter_mm','layers','x_start_m','x_end_m'):
                need('bar.'+b['occurrence_id']+'.'+k,b[k])
            if b.get('function') is None or b.get('face') not in ('lower','upper'):
                pending.append('bar.'+b['occurrence_id']+'.function_or_face')
            position = next((p for p in model.get('documentary_reconciliation',{}).get('positions',[]) if p['mark'] == b['mark']),None)
            if position:
                dependent_fields = {'quantity','diameter_mm'}
                if control == 'scaling':
                    dependent_fields.update(('shape','nominal_length_cm'))
                conflicts = [issue for issue in position['issues']
                    if issue['code'] in ('PHYSICAL_TOTAL_DIVERGENCE','STALE_DOCUMENT_PROVED')
                    or issue['code']=='DOCUMENTARY_DIVERGENCE' and issue.get('field') in dependent_fields]
                if conflicts:
                    pending.append('documentary_conflict.'+b['mark'])
        # Complete inventory is a separate proof: known bars cannot prove no others.
        from input_evidence import fact
        need('physical_inventory_complete',inputs.get('physical_inventory_complete',fact()))
    return dict(region_id=region_id, interval_m=list(interval_m), control=control,
                readiness='PENDING' if pending else 'RUNNABLE_WITH_ASSUMPTIONS' if assumptions else 'RUNNABLE',
                pending=sorted(set(pending)), assumptions=assumptions, evidence=required,
                scope=dict(force_policy='TQS_ENVELOPES', concomitant_combinations_required=False,
                           mandatory_curved_path=False, mandatory_pin_check=False, mandatory_column_reinforcement_interference=False))


def execute(plan, checker, *args, **kwargs):
    """Checker is never called with pending input. No fabricated PASS or FAIL."""
    if plan['readiness'] in ('PENDING','NOT_APPLICABLE'):
        return dict(status='INCONCLUSIVE' if plan['readiness']=='PENDING' else 'NOT_APPLICABLE',
                    execution_state='NOT_EXECUTED' if plan['readiness']=='PENDING' else 'EXECUTED_COMPLETE', input_validation=deepcopy(plan), result=None)
    result = checker(*args, **kwargs)
    state = result.get('status', result.get('overall_structural_result'))
    if state is None and 'passes' in result:
        state = 'PASS' if result['passes'] is True else 'FAIL' if result['passes'] is False else 'INCONCLUSIVE'
    state = state or 'INCONCLUSIVE'
    return dict(status=state,
                execution_state='EXECUTED_INCONCLUSIVE' if state=='INCONCLUSIVE' else 'EXECUTED_COMPLETE',
                conditional=bool(plan['assumptions']), input_validation=deepcopy(plan), result=result)


def prepare_local_batches(model, *, flexure_sign='POSITIVE'):
    """Feed existing flexure_regions. Abrupt geometry transition stays explicit."""
    from flexure_regions import decompose_regions
    function = 'positive' if flexure_sign == 'POSITIVE' else 'negative'
    bars = [b for b in project_occurrences(model) if b.get('function') in (function, None)]
    segments, pending = project_segments(model)
    if not segments:
        return dict(regions=[], pending_geometry=pending, bars=bars)
    domain = (min(s['x_start_common'] for s in segments),max(s['x_end_common'] for s in segments))
    return dict(regions=decompose_regions(bars,domain,segments,flexure_sign=flexure_sign), pending_geometry=pending, bars=bars,
                correction_generation_enabled=False)


def correction_readiness(plans):
    """Input guard only; this stage never generates changes to reinforcement."""
    return dict(eligible=all(p['readiness']=='RUNNABLE' for p in plans) and bool(plans),
                pending=[dict(region_id=p['region_id'],control=p['control'],missing=p['pending']) for p in plans if p['readiness']!='RUNNABLE'],
                correction_generation_enabled=False)


def execute_control(model, *, region_id, interval_m, control, inputs, checker, args=(), kwargs=None):
    """Same guarded entry for simplified anchorage, shear, scaling and suspension."""
    plan = preflight(model, region_id=region_id, interval_m=interval_m, control=control, inputs=inputs)
    return execute(plan, checker, *args, **(kwargs or {}))
