"""Negative END/COLUMN structural review; no detailing optimization or resistance formulas."""
from copy import deepcopy
from collections import Counter
from importlib import import_module
from moment_diagram import dec
from longitudinal_review import prepare_reinforcement,composition_capacity,basic_anchorage,negative_support_terminal_demand
from negative_detailing import check_negative_end_node,negative_end_vertical_bend_limits
from bar_scaling import api_provenance

BEND_RULE='engineer_confirmed_negative_end_support_vertical_bend_v1'
VIBRATOR_RULE='engineer_confirmed_negative_reinforcement_vibrator_clearance_v1'
COLUMN_RULE='engineer_confirmed_column_interference_effective_cover_v1'


def control(passes=None,**data):
    return {'status':'INCONCLUSIVE' if passes is None else 'PASS' if passes else 'FAIL','passes':passes,**data}


def transverse_disposition(section,bars,*,layout=None,column_geometry=None):
    """Audit supplied physical centers; never invent or optimize a distribution.

    x_cm is measured from the beam's left lateral face. An explicit individual
    bar record per physical layer is required. Effective cover is an overlay,
    not a new resistant section or a repositioning of the original bars.
    """
    cover=section['cobrimento'];width=section['bw'];stirrup=section['diametro_estribo_mm']/10
    out={'minimum_bar_spacing':control(reason='documentary_transverse_centers_missing'),
        'vibrator_access_spacing':control(rule=VIBRATOR_RULE,required_clearance_cm=4,reason='documentary_transverse_centers_missing'),
        'column_interference_spacing':control(rule=COLUMN_RULE,reason='column_perpendicular_dimension_missing'),
        'real_lateral_cover_cm':cover,'useful_width_before_stirrup_cm':width-2*cover,
        'inside_stirrup_width_cm':width-2*(cover+stirrup),'layout':deepcopy(layout),
        'limitations':['node_interferences_not_completely_verified','vertical_alignment_of_vibrator_corridors_not_verified'],
        'provenance':{'section_unchanged':deepcopy(section),'column_geometry':deepcopy(column_geometry)}}
    applies=None;effective=cover
    try:
        if column_geometry is not None:
            if not column_geometry.get('provenance'):raise ValueError('column_dimension_provenance_missing')
            perpendicular=dec(column_geometry['perpendicular_width_cm'])
            if perpendicular<=0:raise ValueError('invalid_column_perpendicular_width')
            tolerance=dec(column_geometry.get('equivalence_tolerance_cm',0))
            if tolerance<0 or tolerance>0 and not column_geometry.get('tolerance_provenance'):
                raise ValueError('column_equivalence_tolerance_not_confirmed')
            applies=abs(perpendicular-dec(width))<=tolerance
            if applies:
                effective=cover+2.5
                out['column_interference_spacing'].update(effective_lateral_cover_cm=effective,
                    useful_width_cm=width-2*effective,inside_stirrup_width_cm=width-2*(effective+stirrup),
                    geometry_condition_confirmed=True,reason='documentary_transverse_centers_missing')
            else:
                out['column_interference_spacing']={'status':'NOT_APPLICABLE','passes':None,'rule':COLUMN_RULE,
                    'geometry_condition_confirmed':False,'reason':'perpendicular_dimension_not_equivalent_to_beam_width',
                    'provenance':deepcopy(column_geometry)}
    except (ValueError,KeyError,TypeError) as error:
        out['column_interference_spacing']['reason']=str(error)
    if layout is None:return out
    try:
        if not layout.get('provenance') or not layout.get('layers'):raise ValueError('transverse_layout_source_or_layers_missing')
        expected=Counter((b['mark'],i+1,b['diameter_mm']) for b in bars for i,n in enumerate(b['layers']) for _ in range(n))
        actual=Counter();details=[];clearances=[];minimum_ok=True;bounds_ok=True;column_bounds=True
        minimum=import_module('concretopy.normas').espacamento_min_arm_long_viga
        seen=set()
        for layer in layout['layers']:
            index=layer['layer']
            if type(index)!=int or index<1 or index in seen:raise ValueError('transverse_layer_identity_invalid')
            seen.add(index);positions=sorted(layer['bars'],key=lambda b:dec(b['x_cm']))
            if not positions:raise ValueError('empty_transverse_layer')
            for b in positions:
                phi=dec(b['diameter_mm'])/10;x=dec(b['x_cm']);actual[(b['mark'],index,b['diameter_mm'])]+=1
                bounds_ok &= x-phi/2>=dec(cover+stirrup) and x+phi/2<=dec(width-cover-stirrup)
                column_bounds &= x-phi/2>=dec(effective+stirrup) and x+phi/2<=dec(width-effective-stirrup)
            gaps=[]
            for a,b in zip(positions,positions[1:]):
                free=float(dec(b['x_cm'])-dec(a['x_cm'])-(dec(a['diameter_mm'])+dec(b['diameter_mm']))/20)
                required=max(minimum(a['diameter_mm']),minimum(b['diameter_mm']))
                okay=dec(free)>=dec(required);minimum_ok &= okay;clearances.append(free)
                gaps.append({'left_bar':deepcopy(a),'right_bar':deepcopy(b),'free_cm':free,'minimum_cm':required,'passes':okay})
            details.append({'layer':index,'gaps':gaps})
        if actual!=expected:raise ValueError('transverse_layout_does_not_match_actual_reinforcement')
        common={'layers':details,'provenance':{'layout':deepcopy(layout['provenance']),
            'minimum_spacing_api':api_provenance(minimum),'aggregate_parameter':'existing Concretopy default 16 mm, not a project aggregate certification'}}
        out['minimum_bar_spacing']=control(minimum_ok and bounds_ok,**deepcopy(common),
            pairwise_minimum_passes=minimum_ok,physical_lateral_bounds_passes=bounds_ok)
        maximum=max(clearances) if clearances else None
        corridor=maximum is not None and dec(maximum)>=dec(4)
        out['vibrator_access_spacing']=control(corridor and minimum_ok and bounds_ok,rule=VIBRATOR_RULE,
            maximum_free_spacing_cm=maximum,required_clearance_cm=4,raw_corridor_passes=corridor,
            minimum_spacing_passes=minimum_ok,physical_lateral_bounds_passes=bounds_ok,**deepcopy(common))
        if applies is True:
            out['column_interference_spacing']=control(column_bounds and minimum_ok and corridor,rule=COLUMN_RULE,
                effective_lateral_cover_cm=effective,useful_width_cm=width-2*effective,
                inside_stirrup_width_cm=width-2*(effective+stirrup),geometry_condition_confirmed=True,
                lateral_bounds_passes=column_bounds,minimum_spacing_passes=minimum_ok,vibrator_corridor_passes=corridor,
                provenance={'column':deepcopy(column_geometry),'layout':deepcopy(layout['provenance']),
                    'scope':'Effective lateral cover only; original section, d and flexural capacity unchanged'})
    except (ValueError,KeyError,TypeError) as error:
        out['minimum_bar_spacing']['reason']=str(error);out['vibrator_access_spacing']['reason']=str(error)
        if applies is True:out['column_interference_spacing']['reason']=str(error)
    return out


def check_negative_end_support(bars,context,diagram,api,*,geometry,mark,
        bend_leg_cm=None,bend_provenance=None,transverse_layout=None,column_geometry=None):
    """Independent structural, anchorage and disposition controls of actual marks."""
    out={'verification':'NEGATIVE_END_SUPPORT_ANCHORAGE','bar':mark,'support':geometry.support_id,
        'support_type':geometry.support_type,'support_side':geometry.support_side,'geometry':geometry.as_dict(),
        'checks':{},'diagnostics':[],'selected_solution':None,'detailing_optimization':None,
        'global_beam_approval':None,'ready_for_detailing':False,'provenance':{'context':deepcopy(context)}}
    names=('flexural_capacity','straight_anchorage_geometry','vertical_bend_geometry','minimum_bar_spacing',
        'vibrator_access_spacing','column_interference_spacing','curved_anchorage_resistance')
    out['checks']={name:control() for name in names}
    try:
        if geometry.support_type!='END' or context.get('support_element')!='COLUMN' or not context.get('support_scenario_provenance'):
            raise ValueError('end_column_support_not_confirmed')
        matches=[b for b in bars if b.get('mark')==mark and b.get('function')=='negative']
        if len(matches)!=1:raise ValueError('negative_mark_not_unique')
        bar=matches[0]
        penetration=geometry.penetration(bar)
        if not penetration['area_presente_na_face'] or penetration['continuity']=='CONTINUES_THROUGH_SUPPORT':
            raise ValueError('negative_mark_end_support_trajectory_unresolved')
        out['physical_bar']=deepcopy(bar);out['provenance']['bar']=deepcopy(bar)
        # Same deterministic anchorage and geometry as legacy end-node review.
        legacy=check_negative_end_node(bar,context,geometry,api,bend_leg_cm=bend_leg_cm,bend_provenance=bend_provenance)
        out['legacy_node_check']=legacy
        if 'anchorage' not in legacy:raise ValueError('basic_anchorage_unresolved')
        out['anchorage']=legacy['anchorage'];lb=legacy['anchorage']['result']['lb_cm'];out['lb_basic_cm']=lb
        possible=legacy['straight_geometrically_possible'];straight=legacy['straight_anchorage_passes']
        out['checks']['straight_anchorage_geometry']=control(straight,
            required_basic_lb_cm=lb,available_space_cm=geometry.support_width_cm-context['section']['cobrimento'],
            documentary_horizontal_projection_cm=penetration['comprimento_penetracao_cm'],
            geometrically_possible=possible,reference_face_m=geometry.internal_face_m,
            reason='A bent-bar projection is not a verified straight anchorage',provenance=geometry.as_dict())
        side_bend=bar.get('end_bend',{})
        documented_bend=bar.get('termination_by_side',{}).get(geometry.support_side)=='VERTICAL_BEND' or (
            side_bend.get('side','').upper()==geometry.support_side and side_bend.get('orientation')=='vertical')
        if bend_provenance and bend_provenance.get('orientation')=='vertical' and bend_provenance.get('support_side')==geometry.support_side:
            documented_bend=True
        if straight:
            out['anchorage_mode']='STRAIGHT'
            out['checks']['vertical_bend_geometry']={'status':'NOT_APPLICABLE','passes':None,'rule':BEND_RULE}
            out['checks']['curved_anchorage_resistance']={'status':'NOT_APPLICABLE','passes':None}
        elif documented_bend:
            out['anchorage_mode']='VERTICAL_BEND'
            limits=negative_end_vertical_bend_limits(context,lb)
            section=context['section'];provided=None
            if bend_leg_cm is not None and bend_provenance:
                if dec(bend_leg_cm)>=0:provided=bend_leg_cm
                else:out['diagnostics'].append('negative_documentary_bend_length')
            margin=None if provided is None else float(dec(provided)-dec(limits['vertical_bend_required_cm']))
            out['checks']['vertical_bend_geometry']=control(None if margin is None else margin>=0,
                rule=BEND_RULE,beam_height_cm=section['h'],cover_cm=section['cobrimento'],
                stirrup_diameter_mm=section['diametro_estribo_mm'],lb_basic_cm=lb,**limits,
                vertical_bend_provided_cm=provided,margin_cm=margin,
                provenance={'documentary_leg':deepcopy(bend_provenance),'section':deepcopy(section),
                    'interpretation':'Vertical leg only, never horizontal + vertical or straight equivalent'})
            out['checks']['curved_anchorage_resistance']=control(reason='Curved anchorage resistance, pin/radius and node confinement not represented; no alpha=0.7 credit')
        else:
            out['anchorage_mode']='UNRESOLVED'
            out['checks']['vertical_bend_geometry'].update(rule=BEND_RULE,reason='vertical_bend_not_documented_at_this_support')
        # Flexure is independent: unresolved terminal/centers never erases bend check.
        at_face=None
        try:
            terminal=negative_support_terminal_demand(diagram,geometry.support_side);out['terminal_demand']=terminal
            physical=prepare_reinforcement(bars,context,api,flexure_sign='NEGATIVE')
            at_face=[b for b in physical if b['x_start_common']<=geometry.internal_face_m<=b['x_end_common']]
            at_terminal=[b for b in physical if b['x_start_common']<=terminal['x_m']<=b['x_end_common']]
            if {b['mark'] for b in at_face}!={b['mark'] for b in at_terminal}:raise ValueError('face_and_terminal_resistant_compositions_differ')
            capacity=composition_capacity(at_face,geometry.internal_face_m,context,api,flexure_sign='NEGATIVE')
            demand=terminal['negative_demand_knm'];out['capacity']=capacity
            if not capacity['valid']:raise ValueError('terminal_flexural_capacity_invalid')
            check=control(capacity['Mk_equivalent_knm']>=demand,MRd_knm=capacity['MRd_knm'],
                Mk_equivalent_knm=capacity['Mk_equivalent_knm'],negative_terminal_demand_knm=demand,
                d_equivalent_cm=capacity['concretopy']['d_equivalente_cm'],composition=deepcopy(at_face),
                rule=terminal['rule'],provenance={'capacity':capacity['provenance'],'terminal':terminal})
            if demand==0:check.update(status='NOT_APPLICABLE',passes=None,reason='terminal TQS moment is not negative; physical mark may serve other regions')
            remaining=[b for b in at_face if b['mark']!=mark]
            remaining_capacity=composition_capacity(remaining,geometry.internal_face_m,context,api,flexure_sign='NEGATIVE') if remaining else None
            check['selected_mark_required_at_terminal']=False if demand==0 else (
                True if not remaining else None if not remaining_capacity['valid'] else remaining_capacity['Mk_equivalent_knm']<demand)
            check['capacity_without_selected_mark']=remaining_capacity
            out['checks']['flexural_capacity']=check
        except (ValueError,TypeError,KeyError,IndexError) as error:
            out['checks']['flexural_capacity']['reason']=str(error)
        # Transverse geometry remains evaluable independently of flexural demand.
        if at_face is None and context.get('layer_order_basis')=='from_tension_face':
            at_face=[deepcopy(b) for b in bars if b.get('function')=='negative' and b.get('face')=='upper' and b['x_start_common']<=geometry.internal_face_m<=b['x_end_common']]
        if at_face is not None:
            transverse=transverse_disposition(context['section'],at_face,layout=transverse_layout,column_geometry=column_geometry)
            out['transverse_disposition']=transverse
            for name in ('minimum_bar_spacing','vibrator_access_spacing','column_interference_spacing'):
                out['checks'][name]=transverse[name]
        out['provenance']['separation']='terminal TQS force; physical support faces; actual bar and vertical bend; independent transverse cover overlay'
    except (ValueError,TypeError,KeyError,IndexError) as error:out['diagnostics'].append(str(error))
    return out


def review_negative_end_support(bars,context,diagram,api,*,geometry,bend_documents=None,
        transverse_layout=None,column_geometry=None):
    """Discover actual negative marks reaching the END support; no armature search."""
    out={'support':geometry.as_dict(),'marks':[],'diagnostics':[],
        'selected_solution':None,'detailing_optimization':None}
    if geometry.support_type!='END' or context.get('support_element')!='COLUMN':
        out['diagnostics'].append('end_column_support_not_confirmed');return out
    for bar in bars:
        if bar.get('function')!='negative' or bar.get('face')!='upper':continue
        try:
            if not geometry.penetration(bar)['area_presente_na_face']:continue
            document=(bend_documents or {}).get(bar['mark'])
            if document is None:
                explicit=bar.get('end_bend') or {}
                if explicit.get('side','').upper()==geometry.support_side:document=explicit
            out['marks'].append(check_negative_end_support(bars,context,diagram,api,geometry=geometry,mark=bar['mark'],
                bend_leg_cm=None if document is None else document.get('vertical_leg_cm'),
                bend_provenance=None if document is None else {
                    'orientation':document.get('orientation'),'support_side':document.get('side'),
                    'source':document.get('provenance')} if document.get('provenance') else None,
                transverse_layout=transverse_layout,column_geometry=column_geometry))
        except (ValueError,TypeError,KeyError) as error:out['diagnostics'].append(str(error))
    if not out['marks']:out['diagnostics'].append('no_negative_mark_documented_at_end_support')
    return out
