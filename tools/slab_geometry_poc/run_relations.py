"""Stage 7: derived relation/contour inventories and separate validation maps."""
import argparse
import hashlib
import json
from pathlib import Path
from run_sheet import ROOT,fitz,save_json
from run_structural_regions import canvas,box,write_png,COLORS
from polygonal_slabs import shape,geo,polygons
from occurrence_relations import analyze_relations


def draw_geometry(page,geometry,clip,color,label='',dashed=False):
    for poly in polygons(shape(geometry)):
        points=[fitz.Point(x-clip.x0,y-clip.y0) for x,y in poly.exterior.coords]
        s=page.new_shape();s.draw_polyline(points);s.finish(color=color,width=1.1,dashes='[4 2] 0' if dashed else None);s.commit()
        for ring in poly.interiors:
            s=page.new_shape();s.draw_polyline([fitz.Point(x-clip.x0,y-clip.y0) for x,y in ring.coords]);s.finish(color=color,width=.8,dashes='[2 2] 0');s.commit()
        if label:
            p=poly.representative_point();page.insert_text((p.x-clip.x0,p.y-clip.y0),label,fontsize=7,color=color)


def visuals(source,result,out):
    a=result['occurrence_relation_analysis'];sp=result['distributed_spatial_analysis'];lookup={r['id']:r for r in sp['regions']};cells={c['id']:c for c in sp['composition_regions']};roi=[50,145,1900,1205]
    doc,p,clip=canvas(source,roi)
    for rel in a['relations']:
        if shape(rel['validity_geometry_pdf_pt']).is_empty:continue
        confirmed=rel['state']=='ENGINEER_CONFIRMED_LOCAL_SCOPE';color=(0,.55,.25) if confirmed else (.65,.4,.1)
        draw_geometry(p,rel['validity_geometry_pdf_pt'],clip,color,dashed=not confirmed)
    write_png(doc,p,out/'relacoes.png','Verde continuo: confirmacao humana local | Marrom tracejado: evidencia/candidato; sem alcance fisico global comprovado')
    for name,classification in [('base_reforco','BASE_PLUS_REINFORCEMENT'),('traspasses','LAP_SPLICE'),('residuais','GRAPHICAL_RESIDUAL'),('indeterminadas','UNDETERMINED')]:
        doc,p,clip=canvas(source,roi)
        for i in a['interpreted_compositions']:
            if i['classification']==classification:box(p,cells[i['composition_id']]['bbox'],clip,i['composition_id'],COLORS[classification],classification=='UNDETERMINED')
        write_png(doc,p,out/(name+'.png'),'Classificacao derivada Etapa 7 | Poligonos e classificacoes humanas da Etapa 6 preservados')
    doc,p,clip=canvas(source,roi)
    for s in a['slab_reconstruction']['slabs']:
        box(p,s['label']['bbox'],clip,s['name']+' h:'+str(s['thickness_cm']),(.1,.2,.8))
        for c in s['contour_candidates']:
            draw_geometry(p,c['geometry_pdf_pt'],clip,(0,.6,.4) if s['selected_candidate_id'] else (.8,.45,.1),dashed=not bool(s['selected_candidate_id']))
    write_png(doc,p,out/'contornos.png','Azul: etiqueta documental | Verde: candidato unico preliminar | Laranja tracejado: concorrente ou face de borda suspeita; nenhum confirmado')
    doc,p,clip=canvas(source,roi)
    for s in a['slab_reconstruction']['slabs']:
        if not s['selected_candidate_id']:continue
        for h in s['region_relations']:draw_geometry(p,h['intersection_pdf_pt'],clip,(0,.55,.55),h['region_id']+'/'+s['name'])
    write_png(doc,p,out/'associacao_lajes.png','Apenas intersecoes com candidato unico preliminar | Sem recorte fisico de barras ou atribuicao por proximidade')
    # Side-by-side maps, same source clip and scale.
    doc=fitz.open();p=doc.new_page(width=1850*2+20,height=1100);clip=fitz.Rect(roi)
    pix=source.get_pixmap(clip=clip)
    for offset in (0,1870):p.insert_image(fitz.Rect(offset,0,offset+1850,1060),stream=pix.tobytes('png'))
    for offset,records in [(0,result['structural_interpretation']['overlap_interpretations']),(1870,a['interpreted_compositions'])]:
        shifted=fitz.Rect(clip.x0-offset,clip.y0,clip.x1-offset,clip.y1)
        for i in records:
            if i['classification'] not in ('SINGLE_DISTRIBUTED','UNDETERMINED'):
                b=cells[i['composition_id']]['bbox'];rect=fitz.Rect(b[0]-shifted.x0,b[1]-shifted.y0,b[2]-shifted.x0,b[3]-shifted.y0)
                p.draw_rect(rect,color=COLORS[i['classification']],fill=COLORS[i['classification']],fill_opacity=.25,width=1)
    for s in result['structural_interpretation']['slabs']:
        for c in s['contour_alternatives']:
            ring=c['polygon_pdf_pt'];draw_geometry(p,{'type':'Polygon','coordinates':[ring+[ring[0]]]},clip,(0,.55,.4) if s['contour'] else (.8,.45,.1),dashed=not bool(s['contour']))
    shifted=fitz.Rect(clip.x0-1870,clip.y0,clip.x1-1870,clip.y1)
    for s in a['slab_reconstruction']['slabs']:
        for c in s['contour_candidates']:draw_geometry(p,c['geometry_pdf_pt'],shifted,(0,.55,.4) if s['selected_candidate_id'] else (.8,.45,.1),dashed=not bool(s['selected_candidate_id']))
    write_png(doc,p,out/'comparacao_6_7.png','Esquerda: Etapa 6 | Direita: Etapa 7 | Confirmacoes locais mantidas; nenhuma extensao automatica do alcance humano')
    # Zooms selected by provenance, not by hardcoded composition IDs.
    for rel in a['relations']:
        if rel['state']!='ENGINEER_CONFIRMED_LOCAL_SCOPE':continue
        g=shape(rel['validity_geometry_pdf_pt']);b=g.bounds;cx=(b[0]+b[2])/2;cy=(b[1]+b[3])/2;w=max(480,b[2]-b[0]+130);h=max(340,b[3]-b[1]+130)
        doc,p,clip=canvas(source,fitz.Rect(cx-w/2,cy-h/2,cx+w/2,cy+h/2)&source.rect)
        for id in rel['members']:box(p,lookup[id]['bbox'],clip,id,(.3,.45,.7),True)
        draw_geometry(p,rel['validity_geometry_pdf_pt'],clip,COLORS[rel['structural_meaning']])
        label=rel['evidence']['confirmed_composition_id'];write_png(doc,p,out/(label+'_relacao.png'),label+' '+rel['type']+' | Confirmacao humana restrita ao dominio colorido; tracejado: envoltorias candidatas')
    for check in a['containment_checks']:
        if not check['uncovered_area_pt2']:continue
        r=lookup[check['reinforcement_id']];b=r['bbox'];cx=(b[0]+b[2])/2;cy=(b[1]+b[3])/2
        doc,p,clip=canvas(source,fitz.Rect(cx-350,cy-150,cx+350,cy+150)&source.rect)
        for id in check['base_region_ids']:box(p,lookup[id]['bbox'],clip,'',(.1,.4,.8),True)
        box(p,b,clip,'',(.85,.4,.1),True)
        for poly in check['uncovered_polygons_pdf_pt']:draw_geometry(p,{'type':'Polygon','coordinates':[poly+[poly[0]]]},clip,(.75,0,.6))
        write_png(doc,p,out/(r['id']+'_reavaliacao.png'),'Azul: base candidata | Laranja: '+r['id']+' funcao nao confirmada | Roxo: descoberta; sem conclusao de erro estrutural')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--inventory',default=str(ROOT/'analises/lajes_interpretacao_estrutural/inventario.json'));parser.add_argument('--entities',default=str(ROOT/'analises/lajes_geometria_lideres/entidades_pagina.json'));parser.add_argument('--out',default=str(ROOT/'analises/lajes_relacoes_contornos'));args=parser.parse_args()
    inp=Path(args.inventory);ent=Path(args.entities);out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    previous=json.loads(inp.read_text(encoding='utf-8'));data=json.loads(ent.read_text(encoding='utf-8'));source=Path(previous['stage5_provenance']['source_pdf']);before=hashlib.sha256(source.read_bytes()).hexdigest()
    if before!=previous['stage5_provenance']['sha256']:raise ValueError('SOURCE_PDF_CHANGED')
    result=analyze_relations(previous,data);a=result['occurrence_relation_analysis']
    result['stage7_provenance']={'source_pdf_sha256':before,'stage6_inventory_sha256':hashlib.sha256(inp.read_bytes()).hexdigest(),'entities_sha256':hashlib.sha256(ent.read_bytes()).hexdigest(),
        'prior_layers_preserved':all(result[k]==v for k,v in previous.items()),'geometric_partition_preserved':result['distributed_spatial_analysis']==previous['distributed_spatial_analysis'],
        'human_confirmations_preserved':result['structural_interpretation']==previous['structural_interpretation'],'n38_preserved':result['stage5_documentary_consistency']==previous['stage5_documentary_consistency']}
    with fitz.open(str(source)) as pdf:visuals(pdf[0],result,out)
    if hashlib.sha256(source.read_bytes()).hexdigest()!=before:raise ValueError('SOURCE_PDF_CHANGED_DURING_RUN')
    save_json(out/'inventario.json',result)
    for file,key in [('relacoes','relations'),('regioes_interpretadas','interpreted_compositions'),('regioes_consolidadas','consolidated_regions'),('lajes','slab_reconstruction'),('contencao','containment_checks'),('ambiguidades','ambiguities'),('indicadores','metrics')]:save_json(out/(file+'.json'),a[key])
    rows=['| Relação | Tipo | Regiões individuais | Estado |','|---|---|---|---|']
    rows.extend('| '+r['id']+' | '+r['type']+' | '+', '.join(r['members'])+' | '+r['state']+' |' for r in a['relations'])
    (out/'relacoes.md').write_text('\n'.join(rows)+'\n',encoding='utf-8')
    print(json.dumps(a['metrics'],ensure_ascii=False))


if __name__=='__main__':main()
