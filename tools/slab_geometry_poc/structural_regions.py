"""Stage 6: conservative documentary interpretation, never a resistance engine.

Thresholds below only generate review candidates. Human confirmations are bound
to source + geometry fingerprints, not to composition IDs in classifier code.
"""
import copy
import hashlib
import itertools
import json
import re
from collections import Counter
from automatic import center,contains
from distributed_regions import area,intersection,partition,polygon
from opening_groups import covered_edge

CATEGORIES={'BASE_PLUS_REINFORCEMENT','LAP_SPLICE','GRAPHICAL_RESIDUAL','UNDETERMINED'}
CRITERIA={'narrow_pt':4.0,'small_fraction':.04,'endpoint_distance_pt':4.0,
          'equivalent_spacing_relative':.05,'text_to_bar_pt':9.0,'contour_tolerance_pt':.25}


def fingerprint(c):
    """Stable under display ID/order changes; stale geometry invalidates a review."""
    payload={'polygon':c['polygon_pdf_pt'],'contributors':sorted(
        ({k:r.get(k) for k in ('position','occurrence_id','orientation','diameter_mm','spacing_cm','layer')} for r in c['contributors']),
        key=lambda r:(r['occurrence_id'],r['position']))}
    return hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def detect_slabs(texts,segments,roi,excluded_ids=()):
    """Typography pairs name/thickness; contours require four supported sides.

    Only nearest surrounding non-reinforcement lines are investigated. This is a
    deliberately incomplete rectangular contour detector, not a formwork reader.
    """
    names=[t for t in texts if re.fullmatch(r'L\d+',t['text'].strip(),re.I) and contains(roi,center(t['bbox']))]
    thickness=[(t,re.fullmatch(r'h\s*[:=]\s*(\d+(?:[.,]\d+)?)',t['text'].strip(),re.I)) for t in texts]
    lines=[s for s in segments if s['id'] not in excluded_ids and
           s['a']!=s['b'] and
           (s['a'][0]==s['b'][0] or s['a'][1]==s['b'][1]) and
           contains(roi,s['a']) and contains(roi,s['b'])]
    slabs=[]
    for t in sorted(names,key=lambda t:(t['text'],t['id'])):
        b=t['bbox'];cx,cy=center(b)
        hs=[(h,m) for h,m in thickness if m and h['bbox'][0]<b[2] and h['bbox'][2]>b[0] and 0<center(h['bbox'])[1]-cy<2*(b[3]-b[1])]
        candidates=[];sides=[set() for _ in range(4)]
        for s in lines:
            a,z=s['a'],s['b']
            if a[0]==z[0] and min(a[1],z[1])<=cy<=max(a[1],z[1]):
                if a[0]<b[0]:sides[0].add(a[0])
                if a[0]>b[2]:sides[2].add(a[0])
            if a[1]==z[1] and min(a[0],z[0])<=cx<=max(a[0],z[0]):
                if a[1]<b[1]:sides[1].add(a[1])
                if a[1]>b[3]:sides[3].add(a[1])
        # No joining across unproved gaps: nearest three bounding coordinates only.
        options=[sorted(v,reverse=i in (0,1))[:3] for i,v in enumerate(sides)]
        for box in itertools.product(*options):
            p=polygon(box)
            if any(n['id']!=t['id'] and contains(box,center(n['bbox'])) for n in names):continue
            if len(hs)==1 and not contains(box,center(hs[0][0]['bbox'])):continue
            edges=[covered_edge(lines,a,z,tolerance=CRITERIA['contour_tolerance_pt']) for a,z in zip(p,p[1:]+p[:1])]
            if all(e['complete'] for e in edges):candidates.append({'bbox':list(box),'polygon_pdf_pt':p,'edge_evidence':edges})
        candidates.sort(key=lambda c:(area(c['bbox']),c['bbox']))
        # Nested rectangles may be beam faces; retain alternatives, no nearest choice.
        chosen=candidates[0] if len(candidates)==1 else None
        slabs.append({'id':t['id'],'name':t['text'],'label':copy.deepcopy(t),
            'thickness_cm':float(hs[0][1][1].replace(',','.')) if len(hs)==1 else None,
            'thickness_sources':[h['id'] for h,m in hs],
            'documentary_state':'NAME_AND_THICKNESS_EXTRACTED' if len(hs)==1 else 'THICKNESS_PENDING',
            'contour_state':'PRELIMINARY_FOUR_SIDED_GRAPHIC_CONTOUR' if chosen else ('AMBIGUOUS_CONTOURS' if candidates else 'CONTOUR_PENDING'),
            'contour':chosen,'contour_alternatives':candidates,'engineer_validated':False,
            'formwork_substitute':False,'region_relations':[]})
    return slabs


def relate_slabs(slabs,regions):
    for s in slabs:
        s['region_relations']=[]
        if not s['contour']:continue
        for r in regions:
            b=intersection(s['contour']['bbox'],r['bbox'])
            if b:s['region_relations'].append({'region_id':r['id'],'intersection_pdf_pt':polygon(b),'area_pt2':area(b),'fraction_of_region':area(b)/r['area_pt2'],'state':'PRELIMINARY_GEOMETRIC_INTERSECTION'})
    return slabs


def coverage(reinforcement,bases):
    """Exact covered/uncovered pieces; bases may cover jointly, never double-count."""
    target=dict(id='@target',bbox=reinforcement['bbox'])
    cells=partition([target]+[{'id':'@base'+str(i),'bbox':b['bbox']} for i,b in enumerate(bases)])
    own=[c for c in cells if '@target' in c['region_ids']]
    covered=[c for c in own if len(c['region_ids'])>1];uncovered=[c for c in own if len(c['region_ids'])==1]
    return {'reinforcement_id':reinforcement['id'],'base_region_ids':[b['id'] for b in bases],
        'covered_area_pt2':sum(c['area_pt2'] for c in covered),'uncovered_area_pt2':sum(c['area_pt2'] for c in uncovered),
        'uncovered_polygons_pdf_pt':[c['polygon_pdf_pt'] for c in uncovered],
        'state':'NO_COMPATIBLE_BASE_IDENTIFIED' if not bases else ('GRAPHICALLY_COVERED' if not uncovered else 'GRAPHICALLY_UNCOVERED'),
        'layer_compatibility_confirmed':False,'structural_insufficiency_proved':False,
        'small_difference_review':bool(uncovered) and sum(c['area_pt2'] for c in uncovered)/reinforcement['area_pt2']<CRITERIA['small_fraction']}


def roles(regions,texts):
    """Function hints require geometric support; office words are optional evidence."""
    result=[]
    for r in regions:
        k=r['orientation'];j=1-k;coordinate=r['bar']['a'][j]
        nearby=[t for t in texts if (t['text'].strip().upper()=='(BASE)' or t['text'].strip().upper().startswith('(REFOR')) and
                abs(center(t['bbox'])[j]-coordinate)<CRITERIA['text_to_bar_pt'] and r['bbox'][k]<=center(t['bbox'])[k]<=r['bbox'][k+2]]
        words={'BASE' if t['text'].upper()=='(BASE)' else 'REINFORCEMENT' for t in nearby}
        bigger=[];smaller=[]
        for other in regions:
            if r['id']==other['id'] or k!=other['orientation']:continue
            b=intersection(r['bbox'],other['bbox'])
            if not b:continue
            if other['area_pt2']>r['area_pt2']*1.5 and area(b)/r['area_pt2']>.3:bigger.append(other['id'])
            if r['area_pt2']>other['area_pt2']*1.5 and area(b)/other['area_pt2']>.3:smaller.append(other['id'])
        geometric=[]
        if bigger:geometric.append('REINFORCEMENT')
        if smaller:geometric.append('BASE')
        candidates=sorted(words.intersection(geometric) if words else set(geometric))
        role=candidates[0] if len(candidates)==1 else 'UNKNOWN'
        result.append({'region_id':r['id'],'role_candidate':role,'confirmed':False,'documentary_words':sorted(words),
            'text_ids':[t['id'] for t in nearby],'larger_overlapping_regions':bigger,'smaller_overlapping_regions':smaller,
            'basis':'GEOMETRIC_EXTENT_AND_OPTIONAL_DOCUMENTARY_WORDS','alternatives':candidates})
    return result


def automatic_interpretation(c,members,role_map):
    """Evidence proposals remain UNDETERMINED without documentary confirmation."""
    if len(c['identity_groups'])==1:return {'classification':'SINGLE_DISTRIBUTED','proposals':[],'evidence':{}}
    b=c['bbox'];dims=[b[2]-b[0],b[3]-b[1]];same=len({r['orientation'] for r in members})==1
    fractions=[c['area_pt2']/r['area_pt2'] for r in members]
    endpoints=[min(abs(b[1-r['orientation']]-r['bbox'][1-r['orientation']]),abs(b[3-r['orientation']]-r['bbox'][3-r['orientation']]))<=CRITERIA['endpoint_distance_pt'] for r in members]
    narrow=min(dims)<=CRITERIA['narrow_pt'];small=max(fractions)<CRITERIA['small_fraction']
    # Bar ends along the longitudinal direction, not ends of distribution axes.
    end_pairs=[];equivalent=[];bar_offsets=[]
    for a,z in itertools.combinations(members,2):
        k=a['orientation'];ab=a['bbox'];zb=z['bbox'];overlap=intersection(ab,zb)
        if same:bar_offsets.append({'regions':[a['id'],z['id']],'transverse_bar_offset_pt':abs(a['bar']['a'][1-k]-z['bar']['a'][1-k]),'collinearity_confirmed':a['bar']['a'][1-k]==z['bar']['a'][1-k]})
        opposite=ab[k]<zb[k]<ab[k+2]<zb[k+2] or zb[k]<ab[k]<zb[k+2]<ab[k+2]
        if same and overlap and opposite and overlap[k+2]-overlap[k]<min(a['longitudinal_extent_pt'],z['longitudinal_extent_pt'])/2:end_pairs.append([a['id'],z['id']])
        sa,sz=a['spacing_cm'],z['spacing_cm']
        if same and a['diameter_mm']==z['diameter_mm'] and sa and sz and abs(sa-sz)/max(sa,sz)<=CRITERIA['equivalent_spacing_relative']:equivalent.append([a['id'],z['id']])
    present={role_map[r['id']]['role_candidate'] for r in members};proposals=[]
    if same and {'BASE','REINFORCEMENT'}<=present:proposals.append('BASE_PLUS_REINFORCEMENT')
    if end_pairs:proposals.append('LAP_SPLICE')
    if narrow and small and sum(endpoints)>=2:proposals.append('GRAPHICAL_RESIDUAL')
    return {'classification':'UNDETERMINED','proposals':proposals,'evidence':{'same_direction':same,'dimensions_pt':dims,'fractions_of_members':fractions,
        'near_distribution_ends':endpoints,'longitudinal_end_overlap_pairs':end_pairs,'equivalent_diameter_spacing_pairs':equivalent,'representative_bar_offsets':bar_offsets,
        'neighbor_context_required':True,'layer_and_physical_identity_unconfirmed':True}}


def adjacent(a,b):
    return ((a[2]==b[0] or b[2]==a[0]) and min(a[3],b[3])>max(a[1],b[1])) or ((a[3]==b[1] or b[3]==a[1]) and min(a[2],b[2])>max(a[0],b[0]))


def consolidate(cells,interpretations):
    """Connected rectangle covers, never bounding boxes across gaps or voids."""
    imap={i['composition_id']:i for i in interpretations};remaining={c['id']:c for c in cells};groups=[]
    while remaining:
        first=remaining.pop(sorted(remaining)[0]);stack=[first];component=[first]
        def key(c):
            i=imap[c['id']]
            return (i['classification'],i['validation_state'],tuple(c['identity_groups']))
        while stack:
            current=stack.pop()
            for id,c in list(remaining.items()):
                if key(c)==key(first) and adjacent(current['bbox'],c['bbox']):
                    remaining.pop(id);component.append(c);stack.append(c)
        groups.append({'id':f'S{len(groups)+1:03d}','classification':imap[first['id']]['classification'],
            'validation_state':imap[first['id']]['validation_state'],
            'composition_ids':sorted(c['id'] for c in component),'occurrences':sorted({o for c in component for o in c['occurrences']}),
            'individual_region_ids':sorted({id for c in component for id in c.get('region_ids',[])}),
            'identity_groups':first['identity_groups'],'polygon_parts_pdf_pt':[c['polygon_pdf_pt'] for c in component],
            'area_pt2':sum(c['area_pt2'] for c in component),'continuity':'SHARED_EDGE_POSITIVE_LENGTH' if len(component)>1 else 'SINGLE_PART',
            'effective_resistant_contributions':None,'resistant_use_authorized':False,
            'pending':'Physical identity, layer compatibility and structural domain require confirmation'})
    return groups


def interpret(inventory,data,reviews=None):
    result=copy.deepcopy(inventory);a=inventory['distributed_spatial_analysis'];regions=a['regions'];cells=a['composition_regions'];lookup={r['id']:r for r in regions}
    excluded=set()
    def collect(x):
        if isinstance(x,dict):
            excluded.update(x.get('source_ids',[]))
            for v in x.values():collect(v)
        elif isinstance(x,list):
            for v in x:collect(v)
    collect(inventory['occurrences'])
    slab_inventory=relate_slabs(detect_slabs(data['texts'],data['segments'],inventory['layout']['detail_roi_pt'],excluded),regions)
    functions=roles(regions,data['texts']);fmap={r['region_id']:r for r in functions};interpretations=[];unused=copy.deepcopy((reviews or {}).get('reviews',[]));review_errors=[]
    source_sha=inventory.get('stage5_provenance',{}).get('sha256')
    for c in cells:
        members=[lookup[id] for id in c['region_ids']];auto=automatic_interpretation(c,members,fmap)
        matches=[r for r in unused if source_sha and r.get('fingerprint')==fingerprint(c) and r.get('source_sha256')==source_sha]
        confirmation=None
        if len(matches)==1 and matches[0].get('classification') in CATEGORIES and matches[0].get('reviewer'):
            confirmation=matches[0];unused.remove(confirmation)
        elif matches:review_errors.append({'composition_id':c['id'],'reason':'CONFLICTING_OR_INVALID_REVIEWS'})
        interpretations.append({'composition_id':c['id'],'fingerprint':fingerprint(c),'automatic':auto,
            'classification':confirmation['classification'] if confirmation else auto['classification'],
            'validation_state':'ENGINEER_CONFIRMED' if confirmation else 'PENDING_ENGINEER_REVIEW',
            'human_confirmation':confirmation,'physical_addition_authorized':False,
            'lap_steel_summation_blocked':True,'effective_contributions':None})
        interpretations[-1]['resistant_membership_state']={
            'LAP_SPLICE':'NO_INDEPENDENT_ADDITION_FOR_OVERLAPPED_BARS',
            'GRAPHICAL_RESIDUAL':'GRAPHIC_OVERLAP_NOT_RESISTANT_COMPOSITION; EFFECTIVE_NEIGHBOR_MEMBERSHIP_PENDING',
            'BASE_PLUS_REINFORCEMENT':'JOINT_FUNCTION_CONFIRMED_LOCALLY; LAYER_AND_IDENTITY_SCOPE_PENDING',
            'SINGLE_DISTRIBUTED':'SINGLE_GRAPHIC_IDENTITY; PHYSICAL_SCOPE_PENDING',
            'UNDETERMINED':'UNDETERMINED'}[interpretations[-1]['classification']]
    # Residual candidates also record adjacent constant-membership cells as context.
    for c,i in zip(cells,interpretations):
        if 'GRAPHICAL_RESIDUAL' in i['automatic']['proposals']:
            neighbors=[z for z in cells if z['id']!=c['id'] and adjacent(c['bbox'],z['bbox'])]
            continuous=[z['id'] for z in neighbors if set(z['identity_groups'])<set(c['identity_groups'])]
            i['automatic']['evidence']['neighbor_compositions']=[z['id'] for z in neighbors]
            i['automatic']['evidence']['continuous_neighbors_with_subset_membership']=continuous
            if not continuous:i['automatic']['proposals'].remove('GRAPHICAL_RESIDUAL')
    checks=[]
    for f in functions:
        if f['role_candidate']!='REINFORCEMENT':continue
        r=lookup[f['region_id']];bases=[z for z in regions if fmap[z['id']]['role_candidate']=='BASE' and z['orientation']==r['orientation'] and (r.get('layer') is None or z.get('layer') is None or r['layer']==z['layer']) and intersection(z['bbox'],r['bbox'])]
        check=coverage(r,bases);check['function_state']='PROVISIONAL_FUNCTION_CANDIDATE';checks.append(check)
    consolidated=consolidate(cells,interpretations);imap={i['composition_id']:i for i in interpretations}
    for slab in slab_inventory:
        rr={r['region_id'] for r in slab['region_relations']}
        slab['base_region_candidates']=[f['region_id'] for f in functions if f['region_id'] in rr and f['role_candidate']=='BASE']
        slab['reinforcement_region_candidates']=[f['region_id'] for f in functions if f['region_id'] in rr and f['role_candidate']=='REINFORCEMENT']
        slab['compositions_by_classification']={key:[] for key in sorted(CATEGORIES|{'SINGLE_DISTRIBUTED'})}
        slab['association_state']='PRELIMINARY_CONTOUR_INTERSECTIONS_ONLY' if slab['contour'] else 'PENDING_CONTOUR_NO_REGION_ASSIGNMENT'
        if slab['contour']:
            for c in cells:
                if intersection(slab['contour']['bbox'],c['bbox']):slab['compositions_by_classification'].setdefault(imap[c['id']]['classification'],[]).append(c['id'])
    result['structural_interpretation']={'criteria':copy.deepcopy(CRITERIA),'slabs':slab_inventory,'function_candidates':functions,
        'overlap_interpretations':interpretations,'containment_checks':checks,'consolidated_regions':consolidated,
        'unmatched_reviews':unused,'review_errors':review_errors,'structural_calculations_performed':False,
        'metrics':{'slab_labels':len(slab_inventory),'preliminary_contours':sum(s['contour'] is not None for s in slab_inventory),
            'classifications':dict(Counter(i['classification'] for i in interpretations)),
            'human_confirmations':sum(i['validation_state']=='ENGINEER_CONFIRMED' for i in interpretations),
            'function_candidates':dict(Counter(f['role_candidate'] for f in functions)),
            'containment_states':dict(Counter(c['state'] for c in checks)),
            'consolidated_regions':len(consolidated),'resistant_use_authorized':False}}
    return result
