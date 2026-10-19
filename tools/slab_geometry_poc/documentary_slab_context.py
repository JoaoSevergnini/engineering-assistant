"""Documentary association contexts, explicitly NOT replacement slab contours.

Source-only patterns: double-faced U frames with documentary pointers, and
paired capped support strips continuing a candidate frontier. No slab/mark IDs,
color rules, nearest labels, hull filling or changes to source geometry.
"""
import hashlib
import json
from polygonal_slabs import shape, geo, box, LineString, unary_union

EPS = .001  # Numerical contact tolerance in PDF points; not an engineering tolerance.


def segment(e):return LineString([e['a'],e['b']])


def coverage(line, entries):
    return unary_union([segment(e).intersection(line) for e in entries]).length


def u_frame(candidate, edges):
    """Three complete exterior sides, inward parallel faces, explicit name pointer."""
    if not any(e['basis']=='FULL_NAME_THICKNESS_BLOCK_POINTER' for e in candidate['label_evidence']):return None
    g=shape(candidate['geometry_pdf_pt']);x0,y0,x1,y1=g.bounds
    if g.geom_type!='Polygon' or g.interiors:return None
    sides=[LineString([(x0,y0),(x1,y0)]),LineString([(x1,y0),(x1,y1)]),
           LineString([(x1,y1),(x0,y1)]),LineString([(x0,y1),(x0,y0)])]
    full=[i for i,s in enumerate(sides) if s.difference(g.boundary).length<=EPS]
    if len(full)!=3:return None
    source=[e for e in edges if e['id'] in candidate['boundary_segment_ids']]
    if any(coverage(sides[i],source)<sides[i].length-EPS for i in full):return None
    pairs=[]
    for i in full:
        side=sides[i];a,b=list(side.coords);k=1 if a[1]==b[1] else 0;axis=1-k
        inward=1 if a[k] in (x0 if k==0 else y0,) else -1
        low,high=sorted([a[axis],b[axis]])
        choices=[]
        for e in source:
            p,q=e['a'],e['b']
            if p[k]!=q[k]:continue
            distance=(p[k]-a[k])*inward
            overlap=max(0,min(high,max(p[axis],q[axis]))-max(low,min(p[axis],q[axis])))
            # Experimental frame shape filters, never acceptance by area alone.
            if EPS<distance<=.25*min(x1-x0,y1-y0) and overlap>=.65*side.length:
                choices.append(e['id'])
        if not choices:return None
        pairs.append({'side':i,'inward_parallel_source_ids':sorted(choices)})
    return {'geometry_pdf_pt':geo(box(x0,y0,x1,y1)),'basis':'DOCUMENTARY_POINTER_AND_THREE_DOUBLE_FACED_FRAME_SIDES',
        'source_segment_ids':sorted(e['id'] for e in source), 'parallel_face_evidence':pairs,
        'open_side':next(i for i in range(4) if i not in full),
        'interpretation':'ASSOCIATION_SEARCH_CONTEXT_ONLY; OPEN_FRONTIER_NOT_A_PROVED_SLAB_BOUNDARY'}


def support_continuations(candidate, edges):
    """Opposite capped double faces bracket candidate wall ends at a frontier.

    All four outward directions are examined. Matching support ends, not distance
    to text, define each continuation. Competing continuations remain alternatives.
    """
    original=shape(candidate['geometry_pdf_pt']);results=[]
    for swap in (False,True):
        for sign in (-1,1):
            def transform(p):
                a,b=(p[1],p[0]) if swap else p
                return (a,sign*b)
            def inverse(p):
                a,b=p[0],sign*p[1]
                return (b,a) if swap else (a,b)
            from shapely.affinity import affine_transform
            g=affine_transform(original,[0,1,sign,0,0,0] if swap else [1,0,0,sign,0,0])
            x0,y0,x1,front=g.bounds;width=x1-x0
            if width<=0:continue
            frontier=LineString([(x0,front),(x1,front)])
            if frontier.intersection(g.boundary).length<.8*width:continue
            transformed=[dict(e,a=transform(e['a']),b=transform(e['b'])) for e in edges]
            vertical=[]
            for e in transformed:
                a,b=e['a'],e['b']
                if a[0]!=b[0]:continue
                lo,hi=sorted([a[1],b[1]])
                if abs(lo-front)<=EPS and hi>front+EPS:vertical.append((e,hi))
            strips=[[],[]]
            for endpoint,index in [(x0,0),(x1,1)]:
                for left,stop in vertical:
                    for right,end in vertical:
                        l,r=left['a'][0],right['a'][0]
                        if not (l<=endpoint<=r and EPS<r-l<=.15*width and abs(stop-end)<=EPS):continue
                        caps=[LineString([(l,front),(r,front)]),LineString([(l,stop),(r,stop)])]
                        if any(coverage(c,transformed)<c.length-EPS for c in caps):continue
                        ids={left['id'],right['id']}
                        ids.update(e['id'] for e in transformed if any(segment(e).intersection(c).length>EPS for c in caps))
                        strips[index].append({'stop':stop,'ids':sorted(ids),'width_pt':r-l})
            for left in strips[0]:
                for right in strips[1]:
                    if abs(left['stop']-right['stop'])>EPS:continue
                    points=[inverse(p) for p in [(x0,front),(x1,front),(x1,left['stop']),(x0,left['stop'])]]
                    from polygonal_slabs import Polygon
                    results.append({'geometry_pdf_pt':geo(Polygon(points)),
                        'basis':'CONTINUATION_BETWEEN_OPPOSITE_CAPPED_DOUBLE_SUPPORT_FACES',
                        'source_segment_ids':sorted(set(left['ids']+right['ids'])),
                        'frontier_pdf_pt':[list(inverse((x0,front))),list(inverse((x1,front)))],
                        'interpretation':'SUPPORT_CONTEXT_ONLY; NOT_A_VALIDATED_SLAB_EXTENSION'})
    unique={}
    for r in results:
        key=json.dumps(r['geometry_pdf_pt'],sort_keys=True)
        if key in unique:r['source_segment_ids']=sorted(set(r['source_segment_ids']+unique[key]['source_segment_ids']))
        unique[key]=r
    return [unique[k] for k in sorted(unique)]


def build_contexts(inventory, domains):
    analysis=inventory['complex_slab_contour_analysis'];edges=analysis['linework']
    candidates={c['id']:c for c in analysis['candidates']}
    result=[]
    for d in sorted(domains,key=lambda d:d['id']):
        candidate=candidates[d['id']]
        evidence=[{'geometry_pdf_pt':d['geometry_pdf_pt'],'basis':'ORIGINAL_CANDIDATE_UNCHANGED',
            'source_segment_ids':candidate['boundary_segment_ids']}]
        u=u_frame(candidate,edges)
        if u:evidence.append(u)
        evidence.extend(support_continuations(candidate,edges))
        context=unary_union([shape(e['geometry_pdf_pt']) for e in evidence])
        result.append({'domain_id':d['id'],'slab':d['slab'],'thickness_cm':d['thickness_cm'],
            'geometry_pdf_pt':geo(context),'evidence':evidence,'documentary_sources':d['source'],
            'contour_confidence':'CONFIRMED' if d['confirmed'] else 'CANDIDATE_NOT_CONFIRMED',
            'contour_review_flag':d['review_flag'],'source_contour_modified':False,
            'context_id':'CTX-'+hashlib.sha256(json.dumps(geo(context),sort_keys=True).encode()).hexdigest()[:12],
            'not_for_structural_clipping_or_effective_depth':True})
    return sorted(result,key=lambda r:(r['slab'],r['domain_id']))
