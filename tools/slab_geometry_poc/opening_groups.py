"""Stage 4: evidence-separated opening edges and localized physical-group hypotheses.

No changes to distributed reinforcement or stage 3 decisions. A graphical stroke
count is never a physical bar count. Office conventions require explicit scope.
"""
import copy
import hashlib
import json
import math
from collections import defaultdict
from automatic import line_geometry,center


def box_of(line):
    a,b=line['a'],line['b']
    return [min(a[0],b[0]),min(a[1],b[1]),max(a[0],b[0]),max(a[1],b[1])]


def graphic_pairs(lines):
    """Equal-extent adjacent strokes; counts describe drawing entities only."""
    result=[];used=set()
    for a in sorted(lines,key=lambda s:s['id']):
        if a['length_pt']<15 or a['id'] in used:continue
        k=a['orientation'];j=1-k;lo,hi=sorted([a['a'][k],a['b'][k]])
        matches=[]
        for b in lines:
            if b['id']==a['id'] or b['orientation']!=k:continue
            bl,bh=sorted([b['a'][k],b['b'][k]])
            if abs(bl-lo)<=.3 and abs(bh-hi)<=.3 and 1<=abs(b['a'][j]-a['a'][j])<=4:
                matches.append(b)
        # A cluster of more than two strokes is retained as an ambiguous graphic
        # cluster; not split to match any printed multiplicity.
        members=sorted([a]+matches,key=lambda s:s['id'])
        if not matches:continue
        key=tuple(s['id'] for s in members)
        if any(tuple(p['line_ids'])==key for p in result):continue
        used.update(key)
        geometry=sorted([[*s['a'],*s['b']] for s in members])
        id='P-'+hashlib.sha256(json.dumps(geometry).encode()).hexdigest()[:10]
        result.append(dict(id=id,orientation=k,lines=members,line_ids=list(key),
                           extent=[lo,hi],normal=sum(s['a'][j] for s in members)/len(members),
                           state='GRAPHIC_PAIR' if len(members)==2 else 'AMBIGUOUS_GRAPHIC_CLUSTER'))
    return result


def edge_attachment(pair,box,max_gap=8,overhang=2):
    k=pair['orientation'];lo,hi=pair['extent'];n=pair['normal']
    edge_lo,edge_hi=(box[0],box[2]) if k==0 else (box[1],box[3])
    if lo>edge_lo-overhang or hi<edge_hi+overhang:return None
    borders=[('TOP',box[1],box[1]-n),('BOTTOM',box[3],n-box[3])] if k==0 else [('LEFT',box[0],box[0]-n),('RIGHT',box[2],n-box[2])]
    hits=[dict(side=side,normal_gap_pt=gap,border_coordinate_pt=value,
               overhang_pt=[edge_lo-lo,hi-edge_hi]) for side,value,gap in borders if .4<=gap<=max_gap]
    return hits[0] if len(hits)==1 else None


def covered_edge(segments,a,b,tolerance=.25):
    k=0 if abs(a[1]-b[1])<tolerance else 1;j=1-k
    lo,hi=sorted([a[k],b[k]]);intervals=[];ids=[]
    for s in segments:
        if abs(s['a'][j]-a[j])>tolerance or abs(s['b'][j]-a[j])>tolerance:continue
        l,h=sorted([s['a'][k],s['b'][k]])
        if h>lo+tolerance and l<hi-tolerance:intervals.append((max(lo,l),min(hi,h)));ids.append(s['id'])
    reached=lo
    for l,h in sorted(intervals):
        if l>reached+tolerance:break
        reached=max(reached,h)
    return dict(complete=reached>=hi-tolerance,segment_ids=sorted(ids))


def recognize_openings(data,roi,scale=50):
    """Propose rectangles from complete X diagonals; require contour + edge pairs.

    Rectangle/X alone is inconclusive. No color, fixed position or dimensions
    whitelist. More exotic symbols remain outside this experimental recognizer.
    """
    diagonals=defaultdict(list)
    for s in data['segments']:
        box=box_of(s)
        if min(box[2]-box[0],box[3]-box[1])<3:continue
        if not (roi[0]<=box[0] and box[2]<=roi[2] and roi[1]<=box[1] and box[3]<=roi[3]):continue
        diagonals[tuple(round(v,1) for v in box)].append(s)
    lines=line_geometry(data['segments']);pairs=graphic_pairs(lines);candidates=[]
    for key,diags in diagonals.items():
        pos=[s for s in diags if (s['a'][0]-s['b'][0])*(s['a'][1]-s['b'][1])>0]
        neg=[s for s in diags if (s['a'][0]-s['b'][0])*(s['a'][1]-s['b'][1])<0]
        if not pos or not neg:continue
        box=box_of(diags[0]);x0,y0,x1,y1=box
        contour=[[x0,y0],[x1,y0],[x1,y1],[x0,y1]]
        edges=[covered_edge(data['segments'],a,b) for a,b in zip(contour,contour[1:]+contour[:1])]
        adjacent=[]
        for pair in pairs:
            relation=edge_attachment(pair,box)
            if relation and pair['state']=='GRAPHIC_PAIR':adjacent.append(dict(pair_id=pair['id'],**relation))
        sides={r['side'] for r in adjacent}
        supported=all(e['complete'] for e in edges) and len(sides)>=2
        candidates.append(dict(bbox=box,contour_pdf_pt=contour,diagonal_ids=sorted(s['id'] for s in diags),
            edge_evidence=edges,adjacent_graphic_pairs=adjacent,
            state='GRAPHICALLY_SUPPORTED_OPENING' if supported else 'UNCONFIRMED_RECTANGLE_X',
            dimensions_graphic=dict(width_pt=x1-x0,height_pt=y1-y0,
                width_cm=(x1-x0)*2.54/72*scale,height_cm=(y1-y0)*2.54/72*scale),
            validation=dict(status='PENDING_ENGINEER_REVIEW',reviewer=None),
            nature='GRAPHICAL_INTERPRETATION; NOT A DIMENSIONED PHYSICAL SURVEY'))
    candidates.sort(key=lambda h:(h['bbox'][1],h['bbox'][0]))
    for i,h in enumerate(candidates,1):h['id']=f'H{i:02}'
    return dict(candidates=candidates,openings=[h for h in candidates if h['state']=='GRAPHICALLY_SUPPORTED_OPENING'],pairs=pairs)


def choose_opening_relations(pair,openings):
    hits=[]
    for h in openings:
        relation=edge_attachment(pair,h['bbox'])
        if relation:hits.append(dict(opening_id=h['id'],**relation))
    if len(hits)<=1:return ('ASSOCIATED' if hits else 'UNRESOLVED'),hits
    # Several aligned, disjoint openings can be bordered by one continuous run.
    boxes={h['id']:h['bbox'] for h in openings};k=pair['orientation']
    ordered=sorted((boxes[r['opening_id']][k],boxes[r['opening_id']][k+2]) for r in hits)
    same_edge=len({r['side'] for r in hits})==1 and max(r['border_coordinate_pt'] for r in hits)-min(r['border_coordinate_pt'] for r in hits)<=.3
    disjoint=all(a[1]<b[0] for a,b in zip(ordered,ordered[1:]))
    return ('SHARED_EDGE_RUN' if same_edge and disjoint else 'AMBIGUOUS'),hits


def convention_applicability(profile,source_sha256):
    if not profile:return dict(confirmed=False,reason='NO_CONFIRMED_CONVENTION',profile_id=None)
    if profile.get('source_pdf_sha256')!=source_sha256 or profile.get('office')!='SIM Projetos':
        return dict(confirmed=False,reason='OFFICE_OR_DOCUMENT_SCOPE_MISMATCH',profile_id=profile.get('id'))
    if not profile.get('confirmed_by_engineer') or not profile.get('sources'):
        return dict(confirmed=False,reason='CONVENTION_SOURCE_NOT_CONFIRMED',profile_id=profile.get('id'))
    rule=profile.get('rule',{})
    if (rule.get('per_group_bars'),rule.get('lower'),rule.get('upper'))!=(3,2,1):
        return dict(confirmed=False,reason='UNSUPPORTED_OR_CONTRADICTORY_RULE_REQUIRES_REVIEW',profile_id=profile.get('id'))
    return dict(confirmed=True,reason='EXPLICIT_ENGINEER_CONFIRMATION_AND_DOCUMENT_SCOPE',profile_id=profile['id'])


def physical_id(mark,pair):
    # Geometry and mark, not textual occurrence. Repeated calls reuse the group.
    coords=sorted([tuple(round(v,2) for v in box_of(s)) for s in pair['lines']])
    return 'G-'+hashlib.sha256(json.dumps([mark,coords]).encode()).hexdigest()[:10]


def reconstruct_localized(stage3,data,profile=None):
    """Enrich a COPY: stage 3 statuses, distributed entities and geometry unchanged."""
    original=copy.deepcopy(stage3)
    detected=recognize_openings(data,stage3['layout']['detail_roi_pt'],stage3['layout']['scale_denominator'])
    pairs=detected['pairs'];openings=detected['openings'];groups={};records=[]
    applicability=convention_applicability(profile,stage3['provenance']['sha256'])
    targeted_by=defaultdict(set)
    for o in stage3['occurrences']:
        if o['representation_kind']=='LOCALIZED':
            for s in o['associated_lines']:targeted_by[s['id']].add(o['documentary_mark'])
    for o in stage3['occurrences']:
        if o['representation_kind']!='LOCALIZED':continue
        call=o['call'];factors=call['quantity_factors'];issues=[]
        overrides=(profile or {}).get('specific_overrides',{}).get(o['occurrence_id'])
        ids={s['id'] for s in o['associated_lines']}
        targets=[p for p in pairs if ids==set(p['line_ids'])]
        record=dict(occurrence_id=o['occurrence_id'],display_id=o['display_id'],mark=o['documentary_mark'],
            text=o['text'],call=copy.deepcopy(call),leader=copy.deepcopy(o['leader_association']['trace']),
            direct_trace_ids=sorted(ids),group_ids=[],candidate_opposite_pairs=[],opening_alternatives=[],
            convention=copy.deepcopy(applicability),issues=issues,validation=dict(status='PENDING_ENGINEER_REVIEW',reviewer=None))
        accepted=[];relations=[];relation_state='UNRESOLVED';rule=False
        if len(targets)==1 and targets[0]['state']=='GRAPHIC_PAIR':
            target=targets[0];accepted=[(target,'DIRECT_LEADER_TARGET')]
            relation_state,relations=choose_opening_relations(target,openings)
            record['opening_alternatives']=relations
            rule=(applicability['confirmed'] and factors in ([2,3],[3])
                  and factors in profile['rule'].get('allowed_factors',[])
                  and factors not in profile.get('excluded_factors',[])
                  and not overrides
                  and relation_state in ('ASSOCIATED','SHARED_EDGE_RUN'))
            if factors==[2,3] and relations:
                opposite={'LEFT':'RIGHT','RIGHT':'LEFT','TOP':'BOTTOM','BOTTOM':'TOP'}
                for peer in pairs:
                    if peer['id']==target['id'] or peer['orientation']!=target['orientation'] or peer['state']!='GRAPHIC_PAIR':continue
                    if any(abs(a-b)>1 for a,b in zip(peer['extent'],target['extent'])):continue
                    peer_state,peer_relations=choose_opening_relations(peer,openings)
                    if peer_state not in ('ASSOCIATED','SHARED_EDGE_RUN'):continue
                    expected={(r['opening_id'],opposite[r['side']]) for r in relations}
                    actual={(r['opening_id'],r['side']) for r in peer_relations}
                    if actual!=expected:continue
                    conflicts=sorted(set().union(*(targeted_by[s] for s in peer['line_ids']))-{o['documentary_mark']})
                    record['candidate_opposite_pairs'].append(dict(pair_id=peer['id'],line_ids=peer['line_ids'],relations=peer_relations,conflicting_marks=conflicts))
                candidates=record['candidate_opposite_pairs']
                if rule and len(candidates)==1 and not candidates[0]['conflicting_marks']:
                    peer=next(p for p in pairs if p['id']==candidates[0]['pair_id'])
                    accepted.append((peer,'GEOMETRY_OPPOSITE_EDGE_AND_SIM_CONVENTION'))
                else:
                    issues.append('OPPOSITE_GROUP_NOT_UNIQUELY_PROVED_OR_CONVENTION_UNCONFIRMED')
            if relation_state=='AMBIGUOUS':issues.append('MULTIPLE_PLAUSIBLE_OPENING_ASSOCIATIONS')
            elif relation_state=='UNRESOLVED':issues.append('NO_OPENING_EDGE_SUPPORTED')
        else:issues.append('DIRECT_GRAPHIC_CLUSTER_NOT_UNIQUELY_IDENTIFIED')
        # A convention conflict or a specific-detail override never rewrites facts.
        if overrides:
            issues.append('SPECIFIC_DETAIL_CONFLICT_REQUIRES_REVIEW');rule=False
            record['specific_detail_evidence']=overrides
        for pair,origin in accepted:
            id=physical_id(o['documentary_mark'],pair)
            state,edge_relations=choose_opening_relations(pair,openings)
            # Missing the opposite group does not erase the confirmed per-group
            # convention for an actually located edge group. No absent group is
            # materialized to make the printed count balance.
            interpreted=rule
            quantity=3 if interpreted else call['quantity'] if factors==[3] and len(accepted)==1 else None
            group=dict(id=id,mark=o['documentary_mark'],representation_ids=[o['occurrence_id']],
                opening_association_state=state,opening_relations=edge_relations if state!='AMBIGUOUS' else [],
                opening_alternatives=edge_relations if state=='AMBIGUOUS' else [],
                orientation='HORIZONTAL' if pair['orientation']==0 else 'VERTICAL',
                lines=copy.deepcopy(pair['lines']),graphic_pair_id=pair['id'],
                quantity_bars=quantity,quantity_origin='EXPLICIT_SINGLE_GROUP_CALL' if factors==[3] and quantity is not None else 'SIM_CONVENTION_AND_PROVED_OPENING_EDGE_GROUP' if interpreted else 'UNKNOWN',
                diameter_mm=call['diameter_mm'],nominal_length_cm=call['nominal_length_cm'],
                layer_distribution=dict(lower=2,upper=1,origin='OFFICE_CONVENTION_NOT_PLAN_GEOMETRY',convention_id=profile['id']) if interpreted else dict(lower=None,upper=None,origin='UNKNOWN',convention_id=None),
                geometry_origin=origin,source_trace_ids=pair['line_ids'],
                location_pdf_pt=dict(bbox= [min(box_of(s)[0] for s in pair['lines']),min(box_of(s)[1] for s in pair['lines']),max(box_of(s)[2] for s in pair['lines']),max(box_of(s)[3] for s in pair['lines'])]),
                documentary_sources=dict(representation_id=o['occurrence_id'],text_ids=o['text_ids'],diameter='PDF_CALL',length='PDF_CALL_NOMINAL_NOT_GRAPHIC_PROJECTION'),
                interpretation_sources=copy.deepcopy(profile['sources']) if interpreted else [dict(type='PDF_CALL_AND_LEADER',text_ids=o['text_ids'])],
                evidence_state='GEOMETRICALLY_SUPPORTED_PENDING_ENGINEER_REVIEW',
                validation=dict(status='PENDING_ENGINEER_REVIEW',reviewer=None),issues=[])
            if overrides:
                group['issues'].append(dict(code='SPECIFIC_DETAIL_CONFLICT_REQUIRES_REVIEW',evidence=overrides,
                    convention_proposal=dict(lower=2,upper=1,bars_per_group=3)))
                group['evidence_state']='CONFLICTING_REQUIRES_ENGINEER_REVIEW'
            if id in groups:
                prior=groups[id];prior['representation_ids']=sorted(set(prior['representation_ids']+[o['occurrence_id']]))
                for key in ('quantity_bars','diameter_mm','nominal_length_cm','layer_distribution'):
                    if prior[key]!=group[key]:
                        prior['issues'].append(dict(code='CONFLICTING_DOCUMENTARY_INTERPRETATIONS',field=key,values=[prior[key],group[key]]))
                        prior[key]=None if key!='layer_distribution' else dict(lower=None,upper=None,origin='CONFLICTING',convention_id=None)
                        prior['evidence_state']='CONFLICTING_REQUIRES_ENGINEER_REVIEW'
            else:groups[id]=group
            record['group_ids'].append(id)
        record['opening_association_state']=relation_state
        record['convention_applied']=bool(rule and accepted)
        record['multiplicity']=dict(original_factors=factors,printed_total=call['quantity'],
            groups_geometrically_located=len(accepted),bars_per_group=3 if rule and accepted else call['quantity'] if factors==[3] else None,
            indicated_group_count=2 if factors==[2,3] and applicability['confirmed'] else 1 if factors==[3] else None,
            unlocated_group_count=2-len(accepted) if factors==[2,3] and applicability['confirmed'] else 0 if factors==[3] and len(accepted)==1 else None,
            factor_semantics='SIM_2_GROUPS_OF_3' if factors==[2,3] and applicability['confirmed'] else 'SINGLE_GROUP_EXPLICIT' if factors==[3] else 'UNCONFIRMED',
            conditional_missing_if_first_factor_means_groups=max(0,factors[0]-len(accepted)) if len(factors)>1 else None)
        if factors not in ([2,3],[3]):issues.append('MULTIPLICITY_OUTSIDE_CONFIRMED_SIM_RULE')
        records.append(record)
    ordered_groups=sorted(groups.values(),key=lambda g:(min(box_of(s)[1] for s in g['lines']),min(box_of(s)[0] for s in g['lines']),g['mark']))
    for i,g in enumerate(ordered_groups,1):g['display_id']=f'G{i:02}'
    for record in records:
        record['reconstruction_state']='PARTIAL' if record['issues'] else 'SUPPORTED_PENDING_ENGINEER_REVIEW'
    original['localized_reconstruction']=dict(opening_candidates=detected['candidates'],openings=openings,
        physical_scope='GROUP_HYPOTHESES_IN_ONE_DRAWN_LAYOUT; TIPO_1_AND_2_FLOOR_MULTIPLICITY_NOT_EXPANDED',
        graphic_pairs=pairs,representations=records,physical_groups=ordered_groups,
        convention_profile=profile,convention_scope=applicability,
        criteria=dict(edge_normal_gap_pt=[.4,8],edge_overhang_min_pt=2,equal_extent_pt=.3,opposite_group_extent_match_pt=1,paired_stroke_gap_pt=[1,4],identity_geometry_rounding_pt=.01,
                      opening_requires='RECTANGULAR_CONTOUR + X + PAIRED_REINFORCEMENT_ON_AT_LEAST_TWO_SIDES'),
        metrics=dict(localized_representations=len(records),opening_candidates=len(detected['candidates']),supported_openings=len(openings),
            physical_groups=len(groups),convention_applied_representations=sum(r['convention_applied'] for r in records),
            groups_with_layer_distribution=sum(g['layer_distribution']['lower'] is not None for g in groups.values()),
            unresolved_representations=sum(bool(r['issues']) for r in records),coverage=None,independent_engineer_validations=0))
    return original
