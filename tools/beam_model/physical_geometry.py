"""Optional physical extension to longitudinal_beam_detail; common axis is metres.

No PDF scales, average sections, capacities or combination reconstruction.
"""
from copy import deepcopy
from pathlib import Path
from input_evidence import validate_fact, fact, resolve, PROVED
from documentary_reconciliation import reconcile

GEOMETRY = ('section_shape', 'width_cm', 'height_cm', 'top_level_cm', 'bottom_level_cm', 'lateral_offset_cm', 'cover_cm', 'stirrup_diameter_mm')


def interval(item):
    a = validate_fact(item['x_start_m'], 'm')
    b = validate_fact(item['x_end_m'], 'm')
    import math
    if any(v['value'] is not None and (type(v['value']) not in (int,float) or not math.isfinite(v['value'])) for v in (a,b)):
        raise ValueError('finite_coordinate_required')
    if a['value'] is not None and b['value'] is not None and a['value'] >= b['value']:
        raise ValueError('nonpositive_physical_interval')
    return a, b


def normalize_segment(original):
    s = deepcopy(original)
    if not s.get('id') or not s.get('provenance'):
        raise ValueError('segment_id_and_provenance_required')
    interval(s)
    unit = lambda k: None if k == 'section_shape' else 'mm' if k.endswith('_mm') else 'cm'
    s['geometry'] = {k: validate_fact(s.get('geometry', {}).get(k, fact(unit=unit(k))), unit(k)) for k in GEOMETRY}
    for k in ('width_cm', 'height_cm', 'stirrup_diameter_mm'):
        v = s['geometry'][k]['value']
        if v is not None and (type(v) not in (int, float) or v <= 0):
            raise ValueError('positive_section_dimension_required')
    levels = [s['geometry'][k] for k in ('top_level_cm', 'bottom_level_cm', 'height_cm')]
    if all(v['state'] in PROVED for v in levels) and abs(levels[0]['value'] - levels[1]['value'] - levels[2]['value']) > 1e-8:
        s['geometry']['height_cm'] = fact(state='CONFLICTING', provenance=levels, unit='cm')
    s['geometry_type'] = s.get('geometry_type', 'UNRESOLVED')
    return s


def normalize_occurrence(original):
    b = deepcopy(original)
    if not b.get('occurrence_id') or not b.get('mark') or not b.get('provenance'):
        raise ValueError('physical_occurrence_identity_required')
    interval(b)
    for key, unit in (('quantity', None), ('diameter_mm', 'mm'), ('layers', None)):
        b[key] = validate_fact(b.get(key, fact(unit=unit)), unit)
    n, phi, layers = [b[k]['value'] for k in ('quantity', 'diameter_mm', 'layers')]
    if n is not None and (type(n) is not int or n <= 0):
        raise ValueError('positive_integer_quantity_required')
    if phi is not None and (type(phi) not in (int, float) or phi <= 0):
        raise ValueError('positive_bar_diameter_required')
    if layers is not None:
        if not isinstance(layers, list) or any(type(v) is not int or v < 0 for v in layers) or not sum(layers):
            raise ValueError('invalid_physical_layers')
        if n is not None and sum(layers) != n:
            b['layers'] = fact(state='CONFLICTING', provenance=[b['quantity'], b['layers']])
    b.setdefault('continuity', fact())
    b.setdefault('laps', [])
    b.setdefault('extensions', [])
    b.setdefault('termination', {})
    return b


def classify_span(original):
    """B proves documentary cantilever; side/bounds need separate physical proof."""
    s = deepcopy(original)
    token = str(s.get('tqs_span_token', ''))
    import re
    if token and not re.fullmatch(r'\d+B?', token):
        raise ValueError('invalid_tqs_span_token')
    documentary = 'CANTILEVER' if token.endswith('B') else 'BETWEEN_SUPPORTS' if token else 'UNRESOLVED'
    physical = s.get('physical_kind', fact())
    validate_fact(physical)
    allowed = ('CANTILEVER', 'BETWEEN_SUPPORTS', 'COLUMN_TERMINATION', 'UNRESOLVED')
    if physical['value'] is not None and physical['value'] not in allowed:
        raise ValueError('invalid_physical_span_kind')
    # COLUMN_TERMINATION describes an end condition, not a replacement for a span.
    conflict = physical['state'] == 'CONFLICTING' or (documentary != 'UNRESOLVED' and physical['state'] in PROVED and physical['value'] not in (documentary, 'UNRESOLVED'))
    side = validate_fact(s.get('orientation', fact()))
    if side['value'] is not None and side['value'] not in ('LEFT', 'RIGHT'):
        raise ValueError('invalid_cantilever_orientation')
    bounds = s.get('physical_bounds')
    bounds_proved = bounds is not None and all(v['state'] in PROVED for v in interval(bounds))
    s.update(documentary_kind=documentary, kind='UNRESOLVED' if conflict else documentary if documentary != 'UNRESOLVED' else physical['value'] or 'UNRESOLVED',
             conflicting=conflict, orientation=side,
             physical_validation='CONFLICTING' if conflict else 'VALIDATED' if physical['state'] in PROVED and physical['value'] != 'UNRESOLVED' and bounds_proved and (documentary != 'CANTILEVER' or side['state'] in PROVED) else 'PENDING')
    return s


def extend(model, extension):
    if extension.get('schema_version') != '1.0':
        raise ValueError('physical_extension_version_required')
    if not extension.get('coordinate_system', {}).get('provenance') or extension['coordinate_system'].get('unit') != 'm':
        raise ValueError('common_axis_definition_required')
    out = deepcopy(model)
    segments = [normalize_segment(s) for s in extension.get('segments', [])]
    bars = [normalize_occurrence(b) for b in extension.get('occurrences', [])]
    for items, key in ((segments, 'id'), (bars, 'occurrence_id')):
        ids = [i[key] for i in items]
        if len(set(ids)) != len(ids):
            raise ValueError('duplicate_physical_identity')
    known_marks = {b['mark'] for b in model['longitudinal_reinforcement'] + model['skin_reinforcement']}
    known_marks.update(o['mark'] for o in extension.get('observations', []))
    if any(b['mark'] not in known_marks for b in bars):
        raise ValueError('physical_mark_has_no_documentary_position')
    out['schema_version'] = '1.1'
    out['physical_geometry'] = dict(schema_version='1.0', coordinate_system=deepcopy(extension['coordinate_system']),
                                    segments=segments, occurrences=bars,
                                    spans=[classify_span(s) for s in extension.get('spans', [])],
                                    support_faces=deepcopy(extension.get('support_faces', [])))
    out['documentary_reconciliation'] = reconcile(extension.get('observations', []), extension.get('coverage', []), expected_marks=sorted(known_marks))
    out['input_validation'] = dict(required_before_calculation=True, global_beam_block=False,
                                  envelope_policy='TQS_ENVELOPES', concomitant_combinations_required=False)
    return out


def at_x(model, x_m):
    """Contributions are per occurrence. Unknown ends only affect their possible range."""
    import math
    if type(x_m) not in (int,float) or not math.isfinite(x_m):
        raise ValueError('finite_query_coordinate_required')
    result = dict(present=[], absent=[], indeterminate=[])
    for b in model['physical_geometry']['occurrences']:
        a, z = b['x_start_m'], b['x_end_m']
        # Assumed/graphic endpoints cannot prove an exclusion.
        outside = (a['state'] in PROVED and x_m < a['value']) or (z['state'] in PROVED and x_m > z['value'])
        state = 'absent' if outside else 'present' if a['state'] in PROVED and z['state'] in PROVED else 'indeterminate'
        result[state].append(dict(mark=b['mark'], occurrence_id=b['occurrence_id'], layers=deepcopy(b['layers'])))
    result['complete'] = not result['indeterminate']
    return result


def project_occurrences(model, *, allow_assumptions=False):
    """Adapter to existing flexure_regions. Unique check mark preserves original mark."""
    accepted = PROVED + (('ENGINEERING_ASSUMPTION',) if allow_assumptions else ())
    bars = []
    for b in model['physical_geometry']['occurrences']:
        get = lambda k: deepcopy(b[k]['value']) if b[k]['state'] in accepted else None
        bars.append(dict(mark=b['mark'] + '@' + b['occurrence_id'], documentary_mark=b['mark'], occurrence_id=b['occurrence_id'],
                         bars=get('quantity'), diameter_mm=get('diameter_mm'), layers=get('layers'),
                         x_start_common=get('x_start_m'), x_end_common=get('x_end_m'),
                         function=b.get('function'), face=b.get('face'), source=deepcopy(b['provenance']),
                         physical_evidence=deepcopy(b)))
    return bars


def project_segments(model):
    """Existing transverse region contract; variable profiles are never averaged."""
    regions, pending = [], []
    for s in model['physical_geometry']['segments']:
        a, b = interval(s)
        keys = {'bw_cm': 'width_cm', 'h_cm': 'height_cm', 'cover_cm': 'cover_cm', 'stirrup_diameter_mm': 'stirrup_diameter_mm'}
        if s['geometry_type'] != 'CONSTANT' or any(v['state'] not in PROVED for v in (a, b)):
            pending.append(dict(segment_id=s['id'], reason='unsupported_or_unlocated_geometry'))
            continue
        regions.append(dict(id=s['id'], x_start_common=a['value'], x_end_common=b['value'],
                            **{k: s['geometry'][v]['value'] if s['geometry'][v]['state'] in PROVED else None for k, v in keys.items()},
                            source=deepcopy(s['provenance'])))
    return regions, pending


def apply_end_convention(occurrence, ends):
    """Reuse the established mapping rule, preserving explicit/conventional origin."""
    import sys
    mapping = Path(__file__).resolve().parents[1] / 'beam_mapping'
    if str(mapping) not in sys.path:
        sys.path.insert(0,str(mapping))
    from termination_geometry import interpret_endpoints, RULE
    result = interpret_endpoints(ends)
    out = deepcopy(occurrence)
    for side,item in ({} if 'inconsistent_bar_interval' in result['diagnostics'] else result['resolved']).items():
        explicit = item['method'] == 'EXPLICIT_DIMENSION'
        out['x_start_m' if side=='LEFT' else 'x_end_m'] = fact(item['x_m'], unit='m',
            state='DOCUMENTED_CONFIRMED' if explicit else 'INFERRED_EXPLICIT_CONVENTION',
            provenance=[item['source']],criterion=None if explicit else dict(origin='OFFICE_STANDARD',reference=RULE,version='v1'))
    out['termination_interpretation'] = result
    return out
