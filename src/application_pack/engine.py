from __future__ import annotations

import os
import shutil
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .artifacts import artifact_metadata, canonical_json, load_json, sha256_bytes, sha256_file, write_json
from .contracts import ARTIFACT_IDS, SCHEMA_VERSION, SOURCE_KEYS, ContractError, resolve_path, validate_manifest
from .schema_validation import validate_document
from .validation import validate_release
from .rendering import require_fresh_render_match, verified_renderer_identities


STAGE_SKILLS = {
    "evidence": "career-evidence",
    "opportunity": "opportunity-auditor",
    "positioning": "application-positioner",
    "resume": "resume-author",
    "pitch": "speaker-pitch-author",
    "design": "document-compositor",
    "changes": "artifact-change-controller",
    "render": "document-compositor",
    "review": "submission-release-auditor",
}

SOURCE_STAGES: tuple[tuple[str, tuple[tuple[str, str], ...]], ...] = (
    ("evidence", (("evidence-bundle.json", "evidence_bundle"),)),
    ("opportunity", (("opportunity-brief.json", "opportunity_brief"),)),
    ("positioning", (("strategy.json", "strategy"),)),
    ("resume", (("resume.json", "resume"), ("coverage-ledger.json", "coverage_ledger"))),
    ("pitch", (("cover-letter.json", "cover_letter"),)),
    ("design", (("design-contract.json", "design_contract"),)),
    ("changes", (("change-set.json", "change_set"),)),
)


class NextActionRequired(RuntimeError):
    def __init__(self, next_action: dict[str, Any]):
        super().__init__(next_action["message"])
        self.next_action = next_action


def utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _state_path(run_dir: Path) -> Path:
    return run_dir / "work" / "state.json"


def _load_state(run_dir: Path, run_id: str) -> dict[str, Any]:
    path = _state_path(run_dir)
    if path.exists():
        state = load_json(path)
        if not isinstance(state, dict) or state.get("run_id") != run_id:
            raise ContractError("Existing run state does not match manifest.run_id")
        return state
    return {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "status": "created",
        "stages": {},
        "failure_history": [],
        "created_at": utc_now(),
        "updated_at": utc_now(),
    }


def _save_state(run_dir: Path, state: dict[str, Any]) -> None:
    state["updated_at"] = utc_now()
    write_json(_state_path(run_dir), state)


def _next_action(run_dir: Path, stage: str, missing: list[dict[str, str]]) -> dict[str, Any]:
    action = {
        "schema_version": SCHEMA_VERSION,
        "status": "action_required",
        "stage": stage,
        "skill": STAGE_SKILLS[stage],
        "missing_outputs": missing,
        "message": f"Invoke ${STAGE_SKILLS[stage]} to create the missing stage outputs, then run the same manifest again.",
    }
    write_json(run_dir / "next-action.json", action)
    return action


def _copy_json_source(source: Path, destination: Path) -> None:
    value = load_json(source)
    validate_document(value, destination.name.replace(".json", ".schema.json"))
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def _record_stage(
    state: dict[str, Any],
    stage: str,
    input_hashes: dict[str, str],
    output_paths: list[Path],
    source_hashes: dict[str, str] | None = None,
) -> dict[str, str]:
    output_hashes = {path.name: sha256_file(path) for path in output_paths}
    previous = state["stages"].get(stage)
    state["stages"][stage] = {
        "status": "complete",
        "input_hashes": dict(input_hashes),
        "output_hashes": output_hashes,
        "source_hashes": source_hashes or {},
        "completed_at": utc_now(),
        "changed": not isinstance(previous, dict) or previous.get("output_hashes") != output_hashes,
    }
    return output_hashes


def _prepare_source_stage(
    *,
    manifest: dict[str, Any],
    manifest_dir: Path,
    run_dir: Path,
    state: dict[str, Any],
    stage: str,
    outputs: tuple[tuple[str, str], ...],
    previous_output_hashes: dict[str, str],
) -> dict[str, str]:
    missing: list[dict[str, str]] = []
    resolved: list[tuple[Path, Path]] = []
    for filename, key in outputs:
        source = resolve_path(manifest_dir, manifest["stage_sources"][key])
        destination = run_dir / "audit" / filename
        if not source.is_file():
            missing.append({"contract": key, "expected_path": str(source), "schema": f"schemas/{filename[:-5]}.schema.json"})
        else:
            resolved.append((source, destination))
    if missing:
        state["status"] = "action_required"
        state["blocked_stage"] = stage
        _save_state(run_dir, state)
        raise NextActionRequired(_next_action(run_dir, stage, missing))

    source_hashes: dict[str, str] = {}
    destinations: list[Path] = []
    for source, destination in resolved:
        _copy_json_source(source, destination)
        source_hashes[str(source)] = sha256_file(source)
        destinations.append(destination)
    return _record_stage(state, stage, previous_output_hashes, destinations, source_hashes)


def _prepare_render_stage(
    *,
    manifest: dict[str, Any],
    manifest_dir: Path,
    run_dir: Path,
    state: dict[str, Any],
    previous_output_hashes: dict[str, str],
) -> dict[str, str]:
    candidate = run_dir / "candidate"
    candidate.mkdir(parents=True, exist_ok=True)
    for stale in candidate.iterdir():
        if stale.is_dir() and not stale.is_symlink():
            shutil.rmtree(stale)
        else:
            stale.unlink()

    missing: list[dict[str, str]] = []
    sources: dict[str, Path] = {}
    for artifact_id in ARTIFACT_IDS:
        source = resolve_path(manifest_dir, manifest["artifact_sources"][artifact_id])
        sources[artifact_id] = source
        if not source.is_file():
            missing.append({"contract": artifact_id, "expected_path": str(source), "schema": "binary artifact"})
    evidence_source = resolve_path(manifest_dir, manifest["stage_sources"]["render_evidence"])
    if not evidence_source.is_file():
        missing.append({
            "contract": "render_evidence",
            "expected_path": str(evidence_source),
            "schema": "schemas/render-evidence.schema.json",
        })
    if missing:
        state["status"] = "action_required"
        state["blocked_stage"] = "render"
        _save_state(run_dir, state)
        raise NextActionRequired(_next_action(run_dir, "render", missing))

    render_evidence = load_json(evidence_source)
    validate_document(render_evidence, "render-evidence.schema.json")
    renderer_capabilities = render_evidence["tool_capabilities"]
    renderer_identities = verified_renderer_identities(renderer_capabilities)
    evidence_items: dict[str, dict[str, Any]] = {}
    for raw_item in render_evidence["artifacts"]:
        artifact_id = raw_item["id"]
        if artifact_id in evidence_items:
            raise ContractError(f"Render evidence repeats artifact {artifact_id}")
        evidence_items[artifact_id] = raw_item
    if set(evidence_items) != set(ARTIFACT_IDS):
        raise ContractError("Render evidence must contain each required artifact exactly once")

    metadata: list[dict[str, Any]] = []
    seen_names: set[str] = set()
    evidence_root = run_dir / "audit" / "render-evidence"
    if evidence_root.exists():
        shutil.rmtree(evidence_root)
    source_hashes: dict[str, str] = {str(evidence_source): sha256_file(evidence_source)}
    for artifact_id, source in sources.items():
        if source.name in seen_names:
            raise ContractError(f"Artifact filenames must be unique; repeated {source.name}")
        seen_names.add(source.name)
        destination = candidate / source.name
        shutil.copy2(source, destination)
        item = artifact_metadata(destination, artifact_id)
        evidence = evidence_items[artifact_id]
        declared_source = resolve_path(evidence_source.parent, evidence["source"])
        if declared_source != source:
            raise ContractError(
                f"Render evidence source for {artifact_id} resolves to {declared_source}, expected {source}"
            )
        if evidence["format"] != item["format"]:
            raise ContractError(f"Render evidence format differs for {artifact_id}")
        if evidence["sha256"] != item["sha256"]:
            raise ContractError(f"Render evidence is stale for {artifact_id}")

        document_id = "resume" if artifact_id.startswith("resume_") else "cover_letter"
        expected_pages = manifest["constraints"]["page_counts"][document_id]
        evidence_pages = evidence["pages"]
        if len(evidence_pages) != expected_pages:
            raise ContractError(
                f"Render evidence for {artifact_id} has {len(evidence_pages)} pages; expected {expected_pages}"
            )
        if item["pages"] is not None and item["pages"] != len(evidence_pages):
            raise ContractError(f"PDF page count disagrees with render evidence for {artifact_id}")

        require_fresh_render_match(
            destination,
            artifact_id,
            item["format"],
            evidence_pages,
            renderer_capabilities,
            run_dir / "work" / "fresh-render-verification" / artifact_id,
        )

        page_directory = evidence_root / artifact_id
        page_directory.mkdir(parents=True, exist_ok=True)
        frozen_pages: list[dict[str, Any]] = []
        for page_number, page in enumerate(evidence_pages, start=1):
            if page["page"] != page_number:
                raise ContractError(f"Render evidence page numbers are not contiguous for {artifact_id}")
            source_page = resolve_path(evidence_source.parent, page["path"])
            if not source_page.is_file():
                raise ContractError(f"Rendered page is missing for {artifact_id} page {page_number}")
            actual_page_hash = sha256_file(source_page)
            if actual_page_hash != page["sha256"]:
                raise ContractError(f"Rendered page hash changed for {artifact_id} page {page_number}")
            if source_page.stat().st_size != page["bytes"]:
                raise ContractError(f"Rendered page byte count changed for {artifact_id} page {page_number}")
            frozen_page = page_directory / f"page-{page_number}.png"
            shutil.copy2(source_page, frozen_page)
            frozen_pages.append({
                "page": page_number,
                "path": str(frozen_page.relative_to(run_dir / "audit")),
                "sha256": actual_page_hash,
                "bytes": frozen_page.stat().st_size,
            })
            source_hashes[str(source_page)] = actual_page_hash
        item["pages"] = len(frozen_pages)
        item["page_images"] = frozen_pages
        metadata.append(item)
        source_hashes[str(source)] = item["sha256"]

    render_manifest = {
        "schema_version": SCHEMA_VERSION,
        "run_id": manifest["run_id"],
        "generated_at": utc_now(),
        "renderer_identities": renderer_identities,
        "artifacts": metadata,
    }
    validate_document(render_manifest, "render-manifest.schema.json")
    path = run_dir / "audit" / "render-manifest.json"
    write_json(path, render_manifest)
    for identity in renderer_identities.values():
        source_hashes[identity["path"]] = identity["sha256"]
    return _record_stage(state, "render", previous_output_hashes, [path], source_hashes)


def _prepare_review_stage(
    *,
    manifest: dict[str, Any],
    manifest_dir: Path,
    run_dir: Path,
    state: dict[str, Any],
    previous_output_hashes: dict[str, str],
) -> dict[str, str]:
    sources = {
        "review-evidence.json": resolve_path(manifest_dir, manifest["stage_sources"]["review_evidence"]),
        "review-record.json": resolve_path(manifest_dir, manifest["stage_sources"]["review_record"]),
    }
    missing = [
        {
            "contract": "review_evidence" if filename == "review-evidence.json" else "review_record",
            "expected_path": str(source),
            "schema": f"schemas/{filename[:-5]}.schema.json",
        }
        for filename, source in sources.items()
        if not source.is_file()
    ]
    if missing:
        state["status"] = "action_required"
        state["blocked_stage"] = "review"
        _save_state(run_dir, state)
        raise NextActionRequired(_next_action(run_dir, "review", missing))
    destinations: list[Path] = []
    for filename, source in sources.items():
        destination = run_dir / "audit" / filename
        _copy_json_source(source, destination)
        destinations.append(destination)
    return _record_stage(
        state,
        "review",
        previous_output_hashes,
        destinations,
        {str(source): sha256_file(source) for source in sources.values()},
    )


def _promote(run_dir: Path) -> None:
    candidate = run_dir / "candidate"
    final = run_dir / "final"
    candidate_entries = list(candidate.iterdir())
    if len(candidate_entries) != len(ARTIFACT_IDS) or any(not path.is_file() for path in candidate_entries):
        raise ContractError("candidate/ must contain exactly four submission files")
    expected = {path.name: sha256_file(path) for path in candidate_entries}
    if final.exists():
        final_entries = list(final.iterdir())
        if len(final_entries) != len(ARTIFACT_IDS) or any(not path.is_file() for path in final_entries):
            raise ContractError("final/ must contain exactly four submission files")
        current = {path.name: sha256_file(path) for path in final_entries}
        if current != expected:
            raise ContractError("Existing final/ differs from the passing candidate; use a new run_id")
        return
    pending = Path(tempfile.mkdtemp(prefix="final.pending-", dir=run_dir))
    try:
        for source in candidate.iterdir():
            if source.is_file():
                shutil.copy2(source, pending / source.name)
        os.replace(pending, final)
    except Exception:
        shutil.rmtree(pending, ignore_errors=True)
        raise


def run_manifest(manifest_path: Path) -> tuple[int, dict[str, Any]]:
    manifest_path = manifest_path.resolve()
    raw_manifest = load_json(manifest_path)
    validate_document(raw_manifest, "run-manifest.schema.json")
    manifest = validate_manifest(raw_manifest)
    manifest_dir = manifest_path.parent
    output_root = resolve_path(manifest_dir, manifest["output_dir"])
    run_dir = output_root / manifest["run_id"]
    for name in ("work", "audit", "candidate"):
        (run_dir / name).mkdir(parents=True, exist_ok=True)

    manifest_hash = sha256_bytes(canonical_json(manifest))
    stored_manifest = run_dir / "work" / "run-manifest.json"
    if stored_manifest.exists():
        stored_hash = sha256_bytes(canonical_json(load_json(stored_manifest)))
        if (run_dir / "final").exists() and stored_hash != manifest_hash:
            raise ContractError("A released run is immutable; use a new run_id for a changed manifest")
    write_json(stored_manifest, manifest)
    state = _load_state(run_dir, manifest["run_id"])
    state["manifest_sha256"] = manifest_hash
    state["status"] = "running"
    state.pop("blocked_stage", None)
    _save_state(run_dir, state)
    (run_dir / "next-action.json").unlink(missing_ok=True)

    previous_output_hashes: dict[str, str] = {}
    try:
        for stage, outputs in SOURCE_STAGES:
            current = _prepare_source_stage(
                manifest=manifest,
                manifest_dir=manifest_dir,
                run_dir=run_dir,
                state=state,
                stage=stage,
                outputs=outputs,
                previous_output_hashes=previous_output_hashes,
            )
            previous_output_hashes.update(current)
            _save_state(run_dir, state)

        current = _prepare_render_stage(
            manifest=manifest,
            manifest_dir=manifest_dir,
            run_dir=run_dir,
            state=state,
            previous_output_hashes=previous_output_hashes,
        )
        previous_output_hashes.update(current)
        _save_state(run_dir, state)

        current = _prepare_review_stage(
            manifest=manifest,
            manifest_dir=manifest_dir,
            run_dir=run_dir,
            state=state,
            previous_output_hashes=previous_output_hashes,
        )
        previous_output_hashes.update(current)
        _save_state(run_dir, state)
    except NextActionRequired as exc:
        return 4, exc.next_action

    report = validate_release(run_dir, manifest, state)
    validate_document(report, "release-report.schema.json")
    write_json(run_dir / "audit" / "release-report.json", report)
    if report["status"] != "pass":
        signature = sha256_bytes(canonical_json([
            error
            for gate in report["gates"]
            for error in gate["errors"]
        ]))
        candidate_digest = sha256_bytes(canonical_json(report.get("artifact_hashes", {})))
        history = state.setdefault("failure_history", [])
        repeated = bool(history and history[-1].get("signature") == signature and history[-1].get("candidate_digest") == candidate_digest)
        history.append({"signature": signature, "candidate_digest": candidate_digest, "at": utc_now()})
        state["status"] = "blocked_no_progress" if repeated else "failed"
        state["last_release_report"] = str(run_dir / "audit" / "release-report.json")
        _save_state(run_dir, state)
        report["run_status"] = state["status"]
        write_json(run_dir / "audit" / "release-report.json", report)
        return 3 if repeated else 2, report

    # Promotion is the commit point. Keep the run non-released until the
    # complete, hash-checked four-file candidate has been atomically promoted.
    # If promotion raises, a retry can safely resume from the unchanged state.
    _promote(run_dir)
    state["status"] = "released"
    state["last_release_report"] = str(run_dir / "audit" / "release-report.json")
    _save_state(run_dir, state)
    report["run_status"] = "released"
    report["final_dir"] = str(run_dir / "final")
    write_json(run_dir / "audit" / "release-report.json", report)
    return 0, report


def validate_run(run_dir: Path) -> dict[str, Any]:
    run_dir = run_dir.resolve()
    manifest = validate_manifest(load_json(run_dir / "work" / "run-manifest.json"))
    state = load_json(_state_path(run_dir))
    report = validate_release(run_dir, manifest, state)
    report["run_status"] = state.get("status")
    return report


def capability_report(profile_path: Path | None = None) -> dict[str, Any]:
    required = {
        "filesystem": True,
        "research": True,
        "rendering": True,
        "visual_inspection": True,
        "second_model": False,
    }
    profile: dict[str, Any] | None = None
    if profile_path:
        candidate = profile_path / "profile" / "profile.json" if profile_path.is_dir() else profile_path
        if candidate.exists():
            profile = load_json(candidate)
            if isinstance(profile, dict):
                required.update(profile.get("required_capabilities", {}))
    return {
        "schema_version": SCHEMA_VERSION,
        "engine": "application-pack",
        "required_capabilities": required,
        "minimum_verified_workflow": [
            "read and write files",
            "research primary sources",
            "create PDF and DOCX",
            "render and inspect every page",
        ],
        "degraded_behavior": "Return next-action.json or a precise blocker; never claim unperformed verification.",
        "profile_loaded": bool(profile),
    }
