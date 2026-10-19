"""Endpoint-topology leader tracing and conservative localized graphic groups.

No nearest destination, no switching at interior crossings, no color/mark whitelist.
All thresholds are experimental PDF-point tolerances, not engineering limits.
The baseline read_sheet API and its output classifications remain available.
"""
import math
from collections import Counter,defaultdict
from automatic import (read_sheet,line_geometry,distribution_axes,junctions,local_box,
                       center,bar_axis_intersection,graphic_envelope)


def dot(a,b):return a[0]*b[0]+a[1]*b[1]
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def sub(a,b):return [a[0]-b[0],a[1]-b[1]]


class EndpointGraph:
    """Use geometrical endpoints only; interior intersections are not graph nodes."""
    def __init__(self,segments,tolerance=.2):
        self.tolerance=tolerance;self.cells=defaultdict(list)
        self.segments={s['id']:s for s in segments if s['length_pt']>.05}
        for s in self.segments.values():
            for end in ('a','b'):self.cells[self.key(s[end])].append((s['id'],end))

    def key(self,p):return (math.floor(p[0]/self.tolerance),math.floor(p[1]/self.tolerance))

    def incident(self,p):
        x,y=self.key(p);found=[]
        for i in (-1,0,1):
            for j in (-1,0,1):
                for id,end in self.cells.get((x+i,y+j),[]):
                    s=self.segments[id]
                    if math.dist(s[end],p)<=self.tolerance:found.append((s,end))
        return sorted(found,key=lambda entry:(entry[0]['id'],entry[1]))


def terminal_arrow(graph, tip, incoming):
    """Two backward wings on opposite sides of incoming direction, any rotation."""
    vector=sub(tip,incoming);length=math.hypot(*vector)
    if not length:return None
    u=[v/length for v in vector];wings=[]
    for s,end in graph.incident(tip):
        if not 2<s['length_pt']<10:continue
        other=s['b' if end=='a' else 'a'];delta=sub(other,tip)
        along=dot(delta,u);side=cross(u,delta)
        if -10<along<-1 and .15<abs(side)<3:
            wings.append((side,s['id']))
    pairs=[sorted([a[1],b[1]]) for a in wings for b in wings if a[0]*b[0]<0]
    if not pairs:return None
    return sorted({id for pair in pairs for id in pair})


def shoulder_candidates(occurrence,texts,segments):
    """Only nominate a text-aligned shoulder. Its complete route is still required."""
    selected={id for id in occurrence['text_ids']};parts=[t for t in texts if t['id'] in selected]
    result=[]
    # Each source line matters: length may be printed on the other side of a
    # vertical shoulder, so the union bbox alone loses the true baseline.
    for s in segments:
        if s['length_pt']<12:continue
        d=sub(s['b'],s['a']);u=occurrence['direction']
        if abs(cross(d,u))>.2:continue
        projections=[local_box([p[0],p[1],p[0],p[1]],u) for p in (s['a'],s['b'])]
        lo=min(p[0] for p in projections);hi=max(p[2] for p in projections);v=projections[0][1]
        evidence=[]
        for t in parts:
            box=local_box(t['bbox'],u);overlap=max(0,min(hi,box[2])-max(lo,box[0]))
            if -3.5<=v-box[3]<=5.5 and overlap>=.65*(box[2]-box[0]):
                evidence.append(dict(text_id=t['id'],baseline_gap_pt=v-box[3],overlap_pt=overlap))
        if evidence:result.append(dict(segment=s,text_alignment=evidence))
    return sorted(result,key=lambda r:r['segment']['id'])


def proper_crossings(path_segments,segments):
    """Report crossings without treating them as changes of leader destination."""
    own={s['id'] for s in path_segments};result=[]
    for a in path_segments:
        r=sub(a['b'],a['a'])
        for b in segments:
            if b['id'] in own or b['length_pt']<2:continue
            s=sub(b['b'],b['a']);den=cross(r,s)
            if abs(den)<1e-6:continue
            delta=sub(b['a'],a['a']);t=cross(delta,s)/den;u=cross(delta,r)/den
            if 1e-5<t<1-1e-5 and 1e-5<u<1-1e-5:
                result.append(dict(leader_segment_id=a['id'],other_segment_id=b['id'],
                                   point=[a['a'][0]+t*r[0],a['a'][1]+t*r[1]],behavior='CROSSED_WITHOUT_SWITCHING'))
    return result


def trace_leaders(occurrence,data,graph,max_segments=8,max_length=600,max_states=256):
    traces=[];states=0;limits=[];markers=junctions(data['paths'])
    for shoulder in shoulder_candidates(occurrence,data['texts'],data['segments']):
        start=shoulder['segment']
        for end in ('a','b'):
            stack=[([start],start[end],start['b' if end=='a' else 'a'],start['length_pt'])]
            while stack:
                path,tip,previous,total=stack.pop();states+=1
                if states>max_states:
                    limits.append('STATE_LIMIT');stack.clear();break
                wings=terminal_arrow(graph,tip,previous)
                terminal_markers=[p['id'] for p in markers if math.dist(center(p['bbox']),tip)<.3]
                if wings or terminal_markers:
                    traces.append(dict(segments=path,segment_ids=[s['id'] for s in path],
                        shoulder_id=start['id'],text_alignment=shoulder['text_alignment'],tip=tip,
                        terminal_kind='TWO_WING_ARROW' if wings else 'CIRCULAR_MARKER',terminal_entity_ids=wings or terminal_markers,
                        crossings=proper_crossings(path,data['segments']),length_pt=total))
                    continue
                ids={s['id'] for s in path}
                next_edges=[(s,e) for s,e in graph.incident(tip) if s['id'] not in ids]
                for s,e in next_edges:
                    if len(path)>=max_segments:limits.append('SEGMENT_LIMIT');continue
                    if total+s['length_pt']>max_length:limits.append('LENGTH_LIMIT');continue
                    stack.append((path+[s],s['b' if e=='a' else 'a'],tip,total+s['length_pt']))
            if states>max_states:break
        if states>max_states:break
    # Same route traversed from an internal text line is not silently collapsed
    # with another shoulder; distinct routes remain alternatives for review.
    unique={tuple(t['segment_ids']):t for t in traces}
    return dict(traces=list(unique.values()),search_limits=sorted(set(limits)),states=states)


def point_on_line(point,line,tolerance=.2):
    a,b=line['a'],line['b'];v=sub(b,a);length=math.hypot(*v)
    if not length:return False
    t=dot(sub(point,a),v)/(length*length)
    return -.001<=t<=1.001 and abs(cross(sub(point,a),v))/length<=tolerance


def terminal_contact(trace,line,max_extension=2,max_offset=1.5):
    """Bounded intersection of terminal shaft direction with target centerline.

    PDF arrow tips need not exactly equal the target centerline. Keep both raw
    coordinates and the proposed contact; never move or snap source entities.
    All destinations within this explicit bound survive, not just the nearest.
    """
    tip=trace['tip'];last=trace['segments'][-1]
    previous=last['b'] if math.dist(last['a'],tip)<.2 else last['a']
    shaft=sub(tip,previous);length=math.hypot(*shaft)
    if not length:return None
    u=[v/length for v in shaft];v=sub(line['b'],line['a']);den=cross(u,v)
    if abs(den)<1e-6:return None
    delta=sub(line['a'],tip);extension=cross(delta,v)/den;t=cross(delta,u)/den
    offset=abs(cross(sub(tip,line['a']),v))/line['length_pt']
    if abs(extension)>max_extension or offset>max_offset or not -.001<=t<=1.001:return None
    return dict(raw_tip=tip,centerline_contact=[tip[0]+extension*u[0],tip[1]+extension*u[1]],
                shaft_extension_pt=extension,tip_centerline_offset_pt=offset,
                mode='EXACT_CENTERLINE' if offset<.05 else 'BOUNDED_TERMINAL_SHAFT_INTERSECTION')


def localized_group(target,lines,max_separation=4):
    """A directly targeted line plus adjacent equal-extent parallel strokes.

    These are graphical strokes, never a count of physical bars or proof of 2x3.
    Do not jump to a remote symmetric group on the other side of an opening.
    """
    k=target['orientation'];j=1-k;lo,hi=sorted([target['a'][k],target['b'][k]])
    members=[]
    for line in lines:
        if line['orientation']!=k:continue
        l,h=sorted([line['a'][k],line['b'][k]])
        if abs(l-lo)<=.3 and abs(h-hi)<=.3 and abs(line['a'][j]-target['a'][j])<=max_separation:
            members.append(line)
    return sorted(members,key=lambda s:s['id'])


def resolve_trace(occurrence,trace,lines,axes,markers,scale=50):
    excluded=set(trace['segment_ids'])|set(trace['terminal_entity_ids']);candidates=[]
    nominal=occurrence['call']['nominal_length_cm']
    for line in lines:
        if line['length_pt']<8 or excluded.intersection(line['source_ids']):continue
        contact=terminal_contact(trace,line)
        if contact is None:continue
        distributions=[]
        for axis in axes:
            point=bar_axis_intersection(line,axis)
            if point is None:continue
            ids=[p['id'] for p in markers if math.dist(center(p['bbox']),point)<.42]
            if ids:distributions.append(dict(axis=axis,junction_path_ids=ids,intersection_pt=point,
                                             region_pdf_pt=graphic_envelope(line,axis)))
        group=localized_group(line,lines)
        projected=line['length_pt']*2.54/72*scale
        contradiction=bool(nominal and projected>nominal*1.05)
        exact=bool(nominal and abs(projected-nominal)/nominal<.015)
        evidence=dict(trace=trace,target=line,terminal_contact=contact,graphic_group=group,distribution_candidates=distributions,
                      localized_scope='DIRECTLY_TARGETED_STROKES_ONLY; NOT_FULL_PHYSICAL_GROUP',
                      nominal_projection_cm=projected,projection_exceeds_nominal=contradiction,
                      length_agreement_auxiliary=exact,multiplicity_geometry='NOT_INFERRED_FROM_PRINTED_FACTORS')
        if len(distributions)==1:
            evidence.update(representation_kind='DISTRIBUTED',sufficient=not contradiction,
                            region_pdf_pt=distributions[0]['region_pdf_pt'])
        elif len(distributions)>1:
            evidence.update(representation_kind='INCONCLUSIVE',sufficient=False,region_pdf_pt=None)
        elif occurrence['call']['spacing_cm'] is None and (len(group)>=2 or exact):
            evidence.update(representation_kind='LOCALIZED',sufficient=not contradiction,region_pdf_pt=None)
        else:
            evidence.update(representation_kind='INCONCLUSIVE',sufficient=False,region_pdf_pt=None)
        candidates.append(evidence)
    return candidates


def enrich_with_leaders(result,data):
    graph=EndpointGraph(data['segments']);lines=line_geometry(data['segments'])
    axes=distribution_axes(lines,data['segments']);markers=junctions(data['paths'])
    for o in result['occurrences']:
        o['previous_interpretation']=dict(status=o['status'],reason=o['reason'])
        o['representation_kind']='DISTRIBUTED' if o['status']=='ASSOCIATED' else 'INCONCLUSIVE'
        o['leader_candidates']=[];o['leader_association']=None;o['associated_lines']=[]
        if o['status']=='ASSOCIATED':
            o['associated_lines']=[o['associations'][0]['bar']]
            o['stage3_reason']='BASELINE_COMPLETE_PRESERVED';continue
        traced=trace_leaders(o,data,graph);o['leader_search']=traced
        resolved=[];unresolved_routes=[]
        for trace in traced['traces']:
            destinations=resolve_trace(o,trace,lines,axes,markers,result['layout']['scale_denominator'])
            resolved.extend(destinations)
            if not destinations:unresolved_routes.append(trace['segment_ids'])
        o['leader_candidates']=resolved
        o['unresolved_terminal_routes']=unresolved_routes
        # Same graphic group reached by distinct complete routes is still reviewable,
        # but any different target or interrupted/limited search blocks acceptance.
        if len(traced['traces'])>1 or len(resolved)>1 or any(len(c['distribution_candidates'])>1 or c['projection_exceeds_nominal'] for c in resolved):
            o.update(status='AMBIGUOUS',reason='LEADER_MULTIPLE_DESTINATIONS_OR_CONTRADICTORY_TARGET',region_pdf_pt=None)
        elif len(resolved)==1 and resolved[0]['sufficient'] and o['call']['parse_complete'] and not o['continuation_alternatives'] and not traced['search_limits']:
            c=resolved[0]
            o.update(status='ASSOCIATED',reason='COMPLETE_LEADER_ROUTE_AND_SUPPORTED_TARGET',
                     representation_kind=c['representation_kind'],region_pdf_pt=c['region_pdf_pt'],
                     leader_association=c,associated_lines=c['graphic_group'] if c['representation_kind']=='LOCALIZED' else [c['target']])
        elif traced['traces']:
            o.update(status='PARTIAL' if o['status']!='AMBIGUOUS' else 'AMBIGUOUS',
                     reason='LEADER_TRACED_WITHOUT_UNIQUE_SUPPORTED_REPRESENTATION',region_pdf_pt=None)
        o['stage3_reason']=o['reason']
    claims=defaultdict(list)
    for o in result['occurrences']:
        if o['status']=='ASSOCIATED':
            for line in o['associated_lines']:
                for id in line.get('source_ids',[line['id']]):claims[id].append(o)
    conflicts=defaultdict(set)
    for owners in claims.values():
        ids={o['occurrence_id'] for o in owners}
        if len(ids)>1:
            for o in owners:conflicts[o['occurrence_id']].update(ids-{o['occurrence_id']})
    for o in result['occurrences']:
        if o['occurrence_id'] in conflicts:
            o['shared_target_representations']=sorted(conflicts[o['occurrence_id']])
            if o['previous_interpretation']['status']!='ASSOCIATED':
                o.update(status='AMBIGUOUS',reason='LEADER_TARGET_SHARED_WITH_ANOTHER_REPRESENTATION',
                    representation_kind='INCONCLUSIVE',region_pdf_pt=None,leader_association=None,associated_lines=[])
                o['stage3_reason']=o['reason']
    counts=Counter(o['status'] for o in result['occurrences'])
    result['status_counts']={s:counts.get(s,0) for s in ('ASSOCIATED','PARTIAL','AMBIGUOUS','UNRESOLVED')}
    result['representation_counts']=dict(Counter(o['representation_kind'] for o in result['occurrences']))
    return result


def read_sheet_with_leaders(data,layout):
    return enrich_with_leaders(read_sheet(data,layout),data)


def compare_previous(current,previous):
    old={o['occurrence_id']:o for o in previous['occurrences']};changes=[];preserved=[]
    for o in current['occurrences']:
        prior=old[o['occurrence_id']]
        if o['status']!=prior['status']:
            changes.append(dict(display_id=o['display_id'],occurrence_id=o['occurrence_id'],mark=o['documentary_mark'],
                                before=prior['status'],after=o['status'],representation_kind=o['representation_kind'],reason=o['reason']))
        if prior['status']=='ASSOCIATED':
            unchanged=o['status']==prior['status'] and o['region_pdf_pt']==prior['region_pdf_pt'] and o['associations']==prior['associations']
            preserved.append(dict(display_id=o['display_id'],occurrence_id=o['occurrence_id'],exact_geometry_preserved=unchanged))
    return dict(before_counts=previous['status_counts'],after_counts=current['status_counts'],changes=changes,
                baseline_complete_associations=preserved)
