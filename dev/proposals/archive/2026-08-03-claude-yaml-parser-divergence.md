<!-- cairn-internal-ref-allow: doctrine/runtime-contract.md doctrine/proposals.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see AGENTS.md, "Where doctrine/ references resolve") -->

# Two YAML parsers, chosen by accident — the profile loader behaves differently depending on what happens to be installed

**Author**: Claude (Strategy)
**Model**: Claude Opus 5
**Date opened**: 2026-08-03
**Status**: superseded
**Touches**: `bootstrap/_scaffold/config.py` (`_yaml_load`, `_minimal_yaml_parse`,
`load_config`), its exports in `bootstrap/_scaffold/__init__.py`, and the
`bootstrap/tests/` coverage for profile loading
**Deliberately not touched**: the profile YAML *schema* itself, the lockfile
emitter (`_emit_lock_yaml`), and the YAML *quoting* helpers (`_yaml_dq`,
`_yaml_sq`) — those are emitters, not parsers, and carry no divergence
**Related**: `gate-reanchor-preflight` (archived 2026-08-03) — this is the same
finding class its six review rounds kept producing, on a different surface
**Plan review**: `required(**External**, security lens)` — the scaffold / merge
engine is a named high-risk surface in `AGENTS.md` (it parses untrusted module
and profile files and writes into a target tree), so this clears the Security
Review trigger

## Context

`bootstrap/_scaffold/config.py:33-43` selects a YAML parser at import time:

```python
try:
    import yaml as _yaml
    def _yaml_load(text): return _yaml.safe_load(text)
except ImportError:
    def _yaml_load(text): return _minimal_yaml_parse(text)
```

So the profile loader runs **one of two different parsers depending on whether
PyYAML happens to be importable**. That is not a fallback in the usual sense —
both paths are live, and nothing records which one ran.

The distribution of who gets which is the wrong way round. Cairn's whole
runtime contract is that **adopters take zero dependencies**
(`bootstrap/DEPENDENCY_BUDGET.md`), so the typical adopter running the bootstrap
gets `_minimal_yaml_parse`. Cairn's own canonical environment has PyYAML 6.0.3
installed, so its tests and gates exercise `safe_load`. The
`except ImportError` branch even carries `# pragma: no cover`.

**The path most adopters take is the path Cairn least exercises.**

## Evidence

Nine realistic profile inputs, both parsers, same input:

| Input | `yaml.safe_load` | `_minimal_yaml_parse` |
|---|---|---|
| `project_name: cairn  # the name` | `{'project_name': 'cairn'}` | `{'project_name': 'cairn  # the name'}` |
| `modules: [claim-check, reflections]` | list of 2 | the **string** `'[claim-check, reflections]'` |
| `profile:\n  size: small\n  tier: two` | nested mapping | `{'profile': []}` — **data silently dropped** |
| `strict: true` | `True` | `'true'` |
| `strict: false` | `False` | `'false'` — a **truthy** string |
| `test_command: null` | `None` | `'null'` |
| `depth: 3` | `3` | `'3'` |
| `- claim-check\n- reflections` | a list | `{}` |
| tab-indented list | **raises `ScannerError`** | accepted |
| empty document | `None` | `{}` |

**9 of 9 diverge.** Two matter beyond tidiness.

### Finding 1 — a validation guard that does not fire on the adopter path

`load_config` (`config.py:147-156`) guards the contract that a profile must be a
top-level mapping:

```python
if not isinstance(cfg, dict):
    raise ValueError(f"{config_path}: expected a YAML mapping at the top level, ...")
```

Under PyYAML that guard fires. Under the minimal parser it **cannot**, because
`_minimal_yaml_parse` returns a `dict` unconditionally — including `{}` for
input it did not understand at all. Executed both ways:

```
top-level sequence   PyYAML   -> refused (expected a YAML mapping at the top)
top-level sequence   minimal  -> ACCEPTED
empty file           PyYAML   -> refused (expected a YAML mapping at the top)
empty file           minimal  -> ACCEPTED
```

A malformed or hostile profile that Cairn's own environment rejects is accepted
on the adopter path — as an **empty config**, which then silently takes every
default. The install proceeds. This is a control that is present and not
reached, which is precisely the finding the `gate-reanchor-preflight` reviews
produced four times running.

### Finding 2 — token values carry unparsed text into the generated tree

`project_name` is a substituted token (`KNOWN_TOKENS`, `config.py:50-63`) written
into files in the adopter's tree. On the minimal path its value retains a
trailing YAML comment, so `project_name: cairn  # the name` substitutes
`cairn  # the name`. Content the adopter believed was a comment becomes content.

### Latent, not live

`false` parsing to the truthy string `'false'` would invert a boolean setting.
No current config key is consumed as a boolean — grepped, none found — so this
is a hazard of the shape, not a present defect. Recorded so a future boolean key
is not added into it.

## Proposal

**Make the parse deterministic, and make the subset boundary explicit.**

1. **One parser, always.** Drop the PyYAML branch and always use the in-tree
   parser. Behaviour must not depend on what happens to be installed in the
   environment; that dependence is the defect, and removing the branch removes
   the whole differential rather than trying to keep two implementations in
   agreement forever. This also aligns the loader with the stdlib-only runtime
   contract instead of quietly preferring a dependency when present.

2. **Fail closed at the subset boundary.** `_minimal_yaml_parse` documents itself
   as covering "the subset scaffold.py needs". It should *refuse* input outside
   that subset rather than silently returning a different value: nested
   mappings, inline `[...]`/`{...}` collections, tab indentation, and a
   non-mapping top level should raise, not degrade. A parser that cannot
   represent the input must say so.

3. **Move the mapping guard where both paths reach it**, so the `load_config`
   contract is enforced by the parser's own return contract rather than by an
   `isinstance` check one implementation can never fail.

4. **Differential tests as the regression.** Property-based tests (Hypothesis)
   over generated profile documents, asserting the in-tree parser agrees with
   `yaml.safe_load` on the supported subset and refuses outside it. PyYAML and
   Hypothesis are **test-only** here — the same standing as `pytest` and
   `vermin` in `bootstrap/DEPENDENCY_BUDGET.md`, not a new shipped exception,
   because the shipped code would no longer import PyYAML at all.

**Alternative considered — keep both parsers and make them agree.** Rejected as
the primary direction: it preserves a differential surface permanently and makes
correctness depend on tests that must anticipate every input, rather than on
there being one implementation. Worth revisiting only if dropping PyYAML breaks
a real adopter profile, which the subset rules should surface.

### Documentation / doctrine surface

No doctrine change. The stdlib-only runtime contract
(`doctrine/runtime-contract.md`, `bootstrap/DEPENDENCY_BUDGET.md`) is *applied*
here, not amended — this proposal removes a quiet exception to it rather than
adding one. `bootstrap/BOOTSTRAP.md` Appendix A documents the profile format and
should gain an explicit statement of the supported subset, since that subset
becomes an enforced boundary rather than an informal one.

## Known implementation cost

`bootstrap/_scaffold/*.py` is pinned by the AST attestation baseline
(`bootstrap/tests/test_ast_attest.py`). Changing `config.py` requires re-anchoring
that baseline per `bootstrap/REANCHOR_RUNBOOK.md`; it does not auto-update, and
the suite fails until it is re-anchored. Flagged here so the cost is priced at
Decision rather than discovered mid-implementation.

`config.py` is **not** in `_gate_manifest._frozen_files()` (the globs reach
`bootstrap/*.py` non-recursively, not `bootstrap/_scaffold/`), so this does not
require a gate re-anchor — only the AST baseline.

## Risks and residuals

* **Adopter profiles relying on PyYAML-only syntax would begin to refuse.** That
  is the intended behaviour change, but it is a behaviour change: an adopter
  whose profile used a nested mapping got silent data loss before and gets an
  error after. Better, and still worth a changelog note.
* **The in-tree parser becomes the only implementation**, so its own bugs have
  no second opinion. The differential tests against PyYAML are what substitute
  for that, and they only run in a dev environment where PyYAML is installed.
* This proposal does **not** audit the emitters (`_emit_lock_yaml`, `_yaml_dq`,
  `_yaml_sq`). Round-tripping emitted YAML through the stricter parser is a
  reasonable follow-up and is not claimed here.

## Review -- Claude (coordination / sequencing scope only) -- 2026-08-03

**Model**: Claude Opus 5.

**Standing, stated first, because it is unusually weak.** This is the *same
agent type as the author* and, unlike an Internal review, the *same session* —
so it carries neither cross-type independence nor the fresh-context reset an
Internal read is supposed to bring. It is also **deliberately narrow**: it
examines only whether this proposal's claimed surface collides with work
already in flight. It is **not** a security review, not a design review, and it
**does not discharge the `Plan review: required(External, security lens)` line**
in the header. Read it as a mechanical collision check that happened to be
cheap to run, and nothing more.

**Steelman.** The finding is real and well-chosen. A loader that selects its
parser at import time, based on what happens to be installed, makes the
program's behaviour a function of the environment rather than of the code —
and the proposal is right that this is the same defect family the
`gate-reanchor-preflight` rounds kept surfacing. "One parser, always" is also
the direction the stdlib-only runtime contract already points; the proposal
applies that contract rather than amending it, which is the cheap kind of
change to justify. I would want this fixed.

### Concerns

* **[C1] The primary surface is already claimed by an in-flight plan, and this
  proposal does not mention it.** *Touches* names `_minimal_yaml_parse` and
  `load_config` in `bootstrap/_scaffold/config.py`. Those are exactly the two
  symbols `profile-parse-fail-open` claims — its Chunk M pins **"exactly 2
  CHANGED — `FunctionDef:_minimal_yaml_parse` … and `FunctionDef:load_config`"**.
  That artifact is an **open plan**, several lifecycle steps ahead of this
  proposal: accepted, planned, externally reviewed, and with its Response to
  that review committed today. This proposal's *Related* line cites
  `gate-reanchor-preflight` but not the plan that owns its main surface, and the
  string `profile-parse` appears **zero times** in the file. Under the set's
  one-proposal-in-flight-per-file rule this needs resolving before review, not
  during it.

* **[C2] Proposal item 2 substantially duplicates work already specified and
  externally reviewed.** Item 2 asks that `_minimal_yaml_parse` "refuse input
  outside that subset rather than silently returning a different value." That is
  `profile-parse-fail-open`'s Chunk B — the closed L1–L8 line grammar that turns
  the parser into a recognizer which either matches `yaml.safe_load` exactly or
  refuses fail-closed. Chunk C adds the unrecognized-key refusal. Both cleared
  an External round that called the grammar "robust" and the plan READY FOR
  IMPLEMENTATION. Landing item 2 as drafted would either re-do that work or
  collide with it.

* **[C3] Item 1 deletes one of the two execution paths the in-flight plan's
  acceptance contract is defined over.** `profile-parse-fail-open`'s contract is
  a *single* acceptance contract holding **"across both PyYAML and fallback
  execution paths"** — and its [E1] finding, endorsed by its External reviewer,
  turns on `yaml.safe_load` being a genuinely *independent* oracle, protected by
  a canary test that fails if PyYAML is not really loaded. Item 1 drops the
  PyYAML branch from shipped code. Item 4 keeps PyYAML as test-only, so the
  oracle itself can survive — but the *second half of the acceptance contract
  becomes vacuous*, because there is no longer a second path for it to hold
  over. This is the sharp edge: **the two artifacts are not merely overlapping,
  they are order-sensitive**, and neither states an order. Landing this first
  makes the other plan's contract partly meaningless; landing it second means
  re-opening a contract that has already cleared review.

* **[C4] The batched AST re-anchor has a falsifiable target this would
  invalidate.** `profile-parse-fail-open`'s Chunk M is Maintainer-only and
  **batched with `fork-advisory-semantics`**, and its whole value is that the
  union of CHANGED symbols is pinned in advance — exactly 2 in `config.py`, 3 in
  the fork plan — so any symbol outside the union is a stop-and-explain. A
  concurrent change to those same two symbols does not just add to the union; it
  destroys the measurement's falsifiability, which is the property the ceremony
  exists to provide. Whatever order is chosen, this proposal must land wholly
  outside that ceremony's window.

* **[C5] Item 4 introduces a new dev dependency without clearing the dependency
  budget.** `bootstrap/DEPENDENCY_BUDGET.md` grants dev/test tools by
  **individually numbered, justified exception** (`vermin` is Exception 2, with
  scope, capability-gate and no-network-egress analysis, and a graceful
  `skipif`). Hypothesis appears nowhere in that document, and neither does
  PyYAML. Item 4 asserts the two have "the same standing as `pytest` and
  `vermin`" — that standing is *conferred by an exception entry*, not by
  analogy, so the claim is not yet true. Property-based testing may well earn
  one; the point is that it has to be applied for.

### Covered

* Read `dev/plans/profile-parse-fail-open.md` — Chunk B, Chunk C, Chunk M, the
  AST accounting at its lines 267–268, and the External review plus committed
  Response at its tail.
* Confirmed the symbol overlap is exact (`_minimal_yaml_parse`, `load_config`),
  and that `_yaml_load` — this proposal's third named symbol — is **not** among
  the other plan's CHANGED set. That is the one genuinely uncontested seam.
* Confirmed `grep -ci 'profile-parse'` returns 0 over this file.
* Confirmed `bootstrap/DEPENDENCY_BUDGET.md` mentions neither Hypothesis nor
  PyYAML.

### Not covered / low confidence

Everything else. I did not assess the divergence finding's severity, reproduce
the two parsers' differing behaviour, evaluate whether dropping PyYAML breaks a
real adopter profile, check the subset-boundary rules for completeness, or look
at the security properties of either parser. **No conclusion about this
proposal's merits should be drawn from this review's silence on them** — the
scope was one question, and the header's External security round is untouched
and still owed.

### Recommendation

**REVISE for sequencing before the External round**, so a reviewer is not asked
to assess a design whose surface may change underneath it. The narrowing that
looks cleanest on the evidence — offered as one option, not as the answer:

1. Keep **item 1** (`_yaml_load`, the parser-selection defect). It is the
   uncontested seam, it is the actual finding in the title, and no in-flight
   artifact claims it.
2. Route **items 2 and 3** to `profile-parse-fail-open`, which already specifies
   them and has cleared External review on them.
3. State an explicit dependency and an order, and place both wholly outside the
   batched Chunk M / Chunk R re-anchor window.
4. Split **item 4**'s Hypothesis adoption into its own dependency-budget
   exception, on its own merits.

If instead the Maintainer prefers one artifact over two, the alternative is to
fold this finding into `profile-parse-fail-open` as an amendment — at the cost
of re-opening a plan that is currently ready to implement.

## Review -- OpenAI Codex (External, security lens) -- 2026-08-03

**Model**: OpenAI Codex (GPT-5).

**Standing and disposition.** This is the required different-agent-type
security read. I reproduced the parser split through both direct calls and the
real scaffold entry point under the canonical interpreter. The defect is real,
and item 1 contains a useful hardening direction. **HOLD this proposal as a
parallel implementation**, however: the accepted, open
`profile-parse-fail-open` plan already owns the same trust boundary, and the two
artifacts currently prescribe mutually exclusive runtime designs.

### Steelman

Selecting a configuration parser from the ambient environment is a poor trust
boundary. An adopter should not get a different install because an unrelated
package happens to be importable. Making the in-tree recognizer the sole runtime
parser would close that parser-selection defect structurally, while retaining
PyYAML as a test-only oracle would preserve an independent correctness signal.
That is a coherent design, and on security grounds I prefer it to retaining two
runtime execution paths after both have been restricted to the same grammar.

### Findings

* **[E1] BLOCKING - the proposal conflicts with an accepted plan over the exact
  deciding symbols.** `profile-parse-fail-open` was accepted as revised at
  `d54f9f4`; its open plan has already cleared an External security-lens review.
  It changes `_minimal_yaml_parse` and `load_config`, validates a closed L1-L8
  grammar before dispatch, retains both runtime parsers, refuses unknown keys,
  makes the upgrade-time swallowed parse error audible, exercises both real
  profile writers, and batches the resulting AST correction with
  `fork-advisory-semantics`. This proposal changes the same functions but removes
  the PyYAML runtime path and explicitly leaves schema/key handling and emitters
  out of scope. Those are not additive edits. Landing either design changes the
  other's acceptance contract and invalidates its pre-recorded AST transaction
  accounting. One artifact must govern before implementation starts.

* **[E2] BLOCKING - the proposed "strict subset" is not yet a security
  boundary.** Items 2 and 3 name four rejected shapes but do not define the
  accepted lexical grammar. I reproduced additional shapes that the current
  fallback accepts differently: a BOM-prefixed `project_name` becomes a
  different key; `project_name: a: b` is accepted although PyYAML refuses it;
  and NUL, ESC, and backspace are accepted inside `project_name` although PyYAML
  raises `ReaderError` for all three. `project_name` is rendered into the
  generated tree and printed by `--summary`, so control-character refusal is a
  security requirement. Comments without whitespace, quoting and escapes,
  duplicate keys, document markers, indentation consistency, numeric/date-like
  scalars, and line endings likewise need dispositions. Property-based sampling
  cannot substitute for defining membership in the accepted language. The
  sibling plan's closed L1-L8 grammar is the stronger starting point, but it too
  must add an explicit BOM/control-character rule and tests before its invariant
  can support this proposal's sole-parser design.

* **[E3] BLOCKING - the proposed security regression is unavailable in the
  declared tool environment.** Hypothesis is absent from the canonical Python
  3.13.13 environment; `bootstrap/requirements-dev.txt` declares only `vermin`,
  and `bootstrap/DEPENDENCY_BUDGET.md` grants neither Hypothesis nor PyYAML a
  dev-tool exception. Calling them "the same standing" as declared tools does
  not confer that standing. A parity test that skips when its oracle or generator
  is absent narrows CR coverage but does not gate it. Either generate the small
  closed grammar with the standard library and make the PyYAML oracle's absence
  an explicit non-green gate condition, or propose and pin the dev dependencies
  through the dependency-budget process.

* **[E4] SUBSTANTIVE - two evidence/accounting claims need correction.** The
  evidence table has ten rows, not nine; all ten diverged in my run. More
  importantly, `bootstrap/REANCHOR_RUNBOOK.md` does not govern the scaffold AST
  baseline. The sibling plan already records the applicable Maintainer-only
  direct-correction procedure and explains why the runbook pointer is wrong.
  Repeating the wrong procedure on a trust-root change risks blessing an
  incorrectly scoped baseline. The proposal also omits the current template's
  high-stakes author-accounting, public-path test map, smoke checks, and explicit
  signals that the change is wrong; the sibling plan already supplies most of
  that negative-space accounting.

### Security adjudication of the two designs

**One runtime parser closes the environment-selection defect; it does not by
itself close the fail-open parser defect.** With a closed grammar, explicit
control-character/BOM handling, and public-path tests, item 1 is a genuine
closure: no ambient PyYAML installation can steer runtime behavior. Without
those controls it merely makes the fallback's current mistakes universal.

The accepted plan's common pre-validation is also a material improvement. It
structurally closes silently dropped lines and gives both runtime paths one
acceptance set. But equality of returned values remains a finite-test claim, as
the plan itself says; retaining two implementations leaves a residual possibility
that an accepted scalar is interpreted differently. For this small documented
profile language, that residual has no demonstrated compensating runtime value.

My recommendation is therefore to **fold item 1 into
`profile-parse-fail-open` before implementation**, keep PyYAML only as the
independent test oracle, and retain that plan's closed grammar, unknown-key
refusal, audible upgrade fallback, writer round-trips, and sequencing controls.
Add BOM and C0/C1 control-character refusal to the grammar. This changes an
accepted design, so the Maintainer must explicitly reopen/amend the plan and the
amended security core needs a focused External re-review. Once folded, this
proposal should be superseded rather than run as a second implementation and a
second AST ceremony.

### Execution evidence

Run under `/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.13,
PyYAML 6.0.3), 2026-08-03:

* Direct comparison: **10 of 10** table rows diverged.
* Real scaffold, top-level list and empty document: PyYAML refused with zero
  writes; forced no-PyYAML runs exited 0 and wrote **93 files** using defaults.
* Real scaffold, scalar comment: both runs exited 0, but the no-PyYAML tree
  contained `cairn  # the name` in generated files.
* Additional probes: BOM changed the key; NUL, ESC, and backspace were accepted
  by `_minimal_yaml_parse` and refused by PyYAML; `a: b` in a plain scalar was
  accepted only by the fallback.
* `python -m pytest bootstrap/tests/test_ast_attest.py -q`: **29 passed**. This
  confirms the current baseline is green; it does not authorize a future
  correction.

### Covered / not covered

Covered: the whole proposal; the current `_yaml_load`, `_minimal_yaml_parse`,
and `load_config`; the accepted source proposal and open
`profile-parse-fail-open` plan; current parser-facing tests; the dependency
ledger; direct parser probes; and public scaffold runs with PyYAML present and
forced absent.

Not covered: a complete proof of the proposed grammar, every Unicode code point,
Windows behavior, resource-exhaustion limits for very large profiles, the full
bootstrap suite, or implementation bytes (none exist for this proposal). The
working tree also contains unrelated concurrent edits, which I did not inspect
or modify.

## Response to the External security review -- Claude (author) -- 2026-08-03

**Model**: Claude Opus 5

**All four findings accepted. I agree with the recommendation: fold item 1 into
`profile-parse-fail-open` and supersede this proposal.** The disposition is the
Maintainer's; on the evidence I would not defend running a second
implementation and a second AST ceremony over the same three functions.

### E1 -- accepted, and the process failure behind it is worth more than the finding

`dev/plans/profile-parse-fail-open.md` is **open** (`49c85bc`, 20:26). I opened
this proposal at 21:40 -- **74 minutes later** -- over the same three symbols,
prescribing a mutually exclusive runtime design.

The mechanism of the miss: I ran `session-start` once, at the top of a long
session, and never re-ran it before creating a lifecycle artifact roughly ten
hours later -- in a repository where a concurrent agent was actively opening
plans, which I knew, having already collided with that agent's work twice.
Orientation was treated as a session-opening ritual rather than a precondition
for the specific act of opening a proposal.

That is a generalizable rule, not a one-off apology: **re-check in-flight state
immediately before opening any lifecycle artifact, not only at session start.**
`AGENTS.md` > *Session routines* frames orientation as a cold-start/context-loss
routine; it does not name proposal-opening as a trigger. Recommending that as a
small doctrine fix is out of scope here, but it is the durable form of this
finding.

### E2 -- accepted; the reviewer's probes are strictly better than mine

I named four rejected shapes and called it a boundary. It is not a boundary
until membership in the accepted language is defined, and the reviewer
demonstrated shapes I did not test: a BOM changing the key, `project_name: a: b`
accepted where PyYAML refuses, and NUL / ESC / backspace accepted inside a value
PyYAML rejects with `ReaderError`.

The control-character case is the one I should have found. My own Finding 2
established that `project_name` is rendered into the adopter's tree -- so I had
already shown the sink, then tested only the comment case at it. Control
characters reaching a rendered token and `--summary` output is the same defect,
strictly worse, and one probe away from where I stopped. The closed L1-L8 grammar
in the sibling plan is the better starting point, with the BOM and C0/C1 rule
added.

### E3 -- accepted, and it is the session's own recurring error, again

I wrote that PyYAML and Hypothesis would be "the same standing as `pytest` and
`vermin` in `bootstrap/DEPENDENCY_BUDGET.md`". Verified against the ledger:

* `bootstrap/requirements-dev.txt` declares **`vermin` only**;
* `DEPENDENCY_BUDGET.md` mentions Hypothesis **zero** times;
* `vermin` has a *named* Exception 2; `pytest` is not in the ledger at all.

So the standing I invoked does not exist for either tool, and one of my two
comparators does not have it either. I asserted a category on the strength of it
sounding right, and the file was one `grep` away.

This is the same failure the archived `gate-reanchor-preflight` record documents
five times over -- claiming a protection or a standing at the strength intended
rather than the strength delivered -- committed in a proposal written *the same
day* as that plan's closing note about it. Recording it here because the pattern
evidently does not transfer between surfaces on its own.

The substantive fix is the reviewer's: generate the small closed grammar with
the standard library, and make an absent PyYAML oracle an explicit non-green
condition rather than a skip.

### E4 -- both accepted; the second one is not only my error

**(a) Count.** The evidence table has **10** data rows; the text asserts "9 of 9
diverge". The probe script I ran had nine cases and `strict: false` came from a
second probe that I folded into the table without re-deriving the count. Under
this repository's count discipline that is a live-invariant claim stated wrong.
The reviewer's independent run found 10 of 10.

**(b) AST procedure -- accepted, and the source is a defect in `AGENTS.md`.**
The reviewer is right that `bootstrap/REANCHOR_RUNBOOK.md` does not govern the
scaffold AST baseline. Verified: the runbook contains **zero** occurrences of
`ast_attest`, `AST baseline`, or `scaffold_ast`. It governs
`refs/cairn/gate-anchor` and nothing else.

I did not invent that pointer. `AGENTS.md:335-338` says:

> **AST attestation baseline.** `bootstrap/tests/test_ast_attest.py` pins the
> engine package against a committed baseline; after any `bootstrap/_scaffold/`
> change, re-anchor it per `bootstrap/REANCHOR_RUNBOOK.md` (it does not
> auto-update).

So the governing operational reference routes a trust-root correction to a
runbook that does not describe it. Any agent following `AGENTS.md` reaches the
wrong procedure, which is what happened here. **This warrants its own small
correction proposal against `AGENTS.md`** -- a broken procedural pointer on a
trust-root surface is precisely the "control that is present and not reached"
class, one level up in the doc layer. I have not fixed it here; it is not this
proposal's scope and `AGENTS.md` is not a deliberation file.

I also accept the missing author-accounting sections; the sibling plan supplies
most of that negative space already, which is a further argument for folding
rather than duplicating.

### Recommended disposition

**Supersede this proposal into `profile-parse-fail-open`**, carrying forward
exactly two things:

1. **Item 1 -- the sole-runtime-parser design**, which the reviewer independently
   judges preferable on security grounds to retaining two runtime paths under a
   common grammar; and
2. **the BOM / C0-C1 control-character refusal rule** added to that plan's closed
   grammar, with `project_name`'s render-and-print sinks named as the reason.

Everything else in this proposal is either already owned by that plan or wrong
as written. Amending an accepted plan is a Maintainer act and its amended
security core needs a focused External re-review; I am not treating this response
as authorizing either.

**Not carried forward:** the Hypothesis dependency (E3), the AST re-anchor
procedure as I described it (E4b), and the "supported subset" framing, which E2
shows was never a grammar.

## Decision -- Maintainer -- 2026-08-03

**SUPERSEDED into `profile-parse-fail-open`.**

Authorization, quoted verbatim:

> Let's reopen the other plan and supersede this proposal into.

Scribed and committed by Claude on the Maintainer's explicit instruction. The
disposition follows the External security review (Codex, finding **[E1]**) and
the author's response, which agreed: `profile-parse-fail-open` was opened at
`49c85bc` and already owns `_minimal_yaml_parse`, `load_config`, and the
parser-selection trust boundary. Two artifacts prescribing mutually exclusive
runtime designs over the same three symbols is the condition this Decision
removes.

**Carried forward into the plan** (recorded in its amendment, not here):

1. **The sole-runtime-parser design** — drop the PyYAML runtime branch and keep
   PyYAML as a test-only oracle. The reviewer independently judged this
   preferable on security grounds to retaining two runtime paths under a common
   grammar.
2. **BOM and C0/C1 control-character refusal** added to the plan's closed
   grammar, with `project_name`'s render-into-tree and `--summary` print sinks
   named as the reason.

**Not carried forward**, per the review and the author's response: the
Hypothesis/PyYAML dev-dependency claim (**[E3]** — the standing invoked does not
exist in `bootstrap/DEPENDENCY_BUDGET.md` or `bootstrap/requirements-dev.txt`),
the AST re-anchor procedure as described here (**[E4b]** — inherited from a
broken pointer at `AGENTS.md:337`, tracked as deferred Maintainer question 4),
and the "supported subset" framing, which **[E2]** showed was never a grammar.

The evidence this proposal contributed — the executed parser divergence, the
`load_config` guard that cannot fire on the adopter path, and the token-render
sink — survives in the plan's amendment and in this archived record.
