"""Stage 9.1: association evidence is independent of full contour containment.

Consumes the frozen stage 9 overlay. Never extends domains, clips original bars,
allocates quantities, or calls exterior portions anchorage.
"""
import copy
from collections import Counter
from polygonal_slabs import shape, LineString


def interior_length(line, domain):
    return line.intersection(domain).difference(domain.boundary).length


def line_parts(geometry):
    if geometry.geom_type == 'LineString': return [geometry]
    return [line for part in getattr(geometry, 'geoms', []) for line in line_parts(part)]


def association_evidence(occurrence, domain):
    """Use interior intersections of accepted source entities, not label distance."""
    boundary = shape(domain['geometry_pdf_pt'])
    sources = occurrence['geometry_sources']
    doc = domain['source']
    documentary = bool(doc.get('label', {}).get('text') and doc.get('thickness_text_ids') and domain['thickness_cm'] is not None)
    measure = sum(s['measure'] for s in occurrence['segments'] if domain['id'] in s['domain_ids'])
    evidence = {'domain_id':domain['id'], 'slab':domain['slab'], 'thickness_cm':domain['thickness_cm'],
        'documentary_sources':copy.deepcopy(doc), 'documentary_identity_and_thickness_available':documentary,
        'intersection_measure':measure, 'contour_confidence':'CONFIRMED' if domain['confirmed'] else 'CANDIDATE_NOT_CONFIRMED',
        'contour_review_flag':domain['review_flag'], 'state':'INDETERMINATE', 'reasons':[]}
    if not measure:
        evidence['reasons']=['NO_INTERSECTION']; return evidence
    strong = False; supported = False
    if occurrence['representation_kind']=='DISTRIBUTED':
        source=sources[0]
        bar=LineString([source['bar']['a'],source['bar']['b']])
        axis=LineString([source['distribution_axis']['a'],source['distribution_axis']['b']])
        bl,al=interior_length(bar,boundary),interior_length(axis,boundary)
        crossing=bar.intersection(axis)
        crossing_inside=not crossing.is_empty and boundary.contains(crossing)
        evidence.update(bar_interior_length_pt=bl,distribution_axis_interior_length_pt=al,
            bar_axis_crossing_inside_domain=crossing_inside,
            continuity_basis='ACCEPTED_CONTINUOUS_BAR_AND_DISTRIBUTION_AXIS',
            source_bar_ids=source['bar']['source_ids'],source_axis_ids=source['distribution_axis']['source_ids'])
        strong=bl>0 and al>0 and crossing_inside
        supported=bl>0 or al>0
        if not strong:evidence['reasons'].append('LIMITED_BAR_OR_DISTRIBUTION_AXIS_SUPPORT')
    elif occurrence['representation_kind']=='LOCALIZED':
        tests=[]
        for source in sources:
            lines=line_parts(shape(source['geometry_pdf_pt']))
            lengths=[interior_length(line,boundary) for line in lines]
            tests.append({'physical_group_id':source['physical_group_id'], 'trace_interior_lengths_pt':lengths,
                'all_traces_intersect_interior':bool(lengths) and all(x>0 for x in lengths)})
        evidence['group_support']=tests
        strong=bool(tests) and all(t['all_traces_intersect_interior'] for t in tests)
        supported=any(x>0 for t in tests for x in t['trace_interior_lengths_pt'])
        evidence['continuity_basis']='INTERIOR_INTERSECTION_OF_EACH_ACCEPTED_CONTINUOUS_TRACE; NO_BRIDGE_BETWEEN_GROUPS'
        if not strong:evidence['reasons'].append('SOME_GROUPS_OR_TRACES_HAVE_NO_INTERIOR_SUPPORT_IN_THIS_DOMAIN')
    if not documentary:evidence['reasons'].append('DOCUMENTARY_IDENTITY_OR_THICKNESS_MISSING')
    if domain['review_flag']:evidence['reasons'].append('CONTOUR_TOPOLOGY_REVIEW_FLAG')
    if supported and documentary:
        evidence['state']='RELIABLE' if strong and not domain['review_flag'] else 'PROBABLE'
    elif not supported:evidence['reasons'].append('GRAPHIC_INTERSECTION_WITHOUT_INTERIOR_ENTITY_SUPPORT')
    if evidence['state']=='RELIABLE':evidence['reasons'].append('CONSISTENT_DOCUMENTARY_AND_INTERIOR_ENTITY_EVIDENCE')
    return evidence


def refine(stage9):
    domain_lookup={d['id']:d for d in stage9['domains']}
    occurrences=[]; comparison=[]
    for old in stage9['occurrences']:
        item=copy.deepcopy(old)
        item['stage9_state']=old['state']
        ids=sorted({i for s in old['segments'] for i in s['domain_ids']})
        associations=[association_evidence(old,domain_lookup[i]) for i in ids]
        conflicts=[]
        for segment in old['segments']:
            if len(segment['domain_ids'])<2:continue
            ds=[domain_lookup[i] for i in segment['domain_ids']]
            conflicts.append({'segment_id':segment['id'], 'domain_ids':segment['domain_ids'],
                'different_thicknesses':len({d['thickness_cm'] for d in ds})>1,
                'reason':'COMPETING_DOMAINS_ON_SAME_GRAPHIC_PART'})
        state=('INDETERMINATE' if conflicts or not associations or any(a['state']=='INDETERMINATE' for a in associations)
               else 'PROBABLE' if any(a['state']=='PROBABLE' for a in associations) else 'RELIABLE')
        reasons=sorted({r for a in associations for r in a['reasons'] if a['state']!='RELIABLE'})
        if conflicts:reasons.append('COMPETING_DOMAINS_REQUIRE_ENGINEER_DECISION')
        if not associations:reasons.append('NO_INTERSECTING_DOMAIN' if old['geometry_sources'] else 'NO_PROVED_ACTUATION_GEOMETRY')
        # Exterior is preserved but has no domain thickness or semantic anchorage label.
        exterior=[s['id'] for s in old['segments'] if not s['domain_ids']]
        item.update(state=state,association_confidence=state,
            contour_confidence={a['domain_id']:a['contour_confidence'] for a in associations},
            slab_associations=associations,association_conflicts=conflicts,
            exterior_segment_ids=exterior,exterior_interpretation='UNKNOWN_NOT_AUTOMATICALLY_ANCHORAGE',
            requires_engineer_decision=state!='RELIABLE',pending_reasons=reasons,
            association_scope='OCCURRENCE_TO_SLAB; NOT_ASSIGNMENT_OF_EXTERIOR_GEOMETRY_OR_EFFECTIVE_DEPTH')
        occurrences.append(item)
        comparison.append({'display_id':item['display_id'],'position':item['documentary_mark'],
            'stage9_state':old['state'],'stage91_state':state,'changed':old['state']!=state,
            'slabs':item['slabs'],'thickness_options_cm':item['thickness_options_cm'],
            'exterior_segments_preserved':exterior,'requires_engineer_decision':item['requires_engineer_decision'],
            'reasons':reasons or ['ASSOCIATION_SUPPORTED_INDEPENDENTLY_OF_FULL_CONTAINMENT']})
    result=copy.deepcopy(stage9)
    result.update(occurrences=occurrences,comparison=comparison,
        confidence_policy='Association RELIABLE: documentary identity/thickness plus interior bar/axis or all accepted local traces. Contour confidence separate; exterior alone never downgrades association. RELIABLE is automatic association evidence, not human validation.',
        metrics={'occurrences':len(occurrences),'states':dict(Counter(o['state'] for o in occurrences)),
            'changed':sum(c['changed'] for c in comparison),
            'requires_engineer_decision':sum(o['requires_engineer_decision'] for o in occurrences),
            'with_slab_intersection':sum(bool(o['slabs']) for o in occurrences),
            'multiple_slabs':sum(o['multiple_slabs'] for o in occurrences),
            'different_thickness_domains':sum(o['different_thickness_domains'] for o in occurrences)})
    return result
