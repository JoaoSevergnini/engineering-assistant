"""Register a human marked contour separately from automatic slab candidates."""
import hashlib
import json
import math
from pathlib import Path
from polygonal_slabs import Polygon,LineString,geo


def fit_axis(anchors):
    if len(anchors)<2:raise ValueError('At least two registration anchors required')
    x=sum(a for a,b in anchors)/len(anchors);y=sum(b for a,b in anchors)/len(anchors)
    denominator=sum((a-x)**2 for a,b in anchors)
    if denominator==0:raise ValueError('Degenerate registration')
    slope=sum((a-x)*(b-y) for a,b in anchors)/denominator
    if slope<=0:raise ValueError('Expected unrotated positive-axis screenshot')
    offset=y-slope*x
    return {'pdf_to_image_scale':slope,'offset_px':offset,'rms_residual_px':math.sqrt(sum((slope*a+offset-b)**2 for a,b in anchors)/len(anchors))}


def register_outline(profile):
    fits={k:fit_axis(profile['registration_anchors'][k]) for k in ('x','y')}
    points=[[(p[i]-fits[k]['offset_px'])/fits[k]['pdf_to_image_scale'] for i,k in enumerate(('x','y'))] for p in profile['vertices_image_px']]
    poly=Polygon(points)
    if not poly.is_valid or poly.is_empty or poly.area<=0:raise ValueError('Invalid digitized outline; no silent repair')
    return poly,{'axes':fits,'rotation_or_shear_fitted':False,'source_vertices_image_px':profile['vertices_image_px'],
                 'metric_validation':profile['metric_validation'],'source_confirmation_scope':profile['confirmation_scope']}


def analyze(inventory,profile):
    if profile['pdf_sha256']!=inventory['stage5_provenance']['sha256']:raise ValueError('Confirmation refers to a different PDF')
    poly,registration=register_outline(profile);margin=profile['boundary_uncertainty_pdf_pt']
    if margin<0:raise ValueError('Negative boundary uncertainty')
    inner=poly.buffer(-margin);outer=poly.buffer(margin);hits=[]
    for r in inventory['distributed_spatial_analysis']['regions']:
        p=Polygon(r['polygon_pdf_pt']);g=p.intersection(poly);maximum=p.intersection(outer).area;minimum=p.intersection(inner).area
        if maximum<=1e-8:continue
        hits.append({'region_id':r['id'],'occurrence_id':r['occurrence_id'],'display_id':r['display_id'],'position':r['position'],
            'intersection_pdf_pt':geo(g),'intersection_area_pt2':g.area,'fraction_of_graphic_region':g.area/p.area,
            'minimum_intersection_area_pt2_under_margin':minimum,'maximum_intersection_area_pt2_under_margin':maximum,
            'state':'INTERIOR_INTERSECTION_SUPPORTED' if minimum>1e-8 else 'BOUNDARY_SENSITIVE_REVIEW_REQUIRED',
            'physical_assignment_of_entire_bar_confirmed':False})
    local=[]
    for group in inventory.get('localized_reconstruction',{}).get('physical_groups',[]):
        segments=[LineString([s['a'],s['b']]) for s in group['lines'] if s['a']!=s['b']]
        nominal=sum(s.intersection(poly).length for s in segments);minimum=sum(s.intersection(inner).length for s in segments);maximum=sum(s.intersection(outer).length for s in segments)
        if maximum>1e-7:local.append({'group_id':group['id'],'position':group['mark'],'intersection_length_pt':nominal,
            'minimum_length_under_margin_pt':minimum,'maximum_length_under_margin_pt':maximum,
            'state':'TRACE_INTERIOR_INTERSECTION_SUPPORTED' if minimum>1e-7 else 'BOUNDARY_SENSITIVE_REVIEW_REQUIRED',
            'whole_group_assignment_confirmed':False})
    return {'slab':profile['slab'],'thickness_cm':profile['thickness_cm'],'human_confirmation':profile,
        'geometry_pdf_pt':geo(poly),'registration':registration,'geometry_state':'HUMAN_CONFIRMED_TOPOLOGY_APPROXIMATE_METRIC_DIGITIZATION',
        'coordinate_units':'PDF_PT','area_units':'PT2_NOT_STEEL_AREA','graphic_area_pt2':poly.area,
        'distributed_intersections':hits,'localized_trace_intersections':local,'original_geometry_modified':False,
        'structural_calculations_performed':False,'all_openings_confirmed':False,
        'metrics':{'distributed_nominal_intersections':sum(h['intersection_area_pt2']>1e-8 for h in hits),
                   'distributed_interior_supported':sum(h['state']=='INTERIOR_INTERSECTION_SUPPORTED' for h in hits),
                   'distributed_boundary_sensitive':sum(h['state']=='BOUNDARY_SENSITIVE_REVIEW_REQUIRED' for h in hits)}}


def main():
    from run_sheet import ROOT,fitz,save_json
    from run_structural_regions import canvas,write_png
    from run_relations import draw_geometry
    out=ROOT/'analises/lajes_l603_confirmada';p=out/'confirmacao_joao_L603.json'
    profile=json.loads(p.read_text(encoding='utf-8'));inp=ROOT/'analises/lajes_relacoes_contornos/inventario.json';inv=json.loads(inp.read_text(encoding='utf-8'))
    result=analyze(inv,profile);source=Path(inv['stage5_provenance']['source_pdf']);before=hashlib.sha256(source.read_bytes()).hexdigest()
    if before!=profile['pdf_sha256']:raise ValueError('SOURCE_CHANGED')
    result['provenance']={'pdf_sha256':before,'input_inventory_sha256':hashlib.sha256(inp.read_bytes()).hexdigest(),'confirmation_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
    with fitz.open(str(source)) as pdf:
        for name,with_hits in [('L603_contorno_confirmado',False),('L603_armaduras',True)]:
            doc,page,clip=canvas(pdf[0],[50,360,1910,1160])
            draw_geometry(page,result['geometry_pdf_pt'],clip,(.85,0,0),dashed=False)
            if with_hits:
                for h in result['distributed_intersections']:
                    if h['intersection_area_pt2']>1e-8:draw_geometry(page,h['intersection_pdf_pt'],clip,(0,.5,.6),h['display_id']+'/'+h['position'],dashed=h['state']=='BOUNDARY_SENSITIVE_REVIEW_REQUIRED')
            write_png(doc,page,out/(name+'.png'),'Vermelho: perimetro indicado por Joao, digitalizacao metrica aproximada | Ciano: intersecoes graficas, sem atribuicao integral de barras')
    assert before==hashlib.sha256(source.read_bytes()).hexdigest()
    save_json(out/'L603_associacoes.json',result)
    print(json.dumps(result['metrics']));print([(h['display_id'],h['position'],round(h['fraction_of_graphic_region'],3),h['state']) for h in result['distributed_intersections']])


if __name__=='__main__':main()
