<!-- Author tip: numeric claims follow the three-kind precision /
     `as_of` discipline -- approximate a decision-irrelevant count
     (`~4900 lines`), date a snapshot (`N, as_of YYYY-MM-DD`, never
     re-measured), register a live invariant; never quote one from
     memory.  See `doctrine/proposals.md` > "Count claims".  (The old
     `claim_check` count soft-flag + `claim-check-allow-count`
     directive were retired 2026-06-05 -- claim_check no longer flags
     counts.) -->

# Proposal template

> **This is the proposal template.** To open a proposal, copy the
> section template below the horizontal rule into
> `dev/proposals/<YYYY-MM-DD>-<author>-<short-slug>.md`, fill it,
> and commit it with status `proposed`. The lifecycle, triage,
> forward-reference-path, file-move, archive-precondition, count-claim,
> and Response-grammar doctrine above the rule live in
> `doctrine/proposals.md` — read it once, then work from the
> sections below.

## The lifecycle

See `doctrine/proposals.md` > "The proposal lifecycle" for the full
lifecycle diagram, the append-only rule, and the one-commit-per-transition
rule.

Two rules are bright-line: **append-only** (earlier sections are immutable;
append new content below the existing arc) and **one commit per transition**
(open, review, response, decision each land as their own commit).

The directory location encodes **work-status**; the `Status:` field encodes
**deliberation state**. Two orthogonal axes. See
[`dev/plans/_template.md`](../plans/_template.md) for the plan
counterpart and the trivial-vs-non-trivial triage rule.

## Triage: trivial vs. non-trivial

See `doctrine/proposals.md` > "Triage: trivial vs. non-trivial" for the full
triage rule and the escape hatch.

Open a proposal when the change touches a public API or config contract,
introduces a new abstraction, moves files, revives a proposal-worthy deferred
follow-up, or has implementation tradeoffs worth a second opinion. Everything
else — a new helper, a test, a typo fix, a self-contained refactor — just
commit.

**Escape hatch, local copy** (a short gloss alongside the pointer above, not
a substitute for it — see `doctrine/proposals.md` for the full rule): if a
change is urgent, clearly reversible, or explicitly experimental, it may
proceed without a proposal, but the commit or follow-up note should say why
the proposal step was skipped. *Sync note:* this gloss is a duplicate of
`doctrine/proposals.md`'s escape-hatch paragraph; if that doctrine text is
ever revised, re-sync this copy in the same change. *Port-exemption note:*
this text predates Cairn's own self-hosting (introduced 2026-06-08, four
days before the 2026-06-12 adoption) — there is no discrete `dev/` Decision
to cite for it.

<!-- cairn:slot triage-extra-triggers -->
Cairn guards several protected contracts — a change touching any of
these opens a proposal regardless of size:

* **Invariant-kernel or doctrine change** — anything under
  `doctrine/`, the dimension matrix / module gate-table (`dimensions/`,
  `bootstrap/BOOTSTRAP.md`), or the framework anchors in
  `doctrine/rationale.md`. The kernel is what makes a thing Cairn at
  all; it does not move silently, and a doctrine change additionally
  clears the doctrine-evolution rate-limit below.
* **Bootstrap fidelity / install contract** — the scaffold's install
  set, the fidelity manifest (`bootstrap/fidelity-check.md`), the gate
  manifest, the lockfile schema, or the published install manifest
  (`scaffold.py --manifest`). Adopters depend on these.
* **Vendor-neutrality boundary** — introducing a model / vendor name
  into doctrine or a template (the `quality_gate.py --sub neutrality`
  surface). The deliberation record may name reviewers; shipped
  doctrine may not.
* **Bootstrap safety / security stack** — `bootstrap/SAFETY.md` (R-I),
  `bootstrap/security_check.py`, or the content scanner; a change here
  is also a Security Review trigger.
* **Licensing / provenance** — the by-file license split or
  `bootstrap/PROVENANCE.md`.
<!-- cairn:end triage-extra-triggers -->

## Forward-reference paths — `Proposed paths:` marker doctrine

See `doctrine/proposals.md` > "Forward-reference paths" for the full
marker mechanism, placement rules, and the two other marker keywords
(`Untracked paths:`, `External-repo paths:`).

Use the marker when the proposal cites paths it plans to create, future
test / fixture / documentation files, or a future archive path. Place it
near the top of the proposal; the marker exempts tokens on its own line
and any contiguous structured block immediately beneath it.

**The marker block is also a small document registry.** Every *exact*
backticked path listed in the block may recur anywhere else in the same
document without a second, document-wide `claim-check-allow` directive. Write
the declaration in registry form and you will rarely need the directive at all:

    Proposed paths:
    * `tests/test_widget_contract.py` -- the acceptance tests
    * `docs/widget-tour.md` -- the topic doc this lands

What counts as an entry: on the marker line itself, **every** backticked token
(the compact ``Proposed paths: `a.md`, `b.md` `` form); on a continuation row,
the row's **first** backticked token only -- a row names one path and then
explains it, so a path cited later in that row's prose is a reference, not a
second declaration.

Four rules keep the registry exact, and each fails **closed**:

* **Literal paths, never globs.** A wildcard makes the entry *malformed*: it
  grants no document-wide authority at all.
* **Exact match only** -- never a sibling, a descendant, or a look-alike prefix.
* **A placeholder declares nothing.** A token carrying `<slug>` or a brace is an
  illustrative form, not a declaration -- so write the real path when you mean
  to register it.
* **Declared twice inside one block** is a duplicate and grants nothing. The
  same path in two *different* blocks is fine: an append-only record whose
  later section restates its proposed paths is doing the right thing.

**An exemption is temporary debt, and liveness says so.** While this artifact is
non-terminal, every registry entry must authorize at least one exemption
*outside its own block*; an entry whose path has since materialized -- or that
nothing outside the block cites -- is a hard finding, as is a
`claim-check-allow` glob that suppresses nothing. Every exemption is reported
together with the declaration that authorized it, so the audit trail is the
report, not a reading of the file.

## File moves

See `doctrine/proposals.md` > "File moves" for the full rule on when the
archive move is decoupled from the Decision-status flip (accepted proposals
stay in `dev/proposals/` until plan-open or the trivial-implementing commit)
and when it is bundled (rejected / superseded proposals archive in the
Decision commit itself).

## Archive preconditions

See `doctrine/proposals.md` > "Archive preconditions" for the rule that every
deferred follow-up must carry a recorded disposition before archiving —
`accept`, `guard`, `wontfix`, or (with the Maintainer's quoted authorization)
`defer` — the acceptable `defer` homes, the required `Dispositions:`
commit-body form, and guidance on deferred-follow-up wording.

## Assurance paths — declare one, and know which triggers are mandatory

Every proposal declares an **assurance path** in its header, `standard` or
`high-assurance`. The declaration decides which independent boundaries the
change receives, so it is stated once, in the metadata block, and never left to
be inferred from the topic.

`high-assurance` is **mandatory** when the change affects:

* a security trust boundary, credential, executable path, untrusted-input
  parser, network boundary, or protected surface named in `AGENTS.md`;
* a scientific assumption, transformation, unit/CRS convention, numerical
  method, or data-selection rule that can change reported results;
* a destructive migration, data-loss risk, public compatibility break, or
  release/trust ceremony;
* governing doctrine or lifecycle enforcement; or
* a concern escalated by a reviewer or the Maintainer.

**Uncertainty resolves to `high-assurance`.** An author may escalate freely; a
*downgrade* requires a recorded Maintainer Decision. There is no default value
and no silent `standard`: an absent declaration is a finding, not an ordinary
change.

**These are author declarations, not inferences, and no tool can check them.**
The lifecycle planner verifies that the declaration exists and is in vocabulary;
it cannot know whether your change touches a scientific assumption or a trust
boundary. That judgement is yours, it is recorded in your own words, and a
reviewer checks it the way they check any other claim in the proposal.

**What the path does *not* decide: how the derived plan is reviewed.** A
high-assurance declaration governs verification, Security Review, scientific
review, protected-surface handling, risk acceptance and ceremonies. It does
**not** buy a second different-agent-type read of the plan: a high-assurance
proposal may record `Plan readiness: READY` exactly as a standard one may, and
the derived plan then takes a fresh-context **Internal** pass. Where a
high-assurance trigger keeps an independent backstop, it keeps it outside the
plan-review allocation -- a named high-risk surface takes its Security Review on
its own trigger, whatever this field says.

<!-- cairn:slot assurance-path-triggers -->
Cairn's own mandatory high-assurance surfaces, each named in `AGENTS.md` >
"High-risk surfaces" and each already a Security-Review trigger:

* the **scaffold / merge engine** (`bootstrap/scaffold.py` →
  `bootstrap/_scaffold/`) — untrusted module/profile parsing, path handling,
  and writes into a target tree;
* the **install contract** — the fidelity manifest, the gate manifest, the
  lockfile schema, and the published `scaffold.py --manifest`;
* the **local interpreter binding** — `dev/.cairn/local-env.json`, its reader,
  and every call site that executes the path it returns;
* the **portable-sweep executable trust root** —
  `run_portable_security_sweeps.py`, its resolve/revalidate pair, and
  `portable_security_policy.json`;
* **governing doctrine and lifecycle enforcement** — anything under
  `doctrine/`, the lifecycle planner's gate predicates, or the authoring
  templates themselves.

Plus the two non-surface triggers: the **by-file license split**, and the
**vendor-neutrality boundary** (a model/vendor name reaching doctrine or a
shipped template).
<!-- cairn:end assurance-path-triggers -->

## Count claims — the three-kind precision / `as_of` discipline

See `doctrine/proposals.md` > "Count claims" for the three-kind discipline
(decision-irrelevant / dated snapshot / live invariant) and the retired
`claim-check-allow-count` directive.

---

# {{proposal title}}

**Author**: {{name / role}}
**Model**: {{your actual running model — query and state it; don't copy a label from an old template or archive}}
**Date opened**: {{YYYY-MM-DD}}
**Status**: proposed
**Assurance path**: {{standard | high-assurance — the mandatory trigger set is above under "Assurance paths"; there is NO default and uncertainty resolves to high-assurance}}
**Touches**: {{the files / surfaces this changes}}
**Related**: {{roadmap links, prior proposals, commits, issues}}
**Plan review**: {{if non-trivial — required(<tier>) | not required(<rationale>); ratified at Decision}}

## Context

What problem is being solved? What is the felt pain that triggered
this? Cite specific files, commits, or issues.

## Proposed paths

*(Optional. Populate as forward-reference paths accrue — files this
proposal would create, surfaces it would touch into existence — so
they don't trigger `claim_check` while the proposal is being authored.
Each entry is the path **and** a one-line note on what it is / when it
materializes. Remove the section if empty. Once a path resolves on
disk, drop its line.*

*Three structural rules for the marker to work: (a) the literal
`Proposed paths:` line below is the marker `claim_check` matches —
don't drop it while bullets remain; (b) **no blank line between
the marker line and the first bullet** — `claim_check`'s
continuation check uses original line numbers, so a gap breaks
adjacency; (c) **keep each bullet on a single physical line** —
wrapped/indented bullet continuations close the marker block and
re-expose subsequent paths to hard-check.)*

Proposed paths:
- `path/to/proposed/file.md` — what it is; when it lands.

## Proposal

The change, concretely — name files, signatures, contracts. What
is added, changed, or removed.

### Documentation / doctrine surface

What documentation, doctrine, or contract surface does this change
touch? If none, say so explicitly — silent omission is a review
finding.

<!-- cairn:slot documentation-tier-home -->
**Doc tier home rule** — route doc and doctrine changes by layer per
[`docs/DOCUMENTATION_PLAN.md`](../../docs/DOCUMENTATION_PLAN.md):
cross-cutting prescription → governing layer (`AGENTS.md`);
deliberation about what to build → deliberation layer (`dev/`);
description of the software as it is → descriptive layer (`docs/`). A
proposal that omits the doctrine-surface routing is itself a review
finding.
<!-- cairn:end documentation-tier-home -->

### Doctrine-change rate-limit (if this proposal changes doctrine)

If this proposal **changes doctrine** — a rule, process, or
contract every contributor follows — it must clear the
doctrine-evolution gate (`doctrine/rationale.md` > "How the
doctrine evolves under evidence"). Link the justification here:

* the **recurrence** evidence (the same failure shape, ≥2 times in
  a rolling window), or
* the Maintainer's **high-risk classification** (a security or
  data-loss surface), or
* the **goodnight-time synthesis** that aggregated the signal into
  this proposal.

A single incident does not justify a doctrine change unless it is
the high-risk case. *This prompt applies to a proposal that
introduces a **new** doctrine change. A proposal that merely
**syncs or ports already-accepted doctrine** from one place to
another is not itself a new change — it cites the original
accepting Decision and the gate does not re-apply.*

## Rationale

Why this change, and why now — the user-facing or project-facing
improvement it delivers. Per the collaboration agreement's review
checklist:

* Which user workflow does it improve?
* What stable contract or module boundary does it preserve or clarify?
* What domain-specific transparency, reproducibility, or correctness
  does it improve? (if applicable)
* Why is now the right time?

## Alternatives considered

What else was on the table? Why does this win? Naming the alternatives
is more important than picking the best one — it forces the reviewer
to push back at the right level. Include "do nothing". If the draft
incorporates the Maintainer's chat-mode preferences, cite them here
(or in *Rationale*) as **"maintainer preference during drafting"**
with the quote or paraphrase — chat input shapes the draft but is not
the Decision (see `doctrine/lifecycle.md` > "Chat preferences are not
a lifecycle Decision").

## Evidence / verification plan

What proves the change works, and what signal would tell us it's
wrong?

The three things every change accounts for: the **tests** that prove
it, the **examples / smoke checks** that exercise it end-to-end, and
the **docs** it delivers (named earlier under `## Proposal >
Documentation / doctrine surface`). Name each, or give an explicit
"**N/A**: <reason>" — silent omission is a review finding.

### Author-accounting — invariants, failure modes, edge cases

<!-- Triage-gated. Fill this for a HIGH-STAKES change — a scientific /
modeling-assumption change, a public-API or config-contract change, a
protected-schema change, or a new abstraction. For a routine or mechanical
change, a one-line "N/A: no new contract / invariant / public path" is the
correct entry, not an empty table. -->

For a high-stakes change, account up front for what a reviewer would
otherwise have to *discover* — collapsing the review from "find the absence"
to "check this claim":

* **Invariants** — what must stay true (e.g. "the manifest's `schema_version`
  is always a known value"), and what *enforces* each (a validator, a test).
* **Failure modes** — how it fails, and whether each failure is *closed*
  (raises) or *open* (degrades) — and whether the open ones are intentional.
* **Edge-case inventory** — empty / None / zero / single / N≫1 / mismatched
  units or CRS: which are handled, which are out of scope.
* **Public-path → test mapping** — each public entry point this change adds
  or touches, mapped to the test that exercises it *through its public path*
  (not via a helper or a stub). Write the mapping as a **relative markdown
  link** to the test file — target relative to this document, e.g. a link
  whose target is `../../tests/contract/<your_test>.py` — so the link checker
  verifies the cited test exists. (Shown as a bare path here so this template
  itself stays link-clean; in a real proposal, write it as an actual relative
  markdown link to that test file.)
* **Known omissions / intentionally untested edges** — the one line that
  keeps this honest: what you did *not* cover, and why.

This block is **reviewed as evidence, not accepted as a filled form**: the
reviewer challenges at least one row (or names the row they sampled and
verified) — "which invariant has no enforcer? which public path has no
through-test?" — never "the table is present." An empty in-scope block is
itself a finding.

#### Security preflight — five questions, answered in writing

*Gated to a **security-touching** change: one that adds, moves, or widens a
trust boundary (deserialization, subprocess invocation, parsing, file and path
handling, network I/O, credentials and environment — the `security-review`
module's boundary list), or one that touches a high-risk surface this project's
`AGENTS.md` names. For every other change, one line — "N/A: no trust boundary
added, moved, or widened" — is the correct entry.*

Answer all five, one or two sentences each. These are **design questions, asked
while the design is still movable** — not documentation written after it is
fixed. An absent answer is a review finding. A *wrong* answer is a falsifiable
review finding, which is the point: the reviewer checks a stated claim in one
read instead of hunting for an absence over four rounds.

* **S1 — Who supplied it?** For each step where this change *decides* something
  (verifies, authenticates, authorizes, classifies, admits), name every input
  and the channel it arrives by, and say whether any input is supplied —
  directly or **by reference** — by the thing being decided about. Apply this to
  every step in the change *and to every step you describe in prose in this
  document*.
* **S2 — Can it fail?** For each test or check this change relies on to enforce
  an invariant, state the one-line mutation that makes it fail, and confirm you
  ran it. If a check derives what it expects from the same object it is
  checking, say so plainly — that check cannot fail.
* **S3 — What fires it, over what?** Name the command that runs the check, what
  selects it (a preset, a profile, a suite, or nothing), and the exact input set
  it covers. Then quote the sentence in adopter-facing prose that describes it,
  and show the two agree.
* **S4 — Which way does it break?** For each default, fallback, normalization,
  and parse-error path this change adds or touches, say which side of the
  boundary it lands on when it goes wrong — and whether that is *more* authority
  or less.
* **S5 — Who still wins?** State the attacker capability this change assumes,
  then name one capability that still succeeds after it. If you cannot name one,
  say whether the class is closed **by construction** or merely **by
  enumeration** — enumeration ages.

**What these five do not reach.** They are structural questions about where
material comes from and what runs. A semantically valid instruction that is
hostile carries no lexical signature, and no question here finds it. They also
do not check whether an answer is *true* — they convert a hidden property into a
written claim a reviewer can falsify.

**Prospective only.** This accounting — and the review sweep that checks it
(`doctrine/dual-review.md`) — applies to active and future artifacts; an
archived proposal or plan is immutable and is never retro-fitted with it.

### Tests required

<!-- cairn:slot tests-tier-home -->
Cairn's behavioral **test homes** are:

* **`bootstrap/tests/`** — the engine suite (the scaffold, the module
  merge, the upgrade path, the security stack, the gates). Fast,
  offline, `pytest` + standard library only (`vermin` is the one
  dev-only floor-check dep). Run the whole suite with
  `python -m pytest bootstrap/tests`; route by file
  (`test_<surface>.py`) and by node when scoping a change.
* **The example self-tests** — `examples/minimal/test_greet.py` and
  `examples/scientific-minimal/test_water_budget.py`, which prove the
  shipped runnable examples still run.

For the proposed change, name the affected test homes, exact behavioral nodes,
and public paths that must be exercised through their real entry points. Record
any speed or environment tiers that exist, but **speed alone does not establish
affected coverage**. The eventual plan owns a reviewed change-specific mapping,
not a permanent fast set; **unknown or uncertain scope falls back to the full
suite**. Prose-integrity and quality gates (below) are not pytest tests; name
them under *Examples / smoke checks* and the plan's verification commands.
<!-- cairn:end tests-tier-home -->

### Examples / smoke checks

<!-- cairn:slot examples-smoke-home -->
End-to-end surfaces a change can exercise:

* **The example gallery** — `examples/minimal/` and
  `examples/scientific-minimal/` run their own `greet.py` /
  `water_budget.py` under `pytest`; a change that touches what the
  examples demonstrate runs them.
* **The scaffold, without writing** — `python bootstrap/scaffold.py
  --summary --config <profile>`, `--dry-run`, and `--manifest`
  exercise the install path end-to-end with no side effects.
* **The prose-integrity gate** — `python scripts/check_cairn.py`
  (internal link resolution + claim-path check) is the doc smoke for
  any Markdown / doctrine change.
<!-- cairn:end examples-smoke-home -->

## Signals the change is wrong

The observations that would show this change should be reverted or
rethought — and the recovery for each.

## Review -- {{reviewer}} -- {{YYYY-MM-DD}}

**Model**: <your actual running model or tier when known; "unknown" if not. Do not copy-paste old model labels from past templates or archives; query and state your running model identity.>

**The four-field review basis is mandatory**, on its own lines, above this
pass's first `###` heading (a field below an H3 does not count). It names the
bounded target this pass actually read:

    Reviewed commit: <full commit id>
    Target: <the complete current-contract section this pass reviewed>
    Prior findings: <ids being closed, or none>
    Assurance path: <standard | high-assurance>

The basis is a **default navigation target, not a prohibition on examining
history**: open any earlier section a current claim depends on, and raise a new
correctness, security, scientific-validity, or scope finding whenever you find
one. A later review does not silently inherit an earlier reviewer's claims — it
either verifies them or names them as not covered.

**Reviewing a revision, verify its withdrawal ledger.** When `Target:` names a
complete current-contract revision, one part of the read is a comparison no tool
can perform for you: read that revision against the **previously reviewed**
contract, and confirm its `### Withdrawn / superseded commitments` ledger
accounts for every commitment the earlier contract carried and this one does
not. The conformance check can only see that the heading is there with a written
value; whether the ledger is *true* is this pass's finding to make.

**Plan readiness — the finding a derived plan may inherit.** An **External**
reviewer who has read a *complete* current contract may record, beside the basis
above:

    **Plan readiness**: READY | DISTINCT REVIEW REQUIRED

`READY` means that exact contract fixes scope and exclusions, invariants, failure
dispositions, public paths, omissions, test homes and standing gates,
documentation and release-note surfaces, implementation areas and sequence, and
any Maintainer fences or ceremonies. The derived plan then takes a fresh-context
**Internal** plan review rather than a second different-agent-type round, and
binds this record by commit.

Three things about the field, each of which a checker enforces:

* **It is optional, and it has no default.** Omit it and the derived plan takes a
  distinct plan review at its declared tier. A value outside the two tokens
  refuses rather than reading as `READY`.
* **`DISTINCT REVIEW REQUIRED` is a finding, not a fallback** — you saying
  consequential design necessarily remains for planning. It is an explicit
  judgement about *this* contract, never inferred from the topic.
* **Only an External pass may supply it.** What inheritance spends is the
  different-agent-type read; an Internal review has none to spend. The assurance
  path does *not* decide this: a high-assurance proposal may record `READY` too,
  and high assurance keeps governing verification, Security Review, protected
  surfaces and ceremonies.

The record needs no extra basis line — the reviewed commit and contract section
are already the four fields above.

Proposal reviews are written into the proposal file by default.
Chat comments can help the conversation, but they are not the durable
review record. Append the review as a new section in this file,
commit that lifecycle transition, and let the author's Response
answer the numbered critiques here.

**Steelman first** (per the review norms in
`dev/collaboration_agreement.md`). What's right about this proposal?

Then critique. Number each substantive concern so the response can
address them point-by-point. Use the project's review lenses where
relevant (workflow coherence, data contracts, extensibility,
operational maturity).

Critiques are prose-first. When a critique is *also* a specific edit
suggestion, attach it in one of two forms:

* **Inline suggested edit** — a fenced code block under the critique
  showing the proposed wording / code. Best for small fixes:

      * **[R2]** The triage rule reads as too narrow. Suggested edit:

          > Open a proposal only when the change ... **or when the
          > author wants a second opinion before baking it in.**

* **Review branch** — for substantive rewrites, create a branch
  named `<reviewer>/review-of-<original-slug>` with your edits as
  commits and reference the commit hash(es) in the critique. The
  author can cherry-pick or merge selectively. Push only with
  explicit Maintainer approval (per `AGENTS.md`'s "never commit or
  push without explicit user approval" rule).

      * **[R5]** Section X needs a stronger case. Suggested rewrite
        on branch `<reviewer>/review-of-<slug>` (commits `<sha>`).

Stick to prose-only when the critique isn't an edit — conceptual
concerns, questions, and steelmans don't fit in a diff.

* **[R1]** ...
* **[R2]** ...
* **[R3]** ...

**End with the coverage line + a second-round recommendation** (see
`doctrine/dual-review.md` > "Recommend-and-decide"). Two parts, then a call:

* **Covered** — the review-sweep lenses you swept, each with a falsifiable
  citation (file / test-node / line / command), not a bare "checked."
* **Not covered / low confidence** — the negative space: a lens you could not
  exercise, "same-type reviewer — no cross-type independence on this pass."

Then state an explicit **second-round recommendation** (recommended / not, with
reasons grounded in the negative space). Whether a second structurally-independent
pass runs is the Maintainer's call; a declared-`required` tier still runs
regardless.

## Response -- {{author}} -- {{YYYY-MM-DD}}

**Model**: <model or tier when known; "unknown" if not>

See `doctrine/proposals.md` > "Response — disposition grammars" for
the two-grammar vocabulary (Proposal-Response grammar when no
implementing commit exists; Code-review-Response grammar when
implementing commits are citable by sha).

For each numbered critique, write one disposition token from the
grammar above plus a one-sentence rationale. No silent dropping.
Brief is fine; precision matters more than length.

**Append one complete current contract with the Response, every time.** A
Response disposes findings; it does not restate the design, so on its own it
leaves the next reviewer to reassemble the contract out of the whole history —
which is the repeated reading this rule exists to remove. So beside this
Response append one **complete current-contract revision** —
`## Revised proposal`, or `## Revision <n>` — and set `Status:` to `revised`.
Not a delta and not a diff: one self-contained statement of scope and
exclusions, invariants, failure dispositions, public paths, evidence, omissions
and deferred work, plus the mandatory ledger:

    ### Withdrawn / superseded commitments
    * <earlier commitment, the replacement or withdrawal, and the reason>

**The heading is mandatory even when its value is `None`.** Write `* None`
rather than leaving the section empty or omitting it: a revision that quietly
drops an earlier commitment is exactly what this one heading exists to make
visible, and only a written `None` distinguishes "nothing was withdrawn" from
"nobody checked".

The **newest reviewed** complete revision is what the Decision and the
implementation bind. Every earlier section stays as immutable history — you are
appending a new contract, never editing the old one.

**Completeness is what buys the derived plan its lighter review.** Only an
**External** reviewer who has read a *complete* current contract may record
`Plan readiness: READY`, and only that finding lets the plan take a
fresh-context Internal pass instead of a second different-agent-type round. A
revision that leaves the reviewer reassembling the contract out of the history
cannot earn it -- so the completeness this section asks for is not bookkeeping,
it is the thing that removes a review round downstream.

Three mechanical facts, each of which the lifecycle conformance check enforces:

* **A Response with no revision refuses.** Either order is fine — the revision
  may sit above or below the Response — and no ratio of revisions to rounds is
  required.
* **Each revision carries exactly one ledger, with a written value.** A bare
  heading refuses; so do two ledgers in one contract, because two cannot both be
  the complete account.
* **The ledger is a real `###` heading at the left margin.** The block above is
  indented, which makes it an example rather than a heading; a copy inside a
  fenced block is not a heading either. Un-indent it when you use it.

And what the check cannot do is *read*: it never judges whether the revision is
genuinely complete, and it never verifies that the ledger is true. Both are the
reviewer's, per the comparison named in the `## Review` section above.

**Scope delta — declare it when the revision narrows what this proposal
will deliver.** Judge the narrowing against the **scope as opened**, not
against the previous round and not against a summary of purpose written
now. If every outcome the opened proposal committed to is still
delivered, the narrowing is `preserved` and **nothing further is
owed** — a lighter mechanism that still delivers is what restraint asks
for. You may state `preserved` so the record shows you checked; only
`degraded` and `lost` require the block below:

```
**Scope delta**: preserved | degraded | lost

**Removed scope**
* <unit> -- source section: <where it was committed to>; reason: <why>;
  **disposition**: <accept | guard (<path>::<node>) | wontfix (<why>) |
  defer (Maintainer's quoted authorization)>; revival/closure condition:
  <what would bring it back>.

**Disposition/home**: <where the grouped remainder now lives>

Each entry needs its **own** disposition -- a shared home is a location, not a
decision, and `doctrine/lifecycle.md` blocks archive on each entry
independently.
```

Three rules make this worth writing rather than ritual:

* **One grouped record**, not one roadmap row per unit. Dispersing a
  reduction into backlog fragments preserves the words and loses the
  reach.
* **The Maintainer allows the loss**, via the Decision, with the
  reduction visible. An author may propose one and a reviewer may
  recommend one; neither may concede a baseline outcome. `degraded`
  changes *what residual is recorded*, never *who may concede it*.
* **Declining a reviewer's proposed expansion is not a reduction.** It
  was never in the baseline. Record the suggestion and the reason in the
  Response — *Alternatives considered* if the idea is worth keeping.

And when review finds a part *underspecified*, the default resolution is
to **specify** it. Removing it instead is available and sometimes right,
but say why specifying was rejected — that sentence is what makes the
easy path visible as a choice. Full rule:
`doctrine/dual-review.md` > "Review expectations — the scope-reduction
trap".

<!-- `{{Maintainer}}` is the human Maintainer's FULL DISPLAY NAME, exactly as
     configured in `dev/.cairn/agent-identities.json` ("human_maintainers") --
     e.g. `## Decision -- Ada Lovelace (Maintainer) -- 2026-05-20`.  A bare role
     word ("Maintainer", "Human Maintainer") is NOT a name: the lifecycle
     conformance check refuses it, because a terminal Decision requires a KNOWN
     human and an unrecognized author cannot be confirmed human.  The `(role)`
     parenthetical is optional and is stripped before the name is matched. -->
## Decision -- {{Maintainer}} (Maintainer) -- {{YYYY-MM-DD}}

Final call: accept, reject, or supersede. Brief reasoning. Optional:
link to the commit(s) that implemented the accepted version.

If accepted and the change touches the roadmap, add a corresponding
`dev/PLANNING.md` entry in the same commit.

*If an agent scribes this Decision at the Maintainer's instruction:
quote or clearly paraphrase the Maintainer's instruction, name the
scribe, and record whether commit permission was explicitly given or
separately confirmed (per `AGENTS.md`'s Decision-commit guard-rail).*
