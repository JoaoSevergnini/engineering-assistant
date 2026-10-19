"""Reproduce the manually selected N26 experiment. Never writes the input PDF."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'tmp/pdf_deps'))
sys.path.insert(0, str(ROOT/'tools/beam_model'))
import fitz
from pdf_observations import extract_zones
from geometry import extract_page, associate


def save_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def visual(page, result, out):
    clip = fitz.Rect(810, 640, 1170, 1030)
    original = page.get_pixmap(matrix=fitz.Matrix(2,2), clip=clip).tobytes('png')
    canvas = fitz.open()
    p = canvas.new_page(width=780, height=492)
    p.insert_text((18,22), 'N26 / L607 - validacao da interpretacao geometrica', fontsize=15)
    p.insert_text((18,43), 'Original', fontsize=11)
    p.insert_text((408,43), 'Sobreposicao independente (coordenadas do PDF)', fontsize=10)
    for x in (18,408):
        p.insert_image(fitz.Rect(x,54,x+360,444), stream=original)
    if len(result['accepted_pairs']) == 1:
        pair = result['accepted_pairs'][0]
        def point(v):
            return fitz.Point(v[0]-clip.x0+408, v[1]-clip.y0+54)
        poly = [point(v) for v in pair['region_pdf_pt']]
        shape = p.new_shape()
        shape.draw_polyline(poly+[poly[0]])
        shape.finish(color=(0,.5,.1), fill=(.2,.8,.3), fill_opacity=.12, width=1, dashes='[4 3] 0')
        shape.commit()
        for key, color in [('bar',(1,.15,0)), ('axis',(.75,0,.8))]:
            s = pair[key]
            p.draw_line(point(s['a']), point(s['b']), color=color, width=2)
        segments = {s['id']:s for s in result['_data']['segments']}
        for wing in sum(pair['evidence']['arrow_wing_ids'], []):
            s=segments[wing]
            p.draw_line(point(s['a']), point(s['b']), color=(.75,0,.8), width=1.5)
        cross = [pair['axis']['a'][0], pair['bar']['a'][1]]
        p.draw_circle(point(cross), 3, color=(0,0,0), width=1)
        box = result['label']['bbox']
        p.draw_rect(fitz.Rect(point(box[:2]),point(box[2:])),color=(.1,.5,.9),width=.7)
    p.insert_text((18,465),'Vermelho: barra | Magenta: eixo e setas da faixa | Verde tracejado: envoltoria grafica',fontsize=10)
    p.insert_text((18,482),'Azul claro: chamada | Circulo preto: juncao | Envoltoria nao define eixos extremos nem cobrimento.',fontsize=9)
    p.get_pixmap(matrix=fitz.Matrix(2,2)).save(str(out/'validacao_N26.png'))
    canvas.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdf', type=Path)
    parser.add_argument('--out', type=Path, default=ROOT/'analises/lajes_geometria_poc')
    args = parser.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)
    digest = hashlib.sha256(args.pdf.read_bytes()).hexdigest()
    with fitz.open(args.pdf) as doc:
        page=doc[0]
        data=extract_page(page)
        # Explicit human choice of ONE occurrence; not a sheet-wide detector.
        labels=[t for t in data['texts'] if t['text'].strip().startswith('N26 35 ')]
        if len(labels)!=1:
            raise ValueError('selected_occurrence_not_unique')
        result=associate(labels[0],data,scale_denominator=50)
        result['provenance']=dict(file=str(args.pdf.resolve()), sha256=digest, page=1,
                                 page_rect_pt=list(page.rect), rotation=page.rotation,
                                 coordinate_system='PyMuPDF page points; top left; x right; y down',
                                 engine=fitz.__doc__, selection='MANUAL_CASE_N26',
                                 scale_source='Printed ESCALA: 1/50 for main plan')
        # Reuse existing table extractor, including its original column contract.
        result['steel_schedule']=extract_zones(args.pdf,[dict(id='N26_SCHEDULE',page=0,
            bbox=[1995,416,2210,431],view='STEEL_SCHEDULE',marks=['N26'],
            quantity_scope='POSITION_TOTAL',integrity='UNVERIFIED',
            columns=['mark','diameter_mm','quantity','nominal_length_cm','total_length_cm'])])
        obs=result['steel_schedule']['observations']
        result['schedule_matches']=len(obs)==1 and all(obs[0][k]==result['call'][k] for k in
            ('mark','quantity','diameter_mm','nominal_length_cm'))
        result['counts']=dict(text_lines=len(data['texts']),paths=len(data['paths']),segments=len(data['segments']))
        if len(result['accepted_pairs'])==1:
            pair=result['accepted_pairs'][0]
            factor=2.54/72*50
            result['graphic_dimensions']=dict(bar_projected_cm=pair['bar']['length_pt']*factor,
                distribution_cm=pair['axis']['length_pt']*factor,
                n_minus_one_times_spacing_cm=(result['call']['quantity']-1)*result['call']['spacing_cm'],
                n_times_spacing_cm=result['call']['quantity']*result['call']['spacing_cm'],
                nature='GRAPHICAL_ESTIMATE_FROM_PRINTED_SCALE; not dimensioned physical coordinates')
        result['limitations']=[
            'Only one manually selected horizontal straight-bar occurrence; no general slab recognizer.',
            'Other labels may contain undecoded glyphs; selected N26 diameter glyph is decoded and table-confirmed.',
            'No explicit leader ties label to bar: association uses combined geometric evidence and remains interpretation.',
            'Arrow limits are graphical distribution limits, not proved first/last bar centers.',
            'Region is a translated straight-bar envelope; no slab clipping, bends, openings or anchorage interpretation.',
            'Printed scale provides estimates only; CAD/world coordinates and construction tolerances unknown.',
            'No resistance, TQS actions, minimum reinforcement, anchorage checks or ATP findings.']
        save_json(args.out/'entidades_pagina.json',data)
        result['_data']=data
        visual(page,result,args.out)
        del result['_data']
        page.get_pixmap(matrix=fitz.Matrix(.65,.65)).save(str(args.out/'prancha_contexto.png'))
        page.get_pixmap(matrix=fitz.Matrix(3,3),clip=fitz.Rect(1890,80,2220,438)).save(str(args.out/'tabela_ate_N26.png'))
    result['source_unchanged']=hashlib.sha256(args.pdf.read_bytes()).hexdigest()==digest
    save_json(args.out/'resultado_N26.json',result)
    print(json.dumps({k:result[k] for k in ('status','counts','schedule_matches','source_unchanged','graphic_dimensions')},indent=2))


if __name__=='__main__':
    main()
