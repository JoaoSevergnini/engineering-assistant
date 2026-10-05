"""Golden real V1001: diagrama linear e capacidade isolada da N5, sem validar cortes."""
import argparse
import copy
from dataclasses import asdict
import hashlib
import importlib
import json
from pathlib import Path
import sys
from flexure_regions import compose_layers, decimal
from moment_diagram import diagram_from_tqs
from positive_flexure import check_positive_flexure


def analyze(detail, tqs, positioned, mapping, raw, api):
    diagram = diagram_from_tqs(mapping,tqs,positioned,raw)
    review = check_positive_flexure(detail,tqs,positioned,mapping,raw,api)
    endings = [b for b in mapping['reinforcement'] if b['mark']=='N3']
    remaining = [b for b in mapping['reinforcement'] if b['mark']=='N5']
    if len(endings)!=1 or len(remaining)!=1:
        raise ValueError('Golden requer marcas documentais N3/N5 únicas.')
    event_x = endings[0]['x_end_common']
    if event_x is None: raise ValueError('Fim N3 desconhecido.')
    local = [r for r in review['regions'] if decimal(r['x_start_m']) < decimal(event_x) <= decimal(r['x_end_m'])]
    if len(local)!=1 or local[0]['blockers'] or not local[0]['concretopy_call']:
        raise ValueError('Configuração transversal/material imediatamente à esquerda do evento não resolvida.')
    if not decimal(remaining[0]['x_start_common']) <= decimal(event_x) <= decimal(remaining[0]['x_end_common']):
        raise ValueError('N5 não está geometricamente presente no evento.')
    composition = compose_layers(remaining)
    if composition['status']!='resolved': raise ValueError('Composição N5 não resolvida.')
    call = copy.deepcopy(local[0]['concretopy_call'])
    call['layers']=[{'numero_barras':c['numero_barras'],'diametro_mm':c['diametro_mm'],'d_cm':None} for c in composition['layers']]
    g=call['geometry']; co=call['coefficients']
    response = api.verificar_flexao_viga_retangular(
        api.SecaoRetangular(g['bw_cm'],g['h_cm'],g['cover_cm'],g['stirrup_diameter_mm']),
        api.Concreto(call['fck_mpa']),api.Aco(call['fyk_mpa'],call['Es_mpa']),
        [api.CamadaArmaduraLongitudinal(c['numero_barras'],api.Barra(c['diametro_mm'])) for c in call['layers']],
        gamma_c=co['gamma_c'],gamma_s=co['gamma_s'],gamma_f=co['gamma_f'],verificar_armadura_minima=False)
    mk=None if response.mk_equivalente_kncm is None else response.mk_equivalente_kncm/100
    query=diagram.moment_at_x(event_x)
    query['reinforcement_event']={'source_type':'reinforcement_event_point','mark':'N3','kind':'geometric_end',
        'x_m':event_x,'source':copy.deepcopy(endings[0]['source']),
        'mapping_provenance':copy.deepcopy(endings[0]['mapping_provenance'])}
    transverse_provenance=copy.deepcopy(local[0]['provenance'])
    for key,target in (('materials','material_interpretation'),('moment_series','source_series'),('concretopy','concretopy_interface')):
        transverse_provenance[key]={'shared_pointer':'/audit_context/'+target}
    result={'model_type':'moment_linear_interpolation_golden','schema_version':'1.0','beam_id':tqs['beam']['id'],
        'diagram':diagram.as_dict(),'reinforcement_event_query':query,'maximum':diagram.positive_maximum(),
        'zero_crossings':diagram.find_crossings(0),
        'remaining_reinforcement_capacity':{'marks':['N5'],'composition':composition,'configuration_side':'left_limit',
            'reference_x_m':event_x,'reference_region_id':local[0]['region_id'],
            'concretopy_call':call,'concretopy_result':asdict(response),
            'MRd_knm':None if response.mrd_kncm is None else response.mrd_kncm/100,'Mk_equivalent_knm':mk,
            'provenance':{'reinforcement':copy.deepcopy(remaining[0]),'transverse_configuration':transverse_provenance,
                          'materials':copy.deepcopy(review['material_interpretation']),
                          'material_parameters':copy.deepcopy(review['material_parameters']),
                          'concretopy_interface':copy.deepcopy(review['concretopy_interface'])},
            'diagnostics':{'model_assumptions_valid':response.hipoteses_validas,'ductility':response.ductilidade_atendida,
                          'minimum_reinforcement':response.armadura_minima_atendida,
                          'anchorage_checked':False,'reinforcement_development_checked':False,'bar_cut_checked':False}},
        'capacity_crossings':None,
        'audit_context':{k:copy.deepcopy(review[k]) for k in ('material_interpretation','source_series','concretopy_interface')},
        'scope':'Propriedades do diagrama adotado e capacidade isolada; sem escolha de corte normativo.'}
    if response.hipoteses_validas and mk is not None and mk>0:
        result['capacity_crossings']=diagram.find_crossings(mk)
    else:
        result['capacity_crossings']={'status':'invalid_capacity','crossings':[]}
    # Auditoria compacta: fontes completas permanecem nos arquivos de entrada.
    result['remaining_reinforcement_capacity']['provenance']['reinforcement']={k:copy.deepcopy(remaining[0][k]) for k in
        ('mark','x_start_cm','x_end_cm','x_start_common','x_end_common','source','mapping_provenance')}
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--concretopy-root',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();root=Path(__file__).resolve().parents[2]
    names=('V1001_beam_model.json','V1001_tqs.json','V1001_tqs_positions.json','V1001_beam_mapping.json','V1001_tqs_raw.json')
    paths=[root/'analises/pranchas'/n for n in names]
    try:
        data=[json.loads(p.read_text(encoding='utf8')) for p in paths]
        if any(args.output.resolve()==p.resolve() for p in paths): raise ValueError('Saída sobre entrada.')
        for entry in data[3]['inputs'].values():
            p=Path(entry['path']);p=p if p.is_absolute() else root/p
            if hashlib.sha256(p.read_bytes()).hexdigest()!=entry['sha256']: raise ValueError('Mapping desatualizado.')
        if hashlib.sha256(paths[-1].read_bytes()).hexdigest()!=data[1]['raw_document']['sha256']:
            raise ValueError('Raw incompatível com consolidado.')
        sys.path.insert(0,str(args.concretopy_root.resolve()));api=importlib.import_module('concretopy')
        if not Path(api.__file__).resolve().is_relative_to(args.concretopy_root.resolve()): raise ValueError('Raiz Concretopy incompatível.')
        out=analyze(*data,api)
        out['inputs']={n:{'path':str(p.resolve()),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for n,p in zip(names,paths)}
        out['implementation']={n:hashlib.sha256(Path(__file__).with_name(n).read_bytes()).hexdigest() for n in
            ('moment_diagram.py','v1001_moment_interpolation.py','tqs_moments.py','positive_flexure.py','flexure_regions.py','materials.py')}
        args.output.write_text(json.dumps(out,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf8')
        print(json.dumps({'query':out['reinforcement_event_query']['value_knm'],'Mk_N5':out['remaining_reinforcement_capacity']['Mk_equivalent_knm'],
                          'crossings':[e.get('x_m') for e in out['capacity_crossings']['crossings']]},ensure_ascii=False))
    except (ValueError,KeyError,TypeError,OSError) as error: parser.error(str(error))


if __name__=='__main__':main()
