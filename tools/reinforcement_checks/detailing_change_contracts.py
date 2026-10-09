"""Preferences and serializable change contracts. No generator, optimizer or PDF IO."""
from copy import deepcopy
OPERATIONS=('ALTER_QUANTITY','ALTER_DIAMETER','ALTER_LENGTH','REDISTRIBUTE_BARS','ADD_POSITION','MIX_DIAMETERS')
APPROVAL_STATES=('DRAFT','PENDING_ENGINEERING_APPROVAL','APPROVED','REJECTED')


def detailing_preferences(diameter_series, *, max_diameter_steps=2):
    if not diameter_series or len(set(diameter_series))!=len(diameter_series) or any(type(v) not in (int,float) or v<=0 for v in diameter_series):
        raise ValueError('invalid_commercial_diameter_series')
    if list(diameter_series)!=sorted(diameter_series) or type(max_diameter_steps)!=int or max_diameter_steps<0:
        raise ValueError('invalid_diameter_preference')
    return {'schema_version':'1.0','authority':'engineer_confirmed_detailing_preferences_v1',
        'allowed_operations':list(OPERATIONS),'commercial_diameter_series':list(diameter_series),
        'preferred_max_diameter_steps':max_diameter_steps,'diameter_step_preference_is_normative':False,
        'priorities':['structural_validity','constructibility','reuse_existing_detailing','simplicity'],
        'moderate_excess_area_and_anchorage_acceptable':True,'excess_limits':None,
        'values_below_required_acceptable':False,'avoid':['excessive_optimization','unnecessary_scaling','excess_positions','excess_rework'],
        'optimizer_implemented':False}


def diameter_preference(a,b,preferences):
    series=preferences['commercial_diameter_series']
    if a not in series or b not in series:return {'steps':None,'preferred':None,'reason':'diameter_outside_configured_series'}
    steps=abs(series.index(a)-series.index(b))
    return {'steps':steps,'preferred':steps<=preferences['preferred_max_diameter_steps'],
            'structural_acceptance':None,'authority':preferences['authority']}


def proposal_template():
    return {'schema_version':'1.0','beam_id':None,'floor':None,'drawing_source':None,'drawing_version':None,
        'reinforcement_mark':None,'original_geometry':None,'proposed_geometry':None,'operation':None,
        'quantities_before':{},'quantities_after':{},'units':{},'affected_checks':[],
        'reverification_results':[],'evidence':[],'pending_information':[],
        'approval_state':'DRAFT','approval_evidence':None,'graphical_reference':None,
        'physical_to_graphical_mapping_evidence':None,'ready_for_graphical_application':False}


def validate_proposal(proposal):
    p=deepcopy(proposal)
    for key in ('beam_id','floor','drawing_source','drawing_version','reinforcement_mark','original_geometry','proposed_geometry'):
        if p.get(key) is None:raise ValueError('proposal_field_missing:'+key)
    if p.get('operation') not in OPERATIONS or p.get('approval_state') not in APPROVAL_STATES:
        raise ValueError('invalid_proposal_operation_or_approval')
    for result in p.get('reverification_results',[]):
        if result.get('beam_id')!=p['beam_id'] or result.get('floor')!=p['floor']:
            raise ValueError('reverification_identity_mismatch')
    if p['approval_state']=='APPROVED':
        results=p.get('reverification_results',[])
        if (not p.get('approval_evidence') or p.get('pending_information') or not p.get('affected_checks')
                or {r.get('check_id') for r in results}!={c for c in p['affected_checks']}
                or any(r.get('status') not in ('PASS','NOT_APPLICABLE') or r.get('execution_state')!='EXECUTED_COMPLETE' for r in results)):
            raise ValueError('proposal_approval_not_proven')
    if p.get('graphical_reference') and not p.get('physical_to_graphical_mapping_evidence'):
        raise ValueError('graphical_mapping_unproven')
    p['ready_for_graphical_application']=bool(p['approval_state']=='APPROVED' and p.get('graphical_reference') and p.get('physical_to_graphical_mapping_evidence'))
    return p
