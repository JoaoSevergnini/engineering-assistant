"""Read all textual armature representations in the main plan, no selected marks."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tmp/pdf_deps'))
sys.path.insert(0,str(ROOT/'tools/beam_model'))
import fitz
from geometry import extract_page
from automatic import detect_layout, read_sheet, compare_schedule, union
from pdf_observations import extract_zones
from run_case import save_json

COLORS={'ASSOCIATED':(0,.5,.2),'PARTIAL':(.9,.45,0),'AMBIGUOUS':(.65,0,.75),'UNRESOLVED':(.85,0,.05)}
DASHES={'ASSOCIATED':'[] 0','PARTIAL':'[5 2] 0','AMBIGUOUS':'[2 2] 0','UNRESOLVED':'[1 2] 0'}


def annotation(page,o,shift=(0,0),show_candidates=False):
    color=COLORS[o['status']]
    def pt(v): return fitz.Point(v[0]+shift[0],v[1]+shift[1])
    box=o['bbox']; page.draw_rect(fitz.Rect(pt(box[:2]),pt(box[2:])),color=color,width=.8,dashes=DASHES[o['status']])
    if o['region_pdf_pt']:
        points=[pt(v) for v in o['region_pdf_pt']]
        shape=page.new_shape();shape.draw_polyline(points+[points[0]])
        shape.finish(color=color,fill=color,width=.7,fill_opacity=.035,dashes='[4 3] 0');shape.commit()
    if o.get('leader_search'):
        traces=o['leader_search']['traces'] if show_candidates else [o['leader_association']['trace']] if o.get('leader_association') else []
        for trace in traces:
            for line in trace['segments']:
                page.draw_line(pt(line['a']),pt(line['b']),color=(0,.5,.85),width=1.5,dashes='[3 1] 0')
            page.draw_circle(pt(trace['tip']),2,color=(0,.5,.85),width=.7)
        targets=o.get('leader_candidates',[]) if show_candidates else [o['leader_association']] if o.get('leader_association') else []
        for ci,c in enumerate(targets,1):
            for line in c['graphic_group']:
                page.draw_line(pt(line['a']),pt(line['b']),color=(1,.35,0),width=1.6)
            at=pt(c['terminal_contact']['centerline_contact'])
            if show_candidates:page.insert_text((at.x+2,at.y-2),f'T{ci}',color=(1,.35,0),fontsize=6)
            for ev in c['distribution_candidates']:
                axis=ev['axis'];page.draw_line(pt(axis['a']),pt(axis['b']),color=(.9,0,.7),width=1)
        return
    candidates=o['candidates'] if show_candidates else [dict(bar=p['bar'],distribution_candidates=[p['evidence']]) for p in o['associations']] if o['status']=='ASSOCIATED' else []
    for ci,c in enumerate(candidates,1):
        page.draw_line(pt(c['bar']['a']),pt(c['bar']['b']),color=color,width=1.3)
        if show_candidates:
            a,b=c['bar']['a'],c['bar']['b']
            at=pt([(a[0]+b[0])/2,(a[1]+b[1])/2])
            page.insert_text((at.x,at.y-2),f'B{ci}',color=color,fontsize=6)
        for ev in c['distribution_candidates']:
            axis=ev['axis'];page.draw_line(pt(axis['a']),pt(axis['b']),color=(.9,0,.7),width=1)
            page.draw_circle(pt(ev['intersection_pt']),2.2,color=(0,0,0),width=.7)


def overview(source,occurrences,out):
    doc=fitz.open();page=doc.new_page(width=source.rect.width,height=source.rect.height+65)
    image=source.get_pixmap(matrix=fitz.Matrix(1.5,1.5)).tobytes('png')
    page.insert_image(fitz.Rect(0,65,source.rect.width,source.rect.height+65),stream=image)
    page.insert_text((35,22),'Inventario automatico - IDs sao representacoes textuais; conferir tabela e ampliacoes',fontsize=15)
    x=35
    for status in COLORS:
        page.insert_text((x,47),status,color=COLORS[status],fontsize=13);x+=290
    if any('representation_kind' in o for o in occurrences):
        page.insert_text((35,61),'Caixas: situacao | Azul tracejado: lider | Laranja: tracos do destino | Magenta: faixa | Localizadas sem envoltoria',fontsize=11)
    occupied=[]
    for o in occurrences:
        annotation(page,o,(0,65))
        box=o['bbox'];cx=(box[0]+box[2])/2;cy=(box[1]+box[3])/2+65
        text=o['display_id']+' '+o['documentary_mark'];w=fitz.get_text_length(text,fontsize=8)+5
        options=[]
        for dy in (-17,17,-30,30,-45,45,-60,60):
            for dx in (-w/2,10,-w-10):
                r=fitz.Rect(cx+dx,cy+dy-9,cx+dx+w,cy+dy+3)
                if r.x0>=30 and r.x1<1890 and not any(r.intersects(q) for q in occupied): options.append(r)
            if options:break
        r=options[0] if options else fitz.Rect(cx,cy-9,cx+w,cy+3)
        occupied.append(r)
        page.draw_line(fitz.Point(cx,cy),fitz.Point((r.x0+r.x1)/2,(r.y0+r.y1)/2),color=COLORS[o['status']],width=.5)
        page.draw_rect(r,color=COLORS[o['status']],fill=(1,1,1),width=.5)
        page.insert_text((r.x0+2,r.y1-2),text,fontsize=8,color=COLORS[o['status']])
    page.get_pixmap(matrix=fitz.Matrix(1.6,1.6)).save(str(out/'prancha_inventariada.png'))
    doc.close()


def zoom(source,o,out):
    boxes=[o['bbox']]
    if o.get('leader_search',{}).get('traces'):
        for t in o['leader_search']['traces']:
            for s in t['segments']:boxes.extend([[*s['a'],*s['a']],[*s['b'],*s['b']]])
        for c in o.get('leader_candidates',[]):
            for s in c['graphic_group']:boxes.extend([[*s['a'],*s['a']],[*s['b'],*s['b']]])
            for ev in c['distribution_candidates']:
                s=ev['axis'];boxes.extend([[*s['a'],*s['a']],[*s['b'],*s['b']]])
        old_candidates=[]
    else:old_candidates=o['candidates']
    for c in old_candidates:
        boxes.append(union([[*c['bar']['a'],*c['bar']['a']],[*c['bar']['b'],*c['bar']['b']]]))
        for ev in c['distribution_candidates']:
            axis=ev['axis'];boxes.append(union([[*axis['a'],*axis['a']],[*axis['b'],*axis['b']]]))
    b=union(boxes);clip=fitz.Rect(max(30,b[0]-35),max(140,b[1]-40),min(1884,b[2]+35),min(1245,b[3]+40))
    w,h=clip.width,clip.height
    doc=fitz.open();p=doc.new_page(width=2*w+45,height=h+90)
    for x,title in [(15,'Original'),(w+30,'Candidatas e evidencias')]:
        image=source.get_pixmap(matrix=fitz.Matrix(2,2),clip=clip).tobytes('png')
        p.insert_image(fitz.Rect(x,55,x+w,55+h),stream=image)
        p.insert_text((x,45),title,fontsize=min(10,(w-5)/fitz.get_text_length(title,fontsize=1)))
    heading=o['display_id']+' / '+o['occurrence_id']+' / '+o['documentary_mark']+' / '+o['status']
    p.insert_text((15,20),heading,fontsize=min(11,(p.rect.width-30)/fitz.get_text_length(heading,fontsize=1)),color=COLORS[o['status']])
    annotation(p,o,(w+30-clip.x0,55-clip.y0),show_candidates=True)
    legend='Azul tracejado: lider | Laranja: destinos candidatos | Magenta: faixa | T1/T2: alternativas, nao quantidade de barras.' if 'leader_search' in o else 'Cor da situacao: candidatas de barra | Magenta: eixos | Circulos pretos: cruzamentos; nao significam vinculo aprovado.'
    p.insert_text((15,h+77),legend,fontsize=min(8,(2*w+15)/fitz.get_text_length(legend,fontsize=1)))
    scale=min(3,1800/p.rect.width,1400/p.rect.height)
    p.get_pixmap(matrix=fitz.Matrix(scale,scale)).save(str(out/'ampliacoes'/f"{o['display_id']}_{o['documentary_mark']}_{o['status']}.png"))
    doc.close()


def write_summary(result,out):
    columns=['id','occurrence_id','position','quantity_expression','diameter_mm','spacing_cm','length_cm','status','bar_candidates','complete_pairs','reason','visual_review']
    rows=[]
    for o in result['occurrences']:
        c=o['call'];rows.append([o['display_id'],o['occurrence_id'],o['documentary_mark'],c['quantity_expression'],c['diameter_mm'],c['spacing_cm'],c['nominal_length_cm'],o['status'],len(o['candidates']),len(o['associations']),o['reason'],o['manual_validation']['status']])
    with (out/'associacoes.csv').open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.writer(f,delimiter=';');writer.writerow(columns);writer.writerows(rows)
    lines=['# Resumo das representações detectadas','',
           'IDs Oxxx localizam chamadas; não comprovam identidade física. ASSOCIATED não significa validação pelo engenheiro.','',
           '| ID | Ocorrência | Posição | Qtd. impressa | Ø mm | s cm | C cm | Situação | Candidatas | Conferência visual |',
           '|---|---|---|---|---|---|---|---|---|---|']
    for o,row in zip(result['occurrences'],rows):
        link=f"[imagem](ampliacoes/{o['display_id']}_{o['documentary_mark']}_{o['status']}.png)"
        lines.append('| '+' | '.join(str(v) if v is not None else '-' for v in [row[0]+' '+link,*row[1:8],row[8],row[11]])+' |')
    (out/'associacoes.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdf',type=Path)
    parser.add_argument('--out',type=Path,default=ROOT/'analises/lajes_geometria_automatico')
    parser.add_argument('--validation',type=Path,help='Optional separate review ledger; never changes algorithmic statuses')
    args=parser.parse_args();args.out.mkdir(parents=True,exist_ok=True);(args.out/'ampliacoes').mkdir(exist_ok=True)
    digest=hashlib.sha256(args.pdf.read_bytes()).hexdigest()
    with fitz.open(args.pdf) as doc:
        page=doc[0];data=extract_page(page);layout=detect_layout(data['texts'],list(page.rect))
        result=read_sheet(data,layout)
        for i,o in enumerate(result['occurrences'],1): o['display_id']=f'O{i:03}'
        schedule=extract_zones(args.pdf,[dict(id='AUTO_STEEL_TABLE',page=0,bbox=layout['steel_table_roi_pt'],
            view='STEEL_SCHEDULE',quantity_scope='POSITION_TOTAL',integrity='UNVERIFIED',
            columns=['mark','diameter_mm','quantity','nominal_length_cm','total_length_cm'])])
        result['steel_schedule']=schedule
        result['schedule_comparison']=compare_schedule(result['occurrences'],schedule['observations'])
        result['provenance']=dict(file=str(args.pdf.resolve()),sha256=digest,page=1,page_rect_pt=list(page.rect),
            rotation=page.rotation,engine=fitz.__doc__,coordinate_system='PyMuPDF points; top left; x right; y down',
            implementation_sha256={name:hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest() for name in ('geometry.py','automatic.py','run_sheet.py')},
            selection='ALL_CALL_LIKE_TEXTS_IN_ANCHOR_DERIVED_MAIN_PLAN_ROI')
        result['experimental_criteria']=dict(text_gap_pt=[-3,22],complete_max_gap_pt=8,
            min_text_overlap_pt='min(15, 35% of projected text width)',axis_alignment_pt=.15,
            fragment_gap_max_pt=.3,protect_arrow_tips_from_merging=True,junction_center_distance_pt=.42,
            marker_absent='PARTIAL_OR_AMBIGUOUS',nominal_length='auxiliary; equality not required',
            projected_over_nominal_ratio_review_threshold=1.05)
        result['metrics']=dict(candidate_calls=len(result['occurrences']),parsed_calls=sum(o['call']['parse_complete'] for o in result['occurrences']),
            positions=len({o['documentary_mark'] for o in result['occurrences']}),**result['status_counts'],
            orphan_call_fragments=len(result['unowned_continuations']),reference_inventory=None,coverage=None,
            accuracy=None,independent_engineer_validations=0)
        if args.validation:
            ledger=json.loads(args.validation.read_text(encoding='utf-8'))
            if ledger['source_sha256']!=digest: raise ValueError('review_ledger_source_mismatch')
            for o in result['occurrences']:
                if o['occurrence_id'] in ledger['reviews']:
                    review=ledger['reviews'][o['occurrence_id']]
                    selected=review.get('selected_pair')
                    if selected and not any(p['bar']['id']==selected['bar_id'] and p['evidence']['axis']['id']==selected['axis_id'] for p in o['associations']):
                        raise ValueError('review_geometry_changed:'+o['occurrence_id'])
                    o['manual_validation']=review
            result['review_ledger']=str(args.validation.resolve())
        result['metrics']['assistant_visual_supported']=sum(o['manual_validation']['status']=='VISUALLY_SUPPORTED_ASSISTANT' for o in result['occurrences'])
        result['metrics']['assistant_reviewed_total']=sum(o['manual_validation']['status']!='PENDING' for o in result['occurrences'])
        result['source_unchanged']=hashlib.sha256(args.pdf.read_bytes()).hexdigest()==digest
        save_json(args.out/'inventario.json',result)
        save_json(args.out/'entidades_pagina.json',data)
        save_json(args.out/'validacao_manual_modelo.json',dict(source_sha256=digest,
            instructions='Independent engineer review; keep algorithm result intact; use CORRECT/INCORRECT/INCONCLUSIVE and identify chosen geometry.',
            reviews={o['occurrence_id']:dict(status='PENDING',reviewer=None,method=None,selected_pair=None,notes=None) for o in result['occurrences']}))
        overview(page,result['occurrences'],args.out)
        for o in result['occurrences']: zoom(page,o,args.out)
        write_summary(result,args.out)
        print(json.dumps(result['metrics'],indent=2))


if __name__=='__main__':main()
