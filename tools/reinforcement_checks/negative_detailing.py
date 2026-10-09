"""Negative-specific detailing decisions; no resistant formula duplicates."""
from copy import deepcopy
from moment_diagram import dec
from support_geometry import SupportGeometry
from support_anchorage import _complete_pass
from longitudinal_review import basic_anchorage

HOLDER_RULE='engineer_confirmed_beam_stirrup_holder_diameter_v1'
CONTINUITY_RULE='engineer_confirmed_negative_intermediate_support_extension_v1'
BEND_RULE='engineer_confirmed_negative_end_frame_node_bend_v1'
CANTILEVER_RULE='engineer_confirmed_single_cantilever_negative_anchorage_1_5lb_v1'
TAIL_RULE='engineer_confirmed_cantilever_free_end_negative_tail_v1'


def check_stirrup_holder(bar,stirrups,diagram):
    """Spatial overlap with actual stirrup intervals, not global maximum phi."""
    out={'classification':'UNKNOWN','regions':[],'required_diameter_mm':None,'passes':None,'diagnostics':[],
        'rule':HOLDER_RULE,'provenance':{'bar':deepcopy(bar),'stirrup_regions':deepcopy(stirrups)}}
    try:
        if bar.get('explicit_skin') is True or (bar.get('function')=='skin' and bar.get('function_provenance')):
            out.update(classification='SKIN',status='NOT_APPLICABLE');return out
        if bar.get('function')!='stirrup_holder' or not bar.get('function_provenance'):
            raise ValueError('upper_bar_function_unknown')
        a,b=map(dec,(bar['x_start_common'],bar['x_end_common']))
        if a>=b:raise ValueError('invalid_holder_interval')
        points=[diagram.moment_at_x(float(x)) for x in sorted({a,b,*[x for x in diagram.xs if a<=x<=b]})]
        if any(p['status']!='resolved' for p in points):raise ValueError('holder_moment_domain_unresolved')
        if any(p['value_knm']<0 for p in points):raise ValueError('negative_demand_requires_resistant_reinforcement')
        events={a,b}; intervals=[]
        for stirrup in stirrups or []:
            x,y=map(dec,(stirrup['x_start_common'],stirrup['x_end_common']))
            if x>=y or stirrup.get('diameter_mm') is None or not stirrup.get('provenance'):raise ValueError('stirrup_interval_or_source_unresolved')
            if max(a,x)<min(b,y):
                intervals.append((x,y,stirrup));events.update([max(a,x),min(b,y)])
        for x,y in zip(sorted(events),sorted(events)[1:]):
            mid=(x+y)/2;active=[s for left,right,s in intervals if left<=mid<=right]
            if len(active)!=1:raise ValueError('stirrup_region_missing_or_overlapping')
            phi=active[0]['diameter_mm']
            if dec(phi)<=0:raise ValueError('invalid_stirrup_diameter')
            out['regions'].append({'start_m':float(x),'end_m':float(y),'stirrup_diameter_mm':phi,
                'required_holder_diameter_mm':max(6.3,phi),'provenance':deepcopy(active[0])})
        if not out['regions']:raise ValueError('stirrup_regions_missing')
        out['classification']='STIRRUP_HOLDER'
        if len({r['stirrup_diameter_mm'] for r in out['regions']})!=1:
            raise ValueError('holder_crosses_stirrup_diameter_change_requires_engineer_decision')
        required=out['regions'][0]['required_holder_diameter_mm'];out['required_diameter_mm']=required
        out['passes']=dec(bar['diameter_mm'])>=dec(required)
    except (ValueError,TypeError,KeyError) as error:out['diagnostics'].append(str(error))
    return out


def check_intermediate_continuity(left_bar,right_bar,left_support,right_support,left_check,right_check):
    out={'continuity':'UNKNOWN','passes':None,'rule':CONTINUITY_RULE,'diagnostics':[],
        'left_span_check':deepcopy(left_check),'right_span_check':deepcopy(right_check),
        'required_extension_left_span':left_check.get('required_end_position_m'),
        'required_extension_right_span':right_check.get('required_end_position_m'),
        'provenance':{'left_bar':deepcopy(left_bar),'right_bar':deepcopy(right_bar)}}
    try:
        if not isinstance(left_support,SupportGeometry) or not isinstance(right_support,SupportGeometry):raise ValueError('physical_support_geometry_missing')
        if left_support.support_side!='RIGHT' or right_support.support_side!='LEFT' or left_support.support_type!='INTERMEDIATE' or right_support.support_type!='INTERMEDIATE':raise ValueError('adjacent_support_orientation_invalid')
        if left_support.support_id!=right_support.support_id or left_support.span_id==right_support.span_id:raise ValueError('adjacent_span_or_support_identity_invalid')
        if dec(left_support.internal_face_m)!=dec(right_support.external_face_m) or dec(left_support.external_face_m)!=dec(right_support.internal_face_m):raise ValueError('adjacent_common_support_faces_incompatible')
        for bar in (left_bar,right_bar):
            if bar.get('function')!='negative' or bar.get('face')!='upper':raise ValueError('negative_bar_identity_missing')
        if left_bar.get('continuity_documentation') is None or right_bar.get('continuity_documentation') is None:raise ValueError('continuity_documentary_evidence_missing')
        for key in ('mark','diameter_mm','layers','trajectory_id','physical_layer_id'):
            if left_bar.get(key) is None or left_bar.get(key)!=right_bar.get(key):raise ValueError('continuity_identity_or_trajectory_incompatible:'+key)
        for geometry,bar in ((left_support,left_bar),(right_support,right_bar)):
            if geometry.penetration(bar)['continuity']!='CONTINUES_THROUGH_SUPPORT':
                out['continuity']='TERMINATES_IN_SUPPORT';out['diagnostics'].append('bar_does_not_cross_support');return out
        out['continuity']='CONTINUES_THROUGH_SUPPORT'
        out['passes']=_complete_pass([left_check.get('passes'),right_check.get('passes')])
        out['provenance']['support_geometries']=[left_support.as_dict(),right_support.as_dict()]
    except (ValueError,TypeError,KeyError) as error:out['diagnostics'].append(str(error))
    return out


def negative_end_vertical_bend_limits(context,lb):
    """Existing geometric rule, shared by legacy node and explicit end review."""
    section=context['section']
    geometric=section['h']-section['cobrimento']-section['diametro_estribo_mm']/10
    if geometric<=0 or dec(lb)<=0:raise ValueError('invalid_negative_bend_geometry')
    return {'geometric_limit_cm':geometric,'two_lb_cm':2*lb,
        'vertical_bend_required_cm':min(geometric,2*lb),
        'governing':'GEOMETRY' if geometric<=2*lb else 'TWO_BASIC_LB'}


def check_negative_end_node(bar,context,geometry,api,*,scenario='FRAME_END',bend_leg_cm=None,bend_provenance=None):
    """Straight basic anchorage or geometrical bend proposal; no hook reduction.

    A defined bend does NOT verify resistant anchorage, pino or fabrication C.
    """
    out={'scenario':scenario,'straight_anchorage_passes':None,'bend_geometry_defined':False,
        'anchorage_resistance_verified':None,'fabrication_geometry_complete':False,'passes':None,
        'diagnostics':[],'selected_solution':None,'provenance':{'bar':deepcopy(bar),'context':deepcopy(context)},
        'rule':CANTILEVER_RULE if scenario=='SINGLE_CANTILEVER_COLUMN' else BEND_RULE}
    try:
        if scenario not in ('FRAME_END','SINGLE_CANTILEVER_COLUMN'):raise ValueError('unsupported_negative_end_scenario')
        if not isinstance(geometry,SupportGeometry) or geometry.support_type!='END':raise ValueError('negative_end_geometry_unresolved')
        if bar.get('function')!='negative' or bar.get('face')!='upper':raise ValueError('negative_bar_unresolved')
        if context.get('support_element')!='COLUMN' or not context.get('support_scenario_provenance'):raise ValueError('column_frame_or_cantilever_scenario_unresolved')
        if scenario=='SINGLE_CANTILEVER_COLUMN' and (context.get('span_count')!=1 or context.get('cantilever_type')!='SINGLE_FIXED_COLUMN'):raise ValueError('cantilever_1_5lb_outside_confirmed_scope')
        anchor=basic_anchorage(bar['diameter_mm'],context,api,flexure_sign='NEGATIVE');lb=anchor['result']['lb_cm']
        required=lb*(1.5 if scenario=='SINGLE_CANTILEVER_COLUMN' else 1)
        out['anchorage']=anchor;out['straight_required_cm']=required
        penetration=geometry.penetration(bar);out['penetration']=penetration
        space=geometry.support_width_cm-context['section']['cobrimento']
        out['straight_geometrically_possible']=space>=required
        # Existing bend endpoints are projections, not proven straight developments.
        explicit=bar.get('termination_by_side',{}).get(geometry.support_side)
        straight=bar.get('shape')=='straight' or explicit=='STRAIGHT'
        if penetration['continuity']=='CONTINUES_THROUGH_SUPPORT':raise ValueError('end_bar_continuity_rule_unresolved')
        out['straight_anchorage_passes']=straight and penetration['area_presente_na_face'] and penetration['comprimento_penetracao_cm']>=required
        if out['straight_anchorage_passes']:
            out.update(anchorage_mode='STRAIGHT',anchorage_resistance_verified=True,passes=True);return out
        if out['straight_geometrically_possible']:
            out.update(anchorage_mode='STRAIGHT_EXTENSION_REQUIRED',anchorage_resistance_verified=False,passes=False,
                required_end_position_m=geometry.required_end(geometry.internal_face_m,required));return out
        limits=negative_end_vertical_bend_limits(context,lb)
        geometric=limits['geometric_limit_cm'];required_leg=limits['vertical_bend_required_cm']
        out.update(anchorage_mode='BEND_REQUIRED',bend_geometry_defined=True,L_bend_geom_cm=geometric,
            L_bend_cm=required_leg,bend_governing='GEOMETRY' if geometric<=2*lb else 'TWO_BASIC_LB',
            bend_leg_available_cm=bend_leg_cm,bend_geometry_passes=None if bend_leg_cm is None or not bend_provenance else dec(bend_leg_cm)>=dec(required_leg))
        out['diagnostics']+=['bend_anchorage_resistance_not_verified','bend_pino_radius_and_fabrication_C_unresolved']
        out['provenance']['bend_leg']=deepcopy(bend_provenance)
    except (ValueError,TypeError,KeyError) as error:out['diagnostics'].append(str(error))
    return out


def check_cantilever_free_end(context,*,bend_leg_cm=None,provenance=None,other_checks=()):
    out={'rule':TAIL_RULE,'tail_mode':'FREE_END_BEND_LEG','passes':None,'required_leg_cm':None,
        'available_leg_cm':bend_leg_cm,'tail_geometry_passes':None,'diagnostics':[],
        'fabrication_geometry_complete':False,'other_checks':deepcopy(list(other_checks)),
        'provenance':{'context':deepcopy(context),'bend_leg':deepcopy(provenance),
            'engineer_clarification':'Sobra is the free-end bend leg, not longitudinal projection'}}
    try:
        if context.get('cantilever_type')!='SINGLE_FIXED_COLUMN' or context.get('span_count')!=1:raise ValueError('cantilever_tail_scope_unresolved')
        s=context['section'];required=s['h']-2*s['cobrimento']-s['diametro_estribo_mm']/10
        if required<=0:raise ValueError('invalid_cantilever_tail_geometry')
        out['required_leg_cm']=required
        if bend_leg_cm is None or not provenance:raise ValueError('free_end_bend_leg_length_or_source_missing')
        if dec(bend_leg_cm)<0:raise ValueError('negative_bend_leg_length')
        tail=dec(bend_leg_cm)>=dec(required);out['tail_geometry_passes']=tail
        out['passes']=_complete_pass([tail,*[c.get('passes') for c in other_checks]])
        # Orthogonal constraints are not converted into a fictitious longitudinal end.
        out['governing_conditions']=['FREE_END_TAIL'] if tail is False else [c.get('rule','LONGITUDINAL_CONTROL') for c in other_checks if c.get('passes') is False]
    except (ValueError,TypeError,KeyError) as error:out['diagnostics'].append(str(error))
    return out
