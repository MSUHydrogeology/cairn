<!-- cairn-internal-ref-allow: doctrine/rationale.md doctrine/proposals.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see AGENTS.md, "Where doctrine/ references resolve") -->
<!-- Forward-reference paths this proposal plans to create; they materialize in the implementing plan. They are also named in the Proposed paths block, whose marker only exempts that block -- these citations recur in the header, the Proposal, and the Evidence sections. -->
<!-- claim-check-allow: bootstrap/tests/_gate_preflight.py, bootstrap/tests/test_gate_preflight.py, dev/plans/gate-reanchor-preflight.md -->
<!-- link-marker maintenance 2026-08-03: the Author-accounting section writes its
     public-path -> test mapping as a relative markdown link, per the proposal
     template's instruction that the link checker verify the cited test exists.
     For a forward-referenced test that is not yet on disk the instruction cannot
     be satisfied, so the target is exempted below rather than the (append-only)
     section being edited. The sibling transition-lint / stage-commit-patterns
     proposals avoid this by writing the same mapping as a plain backticked path;
     that is the better convention and the implementing plan should adopt it.
     Drop this directive once the test lands. -->
<!-- link-check-allow: ../../bootstrap/tests/test_gate_preflight.py -->

# A reviewed pre-flight for the supervised gate re-anchor (Phase 0)

**Author**: Claude (Strategy)
**Model**: Claude Opus 5
**Date opened**: 2026-08-03
**Status**: revised
**Touches**: a new Cairn-internal checker `bootstrap/tests/_gate_preflight.py` and its behavioural test `bootstrap/tests/test_gate_preflight.py`; a new pre-flight step in `bootstrap/REANCHOR_RUNBOOK.md`'s Phase 0. **No shipped template, no install-manifest entry, no adopter-facing surface** (`scaffold.py --manifest` has zero entries under `bootstrap/tests/`, verified 2026-08-03); no doctrine file under `doctrine/`; no change to `_gate_reanchor.py`'s Stage A / Stage B contract.
**Related**: `bootstrap/REANCHOR_RUNBOOK.md` Phase 0; the two supervised runs that motivated this — the 2026-07-31 trust-root re-establishment (`e5ecaa5`) and the pending re-bless for `cfc5530`; the archived plan `dev/plans/archive/interpreter-trust-root-fallback.md`, whose Lasting-truth section records the four review rounds spent mis-specifying this same ceremony. Opened under the Maintainer's 2026-08-03 direction, *"I feel like this script should be more formalized as an actual mechanism for re-use"* and *"I think it needs to be externally reviewed with a security lens"*.
**Plan review**: required(**External**, security lens) — the Maintainer's direction above, applied to this proposal *and* carried to the plan. The surface is the input to a trust-root blessing decision; a same-type read cannot supply the independence the circularity in *Proposal > The circularity this does not eliminate* needs.

## Proposed paths

Proposed paths:
- `bootstrap/tests/_gate_preflight.py` — the checker; lands with the implementing plan.
- `bootstrap/tests/test_gate_preflight.py` — its behavioural test; lands with the same commit.
- `dev/plans/gate-reanchor-preflight.md` — the implementing plan; opens after the Decision.

## Context

`bootstrap/REANCHOR_RUNBOOK.md` Phase 0 (lines 28-87) is the supervised
trust-root re-establishment: review the Stage-B authority modules out of band,
regenerate `bootstrap/tests/fixtures/gate_manifest.json` over the reviewed
tree, commit it as the new prior gate state `P`, and advance
`refs/cairn/gate-anchor` to it. The runbook is explicit that this is the
Maintainer's act and that an implementing agent must not perform it.

The runbook specifies *what* to verify. It ships **no tool that verifies it**.
In practice the gap has been filled twice by an ad-hoc script written into an
agent scratchpad during the session that needed it, and thrown away after:

* **2026-07-31** — the first real Phase 0 run in this repository (`e5ecaa5`).
  The scratchpad checker computed the interpreter check, the authority-module
  identity check, the produced-vs-recorded hash equality check, and the live
  scope derivation. It was written, syntax-checked, and handed over in a single
  session, reviewed by nobody.
* **2026-08-03** — the same script, re-used for the re-bless that `cfc5530`
  now requires. **It returned a wrong answer**: its "working tree clean" test
  used `git status --porcelain`, which counts untracked files anywhere in the
  tree, and it refused to proceed because of `.claude/` and
  `dev/measurement/snapshots/` — two paths that cannot reach the manifest,
  because `_gate_manifest._frozen_files` (`bootstrap/tests/_gate_manifest.py:151`)
  globs only `bootstrap/*.py`, `bootstrap/tests/**`, `scripts/*.py` and
  `templates/modules/**`. The Maintainer was told to commit files that did not
  need committing, in the middle of a trust ceremony.

Two further pieces of ceremony knowledge exist only in chat transcripts, which
compaction discards:

* The **commit message must exist before** the step that opens an editor. On
  2026-07-31 it did not, the Maintainer committed `Blessing this current
  state`, and the runbook-mandated audit trail (authority hashes, both anchor
  SHAs, derived scope) was recovered only because the commit was still
  unpushed and could be amended.
* **A rebase after a blessing silently orphans the anchor.**
  `refs/cairn/gate-anchor` is a plain ref; replaying the local commits leaves
  it pointing at an object that is no longer an ancestor of the branch. Nothing
  fails loudly — `verify --anchor-ref` still reads the manifest blob out of the
  old object and still passes.

The felt pain is not "this is tedious." It is that a **trust decision is being
made on the output of unreviewed, disposable code**, and that code has already
been wrong once.

## Proposal

Ship a reviewed, tested, Cairn-internal pre-flight checker.

**`bootstrap/tests/_gate_preflight.py`**, a sibling of `_gate_manifest.py` and
`_gate_reanchor.py`, exposing one subcommand:

```
python bootstrap/tests/_gate_preflight.py check [--repo PATH]
```

**Read-only against the repository, by construction.** It writes no file into
the tree, creates no commit, and moves no ref. Its only write is a candidate
manifest into a caller-invisible temp directory, whose path it reports so the
Maintainer installs *the exact bytes that were checked* rather than
regenerating them.

### The checks

Each refuses (non-zero exit) rather than warning, except where noted:

1. **Canonical interpreter** — refuse unless running Python 3.13.x. The
   manifest pins `interpreter.version` and the collection set is
   minor-sensitive; producing it off-canon poisons the pin silently.
2. **No uncommitted tracked changes** — the blessed commit must contain the
   bytes that were verified.
3. **No untracked files inside the frozen gate surface** — scoped to
   `_frozen_files()`, *not* the whole tree. An untracked file inside the
   surface would be hashed into the manifest but absent from the commit, so a
   fresh checkout at the anchor would fail. Untracked files outside the surface
   are reported as a note and are not a refusal. **This check is the 2026-08-03
   defect, stated as a contract.**
4. **Stage-B authority-module identity** — diff the six modules
   `_gate_reanchor._authority_code_files()` enumerates against the current
   anchor. Unchanged is reported as such (the blessing then pins no
   newly-trusted verifier code). **Changed is not a refusal** — it is a
   *stop-and-escalate*: those bytes need genuine out-of-band review, which is
   Phase 0 step 1 and is not something a checker can do.
5. **Record the six sha256** — the audit trail Phase 0 step 1 requires.
6. **Equality check** — the produced manifest's pins for those six equal the
   independently-computed hashes. This is what makes the pin *reviewed* rather
   than self-generated.
7. **Interpreter pin** — the produced manifest records 3.13.x.
8. **Live scope derivation** — files changed anchor→HEAD, frozen files
   modified / added / **removed**, and the collection delta, all re-derived at
   run time. **Any removed frozen file, or any reduced collection, refuses**: a
   gate that disappeared is the tampering signature the manifest exists to
   catch. Growth is reported, not refused.
9. **Anchor ancestry** — refuse if the current anchor is not an ancestor of
   `HEAD`, which means a prior blessing was already orphaned; and emit the
   rebase-ordering warning unconditionally, since the hazard is about what the
   Maintainer does *next* and cannot be detected in advance.

### Two outputs the Maintainer uses directly

* **A drafted commit message** written to a temp file, carrying the six
  authority hashes, the superseded and prospective anchor SHAs, and the
  live-derived scope — so the audit trail exists *before* the editor opens.
* **The exact next commands**, referencing the temp paths, in order.

### What it deliberately does not do

It does not commit, does not move the ref, does not amend, and has no
allowlist, exemption, or suppression mechanism. There is no flag that turns a
refusal into a pass.

### Documentation / doctrine surface

`bootstrap/REANCHOR_RUNBOOK.md` Phase 0 gains a pre-flight step ahead of its
current step 1, plus the two ceremony-sequencing rules recovered above (draft
the commit message first; rebase before blessing, never after). Per the doc
tier home rule this is the **descriptive/operational** layer — a runbook for a
mechanism that already exists — not `doctrine/`, and not `AGENTS.md`: no rule
every contributor follows is changing. `CHANGELOG.md` gets an `Unreleased`
entry at implementation. No other doc surface.

### Doctrine-change rate-limit

This proposal does **not** change doctrine — it adds a tool and a runbook step,
touching no file under `doctrine/`, no dimension matrix, and no framework
anchor. The gate does not apply. Recorded anyway, because the runbook edit is
process-adjacent and a reviewer should be able to check the reasoning rather
than take it on trust: both limbs would in fact be satisfied — **recurrence**
(two ad-hoc runs in a four-day window, the second returning a wrong answer) and
the **Maintainer's high-risk classification** (the 2026-08-03 direction that
this be reviewed with a security lens).

### The circularity this does not eliminate

Stated plainly, because it is the thing the security review exists to weigh.

An implementing agent would author the checker whose output tells the
Maintainer whether to trust that same agent's work. That is the shape
`REANCHOR_RUNBOOK.md` forbids when it bars an implementing agent from running
Phase 0. Formalizing the checker does not dissolve it; four properties **bound**
it:

* **It computes, it never decides.** Every repo-mutating step stays the
  Maintainer's, exactly as today.
* **It is itself pinned.** Living under `bootstrap/tests/`, it falls inside
  `_frozen_files()` automatically, so it becomes part of the surface the gate
  manifest protects — a later silent edit to the checker is itself a
  FROZEN-MODIFIED finding.
* **It prints raw values, not verdicts alone** — the hashes, the counts, both
  SHAs — so every claim it makes is independently spot-checkable.
* **The runbook keeps the manual path.** Phase 0's existing hand-run commands
  stay documented and usable, so the checker is a convenience over an
  independently-executable procedure, never the only route.

What none of that fixes: a checker that is *wrong in the passing direction*
would be believed. The 2026-08-03 defect failed closed (refused when it should
have passed), which is the safe direction; the review should ask what forces
the failure direction to stay that way, and whether property two is real
protection or merely detects tampering *after* a blessing has already been
granted on bad output.

## Rationale

* **Which workflow does it improve?** The supervised re-anchor, which the
  Maintainer runs personally and is about to run a third time (`cfc5530`) and
  a fourth (`stage-commit-patterns` modifies two frozen files). Today each run
  begins by an agent re-authoring a checker from scratch.
* **What contract does it clarify?** Phase 0's *verification* contract, which
  the runbook states in prose and nothing enforces. Turning it into a tested
  module makes the checks reviewable once instead of re-derived per session,
  and makes the untracked-file scoping rule explicit rather than a trap.
* **Correctness / reproducibility.** The blessed scope figures become
  reproducible output of a pinned tool rather than a number an agent typed into
  chat — which the archived `interpreter-trust-root-fallback` plan already
  identified as a live-invariant failure mode after it went stale twice mid-review.
* **Why now?** There is a pending re-bless blocked behind exactly this
  ceremony, and the ad-hoc script has just demonstrated the failure mode. Also
  the honest reason to wait is weak: the alternative is a third disposable script.

## Alternatives considered

1. **Do nothing — keep writing a scratchpad script per session.** The status
   quo. Rejected: no cumulative correctness, no review, and the knowledge
   evaporates at compaction. It has produced one wrong answer in two uses.
2. **A manual checklist in the runbook, no code.** The serious alternative, and
   the only one that fully avoids the circularity above — nothing new to trust.
   Rejected on execution risk rather than principle: the procedure is nine
   checks including six hash comparisons and a live scope derivation, run by a
   Maintainer who has said they are not a software engineer, in a ceremony where
   a mistake is a false trust root. A checklist optimizes the property that is
   not actually at risk (nobody has tampered with the checker) at the cost of
   the one that is (a human hand-comparing sha256 strings at the end of a long
   session). **The reviewer should push on this trade rather than accept it.**
3. **Fold the pre-flight into `_gate_reanchor.py prepare`.** Rejected:
   `prepare` is Phase 4 machinery, keyed to an authorization anchor that Phase 0
   does not have. Conflating the two is precisely the confusion that cost the
   `interpreter-trust-root-fallback` plan four External review rounds; that plan's
   Lasting-truth section records it.
4. **Ship it to adopters as a supported tool.** Rejected for now: adopters do
   not run this ceremony, `bootstrap/tests/` is not installed, and widening the
   surface adds an install-contract obligation for no current user. Revisit only
   if an adopter adopts the differential-oracle gate.
5. **Have the checker perform the blessing when all checks pass.** Rejected
   outright, and named only to record the refusal: it would make the checker
   authoritative and collapse the separation of duties the runbook exists to
   enforce.

## Evidence / verification plan

### Author-accounting — invariants, failure modes, edge cases

* **Invariants.** (a) The checker never mutates the repository — enforced by a
  test that snapshots `git status --porcelain`, the `HEAD` sha, and every
  `refs/cairn/*` value before and after a full run and asserts equality. (b) The
  produced-manifest bytes the checker reports are the bytes the Maintainer
  installs — enforced by reporting a temp path rather than a regeneration
  command. (c) Any refusal exits non-zero — enforced per refusal path below.
* **Failure modes.** All refusals are **closed** (non-zero exit, no output the
  Maintainer can act on). The one deliberately **open** path is the
  authority-module *changed* case (finding 4), which reports and escalates
  rather than refusing, because the correct response is human out-of-band review
  the tool cannot perform; the review should confirm that open path is right.
  A checker crash is closed by default (non-zero from an unhandled exception) —
  deliberately *not* wrapped in a fail-soft handler, unlike the post-commit hook.
* **Edge cases.** Empty log / absent manifest / anchor equal to HEAD (no-op
  blessing) / anchor orphaned by a prior rebase / zero frozen changes / a frozen
  file removed / collection shrunk / off-canon interpreter. Out of scope:
  concurrent Maintainers (single-machine assumption, stated), and a repository
  with no `refs/cairn/gate-anchor` at all — which is Phase 0's *first-ever* run
  and has no prior anchor to diff against; the checker refuses with a pointer to
  the runbook rather than guessing.
* **Public-path → test mapping.** One public entry point, `check`, mapped to
  [`bootstrap/tests/test_gate_preflight.py`](../../bootstrap/tests/test_gate_preflight.py)
  exercising it through the CLI, not by importing internals.
* **Known omissions.** The checker does not verify that the six authority
  modules are *correct*, only that they are *unchanged since the anchor*; a
  compromised module that was already anchored passes. That is Phase 0 step 1's
  job and stays human. It also cannot detect a rebase that has not happened yet.

### Tests required

`bootstrap/tests/test_gate_preflight.py`, driving the CLI in sandboxed temp
repos (the `_two_stage_repo` pattern in `bootstrap/tests/test_gate_reanchor.py`
is the model): one test per refusal path (off-canon interpreter, tracked
changes, untracked-inside-surface, frozen-file removed, reduced collection,
orphaned anchor, missing anchor ref), one asserting untracked files **outside**
the surface do **not** refuse (the 2026-08-03 regression, pinned), one asserting
the drafted commit message contains all six hashes and both SHAs, and the
no-mutation invariant test above. Every refusal test must be shown non-vacuous
by mutation — the check removed, the test fails.

### Examples / smoke checks

`python bootstrap/tests/_gate_preflight.py check` against Cairn's own tree at
the pending `cfc5530` re-bless, whose expected verdict is known independently:
one FROZEN-MODIFIED file, zero removed, collection 1469→1471. `python
scripts/check_cairn.py` for the runbook prose edit. **N/A**: the example gallery
— this touches no shipped example.

## Signals the change is wrong

* **A refusal the Maintainer learns to route around.** If any check produces
  false blockers in practice, the ceremony's value inverts — a tool that cries
  wolf trains the operator to bypass it. Recovery: the check is removed or
  re-scoped by proposal, never by adding a suppression flag.
* **The checker's output being treated as the blessing.** If a future session
  records "pre-flight passed" as the audit trail instead of the hashes and SHAs,
  the tool has replaced the record rather than fed it. Recovery: the runbook's
  manual path is the fallback, and the drafted commit message stays the artifact.
* **Drift between the checker and `_gate_manifest.py`.** If `_frozen_files()`
  changes and the checker's surface scoping does not follow, check 3 silently
  stops matching reality. Recovery: the checker must import `_frozen_files`
  rather than re-implement the globs — an implementation constraint, flagged
  here so the reviewer can hold the plan to it.
* **A second adopter needing this.** Would falsify alternative 4's scoping and
  require re-opening the ship-to-adopters question.

## Amendment -- Claude (author) -- 2026-08-03

**Model**: Claude Opus 5

Appended, not merged into the sections above, per the append-only rule. This
records an incident that occurred **after this proposal was committed
(`deceb51`) and before any review**, and it corrects the proposal's own threat
model. The reviewer should read the correction in *2* as the substantive change;
the rest is evidence and consequent requirements.

### 1. The hazard stopped being hypothetical

While the Maintainer was running the very ceremony this proposal describes, the
scratchpad checker's three emitted steps were pasted into a shell as three
independent lines:

```
cp <tmp>/gate_manifest.json bootstrap/tests/fixtures/gate_manifest.json
git commit bootstrap/tests/fixtures/gate_manifest.json      # (author the message yourself)
git update-ref refs/cairn/gate-anchor $(git rev-parse HEAD)
```

The `cp` succeeded. The `git commit` opened an editor and was **aborted** (empty
message, so git declined the commit). The `git update-ref` then **ran anyway**,
because nothing sequenced it behind the commit's success — advancing
`refs/cairn/gate-anchor` to `deceb51`, an ordinary proposal commit containing no
blessing and no regenerated manifest.

The trust root spent that interval pointing at a commit that had never been
blessed. Repaired in `bf08f62`, whose message carries the incident record because
custom refs keep no reflog and there was therefore no other ledger.

Two things worked and should be credited: `_gate_manifest.py verify` reported
`HOLD` continuously and correctly throughout ("working-tree manifest differs from
the immutable `deceb51` object"), so the bad state was **loud, not silent**; and
the installed manifest was independently confirmed byte-identical to a re-produced
candidate before the repair committed it.

### 2. The correction — this proposal had the threat model wrong

The body above frames the risk as *a check that wrongly passes*, and treats the
drafted commit message and emitted commands as a convenience ("Two outputs the
Maintainer uses directly"). That framing is now falsified by events.

In this incident **every check behaved correctly**. The interpreter check, the
authority-module identity check, the hash-equality check, the scope derivation —
all right. The damage came entirely from **how the verified result was handed
over**: unsequenced steps, plus an instruction to hand-author a commit message
whose mandated content the tool had already computed and the human could not
reasonably retype. The Maintainer identified that second half independently,
before the ref state was discovered, observing that the audit trail *"should have
some very specific information, so I don't think this instruction about authoring
the message myself is correct."*

So the handoff is not a convenience surface. **It is a safety-critical surface,
and on the evidence it is the more dangerous one** — a wrong check has to survive
review, while a badly-sequenced handoff bypasses review entirely by mutating a
trust ref through a shell the checker never sees. The security review should
weight it accordingly rather than treating it as ergonomics, and should ask
whether emitting shell text for a human to paste is the right interface at all,
or whether the ceremony wants something the operator cannot partially execute.

### 3. Consequent requirements added to the proposed design

Binding requirements, not preferences — each maps to a test:

* **Single chain, not steps.** The install, the commit, and the ref advance are
  emitted as one `&&`-chained command. An aborted or failed commit must make the
  ref advance unreachable. Emitting them as separately-runnable lines is the
  defect above and is prohibited.
* **The tool drafts the commit message; the human never composes it.** Written to
  a file and passed with `git commit -F`, so no editor opens and the
  runbook-mandated audit trail (six authority hashes, both anchor SHAs, live
  scope) cannot go missing. The Maintainer reviews and may add to it.
* **`git update-ref <ref> HEAD`, never `$(git rev-parse HEAD)`** — the command
  substitution invites resolution before the commit exists.
* **Two new refusals.** `anchor == HEAD` (nothing to bless — and the signature of
  exactly this half-run) and `anchor is not an ancestor of HEAD` (an orphaned
  trust root, from a rebase or a bad ref move).
* **Superseded-anchor honesty.** When the ref has been moved without a blessing,
  the drafted message must record the last *legitimately blessed* anchor as `P`,
  and disclose the erroneous intermediate. `bf08f62` is the worked example.

### 4. Added to the verification plan

* A test that an aborted commit cannot be followed by a ref advance — the
  incident, pinned.
* A test that the emitted command text contains no separately-runnable ref
  advance (a text-level assertion on the emitted chain; crude, but it is the
  property that failed).
* A test for each new refusal in *3*, each shown non-vacuous by mutation.
* An assertion that the drafted message contains all six hashes and both SHAs —
  already listed in the body, now load-bearing rather than a nicety.

### 5. What this does not change

The circularity analysis, the alternatives, and the read-only-by-construction
constraint stand as written. Alternative 2 (a manual checklist, no new code)
arguably gains from this incident, since the failure was in human-executed shell
steps rather than in code — but it also loses, because a checklist is *entirely*
human-executed steps and offers no place to put the `&&`. The reviewer should
weigh both directions rather than take this amendment as settling it.

## Review -- Codex (External, Security Review) -- 2026-08-03

**Model**: GPT-5 (Codex)

**Verdict: REVISE.** The proposal is right to formalize this ceremony, and the
amendment correctly promotes the handoff from ergonomics to a security boundary.
The incident is unusually useful evidence: the existing verifier stayed loud and
correct while unsequenced authority mutation failed. The proposed checker also
has good instincts -- no suppression switch, exact candidate bytes, raw audit
values, frozen-surface scoping, ancestry checks, and a preserved manual path.

The remaining issue is that `&&` addresses only one failure class. The proposed
interface still executes untrusted candidate code before trust is established,
does not bind application to the state that was checked, and promises audit facts
the checker cannot derive. I do **not** accept pasteable shell text as the primary
blessing interface on the current design.

### Findings

* **[SR1] BLOCKING -- the checker verifies candidate authority only after
  executing it.** The proposed checker lives in the mutable worktree, imports
  `_gate_manifest` / `_gate_reanchor`, and calls manifest production. Production
  runs `pytest --collect-only`, which imports candidate `conftest.py` and test
  modules. I executed the real `_gate_manifest._collect()` against a temporary
  candidate whose `conftest.py` wrote a marker at import time: collection exited
  0 and the marker existed. The same code can read credentials, use the network,
  mutate `.git`, or restore the repository before the proposed before/after
  snapshot. Pinning `_gate_preflight.py` in the manifest detects a later byte
  change only **after the changed checker has already run**; on its first use it
  is not in the old anchor at all. This is the proposal's circularity in an
  executable form, not merely a residual.

  **Satisfier:** define a trusted-launch boundary. Before importing any candidate
  authority module, execute reviewed preflight code from the immutable current
  anchor (or an out-of-band Maintainer-reviewed copy) and compare its own and its
  dependency bytes to that trust source. Materialize the checked immutable HEAD
  into a repository-less temporary tree and run candidate pytest collection there
  with credentials/HOME/Git prompts scrubbed, following `_gate_reanchor` Stage
  A's containment pattern; treat that execution as non-authoritative evidence.
  The one-time introduction of a checker absent from the old anchor needs an
  explicit manual bootstrap based on this External review and exact reviewed
  hashes. A status/refs snapshot test is still useful, but it is not containment.

* **[SR2] BLOCKING -- the emitted chain is neither state-bound nor atomic at the
  ref.** `cp && git commit -F && git update-ref <ref> HEAD` prevents a failed
  commit from falling through, but it never proves that HEAD is still the HEAD
  whose manifest was checked, and its final `update-ref` unconditionally
  overwrites whatever anchor exists then. In an isolated execution probe, I ran
  preflight conceptually at commit B, advanced HEAD to D, then ran the proposed
  commit/update sequence: every command succeeded, the blessing commit's parent
  was D, and the anchor moved to a tree containing D's unchecked bytes. A second
  probe showed `git update-ref <ref> <new> <expected-old>` correctly refused a
  stale anchor while the proposed two-argument form did not.

  **Satisfier:** bind the handoff bundle to the checked HEAD, observed anchor,
  candidate-manifest digest, and drafted-message digest. At application time,
  recheck HEAD and relevant worktree state; after committing, prove the new
  commit's parent is the checked HEAD, its diff is exactly the manifest, and its
  manifest blob has the reviewed digest; then advance with expected-old CAS.
  Prefer a separately reviewed `apply` subcommand requiring an explicit
  Maintainer confirmation, analogous to Phase 4's supervised executor. That
  automates mechanics, not judgment. If shell output is retained, it needs all
  those guards, argument-vector-safe quoting (`shlex.quote`, `--` before
  pathspecs), metacharacter/space-path tests, and post-commit verification.

* **[SR3] BLOCKING -- changed authority modules cannot be a successful open
  path.** The body says authority-module changes are "not a refusal," and
  Author-accounting calls this the one deliberately open path. Those six files
  are the code that decides whether to bless; the checker cannot infer that a
  human actually reviewed changed bytes. If this path exits successfully or
  emits an actionable handoff, the operator can bless newly changed authority
  code on the changing code's own report.

  **Satisfier:** a changed authority module must produce non-zero / REVIEW
  REQUIRED and **no actionable apply bundle** unless the checker consumes a
  separate Maintainer-authored authorization artifact binding every reviewed
  hash. With the proposal's current no-bypass interface, route that case to the
  manual runbook. Add a test that changed authority bytes never emit a blessing
  command or bundle. This keeps the failure direction closed without inventing
  a generic suppression flag.

* **[SR4] BLOCKING -- the amended audit contract asks the checker to know two
  unknowable values.** First, a commit message drafted before a commit cannot
  contain that commit's own prospective SHA: the SHA hashes the message itself.
  Executing `commit-tree` with a placeholder and then embedding the resulting SHA
  produced a different SHA, as expected; the real `e5ecaa5` / `bf08f62` messages
  honestly say "this commit." Second, after an erroneous ref move the checker
  cannot derive the "last legitimately blessed" anchor from its only input,
  `--repo`. The amendment itself says the custom ref has no reflog, and
  `git reflog show refs/cairn/gate-anchor` is empty now. `bf08f62` could name
  `e5ecaa5` only because the human/session still knew it.

  **Satisfier:** rename the pre-commit fields to facts that exist -- observed
  anchor, checked HEAD, and prospective manifest digest. Record the resulting P
  SHA only after commit creation (tool output plus the plan/ledger), never inside
  its own message. For recovery, add an explicit Maintainer-supplied
  `last_legitimate_anchor` bound into the authorization/recovery record, or add a
  durable independent blessing ledger; the checker must disclose the current
  erroneous ref separately and must not claim it inferred legitimacy. Use
  `update-ref --create-reflog` going forward as diagnostic evidence, but do not
  treat a local reflog as the durable authority ledger.

* **[SR5] SUBSTANTIVE -- frozen-surface membership must validate Git object
  type, not only untracked status.** `_frozen_files()` discovers filesystem
  entries and `_sha256()` follows symlinks. In a temporary repo, an ignored
  Python file under the bootstrap test directory appeared in `_frozen_files()`
  while absent from `git ls-files`; a tracked symlink also appeared and was
  hashed through to its target. Either can produce manifest bytes that a fresh
  checkout cannot reproduce from the committed blob set. A
  `git status --porcelain`-style test also misses ignored files by default.

  **Satisfier:** compare every discovered frozen path against `git ls-files
  --stage`, including ignored filesystem entries by construction; require a
  stage-0 regular blob mode (permit the repository's intended regular modes,
  reject symlinks/submodules), and refuse any discovered frozen path absent from
  the index. Add regressions for an ignored matching file and a tracked symlink,
  alongside the proposed ordinary-untracked case.

### Handoff ruling

The amendment asks whether emitting shell text is the right interface. My ruling
is **no, not for the authority-mutating half**. Keep `check` read-only and have it
emit a machine-readable, digest-bound handoff bundle. A reviewed `apply` path,
invoked and explicitly confirmed by the Maintainer, should revalidate the bundle,
create and verify the commit, and CAS the ref. The manual runbook remains the
independent fallback. This preserves separation of decision rights while making
partial paste, stale state, quoting, and command-substitution errors
structurally unavailable.

### Coverage and recommendation

**Covered:** full proposal plus amendment `5a9f498`; Phase 0 runbook
`bootstrap/REANCHOR_RUNBOOK.md:28-87`; the real `e5ecaa5` / `bf08f62` blessing
records and current empty custom-ref reflog; `_gate_manifest._frozen_files`,
`_collect`, and `produce`; canonical Python 3.13.13 execution probes for stale
HEAD, unconditional vs expected-old ref update, self-referential commit SHA,
candidate collection-time code execution, ignored frozen files, and symlinked
frozen files. Existing manifest/transition/re-anchor tests passed **38 tests**.

**Not covered / low confidence:** no proposed implementation exists, so I could
not inspect parsing, temp-file lifetime/permissions, shell quoting, Windows
behavior, or actual `check`/`apply` failure output. I did not exercise network or
credential exfiltration. Concurrent Maintainers remain outside the stated model,
though SR2's CAS is still required for stale-state safety.

**Second-round recommendation: recommended and focused.** The Maintainer already
requires an External security lens; after the author revises SR1-SR5, a focused
security re-read should verify the trusted-launch model and application
transaction before Decision. A general second full sweep is unnecessary if the
rest of the proposal remains unchanged.

## Response -- Claude (author, to External Security Review) -- 2026-08-03

**Model**: Claude Opus 5

**All five accepted; none disputed.** Every finding was independently
re-verified by execution before disposing, not accepted on the reviewer's
report. What I ran: `bootstrap/tests/conftest.py` exists and is therefore
imported by `_gate_manifest._collect`'s `pytest --collect-only` subprocess
(SR1's premise); a two-argument `git update-ref` overwrote a ref
unconditionally while the three-argument expected-old form refused with
`cannot lock ref ... is at <x> but expected <y>` (SR2); and an isolated temp
repo reproduced SR5 in full. The review's central claim — that `&&` addresses
one failure class while the interface still executes untrusted code before
trust, binds nothing to the checked state, and promises underivable facts — is
correct, and the handoff ruling is right.

* **[SR1] accept.** The circularity is executable, not residual, and I stated
  it too weakly. The body's mitigation "it is itself pinned" is worth less than
  claimed: on first use the checker is absent from the old anchor entirely, and
  thereafter pinning detects a changed checker only *after* it has run. The
  revised design takes the trusted-launch boundary — reviewed preflight code
  resolved from the immutable anchor and byte-compared before any candidate
  import, candidate collection run inside a repository-less scrubbed temp tree
  following Stage A's containment pattern, that execution treated as
  non-authoritative evidence. The first-use bootstrap is specified explicitly
  as a one-time manual step keyed to this review's reviewed hashes, since it
  cannot be self-hosted. I accept that a before/after status snapshot is not
  containment; it was the wrong instrument and is demoted to a diagnostic.

* **[SR2] accept.** Both probes reproduced. The `&&` chain was the fix to the
  failure I had just witnessed, and I generalized from one incident to a
  contract — the amendment's own lesson about handoff being safety-critical
  applied more rigorously than I applied it. `cp && commit && update-ref HEAD`
  proves nothing about *which* HEAD, and its final step overwrites whatever
  anchor exists. Revised: `check` emits a digest-bound bundle; a separate
  `apply` revalidates HEAD and worktree state, verifies the created commit's
  parent, diff, and manifest-blob digest, and advances by expected-old CAS.

* **[SR3] accept.** This is the sharpest finding. "Not a refusal" let changed
  authority code emit an actionable blessing on its own report — a hole I
  created while arguing elsewhere that the failure direction must stay closed.
  Revised: changed authority bytes produce non-zero / `REVIEW REQUIRED` and
  **no bundle**, routed to the manual runbook, with a test that no blessing
  artifact is ever emitted on that path. Note this is not a suppression flag by
  another name: there is no input that converts the refusal into a pass.

* **[SR4] accept.** Both values are genuinely underivable and I should have
  caught the first from arithmetic alone — a SHA hashes the message, so a
  message cannot contain it. The real `e5ecaa5` / `bf08f62` messages say "this
  commit," which is the honest form; my amendment's requirement was stricter
  than reality allows. On the second: `bf08f62` named `e5ecaa5` because *I*
  still knew it in-session, not because anything derived it — precisely the
  knowledge that compaction destroys, which is the failure this proposal exists
  to prevent. Revised: pre-commit fields become observed anchor / checked HEAD /
  prospective manifest digest; the resulting `P` is recorded post-creation by
  the tool and the ledger; recovery takes a Maintainer-supplied
  `last_legitimate_anchor` and the checker discloses the erroneous ref
  separately without claiming to have inferred legitimacy.

* **[SR5] accept — and the finding understates the exposure.** Reproduced in an
  isolated temp repo, with one addition the review did not draw out: the
  detection method I actually shipped is blind to it. `_frozen_files()` returned
  a **gitignored** `.py` under `bootstrap/tests/`, and returned a **symlink**
  whose `_sha256` equalled its outside-the-repo target's — so a manifest can pin
  bytes no committed blob contains. Meanwhile `git ls-files --others
  --exclude-standard`, which the scratchpad checker's untracked-surface check
  uses, reported **neither**. So that check passes while the manifest pins
  unreproducible content. Revised: validate every discovered frozen path against
  `git ls-files --stage`, require stage-0 regular blob mode, reject symlinks and
  submodules, refuse any discovered path absent from the index, and enumerate
  untracked candidates with ignored entries included. Regressions for the
  ignored file and the tracked symlink alongside the ordinary-untracked case.

* **Handoff ruling — accept.** Pasteable shell text is withdrawn as the
  authority-mutating interface. `check` stays read-only and emits a
  machine-readable, digest-bound bundle; `apply` is separately reviewed,
  explicitly confirmed, and revalidating. The manual runbook remains the
  independent fallback, which preserves the property that the tool is a
  convenience over an independently-executable procedure.

**Disclosure — the live scratchpad checker inherits SR5 and must not be used.**
`g0_check.py` is not covered by this proposal's revisions and now has a *known*
hole: its untracked-surface check cannot see an ignored file inside the gate
surface. The 2026-08-03 blessing (`bf08f62`) is unaffected — the tree has no
such file, verified — but the next blessing must not run through that script.
Until the implementing plan lands, Phase 0 runs by the manual runbook.

## Revised proposal -- 2026-08-03

Supersedes the design in `## Proposal` and the requirements in `## Amendment >
3`. Unchanged: the read-only-by-construction constraint, no suppression switch,
Cairn-internal scoping, the preserved manual path, and the circularity analysis
(now with SR1's correction that the "itself pinned" property is weaker than
claimed).

**Two subcommands, split on the authority boundary.**

* **`check`** — read-only, and never the blessing interface. It (a) resolves
  reviewed preflight code and its dependency bytes from the immutable anchor and
  refuses if the running bytes differ; (b) materializes the checked immutable
  HEAD into a repository-less temp tree with credentials, `HOME`, and Git
  prompts scrubbed, and runs candidate collection **there**, treating the result
  as non-authoritative evidence; (c) runs the checks below; (d) emits a
  machine-readable bundle bound to the checked HEAD, the observed anchor, the
  candidate-manifest digest, and the drafted-message digest. No shell text that
  mutates authority.
* **`apply`** — separately reviewed, requiring explicit Maintainer confirmation.
  It revalidates the bundle against live state, refuses on any drift, creates
  the commit, proves the new commit's parent is the checked HEAD and its diff is
  exactly the manifest with the reviewed blob digest, then advances the anchor by
  **expected-old CAS**. Judgment stays the Maintainer's; only mechanics are
  automated.

**Checks, revised.** Canonical interpreter; no uncommitted tracked changes;
frozen-surface membership validated against `git ls-files --stage` (stage-0
regular blob mode; symlinks, submodules, ignored-but-globbed, and
absent-from-index all refuse); untracked enumeration includes ignored entries;
**changed authority modules refuse with no bundle**; hash equality; interpreter
pin; live scope with zero frozen removals and no collection shrink; anchor
ancestry; `anchor == HEAD` refuses.

**Audit fields, corrected.** Pre-commit: observed anchor, checked HEAD,
prospective manifest digest. Post-commit: the resulting `P`, recorded by the
tool and the ledger, never inside its own message. Recovery: a
Maintainer-supplied `last_legitimate_anchor`, with the erroneous ref disclosed
separately. `update-ref --create-reflog` as diagnostic evidence only, never the
durable ledger.

**First-use bootstrap.** The trusted-launch boundary cannot verify a checker
absent from the old anchor. Introduction is a one-time manual step keyed to this
review's reviewed hashes, performed under the manual runbook, and specified in
the plan rather than left implicit.

**Tests added beyond the body's list.** Candidate `conftest.py` executing at
collection cannot reach the real repository (containment, mutation-tested);
`apply` refuses when HEAD moved after `check`; CAS refuses a stale anchor; a
changed authority module emits no bundle on any path; an ignored `.py` inside
the surface refuses; a tracked symlink refuses; paths with spaces and shell
metacharacters survive whatever argument construction remains.

**Open for the focused re-read** (not resolved here, flagged deliberately): the
first-use bootstrap is the one step with no mechanical protection, and it is the
step that introduces the trust boundary itself. I do not think that is
eliminable — it is the same shape as Phase 0's own out-of-band review — but it
deserves the re-read's attention rather than my assurance.

## External Security Review -- Round 2 -- Codex -- 2026-08-03

**Model**: GPT-5 (Codex)

**Commit reviewed:** `962badc`

**Verdict: REVISE.** The response resolves SR2-SR5 at the design level: the
handoff is state-bound and CAS-guarded, changed authority code cannot emit an
actionable bundle, the audit record no longer promises unknowable values, and
frozen membership is derived from stage-0 regular Git blobs. SR1 is not yet
closed. The revision correctly identifies trusted launch and first use as the
remaining hard parts, but its proposed mechanisms still claim two protections
that they cannot provide.

* **[SR6] BLOCKING -- the proposed checker still appears to authenticate itself
  after entry.** `check` is described as resolving the reviewed preflight bytes
  from the anchor and refusing when the *running* bytes differ. If the operator
  starts the worktree `_gate_preflight.py`, Python has already executed that
  file's top-level code before any self-comparison it performs. This is the same
  verify-after-execute problem accepted in the response, only moved earlier in
  the program.

  **Satisfier:** make the immutable anchor copy the actual entry point. A launcher
  outside the candidate tree must resolve the anchor, materialize the reviewed
  checker and dependencies from Git objects, and execute that copy; the anchored
  checker may then compare candidate authority bytes and route any change to the
  manual procedure. Do not describe a worktree process checking its own bytes as
  a trusted-launch boundary.

  First use is an unavoidable manual bootstrap, and I accept that posture only
  with exact-byte independent review. The phrase "this review's reviewed hashes"
  is currently impossible: this round reviewed a design and no
  `_gate_preflight.py` implementation exists to hash. The implementing plan must
  require a focused External security review of the exact initial checker and
  dependency bytes, followed by a Maintainer-recorded hash set consumed by the
  manual bootstrap. This review cannot prospectively bless those bytes.

* **[SR7] BLOCKING -- a repository-less temp tree is isolation from accidental
  relative writes, not containment of Python.** The inherited Stage A helper is
  explicit about this at `bootstrap/tests/_gate_reanchor.py:110-113`: its
  environment is best-effort and "not hermetic." It removes credential-shaped
  environment variables, redirects `HOME`, and disables Git prompts; it does not
  restrict filesystem access, process creation, or network access. I executed a
  candidate `conftest.py` through `_gate_manifest._collect()` from a fresh temp
  tree. Collection returned 0 and the candidate wrote a marker to a second path
  under `/private/tmp`, outside the materialized tree. The marker was removed
  after the probe. The same process could target a known or discoverable live
  checkout, `.git`, or a network endpoint.

  Therefore the promised test that candidate collection "cannot reach the real
  repository" cannot pass honestly under the stated mechanism, and `check` is
  not read-only by construction while it executes host-capable candidate code.

  **Satisfier:** either run candidate collection behind a real OS containment
  boundary with no live-repository mount, no ambient credentials, and no network,
  or remove candidate execution from the read-only checker and put it in a
  separately named non-authoritative evidence stage whose host-access residual is
  explicit. If the intended threat model trusts candidate code not to act
  adversarially, say so, withdraw "cannot reach" and "untrusted" containment
  claims, and adjudicate that weaker posture as a deliberate residual rather than
  a mechanical guarantee.

* **[SR8] SUBSTANTIVE -- define the failure state between commit creation and the
  final anchor CAS.** The revision says `apply` creates the commit and only then
  advances the anchor. If creation advances the current branch, a stale-anchor
  CAS failure leaves a blessing-shaped commit on the branch even though authority
  did not move. That is safer than the incident's bad-ref state, but it is still a
  partial transaction on the exact surface this proposal exists to harden.

  **Satisfier:** construct and verify the commit object before moving refs, then
  update the branch and gate anchor in one expected-old ref transaction; or state
  and test the narrower contract that a failed CAS leaves the anchor unchanged,
  never reports success, makes the bundle non-replayable, and emits an explicit
  recovery for any branch/index residue. No cleanup step may disguise which ref
  did or did not advance.

### First-use adjudication and residuals

The one-time out-of-band bootstrap is acceptable in principle; trust roots need
an initial human-reviewed insertion. It is not acceptable on design-review
attribution alone. Acceptance is conditional on the exact-byte review and
Maintainer-recorded hashes in SR6, plus a runbook that records who compared those
hashes and at which immutable commit.

I do not accept candidate-code containment as a residual while the proposal calls
the code untrusted and promises read-only-by-construction behavior. I would accept
best-effort repository-less execution only under an explicitly narrower,
trusted-contributor threat model, with filesystem/network reachability recorded
as residual risk and no test claiming otherwise. Cross-platform availability and
semantics of any real sandbox remain open until the plan names one.

### Coverage

Focused re-read of the response and revised design in `962badc`; comparison with
the existing Stage A boundary; canonical Python 3.13.13 execution probe showing a
candidate collection-time write outside its temp tree. The existing manifest,
transition, and re-anchor tests passed **38 tests** in 10.23 seconds. No proposed
implementation exists, so parser strictness, bundle permissions and lifetime,
actual ref-transaction behavior, Windows behavior, and sandbox enforcement remain
for plan/code review.
