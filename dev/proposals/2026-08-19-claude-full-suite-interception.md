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
