from __future__ import annotations

import html
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from .artifacts import canonical_json, docx_visual_findings, load_json, normalize_semantic_text, sha256_bytes, sha256_file
from .contracts import ARTIFACT_IDS, ContractError, SCHEMA_VERSION, require_list, require_mapping
from .invariant_checks import (
    atomic_phrase_findings,
    change_findings,
    conflicting_provenance_requirements,
    design_findings,
    manual_check_failures,
    outline_findings,
    reviewed_input_findings,
    verb_variety_findings,
)


_TRACE_STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "been", "being", "but", "by", "for", "from",
    "had", "has", "have", "i", "in", "into", "is", "it", "its", "my", "of", "on", "or", "our",
    "that", "the", "their", "these", "this", "those", "to", "was", "we", "were", "with", "you",
}
_HIGH_CONSEQUENCE_ASSERTION = re.compile(
    r"(?:[$£€]\s?\d|\b\d+(?:[.,]\d+)?(?:[%×+]|\s*(?:million|billion|engineers?|users?|years?))?\b|"
    r"\b(?:award(?:ed|s)?|certif(?:ied|icate|ication)s?|degree(?:s)?|fellow(?:ship)?s?|honou?rs?|"
    r"nobel|patent(?:ed|s)?|prize(?:s)?|promot(?:ed|ion|ions)|scholar)\b)",
    flags=re.IGNORECASE,
)


def review_packet_sha256(
    artifact_hashes: dict[str, Any],
    page_image_hashes: dict[str, Any],
    reviewed_input_hashes: dict[str, Any],
) -> str:
    """Bind an external-review request to the exact reviewable packet.

    Transcript hashes prove only that a stored string did not change. This
    digest proves that the request named the same artifacts, rendered pages,
    and canonical inputs that the release validator is checking.
    """

    return sha256_bytes(canonical_json({
        "schema_version": SCHEMA_VERSION,
        "artifact_hashes": artifact_hashes,
        "page_image_hashes": page_image_hashes,
        "reviewed_input_hashes": reviewed_input_hashes,
    }))


def _trace_tokens(text: str) -> set[str]:
    return {
        token
        for token in normalize_semantic_text(html.unescape(text)).split()
        if token not in _TRACE_STOPWORDS
    }


def _iter_strings(value: Any):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for child in value.values():
            yield from _iter_strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from _iter_strings(child)


def _is_structural_fact_line(line: str) -> bool:
    letters = "".join(character for character in line if character.isalpha())
    if letters and letters.upper() == letters:
        return True
    if "|" in line:
        return True
    return re.fullmatch(
        r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)?\s*\d{0,2},?\s*\d{4}"
        r"(?:\s*[-–—]\s*(?:Present|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)?\s*\d{0,2},?\s*\d{4}))?",
        line,
        flags=re.IGNORECASE,
    ) is not None


def _unsupported_high_consequence_lines(semantic_text: str, authority_tokens: set[str]) -> list[str]:
    """Return factual lines whose consequential details lack evidence anchors.

    Canonical documents contain reader-facing structural text that is not a claim
    (headings, dates, salutations, and contact labels). High-consequence factual
    lines are different: metrics, credentials, awards, patents, and promotions
    must share multiple substantive tokens with the accepted evidence bundle.
    This catches undeclared assertions without treating layout labels as claims.
    """

    unsupported: list[str] = []
    for raw_line in semantic_text.splitlines():
        line = raw_line.strip()
        if not line or _is_structural_fact_line(line) or not _HIGH_CONSEQUENCE_ASSERTION.search(line):
            continue
        tokens = _trace_tokens(line)
        if not tokens:
            continue
        required_anchors = min(3, len(tokens))
        if len(tokens & authority_tokens) < required_anchors:
            unsupported.append(line)
    return unsupported


@dataclass
class Gate:
    gate_id: str
    label: str
    errors: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.errors

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.gate_id,
            "label": self.label,
            "status": "pass" if self.passed else "fail",
            "errors": self.errors,
        }


class ReleaseValidator:
    def __init__(self, run_dir: Path, manifest: dict[str, Any], state: dict[str, Any]):
        self.run_dir = run_dir
        self.manifest = manifest
        self.state = state
        self.audit = run_dir / "audit"
        self.candidate = run_dir / "candidate"
        self.work = run_dir / "work"
        self.data: dict[str, Any] = {}
        self.gates: list[Gate] = []

    def _gate(self, gate_id: str, label: str, check: Callable[[Gate], None]) -> None:
        gate = Gate(gate_id, label)
        try:
            check(gate)
        except (ContractError, KeyError, TypeError, ValueError) as exc:
            gate.errors.append(str(exc))
        self.gates.append(gate)

    def _load_stage_json(self) -> None:
        filenames = (
            "evidence-bundle.json",
            "opportunity-brief.json",
            "strategy.json",
            "resume.json",
            "coverage-ledger.json",
            "cover-letter.json",
            "design-contract.json",
            "change-set.json",
            "render-manifest.json",
            "review-evidence.json",
            "review-record.json",
        )
        for filename in filenames:
            path = self.audit / filename
            if not path.exists():
                raise ContractError(f"Missing required audit artifact: {filename}")
            value = load_json(path)
            if not isinstance(value, dict) or value.get("schema_version") != SCHEMA_VERSION:
                raise ContractError(f"{filename} must be an object with schema_version {SCHEMA_VERSION}")
            self.data[filename] = value

    def validate(self) -> dict[str, Any]:
        try:
            self._load_stage_json()
        except (ContractError, ValueError) as exc:
            self.gates.append(Gate("contracts", "Typed stage contracts", [str(exc)]))
            return self._report()

        self._gate("evidence_integrity", "Evidence integrity", self._check_evidence)
        self._gate("substance_preservation", "Substance preservation", self._check_coverage)
        self._gate("career_provenance", "Career provenance", self._check_provenance)
        self._gate("opportunity_fit", "Opportunity fit", self._check_opportunity)
        self._gate("persuasive_content", "Persuasive content contract", self._check_content)
        self._gate("document_hierarchy", "Document hierarchy and element purpose", self._check_design)
        self._gate("layout_quality", "Layout and page constraints", self._check_layout)
        self._gate("cross_format_parity", "Cross-format parity", self._check_parity)
        self._gate("change_isolation", "Change isolation", self._check_changes)
        self._gate("exact_artifact_review", "Exact-artifact review", self._check_review)
        self._gate("state_freshness", "Hash-bound state freshness", self._check_state)
        self._gate("submission_readiness", "Submission readiness", self._check_artifacts)
        return self._report()

    def _evidence_maps(self) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
        evidence = self.data["evidence-bundle.json"]
        sources = {item["id"]: item for item in require_list(evidence.get("sources"), "evidence.sources")}
        claims = {item["id"]: item for item in require_list(evidence.get("claims"), "evidence.claims")}
        return sources, claims

    def _document_claims(self) -> list[tuple[str, dict[str, Any]]]:
        items: list[tuple[str, dict[str, Any]]] = []
        for filename, document_id in (("resume.json", "resume"), ("cover-letter.json", "cover_letter")):
            document = self.data[filename]
            for claim in require_list(document.get("claims"), f"{filename}.claims"):
                items.append((document_id, require_mapping(claim, f"{filename}.claim")))
        return items

    def _check_semantic_units(
        self,
        gate: Gate,
        filename: str,
        sources: dict[str, dict[str, Any]],
        claims: dict[str, dict[str, Any]],
    ) -> None:
        """Require a source-bearing classification for every visible text line.

        `semantic_text` is the canonical reader-visible text used for parity.
        Requiring a one-to-one semantic-unit ledger makes an undeclared sentence
        impossible to append silently, while support references make ordinary
        factual assertions subject to the same evidence gate as metrics and
        credentials.  Structural labels have a closed, verifiable vocabulary;
        they cannot be used as a generic escape hatch for prose.
        """

        document = self.data[filename]
        document_id = str(document.get("document_id"))
        raw_text = document.get("semantic_text")
        if not isinstance(raw_text, str):
            return
        lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
        units = require_list(document.get("semantic_units"), f"{filename}.semantic_units")
        if len(units) != len(lines):
            gate.errors.append(
                f"{filename} semantic-unit ledger has {len(units)} units for {len(lines)} visible lines"
            )

        declared_claim_ids = {
            str(item.get("claim_id"))
            for item in require_list(document.get("claims"), f"{filename}.claims")
        }
        opportunity = self.data["opportunity-brief.json"]
        opportunity_urls = {
            str(item.get("url")): item
            for item in require_list(opportunity.get("sources"), "opportunity.sources")
        }
        strategy = self.data["strategy.json"]
        topics = {
            str(item.get("id")): item
            for item in require_list(strategy.get("proposed_topics"), "strategy.proposed_topics")
        }
        sections = {
            str(item.get("id")): str(item.get("heading"))
            for item in document.get("sections", [])
            if isinstance(item, dict)
        }

        seen_ids: set[str] = set()
        evidence_text_by_claim: dict[str, list[str]] = {}
        for index, unit_value in enumerate(units):
            unit = require_mapping(unit_value, f"{filename}.semantic_units[{index}]")
            unit_id = str(unit.get("id", ""))
            if unit_id in seen_ids:
                gate.errors.append(f"{filename} repeats semantic unit id {unit_id!r}")
            seen_ids.add(unit_id)
            if index >= len(lines):
                continue
            unit_text = unit.get("text")
            if not isinstance(unit_text, str) or normalize_semantic_text(unit_text) != normalize_semantic_text(lines[index]):
                gate.errors.append(
                    f"{filename} semantic unit {unit_id!r} does not match visible line {index + 1}"
                )
                continue

            kind = unit.get("kind")
            refs = require_list(unit.get("support_refs"), f"{filename}.{unit_id}.support_refs")
            support_texts: list[str] = []
            claim_ref_count = opportunity_ref_count = strategy_ref_count = structure_ref_count = 0
            unit_claim_ids: list[str] = []
            for raw_ref in refs:
                ref = str(raw_ref)
                prefix, separator, value = ref.partition(":")
                if not separator or not value:
                    gate.errors.append(f"{filename} semantic unit {unit_id!r} has malformed support ref {ref!r}")
                    continue
                if prefix == "claim":
                    claim_ref_count += 1
                    unit_claim_ids.append(value)
                    canonical = claims.get(value)
                    if canonical is None:
                        gate.errors.append(f"{filename} semantic unit {unit_id!r} cites unknown claim {value!r}")
                    elif kind == "evidence" and value not in declared_claim_ids:
                        gate.errors.append(
                            f"{filename} evidence unit {unit_id!r} cites claim {value!r} absent from document claims"
                        )
                    else:
                        support_texts.append(str(canonical.get("text", "")))
                elif prefix == "opportunity":
                    opportunity_ref_count += 1
                    source = opportunity_urls.get(value)
                    if source is None:
                        gate.errors.append(
                            f"{filename} semantic unit {unit_id!r} cites unknown opportunity source {value!r}"
                        )
                    else:
                        support_texts.extend(str(text) for text in _iter_strings(source))
                        support_texts.extend(str(text) for text in _iter_strings(opportunity))
                elif prefix == "strategy":
                    strategy_ref_count += 1
                    topic = topics.get(value)
                    if topic is None:
                        gate.errors.append(f"{filename} semantic unit {unit_id!r} cites unknown topic {value!r}")
                    else:
                        support_texts.extend(str(text) for text in _iter_strings(topic))
                elif prefix == "section":
                    structure_ref_count += 1
                    heading = sections.get(value)
                    if heading is None or normalize_semantic_text(heading) != normalize_semantic_text(unit_text):
                        gate.errors.append(
                            f"{filename} semantic unit {unit_id!r} is not the declared heading for section {value!r}"
                        )
                elif prefix == "structure":
                    structure_ref_count += 1
                    normalized = normalize_semantic_text(unit_text)
                    valid = (
                        value == "salutation" and document_id == "cover_letter" and normalized.startswith("dear ")
                    ) or (
                        value == "heading" and document_id == "cover_letter" and normalized == "conclusion"
                    ) or (
                        value == "closing" and document_id == "cover_letter" and normalized == "sincerely"
                    )
                    if not valid:
                        gate.errors.append(
                            f"{filename} semantic unit {unit_id!r} misuses closed structural ref {ref!r}"
                        )
                else:
                    gate.errors.append(f"{filename} semantic unit {unit_id!r} has unknown support ref {ref!r}")

            if kind == "evidence":
                if not claim_ref_count or opportunity_ref_count or strategy_ref_count or structure_ref_count:
                    gate.errors.append(
                        f"{filename} evidence unit {unit_id!r} must cite one or more declared evidence claims only"
                    )
                unit_tokens = _trace_tokens(unit_text)
                support_tokens = set().union(*(_trace_tokens(text) for text in support_texts)) if support_texts else set()
                required_anchors = min(2, len(unit_tokens))
                if required_anchors and len(unit_tokens & support_tokens) < required_anchors:
                    gate.errors.append(
                        f"{filename} evidence unit {unit_id!r} lacks lexical anchors in its cited claims"
                    )
                for claim_id in unit_claim_ids:
                    if claim_id in declared_claim_ids and claim_id in claims:
                        if claims[claim_id].get("verbatim_only") is True:
                            canonical_text = normalize_semantic_text(str(claims[claim_id].get("text", "")))
                            if normalize_semantic_text(unit_text) not in canonical_text:
                                gate.errors.append(
                                    f"{filename} evidence unit {unit_id!r} is not verbatim accepted text for claim {claim_id!r}"
                                )
                        evidence_text_by_claim.setdefault(claim_id, []).append(unit_text)
            elif kind == "opportunity":
                if not opportunity_ref_count or claim_ref_count or strategy_ref_count or structure_ref_count:
                    gate.errors.append(
                        f"{filename} opportunity unit {unit_id!r} must cite official opportunity sources only"
                    )
                unit_tokens = _trace_tokens(unit_text)
                support_tokens = set().union(*(_trace_tokens(text) for text in support_texts)) if support_texts else set()
                # Opportunity prose is often line-wrapped mid-sentence; one
                # substantive anchor per physical line still prevents arbitrary
                # prose from borrowing an unrelated official source.
                required_anchors = min(1, len(unit_tokens))
                if required_anchors and len(unit_tokens & support_tokens) < required_anchors:
                    gate.errors.append(
                        f"{filename} opportunity unit {unit_id!r} lacks lexical anchors in official opportunity evidence"
                    )
            elif kind == "strategy":
                if not strategy_ref_count or opportunity_ref_count or structure_ref_count:
                    gate.errors.append(
                        f"{filename} strategy unit {unit_id!r} must cite a proposed topic and may cite evidence claims"
                    )
                unit_tokens = _trace_tokens(unit_text)
                support_tokens = set().union(*(_trace_tokens(text) for text in support_texts)) if support_texts else set()
                # Strategy units may be continuations of a paragraph. Require a
                # real anchor on every visible line without mistaking wrapping
                # for a new unsupported assertion.
                required_anchors = min(1, len(unit_tokens))
                if required_anchors and len(unit_tokens & support_tokens) < required_anchors:
                    gate.errors.append(
                        f"{filename} strategy unit {unit_id!r} lacks lexical anchors in its cited topic or evidence"
                    )
            elif kind == "structure":
                if not structure_ref_count or claim_ref_count or strategy_ref_count:
                    gate.errors.append(
                        f"{filename} structure unit {unit_id!r} must use a closed structural ref"
                    )
                if any(str(ref).startswith("structure:salutation") for ref in refs) and not opportunity_ref_count:
                    gate.errors.append(
                        f"{filename} salutation unit {unit_id!r} must also cite the official opportunity"
                    )
            else:
                gate.errors.append(f"{filename} semantic unit {unit_id!r} has unknown kind {kind!r}")

        # Document claims are coverage attestations, not merely a bag of sources.
        # Every declared claim must be visibly represented by evidence-classified
        # text, and the visible representation must retain the claim's material
        # substance. Strategy prose may cite any accepted claim as support without
        # falsely claiming that the whole source claim appears in the document.
        for claim_id in sorted(declared_claim_ids):
            canonical = claims.get(claim_id)
            if canonical is None:
                continue
            visible_texts = evidence_text_by_claim.get(claim_id, [])
            if not visible_texts:
                gate.errors.append(
                    f"{filename} declares claim {claim_id!r} but no evidence semantic unit visibly represents it"
                )
                continue
            claim_tokens = _trace_tokens(str(canonical.get("text", "")))
            visible_tokens = _trace_tokens(" ".join(visible_texts))
            if claim_tokens:
                coverage = len(claim_tokens & visible_tokens) / len(claim_tokens)
                numeric_tokens = {token for token in claim_tokens if any(character.isdigit() for character in token)}
                if coverage < 0.5 or not numeric_tokens.issubset(visible_tokens):
                    missing_numbers = sorted(numeric_tokens - visible_tokens)
                    detail = f"; missing numeric anchors {missing_numbers}" if missing_numbers else ""
                    gate.errors.append(
                        f"{filename} materially weakens declared claim {claim_id!r}: "
                        f"visible evidence retains {coverage:.0%} of substantive claim tokens{detail}"
                    )

            location_anchors = canonical.get("representation_anchors", {})
            if isinstance(location_anchors, dict):
                anchors = location_anchors.get(document_id, [])
                if isinstance(anchors, list):
                    for anchor in anchors:
                        anchor_tokens = _trace_tokens(str(anchor))
                        if anchor_tokens and not anchor_tokens.issubset(visible_tokens):
                            gate.errors.append(
                                f"{filename} claim {claim_id!r} omits required representation anchor {anchor!r}"
                            )

    def _check_evidence(self, gate: Gate) -> None:
        evidence = self.data["evidence-bundle.json"]
        sources, claims = self._evidence_maps()
        if not sources:
            gate.errors.append("Evidence bundle has no sources")
        if not claims:
            gate.errors.append("Evidence bundle has no claims")
        for claim_id, claim in claims.items():
            source_ids = claim.get("source_ids")
            if not isinstance(source_ids, list) or not source_ids:
                gate.errors.append(f"Claim {claim_id} has no source_ids")
                continue
            missing = [source_id for source_id in source_ids if source_id not in sources]
            if missing:
                gate.errors.append(f"Claim {claim_id} references missing sources: {missing}")
            derived_from = claim.get("derived_from_claim_ids", [])
            if isinstance(derived_from, list):
                unknown_parents = [parent_id for parent_id in derived_from if parent_id not in claims]
                if unknown_parents:
                    gate.errors.append(f"Claim {claim_id} derives from unknown claims: {unknown_parents}")
                if claim_id in derived_from:
                    gate.errors.append(f"Claim {claim_id} cannot derive from itself")

        conflict_ids: set[str] = set()
        for index, conflict in enumerate(require_list(evidence.get("conflicts"), "evidence.conflicts")):
            if not isinstance(conflict, dict):
                gate.errors.append(f"Evidence conflict at index {index} is not an object")
                continue
            conflict_id = str(conflict.get("id", "")).strip()
            if conflict_id in conflict_ids:
                gate.errors.append(f"Evidence conflict id is repeated: {conflict_id!r}")
            conflict_ids.add(conflict_id)
            source_ids = conflict.get("source_ids")
            if isinstance(source_ids, list):
                missing = [source_id for source_id in source_ids if source_id not in sources]
                if missing:
                    gate.errors.append(f"Evidence conflict {conflict_id!r} references missing sources: {missing}")
            if conflict.get("material") is True and conflict.get("status") == "unresolved":
                gate.errors.append(
                    f"Material evidence conflict {conflict_id!r} is unresolved: {conflict.get('impact', '')}"
                )
            if conflict.get("status") == "resolved":
                decision_source_ids = conflict.get("decision_source_ids")
                if isinstance(decision_source_ids, list):
                    missing = [source_id for source_id in decision_source_ids if source_id not in sources]
                    if missing:
                        gate.errors.append(
                            f"Evidence conflict {conflict_id!r} decision references missing sources: {missing}"
                        )
        for document_id, claim in self._document_claims():
            claim_id = claim.get("claim_id")
            if claim_id not in claims:
                gate.errors.append(f"{document_id} uses unsupported claim {claim_id!r}")
            elif normalize_semantic_text(str(claim.get("text", ""))) != normalize_semantic_text(
                str(claims[claim_id].get("text", ""))
            ):
                gate.errors.append(f"{document_id} changes the canonical text of claim {claim_id!r}")

        for filename in ("resume.json", "cover-letter.json"):
            self._check_semantic_units(gate, filename, sources, claims)

        authority_tokens: set[str] = set()
        for filename in ("evidence-bundle.json", "opportunity-brief.json", "strategy.json"):
            for text in _iter_strings(self.data[filename]):
                authority_tokens.update(_trace_tokens(text))
        for filename in ("resume.json", "cover-letter.json"):
            semantic_text = self.data[filename].get("semantic_text")
            if not isinstance(semantic_text, str):
                continue
            for line in _unsupported_high_consequence_lines(semantic_text, authority_tokens):
                gate.errors.append(
                    f"{filename} contains a high-consequence assertion without accepted evidence anchors: {line!r}"
                )

    def _check_coverage(self, gate: Gate) -> None:
        _, claims = self._evidence_maps()
        ledger = self.data["coverage-ledger.json"]
        entries = {entry["claim_id"]: entry for entry in require_list(ledger.get("entries"), "coverage.entries")}
        content_locations: dict[str, set[str]] = {}
        for document_id, claim in self._document_claims():
            content_locations.setdefault(str(claim.get("claim_id")), set()).add(document_id)

        accepted = {"retained", "meaning_preserving_rewording", "merged"}
        for claim_id, claim in claims.items():
            required_in = claim.get("required_in", [])
            entry = entries.get(claim_id)
            if entry is None:
                gate.errors.append(f"Evidence claim {claim_id} is absent from the coverage ledger")
                continue
            status = entry.get("status")
            if status == "approved_omission":
                if entry.get("approved_by_user") is not True:
                    gate.errors.append(f"Claim {claim_id} is omitted without explicit user approval")
                continue
            if status not in accepted:
                gate.errors.append(f"Claim {claim_id} has non-releasable coverage status {status!r}")
            if claim.get("protected") and entry.get("strength_preserved") is not True:
                gate.errors.append(f"Protected claim {claim_id} lacks strength_preserved=true")
            final_locations = set(entry.get("final_locations", []))
            actual_locations = content_locations.get(claim_id, set())
            if final_locations != actual_locations:
                gate.errors.append(
                    f"Claim {claim_id} ledger locations {sorted(final_locations)} do not match "
                    f"canonical locations {sorted(actual_locations)}"
                )
            for document_id in required_in:
                if document_id not in final_locations or document_id not in content_locations.get(claim_id, set()):
                    gate.errors.append(f"Claim {claim_id} is required in {document_id} but is not present there")

    def _check_provenance(self, gate: Gate) -> None:
        evidence = self.data["evidence-bundle.json"]
        gate.errors.extend(conflicting_provenance_requirements(evidence))
        gate.errors.extend(manual_check_failures(self.data["review-record.json"], "provenance"))
        _, claims = self._evidence_maps()
        required_parents = {
            item["child_entity_id"]: item["parent_entity_id"]
            for item in require_list(evidence.get("provenance_requirements", []), "evidence.provenance_requirements")
        }
        for document_id, content_claim in self._document_claims():
            claim_id = content_claim.get("claim_id")
            canonical = claims.get(claim_id)
            if canonical is None:
                continue
            if content_claim.get("parent_entity_id") != canonical.get("parent_entity_id"):
                gate.errors.append(f"{document_id} claim {claim_id} changes its parent entity")
            entity_id = content_claim.get("entity_id")
            if entity_id in required_parents and content_claim.get("parent_entity_id") != required_parents[entity_id]:
                gate.errors.append(
                    f"{document_id} claim {claim_id} assigns {entity_id} to {content_claim.get('parent_entity_id')}; "
                    f"expected {required_parents[entity_id]}"
                )

    def _check_opportunity(self, gate: Gate) -> None:
        brief = self.data["opportunity-brief.json"]
        strategy = self.data["strategy.json"]
        _, claims = self._evidence_maps()
        if not require_list(brief.get("sources"), "opportunity.sources"):
            gate.errors.append("Opportunity brief has no primary sources")
        if not require_list(brief.get("audiences"), "opportunity.audiences"):
            gate.errors.append("Opportunity brief has no audiences")
        if not require_list(brief.get("selection_criteria"), "opportunity.selection_criteria"):
            gate.errors.append("Opportunity brief has no selection criteria")
        topics = require_list(strategy.get("proposed_topics"), "strategy.proposed_topics")
        if not topics:
            gate.errors.append("Strategy has no proposed topics")
        for topic in topics:
            topic_id = topic.get("id", "<unknown>")
            evidence_ids = topic.get("evidence_claim_ids")
            outcomes = topic.get("attendee_outcomes")
            if not isinstance(evidence_ids, list) or not evidence_ids:
                gate.errors.append(f"Topic {topic_id} has no evidence_claim_ids")
            elif unknown := [claim_id for claim_id in evidence_ids if claim_id not in claims]:
                gate.errors.append(f"Topic {topic_id} cites unknown claims: {unknown}")
            if not isinstance(outcomes, list) or not outcomes:
                gate.errors.append(f"Topic {topic_id} has no attendee outcomes")

    def _check_content(self, gate: Gate) -> None:
        for filename in ("resume.json", "cover-letter.json"):
            document = self.data[filename]
            semantic_text = document.get("semantic_text")
            if not isinstance(semantic_text, str) or not normalize_semantic_text(semantic_text):
                gate.errors.append(f"{filename} has no canonical semantic_text")
            claim_ids: set[str] = set()
            for claim in require_list(document.get("claims"), f"{filename}.claims"):
                claim_id = claim.get("claim_id")
                if claim_id in claim_ids:
                    gate.errors.append(f"{filename} repeats claim {claim_id}")
                claim_ids.add(claim_id)
                if not isinstance(claim.get("text"), str) or not claim["text"].strip():
                    gate.errors.append(f"{filename} claim {claim_id} has empty text")
        gate.errors.extend(outline_findings(self.data["resume.json"]))
        gate.errors.extend(verb_variety_findings(self.data["resume.json"]))

    def _check_design(self, gate: Gate) -> None:
        design = self.data["design-contract.json"]
        elements = require_list(design.get("visible_elements"), "design.visible_elements")
        if not elements:
            gate.errors.append("Design contract has no visible elements")
        seen: set[tuple[str, str]] = set()
        forbid_numbers = self.manifest["constraints"]["forbid_page_numbers"]
        for element in elements:
            key = (str(element.get("document_id")), str(element.get("element_id")))
            if key in seen:
                gate.errors.append(f"Duplicate visible element identifier {key}")
            seen.add(key)
            if not isinstance(element.get("reader_purpose"), str) or not element["reader_purpose"].strip():
                gate.errors.append(f"Visible element {key} has no reader purpose")
            if forbid_numbers and element.get("function") == "page_number":
                gate.errors.append(f"Page number element {key} is forbidden")
        gate.errors.extend(design_findings(design, str(self.data["cover-letter.json"].get("semantic_text", ""))))

    def _render_artifacts(self) -> dict[str, dict[str, Any]]:
        render = self.data["render-manifest.json"]
        return {item["id"]: item for item in require_list(render.get("artifacts"), "render.artifacts")}

    def _check_layout(self, gate: Gate) -> None:
        artifacts = self._render_artifacts()
        expected = self.manifest["constraints"]["page_counts"]
        for artifact_id, document_id in (
            ("resume_pdf", "resume"),
            ("resume_docx", "resume"),
            ("cover_letter_pdf", "cover_letter"),
            ("cover_letter_docx", "cover_letter"),
        ):
            item = artifacts.get(artifact_id)
            if item is None:
                gate.errors.append(f"Render manifest lacks {artifact_id}")
                continue
            if item.get("pages") != expected[document_id]:
                gate.errors.append(
                    f"{artifact_id} has {item.get('pages')} pages; expected {expected[document_id]}"
                )
            page_images = item.get("page_images")
            if not isinstance(page_images, list) or len(page_images) != expected[document_id]:
                gate.errors.append(f"{artifact_id} lacks exact render evidence for every page")
                continue
            for page_number, page in enumerate(page_images, start=1):
                if page.get("page") != page_number:
                    gate.errors.append(f"{artifact_id} render evidence has non-contiguous page numbers")
                    continue
                page_path = (self.audit / str(page.get("path", ""))).resolve()
                try:
                    page_path.relative_to(self.audit.resolve())
                except ValueError:
                    gate.errors.append(f"{artifact_id} render evidence escapes audit directory")
                    continue
                if not page_path.is_file():
                    gate.errors.append(f"{artifact_id} rendered page {page_number} is missing")
                    continue
                if sha256_file(page_path) != page.get("sha256"):
                    gate.errors.append(f"{artifact_id} rendered page {page_number} hash changed")
                if page_path.stat().st_size != page.get("bytes"):
                    gate.errors.append(f"{artifact_id} rendered page {page_number} byte count changed")
            if item.get("format") == "docx":
                document_path = self.candidate / str(item.get("filename", ""))
                for finding in docx_visual_findings(document_path, expected_pages=expected[document_id]):
                    gate.errors.append(f"{artifact_id}: {finding}")
            document_path = self.candidate / str(item.get("filename", ""))
            for finding in atomic_phrase_findings(
                document_path,
                str(item.get("format", "")),
                [
                    phrase.get("text", "")
                    for phrase in self.data["design-contract.json"].get("atomic_phrases", [])
                    if isinstance(phrase, dict) and phrase.get("document_id") == document_id
                ],
            ):
                gate.errors.append(f"{artifact_id}: {finding}")
        visual_review = self.data["review-record.json"].get("visual_review", {})
        if visual_review.get("all_pages_inspected") is not True:
            gate.errors.append("Review record does not confirm inspection of every rendered page")
        if visual_review.get("blocking_defects") not in ([], None):
            gate.errors.append("Visual review contains blocking defects")
        gate.errors.extend(manual_check_failures(self.data["review-record.json"], "layout"))

    def _check_parity(self, gate: Gate) -> None:
        artifacts = self._render_artifacts()
        for document_id in ("resume", "cover_letter"):
            pdf = artifacts.get(f"{document_id}_pdf")
            docx = artifacts.get(f"{document_id}_docx")
            if not pdf or not docx:
                gate.errors.append(f"Missing PDF or DOCX metadata for {document_id}")
                continue
            if pdf.get("semantic_text_sha256") != docx.get("semantic_text_sha256"):
                gate.errors.append(f"PDF and DOCX semantic text differ for {document_id}")
            if pdf.get("external_links") != docx.get("external_links"):
                gate.errors.append(f"PDF and DOCX external links differ for {document_id}")
            if (
                pdf.get("emphasis_sha256") != docx.get("emphasis_sha256")
                or pdf.get("emphasis_word_count") != docx.get("emphasis_word_count")
            ):
                gate.errors.append(f"PDF and DOCX semantic emphasis differs for {document_id}")
            canonical = self.data["resume.json" if document_id == "resume" else "cover-letter.json"]
            expected_hash = sha256_bytes(normalize_semantic_text(canonical["semantic_text"]).encode("utf-8"))
            if pdf.get("semantic_text_sha256") != expected_hash:
                gate.errors.append(f"Rendered {document_id} does not match canonical semantic_text")
            for item in (pdf, docx):
                artifact_id = str(item.get("id", f"{document_id}_artifact"))
                accessibility = item.get("accessibility")
                if not isinstance(accessibility, dict) or accessibility.get("checked") is not True:
                    gate.errors.append(f"{artifact_id} lacks derived accessibility evidence")
                    continue
                if accessibility.get("encrypted") is not False:
                    gate.errors.append(f"{artifact_id} is encrypted and not independently readable")
                if accessibility.get("text_extractable") is not True:
                    gate.errors.append(f"{artifact_id} has no extractable reading order")
                if not str(accessibility.get("document_title", "")).strip():
                    gate.errors.append(f"{artifact_id} has no accessible document title")
                if accessibility.get("external_link_targets_valid") is not True:
                    gate.errors.append(f"{artifact_id} has an invalid external link target")
                if accessibility.get("nontext_alt_text_complete") is not True:
                    gate.errors.append(f"{artifact_id} has nontext content without alternative text")
                if accessibility.get("reading_order_sha256") != item.get("semantic_text_sha256"):
                    gate.errors.append(f"{artifact_id} accessibility reading order is stale")
        gate.errors.extend(manual_check_failures(self.data["review-record.json"], "parity"))

    def _check_changes(self, gate: Gate) -> None:
        changes = self.data["change-set.json"]
        for change in require_list(changes.get("changes"), "changes.changes"):
            if not isinstance(change.get("target_ids"), list) or not change["target_ids"]:
                gate.errors.append(f"Change {change.get('id')} has no target_ids")
            if not isinstance(change.get("invalidates"), list):
                gate.errors.append(f"Change {change.get('id')} has no invalidates list")
        for region in require_list(changes.get("accepted_regions", []), "changes.accepted_regions"):
            if not isinstance(region.get("artifact_id"), str) or not isinstance(region.get("sha256"), str):
                gate.errors.append("Accepted region lacks artifact_id or sha256")
        page_hashes = [
            str(page.get("sha256"))
            for artifact in self._render_artifacts().values()
            for page in artifact.get("page_images", [])
        ]
        gate.errors.extend(change_findings(changes, page_hashes))

    def _check_review(self, gate: Gate) -> None:
        review = self.data["review-record.json"]
        evidence = self.data["review-evidence.json"]
        artifacts = self._render_artifacts()
        mode = review.get("mode")
        if mode not in {"cross_model", "disclosed_fallback"}:
            gate.errors.append(f"Unknown review mode {mode!r}")
        if mode == "disclosed_fallback":
            if not self.manifest["review_policy"]["allow_disclosed_fallback"]:
                gate.errors.append("Fallback review is not allowed by the manifest")
            if review.get("fallback_disclosed") is not True:
                gate.errors.append("Fallback review is not disclosed")
        if evidence.get("review_mode") != mode:
            gate.errors.append("External review evidence mode differs from the review record")
        evidence_reference = review.get("external_review_evidence")
        evidence_path = self.audit / "review-evidence.json"
        if not isinstance(evidence_reference, dict):
            gate.errors.append("Review record does not reference external review evidence")
        elif (
            evidence_reference.get("path") != "review-evidence.json"
            or evidence_reference.get("sha256") != sha256_file(evidence_path)
        ):
            gate.errors.append("External review evidence reference is stale or missing")
        primary_reviewer = evidence.get("primary_reviewer")
        if not isinstance(primary_reviewer, dict) or review.get("provider") != primary_reviewer.get("provider"):
            gate.errors.append("Review provider differs from the external reviewer identity")
        reviewed = require_mapping(review.get("artifact_hashes"), "review.artifact_hashes")
        reviewed_pages = require_mapping(review.get("page_image_hashes"), "review.page_image_hashes")
        evidence_artifacts = require_mapping(evidence.get("artifact_hashes"), "review_evidence.artifact_hashes")
        evidence_pages = require_mapping(evidence.get("page_image_hashes"), "review_evidence.page_image_hashes")
        evidence_inputs = require_mapping(
            evidence.get("reviewed_input_hashes"),
            "review_evidence.reviewed_input_hashes",
        )
        expected_review_packet = review_packet_sha256(
            evidence_artifacts,
            evidence_pages,
            evidence_inputs,
        )
        if evidence.get("review_packet_sha256") != expected_review_packet:
            gate.errors.append("External review packet digest is stale or missing")
        for artifact_id in ARTIFACT_IDS:
            actual = artifacts.get(artifact_id, {}).get("sha256")
            if reviewed.get(artifact_id) != actual:
                gate.errors.append(f"Review hash is stale or missing for {artifact_id}")
            if evidence_artifacts.get(artifact_id) != actual:
                gate.errors.append(f"External review evidence hash is stale or missing for {artifact_id}")
            current_pages = [
                page.get("sha256")
                for page in artifacts.get(artifact_id, {}).get("page_images", [])
            ]
            if reviewed_pages.get(artifact_id) != current_pages:
                gate.errors.append(f"Review page hashes are stale or missing for {artifact_id}")
            if evidence_pages.get(artifact_id) != current_pages:
                gate.errors.append(f"External review page hashes are stale or missing for {artifact_id}")
        exchanges = evidence.get("exchanges")
        if not isinstance(exchanges, list) or len(exchanges) < 2:
            gate.errors.append("External review evidence lacks reciprocal request/response transcripts")
        else:
            for index, exchange in enumerate(exchanges):
                if not isinstance(exchange, dict):
                    gate.errors.append(f"External review exchange {index} is malformed")
                    continue
                request = exchange.get("request")
                response = exchange.get("response")
                if not isinstance(request, str) or sha256_bytes(request.encode("utf-8")) != exchange.get("request_sha256"):
                    gate.errors.append(f"External review exchange {index} has a stale request transcript hash")
                if exchange.get("review_packet_sha256") != expected_review_packet:
                    gate.errors.append(f"External review exchange {index} is bound to a different review packet")
                if not isinstance(request, str) or expected_review_packet not in request:
                    gate.errors.append(
                        f"External review exchange {index} request does not identify the current review packet"
                    )
                if not isinstance(response, str) or sha256_bytes(response.encode("utf-8")) != exchange.get("response_sha256"):
                    gate.errors.append(f"External review exchange {index} has a stale response transcript hash")
                if exchange.get("verdict") != "pass":
                    gate.errors.append(f"External review exchange {index} did not pass")
            reciprocal = evidence.get("reciprocal_review")
            if not isinstance(reciprocal, dict) or reciprocal.get("completed") is not True:
                gate.errors.append("Reciprocal review is not complete")
            else:
                primary_index = reciprocal.get("primary_exchange_index")
                reciprocal_index = reciprocal.get("reciprocal_exchange_index")
                if not isinstance(primary_index, int) or not isinstance(reciprocal_index, int) or not (
                    0 <= primary_index < len(exchanges) and 0 <= reciprocal_index < len(exchanges)
                ):
                    gate.errors.append("Reciprocal review exchange indices are invalid")
                elif primary_index == reciprocal_index:
                    gate.errors.append("Primary and reciprocal review must use distinct exchanges")
                else:
                    primary = exchanges[primary_index]
                    reciprocal_exchange = exchanges[reciprocal_index]
                    if isinstance(primary_reviewer, dict) and primary.get("reviewer_provider") != primary_reviewer.get("provider"):
                        gate.errors.append("Primary exchange reviewer differs from the declared reviewer")
                    if (
                        reciprocal_exchange.get("requester_provider") != primary.get("reviewer_provider")
                        or reciprocal_exchange.get("reviewer_provider") != primary.get("requester_provider")
                    ):
                        gate.errors.append("Reciprocal exchange does not reverse the primary reviewer relationship")
                    if mode == "cross_model" and primary.get("requester_provider") == primary.get("reviewer_provider"):
                        gate.errors.append("Cross-model review was not performed by a distinct provider")
        if evidence.get("verdict") != "pass":
            gate.errors.append("External review evidence verdict is not pass")
        evidence_unresolved = evidence.get("unresolved_findings")
        if not isinstance(evidence_unresolved, list) or evidence_unresolved:
            gate.errors.append("External review evidence has unresolved findings")
        unresolved = review.get("unresolved_findings")
        if not isinstance(unresolved, list) or unresolved:
            gate.errors.append("Review has unresolved findings")
        gate.errors.extend(reviewed_input_findings(review, self.audit, sha256_file))
        gate.errors.extend(reviewed_input_findings(evidence, self.audit, sha256_file))

    def _check_state(self, gate: Gate) -> None:
        stage_records = self.state.get("stages")
        if not isinstance(stage_records, dict):
            gate.errors.append("Run state has no stage records")
            return
        previous_output_hashes: dict[str, str] = {}
        for stage_name, filenames in (
            ("evidence", ("evidence-bundle.json",)),
            ("opportunity", ("opportunity-brief.json",)),
            ("positioning", ("strategy.json",)),
            ("resume", ("resume.json", "coverage-ledger.json")),
            ("pitch", ("cover-letter.json",)),
            ("design", ("design-contract.json",)),
            ("changes", ("change-set.json",)),
            ("render", ("render-manifest.json",)),
            ("review", ("review-evidence.json", "review-record.json")),
        ):
            record = stage_records.get(stage_name)
            if not isinstance(record, dict) or record.get("status") != "complete":
                gate.errors.append(f"Stage {stage_name} is incomplete")
                continue
            if record.get("input_hashes") != previous_output_hashes:
                gate.errors.append(f"Stage {stage_name} has stale input hashes")
            current: dict[str, str] = {}
            for filename in filenames:
                path = self.audit / filename
                if path.exists():
                    current[filename] = sha256_file(path)
            if record.get("output_hashes") != current:
                gate.errors.append(f"Stage {stage_name} output hashes do not match current files")
            previous_output_hashes.update(current)

    def _check_artifacts(self, gate: Gate) -> None:
        artifacts = self._render_artifacts()
        expected_final: dict[str, str] = {}
        for artifact_id in ARTIFACT_IDS:
            item = artifacts.get(artifact_id)
            if item is None:
                gate.errors.append(f"Missing required artifact {artifact_id}")
                continue
            path = self.candidate / item["filename"]
            if not path.is_file():
                gate.errors.append(f"Candidate artifact file is missing: {path.name}")
                continue
            if sha256_file(path) != item.get("sha256"):
                gate.errors.append(f"Candidate artifact hash changed: {artifact_id}")
            expected_final[item["filename"]] = item.get("sha256")
        candidate_files = {path.name for path in self.candidate.iterdir() if path.is_file()}
        candidate_entries = {path.name for path in self.candidate.iterdir()}
        if candidate_entries != set(expected_final) or candidate_files != set(expected_final):
            gate.errors.append("candidate/ does not contain exactly the four hash-bound submission artifacts")
        final = self.run_dir / "final"
        if self.state.get("status") == "released" and not final.is_dir():
            gate.errors.append("Run state is released but final/ is missing")
        if final.exists():
            final_entries = list(final.iterdir())
            actual_final = {path.name: sha256_file(path) for path in final_entries if path.is_file()}
            if (
                len(final_entries) != len(expected_final)
                or any(not path.is_file() for path in final_entries)
                or actual_final != expected_final
            ):
                gate.errors.append("final/ does not contain exactly the four hash-bound submission artifacts")

    def _report(self) -> dict[str, Any]:
        passed = sum(gate.passed for gate in self.gates)
        total = len(self.gates)
        status = "pass" if total and passed == total else "fail"
        score = 100 if status == "pass" else round((100 * passed / total), 2) if total else 0
        artifacts: dict[str, str] = {}
        render = self.data.get("render-manifest.json")
        if isinstance(render, dict):
            for item in render.get("artifacts", []):
                if isinstance(item, dict) and item.get("id") and item.get("sha256"):
                    artifacts[item["id"]] = item["sha256"]
        return {
            "schema_version": SCHEMA_VERSION,
            "run_id": self.manifest.get("run_id"),
            "status": status,
            "score": score,
            "all_gates_required": True,
            "gates": [gate.as_dict() for gate in self.gates],
            "artifact_hashes": artifacts,
        }


def validate_release(run_dir: Path, manifest: dict[str, Any], state: dict[str, Any]) -> dict[str, Any]:
    return ReleaseValidator(run_dir, manifest, state).validate()
