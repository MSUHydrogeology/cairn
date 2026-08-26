<!-- cairn-internal-ref-allow: doctrine/ reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
# AGENTS.md — Cairn

> **Single living reference for AI agents working on this
> repository.** Read top-to-bottom on first entry; skim or jump on
> later sessions. This repository runs the **Cairn** methodology —
> a human + AI development method built on recorded, reviewed
> deliberation.

<!-- cairn:slot project-overview -->
**Cairn is a methodology, not software** — an Open Science repository
for scientists and research-software teams adopting AI coding agents who
care about rigor, reproducibility, and review discipline. It packages a
human + AI development method around two differentiators: an
**append-only, git-committed deliberation lifecycle** (proposal → review
→ decision, plus plans for non-trivial work), and a **Dual-Review
model** (two-tier review across structural independence — a
fresh-session same-type *Internal* read that helps a change land, and a
different-agent-type-or-human *External* read that makes it prove it
should). Cairn has four jobs: explain the doctrine (and *why* each piece
exists), ship forkable templates, ship a single-agent bootstrap that
installs and customizes the apparatus, and show two worked case studies.

Cairn is for a scientist or small research-software team (one human plus
agents, up to a small group) building scientific code who want recorded,
reviewed deliberation rather than ad-hoc prompting. It is **vendor-
neutral and model-agnostic by construction**: the coordination channel
is git-committed files, so a project can mix or swap AI vendors without
changing the method. **This repository builds Cairn using Cairn** — it
is its own first adopter, which is why this `AGENTS.md` and `dev/` tree
exist.
<!-- cairn:end project-overview -->

## How this project is built

Work on Cairn is **deliberated, reviewed, and
recorded**. A substantive change does not land because its author
is confident; it lands because it went through a proposal, was
reviewed across structural independence, and the reasoning is
committed to the durable record. The coordination space is the
`dev/` tree — a tree of git-committed files, which makes the
method **model-agnostic**: this project can mix or swap AI vendors
(or run a local open-weights model) without changing the
coordination layer.

* [`dev/README.md`](dev/README.md) — the entry point to the `dev/`
  tree.
* [`dev/collaboration_agreement.md`](dev/collaboration_agreement.md)
  — the working norms and decision rights.
* [`dev/agent_collaboration.md`](dev/agent_collaboration.md) — the
  roles, the review loop, and the coordination doctrine in full.

This file (`AGENTS.md`) is the **operational** reference — the
rules an agent must follow to make a correct change. The `dev/`
docs carry the deeper *why*. Which file a given rule belongs in —
and the discipline that keeps this file's operational-safety content
a compact imperative rather than a process manual — is the
**doc-governance** routing rule (`doctrine/doc-governance.md`):
build-the-software and operate-safely rules live here; the
deliberation and decision process lives in
`dev/agent_collaboration.md`; each rule has one canonical home and
the other file only points.

**Where `doctrine/` references resolve.** Throughout this file and the
`dev/` tree, a reference to a `doctrine/<name>.md` file points to **Cairn's
published methodology doctrine** — the repository you adopted from — **not
a file in your own tree**. The bootstrap installs your `AGENTS.md` + `dev/`
tree and the modules you selected, *not* Cairn's `doctrine/` directory; the
doctrine is the shared methodology you consult in the Cairn repository (or
its docs). So such a reference is a citation, never a broken local link.

## The lifecycle

A substantive change — a new abstraction, a cross-cutting
refactor, a contract change, anything worth a second opinion —
goes through a **proposal**:

```
awaiting-review <-> revising -> awaiting-decision
                             -> accepted / rejected / superseded
```

A blocking review moves a proposal to `revising`; the author's Response
and complete current-contract revision return it to `awaiting-review`; a
clearing review moves it to `awaiting-decision`, which is the
Maintainer's. A non-trivial accepted proposal then gets a **plan**:

```
awaiting-plan-review <-> revising-plan -> ready-to-implement
  -> implementing -> awaiting-code-review <-> revising-code
  -> ready-to-archive -> archived
```

Each status names **who holds it next**, which is why the flat
`proposed / open / executing / review` tokens were retired: they named a
phase but not an owner. They remain readable on archived artifacts and
in longitudinal metrics, and are refused on an active one. Two rules are
bright-line:

* **Append-only.** Never edit a prior section of a proposal —
  append a revising one. The record shows what was believed *at
  each point*, not a tidied final state.
* **One commit per lifecycle transition.** Open, review, response,
  and decision each get their own commit; bundling hides who
  changed what.

The full lifecycle, the trivial-vs-non-trivial triage, and the
file-move rules are in
[`dev/proposals/_template.md`](dev/proposals/_template.md) and
[`dev/plans/_template.md`](dev/plans/_template.md).

## Review

Every substantive change is reviewed (see
`dev/agent_collaboration.md`):

* **Internal review** helps a change land — a constructive second
  read. Floor: the same agent in a fresh session.
* **External review** makes a change prove it should land — an
  independent read. Floor: a different agent type, or a human.

Review is asynchronous and commit-mediated: a review is a section
appended to the artifact and committed, not a conversation that
leaves no record.

**A plan review is Internal, fresh-context — always.** External plan
review does not exist as a tier, a requirement, a recommendation slot,
or an escalation target; the External floor lives at the deliberate
lane's **proposal** review, where the design is still movable.
**Code review's floor is unchanged and independent: not the
implementing agent** — a same-type agent in an independent context
clears it. A plan whose surface or triggers call for security
treatment declares `Plan review: required(Internal + Internal Security
Review)`, satisfied only by an appended `## Plan review` pass whose
`**Obligation**: Internal Security Review` line matches it, authored
by a fresh-context same-type session in the Security Review role —
never by an ordinary Internal pass, and never by a record headed
`## Security review (...)`, which the checker does not read as a pass
at all. A high-risk surface named
below still takes its own Security Review; that trigger is untouched
by this routing, and the Maintainer may still choose to ask any
additional reader for any artifact — a choice is not a tier. Contract
and rationale: `doctrine/dual-review.md` > "Plan review is Internal,
always"; process framing in `dev/agent_collaboration.md`.

**Reviews are attributed and self-committed.** No agent writes or
commits a review attributed to another agent — the named reviewer
commits their own findings, or the Maintainer does. The attribution
*is* the record's integrity: a review you did not write is not yours to
sign, and a structurally-independent read is only independent if its
author is its committer.

**Comprehension is a precondition of the Decision, not a courtesy.** You cannot
review what you cannot penetrate, so an opaque change quietly turns "review and
decide" into "approve". Lead plain and keep the precision beneath it; define a
specialist term the first time it carries weight; and treat *"I don't
understand this yet"* as a **mandatory pause** — a decision surface the
Maintainer cannot follow is not decidable. This binds the agent, who is
typically the stronger party on the software, not the reader. **The same floor
reaches forward in time** — see the durable-artifact rules under
*Project-specific conventions*. Rationale and
grounding: `doctrine/rationale.md` > the comprehension floor.

## Session routines

* **Session start** — at a cold start, or after a context-loss
  event, run a short orientation pass: if the project keeps a
  `RULES.md` (tracked, project-owned agent rules — Cairn never
  templates it; see `doctrine/doc-governance.md`), read it *first*;
  then re-anchor on the `dev/` tree, read the commit log since the
  last handoff, note in-flight proposals, and confirm your role
  before substantive work.

  For the in-flight threads, **start from the board, not from the
  artifacts**:

  ```
  python tools/lifecycle_planner.py board --compact
  ```

  One row per active artifact — kind, artifact, status, owner role,
  active work-intent, review obligation, evidence, what blocks it, and
  row validity. **Run the board, choose the row you need, then read that
  artifact and the evidence it cites** — not every active record. The
  view is derived and says so; the artifact is authoritative, and it
  mutates nothing.
* **Goodnight** — at the end of a session, leave a clean handoff:
  a status summary, a per-agent reflection, and (for the
  designated owner) a scrub of the roadmap boards. The handoff commit is
  part of the routine and its owner lands it; **pushing is never implied
  by the routine** and waits on explicit maintainer approval.

## Roles

Work is organized by **roles**, not people — a role is a frame.
The **Human Maintainer** holds final Decision authority and is the
one role that is not interchangeable. Other roles (Strategy,
Implementation, the reviewer tiers, and any the dimensional
profile adds) are frames any capable agent fills; name your role
before substantive work, and if it is not explicit, ask. The
roster is in `dev/agent_collaboration.md`.

## Git and commit workflow

* **Implementing an accepted plan, commit your own work.** An agent executing a
  reviewed, accepted plan commits as it goes — code, tests, templates, docs and
  deliberation artifacts alike. There is **no per-commit approval gate**.
  Approval attaches to exactly four things:
  * **Pushing.** Always, without exception. The plan authorized the change; it
    did not authorize publishing it.
  * **A Decision on a proposal** (accept / reject / supersede) — the
    Maintainer's to make, and theirs to land, bounded by the scribing
    guard-rail below.
  * **A deviation from the approved plan** — new scope, a struck chunk revived,
    a contract the review never saw, an acceptance criterion you cannot meet,
    **or accepted scope removed**. *Deviating* is what needs asking; committing
    is not.

    **Removal counts as a deviation, in both directions.** Accepted scope is a
    **floor**: sequencing may move work between chunks, but dropping an outcome
    the accepted artifact committed to is a deviation exactly as adding one is.
    Judge it against the baseline's own commitments — if every accepted outcome
    is still delivered, a lighter mechanism owes nothing; otherwise declare the
    `Scope delta`, group the remainder into one record, and get the
    Maintainer's explicit allowance. **A reviewer cannot create that authority
    by calling the remainder "out of scope."** Narrowing is the path of least
    resistance in review — it costs the reviewer nothing, reads as prudence,
    and can never be shown wrong, because the wider version is never built.
  * **A plan's own explicit fence.** A chunk marked MAINTAINER-GATED or
    MAINTAINER-ONLY does not execute without the authorization it names,
    whatever this rule says. Fences are the mechanism by which a plan places
    approval where it is actually load-bearing.

  Report what changed when you report, and keep the commit body a faithful
  snapshot. **Never a bare `git commit`** — but that rule (below) protects
  against the *shared index*, not against missing approval; the two are
  unrelated and only one of them is a gate.

  **Why this is stated positively, and why it must not be re-tightened by
  reflex.** The rule this replaces — *never commit without explicit approval* —
  **predates Cairn** and was the reaction that led to building it: unreviewed
  agent commits accumulating faster than a human could read them. That hazard is
  real, and it is now answered by the apparatus itself — a proposal, a review
  across structural independence, an accepted plan with per-chunk acceptance
  criteria, and fences at the points that genuinely need a human. A blanket
  per-commit gate on top of all that is not additional safety; it is the earlier,
  cruder instrument left running after its replacement was built, and it has cost
  real work — an agent has stranded verified files uncommitted rather than land
  them. If a future incident argues for tightening, tighten *the plan's fences*
  or the review tier, which is where approval binds to something specific.
* **Scribing a Decision — the guard-rail.** The Maintainer's Decision
  (accept / reject / supersede) is theirs to land; an
  explicitly-instructed agent may *scribe and commit* it, bounded by
  three rules:
  * **Attribution — quote the authorization verbatim.** Quote the
    Maintainer's authorizing phrase(s) **verbatim and visually
    isolated** in both the `## Decision` block and the commit body. Do
    **not** paraphrase the authorization itself — paraphrase admits
    semantic drift, condition-softening, or a hallucinated approval.
    Surrounding explanatory prose is allowed, but clearly separated
    from the quoted words, so a reader can tell exactly what was
    authorized.
  * **Unambiguous instruction, or confirm.** Act only on an instruction
    unambiguous on *both* the disposition and the commit; if either is
    unclear, confirm with the Maintainer before scribing.
  * **Decision-only commit.** Flip the status and append the Decision
    section, and nothing else — no implementation, plan-open, archive,
    or roadmap work rides in a scribed Decision commit.

  Absent an explicit, unambiguous (or confirmed) instruction, no agent
  lands a Decision commit.
* **Commit with explicit paths** — `git commit <path> [<path> ...]`,
  naming exactly the files the commit should contain. **Never a bare
  `git commit`**: it commits the *entire* staged index, so anything
  another agent has staged rides into your commit under your message
  and author. A path-scoped commit makes that collision *structurally
  impossible*; the windowless habit below removes the staged window the
  old backstops only narrowed.
  * **Prefer the windowless commit** — for *tracked* files, `git commit
    <paths>` stages *and* commits atomically: **no separate `git add`**,
    so no staged window is ever exposed. **Verify via the working tree**
    (`git status --short`, `git diff <paths>`) as its own step —
    index-independent, and it does **not** show other agents' staged
    work; do **not** verify with `git diff --cached`, which both
    *manufactures* the window (it needs a prior `git add`) and reads back
    *everyone's* staged index.
  * **New / untracked files** — `git add <paths> && git commit <paths>`
    in one invocation. If the chain aborts on a pre-commit / intent
    check, the files are left staged — immediately `git restore --staged
    <paths>` so a failed commit leaves no residue.
  * **A `git mv` rename needs *both* sides named** in a path-scoped
    commit — naming only the destination commits the "add" and leaves
    the source-side deletion unstaged, so HEAD carries the file at both
    paths until a fixup. Name both source and destination, and verify via
    `git status --short` (the `R  source -> destination` line), not
    `git diff --cached`.
  * **Bright line** — never leave a `git add` / `git mv` sitting exposed
    across tool calls, verification, or other work.
* **Untracked lifecycle artifacts — commit atomically.** If you write a
  lifecycle-opening artifact (plan, proposal, strategy doc) meaning to ship it,
  commit it the *same turn* — write + `git mv` + `git commit` together; never
  leave it untracked for another agent to inherit (the written-but-uncommitted
  state is the failure surface). If you can't commit this turn, don't write it
  yet (draft in chat or the harness scratch surface). Cold-start orientation
  checks `dev/proposals/`, `dev/plans/`, `dev/strategy/` for untracked drafts:
  commit one your own intent claim covers, leave one another agent's claim
  covers, surface an unclaimed one to the maintainer. This is the third
  commit-discipline hazard alongside the staged-index discipline
  (`doctrine/coordination.md`); recurrences are tracked via the
  `incident-trackers` module.
* **Shared communication files** — the roadmap boards, the
  changelog, and (when the `progressive-onboarding` mechanism is
  installed) its activation log — are edited
  only at defined serialization points (a lifecycle archive, the
  goodnight routine, explicit instruction).  Refer to proposals
  and plans by filename stem, not path link.
* **Verification boundaries.** Verification has three jobs; do not pay for the
  same broad run at every one (full doctrine: `doctrine/plans.md` and
  `doctrine/dual-review.md`).
  * **A — Iteration (scoped).** During implementation, run the tests and public-
    path probes mapped by the reviewed plan, plus standing gates for every
    touched surface. If a substantive code surface has no reviewed mapping, or
    its effects cannot be bounded confidently, run the full suite.
  * **B — Integration (stable evidence).** After the final implementation commit
    and before code review, run against a clean, unchanged commit under the
    **canonical interpreter (Python 3.13.x)**. Cairn's ordinary pair is
    `python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0` followed
    by `python scripts/quality_gate.py --sub neutrality --sub redundancy`.
    Boundary B's canonical pair now requires `CAIRN_FULL_SUITE=1`; verification
    records written before this guard cite the bare form and are accurate for
    the runs they describe.
    Run the **full suite unless the plan's reviewed mapping bounds the change's
    effects confidently**, in which case run that mapping plus every standing
    gate for every touched surface — the same test and the same fail-closed
    direction as Boundary A. **Bounded mode refuses**, and the full suite runs,
    whenever the change touches a **contract surface** (the install contract,
    the fidelity or gate manifest, the lockfile schema, the published
    `scaffold.py --manifest`) or a **trust-ceremony surface** (any high-risk
    surface named below, or work under a release or security ceremony).
    **Uncertainty resolves to `full`** — the fence is a refusal rule, not a
    checklist to argue past. Record `**Boundary B mode**: full | bounded`; on
    `bounded`, name the touched surfaces, the mapping and gates run, why the
    effects are bounded, and the explicit absence of any contract or
    trust-ceremony surface.

    **An already-open plan keeps the verification contract written in it.**
    Bounded mode becomes available to it only through that plan's own explicit,
    append-only revision under the deviation rule above. A plan opened after
    this rule landed may use bounded mode where its reviewed mapping supports
    it. Editing this file acts immediately; editing the plan templates acts
    prospectively, so without this sentence an in-flight plan would get two
    answers.
    Append the tested SHA/range, interpreter, clean pre/post state, commands,
    outcomes, timing, non-pass disposition, and known omissions to the plan as
    `## Implementation verification -- <agent> -- YYYY-MM-DD`.
  * **C — Falsification (independent).** The code reviewer verifies that record against
    the reviewed range, then runs independent targeted falsification; copying
    Boundary B's broad command is not a falsification ledger. On a bounded record the
    reviewer records `**Bounding**: ACCEPTED | FULL RUN REQUIRED` after
    challenging at least one named surface, mapped test, or stated omission —
    never "the field is present". `FULL RUN REQUIRED` **invalidates** the
    bounded record, which lands it on trigger 1 below; it adds no seventh
    trigger. Missing or stale
    evidence, unexplained non-pass outcomes, newly discovered coupling, changed
    implementation/test/executable-template/fixture bytes, a stronger trust-
    ceremony rule, or concrete doubt requires a fresh full run.
  Prose-only work runs its applicable claim, link, snippet, and neutrality
  gates unless its plan maps it to pytest. Release verification remains a
  separate strict ceremony. Name the interpreter alongside every suite figure;
  see `bootstrap/DEPENDENCY_BUDGET.md` > "The canonical interpreter".
* **Keep commit bodies concise.** The body is a *snapshot* — what
  shipped and how it was verified — not a restatement of the proposal,
  plan, or changelog (those are the durable audit trail). Target 15–30
  lines for a non-trivial implementing commit (soft cap ~50; a trivial
  fix is often just the subject + a one-line body): a one- or
  two-sentence opener cross-referencing the source proposal / plan, a
  short bullet list of the substantive changes by file or surface, and
  a one-line verification snapshot with concrete numbers. Optimize for
  `git log --oneline` skimmability.

## Verifying claims

<!-- cairn:slot claim-check -->
**Verify before asserting.** Before committing a proposal, plan, or
doc, run the claim checker (`python scripts/claim_check.py`) over it: it
hard-flags broken repo paths and out-of-bounds line citations. A hard
flag is resolved before commit; a deliberate forward-reference is
*marked*, not left to assert, and a `claim-check-allow` directive
(`<!-- claim-check-allow: <glob>, <glob> -->`) is the file-scoped path
equivalent. Numeric claims follow the three-kind precision / `as_of`
discipline — approximate a decision-irrelevant count, date a snapshot,
register a live invariant — rather than a write-time count flag (retired
2026-06-05).

The checker is a **discipline aid, not a gate**: the verify-before-
asserting habit is the doctrine (see `dev/modules/claim-check.md` for
the A–E typology and the costlier runtime-behavior class no scanner
reaches); the tool only shifts its cheap, mechanical part left, ahead
of review. Cairn runs this exact checker on itself —
`scripts/check_cairn.py` imports the same claim-path checker and adds
link-checking on top.
<!-- cairn:end claim-check -->

**Name the trigger, check what it checks, and open it.** Any document that
describes a check says what runs it — a command a person runs, a test in
`bootstrap/tests`, a git hook, or a CI job. Cairn has no CI; do not write
"in CI" for something no CI runs. A check whose only trigger is a human
remembering is described that way. And when a named trigger exists, the
document states what that trigger actually verifies: a tool that returns
success without testing the claimed property is a worse defect than no
tool, because it is silent. **A named trigger is checked by opening it and
confirming the procedure is there — a path that resolves is not a trigger
that governs — and the check does not stop at the first named artifact: it
recurses until it reaches a human or a machine.**

**Confirm the instrument before trusting an absence.** A grep that returns
nothing, a count that matches, a failure list that comes back clean — each is
evidence only if the pattern *could* have matched, so before acting on a
negative result, run the same measurement against a case known to be present.
This is the silent-tool defect one level down, on the ad-hoc measurements
nobody writes into a document: a count kept without its failure identities, a
regex anchored to a prefix the target lines never carry, a liveness grep scoped
to the doc tree but not the code. Each returns clean, confident, and wrong.

## Documentation discipline

<!-- cairn:slot documentation-discipline -->
Cairn uses a **placement-decision procedure** for documentation and
doctrine: see [`docs/DOCUMENTATION_PLAN.md`](docs/DOCUMENTATION_PLAN.md)
for the four-layer vision (entry / governing / deliberation /
descriptive), the routing rules, and the `AGENTS.md` ↔
`agent_collaboration.md` boundary doctrine. When adding new
documentation or doctrine, identify what the content is *doing*
(prescription / deliberation / description) and route by layer.

That `docs/DOCUMENTATION_PLAN.md` is Cairn's own self-hosted instance of
the `documentation-plan` module — the same procedure Cairn ships its
adopters, dogfooded on Cairn's own tree.
<!-- cairn:end documentation-discipline -->

## Project-specific conventions

**Durable artifacts stand without the deliberation that produced them.**
A test name, a comment, a docstring outlives the plan chunk and the review
finding that prompted it. The next reader has no proposal open and no reviewer
to ask, so a coordinate — a finding id, a chunk letter, a plan row — is a
pointer into a conversation that has ended. It reads as information and carries
none. Two consequences, both at authoring time:

* **Name a test for the property it pins, not for what produced it.**
  `TestP2AmendmentBScopeReduction` tells the next reader nothing they can act
  on -- P2 is a plan chunk and Amendment B a review finding, both long
  archived. `TestScopeReductionNeedsMaintainerAllowance` tells them what breaks
  if it fails. Put the *reason* in the docstring — why the obligation exists, what
  goes wrong without it — and no coordinate:

  ```python
  class TestScopeReductionNeedsMaintainerAllowance:
      """Accepted scope is a floor, so dropping an outcome takes an explicit
      allowance. Without this, narrowing passes as prudence: it costs the
      reviewer nothing and can never be shown wrong, because the wider
      version is never built."""
  ```

* **Comments and docstrings explain the code, not the process.** State the
  reason the code is the way it is; do not cite the finding that asked for it.
  `# CR3: use a set here` decays the moment CR3 archives; `# set, not list --
  membership is checked once per candidate and the candidate list is large`
  still works in five years. The bar is not *"is the reasoning recorded somewhere"* but **"can the
  next reader act on this without the record?"** — usually one sentence, and
  sometimes none. Writing the reason in is not licence to narrate: restating
  what the code already says is waste, not comprehension.

Grounding: `doctrine/rationale.md`, Anchor 16 (the comprehension floor and its
temporal half), fenced by Anchor 17.

<!-- cairn:slot project-conventions -->
**Naming.** UPPERCASE for landmark files (`README.md`, `AGENTS.md`,
`BOOTSTRAP.md`, `CHANGELOG.md`, `SECURITY.md`, `PLANNING.md`,
`NEXT_SESSION.md`); lowercase-kebab for content (doctrine and module
files — `dual-review.md`, `doc-governance.md`). Proposal stems are
`<YYYY-MM-DD>-<author>-<slug>.md`; plan stems are `<slug>.md`.

**Development environment & dependency budget.** Everything Cairn ships
an adopter — the scaffold engine, `scripts/`, the reference checkers
(`claim_check.py`, `link_check.py`, `content_scan.py`) — is **standard-
library-only**: adopters take on **zero runtime dependencies**. Dev/test
tooling is dev-only and never in the adopter path (`vermin` for the
Python-floor check; `pytest` for the suite). See
`bootstrap/DEPENDENCY_BUDGET.md` and `doctrine/runtime-contract.md`
before adding any import. Run the suite with `CAIRN_FULL_SUITE=1 python -m
pytest bootstrap/tests` — the bare form is refused by the broad-run guard in
`bootstrap/tests/conftest.py`; see *Verification boundaries* above.

**A fresh clone has no gate anchor, and the gate will refuse.** `git
clone` fetches `refs/heads/*` and `refs/tags/*`; the differential-oracle
gate's trust root lives at `refs/cairn/gate-anchor`, which is in neither.
So a clone that looks complete has nothing for the gate to verify
against, and it stops with `[REFUSE ] ref does not resolve to a commit:
'refs/cairn/gate-anchor'`. Fetch it explicitly:

```
git fetch origin '+refs/cairn/gate-anchor:refs/cairn/gate-anchor'
```

Refusing is correct — a missing trust root must never read as a pass —
so the hazard here is **human**: the refusal arrives during setup, looks
like a configuration annoyance, and invites skipping the gate or
building the habit of routing around a refusal. Fetch the ref instead.
Receiving it proves availability, not authenticity; what makes the
anchor trustworthy is the signature on the commit it names, checked
against the anchored roster.

**High-risk surfaces (Security-Review + proposal triggers).**
* **The scaffold / merge engine** (`bootstrap/scaffold.py` →
  `bootstrap/_scaffold/`) parses untrusted module and profile files,
  does path handling and YAML loading, and writes into a target tree —
  guarded by a symlink/containment check and a Bandit gate over the
  whole engine package.
* **Vendor-neutrality.** Doctrine and templates must name no AI
  model/vendor (`scripts/quality_gate.py --sub neutrality`); names live
  only in the deliberation record or behind a `vendor-ok` marker.
* **The install contract** — the fidelity manifest, the gate manifest,
  the lockfile schema, and the published `scaffold.py --manifest` — is
  what adopters depend on; treat it as byte-level stable.
* **The by-file license split** — code is MIT wherever it lives; prose
  and document templates are CC BY 4.0; the brand mark alone is CC
  BY-ND. Keep the three families from overlapping.
* **The local interpreter binding** — `dev/.cairn/local-env.json`, its
  reader `_resolve_interpreter` in `templates/skills/_lib/session.py`
  (self-hosted at `tools/session.py`, kept byte-identical), and every
  call site that executes the path it returns. The same module owns
  `encode_display`, the single terminal encoder — there is no second
  escape table in this tree, because a fallback engages exactly when
  something is already wrong. This is an
  untracked, gitignored, lockfile-uncovered **executable trust root**,
  and the reader is a strict *shape* validator, not an authenticator: it
  checks absoluteness, schema, symlink-freedom and the executable bit,
  but neither Python identity nor provenance. Changes to its schema,
  validation order, fallback disposition, warning visibility, or
  subprocess use take a Security Review.
* **The portable-sweep executable trust root** — `run_portable_security_sweeps.py`
  (shipped at `templates/modules/team-gated/`, self-hosted at `scripts/`, kept
  byte-identical), its `resolve_executable` / `revalidate` pair, and
  `portable_security_policy.json`. Unlike the interpreter binding above, the
  authority here is **`PATH` resolution**: the runner locates a host `gitleaks`
  and executes it, and Gitleaks invokes `git` transitively — two host trust
  roots the scaffold neither installs nor ships. Resolution digests the binary
  and `revalidate` re-checks that digest **immediately before every
  invocation**, so the resolve→execute gap is measured rather than assumed; a
  repository's own `.git/config`, refs, shallow boundary and remote metadata are
  treated as **candidate-controlled input**. Absence is `INCOMPLETE` (exit 5),
  loudly, and never clean; the adapter has **no egress path**. Changes to
  executable resolution, the revalidation points, the policy schema, the child
  environment (`child_env`), the exit precedence, or the admitted version set
  take a Security Review. Fuller treatment in `bootstrap/SAFETY.md`.

**Operational pitfalls.**
* **Self-host `dev/` citation gotcha.** `scripts/check_cairn.py`'s
  claim-path checker resolves `dev/`-prefixed citations now that Cairn hosts a
  real `dev/` tree; doctrine/templates/CHANGELOG cite adopter-tree and
  historical `dev/` paths that don't resolve. Handling is tracked in the
  first proposal under `dev/proposals/`.
* **AST attestation baseline.** `bootstrap/tests/test_ast_attest.py`
  pins the engine package against a committed baseline; after any
  `bootstrap/_scaffold/` change it must be re-anchored (it does not
  auto-update). **Not** via `bootstrap/REANCHOR_RUNBOOK.md` — that
  runbook governs the differential-oracle *gate* anchor and says nothing
  about this baseline. Self-service repair reaches only the four symbols
  in `_ast_attest._UPDATE_ALLOWLIST`; anything else is a **Maintainer-run,
  dry-run-verified direct correction that an implementing agent does not
  perform** (precedent: `c3d5bd9`). The procedure is
  [`bootstrap/AST_BASELINE_RUNBOOK.md`](bootstrap/AST_BASELINE_RUNBOOK.md) —
  still derive the expected CHANGED set against the committed baseline
  rather than carrying a figure forward, including from that runbook.
* **Commit hygiene.** Always `git commit <paths>` (never a bare
  `git commit` — the index is shared); see *Git and commit workflow*
  above.
* **Doctrine changes clear the rate-limit gate** (`doctrine/rationale.md`
  > "How the doctrine evolves under evidence") — a single incident does
  not justify a doctrine change unless it is the high-risk case.
<!-- cairn:end project-conventions -->

## Vendor addendum

`AGENTS.md` is vendor-neutral — it names no specific AI agent tool.
Doctrine specific to one agent tool (a harness path, a
session-model habit) goes in that tool's own file, which opens by
importing this one (`@AGENTS.md`), so the shared content stays
single-sourced. Cairn ships the thin wrapper as `VENDOR.md`; the
adopter renames it to their tool's auto-loaded file (`CLAUDE.md`,
`GEMINI.md`, …).

**Drift guard.** The wrapper carries *only* harness-specific habits —
this tool's session/context model, its scratch directory, its
command quirks. Everything an agent of a *different* tool would also
need — the required reading, the session routines, the CLI, the
conventions, the development environment, the test command, the git
rules — stays canonical **here**, and the wrapper points at it. A
wrapper that duplicates this content has drifted into a fat fourth
doc; fold it back and leave only the pointer. (`VENDOR.md` carries the
same guard inline; `bootstrap/fidelity-check.md` notes it as a check.)
