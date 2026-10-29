---
name: application-package
description: Build and release a complete opportunity-specific application package from evidence and research through verified PDF and DOCX artifacts. Use when the user wants a resume plus cover letter, speaker proposal, or similarly consequential application package completed in one interaction. Requires a tool-capable host; use a drafting skill for text-only requests.
---

# Application Package

Own orchestration, convergence, and release. The stage skills own evidence, strategy, writing, composition, change control, and audit decisions.

## Run the package

1. Translate the user's request into a `run-manifest.json` that conforms to the repository schema. Preserve every supplied source, constraint, correction, referral detail, and requested format. Resolve a profile identifier through the explicit path, `APPLICATION_PACK_CONFIG`, or `~/.config/application-pack/profiles.json`, then load defaults from `<profile-root>/profile/profile.json` before asking for information. Write the resolved absolute profile path into the manifest.
2. Run `application-pack capabilities --profile <profile-root>`. A missing capability may narrow what can be verified; record it instead of claiming work occurred.
3. Start or resume with `application-pack run <run-manifest>`. Treat the run directory named in the manifest as authoritative state.
4. Exit code `4` means the CLI wrote `<run>/next-action.json` for a model-owned stage. Load its named stage skill, validate the declared inputs, produce only the requested schema artifact, and call the same `run` command again. Repair a failure in its owning stage rather than rewriting downstream artifacts.
5. Continue while artifacts change or findings close. If the same finding and artifact hashes recur twice, preserve the best candidate and return the CLI's precise blocker.
6. Deliver only files promoted to `final/`. Keep ledgers, renders, hashes, and reviewer records in `audit/`.

## Release boundary

A package is complete only when `application-pack validate <run-dir>` succeeds, `release-report.json` says `released`, every hard gate passes, and the report hashes match the files in `final/`. A reviewer score cannot override a deterministic or visible defect.

Ask the user only for a material source conflict, inaccessible essential evidence, a genuinely required unknown field, or a hard constraint that would remove protected evidence. Never expose partial artifacts as final.
