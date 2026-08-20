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

## Response -- Claude (author) -- 2026-08-20 (round 2)

**Model**: claude-opus-5 (Claude Opus 5)

**P1 I reproduced independently against Homebrew gitleaks 8.30.1 before
accepting it**, because it asserts the module is broken a second way:

```
$ gitleaks dir . ... --timeout=840s
FTL invalid argument "840s" for "--timeout" flag: strconv.ParseInt: parsing "840s": invalid syntax
$ gitleaks dir . ... --timeout=840
INF scanned ~6 bytes (6 bytes) in 2.69ms
INF no leaks found          # report written
```

`gitleaks dir --help` declares `--timeout int ... in seconds`. The suffixed form
is emitted at `run_portable_security_sweeps.py:1628` and **pinned** at
`bootstrap/tests/test_portable_security_sweeps.py:1195`.

* **[P1] accept — and it expands scope.** This is a second, independent reason
  the module cannot run, and it is invisible to the entire suite because the
  fake accepts any argv while the test asserts the invalid one. Revision 2 adds
  it as **D4**. Scope expansion authorized by the Maintainer:

  > "Yes, please go on"

  given in answer to a message that named the expansion, its content (the argv,
  its fake, its pinned test, and the misleading diagnostic) and its consequence
  for plan-readiness inheritance. **Declared expansion invalidates any inherited
  plan-readiness basis**, which is consistent with this pass withholding it.
* **[P2] accept.** My gate 3 predicate was unfalsifiable in the direction that
  matters: "a non-`5` aggregate" admits DEGRADED `20`, which is exactly what P1
  produces. Replaced with the machine-checkable conjunction. I also accept the
  gate-2 ambiguity — "the External Security Review" could be read to mean *this*
  pass, which would let a proposal review satisfy an implementation gate.
* **[P3] accept.** "S1–S4 stand as written above" made a *complete current
  contract* point backward, which is a contradiction in terms. Revision 2
  restates S1–S5 in full. Three reviewers raised this same defect on three
  proposals; it was one habit, not three slips.

## Revision 2

**Complete current contract.** Self-contained: this section plus the header is
the whole operative contract. It supersedes Revision 1 entirely and inherits
nothing from the `## Proposal` section or the `## Amendment`.

### Scope

Four defects in the `portable-security-sweeps` adapter runner, shipped at
`templates/modules/team-gated/run_portable_security_sweeps.py` (**the source**)
and mirrored byte-identically at `scripts/run_portable_security_sweeps.py`
(**the twin**), guarded by
`test_the_runner_twin_is_byte_identical_to_its_template_source`. The template is
edited first.

**Out of scope, explicitly:** executable resolution and the revalidation points;
the policy schema; `child_env`; the exit precedence; the contents of the
admitted-artifact set (**no artifact is admitted by this change**).

### D1 — extraction between probe and parse

`probe_version` returns the adapter's first `--version` line; `parse_version`
(`:275`) accepts only an exact `X.Y.Z`. Gitleaks prints `gitleaks version 8.30.1`
for `--version` and a bare `8.30.1` for the `version` subcommand, so
`select_mode` never receives a parseable string and every run refuses at
`result=5`.

Add one anchored, total extraction function between them, accepting exactly
`gitleaks version <X.Y.Z>` or a bare `<X.Y.Z>`. **`parse_version` is not
modified** — `None` keeps meaning *unmeasured*.

**The fixture is part of the fix.** `fake_tool`'s `--version` branch writes a
bare `{version}` (`test_portable_security_sweeps.py:154-159`) — the one shape
gitleaks never emits from that flag. Its **default flips** to
`gitleaks version {version}`; the bare form stays an explicit parametrization,
because `gitleaks version` genuinely emits it.

### D2 — a structural inert-key fence

`_INERT_LOCAL_PATTERNS` matches the subsection with `[^.]+`, and Git stores
subsections **verbatim**. Measured: `branch.main.remote` is INERT;
`branch.v1.2.remote` and `branch.release/2.0.remote` are REFUSED. `git checkout
-b v1.2` reproduces it on any tree.

A Git key is `section.subsection.variable`. What can reference a program is the
**variable**, never the subsection — `branch.<anything>.remote` is a tracking
string whatever `<anything>` is. `[^.]+` fenced the wrong component: it bought
no security property and only broke on legal names. The subsection widens to an
anchored greedy `.+`; the variable stays a closed named set:

```
\Aremote\..+\.(url|fetch|pushurl|mirror|tagopt|glab-resolved)\Z
\Abranch\..+\.(remote|merge|rebase|vscode-merge-base)\Z
```

Deny-by-default **on the variable**. `.` does not match a newline, so a
newline-bearing key still refuses; a test pins it, and so do suffix-injection
and empty-subsection cases.

**Accumulated refusal with a stated cap.** Every non-inert key is reported in
one refusal, capped at a fixed key count with the elided count named.
Cap-and-count is the design: `_SCREEN_MAX_BYTES = 256 * 1024` (`:609`) bounds
the *input*, and 256 KB of key names in a JSON `reason` is not a usable report.

**Containment stays first-failure**, and both directions of that choice:

* *Cost.* Containment (`:790`) and inert-ness (`:796`) share one per-pair loop.
  Today it short-circuits at the first non-inert key, so later pairs are never
  `resolve()`-d. After accumulation they are — more symlink-following resolution
  on candidate-controlled origin strings, bounded by `_SCREEN_MAX_BYTES`.
* *Benefit.* An injected origin **behind** a non-inert key is today masked by
  the earlier refusal; after accumulation it is detected and named.

### D3 — fix the misleading comment; do not restate the doc

The module doc is **not** missing this content:
`portable-security-sweeps.md:96-99` already ships *"Full mode — the only mode
that can reach `0` — is unreachable without a digest match"*, with the mode
table at `:82-85` and the cadence at `:162-175`.

**The shipped runner's own comment is the defect**, wrong twice: it points at
`dev/measurement/gitleaks-version-support.md` (`:86-90`), which the `team-gated`
module **does not install**, so the path does not resolve for an adopter; and it
says `8.30.1` *"enters only when the admission subcommand emits a record"*
(`:99-102`) — the sentence that produced the adopter's gap-3 conclusion.
`--verify-version-support` emits an *evidence record*; emitting one admits
nothing.

Corrected to state what holds, pointing only where an adopter can follow.

**The ceremony is four steps**, per `dev/measurement/gitleaks-version-support.md:26-38`:
Maintainer supplies a checksum-verified binary; the matrix subcommand emits a
record; a **security-lens review** reads it; only then does a reviewed source
change add the key and digest. Anything carried into the module doc carries all
four or points at them. **Admission stays un-automated**: an automated writer
that reads an evidence record and edits the admitted set is a path by which
anything that can produce a record can admit a binary. The manual step is the
control.

The sha256 in issue #4 arrived by the candidate channel; it may be recorded as a
*reported observation with its source named*, and may not enter
`_ADMITTED_ARTIFACTS` except through that ceremony.

### D4 — the leg argv is invalid, and the suite pins it (new in Revision 2)

**Measured on Homebrew gitleaks 8.30.1, darwin/arm64:**

| argv | result |
|---|---|
| `--timeout=840s` | `FTL invalid argument "840s" ... strconv.ParseInt` — no report |
| `--timeout=840` | scans, `no leaks found`, report written |

`gitleaks dir --help` declares `--timeout int ... in seconds`. `_leg_argv` emits
`f"--timeout={_ADAPTER_TIMEOUT}s"` (`:1628`), and
`test_portable_security_sweeps.py:1195` asserts that exact suffixed string — so
the suite **locks the defect in**.

Three changes, and the third is the one that matters for the next defect of this
kind:

1. **Emit the measured integer-seconds form** (no suffix), and re-point the
   test at it.
2. **Preserve the adapter's bounded stderr diagnostic when exit 1 carries no
   valid report.** Today the runner reads exit 1 as the findings exit, finds no
   report, and returns DEGRADED with *"adapter wrote no report"* — which is true
   and useless. The adapter said exactly what was wrong; the runner discarded
   it. `_STDERR_DIAGNOSTIC_BYTES` already exists for bounded stderr capture.
3. **The fake must be able to refuse.** `fake_tool` accepts every argv, which is
   why a green suite coexists with a module that cannot run. It gains a mode
   that **rejects the field-invalid form**, so an argv regression reddens
   locally instead of waiting for a host with a real adapter.

**Ordering.** D1 → D2 → D4 → D3. D4 is only observable once D1 lets a run reach
the leg, and it must land before any close, because it is the defect gate 3 now
exists to catch.

### Invariants, failure dispositions, public paths

* **(i)** `parse_version` accepts only exact `X.Y.Z` — existing tests, unmodified.
* **(ii)** No leg executes before the config screen returns — call order, plus a
  test that a non-inert key refuses with no adapter invocation.
* **(iii)** `_ADMITTED_ARTIFACTS` changes only by a reviewed source edit. Two
  nodes enforce the operative halves:
  `test_verify_version_support_cannot_mutate_the_source_version_set` (`:2135`)
  and `test_every_full_mode_version_has_an_evidence_record_in_the_ledger`
  (`:1977`), which parses the ledger independently of the set it judges. The
  untestable residual is narrow and stated: **that a human editing the source
  did so with review**.
* **(iv)** The twin stays byte-identical — `test_..._twin_is_byte_identical...` (`:2300`).
* **(v)** *(new)* The emitted leg argv is accepted by the admitted adapter major
  — enforced by the refusing fake, and by the real-adapter smoke.

**Failure dispositions.** Extraction failure → INCOMPLETE (5), closed. Screen
violation → refuse before execution, closed. Containment violation → refuse
immediately, closed. Newline-bearing key → refuse, closed. **Adapter usage error
→ DEGRADED (20) carrying the adapter's own bounded diagnostic**, closed — the
disposition is unchanged from today; what changes is that it says why. No path
added here grants authority.

**Public paths → tests.** `probe_version`, the extractor, `parse_version`,
`select_mode`, `screen_local_config`, `_leg_argv`, and the twin guard — all
through their real entry points in
[`test_portable_security_sweeps.py`](../../bootstrap/tests/test_portable_security_sweeps.py).

### Security preflight — S1 to S5, restated in full

* **S1 — Who supplied it?** The version decision consumes the **adapter's own
  stdout**, supplied by the thing being decided about; that is the design's
  premise, and it is why the **digest** is the authority and the self-reported
  version only selects a key. The extractor therefore consumes
  candidate-controlled bytes and is anchored and total. The config screen
  consumes the **candidate repository's own config and origin paths**, supplied
  by reference by the candidate. The policy document is adopter-owned;
  `_ADMITTED_ARTIFACTS` is reviewed source. The sha256 in issue #4 arrives by
  the candidate channel and is **not** admitted.
* **S2 — Can it fail?** Mutations that must redden, each run and recorded:
  unanchor the extractor (a fixture emitting `gitleaks version 8.30.1-dirty`
  must not parse as `8.30.1`); restore `[^.]+` (the dotted-subsection cases must
  fail); **restore the `s` suffix in `_leg_argv` (the refusing fake must fail)**.
  That third mutation is the one Revision 1 had no instrument for: a fake that
  accepts every argv cannot fail, and P1 is what that bought.
* **S3 — What fires it, over what?**
  `python -m pytest bootstrap/tests/test_portable_security_sweeps.py` — nothing
  else selects it: no CI (Cairn has none), no hook, no gate. **That suite
  exercises a Python fake, not gitleaks**, so the only trigger over a real
  adapter is the smoke below, whose trigger is a human running it. The module
  doc's description of the check is quoted in the plan and shown to agree.
* **S4 — Which way does it break?** Every path lands on *less* authority:
  unparseable → no leg; unscreened → refuse; drifted digest → DEGRADED; invalid
  argv → DEGRADED **with the reason preserved**. No default, fallback or
  normalization added here grants authority.
* **S5 — Who still wins?** The capability that still succeeds, named: **a parser
  or rule-engine defect in an unadmitted adapter binary, reached by hostile
  repository content, executing uncontained in the operator's own user
  context.** The module's shipped doc states the enabling condition verbatim
  (`portable-security-sweeps.md:194-196`): *"There is no process containment. A
  malicious adapter is not contained, and reduced mode in particular executes a
  binary whose behaviour has not received this module's matrix."* D1 and D4 are
  what make it reachable. Which control bounds which surface:

  | Control | Bounds |
  |---|---|
  | `child_env` allowlist | the child **environment** |
  | `screen_local_config` + include-origin containment | candidate **configuration** — its own docstring says it bounds configuration, "not everything a candidate repository controls" |
  | `refuse_candidate_ignore_files` | **report suppression** — it protects report integrity, not the operator, and does **not** bound this class |
  | the admitted-digest gate | reaching **full mode / `0`** — not reduced-mode execution |

  **Nothing in the module bounds adapter execution over candidate-controlled
  file content.** That is the accepted residual of running a scanner at all and
  the module's stated posture. The class is **open**, not bounded.

### Evidence, omissions, deferred work

**Tests.** The probe→parse pin; the `fake_tool` default flip; the refusing-fake
argv mode; dotted, slashed, suffixed, empty and newline-bearing subsection cases;
a synthesized multi-key config asserting one capped refusal with an elision
count; a containment case asserting *immediate* refusal; the exit-1/no-report
diagnostic. Every D2 case is **synthesized** — a tree lacking the keys cannot
exercise the change.

**Smoke — the only real-adapter instrument.**
`python scripts/run_portable_security_sweeps.py --target . --json` on a host
with real gitleaks, against a **fresh repository** so local config cannot mask
the leg.

**Known omissions.** The extractor pins observed shapes only; an unobserved
shape fails closed. Not tested: Linux, Windows, a symlinked Git common
directory, a malicious adapter binary, the admission ceremony, or a full-mode
admitted digest. The four-step ceremony is documented, not performed. Whether
the two named variables complete the ordinary-tooling set is not established —
the structural fix is what makes that non-blocking, since the residual risk is a
new *variable*, not a new subsection shape.

**Deferred.** Nothing.

### The issue-closure contract — restated in full

Closing issue [#4](https://github.com/MSUHydrogeology/cairn-scientist-ai-teams/issues/4)
is an acceptance criterion of the derived plan's final chunk. This proposal can
close #4 alone; no sibling holds a piece of it. The chunk is
**MAINTAINER-GATED** — closing a public issue publishes a claim that the
reported problem is resolved, which is a publication step, not bookkeeping.

Five gates, all required:

1. Implementation landed and code-reviewed.
2. **The implementation's External Security code review** completed. *Not* this
   proposal review — stated explicitly so a proposal pass cannot satisfy an
   implementation gate.
3. **The legs demonstrably run against a real adapter**, by the machine-checkable
   predicate: `mode == "reduced"`, **and** a current-tree leg whose status is
   `INCOMPLETE` or `FINDINGS`, **and** no leg with status `DEGRADED`, **and**
   recorded evidence that a real adapter invocation occurred. *(The earlier
   predicate — "a non-`5` aggregate" — is withdrawn: it admits DEGRADED `20`,
   which is precisely what D4's defect produces.)* **Owner: the Maintainer or
   the adopter**, because a real gitleaks is a host fact and may not exist on
   the implementing agent's host. If nobody can satisfy it, the issue does not
   close.
4. A closing comment that names **what was declined**: that the bare `version`
   subcommand was considered and not taken, and why; that admission was
   deliberately **not** automated, so reduced mode remains the shipped posture —
   the reporter's gap-3 question answered rather than dodged; and that the
   digest they measured was **not** admitted, with the route by which it could
   be. It also carries the D3 correction — `--verify-version-support` exists;
   what is missing is its second half — and **D4**, since the reporter's
   original report could not have seen it.
5. Maintainer authorization for the outward-facing act.

### Withdrawn / superseded commitments

* **Revision 1's "S1–S4 stand as written above."** Withdrawn. S1–S5 are restated
  in full above. Reason: P3 — a complete current contract that points backward
  is not complete, and this is why no `Plan readiness` was recorded.
* **Gate 3's predicate "a completed reduced-mode run with a non-`5` aggregate."**
  Withdrawn as unfalsifiable in the direction that matters. Replaced by the
  four-part conjunction. Reason: P2.
* **Gate 2's "the External Security Review."** Superseded by "the
  implementation's External Security code review." Reason: P2 and its siblings.
* **The implicit claim that D1 + D2 + D3 make the module runnable.** Withdrawn.
  D4 is a second, independent blocker, measured. Reason: P1.
* **`Scope delta`: expanded.** D4 is **added** scope, authorized by the
  Maintainer as quoted in the Response above. No accepted outcome is removed;
  every commitment from the opened proposal survives. **This declared expansion
  invalidates any inherited plan-readiness basis** — consistent with the
  External pass having withheld `READY`.

## Review -- Claude (Internal, fresh-context subagent) -- 2026-08-20 (round 3, narrow: D4)

**Tier**: Internal (fresh-context same-type read — the Internal floor)
**Findings**: raised

**Model**: claude-opus-5 (Claude Opus 5)

Reviewed commit: 37d89a047f0dda664b2a94a7fe0f8185c0b899a5
Target: **Revision 2, `### D4` only, and D4's consequences elsewhere in
Revision 2.** This is a **narrow pass**, not a whole-contract read. D1, D2, D3
and the surviving parts of S1–S5 were covered by the round-1 Internal read
(R1–R10) and the round-2 Codex External Security read (P1–P3); I did not
re-derive them. D4 is scope added *after* the External pass, so no reviewer has
read it — that is the whole reason for this round.
Prior findings: R1–R10 (Internal, round 1); P1–P3 (Codex External Security,
round 2). All accepted and folded into Revision 2.
Assurance path: high-assurance

**No `Plan readiness` is recorded, and none may be**: an Internal pass cannot
supply it, and Revision 2's own declared scope expansion invalidates any
inherited basis.

### Review sweep

I read `### D4` and the four Revision 2 sections it reaches (`Invariants`,
`Security preflight`, `Evidence`, `The issue-closure contract`, `Withdrawn /
superseded commitments`). I opened `_leg_argv`
(`templates/modules/team-gated/run_portable_security_sweeps.py:1602-1630`), its
three call sites (`:1421`, `:1755`, `:1820`), `classify_leg` (`:988-1024`),
`read_report` (`:845-915`), `_diagnostic` (`:918-922`), the output contract
(`:804-831`), `child_env` (`:541-571`), `REQUIRED_LEG_OPTIONS` (`:1179-1183`),
the matrix subcommand's end-to-end block (`:1419-1447`), `fake_tool`
(`bootstrap/tests/test_portable_security_sweeps.py:120-186`) and the pinned
assertion (`:1186-1195`). Every citation in D4 resolves and is accurate; the
twin is byte-identical as of this commit (`cmp`, clean).

I exercised the **real Homebrew gitleaks 8.30.1 on darwin/arm64** throughout,
against purpose-built repositories in a scratch tree: a clean one, one carrying
a live `ghp_` token, and a non-repository directory. Where I report a negative
result below I first confirmed the same measurement returns a positive on a
case known to be present — the argv sweep is anchored by the `--timeout` defect
itself reproducing, and the "no secret material on stderr" result is anchored
by a run that did find and report a real secret.

### Steelman

D4 is a good catch and the proposal handles it with the right instincts. It
does not merely fix the flag: it names the reason the defect was invisible (a
fake that accepts every argv, and an assertion whose *purpose* was the deadline
arithmetic with the wire format riding along), and item 3 correctly identifies
that the instrument, not the flag, is what matters for the next defect of this
kind. The ordering constraint is real, invariant (v) is the right shape, the S2
mutation ledger gains the one mutation Revision 1 had no instrument for, and
the withdrawal of "D1 + D2 + D3 make the module runnable" is honest about what
P1 cost the earlier contract. The scope expansion is declared, quoted, and
paired with the correct consequence for plan-readiness inheritance.

### Coverage — what I could not falsify

**The argv fix is complete for 8.30.1, and I checked it exhaustively rather
than trusting that `--timeout` was the only one.** I compared every element
`_leg_argv` emits against `gitleaks dir --help` and `gitleaks git --help`, then
ran both legs' exact argv end-to-end with only the `s` dropped:

* current-tree (`dir`): scans, writes the report, exit `0` clean / `1` with a
  planted `ghp_` token, `Match` and `Secret` both `REDACTED`.
* history (`git`): scans 2 commits, writes the report, same dispositions.

Specifics I challenged and found sound: `--follow-symlinks=false` is a pflag
bool and accepts `=false`; `--redact=100` matches the declared
`uint[=100]`; `--max-archive-depth=0` / `--max-decode-depth=0` are `int`;
the subcommand split is right in both directions (`--follow-symlinks` is
`dir`-only and `--log-opts` is `git`-only, and each is emitted only on its own
leg — the real adapter rejects the swap); the target is a resolved absolute
path in positional position, so it cannot be read as a flag. **`--timeout` was
the only field-invalid element.** The author's stated worry — that they found
one bad flag by accident of it being first — is discharged for this version and
platform, which is the scope any single measurement can carry.

**Gate 3's new predicate does exclude D4's failure, and I could not satisfy it
while the module is broken.** Traced: invalid `--timeout` → exit `1`, no report
→ `read_report` raises → current-tree `DEGRADED`, failing *two* conjuncts. With
D1 unfixed, `choice.mode is None` and no leg runs at all, failing `mode ==
"reduced"`. In the healthy reduced case the current-tree leg lands on
`INCOMPLETE` (`:1017-1023`) when clean and `FINDINGS` when not, so both real
outcomes are admitted and the predicate is satisfiable exactly when the leg
genuinely ran. P2's repair holds. Two qualifications are in R4 below.

### Findings

Two blocking, five non-blocking.

#### B1 (blocking) — item 2's condition spans the redaction-failure branch, which turns the diagnostic into a secret-bearing sink

D4 item 2 scopes the new stderr preservation to *"exit 1 carries no valid
report"*. Read against the code, that condition is the **whole** `Degraded`
surface of `read_report` (`:845-915`), because `classify_leg` catches it in one
place (`:1006-1007`). That surface includes:

```
adapter result {index} carries an unredacted {field!r}; the report is not
trustworthy and no finding is relayed          (:902-907)
```

That branch fires precisely when the adapter **ignored `--redact=100`**. And
gitleaks' own help scopes that flag to *"redact secrets from logs and stdout"*
— one flag governs both surfaces, so an adapter that did not honour it in the
report is the adapter that did not honour it in its logs either. Preserving its
stderr into `LegOutcome.reason` carries it into `summarize()` (`:1087`) and
from there into the summary JSON, the human report and the `--security-
verification` child document — the sink the module's own comment calls *"the
one failure mode in which this module would be strictly worse than not
existing"* (`:809-812`), and the one `FORBIDDEN_RESULT_FIELDS` exists to close.

This is not hypothetical for the case the module is built for: reduced mode
exists to run an **unadmitted** binary, so "the adapter did not behave as
measured" is its normal operating assumption, not an edge case.

Revision 2's preflight does not catch this because **S4 asks the authority
question and no S asks the sink question**. S4's *"No default, fallback or
normalization added here grants authority"* is true of item 2 and beside the
point: item 2 grants no authority, it opens an egress. S1 asks who supplied the
bytes and answers for the version probe and the config screen, not for the
adapter's stderr. The preflight needs a sentence that asks, of every newly
relayed byte, *which sink does this reach*.

Two additional notes on the same item, both smaller than the above but in it:

* D4 cites the **constant** `_STDERR_DIAGNOSTIC_BYTES` (`:807`) as the existing
  machinery. The existing machinery is the **function** `_diagnostic()`
  (`:918-922`), which bounds *and* `_escape`s, and whose docstring states the
  property that matters: *"No child stdout or stderr is ever relayed
  verbatim."* Naming only the constant admits an implementation that slices 512
  bytes and interpolates them raw. Name the function.
* The plain usage-error case is clean on this point — I measured stderr for the
  invalid `--timeout` and it carries the flag error plus a usage dump and no
  candidate content beyond the runner-owned argv and the target path. It is the
  *other* members of the condition set that are the problem.

**How to resolve it.** Either narrow the condition so it reaches only "the
adapter wrote no report at all" and explicitly excludes every branch that
judged a report the adapter *did* write — or take B2's remedy, which dissolves
this finding rather than fencing it.

#### B2 (blocking) — D4's blast radius includes the admission ceremony, which is un-performable and misdiagnoses; Revision 2 names neither

`_leg_argv` has **three** call sites, and D4 accounts for one. The third is
`cmd_verify_version_support` (`:1421`) — the matrix subcommand that is **step 2
of D3's own four-step admission ceremony**. Reproduced on this host against the
unmodified tree:

```
$ python scripts/run_portable_security_sweeps.py \
    --verify-version-support /opt/homebrew/Cellar/gitleaks/8.30.1/bin/gitleaks \
    --confirm-executing-an-unadmitted-binary
admit: false
refusals: ["output-schema drift on the 'current-tree' leg:
            the adapter wrote no report at '.../reports/current-tree.json'"]
candidate_version: gitleaks version 8.30.1
```

Three consequences, none of them in Revision 2:

1. **The guard written for exactly this is bypassed.** `:1434-1440` refuses
   with *"the candidate did not accept the runner-owned argv for the {leg!r}
   leg... a candidate that rejects a required option is not the tool this
   contract was measured against"* — but it fires only on
   `returncode not in (_EXIT_NO_FINDINGS, _EXIT_FINDINGS)`, and gitleaks
   signals an invalid flag **value** with exit `1`, which the runner has a
   documented meaning for. So the ceremony refuses with the **wrong reason**,
   sending the next investigator at the report schema instead of the argv. By
   `AGENTS.md`'s own standard this is the silent-tool defect wearing a
   confident face: the trigger exists, resolves, runs, and does not check the
   property it names. `REQUIRED_LEG_OPTIONS` (`:1179-1183`) does not save it —
   it is a **presence** check that never inspects form, and it omits
   `--timeout` entirely.
2. **Step 4 is therefore unreachable for every real gitleaks.** D3 says *"the
   four-step ceremony is documented, not performed."* The stronger and true
   statement is that it is **un-performable** until D4 lands: no candidate can
   get past step 2, so nothing can ever enter `_ADMITTED_ARTIFACTS`, so full
   mode and `0` are unreachable for a reason D3 does not give. D3's corrected
   comment must not describe a ceremony that cannot currently run, and the
   issue-closure comment (gate 4) owes the reporter this, since it is the real
   answer underneath their gap-3 question. I confirmed the ledger
   (`dev/measurement/gitleaks-version-support.md`) carries no admitted triple,
   so nothing already recorded is invalidated — the exposure is forward-looking
   only.
3. **The evidence plan has no instrument for this path** — see R3.

**The remedy I recommend, which also dissolves B1.** The root cause of both is
that gitleaks overloads exit `1`. That is removable at the source. Measured on
8.30.1, with `--exit-code 42` added to the leg argv:

| condition | exit |
|---|---|
| leaks found (`dir` and `git`) | `42` |
| invalid flag value (`--timeout=840s`) | `1` |
| unwritable report path | `1` |
| unloadable config | `1` |
| unknown flag | `126` |

Move `_EXIT_FINDINGS` off `1` and the invalid-argv case lands in the runner's
**existing** branch at `:999-1003`, which already attaches `_diagnostic(stderr)`
— bounded, escaped, and reached only on exit codes the runner has no meaning
for. No new relay path, no new sink, `read_report`'s `Degraded` branches
untouched, and `:1434` starts firing with its correct message. The diagnostic
preservation item 2 wants becomes a consequence of existing code rather than a
new one. Note that the unknown-flag class **already** gets its diagnostic
preserved today at exit `126`; the runner loses it only for the invalid-value
class, and only because of the overload.

I record plainly that this is **a further argv element on top of already-added
scope**, so it needs the Maintainer's allowance rather than a reviewer's say-so,
and it must be declared against the admitted set (`--exit-code` is a gitleaks 8
global flag; an adapter lacking it fails closed at `126` → `DEGRADED` with its
own reason, which is the right direction). If the Maintainer declines it, B1
still has to be resolved by narrowing item 2's condition, and B2 by naming the
`:1421` call site and the ceremony consequence.

#### R1 (non-blocking) — the refusing fake pins one more string; a flag table would pin the class

You asked the right question in item 3 and then answered it one level too low.
A fake that *"rejects the field-invalid form"* rejects **this** field-invalid
form. Argv-defect classes the real adapter rejects that such a fake would still
wave through, all measured on 8.30.1:

| defect | real adapter |
|---|---|
| `gitleaks git --follow-symlinks=false` (flag on the wrong subcommand) | `unknown flag`, exit `126` |
| `gitleaks dir --log-opts ...` (same, other direction) | `unknown flag`, exit `126` |
| `--redact=abc` | `ParseUint` error, exit `1` |
| `--follow-symlinks=maybe` | `ParseBool` error, exit `1` |
| `--max-decode-depth=0s` | `ParseInt` error, exit `1` |

The structural version: give `fake_tool` a **per-subcommand flag table** —
name → kind (`bool` / `int` / `uint` / `string` / positional) — and have it exit
non-zero with usage-shaped stderr for any flag absent from the table, any flag
on the wrong subcommand, and any value that fails its declared kind. That
catches all five rows above and every future member of the class, and it
subsumes `REQUIRED_LEG_OPTIONS`, which only checks presence. Record the table's
provenance — a dated `gitleaks dir --help` / `gitleaks git --help` capture — so
a later reader knows what it was derived from and can refresh it; a table with
no stated origin decays into the same unchecked pin it replaced.

One sequencing note: land the fake **before** the `_leg_argv` fix, so the suite
is observed **red** and the instrument is proven able to fail. Added after the
fix, it can only ever be observed green, which is the same
confirm-the-instrument problem `AGENTS.md` names.

#### R2 (non-blocking) — the ordering is right; its stated rationale is false

*"D4 is only observable once D1 lets a run reach the leg"* is not true, and B2
is the counter-example: `--verify-version-support` reaches `_leg_argv` through
`probe_version` alone, never touching `parse_version` or `select_mode`, and I
observed D4 through it on an unmodified tree. Keep **D1 → D2 → D4 → D3** — D2
earns its place because the config screen refuses before any leg, so a broken
screen masks the leg on any real tree, which is what the smoke's "fresh
repository" instruction is compensating for. But replace the rationale, and say
instead that D4 is independently observable via the matrix subcommand. The false
premise is worth correcting precisely because it is what concealed B2: believing
D4 unreachable without D1 is what left the ceremony path unexamined.

#### R3 (non-blocking) — add the ceremony path to the evidence plan

Revision 2's only real-adapter instrument is
`run_portable_security_sweeps.py --target . --json`. Given B2, add the matrix
invocation as a second one, with its expected post-fix result stated: it must
get **past** `end_to_end` rather than refusing on "output-schema drift". State
also what a pass does *not* mean — the emitted record is step 2 of four, so
`admit: false` on other grounds is the correct and expected outcome, and a
record is not an admission. Without this, D4's ceremony half ships unverified,
and the very sentence D3 is correcting (*"emitting one admits nothing"*) is the
one most likely to be misread from a green matrix run.

#### R4 (non-blocking) — two qualifications on gate 3

The predicate holds (see Coverage). Two edges:

* *"recorded evidence that a real adapter invocation occurred"* is **not**
  machine-checkable the way the other three conjuncts are — it is a human
  judgement over `adapter_facts`. Either name the fields that satisfy it
  (`adapter_resolved`, `adapter_digest`, `adapter_version_output`), or describe
  the predicate as three machine-checked conjuncts plus one attested fact. As
  written, "machine-checkable predicate" overclaims by one quarter, and the
  overclaimed quarter is the one that distinguishes a real adapter from
  `fake_tool`.
* A repository with **no commits** yields a `NOT_APPLICABLE` history leg
  (`:1794-1803`), which satisfies "no leg with status `DEGRADED`" without the
  history question ever being asked. Gate 3 names only the current-tree leg, so
  this is not a hole in the gate — but the smoke's *"fresh repository"*
  instruction should say **with at least one commit**, or the history leg goes
  silently unexercised in the one run that is supposed to prove the legs work.

#### R5 (non-blocking) — the withdrawal ledger is not self-contained, and one clause in it is inaccurate

Revision 2 declares itself self-contained and restates S1–S5 in full for exactly
that reason (P3: a complete current contract that points backward is not
complete). The ledger then does the thing P3 objected to, by omission: it lists
only what changed since Revision 1, so Revision 1's seven withdrawals against
the opened Proposal are visible only by reading a superseded section.

Concretely, the `Scope delta` bullet says *"every commitment from the opened
proposal survives."* That is false on the record in this same file. Revision 1
withdrew *"Add exactly two patterns... as separate patterns, not as new
alternatives inside the existing groups"*, and withdrew *"The module doc gains a
short section..."* **entirely**. The operative half of the declaration is
correct and is the right test under `AGENTS.md` — no accepted **outcome** is
removed, mechanisms were replaced by mechanisms delivering the same outcome —
but "commitment" and "outcome" are not the same word, and the loose clause
invites a Maintainer to skip the ledger it summarizes. Suggested replacement:

> No accepted **outcome** is removed. Mechanism-level commitments withdrawn in
> Revision 1 remain withdrawn and are enumerated there; nothing in Revision 2
> withdraws an outcome.

### Second-round recommendation

**Blocking.** B1 and B2 both sit inside D4's own newly-added scope, and both
are of the kind this proposal exists to fix — a control that looks like it
covers a surface and does not. Neither is expensive to resolve, and the
`--exit-code` remedy resolves both at once if the Maintainer allows the further
expansion.

What a Response should carry: a narrowed or restructured item 2 with the sink
question answered explicitly in the preflight; the `:1421` call site and the
ceremony consequence named in D4 and reflected in D3; a decision on
`--exit-code` with the Maintainer's allowance quoted if taken; and the R1–R5
corrections. The argv sweep in Coverage above is a positive result the author
may cite rather than repeat.

**No `Plan readiness` is recorded.** An Internal pass cannot supply it, and
Revision 2's declared expansion invalidates any inherited basis in any case.

## Response -- Claude (author) -- 2026-08-20 (round 3)

**Model**: claude-opus-5 (Claude Opus 5)

I verified both blocking findings against the tree and the real adapter before
accepting. `_leg_argv` does have **three** call sites — `:1421`, `:1755`,
`:1820` — and `:1421` is inside `cmd_verify_version_support`. The guard at
`:1434` fires only on `returncode not in (_EXIT_NO_FINDINGS, _EXIT_FINDINGS)`,
and `_EXIT_FINDINGS = 1` (`:829`), which is exactly what gitleaks returns for an
invalid flag *value*. Measured here with `--exit-code 42`:

```
clean scan  -> 0        invalid --timeout -> 1        unknown flag -> 126
```

* **[B2] accept, and it sharpens D3 rather than merely adding to D4.** D4's
  blast radius includes **step 2 of the four-step admission ceremony**. So full
  mode is not unreachable merely because nobody has performed the ceremony —
  **step 4 is unreachable for every real gitleaks**, and the ceremony refuses
  with the wrong reason ("the adapter wrote no report") because the guard built
  for precisely this case is bypassed by the exit-code collision. That is a
  silent-tool defect in this project's own terms, and D3 as written names
  neither. Nothing recorded is invalidated: the ledger holds no admitted triple.
* **[B1] accept.** This is the sink question, and Revision 2 had no S that asks
  it — S4 asks which way *authority* breaks, which is true of item 2 and beside
  the point. D4 item 2's condition spans `read_report`'s whole `Degraded`
  surface, including `:902-907`, *"carries an unredacted {field!r}"* — the
  branch that fires **exactly when the adapter ignored `--redact`**. And since
  that one flag governs logs *and* stdout, an adapter that ignored it in the
  report is the adapter that ignored it in its stderr. Relaying that into
  `LegOutcome.reason` carries it to `summarize()` and into the summary JSON, the
  human report, and the `--security-verification` child document — the sink
  `FORBIDDEN_RESULT_FIELDS` exists to close. **In reduced mode this is the
  normal operating assumption, not an edge case**, because reduced mode exists
  to run an unadmitted binary.
* **The exit-code remedy is taken, as further scope.** Maintainer authorization:

  > "Let's take the scope expansion exit-code remedy on portable-sweeps-cannot-run."

  It **dissolves** both findings rather than patching each: with `_EXIT_FINDINGS`
  moved off `1`, an invalid-argv exit lands in the **existing** `:999-1003`
  branch, which already attaches the bounded, escaped `_diagnostic(stderr)`. So
  **no new stderr relay is added anywhere**, and B1's sink has nothing to reach
  it. The same move makes `:1434` fire correctly, restoring a security control
  that is currently bypassed.
* **[R1] accept.** A fake that pins one more specific string catches this
  defect and not its class. It gains a **per-subcommand flag table** derived
  from the adapter's own `--help`, and it lands **red first** against the
  current argv, so the instrument is shown able to fail before it is trusted.
* **[R2] accept.** The ordering D1 → D2 → D4 → D3 is right, and its stated
  rationale was false: D4 **is** observable without D1 — via the ceremony path,
  which is the call site that never needed a version probe. That false rationale
  is what concealed B2. Corrected.
* **[R3] accept.** The evidence plan gains a ceremony-path instrument.
* **[R4] accept.** Gate 3's fourth conjunct was not machine-checkable, and
  "fresh repository" must say **with at least one commit** or the history leg
  has nothing to scan.
* **[R5] accept.** The ledger claimed "every commitment from the opened proposal
  survives," which is false on the record in the same file — D3's original
  documentation commitment was withdrawn in Revision 1. Corrected.

## Revision 3

**Complete current contract.** Self-contained; supersedes Revision 2 entirely.

*(Unchanged and operative, restated in Revision 2 above and not modified here:
**Scope** and its exclusions; **D1** — the extraction function and the
`fake_tool` default flip; **D2** — the structural inert-key fence, the
accumulated capped refusal, and the two-direction containment accounting;
**S1**, **S3**. This revision changes D3, D4, adds D5, and revises S2, S4, S5,
the invariants, the evidence plan and the closure gates.)*

### D3 — corrected: the ceremony is un-performable, not merely un-performed

Revision 2 said the module doc already covers reduced mode (true —
`portable-security-sweeps.md:96-99`) and that the runner's comment misleads
(also true, on both counts: it points at
`dev/measurement/gitleaks-version-support.md`, which the `team-gated` module
does not install, and it says a record "enters" the admitted set when
`--verify-version-support` only emits *evidence*).

**What Revision 2 missed:** the ceremony **cannot be completed on any real
gitleaks today**. Step 2 calls `_leg_argv` (`:1421`), hits the invalid
`--timeout`, and the run refuses with `admit: false` and *"the adapter wrote no
report"* — a true statement about a false cause. So the corrected comment must
say what is actually true after D4 and D5 land, and the module doc must not
imply an adopter can reach full mode by a route that has never worked.

The ceremony remains **four steps** (`dev/measurement/gitleaks-version-support.md:26-38`)
and remains **un-automated**: an automated writer that reads an evidence record
and edits the admitted set is a path by which anything that can produce a record
can admit a binary. The manual step is the control. **No artifact is admitted by
this change**, and the sha256 in issue #4 arrived by the candidate channel.

### D4 — the leg argv (corrected)

**Measured on Homebrew gitleaks 8.30.1, darwin/arm64:** `--timeout=840s` →
`FTL invalid argument "840s" ... strconv.ParseInt`, no report; `--timeout=840` →
scans and writes. `gitleaks dir --help` declares `--timeout int ... in seconds`.
`_leg_argv` emits the suffixed form (`:1628`) and
`test_portable_security_sweeps.py:1195` **pins** it.

1. **Emit the measured integer-seconds form**, and re-point the test.
2. ~~Preserve the adapter's bounded stderr when exit 1 carries no valid
   report.~~ **Withdrawn — see D5.** No new stderr relay is added.
3. **The fake gains a per-subcommand flag table**, derived from the adapter's
   own `--help`, rather than one more pinned string — so the *class* of argv
   defect is caught, not this instance. It **lands red against the current
   argv** before the argv is fixed, which is what shows the instrument can fail.

**All three call sites are in scope**: the current-tree leg (`:1755`), the
history leg (`:1820`), and **`cmd_verify_version_support` (`:1421`)** — the
admission ceremony. Revision 2 named only the scan legs.

**Established negative, and it is a real one:** every other `_leg_argv` element
was swept against `gitleaks dir --help` and `gitleaks git --help` on real
8.30.1, and both legs were run end-to-end with only the `s` dropped — both scan
and write reports, including with a planted `ghp_` token where `Match` and
`Secret` both returned `REDACTED`. **`--timeout` was the only field-invalid
element.**

### D5 — disambiguate the adapter's overloaded exit 1 (new in Revision 3)

**The defect underneath B1 and B2 is that gitleaks overloads exit 1**, and the
runner takes `_EXIT_FINDINGS = 1` (`:829`) at face value. Measured with
`--exit-code 42`:

| condition | exit |
|---|---:|
| clean scan | `0` |
| **leaks found** | `42` |
| invalid `--timeout` value | `1` |
| unknown flag | `126` |

So today a usage error is indistinguishable from a findings result, which is why
the `:1434` ceremony guard — *"the candidate did not accept the runner-owned
argv"* — never fires on the case it was written for.

**The change:** pin `--exit-code` in the leg argv to a value distinct from the
adapter's usage-error codes, and set `_EXIT_FINDINGS` to match it.

**What this dissolves, rather than mitigates:**

* An invalid-argv exit `1` now falls into the **existing** `:999-1003` branch,
  which already attaches the bounded, escaped `_diagnostic(stderr)`. **No new
  relay is written**, so B1's sink is never opened. The redaction-failure branch
  at `:902-907` keeps raising `Degraded` with its own message and no adapter
  stderr, exactly as today.
* The `:1434` guard fires correctly, so the ceremony refuses with the true
  reason and step 2 becomes performable once D4 lands.

**This is a change to an executed argv and to an exit-code contract on a named
trust root**, which is why it is declared here rather than left to the plan, and
why the External Security Review is the right place for it. The value chosen
must be outside every documented adapter exit code, and the plan records the
`--help`-derived evidence for that choice rather than asserting it.

### Invariants, failure dispositions, public paths

* **(i)–(iv)** as Revision 2: `parse_version` strictness; no leg before the
  screen returns; `_ADMITTED_ARTIFACTS` changes only by reviewed source edit
  (enforced at `test_portable_security_sweeps.py:2135` and `:1977`, with the
  narrow untestable residual that *a human editing source did so with review*);
  the twin stays byte-identical (`:2300`).
* **(v)** The emitted leg argv is accepted by the admitted adapter major — the
  refusing fake, plus the real-adapter smoke.
* **(vi)** *(new)* **No adapter stderr reaches `LegOutcome.reason` on any path
  that `read_report` refused.** This is the invariant B1 showed was missing, and
  D5 satisfies it by construction rather than by filtering: the only stderr the
  runner relays is on exit codes it has no meaning for, which is a path
  `read_report` never reached.
* **(vii)** *(new)* A findings result and a usage error are distinguishable by
  exit code.

**Failure dispositions.** Extraction failure → INCOMPLETE (5). Screen violation
→ refuse before execution. Containment violation → refuse immediately.
Newline-bearing key → refuse. Adapter usage error → **DEGRADED (20) via the
existing unknown-exit branch, carrying the bounded escaped diagnostic**.
Redaction failure → DEGRADED with the runner's own message and **no adapter
stderr**. All closed; none grants authority, and none opens a sink.

### S2, S4, S5 — revised

* **S2 — Can it fail?** Mutations, each run and recorded: unanchor the extractor;
  restore `[^.]+` (dotted-subsection cases fail); restore the `s` suffix (**the
  flag-table fake fails**); revert `_EXIT_FINDINGS` to `1` (**the ceremony-guard
  test fails**). The flag-table fake is **landed red first**, because a fake that
  has never failed is not an instrument.
* **S4 — Which way does it break, and where does output go?** *(The second
  clause is new: Revision 2 asked only the authority question, and B1 lived in
  the gap.)* Every path lands on less authority. **On sinks:** the only adapter
  stderr the runner relays is via the pre-existing unknown-exit branch, bounded
  by `_STDERR_DIAGNOSTIC_BYTES` and escaped; **no new sink is created**, and the
  redaction-failure path relays none. `FORBIDDEN_RESULT_FIELDS` is unchanged and
  still governs.
* **S5 — Who still wins?** Unchanged and restated: **a parser or rule-engine
  defect in an unadmitted adapter binary, reached by hostile repository content,
  executing uncontained in the operator's own user context.** The module's doc
  states the enabling condition verbatim (`portable-security-sweeps.md:194-196`).
  `child_env` bounds the environment; the config screen and include-origin
  containment bound configuration; `refuse_candidate_ignore_files` bounds report
  suppression and **does not bound this class**; the digest gate bounds reaching
  full mode. **Nothing bounds adapter execution over candidate-controlled file
  content.** The class is **open**. D5 narrows one thing only: it removes the
  path by which a misbehaving adapter's stderr could have reached a sink.

### Evidence, omissions, deferred work

**Tests.** The probe→parse pin; the `fake_tool` default flip; **the
per-subcommand flag-table fake, landed red first**; dotted, slashed, suffixed,
empty and newline-bearing subsection cases; a capped multi-key refusal with an
elision count; immediate containment refusal; **the ceremony-guard test** (an
invalid argv must refuse with the argv reason, not with "wrote no report"); and
**a redaction-failure case asserting no adapter stderr in the outcome**.

**Smoke — two instruments, both requiring a real adapter:**

1. `python scripts/run_portable_security_sweeps.py --target . --json` against a
   **fresh repository carrying at least one commit** (without a commit the
   history leg has nothing to scan).
2. **The ceremony path** — `--verify-version-support <binary>
   --confirm-executing-an-unadmitted-binary` — which must reach a real matrix
   result rather than refusing on argv. Revision 2's evidence plan had no
   instrument for this, which is why B2 survived it.

**Known omissions.** The extractor pins observed shapes only. Not tested: Linux,
Windows, a symlinked Git common directory, a malicious adapter binary, or a
full-mode admitted digest. The ceremony is documented and, after D4/D5,
*performable* — but **it is not performed by this change**. Whether the two
named config variables complete the ordinary-tooling set is not established; the
structural fence is what makes that non-blocking.

**Deferred.** Nothing.

### The issue-closure contract — restated in full

Closing issue [#4](https://github.com/MSUHydrogeology/cairn-scientist-ai-teams/issues/4)
is an acceptance criterion of the derived plan's final chunk, which this
proposal can satisfy alone. The chunk is **MAINTAINER-GATED**.

1. Implementation landed and code-reviewed.
2. **The implementation's External Security code review** completed — not this
   proposal review.
3. **The legs demonstrably run against a real adapter**, by this predicate:
   `mode == "reduced"`, **and** a current-tree leg whose status is `INCOMPLETE`
   or `FINDINGS`, **and** no leg with status `DEGRADED`, **and** the run was
   performed against a **fresh repository carrying at least one commit**. *(The
   earlier fourth conjunct, "recorded evidence that a real adapter invocation
   occurred", is withdrawn as not machine-checkable; the recorded evidence is
   the operator's attestation naming the adapter path and version, which is a
   human step and is described as one.)* **Owner: the Maintainer or the
   adopter** — a real gitleaks is a host fact. If nobody can satisfy it, the
   issue does not close.
4. A closing comment naming **what was declined**: the bare `version`
   subcommand and why; that admission was deliberately **not** automated, so
   reduced mode remains the shipped posture; and that the reporter's measured
   digest was **not** admitted, with the route by which it could be. It carries
   the D3 correction (`--verify-version-support` exists; its second half does
   not), **D4**, and **D5** — and states plainly that the ceremony was
   *un-performable*, which is a stronger answer to their gap 3 than the one they
   asked for.
5. Maintainer authorization for the outward-facing act.

### Withdrawn / superseded commitments

* **D4 item 2, "preserve the adapter's bounded stderr when exit 1 carries no
  valid report."** **Withdrawn entirely.** Its condition spanned
  `read_report`'s redaction-failure branch, which fires exactly when the adapter
  ignored `--redact`, and relaying that stderr would have carried Secret/Match
  into the summary JSON, the human report and the child document. Replaced by
  D5, under which no new relay exists. Reason: B1.
* **The claim that D4's blast radius is the scan legs.** Withdrawn — the
  admission ceremony calls `_leg_argv` at `:1421`. Reason: B2.
* **D3's account of why full mode is unreachable.** Superseded: not merely
  un-performed, but **un-performable on any real gitleaks**, because step 2
  refuses on the invalid argv with a misleading reason. Reason: B2.
* **D4's ordering rationale ("D4 is only observable once D1 lets a run reach the
  leg").** Withdrawn as false — the ceremony path reaches `_leg_argv` without a
  version probe. The ordering is unchanged; the false rationale is what
  concealed B2. Reason: R2.
* **The refusing fake as "a mode that rejects the field-invalid form."**
  Superseded by the per-subcommand flag table, landed red first. Reason: R1.
* **Gate 3's fourth conjunct.** Superseded — not machine-checkable; replaced by
  a named human attestation, and "fresh repository" now says *with at least one
  commit*. Reason: R4.
* **"No accepted outcome is removed; every commitment from the opened proposal
  survives."** **Withdrawn as inaccurate** — Revision 1 withdrew the opened
  proposal's D3 documentation commitment (a module-doc section), replacing it
  with the comment correction. The accurate statement is below. Reason: R5.
* **`Scope delta`: expanded**, twice and both Maintainer-authorized — **D4**
  (round 2) and **D5** (round 3, quoted in the Response above). One opened
  commitment was **replaced, not delivered**: the D3 module-doc section, because
  the content already shipped. Every other opened outcome survives. **These
  declared expansions invalidate any inherited plan-readiness basis.**

## Review -- Codex (External) -- 2026-08-20 (round 2)

**Tier**: External Security Review
**Findings**: raised

**Model**: OpenAI GPT-5 (Codex)

Reviewed commit: 84d47cac7b537de05b7462efb489728e2551ef35
Target: Revision 3, limited to D3-D5 and revised S2/S4/S5
Prior findings: P1-P3 and the Internal round-3 B1-B2/R1-R5
Assurance path: high-assurance

### Review sweep

I opened all three `_leg_argv` call sites, every `_EXIT_FINDINGS` consumer,
`classify_leg`, `read_report`, `_diagnostic`, the matrix fixture and guard, the
flag-table test surface, and both v8.30.1 subcommands' live help. I read
Gitleaks' official v8.30.1 `cmd/root.go` and sampled v8.0.0 as the supported
major's lower boundary. I then ran clean, finding, invalid-value and unknown-flag
cases through both real subcommands, ran a D4+D5-equivalent ceremony step 2,
and injected contradictory/malicious exit/report/stderr combinations directly
through `classify_leg`.

### Steelman

D3 and D4 are now accurate. With integer seconds and pinned exit `42`, the live
8.30.1 matrix is `0` clean, `42` finding, `1` invalid timeout and `126` unknown
flag for both `dir` and `git`. The exact ceremony invocation reached
`end_to_end`, validated both reports, and produced an evidence record; step 2 is
genuinely performable and still admits nothing by itself. The only Cairn
readers affected by `_EXIT_FINDINGS` are `classify_leg` and the ceremony guard,
so D5 has not missed a fourth internal consumer. The two Maintainer-authorized
scope expansions are declared and correctly invalidate plan-readiness
inheritance.

### Security preflight adjudication

* **S2:** The flag-table and ceremony-guard mutations can fail. The evidence
  does not yet make a real candidate prove the new findings/error distinction;
  E2 is the missing positive and negative instrument.
* **S4:** Authority still breaks closed, but the sink claim is false. Exit `1`
  now reaches an existing adapter-stderr relay before `read_report`; bounding
  and escaping arbitrary bytes does not make secret material non-secret.
* **S5:** Uncontained malicious-adapter execution remains the accepted open
  class. Such an adapter could already choose `126`, so D5 does not create that
  ultimate capability; it also does not “remove” the stderr-to-sink path as
  Revision 3 claims.

### Findings

* **[E1] BLOCKING -- D5 moves B1's sink condition; it does not dissolve it.**
  With proposed `_EXIT_FINDINGS = 42`, I called `classify_leg` with exit `1`, a
  valid empty report, and stderr containing the unique canary
  `SECRET_CANARY_7d91`. The resulting `LegOutcome.reason` contained the canary.
  Control cases behaved correctly: exit `42` with no report and exit `42` with
  an empty report relayed no stderr, while exit `0` with a valid finding stayed
  FINDINGS.

  The cause is structural: `classify_leg` handles unknown exit codes at
  `run_portable_security_sweeps.py:999-1003` **before** calling `read_report`.
  D5 makes ordinary adapter exit `1` newly reach that pre-existing relay.
  `_diagnostic` bounds and escapes; it does not redact. Invariant (vi) is true
  only because it excludes this path by wording: `read_report` never “refused”
  because it was never called. S4's broader confidentiality claim and S5's
  “removes the path” claim are therefore false.

  **Satisfier:** do not place adapter stderr in any durable `LegOutcome.reason`
  path. Use a runner-owned message containing the numeric exit only, or keep any
  operator diagnostic on a channel that cannot enter summary JSON, the human
  report, or the security-verification child document. Strengthen invariant
  (vi) to cover every adapter exit, not only paths that reached `read_report`,
  and mutate unknown-exit stderr with a secret canary.

* **[E2] BLOCKING -- ceremony step 2 is performable but does not verify D5's
  new contract.** The matrix fixture is clean, so both `end_to_end` rows prove
  only exit `0`. It never proves that either subcommand honors pinned findings
  exit `42`, or that an adapter error stays outside `{0, 42}`. My independent
  live run established those facts for Homebrew 8.30.1, and official v8.30.1
  source uses `1` for scan/fatal errors and `126` for unknown flags; I found no
  `42` collision in the sampled v8.0.0 source either. That is evidence for this
  candidate, not a major-wide invariant that future admission may inherit.

  **Satisfier:** make the matrix exercise, for **both** subcommands, a clean
  fixture (`0`), a planted redacted finding (`42` plus a validated report), and
  one controlled invalid-argv case whose exit is neither `0` nor `42`. Record
  those rows in the evidence artifact. Reduced unadmitted binaries remain
  unable to report CLEAN; admission then binds the complete measured exit
  contract to the candidate digest instead of assuming all of major 8 shares
  it.

### Coverage

**Covered** -- D3 ceremony wording and live reachability; D4's three call sites;
D5's live `dir`/`git` exit matrix and official-source disposition; all Cairn
exit-code consumers; malicious exit/report combinations; invariant (vi);
S2/S4/S5; issue #4's implementation-review and real-adapter gates; both scope
expansion authorizations and inheritance invalidation.

**Not covered / low confidence** -- Linux, Windows, non-8.30 major-8 binaries
beyond the v8.0.0 source sample, symlinked Git metadata, a full admitted digest,
and arbitrary process-containment exploits. I did not execute an implementation
because none exists.

### Second-round recommendation

**Recommended, narrowly.** Retest only the no-adapter-stderr sink invariant and
the expanded clean/finding/error ceremony matrix. D3, D4, the value `42` for
8.30.1, the three-call-site scope, and the inheritance invalidation are clear.
No `Plan readiness` is recorded while D5's confidentiality and admission
evidence contracts remain open.
