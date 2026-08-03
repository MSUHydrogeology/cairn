<!-- cairn-internal-ref-allow: doctrine/doc-governance.md doctrine/proposals.md doctrine/dual-review.md doctrine/fold-back.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see AGENTS.md, "Where doctrine/ references resolve") -->

# The front door — a contributor entry point, and a disclosure channel that outlives the roster

**Author**: Claude (Strategy)
**Model**: Claude Opus 5
**Date opened**: 2026-08-03
**Status**: proposed
**Touches**: `CONTRIBUTING.md` (new, repository root), `SECURITY.md`
(the *Reporting a vulnerability* section only), `README.md` (one pointer),
`dev/.cairn/profile.yml` (one clarifying comment; no value changes)
**Deliberately not touched**: `dev/.cairn/profile.yml`'s `human_team` value,
`templates/optional/CONTRIBUTING.md`, `bootstrap/_scaffold/`, the fidelity
manifest spec, and the lockfile. Recorded in the header so a reader can tell a
scoping decision from an oversight without reading to the residuals.
**Related**: `identity-not-name` (**superseded** 2026-08-03, Decision `6c6ce39`),
successor scope 4 of 4, and its finding [IDN5]; the sibling Theme 3 proposals
`scan-coverage` and `agent-context-scrub`, which claim other sections of
`SECURITY.md` — see *Cross-lineage collisions*; the `gate-reanchor-preflight`
lifecycle, whose dated-posture pattern this proposal reuses for its residuals
**Plan review**: `required(Internal)` — with a **non-review ordering
precondition** (the disclosure channel is verified live before the prose that
names it lands) and a stated escalation condition. The reasoning is in
*Plan review tier, and why not External* below, because under-calling a tier
silently is exactly the failure this lineage exists to correct.

## Context

The `identity-not-name` proposal was superseded on 2026-08-03 and split into
four successor scopes. This is the fourth: **contributor entry and
disclosure** — the least security-critical of the four, and the one a real
human is most likely to touch first.

Two concrete gaps, both verified against the live tree on 2026-08-03:

1. **There is no front door.** A `git clone` of this repository produces no
   `CONTRIBUTING.md` at the root. `README.md` (327 lines, `as_of 2026-08-03`)
   has no *Contributing* heading, no test command, and no development-environment
   guidance; a search of it for `pytest`, `interpreter`, `requirements`, or a
   Python version returns nothing relevant. The information a contributor needs
   *does* exist — but it is in `AGENTS.md`, a file whose own opening frames it
   as the operational reference for **AI agents**, and in
   `bootstrap/DEPENDENCY_BUDGET.md`, which nothing at the entry layer points to.
2. **There is no disclosure channel.** `SECURITY.md:29` opens *"Reporting a
   vulnerability"* and instructs a reporter to report *"privately to the
   maintainer"* — naming no address, no form, and no mechanism. A scan of
   `SECURITY.md` and `README.md` together for anything address-shaped
   (an `@`-form address, a `mailto:` link, a GitHub-advisory reference) returns
   **zero** hits. A security researcher who finds a template-injection path in
   Cairn today has been told to do something the repository does not tell them
   how to do.

This matters now rather than later for a specific reason: Cairn is
pre-first-external-adopter, and the first adopter is a postdoc. The first
outside contribution and the first outside vulnerability report will arrive
from the same population, and both currently land on an unmarked door.

**A caution about how this scope was reached.** The parent proposal's Part 4
proposed flipping `dev/.cairn/profile.yml:19` from `human_team: solo` to
`small-multi` to make the scaffold auto-install `CONTRIBUTING.md`. [IDN5]
rejected that: `human_team` is a **staffing descriptor** (how many humans work
this repository), not a **contribution-readiness switch** (whether the project
accepts outside work). The author accepted the finding. This proposal honours it
— and, as *Residual R1* records, discovers that the same conflation is baked
into the engine in the opposite direction, where this scope cannot reach it.

## Proposed paths

Proposed paths:
- `CONTRIBUTING.md` — the repository-root contributor entry point this proposal creates; materializes at implementation.

## Proposal

Three files change, one file gains a comment, and one question is **asked, not
answered**. No code changes. No test changes. No engine, install-contract, or
lockfile surface is touched.

### 1. A project-owned root `CONTRIBUTING.md`

**What it is.** A repository-root `CONTRIBUTING.md`, authored from
`templates/optional/CONTRIBUTING.md` as its starting text, with the
`contributing-specifics` slot at `templates/optional/CONTRIBUTING.md:44`
filled for Cairn.

**What it is *not*, and this distinction is the whole design.** It is **not**
the scaffold-installed optional template. Cairn's profile selects no optional
template — `dev/.cairn/cairn-lock.yml:598` records `"optional_templates": []`,
which is *correct* and stays correct, because the gate at
`bootstrap/_scaffold/config.py:249` installs `CONTRIBUTING.md` only when the
`human_team` axis resolves to `small-multi` or `large-multi`, and Cairn's is
`solo`. Cairn's root file is therefore **project-owned**: outside the lockfile,
outside the fidelity manifest's `optional_templates` block, and receiving no
template upgrades.

That is not an improvisation — it is the shape `doctrine/doc-governance.md`
already sanctions for `RULES.md`: *"an optional, repo-root, **project-owned**
rules file that Cairn **never templates and never tracks**."* The parallel is
close but not exact, and the difference is the source of *Residual R1* and
*R2*: `RULES.md` shares its name with nothing Cairn ships, whereas
`CONTRIBUTING.md` shares its name with a template Cairn *does* ship under a
dimension gate. The file is honest about this in its own header.

**Why start from the template rather than write fresh.** Cairn ships
`templates/optional/CONTRIBUTING.md` to adopters and has never used it itself.
Authoring from it is the only dogfooding that surface gets, and the template's
own slot placeholder says an empty slot at first release is a review finding —
a rule Cairn has been applying to adopters while shipping no instance of its
own. Keeping the `cairn:slot` markers in Cairn's copy also makes a future
migration mechanical if the axis ever moves (see *R2*).

**What the `contributing-specifics` slot carries.** Five things, each of which
a fresh contributor cannot currently discover from the entry layer, and each
kept to a pointer wherever a canonical home already exists:

* **The canonical interpreter.** Python 3.13.x, and *why it is not advice*:
  `bootstrap/DEPENDENCY_BUDGET.md:127` records, measured 2026-07-22 on one tree
  with nothing differing but the interpreter, that off-canon the AST attestation
  reports *hundreds* of spurious mismatches and the Bandit gate **silently
  skips** rather than failing — and a skip reads as a pass. A contributor who
  runs the suite on 3.12 and reports "the attestation is broken" has hit a
  documented environment mismatch and has no way to know it.
* **The dev dependencies.** `pip install -r bootstrap/requirements-dev.txt` —
  one package (`vermin`), dev-only, never in the adopter runtime path. This file
  exists today but is referenced only from `bootstrap/DEPENDENCY_BUDGET.md`,
  `doctrine/runtime-contract.md`, a test module, and `dev/PLANNING.md` — nothing
  a contributor reads. The same sentence states the load-bearing fact that
  **adopters take zero runtime dependencies**, so a contributor understands why
  a pull request adding an import is a contract question rather than a
  preference.
* **The test command.** `python -m pytest bootstrap/tests`. This is the one
  **deliberate duplication** in the file: `AGENTS.md` is the canonical home, and
  the slot's own placeholder text explicitly asks for "how to run the tests."
  The file carries an inline *Sync note* naming `AGENTS.md` as canonical and the
  sync direction — the same pattern `dev/proposals/_template.md` already uses
  for its escape-hatch gloss. Named here so a reviewer checks the note exists
  rather than discovering the duplication.
* **The local interpreter binding.** `dev/.cairn/local-env.json` is gitignored
  (line 7 of `.gitignore`), so a fresh clone has none. `_resolve_interpreter` at
  `templates/skills/_lib/lifecycle.py:387` **degrades** rather than refusing when
  the file is absent: it returns the currently-running interpreter with
  `source="fallback"` and the caller surfaces install guidance. A contributor
  needs one sentence saying the file is written by the bootstrap, that its
  absence is expected and warned about rather than broken, and that
  hand-authoring it is not a routine step. **This documents the binding; it
  changes nothing about it** — not its schema, validation order, fallback
  disposition, warning visibility, or subprocess use, which `AGENTS.md` lists as
  the changes that would take a Security Review.
* **A router for the four contribution shapes**, all pointers, no duplication:
  an **issue** (`.github/ISSUE_TEMPLATE/` ships generic `bug` / `friction` /
  `gap` / `wish` forms); a **case study** (`case-studies/README.md` already
  carries the three-step procedure and the bar); a **fold-back from a
  deployment** (the `.github/PULL_REQUEST_TEMPLATE/foldback.md` template and its
  export-safety gate); and an **ordinary code or documentation pull request**.

**On the licensing question, which looks worse than it is.** A mixed `.py` +
`.md` pull request is not two licenses in one change from the contributor's
side, because **the contributor never chooses**. The split is deterministic per
file, with the precedence rule stated in both license files.
`LICENSE-MIT.md` puts it directly:

> **Source code takes precedence over the document license:** a code file is
> MIT even when delivered inside the otherwise-CC-BY `templates/` tree.

`LICENSE-CC-BY.md` states the same rule from the other side as its Exception 1:
any source-code file *"is **MIT, wherever it lives**"*, and *"A code file is
never CC BY, even when it sits beside CC-BY documents."* File kind determines
license; nothing about a pull request's *composition* changes that.

So the inbound-license statement is one sentence, and it is **already written in
Cairn's own words** at `case-studies/README.md:101`, scoped to one directory:
*"A case study contributed to Cairn is offered under the same license split as
the rest of the repository — CC BY 4.0 for the prose … MIT for any code."*
Generalizing "A case study" to "A contribution" is a copy-edit, and it is the
whole of the inbound-license term. The paragraph **restates** the split; it
introduces no new term, and that is a hard constraint on the implementation,
because the by-file split is a named protected contract in `AGENTS.md`.

**The one genuinely non-obvious point deserves its own sentence**, and it must
be stated precisely rather than dramatically. The brand mark
(`docs/assets/cairn-banner.svg`) is CC BY-ND: *"you may **not** distribute
modified versions of it, so the identity mark stays canonical."* A contributor
who "improves" the logo and opens a pull request has done work Cairn cannot
merge — not because the mark can never change (the copyright holder may change
their own work; ND binds licensees, not the licensor) but because the
contributor received the mark under a licence that did not permit them to make
and distribute that derivative. The correct guidance is therefore procedural:
**brand-mark changes go to the Maintainer as an issue, never as a pull
request.**

**No CLA.** Argued, not asserted, on four grounds — the third is the one that
decides it for this audience:

1. **The option a CLA buys is one Cairn has already committed not to exercise
   unilaterally.** A contributor licence agreement's main benefit is
   relicensing optionality. Cairn's outbound licences (MIT, CC BY 4.0) are
   already permissive and irrevocable, and the by-file split is a *named
   protected contract* in `AGENTS.md` — a relicense would take a proposal and a
   Maintainer Decision regardless. The CLA protects a manoeuvre the governance
   already gates.
2. **The friction falls hardest on exactly the contributor Cairn wants.** The
   usual CLA flow is an account with a third-party signing service plus a bot
   checking every pull request. For a postdoc sending a one-file case study or
   a typo fix, that is a hard stop unrelated to the change.
3. **Institutional entanglement.** Many CLAs require a corporate or
   institutional signature where the contributor's employer holds the IP. For an
   academic contributor, routing a two-paragraph documentation fix through a
   university technology-transfer office is a guaranteed abandonment. This
   argument is *stronger* for a scientific-audience project than for general
   open source, and it is why the answer is not merely "not yet" but "no."
4. **There is no entity to hold the assignment.** Cairn's copyright line is
   *"Anthony Kendall and the Cairn contributors"* — a natural person plus an
   unincorporated set. A CLA assigning rights to an individual is a *worse*
   trust proposition for a contributor than no CLA at all.

**Steelmanned counter-argument**, because the finding it names is real: without
a CLA there is no explicit record that a contributor had the right to
contribute. The *licence grant* is covered by the inbound-equals-outbound term
above (and, on this forge, by its terms of service default). What is genuinely
missing is an **originality warranty** — and that is what a DCO, not a CLA, is
designed to supply cheaply. It is carried as *Residual R4* rather than waved
away.

**No DCO yet.** Three grounds:

1. **A DCO's entire value is that it is checked.** Its mechanism is a
   `Signed-off-by:` trailer verified by a bot or CI on every pull request.
   Cairn has no CI — indeed the sibling `gate-claims-vs-enforcement` proposal's
   whole thesis is that this tree's existing "CI-proven" claims are false,
   because the gates are suite-run, not CI-run. An unenforced DCO is a sentence
   plus a `-s` flag half of contributors will forget, after which the Maintainer
   must either reject good work over a trailer or ignore the project's own
   stated rule. Both outcomes are worse than not claiming it.
2. **Adopting an unenforced control this week would be a fresh instance of this
   lineage's own named failure class.** The parent proposal exists because
   `bootstrap/PROVENANCE.md` promises signing that the shipped verifier does not
   check. Writing a second unenforced control into Cairn's front door while
   correcting the first is precisely the mistake to avoid.
3. **Deferring costs nothing that adopting early buys.** A DCO can be adopted at
   any future point going forward; pre-DCO commits stay covered by the
   inbound-equals-outbound term. The cost curve is flat, so the decision waits
   for the enforcement premise.

### 2. `SECURITY.md` — a disclosure channel that survives the roster

**Change**, confined to the *Reporting a vulnerability* section at
`SECURITY.md:29` and touching no other section of the file:

* **Name a channel: GitHub private vulnerability reporting.** The reporter uses
  the repository's *Report a vulnerability* control; the report opens a private
  draft advisory visible to the repository's maintainers.
* **Say who can read it, in one sentence** — access follows the repository's
  own permissions, which is the property that makes this the right choice.
* **Keep the existing content**: the "do not open a public issue for an unfixed
  vulnerability" instruction, the four in-scope examples (a hidden instruction
  in a template, a way to make the scaffold write outside its target, an SSRF /
  content-integrity bypass, anything that could subvert a downstream adopter's
  agents), and the request for a reproducer. All of that is already good.
* **Add a calibration sentence and a pointer.** State plainly that Cairn is a
  single-maintainer project with no on-call rotation and no guaranteed response
  time — a true statement that is more useful to a reporter than silence, and
  that cannot become an overstatement. And point at the file's own *Documented
  residual risks* section at `SECURITY.md:72`, so a reporter can tell a new
  finding from one already consciously accepted.

**Why this channel and not an address.** The requirement is that the channel not
break when the roster grows, and a personal email address is precisely what
does: it is a document edit away from stale on every roster change, it dies with
one person's account or job, and it is scraped. Permission-scoped forge
reporting inverts every one of those properties — adding a maintainer to the
repository grants access, removing them revokes it, and no document is edited
either time. It is also free, needs no infrastructure, and adds no dependency,
which matters for a project whose adopters take zero runtime dependencies.

**What it does not fix**, so the claim is not read wider than it is: this removes
the *document-rot* failure mode, not the single-point-of-failure one. The channel
still depends on one forge and on the account that owns the repository — the same
account residual **RA1** in successor scope 1 identifies as the trust anchor for
release signing, so a forge-account compromise takes both. And it still requires
the reporter to hold an account on that forge. Both are carried as **R3** rather
than argued away.

**The ordering constraint, which is the load-bearing part.** Private
vulnerability reporting is **off by default** and is enabled by the Maintainer
in the repository's own settings. That is a Maintainer action, not agent work,
and it must happen — and be verified live — **before** the prose naming the
channel lands. Documenting a channel that is not yet enabled would replicate
`PROVENANCE.md`'s exact defect (a published control the mechanism does not
provide) inside the very proposal correcting it. The plan carries this as a
sequenced precondition, not as a checklist item.

**On vendor-neutrality**, checked rather than assumed: naming a *forge* is not a
neutrality violation. The neutrality gate's denylist covers AI vendor and model
names plus two project names, and its scan roots at `scripts/quality_gate.py:208`
are `doctrine`, `dimensions`, `bootstrap`, `scripts`, `on-ramp`, `docs`, and
`examples` — repository-root files are outside the scanned set regardless.
Cairn's own profile already carries `forge: github` as a first-class token. The
*doctrine* stays forge-neutral; only Cairn's own `SECURITY.md` names Cairn's own
forge.

### 3. `README.md` — one pointer

Add a short *Contributing* pointer to `README.md` linking `CONTRIBUTING.md` and
`SECURITY.md`. One or two sentences; no content moves. A front door nobody can
find from the front page is not a front door, and `README.md` is currently the
only entry-layer file a first-time visitor reliably reads.

### 4. `dev/.cairn/profile.yml` — one clarifying comment

A comment beside `human_team: solo` at `dev/.cairn/profile.yml:19` recording
that the axis is a staffing descriptor, that it stays `solo`, and that the root
`CONTRIBUTING.md` is project-owned rather than the human-team-gated optional
template. **No value changes**; the resolved axes are unchanged, so no lockfile
regeneration is implied, and the file carries no lockfile hash record.

This is the cheapest possible placement of the disambiguation: exactly where a
future reader — human or agent — would otherwise be misled, which is where the
parent proposal's author *was* misled. It is the one element of this proposal a
reviewer can cut without weakening anything else.

### A question, not a mechanism — contribution-readiness

[IDN5]'s satisfier invited a distinct contribution-readiness switch *"if this
should be a reusable adopter feature."* Building one is out of scope by
construction, and this section deliberately does not design it. But the question
should be asked, because *Residual R1* below shows the conflation is live in the
engine and this scope cannot reach it:

**Cairn's dimension matrix has six axes describing what a project *is*.
`human_team` says how many humans work the repository. "Do we accept outside
contributions?" is a *policy* fact, orthogonal to staffing.** A solo maintainer
can accept contributions — that is exactly Cairn's own situation today — and a
small-multi team can be closed to them. The gate
`human_team in {small-multi, large-multi}` conflates the two, which is why the
parent proposal reached for the wrong lever and why the presence heuristic at
`bootstrap/_scaffold/upgrade.py:1033` reads back a staffing answer from a policy
artifact.

Three dispositions, with their costs, and **no recommendation**:

* **A seventh axis.** Most expressive; most expensive. It changes the dimension
  matrix and every preset, and adopters' existing profiles would need a default.
* **A non-axis profile boolean** (e.g. `accepts_contributions`) that gates the
  optional template instead of `human_team`. Cheaper, and it leaves the six-axis
  matrix intact — but it adds a second kind of thing to the profile schema,
  which is its own doctrine question.
* **Nothing.** Leave `CONTRIBUTING.md` a project-owned file every adopter writes
  themselves, and *narrow* the presence heuristic so it stops inferring a
  staffing axis from a policy artifact. Cheapest; loses the templated starting
  text for adopters who would benefit from it.

Any of the three changes the **dimension matrix or the module gate-table**,
which `dev/proposals/_template.md`'s triage list names as an invariant-kernel
change that opens a proposal regardless of size. It therefore needs its own
go-ahead and its own proposal, and it is raised here only so the Maintainer can
decide whether to queue one.

### Documentation / doctrine surface

* **`CONTRIBUTING.md`** routes to the **entry layer**.
  `docs/DOCUMENTATION_PLAN.md` defines that layer as the root files that live
  there because *"external convention puts them there — a visitor expects
  `README.md`; … the security disclosure convention expects `SECURITY.md`."*
  `CONTRIBUTING.md` is the same class of convention-inherited root file; its
  placement is inherited, not a project choice.
* **`SECURITY.md`** is already named in that same entry-layer list as *"the
  security disclosure surface."* This change makes one section of it do the job
  the layer assigns it.
* **`README.md`** is entry layer; it gains a pointer, not content.
* **No `doctrine/` change. No `AGENTS.md` change. No template change.**
  `templates/optional/CONTRIBUTING.md` keeps its unfilled slot, because the slot
  is per-adopter by design. `bootstrap/fidelity-check.md` — the manifest spec —
  is **not** touched, because it is part of the install contract that
  `AGENTS.md` says to treat as byte-level stable.

### Doctrine-change rate-limit

**Not applicable.** No rule, process, or contract that every contributor follows
changes. `CONTRIBUTING.md` is a new project document that *routes to* existing
rules; the `SECURITY.md` change replaces an unactionable instruction with an
actionable one in the same section, adding no obligation; the `README.md` and
`profile.yml` edits are a pointer and a comment.

The one thing that *would* clear a rate-limit gate — a contribution-readiness
switch — is deliberately posed as a question above and built nowhere.

## Cross-lineage collisions

Seven Theme 3 proposals were opened on 2026-08-03. Two touch files this scope
touches; both are **section-disjoint**, verified by heading line number
`as_of 2026-08-03`:

| Proposal | Shared file | This scope's section | Their section |
|---|---|---|---|
| `scan-coverage` | `SECURITY.md` | *Reporting a vulnerability* (`:29`) | *Release security checklist* (`:59`) |
| `agent-context-scrub` | `SECURITY.md` | *Reporting a vulnerability* (`:29`) | *Documented residual risks* (`:72`) |

Three proposals, three disjoint sections of one file, in landing order that does
not matter. There is **no ordering dependency in either direction** and no
shared claim: this scope asserts nothing about the release gate or the residual
list, and neither of them asserts anything about the disclosure channel.

Also checked and clear: `gate-claims-vs-enforcement` cites `README.md` five
times, but every citation is to `bootstrap/tests/fixtures/skills/README.md` or
`doctrine/README.md` — never the repository-root `README.md`, which is
uncontested across all live proposals.

**Two things the sibling successors offered this scope, both declined — recorded
here so neither is left believing it was taken.** Reconciled against the sibling
drafts on 2026-08-03, not assumed.

* **Scope 2's residual R6** — `dev/.cairn/agent-identities.json` has no
  documented home — names the parent's Part 4 phrase *"name the roster's home"*
  and looks to this scope. **This scope declines it.** That file is the *agent
  and maintainer identity roster read by `lifecycle_planner`*, not a contributor
  list; documenting it belongs with the code that reads it and the adopter
  documentation that describes the planner, neither of which is in this scope's
  `Touches` line. Taking it would also mean a contributor's first document
  explaining an internal classifier's config file, which is the wrong reader.
  Scope 2's R6 has been restated in its **reverted** form (a trivial-class
  documentation commit no later than v0.4.0 release preparation), so the residual
  is owned, not parked here. If the Maintainer prefers it here, it is one
  sentence and this scope will take it — but it is not taken silently.
* **Scope 2's residual R3** cites "a contributor roster" as a non-mechanical
  expiry condition for the review-independence gate. **This scope lands no
  roster** — `CONTRIBUTING.md` is an entry point, not a list of people — and
  scope 2's draft has been corrected to say so. No obligation flows here.

**Gate-freeze check.** The active gate batch freezes files matching
`bootstrap/*.py` (non-recursive), `bootstrap/tests/**/*.py`,
`bootstrap/tests/fixtures/**/*`, `scripts/*.py`, and
`templates/modules/**/*.py`. None of this scope's four files matches any of
those globs, and no file in this scope is covered by the AST attestation. **No
re-anchor is required or implied**, which is a deliberate consequence of the
scoping rather than a lucky one.

## Rationale

* **Which user workflow does it improve?** The first ten minutes of the first
  outside contributor. Today those minutes produce: no front door, a `README.md`
  with no test command, an environment requirement discoverable only two
  documents deep, and a security-report instruction with no mechanism. That is
  the workflow, and every part of it is fixable with prose.
* **What contract does it preserve or clarify?** It clarifies the by-file
  licence split for someone approaching it from outside — restating the
  precedence rule the licence files already carry, adding no term. And it
  **preserves** the `human_team` axis's meaning, which the parent proposal would
  have spent to obtain a side effect.
* **What correctness or transparency does it improve?** `SECURITY.md` currently
  states a control (private reporting to the maintainer) with no mechanism
  behind it. That is the same shape as `PROVENANCE.md` promising a signature the
  verifier never checks — a claim outrunning its enforcement. Closing it in the
  disclosure surface is a small, exact instance of the correction this whole
  lineage is about.
* **Why now?** Three timing-bound reasons. The first external adopter is a
  postdoc, and a postdoc is the likeliest first contributor. The remaining three
  successor scopes are security-lensed and will queue; this one is documentation
  and should not wait behind them — that was the reviewer's explicit argument
  for splitting on gate boundaries. And a disclosure channel is worth most
  strictly *before* the first report, not after.

## Alternatives considered

* **Do nothing.** Defensible while the repository has no outside visitors, and
  indefensible the moment it does. The specific asymmetry: a missing
  `CONTRIBUTING.md` costs a contributor some confusion, while a missing
  disclosure channel can cost a vulnerability report entirely — a researcher who
  cannot find a private channel either drops it or opens a public issue.
* **Flip `human_team` to `small-multi` and let the scaffold install the
  template** (the parent proposal's Part 4). Rejected by [IDN5] and accepted by
  the author: it trades a missing document for false machine-readable project
  state, in a repository whose product is an honest record. Not reopened.
* **Build a contribution-readiness switch now.** Rejected as scope violation and
  as premature mechanism. It changes the dimension matrix or the module gate
  table, so it takes its own proposal; and the right shape of an adopter feature
  is not knowable before Cairn has had a single outside contribution. Raised as
  a question above instead.
* **A personal or institutional email address as the disclosure channel.**
  Rejected: it breaks on exactly the event this scope is preparing for. It also
  needs a document edit on every roster change, which is the failure mode
  `dev/collaboration_agreement.md:15`'s `team-roster` slot already exists to
  manage, and duplicating that state in `SECURITY.md` would create a second
  place for it to go stale.
* **A CLA, or a DCO now.** Argued down at length above. Both are recorded with
  expiry triggers rather than dismissed (*R4*).
* **Fix the presence heuristic at `bootstrap/_scaffold/upgrade.py:1033` in this
  proposal.** Seriously considered and **rejected on gates**. It is a
  `bootstrap/_scaffold/` change, which carries the high-risk engine obligations,
  the Bandit gate, and the mandatory AST re-anchor — the exact gate set whose
  presence in one bundled plan the reviewer used to justify the four-way split.
  Importing it would make the least security-critical scope carry the third
  scope's gates and re-create the bundling failure the split exists to prevent.
  Carried as *R1* with a named trigger instead.
* **Write `CONTRIBUTING.md` fresh, ignoring the template.** Rejected: it would
  leave `templates/optional/CONTRIBUTING.md` with zero dogfooding while Cairn
  continues telling adopters an unfilled slot is a review finding.
* **Add a default pull-request template while in the neighbourhood.** Rejected
  as new mechanism on no evidence; carried as *R6*.

## Evidence / verification plan

Every factual claim above was verified by reading or executing against the live
tree on 2026-08-03. Verification of the *change* is prose-integrity checking
plus one live channel check, because the change is prose plus one repository
setting.

### Author-accounting — invariants, failure modes, edge cases

* **Invariants.**
  * `dev/.cairn/profile.yml`'s `human_team` value is unchanged, and
    `dev/.cairn/cairn-lock.yml`'s `"optional_templates": []` stays empty.
    *Enforced by*: the existing `bootstrap/tests/test_scaffold.py` optional-template
    gate assertions, which would fail if the selection set changed — they do not
    exercise this proposal, they *bound* it. This is the honest characterization:
    the invariant has a pre-existing enforcer, not a new one.
  * `CONTRIBUTING.md` never enters the lockfile. *Enforced by*: the scaffold's
    install mappings, which do not list it at Cairn's axes — the same structural
    guarantee `doctrine/doc-governance.md` describes for `RULES.md`.
  * The licence paragraph restates and never extends the by-file split.
    *Enforced by*: review against the two licence files, not by a test. Stated
    as a review obligation rather than implied to be mechanized.
* **Failure modes.**
  * **Open, intentional**: a stale `CONTRIBUTING.md`. Nothing verifies that its
    stated test command still matches `AGENTS.md`, or that Python 3.13.x is
    still canonical. `check_cairn` checks links and claim-paths, not the content
    of a stated command. Mitigated by the inline sync note, not closed. This is
    *R5*.
  * **Open, intentional**: the `_infer_init_lock_axes` disagreement (*R1*).
  * **Closed**: nothing here can fail at runtime, because nothing here runs.
    There is no new code path, so there is no new failure to fail closed.
* **Edge cases.**
  * *Handled*: `verify_integrity` is unaffected — its loop at
    `bootstrap/verify_integrity.py:62` iterates lockfile records only, so a root
    file absent from the lock is invisible to it and adds no violation.
  * *Handled*: `check_cairn` covers the new file automatically, since it scans
    tracked markdown and a committed root file is tracked.
  * *Named, not handled*: if Cairn's `human_team` axis ever moves to
    `small-multi`, the scaffold would want to install `CONTRIBUTING.md` at a
    path that already holds a project-owned file. The one-time reconciliation is
    named in *R2*; this proposal does not pre-solve a migration for an axis
    change that has not been proposed.
  * *Out of scope, stated*: what happens when two maintainers both hold the
    disclosure channel — the channel handles it (permissions are per-person),
    but the *process* for triaging a report with two maintainers is not designed
    here.
* **Public-path → test mapping.** **N/A** — this change adds no public entry
  point and no code path. Writing a mapping row would be a forward reference to
  a test that should not exist: a pytest test asserting the contents of a prose
  file would pin wording, not behaviour, and Cairn's testing discipline is
  behavioural.
* **Known omissions.** Three, stated rather than discovered:
  1. I did **not** execute the test suite. Running `pytest` writes
     `__pycache__` / `.pytest_cache` into the tree, and this drafting session
     holds no write claim on it. Every suite figure cited above is quoted from a
     dated in-repo record, never re-measured and never asserted as current.
  2. I could **not** verify GitHub's live behaviour for a
     `.github/PULL_REQUEST_TEMPLATE/` **directory**. The filesystem fact is
     verified — the directory holds exactly one template, `foldback.md`, which
     is deployment-specific. My statement that a plain pull request therefore
     opens with an empty body is an **inference from the directory layout**
     (GitHub applies a template *directory*'s entries only on explicit
     selection), not an executed observation. Flagged as *R6* accordingly.
  3. I did **not** assess whether the repository's current settings already
     enable private vulnerability reporting. That is a settings surface I do not
     read and would not change; it is the plan's first sequenced step and the
     Maintainer's action.

### Tests required

**N/A — no pytest test.** This change adds no behaviour. The existing
optional-template gate assertions in `bootstrap/tests/test_scaffold.py` already
bound the invariant that matters (the selection set is unchanged) and are run
unchanged as a regression check, not extended.

Asserting prose content in `bootstrap/tests/` would pin wording rather than
behaviour and would make every future copy-edit a test failure. Named as an
explicit N/A because silent omission is a review finding.

### Examples / smoke checks

* `python scripts/check_cairn.py` — the prose-integrity gate (internal link
  resolution plus claim-path checking) over all four changed files. This is the
  primary check.
* `python scripts/claim_check.py CONTRIBUTING.md` — one file per invocation.
* `python bootstrap/scaffold.py --manifest` — run to show the install set is
  **unchanged**. This is the negative smoke check that distinguishes this
  proposal from its superseded parent: the parent's Part 4 would have *added*
  `CONTRIBUTING.md` to the manifest, and this one must not.
* `python -m pytest bootstrap/tests` under the canonical interpreter
  (Python 3.13.13) — green, with no delta attributable to this change.
* **The live channel check** — after the Maintainer enables private
  vulnerability reporting, confirm the *Report a vulnerability* control is
  actually present on the repository before the prose naming it lands. This is
  the one check that is not a command, and it is the one that keeps this
  proposal from writing a claim its mechanism does not back.

## Residuals and expiry triggers

Per the Decision's second anti-debt condition, reusing the dated-posture pattern
from `gate-reanchor-preflight`: **a residual with a named trigger is a decision;
a residual without one is debt.** Six residuals. Each names whether this change
**creates** it or **leaves it standing**, and each trigger is observable — it
lands in a command's output, a repository event, or the issue tracker — rather
than depending on someone remembering.

**R1 — the presence heuristic will disagree with the axis. (Created, and it is
the sharpest thing in this proposal.)**
`bootstrap/_scaffold/upgrade.py:1033` infers `human_team` as `small-multi` from
the mere presence of a root `CONTRIBUTING.md`, and `solo` otherwise. After this
change Cairn's tree carries that file while its committed profile says `solo`,
so the engine's heuristic and the project's declared axis **disagree**. This is
[IDN5]'s conflation in mirror image: [IDN5] forbade falsifying the axis to get
the file, and this proposal instead takes the file and leaves a heuristic that
would read the axis back wrong. Not fixing it here is a **gate decision**, not a
judgment that it is unimportant — the fix is a `bootstrap/_scaffold/` change
carrying the engine obligations and the mandatory AST re-anchor.
*Bounded*: `_infer_init_lock_axes` is called only from
`_write_init_lock_profile_template`, which runs on a **first**
`upgrade --init-lock` in a tree with **no committed `dev/.cairn/profile.yml`**.
Cairn has one, so the path is unreachable on Cairn's own tree today, and the
comment added in §4 is the human-readable guard.
*Expiry triggers*, any one: (a) Cairn's `dev/.cairn/profile.yml` is removed or
regenerated via `upgrade --init-lock` — observable, because that command writes
the prefilled file and then fails loud by design; (b) Cairn's `human_team` axis
moves off `solo`; (c) the first adopter report of a wrong axis prefill — Cairn
has the `issue-capture` module installed with a `bug` template, so this trigger
has a real inbox.
*Named upgrade path*: make the inference read the manifest's
`optional_templates` block rather than file presence, so it reads a recorded
gate instead of guessing from a filename. That is scope-3-adjacent engine work
and takes its own proposal.

**R2 — Cairn's `CONTRIBUTING.md` receives no template upgrades, and the drift is
silent. (Created.)**
Because the file is project-owned, improvements to
`templates/optional/CONTRIBUTING.md` do not propagate to it, and nothing
detects the divergence: `verify_integrity`'s loop at
`bootstrap/verify_integrity.py:62` iterates lockfile records, and this file has
none.
*Expiry triggers*: (a) `templates/optional/CONTRIBUTING.md` is next edited — the
editing change re-checks Cairn's copy, and this obligation is written into that
template's own header so the trigger is where the editor will be; (b) Cairn's
`human_team` axis moves to `small-multi` or `large-multi`, at which point the
file becomes the scaffold-installed optional template, enters the lockfile, and
the accumulated drift is reconciled once via the normal three-way merge. The
retained `cairn:slot` markers are what make that reconciliation mechanical.

**R3 — the disclosure channel is single-forge and requires an account.
(Created — this is the cost of the recommended channel, and it should be paid
with open eyes.)**
GitHub private vulnerability reporting requires the reporter to hold a GitHub
account and requires that forge to be reachable. Cairn will publish **no**
non-forge fallback, because the available fallbacks are personal addresses,
which is the exact property the channel was chosen to avoid.
*Correlated with a sibling residual, recorded so the two are not read as
independent:* successor scope 1's residual **RA1** anchors release-signing trust
in the maintainer's control of the same forge account. A compromise of that
account therefore reaches both the disclosure channel and one of the two signing
trust channels at once. Neither proposal claims otherwise; scope 1's second
channel (ORCID) is what keeps the signing anchor from being single-provider, and
this channel has no such second.
*Expiry triggers*: (a) the first substantive report arrives **outside** the
channel — a direct message to the Maintainer, or a public issue about an unfixed
vulnerability. Both are observable where the Maintainer already looks, and
either is direct evidence that one channel is insufficient; (b) Cairn acquires a
project-owned domain or an organization-level security alias, at which point
publishing a non-forge address costs nothing and the residual closes for free.

**R4 — no inbound-rights attestation. (Left standing, deliberately.)**
With no CLA and no DCO, Cairn records the *licence grant*
(inbound-equals-outbound, stated in `CONTRIBUTING.md`) but obtains no
**originality warranty** from a contributor — no per-commit assertion that they
wrote what they sent and had the right to send it.
*Expiry triggers*: (a) the repository gains **any** automated pull-request check
— that is the DCO's missing enforcement premise, and adding a `Signed-off-by:`
check alongside it is then a few lines; (b) the first outside contribution is
merged, at which point the inbound-rights record has a real subject and a real
precedent to set. The **CLA** stays rejected under both triggers on the
institutional-friction argument, and reopens only if Cairn's copyright holder
changes from a natural person to an entity.

**R5 — nothing verifies that `CONTRIBUTING.md` stays true. (Created.)**
Its stated interpreter version, dev-dependency command, and test command can
drift from `AGENTS.md` and `bootstrap/DEPENDENCY_BUDGET.md` with no gate
catching it; `check_cairn` verifies that cited *paths* and *links* resolve, not
that a quoted command is still current.
*Expiry triggers*: (a) the canonical interpreter version changes — a
single-line, greppable event in `bootstrap/DEPENDENCY_BUDGET.md` and the gate
manifest; (b) `dev/.cairn/profile.yml`'s `test_command` token changes. On
either, the sync note in `CONTRIBUTING.md` names this file as a required
follow-through. Building a checker for a three-line duplication is
disproportionate today; if a *third* such duplication appears, that is the
recurrence signal for a `doc-drift-prevention` mechanism rather than another
note.

**R6 — there is no default pull-request template. (Left standing.)**
`.github/PULL_REQUEST_TEMPLATE/` is a directory holding exactly one
deployment-specific fold-back template, so an ordinary contributor most likely
opens a pull request with an empty body — an inference from the directory
layout, not an executed observation (see *Known omissions*). Building a general
template now would be new mechanism designed against zero real contributions,
and the template a first contribution teaches you is better than the one you
guess.
*Expiry trigger*: **the first outside pull request.** Observable, dated,
unambiguous, and it arrives with exactly the evidence the template needs.

## Signals the change is wrong

* **The contributor's actual first question is not answered.** If the first
  outside contributor reads `CONTRIBUTING.md` and still has to ask, the slot
  content is wrong. *Recovery*: it is a slot — refill it against the real
  question. This is the cheapest failure in the proposal and the most likely.
* **The disclosure channel goes unused while reports arrive elsewhere.** If
  reports keep landing as direct messages or public issues, the channel is
  wrong for this audience rather than merely new. *Recovery*: that is *R3*'s
  first trigger firing; add a second channel rather than defending the first.
* **The project-owned framing is judged wrong.** If a reviewer shows that a root
  `CONTRIBUTING.md` outside the lockfile is worse than either flipping the axis
  or leaving the file absent — because *R1*'s heuristic disagreement is a
  falsehood in machine-readable state, only relocated rather than avoided — then
  the framing fails and the honest answer is to fix the heuristic first and land
  this scope behind it. **This is the finding I would most expect a reviewer to
  land**, and it is worth stating plainly that the counter-argument is real: the
  parent proposal was told not to falsify the axis, and this proposal creates a
  state where an engine function would infer the axis falsely. My argument that
  it is nonetheless better — the heuristic path is unreachable on this tree, the
  declared value stays true, and the alternative imports a gate set that
  re-creates the bundling failure — is exactly the kind of argument a reviewer
  should be adversarial about.
* **The licence paragraph turns out to add a term.** If a reader concludes from
  `CONTRIBUTING.md` something about licensing not already true from the licence
  files, the restatement failed and became a change to a protected contract.
  *Recovery*: cut the paragraph to a link. The precedence rule is stated well in
  both licence files already.
* **`README.md`'s pointer is read as a promise of responsiveness.** If a
  contributor infers a review SLA the project cannot honour, the single-maintainer
  calibration sentence is not doing its job or is in the wrong file. *Recovery*:
  move the calibration into `CONTRIBUTING.md`'s opening rather than only
  `SECURITY.md`.

## Plan review tier, and why not External

**`required(Internal)`.** The change is prose at the entry layer: no code, no
test surface, no engine, no install contract, no lockfile, no doctrine, no
template, and nothing in the active gate-freeze set or under AST attestation.

**Why not External, stated rather than assumed.** `dev/proposals/_template.md`'s
triage list names the Security-Review triggers as `bootstrap/SAFETY.md`,
`bootstrap/security_check.py`, and the content scanner. Root `SECURITY.md` is
**not** among them, and I am not going to claim a tier the rules do not require
in order to look careful. Over-calling has a real cost here: it queues the least
security-critical of four successors behind an External reviewer, which is the
precise queueing failure the reviewer's split was designed to prevent.

**What replaces the tier is stronger than the tier would have been.** The actual
failure mode for this scope is not a design flaw an independent reader would
catch — it is *publishing a channel that does not work*. A review cannot detect
that; a live check can. So the plan carries a **sequenced precondition**: the
disclosure channel is enabled by the Maintainer and verified present **before**
the prose naming it lands, and the plan may not reorder those steps.

**Escalation condition, offered rather than pre-empted.** If the Internal
reviewer or the Maintainer judges that publishing a security-disclosure channel
is itself a security-surface change — or that *R1*'s heuristic disagreement is a
security-relevant falsehood rather than a documentation residual — the tier
should be raised to `required(External)` and I will not argue the point. The
tier is ratified at Decision; this is a recommendation, not a ruling.
