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
`## Plan review` section is in the tree.**
**Last update**: 2026-08-04
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

### 4. One un-ledgered instance, in a file already inside `Touches` — proposed as row A9

Re-running the proposal's **axis 1** sweep (both commands, verbatim) for this
plan reproduces its figures — **17 Markdown files** and **24 source files**
match, `as_of 2026-08-04` — and surfaces one hit the ledger does not
disposition:

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

## Scope

Executes the accepted contract across **five chunks and eight files**, of which
two (`AGENTS.md`, `CHANGELOG.md`) are serialized shared files whose text this
plan **returns** rather than edits. Every touched file is Cairn-internal:
**nothing ships to an adopter, no manifest row moves, and no executable line
changes** — the one non-Markdown edit (Chunk B, row A7) is a `#` comment.

**Rows this plan lands:** A1, A2, A3, A4, A7, A9 (new), B1, C1, C2, and the
governing rule.
**Rows this plan records as closed:** E1, F1.
**Rows this plan defers:** A5, A6, A8.
**Rows this plan fences out:** B2.
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

### The frozen-file question — measured, and put to the reviewer rather than decided

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
* **The manifest is already stale by nine entries, none of them re-pinned.**
  Hashing the working tree against the committed map for this plan:

```
frozen entries: 164
mismatches: 9
   MODIFIED bootstrap/security_check.py
   MODIFIED bootstrap/tests/test_lifecycle_contract.py
   MODIFIED bootstrap/tests/test_lockfile_module.py
   MODIFIED bootstrap/tests/test_quality_gate_redundancy.py
   MODIFIED bootstrap/tests/test_security_check.py
   MODIFIED bootstrap/tests/test_security_lint.py
   MODIFIED bootstrap/tests/test_verify_integrity.py
   MODIFIED bootstrap/verify_integrity.py
   MODIFIED scripts/quality_gate.py
```

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
applying because nine other commits already drifted the map. This plan does not
grant itself an exception the ledger it is executing would have flagged.

**What would release them**, stated so the follow-up is pickable cold: the
manifest is retired, **or** a supervised re-pin lands and the Maintainer says the
three rows may ride it. Both are Maintainer-side; neither is this plan's to
decide. The nine stale pins are already an open Maintainer question raised by
`scan-coverage` (*"whether re-pinning the three stale frozen entries should
happen now or at the next supervised re-anchor"*), and this plan adds three
prospective rows to it rather than opening a second question.

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
| A-1 | `AGENTS.md` > *Verifying claims* | Insert the rule paragraph **after** the `<!-- cairn:end claim-check -->` marker at `AGENTS.md:267` and before the `## Documentation discipline` heading at `AGENTS.md:269`. Text below, verbatim. |

**The exact text to insert** (the proposal's rule, unchanged):

> **Name the trigger, and check what it checks.** Any document that
> describes a check says what runs it — a command a person runs, a test in
> `bootstrap/tests`, a git hook, or a CI job. Cairn has no CI; do not write
> "in CI" for something no CI runs. A check whose only trigger is a human
> remembering is described that way. And when a named trigger exists, the
> document states what that trigger actually verifies: a tool that returns
> success without testing the claimed property is a worse defect than no
> tool, because it is silent.

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

**The open question this chunk hands to the reviewer.** The proposal's appended
section offers a third clause it *"would take at review"*:

> **and open it.** A named trigger is checked by opening it and confirming the
> procedure is there. A path that resolves is not a trigger that governs.

Its status is genuinely ambiguous. It is stated inside the appended section the
Decision accepts, but framed conditionally, and the Internal reviewer never
addressed it. **The plan's recommendation is to include it**, because the row
that motivated it (F1) is the one the two-clause rule provably fails to catch —
`claim_check.py` passed the mispointing `AGENTS.md` clean, precisely because the
path resolved. **It is not in the text above**, so that including it is a
one-line ratification by the reviewer rather than a silent authorial expansion.

**Acceptance criteria — Chunk A.**

* The text lands verbatim, outside the slot, in a serialization commit the
  orchestrator or the Maintainer makes.
* `~/conda_envs/lhm/bin/python3.13 scripts/claim_check.py AGENTS.md` → clean.
* `~/conda_envs/lhm/bin/python3.13 scripts/check_cairn.py` → green.
* `~/conda_envs/lhm/bin/python3.13 scripts/quality_gate.py --sub neutrality` →
  green. The rule names no vendor.
* **`templates/core/AGENTS.md` is unchanged**, verified with `git status --short`
  — checked because the rule is Cairn-specific and false for an adopter.

---

### Chunk B — the container surface, indivisible

Rows A2, A3 and A7. The document and the script it describes move in one commit.

| # | File | Change |
|---|------|--------|
| B1 | `bootstrap/container/recipe.md:152-153` | Replace *"The **floor gate** … and the **acceptance test** … run in **Cairn's CI**, not in an adopter's CI."* with a sentence naming the real trigger **and** the suite's partial coupling to `acceptance.sh`. Draft below. The following sentence (*"records **SKIPPED** (never PASS)…"*, lines 153-154) is Class D and is left byte-identical. |
| B2 | `bootstrap/container/recipe.md:147` | Platform matrix, *Rootless Linux + Podman/Docker* row: change *"(the F4 acceptance gate runs here)"* to *"(the F4 acceptance gate is run here by hand)"*. |
| B3 | `bootstrap/container/floor-gate.sh:5` | Replace the header comment *"# Runs in CAIRN's CI (not adopter CI)."* with *"# Run by the maintainer from a Cairn checkout (not adopter CI)."* Comment-only; no executable line moves. |

**Draft replacement for B1**, written against the measurement in *What changed*
> 5 rather than against the proposal's stale supporting claim:

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

  Expected today (`as_of 2026-08-04`): `CHANGELOG.md`,
  `bootstrap/container/Dockerfile`, `bootstrap/container/acceptance.sh`,
  `bootstrap/container/floor-gate.sh`, `bootstrap/container/recipe.md`,
  `bootstrap/container/verify-ref.sh`, `bootstrap/tests/test_verify_ref.py`,
  `doctrine/runtime-contract.md`. **If a new invoker has appeared, the sentence
  changes before it is written.** If `test_verify_ref.py` has *stopped*
  appearing, the parenthetical is deleted rather than left to assert.
* `git diff --stat bootstrap/container/floor-gate.sh` shows exactly one changed
  line, and `git diff bootstrap/container/floor-gate.sh` shows it beginning with
  `#`.
* `bash -n bootstrap/container/floor-gate.sh` → exit 0 (syntax intact after a
  comment edit).
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
| C1 | `bootstrap/DEPENDENCY_BUDGET.md:101` | *"It runs only in Cairn's own CI (`bootstrap/tests/test_python_floor.py`)"* → *"It runs only in Cairn's own test suite (`bootstrap/tests/test_python_floor.py`, run by `python -m pytest bootstrap/tests`)"*. Doubly wrong as written: there is no CI, **and** the test runs locally. |
| C2 | `bootstrap/DEPENDENCY_BUDGET.md:97` | **Row A9, proposed.** Heading *"## Exception 2 — `vermin`: floor CI check (dev/test-only)"* → *"## Exception 2 — `vermin`: floor check (dev/test-only)"*. |
| C3 | `doctrine/runtime-contract.md:189` | Heading *"## Floor CI check"* → *"## Floor check"*. |
| C4 | `doctrine/runtime-contract.md:46` | *"the surface measured for the floor CI check"* → *"…for the floor check"*. |
| C5 | `doctrine/runtime-contract.md:185` | *"(`vermin` for the floor CI check)"* → *"(`vermin` for the floor check)"*. |

The section bodies are already accurate — `doctrine/runtime-contract.md:191-195`
correctly says the check is a test that skips gracefully — so **only the names
lie**, and only the names move.

**Acceptance criteria — Chunk C.**

* **The anchor check, and the perturbation that would make it fail.** Renaming a
  heading changes its GitHub anchor (`#floor-ci-check` → `#floor-check`;
  `#exception-2--vermin-floor-ci-check-devtest-only` →
  `#exception-2--vermin-floor-check-devtest-only`), and
  `scripts/check_cairn.py` resolves internal anchors. Verified for this plan,
  `as_of 2026-08-04`: **zero** inbound references —

```
$ grep -rn "floor-ci-check" --include="*.md" . ; echo "rc=$?"
rc=1
$ grep -rn "exception-2" --include="*.md" . ; echo "rc=$?"
rc=1
$ grep -rn "runtime-contract.md#" --include="*.md" . ; echo "rc=$?"
rc=1
$ grep -rn "DEPENDENCY_BUDGET.md#" --include="*.md" . ; echo "rc=$?"
rc=1
```

  **State the consequence plainly rather than claiming a guard: because there
  are no inbound anchors, `check_cairn.py` staying green over this rename is
  *vacuous* — it would stay green whether or not the rename were correct.** The
  check is worth running (concurrent work could add an inbound link before this
  chunk lands) and is worth **nothing** as evidence that the rename is right. A
  claims-audit plan does not get to present a vacuous green as a guard.
* The four greps above are **re-run at implementation**, not trusted from here.
* `~/conda_envs/lhm/bin/python3.13 scripts/claim_check.py
  bootstrap/DEPENDENCY_BUDGET.md` and the same over
  `doctrine/runtime-contract.md` → clean, one file per invocation.
* `~/conda_envs/lhm/bin/python3.13 scripts/check_cairn.py` → green.
* **C1's replacement names a trigger that must be true.** Re-run
  `~/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests/test_python_floor.py -q`
  and record the result in the commit body. The 2026-07-22 correction the
  proposal carries forward (the test *runs*, it does not skip, because `vermin`
  resolves on PATH in the canonical environment) is what makes the new sentence
  true; if it now skips, the sentence changes.

---

### Chunk D — Class C, the two trigger clauses

Rows C1 and C2. **They move together**: the same gate, the same phrasing, in two
files. Correcting one leaves the other overstating.

| # | File | Change |
|---|------|--------|
| D1 | `doctrine/lifecycle.md:218-221` | After *"…a reference that resolves in the Cairn source but **dangles once installed**."*, append the trigger clause. |
| D2 | `bootstrap/fidelity-check.md:42-48` | The same one-clause addition to the parallel sentence. |

**The clause**, in both places (the proposal's wording, with the release-gate
caller named because the new rule's second half requires stating what the trigger
verifies):

> — when run: `python scripts/check_cairn.py`, at review time and in the release
> gate (`bootstrap/security_check.py` runs it).

**Both halves verified against the code for this plan**, since this is an
enforcement claim in a plan about enforcement claims:

* `bootstrap/security_check.py:214` defines `run_check_cairn()`, which executes
  `CAIRN_ROOT / "scripts" / "check_cairn.py"`; `bootstrap/security_check.py:226`
  returns `run_bandit() | run_check_cairn()`. The release gate does run it.
* `scripts/check_cairn.py` scans `git ls-files '*.md'` via `tracked_markdown()`
  at `scripts/check_cairn.py:180`, and its own header (`scripts/check_cairn.py:50`)
  states the scanned set is *"the whole tracked Markdown tree."*

**Acceptance criteria — Chunk D.**

* Both files edited in one commit; `git diff --stat` shows exactly two files.
* `~/conda_envs/lhm/bin/python3.13 scripts/claim_check.py doctrine/lifecycle.md`
  and the same over `bootstrap/fidelity-check.md` → clean.
* `~/conda_envs/lhm/bin/python3.13 scripts/check_cairn.py` → green. This chunk is
  the one place where that command is a **real** check rather than a vacuous one:
  `bootstrap/fidelity-check.md:42-52` is the document describing the very lens
  `check_cairn.py` implements, and it carries a live
  `cairn-internal-ref` marker at line 52 whose text the edit sits next to.
* The claim *"fails closed"* is **kept, not weakened** — that is the whole point
  of Class C, and the proposal's alternative 4 rejects deleting a true claim to
  avoid an untrue implication.

---

### Chunk E — `bootstrap/SAFETY.md`, and the changelog

Row B1, plus the serialized release note. Last, and reviewed with a security
lens.

| # | File | Change |
|---|------|--------|
| E1 | `bootstrap/SAFETY.md:120-121` | Replace the *"must pass the content-integrity scanner"* clause with the replacement below. The surrounding sentence and the by-file-class list are untouched. |
| E2 | `CHANGELOG.md > Unreleased > Fixed` | One line. **Serialized: text returned, not edited in-agent.** |

**The replacement clause** (carried verbatim from the proposal, rebased onto the
text `scan-coverage` left):

> — and is scanned with the content-integrity scanner (`content_scan.py`).
> Two triggers exist and neither fires on a commit: the suite scans
> generated output and the skills artifacts on every `pytest` run, and
> `check_cairn.py` scans every tracked Markdown file when a person runs it
> (the release gate `security_check.py` runs it). Source prose that no
> scaffolded profile emits — `doctrine/`, `docs/`, `case-studies/`, this
> document — is reached **only** by that manual run. Running it is the
> reviewer's obligation, not a mechanism's guarantee.

**Every factual claim in that replacement, verified against the code for this
plan** — not against the proposal:

| Claim | Verified against |
|---|---|
| the suite scans **generated output** on every `pytest` run | `bootstrap/tests/test_generated_output_scan.py` imports `content_scan` and calls `content_scan.scan_file` over a scaffolded tree (lines 32, 53, 121) |
| the suite scans the **skills artifacts** | `bootstrap/tests/test_skills_security.py` loads `templates/modules/team-gated/content_scan.py` and scans the canonical skills artifacts (lines 9, 42) |
| `check_cairn.py` scans **every tracked Markdown file** | `tracked_markdown()` at `scripts/check_cairn.py:180` runs `git ls-files '*.md'`; the header at line 50 says so |
| **the release gate runs it** | `run_check_cairn()` at `bootstrap/security_check.py:214`; composed at line 226 |
| **neither trigger fires on a commit** | the two installed git hooks are `pre-commit` → `tools/intent.py _precommit_check` (work-intent claim collisions only) and `post-commit` → `tools/intent.py _auto_release`, terminated `\|\| true` |

**One precision residual, recorded rather than smoothed over.**
`scripts/check_cairn.py` accepts `--no-content-scan` (line 560), so *"scans every
tracked Markdown file when a person runs it"* is true of the default invocation
and not of every invocation. The clause is left as the proposal wrote it — adding
"unless they pass `--no-content-scan`" buys precision no reader needs and costs
the sentence its point — but the residual is named here so the reviewer decides
rather than discovers.

**The proposed `CHANGELOG.md` line** (returned for serialization; `Unreleased` >
`Fixed`):

> - **Enforcement claims name their trigger.** Corrected nine documented checks
>   that described themselves in the vocabulary of an automatic gate — eight
>   naming a CI this repository does not have — across `bootstrap/SAFETY.md`,
>   `bootstrap/DEPENDENCY_BUDGET.md`, `bootstrap/container/recipe.md`,
>   `bootstrap/container/floor-gate.sh`, `bootstrap/fidelity-check.md`,
>   `doctrine/runtime-contract.md` and `doctrine/lifecycle.md`. Nothing that
>   executes changed. `AGENTS.md` gains the governing rule: a document that
>   describes a check names what runs it, and states what that trigger actually
>   verifies.

**Acceptance criteria — Chunk E.**

* **`bootstrap/SAFETY.md:115-125` is re-read immediately before editing.** This
  file moved twice today (`5c91c23`, and this plan). If the quoted clause is not
  where this plan says it is, the plan is stale and the reviewer is told, not
  worked around.
* `git diff bootstrap/SAFETY.md` touches **only** the clause. Specifically: the
  by-file-class list (lines 122-198) and the residuals block `scan-coverage`
  added at lines 170-196 are byte-identical. Verify with `git diff -U0` and read
  every hunk.
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
    not by a mechanism** — this is the row the Internal reviewer should challenge.
    B1's replacement deliberately keeps the word "obligation" and names who holds
    it; C1/C2 keep *"fails closed"*.
  * *A serialized shared file is never edited by the implementing agent.*
    Enforced by the chunk tables (Chunks A and E mark their rows SERIALIZED) and
    by review of the commit's path list. No mechanism detects it.
* **Public-path → test mapping.** **N/A** — no public code path is added or
  changed. The only non-Markdown edit is a `#` comment in
  `bootstrap/container/floor-gate.sh`, a script no test invokes.
* **Failure modes.**
  * *Open (degrades):* the re-worded B1 reads as permission to skip the scan.
    Mitigated by naming the reviewer's obligation explicitly and by the
    security-lens read on Chunk E. Recovery: restore the imperative and add the
    trigger as a separate sentence, keeping "must" intact.
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
  * *New, introduced by this plan:* row A9 is an authorial addition beyond the
    accepted ledger. Mitigated by isolating it in one chunk row (C2) that the
    reviewer can strike in one line, and by refusing to add it to the rate-limit
    gate's cleared count.
  * *New, introduced by this plan:* the Chunk A placement deviation. Mitigated by
    stating the mechanism it guards against, verifying that mechanism is inert
    today, and inviting the literal placement instead.
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
     pass. This plan runs no systematic pass on it.
  3. **No human has re-read the corrected sentences for downstream readers other
     than the reviewer.** There is no mechanism that would.
  4. **The nine stale frozen pins** are recorded, not resolved. They are a
     Maintainer question `scan-coverage` already raised.
  5. **Whether the rule's third clause belongs in `AGENTS.md`** is left to the
     plan review rather than settled here.

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

**One correction to that slot, which this plan is obliged to make.** The slot
text reads *"the same ones CI enforces."* **Cairn has no CI.** The slot is
Cairn's own copy of a template block written for adopters, who do. It is left
unedited here — it is a `cairn:slot` body in the plan **template**, not a claim
about a check, and correcting it means editing `dev/plans/_template.md`, which is
outside this plan's `Touches`. **Recorded as a found instance and routed** — see
*Lasting-truth migration*. Noting it and not fixing it is the correct move; not
noticing it would have been the ledger failing on itself.

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
> `## Plan review` heading, an empty section satisfies the gate. This heading is
> shaped so a placeholder cannot satisfy it.

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
| **Row B2** — the archive-commit-body auditability claim in `doctrine/proposals.md:370` and `doctrine/plans.md:611` | A **queued follow-up proposal** under `dev/proposals/`, unless the plan review ratifies it into a Chunk F | It is a doctrine edit into two files no accepted *Touches* line names. The proposal's own appended text warns that the sibling restatements in `doctrine/lifecycle-contract.md`, `dev/PLANNING.md` and `templates/core/dev/PLANNING.md` engage the loop-fidelity lens, so the scope needs its own artifact. **Naming a prospective proposal is not a home** — B2's own evidence establishes that — so the fallback home is a `dev/PLANNING.md` board row carrying the measurement (plans 7 of 9 / proposals 1 of 12 in-file; 0 of 9 and 0 of 12 in commit bodies, `as_of 2026-08-03`) until such a proposal exists. |
| **The `dev/plans/_template.md` verification-slot instance** — *"the same ones CI enforces"* in the `verification-commands` slot, found by this plan and out of its `Touches` | `dev/PLANNING.md` board row | It is a one-line Class A correction in a template Cairn ships itself, and it needs the adopter-vs-Cairn boundary drawn: the sentence is *correct* for an adopter with CI and *false* for Cairn's own copy. That is a real design question, not a typo, and it should not ride this plan. |
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
