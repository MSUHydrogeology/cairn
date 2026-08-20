# Adopting a module into an existing tree: an unfillable token, a silent keep, and a gate pointed at the archive

**Author**: Claude (Strategy)
**Model**: claude-opus-5 (Claude Opus 5)
**Date opened**: 2026-08-20
**Status**: awaiting-review
**Assurance path**: **high-assurance** — mandatory. The change touches the
**install contract** (`AGENTS.md` > High-risk surfaces): the lockfile and the
`--adopt-module` path that writes it.
**Touches**: `bootstrap/_scaffold/upgrade.py` (`_cmd_adopt_module`, its error
text, and its use of the existing profile reader); `bootstrap/UPGRADE.md`;
`bootstrap/tests/test_upgrade_module.py` and
`bootstrap/tests/test_module_merge_lockfile.py`. **No lockfile *schema* change,
no change to `scaffold.py --manifest`, no change to the fidelity or gate
manifests.**
**Related**: adopter issues
[#5](https://github.com/MSUHydrogeology/cairn-scientist-ai-teams/issues/5)
(gaps 1 and 2) and
[#7](https://github.com/MSUHydrogeology/cairn-scientist-ai-teams/issues/7).
Issue #5's gap 3 is deliberately **not** here — it is a scanner-scope defect that
is wrong on a clean tree too, and it is drafted as
[`2026-08-20-claude-scanner-claim-scope`](2026-08-20-claude-scanner-claim-scope.md).
Sibling: [`2026-08-20-claude-portable-sweeps-cannot-run`](2026-08-20-claude-portable-sweeps-cannot-run.md).
**Plan review**: required(**Internal**) — an Internal proposal review spends no
different-agent-type read, so no `Plan readiness` inheritance is claimed. **No
Security Review trigger**: the install contract is a protected surface for
*compatibility*, and this change adds no trust boundary, no subprocess, no
parser over untrusted input, and no executable path. That call is the author's
and a reviewer should challenge it if D2's byte comparison reads differently.

## Context

An adopter upgrading `0.2.0` → `a26a180` via `upgrade --stage/--apply` and then
`--adopt-module` hit three problems. **The first blocks adoption outright; the
second means an adopter can believe they adopted a module while still running
the old apparatus; the third points a brand-new gate at 244 findings nobody may
act on.** All three are confirmed in the source.

### D1 — a required token cannot be filled, and the printed remedy is a no-op

`python-security` requires the `python_package` token. `_cmd_adopt_module` reads
token values from the **lockfile only** (`bootstrap/_scaffold/upgrade.py:1387`),
so a tree that upgraded from before that token existed has no filled value and
adoption fail-closed refuses:

```
error: module 'python-security' requires token(s) python_package but the lockfile
has no filled value; refusing to adopt (no files written, lockfile unchanged).
Fill the token (upgrade --init-lock) and retry.
```

**The refusal is right. The remedy is not.** `_cmd_init_lock` returns early
whenever a lockfile already exists (`bootstrap/_scaffold/upgrade.py:1138-1140`)
— and every adopter who can reach this error has a lockfile. The advice can only
ever be given to someone it cannot help. There is no `--set-token` anywhere in
`bootstrap/`, and `--finalize` advances hashes rather than tokens.

**Two facts make this sharper than the issue reports.**

First, the module's own doc tells the adopter to put it in the profile:
`templates/modules/team-gated/python-security.md` — *"Supply it in the profile
alongside the module selection."* The adopter did exactly that and it had no
effect, because `--adopt-module` never reads the profile.

Second, **the engine already reads the profile at upgrade time, and already
extracts tokens from it.** `_resolve_current_profile`
(`bootstrap/_scaffold/upgrade.py:216`) reads the committed
`dev/.cairn/profile.yml` with a documented fallback to the lockfile's embedded
profile — and discards the token half of the result at
`bootstrap/_scaffold/upgrade.py:239` (`block, _tokens, missing, invalid = …`).
`_cmd_init_lock` calls the same helper and **keeps** them
(`bootstrap/_scaffold/upgrade.py:1154`). So the mechanism exists, is already
trusted on this surface, and `--adopt-module` is the one path that ignores it.

The adopter's only remaining route was hand-editing `dev/.cairn/cairn-lock.yml`,
whose own header reads *tool-owned; regenerate-only; do not hand-edit*. They did
so additively, matching what a fresh install writes, and `verify_integrity`
passes afterwards — but a documented-unsupported edit must not be the supported
path to adopting a shipped module.

### D2 — adoption cannot say "I kept yours"

For each of a module's specs, `_cmd_adopt_module` installs from template only
when the destination is **missing** (`bootstrap/_scaffold/upgrade.py:1419`);
otherwise it records the on-disk bytes as the fork entry. The success line
reports `recorded N file(s)` either way
(`bootstrap/_scaffold/upgrade.py:1447`).

The general behaviour is right — adoption is *for* trees that already carry the
files. But `python-security`'s `run_security_audit.py` lands on a path an
adopter may already occupy from the `content-security` era. Result: adoption
reports success, the module doc installs, the lockfile records the module, and
the tree keeps running a months-old orchestrator **that shares only a filename**
with the one the module ships. Nothing in the output distinguishes the two
outcomes.

There is already a partial mechanism at this exact call site:
`_superseded_surface_note` (`bootstrap/_scaffold/upgrade.py:1337`), advisory,
which flags declared superseded *local* surfaces. It does not fire here because
this collision is on a **spec destination**, not a declared superseded surface.

**What the silence costs is measurable, and the adopter measured it.** They
report the shipped orchestrator's SR-1 integrity preflight caught their manual
apparatus swap immediately — *"apparatus file does not match its lockfile hash;
refusing to self-audit from an unverified apparatus"* — that pip-audit defaults
network-off and reports `UNAVAILABLE` rather than clean, and that the run
enumerates the conda-managed packages it does not audit instead of implying
coverage. **A tree that silently keeps the old file gets none of those.**

### D3 — `UPGRADE.md` points the new gate at records nobody may edit

`bootstrap/UPGRADE.md:255` tells every upgrading adopter:

> 1. Run `python tools/lifecycle_planner.py scan --include-archive` **before**
>    you rely on the upgraded gate.

On the adopter's tree (102 archived plans): `scan` reported **1 of 1** artifacts
with structural violations — specific, quoted, actionable, and it surfaced two
genuine problems in a live proposal. `scan --include-archive` reported **244 of
247**, burying that finding under 243 reports against immutable history.

**This is not a judgment call between two defensible positions.** The checker's
own docstring holds the opposite position in as many words
(`tools/lifecycle_planner.py:5352-5375`): the default is *"deliberately
live-only"* because those are *"artifacts someone can still fix"*;
`--include-archive` is *"the **explicit strict historical audit**, not the
routine gate"*; archived records *"most predate the rules they are now measured
against, and a gate that reds permanently on records nobody may edit is one
people learn to ignore"*; and, flatly:

> **Nothing invokes `--include-archive`, and that is correct.**

One upgrade-note line contradicts the tool it recommends.

The note's own remedy also does not reach archived records: append-only forbids
editing a landed review, so the repair is a *new* conforming pass appended — for
a plan that archived months ago, that means performing a fresh review of
finished work to satisfy a schema that postdates it. Nobody will do that 102
times, and they should not: **the value of an archived record is that it says
what was believed at the time**, which a retroactive conforming pass destroys.

## Proposal

### D1 — read the profile at adopt time, and persist what it yields

`_cmd_adopt_module` resolves tokens from the committed profile **and** the
lockfile, with the lockfile's filled values taking precedence, then **writes any
newly-resolved token into the lockfile** as part of the same atomic
`_commit_lock_and_caches` it already performs.

That last clause is the whole design. The concern with a second token source is
two authorities that can disagree — which is the exact shape of issue #5's gap 3
one level down. Persisting on read means the profile acts as a **seed, never a
parallel truth**: after adoption the lockfile is the single authority, exactly as
it is today.

Reuse `_resolve_lock_profile_fields` — the helper `_cmd_init_lock` already uses
for this — rather than writing a second reader.

The refusal is unchanged in disposition and stays fail-closed: a token that
resolves from neither source still refuses before any write. Only the **error
text** changes, to name a command that can actually help.

### D2 — one advisory line when a kept file differs from the template

In the `else` branch of the spec loop, compare the on-disk bytes to the template
bytes. **Both are already in hand** — `theirs_b` and `dst_abs.read_bytes()` are
read on the next line for the fork record — so this costs no additional I/O.
When they differ, accumulate the path; after the loop, print one advisory block
naming each kept-and-differing path **and the template it differs from**, so the
adopter can diff rather than merely worry.

Print **nothing** when the bytes match. A byte-identical file is not news, and a
note that fires on the common case is how a channel becomes noise — which is the
same failure this proposal's D3 is about.

**Advisory only: it neither blocks nor overwrites.** Overwriting destroys
adopter work on a path adoption exists to protect; blocking turns a reporting
gap into a refusal on a common, legitimate case. The adopter asked for exactly
this line: *"The adopter can then decide. Silence here is the bit that
misleads."*

### D3 — drop the flag from the recommendation

`bootstrap/UPGRADE.md:255` becomes:

> 1. Run `python tools/lifecycle_planner.py scan` **before** you rely on the
>    upgraded gate.

If the archive sweep is mentioned at all, it is described as its own docstring
describes it — a development-time instrument for validating a predicate, run
when a predicate changes — with the warning that on an established tree it will
report essentially every archived artifact.

**Measured answer to the adopter's "check whether the flag is recommended
anywhere else" (`as_of 2026-08-20`, at `a26a180`): `bootstrap/UPGRADE.md:255` is
the only recommendation.** The other occurrences are not advice and are left
alone: `dev/PLANNING.md:2202` (a dated measurement),
`bootstrap/tests/test_lifecycle_contract.py:169` (contract coverage of the
flag's existence — correct to keep), and `CHANGELOG.md` plus
`dev/modules/doc-drift-prevention.md`, which describe **`--include-archives`**,
a *different flag on a different tool* (`check_cairn` / `link_check`). The plan
must not conflate the two; a careless fix edits the wrong document.

### Documentation / doctrine surface

`bootstrap/UPGRADE.md` (entry layer — the adopter-facing upgrade note) and two
error/advisory strings. **No doctrine rule changes**, so the doctrine-evolution
rate-limit gate is not engaged. D3 in particular *removes* a line that
contradicts existing doctrine rather than adding a rule.

## Rationale

**Which user workflow this improves:** every upgrade into an existing tree —
which is the workflow Cairn has the least evidence about, because Cairn itself
is a fresh-install tree and cannot exercise it on its own.

**What contract it preserves:** the lockfile schema, the manifest, and the
fail-closed refusal all stay exactly as they are. D1 changes *where a value may
be found*, not what is recorded or how integrity is verified.

**Why now:** D1 makes a shipped module unadoptable by its documented procedure;
D2 lets an adopter believe they adopted it when they did not; D3 is a one-line
contradiction that costs the adopter's trust in a gate on first contact. The
three arrive together because they are one journey.

## Alternatives considered

* **Add `--set-token NAME=VALUE`** (the adopter's second preference). Narrow,
  auditable, and it is genuinely the missing operation. **Kept as the named
  fallback, not the primary**: it adds a new CLI surface to a published,
  byte-level-stable install contract, and it leaves the module doc's own
  instruction ("supply it in the profile") still wrong. Worth revisiting for a
  tree with no committed profile — the plan should say what happens there.
* **Fix only the error text** (the adopter's minimum). Rejected: it leaves
  hand-editing a do-not-hand-edit file as the supported path to adopting a
  shipped module.
* **Read the profile without persisting to the lockfile.** Rejected — it creates
  the two-authorities problem this proposal exists partly to avoid.
* **Make D2 block, or overwrite.** Rejected, both directions, above.
* **Suppress archived findings inside the checker** rather than removing the
  recommendation. Rejected: `--include-archive` is *correct* and has a real use;
  the defect is one document pointing an adopter at it on an upgrade path.
* **Do nothing.** The next adopter repeats all three, and the third one teaches
  them that this project's tooling output is noise.

## Evidence / verification plan

### Author-accounting — invariants, failure modes, edge cases

* **Invariants.** (i) A module whose required token resolves from nowhere still
  refuses **before any write or lockfile mutation** — enforced by the existing
  preflight, plus a test asserting no file and no lockfile change on refusal.
  (ii) After a successful adopt, every required token has a value **in the
  lockfile** — a new test. (iii) The lockfile schema is unchanged — the existing
  schema/contract tests, unmodified.
* **Failure modes.** Unresolvable token → refuse, closed. Unparseable
  `profile.yml` → falls back to the lockfile's embedded profile with a warning,
  matching `_resolve_current_profile`'s existing disposition — **not** silently
  clean. Kept-file byte comparison fails to read → the advisory says so; it
  never suppresses the note, and it never fails the adopt (open, and
  intentionally so: an advisory that can break an install is worse than the
  silence it replaces).
* **Edge cases.** No `profile.yml` at all; profile present but token absent;
  token in both sources and disagreeing (**lockfile wins** — a test pins the
  direction); destination present and byte-identical (no note); destination
  present and differing (one note); several differing (one block, all listed);
  module already in the roster (existing early return, unchanged).
* **Public-path → test mapping.** `--adopt-module` through its real CLI entry
  point in
  [`test_upgrade_module.py`](../../bootstrap/tests/test_upgrade_module.py), with
  lockfile-shape assertions in
  [`test_module_merge_lockfile.py`](../../bootstrap/tests/test_module_merge_lockfile.py).
* **Known omissions.** Whether other modules besides `python-security` collide
  on a spec destination is **not** enumerated here. The plan should measure it —
  a per-module answer, not an assumption — and an unmeasured "probably only this
  one" is exactly the confident absence this project has been bitten by.

#### Security preflight — five questions

*Gated, and answered because the surface is protected even though the author's
judgement is that no trust boundary moves. A reviewer should test that judgement
rather than accept it.*

* **S1 — Who supplied it?** D1 adds one input to the adopt decision:
  `dev/.cairn/profile.yml`, a **committed, adopter-owned, schema-validated** file
  already read by the upgrade path. It is not supplied by anything being decided
  about. D2 adds no decision input — it compares two byte buffers already read.
* **S2 — Can it fail?** For the "token persists to the lockfile" test: delete the
  persist call and it must redden. For the "kept-and-differing note" test: make
  the comparison always-equal and the note must vanish, reddening a test that
  asserts its presence — **and** a second test must assert the note is *absent*
  on byte-identical files, or the pair cannot distinguish "correct" from "always
  fires". Both mutations run and are recorded.
* **S3 — What fires it, over what?** `python -m pytest bootstrap/tests` selects
  both files; nothing else runs them — no CI, no hook. `bootstrap/UPGRADE.md`'s
  prose must be quoted in the plan and shown to agree with the command it now
  recommends.
* **S4 — Which way does it break?** The token refusal stays closed. The profile
  fallback is *open* and unchanged from its existing behaviour — it is loud, and
  it lands on the lockfile, which is the more-trusted of the two. The D2
  advisory is open by construction and grants no authority: it prints.
* **S5 — Who still wins?** Assumes an attacker who can write to the adopter's
  tree. Such an attacker can still edit `profile.yml` to supply a token value —
  but they could already edit the lockfile, the templates, and the engine, so
  this adds no capability. What it does **not** close: an adopter who ignores
  the D2 advisory keeps running an unverified apparatus. That class is closed
  only by the operator reading the line, which is why the line must not fire on
  the common case.

### Tests required

`bootstrap/tests/test_upgrade_module.py` and
`bootstrap/tests/test_module_merge_lockfile.py`, per the mapping above. Every
D2 case must be **synthesized** — a fixture tree with a deliberately-differing
destination — because a tree without the collision cannot exercise the change
and a test that passes on its absence proves nothing.

### Examples / smoke checks

`python bootstrap/scaffold.py --manifest` and `--dry-run` must be byte-unchanged
(the published contract). An end-to-end adopt against a fixture tree carrying a
pre-existing differing `run_security_audit.py` is the smoke that reproduces the
report. `python scripts/check_cairn.py` for the `UPGRADE.md` edit.

## Signals the change is wrong

* **A token resolves from a profile the adopter did not intend to apply.**
  Symptom: an adopt succeeds where it should have refused. Recovery: the
  lockfile-wins precedence is the fence; if it proves insufficient, fall back to
  the `--set-token` alternative, which requires the value to be typed.
* **The D2 note fires on trees where nothing is wrong.** Symptom: adopters
  reporting the advisory on byte-identical files, or on files that differ only
  by token substitution. **This second case is the one to watch** — mergeable
  specs are token-substituted at install, so the comparison must be against the
  *substituted* template, not the raw one, or the note fires on every mergeable
  spec. The plan owns proving this; getting it wrong reproduces the exact noise
  failure D3 is about.
* **An adopter drains the live `scan` and concludes their archive is clean.**
  D3 removes a recommendation, not a capability; if the archive sweep turns out
  to be load-bearing for some upgrade, the recovery is a sentence saying what it
  is for — not restoring the flag to the default advice.

## Amendment -- Claude (author) -- 2026-08-20 -- issue closure is in scope

**Model**: claude-opus-5 (Claude Opus 5)

Appended, not merged into the sections above, per the append-only rule. This
records Maintainer direction received **after this proposal was committed
(`aa479dc`) and before any review**. It **adds** a deliverable; it withdraws
nothing, so no `Scope delta` is owed (scope as opened is `preserved`).

### 1. What was directed

> "please make sure that these proposals all include closing the issues"

### 2. What this proposal can close, and what it cannot

**It closes adopter issue
[#7](https://github.com/MSUHydrogeology/cairn-scientist-ai-teams/issues/7)
alone** — D3 is the whole of that issue, including the "check whether the flag
is recommended anywhere else" question, which is measured in *Proposal > D3*.

**It cannot close issue
[#5](https://github.com/MSUHydrogeology/cairn-scientist-ai-teams/issues/5) by
itself, and neither can its sibling.** Issue #5 reports three gaps: gaps 1 and 2
are D1 and D2 here; **gap 3 is in
[`2026-08-20-claude-scanner-claim-scope`](2026-08-20-claude-scanner-claim-scope.md)**,
because it is a scanner-scope defect that is wrong on a clean tree too and does
not belong to the upgrade path.

So issue #5 closes **only when both proposals have landed**. This is the
coordination fact most likely to be lost: each proposal, read alone, looks like
it finishes an issue it only two-thirds finishes, and the natural failure is a
close posted from whichever lands first.

Two consequences the derived plan carries:

* **The plan's closing chunk for #5 is blocked on the sibling**, named by stem,
  and states that dependency in the chunk itself rather than in a comment
  somewhere. It is not enough for the author to know it.
* **If the sibling is rejected or narrowed**, #5 does not close. It gets a
  comment saying which gaps were fixed and that gap 3 was dispositioned
  otherwise, with the reason. A partially-fixed issue closed as fixed is worse
  for the reporter than one left open.

The adopter offered this split themselves — *"Happy to file separately if that
suits triage better"* — so the split is not a liberty taken with their report.
The closing comment should say so, and should say which proposal took which gap,
so their offer is answered rather than silently acted on.

### 3. The gate and the honesty bar

Each close is an acceptance criterion of the derived plan's final chunk, gated
on: implementation landed and code-reviewed; a closing comment meeting *4*; and
**Maintainer authorization** — closing an issue on a public repository publishes
a claim that the problem is resolved, which is a publication step and not a
bookkeeping one. That chunk is **MAINTAINER-GATED**.

### 4. The closing comments must name what was declined

* For **#5**: that `--set-token` was **considered and kept as a fallback rather
  than taken** as the primary fix, and why — the profile is where the module's
  own doc already told them to put the token, and the engine already reads it.
  The adopter ranked profile-reading first, so this is agreement, but the reason
  matters because it is *not* the reason they gave.
* For **#5 gap 2**: that the advisory is **advisory only** — it will not block
  and will not overwrite — which is what they asked for, and worth confirming
  explicitly so they do not expect adoption to start refusing.
* For **#7**: that the archive sweep was **not removed, only un-recommended**,
  and that the reasoning came from the checker's own docstring rather than from
  their report alone — they were right, and they were right in company.

### 5. Something owed back to the reporter

Issue #5 hand-edited `dev/.cairn/cairn-lock.yml` against its own header's
instruction, additively, and reported that `verify_integrity` passes afterwards.
The closing comment should say **whether that tree is now in a state the fixed
`--adopt-module` will handle correctly**, or whether it needs anything. An
adopter who took a documented-unsupported route on our advice-by-absence should
not have to guess whether they are still on a supported path.

### 6. What a reviewer should test in this amendment

That *2* is right — specifically, that gap 3 really is out of scope here rather
than moved out for convenience. If a reviewer concludes gap 3 belongs on the
upgrade path after all, the closure mapping changes and this amendment is what
has to move, not the sibling.
