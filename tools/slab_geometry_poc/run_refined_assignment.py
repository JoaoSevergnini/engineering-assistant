"""Stage 9.1 derived artifacts; the complete stage 9 inventory is preserved."""
import copy
import hashlib
import json
from collections import Counter
from pathlib import Path
from run_sheet import ROOT, fitz, save_json
from polygonal_slabs import shape, polygons
from run_relations import draw_geometry
from run_structural_regions import canvas, box, write_png
from refine_slab_assignment import refine, line_parts


REASONS={
 'NO_PROVED_ACTUATION_GEOMETRY':'Geometria de atuação não comprovada',
 'NO_INTERSECTING_DOMAIN':'Geometria extraída sem interseção com os domínios candidatos',
 'SOME_GROUPS_OR_TRACES_HAVE_NO_INTERIOR_SUPPORT_IN_THIS_DOMAIN':'Parte dos grupos/traços não possui suporte interior no domínio',
 'CONTOUR_TOPOLOGY_REVIEW_FLAG':'Contorno candidato com alerta topológico (faixa estreita)',
 'LIMITED_BAR_OR_DISTRIBUTION_AXIS_SUPPORT':'Suporte parcial da barra ou eixo de distribuição',
 'COMPETING_DOMAINS_REQUIRE_ENGINEER_DECISION':'Domínios concorrentes na mesma parcela',
 'ASSOCIATION_SUPPORTED_INDEPENDENTLY_OF_FULL_CONTAINMENT':'Evidências sustentam associação independentemente da contenção integral'}


def visuals(source, inventory, result, out):
    colors={d['slab']:((i*37%130+40)/255,(i*71%130+40)/255,(i*97%130+40)/255) for i,d in enumerate(result['domains'])}
    original={o['occurrence_id']:o for o in inventory['occurrences']}
    for filename,roi in [('mapa_conferencia.png',[50,145,1910,1205]),('pendencias_L605.png',[580,960,1395,1195]),('pendencias_N21.png',[810,790,1215,995])]:
        doc,page,clip=canvas(source,roi)
        for domain in result['domains']:
            draw_geometry(page,domain['geometry_pdf_pt'],clip,(.6,.6,.6),dashed=True)
            label=domain['source']['label']
            if fitz.Rect(label['bbox']).intersects(clip):
                b=label['bbox'];page.insert_text((b[0]-clip.x0,b[1]-clip.y0-5),domain['slab']+' h='+str(domain['thickness_cm']),fontsize=8,color=colors[domain['slab']])
        for occurrence in result['occurrences']:
            for segment in occurrence['segments']:
                color=colors[segment['slabs'][0]] if len(segment['slabs'])==1 else (.65,.65,.65)
                geometry=shape(segment['geometry_pdf_pt'])
                if not geometry.intersects(shape({'type':'Polygon','coordinates':[[[clip.x0,clip.y0],[clip.x1,clip.y0],[clip.x1,clip.y1],[clip.x0,clip.y1],[clip.x0,clip.y0]]]})):continue
                for poly in polygons(geometry):
                    s=page.new_shape()
                    for ring in [poly.exterior]+list(poly.interiors):
                        s.draw_polyline([fitz.Point(x-clip.x0,y-clip.y0) for x,y in ring.coords])
                    s.finish(color=color,fill=color,fill_opacity=.10,width=.4,even_odd=True);s.commit()
                for line in line_parts(geometry):
                    page.draw_polyline([fitz.Point(x-clip.x0,y-clip.y0) for x,y in line.coords],color=color,width=1)
            if occurrence['requires_engineer_decision']:
                color=(.85,.38,0) if occurrence['state']=='PROBABLE' else (.85,0,.15)
                call=original[occurrence['occurrence_id']]
                clipped=fitz.Rect(call['bbox']) & clip
                if not clipped.is_empty:
                    box(page,list(clipped),clip,'',color,True)
                    page.insert_text((max(2,clipped.x0-clip.x0),max(8,clipped.y0-clip.y0-3)),occurrence['display_id'],fontsize=8,color=color)
        write_png(doc,page,out/filename,'Cores suaves: laje candidata | Cinza: parcela externa sem espessura atribuida | Destaques: laranja provavel; vermelho indeterminada (decisao pendente)')


def report(result, baseline, out):
    transitions=Counter((c['stage9_state'],c['stage91_state']) for c in result['comparison'])
    rows=['# Comparação das 59 ocorrências — Etapas 9 e 9.1','','| Ocorrência | Posição | Etapa 9 | Etapa 9.1 | Lajes / h (cm) | Motivo ou pendência |','|---|---|---|---|---|---|']
    for c in result['comparison']:
        rows.append('| '+' | '.join([c['display_id'],c['position'],c['stage9_state'],c['stage91_state'],', '.join(c['slabs'])+' / '+', '.join(map(str,c['thickness_options_cm'])), '; '.join(REASONS.get(r,r) for r in c['reasons'])])+' |')
    (out/'comparacao_59.md').write_text('\n'.join(rows)+'\n',encoding='utf8')
    pending=[c for c in result['comparison'] if c['requires_engineer_decision']]
    save_json(out/'pendencias.json',pending)
    lines=['# Etapa 9.1 — Associação independente de contenção integral','',
        '## Auditoria e alteração do critério','',
        'A Etapa 9 classificava a ocorrência pela pior classe de suas parcelas. Uma parcela NO_DOMAIN tornava toda a associação INDETERMINATE, mesmo quando barra, faixa e etiqueta sustentavam uma única laje. Isso confundia extensão externa da armadura com incerteza sobre sua laje. A revisão utiliza a partição e as entidades existentes, sem recalcular ou modificar seus polígonos.',
        '', 'A camada derivada separa association_confidence, contour_confidence e os estados históricos das parcelas. RELIABLE significa associação automática sustentada por dados documentais e entidades geométricas interiores; não significa contorno confirmado, validação humana ou aptidão para cálculo resistente. Os nove contornos continuam candidatos. PROBABLE preserva uma hipótese com suporte parcial ou alerta topológico. INDETERMINATE registra ausência de suporte suficiente ou concorrência no mesmo trecho.',
        '', '## Evidências utilizadas','',
        'Para distribuídas: interseção de área, comprimentos interiores da barra e do eixo transversal, e cruzamento de ambos dentro do domínio. Para RELIABLE são necessários os dois comprimentos positivos e o cruzamento interior, além de etiqueta documental de laje/espessura e ausência de alerta topológico. Uma interseção apenas da envoltória não basta. Para localizadas: interseção interior de cada traço contínuo aceito, sem pontes inventadas entre grupos. Suporte incompleto mantém PROBABLE. Nenhum critério usa distância ao texto, centroide, cor ou palavras BASE/REFORÇO.',
        '', 'Não foi aplicado limite de área para descartar pequenas diferenças. Os trechos externos continuam nos segmentos originais, com domínio e espessura não atribuídos. Não são automaticamente ancoragem; a associação da ocorrência à laje não transfere a espessura para esses trechos. A continuidade considerada é a das entidades já extraídas, não uma comprovação da continuidade física das barras.',
        '', '## Comparação','', '| Estado | Etapa 9 | Etapa 9.1 |','|---|---:|---:|']
    for state in ['RELIABLE','PROBABLE','INDETERMINATE']:
        lines.append('| '+state+' | '+str(baseline['metrics']['states'].get(state,0))+' | '+str(result['metrics']['states'].get(state,0))+' |')
    lines+=['','Transições: '+ '; '.join(a+' → '+b+': '+str(n) for (a,b),n in sorted(transitions.items()))+'.',
        '', '```json',json.dumps(result['metrics'],ensure_ascii=False,indent=2),'```',
        '', 'A contagem de associações sustentadas não é taxa de acerto: não houve nova conferência independente de cada associação. A mudança decorre de separar o critério de associação do critério de contenção.',
        '', '## Casos que exigem decisão','',
        'Os destaques do mapa são apenas as ocorrências abaixo. Os demais contornos continuam sujeitos à revisão geométrica geral, sem que isso torne automaticamente pendente a identidade da laje atendida.']
    for c in pending:lines+=['', '- **'+c['display_id']+'/'+c['position']+' — '+c['stage91_state']+'**: '+'; '.join(REASONS.get(r,r) for r in c['reasons'])+'.']
    lines+=['','## Múltiplas lajes, espessuras e preservação','',
        'A mesma ocorrência pode manter várias associações em domínios disjuntos, inclusive com espessuras diferentes. Cada parcela conserva suas opções documentais de espessura. Espessuras distintas na mesma parcela concorrente impedem resolução automática. Não se cria uma altura útil única nem se duplicam barras. Nenhuma ocorrência desta prancha intersectou dois domínios candidatos; a capacidade foi validada em testes sintéticos.',
        '', 'N14 permanece reforço em toda a extensão das duas ocorrências, e R053/N40 permanece traspasse por confirmação do engenheiro. As quatro confirmações locais, a inconsistência N38, os quantitativos, os grupos e todas as geometrias anteriores foram preservados. O inventário completo inclui a camada original da Etapa 9 intacta e uma nova camada refined_slab_assignment.',
        '', '## Entregáveis e próximos passos','',
        '[Mapa de conferência](mapa_conferencia.png) · [Comparação individual das 59 ocorrências](comparacao_59.md) · [Inventário derivado](associacoes.json) · [Pendências](pendencias.json) · [L605](pendencias_L605.png) · [N21](pendencias_N21.png)',
        '', 'Priorizar revisão do contorno L605, dos grupos N21 em L607, da faixa O047/N24 e das geometrias ainda inconclusivas. A falta de interseção não prova ausência de laje ou falha estrutural. Não foram executadas verificações resistentes ou inferências de altura útil.']
    (out/'relatorio.md').write_text('\n'.join(lines)+'\n',encoding='utf8')


def main():
    inp=ROOT/'analises/lajes_associacao_espessuras/inventario.json'
    out=ROOT/'analises/lajes_associacao_refinada';out.mkdir(parents=True,exist_ok=True)
    inventory=json.loads(inp.read_text(encoding='utf8'));baseline=inventory['slab_reinforcement_assignment']
    result=refine(baseline)
    source=Path(inventory['stage5_provenance']['source_pdf']);before=hashlib.sha256(source.read_bytes()).hexdigest()
    if before!=inventory['stage5_provenance']['sha256']:raise ValueError('PDF_CHANGED')
    enriched=copy.deepcopy(inventory);enriched['refined_slab_assignment']=result
    enriched['stage91_provenance']={'input_inventory_sha256':hashlib.sha256(inp.read_bytes()).hexdigest(),'source_pdf_sha256':before,
        'previous_layers_preserved':all(enriched[k]==v for k,v in inventory.items()),
        'source_entities_or_partitions_modified':False,'external_segments_classified_as_anchorage':False}
    save_json(out/'inventario.json',enriched);save_json(out/'associacoes.json',result);save_json(out/'comparacao_59.json',result['comparison'])
    with fitz.open(str(source)) as pdf:visuals(pdf[0],inventory,result,out)
    if hashlib.sha256(source.read_bytes()).hexdigest()!=before:raise ValueError('PDF_CHANGED')
    report(result,baseline,out)
    print(json.dumps(result['metrics'],indent=2))


if __name__=='__main__':main()
