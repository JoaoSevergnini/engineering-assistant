"""Stage 8 runner. Reference loaded only after source-only candidates are saved."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
from run_sheet import ROOT,fitz,save_json
from run_structural_regions import canvas,box,write_png
from run_relations import draw_geometry
from polygonal_slabs import shape,geo
from complex_slab_contours import recognize


def plot_candidates(source,analysis,out):
    doc,page,clip=canvas(source,[50,145,1910,1205])
    for i,s in enumerate(analysis['slabs']):
        color=((i*37%130+40)/255,(i*71%130+40)/255,(i*97%130+40)/255)
        box(page,s['label_block_pdf_pt'],clip,s['name'],color,True)
        for c in s['candidates']:draw_geometry(page,c['geometry_pdf_pt'],clip,color,dashed=True)
    write_png(doc,page,out/'contornos_candidatos.png','Todos os contornos tracejados sao candidatos automaticos, sem confirmacao automatica | Nenhum segmento de fechamento inserido')


def plot_validation(source,candidate,reference,metrics,out):
    bounds=shape(candidate['geometry_pdf_pt']).bounds;clip=fitz.Rect(bounds[0]-35,bounds[1]-45,bounds[2]+35,bounds[3]+35)&source.rect
    w,h=clip.width,clip.height
    doc=fitz.open();page=doc.new_page(width=2*w+24,height=h+65)
    pix=source.get_pixmap(matrix=fitz.Matrix(1.3,1.3),clip=clip)
    for x,title in [(0,'Referencia humana: digitalizacao aproximada'),(w+24,'Automatico azul + referencia vermelha tracejada')]:
        page.insert_image(fitz.Rect(x,25,x+w,25+h),stream=pix.tobytes('png'))
        page.insert_text((x+8,15),title,fontsize=11)
    left=fitz.Rect(clip.x0,clip.y0-25,clip.x1,clip.y1-25)
    right=fitz.Rect(clip.x0-w-24,clip.y0-25,clip.x1-w-24,clip.y1-25)
    draw_geometry(page,reference,left,(.9,0,0))
    draw_geometry(page,reference,right,(.9,0,0),dashed=True)
    draw_geometry(page,candidate['geometry_pdf_pt'],right,(0,.3,.85))
    text=f"IoU = {metrics['intersection_over_union']:.4f} | Hausdorff exterior = {metrics['exterior_hausdorff_distance_pt']:.2f} pt | Candidato nao validado automaticamente"
    page.insert_text((8,h+49),text,fontsize=10)
    page.get_pixmap(matrix=fitz.Matrix(1.3,1.3)).save(str(out/'comparacao_L603.png'));doc.close()
    doc,page,c=canvas(source,clip)
    draw_geometry(page,metrics['candidate_only_geometry_pdf_pt'],c,(0,.35,.85))
    draw_geometry(page,metrics['reference_only_geometry_pdf_pt'],c,(.9,.4,0))
    write_png(doc,page,out/'diferencas_L603.png','Azul: apenas automatico | Laranja: apenas referencia | Divergencias incluem digitalizacao manual e aneis internos nao desenhados na referencia')
    x,y=metrics['largest_vertex_discrepancy']['point_pdf_pt']
    doc,page,c=canvas(source,fitz.Rect(x-230,y-150,x+230,y+150)&source.rect)
    draw_geometry(page,reference,c,(.9,0,0),dashed=True);draw_geometry(page,candidate['geometry_pdf_pt'],c,(0,.3,.85))
    write_png(doc,page,out/'maior_divergencia.png','Azul: automatico | Vermelho: referencia | Recorte local pendente de revisao')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--inventory',default=str(ROOT/'analises/lajes_relacoes_contornos/inventario.json'));parser.add_argument('--entities',default=str(ROOT/'analises/lajes_geometria_lideres/entidades_pagina.json'));parser.add_argument('--out',default=str(ROOT/'analises/lajes_contornos_complexos'));parser.add_argument('--reference-profile',default=str(ROOT/'analises/lajes_l603_confirmada/confirmacao_joao_L603.json'));parser.add_argument('--skip-reference',action='store_true');args=parser.parse_args()
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True);inp=Path(args.inventory);ent=Path(args.entities)
    inventory=json.loads(inp.read_text(encoding='utf-8'));data=json.loads(ent.read_text(encoding='utf-8'))
    source=Path(inventory['stage5_provenance']['source_pdf']);before=hashlib.sha256(source.read_bytes()).hexdigest()
    if before!=inventory['stage5_provenance']['sha256']:raise ValueError('SOURCE_PDF_CHANGED')
    analysis=recognize(inventory,data)
    # Independent automatic artifact exists before any reference is read.
    save_json(out/'candidatos_automaticos.json',analysis)
    baseline=recognize(inventory,data,minimum_inside_fraction=1.0)
    comparison={'strict_endpoint_context':baseline['metrics'],'complete_crossing_entities':analysis['metrics']}
    old_review=ROOT/'analises/lajes_revisao_contornos/revisao.json'
    if old_review.exists():
        old=json.loads(old_review.read_text(encoding='utf-8'));checks=[]
        for s in analysis['slabs']:
            prior=next((v for v in old['slabs'] if v['name']==s['name']),None)
            exact=bool(prior) and sorted(json.dumps(c['geometry_pdf_pt'],sort_keys=True) for c in s['candidates'])==sorted(json.dumps(c['geometry_pdf_pt'],sort_keys=True) for c in prior['contour_review_candidates'])
            checks.append({'slab':s['name'],'exactly_preserved_from_previous_review':exact,'previous_candidate_count':len(prior['contour_review_candidates']) if prior else None,'current_candidate_count':len(s['candidates'])})
        comparison['previous_review_regressions']=checks
    result=copy.deepcopy(inventory);result['complex_slab_contour_analysis']=analysis
    result['stage8_provenance']={'source_pdf_sha256':before,'input_inventory_sha256':hashlib.sha256(inp.read_bytes()).hexdigest(),'entities_sha256':hashlib.sha256(ent.read_bytes()).hexdigest(),
        'prior_layers_preserved':all(result[k]==v for k,v in inventory.items()),'recognition_uses_reference':False}
    with fitz.open(str(source)) as pdf:
        plot_candidates(pdf[0],analysis,out)
        if not args.skip_reference:
            from confirmed_slab_outline import register_outline
            from contour_validation import compare
            profile=json.loads(Path(args.reference_profile).read_text(encoding='utf-8'))
            if profile['pdf_sha256']!=before:raise ValueError('REFERENCE_DOCUMENT_MISMATCH')
            reference,registration=register_outline(profile)
            slab=next((s for s in analysis['slabs'] if s['name']==profile['slab']),None)
            if slab and len(slab['candidates'])==1:
                c=slab['candidates'][0];evaluation=compare(c['geometry_pdf_pt'],geo(reference),profile['boundary_uncertainty_pdf_pt'])
                evaluation.update(slab=slab['name'],candidate_id=c['id'],reference_registration=registration,reference_sha256=hashlib.sha256(Path(args.reference_profile).read_bytes()).hexdigest())
                visual_reference=Path(args.reference_profile).parent/(profile['slab']+'_contorno_confirmado.png')
                if visual_reference.exists():evaluation['reference_visual_sha256']=hashlib.sha256(visual_reference.read_bytes()).hexdigest()
                save_json(out/'comparacao_referencia.json',evaluation);plot_validation(pdf[0],c,geo(reference),evaluation,out)
                # Diagnostic zoom selected by recovered source IDs, never fixed slab vertices.
                ids=set(c['crossing_roi_segment_ids']);records=[s for s in analysis['linework'] if s['id'] in ids]
                if records:
                    xs=[p[0] for s in records for p in (s['a'],s['b'])];ys=[p[1] for s in records for p in (s['a'],s['b'])];cx=(min(xs)+max(xs))/2;cy=(min(ys)+max(ys))/2
                    doc,page,clip=canvas(pdf[0],fitz.Rect(cx-160,cy-100,cx+160,cy+100)&pdf[0].rect)
                    draw_geometry(page,c['geometry_pdf_pt'],clip,(0,.3,.85))
                    for s in records:page.draw_line(fitz.Point(s['a'][0]-clip.x0,s['a'][1]-clip.y0),fitz.Point(s['b'][0]-clip.x0,s['b'][1]-clip.y0),color=(0,.7,.4),width=2)
                    x=analysis['context_audit']['roi_pdf_pt'][2]-clip.x0
                    page.draw_line(fitz.Point(x,0),fitz.Point(x,clip.height),color=(.8,.1,.1),dashes='[3 2] 0')
                    write_png(doc,page,out/'borda_recuperada.png','Verde: borda original | Vermelho: limite antigo da ROI | Azul: candidato')
    assert before==hashlib.sha256(source.read_bytes()).hexdigest()
    save_json(out/'inventario.json',result);save_json(out/'comparacao_etapas.json',comparison)
    print(json.dumps(analysis['metrics']));print(comparison.get('previous_review_regressions'))


if __name__=='__main__':main()
