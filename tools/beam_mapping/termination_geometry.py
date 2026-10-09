"""Sourced interpretation of undimensioned longitudinal endpoints, not anchorage."""
from copy import deepcopy
from math import isfinite
RULE='engineer_confirmed_undimensioned_bar_end_external_column_face_v1'


def interpret_endpoints(ends):
    """LEFT/RIGHT are physical ends. Explicit dimensions outrank graphics.

    Caller proves terminates_in_support, support_type/element and physical face.
    Both ends in supports without either explicit endpoint remain inconclusive.
    Graphic positions are retained for audit and never used as lengths.
    """
    out={'rule':RULE,'ends':deepcopy(ends),'resolved':{},'diagnostics':[],
         'bend_geometry_inferred':False,'anchorage_length_inferred':False}
    both=all(ends.get(side,{}).get('terminates_in_support') is True for side in ('LEFT','RIGHT'))
    explicit=lambda e:e.get('explicit_x_m') is not None and bool(e.get('explicit_dimension_source'))
    if both and not any(explicit(e) for e in ends.values()):
        out['diagnostics'].append('both_support_ends_undimensioned')
        out['status']='INCONCLUSIVE';return out
    for side,e in ends.items():
        if side not in ('LEFT','RIGHT'):raise ValueError('unknown_physical_bar_end')
        if explicit(e):
            value=e['explicit_x_m'];source=e['explicit_dimension_source'];method='EXPLICIT_DIMENSION'
        elif e.get('explicit_x_m') is not None:
            out['diagnostics'].append(side+':explicit_dimension_source_missing');continue
        elif (e.get('terminates_in_support') is True and e.get('support_type')=='END'
              and e.get('support_element')=='COLUMN' and e.get('source')):
            value=e.get('external_face_m');source=e['source'];method='EXTERNAL_COLUMN_FACE_CONVENTION'
        else:
            out['diagnostics'].append(side+':endpoint_geometry_unresolved');continue
        if type(value) not in (int,float) or not isfinite(value):
            out['diagnostics'].append(side+':physical_coordinate_unresolved');continue
        out['resolved'][side]={'x_m':value,'source':source,'method':method,'rule':RULE if method!='EXPLICIT_DIMENSION' else None}
    if set(out['resolved'])=={'LEFT','RIGHT'} and out['resolved']['LEFT']['x_m']>=out['resolved']['RIGHT']['x_m']:
        out['diagnostics'].append('inconsistent_bar_interval')
    out['status']='PASS' if not out['diagnostics'] else 'INCONCLUSIVE'
    return out
