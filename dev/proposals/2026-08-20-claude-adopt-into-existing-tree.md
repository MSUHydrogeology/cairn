# Adopting a module into an existing tree: an unfillable token, a silent keep, and a gate pointed at the archive

**Author**: Claude (Strategy)
**Model**: claude-opus-5 (Claude Opus 5)
**Date opened**: 2026-08-20
**Status**: revising
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

## Review -- Claude (Internal, fresh-context subagent) -- 2026-08-20

**Model**: claude-opus-5 (Claude Opus 5)

<!-- claim-check-allow: dev/architecture_review.md, scripts/run_security_audit.py -->

*The directive above exempts two paths this review cites as **adopter-tree
install destinations** -- the `dst` side of an `InstallSpec` -- not as Cairn
paths. Neither exists in Cairn's own tree by design, and both are named in
`bootstrap/_scaffold/config.py` at the lines cited beside them. This is the
self-host citation gotcha `AGENTS.md` names, and the directive is its
file-scoped path equivalent.*

Reviewed commit: e718eaf9bc67b4a5f3f9763e215c12e53e8f938d
Target: the complete current contract -- the whole file, opened at `aa479dc` and extended by the `## Amendment -- Claude (author) -- 2026-08-20` landed at `1354ed5`
Prior findings: none (first review)
Assurance path: high-assurance

**Tier**: Internal
**Findings**: raised (3 blocking, 5 non-blocking)

*No `Plan readiness` field is recorded. This is an Internal pass, which has no
different-agent-type read to spend, so the field is not mine to supply.*

### Steelman

Three defects, all confirmed in source rather than taken on report. D1's
citations resolve exactly: `_cmd_adopt_module` reads tokens from the lockfile
alone (`upgrade.py:1387`), `_cmd_init_lock` returns `0` early whenever a
lockfile exists (`:1138-1140`), `_resolve_current_profile` discards the token
half at `:239` while `_cmd_init_lock` keeps it at `:1154`, there is no
`--set-token` anywhere under `bootstrap/`, and `--finalize` re-attests on-disk
content rather than tokens (`lockfile.py:397`). The module-doc quote is real and
exact -- `templates/modules/team-gated/python-security.md:60-61`, *"Supply it in
the profile alongside the module selection."* The lockfile header quote is real
(`lockfile.py:_emit_lock_yaml`). `_superseded_surface_note` genuinely cannot
fire for this module: `_MODULE_SUPERSEDES` (`config.py:1206-1210`) has no
`python-security` key at all. And `--include-archive`'s docstring says every
word D3 attributes to it (`tools/lifecycle_planner.py:5354`, `:5359`, `:5361`,
`:5371`).

Three judgements are better than correct, they are load-bearing:

* **D1's persist-on-read is the right answer to the two-authorities problem**,
  and the proposal is right that it is the *whole* design. A profile that seeds
  and then stops mattering is not a second authority; a profile consulted on
  every adopt would be.
* **D3 wins on the tool's own words, not on the reporter's.** Grounding the
  contradiction in `--include-archive`'s docstring -- which holds the opposite
  position in as many words, including *"Nothing invokes `--include-archive`,
  and that is correct"* -- converts a judgement call into a documented
  self-contradiction. The refusal to "fix" it by suppressing archived findings
  inside the checker is the correct direction.
* **The Amendment's coordination fact is real and was named before it bit.**
  Two proposals, one issue, and the natural failure is a close posted from
  whichever lands first. That is worth an amendment.

The *Signals the change is wrong* section is unusually honest -- it names the
token-substitution hazard against the author's own D2 -- and the *Known
omissions* line refusing to assume `python-security` is the only spec-collision
is exactly the discipline this project asks for. My findings below are
substantially easier to write because that section exists.

### Findings

* **[R1] BLOCKING -- the `No Security Review trigger` declaration answers a
  question nobody asked, and never engages the trigger that actually fires.**
  The declaration argues the *install contract*: no schema change, no manifest
  change, protected for compatibility. That argument I verified and accept --
  `_LOCK_SCHEMA = 1` (`lockfile.py:50`) and `tokens` is a free map, so adding a
  key is genuinely not a version bump. But the install contract is the
  **third** high-risk surface in `AGENTS.md`. The **first** is *"The scaffold /
  merge engine (`bootstrap/scaffold.py` -> `bootstrap/_scaffold/`) parses
  untrusted module and **profile** files, does path handling and YAML loading,
  and writes into a target tree."* This proposal's headline `Touches` entry is
  `bootstrap/_scaffold/upgrade.py`, and D1's substance is *adding profile
  parsing and YAML loading to a path that today has none*, where the parsed
  result gates a fail-closed refusal and then a lockfile write. The proposal
  template's own gate -- *"adds, moves, or widens a trust boundary
  (deserialization, subprocess invocation, parsing, file and path handling...)"*
  -- fires textually on that sentence, and `AGENTS.md`'s assurance-path rule
  says a named high-risk surface *"takes its Security Review on its own
  trigger, whatever this field says."*

  The author's S5 answer -- an attacker who can write `profile.yml` could
  already write the lockfile -- is a good *risk* argument and I think it is
  right. It is not a *trigger* argument, and the trigger is structural. The
  distinction is not bookkeeping: **[R2] and [R8] are two concrete things a
  Security Review lens found in this exact code, and neither appears anywhere in
  S1-S5.** The invitation to challenge the call was scoped to "if D2's byte
  comparison reads differently"; D2 is not where the call goes wrong.

  Suggested edit to the header:

  > **Security Review**: required -- D1 adds profile parsing / YAML loading to
  > `_cmd_adopt_module`, inside `bootstrap/_scaffold/`, the scaffold-engine
  > surface `AGENTS.md` names first. No trust boundary *moves*, and the install
  > contract is unchanged; the trigger is the new parse on a write-gating path.

* **[R2] BLOCKING -- D1 as specified introduces a fail-open the current code
  does not have: the two "unfilled value" predicates disagree, and the proposal
  names the weaker one.** `missing_required_tokens` (`config.py:1301-1330`)
  treats a required token as unfilled when it is absent, blank, or matches
  `_UNFILLED_TOKEN_VALUE = re.compile(r"\{\{\s*[\w.-]+\s*\}\}")`
  (`config.py:1284`) -- **curly-brace placeholders only**. `_cmd_init_lock`
  carries a *separate, additional* guard for **angle-bracket** placeholders
  (`upgrade.py:1146-1148`, `v.strip().startswith("<") and
  v.strip().endswith(">")`), because the profile template it writes uses exactly
  that form (`upgrade.py:1058-1061`, `"<your project name>"`). That second guard
  lives in `_cmd_init_lock`'s **body**, not in `_resolve_lock_profile_fields`
  (`upgrade.py:1064-1084`) -- the helper this proposal instructs the plan to
  reuse.

  So D1, implemented as written, accepts `python_package: "<my package>"` from a
  committed profile: the preflight passes, the value substitutes into installed
  files, and it is **persisted into the lockfile as a filled token** -- on the
  authority this proposal argues becomes single and final. Today no such value
  can reach a lockfile by any supported path, because the one writer that
  accepts profile tokens refuses it. The *Edge cases* inventory lists "profile
  present but token absent" and "token in both sources and disagreeing"; it does
  not list "profile present, token present, value is an unfilled placeholder",
  which is the case the existing code took the trouble to guard.

  This is not hypothetical polish: the lockfile is the artifact whose own header
  says *do not hand-edit*, and the whole point of D1 is that adopters stop
  hand-editing it. Writing a placeholder into it via the supported path is
  strictly worse than the hand-edit it replaces. **The proposal must say which
  predicate governs the adopt path**, and if it is the stricter one, say where
  that check lives -- because "reuse `_resolve_lock_profile_fields`" hands the
  plan the narrower one by construction.

* **[R3] BLOCKING -- D2's specification and D2's stated risk are two
  incompatible specifications, and the document resolves the contradiction by
  assigning it to the plan.** *Proposal > D2* says: compare on-disk bytes to
  template bytes, *"Both are already in hand -- `theirs_b` and
  `dst_abs.read_bytes()`."* `theirs_b` is the **raw** template
  (`upgrade.py:143-148` reads the file and returns its bytes; no substitution).
  A non-verbatim spec installs `substitute_tokens(theirs_b.decode("utf-8"),
  tokens)` (`upgrade.py:1425-1427`). *Signals the change is wrong* then says the
  comparison *"must be against the **substituted** template, not the raw one, or
  the note fires on every mergeable spec"*, and assigns proving it to the plan.
  A plan cannot choose between two contract statements in its own baseline; it
  can only pick one and be accused of deviation either way.

  **Instrument confirmed rather than assumed** -- the pattern could have matched,
  and did. Mergeable (non-`verbatim`) module specs carrying *real* substituted
  tokens exist today:

  | template | token(s) | dst | verbatim? |
  |---|---|---|---|
  | `templates/modules/default-on/claim-check.md` | `{{claim_check_command}}` x6 | `dev/modules/claim-check.md` | no (`config.py:784-785`) |
  | `templates/modules/default-on/lifecycle-metrics.md` | `{{metrics_command}}` x4 | `dev/modules/lifecycle-metrics.md` | no (`config.py:740-741`) |
  | `templates/modules/team-gated/architecture_review_template.md` | `{{project_name}}` | `dev/architecture_review.md` | no (`config.py:1144-1145`) |

  None of those three token names is in `_DOC_AUTHOR_TOKENS`
  (`slotmerge.py:472-479`), so all three really are substituted at install and a
  raw comparison really would differ. The `architecture-review` row is the
  sharpest case: that same dst is *also* the module's declared superseded
  surface (`config.py:1209`), so an adopt against a tree that already has it
  would emit the D2 advisory **and** `_superseded_surface_note` about the same
  path in one run -- a spurious note, doubled.

  Two things make this cheap to fix rather than a redesign, which is why I raise
  it as under-specification and not as a design objection: (i) the "costs no
  additional I/O" justification survives intact, because substitution is CPU,
  not I/O; (ii) the flagship case is unaffected either way --
  `run_security_audit.py` is `verbatim=True` (`config.py:1043-1044`), so raw ==
  installed for it. That second fact is precisely why the specification must not
  be settled by reasoning from the motivating example. Suggested edit to
  *Proposal > D2*, replacing the "Both are already in hand" sentence:

  > In the `else` branch of the spec loop, compare the on-disk bytes to **what
  > this spec would install** -- `theirs_b` for a `verbatim` spec, and
  > `substitute_tokens(theirs_b.decode("utf-8"), tokens)` for a mergeable one,
  > matching the `if not dst_abs.exists()` branch immediately above
  > (`upgrade.py:1425-1427`) line for line. Comparing against the raw template
  > would fire on every mergeable spec that carries a token.

* **[R4] MEDIUM -- D2 is placed in a branch the motivating collision may never
  reach, and the branch it misses is even quieter.** The spec loop skips a
  destination *before* the exists/else split:

  ```
  if dst_rel in lock_dsts:
      continue  # already tracked under another roster entry; skip the file
  ```

  (`upgrade.py:1411-1412`). A destination already tracked under another roster
  entry is not compared, not recorded, not appended to `added`, and produces
  **no output whatsoever** -- so the `recorded N file(s)` success line
  (`:1447`) silently under-counts, and the adopter is told a number that does
  not describe what happened. That is *the same failure D2 names* -- "adoption
  cannot say `I kept yours`" -- one branch earlier and with less signal, and
  D2's `else`-branch placement does not reach it.

  Which branch the reporting adopter actually hit is not established anywhere in
  *Context*. If their `scripts/run_security_audit.py` was untracked in the
  lockfile, they hit the `else` branch and D2 as specified covers them. If it
  was tracked under an earlier roster entry, they hit `continue` and D2 does
  nothing for them at all. The proposal should either extend D2 to the
  `continue` branch, or state -- with the reason, and with the *Context*
  evidence that settles which branch was taken -- that it deliberately does not.
  Note this also interacts with *Known omissions*: the per-module collision
  measurement the plan is asked to perform should distinguish the two branches,
  or it will measure the wrong set.

* **[R5] MEDIUM -- D3's positive claim survives measurement; the enumeration
  presented alongside it does not, and the enumeration is the part the plan is
  told to rely on.** The headline -- `bootstrap/UPGRADE.md:255` is the only
  *recommendation* -- I re-measured and it holds. But the sentence that follows
  it, *"The other occurrences are not advice and are left alone: [four named]"*,
  is framed as exhaustive and is not. Measured at `e718eaf`, `as_of 2026-08-20`,
  with `git grep -n -- '--include-archive'` over tracked files, matches also
  occur in: `tools/lifecycle_planner.py` (x6); **`templates/skills/_lib/
  lifecycle_planner.py` (x6)**; `dev/plans/archive/archive-precondition-
  substance.md` (x10); `dev/plans/archive/deferral-discipline.md` (x3);
  `dev/plans/archive/release-security-bar.md`; `dev/plans/archive/review-gate-
  enforcement.md` (x4); `dev/plans/archive/review-efficient-lifecycle.md` (x2);
  `dev/proposals/archive/2026-08-11-claude-archive-precondition-substance.md`
  (x10).

  Three consequences, in ascending order of how much they matter:

  1. `templates/skills/_lib/lifecycle_planner.py` is the **shipped
     byte-identical twin** (verified: `cmp` reports identical at `e718eaf`), and
     it is the copy an adopter's installed tree actually runs. D3's authority
     for the whole argument is a docstring the proposal cites only at `tools/`.
     Cite the twin too, or say the pair is byte-identical and why that is
     enough -- an adopter-facing argument should point at the adopter's file.
  2. On the `--include-archives` side, the named pair (`CHANGELOG.md`,
     `dev/modules/doc-drift-prevention.md`) omits `scripts/link_check.py`,
     `scripts/check_cairn.py`, **`templates/modules/team-gated/link_check.py`**,
     and **`templates/modules/team-gated/doc-drift-prevention.md`** -- the last
     two being shipped templates. The proposal's own warning is *"a careless fix
     edits the wrong document"*; the conflation surface it hands the plan is
     roughly a third of the real one.
  3. `dev/plans/archive/release-security-bar.md:662` is a table row citing
     `bootstrap/UPGRADE.md:255` **by line number** for this exact command.
     Archived, immutable, correctly left alone -- but the plan should know a
     landed record points at the line it is about to rewrite, so that it is a
     recorded fact rather than a later surprise.

  The fix is small: state the exact command and its exact match set, or drop the
  "the other occurrences are" framing to "the occurrences that could be mistaken
  for advice are". A separate trivial note: the cited docstring range
  `tools/lifecycle_planner.py:5352-5375` stops one line short of the
  *"development-time instrument for validating a predicate"* sentence D3
  paraphrases, which is at `:5376-5378`. Extend the range.

* **[R6] MEDIUM -- the Amendment's section 2 is right on the substance and
  asymmetric on the protocol.** Section 6 asks a reviewer to test whether gap 3
  is genuinely out of scope or was moved out for convenience. **It is genuine.**
  The sibling's own D1 carries the independence argument in its own words --
  that proposal *"stops the mixed tree, but an imperative that overreaches its
  audited set is wrong on a clean tree too. It just stops getting caught"* -- and
  the defect it fixes (`content_scan_runner.py`'s exit-3 imperative over a
  baseline with four consumers) survives every fix in *this* proposal. A
  scanner-scope defect that outlives the upgrade-path fix does not belong on the
  upgrade path. Section 2's mapping stands and section 6's question is answered
  yes.

  **What does not stand is the closure protocol.** The sibling's amendment
  carries an explicit tiebreak: *"Whichever of the two lands second carries the
  close; whichever lands first posts a progress comment and leaves the issue
  open."* This amendment says only that its closing chunk is **blocked on the
  sibling**, and its second bullet covers the sibling being *rejected or
  narrowed*. It does not cover the ordinary in-flight case -- this proposal
  lands first, the sibling is still under review -- where a progress comment on
  #5 is owed and this plan is the only party in a position to post it. So the
  shared closure event has a written protocol in one of the two derived plans
  and a one-directional block in the other. That is exactly the failure this
  amendment identifies one paragraph earlier: *"It is not enough for the author
  to know it."* A plan is read alone. Suggested edit, appended to section 2's
  first consequence bullet:

  > Whichever of the two proposals lands **second** carries the close for #5;
  > whichever lands **first** posts a progress comment naming the gaps fixed,
  > the gap still open, and the sibling holding it, and leaves #5 open. This
  > sentence is in the sibling's amendment too, and is stated in both because
  > each plan is executed without the other in view.

* **[R7] LOW -- "Reuse `_resolve_lock_profile_fields`" names a helper that
  cannot supply the disposition the proposal promises.** *Failure modes* states
  that an unparseable `profile.yml` *"falls back to the lockfile's embedded
  profile with a warning, matching `_resolve_current_profile`'s existing
  disposition"*. That fallback and its `[warn]` line live in
  `_resolve_current_profile` (`upgrade.py:216-250`) -- which is precisely the
  function that **throws the tokens away** at `:239`. `_resolve_lock_profile_
  fields` (`upgrade.py:1064-1084`) has no fallback, no warning, and raises
  `PresetError` on an unknown preset; `_cmd_init_lock` turns that into `return
  1` (`:1155-1157`), a refusal, not a fallback. The proposal promises one
  function's disposition while instructing reuse of a different function. Name
  the layer that supplies the fallback -- most plausibly widening
  `_resolve_current_profile` to return its token half rather than discarding it,
  which is also the smallest change and the one the *Context* argument already
  points at.

  Related and worth adding rather than fixing: `_resolve_lock_profile_fields`
  filters to `KNOWN_TOKENS` (`config.py:63-75`, five names), so a profile cannot
  introduce arbitrary lockfile token keys. That is a real and useful bound on
  what "read the profile" admits, and it currently goes unstated -- the S1
  answer would be stronger for saying it.

* **[R8] LOW, and part of R1's case -- D1 creates a second lockfile-token write
  path that skips `_refuse_secret_tokens`.** `_refuse_secret_tokens`
  (`lockfile.py:243-260`) is the `bootstrap/SAFETY.md` control that refuses
  secret-bearing token *names* into a lockfile. `git grep` at `e718eaf` finds
  exactly one production caller: `install.py:1667`. Neither `_cmd_init_lock` nor
  `_cmd_adopt_module` calls it, so the invariant "every lockfile token write
  clears the secret-name refusal" already has one exception and D1 adds a
  second. Bounded today by `KNOWN_TOKENS` per R7, so this is latent rather than
  live and I do not think it blocks. I raise it because it is the shape of thing
  a Security Review names and S1-S5 does not -- the preflight asked "who
  supplied it" and "which way does it break", and never asked which existing
  control the new write path bypasses.

### Coverage

**Covered.**

* **Citation integrity (every source line in the document).** Opened each:
  `upgrade.py:216`, `:239`, `:1128`, `:1138-1140`, `:1154`, `:1337`, `:1387`,
  `:1419`, `:1447` -- all resolve to the claimed content. `bootstrap/
  UPGRADE.md:255` verified verbatim including the surrounding remedy paragraph.
  `tools/lifecycle_planner.py` docstring quotes verified at `:5354`, `:5359`,
  `:5361`, `:5371` (range off-by-one noted in R5). Module-doc quote verified at
  `templates/modules/team-gated/python-security.md:60-61`.
* **Absence claims, each with the instrument confirmed against a known
  positive.** `--set-token`: `git grep 'set-token\|set_token' -- bootstrap/`
  returns nothing, and the same grep shape returns hits for `--finalize`, so the
  pattern could have matched. `_MODULE_SUPERSEDES` has no `python-security` key
  (`config.py:1206-1210`) while it does have three other keys, so the negative
  is a real negative. `run_security_audit.py` appears exactly once in
  `_MODULE_MAPPINGS` (`config.py:1043-1044`) -- `content-security`
  (`config.py:1003`) does **not** ship that path, which the *Context* wording
  ("from the `content-security` era") could mislead a reader about.
* **D3's measurement, re-run rather than accepted.** `git grep -n --
  '--include-archive'` at `e718eaf`; result and the enumeration gap in R5. Twin
  byte-identity checked with `cmp`.
* **Contract-stability claim.** `_LOCK_SCHEMA = 1` (`lockfile.py:50`); `tokens`
  is an unconstrained map; adding a key is not a schema bump. The "no lockfile
  schema change" claim is **true as stated**.
* **Public-path -> test mapping.** Both cited files exist
  (`bootstrap/tests/test_upgrade_module.py`,
  `bootstrap/tests/test_module_merge_lockfile.py`); relative links resolve.
* **Author-accounting challenged, not counted.** Sampled the *Edge cases* row
  and falsified it (R2: the placeholder case is absent and is the one the
  existing code guards); sampled *Failure modes* and falsified it (R7: the named
  disposition belongs to a different helper); sampled S2's mutation pair and
  accept it as sound -- the "note absent on byte-identical files" second test is
  the right instrument-confirmation and is correctly demanded.
* **Cross-artifact scope.** Read `dev/proposals/2026-08-20-claude-scanner-claim-
  scope.md` in full through its amendment to test the gap-3 split and the
  closure mapping (R6).

**Not covered / low confidence.**

* **Same-type reviewer -- no cross-type independence on this pass.** Independence
  here is by time and context only.
* **Nothing was executed.** I ran no pytest, no `--dry-run`, no `--manifest`, and
  built no fixture tree. R2, R3 and R4 are read from source and are *predictions
  about behaviour*, not observations of it. Each is stated so a single fixture
  falsifies it, and each should be falsified that way before it is dispositioned
  -- particularly R4, whose reachability depends on facts about the reporter's
  tree that are not in the record.
* **The adopter's figures are unverified and unverifiable here.** 244 of 247, 1
  of 1, 102 archived plans, and the SR-1 / pip-audit / conda-enumeration
  behaviours in D2 are all reported, on a tree I cannot see. They are plausible
  and consistent with the docstring's own account, and none of my findings
  depends on them -- but no reader should take them as confirmed by this pass.
* **Issue #5 / #7 contents not read.** I have no network access, so the closure
  mapping in R6 is tested against the *sibling proposal's* account of the gaps,
  not against the issues themselves. If the issues' gap numbering differs from
  the proposals', R6's conclusion changes and I could not detect it.
* **The `KNOWN_TOKENS` bound (R7, R8) was not tested against a profile carrying
  an unknown key.** I read the filter; I did not exercise it.
* **No per-module spec-destination collision census.** The proposal's *Known
  omissions* correctly reserves this for the plan, and I did not perform it
  either -- so R4's "which branch did the adopter hit" stays open.

### Second-round recommendation

**Recommended, and specifically an External or Security pass -- not another
Internal one.**

Grounding it in the negative space rather than in the topic: R1 is a claim about
which *trigger* fires on a surface `AGENTS.md` names, and R2 and R8 are the two
concrete things that lens surfaced in a single read of code the author had
already read carefully. That is evidence the lens is productive here, not an
inference from the change's size. The proposal's own header invited the
challenge but scoped it to D2's byte comparison; the call goes wrong on D1, and
D1 is the arm that writes.

The Internal floor is met by this pass and the author's Response can dispose
R1-R8 on the record. What this pass could not do is execute anything, and R2's
severity in particular turns on a behaviour -- does a `<...>` value really reach
the lockfile through the specified design -- that one fixture settles and no
amount of reading does. A reviewer with a different failure imagination, running
the code, is worth more here than a second reader of the same document.

If the Maintainer prefers to spend no independent read at proposal stage, the
minimum I would ask is that R1's disposition be explicit rather than folded into
a revision: either the Security Review is declared, or the reason the
scaffold-engine trigger does not fire is written down where the next reader
finds it. "It was considered" is not recoverable from a revised header.
