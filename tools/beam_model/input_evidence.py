"""Evidence contract for documentary/physical inputs; no structural equations."""
from copy import deepcopy
import math

STATES = ('DOCUMENTED_CONFIRMED', 'INFERRED_EXPLICIT_CONVENTION', 'ENGINEERING_ASSUMPTION', 'CONFLICTING', 'MISSING', 'NOT_APPLICABLE')
ORIGINS = ('NORMATIVE', 'OFFICE_STANDARD', 'ENGINEERING_ASSUMPTION', 'SOFTWARE_CRITERION', 'OUT_OF_SCOPE')
PROVED = STATES[:2]


def fact(value=None, *, state='MISSING', provenance=None, criterion=None, unit=None):
    if state not in STATES:
        raise ValueError('invalid_evidence_state')
    if state in PROVED and (value is None or not provenance):
        raise ValueError('proved_value_requires_provenance')
    if state == 'INFERRED_EXPLICIT_CONVENTION' and not criterion:
        raise ValueError('convention_requires_criterion')
    if state in ('CONFLICTING', 'MISSING', 'NOT_APPLICABLE') and value is not None:
        raise ValueError('unresolved_value_must_be_null')
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError('nonfinite_value')
    if criterion:
        if criterion.get('origin') not in ORIGINS or not criterion.get('reference'):
            raise ValueError('criterion_origin_and_reference_required')
        if criterion['origin'] == 'NORMATIVE' and not criterion.get('consulted'):
            raise ValueError('normative_text_not_consulted')
    return dict(value=deepcopy(value), state=state, unit=unit,
                provenance=deepcopy(provenance or []), criterion=deepcopy(criterion))


def validate_fact(item, unit=None):
    result = fact(**item)
    if unit and result['unit'] != unit:
        raise ValueError('physical_unit_required:' + unit)
    return result


def resolve(observations, *, unit=None):
    """Dimensioned/structured proof precedes graphic estimates, never another proof.

    Different proved values are conflicts. Estimates are retained in provenance.
    """
    items = [validate_fact(o, unit) for o in observations]
    candidates = [o for o in items if o['state'] in PROVED]
    if any(o['state'] == 'CONFLICTING' for o in items):
        return fact(state='CONFLICTING', provenance=items, unit=unit)
    if candidates:
        values = [o['value'] for o in candidates]
        if any(v != values[0] for v in values[1:]):
            return fact(state='CONFLICTING', provenance=items, unit=unit)
        state = 'DOCUMENTED_CONFIRMED' if any(o['state'] == 'DOCUMENTED_CONFIRMED' for o in candidates) else 'INFERRED_EXPLICIT_CONVENTION'
        criterion = next((o['criterion'] for o in candidates if o['criterion']), None)
        return fact(values[0], state=state, provenance=items, criterion=criterion, unit=unit)
    estimates = [o for o in items if o['state'] == 'ENGINEERING_ASSUMPTION']
    if estimates and all(o['value'] == estimates[0]['value'] for o in estimates):
        return fact(estimates[0]['value'], state='ENGINEERING_ASSUMPTION', provenance=items, unit=unit)
    return fact(state='CONFLICTING' if estimates else 'MISSING', provenance=items, unit=unit)
