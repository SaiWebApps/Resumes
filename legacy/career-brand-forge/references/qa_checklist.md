# QA Checklist

Run before declaring any package done. Three passes: reconcile, the two reads, and
the mechanical lint.

## 1. Reconcile (résumé ↔ LinkedIn tell one story)

Put them side by side. They should never *contradict*; the résumé is tighter and
LinkedIn is fuller, but the facts match.

- [ ] **Headline / banner** framing matches (the résumé banner echoes the LinkedIn
      headline, same positioning, same key number).
- [ ] **Titles** match for every role.
- [ ] **Dates** match for every role and degree.
- [ ] **Numbers** match (team sizes, dollar figures, percentages, user counts).
      This is the most common drift; check each one against the fact ledger.
- [ ] **Same ventures/projects** appear, named the same way.
- [ ] **Education, honors, publications** consistent (titles, dates, honors).
- [ ] The **story from Phase 0** is recognizable in both, and nothing in either
      surface pulls against it.

A number that was changed or removed in one place must be changed or removed in the
other. Deletions that survive in one surface are a classic regression.

## 2. The recruiter read (the 6-second skim)

Recruiters skim fast and rely on parsers. Check:

- [ ] The top third communicates who this person is and the level they're at,
      without reading every bullet.
- [ ] **ATS-parseable**: single column, real text, standard headings, no
      information trapped in tables/images/text boxes. (See `resume_playbook.md`.)
- [ ] The **keywords** from the target job descriptions are present where true.
- [ ] Two full pages, clean and scannable, strong verbs leading bullets.
- [ ] Contact info and links are present and correct.

## 3. The hiring-manager read (the credibility pass)

A manager reads for substance and sniffs out inflation. For each strong claim, ask
the follow-up question they would ask:

- [ ] Every impressive number would **survive one follow-up question** in an
      interview. If "tell me about that" would expose a stretch, fix the line.
- [ ] Claims are **concrete** (named systems, real scope) rather than adjective
      soup.
- [ ] Scope and seniority are **credible together** (the title, the team size, and
      the impact line up; nothing reads as borrowed credit).
- [ ] The narrative shows a **trajectory** toward the goal/level being targeted,
      not a flat list of tasks.
- [ ] Nothing **undersells**: a true, larger framing isn't hiding behind a modest
      one.

## 4. Mechanical lint (objective, fast)

- [ ] **Zero em-dashes** anywhere (—). Search for the character. (En-dashes in
      date ranges are fine.)
- [ ] **Zero cliché/tell blocklist hits** (see `voice_and_integrity.md`):
      spearheaded, leverage, utilize, passionate, results-driven, proven track
      record, boasts, synergy, etc.
- [ ] **Every number traces to the fact ledger** and is marked verified.
- [ ] **Tense** is consistent (present for current roles, past for prior).
- [ ] **Active voice**, varied sentence structure, one strong verb per bullet.
- [ ] Names, companies, and links spelled and formatted correctly.

A quick grep for em-dashes and blocklist words catches most mechanical misses in
seconds; do it rather than eyeballing.

## If anything fails

Fix it before delivering, and if a fact is in question, ask the person rather than
guessing. The whole pipeline's credibility rests on the integrity rule; a single
caught fabrication does more damage than a dozen merely-fine bullets.
