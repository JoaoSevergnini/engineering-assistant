"""Stage 8 source-only contour recognition. No reference profile or slab-ID rules.

ROI is a context selector, not a guillotine for whole crossing vector entities.
Faces stay candidates even when geometrically closed or visually plausible.
"""
import hashlib
import json
from polygonal_slabs import (Point,LineString,Polygon,box,geo,unary_union,polygonize_full,
    excluded_entities,boundary_evidence)
from automatic import center,union,line_geometry,distribution_axes
from review_slab_contours import label_block,label_links


def context_segments(segments,roi,minimum_inside_fraction=.8):
    """Retain complete source entities, recording context-boundary crossings.

    At least 80% inside suppresses long sheet grid/table lines. It is a declared
    experimental layout parameter, not a structural or closure tolerance.
    """
    if not 0<minimum_inside_fraction<=1:raise ValueError('Invalid ROI fraction')
    window=box(*roi);kept=[];crossings=[];dropped=[]
    for s in sorted(segments,key=lambda e:e['id']):
        line=LineString([s['a'],s['b']])
        if line.length==0:continue
        fraction=line.intersection(window).length/line.length
        if fraction+1e-12<minimum_inside_fraction:
            if fraction>0:dropped.append({'segment_id':s['id'],'inside_fraction':fraction,'reason':'LONG_LAYOUT_CROSSING_CONTEXT_FILTER'})
            continue
        kept.append(s)
        if fraction<1-1e-12:crossings.append({'segment_id':s['id'],'original_a':s['a'],'original_b':s['b'],
            'inside_fraction':fraction,'action':'COMPLETE_SOURCE_SEGMENT_RETAINED_NO_CLIPPING'})
    return kept,crossings,dropped


def recognize(inventory,data,minimum_inside_fraction=.8):
    """Inventory provides raw association exclusions and documentary slab labels only.

    It does not consume prior contour candidates, human contour vertices, images,
    region composition classes, or reference matching metrics.
    """
    roi=inventory['layout']['detail_roi_pt'];labels=inventory['structural_interpretation']['slabs']
    selected,crossings,dropped=context_segments(data['segments'],roi,minimum_inside_fraction)
    excluded=excluded_entities(inventory)
    context_box=union([roi]+[[*s['a'],*s['a']] for s in selected]+[[*s['b'],*s['b']] for s in selected])
    support=boundary_evidence({'segments':selected},context_box,excluded);strong={e['id'] for e in support}
    axes=distribution_axes(line_geometry(data['segments']),data['segments']);annotation={id for a in axes for id in a.get('source_ids',[a['id']])}
    links={s['id']:label_links(s,data['texts'],[e for e in selected if e['id'] not in excluded]) for s in labels}
    pointers={l['segment_id'] for entries in links.values() for l in entries}
    edges=[s for s in selected if s['id'] not in excluded|pointers and (s['id'] not in annotation or s['id'] in strong)
           and (s['a'][0]==s['b'][0] or s['a'][1]==s['b'][1]) and LineString([s['a'],s['b']]).length>=2]
    lines=[LineString([s['a'],s['b']]) for s in edges]
    network=unary_union(lines);parts=list(network.geoms) if hasattr(network,'geoms') else [network]
    faces,cuts,dangles,invalid=polygonize_full(parts)
    face_records=[]
    for face in faces.geoms:
        owners=[];link_evidence=[]
        for s in labels:
            if face.contains(Point(center(s['label']['bbox']))):
                owners.append(s['id']);link_evidence.append({'label_id':s['id'],'basis':'DOCUMENTARY_LABEL_INSIDE_FACE'})
            else:
                landed=[l for l in links[s['id']] if face.contains(Point(l['target']))]
                if landed:owners.append(s['id']);link_evidence.append({'label_id':s['id'],'basis':'FULL_NAME_THICKNESS_BLOCK_POINTER','links':landed})
        if not owners:continue
        ids=sorted(s['id'] for s,l in zip(edges,lines) if face.boundary.intersection(l).length>1e-7)
        positive=[e for e in support if e['id'] in ids]
        supported=unary_union([LineString([e['a'],e['b']]).intersection(face.boundary) for e in positive]).length
        if not positive and not any(e['basis']=='FULL_NAME_THICKNESS_BLOCK_POINTER' for e in link_evidence):continue
        geometry=geo(face);id='CX-'+hashlib.sha256(json.dumps(geometry,sort_keys=True).encode()).hexdigest()[:12]
        face_records.append({'id':id,'geometry_pdf_pt':geometry,'area_pt2':face.area,'bbox':list(face.bounds),
            'label_ids':sorted(owners),'label_evidence':link_evidence,'boundary_segment_ids':ids,
            'hatch_supported_segment_ids':[e['id'] for e in positive],'hatch_supported_perimeter_fraction':supported/face.length,
            'crossing_roi_segment_ids':sorted(set(ids)&{e['segment_id'] for e in crossings}),
            'concavity_area_ratio':face.area/face.convex_hull.area,'exterior_vertices':len(face.exterior.coords)-1,
            'graphic_interior_rings':len(face.interiors),'interior_ring_semantics':'GRAPHIC_VOIDS_NOT_CONFIRMED_STRUCTURAL_OPENINGS',
            'thin_border_review_flag':face.area/face.convex_hull.area<.35,
            'status':'CANDIDATE_REQUIRES_ENGINEER_REVIEW' if len(owners)==1 else 'AMBIGUOUS_MULTIPLE_LABELS',
            'engineer_confirmed':False,'synthetic_closure_segments':[],'source_coordinates_modified':False})
    face_records.sort(key=lambda c:c['id']);slabs=[]
    for s in sorted(labels,key=lambda s:(s['name'],s['id'])):
        matches=[c for c in face_records if s['id'] in c['label_ids']]
        slabs.append({'label_id':s['id'],'name':s['name'],'thickness_cm':s['thickness_cm'],
            'candidates':matches,'state':'UNIQUE_CANDIDATE_NOT_CONFIRMED' if len(matches)==1 and len(matches[0]['label_ids'])==1 else ('AMBIGUOUS' if matches else 'UNRESOLVED'),
            'label_block_pdf_pt':label_block(s,data['texts']),'engineer_confirmed':False})
    return {'slabs':slabs,'candidates':face_records,'linework':edges,'positive_boundary_evidence':support,
        'context_audit':{'roi_pdf_pt':roi,'minimum_inside_fraction':minimum_inside_fraction,'retained_crossings':crossings,'rejected_layout_crossings':dropped},
        'network':{'faces':len(faces.geoms),'cuts':len(cuts.geoms),'dangles':len(dangles.geoms),'invalid_rings':len(invalid.geoms),
                   'dangling_geometry_pdf_pt':geo(dangles),'gap_closure_used':False,'snapping':False},
        'metrics':{'documentary_labels':len(slabs),'unique_candidate_labels':sum(s['state']=='UNIQUE_CANDIDATE_NOT_CONFIRMED' for s in slabs),
                   'ambiguous_labels':sum(s['state']=='AMBIGUOUS' for s in slabs),'unresolved_labels':sum(s['state']=='UNRESOLVED' for s in slabs),'automatically_validated':0},
        'reference_used_for_recognition':False,'steel_or_resistance_calculations':False}
