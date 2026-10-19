"""Stage 7 occurrence hyperedges with explicit spatial scope; no transitive closure."""
import copy
import hashlib
import itertools
import json
from collections import Counter
from polygonal_slabs import Polygon,shape,geo,unary_union,reconstruct_slabs
from structural_regions import coverage,adjacent


def relation(kind,members,domain,evidence,state='AUTOMATIC_CANDIDATE',reinforcement=None,bases=(),meaning=None):
    if kind=='SAME_PHYSICAL_REPRESENTATION' and state=='ENGINEER_CONFIRMED_LOCAL_SCOPE' and not (evidence.get('human_confirmation') or evidence.get('physical_identity_evidence')):
        raise ValueError('Specific physical identity evidence is required')
    payload={'type':kind,'members':sorted(members),'validity_geometry_pdf_pt':geo(domain),
        'reinforcement':reinforcement,'bases':sorted(bases),'state':state,'structural_meaning':meaning,'evidence':evidence}
    def no_colors(value):
        if isinstance(value,dict):return {k:no_colors(v) for k,v in value.items() if k not in ('color','fill')}
        if isinstance(value,list):return [no_colors(v) for v in value]
        return value
    payload['id']='Q-'+hashlib.sha256(json.dumps(no_colors(payload),sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()[:12]
    payload['physical_addition_authorized']=False;payload['transitive_inference_authorized']=False
    payload['shared_physical_identity_id']='F-'+payload['id'][2:] if kind=='SAME_PHYSICAL_REPRESENTATION' and state=='ENGINEER_CONFIRMED_LOCAL_SCOPE' else None
    return payload


def build_relations(inventory):
    spatial=inventory['distributed_spatial_analysis'];regions=spatial['regions'];lookup={r['id']:r for r in regions}
    stage6=inventory['structural_interpretation'];cells={c['id']:c for c in spatial['composition_regions']};functions={f['region_id']:f for f in stage6['function_candidates']};relations=[]
    for check in stage6['containment_checks']:
        r=lookup[check['reinforcement_id']];bases=[lookup[id] for id in check['base_region_ids']]
        domain=Polygon(r['polygon_pdf_pt']).intersection(unary_union([Polygon(b['polygon_pdf_pt']) for b in bases]))
        relations.append(relation('REINFORCES',[r['id']]+[b['id'] for b in bases],domain,
            {'origin':'STAGE6_FUNCTION_AND_COVERAGE_CANDIDATES','containment':copy.deepcopy(check),
             'function_evidence':[functions[id] for id in [r['id']]+check['base_region_ids']],
             'same_orientation':all(b['orientation']==r['orientation'] for b in bases),'layer_confirmed':False,
             'source_entities':{z['id']:{'bar':z['bar'],'axis':z['distribution_axis'],'call':z['source']} for z in [r]+bases}},
             reinforcement=r['id'],bases=check['base_region_ids'],meaning='BASE_PLUS_REINFORCEMENT'))
    for a,b in itertools.combinations(sorted(regions,key=lambda r:r['id']),2):
        domain=Polygon(a['polygon_pdf_pt']).intersection(Polygon(b['polygon_pdf_pt']));same_mark=a['position']==b['position']
        if domain.area<=1e-8 and not same_mark:continue
        members=[a['id'],b['id']];related=[i for i in stage6['overlap_interpretations'] if set(members)<=set(cells[i['composition_id']]['region_ids'])]
        evidence={'same_documentary_mark':same_mark,'same_orientation':a['orientation']==b['orientation'],
            'same_graphic_identity_group':a['identity_group']==b['identity_group'],
            'diameters_mm':[a['diameter_mm'],b['diameter_mm']],'spacings_cm':[a['spacing_cm'],b['spacing_cm']],
            'nominal_lengths_cm':[a['nominal_length_cm'],b['nominal_length_cm']],
            'composition_ids':[i['composition_id'] for i in related],
            'geometric_evidence':[i['automatic']['evidence'] for i in related],
            'calls':[a['source'],b['source']],'physical_identity_proved':False}
        if domain.area>1e-8:
            relations.append(relation('GRAPHICAL_INTERSECTION',members,domain,evidence,state='OBSERVED_GEOMETRY_ONLY'))
            if any(members in i['automatic']['evidence'].get('longitudinal_end_overlap_pairs',[]) or list(reversed(members)) in i['automatic']['evidence'].get('longitudinal_end_overlap_pairs',[]) for i in related):
                relations.append(relation('LAPS_WITH',members,domain,evidence,meaning='LAP_SPLICE'))
            if a['identity_group']==b['identity_group']:
                relations.append(relation('SAME_PHYSICAL_REPRESENTATION',members,domain,
                    dict(evidence,specific_evidence='SAME_RAW_BAR_AXIS_AND_DOCUMENTARY_PROPERTIES; ENGINEER_CONFIRMATION_REQUIRED'),meaning='DEDUPLICATION_PENDING'))
        else:
            relations.append(relation('UNDETERMINED',members,domain,dict(evidence,reason='SAME_MARK_AT_DIFFERENT_LOCATIONS_IS_NOT_PHYSICAL_IDENTITY')))
    # Lift each human review only onto its actual members and exact confirmed domain.
    # A cell confirmation does not certify a global reinforcement hyperedge.
    types={'BASE_PLUS_REINFORCEMENT':'REINFORCES','LAP_SPLICE':'LAPS_WITH','GRAPHICAL_RESIDUAL':'GRAPHICAL_INTERSECTION'}
    for i in stage6['overlap_interpretations']:
        if i['validation_state']!='ENGINEER_CONFIRMED' or i['classification'] not in types:continue
        c=cells[i['composition_id']];members=c['region_ids'];reinforcements=[id for id in members if functions[id]['role_candidate']=='REINFORCEMENT']
        r=reinforcements[0] if i['classification']=='BASE_PLUS_REINFORCEMENT' and len(reinforcements)==1 else None
        bases=[id for id in members if id!=r] if r else []
        relations.append(relation(types[i['classification']],members,Polygon(c['polygon_pdf_pt']),
            {'origin':'PRESERVED_STAGE6_ENGINEER_CONFIRMATION','human_confirmation':i['human_confirmation'],
             'confirmed_composition_id':c['id'],'scope':'EXACT_CONFIRMED_POLYGON_ONLY',
             'direction_assignment':'GEOMETRIC_FUNCTION_CANDIDATE_NOT_GLOBAL_HUMAN_ROLE_CONFIRMATION' if r else 'NOT_ASSIGNED',
             'same_orientation':len({lookup[id]['orientation'] for id in members})==1},
            state='ENGINEER_CONFIRMED_LOCAL_SCOPE',reinforcement=r,bases=bases,meaning=i['classification']))
    for rel in relations:
        rel['graphic_occurrences']=[{'region_id':id,'occurrence_id':lookup[id]['occurrence_id'],'display_id':lookup[id]['display_id'],'position':lookup[id]['position'],'orientation':lookup[id]['orientation'],'layer':lookup[id]['layer']} for id in rel['members']]
        rel['physical_identity_state']='NOT_INFERRED_FROM_MARK_OR_PROPERTIES'
    return sorted(relations,key=lambda r:r['id'])


def propagate(cells,relations,stage6_interpretations,lookup):
    previous={i['composition_id']:i for i in stage6_interpretations};result=[]
    for c in cells:
        cell=Polygon(c['polygon_pdf_pt']);present=set(c['region_ids']);applicable=[];confirmed=[];conflicts=[]
        for rel in relations:
            active=present.intersection(rel['members'])
            if rel['type']=='REINFORCES' and rel['reinforcement']:
                member_match=rel['reinforcement'] in active and bool(active.intersection(rel['bases']))
            else:member_match=set(rel['members'])<=present
            if not member_match:continue
            if len({lookup[id]['orientation'] for id in active})>1 and rel['type'] in ('REINFORCES','LAPS_WITH'):
                if rel['state']=='ENGINEER_CONFIRMED_LOCAL_SCOPE':conflicts.append({'relation_id':rel['id'],'reason':'KNOWN_INCOMPATIBLE_ORIENTATIONS'})
                continue
            layers={lookup[id].get('layer') for id in active if lookup[id].get('layer') is not None}
            if len(layers)>1 and rel['type'] in ('REINFORCES','LAPS_WITH'):
                if rel['state']=='ENGINEER_CONFIRMED_LOCAL_SCOPE':conflicts.append({'relation_id':rel['id'],'reason':'KNOWN_INCOMPATIBLE_LAYERS'})
                continue
            g=cell.intersection(shape(rel['validity_geometry_pdf_pt']))
            if g.area<=1e-8:continue
            full=cell.difference(g).area<=1e-8
            applicable.append({'relation_id':rel['id'],'active_region_ids':sorted(active),'active_occurrences':[lookup[id]['occurrence_id'] for id in sorted(active)],
                'applicable_geometry_pdf_pt':geo(g),'area_pt2':g.area,'full_cell':full,'state':rel['state']})
            if full and rel['state']=='ENGINEER_CONFIRMED_LOCAL_SCOPE' and rel.get('structural_meaning'):confirmed.append(rel)
        meanings={r['structural_meaning'] for r in confirmed};old=previous[c['id']]
        old_human=old['classification'] if old['validation_state']=='ENGINEER_CONFIRMED' else None
        if old_human and meanings and old_human not in meanings:conflicts.append({'reason':'CONFLICT_WITH_PRESERVED_HUMAN_CLASSIFICATION','stage6':old_human})
        if len(meanings)>1:conflicts.append({'reason':'CONFLICTING_CONFIRMED_RELATIONS','alternatives':sorted(meanings)})
        if conflicts:classification='UNDETERMINED';state='CONFLICT_PENDING'
        elif len(meanings)==1:classification=next(iter(meanings));state='ENGINEER_CONFIRMED_WITHIN_VALID_DOMAIN'
        elif old_human:classification=old_human;state='PRESERVED_STAGE6_HUMAN_CLASSIFICATION'
        else:classification='SINGLE_DISTRIBUTED' if len(c['identity_groups'])==1 else 'UNDETERMINED';state='PENDING_REVIEW'
        result.append({'composition_id':c['id'],'polygon_pdf_pt':copy.deepcopy(c['polygon_pdf_pt']),'region_ids':c['region_ids'],
            'occurrences':c['occurrences'],'relations':applicable,'classification':classification,'validation_state':state,
            'stage6_classification':old['classification'],'conflicts':conflicts,'physical_addition_authorized':False,
            'newly_interpreted_by_propagation':classification!='UNDETERMINED' and old['classification']=='UNDETERMINED'})
    return result


def consolidate_relations(cells,interpretations,slabs,lookup):
    imap={i['composition_id']:i for i in interpretations};remaining={c['id']:c for c in cells};groups=[]
    def slab_ids(c):
        return sorted(s['name'] for s in slabs if s['selected_candidate_id'] and any(h['region_id']==c['id'] and h['candidate_id']==s['selected_candidate_id'] for h in s['composition_relations']))
    def key(c):
        i=imap[c['id']]
        return (tuple(c['identity_groups']),i['classification'],i['validation_state'],
            tuple((r['relation_id'],tuple(r['active_region_ids']),r['full_cell']) for r in i['relations']),
            tuple(slab_ids(c)),tuple(sorted({lookup[id]['orientation'] for id in c['region_ids']})))
    while remaining:
        c=remaining.pop(min(remaining));parts=[c];stack=[c]
        while stack:
            current=stack.pop()
            for id,z in list(remaining.items()):
                if key(c)==key(z) and adjacent(current['bbox'],z['bbox']):remaining.pop(id);parts.append(z);stack.append(z)
        groups.append({'id':f'V{len(groups)+1:03d}','geometry_pdf_pt':geo(unary_union([Polygon(p['polygon_pdf_pt']) for p in parts])),
            'composition_ids':sorted(p['id'] for p in parts),'region_ids':sorted({id for p in parts for id in p['region_ids']}),
            'occurrences':sorted({id for p in parts for id in p['occurrences']}),'identity_groups':c['identity_groups'],
            'relation_ids':sorted({r['relation_id'] for p in parts for r in imap[p['id']]['relations']}),
            'preliminary_slab_names':slab_ids(c),'confirmed_slab_names':[],
            'classification':imap[c['id']]['classification'],'validation_state':imap[c['id']]['validation_state'],
            'physical_addition_authorized':False,'area_pt2':sum(p['area_pt2'] for p in parts)})
    return groups


def analyze_relations(inventory,data,contours=None):
    result=copy.deepcopy(inventory);a=inventory['distributed_spatial_analysis'];lookup={r['id']:r for r in a['regions']}
    relations=build_relations(inventory);slab_result=contours if contours is not None else reconstruct_slabs(inventory,data)
    interpreted=propagate(a['composition_regions'],relations,inventory['structural_interpretation']['overlap_interpretations'],lookup)
    checks=[]
    for rel in relations:
        if rel['type']!='REINFORCES' or rel['state']!='AUTOMATIC_CANDIDATE' or not rel['reinforcement']:continue
        check=coverage(lookup[rel['reinforcement']],[lookup[id] for id in rel['bases']]);check['relation_id']=rel['id'];check['function_confirmed']=False
        check['review_state']='FUNCTION_AND_UNCOVERED_PART_PENDING' if check['uncovered_area_pt2'] else 'PROVISIONAL_UNION_COVERAGE'
        checks.append(check)
    groups=consolidate_relations(a['composition_regions'],interpreted,slab_result['slabs'],lookup)
    ambiguities=[{'composition_id':i['composition_id'],'kind':'UNDETERMINED_INTERPRETATION','conflicts':i['conflicts'],'candidate_relation_ids':[r['relation_id'] for r in i['relations']]} for i in interpreted if i['classification']=='UNDETERMINED']
    ambiguities.extend({'slab':s['name'],'kind':s['contour_state'],'candidate_ids':[c['id'] for c in s['contour_candidates']]} for s in slab_result['slabs'] if not s['selected_candidate_id'])
    ambiguities.extend({'region_id':c['reinforcement_id'],'kind':'UNCOVERED_WITH_UNCONFIRMED_FUNCTION','area_pt2':c['uncovered_area_pt2']} for c in checks if c['uncovered_area_pt2'])
    metrics={'candidate_relations':sum(r['state']=='AUTOMATIC_CANDIDATE' for r in relations),'confirmed_local_relations':sum(r['state']=='ENGINEER_CONFIRMED_LOCAL_SCOPE' for r in relations),
        'observed_graphical_intersections':sum(r['state']=='OBSERVED_GEOMETRY_ONLY' for r in relations),'relations_by_type':dict(Counter(r['type'] for r in relations)),
        'undetermined_compositions':sum(i['classification']=='UNDETERMINED' for i in interpreted),'newly_interpreted_by_propagation':sum(i['newly_interpreted_by_propagation'] for i in interpreted),
        'unique_preliminary_slab_contours':sum(bool(s['selected_candidate_id']) for s in slab_result['slabs']),'confirmed_slab_contours':0,
        'unique_geometric_contour_candidates':sum(len(s['contour_candidates'])==1 for s in slab_result['slabs']),
        'border_or_beam_face_review_required':sum(s['contour_state']=='BORDER_OR_BEAM_FACE_REVIEW_REQUIRED' for s in slab_result['slabs']),
        'occurrences_associated_to_unique_preliminary_contours':len({r['region_id'] for s in slab_result['slabs'] if s['selected_candidate_id'] for r in s['region_relations']}),
        'conflicting_compositions':sum(bool(i['conflicts']) for i in interpreted),'ambiguous_slab_contours':sum(s['contour_state']=='COMPETING_CANDIDATES' for s in slab_result['slabs']),
        'consolidated_regions':len(groups),'resistant_use_authorized':False}
    result['occurrence_relation_analysis']={'relations':relations,'interpreted_compositions':interpreted,'consolidated_regions':groups,
        'slab_reconstruction':slab_result,'containment_checks':checks,'ambiguities':ambiguities,'metrics':metrics,
        'inference_policy':'NO_TRANSITIVITY; HUMAN_CELL_REVIEW_SCOPE_NOT_EXTENDED; NO_STEEL_SUMMATION'}
    return result
