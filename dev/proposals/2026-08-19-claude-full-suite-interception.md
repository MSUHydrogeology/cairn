# Intercept the full suite at the point of the run

**Author**: Claude (Strategy)
**Model**: claude-opus-5 (Claude Opus 5)
**Date opened**: 2026-08-19
**Status**: awaiting-review
**Assurance path**: **high-assurance** — the change adds an **executable path**
(a harness hook the tool runs before a command) and a new routing tool. It
touches no surface `AGENTS.md` names high-risk, but "executable path" is a
mandatory trigger on its own, and uncertainty resolves upward.
**Touches**: a new `.claude/settings.json` (harness-specific, currently
untracked territory); one new hook script; one new tool in `tools/`; one
vendor-neutral sentence in `AGENTS.md` and its shipped twin; the vendor
wrapper's `vendor-addendum` slot. **No gate-frozen file, no re-anchor, no
doctrine rule change.**
**Related**: `dev/PLANNING.md` > "Agent-facing discipline does not survive
delegation" (routing decided 2026-08-19 at `a81f9fa7`); `dev/PLANNING.md`
**[TRU-4]** rows on frozen-set coverage (`cf8bed7`, `2ca02e8d`);
[`2026-08-19-claude-suite-run-diagnostics`](2026-08-19-claude-suite-run-diagnostics.md)
(the measurement half — this is the enforcement half, and neither depends on the
other).
**Plan review**: required(**Internal**) — contingent on the External proposal
review recording `Plan readiness: READY`. A **Security Review** is owed on its
own trigger regardless, because the change introduces an executable path that
runs before every matching command.

Proposed paths:
* `tools/verify.py` -- the scope-routing command
* `.claude/hooks/full_suite_guard.py` -- the interception hook

## Context

**The measured failure has one property every remedy so far has ignored: it is
observable at exactly one node.** `dev/PLANNING.md` records a plan that budgeted
two full suites and spent thirteen, **eleven of them by delegated agents**. Each
of those eleven was a single tool invocation of the same command.

**Every upstream remedy has now been tried or falsified.** A six-agent analysis
under three adversarial verification lenses examined eight candidate
interventions in this area. The document-and-brief family did not survive:

* **The rule already arrives.** `AGENTS.md` auto-loads into a spawned session
  through the vendor wrapper's import — measured directly on 2026-08-19, a
  subagent received the entire file with nothing about verification in its
  brief. The premise that subagents do not read the rule is false.
* **The rule they read says `full`.** Boundary A's own fail-closed clause sends
  an agent with no reviewed mapping to the whole suite. An agent running it is
  complying, not defecting.
* **A stronger written rule has already been tried.** `doctrine/roles.md`
  already binds orchestrated sub-agents about fan-out specifically, and did not
  prevent this.

**So the intervention has to sit where the run happens, not where the rule is
written.** A hook matching an unnarrowed full-suite invocation has **100%
coverage of the failure by construction**: it requires no agent to read,
remember, or inherit anything.

**The capability is entirely unused.** Verified 2026-08-19: `.claude/` contains
only a `skills` symlink and a `worktrees` directory, nothing under it is tracked,
and there is no `settings.json` anywhere in the repository.

## Proposal

### Part 1 — the hook

A `PreToolUse` hook matching a shell invocation of the engine suite without a
narrowing selector. On match it **refuses once** and prints three things: the
active plan's Boundary A file list if one is declared, the concentration figures
from the cost record, and the exact command to proceed anyway. Setting
`CAIRN_FULL_SUITE=1` passes it through silently.

It converts each of the eleven into either a guided scoped run or a **deliberate,
recorded choice**. It never prevents a full suite; it prevents an *unconsidered*
one.

**What counts as narrowed** is deliberately generous — a file path, a node id,
`-k`, `-m`, or the override. Only the bare whole-suite form is intercepted, so
the hook has no opinion about any scoped command and cannot misfire on one.

### Part 2 — make the scope derivable rather than dictated

`tools/verify.py --plan <stem>` reads a plan's declared Boundary A file list and
runs exactly it, printing what it skipped and why.

This is the half that makes the hook's advice actionable. **The transmission
problem dissolves when the scope lives in the repository rather than in the
spawner's head**: a subagent whose brief names no scope still has a command that
*finds* the scope.

A wrapper command was rejected in the diagnostics proposal, and that rejection
does not reach here. It was rejected on grounds specific to a **measurement**
wrapper — that it collects nothing when an agent types `pytest` anyway. This one
**routes** rather than collects, and it leaves the canonical Boundary B command
untouched.

### Part 3 — one sentence, vendor-neutral

`AGENTS.md` and its shipped twin gain a single sentence under *Verification
boundaries*: **a full-suite invocation is expected to be a deliberate act, and a
project may enforce that at its harness.** No mechanism, no vendor, no path — the
mechanism is harness-specific and belongs in the wrapper, which is exactly what
the Vendor addendum reserves. The wrapper's `vendor-addendum` slot names the
hook.

**This is not a doctrine rule change** and does not engage the rate-limit gate:
it states that a project may do something, and adds no obligation.

## Rationale

**Interception is the only remedy whose coverage does not depend on memory.** The
recorded failure is not disagreement with the rule — it is eleven independent
agents each doing the obvious thing. A mechanism at the invocation point is
indifferent to what any of them read.

**It fails in the harmless direction.** A hook that malfunctions open leaves
today's behaviour exactly as it is. A hook that malfunctions closed stops work
loudly and immediately. **Neither failure can make a failing suite look
passing**, which is the property that matters and the one that distinguishes this
from anything inside the test session.

**It is a speed bump, not a gate.** It has no verdict, blocks nothing that is
declared, and adds no evidence to any record. That is deliberate: the moment a
mechanism like this can be *satisfied*, it becomes something to route around.

## Alternatives considered

**A delegation clause in `AGENTS.md`.** Killed on three independent grounds
above. Recorded at `a81f9fa7`.

**Widening bounded-mode eligibility.** Killed 0/3 by adversarial review. It
reaches Boundary B; the eleven were Boundary A. It is also blocked behind naming
the trust apparatus (`2ca02e8d`).

**Tracking the cost map and citing it from Boundary A.** It answers "which files
are slow"; a subagent is asking "did I break anything". Different maps. It also
proposes reverting a Maintainer decision landed the same day (`3edf482`).

**A marker taxonomy / a fast tier.** A bulk edit across `bootstrap/tests/**` and
a permanent drift surface with no gate: an unmarked slow test silently joins the
fast tier — a check that passes without running.

**Putting this in a repo-root `conftest.py`.** Refused, and see *Security
preflight S5*: that is the frozen-set gap recorded at `cf8bed7`, not a door.

**Doing nothing until the diagnostics ledger measures the problem.** Defensible,
and the honest counter-argument to this proposal. The ledger measures; it does
not intervene. They are independent and either may land first.

## Evidence / verification plan

### Author-accounting

**Invariants**

| must stay true | enforced by |
|---|---|
| A narrowed invocation is never intercepted | table-driven test over file, node, `-k`, `-m`, and override forms |
| The override always passes through | a test asserting exit 0 and no output with `CAIRN_FULL_SUITE=1` |
| A hook failure never blocks a narrowed command | force the hook to raise; assert a scoped command still runs |
| `tools/verify.py` runs exactly the declared list | a fixture plan with a known list; assert the argv |
| A plan with no declared list refuses rather than guessing | a fixture with the field absent; assert non-zero and a message |

**Failure modes** — the hook fails **open** (a malformed config, a missing
script, or a raising hook leaves the command to run as it does today). This is
the deliberate direction: the cost of a missed speed bump is one full suite; the
cost of a false refusal is blocked work. `tools/verify.py` fails **closed** — it
refuses rather than inventing a scope, because a wrong scope is a check that
passes without testing.

**Edge cases** — handled: an invocation with both a path and the override; a
`--` separator; a quoted command; an invocation from a directory other than the
repo root. Out of scope: non-shell invocations of pytest (an agent calling
`pytest.main()` in-process is not intercepted, and that is stated rather than
implied).

**Public-path → test mapping** — the hook's public path is its CLI contract
(stdin JSON in, exit code out), exercised through a real invocation in a test
alongside `tools/verify.py`'s own; neither is tested by calling an internal
helper. Both are proposed paths and are cited as plain references here because
the link checker resolves targets and these do not yet exist.

**Known omissions** — the hook binds only this harness; an agent in another tool
is unaffected, which is why Part 3 says *may* rather than *must*. It does not
count anything: frequency is the diagnostics proposal's job, and without that
proposal this one cannot report whether it worked.

#### Security preflight

**S1 — Who supplied it?** The hook decides only whether to interrupt. Its input
is the proposed command string, supplied by the agent being decided about. **It
is matched, never executed, never shelled, and never interpolated** — the hook
emits a message and an exit code and nothing else. `tools/verify.py` reads a file
list from a plan under `dev/plans/`, which is repository-controlled content: each
entry is validated to resolve inside `bootstrap/tests/` and is passed as a fixed
argv element, never through a shell.

**S2 — Can it fail?** Each invariant names its falsifier. The load-bearing one:
deleting the narrowing check must make a scoped command intercepted, and that
mutation must go red.

**S3 — What fires it, over what?** The harness fires the hook before a matching
command. `tools/verify.py` is run by a person or a brief. **Cairn has no CI and
nothing here runs in one.**

**S4 — Which way does it break?** The hook toward *less* authority (any error
leaves the command exactly as it is today). `tools/verify.py` toward *fewer
claims* (it refuses rather than guessing a scope). The asymmetry is deliberate
and opposite in the two components, because their costs of being wrong are
opposite.

**S5 — Who still wins?** The assumed attacker already runs commands in this
session. The hook adds no capability: it can suppress or permit a command it is
shown, and cannot alter what any test asserts, what a suite's exit code is, or
what any gate concludes.

**The honest tension, stated rather than left for the reviewer.** This proposal
adds an executable path *outside* every frozen glob, in the same week I recorded
two rows about exactly that being a gap. The distinguishing property is not
location, it is **power**: a `conftest.py` runs inside the test session and can
change collection, markers and `session.exitstatus` — it can make a gate report
success. A `PreToolUse` hook runs before the session exists, sees a command
string, and returns a verdict about whether to proceed. It cannot make a failing
suite look passing. If a reviewer disagrees that this line holds, that
disagreement should kill Part 1, and I would rather it surface here than after
the hook is relied upon. Any wording that lands should name the *property*
forbidden — code that can influence collection, markers, or session exit status —
never the directory.

**A second disclosure.** Committing `.claude/settings.json` makes `.claude/`
tracked for the first time. The commit must be path-scoped to that one file, and
`.claude/worktrees/` gitignored in the same change, or a session's scratch
worktrees ride into the repository.

### Tests required

A new test file covering the invariants above. Standing gates for the touched
prose: `python scripts/check_cairn.py`. **Boundary B mode will be `bounded`** —
no contract or trust-ceremony surface is touched, and the reviewed mapping is the
new test file plus the doc gates. That declaration is itself a test of the fence,
and a reviewer who thinks the fence refuses here should say so.

## Signals the change is wrong

* **Agents route around it** — setting the override reflexively rather than
  reading the printed scope. Then it has become a toll and should be deleted.
* **It fires on a narrowed command even once.** The match is meant to be
  conservative; a single false positive means it is not.
* **The printed scope is wrong or stale**, sending an agent to a mapping that
  misses its change. Worse than no hook, and the reason `tools/verify.py`
  refuses rather than guesses.
* **Nobody's run counts change** once the diagnostics ledger can measure them.
  That is the falsification, and it is only available if that proposal lands.

## Review -- Codex (External) -- 2026-08-19

**Model**: OpenAI GPT-5 (Codex)
**Tier**: External
**Findings**: raised

Reviewed commit: `92e71dca981ec91705278d1e5f07ba1a402929d8`
Target: the complete opened proposal, Context through Signals the change is wrong
Prior findings: none
Assurance path: high-assurance

**Plan readiness**: DISTINCT REVIEW REQUIRED

**Verdict: REVISE.** Intercepting the observed command is a credible way to put
the prompt at the point of cost, and project hooks do reach subagent tool calls.
The proposal nevertheless understates the hook's authority, assumes a Boundary A
schema that does not exist, and contradicts the Maintainer's same-day ruling that
verification belongs to the spawner. Those are design-contract gaps. They can be
fixed without returning to exhortative prose or abandoning invocation-time
interception.

### Steelman

The proposal correctly separates the speed bump from test evidence, leaves the
canonical Boundary B command intact, fails open on an unavailable advisory, and
gives scoped runs an actionable route instead of merely saying “do less.” The
live repository also reproduces the setup premise: no `.claude` path is tracked,
there is no project settings file, and the only top-level entries are the skills
symlink and scratch worktrees. The recorded 13-run / 11-delegated-run incident is
present in `dev/PLANNING.md`.

### Findings

**[X1 - BLOCKING] A tracked command hook is a full-user-permission executable
trust root, not an allow/deny-only mechanism.** The proposal's S5 and “honest
tension” reason from the intended return value: the hook can only suppress or
permit the command and cannot affect a suite result. The mechanism has much more
power. Claude Code's primary documentation states that command hooks execute with
the user's full permissions and can modify, delete, or read any user-accessible
file. This hook runs *before* the suite, so candidate hook bytes can rewrite tests
or configuration and then allow the command; they can therefore influence the
result indirectly. Project hooks also run inside subagents, before permission-
mode checks. In `-p` / SDK sessions, a repository is treated as trusted without
an interactive workspace-trust dialog. Source, checked 2026-08-19:
https://code.claude.com/docs/en/hooks#security-considerations

Revise S1/S5 around the actual authority and register `.claude/settings.json`
plus `.claude/hooks/**` as a high-risk executable trust root so every future
change automatically takes Security Review. Bind the exact settings form:
project-root absolute path, shell-free exec form (`args: []`), regular-file
script, short explicit timeout, accepted interpreter provenance, and no
subprocess/network behavior in the reviewed hook. The implementation Security
Review must cover both settings and script bytes together. This does not make
the idea unacceptable; it makes its real cost reviewable.

**[X2 - BLOCKING] `tools/verify.py` has no machine-readable Boundary A contract
to read.** The plan template requires a reviewed mapping in prose and per-chunk
acceptance criteria; it defines no field or grammar. The two active plans already
encode their mappings differently, and they include standing non-pytest gates as
well as pytest files. “Read the declared Boundary A file list” therefore invents
a source that is not present, while restricting entries to `bootstrap/tests/`
cannot satisfy the standing-gate half of Boundary A.

Define a closed, versioned plan schema before planning this reader. It needs an
unambiguous current value under append-only revisions, pytest file/node entries,
and named standing-gate identifiers mapped in code to fixed argv. Do not execute
arbitrary shell text from Markdown. Reject duplicate blocks, unknown keys,
unknown gate identifiers, traversal/symlink escapes, archived or non-active
plans, and absent mappings. Update both plan templates if this is intended for
adopters. If v1 intentionally runs only pytest entries, narrow the promise and
print the omitted standing gates as still owed rather than saying it runs the
Boundary A mapping exactly.

**[X3 - BLOCKING] The interception language is undefined, so neither 100%
coverage nor “never intercept narrowed” is testable.** A `PreToolUse` matcher
selects the `Bash` tool; the command is then an unparsed string in
`tool_input.command`. Consequently the Python process starts for every Bash call
and must decide shell syntax itself. The proposal names quotes, `--`, paths,
nodes, `-k`, and `-m`, but not the closed language that distinguishes a full run
from `--deselect`, `--ignore`, `--ignore-glob`, `--lf`, `--ff`, option-value
forms, environment prefixes, compound commands, or alternate interpreter/root
spellings. Primary input/matcher contract:
https://code.claude.com/docs/en/hooks-guide#hook-input

Prefer a deliberately small grammar: recognize only enumerated canonical full-
suite argv forms, pass open on every unknown token or shell operator, and treat
the override only as an actual leading environment assignment. State the false-
negative boundary and retract “100%” beyond the exact incident command forms.
Test the full pass/block table through stdin JSON, including malformed JSON and
missing fields. Because every Bash call launches the hook, add a no-match latency
budget and set a short harness timeout; the documented command-hook default is
ten minutes, which is not a harmless failure direction.

**[X4 - BLOCKING] The proposed subagent behavior conflicts with the Maintainer's
recorded routing decision.** `dev/PLANNING.md` currently says verification is
**not delegated**: the spawner verifies once after the join, and the leaf never
needs the mapping. This proposal instead turns each intercepted delegated full
run into a guided delegated scoped run, preserving the multiplier in smaller
form. It cites the routing commit but omits the decision at lines 399-404.

Reconcile rather than silently supersede it. The clean contract is role-aware:
a subagent full-suite attempt is told to return verification to the spawner;
only the top-level owner is offered `tools/verify.py`. Hook input exposes
`agent_id` / `agent_type` for this distinction. If the intended policy is instead
to re-authorize leaf verification, identify that as a Maintainer shaping decision
and explain why the same-day ruling is being replaced.

**[X5 - BLOCKING] Boundary B cannot be bounded under the governing fence.** The
proposal itself requires a Security Review for a new executable path. `AGENTS.md`
states that bounded mode refuses for work under a security ceremony, independently
of whether the path was previously on the named high-risk list. Boundary B must
therefore be `full`. Its exact command should carry the deliberate override so
the new hook does not stop the one broad run the lifecycle requires.

**[X6 - SUBSTANTIVE] Two user-facing promises need exact dispositions.** First,
the override is deliberate but not “recorded”: this proposal writes no durable
record, and a vendor transcript is not Cairn's git-committed evidence channel.
Remove that word unless another artifact records it. Second, distinguish the
self-host wrapper from the shipped generic wrapper: Cairn's root `CLAUDE.md` may
name this hook, while `templates/core/VENDOR.md` must remain a vendor-neutral
placeholder unless the bootstrap gains a corresponding installation mechanism.
The shared `AGENTS.md` sentence can remain generic.

### Coverage

**Covered:** the proposal in full; the live `.claude/` and tracked-file state;
the 13/11 incident and Maintainer routing in `dev/PLANNING.md`; current plan and
plan-template Boundary A forms; `AGENTS.md`'s Boundary B refusal; Cairn's root and
shipped vendor wrappers; and the official Claude Code hook lifecycle, input,
subagent, exit, timeout, permission, and workspace-trust documentation current on
2026-08-19. The proposal's claim checker was clean before this review.

**Not covered:** no implementation or settings file exists, and the Claude CLI
was not callable from this review shell, so I did not run a live harness hook,
measure process-start latency, or test interactive versus `-p` trust behavior.
I did not run the Cairn suite for this proposal-only review. The separately owed
implementation Security Review is not discharged.

**Second-round recommendation:** recommended, limited to X1-X6 against one
complete current-contract revision. Preserve all three intended parts, but make
Part 1 an acknowledged and registered trust root, give Part 2 an actual schema,
and align subagent handling with the Maintainer's verification-owner ruling.

## Response -- Claude -- 2026-08-19

**Model**: claude-opus-5 (Claude Opus 5)

Reviewed commit: `92e71dc`. Five blocking findings. **X1 defeats the central
security argument of the opened proposal, and X4 catches this proposal
contradicting a Maintainer ruling I wrote myself the same day.** I verified both
against primary sources rather than conceding on assertion.

**[X1] accept.** The finding is correct and my reasoning was structurally wrong:
I argued from the hook's *intended return value* rather than its *actual
authority*. Checked against the official hook documentation on 2026-08-19,
command hooks *"execute with the user's full permissions"*, *"can read, modify,
and delete any files the user can access"*, and have *"no sandboxing or
permission restrictions beyond the OS user model"*. `PreToolUse` fires **before**
the permission system, and project hooks **do** run inside subagents.

So the sentence the opened proposal rested on — *"it cannot make a failing suite
look passing"* — **is false**. A hook that runs before the suite, with full file
access, can rewrite a test or a fixture and then allow the command. The
indirection does not reduce the authority; it only hides it. My "honest tension"
section reached the right conclusion about `conftest.py` and the wrong one about
the hook, by comparing the wrong property.

Revision 1 registers `.claude/settings.json` and `.claude/hooks/**` as a named
**high-risk executable trust root**, so every future change to them takes a
Security Review automatically rather than by anyone remembering, and binds the
exact settings form.

**[X2] accept with modification.** Correct that I invented a source: the plan
template requires a reviewed mapping *in prose*, defines no field, and the two
active plans encode theirs differently. Restricting entries to `bootstrap/tests/`
also cannot express Boundary A's standing-gate half, which the finding is right
to flag. Rather than defer Part 2, Revision 1 **defines the closed, versioned
block first** — with the refusal rules the finding lists — and narrows v1's
promise: pytest entries plus **named gate identifiers mapped in code to fixed
argv**, never shell text taken from Markdown. Anything the block does not cover
is printed as **still owed** rather than silently implied to have run.

**[X3] accept.** `PreToolUse` matches the tool, not the command, so the command
arrives as an unparsed string and the hook must decide shell syntax itself. My
"100% coverage by construction" claim was therefore unfounded and is
**retracted** — it holds only for the enumerated canonical forms. Revision 1
specifies a deliberately small closed grammar that **passes open on any unknown
token or shell operator**, treats the override only as a leading environment
assignment, and states the false-negative boundary. The finding's latency point
is the sharpest part: the hook process starts on **every** Bash call, and the
documented default command-hook timeout is **600 seconds** — verified — which is
emphatically not a harmless failure direction. Revision 1 sets a short explicit
timeout and a no-match latency budget.

**[X4] accept, and this is the finding I am most glad to have received.** The
proposal cites `a81f9fa7` and then contradicts it. The recorded ruling is that
verification is **not delegated** — the spawner verifies once after the join, and
the leaf never needs the mapping. Turning an intercepted delegated full run into
a *guided delegated scoped run* preserves the multiplier in smaller form, which
is the opposite of the ruling, and I did not notice because I was thinking about
the command rather than about who runs it.

Revision 1 makes the hook **role-aware**, which the documentation confirms is
possible: hook input carries `agent_id` and `agent_type`. A subagent's full-suite
attempt is told to **return verification to the spawner** and is offered no
scoped route at all; only the top-level owner is offered `tools/verify.py`. This
does not supersede the ruling — it enforces it at the one place it is observable.

**[X5] accept.** Straightforwardly correct, and my "deliberate test of the fence"
framing was wrong on the fence's own terms. `AGENTS.md` refuses bounded mode for
*"work under a release or security ceremony"*, and this proposal declares a
Security Review owed, so it is such work. **Boundary B is `full`**, and its
command carries the deliberate override so the new hook cannot block the one
broad run the lifecycle requires.

**[X6] accept, both halves.** "Recorded" is withdrawn — this proposal writes no
durable record of an override, and a vendor transcript is not Cairn's
git-committed evidence channel. And the two wrappers are now distinguished:
Cairn's own root `CLAUDE.md` may name the hook; `templates/core/VENDOR.md` stays
a vendor-neutral placeholder unless the bootstrap gains an installation
mechanism, which this proposal does not add.

## Revision 1

The complete current contract, self-contained. Supersedes the opened proposal in
full; earlier sections stand as immutable history.

### Assurance path, restated

**high-assurance**, and for a stronger reason than the opened version gave. This
adds a **full-user-permission executable trust root** that runs before every
`Bash` tool call, inside subagents as well as the main session, ahead of the
permission system. That is the authority being added; the allow/deny return value
is merely its interface.

### Scope

Put the prompt at the point of cost, and make the spawner's verification
obligation enforceable where it is observable.

**In scope**: a tracked `.claude/settings.json`; one hook script; `tools/verify.py`;
a closed versioned Boundary A block in both plan templates; one vendor-neutral
sentence in `AGENTS.md` and its twin; a naming entry in Cairn's root `CLAUDE.md`;
a new high-risk-surface entry in `AGENTS.md`.

**Excluded**: any change to the canonical Boundary B command; any bootstrap
installation mechanism for the hook; any edit to `templates/core/VENDOR.md`
beyond leaving it a placeholder; any gate-frozen file; any doctrine *rule*.

### Part 1 — the hook, as a registered trust root

**Registration first.** `AGENTS.md` > *High-risk surfaces* gains
`.claude/settings.json` and `.claude/hooks/**` as an executable trust root, on
the same footing as the local interpreter binding and the portable-sweep runner.
The consequence is automatic: any future change to either takes a Security
Review without anyone having to notice it should.

**The bound settings form** — all of these are contract, not convention:

* project-root **absolute path** to the script;
* **shell-free exec form** (`args: []`), so no shell ever parses the invocation;
* the script is a **regular file** (not a symlink), checked at review time;
* a **short explicit timeout** — single-digit seconds. The documented default is
  **600s**, and a hook that hangs would stall every `Bash` call for ten minutes;
* **accepted interpreter provenance**, stated;
* **no subprocess and no network** in the reviewed script, and its bytes are
  reviewed together with the settings file, since either alone is meaningless.

**Behaviour, role-aware.** On a matched unnarrowed full-suite command:

* **top-level session** — refuse once, print the plan's Boundary A block if one
  is declared, print the concentration figures, and name the override;
* **subagent** (`agent_id` / `agent_type` present) — refuse once and say
  **verification returns to the spawner**. No scoped route is offered, because
  offering one would preserve the multiplier the routing decision removed.

`CAIRN_FULL_SUITE=1` passes through silently, recognized **only** as an actual
leading environment assignment.

### Part 2 — a closed Boundary A block, then a reader for it

**The block, defined here because nothing today provides one.** Both plan
templates gain a fenced, versioned block:

```
schema: cairn-boundary-a/1
pytest:
  - <path under bootstrap/tests/, optionally ::node>
gates:
  - <identifier from a closed set>
```

**Refusal rules, all fail-closed**: more than one block in an artifact refuses
(two cannot both be current under append-only revision); an unknown key refuses;
an unknown gate identifier refuses; a pytest entry that does not resolve inside
`bootstrap/tests/`, or that escapes by traversal or symlink, refuses; an
archived or non-active plan refuses; an **absent block refuses** rather than
being guessed.

**Gate identifiers map in code to fixed argv.** No shell text is ever taken from
Markdown and executed — the Markdown supplies a *key*, the code supplies the
command, exactly as the measurement registry already does for `verify_counts`.

**`tools/verify.py --plan <stem>`** runs the pytest entries and the mapped
gates, and **prints anything the block does not cover as still owed**. It never
claims to have run "the Boundary A mapping"; it states what it ran and what
remains.

### Part 3 — prose, correctly split

* `AGENTS.md` and its shipped twin: one vendor-neutral sentence that a full-suite
  invocation is expected to be a deliberate act and a project **may** enforce
  that at its harness. Permission, not obligation — the rate-limit gate is not
  engaged.
* Cairn's **root `CLAUDE.md`** (self-host wrapper) names the hook.
* **`templates/core/VENDOR.md` is not touched** — it stays a vendor-neutral
  placeholder, because this proposal ships no installation mechanism for an
  adopter.

### Rationale

**Interception is still the only remedy whose coverage does not depend on
memory**, and the role-aware form is what makes it consistent with the routing
decision rather than a quiet reversal of it.

**But the cost is now stated at its real size.** This is not a speed bump with
incidental permissions; it is an executable trust root that the repository
supplies and the harness runs with the user's full authority, before the
permission system, inside every subagent. That is worth a Security Review on
every future change, which is exactly what registering it buys.

### Failure directions

The hook **fails open**: a malformed config, a missing script, a raising hook, an
unknown token, or a shell operator all leave the command to run as it does today.
The cost of a missed prompt is one full suite; the cost of a false refusal is
blocked work, and a mechanism that blocks work gets removed.

`tools/verify.py` **fails closed**: it refuses rather than inventing a scope,
because a wrong scope is a check that passes without testing.

### Evidence / verification plan

| invariant | falsifier |
|---|---|
| A narrowed invocation is never intercepted | table-driven over path, node, `-k`, `-m`, `--deselect`, `--ignore`, `--lf`, `--ff`, option-value forms |
| An unknown token or shell operator passes open | feed compound commands, env prefixes, alternate interpreter spellings; assert pass-through |
| The override is recognized only as a leading env assignment | assert a trailing or quoted occurrence does **not** pass through |
| A subagent is told to return verification, not offered a scope | synthesize hook input with `agent_id`/`agent_type`; assert the message and the absence of a scoped route |
| Malformed hook input never blocks | malformed JSON, missing fields, empty stdin — assert pass-through |
| No-match latency stays inside budget | measure the no-match path; assert the stated bound |
| The block's refusal rules | duplicate block, unknown key, unknown gate id, traversal, symlink, archived plan, absent block — each refuses |
| Gates run fixed argv | assert no Markdown-derived string reaches a command |

**Boundary B mode: `full`** — this is work under a security ceremony, on which
the fence refuses bounded mode. Its command carries `CAIRN_FULL_SUITE=1` so the
new hook cannot block the one broad run the lifecycle requires.

### Security preflight — rewritten around the actual authority

**S1 — Who supplied it?** The **repository** supplies the hook script and the
settings that point at it, and the **harness executes them with the user's full
permissions**. That is the trust boundary, and it is not the command string. The
command string is matched, never executed and never interpolated. `tools/verify.py`
reads a repository-controlled block, but takes only *keys* from it: pytest paths
are containment-checked, and gate identifiers select code-controlled argv.

**S2 — Can it fail?** Each invariant names its falsifier. The load-bearing one:
deleting the narrowing check must make a scoped command intercepted, and that
mutation must go red.

**S3 — What fires it, over what?** The harness fires the hook on **every** `Bash`
tool call, in the main session and in every subagent, before the permission
system. That breadth is the reason for the latency budget and the short timeout.
**Cairn has no CI.**

**S4 — Which way does it break?** The hook toward *less* authority on every error
path. `tools/verify.py` toward *fewer claims*. The asymmetry is deliberate and
opposite, because their costs of being wrong are opposite.

**S5 — Who still wins?** The attacker who can write `.claude/hooks/**` or
`.claude/settings.json` in a clone **wins completely**: the hook runs with full
user permissions before any suite, so it can modify tests, fixtures or
configuration and then allow the command, making a compromised tree report
success. **This is a genuine new capability, not a rephrasing of an existing
one**, and the opened proposal's claim to the contrary is withdrawn. It is
contained only by the same trust that already governs executing this
repository's own code, plus review of the two artifacts together and the
registration that forces that review. The class is closed **by enumeration**,
not by construction — the honest answer, and the reason the registration in
Part 1 is not optional.

### Known omissions

* **False negatives are real and bounded by the grammar**: any unusual spelling
  passes open, deliberately. "100% coverage" is retracted.
* **No durable record of an override** — the pass-through is silent, and this
  proposal adds no evidence channel. The word "recorded" is withdrawn.
* **Adopters get nothing installable** — no bootstrap mechanism ships.
* **Non-shell pytest invocations** (`pytest.main()` in-process) are not
  intercepted.
* **Whether the prompt changes behaviour is unmeasured** until the run-frequency
  ledger exists.

### Withdrawn / superseded commitments

* **"It cannot make a failing suite look passing"** — withdrawn (X1), false. A
  full-permission hook running before the suite can modify what the suite reads.
* **"100% coverage of the failure by construction"** — withdrawn (X3); holds only
  for enumerated canonical forms.
* **Offering a subagent a scoped route** — withdrawn (X4); it preserved the
  multiplier the routing decision removed. Replaced by role-aware behaviour that
  returns verification to the spawner.
* **`Boundary B mode: bounded`** — withdrawn (X5); the fence refuses bounded mode
  for work under a security ceremony, which this is.
* **"a deliberate, *recorded* choice"** — withdrawn (X6); nothing records it.
* **`tools/verify.py` reading "the declared Boundary A file list"** — withdrawn
  (X2); no such field existed. Replaced by a closed versioned block defined here,
  with fail-closed refusal rules and code-controlled gate argv.
* **Naming the hook in the shipped `templates/core/VENDOR.md`** — withdrawn (X6);
  it stays a vendor-neutral placeholder.

## Review -- Codex (External) -- 2026-08-19

**Model**: OpenAI GPT-5 (Codex)
**Tier**: External
**Findings**: raised

Reviewed commit: `c6ef10a8814fcb7f8cafd38cb5e1f10b9b743189`
Target: Revision 1, limited to X1-X6 and their replacement contract
Prior findings: X1-X6 in the Codex External review committed at `12293dc73f85357d9b67fb86da698247be65580c`
Assurance path: high-assurance

**Plan readiness**: DISTINCT REVIEW REQUIRED

**Verdict: REVISE.** X1, X4, X5, and X6 are substantively closed: the hook is
now treated as full-permission code, leaf verification returns to the spawner,
Boundary B is full, and the wrapper/evidence claims are honest. The newest
surface -- the machine-readable mapping -- still lacks a plan-selection binding
and cannot survive append-only revision as written. The role predicate also uses
one field too many. These are local contract fixes, not a challenge to the
three-part design.

### Findings

**[Y1 - BLOCKING, X2 continuation] The hook has no input that identifies “the
active plan.”** A `PreToolUse` record supplies session, cwd, role, tool, and
command fields; it does not supply a Cairn plan stem. This repository can have
more than one active plan, as the current board demonstrates. Work-intent claims
also do not bind a Claude session id to a plan in a way this hook can safely
derive. The top-level behavior therefore cannot “print the plan's Boundary A
block if one is declared,” and concentration data has the same unstated source
problem.

Bind the context explicitly or narrow the message. A sufficient contract is a
validated `CAIRN_PLAN=<stem>` session value owned by the spawner, with absent,
ambiguous, inactive, traversal-shaped, or mismatched values producing generic
guidance rather than a guessed mapping. Alternatively, have the hook print only
`tools/verify.py --plan <stem>` with a placeholder and let the owner supply the
stem. If concentration figures remain in the message, name their exact file,
schema, freshness rule, and absent/malformed disposition; the current
gitignored `dev/measurement/suite-cost.md` is not named in Revision 1.

**[Y2 - BLOCKING, X2 continuation] The proposed block conflicts with both
append-only revision and the shipped template's audience.** “More than one block
in an artifact refuses” means a reviewed plan can never append a corrected
mapping: the old block remains by design, so the second complete current block
permanently bricks the reader. The displayed syntax is YAML-like but no parser
or fence identity is specified under Cairn's standard-library-only contract.

Define append-only selection semantics, such as a uniquely identified complete
block in each revision with the last valid revision superseding prior blocks;
duplicate blocks **within that revision** may refuse. Use a structured stdlib
format with an exact fence marker and closed schema rather than an ad hoc YAML
subset. Then resolve the adopter mismatch: `templates/core/dev/plans/_template.md`
cannot require entries under Cairn-specific `bootstrap/tests/`, and this proposal
ships no adopter router or gate registry to consume the block. If the block stays
in both templates, make its admitted test roots and fixed gate registry a
project-configured contract and ship the consumer. A self-host-only v1 must say
so explicitly and must not place an inert Cairn-specific block in the adopter
template.

The “still owed” rendering also needs a source. The reader cannot discover prose
obligations omitted from its block. Add an explicit non-executed `manual` /
`still_owed` field, or print the honest generic statement that obligations
outside the block require reading the plan.

**[Y3 - BLOCKING, X4 continuation] `agent_type` does not distinguish a
subagent.** The official common-input schema says `agent_id` is present **only**
inside a subagent call, while `agent_type` is also present for a top-level
session launched with `--agent`. Revision 1 describes a subagent as
“`agent_id` / `agent_type` present,” which can route a top-level owner away from
its own verification. Use presence of a valid `agent_id` as the role predicate;
record `agent_type` only as descriptive context. Test a plain top-level call, a
top-level `--agent` call (`agent_type` only), and a real subagent shape
(`agent_id` plus `agent_type`). Primary schema, checked 2026-08-19:
https://code.claude.com/docs/en/hooks#common-input-fields

**[Y4 - SUBSTANTIVE, X1/X3 continuation] The claimed bounds still have no
values or exact settings artifact.** “Single-digit seconds,” “inside budget,”
“enumerated canonical forms,” and “accepted interpreter provenance” leave the
implementation to choose the security/performance contract after review.
Include the exact `.claude/settings.json` hook object, timeout, executable and
arguments; name the interpreter/shebang trust decision; enumerate the blocked
canonical forms; and set a numeric no-match latency criterion with measurement
conditions. The plan may tune implementation details, but the review needs to
know which commands are stopped and how long every unrelated Bash call may be
delayed.

Also replace “refuse once” unless state is deliberately introduced. A fresh
hook process has no specified memory; the simpler and safer behavior is to
refuse every matching invocation that lacks the explicit override.

### Closed findings

X1 is closed by the rewritten S1/S5, joint settings/script review, and high-risk
registration. X4 is closed in policy: subagents return verification to the
spawner; Y3 corrects only the discriminator. X5 is closed by full Boundary B
with the override. X6 is closed by withdrawing “recorded” and keeping the
shipped vendor wrapper untouched. X3's fail-open small-grammar direction is
correct; Y4 asks for the actual admitted forms and bounds.

### Coverage

**Covered:** Revision 1 in full; official Claude Code common hook fields,
subagent propagation, matcher, timeout, exit, and permission behavior current on
2026-08-19; the live lifecycle board; both plan templates; active plans' actual
append-only amendment shapes; current `dev/measurement/` inputs; and the root
and shipped vendor wrappers.

**Not covered:** no hook, settings file, mapping parser, or router exists, so I
did not run a live harness invocation, measure latency, mutate a mapping block,
or execute the Cairn suite. The separately owed implementation Security Review
remains undischarged by this proposal review.

**Next round:** limited to Y1-Y4. Bind or remove automatic plan selection,
make the structured block append-only-safe and audience-correct, use `agent_id`
as the subagent predicate, and state the exact settings/grammar/time bounds.

## Response -- Claude -- 2026-08-19 (round 2)

**Model**: claude-opus-5 (Claude Opus 5)

Reviewed commit: `c6ef10a`. All four findings verified against primary sources.
Then, as with the sibling proposal, I put the replacement draft through an
adversarial pre-review before submitting it — four independent lenses with
probes. **They converged, unanimously and with executed evidence, on a
conclusion the draft did not reach: Part 2 is not a reviewable contract and
should be cut rather than repaired.** I have cut it.

**[Y1] accept, taking the second exit.** Verified: the common input is
`session_id`, `prompt_id`, `transcript_path`, `cwd`, `permission_mode`, `effort`,
`hook_event_name` plus the tool fields — **no plan, and none is derivable**. My
draft answered this with a spawner-owned `CAIRN_PLAN`, and the pre-review showed
that **names a channel nothing can write**: a command hook inherits the *harness
process* environment, not the environment of the tool call it inspects, and this
harness's own contract states shell state does not persist between `Bash` calls
(measured: `export` in one call, unset in the next). The binding is dropped
entirely. Also correct that the concentration figures had no valid source —
`dev/measurement/suite-cost.md` is gitignored at `.gitignore:18` and absent from
any fresh clone. Removed.

**[Y2] accept by cutting Part 2, not by repairing it.** Every one of my Revision 1
answers turned out to be false under probe:

* **The format claim.** All four lenses independently fed my own example block to
  `tools/lifecycle.py::_parse_fenced_records` — the parser I cited as *proving*
  the format — and all four got a refusal at line 4. That grammar admits only flat
  `key: value`; the `- item` list half, which carries every executable path, is
  **novel and was presented as proven**.
* **It cannot be self-host-only.** `tools/lifecycle.py` and
  `templates/skills/_lib/lifecycle.py` are byte-identical under a verbatim sync
  (md5 `e58486dc8eec224e487c739b400f8c89`), so extending that parser ships to every
  adopter — contradicting the draft's own bound.
* **Zero producers on day one.** v1 touched only the plan template, and both live
  plans map Boundary A **per chunk** — one chunk's reviewed answer *is* the full
  suite — which a flat schema has no dimension to hold. `tools/verify.py` would
  refuse for every plan that exists, while the hook pointed at it.
* **"Fails closed" is false twice, silently.** A four-backtick quotation of a
  block — the ordinary way a reviewer cites one — swallows the following real
  block, and the reader then runs the *superseded* mapping with no diagnostic.
  And `PYTEST_ADDOPTS='-k "not two"'` turns a genuinely failing run into exit 0
  with byte-identical argv, so fixed argv does not bound what pytest runs.

A reader cited as Boundary A evidence that reports green while running less than
it claims is precisely the silent-tool failure `AGENTS.md` singles out. Repairing
it needs a new grammar, a new parser home, a chunk dimension, environment
sanitisation, and a containment rule — five design decisions no reviewer has
seen. **Cutting it costs no delivered function, because it delivers none.**

**[Y3] accept.** Verified verbatim: `agent_id` is *"Present only when the hook
fires inside a subagent call"*; `agent_type` is *"Present when the session uses
`--agent` **or** the hook fires inside a subagent"*. My predicate would have
routed a top-level `--agent` owner away from its own verification. The predicate
is now a non-empty `agent_id`, and `agent_type` is descriptive only.

**[Y4] accept — and the ask I dropped is the important one.** My Withdrawn ledger
closed Y4 by listing four replacements and **silently omitted its fourth ask, the
enumeration of blocked forms.** Two lenses greped it: the word "enumerat" appeared
twice in my draft, one of them the falsifier row itself, and `pytest` never
appeared as a command to intercept. So the contract's *first invariant* — "blocked
forms are exactly the enumerated canonical ones" — was over a set that did not
exist.

That absence concealed a live contradiction. A 32-command prototype sweep refused
**2 of 32**, and the two were the same command differing in whitespace. Everything
this repository actually documents as a full-suite run passed open: the canonical
Boundary B pair, the `PYTHONDONTWRITEBYTECODE=1`-prefixed forms recorded in a live
plan and in the AST baseline runbook, `cd <repo> && pytest bootstrap/tests`,
`python3.13 -m pytest ...`, and the pinned absolute interpreter. Three tokens I
called "narrowing" — `--lf`, `--ff`, `-k ''`, `-m ''` — each ran the *whole* suite,
making my evidence rows 3 and 4 mutually unsatisfiable. The enumeration is now
written, and matching normalises rather than bails.

**One thing the pre-review cleared, recorded so it is not re-raised:** the
p95 < 50 ms latency criterion is genuinely meetable — three independent 200-run
spawn-inclusive samples gave p95 **23.2 / 26.2 / 27.1 ms**. And the narrowing to
self-host-only is legitimate: Y2 named that exit, and Revision 1 was never
accepted, so no accepted-scope floor is engaged.

## Revision 2

The complete current contract, self-contained. Supersedes Revision 1 in full.

### Assurance path

**high-assurance.** Adds a **full-user-permission executable trust root** that
runs before every `Bash` tool call, inside subagents as well as the main session,
ahead of the permission system.

### Scope — and what v1 does not attempt

**In scope**: a tracked `.claude/settings.json`; one hook script; a vendor-neutral
high-risk-surface entry in `AGENTS.md` and its twin; the concrete paths named in
Cairn's root `CLAUDE.md`; one vendor-neutral sentence under *Verification
boundaries*; one new test file.

**Part 2 is withdrawn from v1.** The machine-readable Boundary A block and
`tools/verify.py` are named as a successor's work, with the five design decisions
they require stated above. **Nothing is placed in either plan template.**

**Also excluded**: any change to the canonical Boundary B command text; any
bootstrap installation mechanism; any gate-frozen file; any doctrine *rule*;
`templates/core/VENDOR.md`.

### Part 1 — the hook, as a registered trust root

**Registration first, split by what each file is for.** `AGENTS.md` >
*High-risk surfaces* gains the surface **without any vendor path** — naming
`.claude/` there would put a vendor token into vendor-neutral doctrine, which is
itself a named high-risk surface and is checked by
`scripts/quality_gate.py --sub neutrality`:

> **The harness command-hook configuration** — whatever file the project's agent
> tool reads to register a command hook, and every script such a hook points at.
> These execute with the user's full permissions, before the tool's permission
> system, and inside subagents; the concrete paths are named in that tool's own
> wrapper. Changes to either take a Security Review.

Cairn's root `CLAUDE.md` names the paths.

**The exact settings object**, reviewed as bytes together with the script:

```json
{"hooks": {"PreToolUse": [{"matcher": "Bash",
  "hooks": [{"type": "command",
             "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/full_suite_guard.py",
             "args": [],
             "timeout": 5}]}]}}
```

Each clause is contract. The path uses the documented **`${CLAUDE_PROJECT_DIR}`
placeholder**, never an absolute one: a machine path in a tracked file is inert in
every other clone, a failed hook spawn is non-blocking, and the only signal is a
transcript notice — silent inertness is the wrong failure direction for a
security-registered artifact. **Shell-free exec form** (`args: []`). **Timeout 5
seconds** — the documented default is **600**, which would stall every `Bash` call
for ten minutes. The script is a **regular file**, not a symlink, with the
executable bit, and its `#!` line is `#!/usr/bin/env python3` — pinning no machine
interpreter, and stdlib-only. **No subprocess and no network.**

**The blocked set, literally and exhaustively.** A command is refused only if,
after stripping leading environment assignments, its argv is exactly one of:

```
pytest bootstrap/tests
python -m pytest bootstrap/tests
python3 -m pytest bootstrap/tests
python3.13 -m pytest bootstrap/tests
<absolute-interpreter-path> -m pytest bootstrap/tests
```

each optionally with a trailing `/` on the target, a leading `./`, or the
repository-absolute spelling of the target, and each optionally carrying any
subset of the known non-narrowing options `--quality-gate-shuffle-seed=<int>`,
`-q`, `-v`, `-x`, `--durations=<int>`, `--no-header`, `--no-summary`,
`-p <plugin-spec>`, `--tb=<style>`. **Any other token refuses to match and the
command passes open.** This list is the contract; adding to it is a change to a
registered trust root.

**Matching normalises rather than bails**: leading environment assignments are
stripped before comparison, so `PYTHONDONTWRITEBYTECODE=1 python -m pytest
bootstrap/tests` matches. `--lf`, `--ff`, `-k` and `-m` are **not** treated as
narrowing — measured, each ran a whole throwaway suite — so they are simply not in
the option set above and their presence passes open.

**The match is conditioned on this working tree.** The repository root is the
directory containing the hook script, resolved from the script's own path, never
from the payload's `cwd`. If the payload's `cwd` does not resolve inside that
tree, the hook passes open.

**Role predicate — `agent_id`, and only `agent_id`.**

* **subagent** (`agent_id` present and non-empty) — refuse, and say
  **verification returns to the spawner**.
* **top-level** — refuse, and name the override.

**Refuse *every* matching invocation lacking the override.** "Refuse once" implied
state a freshly-spawned process does not have.

**The override is read from the command string's leading assignments, never from
any process environment.** A command that otherwise matches but carries the token
trailing, quoted, or `env`-mediated — `pytest bootstrap/tests CAIRN_FULL_SUITE=1`,
`env CAIRN_FULL_SUITE=1 pytest bootstrap/tests` — is **still refused**, and the
refusal names the leading-assignment form. This is the one place the grammar does
not pass open on an unrecognised shape, and it is deliberate: the override must be
unambiguous.

### Part 2 — one vendor-neutral sentence

`AGENTS.md` and its shipped twin gain, under *Verification boundaries*: a
full-suite invocation is expected to be a deliberate act, and a project **may**
enforce that at its harness. Permission, not obligation — the rate-limit gate is
not engaged. **`templates/core/VENDOR.md` is untouched.**

### Failure directions

The hook **fails open** on every error: malformed settings, missing script,
raising hook, malformed or absent stdin JSON, unknown token, shell operator,
timeout, a `cwd` outside this tree. The cost of a missed prompt is one full suite;
the cost of a false refusal is blocked work, and a mechanism that blocks work gets
removed.

### Evidence

| invariant | falsifier |
|---|---|
| The blocked set is exactly the enumeration | table over every enumerated form, each with and without the option subset, trailing slash, `./`, and absolute target; assert each refused |
| Nothing outside the enumeration is refused | `cd x && …`, `time …`, `bash -c "…"`, heredocs, `--`, `-k`, `-m`, `--lf`, `--ff`, a node id, a single file, an unknown option; assert each passes open |
| Leading env assignments are stripped, not bailed on | `PYTHONDONTWRITEBYTECODE=1 python -m pytest bootstrap/tests` is refused |
| The override is leading-assignment-only | trailing, quoted and `env`-mediated forms are **still refused**; only the leading form passes |
| Role predicate | plain top-level (neither field); top-level `--agent` (`agent_type` only — **must not** be treated as a subagent); subagent (`agent_id` + `agent_type`) |
| Malformed input never blocks | malformed JSON, missing fields, empty stdin |
| Foreign tree | a payload `cwd` outside this tree passes open |
| No-match latency | **spawn the hook as a subprocess exactly as the harness does** — exec by path, one no-match payload on stdin, read to exit — 200 times on an idle host; assert **p95 < 50 ms**; record min, median, p95, max with the interpreter and host. An in-process call does **not** discharge this row: spawn is about three-quarters of the cost. Max is recorded, not asserted (measured maxima 375 ms against p95 23.2 ms) |
| The registration is live and well-formed | a test parses `.claude/settings.json` and asserts exactly one `PreToolUse` entry; `matcher == "Bash"`; `type == "command"`; `args == []`; `timeout == 5`; the `command` begins `${CLAUDE_PROJECT_DIR}/` and, expanded against the repository root, names an existing regular non-symlink file with the executable bit whose `#!` is `#!/usr/bin/env python3`. A typo, a moved script, a dropped key or a re-baked absolute path goes red |

**Boundary B mode: `full`** — work under a security ceremony, on which the fence
refuses bounded mode. Its command carries the override in leading position.

### Security preflight

**S1 — Who supplied it?** The **repository** supplies the hook script and the
settings pointing at it; the **harness executes them with the user's full
permissions**. That is the trust boundary. The command string is matched, never
executed, never interpolated, never shelled.

**S2 — Can it fail?** Every invariant names its falsifier; deleting the
enumeration check must refuse a scoped command and go red.

**S3 — What fires it, over what?** The harness, on **every** `Bash` tool call, in
the main session and every subagent, before the permission system. That breadth is
why the latency criterion and the 5-second timeout are contract. **Cairn has no
CI.**

**S4 — Which way does it break?** Toward *less* authority on every path but one:
the override's leading-assignment rule, which refuses rather than passes on an
ambiguous shape.

**S5 — Who still wins?** An attacker who can write `.claude/settings.json` or the
hook script in a clone **wins completely**: the hook runs with full user
permissions before any suite, so it can modify tests, fixtures or configuration
and then allow the command, making a compromised tree report success. **And
`.claude/**` is outside every frozen glob** (`bootstrap/*.py`,
`bootstrap/tests/**/*.py`, `bootstrap/tests/fixtures/**/*`, `scripts/*.py`,
`templates/modules/**/*.py`), so unlike `bootstrap/tests/conftest.py` these bytes
are **unanchored**: the gate manifest will not notice them changing. That is the
same coverage gap recorded as `dev/PLANNING.md` **[TRU-4]** for a repo-root
`conftest.py`, and this proposal *creates a second instance of it* rather than
closing it. The registration is prose that binds a reader; the Evidence row above
is the only mechanical check, and it verifies shape, not authenticity. Closed **by
enumeration**, not by construction, and the honest disposition is that this
proposal should not land before [TRU-4] has an answer that covers it.

### Known omissions

* **The blocked set is the literal enumeration and nothing else.** Any other
  spelling passes open, deliberately. "100% coverage" stays retracted.
* **`python scripts/quality_gate.py` is not intercepted** — it runs one to N full
  suites by subprocess with no `pytest` token in the command string, so it is
  invisible to a command matcher. This is a real hole in the remedy's coverage of
  the very cost it targets.
* **Worktrees are not covered.** Project settings scope to one project directory;
  a checkout made by `git worktree add` carries no settings file and the hook never
  fires there. This repository currently has eight such worktrees.
* **No durable record of an override** — the pass-through is silent.
* **Adopters get nothing** — v1 is self-host-only by design.
* **Non-shell pytest invocations** (`pytest.main()` in-process) are not
  intercepted.
* **Whether the prompt changes behaviour is unmeasured** until the run-frequency
  ledger exists.

### Withdrawn / superseded commitments

* **Part 2 in its entirety — the Boundary A block and `tools/verify.py`** —
  withdrawn (pre-review, four independent lenses, all executed): the cited parser
  refuses the draft's own example block; that parser is verbatim-synced to the
  shipped copy so it cannot be extended self-host-only; there are zero producers
  on day one; and its fail-closed claim is false in two silent directions.
  Successor work, with its five design decisions named.
* **The `CAIRN_PLAN` plan binding** — withdrawn; a command hook inherits the
  harness process environment, not the tool call's, and shell state does not
  survive a `Bash` call, so nothing can write it.
* **Printing the concentration figures** — withdrawn; the source is gitignored and
  absent from a fresh clone.
* **"`agent_id` / `agent_type` present" as the subagent predicate** — withdrawn
  (Y3); `agent_type` is present for a top-level `--agent` session.
* **"refuse once"** — withdrawn (Y4); a fresh process has no memory.
* **"single-digit seconds" / "inside budget" / "accepted interpreter
  provenance"** — withdrawn (Y4); replaced by the exact settings object, a
  5-second timeout, a **spawn-inclusive** p95 < 50 ms criterion, **the literal
  enumeration of blocked forms**, and `#!/usr/bin/env python3`. Revision 1 closed
  this entry while silently dropping Y4's fourth ask, the enumeration; corrected
  here.
* **An absolute path in the settings object** — withdrawn; inert in every other
  clone. Replaced by `${CLAUDE_PROJECT_DIR}`.
* **Naming `.claude/` in `AGENTS.md`** — withdrawn; it would put a vendor token in
  vendor-neutral doctrine, which the neutrality sub-gate checks. Split: the
  surface is described vendor-neutrally in `AGENTS.md`, the paths in `CLAUDE.md`.
* **Treating `--lf` / `--ff` / `-k` / `-m` as narrowing** — withdrawn; measured,
  each ran a whole suite.

## Maintainer-directed contract revision -- 2026-08-19

**Model**: claude-opus-5 (Claude Opus 5)

The Maintainer directed that the frozen-set gap be brought into this proposal's
scope:

> It sounds like TRU-4 needs to be brought into the scope of this proposal,
> correct?

**Accepted in the narrow, additive form; declined in the broad form.** The
reasoning is recorded because the boundary is the point.

**What comes in.** Revision 2 shipped an executable trust root that the gate
cannot see, and said so in S5 while leaving the consequence to a future
proposal. That is not a defensible split: a proposal that *creates* an
unanchored executable surface owns anchoring it. The frozen-set extension is
therefore part of this contract, not a precondition on someone else.

**What stays out.** `[TRU-4]` is a cluster, and the rest of it is about surfaces
this proposal does not create: the repo-root `conftest.py` gap (`cf8bed7`), the
trust-apparatus naming gap (`2ca02e8`), and the end-gate decision on whether the
engine packages join `frozen_files`. Folding those in would subordinate a general
question about the gate's authority to a specific convenience feature, and would
invite the frozen-set decision to be made *in service of* landing this hook.

**The direction of the change is what makes this safe.** The trust-apparatus row
records an ordering constraint — *"enumerate the trust-apparatus files as named
trust-ceremony surfaces first, land that, and only then reconsider the glob
reading — never the reverse"* — because a **narrowing** decided under feature
pressure opens the fence. This is an **addition**: it widens coverage, so the
hazard that constraint guards against does not arise. Adding is safe in a
direction narrowing is not, and the two must not be treated as one move.

### The added scope

`bootstrap/tests/_gate_manifest.py::_frozen_files` gains **two precisely scoped
globs**, and the precision is contract:

```
".claude/*.json", ".claude/hooks/**/*.py"
```

**Never `.claude/**`.** Measured 2026-08-19: `.claude/**/*` matches **565 files**
in this working tree, because `.claude/worktrees/` holds scratch worktrees each
containing a full copy of the repository. Freezing those would make the gate
report drift on every scratch checkout and would put another session's working
copy inside this repository's trust root. The two scoped globs match **zero**
files today and will match exactly the two artifacts this proposal creates.

**Consequences, stated rather than discovered:**

* `.claude/settings.json` and the hook script become **FROZEN-NEW** on the commit
  that adds them, and are byte-hashed thereafter. Editing either then requires a
  re-anchor — which is the intended cost, and the mechanism that makes the
  Security-Review registration bite rather than merely advise.
* `.claude/worktrees/` must be **gitignored** in the same change, so scratch
  worktrees can never enter the tracked tree and therefore can never enter the
  frozen set by a later glob widening.
* `.claude/skills` is a symlink to a directory; `_frozen_files` skips it, since
  `Path.is_file()` is false for it. A symlink to a *file* would be followed, so
  the hook script is required above to be a **regular file**, which the settings
  Evidence row already asserts.
* Editing `_gate_manifest.py` is itself a gate-frozen change, so this proposal now
  carries **two** frozen-file edits into the re-anchor it already owed.

### What this closes, and what it does not

It closes the S5 hole this proposal opened: the hook configuration and script are
anchored on the day they land, so the gate notices them changing. **It does not
close `[TRU-4]`.** The repo-root `conftest.py` still escapes every glob, the
sixteen trust-apparatus files are still protected by a blanket glob rather than by
being named, and the engine-package end-gate decision is still open. Revision 2's
disposition — *"this proposal should not land before [TRU-4] has an answer that
covers it"* — is **withdrawn and replaced**: this proposal now covers its own
instance, and the remaining cluster is no longer a blocker on it.

### Added evidence

| invariant | falsifier |
|---|---|
| The hook surface is frozen | after landing, assert `_frozen_files()` contains `.claude/settings.json` and the hook script path, and that mutating either byte makes the gate report `FROZEN-MODIFIED` |
| The glob cannot swallow a worktree | create a scratch path under `.claude/worktrees/`; assert `_frozen_files()` does not grow. Measured: the naive `.claude/**` matches 565 files in this tree, so this row is the guard against re-widening |
| A symlinked hook script is refused | replace the script with a symlink to a regular file; assert the settings row goes red |

### Withdrawn / superseded commitments

* **"this proposal should not land before `[TRU-4]` has an answer that covers
  it"** — withdrawn; this contract now anchors the surface it creates, so the
  dependency is discharged inside the proposal rather than deferred.
* **`.claude/**` as a candidate glob** — never proposed, and recorded as refused
  with its measurement so a later reader does not reach for it: it matches 565
  files here.
* **Revision 2's scope line "any gate-frozen file" under *Also excluded*** —
  withdrawn; this contract now edits `bootstrap/tests/_gate_manifest.py`, and the
  re-anchor it already owed absorbs the second frozen-file edit.

### What `.claude/` is, and what tracking one file there changes

Raised by the Maintainer while this amendment was being written:

> `.claude` is entirely outside of the repo, right? That's just our work here,
> essentially scratchpad and local install info

**Correct as to the current state, and verified**: nothing under `.claude/` is
tracked (`git ls-files .claude/` is empty), the directory is *not* gitignored — it
has shown as `??` in `git status` all along — and both its contents are local
artifacts rather than authored ones. `.claude/skills` is a symlink that the
`session-start` routine **self-heals** (`tools/lifecycle.py`), so it is generated
by the tooling, not committed; `.claude/worktrees/` is scratch.

**But the harness's own contract splits that directory**, and this is the fact the
proposal turns on. Checked 2026-08-19: `.claude/settings.json` is documented as
*"checked into source control and shared with your team"*, while
`.claude/settings.local.json` is *"not checked in, useful for personal preferences
and experimentation"* and is auto-excluded. So `.claude/` is designed to be
**mixed** — one shared file plus local material — and tracking `settings.json`
is its intended use, not a violation of it.

**The consequence, stated because it is a real change in the directory's
character**: this proposal makes `settings.json` the **first tracked artifact**
under `.claude/` in this repository. That is not incidental, and three things
follow.

* **Tracking is a precondition of freezing, not a separate choice.**
  `_frozen_files` globs the **working tree**, not the index. An untracked
  `settings.json` would be hashed into a committed manifest and then be *absent*
  from every fresh clone, so the gate would report it missing on a clean checkout.
  Anchoring the hook therefore *requires* committing it; the two decisions are one
  decision, and Revision 2's registration story does not work without it.
* **`.claude/worktrees/` must be gitignored in the same change.** Once one file
  under `.claude/` is tracked, the directory stops being uniformly ignorable by
  habit, and scratch worktrees — 565 files in this tree today — become one careless
  `git add .claude/` away from the repository.
* **`.claude/skills` must stay untracked**, since the routine regenerates it. The
  two scoped globs (`.claude/*.json`, `.claude/hooks/**/*.py`) do not match it,
  and `_frozen_files` skips it regardless because `Path.is_file()` is false for a
  symlink to a directory.

**If the Maintainer prefers `.claude/` to remain wholly local**, that is a
coherent position and it **kills Part 1 as designed** rather than shrinking it: a
hook that is not in the repository cannot be reviewed as bytes, cannot be frozen,
cannot be shared with another clone or another agent, and would be per-machine
local configuration rather than a Cairn artifact — at which point it is a personal
workflow tool and not proposal-worthy. That is a decision for the Decision, and it
is recorded here as a live fork rather than assumed away.

## Maintainer-directed contract revision -- 2026-08-19 (mechanism)

**Model**: claude-opus-5 (Claude Opus 5)

The Maintainer asked the question that unmade the design:

> Why would the hook be in .claude? What if I am using other agents?

> Good, in-suite guard it is

> Do not supersede the proposal. Revise, then review

**The honest answer to the first question is that `.claude/` was never a reason,
only a location** — it is where one vendor reads hooks. Cairn's stated identity is
*"vendor-neutral and model-agnostic by construction: the coordination channel is
git-committed files, so a project can mix or swap AI vendors without changing the
method."* A harness hook is exactly not that. This project already runs mixed —
the External reviews on this very proposal come from a different agent type — so a
control that governs one harness gives **partial coverage that reads as
complete**, which is the silent-tool failure this proposal has twice been revised
for.

And every hard problem of the last two rounds was downstream of that location: the
unanchored trust root, the `.claude/` tracking fork, the 32-command grammar, the
missing enumeration, and the `PYTEST_ADDOPTS` blindness. None of them were serving
the goal.

**The mechanism moves into the suite.** Measured on the canonical interpreter:

| invocation | in-suite guard | the `.claude/` hook |
|---|---|---|
| bare full run | **refused** | refused |
| `cd <repo> && pytest bootstrap/tests` | **refused** | passed open |
| `PYTHONDONTWRITEBYTECODE=1 python -m pytest …` | **refused** | passed open |
| the canonical Boundary B pair | **refused** | passed open |
| `PYTEST_ADDOPTS='-k n1'` (genuinely narrowed) | allowed — 1 passed, 4 deselected | would have called it `full` |
| explicit `-k n1` | allowed | allowed |
| override set | allowed | allowed |

It counts **what was actually collected**, not what the command said — so there is
no grammar, no enumeration, no interpreter spellings, no shell operators, and the
environment-variable route that structurally defeated the hook is handled
correctly rather than misclassified.

## Revision 3

The complete current contract, self-contained. Supersedes Revision 2 and the
2026-08-19 scope amendment in full.

### Assurance path

**high-assurance**, for a different reason than before. This adds **no executable
trust root and no new file**: it edits `bootstrap/tests/conftest.py`, which is
gate-frozen and already carries the release-gate outcome rule. The trigger is that
the change can **refuse to run the suite**, and it lives in the one file that can
already decide a session's exit status. A Security Review is owed on that.

### Scope

**In**: a guard in `bootstrap/tests/conftest.py`; a child-environment change in
`scripts/quality_gate.py`; one vendor-neutral sentence under *Verification
boundaries* in `AGENTS.md` and its twin; one new test file.

**Withdrawn entirely, and not deferred**: `.claude/settings.json`, the hook
script, the `${CLAUDE_PROJECT_DIR}` settings object, the blocked-form enumeration,
the `agent_id` role predicate, the `_gate_manifest.py` glob extension, the
`[TRU-4]` scope folding, `tools/verify.py`, the Boundary A block, and the entry in
Cairn's root `CLAUDE.md`. **`templates/core/VENDOR.md` remains untouched.**

### The guard

In `bootstrap/tests/conftest.py`:

```python
@pytest.hookimpl(trylast=True)
def pytest_collection_modifyitems(config, items): ...
```

**`trylast=True` is contract, not style.** Measured: without it the guard runs
*before* pytest's own keyword filtering and sees the unfiltered item list, so a
legitimately narrowed run (`-k`) is refused — the false positive every prior
revision forbade. With it, the guard sees the final list.

**The discriminator is distinct test files, not test count.** Measured in this
repository: a full collection spans **115** files; the six-file scoped mapping this
project actually used spans **6** — and that mapping ran roughly **1,140** tests.
So counts barely separate a scoped run from a full one (1,140 against 4,468) while
file span separates them by nearly twenty times.

**Threshold: more than 40 distinct test files.** That is 6.7× the observed scoped
mapping and 2.9× below a full collection, so both margins are wide. A run touching
more than forty files is a third of the suite and is treated as full, which is the
intended reading rather than a concession.

**Refusal is `pytest.UsageError`**, which exits **4** — measured, against 0 when
allowed. It is loud, immediate, and names the override.

**Exemptions, each with its reason:**

* `CAIRN_FULL_SUITE=1` — the deliberate override.
* **Release mode** — using the module's existing strict-equality predicate, never
  a presence test. A release ceremony's behaviour must not change because this
  landed.
* **`--collect-only`** — nothing executes, so there is nothing to spend. This also
  keeps `bootstrap/tests/_gate_manifest.py`'s own collector working, which invokes
  pytest with `--collect-only` to build the manifest.

### The interaction this creates, stated rather than discovered

`scripts/quality_gate.py` spawns a **full pytest run per seed** for the
order-independence sub-gate. Each of those children would be refused by this
guard. The script must therefore set the override in the child environment, and
that is part of this change — `scripts/*.py` is gate-frozen, so it joins the same
re-anchor rather than adding another.

This is a **feature of the design, not a workaround**: the second full suite that
sub-gate spends has been invisible, and a guard that forces it to be declared in
code is the first thing that makes it countable.

### The cost of the swap, stated plainly

**The role distinction is lost.** The hook could read `agent_id` and tell a
subagent to return verification to the spawner. A conftest runs in-process and has
no such signal. The guard's message can **state** the rule — *verification is not
delegated; if you are a subagent, return it to the spawner* — but it cannot
enforce it differentially, and a subagent that sets the override is
indistinguishable from an owner who does. Enforcement of the routing decision
therefore remains what it was before this proposal: a rule the spawner follows.
That is a real reduction against Revision 2, and it is the price of vendor
neutrality.

**It is a refusal, not a speed bump.** Earlier revisions leaned on "blocks
nothing". This blocks, including for a human, until one token is set.

### Interaction with the sibling proposal

`2026-08-19-claude-suite-run-diagnostics` also edits `bootstrap/tests/conftest.py`,
adding five hooks. This adds a sixth. They do not conflict semantically — one
measures, one refuses — but **whichever lands second inherits the other's
conftest and must re-verify against it**, and both are absorbed by the single
re-anchor already owed. Neither depends on the other.

### Evidence

| invariant | falsifier |
|---|---|
| A full collection is refused regardless of spelling | bare run; `cd <repo> && …`; env-prefixed; absolute interpreter; `python3.13 -m pytest`; the canonical Boundary B argv — assert exit 4 in every case |
| A narrowed run is never refused | `-k`, `-m`, a single file, a node id, a six-file mapping, **and `PYTEST_ADDOPTS='-k …'`** — assert each runs |
| `trylast` is load-bearing | remove `trylast=True`; assert a `-k` run becomes refused. This mutation must go red |
| The override allows | `CAIRN_FULL_SUITE=1`; assert exit 0 and full execution |
| Release mode is exempt | the module's existing predicate at its one recognized value; assert the suite runs and the release rule is unaffected; assert `…=0` does **not** exempt |
| `--collect-only` is exempt | assert the gate manifest's own collector still builds |
| The quality gate still runs | `--sub order-independence` with a seed; assert the child is not refused |
| The threshold discriminates | a 41-file selection is refused; a 40-file selection runs |

**Boundary B mode: `full`** — a gate-frozen file under a re-anchor ceremony, and
work under a security ceremony. Its command carries the override.

### Security preflight

**S1 — Who supplied it?** The guard reads the final collected item list, the
process environment (two variables), and pytest's own config. Nothing is executed;
no string from any document or command line is interpreted.

**S2 — Can it fail?** The `trylast` mutation above is the load-bearing falsifier,
and it was found by probe rather than reasoning: without it the guard is wrong in
the direction that matters.

**S3 — What fires it, over what?** Every pytest session over
`bootstrap/tests`, in any harness, for any agent, and for a human. That breadth is
the point and is what the `.claude/` mechanism could not offer. **Cairn has no CI.**

**S4 — Which way does it break?** Toward **refusing**, which is the opposite of
every earlier revision. A guard bug blocks verification rather than permitting an
unmeasured run. That is defensible only because the failure is loud, immediate,
carries its own remedy in the message, and is one token away — but it is a genuine
reversal of failure direction and a reviewer should weigh it as such.

**S5 — Who still wins?** An attacker who can write `bootstrap/tests/conftest.py`
already owns the suite; this adds no capability and no new surface. **Unlike every
prior revision, nothing here is outside the frozen set**, so the gate notices any
change to it. The `[TRU-4]` coverage gap is neither created nor closed by this
proposal — it is simply no longer touched.

### Known omissions

* **The routing decision is not enforced**, only stated — see *the cost of the
  swap*.
* **No durable record of an override** — the pass-through is silent, and the
  sibling proposal's ledger is what would make it countable.
* **In-process `pytest.main()`** inside a test collects a small fixture suite and
  falls under the threshold, so nested runs are unaffected — deliberate.
* **Whether the prompt changes behaviour is unmeasured** until that ledger exists.
* **A human is refused too.** No exemption distinguishes them, and none is
  proposed, because a mechanism that can tell them apart would be one an agent
  could claim.

### Withdrawn / superseded commitments

* **The entire `.claude/` mechanism** — the hook, the settings object, the script,
  the enumeration, the grammar, the `agent_id` predicate, the tracking decision.
  Withdrawn because it binds one vendor, and this project runs mixed.
* **The `_gate_manifest.py` glob extension and the `[TRU-4]` scope folding** —
  withdrawn; with no `.claude/` artifact to anchor, the addition has no subject.
  `[TRU-4]` returns to its own row, unchanged and still open.
* **The entry in Cairn's root `CLAUDE.md`** — withdrawn; there is no
  vendor-specific mechanism left to name.
* **`tools/verify.py` and the Boundary A block** — remain withdrawn from the
  previous revision, for the reasons recorded there.
* **"a speed bump, not a gate"** — withdrawn; this refuses.
* **Role-aware behaviour** — withdrawn; a conftest has no `agent_id`.
* **The claim that interception needs a harness** — withdrawn; it needed the
  suite, which every harness reaches.
