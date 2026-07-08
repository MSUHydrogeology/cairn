<!-- cairn-internal-ref-allow: doctrine/rationale.md doctrine/dual-review.md doctrine/proposals.md doctrine/lifecycle.md doctrine/runtime-contract.md doctrine/doc-governance.md doctrine/README.md reason=doctrine/ citation convention -- references resolve locally in Cairn's self-hosted tree -->

# Cairn v0.3 broad-look — a skeptical outsider's read (code, docs, concept, formulation)

**Author**: Claude (Strategy)
**Model**: Claude Fable 5
**Date**: 2026-07-08
**Status**: settled
**Type**: product-strategy
**Surfaces this would feed**: the tighten-up proposal series scoped in
the Recommendation below; the `dev/PLANNING.md` broad-look / 0.4-gate
items at the next serialization point; the R-H probe protocol.

## The question / felt gap

The Maintainer asked for a wide, skeptical-outsider read of the whole
project — what the repository contains, what it claims to be, what the
strategy corpus commits to, and how faithfully the tree implements all
three — across code, documentation, conceptualization, and formulation.
The context sharpens the question: the first external adopter (a
postdoc in the Maintainer's lab, likely with an existing research
codebase) is imminent, that adopter is in effect the R-H third-party
probe that gates the 0.4 public release, and the probe is one-shot.
So the operative question is not "is Cairn good?" but **"what would a
skeptical outsider find in an afternoon, and which of those findings
would cost us the first adopter or the launch?"**

This note implements the "Broad-look + roadmap pass" item queued on the
migrated roadmap. It deliberately goes *around* the surfaces already
covered: the 2026-06-12 adopter-friction audit (its F1–F9 all landed
via the archived `adopter-entry-doc-refresh` proposal) and the two
tracked gate issues (#1 AST-baseline drift, #2 neutrality-gate scope).

## Method *(grounded, falsifiable)*

* **A structured multi-agent audit** over the 2026-06-12 tree:
  seven surface mappers (public identity, strategy corpus, doctrine,
  engine code, shipped adopter artifacts, the self-host `dev/`
  instance, plus a live replay of Cairn's own gates), then seven
  skeptical reviewer personas (methodologist, fact-checker, program
  reviewer, RSE/security auditor, technical-writing lead, JOSS-style
  reviewer, and a simulated postdoc first adopter), then **adversarial
  verification of every finding** — high-severity findings faced a
  three-lens panel (evidence accuracy, materiality at this project
  stage, steelman-the-status-quo) — then a completeness critic that
  spawned four targeted follow-up reviews (downstream licensing, the
  daily-loop runtime code surface, cross-harness operability, the
  upgrade path). 147 agents in total. **89 findings raised; 87
  survived adversarial verification; 2 were refuted** and are excluded
  below. Already-tracked items (F1–F9, issues #1/#2) were auto-refuted
  as duplicates by construction.
* **Hand re-verification at today's HEAD.** The audit ran before the
  doc-refresh landed; every claim asserted in this note was re-checked
  against HEAD `d789414` on 2026-07-08 (citations spot-checked
  file-by-file; the gates re-run live). Findings that the doc-refresh
  fixed were dropped.
* **Live gate snapshot** (as of 2026-07-08, HEAD `d789414`, Python
  3.12): `python -m pytest bootstrap/tests` → **3 failed, 1403 passed,
  3 skipped** (the two tracked issue-#1 failures plus one *new*
  failure, T3.7 below); `scripts/check_cairn.py` → clean;
  `scripts/quality_gate.py` → neutrality **fail=99** (unchanged since
  the v0.3.0 cut), redundancy **fail=10**, order-independence fails by
  cascade from the suite. Newest tag is `v0.3.0`, now 20 commits behind
  HEAD.
* **Falsification:** every claim below carries a checkable citation or
  a replayable command; this note passes `scripts/claim_check.py`.

## What holds up under attack (read this first)

A skeptical review is only useful if it is calibrated, and much of
Cairn survived adversarial verification impressively:

* **The stdlib-only / zero-runtime-dependency claim is true** —
  verified by enumerating imports across every shipped Python surface.
* **The engine's untrusted-input core is genuinely strong**: every
  adopter-tree write routes through fail-closed symlink/containment
  guards, slot parsing fails closed on every malformation tried,
  verbatim scripts are hash-classified rather than text-merged, the
  lockfile verifier enforces the living-state boundary verifier-side,
  and there are zero bare excepts. The tests perform real installs with
  negative-path attacks. This is well above typical research-software
  hygiene, and the audit's security reviewer said so explicitly.
* **The install contract has factually held**: the engine diff from
  v0.3.0 to HEAD is four lines of print text.
* **Strategy-to-implementation traceability is strong where the
  lifecycle actually ran**: every recommendation of the 2026-06-05
  complexity-debt audit verifiably landed.
* **The honest-framing voice is real and consistent** (the
  slower-at-first admission, the R-H gap admission), `doctrine/rationale.md`
  is a genuine, DOI-anchored related-work document, and
  `docs/workflow-role.md` correctly preempts the most common misreads.
* **The self-host copies match their template sources**, and the two
  refuted findings both died because the repo had already handled the
  concern — evidence the record sometimes defends itself.

The pattern in what follows is therefore *not* "the apparatus is
hollow." It is: **the deep machinery is better than the claims layer
that describes it, and the record layer that showcases it.** For a
methodology whose product *is* the record and the claims discipline,
that inversion is the strategic finding.

## Findings — seven themes

### T1. Record integrity: verifiable cracks exactly where a skeptic will look first

The flagship promise is a trustworthy deliberation record. The audit
replayed the record and found the flagship instances broken:

1. **The self-host showcase arc's commit history narrates transitions
   its diffs refute.** The proposal-open commit `17b7e5c` ("open
   check_cairn self-host-compat (+ Internal review)") already contained
   the *full* arc — both the Internal review and the Gemini External
   review sections — while the Status line still read `proposed`; the
   next commit `f4a8308`, whose message says it appends the Gemini
   External review, actually adds no review content (its whole diff is
   a 2-line claim-check-allow edit). Re-verified by hand at HEAD. To an
   outside auditor this is indistinguishable from a fabricated review
   trail; the likely truth (the deliberation happened, then was
   serialized in a sweep) is undisclosed. This falsifies "one commit
   per lifecycle transition" in the first worked example a newcomer
   would study.
2. **The v0.3.0 cut commit carries a gate-green attestation that fails
   replay.** Commit `12ec2ad` asserts "quality_gate exit 0 (neutrality
   all-info/justified; 6 advisory R6 redundancy notes)". Replaying the
   identical gate code on the committed cut tree yields neutrality
   **exit 1, fail=99** and redundancy **exit 1, fail=6** — independently
   reproduced three times by the verification panel and once by hand
   this session. The release record asserts a verification that did not
   happen as described.
3. **The standing pre-release sweep did not run at v0.3.0.** The sweep
   doc (`dev/strategy/2026-05-27-claude-cairn-pre-release-sweep.md`)
   declares itself "a standing Cairn practice" gating every version
   increment; its status tables carry only v0.2.0 rows, and the drift
   class Sweep A exists to catch (F1–F9) shipped in 0.3.0 and was found
   only post-cut.
4. **The adoption record points at deliberation that does not exist.**
   `dev/.cairn/profile.yml` and `dev/PLANNING.md` both say the
   preset-selection deliberation "lives in dev/strategy/"; no strategy
   note records it (grep for the preset name across `dev/strategy/`
   comes back empty).
5. **Both declared review floors bent within hours of self-hosting,
   without recorded waivers** — a same-session "Internal" review below
   the fresh-session floor, and a "ratified at Decision" plan-review
   requirement that the Decision never addressed — and no apparatus
   noticed (no incident-tracker entry).
6. **The gating function of review has never visibly fired.** The only
   measured corpus (the v1 metrics baseline) shows 51 proposals, 0
   rejected, 0 superseded, median days-to-decision 0. The *improvement*
   function is well evidenced (mean 7.7 findings per review); the
   *adversarial* function — the differentiator — is, on the record so
   far, indistinguishable from an accept-ceremony. The candidate
   explanation (chat-stage shaping filters losers before a proposal
   opens) is half-acknowledged in `doctrine/lifecycle.md` but never
   stated where a reader of the metrics will need it.

None of these is expensive to fix, and none was found dishonest in
intent — but every one is checkable in minutes by exactly the skeptical
outsider Cairn courts, and each hits the differentiator, not the
periphery.

### T2. The map lags the territory in a dozen checkable places

Cairn's pitch is that recorded discipline keeps the map matching the
territory. Verified counter-examples currently in the tree, beyond the
already-fixed F1–F9 class:

* **Module rosters:** the engine resolves 6 default-on + 14 team-gated
  modules; `templates/modules/README.md` tables 12 of the 20;
  `dimensions/README.md` lists 3 default-on; the two case studies give
  mutually contradictory team-gated counts; `bootstrap/BOOTSTRAP.md`'s
  Appendix B example still hand-lists 3 of the 6 default-on modules
  (re-verified today) — and the engine installs a literal `modules:`
  list silently, so the fallback path for the no-preset-fits adopter
  quietly drops half the default disciplines.
* **The doctrine index:** `doctrine/README.md` maps 8 of the
  directory's 16 files (~19k of ~38k words unmapped, including the
  proposals/plans contracts a first adopter most needs) while asserting
  the core "is small by design."
* **The documentation-routing authority:** `docs/DOCUMENTATION_PLAN.md`
  — the self-hosted showcase of the documentation-plan module — still
  says in five places that Cairn "does not yet self-host its own dev/
  tree" (re-verified today at lines 26–27, 101–105, 148–149, 177),
  places BOOTSTRAP/PROVENANCE/SAFETY at the repo root when all three
  live under `bootstrap/`, and routes only 6 of the 9 `docs/` content
  pages. Its house `cairn/` path prefix also structurally exempts every
  path claim it makes from `scripts/claim_check.py`.
* **Release identity:** `CHANGELOG.md` line 2044 declares a 0.1.0
  "Initial public release" that never happened (the repo has never been
  public); `README.md` says v0.3.0 is "released" with no privacy
  qualifier — both contradict the release ladder in `dev/PLANNING.md`.
* **Citation metadata:** `CITATION.cff:3` titles the work "An Adaptable
  Framework…" with `type: software` against the README's "a
  methodology, not software," and its license list omits the CC-BY-ND
  brand-mark family the README declares load-bearing.
* **Security scope:** `SECURITY.md` promises a SHA-256 check of "every
  file in your tree"; `bootstrap/verify_integrity.py` checks only
  lockfile-recorded files, and Cairn's own install has scaffold-written
  onboarding docs with no lockfile records at all.
* **The evidence layer:** `case-studies/lhm.md` asserts, uncited, that
  "the multi-agent-systems literature cites handoff / coordination
  breakdowns as 35–57% of failures" — the exact statistic the guide
  star privately flags as needing primary-source verification "for the
  publishable artifact." `doctrine/rationale.md` claims every doctrine
  practice traces to a reason there, yet six doctrine files (~1.5k
  lines) are never referenced, and it misstates Cairn's always-loaded
  files (no RULES.md exists in this tree).
* **Vendor neutrality:** `templates/README.md:95-96` claims every
  template is vendor-neutral, while shipped, adopter-installed files
  carry vendor-named provenance notes, and the tracked issue #2
  mischaracterizes the gate's live distribution (only ~17 of the 99
  failures are under `templates/skills/`; the rest hit shipped modules,
  `docs/`, and `doctrine/` — so a triage built on the issue as written
  would declare the 0.4 gate satisfied while the headline invariant
  still fails).

The root cause is the same one the friction audit found for the
quickstart: these surfaces are hand-maintained mirrors of a moving
source with no drift gate. The just-landed quickstart drift-gate is the
right pattern; it currently guards two numbers on one page.

### T3. Security narrative vs security fact

The implemented core is strong (see "What holds up"); the *narrative*
around it is ahead of the facts in ways a security-literate adopter
will catch:

1. **The Bandit gate that three docs lean on runs nowhere.** `AGENTS.md`
   describes the engine as "guarded by … a Bandit gate"; the dev-suite
   tests skip when bandit is absent (it is not installed here) with
   "fails (not skips) in CI" docstrings — and the repository has no CI
   workflow at all (nothing under `.github/` but templates and labels).
   The fail-closed release gate (`bootstrap/security_check.py`) is
   real but manual.
2. **The release security gate never scans the highest-frequency
   shipped surface.** `scan_targets()` in `bootstrap/security_check.py`
   derives its Bandit surface from two registries but never consults
   the skills registry, so `templates/skills/_lib/lifecycle.py`
   (~1.3k lines — the code that *writes* in the adopter's repo at every
   session start) and `templates/skills/_lib/lifecycle_planner.py`
   (~1.1k lines) ship outside the gate, while `SECURITY.md` says the
   gate covers "the shipped Python surface." The skills security suite
   has the same stale-hand-list problem: its artifact lists predate the
   planner entirely.
3. **The one fail-open input.** The profile — the primary untrusted
   input — is parsed by a stdlib YAML fallback that diverges from
   PyYAML *inside the documented flat schema* (trailing comments on
   scalars are kept as data, including for the example printed by
   `--help`; quoted list items are comment-split), and unknown or
   typo'd top-level keys are silently ignored: a misspelled `preset:`
   silently yields the default-on install. Everything else in the
   engine is fail-closed; this is the exception, on the input a postdoc
   is most likely to get slightly wrong.
4. **The redundancy gate red-flags its own security code.** The R6 pass
   does not count `from X import name` aliases as references, so 10 of
   its 10 current FAILs include the engine's import-boundary installer
   (`bootstrap/_scaffold/_guard.py`) and a test-pinned renderer — with
   remediation text advising deletion. A gate that is red with false
   positives trains everyone to ignore it.
5. **One guard-order inversion**: `write_install_lockfile` creates the
   lockfile's parent directory *before* its containment guard — the
   single write site that inverts the engine's otherwise-uniform
   guard-then-mkdir order.
6. **A false "read-only" promise in the daily loop**: `tools/lifecycle.py
   --help` says every side-effecting subcommand honors `--dry-run` and
   calls session-start "read-only orientation," yet session-start
   performs the self-heal writes (symlink creation, `.gitignore`
   append, quarantine-moves) and has no `--dry-run`.
7. **New this session — the suite now goes red by pure passage of
   time.** `bootstrap/tests/test_evolution_infer.py` (the `main()`-path
   test) hardcodes June 2026 incident dates against a 14-day rolling
   window read from the real clock
   (`templates/modules/default-on/evolution_infer.py:281` pins
   `datetime.date.today()` with no injection point). It passed during
   the June audit and fails today with zero code changes. A
   self-reddening suite corrodes the "run the suite after any
   substantive change" discipline — a red baseline normalizes ignoring
   failures. (A fix task was spun off this session: add a `--today`
   override.)

### T4. Licensing: adopters end up non-compliant by default

The completeness critic found the one surface where Cairn's provenance
discipline is simply absent — and it should gate the public release:

* `LICENSE-MIT.md` requires the copyright + permission notice in "all
  copies or substantial portions," and explicitly scopes the shipped
  tools under `templates/` — yet **no shipped `.py` carries any license
  or copyright header** (grep across `templates/` finds zero legal
  notices), and the scaffold writes no notice file.
* The installed prose tree is an adaptation of CC-BY-licensed works;
  CC BY 4.0 obliges the adopter to retain attribution, a license
  notice, a URI, and a modification indication the moment their repo
  goes public. **Nothing installed satisfies this and no adopter-facing
  doc mentions the topic** (grep across `bootstrap/BOOTSTRAP.md`,
  `bootstrap/UPGRADE.md`, `docs/quickstart.md`, `on-ramp/README.md`:
  nothing).
* The scaffold also caches raw, pre-substitution Cairn templates into
  the adopter's *tracked* tree (the lockfile base cache under
  `dev/.cairn/`) — verbatim CC-BY redistribution, deliberately hidden,
  notice-free.
* The lockfile — the only record tying installed files to Cairn — names
  no creator, license, or URL, and both provenance fields can degrade
  to `"unknown"` (Cairn's own `dev/.cairn/cairn-lock.yml` already
  records `cairn_commit: "unknown"`).
* There is no stated position on how the installed MIT/CC-BY material
  interacts with the adopter's own repository license (research code is
  routinely GPL-2.0 or custom-academic), and no inbound-license
  statement for the case-study contributions the repo invites.

The postdoc's hydrogeology repo, made public for a paper, would
redistribute MIT code with its notice stripped and CC-BY prose with no
attribution. For an Open Science methodology, this is a
credibility-level exposure — and the fix is small: one installed
notice file carrying both license blocks (tracked in the lockfile),
two-line SPDX headers on shipped `.py` files (verbatim copy makes them
self-propagating), one "licensing of the installed files" paragraph in
`bootstrap/BOOTSTRAP.md`, an inbound=outbound sentence for
contributions, and a Maintainer decision on the cleanest option: an
explicit downstream permission in `LICENSE-CC-BY.md` that collapses the
adopter's entire obligation to retaining the notice file.

### T5. The postdoc's actual path is unbuilt where it matters

The friction audit fixed the greenfield demo path. The path the *named
first adopter* will walk — solo scientist, existing messy codebase,
second harness for External review, PI watching — has verified gaps at
each step:

1. **No preset fits them, and the workaround silently under-installs.**
   The three presets and the on-ramp level table all disagree about the
   solo-legacy persona; axis overrides do not re-derive age-gated
   module rows, so overriding `age: legacy` onto a solo preset skips
   the legacy-retrofit modules Cairn's own age doctrine prescribes; the
   documented fallback (a hand-derived `modules:` list, Appendix B)
   starts from the stale 3-of-6 example and installs literal lists
   silently.
2. **The shipped solo onboarding mislabels the review record from day
   one.** `templates/onboarding/solo-greenfield.md:76` (and again at
   :115) teaches that fresh-session same-vendor review "fills the
   External tier" — directly contradicting `doctrine/dual-review.md`'s
   floors. The first adopter's committed record would assert a
   structural independence the doctrine says it cannot have; any later
   cross-type reviewer (or the PI) finds a corrupted provenance trail.
   Three independent verifiers confirmed this verbatim.
3. **The triage list omits the science trigger.** The canonical
   trivial-vs-non-trivial triggers (`doctrine/proposals.md` and the
   template's inlined copy) list API contracts, abstractions, file
   moves — never a scientific-assumption, sign/unit-convention, or
   default-parameter change, which the readiness report calls "the
   question Cairn is most differentiated on." The apparatus
   acknowledges the class elsewhere (a triage-extras slot; the
   high-stakes classification in the template body) but nothing wires
   it in, so the postdoc's most likely first real change — tweaking a
   calibration constant — triages to "just commit."
4. **The sanctioned escape hatch is not installed.** The
   deadline-pressure rule ("urgent, reversible, or experimental may
   proceed without a proposal, but say why") lives only in
   `doctrine/proposals.md`; the installed template carries a pointer to
   a directory adopters do not have locally. The designed pressure
   valve will read, in their tree, as unrecorded rule-breaking.
5. **Week-one value is real but unrouted.** The corpus's one genuinely
   early, science-shaped payoff — "your first substantive proposal
   should be a docs/assumptions.md capturing load-bearing scientific
   choices" — exists only as a conditional bullet in the readiness
   report's appendix. The entry surfaces repeat the honest "slower at
   first" framing without ever naming a concrete first payoff.
6. **Nobody has told the postdoc what happens under observation.** The
   readiness report and metrics carry "not a scorecard" postures; the
   deliberation record itself — rejected designs, incident logs, review
   findings, fully readable by the PI/maintainer — carries no
   equivalent statement anywhere. The rational response is a sanitized
   record, which destroys exactly the value the record exists to hold.
7. **There is no exit.** `docs/vision.md` promises "adoption is
   reversible"; no adopter-facing doc says how to move down a level, go
   dormant, or uninstall (the lockfile records every installed
   destination, so a documented removal path is cheap). Undocumented
   exit raises entry cost.
8. **The cross-harness layer the External tier depends on has zero
   verified targets.** `docs/skills-compatibility.md` records every
   harness at "native-claimed-unverified"; the one empirical
   confirmation (Antigravity, 2026-06-02) was never serialized as the
   fixture transcript its own promotion protocol demands; the
   second-agent onboarding walk never wires the reviewer harness's
   instruction file (nothing ensures the External reviewer ever loads
   `AGENTS.md`); and `templates/core/VENDOR.md`'s own
   `.github/copilot-instructions.md` rename example is unfollowable by
   the root-only rename resolver in `bootstrap/_scaffold/upgrade.py`.
9. **The one-shot probe has no protocol, and nothing rehearses the path
   before spending it.** The R-H item is "blocked on enrolling a third
   party" with no in-tree protocol, consent artifact, or success
   criteria (its plan citation points into the private modflow_tools
   tree), and every queued validation item is greenfield-scoped —
   nothing exercises a bootstrap into a populated repository.
   Meanwhile `SECURITY.md:25` tells adopters to scaffold from a
   released tag, and the newest tag (`v0.3.0`) predates all twenty
   commits of entry-doc fixes.

### T6. Positioning: the differentiators outrun their evidence

* **The prior art a skeptic actually knows is never engaged.** Grep
  across `README.md`, `doctrine/`, `docs/`, and `on-ramp/` finds zero
  mention of Architecture Decision Records, RFC/PEP processes,
  design-doc review, or lab-notebook/preregistration practice — while
  `docs/vision.md` claims both differentiators are "genuinely
  uncommon." The one compression most likely to kill adoption ("this is
  ADRs plus checklists plus a scaffolder") is the one the repo never
  answers, even though real answers exist (pre-code adversarial review
  across model independence; registered-report-style locked
  verification plans; repo-held rather than platform-held deliberation).
* **The independence premise is asserted at a confidence the
  measurement doctrine forbids.** `doctrine/dual-review.md` states as
  fact that a different architecture "does not silently inherit the
  author's" failure modes and quotes a cross-type catch-rate with no
  citation or denominator; the correlated-failure caveat the README
  already carries never made it into the doctrine or the shipped
  templates. An ML-literate reviewer will find the sharpest claim
  stated most weakly.
* **The identity contradiction is structural, not cosmetic.**
  "A methodology, not software" (`README.md`) coexists with
  `doctrine/runtime-contract.md:122` declaring the scaffold/lockfile
  tooling "the minimum mechanized kernel — the floor for a Cairn
  adoption" and methodology-only operation an *unsupported
  configuration* — while `on-ramp/README.md:33` calls exactly that
  configuration "the natural home for solo + one-agent adopters." One
  of these three surfaces must yield.
* **The language is a measurable adoption tax.** ~40 coined or
  house-heavy terms with no glossary; unexpanded internal codes on the
  front door (R-A/R-I/R-H, "chunk 5.3", G/M/P); no portable
  two-sentence pitch anywhere a postdoc could repeat to a PI; a
  `CITATION.cff` abstract in house dialect. And there is no
  CONTRIBUTING or support path in a repo whose identity claim is "Open
  Science repository" — a standard JOSS-review check.

### T7. Strategy-corpus and self-host hygiene

The corpus this audit was asked to treat as the statement of intent has
its own drift: the migrated metrics doc still carries an unfolded
2026-05-28 review (against the folder's own inline-revise rule) and
defers to a PLANNING "Goal 7" section that no longer exists; the
living guide star still says "Cairn is at v0.2.0"; the
collaboration-agreement retirement decision coexists with a live
day-one seed task telling agents to invest in the agreement (and
`AGENTS.md` still lists it as core reading); `doctrine/plans.md` cites
section anchors in `dev/agent_collaboration.md` that do not exist;
the charter has three conflicting canonical homes and `docs/vision.md`
has no inbound navigation link; ~900 words of lifecycle doctrine are
duplicated across `doctrine/proposals.md` and `doctrine/plans.md`
against the one-canonical-home rule; and the upgrade path — the
contract adopters will live on — has never been rehearsed across a real
version boundary (the lockfile `schema` field is written but never
validated on read, and Cairn's own init-lock-degraded install cannot
rehearse the 3-way merge it sells).

## Options

1. **Do nothing; proceed to the postdoc now.** Rejected. The probe is
   one-shot, and the current path teaches the adopter to mislabel their
   review record (T5.2), leaves their public repo license-noncompliant
   by default (T4), and hands a skeptical reader the record-integrity
   refutations (T1) in the first hour.
2. **Entry-surface polish only** — extend the doc-refresh pattern over
   T2's stale surfaces and stop. Cheap and visible, but it fixes the
   *description* while leaving the record repairs, the licensing
   exposure, and the adopter path itself.
3. **The full tighten-up, sequenced by the adopter timeline**
   (recommended, below): record repairs and the postdoc path before the
   install; accuracy-with-drift-gates and security-narrative alignment
   before the 0.4 cut; positioning and corpus hygiene rolling.
4. **Re-rank the existing 0.4 polish list.** The queued
   graphics/comment-cleanup items are worth less than any single theme
   above; they should sort behind Phases A and B.

## Recommendation — the tighten-up package

Sequenced into three phases keyed to the two real deadlines (the
postdoc install; the 0.4 cut). Each lettered item is proposal-sized;
items marked *(doctrine)* touch doctrine and must clear the
rate-limit gate on their own evidence.

**Phase A — before the postdoc installs** *(days of work, highest stakes)*

* **A1. Record-integrity repairs** (T1): append a dated provenance
  correction to the archived check_cairn arc (what actually happened,
  why `f4a8308`'s message is wrong); land a correcting record restating
  v0.3.0's true gate state; write the missing adoption-record strategy
  note or repoint the two "lives in dev/strategy/" claims; file the two
  bent-floor incidents in the incident tracker; state the
  0-rejections fact and its chat-stage-filtering explanation where the
  metrics are presented.
* **A2. Fix the review-record corruption vector** (T5.2): reword the
  three External-tier passages in `templates/onboarding/solo-greenfield.md`
  to the doctrine floors, and add a test asserting onboarding presets
  never pair "External" with fresh-session review.
* **A3. The solo-legacy recipe** (T5.1, T5.3–T5.5): a fourth preset or
  a documented compose route reaching the legacy modules (plus the
  Appendix-B example fixed to 6 default-on modules and an info line
  when a literal list omits default-ons); the science trigger added to
  the canonical triage list *(doctrine)*; the escape hatch inlined in
  the installed template; the assumptions-doc named as the standing
  first-proposal recipe for legacy adopters.
* **A4. The licensing package** (T4): installed notice file + SPDX
  headers + one BOOTSTRAP.md licensing paragraph + inbound=outbound
  sentence; Maintainer decision on the downstream-permission clause.
* **A5. Probe readiness** (T5.8–T5.9): rehearse the existing-codebase
  adoption internally on a populated repo before spending the real
  probe; record the two harness fixture transcripts (this harness + the
  reviewer harness) and flip those matrix rows; add "Step 0 — wire the
  reviewer harness's instruction file, then run a loaded-doctrine smoke
  check" to the second-agent onboarding; write the R-H protocol item
  (candidate, access, consent, pass/fail) in-tree; tag a v0.3.1 so
  tag-guided installs include the entry-doc fixes.
* **A6. The observation and exit notes** (T5.6–T5.7): a short
  "adopting within a lab hierarchy" statement (the record serves
  system learning, never performance evaluation) and a lockfile-driven
  de-adoption/dormancy section in the on-ramp.

**Phase B — before the 0.4 cut**

* **B1. One accuracy pass, drift-gated** (T2): fix the dozen
  map-vs-territory items and extend the quickstart drift-gate pattern
  to the surfaces that will drift again (module-roster tables generated
  from the engine registry; a doctrine-index completeness check in
  `scripts/check_cairn.py`; `docs/DOCUMENTATION_PLAN.md` refreshed and
  made claim-checkable). Re-scope issue #2 to the measured
  distribution and run the full neutrality disposition pass.
* **B2. Security-narrative alignment** (T3): derive `scan_targets()`
  and the skills-suite artifact lists from the registries; stand up
  minimal CI (suite + bandit + gates) or reword every fails-in-CI claim
  to release-manual-only; make the YAML fallback comment-handling
  PyYAML-parity and warn on unknown profile keys; swap the one
  guard/mkdir inversion; count ImportFrom aliases in R6; fix the
  lifecycle `--help` read-only claim; require a machine-generated,
  replayable gate transcript in the 0.4 cut commit.
* **B3. Positioning pass** (T6): a related-practice subsection in
  `doctrine/rationale.md` (ADR/RFC/design-doc/lab-notebook, one delta
  each) and scope `docs/vision.md`'s "genuinely uncommon" to it; the
  correlated-failure limit stated in `doctrine/dual-review.md`
  *(doctrine)* and the catch-rate claim cited or downgraded; the
  two-sentence PI pitch at the top of README and the CITATION.cff
  abstract; retitle CITATION.cff to the methodology identity and add
  the ND license; a glossary; strip the internal codes from the front
  door; a one-page CONTRIBUTING; reconcile the runtime-contract /
  on-ramp identity contradiction *(doctrine)*.

**Phase C — rolling hygiene** (T7): fold the metrics doc's review in
and re-home Goal 7; guide-star vantage pass; serialize the
collaboration-agreement retirement (annotate the seed task, open the
retirement proposal) before the postdoc inherits the agreement; repoint
the dangling doctrine anchors; single-home the duplicated lifecycle
doctrine; link `docs/vision.md` from the README; one worktree-based
v0.3.0→HEAD upgrade rehearsal plus lockfile-schema validation on read;
fix the clock-dependent test (spun off already).

## Open questions

1. **Licensing posture** (A4): explicit downstream permission keyed to
   retaining the notice file (collapses adopter obligations to one
   file — recommended), or plain CC-BY attribution mechanics?
2. **Solo-legacy** (A3): a fourth preset, or axis overrides that
   re-derive gated module rows? (Preset is simpler to explain; the
   override fix is more general.)
3. **CI** (B2): adopt a minimal workflow before 0.4, or re-word the
   fails-in-CI postures everywhere? (Recommend the workflow: it is the
   cheap, actually-load-bearing control, and it makes the attestation
   discipline in A1/B2 mechanical.)
4. **Identity reconciliation** (B3): scope the mechanized-kernel floor
   to bootstrap-installed adoptions and declare Level 0/1 supported
   methodology-only tiers, or stop calling Level 1 the natural solo
   home? The README identity should follow whichever wins.
5. **The construction record**: publish a lasting-truth digest of the
   private construction plan into `dev/plans/archive/`, or re-point the
   in-tree citations with an explicit privacy note?
6. **Probe identity**: is the postdoc formally the R-H probe (with the
   protocol and consent that implies), or a friendly pre-probe whose
   run does not consume the gate?

## Fold-up note

Four methodology-general candidates surfaced (each would be its own
proposal; the doctrine rate-limit applies):

* **Release attestations must be replayable.** A commit body asserting
  gate results is a claim surface; the discipline that would have
  prevented T1.2 is "paste the machine-generated transcript, never a
  summary."
* **Gate scopes derive from registries.** Every T3 coverage gap
  (Bandit surface, skills suite, R6 roots) is a hand-list that lagged
  its registry; the pattern "the owning registry is the single source
  for any scanner's target list" is general.
* **Wall-clock-anchored tests are a named hazard class.** T3.7's
  self-reddening suite is a reproducibility failure mode scientists
  already know from data pipelines; test-time must be injectable.
* **Transition lint.** A cheap mechanical check that a commit whose
  message claims a lifecycle transition actually contains that
  transition (and that an open commit contains no review sections)
  would have caught T1.1 at commit time.

---

## Appendix — verified finding inventory (87 confirmed, 2 refuted)

One line per confirmed finding, grouped by audit dimension; severity in
brackets. Full evidence, impact, and per-finding verification notes
remain in the session record; every item above cites its own evidence.

**Concept (10):** [H] showcase-arc provenance misstated (T1.1) · [H]
runtime-contract vs on-ramp identity conflict (T6) · [H] ADR/RFC prior
art unharvested, "genuinely uncommon" unscoped (T6) · [H]
correlated-failure limit absent from doctrine; uncited catch-rate (T6)
· [M] review floors bent without waivers (T1.5) · [M] rationale
traceability overbroad; RULES.md misstated (T2) · [M] case study ships
internally-flagged statistic (T2) · [M] External gate never fired on
the record (T1.6) · [M] CI absence untracked while trust apparatus
grows (T3.1) · [M] second-agent-type graduation step unnamed (T6).

**Claims (12):** [H] module rosters 12/20 with contradictory counts
(T2) · [H] vendor-neutrality contradicted in shipped files (T2) · [M]
SECURITY.md "every file" overpromise (T2) · [M] CHANGELOG false public
release; README unqualified "released" (T2) · [M] doctrine index 8/16
(T2) · [M] DOCUMENTATION_PLAN misdescribes its tree (T2) · [M]
CITATION.cff identity/license mismatch (T2) · [M] LHM statistic
provenance upgraded without citation (T2) · [M] usage claim carries no
verifiability statement (T6) · [L] rationale Anchor-12 RULES.md error
(T2) · [L] README trust block over-absolute vs link_check external
probe (T2) · [L] adoption deliberation pointer resolves to nothing
(T1.4).

**Alignment (11):** [H] v0.3.0 gate-green attestation fails replay
(T1.2) · [H] pre-release sweep skipped at v0.3.0, unhomed for 0.4
(T1.3) · [H] R-H probe has no enrollment path (T5.9) · [M]
collaboration-agreement decision unserialized vs live seed task (T7) ·
[M] no existing-codebase rehearsal queued before the probe (T5.9) · [M]
metrics doc supersession pointers dangle (Goal 7 ghost) (T7) · [M]
metrics doc carries unfolded stale review (T7) · [M] guide-star release
facts stale; Sweep B baseline missing (T7) · [M] construction record
not publicly auditable; citations point out-of-tree (T6) · [M]
neutrality-gate triage basis misdescribes live distribution (T2) · [L]
plan-open board row-move skipped (T1.7-adjacent).

**Code (8):** [H] Bandit/CI postures presuppose CI that does not exist
(T3.1) · [M] YAML fallback diverges from PyYAML on documented schema
(T3.3) · [M] R6 false-flags live security code (T3.4) · [M] upgrade.py
mega-functions outside the debt ledger (T7) · [L] sibling entry points
skip scaffold.py's hardened load path (T3) · [L] lockfile-write
guard-order inversion (T3.5) · [L] profile keys fail open (T3.3) · [L]
MergeResult status contract omits needs-value (T3).

**Docs (10):** [H] DOCUMENTATION_PLAN five stale self-host denials
(T2) · [H] doctrine map omits half the corpus incl. proposals/plans
contracts (T2) · [M] DOCUMENTATION_PLAN root-file placements wrong;
cairn/ prefix evades claim_check (T2) · [M] ~900-word doctrine
duplication proposals/plans (T7) · [M] plans.md cites nonexistent
anchors (T7) · [M] charter has three homes; vision.md orphaned (T7) ·
[M] descriptive-layer inventory 6/9 (T2) · [M] AGENTS.md git-section
accretion vs doc-governance (T7) · [L] doc-governance "forthcoming"
mechanism already shipped (T7) · [L] dev/README tree table omits two
installed dirs (T7).

**Formulation (8):** [H] skeptic compression unpreempted; comparables
unharvested (T6) · [H→M] ~40-term vocabulary, no glossary (T6) · [M]
README internal codes unexplained (T6) · [M] installed AGENTS.md
multi-agent-voiced for solo installs (T5) · [M] proposal template
preamble-before-skeleton ordering (T5) · [M] no two-sentence
mechanism+benefit pitch (T6) · [M] CITATION.cff Framework title, ND
omitted (T2/T6) · [M] no CONTRIBUTING/support path (T6).

**Postdoc (10):** [H] solo-legacy preset gap; silent age-gate skip
(T5.1) · [H] solo onboarding mislabels External tier (T5.2) · [H]
science trigger missing from canonical triage (T5.3) · [M] escape
hatch off-tree (T5.4) · [M] intent-claim referent uninstalled in solo
trees (T5) · [M] de-adoption undocumented vs "reversible" promise
(T5.7) · [M] adopting-under-observation unaddressed (T5.6) · [M] no
named week-one value moment (T5.5) · [M] Appendix B example 3/6 +
silent literal lists (T5.1) · [L] getting-started review step omits
solo floor (T5).

**Licensing gap (6):** [H] MIT notice stripped from installed copies ·
[H] no CC-BY attribution travels; no adopter-facing mention · [M] base
cache is hidden verbatim redistribution · [M] lockfile carries no
creator/license/URL · [M] no downstream-license position · [L] no
inbound-license statement (all T4).

**Daily-loop runtime gap (5):** [H] release Bandit gate skips the
skills registry · [M] lifecycle_planner.py outside every security
hand-list · [M] "faithful port" has drifted, no parity check · [M]
lifecycle.py false read-only/--dry-run claims · [L] R6/debt-ledger
scope misses the daily-loop surface (all T3).

**Cross-harness gap (6):** [H] zero native-tested targets incl. both
harnesses the postdoc needs · [H] reviewer-harness onboarding never
wires the instruction file · [M] Antigravity confirmation never
serialized per its own protocol · [M] cli-backstop-only vocabulary
defined nowhere adopters read; matrix orphaned · [M] VENDOR.md rename
example unfollowable by the resolver · [M] "vendor-neutral throughout"
broader than the construction-level guarantee (all T5.8/T6).

**Upgrade gap (1 verified + 4 hand-checked):** [L] lockfile schema
write-only, no read validation · plus, verified directly this session:
Cairn's own install records cairn_commit "unknown"; tag-only guidance
(`SECURITY.md:25`) routes to a v0.3.0 tag now 20 commits behind the
entry-doc fixes; the retirement-queued collaboration agreement has no
upgrade-path handling; no real-tree upgrade rehearsal has crossed a
version boundary (all T7/T5.9).

**Refuted (2, for the record):** the complexity-debt-audit
"recommendations unimplemented" claim (they all landed — kept above as
a *strength*), and a reading-burden framing that ignored the minimal
path the quickstart already names.
