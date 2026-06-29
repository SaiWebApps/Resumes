# Sai Krishnan — Professional Dossier (Source of Truth)

> **Purpose.** Single comprehensive superset of every verifiable fact about Sai Krishnan, assembled to feed his resume, LinkedIn rewrite, and personal website. Target: external search for **Senior Engineering Manager / Director (people-management track), AI/ML focus** — AI labs, Big Tech, AI scaleups, AI-focused consulting.
> **Compiled:** 2026-06-27.
> **Sources:** Manager-track resume (`Sairam_Krishnan_Resume.pdf`); Engineering/IC resume (`Sairam_Krishnan_Engineering_Resume.pdf`); live LinkedIn capture (`sai_linkedin_current.md`); ORCID `0009-0004-2626-1273` (verified via Crossref); CMR working paper (`CMR_Submission.pdf`); Apple Claude Code usage report (`apple_ai_usage_report.html`); personal venture repos (persuaider, dependiq/Lore, airoi, ondoway, claude-kit) read at source level.
> **Rules honored:** Nothing dropped. Verifiable facts kept exact. No fabrication — strong framing only. Anything ambiguous is flagged in **§17 NEEDS CONFIRMATION**. Apple descriptions kept at the public-resume level (no proprietary detail, codenames, or specifics).

---

## Table of Contents
1. Identity & Contact
2. Positioning Summary (one paragraph)
3. Full Chronological Career History
4. Education & Academic Honors
5. Publications & Thought Leadership
6. AI Ventures / Projects (from repos)
7. Open-Source & Tooling
8. Speaking & Teaching
9. Honors & Awards
10. Certifications
11. Skills (grouped)
12. Spoken Languages
13. Volunteering
14. Recommendations
15. Quantified-Impact Bank
16. Proof-Point Bank (headlines / About)
17. Needs Confirmation

---

## 1. Identity & Contact

- **Name:** Sairam Krishnan (goes by **Sai Krishnan**). Pronouns: He/Him.
- **Current title (employer):** Principal Software Engineer, Apple (Apple Media Products — Knowledge Graph Platform).
- **Location:** Sammamish / Seattle, Washington, United States. (Resume address: 1461 240th Ave NE, Sammamish, WA 98074.) Open to relocation anywhere.
- **Citizenship / work authorization:** U.S. Citizen.
- **Phone:** 281-513-1263.
- **Email:** sairambkrishnan@gmail.com.
- **LinkedIn:** linkedin.com/in/sairambkrishnan (500+ connections; 552 followers; "Open to work" — senior engineering leadership, recruiters only, US).
- **GitHub:** github.com/SaiWebApps.
- **ORCID:** orcid.org/0009-0004-2626-1273.
- **Personal project site:** saiwebapps.github.io/airoi (AI ROI Framework).
- **Signal of interest (LinkedIn follows):** Anthropic, Google DeepMind, Perplexity, Wharton Executive Education.

---

## 2. Positioning Summary

Sai Krishnan is a hands-on engineering leader with **11 years** across Apple, Amazon, Microsoft, and Susquehanna International Group (SIG), now leading the **8-engineer team that builds Apple's media knowledge graph** — the platform powering search, recommendations, and content discovery for **100M+ users**. He pairs distributed-systems and ML-platform depth (knowledge graphs, entity resolution, Flink/Kafka/Spark/Cassandra/Neo4j at catalog scale) with documented business impact (**$40M/yr saved** at Amazon Alexa; **40% data-quality** and **30% velocity** gains, **45% fewer incidents** at Apple). He is finishing a **Wharton Executive MBA** (WEMBA Class of 2026; five majors incl. AI in Business) where he won the peer-voted **Benjamin Franklin Award** and made the **Director's List in all six terms** — all while working full-time at Apple. His differentiator is that he **still bleeds on the field**: he builds production agentic-AI tooling himself (an LLM-powered ops assistant over logs/traces/metrics via MCP; an agentic skill platform; an open-source Claude Code kit), publishes peer-reviewed and management research on AI's effect on engineering (CMR working paper; SSRN AI-ROI framework), and teaches AI strategy to C-suite audiences (Praxtera AI Institute; HP, Morgan Lewis, PBS, Philadelphia Eagles). Equally effective in an architecture review, an executive briefing, or a 2 a.m. incident bridge.

---

## 3. Full Chronological Career History

> Reverse-chronological. Every role, level, promotion, location, and impact bullet captured across all sources. Where the two resumes phrase a role differently, both framings are preserved.

### Apple — Principal Software Engineer, Knowledge Graph Platform
**Feb 2021 – Present** (~5 yrs 5 mos as of capture) · Apple Media Products · Seattle, WA
**Scope/level:** Principal Software Engineer. Leads an **8-engineer team** spanning **Seattle, London, and vendor sites in Europe and Latin America**; reports to the engineering **Director**. (Earlier resume framing also references coordinating teams across Cupertino, Seattle, London, and Singapore for specific programs.)

Impact bullets (superset across resumes + LinkedIn):
- Lead architecture and cross-functional delivery of Apple's **media knowledge graph**, unifying metadata from **15+ sources** (music, books, podcasts, TV) into a single canonical, Apple-standardized model that powers **search, recommendations, and content discovery for 100M+ users**.
- **Spearheaded the global launch of Apple Music Credits**, directing a **15-engineer program across 4 sites** (Cupertino, Seattle, London, Singapore) to deliver **real-time credits curation for millions of tracks**.
- **Drove the re-platform from batch to real-time streaming** (Spark → **Flink / Kafka / Cassandra**), moving catalog-scale entity ingestion, similarity mapping, and graph generation to an event-driven architecture.
- **Designed an ML entity-resolution system** (similarity mapping + clustering; K-Means referenced in IC resume) that deduplicates entities across disparate sources — **improved data quality 40%** and cut downstream processing costs.
- Built and operates **graph query services and a client library** consumed by partner teams — the documented, supported entry point to the knowledge graph.
- **Standardized cross-team data exchange** through a shared **Protobuf** interface definition, adopted across the platform's streaming modules and by partner teams.
- **Pioneered agentic AI for production operations:** built an **LLM-powered ops assistant** integrating logs, traces, and metrics via **MCP** — natural-language debugging, anomaly detection, and incident triage for the platform.
- **Created an agentic skill platform** turning specialized pipeline operations (entity curation, fact verification, data queries, log forensics) into plain-English workflows usable by engineers and non-engineers; adopted by the team for daily operations and on-call.
- **Raised the engineering bar** through design-review, code-review, and CI/CD standards — **team velocity up 30%, production incidents down 45%**; mentors the team's engineers, provides performance-review input, and drives hiring.

*(See §6/§7 for the agentic-AI tooling he built; the Apple Claude Code usage report independently documents his hands-on, evidence-first engineering — adversarial verification, cross-repo root-cause tracing, deep-debugging-to-shipped-fix, parallel agent orchestration. Kept at public-resume level by design.)*

### Praxtera AI Institute — AI/ML Technical Leader (Executive Education) · Contract
**Sep 2025 – Present** · Philadelphia-based AI executive-education firm · concurrent with the Apple role
- **Teaches AI strategy to C-suite leaders.** Clients include **HP, Morgan Lewis, PBS, and the Philadelphia Eagles.**
- **Designed the executive curriculum** for evaluating, governing, and implementing AI initiatives, **grounded in original Wharton research** (his AI-ROI work).
- **Keynoted the Philadelphia Eagles' 12th annual Eagles Care Summit** (Lincoln Financial Field, 2026) on **"AI for Impact: Basics to Advanced Automation"** before **300+ community and business leaders.**

### Amazon — Senior Software Engineer, Alexa
**Apr 2018 – Feb 2021** (~2 yrs 11 mos) · Seattle, WA
**Scope/level:** **Promoted from SDE II (L5) to SDE III / Senior SDE (L6).** Led the **8-engineer Alexa Core Engine data team.**

Impact bullets (superset):
- **Pioneered a batching/clustering approach** to Alexa Engine data mining and modeling — **improved model accuracy 40% and saved $40M per year.**
- **Created a GraphQL-based data-aggregation platform** with intelligent caching, improving modularity and reducing latency for downstream Alexa services. *(IC resume associates the $40M/yr saving with this team-lead work; manager resume associates it with the batching/clustering work — see §15 note.)*
- **Cut partner/new-customer onboarding from 2 weeks to 15 minutes** by designing a self-service rapid-development-and-deployment platform.
- **Owned operational excellence:** established coding standards, fine-tuned metrics and alarms, identified security gaps, and **drove average weekly issue count from a peak of 40 down to 10.**
- **Re-engineered the Alexa app's new-user registration flow**, cutting **Christmas-peak customer issues by a factor of 10 (10x).**
- **Led capacity planning for traffic peaks** (Prime Day, Black Friday) — forecasted hardware requirements and made the case to management for fleet expansion ahead of demand.
- **Mentored half the team** from entry level through promotion to associate engineers; **selected for Amazon's Mentorship & Leadership Development Program.**

### Susquehanna International Group (SIG) — Senior Financial Data Engineer
**Nov 2016 – Mar 2018** (~1 yr 5 mos) · Greater Philadelphia, PA
**Scope/level:** **Promoted from Financial Data Engineer** to Senior. (IC resume tags this as a **Team Lead** role.)
- **Led real-time FINRA compliance surveillance** over the firm's market-making transactions (**C++, Python/Pandas, Django**), flagging violations as they occurred.
- **Conceived and shipped a real-time hardware asset-tracking and distribution system**, automating capacity scaling for the first time and eliminating chronic inter-team coordination failures.
- **Drove development of a real-time reporting mechanism** on the firm's market-making transactions, focused on FINRA compliance.

### Microsoft — Software Development Engineer, Windows OS Group
**Mar 2015 – Oct 2016** (~1 yr 8 mos) · Redmond, WA
*(IC resume title: "Microsoft OSG Core Software Engineer.")*
- **Set power-consumption targets for Windows 10 Mobile Mail** (Windows Phone 10 Mail / "OneSync") and **delivered a 4x reduction vs. Windows Phone 8.**
- **Drove product decisions through telemetry** — real-time dashboards and weekly guidance reports to leadership (e.g., a data-derived default auto-sync interval of 15 minutes, based on average time between manual syncs).

### Amazon Web Services (AWS) — Software Engineer Intern
**May 2014 – Aug 2014** (4 mos) · Seattle, WA
- **Unified existing logging systems** into a single general-purpose logging framework.
- Built a **Python script to construct call traces and gather metrics from logs**, serving up to **8M customers**; **achieved a 15% speedup** in the logging system. *(IC resume.)*

### LeanFM Technologies — Winter Intern, Full-Stack Web Developer
**Dec 2013 – Feb 2014** (3 mos) · Pittsburgh, PA
- **Refined 3D building-visualization software** consolidating sensor readings for building maintenance.
- Built a **Django admin interface** for building managers to control sensor-access permissions.

### Carnegie Mellon University — (three concurrent roles, ~11 mos total) · Pittsburgh, PA
- **Course Assistant, Web Applications & Development (15-437 / 15-637)** — Aug–Dec 2013: assisted **105+ students**; gave feedback on software practices and security; served as **Agile Product Owner** for the final project.
- **Web Applications Developer** — May–Aug 2013: evaluated Play!, Spring MVC, and Django for the course; built a Spring-MVC survey site with image upload deployed on Google App Engine; built a **cloud platform for course administration.**
- **Cyberphysical Systems Undergraduate Researcher (NSF-sponsored, CSSI)** — Feb–Aug 2013: built a **3D bacterial chemotaxis simulation** (to replace live-culture experiments); plotted distributions over **10M+ data points** in MATLAB.

---

## 4. Education & Academic Honors

### The Wharton School, University of Pennsylvania — Executive MBA (WEMBA Class of 2026)
**May 2024 – Mar 2026** · Completed **while working full-time at Apple.**
- **Honors:**
  - **Benjamin Franklin Award** — prestigious **peer-voted** honor for an exceptional graduate.
  - **Director's List — all 6 terms.**
  - **First Year Honors.**
- **Majors (5):** AI in Business · Business Analytics · Operations, Information & Decision-Making · Entrepreneurship & Innovation · Strategic Management.
- **Research:** First-author research on enterprise AI ROI, **published on SSRN** (faculty sponsor **Prof. Gad Allon**); foundation of his executive teaching at Praxtera. (See §5.)

### Carnegie Mellon University
- **M.S., Electrical & Computer Engineering** — **Dec 2014 · GPA 4.00/4.00.**
- **B.S., Electrical & Computer Engineering** — May 2014.
- **Minor in Business Administration** — May 2014.
- **Selected coursework (19 courses cited; CMU):** Cloud Computing (15-619), Cyber-Intelligence & Cyber-Security / Cyber-Warfare (14-809), Web Applications Development, Distributed & Real-Time Embedded Systems, "How to Write Fast Code," Java Smartphone Development, Financial & Managerial Accounting, Microeconomics I.
- **Coursera coursework cited:** Fundamentals of Quantitative Modeling, R Programming, Intro to Spreadsheets & Models, Statistical Inference, Machine Learning, Foundations of Scala Programming, Programming with Google Go.

---

## 5. Publications & Thought Leadership

> Four works confirmed on ORCID via Crossref (DOIs below) plus the CMR working paper. Author name appears as "Krishnan, S."

### A. "Who Trains the Next Senior? Managing Engineering Teams When AI Makes Code Cheap"
- **Status:** **In-Depth Article, submitted to *California Management Review* (CMR / UC Berkeley Haas)**, ScholarOne manuscript (Draft ID), "For Review Only." Topic: Generative AI.
- **Authors:** Krishnan, S., with co-author **Gajendra Babu Thokala** (the manager-track resume lists this as **"Breadth Without Depth: Steering the AI Inversion of Software Engineering," SSRN posting forthcoming** — same body of work; see §17 on title/venue reconciliation).
- **Thesis (his argument):** Generative and agentic AI have made the *breadth* of software engineering (plausible, conventional code) nearly free; the **first casualty is the junior engineer**, whose old work — boilerplate, well-specified tickets, first-pass tests/debugging — was both the production *and* the apprenticeship. Cheap breadth raises the value of two scarce human contributions: **depth** (judgment of which answer is right in *this* system) and **divergence** (the perspective outside the consensus). Left to inertia, firms slide into a **"substitution" equilibrium** — hollowed-out review ("review theater," where the signature stays but verification drains out), a starved apprenticeship, and output that converges on the model's mean. The alternative, **"complementarity,"** is a set of concrete management moves: **(1) shrink the unit of review** (atomic, single-responsibility PRs, now enforceable because the producer is an agent); **(2) tier scrutiny by consequence** (synchronous, senior-led review for high-stakes change; async-with-agent for the rest); **(3) measure what is scarce** (verified outcome, depth transfer, divergence — not lines of code); and **(4) rebuild the apprenticeship on purpose** (juniors as "directors of agents" under senior mentorship). Grounded in a worked **enterprise data-pipeline case** with a labor-share table projecting agent absorption to ~2032, plus a "Risks & Conditions of Reversal" section (incentives/"adoption theater," capability-vs-reliability, the pipeline/human-capital risk). Strong, citable, leadership-defining thought leadership directly on his target market.

### B. "A Multi-Layer Framework for Evaluating the Return on Investment of AI Projects"
- **Authors:** Krishnan, S.; **Hepp, A.; Gandhi, S.** (2026).
- **Venue:** **SSRN.** **DOI: 10.2139/ssrn.6732598.**
- Basis of the **AI ROI Framework** product (§6) and the Praxtera curriculum. Synthesizes **8 enterprise case studies across 4 analytical layers** (organizational readiness / SCALE; ROIC decomposition; stage-gate investment; decision scorecard).

### C. "Drone-Megaddon 2026: Co-Intelligent Swarm Control with Language and Vision Models"
- **Authors:** Krishnan, S.; **Ting, D.** (2026).
- **Venue:** **engrXiv**, preprint. **DOI: 10.31224/6987.** (ORCID/Crossref: posted 2026-06-10.)

### D. "Drone-Megaddon: A Real-Time Strategy Interface for Managing Drone Swarms"
- **Authors:** Krishnan, S.; **Ting, D.** **Venue:** **engrXiv**, 2026 (preprint of 2014 CMU capstone work). **DOI: 10.31224/6924.** (ORCID/Crossref: posted 2026-06-10.)

---

## 6. AI Ventures / Projects (independent, built end-to-end)

> Designed, architected, coded, and operated solo — concept to deployment. Read at source level. These are the spine of the "still bleeds on the field" brand: a manager who personally ships graph systems, multi-provider LLM orchestration, and full-stack products, then red-teams his own code.

### Ondoway — graph-backed audio-tour platform
- **What:** A Neo4j knowledge graph of city points-of-interest and narrative "beats" powering GPS-triggered, personalized audio walking tours ("a local storyteller in your pocket"). Launch city: Paris.
- **Graph model:** Versioned, event-centric, **CIDOC-CRM-aligned** schema — **7 core MVP entity types** (User, Profile, Trip, ItineraryItem, POI, NarrativeBeat, Lens) and **11 relationship types** (HAS_PROFILE, IS_CAPTAIN_OF, IS_CREW_OF, PREFERS_LENS, HAS_STOP, ASSIGNED_TO, AT_POI, PLAYS_BEAT, HAS_BEAT, TAGGED_WITH, IS_PARENT_OF), several as reified edges carrying their own properties. *(Live code has since grown to 8 nodes / 12 relationships, adding `Area` + `WITHIN` containment — a documented expansion.)* Controlled vocabularies, canonical IDs, per-fact provenance. **Lens taxonomy:** 8 parent genres + 21 child sub-genres.
- **Stack:** **Python 3.11 + FastAPI** (JWT + Google/Apple Sign-In + email auth, `slowapi` rate limiting); **Neo4j 5.28** (POINT spatial indexes for geo); **Flutter (Dart)** mobile app (~26 Dart files; `apple_maps_flutter`, `geolocator`, `just_audio`); geo via OpenStreetMap → Google Maps; storage on **AWS S3**.
- **AI/audio:** **Dual-provider TTS** behind a `TTSProvider` protocol — OpenAI TTS (dev) / **ElevenLabs `eleven_multilingual_v2`** (prod) — stereo 256kbps/44.1kHz MP3; generative narration "glue" via **Anthropic Claude Haiku** (`claude-haiku-4-5`), content extraction/fact-check via **Google Gemini**. LLM is constrained to glue templates can't cover, behind a mock for deterministic tests, with **sentence-level provenance** (every output sentence traces to a NarrativeBeat UUID or a whitelisted glue label) so AI can't fabricate.
- **Scope:** 16 REST content-API endpoints; a ~25-module deterministic tour engine (beat selection, density, routing, grading, audit) in two modes (Planner / Wanderer); a browser canvas-based force-directed **graph editor** plus a Leaflet "Editorial Workbench" with cosine-similarity conflict detection; **177 tests** with a **CI tour-grading regression gate** scoring generated tours against human-curated golden tours.
- **Proves:** Senior-architect knowledge-graph modeling judgment (documents what he deliberately *skips* — RDF/SPARQL, OWL, embeddings — and the triggers to revisit); one person owning graph + backend + ML/audio pipeline + generative content + interactive authoring frontend + Flutter mobile with GPS geofencing.

### Persuaider — AI negotiation-/persuasion-training platform
- **What:** Admins author negotiation scenarios with in-character AI personas; learners practice live; an LLM evaluates each session and returns scored, framework-based feedback (built-in **CLEAR** and **AIDA** frameworks plus admin-defined weighted frameworks; 0–100 score, per-framework weighted scores, 3–5 "winning arguments").
- **Stack:** **TypeScript / Next.js 16** (App Router), **React 19.2**, **Tailwind v4**; **Prisma 6** over **SQLite (dev) / PostgreSQL (prod)** (11 data models); **Clerk** auth (migrated off NextAuth mid-project; Clerk webhooks + `svix`); **Upstash Redis** rate limiting; React-PDF report export; hosted on **Vercel** (~$0.07/session).
- **LLM orchestration:** **Three-tier multi-provider chain with pinned model versions** — **Anthropic Claude Sonnet 4.5** (primary) → **Google Gemini 2.0 Flash** (backup) → **OpenAI GPT-5.2 Instant** (fallback) — via a `LLMProviderChain` with exponential backoff (3 retries, 1s→30s, 2×), retryable-vs-terminal error classification, transparent mid-conversation failover, and monitoring hooks. Model versions hardcoded so "upgrades go through code review." LLM in three agentic roles: persona simulation, rubric-based evaluation (3-strategy defensive JSON parser), and **scenario generation from a prompt OR an uploaded document.**
- **Scope:** ~12,875 lines of non-test TS/TSX; 24 React components; ~65 API route handlers; 14 documented user pathways across 3 actor types; **1,246 Jest unit tests + 15 E2E, 0 skipped** (grown 725 → 792 → 1,246, incl. 67 security/middleware tests and dedicated red-team test files); dual Selenium *and* Playwright E2E.
- **Proves:** Production-grade multi-provider LLM orchestration (not a single-API wrapper), genuine full-stack ownership, and real operational maturity ("0 skipped" rule, dedicated security/red-team layer).

### DependIQ (renamed "Lore") — cross-repo dependency impact / "blast radius" analysis
- **What:** Multi-tenant web app that builds a cross-project dependency graph over a workspace of repos and computes the **"blast radius"** of a dependency change — given a package upgrade, shows which projects across the org break, in dependency order, with a streaming LLM explanation of *why*. Positioned as **"the verification layer AI coding agents lack."** (`pyproject` name `lore` v0.2.0; renamed from DependIQ 2026-06-10.)
- **Stack:** **Python 3.11 + FastAPI** (async SQLAlchemy 2.x, `asyncpg`, Pydantic v2); **polyglot persistence — PostgreSQL 14+** (identity, workspaces, history) **+ Neo4j 5.x with APOC** (the dependency graph); **WorkOS AuthKit** auth; frontend deliberately **HTMX + Jinja2 + Alpine + Tailwind, no React / no build step**; hosted on **Render**; "200+ tests."
- **LLM:** Provider-agnostic via **litellm** with a custom **model router** — **11 `TaskType`s** (MANIFEST_PARSE, DEPENDENCY_EXTRACT, SECURITY_ANALYSIS, CHAIN_REACTION, etc.) tiered across **Anthropic Claude (haiku-4-5 / sonnet-4 / opus-4), OpenAI (gpt-4o / -mini), and local Ollama** (qwen2.5-coder, deepseek-coder-v2, llama3.1) in four modes — QUALITY / BALANCED / COST / **LOCAL_ONLY** (privacy) — each with failover chains.
- **Graph algorithm:** Hand-written Cypher starting from a `Package`, finding directly-affected projects, then traversing inter-project `RELATES_TO` semantics (`imports_from`, `calls_api`, `shares_db`, `shares_package`) up to **5 hops** via `shortestPath`, returning each with distance + impact type, severity-bucketed by hop distance, 1-hour TTL cache. Design-target scale ≈ 50,000 Package nodes (100 projects × 50 packages × 10 tenants).
- **Proves:** Real graph-systems and graph-algorithm work; deliberate polyglot persistence with explicit reasoning about the dual-write atomicity gap; and — a strong leadership signal — he **commissioned/authored a brutally honest senior-graph-engineer audit of his own code** (Critical/High bugs with file:line evidence and a prioritized fix plan) alongside an investor-grade competitive/moat memo.

### AI ROI Framework (airoi) — interactive AI-investment decision tool
- **What:** Single-page decision-support tool operationalizing his Wharton research (WEMBA 50): **8 enterprise case studies across 4 analytical layers**, synthesized into a usable framework. Headline framing: "**80% of AI projects fail** — this framework helps you avoid being one of them." Live at **saiwebapps.github.io/airoi**.
- **4 analytical layers (sequential):** **Layer 0 SCALE Assessment** (invest at all? → Go/No-Go) · **Layer 1 ROIC Decomposition** (where AI creates value) · **Layer 2 Stage-Gate Investment** (how to phase spend) · **Layer 3 Decision Scorecard** (A–F grade) — plus a novel **8-category risk-adjustment table** tuning the discount rate.
- **8 case studies (2×4: Build/Validate × B2B/B2C/Platform/Internal):** Salesforce/Palantir, Spotify/Duolingo, Shopify/Uber, JPMorgan/NatWest (discount-rate range 19.25%–25.5%; Apple Intelligence appears as a 9th cautionary counter-example).
- **Stack:** Pure static, hand-authored — **100% vanilla HTML/CSS/JS, no build system, no dependencies, no CDNs**; one self-contained 1,130-line `index.html`; GitHub Pages. Source paper is a ~1,157-line academic doc grounded in SEC filings + McKinsey/BCG/MIT/RAND data.
- **Proves:** Bridges rigorous graduate research with a shipped public product; range across finance/strategy (DCF, ROIC, risk-adjusted discounting), AI build-vs-buy judgment, and front-end delivery — same person did the analysis and shipped the interface.

---

## 7. Open-Source & Tooling

### claude-kit — open-source agentic-AI tooling kit for Claude Code (github.com/SaiWebApps)
- **What:** A kit that encodes disciplined engineering practice into an AI coding agent — slash-command **skills**, multi-perspective **agent** definitions, reusable skill-building **patterns**, and mechanically-enforced behavioral hooks.
- **Ships:** **10 skills, 10 agents, 4 patterns.** Format: Markdown `SKILL.md` + YAML frontmatter; ~31 `.md`, ~15 JS files (a Node verification engine), ~8 `.sh` (Bash installer + enforcement hooks). Flagship `workflows/forge.js` backed by **13 committed Node test files**.
- **Key skills:** **`forge`** (multi-perspective answer engine with hostile, evidence-gated verification behind a deterministic JS gate — "beat a lazy, lying, shallow-exploring Claude": parallel generators, per-claim skeptics that re-open each cited `file:line` and confirm the quoted bytes, up to 3 adversaries; **PASS requires positive evidence, never the mere absence of objections**); **`build-fix`** (iterative JVM build-fix, max 5 cycles, minimal fixes, never skip a failing test to go green); plus `ship`, `retro`, `error-diagnosis`, `prwalk`, agent-management skills. **10 agents** each carry an explicit authority rank (architect=1 … ops/user-advocate=5) and persistent per-agent `MEMORY.md`; conflicts merge in authority order. **4 patterns:** observe / mutate / verify / pipelines, each with a runnable example.
- **Thesis it proves:** An LLM coding agent must be **treated as an adversary and disciplined with code, not prose** — applying classical software discipline (adversarial verification, test-first, deterministic gating, honesty contracts) to make autonomous agents trustworthy. Directly operationalizes the CMR paper's "deterministic scaffolding outside the model" argument.

### Earlier / notable projects (CMU + personal — IC resume "Projects" + LinkedIn)
- **Amazon Machine Learning Hackathon (AWS):** OpenCV image-matching to detect whether two warehouse bins held the same objects; ensemble (feature-matching vs. contour/canny-edge) with averaged confidence; addressed a real Amazon Fulfillment / Kiva Robots problem.
- **N-an-Instant (CMU):** custom "Google Instant" from n-grams over a 10,000-book corpus + Bayesian statistics; Hadoop; TableReducer into HBase; PHP backend → jQuery autocomplete.
- **Drone-Megaddon (CMU, Fall 2014):** end-to-end cyberphysical system where a high-level, StarCraft-like RTS interface controls drone swarms. (Now published — see §5C/§5D.)
- **End-to-End AWS Cloud Service (CMU):** 2nd most cost-effective/performant RESTful API analyzing a 200 GB Twitter corpus; Elastic MapReduce ETL into HBase.
- **Twitter Hashtag Similarities (CMU):** 50 GB corpus co-occurrence counts via Hadoop; **78% speedup** over the default solution.
- **Wikipedia Page-Views Timeline (CMU):** monthly view counts via Elastic MapReduce on a **$20 operating budget.**
- **LinkedIn Extractor (2016):** NodeJS API to extract LinkedIn profile details; used to build a professional website for his father.
- **Bing Rewards Points Bot (2015); Synonyms Crawler (2015, D3.js tree); Real-Time Embedded Linux Kernel (2014, energy-aware RTOS); Embedded Capstone "Hand-2048" (2014, Raspberry Pi + Asus Xtion Pro motion sensing); MedHub (2014, crowdsourced medical-issues Android app); Discrete-Time Elevator Simulation (2013, CAN-network Java); Stock Exchange Web Application (2013, J2EE/MySQL with bot AI); Image Taxonomy Interface (DynamoDB, 256 categories / 30,607 images).**

---

## 8. Speaking & Teaching

- **Praxtera AI Institute — guest/contract instructor (Sep 2025 – Present):** executive-education program on **AI strategy and business integration**; designed curriculum for C-suite leaders on evaluating, governing, and implementing AI initiatives. **Clients: HP · Morgan Lewis · PBS · Philadelphia Eagles.**
- **Eagles Care Summit keynote (2026):** keynoted the **Philadelphia Eagles' 12th annual Eagles Care Summit** at **Lincoln Financial Field** — **"AI for Impact: Basics to Advanced Automation"** — before **300+ community and business leaders.**
- **Wharton research → public artifacts:** AI-ROI framework (SSRN paper + interactive tool); CMR working paper on AI and engineering management.
- **CMU Course Assistant (15-437/15-637, 2013):** taught/assisted **105+ students**; Agile Product Owner for the capstone.
- **Recommendation corroboration:** described as a "compelling storyteller, equally effective with colleagues, senior stakeholders, and board-level audiences" (Jonas Pulver, §14).

---

## 9. Honors & Awards

- **Benjamin Franklin Award** — The Wharton School (peer-voted honor for an exceptional graduate), 2026.
- **Director's List — all 6 terms**, Wharton Executive MBA.
- **First Year Honors**, Wharton Executive MBA.
- **Amazon Mentorship & Leadership Development Program** — selected participant (Amazon, ~2018–2021).
- **2010 National Merit Finalist** — National Merit Scholarship Program (May 2010).
- **Jesse Jones Scholarship** — Houston Endowment (Jesse H. and Mary Gibbs Jones Scholars), May 2010.
- **(1 more Honors & Awards item listed on LinkedIn — not yet captured; see §17.)**
- **Academic:** CMU M.S. GPA **4.00/4.00.**

---

## 10. Certifications

> LinkedIn shows **"Licenses & Certifications (9 total)"**; only two are captured verbatim so far. The remaining seven are listed in §17 NEEDS CONFIRMATION. Coursework that may correspond to certificates appears in §4.

1. **Mathematics for Machine Learning Specialization** — Coursera — Jan 2021 (Credential ID **AF6BVULTK5KW**).
2. **Become a Thought Leader** — LinkedIn (Learning) — Jan 2021.
3–9. *(7 more — to confirm; likely drawn from the Coursera/CMU list in §4: e.g., Machine Learning, Statistical Inference, R Programming, Foundations of Scala Programming, Programming with Google Go, Fundamentals of Quantitative Modeling, Intro to Spreadsheets & Models.)*

---

## 11. Skills (grouped)

**Leadership & Management**
Cross-functional & multi-site team leadership (Seattle / London / Cupertino / Singapore / EU & LatAm vendors) · people management of 8-engineer teams (Apple, Amazon) · program / project management · mentorship & talent development (promoted half a team; CMU TA for 105+) · hiring · roadmap & ownership · performance-review input · engineering process design (design-review, code-review, CI/CD standards) · executive communication & public speaking · stakeholder management · incident command · capacity planning · operational excellence.

**Data & ML Platforms / Distributed Systems**
Knowledge graphs · entity resolution / deduplication (similarity mapping, K-Means clustering) · graph databases (Neo4j; Cypher; APOC; spatial/POINT indexes) · stream processing (**Apache Flink, Kafka**) · batch & big data (**Apache Spark, Hadoop, HBase, Elastic MapReduce**) · **Cassandra**, MongoDB, DynamoDB, PostgreSQL, MySQL, Azure Cosmos DB/SCOPE · **GraphQL** · **Protobuf / Avro** · distributed systems at **100M+ user scale** · data quality & lineage · OpenCV / computer vision.

**Applied AI / Agentic Systems**
LLM application development (**Claude / Anthropic API**, Gemini, OpenAI; multi-provider failover chains with pinned versions) · **agentic systems & MCP (Model Context Protocol)** · AI-assisted engineering operations (LLM ops assistant over logs/traces/metrics; agentic skill platforms) · adversarial verification / evidence-gated agent workflows · RAG concepts · AI strategy, governance & **ROI evaluation** · prompt/scenario generation; TTS pipelines (ElevenLabs/OpenAI).

**Cloud & Infra / Tooling**
AWS (CloudWatch, SNS, S3, EBS, EC2, Elastic MapReduce, DynamoDB) · Microsoft Azure (Cosmos DB, SCOPE QL) · Google App Engine / Cloud · Heroku · Vercel · Render · Docker / Docker Compose · CI/CD · Redis (Upstash) · Git / Subversion / Perforce · Selenium / Playwright · Linux / Windows · HTTP/SSL/TCP-IP.

**Programming Languages**
Java · Scala · Python 2/3 (+Pandas) · Go · **C / Embedded-C · C++** · C# · TypeScript / JavaScript (React, Next.js, Node.js, Express) · PowerShell · Bash / Zsh / Awk / Perl · HTML/CSS · MATLAB / GNU Octave · R · Dart (Flutter). *(Embedded/parallel: OpenMP, SIMD, CUDA, Arduino, Raspberry Pi, OpenNI.)*

**Frameworks / General**
FastAPI · Django · Spring MVC · Play! · Hibernate · J2EE · Prisma · SQLAlchemy · HTMX / Jinja2 / Alpine · Tailwind · Bootstrap · ASP.NET MVC · jQuery / AJAX · React-PDF.

---

## 12. Spoken Languages (6)

- **English** — Native / bilingual.
- **Tamil** — (heritage; resume-listed).
- **Spanish** — (resume-listed).
- **French** — (resume-listed).
- **Italian** — (resume-listed).
- **Chinese** — Limited working proficiency (LinkedIn). *(Resume lists Chinese among the six; proficiency levels for Tamil/Spanish/French/Italian not specified — see §17.)*

---

## 13. Volunteering (6 total per LinkedIn; 2 captured verbatim)

1. **The Art of Living** — Volunteer, **Economic Empowerment** — **May 2010 – Feb 2025** (14 yrs 10 mos).
2. **Connect at Seattle** — Fundraising Volunteer & Mentor, **Education** — **Apr 2018 – Aug 2025** (7 yrs 5 mos): organized blood drives; worked with **Mary's Place** to feed the homeless and clean shelters; instructs professionals in CS and finance in **employment-retraining programs.**
3–6. *(4 more volunteering entries listed on LinkedIn — not yet captured; see §17.)*

---

## 14. Recommendations (quotes)

> LinkedIn: **7 received, 2 given.** Two received are captured verbatim.

**Jonas Pulver** — Head of Communications & Culture, Swiss Embassy in Japan; Wharton MBA; UTokyo MA; JLPT N1 (studied together at Wharton; May 4, 2026):
> "Sai is one of the most impressive peers I met at Wharton. He combines deep technical expertise in AI and engineering with genuine empathy, strong intrinsic motivation, and a rare ability to bring together individuals with very different perspectives... He leads with clarity and purpose, consistently elevating the performance of those around him... not only develops sharp, well-structured solutions, but brings them to life as a compelling storyteller, equally effective with colleagues, senior stakeholders, and board-level audiences. I am confident Sai will excel as a high-impact manager and a purpose-driven leader."

**Gajendra Babu Thokala** — Senior Engineering Leader at Apple; "Built AI & Data Platforms Serving 100M+ Users"; ex-Microsoft; co-author on "Breadth Without Depth" (senior to Sai, not direct manager; April 18, 2026):
> "I've worked with Sairam for about 4 years on the Knowledge Graph team at Apple... deep commitment to his work; if there is something that needs to be completed, he acts on it immediately... a relatively rare combination of both solid technical ability and a sense of ownership... learns context rapidly, accelerates into new domains quickly, collaborates well... a consistent source of calmness during stressful periods... Sairam will make a tangible impact on any engineering organization."

*(5 more received + 2 given — to be captured; see §17.)*

---

## 15. Quantified-Impact Bank

> Every citable metric, tied to the role it belongs to. Use verbatim; do not inflate.

**Apple (Principal SWE, Knowledge Graph, 2021–present)**
- **100M+ users** served by the media knowledge graph (search / recommendations / discovery).
- **15+ data sources** unified into one canonical model.
- **40%** data-quality improvement from ML entity-resolution/dedup.
- **30%** increase in team velocity (engineering-bar standards).
- **45%** reduction in production incidents.
- **15-engineer** program across **4 international sites** for the Apple Music Credits launch; **millions of tracks** with real-time credits curation.
- **8-engineer** team led; multi-site (Seattle, London, EU & LatAm vendors).

**Amazon (Senior SDE, Alexa, 2018–2021)**
- **$40M per year** saved (batching/clustering approach to Alexa Engine data mining/modeling). *(Note: IC resume attributes the $40M/yr to the GraphQL data-aggregator team-lead work; manager resume attributes it to the batching/clustering work. Same role, same year, same number — pick one attribution per document; do not double-count.)*
- **40%** model-accuracy improvement (same initiative).
- Partner/customer onboarding **2 weeks → 15 minutes** (self-service deployment platform).
- Weekly issue count **40 → 10** (operational excellence).
- **10x** reduction in Christmas-peak customer issues (re-engineered registration flow).
- **8-engineer** Alexa Core Engine data team led; mentored **half the team** to promotion.

**SIG (Senior Financial Data Engineer, 2016–2018)**
- Real-time FINRA compliance surveillance over the firm's market-making transactions (first-time automated capacity scaling).

**Microsoft (SDE, Windows OS, 2015–2016)**
- **4x** reduction in Windows 10 Mobile Mail power consumption vs. Windows Phone 8.
- Data-derived default auto-sync interval (15 min) shipped from telemetry.

**AWS Intern (2014)**
- Logging framework serving up to **8M customers**; **15%** logging speedup.

**CMU / projects**
- **10M+ data points** plotted (NSF cyberphysical research).
- **78%** speedup (Twitter hashtag similarities, Hadoop).
- **$20** operating budget (Wikipedia page-views pipeline).
- **105+ students** supported as TA.

**Ventures (self-built; show hands-on rigor)**
- Persuaider: **1,246 unit tests + 15 E2E, 0 skipped**; ~12,875 LOC; 3-tier LLM failover; ~$0.07/session.
- Ondoway: **177 tests** + CI tour-grading gate; 7→8 entity / 11→12 relationship Neo4j graph; sentence-level provenance.
- DependIQ/Lore: 5-hop blast-radius graph traversal; 11 LLM TaskTypes; 4 routing modes incl. local-only privacy; "200+ tests"; design-target ~50,000 nodes.
- AI ROI: **8 case studies × 4 layers**; self-contained 1,130-line zero-dependency app.
- claude-kit: 10 skills / 10 agents / 4 patterns; 13 test-driven verification suites.

**Thought leadership**
- CMR working paper (UC Berkeley) on AI + engineering management; SSRN AI-ROI paper (DOI 10.2139/ssrn.6732598); 2 engrXiv preprints (DOIs 10.31224/6987, 10.31224/6924).
- Praxtera: taught **HP, Morgan Lewis, PBS, Philadelphia Eagles**; keynote to **300+** at Eagles Care Summit.

---

## 16. Proof-Point Bank (for headlines / About)

Ready-to-use, all factual:

1. **"Leads the 8-engineer team behind Apple's media knowledge graph — the platform powering search, recommendations, and discovery for 100M+ users."**
2. **"Saved $40M/yr at Amazon Alexa with a batching/clustering ML approach that also lifted model accuracy 40%."**
3. **"Raised the bar: +30% team velocity, −45% production incidents, +40% data quality."**
4. **"Wharton Executive MBA (Class of 2026) — Benjamin Franklin Award (peer-voted), Director's List all 6 terms — earned while working full-time at Apple."**
5. **"Still bleeds on the field: personally built Apple's LLM-powered ops assistant (logs + traces + metrics over MCP) and an agentic skill platform now used on-call."**
6. **"Published researcher on AI + engineering management — California Management Review working paper; SSRN AI-ROI framework (faculty sponsor Prof. Gad Allon)."**
7. **"Ships graph systems for real: two independent Neo4j knowledge graphs and a 5-hop dependency 'blast-radius' engine — designed, coded, and red-teamed solo."**
8. **"Teaches AI strategy to the C-suite — HP, Morgan Lewis, PBS, and the Philadelphia Eagles; keynoted the Eagles Care Summit to 300+ leaders."**
9. **"Cut Alexa partner onboarding from 2 weeks to 15 minutes and Christmas-peak customer issues 10x."**
10. **"Open-source author of claude-kit — disciplining AI coding agents with adversarial, evidence-gated verification (10 skills, 10 agents, test-driven gates)."**
11. **"11 years across Apple, Amazon, Microsoft, and SIG — promoted at Amazon (SDE II/L5 → Senior SDE/L6) and SIG."**
12. **"Equally effective in an architecture review, an executive briefing, or a 2 a.m. incident bridge."**

---

## 17. Needs Confirmation

**Publications / titles**
- **CMR paper title:** the live CMR submission is titled **"Who Trains the Next Senior? Managing Engineering Teams When AI Makes Code Cheap"**; the manager-track resume cites the same work as **"Breadth Without Depth: Steering the AI Inversion of Software Engineering"** (SSRN forthcoming). Confirm which title is the final/public one (likely a retitle for CMR vs. an SSRN working-paper title), and the final venue/status before publishing in resume/LinkedIn. Co-author **Gajendra Babu Thokala** confirmed.
- **engrXiv Drone-Megaddon entries** post-date the original 2014 work (Crossref shows 2026-06-10). Confirm co-author **"D. Ting"** full name and whether both preprints should be listed or consolidated.
- AI-ROI co-authors **A. Hepp** and **S. Gandhi** — confirm full names/affiliations for citation.

**Certifications (9 total on LinkedIn; 2 captured)**
- Need the remaining **7** certification names/issuers/dates/IDs. Candidates (from coursework) listed in §10 but must be verified against the actual LinkedIn "Licenses & Certifications" section.

**Honors (3 total on LinkedIn; 2 captured + program)**
- One additional Honors & Awards entry on LinkedIn not yet captured.

**Volunteering (6 total; 2 captured)**
- Four additional volunteering entries to capture.

**Recommendations (7 received / 2 given; 2 captured)**
- Five more received + two given to capture (names, roles, quotes).

**Languages**
- Proficiency levels for **Tamil, Spanish, French, Italian** not specified (only English = native, Chinese = limited working). Confirm honest self-assessed levels before publishing.

**Dates / titles to reconcile across sources**
- LinkedIn lists the Apple title as **"Principal Software Engineer"** with tenure "5 yrs 5 mos"; resume start is **Feb 2021**. Consistent. Confirm whether to surface "Principal" (level) vs. a manager-track framing for target roles.
- Amazon level: resumes say **SDE II (L5) → SDE III / Senior SDE (L6)**. LinkedIn says "Promoted from SDE II (L5) to SDE III (L6)." Consistent; confirm preferred external phrasing ("Senior SDE").
- **$40M/yr attribution** (Amazon) differs between the two resumes (batching/clustering vs. GraphQL aggregator). Decide a single attribution per document (see §15).
- **Wharton 4th education entry:** LinkedIn "Education (4 total)" — entries are Wharton EMBA, CMU M.S. (ECE), CMU B.S. (ECE) + Minor (Business Admin). Confirm whether the 4th is a separate listing (e.g., a high-school/other) or just the BS/Minor counted separately.
- **Ondoway / DependIQ "renamed Lore":** the brief says **DependIQ** was renamed "Lore." The repos confirm **DependIQ → Lore** (pyproject `lore`). The resume still lists "DependIQ." Decide which name to use publicly (and note Ondoway is unrelated).
- **Apple team size:** "8-engineer team" (current resume) vs. earlier "15 engineers" framing for the Apple Music Credits *program* specifically. Both true at different scopes — keep "8-engineer team" for steady-state line management and "15-engineer program across 4 sites" for the Credits launch.

**Other**
- Confirm whether **Praxtera AI Institute** should be presented as employment, contract, or advisory on LinkedIn/resume (currently "Contract," concurrent with Apple).
- Personal venture repos are private/solo; confirm which (if any) are public and linkable (airoi is public on GitHub Pages; persuaider/ondoway/dependiq/claude-kit status to confirm before linking on a public site).
