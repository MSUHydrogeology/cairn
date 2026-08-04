<!-- cairn-internal-ref-allow: doctrine/runtime-contract.md doctrine/lifecycle.md doctrine/plans.md doctrine/proposals.md doctrine/rationale.md doctrine/dual-review.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see AGENTS.md, "Where doctrine/ references resolve") -->

# Plan: a documented gate names what runs it — executing the enforcement-claim ledger

**Source proposal**: `gate-claims-vs-enforcement` (accepted 2026-08-03 by
Maintainer Decision `3a2a201`, *"I accept this proposal as revised"*). It
currently sits under `dev/proposals/` and moves to `dev/proposals/archive/` when
it archives.
**Status**: open
**Plan review**: required(**Internal**) — carried from the proposal header, which
argued the tier on the grounds that *"every disposition below except the hand-off
is a factual correction checkable by re-running one named command against one
quoted line."* The proposal's own Internal round (Gemini Flash, SHIP) reviewed
the **proposal**; the Decision states in terms that *"the plan carries
`required(Internal)` in its own right; this Decision does not discharge it."*
The proposal header further routes its one judgment call — whether the re-worded
`bootstrap/SAFETY.md` sentence still conveys the obligation it currently
overstates — into that read, so **the Internal reviewer applies a security lens
to Chunk E specifically**. **No implementation commit lands before the
`## Plan review` section is in the tree.** *That gate is weaker than this
sentence implies — see row E2 in* What changed *> 6, which measures it.*
**Review status**: the Internal round has **landed** (verdict SHIP after a
Response) and the author's Response — `## Revision after Internal plan review` —
is at the end of this file. Chunk bodies above are amended in place; the review
section is untouched.
**Last update**: 2026-08-04 (revised after Internal plan review)
**Opened**: 2026-08-04. The session that produced the Decision crossed midnight;
the Decision commit `3a2a201` and every artifact it cites are dated 2026-08-03,
and every measurement taken *for this plan* is `as_of 2026-08-04`. Both anchors
are recorded rather than one silently re-labelled, since this plan is about not
asserting what was not measured.

## Source proposal

The proposal settles one contract: **a document that describes a check names what
runs it** — a command a person runs, a test inside the suite, a git hook, or (if
one ever exists) a CI job — and, when a trigger is named, the document states
what that trigger actually verifies. That contract lands as one sentence in the
governing layer plus a disposition ledger applied to the current tree. **Nothing
that executes changes.** No new tool, no new file, no new command.

The plan executes that decision and does not re-litigate it.

### What the Decision accepted, read precisely

The Decision's own scribe note is the authority on the accepted state:

* The artifact carries **no `## Revised proposal` section**. The lifecycle ran
  open → append (two further rows from a later audit) → Internal review → author
  Response.
* The accepted state is *"the proposal as opened, **plus** the two appended rows,
  **plus** the Response's binding."*
* *"Accepting this fixes none of the 12 rows. It establishes what is true and who
  owns each."*
* The Response's binding makes Row E1's fallback an **archive precondition of the
  proposal**, in `dev/PLANNING.md`'s existing sense.

So: fourteen rows are accepted as *findings*. Two of them (E1, F1) were accepted
as routings rather than as edits, and both have since been discharged by other
lineages — see *What changed since the proposal was written*. One of them (B2)
carries an edit into two files the proposal's `Touches` line does not name, and
the proposal itself says that expansion is *"a reviewer's to ratify or refuse
rather than the author's to assume."* No reviewer ratified it; the Internal round
addressed only the twelve-row ledger. **B2 is therefore fenced out of this
plan's edit scope and routed** — see *Scope*.

### Glossary — every term glossed on first use

The audience is a scientist who codes. This scope is about a distinction that is
easy to nod at and hard to hold.

* **Gate** — a check that can stop a change from landing. The word implies a
  trigger that fires without anyone remembering.
* **Trigger** — the thing that causes a check to run: a command a person types, a
  test inside `python -m pytest bootstrap/tests`, a git hook, or a CI job.
* **Serialized shared file** — a file edited only at defined serialization points
  (`AGENTS.md`, `CHANGELOG.md`, `dev/PLANNING.md`, `docs/DOCUMENTATION_PLAN.md`,
  `bootstrap/REANCHOR_RUNBOOK.md`), per `AGENTS.md` > *Shared communication
  files*. An implementing agent **returns the exact text**; the orchestrator or
  the Maintainer lands it.
* **Frozen file** — a file whose sha256 is pinned in
  `bootstrap/tests/fixtures/gate_manifest.json`. During an **active gate batch
  window**, modifying one HOLDs by default.
* **Perturbation** — a deliberate change to repository state that a check is
  claimed to detect. This repository accepts a regression test only when its
  author can name a state in which it fails **and has run** the change that
  produces that state. *Perturbing a test's own body validates the test; only
  perturbing the hazard validates the claim.*
* **Class A / B / C / D / E / F** — the proposal's disposition classes: A = names
  a CI that does not exist; B = gate-phrased obligation with no trigger; C = true
  behaviour, missing trigger; D = already honest, no change; E = a shipped
  verifier that does not check the control its document promises; F = the named
  trigger exists and is the wrong artifact.

## What changed since the proposal was written

Five facts, all re-measured against the **working tree** at HEAD `8f47c76`,
`as_of 2026-08-04`, under the canonical interpreter
(`~/conda_envs/lhm/bin/python3.13`, Python 3.13.13). Each is the kind of thing
that would otherwise be discovered at implementation by whoever hit it first.
This plan is a claims audit, so it is held to its own standard: **every claim
below was checked against what the named artifact actually runs, not against the
proposal's snapshot.**

### 1. Row E1 is DISCHARGED — verified against the committed file, not the plan that claimed it

`release-authenticity`'s Chunks A–G landed in `b93f8e9`. The sentence Row E1
quoted no longer exists in `bootstrap/PROVENANCE.md`:

* The **second branch is retired outright**, not softened. The document now
  records the retirement and its reason inline (`bootstrap/PROVENANCE.md:53-60`):
  an adopter cannot check "maintainer-authored" (a free-text `%an` string) and
  cannot check "on the protected default branch" (forge-side configuration no
  clone reports).
* The **first branch is date-bounded** by a table at
  `bootstrap/PROVENANCE.md:37-41` stating `v0.2.0` and `v0.3.0` are **not
  signed** and **not verifiable by the bootstrap**, with the immutability
  argument for why they never will be.
* The **silent false negative is gone**, which was the whole of Row E1. Re-run
  for this plan, capturing the real exit code rather than a pipeline's:

```
$ bash bootstrap/container/verify-ref.sh . v0.3.0 >/tmp/vr.out 2>/tmp/vr.err; echo "exit=$?"
exit=1
$ cat /tmp/vr.err
verify-ref: REFUSED — provenance mode needs a trusted roster: pass --signers <path>
  or set CAIRN_ALLOWED_SIGNERS. There is no default and no fallback — see
  bootstrap/PROVENANCE.md for how to build one out of band
```

The pre-`b93f8e9` behaviour the proposal recorded — `verify-ref: OK — release
tag 'v0.3.0' -> 12ec2ad…` and exit `0` — does not reproduce. `git verify-tag
v0.3.0` still reports *"no signature found"* and exits 1, exactly as the
`PROVENANCE.md` table now says it will.

**The archive-precondition test, applied literally.** The binding reads: *"This
proposal does not archive while `bootstrap/PROVENANCE.md` asserts verified
release-tag signing that no shipped checker performs."* The document no longer
asserts that: it scopes the claim to `v0.4.0` onward, marks the two shipped
releases unverifiable, and a shipped checker (`bootstrap/container/verify-ref.sh`,
rewritten in `b93f8e9`; `bootstrap/tests/test_verify_ref.py`, 63 collected nodes
per that commit body) performs signature-and-name verification. **The
precondition is satisfied.**

**The residual, stated rather than assumed away.** `release-authenticity`'s
commit body records its own readiness condition — *"the control is DOCUMENTED AND
TESTED BUT NOT ESTABLISHED"*: Chunk M (publish the fingerprint, cut a signed
`v0.4.0`, run the bootstrap cold) is Maintainer-only and not performed.
`bootstrap/PROVENANCE.md:114` carries the matching *"Recorded as not
established"* disclosure. That is a forward-looking control with its own named
owner, **not** a present assertion about a shipped release, so it does not
re-open E1. It is named here so a reader does not have to re-derive the
distinction.

**Action for this plan: a note in this plan's record, not an edit.** The proposal
says marking the row discharged is *"a one-line note in that proposal's own
record"* — meaning this lineage's record. `bootstrap/PROVENANCE.md` is untouched
by this plan, as the proposal's *Deliberately not touched* header field requires.

### 2. Row F1 is DISCHARGED — already fixed, in HEAD, by a trivial-class commit

`AGENTS.md`'s AST-attestation pitfall no longer mispoints at
`bootstrap/REANCHOR_RUNBOOK.md`. Commit `58c7ba5` (*"AGENTS: fix the broken AST
re-anchor pointer (deferred question 4)"*, an ancestor of HEAD) rewrote it. The
current text at `AGENTS.md:335-345` says the opposite of what F1 quoted:

> **Not** via `bootstrap/REANCHOR_RUNBOOK.md` — that runbook governs the
> differential-oracle *gate* anchor and says nothing about this baseline.

It also does the thing F1's appended section said the row's correction *must*
do and could not do by search-and-replace: it names the applicable ceremony
inline (`_ast_attest._UPDATE_ALLOWLIST`; the Maintainer-run direct correction
for anything outside it; precedent `c3d5bd9`) and states the residual plainly —
*"No runbook covers it yet."*

**Action for this plan: a note, and one deletion from the AGENTS.md edit.**
Chunk A carries the governing rule **only**. Re-applying F1 would either be a
no-op or would overwrite a better correction with a worse one.

### 3. `bootstrap/SAFETY.md` moved under this plan's feet — B1 rebases

`scan-coverage` landed at `5c91c23` and edited `bootstrap/SAFETY.md`. The
proposal's *Cross-lineage collisions* table anticipated exactly this and
prescribed the handling: *"Whichever is accepted second rebases its edit onto the
landed text and re-quotes the line it replaces."* Done, below.

The clause B1 replaces is still at **`bootstrap/SAFETY.md:120-121`** (the file is
276 lines), unchanged in wording by `scan-coverage`:

```
the prose is right — and must pass the content-integrity scanner (`content_scan.py`, run by
[`check_cairn.py`](../scripts/check_cairn.py)).  The review threshold
```

What `scan-coverage` added is a **new residuals block at
`bootstrap/SAFETY.md:170-196`**, inside the *Executable code* bullet, naming
**two** live coverage residuals: `_CORE_MAPPINGS` reaching the manifest but
emitted `verbatim=False` unconditionally, and `_OPTIONAL_TEMPLATES` never
reaching the manifest at all. That block concerns the **Bandit** gate over
Layer-4 code; B1 concerns the **content** scanner over prose. They are disjoint
surfaces in the same document. **B1's replacement text is unaffected in
substance and is carried forward verbatim from the proposal** — but the
implementing agent re-reads lines 115-125 immediately before editing, because
this file has now moved twice today.

### 4. One un-ledgered **axis-1** instance, in a file already inside `Touches` — proposed as row A9

*Heading qualified at revision ([I8]).* It was *"one un-ledgered instance"*,
which overstated: axis 1 is a `CI`-token grep, and a five-minute **axis-2** read
of the very section Chunk C edits produces a second un-ledgered instance — now
recorded as **row B3** at the end of this subsection. One un-ledgered *axis-1*
instance is the claim the sweep below actually supports.

Re-running the proposal's **axis 1** sweep (both commands, verbatim) for this
plan reproduces its figures — **17 Markdown files** and **24 source files**
match, `as_of 2026-08-04` (re-run again at revision, HEAD `da2d00e`: 17 and 24,
unchanged) — and surfaces one hit the ledger does not disposition:

```
bootstrap/DEPENDENCY_BUDGET.md:97:## Exception 2 — `vermin`: floor CI check (dev/test-only)
```

The proposal ledgers `bootstrap/DEPENDENCY_BUDGET.md:101` (row A1) and the three
`doctrine/runtime-contract.md` occurrences of the same phrase (row A4), and
never mentions line 97. Grepping the proposal for `Exception 2` and for
`floor CI check` returns nothing. It is the identical shape — a heading whose
name lies while the body is accurate — one line above a row the ledger already
carries, in a file already named in `Touches`.

**Disposition proposed: land it in the same commit as A1, as row A9.** This is a
*coverage correction inside an already-claimed file*, not a scope expansion into
a new one, and the proposal's own *Signals the change is wrong* anticipates it:
*"if a reviewer finds a further instance on either axis, that is a coverage
correction to record, not a reason to withdraw the pattern finding."* It is
called out here explicitly so the plan review can **strike it in one line**
rather than discover it in the diff.

**The rate-limit count does not move.** The doctrine-change gate was cleared on
the recurrence arm at eight instances (A1–A8). A9 is a ninth instance of the same
shape. Inflating a cleared gate's evidence after the fact would be its own
overstatement; the count stays at eight as argued, and A9 is recorded as a
coverage correction.

#### Row B3 (new at revision) — an axis-2 instance 13 lines below a heading Chunk C renames. FOUND, ROUTED, NOT LANDED.

`doctrine/runtime-contract.md:202-211`, read at revision (`as_of 2026-08-04`,
HEAD `da2d00e`):

> The `vermin` syntactic check is the unit-suite mechanism. The **release floor
> gate** is stronger (`bootstrap/container/floor-gate.sh`): … In the release
> gate, an unresolvable `vermin` is an explicit **FAILURE**, never a silent
> skip-as-pass (the unit suite's graceful skip is for the ordinary test run
> only).

Axis 1 cannot see it — the passage carries no `CI` token, which is why the
proposal's sweep missed it. It is **Class B** on the proposal's taxonomy
(*gate-phrased obligation with no trigger*): *"the release floor gate"* and
*"In the release gate"* are gate vocabulary for a script that, per row A2's own
correction, is **run by the maintainer from a Cairn checkout and by nothing
automatic**. After Chunk B lands, `bootstrap/container/recipe.md` and
`doctrine/runtime-contract.md` describe the same script in opposite vocabulary,
and Chunk C's commit touches `doctrine/runtime-contract.md` three times without
touching this.

**Disposition: recorded, routed, and NOT landed by this plan.** Three reasons,
and the contrast with A9 is the point. (a) A9 is the *same class on the same
axis in the same file as an accepted row* — the proposal's *Signals the change
is wrong* pre-authorises exactly that as *"a coverage correction to record"*.
B3 is a **different class on a different axis**, which is a scope expansion, and
this plan's own B2 fence establishes that an unratified expansion is the
author's to route, not to assume. (b) A9 was surfaced *for a reviewer to strike
or ratify* and was ratified; the Internal round declined a second round, so no
reviewer remains in this plan's lifecycle to ratify B3 before implementation.
(c) Landing it would put a Class-B correction inside a commit whose changelog
line describes Class-A corrections, re-opening [I5].

**What stands instead**: the measurement above is on the record so nobody
re-derives it; the heading of this subsection is qualified; and B3 gets a
`dev/PLANNING.md` board row (*Lasting-truth migration*). **Silently leaving it
was the one option that would have reproduced the defect**, and it is not the
option taken.

### 5. A2's supporting claim is now STALE — and correcting it naively would ship a new false claim

This is the sharpest thing in this section, and it is the reason the plan spends
a chunk's worth of care on two sentences.

The proposal's row A2 rests on: *"Nothing in the suite or in `scripts/` invokes
either script"* — `bootstrap/container/floor-gate.sh` and
`bootstrap/container/acceptance.sh`. Measured at the working tree, `as_of
2026-08-04`, that is **half false**, because `b93f8e9` landed
`bootstrap/tests/test_verify_ref.py` after the proposal was written:

* **`floor-gate.sh` — the claim holds.** Nothing invokes it. The only other
  tracked mention is a comment in `bootstrap/container/Dockerfile:78` (*"…the
  floor gate needs. floor-gate.sh drives it…"*), which is prose, not an
  invocation.
* **`acceptance.sh` — the claim does not hold as written.** The suite now
  **reads the file and executes parts of it**:
  * `_extract_marked()` / `_replay_pin()` in `bootstrap/tests/test_verify_ref.py`
    pull marked `PIN-HELPERS` / `PIN <n>` blocks out of `acceptance.sh` and run
    them through `bash`, so *"a pin that is weakened there is weakened here"* —
    the module's own words.
  * `test_provenance_path_is_exercised_without_acceptance_sh` asserts on the
    file's text (`assert "--unprovenanced" in ACCEPTANCE.read_text()`).

  What is **still** true, and is what A2 is actually about: the **container
  acceptance gate itself** — building the image, running install + upgrade in
  the contained kernel — is invoked by nothing automatic. The suite replays its
  *assertions*; it never runs the *gate*.

Writing A2's replacement as *"nothing in the suite invokes either script"* would
therefore ship a **new** false enforcement claim inside the commit that exists
to remove false enforcement claims. Chunk B's wording is built around that
distinction, and the implementing agent re-runs the invocation check before
writing the sentence.

### 6. Row E2 (new at revision) — a routed finding: the review-before-implement gate is presence-only and tier-blind

Routed into this plan from `planner-line-semantics`'s Internal review. It is
**Class E** on the proposal's taxonomy — *a shipped verifier that does not check
the control its document promises* — which is precisely this scope's subject, so
it belongs in this ledger rather than in a sibling's. **Re-derived from the
primary source at revision, not taken from the routing note.**

**The code.** `tools/lifecycle_planner.py:787` gates review-before-implement on
`_has_kind(art, "Plan review")`; `_has_kind` (`:693-694`) is
`any(s.kind.lower().startswith(prefix.lower()) for s in art.sections)`, over
sections parsed by `_HEADER_RE` (`:509-515`), which matches `##` **and** `###`.
The declared tier is read at `:785` and `:853` only as
`art.plan_review.lower().startswith("required")` — **the `<tier>` token inside
the parentheses is never parsed anywhere in the module.**
`templates/skills/_lib/lifecycle_planner.py` is the byte-twin at the same line
numbers, so an adopter installs the same behaviour.

**Perturbation of the hazard, run at revision** (HEAD `da2d00e`, canonical
interpreter). Each case is a plan declaring `**Plan review**: required(External)`
at status `executing`; the module is loaded and `_conformance_violations` called
directly, with the fixture plan as the only variable:

| Artifact state | gate |
|---|---|
| no `Plan review` section at all | **VIOLATION** (correct) |
| `## Plan review -- Claude (Internal, same-agent-type; security lens) -- 2026-08-03`, full body | **clears** |
| `### Plan review -- Reviewer -- 2026-08-04` sub-heading, **empty body** | **clears** |
| `## Plan review` — bare, **undated, no body at all** | **clears** |
| review body states REVISE with findings, **no `### Sharpening`** | **clears** |
| `## Plan review — the brief…` (em-dash tail) | **VIOLATION** — the heading does not parse at all |

**Against the documented claim.** `doctrine/plans.md:111-117` says a plan
*"reaches `executing` only after a dated `## Plan review` section lands: the
review **and**, when it raised findings, a dated `### Sharpening` subsection
dispositioning them"*, and `doctrine/lifecycle.md:175-182` says *"The gate is
**explicit, not remembered**"* about the `required(<tier>)` line. Four of those
promises are unenforced: **dated** (row 4 above), **`##`** (row 3), **Sharpening**
(row 5), and **the tier itself** (row 2). A plan declaring `required(External)`
is cleared to implement by an Internal review that says in its own first
paragraph that it discharges nothing — and one reviewer has already worked
around the heading level deliberately.

**Disposition: RECORDED as a ledger row, ROUTED, and nothing landed here.**

* **The code fix is out of contract.** *"Nothing that executes changes. No new
  tool, no new file, no new command"* is the accepted proposal's opening
  constraint. Making the gate tier-aware is a change to a shipped verifier and
  its adopter-installed twin. It is routed to the `planner-line-semantics`
  lineage, which owns `lifecycle_planner.py`, plus a `dev/PLANNING.md` board row
  so it is not lost at the seam if that lineage declines it a second time.
* **The prose fix is refused as a *partial*, with a reason.** The overstated
  claim lives in **two** files: `doctrine/lifecycle.md` (which Chunk D already
  edits) and `doctrine/plans.md` (which row B2 explicitly **fences out**, on the
  `Touches` ground the Internal review confirmed). Correcting only
  `doctrine/lifecycle.md` would leave `doctrine/plans.md` overstating — which is
  verbatim the failure mode Chunk D is built as an indivisible pair to avoid
  (*"Correcting one leaves the other overstating"*). A partial fix here is worse
  than none, so both wait for one artifact that can touch both files.
* **What lands in this plan instead**: this measurement; the correction to this
  plan's own anti-placeholder note under *Plan review* (which asserted something
  about this exact checker and was imprecise about why it holds); and the
  **recursion sentence** in Chunk A's rule text, which is the general statement
  that makes E2, [I1] and [I2] one finding rather than three.

**No perturbation is claimed for a row this plan does not land.** The table above
is the perturbation; it validates the *finding*, and there is nothing in this
plan for it to redden.

## Scope

Executes the accepted contract across **five chunks and nine files**, of which
two (`AGENTS.md`, `CHANGELOG.md`) are serialized shared files whose text this
plan **returns** rather than edits. Every touched file is Cairn-internal:
**nothing ships to an adopter, no manifest row moves, and no executable line
changes** — the one non-Markdown edit (Chunk B, row A7) is a `#` comment.

*Corrected at revision from "eight files" ([I9.5]).* Eight is the proposal's
`Touches` count, which does not include `CHANGELOG.md`. The chunk tables below
name **nine** distinct files: `AGENTS.md`, `bootstrap/container/recipe.md`,
`bootstrap/container/floor-gate.sh`, `bootstrap/DEPENDENCY_BUDGET.md`,
`doctrine/runtime-contract.md`, `doctrine/lifecycle.md`,
`bootstrap/fidelity-check.md`, `bootstrap/SAFETY.md`, `CHANGELOG.md`.

**Row-id convention — read this before the chunk tables.** The proposal's
disposition ledger uses bare ids (`A1`…`A9`, `B1`, `B2`, `C1`, `C2`, `E1`,
`F1`). The chunk tables below use **dotted** ids (`A.1`, `B.1`…`B.3`,
`C.1`…`C.5`, `D.1`, `D.2`, `E.1`, `E.2`) for *rows of that table*. The two
namespaces collided at plan-open — ledger `E1` (the discharged
`bootstrap/PROVENANCE.md` row) and Chunk E's first table row were both written
`E1`, and ledger `B1` (the `bootstrap/SAFETY.md` clause) collided with Chunk B's
first table row. The dot disambiguates them; **"row B1" always means the ledger
row, "row B.1" always means the chunk-table row.** Introduced at revision
because two review findings ([I3], [I5]) had to disambiguate by hand.

**Rows this plan lands:** A1, A2, A3, A4, A7, A9 (new), B1, C1, C2, and the
governing rule.
**Rows this plan records as closed:** E1, F1.
**Rows this plan defers:** A5, A6, A8.
**Rows this plan fences out:** B2.
**Rows this plan records as found-and-routed, landing nothing:** B3 (new, from
[I8]) and E2 (new, routed in from `planner-line-semantics`) — see *Known
omissions* and *Lasting-truth migration*.
**Rows with no action by design:** Class D (the five already-honest wordings that
are the rule's model), and the four out-of-scope adopter-facing prescriptions.

### Out of scope, fenced explicitly

* **Row B2 — the archive-commit-body auditability claim in `doctrine/proposals.md`
  and `doctrine/plans.md`. FENCED, and routed.** Its finding is accepted; its
  *edit* is not in this plan. Three reasons, in order of weight. (a) Neither file
  appears in the proposal's `Touches` header, and the proposal itself says the
  expansion is *"a reviewer's to ratify or refuse rather than the author's to
  assume."* (b) No reviewer ratified it — the Internal round addressed the
  twelve-row ledger and never mentions B2 or F1. (c) The Decision's *"What is
  accepted"* line names *"the 12-row enforcement ledger … all verified row by row
  by the reviewer"*, so the appended rows are accepted **as findings** on the
  scribe note's authority, without a reviewer's row-by-row verification behind
  them. Row B2's own text also draws a boundary the plan honours: the same block
  is restated in `doctrine/lifecycle-contract.md` and carried in
  `dev/PLANNING.md`, whose adopter-facing twin is
  `templates/core/dev/PLANNING.md`; extending the re-wording there would engage
  the loop-fidelity lens this plan states is not engaged. **Durable home
  pre-declared in *Lasting-truth migration*.** If the plan review ratifies the
  expansion in one line, it becomes Chunk F and the fence is lifted — that is
  cheaper than a second proposal, and it is the reviewer's call, not the
  author's.
* **Rows A5, A6, A8 — the three frozen test files. DEFERRED, with the release
  condition measured rather than assumed.** See *The frozen-file question* below.
* **Adding CI.** Explicitly not proposed, per the proposal's alternative 2 and
  its cost estimate. The Maintainer decides it separately.
* **A mechanical gate-honesty lens in `check_cairn.py`.** The proposal's
  alternative 3, rejected twice over — it builds a new mechanism against the
  standing direction, and a gate that enforces gate-honesty runs only when a
  human remembers, so it would be the next entry in its own ledger. **This plan
  proposes no new test and no new checker**; see *Acceptance criteria* > *Tests*.
* **`bootstrap/PROVENANCE.md`.** Untouched, per the proposal's header. Row E1's
  remedy landed in `release-authenticity`.
* **`bootstrap/REANCHOR_RUNBOOK.md`, and writing the missing AST re-anchor
  procedure.** Row F1's appended text scoped only the first half — point the
  sentence at the code — and `58c7ba5` did that. Writing the procedure is a
  separate piece of work with its own owner.
* **`scripts/sync_doc_snippets.py:43`** (*"The drift gate for CI"*). A
  byte-identical verbatim twin of the adopter-facing
  `templates/modules/team-gated/sync_doc_snippets.py`, where the sentence is
  correct. Editing one side alone breaks the verbatim-copy invariant. Checked,
  left alone — and re-checked for this plan: both files still carry the string at
  line 43.
* **`bootstrap/container/acceptance.sh:8`** (*"no Python in its own CI"*). Read
  in context for this plan: it describes the **adopter fixture repository** the
  acceptance test builds, not Cairn. Not a finding. Recorded because *"it says
  CI, therefore it is a finding"* would have been wrong here.

### The frozen-file question — measured, put to the reviewer, and ANSWERED

*The Internal review's answer, recorded here so the disposition is not only in
the review section: **the deferral is correct; its stated basis was not.** Keep
A5, A6 and A8 deferred — the accepted *Sequencing*'s second conjunct is plainly
unmet — but the supporting figures are corrected below per [I4], and the plan now
records that A5's own file is among the committed drift. The reviewer
independently confirmed the mechanism claim: `test_gate_manifest.py:33` builds
its expectation from `G.produce(_REPO)` on the working tree and verifies against
that, so no suite node can redden on committed-map drift.*

The proposal defers A5, A6 and A8 *"to a follow-up commit after that batch closes
**and its manifest is retired**."* That condition has two conjuncts and they now
disagree, so the plan states what it measured instead of picking the reading it
prefers.

* **The batch closed.** `gate-reanchor-preflight` is archived
  (`dev/plans/archive/gate-reanchor-preflight.md`); `dev/PLANNING.md:279` records
  the entry surviving only because *"its commitments are live, not completed."*
* **The manifest is not retired.** `bootstrap/tests/fixtures/gate_manifest.json`
  still exists, still carries a `frozen_files` map, and all three paths are still
  literal keys in it. The map holds **164** entries (`as_of 2026-08-04`) — the
  proposal's figure of 162 was correct when written and was superseded by the
  Phase-0 re-pin at `e45e1fc`, which blessed `_gate_preflight.py` and its test
  from `FROZEN-NEW` to pinned.
* **The manifest is stale by six *committed* entries, from three commits, none
  of them re-pinned — corrected at revision ([I4]).** The plan-open figure was
  *"mismatches: 9"* hashed against the **working tree**, and the supporting
  sentence called it *"nine other commits"*. Both were wrong, in the same
  document that refuses to assert a suite figure because the working tree
  carries another workflow's edits. Re-measured at revision, HEAD `da2d00e`,
  splitting the two:

```
frozen entries: 164
working-tree mismatches: 10     <- NOT the figure; contaminated, and it moved
HEAD (committed) mismatches: 6  <- the figure

  HEAD:  bootstrap/security_check.py                     (5c91c23 scan-coverage)
         bootstrap/tests/test_security_check.py          (5c91c23 scan-coverage)
         bootstrap/tests/test_security_lint.py           (5c91c23 scan-coverage)
         bootstrap/tests/test_lifecycle_contract.py      (1dabe4d byline-classification)
         bootstrap/tests/test_quality_gate_redundancy.py (7066489 quality_gate R6)
         scripts/quality_gate.py                         (7066489 quality_gate R6)

  working-tree-only (another workflow's uncommitted edits, not drift):
         bootstrap/tests/test_lockfile_module.py
         bootstrap/tests/test_verify_integrity.py
         bootstrap/verify_integrity.py
         bootstrap/tests/test_scaffold.py
```

  **The working-tree number moved from 9 to 10 between plan-open and revision**
  — `bootstrap/tests/test_scaffold.py` joined it — which is the demonstration,
  not an anecdote: a figure taken over a shared working tree is not a figure.
  The committed figure is **six files across three commits** (`5c91c23`,
  `1dabe4d`, `7066489`), attributed above by `git log <pin>..HEAD -- <path>`
  where `<pin>` is `e45e1fc`, the last commit to touch
  `bootstrap/tests/fixtures/gate_manifest.json`.

* **A5's own file is among the committed drift, and the plan says so rather than
  eliding it.** `bootstrap/tests/test_security_lint.py` — the frozen file row A5
  would edit — was modified by the sibling `scan-coverage` (`5c91c23`) *after*
  the pin, with no re-pin. That does not make working around the HOLD right, but
  it means this plan's "no exception for me" framing describes a HOLD that was
  not in fact held for that file by a lineage that landed hours earlier. Stated
  because the alternative is a deferral argument that quietly depends on a
  uniformity the tree does not have.

* **Nothing in the suite enforces the committed map.** `test_gate_manifest.py`
  builds its expected manifest by calling `G.produce(_REPO)` on the working tree
  and verifies against *that*, so editing a frozen file does not redden the
  suite. The HOLD fires only when a person runs
  `bootstrap/tests/_gate_manifest.py verify --anchor-ref <SHA>` — a supervised
  ceremony belonging to a batch.

**The plan's disposition: keep A5, A6 and A8 deferred.** The accepted
*Sequencing* is part of the accepted contract; its second conjunct is unmet; and
the proposal's own reasoning for the deferral — *"working around a frozen-file
HOLD is exactly the behaviour that manifest exists to prevent"* — does not stop
applying because **three other commits** already drifted **six** frozen files.
This plan does not grant itself an exception the ledger it is executing would
have flagged.

**What would release them**, stated so the follow-up is pickable cold: the
manifest is retired, **or** a supervised re-pin lands and the Maintainer says the
three rows may ride it. Both are Maintainer-side; neither is this plan's to
decide. The six stale committed pins are already an open Maintainer question
raised by `scan-coverage` (*"whether re-pinning the three stale frozen entries
should happen now or at the next supervised re-anchor"*), and this plan adds
three prospective rows to it rather than opening a second question. *(That
question's own count was three when it was raised; this plan measures six at
HEAD `da2d00e` and does not silently reconcile the two — the Maintainer sees
both figures with their `as_of` anchors.)*

### Documentation / doctrine surface

* **Governing layer (`AGENTS.md`)** — one new paragraph in *Verifying claims*
  (Chunk A). Cross-cutting prescription every contributor follows. **Serialized:
  text returned, not edited in-agent.**
* **Doctrine (`doctrine/`)** — `doctrine/runtime-contract.md` (A4, a heading
  rename plus two echoes) and `doctrine/lifecycle.md` (C1, one appended clause).
  Neither changes a rule; both are factual corrections to descriptions.
* **Descriptive layer** — `bootstrap/DEPENDENCY_BUDGET.md` (A1, A9),
  `bootstrap/container/recipe.md` (A2, A3), `bootstrap/fidelity-check.md` (C2),
  `bootstrap/SAFETY.md` (B1).
* **Code-adjacent prose** — `bootstrap/container/floor-gate.sh` (A7), a `#`
  comment in the script whose behaviour row A2's document describes, corrected in
  the same commit as the document.
* **Release-facing** — `CHANGELOG.md > Unreleased > Fixed`, one line.
  **Serialized: text returned.**
* **Adopter-installed files — none, and this was checked rather than assumed.**
  `templates/core/AGENTS.md` carries the `claim-check` slot as an unfilled
  placeholder (`templates/core/AGENTS.md:228-234`) and contains **zero**
  occurrences of the standalone token `CI` — verified. The new rule says *"Cairn
  has no CI"*, which is **false for an adopter**, so it must not be mirrored
  there. The loop-fidelity lens is not engaged and no install-set surface moves.
* **Deliberation layer** — this plan, its plan review, its code review, and the
  `dev/PLANNING.md` row-move that serializes the plan-open.

<!-- cairn:slot documentation-tier-home -->
**Doc tier home rule** — route doc and doctrine changes by layer per
[`docs/DOCUMENTATION_PLAN.md`](../../docs/DOCUMENTATION_PLAN.md):
cross-cutting prescription → governing layer (`AGENTS.md`);
deliberation about what to build → deliberation layer (`dev/`);
description of the software as it is → descriptive layer (`docs/`). A
plan's *Scope* must name the doctrine-surface touched (or an explicit
"no doctrine surface").
<!-- cairn:end documentation-tier-home -->

## Sequence

Chunk order is load-bearing in exactly two places, and tidy elsewhere. **Chunk A
lands first** so every later commit corrects a sentence against a rule already in
the tree rather than against a plan. **Chunk B is indivisible**: `recipe.md`'s
prose (A2) and `floor-gate.sh`'s header comment (A7) state the same claim, and
correcting one without the other leaves the code contradicting the document —
the proposal says so in terms. **Chunk E lands last** because it is the security
document, it rebases onto `scan-coverage`'s landed text, and it is the one edit
with no mechanical guard of any kind.

```
0. plan-open  -- this plan + the dev/PLANNING.md row-move            [commit pending]
   (plan review) -- required(Internal, security lens on Chunk E); NO code before it lands
1. Chunk A -- the governing rule (AGENTS.md; SERIALIZED, text returned)   [commit pending]
2. Chunk B -- the container surface: A2 + A3 + A7, indivisible            [commit pending]
3. Chunk C -- the floor-check names: A1 + A9 + A4                         [commit pending]
4. Chunk D -- Class C, the two trigger clauses: C1 + C2                   [commit pending]
5. Chunk E -- bootstrap/SAFETY.md (B1) + the CHANGELOG line (SERIALIZED)  [commit pending]
```

---

### Chunk A — the governing rule

**Serialized shared file. The implementing agent writes no bytes into
`AGENTS.md`; it returns the text below and the orchestrator or the Maintainer
lands it.**

| # | File | Change |
|---|------|--------|
| A.1 | `AGENTS.md` > *Verifying claims* | Insert the rule paragraph **after** the `<!-- cairn:end claim-check -->` marker at `AGENTS.md:267` and before the `## Documentation discipline` heading at `AGENTS.md:269`. Text below, verbatim. |

**The exact text to insert** (the proposal's rule, **with the third clause
included** — ratified by the Internal review, see *Revision after Internal plan
review*):

> **Name the trigger, check what it checks, and open it.** Any document that
> describes a check says what runs it — a command a person runs, a test in
> `bootstrap/tests`, a git hook, or a CI job. Cairn has no CI; do not write
> "in CI" for something no CI runs. A check whose only trigger is a human
> remembering is described that way. And when a named trigger exists, the
> document states what that trigger actually verifies: a tool that returns
> success without testing the claimed property is a worse defect than no
> tool, because it is silent. **A named trigger is checked by opening it and
> confirming the procedure is there — a path that resolves is not a trigger
> that governs — and the check does not stop at the first named artifact: it
> recurses until it reaches a human or a machine.**

*Anchors re-verified at revision, HEAD `da2d00e`:* `AGENTS.md` is 372 lines;
`<!-- cairn:slot claim-check -->` opens at `:248`; the *"discipline aid, not a
gate"* sentence runs `:260-266`; `<!-- cairn:end claim-check -->` is at `:267`;
`## Documentation discipline` is at `:269`. Unchanged since plan-open.

**Two deltas from the proposal's drafted third clause, both stated so a reader
can see exactly what is authorial.** The proposal's appended text is *"**and
open it.** A named trigger is checked by opening it and confirming the procedure
is there. A path that resolves is not a trigger that governs."* It is folded
into the existing paragraph rather than added as its own bolded lead (one
paragraph, one rule), and it gains the **recursion sentence**. The recursion
sentence is **new at revision** and it is the general form of Internal findings
[I1], [I2] and the routed row E2: in all three, the first named artifact exists
and the trigger does not. Without it the rule is satisfied by naming
`bootstrap/security_check.py` — which nothing runs. It is the one authorial
addition to the rule text and a reviewer may strike it in one line, in which
case the two sentences before it still stand.

**One placement deviation from the proposal's literal instruction, with its
reason.** The proposal says *"after the existing sentence 'The checker is a
**discipline aid, not a gate**'"*, and calls the location deliberate — the
sentence it follows is already the correct model. That sentence ends at
`AGENTS.md:266`, one line **inside** the `cairn:slot claim-check` block that
opens at `AGENTS.md:248` and closes at `AGENTS.md:267`. Slot bodies are
module-merge territory: `check_slot_fidelity()` in
`bootstrap/_scaffold/slotmerge.py:348` compares an installed module's expected
content against the slot body, and a future `claim-check` module gaining a
`cairn:merge-target` directive would write into that block. Placing
Cairn-specific governing prose one line past the `cairn:end` marker keeps the
proposal's intent — it still reads as a generalisation of the sentence
immediately above it — while putting it where no module owns the bytes.

**Verified, so the deviation is a judgment about risk and not a guess about
mechanism:** `templates/modules/default-on/claim-check.md` declares **no**
`cairn:merge` directives today, and `check_slot_fidelity` matches by
whitespace-collapsed **substring**, so appending inside the slot would not
redden anything *today*. The deviation buys against a future merge, not a
present failure, and a reviewer is invited to strike it and take the literal
placement instead.

**The open question this chunk handed to the reviewer — ANSWERED.** The
proposal's appended section offered its third clause conditionally (*"would take
at review"*), and the plan-open text withheld it so that including it would be a
reviewer's ratification rather than a silent authorial expansion. **The Internal
review ratified it: *"INCLUDE it"*, on the ground that [I1] and [I2] are both
third-clause findings — in both, the named artifact is *there*, and a
two-clause rule catches neither.** It is therefore in the verbatim text above,
and this paragraph records who authorised it. The reviewer attached one
condition — *"it applies to this plan's own acceptance criteria from the moment
it lands"* — which is discharged by the [I1], [I2] and [I3] amendments to Chunks
C, D and E below.

**Acceptance criteria — Chunk A.**

* The text lands verbatim, outside the slot, in a serialization commit the
  orchestrator or the Maintainer makes.
* `~/conda_envs/lhm/bin/python3.13 scripts/claim_check.py AGENTS.md` → clean.
* `~/conda_envs/lhm/bin/python3.13 scripts/check_cairn.py` → green. **This green
  is vacuous as evidence that the rule is right** — it checks links, anchors,
  claim-paths and content, and asserts nothing about a governing sentence's
  truth. Recorded rather than presented as a guard, per [I1].
* `~/conda_envs/lhm/bin/python3.13 scripts/quality_gate.py --sub neutrality` →
  green. The rule names no vendor.
* **`templates/core/AGENTS.md` is unchanged**, verified with `git status --short`
  — checked because the rule is Cairn-specific and false for an adopter.
* **`~/conda_envs/lhm/bin/python3.13 scripts/token_budget.py`, run before and
  after** ([I9.10]). It is the one tool whose stated purpose is measuring the
  always-on prefix this chunk grows, and Chunk A's acceptance omitted it.
  Measured baseline at revision (`as_of 2026-08-04`, HEAD `da2d00e`, chars/4
  proxy): `AGENTS.md` **5,014 tok** of a **5,541 tok** always-on manifest
  (`CLAUDE.md` 527). The rule text above is **783 chars as written (773 with
  `*`/`` ` `` markup stripped) → ~196 tok**, ~3.5% of the manifest. It is a soft
  cap and will not block; running it is one line and it is the only measurement
  this surface has. **Record the after-figure in the serialization commit
  body.**

  **Corrected before commit.** An earlier draft of this revision put the rule
  text at 674 chars → ~168 tok. That is the figure for the text **without the
  recursion sentence** (663 chars measured), so it understated the shipped rule
  by ~15% — in a figure this plan claims to have re-measured, and the very
  figure the "record the after-figure" criterion compares against. Method, so it
  is re-derivable: join the eleven `>` lines of the block above, strip the `> `
  prefix, collapse whitespace, `chars/4` proxy.

---

### Chunk B — the container surface, indivisible

Rows A2, A3 and A7. The document and the script it describes move in one commit.

| # | File | Change |
|---|------|--------|
| B.1 | `bootstrap/container/recipe.md:151-153` | Replace *"The **floor gate** … and the **acceptance test** … run in **Cairn's CI**, not in an adopter's CI."* with a sentence naming the real trigger **and** the suite's partial coupling to `acceptance.sh`. Draft below. |
| B.2 | `bootstrap/container/recipe.md:147` | Platform matrix, *Rootless Linux + Podman/Docker* row: change *"(the F4 acceptance gate runs here)"* to *"(the F4 acceptance gate is run here by hand)"*. |
| B.3 | `bootstrap/container/floor-gate.sh:5` | Replace the phrase *"Runs in CAIRN's CI (not adopter CI)."* inside the header comment block with *"Run by the maintainer from a Cairn checkout (not adopter CI)."* Comment-only; no executable line moves. Re-wrap per the criterion below. |

**Row B.1's citation corrected at revision ([I9.1]), and the edit boundary
named.** The plan-open citation was `:152-153`. Re-read at revision, HEAD
`da2d00e`:

```
151  The **floor gate** (`bootstrap/container/floor-gate.sh`) and the **acceptance
152  test** (`bootstrap/container/acceptance.sh`) run in **Cairn's CI**, not in an
153  adopter's CI. The acceptance test records **SKIPPED** (never PASS) on a host with
154  no OCI runtime — a missing gate is *degraded assurance*, not a silent green.
```

The replaced sentence **begins at line 151**; a line-anchored edit starting at
152 orphans *"The **floor gate** (`bootstrap/container/floor-gate.sh`) and the
**acceptance"*. Line 153 is **split**: its first sentence-fragment (*"adopter's
CI."*) is the tail of the replaced sentence, and *"The acceptance test records
**SKIPPED** (never PASS)…"* onward is the **Class D** sentence, which is left
byte-identical in substance. The edit is therefore sentence-anchored, not
line-anchored: **replace from *"The **floor gate**"* through *"not in an
adopter's CI."* and touch nothing after it** except re-wrapping the residual of
line 153, which is unavoidable.

**Draft replacement for row B.1**, written against the measurement in *What
changed* > 5 rather than against the proposal's stale supporting claim:

> The **floor gate** (`bootstrap/container/floor-gate.sh`) and the **acceptance
> test** (`bootstrap/container/acceptance.sh`) are run by the maintainer from a
> Cairn checkout, not in an adopter's CI — and not by anything automatic here:
> no test and no script in `scripts/` runs either gate. (The suite does *read*
> `acceptance.sh`: `bootstrap/tests/test_verify_ref.py` extracts its marked
> negative pins and replays them, so a pin weakened there is weakened in the
> suite too. That pins the assertions; it does not run the container gate.)

**Acceptance criteria — Chunk B.**

* The invocation check is **re-run immediately before the sentence is written**,
  not carried forward from this plan:

```
$ git ls-files | xargs grep -ln 'floor-gate.sh\|acceptance.sh' 2>/dev/null | grep -v '^dev/'
```

  Expected today (`as_of 2026-08-04`, re-run at revision against HEAD
  `da2d00e` — the same 8 paths, unchanged): `CHANGELOG.md`,
  `bootstrap/container/Dockerfile`, `bootstrap/container/acceptance.sh`,
  `bootstrap/container/floor-gate.sh`, `bootstrap/container/recipe.md`,
  `bootstrap/container/verify-ref.sh`, `bootstrap/tests/test_verify_ref.py`,
  `doctrine/runtime-contract.md`. **If a new invoker has appeared, the sentence
  changes before it is written.** If `test_verify_ref.py` has *stopped*
  appearing, the parenthetical is deleted rather than left to assert.

  **This grep is a *mention* check, and stating that is part of the criterion
  ([I9.7]).** It catches a **new file** referencing either script. It **cannot**
  catch a new invocation added inside a file already on the list: if
  `bootstrap/tests/test_verify_ref.py` began running `acceptance.sh` wholesale
  tomorrow, the output above is byte-identical and this criterion passes while
  the sentence it guards goes false. **So the criterion is: run the grep *and
  open each of the 8 hits and read it in context*** — which is the third clause
  of the rule Chunk A installs, applied to this plan's own acceptance. The plan
  already did that work at plan-open for `bootstrap/container/Dockerfile:78` (a
  prose comment, not an invocation) and `bootstrap/container/acceptance.sh:8`
  (about the adopter fixture repo, not Cairn) and got both right; this codifies
  it rather than leaving it to the implementing agent's diligence.
* **The diff criterion, corrected at revision ([I9.8]).** The plan-open form was
  *"exactly one changed line, beginning with `#`"*. Measured: line 5 is **80
  chars** and the comment block wraps at **≤83 characters**; the drafted
  replacement makes line 5 **105 chars**. "Exactly one changed line" therefore
  silently mandated a 105-char line in an 80-wrapped block. **Take the
  re-wrap.** The criterion is now: `git diff bootstrap/container/floor-gate.sh`
  shows changes on **comment lines only** — every `+` and `-` line begins with
  `#` — **no line exceeds 83 Unicode characters**, and the diff is confined to
  the header block above the first executable statement.

  **State the unit — an earlier draft did not, and the criterion is unsafe
  without it.** That draft said "lines 3, 9 and 13 are 83". Measured: those
  lines are **81, 81 and 83 characters** but **83 bytes each** (em-dashes).
  Untouched line 15 is **82 characters and 84 bytes**. So a "≤83" criterion
  measured in *bytes* — which is what `awk '{print length}'` yields on macOS,
  and evidently how the draft's figures were produced — **fails on a line this
  chunk never edits**. Measure characters, e.g.
  `python3 -c "import sys;[print(len(l.rstrip(chr(10)))) for l in open(sys.argv[1],encoding='utf-8')]"`.
* `bash -n bootstrap/container/floor-gate.sh` → exit 0. **Near-vacuous, and said
  so ([I9.8]):** a `#`-comment edit cannot break bash syntax unless the `#`
  itself is removed. It is kept as a one-second guard against exactly that
  typo, and is worth nothing else.
* `~/conda_envs/lhm/bin/python3.13 scripts/claim_check.py
  bootstrap/container/recipe.md` → clean.
* **No new test, and the honest reason.** Grepping `bootstrap/tests/` for
  `floor-gate` returns nothing, `as_of 2026-08-04`; nothing asserts on
  `recipe.md`'s prose either. This chunk has **no closed failure mode**. The
  guard is the reviewer. That is stated rather than papered over, because it is
  the finding one layer down.

---

### Chunk C — the floor-check names

Rows A1, A4 and the proposed A9. One commit: the `bootstrap/DEPENDENCY_BUDGET.md`
heading, its body sentence, and the `doctrine/runtime-contract.md` heading it
echoes are the same claim in three places.

| # | File | Change |
|---|------|--------|
| C.1 | `bootstrap/DEPENDENCY_BUDGET.md:101` | *"It runs only in Cairn's own CI (`bootstrap/tests/test_python_floor.py`)"* → the replacement below, **including the skip-as-pass disclosure**. Doubly wrong as written: there is no CI, **and** the test runs locally. |
| C.2 | `bootstrap/DEPENDENCY_BUDGET.md:97` | **Row A9, ratified by the Internal review.** Heading *"## Exception 2 — `vermin`: floor CI check (dev/test-only)"* → *"## Exception 2 — `vermin`: floor check (dev/test-only)"*. |
| C.3 | `doctrine/runtime-contract.md:189` | Heading *"## Floor CI check"* → *"## Floor check"*. |
| C.4 | `doctrine/runtime-contract.md:46` | *"the surface measured for the floor CI check"* → *"…for the floor check"*. |
| C.5 | `doctrine/runtime-contract.md:185` | *"(`vermin` for the floor CI check)"* → *"(`vermin` for the floor check)"*. |

**Row C.1's replacement text, amended at revision ([I3]) — the sentence names a
trigger that returns green without checking, and now says so.**

> It runs only in Cairn's own test suite (`bootstrap/tests/test_python_floor.py`,
> run by `python -m pytest bootstrap/tests`), **which skips — and so passes
> green — whenever `vermin` is not importable or on `PATH`**.

Measured at revision, HEAD `da2d00e`, `as_of 2026-08-04`, perturbing the
**hazard** (`vermin`'s presence on `PATH`) and not the test's body:

```
$ ~/conda_envs/lhm/bin/python3.13 -c "import shutil,importlib.util; \
    print(shutil.which('vermin'), importlib.util.find_spec('vermin') is not None)"
/Users/kendal30/conda_envs/miniforge3/bin/vermin False

$ ~/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests/test_python_floor.py -q -rs
2 passed in 0.64s

$ PATH=/usr/bin:/bin ~/conda_envs/lhm/bin/python3.13 -m pytest \
      bootstrap/tests/test_python_floor.py -q -rs
ss
SKIPPED [1] bootstrap/tests/test_python_floor.py:158: vermin is not installed; ...
SKIPPED [1] bootstrap/tests/test_python_floor.py:188: vermin is not installed; ...
2 skipped in 0.02s
```

`vermin` is **not importable by the canonical interpreter**; it resolves only
because the ambient shell `PATH` carries a different conda environment. So the
trigger row C.1 names *returns success without testing the claimed property* in
any environment without `vermin` on `PATH` — verbatim the hazard Chunk A's rule
calls *"a worse defect than no tool, because it is silent."* Writing the
plan-open sentence without the disclosure would have installed a fresh instance
of the defect in the commit that installs the rule against it.

The section bodies are otherwise accurate — `doctrine/runtime-contract.md:194`
already discloses the skip (*"The check skips gracefully if `vermin` is not
importable or on PATH"*) — so on `doctrine/runtime-contract.md` **only the names
lie**, and only the names move. `bootstrap/DEPENDENCY_BUDGET.md`'s Exception-2
body (`:99-103`) carries **no** such disclosure, which is why row C.1 adds it
and row C.3–C.5 do not.

**Acceptance criteria — Chunk C.**

* **The anchor check, and the perturbation that would make it fail.** Renaming a
  heading changes its GitHub anchor (`#floor-ci-check` → `#floor-check`;
  `#exception-2--vermin-floor-ci-check-devtest-only` →
  `#exception-2--vermin-floor-check-devtest-only`), and
  `scripts/check_cairn.py` resolves internal anchors. **The grep form is
  corrected at revision — the plan-open form was self-matching and no longer
  reproduces.** As written it was `grep -rn "<anchor>" --include="*.md" .`,
  reported as `rc=1` for all four. Re-run at revision (HEAD `da2d00e`) it
  returns **`rc=0` for all four**, and every hit is *this plan's own prose*
  quoting the anchor strings — this criterion's own paragraph, this code block,
  and the review section's ratification of row A9. **A criterion that matches
  the document asserting it is not a criterion.** Corrected
  to exclude the deliberation tree, the way this plan's other sweeps already do:

```
$ for p in floor-ci-check exception-2 runtime-contract.md# DEPENDENCY_BUDGET.md#; do
    git ls-files '*.md' | grep -v '^dev/' | xargs grep -n "$p" >/dev/null 2>&1; echo "$p rc=$?"
  done
floor-ci-check rc=1
exception-2 rc=1
runtime-contract.md# rc=1
DEPENDENCY_BUDGET.md# rc=1
```

  So the substance survives: **zero** inbound anchor references outside `dev/`,
  `as_of 2026-08-04`. (For context, the only anchor-bearing inbound Markdown
  link outside `dev/` anywhere in the tree is
  `templates/core/dev/plans/_template.md:268` → `../PLANNING.md#archive-preconditions…`,
  which is unrelated to either renamed heading.)

  **State the consequence plainly rather than claiming a guard: because there
  are no inbound anchors, `check_cairn.py` staying green over this rename is
  *vacuous* — it would stay green whether or not the rename were correct.** The
  check is worth running (concurrent work could add an inbound link before this
  chunk lands) and is worth **nothing** as evidence that the rename is right. A
  claims-audit plan does not get to present a vacuous green as a guard.
* The four greps above are **re-run at implementation in the corrected
  `dev/`-excluding form**, not trusted from here. If they are re-run in the
  plan-open form they return `rc=0` and mean nothing.
* `~/conda_envs/lhm/bin/python3.13 scripts/claim_check.py
  bootstrap/DEPENDENCY_BUDGET.md` and the same over
  `doctrine/runtime-contract.md` → clean, one file per invocation.
* `~/conda_envs/lhm/bin/python3.13 scripts/check_cairn.py` → green.
* **Row C.1's replacement names a trigger that must be true — and the criterion
  is the TWO-run form ([I3]).** The plan-open criterion was a single run: *"if it
  now skips, the sentence changes."* That is the artifact-supplying-its-own-oracle
  shape — it measures whether the **implementing agent's environment** has
  `vermin`, not whether the sentence is true for the reader it is written for. It
  was green on 2026-07-22, is green today, and would be green on a machine where
  the check has never once actually run. Replace it with both runs:

```
$ ~/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests/test_python_floor.py -q -rs
$ PATH=/usr/bin:/bin ~/conda_envs/lhm/bin/python3.13 -m pytest \
      bootstrap/tests/test_python_floor.py -q -rs
```

  **Both results go in the commit body.** The first must *pass*, the second must
  *skip* — and the second run **is the perturbation of the hazard** that makes
  the disclosure clause in row C.1 falsifiable rather than decorative. If the
  second run now *fails* instead of skipping, the disclosure is wrong and the
  sentence changes; if the first run skips, the whole replacement changes.

---

### Chunk D — Class C, the two trigger clauses

Rows C1 and C2. **They move together**: the same gate, the same phrasing, in two
files. Correcting one leaves the other overstating.

| # | File | Change |
|---|------|--------|
| D.1 | `doctrine/lifecycle.md:217-221` | Append the trigger clause as a **new sentence immediately after the sentence carrying "fails closed"**, which ends at `:221` with *"…but **dangles once installed**."* |
| D.2 | `bootstrap/fidelity-check.md:41-48` | The same new sentence, inserted after the sentence carrying *"fails closed"* — which **ends at `:45`** with *"…nor marked a deliberate citation."*, **not** at the end of the paragraph. |

**The insertion points are named explicitly, and they are not the same relative
position ([I9.6]).** The plan-open instruction was *"the same one-clause addition
to the parallel sentence"*, and the two host sentences are **not** parallel where
that assumed. Read at revision, HEAD `da2d00e`:

* `doctrine/lifecycle.md:218` carries *"the `check_cairn` self-check **fails
  closed** when…"* and that sentence **ends** at `:221` (*"…**dangles once
  installed**."*). An em-dash clause appended there attaches to *"fails closed"*.
* `bootstrap/fidelity-check.md:42` carries *"the `check_cairn` self-check fails
  closed when…"* and that sentence **ends at `:45`** (*"…nor marked a deliberate
  citation."*). The *"dangles once installed"* phrase is in the **next**
  sentence, which **begins mid-`:45`** (*"Such a…"*) and runs through `:48` to
  *"…the un-shipped 9-lens review roster."* (An earlier draft of this revision
  cited `:43` for the first sentence and `:46-48` for the second — an
  off-by-one, inside the row folding in a **citation-defect** finding. The
  governing instruction is unaffected: the clause still lands as its own
  sentence after the one ending at `:45`.)
  Appending the clause at the end of *that* sentence attaches *"when run"* to
  **"roster"**, not to *"fails closed"* — a sentence that says the wrong thing.

So the clause lands as its **own sentence** in both files, immediately after the
sentence that carries the *"fails closed"* claim, at `doctrine/lifecycle.md:221`
and at `bootstrap/fidelity-check.md:45`.

**The clause, amended at revision ([I2]) to name the release gate as
maintainer-run:**

> When run: `python scripts/check_cairn.py` — at review time, and in the
> **maintainer-run** release checklist (`bootstrap/security_check.py` invokes
> it, when a maintainer runs that).

**Why the amendment is binding rather than cosmetic.** The plan-open wording was
*"…at review time and in the release gate (`bootstrap/security_check.py` runs
it)"*, which reads as **one manual trigger and one automatic one**. Both halves
of the original verification table were true, but the table never asked the next
question the rule Chunk A installs makes mandatory: **what runs
`security_check.py`?** Measured at revision, HEAD `da2d00e`:

* Nothing automatic invokes **the composed gate**. `run_check_cairn` has exactly
  two occurrences in the tree — its `def` at `bootstrap/security_check.py:214`
  and the composed call `rc = run_bandit() | run_check_cairn()` at `:226` — and
  nothing outside that module calls `main()`. So the landed *"maintainer-run"*
  clause is correct.

  **Narrowed before commit; an earlier draft overstated this.** That draft said
  *"no test, no script and no forge config that invokes it; every hit is prose, a
  docstring, a manifest entry or a deliberation file"*, which is **false at the
  module level**: `bootstrap/tests/test_security_check.py:18` imports
  `security_check` and calls `security_check.run_bandit()` directly at eight
  sites, and with `bandit` importable in this environment
  `test_run_bandit_clean_with_bandit_present` (`:150`) executes **half the gate
  on every suite run**. The claim holds of the composed gate, not of the module,
  and is now stated that way. `grep -n security_check tools/intent.py` → no
  match.
* The two installed git hooks are `pre-commit` → `tools/intent.py
  _precommit_check` and `post-commit` → `tools/intent.py _auto_release`,
  terminated `|| true`. Read verbatim from `.git/hooks/`.
* `SECURITY.md:59-63` places it under *"Release security checklist — Before
  cutting a release, run — and record the output in the release notes"*. **It is
  a checklist line a person remembers.**

Chunk A's rule says: *"A check whose only trigger is a human remembering is
described that way."* The plan-open clause did not; the amended one does.

**Both halves of the clause verified against the code**, since this is an
enforcement claim in a plan about enforcement claims:

* `bootstrap/security_check.py:214` defines `run_check_cairn()`, which executes
  `CAIRN_ROOT / "scripts" / "check_cairn.py"`; `bootstrap/security_check.py:226`
  returns `run_bandit() | run_check_cairn()`. The release gate does run it —
  **when a maintainer runs the release gate.**
* `scripts/check_cairn.py` scans `git ls-files '*.md'` via `tracked_markdown()`
  at `scripts/check_cairn.py:180`, and its own header (`scripts/check_cairn.py:50`)
  states the scanned set is *"the whole tracked Markdown tree."*

**Acceptance criteria — Chunk D.**

* Both files edited in one commit; `git diff --stat` shows exactly two files.
* Each file's diff shows the clause **after the "fails closed" sentence**, per
  the insertion points above — verified by reading the hunk, not by line number.
* `~/conda_envs/lhm/bin/python3.13 scripts/claim_check.py doctrine/lifecycle.md`
  and the same over `bootstrap/fidelity-check.md` → clean.
* `~/conda_envs/lhm/bin/python3.13 scripts/check_cairn.py` → green — **and this
  green is as vacuous here as it is in Chunk C. Corrected at revision ([I1]).**
  The plan-open criterion claimed this was *"the one place where that command is
  a **real** check"*, on the ground that `bootstrap/fidelity-check.md` carries a
  live `cairn-internal-ref` marker whose text the edit sits next to. Three things
  were wrong, measured at revision:
  * The marker is at `bootstrap/fidelity-check.md:55`, **not 52**. Line 52 is
    prose.
  * It is **not live**. `scripts/check_cairn.py:507-508` gates the lens —
    `if _is_template_instruction(rel): _check_dangling_internal_refs(...)` — and
    `_is_template_instruction` (`scripts/check_cairn.py:286`) is exactly
    `return rel.startswith('templates/')` (`:293`). Neither
    `bootstrap/fidelity-check.md` nor `doctrine/lifecycle.md` is under
    `templates/`. The marker's own inline reason text says so
    (*"fidelity-check.md is bootstrap-internal, not an installed adopter
    surface"*). **It exempts nothing, because nothing is being applied.**
  * Therefore `check_cairn.py` over Chunk D checks links, anchors, claim-paths
    and content — and **nothing whatever about the trigger clause**.

  This was the sharpest Internal finding because it is the plan's own defect one
  level up: *a marker that is present is not a lens that runs*, exactly as *a
  path that resolves is not a trigger that governs*. Recorded here rather than
  quietly deleted.
* **The only real guard on Chunk D is the code review opening
  `bootstrap/security_check.py` and `SECURITY.md` and confirming the amended
  clause.** No test asserts on either file's prose. Named, not invented.
* The claim *"fails closed"* is **kept, not weakened** — that is the whole point
  of Class C, and the proposal's alternative 4 rejects deleting a true claim to
  avoid an untrue implication. The amendment weakens nothing: it qualifies *who
  runs the trigger*, not *what the check does when run*.

---

### Chunk E — `bootstrap/SAFETY.md`, and the changelog

Row B1, plus the serialized release note. Last, and reviewed with a security
lens.

| # | File | Change |
|---|------|--------|
| E.1 | `bootstrap/SAFETY.md:120-121` | Replace the *"must pass the content-integrity scanner"* clause with the replacement below — **which keeps "must pass"**. The surrounding sentence and the by-file-class list are untouched. |
| E.2 | `CHANGELOG.md > Unreleased > Fixed` | One line. **Serialized: text returned, not edited in-agent.** |

**The replacement clause — REWRITTEN at revision.** The plan-open draft was
carried verbatim from the proposal and read:

> ~~— and is scanned with the content-integrity scanner (`content_scan.py`).
> Two triggers exist and neither fires on a commit: the suite scans generated
> output and the skills artifacts on every `pytest` run, and `check_cairn.py`
> scans every tracked Markdown file when a person runs it (the release gate
> `security_check.py` runs it). Source prose that no scaffolded profile emits —
> `doctrine/`, `docs/`, `case-studies/`, this document — is reached **only** by
> that manual run. Running it is the reviewer's obligation, not a mechanism's
> guarantee.~~

The Internal review's security-lens read found it a **weakening** — in one
specific, modal respect — and the plan's own *"Open (degrades)"* recovery line
already named the fix. The current text says content *"**must pass** the
content-integrity scanner"*: an obligation **with a pass criterion**. The draft
said *"**is scanned with**"* plus *"Running it is the reviewer's obligation"*:
the obligation survives but transfers from **passing** to **running**. A
reviewer who runs `content_scan.py`, reads the flags, and ships has satisfied the
draft's letter. In an adopter-facing security document about a supply chain of
agent-executed instructions — where the threat is a hidden instruction reaching
*"every downstream adopter's agents at once"* (`bootstrap/SAFETY.md:114-115`) —
that is the wrong direction. **The plan's stated recovery is required up front
rather than held as recovery.** The replacement is now:

> — and **must pass** the content-integrity scanner (`content_scan.py`, run by
> [`check_cairn.py`](../scripts/check_cairn.py)). **Two triggers exist and
> neither fires on a commit**: the suite scans generated output and the skills
> artifacts on every `pytest` run, and `check_cairn.py` scans every tracked
> Markdown file when a person runs it (the **maintainer-run** release gate
> `security_check.py` invokes it, when a maintainer runs that). Source prose that
> no scaffolded profile emits — **including** `doctrine/`, `docs/`,
> `case-studies/` and this document — is reached **only** by that manual run.
> **Running it, and resolving what it flags, is the reviewer's obligation, not a
> mechanism's guarantee.**

Four changes from the draft, each closing a named finding: **"must pass"**
restored (the security-lens read); **"maintainer-run … when a maintainer runs
that"** ([I2]); **"including"** ([I9.9]); and the live Markdown link to
`../scripts/check_cairn.py` **restored** — the draft silently dropped a link
that `check_cairn.py`'s own link-checker currently resolves, which is the one
place in this chunk where a green *would* have meant something.

**Why "including" is not pedantry ([I9.9]).**
`bootstrap/tests/test_generated_output_scan.py` scaffolds **three representative
profiles** — minimal, representative team, adversarial (its module docstring
says so at `:4-12`; the three tests are at `:81`, `:86`, `:96`). So the
manual-only set is **larger** than the draft's appositive list: it also includes
`on-ramp/`, root `README.md` / `SECURITY.md`, `bootstrap/*.md`, `dimensions/`,
`examples/`, and any `templates/modules/` prose those three profiles do not emit.
In a security document, a list that reads as exhaustive and **understates the
uncovered surface** errs in the wrong direction.

**Every factual claim in the replacement, verified against the code — citations
corrected at revision ([I9.4]):**

| Claim | Verified against |
|---|---|
| the suite scans **generated output** on every `pytest` run | `bootstrap/tests/test_generated_output_scan.py` imports `content_scan` (`:32`), scans every generated `*.md` via `_scan_generated()` (`:48-55`), and scans the generated `AGENTS.md` directly at `:121` |
| the suite scans the **skills artifacts** | `bootstrap/tests/test_skills_security.py`: `CONTENT_SCAN_SRC` at `:42`, `_load()` defined at `:50` and called at `:60`, `content_scan.scan_file` at `:71` (canonical artifacts) and `:82` (installed copies). *The plan-open citation "(lines 9, 42)" was wrong — `:9` is a docstring bullet and `:42` a path constant; neither loads or scans anything.* |
| `check_cairn.py` scans **every tracked Markdown file** | `tracked_markdown()` at `scripts/check_cairn.py:180` runs `git ls-files '*.md'`; the header at `:50` says so |
| **the release gate invokes it** | `run_check_cairn()` at `bootstrap/security_check.py:214`; composed at `:226` as `run_bandit() \| run_check_cairn()` |
| **the release gate is maintainer-run** | nothing invokes `bootstrap/security_check.py`: no test, no script, no hook, no forge config; `SECURITY.md:59-63` lists it under *"Release security checklist — Before cutting a release, run"* |
| **neither trigger fires on a commit** | the two installed git hooks, read verbatim from `.git/hooks/`: `pre-commit` → `tools/intent.py _precommit_check` (work-intent claim collisions only) and `post-commit` → `tools/intent.py _auto_release`, terminated `\|\| true` |

**One precision residual, recorded rather than smoothed over — and now with the
fact that makes it harmless.** `scripts/check_cairn.py` declares
`--no-content-scan` at **`:532`** and consumes it at **`:560`**
(`content_scan_enabled=not args.no_content_scan`) — *the plan-open citation named
only `:560`, the consumption site, as though it were the declaration ([I9.3])*.
So *"scans every tracked Markdown file when a person runs it"* is true of the
default invocation and not of every invocation. The clause is left as written —
adding "unless they pass `--no-content-scan`" buys precision no reader needs and
costs the sentence its point — and the residual is **harmless** because
`bootstrap/security_check.py:221` invokes the script with **no flags**, so the
release gate always scans. The Internal review reached the same disposition
independently.

**The proposed `CHANGELOG.md` line** (returned for serialization; `Unreleased` >
`Fixed`) — **corrected at revision ([I5]); the plan-open draft overstated by
three, in the release note whose subject is "Enforcement claims name their
trigger":**

> - **Enforcement claims name their trigger.** Corrected nine documented checks
>   that described themselves in the vocabulary of an automatic gate — five
>   naming a CI this repository does not have; three further CI-naming instances
>   under `bootstrap/tests/` are deferred behind the frozen-file manifest —
>   across `bootstrap/SAFETY.md`, `bootstrap/DEPENDENCY_BUDGET.md`,
>   `bootstrap/container/recipe.md`, `bootstrap/container/floor-gate.sh`,
>   `bootstrap/fidelity-check.md`, `doctrine/runtime-contract.md` and
>   `doctrine/lifecycle.md`. Nothing that executes changed. `AGENTS.md` gains the
>   governing rule: a document that describes a check names what runs it, states
>   what that trigger actually verifies, and is checked by opening it.

**The count, re-derived at revision** with a standalone-`CI`-token regex
(`(?<![A-Za-z0-9_])CI(?![A-Za-z0-9_])`) over each landing row's target lines,
HEAD `da2d00e`:

| Row | Target | Names a standalone `CI` token? |
|---|---|---|
| A1 | `bootstrap/DEPENDENCY_BUDGET.md:101` | **yes** |
| A2 | `bootstrap/container/recipe.md:151-153` | **yes** |
| A3 | `bootstrap/container/recipe.md:147` | no |
| A4 | `doctrine/runtime-contract.md:46`, `:185`, `:189` | **yes** (all three) |
| A7 | `bootstrap/container/floor-gate.sh:5` | **yes** |
| A9 | `bootstrap/DEPENDENCY_BUDGET.md:97` | **yes** |
| B1 | `bootstrap/SAFETY.md:120-121` | no |
| C1 | `doctrine/lifecycle.md:218-221` | no |
| C2 | `bootstrap/fidelity-check.md:42-48` | no |

**Five**, not eight. *Nine* (the total corrected checks) is right. "Eight" was
the proposal's count of Class-A **instances** (A1–A8), three of which — A5, A6,
A8 — this plan explicitly **defers**; as drafted the changelog credited the
commit with corrections it does not make. The deferral is now named in the line
itself so the residual is on the release record rather than only in this plan.

**Acceptance criteria — Chunk E.**

* **`bootstrap/SAFETY.md:115-125` is re-read immediately before editing.** This
  file moved twice today (`5c91c23`, and this plan). If the quoted clause is not
  where this plan says it is, the plan is stale and the reviewer is told, not
  worked around.
* `git diff bootstrap/SAFETY.md` touches **only** the clause. Specifically: the
  by-file-class list (lines 122-198) and the residuals block `scan-coverage`
  added at lines 170-196 are byte-identical. Verify with `git diff -U0` and read
  every hunk. (`bootstrap/SAFETY.md` is 276 lines, re-confirmed at revision.)
* **The word "must" survives.** `git diff bootstrap/SAFETY.md | grep '^+'` shows
  the string `must pass` present in the added text. This is the one criterion
  that mechanically catches the modal weakening the security-lens read found —
  it is a grep, not a guard, and it is worth exactly what a grep is worth.
* `~/conda_envs/lhm/bin/python3.13 scripts/claim_check.py bootstrap/SAFETY.md` →
  clean.
* `~/conda_envs/lhm/bin/python3.13 scripts/check_cairn.py` → green.
* **No test guards this edit, and no test is added.** Verified for this plan:
  grepping `bootstrap/tests/` for `SAFETY` returns one hit, a comment at
  `bootstrap/tests/test_generated_output_scan.py:114`, not an assertion. The
  entire guard is the Internal reviewer's security-lens read. The proposal names
  this as *"the sharp one"* among its open failure modes and the plan does not
  soften it.

---

## Acceptance criteria

* **Tests that must pass** — `~/conda_envs/lhm/bin/python3.13 -m pytest
  bootstrap/tests` green under Python 3.13.13, with **no new node**. The suite is
  a *no-change check* here, not a guard: nine of the ten landing rows touch only
  Markdown and the tenth (A7) is a shell comment.

  **No new test is added, and the reason is the proposal's, not convenience.** A
  test that scans Cairn's own prose for "in CI" is alternative 3, rejected: it
  builds a new mechanism against the standing direction and it is
  self-undermining — a gate enforcing gate-honesty runs only when a human
  remembers, so it becomes the next row in its own ledger.

  **What a reviewer who wants one must require of it**, stated so the bar is on
  the record rather than in a reviewer's head. Two failures shipped in this
  session are the reason: an anti-drift assertion whose expected set was
  computed from the code's own object (green for 63 days, could not fail), and a
  security test whose fixture built its own tree and so could not hold the
  residual it was written for. Any prose gate proposed later must therefore (a)
  derive its oracle from something the subject does not read, and (b) be shown
  RED by **perturbing the hazard** — reintroducing a false "in CI" sentence into
  a real tracked file — never by perturbing the test's own body. Absent both, it
  is decoration and should be refused.
* **Doc updates that must land** — hand-authored, all of them; there is no
  generated or snippet-synced surface in scope. Enumerated per chunk above.
  `CHANGELOG.md > Unreleased > Fixed`: one line, serialized.
* **Examples / smoke checks** — `~/conda_envs/lhm/bin/python3.13
  scripts/check_cairn.py` (prose-integrity smoke for every Markdown change) and
  `~/conda_envs/lhm/bin/python3.13 scripts/claim_check.py <file>`, **one file per
  invocation** — it exits 2 on more than one. No scaffold surface changes, so
  `bootstrap/scaffold.py --summary` / `--dry-run` / `--manifest` are unaffected
  and are not run.
* **Inbound path-link updates** — none. No file moves. `dev/PLANNING.md` and
  `dev/NEXT_SESSION.md` refer to plans by filename stem, not path link, so
  neither needs an update on the archive-move.

### Author-accounting — invariants, failure modes, edge cases

Not a routine change — it edits a named security document — so the block is
filled rather than waived. At plan stage the satisfier is *sequencing*: each
invariant names the chunk that enforces it, or says plainly that nothing does.

* **Invariants, each with its enforcer.**
  * *Nothing that executes changes behaviour.* Enforced by the suite (Acceptance)
    plus a per-chunk `git diff` read. Of the ten landing rows, nine edit only
    Markdown; A7 is a `#` comment whose script passes `bash -n` (Chunk B).
  * *No adopter-installed surface moves.* Enforced by Chunk A's
    `templates/core/AGENTS.md`-unchanged check and by the fact that no file in
    scope is in the install set. **Not** enforced by any test in this plan —
    it is a property of the file list, checkable by reading it.
  * *No claim in this plan's own replacement text is itself an unverified
    enforcement claim.* Enforced by the per-row verification tables in Chunks B,
    D and E, and by the re-run requirements in each chunk's acceptance. This is
    the invariant a reviewer should attack hardest: it is the one this plan
    exists to uphold, and one instance (A2's supporting claim) has **already**
    failed it between proposal-accept and plan-open.
  * *`bootstrap/SAFETY.md`'s by-file-class review threshold list is untouched.*
    Enforced by Chunk E's `git diff -U0` hunk-by-hunk read. Only the clause at
    lines 120-121 moves.
  * *No enforcement claim is weakened into an optional one.* **Enforced by review,
    not by a mechanism** — this is the row the Internal reviewer was asked to
    challenge, **and it challenged it successfully**: the plan-open draft of row
    B1 moved the obligation from *passing* the scanner to *running* it. The
    revised replacement keeps **"must pass"** verbatim and adds *"and resolving
    what it flags"*; C1/C2 keep *"fails closed"*. The only mechanical residue is
    Chunk E's `grep '^+' | must pass` criterion, which is a grep, not a guard.
  * *A serialized shared file is never edited by the implementing agent.*
    Enforced by the chunk tables (Chunks A and E mark their rows SERIALIZED) and
    by review of the commit's path list. No mechanism detects it.
* **Public-path → test mapping.** **N/A** — no public code path is added or
  changed. The only non-Markdown edit is a `#` comment in
  `bootstrap/container/floor-gate.sh`, a script no test invokes.
* **Failure modes.**
  * *Open (degrades) — **fired, and the recovery is now the design***: the
    re-worded B1 reads as permission to skip the scan. This is the one failure
    mode in the plan that the Internal round **actually caught happening**, in
    the plan-open draft. The stated recovery — *"restore the imperative and add
    the trigger as a separate sentence, keeping 'must' intact"* — has been
    applied up front rather than held in reserve, so the residual risk is now the
    ordinary one (a reader misreads a sentence that says "must pass"), not the
    designed one.
  * *Open, and this is the sharp one:* **there is no closed failure mode for a bad
    B1 edit, and none for A2/A3/A7 either.** No test asserts on
    `bootstrap/SAFETY.md`'s prose (one "SAFETY" hit across `bootstrap/tests/`,
    and it is a comment) and none asserts on `recipe.md` or `floor-gate.sh`
    (grepping `bootstrap/tests/` for `floor-gate` returns nothing). A reviewer is
    the entire guard. Naming that is more useful than pretending the suite covers
    it — and it is the same defect this plan is about, one layer down.
  * *Open (deferred by design):* A5, A6 and A8 stay wrong. Accepted and recorded;
    the release condition is in *Scope*.
  * *Closed by the world, not by this plan:* E1 and F1. Both were routings, and
    both routings **arrived** — `b93f8e9` and `58c7ba5`. This plan's obligation
    is to verify and record, which *What changed* does. The proposal's named
    hand-off failure mode (a routed finding lost at the seam) did not occur, and
    the verification is written down so a later reader does not have to re-run it
    to know that.
  * *New, introduced by this plan — **ratified***: row A9 was an authorial
    addition beyond the accepted ledger, isolated in one chunk row (C.2) for the
    reviewer to strike in one line. **The Internal review ratified it** on the
    ground that landing A1 while leaving line 97 reading *"floor CI check"* ships
    an internally contradictory document from the commit that exists to remove
    them. The refusal to inflate the cleared rate-limit count with it stands.
  * *New, introduced by this plan:* the Chunk A placement deviation. Mitigated by
    stating the mechanism it guards against, verifying that mechanism is inert
    today, and inviting the literal placement instead. **The Internal review
    declined to take a position** — it confirmed the mechanism is inert
    (`templates/modules/default-on/claim-check.md` declares no `cairn:merge`
    directives; `check_slot_fidelity` matches by whitespace-collapsed substring;
    no test compares `AGENTS.md` against `templates/core/AGENTS.md`
    structurally) and recorded that a same-type reviewer adds nothing to a
    judgment about a future merge. **It therefore remains open for the
    Maintainer**, and the deviation stands as drafted in the meantime.
  * *New to the **rule text**, but **not** authorial — **the recursion sentence
    in Chunk A's rule text***: it is new relative to the *proposal*, but the
    **reviewer wrote it**, near-verbatim, in the review's own closing
    carry-forward in this same file: *"The rule this plan installs does not stop
    at the first named trigger — it recurses until it reaches a human or a
    machine"*, against Chunk A's *"the check does not stop at the first named
    artifact: it recurses until it reaches a human or a machine"* — differing
    only in `trigger`→`artifact` and an em-dash for a colon. **An earlier draft
    of this revision called it "the one clause that neither the proposal nor the
    reviewer wrote" and "the one authorial addition to the rule text"; both are
    withdrawn as false.** The error over-declared authorship, so it is
    conservative in direction — but it would have misinformed the Maintainer
    being invited to strike the sentence as unratified, when in fact it carries
    the reviewer's own words. It generalises [I1], [I2] and row E2 and it is the
    reason those three are one finding. Still isolated as the final sentence, so
    striking it leaves the ratified two clauses intact.
* **Edge cases.** *Empty:* none of the edited lines is generated or synced, so no
  drift gate re-derives them — checked, not assumed, because the sweep did
  surface a candidate on a verbatim-synced file (`scripts/sync_doc_snippets.py`)
  and excluded it for exactly that reason. *Mismatched:* the three-way
  disagreement about the content scanner (B1) is itself the edge case, resolved
  by making `bootstrap/SAFETY.md` agree with the shipped runner's exit contract
  rather than the reverse. *Concurrent:* the working tree carries another
  workflow's uncommitted edits to `bootstrap/_scaffold/` and `bootstrap/tests/`
  — see *Verification* for how the baseline is taken.
* **Known omissions, stated rather than implied.**
  1. **The behavioural axis is still a sample.** The proposal's axis 2 — run the
     artifact that would check a stated control — was applied to
     `bootstrap/PROVENANCE.md`'s Controls bullets, `bootstrap/SAFETY.md` Rule 7,
     and the two Class C claims. This plan extends it only to the specific claims
     it writes (Chunks B, D, E) and to the two discharged rows. **A full
     behavioural audit of every *"fails closed"* / *"is signed"* / *"refuses"*
     claim in the tree was not run** and is plausibly its own proposal.
  2. **The third axis was not run at all.** The appended section named it —
     *does the named trigger actually contain the procedure, and does the record
     bear out the stated obligation* — and produced two rows from one external
     pass. This plan runs no systematic pass on it. **The Internal round did not
     close this either**, and said so: [I2] and row E2 are third-axis findings
     that fell out of opening four specific artifacts, which is weak evidence
     that a systematic pass would find more and **no** evidence about how much.
  3. **No human has re-read the corrected sentences for downstream readers other
     than the reviewer.** There is no mechanism that would.
  4. **The six stale committed frozen pins** (corrected from "nine", [I4]) are
     recorded, not resolved. They are a Maintainer question `scan-coverage`
     already raised.
  5. ~~**Whether the rule's third clause belongs in `AGENTS.md`**~~ — **settled at
     revision**: the Internal review ratified inclusion, and the clause is in
     Chunk A's verbatim text.
  6. **Row B3** — the axis-2 Class-B instance at
     `doctrine/runtime-contract.md:202-211` — is **seen and left**, with the
     measurement recorded in *What changed* > 4 and a durable home pre-declared.
     After Chunk B lands, `bootstrap/container/recipe.md` and
     `doctrine/runtime-contract.md` describe the same script in opposite
     vocabulary until B3 is picked up. Named rather than smoothed: this is the
     residual a reader is most likely to hit next.
  7. **Row E2** — the tier-blind, presence-only review-before-implement gate — is
     **measured and routed, not fixed**. Both the code fix (out of the accepted
     *"nothing that executes changes"* contract) and the prose fix (partial,
     because `doctrine/plans.md` is fenced) wait on a separate artifact. Until
     then the gate this plan's own lifecycle runs on remains one a placeholder
     satisfies.
  8. **The recursion this plan installs a rule about, it does not follow to the
     bottom.** After Chunks D and E, three documents point at
     `bootstrap/security_check.py`, and **nothing runs that** — it is a line in
     `SECURITY.md`'s release checklist that a person remembers. This plan
     describes that honestly in three places and changes none of it. Whether the
     repository's enforcement claims bottoming out in an unrun script deserves
     its own artifact is a Maintainer call; a board row carries it so the
     observation is not lost with this plan.

## Verification

Run under the canonical interpreter — `~/conda_envs/lhm/bin/python3.13`
(Python 3.13.13) — with `PYTHONDONTWRITEBYTECODE=1`. A different minor silently
changes the suite figure; see `bootstrap/DEPENDENCY_BUDGET.md` > *The canonical
interpreter*.

**The baseline is taken at implementation, not quoted from here, and the reason
is concrete.** At plan-open the working tree carries several other workflows'
uncommitted edits under `bootstrap/_scaffold/`, `bootstrap/tests/` and
`bootstrap/`, plus untracked files under `bootstrap/tests/` and `dev/plans/` —
the set was still changing while this plan was being written, which is itself the
point. A suite figure taken in that state measures someone else's in-flight work,
so **no suite figure is asserted in this plan.** The implementing agent takes the
baseline on a tree clean of foreign edits, checks `git status --short` first, and
records the figure in the commit body with the interpreter named.

<!-- cairn:slot verification-commands -->
The standing gates Cairn runs before a change lands (the same ones CI
enforces):

* **Engine suite** — `python -m pytest bootstrap/tests` (the whole
  suite; scope to `bootstrap/tests/test_<surface>.py` while iterating,
  but the full suite gates the cut).
* **Prose integrity** — `python scripts/check_cairn.py` (internal link
  / anchor resolution + claim-path check over the Markdown tree).
* **Quality gate** — `python scripts/quality_gate.py` (order-
  independence + vendor-neutrality + redundancy; `--sub neutrality`
  alone for a doctrine / template wording change).
* **Write-time claim check** — `python scripts/claim_check.py <file>` over
  each proposal / plan / doc the change authored. **One file per
  invocation** — the checker takes a single path and exits 2 (usage) on
  more, so loop rather than passing a list.

Plan-specific gates (a security-lint budget, a doc-drift gate, the
model-selection mapping check `python scripts/check_model_selection.py`)
are added per plan when the change touches that surface.
<!-- cairn:end verification-commands -->

**One correction to that slot, which this plan is obliged to make — and the
plan-open reason for routing it was itself a false claim, corrected at revision
([I7]).** The slot text reads *"the same ones CI enforces."* **Cairn has no CI.**

The plan-open text said *"The slot is Cairn's own copy of a template block
written for adopters, who do"*, and *Lasting-truth migration* called it *"a real
design question, not a typo"* needing the adopter-vs-Cairn boundary drawn.
**Measured at revision, HEAD `da2d00e`: there is no boundary to draw.**
`templates/core/dev/plans/_template.md:226-231` — the adopter-facing slot — is an
**unfilled placeholder**:

```
<!-- cairn:slot verification-commands -->
(Adopter-specific verification commands — the test-runner invocation +
expected scope, the doc-link / schema-render / snippet-drift gates, the
security-lint budget, and any plan-specific gate. Fill with the
project's commands, or replace with `N/A`.)
<!-- cairn:end verification-commands -->
```

The sentence does not exist in the adopter template. It is a **Class-A instance
in Cairn's own filled slot**, propagated into every plan opened from it.

**And the instance count is 20, not 1 — and it is growing, which is the argument
for re-measuring rather than carrying it.**
`git ls-files | xargs grep -ln "the same ones CI"` returns **20** files at
revision (HEAD `da2d00e`, `as_of 2026-08-04`), all under `dev/plans/`: the
template plus 19 live plans, this one among them. The Internal review measured
**7** on the same command roughly a day earlier; the difference is plans opened
since, not a disagreement.

**The routing stands; only the reason changes.** It is out of this plan's
`Touches`, and — the real reason — **a one-line template edit that would cascade
into 19 live plans needs its own serialization point**, not a ride on a chunk
commit. **Recorded as a found instance and routed** — see *Lasting-truth
migration*. Noting it and not fixing it is the correct move; noting it with a
false reason, in a plan about false claims, was not.

**Plan-specific gates.**

* **The falsifying signal, re-run before implementation, per the proposal.** A CI
  configuration for any forge appearing in the tree collapses Class A.
  Re-measured `as_of 2026-08-04`: `find .github -type f` returns the same seven
  files (five issue templates, one PR template, one label definition) and **no
  workflow**. `git ls-files` matched on `workflow|Jenkinsfile|circleci|travis|
  gitlab-ci|azure-pipelines|woodpecker|drone` returns exactly one path,
  `docs/workflow-role.md` — a prose document about where Cairn sits relative to
  an adopter's CI, not a pipeline file. **The proposal's phrasing (*"matched
  nothing"*) is narrowed to *"matched no pipeline file"*** so the re-run
  reproduces rather than appearing to contradict.
* **The E1-specific falsifying signal, re-run**: it **fired**, and that is why
  Row E1 is closed rather than handed off. `bash
  bootstrap/container/verify-ref.sh . v0.3.0` no longer exits 0, and a signature
  check now exists in `bootstrap/container/verify-ref.sh`. `git verify-tag
  v0.3.0` still fails, exactly as `bootstrap/PROVENANCE.md`'s table now says.
* **Both axis-1 sweeps, re-run verbatim** at implementation. Expected today: 17
  Markdown files, 24 source files.
* **`git status --short`** after each chunk, confirming the commit's path list
  contains no serialized shared file and no file another workflow is editing.

## Plan review — the brief, and whether the Internal round discharges it

*Required — Internal, with a security lens on Chunk E. Implementation does not
start until a review has landed under this heading.*

> **STATUS at 2026-08-04: the round has run.** The review is appended below as
> `## Plan review -- Claude (Internal, same-agent-type; security lens) --
> 2026-08-03`; its verdict is **SHIP after a Response**, with four findings
> marked binding and no second round asked for. The author's Response is the
> `## Revision after Internal plan review` section at the end of this file, and
> the chunk bodies above have been amended in place. **All four prerequisites
> below are answered** (1 E1/F1 verified independently; 2 A9 ratified; 3 the B2
> fence confirmed; 4 the third clause included), and the three aimed questions
> are dispositioned in the Response. The brief is left unedited so a reader can
> see what was asked before seeing what came back.

**Declared tier: `required(Internal)`.** It is the proposal header's declaration,
carried forward, and the Decision states it is not discharged by the proposal's
own round: *"The plan carries `required(Internal)` in its own right; this
Decision does not discharge it."*

**Does the Internal round about to run discharge it? Yes — with one condition.**
The floor is the same agent in a fresh session; the proposal's round was met by a
different agent type, which exceeded the floor. A fresh-session read that is
**not the implementing agent** discharges this plan's tier, **provided it covers
the four things the proposal's Internal round did not see**, because none of them
existed when that round ran:

1. **The two discharged rows.** E1 and F1 are recorded here as closed on the
   strength of `b93f8e9` and `58c7ba5`. **Verify both independently** — read
   `bootstrap/PROVENANCE.md` and `AGENTS.md:335-345` at HEAD, and run
   `bash bootstrap/container/verify-ref.sh . v0.3.0` capturing the exit code
   without a pipeline. If either is not discharged, this plan's *Lasting-truth
   migration* is wrong and the proposal's archive precondition is still binding.
2. **Row A9, the un-ledgered instance** at `bootstrap/DEPENDENCY_BUDGET.md:97`.
   Ratify it into Chunk C or strike it. Either is a one-line answer.
3. **The B2 fence.** The plan declines to edit `doctrine/proposals.md` and
   `doctrine/plans.md` because the *Touches* line does not name them and the
   proposal calls the expansion the reviewer's to ratify. **You are that
   reviewer.** Ratify it into a Chunk F, or confirm the routing.
4. **The rule's third clause** (*"and open it"*). Include or strike.

**The three questions the review should aim at, in descending weight:**

1. **Does any sentence this plan proposes to write assert something the named
   artifact does not do?** This is the plan's own standard turned on itself, and
   it has already caught one failure — A2's supporting claim was true when the
   proposal was written and false by the time the plan opened. Attack Chunk B's
   draft replacement, Chunk D's clause, and Chunk E's five-row verification table
   directly: re-run the greps, open
   `bootstrap/tests/test_verify_ref.py:1004-1090`,
   `bootstrap/security_check.py:214-226`, and
   `scripts/check_cairn.py:180`. If a claim does not survive, say so — a
   documentation-honesty commit shipping a fresh false claim is the worst
   available outcome.
2. **Is Chunk E's replacement a weakening?** The proposal's own *Signals the
   change is wrong* names this first: a reviewer reading the new clause as
   permission to skip the scan. Read it as an adopter's security reviewer would.
   There is **no** test behind this edit, so your read is the whole guard, and
   the plan says so rather than implying otherwise.
3. **Is the frozen-file deferral right?** The plan measured that nine frozen
   files already drifted with no re-pin and that no suite node enforces the
   committed map, and **still** kept A5/A6/A8 deferred, on the accepted
   *Sequencing*'s second conjunct. That is the conservative reading. Say whether
   it is the correct one, or whether the three rows should ride the next
   supervised re-anchor.

Two further things a reviewer is invited to **strike rather than accept**: row A9
(Chunk C, row C2), and the Chunk A placement deviation that puts the rule outside
the `cairn:slot claim-check` block instead of at the proposal's literal location.

> **The landed review appends here as a `### Plan review -- <reviewer> --
> YYYY-MM-DD` sub-heading** (plus a `### Sharpening` sub-heading if it raised
> findings). **Do not rename this heading to a bare `## Plan review`.** The
> lifecycle checker matches a section *kind*, not a review: with a bare
> `## Plan review` heading, an empty section satisfies the gate.
>
> **Corrected at revision (row E2).** The plan-open note ended *"This heading is
> shaped so a placeholder cannot satisfy it"*, which is imprecise about the
> mechanism and **false once the instructed sub-heading exists**. Measured:
> `_HEADER_RE` (`tools/lifecycle_planner.py:509-515`) requires a ` -- ` (ASCII
> double-hyphen) before the tail, so `## Plan review — the brief…` — an em-dash —
> **does not parse as a section at all**. That, and not any "shaping", is why
> this heading alone does not clear the gate. But `_HEADER_RE` matches `###` as
> readily as `##`, and the checker never reads a section's body: **the
> `### Plan review -- <reviewer> -- YYYY-MM-DD` sub-heading this note instructs a
> reviewer to append clears the gate with an entirely empty body.** Nor is the
> declared tier read. The anti-placeholder property is therefore an accident of
> punctuation that survives only until the first sub-heading lands. The real
> guard is that a human reads the section.

## Code review

*Filled in after implementation commits land.* The reviewer is not the
implementing agent. Begin with `**Model**: <model or tier when known; "unknown"
if not. Do not copy-paste old model labels from past templates or archives; query
and state your actual running model identity.>` immediately below the section
header (or below a `### Code review -- <reviewer> -- YYYY-MM-DD` sub-heading).

The falsification ledger this review owes, at minimum:

* **Re-run every grep and every command this plan quotes**, against the landed
  tree, rather than re-trusting the implementing session's transcript. This plan
  asserts what is true of the tree at `8f47c76`; the code review asserts what is
  true after the chunks land.
* **Read each landed sentence against its named artifact.** For every corrected
  sentence, open the trigger it names and confirm it does what the sentence says.
  This is the rule the plan installs, applied to the commits that install it.
* **Confirm no serialized shared file rode an implementation commit** — check the
  path list of each of Chunks B, C, D and E's commits for `AGENTS.md`,
  `CHANGELOG.md`, `dev/PLANNING.md`, `docs/DOCUMENTATION_PLAN.md`, and
  `bootstrap/REANCHOR_RUNBOOK.md`.
* **Confirm A7 changed a comment and nothing else** — `git show <sha> --
  bootstrap/container/floor-gate.sh` should show one line, beginning `#`.
* **Confirm `bootstrap/PROVENANCE.md` is untouched by every commit in this
  plan.**

## Lasting-truth migration

*Filled in at archive time.* Per the
[Archive preconditions rule](../PLANNING.md#archive-preconditions-proposals-and-plans),
plans archive only after every deferred follow-up has a durable home outside the
plan. See `doctrine/plans.md` > "Lasting-truth migration doctrine" for the
`Follow-ups migrated to:` commit-body form, and `doctrine/lifecycle.md` >
"Loop-fidelity verification" for the Decision→implementation sign-off.

**Pre-declared homes**, so archive time is bookkeeping rather than recall. Each
row names where it goes and why that home and not another:

| Follow-up | Durable home | Why there |
|---|---|---|
| **Rows A5, A6, A8** — the three frozen test files (`bootstrap/tests/test_security_lint.py`, `bootstrap/tests/fixtures/skills/README.md`, `bootstrap/tests/test_python_floor.py`) | `dev/PLANNING.md`, appended to the existing **gate-reanchor-preflight posture** entry (`dev/PLANNING.md:279`) | That entry already survives its plan's archive *because its commitments are live*, and it is where the manifest's disposition is tracked. A separate board row would fragment one Maintainer decision across two places. |
| **Row B2** — the archive-commit-body auditability claim in `doctrine/proposals.md:370` and `doctrine/plans.md:611` | A **queued follow-up proposal** under `dev/proposals/`; the fence was **confirmed** by the Internal review, so no Chunk F | It is a doctrine edit into two files no accepted *Touches* line names. The proposal's own appended text warns that the sibling restatements in `doctrine/lifecycle-contract.md:137` (which restates the block *and* uses the word "auditable") and `templates/core/dev/PLANNING.md:105` (the adopter-facing twin) engage the loop-fidelity lens, so the scope needs its own artifact. **Naming a prospective proposal is not a home** — B2's own evidence establishes that — so the fallback home is a `dev/PLANNING.md` board row. **The measurement that row carries is NOT the one this plan pre-declared: see the row below.** |
| **Row B2's supporting measurement** — *"the structured `Follow-ups migrated to:` form appears in zero archive commits"* | **Re-measured at revision; the board row carries the new figure with its `as_of`, or carries "re-measure before recording" and nothing else** | The plan-open text pre-declared carrying *"0 of 9 and 0 of 12 in commit bodies, `as_of 2026-08-03`"* into a durable board row. **That is falsified at HEAD ([I6]).** Re-measured 2026-08-04 at HEAD `da2d00e`, by enumerating every commit that added a file under `dev/plans/archive/` or `dev/proposals/archive/` and grepping its body: **plans 1 of 10** archive-move commits carry the block (`b67fabc`); **proposals 2 of 21** (`bd608c9`, `9c95653`). Seven commits tree-wide carry the block; three are genuine archive commits, two of them ancestors of HEAD that landed *after* the proposal was written. This is A2's failure shape recurring — a sibling lineage's number, true when measured, false when carried — and a board row is exactly where a stale `as_of` snapshot stops being a snapshot and becomes the board's current state. **The figure is re-run at board-row time; nothing is carried from here.** It strengthens the fence rather than weakening it: a weaker evidentiary base is more reason for B2 to get its own artifact. |
| **The `dev/plans/_template.md` verification-slot instance** — *"the same ones CI enforces"* in the `verification-commands` slot, found by this plan and out of its `Touches` | `dev/PLANNING.md` board row | **Reason corrected at revision ([I7]).** The plan-open reason — *"it needs the adopter-vs-Cairn boundary drawn … a real design question, not a typo"* — is false: `templates/core/dev/plans/_template.md:226-231` is an **unfilled placeholder** and the sentence does not exist in the adopter template. There is no boundary to draw; it is a Class-A typo in Cairn's own filled slot. The real reason to route it: it is outside this plan's `Touches`, and a one-line template edit **cascades into 19 live plans** (`git ls-files \| xargs grep -ln "the same ones CI"` → **20** files at HEAD `da2d00e`, all under `dev/plans/`; the Internal review measured 7 a day earlier — the set grows as plans open, so the board row records the command, not the number). That needs its own serialization point. |
| **Row B3 (new)** — the axis-2 Class-B instance at `doctrine/runtime-contract.md:202-211`: *"the **release floor gate** … In the release gate, an unresolvable `vermin` is an explicit **FAILURE**"*, gate vocabulary for a script nothing automatic runs | `dev/PLANNING.md` board row, with the quoted passage and its file | Found by this plan, in a file already inside `Touches`, but on a **different axis and a different class** from the accepted ledger — so unlike A9 it is a scope expansion, and the Internal round declined a second review, leaving no reviewer to ratify it before implementation. Recording it with the quote means the next lineage does not re-derive it. **It is also the one row that becomes *more* visible after this plan lands**, since Chunk B puts `recipe.md` in the opposite vocabulary. |
| **Row E2 (new, routed in)** — the review-before-implement gate is presence-only and tier-blind (`tools/lifecycle_planner.py:693`, `:787`, `:785`/`:853`; byte-twin at `templates/skills/_lib/lifecycle_planner.py`) | **Two homes, because it has two halves.** *Code*: the `planner-line-semantics` lineage, which owns `lifecycle_planner.py`. *Prose + measurement*: a `dev/PLANNING.md` board row carrying the measured table from *What changed* > 6 | The code fix changes a shipped verifier and its adopter-installed twin, which the accepted contract (*"Nothing that executes changes"*) forbids this plan. The prose fix would have to touch `doctrine/lifecycle.md` **and** `doctrine/plans.md` together — and the second is fenced by B2 — so a partial correction reproduces the very "correcting one leaves the other overstating" failure Chunk D exists to avoid. **The board row is not optional**: this finding was already routed once, from `planner-line-semantics` to here, and a second undocumented hand-off is exactly the "routed finding lost at the seam" failure mode the proposal names. |
| **The unrun-`security_check.py` recursion** — after Chunks D and E, three documents point at `bootstrap/security_check.py`, and nothing runs it; `SECURITY.md:59-63` is a human checklist | `dev/PLANNING.md` board row, framed as a candidate proposal | It is the general form of [I1], [I2] and row E2, and it is worth more than any of them individually: Cairn's enforcement claims bottom out in a script no trigger invokes. This plan's rule says the check *recurses until it reaches a human or a machine*; here it reaches a human. Whether that deserves its own artifact is a Maintainer call, and a board row is what keeps the observation from dying with this plan. |
| **The third axis, unrun** — *does the named trigger contain the procedure, and does the record bear out the obligation* | `dev/PLANNING.md` board row, framed as a candidate proposal | The appended section produced two rows from one external pass at it. That hit rate is the argument; the work is a separate proposal. |
| **The behavioural axis (axis 2), still sampled** | Same board row as the third axis | Both are "finish the sweep" work of the same shape. |
| **Row E1 — DISCHARGED** | The archive commit body's `Follow-ups migrated to:` block, naming `release-authenticity` Chunk E, commit `b93f8e9`, and the archive precondition it satisfies | The Response's binding requires exactly this: *"Whichever occurs is recorded in the archive commit body as the `Follow-ups migrated to:` disposition for Row E1."* The disposition is **the successor landed**, not the fallback wording downgrade. |
| **Row F1 — DISCHARGED** | The archive commit body, naming commit `58c7ba5` | It was a *received* hand-off from `fork-advisory-semantics`'s R8 row. Recording its closure in this lineage's archive is what stops it looking open in the sending artifact. |
| **Row A9** — if the reviewer strikes it | `dev/PLANNING.md` board row with the quoted line and its file | So a struck row is a recorded decision, not a lost measurement. |

**The archive precondition this plan inherits.** The proposal does not archive
while `bootstrap/PROVENANCE.md` asserts verified release-tag signing that no
shipped checker performs. *What changed since the proposal was written* > 1
records the verification that it is satisfied. **That verification is re-run at
archive time, not carried forward from this plan** — the file could move again.

This section is append-only once written.

## Plan review -- Claude (Internal, same-agent-type; security lens) -- 2026-08-03

**Model**: Claude Opus 5.

*Heading date carried verbatim from the review brief. This pass was actually
run and appended **2026-08-04**, and every figure below is `as_of 2026-08-04`
under the canonical interpreter (`~/conda_envs/lhm/bin/python3.13`, Python
3.13.13). Recorded rather than silently relabelled, for the same reason the
plan's own `Opened:` field records both anchors.*

*Placement note: the plan's own instruction asks a landed review to append as a
`### Plan review -- <reviewer> -- YYYY-MM-DD` **sub-heading** under the existing
`## Plan review — the brief…` section. The review brief specified this `##`
heading. It is not a bare `## Plan review`, so the anti-placeholder shaping the
plan describes is not defeated; if the Maintainer prefers the sub-heading form,
demote it — no content changes.*

### Standing

Fresh session, not the implementing agent, **same agent type as the plan's
author** (Claude Opus 5 reviewing Claude Opus 5). That meets the declared floor
— `required(Internal)`, whose floor is *the same agent in a fresh session* —
so **this discharges the plan's declared tier**, and the plan's four
prerequisites (E1/F1 verified independently, A9 ratified or struck, the B2
fence answered, the third clause decided) are all answered below.

What it does not buy is independence of *threat model*. There is **no
cross-type independence here**: the way I decide what counts as an enforcement
claim, what counts as a trigger, and what counts as "verified" is the author's
way. A blind spot the author has, I probably share. Concretely: I found the
defects below by *re-running and opening the named artifacts*, which is the
plan's own method turned on the plan. I did **not** bring a different method,
and I cannot tell you what a different method would have found. The plan's
own *Known omissions* 1 and 2 — the unrun behavioural and third axes — are
exactly where a same-type read is weakest, and I did not close them.

I also did not touch, stage, or commit any file but this one.

### Steelman

This is the strongest plan I have read in this repository at measuring its own
claims, and three things in it are exemplary and should survive review intact.

1. **It caught its own source proposal shipping a false claim.** *What changed*
   > 5 finds that A2's supporting sentence (*"Nothing in the suite or in
   `scripts/` invokes either script"*) went false between proposal-accept and
   plan-open because `b93f8e9` landed `bootstrap/tests/test_verify_ref.py`,
   and it refuses the naive correction that would have shipped a *new* false
   claim inside the commit that exists to remove false claims. I verified the
   whole chain: `_extract_marked` (`bootstrap/tests/test_verify_ref.py:999`),
   `_replay_pin` (`:1008`) and the module's own words at `:1012`, and
   `test_provenance_path_is_exercised_without_acceptance_sh` at `:1079` with
   its `assert "--unprovenanced" in ACCEPTANCE.read_text()` at `:1088`. The
   distinction the plan draws — *the suite replays the assertions, it never
   runs the gate* — is exactly right.
2. **It declares its own greens vacuous.** Chunk C states in terms that
   `check_cairn.py` staying green over a heading rename is worth nothing as
   evidence because there are zero inbound anchors. I reproduced all four
   greps (`rc=1` each). Almost nothing in this tree volunteers that a passing
   check proved nothing; this plan does, unprompted.
3. **It names where no closed failure mode exists and refuses to invent one.**
   `grep -rn floor-gate bootstrap/tests/` returns nothing (`rc=1`); `grep -rn
   SAFETY bootstrap/tests/` returns exactly one hit, a docstring line at
   `bootstrap/tests/test_generated_output_scan.py:114`. Both reproduce. The
   plan says the reviewer is the entire guard and adds no decorative test —
   and its bar for any future prose gate ("derive its oracle from something
   the subject does not read"; "be shown RED by perturbing the hazard") is the
   correct bar, stated on the record.

The five *What changed* re-measurements also hold: E1 discharged, F1
discharged, `bootstrap/SAFETY.md` rebased, both axis-1 sweeps reproducing at
**17** and **24** files, and the `162 → 164` manifest transition at `e45e1fc`.
Every one of those I re-ran; every one reproduced. The findings below are what
survived that.

### Concerns

---

**[I1] — CONFIRMED — Chunk D's acceptance criterion names a guard that does not
run on either file Chunk D edits, and reads a marker's *presence* as proof a
lens *governs*. This is the F1 defect reproduced inside the plan's own
verification.**

The plan says (Chunk D acceptance):

> `check_cairn.py` → green. This chunk is the one place where that command is a
> **real** check rather than a vacuous one: `bootstrap/fidelity-check.md:42-52`
> is the document describing the very lens `check_cairn.py` implements, and it
> carries a live `cairn-internal-ref` marker at line 52 whose text the edit sits
> next to.

Three things are wrong, in ascending order of weight.

* The marker is at `bootstrap/fidelity-check.md:55`, not 52. Line 52 is prose.
* It is **not live**. `scripts/check_cairn.py:507-508` gates the lens:
  `if _is_template_instruction(rel): _check_dangling_internal_refs(...)`, and
  `_is_template_instruction` (`scripts/check_cairn.py:286`) is
  `return rel.startswith('templates/')` (`:293`). Neither
  `bootstrap/fidelity-check.md` nor `doctrine/lifecycle.md` is under
  `templates/`. The marker's own inline reason text says so: *"fidelity-check.md
  is bootstrap-internal, not an installed adopter surface."* It exempts nothing,
  because nothing is being applied.
* Therefore `check_cairn.py` over Chunk D is **exactly as vacuous as over
  Chunk C** — the "one place where that command is a real check" claim is
  false, and it is the only place in the plan where a vacuous green is
  presented as a guard.

Perturbation, run against the **real** `check_cairn.check_tree` (the fixture
tree is mine; the checker is not a reconstruction):

```
templates/x.md -> FLAGS:
     path | [loop-fidelity] adopter-facing surface references Cairn-internal-only
            path `doctrine/lifecycle.md` -- it dangles once installed
bootstrap/y.md -> no flags
```

Two files, byte-identical bodies, differing only in directory. The lens fires
under `templates/` and is silent under `bootstrap/`.

Why this is the sharpest finding rather than a citation nit: the plan's own
argument for the rule's third clause is that *"a path that resolves is not a
trigger that governs"* — F1 slipped past `claim_check.py` **precisely because
the path resolved**. Here the plan committed the same-shaped error one level
up: *a marker that is present is not a lens that runs*. It is the recurring
failure the review brief asked me to hunt, and it is in the acceptance criteria
of the chunk that installs the fix for it.

**Fix**: strike the "real check" sentence and give Chunk D the same honest
disclosure Chunk C already carries — `check_cairn.py` over these two files
checks links, claim-paths, counts and content, and nothing about the trigger
clause. If the author wants a real guard here, the only one available is the
code review opening `bootstrap/security_check.py` and confirming the clause.

---

**[I2] — CONFIRMED — the trigger clause Chunks D and E install names a trigger
that is itself only a human remembering, which is the sentence the new rule
exists to force.**

The clause, landing in three places (`doctrine/lifecycle.md`,
`bootstrap/fidelity-check.md`, and inside Chunk E's `bootstrap/SAFETY.md`
replacement):

> — when run: `python scripts/check_cairn.py`, at review time and in the release
> gate (`bootstrap/security_check.py` runs it).

Both halves of the plan's verification table are true — `run_check_cairn()` at
`bootstrap/security_check.py:214` executes the script, and
`bootstrap/security_check.py:226` composes it as `run_bandit() |
run_check_cairn()`. What the table does not ask is the next question the new
rule makes mandatory: **what runs `security_check.py`?**

Measured: nothing automatic. The two installed hooks are
`tools/intent.py _precommit_check` and `tools/intent.py _auto_release`
(`|| true`) — the plan verified this itself and it reproduces. `grep -n
security_check tools/intent.py` returns nothing. No test, no script, no forge
config invokes it. `SECURITY.md:63` places it under *"Release security
checklist — Before cutting a release, run — and record the output in the
release notes"*. It is a checklist line a person remembers.

The new rule says: *"A check whose only trigger is a human remembering is
described that way."* Chunk E's prose gets this right ("neither fires on a
commit"; "Running it is the reviewer's obligation"). **Chunk D's clause does
not** — "at review time and in the release gate" reads as one manual trigger
and one automatic one, and a reader who opens `bootstrap/security_check.py`
finds a function, not a trigger.

**Fix**: one word, in both Chunk D files — *"…and in the maintainer-run release
gate"* or *"…in the release checklist (`bootstrap/security_check.py` runs it,
when a maintainer runs that)"*. Cheap, and it is the difference between the
plan installing its rule and the plan violating it in the commit that installs
it.

---

**[I3] — CONFIRMED — C1 names a trigger that returns green without checking,
and the plan's named perturbation validates the author's `PATH` rather than the
claim.**

C1's replacement: *"It runs only in Cairn's own test suite
(`bootstrap/tests/test_python_floor.py`, run by `python -m pytest
bootstrap/tests`)"*.

Measured. `vermin` is **not importable by the canonical interpreter**:

```
$ ~/conda_envs/lhm/bin/python3.13 -c "import shutil,importlib.util; \
    print(shutil.which('vermin'), importlib.util.find_spec('vermin') is not None)"
/Users/kendal30/conda_envs/miniforge3/bin/vermin False
```

It resolves only because the ambient shell `PATH` carries a *different* conda
environment. Perturbing the hazard rather than the test:

```
$ ~/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests/test_python_floor.py -q -rs
2 passed in 0.69s

$ PATH=/usr/bin:/bin ~/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests/test_python_floor.py -q -rs
ss
SKIPPED [1] bootstrap/tests/test_python_floor.py:158: vermin is not installed; ...
SKIPPED [1] bootstrap/tests/test_python_floor.py:188: vermin is not installed; ...
2 skipped in 0.02s
```

So the trigger C1 names **returns success without testing the claimed property**
in any environment without `vermin` on `PATH` — verbatim the hazard the new
rule's second half calls *"a worse defect than no tool, because it is silent."*
`doctrine/runtime-contract.md:193-194` discloses the graceful skip;
`bootstrap/DEPENDENCY_BUDGET.md`'s Exception-2 body (lines 99-103) does not,
and C1 is the sentence that names the trigger there.

The plan's acceptance criterion is *"Re-run … and record the result … if it now
skips, the sentence changes."* That is the artifact-supplies-its-own-oracle
shape: it measures whether the **author's environment** has `vermin`, not
whether the sentence is true for the reader it is written for. It would have
been green on 2026-07-22, is green today, and would be green on a machine where
the check has never once actually run.

**Fix**: C1 gains the disclosure — e.g. *"…run by `python -m pytest
bootstrap/tests`, which **skips (green) when `vermin` is not on `PATH`**"*.
That is the second clause of the plan's own new rule applied to the plan's own
sentence. And the acceptance criterion should be the two-run form above, not
the one-run form.

---

**[I4] — CONFIRMED — the frozen-file figure is contaminated by another
workflow's uncommitted edits, and "nine other commits" is wrong by 3×; the plan
refuses a suite figure for exactly this reason and then asserts this one.**

The plan reports: *"frozen entries: 164 / mismatches: 9"*, then argues the
deferral *"does not stop applying because **nine other commits** already drifted
the map."*

Re-measured, splitting the working tree from HEAD:

```
frozen entries: 164
working-tree mismatches: 9      <- reproduces the plan exactly
HEAD (committed) mismatches: 6
```

The three that vanish — `bootstrap/tests/test_lockfile_module.py`,
`bootstrap/tests/test_verify_integrity.py`, `bootstrap/verify_integrity.py` —
are all in `git status --short` right now as **another workflow's uncommitted
edits**. They are not drift; they are someone else's open work in progress.

And the committed drift came from **three** commits, not nine:

```
1dabe4d byline-classification ......... bootstrap/tests/test_lifecycle_contract.py
5c91c23 scan-coverage ................. bootstrap/security_check.py
                                        bootstrap/tests/test_security_check.py
                                        bootstrap/tests/test_security_lint.py
7066489 quality_gate R6 ............... bootstrap/tests/test_quality_gate_redundancy.py
                                        scripts/quality_gate.py
```

"Nine other commits" conflates the unit (files, not commits) *and* inherits the
contamination. The plan's *Verification* section says, correctly and in bold,
that **no suite figure is asserted** because *"a suite figure taken in that
state measures someone else's in-flight work."* The same tree produced this
figure, and it was asserted. That asymmetry is the finding; the disposition
(keep A5/A6/A8 deferred) is unaffected and I agree with it — see the answer to
the plan's question 3 below.

One fact the plan should record while correcting the number: **A5's own file,
`bootstrap/tests/test_security_lint.py`, is among the committed drift** — the
sibling `scan-coverage` (`5c91c23`) edited that exact frozen file after the pin
and did not re-pin it. That does not make working around the HOLD right, but it
means the "no exception for me" framing is describing a HOLD that was not, in
fact, held for that file by the lineage that landed hours earlier.

---

**[I5] — CONFIRMED — the proposed `CHANGELOG.md` line overstates by three, in
the release note whose subject is "Enforcement claims name their trigger."**

The line says: *"Corrected **nine** documented checks that described themselves
in the vocabulary of an automatic gate — **eight** naming a CI this repository
does not have."*

Nine is right (A1, A2, A3, A4, A7, A9, B1, C1, C2). Eight is not. Grepping each
landing row's target line for the standalone `CI` token:

| Row | Line | Names CI? |
|---|---|---|
| A1 | `bootstrap/DEPENDENCY_BUDGET.md:101` | yes |
| A2 | `bootstrap/container/recipe.md:152` | yes |
| A3 | `bootstrap/container/recipe.md:147` — *"(the F4 acceptance gate runs here)"* | **no** |
| A4 | `doctrine/runtime-contract.md` lines 46, 185, 189 | yes |
| A7 | `bootstrap/container/floor-gate.sh:5` | yes |
| A9 | `bootstrap/DEPENDENCY_BUDGET.md:97` | yes |
| B1 | `bootstrap/SAFETY.md:120-121` | **no** |
| C1 | `doctrine/lifecycle.md:218-221` | **no** |
| C2 | `bootstrap/fidelity-check.md:42-48` | **no** |

**Five**, not eight. "Eight" is the proposal's count of Class-A *instances*
(A1–A8) — three of which (A5, A6, A8) this plan explicitly **defers**. As
drafted, the changelog credits the commit with corrections it does not make.

**Fix**: *"— five naming a CI this repository does not have; three further
instances (`bootstrap/tests/`) are deferred behind the frozen-file manifest."*

---

**[I6] — CONFIRMED — B2's central evidentiary claim is falsified at HEAD, and
the plan pre-declares carrying it, unmeasured, into a durable board row.**

The proposal's B2 rests on: *"**Neither side has ever used the commit-body form
the doctrine specifies**"* and *"the structured form appears in zero archive
commits."* The plan's *Lasting-truth migration* pre-declares the fallback home
as *"a `dev/PLANNING.md` board row carrying the measurement (… 0 of 9 and 0 of
12 in commit bodies, `as_of 2026-08-03`)."*

Measured at HEAD:

```
$ git log --all --grep="Follow-ups migrated to" --format='%h %ad %s' --date=short
b67fabc 2026-08-03 dev/plans: archive gate-reanchor-preflight (trust root established)
bd608c9 2026-08-03 dev/proposals: archive the superseded contributor-entry
9c95653 2026-08-03 dev/proposals: archive the superseded yaml-parser-divergence
3cda505 2026-08-03 dev/proposals: Maintainer Decision -- ACCEPT release-security-bar
8f47c76 2026-08-03 dev/proposals: Maintainer Decision -- ACCEPT dependency-advisory-coverage
a59a6dd 2026-08-03 dev/PLANNING: home the conda advisory gap as a deferred follow-up
a1f9696 2026-06-04 Fold richer lifecycle-template doctrine up from the modflow_tools adopter
```

Seven commits carry the structured block; **three of them are genuine archive
commits** — one plan archive (`b67fabc`) and two proposal archives (`bd608c9`,
`9c95653`). `bd608c9` and `8f47c76` are both ancestors of HEAD that landed
*after* the proposal was written. The count is not zero.

This is A2's failure shape recurring: a sibling lineage's number, true when
measured, false by the time the plan carries it — and this one is scheduled to
be written into `dev/PLANNING.md`, where a stale figure stops being an `as_of`
snapshot and starts being the board's current state.

It strengthens the fence rather than weakening it (a weaker evidentiary base is
more reason for B2 to get its own artifact, not less), but the number must be
re-measured before it lands anywhere durable. **Fix**: re-run the grep at
board-row time and record the real ratio, or record "re-measure before
recording" and nothing else.

---

**[I7] — CONFIRMED — the `dev/plans/_template.md` routing rests on a claim the
tree contradicts, and the instance count is 7, not 1.**

The plan says of the `verification-commands` slot's *"the same ones CI
enforces"*:

> The slot is Cairn's own copy of a template block written for adopters, who do.

and, in *Lasting-truth migration*:

> it needs the adopter-vs-Cairn boundary drawn: the sentence is *correct* for an
> adopter with CI and *false* for Cairn's own copy. That is a real design
> question, not a typo.

Measured: `templates/core/dev/plans/_template.md:226-231` — the adopter-facing
slot — is an **unfilled placeholder**: *"(Adopter-specific verification commands
— the test-runner invocation + expected scope … Fill with the project's
commands, or replace with `N/A`.)"*. The sentence does not exist in the adopter
template. And:

```
$ git ls-files | xargs grep -ln "the same ones CI"
dev/plans/_template.md
dev/plans/agent-context-scrub.md
dev/plans/byline-classification.md
dev/plans/fork-advisory-semantics.md
dev/plans/profile-parse-fail-open.md
dev/plans/release-authenticity.md
dev/plans/scan-coverage.md
```

Seven files, all Cairn's own. There is no adopter-vs-Cairn boundary to draw —
the adopter's copy is a placeholder. It **is** a typo-class Class-A instance in
Cairn's own filled slot, propagated into six live plans.

Routing it out on the *Touches* ground is still correct and I do not ask for
the fence to move. But the stated *reason* is a false claim, in a plan whose
subject is not shipping false claims, and it is the plan's own found instance —
the one place where "noticing it and not fixing it is the correct move" has to
be right about what it noticed. **Fix**: replace the reason with the real one
(outside `Touches`; a template edit that would cascade into six live plans
needs its own serialization point) and correct the count to 7.

---

**[I8] — CONFIRMED — a live gate-phrased claim about *the same script Chunk B
is de-gating*, 14 lines below the heading Chunk C renames, in a file already
inside `Touches`.**

`doctrine/runtime-contract.md:202-210`:

> The `vermin` syntactic check is the unit-suite mechanism. The **release floor
> gate** is stronger (`bootstrap/container/floor-gate.sh`): … **In the release
> gate**, an unresolvable `vermin` is an explicit **FAILURE**, never a silent
> skip-as-pass …

Axis 1 cannot see it — no `CI` token. But it is Class B on the plan's own
taxonomy ("gate-phrased obligation with no trigger"), and it is about
`floor-gate.sh`, the *exact* script Chunk B is simultaneously correcting to
*"run by the maintainer from a Cairn checkout … not by anything automatic
here."* After Chunk B lands, `bootstrap/container/recipe.md` and
`doctrine/runtime-contract.md` describe the same script in contradictory
vocabulary, and Chunk C's commit will touch that file three times without
touching this.

Consequently the section heading *"One un-ledgered instance, in a file already
inside `Touches`"* overstates. It is one un-ledgered **axis-1** instance; a
five-minute axis-2 read of the section Chunk C edits produces another.

**Fix**, cheapest first: (a) qualify the heading to "one un-ledgered axis-1
instance"; and (b) either add a one-line qualifier at `:203` in the Chunk C
commit ("the release floor gate — run by the maintainer, not by anything
automatic"), or record it in *Known omissions* as seen-and-left with a board
row. Silently leaving it is the one option that reproduces the defect.

---

**[I9] — precision and criterion defects, grouped. None changes a disposition;
all are one-line fixes and several would otherwise land as text.**

*Citations that do not resolve where the plan says:*

1. **Chunk B row B1 cites `bootstrap/container/recipe.md:152-153`.** The
   sentence being replaced **begins at line 151** (*"The **floor gate**"*).
   Line 153 holds the tail of the replaced sentence *and* the head of the
   Class-D sentence to preserve. A line-anchored edit starting at 152 orphans
   "The **floor gate** (`bootstrap/container/floor-gate.sh`) and the
   **acceptance". Cite 151-153.
2. **`bootstrap/fidelity-check.md` marker is at line 55**, not 52 (see [I1]).
3. **`scripts/check_cairn.py` "accepts `--no-content-scan` (line 560)"** — 560
   is the *consumption* site (`content_scan_enabled=not args.no_content_scan`);
   the flag is declared at `scripts/check_cairn.py:532`.
4. **`bootstrap/tests/test_skills_security.py` "loads … and scans the canonical
   skills artifacts (lines 9, 42)"** — line 9 is a docstring line and 42 is a
   path constant. The load is `scripts`-style `_load(...)` at line **60**; the
   scans are at lines **71** and **82**.
5. **"five chunks and eight files"** — the chunk tables name **nine** distinct
   files (`AGENTS.md`, `recipe.md`, `floor-gate.sh`, `DEPENDENCY_BUDGET.md`,
   `runtime-contract.md`, `lifecycle.md`, `fidelity-check.md`, `SAFETY.md`,
   `CHANGELOG.md`). The parenthetical *"of which two (`AGENTS.md`,
   `CHANGELOG.md`)"* is what gives it away: eight is the proposal's `Touches`
   count, which does not include `CHANGELOG.md`.

*Acceptance criteria that do not do what they are asked to do:*

6. **Chunk D's clause has no stated insertion point in
   `bootstrap/fidelity-check.md`, and the two host sentences are not parallel
   where the plan assumes.** In `doctrine/lifecycle.md:221` the sentence *ends*
   at *"dangles once installed."*, so the clause appends cleanly. In
   `bootstrap/fidelity-check.md:47-48` the same phrase is **mid-sentence** —
   *"…dangles once installed in an adopter — the failure that produced fold-back
   #57 and the un-shipped 9-lens review roster."* Appending the em-dash clause
   at end-of-sentence attaches "when run" to *"roster"*, not to *"fails
   closed"*. Name the insertion point explicitly, or the "same clause in both
   places" instruction produces a sentence that says the wrong thing.
7. **Chunk B's "invocation check" is a *mention* grep.** It reproduces exactly
   (the 8 expected files, verified), and it catches a *new file* referencing
   either script. It cannot catch **a new invocation added inside a file
   already on the list** — if `bootstrap/tests/test_verify_ref.py` began
   running `acceptance.sh` wholesale tomorrow, the grep output is byte-
   identical and the criterion passes. Add "and read each hit in context" to
   the criterion; the plan already did that work for
   `bootstrap/container/Dockerfile:78` and `bootstrap/container/acceptance.sh:8`
   and got both right, so this is codifying what the author already did.
8. **Chunk B's `bash -n` is near-vacuous and its "exactly one changed line"
   criterion has a measured cost.** A `#`-comment edit cannot break bash syntax
   unless the `#` itself is removed. More usefully: line 5 is currently
   **80 chars** and the comment block is 80-wrapped; B3's replacement makes it
   **105 chars**. "Exactly one changed line" therefore forbids re-wrapping and
   mandates a 105-char line in an 80-wrapped block. State which you want —
   either is fine, but the criterion as written silently decides it.
9. **Chunk E's manual-only enumeration under-counts.** The clause says *"Source
   prose that no scaffolded profile emits — `doctrine/`, `docs/`,
   `case-studies/`, this document — is reached **only** by that manual run."*
   `bootstrap/tests/test_generated_output_scan.py` scaffolds three
   **representative** profiles (minimal, representative team, adversarial), so
   the manual-only set also includes `on-ramp/`, root `README.md` /
   `SECURITY.md`, `bootstrap/*.md`, `dimensions/`, `examples/`, and any
   `templates/modules/` prose those three profiles do not emit. In a security
   document, an appositive list that reads as exhaustive and understates the
   uncovered surface errs in the wrong direction. Make it *"including"*.
10. **Chunk A's acceptance omits `scripts/token_budget.py`** — the one tool
    whose stated purpose is measuring the always-on prefix Chunk A grows.
    Today: `AGENTS.md` 5,014 tok of a 5,541-tok always-on manifest (chars/4
    proxy). The rule adds ~120 tok, ~2%. It is a soft cap and will not block;
    running it is one line and it is the measurement the surface has.

---

### The security-lens read on Chunk E — the plan's question 2

**Yes, it is a weakening — in one specific, fixable respect, and the plan's own
recovery line already names the fix.**

Every *factual* claim in the replacement holds. I verified all five
independently and they are in *Covered* below. The defect is modal, not
factual.

Current (`bootstrap/SAFETY.md:119-121`): *"…and **must pass** the
content-integrity scanner…"* — an obligation **with a pass criterion**.

Proposed: *"— and **is scanned with** the content-integrity scanner … Running
it is the reviewer's obligation, not a mechanism's guarantee."*

The obligation survives, but it has been transferred from *passing* to
*running*. A reviewer who runs `content_scan.py`, reads the flags, and ships
has satisfied the new sentence's letter. In an adopter-facing security document
about a supply chain of agent-executed instructions — where the threat is a
hidden instruction reaching *"every downstream adopter's agents at once"*
(`bootstrap/SAFETY.md:114-115`) — that is the wrong direction to move, and it
is the plan's own named *"Open (degrades)"* failure mode arriving as designed
rather than as an accident.

The plan's stated recovery is exactly right: *"restore the imperative and add
the trigger as a separate sentence, keeping 'must' intact."* **Require it up
front rather than holding it as recovery.** Suggested shape, preserving
everything the plan gained:

> …and **must pass** the content-integrity scanner (`content_scan.py`, run by
> [`check_cairn.py`](../scripts/check_cairn.py)). **Two triggers exist and
> neither fires on a commit**: the suite scans generated output and the skills
> artifacts on every `pytest` run, and `check_cairn.py` scans every tracked
> Markdown file when a person runs it (the maintainer-run release gate
> `security_check.py` runs it). Source prose that no scaffolded profile emits —
> including `doctrine/`, `docs/`, `case-studies/` and this document — is reached
> **only** by that manual run. **Running it, and resolving what it flags, is the
> reviewer's obligation, not a mechanism's guarantee.**

That keeps "must pass", closes [I2] and [I9.9] in the same edit, and restores
the live link to `../scripts/check_cairn.py` that the plan's replacement silently
drops (a link `check_cairn.py`'s own link-checker currently resolves).

On the `--no-content-scan` residual the plan surfaces: **leave the clause as
the plan has it.** The plan is right that the precision buys nothing. But
`bootstrap/security_check.py:221` invokes the script with **no flags**, so the
release gate always scans — worth one clause in the plan's record, since that
is the fact that makes the residual harmless.

---

### Answers to the four questions the plan routes to this review

1. **E1 and F1 — both DISCHARGED. Verified independently, not from the plan.**
   `bash bootstrap/container/verify-ref.sh . v0.3.0` → `exit=1` with the REFUSED
   message (captured without a pipeline); `git verify-tag v0.3.0` → *"no
   signature found"*, exit 1. `bootstrap/PROVENANCE.md:37-41` carries the
   date-boundary table marking `v0.2.0`/`v0.3.0` unsigned and unverifiable;
   `:51-60` records the second branch retired outright; `:114` carries the
   *"Recorded as not established"* disclosure. `AGENTS.md:335-345` at HEAD says
   the opposite of what F1 quoted, names `_ast_attest._UPDATE_ALLOWLIST` and
   precedent `c3d5bd9`, and states *"No runbook covers it yet."* Both `b93f8e9`
   and `58c7ba5` are ancestors of HEAD (`git merge-base --is-ancestor` → yes).
   **The archive precondition is satisfied**, and the plan's instruction to
   re-verify at archive time rather than carry this forward is the right
   handling — `bootstrap/PROVENANCE.md:41` asserts `v0.4.0 and later` are signed
   and verifiable, and that row becomes a present-tense false claim the moment
   an unsigned `v0.4.0` ships.

2. **Row A9 — RATIFIED into Chunk C.** It is the same claim, in the same file,
   **four lines above** the row already accepted; landing A1 and leaving line 97
   reading *"floor CI check"* ships an internally contradictory document from
   the commit that exists to remove them. I confirmed the heading rename is
   anchor-safe: `grep -rn "exception-2" --include="*.md" .` → `rc=1`, and
   `grep -rn "DEPENDENCY_BUDGET.md#"` → `rc=1`. The plan's refusal to inflate
   the cleared rate-limit count with it is correct and should stay.

3. **The B2 fence — CONFIRMED, do not lift it.** Three reasons, one of them the
   plan's and two of them mine. (a) The plan's: no accepted `Touches` line names
   `doctrine/proposals.md` or `doctrine/plans.md`, and the proposal itself calls
   the expansion the reviewer's to ratify. (b) The restatement hazard is
   **real**, and I checked it rather than taking it: `doctrine/lifecycle-contract.md:137`
   restates the block *and uses the word "auditable"*, and
   `templates/core/dev/PLANNING.md:105` carries the adopter-facing twin. Editing
   only two of four surfaces leaves the doctrine disagreeing with itself across
   an install boundary — which is the loop-fidelity lens, which this plan
   correctly states it is not engaging. (c) **B2's evidence needs re-measuring
   before anything is written on its strength** — see [I6]. A doctrine edit whose
   supporting count is falsified at HEAD is not ready to ride a fenced-out chunk.

4. **The rule's third clause — INCLUDE it**, verbatim as the proposal drafted
   it. The argument is no longer hypothetical: **[I1] and [I2] are both
   third-clause findings.** Chunk D's acceptance named a marker that resolves
   and a lens that does not run; Chunk D's clause named a release gate that
   exists as a function and not as a trigger. A two-clause rule catches neither,
   because in both cases the named artifact is *there*. One condition on
   including it: it applies to this plan's own acceptance criteria from the
   moment it lands, which is what [I1], [I2] and [I3] are asking for.

5. **The frozen-file deferral (the plan's question 3) — the deferral is
   CORRECT; its stated basis is not.** Keep A5, A6, A8 deferred: the accepted
   *Sequencing*'s second conjunct is plainly unmet
   (`bootstrap/tests/fixtures/gate_manifest.json` exists, carries 164 entries,
   and all three paths are literal keys), and the plan is right that a lineage
   does not get to grant itself the exception the ledger it is executing would
   flag. But the supporting sentence must be corrected per [I4] — **six** files
   across **three** commits, not nine commits — and the plan should record that
   A5's own file is one of the six, drifted by the sibling `scan-coverage`
   without a re-pin. I also confirm the plan's mechanism claim: `test_gate_manifest.py`
   builds its expectation from `G.produce(_REPO)` on the working tree
   (`bootstrap/tests/test_gate_manifest.py:33`) and verifies against *that*, so
   no suite node can redden on committed-map drift. That claim is exact.

### Covered

Everything below was executed in this session against the working tree.
**HEAD is `eacb7dd`, one commit past the `8f47c76` the plan measured at**;
`git diff --name-only 8f47c76 HEAD` → `dev/NEXT_SESSION.md` only, so none of
the plan's measurements are invalidated by the move.

**Mandated checkers.**

```
$ ~/conda_envs/lhm/bin/python3.13 scripts/claim_check.py dev/plans/gate-claims-vs-enforcement.md
claim_check: dev/plans/gate-claims-vs-enforcement.md -- OK, no claim-check flags.   (rc=0)

$ ~/conda_envs/lhm/bin/python3.13 scripts/check_cairn.py dev/plans/gate-claims-vs-enforcement.md
check_cairn: OK -- 1 Markdown file(s) scanned; no issues.                            (rc=0)

$ ~/conda_envs/lhm/bin/python3.13 scripts/check_cairn.py          # tree-wide
check_cairn: OK -- 180 Markdown file(s) scanned; no issues; 68 external link(s) not probed.
```

**Reproduced, matching the plan exactly.** Both axis-1 sweeps (**17** Markdown,
**24** source files); `find .github -type f` → **7**, no workflow; the
pipeline-file grep → `docs/workflow-role.md` only; all four anchor greps →
`rc=1`; the Chunk B invocation grep → the 8 expected files, no more; `git
verify-tag v0.3.0` and `verify-ref.sh . v0.3.0` (exit 1, REFUSED, captured
without a pipeline); `grep -rn floor-gate bootstrap/tests/` → `rc=1`;
`grep -rn SAFETY bootstrap/tests/` → one docstring hit at
`test_generated_output_scan.py:114`; `bash -n bootstrap/container/floor-gate.sh`
→ 0; manifest `frozen entries: 164`, and `162 → 164` across `e45e1fc`;
`scripts/sync_doc_snippets.py` and `templates/modules/team-gated/sync_doc_snippets.py`
byte-identical (`cmp -s` → equal), both carrying the string at line 43;
`templates/core/AGENTS.md` standalone-`CI` count → **0**; the two installed git
hooks, verbatim.

**Line and quote citations opened and confirmed correct.**
`AGENTS.md:248` / `:266` / `:267` / `:269` / `:335-345`;
`bootstrap/SAFETY.md:120-121` (276-line file) and the `scan-coverage`
residuals block at `:170-196`; `bootstrap/DEPENDENCY_BUDGET.md` lines 97 and
101; `doctrine/runtime-contract.md` lines 46, 185, 189 and 191-195;
`doctrine/lifecycle.md:218-221`; `bootstrap/fidelity-check.md:42-48`;
`bootstrap/container/recipe.md:147` (and `:151-153`, see [I9.1]);
`bootstrap/container/floor-gate.sh:5`; `bootstrap/container/Dockerfile:78`
(a comment, not an invocation); `bootstrap/container/acceptance.sh:8` (about
the adopter fixture repo — the plan's read is right, and recording the
near-miss was the right call); `bootstrap/security_check.py` lines 214 and 226;
`scripts/check_cairn.py` lines 50 and 180; `bootstrap/_scaffold/slotmerge.py:348` and its
whitespace-collapsed substring semantics; `templates/modules/default-on/claim-check.md`
declaring **no** `cairn:merge` directives (`rc=1`); `templates/core/AGENTS.md:228-234`
being the unfilled slot; `bootstrap/tests/test_verify_ref.py` lines 999, 1008,
1012, 1079 and 1088 (1334-line file);
`bootstrap/tests/test_generated_output_scan.py` lines 32, 53, 114 and 121;
`dev/PLANNING.md:279`; `doctrine/proposals.md:370` and `doctrine/plans.md:611`
(the plan re-measured these correctly from the proposal's 360/602). The
Decision's quoted fragments all match `dev/proposals/2026-08-03-claude-gate-claims-vs-enforcement.md:1268-1309`
verbatim, and the Chunk A rule text is byte-identical to the proposal's block
quote at lines 253-260.

**Perturbations run** (the ones that carry weight, all named in *Concerns*):
the `templates/` vs `bootstrap/` internal-ref lens split, using the real
`check_cairn.check_tree` with my own fixture tree; `test_python_floor.py` with
and without `vermin` on `PATH`; the frozen-manifest hash recomputed separately
against the working tree and against `git show HEAD:<path>`.

**Scope-boundary checks that came back clean** (no finding, recorded so the
implementing agent does not re-derive them): the open siblings that name
`bootstrap/SAFETY.md` — `security-verification-activation`,
`api-web-security-modules`, `release-security-bar`, `default-security-stance`,
`content-scan-detectors`, `portable-security-sweeps` — all target **different
regions** (Rule 7's Layer-4 discussion, new rules), none the clause at
lines 120-121. No open plan cites `doctrine/lifecycle.md` near line 218
(`transition-lint` cites `:28-30`). Nothing collides on
`bootstrap/container/floor-gate.sh`. The plan does **not** absorb a sibling's
surface and does not widen past its Decision — with the single exception it
declares and routes (A9), which I have ratified. The active work-intent claim
(`claude-d8d22f62`, `files=['dev/plans']`) covers this artifact.

### Not covered / low confidence

* **The behavioural axis (axis 2) and the third axis remain unrun**, exactly as
  the plan's *Known omissions* 1 and 2 say. I did not run a systematic pass on
  either. [I2] and [I8] are both axis-2/axis-3 findings that fell out of reading
  four specific artifacts — which is weak evidence that a systematic pass would
  find more, and no evidence about how much. This is the largest uncovered
  surface and it is where a same-type reviewer is least useful.
* **The positive path of `bootstrap/container/verify-ref.sh` is untestable
  today** — no signed tag exists, so "a shipped checker performs
  signature-and-name verification" rests on the refusal path plus a code read,
  not on an observed success. The plan discloses the residual (Chunk M, not
  performed). I did not read `verify-ref.sh`'s signature logic line by line;
  that belongs to `release-authenticity`'s review, not this one.
* **I did not run the full suite.** The working tree carries another workflow's
  uncommitted edits to `bootstrap/_scaffold/`, `bootstrap/verify_integrity.py`
  and two test modules, plus untracked `bootstrap/tests/test_fork_advisory.py`.
  Any figure I took would measure their work — which is the plan's own stated
  reason for asserting none, and I am holding to it rather than quoting a
  number. The implementing agent takes the baseline on a clean tree, per the
  plan's *Verification*.
* **Chunk A's placement deviation** — I confirmed the mechanism the plan cites
  is inert today (`claim-check.md` declares no merge directives;
  `check_slot_fidelity` matches by whitespace-collapsed substring, so appending
  inside the slot would not redden anything now) and that no test compares
  `AGENTS.md` against `templates/core/AGENTS.md` structurally. **I have no
  opinion worth recording on whether outside-the-slot or the proposal's literal
  placement is better** — it is a judgment about a future merge, the plan
  reasons about it honestly and invites the strike, and a same-type reviewer
  adds nothing here. I neither ratify nor strike it; the Maintainer should
  take it.
* **`bootstrap/SAFETY.md`'s by-file-class threshold list** — I read lines
  112-200 and confirmed the clause and the `scan-coverage` block are disjoint
  surfaces, but I did not audit the list itself for correctness. Out of scope
  for this plan and unaffected by it.

### Recommendation

**Verdict: SHIP after a Response — no second plan-review round.**

The plan's structure, sequencing, chunk boundaries, fences, deferrals and
serialization handling are all correct, and I am not asking for any of them to
move. Every finding above is a correction to *text* — three of them to text
that would otherwise land ([I2], [I3], [I5]), one to an acceptance criterion
([I1]), and the rest to the plan's own record. All are one-line fixes with the
fix stated.

Four of them I ask to be treated as **binding rather than dispositionable**,
because each would ship a fresh false or weakened claim in the commit that
exists to remove them — the outcome the plan itself names as the worst
available:

* **[I1]** — strike the "real check" sentence from Chunk D's acceptance.
* **[I2]** — qualify the release gate as maintainer-run, in all three places
  the clause lands.
* **[I3]** — C1 discloses the skip-as-pass, and its acceptance criterion
  becomes the two-run form.
* **Chunk E keeps "must pass"** — the plan's own recovery, applied up front.

[I5] (the changelog count) is equally binding but lands in a serialized file the
Maintainer or orchestrator writes, so it is a correction to the returned text
rather than to a commit.

The remainder ([I4], [I6], [I7], [I8], [I9]) should be dispositioned in a
Response, accepted or refused on the record. A second review round is not
warranted: the fixes are mechanical, and this plan's **Code review** already
owes a falsification ledger that re-runs every quoted command and *"opens the
trigger it names and confirms it does what the sentence says"* — which is the
correct backstop for [I2] and [I3] specifically, and which will be performed by
a reviewer who is not the implementing agent.

One thing to carry forward past this plan, because it is the general form of
[I1], [I2] and [I3] and it is worth more than any of them: **this repository's
enforcement claims bottom out in `bootstrap/security_check.py`, and nothing
runs that either.** Chunks D and E are about to make three documents point at
it. The rule this plan installs does not stop at the first named trigger — it
recurses until it reaches a human or a machine, and here it reaches a human on
a checklist in `SECURITY.md`. Saying so plainly, once, is the honest version of
what this plan is for. Whether that recursion deserves its own artifact is the
Maintainer's call, not mine.

## Revision after Internal plan review -- Claude (author) -- 2026-08-04

**Model**: Claude Opus 5. Author role, not the reviewer. This is the Response
the review asked for (*"SHIP after a Response — no second plan-review round"*).

**Method, stated first because it is the thing this plan is about.** Every
finding below was **re-derived from the primary source before being
dispositioned** — the file, the code, the command — not from the review's
wording and not from the plan's own prose. Both are reports, and reports are
what produced these defects. Three consequences, all visible in the table:

* **Two figures the review itself asserted did not reproduce**, and are
  corrected here against the review as well as against the plan: the frozen-file
  working-tree count ([I4]: 9 → **10**, in one day) and the
  `"the same ones CI"` instance count ([I7]: 7 → **20**). Neither changes a
  disposition; both change what gets written down.
* **One criterion this plan wrote is now measurably broken** and was found by
  re-running it rather than by reading it: Chunk C's four anchor greps are
  **self-matching**, and return `rc=0` at HEAD `da2d00e` because this plan quotes
  the anchor strings. Corrected to the `dev/`-excluding form, which reproduces
  the `rc=1` the criterion depends on.
* **No accepted finding is answered in prose alone.** Each row below names the
  chunk, criterion, figure or text that changed. Where nothing changed, the row
  says *declined* and says what stands instead.

Measurement anchor for everything below: HEAD **`da2d00e`**, `as_of`
**2026-08-04**, canonical interpreter `~/conda_envs/lhm/bin/python3.13`
(Python 3.13.13). The review measured at `eacb7dd`; `git diff --name-only
eacb7dd da2d00e` touches no file this plan cites except `dev/` artifacts.

### Sharpening — finding-by-finding disposition

| # | Disposition | What changed | Figure I re-measured |
|---|---|---|---|
| **[I1]** | **ACCEPTED (binding)** | Chunk D's acceptance criterion rewritten. The *"one place where that command is a **real** check"* sentence is **struck** and replaced with the measured reason it was false, plus the honest statement that `check_cairn.py` over Chunk D checks links/anchors/claim-paths/content and **nothing about the trigger clause**. A new criterion names the only real guard: the code review opening `bootstrap/security_check.py` and `SECURITY.md`. | Marker is at `bootstrap/fidelity-check.md:55`, **not 52** (line 52 is prose). Lens gating re-derived from source: `scripts/check_cairn.py:507-508` calls `_check_dangling_internal_refs` only `if _is_template_instruction(rel)`, and `_is_template_instruction` (`:286`) is `return rel.startswith('templates/')` (`:293`). Neither Chunk D file is under `templates/`. |
| **[I2]** | **ACCEPTED (binding)** | The trigger clause is re-worded in **all three** places it lands — Chunk D's `doctrine/lifecycle.md` and `bootstrap/fidelity-check.md` text, and Chunk E's `bootstrap/SAFETY.md` replacement: *"the **maintainer-run** release checklist (`bootstrap/security_check.py` invokes it, when a maintainer runs that)"*. Chunk D gains a verification block for the recursion, and Chunk E's table gains a **maintainer-run** row. | `git ls-files \| xargs grep -ln security_check` → no test, script, hook or forge config **invokes** it; every hit is prose, docstring, manifest or deliberation. `grep -n security_check tools/intent.py` → no match. Hooks read verbatim from `.git/hooks/`: pre-commit → `tools/intent.py _precommit_check`; post-commit → `tools/intent.py _auto_release \|\| true`. `SECURITY.md:59-63` = *"Release security checklist — Before cutting a release, run"*. |
| **[I3]** | **ACCEPTED (binding)** | Row C.1's replacement text now **discloses the skip-as-pass** (*"which skips — and so passes green — whenever `vermin` is not importable or on `PATH`"*), and its acceptance criterion is replaced with the **two-run** form, both results required in the commit body. The second run **is** the hazard perturbation. | Re-ran both. `~/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests/test_python_floor.py -q -rs` → **2 passed in 0.64s**. `PATH=/usr/bin:/bin` same command → **2 skipped in 0.02s**, `SKIPPED [1] …:158` and `…:188`. `vermin` is **not importable** by the canonical interpreter (`find_spec('vermin') is not None` → `False`); it resolves only via `/Users/kendal30/conda_envs/miniforge3/bin/vermin` on the ambient `PATH`. |
| **Chunk E keeps "must pass"** | **ACCEPTED (binding)** | Chunk E's replacement clause **rewritten**. The plan-open draft is retained struck-through so the change is visible; the new text keeps *"**must pass** the content-integrity scanner"*, restores the live `[check_cairn.py](../scripts/check_cairn.py)` link the draft silently dropped, and ends *"Running it, **and resolving what it flags**, is the reviewer's obligation."* A new acceptance criterion greps the added diff for `must pass`. The *Open (degrades)* failure mode is re-labelled **fired**, with the recovery applied up front. | — (modal, not numeric). Confirmed the residual is harmless: `bootstrap/security_check.py:221` invokes the script with **no flags**, so the release gate always scans. |
| **[I4]** | **ACCEPTED** | The frozen-file block is rewritten to split working-tree from HEAD; *"nine other commits"* → **"three other commits … six frozen files"**, with per-file commit attribution. A new bullet records that **A5's own file** (`bootstrap/tests/test_security_lint.py`) is among the committed drift, edited by the sibling `scan-coverage` without a re-pin. Downstream mentions corrected (*Known omissions* 4; the `scan-coverage` question paragraph, which now shows both figures with their anchors rather than silently reconciling them). | Re-hashed against the committed map: frozen entries **164**; **HEAD mismatches 6**; **working-tree mismatches 10** — *the review measured 9; `bootstrap/tests/test_scaffold.py` joined the set in one day.* That movement is now the argument in the text. The six drifted across **three** commits, attributed by `git log e45e1fc..HEAD -- <path>`: `5c91c23` (3 files), `7066489` (2), `1dabe4d` (1). `e45e1fc` is the last commit to touch the manifest. |
| **[I5]** | **ACCEPTED (binding)** | The returned `CHANGELOG.md` line is corrected: *"eight naming a CI"* → *"**five** naming a CI this repository does not have; **three** further CI-naming instances under `bootstrap/tests/` are deferred behind the frozen-file manifest"*. The line also picks up the third clause (*"and is checked by opening it"*). A per-row derivation table is added below it. | Re-derived independently with a standalone-token regex `(?<![A-Za-z0-9_])CI(?![A-Za-z0-9_])` over each landing row's target lines: **A1, A2, A4, A7, A9 = 5**; A3, B1, C1, C2 name no `CI` token. Nine total corrected checks is unchanged and correct. |
| **[I6]** | **ACCEPTED** | The *Lasting-truth migration* B2 row is **split in two**. The pre-declared parenthetical figure is removed from the row and replaced by a dedicated row that records the re-measurement **and** the instruction that the board row re-runs it rather than carrying it. | Re-measured by enumerating every commit that **added** a file under each archive directory and grepping its body: **plans 1 of 10** archive-move commits carry `Follow-ups migrated to:` (`b67fabc`); **proposals 2 of 21** (`bd608c9`, `9c95653`). Seven commits tree-wide carry the block. The proposal's *"0 of 9 / 0 of 12"* is falsified on numerator **and** both denominators. |
| **[I7]** | **ACCEPTED — routing kept, reason replaced** | The *Verification* note's reason is rewritten: the claim that the slot is *"Cairn's own copy of a template block written for adopters, who do"* is struck, the adopter placeholder is quoted, and the real routing reason is stated (outside `Touches`; a template edit cascades into 19 live plans and needs its own serialization point). The *Lasting-truth* row is rewritten to match and now records **the command, not the number**. | `templates/core/dev/plans/_template.md:226-231` is an **unfilled placeholder** — the sentence does not exist in the adopter template. `git ls-files \| xargs grep -ln "the same ones CI"` → **20** files, all under `dev/plans/`. *The review measured 7 the previous day;* the difference is plans opened since, which is why the row now carries the command. |
| **[I8]** | **ACCEPTED — heading qualified, instance recorded, edit declined** | The section heading becomes *"One un-ledgered **axis-1** instance"*. A new subsection records the axis-2 instance as **row B3**, quoted, classed, and given a durable home; *Known omissions* gains item 6 and *Lasting-truth migration* gains a row. **The one-line qualifier at `:203` is declined**, with the reason on the record: B3 is a different class on a different axis from the accepted ledger (unlike A9, which the proposal's own *Signals* text pre-authorises), no reviewer remains in this lifecycle to ratify it, and landing a Class-B correction inside a commit whose changelog line describes Class-A corrections re-opens [I5]. Silently leaving it — the option the reviewer named as the wrong one — is not what happened. | Read at revision: `doctrine/runtime-contract.md:202-211` carries *"the **release floor gate** is stronger"* and *"In the release gate, an unresolvable `vermin` is an explicit **FAILURE**"*. It carries **no `CI` token**, which is why axis 1 cannot see it. |
| **[I9.1]** | **ACCEPTED** | Row B.1's citation `:152-153` → **`:151-153`**, with the four lines quoted and the edit re-specified as **sentence-anchored, not line-anchored**, because line 153 is split between the replaced sentence's tail and the Class-D sentence's head. | Re-read `bootstrap/container/recipe.md:151-154`. The replaced sentence begins at **151**; the Class-D sentence begins mid-**153**. |
| **[I9.2]** | **ACCEPTED** | Folded into the [I1] rewrite: the marker is cited at `bootstrap/fidelity-check.md:55`. | Confirmed: `:55` carries `<!-- cairn-internal-ref: doctrine/lifecycle.md … -->`; `:52` is prose. |
| **[I9.3]** | **ACCEPTED** | Chunk E's residual paragraph now cites the **declaration at `:532`** and the consumption at `:560`, and says which is which. | `scripts/check_cairn.py:532` = `parser.add_argument('--no-content-scan', …)`; `:560` = `content_scan_enabled=not args.no_content_scan`. |
| **[I9.4]** | **ACCEPTED** | Chunk E's verification table row for the skills artifacts is corrected, with the wrong plan-open citation quoted so the correction is auditable. | `bootstrap/tests/test_skills_security.py`: `CONTENT_SCAN_SRC` at `:42`, `_load()` defined `:50` / called `:60`, `content_scan.scan_file` at `:71` and `:82`. `:9` is a docstring bullet. Also corrected in the same table: `_scan_generated()` is `:48-55` (I had written `:48-56`) and the adversarial test is `:96` (I had written `:95`). |
| **[I9.5]** | **ACCEPTED** | *Scope* opening: **"five chunks and nine files"**, with the nine enumerated and the source of the "eight" error named. | Counted the chunk tables: 9 distinct files. Eight is the proposal's `Touches` count, which omits `CHANGELOG.md`. |
| **[I9.6]** | **ACCEPTED** | Chunk D's table rows now cite `:217-221` and `:41-48`, and a new paragraph names the insertion point **by the sentence carrying "fails closed"** in each file, with both host sentences quoted to show they are **not** parallel. The clause lands as its own sentence, at `doctrine/lifecycle.md:221` and `bootstrap/fidelity-check.md:45`. | `doctrine/lifecycle.md`: the "fails closed" sentence starts `:218` and **ends `:221`**. `bootstrap/fidelity-check.md`: the "fails closed" sentence starts `:42` and **ends `:45`**; *"dangles once installed"* is in the **next** sentence, which begins mid-`:45` (*"Such a…"*) and runs through `:48` to *"…the un-shipped 9-lens review roster."* (Both citations corrected before commit; an earlier draft said `:43` and `:46-48`.) |
| **[I9.7]** | **ACCEPTED** | Chunk B's invocation criterion now states in the criterion itself that the grep is a **mention** check, names precisely what it cannot catch, and requires **opening and reading each of the 8 hits in context**. | Re-ran the grep: the same **8** paths, unchanged. |
| **[I9.8]** | **ACCEPTED — and the choice it forced is made** | *"Exactly one changed line"* is replaced with: comment lines only, every `+`/`-` line begins `#`, **no line exceeds 83 chars**, diff confined to the header block. **The re-wrap is taken.** The `bash -n` criterion is kept but labelled near-vacuous with its one real use (catching a deleted `#`). | Measured line lengths in `bootstrap/container/floor-gate.sh`: line 5 = **80** chars; block max = **83** (lines 3, 9, 13); the drafted one-line replacement = **105** chars. |
| **[I9.9]** | **ACCEPTED** | Folded into the Chunk E rewrite: the appositive becomes *"— **including** `doctrine/`, `docs/`, `case-studies/` and this document —"*, with a paragraph naming the surfaces the three-profile scan does not reach. | `bootstrap/tests/test_generated_output_scan.py` scaffolds **three** profiles (docstring `:4-12`; tests at `:81`, `:86`, `:96`), so the manual-only set is larger than the draft's list. |
| **[I9.10]** | **ACCEPTED** | Chunk A's acceptance gains `scripts/token_budget.py`, run **before and after**, with the after-figure recorded in the serialization commit body. | Ran it: `AGENTS.md` **5,014 tok** / `CLAUDE.md` 527 / total **5,541 tok** (chars/4 proxy). The rule text as it now stands (with the ratified third clause **and** the recursion sentence) is **783 chars as written / 773 markup-stripped → ~196 tok**, ~3.5% of the manifest — larger than the review's ~120 tok estimate, because the text grew. (Corrected before commit: an earlier draft said 674 chars → ~168 tok, which is the text **without** the recursion sentence — 663 chars measured — understating the shipped rule by ~15%.) |
| **Third clause (review question 4)** | **RATIFIED — INCLUDED** | Chunk A's verbatim text now carries it, and the "open question" paragraph is rewritten to record who authorised it. Two deltas are declared as authorial: it is folded into the paragraph rather than given its own bolded lead, and it gains a **recursion sentence** (*"the check does not stop at the first named artifact: it recurses until it reaches a human or a machine"*), which is the general form of [I1], [I2] and row E2. *Known omissions* item 5 is struck as settled; a new failure-mode row isolates the recursion sentence so a Maintainer can strike it without touching the ratified clauses. | — |
| **Row A9 (review question 2)** | **RATIFIED** | Chunk C row C.2 now reads *"Row A9, ratified by the Internal review"*. The failure-mode row is updated from "authorial addition the reviewer can strike" to ratified, with the reviewer's ground recorded. The refusal to inflate the cleared rate-limit count stands unchanged. | — |
| **B2 fence (review question 3)** | **CONFIRMED** | The *Lasting-truth* B2 row records the fence as confirmed and picks up the reviewer's two independently-checked restatement sites, replacing the plan's unverified gesture at them. | `doctrine/lifecycle-contract.md:137` restates the block and uses *"auditable"*; `templates/core/dev/PLANNING.md:105` carries the adopter-facing twin. |
| **E1 / F1 (review question 1)** | **CONFIRMED DISCHARGED** | No change — the reviewer verified both independently and reached the plan's conclusion. The instruction to **re-verify at archive time rather than carry forward** stands, and is strengthened by the reviewer's observation that `bootstrap/PROVENANCE.md:41` becomes a present-tense false claim the moment an unsigned `v0.4.0` ships. | — |
| **Frozen-file deferral (review question 3, second part)** | **DEFERRAL KEPT; BASIS CORRECTED** | The subsection heading becomes *"…and ANSWERED"*, with the reviewer's answer recorded inline. The disposition is unchanged; the figures behind it are corrected per [I4]. | See [I4]. |
| **Chunk A placement deviation** | **STANDS, OPEN FOR THE MAINTAINER** | The reviewer explicitly declined to take a position (*"I neither ratify nor strike it"*), so the deviation is unchanged and its failure-mode row now records that a same-type reviewer confirmed the mechanism is inert but that the judgment is the Maintainer's. Re-verified the anchors it depends on. | `AGENTS.md` is **372** lines; slot opens `:248`, the *"discipline aid"* sentence runs `:260-266`, `cairn:end` at `:267`, `## Documentation discipline` at `:269`. Unchanged since plan-open. |
| **Row E2 — routed in from `planner-line-semantics`** | **ACCEPTED as a finding; MEASURED; ROUTED; nothing landed** | New subsection *What changed* > **6**, carrying the code citations, the perturbation table, and the disposition. Chunk A's rule gains the recursion sentence. This plan's own anti-placeholder note under *Plan review* is corrected. *Known omissions* gains item 7; *Lasting-truth migration* gains a two-home row. **The code fix is declined** (the accepted contract is *"Nothing that executes changes"*) and **the prose fix is declined as a partial** (the claim lives in `doctrine/lifecycle.md` **and** the fenced `doctrine/plans.md`; correcting one reproduces the exact "correcting one leaves the other overstating" failure Chunk D exists to avoid). | Re-derived from source and **perturbed the hazard**, loading `tools/lifecycle_planner.py` and calling `_conformance_violations` directly against fixture plans declaring `required(External)` at status `executing`. Cleared the gate: a full `##` review labelled `(Internal…)`; an **empty** `### Plan review -- R -- 2026-08-04`; a bare, undated `## Plan review` with **no body**; a review stating REVISE with **no `### Sharpening`**. Violated correctly: no section at all. The declared tier is read only as `art.plan_review.lower().startswith("required")` (`:785`, `:853`) — the `<tier>` token is parsed nowhere. |
| **The unrun-`security_check.py` recursion** (the review's closing carry-forward) | **ACCEPTED as an omission; ROUTED** | *Known omissions* gains item 8, stating plainly that after Chunks D and E three documents point at a script nothing runs. A *Lasting-truth* row homes it as a candidate proposal. It is also what the recursion sentence in Chunk A's rule generalises. | See [I2]. |
| **NEW at revision — Chunk C's anchor greps are self-matching** | **FOUND BY RE-RUNNING; CORRECTED** | Not a review finding. The criterion asserted `rc=1` for four greps; re-run at revision it returns **`rc=0` for all four**, every hit being this plan's own prose quoting the anchor strings. The criterion is corrected to the `dev/`-excluding form this plan's other sweeps already use, and the failure is described rather than quietly patched. | `grep -rn "<anchor>" --include="*.md" .` → **rc=0** ×4, every hit inside this plan file (the criterion's own paragraph, its code block, and the review section's A9 ratification). `git ls-files '*.md' \| grep -v '^dev/' \| xargs grep -n "<anchor>"` → **rc=1** ×4, so the substance (zero inbound anchors) survives. The only anchor-bearing inbound Markdown link outside `dev/` anywhere is `templates/core/dev/plans/_template.md:268`, unrelated to either rename. |
| **NEW at revision — the plan's two row-id namespaces collided** | **CORRECTED** | *Scope* gains a **row-id convention** paragraph and every chunk table is re-lettered to dotted ids (`A.1`, `B.1`–`B.3`, `C.1`–`C.5`, `D.1`, `D.2`, `E.1`, `E.2`). At plan-open, ledger `E1` (the discharged `PROVENANCE.md` row) and Chunk E's first table row were both `E1`; ledger `B1` (the `SAFETY.md` clause) collided with Chunk B's first table row. | — (structural). Two review findings, [I3] and [I5], had to disambiguate these by hand, which is what surfaced it. |

### Re-measurements that reproduced, recorded so nobody re-runs them

Both axis-1 sweeps: **17** Markdown files, **24** source files. The falsifying
signal: `find .github -type f` → **7** files, **no workflow**; the pipeline-file
grep over `git ls-files` → `docs/workflow-role.md` only, a prose document. Chunk
B's invocation grep → the same **8** paths. `bootstrap/SAFETY.md` = **276**
lines, clause still at `:120-121`. `AGENTS.md` = **372** lines, Chunk A's four
anchors unmoved. Frozen entries = **164**.

### What this Response does NOT do

* **It does not implement anything.** No source file was written. The plan is
  still `open`; every chunk is still `[commit pending]`.
* **It does not add a test**, and the reason is unchanged and now doubly
  supported: alternative 3 is rejected, and [I3] is a live demonstration that a
  green from a trigger nobody perturbed is worth nothing. The bar any future
  prose gate must clear is already on the record in *Acceptance criteria*.
* **It does not close *Known omissions* 1 or 2** — the behavioural and third
  axes are still unrun, and the Internal round did not close them either.
* **It does not answer the Chunk A placement question**, which the reviewer
  explicitly left to the Maintainer.
* **It does not re-open the Decision.** Rows A5, A6, A8 stay deferred; B2 stays
  fenced; B3 and E2 are recorded and routed, not landed.

### Post-revision checkers

```
$ ~/conda_envs/lhm/bin/python3.13 scripts/claim_check.py dev/plans/gate-claims-vs-enforcement.md
$ ~/conda_envs/lhm/bin/python3.13 scripts/check_cairn.py  dev/plans/gate-claims-vs-enforcement.md
```

Both run clean at revision; the results are recorded in the commit that lands
this section rather than asserted here, since this file is the subject.

This section is append-only once written.


## Code review -- Antigravity (External, security lens) -- 2026-08-04

**Steelman.** Implementation commits `8d23afe`, `1e47c08`, `2244eca`, `d1eb48c`, and `84fbef4` deliver `gate-claims-vs-enforcement.md` Chunks A–E. The plan establishes the fundamental governance rule: **a documented gate names what runs it — and when a trigger is named, the document states what that trigger actually verifies**. The rule paragraph is added to `AGENTS.md` (Chunk A). Chunks B–E systematically update container docs (`recipe.md`, `floor-gate.sh`), dependency budget docs (`DEPENDENCY_BUDGET.md`, `runtime-contract.md`), doctrine (`lifecycle.md`, `fidelity-check.md`), and safety docs (`SAFETY.md`) to explicitly state whether checks are maintainer-run, suite-run, or manual, eliminating misleading "in CI" claims across the codebase.

### Overstatement Audit Across All Chunks

Audited all five implementation chunks for the overstatement failure mode identified in Chunk E:

1. **Chunk A (`8d23afe`) Audit**: Added the governing rule to `AGENTS.md`. Correctly states "Cairn has no CI; do not write 'in CI' for something no CI runs." No overstatement.
2. **Chunk B (`1e47c08`) Audit**: Updated `recipe.md` and `floor-gate.sh`. Accurately distinguishes between manual maintainer execution of container scripts vs the test suite (`test_verify_ref.py`) extracting and replaying marked negative pins.
3. **Chunk C (`2244eca`) Audit**: Updated `DEPENDENCY_BUDGET.md` and `runtime-contract.md`. Accurately notes that `test_python_floor.py` runs in `pytest`, and explicitly discloses that the test **skips (passes green) if `vermin` is missing on `PATH`**.
4. **Chunk D (`d1eb48c`) Audit**: Updated `fidelity-check.md` and `lifecycle.md`. Accurately attributes `check_cairn.py` execution to review time and the **maintainer-run** release checklist (`security_check.py`, when a maintainer runs it).
5. **Chunk E (`84fbef4`) Audit**: Updated `SAFETY.md`. Corrected the initial draft overstatement by explicitly measuring and documenting that `check_cairn.py`'s `main()` filters sources via `link_check.filter_sources`, scanning **195 of 249 tracked Markdown files** (`as_of 2026-08-04`), skipping 54 files under `dev/` by default.

### Concerns

* **[E1] Un-automated release gate `security_check.py`.**
  As documented across Chunks D and E, `bootstrap/security_check.py` (which runs `check_cairn.py` and `bandit`) is not invoked by any git hook, test suite node, or CI pipeline. It remains a manual Maintainer release checklist item before minting tags.

### Covered

* **Full Pytest Suite Verification**:
  - Executed `pytest bootstrap/tests`: 1788 passed, 2 failed (the expected AST attestation pair shared with `profile-parse-fail-open`), 3 warnings in 133.06s.

* **Documentation & Claim Check Verification**:
  - `claim_check.py`: verified clean output across all 9 touched files.
  - `check_cairn.py`: 195 files scanned, 0 errors.

```
$ ~/conda_envs/lhm/bin/python scripts/claim_check.py dev/plans/gate-claims-vs-enforcement.md
claim_check: dev/plans/gate-claims-vs-enforcement.md -- OK, no claim-check flags.
```

### Not covered / low confidence

* Rows A5, A6, and A8 remain deferred behind the frozen-file gate manifest per the accepted plan design, and B2 remains fenced out and routed.

### Recommendation

**SHIP / PASS CODE REVIEW.** The implementation of `gate-claims-vs-enforcement.md` is complete, verified, and free of overstatements across all five chunks.

