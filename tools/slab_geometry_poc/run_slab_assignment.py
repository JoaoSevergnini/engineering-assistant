"""Reproducible stage 9 inventories, PNG overlays and review lists."""
import copy
import hashlib
import json
from pathlib import Path
from run_sheet import ROOT, fitz, save_json
from slab_assignment import analyze
from polygonal_slabs import shape, polygons
from run_structural_regions import canvas, write_png
from run_relations import draw_geometry

OUT = ROOT/'analises/lajes_associacao_espessuras'


def visuals(source, analysis, out):
    colors = {d['slab']: ((i*37%150+30)/255,(i*71%150+30)/255,(i*97%150+30)/255) for i,d in enumerate(analysis['domains'])}
    for kind, name in [('DISTRIBUTED','mapa_distribuidas.png'),('LOCALIZED','mapa_localizadas.png')]:
        doc,page,clip=canvas(source,[50,145,1910,1205])
        for d in analysis['domains']:
            draw_geometry(page,d['geometry_pdf_pt'],clip,colors[d['slab']],d['slab']+' h='+str(d['thickness_cm']),True)
        for occurrence in analysis['occurrences']:
            if occurrence['representation_kind'] != kind:continue
            for segment in occurrence['segments']:
                color = colors[segment['slabs'][0]] if len(segment['slabs'])==1 else (.8,0,.6) if segment['slabs'] else (.45,.45,.45)
                g=shape(segment['geometry_pdf_pt'])
                if kind=='DISTRIBUTED':
                    for poly in polygons(g):
                        s=page.new_shape()
                        for ring in [poly.exterior]+list(poly.interiors):
                            s.draw_polyline([fitz.Point(x-clip.x0,y-clip.y0) for x,y in ring.coords])
                        s.finish(color=color,fill=color,fill_opacity=.15,even_odd=True,width=.5);s.commit()
                    draw_geometry(page,segment['geometry_pdf_pt'],clip,color,occurrence['display_id'])
                else:
                    parts=list(g.geoms) if hasattr(g,'geoms') else [g]
                    for line in parts:
                        if line.geom_type!='LineString':continue
                        page.draw_polyline([fitz.Point(x-clip.x0,y-clip.y0) for x,y in line.coords],color=color,width=2)
                    anchor=g.representative_point()
                    page.insert_text((anchor.x-clip.x0+3,anchor.y-clip.y0-3),occurrence['display_id'],fontsize=7,color=color)
        write_png(doc,page,out/name,'Cores por laje (etiquetas h em cm) | Cinza: sem dominio | Magenta: concorrencia | Contornos candidatos tracejados; sem alocacao de quantidades')


def report(analysis, out):
    items=analysis['occurrences']; m=analysis['metrics']
    lines=['# Etapa 9 — Associação geométrica a lajes e espessuras','',
        '## Auditoria e método','',
        'Reutilizados os 35 polígonos da Etapa 5, os grupos e traços localizados da Etapa 4 e os nove contornos candidatos da Etapa 8. Nenhum reconhecimento documental, contorno ou partição anterior foi alterado. Shapely executa interseção e diferença, preservando os pontos originais; novos vértices são interseções geométricas derivadas. Não há seleção por centroide, proximidade de etiqueta, cor, BASE ou REFORÇO.',
        '', 'Cada ocorrência distribuída é particionada por domínio candidato; a extensão longitudinal continua vinculada à barra e a transversal ao eixo de distribuição. Comprimento nominal C não foi convertido em projeção. Grupos localizados são associados por comprimento dos traços, sem envoltória fictícia. Contatos sem área não associam regiões distribuídas; traços exatamente sobre uma borda continuam sujeitos à incerteza do contorno.',
        '', 'Nome e espessura são dados documentais: suas etiquetas, IDs, coordenadas e textos de espessura estão no inventário de domínios. Os recortes são interpretações geométricas. Todas as associações reais são provisórias: RELIABLE exige contorno confirmado; PROBABLE identifica interseção com candidato único; INDETERMINATE registra partes descobertas, domínios concorrentes ou geometria não comprovada. A classe da ocorrência adota a pior classe de suas parcelas. Não foi realizada nova confirmação humana das associações.',
        '', '## Resultados','', '```json',json.dumps(m,ensure_ascii=False,indent=2),'```','',
        'Há interseções em 34 ocorrências DISTRIBUTED e 14 LOCALIZED. Doze ocorrências têm somente parcelas PROBABLE; 36 combinam parcelas prováveis com partes descobertas e ficam globalmente INDETERMINATE. O047/N24 e O054/N37 têm geometria recuperada, mas nenhuma interseção com os domínios candidatos. Outras nove não possuem geometria de atuação comprovada. Nenhuma associação é RELIABLE porque nenhum contorno utilizado está confirmado. Não houve ocorrência em múltiplos domínios nesta execução real; o cruzamento de espessuras foi demonstrado apenas em testes sintéticos.',
        'As parcelas mantêm referência à chamada e ao grupo físico original. quantity_allocation é nulo: não se distribuem barras ou quantitativos por laje, nem se somam ocorrências repetidas. Medidas em pt²/pt descrevem geometria da prancha, não área de aço ou dimensão física calibrada.',
        '', '## Classificações preservadas','',
        'N14/R034 e R035: função REINFORCEMENT confirmada pelo engenheiro em toda a extensão das respectivas ocorrências. R053/N40: interpretação LAP_SPLICE confirmada pelo engenheiro; parceiro e extensão efetiva do traspasse continuam pendentes. O candidato anterior de N40 como reforço permanece apenas como histórico e é superado pela camada humana atual. Não se aplica a ele a conclusão anterior de contenção como se fosse reforço. As confirmações são dados externos, vinculados ao hash do PDF, ocorrência e geometria, sem regras de produção por marca.',
        '', 'As quatro confirmações locais C059, C083, C092 e C073 e a inconsistência documental N38 permanecem integralmente no inventário anterior. Nenhuma classificação foi propagada a outras células por esta etapa.',
        '', '## Pendências e próxima etapa','',
        'Conferir os contornos candidatos, em especial a faixa estreita de L605 e os anéis internos gráficos, que ainda não comprovam vazios estruturais. Parcelas fora dos domínios são preservadas: não significam ausência de laje nem falha resistente. Várias lajes possíveis na ocorrência não equivalem a uma associação confirmada; consultar os motivos e os polígonos de cada parcela. As nove representações sem geometria suficientemente comprovada não recebem laje pela posição de seu texto.',
        '', 'Recomenda-se conferir os recortes com a planta de formas e revisar as associações listadas abaixo. Espessura documental não fornece altura útil: cobrimento, camada e posição efetiva continuam necessários. Não houve cálculo resistente, soma de contribuições ou alteração do PDF.',
        '', '[Mapa distribuídas](mapa_distribuidas.png) · [Mapa localizadas](mapa_localizadas.png) · [Múltiplas lajes](multiplas_lajes.md) · [Pendências](pendencias.md) · [Inventário](associacoes.json)']
    (out/'relatorio.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
    for filename,title,selected in [('multiplas_lajes.md','Ocorrências com interseção em múltiplos domínios',[o for o in items if o['multiple_slabs']]),('pendencias.md','Associações que exigem conferência',[o for o in items if o['state']!='RELIABLE'])]:
        rows=['# '+title,'','| Ocorrência | Posição | Lajes candidatas | h (cm) | Estado | Motivos |','|---|---|---|---|---|---|']
        if not selected:rows[2:2]=['Nenhum caso detectado nos contornos candidatos atuais. Isso não comprova ausência física de armaduras compartilhadas. A segmentação entre lajes de espessuras diferentes foi verificada em testes sintéticos.','']
        for o in selected:rows.append('| '+ ' | '.join([o['display_id'],o['documentary_mark'],', '.join(o['slabs']) or '—',', '.join(map(str,o['thickness_options_cm'])) or '—',o['state'],', '.join(o['pending_reasons'])])+' |')
        (out/filename).write_text('\n'.join(rows)+'\n',encoding='utf8')


def main():
    out=OUT;out.mkdir(parents=True,exist_ok=True)
    inp=ROOT/'analises/lajes_contornos_complexos/inventario.json'
    inventory=json.loads(inp.read_text(encoding='utf8'))
    entities=json.loads((ROOT/'analises/lajes_geometria_lideres/entidades_pagina.json').read_text(encoding='utf8'))
    profile=json.loads((out/'confirmacoes_engenheiro.json').read_text(encoding='utf8'))
    source=Path(inventory['stage5_provenance']['source_pdf']);before=hashlib.sha256(source.read_bytes()).hexdigest()
    if before!=inventory['stage5_provenance']['sha256']:raise ValueError('PDF_CHANGED')
    analysis=analyze(inventory,entities['texts'],profile)
    result=copy.deepcopy(inventory);result['slab_reinforcement_assignment']=analysis
    result['stage9_provenance']={'source_pdf_sha256':before,'input_inventory_sha256':hashlib.sha256(inp.read_bytes()).hexdigest(),
        'confirmation_sha256':hashlib.sha256((out/'confirmacoes_engenheiro.json').read_bytes()).hexdigest(),
        'prior_layers_preserved':all(result[k]==v for k,v in inventory.items())}
    save_json(out/'inventario.json',result);save_json(out/'associacoes.json',analysis)
    with fitz.open(str(source)) as pdf:visuals(pdf[0],analysis,out)
    if hashlib.sha256(source.read_bytes()).hexdigest()!=before:raise ValueError('PDF_CHANGED')
    report(analysis,out);print(json.dumps(analysis['metrics'],indent=2))


if __name__=='__main__':main()
