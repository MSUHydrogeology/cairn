# A scanner's imperative must name the set it audited

**Author**: Claude (Strategy)
**Model**: claude-opus-5 (Claude Opus 5)
**Date opened**: 2026-08-20
**Status**: revising
**Assurance path**: **high-assurance** — D1 changes what a security control
**instructs an operator to do to a reviewed security baseline**, and D2 adds a
derived annotation to a security report. Neither is obviously a trust-boundary
change; uncertainty resolves to high-assurance.
**Touches**: `scripts/content_scan_runner.py` and its byte-identical twin
`templates/modules/team-gated/content_scan_runner.py` (verified identical,
`as_of 2026-08-20`); `templates/modules/team-gated/python-security.md`;
`templates/modules/team-gated/run_security_audit.py`;
`bootstrap/tests/test_security_stack.py`. **No change to any exit code, to what
is scanned, to what is reported, or to the residual baseline's contents.**
**Related**: adopter issues
[#5](https://github.com/MSUHydrogeology/cairn-scientist-ai-teams/issues/5)
(gap 3) and
[#6](https://github.com/MSUHydrogeology/cairn-scientist-ai-teams/issues/6).
Siblings opened the same day:
[`2026-08-20-claude-portable-sweeps-cannot-run`](2026-08-20-claude-portable-sweeps-cannot-run.md),
[`2026-08-20-claude-adopt-into-existing-tree`](2026-08-20-claude-adopt-into-existing-tree.md).
**Plan review**: required(**Internal**) — an Internal proposal review spends no
different-agent-type read, so no `Plan readiness` inheritance is claimed. **No
Security Review trigger**: no trust boundary is added, moved or widened, and no
verdict changes. D2's annotation carries a bright line (below) whose violation
*would* change that; the reviewer should check it.

## Context

Two adopter reports, filed separately, are **one defect shape**: a control makes
a claim — or issues an imperative — over a set **wider or narrower than the one
it actually audited**, and the reader cannot tell which. In both cases the
consequence is the one the adopter names three separate times in their own
words: a control whose output people learn to skim has stopped being a control.

### D1 — exit 3 tells an operator to prune a shared security baseline

`content_scan_runner.py` prints, on its stale-baseline class
(`scripts/content_scan_runner.py:594-595`):

```
result: STALE baseline authority (15 entr(y/ies)) -- FAILS (prune the residual baseline).
```

**The detection is right and stays.** A reviewed-residual entry with no live
occurrence can preauthorize a replay, and that is a real fail-closed class
(`scripts/content_scan_runner.py:37-38`).

**The scope of the imperative is wrong.** The runner audits a set defined by
`content_scan_roots.txt`, and concludes about the whole baseline. On the
adopter's mixed tree the upgraded runner called all 15 entries stale while
`run_security_audit.py` found all 15 live. They followed the instruction, pruned,
and their own contract test caught it. Restored.

**The baseline demonstrably has more than one consumer.** Measured at `a26a180`
(`as_of 2026-08-20`), `content_scan_residuals.txt` is read by
`scripts/content_scan_runner.py`,
`templates/modules/team-gated/run_security_audit.py`,
`bootstrap/_scaffold/config.py`, and `bootstrap/tests/test_security_stack.py`.
So "prune the residual baseline" is a **security-relevant imperative, worded
authoritatively, issued by one consumer about a shared reviewed artifact** on
evidence that covers only its own audited set.

The adopter correctly notes the disagreement is downstream of the silent-keep
defect drafted in
[`2026-08-20-claude-adopt-into-existing-tree`](2026-08-20-claude-adopt-into-existing-tree.md)
— two scanners from different upstreams. **It still needs fixing independently:**
that proposal stops the mixed tree, but an imperative that overreaches its
audited set is wrong on a clean tree too. It just stops getting caught.

### D2 — the pip-audit leg audits the environment; the adopter reads it as the project

Measured by the adopter on a scientific Python library in a conda environment:

| | count |
|---|---:|
| distributions discoverable in the environment | 299 |
| in the adopter's declared dependency closure | 93 |
| **outside the adopter's scope** | **212 (71%)** |
| vulnerabilities reported over the ambient environment | 144 across 21 packages |
| **reachable from a declared runtime dependency** | **27 across 2 packages** |

Both reachable findings were transitive and one patch release behind
(`flopy → matplotlib → pillow`, `rasterio → click`).

**The design is correct and this proposal does not weaken it.** `pip_audit_argv`'s
docstring (`templates/modules/team-gated/run_security_audit.py:808-816`) says a
narrowed claim over an ambient environment is exactly as false as a wide one,
and the adopter agrees in writing. The ambient audit answers *"is the environment
I execute in vulnerable?"*, which is the right question for a self-audit
tripwire.

The problem is **actionability at a 5:1 ratio**, in an environment shape Cairn's
stated audience makes the *common* case: a conda scientific stack widens the
gap between "the env" and "the project" far past a venv-per-project workflow.

**The module doc discloses the opposite direction, and only that one.**
`templates/modules/team-gated/python-security.md:35-52` — *"Declared scope — what
the dependency check covers"* — is careful and good about the **coverage floor**:
what the leg does *not* audit (conda-managed native packages, OS packages,
vendored libraries), and that the excess is concentrated in the native layer.
Nothing states the **coverage ceiling**: that most of what it *does* report is
not yours. An adopter who reads that section comes away expecting
under-coverage and meets over-reporting.

## Proposal

### The rule both fixes instantiate

**A control that reports a finding, or instructs an operator to mutate a shared
reviewed artifact, names the set its conclusion is drawn from — in the same
output as the claim, not in a doc the reader may not have open.**

This is stated here and written into the two docstrings and the module doc where
these controls live. It is **not** proposed as an `AGENTS.md` doctrine rule —
see *Documentation / doctrine surface*.

### D1 — scope the imperative to the audited set

Three changes, none of which touches behaviour, exit codes, or the baseline:

1. **Scope the sentence.** The stale-entry message says which roots were
   audited, that an entry with no occurrence *in that set* may still be live
   elsewhere, and that the operator confirms across consumers before pruning.
2. **Name the audited set in the output**, so the claim is checkable rather than
   merely hedged. The roots manifest is already loaded — this is printing what
   the runner already knows.
3. **Say what the exit-3 class means** in one line: it is a fail-closed signal
   that the baseline and this scan disagree, not a verdict that the baseline is
   wrong.

Exit 3 still fires, over the same condition, with the same disposition.

### D2 — document the ratio, and annotate reachability

Take the adopter's options **1 and 3. Explicitly not 2.**

**(1) Document the ceiling** — a second paragraph in the existing *Declared
scope* section, which already does this job well in the other direction: the leg
audits the environment, in a conda workflow this will substantially exceed the
project's own closure, and triage starts from reachability. It belongs beside
the floor disclosure, not in a new section.

**(3) Annotate reachability** on the existing output: mark each finding
*reachable* / *not reachable* / *unknown* with respect to the declared closure.
One leg, one claim, audited set unchanged, triage axis added.

**The bright line, and it is testable.** The annotation is derived from the same
closure walk the adopter warns is fiddly, so **it can be wrong**. That is
tolerable for an *annotation* and not for a *leg*, precisely because it changes
no verdict: every finding is reported either way, exit codes are untouched, and
a mis-annotation costs triage *order*, not coverage. **If the annotation ever
gates what is reported, option 3 has collapsed into option 2 and must be
refused.** A test asserts that the reported finding set is byte-identical with
annotation on and off.

**Failure disposition:** if the closure cannot be computed, annotate every
finding `unknown` and say so in the report. Never silently drop the axis, never
omit a finding, never fail the leg on it.

### Documentation / doctrine surface

`templates/modules/team-gated/python-security.md` (descriptive layer — the
module's own doc) and two docstrings.

**No doctrine rule change, deliberately.** The generalization — *a scanner's
imperative names the set it audited* — has enough recurrence to clear the
rate-limit gate (four instances in one day's reports, counting this proposal's
two, the archive-sweep advice, and the one-key-at-a-time refusal). It is still
**not** proposed as doctrine here, for two reasons: the principle is already
stated, correctly, in the docstrings of the tools that hold it, so the marginal
value of a governing-layer rule is low; and a governing rule generalized from a
single adopter's single report is the churn the gate exists to prevent, whoever
files it. If it recurs on a surface the docstrings do not reach, that is the
goodnight-synthesis path.

**This proposal does not edit `dev/PLANNING.md`** — the roadmap is a shared
communication file edited at defined serialization points, and opening a
proposal is not one. Filing the doctrine candidate there is a Maintainer or
goodnight-time act.

## Rationale

**Which user workflow this improves:** acting on a security report. D1 stops a
control from confidently instructing an operator to damage a shared baseline.
D2 lets an adopter triage 144 findings without first building the scoping
themselves — which is what this adopter actually did.

**What contract it preserves:** every one. No exit code, audited set, reported
finding, or baseline entry changes. The ambient claim stays exactly as wide as
it is.

**Why now:** D1 has already caused an operator to prune a security allowlist and
be saved by a test they happened to have. D2 is the difference between a control
that is read and one that is skimmed, on the environment shape Cairn's audience
actually runs.

## Alternatives considered

* **D1: establish sole-consumership** — have the runner assert it is the only
  reader and prune with authority. **Falsified, not merely rejected:** the
  baseline has four readers today (measured above). Even if it had one, the
  assertion is a claim about other tools that ages the moment a fifth arrives —
  closed by enumeration, which is the weaker kind.
* **D1: drop exit 3 entirely.** Rejected: a residual entry that can preauthorize
  a replay is a real class, and this is a wording defect, not a detection one.
* **D1: keep the wording and fix only the mixed tree** (via the sibling
  proposal). Rejected: it makes the symptom rare rather than the imperative
  correct, so the next occurrence is harder to catch, not easier.
* **D2 option 2: a second declared-closure leg.** Rejected, on the adopter's own
  argument against their own suggestion. They built the closure by hand and it
  produced junk from environment-marker parsing (`cffi~`, `mdurl~`), needed care
  to skip `; extra ==` requirements without dropping genuine ones, and hit
  normalization (`Pillow` vs `pillow`). **A second *leg* implies a second claim
  of the same standing as the ambient one**, and a claim resting on a resolver
  this fragile does not deserve that standing. The same fragility is acceptable
  in an annotation, which is why 3 is in and 2 is out.
* **D2: narrow the audited set to the declared closure.** Rejected — this is the
  one thing the design explicitly forbids, and the adopter agrees.
* **Do nothing.** Both controls remain correct and unactionable, which is the
  state that ends with them switched off.

## Evidence / verification plan

### Author-accounting — invariants, failure modes, edge cases

* **Invariants.** (i) The reported finding set is **identical** with the D2
  annotation present and absent — the bright line, enforced by a test comparing
  both runs. (ii) Exit codes are unchanged across every D1 and D2 path —
  enforced by the existing exit-contract tests, unmodified. (iii) The residual
  baseline is never written by either tool — it is read-only to both today and
  stays so.
* **Failure modes.** Closure computation fails → all findings `unknown`, report
  says so, leg still succeeds (**open, and intentionally**: an annotation that
  can fail a security leg is worse than no annotation). Roots manifest
  unreadable → the existing exit-2 fail-closed path, unchanged. Stale entries
  detected → exit 3 as today, with a scoped sentence.
* **Edge cases.** Zero stale entries (no message); every entry stale; a
  distribution in the closure but absent from the environment; a distribution in
  the environment in nobody's closure (the 71% case); an extras-only
  requirement; a marker-gated requirement; a case-normalization pair
  (`Pillow`/`pillow`); a closure of size zero.
* **Public-path → test mapping.** `run_content_scan` and the exit-3 path, plus
  the pip-audit leg's report assembly, through their real entry points in
  [`test_security_stack.py`](../../bootstrap/tests/test_security_stack.py).
* **Known omissions.** The annotation's *accuracy* is not claimed to be
  complete — only that it is honest about `unknown` and that it gates nothing.
  Whether the four measured baseline consumers are the complete set is
  established for this tree at this commit, not in general.

#### Security preflight — five questions

* **S1 — Who supplied it?** D1 adds no input; it prints what the runner already
  read. D2's annotation consumes distribution metadata from the audited
  environment — the same source the leg already audits, and already untrusted in
  the sense that matters: it is *described* by the packages, not verified. That
  is acceptable **only because the annotation decides nothing**; if it ever
  gates reporting, this answer changes and the design must be refused.
* **S2 — Can it fail?** For the bright-line test: make the annotation filter the
  finding list, and the identical-set assertion must redden. For the `unknown`
  disposition: force the closure walk to raise, and a test asserting every
  finding is present-and-`unknown` must pass while a test asserting no findings
  were dropped also passes. Both mutations run and are recorded. **The
  identical-set test must be shown to fail under the filtering mutation** — an
  assertion derived from the same list it checks cannot fail.
* **S3 — What fires it, over what?** `python -m pytest bootstrap/tests/test_security_stack.py`
  for the tests; `python scripts/content_scan_runner.py` and
  `python scripts/run_security_audit.py` are the operator-run entry points. No
  CI, no hook, no gate runs either — Cairn has no CI, and the plan must not
  write otherwise. The module doc's description of each must be quoted and shown
  to agree with what the command does.
* **S4 — Which way does it break?** D1's rewording lands on *less* operator
  authority — it asks for confirmation before a destructive prune where it
  previously instructed one. D2's failure lands on `unknown`, which is less
  claim, not more. Neither adds authority anywhere.
* **S5 — Who still wins?** Assumes an attacker who can influence package
  metadata in the audited environment. After this change they can make a finding
  annotate as *not reachable* and be triaged last — **they cannot make it
  disappear**, which is exactly what the bright line buys and why it is worth
  testing rather than asserting. Closed by construction (the annotation is
  additive), not by enumeration. What remains open, and is unchanged: an
  operator who prunes the baseline anyway.

### Tests required

`bootstrap/tests/test_security_stack.py` — the identical-set invariant, the
`unknown` disposition, the exit-code invariance, and the D1 message scoping.
Per the adopter's caution, the closure fixtures are **messy by construction**:
an extras-marked requirement, a marker-gated requirement, a
case-normalization pair, and a distribution in nobody's closure. A tidy fixture
would pass without exercising anything the adopter actually hit.

### Examples / smoke checks

`python scripts/content_scan_runner.py` and `python scripts/run_security_audit.py`
on this tree — both are the operator paths that produced the reports.
`python scripts/check_cairn.py` for the module-doc edit. **N/A**: the example
gallery and the scaffold dry-run do not reach either tool.

## Signals the change is wrong

* **The annotation is trusted as a verdict.** Symptom: anyone — adopter, agent,
  or a later change — treating *not reachable* as *not a problem*, or a proposal
  suggesting the leg skip unreachable findings. Recovery: the identical-set test
  is the fence; if the *social* pressure to filter proves stronger than the
  test, remove the annotation rather than let it drift into option 2.
* **`unknown` becomes the common case.** If the closure walk fails often enough
  that most findings annotate `unknown`, the axis is noise and should be removed
  — the honest failure is still a failure. Threshold worth measuring in the
  plan rather than asserting here.
* **The scoped D1 message is read as permission to ignore exit 3.** Symptom: an
  operator concluding the disagreement is fine because it might be another
  consumer's entry. The sentence must ask for confirmation, not offer an excuse;
  if it reads as the latter, tighten the wording, not the detection.
* **A fifth baseline consumer appears and disagrees differently.** That is
  evidence the shared-artifact problem is structural and wants a real
  multi-consumer protocol — a distinct proposal, not a further reword.

## Amendment -- Claude (author) -- 2026-08-20 -- issue closure is in scope

**Model**: claude-opus-5 (Claude Opus 5)

Appended, not merged into the sections above, per the append-only rule. This
records Maintainer direction received **after this proposal was committed
(`3499fc5`) and before any review**. It **adds** a deliverable; it withdraws
nothing, so no `Scope delta` is owed (scope as opened is `preserved`).

### 1. What was directed

> "please make sure that these proposals all include closing the issues"

### 2. What this proposal can close, and what it cannot

**It closes adopter issue
[#6](https://github.com/MSUHydrogeology/cairn-scientist-ai-teams/issues/6)
alone** — D2 is the whole of it.

**It holds the last piece of issue
[#5](https://github.com/MSUHydrogeology/cairn-scientist-ai-teams/issues/5), and
cannot close it alone.** Gap 3 is D1 here; gaps 1 and 2 are in
[`2026-08-20-claude-adopt-into-existing-tree`](2026-08-20-claude-adopt-into-existing-tree.md).
Issue #5 closes **only when both proposals have landed**, and the closing
comment names which proposal took which gap — the adopter offered the split
(*"Happy to file separately if that suits triage better"*), so it is owed an
answer rather than a silent regrouping.

The failure this guards against: this proposal lands, D1 is genuinely fixed, and
a close gets posted for #5 on the strength of the gap the closer happened to be
holding. Whichever of the two lands second carries the close; whichever lands
first posts a progress comment and leaves the issue open.

### 3. The gate and the honesty bar

Each close is an acceptance criterion of the derived plan's final chunk, gated
on implementation landed and code-reviewed, a closing comment meeting *4*, and
**Maintainer authorization** — a close publishes a public claim that the problem
is resolved. The chunk is **MAINTAINER-GATED**.

### 4. The closing comment must name what was declined — and here it matters most

Issue #6 is the one report where the adopter offered three shapes and **this
proposal refuses their middle one**. A close that lists what shipped without
saying that is the least honest of the four.

The comment states:

* that **options 1 and 3 were taken and option 2 was refused**, and that the
  refusal rests on **their own caution** about the closure walk — the junk from
  environment-marker parsing, the `; extra ==` handling, the `Pillow`/`pillow`
  normalization. They argued against their own suggestion; the comment should
  credit that rather than present the refusal as ours;
* that the distinction is *standing*, not effort: an annotation may be wrong
  because it decides nothing, and a leg may not, because it makes a claim of
  equal standing to the ambient one;
* **the bright line**, in the comment and not only in the code: the reported
  finding set is identical with the annotation present and absent, and a test
  enforces it. That is the commitment that keeps option 3 from becoming option 2
  later, and the reporter is the right party to hold us to it;
* that **the ambient audit's width was not narrowed**, which is what they asked
  for and is easy to lose in a summary that leads with "we added reachability";
* and, for **#5 gap 3**, that the imperative was scoped rather than the detection
  removed — exit 3 still fires. They pruned a security allowlist on our
  instruction and were saved by a test they happened to have; the comment should
  be plain that the instruction was wrong, not that it was imprecise.

### 5. Something owed back to the reporter

Issue #6's measurement — 299 discoverable, 93 in closure, 212 outside, 144
findings, 27 reachable — is the only field data this project has on the
env-versus-project gap in a conda workflow. The closing comment should say
whether it was used as evidence, and *where it is now recorded*, so that a
measurement an adopter built by hand does not evaporate into a closed issue. If
the plan records it under `dev/measurement/`, name the file in the comment.

### 6. What a reviewer should test in this amendment

That *4*'s bright-line commitment is one this proposal can actually keep. If the
identical-set test turns out to be unbuildable as specified, the honest move is
to say so **before** promising it to the reporter in a public comment — a
commitment made in a closing comment is harder to walk back than one made in a
proposal.

## Review -- Claude (Internal, fresh-context subagent) -- 2026-08-20

**Model**: claude-opus-5 (Claude Opus 5)

Reviewed commit: 841bfc6708974267362f6d0926c12ee9d9113944
Target: the complete current contract -- the whole file, opened at `3499fc5` and extended by the `## Amendment -- Claude (author) -- 2026-08-20` landed at `e718eaf`
Prior findings: none
Assurance path: high-assurance

**Tier**: Internal
**Findings**: raised (4 blocking, 4 non-blocking)

<!-- claim-check-allow: scripts/run_security_audit.py -->
<!-- The directive covers [R5] only, which cites that path *because it does not
     resolve*. It suppresses nothing of the author's: their two occurrences sit
     inside backticked commands, which claim_check never matched in the first
     place -- see the instrument note in [R5]. -->

No `Plan readiness` field is recorded: only an **External** pass may supply it, and
this is an Internal read with no different-agent-type read to spend.

All source citations below are reads of the working tree at `841bfc6`; every file
cited was confirmed clean against HEAD (`git status --short` empty) before being
read, so the line numbers are the committed ones.

### Steelman

**The defect shape is real, correctly generalized, and the four cited claims all
verify.** I opened every one:

* `scripts/content_scan_runner.py:37-38` -- "a reviewed-residual entry has no live
  occurrence (it could preauthorize a replay). A distinct fail-closed class."
  Exact. The detection genuinely is right and the proposal is right to keep it.
* `scripts/content_scan_runner.py:594-595` -- the `STALE baseline authority ... --
  FAILS (prune the residual baseline).` message. Exact, and the imperative really
  is unqualified.
* `templates/modules/team-gated/run_security_audit.py:808-816` -- `pip_audit_argv`'s
  docstring, ending "a narrowed claim over an ambient environment is exactly as
  false as a wide one." Exact, and the proposal reads it correctly rather than
  against itself.
* `templates/modules/team-gated/python-security.md:35-52` -- the *Declared scope*
  section, exactly those lines.
* The twins are byte-identical: `sha256 073c8669...` for both
  `scripts/content_scan_runner.py` and
  `templates/modules/team-gated/content_scan_runner.py`.

**The refusal of option 2 is procedurally and substantively correct, and I want to
say so before the findings, because it is the judgement most likely to be second-
guessed.** Option 2 was the reporter's suggestion, never accepted scope, so
declining it is not a scope reduction (`dev/proposals/_template.md` > "Declining a
reviewer's proposed expansion is not a reduction") -- and it is recorded in
*Alternatives considered* with a reason rather than dropped. The reason is the
right one: the distinction drawn is **standing**, not effort, and a leg makes a
claim of the same standing as the ambient one. This is not the author using the
reporter's caution to avoid work; the work in option 3 is the same closure walk.

**The Amendment is the best part of the artifact.** Splitting issue #5's close
across two proposals, refusing to let whichever lands first post the close, and
requiring the closing comment to name *what was declined* -- these are the
disciplines that keep a public "resolved" from outrunning what shipped. And §6
asks the reviewer to test the one commitment that is about to become
irreversible. That instruction is what produced [R1] below, which is the finding
I would most want the author to have before that comment is posted.

### Findings

* **[R1] BLOCKING -- the D2 bright line has no referent, because the pip-audit leg
  reports *counts*, not findings.** This is §6's question, and the answer is no:
  the identical-set test is not buildable as specified.

  The leg discards vulnerability identity at parse time.
  `classify_pip_audit_output` (`run_security_audit.py:879`+) accumulates
  `vulnerabilities += len(vulns)` (`:942`) and keeps nothing else; `Coverage`
  (`:767-787`) carries `established / scanned / no_match / unknown / note / names /
  vulnerabilities` and **no per-vulnerability field**; `_valid_pip_audit_vulnerability`
  (`:872-876`) reads `id` and `fix_versions` only to validate shape and retains
  neither. The printed report (`:1198-1215`) is counts plus distribution names, and
  the pass returns a status string and a tier (`:1217-1230`). I grepped the module
  for any per-vulnerability output (`vulns|"id"|aliases|fix_versions|advisory`) and
  found only that shape check -- and the grep is confirmed live, because it *did*
  match the retention site at `:938-942`.

  Three consequences, each load-bearing:

  1. **The header's "No change to ... what is reported" is false for D2.**
     Annotating "each finding" requires first *creating* a per-finding report --
     new retention in `Coverage`, new fields read out of the child JSON, new
     output. That is materially more than "annotate the existing output" / "triage
     axis added" (§*D2 (3)*).
  2. **The invariant has no pre-change referent.** "The reported finding set is
     byte-identical with the annotation present and absent" -- with the annotation
     absent, the reported finding set is **empty**. A test comparing empty to empty
     is exactly the hazard S2 names ("an assertion derived from the same list it
     checks cannot fail"), and worse: both sides are vacuous, so the S2 filtering
     mutation would not redden it either.
  3. **"byte-identical" stays wrong even after (1) is fixed.** An annotation
     printed into a report changes that report's bytes by construction. The
     invariant can only ever be about a *projection*.

  Satisfier -- and this must land **before** Amendment §4 publishes the commitment
  to the reporter, per §6's own instruction. Restate the bright line as two
  invariants that have referents:

      (i)  Pre-existing referent, testable today: `coverage.vulnerabilities`,
           `coverage.scanned`, `coverage.unknown`, `coverage.names` and the
           `(status, tier)` the pass returns are identical with the reachability
           axis present and absent. This exists now, and it reddens under S2's
           filtering mutation.
      (ii) New referent, once the per-finding list exists: the reported list's
           `(distribution, vulnerability id)` projection equals the set derived
           from the **raw child JSON**, not from the annotated list -- so a filter
           anywhere between parse and print reddens it.

  And correct the `Touches` line: D2 does change what is reported.

* **[R2] BLOCKING -- the four-consumer measurement counts *mentions*, not *reads*,
  and omits the one consumer that would make D1's case mechanically.** I opened all
  four:

  * `scripts/content_scan_runner.py:84` -- genuine reader of baseline entries. ✔
  * `templates/modules/team-gated/run_security_audit.py:104` -- this is the
    `_MODULE_APPARATUS` table (`:99-110`), an **integrity preflight** list. It never
    reads entries; its only route to the file's content is `integrity_preflight`
    hashing it (`:196-202`). And for the *scan* it is not an independent auditor at
    all: it `importlib`-loads the runner (`:596-601`) and calls `runner.audit(...)`
    then `runner._print_summary(...)` (`:625-627`). It is a **caller**, not a second
    consumer with its own audited set.
  * `bootstrap/_scaffold/config.py:1017-1018` -- an `InstallSpec`. That is the
    *installer* writing the shipped template into an adopter tree; it never reads an
    adopter's baseline.
  * `bootstrap/tests/test_security_stack.py` -- writes tmp fixtures (`:337`, `:464`,
    `:490`).

  So exactly **one** component reads baseline entries. The evidence does not
  falsify sole-consumership, and "**Falsified**, not merely rejected" overstates
  what was measured. (The conclusion survives on the proposal's own fallback --
  "the assertion ... ages the moment a fifth arrives" -- which is the argument
  actually doing the work; it is closed by construction, and the enumeration is the
  weaker kind the proposal itself disparages two lines later.)

  The omitted consumer is the strong one: **the lockfile**.
  `dev/.cairn/cairn-lock.yml:631-637` records
  `"hash": "sha256:49ba1709fe519dd52205c1a64e36e14e723135bef3a358e1a7464d8c814146cd"`
  for `scripts/content_scan_residuals.txt`, and `integrity_preflight` compares
  on-disk bytes to that record and raises `AuditDegraded` on mismatch
  (`run_security_audit.py:196-202`). A prune changes the bytes. So on an installed
  tree the exit-3 imperative instructs the operator into a state that **degrades a
  sibling security control** unless the lockfile record is reconciled in the same
  act -- a mechanical, checkable consequence, unlike "another consumer may hold
  that entry."

  Satisfier: replace the count with the read-relationship taxonomy (reads entries /
  hashes the file for integrity / installs it / writes test fixtures), soften
  "falsified" to "rejected", and add the lockfile-plus-preflight consumer. The
  scoped exit-3 sentence should name lockfile reconciliation as part of "confirm
  across consumers before pruning."

* **[R3] BLOCKING -- "No Security Review trigger" is refused by this project's own
  trigger list.** `dev/proposals/_template.md:76-78`, the `triage-extra-triggers`
  slot: "**Bootstrap safety / security stack** -- `bootstrap/SAFETY.md` (R-I),
  `bootstrap/security_check.py`, or **the content scanner**; a change here is also a
  Security Review trigger." D1 changes the content scanner. The header's reasoning
  -- "no trust boundary is added, moved or widened" -- answers a different question:
  this trigger is **surface-based, not boundary-based**, and it does not ask whether
  a boundary moved. `AGENTS.md` reads the same way in both directions ("a named
  high-risk surface takes its Security Review on its own trigger, whatever this
  field says"; and for verification, "**Bounded mode refuses** ... any high-risk
  surface named below").

  Compounding it: by [R1](1), D2 widens the **parse surface** bound to
  `_PIP_AUDIT_SCHEMA_ESTABLISHED` -- new fields read out of untrusted child output.
  S1 accounts only for distribution metadata and does not reach this.

  Satisfier: declare the Security Review, or state explicitly why a message-only
  change to the content scanner falls outside the slot's trigger and let the
  Maintainer rule on it -- but do not leave it as a silent "no". Extend S1 to the
  per-finding child-JSON fields either way.

* **[R4] BLOCKING (scope) -- D1 fixes the terminal message and leaves the *more
  authoritative* copy of the same wrong imperative in place.**
  `templates/modules/team-gated/content-security.md:122-123` -- the adopter-facing
  module doc -- says: "A baseline entry with no live occurrence is **STALE** and
  **fails** the scan (exit 3): **it must be deleted before the baseline is
  current.**" That is *stronger* than the runner's message, and it is what an
  operator consults when deciding what to do about exit 3. It is absent from
  `Touches` and from *Documentation / doctrine surface*, which name only
  `python-security.md` and "two docstrings" (themselves unnamed).

  Cairn self-hosts copies at `dev/modules/content-security.md:112` and
  `dev/.cairn/base/dev/modules/content-security.md:112`, so the fix has a
  scaffold-state dimension the plan must handle.

  Leaving this is the proposal's own defect shape at one remove: a control's
  imperative corrected in one output and left overreaching in the document the
  reader is more likely to have open. Satisfier: add `content-security.md` to
  `Touches` and to the documentation surface, and name the self-hosted copies'
  handling.

* **[R5] Non-blocking -- `scripts/run_security_audit.py` does not exist on this
  tree, so the smoke check that names it cannot run.** *Examples / smoke checks*
  claims: "`python scripts/content_scan_runner.py` and `python
  scripts/run_security_audit.py` **on this tree** -- both are the operator paths
  that produced the reports." Verified: `git ls-files | grep run_security_audit`
  returns only `templates/modules/team-gated/run_security_audit.py`; `scripts/`
  holds no such file; and **`python-security` is not in Cairn's installed roster**
  (`dev/.cairn/cairn-lock.yml:647-664` lists 16 modules -- `content-security` is
  there, `python-security` is not). S3 repeats the same path as an "operator-run
  entry point."

  Two errors in one sentence: the path does not resolve here, and the reports were
  produced on the *adopter's* tree, not this one. This is `AGENTS.md`'s "name the
  trigger ... and open it" applied to the proposal itself.

  Instrument note, because it matters for how much the author should trust the
  gate: `python scripts/claim_check.py` on this file returns **OK, no flags** -- the
  path sits inside a backticked *command* rather than a bare backticked path, so
  the checker never had the chance to match it. Its silence here is not evidence.

  Satisfier: state that the D2 smoke is exercised through `test_security_stack.py`'s
  orchestrator fixture against the template file (which is how the leg is reachable
  in this tree at all), or give an explicit "**N/A**: `python-security` is not
  installed in Cairn's own tree."

* **[R6] Non-blocking -- "the annotation decides nothing" is too clean, and it is
  the sentence headed for a public comment.** S5 already concedes an attacker "can
  make a finding annotate as *not reachable* and be triaged last." At the ratio D2
  is built around (144 findings, 27 reachable), *triaged last* is operationally
  *not triaged* -- and for a control whose named failure mode is being **skimmed**,
  deciding attention is close to the thing at stake. The defensible form is
  "decides nothing **the tool acts on** -- no verdict, no exit code, no finding
  omitted." Satisfier: that wording, in the *bright line* paragraph, in S1, and in
  Amendment §4's third bullet, so the closing comment does not claim more than the
  design delivers.

* **[R7] Non-blocking -- the D1 plumbing is a cross-module signature change on
  exactly the mixed-tree surface D1 came from.** `audit()` returns
  `(code, files, all_flags, new_flags, stale)` -- **no roots**
  (`content_scan_runner.py:555-570`) -- and `_print_summary(code, files, all_flags,
  new_flags, stale)` (`:573`) does not receive them. So "the roots manifest is
  already loaded -- this is printing what the runner already knows" is true at
  module scope but is not free. And `run_security_audit.py:627` calls
  `runner._print_summary(...)` **positionally across the module boundary**, so a
  signature change breaks a tree whose `run_security_audit.py` is at a different
  version -- which is the mixed-tree condition that produced this report.

  Also worth noting for accuracy: `_print_summary` **already** prints
  `from {_ROOTS_MANIFEST.name}` (`:579`), so D1 item 2 is partly done -- the
  manifest is named; the *roots it resolved to* are not, and that is the part that
  makes the claim checkable.

  Satisfier: derive the roots inside `_print_summary` from `_ROOTS_MANIFEST` (no
  signature change), or record the positional cross-module call as a compatibility
  constraint the plan must handle explicitly.

* **[R8] Non-blocking -- the coverage-ceiling gap is real, with one calibration.**
  I read `python-security.md:35-52` in full against the charge that the author
  under-read it. They did not. Paragraph one states the set and lists non-coverage
  (conda-managed native, OS, vendored); paragraph two is entirely about the
  **excess outside** the tool's reach ("routinely carries substantially more
  packages than the Python distributions the tool can enumerate"). Nothing draws
  the opposite consequence.

  Calibration: the *set* is disclosed -- there, and again at runtime
  (`run_security_audit.py:1116-1119`, the `[pip-audit] DECLARED SCOPE` banner).
  So the gap is precisely "the consequence is never drawn," not "the scope is
  undisclosed." Worth stating that way, because it makes the fix a sentence about
  consequence rather than a re-disclosure of scope the doc already makes twice.

### Coverage

**Covered** --

1. **Claims** -- probed every load-bearing citation against the tree: the four
   cited line ranges (all exact, quoted in the steelman); twin byte-identity
   (`shasum` -> `073c8669...` both); the four-consumer claim ([R2], each opened);
   the `scripts/run_security_audit.py` path (`git ls-files`, `ls scripts/`,
   `cairn-lock.yml:647-664`) ([R5]); the "annotation on the existing output" premise
   (`run_security_audit.py:767-787`, `:879-950`, `:1198-1230`) ([R1]).
2. **Production path exercised by tests** -- `bootstrap/tests/test_security_stack.py`
   reaches the leg only through `run_pip_audit_pass` with monkeypatched
   `shutil.which` / `active_pip_audit_version` (`:785-822`); the mapping link
   resolves. The gap is that there is no existing per-finding assertion to extend,
   which is [R1].
3. **Design completeness** -- the edge-case inventory is genuinely good (extras,
   markers, `Pillow`/`pillow`, empty closure, the 71% case) and the "messy by
   construction" fixture instruction is the right call. The missing precondition is
   the one in [R1]: what "annotation absent" *is*.
4. **Silent failure / fail-closed** -- the `unknown` disposition is declared open
   and intentionally so, and I agree; exit-code invariance is checkable against the
   existing contract tests (`TestRunnerExitContract`, `:433-546`). [R2]'s
   `integrity_preflight` path (`:196-202`) fails closed correctly -- the hazard
   there is the *instruction*, not the guard.
5. **Cross-document consistency** -- swept the docs for the changing behaviour and
   found [R4] (`content-security.md:122-123` plus two self-hosted copies) and [R5].
6. **Drift** -- `Touches` is inaccurate in two places ([R1](1), [R4]); the
   docstring/doc claims otherwise match shipped behaviour.
7. **Lifecycle / process placement** -- the Amendment's MAINTAINER-GATED close, the
   two-proposal split for #5, and the refusal to edit `dev/PLANNING.md` at
   proposal-open are all correctly placed. `python tools/lifecycle_planner.py scan`
   -> all 6 artifacts structurally sound. The doctrine rate-limit reasoning
   (declining to make this an `AGENTS.md` rule) is sound.
8. **Domain validity & scope** -- [R3] (assurance/Security-Review routing) and [R4]
   (scope under-reach). The option-2 refusal is justified, per the steelman.
9. **Name the satisfier** -- each of [R1]-[R8] carries one.

**Not covered / low confidence** --

* **Same-type reviewer.** No cross-type independence on this pass, and no
  `Plan readiness` may be recorded from an Internal read.
* **Nothing was executed.** I ran `claim_check`, `lifecycle_planner scan`, `shasum`,
  `git ls-files` and greps -- but not `pytest bootstrap/tests/test_security_stack.py`
  and neither operator command. Every behavioural finding rests on source reading.
* **[R2]'s recoverability is not established.** I read `integrity_preflight` only.
  Whether a supported lockfile re-record path makes a post-prune `AuditDegraded`
  routinely recoverable -- and therefore how loudly the scoped exit-3 sentence needs
  to say it -- I did not determine. Treat the *mechanism* as verified and the
  *severity* as open.
* **The adopter's field numbers** (299 / 93 / 212 / 144 / 27) are on an external
  tree and are unverifiable from here. I did not treat them as claims; they are
  reported measurement.
* **Amendment §5's `dev/measurement/` home** -- I did not check what is already
  recorded there or whether it is the right home.
* **Lens 7, lightly.** I did not determine whether an exit-3 wording change owes a
  `CHANGELOG.md` line at the next serialization point (the archived
  `content-scan-detectors` plan carries an addendum about exactly that surface being
  under-populated, which suggests it may).

### Second-round recommendation

**A second structurally-independent pass is recommended, and it should be
External.** Not because this pass was thin, but because of what it found: [R1]
means the artifact's central commitment has to be re-specified rather than merely
corrected, and [R3] means the review tier itself is contested. A revision that
rebuilds the bright line on real referents is a *new* contract, and the design
question underneath it -- whether adding a per-finding report to a security leg is
still "no change to what is reported" -- is precisely the kind of consequential
design a same-type reader is worst placed to challenge twice. An External pass on
the revision would also be the one able to record `Plan readiness`, which this pass
cannot.

**Disposition: blocking.** Four blocking findings ([R1]-[R4]); status moved to
`revising`.
