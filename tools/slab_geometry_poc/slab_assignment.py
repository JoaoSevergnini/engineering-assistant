"""Stage 9: spatial domains only; no allocation of bars or structural capacity."""
import copy
import hashlib
import json
from collections import Counter
from polygonal_slabs import shape, geo, LineString, unary_union


def domains(inventory, texts=()):
    documentary = {s['id']: s for s in inventory['structural_interpretation']['slabs']}
    lookup = {t['id']: t for t in texts}
    result = []
    for slab in inventory['complex_slab_contour_analysis']['slabs']:
        source = documentary[slab['label_id']]
        for candidate in slab['candidates']:
            result.append({'id': candidate['id'], 'slab': slab['name'],
                'thickness_cm': source['thickness_cm'],
                'geometry_pdf_pt': candidate['geometry_pdf_pt'],
                'confirmed': candidate.get('engineer_confirmed', False),
                'review_flag': candidate.get('thin_border_review_flag', False),
                'source': {'label': source['label'], 'thickness_text_ids': source['thickness_sources'],
                    'thickness_texts': [lookup[i] for i in source['thickness_sources'] if i in lookup],
                    'boundary_segment_ids': candidate['boundary_segment_ids']}})
    return sorted(result, key=lambda d: (d['slab'], d['id']))


def partition_domains(geometry, domain_list, dimension=2):
    """Disjoint exact overlay. Alternative domains remain alternatives, never additive."""
    if geometry.is_empty or not geometry.is_valid:
        return []
    measure = lambda g: g.area if dimension == 2 else g.length
    parts = [(geometry, ())]
    ordered = sorted(domain_list, key=lambda d: (d['slab'], d['id']))
    for domain in ordered:
        boundary = shape(domain['geometry_pdf_pt'])
        if not boundary.is_valid or boundary.is_empty:
            raise ValueError('INVALID_SLAB_DOMAIN:' + domain['id'])
        split = []
        for part, membership in parts:
            inside, outside = part.intersection(boundary), part.difference(boundary)
            if measure(inside) > 0: split.append((inside, membership + (domain['id'],)))
            if measure(outside) > 0: split.append((outside, membership))
        parts = split
    lookup = {d['id']: d for d in ordered}
    result = []
    for part, membership in parts:
        members = [lookup[i] for i in membership]
        # No confidence upgrade from visual plausibility of an unconfirmed contour.
        state = ('INDETERMINATE' if len(members) != 1 or members[0]['thickness_cm'] is None
                 else 'RELIABLE' if members[0]['confirmed'] and not members[0]['review_flag'] else 'PROBABLE')
        result.append({'geometry_pdf_pt': geo(part), 'domain_ids': list(membership),
            'slabs': sorted({d['slab'] for d in members}),
            'thickness_options_cm': sorted({d['thickness_cm'] for d in members if d['thickness_cm'] is not None}),
            'state': state, 'reason': 'NO_DOMAIN' if not members else 'COMPETING_DOMAINS' if len(members)>1 else 'CONFIRMED_DOMAIN' if state=='RELIABLE' else 'CANDIDATE_DOMAIN',
            'measure': measure(part), 'measure_unit': 'pt2' if dimension == 2 else 'pt',
            'quantity_allocation': None, 'physical_bar_segmentation': False})
    return sorted(result, key=lambda p: (p['domain_ids'], json.dumps(p['geometry_pdf_pt'], sort_keys=True)))


def apply_confirmations(regions, profile, source_hash):
    """Scoped human overlay; documentary marks are not algorithmic role rules."""
    if profile.get('source_pdf_sha256') != source_hash:
        raise ValueError('CONFIRMATION_SOURCE_MISMATCH')
    lookup = {r['id']: r for r in regions}
    result = []
    for record in profile['records']:
        r = lookup[record['region_id']]
        if r['occurrence_id'] != record['occurrence_id'] or r['position'] != record['position']:
            raise ValueError('CONFIRMATION_IDENTITY_MISMATCH')
        if record['geometry_sha256'] != hashlib.sha256(json.dumps(r['polygon_pdf_pt'], sort_keys=True).encode()).hexdigest():
            raise ValueError('CONFIRMATION_GEOMETRY_MISMATCH')
        result.append(copy.deepcopy(record))
    return result


def analyze(inventory, texts=(), confirmations=None):
    domain_list = domains(inventory, texts)
    regions = inventory['distributed_spatial_analysis']['regions']
    by_occurrence = {r['occurrence_id']: r for r in regions}
    groups = inventory['localized_reconstruction']['physical_groups']
    human = apply_confirmations(regions, confirmations, inventory['stage5_provenance']['sha256']) if confirmations else []
    overrides = {r['region_id']: r for r in human}
    roles = {r['region_id']: r for r in inventory['structural_interpretation']['function_candidates']}
    occurrences = []
    for occurrence in inventory['occurrences']:
        oid = occurrence['occurrence_id']
        item = {k: copy.deepcopy(occurrence[k]) for k in ('occurrence_id','display_id','documentary_mark','representation_kind','status','call','text_ids')}
        item.update(quantity_policy='ORIGINAL_CALL_ONLY_NO_SUM_OR_ALLOCATION', segments=[], geometry_sources=[])
        r = by_occurrence.get(oid)
        if r:
            from polygonal_slabs import Polygon
            item['geometry_sources'] = [{'region_id': r['id'], 'bar': r['bar'], 'distribution_axis': r['distribution_axis'],
                'longitudinal_extent_pt': r['longitudinal_extent_pt'], 'transverse_extent_pt': r['transverse_extent_pt'],
                'identity_group': r['identity_group'], 'nominal_length_is_graphic_projection': False}]
            item['segments'] = partition_domains(Polygon(r['polygon_pdf_pt']), domain_list)
            item['structural_interpretation'] = {'previous_role_candidate': roles.get(r['id']),
                'human_overlay': overrides.get(r['id']), 'prior_composition_classifications_preserved': True,
                'lap_partner_and_lap_length_not_inferred': True}
            human_record = overrides.get(r['id'])
            item['structural_interpretation']['active_classification'] = (human_record['classification'] if human_record
                else roles.get(r['id'], {}).get('role_candidate', 'UNKNOWN'))
            item['structural_interpretation']['active_origin'] = 'ENGINEER_CONFIRMED' if human_record else 'PREVIOUS_CANDIDATE_NOT_CONFIRMED'
            item['structural_interpretation']['reinforcement_containment_applicable'] = (False if human_record and human_record['classification']=='LAP_SPLICE' else None)
        elif occurrence['representation_kind'] == 'LOCALIZED':
            for group in groups:
                if oid not in group['representation_ids']: continue
                geometry = unary_union([LineString([line['a'],line['b']]) for line in group['lines']])
                pieces = partition_domains(geometry, domain_list, 1)
                for piece in pieces: piece['physical_group_id'] = group['id']
                item['segments'].extend(pieces)
                item['geometry_sources'].append({'physical_group_id': group['id'], 'source_trace_ids': group['source_trace_ids'],
                    'geometry_pdf_pt': geo(geometry), 'quantity_reference': 'localized_reconstruction.physical_groups:' + group['id'],
                    'area_envelope_created': False})
        for index, segment in enumerate(item['segments'],1):
            segment.update(id=occurrence['display_id']+'-S'+str(index).zfill(3), quantity_reference=oid)
        item['slabs'] = sorted({name for s in item['segments'] for name in s['slabs']})
        item['thickness_options_cm'] = sorted({h for s in item['segments'] for h in s['thickness_options_cm']})
        item['multiple_slabs'] = len(item['slabs']) > 1
        item['different_thickness_domains'] = len(item['thickness_options_cm']) > 1
        item['measure_summary'] = {unit: {'total': sum(s['measure'] for s in item['segments'] if s['measure_unit']==unit),
            'outside_all_domains': sum(s['measure'] for s in item['segments'] if s['measure_unit']==unit and not s['domain_ids']),
            'competing_domains': sum(s['measure'] for s in item['segments'] if s['measure_unit']==unit and len(s['domain_ids'])>1)}
            for unit in sorted({s['measure_unit'] for s in item['segments']})}
        states = {s['state'] for s in item['segments']}
        item['state'] = 'INDETERMINATE' if not states or 'INDETERMINATE' in states else 'PROBABLE' if 'PROBABLE' in states else 'RELIABLE'
        item['pending_reasons'] = sorted({s['reason'] for s in item['segments'] if s['state'] != 'RELIABLE'}) or ([] if states else ['NO_PROVED_ACTUATION_GEOMETRY'])
        occurrences.append(item)
    return {'domains': domain_list, 'occurrences': occurrences, 'human_confirmations': human,
        'slab_index': [{'slab': name, 'occurrences': [o['display_id'] for o in occurrences if name in o['slabs']],
            'quantity_sum': None} for name in sorted({d['slab'] for d in domain_list})],
        'metrics': {'occurrences':len(occurrences), 'states':dict(Counter(o['state'] for o in occurrences)),
            'with_slab_intersection':sum(bool(o['slabs']) for o in occurrences),
            'multiple_slabs':sum(o['multiple_slabs'] for o in occurrences),
            'different_thickness_domains':sum(o['different_thickness_domains'] for o in occurrences),
            'without_actuation_geometry':sum(not o['geometry_sources'] for o in occurrences)},
        'confidence_policy':'RELIABLE requires confirmed domain; candidate-only matches are PROBABLE; competing or uncovered parts INDETERMINATE',
        'coordinates':'PDF_POINTS_ORIGINAL', 'quantities_aggregated':False, 'effective_depth_or_resistance_computed':False}
