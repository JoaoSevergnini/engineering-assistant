"""Interpretação documental de aço; não calcula resistência nem consulta normas."""
import copy

RULE_ID = 'engineer_confirmed_ca50_fyk_500_v1'
RULE = {
    'id': RULE_ID,
    'authority': 'Engenheiro responsável João; confirmação explícita neste fluxo em 04/10/2026',
    'aliases': ['CA50', 'CA-50', 'CA-50A'],
    'normalized_class': 'CA-50',
    'fyk_mpa': 500.0,
    'scope': 'Resistência característica do aço neste fluxo; CA-50A não implica equivalência de outras propriedades.',
}


def interpret_steel(raw):
    """Concilia fyk derivado de todas as fontes operacionais; desconhecido bloqueia."""
    observations, excluded = [], []
    for i, record in enumerate(raw['categorias']['materiais']):
        for j, field in enumerate(record.get('campos_explicitos', [])):
            if field.get('chave') != 'classe_aco':
                continue
            original = field.get('valor')
            recognized = isinstance(original, str) and original.strip() in RULE['aliases']
            item = {'original_text': original,
                    'normalized_class': RULE['normalized_class'] if recognized else None,
                    'derived_fyk_mpa': RULE['fyk_mpa'] if recognized else None,
                    'derivation_rule': RULE_ID if recognized else None,
                    'provenance': {'input': 'tqs_raw',
                                   'json_pointer': f'/categorias/materiais/{i}/campos_explicitos/{j}',
                                   'record': copy.deepcopy(record['origem'])}}
            if record['origem']['arquivo'].upper() == 'RELDTVET.LST':
                item['exclusion_reason'] = 'RELDTVeT excluído pela política operacional confirmada'
                excluded.append(item)
            else:
                observations.append(item)
    unknown = [o for o in observations if o['normalized_class'] is None]
    values = {o['derived_fyk_mpa'] for o in observations}
    status = 'missing' if not observations else 'unrecognized' if unknown else 'conflict' if len(values) != 1 else 'consistent'
    return {'status': status, 'normalized_class': 'CA-50' if status == 'consistent' else None,
            'derived_fyk_mpa': next(iter(values)) if status == 'consistent' else None,
            'unit': 'MPa', 'rule': copy.deepcopy(RULE), 'observations': observations,
            'excluded_observations': excluded}


def documented_fields(raw, key, unit=None):
    found = []
    for i, record in enumerate(raw['categorias']['materiais']):
        if record['origem']['arquivo'].upper() == 'RELDTVET.LST':
            continue
        for j, field in enumerate(record.get('campos_explicitos', [])):
            if field.get('chave') == key and (unit is None or field.get('unidade_original') == unit):
                found.append({'value': field['valor'], 'field': copy.deepcopy(field),
                              'raw_pointer': f'/categorias/materiais/{i}/campos_explicitos/{j}',
                              'record': copy.deepcopy(record['origem'])})
    if not found or len({f['value'] for f in found}) != 1:
        return None, found
    return found[0]['value'], found


