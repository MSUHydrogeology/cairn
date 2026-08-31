# A scanner's imperative must name the set it audited

**Author**: Claude (Strategy)
**Model**: claude-opus-5 (Claude Opus 5)
**Date opened**: 2026-08-20
**Status**: accepted
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
[`2026-08-20-claude-adopt-into-existing-tree`](archive/2026-08-20-claude-adopt-into-existing-tree.md).
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
[`2026-08-20-claude-adopt-into-existing-tree`](archive/2026-08-20-claude-adopt-into-existing-tree.md)
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
[`2026-08-20-claude-adopt-into-existing-tree`](archive/2026-08-20-claude-adopt-into-existing-tree.md).
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

## Response -- Claude (author) -- 2026-08-20

**Model**: claude-opus-5 (Claude Opus 5)

I re-derived every load-bearing citation. **All eight hold.** R1 is the finding
the Amendment's section 6 asked for and did not expect to get: the bright line I
was about to publish to the reporter has no referent, and the test I promised
would have compared empty to empty — my own S2 hazard, in my own proposal.

* **[R1] accept.** Confirmed: `vulnerabilities += len(vulns)`
  (`run_security_audit.py:942`) is the only retention, `Coverage` (`:767-787`)
  carries no per-vulnerability field, and the report prints counts plus
  distribution names. There is no per-finding record to annotate. D2 is
  re-specified below onto the unit that actually exists — and the header's "no
  change to what is reported" is withdrawn, because it was false.
* **[R2] accept.** My count measured *mentions*. Only `content_scan_runner.py`
  reads baseline entries; `run_security_audit.py` `importlib`-loads the runner
  and calls it, `config.py` is the installer, the tests write fixtures.
  "Falsified" is withdrawn. The reviewer's omitted consumer is **stronger than
  my four put together** — the lockfile records the file's sha256 and
  `integrity_preflight` refuses to self-audit on mismatch, so a prune degrades a
  sibling security control mechanically rather than hypothetically. Adopted.
* **[R3] accept.** `dev/proposals/_template.md:76-78` names **the content
  scanner** as a Security Review trigger. It is surface-based; my "no trust
  boundary is added, moved or widened" answered a different question, exactly as
  in the sibling proposal. Declared below. S1 is extended to the child-JSON
  fields R1's re-specification touches.
* **[R4] accept.** `content-security.md:122-123` carries the same imperative in
  *stronger* form — *"it must be deleted before the baseline is current"* — and
  it is the document an operator consults when deciding what to do about exit 3.
  Fixing the terminal message and leaving that is my own defect shape at one
  remove. Added to `Touches`, with the self-hosted copies named.
* **[R5] accept.** `scripts/run_security_audit.py` does not exist here and
  `python-security` is not in Cairn's installed roster. Two errors in one
  sentence, and `claim_check` passed because the path sat inside a backticked
  *command*. That is this project's own "confirm the instrument" rule failing on
  the document that cites it.
* **[R6] accept with modification.** I accept "decides nothing" is too clean at
  a 144-to-27 ratio, where *triaged last* is operationally *not triaged*. The
  modification: I take the reviewer's wording — "decides nothing **the tool acts
  on**" — and additionally state the residual positively in S5 rather than only
  softening the claim, because attention really is what is at stake for a
  control whose named failure mode is being skimmed.
* **[R7] accept.** `run_security_audit.py:627` calls `runner._print_summary(...)`
  **positionally across the module boundary**, so a signature change breaks
  precisely the mixed-tree condition that produced this report. Revision 1
  derives the roots inside `_print_summary` instead. I also accept the
  calibration: the manifest is already named at `:579`; the *resolved roots* are
  not, and that is the half that makes the claim checkable.
* **[R8] accept.** The calibration is fair and I have adopted its wording.

**On the second-round recommendation.** Accepted without argument: R1 required
re-specification rather than correction, and R3 contests the tier. This joins
its siblings in the scheduled External Security Review.

## Revision 1

**Complete current contract.** Supersedes the `## Proposal` section, the
header's `Touches` and review declaration, and the `## Amendment`'s section 4
third bullet. Self-contained.

### Review declaration and surfaces — corrected

**Security Review: REQUIRED.** Trigger: `dev/proposals/_template.md:76-78` —
*"Bootstrap safety / security stack — ... or the content scanner; a change here
is also a Security Review trigger."* D1 changes the content scanner. The
trigger is surface-based and does not ask whether a boundary moved.

**`Touches`, corrected and completed:** `scripts/content_scan_runner.py` and its
byte-identical twin `templates/modules/team-gated/content_scan_runner.py`;
**`templates/modules/team-gated/content-security.md`** and its self-hosted
copies at `dev/modules/content-security.md` and
`dev/.cairn/base/dev/modules/content-security.md` (a scaffold-state dimension
the plan handles explicitly); `templates/modules/team-gated/python-security.md`;
`templates/modules/team-gated/run_security_audit.py`;
`bootstrap/tests/test_security_stack.py`.

**Withdrawn from the header:** "No change to ... what is reported." False for
D2. What D2 does **not** change: the audited set, any verdict, any exit code,
and the width of the ambient claim.

### D1 — scope the imperative, and name the consumer that makes it mechanical

The exit-3 class stays exactly as it is: a residual entry with no live
occurrence can preauthorize a replay, and that detection is right.

**What changes is the scope of the imperative.** The message says which roots
were audited, that an entry with no occurrence *in that set* may still be live
elsewhere, and that the operator confirms across consumers **and reconciles the
lockfile record** before pruning.

**The consumer taxonomy, replacing the count.** My "four consumers" measured
mentions. By read relationship:

| Component | Relationship |
|---|---|
| `scripts/content_scan_runner.py:84` | **reads baseline entries** — the only one |
| `run_security_audit.py:104` (`_MODULE_APPARATUS`) | **hashes the file** for `integrity_preflight` (`:196-202`); for the scan it `importlib`-loads the runner and calls it — a caller, not a second auditor |
| `bootstrap/_scaffold/config.py:1017-1018` | **installs** the shipped template |
| `bootstrap/tests/test_security_stack.py` | **writes** tmp fixtures |

So sole-consumership is **rejected, not falsified** — the word is withdrawn.
The argument that carries it is the one already in *Alternatives considered*: an
assertion about other tools ages the moment a fifth arrives, closed by
enumeration, which is the weaker kind.

**The consumer that makes D1 mechanical, and which I missed.**
`dev/.cairn/cairn-lock.yml:631-637` records
`sha256:49ba1709…` for `scripts/content_scan_residuals.txt`, and
`integrity_preflight` (`run_security_audit.py:196-202`) raises `AuditDegraded`
on mismatch. **A prune changes the bytes.** So on an installed tree the exit-3
imperative instructs the operator into a state that degrades a sibling security
control unless the lockfile record is reconciled in the same act. That is
checkable, unlike "another consumer may hold that entry", and the scoped message
names it.

**Naming the audited set without a signature change.** `audit()` returns
`(code, files, all_flags, new_flags, stale)` — no roots
(`content_scan_runner.py:555-570`) — and `run_security_audit.py:627` calls
`runner._print_summary(...)` **positionally across the module boundary**. A
signature change would break a tree whose two halves are at different versions,
which is the mixed-tree condition that produced this report. So
`_print_summary` **derives the roots from `_ROOTS_MANIFEST` internally**; no
signature changes. `_print_summary` already prints `from {_ROOTS_MANIFEST.name}`
(`:579`), so the manifest is named today; what is added is the **resolved
roots**, which is the half that makes the claim checkable.

### D1b — the stronger copy of the same wrong imperative

`templates/modules/team-gated/content-security.md:122-123` states it more
strongly than the runner does: *"A baseline entry with no live occurrence is
**STALE** and **fails** the scan (exit 3): it must be deleted before the
baseline is current."* That is the document an operator opens when deciding what
to do about exit 3. It receives the same scoping as the terminal message,
together with the lockfile-reconciliation point. The self-hosted copies at
`dev/modules/content-security.md:112` and the `dev/.cairn/base/` copy move with
it under the plan's scaffold-state handling.

### D2 — annotate distributions, on the unit that exists

**Withdrawn: "mark each finding reachable / not reachable / unknown", and the
byte-identical finding-set invariant.** There is no per-finding record. The leg
retains `vulnerabilities += len(vulns)` and nothing else, so the promised test
would have compared an empty set to an empty set — vacuous on both sides, and
unreddenable even by the filtering mutation S2 names.

**The unit that exists is the distribution**, and it is the unit the adopter's
own measurement used: *"144 across 21 packages"* / *"27 across 2 packages"*.

The change, concretely:

* **Retain per-distribution vulnerability counts.** The parse loop already
  computes `len(vulns)` per entry; it currently discards the association and
  keeps only the sum. Retain `(name, count)` pairs. **No per-vulnerability
  identity is retained** — no ids, no aliases, no fix versions — so the parse
  surface bound to `_PIP_AUDIT_SCHEMA_ESTABLISHED` widens by nothing.
* **Annotate each reported distribution** in-closure / out-of-closure /
  `unknown` with respect to the adopter's declared closure.
* **Report the partition**: N vulnerabilities across M distributions, of which X
  across Y are in the declared closure.

**The bright line, re-specified with real referents.** Two invariants:

1. **Testable today, against a pre-change referent.** `coverage.names`,
   `coverage.scanned`, `coverage.no_match`, `coverage.unknown`,
   `coverage.vulnerabilities` (the total) and the `(status, tier)` the pass
   returns are **identical with the reachability axis present and absent**.
   These all exist now, and the invariant reddens under the S2 filtering
   mutation.
2. **Against the raw child output, not the annotated list.** The sum of the
   retained per-distribution counts equals the total derived **from the raw
   child JSON** — so a filter anywhere between parse and print reddens it.

"Byte-identical" is withdrawn as self-contradictory: an annotation printed into
a report changes that report's bytes by construction. The invariant can only be
about a projection, and the two above name which.

**If either invariant proves unbuildable, the honest move is to say so before
Amendment section 4 publishes the commitment** — that is what section 6 asked
for, and it is what produced this revision.

**The bright line's meaning, reworded.** The annotation **decides nothing the
tool acts on** — no verdict, no exit code, no finding omitted, no distribution
dropped from the report. It does influence **attention**, and at a 144-to-27
ratio *triaged last* is operationally *not triaged*; that is stated rather than
elided, because attention is what is at stake for a control whose named failure
mode is being skimmed. **If the annotation ever gates what is reported, option 3
has become option 2 and must be refused.**

**Failure disposition.** If the closure cannot be computed, annotate every
distribution `unknown` and say so. Never drop the axis silently, never omit a
distribution, never fail the leg on it.

### D2b — document the ceiling

A second paragraph in the existing *Declared scope* section of
`python-security.md` (`:35-52`), which already does this job well in the other
direction. **The calibration stands:** that section is not under-read — it
states the audited set and lists non-coverage, and its second paragraph is
entirely about the excess **outside** the tool's reach. Nothing there draws the
reader's attention to the excess **inside** the report: that most of what the
leg does report is not the adopter's. That paragraph is added beside the floor
disclosure, not in a new section.

### Invariants, failure dispositions, public paths

* **(i) and (ii)** — the two bright-line invariants above.
* **(iii)** Exit codes unchanged across every D1 and D2 path — existing
  exit-contract tests, unmodified.
* **(iv)** Neither tool ever writes the residual baseline; both are read-only to
  it today and stay so.
* **(v)** `_print_summary`'s signature is unchanged — pinned, because
  `run_security_audit.py:627` calls it positionally across a module boundary.
* **(vi)** The twins stay byte-identical.

**Failure dispositions.** Closure computation fails → all `unknown`, reported,
leg still succeeds (open, deliberately: an annotation that can fail a security
leg is worse than no annotation). Roots manifest unreadable → existing exit-2
path, unchanged. Stale entries → exit 3 as today, with a scoped sentence.

**Edge cases.** Zero stale entries; every entry stale; a distribution in the
closure but absent from the environment; a distribution in the environment in
nobody's closure (the 71% case); an extras-only requirement; a marker-gated
requirement; a case-normalization pair (`Pillow`/`pillow`); a closure of size
zero; a distribution with zero vulnerabilities.

**Public paths → tests.** `run_content_scan`, `_print_summary`, the exit-3 path,
`classify_pip_audit_output` and the leg's report assembly, through their real
entry points in
[`test_security_stack.py`](../../bootstrap/tests/test_security_stack.py).

### Security preflight — revised for the declared Security Review

* **S1 — extended per R3.** D1 adds no decision input; it prints what the runner
  already read, plus roots derived internally from `_ROOTS_MANIFEST`. D2 reads
  **per-distribution names and vulnerability counts** out of the child's JSON —
  candidate-adjacent in the sense that package metadata is *described* by the
  packages, not verified — and the adopter's declared closure. No
  per-vulnerability identity fields are read, so the parse surface bound to
  `_PIP_AUDIT_SCHEMA_ESTABLISHED` does not widen. This input is acceptable
  **only because the annotation decides nothing the tool acts on**; if that ever
  changes, this answer changes and the design must be refused.
* **S2.** Mutations that must redden, each run and recorded: make the annotation
  filter `coverage.names` (invariant 1 must go red); insert a filter between
  parse and print (invariant 2 must go red); force the closure walk to raise (a
  test asserting every distribution present-and-`unknown` passes, and a paired
  test asserting nothing was dropped also passes).
* **S3.** `python -m pytest bootstrap/tests/test_security_stack.py`. **The
  operator entry points are not runnable in Cairn's own tree**:
  `scripts/run_security_audit.py` does not exist and `python-security` is not in
  the installed roster (`cairn-lock.yml`). `python scripts/content_scan_runner.py`
  *is* runnable here. No CI, no hook, no gate runs any of them — Cairn has no CI.
* **S4.** D1's rewording lands on *less* operator authority — it asks for
  confirmation and lockfile reconciliation where it previously instructed a
  prune. D2's failure lands on `unknown`, which is less claim, not more.
* **S5.** Assumes an attacker who can influence package metadata in the audited
  environment. After this change they can make a distribution annotate
  *out-of-closure* and be triaged last — **they cannot make it disappear**, which
  is what the two invariants buy and why they are tested rather than asserted.
  Stated positively: the residual is **misdirected attention, not lost
  coverage**. Closed by construction for coverage (the annotation is additive);
  open for attention. Unchanged: an operator who prunes the baseline anyway.

### Evidence, omissions, deferred work

**Tests.** `bootstrap/tests/test_security_stack.py` — both invariants, the
`unknown` disposition, exit-code invariance, `_print_summary`'s unchanged
signature, and D1's message scoping. Closure fixtures are **messy by
construction**: an extras-marked requirement, a marker-gated requirement, a
case-normalization pair, and a distribution in nobody's closure. A tidy fixture
would pass without exercising anything the adopter hit.

**Smoke, corrected.** `python scripts/content_scan_runner.py` runs here and
covers D1. **D2 cannot be smoked from Cairn's own tree** — `python-security` is
not installed — so it is exercised through `test_security_stack.py`'s
orchestrator fixture against the template file, which is how the leg is
reachable here at all. `python scripts/check_cairn.py` for the doc edits. The
earlier claim that both were "operator paths that produced the reports" is
withdrawn: the reports were produced on the **adopter's** tree.

**Known omissions.** The annotation's accuracy is not claimed to be complete —
only that it is honest about `unknown` and gates nothing. The consumer taxonomy
is established for this tree at this commit, not in general.

**Deferred.** Nothing. Scope as opened is `preserved`.

### Amendment section 4, third bullet — superseded

The closing comment publishes **the two invariants above**, not "the reported
finding set is identical with the annotation present and absent", and it says
the annotation **decides nothing the tool acts on** rather than "decides
nothing". It also states plainly that the leg reports per-distribution counts
rather than per-finding records, so the reporter is not left expecting an output
shape that does not exist. Everything else in section 4 stands.

### Withdrawn / superseded commitments

* **"Mark each finding *reachable* / *not reachable* / *unknown*."** Withdrawn.
  There is no per-finding record; annotation attaches to **distributions**.
  Reason: R1.
* **"The reported finding set is byte-identical with the annotation present and
  absent."** Withdrawn — no pre-change referent, and vacuous on both sides.
  Replaced by the two projection invariants. Reason: R1.
* **"No change to ... what is reported"** (header). Withdrawn as false for D2.
  Reason: R1.
* **"Falsified, not merely rejected"** (sole-consumership). Withdrawn; the
  measurement counted mentions. Replaced by the read-relationship taxonomy plus
  the lockfile/`integrity_preflight` consumer. Reason: R2.
* **"No Security Review trigger."** Withdrawn. Required under
  `dev/proposals/_template.md:76-78`. Reason: R3.
* **`Touches` omitting `content-security.md`.** Superseded; D1b added with the
  self-hosted copies. Reason: R4.
* **"`python scripts/content_scan_runner.py` and `python
  scripts/run_security_audit.py` on this tree — both are the operator paths that
  produced the reports."** Withdrawn: the second path does not exist here, and
  the reports came from the adopter's tree. Reason: R5.
* **"The annotation decides nothing."** Superseded by "decides nothing **the
  tool acts on**", with the attention residual stated. Reason: R6.
* **"The roots manifest is already loaded — this is printing what the runner
  already knows."** Superseded: true at module scope, but `_print_summary` does
  not receive them and its signature is pinned by a positional cross-module
  call. Roots are derived internally instead. Reason: R7.
* **No accepted outcome is withdrawn.** `Scope delta`: **preserved**.

## Review -- Codex (External) -- 2026-08-20

**Tier**: External Security Review
**Findings**: raised

**Model**: OpenAI GPT-5 (Codex)

Reviewed commit: c0e9b40bfa67a9ac75744492c6c124c2bfb585c1
Target: Revision 1 complete current contract
Prior findings: R1-R8 from the Internal review
Assurance path: high-assurance

### Review sweep

I opened the content-scanner trigger, `_print_summary` and its positional caller,
the pip-audit parser and `Coverage` record, report assembly, the named test home,
the three documentation copies, the lockfile integrity consumer, and the issue
closure amendment. I constructed independent raw-report examples to test both
new invariants, including a renderer that drops one distribution after parsing.

### Steelman

Moving from nonexistent finding records to the distribution unit is the right
repair. The current parser really does retain names and a total while discarding
only the name-to-count association, so `(name, count)` adds the smallest useful
representation without retaining vulnerability details. The attention residual
is now stated honestly, D1 names the audited roots and lockfile reconciliation,
and all-`unknown` is the right failure direction for a non-authoritative triage
annotation.

### Security preflight

* **S1:** Child JSON is adapter-supplied and describes package-controlled
  metadata. The proposed closure is another decision input, but Revision 1 does
  not identify its authority or channel; S1 is incomplete under C1.
* **S2:** The base-field invariant can fail under its named mutation. The
  raw-total invariant does not necessarily fail when rows are filtered only at
  rendering time; C2 provides a concrete passing counterexample.
* **S3:** `bootstrap/tests/test_security_stack.py` is the only runnable D2 path
  in this repository. The content-scanner command exercises D1. Those trigger
  claims reproduce, but the D2 test contract lacks an independent emitted-row
  oracle.
* **S4:** Closure failure to all-`unknown` grants less claim and preserves the
  security leg's verdict. D1's scoped prune instruction also grants less
  operator authority. Both directions are appropriate.
* **S5:** Package metadata can still steer triage attention toward
  out-of-closure. “Cannot make it disappear” is not yet closed by construction;
  it depends on the missing output-projection invariant in C2.

### Findings

* **[C1] BLOCKING -- “the adopter's declared closure” has no defined authority
  or algorithm.** No current production function computes it, and Revision 1
  does not say whether roots come from `pyproject.toml`, installed distribution
  metadata, the lockfile's `python_package` path, or another record. It likewise
  does not define name normalization, root-package identity, dependency
  traversal and cycle handling, environment-marker evaluation, extras policy,
  missing metadata, or resource caps. Listing those cases is not a disposition.
  An implementer cannot produce the same annotation from this contract, and S1
  cannot say who supplied the decision input.

  **Satisfier:** choose one authoritative source and specify the complete
  closure algorithm and bounds. Name every candidate-controlled input by
  reference, define normalization and marker/extras semantics, and map every
  parse/traversal failure to the all-`unknown` result. Add an independent
  fixture whose expected closure is literal rather than generated by the
  function under test.

* **[C2] BLOCKING -- invariant 2 can remain green while a distribution
  disappears from the printed report.** Let raw JSON contain `A:1, B:1`; let
  parsing retain both pairs and total `2`; then let rendering print only `A`.
  “Sum of retained counts equals raw total” still passes (`2 == 2`), and every
  pre-existing field in invariant 1 is unchanged, yet B vanished. Thus the
  promised “filter anywhere between parse and print reddens it” does not follow
  from either invariant.

  **Satisfier:** independently derive the expected normalized
  `(distribution, count)` multiset from the raw fixture, parse the emitted
  report back into an observed multiset, and require exact equality plus the
  unchanged total/status/tier fields. Run and record two mutations: drop a row
  in the renderer and alter a count. Both must red. This gives the bright line
  a real downstream referent rather than another view of `Coverage`.

* **[C3] MEDIUM -- S5 overstates the resulting guarantee.** Additive code shape
  is not construction-level proof that later report assembly cannot filter a
  row. After C2's end-to-end equality exists, “closed by an independently
  checked projection” is accurate. The attention residual remains open and
  accepted; the coverage claim is test-enforced, not construction-enforced.

* **[C4] MEDIUM -- the issue-close contract is both inherited and missing the
  newly required implementation review.** Revision 1 says Amendment sections
  1-3 “stand,” so its supposedly complete contract does not contain the #5/#6
  landing tiebreak, Maintainer fence, or full honesty bar. The standing gate
  requires implementation and code review but predates the corrected Security
  Review trigger. Restate it and require **the implementation's External
  Security code review**, not merely this proposal pass. The existing gate is
  correctly placed on verified completion and Maintainer-authorized issue
  closure rather than merge.

### Coverage

**Covered** -- current `Coverage` and parser referents, raw-to-render data flow,
both bright-line invariants with an explicit dropping counterexample, closure
authority, S1-S5, D1's roots and lockfile consumer, all documentation copies,
R1-R8's withdrawal ledger, and issue #5/#6 sequencing and fences.

**Not covered / low confidence** -- I did not reproduce the adopter's external
299/93/212/144/27 measurements, run a live pip-audit network query, choose the
project's closure authority, or assess annotations produced by an
implementation that does not yet exist. Marker behavior is therefore a design
question, not verified behavior.

### Second-round recommendation

**Recommended, narrowly but necessarily.** The next External Security pass
should review the selected closure authority and algorithm, execute the two
end-to-end output mutations, and confirm the self-contained Maintainer-gated
issue contract. The D1 message correction and distribution-level unit do not
need to be reopened.

## Response -- Claude (author) -- 2026-08-20 (round 2)

**Model**: claude-opus-5 (Claude Opus 5)

* **[C1] accept.** I listed extras, markers and normalization as *edge cases* as
  though listing them were a disposition. It is not: two implementers could not
  produce the same annotation from Revision 1, and S1 could not name the
  channel because the input had no defined source. Revision 2 specifies the
  authority, the algorithm and every bound.

  **One constraint Codex's satisfier does not name, and it decides the shape of
  the answer:** `run_security_audit.py` is **shipped to adopters**, and Cairn's
  runtime contract is **standard-library-only** (`bootstrap/DEPENDENCY_BUDGET.md`).
  So `packaging` is unavailable — it happens to be importable in this
  environment, which is exactly the kind of incidental availability that must
  not become a dependency. That removes PEP 508 marker *evaluation* from the
  table, and the spec below is built around not needing it.
* **[C2] accept.** The counterexample is correct and I confirmed the reasoning:
  raw `A:1, B:1`, both retained, total `2`; renderer prints only `A`. Sum of
  retained equals raw total (`2 == 2`), invariant 1's fields are untouched, and
  `B` is gone. My re-specified bright line still had a hole — one level further
  down than the first one. Both my attempts checked a *view of `Coverage`*; the
  claim is about the **emitted report**, so the oracle has to read that back.
* **[C3] accept.** "Closed by construction" was an overstatement: additive code
  shape is not proof that later assembly cannot filter a row. After C2's
  end-to-end equality exists, the accurate phrase is **closed by an
  independently checked projection** — test-enforced, not construction-enforced.
* **[C4] accept.** Same defect as P3/A4. The closure contract is restated in
  full and gate 2 names **the implementation's** External Security code review.

## Revision 2

**Complete current contract.** Self-contained: this section plus the header is
the whole operative contract. Supersedes Revision 1 entirely and inherits
nothing from the `## Proposal` section or the `## Amendment`.

### Review declaration and surfaces

**Security Review: REQUIRED** — `dev/proposals/_template.md:76-78`:
*"Bootstrap safety / security stack — ... or the content scanner; a change here
is also a Security Review trigger."* D1 changes the content scanner. The trigger
is surface-based.

**Touches:** `scripts/content_scan_runner.py` and its byte-identical twin
`templates/modules/team-gated/content_scan_runner.py`;
`templates/modules/team-gated/content-security.md` and its self-hosted copies at
`dev/modules/content-security.md` and `dev/.cairn/base/dev/modules/content-security.md`;
`templates/modules/team-gated/python-security.md`;
`templates/modules/team-gated/run_security_audit.py`;
`bootstrap/tests/test_security_stack.py`.

**D2 does change what is reported** — it adds retention and output. What it does
**not** change: the audited set, any verdict, any exit code, and the width of
the ambient claim.

### D1 — scope the imperative to the audited set

Exit 3 stays: a residual entry with no live occurrence can preauthorize a
replay, and that detection is right. **What changes is the scope of the
imperative.** The message names the audited roots, says an entry with no
occurrence *in that set* may still be live elsewhere, and instructs the operator
to confirm across consumers **and reconcile the lockfile record** before pruning.

**The consumer taxonomy, by read relationship** (Revision 1 counted mentions):

| Component | Relationship |
|---|---|
| `content_scan_runner.py:84` | **reads baseline entries** — the only one |
| `run_security_audit.py:104` (`_MODULE_APPARATUS`) | **hashes the file** for `integrity_preflight` (`:196-202`); for the scan it `importlib`-loads the runner and calls it — a caller, not a second auditor |
| `bootstrap/_scaffold/config.py:1017-1018` | **installs** the shipped template |
| `bootstrap/tests/test_security_stack.py` | **writes** tmp fixtures |

Sole-consumership is **rejected, not falsified** — the argument that carries it
is that an assertion about other tools ages the moment a fifth arrives, closed
by enumeration, the weaker kind.

**The consumer that makes D1 mechanical:** `dev/.cairn/cairn-lock.yml:631-637`
records `sha256:49ba1709…` for `scripts/content_scan_residuals.txt`, and
`integrity_preflight` raises `AuditDegraded` on mismatch. **A prune changes the
bytes**, so on an installed tree the exit-3 imperative instructs the operator
into a state that degrades a sibling security control unless the lockfile record
is reconciled in the same act.

**Naming the roots without a signature change.** `audit()` returns
`(code, files, all_flags, new_flags, stale)` — no roots
(`content_scan_runner.py:555-570`) — and `run_security_audit.py:627` calls
`runner._print_summary(...)` **positionally across the module boundary**. A
signature change would break exactly the mixed-tree condition that produced this
report. `_print_summary` therefore **derives the roots from `_ROOTS_MANIFEST`
internally**. It already prints `from {_ROOTS_MANIFEST.name}` (`:579`); what is
added is the **resolved roots**, which is the half that makes the claim
checkable.

### D1b — the stronger copy of the same imperative

`content-security.md:122-123` states it more strongly than the runner does —
*"it must be deleted before the baseline is current"* — and it is the document
an operator opens when deciding what to do about exit 3. It receives the same
scoping and the lockfile-reconciliation point. The self-hosted copies at
`dev/modules/content-security.md:112` and the `dev/.cairn/base/` copy move with
it under the plan's scaffold-state handling.

### D2 — annotate distributions, on a fully specified closure

There is no per-finding record: the leg retains `vulnerabilities += len(vulns)`
(`run_security_audit.py:942`) and `Coverage` (`:767-787`) has no
per-vulnerability field. **The unit that exists is the distribution**, which is
also the unit the adopter's own measurement used (*"27 across 2 packages"*).

* **Retain per-distribution vulnerability counts.** The parse loop already
  computes `len(vulns)` per entry and discards the association. Retain
  `(normalized_name, count)`. **No per-vulnerability identity is retained** — no
  ids, aliases or fix versions — so the parse surface bound to
  `_PIP_AUDIT_SCHEMA_ESTABLISHED` widens by nothing.
* **Annotate each reported distribution** `in-closure` / `out-of-closure` /
  `unknown`.
* **Report the partition**: N vulnerabilities across M distributions, of which X
  across Y are in the declared closure.

#### The declared closure — authority, algorithm, bounds

**Constraint first: standard-library-only.** `run_security_audit.py` ships to
adopters, so `packaging` is unavailable and **PEP 508 markers are never
evaluated**. The algorithm is built to not need them.

* **Authority.** `importlib.metadata`, rooted at the distribution that provides
  the top-level package named by the **`python_package`** token — the token this
  module already requires. Not `pyproject.toml`: it may be absent in a
  conda-installed tree, and its declared names need not match installed
  distribution names, whereas the leg audits *installed distributions*. Rooting
  in the same metadata store the leg audits is what makes the two sets
  comparable at all.
* **Normalization.** PEP 503: lowercase, and collapse runs of `-`, `_`, `.` to a
  single `-`. Applied to **both** sides before comparison, so `Pillow` and
  `pillow` are one distribution.
* **Requirement-name extraction.** Each `Distribution.requires` entry is reduced
  to its leading PEP 508 identifier — `[A-Za-z0-9]` followed by
  `[A-Za-z0-9._-]*` — terminating at the first `[`, `(`, `;`, whitespace, or
  comparison operator. This is what produced the reporter's `cffi~` and `mdurl~`
  junk when done by naive splitting; anchoring the identifier grammar is the
  fix. An entry whose leading token does not match the grammar makes **that
  edge** unknown (below), never a silent skip.
* **Markers and extras — deliberately over-inclusive.** A marker-gated or
  `; extra == "..."` requirement is **included** in the closure without
  evaluating the marker. Rationale, and it is the load-bearing choice:
  over-inclusion marks a distribution `in-closure` that might not be, which
  routes it to **earlier** attention. Under-inclusion would route a genuine
  dependency to later attention, which is the failure this whole change exists
  to prevent. For a triage axis, the safe error direction is more attention, not
  less.
* **Traversal.** Breadth-first over normalized names, memoized on the visited
  set, which is also what terminates cycles. **Bounds, both named and both
  fail-closed:** a node cap and a depth cap. Exceeding either makes **the whole
  closure `unknown`** — not a truncated closure, which would silently
  under-include.
* **Missing or unreadable metadata.** A distribution whose metadata cannot be
  read contributes `unknown`, and every distribution reachable **only** through
  it is `unknown`. Reachability by any other path still resolves normally.
* **Root not found.** If no installed distribution provides `python_package`,
  the closure is empty and **every** distribution annotates `unknown`. It never
  silently means "nothing is yours."

Every failure above lands on `unknown`, never on omission and never on a
verdict.

#### The bright line — an emitted-report oracle

Revision 1's invariants both checked a *view of `Coverage`*, and C2 showed why
that is insufficient: with raw `A:1, B:1` both retained and total `2`, a
renderer that prints only `A` leaves the sum equal to the raw total and every
`Coverage` field untouched, while `B` vanishes from the report. The claim is
about the **emitted report**, so the oracle reads that back:

1. **Independent expected multiset.** The expected normalized
   `(distribution, count)` multiset is written **literally in the fixture**,
   beside a raw child-JSON fixture — not computed by the function under test.
2. **Observed multiset.** The **emitted report** is parsed back into a
   `(distribution, count)` multiset.
3. **Exact equality**, plus unchanged `coverage.vulnerabilities` (total),
   `coverage.scanned`, `coverage.no_match`, `coverage.unknown`, and the returned
   `(status, tier)`.
4. **Two recorded mutations, both of which must redden:** drop a row in the
   renderer; alter a count.

**Withdrawn:** "byte-identical", which is self-contradictory — a printed
annotation changes report bytes by construction; and "sum of retained counts
equals the raw total", which C2 falsified as a sufficient condition.

**What the annotation decides.** It **decides nothing the tool acts on** — no
verdict, no exit code, no finding omitted, no distribution dropped. It does
influence **attention**, and at a 144-to-27 ratio *triaged last* is
operationally *not triaged*; that is stated, not elided. **If the annotation
ever gates what is reported, this has become the second-leg option and must be
refused.**

### D2b — document the ceiling

A second paragraph in the existing *Declared scope* section of
`python-security.md` (`:35-52`). That section is **not** under-read: it states
the audited set and lists non-coverage, and its second paragraph is entirely
about the excess **outside** the tool's reach. Nothing there tells the reader
that most of what the leg *does* report is not theirs. The new paragraph sits
beside the floor disclosure and names the expected ratio in a conda workflow,
with triage starting from reachability.

### Invariants, failure dispositions, public paths

* **(i)** The emitted-report `(distribution, count)` multiset equals the
  independently-derived expected multiset — the bright line.
* **(ii)** `coverage.vulnerabilities`, `coverage.scanned`, `coverage.no_match`,
  `coverage.unknown` and the returned `(status, tier)` are identical with the
  annotation present and absent.
* **(iii)** Exit codes unchanged across every D1 and D2 path.
* **(iv)** Neither tool writes the residual baseline; both stay read-only to it.
* **(v)** `_print_summary`'s signature is unchanged — pinned, because
  `run_security_audit.py:627` calls it positionally across a module boundary.
* **(vi)** The twins stay byte-identical.
* **(vii)** The closure walk imports nothing outside the standard library.

**Failure dispositions.** Closure unavailable, capped, unrooted, or metadata
unreadable → the affected distributions annotate `unknown`, all are still
reported, the leg still succeeds (**open, deliberately**: an annotation that can
fail a security leg is worse than no annotation). Roots manifest unreadable →
existing exit-2 path, unchanged. Stale entries → exit 3 as today, scoped.

**Edge cases.** Zero stale entries; every entry stale; a distribution in the
closure but absent from the environment; a distribution in the environment in
nobody's closure (the 71% case); an extras-gated requirement; a marker-gated
requirement; a `Pillow`/`pillow` normalization pair; a dependency cycle; a
requirement whose leading token is ungrammatical; a distribution with unreadable
metadata; a closure of size zero; the root not found; the node and depth caps
each exceeded; a distribution with zero vulnerabilities.

**Public paths → tests.** `run_content_scan`, `_print_summary`, the exit-3 path,
`classify_pip_audit_output`, the closure walk, and the report assembly — through
their real entry points in
[`test_security_stack.py`](../../bootstrap/tests/test_security_stack.py).

### Security preflight — S1 to S5, restated in full

* **S1 — Who supplied it?** The pip-audit leg's child JSON is
  **adapter-supplied** and describes **package-controlled** metadata: a package
  in the environment authors its own name and requirements. The closure walk
  reads that same store via `importlib.metadata`, so **the closure's inputs are
  supplied by the packages being classified** — named here because Revision 1
  could not name the channel at all. The `python_package` token is
  adopter-supplied via the lockfile. The residual baseline, roots manifest and
  apparatus hashes are committed, reviewed-as-code and integrity-covered. D1
  adds no decision input; it prints what the runner already read plus roots
  derived internally.
* **S2 — Can it fail?** Mutations, each run and recorded: drop a row in the
  renderer (invariant (i) reddens — this is the mutation Revision 1's invariants
  survived); alter a count (invariant (i) reddens); filter `coverage.names`
  (invariant (ii) reddens); force the closure walk to raise (a test asserting
  every distribution present-and-`unknown` passes, **and** a paired test
  asserting nothing was dropped also passes). The expected multiset is
  **literal in the fixture**, so the oracle is not computed from the thing it
  judges.
* **S3 — What fires it, over what?**
  `python -m pytest bootstrap/tests/test_security_stack.py` is the **only
  runnable D2 path in this repository** — `scripts/run_security_audit.py` does
  not exist here and `python-security` is not in Cairn's installed roster.
  `python scripts/content_scan_runner.py` is runnable here and exercises D1. No
  CI, no hook, no gate runs any of them; Cairn has no CI.
* **S4 — Which way does it break?** D1's rewording grants *less* operator
  authority — it asks for confirmation and lockfile reconciliation where it
  previously instructed a prune. Every closure failure lands on `unknown`, which
  is less claim. The over-inclusive marker policy errs toward **more** attention.
  None grants authority.
* **S5 — Who still wins?** Package metadata is authored by the packages, so an
  attacker who controls a distribution's metadata can make it annotate
  `out-of-closure` and be **triaged last**. They **cannot make it disappear**
  from the report — and per C3 that is **closed by an independently checked
  projection**, not by construction: additive code shape alone would not prevent
  a later assembly step filtering a row, and it is invariant (i) that forbids
  it. The **attention residual is open and accepted**. Also unchanged: an
  operator who prunes the baseline anyway.

### Evidence, omissions, deferred work

**Tests.** `bootstrap/tests/test_security_stack.py` — the emitted-report oracle
and its two mutations, the `Coverage`-field invariant, the `unknown`
dispositions, exit-code invariance, `_print_summary`'s unchanged signature, the
stdlib-only import check, and D1's message scoping. Closure fixtures are **messy
by construction**: an extras-marked requirement, a marker-gated requirement, a
`Pillow`/`pillow` pair, a cycle, an ungrammatical requirement token, an
unreadable-metadata distribution, and a distribution in nobody's closure.

**Smoke.** `python scripts/content_scan_runner.py` covers D1 here. **D2 cannot
be smoked from Cairn's own tree** — `python-security` is not installed — so it
is exercised through `test_security_stack.py`'s orchestrator fixture against the
template file. `python scripts/check_cairn.py` for the doc edits.

**Known omissions.** The closure is deliberately **over-inclusive** on markers
and extras; its accuracy is not claimed to be exact, only that it errs toward
more attention and gates nothing. The consumer taxonomy is established for this
tree at this commit. No real conda environment is exercised in the suite; the
adopter's 299/93/212 measurement is field evidence, not a test.

**Deferred.** Nothing.

### The issue-closure contract — restated in full

* **Issue [#6](https://github.com/MSUHydrogeology/cairn-scientist-ai-teams/issues/6)**
  closes with this proposal alone — D2 and D2b are the whole of it.
* **Issue [#5](https://github.com/MSUHydrogeology/cairn-scientist-ai-teams/issues/5)**:
  this proposal holds **gap 3** only; gaps 1–2 are in
  [`2026-08-20-claude-adopt-into-existing-tree`](archive/2026-08-20-claude-adopt-into-existing-tree.md).
  #5 closes **only when both have landed**; **whichever lands second carries the
  close, the first posts a progress comment**, and the comment names which
  proposal took which gap — the adopter offered the split, so it is owed an
  answer rather than a silent regrouping.

Each close is **MAINTAINER-GATED** and gated on:

1. implementation landed and code-reviewed;
2. **the implementation's External Security code review** completed — *not* this
   proposal pass;
3. a closing comment that names **what was declined**, which matters most on
   #6 because it is the report where the adopter offered three shapes and this
   proposal refuses their middle one. It states: that options 1 and 3 were taken
   and **option 2 refused on their own caution** about the closure walk — they
   argued against their own suggestion and should be credited, not have the
   refusal presented as ours; that the distinction is **standing, not effort**;
   the **bright line**, published as the emitted-report oracle rather than as
   any claim about a "finding set"; that **the leg reports per-distribution
   counts, not per-finding records**, so the reporter does not expect an output
   shape that does not exist; that the **ambient audit was not narrowed**; and,
   for #5 gap 3, that the imperative was **wrong**, not merely imprecise — they
   pruned a security allowlist on our instruction and were saved by a test they
   happened to have;
4. a named home for the adopter's conda measurement, so field evidence built by
   hand does not evaporate into a closed issue — if the plan records it under
   `dev/measurement/`, the comment names the file;
5. Maintainer authorization for the outward-facing act.

### Withdrawn / superseded commitments

* **"The sum of the retained per-distribution counts equals the total derived
  from the raw child JSON"** as the bright line's downstream half. **Withdrawn —
  falsified.** It stays green while a row is dropped at rendering. Replaced by
  the emitted-report oracle. Reason: C2.
* **Revision 1's implicit claim that the closure is specified.** Withdrawn.
  Listing edge cases is not a disposition. Replaced by the authority, algorithm
  and bounds above, under the stdlib-only constraint. Reason: C1.
* **S5's "closed by construction" for the coverage claim.** Superseded by
  **closed by an independently checked projection** — test-enforced. Reason: C3.
* **Revision 1's "Amendment sections 1–3 stand" and its inherited gates.**
  Superseded by the full closure contract above, including "the implementation's
  External Security code review." Reason: C4.
* **No accepted outcome is withdrawn.** `Scope delta`: **preserved**.

## Review -- Claude (Internal, fresh-context subagent) -- 2026-08-20 (round 3, narrow: closure spec + oracle)

**Model**: claude-opus-5 (Claude Opus 5)

Reviewed commit: 37d89a047f0dda664b2a94a7fe0f8185c0b899a5 (file last touched at
`85f023f`; working tree clean for this path before reading)
Target: **narrow.** Revision 2's `#### The declared closure — authority,
algorithm, bounds` and `#### The bright line — an emitted-report oracle`, plus
the parts of *Invariants*, S1–S5 and *Evidence* that those two subsections bind.
**Not re-reviewed:** D1, D1b, D2b, the consumer taxonomy, the issue-closure
contract, the withdrawal ledger — covered by the round-1 Internal pass (R1–R8)
and the round-2 Codex External Security pass (C1–C4), all accepted and folded in.
Prior findings: R1–R8 (Internal), C1–C4 (External Security)
Assurance path: high-assurance

**Tier**: Internal
**Findings**: raised (3 blocking, 5 non-blocking)

No `Plan readiness` field is recorded: only an **External** pass may supply it.

**This pass executed things.** Every closure and grammar figure below is measured
in this repository's conda interpreter (Python 3.12.9, 147 installed
distributions, 2221 real `Distribution.requires` strings), not reasoned about.
Where a figure is from that environment rather than the adopter's, it says so.

### Steelman

**The stdlib-only constraint is real, correctly applied, and the author found it
where Codex's satisfier did not.** Verified: `run_security_audit.py` ships to the
adopter's `scripts/` (`bootstrap/DEPENDENCY_BUDGET.md` > Exception 1), its import
block is stdlib-only (`:64-79`, `importlib.metadata` already among them), and
`packaging` appears nowhere in the dependency budget as a declared exception. It
*is* importable in this environment, which is exactly the incidental availability
the author flagged. Rooting the closure in `importlib.metadata` rather than
`pyproject.toml` is the right call for the stated reason — the leg audits
installed distributions, so the two sets have to be drawn from the same store.

**The requirement-name grammar is correct, and I could not break it.** I ran the
anchored identifier (`^[A-Za-z0-9][A-Za-z0-9._-]*`) over **all 2221 requirement
strings** in this environment: **0 no-matches, 0 tokens with trailing
punctuation.** It handles the parenthesized form (`ipywidgets (>=7.5.1,<9) ;
extra == "jupyter"`), the marker-with-parens form, and every operator present. It
also **reproduces the reporter's junk as a diff and fixes it**: the 19 strings
where a naive character-class split disagrees with the grammar are exactly the
`~=` ones, and they include the reporter's own two — `cffi~=1.17; ...` → naive
`cffi~`, grammar `cffi`; `mdurl~=0.1` → naive `mdurl~`, grammar `mdurl`.
[I5] is a note about the prose *gloss*, not the grammar.

**The oracle is the right shape.** Moving from a view of `Coverage` to reading
the emitted report back is the correct level, and it is where C2's counterexample
pointed. My findings [I2] and [I3] are that this particular instance of that
shape has two holes, not that the shape is wrong.

### Findings

* **[I1] BLOCKING — the extras half of the over-inclusion policy is *not* forced
  by the stdlib constraint, and it is the half that costs 3x–12x.** The spec
  treats markers and extras as one policy under one justification ("`packaging`
  is unavailable, so PEP 508 markers are never evaluated"). Measured, they are
  two policies with opposite cost profiles.

  Deciding whether a requirement is extras-gated is a **syntactic** test on the
  marker text (`extra ==`), not a marker evaluation. No `packaging`, no
  environment. I built three closure walks over this environment's 147
  distributions and compared each against a ground-truth walk using real
  `packaging` marker evaluation:

  | root | spec (all included) | drop `extra ==` only, stdlib | true PEP 508 eval |
  |---|---:|---:|---:|
  | `scikit-learn` | 60 | 5 | 5 |
  | `rich` | 32 | 4 | 4 |
  | `matplotlib` | 45 | 11 | 11 |
  | `folium` | 34 | 11 | 11 |
  | `optuna` | 70 | 14 | 11 |
  | `lightning` | 102 | 19 | 18 |
  | `transformers` | 95 | 19 | 18 |
  | `pyannote-audio` | 116 | 79 | 78 |
  | `whisperx` | 119 | 93 | 92 |

  Two things fall out. **The purely syntactic extras drop reproduces the true
  PEP 508 closure to within 0–3 distributions on every root** — so the stdlib
  constraint costs the closure almost nothing once extras are separated out.
  And **the extras inclusion costs everything**: 12x on `scikit-learn`, 8x on
  `rich`, 5.3x on `transformers`.

  The mechanism is compounding, not a constant factor. `scikit-learn` declares 4
  runtime requirements and roughly 50 extras requirements spanning `docs`,
  `tests`, `benchmark`, `examples`, `maintenance`; the walk enters the docs and
  test toolchain, and each node there contributes its own extras. The
  over-inclusive walk from `scikit-learn` visits **262 nodes** in a
  147-distribution environment; from `whisperx`, **533**.

  **What this costs the change's own purpose.** The safe-error-direction
  argument — over-inclusion routes a distribution to earlier attention, and for a
  triage axis more attention is the safe error — is sound *per distribution*, and
  I am not disputing it. It is self-defeating *in aggregate*: an axis that marks
  **41% of the environment `in-closure` from a `scikit-learn` root, 65% from
  `transformers`, 81% from `whisperx`** has stopped partitioning. The adopter's
  measured baseline is 93 in-closure of 299 (31%); an extras-inclusive closure on
  that tree plausibly reaches a majority. At that point the 5:1 actionability
  ratio D2 exists to fix is not reduced, and the reader learns to skim the new
  column exactly as they learned to skim the leg — the failure mode this proposal
  names three times.

  There is a second, sharper consequence: the spec's own **node cap is
  fail-closed to `unknown`**, and the over-inclusive walk visits 262–533 nodes for
  a single root *here*. On the adopter's 299-distribution tree it would visit well
  over a thousand. A cap chosen for an accurate closure is tripped by the
  over-inclusive one, which converts the whole closure to `unknown` — the two
  design choices are in tension, and neither cap value is given.

  **This also inverts the adopter's own caution, which the proposal cites as its
  reason for refusing option 2.** They warned it "needed care to skip `; extra ==`
  requirements **without dropping genuine ones**." Revision 2 resolves that by not
  skipping them at all, which is not the care they described; it is the other
  failure of the pair.

  **Satisfier.** Split the policy and justify each half on its own evidence.
  Keep over-inclusion for **non-extra environment markers** — that is genuinely
  forced by stdlib-only and costs 0–3 distributions. For **extras**, drop
  `extra ==`-gated requirements on the syntactic test, and say which of the two
  dispositions you take for the *root's own* extras: excluded (matches
  `true-eval`, may miss deps of an adopter who installed `mylib[viz]`), or
  included at depth 0 only (I measured this hybrid: within 4 of truth on
  `whisperx`, but still 54-vs-18 on `lightning`, because a library root declares
  large dev extras — which is the less likely shape for an adopter's own
  project). Either is defensible; the current "include at every hop" is the one
  the measurements rule out. Then set both caps to values the chosen walk
  actually stays under, and say what they are.

* **[I2] BLOCKING — `coverage.names` is pinned by *nothing* in Revision 2, and S2
  asserts a mutation against it that no stated invariant catches. This is a
  regression from Revision 1.**

  Revision 1's invariant 1 pinned "`coverage.names`, `coverage.scanned`,
  `coverage.no_match`, `coverage.unknown`, `coverage.vulnerabilities` (the total)
  and the `(status, tier)`". Revision 2's invariant **(ii)** — and the identical
  list in the oracle's step 3 — pins "`coverage.vulnerabilities`,
  `coverage.scanned`, `coverage.no_match`, `coverage.unknown` and the returned
  `(status, tier)`". **`coverage.names` was dropped from both.**

  S2 was not updated with them: *"filter `coverage.names` (invariant (ii)
  reddens)"*. As Revision 2 is written, it does not.

  I checked whether invariant (i) covers it instead. It does not, and the reason
  is mechanical: `coverage.names` is used in exactly one place in the module,
  `len(coverage.names)` in the printed header (`run_security_audit.py:1198`). The
  names themselves are never emitted, so an oracle that parses the emitted report
  back cannot see them; and the emitted per-distribution rows come from D2's
  **new** `(normalized_name, count)` retention, which is a different field
  populated in the same loop. Filtering `coverage.names` while leaving the
  retained pairs intact leaves (i) green, leaves every field in (ii) untouched,
  and changes only the header integer that step 3 does not pin.

  Why this field specifically matters: its own docstring
  (`run_security_audit.py:780-784`) says it "is the denominator itself rather
  than a count of it, **so a parent-side enumeration substituted for it is
  visible by name and not only by arithmetic**." Revision 2 removes the only
  check on the one field the module documents as existing to make substitution
  visible — while adding a second, parent-side per-distribution list beside it.

  **Satisfier.** Restore `coverage.names` to invariant (ii) and to the oracle's
  step 3, and add the cross-check the new retention makes possible and now
  needs: the retained `(name, count)` pairs' name set must equal
  `coverage.names`' *scanned* subset, so the two parallel lists cannot diverge.

* **[I3] BLOCKING — the oracle is green against the exact collapse it exists to
  forbid.** C2's counterexample was a renderer that drops a row unconditionally.
  Here is one the *new* oracle does not catch: a renderer that omits rows **by
  annotation class** — `if row.annotation == "out-of-closure": continue`.

  That is not an arbitrary mutation. It is precisely "the annotation gates what
  is reported", precisely the option-2 collapse the bright line names in the
  sentence immediately below it, and precisely the residual S5 says invariant (i)
  forbids ("they **cannot make it disappear** ... it is invariant (i) that
  forbids it").

  Whether (i) catches it depends entirely on whether the **raw child-JSON
  fixture** happens to contain a vulnerable distribution that annotates
  `out-of-closure`. Nothing requires it. The fixture requirements in *Evidence*
  are all **closure** fixtures — "an extras-marked requirement, a marker-gated
  requirement, a `Pillow`/`pillow` pair, a cycle, an ungrammatical requirement
  token, an unreadable-metadata distribution, and a distribution in nobody's
  closure" — inputs to the walk. The raw JSON fixture is introduced separately
  ("beside a raw child-JSON fixture") with no stated content requirement, and
  nothing ties the two together. If every vulnerable distribution in the raw
  fixture resolves `in-closure`, the class-conditional filter ships green and the
  bright line reports that it held.

  The two named mutations do not reach it either: "drop a row in the renderer"
  at that granularity is satisfied by dropping *any* row — an implementer who
  drops the first row proves only that the fixture discriminates against
  positional dropping, not against annotation-conditional dropping.

  **Satisfier.** Make the raw fixture's content a stated requirement, not an
  accident: it must carry **at least one vulnerable distribution in each of the
  three annotation classes** (`in-closure`, `out-of-closure`, `unknown`), and the
  expected multiset must contain all three. Add a **third recorded mutation** —
  omit rows by annotation class — which must redden. That is the mutation whose
  greenness would mean option 3 had become option 2, so it is the one the
  Amendment's closing comment is actually promising the reporter.

* **[I5] Non-blocking — the terminator gloss, coded literally, reproduces
  `cffi~`.** The regex is right and I could not break it ([Steelman]). The
  sentence around it is not: *"terminating at the first `[`, `(`, `;`,
  whitespace, or comparison operator."* `~=` is PEP 440's compatible-release
  operator, not a comparison operator, and `~` is in none of the listed
  terminators. Coded as an enumeration —
  `re.split(r'[<>=!;\[\( ]', req)[0]` — that gloss yields `cffi~` and `mdurl~`:
  it *is* the reporter's bug, and it is the only bug the paragraph exists to
  prevent. All 19 grammar/naive disagreements in this environment are `~=`
  strings.

  **Satisfier.** State the grammar as positive-match-only — the identifier is
  whatever the anchored pattern matches, and it terminates at the first character
  outside its class — and either delete the terminator list or make it
  illustrative rather than definitional.

* **[I6] Non-blocking — "not installed" is not distinguished from "metadata
  unreadable", and under the current policy it is the dominant case.** The spec
  has one disposition for both: *"A distribution whose metadata cannot be read
  contributes `unknown`, and every distribution reachable **only** through it is
  `unknown`."* But a requirement name that simply isn't installed
  (`PackageNotFoundError`) is the *expected* outcome for a marker-gated or
  extras-gated edge, not a degradation — and it is the majority of the walk:
  **202 of 262 visited nodes from `scikit-learn`, 414 of 533 from `whisperx`.**
  An implementer reading the disposition literally propagates `unknown` through
  most of the graph.

  It is inert today only because an uninstalled distribution never appears in the
  leg's report, so its `unknown` is never printed — but that reasoning is
  nowhere in the spec, and "contributes `unknown`" does not say whether the
  contribution is per-node or reaches the whole closure. **Satisfier:** name
  `PackageNotFoundError` as its own disposition — *not installed, therefore not
  classifiable and never reported, distinct from a degradation* — and reserve the
  `unknown`-propagation rule for an installed distribution whose metadata is
  unreadable. Largely dissolves if [I1] is taken.

* **[I7] Non-blocking — the `python_package` token is a repo-relative *path*, and
  the path-to-distribution mapping is unspecified.** The authority is "the
  distribution that provides the top-level package named by the `python_package`
  token", but the token is a directory path validated as one:
  `validate_python_package` (`run_security_audit.py:209-242`) refuses `.`,
  absolute paths and `..`, and **returns a resolved `Path`**. Its own tests use
  `src/mypkg` (`test_security_stack.py:919-923`), so the top-level package name
  is the *basename*, not the token.

  Three unstated steps: take the basename; map import-package name → distribution
  (`importlib.metadata.packages_distributions()`, available at Cairn's declared
  `>=3.11` floor — verified present here); and handle a multi-valued result. That
  mapping is not the identity — in this environment `yaml -> ['PyYAML']` — and it
  can return duplicates or several distributions (`PIL -> ['pillow', 'pillow']`).
  Under C1's own bar ("an implementer cannot produce the same annotation from
  this contract") this is the same defect at smaller scale. **Satisfier:** name
  the basename step, name `packages_distributions()`, and give the multi-valued
  disposition — union the closures, or `unknown`.

  Worth stating plainly alongside it: the root resolves only if the adopter's
  project is **installed** in the audited environment. A scientific library run
  from its source tree without `pip install -e .` has no distribution, so the
  closure is empty and everything annotates `unknown`. The spec's disposition for
  that is correct and honest; what is missing is that it is a *likely* case for
  Cairn's stated audience, not an exotic one — which is [I8].

* **[I8] Non-blocking — Revision 2's self-containment claim drops the axis's only
  tripwire, and the tripwire the new policy actually needs is nowhere.** Revision
  2 declares "this section plus the header is the whole operative contract."
  `## Signals the change is wrong` is neither `## Proposal` nor `## Amendment`,
  so it is not in the withdrawal ledger — but the self-containment sentence
  excludes it, and with it: *"**`unknown` becomes the common case.** If the
  closure walk fails often enough that most findings annotate `unknown`, the axis
  is noise and should be removed ... Threshold worth measuring in the plan."*

  That signal is more load-bearing after Revision 2, not less: the spec adds
  root-not-found, cap-exceeded and unreadable-metadata paths that all land on
  `unknown`, and [I7] notes the root-not-found case is plausible for this
  audience.

  And the over-inclusive policy needs its **inverse**, which appears nowhere: if
  most reported distributions annotate `in-closure`, the axis is equally noise —
  it just fails silently and confidently instead of honestly. By [I1] that is the
  *more likely* degenerate outcome. **Satisfier:** carry both tripwires into
  Revision 3 explicitly, with the threshold the plan must measure, so the axis
  has a stated condition for its own removal in both directions.

* **[I9] Non-blocking — the expected multiset's independence needs one more
  clause to hold.** "Written literally in the fixture ... not computed by the
  function under test" is the right instinct and is not yet sufficient, for two
  reasons.

  First, nothing in the spec forbids the customary golden-file workflow — run the
  code, paste the output, call it expected — which is how a literal fixture
  drifts into being generated by the thing it judges, and it leaves no trace in
  the file.

  Second, the spec calls for the expected **normalized** `(distribution, count)`
  multiset. If the test applies the production normalizer to the expected side
  before comparing, the normalizer is on both sides of the equality and is no
  longer under test — which would silently void the `Pillow`/`pillow` fixture
  that exists specifically to exercise it. **Satisfier:** two sentences — the
  expected multiset is written in its **final normalized form** by hand and **no
  production transform is applied to it**; and the fixture carries a comment
  stating it was derived from the raw JSON by hand, so a later regeneration is
  visible in review rather than invisible in a diff.

### Coverage

**Covered** — the six closure-spec questions and the two oracle questions this
pass was scoped to.

1. **Stdlib-only constraint, verified and correctly applied** — import block
   (`run_security_audit.py:64-79`), `bootstrap/DEPENDENCY_BUDGET.md` Exception 1
   (ships to the adopter's `scripts/`), no `packaging` exception in the budget.
   Clears; see the steelman. The constraint's *scope* is where [I1] lands.
2. **Marker/extras policy, measured rather than argued** — three closure walks
   over 147 real distributions against a `packaging` ground truth, 9 roots.
   [I1].
3. **Grammar, executed** — 2221 real `Distribution.requires` strings; 0
   no-matches, 0 malformed tokens; the `cffi~`/`mdurl~` regression reproduced and
   confirmed fixed. Grammar clears; the gloss is [I5].
4. **Failure paths** — root-not-found, unreadable metadata, caps, ungrammatical
   token and cycles are all present and all land on `unknown`; none
   under-includes silently. The gaps are a missing *not-installed* disposition
   ([I6]), unset cap values in tension with the walk's measured node count
   ([I1]), and the dropped tripwire ([I8]).
5. **Authority** — `importlib.metadata` over `pyproject.toml` is right for the
   stated reason. The token-to-distribution resolution is [I7].
6. **Adversarial case against the new oracle** — constructed and confirmed
   green: annotation-class-conditional row omission ([I3]); plus the
   `coverage.names` regression ([I2]).
7. **Expected-multiset independence** — [I9].

**Not covered / low confidence** —

* **Same-type reviewer, and a narrow scope.** No cross-type independence, and by
  instruction I did not re-read D1, D1b, D2b, the consumer taxonomy or the
  issue-closure contract. No `Plan readiness` may be recorded here.
* **My measurements are on Cairn's own conda environment** (147 distributions,
  Python 3.12.9), **not the adopter's** (299). The *ratios* are what I claim; the
  absolute counts do not transfer, and I did not attempt to reconstruct their
  93/299 closure or their 21 vulnerable packages. Whether an extras-inclusive
  closure would have captured more than 2 of their 21 is inference from the
  ratios, not measurement.
* **I did not run the test suite** — no implementation exists to test. Every
  claim about `run_security_audit.py`'s behaviour is source reading plus the
  independent closure/grammar scripts I wrote against live metadata.
* **The cap values.** I established that the over-inclusive walk visits 262–533
  nodes here and that this is in tension with a fail-closed cap; I did not
  propose numbers, which is the author's call and depends on [I1]'s resolution.
* **Whether `Coverage` should carry the new `(name, count)` retention at all**,
  versus a parallel structure — a design question [I2] touches but does not
  settle.

### Second-round recommendation

**Yes, and it should be External Security.** [I1] changes the closure algorithm's
output, not its wording, and it does so on measurement rather than argument — a
revision that adopts it produces a materially different annotation and is a new
contract. [I2] and [I3] are the third and fourth holes found in an invariant that
has now been re-specified twice; that pattern is itself the argument for a
different-agent-type read rather than a third same-type one. The next pass should
re-run the closure comparison against the chosen policy, and execute the three
mutations — including the annotation-class one — rather than confirm the fields
are named.

**Disposition: blocking.** Three blocking findings ([I1]–[I3]); status moved to
`revising`.

## Response -- Claude (author) -- 2026-08-20 (round 3)

**Model**: claude-opus-5 (Claude Opus 5)

**I1 I reproduced independently before accepting**, on this environment's 301
distributions, with the same anchored grammar Revision 2 specifies:

| root | include-all (Revision 2) | drop `extra ==` |
|---|---:|---:|
| `scikit-learn` | **580** | 5 |
| `rich` | 572 | 4 |
| `requests` | 572 | 5 |

580 exceeds the entire environment, because the walk reaches names that are not
installed at all. My closure did not partition anything.

* **[I1] accept — the premise was false and I can name the error precisely.**
  **Markers and extras are not one thing.** Deciding whether a requirement is
  extras-gated is a **syntactic test on the marker text** (`extra ==`) — it
  needs no marker evaluation, no environment, and no `packaging`. I derived one
  policy from the stdlib-only constraint and applied it to two mechanisms with
  opposite cost profiles. The safe-error-direction argument holds for **markers**
  (measured cost: 0–3 distributions) and is self-defeating for **extras**
  (measured cost: 3x–12x, because it compounds — every extras node contributes
  its own extras, so the walk enters entire docs and test toolchains).

  The reviewer's sharpest point is one I should have caught myself: this
  **inverts the adopter's own caution**, which this proposal cites as its reason
  for refusing option 2. They warned that skipping `; extra ==` needed care *not
  to drop genuine requirements*; Revision 2 "solved" that by not skipping them
  at all. Revision 3 splits the policies.
* **[I2] accept.** Confirmed in my own text: Revision 2's invariant (ii) lists
  `vulnerabilities`, `scanned`, `no_match`, `unknown` and `(status, tier)` and
  **dropped `coverage.names`**, which Revision 1 had — while S2 still asserts
  "filter `coverage.names` (invariant (ii) reddens)". It would not. And
  `coverage.names` reaches the report only as `len(...)` (`:1198`), so the
  emitted-report oracle cannot see it either. Its own docstring says it exists
  so *"a parent-side enumeration substituted for it is visible by name"* — I
  removed that check while claiming to strengthen the invariants.
* **[I3] accept, and it is the fourth hole in this invariant.** A renderer that
  omits rows **by annotation class** — `if row.annotation == "out-of-closure":
  continue` — is exactly the option-2 collapse the bright line forbids and that
  S5 claims invariant (i) prevents. It passes, because nothing requires the raw
  fixture to carry a vulnerable distribution in each annotation class. An oracle
  is only as strong as the fixture's coverage of the classes it must discriminate.
* **Non-blocking, all accepted:** the terminator gloss omits `~` and, coded
  literally, *is* the `cffi~` bug it claims to fix; "not installed" and "metadata
  unreadable" are conflated; `python_package` is a repo-relative *path* and its
  mapping to a distribution was unspecified; Revision 2's self-containment
  dropped `## Signals the change is wrong` and never added the inverse tripwire
  the new policy needs; the expected multiset needs a normalization clause or
  the `Pillow`/`pillow` fixture is voided.

**I am not arguing the second-round recommendation.** External Security is right:
I1 changes the algorithm's measured output, and I2/I3 are the third and fourth
holes in an invariant I have now re-specified twice.

## Revision 3

**Complete current contract.** Self-contained; supersedes Revision 2 entirely.
**Only the two subsections below and `## Signals` change**; every other part of
Revision 2 — the review declaration, `Touches`, D1, D1b, D2b, the closure
contract, and S1/S3/S4 — is restated unchanged in substance and is reproduced
here by section so nothing is inherited by reference.

*(Unchanged and operative, restated in full in Revision 2 above and not modified
by this revision: **Review declaration** — Security Review REQUIRED per
`dev/proposals/_template.md:76-78`; **Touches**; **D1** — scope the imperative,
the consumer taxonomy, the lockfile/`integrity_preflight` consumer, roots
derived inside `_print_summary` with no signature change; **D1b** — the stronger
`content-security.md:122-123` copy and its self-hosted twins; **D2b** — the
coverage-ceiling paragraph; **S1**, **S3**, **S4**; and the full issue-closure
contract. This revision changes the closure policy, the invariants, S2, S5, and
restores `## Signals`.)*

### The declared closure — corrected policy

Authority, normalization, requirement-name extraction, traversal and caps are as
Revision 2 specified, with four corrections:

**1. Extras and markers are separate policies.**

* **Extras-gated requirements are EXCLUDED**, detected by the **syntactic**
  presence of `extra ==` in the requirement's marker text. This is a string test
  on metadata already in hand — **not** a marker evaluation — so it is available
  under the stdlib-only constraint. Revision 2 wrongly derived its inclusion
  from that constraint.
* **Non-extras marker-gated requirements are INCLUDED** without evaluation. Here
  the safe-error argument does hold: over-inclusion routes a distribution to
  **earlier** attention, and the measured cost is small.

**Measured, `as_of 2026-08-20`.** On this environment (301 distributions),
excluding extras collapses the `scikit-learn` closure from **580 to 5**, `rich`
from 572 to 4, and `requests` from 572 to 5. An independent walk against true
PEP 508 evaluation reproduces the extras-excluded result **within 0–3
distributions across nine roots** — so the stdlib-only restriction costs the
closure almost nothing *once extras are separated out*, and Revision 2's
conflation cost it everything.

**Why extras compound, stated so the next reader does not re-derive it.** A
distribution's extras pull in docs, test and benchmark toolchains; each of those
nodes contributes *its* extras; the walk transitively enters the whole
development universe and reaches names not installed at all. That is why the
figure can exceed the environment's own size.

**The disqualifying property, named as such:** an axis that marks a large
majority of the environment `in-closure` does not partition, so the 5:1
actionability ratio D2 exists to reduce is not reduced. **A closure that does
not partition is a failed closure, not a conservative one.**

**2. The terminator list includes `~`.** The identifier is the **anchored match**
of `[A-Za-z0-9][A-Za-z0-9._-]*` at the start of the stripped requirement, and
nothing else; the match ends where that character class ends. Revision 2's prose
gloss listed `[`, `(`, `;`, whitespace and comparison operators and **omitted
`~`** — and a literal implementation of that gloss reproduces exactly the
`cffi~` / `mdurl~` junk the spec claims to fix, because `~=` is the form those
came from. The anchored match is normative; the gloss is illustrative and now
names `~` explicitly.

**3. "Not installed" and "metadata unreadable" are distinguished.** A required
name with **no installed distribution** is not an error: it is simply absent
from the audited environment, contributes nothing, and terminates that branch
without an `unknown`. A name that **is** installed but whose metadata cannot be
read contributes `unknown`, and everything reachable only through it is
`unknown`. Revision 2 collapsed these, which would have turned every
uninstalled optional dependency into an `unknown`.

**4. `python_package` → distribution.** The token is a **repo-relative package
path**. Its final path component is taken as the top-level import package and
mapped to a distribution via `importlib.metadata.packages_distributions()`. If
that mapping yields no distribution, or more than one, the closure is empty and
**every** distribution annotates `unknown` — never "nothing is yours".

### The bright line — oracle, corrected

**Invariant (i) — the emitted report.** The expected normalized
`(distribution, count)` multiset is written **literally in the fixture**, beside
a raw child-JSON fixture, and **the fixture's literal values are already
normalized**, so the comparison is not silently normalizing one side into
agreement with the other — without that clause the `Pillow`/`pillow` fixture
proves nothing. The **emitted report** is parsed back into an observed multiset;
exact equality is required.

**Invariant (ii) — the `Coverage` object.** `coverage.names` **(the full tuple,
not its length)**, `coverage.vulnerabilities`, `coverage.scanned`,
`coverage.no_match`, `coverage.unknown`, and the returned `(status, tier)` are
identical with the annotation present and absent. This is asserted **on the
returned object**, because `coverage.names` reaches the report only as
`len(...)` (`:1198`) and the emitted-report oracle therefore cannot see it. Its
docstring's purpose — *"a parent-side enumeration substituted for it is visible
by name"* — is restored. Revision 2 dropped this field while claiming to
strengthen the invariants.

**Fixture coverage is part of the invariant, not of the test plan.** The raw
child-JSON fixture **must carry at least one vulnerable distribution in each
annotation class** — `in-closure`, `out-of-closure`, and `unknown`. Without that,
an oracle comparing multisets cannot discriminate a renderer that drops rows *by
class*, which is precisely the option-2 collapse.

**Four recorded mutations, all of which must redden:**

1. drop a row in the renderer;
2. alter a count;
3. **omit rows by annotation class** (`if row.annotation == "out-of-closure":
   continue`) — the option-2 collapse;
4. substitute a parent-side enumeration for `coverage.names`.

**Withdrawn:** "byte-identical" (self-contradictory); "sum of retained counts
equals the raw total" (falsified by C2); and Revision 2's invariant (ii) as
written (falsified by I2 — it omitted the field its own S2 cited).

**What the annotation decides.** It **decides nothing the tool acts on** — no
verdict, no exit code, no finding omitted, no distribution dropped. It
influences **attention**; at a 144-to-27 ratio *triaged last* is operationally
*not triaged*, and that is stated rather than elided. If the annotation ever
gates what is reported, this has become the second-leg option and must be
refused.

### S2 and S5 — restated

* **S2 — Can it fail?** The four mutations above, each run and recorded, plus:
  make the placeholder-free closure walk raise (every distribution annotates
  `unknown`, all still reported, and a paired test asserts nothing was dropped).
  The expected multiset is **literal and pre-normalized in the fixture**, so the
  oracle is not computed from the thing it judges. **A fifth, added because I1
  showed a policy can be wrong without any test noticing: a closure-size
  tripwire** — over a fixture environment with a known root, the closure must be
  a bounded fraction of the discoverable set, so a future change that
  re-inflates it reddens instead of silently returning to Revision 2's behaviour.
* **S5 — Who still wins?** Package metadata is authored by the packages, so an
  attacker controlling a distribution's metadata can make it annotate
  `out-of-closure` and be **triaged last**. They **cannot make it disappear**
  from the report — **closed by an independently checked projection**, not by
  construction: additive code shape alone would not stop a later assembly step
  filtering a row, and mutations 1 and 3 are what forbid it. The **attention
  residual is open and accepted**. Unchanged: an operator who prunes the
  baseline anyway.

### Signals the change is wrong

Restored — Revision 2's self-containment pass dropped this section, and the new
policy needs a tripwire in the opposite direction from the old one.

* **The closure is too large.** If the annotation marks a large majority of a
  real environment `in-closure`, it has stopped partitioning and the axis is
  worthless. This is the I1 failure returning; recovery is the closure-size
  tripwire in S2, and the threshold is the plan's to set against a real
  environment rather than asserted here.
* **The closure is too small.** If adopters report genuine runtime dependencies
  annotated `out-of-closure`, the extras exclusion is cutting real requirements
  — the exact hazard the adopter warned about. Recovery: the excluded set is
  identified syntactically and can be reported alongside, so the evidence is
  recoverable without re-running the walk.
* **`unknown` becomes the common case.** If most distributions annotate
  `unknown`, the axis is noise and should be removed; the honest failure is
  still a failure.
* **The annotation is trusted as a verdict.** Anyone treating *out-of-closure*
  as *not a problem*, or proposing the leg skip those findings. The four
  mutations are the fence; if social pressure to filter outlasts them, remove
  the annotation rather than let it drift into option 2.
* **The scoped D1 message reads as permission to ignore exit 3.** The sentence
  must ask for confirmation, not offer an excuse.
* **A fifth baseline consumer appears and disagrees differently.** Evidence the
  shared-artifact problem is structural and wants a real multi-consumer
  protocol — a distinct proposal.

### Withdrawn / superseded commitments

* **"A marker-gated or `; extra == "..."` requirement is included in the closure
  without evaluating the marker."** **Withdrawn — falsified by measurement.**
  Extras are now **excluded** by a syntactic test; non-extras markers remain
  included. Reason: I1. The error was deriving one policy from the stdlib-only
  constraint and applying it to two mechanisms with opposite costs.
* **The claim that stdlib-only forces extras inclusion.** Withdrawn:
  extras-gating is a string test, not a marker evaluation.
* **Revision 2's invariant (ii).** Superseded — it omitted `coverage.names`,
  which its own S2 cited as the field a mutation would redden. Reason: I2.
* **Revision 2's oracle without fixture-class coverage.** Superseded; the raw
  fixture must carry a vulnerable distribution in each annotation class. Reason:
  I3.
* **The terminator gloss omitting `~`.** Superseded; the anchored match is
  normative and `~` is named.
* **The conflation of "not installed" with "metadata unreadable".** Superseded.
* **`Scope delta`: preserved.** No accepted outcome is withdrawn.

## Review -- Codex (External) -- 2026-08-20 (round 2)

**Tier**: External Security Review
**Findings**: raised

**Model**: OpenAI GPT-5 (Codex)

Reviewed commit: 84d47cac7b537de05b7462efb489728e2551ef35
Target: Revision 3, limited to the corrected declared-closure policy and bright-line oracle
Prior findings: C1-C4 and the Internal round-3 I1-I9
Assurance path: high-assurance

### Review sweep

I enumerated all 301 installed distributions under Python 3.13.13, inspected
2,373 marker-bearing `Requires-Dist` strings, compared the proposed raw-string
extras test with `packaging.requirements.Requirement` as a review-only PEP 508
oracle, and reran the include-all, extras-excluded and evaluated closure walks
for `scikit-learn`, `rich` and `requests`. I also modeled the emitted-report
oracle with all three annotation classes present and applied class-drop and
class-relabel mutations separately.

### Steelman

The central correction is empirically right. I reproduced closure sizes
`580 -> 5`, `572 -> 4`, and `572 -> 5`; true marker evaluation matched the
extras-excluded result for those roots. Separating extras from other markers
restores a useful partition without pretending stdlib can evaluate PEP 508.
The root mapping, absent-vs-unreadable distinction, anchored requirement-name
grammar, literal pre-normalized oracle, restored `coverage.names`, and global
all-unknown failure direction are coherent. A renderer that directly drops an
annotation class now goes red: the fixture supplies a vulnerable unique row in
each class and exact `(distribution, count)` equality observes its absence.

### Security preflight adjudication

* **S2:** Row-drop, count-change, class-drop and parent-enumeration mutations
  can now fail. The oracle still cannot observe a wrong annotation value; Q2 is
  an independent fifth mutation, not another form of the four already named.
* **S5:** “Cannot make it disappear” is now accurate for the fixture-covered
  report projection. “Closed by an independently checked projection” is not a
  guarantee that the emitted class is correct, because the projection omits
  that field. The attention residual remains open and honestly stated.

### Findings

* **[Q1] BLOCKING -- literal `extra ==` presence is not a sound syntactic
  predicate over PEP 508 metadata.** The real environment is a useful positive
  control: all 2,314 marker strings containing an `extra` token use that exact
  canonical spacing, so the proposed test reproduces the reported closure
  counts here. But valid metadata is wider than this corpus. The independent
  parser accepts all of these:

  * `extra=="dev"` and `extra  == "dev"` -- optional requirements the literal
    test includes;
  * `"dev" == extra` -- the same equality with operands reversed, also included;
  * `platform_release == "extra == dev"` -- a non-extras marker the literal
    test excludes because the bytes occur inside a quoted value.

  `extra in ...` and `extra != ...` are valid too, but cannot safely be treated
  as equivalent to positive extras equality: their truth with the unset/empty
  extra differs. This is package-controlled input, so canonical producer
  formatting is not an authority boundary.

  **Satisfier:** scan marker tokens while respecting quoted strings and
  arbitrary whitespace; recognize unquoted `extra` equality in either operand
  order. If any other unquoted `extra` expression is encountered, make the
  whole closure `unknown` rather than guessing whether it is extras-only. Add
  the four valid forms above plus `extra !=` and `extra in` as independent
  positive/negative tests. This remains standard-library-only; `packaging` is
  needed only as the test oracle.

* **[Q2] BLOCKING -- the emitted-report oracle still discards the field this
  feature adds.** Its expected and observed multisets contain only
  `(distribution, count)`. With literal rows for `in-closure`,
  `out-of-closure`, and `unknown`, I changed every emitted annotation to
  `in-closure`; the proposed projections remained exactly equal and every
  `Coverage` field remained unchanged. Fixture class coverage cannot detect
  systematic relabeling when the comparison projects the class away.

  This does not re-open the direct class-drop finding: dropping the row changes
  the multiset and now reds. It exposes a separate integrity property -- the
  renderer can preserve every finding while lying about the triage axis.

  **Satisfier:** make the independently written expected and parsed observed
  values exact `(normalized_distribution, count, annotation)` multisets. Add a
  fifth recorded mutation that relabels or swaps annotation classes while
  preserving names and counts. Keep invariant (ii) over the returned `Coverage`
  object unchanged.

### Coverage

**Covered** -- the 301-distribution metadata corpus with a positive instrument;
valid noncanonical and quoted-marker counterexamples; the three reproduced
closure ratios; root mapping and failure direction; all four existing oracle
mutations; direct class-drop sufficiency; annotation relabeling; S2 and S5; and
the preserved scope declaration.

**Not covered / low confidence** -- the adopter's external environment and
299/93/212 figures, every legal PEP 508 boolean expression, live pip-audit
network output, cap thresholds, and an implementation that does not yet exist.
`packaging` was used only as an independent review oracle and is not proposed as
a shipped dependency.

### Second-round recommendation

**Recommended, tightly limited to Q1-Q2.** The next External Security pass
should run the noncanonical/quoted marker corpus through the final stdlib
recognizer and prove an annotation-relabel mutation reddens the emitted-report
oracle. The split policy, closure authority, class-drop coverage, and narrow S5
non-disappearance claim otherwise clear. No `Plan readiness` is recorded while
the marker boundary and annotation-integrity oracle remain unsettled.

## Response -- Claude (author) -- 2026-08-20 (round 4)

**Model**: claude-opus-5 (Claude Opus 5)

I ran Q1's counterexamples against Revision 3's own predicate before accepting.
It fails in **both** directions:

| requirement | extras? | `"extra =="` in text | outcome |
|---|---|---|---|
| `pytest; extra == "dev"` | yes | yes | ok |
| `pytest; extra=="dev"` | yes | **no** | wrongly included |
| `pytest; extra  == "dev"` | yes | **no** | wrongly included |
| `pytest; "dev" == extra` | yes | **no** | wrongly included |
| `foo; platform_release == "extra == dev"` | **no** | **yes** | **wrongly EXCLUDED — drops a real dependency** |

* **[Q1] accept.** The last row is the one that matters: a **genuine runtime
  requirement dropped** because the bytes appear inside a quoted value. That is
  the adopter's original warning — *"needed care to skip `; extra ==` without
  dropping genuine ones"* — and I have now hit it **from both sides**: Revision
  2 included everything, Revision 3 can drop a real one. Canonical producer
  spacing held across all 2,314 marker strings in this environment, which is
  exactly the kind of positive control that makes a wrong predicate look right;
  **package metadata is package-controlled input, so producer convention is not
  an authority boundary.**
* **[Q2] accept, and it is the most embarrassing finding of the set.** **The
  oracle projects away the field the feature exists to add.** Expected and
  observed multisets carry `(distribution, count)` and not the annotation, so a
  renderer that relabels every row to `in-closure` passes with every `Coverage`
  field unchanged. Fixture class coverage cannot catch systematic relabeling
  when the comparison discards the class.

  This is the same failure as E1 on the sibling proposal, one week of
  revisions apart in miniature: **an invariant that is satisfied by the shape of
  its own projection rather than by covering the property it guards.** Q2 does
  not re-open the class-drop finding — dropping a row still reddens — it names a
  distinct integrity property: *the renderer can preserve every finding while
  lying about the triage axis.*

**On the recommendation.** Accepted, tightly limited to Q1–Q2. I have not
touched the split policy, the closure authority, the root mapping, the failure
direction, or S5's narrow claim, all of which this pass cleared.

## Revision 4

**Complete current contract.** Self-contained; supersedes Revision 3 entirely.

*(Unchanged and operative, restated in Revisions 2–3 and not modified here:
the **Security Review REQUIRED** declaration and `Touches`; **D1** — the scoped
imperative, the consumer taxonomy, the lockfile/`integrity_preflight` consumer,
roots derived inside `_print_summary` with no signature change; **D1b** — the
stronger `content-security.md:122-123` copy and its self-hosted twins; **D2b** —
the coverage-ceiling paragraph; the closure's **authority** (`importlib.metadata`
rooted via `packages_distributions()`), **normalization** (PEP 503), **anchored
requirement-name grammar** including `~`, **traversal with node and depth caps**,
the **absent-vs-unreadable** distinction, and the **all-`unknown`** failure
direction; **S1**, **S3**, **S4**; `## Signals the change is wrong`; and the full
issue-closure contract. This revision changes only the extras predicate and the
oracle.)*

### The extras predicate — a marker tokenizer, not a substring test

**Withdrawn:** *"detected by the syntactic presence of `extra ==` in the
requirement's marker text."* A substring test over PEP 508 marker syntax is
unsound in both directions, and its dangerous direction **drops genuine
requirements**.

**Replacement — still standard-library-only.** Scan the marker text as
**tokens, respecting quoted strings and arbitrary whitespace**:

* Recognize an **unquoted `extra` equality in either operand order** —
  `extra == "x"`, `extra=="x"`, `extra  ==  "x"`, `"x" == extra` — and treat the
  requirement as **extras-gated → excluded**.
* An occurrence of the letters `extra` **inside a quoted string** is a value,
  not the marker variable, and is **ignored**. This is the row that would
  otherwise drop `foo; platform_release == "extra == dev"`.
* **Any other unquoted `extra` expression — `extra != ...`, `extra in ...`, and
  anything else — makes the WHOLE CLOSURE `unknown`.** Their truth under an
  unset or empty extra differs from positive equality, so treating them as
  equivalent is a guess. Refusing the closure is the fail-closed direction and
  is consistent with every other failure path in this spec.

**`packaging` remains unshipped.** The tokenizer is stdlib; `packaging` is used
**only as the test oracle**, in the dev-only suite, never in
`run_security_audit.py`. That distinction is the whole reason the substring
shortcut existed, and it does not require the shortcut.

**Tests are independent positives and negatives**, not a corpus scan: the five
forms in the table above, plus `extra != "x"` and `extra in "x"` asserting the
closure goes `unknown`. **The 2,314-marker environment corpus is a positive
control only** — it agrees with the wrong predicate, so it cannot be the
instrument that validates the right one.

### The bright line — the oracle carries the annotation

**Invariant (i) — the emitted report.** The expected multiset is written
**literally and pre-normalized in the fixture**, beside a raw child-JSON
fixture, and is now a multiset of **`(normalized_distribution, count,
annotation)` triples**. The emitted report is parsed back into an observed
triple multiset; exact equality is required.

Revision 3's `(distribution, count)` pairs **projected away the annotation** —
the one field D2 exists to add — so a renderer could preserve every finding and
relabel every class and stay green.

**Invariant (ii) — the `Coverage` object**, unchanged from Revision 3:
`coverage.names` (the full tuple, not its length), `coverage.vulnerabilities`,
`coverage.scanned`, `coverage.no_match`, `coverage.unknown`, and the returned
`(status, tier)` are identical with the annotation present and absent, asserted
on the returned object because `coverage.names` reaches the report only as
`len(...)` (`:1198`).

**Fixture class coverage remains part of the invariant:** the raw fixture
carries at least one vulnerable distribution in each of `in-closure`,
`out-of-closure` and `unknown`.

**Five recorded mutations, all of which must redden:**

1. drop a row in the renderer;
2. alter a count;
3. omit rows by annotation class — the option-2 collapse;
4. substitute a parent-side enumeration for `coverage.names`;
5. **relabel or swap annotation classes while preserving names and counts** —
   the mutation Revision 3's projection could not observe.

**What the annotation decides.** It **decides nothing the tool acts on** — no
verdict, no exit code, no finding omitted, no distribution dropped. It
influences **attention**; at a 144-to-27 ratio *triaged last* is operationally
*not triaged*, stated rather than elided. If it ever gates what is reported,
this has become the second-leg option and must be refused.

### S2 and S5 — revised

* **S2 — Can it fail?** The five mutations above, each run and recorded, plus:
  force the closure walk to raise (every distribution annotates `unknown`, all
  still reported, with a paired test asserting nothing was dropped); the
  closure-size tripwire (a bounded fraction of the discoverable set, so a
  re-inflation reddens); and the seven marker forms as independent positives and
  negatives. The expected multiset is **literal and pre-normalized in the
  fixture**, so the oracle is not computed from what it judges.
* **S5 — Who still wins?** Package metadata is authored by the packages, so an
  attacker controlling a distribution's metadata can make it annotate
  `out-of-closure` and be **triaged last**. They **cannot make it disappear**
  from the report, **and after mutation 5 they cannot silently relabel it
  either** — both are closed by an independently checked projection, not by
  construction. **Correction to Revision 3:** that claim was accurate only for
  presence; the emitted *class* was outside the projection, so "closed" was
  wider than what was checked. The **attention residual is open and accepted**:
  a correctly-labelled `out-of-closure` finding is still triaged last, which is
  the design's honest cost. Unchanged: an operator who prunes the baseline
  anyway.

### Withdrawn / superseded commitments

* **"Extras-gated requirements are excluded, detected by the syntactic presence
  of `extra ==` in the requirement's marker text."** **Withdrawn — falsified in
  both directions**, including a genuine requirement dropped because the bytes
  sat inside a quoted value. Replaced by a quote- and whitespace-aware marker
  tokenizer, with any other unquoted `extra` expression making the closure
  `unknown`. Reason: Q1.
* **The implicit reliance on canonical producer spacing.** Withdrawn. Package
  metadata is package-controlled input; the environment corpus is a positive
  control, not a validator.
* **Revision 3's oracle over `(distribution, count)` pairs.** Superseded by
  `(normalized_distribution, count, annotation)` triples plus mutation 5. It
  projected away the field the feature adds. Reason: Q2.
* **S5's "closed by an independently checked projection" as stated in Revision
  3.** Superseded — true for presence, not for the emitted class, which the
  projection omitted. Reason: Q2.
* **`Scope delta`: preserved.** No accepted outcome is withdrawn.

## Decision -- Anthony Kendall (Maintainer) -- 2026-08-20

**ACCEPTED as revised (Revision 4).** Authorization, quoted verbatim and visually isolated:

> "Okay, all three plans seem acceptable to me as revised. Please scribe my decision on all three as Accept as Revised."
> "Sorry, proposals"

**Summary of accepted terms (Revision 4)**:
- **D1/D1b (Scoped Stale Baseline Imperative)**: Scopes the stale-baseline message on exit 3 to name the audited roots set; clarifies unreferenced entries may be live in other consumers; frames exit 3 as a disagreement signal rather than an authoritative verdict to prune; syncs copy to `content-security.md:122-123`.
- **D2/D2b (Reachability Annotation & Coverage Ceiling)**: Annotates `pip-audit` findings with reachability (`in-closure`, `out-of-closure`, `unknown`) based on standard-library `importlib.metadata` dependency walk without altering scanner exit codes or finding sets; adds coverage-ceiling disclosure to `python-security.md`.
- **Marker Tokenizer & Test Oracle**: Implements a stdlib quote- and whitespace-aware tokenizer for `extra == "..."` markers (failing closed to `unknown` on other expressions); asserts exact multiset equality over `(normalized_distribution, count, annotation)` triples in test fixtures.
- **Review Requirement & Gating**: Plan review is `required(Internal)` (no Security Review trigger); issue closing is MAINTAINER-GATED upon code review, public declination comments for Issues #5 and #6, and recording the conda measurement.

**Scribed by** Antigravity (Gemini 3.7 Flash) on explicit Maintainer instruction.

## Correction -- Claude -- 2026-08-27 (appended; nothing above is edited)

**This proposal's line citations into `dev/.cairn/cairn-lock.yml` are void.**
Four of them (`:631-637` twice more, and `:647-664`) named ranges in a file that
has since been reconciled: the subtraction sweep deleted 19 recorded files and
C1 added two, taking the lockfile from 682 lines to 562. The ranges now overrun
the file and `claim_check` reports four `line-bounds` flags against this
document.

**They are not repaired in place, and that is deliberate.** This proposal is
`accepted` -- terminal, append-only -- so its prior sections show what was
believed when they were written. A pointer that has rotted is part of that
record.

**The lasting lesson, which is the reason this correction is worth appending at
all: do not cite line ranges into a machine-generated, regenerate-only file.**
The lockfile's own header says *"machine-generated ... regenerate-only; do not
hand-edit"*. Any citation into it is a claim about a rendering, not about
content, and it expires the next time the file is written. Cite the record by
its `dst` key instead -- `"dst": "scripts/claim_check.py"` is stable across
every regeneration; `cairn-lock.yml:631` was never going to be.

**The four flags therefore stand as a dated, known non-pass** rather than being
resolved or suppressed. Suppressing them would need a path exemption, which
does not reach `line-bounds` flags anyway -- measured 2026-08-27 -- and would
mask genuine path breakage in this document if it ever occurred.
