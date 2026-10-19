"""Stage 3 runner; preserve earlier case artifacts and compare every occurrence."""
import argparse
import copy
import csv
import hashlib
import json
from pathlib import Path
from run_sheet import (ROOT,fitz,extract_page,detect_layout,extract_zones,compare_schedule,
                       save_json,overview,zoom)
from leaders import read_sheet_with_leaders,compare_previous


def summary(result,out):
    fields=['id','occurrence_id','mark','before','after','representation_kind','leader_ids','target_ids','review']
    rows=[]
    for o in result['occurrences']:
        leader=o['leader_association']
        rows.append([o['display_id'],o['occurrence_id'],o['documentary_mark'],o['previous_interpretation']['status'],o['status'],
            o['representation_kind'],','.join(leader['trace']['segment_ids']) if leader else '',
            ','.join(line['id'] for line in o['associated_lines']),o['manual_validation']['status']])
    with (out/'associacoes.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f,delimiter=';');w.writerow(fields);w.writerows(rows)
    content=['# Etapa 3: representações e trajetórias','',
        'ASSOCIATED é uma interpretação experimental, não aprovação do engenheiro. Linhas localizadas são traços gráficos, não contagem física de barras.','',
        '| ID / imagem | Posição | Antes | Depois | Tipo | Líder | Destinos aceitos | Conferência |','|---|---|---|---|---|---|---|---|']
    for row in rows:
        id,occ,mark,before,after,kind,leader,targets,review=row
        content.append(f'| [{id}](ampliacoes/{id}_{mark}_{after}.png) | {mark} | {before} | {after} | {kind} | {leader or "-"} | {targets or "-"} | {review} |')
    (out/'associacoes.md').write_text('\n'.join(content)+'\n',encoding='utf-8')


def apply_reviews(result,previous,ledger):
    old={o['occurrence_id']:o for o in previous['occurrences']}
    if ledger and ledger['source_sha256']!=result['provenance']['sha256']:raise ValueError('review_source_mismatch')
    for o in result['occurrences']:
        prior=old[o['occurrence_id']];o['prior_validation']=prior['manual_validation']
        if prior['status']=='ASSOCIATED' and o['associations']==prior['associations'] and o['status']=='ASSOCIATED':
            o['manual_validation']=dict(copy.deepcopy(prior['manual_validation']),carried_from_stage2=True)
        if ledger and o['occurrence_id'] in ledger['reviews']:
            review=ledger['reviews'][o['occurrence_id']]
            selected=review.get('selected_leader')
            if selected:
                c=o.get('leader_association')
                if not c or c['trace']['segment_ids']!=selected['segment_ids'] or c['target']['id']!=selected['target_id']:
                    raise ValueError('review_geometry_changed:'+o['occurrence_id'])
            o['manual_validation']=review


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('pdf',type=Path)
    p.add_argument('--previous',type=Path,default=ROOT/'analises/lajes_geometria_automatico/inventario.json')
    p.add_argument('--out',type=Path,default=ROOT/'analises/lajes_geometria_lideres')
    p.add_argument('--validation',type=Path)
    args=p.parse_args();args.out.mkdir(parents=True,exist_ok=True);(args.out/'ampliacoes').mkdir(exist_ok=True)
    previous=json.loads(args.previous.read_text(encoding='utf-8'));digest=hashlib.sha256(args.pdf.read_bytes()).hexdigest()
    if previous['provenance']['sha256']!=digest:raise ValueError('baseline_source_mismatch')
    with fitz.open(args.pdf) as doc:
        page=doc[0];data=extract_page(page);layout=detect_layout(data['texts'],list(page.rect))
        result=read_sheet_with_leaders(data,layout)
        if {o['occurrence_id'] for o in result['occurrences']}!={o['occurrence_id'] for o in previous['occurrences']}:raise ValueError('occurrence_identity_changed')
        for i,o in enumerate(result['occurrences'],1):o['display_id']=f'O{i:03}'
        result['comparison']=compare_previous(result,previous)
        result['steel_schedule']=extract_zones(args.pdf,[dict(id='STAGE3_TABLE',page=0,bbox=layout['steel_table_roi_pt'],view='STEEL_SCHEDULE',quantity_scope='POSITION_TOTAL',integrity='UNVERIFIED',columns=['mark','diameter_mm','quantity','nominal_length_cm','total_length_cm'])])
        result['schedule_comparison']=compare_schedule(result['occurrences'],result['steel_schedule']['observations'])
        result['provenance']=dict(file=str(args.pdf.resolve()),sha256=digest,page=1,page_rect_pt=list(page.rect),rotation=page.rotation,
            engine=fitz.__doc__,coordinate_system='PyMuPDF points; top left; x right; y down',previous_file=str(args.previous.resolve()),
            previous_sha256=hashlib.sha256(args.previous.read_bytes()).hexdigest(),
            implementation_sha256={n:hashlib.sha256(Path(__file__).with_name(n).read_bytes()).hexdigest() for n in ('geometry.py','automatic.py','leaders.py','run_sheet.py','run_leaders.py')})
        result['leader_criteria']=dict(endpoint_connection_pt=.2,shoulder_baseline_gap_pt=[-3.5,5.5],shoulder_overlap_min=.65,
            terminal_shaft_extension_max_pt=2,terminal_centerline_offset_max_pt=1.5,group_equal_extent_pt=.3,group_parallel_separation_max_pt=4,
            max_segments=8,max_length_pt=600,max_states=256,limit_policy='BLOCK_ACCEPTANCE',interior_crossings='NO_GRAPH_SWITCH',
            localized_geometry='TARGETED_STROKES_ONLY; NO_RECTANGULAR_ENVELOPE; PHYSICAL_MULTIPLICITIES_UNRESOLVED')
        ledger=json.loads(args.validation.read_text(encoding='utf-8')) if args.validation else None
        apply_reviews(result,previous,ledger)
        result['metrics']=dict(candidate_calls=len(result['occurrences']),**{s:result['status_counts'].get(s,0) for s in ('ASSOCIATED','PARTIAL','AMBIGUOUS','UNRESOLVED')},
            representations=result['representation_counts'],new_complete=sum(o['status']=='ASSOCIATED' and o['previous_interpretation']['status']!='ASSOCIATED' for o in result['occurrences']),
            previous_complete_preserved=sum(row['exact_geometry_preserved'] for row in result['comparison']['baseline_complete_associations']),
            new_visual_supported=sum(o['manual_validation']['status']=='VISUALLY_SUPPORTED_ASSISTANT' and o.get('leader_association') is not None for o in result['occurrences']),
            coverage=None,accuracy=None,independent_engineer_validations=0)
        overview(page,result['occurrences'],args.out)
        for o in result['occurrences']:zoom(page,o,args.out)
        summary(result,args.out)
        result['source_unchanged']=hashlib.sha256(args.pdf.read_bytes()).hexdigest()==digest
        save_json(args.out/'inventario.json',result);save_json(args.out/'entidades_pagina.json',data)
        save_json(args.out/'comparacao.json',result['comparison'])
        save_json(args.out/'validacao_manual_modelo.json',dict(source_sha256=digest,reviews={o['occurrence_id']:dict(status='PENDING',reviewer=None,method=None,selected_leader=None,notes=None) for o in result['occurrences']}))
        print(json.dumps(result['metrics'],indent=2))


if __name__=='__main__':main()
