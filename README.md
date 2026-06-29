# Resumes

Backup and working set for iterating on Sairam Krishnan's résumé with Claude.
Clone this, point a fresh Claude session at it, and pick up where the last one left
off. Self-contained on purpose: time-sensitive research is regenerated, not stored.

## Layout

- `resume/` — the current résumé: `Sairam_Krishnan_Resume_content.json` (the source
  of truth), `build_resume.js` + `package.json` (the builder), and the rendered
  `Sairam_Krishnan_Resume.pdf`.
- `skill/` — the `career-brand-forge` Claude skill: the unpacked source and the
  installable `career-brand-forge.skill`. It carries all the rules (voice, integrity,
  no-pronoun, tense, ordering, layout) and the procedures to regenerate anything
  time-sensitive.
- `context/` — the durable inputs a fresh session should read first: the
  professional dossier (the verified fact ledger) and the LinkedIn capture.
- `legacy/` — the older résumé.

## Resume a Claude session

1. Connect this folder in Claude.
2. Install the skill (`skill/career-brand-forge.skill` via Settings → Capabilities),
   or just have Claude read `skill/career-brand-forge/SKILL.md`.
3. Tell Claude to read `context/` first. `Sai_Professional_Dossier.md` is the
   verified fact ledger; never invent a number that is not in it.
4. Iterate on `resume/Sairam_Krishnan_Resume_content.json` and rebuild.

## Rebuild the PDF

```bash
cd resume
npm install docx
node build_resume.js Sairam_Krishnan_Resume_content.json Sairam_Krishnan_Resume.docx
soffice --headless --convert-to pdf Sairam_Krishnan_Resume.docx   # LibreOffice
```

The builder keeps the résumé to a clean two pages, controls page-break orphans, and
supports an optional bold `target` line on the profile. Page-fit knobs live in the
content JSON `style` block (see `skill/career-brand-forge/references/resume_playbook.md`).

## Refresh the time-sensitive material

Compensation, market keywords, target-role profiles, and critique notes are **not**
stored here on purpose: they go stale and some are sensitive. Regenerate them with
`skill/career-brand-forge/references/refresh_and_research.md`.
