<!-- cairn-internal-ref-allow: doctrine/rationale.md doctrine/proposals.md doctrine/coordination.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see AGENTS.md, "Where doctrine/ references resolve") -->
<!-- claim-check-allow: bootstrap/tests/test_fork_advisory.py -->
<!-- ^ The forward-reference test file this proposal would create; declared under "Proposed paths" below and cited again in the Tests section. -->

# Fork advisory semantics — the comparison bytes come from the caller, never from the tree being checked

**Author**: Claude (Strategy)
**Model**: Claude Opus 5
**Date opened**: 2026-08-03
**Status**: reviewed
**Touches**: `bootstrap/_scaffold/lockfile.py` (`forked_facade_findings`,
`format_forked_facade_warning`), `bootstrap/_scaffold/install.py` (one new
helper), `bootstrap/_scaffold/upgrade.py` (`cmd_upgrade`, one call site),
`bootstrap/verify_integrity.py` (one call site), `bootstrap/UPGRADE.md`,
`bootstrap/_scaffold/SECURITY_MUTATIONS.md` (one recorded trigger sentence),
`bootstrap/tests/test_verify_integrity.py` (call-signature update, assertions
unchanged), and a new test file
**Related**: successor **scope 3 of 4** from the superseded `identity-not-name`
proposal (Decision 2026-08-03), which this proposal executes; its External
Security Review finding **[IDN4]**, its author Response accepting [IDN4]
including the omission; the `gate-reanchor-preflight` lifecycle, whose
dated-posture expiry pattern the residuals below reuse; the
`lockfile-provenance-fields` lifecycle, the direct precedent for changing
`bootstrap/_scaffold/lockfile.py` and re-anchoring the AST baseline afterwards
**Plan review**: **required(External, security lens)** — see *Why this tier*
below. This is not a discretionary escalation: `bootstrap/_scaffold/` is on
`AGENTS.md`'s high-risk-surface list, which is an independent Security-Review
trigger, and the specific defect class here has a demonstrated same-author blind
spot recorded in the parent lifecycle.

## Context

**A one-paragraph glossary first**, because three Cairn-specific terms carry the
whole argument. A **facade** is a thin launcher script Cairn installs into an
adopter's tree (`tools/intent.py`) that loads an **engine package** sitting
beside it (`tools/_intent/`) — the launcher is deliberately tiny and the real
code lives in the package. The **lockfile**
(`dev/.cairn/cairn-lock.yml`) is a machine-generated record of every file the
install wrote, with a SHA-256 hash for each, so `bootstrap/verify_integrity.py`
can later attest that nobody swapped a shipped script. Each lockfile record
carries two hashes: `hash` (what is on disk now, as last attested) and
`base_hash` (nominally the upstream template the file started from).

`bootstrap/_scaffold/lockfile.py` contains a **fork advisory**: a detector that
warns when a facade has diverged from upstream while its engine package sits
installed, on the theory that you are then running a stale launcher against a
maintained engine. Two things about it are wrong, and both were verified by
execution against this tree on 2026-08-03 under the canonical interpreter
(`~/conda_envs/lhm/bin/python`, 3.13.13).

**(a) It fires on files that have not forked.** Running the verifier against
Cairn's own tree emits two notes:

```
$ python bootstrap/verify_integrity.py --target .
verify_integrity: NOTE -- facade 'tools/intent.py' is forked from upstream
  (hash != base_hash) but its engine package 'tools/_intent' is installed.
  You are running an un-maintained fork of the launcher while the
  maintained engine sits dormant; upstream engine fixes will not take effect.
  ...
verify_integrity: NOTE -- facade 'tools/lifecycle_metrics.py' is forked ...
verify_integrity: OK -- 76 recorded file(s) match dev/.cairn/cairn-lock.yml
  (5 adopter-authored living-state file(s) ...)          # as_of 2026-08-03
```

Both notes are false in both of their claims. Each facade is **byte-identical**
to its current template source — `tools/intent.py` and
`templates/modules/team-gated/intent.py` both hash `sha256:6462d404…`;
`tools/lifecycle_metrics.py` and `templates/modules/default-on/lifecycle_metrics.py`
both hash `sha256:86a64b0a…`. And the engine is not dormant: `tools/_intent/`
holds 7 modules and `tools/intent.py`'s `_load_engine()` raises `RuntimeError`
if the package is absent, so the launcher cannot run *without* loading it.

The cause is the comparison. The detector's fork test is `hash != base_hash`,
and `base_hash` is not reliably an upstream hash. `bootstrap/_scaffold/upgrade.py`
documents that `--finalize` preserves `base_hash` and, for a record predating
that field, **backfills it from the then-current installed hash** — a snapshot of
the local tree. So every legitimate edit-then-finalize widens the apparent gap.
It ratchets, and it never narrows.

This is not a self-hosting curiosity. Any adopter who customizes a facade and
runs `--finalize` inherits the same permanent warning telling them their tree is
compromised.

**(b) The remediation string advises an action that breaks the tool** — and it
is **not in this proposal's scope.** The Maintainer's Decision on
`identity-not-name` routes it out as condition 3: it lands immediately as a
trivial-class commit outside all four successor scopes, because it has no design
question attached. Recorded here only so a reader can see it is routed, not
dropped. Its sequencing interaction with this proposal is in *Coordination* below.

**What [IDN4] added, and why it is the real content of this proposal.** The
parent proposal's fix was one sentence: *"when a template source is resolvable,
compare against it."* The External Security Review found that under-specified in
exactly the way its own [IDN1] was:

> Resolving `src` from the target or a path named by its lockfile would let the
> tree being checked choose the comparison bytes.

The parent's Response accepted this and named the invariant that survived the
whole exchange:

> **The artifact under verification must not supply the material used to verify it.**

That is the design constraint this proposal exists to satisfy. Getting the false
positive to stop is the easy half; getting it to stop **without handing the
target a lever** is the half that needs a security review.

## Proposed paths

Proposed paths:
- `bootstrap/tests/test_fork_advisory.py` — the new test home for this change; lands with the implementing plan.

## Proposal

### The shape of the change

The detector gains a **required, caller-supplied trusted upstream**, and the
lockfile stops contributing anything the comparison depends on.

`bootstrap/_scaffold/lockfile.py`:

```python
class UpstreamSource(NamedTuple):
    templates_root: Path            # trusted, caller-resolved, absolute
    src_for_dst: Mapping[str, str]  # trusted dst -> templates-relative src
    ref: str                        # "<cairn_version>@<cairn_commit>", for the note

def forked_facade_findings(
    target: Path,
    lock: dict[str, Any],
    *,
    upstream: UpstreamSource | None,      # NO default -- see below
) -> list[dict[str, Any]]: ...
```

**`upstream` is keyword-only and has no default.** A caller must decide, in
writing, which bytes it is comparing against; passing `None` is a legal and
explicit choice meaning *"I have no trusted upstream — report install-time
semantics only."* Omitting the argument is a `TypeError`. That is deliberate:
the failure mode this whole class produces is a caller silently inheriting an
ambiguous default, and a required parameter is the only construction that makes
that impossible rather than merely discouraged.

### Where each caller's bytes come from

Per [IDN4]'s satisfier, the source is defined **per caller** and neither caller
derives a root from anything the target controls.

| Caller | `templates_root` | Meaning of the note |
|---|---|---|
| `bootstrap/verify_integrity.py` | `CAIRN_ROOT / "templates"`, where `CAIRN_ROOT` is resolved from the verifier script's own on-disk location | *differs from the upstream in the verifier checkout you ran* |
| `cmd_upgrade` in `bootstrap/_scaffold/upgrade.py` | the already-resolved `cairn_root / "templates"` it computes before dispatch | *differs from the upstream you are upgrading against* |
| `cmd_upgrade` with `--to <ref>` | **`None`** | *could not be confirmed against upstream* (see R3) |

`src_for_dst` is built once by a new helper in `bootstrap/_scaffold/install.py`,
beside `install_manifest()` which supplies its data:

```python
def trusted_upstream(cairn_root: Path) -> UpstreamSource: ...
```

`install_manifest()` returns `(source, destination, verbatim)` derived purely
from the engine's own registries (`_CORE_MAPPINGS`, `_SKILLS_MAPPINGS`,
`_ALWAYS_ON_MAPPINGS`, `_MODULE_MAPPINGS`) and **already refuses a duplicate
destination**, so the destination→source map is well-defined. Measured on this
tree: 95 rows, 95 unique destinations, 0 duplicates, `as_of 2026-08-03`.

This is stronger than validating the lockfile's `src` field, and it is the
substantive design decision in this proposal. The lockfile's `src` is
target-controlled data; under the parent's phrasing it would have chosen which
template the comparison read. Here **`src` is never used for comparison at all.**
The lockfile contributes only `dst` — which is also the path being read off
disk, so it cannot select bytes independently of the file it is about — and `dst`
is used to *look up* a source in a map built entirely from trusted code. A tree
cannot point the comparison at a lookalike template it planted, because the tree
never names the source.

`src` is still read, for one purpose: if the lockfile's recorded `src` disagrees
with the trusted map for the same `dst`, the finding carries
`src_relabelled: True` and the note appends a tamper line. A disagreement can
never *suppress* a note; it can only add one.

### The one-way property, stated as an invariant

**Invariant F1 — the new finding set is a subset of today's finding set.**
Supplying a trusted upstream can only *remove* a finding (when the on-disk file
is byte-identical to trusted upstream, so the "un-maintained fork" claim is false
by construction). It can never add one.

F1 is what makes this change safe for adopters whose install is legitimately
behind the templates in the checkout they happen to be verifying from. The
parent proposal named that scenario as the finding it most expected a reviewer to
land — *"if comparing against the template source produces new false positives in
adopter trees where the template legitimately advanced ahead of the install"* —
and F1 forecloses it structurally rather than by argument. If a reviewer breaks
F1, the design is wrong, not the wording.

### Path validation on the source side

Even though `src_rel` now comes from trusted code, the joined path is validated
before it is read, because [IDN4]'s satisfier asks for it and because a
templates tree can be tampered with independently:

1. `src_rel` must be relative, POSIX-shaped, and free of `..` components.
2. `(templates_root / src_rel)` is checked with the engine's existing
   containment guard `_assert_safe_write(candidate, templates_root)` from
   `bootstrap/_scaffold/security.py` — three fail-closed checks: the path is not
   itself a symlink, no directory between the root and the path is a symlink, and
   the resolved path stays inside the root.
3. The result must be an existing **regular file**, not a symlink.

Any failure means **no comparison happens** and the finding is retained with an
explicit "could not confirm" kind. It is never treated as a match. The exception
is caught inside `lockfile.py` so a malformed templates tree degrades the
advisory instead of crashing the verifier.

Reusing `_assert_safe_write` on a *read* path is a deliberate reuse of an
already-reviewed, regression-pinned primitive rather than a second copy of the
same three checks; its write-flavoured message is caught and never surfaced. The
naming mismatch is recorded as **R6** below rather than fixed by growing the
security leaf for a single caller.

### What the note says, and what each phrasing means

[IDN4] requires the note's meaning to be stated rather than left ambiguous. It
has three kinds, and the kind is a field on the finding, not a guess the reader
makes:

* **`differs-from-upstream`** — a trusted upstream was resolved and the on-disk
  file differs from it. The note names the upstream it compared against
  (`<version>@<commit>`), so the reader can see whose bytes decided the verdict.
* **`unconfirmed`** — no trusted upstream was available for this record (the
  caller passed `None`, `dst` is absent from the trusted map, the file is
  missing, or validation refused). The note says the file differs from its
  **install-time baseline** and that this **could not be confirmed against
  upstream**. This is today's behaviour, now labelled instead of implied.
* **skew annotation** — when the trusted upstream's `cairn_version` /
  `cairn_commit` differ from the lockfile's, the note appends a line saying so:
  *"the comparison upstream is Cairn X (commit c) while this tree was installed
  from Y (d); a difference may be a version gap rather than a fork."* Skew is
  labelled, not resolved. Under F1 it cannot manufacture a finding.

### What this change does **not** fix

Stated explicitly, because the parent lifecycle recorded its author overstating a
protection three times and the review caught each one.

1. **It does not authenticate the checkout that supplies the comparison bytes.**
   `verify_integrity`'s `CAIRN_ROOT` is derived from the script's own location.
   Run a tampered verifier and you get tampered comparison bytes. That is the
   pre-existing trust root, and the out-of-band bootstrap for it is the
   **release-authenticity** successor's job ([IDN1]), not this one. This change
   moves the comparison from *target-controlled* to *caller-controlled*; it does
   not move it to *cryptographically-anchored*.
2. **It does not repair `base_hash`.** For an `unconfirmed` record the ratchet is
   still there. Re-anchoring `base_hash` during `--finalize` was considered and
   rejected in the parent proposal — it would make finalize bless the current
   tree as upstream, a strictly worse failure than a noisy note — and this
   proposal does not revisit that.
3. **It does not change any exit code.** The advisory stays advisory. A genuinely
   forked facade still passes `verify_integrity` (its on-disk bytes match the
   recorded `hash`), exactly as today.
4. **It does not attest the engine package's contents** — only its presence
   (a directory holding at least one `.py`). Engine members are covered by the
   ordinary lockfile hash check, or not at all.
5. **It does not close `fork_acknowledged`**, the target-controlled verify-time
   opt-out. Unchanged.
6. **It does not fix the remediation string** (condition 3 routes that out).

### Coordination

* **The trivial-class remediation-string commit should land first.** It edits
  `format_forked_facade_warning`, the same function this proposal rewrites. If it
  lands after, it re-touches a function this plan already changed and the AST
  delta below must be re-derived. **A coordination hazard worth the Maintainer's
  attention, offered without reopening condition 3:** that commit is trivial in
  *design*, but because it edits `bootstrap/_scaffold/`, it inherits the same
  supervised AST re-anchor obligation described below. It therefore needs either
  its own supervised re-anchor, or — cheaper, and the recommendation here — it
  lands first and this plan's single re-anchor absorbs both deltas. Which of the
  two is the Maintainer's call, not this proposal's.

  **The cost of the cheaper path, priced rather than assumed.** If the trivial
  commit lands first and waits for *this* plan's re-anchor, the canonical suite
  command is **red** for the whole interval between them — measured in a scratch
  copy under the canonical interpreter on 2026-08-03: a one-clause edit to
  `format_forked_facade_warning`'s string changes its structural digest and fails
  exactly two nodes in `bootstrap/tests/test_ast_attest.py`, with no other net
  delta. This plan's lifecycle is weeks, not hours, and any concurrent session
  inherits that red tree — which sits badly against `AGENTS.md`'s "run the test
  suite after any substantive change". The three shapes actually available are:
  (1) trivial commit + its own Maintainer-run one-key re-anchor **in the same
  sitting**, keeping the tree green and costing one extra ceremony;
  (2) trivial commit first, re-anchor deferred to this plan, cheapest in ceremony
  and red in between; (3) the trivial fix folds into this plan as its first chunk,
  one ceremony and no red window, at the cost of the dangerous advice staying live
  until this lifecycle completes — **and that shape requires the Maintainer to
  amend condition 3**, which this proposal does not ask for and would not take
  without an explicit instruction. Recorded because condition 3 was written before
  the AST gate's reach on this function was measured.
* **No collision with the other successors.** Scope 1 touches
  `bootstrap/container/verify-ref.sh` and `bootstrap/PROVENANCE.md`; scope 2
  touches `tools/lifecycle_planner.py` and its shipped twin; scope 4 touches
  root documentation. None touches `bootstrap/_scaffold/lockfile.py` or
  `bootstrap/verify_integrity.py`.
  **One adjacency worth an implementer's attention, and it is not a collision.**
  Scope 4's residual **R1** identifies a defect in `bootstrap/_scaffold/upgrade.py`
  — `_infer_init_lock_axes` infers `human_team` from the mere *presence* of a root
  `CONTRIBUTING.md` — and declines to fix it on exactly this proposal's gate
  reasoning (the fix is an engine change carrying an AST re-anchor). **This scope
  does not claim that fix either**, and says so deliberately: it is a different
  function from the three this change touches, folding it in would break the
  falsifiable AST target enumerated below (3 CHANGED, not 4), and scope 4 already
  carries it as a residual with three observable triggers. Recorded so an
  implementer working in `upgrade.py` sees the adjacent item rather than
  discovering it, and so no reader concludes scope 3 absorbed it.
* **No collision with the concurrent Theme 3 proposals.** Checked by grep across
  the seven proposals opened 2026-08-03: none names `lockfile.py`,
  `verify_integrity`, or the fork advisory.

### Class C — a declared departure from the Decision's *Carried forward*, needing ratification

> **This section is worded identically in scope 1 (`release-authenticity`),**
> **apart from two cross-reference sentences that necessarily point the other way.**
> It records a *joint* disposition reached by both drafting authors, so the two
> proposals cannot be read as disagreeing. A reader needs it in only one place;
> it appears in both so that whichever proposal is read first carries it.

The superseding Decision carries forward the `SECURITY_MUTATIONS.md` Class C
follow-on — six `upgrade`-family commands (`cmd_update_profile`, `cmd_init_lock`,
`cmd_rebase`, `cmd_verify`, `cmd_drift`, `cmd_complete_merge`) that write into an
adopter tree without routing through the `_assert_safe_write` containment guard —
as a candidate for scope 1 or scope 3, *"at the drafting author's judgment"*. The
Decision's own condition 1 exists because that follow-on was routed to a roadmap
row in a prior lifecycle and **never opened**.

**Both authors exercised that judgment and both declined.** That is the departure,
and it is stated rather than disguised, because a candidate that each scope
assumes the other took is exactly how this item went missing the first time.

* **Scope 1 declines** because it touches **no** `bootstrap/_scaffold/` file at
  all. Absorbing Class C would attach the entire engine gate set — the Bandit
  engine gate and a Maintainer-run AST baseline re-anchor — to a change that is
  otherwise a shell script and three markdown files, and would stall the v0.4.0
  tag behind it. That coupling is precisely what the four-way split exists to
  prevent.
* **Scope 3 declines** because Class C is a **behavioral change to six write
  paths**, and scope 3 adds no write at all: its detector reads, and
  `test_security_leaf.py`'s pinned `_GUARDED_WRITE_FUNCS` set is untouched by it.
  Folding Class C in would put two contracts and two gate sets in one plan — the
  same failure. Scope 3 already carries two `FROZEN-MODIFIED` HOLDs and an AST
  re-anchor; a six-command write-capability redesign is not a rider on that.

**Shared-package adjacency is not a shared contract.** The one argument for
folding Class C into scope 3 is that both live in `bootstrap/_scaffold/`. Both
authors judged that insufficient: co-location in a package is not co-location in
a *contract*, and "it is in the same directory" is the reasoning that produced
the parent proposal's four-gate-sets-in-one-artifact failure.

**The consequence, stated plainly:** on this disposition Class C is **not claimed
by any of the four successors**, and it therefore needs **its own proposal**.
Neither drafting author has authority to open a fifth scope, so this is put to the
Maintainer as a decision, not resolved here.

**What the Maintainer must choose.** Option 1 is what both authors propose;
options 2 and 3 are recorded as honest alternatives, not straw men.

1. **Ratify the departure and open Class C as its own proposal** — *the option
   both authors propose.* It gets the same anti-debt treatment condition 1 gave
   the four: it is *opened*, not routed. The cheapest form matching condition 1's
   shape is to extend that condition — `identity-not-name` does not archive until
   Class C is opened either. That is a Maintainer condition and only the
   Maintainer can add it.
2. **Overrule scope 3's decline** and direct it to absorb Class C. The cost is
   named above and it is real: two contracts, two gate sets, and a longer
   External security read on the successor that already carries the heaviest gate
   accounting.
3. **Overrule scope 1's decline.** Both authors judge this the worst of the three
   — it puts adopter-tree write containment inside a cryptographic
   release-provenance proposal, and the two share no surface, no test home and no
   reviewer lens — but it is recorded so the choice is a full one.

**The anti-drop mechanism, whichever branch is taken**, because naming a home is
what failed last time: the disposition lands as a `dev/PLANNING.md` row in the
Decision commit of **whichever successor is decided first**, and as one recorded
sentence in `SECURITY_MUTATIONS.md`'s own Class C section — **R7** below owns that
sentence and its trigger. An accepted proposal archives, and archived proposals
are not read — that is the lesson `gate-reanchor-preflight` Round 5 recorded when
it moved its non-mechanical expiry triggers out of the proposal and into
`dev/PLANNING.md` and the runbook. What is not acceptable is the row existing
nowhere; that state is what the Decision's conditions were written to make
impossible.

### Documentation / doctrine surface

* **`bootstrap/UPGRADE.md`** (descriptive layer, adopter-facing how-to) gains a
  short subsection stating the advisory's three note kinds and what each means.
  Today `UPGRADE.md` does not document the fork advisory at all, so an adopter
  who receives the note has no documented referent. This is the doc deliverable.
* **`bootstrap/_scaffold/SECURITY_MUTATIONS.md`** gains **one sentence** in its
  Class C section recording that the follow-on is **unclaimed by any of the four
  successors** as of this proposal — the declared departure above — and naming
  R7's three triggers. Not a re-classification; a durable home for a residual,
  per the pattern `gate-reanchor-preflight` established. The wording follows the
  Maintainer's ratification, so this sentence is written at plan time, not
  proposal time.
* **No `AGENTS.md` change and no `doctrine/` change is proposed.** One
  `AGENTS.md` correction is *identified* and deliberately **not** taken — see
  **R8**; it is a governing-layer edit on a different contract and bundling it
  would lose the git-workflow approval carve-out and mix two review tiers.

### Doctrine-change rate-limit

**Not applicable.** This proposal changes no rule, process, or contract that
every contributor follows. It is a defect fix in engine code, its tests, and one
descriptive-layer document. The one item that *would* engage the gate (R8's
`AGENTS.md` pointer correction) is explicitly routed out; the recurrence
evidence for it is recorded under R8 for whoever takes it.

## Rationale

* **Which user workflow does it improve?** The first-two-weeks adopter workflow.
  A scientist who customizes a facade — the thing Cairn's templates invite — and
  runs `--finalize` currently gets a permanent warning that their tree is running
  an un-maintained fork against a dormant engine. Both halves are false, and the
  adopter has no way to tell. Cairn's own tree demonstrates it today.
* **What contract does it preserve or clarify?** The lockfile's fork semantics
  are part of the install contract. Right now the advisory reports *"differs from
  a snapshot of your own tree"* while saying *"forked from upstream."* This makes
  the words match the computation, and names which upstream.
* **Reproducibility / correctness?** A verification tool that cries wolf trains
  its user to ignore it. For a repository whose product is an honest record, an
  integrity advisory that is wrong on its own tree is the worst possible
  demonstration.
* **Why now?** Three reasons. The parent proposal is superseded and does not
  archive until this successor is opened (condition 1), so this is on the
  critical path. The remediation-string fix is landing imminently in the same
  function, so the two want sequencing now rather than a merge conflict later.
  And the supervised re-anchor this change needs is cheapest while the baseline
  is clean — measured green today, 174 baselined symbols, 0 CHANGED,
  `as_of 2026-08-03` — rather than after unrelated drift accumulates.

### Why this tier — `required(External, security lens)`

Three independent reasons, any one of which would suffice:

1. **`bootstrap/_scaffold/` is on `AGENTS.md`'s high-risk-surface list** ("the
   scaffold / merge engine … guarded by a symlink/containment check and a Bandit
   gate over the whole engine package"). That is a Security-Review trigger by the
   letter of the rule, not by judgment.
2. **The defect class has a demonstrated same-author blind spot in this exact
   lifecycle.** The parent's Revised section records it plainly: the author found
   the "artifact must not supply its own verification material" violation at
   07:59 and then wrote two fresh instances of the identical class into the
   proposal within the hour. An Internal (same-type, fresh-session) read is by
   construction the same reasoning that produced the error. This is the strongest
   argument, and it is empirical rather than procedural.
3. **The parent's [IDN4] finding was BLOCKING DESIGN**, and the design it blocked
   is the whole content of this proposal. A blocking finding's satisfier deserves
   the tier that produced it.

**Additionally recommended, though not required by the Decision:** an External
security read of *this proposal* before its own Decision. The Decision required
proposal-time resolution of [IDN1]/[IDN2] for scope 1 for the same reason that
applies here — the trust-boundary design is settled in the proposal, so that is
where it should be attacked.

## Alternatives considered

* **Do nothing.** Not defensible. The advisory actively misleads today, on
  Cairn's own tree, in a first-two-weeks surface.
* **Validate the lockfile's `src` and use it** (the parent proposal's shape, with
  [IDN4]'s validation bolted on). Rejected. Validation proves *containment*, not
  *provenance*: a contained, regular, non-symlinked file under `templates/` can
  still be a template the target chose. Using the trusted destination→source map
  removes the choice instead of policing it. This is the difference between
  checking that the burglar used the front door and not giving them a key.
* **Re-anchor `base_hash` at `--finalize`.** Rejected in the parent proposal and
  not revisited: it would make finalize silently bless the current tree as
  upstream — a silent wrong answer replacing a noisy one.
* **Make the advisory blocking.** Rejected. It is heuristic (it correlates two
  weak signals: a hash gap and a directory's presence). A heuristic that changes
  an exit code is a heuristic people disable.
* **Add a read-flavoured containment sibling to `bootstrap/_scaffold/security.py`.**
  Considered and deferred. It is the tidier long-term shape, but it grows the
  security leaf — a high-risk surface — by a symbol with exactly one caller. Kept
  as R6 with a trigger (the second read-side caller) rather than taken now.
* **Materialize `--to <ref>`'s templates via `git show` and compare against
  those.** Rejected for this proposal as scope creep with its own trust
  questions (which ref, verified how). `--to` falls back to `unconfirmed`, which
  is honest, and R3 carries the trigger.
* **Suppress the note entirely when a trusted upstream matches, and drop the
  detector's `base_hash` test.** Rejected: `base_hash` is still the only signal
  available for `unconfirmed` records, and dropping it would silently retire
  coverage rather than fix it.

## Evidence / verification plan

Every factual claim above was verified by execution against this tree on
2026-08-03 under the canonical interpreter (`~/conda_envs/lhm/bin/python`,
3.13.13). Reproductions are inline so a reviewer can re-run them.

### The gate accounting — mandatory, and the thing the parent omitted

The parent proposal's Response called this omission *"a straight miss, not a
scoping choice … the single strongest argument for splitting."* It is carried
here in full. **Two different re-anchor ceremonies apply, and they are routinely
conflated** — including by `AGENTS.md` itself (R8).

**(i) The AST source-motion attestation.** `bootstrap/tests/test_ast_attest.py`
pins every top-level symbol in `bootstrap/_scaffold/*.py` against a committed
baseline (`bootstrap/tests/fixtures/scaffold_ast_baseline.json`) by a structural
digest that is insensitive to comments and formatting but sensitive to any logic
change. It **does not auto-update**. Verified today: 29 tests pass, 174 baselined
symbols, 0 CHANGED / MISSING / DUPLICATE, `as_of 2026-08-03`.

The self-service repair path is **not available** here. `_ast_attest.py`'s
`_UPDATE_ALLOWLIST` admits exactly four symbols (`_MODULE_MAPPINGS`,
`_SKILLS_MAPPINGS`, `_CORE_MAPPINGS`, `install_onboarding`); none of the symbols
this change touches is among them. The mechanism that actually applies is the
one the `lockfile-provenance-fields` plan established and used: a **Maintainer-run,
dry-run-verified direct-correction script**, whose result is recorded in a commit
the Maintainer authors — *"the correction itself was performed and decided by the
Maintainer, per `bootstrap/REANCHOR_RUNBOOK.md`'s 'must not bless its own
verifier' principle"* (commit `c3d5bd9`). **An implementing agent does not
perform it.**

The **falsifiable pre-re-anchor target**, derived from the designed edit and
re-derived by the plan against real digests before the handoff:

* **exactly 3 CHANGED** — `FunctionDef:forked_facade_findings`,
  `FunctionDef:format_forked_facade_warning` (both in `lockfile.py`),
  `FunctionDef:cmd_upgrade` (in `upgrade.py`);
* **0 MISSING, 0 DUPLICATE**;
* NEW-note set exactly `{FunctionDef:trusted_upstream, ClassDef:UpstreamSource}`,
  plus rotated `Import:` keys — reported as notes, never failures. The module
  docstring of `lockfile.py` also changes (its dependency paragraph must name the
  new import), but `_classify()` skips `Docstring*` keys in both directions, so
  it produces neither a failure nor a NEW note;
* `FunctionDef:_facade_engine_dir` **unchanged**.

A 4th CHANGED symbol is a stop-and-explain, not a re-run. (If the trivial-class
remediation commit lands first and is re-anchored with it, the target is measured
against that post-commit baseline; the count is unchanged.)

**(ii) The gate manifest.** `bootstrap/tests/_gate_manifest.py` freezes a set of
gate-defining files by SHA — **162 files, `as_of 2026-08-03`** — discovered by
glob over `bootstrap/*.py` (non-recursive), `bootstrap/tests/**/*.py`,
`bootstrap/tests/fixtures/**/*`, `scripts/*.py`, and
`templates/modules/**/*.py`. Editing a frozen file produces `FROZEN-MODIFIED`,
which the verifier records as a **HOLD** — a hard stop the run cannot
self-certify. This *is* the ceremony `bootstrap/REANCHOR_RUNBOOK.md` governs, and
its Phase 0 and Phase 4 are explicitly **Maintainer-only**.

Confirmed by direct membership check against the committed manifest,
`as_of 2026-08-03`:

| File | Frozen? | Consequence |
|---|---|---|
| `bootstrap/_scaffold/lockfile.py` | no (0 `_scaffold` entries in the frozen set) | AST attestation only |
| `bootstrap/_scaffold/install.py` | no | AST attestation only |
| `bootstrap/_scaffold/upgrade.py` | no | AST attestation only |
| `bootstrap/verify_integrity.py` | **yes** | `FROZEN-MODIFIED` → HOLD → supervised re-anchor |
| `bootstrap/tests/test_verify_integrity.py` | **yes** | `FROZEN-MODIFIED` → HOLD → supervised re-anchor |
| a new `bootstrap/tests/test_fork_advisory.py` | n/a | `FROZEN-NEW` → note, allowed and recorded |
| `bootstrap/UPGRADE.md` | no (`bootstrap/*.py` is non-recursive and matches no `.md`; the only `.md`-reaching glob is `bootstrap/tests/fixtures/**/*`) | free |
| `bootstrap/_scaffold/SECURITY_MUTATIONS.md` | no (same reason) | free |

**Both frozen-file edits are unavoidable and both are non-weakening.**
`verify_integrity.py` must change because the trusted upstream is supplied at the
call site — that is the entire point of the design. `test_verify_integrity.py`
must change because one existing node calls `forked_facade_findings`
positionally (`assert forked_facade_findings(target, lock) == []`) and the new
keyword is required; **its assertions are untouched** — the edit adds one
keyword argument to one call —
which is the same character as the `test_intents_tool.py` precedent already
recorded in `_gate_manifest.py`'s `PHASE_SPLIT_TARGETS` ("ASSERTIONS UNCHANGED").
The Maintainer's falsifiable check is that the diff on that file shows only added
keyword arguments. All *new* nodes go in the new file, never appended to the
frozen one — the lesson from `lockfile-provenance-fields`'s blocking [R2].

**(iii) The engine security gates.** `bootstrap/tests/test_security_lint.py` runs
Bandit over the engine package; the change adds no `subprocess`, no `eval`, no
new file write, and no new dependency (standard library only, per
`bootstrap/DEPENDENCY_BUDGET.md`). `bootstrap/tests/test_security_leaf.py`'s
pinned `_GUARDED_WRITE_FUNCS` set is unchanged, because this change adds no
adopter-tree write.

**(iv) The full suite.** `python -m pytest bootstrap/tests` under the canonical
interpreter, captured as a **live invariant** at implementation time — equal
counts before and after, plus the new nodes. No figure is asserted here; the
plan captures its own pre-edit baseline rather than inheriting a stale one.

### Author-accounting — invariants, failure modes, edge cases

* **Invariants.**
  * **F1** (subset property, above) — enforced by a test that runs the fixture
    matrix through both the `upstream=None` path and the trusted-upstream path
    and asserts the second's finding set is a subset of the first's.
  * **F2** — the trusted upstream is never derived from `target` or from lock
    data. Enforced by the target-supplied-lookalike test and by the
    `src`-relabelled test: neither can suppress a note.
  * **F3** — the advisory never changes an exit code. Enforced by a test
    asserting `verify_integrity.verify(target) == 0` with a live finding
    present. This test doubles as R5's mechanical trigger.
  * **F4** — a caller cannot omit the comparison source. Enforced by a test
    asserting `TypeError` on the positional two-argument call.
* **Failure modes.** The advisory is a **fail-loud** surface: every degradation
  path (no trusted map row, missing file, containment refusal, `--to <ref>`,
  `upstream=None`) **retains** the finding under the `unconfirmed` kind rather
  than dropping it. The only path that removes a finding is a successful
  byte-equality against validated trusted upstream. Containment refusals are
  caught inside `lockfile.py` so a malformed templates tree degrades the advisory
  instead of aborting the verifier — an intentional open edge on an advisory-only
  surface, and the only one.
* **Edge-case inventory.** Handled: `dst` absent from the trusted map; source
  file missing; source is a symlink; source has a symlinked parent; `src_rel`
  absolute or containing `..`; source-version skew in both directions; lock `src`
  disagreeing with the trusted map; a target-planted `templates/` tree; facade
  present with engine absent; engine directory present but holding no `.py`;
  non-`.py` `dst`; record with no `base_hash`; `upstream=None`. Out of scope:
  authenticating the trusted checkout itself (R1); engine-package content
  attestation (item 4 under *does not fix*); a concurrently-mutating templates
  tree (the read is not atomic, and the advisory is not a security boundary).
* **Public-path → test mapping.** Deferred to plan time against real node names,
  written there as relative markdown links so the link checker verifies them.
  The four public paths that must each get a through-test rather than a helper
  test: `forked_facade_findings`, `format_forked_facade_warning`,
  `trusted_upstream`, and `verify_integrity.verify` end-to-end. Naming node names
  now would be a forward reference this proposal cannot verify.
* **Known omissions.** I have not measured the advisory's behaviour on a real
  adopter tree — only on Cairn's self-host and on synthetic fixtures; the two
  differ in that Cairn's `templates/` is co-located with its install. That gap is
  what the fixture matrix exists to cover, and a reviewer should treat the
  fixtures as the evidence rather than the self-host run. I have also not swept
  for *other* consumers of `base_hash` that inherit the same ratchet; that sweep
  is named, not claimed.

### Tests required

All new nodes land in a **new** `bootstrap/tests/test_fork_advisory.py`
(`FROZEN-NEW`, allowed and recorded), importing existing fixture helpers rather
than duplicating them. The matrix [IDN4] requires, plus the invariant guards:

1. **No false positive** — a facade byte-identical to its trusted template
   source emits **no** note, even when `hash != base_hash`. (The headline
   regression; reproduces today's two live false notes as a fixture.)
2. **Source-version skew** — a trusted upstream whose `cairn_version` /
   `cairn_commit` differ from the lockfile's: the skew line fires, the finding
   set does not grow (F1), and a byte-identical facade is still suppressed.
3. **Unsafe source paths** — four nodes: `src` absolute; `src` containing `..`;
   source is a symlink; source has a symlinked parent. Each: comparison refused,
   finding **retained** as `unconfirmed`, never suppressed, no exception escapes.
4. **Missing source** — `dst` absent from the trusted map, and source file
   absent: `unconfirmed`, finding retained.
5. **Target-supplied lookalike template** — the target tree carries its own
   templates directory holding a file byte-identical to its forked facade,
   **and** the lockfile's `src` is re-pointed at it. The note is **not**
   suppressed, and `src_relabelled` fires. This is the [IDN4] regression proper.
6. **Both facade/engine layouts** — facade + populated engine dir (finding);
   facade + no engine dir (no finding); engine dir present but empty of `.py`
   (no finding); non-`.py` `dst` (no finding).
7. **F1 subset property** over the whole matrix.
8. **F3** — exit code unchanged with a live finding.
9. **F4** — `TypeError` on the positional call.
10. **Both callers** — `verify_integrity` honours `fork_acknowledged`; `upgrade`
    does not; the `--to <ref>` path yields `unconfirmed`.

### Examples / smoke checks

* `python bootstrap/verify_integrity.py --target .` — **zero** fork notes on
  Cairn's own clean tree (today: two). The end-to-end demonstration.
* `python bootstrap/scaffold.py --manifest` — row count unchanged (a live
  invariant; the plan captures the pre-edit number).
* `python bootstrap/tests/_ast_attest.py verify …` — the 3-CHANGED target above,
  before the supervised re-anchor; 0 after.
* `python bootstrap/tests/_gate_manifest.py verify` — exactly 2
  `FROZEN-MODIFIED` holds (`bootstrap/verify_integrity.py`,
  `bootstrap/tests/test_verify_integrity.py`), 1 `FROZEN-NEW` note, plus
  `COLLECTION-ADDED` notes for the new nodes. Any third hold is a stop.
* `python scripts/check_cairn.py` and `python scripts/claim_check.py` — for the
  `UPGRADE.md` and `SECURITY_MUTATIONS.md` prose.

## Residuals and proposed expiry triggers

Per the Maintainer's second anti-debt condition — *"Each successor's Decision
states its residuals with an expiry trigger"* — reusing the pattern
`gate-reanchor-preflight` established, which distinguishes **mechanical**
triggers (a check that fires on its own) from **non-observable** ones, and which
records each residual **where it will actually be read** rather than in a
proposal that archives.

**Dated posture.** All of the below are scoped to Cairn as it stands
`as_of 2026-08-03`: single maintainer, pre-first-external-adopter, self-hosting
tree with `templates/` co-located with the install. They are not standing
assumptions.

| # | Residual | Trigger | Kind | Durable home |
|---|---|---|---|---|
| **R1** | The comparison bytes are only as trustworthy as the checkout hosting the verifier. This change makes the source caller-controlled, not cryptographically anchored. | Resolved when the release-authenticity successor lands an out-of-band trust bootstrap. Re-opened on the first Cairn install verified from a checkout the adopter did not obtain themselves. | non-observable | the note string itself (it prints the root and ref it compared against, so an operator sees whose bytes decided it) + `bootstrap/UPGRADE.md` + a `dev/PLANNING.md` row opened at **plan-open** |
| **R2** | `base_hash` still ratchets for `unconfirmed` records; `--finalize`'s backfill is unchanged. | The next change touching `--finalize`'s `base_hash` backfill (observable in review), **or** the first adopter report of a persistent note on a tree where a trusted upstream *was* available. | half-mechanical | a `#` comment at the backfill site in `bootstrap/_scaffold/upgrade.py` (AST-invisible, no delta) |
| **R3** | `upgrade --to <ref>` gets `unconfirmed` semantics only — the ref's template bytes are not materialized. | When any caller materializes a ref's templates for comparison, **or** the first adopter report. | mechanical (the note says so on every `--to` run) | the note string + `bootstrap/UPGRADE.md` |
| **R4** | Destinations absent from the trusted install manifest — adopter-authored files, `--adopt-module` forks — keep `unconfirmed` semantics. | When the fork-entry recorder gains a trusted-source pointer, **or** when the manifest gains adopter-declared rows. | mechanical (a test pins the `unconfirmed` kind for an unmapped `dst`) | the test + `bootstrap/UPGRADE.md` |
| **R5** | `fork_acknowledged` remains a target-controlled verify-time opt-out. Tolerable only while the advisory is advisory. | **Mechanical**: F3's test asserts the advisory never changes an exit code. The moment someone makes it blocking, that test fails, forcing the opt-out to be re-evaluated in the same change. | mechanical | the F3 test |
| **R6** | A write-flavoured containment guard (`_assert_safe_write`) is reused on a read path; its message would read oddly if it ever surfaced. | The **second** read-side caller — at which point it is renamed to a neutral containment primitive in the security leaf. | non-observable | a comment at the call site in `bootstrap/_scaffold/lockfile.py` |
| **R7** | The `SECURITY_MUTATIONS.md` **Class C** follow-on (RR6/SR6) is **not claimed** by this scope, and scope 1 has independently declined it too — the joint disposition above, which departs from the Decision's *Carried forward* and needs Maintainer ratification. Until that ratification the follow-on is **unowned**, and this row is the only thing holding it. | Three, and the **first** to occur discharges it: **(a)** the Maintainer's ratification at the first successor Decision, which either opens Class C as its own proposal or assigns it — this is the intended discharge and the one the disposition asks for; **(b)** the next change that adds or modifies an adopter-tree write in `bootstrap/_scaffold/upgrade.py` — the condition `SECURITY_MUTATIONS.md`'s own closing line already names ("Re-take the inventory if a future stage adds an adopter-tree write"); **(c)** **backstop: v0.4.0 release preparation.** A follow-on that is still unowned when a release is being cut is the debt state, not a posture, and at that point it is opened cold or explicitly closed as won't-fix with a reason. | half-mechanical — (a) and (c) are calendar-independent events on the Maintainer's own path; (b) is observable in review | one sentence in `SECURITY_MUTATIONS.md`'s Class C section recording the decline, the departure and all three triggers, plus a `dev/PLANNING.md` row opened at **plan-open** |
| **R8** | `AGENTS.md`'s operational-pitfall entry routes the AST-baseline re-anchor to `bootstrap/REANCHOR_RUNBOOK.md`, which never governs it. Identified, deliberately **not** fixed here (governing layer, different contract). | Already met on the recurrence limb: **three** artifacts now record it (the `adopter-licensing-compliance` plan review, the `lockfile-provenance-fields` plan's Chunk G, and this proposal), `as_of 2026-08-03`. Routed to a doc-correction commit or the next proposal touching that list. | mechanical — `grep -n -iE 'ast_attest\|scaffold_ast_baseline' bootstrap/REANCHOR_RUNBOOK.md` returns zero hits (re-run against the working tree 2026-08-03; the runbook is under concurrent edit by another session, so a re-check before acting is cheap) | a `dev/PLANNING.md` row opened at **plan-open** |

**Rejected as a trigger: a calendar timer.** For the same reason
`gate-reanchor-preflight` rejected one — a refusal that fires on the calendar is
a refusal the operator learns to route around, and it says nothing about whether
the condition actually changed.

**Why plan-open and not archive.** An accepted proposal archives, and archived
proposals are not read. Every non-observable residual above therefore opens its
`dev/PLANNING.md` row at plan-open, so the row exists before this proposal stops
being read. That mechanic is `gate-reanchor-preflight`'s, adopted wholesale.

## Signals the change is wrong

* **F1 is breakable.** If a reviewer constructs a tree where supplying a trusted
  upstream *adds* a finding that `upstream=None` would not produce, the subset
  property is not an invariant and the central safety argument collapses.
  Recovery: make the trusted-upstream path strictly suppression-only in code
  (compute the legacy finding set first, then filter), rather than relying on the
  branch structure to preserve it.
* **The trusted map is not actually trusted.** If a reviewer shows a path by
  which `install_manifest()`'s output can be influenced by the target — a profile
  read from the target tree, a module list derived from lock data — then the
  design has the same defect it was written to fix, one level up. Recovery: pass
  an explicitly-enumerated map from each caller rather than deriving it.
  **This is the finding I would most expect a security reviewer to land**, and it
  is the right place to attack this proposal.
* **The note is now too quiet.** If a genuinely stale facade stops being reported
  because it happens to match a *newer* upstream the adopter never installed, the
  suppression rule is wrong even though F1 holds. Recovery: gate suppression on
  the absence of version skew rather than on byte-equality alone.
* **Two frozen-file edits are judged too expensive.** If the Maintainer judges
  the supervised gate re-anchor disproportionate for a false-positive fix,
  the design should be reshaped so `verify_integrity.py` does not change —
  which, on my reading, forces the comparison source back into the engine and
  reintroduces the ambiguity [IDN4] blocked. Recovery: say so explicitly and
  defer the whole scope rather than take the cheaper, worse shape.
* **The `unconfirmed` kind is where everything lands.** If, in practice, real
  adopter trees almost never resolve a trusted upstream, this change relabels the
  noise rather than removing it. Recovery: measure on a real adopter install
  before the plan's final chunk, and if the rate is high, reconsider whether the
  advisory earns its place at all.

## Review -- Gemini Flash (External, Security Review) -- 2026-08-03

**Model**: Gemini 3.6 Flash (External, different-agent-type)
**Verdict**: SHIP (recommend ACCEPT; verified claims a–c, verified complete target-independence of caller-supplied comparison source)

### Steelman

This proposal satisfies the core Cairn integrity invariant: *"The artifact under verification must not supply the material used to verify it."* By refactoring `forked_facade_findings` to take a required, keyword-only `upstream: UpstreamSource` parameter with no default value, the proposal forces callers to supply their own trusted upstream template root and destination-to-source mapping.

The design completely removes the lockfile's `src` field from comparison path resolution—using it only to detect and flag relabeling tamper attempts—and builds `src_for_dst` from static engine mappings (`install_manifest(modules=None)`). This closes the vulnerability where a target tree could point the verification logic at a lookalike or target-planted template file.

### Concerns and Findings

* **[G1] (Verification of Claims a, b, and c)**
  * **Claim (a) — SHA-256 Byte-Identity of `tools/intent.py` Twins:**
    Verified under Python 3.13.13. `tools/intent.py` and `templates/modules/team-gated/intent.py` are byte-identical.
    * *Command:* `~/conda_envs/lhm/bin/python -c "import hashlib, pathlib; h1 = hashlib.sha256(pathlib.Path('tools/intent.py').read_bytes()).hexdigest(); h2 = hashlib.sha256(pathlib.Path('templates/modules/team-gated/intent.py').read_bytes()).hexdigest(); print('tools/intent.py:', h1); print('templates/modules/.../intent.py:', h2); print('Identical:', h1 == h2)"`
    * *Output:*
      ```
      tools/intent.py: 6462d4041d5d88d1013a88b02d2c52a28523472899ddc8fde3ad51491a016e03
      templates/modules/.../intent.py: 6462d4041d5d88d1013a88b02d2c52a28523472899ddc8fde3ad51491a016e03
      Identical: True
      ```
  * **Claim (b) — Runtime Load of `tools._intent.*` Package:**
    Verified under Python 3.13.13. All 7 modules in `tools._intent/` load without error.
    * *Command:* `~/conda_envs/lhm/bin/python -c "import importlib, pathlib; pkg = pathlib.Path('tools/_intent'); files = sorted([p.name for p in pkg.glob('*.py')]); print('Files:', files); imported = [importlib.import_module('tools._intent.' + f[:-3] if f != '__init__.py' else 'tools._intent').__name__ for f in files]; print('Loaded:', len(imported), imported)"`
    * *Output:*
      ```
      Files: ['__init__.py', 'cli.py', 'conflict.py', 'hooks.py', 'identity.py', 'record_io.py', 'shared.py']
      Loaded: 7 ['tools._intent', 'tools._intent.cli', 'tools._intent.conflict', 'tools._intent.hooks', 'tools._intent.identity', 'tools._intent.record_io', 'tools._intent.shared']
      ```
  * **Claim (c) — Documentation of `--finalize` `base_hash` Backfill:**
    Verified in `bootstrap/_scaffold/upgrade.py:1624-1628`. The docstring explicitly documents that `--finalize` preserves `base_cache` / `base_hash` and copies `hash` to `base_hash` for records predating `base_hash`.

* **[G2] (Deep Security Evaluation — Target Independence Trace)**
  * *Question:* Can the target tree being checked (`target`) influence the comparison source?
  * *Trace of Caller 1 (`bootstrap/verify_integrity.py`):*
    1. Resolves `CAIRN_ROOT = Path(__file__).resolve().parent.parent` from the location of `verify_integrity.py` itself (the runner checkout).
    2. Builds `upstream = trusted_upstream(CAIRN_ROOT)` where `templates_root = CAIRN_ROOT / "templates"` and `src_for_dst` comes from `install_manifest(modules=None)`.
    3. `install_manifest(modules=None)` evaluates static in-memory Python structures (`_CORE_MAPPINGS`, `_SKILLS_MAPPINGS`, `_ALWAYS_ON_MAPPINGS`, `_MODULE_MAPPINGS` in `config.py`). It reads zero files from `target`.
    4. Inside `forked_facade_findings`: `target` is used to locate `target / dev/.cairn/cairn-lock.yml` and read target files on disk. `rec["src"]` from `target`'s lockfile is ignored for path resolution. `rec["dst"]` is used as a lookup key in `upstream.src_for_dst`.
    5. If `rec["dst"]` is not in `src_for_dst`, `src_rel` is `None` -> degrades to `unconfirmed` (no template read, no suppression). If `rec["dst"]` is in `src_for_dst`, `src_rel` is hardcoded by the engine. `template_path = upstream.templates_root / src_rel` is validated via `_assert_safe_write` inside `upstream.templates_root`.
  * *Trace of Caller 2 (`cmd_upgrade` in `bootstrap/_scaffold/upgrade.py`):*
    1. `cairn_root` is resolved from CLI `--cairn-root` or `_cairn_root()` (`Path(__file__).resolve().parents[2]`). Neither reads `target`.
    2. If `--to <ref>` is specified, `upstream` is set to `None`, falling back to `unconfirmed` without reading templates.
  * *Verdict:* **ZERO target-influence paths exist.** The comparison source is strictly caller-controlled and target-independent.

* **[G3] (Coordination with Trivial Remediation String Commit)**
  Confirming the proposal's coordination recommendation: because `format_forked_facade_warning` is edited by both the trivial remediation fix and this proposal, the trivial commit should land first (or be absorbed into this plan's Chunk 1) to avoid invalidating the AST attestation baseline on `lockfile.py`.

### Covered (Lenses Swept & Verbatim Executions)

Executed under canonical interpreter `~/conda_envs/lhm/bin/python` (Python 3.13.13).

1. **Byte-Identity Check (`tools/intent.py` vs `templates/modules/team-gated/intent.py`):**
   * *Command:*
     ```bash
     ~/conda_envs/lhm/bin/python -c "import hashlib, pathlib
     h1 = hashlib.sha256(pathlib.Path('tools/intent.py').read_bytes()).hexdigest()
     h2 = hashlib.sha256(pathlib.Path('templates/modules/team-gated/intent.py').read_bytes()).hexdigest()
     print('tools/intent.py sha256:                    ', h1)
     print('templates/modules/team-gated/intent.py sha256:', h2)
     print('Byte identical:', h1 == h2)
     "
     ```
   * *Output:*
     ```
     tools/intent.py sha256:                     6462d4041d5d88d1013a88b02d2c52a28523472899ddc8fde3ad51491a016e03
     templates/modules/team-gated/intent.py sha256: 6462d4041d5d88d1013a88b02d2c52a28523472899ddc8fde3ad51491a016e03
     Byte identical: True
     ```

2. **Runtime Import Check (`tools._intent.*` package):**
   * *Command:*
     ```bash
     ~/conda_envs/lhm/bin/python -c "import importlib, pathlib
     pkg = pathlib.Path('tools/_intent')
     files = sorted([p.name for p in pkg.glob('*.py')])
     print('Files in tools/_intent:', files)
     imported = []
     for f in files:
         mod_name = 'tools._intent.' + f[:-3] if f != '__init__.py' else 'tools._intent'
         mod = importlib.import_module(mod_name)
         imported.append(mod.__name__)
     print('Loaded modules (count:', len(imported), '):', imported)
     "
     ```
   * *Output:*
     ```
     Files in tools/_intent: ['__init__.py', 'cli.py', 'conflict.py', 'hooks.py', 'identity.py', 'record_io.py', 'shared.py']
     Loaded modules (count: 7 ): ['tools._intent', 'tools._intent.cli', 'tools._intent.conflict', 'tools._intent.hooks', 'tools._intent.identity', 'tools._intent.record_io', 'tools._intent.shared']
     ```

3. **Docstring Inspection (`bootstrap/_scaffold/upgrade.py:1624-1628`):**
   Opened file `bootstrap/_scaffold/upgrade.py` and inspected lines 1624-1628 confirming exact wording regarding `base_hash` backfill logic.

### Not Covered / Low Confidence (Negative Space)

* **Un-Patched Code Verification:** The proposed refactoring of `lockfile.py`, `install.py`, and `upgrade.py` has not been implemented in code yet; all verifications were conducted against the current un-patched codebase and proposal text.
* **Out-of-Band Checkout Authenticity (R1):** This review confirms that the target tree cannot influence the comparison source, but does not verify that the runner's checkout (`CAIRN_ROOT`) is cryptographically authentic. That trust boundary is explicitly assigned to Scope 1 (`release-authenticity`).

## Decision -- {{Maintainer}} -- {{YYYY-MM-DD}}

*(Awaiting the Maintainer. The proposal has cleared External Security Review. The Maintainer may accept the proposal to proceed with plan creation.)*

## Addendum — 2026-08-03 — the mechanical reason Class C was dropped

> **This addendum is worded identically in scope 1 (`release-authenticity`), for the same reason
> the *Class C* section above is: the two proposals must not be readable as
> disagreeing about the disposition or about how it is held.** It is *appended*
> rather than folded into that section because that section is committed
> lifecycle record. It states what its authors believed when they wrote it —
> before anyone had measured whether the mechanism they proposed is the kind of
> mechanism that holds. Rewriting it would erase that, so the correction is a
> later section.

**What this adds.** The *Class C* section above establishes *that* the follow-on
was documented, routed, and never opened, and takes from it the lesson that
"naming a home is what failed last time." It does not say **why** naming a home
failed. A later audit proposed a mechanical answer. I re-measured it rather than
adopting it on report, and the measured version is stronger and more specific
than the reported one. The disposition does not change; the strength ranking of
the parts holding it does, and one drafting defect in the mechanism surfaces.

### The measurement

Two forms have to be kept apart, and the distinction is the finding.

* **The commit-body form** is what the doctrine actually requires. Cairn's
  archive precondition says the archive commit *body* must name where each
  deferred item went, in a literal `Follow-ups migrated to:` block — the stated
  purpose being that the migration is auditable from the commit log alone
  (`doctrine/proposals.md:370`).
* **The in-file form** is what the only checker in the tree actually looks for:
  a `Follow-ups migrated to:` block inside the artifact.

Measured on this repository, `as_of 2026-08-03`:

* **Commit-body form: 0 of 9** archived plans and **0 of 12** archived proposals.
  Across the entire history exactly one commit message contains the phrase, and
  it is the commit that *introduced* the doctrine, not an archive commit. Plans
  record the migration in prose instead ("Lasting-truth migration: … moved to
  `dev/PLANNING.md` > Queued"). Neither side satisfies the doctrine as written.
* **In-file form: 7 of 9** archived plans carry the block; **1 of 12** archived
  proposals do. The single compliant proposal is a *superseded* one that carries
  the block inside its own Decision section — hand-written, in a Decision commit
  that also performed the archive move.

Method, so this is re-runnable rather than asserted: for the in-file form,
`grep -rl` for the phrase across `dev/plans/archive/` and
`dev/proposals/archive/`; for the commit-body form, for each archived file the
commit that added it at its archive path, then that commit's message body. The
7-of-9 / 1-of-12 figures reproduce the audit's exactly. The commit-body figures
are new here.

### The mechanism, and it is not carelessness

`tools/lifecycle_planner.py` — with its byte-parity twin shipped under
`templates/skills/_lib/` — is the only place in the tree where this precondition
is checked at all. Two facts about it:

* The parser computes the field for **every** artifact, plan or proposal; it is
  kind-independent (`tools/lifecycle_planner.py:488`).
* The *check* is not. It sits inside the plan branch's archived-status arm
  (`tools/lifecycle_planner.py:654`). The proposal branch has no counterpart.

And in the current model it cannot have one, which is the real finding.
`archived` is a plan status; it is **not** a proposal status. The proposal state
tuple (`tools/lifecycle_planner.py:501`) runs `proposed → reviewed → revised →
accepted / rejected / superseded` and stops there; the transition table returns
the empty list from `accepted`, carrying an inline comment that says why — the
archive move is a file operation, not a status flip. There is therefore no
proposal state for an archive-time precondition to attach to. On the proposal
side the gate is not lax. It is **structurally absent**.

That asymmetry is visible in one pair of commands (output abridged,
`as_of 2026-08-03`):

```
$ python tools/lifecycle_planner.py next dev/plans/archive/interpreter-trust-root-fallback.md
lifecycle-planner: current state: archived
lifecycle-planner: VIOLATION: status is 'archived' but no 'Follow-ups migrated to:'
                   block is present (archive precondition).

$ python tools/lifecycle_planner.py next dev/proposals/archive/2026-07-11-claude-record-corrections.md
lifecycle-planner: current state: accepted
   ... three VIOLATIONs reported, none of them about follow-ups ...
lifecycle-planner: (terminal state -- no status transition; any archive move is a
                   file operation, not a status flip.)
```

An archived plan missing its migration block is told so by name. An archived
proposal missing its migration block is told about three unrelated things and
then told the archive is not a transition. (Both artifacts are cited by path in
the transcript because they are literal command arguments; in prose they are the
`interpreter-trust-root-fallback` plan and the `record-corrections` proposal.)

### What this corrects

The superseding Decision's condition 1 in `identity-not-name` diagnosed the loss
this way: the existing archive-precondition rule *"is satisfied by a roadmap
row, and a roadmap row is where `SECURITY_MUTATIONS.md`'s Class C gap went."*
That is right about the outcome and it understates the cause. The rule is not
merely satisfiable by a weak home on the proposal side — on the proposal side it
is not applied at all, and 1-of-12 is what that looks like from outside. Class C
did not slip past a permissive gate. It was routed to the one half of the
lifecycle where the gate does not run.

This is a correction *in favour of* condition 1's instinct, not against it. The
condition was written against the right failure; the failure is worse than
stated.

### Does the anti-drop mechanism inherit the weakness? Yes

Stated plainly, because the *Class C* section above rests on it. The mechanism
proposed there is a `dev/PLANNING.md` row landed in the first successor's
Decision commit. That is **a roadmap row on the proposal side of the lifecycle**
— the same class of object, on the same side, as the one that lost Class C. On
this measurement it is not a stronger mechanism than the one that failed; it is
the same mechanism.

The inheritance is not total, and the two refinements both cut the same way:

* The row lands at **Decision**, not at archive, and `accepted` / `rejected` /
  `superseded` *are* modeled proposal states that the checker validates. So the
  moment is one the tooling can see. But the terminal-state validation checks
  three things — that a `## Decision` section exists, that it carries an isolated
  verbatim-authorization blockquote, and that its byline classifies as a known
  human Maintainer — and follow-up migration is not among them. The row is
  unenforced at precisely the moment it is supposed to land.
* Nothing later can catch its absence. The transition table returns no legal
  target from `accepted`, so there is no subsequent modeled event at which a
  missing row becomes visible to anything.

The row's only guarantee is that a human remembered. That is exactly the
guarantee Class C already had, and it is the guarantee that failed.

### A second defect in the mechanism as written, found while checking this

The *Class C* section says the disposition "lands as a `dev/PLANNING.md` row in
the Decision commit of whichever successor is decided first." `AGENTS.md`'s
scribing guard-rail says a scribed Decision commit flips the status and appends
the Decision section *"and nothing else — no implementation, plan-open, archive,
or roadmap work rides in a scribed Decision commit."* A `dev/PLANNING.md` row is
roadmap work.

This is not hypothetical. The Decision that spawned these four scopes was itself
scribed: commit `6c6ce39` opens "Scribed by Claude (Strategy) at the Maintainer's
explicit instruction" and closes by attesting "no plan-open, **no board edit**,
no implementation." A `dev/PLANNING.md` row would have been excluded from it by
the rule the scribe was following.

So the mechanism as drafted is executable only when the Maintainer types the
Decision commit themselves. If it is scribed — the immediately preceding
precedent — the instruction is either to drop the row or to break the
guard-rail, and neither is what the section intends. This is a drafting defect
in the mechanism, not a problem with the guard-rail. The fix is cheap and is the
Maintainer's to choose: land the row in a **separate, immediately-following**
commit (a one-file `dev/PLANNING.md` commit, which the git-workflow carve-out
already lets land without per-commit approval), and have the Decision section
name that commit as its discharge.

### What would have to change for the row to actually hold

Three components are on the table. The *Class C* section lists them in what this
measurement shows is the wrong order of strength. Corrected ordering, strongest
first:

1. **Extend condition 1 — the only *blocking* component, and already option 1's
   real content.** Option 1 proposes that `identity-not-name` not archive until
   Class C is opened. That is not a row; it is a precondition on an act only the
   Maintainer performs. No tool enforces it either — but its holder is the one
   role that cannot delegate the archive, and its failure mode is a visibly stuck
   artifact rather than a silent missing line. On this measurement the
   *condition* is the load-bearing half of option 1, not the "open a proposal"
   half. Only the Maintainer can add it.
2. **The `SECURITY_MUTATIONS.md` sentence — stronger than the row, and it should
   have been named first.** It sits in the file that an engine change forces
   someone to open, and that file's own closing line already carries a
   re-inventory instruction firing on exactly that event — the trigger scope 3's
   residual **R7** names as its (b). A durable home on a path someone *must*
   walk beats a durable home on a board someone *might* scan. Concrete
   recommendation to the Maintainer: **if only one of the two is landed, land the
   sentence.**
3. **Wire the proposal side — named here, explicitly not taken here.** The
   parser already computes the field for both artifact kinds; what is missing is
   a proposal-side check and a modeled state for it to attach to. That is a
   change to `tools/lifecycle_planner.py` plus its byte-parity template twin, it
   touches the shipped lifecycle contract that adopters install, and on the
   numbers above it would immediately flag 11 of the 12 already-archived
   proposals — which is a disposition question about historical artifacts, not a
   code question. It is proposal-sized. Naming it is the correct treatment;
   taking it as a rider on either successor would repeat exactly the
   four-gate-sets-in-one-artifact failure the split exists to prevent. Recorded
   so whoever opens Class C, or whoever next touches the lifecycle checker,
   finds it rather than rediscovers it.

### What this addendum does not establish

* **It does not establish that the plan side works.** The checker is a read-only
  reporter run at session-start, not a CI gate — it reports, it does not block.
  And 0-of-9 on the commit-body form says the plan side fails the doctrine's own
  stated requirement too. Both sides are out of conformance with the archive
  precondition as written; the difference measured here is that only one side is
  ever *told*.
* **It does not prove this is why Class C specifically was lost.** It establishes
  that the check which should have caught it does not run on that side of the
  lifecycle. That is a sufficient and checkable explanation. Whether some further
  factor also contributed is not measured, and no claim is made that it did not.
* **It does not establish that a `dev/PLANNING.md` row never works.** Rows have
  carried follow-ups in this repository. It establishes that a row is the weakest
  of the three components on offer, and that this particular item has already
  been lost from one.
* **It does not change the disposition.** Both authors still decline Class C, for
  the reasons recorded above, and the three options put to the Maintainer are
  unchanged. What changes is the strength ranking in the anti-drop paragraph and
  the commit mechanics for the row.

### Status

**No status change.** This is an append to a proposal still in `proposed` status
with no review yet; it requests no re-review, adds no scope, changes no
deliverable, and moves no residual. A reviewer reading top-to-bottom should treat
this addendum's ordering — condition, then `SECURITY_MUTATIONS.md` sentence, then
row — as superseding the ordering in the *Class C* section's anti-drop paragraph,
and should treat the separate-commit note above as superseding "in the Decision
commit" there.
