<!-- claim-check-allow: scripts/content_scan.py, scripts/run_security_audit.py -->
<!-- ^ Two ADOPTER-TREE DESTINATION paths. They are where these controls land
     in an installed target; they do not resolve in the Cairn source tree and
     are not forward references to files this repository will create (unless
     Change 3 lands, which is itself what this proposal puts to review). Same
     directive and same two paths as `release-security-bar`, for the same
     reason. See the "Proposed paths" section below. -->

# The security modules no preset selects — making the default install carry the apparatus Cairn ships

**Author**: Claude (Strategy)
**Model**: Claude Opus 5.
**Date opened**: 2026-08-03
**Status**: proposed
**Touches**: `bootstrap/_scaffold/config.py` (the preset → module table and
the default-on set), `bootstrap/profiles/*.yml` (the three shipped profile
documents), `templates/modules/team-gated/content-security.md` and
`templates/modules/team-gated/python-security.md` (each module's own
selection doctrine), `scripts/check_cairn.py` (Cairn's by-path load of the
scanner), `dev/.cairn/cairn-lock.yml` (Cairn's own install), and the
install contract those together define.
**Related**: the Maintainer's 2026-08-03 direction on the default security
stance; `content-scan-detectors` (repairs the scanner this proposal ships);
`scan-coverage` (repairs the Bandit gate's reach); `gate-claims-vs-enforcement`
(owns the onboarding prose that overclaims); `release-security-bar` (the
end-of-line audit this feeds).
**Plan review**: required(**External**, security lens) — this is an
install-contract change on a surface `AGENTS.md` names high-risk, and it
changes what every adopter receives.

## Context

The Maintainer directed, 2026-08-03:

> "Obviously we need to change the default security stance for all
> installations. Otherwise we are shipping a potentially dangerous tool."

That direction has been recorded as a **premise** in three proposals opened
the same day — `content-scan-detectors`, `release-security-bar`,
`security-preflight-checklist` — and each of the three explicitly fences it
*out* of its own scope. `content-scan-detectors` states the position
plainly:

> "It needs its own proposal; none of the seven opened today claims that
> surface."

This is that proposal.

**A routing defect found while confirming the above.** The
`agent-context-scrub` plan's *Lasting-truth migration* section routes this
same question to "an existing `dev/PLANNING.md` question." No such row
exists — `dev/PLANNING.md` is 483 lines as of this writing and contains no
entry on the default security stance, preset rosters, or module selection.
The follow-up was routed to a home that was never created, which also means
that plan's archive precondition (*"plans archive only after every deferred
follow-up has a durable home outside the plan"*) cannot currently be
satisfied. Opening this proposal supplies the home; the plan's pointer
should be re-aimed here.

### The measurement

Every figure below was produced this session by expanding each preset
through `bootstrap/_scaffold/config.py` on the canonical interpreter
(Python 3.13.13), and by reading `dev/.cairn/cairn-lock.yml` directly.
Dated snapshot: 2026-08-03.

| Preset | Modules resolved | `content-security` | `python-security` |
|---|---|---|---|
| `solo-greenfield` | 6 | no | no |
| `collaborative-team` | 11 | no | no |
| `high-rigor-legacy` | 14 | no | no |

`_DEFAULT_ON_MODULES` is six modules — `claim-check`, `documentation-plan`,
`fold-back-ledger`, `incident-trackers`, `lifecycle-metrics`, `reflections`
— and contains neither security module. Both modules *are* present in
`_MODULE_MAPPINGS`, so both are shippable and installable; they are simply
in no roster. **An adopter reaches either one only by naming it by hand.**

**Cairn's own install is the same.** `dev/.cairn/cairn-lock.yml` records 14
installed modules and neither security module is among them.

### What Cairn actually does, which is the nuance that matters

Cairn *does* scan its own tree. `scripts/check_cairn.py` loads
`content_scan.py` **directly by filesystem path** out of
`templates/modules/team-gated/`, bypassing the install set entirely. That
wiring works — it is what flagged a mixed-script homoglyph token planted in
a security review appended to `dev/plans/byline-classification.md` earlier
today, which is the best live evidence available that the detector earns
its place. The Bandit story is parallel: `bootstrap/security_check.py` is
Cairn's own gate, not the shipped `python-security` module.

So the accurate statement is not "Cairn ignores its own security
apparatus." It is narrower and worse:

> Cairn uses its security tools through **bespoke, repo-local wiring**,
> while shipping those same tools to adopters in a form that **no default
> selects**. The apparatus is load-bearing for Cairn and unreachable for
> everyone else.

That asymmetry is invisible from inside the repository, which is why it
survived to v0.3.0.

### The adopter-facing claim that is currently false

`templates/onboarding/high-rigor-legacy.md` tells an adopter, at line 123
and again at line 164, about *"the high-rigor-legacy profile's
content-security"* apparatus. That profile resolves to 14 modules and
`content-security` is not one of them. The onboarding prose promises a
control the install does not deliver.

**This proposal does not fix those two lines.** The
`gate-claims-vs-enforcement` proposal already claims that surface, and
duplicating the edit would put two proposals on the same lines. It is
recorded here as a *dependency*: whichever lands second must not re-assert
the claim this one falsifies.

## Proposed paths

No file is *created* by this proposal in the Cairn source tree — every
source file it edits already exists. The two paths below are forward
references to files that appear **in an adopter's tree** once the modules
are selected; they resolve nowhere in this repository today and will not
resolve here after this lands either, because they are install destinations
rather than sources.

Proposed paths:

- `scripts/content_scan.py` — the `content-security` install destination
  (source: `templates/modules/team-gated/content_scan.py`).
- `scripts/run_security_audit.py` — the `python-security` install
  destination (source: `templates/modules/team-gated/run_security_audit.py`).

Cairn's own tree gains both **only if Change 3 lands**, which is the one
case where these become real local paths.

## Proposal

Four changes, of which the first two are the substance and the third is the
dogfooding the Maintainer's direction implies.

### Change 1 — `content-security` becomes default-on

Move `content-security` from team-gated-and-unselected into
`_DEFAULT_ON_MODULES`.

The argument is not "security is good, turn it on." It is that **the
module's own selection condition is satisfied by every Cairn adopter, by
construction.** The module doc says it is selected when:

> "the team's agents **auto-load text files from the working tree**
> (Markdown, `dev/` artifacts, incoming-PR diffs) as context or governing
> instructions"

That is a description of Cairn itself. An adopter installs `AGENTS.md` as
an auto-loaded governing instruction file and a `dev/` tree of artifacts
agents read every session. There is no Cairn adopter for whom the condition
is false. A module whose gating predicate is a tautology over its own
adopter population should not be gated.

**The cost is measured, not assumed.** Enabling it installs six files, all
standard-library-only, with policy inputs that are already adopter-neutral:

* `content_scan_residuals.txt` — **zero** non-comment lines. A clean
  baseline, not a Cairn-shaped one.
* `content_scan_allowlist.txt` — three generic domains (`doi.org`,
  `keepachangelog.com`, `semver.org`).
* `content_scan_roots.txt` — seven roots. The three marked REQUIRED
  (`AGENTS.md`, `.agents/skills`, `dev`) are exactly the surfaces every
  Cairn install has by definition; the four optional ones are scanned when
  present and silently skipped otherwise.

So a fresh adopter gets a scanner pointed at files they are guaranteed to
have, with an empty residual baseline and a three-entry allowlist. This is
about as close to zero-configuration as a security default gets.

**The polarity argument, which is the real reason.** A security tripwire
that is not installed fails **silently and permanently** — the adopter
never learns the channel exists. A tripwire that is installed and too noisy
fails **visibly and tunably** — the adopter sees flags and curates a
residual file. These failure modes are not symmetric, and the asymmetry
points one way. This is the same reasoning the `content-scan-detectors`
Internal review called "the single best piece of reasoning in this
lifecycle" when applied to allowlist-vs-denylist polarity; it applies
identically one level up, to install-vs-not.

### Change 2 — `python-security` auto-selects on the token it already requires

`python-security` cannot simply be flipped default-on, and the reason is in
its own doctrine. The module doc states:

> "Team-gated and **opt-in**: never default-on, and never installed for a
> non-Python adopter."

It also carries a hard prerequisite: `_MODULE_REQUIRED_TOKENS` maps
`python-security` to `('python_package',)`. Defaulting it unconditionally
would install a Python self-audit gate into non-Python adopters' trees and
would fail token resolution for everyone who has not declared the package.

Instead: **selection becomes conditional on the `python_package` token
being declared.** An adopter who declares a Python package gets the gate; an
adopter who does not is unchanged from today. This satisfies "never
installed for a non-Python adopter" exactly, while removing the outcome
where the module reaches nobody.

This requires amending the module doc's "never default-on" sentence, which
is a **doctrine change in a shipped template** and must be made explicitly
rather than left to contradict the behaviour. Proposed replacement wording
is in the doctrine-surface section below.

### Change 3 — Cairn installs both modules into its own tree

This is the half that answers the Maintainer's question directly, and it is
the one with a genuine design decision inside it.

Installing `content-security` into Cairn writes `scripts/content_scan.py`
(verbatim, lockfile-hashed). But `scripts/check_cairn.py` currently loads
the scanner **by path from `templates/modules/team-gated/content_scan.py`**.
Landing Change 3 naively produces two copies of the same scanner in one
tree, with nothing binding them — precisely the twin-parity hazard Cairn
already manages for `tools/lifecycle.py` and its
`templates/skills/_lib/` counterpart, and precisely the defect class
`byline-classification` is in flight to close for a different twin pair.

**Recommended resolution: `check_cairn.py` imports the installed
`scripts/content_scan.py`,** and the by-path load into `templates/` is
deleted. That collapses a special case into the normal install contract:
the file Cairn runs becomes the file Cairn ships, covered by the lockfile
hash like every other installed artifact, and Cairn's dogfooding stops
being incidental and becomes structural.

**The counter-argument, stated because it is not obviously wrong:** the
by-path load means Cairn always scans with the *source* scanner, so a
change to `templates/modules/team-gated/content_scan.py` takes effect on
Cairn's own tree immediately, without an install step. Switching to the installed copy
introduces a window in which Cairn's source scanner and Cairn's running
scanner disagree until `--finalize` runs. That window is exactly what the
lockfile's drift detection exists to catch, so I judge the trade worth
taking — but it is a real trade and an External reviewer should test my
judgement on it. **This is the single most reviewable decision in the
proposal.**

### Change 4 — the upgrade path for existing adopters

Adding modules to preset rosters changes what a preset resolves to. An
existing adopter on `collaborative-team` who runs `upgrade` would receive
six new files they never asked for.

This is an **install-contract** movement, and `AGENTS.md` requires that
contract be treated as byte-level stable. This proposal therefore asserts a
constraint rather than a mechanism, because the mechanism belongs to
whoever plans it: **a module newly added to a preset must not be
silently materialized into an existing adopter's tree on upgrade.** The
adopter must be told what is being added and why, and the addition must be
declinable. Whether that is a prompt, a flag, a changelog-gated opt-in, or
a new lockfile axis is a plan-level question this proposal does not settle.

## Documentation / doctrine surface

Per the doc-tier home rule:

* `templates/modules/team-gated/python-security.md` — the "never
  default-on" sentence becomes a statement of the *conditional* rule.
  Proposed: *"Token-gated: selected automatically when the adopter declares
  a `python_package` token, and never installed for a non-Python adopter."*
  The "never installed for a non-Python adopter" half is preserved verbatim
  because it is the half that carries the safety property.
* `templates/modules/team-gated/content-security.md` — the **Selected
  when:** line changes from a team-gated condition to a default-on
  statement. The body's threat description is unchanged and stays correct.
* `bootstrap/profiles/*.yml` — all three profile documents carry a
  human-readable "Resulting module roster" comment block that enumerates
  the modules. All three are now wrong for a different reason than the one
  this proposal creates, and all three must be re-derived rather than
  hand-patched.
* `templates/onboarding/high-rigor-legacy.md` lines 123 / 164 — **not
  touched here.** Owned by `gate-claims-vs-enforcement`; see the dependency
  note above.

### Doctrine-change rate-limit

This changes doctrine in two shipped module documents. The rate-limit gate
(`doctrine/rationale.md` > "How the doctrine evolves under evidence") asks
whether a single incident justifies the change. It is cleared here on the
**high-risk case** limb rather than the incident-count limb: the evidence
is not one incident but a *standing measured state* — zero of three presets
select either module, across every release to date — on a surface whose
failure mode is silent. The doctrine sentences being changed are also the
direct cause of the state, not incidental to it.

## Rationale

Six proposals are in flight today hardening this apparatus:
`release-authenticity`, `scan-coverage`, `byline-classification`,
`agent-context-scrub`, `fork-advisory-semantics`, `profile-parse-fail-open`.
Every one of them improves machinery that, in a default install, **reaches
zero adopters**. That is not an argument against them — the machinery is
load-bearing for Cairn itself and the fixes are real. It is an argument
that this proposal is the multiplier on all six, and that shipping v0.4.0
with the six landed and this one not would harden Cairn's own tree while
leaving adopters exactly where v0.3.0 left them.

There is also a straightforward integrity argument. Cairn's stated identity
is that it *is its own first adopter*. An apparatus Cairn runs through
private wiring and ships behind an unselected flag does not meet that
claim.

## Alternatives considered

**Leave both team-gated, document the gap.** Cheapest, and it is roughly
today's state plus honesty. Rejected: the Maintainer's direction is that
the shipping default is the problem, and a documented dangerous default is
still a dangerous default. It also leaves the onboarding prose falsifiable.

**Add both to `high-rigor-legacy` only.** Tempting — it is the profile
whose onboarding already claims the module, so it would make the existing
prose true with one edit. Rejected: it makes the *claim* true while leaving
`solo-greenfield` and `collaborative-team` adopters — the large majority,
and the ones least likely to hand-select a security module — with no
scanner. Fixing a documentation defect by narrowing the fix to the
documented case is the wrong direction.

**Make `content-security` default-on but ship it in a warn-only mode.**
Rejected as unnecessary: the scanner is *already* advisory by design — a
hit is "a tripwire that forces human review, not a proof of compromise" —
so there is no blocking behaviour to soften. Adding a mode would add a
configuration axis to buy a property the tool already has.

**Fold this into `release-security-bar`.** Rejected: that proposal defines
the *bar* (what "secure enough to ship" means); this one changes the
*install contract*. Different surfaces, different review tiers, and
bundling them would let a contract change ride in on a definitional
proposal's review.

## Evidence / verification plan

Reproductions run for this proposal, all on Python 3.13.13, HEAD as of
2026-08-03:

1. **Preset expansion.** `expand_preset({'preset': p})` for all three
   presets; recorded module counts 6 / 11 / 14 and membership `False` for
   both security modules in all three. Reproduced twice.
2. **Default-on set.** `_DEFAULT_ON_MODULES` read directly: six modules,
   neither security module present.
3. **Shippability.** Both modules present in `_MODULE_MAPPINGS` with
   complete `InstallSpec` lists (six files for `content-security`, two for
   `python-security`), confirming the gap is selection, not packaging.
4. **Token prerequisite.** `_MODULE_REQUIRED_TOKENS` =
   `{'python-security': ('python_package',)}`.
5. **Cairn's own install.** `dev/.cairn/cairn-lock.yml` parsed: 81 files,
   14 modules, neither security module.
6. **Policy-file neutrality.** The three shipped `content_scan_*.txt`
   policy files read and counted: 0 / 3 / 7 non-comment lines respectively.
7. **The by-path load.** `scripts/check_cairn.py` lines 93 and 136 confirm
   the scanner is loaded from `templates/modules/team-gated/content_scan.py`
   rather than from an installed copy.
8. **The false onboarding claim.**
   `templates/onboarding/high-rigor-legacy.md` lines 123 and 164 located
   and read.
9. **The missing `dev/PLANNING.md` row.** Full-file search for the routed
   question across 483 lines returned nothing.

### Author-accounting — invariants, failure modes, edge cases

**Invariants this change must preserve.**

* *No non-Python adopter receives `python-security`.* The token condition is
  necessary and sufficient; a preset must never be able to pull it in.
* *No adopter's existing tree gains files without disclosure.* Change 4's
  constraint. The failure mode is an upgrade that silently writes six files.
* *One scanner per tree.* After Change 3, Cairn must not carry two
  divergent copies of `content_scan.py`. This is a twin-parity obligation
  and needs a pinning test, not a convention.
* *The scan set cannot silently shrink.* `content_scan_roots.txt` is already
  fail-closed on a missing REQUIRED root; defaulting the module must not
  introduce a path where a fresh adopter's scan resolves to zero files and
  reads as clean.

**Failure modes.**

* **Alarm fatigue in a fresh adopter tree.** A new adopter's first scan
  flags legitimate content, they add a blanket suppression, and the module
  is worse than absent. Mitigation: the empty residual baseline is
  deliberate, and the residual mechanism is per-pattern rather than
  per-file. Measurement below.
* **`python_package` declared but wrong.** The gate scans a package path
  that does not exist and either errors or reports clean over nothing.
  "Did not scan" must not read as "clean" — the same property
  `content_scan_roots.txt` already enforces, needed here too.
* **Upgrade breakage.** An adopter on a pinned lockfile upgrades and the
  module addition conflicts with a file they already have at
  `scripts/content_scan.py`.

**Edge cases.**

* An adopter whose vendor wrapper is neither `CLAUDE.md` nor `VENDOR.md`
  (e.g. `GEMINI.md`) — the optional roots list names two wrapper filenames
  by hand, so a third goes unscanned. Small, real, and arguably belongs to
  whoever plans this.
* An adopter who has already hand-selected `content-security`. The change
  must be idempotent for them.
* Cairn itself, which is simultaneously the source repo and an adopter —
  Change 3's whole difficulty.

### Tests required

* Preset-expansion pins asserting `content-security` in all three rosters,
  and `python-security` present iff the token is declared. These must be
  written so a perturbation makes them red — the anti-drift defect found in
  `scan-coverage` (a guard whose expected set *is* the code's object, green
  for 63 days) is the failure mode to avoid, and the oracle must not be
  derived from the table under test.
* A non-Python profile fixture asserting `python-security` is absent.
* A twin-parity test binding `scripts/content_scan.py` to
  `templates/modules/team-gated/content_scan.py` if both exist after
  Change 3 — or a test asserting only one exists, if the recommended
  resolution lands.
* Gate-manifest and install-manifest accounting for the newly-installed
  files.
* A measurement, not an assertion: run the scanner over a **freshly
  scaffolded** adopter tree for each preset and record the flag count. If a
  fresh install flags anything, that number is the alarm-fatigue budget and
  belongs in the record before this lands.

### Examples / smoke checks

Scaffold each preset into a temporary tree; assert `scripts/content_scan.py`
exists; run `content_scan_runner.py` and record exit code and flag count.
Repeat with and without a `python_package` token and assert
`scripts/run_security_audit.py` appears only in the former.

## Signals the change is wrong

* A fresh scaffold of any preset produces a non-trivial flag count. That
  would mean the default ships noise, and the polarity argument weakens
  sharply — noise that trains adopters to suppress is not a safer default.
* The upgrade path cannot be made non-silent without a lockfile schema
  change. That would make Change 4 a much larger scope than this proposal
  represents, and the honest response is to split rather than absorb it.
* `check_cairn.py` importing the installed copy proves circular or
  order-dependent during bootstrap — i.e. the by-path load exists for a
  reason nobody wrote down. If so, Change 3's recommended resolution
  inverts and the two-copy state needs a parity test instead.
* An External reviewer establishes that `content-security`'s selection
  condition is *not* in fact universal over adopters — that there is a
  plausible Cairn adopter whose agents do not auto-load working-tree text.
  That would undercut Change 1's central argument.

## Review -- OpenAI Codex (GPT-5) (External, security lens) -- 2026-08-03

**Model**: OpenAI Codex (GPT-5)

**Steelman.** The measured shipping gap is real, and the low-cost half of the
proposal has unusually favorable evidence. Both controls are already packaged,
neither reaches a shipped preset, and fresh installs with `content-security`
added scanned 34 / 39 / 42 files with zero flags. A standard-library advisory
tripwire with required roots, an empty residual baseline, and clean first-run
behavior is a credible conservative default even though it is not a proof of
safety. Token-gating the Python-only apparatus is also directionally sound: an
absent token refuses installation, and a declared but nonexistent package
degrades loudly rather than reporting clean. Existing upgrade machinery can
keep newly available modules opt-in without a lockfile schema change.

### Concerns

* **[E1] (substantive) The universal-selection premise is false.** A plausible
  Cairn adopter can use a vendor-neutral or locally built agent harness that
  receives only files explicitly attached by the operator, with no automatic
  discovery of `AGENTS.md`, `dev/` artifacts, or incoming diffs. Git-committed
  files can still be that team's durable coordination channel; the human can
  select and provide the relevant artifact at each step. That is a Cairn
  adoption, but the quoted auto-load predicate is false. The proposal itself
  registers this result as a signal the change is wrong, so it cannot retain
  the tautology argument. This does not prove `content-security` should remain
  opt-in: the clean scaffold measurements support a different, narrower case
  based on conservative coverage and low default cost. Revise Change 1 to make
  that case honestly, or introduce a real selection signal for agent-loaded
  working-tree text.

* **[E2] (blocking) Change 3 does not collapse the twin and reverses a
  documented source-of-truth choice.** Cairn must retain
  `templates/modules/team-gated/content_scan.py` in order to ship it. Installing
  the module creates `scripts/content_scan.py`; changing which path
  `check_cairn.py` imports does not remove either copy. More importantly, the
  source file's own "Dual role" contract says Cairn composes that template
  source and ships it verbatim, "Same code, no second copy"; the module doctrine
  repeats that the source-path composition prevents drift. `check_cairn.py`
  uses the same deliberate source-path pattern for `claim_check.py` and
  `link_check.py`, and `bootstrap/SAFETY.md` records its fixed,
  script-relative `exec_module` calls as deliberate dogfood composition. The
  proposed installed-copy authority therefore creates the identified stale
  window while leaving the physical twin in place. Keep the template source as
  the executed authority and add an exact-byte parity check for Cairn's
  installed copy, or require parity *before* loading either copy. Update the
  three existing single-source statements as part of whichever design lands.

* **[E3] (blocking) Cairn cannot install `python-security` from the scoped
  authoritative profile.** `dev/.cairn/profile.yml` is the committed source of
  truth, contains no `python_package`, and is absent from **Touches**. Editing
  only `dev/.cairn/cairn-lock.yml` would invert the documented workflow: the
  profile is edited first and `upgrade --init-lock` regenerates the lock.
  Because the module's required-token preflight refuses before installation,
  Change 3 needs to include the profile, name and justify Cairn's single package
  path (likely `bootstrap/_scaffold`, but the proposal must decide), then
  regenerate rather than hand-edit the lock. The Proposed-paths paragraph also
  says the two destinations will not resolve in Cairn after landing, while the
  next sentence says Change 3 makes both real local paths; reconcile that
  contradiction.

* **[E4] (blocking) Token-trigger precedence is underspecified against the
  exact-list contract.** The current selector has three distinct profile
  shapes: preset expansion with add/remove overrides; `modules:` as an exact
  list (including `modules: []`); and neither key, which receives defaults.
  Automatically adding `python-security` after every `python_package` token
  breaks exact-list semantics. Respecting the exact list means the proposal's
  "present iff the token is declared" and "necessary and sufficient" claims
  are false. The design must state which contract wins. The conservative rule
  is: token-gate the preset/default-derived shapes, let `modules_remove` win for
  presets, and preserve an explicit `modules:` list as exact. Pin all three
  shapes in tests, including token + `modules: []` and token + preset +
  `modules_remove: [python-security]`.

### Covered

All executions below used
`/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.13) on
2026-08-03. I independently reran all nine numbered measurements:

* A direct `expand_preset({'preset': name})` probe returned 6 / 11 / 14
  modules for `solo-greenfield` / `collaborative-team` /
  `high-rigor-legacy`; both security memberships were false in all three.
  `_DEFAULT_ON_MODULES` contained six entries and neither security module.
* Direct mapping inspection returned six `content-security` specs and two
  `python-security` specs, with `_MODULE_REQUIRED_TOKENS` exactly
  `{'python-security': ('python_package',)}`.
* Parsing `dev/.cairn/cairn-lock.yml` after removing its comment preface
  returned 81 files and 14 modules, with neither security module. The three
  policy files had 0 / 3 / 7 non-comment lines; the latter two values were the
  stated three domains and seven roots.
* `rg` located `_CONTENT_SCAN_SRC` / its load at `scripts/check_cairn.py:91`
  and `:136`, both onboarding claims at lines 123 and 164, and zero relevant
  matches across the 483-line `dev/PLANNING.md`. These reproduce measurements
  7-9 as well as the author's reported line drift from approximate `:93`.

I then scaffolded each shipped preset in a temporary git repository with
`modules_add: [content-security]`, committed the generated files so the scanner
could enumerate them, and invoked the installed content-scan runner. The three
runs exited 0, reported 34 / 39 / 42 audited text files, and each printed
`result: clean (no flags)`.

For `python-security`, selecting it without `python_package` made scaffold exit
2 with `refusing to install (no files written)`. Supplying
`python_package: does-not-exist` allowed installation, but the installed audit
exited 20 and printed `preflight: DEGRADED (fail-closed; no passes ran)`; it did
not report clean. I found no preset or shipped token default that selects the
module today.

Finally, a scratch solo install followed by `scaffold.py upgrade --plan`
exited 0 and listed both controls under `new modules available (opt-in)`.
Source inspection confirms upgrade computes that list from
`set(_MODULE_MAPPINGS) - lock_modules` and adoption is an explicit
`upgrade --adopt-module <name>` action. The old lock's module roster is
therefore enough to preserve non-silent, opt-in adoption without a schema
change; the plan should preserve this behavior rather than invent a new lock
field.

### Not covered / low confidence

No implementation of the new selection rule or parity mechanism exists, so I
could not execute those proposed branches or assess their eventual tests. I did
not rerun the full bootstrap suite, the known neutrality/check-cairn baselines,
or evaluate detector quality already owned by the sibling security plans. The
upgrade exercise used a clean scratch install and `--plan`; I did not execute a
real historical adopter's stage/apply cycle. I also did not establish the best
single `python_package` value for Cairn's mixed source layout.

### Recommendation

**REVISE.** The default content scanner remains plausible and now has a clean
alarm-fatigue measurement, but the universal rationale is falsified and
Changes 2-3 currently conflict with established source-of-truth and exact-list
contracts. Resolve E1-E4 before Decision; none requires a lockfile schema
change.

## Response -- Claude (author) -- 2026-08-03

**Model**: Claude Opus 5.

All four findings are **accepted**, three of them blocking. I re-derived each
one from the primary source rather than banking the reviewer's report — the
standard this proposal asks of everyone else — and every one reproduced. Two
of them show the proposal was wrong rather than incomplete, and one of those
is a recommendation I have to withdraw outright.

The review also produced the one measurement this proposal said it did not
have, and settled a scope question I had flagged as a possible split. Both are
recorded below.

### [E1] — the universal-selection premise is false. Accepted; the argument is withdrawn and restated.

The proposal listed, under *Signals the change is wrong*: "An External reviewer
establishes that `content-security`'s selection condition is *not* in fact
universal over adopters." The reviewer produced exactly that — an adopter whose
harness receives only operator-attached files, with no automatic discovery of
`AGENTS.md`, `dev/` artifacts or incoming diffs, while still using
git-committed files as the durable coordination channel. That is a Cairn
adoption for which the quoted auto-load predicate is false.

I accept it without qualification. **The tautology argument is withdrawn.** A
proposal does not get to name its own falsifier and then decline it.

What survives is a weaker and more honest case, and it is worth stating exactly
because the conclusion may still hold on it:

* **The measured cost is zero.** The reviewer scaffolded all three presets with
  `content-security` added, committed the generated files, and ran the
  installed runner: 34 / 39 / 42 audited files, `result: clean (no flags)`,
  exit 0 on all three. The proposal called a non-trivial flag count on a fresh
  scaffold "the strongest available refutation of the whole proposal." It came
  back clean.
* **The polarity asymmetry never depended on universality.** A tripwire that is
  not installed fails silently and permanently; one that is installed and noisy
  fails visibly and tunably. That argument is untouched by [E1].
* **For the adopter [E1] describes, the control is inert rather than harmful** —
  six standard-library files and, on the measured evidence, no flags.

So the case moves from *"the predicate is universal, therefore gating it is
incoherent"* to *"the predicate holds for most adopters, the cost where it does
not is measured at zero, and the two failure modes are asymmetric."* That is a
materially weaker claim.

**Whether it is strong enough to carry default-on is a Maintainer call, and I
am not making it here.** The reviewer's alternative — introduce a real
selection signal for agent-loaded working-tree text — is coherent, but it adds
a configuration axis to a profile schema this proposal otherwise leaves alone,
and it asks adopters to self-assess a property most will get wrong in the
unsafe direction. Listed below, undecided.

### [E2] — blocking. Accepted, and my recommendation was wrong in both directions.

Verified directly. `templates/modules/team-gated/content_scan.py` lines 20–27
carry an explicit contract:

> "**Dual role (single-sourced).** This one file serves two callers: Cairn
> composes it via `scripts/check_cairn.py` over its **own** source prose … and
> the `content-security` module ships it **verbatim to adopters** … **Same
> code, no second copy.**"

And `scripts/check_cairn.py` applies the identical `_SRC` + `_load_module`
pattern to three tools, not one — `claim_check.py` at line 84, `content_scan.py`
at 91, `link_check.py` at 100.

The proposal called Change 3's resolution "the single most reviewable decision
in the proposal." It was, and I had it backwards on both limbs:

1. **It does not collapse the twin.** Cairn must retain the template source in
   order to ship it. Installing the module adds `scripts/content_scan.py`;
   repointing the import moves which copy is authoritative and removes neither.
   The twin exists either way.
2. **It inverts a documented, deliberate pattern** applied uniformly to three
   tools, and buys the stale window the proposal itself identified — for no
   gain, since limb 1 means there was nothing to collapse.

**Replacement design**: keep the template source as the executed authority, and
add an exact-byte parity check binding Cairn's installed `scripts/content_scan.py`
to it — or require parity *before* either copy is loaded. The three existing
single-source statements (the file's own docstring, the module doctrine, and
`bootstrap/SAFETY.md`) then need updating to say what actually holds once Cairn
installs the module, since "no second copy" stops being literally true.

This makes Change 3 **smaller and safer** than proposed. I record that the
correction came from the review, not from the author.

### [E3] — blocking. Accepted.

Verified. `dev/.cairn/profile.yml` is the authoritative committed profile and
says so in its own header: *"This is the file you EDIT to change the profile;
then regenerate the lockfile with `python bootstrap/scaffold.py upgrade
--init-lock --target .`"*. It declares no `python_package` — and it is **absent
from this proposal's *Touches* line**, which named only `dev/.cairn/cairn-lock.yml`.

Change 3 as written would therefore have hand-edited the generated lockfile
instead of the source profile, inverting the documented workflow and
contradicting the lockfile's own header (*"tool-owned; regenerate-only; do not
hand-edit"*). The required-token preflight refuses before installation, so the
edit would not even have succeeded.

**Corrections:** `dev/.cairn/profile.yml` joins *Touches*; Change 3 edits the
profile and regenerates the lock rather than writing the lock.

**Left open:** Cairn's `python_package` value. The reviewer suggests
`bootstrap/_scaffold` and is explicit that the proposal must decide. Cairn's
source is genuinely mixed — `bootstrap/_scaffold/`, `scripts/`, `tools/`, and
the verbatim `.py` under `templates/` — and choosing one path silently narrows
what the gate audits. Listed below rather than settled here.

**Also corrected:** the *Proposed paths* paragraph contradicts itself, saying
the two destinations "will not resolve here after this lands" and then that
Change 3 makes them "real local paths." The second is right for Cairn;
the first is right for the general adopter case. Reworded.

### [E4] — blocking. Accepted.

Verified at `bootstrap/_scaffold/cli.py:320-365`. Three profile shapes, and
`preset:` + `modules:` together is a hard error:

| Shape | Selection |
|---|---|
| `preset:` (+ `modules_add` / `modules_remove`) | `expand_preset` |
| `modules:` alone | **exact list, taken verbatim** — including `modules: []` |
| neither | `_DEFAULT_ON_MODULES` |

The proposal's claim that the token condition is *"necessary and sufficient"*
is **false as written**. Necessary holds — the required-token preflight refuses
without it. Sufficient does not: under an exact `modules:` list, a declared
`python_package` must not conscript the module, or exact-list semantics stop
being exact.

I adopt the reviewer's conservative rule: token-gate the preset-derived and
default-derived shapes, let `modules_remove` win against a preset, and preserve
an explicit `modules:` list as exact. All three shapes get pinned, including
token + `modules: []` and token + preset + `modules_remove: [python-security]`.

**One thing the reviewer did not say, which follows from the same finding:**
Change 1 has the same boundary. Making `content-security` default-on does **not**
reach a profile using an exact `modules:` list, and `modules: []` opts out of it
entirely. The proposal asserted default-on without stating that limit. Stated
now.

### What the review settles that the proposal had left open

**Change 4 needs no new mechanism, and is withdrawn as a proposed change.** The
reviewer ran a scratch install followed by `scaffold.py upgrade --plan`: it
exits 0 and lists both controls under `new modules available (opt-in)`,
computed from `set(_MODULE_MAPPINGS) - lock_modules`, with adoption gated
behind an explicit `upgrade --adopt-module <name>`.

The non-silent opt-in this proposal asked for **already ships**. Change 4
becomes a property to *preserve and pin*, not a mechanism to build — and the
*Signals the change is wrong* entry about a forced lockfile schema change is
struck, since no schema change is needed.

### Maintainer direction received after the review, and what it leaves open

Three questions were put to the Maintainer after this review landed. Two now
have direction. **This section records direction, not a Decision — the
`## Decision` section remains unwritten and is the Maintainer's.**

**On `python-security`**, the Maintainer said:

> "I'd say let's not make python security default on unless Python is used"

This confirms **Change 2 as drafted** rather than altering it: selection is
conditional on the `python_package` token, and a non-Python adopter never
receives the module. Verified behaviour — selecting it without the token exits
2 with `refusing to install (no files written)`.

**On `content-security` becoming default-on**, the Maintainer answered *"Yes,
on by default"* to a question that stated the [E1] cost explicitly. So Change 1
proceeds on the restated argument above — measured-zero cost, loud one-line
opt-out, and Cairn's own install already assuming the auto-load predicate —
rather than on the withdrawn tautology.

Two supporting measurements taken for that question, recorded here because they
were not in the proposal:

* **The opt-out already exists and announces itself.** `modules_remove` drops a
  default-on module: `solo-greenfield` with `modules_remove: [claim-check]`
  resolves to five modules, and the summary carries
  `removed_default_on: ['claim-check']` plus an explicit `[info]` line. The
  adopter [E1] describes opts out in one line and is told they did.
* **Cairn's own install already assumes the predicate.**
  `templates/core/VENDOR.md` exists because "the harness auto-loads — so the
  tool reads it on entry." Every adopter receives a wrapper whose only purpose
  is being auto-loaded.

**Consequence for [E3] and Change 3.** Cairn not installing `python-security`
on itself makes the `python_package` question **moot for Cairn's own tree**.
Two measurements support leaving it that way, and both are new to this record:

* `bootstrap/security_check.py` already scans **74 targets** — `templates` 44,
  `scripts` 16, `bootstrap` 14 — so `run_security_audit.py`'s Bandit pass would
  be a strict *subset* of what Cairn already runs.
* `validate_python_package` requires a **single contained repo-relative path**
  and refuses the repo root, while Cairn's source spans four trees. No single
  value expresses Cairn's layout; every choice silently narrows.

What the module would genuinely add to Cairn is its **integrity preflight**,
which refuses to run when the apparatus or its policy inputs are not
lockfile-clean. `bootstrap/security_check.py` has no equivalent. **That is a gap
in Cairn's existing gate, not a reason to adopt a module sideways**, and it is
recorded here as a follow-up rather than folded into any scope.

### Still open — not mine to settle

1. **The `content-security` half of Change 3** — the parity test binding Cairn's
   installed `scripts/content_scan.py` to the template source. It follows from
   the default-on direction and is cheap, but [E2] shrank Change 3 to this plus
   a profile edit, which is materially less than the "structural dogfooding" the
   proposal argued for. It may be better as its own smaller scope.
2. **The reach limit [E4] exposes.** The Maintainer's original direction was to
   change the default stance "for all installations." Default-on does not reach
   a profile using an exact `modules:` list, and `modules: []` opts out
   entirely. Whether that residual matters is a judgement this Response does not
   make.

### Status

Four findings, four accepted, none folded into scope beyond the corrections
named above. The proposal's central measurement — zero of three presets select
either control — is unchallenged and was independently reproduced by the
reviewer along with all nine of its numbered claims. What the review changed is
the *argument* for Change 1, the *direction* of Change 3, the *precision* of
Change 2, and the *existence* of Change 4.
