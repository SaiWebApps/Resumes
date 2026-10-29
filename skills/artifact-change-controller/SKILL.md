---
name: artifact-change-controller
description: Apply a targeted correction to an application package while preserving accepted content and pixels outside the affected dependency region. Use for follow-up edits, annotated-document comments, frozen sections, or regression-sensitive revisions. Do not reopen settled work without a factual dependency.
---

# Artifact Change Controller

Turn corrections into durable, bounded change directives.

1. Identify the exact target semantic identifiers, requested outcome, evidence source, and affected stage.
2. Record the correction in the append-only change ledger. When it changes a durable fact, route it to the profile correction ledger before regenerating content.
3. Compute downstream dependencies and invalidate only affected stage hashes and approvals.
4. Freeze accepted regions by semantic text and rendered pixels. Permit collateral change only when a documented dependency requires it.
5. Rebuild through the owning stage, compare text and pixels outside the target, and emit schema-valid `change-set.json`. Record frozen-region hashes in its `accepted_regions`; keep the detailed comparison evidence in `audit/` without inventing a second stage contract.

Completion requires the requested change to be present, every required dependent artifact to be fresh, and every unaffected accepted region to match. A local patch without a durable guard is incomplete.
