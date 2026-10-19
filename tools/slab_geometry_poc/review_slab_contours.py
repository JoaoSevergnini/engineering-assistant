"""Independent review experiment: full label block, exact existing vector faces.

Does not replace the stage 7 inventory or certify structural slab domains.
"""
import hashlib
import json
from pathlib import Path
from automatic import center,contains,union,line_geometry,distribution_axes
from polygonal_slabs import Point,LineString,Polygon,box,shape,geo,unary_union,polygonize_full,excluded_entities


def label_block(slab,texts):
    lookup={t['id']:t for t in texts}
    return union([slab['label']['bbox']]+[lookup[id]['bbox'] for id in slab['thickness_sources'] if id in lookup])


def label_links(slab,texts,segments):
    block=box(*label_block(slab,texts));result=[]
    for e in segments:
        if e['a']==e['b'] or LineString([e['a'],e['b']]).length>100:continue
        for label_end,target in ((e['a'],e['b']),(e['b'],e['a'])):
            if block.distance(Point(label_end))<=4 and block.distance(Point(target))>4:
                result.append({'segment_id':e['id'],'label_end':label_end,'target':target,'label_block_pdf_pt':list(block.bounds)})
    return sorted(result,key=lambda r:r['segment_id'])


def review(inventory,data):
    old=inventory['occurrence_relation_analysis']['slab_reconstruction'];roi=inventory['layout']['detail_roi_pt'];excluded=excluded_entities(inventory)
    axes=distribution_axes(line_geometry(data['segments']),data['segments']);annotation_ids={id for a in axes for id in a.get('source_ids',[a['id']])}
    links={s['id']:label_links(s,data['texts'],[e for e in data['segments'] if e['id'] not in excluded]) for s in old['slabs']}
    pointers={l['segment_id'] for values in links.values() for l in values}
    strong={e['id'] for e in old['linework_evidence']}
    edges=[e for e in data['segments'] if e['id'] not in excluded|pointers and (e['id'] not in annotation_ids or e['id'] in strong)
           and e['a']!=e['b'] and contains(roi,e['a']) and contains(roi,e['b']) and LineString([e['a'],e['b']]).length>=2
           and (e['a'][0]==e['b'][0] or e['a'][1]==e['b'][1])]
    network=unary_union([LineString([e['a'],e['b']]) for e in sorted(edges,key=lambda e:e['id'])]);faces,cuts,dangles,invalid=polygonize_full(network)
    slabs=[];regions=inventory['distributed_spatial_analysis']['regions']
    groups=inventory.get('localized_reconstruction',{}).get('physical_groups',[])
    for s in old['slabs']:
        matches=[]
        for face in faces.geoms:
            inside=face.contains(Point(center(s['label']['bbox'])))
            landed=[l for l in links[s['id']] if face.contains(Point(l['target']))]
            if not inside and not landed:continue
            boundary_ids=sorted(e['id'] for e in edges if face.boundary.intersection(LineString([e['a'],e['b']])).length>1e-7)
            hits=[]
            for r in regions:
                g=face.intersection(Polygon(r['polygon_pdf_pt']))
                if g.area>1e-8:hits.append({'region_id':r['id'],'occurrence_id':r['occurrence_id'],'display_id':r['display_id'],'position':r['position'],
                    'intersection_pdf_pt':geo(g),'intersection_area_pt2':g.area,'fraction_of_graphic_region':g.area/r['area_pt2'],
                    'status':'GRAPHIC_INTERSECTION_ONLY_PHYSICAL_ASSIGNMENT_PENDING'})
            local=[]
            for group in groups:
                lines=[LineString([e['a'],e['b']]) for e in group['lines'] if e['a']!=e['b']]
                length=sum(line.intersection(face).length for line in lines)
                if length>1e-7:local.append({'group_id':group['id'],'position':group['mark'],'intersection_length_pt':length,'status':'TRACE_INTERSECTION_NOT_PROOF_OF_WHOLE_GROUP_ASSIGNMENT'})
            geometry=geo(face)
            matches.append({'id':'REV-'+hashlib.sha256(json.dumps(geometry,sort_keys=True).encode()).hexdigest()[:10],
                'geometry_pdf_pt':geometry,'area_pt2':face.area,'bbox':list(face.bounds),'boundary_segment_ids':boundary_ids,
                'evidence':'NAME_INSIDE_CLOSED_VECTOR_FACE' if inside else 'NAME_THICKNESS_BLOCK_WITH_EXPLICIT_POINTER',
                'label_links':landed,'thin_perimeter_review_flag':face.area/face.convex_hull.area<.35,
                'distributed_intersections':hits,'localized_trace_intersections':local,'engineer_confirmed':False})
        slabs.append({'name':s['name'],'thickness_cm':s['thickness_cm'],'stage7_state':s['contour_state'],
            'label_block_pdf_pt':label_block(s,data['texts']),'label_links':links[s['id']],
            'contour_review_candidates':sorted(matches,key=lambda m:m['id']),
            'state':'REVIEW_CANDIDATE_NOT_CONFIRMED' if matches else 'PENDING_CONTOUR',
            'label_point_region_hints_not_assignments':[r['id'] for r in regions if Polygon(r['polygon_pdf_pt']).contains(Point(center(s['label']['bbox']))) ]})
    return {'source':'INDEPENDENT_REVIEW_OF_STAGE7; NOT_A_REPLACEMENT_INVENTORY','units':'PDF_PT_AND_PT2',
        'slabs':slabs,'network':{'faces':len(faces.geoms),'cuts':len(cuts.geoms),'dangles':len(dangles.geoms),'invalid_rings':len(invalid.geoms),'snapping':False},
        'metrics':{'labels':len(slabs),'slabs_with_review_candidates':sum(bool(s['contour_review_candidates']) for s in slabs),
                   'unique_distributed_occurrences_with_geometric_intersection':len({h['occurrence_id'] for s in slabs for c in s['contour_review_candidates'] for h in c['distributed_intersections']}),
                   'engineer_confirmed_contours':0},'original_inventory_modified':False,'physical_assignment_authorized':False}


def main():
    from run_sheet import ROOT,fitz,save_json
    from run_structural_regions import canvas,box as drawbox,write_png
    from run_relations import draw_geometry
    root=ROOT/'analises/lajes_revisao_contornos';root.mkdir(exist_ok=True)
    inv_path=ROOT/'analises/lajes_relacoes_contornos/inventario.json';data_path=ROOT/'analises/lajes_geometria_lideres/entidades_pagina.json'
    inv=json.loads(inv_path.read_text(encoding='utf-8'));data=json.loads(data_path.read_text(encoding='utf-8'));result=review(inv,data)
    source=Path(inv['stage5_provenance']['source_pdf']);before=hashlib.sha256(source.read_bytes()).hexdigest()
    if before!=inv['stage5_provenance']['sha256']:raise ValueError('SOURCE_CHANGED')
    result['provenance']={'pdf_sha256':before,'stage7_inventory_sha256':hashlib.sha256(inv_path.read_bytes()).hexdigest(),'entities_sha256':hashlib.sha256(data_path.read_bytes()).hexdigest()}
    with fitz.open(str(source)) as doc:
        pdoc,page,clip=canvas(doc[0],[50,145,1900,1205])
        for i,s in enumerate(result['slabs']):
            color=(.55,.1,.7) if s['contour_review_candidates'] else (.9,.1,.1)
            drawbox(page,s['label_block_pdf_pt'],clip,s['name'],color,True)
            for c in s['contour_review_candidates']:
                draw_geometry(page,c['geometry_pdf_pt'],clip,color,dashed=True)
                for l in c['label_links']:page.draw_line(fitz.Point(l['label_end'][0]-clip.x0,l['label_end'][1]-clip.y0),fitz.Point(l['target'][0]-clip.x0,l['target'][1]-clip.y0),color=(0,.5,.8),width=1.5)
        write_png(pdoc,page,root/'contornos_revisados.png','Roxo tracejado: candidato em revisao | Azul: apontador documental | Vermelho: contorno pendente | Nenhuma confirmacao humana nova')
        for s in result['slabs']:
            if not s['contour_review_candidates']:continue
            b=union([c['bbox'] for c in s['contour_review_candidates']]+[s['label_block_pdf_pt']]);clip=fitz.Rect(b[0]-25,b[1]-25,b[2]+25,b[3]+25)&doc[0].rect
            pdoc,page,clip=canvas(doc[0],clip)
            for c in s['contour_review_candidates']:
                draw_geometry(page,c['geometry_pdf_pt'],clip,(.5,0,.65),dashed=True)
                for hit in c['distributed_intersections']:draw_geometry(page,hit['intersection_pdf_pt'],clip,(0,.5,.6),hit['display_id']+'/'+hit['position'])
            write_png(pdoc,page,root/(s['name']+'_associacoes.png'),s['name']+' | Roxo: contorno candidato | Ciano: intersecao grafica de armadura; nao prova atribuicao fisica integral')
    assert before==hashlib.sha256(source.read_bytes()).hexdigest()
    save_json(root/'revisao.json',result)
    print(json.dumps(result['metrics'],ensure_ascii=False))
    print([(s['name'],[(c['evidence'],[(h['display_id'],h['position'],round(h['fraction_of_graphic_region'],3)) for h in c['distributed_intersections']]) for c in s['contour_review_candidates']]) for s in result['slabs']])


if __name__=='__main__':main()
