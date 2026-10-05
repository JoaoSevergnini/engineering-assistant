"""Partição por eventos documentais, preservando intervalos fechados de barras."""
import copy
from decimal import Decimal
import math

GEOMETRY_KEYS = ('bw_cm', 'h_cm', 'cover_cm', 'stirrup_diameter_mm')


def decimal(value):
    if isinstance(value, bool) or not isinstance(value, (int,float)) or not math.isfinite(value):
        raise ValueError('Coordenada ausente ou inválida.')
    return Decimal(str(value))


def contains(region, x):
    x=decimal(x); a=decimal(region['x_start_m']); b=decimal(region['x_end_m'])
    return (a<x<b or x==a and region['include_start'] or x==b and region['include_end'])


def compose_layers(bars):
    """Índice do vetor = camada documental a partir da mesma face inferior."""
    layers={}; issues=[]
    for bar in bars:
        if bar.get('function') != 'positive':
            issues.append('unresolved_function:'+str(bar['mark']))
        vector=bar.get('layers')
        if bar.get('face')!='lower' or not isinstance(vector,list) or not vector or any(type(n)!=int or n<0 for n in vector) or sum(vector)!=bar.get('bars'):
            issues.append('unresolved_physical_layers:'+str(bar['mark'])); continue
        diameter=bar.get('diameter_mm')
        if isinstance(diameter,bool) or not isinstance(diameter,(int,float)) or not math.isfinite(diameter) or diameter<=0:
            issues.append('unknown_diameter:'+str(bar['mark'])); continue
        for i,n in enumerate(vector,1):
            if n:
                layers.setdefault(i,[]).append({'mark':bar['mark'],'count':n,'diameter_mm':diameter,'source':copy.deepcopy(bar.get('source'))})
    composition=[{'layer':i,'components':components} for i,components in sorted(layers.items())]
    if not bars:
        issues.append('no_positive_reinforcement')
    if layers and sorted(layers)!=list(range(1,max(layers)+1)):
        issues.append('unsupported_missing_physical_layer')
    for layer in composition:
        diameters={c['diameter_mm'] for c in layer['components']}
        if len(diameters)!=1:
            issues.append('unsupported_reinforcement_composition:mixed_diameters_layer_'+str(layer['layer']))
        else:
            layer.update(numero_barras=sum(c['count'] for c in layer['components']),diametro_mm=next(iter(diameters)),d_cm=None)
    return {'marks':[b['mark'] for b in bars],'layers':composition,
            'status':'unresolved' if issues else 'resolved','issues':issues,
            'layer_identity_basis':'Índice explícito do vetor beam_model, mesma face lower; não inferido por bitola.'}


def decompose_regions(bars, domain, transverse_regions=None):
    """Partição única: interiores por eventos + limites compatíveis ou pontuais.

    transverse_regions contêm intervalos comuns fechados e quatro operandos.
    None permite decomposição longitudinal sem configuração transversal.
    Intervalos desconhecidos nunca são tratados como ausência.
    """
    start,end=map(decimal,domain)
    if start>=end:
        raise ValueError('Domínio físico inválido.')
    if len({b['mark'] for b in bars})!=len(bars):
        raise ValueError('Marcas duplicadas não podem ser contadas duas vezes.')
    entries=[('bar',i,b) for i,b in enumerate(bars)]
    entries += [('transverse',i,t) for i,t in enumerate(transverse_regions or [])]
    intervals={};unknown=[];events={start,end}
    for kind,index,entity in entries:
        a,b=entity.get('x_start_common'),entity.get('x_end_common')
        if a is None or b is None:
            unknown.append((kind,index));continue
        a,b=decimal(a),decimal(b)
        if a>b:
            raise ValueError('Intervalo invertido: '+str(entity.get('mark',index)))
        intervals[(kind,index)]=(a,b)
        events.update(x for x in (a,b) if start<=x<=end)

    def state(x):
        active=[i for i,b in enumerate(bars) if ('bar',i) in intervals and intervals[('bar',i)][0]<=x<=intervals[('bar',i)][1]]
        ts=[i for i,t in enumerate(transverse_regions or []) if ('transverse',i) in intervals and intervals[('transverse',i)][0]<=x<=intervals[('transverse',i)][1]]
        configurations=[{k:(transverse_regions[i].get(k)) for k in GEOMETRY_KEYS} for i in ts]
        geometry=configurations[0] if configurations and all(c==configurations[0] for c in configurations) and not any(k=='transverse' for k,i in unknown) else None
        return active,ts,geometry

    def make(a,b,x,kind):
        active,ts,geometry=state(x)
        geometric=compose_layers([bars[i] for i in active])
        if any(k=='bar' for k,i in unknown):
            geometric['status']='unresolved';geometric['issues'].append('unknown_positive_interval')
        return {'kind':kind,'x_start_m':float(a),'x_end_m':float(b),'include_start':False,'include_end':False,
                'geometric_reinforcement':geometric,'transverse_geometry':geometry,
                'transverse_status':'resolved' if geometry and all(v is not None for v in geometry.values()) else 'unresolved',
                'provenance':{'bars':[{'mark':bars[i]['mark'],'x_start_common':bars[i].get('x_start_common'),'x_end_common':bars[i].get('x_end_common'),
                                     'x_start_cm':bars[i].get('x_start_cm'),'x_end_cm':bars[i].get('x_end_cm'),
                                     'source':copy.deepcopy(bars[i].get('source')),'mapping':copy.deepcopy(bars[i].get('mapping_provenance'))} for i in active],
                              'transverse':[copy.deepcopy((transverse_regions[i].get('provenance') or {})) for i in ts],
                              'unresolved_intervals':[{'kind':k,'index':i,
                                'entity':copy.deepcopy({key:value for key,value in (bars[i] if k=='bar' else transverse_regions[i]).items()
                                                       if key in ('mark','id','x_start_common','x_end_common','source','mapping_provenance','provenance')})} for k,i in unknown]}}

    def signature(region):
        return (region['geometric_reinforcement']['marks'],region['transverse_geometry'])

    points=sorted(events)
    interiors=[make(a,b,(a+b)/2,'interval') for a,b in zip(points,points[1:])]
    isolated=[]
    for j,x in enumerate(points):
        exact=make(x,x,x,'boundary_point')
        right=interiors[j] if j<len(interiors) else None
        left=interiors[j-1] if j else None
        # Preferência direita somente quando a configuração fechada coincide.
        if right and signature(right)==signature(exact):
            right['include_start']=True
            right['provenance'].setdefault('boundary_transverse',[]).extend(exact['provenance']['transverse'])
        elif left and signature(left)==signature(exact):
            left['include_end']=True
            left['provenance'].setdefault('boundary_transverse',[]).extend(exact['provenance']['transverse'])
        else:
            exact.update(include_start=True,include_end=True)
            isolated.append(exact)
    result=sorted(interiors+isolated,key=lambda r:(r['x_start_m'],0 if r['kind']=='boundary_point' else 1))
    for i,r in enumerate(result,1):
        r['region_id']='R'+str(i)
    return result
