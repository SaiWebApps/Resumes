"""Deterministic release invariants that are independent of document parsing.

The renderer and evidence modules own byte-level derivation and factual
traceability.  This module keeps the remaining structure, hierarchy, change,
and reviewer-packet rules explicit so each historical failure can be mutated
and tested without collapsing into a generic reviewer finding.
"""

from __future__ import annotations

import json
import math
import re
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

from .artifacts import extract_docx_text, extract_pdf_text, normalize_semantic_text


MANUAL_CHECK_GROUPS = {
    "layout": (
        "full_page_readability",
        "physical_edge_clearance",
        "natural_content_flow",
        "continuous_page_review",
        "metric_visibility",
        "docx_hanging_indents",
        "role_date_rows_atomic",
        "source_emphasis_preservation",
    ),
    "provenance": ("talk_taxonomy",),
    "parity": ("current_link_inventory",),
}

REVIEWED_INPUTS = (
    "evidence-bundle.json",
    "opportunity-brief.json",
    "strategy.json",
    "resume.json",
    "coverage-ledger.json",
    "cover-letter.json",
    "design-contract.json",
    "change-set.json",
)


def manual_check_failures(review: dict[str, Any], group: str) -> list[str]:
    checks = review.get("manual_checks")
    if not isinstance(checks, dict):
        return ["Review record has no named manual_checks evidence"]
    return [
        f"Named release check did not pass: {name}"
        for name in MANUAL_CHECK_GROUPS[group]
        if checks.get(name) is not True
    ]


def outline_findings(resume: dict[str, Any]) -> list[str]:
    sections = resume.get("sections")
    if not isinstance(sections, list):
        return ["Resume has no ordered section outline"]
    ids = [str(section.get("id", "")).strip() for section in sections if isinstance(section, dict)]
    headings = [str(section.get("heading", "")).strip().casefold() for section in sections if isinstance(section, dict)]
    findings: list[str] = []
    duplicate_ids = sorted(value for value, count in Counter(ids).items() if value and count > 1)
    duplicate_headings = sorted(value for value, count in Counter(headings).items() if value and count > 1)
    if duplicate_ids:
        findings.append(f"Resume outline repeats section ids: {duplicate_ids}")
    if duplicate_headings:
        findings.append(f"Resume outline repeats section purposes/headings: {duplicate_headings}")
    return findings


def verb_variety_findings(resume: dict[str, Any]) -> list[str]:
    openings: list[str] = []
    for claim in resume.get("claims", []):
        if not isinstance(claim, dict):
            continue
        words = re.findall(r"[A-Za-z]+", str(claim.get("text", "")))
        if words:
            openings.append(words[0].casefold())
    if len(openings) < 2:
        return []
    opening, count = Counter(openings).most_common(1)[0]
    permitted = max(1, math.ceil(len(openings) * 0.25))
    if count > permitted:
        return [
            f"Resume overuses the opening verb/word {opening!r}: {count} of {len(openings)} claims; "
            f"maximum allowed is {permitted}"
        ]
    return []


def design_findings(design: dict[str, Any], cover_text: str) -> list[str]:
    elements = [item for item in design.get("visible_elements", []) if isinstance(item, dict)]
    findings: list[str] = []
    by_document_and_function = Counter(
        (str(item.get("document_id")), str(item.get("function"))) for item in elements
    )
    for document_id, function in (("resume", "identity"), ("resume", "contact"), ("cover_letter", "signature")):
        if by_document_and_function[(document_id, function)] > 1:
            findings.append(f"{document_id} contains more than one {function} block")

    if cover_text.lstrip().casefold().startswith("dear ") and not any(
        item.get("document_id") == "cover_letter" and item.get("function") == "salutation"
        for item in elements
    ):
        findings.append("Cover-letter salutation is not classified as a salutation")

    tagline_requested = design.get("page_constraints", {}).get("resume_tagline") is True
    has_tagline = any(
        item.get("document_id") == "resume" and item.get("function") == "tagline"
        for item in elements
    )
    if has_tagline and not tagline_requested:
        findings.append("Resume contains an unrequested tagline")

    styles = design.get("semantic_styles")
    if isinstance(styles, dict):
        serialized = [json.dumps(value, sort_keys=True) for value in styles.values()]
        duplicate_styles = [value for value, count in Counter(serialized).items() if count > 1]
        if duplicate_styles:
            findings.append("Distinct semantic style names resolve to indistinguishable style definitions")

    for page_break in design.get("page_breaks", []):
        if not isinstance(page_break, dict):
            findings.append("Page-break evidence is malformed")
            continue
        reason = str(page_break.get("reason", "")).strip()
        if not reason:
            findings.append("Forced page break has no semantic justification")
        previous_fill = page_break.get("previous_fill_ratio")
        next_fraction = page_break.get("next_block_fraction")
        if isinstance(previous_fill, (int, float)) and isinstance(next_fraction, (int, float)):
            if previous_fill + next_fraction <= 1:
                findings.append("Forced page break interrupts content that fits in the natural flow")
    return findings


def conflicting_provenance_requirements(evidence: dict[str, Any]) -> list[str]:
    parents: dict[str, set[str]] = {}
    for requirement in evidence.get("provenance_requirements", []):
        if not isinstance(requirement, dict):
            continue
        parents.setdefault(str(requirement.get("child_entity_id")), set()).add(
            str(requirement.get("parent_entity_id"))
        )
    return [
        f"Provenance identity {child!r} has conflicting parents: {sorted(values)}"
        for child, values in parents.items()
        if len(values) > 1
    ]


def reviewed_input_findings(review: dict[str, Any], audit: Path, sha256_file) -> list[str]:
    reviewed = review.get("reviewed_input_hashes")
    if not isinstance(reviewed, dict):
        return ["Review record does not identify its requirement and evidence inputs"]
    findings: list[str] = []
    for filename in REVIEWED_INPUTS:
        path = audit / filename
        if not path.is_file() or reviewed.get(filename) != sha256_file(path):
            findings.append(f"Review input hash is stale or missing for {filename}")
    return findings


def change_findings(changes: dict[str, Any], current_page_hashes: Iterable[str]) -> list[str]:
    records = [item for item in changes.get("changes", []) if isinstance(item, dict)]
    findings: list[str] = []
    required_invalidations = {"render", "review", "release"}
    for record in records:
        missing = required_invalidations - set(record.get("invalidates", []))
        if missing:
            findings.append(f"Change {record.get('id')} fails to invalidate {sorted(missing)}")

    collateral = changes.get("collateral_change_ids")
    if not isinstance(collateral, list) or collateral:
        findings.append("Change set contains undeclared collateral changes")

    visual = changes.get("visual_evidence")
    if not isinstance(visual, dict):
        findings.append("Change set lacks visual correction evidence")
    else:
        change_ids = {str(record.get("id")) for record in records}
        reviewed_ids = {str(value) for value in visual.get("reviewed_change_ids", [])}
        if change_ids != reviewed_ids:
            findings.append("Visual correction evidence does not cover every change id exactly")
        current = set(current_page_hashes)
        after = set(str(value) for value in visual.get("after_page_hashes", []))
        if records and (not after or not after.issubset(current)):
            findings.append("Visual correction evidence is not bound to current rendered pages")

    current = set(current_page_hashes)
    for region in changes.get("accepted_regions", []):
        if not isinstance(region, dict):
            findings.append("Accepted-region evidence is malformed")
            continue
        if not str(region.get("description", "")).strip():
            findings.append("Accepted region lacks a useful description")
        if region.get("sha256") not in current:
            findings.append(f"Accepted region {region.get('artifact_id')} no longer matches a current page")
    return findings


def atomic_phrase_findings(path: Path, artifact_format: str, phrases: Iterable[str]) -> list[str]:
    """Reject dangling separators inside protected titles or credentials.

    A break *before* a conjunction is readable (``Electrical`` followed by
    ``& Computer Engineering``).  A break *after* ``|`` or ``&`` strands the
    separator and damages the semantic phrase, so that is the objective defect.
    """

    if artifact_format == "pdf":
        raw_text = extract_pdf_text(path)[0]
    elif artifact_format == "docx":
        raw_text = extract_docx_text(path)
    else:
        return [f"Cannot inspect atomic phrases in unknown format {artifact_format!r}"]
    normalized_document = normalize_semantic_text(raw_text)
    raw_lines = raw_text.splitlines()
    findings: list[str] = []
    for line_number, line in enumerate(raw_lines, start=1):
        if line.rstrip().endswith(("|", "&")):
            findings.append(f"Line {line_number} in {path.name} ends with a dangling separator")
    for phrase in phrases:
        normalized_phrase = normalize_semantic_text(str(phrase))
        if normalized_phrase and normalized_phrase not in normalized_document:
            findings.append(f"Protected atomic phrase is missing from {path.name}: {phrase!r}")
    return findings
