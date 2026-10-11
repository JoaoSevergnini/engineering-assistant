"""Interpret declared form observations on the existing physical common axis.

PDF zones are reviewed by a person/agent; text extraction is not geometry proof.
No coordinates are obtained from stirrup distribution or graphical scale.
"""
from copy import deepcopy
from input_evidence import fact, validate_fact, resolve
from physical_geometry import normalize_segment, classify_span

DOCUMENTARY_STATES = ('PROVED', 'ABSENT_IN_DRAWING', 'PRESENT_NOT_EXTRACTED', 'CONFLICTING', 'NOT_EXAMINED')
FORM_FIELDS = ('section_shape', 'width_cm', 'height_cm', 'top_level_cm', 'bottom_level_cm', 'lateral_offset_cm')


def interpret_observation(item, *, unit=None):
    state = item.get('documentary_state', 'NOT_EXAMINED')
    if state not in DOCUMENTARY_STATES:
        raise ValueError('unknown_form_documentary_state')
    review = item.get('review', {})
    if state == 'ABSENT_IN_DRAWING' and not (review.get('relevant_region_examined') is True and
            review.get('provenance') and review.get('scope')):
        raise ValueError('documentary_absence_requires_examined_region')
    if state == 'PROVED':
        value = validate_fact(item['fact'], unit)
        if value['state'] != 'DOCUMENTED_CONFIRMED':
            raise ValueError('form_proof_must_be_documented')
    else:
        value = fact(state='CONFLICTING' if state == 'CONFLICTING' else 'MISSING', unit=unit,
                     provenance=item.get('provenance', []) + [dict(documentary_state=state, review=review)])
    return value, dict(documentary_state=state, review=deepcopy(review),
                       clarification=item.get('clarification', 'Examinar/cotar a informação na região relevante da planta de formas.'))


def apply_form(model, form):
    """Form is primary; LST/detail comparison may create conflicts, never fill gaps."""
    out = deepcopy(model)
    if form.get('coordinate_system') != model['physical_geometry']['coordinate_system']:
        raise ValueError('form_common_axis_registration_required')
    diagnostics, segments = [], []
    supplied = {s['id']: s for s in form.get('segments', [])}
    if len(supplied) != len(form.get('segments', [])):
        raise ValueError('duplicate_form_segment')
    completeness = validate_fact(form.get('segment_inventory_complete', fact()))
    if not (completeness['state']=='DOCUMENTED_CONFIRMED' and completeness['value'] is True):
        for old in model['physical_geometry']['segments']:
            supplied.setdefault(old['id'], dict(id=old['id']))
    old_by_id = {s['id']: s for s in model['physical_geometry']['segments']}
    for sid, source in supplied.items():
        previous = old_by_id.get(sid, {})
        segment = dict(id=sid, provenance=deepcopy(form['provenance']),
                       geometry_type=source.get('geometry_type', 'UNRESOLVED'), geometry={})
        for field in ('x_start_m', 'x_end_m') + FORM_FIELDS:
            unit = 'm' if field.startswith('x_') else None if field == 'section_shape' else 'cm'
            value, note = interpret_observation(source.get('fields', {}).get(field, {}), unit=unit)
            # Explicit comparisons only: old estimates must not invalidate new proof.
            comparisons = source.get('comparisons', {}).get(field, [])
            if comparisons and value['state'] == 'DOCUMENTED_CONFIRMED':
                value = resolve([value] + comparisons, unit=unit)
                if value['state'] == 'CONFLICTING':
                    note['documentary_state'] = 'CONFLICTING'
            if field.startswith('x_'):
                segment[field] = value
            else:
                segment['geometry'][field] = value
            diagnostics.append(dict(segment_id=sid, field=field, **note, evidence=deepcopy(value)))
        # Cover and stirrup diameter come from their own project/detail sources.
        for field, unit in (('cover_cm', 'cm'), ('stirrup_diameter_mm', 'mm')):
            segment['geometry'][field] = validate_fact(source.get('detail_geometry', {}).get(field,
                previous.get('geometry', {}).get(field, fact(unit=unit))), unit)
        segments.append(normalize_segment(segment))
    out['physical_geometry']['segments'] = segments
    out['physical_geometry']['support_faces'] = deepcopy(form.get('support_faces', []))
    if 'spans' in form:
        spans={str(s['id']):s for s in model['physical_geometry'].get('spans', [])}
        for s in form['spans']:
            spans[str(s['id'])]=s
        out['physical_geometry']['spans'] = [classify_span(s) for s in spans.values()]
    out['form_interpretation'] = dict(provenance=deepcopy(form['provenance']), fields=diagnostics,
        pending=[d for d in diagnostics if d['documentary_state'] != 'PROVED'],
        transitions=deepcopy(form.get('transitions', [])), segment_inventory_complete=completeness,
        source_priority='FORM_THEN_EXPLICIT_LST_COMPARISON')
    return out
