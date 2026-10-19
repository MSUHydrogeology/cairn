# AGENTS.md — Cairn

> **The operational reference for AI agents working on this repository.**
> Read it top-to-bottom on first entry; skim on later sessions. The deeper
> *why* lives in [`dev/agent_collaboration.md`](dev/agent_collaboration.md)
> and the `dev/` tree; this file carries the rules you need to make a correct
> change and to operate safely.

**Cairn is a methodology, not software** — an Open Science repository for
scientists and research-software teams adopting AI coding agents who care about
rigor, reproducibility, and review discipline. It packages a human + AI
development method around two differentiators: an **append-only, git-committed
deliberation lifecycle** (proposal → review → decision, plus plans for
non-trivial work), and a **Dual-Review model**: one review stance at every stage.
It is **vendor-neutral and model-agnostic by construction** — the coordination
channel is git-committed files, so a project can mix or swap AI vendors without
changing the method. **This repository builds Cairn using Cairn.**

**Where `doctrine/` references resolve.** A reference to `doctrine/<name>.md`
points to Cairn's published methodology doctrine — the repository you adopted
from — **not** a file in your own tree. Such a reference is a citation, never a
broken local link.

## The lifecycle

```
awaiting-review <-> revising -> awaiting-decision
                             -> accepted / rejected / superseded
```

A review moves a proposal to `revising`; **the author's Response and revision
carry it to `awaiting-decision`**, which is the Maintainer's. There is no
clearing round — no review is run merely to move a status — except a Security
Review, which clears the obligation it was raised against. A second round
exists only for material the first could not have read: a proposal revision
that **widened scope**, a code revision that **introduced new defects**, or a
Security Review still open. **Plan review never has a second round.** A
non-trivial accepted proposal then gets a plan:

```
awaiting-plan-review -> revising-plan -> ready-to-implement
  -> implementing -> awaiting-code-review <-> revising-code
  -> ready-to-archive -> archived
```

Each status names **who holds it next**. Two rules are bright-line:

* **Append-only.** Never edit a prior section of a proposal — append a revising
  one. The record shows what was believed *at each point*, not a tidied final
  state. (A plan is the exception, and says so in its own template: its
  operative cells revise in place until implementation begins.)
* **One commit per lifecycle transition.** Open, review, response, and decision
  each get their own commit; bundling hides who changed what.

Details are in the two `_template.md` files.

## Review

**One stance at every stage.** A review is by a fresh reviewer who did not
write the work, on the work's side: it makes the work better by questioning
its foundations, and it answers in writing. No agent picks a kind of review.
The stage sets three questions:

| Stage | Should it happen as framed? (code: does it do what it claims?) | Best alternative | What would show it wrong |
|---|---|---|---|
| Proposal | Should this exist as framed? Is there a better design, doing nothing included? | The strongest, doing nothing included | What would make the author withdraw |
| Plan | The Decision settled the premise. Does the plan deliver it? | A simpler path to the same outcomes | The result showing it cannot deliver |
| Code | Does it really do what it claims? Try to break it, in order to fix it. | A simpler or safer build, if any | The input or run that breaks it, and what was tried |

Each pass opens with a **Foundations** block of three lines, one answer per
question, each ending in the file, test, line or command that backs it. For
code review, Answer 3 points at the falsification ledger (the record of what
the reviewer tried to break, and what happened) rather than restating it.
**Improve means recommend**: the reviewer proposes the better version
("don't do this" and "do it differently" count) and the author decides. **There
is no quota of findings.** "No defects found" is allowed only with the three
answers evidenced and the gaps named.

**Every review shows its evidence.** The three answers a review owes rest on
the nine standing lenses in `dev/agent_collaboration.md` > "The review sweep".
A lens a review cites names the file, test, line or command that backs it (a
bare "checked" is an incomplete review), and the coverage line that ends the
review says what the pass did not cover. A reviewer who recommends narrowing
the work states what is lost and why the narrower change still reaches the
cause; only the Maintainer concedes a loss.

**More distance is the Maintainer's call, and only theirs.**

* **What it is.** An *External read* is a review the Maintainer asked for on one
  named artifact that exists now, in chat or inside a Decision, outside the usual
  procedure. A call that covers artifacts not yet written is a standing floor (a
  rule that applies without being asked), and a standing floor returns only by
  proposal. A roster the Maintainer sets in `dev/collaboration_agreement.md`
  (which agent types work the tree) is the team's shape, not a call: it adds no
  read and upgrades none. Distance is information, not a rule: a different agent
  type has different failure modes and a person has different knowledge. The
  staffing reviewer follows the Maintainer's brief, answers the same three
  questions from that distance, and says so.
* **How it is recorded.** The pass carries `**Called by**: Maintainer -- Decision
  at <commit>` (or `-- chat, <date>`, with `, relayed by <who>` where it was
  relayed), followed by the Maintainer's words, verbatim and set apart. The same
  words go in the commit message, as for a scribed Decision. `**Tier**: External`
  is valid only with that line, and a pass headed External without it is read as
  the usual review.
* **What an agent never does.** Declare External as a required review in a
  header, say a change needs one, recommend more distance, head a pass External
  on its own, or start one without those words. It may name a risk and a gap in
  its coverage line.
* **What a called read never does to the other reviews.** It adds to the usual
  review and replaces nothing. Its brief may add focus; it removes no owed
  answer, and it discharges no Security Review by its distance or its brief (a
  pass clears a Security Review only by being one). Any other authority in the
  quoted words, such as a waiver or a change of scope, takes effect only where
  Maintainer authorizations already live, a Decision block or a plan's fence,
  and never from a `Called by` line. Nothing checks the quote mechanically, in
  the pass or in the commit message: the next reviewer and the Maintainer at the
  Decision are the check.

**A reviewer reasons through what is proposed; they are not a second
implementer.** Verification belongs to the implementation and its recorded
evidence, not to every reader re-running it.

Review is asynchronous and commit-mediated: a review is a section appended to
the artifact and committed, not a conversation that leaves no record.

**A review reads a commit, never a shared working tree.** The author commits
what is to be reviewed before handing it over (locally; committing is not
pushing), and the review names that commit. In a working tree it shares with
an author, a reviewer makes one write: its own review record, appended to the
artifact or created as its own review file (plus the artifact's Status line,
where the review moves it), claimed first, and committed by explicit path.
Nothing else: no other edits, and no `restore`, `checkout`, `stash`, `reset`
or `clean`. Anything else that writes, such as a mutation or a scratch
install, runs in a separate copy of the reviewed commit, in a fresh, empty
folder every time: a detached `git worktree` (a second checkout of the same
repository) by default, and a `git archive` extraction (plain files, no
repository) only for checks that just read files. A figure is evidence only if
it was measured on that commit's bytes.

**A plan review is fresh-context — always.** Code review's job is falsification,
and its floor is **not the implementing agent**. It never reopens the Decision
(what to build is settled; how it was built, and what breaks it, is the
question). A clean code review shows a falsification ledger.

**A high-risk surface takes a Security Review.** `usual + Security Review` in a
header means two passes: the usual pass and a Security Review pass that names its
own obligation. The usual pass never clears the second. A plan whose surface
calls for security treatment declares `Plan review: required(Internal + Internal
Security Review)`. Only an appended `## Plan review` pass whose `**Obligation**`
line matches clears it, never an ordinary Internal pass. No tool reads that line:
the next reviewer, the code reviewer and the Maintainer check it.
Here, `Internal` means the ordinary plan review.

**Reviews are attributed and self-committed.** No agent writes or commits a
review attributed to another. The attribution *is* the record's integrity: a
review you did not write is not yours to sign, and a structurally-independent
read is only independent if its author is its committer.

**Comprehension is a precondition of the Decision, not a courtesy.** You cannot
review what you cannot penetrate, so an opaque change quietly turns "review and
decide" into "approve". Lead plain and keep the precision beneath it; define a
specialist term the first time it carries weight; and treat *"I don't understand
this yet"* as a **mandatory pause**. This binds the agent, who is typically the
stronger party on the software, not the reader. The floor itself, and why it
reaches forward in time to durable artifacts, is stated in
`doctrine/rationale.md` — pointed at rather than restated, so there is one
place it can change.

## Session routines

* **Session start** — at a cold start or after a context-loss event, orient
  before substantive work. If the project keeps a `RULES.md`, read it *first*;
  then re-anchor on the `dev/` tree, read the commit log since the last handoff,
  and confirm your role. `python tools/session.py session-start` gathers the
  mechanical half — commits since the last handoff, working-tree state, the
  in-flight proposals and plans, and the resolved interpreter. **Read the
  artifacts it names and the evidence they cite, not every active record.**
* **Goodnight** — leave a clean handoff: a status summary, a per-agent
  reflection, and (for the designated owner) a roadmap scrub. The handoff commit
  is part of the routine; **pushing is never implied by it** and waits on
  explicit Maintainer approval.

## Roles

Work is organized by **roles**, not people. The **Human Maintainer** holds final
Decision authority and is the one role that is not interchangeable. Other roles
(Strategy, Implementation, the Reviewer, Security Review) are frames any
capable agent fills; name your role before substantive work, and if it is not
explicit, ask. The roster is in `dev/agent_collaboration.md`.

## Git and commit workflow

* **Implementing an accepted plan, commit your own work.** There is **no
  per-commit approval gate**. Approval attaches to exactly four things:
  * **Pushing.** Always, without exception. The plan authorized the change; it
    did not authorize publishing it.
  * **A Decision on a proposal** — the Maintainer's to make, bounded by the
    scribing guard-rail below.
  * **A deviation from the approved plan** — new scope, a struck chunk revived,
    a contract the review never saw, an acceptance criterion you cannot meet,
    **or accepted scope removed**.

    **Removal counts as a deviation, in both directions.** Accepted scope is a
    **floor**: sequencing may move work between chunks, but dropping an outcome
    the accepted artifact committed to is a deviation exactly as adding one is.
    If every accepted outcome is still delivered, a lighter mechanism owes
    nothing; otherwise declare the `Scope delta`, group the remainder into one
    record, and get the Maintainer's explicit allowance. **A reviewer cannot
    create that authority by calling the remainder "out of scope."** Narrowing
    is the path of least resistance in review — it costs the reviewer nothing,
    reads as prudence, and can never be shown wrong, because the wider version
    is never built.
  * **A plan's own explicit fence.** A chunk marked MAINTAINER-GATED or
    MAINTAINER-ONLY does not execute without the authorization it names.

  **Why this is stated positively.** The rule it replaces — *never commit
  without explicit approval* — predates Cairn and was the reaction that led to
  building it. That hazard is now answered by the apparatus itself: a proposal,
  a fresh reviewer at every stage, an accepted plan with per-chunk
  acceptance criteria, and fences where a human is genuinely needed. A blanket
  per-commit gate on top of all that is the earlier, cruder instrument left
  running after its replacement was built, and it has cost real work. If an
  incident argues for tightening, tighten *the plan's fences* or *what a review
  must show*, which is where approval binds to something specific.
* **Scribing a Decision.** An explicitly-instructed agent may scribe and commit
  the Maintainer's Decision, bounded by three rules: **quote the authorization
  verbatim and visually isolated** in both the `## Decision` block and the
  commit body (paraphrase admits drift, condition-softening, or a hallucinated
  approval); act only on an instruction unambiguous on *both* disposition and
  commit, or confirm first; and land **nothing else** in that commit.
* **Commit with explicit paths** — `git commit <path> ...`, naming exactly the
  files. **Never a bare `git commit`**: it commits the entire staged index, so
  another agent's staged work rides in under your message and author.
  * **Prefer the windowless commit** — for tracked files `git commit <paths>`
    stages *and* commits atomically, so no staged window is ever exposed.
    **Verify via the working tree** (`git status --short`, `git diff <paths>`);
    do **not** verify with `git diff --cached`, which manufactures the window
    and reads back everyone's staged index.
  * **New / untracked files** — `git add <paths> && git commit <paths>` in one
    invocation. If the chain aborts, `git restore --staged <paths>` immediately.
  * **A `git mv` rename needs *both* sides named** — naming only the destination
    leaves the source-side deletion unstaged.
  * **Bright line** — never leave a `git add` / `git mv` exposed across tool
    calls, verification, or other work.
* **Untracked lifecycle artifacts — commit atomically.** If you write a plan,
  proposal or strategy doc meaning to ship it, commit it the *same turn*; never
  leave it untracked for another agent to inherit. If you can't commit this
  turn, don't write it yet.
* **Shared communication files** — the roadmap boards, the changelog — are
  edited only at defined serialization points (a lifecycle archive, the goodnight
  routine, explicit instruction).
* **Verification boundaries.** Three jobs; do not pay for the same broad run at
  every one.
  * **The full suite runs only as a certifying run.** A full run is evidence
    about a *tree*, not about one change, so it is paid for once per integration
    point, never per change and never per revision. Wherever this section says
    the full suite runs, a record is `full`, or a fresh full run is required,
    that evidence comes from the next **certifying run** that contains the
    change's final commit. It never comes from a run the implementer or a
    reviewer makes for one change. A certifying run is Cairn's pair (Boundary B,
    below) on a clean committed tree under the canonical interpreter, and it is
    made only:
    * before a push;
    * before the Maintainer's re-anchor ceremony;
    * before a release cut;
    * when the Maintainer asks for one.

    One green run at commit `T` certifies every change at or before `T`. A
    record cites it as `**Certified by**: <T>`, or as `pending` until one
    exists. **Nobody sets `CAIRN_FULL_SUITE=1` for any other reason**: not at
    Boundary A, not for a Boundary B record, not to reproduce another agent's
    record, and not for a mutation sweep. The broad-run guard refuses without
    it, and that refusal is this rule working. If a certifying run fails, bisect
    the range since the last certified commit. The change that broke it goes
    back to its owner, and nothing is pushed until the tree certifies. This
    holds for already-open plans too: where a plan's own text asks for a full
    Boundary B, a scoped record plus the certifying run satisfies it.
  * **The suite has a budget.** A test pins a property in one node.
    Parametrizing over every word, line or file of a text does not test a
    property, and a mutation ledger breaks the claims under review, not every
    token. If a certifying run takes longer than 10 minutes on the canonical
    machine with nothing else running, the next goodnight scrub queues a
    consolidation row.
  * **A — Iteration (scoped).** During implementation, run the tests and probes
    the reviewed plan maps — or, for a trivial change, with no proposal or plan,
    the tests that own each touched surface, found by searching for what imports
    or reads the touched files rather than by expectation — plus standing gates
    for every touched surface. If a substantive surface has no such mapping,
    search for its owners the same way; if none can be found, say so in the
    record, and the certifying run covers it. A **substantive surface** is anything that is not ordinary
    prose under the prose-only rule below: code, tests, executable templates and
    snippets, fixtures, manifests, and prose a test or manifest pins.
  * **B — Integration (stable evidence).** After the final implementation commit
    and before code review, against a clean unchanged commit under the
    **canonical interpreter (Python 3.13.x)**. Where this paragraph says the
    full suite runs, read it as "the certifying run covers it" (above): the
    change's own record is scoped, with `**Certified by**: pending`. Cairn's pair is
    `CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests
    --quality-gate-shuffle-seed=0` then
    `python scripts/quality_gate.py --sub neutrality --sub redundancy`.
    Run the **full suite unless the mapping bounds the change's effects
    confidently** — if a substantive surface has no such mapping, or its effects
    **cannot be bounded confidently**, the full suite runs. **Bounded mode refuses**,
    and the full suite runs, whenever the change touches a **contract surface**
    (the install contract, the fidelity or gate manifest, the lockfile schema, the
    published `scaffold.py --manifest`) or a **trust-ceremony surface** (any
    high-risk surface this file names, or release or security ceremony work).
    **Uncertainty resolves to `full`** — the fence is a refusal rule, not a
    checklist to argue past. Record `**Boundary B mode**: full | bounded`; on
    `bounded`, name the touched surfaces, the test files or nodes and the gates
    run, with counts, why the effects are bounded, and the explicit absence of
    any contract or trust-ceremony surface.

    **Boundary B governs every implementation, a trivial change included.** A
    trivial change's mapping is the owning tests Boundary A names, and Boundary
    C's Bounding verdict reviews it afterwards. It runs before the commit, not
    after, on exactly the bytes being committed: a tree clean apart from the
    change, or a separate copy holding only it. Its record is its commit body,
    not a plan section, and carries the mode, the interpreter, and on `bounded`
    every field the record sentence above names. An accepted proposal
    implemented in one commit with no plan records its result the same way, in
    its commit body, and if it ran fewer than all the tests, the code reviewer's
    Bounding verdict rules on whether the tests chosen were enough.

    **An already-open plan keeps the verification contract written in it.**
    Bounded mode reaches it only through that plan's own append-only revision.

    A plan appends the tested SHA/range, interpreter, clean pre/post state,
    commands, outcomes, timing, non-pass disposition, and known omissions as
    `## Implementation verification -- <agent> -- YYYY-MM-DD`.
  * **C — Falsification (independent).** The code reviewer verifies that record
    against the reviewed range, then runs independent targeted falsification;
    copying Boundary B's broad command is not a falsification ledger. On a
    bounded record the reviewer records
    `**Bounding**: ACCEPTED | FULL RUN REQUIRED` after challenging at least one
    named surface, mapped test, or stated omission — never "the field is
    present". **The reviewer never runs the full suite.** A required fresh full
    run is the next certifying run, and until it lands the change stays
    uncertified. A fresh full run is required when: **no valid Boundary B record exists**;
    an **unrecorded cross-surface dependency** appears; the run reports a
    **skip, xfail, or xpass** that the record does not dispose of; **review
    sharpening changes implementation, tests, executable templates, or**
    fixtures — any change to
    **implementation/test/executable-template/fixture bytes** invalidates the
    record; a **trust ceremony that explicitly requires** one applies; or there
    is a **concrete reason to distrust or falsify** the evidence.

    **When a finding or claim says a value must reach every member of a set**
    (every call site, every rendering path), list the set from the tree, not the
    diff, and mutate each member, in a separate copy; reading the diff does not
    settle it. A mutation ledger reports each mutant as killed, survived or
    equivalent, beside an unmutated control run, never as a bare "N of M
    killed". A mutant is one deliberate break, made to see whether any check
    notices: it is killed if some check fails on it, survived if every check
    still passes, and equivalent if the break changes no behaviour. Equivalence
    is measured, not argued: a behaviour test through the real entry point
    passes under the mutation, and where another site is said to recover the
    value, mutating that site fails. Any equivalence that was not measured is
    reported as a survivor. Outside that trigger, mutation stays the reviewer's
    choice.

  **Prose-only work does not run the suite.** Markdown has no importers: a
  sentence cannot propagate into behaviour the way a changed symbol does, so
  the blast radius is bounded by what *reads the file*. Run the applicable
  claim, link, snippet and neutrality gates, plus any test that actually reads
  the changed file — find them, do not assume the set is empty and do not
  assume it is everything. A prose change to a contract or high-risk surface
  does not trigger the full suite unless a test or manifest pins its bytes;
  check whether one does. When none does, the record is the gates run and the
  search that found none, in place of a bounded record. Release verification
  is a separate strict ceremony. Name the interpreter alongside every suite
  figure.
* **Keep commit bodies concise.** The body is a *snapshot* — what shipped and how
  it was verified — not a restatement of the proposal or plan. Target 15–30
  lines for a non-trivial commit: a one- or two-sentence opener cross-referencing
  the source artifact, a short bullet list of substantive changes by file or
  surface, and a one-line verification snapshot with concrete numbers.

## Verifying claims

**Verify before asserting.** Before committing a proposal, plan, or doc, run
`python scripts/claim_check.py` over it: it hard-flags broken repo paths and
out-of-bounds line citations. A hard flag is resolved before commit; a deliberate
forward-reference is *marked*, not left to assert. The checker is a **discipline
aid, not a gate** — the verify-before-asserting habit is the doctrine; the tool
only shifts its cheap, mechanical part left.

**Name the trigger, check what it checks, and open it.** Any document that
describes a check says what runs it — a command a person runs, a test, a git
hook, or a CI job. Cairn has no CI; do not write "in CI" for something no CI
runs. A check whose only trigger is a human remembering is described that way.
A tool that returns success without testing the claimed property is a worse
defect than no tool, because it is silent. **A named trigger is checked by
opening it — a path that resolves is not a trigger that governs — and the check
recurses until it reaches a human or a machine.**

**Confirm the instrument before trusting an absence.** A grep that returns
nothing, a count that matches, a failure list that comes back clean — each is
evidence only if the pattern *could* have matched. Before acting on a negative
result, run the same measurement against a case known to be present.

## Documentation discipline

Cairn uses a **placement-decision procedure**: see
[`docs/DOCUMENTATION_PLAN.md`](docs/DOCUMENTATION_PLAN.md) for the four-layer
vision (entry / governing / deliberation / descriptive) and the routing rules.
Identify what the content is *doing* — prescription, deliberation, description —
and route by layer.

## Project-specific conventions

**Durable artifacts stand without the deliberation that produced them.** A test
name, a comment, a docstring outlives the plan chunk and the review finding that
prompted it. The next reader has no proposal open and no reviewer to ask, so a
coordinate — a finding id, a chunk letter, a plan row — is a pointer into a
conversation that has ended.

* **Name a test for the property it pins, not for what produced it.**
  `TestP2AmendmentBScopeReduction` tells the next reader nothing they can act on;
  `TestScopeReductionNeedsMaintainerAllowance` tells them what breaks if it
  fails. Put the *reason* in the docstring, and no coordinate.
* **Comments and docstrings explain the code, not the process.** `# CR3: use a
  set here` decays the moment CR3 archives; `# set, not list -- membership is
  checked once per candidate and the list is large` still works in five years.
  The bar is **"can the next reader act on this without the record?"**

**Naming.** UPPERCASE for landmark files (`README.md`, `AGENTS.md`,
`CHANGELOG.md`, `SECURITY.md`, `PLANNING.md`, `NEXT_SESSION.md`);
lowercase-kebab for content. Proposal stems are `<YYYY-MM-DD>-<author>-<slug>.md`;
plan stems are `<slug>.md`.

**Development environment & dependency budget.** Everything Cairn ships an
adopter — the scaffold engine, `scripts/`, the reference checkers — is
**standard-library-only**: adopters take on **zero runtime dependencies**.
Dev/test tooling is dev-only and never in the adopter path. See
`bootstrap/DEPENDENCY_BUDGET.md` before adding any import. Run the suite with
`CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests` — the bare form is refused
by the broad-run guard.

**A fresh clone has no gate anchor, and the gate will refuse.** `git clone`
fetches `refs/heads/*` and `refs/tags/*`; the differential-oracle gate's trust
root lives at `refs/cairn/gate-anchor`, which is in neither. Fetch it:

```
git fetch origin '+refs/cairn/gate-anchor:refs/cairn/gate-anchor'
```

Refusing is correct — a missing trust root must never read as a pass — so the
hazard is **human**: the refusal arrives during setup, looks like a
configuration annoyance, and invites building the habit of routing around a
refusal. Receiving the ref proves availability, not authenticity; what makes it
trustworthy is the signature on the commit it names.

**High-risk surfaces (Security-Review + proposal triggers).**
* **The scaffold / merge engine** (`bootstrap/scaffold.py` →
  `bootstrap/_scaffold/`) parses untrusted module and profile files, does path
  handling and YAML loading, and writes into a target tree — guarded by a
  symlink/containment check and a Bandit gate over the whole engine package.
* **Vendor-neutrality.** Doctrine and templates must name no AI model/vendor
  (`scripts/quality_gate.py --sub neutrality`); names live only in the
  deliberation record or behind a `vendor-ok` marker.
* **The install contract** — the fidelity manifest, the gate manifest, the
  lockfile schema, and the published `scaffold.py --manifest` — is what adopters
  depend on; treat it as byte-level stable.
* **The by-file license split** — code is MIT wherever it lives; prose and
  document templates are CC BY 4.0; the brand mark alone is CC BY-ND.
* **The local interpreter binding** — `dev/.cairn/local-env.json`, its reader
  `_resolve_interpreter` in `templates/skills/_lib/session.py` (self-hosted at
  `tools/session.py`, kept byte-identical), and every call site that executes
  the path it returns. This is an untracked, gitignored, lockfile-uncovered
  **executable trust root**, and the reader is a strict *shape* validator, not
  an authenticator: it checks absoluteness, schema, symlink-freedom and the
  executable bit, but neither Python identity nor provenance. Changes to its
  schema, validation order, fallback disposition, warning visibility, or
  subprocess use take a Security Review. The same module owns `encode_display`,
  the single terminal encoder — there is no second escape table in this tree,
  because a fallback engages exactly when something is already wrong.
* **The portable-sweep executable trust root** — `run_portable_security_sweeps.py`
  (shipped at `templates/modules/team-gated/`, self-hosted at `scripts/`, kept
  byte-identical), its `resolve_executable` / `revalidate` pair, and
  `portable_security_policy.json`. The authority here is **`PATH` resolution**:
  the runner locates a host `gitleaks` and executes it, and Gitleaks invokes
  `git` transitively — two host trust roots the scaffold neither installs nor
  ships. Resolution digests the binary and `revalidate` re-checks that digest
  **immediately before every invocation**, so the resolve→execute gap is
  measured rather than assumed. Absence is `INCOMPLETE` (exit 5), loudly, and
  never clean; the adapter has **no egress path**. Changes to executable
  resolution, the revalidation points, the policy schema, the child environment,
  the exit precedence, or the admitted version set take a Security Review.
  Fuller treatment in `bootstrap/SAFETY.md`.

**Operational pitfalls.**
* **AST attestation baseline.** `bootstrap/tests/test_ast_attest.py` pins the
  engine package against a committed baseline; after any `bootstrap/_scaffold/`
  change it must be re-anchored (it does not auto-update). Self-service repair
  reaches only the symbols in `_ast_attest._UPDATE_ALLOWLIST`, and only when the
  target is the **only** changed symbol; anything else is a **Maintainer-run,
  dry-run-verified direct correction**. The procedure is
  [`bootstrap/AST_BASELINE_RUNBOOK.md`](bootstrap/AST_BASELINE_RUNBOOK.md) —
  derive the expected CHANGED set against the committed baseline rather than
  carrying a figure forward.
* **The gate manifest goes stale silently — whether a frozen file changes or is
  deleted.** Once committed, neither reddens the suite: `test_gate_manifest.py`
  self-verifies a freshly produced manifest and never diffs the committed
  fixture, and a deleted file simply drops out of the fresh one. So a green suite
  is not evidence that no re-anchor is owed. An *uncommitted* edit to a frozen
  file does redden it (`FROZEN-MODIFIED`): the fresh manifest hashes the
  committed blob, the check hashes the working tree. That is a reason to run
  Boundary B on a committed tree, not a sign that a re-anchor is owed. Only `python bootstrap/tests/_gate_manifest.py verify`
  compares the tree with the committed fixture (it reports `FROZEN-MODIFIED`,
  `FROZEN-MISSING`, `COLLECTION-DROPPED`), and nothing runs it automatically: it
  runs by hand, in the re-anchor ceremony (`bootstrap/REANCHOR_RUNBOOK.md`).
  Until then, the queued re-anchor row in `dev/PLANNING.md` is the only record
  of what is owed.
* **Commit hygiene.** Always `git commit <paths>`; see *Git and commit workflow*.
* **Doctrine changes clear the rate-limit gate** — a single incident does not
  justify a doctrine change unless it is the high-risk case.

## Vendor addendum

`AGENTS.md` is vendor-neutral — it names no specific AI agent tool. Doctrine
specific to one tool (a harness path, a session-model habit) goes in that tool's
own file, which opens by importing this one (`@AGENTS.md`). Cairn ships the thin
wrapper as `VENDOR.md`; the adopter renames it to their tool's auto-loaded file.

**Drift guard.** The wrapper carries *only* harness-specific habits. Everything
an agent of a *different* tool would also need stays canonical **here**, and the
wrapper points at it. A wrapper that duplicates this content has drifted into a
fat fourth doc; fold it back and leave only the pointer.
