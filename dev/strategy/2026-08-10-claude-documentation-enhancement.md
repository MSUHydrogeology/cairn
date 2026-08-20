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

> **Execution state, `as_of` 2026-08-20** *(added at a later pass; the
> Recommendation below is unchanged and still governs).* **Stages 1 and 2 have
> shipped — do not re-do them.** Stages 3–5 have not started.
>
> * **Stage 1 — the front door: done.** `f6ee989` (lead with what Cairn does,
>   unbacked claims dropped), `0629b44` (the review section rewritten in the
>   reader's register), `ab07789` (customization added).
> * **Stage 2 — the two skeptic answers: done.** `6df71b7` created
>   `docs/related-practices.md` and `docs/glossary.md` and registered both in
>   `docs/DOCUMENTATION_PLAN.md`'s descriptive-layer inventory, which was the
>   stage's own condition; `ab07789` gave both a plain-language pass.
> * **Stage 3 — the visual-system gates: done.** `docs/DOCUMENTATION_PLAN.md`
>   gained an **"Assets"** section carrying both gates: the asset convention
>   (home, naming, per-file license family, the four-part header block,
>   inertness rules, the caption rule) and the named legibility pass, written
>   as the human-triggered manual step it is, since Cairn has no CI. Gate 1 was
>   already closed at authoring time per F5. Written into Cairn's self-hosted
>   copy only, on the Maintainer's instruction; the forkable is untouched, and
>   the section names the legibility pass as the one portable part should that
>   be revisited.
>
>   Two things the writing turned up. The convention was **already being
>   followed** — both existing assets satisfy every file-level rule, so the
>   section mostly records practice rather than imposing it; the legibility
>   pass is the single new obligation. And **captions live in the Markdown
>   embed's alt text**, which the note had not specified: the Dual-Review
>   figure's alt text already states a conclusion and is the form to copy,
>   while the identity mark's describes the image, so the caption rule binds
>   explanatory diagrams only.
>
> * **Stage 4 — the first diagrams: partly done.** The five doctrine state
>   machines render, and `dimensions/README.md` gained the dimensions-to-modules
>   selection map (`c9ad978`). **Gate 2 was discharged**: the Maintainer ran the
>   legibility pass on 2026-08-20 against a proof sheet carrying all four
>   diagrams with theme and width toggles, and passed them. The lifecycle
>   state-machine promotion the note originally listed was **not** done and
>   should not be: `doctrine/` now carries correct rendered diagrams, and
>   `docs/workflow-role.md`'s hand-drawn ASCII figure was left alone — converting
>   a correct, theme-proof, zero-maintenance figure buys prettier, not clearer.
> * **Stage 5 — the F6 generator: not started.** Stage 3
>   no longer blocks them; stage 5 remains gated behind registries that are
>   still active implementation surfaces.
>
> **A stale exemption was removed from the top of this file at the same pass.**
> Its `claim-check-allow` block named six paths as deliberate
> forward-references. Two had since shipped, and — checked properly — **none of
> the six is cited anywhere in the body**, so the whole block suppressed
> nothing and was deleted rather than trimmed. Confirmed by positive control:
> a probe file citing `docs/definitely-not-here-xyz.md` flags, and a probe
> citing the block's own paths flags too, so the checker was capable of
> catching them and simply had nothing to catch. `claim_check` reports a file
> carrying a dead exemption as clean, so nothing detects this class; if those
> citations are ever written, the marker comes back with them.
>
> **One question stage 3 must answer first, which this note does not settle.**
> The Recommendation fences stage 3 to Cairn's self-hosted
> `docs/DOCUMENTATION_PLAN.md` and explicitly excludes the shipped forkable.
> That file's own "Updating this plan" section says the opposite by default:
> cross-propagation to the forkable is *bidirectional under maintainer review*,
> and substantive doctrine changes here *should* propagate. An asset convention
> is plausibly substantive. Whether the fence or the propagation clause governs
> is the Maintainer's call, and it decides whether stage 3 is one file or two.
>
> `dev/PLANNING.md`'s **"0.4 launch-surface polish"** row (F8) remains the
> roadmap home and is still correctly queued, since the graphics stages are
> what remain.

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

**And a drift gate is not automatically the answer — it has to execute the
thing it claims to check.** The 2026-08-11 adopter-friction rebuild found the
sharper version of this, with a live precedent: `docs/quickstart.md`'s
published `git add` command leaves `NOTICE.md` and `profile.yml` untracked,
while `bootstrap/tests/test_quickstart_sequence.py` reports 8 passing tests and
describes itself as driving the literal shell commands. It does not run the
documented staging or commit vector, and asserts nothing about the residual
state; its helper stages an older, smaller set. **The gate was green and the
defect recurred anyway** — and the green gate is *why* nobody noticed.

So the constraint on stage 1 is stronger than "cover the numbers." A gate over
a documentation claim must run the claimed command or read the claimed surface
and assert the result. A gate that tests adjacent output is coverage, not
evidence, and it is worse than no gate because it converts an unchecked claim
into an apparently-checked one. This is the same question Cairn already asks of
its security controls — *what trigger actually executes the claimed check?* —
turned on its own docs.

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

### F8 — The roadmap already has a home for this, and part of that row is not a graphics problem

`dev/PLANNING.md` carries **"0.4 launch-surface polish"** *(queued for 0.4,
not launch-blocking)* — "graphics/figures in the adopter-facing docs +
quickstart (lower the 'doctrine-heavy at first contact' friction)". This note
feeds that existing row. **No new roadmap row is needed**, and none should be
opened at a non-serialization point.

One scoping honesty note, from the adopter-friction rebuild: a large share of
the "doctrine-heavy at first contact" friction is **install output, not prose
or pictures**. The smallest profile prints 72 install rows and labels all 22
remaining slots as requiring attention — including contribution points for
modules the profile never selected — and an explicit empty-module install still
reports all 22. Diagrams will not touch that. The fix there is classifying
obligations by what the accepted profile makes live, which belongs to the
adopter-path work rather than here. **This note should not claim the graphics
stage will lower that friction**, or it will be measured against a problem it
cannot reach.

### F9 — Three findings elsewhere would make this work land twice

The adopter-friction rebuild (2026-08-11) and the executing
`review-efficient-lifecycle` plan each hold a contract this note's stages
would otherwise write against prematurely. None of these is this note's to
settle; all three are sequencing constraints on it.

* **The adoption-level model is under active revision, and the README is one of
  the surfaces teaching the unexecutable path.** The rebuild's headline is that
  Level 1 — the level Cairn recommends to its primary audience — has **no
  executable greenfield path**: the docs instruct hand-copying selected modules
  and no recipe supplies the source→destination mapping. Verified here:
  `README.md:206–217` carries the three-level ladder, and `:212` is literally
  *"Level 1 — hand-copy the kernel."* Its recommendation is one installer, with
  levels distinguished by obligation rather than by whether bytes were copied by
  hand — which rewrites exactly that section. **Stage 1 must not restate or
  harden the level model**; treat those lines as owned by the adopter-path
  proposal and leave them untouched.
* **The "try it in 15 minutes" claim is unbacked.** The rebuild found the
  timing promise has outlived its measured path — entry surfaces gained 222
  lines and lost 71 since v0.3.0, the installed `AGENTS.md` is 2,676 words, and
  no current canary records elapsed time. The recommendation is to reproduce
  the figure with a release-boundary canary or replace it with an unquantified
  "short walkthrough." By this note's own F4 the answer is forced: it is a
  checkable claim with no current measurement, so **the README rewrite must not
  re-assert the number** — drop it or defer to the canary.
* **The lifecycle state machine may be about to change.** The executing
  `review-efficient-lifecycle` plan conditionally changes the proposal/plan
  status vocabulary pending a Maintainer promotion Decision, and the rebuild
  records that the entry surface would need revising if it promotes. Stage 4
  proposes drawing that state machine into `doctrine/lifecycle.md`. **Drawing
  it before that Decision means drawing it twice** — and a stale diagram is
  worse than no diagram, because a picture reads as more authoritative than the
  prose beside it.

The practical consequence is small and worth stating plainly: **stages 1–2 stay
shippable now** provided stage 1 leaves the level model and the timing claim
alone, and **stage 4's lifecycle diagram waits** on the promotion Decision.
Nothing here blocks the front-door work; it bounds it.

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
   vibe-coding paragraph, internal codes stripped. Prose only; no new files.
   Four constraints, three of them from elsewhere (F4, F9):
   * **Numbers**: every checkable figure in the feature list either carries no
     number at all, or is covered by a gate that *executes the claim*. Prefer
     the former — a feature list does not need counts.
   * **Leave the level model alone.** It is being rewritten by the adopter-path
     consolidation proposal; restating it here lands the work twice.
   * **Do not re-assert "15 minutes."** Drop the figure or defer to the release
     canary, per this note's own F4 applied to itself.
   * **One trial, one next step.** The rebuild's first success criterion is that
     the README offers *one* obvious trial and *one* obvious real-adoption next
     step. Today it offers a quickstart, three levels, a bootstrap procedure,
     and a readiness report — four routes, which is the enticement problem in a
     different costume. A feature-forward rewrite that adds a fifth would make
     the page worse while looking better.

   The previously-cited "link `examples/scientific-minimal/`" item is
   **partly done, and the remainder is a placement question rather than a
   missing link.** Verified at `README.md:248`: the mass-balance example is
   linked — but only as a row in the repository-layout table, not anywhere in
   the "How to adopt" flow. A scientist deciding whether to invest reads the
   adoption path, not the directory inventory. Carry it forward as *where it
   should appear*, not *whether it exists*.
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

*Written plainly on purpose — these are the decisions the rest of the note
exists to serve, and a decision you cannot follow is not one you can make.*

**The situation in one paragraph.** Cairn's front page tells a good story but
never gives the reader a list of what Cairn actually does, and the rest of the
documentation has no pictures at all — of nearly three hundred files, exactly
one (the README) contains a diagram. I want to fix the front page with words
first, and separately decide whether the doctrine gets diagrams. The questions
below split along that line.

1. **How far do we go right now?**
   The work comes in two halves. The **words half** rewrites the front page's
   opening and adds two short explainer pages — one answering "how is this
   different from things I already know," one defining the house vocabulary.
   The **pictures half** adds three to five diagrams and possibly a small
   script that draws some of them from Cairn's own configuration files.
   *I recommend approving the words now and deciding pictures later.* The front
   page does not need the diagrams settled, and the words half is the part
   that pays off soonest.

2. **How many things should the front page list?**
   I drafted fourteen. That is a reference table, not something anyone scans.
   *I recommend six to eight*, chosen for what makes Cairn genuinely unusual
   rather than for completeness, with everything else reachable a click away.
   You are better placed than I am to say which six a skeptical colleague
   would actually care about.

3. **Two of those items we can't fully stand behind yet.**
   *Upgrading an existing installation across versions* is built but has never
   been rehearsed — not once, including by Cairn on itself. *Working with
   different AI tools* is claimed but not tested. We can list them with a
   caveat, or leave them off the front page until the evidence exists.
   *I recommend leaving them off.* A front page is the wrong place to hedge,
   and a caveat there invites exactly the scrutiny we cannot yet survive.

4. **Where should image files live?**
   One folder for everything, or separate folders for hand-drawn versus
   script-generated? *I recommend one folder* until a generator actually
   exists to justify splitting. This only matters if you approve the pictures
   half.

5. **The lifecycle diagram — should it wait, and should there be one or two?**
   *Waiting:* the proposal/plan status vocabulary may change pending your
   promotion decision on `review-efficient-lifecycle`. Drawing that diagram
   before you decide means drawing it twice, and a wrong diagram is worse than
   none — a picture reads as more authoritative than the paragraph next to it.
   *I recommend this one diagram waits*; the other candidates don't depend on
   that decision and can proceed.
   *One or two:* if it does proceed, the full version would live in the
   doctrine and the README would keep its simplified one. That is honestly
   **two drawings, not one source** — a simplification is by construction a
   different picture making a smaller claim. The workable arrangement is that
   the doctrine's version is authoritative, the README's may leave things out
   but must never contradict it (the caveat already under it says exactly
   this), and when either changes someone checks the relationship still holds.
   Whether that check is a person or a script is for the implementing proposal
   to decide, not this note.

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
