# Application Package

Application Package turns one opportunity prompt into a source-backed, hash-bound résumé and cover-letter package. It keeps evidence, positioning, writing, composition, change control, and release review separate so a layout repair cannot silently rewrite a career record.

The public repository contains the model-neutral engine and nine portable Agent Skills. Personal evidence belongs in a separate private profile repository.

## What a successful run produces

`final/` contains exactly four submission files:

- résumé PDF;
- résumé DOCX;
- cover-letter PDF;
- cover-letter DOCX.

`audit/` contains the evidence bundle, opportunity brief, positioning strategy, coverage ledger, design contract, change set, render manifest, hash-bound page evidence, external review transcript evidence, exact-artifact review record, and release report. A failed gate leaves candidates outside `final/`.

## Install

Use Python 3.11 or newer.

```bash
python -m pip install -e .
python scripts/install_skills.py --target codex
python scripts/install_skills.py --target claude
python scripts/install_skills.py --target chatgpt
python scripts/install_skills.py --target generic
```

The installer links the same canonical skills into Codex and Claude by default. The ChatGPT front-door archive contains the engine and schemas. The generic target creates a self-contained bundle with all skills, source, schemas, package metadata, and a `bin/application-pack` launcher. Use `--mode copy` when symlinks are inappropriate and `--force` to preserve an existing installation in a timestamped backup before replacement.

For Claude Code, the installer honors `CLAUDE_CONFIG_DIR` before falling back to `~/.claude`; this preserves intentionally isolated personal or work configurations.

## Run

The `application-package` skill is the only user-facing entrypoint. It converts the request into a typed run manifest and resumes the same command until every stage exists and the release gate passes.

```bash
application-pack capabilities --profile /path/to/private-profile
application-pack run /path/to/run-manifest.json
application-pack validate /path/to/run-directory
```

An orchestrator may resolve a profile identifier from `~/.config/application-pack/profiles.json` (or the file named by `APPLICATION_PACK_CONFIG`) before writing the explicit profile path into the run manifest.

Exit code `4` writes `next-action.json` naming the single stage skill and contract the agent must complete. Exit code `2` reports a failed release gate. Repeating an unchanged failure and unchanged candidate produces the no-progress blocker instead of an endless loop.

## Skill boundaries

- `application-package` orchestrates the run and promotion.
- `career-evidence` establishes facts, sources, protection, and provenance.
- `opportunity-auditor` determines what the recipient is deciding.
- `application-positioner` selects the strongest supported narrative.
- `resume-author` writes canonical résumé content and coverage.
- `speaker-pitch-author` writes the cover letter and proposed sessions.
- `document-compositor` renders and inspects PDF and DOCX without editing claims.
- `artifact-change-controller` applies bounded corrections and freezes accepted regions.
- `submission-release-auditor` decides whether the exact bytes are releasable.

All handoffs use versioned JSON Schemas under `schemas/`. The compositor emits hash-bound `render-evidence.json` for every PDF and DOCX page, including the SHA-256 identities of the renderer programs. The reviewer emits `review-evidence.json` with hash-bound request/response transcripts, exact artifact, page, and input hashes, one canonical review-packet digest named in every request, and reciprocal-review metadata; `review-record.json` references those evidence bytes. The engine independently reruns the renderers against the candidate bytes, rejects unrelated or stale page images, freezes the verified renders, records stage input and output hashes, invalidates stale approvals, compares PDF and DOCX semantic text, external links, and emphasis, derives accessibility evidence from each artifact structure, enforces page constraints, and promotes only a passing four-file candidate.

## Private profiles

A profile supplies the accepted baseline, evidence graph, source manifest, protected claims, provenance rules, append-only corrections, and opportunity fixtures. The engine expects the entrypoint at `<profile-root>/profile/profile.json`.

Do not commit real professional records, source documents, or private regression fixtures to this public repository. Public tests use synthetic evidence only.

## Verify

```bash
python -m unittest discover -s tests/synthetic -v
python scripts/validate_skill.py skills/application-package
```

The synthetic suite covers unsupported semantic assertions, protected-claim loss, provenance errors, purposeless elements, page numbers, wrong PDF and DOCX page counts, stale artifact and page-image reviews, visual mutations, DOCX metadata integrity, atomic title separators, external reciprocal review evidence, format drift, schema violations, partial promotion, no-progress handling, and one executable mutation regression for each recorded failure class.

The complete pre-migration implementation remains recoverable at the immutable `pre-application-suite-2026-10-28` tag. A sanitized executable snapshot is archived under `legacy/career-brand-forge/`; personal examples from the original are intentionally absent from the active public branch.
