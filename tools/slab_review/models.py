"""Slab-specific references. Geometry and moment payloads remain external."""
from dataclasses import dataclass
from .common import Confirmation, number, text


@dataclass(frozen=True)
class GeometryReference:
    reference: str
    coordinate_system: str
    unit: str

    def __post_init__(self):
        for name in ("reference", "coordinate_system", "unit"):
            text(getattr(self, name), name)


@dataclass(frozen=True)
class ThicknessRegion:
    id: str
    thickness_cm: float | None
    geometry: GeometryReference | None = None
    evidence_ids: tuple[str, ...] = ()

    def __post_init__(self):
        text(self.id, "id")
        number(self.thickness_cm, "thickness_cm", positive=True)


@dataclass(frozen=True)
class Slab:
    id: str
    formwork_document_id: str
    geometry: GeometryReference | None = None
    thickness_cm: float | None = None
    thickness_regions: tuple[ThicknessRegion, ...] = ()
    top_level_m: float | None = None
    evidence_ids: tuple[str, ...] = ()

    def __post_init__(self):
        text(self.id, "id")
        text(self.formwork_document_id, "formwork_document_id")
        number(self.thickness_cm, "thickness_cm", positive=True)
        number(self.top_level_m, "top_level_m")
        if self.thickness_cm is not None and self.thickness_regions:
            raise ValueError("Choose uniform thickness or thickness regions, not both")
        if len({region.id for region in self.thickness_regions}) != len(self.thickness_regions):
            raise ValueError("Duplicate thickness region IDs")


@dataclass(frozen=True)
class ReinforcementOccurrence:
    id: str
    mark: str
    direction: str | None
    diameter_mm: float | None
    spacing_cm: float | None
    document_id: str
    geometry: GeometryReference | None = None
    confirmation: Confirmation = Confirmation.UNCONFIRMED
    slab_id: str | None = None
    evidence_ids: tuple[str, ...] = ()

    def __post_init__(self):
        for name in ("id", "mark", "document_id"):
            text(getattr(self, name), name)
        if self.direction is not None:
            text(self.direction, "direction")
        number(self.diameter_mm, "diameter_mm", positive=True)
        number(self.spacing_cm, "spacing_cm", positive=True)
        if not isinstance(self.confirmation, Confirmation):
            raise ValueError("confirmation must be Confirmation")


@dataclass(frozen=True)
class GridLine:
    # Assigned from source identity or by the engineer, never a list index.
    id: str
    direction: str
    geometry: GeometryReference
    document_id: str
    moment_data_reference: str | None = None
    evidence_ids: tuple[str, ...] = ()

    def __post_init__(self):
        for name in ("id", "direction", "document_id"):
            text(getattr(self, name), name)
