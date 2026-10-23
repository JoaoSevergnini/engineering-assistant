"""Small documentary contracts; independent of structural element and third-party packages."""
from dataclasses import asdict, dataclass, is_dataclass
from datetime import datetime
from enum import Enum
from math import isfinite
import re

Value = str | int | float | bool | None


def text(value: str, name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be nonempty text")


def number(value: float | None, name: str, *, positive: bool = False) -> None:
    if value is not None and (
        isinstance(value, bool) or not isinstance(value, (int, float))
        or not isfinite(value) or (positive and value <= 0)
    ):
        raise ValueError(f"{name} must be finite" + (" and positive" if positive else ""))


def scalar(value: Value) -> None:
    if value is not None and not isinstance(value, (str, int, float, bool)):
        raise ValueError("Observation values must be scalar; use a geometry reference for shapes")
    if isinstance(value, float) and not isfinite(value):
        raise ValueError("Observation values must be finite")


class Confirmation(str, Enum):
    UNCONFIRMED = "UNCONFIRMED"
    CONFIRMED = "CONFIRMED"
    INCONCLUSIVE = "INCONCLUSIVE"


class DecisionAction(str, Enum):
    CONFIRM = "CONFIRM"
    CORRECT = "CORRECT"
    PROVIDE = "PROVIDE"
    ACCEPT = "ACCEPT"
    REJECT = "REJECT"


class CriterionOrigin(str, Enum):
    NORMATIVE = "NORMATIVE"
    PROJECT_REQUIREMENT = "PROJECT_REQUIREMENT"
    SOFTWARE_CRITERION = "SOFTWARE_CRITERION"
    OFFICE_STANDARD = "OFFICE_STANDARD"
    ENGINEERING_ASSUMPTION = "ENGINEERING_ASSUMPTION"


class TechnicalResult(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    INCONCLUSIVE = "INCONCLUSIVE"
    NOT_EVALUATED = "NOT_EVALUATED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class ExecutionState(str, Enum):
    NOT_EXECUTED = "NOT_EXECUTED"
    PARTIALLY_EXECUTED = "PARTIALLY_EXECUTED"
    EXECUTED_INCONCLUSIVE = "EXECUTED_INCONCLUSIVE"
    EXECUTED_COMPLETE = "EXECUTED_COMPLETE"


@dataclass(frozen=True)
class Document:
    id: str
    path: str
    document_type: str
    revision: str | None = None
    sha256: str | None = None

    def __post_init__(self):
        for name in ("id", "path", "document_type"):
            text(getattr(self, name), name)
        if self.sha256 is not None and not re.fullmatch(r"[a-fA-F0-9]{64}", self.sha256):
            raise ValueError("sha256 must contain 64 hexadecimal characters")


@dataclass(frozen=True)
class EngineerDecision:
    id: str
    target_id: str
    action: DecisionAction
    author: str
    recorded_at: str
    justification: str
    value: Value = None
    evidence_ids: tuple[str, ...] = ()

    def __post_init__(self):
        for name in ("id", "target_id", "author", "justification"):
            text(getattr(self, name), name)
        if not isinstance(self.action, DecisionAction):
            raise ValueError("action must be DecisionAction")
        instant = datetime.fromisoformat(self.recorded_at.replace("Z", "+00:00"))
        if instant.utcoffset() is None:
            raise ValueError("recorded_at requires a timezone")
        scalar(self.value)
        if self.action in (DecisionAction.CORRECT, DecisionAction.PROVIDE):
            if self.value is None:
                raise ValueError("CORRECT/PROVIDE requires a value")
        elif self.value is not None:
            raise ValueError("Only CORRECT/PROVIDE carries a replacement value")


@dataclass(frozen=True)
class Evidence:
    id: str
    document_id: str | None
    observed: Value
    method: str
    interpreted: Value = None
    page: int | None = None
    location: str | None = None
    unit: str | None = None
    confirmation: Confirmation = Confirmation.UNCONFIRMED
    decisions: tuple[EngineerDecision, ...] = ()

    def __post_init__(self):
        text(self.id, "id")
        text(self.method, "method")
        if self.document_id is not None:
            text(self.document_id, "document_id")
        if self.page is not None and (type(self.page) is not int or self.page < 1):
            raise ValueError("page must be a positive 1-based integer")
        if not isinstance(self.confirmation, Confirmation):
            raise ValueError("confirmation must be Confirmation")
        scalar(self.observed)
        scalar(self.interpreted)
        ids = set()
        current = self.interpreted if self.interpreted is not None else self.observed
        for decision in self.decisions:
            if decision.target_id != self.id or decision.id in ids:
                raise ValueError("Decision identity mismatch or duplicate")
            ids.add(decision.id)
            if decision.action not in (DecisionAction.CONFIRM, DecisionAction.CORRECT, DecisionAction.PROVIDE):
                raise ValueError("Evidence accepts CONFIRM/CORRECT/PROVIDE only")
            if decision.action == DecisionAction.PROVIDE and current is not None:
                raise ValueError("PROVIDE is only for missing data; use CORRECT")
            if decision.action == DecisionAction.CORRECT and current is None:
                raise ValueError("CORRECT requires a prior value; use PROVIDE")
            if decision.action == DecisionAction.CONFIRM and current is None:
                raise ValueError("Cannot confirm an absent value")
            if decision.action in (DecisionAction.CORRECT, DecisionAction.PROVIDE):
                current = decision.value
        if self.document_id is None and not self.decisions:
            raise ValueError("A source document or an attributed human decision is required")
        if self.confirmation == Confirmation.CONFIRMED and current is None:
            raise ValueError("Confirmed evidence requires a value")

    @property
    def effective_value(self) -> Value:
        value = self.interpreted if self.interpreted is not None else self.observed
        for decision in self.decisions:
            if decision.action in (DecisionAction.CORRECT, DecisionAction.PROVIDE):
                value = decision.value
        return value

    @property
    def effective_confirmation(self) -> Confirmation:
        return Confirmation.CONFIRMED if self.decisions else self.confirmation


@dataclass(frozen=True)
class Criterion:
    id: str
    description: str
    origin: CriterionOrigin
    reference: str | None = None
    edition: str | None = None
    source_consulted: bool = False

    def __post_init__(self):
        text(self.id, "id")
        text(self.description, "description")
        if not isinstance(self.origin, CriterionOrigin):
            raise ValueError("origin must be CriterionOrigin")


def to_data(value):
    """JSON-compatible projection. No IO; original and human decisions are retained."""
    if is_dataclass(value):
        return to_data(asdict(value))
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, dict):
        return {key: to_data(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [to_data(item) for item in value]
    return value
