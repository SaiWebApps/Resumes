# Voice and Integrity (read before writing anything)

These two disciplines are what separate this pipeline from a generic "make my
résumé better" prompt. They apply to every phase and every piece, down to a
single headline.

---

## Part 1: Integrity (never invent verifiable facts)

### The rule

Never invent or inflate a verifiable fact: numbers, percentages, dollar figures,
dates, titles, team sizes, user counts, company names, scope. You may sharpen,
reframe, reorder, and choose the strongest true framing. You may not manufacture
the underlying fact.

### Why this is the highest-stakes rule

A résumé number is a claim the person will have to defend in an interview, often
to someone who was in the room for the real thing. "Tell me about the $40M you
saved" or "walk me through leading that team of 15" is a normal question. If the
number was invented to sound impressive, the person gets caught, and it reads as
dishonesty, not enthusiasm. That can cost the offer or the job. The downside of
under-claiming is small; the downside of a fabrication is catastrophic. So the bar
is zero invented facts, not "usually accurate."

This is also the failure mode an eager assistant slips into most easily, because
inventing a clean number *feels* helpful. It is not. A vague-but-true line beats a
specific-but-invented one every time.

### The fact ledger

Build a running ledger of every verifiable claim and where it came from. Keep it
for the whole engagement; it is the spine of every later check.

| Claim | Value | Source | Status |
|-------|-------|--------|--------|
| Platform team size | 8 engineers | user confirmed | verified |
| Alexa platform savings | $40M/yr | prior résumé, user confirmed | verified |
| "directs a 15-engineer program" | (none) | appeared in an old draft | **unverified, do not use until confirmed** |

Rules for the ledger:

- A number is **verified** only when the person confirms it or it comes from a
  source the person vouches for. Its mere presence in an old document is **not**
  confirmation. Documents carry forward old errors; treat an unsourced number in a
  prior draft as a question, not a fact.
- If a number is unverified, fuzzy, or you are tempted to "round up," **stop and
  ask.** One quick question now prevents a much worse conversation later.
- When you remove or change a claim at the person's instruction, update the ledger
  so it doesn't creep back in via a later copy-paste. (Numbers that get deleted in
  one place and silently survive in another are a classic regression.)

### Reframing is allowed and encouraged

Integrity is not blandness. Choosing the strongest *true* framing is the job:

- "Reduced issues from 40/week to 10/week" instead of "improved reliability."
- "Promoted from L5 to L6" instead of "senior engineer."
- "Led an eight-engineer team across three sites" instead of "manage a team."

All true, all sharp. That is the target.

---

## Part 2: Voice (leaderly, specific, pronoun-free, and not obviously AI)

### The single hard formatting rule: no em-dashes

Do not use em-dashes (—) anywhere. Not in the résumé, not in LinkedIn copy, not
in cover letters. Use a period, a comma, a colon, or a parenthesis instead. The
em-dash is the most recognizable tell of LLM-generated text, and a profile that
pattern-matches to "AI wrote this" loses credibility instantly with the exact
audience (recruiters, engineering leaders) this pipeline targets. This rule is
absolute because it is binary and easy to verify. Also avoid the minus sign
(U+2212, as in "−45%") and any non-ASCII glyph that can break an ATS parser; write
plain "45%" with a normal hyphen if one is needed.

(En-dashes in date ranges, like "Feb 2021 – Present", are fine and standard.)

### No pronouns, ever (this is the one that gets violated most)

Résumé and profile copy carries **zero personal or reciprocal pronouns.** Not
first person ("I / me / my / we / us / our"), and not third person either
("they / them / their / it / its / he / his / she / her / each other / one
another"). Use the implied-subject telegraphic voice: "Led the team," "Ships
agentic AI," "Develops engineers to promotion."

The trap is the *third-person* pronouns hiding in relative clauses, because a
narrow "remove the I's" pass leaves them in. Watch for:

- "the projects **it** touches" → "every dependent project"
- "workflows the team runs daily" is fine; "blocks a bad tool call before **it**
  executes" → "before execution"
- "personas push back while users practice" is fine; "grades the moves **they**
  made" → "grades the moves that landed"

Relative pronouns (that / which / who / whose) are allowed and natural; they are
not personal pronouns. **Before declaring any copy done, run a literal word
search for every personal and reciprocal pronoun.** This single check would have
saved several rounds in practice.

### Tense, by section (verify verb by verb)

Mixed tense inside one block is the error sharp readers pounce on, and a coarse
"present for current, past for prior" rule is not enough. Hold this standard and
audit *every finite verb* against it:

- **Profile / summary:** present tense, or a participial flow ("leading… building…
  developing…"). No past-tense finite verbs. State completed wins as present-state
  facts or noun phrases. Do not stitch present and past in one paragraph (the
  classic break is "Leads… Sets… **drove**…").
- **Experience bullets (every role, current and prior):** past tense. The leading
  verb is past, and so is every finite verb inside, *including relative clauses*:
  "a platform **that turned** X into Y," not "that turns." Gerunds (-ing) and
  infinitives (to X) are tenseless and fine.
- **Role sublines:** current-role sublines tenseless (noun + gerund: "Engineering
  lead for an 8-engineer team, reporting to the engineering director"); prior-role
  sublines past ("Promoted from SDE II; led…").
- **Projects / live systems:** present tense, describing what the system does
  ("Maps the blast radius… generates fixes"). Consistent across the whole section.
- **Education / Publications / Skills / header:** tenseless noun phrases and
  citations.

These differ by design (a summary is present, accomplishments are past, live
software is present), and that is correct, not inconsistent. The failure is drift
*within* a single block. When in doubt, build a verb-by-verb table per section.

### One idea per sentence (no run-ons, no wall of text)

A profile that reads as one long run-on, or as a paragraph stitched together with
colons and semicolons, gets rejected on sight even when every fact is right.

- One idea per sentence. Short, declarative, scannable.
- Do not join two independent clauses with a colon ("100M+ users: setting
  direction" is a run-on) or a comma (comma splice).
- A profile of several short sentences reads far better than one dense sentence.
  Default to the multi-sentence format; never collapse it into a single block to
  "tighten" it.
- A bolded target line on its own (see the résumé playbook) can close the profile.

### Capitalization and the person's exact words

- **Capitalize every list item** the reader scans: each `·`-separated Skills item
  starts with a capital ("Cross-functional and multi-site delivery"), and each
  Project description starts with a capital after its bold lead.
- **When the person gives exact phrasing, follow it verbatim.** Fix only obvious
  transcription typos (a missing space, a doubled space). Do not reword, "improve,"
  reorder, or drop their words. Dropping a key phrase the person chose is the
  fastest way to lose their trust. If a specific order is given (company
  chronology, which bullet leads), honor it exactly.

### The voice, positively stated

- **Active voice and strong, specific verbs.** "Led," "Built," "Shipped," "Drove,"
  "Designed," "Owned." One strong verb per bullet, not stacked. Never "was
  responsible for."
- **High sentence variety.** Vary length and structure. A wall of identical
  "Did X to achieve Y" bullets reads as a template.
- **Leaderly, not boastful, and never defensive.** Confidence comes from specifics
  and scope, not adjectives. Avoid defensive or combative framing: "runs the team
  and still ships the hard parts" and "whether the room is X, Y, or Z, leads it"
  both read as someone defending themselves. Just state the scope.
- **Concrete over abstract.** Name the system, the stack, the number, the outcome.

### The cliché and tell blocklist

Avoid these. They signal both "AI wrote this" and "this person has nothing
specific to say":

- spearheaded, leverage / leveraging, utilize (just say "use"), passionate,
  results-driven, results-oriented, proven track record / proven record, boasts,
  seasoned, dynamic, synergy, deep dive, deep expertise, high-performing, move the
  needle, wear many hats, think outside the box, go-getter, self-starter,
  detail-oriented, team player, hardworking, "responsible for", "duties included",
  "a wide variety of", "various", "etc."
- Empty intensifiers: very, highly, extremely, incredibly, world-class,
  cutting-edge, state-of-the-art, best-in-class (unless literally and verifiably
  true and load-bearing).

### A quick before/after

**Before (generic, AI-flavored, em-dashes, pronouns, defensive):**
> Results-driven engineering leader with a proven track record of leveraging
> cutting-edge technologies — spearheading cross-functional initiatives. I run the
> team and still ship the hard parts.

**After (specific, leaderly, pronoun-free, clean):**
> Engineering leader with 11 years of experience, leading an 8-engineer team behind
> a media knowledge graph that serves 100M+ users. Ships production agentic AI by
> hand, including an LLM ops assistant the team uses daily.

The second is shorter, says more, names a real number, carries no pronouns, and
contains zero tells.

### Self-check before you call any copy done

- Zero em-dashes and no minus-sign or other ATS-breaking glyphs?
- **Zero pronouns** (personal and reciprocal), checked with a literal word search?
- **One consistent tense per section**, verified verb by verb?
- **No run-ons**; one idea per sentence; the profile readable, not a wall of text?
- Every Skills item capitalized; every Project description capitalized?
- Zero blocklist words; no defensive or combative framing?
- Every number in the fact ledger and verified?
- The person's exact words and ordering preserved wherever they gave them?
- Would this survive being read aloud by the person in an interview?
