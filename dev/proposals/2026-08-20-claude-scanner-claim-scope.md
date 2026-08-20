# A scanner's imperative must name the set it audited

**Author**: Claude (Strategy)
**Model**: claude-opus-5 (Claude Opus 5)
**Date opened**: 2026-08-20
**Status**: awaiting-review
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
