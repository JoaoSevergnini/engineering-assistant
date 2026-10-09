"""Common oriented support geometry. Coordinates m, lengths cm, no mechanics."""
from dataclasses import dataclass
from moment_diagram import dec

ORIENTATION_RULE = 'engineer_confirmed_support_side_orientation_v1'


def normalize_side(value):
    if not isinstance(value, str) or value.upper() not in ('LEFT', 'RIGHT'):
        raise ValueError('invalid_support_side')
    return value.upper()


def normalize_type(value):
    mapping = {'END': 'END', 'EXTREMO': 'END', 'INTERMEDIATE': 'INTERMEDIATE', 'INTERMEDIARIO': 'INTERMEDIATE'}
    if not isinstance(value, str) or value.upper() not in mapping:
        raise ValueError('invalid_support_type')
    return mapping[value.upper()]


class OrientedAxis:
    """Shared longitudinal direction, also usable for a cut inside a span."""
    @property
    def direction_into_support(self):
        return -1 if self.support_side == 'LEFT' else 1

    @property
    def direction_into_span(self):
        return -self.direction_into_support

    @property
    def bar_endpoint_key(self):
        return 'x_start_common' if self.support_side == 'LEFT' else 'x_end_common'

    def distance_cm(self, reference_m, endpoint_m):
        return float(self.direction_into_support * (dec(endpoint_m) - dec(reference_m)) * 100)

    def required_end(self, reference_m, length_cm):
        if dec(length_cm) < 0:
            raise ValueError('negative_required_length')
        return float(dec(reference_m) + self.direction_into_support * dec(length_cm) / 100)



@dataclass(frozen=True)
class LongitudinalOrientation(OrientedAxis):
    support_side: str
    provenance: dict

    def __post_init__(self):
        object.__setattr__(self,"support_side",normalize_side(self.support_side))
        if not self.provenance: raise ValueError("orientation_provenance_missing")

    def as_dict(self):
        return {"side":self.support_side,"direction":self.direction_into_support,
                "rule":ORIENTATION_RULE,"provenance":self.provenance}


@dataclass(frozen=True)
class SupportGeometry(OrientedAxis):
    span_id: object
    support_id: str
    support_side: str
    support_type: str
    internal_face_m: float
    external_face_m: float
    support_axis_m: float
    support_width_cm: float
    provenance: dict

    def __post_init__(self):
        object.__setattr__(self, 'support_side', normalize_side(self.support_side))
        object.__setattr__(self, 'support_type', normalize_type(self.support_type))
        if self.span_id is None or not self.support_id or not self.provenance:
            raise ValueError('support_identity_or_geometry_provenance_missing')
        width = self.distance_cm(self.internal_face_m, self.external_face_m)
        if width <= 0 or dec(width) != dec(self.support_width_cm):
            raise ValueError('inconsistent_support_faces_or_width')
        axis = self.distance_cm(self.internal_face_m, self.support_axis_m)
        if not 0 <= axis <= width:
            raise ValueError('support_axis_outside_support')

    def penetration(self, bar):
        start, end = dec(bar['x_start_common']), dec(bar['x_end_common'])
        if start >= end:
            raise ValueError('invalid_longitudinal_interval')
        face = dec(self.internal_face_m)
        end_x = bar[self.bar_endpoint_key]
        inward_x = bar['x_end_common' if self.support_side == 'LEFT' else 'x_start_common']
        from_span = self.distance_cm(face, inward_x) < 0
        present = start <= face <= end and from_span
        penetration = max(0.0, self.distance_cm(face, end_x)) if present else 0.0
        through = present and penetration > self.support_width_cm
        return {'cruza_face_interna': present and penetration > 0, 'reaches_from_span': from_span,
            'penetra_apoio': present and penetration > 0,
            'area_presente_na_face': present, 'documentary_end_x_m': end_x,
            'comprimento_penetracao_cm': penetration,
            'length_inside_physical_support_cm': min(penetration, self.support_width_cm),
            'continuity': 'CONTINUES_THROUGH_SUPPORT' if through else 'TERMINATES_IN_SUPPORT' if present else 'UNKNOWN',
            'provenance': {'rule': ORIENTATION_RULE, 'geometry': self.provenance,
                'bar_source': bar.get('source'), 'interval_m': [float(start), float(end)]}}

    def as_dict(self):
        return {'span_id': self.span_id, 'support_id': self.support_id,
            'support_side': self.support_side, 'support_type': self.support_type,
            'internal_face_m': self.internal_face_m, 'external_face_m': self.external_face_m,
            'support_axis_m': self.support_axis_m, 'support_width_cm': self.support_width_cm,
            'direction_into_support': self.direction_into_support,
            'direction_into_span': self.direction_into_span,
            'rule': ORIENTATION_RULE, 'provenance': self.provenance}
