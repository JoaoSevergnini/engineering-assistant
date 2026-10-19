"""Stage 9.2 derived inventories and independent association/decision maps."""
import copy
import hashlib
import json
from collections import Counter
from pathlib import Path
from run_sheet import ROOT,fitz,save_json
from polygonal_slabs import shape,polygons,box as spatial_box
from refine_slab_assignment import line_parts
from run_relations import draw_geometry
from run_structural_regions import canvas,box,write_png
from documentary_slab_assignment import analyze


def visuals(source,inventory,result,out):
    original={o['occurrence_id']:o for o in inventory['occurrences']}
    colors={c['slab']:((i*37%130+40)/255,(i*71%130+40)/255,(i*97%130+40)/255) for i,c in enumerate(result['contexts'])}
    for name,pending,roi in [('mapa_associacoes.png',False,[50,145,1910,1205]),('mapa_pendencias.png',True,[50,145,1910,1205]),
        ('L605_contexto.png',False,[580,960,1395,1235]),('L607_apoios.png',False,[800,790,1230,1025])]:
        doc,page,clip=canvas(source,roi)
        view=spatial_box(clip.x0,clip.y0,clip.x1,clip.y1)
        for context in result['contexts']:
            for e in context['evidence'][1:]:
                for line in line_parts(shape(e['geometry_pdf_pt']).boundary.intersection(view)):
                    if line.is_empty:continue
                    page.draw_polyline([fitz.Point(x-clip.x0,y-clip.y0) for x,y in line.coords],color=(.45,.45,.45),width=.8,dashes='[4 2] 0')
            label=context['documentary_sources']['label'];b=fitz.Rect(label['bbox'])
            if b.intersects(clip):page.insert_text((b.x0-clip.x0,b.y0-clip.y0-4),context['slab']+' h='+str(context['thickness_cm']),fontsize=8,color=colors[context['slab']])
        for occurrence in result['occurrences']:
            if pending and not occurrence['requires_engineer_decision']:continue
            for piece in occurrence['spatial_context_partition']:
                if not piece['slabs']:continue
                color=colors[piece['slabs'][0]] if len(piece['slabs'])==1 else (.8,0,.6)
                # Display clipping only; inventory geometries remain unchanged.
                geometry=shape(piece['geometry_pdf_pt']).intersection(view)
                if geometry.is_empty:continue
                for poly in polygons(geometry):
                    s=page.new_shape()
                    for ring in [poly.exterior]+list(poly.interiors):s.draw_polyline([fitz.Point(x-clip.x0,y-clip.y0) for x,y in ring.coords])
                    s.finish(color=color,fill=color,fill_opacity=.12,width=.5,even_odd=True);s.commit()
                for line in line_parts(geometry):
                    page.draw_polyline([fitz.Point(x-clip.x0,y-clip.y0) for x,y in line.coords],color=color,width=1.4,
                        dashes='[3 2] 0' if occurrence['geometry_alternatives_not_selected'] else None)
            call=original[occurrence['occurrence_id']];b=fitz.Rect(call['bbox'])&clip
            if b.is_empty:continue
            color=(.85,0,.15) if occurrence['state']=='INDETERMINATE' else (.85,.4,0) if occurrence['state']=='PROBABLE' else colors[occurrence['slabs'][0]]
            if occurrence['requires_engineer_decision']:box(page,list(b),clip,'',color,True)
            page.insert_text((max(2,b.x0-clip.x0),max(8,b.y0-clip.y0-3)),occurrence['display_id'],fontsize=7,color=color)
        write_png(doc,page,out/name,'Cores: contexto documental da laje | Cinza tracejado: contexto auxiliar, nao contorno validado | Laranja/vermelho: decisao pendente | Tracos de hipoteses: tracejados')


def report(result,previous,out):
    table=['| Ocorrência | Posição | Etapa 9.1 | Etapa 9.2 | Lajes | h (cm) | Problemas documentais | Problemas espaciais | Alertas topológicos | Geometria de atuação |',
        '|---|---|---|---|---|---|---|---|---|---|']
    for c in result['comparison']:
        i=c['issues'];table.append('| '+' | '.join([c['display_id'],c['position'],c['previous_state'],c['new_state'],', '.join(c['slabs']) or '—',
            ', '.join(map(str,c['thickness_options_cm'])) or '—','; '.join(i['documentary']) or '—','; '.join(i['spatial']) or '—',
            '; '.join(t['domain_id'] for t in i['topological']) or '—','; '.join(i['actuation_geometry'])])+' |')
    (out/'comparacao_59.md').write_text('# Comparação individual das 59 ocorrências\n\n'+'\n'.join(table)+'\n',encoding='utf8')
    rows=['# Etapa 9.2 — Associação documental e espacial','',
        '## Auditoria','',
        'A Etapa 9.1 separou contenção e associação, mas ainda impedia RELIABLE quando havia thin_border_review_flag. Além disso, examinava apenas interseções com o contorno candidato e descartava, para associação, todas as hipóteses de geometria não resolvidas. Foram reutilizados association_evidence, partition_domains, as etiquetas documentais, as hipóteses de barras/faixas e líderes já rastreados e a rede vetorial da Etapa 8. Nenhuma extração, ocorrência, quantitativo ou geometria original foi reescrita.',
        '', '## Contextos auxiliares, sem corrigir contornos','',
        '1. Moldura em U com três lados externos vetorialmente completos, faces internas paralelas e apontador explícito da etiqueta: define uma janela auxiliar de associação. A abertura da moldura não vira limite estrutural comprovado. Na prancha, esse padrão recuperou o contexto interior de L605.',
        '2. Dois pares opostos de faces de apoio, fechados por tampas vetoriais e com extremidades coincidentes: permitem avaliar continuidade além de uma fronteira candidata. São examinadas as quatro direções. Na prancha, D1187:0–D1194:0 sustentam o contexto inferior de L607 até o próximo alinhamento de apoios.',
        '', 'Esses contextos são evidências de atribuição documental, não novos contornos validados. O algoritmo não fixa L605, L607, marcas, coordenadas ou IDs de vetores. As dimensões são recuperadas dos segmentos. Não usa fecho convexo nem escolhe a laje mais próxima. Os padrões são experimentais: a janela pode incluir apoios ou vazios, devendo ser revisada quando houver concorrência documental.',
        '', 'Filtros experimentais: contato numérico de 0,001 pt; faces internas com sobreposição longitudinal ≥65% e afastamento ≤25% da menor dimensão da moldura; fronteira apoiada ≥80%; largura de cada faixa lateral ≤15% da fronteira. Esses parâmetros reconhecem padrões gráficos e não são tolerâncias estruturais. Sua generalização para outros escritórios ainda precisa ser testada.',
        '', '## Confianças independentes','',
        'RELIABLE requer identidade/espessura documentais e suporte espacial consistente das entidades no contexto. Um alerta topológico isolado fica no campo issues.topological e não altera a associação. A confiança do contorno permanece CANDIDATE_NOT_CONFIRMED. A qualidade da geometria de atuação é registrada separadamente: hipóteses de barras/líderes permanecem hipóteses, sem seleção silenciosa ou criação de regiões físicas.',
        '', 'Os candidatos de geometria só são usados quando já possuem marcador de junção barra/faixa ou linha de chamada com destino sustentado. Rotas incompletas e alternativas sem suporte mantêm PROBABLE. Alternativas que indicam lajes diferentes, ou contextos concorrentes na mesma parcela, ficam INDETERMINATE. Uma ocorrência aceita pode atravessar contextos disjuntos de espessuras diferentes; cada parcela retém suas possibilidades e nenhuma altura útil única é atribuída.',
        '', '## Resultado comparativo','', '| Associação | Etapa 9.1 | Etapa 9.2 |','|---|---:|---:|']
    for state in ['RELIABLE','PROBABLE','INDETERMINATE']:rows.append('| '+state+' | '+str(previous['metrics']['states'].get(state,0))+' | '+str(result['metrics']['states'].get(state,0))+' |')
    transitions=Counter((c['previous_state'],c['new_state']) for c in result['comparison'])
    rows+=['','Transições: '+'; '.join(a+' → '+b+': '+str(n) for (a,b),n in sorted(transitions.items()))+'.',
        '', '```json',json.dumps(result['metrics'],ensure_ascii=False,indent=2),'```',
        '', 'Esses números descrevem a aplicação dos critérios experimentais, não uma taxa de acerto conferida independentemente. Não há novas confirmações humanas de associação nesta etapa.',
        '', '## Casos obrigatórios','', '| Ocorrência | Posição | Associação | Laje / h | Interpretação e pendências |','|---|---|---|---|---|']
    regression_positions={'N25','N35','N39','N36','N38','N40','N37','N41','N21','N22','N14'}
    for o in result['occurrences']:
        if o['documentary_mark'] not in regression_positions and o['display_id']!='O047':continue
        remarks='; '.join(o['pending_reasons']) or 'Suporte documental e espacial consistente'
        if o['documentary_mark']=='N40':remarks+='; LAP_SPLICE confirmado pelo engenheiro preservado'
        if o['documentary_mark']=='N14':remarks+='; REINFORCEMENT em toda extensão confirmado pelo engenheiro preservado'
        rows.append('| '+' | '.join([o['display_id'],o['documentary_mark'],o['state'],', '.join(o['slabs'])+' / '+', '.join(map(str,o['thickness_options_cm'])),remarks])+' |')
    rows+=['', 'O047/N24: a faixa original vai de y=959,0800 a 1006,7200 pt, enquanto o candidato L607 terminava em y=948,4000 pt. O descompasso é de contexto/contorno, não ausência de barra ou faixa: ambas já estavam extraídas. A continuidade entre faces laterais de apoio fornece associação a L607/h20 sem alterar a faixa ou o contorno.',
        '', 'N37/O054: os traços e a chamada já estavam associados; a ausência anterior de interseção era causada pelo contexto estreito de L605, e não por falta de extração. N41/O057: a associação candidata é L605/h18, mas permanecem alternativas de barras/faixas e uma alternativa sem suporte suficiente; a classificação é PROBABLE. N22/O037: destino de líder já extraído indica L607/h20, porém o rastreamento anterior atingiu limite de busca e a geometria continua inconclusiva. N21: grupos em lados opostos dos vazios recuperam suporte no contexto de apoios, sem classificar automaticamente os trechos externos como ancoragem.',
        '', '## Pendências por natureza','']
    for o in result['occurrences']:
        if not o['requires_engineer_decision']:continue
        rows.append('- **'+o['display_id']+'/'+o['documentary_mark']+' — '+o['state']+'**: '+('; '.join(o['pending_reasons']) or 'Revisar evidências')+'.')
    rows+=['', 'Os alertas topológicos de L605 permanecem visíveis inclusive quando a associação é RELIABLE. A geometria estrutural e os contornos ainda não foram confirmados. Ausência de suporte geométrico não significa ausência física de armadura ou insuficiência resistente.',
        '', '## Rastreabilidade e limites','',
        'O inventário completo preserva integralmente todas as camadas anteriores e acrescenta documentary_spatial_assignment. Segmentos, barras, faixas e geometrias originais mantêm coordenadas e estados históricos. spatial_context_partition é apenas uma interseção auxiliar: não substitui a região de atuação nem fornece geometria estrutural para cálculo. As parcelas externas originais não foram apagadas, nem declaradas ancoragem. Quantitativos não foram distribuídos ou somados.',
        '', 'N14, N40, as quatro classificações humanas locais e a inconsistência N38 estão preservadas. Não houve cálculo de altura útil, resistência ou dimensionamento. Antes de relacionar esforços, é necessário manter o vínculo com o domínio estrutural da planta de formas, a geometria de atuação e as alternativas ainda abertas.',
        '', '[Mapa das associações](mapa_associacoes.png) · [Mapa de decisões pendentes](mapa_pendencias.png) · [Comparação das 59 ocorrências](comparacao_59.md) · [Inventário](associacoes.json) · [Contexto L605](L605_contexto.png) · [Apoios L607](L607_apoios.png)']
    (out/'relatorio.md').write_text('\n'.join(rows)+'\n',encoding='utf8')


def main():
    inp=ROOT/'analises/lajes_associacao_refinada/inventario.json';out=ROOT/'analises/lajes_associacao_documental';out.mkdir(exist_ok=True,parents=True)
    inventory=json.loads(inp.read_text(encoding='utf8'));source=Path(inventory['stage5_provenance']['source_pdf'])
    before=hashlib.sha256(source.read_bytes()).hexdigest()
    if before!=inventory['stage5_provenance']['sha256']:raise ValueError('SOURCE_PDF_CHANGED')
    result=analyze(inventory);enriched=copy.deepcopy(inventory);enriched['documentary_spatial_assignment']=result
    enriched['stage92_provenance']={'source_pdf_sha256':before,'input_inventory_sha256':hashlib.sha256(inp.read_bytes()).hexdigest(),
        'previous_layers_preserved':all(enriched[k]==v for k,v in inventory.items()),
        'source_geometries_modified':False,'contexts_are_not_validated_structural_domains':True}
    save_json(out/'inventario.json',enriched);save_json(out/'associacoes.json',result);save_json(out/'comparacao_59.json',result['comparison'])
    save_json(out/'pendencias.json',[c for c in result['comparison'] if c['requires_engineer_decision']])
    with fitz.open(str(source)) as pdf:visuals(pdf[0],inventory,result,out)
    if hashlib.sha256(source.read_bytes()).hexdigest()!=before:raise ValueError('SOURCE_PDF_CHANGED')
    report(result,inventory['refined_slab_assignment'],out);print(json.dumps(result['metrics'],indent=2))


if __name__=='__main__':main()
