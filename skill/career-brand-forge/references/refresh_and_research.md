# Refresh and research (regenerate the volatile stuff)

Most of what a job search produces is **time-sensitive and derived**: compensation
bands, market keywords, target-role profiles, and critique notes all go stale fast.
Do not treat stored copies as truth, and do not bother backing them up. The only
**durable** inputs are:

- the person's **fact ledger** (their real career facts), and
- their **current LinkedIn / résumé**.

Everything else is regenerated on demand with the procedures below. This keeps the
package small, keeps sensitive comp figures out of any repo, and means a fresh
session always works from current data instead of a stale snapshot.

## 1. Rebuild the fact ledger

The ledger is the spine (see `voice_and_integrity.md`). Rebuild it from the person's
résumé and LinkedIn plus a short confirm-the-numbers interview. Every number carries
a source and a verified / unverified status. Never carry a number forward just
because it appeared in an old draft; confirm it. This file *is* worth keeping,
because it is the person's real history, not derived data.

## 2. Refresh compensation and market data

Comp moves every quarter and equity marks move faster. Regenerate, never
store-and-trust.

- Pin the target: title, level, and company tier (frontier lab vs. big tech vs.
  scaleup) before pulling any numbers.
- Pull **current** ranges from live sources (today's job postings, the person's own
  offers and recruiter conversations, up-to-date public comp data). Record the date.
- **Anchor to level, not aspiration.** A candidate with no manager title anchoring at
  Director numbers gets re-priced down and remembered as inflated. Sell to scope and
  let the number follow.
- Flag anything unverified. Never invent a band to look precise.

## 3. Refresh target-role profiles and keywords

- Read several **current** job descriptions for the exact target title at the target
  companies.
- Extract the keywords the screen actually uses ("engineering management,"
  "agentic," "LLM," "distributed systems," and so on).
- Mirror only the keywords that are **true** of the person (see "ATS keywords" in
  `resume_playbook.md`). This is alignment, not fabrication.

## 4. Run the critique passes (the QA that catches what one pass misses)

Before declaring anything done, role-play adversarial reviewers and force fixes. In
practice this is what separates a "fine" résumé from one that lands. Spin them up as
separate, skeptical reviewers (subagents work well), one per concern, each trying to
find reasons **not** to advance the candidate:

- **Hiring manager** for the exact target role: would this earn an unhesitating "get
  me this candidate now"? If not, what is missing? Loop with an editor until it
  would.
- **Recruiter / ATS**: 6-second skim plus keyword and parse check. Title-vs-target
  gap? Any ATS-breaking glyph (em-dash, minus sign)?
- **Consistency**: numbers, titles, dates, capitalization, and tense, verified
  section by section, verb by verb.
- **Run-on detector**: every sentence one idea; no wall-of-text; no colon- or
  semicolon-stitched clauses.

Apply the legitimate fixes; ignore the noise. Then re-run the mechanical lint in
`qa_checklist.md`.

## What stays in the backup vs. what regenerates

- **Keep (durable):** this skill, the résumé source + rendered PDF, the fact ledger,
  the LinkedIn capture.
- **Regenerate (do not store):** comp and market research, target-role keyword
  research, and critique notes. They go stale and some are sensitive; the procedures
  above rebuild them fresh from current sources.
