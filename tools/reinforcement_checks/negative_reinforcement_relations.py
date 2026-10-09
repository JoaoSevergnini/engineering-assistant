"""Semantic relations of negative pieces. Existing deterministic engines intact."""
from copy import deepcopy
from moment_diagram import dec
from longitudinal_review import prepare_reinforcement, composition_capacity, basic_anchorage
from negative_detailing import check_stirrup_holder
from negative_end_support_review import control, transverse_disposition
from steel_mass import steel_mass

RULES={name:'engineer_confirmed_negative_'+suffix+'_v1' for name,suffix in (
 ('continuity','continuity_preference'),('overlap','detailing_overlap'),
 ('weight','detailing_overlap_weight_choice'),('gap','detailing_overlap_max_gap'),
 ('lap','lap_transition'),('capacity','overlap_capacity'),('spacing','overlap_local_spacing'))}

def interval_demand(diagram,start,end):
    out=control(reason='moment_interval_unresolved',points=[])
    try:
        a,b=dec(start),dec(end)
        if a>=b:raise ValueError('empty_or_inverted_moment_interval')
        points=[diagram.moment_at_x(float(x)) for x in sorted({a,b,*[x for x in diagram.xs if a<=x<=b]})]
        out['points']=points
        if any(p['status']!='resolved' for p in points):raise ValueError('moment_gap_or_outside_domain')
        demand=max(max(0,-p['value_knm']) for p in points)
        out=control(True,points=points,max_negative_demand_knm=demand,
            governing=[p for p in points if max(0,-p['value_knm'])==demand],
            negative_never_zeros=all(p['value_knm']<0 for p in points),
            provenance={'diagram':deepcopy(diagram.provenance),'interval_m':[start,end],
                'proof':'endpoints and all internal vertices of existing piecewise-linear diagram; original sign'})
    except (ValueError,KeyError,TypeError) as e:out['reason']=str(e)
    return out

def _area(bar,api):
    if type(bar['bars'])!=int or bar['bars']<1:raise ValueError('invalid_bar_count')
    return bar['bars']*api.Barra(bar['diameter_mm']).area_cm2

def compare_detailing_mass(a,b,api,*,required_geometry,physical_overlap_cm,
        hanger=None,diagram=None,stirrups=None,density=None):
    out={'maximum_gap_cm':80.0,'required_overlap_cm':30.0,'applicable':None,
        'extension_mass':control(),'hanger_mass':control(),
        'lower_steel_mass_alternative':None,'diagnostics':[],
        'rules':[RULES['weight'],RULES['gap'],RULES['overlap']]}
    try:
        if not required_geometry or not required_geometry.get('provenance'):
            raise ValueError('structurally_required_limits_unresolved')
        gap=(dec(required_geometry['required_start_bar_b_m'])-dec(required_geometry['required_end_bar_a_m']))*100
        out.update(required_geometry=deepcopy(required_geometry),gap_cm=float(gap),applicable=gap<=80)
        if physical_overlap_cm<0:raise ValueError('invalid_physical_overlap_length')
        if gap>80:
            out['extension_mass']=control(status='NOT_APPLICABLE',reason='gap_exceeds_80_cm');return out
        areas=[_area(x,api) for x in (a,b)];indices=[i for i,v in enumerate(areas) if v==min(areas)]
        out['smaller_As_candidates']=[(a,b)[i]['mark'] for i in indices]
        if len(indices)!=1:raise ValueError('equal_total_areas_no_extension_tiebreak')
        chosen=(a,b)[indices[0]];out['smaller_As_bar']=chosen['mark']
        added=max(dec(0),dec(30)-dec(physical_overlap_cm)) if physical_overlap_cm>0 else max(dec(0),gap+30)
        out['extension_alternative']={'additional_length_per_bar_cm':float(added),'number_of_bars':chosen['bars'],
            'total_added_length_m':float(added*chosen['bars']/100),
            'baseline':'physical overlap deficit when present; otherwise structurally required limits',
            'provenance':{'required_geometry':deepcopy(required_geometry),'physical_overlap_cm':physical_overlap_cm}}
        if not density or not density.get('provenance'):raise ValueError('steel_mass_density_unresolved')
        mass=steel_mass(api.Barra(chosen['diameter_mm']).area_cm2,out['extension_alternative']['total_added_length_m'],
            density_kg_m3=density['kg_m3'],provenance=density['provenance'])
        out['extension_mass']=control(True,**mass)
        if not hanger or not hanger.get('quantity_length_provenance'):
            raise ValueError('holder_count_length_or_minimum_policy_unresolved')
        holder=check_stirrup_holder(hanger,stirrups,diagram);out['holder_rule_check']=holder
        if holder['passes'] is not True:raise ValueError('holder_existing_rule_not_satisfied')
        if type(hanger['bars'])!=int or hanger['bars']<1 or not hanger.get('minimum_length_policy_provenance') or hanger['minimum_length_cm']<0 or hanger['length_cm']<max(hanger['minimum_length_cm'],float((dec(hanger['x_end_common'])-dec(hanger['x_start_common']))*100)):
            raise ValueError('holder_count_or_minimum_length_policy_unresolved_or_failed')
        mass=steel_mass(api.Barra(hanger['diameter_mm']).area_cm2,float(dec(hanger['length_cm'])*hanger['bars']/100),
            density_kg_m3=density['kg_m3'],provenance={'density':density['provenance'],'holder':deepcopy(hanger)})
        out['hanger_mass']=control(True,**mass)
        x,y=out['extension_mass']['mass_kg'],mass['mass_kg']
        out['lower_steel_mass_alternative']='EXTEND_NEGATIVE_REINFORCEMENT' if x<y else 'USE_HANGER_REINFORCEMENT' if x>y else 'EQUIVALENT_STEEL_WEIGHT'
    except (ValueError,KeyError,TypeError) as e:out['diagnostics'].append(str(e))
    return out

def local_overlap_disposition(section,bars,*,relation_type,layout=None,direct_pairs=()):
    base=transverse_disposition(section,bars,layout=layout)
    out={'global_disposition':base,'local_spacing_geometry':control(),
        'vibrator_access_spacing':deepcopy(base['vibrator_access_spacing']),
        'rule':RULES['spacing'],'invented_positions':False}
    if relation_type not in ('DETAILING_OVERLAP','REINFORCEMENT_LAP_TRANSITION'):
        out['local_spacing_geometry']=control(status='NOT_APPLICABLE');return out
    minimum=base['minimum_bar_spacing']
    if 'layers' not in minimum:return out
    try:
        pairs={frozenset(p) for p in direct_pairs}
        records=[b for layer in layout['layers'] for b in layer['bars']]
        ids=[b.get('id') for b in records]
        if pairs and (None in ids or len(set(ids))!=len(ids)):raise ValueError('individual_pair_identity_missing')
        participant_marks={b['mark'] for b in bars}
        if pairs and len(participant_marks)!=2:raise ValueError('exactly_two_overlap_groups_required_for_local_exception')
        lookup={b.get('id'):b for b in records}
        for pair in pairs:
            if len(pair)!=2 or not pair.issubset(lookup):raise ValueError('invalid_direct_overlap_pair')
            members=[lookup[x] for x in pair]
            if members[0]['mark']==members[1]['mark'] or any(x['mark'] not in participant_marks for x in members):raise ValueError('overlap_pair_must_join_distinct_groups')
        details=deepcopy(minimum['layers']);okay=True
        for layer in details:
            for gap in layer['gaps']:
                exempt=frozenset((gap['left_bar'].get('id'),gap['right_bar'].get('id'))) in pairs
                gap['local_exception']=exempt
                gap['local_passes']=gap['free_cm']>=0 if exempt else gap['passes']
                okay &= gap['local_passes']
        okay &= minimum['physical_lateral_bounds_passes']
        out['local_spacing_geometry']=control(okay,layers=details,direct_pairs=deepcopy(list(direct_pairs)),
            physical_lateral_bounds_passes=minimum['physical_lateral_bounds_passes'],rule=RULES['spacing'],
            limitations=['interlayer_collisions_and_node_interferences_not_verified'])
        out['vibrator_access_spacing']=control(okay and base['vibrator_access_spacing']['raw_corridor_passes'],
            required_clearance_cm=4,maximum_free_spacing_cm=base['vibrator_access_spacing']['maximum_free_spacing_cm'],
            reason='global corridor; not necessarily between overlapping bars')
    except (ValueError,KeyError,TypeError) as e:out['local_spacing_geometry']=control(reason=str(e))
    return out

def review_negative_relation(a,b,context,diagram,api,*,support_pair,evidence,
        required_geometry=None,hanger=None,stirrups=None,density=None,
        layout=None,direct_pairs=(),regional_checks=()):
    out={'relation_classification':'INCONCLUSIVE','bar_a':deepcopy(a),'bar_b':deepcopy(b),
        'support_pair':deepcopy(support_pair),'diagnostics':[],
        'overlap_length_check':control(),'overlap_flexural_capacity':control(),
        'local_spacing_geometry':control(),'vibrator_access_spacing':control(),
        'mixed_centroid_used':False,'regional_checks':deepcopy(list(regional_checks)),
        'selected_solution':None,'detailing_optimization':None,'ready_for_detailing':False,
        'provenance':{'rules':deepcopy(RULES),'evidence':deepcopy(evidence),'context':deepcopy(context)}}
    try:
        if len(support_pair)!=2 or not all(s.get('provenance') for s in support_pair):raise ValueError('support_geometry_or_source_missing')
        left,right=support_pair
        if right['occurrence']!=left['occurrence']+1 or left['right_face_m']>=right['left_face_m']:
            raise ValueError('supports_not_consecutive')
        if not evidence or not evidence.get('provenance'):raise ValueError('structural_association_missing')
        if evidence.get('support_ids')!=[left['id'],right['id']]:raise ValueError('support_association_mismatch')
        for bar in (a,b):
            if bar.get('function')!='negative' or bar.get('face')!='upper' or not bar.get('source'):raise ValueError('negative_group_source_missing')
            if dec(bar['x_start_common'])>=dec(bar['x_end_common']):raise ValueError('invalid_bar_interval')
        out['bar_a']['As_total_cm2']=_area(a,api);out['bar_b']['As_total_cm2']=_area(b,api)
        moment=interval_demand(diagram,left['right_face_m'],right['left_face_m']);out['moment_between_supports']=moment
        same=all(a.get(k) is not None and a.get(k)==b.get(k) for k in (
            'mark','trajectory_id','physical_layer_id','layers','diameter_mm','bars','x_start_common','x_end_common'))
        if same and a.get('continuity_documentation') and b.get('continuity_documentation'):
            if a['x_start_common']>left['left_face_m'] or a['x_end_common']<right['right_face_m']:
                raise ValueError('piece_does_not_cross_both_supports')
            out.update(relation_classification='CONTINUOUS_NEGATIVE_REINFORCEMENT',
                classification_reason='same documented physical piece spans both supports without termination',
                continuity_proven=True,resistance_bonus=False)
            for key in ('overlap_length_check','overlap_flexural_capacity'):out[key]=control(status='NOT_APPLICABLE',reason='existing regional flexure governs resistance')
            return out
        if a['mark']==b['mark']:raise ValueError('same_mark_physical_identity_unproven')
        if moment['passes'] is not True:raise ValueError('entire_between_supports_domain_unresolved')
        if not (dec(a['x_start_common'])<=dec(left['right_face_m'])<=dec(a['x_end_common']) and
                dec(b['x_start_common'])<=dec(right['left_face_m'])<=dec(b['x_end_common'])):
            raise ValueError('groups_not_present_at_their_associated_support_faces')
        inferred_role='resistant_transition' if moment['negative_never_zeros'] else 'adjacent_support_tails'
        role=evidence.get('role',inferred_role)
        if moment['negative_never_zeros']:
            if role!='resistant_transition':raise ValueError('resistant_transition_role_unproven')
            relation='REINFORCEMENT_LAP_TRANSITION'
        else:
            if role!='adjacent_support_tails':raise ValueError('structural_tail_role_unproven')
            if not required_geometry or not required_geometry.get('provenance'):
                if not evidence.get('existing_tail_meeting_confirmed'):raise ValueError('required_tail_limits_missing')
                relation='DETAILING_OVERLAP'
            else:
                required_a=required_geometry['required_end_bar_a_m'];required_b=required_geometry['required_start_bar_b_m']
                gap=(dec(required_b)-dec(required_a))*100
                if gap>0:
                    gap_demand=interval_demand(diagram,required_a,required_b);out['required_gap_demand']=gap_demand
                    if gap_demand['passes'] is not True or gap_demand['max_negative_demand_knm']>0:
                        raise ValueError('negative_free_required_gap_not_proven')
                relation='DETAILING_OVERLAP' if gap<=80 else 'INDEPENDENT_REINFORCEMENTS'
                out['required_geometry']=deepcopy(required_geometry)
        out.update(relation_classification=relation,classification_reason='documented support roles and whole-interval signed moment behaviour')
        start=max(dec(a['x_start_common']),dec(b['x_start_common']));end=min(dec(a['x_end_common']),dec(b['x_end_common']))
        length=max(dec(0),(end-start)*100)
        out['physical_overlap']={'start_m':float(start),'end_m':float(end),'length_cm':float(length),
            'provenance':{'bar_a':deepcopy(a['source']),'bar_b':deepcopy(b['source']),'operation':'physical interval intersection'}}
        if relation=='INDEPENDENT_REINFORCEMENTS':
            out['economic_comparison']={'applicable':False,'maximum_gap_cm':80,'reason':'required gap exceeds 80 cm'}
            for key in ('overlap_length_check','overlap_flexural_capacity'):out[key]=control(status='NOT_APPLICABLE')
            return out
        smallest=min(a['diameter_mm'],b['diameter_mm']);choices=[x for x in (a,b) if x['diameter_mm']==smallest]
        out['smallest_diameter_candidates']=[x['mark'] for x in choices];required=30.0
        if relation=='REINFORCEMENT_LAP_TRANSITION':
            anchor=basic_anchorage(smallest,context,api,flexure_sign='NEGATIVE');out['lap_anchorage']=anchor
            required=2*anchor['result']['lb_cm']
        out['overlap_length_check']=control(length>=dec(required),provided_cm=float(length),required_cm=required,
            margin_cm=float(length-dec(required)),rule=RULES['lap'] if relation=='REINFORCEMENT_LAP_TRANSITION' else RULES['overlap'])
        if relation=='DETAILING_OVERLAP':
            out['economic_comparison']=compare_detailing_mass(a,b,api,required_geometry=required_geometry,
                physical_overlap_cm=float(length),hanger=hanger,diagram=diagram,stirrups=stirrups,density=density)
        if len(choices)!=1:out['overlap_flexural_capacity']=control(reason='equal_diameter_groups_no_capacity_tiebreak')
        elif length<=0:out['overlap_flexural_capacity']=control(status='NOT_APPLICABLE',reason='no physical overlap')
        else:
            chosen=choices[0];out['smallest_diameter_bar']=chosen['mark']
            demand=interval_demand(diagram,float(start),float(end));out['overlap_demand']=demand
            try:
                physical=prepare_reinforcement([chosen],context,api,flexure_sign='NEGATIVE')
                capacity=composition_capacity(physical,float((start+end)/2),context,api,flexure_sign='NEGATIVE')
                if not capacity['valid'] or capacity['Mk_equivalent_knm'] is None:raise ValueError('isolated_capacity_invalid')
                out['isolated_capacity']=capacity
                if demand['passes'] is not True:raise ValueError('entire_overlap_domain_unresolved')
                out['overlap_flexural_capacity']=control(capacity['Mk_equivalent_knm']>=demand['max_negative_demand_knm'],
                    reference_bar=chosen['mark'],number_of_bars=chosen['bars'],diameter_mm=chosen['diameter_mm'],
                    MRd_knm=capacity['MRd_knm'],Mk_equivalent_knm=capacity['Mk_equivalent_knm'],
                    d_cm=capacity['concretopy']['d_equivalente_cm'],max_negative_demand_knm=demand['max_negative_demand_knm'],
                    governing=demand['governing'],rule=RULES['capacity'],provenance=capacity['provenance'])
            except (ValueError,KeyError,TypeError) as e:out['overlap_flexural_capacity']=control(reason=str(e))
        disposition=local_overlap_disposition(context['section'],[a,b],relation_type=relation,layout=layout,direct_pairs=direct_pairs)
        out.update(local_spacing_geometry=disposition['local_spacing_geometry'],vibrator_access_spacing=disposition['vibrator_access_spacing'],transverse_audit=disposition)
    except (ValueError,KeyError,TypeError) as e:out['diagnostics'].append(str(e))
    return out
