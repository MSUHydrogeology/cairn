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
