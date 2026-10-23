"""Contract behavior tests. No PDFs, DXFs, Concretopy or historical computations."""
from dataclasses import FrozenInstanceError, replace
import json
import unittest
from tools.slab_review.common import (
    Confirmation, Criterion, CriterionOrigin, DecisionAction, Document,
    EngineerDecision, Evidence, ExecutionState as X, TechnicalResult as R, to_data,
)
from tools.slab_review.models import (
    GeometryReference, GridLine, ReinforcementOccurrence, Slab, ThicknessRegion,
)
from tools.slab_review.review import (
    Control, Dependency, assess_dependencies, record_outcome,
    review_evidence, review_finding,
)
from tools.slab_review.example_s07 import build_example


def decision(target, action, value=None, id="decision-1"):
    return EngineerDecision(
        id, target, action, "Engenheiro de teste", "2026-10-23T12:00:00-03:00",
        "Justificativa de teste", value=value,
    )


def criterion(origin=CriterionOrigin.OFFICE_STANDARD):
    return Criterion("criterion", "Critério local explícito", origin)


class DocumentaryTests(unittest.TestCase):
    def test_optional_revision_hash_and_nonexistent_path_are_allowed(self):
        doc = Document("doc", "not-opened.pdf", "FORMWORK")
        self.assertIsNone(doc.revision)
        self.assertIsNone(doc.sha256)
        with self.assertRaises(ValueError):
            replace(doc, sha256="invalid")
        self.assertEqual(replace(doc, sha256="a" * 64).sha256, "a" * 64)

    def test_original_and_previous_corrections_are_preserved(self):
        original = Evidence("e", "doc", "Ø12.5", "EXTRACTION", interpreted=12.0, unit="mm")
        corrected = review_evidence(original, decision("e", DecisionAction.CORRECT, 12.5))
        confirmed = review_evidence(corrected, decision("e", DecisionAction.CONFIRM, id="decision-2"))
        self.assertEqual((original.observed, original.interpreted, original.decisions), ("Ø12.5", 12.0, ()))
        self.assertEqual((confirmed.observed, confirmed.interpreted), ("Ø12.5", 12.0))
        self.assertEqual(confirmed.effective_value, 12.5)
        self.assertEqual(confirmed.effective_confirmation, Confirmation.CONFIRMED)
        self.assertEqual(len(confirmed.decisions), 2)
        with self.assertRaises(FrozenInstanceError):
            original.interpreted = 13

    def test_manual_data_without_document_requires_attributed_decision(self):
        manual = Evidence(
            "manual", None, None, "ENGINEER_MANUAL", unit="cm",
            decisions=(decision("manual", DecisionAction.PROVIDE, 11),),
        )
        self.assertIsNone(manual.observed)
        self.assertEqual(manual.effective_value, 11)
        with self.assertRaises(ValueError):
            Evidence("manual", None, 11, "ENGINEER_MANUAL")

    def test_confirm_does_not_invent_value_and_zero_is_not_missing(self):
        absent = Evidence("e", "doc", None, "EXTRACTION", confirmation=Confirmation.INCONCLUSIVE)
        with self.assertRaises(ValueError):
            review_evidence(absent, decision("e", DecisionAction.CONFIRM))
        provided = review_evidence(absent, decision("e", DecisionAction.PROVIDE, 0))
        self.assertEqual(provided.effective_value, 0)
        with self.assertRaises(ValueError):
            review_evidence(provided, decision("e", DecisionAction.PROVIDE, 2, id="d2"))
        zero = Evidence("zero", "doc", 0, "READING", interpreted=False)
        self.assertIs(zero.effective_value, False)

    def test_decision_identity_action_author_reason_timestamp(self):
        evidence = Evidence("e", "doc", 8, "READING")
        invalid = (
            decision("other", DecisionAction.CONFIRM),
            decision("e", DecisionAction.ACCEPT),
        )
        for item in invalid:
            with self.subTest(item=item), self.assertRaises(ValueError):
                review_evidence(evidence, item)
        confirmed = review_evidence(evidence, decision("e", DecisionAction.CONFIRM))
        with self.assertRaises(ValueError):
            review_evidence(confirmed, confirmed.decisions[0])
        for overrides in ({"author": ""}, {"justification": ""}, {"recorded_at": "2026-10-23T12:00:00"}):
            with self.subTest(overrides=overrides), self.assertRaises(ValueError):
                replace(decision("e", DecisionAction.CONFIRM), **overrides)
        with self.assertRaises(ValueError):
            decision("e", DecisionAction.CORRECT)
        with self.assertRaises(ValueError):
            decision("e", DecisionAction.CONFIRM, 8)

    def test_invalid_page_and_nonfinite_observations(self):
        for overrides in ({"page": 0}, {"page": True}, {"interpreted": float("nan")}):
            with self.subTest(overrides=overrides), self.assertRaises(ValueError):
                Evidence("e", "doc", "raw", "READING", **overrides)

    def test_unknown_thickness_does_not_prevent_occurrence(self):
        slab = Slab("slab", "form")
        bar = ReinforcementOccurrence("bar", "N26", "V", 12.5, None, "drawing")
        self.assertIsNone(slab.thickness_cm)
        self.assertEqual(bar.diameter_mm, 12.5)
        self.assertIsNone(bar.geometry)

    def test_one_slab_preserves_multiple_thickness_regions(self):
        geometry = GeometryReference("polygon.json#/zone", "FORM_LOCAL", "cm")
        zones = (ThicknessRegion("a", 15, geometry), ThicknessRegion("b", 20))
        slab = Slab("slab", "form", thickness_regions=zones, top_level_m=0)
        self.assertEqual(slab.id, "slab")
        self.assertEqual(len(slab.thickness_regions), 2)
        self.assertEqual(slab.top_level_m, 0)
        with self.assertRaises(ValueError):
            replace(slab, thickness_cm=20)
        with self.assertRaises(ValueError):
            replace(slab, thickness_regions=(zones[0], zones[0]))

    def test_invalid_dimensions_and_unknown_direction(self):
        for value in (-1, 0, True, float("inf")):
            with self.subTest(value=value), self.assertRaises(ValueError):
                Slab("s", "form", thickness_cm=value)
            with self.subTest(value=value), self.assertRaises(ValueError):
                ReinforcementOccurrence("b", "N1", None, value, None, "doc")
        unknown = ReinforcementOccurrence("b", "N1", None, None, None, "doc")
        self.assertIsNone(unknown.direction)

    def test_grid_id_is_explicit_and_not_derived_from_input_order(self):
        geometry = GeometryReference("source#/line/A", "DXF_LOCAL", "cm")
        a = GridLine("line-A", "V", geometry, "dxf", "moments.json#/A")
        b = GridLine("line-B", "V", geometry, "dxf")
        self.assertEqual({line.id for line in (a, b)}, {line.id for line in (b, a)})
        self.assertIsNone(b.moment_data_reference)


class ReviewTests(unittest.TestCase):
    def test_state_pairs(self):
        valid = {
            X.NOT_EXECUTED: {R.NOT_EVALUATED},
            X.PARTIALLY_EXECUTED: {R.NOT_EVALUATED, R.INCONCLUSIVE, R.FAIL},
            X.EXECUTED_INCONCLUSIVE: {R.INCONCLUSIVE},
            X.EXECUTED_COMPLETE: {R.PASS, R.FAIL, R.NOT_APPLICABLE},
        }
        for execution in X:
            for result in R:
                with self.subTest(execution=execution, result=result):
                    args = dict(
                        id="c", object_id="s", criterion=criterion(), execution=execution,
                        result=result, evidence_ids=("e",), engineer_notes=("Motivo explícito",),
                    )
                    if result in valid[execution]:
                        Control(**args)
                    else:
                        with self.assertRaises(ValueError):
                            Control(**args)

    def test_inconclusive_inapplicable_and_pass_need_support(self):
        for execution, result in ((X.EXECUTED_INCONCLUSIVE, R.INCONCLUSIVE), (X.EXECUTED_COMPLETE, R.NOT_APPLICABLE)):
            with self.subTest(result=result), self.assertRaises(ValueError):
                Control("c", "s", criterion(), execution=execution, result=result)
        with self.assertRaises(ValueError):
            Control("c", "s", criterion(), execution=X.EXECUTED_COMPLETE, result=R.PASS)
        with self.assertRaises(ValueError):
            Control("c", "s", criterion(), execution=X.EXECUTED_COMPLETE, result=R.PASS,
                    evidence_ids=("e",), pending=("Missing input",))

    def test_dependencies_block_only_their_own_control_and_do_not_run_it(self):
        complete = Control("local", "bar", criterion(), dependencies=(Dependency("diameter", "Bitola"),))
        blocked = Control("capacity", "bar", criterion(), dependencies=(Dependency("thickness", "Espessura"),))
        availability = {"diameter": True}
        passed = record_outcome(complete, availability, execution=X.EXECUTED_COMPLETE, result=R.PASS, evidence_ids=("e",))
        self.assertFalse(assess_dependencies(blocked, availability).ready)
        self.assertEqual(blocked.result, R.NOT_EVALUATED)
        self.assertEqual(blocked.execution, X.NOT_EXECUTED)
        self.assertEqual(passed.result, R.PASS)
        self.assertEqual(complete.result, R.NOT_EVALUATED)
        with self.assertRaises(ValueError):
            record_outcome(blocked, availability, execution=X.EXECUTED_COMPLETE, result=R.PASS, evidence_ids=("e",))
        self.assertEqual(passed.result, R.PASS)
        with self.assertRaises(ValueError):
            assess_dependencies(blocked, {"thickness": 1})

    def test_resolved_dependency_only_releases_does_not_approve(self):
        control = Control("c", "s", criterion(), dependencies=(Dependency("data", "Dado"),))
        self.assertTrue(assess_dependencies(control, {"data": True}).ready)
        self.assertEqual(control.result, R.NOT_EVALUATED)

    def test_partial_known_failure_survives_other_missing_inputs(self):
        control = Control("c", "s", criterion(), dependencies=(Dependency("other", "Outra informação"),))
        failed = record_outcome(
            control, {}, execution=X.PARTIALLY_EXECUTED, result=R.FAIL,
            evidence_ids=("proven-failure",), pending=("Outra parcela ainda não examinada",),
        )
        self.assertEqual(failed.result, R.FAIL)
        self.assertFalse(assess_dependencies(failed, {}).ready)
        self.assertEqual(failed.criterion.origin, CriterionOrigin.OFFICE_STANDARD)

    def test_finding_acceptance_rejection_never_rewrites_technical_result(self):
        failed = Control("c", "s", criterion(), execution=X.EXECUTED_COMPLETE, result=R.FAIL, evidence_ids=("e",))
        accepted = review_finding(failed, decision("c", DecisionAction.ACCEPT))
        rejected = review_finding(accepted, decision("c", DecisionAction.REJECT, id="decision-2"))
        self.assertEqual(rejected.result, R.FAIL)
        self.assertEqual(rejected.execution, X.EXECUTED_COMPLETE)
        self.assertEqual(len(rejected.decisions), 2)
        self.assertEqual(failed.decisions, ())
        with self.assertRaises(ValueError):
            review_finding(failed, decision("c", DecisionAction.CORRECT, 12))
        with self.assertRaises(ValueError):
            review_finding(failed, decision("other", DecisionAction.ACCEPT))

    def test_possible_issue_remains_inconclusive(self):
        control = Control(
            "c", "s", criterion(), execution=X.EXECUTED_INCONCLUSIVE,
            result=R.INCONCLUSIVE, pending=("Possível lacuna; extração ainda não conferida.",),
        )
        self.assertEqual(control.result, R.INCONCLUSIVE)

    def test_not_applicable_requires_reason_instead_of_missing_data_inference(self):
        control = Control("c", "s", criterion(), dependencies=(Dependency("data", "Dado"),))
        result = record_outcome(
            control, {}, execution=X.EXECUTED_COMPLETE, result=R.NOT_APPLICABLE,
            engineer_notes=("Inaplicabilidade física documentada pelo responsável.",),
        )
        self.assertEqual(result.result, R.NOT_APPLICABLE)


class ExampleTests(unittest.TestCase):
    def test_demonstration_is_independent_and_preserves_missing_data(self):
        example = build_example()
        self.assertTrue(example["demonstration_only"])
        self.assertEqual(example["occurrence_before"].diameter_mm, 12)
        self.assertEqual(example["occurrence_after"].diameter_mm, 12.5)
        self.assertIsNone(example["evidence_before"][1].effective_value)
        self.assertEqual(example["evidence_after"][1].effective_value, 11)
        self.assertIsNone(example["slabs"][0].thickness_cm)
        self.assertEqual([c.result for c in example["controls"]], [R.PASS, R.NOT_EVALUATED, R.NOT_EVALUATED])
        self.assertEqual([a.ready for a in example["dependency_assessments"]], [True, False, False])

    def test_json_projection_keeps_original_sources_and_review_history(self):
        example = build_example()
        data = json.loads(json.dumps(to_data(example), ensure_ascii=False, allow_nan=False))
        after = data["evidence_after"][0]
        self.assertEqual(after["observed"], "38 Ø12.5 c/11 C=618")
        self.assertEqual(after["interpreted"], 12)
        self.assertEqual(after["decisions"][0]["value"], 12.5)
        self.assertEqual(data["controls"][0]["result"], "PASS")
        self.assertIn("fictício", after["decisions"][0]["author"])
        self.assertEqual(to_data(build_example()), to_data(example))


if __name__ == "__main__":
    unittest.main()
