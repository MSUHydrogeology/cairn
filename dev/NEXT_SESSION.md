# Next session

*Rewritten from scratch 2026-08-28, after the subtraction sweep archived. Run
`python tools/board.py` first — it is derived and current; this file is
hand-written orientation and may already be stale.*

## Where the project stands

**The subtraction sweep is archived.** `dev/plans/archive/subtraction-sweep.md`.
C1–C9 landed, the code-review floor was met for every chunk group it names, both
re-anchors ran, and its lasting truths migrated to
`dev/strategy/2026-08-21-claude-nimbleness-recovery.md`.

**The tree is fully green** for the first time in the sweep's life: full suite
**3178 passed, 0 skipped, 0 failed** (Python 3.13.13, quiet tree);
`_ast_attest verify` OK at 173 baselined symbols, unchanged; `_gate_manifest
verify` OK at 183 frozen files / 3178 pinned nodes.

**19 commits are unpushed.** Pushing is the Maintainer's, always.

## The one asymmetry to resolve first

**`lhm` is merged; `modflow_tools` is not.** `lhm`'s `cairn-0.3.0-migration`
merged to its `master` (plus a Maintainer follow-up recording the 0.3.0 consume
in its fidelity manifest). `modflow_tools` is still sitting on its
`cairn-0.3.0-migration` branch with `master` untouched at `5ef8851b`.

Its suite was green at **3472 passed / 0 failed** when the branch was cut. It has
not been re-verified since; **re-run before merging** rather than trusting that
figure, and expect its fidelity manifest to want the same follow-up `lhm` got.

## What is genuinely next

* **The `repin` tool.** The successor to the blocked
  `scripts/correct_pinned_digests.py`, designed in
  `dev/strategy/2026-08-28-claude-repin-revitalization.md`. Its route is already
  set: a **deliberate-lane proposal** with Security Review declared and the
  External floor at the *proposal*, because that is where the design is still
  movable. Codex reviewing the successor to the thing it blocked is named as the
  natural External seat. **Until it lands, corrections continue by hand** — that
  is the strategy's own instruction, not a shortcut.
* **RD-3, pre-registered as an acceptance criterion for that proposal.** The
  re-anchor launcher is built from `bootstrap/reanchor-launcher.template.sh`,
  and **the template is not a closure member** — nothing pins the
  pre-candidate trust root, whose work all happens before the checker exists.
* **Three deposits still open**, from the batch the Maintainer authorized:
  [TRU-4]'s known-new graduation decision (now much cheaper — the manifest is
  enforced and accurate), C6's two onboarding findings behind the
  MAINTAINER-GATED `_ALWAYS_ON_MAPPINGS` fence, and the four unfiled forge
  issues in `dev/measurement/queued-issue-drafts.md`.
* **`2026-08-20-claude-adopter-path-consolidation`** — `awaiting-review`,
  untouched throughout.

## Things that are true and will look wrong

* **`check_cairn` reports 6.** Two are pre-existing; four are `line-bounds`
  flags in `2026-08-20-claude-scanner-claim-scope.md`, a **known, dated
  non-pass** — the lockfile shrank and that proposal is append-only, so its
  citations were corrected by appending rather than editing.
* **`quality_gate --sub neutrality` reports fail=79.** Unchanged for months;
  not introduced by recent work.
* **A `verify` run without `--known-new` still passes over an altered
  known-new body**, and warns that it did. **Treat such a run as not having
  checked.** The attestation gained that enforcement on 2026-08-28 after an
  injection into `verify_within_root`, the containment guard, printed
  `note: NEW` and exited 0.
* **`_gate_manifest.py verify` will HOLD again after the next edit** to
  anything under `bootstrap/tests/**` or `scripts/*.py`. A *committed* change
  to a frozen file does not redden the suite; an *uncommitted* one does. And
  the suite passes while the manifest HOLDs, because the test self-verifies a
  freshly produced manifest and never diffs the committed fixture — **a green
  suite is not evidence that no re-anchor is owed.**

## Worth not relearning

**Measure over the DECLARED set, never the present one.** Three instances in
one day, in unrelated code: a lockfile scan that skipped absent files and
reported the intersection as the whole; a packet check that compared only the
rows the packet happened to contain; and a grep over a *truncated* report that
concluded about the twelve entries it could not see. Iterate over what is
declared and let a missing entry be visible as missing.

**A named hazard with no enforcing trigger is not a control.** The AST runbook
stated *"a symbol in known-new is invisible to the baseline gate"* — correctly,
in writing, for months — while nothing enforced it.

**A review's findings are a specification, not an argument for retreat.** An
adversarial review of a convenience tool returned 28 confirmed findings and the
first instinct was to delete the half they landed in. Only one of six root
causes genuinely resisted automation. Retreat *feels* like rigour and cannot be
shown wrong, because the deleted version is never built.

**Quiesce the tree, then measure.** A suite in flight while files are being
edited returns figures that are worthless in both directions. This cost time
three times: a review whose `HEAD` moved beneath it, a ceremony refused by a
peer's mid-write, and a suite run against a tree being committed to.
