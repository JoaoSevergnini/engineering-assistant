"""Structural dispatch at intermediate supports, separate from detailing optimization."""
from copy import deepcopy
from moment_diagram import dec,tension_diagram,terminal_tension_branch
from longitudinal_review import prepare_reinforcement,check_bar_event,basic_anchorage,negative_support_terminal_demand,composition_capacity
from support_correction import check_longitudinal
from support_geometry import LongitudinalOrientation,normalize_side
from support_anchorage import _control
from termination_event import describe_termination

RULE='engineer_confirmed_intermediate_support_anchorage_when_not_required_v1'
ANCHORAGE='ANCHORAGE_BEYOND_INTERMEDIATE_SUPPORT'


def _proof(bars,context,diagram,api,support_side):
    # Entire connected terminal lobe: a shortened caller branch cannot hide demand.
    domain=terminal_tension_branch(diagram,'NEGATIVE',support_side)
    view=tension_diagram(diagram,'NEGATIVE',domain=domain)
    result=check_longitudinal(bars,context,view,api,flexure_sign='NEGATIVE')
    state=result['compatibilidade_flexao_negativa']
    if not result['regions'] or result['diagnostics'] and state is not False:
        state=None
    maximum=max((max(0,float(m)) for m in view.ms if m is not None),default=None)
    return {'sufficient_everywhere':state,'domain_m':domain,'maximum_negative_demand_knm':maximum,
        'regions':result['regions'],'diagnostics':result['diagnostics'],
        'provenance':{'regional_verification':result['provenance'],'signed_diagram':diagram.as_dict(),
            'coverage':'Entire connected terminal negative lobe, including every composition interval and piecewise-linear vertex; no extrapolation or gaps'}}


def check_intermediate_bar_event(bars,context,diagram,shear,api,*,mark,cut_side,support,
        previous_bars=None,previous_context=None,previous_diagram=None,branch_domain=None):
    """Prove need first; dispatch to unchanged SCALING or physical-face basic lb.

    support is SupportGeometry of the ADJACENT span. Previous inputs must be
    its other span, in the same global frame; no force mirroring is performed.
    Each coincident mark is independent; actual physical after is shared.
    """
    out={'bar_or_group':mark,'flexure_sign':'NEGATIVE','cut_side':normalize_side(cut_side),
        'classification':'INCONCLUSIVE','mode':'INCONCLUSIVE','passes':None,'complete':False,
        'checks':{},'diagnostics':[],'selected_solution':None,'detailing_optimization':None,
        'required_in_previous_span':None,'required_in_adjacent_span':None,'rule':RULE}
    try:
        if support.support_type!='INTERMEDIATE':raise ValueError('intermediate_support_required')
        direction=support.direction_into_span
        if (1 if out['cut_side']=='RIGHT' else -1)!=direction:raise ValueError('cut_direction_inconsistent_with_adjacent_span')
        if context.get('horizontal') is not True or context.get('sliding_formwork') is not False:
            raise ValueError('straight_horizontal_scope_unresolved')
        if direction==1 and diagram.xs[0]<dec(support.support_axis_m) or direction==-1 and diagram.xs[-1]>dec(support.support_axis_m):
            raise ValueError('adjacent_diagram_not_on_support_side')
        physical=prepare_reinforcement(bars,context,api,flexure_sign='NEGATIVE')
        matches=[b for b in physical if b['mark']==mark]
        if len(matches)!=1:raise ValueError('interrupted_mark_not_unique')
        bar=matches[0]
        if bar.get('shape')!='straight' or not bar.get('continuity_documentation'):
            raise ValueError('straight_bar_continuity_unresolved')
        left,right=sorted((dec(support.internal_face_m),dec(support.external_face_m)))
        if not dec(bar['x_start_common'])<left<right<dec(bar['x_end_common']):
            raise ValueError('bar_does_not_cross_both_physical_support_faces')
        end=bar['x_end_common' if direction==1 else 'x_start_common']
        if context.get('span_domain_m') is not None and not dec(context['span_domain_m'][0])<=dec(end)<=dec(context['span_domain_m'][1]):
            raise ValueError('bar_end_outside_known_adjacent_span')
        before=[b for b in physical if (b['x_start_common']<end<=b['x_end_common'] if direction==1 else b['x_start_common']<=end<b['x_end_common'])]
        after=[b for b in physical if (b['x_start_common']<=end<b['x_end_common'] if direction==1 else b['x_start_common']<end<=b['x_end_common'])]
        out.update(termination_event=describe_termination([b['mark'] for b in before],[b['mark'] for b in after],mark,end,cut_side),
            reinforcement_before_cut=deepcopy(before),reinforcement_after_cut=deepcopy(after),
            actual_end_position_m=end,provided_end_position_m=end,support_geometry=support.as_dict(),
            support_terminal_demand=negative_support_terminal_demand(diagram,support.support_side))
        if not after:raise ValueError('remaining_composition_missing')
        adjacent=_proof(after,context,diagram,api,support.support_side)
        out['adjacent_need_evidence']=adjacent
        state=adjacent['sufficient_everywhere']
        if state is None:raise ValueError('adjacent_branch_sufficiency_unresolved')
        out['required_in_adjacent_span']=not state
        if state is False:
            scaling=check_bar_event(bars,context,diagram,shear,api,mark=mark,cut_side=cut_side,branch_domain=branch_domain)
            scaling.update(classification='SCALING' if scaling.get('capacity_crossing',{}).get('selected_x_nec_m') is not None else 'INCONCLUSIVE',
                required_in_adjacent_span=True,required_in_previous_span=None,adjacent_need_evidence=adjacent,
                support_geometry=support.as_dict(),detailing_optimization=None)
            return scaling
        out['reason']='BAR_NOT_REQUIRED_IN_ADJACENT_SPAN'
        if previous_bars is None or previous_context is None or previous_diagram is None:
            raise ValueError('previous_span_need_evidence_missing')
        other_side='RIGHT' if support.support_side=='LEFT' else 'LEFT'
        if direction==1 and previous_diagram.xs[-1]>dec(support.support_axis_m) or direction==-1 and previous_diagram.xs[0]<dec(support.support_axis_m):
            raise ValueError('previous_diagram_not_on_opposite_support_side')
        previous=prepare_reinforcement(previous_bars,previous_context,api,flexure_sign='NEGATIVE')
        original=[b for b in previous if b['mark']==mark]
        if len(original)!=1 or any(original[0].get(k)!=bar.get(k) for k in ('bars','diameter_mm','x_start_common','x_end_common','trajectory_id')):
            raise ValueError('previous_span_bar_identity_unresolved')
        # Counterfactual individual need, never an ordered sequence of actual cuts.
        previous_proof=_proof([b for b in previous if b['mark']!=mark],previous_context,previous_diagram,api,other_side)
        previous_proof['provenance']['need_comparison']='Independently omit selected mark from original previous-span composition; peers stay original; no intermediate cut sequence'
        out['previous_need_evidence']=previous_proof
        if previous_proof['sufficient_everywhere'] is None:raise ValueError('previous_span_need_unresolved')
        out['required_in_previous_span']=not previous_proof['sufficient_everywhere']
        if not out['required_in_previous_span']:raise ValueError('bar_not_proven_required_in_previous_span')
        anchor=basic_anchorage(bar['diameter_mm'],context,api,flexure_sign='NEGATIVE')
        lb=anchor['result']['lb_cm']
        orientation=LongitudinalOrientation(cut_side,{'support_geometry':support.as_dict(),'purpose':'outward from physical face into adjacent span'})
        control=_control(orientation,end,support.internal_face_m,lb,RULE)
        if control['available_length_cm']<0:raise ValueError('negative_available_anchorage')
        control['margin_cm']=control['available_length_cm']-control['required_length_cm']
        out.update(classification=ANCHORAGE,mode=ANCHORAGE,anchorage=anchor,lb_basic_cm=lb,
            capacity_remaining=composition_capacity(after,end,context,api,flexure_sign='NEGATIVE'),
            anchorage_reference_face={'face':'right' if dec(support.internal_face_m)>dec(support.external_face_m) else 'left',
                'x_m':support.internal_face_m,'basis':'SupportGeometry.internal_face_m: physical face toward adjacent span',
                'provenance':support.as_dict(),'rule':RULE},
            checks={'basic_lb_beyond_support':control},required_end_position_m=control['required_end_position_m'],
            passes=control['passes'],complete=control['passes'] is not None,
            provenance={'rule':RULE,'event_bar':deepcopy(bar),'geometric_reference':'physical support face, independent of S1/S13 and DEPEV',
                'scope':'Structural verification of provided detailing; no detailing optimization'})
    except (ValueError,TypeError,KeyError,IndexError,StopIteration) as error:
        out['diagnostics'].append(str(error))
    return out
