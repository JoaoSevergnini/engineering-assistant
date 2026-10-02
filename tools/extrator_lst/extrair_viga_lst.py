"""Extracao documental de LST TQS. Sem verificacoes estruturais. Python >=3.10."""
import argparse
import hashlib
import json
import re
import unicodedata
from pathlib import Path

CATEGORIES = 'geometria materiais vaos apoios reacoes esforcos_ao_longo_dos_vaos dimensionamento_flexao_positiva dimensionamento_flexao_negativa cisalhamento ancoragens grampos armadura_suspensao avisos_tqs'.split()
NUMBER = r'[-+]?(?:\d+(?:[.,]\d*)?|[.,]\d+)'
HEADER = re.compile(r'^\s*(?:CAD\s*/\s*Vigas\s+|Lendo a\s+)?VIGA\s*[=:]\s*(\d+)(?=\s|\.|$)', re.I)
UNITS = {'m': ('m',1), 'cm': ('m',.01), 'mm': ('m',.001), 'cm2': ('m2',.0001), 'cm3': ('m3',.000001), 'cm4': ('m4',.00000001), 'tf': ('kN',9.80665), 'tf*m': ('kN.m',9.80665), 'tfm': ('kN.m',9.80665), 'tfcm': ('kN.m',.0980665), 'tf.cm': ('kN.m',.0980665), 'tf,cm': ('kN.m',.0980665), 'tf*cm': ('kN.m',.0980665), 'tf/m': ('kN/m',9.80665), 'tf/m2': ('MPa',.00980665), 'kgf/cm2': ('MPa',.0980665), 'mpa': ('MPa',1), '%': ('%',1)}

def fold(s):
    return ''.join(c for c in unicodedata.normalize('NFKD',s) if not unicodedata.combining(c)).lower()

def num(s):
    return float(s.replace(',','.'))

def quantity(value, unit=None):
    result={'valor':value,'unidade_original':unit}
    if unit and unit.lower() in UNITS:
        u,f=UNITS[unit.lower()]
        result['normalizado']={'valor':round(value*f,12),'unidade':u,'criterio':'conversao literal da unidade impressa; sem correcao de inconsistencias do TQS'}
    return result

def fields(line):
    """Campos explicitos, mantendo repeticoes, contexto e posicao de coluna."""
    result=[]
    pattern=r'([^=|]+?)\s*=\s*('+NUMBER+r')(?:\s*(kgf/cm2|tf/m2|tf/m|tf\s*\*\s*cm|tf\s*\*\s*m|tf[.,]cm|tfcm|tfm|cm[234]?|mm|MPa|tf|m|%)(?![A-Za-z]))?'
    for m in re.finditer(pattern,line,re.I):
        label=re.split(r'\s+-\s+|\s{2,}',m[1].strip())[-1].strip(' /-')
        if not label: continue
        result.append({'rotulo_original':label,'chave':re.sub(r'[^a-z0-9]+','_',fold(label)).strip('_'),'coluna':m.start()+1,**quantity(num(m[2]), re.sub(r'\s+','',m[3]) if m[3] else None)})
    return result

def extract(folder, beam='V504', encoding='cp1252'):
    number=int(beam.upper().removeprefix('V'))
    out={'schema_version':'1.0','viga':f'V{number}','escopo':'extracao documental, sem verificacao estrutural','categorias':{c:[] for c in CATEGORIES},'outros_dados':[],'arquivos':[],'trechos':[], 'notas_extracao':[
        'Ocorrencias e etapas de processamento sao preservadas separadamente; nao representam uma unica solucao final.',
        'Numeracao de vaos e a original de cada relatorio. Vaos de comprimento zero nao sao removidos nem renumerados.',
        'Unidades ausentes permanecem null. Conversoes seguem unidades impressas, mesmo quando inconsistentes.',
        'Registros documentais preservam todas as linhas nao vazias dos blocos. Campos e tabelas reconhecidos acrescentam estrutura; consulte o texto para sintaxes nao normalizadas.',
        'Ausencia de registro de aviso ou armadura nao significa ausencia de problema ou quantidade zero.',
        'Asteriscos sao marcadores do relatorio; nao sao convertidos automaticamente em erro estrutural.'
    ]}
    def add(cats, data, source):
        record={**data,'origem':source}
        for cat in cats: out['categorias'][cat].append(record)
        if not cats: out['outros_dados'].append(record)
    files=sorted(p for p in Path(folder).iterdir() if p.suffix.lower()=='.lst')
    if not files: raise ValueError('Nenhum LST encontrado')
    for path in files:
        raw=path.read_bytes()
        text=raw.decode(encoding, errors='strict')
        # LF defines physical lines; form feed remains in original excerpts.
        lines=text.split('\n')
        lines=[s.removesuffix('\r') for s in lines]
        starts=[(i,int(m[1])) for i,s in enumerate(lines) if (m:=HEADER.search(s))]
        spans=[(i,starts[k+1][0] if k+1<len(starts) else len(lines)) for k,(i,n) in enumerate(starts) if n==number]
        out['arquivos'].append({'arquivo':path.name,'caminho':str(path.resolve()),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'encoding':encoding,'blocos_viga':len(spans),'status':'vazio' if not raw else 'viga_encontrada' if spans else 'sem_bloco_da_viga'})
        if starts:
            out['trechos'].append({'arquivo':path.name,'tipo':'cabecalho_global','linha_inicial':1,'linha_final':starts[0][0],'texto':'\n'.join(lines[:starts[0][0]])})
        for start,end in spans:
            out['trechos'].append({'arquivo':path.name,'tipo':'bloco_viga','linha_inicial':start+1,'linha_final':end,'texto':'\n'.join(lines[start:end])})
            name=path.name.upper()
            default={'FLEXPS.LST':'dimensionamento_flexao_positiva','RELDTFPS.LST':'dimensionamento_flexao_positiva','FLEXNG.LST':'dimensionamento_flexao_negativa','RELDTFNG.LST':'dimensionamento_flexao_negativa','ESTRIB.LST':'cisalhamento','RELDTVET.LST':'cisalhamento'}.get(name)
            table=None; table_source=None; section='inicio'; vao=None; side=None; anchor=False
            for i in range(start,end):
                line=lines[i]; t=fold(line); stripped=line.strip()
                source={'arquivo':path.name,'linha_inicial':i+1,'linha_final':i+1,'texto':line}
                if not stripped or re.fullmatch(r'[-=\s]+',line):
                    table=None
                    continue
                cats=set([default] if default else [])
                if 'geometria dos vao' in t: section=stripped; anchor=False
                if 'geometria dos apoio' in t: section=stripped; anchor=False
                if 'reacoes nos apoios' in t: section=stripped
                if any(x in t for x in ['momentos fletores','forcas cortantes','momentos torsores','fi,estribo por ponto','fi,pe -','estribo por ponto','esforcos solicitantes','esforcos provenientes']): section=stripped
                if any(x in t for x in ['esquerda do vao','direita do vao','meio do vao']):
                    side='esquerda' if 'esquerda' in t else 'direita' if 'direita' in t else 'meio'
                vm=re.search(r'\bvao\s*(?:[=\-]|(?:m[k]?,(?:neg|pos)|fiest|espac|fi,es|esp,es)\s*=)\s*(\d+)',t)
                if vm: vao=int(vm[1])
                if 'ancoragem das armaduras' in t or t.lstrip().startswith('ancoragem -'): anchor=True; section=stripped
                if 'agrupamento de barras' in t or 'compatibilizacao e uniao' in t: anchor=False; section=stripped
                if anchor or 'ancor' in t: cats.add('ancoragens')
                if 'grampo' in t: cats.add('grampos')
                if 'susp' in t or 'astrt' in t: cats.add('armadura_suspensao')
                if 'fck' in t or 'aco -' in t or 'aco ca' in t or 'dagreg' in t: cats.add('materiais')
                if any(x in t for x in ['cobr','geometria','comprimento=','/l=','c,sup.adic']): cats.add('geometria')
                if any(x in t for x in ['aviso','erro','atencao','nao detalhavel','nao calculado','prolongando barra']) or '****' in t: cats.add('avisos_tqs')
                if name=='ORDCON.LST' and not t.startswith('lendo a'): cats.add('avisos_tqs')
                if re.search(r'\bvao\s+(?:comprim\.|l\s+b\s+h)',t): table='geometria'; table_source=source
                elif re.search(r'titulo\s+(?:bp|dimensaoi)',t): table='apoios'; table_source=source
                elif 'r.apoio-no.' in t or 'reac. apoio -' in t: table='reacoes_numeradas'; table_source=source
                elif 'titulo' in t and 'reacao_max' in t: table='reacoes'; table_source=source
                elif 'apoio' in t and 'faixa' in t and 'bar/fx' in t: table='barras_negativas'; table_source=source
                values=stripped.split()
                data=None
                if table in ('geometria','apoios','reacoes','reacoes_numeradas'):
                    cats.add('geometria' if table=='geometria' else 'apoios' if table=='apoios' else 'reacoes')
                if table=='geometria' and re.match(r'^\d+\s',stripped):
                    keys='vao comprimento largura altura mesa_superior mesa_inferior tipo_secao espessura_laje_superior espessura_laje_inferior face_superior_eixo face_lateral_eixo'.split()
                    unit='m' if name in ('VGESFS.LST','RELDTVGS.LST') else 'cm'
                    data={'tipo':'geometria_tabular','campos':{k:quantity(num(v),None if k in ('vao','tipo_secao') else unit) for k,v in zip(keys,values)},'cabecalho':table_source}
                    cats.update(['geometria','vaos']); vao=int(values[0])
                    if name=='RELDTVET.LST': data['ressalva']='Unidade impressa cm; valores divergem dos demais relatorios. Nao corrigidos.'
                elif table=='apoios' and re.match(r'^[VP]\S+\s+[-\d]',stripped):
                    keys='nome largura excentricidade continuidade alavanca dimensao_superior espessura_inferior espessura_superior'.split()
                    if len(values)==4: keys=keys[:4]
                    unit='m' if name=='RELDTVGS.LST' else 'cm'
                    data={'tipo':'apoio','campos':{k:quantity(num(v),unit) if re.fullmatch(NUMBER,v) else v for k,v in zip(keys,values)},'cabecalho':table_source}; cats.add('apoios')
                elif table in ('reacoes','reacoes_numeradas') and re.match(r'^(?:\d+|[VP]\S+)\s+[-\d]',stripped):
                    if table=='reacoes': keys=['nome','maxima','minima']
                    elif name=='VGESFS.LST': keys='numero maxima minima largura depev morte nome momento_maximo momento_minimo pilars espesi espess percentual_rdmo pilar_1 pilar_2 pilar_3 pilar_4 pilar_5 pilar_6'.split()
                    else: keys='numero maxima minima largura depev morte nome momento_maximo momento_minimo pilar_1 pilar_2 pilar_3 pilar_4 pilar_5 pilar_6'.split()
                    data={'tipo':'reacao_apoio','campos':{k:quantity(num(v),'tf' if k in ('maxima','minima') else None) if re.fullmatch(NUMBER,v) else v for k,v in zip(keys,values)},'cabecalho':table_source,'unidade_reacoes':'tf' if name=='RELDTVGS.LST' else 'tf (convencao do formato, corroborada por RELDTVGS)'}; cats.update(['reacoes','apoios'])
                elif table=='barras_negativas' and re.match(r'^\d+\s',stripped):
                    keys='apoio faixa barras_por_faixa diametro distancia_face comprimento dobra_esquerda dobra_direita'.split()
                    data={'tipo':'barras_negativas','campos':{k:quantity(num(v),'cm' if j>=3 else None) for j,(k,v) in enumerate(zip(keys,values))},'cabecalho':table_source}
                # Series use printed column positions: blank interior cells stay null.
                series=re.match(r'^\s*((?:Q|M|MT)\s+(?:MN|MX)\.)\s*VAO\s*=\s*(\d+)\s+(.+)$',line,re.I) if name=='VGESFS.LST' else None
                if name=='RELDTVGS.LST': series=re.match(r'^\s*([MV]\w*,\w+)\s+V.o=\s*(\d+)\s+(.+)$',line,re.I)
                detail=re.match(r'^\s*V.o\s+(Mk,neg|M,neg|M,pos|Fiest|Espac|fi,es|esp,es)=\s*(\d+)(.*)$',line,re.I)
                shear=re.match(r'^\s*V.o=\s*(\d+)\s+(V,max|V,min|Ts,max)\s*=(.*)$',line,re.I)
                if series:
                    label,n,tail=series.groups(); cells=tail.split()
                    if len(cells)==13 and all(re.fullmatch(NUMBER,x) for x in cells):
                        vals=[num(x) for x in cells]
                        unit='tf' if fold(label).startswith(('q','vk')) else 'tf*m'
                        data={'tipo':'serie_13_secoes','grandeza_original':label.strip(),'vao_original':int(n),'valores':[quantity(v,unit) for v in vals],'secoes':list(range(1,14)),'unidade_base':'convencao do formato, corroborada por RELDTVGS [Tf,m]'}; cats.add('esforcos_ao_longo_dos_vaos')
                elif detail or shear:
                    if detail: label,n,tail=detail.groups(); offset=detail.start(3)
                    else: n,label,tail=shear.groups(); offset=shear.start(3)
                    header=next((lines[j] for j in range(i-1,max(start-1,i-12),-1) if re.search(r'(secao|ponto)\s*[:=]',fold(lines[j]))),None)
                    if header:
                        positions=[m.end() for m in re.finditer(r'\d+',header)]
                        if len(positions)==13:
                            vals=[None]*13
                            cells=list(re.finditer(NUMBER,tail.split('M,max')[0]))
                            for cell in cells:
                                absolute_end=offset+cell.end()
                                slot=min(range(13),key=lambda k:abs(positions[k]-absolute_end))
                                if abs(positions[slot]-absolute_end)<=3:
                                    vals[slot]=num(cell[0])
                            unit='tf' if label.lower().startswith('v,') else 'tf*m' if label.lower().startswith('ts') else 'tf,cm' if label.lower().startswith('m') else None
                            data={'tipo':'serie_13_secoes','grandeza_original':label,'vao_original':int(n),'secoes':list(range(1,14)),'valores':[quantity(v,unit) if v is not None else None for v in vals],'cabecalho_texto':header}
                            cats.add('esforcos_ao_longo_dos_vaos' if unit else 'cisalhamento')
                if name=='ESTRIB.LST' and re.match(r'^\s*\d+\s*-\s*\d+',line):
                    nums=re.findall(NUMBER,line)
                    keys='inicio fim bitola_1 espacamento_1 espacamento_calculado_1 ramos_1 bitola_2 espacamento_2 espacamento_calculado_2 ramos_2 bitola_3 espacamento_3 espacamento_calculado_3 ramos_3 as vsd vrd2 bitola_escolhida espacamento_escolhido ramos_escolhidos as_tirante as_suspensao'.split()
                    # The hyphen between endpoints is a separator, not a sign.
                    nums=re.findall(NUMBER,re.sub(r'^(\s*\d+)\s*-\s*',r'\1 ',line))
                    data={'tipo':'faixa_estribos','campos':{k:quantity(num(v),'mm' if 'bitola' in k else 'cm' if k in ('inicio','fim') or 'espacamento' in k else 'tf' if k in ('vsd','vrd2') else 'cm2' if k.startswith('as') else None) for k,v in zip(keys,nums)}}; cats.add('armadura_suspensao')
                if name=='RELGER.LST' and '|' in line:
                    cells=line.split('|')[1:]
                    data={'tipo':'flexao_por_posicao','posicoes':{k:{'texto':v,'campos':fields(v)} for k,v in zip(('esquerda','meio','direita'),cells)}}
                    cats.update(['dimensionamento_flexao_positiva','dimensionamento_flexao_negativa'])
                if name=='RELGER.LST' and re.match(r'^\s*\[tf,cm\]\s+[-0-9]',line):
                    tokens=re.findall(NUMBER,line.split(']',1)[1].replace('.-','. '))
                    keys='inicio fim vsd vrd2 modelo angulo asw_c asw_min asw_c_t bitola espacamento ramos as_tirante as_suspensao'.split()
                    data={'tipo':'cisalhamento_resumo','campos':{k:quantity(num(v), 'tf' if k in ('vsd','vrd2') else 'mm' if k=='bitola' else 'cm' if k in ('inicio','fim','espacamento') else None) for k,v in zip(keys,tokens)}}
                    cats.update(['cisalhamento','armadura_suspensao'])
                if not data and '=' in line:
                    vector=re.match(r'^([^=]+)=\s*('+NUMBER+r'(?:\s+'+NUMBER+r')+)\s*$',line)
                    if vector:
                        data={'tipo':'vetor_documental','rotulo_original':vector[1].strip(),'valores':[num(x) for x in vector[2].split()],'unidade':None,'observacao':'Indices e unidades conforme contexto original; sem associacao automatica a vaos ou apoios.'}
                explicit=fields(line)
                for m in re.finditer(r'([^=|]+?)=\s*(NAO|SIM)(?=\s|$)',line,re.I):
                    explicit.append({'rotulo_original':re.split(r'\s{2,}',m[1].strip())[-1],'valor':m[2].upper()=='SIM','texto_original':m[2]})
                steel=re.search(r'CA[- ]?\d+[A-Z]?',line)
                if steel and 'materiais' in cats: explicit.append({'chave':'classe_aco','valor':steel[0]})
                add(sorted(cats),{'tipo':'registro_documental','secao':section,'vao_contexto_original':vao,'lado_contexto':side,'campos_explicitos':explicit,'tokens':values,'normalizacao':data},source)
    if not any(f['blocos_viga'] for f in out['arquivos']): raise ValueError(f'Viga V{number} nao encontrada')
    out['cobertura']={'arquivos_lidos':len(files),'blocos_extraidos':sum(f['blocos_viga'] for f in out['arquivos']),'registros_por_categoria':{k:len(v) for k,v in out['categorias'].items()},'registros_outros':len(out['outros_dados'])}
    return out

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pasta',type=Path)
    parser.add_argument('--viga',default='V504')
    parser.add_argument('--saida',type=Path,required=True)
    parser.add_argument('--encoding',default='cp1252')
    args=parser.parse_args()
    result=extract(args.pasta,args.viga,args.encoding)
    args.saida.parent.mkdir(parents=True,exist_ok=True)
    args.saida.write_text(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print(json.dumps(result['cobertura'],ensure_ascii=True))

if __name__=='__main__': main()
