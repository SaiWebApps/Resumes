from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from test_engine import make_fixture

from application_pack.artifacts import sha256_file
from application_pack.engine import run_manifest


class ReleaseInvariantTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.manifest_path = make_fixture(self.root)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def load(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def save(self, path: Path, value: dict) -> None:
        path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    def refresh_review_hashes(self) -> None:
        manifest = self.load(self.manifest_path)
        review_path = self.root / "stages" / "review-record.json"
        review = self.load(review_path)
        evidence_path = self.root / "stages" / "render-evidence.json"
        evidence = self.load(evidence_path)
        evidence_by_id = {item["id"]: item for item in evidence["artifacts"]}
        for artifact_id, relative_path in manifest["artifact_sources"].items():
            artifact_path = self.root / relative_path
            artifact_hash = sha256_file(artifact_path)
            review["artifact_hashes"][artifact_id] = artifact_hash
            evidence_by_id[artifact_id]["sha256"] = artifact_hash
            evidence_by_id[artifact_id]["bytes"] = artifact_path.stat().st_size
        self.save(evidence_path, evidence)
        self.save(review_path, review)

    def test_undeclared_nobel_claim_blocks_release(self) -> None:
        resume_path = self.root / "stages" / "resume.json"
        resume = self.load(resume_path)
        lines = resume["semantic_text"].splitlines() + ["Won a Nobel Prize."]
        resume["semantic_text"] = "\n".join(lines)
        self.save(resume_path, resume)

        code, report = run_manifest(self.manifest_path)
        self.assertEqual(code, 2, report)
        evidence_gate = next(gate for gate in report["gates"] if gate["id"] == "evidence_integrity")
        self.assertEqual(evidence_gate["status"], "fail")
        self.assertTrue(any("Nobel Prize" in error for error in evidence_gate["errors"]), evidence_gate)
        self.assertFalse((self.root / "runs" / "synthetic-run" / "final").exists())

    def test_retry_replaces_stale_candidates_and_promotes_exactly_four(self) -> None:
        design_path = self.root / "stages" / "design-contract.json"
        design = self.load(design_path)
        design["visible_elements"][0]["reader_purpose"] = ""
        self.save(design_path, design)
        first_code, _ = run_manifest(self.manifest_path)
        self.assertEqual(first_code, 2)

        design["visible_elements"][0]["reader_purpose"] = "Identify the candidate"
        self.save(design_path, design)
        manifest = self.load(self.manifest_path)
        renamed = {
            "resume_pdf": "revised-resume.pdf",
            "resume_docx": "revised-resume.docx",
            "cover_letter_pdf": "revised-cover-letter.pdf",
            "cover_letter_docx": "revised-cover-letter.docx",
        }
        render_evidence_path = self.root / "stages" / "render-evidence.json"
        render_evidence = self.load(render_evidence_path)
        for artifact_id, filename in renamed.items():
            old_path = self.root / manifest["artifact_sources"][artifact_id]
            new_path = self.root / "artifacts" / filename
            shutil.copy2(old_path, new_path)
            manifest["artifact_sources"][artifact_id] = str(Path("artifacts") / filename)
            item = next(item for item in render_evidence["artifacts"] if item["id"] == artifact_id)
            item["source"] = str(new_path)
        self.save(self.manifest_path, manifest)
        self.save(render_evidence_path, render_evidence)
        self.refresh_review_hashes()

        second_code, report = run_manifest(self.manifest_path)
        self.assertEqual(second_code, 0, report)
        final_dir = self.root / "runs" / "synthetic-run" / "final"
        self.assertEqual(sorted(path.name for path in final_dir.iterdir()), sorted(renamed.values()))

    def test_extra_candidate_blocks_release_validation(self) -> None:
        code, report = run_manifest(self.manifest_path)
        self.assertEqual(code, 0, report)
        run_dir = self.root / "runs" / "synthetic-run"
        (run_dir / "candidate" / "unexpected.txt").write_text("not a submission file", encoding="utf-8")

        from application_pack.engine import validate_run

        revalidated = validate_run(run_dir)
        readiness = next(gate for gate in revalidated["gates"] if gate["id"] == "submission_readiness")
        self.assertEqual(readiness["status"], "fail")
        self.assertTrue(any("exactly the four" in error for error in readiness["errors"]), readiness)

        (run_dir / "candidate" / "unexpected.txt").unlink()
        (run_dir / "final" / "unexpected.txt").write_text("not a submission file", encoding="utf-8")
        revalidated = validate_run(run_dir)
        readiness = next(gate for gate in revalidated["gates"] if gate["id"] == "submission_readiness")
        self.assertEqual(readiness["status"], "fail")
        self.assertTrue(any("exactly the four" in error for error in readiness["errors"]), readiness)


if __name__ == "__main__":
    unittest.main()
