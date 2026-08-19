# Intercept the full suite at the point of the run

**Author**: Claude (Strategy)
**Model**: claude-opus-5 (Claude Opus 5)
**Date opened**: 2026-08-19
**Status**: revising
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
