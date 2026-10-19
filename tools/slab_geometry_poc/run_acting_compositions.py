"""Stage 10 offline inventories, review maps and click-to-query SVG viewer."""
import argparse
import copy
import hashlib
import html
import json
from pathlib import Path
from run_sheet import ROOT,fitz,save_json
from polygonal_slabs import shape,polygons,box as spatial_box
from refine_slab_assignment import line_parts
from run_structural_regions import canvas,box,write_png
from acting_compositions import analyze,query

COLORS={'SINGLE_REINFORCEMENT':(.1,.4,.8),'BASE_PLUS_REINFORCEMENT':(0,.6,.25),
    'MULTIPLE_REINFORCEMENTS':(.65,.55,0),'LAP_SPLICE':(.9,.4,0),'UNRESOLVED_COMPOSITION':(.65,.1,.7)}
OUT=ROOT/'analises/lajes_composicao_atuacao'


def draw_polygon(page,geometry,clip,color,label='',fill=.12):
    for poly in polygons(shape(geometry).intersection(spatial_box(*list(clip)))):
        s=page.new_shape()
        for ring in [poly.exterior]+list(poly.interiors):s.draw_polyline([fitz.Point(x-clip.x0,y-clip.y0) for x,y in ring.coords])
        s.finish(color=color,fill=color,fill_opacity=fill,width=.65,even_odd=True);s.commit()
        if label:
            p=poly.representative_point();page.insert_text((p.x-clip.x0,p.y-clip.y0),label,fontsize=6,color=color)


def visuals(source,inventory,result,out):
    raw={o['occurrence_id']:o for o in inventory['occurrences']}
    rois=[('mapa_composicoes.png',[50,145,1910,1205]),('L603_esquerda.png',[280,610,885,1020]),
        ('L603_direita.png',[1090,610,1700,1020]),('L605_N40.png',[600,980,1380,1215]),('L607_tracos_e_faixas.png',[810,790,1210,1020])]
    for name,roi in rois:
        doc,page,clip=canvas(source,roi);view=spatial_box(*list(clip))
        for c in result['compositions']:
            draw_polygon(page,c['geometry_pdf_pt'],clip,COLORS[c['classification']],c['source_composition_id'])
        for r in result['acting_regions']:
            if r['kind']=='LOCALIZED_TRACES_ONLY':
                for line in line_parts(shape(r['geometry_pdf_pt']).intersection(view)):
                    if not line.is_empty:page.draw_polyline([fitz.Point(x-clip.x0,y-clip.y0) for x,y in line.coords],color=(.1,.55,.55),width=1.5)
            if r['documentary_role']=='LAP_SPLICE' and r['geometry_pdf_pt']:
                g=shape(r['geometry_pdf_pt']).boundary.intersection(view)
                for line in line_parts(g):
                    if not line.is_empty:page.draw_polyline([fitz.Point(x-clip.x0,y-clip.y0) for x,y in line.coords],color=(.95,.35,0),width=2,dashes='[4 2] 0')
            if r['requires_previous_decision']:
                b=fitz.Rect(raw[r['occurrence_id']]['bbox'])&clip
                if not b.is_empty:box(page,list(b),clip,r['display_id']+' pendente',(.8,.1,.5),True)
        write_png(doc,page,out/name,'Azul: isolada | Verde: base+reforco documental | Laranja: traspasse local; contorno tracejado=tipo documental com zona pendente | Roxo: composicao pendente | Ciano: tracos sem area')
    doc,page,clip=canvas(source,[50,145,1910,1205])
    for r in result['acting_regions']:
        if r['kind']=='DISTRIBUTED_AREA':draw_polygon(page,r['geometry_pdf_pt'],clip,(.1,.4,.8),r['id']+'/'+r['position'],.04)
    write_png(doc,page,out/'regioes_individuais.png','Regioes graficas originais integrais; sem recorte por laje | Rotulos R/N; associacao e espessura consultaveis no inventario')


def viewer(source,result,out):
    roi=fitz.Rect(50,145,1910,1205)
    source.get_pixmap(matrix=fitz.Matrix(1.4,1.4),clip=roi).save(str(out/'prancha_original.png'))
    paths=[]
    for c in result['compositions']:
        color='rgb('+','.join(str(round(v*255)) for v in COLORS[c['classification']])+')'
        for poly in polygons(shape(c['geometry_pdf_pt'])):
            d=' '.join('M '+' L '.join(f'{x},{y}' for x,y in ring.coords)+' Z' for ring in [poly.exterior]+list(poly.interiors))
            paths.append(f'<path d="{d}" fill="{color}" fill-opacity=".14" fill-rule="evenodd" stroke="{color}" stroke-width=".6" data-cell="{html.escape(c["source_composition_id"])}"><title>{html.escape(c["source_composition_id"]+" / "+", ".join(c["positions"]))}</title></path>')
    data=json.dumps({'compositions':result['compositions'],'regions':result['acting_regions']},ensure_ascii=False).replace('<','\\u003c')
    template='''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><title>Regiões de atuação — Etapa 10</title>
<style>body{margin:0;font:14px system-ui;color:#19202a}header{padding:12px;background:#eef2f7}main{display:flex;height:85vh}.map{overflow:auto;width:67%;background:#ddd}svg{width:100%;height:auto}aside{width:33%;padding:12px;overflow:auto}pre{white-space:pre-wrap;font-size:12px}path{cursor:pointer}path:hover{fill-opacity:.5;stroke-width:2}button{margin:3px}input{max-width:150px}</style>
<header><b>Presença gráfica e função documental — sem aprovação estrutural ou soma resistente</b><br>Azul: isolada · Verde: base+reforço · Laranja: traspasse local · Roxo: pendente. Clique numa célula para consultar ocorrências e fundamentos.<br>
Busca por C, R, O ou N: <input id="search" placeholder="Ex.: C088 ou N14"><button id="find">Consultar</button> Zoom <input id="zoom" type="range" min="100" max="400" value="100"> <button id="pending">Nove pendências anteriores</button></header>
<main><div class="map"><svg viewBox="50 145 1860 1060" xmlns="http://www.w3.org/2000/svg"><image href="prancha_original.png" x="50" y="145" width="1860" height="1060"/>__PATHS__</svg></div><aside><p>As regiões não foram recortadas pelos contornos das lajes. N40 mantém tipo documental de traspasse, com parceiro e zona exata pendentes; não recebe contribuição adicional.</p><pre id="info">Selecione uma célula ou pesquise uma posição.</pre></aside></main>
<script type="application/json" id="data">__DATA__</script><script>
const data=JSON.parse(document.getElementById('data').textContent),info=document.getElementById('info');
function show(records){info.textContent=JSON.stringify(records,null,2)}
document.querySelectorAll('[data-cell]').forEach(p=>p.addEventListener('click',()=>show(data.compositions.filter(c=>c.source_composition_id===p.dataset.cell))));
document.getElementById('find').onclick=()=>{const q=document.getElementById('search').value.trim().toUpperCase();show({compositions:data.compositions.filter(c=>c.source_composition_id===q||c.id.toUpperCase()===q||c.region_ids.includes(q)||c.occurrences.includes(q)||c.positions.includes(q)),acting_regions:data.regions.filter(r=>r.id===q||r.display_id===q||r.position===q)})};
document.getElementById('pending').onclick=()=>show(data.regions.filter(r=>r.requires_previous_decision));
document.getElementById('zoom').oninput=e=>document.querySelector('svg').style.width=e.target.value+'%';
</script></html>'''
    (out/'consulta_regioes.html').write_text(template.replace('__PATHS__',''.join(paths)).replace('__DATA__',data),encoding='utf8')


def report(result,inventory,out):
    lookup={r['id']:r for r in result['acting_regions']};rows=['# Etapa 10 — Regiões de atuação e composição','',
        '## Auditoria e reutilização','',
        'Reutilizados os 35 polígonos da Etapa 5, as 119 células originais, as relações com escopo da Etapa 7, os contornos candidatos da Etapa 8 e as atribuições da Etapa 9.2. Não houve nova extração, nova partição ou recorte por laje. Das 59 ocorrências, 35 têm envoltórias distribuídas sustentadas por barra/eixo; 15 localizadas têm traços, sem região de área comprovada; nove continuam pendentes. RELIABLE na associação não transforma hipótese de geometria em área física validada.',
        '', '## Critérios','',
        'SINGLE_REINFORCEMENT registra uma ocorrência gráfica distribuída na direção/camada examinada. BASE_PLUS_REINFORCEMENT exige função conjunta confirmada localmente ou papéis humanos compatíveis de base/reforço com sobreposição vetorial. MULTIPLE_REINFORCEMENTS exige suporte explícito da combinação completa; não há caso comprovado nesta prancha. LAP_SPLICE é aplicado a domínio de traspasse confirmado localmente. As demais interseções ficam UNRESOLVED_COMPOSITION. Funções candidatas BASE/REFORÇO, dimensões pequenas e igualdade de marcas não autorizam composição adicional.',
        '', 'Os papéis humanos N13=base e N14=reforço em toda extensão sustentam relações de função nas interseções dos pares esquerdo e direito. A origem dessa confirmação é a solicitação da Etapa 10, seção 5; os dados externos são vinculados ao hash do PDF, ocorrências e geometrias. O algoritmo não contém regras por marca. Camadas exatas e independência para soma numérica continuam não autorizadas. Nenhum resultado calcula As/m, altura útil ou momento resistente.',
        '', '## Resultados','', '```json',json.dumps(result['metrics'],ensure_ascii=False,indent=2),'```',
        '', 'Todas as células retêm C original e um ID derivado estável. O agrupamento em blocos exige as mesmas ocorrências, direção/camada, função, evidências e continuidade geométrica. Partes desconectadas e ocorrências distintas de uma mesma marca não são fundidas. As áreas são em pt² da prancha, não áreas de aço.',
        '', '## L603 — comparação N13/N14','', '| Base | Reforço | Área de sobreposição gráfica (pt²) | Área de células com somente essa N13 (pt²) | Células com terceiros ainda pendentes |','|---|---|---:|---:|---|']
    comp={c['id']:c for c in result['compositions']}
    for r in result['base_reinforcement_comparison']:
        b,z=lookup[r['base_region_id']],lookup[r['reinforcement_region_id']]
        rows.append('| '+ ' | '.join([b['display_id']+'/'+b['position'],z['display_id']+'/'+z['position'],f"{r['overlap_area_pt2']:.3f}",f"{r['isolated_base_area_pt2']:.3f}",', '.join(comp[id]['source_composition_id'] for id in r['overlap_with_other_unresolved_members'])])+' |')
    rows+=['', 'C083 preserva a confirmação local N13+N14 à esquerda. C088 recebe função conjunta sustentada pelos papéis confirmados e pela geometria à direita. C071/C076 preservam o subconjunto N13+N14 sustentado, mas ficam pendentes quanto à contribuição adicional de N15. C059 continua base+reforço confirmado localmente, sem ampliar essa confirmação para todas as ocorrências N15. A N14 permanece reforço também fora da interseção com N13; isso não comprova automaticamente sua composição com outras bases.',
        '', '## L605 — N40 e traspasses','',
        'R053/N40 mantém o papel humano LAP_SPLICE. As quatro células que a contêm (C109, C110, C115 e C116) não recebem função de reforço nem soma adicional: ficam UNRESOLVED_COMPOSITION porque parceiro e zona exata do traspasse não foram confirmados. A borda laranja tracejada no mapa mostra o escopo da representação documental, não um comprimento de traspasse comprovado. C092 mantém LAP_SPLICE no domínio exato da confirmação anterior. C073 permanece residual gráfico confirmado, mapeado como composição não resistente pendente, sem exclusão de sua geometria.',
        '', '## L607 — barras, faixas e apoios','',
        'N24/O033 e O047 mantêm suas regiões distribuídas integrais, inclusive fora do contorno candidato. A associação L607/h20 é documental/espacial. N21/O039/O040 e N22/O038 são traços localizados: não foi inventada área retangular nem contribuição distribuída. N22/O037 permanece pendente de geometria/rastreamento. Nenhuma parcela externa é declarada ancoragem ou contribuição resistente de apoio.',
        '', '## Pendências e comparação com etapas anteriores','',
        'As nove pendências de associação/geometria da Etapa 9.2 permanecem: '+', '.join(result['previous_pending_occurrences'])+'. Nenhuma produz área elegível. As 45 composições pendentes incluem sobreposições sem interpretação física, o residual confirmado e o escopo documental de N40 ainda não delimitado como zona de traspasse. Não se buscou reduzir esse número artificialmente.',
        '', 'Foram preservadas as 35 regiões e as 119 células. Em relação às quatro classificações humanas locais: duas base+reforço e um traspasse continuam nas mesmas geometrias; o residual permanece registrado com seu significado original e não vira contribuição. C088 é a nova composição base+reforço sustentada pela confirmação atual. As relações candidatas anteriores permanecem no histórico e não são promovidas por transitividade.',
        '', '## Consulta e entregáveis','',
        '[Consulta interativa local](consulta_regioes.html) — clique na prancha ou busque C, R, O ou N para consultar membros e motivos. O arquivo usa somente a imagem e os dados locais, sem serviços externos.',
        '', '[Mapa das composições](mapa_composicoes.png) · [Regiões individuais](regioes_individuais.png) · [L603 esquerda](L603_esquerda.png) · [L603 direita](L603_direita.png) · [L605/N40](L605_N40.png) · [L607](L607_tracos_e_faixas.png)',
        '', '[Regiões de atuação](regioes_atuacao.json) · [Composições](composicoes.json) · [Blocos consolidados](blocos.json) · [Pendências](pendencias.json) · [Comparação rastreável com etapas anteriores](comparacao_etapas.json)',
        '', 'Consulta por coordenadas PDF: `python tools/slab_geometry_poc/run_acting_compositions.py --query X Y`. Pontos em fronteiras devolvem todas as células incidentes, sem seleção por proximidade.',
        '', '## Limitações e próxima etapa','',
        'As envoltórias são interpretações gráficas sustentadas por entidades vetoriais, não geometria física integralmente confirmada. As 15 representações localizadas exigem modelo próprio de atuação para verificações futuras. A composição documental não autoriza soma numérica com camadas desconhecidas, regiões de apoio, duplicidade ou traspasse. A próxima etapa deve manter esses bloqueios, resolver ambiguidades relevantes e comprovar posicionamento/camadas antes de calcular altura útil ou composições resistentes. Não foi feita verificação normativa ou aprovação estrutural.']
    (out/'relatorio.md').write_text('\n'.join(rows)+'\n',encoding='utf8')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--query',type=float,nargs=2);args=parser.parse_args()
    if args.query:
        result=json.loads((OUT/'atuacao.json').read_text(encoding='utf8'));print(json.dumps(query(result,*args.query),ensure_ascii=False,indent=2));return
    OUT.mkdir(parents=True,exist_ok=True);inp=ROOT/'analises/lajes_associacao_documental/inventario.json'
    inventory=json.loads(inp.read_text(encoding='utf8'));profile_path=OUT/'confirmacoes_engenheiro.json';profile=json.loads(profile_path.read_text(encoding='utf8'))
    source=Path(inventory['stage5_provenance']['source_pdf']);before=hashlib.sha256(source.read_bytes()).hexdigest()
    if before!=inventory['stage5_provenance']['sha256']:raise ValueError('SOURCE_PDF_CHANGED')
    result=analyze(inventory,profile);enriched=copy.deepcopy(inventory);enriched['acting_composition_analysis']=result
    enriched['stage10_provenance']={'source_pdf_sha256':before,'input_inventory_sha256':hashlib.sha256(inp.read_bytes()).hexdigest(),
        'human_role_profile_sha256':hashlib.sha256(profile_path.read_bytes()).hexdigest(),
        'all_previous_layers_preserved':all(enriched[k]==v for k,v in inventory.items()),'source_geometries_and_partition_unchanged':True}
    save_json(OUT/'inventario.json',enriched);save_json(OUT/'atuacao.json',result)
    old={c['composition_id']:c for c in inventory['occurrence_relation_analysis']['interpreted_compositions']}
    save_json(OUT/'comparacao_etapas.json',{'all_previous_inventory_layers_equal':enriched['stage10_provenance']['all_previous_layers_preserved'],
        'original_region_count':len(inventory['distributed_spatial_analysis']['regions']),
        'original_composition_count':len(inventory['distributed_spatial_analysis']['composition_regions']),
        'previous_pending_occurrences_preserved':result['previous_pending_occurrences'],
        'cells':[{'source_composition_id':c['source_composition_id'],'derived_id':c['id'],
            'previous_classification':old[c['source_composition_id']]['classification'],'stage10_classification':c['classification'],
            'source_coordinates_equal':old[c['source_composition_id']]['polygon_pdf_pt']==c['original_polygon_pdf_pt'],
            'documentary_lap_region_ids':c['documentary_lap_region_ids'],'physical_addition_authorized':False} for c in result['compositions']]})
    for filename,key in [('regioes_atuacao.json','acting_regions'),('composicoes.json','compositions'),('blocos.json','consolidated_blocks')]:save_json(OUT/filename,result[key])
    save_json(OUT/'pendencias.json',{'previous_occurrences':result['previous_pending_occurrences'],
        'unresolved_composition_ids':[c['id'] for c in result['compositions'] if c['classification']=='UNRESOLVED_COMPOSITION'],
        'localized_without_proved_area':[r['id'] for r in result['acting_regions'] if r['kind']=='LOCALIZED_TRACES_ONLY']})
    with fitz.open(str(source)) as pdf:visuals(pdf[0],inventory,result,OUT);viewer(pdf[0],result,OUT)
    if hashlib.sha256(source.read_bytes()).hexdigest()!=before:raise ValueError('SOURCE_PDF_CHANGED')
    report(result,inventory,OUT);print(json.dumps(result['metrics'],indent=2))


if __name__=='__main__':main()
