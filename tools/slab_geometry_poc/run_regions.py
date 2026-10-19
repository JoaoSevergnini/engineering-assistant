"""Stage 5 reproducible artifacts; never saves or edits the source PDF."""
import argparse
import base64
import hashlib
import html
import json
from pathlib import Path
from run_sheet import ROOT,fitz,save_json
from distributed_regions import reconstruct


def color(i):return ((i*37%151+50)/255,(i*73%151+50)/255,(i*109%151+50)/255)


def render(source,items,path,clip=None,labels=True):
    clip=fitz.Rect(clip) if clip else source.rect
    doc=fitz.open();p=doc.new_page(width=clip.width,height=clip.height)
    pix=source.get_pixmap(matrix=fitz.Matrix(1.2,1.2),clip=clip)
    p.insert_image(p.rect,stream=pix.tobytes('png'))
    for i,r in enumerate(items):
        b=fitz.Rect(r['bbox'])
        if not b.intersects(clip):continue
        b=fitz.Rect(b.x0-clip.x0,b.y0-clip.y0,b.x1-clip.x0,b.y1-clip.y0)
        p.draw_rect(b,color=color(i),fill=color(i),fill_opacity=.22,width=.8)
        if labels:p.insert_text((b.x0+1,max(7,b.y0+7)),r.get('id',r.get('display_id','?')),fontsize=6,color=(.6,0,.2))
    p.get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(str(path));doc.close()


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--pdf',required=True);parser.add_argument('--inventory',default=str(ROOT/'analises/lajes_grupos_fisicos/inventario.json'));parser.add_argument('--out',default=str(ROOT/'analises/lajes_regioes_distribuidas'));args=parser.parse_args()
    src=Path(args.pdf);out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    before=hashlib.sha256(src.read_bytes()).hexdigest();input_path=Path(args.inventory)
    prior=json.loads(input_path.read_text(encoding='utf-8'));result=reconstruct(prior);a=result['distributed_spatial_analysis']
    result['stage5_provenance']={'source_pdf':str(src.resolve()),'sha256':before,'inventory':str(input_path.resolve()),'inventory_sha256':hashlib.sha256(input_path.read_bytes()).hexdigest(),'occurrences_preserved':result['occurrences']==prior['occurrences'],'localized_reconstruction_preserved':result['localized_reconstruction']==prior['localized_reconstruction']}
    with fitz.open(str(src)) as doc:
        source=doc[0];source.get_pixmap().save(str(out/'original.png'))
        render(source,a['regions'],out/'regioes_individuais.png')
        render(source,a['composition_regions'],out/'composicoes.png')
        excluded=[o for o in result['occurrences'] if o['status']!='ASSOCIATED']
        render(source,excluded+a['pending'],out/'pendencias.png')
        overlaps=sorted((c for c in a['composition_regions'] if len(c['identity_groups'])>1),key=lambda c:(-len(c['identity_groups']),-c['area_pt2'],c['id']))
        selected={c['id']:c for c in overlaps[:6]+sorted(overlaps,key=lambda c:(-c['area_pt2'],c['id']))[:3]}
        for c in selected.values():
            b=c['bbox'];cx=(b[0]+b[2])/2;cy=(b[1]+b[3])/2
            w=max(400,b[2]-b[0]+70);h=max(240,b[3]-b[1]+70)
            clip=fitz.Rect(cx-w/2,cy-h/2,cx+w/2,cy+h/2)&source.rect
            render(source,a['composition_regions'],out/(c['id']+'_sobreposicao.png'),clip)
        encoded=base64.b64encode((out/'original.png').read_bytes()).decode('ascii')
        shapes=''.join(f'<rect data-id="{c["id"]}" x="{c["bbox"][0]}" y="{c["bbox"][1]}" width="{c["bbox"][2]-c["bbox"][0]}" height="{c["bbox"][3]-c["bbox"][1]}" fill="rgb({int(color(i)[0]*255)},{int(color(i)[1]*255)},{int(color(i)[2]*255)})"><title>{c["id"]}: {html.escape(", ".join(c["occurrences"]))}</title></rect>' for i,c in enumerate(a['composition_regions']))
        payload=json.dumps({c['id']:c for c in a['composition_regions']},ensure_ascii=False).replace('</','<\\/')
        viewer='''<!doctype html><meta charset="utf-8"><title>Regiões distribuídas — Etapa 5</title><style>body{font:14px sans-serif;margin:20px}main{display:grid;grid-template-columns:70% 30%}svg{width:100%}rect{fill-opacity:.25;stroke:#333;stroke-width:.4;cursor:pointer}rect:hover,rect.selected{fill-opacity:.65;stroke:red;stroke-width:2}pre{white-space:pre-wrap;overflow-wrap:anywhere;height:85vh;overflow:auto}</style><h1>Regiões gráficas de composição</h1><p>Selecione uma região. Coordenadas em pontos PDF; área em pt². Interpretação experimental, sem soma resistente ou validação de camada.</p><main><svg viewBox="0 0 2384 1684"><image width="2384" height="1684" href="data:image/png;base64,IMAGE"/>SHAPES</svg><pre id="info">Selecione um polígono.</pre></main><script>const data=PAYLOAD;document.querySelectorAll('rect').forEach(e=>e.onclick=()=>{document.querySelectorAll('.selected').forEach(x=>x.classList.remove('selected'));e.classList.add('selected');document.getElementById('info').textContent=JSON.stringify(data[e.dataset.id],null,2)})</script>'''
        (out/'consulta.html').write_text(viewer.replace('IMAGE',encoded).replace('SHAPES',shapes).replace('PAYLOAD',payload),encoding='utf-8')
    assert hashlib.sha256(src.read_bytes()).hexdigest()==before
    save_json(out/'inventario.json',result)
    for name,key in [('regioes_individuais','regions'),('regioes_composicao','composition_regions'),('identidades_graficas','identity_groups'),('intersecoes_aberturas','opening_intersections')]:save_json(out/(name+'.json'),a[key])
    save_json(out/'consistencia_N38.json',result['stage5_documentary_consistency'])
    rows=['| Região | Ocorrências | Posições | Área (pt²) |','|---|---|---|---:|']
    rows += [f'| {c["id"]} | {", ".join(c["occurrences"])} | {", ".join(c["positions"])} | {c["area_pt2"]:.4f} |' for c in a['composition_regions']]
    (out/'composicoes.md').write_text('\n'.join(rows)+'\n',encoding='utf-8')
    print(json.dumps(a['metrics'],ensure_ascii=False))


if __name__=='__main__':main()
