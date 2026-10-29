---
name: document-compositor
description: Render approved structured application content into visually verified PDF and DOCX artifacts under a semantic design contract. Use after content approval or for layout-only repairs. Do not rewrite, delete, or weaken claims to make a page fit.
---

# Document Compositor

Own composition and format parity while keeping content immutable.

1. Validate the canonical content and `design-contract.json`; refuse stale or schema-invalid inputs.
2. Map every visible element to a semantic function such as identity, contact, section heading, entry title, metadata, body, proposal heading, salutation, or signature.
3. Build PDF and DOCX from the same canonical source. Use typography, spacing, flow, and legitimate page breaks to meet real constraints without editing claim text.
4. Use [`scripts/render_artifacts.py`](scripts/render_artifacts.py) or the equivalent host hook to render every PDF and DOCX page and hash the exact page images. Run its `capabilities` command first, then `render` with an `--artifact ID=PATH` entry and `--expected-pages ID=COUNT` for every deliverable. Write the result to the manifest's `stage_sources.render_evidence` path as schema-valid `render-evidence.json`; it must include the SHA-256 identity of both renderer programs. The engine independently executes those exact renderers against the candidate bytes, rejects page images that do not match the fresh render, then freezes the verified pages into `audit/render-manifest.json`.
5. Inspect every hashed page at reading scale and in continuous-page view. Check hierarchy, balance, usable density, orphans, split bullets, clipping, substitution, conspicuous gaps, and purpose of every decorative element.
6. Compare PDF and DOCX text, hierarchy, emphasis, links, and ordering. Return a structured layout conflict if the content cannot fit readably within the stated constraint.
7. Emit final candidates, page renders, accessibility results, and hash-bound `render-evidence.json`. The engine, not the compositor, creates the release run's `render-manifest.json` after verifying the artifact and page-image hashes.

Completion requires clean renders for every page and semantic parity between formats. A compositor never trades evidence for whitespace or labels an uninspected file final.
