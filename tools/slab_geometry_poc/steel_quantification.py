"""Stage 11: nominal steel rates, not effective/resistant steel or flexure."""
import copy
import importlib
import hashlib
import math
import sys
from pathlib import Path
from collections import Counter


def load_concretopy(root):
    """Reuse the existing public bar model; no flexure calculation is invoked."""
    root=Path(root).resolve()
    sys.path.insert(0,str(root))
    before_bytecode=sys.dont_write_bytecode
    try:
        sys.dont_write_bytecode=True
        api=importlib.import_module('concretopy')
    finally:sys.dont_write_bytecode=before_bytecode
    if not Path(api.__file__).resolve().is_relative_to(root):raise ValueError('CONCRETOPY_ROOT_MISMATCH')
    files=['concretopy/armaduras.py','concretopy/unidades.py','concretopy/verificacoes/flexao.py',
        'concretopy/detalhamento/arranjos.py','concretopy/secoes.py','pyproject.toml']
    audit={'root':str(root),'bar_area_function':'concretopy.Barra.area_cm2',
        'source_sha256':{f:hashlib.sha256((root/f).read_bytes()).hexdigest() for f in files},
        'flexure_executed':False,'concretopy_modified':False,
        'same_layer_mixed_diameters_current_interface':'NOT_DIRECTLY_SUPPORTED_BY_VERTICAL_LAYER_VERIFIER',
        'integer_count_interface':'CamadaArmaduraLongitudinal.numero_barras requires integer; 100/s is a density, not a finite strip bar count',
        'future_adapter_required':True}
    return lambda diameter:api.Barra(diameter).area_cm2,audit


def positive_number(value):
    return not isinstance(value,bool) and isinstance(value,(int,float)) and math.isfinite(value) and value>0


def steel_rate(diameter_mm,spacing_cm,bar_area):
    """Bar area is delegated to Concretopy; scaling by 100/s keeps full precision."""
    if not positive_number(diameter_mm):raise ValueError('INVALID_DIAMETER_MM')
    if not positive_number(spacing_cm):raise ValueError('INVALID_SPACING_CM')
    area=bar_area(diameter_mm)
    if not positive_number(area):raise ValueError('INVALID_BACKEND_BAR_AREA')
    return area*(100.0/spacing_cm)


def validate_profile(inventory,profile,texts):
    if profile['source_pdf_sha256']!=inventory['stage5_provenance']['sha256']:raise ValueError('PROFILE_SOURCE_MISMATCH')
    if profile['same_layer_rule']['validation']!='USER_EXPLICIT_CONFIRMATION':raise ValueError('SAME_LAYER_RULE_NOT_CONFIRMED')
    rule=profile['same_layer_rule']
    if rule.get('base_reinforcement_interleaved') is not True or type(rule.get('extra_stacked_layers_for_reinforcement')) is not int or rule['extra_stacked_layers_for_reinforcement']!=0:
        raise ValueError('INCONSISTENT_INTERLEAVED_LAYER_RULE')
    cover=profile.get('cover_evidence')
    if not cover:return
    lookup={t['id']:t for t in texts}
    for evidence in cover['texts']:
        if evidence['text']!=lookup[evidence['id']]['text']:raise ValueError('COVER_TEXT_SOURCE_CHANGED')
    value=lookup[cover['value_text_id']]['text'].strip().replace(',','.')
    if float(value)!=cover['value_cm'] or not positive_number(cover['value_cm']):raise ValueError('INVALID_DOCUMENTARY_COVER')
    if 'COBRIMENTO' not in lookup[cover['heading_text_id']]['text'].upper():raise ValueError('COVER_HEADING_NOT_FOUND')
    if 'POSITIVA' not in lookup[cover['positive_label_text_id']]['text'].upper():raise ValueError('POSITIVE_COVER_LABEL_NOT_FOUND')
    if 'MEDIDAS EM CENT' not in lookup[cover['units_text_id']]['text'].upper():raise ValueError('COVER_UNIT_NOT_DOCUMENTED')


def thickness_cases(association):
    """Thickness attribution is independent of complete contour reconstruction."""
    cases={}
    for a in association['slab_associations']:
        key=(a['domain_id'],a['slab'],a['thickness_cm'])
        reliable=association['state']=='RELIABLE' and a['state']=='RELIABLE' and positive_number(a['thickness_cm'])
        if key not in cases:
            cases[key]={'slab':a['slab'],'domain_id':a['domain_id'],
                'documentary_thickness_cm':a['thickness_cm'],
                'thickness_cm':a['thickness_cm'] if reliable else None,
                'association_confidence':association['state'],'usable_for_depth_preparation':reliable,
                'documentary_sources':copy.deepcopy(a['documentary_sources']),
                'spatial_context_geometry_references':[],'context_is_not_validated_structural_domain':True}
        cases[key]['spatial_context_geometry_references']=[{'branch_id':p['branch_id'],'geometry_pdf_pt':copy.deepcopy(p['geometry_pdf_pt'])}
            for p in association['spatial_context_partition'] if a['domain_id'] in p['domain_ids']]
    return [cases[k] for k in sorted(cases,key=str)]


def quantify_composition(cell,lookup,rule):
    """Authorize only nominal sums under the new scoped same-layer instruction."""
    ids=cell['region_ids'];members=[lookup[i] for i in ids];classification=cell['classification']
    reasons=[];kind='PENDING_COMPOSITION';total=None;addition=False
    if len(ids)!=len(set(ids)):reasons.append('DUPLICATE_REGION_REFERENCES')
    identities=[m['graphic_identity_group'] for m in members if m['graphic_identity_group'] is not None]
    if len(identities)!=len(set(identities)):reasons.append('GRAPHIC_IDENTITIES_NOT_INDEPENDENT')
    if any(not m.get('nominal_composition_eligible',m['source_area_composition_eligible']) or m['as_cm2_per_m'] is None for m in members):reasons.append('MEMBER_ASSOCIATION_GEOMETRY_OR_RATE_PENDING')
    if len({m['orientation'] for m in members})!=1:reasons.append('DIFFERENT_BAR_DIRECTIONS')
    if any(m['orientation'] is None for m in members):reasons.append('BAR_DIRECTION_UNKNOWN')
    known_layers={m.get('source_layer') for m in members if m.get('source_layer') is not None}
    if len(known_layers)>1:reasons.append('CONFLICTING_DOCUMENTED_PHYSICAL_LAYERS')
    if any(m['reinforcement_type']=='LAP_SPLICE' for m in members) or cell['documentary_lap_region_ids'] or classification=='LAP_SPLICE':
        reasons.append('LAP_SPLICE_DOES_NOT_AUTHORIZE_ADDITION');kind='NON_ADDITIVE_LAP'
    if classification=='UNRESOLVED_COMPOSITION':reasons.append('SOURCE_COMPOSITION_UNRESOLVED')
    if not reasons and classification=='SINGLE_REINFORCEMENT' and len(members)==1:
        total=members[0]['as_cm2_per_m'];kind='INDIVIDUAL_NOMINAL_AREA'
    elif not reasons and classification in ('BASE_PLUS_REINFORCEMENT','MULTIPLE_REINFORCEMENTS'):
        whole=[s for s in cell['supported_joint_sets'] if set(s['members'])==set(ids) and s['classification']==classification]
        if not cell['joint_function_supported'] or not whole:reasons.append('COMPLETE_JOINT_FUNCTION_NOT_SUPPORTED')
        if not all(m['same_layer_rule_applicable'] for m in members):reasons.append('SAME_PHYSICAL_LAYER_NOT_CONFIRMED_FOR_THIS_FLOW')
        if not reasons:
            total=math.fsum(m['as_cm2_per_m'] for m in members);addition=True;kind='CONFIRMED_JOINT_NOMINAL_AREA'
    elif not reasons:reasons.append('SOURCE_CLASSIFICATION_NOT_ELIGIBLE_FOR_NOMINAL_TOTAL')
    return {'id':cell['id'],'source_composition_id':cell['source_composition_id'],
        'source_classification':classification,'geometry_pdf_pt':copy.deepcopy(cell['geometry_pdf_pt']),
        'direction_layer_key_original':cell['direction_layer_key'],'region_ids':ids,'positions':cell['positions'],
        'slabs':cell['slabs'],'thickness_options_cm':cell['thickness_options_cm'],
        'individual_areas':[{'region_id':m['region_id'],'occurrence_id':m['occurrence_id'],'display_id':m['display_id'],
            'position':m['position'],'diameter_mm':m['diameter_mm'],'spacing_cm':m['spacing_cm'],'as_cm2_per_m':m['as_cm2_per_m'],
            'physical_layer_id':rule['id'] if m['same_layer_rule_applicable'] else None,
            'center_from_tension_face_cm':None} for m in members],
        'nominal_total_cm2_per_m':total,'nominal_addition_authorized':addition,'quantification_kind':kind,
        'blocking_reasons':reasons,'same_layer_rule_source':copy.deepcopy(rule) if addition else None,
        'source_joint_evidence':copy.deepcopy(cell['supported_joint_sets']),
        'source_physical_addition_authorized':cell['physical_addition_authorized'],
        'extra_stacked_layers_assumed_for_reinforcement':0 if addition else None,
        'diameter_specific_centers_required':True,'effective_depth_cm':None,
        'resistant_area_or_capacity_validated':False}


def quantify(inventory,profile,texts,bar_area):
    validate_profile(inventory,profile,texts)
    stage10=inventory['acting_composition_analysis'];rule=profile['same_layer_rule']
    associations={o['occurrence_id']:o for o in inventory['documentary_spatial_assignment']['occurrences']}
    raw={o['occurrence_id']:o for o in inventory['occurrences']}
    groups={g['id']:g for g in inventory['localized_reconstruction']['physical_groups']}
    cells=stage10['compositions'];result=[]
    for r in sorted(stage10['acting_regions'],key=lambda r:r['display_id']):
        call=r['original_call'];diameter=call.get('diameter_mm');spacing=call.get('spacing_cm')
        errors=[];rate=None;area=None
        if positive_number(diameter):area=bar_area(diameter)
        else:errors.append('DIAMETER_MISSING_OR_INVALID')
        if spacing is None:errors.append('SPACING_NOT_INDICATED; TOTAL_BAR_QUANTITY_IS_NOT_SPACING')
        elif not positive_number(spacing):errors.append('SPACING_INVALID')
        if not errors:rate=steel_rate(diameter,spacing,bar_area)
        a=associations[r['occurrence_id']];cases=thickness_cases(a)
        reliable_h=sorted({c['thickness_cm'] for c in cases if c['usable_for_depth_preparation'] and c['thickness_cm'] is not None})
        applicable=(r['kind']=='DISTRIBUTED_AREA' and r.get('sheet_reinforcement_context')==rule['sheet_context'] and r['orientation']==rule['orientation'])
        cover=profile.get('cover_evidence') if applicable else None
        missing=['DIAMETER_SPECIFIC_CENTER_REFERENCE_AND_ORTHOGONAL_BAR_ORDER']
        if not cover:missing.append('APPLICABLE_DOCUMENTARY_COVER')
        if not reliable_h:missing.append('RELIABLE_SLAB_THICKNESS')
        if not applicable:missing.append('APPLICABLE_PHYSICAL_LAYER_POSITION')
        if r['kind']!='DISTRIBUTED_AREA':missing.append('PROVED_DISTRIBUTED_ACTUATION_GEOMETRY')
        if not positive_number(diameter):missing.append('BAR_DIAMETER')
        role=r['documentary_role'] if r['documentary_role'] in ('BASE','REINFORCEMENT','LAP_SPLICE') else 'PENDING_CLASSIFICATION'
        entry={'region_id':r['id'],'occurrence_id':r['occurrence_id'],'display_id':r['display_id'],'position':r['position'],
            'source_kind':r['kind'],'diameter_mm':diameter,'spacing_cm':spacing,'bar_area_cm2':area,'as_cm2_per_m':rate,
            'rate_state':'DOCUMENTARY_RATE_CALCULATED' if rate is not None else 'PENDING_SPACING_OR_DIAMETER',
            'rate_issues':errors,'rate_calculation_uses_total_bar_quantity':False,
            'original_call':copy.deepcopy(call),'documentary_sources':{'text_ids':raw[r['occurrence_id']]['text_ids'],
                'human_role_confirmation':copy.deepcopy(r['human_role_confirmation']),'prior_role_candidate':copy.deepcopy(r['previous_role_candidate'])},
            'reinforcement_type':role,'geometry_pdf_pt':copy.deepcopy(r['geometry_pdf_pt']),
            'geometry_coordinate_unit':'PDF_PT_NOT_CM','orientation':r['orientation'],
            'source_layer':r.get('layer'),
            'source_area_composition_eligible':r['eligible_for_area_composition'],
            'nominal_composition_eligible':r['eligible_for_area_composition'] and r['association_confidence']=='RELIABLE' and a['state']=='RELIABLE' and not a['requires_geometry_review'],
            'graphic_identity_group':r.get('identity_group'),
            'composition_ids':[c['id'] for c in cells if r['id'] in c['region_ids']],
            'source_composition_ids':[c['source_composition_id'] for c in cells if r['id'] in c['region_ids']],
            'slabs':r['slabs'],'association_confidence':r['association_confidence'],'thickness_cases':cases,
            'documentary_thickness_options_cm':copy.deepcopy(r['thickness_options_cm']),
            'thickness_cm':reliable_h[0] if len(reliable_h)==1 else None,
            'different_reliable_thicknesses':len(reliable_h)>1,'same_layer_rule_applicable':applicable,
            'depth_preparation':{'nominal_cover_cm':cover['value_cm'] if cover else None,
                'cover_source':copy.deepcopy(cover),'physical_layer_id':rule['id'] if applicable else None,
                'layer_arrangement':'INTERLEAVED_POSITIVE_BARS_SAME_PHYSICAL_LAYER' if applicable else 'NOT_ESTABLISHED_BY_CURRENT_POSITIVE_FLOW_RULE',
                'layer_rule_origin':rule['source'] if applicable else None,
                'local_group_layer_evidence':[{'group_id':id,'distribution':copy.deepcopy(groups[id]['layer_distribution'])} for id in r.get('physical_group_ids',[])],
                'bar_radius_cm':diameter/20 if positive_number(diameter) else None,
                'center_from_tension_face_cm':None,'effective_depth_cm':None,
                'same_layer_does_not_imply_equal_centers':True,
                'missing_parameters':missing,
                'cases_by_thickness':[{'slabs':sorted({c['slab'] for c in cases if c['thickness_cm']==h}),
                    'h_cm':h,'cover_cm':cover['value_cm'] if cover else None,'d_cm':None,'center_from_tension_face_cm':None}
                    for h in reliable_h]},
            'concretopy_preparation':{'schema':'POSITIVE_SLAB_RATE_GROUP_NOT_A_DIRECT_CAMADA_INPUT',
                'reference_width_cm':100.0,'diametro_mm':diameter,'espacamento_cm':spacing,
                'as_cm2_for_reference_width':rate,'bar_density_per_meter':100/spacing if positive_number(spacing) else None,
                'numero_barras_for_api':None,'cobrimento_cm':cover['value_cm'] if cover else None,
                'physical_layer_id':rule['id'] if applicable else None,
                'd_cm':None,'fck_mpa':None,'fyk_mpa':None,'direct_flexure_api_ready':False},
            'structural_sufficiency_conclusion':None}
        result.append(entry)
    lookup={o['region_id']:o for o in result}
    compositions=[quantify_composition(c,lookup,rule) for c in cells]
    return {'occurrences':result,'compositions':compositions,'same_layer_rule':copy.deepcopy(rule),
        'cover_evidence':copy.deepcopy(profile.get('cover_evidence')),
        'units':{'rate':'cm2/m','bar_area':'cm2','diameter':'mm','spacing':'cm','section_geometry':'cm',
            'drawing_geometry':'PDF_PT_UNCONVERTED','stress_preparation':'MPa','force_preparation':'kN','moment_preparation':'kN.cm'},
        'metrics':{'occurrences':len(result),'individual_rates_calculated':sum(o['as_cm2_per_m'] is not None for o in result),
            'rates_pending':sum(o['as_cm2_per_m'] is None for o in result),'composition_records':len(compositions),
            'composition_quantification':dict(Counter(c['quantification_kind'] for c in compositions)),
            'nominal_joint_totals_authorized':sum(c['nominal_addition_authorized'] for c in compositions),
            'effective_depth_calculated':0,'flexural_resistance_calculated':0},
        'formula':'Concretopy.Barra(phi_mm).area_cm2 * (100 / spacing_cm); no internal rounding',
        'prior_geometries_or_classifications_modified':False,'structural_validation_performed':False}
