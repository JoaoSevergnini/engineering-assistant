"""Nominal rate inventories and diagnostics; no d or resistance calculation."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
from run_sheet import ROOT,fitz,save_json
from run_structural_regions import canvas,write_png
from run_acting_compositions import draw_polygon
from polygonal_slabs import shape
from steel_quantification import load_concretopy,quantify

OUT=ROOT/'analises/lajes_quantificacao_positiva'


def diagnostics(source,result,out):
    colors={'INDIVIDUAL_NOMINAL_AREA':(.1,.4,.8),'CONFIRMED_JOINT_NOMINAL_AREA':(0,.6,.25),
        'NON_ADDITIVE_LAP':(.9,.4,0),'PENDING_COMPOSITION':(.65,.1,.7)}
    for filename,roi in [('mapa_quantificacao.png',[50,145,1910,1205]),('L603_esquerda_As.png',[280,610,885,1020]),('L603_direita_As.png',[1090,610,1700,1020])]:
        doc,page,clip=canvas(source,roi)
        for c in result['compositions']:
            total=c['nominal_total_cm2_per_m']
            bounds=shape(c['geometry_pdf_pt']).bounds
            label=c['source_composition_id']+(' '+format(total,'.2f') if total is not None else '')
            if bounds[2]-bounds[0]<40 or bounds[3]-bounds[1]<8:label=''
            draw_polygon(page,c['geometry_pdf_pt'],clip,colors[c['quantification_kind']],label,.10)
        write_png(doc,page,out/filename,'Valores nominais em cm2/m | Azul: individual | Verde: soma nominal autorizada | Laranja: traspasse sem soma | Roxo: pendente | Sem calculo de d/MR')


def report(result,audit,out):
    byid={o['display_id']:o for o in result['occurrences']}
    cbyid={c['source_composition_id']:c for c in result['compositions']}
    rows=['# Etapa 11 — Quantificação nominal das armaduras positivas','',
        '## Auditoria e método','',
        'Reutilizados os 59 registros, 35 regiões distribuídas, 119 células e confirmações da Etapa 10, sem alterar geometrias, classes, diâmetros, espaçamentos ou quantitativos. A área circular da barra é obtida da propriedade pública Concretopy.Barra.area_cm2. A única operação adicional é multiplicar por 100/s, com s em cm. Não se usam quantidade impressa, comprimento nominal ou dimensões da envoltória como substitutos do espaçamento.',
        '', '`As/m = [π (φ/10)²/4] × (100/s)`, em cm²/m. Valores internos são preservados sem arredondamento; apenas as tabelas e mapas usam duas casas decimais.',
        '', '## Resultado','', '```json',json.dumps(result['metrics'],ensure_ascii=False,indent=2),'```',
        '', 'Há 38 taxas individuais calculáveis: 35 ocorrências distribuídas com área sustentada e três chamadas com espaçamento, mas geometria pendente (N18/O009, N33/O014 e N41/O057). Estas três taxas não validam região de atuação ou composição. As 21 ocorrências sem espaçamento indicado permanecem sem As/m; quantidade total de barras não foi convertida artificialmente em taxa.',
        '', 'Das 119 células, 70 possuem valor individual nominal; três têm soma nominal autorizada pela função conjunta e pela regra atual de camada intercalada; cinco não admitem soma por traspasse documental/local; as outras 41 permanecem sem total composto. As classificações originais são preservadas separadamente. Não se soma o conjunto inteiro de células como quantitativo da prancha.',
        '', '## Exemplos numéricos','', '| Ocorrência / região | Armadura | As individual ou total (cm²/m) | Fundamento |','|---|---|---:|---|']
    for id in ['O043','O044','O034','O035']:
        o=byid[id];rows.append('| '+id+' | '+o['position']+f" Ø{o['diameter_mm']:g} c/{o['spacing_cm']:g} | {o['as_cm2_per_m']:.2f} | Taxa individual documental |")
    for id in ['C059','C083','C088']:
        c=cbyid[id];rows.append('| '+id+' | '+' + '.join(c['positions'])+f" | {c['nominal_total_cm2_per_m']:.2f} | Função conjunta sustentada no domínio existente; soma nominal |")
    rows+=['', 'C083 e C088 correspondem a N13+N14, esquerda e direita. C059 corresponde à confirmação local N15+N14, com as mesmas bitolas/espaçamentos; não foi renomeada como N13. A N14 foi quantificada individualmente, embora não haja célula somente N14 na partição real; não foi criada uma região isolada fictícia. Nas parcelas triplas C071/C076, as taxas individuais estão disponíveis, mas o total integral continua nulo. C092 e as quatro células com N40 não recebem soma.',
        '', '## Mesma camada física não significa mesmo centro','',
        'A regra fornecida pelo engenheiro nesta Etapa 11 é registrada em criterios_documentais.json e vinculada ao hash deste PDF: base e reforço positivos são intercalados na mesma camada física. Não se cria camada adicional para o reforço. Cada componente mantém diâmetro e espaçamento próprios. A regra não é aplicada às armaduras localizadas de furos, que podem ter distribuição superior/inferior distinta, nem a outro documento sem perfil explícito.',
        '', 'Os centros não foram igualados: os raios de Ø8 e Ø5 são 0,40 e 0,25 cm. Se posteriormente for comprovada a mesma referência de superfície de cobrimento para ambos, seus centros poderão diferir; essa condição ainda não foi usada para calcular d. Não se adotou uma bitola equivalente nem centro único para a composição.',
        '', '## Espessuras, cobrimento e altura útil','',
        'A espessura vem das etiquetas documentais e de associações RELIABLE, independentemente da qualidade completa do contorno. Associações PROBABLE mantêm espessuras candidatas, sem promovê-las a valores confiáveis. Casos de espessuras distintas têm entradas separadas por laje/espessura e nenhum d único. Nenhuma ocorrência real desta prancha recebeu duas espessuras confiáveis; a separação de casos foi verificada sinteticamente. As referências espaciais continuam em pontos PDF, sem serem tratadas como centímetros físicos.',
        '', 'Foi identificado cobrimento documental de **2,0 cm** no detalhe “COBRIMENTO ARMADURA LAJES MACIÇAS”: cota positiva T166:0, etiqueta T156:0, título T152:0 e unidade geral em centímetros T265:0. A leitura combina textos extraídos e inspeção do desenho; é interpretação documental do assistente, não confirmação humana nova nem comprovação de execução. O valor não foi inventado ou adotado por norma. Seu escopo é o detalhe geral de lajes maciças, sem comprovar o centro de cada bitola/direção.',
        '', '[Detalhe original de cobrimento](detalhe_cobrimento_original.png) · [Nota original de unidades](nota_unidades_original.png)',
        '', 'A distância do centro à face tracionada e d permanecem nulos. Falta confirmar a referência vertical específica e a ordem em relação à armadura ortogonal. O perfil de mesma camada entre base/reforço não resolve essa relação entre direções. Para ocorrências sem laje confiável ou sem geometria sustentada, essas pendências também ficam explícitas. A ausência desses dados não impede o cálculo nominal de As/m.',
        '', '## Preparação para o Concretopy','',
        'O código local do Concretopy foi inspecionado, sem alterações: armaduras.py, verificacoes/flexao.py, secoes.py, detalhamento/arranjos.py e unidades.py. Sua propriedade Barra.area_cm2 foi efetivamente reutilizada; nenhuma função de flexão foi executada.',
        '', 'A entrada preparada usa geometria da seção em cm, diâmetros em mm, tensões em MPa, forças em kN e momentos em kN·cm. A referência de largura é 100 cm. A densidade 100/s pode ser fracionária e não é numero_barras de uma faixa finita; por isso esse argumento da API fica nulo. Os parâmetros de materiais não foram inventados.',
        '', 'A interface CamadaArmaduraLongitudinal representa barras iguais e exige quantidade inteira. O posicionamento automático empilha os grupos com afastamento vertical; mesmo com d explícito, o verificador de flexão rejeita envelopes verticais sobrepostos entre camadas. Portanto, enviar Ø8 e Ø5 intercalados como duas camadas distorce o modelo ou é rejeitado. SecaoRetangular também tem padrão de estribo de viga, que não deve ser importado silenciosamente para lajes.',
        '', 'A etapa seguinte precisará de contrato/modelo que represente famílias de bitolas distintas na mesma camada física, com centros próprios e interpretação lateral adequada. Não basta desligar validações nem reutilizar o empilhamento de vigas. Essa adaptação foi somente documentada; não foi implementada, e o pacote Concretopy e os módulos de vigas/pilares permanecem intactos. [Auditoria com hashes](auditoria_concretopy.json).',
        '', '## Entregáveis e limites','',
        '[Propriedades das ocorrências](ocorrencias.json) · [Composições confirmadas e pendentes](composicoes.json) · [Tabela das 59 ocorrências](ocorrencias.md) · [Diagnóstico gráfico](mapa_quantificacao.png) · [N13/N14 esquerda](L603_esquerda_As.png) · [N13/N14 direita](L603_direita_As.png)',
        '', 'Os registros distinguem taxa documental, elegibilidade geométrica, espessura confiável, soma nominal e resistência. N14 continua reforço; N40 continua traspasse sem adição independente; as nove pendências anteriores permanecem preservadas. Não há conclusão de suficiência, conformidade, necessidade de reforço, altura útil ou resistência à flexão.']
    (out/'relatorio.md').write_text('\n'.join(rows)+'\n',encoding='utf8')
    table=['# Taxas documentais das 59 ocorrências','','| Ocorrência | Posição | Ø (mm) | s (cm) | As (cm²/m) | Tipo confirmado | Lajes | h confiável (cm) | Situação da taxa |','|---|---|---:|---:|---:|---|---|---|---|']
    for o in result['occurrences']:
        table.append('| '+' | '.join([o['display_id'],o['position'],str(o['diameter_mm']),str(o['spacing_cm']) if o['spacing_cm'] is not None else '—',
            f"{o['as_cm2_per_m']:.2f}" if o['as_cm2_per_m'] is not None else '—',o['reinforcement_type'],', '.join(o['slabs']) or '—',
            str(o['thickness_cm']) if o['thickness_cm'] is not None else '—',o['rate_state']])+' |')
    (out/'ocorrencias.md').write_text('\n'.join(table)+'\n',encoding='utf8')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--concretopy-root',type=Path,default=ROOT.parent/'concretopy');args=parser.parse_args()
    OUT.mkdir(parents=True,exist_ok=True);inp=ROOT/'analises/lajes_composicao_atuacao/inventario.json';ent=ROOT/'analises/lajes_geometria_lideres/entidades_pagina.json';profile_path=OUT/'criterios_documentais.json'
    inventory=json.loads(inp.read_text(encoding='utf8'));texts=json.loads(ent.read_text(encoding='utf8'))['texts'];profile=json.loads(profile_path.read_text(encoding='utf8'))
    source=Path(inventory['stage5_provenance']['source_pdf']);before=hashlib.sha256(source.read_bytes()).hexdigest()
    if before!=inventory['stage5_provenance']['sha256']:raise ValueError('SOURCE_PDF_CHANGED')
    area,audit=load_concretopy(args.concretopy_root);result=quantify(inventory,profile,texts,area)
    enriched=copy.deepcopy(inventory);enriched['positive_steel_quantification']=result
    enriched['stage11_provenance']={'source_pdf_sha256':before,'input_inventory_sha256':hashlib.sha256(inp.read_bytes()).hexdigest(),
        'entities_sha256':hashlib.sha256(ent.read_bytes()).hexdigest(),'profile_sha256':hashlib.sha256(profile_path.read_bytes()).hexdigest(),
        'all_previous_layers_preserved':all(enriched[k]==v for k,v in inventory.items()),'concretopy_audit':audit}
    for filename,data in [('inventario.json',enriched),('quantificacao.json',result),('ocorrencias.json',result['occurrences']),('composicoes.json',result['compositions']),('auditoria_concretopy.json',audit)]:save_json(OUT/filename,data)
    with fitz.open(str(source)) as pdf:
        diagnostics(pdf[0],result,OUT)
        cover=profile.get('cover_evidence')
        if cover:
            pdf[0].get_pixmap(matrix=fitz.Matrix(2.5,2.5),clip=fitz.Rect(cover['detail_bbox_pdf_pt'])).save(str(OUT/cover['image_reference']))
            units=next(t for t in texts if t['id']==cover['units_text_id']);b=fitz.Rect(units['bbox'])+(-5,-5,5,5)
            pdf[0].get_pixmap(matrix=fitz.Matrix(2,2),clip=b).save(str(OUT/cover['units_image_reference']))
    if hashlib.sha256(source.read_bytes()).hexdigest()!=before:raise ValueError('SOURCE_PDF_CHANGED')
    _,after=load_concretopy(args.concretopy_root)
    if audit['source_sha256']!=after['source_sha256']:raise ValueError('CONCRETOPY_SOURCE_CHANGED')
    report(result,audit,OUT);print(json.dumps(result['metrics'],indent=2))


if __name__=='__main__':main()
