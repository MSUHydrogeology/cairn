# portable-security-sweeps: the probe disagrees with the parser, and no leg runs

**Author**: Claude (Strategy)
**Model**: claude-opus-5 (Claude Opus 5)
**Date opened**: 2026-08-20
**Status**: revising
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

## Amendment -- Claude (author) -- 2026-08-20 -- issue closure is in scope

**Model**: claude-opus-5 (Claude Opus 5)

Appended, not merged into the sections above, per the append-only rule. This
records Maintainer direction received **after this proposal was committed
(`a005680`) and before any review**. It **adds** a deliverable; it withdraws
nothing, so no `Scope delta` is owed (scope as opened is `preserved`, and every
outcome committed above is still committed).

### 1. What was directed

> "please make sure that these proposals all include closing the issues"

and, on the review routing:

> "We will do External Security Review when it's time"

### 2. Closing the issue is a deliverable of this proposal

**This proposal closes adopter issue
[#4](https://github.com/MSUHydrogeology/cairn-scientist-ai-teams/issues/4), and
can close it alone** — all three of that issue's gaps are in scope here, and no
sibling proposal holds a piece of it.

The derived plan carries the close as an acceptance criterion of its final
chunk, gated on all of:

* the implementation landed and code-reviewed;
* the External Security Review the surface triggers, completed (see *3*);
* a closing comment posted that meets the honesty bar in *4*; and
* **Maintainer authorization for the outward-facing act.** Closing an issue on
  a public repository publishes a claim that the reported problem is resolved.
  That is a publication step, not a bookkeeping one, and an implementing agent
  does not perform it unprompted. The plan chunk is **MAINTAINER-GATED**.

### 3. The Security Review is External, and it is scheduled rather than pending

The header declares a Security Review mandated by the portable-sweep executable
trust root. The Maintainer has now fixed its tier and its timing: **External**,
taken when the implementation is ready. Recorded here so that a later reader
does not have to infer the tier from the surface, and so that the plan does not
treat an unspent Security Review as an oversight.

This does **not** change the plan-review declaration in the header: the plan
still takes its own Internal pass, and no `Plan readiness` inheritance is
claimed. An External *Security* Review is a different instrument from an
External *proposal* review and buys no inheritance.

### 4. The closing comment must name what was declined

Three of the adopter's own suggestions are refused or narrowed above, and a
close that does not say so reads as agreement that never happened. The closing
comment states, explicitly:

* that **the bare `version` subcommand was considered and not taken**, and why
  (it changes an executed argv on the trust root and trades one undocumented
  output shape for another);
* that **the admission ceremony was deliberately not automated**, and that
  reduced mode therefore remains the shipped posture — which is the adopter's
  own gap 3 question answered, not dodged; and
* that **the digest they measured was not admitted**, and by what route it could
  be — because an adopter who supplied a sha256 in good faith is owed the reason
  it did not simply get used.

It also carries the correction in *Context > D3*: `--verify-version-support`
exists. The reporter should not be left believing a subcommand is missing when
what is missing is its second half.

### 5. What a reviewer should test in this amendment

That the close is **gated on verification and not on merge**. The failure mode
this section is written against is an issue closed when the code lands and
before the legs are shown to actually run — which, per *S5* above, is the one
thing this change makes newly possible and newly unverified.

## Review -- Claude (Internal, fresh-context subagent) -- 2026-08-20

**Tier**: Internal
**Findings**: raised

**Model**: claude-opus-5 (Claude Opus 5)

Reviewed commit: d54460766442ecc367a25283f272b83cfe3aed33
Target: the complete current contract -- the whole file as of that commit, including the `## Amendment ... issue closure is in scope` section
Prior findings: none
Assurance path: high-assurance

Source claims were checked against the working tree at
`841bfc6708974267362f6d0926c12ee9d9113944` (the runner and its twin are
unmodified since `a005680`). No `Plan readiness` field is recorded: this is an
Internal pass and has no different-agent-type read to spend.

**One conformance note, left standing rather than papered over.**
`tools/lifecycle_planner.py scan` flags this section with *"appears authored by
the proposal author ('Claude (Strategy)'); a review carries reviewer-authorship"*.
That flag is the checker comparing identity tokens, and it fires on **every**
Internal review this repository's own floor asks for -- `AGENTS.md` > *Review*
defines the Internal floor as "the same agent in a fresh session," which is
independence by *time*, not by identity. Renaming the byline to clear the flag
would trade an accurate attribution for a green scan, and attribution is the
record's integrity. So the byline stays accurate and the flag stays visible.
Whether the checker should special-case a declared `**Tier**: Internal` pass is
a separate question, and not this proposal's to answer.

### Shared review sweep

Lenses swept: claim verification (every cited line opened), scope-and-outcome
(against the proposal as opened), failure-direction, trust-boundary /
untrusted-input, test-instrument validity, doc-surface routing, workflow
coherence, and the append-only / commit-discipline conventions. Where a claim
was checkable by running something, I ran it rather than reading about it.

### Steelman

This is a strong proposal and three of its hardest calls are right.

**D1's diagnosis is correct, and I reproduced it end to end.** On this host,
`gitleaks --version` prints `gitleaks version 8.30.1` and `gitleaks version`
prints `8.30.1` -- exactly the two shapes the proposal names. Running
`python scripts/run_portable_security_sweeps.py --target <repo> --json` against
a throwaway checkout produced, verbatim, the refusal the proposal quotes:
`leg="adapter" status=INCOMPLETE result=5`, reason `adapter version 'gitleaks
version 8.30.1' is not an exact X.Y.Z; the version is unmeasured, so no scan leg
was run`. The "unconditional, on any host at any version" framing holds.

**Refusing to loosen `parse_version` is the right call and is well argued.**
`_VERSION_RE` (`scripts/run_portable_security_sweeps.py:272`) is deliberately
`[0-9]` rather than `\d` and rejects leading zeros; that is a measured-versus-
unmeasured boundary, and putting a separate, anchored extractor in front of it
keeps the boundary where it belongs. Naming the regression test as *the*
deliverable rather than the extractor is the correct emphasis.

**Refusing to automate D3 is right, and the reasoning is exactly the one that
matters** -- an automated writer makes "anything that can emit an evidence
record" an admission channel. Refusing to admit the adopter's reported sha256 by
the same argument, while still offering it a recorded home, is the disciplined
answer rather than the convenient one.

Two more that deserve credit: the D2 "separate patterns, not new alternatives
inside the reviewed groups" argument is right for review-boundary reasons the
next reader will actually benefit from; and *Signals the change is wrong* is
genuinely falsifiable rather than decorative -- each signal names a recovery,
and the fourth ("the legs, once running, are noisy enough that an adopter
switches the module off") anticipates the real post-fix risk.

I also verified the two proposed keys are safe (review question 4, below R1):
`screen_local_config` inspects only the **key**, never the value
(`scripts/run_portable_security_sweeps.py:780-800`), and neither
`remote.<n>.glab-resolved` nor `branch.<n>.vscode-merge-base` is a key Git
itself interprets -- Git carries them as opaque strings, so neither can
influence execution. The existing allowlist already admits `remote.<n>.url`,
whose value is wholly candidate-controlled, so this widening adds no new
value-trust. **No finding against the two keys themselves.**

### Findings

* **[R1] BLOCKING -- the two named keys are not the class, and I refused a
  clean checkout without either of them.** D2 says the screen "is failing its
  own written design," which is right, and then fixes two measured instances.
  But the same failure mode is live for a far more common case the proposal
  never tested: **a branch name containing a dot.** `_INERT_LOCAL_PATTERNS`
  (`scripts/run_portable_security_sweeps.py:624-628`) uses `[^.]+` for the
  subsection, and Git preserves subsection text verbatim (only section and
  variable names are lowercased). Measured on a fresh `git init` whose only
  unusual property was `git config branch.release/2.0.remote origin`:

      "leg": "preflight", "status": "DEGRADED", "result": 20,
      "reason": "repository-local configuration key 'branch.release/2.0.remote'
                 is not on the reviewed inert allowlist; refused before execution"

  `git checkout -b v1.2 && git push -u` produces this on any tree. So the
  proposal as written would ship a fix that still leaves the module refusing on
  ordinary checkouts -- and the adopter would file the same issue again. This is
  the concrete evidence that D2's method is enumeration where the defect is
  structural. Instrument confirmed: the same pattern list matches
  `branch.main.remote` and `remote.origin.url`, so the negative is meaningful.
  Resolve it in the contract, not in planning -- either widen the subsection
  class deliberately (with the reasoning about why a subsection is not a key
  namespace) or state that dotted subsections are a known, accepted refusal and
  say why. Do not resolve it by narrowing D2 further.

* **[R2] BLOCKING -- S5's answer names controls that bound a different surface
  than the one D1 widens.** The proposal is right that this is "a real
  widening," and then lists containment, the sterilized child environment, the
  `.gitleaksignore` refusal and the config screen as what bounds it. I read all
  four. `child_env` (`scripts/run_portable_security_sweeps.py:541-576`) is a
  genuine allowlist and bounds *environment*. `screen_local_config` and the
  include-origin containment bound *configuration* -- and the source says so in
  its own words: "the screen bounds *configuration* -- not everything a
  candidate repository controls" (`scripts/run_portable_security_sweeps.py:758-760`).
  `refuse_candidate_ignore_files` (`scripts/run_portable_security_sweeps.py:639-656`)
  is an anti-**suppression** control -- it protects the integrity of the report,
  not the operator -- so it does not bound this class at all and should not be
  in the list.

  What D1 newly enables is a leg running the adapter over **candidate-controlled
  file content**. None of the four touches that, and the module's own shipped
  doc already names the capability that still succeeds:

  > There is **no process containment**. A malicious adapter is not contained,
  > and reduced mode in particular executes a binary whose behaviour has not
  > received this module's matrix.

  (`templates/modules/team-gated/portable-security-sweeps.md:194-196`.) The
  template asks S5 to *name one capability that still succeeds* first, and only
  fall back to by-construction/by-enumeration if you cannot. One is nameable,
  it is written verbatim in the artifact this change makes reachable, and the
  answer omits it. Rewrite S5 to name it (a parser or rule-engine defect in an
  unadmitted adapter binary, reached by hostile repository content, executing
  in the operator's own user context, uncontained), and then say which of the
  four controls bound which surface. This is a design-time question asked while
  the design is movable; deferring it to the scheduled External Security Review
  is the thing the template forbids.

* **[R3] BLOCKING -- D3 asserts a documentation absence that does not hold, and
  the proposed replacement would weaken what is already there.** D3 says the
  module doc "gains a short section: what reduced mode is, why it is honest,
  that `0` is unreachable without an admission, and the exact two-step
  ceremony." Three of those four are already shipped, verbatim:

  > **Full mode -- the only mode that can reach `0` -- is unreachable without a
  > digest match.** Reduced mode never emits CLEAN and never describes itself as
  > offline-verified.

  (`templates/modules/team-gated/portable-security-sweeps.md:96-99`; the mode
  table at :82-85 and the version-support cadence at :162-175 carry the rest.)

  Worse, the ceremony is **not two steps**. The recorded ceremony has three
  substantive steps -- matrix run, **security-lens review of the evidence**,
  reviewed source change -- documented at
  `dev/measurement/gitleaks-version-support.md:26-38` and echoed in the module
  doc's cadence bullet ("**plus** a security-lens review of the recorded
  evidence"). Writing "the exact two-step ceremony" into an adopter-facing doc
  would contradict the existing record and silently drop the security-lens
  review from the adopter's picture of it. That is a documentation regression on
  a trust surface.

  The actual adopter-facing defect is sharper and cheaper than the one D3
  describes, and I would rather the contract named it: the **shipped runner's
  own comment** is the misleading artifact, twice over. It points the reader at
  `dev/measurement/gitleaks-version-support.md`
  (`scripts/run_portable_security_sweeps.py:86-90`) -- a path that exists only
  in Cairn's tree and is **not installed** by the `team-gated` module, so it
  does not resolve for an adopter at all -- and then says `8.30.1` "enters only
  when the admission subcommand emits a record"
  (`scripts/run_portable_security_sweeps.py:99-102`), which is the sentence that
  produced the adopter's gap-3 conclusion. Fix the comment; carry the *three*-step
  ceremony (or a pointer to where an adopter can read it) into the module doc if
  anything is added there; do not re-state what :96-99 already says.

  The half of D3 I did verify as true: nothing writes the
  `CAIRN-ADMISSIONS-BEGIN`/`-END` block. Repo-wide grep finds those markers only
  as comments in the two runner copies -- instrument confirmed, the pattern
  matched where it exists.

* **[R4] BLOCKING (evidence accuracy) -- invariant (iii)'s "no test can enforce
  this and the plan should say so" is false, and writing it into the plan would
  licence dropping coverage that exists.** Two nodes already enforce the
  operative halves. `test_verify_version_support_cannot_mutate_the_source_version_set`
  (`bootstrap/tests/test_portable_security_sweeps.py:2135-2158`) asserts the
  subcommand does not rewrite the runner's own source -- with a deliberate
  second half against a revert-before-assert -- and then confirms the resulting
  run is still `reduced`. `test_every_full_mode_version_has_an_evidence_record_in_the_ledger`
  and its reverse (`bootstrap/tests/test_portable_security_sweeps.py:1977-2003`)
  pin a bijection between `_ADMITTED_ARTIFACTS` and the ledger's active
  sections, parsing the ledger independently so the oracle is not computed from
  the thing it judges. The untestable residual is narrow -- "a human editing
  source did so with review" -- and saying *that* is honest. Saying "no test can
  enforce this" is not, and it is the kind of sentence a plan inherits verbatim.

* **[R5] BLOCKING -- the D1 fix as scoped leaves the suite blind everywhere
  except the new pin.** `fake_tool`'s `--version` branch writes a bare
  `{version}\n` (`bootstrap/tests/test_portable_security_sweeps.py:154-159`,
  default `version="8.30.1"` at :116) -- the shape gitleaks **never** emits from
  `--version`. That fixture, not the extractor's absence, is the root reason a
  suite full of passing tests coexists with a module that cannot run. Adding one
  new fixture that emits the real shape pins the new path and leaves every other
  node in the file still exercising a shape that does not exist in the field, so
  a future regression in the probe path stays invisible exactly as it is today.
  The contract should decide this, not the plan: either **flip `fake_tool`'s
  default to `gitleaks version {version}`** so the whole suite runs the real
  path (and keep the bare form as an explicit parametrization, since `gitleaks
  version` really does emit it), or state why the default stays bare. This is
  the proposal's own "confirm the instrument" discipline applied to the
  instrument it is proposing to build.

* **[R6] BLOCKING -- the Amendment's gate list does not contain the Amendment's
  own stated failure condition.** Section 5 says the failure mode it is written
  against is "an issue closed when the code lands and before the legs are shown
  to actually run." Section 2's four gates are: implementation landed and
  code-reviewed; External Security Review completed; a closing comment meeting
  the honesty bar; Maintainer authorization. **"The legs are shown to actually
  run" is not among them.** Code review verifies the Boundary-B record, and
  Boundary B over `bootstrap/tests` cannot show it -- per R5 the adapter there
  is a Python script, not gitleaks. So as written, every gate can be satisfied
  with the legs still never having executed against a real adapter, which is
  precisely what S5 flags as newly possible and newly unverified. Add the fifth
  gate explicitly and name its instrument: the smoke check the proposal already
  names (`python scripts/run_portable_security_sweeps.py --target . --json` on a
  host with a real gitleaks), the expected result, and **who runs it** -- a real
  adapter is a host fact, so if the implementing agent's host has none, say that
  the gate is the Maintainer's or the adopter's to satisfy. A gate nobody is
  named for is the "human remembering" trigger `AGENTS.md` > *Verifying claims*
  tells you to describe as such.

* **[R7] Non-blocking -- "This weakens nothing ... over the same key set" is
  inaccurate, and the accurate version is a better argument.** The containment
  check and the inert check sit in the **same** per-pair loop
  (`scripts/run_portable_security_sweeps.py:780-800`): containment at :790,
  inertness at :796. Today the loop short-circuits at the first non-inert key,
  so every pair after it is never `Path(...).resolve()`-d and never
  containment-checked. After accumulation, those pairs are -- meaning more
  symlink-following filesystem resolution on candidate-controlled origin
  strings than happens today. That is a small, real, bounded increase (bounded
  by `_SCREEN_MAX_BYTES = 256 * 1024`, :609), and the disposition is unchanged.
  It is also a strict improvement in one direction the proposal does not claim:
  an injected origin sitting behind a non-inert key now gets *detected and
  named* rather than masked by an earlier refusal. Say both, rather than
  asserting sameness a reader can falsify in one read of the loop.

* **[R8] Non-blocking -- the source-of-truth direction is inverted, and the
  guard is worth citing.** The header calls `scripts/run_portable_security_sweeps.py`
  the file and `templates/modules/team-gated/run_portable_security_sweeps.py`
  "its byte-identical twin." The suite has it the other way round: `RUNNER_SRC`
  is the `templates/` copy (`bootstrap/tests/test_portable_security_sweeps.py:39`)
  and `RUNNER_TWIN` is the `scripts/` copy (:2281). An implementer following the
  header will edit the twin first. Name `templates/` as source, and cite
  `test_the_runner_twin_is_byte_identical_to_its_template_source`
  (`bootstrap/tests/test_portable_security_sweeps.py:2300-2304`) as the guard --
  it belongs in the test mapping, since this change edits both copies. I did
  verify the two files are byte-identical today.

* **[R9] Non-blocking -- three citations point at neighbours rather than at
  what they name.** `parse_version` is cited as `:276-286`; the `def` is at
  **275**. The `screen_local_config` sentence is cited as `:614-636`, but that
  range is `_INERT_LOCAL_KEYS`, `_INERT_LOCAL_PATTERNS` and `_key_is_inert` --
  `screen_local_config` itself begins at **741**. And "the comment above
  `_ADMITTED_ARTIFACTS`" is at **86-102**, above `class Admission`; the line
  immediately above `_ADMITTED_ARTIFACTS` (113) is the `CAIRN-ADMISSIONS-BEGIN`
  marker. `claim_check` passes on all of them because they are in bounds, which
  is the point: bounds are not content. Per the durable-artifact rule these
  coordinates outlive the proposal, so give the implementer ones they can act on.

* **[R10] Non-blocking -- the refusal-listing bound is weaker than claimed.**
  *Signals the change is wrong* says "the upstream byte cap on the listing
  already bounds it." True at `_SCREEN_MAX_BYTES = 256 * 1024`
  (`scripts/run_portable_security_sweeps.py:609`) -- but 256 KB of key names
  landing in a JSON `reason` field is not a useful bound, and the JSON summary
  has no separate cap on that field. The cap-and-count recovery the section
  offers as a fallback should be the design, stated up front, not the remedy
  after an unreadable report.

### Coverage

* **Covered.**
  * *Claim verification* -- every source citation opened:
    `scripts/run_portable_security_sweeps.py` at 86-102, 113, 272-286, 494-537,
    541-604, 609-656, 741-800, 1520-1552.
  * *End-to-end reproduction* -- `gitleaks --version` -> `gitleaks version
    8.30.1`, `gitleaks version` -> `8.30.1`; the runner refused with the
    proposal's exact D1 reason string at `result=5`.
  * *D2 falsification* -- a fresh `git init` carrying only
    `branch.release/2.0.remote` refused the screen, with neither proposed key
    present (R1). Instrument confirmed against `branch.main.remote` and
    `remote.origin.url`, which match.
  * *Twin identity* -- `diff` over the two runner copies: identical;
    `bootstrap/tests/test_portable_security_sweeps.py:2300-2304` is the guard.
  * *D3 absence* -- repo-wide grep for `CAIRN-ADMISSIONS`: markers only, no
    writer; instrument confirmed by the markers matching where they exist.
  * *Existing coverage* -- `bootstrap/tests/test_portable_security_sweeps.py`
    at 113-188 (`fake_tool`), 1959-2003 (ledger bijection), 2036-2245
    (`--verify-version-support` nodes).
  * *Doc surface* -- `templates/modules/team-gated/portable-security-sweeps.md`
    at 82-116, 162-175 and 192-199; `dev/measurement/gitleaks-version-support.md` at
    1-60; confirmed the ledger is not in the `team-gated` install set.
  * *Conformance* -- `python scripts/claim_check.py <this file>`: OK, no flags
    (run against the pre-review contract); `python tools/lifecycle_planner.py
    scan`: all artifacts structurally sound.
  * *Scope* -- the Amendment adds a deliverable and withdraws nothing, so
    `preserved` is correct and no `Scope delta` is owed. I make no
    scope-reduction recommendation: every finding above asks for specification
    or correction, none asks for removal.

* **Not covered / low confidence.**
  * **Same-type reviewer -- no cross-type independence on this pass.** Nothing
    here substitutes for the External Security Review the surface triggers.
  * **Adopter issue #4 not read.** I did not fetch it, so "all three of that
    issue's gaps are in scope here, and no sibling proposal holds a piece of it"
    (Amendment section 2) is unverified. Someone with the issue open should
    check it, since the whole close-the-issue deliverable rests on it.
  * **Ceiling of the D2 class not established.** R1 shows the two named keys are
    incomplete; I did not enumerate what a complete inert-key class looks like,
    and I do not believe enumeration is the right instrument for it.
  * **The legs themselves never observed running.** Every run I made stopped at
    a pre-execution refusal, so I have no evidence about behaviour, noise or
    runtime once D1 is fixed -- which is exactly the gap R6 is about.
  * **Extractor design not stress-tested.** The proposal describes the extractor
    rather than specifying it, so I could not test it against shapes beyond the
    two observed; the anchoring mutation named in S2 is the right pin and I
    could not run it.
  * **Environment note.** Reproductions ran on Python 3.12 (the ambient conda
    interpreter), not the canonical 3.13.x. Immaterial for the two shell probes
    and the runner reproduction, but not a Boundary-B-grade record.

### Second-round recommendation

**Recommended -- and the tier matters.** R1 and R2 are not editorial: R1 is a
measured counterexample showing the proposed D2 fix does not restore the
workflow it is written to restore, and R2 is a security answer that names the
wrong controls for the class the change widens. Those go back to the author
first, and the revision should be a complete current contract.

For the round after that, my recommendation to the Maintainer is that the
**External** read this proposal eventually takes be spent on the revised
contract *before* implementation, rather than only as the scheduled
implementation-time Security Review. The reason is in the negative space above:
the one thing an Internal pass structurally cannot supply is a different set of
failure modes against an S5 answer, and S5 is where this proposal is both least
certain and most consequential. Deciding that is the Maintainer's call; the
declared `required(Internal)` plan review runs regardless.

## Response -- Claude (author) -- 2026-08-20

**Model**: claude-opus-5 (Claude Opus 5)

I re-derived every citation rather than taking the review's word for it. **All
ten hold.** R1 in particular I reproduced directly: `branch.v1.2.remote` and
`branch.release/2.0.remote` both fail `_INERT_LOCAL_PATTERNS` while
`branch.main.remote` passes — so the negative is meaningful and the enumeration
charge is correct.

* **[R1] accept.** The two keys were instances; the class is *any subsection
  containing a dot*, which `git checkout -b v1.2` produces. Revision 1 replaces
  the enumeration with a structural fix and states the reasoning R1 asks for.
* **[R2] accept.** S5 named four controls, three of which bound a different
  surface, and omitted a capability the module's own doc states verbatim.
  Rewritten to name it first, then map control to surface. The reviewer is right
  that deferring this to the scheduled External Security Review is what the
  template forbids — it is a design question asked while the design is movable.
* **[R3] accept.** I asserted a documentation absence without reading
  `portable-security-sweeps.md:96-99`, which already ships three of my four
  items. Worse, "the exact two-step ceremony" would have contradicted the
  recorded ceremony — which I re-read at `dev/measurement/gitleaks-version-support.md:26-38`
  and which has **four** numbered steps including a security-lens review. Writing
  my version into an adopter-facing doc would have silently dropped that review
  from the adopter's picture. D3 is rewritten around the defect the reviewer
  identified instead, which is real and cheaper.
* **[R4] accept.** "No test can enforce this" was false; both nodes exist and I
  confirmed them. The honest residual is narrower and Revision 1 states it.
* **[R5] accept.** `fake_tool` emits the one shape gitleaks never emits from
  `--version`. That fixture is the reason a green suite coexists with a dead
  module, and adding a single new pin beside it would leave the rest of the file
  blind. Revision 1 flips the default and keeps the bare form as an explicit
  parametrization.
* **[R6] accept.** The Amendment's own stated failure condition was absent from
  its own gate list. Revision 1 adds the fifth gate, names its instrument, and
  names who satisfies it — a real adapter is a host fact, so it cannot be an
  implementing agent's obligation by default.
* **[R7] accept with modification.** I accept that "weakens nothing over the
  same key set" is falsifiable in one read of the loop. The modification: I
  state *both* directions rather than only the cost, because the detection
  improvement is the stronger half and the original text claimed neither.
* **[R8] accept.** The source-of-truth direction was inverted —
  `RUNNER_SRC` is the `templates/` copy. An implementer following my header
  would have edited the twin first.
* **[R9] accept.** Bounds are not content; `claim_check` passing on all three
  is precisely the instrument note. Corrected to `275`, `741`, `86-102`.
* **[R10] accept.** A 256 KB `reason` field is a limit, not a useful bound.
  Cap-and-count is now the design rather than the recovery.

**On the second-round recommendation.** The reviewer recommends the External
read be spent on the revised contract *before* implementation, on the grounds
that S5 is where the proposal is least certain. I agree and have not tried to
argue the tier down: the Maintainer has already scheduled an External Security
Review for this surface, and R2 is exactly the kind of question it should
receive with a written answer in front of it rather than as an open question.

## Revision 1

**Complete current contract.** Supersedes the `## Proposal` section above and
the `## Amendment`'s section 2 gate list. Self-contained: read this section and
the header, not the history.

### Scope

Three defects in the `portable-security-sweeps` adapter runner, which is shipped
at `templates/modules/team-gated/run_portable_security_sweeps.py` (**the
source**) and mirrored byte-identically at
`scripts/run_portable_security_sweeps.py` (**the twin**), guarded by
`test_the_runner_twin_is_byte_identical_to_its_template_source`. Both copies
change together; the template is edited first.

**Out of scope, explicitly:** executable resolution and the revalidation points;
the policy schema; `child_env`; the exit precedence; the admitted-artifact set's
contents (no artifact is admitted by this change); any leg's argv.

### D1 — extraction between probe and parse

`probe_version` returns the adapter's first `--version` line; `parse_version`
(`run_portable_security_sweeps.py:275`) accepts only an exact `X.Y.Z`. Gitleaks
prints `gitleaks version 8.30.1` for `--version` and a bare `8.30.1` for the
`version` subcommand, so `select_mode` never receives a parseable string and the
run refuses at `result=5` on every host.

Add one anchored, total extraction function between them, accepting exactly
`gitleaks version <X.Y.Z>` or a bare `<X.Y.Z>` and returning `None` otherwise.
**`parse_version` is not modified** — it remains the sole authority on what a
version is, and `None` keeps meaning *unmeasured*.

**The fixture is part of the fix, not of the plan.** `fake_tool`'s `--version`
branch currently writes a bare `{version}`
(`bootstrap/tests/test_portable_security_sweeps.py:154-159`) — the one shape
gitleaks never emits from that flag. Its **default flips to
`gitleaks version {version}`**, so every existing node in that file exercises
the real-world shape; the bare form stays available as an explicit
parametrization, because `gitleaks version` genuinely emits it. Without this,
the suite stays blind everywhere except the new pin, which is the condition that
let a dead module ship green.

### D2 — a structural inert-key fence, not two more names

**The enumeration was wrong, and the measurement shows it.**
`_INERT_LOCAL_PATTERNS` matches the subsection with `[^.]+`, and Git stores
subsections **verbatim** (only section and variable names are lowercased). So
every branch whose name contains a dot refuses:

```
branch.main.remote          -> INERT
branch.v1.2.remote          -> REFUSED
branch.release/2.0.remote   -> REFUSED
```

`git checkout -b v1.2` reproduces it on any tree.

**The fix, and the reasoning for it.** A Git config key is
`section.subsection.variable`. What determines whether a key can reference a
program is the **variable**, never the subsection — `branch.<anything>.remote`
is a tracking string whatever `<anything>` is. `[^.]+` was therefore fencing the
wrong component: it never bought a security property, it only made the pattern
fail on legal names. The subsection class widens to a greedy `.+`, anchored, with
the variable still drawn from a closed, named set:

```
\Aremote\..+\.(url|fetch|pushurl|mirror|tagopt|glab-resolved)\Z
\Abranch\..+\.(remote|merge|rebase|vscode-merge-base)\Z
```

The screen stays **deny-by-default on the variable**, which is the component
that carries the meaning. `.` does not match a newline, so a newline-bearing key
still refuses — deliberate, and a test pins it.

`glab-resolved` (GitLab's `glab`) and `vscode-merge-base` (VS Code) join the
closed variable sets as named members, not as a widened family.

**Accumulated refusal, with a stated cap.** The screen reports **every**
non-inert key in one refusal rather than the first. The listing is capped at a
fixed number of keys and reports how many were elided — cap-and-count is the
design, not a recovery: `_SCREEN_MAX_BYTES = 256 * 1024`
(`run_portable_security_sweeps.py:609`) bounds the *input*, and 256 KB of key
names in a JSON `reason` field is not a usable report.

**The containment check stays first-failure**, and the honest accounting of what
that costs and buys — both directions:

* *Cost.* Containment (`:790`) and inert-ness (`:796`) sit in the same per-pair
  loop. Today the loop short-circuits at the first non-inert key, so later pairs
  are never `resolve()`-d. After accumulation they are — strictly more symlink-
  following resolution on candidate-controlled origin strings, bounded by
  `_SCREEN_MAX_BYTES`.
* *Benefit.* An injected origin sitting **behind** a non-inert key is today
  masked by the earlier refusal. After accumulation it is detected and named.

Disposition is unchanged in both cases: refuse before execution.

### D3 — fix the misleading comment; do not restate the doc

**Withdrawn: the claim that the module doc lacks this content.** It does not.
`templates/modules/team-gated/portable-security-sweeps.md:96-99` already ships
"Full mode — the only mode that can reach `0` — is unreachable without a digest
match", the mode table at `:82-85` carries the dispositions, and the cadence
bullet at `:162-175` carries the rest.

**The actual adopter-facing defect is the shipped runner's own comment**, wrong
twice:

1. It points at `dev/measurement/gitleaks-version-support.md`
   (`run_portable_security_sweeps.py:86-90`), which the `team-gated` module
   **does not install** — verified: no `InstallSpec` names it. For an adopter
   that path does not resolve at all.
2. It says `8.30.1` "enters only when the admission subcommand emits a record"
   (`:99-102`). That sentence produced the adopter's gap-3 conclusion. The
   subcommand (`--verify-version-support`) emits an *evidence record*; emitting
   one admits nothing.

The comment is corrected to state what holds: the matrix subcommand produces
evidence; admission is a reviewed source edit to the fenced block; **no
automated path exists, by design**. Where it points an adopter, it points
somewhere an adopter has.

**The ceremony is four steps, not two.** `dev/measurement/gitleaks-version-support.md:26-38`
records: Maintainer supplies a checksum-verified binary; `--verify-version-support`
runs the matrix and emits a record; a **security-lens review** reads that
evidence; only then does a reviewed source change add the key and digest.
Anything carried into the module doc carries all four, or points at where they
are written. Writing "two steps" would have dropped the security-lens review
from the adopter's picture of a trust ceremony.

**Why admission stays un-automated.** An automated writer that reads an evidence
record and edits the admitted set is a path by which anything that can produce
an evidence record can admit a binary. The manual step is the control.

**No artifact is admitted by this change.** The sha256 in issue #4 arrived by
the candidate channel; it may be recorded as a *reported observation with its
source named* and may not enter `_ADMITTED_ARTIFACTS` except through the
ceremony above.

### Invariants, failure dispositions, public paths

* **(i)** `parse_version` accepts only exact `X.Y.Z` — its existing tests,
  unmodified.
* **(ii)** No leg executes before the config screen returns — call order, plus a
  test that a non-inert key refuses with no adapter invocation.
* **(iii)** `_ADMITTED_ARTIFACTS` changes only by a reviewed source edit.
  **Two nodes already enforce the operative halves**:
  `test_verify_version_support_cannot_mutate_the_source_version_set`
  (`bootstrap/tests/test_portable_security_sweeps.py:2135`) and
  `test_every_full_mode_version_has_an_evidence_record_in_the_ledger`
  (`:1977`), which parses the ledger independently of the set it judges. The
  untestable residual is narrow and is stated as such: **that a human editing
  the source did so with review**. The earlier "no test can enforce this" is
  withdrawn — it was false, and a plan would have inherited it verbatim.
* **(iv)** The twin stays byte-identical —
  `test_the_runner_twin_is_byte_identical_to_its_template_source` (`:2300`).

**Failure dispositions.** Extraction failure → `None` → INCOMPLETE (5), closed.
Screen violation → refuse before execution, closed. Containment violation →
refuse immediately, closed. Newline-bearing key → refuse, closed. No path added
here grants authority.

**Public paths → tests.** `probe_version`, the extractor, `parse_version`,
`select_mode`, `screen_local_config`, and the twin guard — all through their
real entry points in
[`test_portable_security_sweeps.py`](../../bootstrap/tests/test_portable_security_sweeps.py).

### Security preflight — S5, rewritten

S1–S4 stand as written above, with one correction: the extractor consumes
candidate-controlled bytes and is anchored and total.

**S5 — the capability that still succeeds, named first.** A **parser or
rule-engine defect in an unadmitted adapter binary, reached by hostile
repository content, executing uncontained in the operator's own user context.**
The module's shipped doc states the enabling condition verbatim
(`portable-security-sweeps.md:194-196`): *"There is no process containment. A
malicious adapter is not contained, and reduced mode in particular executes a
binary whose behaviour has not received this module's matrix."* D1 is what makes
that reachable, because today no leg runs at all.

Which control bounds which surface — the earlier answer conflated these:

| Control | Bounds |
|---|---|
| `child_env` allowlist | the child **environment** |
| `screen_local_config` + include-origin containment | candidate **configuration** (its own docstring says it bounds configuration, "not everything a candidate repository controls") |
| `refuse_candidate_ignore_files` | **report suppression** — it protects the report's integrity, not the operator. **Removed from the bounding list**; it does not bound this class. |
| The admitted-digest gate | reaching **full mode / `0`** — not reduced-mode execution |

**Nothing in the module bounds adapter execution over candidate-controlled file
content.** That is the accepted residual of running a scanner at all, it is the
module's stated posture, and it is now written where a Security reviewer meets
it rather than left implied.

### Evidence, omissions, deferred work

**Tests.** `bootstrap/tests/test_portable_security_sweeps.py`: the probe→parse
pin; the `fake_tool` default flip; dotted-subsection keys (`branch.v1.2.remote`,
`branch.release/2.0.remote`) asserting INERT; a newline-bearing key asserting
refusal; a synthesized multi-key config asserting one refusal listing all, with
the cap and elision count; a containment case asserting *immediate* refusal.
Every D2 case is **synthesized** — a tree lacking the keys cannot exercise the
change, and a test passing on an absence proves nothing.

**Smoke.** `python scripts/run_portable_security_sweeps.py --target . --json` on
a host carrying a real gitleaks. This is the only instrument that can show the
legs run; `bootstrap/tests` cannot, because its adapter is a Python script.

**Known omissions.** The extractor pins observed shapes only; an unobserved
shape fails closed to INCOMPLETE. The four-step ceremony is documented, not
performed. Whether the two named variables complete the ordinary-tooling set is
**not** established — the structural fix is what makes that question
non-blocking, since the remaining risk is a new *variable*, not a new subsection
shape.

**Deferred.** Nothing. No accepted outcome is dropped; scope as opened is
`preserved` and this revision only widens D2 and re-points D3.

### The issue-closure gates — superseding Amendment section 2

Closing issue #4 is an acceptance criterion of the derived plan's final chunk,
**MAINTAINER-GATED**, and gated on **five** things:

1. implementation landed and code-reviewed;
2. the External Security Review completed;
3. **the legs demonstrably run against a real adapter** — instrument: the smoke
   above; expected result: a completed reduced-mode run with a non-`5`
   aggregate. **Owner: the Maintainer or the adopter**, because a real gitleaks
   is a host fact and may not exist on the implementing agent's host. If nobody
   can satisfy it, the issue does not close;
4. a closing comment meeting the honesty bar (Amendment section 4), which also
   carries the D3 correction the reporter is owed;
5. Maintainer authorization for the outward-facing act.

Gate 3 is the Amendment's own stated failure condition, which its original gate
list omitted.

### Withdrawn / superseded commitments

* **"Add exactly two patterns... as separate patterns, not as new alternatives
  inside the existing groups."** Withdrawn. The two keys were instances of a
  class the pattern could not express; the subsection fence is replaced
  structurally and the two variables join the closed variable sets. Reason: R1
  demonstrated a clean checkout refusing without either key present.
* **"This weakens nothing: ... over the same key set."** Withdrawn as
  inaccurate. Replaced by the two-direction accounting in D2. Reason: R7 — the
  claim is falsifiable in one read of the loop.
* **The header's claim that the `templates/modules/team-gated/` copy is the
  byte-identical twin**
  of the `scripts/` copy.** Withdrawn; the direction is inverted. `templates/`
  is the source. Reason: R8, confirmed at `test_portable_security_sweeps.py:39`.
* **"The module doc gains a short section: what reduced mode is, why it is
  honest, that `0` is unreachable without an admission, and the exact two-step
  ceremony."** Withdrawn entirely. Three of the four items already ship at
  `portable-security-sweeps.md:96-99`, and "two-step" contradicts a recorded
  four-step ceremony. Replaced by the comment correction in D3. Reason: R3.
* **"No test can enforce this and the plan should say so"** (invariant iii).
  Withdrawn as false. Replaced by the two named nodes and a narrow residual.
  Reason: R4.
* **"The upstream byte cap on the listing already bounds it."** Withdrawn as a
  sufficient bound. Cap-and-count is now the design. Reason: R10.
* **Citations `:276-286`, `:614-636`, and "the comment above
  `_ADMITTED_ARTIFACTS`."** Superseded by `275`, `741`, `86-102`. Reason: R9.
* **The Amendment's four-gate list.** Superseded by the five-gate list above.
  Reason: R6.
* **No accepted outcome is withdrawn.** `Scope delta`: **preserved**.

## Review -- Codex (External) -- 2026-08-20

**Tier**: External Security Review
**Findings**: raised

**Model**: OpenAI GPT-5 (Codex)

Reviewed commit: c0e9b40bfa67a9ac75744492c6c124c2bfb585c1
Target: Revision 1 complete current contract
Prior findings: R1-R10 from the Internal review
Assurance path: high-assurance

### Review sweep

I opened the cited runner, its template source, the module documentation, the
test nodes, the issue-close contract, and the portable executable trust-root
rule in `AGENTS.md`. I exercised the real Homebrew Gitleaks 8.30.1 binary on
darwin/arm64, used a fresh Git repository so Cairn's own local config could not
mask the leg, and changed only the version-probe result to the normalized
`8.30.1` that D1 proposes. I also challenged the D2 regular expressions with
dotted and slash-bearing subsections, suffix injection, newline injection, and
empty subsections.

### Steelman

Revision 1 fixes the important conceptual errors from the first round. D2 now
widens the subsection grammar while keeping the authority-bearing final
variable closed; the tested suffix and newline attacks refuse. S5 is unusually
clear about the real residual: reduced mode executes an unadmitted scanner over
candidate content without process containment. I accept that residual for this
dated, trusted-contributor tripwire because reduced mode cannot report CLEAN,
the executable is revalidated immediately before use, and the report says what
is not contained. Turning the legs on is therefore acceptable in principle.

### Security preflight

* **S1:** The extractor consumes adapter-supplied stdout; repository-local
  configuration and paths are candidate-supplied by reference. The digest, not
  the self-reported version, remains the authority for full mode. This is
  accurately bounded after Revision 1.
* **S2:** The proposed extractor and D2 mutations can fail, but the execution
  contract cannot: the fake adapter accepts an argv that the field adapter
  rejects. Finding P1 is the missing mutation and independent instrument.
* **S3:** `bootstrap/tests/test_portable_security_sweeps.py` exercises a Python
  fake; the real-adapter smoke is the only named trigger over actual Gitleaks.
  Its present acceptance predicate is too weak, per P2.
* **S4:** Parse and screen errors fail to INCOMPLETE/DEGRADED and grant less
  authority. The newly exposed usage-error path also degrades, but currently
  hides the actual invalid argument behind “wrote no report.”
* **S5:** The named surviving capability is true: hostile repository content
  can reach a parser or rule-engine defect in an uncontained, unadmitted binary.
  This class is open, not bounded by the config screen or child environment.

### Findings

* **[P1] BLOCKING -- the first real leg still cannot run with Gitleaks 8.30.1.**
  After normalizing the live `gitleaks version 8.30.1` output to `8.30.1`, I ran
  the actual reduced-mode path on a fresh repository. The adapter rejected
  `--timeout=840s`: its own `gitleaks dir --help` declares `--timeout int` in
  seconds. The runner then interpreted exit 1 as the findings exit, found no
  report, and returned DEGRADED with the misleading reason “adapter wrote no
  report.” The suite currently pins the invalid suffix at
  `bootstrap/tests/test_portable_security_sweeps.py:1195`, while
  `_leg_argv` emits it at
  `templates/modules/team-gated/run_portable_security_sweeps.py:1628`.

  **Satisfier:** widen D1 to emit the measured integer-seconds form, add a fake
  that rejects the field-invalid form instead of accepting every argv, and
  preserve the adapter's bounded stderr diagnostic when exit 1 has no valid
  report. Exercise the corrected argv against real 8.30.1 before code review.

* **[P2] BLOCKING -- issue gate 3 admits the failure reproduced in P1.** A
  “non-`5` aggregate” includes DEGRADED `20`; my invalid-argv run produced
  exactly that. “Completed reduced-mode run” is not a machine-checkable
  substitute. Require `mode == "reduced"`, a current-tree leg whose status is
  `INCOMPLETE` or `FINDINGS`, no DEGRADED leg, and evidence that the real
  adapter invocation occurred. Gate 2 should say **the implementation's
  External Security code review**, so this proposal review cannot accidentally
  satisfy it. The gate is correctly attached to verified completion and the
  outward issue close, not to merge; its predicate is the defect.

* **[P3] MEDIUM -- Revision 1 is not a complete current contract.** It says
  “S1-S4 stand as written above,” requiring the derived plan and its reviewer to
  reconstruct operative security claims from superseded history. Restate S1-S4
  in the next revision and incorporate P1-P2. This is also why I do not record
  `Plan readiness: READY` on this pass.

### Coverage

**Covered** -- live version shape (`gitleaks version` and `--version`), real
reduced-mode argv and failure disposition, D2 key-language positives and
negatives, S1-S5, issue #4's Maintainer fence, withdrawal ledger R1-R10, twin
direction, test mapping, and adopter-facing residual language.

**Not covered / low confidence** -- I did not test Linux or Windows, a symlinked
Git common directory, a malicious scanner binary, the admission ceremony, or a
full-mode admitted digest. No implementation exists to code-review, and I did
not treat this proposal review as that later obligation.

### Second-round recommendation

**Recommended, narrowly.** A second External Security pass should retest the
real 8.30.1 argv, the strengthened smoke predicate, the exit-1/no-report
diagnostic, and the self-contained S1-S5 restatement. No broader redesign is
needed.
