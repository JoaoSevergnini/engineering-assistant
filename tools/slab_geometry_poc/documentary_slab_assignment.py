"""Stage 9.2: derived documentary/spatial attribution, no structural geometry repair."""
import copy
from collections import Counter
from polygonal_slabs import shape, geo, LineString, Polygon, unary_union
from slab_assignment import partition_domains
from refine_slab_assignment import association_evidence
from documentary_slab_context import build_contexts


def geometry_branches(item, raw):
    """Accepted geometries or preserved unresolved hypotheses, never nearest bars."""
    if item['geometry_sources']:
        if item['representation_kind']=='DISTRIBUTED':
            geometry=unary_union([shape(s['geometry_pdf_pt']) for s in item['segments']])
        else:geometry=unary_union([shape(s['geometry_pdf_pt']) for s in item['geometry_sources']])
        return [{'id':'ACCEPTED_SOURCE','kind':item['representation_kind'],'sources':item['geometry_sources'],
            'geometry':geometry,'origin':'PREVIOUS_ACCEPTED_SOURCE','source_selection_confirmed':True}], 0
    branches=[];unassessed=0
    for index,candidate in enumerate(raw.get('candidates',[])):
        distributions=candidate.get('distribution_candidates',[])
        if not distributions:unassessed+=1
        for j,distribution in enumerate(distributions):
            if not distribution.get('junction_path_ids'):unassessed+=1;continue
            bar,axis=candidate['bar'],distribution['axis']
            branches.append({'id':'BAR_HYPOTHESIS-'+str(index)+'-'+str(j),'kind':'DISTRIBUTED',
                'sources':[{'bar':bar,'distribution_axis':axis}],
                'geometry':LineString([bar['a'],bar['b']]),'origin':'PRESERVED_UNRESOLVED_BAR_AXIS_WITH_GRAPHIC_JUNCTION',
                'source_selection_confirmed':False})
    for index,candidate in enumerate(raw.get('leader_candidates',[])):
        trace=candidate.get('trace',{})
        if not candidate.get('sufficient') or not trace.get('terminal_kind') or not candidate.get('target'):
            unassessed+=1;continue
        group=candidate.get('graphic_group') or [candidate['target']]
        g=unary_union([LineString([line['a'],line['b']]) for line in group])
        # This is an evidence hypothesis ID, not a newly reconstructed physical group.
        source={'physical_group_id':'LEADER_EVIDENCE_ONLY-'+str(index),'geometry_pdf_pt':geo(g)}
        branches.append({'id':'LEADER_HYPOTHESIS-'+str(index),'kind':'LOCALIZED','sources':[source],
            'geometry':g,'origin':'PRESERVED_UNRESOLVED_LEADER_TARGET','source_selection_confirmed':False,
            'leader_source_ids':trace.get('segment_ids',[])})
    return branches,unassessed


def analyze(inventory):
    previous=inventory['refined_slab_assignment'];contexts=build_contexts(inventory,previous['domains'])
    # A context is an attribution aid, not a validation upgrade of its contour.
    evaluation_domains=[{'id':c['domain_id'],'slab':c['slab'],'geometry_pdf_pt':c['geometry_pdf_pt'],
        'thickness_cm':c['thickness_cm'],'source':c['documentary_sources'],'confirmed':False,'review_flag':False} for c in contexts]
    context_lookup={c['domain_id']:c for c in contexts}
    raw_lookup={o['occurrence_id']:o for o in inventory['occurrences']}
    occurrences=[];comparison=[]
    for old in previous['occurrences']:
        raw=raw_lookup[old['occurrence_id']];branches,unassessed=geometry_branches(old,raw)
        evaluations=[];partitions=[];branch_sets=[];conflicts=[]
        for branch in branches:
            dimension=2 if branch['geometry'].area>0 else 1
            parts=partition_domains(branch['geometry'],evaluation_domains,dimension)
            for p in parts:p.update(branch_id=branch['id'],quantity_reference=old['occurrence_id'],not_a_replacement_actuation_region=True)
            partitions.extend(parts)
            virtual={'geometry_sources':branch['sources'],'representation_kind':branch['kind'],'segments':parts}
            associated=[]
            for d in evaluation_domains:
                if not any(d['id'] in p['domain_ids'] for p in parts):continue
                evidence=association_evidence(virtual,d)
                evidence.update(branch_id=branch['id'],geometry_origin=branch['origin'],
                    source_selection_confirmed=branch['source_selection_confirmed'],
                    context_id=context_lookup[d['id']]['context_id'],
                    contour_confidence=context_lookup[d['id']]['contour_confidence'],
                    contour_review_flag=context_lookup[d['id']]['contour_review_flag'])
                # The alert is retained as contour metadata, never as an association veto.
                evaluations.append(evidence)
                associated.append(evidence['slab'])
            branch_sets.append(set(associated))
            for p in parts:
                if len(p['domain_ids'])>1:
                    ds=[context_lookup[i] for i in p['domain_ids']]
                    conflicts.append({'branch_id':branch['id'],'domain_ids':p['domain_ids'],
                        'thicknesses_cm':sorted({d['thickness_cm'] for d in ds if d['thickness_cm'] is not None}),
                        'geometry_pdf_pt':p['geometry_pdf_pt'],'reason':'COMPETING_SPATIAL_CONTEXTS'})
        hypotheses=bool(branches) and not branches[0]['source_selection_confirmed']
        alternative_disagreement=hypotheses and any(s!=branch_sets[0] for s in branch_sets)
        search_limits=raw.get('leader_search',{}).get('search_limits',[]) if hypotheses else []
        states={e['state'] for e in evaluations}
        state=('INDETERMINATE' if not evaluations or conflicts or alternative_disagreement or 'INDETERMINATE' in states
            else 'PROBABLE' if 'PROBABLE' in states or unassessed or search_limits else 'RELIABLE')
        reasons=[]
        if not evaluations:reasons.append('NO_SUPPORTED_SPATIAL_EVIDENCE' if branches else 'NO_ACTUATION_OR_SUPPORTED_GRAPHIC_HYPOTHESIS')
        if conflicts:reasons.append('COMPETING_SPATIAL_CONTEXTS')
        if alternative_disagreement:reasons.append('GEOMETRY_ALTERNATIVES_DISAGREE_ON_SLAB')
        if unassessed:reasons.append('SOME_GEOMETRY_ALTERNATIVES_LACK_ASSOCIATION_EVIDENCE')
        if search_limits:reasons.append('LEADER_SEARCH_INCOMPLETE')
        reasons.extend(sorted({r for e in evaluations if e['state']!='RELIABLE' for r in e['reasons']}))
        conflict_ids={i for c in conflicts for i in c['domain_ids']}
        for evidence in evaluations:
            if evidence['domain_id'] in conflict_ids or alternative_disagreement:
                evidence['local_evidence_state']=evidence['state'];evidence['state']='INDETERMINATE'
        slabs=sorted({e['slab'] for e in evaluations})
        h=sorted({e['thickness_cm'] for e in evaluations if e['thickness_cm'] is not None})
        quality=('UNRESOLVED_GRAPHIC_ALTERNATIVES_NOT_SELECTED' if hypotheses else
            'EXTRACTED_DISTRIBUTION_NOT_STRUCTURALLY_VALIDATED' if old['representation_kind']=='DISTRIBUTED' else
            'EXTRACTED_GROUP_TRACES_NOT_FULL_PHYSICAL_LAYOUT_VALIDATION' if branches else 'NO_SUPPORTED_GEOMETRY')
        geometry_reasons={'SOME_GEOMETRY_ALTERNATIVES_LACK_ASSOCIATION_EVIDENCE','LEADER_SEARCH_INCOMPLETE','NO_ACTUATION_OR_SUPPORTED_GRAPHIC_HYPOTHESIS'}
        issues={'documentary':sorted({r for e in evaluations for r in e['reasons'] if 'DOCUMENTARY' in r}),
            'spatial':sorted({r for r in reasons if 'DOCUMENTARY' not in r and r not in geometry_reasons}),
            'topological':[{'domain_id':i,'alert':'ORIGINAL_CONTOUR_TOPOLOGY_FLAG; NOT_AN_ASSOCIATION_VETO'}
                for i in sorted({e['domain_id'] for e in evaluations}) if context_lookup[i]['contour_review_flag']],
            'actuation_geometry':[quality]+sorted(set(reasons)&geometry_reasons)}
        item=copy.deepcopy(old)
        item.update(stage91_state=old['state'],state=state,association_confidence=state,
            association_conflicts=conflicts,slabs=slabs,thickness_options_cm=h,
            multiple_slabs=len(slabs)>1,different_thickness_domains=len(h)>1,
            contour_confidence={i:context_lookup[i]['contour_confidence'] for i in sorted({e['domain_id'] for e in evaluations})},
            slab_associations=evaluations,spatial_context_partition=partitions,
            actuation_geometry_quality=quality,geometry_alternatives_not_selected=hypotheses,
            context_branch_sources=[{'id':b['id'],'origin':b['origin'],'geometry_pdf_pt':geo(b['geometry']),
                'source_selection_confirmed':b['source_selection_confirmed'],
                'leader_source_ids':b.get('leader_source_ids',[])} for b in branches],
            issues=issues,pending_reasons=reasons,requires_engineer_decision=state!='RELIABLE',
            requires_geometry_review=hypotheses or not branches,
            resistance_use_authorized=False,
            scope='DOCUMENTARY_SPATIAL_ATTRIBUTION_ONLY; NO_APPROVAL_OR_EFFECTIVE_DEPTH',
            association_scope='OCCURRENCE_TO_SLAB_CONTEXT; DOES_NOT_ASSIGN_CONTEXT_AS_VALIDATED_STRUCTURAL_DOMAIN')
        occurrences.append(item)
        comparison.append({'display_id':old['display_id'],'position':old['documentary_mark'],
            'previous_state':old['state'],'new_state':state,'changed':old['state']!=state,
            'previous_slabs':old['slabs'],'slabs':slabs,'thickness_options_cm':h,
            'issues':issues,'requires_engineer_decision':item['requires_engineer_decision'],
            'requires_geometry_review':item['requires_geometry_review']})
    result=copy.deepcopy(previous)
    result.update(contexts=contexts,occurrences=occurrences,comparison=comparison,
        slab_index=[{'slab':name,'occurrences':[o['display_id'] for o in occurrences if name in o['slabs']],
            'quantity_sum':None} for name in sorted({c['slab'] for c in contexts})],
        confidence_policy='Documentary/spatial association independent of contour quality and geometry-source selection. No topology-only veto; no source geometry repair.',
        metrics={'occurrences':len(occurrences),'states':dict(Counter(o['state'] for o in occurrences)),
            'changed':sum(c['changed'] for c in comparison),
            'association_decisions_pending':sum(o['requires_engineer_decision'] for o in occurrences),
            'geometry_reviews_pending_independently':sum(o['requires_geometry_review'] for o in occurrences),
            'multiple_slabs':sum(o['multiple_slabs'] for o in occurrences),
            'different_thickness_domains':sum(o['different_thickness_domains'] for o in occurrences)})
    return result
