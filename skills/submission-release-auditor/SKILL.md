---
name: submission-release-auditor
description: Decide whether the exact current application artifacts are releasable by checking evidence coverage, provenance, writing, layout, parity, accessibility, change isolation, and reviewer resolution. Use only on release candidates or after a rebuild. Do not repair artifacts inside the audit.
---

# Submission Release Auditor

Audit the exact bytes proposed for release. Findings route back to their owning stage.

1. Verify schemas, stage input/output hashes, source freshness, current artifact hashes, every PDF and DOCX page-image hash, and invalidation state.
2. Require complete evidence coverage, protected-claim strength, correct provenance, opportunity fit, persuasive distinctness, and zero unsupported claims.
3. Inspect every current PDF and DOCX render at reading scale and in continuous view. Fail purposeless elements, unreadable density, avoidable blank blocks, hierarchy defects, page-number clutter, or stale accepted-region changes.
4. Require cross-format semantic parity, working links, accessibility checks, and exact final filenames. Treat the engine-derived text-order, external-link, emphasis, title, encryption, extraction, and nontext-alt evidence as mandatory; a reviewer boolean cannot replace it.
5. Build one canonical review packet from the exact `artifact_hashes`, `page_image_hashes`, and reviewed-input hashes. Put its SHA-256 digest in every primary and reciprocal request, then send the exact artifacts, current rendered pages, and evidence packet to a distinct model when available. Save both request and response transcripts with their hashes and that packet digest in schema-valid `review-evidence.json`. If a distinct model is unavailable, use the same evidence contract for a disclosed same-model adversarial review; deterministic gates remain mandatory.
6. Resolve every reviewer finding as accepted, repaired, or rejected with evidence. Any rebuild invalidates the prior review.
7. Emit schema-valid `review-record.json` bound to the current four artifact hashes and the exact `review-evidence.json` hash. Then rerun the orchestrator; the engine copies both review artifacts into `audit/` and alone emits `release-report.json` with binary hard gates, reviewer mode, artifact hashes, unresolved findings, and `released` or `blocked` status.

Release requires every hard gate to pass. A numeric score, deadline pressure, or reviewer approval cannot overrule a visible or deterministic defect.
