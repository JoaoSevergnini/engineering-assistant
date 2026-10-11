"""Register existing per-span TQS positions onto physical_geometry's common axis.

This is a coordinate adapter, not another longitudinal model or force envelope.
"""
from copy import deepcopy
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'beam_model'))
from input_evidence import validate_fact


def register_span(span, registration, coordinate_system):
    if registration.get('span_id') != span['id'] or registration.get('coordinate_system') != coordinate_system:
        raise ValueError('span_common_axis_identity_mismatch')
    anchors = registration.get('anchors', [])
    if len(anchors) != 2:
        raise ValueError('two_proved_coordinate_anchors_required')
    points = []
    for anchor in anchors:
        values = [validate_fact(anchor[k], 'm') for k in ('local_m', 'common_m')]
        if any(v['state'] != 'DOCUMENTED_CONFIRMED' or type(v['value']) not in (int, float) or not math.isfinite(v['value']) for v in values):
            raise ValueError('force_registration_requires_documentary_proof')
        points.append([v['value'] for v in values])
    (l1, c1), (l2, c2) = points
    if l1 == l2 or not math.isclose(c2-c1, l2-l1, abs_tol=1e-8, rel_tol=0):
        # Reversed force orientation needs force-sign interpretation; not silently enabled.
        raise ValueError('registration_requires_same_orientation_and_metre_scale')
    out = deepcopy(span)
    for series in out['internal_forces']:
        positions = series.get('positions')
        if not positions or len(positions) != len(series['values']) or series.get('unit') is None:
            raise ValueError('existing_positioned_force_series_required')
        if any(type(x) not in (int,float) or not math.isfinite(x) for x in positions) or any(b <= a for a,b in zip(positions,positions[1:])):
            raise ValueError('invalid_local_force_positions')
        if min(positions) < min(l1,l2)-1e-8 or max(positions) > max(l1,l2)+1e-8:
            raise ValueError('registration_does_not_cover_force_domain')
        series['local_positions'] = list(positions)
        series['positions'] = [x + c1-l1 for x in positions]
        series['mapping_provenance'] = deepcopy(registration)
    return out
