"""Reproducible stage 6 inventories and PNG review aids, no source PDF edits."""
import argparse
import hashlib
import json
from pathlib import Path
from collections import Counter
from run_sheet import ROOT,fitz,save_json
from structural_regions import interpret

COLORS={'SINGLE_DISTRIBUTED':(.15,.5,.8),'BASE_PLUS_REINFORCEMENT':(0,.65,.25),
        'LAP_SPLICE':(.9,.4,0),'GRAPHICAL_RESIDUAL':(.7,0,.7),'UNDETERMINED':(.65,.65,.65)}


def canvas(source,clip):
    clip=fitz.Rect(clip);doc=fitz.open();page=doc.new_page(width=clip.width,height=clip.height+38)
    pix=source.get_pixmap(matrix=fitz.Matrix(1.5,1.5),clip=clip)
    page.insert_image(fitz.Rect(0,0,clip.width,clip.height),stream=pix.tobytes('png'))
    return doc,page,clip


def box(page,b,clip,label,color,dashed=False):
    if not fitz.Rect(b).intersects(clip):return
    rect=fitz.Rect(b[0]-clip.x0,b[1]-clip.y0,b[2]-clip.x0,b[3]-clip.y0)
    page.draw_rect(rect,color=color,fill=color,fill_opacity=.16,width=.9,dashes='[3 2] 0' if dashed else None)
    if label:page.insert_text((max(2,rect.x0+2),max(8,rect.y0+8)),label,fontsize=7,color=color)


def write_png(doc,page,path,note):
    page.insert_text((8,page.rect.height-23),note,fontsize=min(9,(page.rect.width-16)/max(fitz.get_text_length(note,fontsize=1),1)))
    page.insert_text((8,page.rect.height-9),'Interpretacao preliminar | sem calculo resistente | coordenadas PDF preservadas',fontsize=min(8,(page.rect.width-16)/380))
    page.get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(str(path));doc.close()


def visuals(source,result,out):
    a=result['structural_interpretation'];spatial=result['distributed_spatial_analysis'];cells=spatial['composition_regions']
    ci={c['id']:c for c in cells};ii={i['composition_id']:i for i in a['overlap_interpretations']};ri={r['id']:r for r in spatial['regions']}
    roi=[50,145,1900,1205]
    doc,p,clip=canvas(source,roi)
    for s in a['slabs']:
        box(p,s['label']['bbox'],clip,s['name']+' h:'+str(s['thickness_cm']),(.1,.2,.8))
        if s['contour']:box(p,s['contour']['bbox'],clip,s['name']+' contorno preliminar',(0,.6,.4))
        else:
            for j,c in enumerate(s['contour_alternatives']):box(p,c['bbox'],clip,s['name']+' alternativa '+str(j+1),(.8,.5,.1),True)
    write_png(doc,p,out/'lajes_preliminares.png','Azul: nome/espessura extraidos | Verde: contorno candidato unico | Laranja tracejado: alternativas')
    doc,p,clip=canvas(source,roi)
    for f in a['function_candidates']:
        if f['role_candidate']!='UNKNOWN':box(p,ri[f['region_id']]['bbox'],clip,f['region_id']+' '+f['role_candidate'],(.15,.45,.8) if f['role_candidate']=='BASE' else (.8,.15,.1),True)
    write_png(doc,p,out/'base_reforco_candidatos.png','Funcoes apenas candidatas: geometria + evidencia documental quando disponivel; nao sao validacoes humanas')
    for name,allowed in [('composicao_estrutural',set(COLORS)),('traspasses',{'LAP_SPLICE'}),('residuais',{'GRAPHICAL_RESIDUAL'}),('pendentes',{'UNDETERMINED'})]:
        doc,p,clip=canvas(source,roi)
        for c in cells:
            i=ii[c['id']]
            if i['classification'] in allowed:box(p,c['bbox'],clip,c['id'],COLORS[i['classification']],i['validation_state']!='ENGINEER_CONFIRMED')
        write_png(doc,p,out/(name+'.png'),'Verde: base+reforco | Laranja: traspasse | Roxo: residual | Cinza: pendente | Azul: uma identidade')
    for i in a['overlap_interpretations']:
        if i['validation_state']!='ENGINEER_CONFIRMED':continue
        c=ci[i['composition_id']];b=c['bbox'];cx=(b[0]+b[2])/2;cy=(b[1]+b[3])/2;w=max(410,b[2]-b[0]+100);h=max(300,b[3]-b[1]+100)
        clip=fitz.Rect(cx-w/2,cy-h/2,cx+w/2,cy+h/2)&source.rect
        doc=fitz.open();p=doc.new_page(width=clip.width*2+20,height=clip.height+62)
        pix=source.get_pixmap(matrix=fitz.Matrix(1.7,1.7),clip=clip)
        for x in (0,clip.width+20):p.insert_image(fitz.Rect(x,0,x+clip.width,clip.height),stream=pix.tobytes('png'))
        shift=fitz.Rect(clip.x0-clip.width-20,clip.y0,clip.x1-clip.width-20,clip.y1)
        # Draw on second panel with explicit coordinates, avoiding false clipping.
        bb=fitz.Rect(b[0]-shift.x0,b[1]-shift.y0,b[2]-shift.x0,b[3]-shift.y0)
        p.draw_rect(bb,color=COLORS[i['classification']],fill=COLORS[i['classification']],fill_opacity=.3,width=1.4)
        p.insert_text((8,clip.height+16),'Original | Interpretacao: '+c['id']+' '+i['classification'],fontsize=10)
        p.insert_text((8,clip.height+30),'Confirmacao humana: Joao | '+', '.join(c['occurrences'])+' | sem autorizacao global de soma',fontsize=9)
        write_png(doc,p,out/(c['id']+'_confirmacao.png'),'A classificacao humana nao estabelece por si so camada, identidade fisica global ou conformidade normativa')
    for check in a['containment_checks']:
        if not check['uncovered_polygons_pdf_pt']:continue
        r=ri[check['reinforcement_id']];b=r['bbox'];cx=(b[0]+b[2])/2;cy=(b[1]+b[3])/2
        w=max(650,b[2]-b[0]+100);h=max(250,b[3]-b[1]+100)
        clip=fitz.Rect(cx-w/2,cy-h/2,cx+w/2,cy+h/2)&source.rect
        doc,p,clip=canvas(source,clip)
        for id in check['base_region_ids']:box(p,ri[id]['bbox'],clip,'',(.1,.4,.8),True)
        box(p,b,clip,'',(.8,.3,.1),True)
        for poly in check['uncovered_polygons_pdf_pt']:
            box(p,[poly[0][0],poly[0][1],poly[2][0],poly[2][1]],clip,'',(.8,0,.5))
        write_png(doc,p,out/(r['id']+'_contencao.png'),'Azul: '+','.join(check['base_region_ids'])+' base candidata | Laranja: '+r['id']+' reforco candidato | Roxo: descoberta; nao comprova insuficiencia')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--inventory',default=str(ROOT/'analises/lajes_regioes_distribuidas/inventario.json'));parser.add_argument('--entities',default=str(ROOT/'analises/lajes_geometria_lideres/entidades_pagina.json'));parser.add_argument('--reviews',default=str(ROOT/'analises/lajes_interpretacao_estrutural/validacoes_engenheiro.json'));parser.add_argument('--out',default=str(ROOT/'analises/lajes_interpretacao_estrutural'));args=parser.parse_args()
    inv=Path(args.inventory);entities=Path(args.entities);reviews=Path(args.reviews);out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    prior=json.loads(inv.read_text(encoding='utf-8'));data=json.loads(entities.read_text(encoding='utf-8'));profile=json.loads(reviews.read_text(encoding='utf-8')) if reviews.exists() else {}
    result=interpret(prior,data,profile);a=result['structural_interpretation'];source=Path(prior['stage5_provenance']['source_pdf']);before=hashlib.sha256(source.read_bytes()).hexdigest()
    if before!=prior['stage5_provenance']['sha256']:raise ValueError('SOURCE_PDF_CHANGED')
    result['stage6_provenance']={'source_sha256':before,'input_inventory_sha256':hashlib.sha256(inv.read_bytes()).hexdigest(),'entities_sha256':hashlib.sha256(entities.read_bytes()).hexdigest(),'reviews_sha256':hashlib.sha256(reviews.read_bytes()).hexdigest() if reviews.exists() else None,
        'occurrences_preserved':result['occurrences']==prior['occurrences'],'geometric_partition_preserved':result['distributed_spatial_analysis']==prior['distributed_spatial_analysis'],'n38_preserved':result['stage5_documentary_consistency']==prior['stage5_documentary_consistency']}
    with fitz.open(str(source)) as pdf:visuals(pdf[0],result,out)
    if hashlib.sha256(source.read_bytes()).hexdigest()!=before:raise ValueError('SOURCE_PDF_CHANGED_DURING_RUN')
    save_json(out/'inventario.json',result)
    for filename,key in [('lajes','slabs'),('classificacoes','overlap_interpretations'),('contencao','containment_checks'),('regioes_consolidadas','consolidated_regions'),('funcoes_candidatas','function_candidates')]:save_json(out/(filename+'.json'),a[key])
    rows=['| Composição | Classificação | Validação | Hipóteses automáticas |','|---|---|---|---|']
    rows.extend('| '+i['composition_id']+' | '+i['classification']+' | '+i['validation_state']+' | '+', '.join(i['automatic']['proposals'])+' |' for i in a['overlap_interpretations'])
    (out/'classificacoes.md').write_text('\n'.join(rows)+'\n',encoding='utf-8')
    print(json.dumps(a['metrics'],ensure_ascii=False))


if __name__=='__main__':main()
