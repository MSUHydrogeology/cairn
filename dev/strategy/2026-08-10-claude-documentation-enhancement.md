<!-- claim-check-allow: docs/related-practices.md, docs/glossary.md, docs/assets/lifecycle-states.svg, docs/assets/module-map.svg, docs/assets/where-cairn-sits.svg, scripts/gen_docs_figures.py -->
<!-- ^ Surfaces this note PROPOSES creating; they deliberately do not resolve
     yet. Marked rather than asserted, per AGENTS.md > Verifying claims. Every
     measured figure below names the command that produced it. -->

# Cairn documentation enhancement — the front door, the feature story, and the visual system

**Author**: Claude (Strategy)
**Model**: Opus 5
**Date**: 2026-08-10
**Status**: revised (External round 1 — Codex, different agent type — folded in
and removed 2026-08-10; the arc is in `git log`, not this body)
**Type**: design-exploration
**Supersedes**: `2026-06-04-claude-documentation-graphics.md` (archived on the
same commit as this note). That note was authored from **modflow_tools'**
vantage; its production model is methodology-portable and is carried forward
here in Cairn's own terms, while its hydrogeology figure inventory is not.
**Surfaces this would feed**: a README-rewrite proposal; the `dev/PLANNING.md`
row **"0.4 launch-surface polish"** (graphics/figures in the adopter-facing
docs + quickstart), which already exists and does not need a new one; the
unstruck **B3** items of `2026-07-08-claude-broad-look-skeptical-review.md`
(related practices, the two-sentence pitch, a glossary, stripping the internal
codes).

---

## The question / felt gap

The Maintainer's framing: *build a better and more attractive set of
documentation, starting with the main README, listing the key features — the
things Cairn does that make it better than vibe coding.*

Two gaps sit under that, and they are not the same gap.

**The enticement gap.** Cairn's front door leads with *recognition* (a pain
list) and *contrast* (an ad-hoc-vs-Cairn table), then narrates. What it never
does is **enumerate**. A reader who lands on `README.md` asking "what do I
actually get?" has to assemble the answer out of five prose sections and a
repository-layout table. Cairn has a genuinely long feature list — most of it
shipped, tested, and unusual — and none of it is *scannable*.

**The comprehension gap.** Cairn's hardest concepts are exactly the ones prose
serves worst: two review tiers crossed with structural independence; a
four-state proposal lifecycle feeding a five-state plan lifecycle; six
adaptation axes selecting three module layers; four verification boundaries
with different evidence bars. These are *state machines and matrices*
explained in paragraphs. A reader re-derives from prose what one diagram
would settle.

The honest open question this note explores: **is the fix a README rewrite, a
visual system, or both — and what has to be true before the first image
lands?** It is not a foregone conclusion that Cairn needs pictures; the
alternative (prose-only clarity plus the two missing skeptic answers) is on
the table and named below.

## Method *(grounded, falsifiable — verify-before-asserting)*

Every figure below is measured against this tree on 2026-08-10, not recalled.
The commands are given so a reader can falsify them.

* **Visual coverage — anchored, so the search cannot match its own
  documentation.** A naive `grep -lE '!\[[^]]*\]\('` matches the *example*
  patterns quoted inside this note, and returns this note. The measurements
  below use line-anchored forms that distinguish a real asset from a quoted
  one: `git ls-files '*.md' | xargs grep -lE '^[[:space:]]*!\[[^]]*\]\('` for
  image embeds, and `... grep -l '^```mermaid'` for fence openings at column
  zero. Both return `README.md` alone.
* **Corpus size** — `git ls-tree -r --name-only <commit> | grep -E '\.md$' |
  wc -l`, bucketed by top-level directory. Pinned to a commit rather than the
  working tree, because the count moves with any commit that adds a file —
  including this one.
* **Asset inventory** — `git ls-files 'docs/assets/*'`.
* **Missing surfaces** — direct `ls` for `CONTRIBUTING.md`,
  `docs/glossary.md`, `docs/related-practices.md`.
* **Internal codes in the front door** — `grep -n 'R-[A-Z]\|G/M/P\|chunk
  [0-9]' README.md`.
* **The image gate, perturbation-tested rather than read** — a deliberately
  broken image reference was appended to a tracked file, `scripts/link_check.py`
  was run, the flag and exit code observed, and the file restored to a clean
  working tree. This is the non-vacuous form; reading the regex alone would
  not have established it.
* **Prior deliberation read in full** — every note in `dev/strategy/`, plus
  `docs/DOCUMENTATION_PLAN.md` and `dev/strategy/MIGRATION.md`.

**What would falsify the central recommendation:** if a reader survey (or the
first third-party adopter) reported the front door was clear and the missing
piece was elsewhere, the enticement finding collapses and this becomes a
comprehension-only exercise. The measured findings (F1, F3) would survive;
the *ordering* in the Recommendation would not.

## Findings

### F1 — The entire visual surface is one file

**282 tracked Markdown files** *(as of `d026440`)*. **Exactly one contains an
image; exactly one contains a diagram. They are the same file: `README.md`.**

*A live demonstration of F4, on this page.* The first draft of this note said
281, measured minutes before the commit that added the note itself — the figure
was stale within one commit of being written. The same draft's search commands
matched the examples quoted in their own Method section and returned this note
as a second "file with visuals." Both are exactly the class of failure F4 warns
the README's feature list against: a hand-measured number with no snapshot
anchor, and an instrument that does not distinguish a real asset from a
description of one. The conclusion survived both defects, which is the useful
part — but a reader is entitled to see the correction rather than a tidied
number.

| Surface | Files | Visuals |
|---|---|---|
| `README.md` | 1 | 2 image embeds (banner, Dual-Review SVG) + 1 Mermaid fence |
| `doctrine/` | 16 (5,547 lines) | **0** |
| `docs/` | 11 (1,814 lines) | **0** |
| `dimensions/` | 7 | **0** |
| `templates/` | 69 | **0** |
| `bootstrap/` | 12 | **0** |
| `case-studies/`, `examples/`, `on-ramp/` | 8 | **0** |

`docs/assets/` holds **two** files: `cairn-banner.svg` and
`dual-review-independence.svg`. The lifecycle state machine — arguably the
single most-explained concept in the repository — is drawn exactly once, as a
Mermaid fence in the README, and never again in the doctrine that defines it.

This is a stronger version of the gap the superseded note diagnosed in
modflow_tools, and it is more consequential here: Cairn's product **is** the
prose. A methodology repository whose 16-file doctrine corpus contains no
diagram is asking every reader to hold four interacting state machines in
their head from text alone.

### F2 — The README does the hard part well and skips the easy part

Credit where the audits already gave it: the front door carries the
pain-recognition hook, the honest "slower for the first few changes" framing
(consistent across four surfaces, per the 2026-06-12 friction audit), the
single-agent reassurance, the trust-and-safety box the same audit called
"exactly the nuance a scientist needs," and a faithful lifecycle diagram.
None of that should be disturbed.

What is missing is the cheapest thing in documentation: **a scannable list of
what the thing does.** Cairn's features are currently dissolved into narrative
("Cairn has four jobs"), into a repository-layout table that describes
*directories* rather than *capabilities*, and into doctrine the reader has not
opened yet. The reader who wants to know whether Cairn is worth twenty minutes
never gets a list.

### F3 — The two answers to the skeptic are still missing, and the front door still speaks in internal codes

Verified against this tree, not carried forward from the review that first
raised them (`broad-look-skeptical-review`, Theme 6 / item **B3**, which
remains **unstruck — i.e. unverified, not necessarily outstanding**; these
four are now re-verified as genuinely outstanding):

* **No `docs/related-practices.md`.** Cairn nowhere mentions Architecture
  Decision Records, the PEP/NEP/APE proposal traditions, lab notebooks, or
  registered reports. The dismissive compression — *"so it's decision records
  plus checklists plus an installer"* — has real answers (review happens
  before the code is written; across genuinely different models; the
  verification plan is locked in advance; the record lives in the repository,
  not a chat platform) and Cairn states none of them.
* **No `docs/glossary.md`**, against roughly forty coined house terms.
* **The internal codes are still in the front door.** `README.md:232`
  (`G/M/P`), `:244` (`R-A`, `R-I`, `R-H`), `:261` (`R-H … chunk 5.3 of the
  plan`). These resolve nowhere a first-time reader can follow.
* **No `CONTRIBUTING.md`** — but note this one is **already dispositioned**:
  `dev/PLANNING.md` records the Maintainer declining the `CONTRIBUTING.md`
  half of `contributor-entry` and keeping only the `SECURITY.md` disclosure
  channel plus its README pointer, as **[REL-6]**. This note does not reopen
  it and the feature work must not smuggle it back in.

### F4 — A feature list is a claim surface, and Cairn's own drift history is against it

This is the finding that most changes the shape of the work.

The 2026-06-12 friction audit's headline failure (F1 there) was that the
quickstart's *most checkable* numbers — module count, slot count, installed
file list — had drifted behind the scaffold, and a skeptic who runs the
command and sees a different number stops trusting the page. The broad-look
review then found the same failure repository-wide: published module lists,
the doctrine index, the placement guide, the changelog, the citation file.

**A README feature list is exactly that class of surface.** "Twenty
selectable modules," "zero runtime dependencies," "installs and upgrades in
place," "every shipped file integrity-checked" are all checkable in minutes,
and each one goes stale the moment the machinery moves. Shipping a
feature-forward README without pairing it to the drift-gate pattern would
reintroduce, on the highest-traffic page in the repository, the precise
failure Cairn's own lifecycle exists to prevent.

Two features in particular must be worded against what is *verified* rather
than what is *built*, because the broad-look left them open: the **upgrade
path** (never rehearsed across versions, by anyone, including Cairn on itself)
and the **cross-harness story** (the compatibility table lists supported AI
tools as claimed-but-unverified). A feature list may name these; it must not
oversell them.

### F5 — What carries over from the superseded graphics note, and what does not

**Carries over (methodology-general, and already half-practiced here):**

* **Mermaid-first, with a committed-SVG escape hatch.** Mermaid is diffable,
  version-controlled, zero-build, and renders natively on the host; fall back
  to SVG only where a diagram needs real spatial layout Mermaid cannot
  express. Cairn's README already demonstrates both halves.
* **No hardcoded fills.** A diagram with a baked `fill:#fff` goes unreadable
  when the host renders a dark theme. Rely on the default theme.
* **Two checks, not one — bytes *and* legibility.** Existence proves the
  bytes are there; it does not catch a diagram illegible in dark mode, a
  clipped SVG, a missing legend, or text unreadable on a phone.
* **The caption states the conclusion to draw.** Alt text and caption carry
  the point, so a screen-reader user or an images-off skimmer still gets it.
  A decoratively-captioned figure remains a review finding.
* **Asset naming, size, and provenance** — kebab-case descriptive names, a
  size pressure rather than a hard cap, and a recorded source per asset.

**Does not carry over:** the entire P0–P3 inventory. Grid-cell topology,
calibration parameter stacking, the PEST++ GLM loop, pathline plots, the
`CellPicker` screenshot — all of it is modflow_tools' hydrogeology
documentation. Cairn has no science outputs to embed, which changes what its
"generated figure" class even *is* (F6).

**One gate is already satisfied.** That note made the P0 embed conditional on
first shipping an image-existence check, because modflow_tools'
`verify_doc_links.py` silently tolerated any missing non-`.md` target.
**Cairn's `scripts/link_check.py` does not have that hole.** Perturbation-
tested this session: a deliberately broken `![…](…svg)` reference in a tracked
file produced `broken link target:` and exit code 1. Its own docstring names
images explicitly, and the target-resolution path checks `.exists()`
regardless of suffix. Gate (1) is closed before the work starts; gates (2)
legibility and (3) provenance are not.

### F6 — Cairn's "figure with a recipe" is a figure generated from Cairn's own registries

The superseded note's reproducibility discipline — *a figure is an artifact
with a recipe, not an opaque binary* — was built on a scientific plotting
module. Cairn has none. But it has something better suited to the drift
problem in F4: **machine-readable registries that the installer already
reads.**

The module roster, the dimension→module mapping, and the lifecycle transition
vocabulary are all already structured data inside the engine and its gates. A
diagram *generated from that same source* cannot drift the way a hand-drawn
one can — it is the drift-gate pattern expressed as a picture. This converts
the graphics note's reproducibility ethos into Cairn's own idiom, and it is
the one place where a small generator script earns its cost.

It also bounds itself honestly: only a few diagrams have a registry behind
them. The conceptual ones (Dual-Review independence, where-Cairn-sits) do not,
and hand-authoring those is correct.

### F7 — Two hard constraints the superseded note did not face

* **Zero runtime dependencies, stdlib-only.** Everything Cairn ships is
  standard-library-only and adopters take on zero runtime dependencies; dev
  tooling is `pytest` + `vermin` and nothing else. There is no matplotlib, no
  diagram build step, no docs generator, and no CI to run one. Any generator
  proposed under F6 must be stdlib-only and emit SVG text directly, or it does
  not ship. **Mermaid stays the default precisely because it costs nothing.**
* **The by-file license split.** Explanatory diagrams in `docs/assets/` are
  CC BY 4.0; the brand mark alone is CC BY-ND; a generator script would be
  MIT wherever it lives. The three families must not overlap, so every new
  asset lands on a declared side.

### F8 — The roadmap already has a home for this

`dev/PLANNING.md` carries **"0.4 launch-surface polish"** *(queued for 0.4,
not launch-blocking)* — "graphics/figures in the adopter-facing docs +
quickstart (lower the 'doctrine-heavy at first contact' friction)". This note
feeds that existing row. **No new roadmap row is needed**, and none should be
opened at a non-serialization point.

## The feature story — raw material, not final copy

What the front door could enumerate, drawn from what the corpus actually
claims. Each is stated here at the register a README would use; the
verification column is the honesty constraint from F4.

| Feature | The one-line version | Evidence status |
|---|---|---|
| Review **before** code | The change is argued and reviewed as a written proposal before implementation exists | Shipped; **extensively** dogfooded across the `dev/` tree — with recorded exceptions, which the incident trackers carry rather than hide |
| Structural independence | The External tier requires a *different agent type or a human*, and who reviewed what is **recorded and reviewable** rather than asserted | Shipped doctrine; measured cross-agent-type review rate exists. **Limit:** the record makes independence *inspectable*; it does not *authenticate* an agent's declared type or a human reviewer's identity |
| The record **is** the repository | Append-only, one commit per lifecycle transition; the whole arc replays from `git log` | Shipped |
| The verification plan is locked first | What would falsify the change is committed before the evidence is gathered (a registered-report shape) | Shipped in the proposal template |
| Vendor- and stack-neutral by construction | The coordination channel is Markdown in git — swap models or languages without changing the method | Shipped; neutrality is lint-gated |
| Fitted, not one-size | Six adaptation axes and three graduated adoption levels; keep only the apparatus your codebase earns | Shipped |
| It installs | A scaffold that writes the apparatus into your tree, with containment and integrity checks | Shipped and tested |
| It upgrades | Three-way module merge against a lockfile, so new doctrine folds in without losing local edits | **Built, never rehearsed cross-version** — word carefully |
| Its own claims are checked | Claim checker, link checker, neutrality and redundancy gates — Cairn runs them on itself | Shipped |
| Zero runtime dependencies | Everything you install is standard-library Python | Verified by the broad-look |
| Nothing phones home | No telemetry, no auto-upload, no egress path | Shipped |
| Improvements flow back | A fold-back channel by which a deployment improves the methodology upstream | Shipped |
| A comprehension floor | You cannot legitimately decide what you cannot follow — plain-language explanation is a reviewable property | Shipped doctrine |
| Works with one agent | The Internal tier degrades gracefully to a fresh session; the External floor lands when a second reviewer exists | Shipped |

**The vibe-coding contrast, stated once and honestly.** The useful framing is
not that unrecorded prompting is bad — it is fast, and the README should keep
saying Cairn is slower at first. It is that **an unrecorded loop cannot answer
three questions**: why is it this way, who checked it, and what would have
falsified it. Cairn's whole apparatus is the machinery for keeping those three
answers in the repository. That is one paragraph, and it belongs above the
feature list, not inside it.

## Options

1. **Do nothing; leave it queued for 0.4.** Defensible — the roadmap already
   marks this "not launch-blocking," and the security and lifecycle work in
   flight is higher-stakes. Cost: the front door stays a wall of text through
   the first third-party adoption, which is one-shot.
2. **README-only, prose-only.** Add the feature list, the two-sentence pitch,
   and the vibe-coding paragraph; strip the internal codes. No new assets, no
   new files. Cheapest real improvement; leaves the comprehension gap (F1) and
   the skeptic's question (F3) untouched.
3. **README + the two skeptic answers, still prose-only.** Option 2 plus
   `docs/related-practices.md` and `docs/glossary.md`. Closes the outstanding
   B3 items. Still no pictures.
4. **The full package: front door, skeptic answers, and a small visual
   system** — options 2 and 3 plus three to five diagrams placed where the
   comprehension cost is highest, under the carried-over production discipline
   and gated as below. Highest cost; the only option that addresses F1.

## Recommendation

**Option 4, sequenced, with the README first and the visuals gated.** The
sequencing matters more than the scope, because each stage is independently
shippable and the later ones are where the cost is.

1. **The front door.** Feature list, the two-sentence pitch at the top, the
   vibe-coding paragraph, internal codes stripped, `examples/scientific-minimal/`
   linked (the friction audit's F6 — the artifact built for the scientist is
   still not linked from the page the scientist reads). Prose only; no new
   files. **Paired with F4's constraint**: every checkable number in the
   feature list either carries no number at all, or is covered by a drift
   gate. Prefer the former — a feature list does not need counts.
2. **The two skeptic answers.** `docs/related-practices.md` and
   `docs/glossary.md`, linked from the README. Independently useful, and the
   related-practices page is the single highest-leverage defence against the
   dismissive compression. Both are descriptive-layer content, so both are
   **registered in `docs/DOCUMENTATION_PLAN.md`'s descriptive-layer
   inventory** as part of this stage — an unregistered page is exactly the
   drift the placement guide exists to prevent.
3. **The visual system, gated on two prerequisites** (gate 1, image existence,
   is already closed per F5):
   * **Gate 2 — a legibility pass exists and is named.** Cairn has no CI, so
     this is a documented manual step, described as such: preview the README
     and one representative page in the target renderer, in both light and
     dark theme and at phone width, and record that each figure is readable,
     scaled, captioned, and not layout-breaking. A check whose only trigger is
     a human remembering must say so.
   * **Gate 3 — the asset convention is written down first, in a named
     home.** Where assets live, how they are named, which license family each
     lands in, what provenance line each carries, and how gate 2 is
     discharged. **`docs/DOCUMENTATION_PLAN.md` owns this** — it is already
     Cairn's governing source for documentation architecture, and an asset
     convention is documentation placement. It does **not** go in this note,
     a new file, or a proposal body. *Scope fence:* this is Cairn's own
     self-hosted instance only. The shipped forkable
     (`documentation_plan_template.md`) is **not** touched by this work; the
     two portable fold-up candidates at the end of this note each need their
     own reviewed doctrine change to reach an adopter.
4. **The diagrams themselves**, in comprehension-cost order — the doctrine
   pages first, not the README, since the README is already the one file with
   pictures. Candidates: the lifecycle state machine promoted out of the
   README and into `doctrine/lifecycle.md` where it is defined; the
   dimensions→modules selection map; a "where Cairn sits in your workflow"
   figure for `docs/workflow-role.md`. Mermaid unless spatial layout forbids
   it. **Gated on the registry question below**: any diagram whose content is
   derived from an active implementation surface waits for that surface to
   settle.
5. **Only then, and only if two or more diagrams have a *settled* registry
   behind them,** consider the F6 generator. The registries that would feed it
   — the lifecycle transition vocabulary, the dimension→module mappings — are
   **active implementation surfaces today**, with lifecycle-vocabulary and
   module work in flight. A generator built against a moving input encodes the
   movement, which is worse than a hand-drawn diagram that is simply correct
   today. Prerequisites, all of which belong in that later proposal rather
   than here:
   * the source registry paths are **named and settled**, not in-flight;
   * generated output **records the source commit or digest** it was derived
     from, so a stale figure is detectable rather than merely wrong;
   * the generator is **deterministic** — same input, byte-identical output —
     so a regeneration is a no-op diff;
   * every registry-derived label is **XML-escaped**, since a module name or
     state token flows from a file into markup;
   * the emitted SVG carries **no scripts, no external resources, and no
     host-font dependency**, keeping it inert and renderer-portable;
   * writes are **atomic** (temp-then-replace), so an interrupted run cannot
     leave a half-written asset in the tree.

   These are all reachable with the standard library, which is what keeps the
   generator inside Cairn's dependency budget. They exist so a generated asset
   does not become a new injection or drift surface — the two ways a figure
   pipeline turns into a liability.

**Residual risk, stated not dissolved.** A visual pass on a methodology
repository can degrade into decoration, and decoration is a maintenance
liability with no offsetting value — every asset is a thing that can go stale,
break in a theme, or contradict the prose beside it. The discipline that
prevents this is the caption rule (the caption states the conclusion to draw)
plus the legibility gate; if either is dropped for speed, stage 4 should be
dropped instead.

## Open questions

Each is the Maintainer's call; the recommended answer is noted.

1. **Scope.** Option 4 as sequenced, or stop after stage 2 (prose only)?
   *Recommended: authorize stages 1–2 now as one proposal, and let stages 3–5
   open separately once the front door has landed.* The README rewrite does
   not need the visual system to be decided.
2. **How many features is the right number?** Fourteen rows is a table, not a
   scan. *Recommended: six to eight in the README, chosen for
   differentiation rather than completeness, with the rest reachable through
   the doctrine.*
3. **The two under-verified features** (upgrade, cross-harness). Name them
   with an honest qualifier, or omit them from the front page until the
   rehearsal and the test records exist? *Recommended: omit from the feature
   list; a front door is the wrong place to hedge.*
4. **Asset convention** — a single `docs/assets/` for everything, or split
   generated from hand-authored? *Recommended: keep the single `docs/assets/`
   until there is a generator to justify a split; the superseded note's
   two-directory recommendation was sized for a repository with a plotting
   module.*
5. **Does the lifecycle diagram move or duplicate?** Promoting it into
   `doctrine/lifecycle.md` and keeping it in the README means two drawings of
   one state machine. *Recommended: keep both, and be precise that this is
   **two representations, not one source** — calling it a single canonical
   source would be a comfortable fiction, since a simplification is by
   construction different bytes conveying a deliberately smaller claim.* The
   honest arrangement names three things: the **authoritative** drawing lives
   in `doctrine/lifecycle.md` and shows every named state and transition; the
   README's is a **faithful simplification**, defined as introducing no state
   or transition the authoritative one lacks and contradicting none of them
   (the caveat already under the README's diagram states exactly this); and
   the **drift check** is the relationship, not the bytes — a reviewer
   confirms the simplification's states remain a subset when either changes.
   Whether that check is a human step at the doctrine-change gate or a
   mechanical one is a question for the implementing proposal, not this note.

## Fold-up note

Most of this is Cairn-internal — Cairn's own front door and its own docs.
Two pieces are methodology-general and are **fold-up candidates**, each
needing its own proposal and each subject to the one-incident-is-not-doctrine
rate-limit gate:

* **"A feature list is a claim surface."** The observation in F4 — that
  enumerating capabilities on an entry page creates exactly the
  hand-maintained-description-of-a-moving-thing class that drift gates exist
  for — generalizes to any adopter's README. It is a candidate line for the
  `doc-drift-prevention` module's doctrine, not just for Cairn's own page.
* **The visual-documentation discipline** carried over in F5 (Mermaid-first,
  no hardcoded fills, existence *and* legibility as two distinct checks, the
  caption states the conclusion) is portable to any adopter and was already
  flagged as a fold-up candidate by the superseded note. It remains one; the
  new element is that the existence half is now demonstrably enforced by a
  shipped checker rather than proposed.
