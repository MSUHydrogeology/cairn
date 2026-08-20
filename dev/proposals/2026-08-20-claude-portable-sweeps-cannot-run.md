# portable-security-sweeps: the probe disagrees with the parser, and no leg runs

**Author**: Claude (Strategy)
**Model**: claude-opus-5 (Claude Opus 5)
**Date opened**: 2026-08-20
**Status**: awaiting-review
**Assurance path**: **high-assurance** — mandatory, twice over. The change
touches the portable-sweep executable trust root named in `AGENTS.md` (the
admitted version set, and the pre-execution configuration screen), and fixing
D1 **turns on scan legs that have never executed in the field**.
**Touches**: `scripts/run_portable_security_sweeps.py` and its byte-identical
twin `templates/modules/team-gated/run_portable_security_sweeps.py` (verified
identical, `as_of 2026-08-20`); `bootstrap/tests/test_portable_security_sweeps.py`;
`templates/modules/team-gated/portable-security-sweeps.md`;
`dev/measurement/gitleaks-version-support.md`. **No policy-schema change, no
change to executable resolution or the revalidation points, no change to
`child_env` or the exit precedence.**
**Related**: adopter issue
[#4](https://github.com/MSUHydrogeology/cairn-scientist-ai-teams/issues/4).
Sibling drafts opened the same day:
[`2026-08-20-claude-adopt-into-existing-tree`](2026-08-20-claude-adopt-into-existing-tree.md),
[`2026-08-20-claude-scanner-claim-scope`](2026-08-20-claude-scanner-claim-scope.md).
**Plan review**: required(**Internal**) — an Internal proposal review spends no
different-agent-type read, so no `Plan readiness` inheritance is claimed and the
plan takes its own pass. The **Security Review** the implementation carries is
mandated by the surface `AGENTS.md` names; it is not a tier spent by choice and
is not a substitute for the plan review.

## Context

An adopter installed `portable-security-sweeps` onto a real developer checkout
(gitleaks 8.30.1, darwin/arm64, Homebrew) and **could not run a single scan
leg**. Three defects in sequence, each visible only after clearing the previous.
All three are confirmed in the source at `a26a180`.

The module's own reduced-mode posture is honest and the adopter says so. The
problem is that until D1 and D2 are fixed, **nobody can tell "reduced by design"
apart from "broken"** — which is the state the module currently ships in.

### D1 — the probe and the parser were specified independently

`probe_version` invokes the adapter as `[exe.resolved, "--version"]` and returns
the first stripped line of stdout
(`scripts/run_portable_security_sweeps.py:514-537`). `parse_version` requires an
**exact** `X.Y.Z` and returns `None` for anything else — a `v` prefix, a suffix,
surrounding text (`scripts/run_portable_security_sweeps.py:276-286`).

Gitleaks 8.x prints two different things:

```
$ gitleaks version      ->  8.30.1
$ gitleaks --version    ->  gitleaks version 8.30.1
```

So `select_mode` receives `gitleaks version 8.30.1`, `parse_version` returns
`None`, and the run refuses before any leg:

```
leg="adapter" status=INCOMPLETE result=5
reason="adapter version 'gitleaks version 8.30.1' is not an exact X.Y.Z;
        the version is unmeasured, so no scan leg was run"
```

This is **unconditional**: no leg runs on any host at any version, because the
probe and the parser disagree with each other rather than with the environment.

### D2 — the inert allowlist is narrower than ordinary developer tooling

`screen_local_config` is deny-by-default against `_INERT_LOCAL_KEYS` /
`_INERT_LOCAL_PATTERNS` (`scripts/run_portable_security_sweeps.py:614-636`). On
an ordinary checkout it refused on two keys neither set covers:

| key | written by |
|---|---|
| `remote.<name>.glab-resolved` | GitLab's `glab` CLI |
| `branch.<name>.vscode-merge-base` | VS Code |

Both are inert cached strings; neither is a program reference. The existing
pattern covers `remote\.[^.]+\.(url|fetch|pushurl|mirror|tagopt)` but not
`glab-resolved`, and there is no `branch.<n>.vscode-merge-base` equivalent.

**The control is failing its own written design**, not presenting a new judgment
call. The comment directly above the patterns already names the failure mode:

> Refusing these would make the screen unusable on real trees, which is the
> over-refusal failure mode that gets a security control switched off.

With the offending keys unset the screen passes cleanly (11 keys screened) and
the run advances to D1 — so the screen *logic* is sound; only the allowlist is
too narrow.

Separately: the refusal fires on the **first** non-inert key
(`scripts/run_portable_security_sweeps.py:796-800`), so an adopter clears them
one run at a time with no idea how many remain.

### D3 — the admission ceremony is half-shipped, and the comment reads as whole

`_ADMITTED_ARTIFACTS` is `{}` (`scripts/run_portable_security_sweeps.py:113`),
so full mode — the only mode that can report `0` — is unreachable.

**One correction to the adopter's report, and it changes the fix.** The issue
says "there is no admission subcommand in the CLI". There is:
`--verify-version-support CANDIDATE`, gated behind a mandatory confirm flag,
which runs the admission matrix against an operator-supplied binary and emits an
evidence record (`scripts/run_portable_security_sweeps.py:1538-1548`). What does
not exist is the **second half** — nothing consumes that evidence record and
writes an entry into the `CAIRN-ADMISSIONS-BEGIN` / `CAIRN-ADMISSIONS-END`
block. So the adopter's *conclusion* is right and their *diagnosis* is one step
off, which matters: this is not "build an admission subcommand", it is "close
the loop from evidence to admitted entry — or say plainly that closing it is a
Maintainer act performed by hand."

## Proposal

### D1 — an explicit extraction step between probe and parse

**`parse_version`'s strictness is correct and is not weakened.** `None` means
*unmeasured*, and unmeasured must never read as fine. The defect is that the
runner never *extracts* a version from the adapter's actual output shape before
handing bytes to the parser.

Add one named function whose sole job is that extraction: it accepts exactly
`gitleaks version <X.Y.Z>` **or** a bare `<X.Y.Z>`, anchored at both ends, and
returns `None` for everything else — a `v` prefix, a prerelease or `-dirty`
suffix, extra fields, a second line. `parse_version` remains the sole authority
on what a version *is*; the extractor only decides which substring is the
candidate.

**The regression test is the actual deliverable.** A fixture adapter emitting
each observed shape, driven end to end through `probe_version` → extractor →
`parse_version` → `select_mode`, asserting a mode is reached — so the probe's
output and the parser's expectation can never again be specified independently.

State its limit honestly: it pins **the shapes we have observed**, not gitleaks'
future output. An unobserved shape still fails closed to INCOMPLETE, which is
the correct direction.

### D2 — two named keys, and one refusal instead of a guessing loop

Add exactly two patterns, `remote\.[^.]+\.glab-resolved` and
`branch\.[^.]+\.vscode-merge-base`.

**As separate patterns, not as new alternatives inside the existing groups.**
Folding them into `remote\.[^.]+\.(url|fetch|…)` would be shorter and is wrong:
those groups are Git's own transport and tracking keys, and a third-party tool's
cache key does not belong in the same reviewed set. Separate patterns keep the
review boundary visible to the next reader.

Then make the refusal report the **full** non-inert set in one message.

**One asymmetry, deliberate, and it goes in the docstring.** The
include-origin containment check stays **first-failure**: an origin resolving
outside the candidate's git directory is an injection signal, not a
configuration-taste question, and continuing the loop after seeing one means
parsing more candidate-influenced keys than necessary. Containment refuses
immediately; inert-ness accumulates and refuses once.

This weakens nothing: the refusal still fires before any execution, over the
same key set, with the same disposition. Only its legibility changes.

### D3 — document what is actually true, and deliberately do not automate it

* The comment above `_ADMITTED_ARTIFACTS` changes from "enters only when the
  admission subcommand emits a record" to what holds: the matrix subcommand
  produces an **evidence record**; a Maintainer reviews it and edits the fenced
  block by hand; **no automated path exists, by design**.
* `templates/modules/team-gated/portable-security-sweeps.md` gains a short
  section: what reduced mode is, why it is honest, that `0` is unreachable
  without an admission, and the exact two-step ceremony.

**Why not automate it.** An automated writer that reads an evidence record and
edits the admitted set is a path by which anything that can produce an evidence
record can admit a binary. The digest deliberately lives in reviewed code rather
than in adopter-editable policy for exactly this reason. **The manual step is
the control**, not friction around it.

**The adopter-supplied digest is not admitted by this proposal.** Issue #4
reports a sha256 for gitleaks 8.30.1 darwin/arm64. Admitting a digest on the
strength of an issue report is precisely the "a candidate admits its own binary"
channel the design excludes. It may be recorded in
`dev/measurement/gitleaks-version-support.md` as a *reported observation with
its source named*, and it may not enter `_ADMITTED_ARTIFACTS` by any route
except the ceremony above.

### Documentation / doctrine surface

`templates/modules/team-gated/portable-security-sweeps.md` (descriptive layer —
the module's own doc) and two docstrings. **No doctrine rule changes**, so the
doctrine-evolution rate-limit gate is not engaged. `AGENTS.md`'s
portable-sweep-surface paragraph is re-read for agreement but is expected to
need no edit: none of the properties it enumerates moves.

## Rationale

**Which user workflow this improves:** installing the module and getting a scan
result. Today that workflow has a 0% success rate on any host.

**What contract it preserves:** all of them. The exit precedence, the policy
schema, `child_env`, executable resolution and the revalidation points are
untouched; `parse_version` keeps its strictness; the screen keeps its
disposition and its ordering relative to execution.

**Why now:** D1 makes the module inert, and D3 means an adopter cannot diagnose
that from the output. The three are cheap and they unblock each other in order.

## Alternatives considered

* **Invoke the bare `version` subcommand instead of `--version`** (the adopter's
  first suggestion). Cheapest available fix. Rejected as the primary: it changes
  an **executed argv on the trust root**, and it trades one undocumented
  output-shape assumption for another — `version` is no better specified than
  `--version`, so the same class of defect can recur, silently, on a future
  release.
* **Loosen `parse_version` to tolerate surrounding text.** Rejected outright.
  That parser is the boundary between *measured* and *unmeasured*, and widening
  it moves a security property to buy a parsing convenience.
* **Widen the allowlist by family** (`remote\.[^.]+\..*`). Rejected: it admits
  every future third-party remote key sight-unseen, which is a deny-by-default
  screen becoming an allow-by-default one.
* **Automate admission from the evidence record.** Rejected — see D3.
* **Do nothing.** The module stays installed, lockfile-tracked, and incapable of
  producing a result. The adopter has already chosen to keep it installed so it
  3-way-merges and starts working the day the probe is fixed; that is a
  reasonable posture for them and not an acceptable one for us.

## Evidence / verification plan

### Author-accounting — invariants, failure modes, edge cases

* **Invariants.** (i) `parse_version` accepts only exact `X.Y.Z` — enforced by
  its existing tests, unchanged. (ii) No leg executes before the config screen
  returns — enforced by call order plus a test that a non-inert key refuses with
  no adapter invocation. (iii) `_ADMITTED_ARTIFACTS` changes only through a
  reviewed code edit — enforced by it being source, plus the fenced-block
  convention; **no test can enforce this and the plan should say so.**
* **Failure modes.** Extraction failure → `None` → INCOMPLETE (exit 5), closed.
  Screen violation → refuse before execution, closed. Containment violation →
  refuse immediately, closed. All three fail *closed*; none becomes open.
* **Edge cases.** Empty `--version` output (already DEGRADED, unchanged);
  multi-line output (first line only, unchanged); a prerelease suffix
  (must return `None` — a named test); a version that extracts but whose major
  is not `_SUPPORTED_MAJOR` (existing path, unchanged); zero non-inert keys
  (screen passes, no report); many non-inert keys (one refusal listing all).
* **Public-path → test mapping.** `probe_version`, the new extractor,
  `select_mode`, and `screen_local_config`, each exercised through its real
  entry point in
  [`test_portable_security_sweeps.py`](../../bootstrap/tests/test_portable_security_sweeps.py).
* **Known omissions.** The extractor is pinned against observed shapes only. The
  ceremony in D3 is documented, not executed — **this proposal admits no
  artifact and reaches no full mode.** Whether the two `glab`/VS Code keys are
  the complete set of ordinary-tooling keys is *not* established; they are the
  two measured on one tree.

#### Security preflight — five questions

* **S1 — Who supplied it?** The version decision consumes the adapter's own
  stdout — supplied by the thing being decided about. That is the design's
  premise, and it is why the **digest** is the authority and the self-reported
  version only selects a key. The extractor therefore consumes
  candidate-controlled bytes and must be anchored and total. The screen consumes
  the candidate repository's own config, already treated as candidate-controlled.
  The sha256 in issue #4 arrives by the candidate channel and is **not** admitted.
* **S2 — Can it fail?** The mutation that must redden the new pin: unanchor the
  extractor, so a fixture emitting `gitleaks version 8.30.1-dirty` parses as
  `8.30.1`. The plan **runs this mutation and records the failure**, because a
  pin derived from the same string it checks cannot fail.
* **S3 — What fires it, over what?**
  `python -m pytest bootstrap/tests/test_portable_security_sweeps.py`. Nothing
  else selects it: no CI (Cairn has none), no hook, no gate. Its only recurring
  trigger is the engine suite. The module doc sentence describing the check must
  be quoted in the plan and shown to agree with that command.
* **S4 — Which way does it break?** Every path added or touched lands on the
  *less authority* side: unparseable → no leg; unscreened → refuse; drifted
  digest → DEGRADED. No default, fallback or normalization added here grants
  authority.
* **S5 — Who still wins?** **This is the answer that matters, and it is a real
  widening.** Fixing D1 causes scan legs to execute that have never executed in
  the field. A candidate controlling the repository under scan does not gain
  full mode (the digest, not the version, gates that) — but it now reaches
  *reduced* mode, where legs run over candidate-controlled content. That is the
  module's intended behavior and the reason containment, the sterilized child
  environment, the `.gitleaksignore` refusal, and the config screen all exist.
  The class is bounded **by those constructions**, not closed by enumeration.
  The plan treats "the legs now work" as a verification obligation, not a
  corollary of "the probe now parses."

### Tests required

`bootstrap/tests/test_portable_security_sweeps.py` — the probe/parser pin
(the D1 deliverable), the two new allowlist patterns, a synthesized multi-key
non-inert config asserting one refusal listing all, and a containment case
asserting *immediate* refusal. D2's cases must **synthesize** the offending keys:
a tree that lacks them cannot exercise the change, and a test that passes on an
absence is the instrument that cannot observe what it is aimed at.

### Examples / smoke checks

`python scripts/run_portable_security_sweeps.py --target . --json` on a real
checkout, which is the exact path that produced the report. **N/A**: the example
gallery and the scaffold dry-run do not reach this module.

## Signals the change is wrong

* **A host prints a third version shape.** Symptom: INCOMPLETE with an
  extraction reason on a supported gitleaks. This is the designed direction, not
  a regression — recovery is to extend the extractor and the pin together, never
  to loosen the anchor.
* **A widened key turns out to be a program reference.** Symptom: any evidence
  that `glab-resolved` or `vscode-merge-base` can influence execution. Recovery
  is one-line: remove that pattern. This is why they are separate patterns.
* **The accumulated refusal grows unmanageably on a hostile config.** The
  upstream byte cap on the listing already bounds it; if it is still unreadable,
  cap the reported list and say how many were elided — never silently truncate.
* **The legs, once running, are noisy or slow enough that an adopter switches
  the module off.** That is the failure mode this module names about itself, and
  it would mean D1's fix exposed a problem D1 was hiding. Recovery is a
  separate proposal about leg scope, not a re-narrowing of the probe.
