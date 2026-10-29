from __future__ import annotations

import re
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "1.0"
ARTIFACT_IDS = ("resume_pdf", "resume_docx", "cover_letter_pdf", "cover_letter_docx")
STAGE_OUTPUTS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("evidence", ("evidence-bundle.json",)),
    ("opportunity", ("opportunity-brief.json",)),
    ("positioning", ("strategy.json",)),
    ("resume", ("resume.json", "coverage-ledger.json")),
    ("pitch", ("cover-letter.json",)),
    ("design", ("design-contract.json",)),
    ("changes", ("change-set.json",)),
    ("render", ("render-manifest.json",)),
    ("review", ("review-evidence.json", "review-record.json")),
)

SOURCE_KEYS = {
    "evidence-bundle.json": "evidence_bundle",
    "opportunity-brief.json": "opportunity_brief",
    "strategy.json": "strategy",
    "resume.json": "resume",
    "coverage-ledger.json": "coverage_ledger",
    "cover-letter.json": "cover_letter",
    "design-contract.json": "design_contract",
    "change-set.json": "change_set",
    "render-evidence.json": "render_evidence",
    "review-evidence.json": "review_evidence",
    "review-record.json": "review_record",
}


class ContractError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def require_mapping(value: Any, label: str) -> dict[str, Any]:
    require(isinstance(value, dict), f"{label} must be an object")
    return value


def require_list(value: Any, label: str) -> list[Any]:
    require(isinstance(value, list), f"{label} must be an array")
    return value


def validate_manifest(manifest: Any) -> dict[str, Any]:
    value = require_mapping(manifest, "manifest")
    require(value.get("schema_version") == SCHEMA_VERSION, f"manifest.schema_version must be {SCHEMA_VERSION}")
    run_id = value.get("run_id")
    require(isinstance(run_id, str) and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}", run_id) is not None,
            "manifest.run_id must be a safe non-empty identifier")
    profile = require_mapping(value.get("profile"), "manifest.profile")
    require(isinstance(profile.get("id"), str) and profile["id"].strip(), "manifest.profile.id is required")
    require(isinstance(value.get("objective"), str) and value["objective"].strip(), "manifest.objective is required")
    opportunity = require_mapping(value.get("opportunity"), "manifest.opportunity")
    require(isinstance(opportunity.get("url"), str) and opportunity["url"].startswith(("http://", "https://")),
            "manifest.opportunity.url must be an HTTP(S) URL")
    require(isinstance(value.get("output_dir"), str) and value["output_dir"].strip(), "manifest.output_dir is required")

    sources = require_mapping(value.get("stage_sources"), "manifest.stage_sources")
    for key in SOURCE_KEYS.values():
        require(isinstance(sources.get(key), str) and sources[key].strip(), f"manifest.stage_sources.{key} is required")
    artifacts = require_mapping(value.get("artifact_sources"), "manifest.artifact_sources")
    for key in ARTIFACT_IDS:
        require(isinstance(artifacts.get(key), str) and artifacts[key].strip(), f"manifest.artifact_sources.{key} is required")

    constraints = require_mapping(value.get("constraints"), "manifest.constraints")
    page_counts = require_mapping(constraints.get("page_counts"), "manifest.constraints.page_counts")
    require(isinstance(page_counts.get("resume"), int) and page_counts["resume"] > 0,
            "manifest.constraints.page_counts.resume must be positive")
    require(isinstance(page_counts.get("cover_letter"), int) and page_counts["cover_letter"] > 0,
            "manifest.constraints.page_counts.cover_letter must be positive")
    require(isinstance(constraints.get("forbid_page_numbers"), bool),
            "manifest.constraints.forbid_page_numbers must be boolean")

    review_policy = require_mapping(value.get("review_policy"), "manifest.review_policy")
    require(isinstance(review_policy.get("allow_disclosed_fallback"), bool),
            "manifest.review_policy.allow_disclosed_fallback must be boolean")
    capabilities = require_mapping(value.get("capabilities"), "manifest.capabilities")
    for key in ("filesystem", "research", "rendering", "visual_inspection"):
        require(isinstance(capabilities.get(key), bool), f"manifest.capabilities.{key} must be boolean")
    return value


def resolve_path(base: Path, raw: str) -> Path:
    value = Path(raw).expanduser()
    return value.resolve() if value.is_absolute() else (base / value).resolve()
