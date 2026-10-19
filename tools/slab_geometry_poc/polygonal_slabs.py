"""Stage 7 polygonal candidates from evidenced linework, not a formwork reader."""
import hashlib
import json
import math
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tmp/slab_spatial_deps'))
try:
    import shapely
    from shapely.geometry import Point,LineString,Polygon,box,mapping,shape
    from shapely.ops import unary_union,polygonize_full
except ImportError as error:
    raise ImportError('Stage 7 needs isolated dependency: python -m pip install --target tmp/slab_spatial_deps --only-binary=:all: shapely==1.8.5.post1') from error
from automatic import center,contains,line_geometry,distribution_axes


def geo(g):
    """JSON geometry, canonical ring orientation/order independent of input order."""
    if g.is_empty:return {'type':'GeometryCollection','geometries':[]}
    def ring(coords):
        p=list(map(tuple,list(coords)[:-1]));options=[]
        for v in (p,list(reversed(p))):
            start=min(range(len(v)),key=lambda i:v[i]);w=v[start:]+v[:start];options.append(w)
        best=min(options);return [list(p) for p in best+[best[0]]]
    if g.geom_type=='Polygon':return {'type':'Polygon','coordinates':[ring(g.exterior.coords)]+sorted([ring(h.coords) for h in g.interiors])}
    if g.geom_type=='MultiPolygon':return {'type':'MultiPolygon','coordinates':sorted([geo(p)['coordinates'] for p in g.geoms])}
    if g.is_empty:return {'type':'GeometryCollection','geometries':[]}
    return json.loads(json.dumps(mapping(g)))


def polygons(g):
    if g.is_empty:return []
    if g.geom_type=='Polygon':return [g]
    if hasattr(g,'geoms'):return [p for part in g.geoms for p in polygons(part)]
    return []


def excluded_entities(inventory):
    ids=set()
    def visit(x):
        if isinstance(x,dict):
            ids.update(x.get('source_ids',[]))
            if 'a' in x and 'b' in x and 'id' in x:ids.add(x['id'])
            for k,v in x.items():
                if k=='arrow_wing_ids':
                    for pair in v:ids.update(pair)
                else:visit(v)
        elif isinstance(x,list):
            for v in x:visit(v)
    for occurrence in inventory['occurrences']:
        visit(occurrence.get('associated_lines',[]))
        if occurrence.get('leader_association'):visit(occurrence['leader_association'])
        elif occurrence.get('status')=='ASSOCIATED':visit(occurrence.get('associations',[]))
    visit(inventory.get('localized_reconstruction',{}).get('physical_groups',[]))
    return ids


def boundary_evidence(data,roi,excluded):
    """Hatch contacts plus parallel face context. No color or path-ID ranges.

    Many boundaries will remain missing. No endpoint snapping or gap closure.
    Short closure segments need two supported neighbors; annotations alone fail.
    """
    source=[s for s in data['segments'] if s['id'] not in excluded and s['a']!=s['b'] and contains(roi,s['a']) and contains(roi,s['b'])]
    hatches=[]
    for s in source:
        dx=abs(s['a'][0]-s['b'][0]);dy=abs(s['a'][1]-s['b'][1]);length=math.hypot(dx,dy)
        if 3<length<45 and dx and abs(dx-dy)/max(dx,dy)<.08:hatches.append(s)
    entries=[];hatch_ids={h['id'] for h in hatches}
    for s in source:
        length=math.dist(s['a'],s['b'])
        if length<2:continue
        # Diagonal hatch strokes do not become boundaries themselves.
        if s['id'] in hatch_ids:continue
        line=LineString([s['a'],s['b']]);x0,y0,x1,y1=line.bounds
        near=[h for h in hatches if any(x0-.25<=p[0]<=x1+.25 and y0-.25<=p[1]<=y1+.25 and line.distance(Point(p))<=.25 for p in (h['a'],h['b']))]
        locations=sorted({round(line.project(Point(p)),2) for h in near for p in (h['a'],h['b']) if line.distance(Point(p))<=.25})
        if len(locations)>=3 and locations[-1]-locations[0]>=8:
            entries.append({'id':s['id'],'a':s['a'],'b':s['b'],'basis':'REPEATED_HATCH_CONTACTS','hatch_ids':sorted(h['id'] for h in near),'hatch_contact_count':len(locations)})
    supported={e['id'] for e in entries};supported_faces=tuple(entries)
    for s in source:
        if s['id'] in supported or s['id'] in hatch_ids or not 2<=math.dist(s['a'],s['b'])<=30:continue
        neighbors=[]
        for p in (s['a'],s['b']):neighbors.append(sorted(e['id'] for e in supported_faces if LineString([e['a'],e['b']]).distance(Point(p))<=.001))
        if all(neighbors) and set(neighbors[0])!=set(neighbors[1]):
            entries.append({'id':s['id'],'a':s['a'],'b':s['b'],'basis':'SHORT_CLOSURE_BETWEEN_SUPPORTED_FACES','supported_neighbors':neighbors});supported.add(s['id'])
    return sorted(entries,key=lambda e:e['id'])


def polygon_candidates(lines,labels,openings=(),connectors=()):
    """Planar noding + faces; associate seeds only after topology, retain alternatives."""
    unique=sorted({tuple(sorted([tuple(e['a']),tuple(e['b'])])) for e in lines})
    network=unary_union([LineString(v) for v in unique])
    faces,cuts,dangles,invalid=polygonize_full(network)
    candidates=[]
    for face in sorted(faces.geoms,key=lambda f:(f.bounds,json.dumps(geo(f),sort_keys=True))):
        seeds=[];label_evidence=[]
        for s in labels:
            if face.covers(Point(center(s['label']['bbox']))):
                seeds.append(s);label_evidence.append({'label_id':s['id'],'basis':'TEXT_SEED_INSIDE_FACE'});continue
            labelbox=box(*s['label']['bbox'])
            links=[e for e in connectors if any(labelbox.distance(Point(p))<=4 for p in (e['a'],e['b'])) and
                face.intersection(LineString([e['a'],e['b']])).length>1e-7 and any(face.contains(Point(p)) for p in (e['a'],e['b']))]
            if links:
                seeds.append(s);label_evidence.append({'label_id':s['id'],'basis':'EXPLICIT_LABEL_CONNECTOR_INTO_FACE','segment_ids':sorted(e['id'] for e in links)})
        if not seeds:continue
        evidence=sorted([e for e in lines if face.boundary.intersection(LineString([e['a'],e['b']])).length>1e-7],key=lambda e:e['id'])
        if any(e.get('basis')=='UNCLASSIFIED_ORTHOGONAL_LINE_AFTER_ANNOTATION_EXCLUSION' for e in evidence):
            strong=[e for e in evidence if e.get('basis')!='UNCLASSIFIED_ORTHOGONAL_LINE_AFTER_ANNOTATION_EXCLUSION']
            supported_length=unary_union([LineString([e['a'],e['b']]).intersection(face.boundary) for e in strong]).length
            linked=any(e['basis']=='EXPLICIT_LABEL_CONNECTOR_INTO_FACE' for e in label_evidence)
            if not linked and (len(strong)<2 or supported_length/face.length<.2):continue
        geometry=geo(face);id='P-'+hashlib.sha256(json.dumps(geometry,sort_keys=True).encode()).hexdigest()[:12]
        # A label pointer can terminate on a narrow perimeter/beam face rather
        # than within the slab. Concavity + slender border geometry + external
        # pointer is a review flag, never proof of an invalid slab.
        border_suspect=face.area/face.convex_hull.area<.35 and all(e['basis']=='EXPLICIT_LABEL_CONNECTOR_INTO_FACE' for e in label_evidence)
        candidates.append({'id':id,'geometry_pdf_pt':geometry,'bbox':list(face.bounds),'area_pt2':face.area,
            'label_ids':[s['id'] for s in seeds],'label_evidence':label_evidence,'boundary_segment_ids':[e['id'] for e in evidence],
            'evidence':evidence,'interior_ring_state':'GRAPHIC_RING_NOT_PROVED_STRUCTURAL_OPENING' if face.interiors else 'NO_INTERIOR_RING',
            'auxiliary_opening_ids':[h['id'] for h in openings if face.intersects(box(*h['bbox']))],
            'state':'PRELIMINARY_CANDIDATE' if len(seeds)==1 else 'MULTIPLE_SLAB_LABELS_AMBIGUOUS',
            'border_or_beam_face_review_required':border_suspect,'convex_hull_fill_fraction':face.area/face.convex_hull.area,
            'engineer_confirmed':False,'source':'HATCH_SUPPORTED_PLANAR_FACE','original_coordinates_modified':False})
    return candidates,{'noded_faces':len(faces.geoms),'cut_edges':len(cuts.geoms),'dangles':len(dangles.geoms),'invalid_rings':len(invalid.geoms),'backend':'Shapely '+shapely.__version__,'snapping':False}


def normalized_topology(lines,tolerance=.001):
    """Alternative topology only; retain every original coordinate and movement.

    Coordinate clusters have maximum span <= tolerance (not chained snapping).
    A representative is an existing coordinate. This never overwrites input data.
    """
    maps=[]
    for k in (0,1):
        values=sorted({e[end][k] for e in lines for end in ('a','b')});m={};anchor=None
        for v in values:
            if anchor is None or v-anchor>tolerance:anchor=v
            m[v]=anchor
        maps.append(m)
    adjusted=[];moves=[]
    for e in lines:
        z=dict(e);z['a']=[maps[k][e['a'][k]] for k in (0,1)];z['b']=[maps[k][e['b'][k]] for k in (0,1)]
        if z['a']!=e['a'] or z['b']!=e['b']:
            moves.append({'segment_id':e['id'],'original_a':e['a'],'original_b':e['b'],'topological_a':z['a'],'topological_b':z['b']})
        if z['a']!=z['b']:adjusted.append(z)
    return adjusted,moves


def reconstruct_slabs(inventory,data):
    previous=inventory['structural_interpretation']['slabs'];roi=inventory['layout']['detail_roi_pt']
    excluded=excluded_entities(inventory);lines=boundary_evidence(data,roi,excluded)
    connectors=[e for e in data['segments'] if e['id'] not in excluded and e['a']!=e['b'] and math.dist(e['a'],e['b'])<100 and
        any(any(box(*s['label']['bbox']).distance(Point(p))<=4 for p in (e['a'],e['b'])) for s in previous)]
    openings=inventory.get('localized_reconstruction',{}).get('openings',[])
    candidates,diagnostics=polygon_candidates(lines,previous,openings,connectors)
    # Additional tier for unhatched perimeters: remove graphic axes/cotas first.
    # A retained face still needs supported boundary context or an explicit label
    # connector entering it. Orthogonality/closure alone never establishes a slab.
    axes=distribution_axes(line_geometry(data['segments']),data['segments'])
    annotation_ids={id for a in axes for id in a.get('source_ids',[a['id']])}
    annotation_ids.update(e['id'] for e in connectors)
    known={e['id'] for e in lines};expanded=list(lines)
    for e in data['segments']:
        if e['id'] in excluded or e['id'] in annotation_ids or e['id'] in known:continue
        if not contains(roi,e['a']) or not contains(roi,e['b']) or math.dist(e['a'],e['b'])<2:continue
        if e['a'][0]!=e['b'][0] and e['a'][1]!=e['b'][1]:continue
        expanded.append({'id':e['id'],'a':e['a'],'b':e['b'],'basis':'UNCLASSIFIED_ORTHOGONAL_LINE_AFTER_ANNOTATION_EXCLUSION'})
    expanded_candidates,expanded_diagnostics=polygon_candidates(expanded,previous,openings,connectors)
    for c in expanded_candidates:
        if any(c['geometry_pdf_pt']==z['geometry_pdf_pt'] and c['label_ids']==z['label_ids'] for z in candidates):continue
        c['source']='EXPANDED_FACE_REQUIRING_STRUCTURAL_CONTEXT_OR_LABEL_CONNECTOR';c['edge_semantics_confirmed']=False;candidates.append(c)
    diagnostics['expanded_linework']=expanded_diagnostics
    normalized,moves=normalized_topology(lines)
    alternatives,normalized_diagnostics=polygon_candidates(normalized,previous,openings,connectors)
    for c in alternatives:
        if any(shape(c['geometry_pdf_pt']).hausdorff_distance(shape(z['geometry_pdf_pt']))<=.002 and c['label_ids']==z['label_ids'] for z in candidates):continue
        c['source']='ALTERNATIVE_NORMALIZED_TOPOLOGY';c['topology_tolerance_pt']=.001;c['original_coordinates_modified']=False
        c['derived_topology_coordinates_adjusted']=True;candidates.append(c)
    diagnostics['normalized_alternative']=normalized_diagnostics
    # Stage 6 alternatives remain alternatives. They are not replaced by a new nearest face.
    for slab in previous:
        for old in slab['contour_alternatives']:
            geom=geo(Polygon(old['polygon_pdf_pt']));existing=next((c for c in candidates if c['geometry_pdf_pt']==geom and c['label_ids']==[slab['id']]),None)
            if existing:existing['also_stage6_candidate']=True;continue
            id='P-'+hashlib.sha256(json.dumps(geom,sort_keys=True).encode()).hexdigest()[:12]
            candidates.append({'id':id,'geometry_pdf_pt':geom,'bbox':old['bbox'],'area_pt2':Polygon(old['polygon_pdf_pt']).area,
                'label_ids':[slab['id']],'boundary_segment_ids':sorted({id for e in old['edge_evidence'] for id in e['segment_ids']}),
                'evidence':old['edge_evidence'],'state':'PRELIMINARY_STAGE6_ALTERNATIVE','engineer_confirmed':False,
                'source':'PRESERVED_STAGE6_RECTANGLE','original_coordinates_modified':False})
    candidates.sort(key=lambda c:(c['bbox'],c['id'],c['label_ids']))
    regions=inventory['distributed_spatial_analysis']['regions'];cells=inventory['distributed_spatial_analysis']['composition_regions'];slabs=[]
    for old in previous:
        options=[c for c in candidates if old['id'] in c['label_ids']];unique=len(options)==1 and options[0]['label_ids']==[old['id']]
        blocked=unique and options[0].get('border_or_beam_face_review_required',False)
        s={k:old[k] for k in ('id','name','thickness_cm','label','thickness_sources','documentary_state')}
        s.update(contour_candidates=options,selected_candidate_id=options[0]['id'] if unique and not blocked else None,
            contour_state='BORDER_OR_BEAM_FACE_REVIEW_REQUIRED' if blocked else ('UNIQUE_PRELIMINARY_CANDIDATE' if unique else ('COMPETING_CANDIDATES' if options else 'PENDING_CONTOUR')),
            contour_confirmed=False,region_relations=[],composition_relations=[])
        for candidate in options:
            poly=shape(candidate['geometry_pdf_pt'])
            for records,key in ((regions,'region_relations'),(cells,'composition_relations')):
                for r in records:
                    g=poly.intersection(Polygon(r['polygon_pdf_pt']))
                    if g.area>1e-8:s[key].append({'candidate_id':candidate['id'],'region_id':r['id'],'area_pt2':g.area,'intersection_pdf_pt':geo(g),
                        'association_state':'PRELIMINARY_UNIQUE_CONTOUR' if unique and not blocked else 'ALTERNATIVE_ONLY_NOT_ASSIGNED','physical_bar_clipped':False})
        slabs.append(s)
    crossing=[]
    for r in regions:
        hits=[s['name'] for s in slabs if s['selected_candidate_id'] and any(h['region_id']==r['id'] for h in s['region_relations'])]
        if len(hits)>1:crossing.append({'region_id':r['id'],'slabs':hits,'state':'PRELIMINARY_MULTIPLE_SLAB_INTERSECTION'})
    return {'slabs':slabs,'candidates':candidates,'linework_evidence':lines,'topology_adjustments':moves,'label_connector_candidates':connectors,
        'polygonization':diagnostics,'crossing_occurrences':crossing,'formwork_substitute':False,'opening_subtraction_authorized':False}
