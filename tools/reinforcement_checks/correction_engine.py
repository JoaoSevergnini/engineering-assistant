"""Diagnostic-driven correction proposals. No PDF IO or resistant equations."""
from copy import deepcopy
import hashlib,json,math
from detailing_change_contracts import detailing_preferences

SECONDARY_TYPES=('ALTER_DIAMETER','ALTER_QUANTITY','REDISTRIBUTE_BARS','EXTEND_OTHER_BARS','ADD_POSITION')
STATES=('PASS','FAIL','INCONCLUSIVE','NOT_APPLICABLE','REQUIRES_ENGINEERING_REVIEW')

def status(values):
    values=list(values)
    for state in ('FAIL','INCONCLUSIVE','REQUIRES_ENGINEERING_REVIEW'):
        if state in values:return state
    return 'PASS' if values and all(v in ('PASS','NOT_APPLICABLE') for v in values) else 'INCONCLUSIVE'

def control(name,state,source=None,**values):
    if state not in STATES:raise ValueError('invalid_control_state')
    if state in ('PASS','NOT_APPLICABLE') and not source:state='INCONCLUSIVE'
    return dict(check_id=name,status=state,source=deepcopy(source),**values)

def bend_geometry(data):
    """Elementary envelope only. Pin/leg limits and position proof are sourced inputs.

    Orthogonal quarter-circle bend; never infers a resistant equivalent length.
    Node interferences remain a separate sourced control.
    """
    d=deepcopy(data or {});checks=[];pending=[]
    if d.get('bend_shape')!='ORTHOGONAL_90_DEG':pending.append('explicit_supported_bend_shape')
    required=('support_geometry','endpoint_position','cover','bar_diameter','available_space','bend_pin_criterion','straight_leg_criteria')
    for key in required:
        if not d.get('sources',{}).get(key):pending.append(key)
    keys=('diameter_mm','cover_cm','available_horizontal_cm','available_vertical_cm','inner_bend_diameter_mm','minimum_inner_diameter_mm','horizontal_leg_cm','vertical_leg_cm','minimum_horizontal_leg_cm','minimum_vertical_leg_cm')
    for key in keys:
        v=d.get(key)
        if type(v) not in (int,float) or not math.isfinite(v) or v<0 or (key.endswith('diameter_mm') and v==0):pending.append(key)
    if pending:
        checks.append(control('bend_dimensions','INCONCLUSIVE',missing_information=sorted(set(pending))))
    else:
        phi=d['diameter_mm']/10
        outer_radius=d['inner_bend_diameter_mm']/20+phi
        horizontal=d['horizontal_leg_cm']+outer_radius+2*d['cover_cm']
        vertical=d['vertical_leg_cm']+outer_radius+2*d['cover_cm']
        checks.append(control('bend_envelope','PASS' if horizontal<=d['available_horizontal_cm'] and vertical<=d['available_vertical_cm'] else 'FAIL',d['sources'],horizontal_extent_cm=horizontal,vertical_extent_cm=vertical))
        checks.append(control('bend_pin','PASS' if d['inner_bend_diameter_mm']>=d['minimum_inner_diameter_mm'] else 'FAIL',d['sources']['bend_pin_criterion']))
        checks.append(control('straight_legs','PASS' if d['horizontal_leg_cm']>=d['minimum_horizontal_leg_cm'] and d['vertical_leg_cm']>=d['minimum_vertical_leg_cm'] else 'FAIL',d['sources']['straight_leg_criteria']))
        d['centerline_arc_length_cm']=math.pi/2*(d['inner_bend_diameter_mm']/20+phi/2)
        d['developed_length_cm']=d['horizontal_leg_cm']+d['vertical_leg_cm']+d['centerline_arc_length_cm']
    for name in ('position_within_support','node_interferences'):
        c=d.get(name,{})
        checks.append(control(name,c.get('status','INCONCLUSIVE'),c.get('source')))
        if checks[-1]['status']=='INCONCLUSIVE':pending.append(name)
    return {'status':status(c['status'] for c in checks),'checks':checks,'pending_information':sorted(set(pending)),'geometry':d,'developed_length_is_resistant_anchorage':False}

def propose_corrections(diagnostic, *, occurrence_id, bar, extremity, original_geometry,
                        bend_data=None, secondary_candidates=(), reverify=None, preferences=None, support_geometry=None, primary_candidate=None, scope_decision=None, input_validation=None):
    """Callbacks must fully rebuild and recheck candidate-dependent geometry/structure.

    No callback means inconclusive, never approval. Original data are deep-copied.
    Stable IDs are hashes of identity, occurrence, operation and proposed geometry.
    """
    if input_validation is not None:
        from input_preflight import correction_readiness
        if not correction_readiness(input_validation)['eligible']:
            raise ValueError('correction_inputs_pending')
    origin=next((o for o in diagnostic['occurrences'] if o['occurrence_id']==occurrence_id),None)
    if origin is None or origin['status']!='FAIL' or origin['check_type']!='anchorage_length':raise ValueError('proven_anchorage_occurrence_required')
    if bar not in origin['drawing_reinforcement_ids'] or extremity not in ('LEFT','RIGHT'):raise ValueError('correction_bar_or_end_mismatch')
    if not support_geometry or support_geometry.get('support_type')!='END' or support_geometry.get('support_side')!=extremity or not support_geometry.get('provenance'):
        raise ValueError('oriented_end_support_geometry_required')
    context=diagnostic['context'];specs=[dict(type='END_BEND',proposed_geometry=deepcopy(bend_data or {}),degree_of_intervention='LOCAL_EXISTING_BAR',changed_dimensions=['end_bend_geometry'],affected_checks=['curved_anchorage_resistance'])]
    if primary_candidate is not None:specs=[deepcopy(primary_candidate)]
    for c in secondary_candidates:
        if c.get('type') not in SECONDARY_TYPES:raise ValueError('unsupported_secondary_intervention')
        specs.append(deepcopy(c))
    output=[]
    for spec in specs:
        identity=[context['beam_id'],context['floor'],occurrence_id,bar,extremity,spec]
        aid='alt-'+hashlib.sha256(json.dumps(identity,sort_keys=True,allow_nan=False).encode()).hexdigest()[:20]
        if any(a['id']==aid for a in output):raise ValueError('duplicate_alternative')
        bend=spec['type']=='END_BEND'
        geometry=bend_geometry(spec['proposed_geometry']) if bend else {'status':'INCONCLUSIVE','checks':[],'pending_information':['candidate_geometry_reverification']}
        affected=spec.get('affected_checks',[])
        if not affected:raise ValueError('affected_checks_required')
        try:raw=deepcopy(reverify(deepcopy(spec))) if reverify else {}
        except (ValueError,TypeError,KeyError) as error:raw={'diagnostics':['reverification_unresolved:'+str(error)]}
        results=raw.get('checks',[]);normalized=[]
        for c in results:
            if c.get('check_id') not in affected:raise ValueError('unexpected_reverification_control')
            normalized.append(control(c['check_id'],c['status'],c.get('source'),result=deepcopy(c)))
        if len({c['check_id'] for c in normalized})!=len(normalized):raise ValueError('duplicate_reverification_control')
        missing=set(affected)-{c['check_id'] for c in normalized}
        normalized.extend(control(name,'INCONCLUSIVE',missing_information=['affected_control_not_reverified']) for name in sorted(missing))
        if not bend:
            gc=raw.get('geometry_checks',[])
            gc=[control(c['check_id'],c['status'],c.get('source')) for c in gc]
            geometry={'checks':gc,'status':status(c['status'] for c in gc),'pending_information':[c['check_id'] for c in gc if c['status']=='INCONCLUSIVE'] if gc else ['candidate_geometry_reverification']}
        structural=status(c['status'] for c in normalized)
        pending=geometry['pending_information']+sorted(missing)+raw.get('pending_information',[])
        pending += [c['check_id'] for c in normalized if c['status']=='INCONCLUSIVE']
        if pending and structural=='PASS':structural='INCONCLUSIVE'
        output.append({'id':aid,'origin_occurrence':deepcopy(origin),'beam_id':context['beam_id'],'floor':context['floor'],'reinforcement_mark':bar,'affected_extremity':extremity,'intervention_type':spec['type'],
            'original_geometry':deepcopy(original_geometry),'proposed_geometry':deepcopy(spec['proposed_geometry']),
            'changed_dimensions':deepcopy(spec.get('changed_dimensions',[])),'affected_checks':list(affected),
            'reverification_results':normalized,'reverification_audit':raw,'geometry_verification':geometry,
            'geometric_feasibility':geometry['status'],'structural_feasibility':structural,'status':status([geometry['status'],structural]),
            'pending_information':sorted(set(pending)),'units':{'geometry_lengths':'cm','diameters':'mm','axis_coordinates':'m'},'support_geometry':deepcopy(support_geometry),'degree_of_intervention':spec.get('degree_of_intervention','UNRESOLVED'),
            'comparison_facts':deepcopy(spec.get('comparison_facts',{})),
            'engineer_approval':'PENDING_ENGINEERING_APPROVAL','ready_for_detailing':False,'graphical_reference':None})
    if scope_decision:
        output=[apply_scope_decision(a,scope_decision) for a in output]
    return {'model_type':'REINFORCEMENT_CORRECTION_STUDY','alternatives':output,
        'preferences':deepcopy(preferences or detailing_preferences([10,12.5,16,20,25])),
        'schema_version':'1.0','comparison_priorities':['proven_structural_and_geometric_validity','reuse_existing_bars','constructive_simplicity','fewer_changed_positions','less_detailing_rework','rational_steel_consumption'],
        'selected_solution':None,'detailing_optimization':None,'pdf_modified':False}


SCOPE_RULE='engineer_confirmed_support_correction_scope_exclusions_v1'
EXCLUDED_NODE_CONTROLS=('bend_pin','curved_bar_trajectory','node_interferences')

def apply_scope_decision(alternative, decision):
    """Explicit office scope, not proof of an omitted check. Preserve original audit."""
    if not decision.get('source') or decision.get('rule')!=SCOPE_RULE:
        raise ValueError('scope_decision_provenance_required')
    a=deepcopy(alternative)
    a['scope_audit_before_exclusions']=deepcopy({'geometry_verification':a['geometry_verification'],'reverification_results':a['reverification_results'],'status':a['status']})
    excluded=set(decision.get('excluded_controls',[]))
    if excluded-set(EXCLUDED_NODE_CONTROLS):raise ValueError('unsupported_scope_exclusion')
    omitted=[{'check_id':name,'execution_state':'NOT_EXECUTED','technical_status':None,'reason':'NOT_EXECUTED_BY_SCOPE_DECISION','source':deepcopy(decision)} for name in sorted(excluded)]
    checks=[c for c in a['reverification_results'] if c['check_id'] not in excluded]
    gc=[c for c in a['geometry_verification']['checks'] if c['check_id'] not in excluded]
    a['reverification_results']=checks
    a['geometry_verification']['checks']=gc
    a['geometric_feasibility']=status(c['status'] for c in gc)
    a['geometry_verification']['status']=a['geometric_feasibility']
    a['geometry_verification']['pending_information']=[p for p in a['geometry_verification']['pending_information'] if p not in excluded]
    a['structural_feasibility']=status(c['status'] for c in checks)
    a['status']=status([a['geometric_feasibility'],a['structural_feasibility']])
    a['pending_information']=[p for p in a['pending_information'] if p not in excluded]
    executed=checks+gc
    a['verification_register']={
        'executed_passed':[deepcopy(c) for c in executed if c['status']=='PASS'],
        'executed_failed':[deepcopy(c) for c in executed if c['status']=='FAIL'],
        'not_executed_by_scope':omitted,
        'inconclusive_missing_data':[deepcopy(c) for c in executed if c['status']=='INCONCLUSIVE'],
        'engineering_review':[deepcopy(c) for c in executed if c['status']=='REQUIRES_ENGINEERING_REVIEW']}
    a['scope_decision']=deepcopy(decision)
    a['construction_conditions_fully_proven']=False
    return a
