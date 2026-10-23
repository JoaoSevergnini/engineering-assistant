"""Local dependency gating and attributed human review, without automatic inference."""
from dataclasses import dataclass, replace
from typing import Mapping
from .common import (
    Criterion, DecisionAction, EngineerDecision, Evidence,
    ExecutionState, TechnicalResult, text,
)


@dataclass(frozen=True)
class Dependency:
    key: str
    description: str

    def __post_init__(self):
        text(self.key, "key")
        text(self.description, "description")


@dataclass(frozen=True)
class Control:
    id: str
    object_id: str
    criterion: Criterion
    dependencies: tuple[Dependency, ...] = ()
    execution: ExecutionState = ExecutionState.NOT_EXECUTED
    result: TechnicalResult = TechnicalResult.NOT_EVALUATED
    evidence_ids: tuple[str, ...] = ()
    pending: tuple[str, ...] = ()
    engineer_notes: tuple[str, ...] = ()
    decisions: tuple[EngineerDecision, ...] = ()

    def __post_init__(self):
        text(self.id, "id")
        text(self.object_id, "object_id")
        allowed = {
            ExecutionState.NOT_EXECUTED: {TechnicalResult.NOT_EVALUATED},
            ExecutionState.PARTIALLY_EXECUTED: {
                TechnicalResult.NOT_EVALUATED, TechnicalResult.INCONCLUSIVE, TechnicalResult.FAIL,
            },
            ExecutionState.EXECUTED_INCONCLUSIVE: {TechnicalResult.INCONCLUSIVE},
            ExecutionState.EXECUTED_COMPLETE: {
                TechnicalResult.PASS, TechnicalResult.FAIL, TechnicalResult.NOT_APPLICABLE,
            },
        }
        if not isinstance(self.execution, ExecutionState) or not isinstance(self.result, TechnicalResult):
            raise ValueError("Use explicit execution/result enums")
        if self.result not in allowed[self.execution]:
            raise ValueError("Inconsistent execution/result pair")
        if len({dep.key for dep in self.dependencies}) != len(self.dependencies):
            raise ValueError("Duplicate dependency keys")
        if self.result in (TechnicalResult.PASS, TechnicalResult.FAIL) and not self.evidence_ids:
            raise ValueError("PASS/FAIL requires evidence")
        if self.result in (TechnicalResult.INCONCLUSIVE, TechnicalResult.NOT_APPLICABLE) and not (
            self.pending or self.engineer_notes
        ):
            raise ValueError("Inconclusive/inapplicable controls require a reason")
        if self.execution == ExecutionState.EXECUTED_COMPLETE and self.pending:
            raise ValueError("Complete controls cannot retain blocking pending items")
        seen = set()
        for decision in self.decisions:
            if decision.target_id != self.id or decision.id in seen:
                raise ValueError("Decision identity mismatch or duplicate")
            if decision.action not in (DecisionAction.ACCEPT, DecisionAction.REJECT):
                raise ValueError("Control decisions accept/reject findings only")
            seen.add(decision.id)


@dataclass(frozen=True)
class DependencyAssessment:
    control_id: str
    missing: tuple[Dependency, ...]

    @property
    def ready(self) -> bool:
        return not self.missing


def assess_dependencies(control: Control, availability: Mapping[str, bool]) -> DependencyAssessment:
    """Unlisted means unavailable. Readiness is supplied, never inferred from values."""
    if any(type(value) is not bool for value in availability.values()):
        raise ValueError("Dependency availability must use explicit booleans")
    return DependencyAssessment(
        control.id, tuple(dep for dep in control.dependencies if not availability.get(dep.key, False))
    )


def record_outcome(
    control: Control, availability: Mapping[str, bool], *,
    execution: ExecutionState, result: TechnicalResult,
    evidence_ids: tuple[str, ...] = (), pending: tuple[str, ...] = (),
    engineer_notes: tuple[str, ...] = (),
) -> Control:
    """Record caller-supplied review, not a structural calculation.

    A partial, evidenced FAIL may survive unresolved dependencies. A complete
    PASS/FAIL requires all declared inputs; NOT_APPLICABLE needs its own reason.
    Returns a new record; retain the previous record if outcome history is needed.
    """
    assessment = assess_dependencies(control, availability)
    if execution == ExecutionState.EXECUTED_COMPLETE and result != TechnicalResult.NOT_APPLICABLE:
        if not assessment.ready:
            raise ValueError("Cannot conclude with missing dependencies: " + ", ".join(d.key for d in assessment.missing))
    return replace(
        control, execution=execution, result=result, evidence_ids=evidence_ids,
        pending=pending, engineer_notes=engineer_notes,
    )


def review_evidence(evidence: Evidence, decision: EngineerDecision) -> Evidence:
    """Append confirmation/correction; original observed/interpreted fields never change."""
    return replace(evidence, decisions=evidence.decisions + (decision,))


def review_finding(control: Control, decision: EngineerDecision) -> Control:
    """Accept/reject an ATP finding without rewriting the technical result."""
    return replace(control, decisions=control.decisions + (decision,))
