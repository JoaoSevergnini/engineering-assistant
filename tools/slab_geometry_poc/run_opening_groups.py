"""Stage 4 case runner: explicit office convention, no changes to prior artifacts."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
from run_sheet import ROOT,fitz,extract_page,save_json
from automatic import union
from opening_groups import reconstruct_localized,box_of


def draw(page,record,groups,holes,shift=(0,0),panel=None):
    def point(p):return fitz.Point(p[0]+shift[0],p[1]+shift[1])
    related={r['opening_id'] for id in record['group_ids'] for r in groups[id]['opening_relations']+groups[id]['opening_alternatives']}
    related.update(r['opening_id'] for r in record['opening_alternatives'])
    for id in related:
        h=holes[id];points=[point(p) for p in h['contour_pdf_pt']]
        shape=page.new_shape();shape.draw_polyline(points+[points[0]]);shape.finish(color=(0,.65,.65),width=1.1);shape.commit()
        page.insert_text((points[0].x+1,points[0].y-2),id,fontsize=6,color=(0,.5,.5))
    for s in record['leader']['segments']:
        page.draw_line(point(s['a']),point(s['b']),color=(0,.45,.85),width=1.2,dashes='[3 1] 0')
    for id in record['group_ids']:
        g=groups[id]
        for s in g['lines']:page.draw_line(point(s['a']),point(s['b']),color=(1,.4,0),width=1.4)
        box=union([box_of(s) for s in g['lines']]);at=point([(box[0]+box[2])/2,(box[1]+box[3])/2])
        side=g['opening_relations'][0]['side'] if g['opening_relations'] else 'UNKNOWN'
        x=at.x-32 if side=='LEFT' else at.x+5;y=at.y-4
        if panel:x=max(panel.x0+3,min(x,panel.x1-23));y=max(panel.y0+8,min(y,panel.y1-3))
        page.draw_line(at,fitz.Point(x,y-2),color=(.65,0,.7),width=.6,dashes='[2 2] 0')
        page.insert_text((x,y),g['display_id'],fontsize=7,color=(.65,0,.7))


def visuals(source,result,out):
    a=result['localized_reconstruction'];groups={g['id']:g for g in a['physical_groups']};holes={h['id']:h for h in a['opening_candidates']}
    occ={o['occurrence_id']:o for o in result['occurrences']}
    for record in a['representations']:
        o=occ[record['occurrence_id']];boxes=[o['bbox']]
        for s in record['leader']['segments']:boxes.extend([[*s['a'],*s['a']],[*s['b'],*s['b']]])
        related={r['opening_id'] for r in record['opening_alternatives']}
        for id in record['group_ids']:
            g=groups[id];boxes.extend(box_of(s) for s in g['lines']);related.update(r['opening_id'] for r in g['opening_relations']+g['opening_alternatives'])
        boxes.extend(holes[id]['bbox'] for id in related)
        b=union(boxes);clip=fitz.Rect(b[0]-35,b[1]-35,b[2]+35,b[3]+35)&source.rect
        w,h=clip.width,clip.height;footer=100+len(record['group_ids'])*12
        doc=fitz.open();p=doc.new_page(width=w*2+45,height=h+footer+60)
        title=f"{record['display_id']} / {record['mark']} / {record['reconstruction_state']}"
        p.insert_text((12,20),title,fontsize=min(11,(p.rect.width-24)/fitz.get_text_length(title,fontsize=1)))
        for x,title in [(15,'Original'),(w+30,'Contorno e tracos / grupos interpretados')]:
            p.insert_text((x,43),title,fontsize=min(10,(w-4)/fitz.get_text_length(title,fontsize=1)))
            pix=source.get_pixmap(matrix=fitz.Matrix(2,2),clip=clip)
            p.insert_image(fitz.Rect(x,55,x+w,55+h),stream=pix.tobytes('png'))
        draw(p,record,groups,holes,(w+30-clip.x0,55-clip.y0),fitz.Rect(w+30,55,w+30+w,55+h))
        y=h+76
        facts=f"PDF: {o['text']}"
        p.insert_text((15,y),facts,fontsize=min(9,(p.rect.width-30)/fitz.get_text_length(facts,fontsize=1)));y+=15
        for id in record['group_ids']:
            g=groups[id];layer=g['layer_distribution'];sides=','.join(r['opening_id']+':'+r['side'] for r in g['opening_relations']) or 'abertura pendente'
            content=f"{g['display_id']} {sides} | q={g['quantity_bars'] if g['quantity_bars'] is not None else '?'} | "
            content+=f"{layer['lower']} inf + {layer['upper']} sup [convencao SIM]" if layer['lower'] is not None else 'camadas desconhecidas'
            p.insert_text((15,y),content,fontsize=min(8,(p.rect.width-30)/fitz.get_text_length(content,fontsize=1)),color=(.65,0,.7));y+=12
        missing=record['multiplicity']['unlocated_group_count']
        note=f"Grupos indicados sem localizacao comprovada: {missing if missing is not None else 'desconhecido; fatores sem semantica confirmada'}"
        p.insert_text((15,y+3),note,fontsize=min(8,(p.rect.width-30)/fitz.get_text_length(note,fontsize=1)),color=(.8,.25,0))
        legend='Ciano continuo: contorno extraido | Azul tracejado: lider extraido | Laranja: tracos | Roxo tracejado: grupo/convencao interpretados'
        p.insert_text((15,y+19),legend,fontsize=min(8,(p.rect.width-30)/fitz.get_text_length(legend,fontsize=1)))
        zoom=min(3,2100/p.rect.width,1500/p.rect.height)
        p.get_pixmap(matrix=fitz.Matrix(zoom,zoom)).save(str(out/'ampliacoes'/f"{record['display_id']}_{record['mark']}.png"));doc.close()
    roi=fitz.Rect(result['layout']['detail_roi_pt']);doc=fitz.open();p=doc.new_page(width=roi.width,height=roi.height+50)
    p.insert_image(fitz.Rect(0,50,roi.width,roi.height+50),stream=source.get_pixmap(matrix=fitz.Matrix(1.6,1.6),clip=roi).tobytes('png'))
    p.insert_text((15,20),'Aberturas: contorno + X + reforcos de borda | Ciano: apoiadas geometricamente | Cinza: candidatas nao confirmadas',fontsize=12)
    for h in a['opening_candidates']:
        color=(0,.6,.6) if h['state']=='GRAPHICALLY_SUPPORTED_OPENING' else (.5,.5,.5)
        rect=fitz.Rect(h['bbox'])+(-roi.x0,50-roi.y0,-roi.x0,50-roi.y0)
        p.draw_rect(rect,color=color,width=1,dashes='[] 0' if color[0]==0 else '[3 2] 0')
        p.insert_text((rect.x0,rect.y0-3),h['id'],fontsize=9,color=color)
    p.get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(str(out/'aberturas.png'));doc.close()


def summaries(result,out):
    a=result['localized_reconstruction'];groups={g['id']:g for g in a['physical_groups']}
    lines=['# Grupos localizados: extração e interpretação','',
        'Grupos são hipóteses geométricas rastreáveis, pendentes de revisão do engenheiro. Dois traços não significam duas barras.','',
        '| Imagem | Posição | Fatores | Grupos localizados | Grupos sem localização | Convenção | Pendências |','|---|---|---|---|---|---|---|']
    for r in a['representations']:
        ids=', '.join(groups[id]['display_id'] for id in r['group_ids']) or '-';m=r['multiplicity']
        missing=m['unlocated_group_count'] if m['unlocated_group_count'] is not None else 'desconhecido'
        lines.append(f"| [{r['display_id']}](ampliacoes/{r['display_id']}_{r['mark']}.png) | {r['mark']} | {'x'.join(map(str,m['original_factors']))} | {ids} | {missing} | {'SIM 2 inf + 1 sup' if r['convention_applied'] else 'não aplicada'} | {', '.join(r['issues']) or '-'} |")
    (out/'associacoes.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    with (out/'grupos.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f,delimiter=';');w.writerow(['id','stable_id','position','representations','openings_and_sides','orientation','quantity_bars','diameter_mm','nominal_length_cm','lower','upper','quantity_origin','validation'])
        for g in a['physical_groups']:
            w.writerow([g['display_id'],g['id'],g['mark'],','.join(g['representation_ids']),','.join(r['opening_id']+':'+r['side'] for r in g['opening_relations']),g['orientation'],g['quantity_bars'],g['diameter_mm'],g['nominal_length_cm'],g['layer_distribution']['lower'],g['layer_distribution']['upper'],g['quantity_origin'],g['validation']['status']])


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('pdf',type=Path);p.add_argument('--previous',type=Path,default=ROOT/'analises/lajes_geometria_lideres/inventario.json')
    p.add_argument('--convention',type=Path);p.add_argument('--out',type=Path,default=ROOT/'analises/lajes_grupos_fisicos')
    args=p.parse_args();args.out.mkdir(parents=True,exist_ok=True);(args.out/'ampliacoes').mkdir(exist_ok=True)
    stage3=json.loads(args.previous.read_text(encoding='utf-8'));digest=hashlib.sha256(args.pdf.read_bytes()).hexdigest()
    if digest!=stage3['provenance']['sha256']:raise ValueError('previous_pdf_hash_mismatch')
    profile=json.loads(args.convention.read_text(encoding='utf-8')) if args.convention else None
    with fitz.open(args.pdf) as doc:
        data=extract_page(doc[0]);previous_data=json.loads(args.previous.with_name('entidades_pagina.json').read_text(encoding='utf-8'))
        canonical=lambda d:hashlib.sha256(json.dumps(d,sort_keys=True,ensure_ascii=False).encode('utf-8')).hexdigest()
        if canonical(data)!=canonical(previous_data):raise ValueError('extracted_entity_ids_or_geometry_changed')
        result=reconstruct_localized(stage3,data,profile)
        result['stage4_provenance']=dict(source_sha256=digest,stage3_file=str(args.previous.resolve()),
            stage3_sha256=hashlib.sha256(args.previous.read_bytes()).hexdigest(),raw_entities_sha256=canonical(data),
            convention_file=str(args.convention.resolve()) if args.convention else None,
            convention_file_sha256=hashlib.sha256(args.convention.read_bytes()).hexdigest() if args.convention else None,
            implementation_sha256={n:hashlib.sha256(Path(__file__).with_name(n).read_bytes()).hexdigest() for n in ('opening_groups.py','run_opening_groups.py')})
        result['distributed_preservation']=[dict(occurrence_id=o['occurrence_id'],display_id=o['display_id'],unchanged=o==stage3['occurrences'][i]) for i,o in enumerate(result['occurrences']) if o['representation_kind']=='DISTRIBUTED']
        visuals(doc[0],result,args.out);summaries(result,args.out)
        doc[0].get_pixmap(matrix=fitz.Matrix(3,3),clip=fitz.Rect(1440,1250,1720,1620)).save(str(args.out/'detalhe_furos_SIM.png'))
    result['stage4_source_unchanged']=hashlib.sha256(args.pdf.read_bytes()).hexdigest()==digest
    save_json(args.out/'inventario.json',result)
    for key,filename in [('opening_candidates','aberturas.json'),('physical_groups','grupos_fisicos.json'),('representations','reforcos_localizados.json')]:
        save_json(args.out/filename,result['localized_reconstruction'][key])
    print(json.dumps(result['localized_reconstruction']['metrics'],indent=2))


if __name__=='__main__':main()
