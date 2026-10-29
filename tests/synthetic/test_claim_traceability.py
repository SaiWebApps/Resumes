from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from test_engine import make_fixture, write_json

from application_pack.engine import run_manifest


class ClaimTraceabilityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.manifest = make_fixture(self.root)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _load(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def _assert_evidence_blocked(self, report: dict) -> None:
        gates = {gate["id"]: gate for gate in report["gates"]}
        self.assertEqual(gates["evidence_integrity"]["status"], "fail", report)
        self.assertFalse((self.root / "runs" / "synthetic-run" / "final").exists())

    def test_ordinary_invented_fact_without_semantic_unit_blocks_release(self) -> None:
        for invention in ("Founded NASA.", "Served as President of Mars.", "Invented cold fusion."):
            with self.subTest(invention=invention):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    manifest = make_fixture(root)
                    path = root / "stages" / "resume.json"
                    data = self._load(path)
                    data["semantic_text"] += "\n" + invention
                    write_json(path, data)
                    code, report = run_manifest(manifest)
                    self.assertEqual(code, 2)
                    gates = {gate["id"]: gate for gate in report["gates"]}
                    self.assertEqual(gates["evidence_integrity"]["status"], "fail", report)
                    self.assertFalse((root / "runs" / "synthetic-run" / "final").exists())

    def test_invented_fact_cannot_cite_an_unrelated_claim(self) -> None:
        path = self.root / "stages" / "resume.json"
        data = self._load(path)
        data["semantic_text"] += "\nFounded NASA."
        data["semantic_units"].append({
            "id": "resume-invented",
            "text": "Founded NASA.",
            "kind": "evidence",
            "support_refs": ["claim:platform-claim"],
        })
        write_json(path, data)
        code, report = run_manifest(self.manifest)
        self.assertEqual(code, 2)
        self._assert_evidence_blocked(report)

    def test_invented_fact_cannot_be_misclassified_as_structure(self) -> None:
        path = self.root / "stages" / "cover-letter.json"
        data = self._load(path)
        data["semantic_text"] += "\nInvented cold fusion."
        data["semantic_units"].append({
            "id": "cover-invented",
            "text": "Invented cold fusion.",
            "kind": "structure",
            "support_refs": ["structure:heading"],
        })
        write_json(path, data)
        code, report = run_manifest(self.manifest)
        self.assertEqual(code, 2)
        self._assert_evidence_blocked(report)

    def test_invented_fact_cannot_be_misclassified_as_strategy_or_opportunity(self) -> None:
        for kind, refs in (
            ("strategy", ["strategy:topic-1"]),
            ("opportunity", ["opportunity:https://example.test/conference"]),
        ):
            with self.subTest(kind=kind):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    manifest = make_fixture(root)
                    path = root / "stages" / "cover-letter.json"
                    data = self._load(path)
                    data["semantic_text"] += "\nServed as President of Mars."
                    data["semantic_units"].append({
                        "id": f"cover-invented-{kind}",
                        "text": "Served as President of Mars.",
                        "kind": kind,
                        "support_refs": refs,
                    })
                    write_json(path, data)
                    code, report = run_manifest(manifest)
                    self.assertEqual(code, 2)
                    gates = {gate["id"]: gate for gate in report["gates"]}
                    self.assertEqual(gates["evidence_integrity"]["status"], "fail", report)

    def test_declared_claim_without_visible_evidence_is_rejected(self) -> None:
        path = self.root / "stages" / "resume.json"
        data = self._load(path)
        platform_unit = next(unit for unit in data["semantic_units"] if unit["id"] == "resume-line-2")
        platform_unit["support_refs"] = ["claim:identity-claim"]
        write_json(path, data)

        code, report = run_manifest(self.manifest)
        self.assertEqual(code, 2)
        self._assert_evidence_blocked(report)
        errors = next(gate["errors"] for gate in report["gates"] if gate["id"] == "evidence_integrity")
        self.assertTrue(any("declares claim 'platform-claim'" in error for error in errors), errors)

    def test_partial_sentence_cannot_attest_full_protected_claim(self) -> None:
        evidence_path = self.root / "stages" / "evidence-bundle.json"
        evidence = self._load(evidence_path)
        full_text = (
            "Designed a platform for city teams. Managed eight engineers, five senior engineers, "
            "and seven vendors; owned performance reviews and compensation recommendations."
        )
        platform_claim = next(claim for claim in evidence["claims"] if claim["id"] == "platform-claim")
        platform_claim.update({
            "text": full_text,
            "protected": True,
            "representation_anchors": {
                "resume": ["five senior engineers", "seven vendors", "compensation recommendations"]
            },
        })
        write_json(evidence_path, evidence)

        resume_path = self.root / "stages" / "resume.json"
        resume = self._load(resume_path)
        next(claim for claim in resume["claims"] if claim["claim_id"] == "platform-claim")["text"] = full_text
        write_json(resume_path, resume)

        code, report = run_manifest(self.manifest)
        self.assertEqual(code, 2)
        self._assert_evidence_blocked(report)
        errors = next(gate["errors"] for gate in report["gates"] if gate["id"] == "evidence_integrity")
        self.assertTrue(any("materially weakens declared claim 'platform-claim'" in error for error in errors), errors)
        self.assertTrue(any("omits required representation anchor" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
