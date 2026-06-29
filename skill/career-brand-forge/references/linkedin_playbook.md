# LinkedIn Playbook

How to optimize a LinkedIn profile section by section, plus the mechanical
realities of editing one (these are easy to get wrong and waste a lot of time).

## The reality to accept first

**There is no official LinkedIn API for reading or editing a personal profile.**
That shapes everything:

- You cannot reliably automate profile edits. Driving the live site through a
  browser agent is brittle and against LinkedIn's terms, and risks account flags.
- The **safe, reliable default is to produce the copy and let the person paste
  it in.** It is faster and lower-risk than fighting the UI, and the person stays
  in control of their own account.
- If you do edit live (with the person watching), go one field at a time and
  verify after every change. Treat each save as a side effect that needs the
  person's explicit go-ahead.
- Editing live LinkedIn via subagents has a track record of dropped characters,
  clicking the wrong target, and accidental deletions. Don't delegate it blind.

## Section-by-section

### Headline (the most-read line on the profile)

220 characters. It shows in search, comments, and messages, so it does more work
than any other field. Pattern that works for senior people:

> [Role/Identity] · [the story, with a number] · [headline credential]

Example: `Apple Engineering Leader · Scaling a 100M-user AI Knowledge Graph |
Wharton MBA`. Lead with identity, put the most impressive *true* scope in the
middle, end with the credential that opens doors. Keep it consistent with the
résumé banner so the two surfaces match.

### About (the story, in first person)

LinkedIn is a first-person, slightly warmer register than the résumé (which is
first-person but terse). Open with the strongest true positioning sentence, then a
short paragraph of scope and proof (numbers, scale, what you own), then a line on
direction or what you care about. A few short paragraphs beats one block. Same
voice rules apply: no em-dashes, no clichés, specific over abstract.

### Experience

Mirror the résumé's bullets but you have more room, so the top role can be fuller.
Keep titles, dates, and numbers **identical** to the résumé (this is where
inconsistencies creep in). Use the role's bullets to carry the keywords a recruiter
searches.

### Featured

The visual proof shelf. Pin the things that most support the story: links to
publications, shipped products/repos, talks, press. Link cards render a title and
description, so the destination's metadata matters. Order so the strongest item is
first.

### Projects

Good home for side ventures and shipped products. For each: a punchy name, a
description that says what it does and what's impressive about it (stack, scale,
test count, what problem it solves), the date, a link, and **attach the relevant
skills** (LinkedIn lets you associate skills with a project, which reinforces
those skills elsewhere). Don't leave projects skill-less; that association is free
signal.

### Skills

Pin the three most important to the top; those show on the profile and carry the
most weight in search. List real, specific skills, and make sure they're the ones
that appear in your Experience and Projects so they're corroborated.

### Education, Honors, Publications

Keep titles, dates, and honors consistent with the résumé. See ordering behavior
below, because these sections sort themselves.

## Section and item ordering (LinkedIn does this for you, sometimes annoyingly)

- **You cannot freely reorder most sections.** The profile has a largely fixed
  section order. Don't promise a custom section order you can't deliver.
- **Within Honors and Publications, items auto-sort by date, reverse-chronological.**
  Entries with **no date sort to the bottom or alphabetically**, not where you'd
  expect. If order matters, set dates deliberately.
- **Experience and Education sort by date too.** Concurrent roles can be ordered by
  adjusting start dates within truth, but don't fabricate dates to reorder.

## Editing mechanics (if you are driving the UI)

These are specific, hard-won quirks. They will save hours:

- **Set whole field values, don't keystroke them.** Use a form-fill that sets the
  entire value at once. Character-by-character typing into LinkedIn fields drops
  characters.
- **Detail/edit pages for Publications and Honors only render when reached via
  "Show all" from the profile**, not by navigating to the details URL directly. A
  direct URL can come up blank.
- **The Project form opens fine from its direct "add" URL.**
- **The Publication date field is free-text mm/dd/yyyy and rejects a year alone.**
  Worse, once it has an invalid value it can hold a *sticky* validation error that
  blocks saving even after you fix the field. If you hit that: abandon the form,
  open a fresh one, and fill everything *except* the date if a precise date isn't
  needed.
- **Element references change on every page load.** Re-find targets after any
  navigation; don't reuse a stale handle.
- **Verify after every save.** Re-read the section to confirm the change landed and
  nothing else moved.

## Keep it consistent with the résumé

Every time you touch LinkedIn, the test is the same: if a recruiter opens the
résumé and the profile side by side, do they see one coherent person? Headline
matches the résumé banner, titles and dates match, the same ventures appear, the
numbers agree. The cross-check lives in `qa_checklist.md`.
