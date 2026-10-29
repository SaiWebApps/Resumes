---
name: career-brand-forge
description: >-
  End-to-end pipeline for building a senior or executive job-search package: a
  polished two-page résumé plus a reconciled LinkedIn profile that tell one
  consistent story. Use this whenever the user wants to write, rewrite, refine,
  polish, or "punch up" a résumé or CV; optimize, audit, or overhaul a LinkedIn
  profile (headline, About, Experience, Featured, Projects, Skills, Honors,
  Publications); reconcile a résumé and LinkedIn so they match; reposition
  themselves for a specific role or level (Senior Engineer, EM, Director, VP,
  exec); or package their experience, repos, and publications into application
  materials. Trigger even when the user mentions only one piece ("fix my
  resume", "my LinkedIn is weak", "make this sound more senior", "help this not
  sound like AI wrote it"), because the voice and anti-fabrication discipline
  apply to any single piece. Enforces a strict no-fabrication rule (never invent
  numbers, dates, titles, or scope) and a leaderly voice with zero em-dashes and
  no LLM clichés.
---

# Career Brand Forge

A pipeline for turning a person's raw career material into a coherent, credible,
senior-sounding job-search package: a two-page executive résumé and a LinkedIn
profile that say the same thing in the same voice.

## What actually creates the value here

The hard, valuable part of this work is **not** asking a model to "improve my
résumé." Any chatbot does that, and the output reads like every other chatbot's
output: inflated, generic, and quietly full of invented numbers. The value of
this pipeline is the discipline layered on top:

1. **Integrity.** Every verifiable claim (number, date, title, team size, scope)
   traces to something the person actually confirmed. Nothing is invented to
   sound better. This is the single most important rule and the one that gets
   violated most easily. A fabricated metric that surfaces in an interview is a
   fireable, offer-rescinding event, so the bar is zero.
2. **One story.** Résumé and LinkedIn are treated as a single system. The
   headline, the framing, the titles, and the numbers match across both. A
   recruiter who opens both tabs should see one person, not two drafts.
3. **A voice that doesn't read like AI.** Active, specific, varied, leaderly,
   and free of the tells (em-dashes, "leverage", "passionate", "results-driven",
   "spearheaded", "boasts a proven track record").
4. **Human-in-the-loop.** The person is the source of truth and the final taste
   check. The pipeline surfaces facts for confirmation and shows work; it does
   not barrel ahead and silently guess.

Hold those four and the output is genuinely differentiated. Drop them and this
is just another wrapper.

## Read this first, every time

Before writing a single line of résumé or profile copy, read
**`references/voice_and_integrity.md`**. It contains the non-negotiables: the
no-fabrication method (fact ledger) and the voice rules. These apply to *every*
phase and every piece, even a one-line headline tweak. In particular: **zero
pronouns** (personal and reciprocal, not just "I"), **one consistent tense per
section** (verified verb by verb), **no run-ons or wall-of-text**, **every list
item and project description capitalized**, no em-dashes, no clichés, and **the
person's exact words and ordering preserved** wherever they gave them. Each of
those, skipped, costs a correction round.

And read what already exists in the project folder *before* drafting: the fact
ledger / dossier, prior critiques, the current résumé, and the person's LinkedIn
About. Re-deriving rules and facts that are already written down is the single
biggest avoidable time-sink in this whole pipeline.

## The pipeline

Run as much or as little of this as the user needs. If they only want the
résumé, do Phases 0-2 and 4-5 on the résumé. If they only want a LinkedIn
headline, you still owe them Phase 1 (don't invent) and the voice rules. The
phases are a checklist, not a forced march.

Anything time-sensitive (compensation, market keywords, target-role profiles,
critique notes) is **regenerated, not stored**: see
`references/refresh_and_research.md`. The only durable inputs are the person's fact
ledger and their current LinkedIn; everything else refreshes from those. This is
why a backup of this work only needs the skill, the résumé source, and those two
inputs, not a pile of stale research.

### Phase 0: Story and goal (the north star)

Before anything, pin down two things and write them down:

- **The goal.** What role, level, and kind of company is this person aiming at?
  "Senior EM / Director, people-management track, at top AI companies" is a goal.
  "A better job" is not.
- **The story.** The one-sentence positioning everything else must reinforce.
  Example: "an engineering leader who has grown from engineer to running the teams
  behind global real-time data platforms." Keep it confident and specific, never defensive;
  "still ships the hard parts" reads as self-justification, not strength.

Everything downstream is judged against these. If a bullet, a skill, or a
headline doesn't serve the goal and the story, it is clutter. When the user later
says "you forgot my story," it means you optimized a section in isolation and
broke the throughline. Re-read the goal before each section.

### Phase 1: Intake and the fact ledger

Gather the raw material: existing résumé, LinkedIn (export or screenshots), brag
docs, performance reviews, project repos, publications, target job descriptions.
**Build from what exists** rather than reinventing a structure the person already
likes.

Then build the **fact ledger**: a running list of every verifiable claim with its
source. Titles, dates, team sizes, dollar figures, percentages, scope, user
counts. This is the spine of the integrity rule. Full method in
`references/voice_and_integrity.md`. When a number is unverified or fuzzy, flag
it and ask. Do not "round up to sound better," and do not carry a number from one
document into another just because it was there; confirm it.

### Phase 2: The résumé

Build a dense, ATS-safe, **two full pages**. Use the bundled script
`scripts/build_resume.js`, which is tuned to land two full pages with a clean
executive layout. Workflow, the content-JSON schema, the page-fit knobs, and the
ATS rules are in `references/resume_playbook.md`.

The short version: draft the content into a JSON file, run the script, render the
result, look at it as a recruiter, and tune. Do not hand-format docx paragraphs;
that is what the script exists to prevent.

For the profile specifically, **build the framework first and get the outline
approved before writing prose** (the senior-EM / director arc framework is in
`references/resume_playbook.md`). Agreeing on structure is far cheaper than
rewriting finished paragraphs, and it is how you avoid the death-by-a-thousand-
edits loop.

### Phase 3: LinkedIn

Optimize section by section: headline, About, Experience, Featured, Projects,
Skills, Education, Honors, Publications. The section-by-section playbook, the
ordering behaviors (what auto-sorts and how), and the editing mechanics are in
`references/linkedin_playbook.md`.

One reality to internalize up front: **there is no official API to read or edit a
LinkedIn profile.** Automating profile edits through a browser is brittle and
violates LinkedIn's terms. The reliable, safe pattern is to produce the copy and
have the person paste it, or drive edits with the person watching and confirming
each change. Treat any profile edit as a side effect that needs the person's
explicit go-ahead.

### Phase 4: Reconcile (one story, two surfaces)

Put résumé and LinkedIn side by side and make them agree: same headline framing,
same titles, same dates, same numbers, same ventures. Differences are either
fixed or deliberate (the résumé is tighter, LinkedIn is fuller, but they never
*contradict*). The cross-check list is in `references/qa_checklist.md`.

### Phase 5: QA and the two reads

Before declaring done, run two passes from `references/qa_checklist.md`:

- **The recruiter read** (6-second skim, ATS-parseable, keywords present).
- **The hiring-manager read** (credible, concrete, no inflation that would
  collapse under one follow-up question).

Plus the mechanical lint: zero em-dashes (and no minus-sign or other ATS-breaking
glyphs), **zero pronouns** (literal word-search), **one tense per section**
(verb by verb), **no run-ons**, every list item and project description
capitalized, no cliché blocklist hits, every number in the fact ledger, and
résumé and LinkedIn consistent.

## Operating notes

- **Confirm before side effects.** Sending, publishing, or editing a live
  profile needs the person's explicit yes. Generating files and copy does not.
- **Show the facts, don't assume them.** When something is unverified, ask. The
  person would much rather answer a quick question than catch an invented number
  later. Inventing a plausible-sounding number is the worst failure mode of this
  whole pipeline.
- **Subagents for live LinkedIn editing are unreliable.** Driving a real LinkedIn
  session through a browser agent has a track record of dropped characters,
  wrong-target clicks, and accidental deletions. Prefer producing copy for the
  person to paste; if editing live, go slowly and verify after every change.
- **Stay on the north star.** Re-read Phase 0 before each section so individual
  edits don't quietly break the overall story.

## Files in this skill

- `references/voice_and_integrity.md`: the non-negotiables: no-fabrication
  method (fact ledger) and the voice rules + cliché blocklist. Read first.
- `references/resume_playbook.md`: résumé workflow, content-JSON schema,
  page-fit knobs, ATS rules.
- `references/linkedin_playbook.md`: section-by-section LinkedIn playbook,
  ordering behaviors, editing mechanics, the no-API reality.
- `references/qa_checklist.md`: reconcile + the recruiter and hiring-manager
  reads + the mechanical lint.
- `references/refresh_and_research.md`: how to regenerate the time-sensitive,
  derived material (comp/market/role research, the critique passes) so it never
  has to be stored stale.
- `scripts/build_resume.js`: data-driven two-page résumé builder (Node + the
  `docx` package). Reads a content JSON, writes a styled .docx.
- `scripts/resume_content.example.json`: a worked sample showing the schema.
