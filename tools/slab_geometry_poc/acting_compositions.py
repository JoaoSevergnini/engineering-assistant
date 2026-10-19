"""Stage 10: presence, documentary joint function and resistance remain distinct.

Reuses source regions/cells. No slab clipping, trace envelopes, steel summation,
role rules by documentary mark, or propagation beyond confirmed relation scope.
"""
import copy
import hashlib
import json
from collections import Counter
from polygonal_slabs import Polygon,Point,shape,geo,polygons,unary_union
from slab_assignment import apply_confirmations
from structural_regions import fingerprint


def stable_id(prefix,payload):
    return prefix+hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':')).encode()).hexdigest()[:14]


def role_relations(regions,confirmations):
    """Confirmed base/reinforcement functions support a geometric pair, no sums."""
    lookup={r['id']:r for r in regions};roles={c['region_id']:c for c in confirmations};result=[]
    for rid,reinf in sorted(roles.items()):
        if reinf['classification']!='REINFORCEMENT':continue
        for bid,base in sorted(roles.items()):
            if base['classification']!='BASE':continue
            a,b=lookup[rid],lookup[bid]
            if a['orientation']!=b['orientation']:continue
            if a.get('layer') is not None and b.get('layer') is not None and a['layer']!=b['layer']:continue
            if a.get('identity_group') and a.get('identity_group')==b.get('identity_group'):continue
            g=Polygon(a['polygon_pdf_pt']).intersection(Polygon(b['polygon_pdf_pt']))
            if g.area<=0:continue
            result.append({'id':stable_id('JF-',[rid,bid,geo(g)]),'members':sorted([rid,bid]),
                'reinforcement':rid,'base':bid,'geometry_pdf_pt':geo(g),'classification':'BASE_PLUS_REINFORCEMENT',
                'validation_state':'DOCUMENTARY_FUNCTION_AND_VECTOR_OVERLAP_SUPPORTED',
                'origin':'ENGINEER_CONFIRMED_ROLES_PLUS_VECTOR_GEOMETRY',
                'role_confirmations':[copy.deepcopy(base),copy.deepcopy(reinf)],
                'physical_addition_authorized':False,'exact_layer_confirmed':a.get('layer') is not None and b.get('layer') is not None})
    return sorted(result,key=lambda r:r['id'])


def classify_presence(members,joint_sets=(),manual=None):
    """Members belong to one direction/layer only; identities are not marks."""
    present={m['id'] for m in members};reasons=[]
    pending=[m['id'] for m in members if not m['eligible_for_area_composition']]
    laps=[m['id'] for m in members if m['documentary_role']=='LAP_SPLICE']
    supporting=[copy.deepcopy(s) for s in joint_sets if set(s['members'])<=present]
    if pending:classification='UNRESOLVED_COMPOSITION';reasons.append('ASSOCIATION_OR_ACTUATION_GEOMETRY_PENDING')
    elif manual and manual['classification']=='GRAPHICAL_RESIDUAL':
        classification='UNRESOLVED_COMPOSITION';reasons.append('ENGINEER_CONFIRMED_GRAPHICAL_RESIDUAL_NOT_ADDITIVE')
    elif manual and laps and manual['classification'] in ('BASE_PLUS_REINFORCEMENT','MULTIPLE_REINFORCEMENTS'):
        classification='UNRESOLVED_COMPOSITION';reasons.append('CONFLICT_BETWEEN_PRESERVED_HUMAN_JOINT_FUNCTION_AND_LAP_ROLE')
    elif manual and manual['classification'] in ('BASE_PLUS_REINFORCEMENT','MULTIPLE_REINFORCEMENTS','LAP_SPLICE'):
        classification=manual['classification'];reasons.append('PRESERVED_ENGINEER_CONFIRMATION_EXACT_CELL')
    elif laps:
        classification='UNRESOLVED_COMPOSITION';reasons.append('DOCUMENTARY_LAP_PRESENT; PARTNER_AND_EXACT_LAP_ZONE_UNCONFIRMED')
    elif len(members)==1:
        classification='SINGLE_REINFORCEMENT';reasons.append('ONE_SUPPORTED_GRAPHIC_OCCURRENCE_IN_DIRECTION_LAYER')
    else:
        full=[s for s in supporting if set(s['members'])==present]
        if full:
            meanings={s['classification'] for s in full}
            if len(meanings)==1:classification=next(iter(meanings));reasons.append('JOINT_DOCUMENTARY_FUNCTION_SUPPORTED_OVER_EXACT_VALIDITY_DOMAIN')
            else:classification='UNRESOLVED_COMPOSITION';reasons.append('CONFLICTING_SUPPORTED_FUNCTIONS')
        else:classification='UNRESOLVED_COMPOSITION';reasons.append('GRAPHIC_OVERLAP_WITH_UNCONFIRMED_FULL_PHYSICAL_COMPOSITION')
    # Unknown layers, duplicate identities and structural checks are never bypassed.
    return {'classification':classification,'reasons':reasons,'supported_joint_sets':supporting,
        'interpretation_origin':'PREVIOUS_ENGINEER_LOCAL_CLASSIFICATION' if manual else
            'CONFIRMED_ROLES_AND_VECTOR_RELATION' if supporting else 'GRAPHIC_PRESENCE_OR_PENDING_PHYSICAL_MEANING',
        'joint_function_supported':classification in ('BASE_PLUS_REINFORCEMENT','MULTIPLE_REINFORCEMENTS'),
        'documentary_lap_region_ids':laps,'independent_addition_blocked':True,
        'physical_addition_authorized':False,'effective_resistant_contributors':None,
        'documentarily_supported_region_ids':sorted(present) if classification in ('SINGLE_REINFORCEMENT','BASE_PLUS_REINFORCEMENT','MULTIPLE_REINFORCEMENTS') else [],
        'exact_layer_state':'KNOWN' if all(m.get('layer') is not None for m in members) else 'EXACT_LAYER_UNKNOWN; SHEET_CONTEXT_RETAINED',
        'manual_classification_preserved':copy.deepcopy(manual)}


def consolidate(compositions):
    """Only connected polygons with identical occurrence-level interpretation merge."""
    buckets={}
    for c in compositions:
        key=(tuple(c['region_ids']),c['classification'],tuple(c['direction_layer_key']),
            tuple(s['id'] for s in c['supported_joint_sets']),
            json.dumps(c['manual_classification_preserved'],sort_keys=True),tuple(c['slabs']))
        buckets.setdefault(key,[]).append(c)
    result=[]
    for key,cells in sorted(buckets.items(),key=lambda p:str(p[0])):
        union=unary_union([shape(c['geometry_pdf_pt']) for c in cells])
        for g in polygons(union):
            active=[c for c in cells if shape(c['geometry_pdf_pt']).intersection(g).area>0]
            ids=sorted(c['id'] for c in active)
            result.append({'id':stable_id('BLOCK-',ids),'geometry_pdf_pt':geo(g),'area_pt2':g.area,
                'composition_ids':ids,'original_cell_ids':sorted({c['source_composition_id'] for c in active}),
                'region_ids':list(key[0]),'classification':key[1],'direction_layer_key':list(key[2]),
                'slabs':list(key[-1]),'physical_addition_authorized':False})
    return sorted(result,key=lambda r:r['id'])


def analyze(inventory,profile):
    previous=inventory['documentary_spatial_assignment'];spatial=inventory['distributed_spatial_analysis']
    regions=spatial['regions'];lookup={r['occurrence_id']:r for r in regions}
    confirmations=apply_confirmations(regions,profile,inventory['stage5_provenance']['sha256'])
    confirmations+=apply_confirmations(regions,{'source_pdf_sha256':inventory['stage5_provenance']['sha256'],
        'records':previous['human_confirmations']},inventory['stage5_provenance']['sha256'])
    roles={}
    for r in confirmations:
        if r['region_id'] in roles and roles[r['region_id']]['classification']!=r['classification']:
            raise ValueError('CONFLICTING_HUMAN_ROLE_CONFIRMATIONS')
        roles[r['region_id']]=r
    pending_roles={r['region_id']:r for r in inventory['structural_interpretation']['function_candidates']}
    entries=[];area_entries={}
    for o in sorted(previous['occurrences'],key=lambda o:o['occurrence_id']):
        r=lookup.get(o['occurrence_id'])
        entry={'id':r['id'] if r else stable_id('TRACE-' if o['geometry_sources'] else 'PENDING-',o['occurrence_id']),
            'occurrence_id':o['occurrence_id'],'display_id':o['display_id'],'position':o['documentary_mark'],
            'slabs':o['slabs'],'thickness_options_cm':o['thickness_options_cm'],
            'association_confidence':o['state'],'actuation_geometry_quality':o['actuation_geometry_quality'],
            'quantity_reference':o['occurrence_id'],'quantities_allocated':False,
            'original_call':copy.deepcopy(o['call']),'geometry_pdf_pt':None,'orientation':None,'layer':None,
            'eligible_for_area_composition':False,'geometry_confirmed_by_engineer':False,
            'physical_addition_authorized':False,'requires_previous_decision':o['requires_engineer_decision'],
            'documentary_role':roles[r['id']]['classification'] if r and r['id'] in roles else 'UNKNOWN',
            'human_role_confirmation':copy.deepcopy(roles.get(r['id'])) if r else None,
            'previous_role_candidate':copy.deepcopy(pending_roles.get(r['id'])) if r else None,
            'original_geometry_sources':copy.deepcopy(o['geometry_sources'])}
        if r:
            g=Polygon(r['polygon_pdf_pt'])
            valid=g.is_valid and not g.is_empty and g.area>0
            entry.update(kind='DISTRIBUTED_AREA',geometry_pdf_pt=geo(g),source_region_id=r['id'],
                original_polygon_pdf_pt=copy.deepcopy(r['polygon_pdf_pt']),orientation=r['orientation'],layer=r.get('layer'),
                source_bar=copy.deepcopy(r['bar']),source_distribution_axis=copy.deepcopy(r['distribution_axis']),
                longitudinal_extent_pt=r['longitudinal_extent_pt'],transverse_extent_pt=r['transverse_extent_pt'],
                geometry_origin='INFERRED_GRAPHIC_ENVELOPE_OF_EXTRACTED_BAR_AND_DISTRIBUTION_AXIS',
                documentary_source=copy.deepcopy(r['source']),identity_group=r['identity_group'],
                sheet_reinforcement_context=r['reinforcement_role'],
                eligible_for_area_composition=valid and o['state']=='RELIABLE' and not o['requires_geometry_review'],
                slab_contours_used_for_clipping=False)
            area_entries[r['id']]=entry
        elif o['geometry_sources']:
            g=unary_union([shape(s['geometry_pdf_pt']) for s in o['geometry_sources']])
            entry.update(kind='LOCALIZED_TRACES_ONLY',geometry_pdf_pt=geo(g),
                geometry_origin='EXTRACTED_ASSOCIATED_GROUP_TRACES; NO_AREA_ENVELOPE',
                physical_group_ids=sorted(s['physical_group_id'] for s in o['geometry_sources']))
        else:
            entry.update(kind='PENDING_GEOMETRY',geometry_origin='UNRESOLVED_HYPOTHESES_NOT_PROMOTED',
                hypotheses=copy.deepcopy(o['context_branch_sources']),pending_reasons=copy.deepcopy(o['pending_reasons']))
        entries.append(entry)
    relations=role_relations(regions,confirmations)
    manual={i['composition_id']:i for i in inventory['structural_interpretation']['overlap_interpretations'] if i['validation_state']=='ENGINEER_CONFIRMED'}
    compositions=[]
    for cell in sorted(spatial['composition_regions'],key=lambda c:c['id']):
        g=Polygon(cell['polygon_pdf_pt']);groups={}
        for id in cell['region_ids']:
            r=area_entries[id];groups.setdefault((r['orientation'],r['layer']),[]).append(r)
        review=manual.get(cell['id'])
        if review and (fingerprint(cell)!=review['fingerprint'] or review['human_confirmation']['source_sha256']!=inventory['stage5_provenance']['sha256']):
            raise ValueError('STALE_HUMAN_CELL_CONFIRMATION')
        for direction,members in sorted(groups.items(),key=lambda pair:str(pair[0])):
            ids=sorted(r['id'] for r in members)
            applicable=[rel for rel in relations if set(rel['members'])<=set(ids) and g.difference(shape(rel['geometry_pdf_pt'])).area<=1e-8]
            local=copy.deepcopy(review) if review and len(groups)==1 else None
            if local and local['classification'] in ('BASE_PLUS_REINFORCEMENT','LAP_SPLICE'):
                applicable.append({'id':stable_id('LOCAL-',review['fingerprint']),'members':ids,
                    'classification':local['classification'],'origin':'EXACT_PREVIOUS_HUMAN_CELL_CONFIRMATION'})
            classification=classify_presence(members,applicable,local)
            compositions.append(dict(classification,id=stable_id('ACT-CELL-',[cell['id'],ids,geo(g)]),
                source_composition_id=cell['id'],geometry_pdf_pt=geo(g),original_polygon_pdf_pt=copy.deepcopy(cell['polygon_pdf_pt']),
                area_pt2=g.area,region_ids=ids,occurrences=sorted(r['display_id'] for r in members),
                positions=sorted({r['position'] for r in members}),
                slabs=sorted({s for r in members for s in r['slabs']}),
                thickness_options_cm=sorted({h for r in members for h in r['thickness_options_cm']}),
                direction_layer_key=list(direction),other_direction_region_ids=sorted(set(cell['region_ids'])-set(ids)),
                source_geometry_unchanged=True,
                cross_direction_human_review_not_propagated=copy.deepcopy(review) if review and len(groups)>1 else None,
                resistance_quantities_computed=False))
    blocks=consolidate(compositions)
    n14_comparison=[]
    for relation in relations:
        bid,rid=relation['base'],relation['reinforcement']
        isolated=[c for c in compositions if c['region_ids']==[bid] and c['classification']=='SINGLE_REINFORCEMENT']
        overlaps=[c for c in compositions if {bid,rid}<=set(c['region_ids'])]
        n14_comparison.append({'relation_id':relation['id'],'reinforcement_region_id':relation['reinforcement'],
            'base_region_id':relation['base'],'overlap_geometry_pdf_pt':relation['geometry_pdf_pt'],
            'overlap_area_pt2':shape(relation['geometry_pdf_pt']).area,
            'base_outside_reinforcement_geometry_pdf_pt':geo(shape(area_entries[relation['base']]['geometry_pdf_pt']).difference(shape(area_entries[relation['reinforcement']]['geometry_pdf_pt']))),
            'reinforcement_outside_this_base_geometry_pdf_pt':geo(shape(area_entries[rid]['geometry_pdf_pt']).difference(shape(area_entries[bid]['geometry_pdf_pt']))),
            'isolated_base_composition_ids':[c['id'] for c in isolated],
            'isolated_base_area_pt2':sum(c['area_pt2'] for c in isolated),
            'overlap_composition_ids':[c['id'] for c in overlaps],
            'overlap_with_other_unresolved_members':[c['id'] for c in overlaps if c['classification']=='UNRESOLVED_COMPOSITION'],
            'not_proof_of_other_contributions_being_absent':True})
    return {'acting_regions':entries,'compositions':compositions,'consolidated_blocks':blocks,
        'documentary_joint_relations':relations,'role_confirmations':confirmations,'base_reinforcement_comparison':n14_comparison,
        'previous_pending_occurrences':[o['display_id'] for o in previous['occurrences'] if o['requires_engineer_decision']],
        'metrics':{'occurrences':len(entries),'area_regions':len(area_entries),
            'eligible_area_regions':sum(r['eligible_for_area_composition'] for r in entries),
            'localized_trace_only':sum(r['kind']=='LOCALIZED_TRACES_ONLY' for r in entries),
            'pending_geometry':sum(r['kind']=='PENDING_GEOMETRY' for r in entries),
            'composition_records':len(compositions),'original_geometric_cells':len(spatial['composition_regions']),
            'classifications':{name:sum(c['classification']==name for c in compositions) for name in
                ['SINGLE_REINFORCEMENT','BASE_PLUS_REINFORCEMENT','MULTIPLE_REINFORCEMENTS','LAP_SPLICE','UNRESOLVED_COMPOSITION']},
            'documentary_lap_pending_cells':sum(bool(c['documentary_lap_region_ids']) for c in compositions),
            'consolidated_blocks':len(blocks)},
        'interpretation_policy':'PRESENCE_AND_DOCUMENTARY_JOINT_FUNCTION_ONLY; NO_STEEL_SUMS; NO_SLAB_CLIPPING; NO_TRACE_ENVELOPES',
        'structural_validation_performed':False}


def query(result,x,y):
    point=Point(x,y)
    return {'pdf_point':[x,y],
        'compositions':[c for c in result['compositions'] if shape(c['geometry_pdf_pt']).covers(point)],
        'localized_trace_hits':[r for r in result['acting_regions'] if r['kind']=='LOCALIZED_TRACES_ONLY' and shape(r['geometry_pdf_pt']).covers(point)],
        'boundary_policy':'ALL_COVERING_REGIONS_RETURNED; NO_NEAREST_REGION_SELECTION'}
