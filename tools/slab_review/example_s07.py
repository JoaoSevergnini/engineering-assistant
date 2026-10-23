"""Standalone illustrative S07 scenario. Reads no PDF/DXF; writes only stdout."""
from dataclasses import replace
import json
from .common import (
    Confirmation, Criterion, CriterionOrigin, DecisionAction, Document,
    EngineerDecision, Evidence, ExecutionState, TechnicalResult, to_data,
)
from .models import GeometryReference, GridLine, ReinforcementOccurrence, Slab
from .review import (
    Control, Dependency, assess_dependencies, record_outcome,
    review_evidence, review_finding,
)


def build_example():
    form = Document(
        "S07-FORMA-7202", "WPBR-EST-EX-7202-PLN-MU2-S07-TE-R03.PDF",
        "FORMWORK", revision="R03",
    )
    drawing = Document(
        "S07-ARM-7308", "WPBR-EST-EX-7308-PLN-MU2-S07-TE-R00.PDF",
        "REINFORCEMENT", revision="R00",
    )
    dxf = Document("S07-DXF-V", "ARPV0002.DXF", "MOMENT_DIAGRAM")
    # No real slab assignment, thickness, contour, or grid identity is asserted.
    slab = Slab("DEMO-S07-LAJE", form.id)
    diameter = Evidence(
        "DEMO-DIAMETER", drawing.id, "38 Ø12.5 c/11 C=618",
        "SIMULATED_AMBIGUOUS_EXTRACTION", interpreted=12.0,
        page=1, location="PC51C / N26; cenário ilustrativo", unit="mm",
        confirmation=Confirmation.INCONCLUSIVE,
    )
    spacing = Evidence(
        "DEMO-SPACING", drawing.id, None, "SIMULATED_MISSING_EXTRACTION",
        page=1, location="PC51C / N26", unit="cm",
        confirmation=Confirmation.INCONCLUSIVE,
    )
    occurrence_before = ReinforcementOccurrence(
        "DEMO-S07-N26", "N26", "V", diameter.effective_value, None, drawing.id,
        confirmation=Confirmation.INCONCLUSIVE,
        evidence_ids=(diameter.id, spacing.id),
    )
    actor = "Engenheiro fictício (demonstração; não é confirmação de João)"
    corrected = review_evidence(diameter, EngineerDecision(
        "DEMO-DEC-1", diameter.id, DecisionAction.CORRECT, actor,
        "2026-10-23T12:00:00-03:00",
        "Simula correção da interpretação; não representa nova conferência do PDF.",
        value=12.5,
    ))
    supplied = review_evidence(spacing, EngineerDecision(
        "DEMO-DEC-2", spacing.id, DecisionAction.PROVIDE, actor,
        "2026-10-23T12:01:00-03:00",
        "Simula informação manual do espaçamento a partir da chamada representativa.",
        value=11.0,
    ))
    # Explicit projection; evidence history is the authoritative provenance.
    occurrence_after = replace(
        occurrence_before, diameter_mm=corrected.effective_value,
        spacing_cm=supplied.effective_value, confirmation=Confirmation.CONFIRMED,
    )
    grid = GridLine(
        "DEMO-GRID-V-A", "V",
        GeometryReference("DEMO:linha-ainda-sem-geometria-real", "DXF_LOCAL_DEMO", "DXF_UNIT_UNKNOWN"),
        dxf.id,
    )
    criteria = {
        "diameter": Criterion(
            "DEMO-CALL", "Conferir apenas a bitola representativa de 12.5 mm.",
            CriterionOrigin.ENGINEERING_ASSUMPTION,
            reference="Cenário demonstrativo; sem julgamento estrutural",
        ),
        "coverage": Criterion(
            "DEMO-COVERAGE", "Cobertura integral positiva exige contorno conhecido.",
            CriterionOrigin.OFFICE_STANDARD, reference="Escopo futuro; não executado",
        ),
        "flexure": Criterion(
            "DEMO-FLEXURE", "Comparar solicitação e resistência com entradas comprovadas.",
            CriterionOrigin.ENGINEERING_ASSUMPTION, reference="Escopo futuro; não executado",
        ),
    }
    diameter_control = Control(
        "DEMO-CONTROL-DIA", occurrence_after.id, criteria["diameter"],
        dependencies=(Dependency("diameter.confirmed", "Bitola confirmada para o controle local"),),
    )
    coverage_control = Control(
        "DEMO-CONTROL-COVERAGE", slab.id, criteria["coverage"],
        dependencies=(Dependency("slab.contour", "Contorno estrutural conciliado"),),
        pending=("Contorno não definido nesta demonstração; não indica ausência de aço.",),
    )
    flexure_control = Control(
        "DEMO-CONTROL-FLEXURE", occurrence_after.id, criteria["flexure"],
        dependencies=(
            Dependency("slab.thickness", "Espessura local confirmada"),
            Dependency("moment.diagram", "Diagrama e natureza comprovados"),
        ),
        pending=("Sem espessura e diagrama; resistência não calculada.",),
    )
    availability = {
        "diameter.confirmed": corrected.effective_confirmation == Confirmation.CONFIRMED,
        "slab.contour": False, "slab.thickness": False, "moment.diagram": False,
    }
    completed = record_outcome(
        diameter_control, availability, execution=ExecutionState.EXECUTED_COMPLETE,
        result=TechnicalResult.PASS if occurrence_after.diameter_mm == 12.5 else TechnicalResult.FAIL,
        evidence_ids=(corrected.id,),
        engineer_notes=("Confronto demonstrativo de bitola; não verifica capacidade ou mínimo.",),
    )
    # Rejecting a proposed finding does not turn an unexecuted control into PASS.
    reviewed_coverage = review_finding(coverage_control, EngineerDecision(
        "DEMO-DEC-3", coverage_control.id, DecisionAction.REJECT, actor,
        "2026-10-23T12:02:00-03:00",
        "Rejeitar alegação de ausência de armadura: o contorno não foi examinado.",
    ))
    controls = (completed, reviewed_coverage, flexure_control)
    return {
        "schema_version": "slab-review-1A",
        "demonstration_only": True,
        "notice": (
            "Dados representativos da chamada N26/7308 e nomes documentais S07. "
            "Interpretação inicial e decisões humanas são simuladas. "
            "Nenhum resultado histórico foi validado e nenhuma ATP foi executada."
        ),
        "historical_reference": (
            "analises/atp_s07_lajes_terreo/dxf_momentos_verticais/"
            "7308_conferencia_cobertura.json"
        ),
        "documents": (form, drawing, dxf), "slabs": (slab,),
        "evidence_before": (diameter, spacing),
        "evidence_after": (corrected, supplied),
        "occurrence_before": occurrence_before, "occurrence_after": occurrence_after,
        "grid_lines": (grid,), "controls": controls,
        "dependency_assessments": tuple(assess_dependencies(c, availability) for c in controls),
    }


def main():
    print(json.dumps(to_data(build_example()), ensure_ascii=False, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
