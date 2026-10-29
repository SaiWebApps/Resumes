# Résumé Playbook

How to build a dense, ATS-safe, two-full-page executive résumé with the bundled
`scripts/build_resume.js`.

## Workflow

0. **Read everything that already exists, first.** Before drafting a word, read the
   project folder end to end: the fact ledger / dossier, any prior critiques or
   verification reports, the current résumé, and especially the person's LinkedIn
   "About" (the truest source of their voice, arc, and facts). Do not re-derive
   rules or re-discover facts that are already written down. Skipping this is the
   single biggest time-sink and makes you re-make mistakes a prior pass already
   caught.
1. **Start from what exists.** If the person has a résumé they like, use its
   structure as the base. Do not reinvent a layout they are comfortable with;
   reconcile and sharpen it. Pull content from their LinkedIn and the fact ledger.
   Get their hard constraints and any exemplar up front (see "Get the spec up
   front" below).
2. **Draft the content into JSON.** Put the substance into a content file matching
   the schema below (copy `scripts/resume_content.example.json` and edit). Keeping
   content as data means you tune wording without touching layout code.
3. **Build.** From `scripts/`:
   ```bash
   npm install docx        # once
   node build_resume.js my_content.json /path/to/output.docx
   ```
4. **Render and look at it.** A docx does not reliably report page count; render to
   PDF and inspect. With the `docx` skill's office tools available:
   ```bash
   python3 .../skills/docx/scripts/office/soffice.py --headless \
     --convert-to pdf --outdir /tmp output.docx
   python3 -c "from pypdf import PdfReader; print(len(PdfReader('/tmp/output.pdf').pages))"
   pdftoppm -jpeg -r 100 /tmp/output.pdf /tmp/pg   # then view pg-1.jpg, pg-2.jpg
   ```
   If `pdftoppm` is missing: `apt-get install -y poppler-utils`.
5. **Read it as a recruiter, then tune.** Two *full* pages is the target, not "two
   pages, the second a third full." See page-fit knobs below.

## The "two full pages" standard

Two full pages is the brief for a senior or executive candidate: enough room to
show scope without sprawling to three. The common failure modes:

- **Overflow to a third page.** A few lines spill over. Fix: trim a weak bullet,
  tighten wording, or shave spacing. Cutting one mediocre bullet usually beats
  shrinking everything.
- **Page two only half-full.** Looks thin and unfinished. Fix: add substance
  (more real bullets, a stronger skills section, projects, publications) or open
  up spacing. Adding *real* content beats padding.

Aim for page two to reach roughly three-quarters down at minimum, ideally near
the bottom. The bottom margin is deliberately smaller than the others to help the
last lines settle onto page two rather than tipping to a third page.

## Page-fit knobs (in the content JSON `style` block)

The script ships with proven defaults. To nudge fit, override any of these in an
optional top-level `"style"` object. Sizes are in half-points (21 = 10.5pt);
spacing is in twentieths of a point (DXA).

```json
"style": {
  "margin": 864,           // left/right/top, DXA. 720 = 0.5", 864 = 0.6"
  "marginBottom": 612,     // smaller than margin on purpose, to pull lines onto p2
  "size":  { "body": 21, "bullet": 21, "head": 23, "name": 38 },
  "space": { "bulletAfter": 22, "sectionBefore": 104, "bodyAfter": 80 }
}
```

To gain space (fix overflow): lower `bulletAfter`, `sectionBefore`, `bodyAfter`;
or drop `body`/`bullet` from 21 to 20; or reduce `margin` to ~792. To fill a
sparse page two: raise those same values, or (better) add content. Make small
moves and re-render; layout is sensitive.

## Content JSON schema

Top level: `name`, `banner` (optional), `contactLines` (array of strings),
`sections` (array), and optional `style`.

Each section has a `type` and a `heading`:

- **profile**: `{ "type": "profile", "heading": "Profile", "text": "...", "target": "Targeting a Senior Software Engineering Manager role in AI/ML." }`
  The story made concrete, as several short readable sentences (not one run-on).
  The optional `target` line renders bold and in the accent color, set apart below
  the paragraph, so the role being sought is impossible to miss. See "The profile:
  tell the arc" below.
- **experience**: `{ "type": "experience", "heading": "Experience", "entries": [...] }`
  Each entry: `org`, `title`, `dates` (e.g. `"Feb 2021 – Present"`), optional
  `subline` (location, scope, reporting line, rendered italic), and `bullets`
  (array of strings). Lead each bullet with a strong verb; keep numbers verified.
- **education**: entries with `org`, `title`, `dates`, and optional `notes`
  (array of strings, e.g. honors line, then a majors line).
- **publications**: `items` is an array where each item is an array of run-parts
  `{ "text": "...", "italics": true }`. Use italics for the work's title:
  ```json
  [ { "text": "Chen, J. (2026). " },
    { "text": "Paper Title", "italics": true },
    { "text": ". Venue. doi:..." } ]
  ```
- **bullets**: a generic bulleted list, good for Projects/Ventures. Optional
  `intro` (italic grey line), then `items`, each either a plain string or
  `{ "lead": "Name: ", "text": "description" }` (lead is bolded).
- **skills**: `rows` of `{ "label": "...", "value": "..." }`, rendered as a bold
  label and a `·`-separated list.

Section order is whatever order you put them in. A common executive order:
Profile, Experience, Education, Publications, Projects/Ventures, Skills.

## ATS rules (don't get filtered before a human reads it)

The script already follows these; preserve them if you edit:

- **Real text in a single column.** No tables, text boxes, columns, or sidebars
  for content. Many ATS parsers mangle multi-column and table layouts.
- **No images or icons** carrying information. Logos and headshots don't parse.
- **Standard section headings** ("Experience", "Education", "Skills"). Clever
  names ("Where I've Made Dents") confuse parsers.
- **Standard fonts** (Calibri here) and normal characters. The bullet glyph and a
  right-tab for dates are safe.
- **Dates as text** in a consistent format.
- Keep contact info as plain text lines, not in a header/footer (some parsers skip
  headers/footers).

## ATS keywords

Mirror the language of the target job descriptions where it is *true* of the
person. If postings say "distributed systems," "people management," and "LLM," and
those are real, use those exact words. This is keyword alignment, not fabrication:
you are choosing true phrasings that match what the screener searches for. If a
keyword is not true of the person, leave it out.

## Strategic ordering (never leave it to chance)

Order is a decision, not a default. The reader skims top-down and on mobile sees
only the first line or two of each block.

- **Experience entries:** reverse-chronological (most recent first). A concurrent
  role sits next to the primary current role.
- **Bullets within a role:** impact-first, not chronological. The first bullet is
  the highest-scale, most role-relevant win, and its *first clause* signals
  people-leadership, scope, or the target domain (AI/ML), with the technical detail
  after. The current role gets the most bullets and the most explicit leadership
  language. If the person says which bullet should lead, that instruction wins.
- **Projects:** lead with the ones that reinforce the target (for an
  eng-leadership / AI role, the agentic and developer-productivity builds before a
  consumer app).
- **Skills rows:** lead with Leadership, then the differentiator (AI / agentic),
  then platforms, then languages.
- **Honor explicit ordering.** If the person gives a sequence (company chronology,
  major order, which item leads), reproduce it exactly. Re-ordering "to improve it"
  after they specified an order is a trust-killer.

## The profile: tell the arc (senior EM / director framework)

For a senior engineering-leadership target, the profile is not a description of the
current job; it is the *arc*. What a strong one does, in order:

1. **Identity + seniority + arc.** "Engineering leader with 11 years of experience,
   rising from software engineer at [first co] through [...] to engineering lead at
   [current co]." Use numerals for years ("11 years of experience"), and do not drop
   the connective words ("of experience") that make it read naturally.
2. **Current scope + title bridge.** Resolve the IC-title-vs-manager question
   immediately: state the literal title and that the role is the leadership job
   (team size, scale, users). Never claim a held manager title the person did not
   hold; name the function instead.
3. **The target-domain centerpiece.** For an AI/ML role, place the hands-on AI proof
   (e.g., the agentic-AI platform) high, not buried. It is usually the single most
   relevant, hardest-to-fake asset.
4. **One marquee, quantified prior win** that proves the arc ($40M, etc.).
5. **The business / strategic dimension** (MBA, exec teaching) that reaches toward
   director, without inventing org size.
6. **A bold `target` line** stating the exact role sought.

Build this framework first and get the person to approve the *outline* before
writing prose. Agreeing on structure is far cheaper than rewriting finished
paragraphs. Keep every sentence short (see "One idea per sentence" in
`voice_and_integrity.md`).

## Get the spec up front

The fastest engagements front-load the constraints. Before drafting, pin down: the
no-pronoun rule, the tense standard, capitalization, the target title verbatim, the
exact company/section order, and any exemplar (the person's own LinkedIn About or a
profile they admire). Surfacing these one at a time through correction rounds is
what turns a 20-minute job into a multi-hour one. When the person hands you exact
text, treat it as final and change only obvious typos.

## Layout: orphan control is built in

The bundled `scripts/build_resume.js` sets `keepNext` on section headings, role
lines, and sublines so a heading can never be stranded alone at the bottom of a
page, and it supports the optional bold `target` line on the profile. If you swap
in a different builder, preserve both behaviors. Always render to PDF and *look* at
the page breaks; never trust the docx alone.
