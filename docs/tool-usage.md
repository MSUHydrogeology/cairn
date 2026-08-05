# Tool usage — worked examples

Cairn ships a few small, standard-library scripts. The doctrine says *that*
they exist; this doc shows *how to run them and what to do with the output* —
the concrete moment, not the abstract capability. Each tool is a **discipline
aid, not a gate**: it shifts the cheap, mechanical part of a habit left, ahead
of review.

Install paths below are the adopter-side defaults; substitute your own if your
profile placed them elsewhere. Tools marked *(team-gated)* install only when
their module is selected.

## claim_check — verify path / line claims

**What it does.** Scans a Markdown proposal/plan/doc and hard-flags broken
repo paths and out-of-bounds line citations. Run it at write-time and before
committing a deliberation artifact. (The category-D count soft-flag was
retired 2026-06-05 — 0 catches across the instance log; numeric drift is now
governed by the three-kind precision / `as_of` discipline and a code-side
registry verifier, not a write-time nag.)

```bash
python scripts/claim_check.py dev/proposals/2026-06-01-me-new-thing.md
```

A clean file:

```
claim_check: dev/proposals/2026-06-01-me-new-thing.md -- OK, no claim-check flags.
```

A file with problems (exit code 1):

```
claim_check: ... -- 1 hard flag(s):
  ...:42: [path] cited path does not resolve: `frontend/helpre/util.py`
```

**What to do.** Fix a hard flag before committing (a real broken path, or a
forward-reference you must *mark* with a `Proposed/Untracked/External-repo
paths:` line, or — for a single cross-document citation — a document-scoped
`<!-- claim-check-allow: <glob> -->` directive).

## scripts/verify_counts.py — re-measure registered live-invariant counts *(Cairn-maintainer-only)*

**What it does.** The **live-invariant** leg of the three-kind numeric-claim
discipline. When `claim_check` retired its category-D count soft-flag, the
*decision-irrelevant* and *snapshot* kinds were handled by doctrine (approximate;
date) — but a count cited as **present fact** and prone to drift (a headline
file size re-quoted across docs as it changes) is registered in a code-side
registry (`scripts/measurements.py`) and re-measured here. **Not installed into
adopters** (not in `_CORE_MAPPINGS`); it dogfoods on Cairn's own docs.

A doc annotates the number with `<!-- verify: <key> -->` **immediately after the
number it verifies** (RR1 — the verifier reads the number directly preceding the
annotation on that line; for a `Snapshot`, put the `as_of` date before the number
or after the annotation, not between them). The annotation carries **only a
registry key** — never a path, never a command — so there is no document-supplied
path and no shell surface (every measurement is root-contained; `git` runs
`shell=False`).

```bash
python scripts/verify_counts.py docs/tool-usage.md
```

Two kinds dispatch from the registry: an **`Invariant`** is re-measured today and
the annotated number compared to it (a mismatch is **drift**); a **`Snapshot`** is
**never re-measured** — only its value-equality and the presence of the ISO
`as_of` date on the line are checked (re-running would erase the evidence the
snapshot is). An `Invariant` whose `root` is an **absent** sibling checkout
degrades to a **visible** `SKIPPED (root absent: …)` (a distinct non-clean exit
status), never a silent pass; an **unregistered** key is **refused**.

Worked example (the number and its annotation share one physical line, per RR1):

> Cairn's `claim_check` watch file is currently 878 lines `<!-- verify: claim_check_watch_file_lines -->`.

The count-soft-flag retirement shrank it from ~876; `verify_counts` re-measures it
and flags that line if the two ever diverge.

**What to do.** Keep the registry **small** (soft cap ~10 keys) and each
measurement cheap (a bounded stdlib scan or `git log` range) — there is no cache
by design. If the verifier ever runs slowly or the registry churns more than the
docs drift, that is the **curation-tax kill-signal**: shrink or freeze the
registry, do not accelerate it. Most numbers are decision-irrelevant — approximate
them; reserve a registered invariant for the few that are cited as live fact and
genuinely drift.

## tools/intent.py — claim work before editing *(team-gated: coordination-tiers)*

**What it does.** On a concurrent team, you claim a set of files before
editing them so a second agent sees the claim and coordinates rather than
colliding. The post-commit hook auto-releases your claim.

```bash
python tools/intent.py claim --files frontend/prep/soils.py tests/test_soils.py \
    --action "fix soil-temp fold-in"
# ... edit, commit (the post-commit hook releases the claim) ...
python tools/intent.py status          # what is claimed right now, by whom
```

First-session setup (opt-in; the scaffold never mutates `.git/hooks`):

```bash
python tools/intent.py install-hook        # post-commit auto-release
python tools/intent.py install-precommit   # pre-commit work-intent check (warn-only)
python tools/intent.py hooks-status        # confirm both are installed
```

**What to do.** If a pre-commit warning says a staged path has no active
claim, either claim it or proceed deliberately — the check is warn-only, not a
gate. If `status` shows a path held by another session, coordinate before
editing it.

## tools/lifecycle_metrics.py — measure the deliberation loop *(default-on)*

**What it does.** Derives per-proposal / per-plan lifecycle metrics — review
rounds, revision counts, finding tallies — from the `dev/` tree. The report is
a derived artifact, regenerable at any commit.

```bash
python tools/lifecycle_metrics.py proposals --format md   # Markdown table to stdout
python tools/lifecycle_metrics.py proposals --out metrics.csv
```

**What to do.** Read it as a health signal, not a target: a proposal that took
many review rounds is a candidate for a retrospective, not a number to
optimize. Regenerate it rather than quoting a stale figure from memory (exactly
the numeric-drift the three-kind precision / `as_of` discipline guards against).

## scripts/link_check.py — check cross-references resolve *(team-gated: doc-drift-prevention)*

**What it does.** Resolves the Markdown links across your tracked docs and
reports the ones that do not.

```bash
python scripts/link_check.py                 # whole tracked tree
python scripts/link_check.py docs/guide.md   # specific files
python scripts/link_check.py --check-external # also probe http(s) links
```

**What to do.** Fix a broken internal link before committing the doc change
that introduced it; treat it as the link sibling of a `claim_check` path flag.
External-link probing is opt-in (slower, network-dependent) — run it at
release-prep, not every edit.

## scripts/transition_lint.py — check a commit's message against its lifecycle diff *(Cairn-maintainer-only)*

**What it does.** Reads commit *subjects* over a bounded rev-range and flags
two shapes: **(a)** a subject claiming a review / response / decision
transition whose diff adds no such section, and **(b)** a proposal- or
plan-*open* commit whose added file already carries a real, dated review. It
enforces a rule that already exists — one commit per lifecycle transition —
rather than creating one. **Not installed into adopter trees**: it has no row
in the install manifest, and its heuristics are pinned against Cairn's own
subject conventions.

```bash
python scripts/transition_lint.py d6646a3..57d1daf   # rev-range is REQUIRED
python scripts/transition_lint.py <sha>..<sha> --report   # TAB-separated
```

**The exit contract, which is the whole point.** `0` on **any** completed
scan, with findings or without. `2` **only** for a usage error — a missing,
malformed, or unresolvable rev-range. **Never `1`.** Nothing may wire it to a
gate; a finding is a printed line a human reads. There is no default
rev-range, deliberately: a `HEAD`-relative default is a window that moves
under the reader.

**Every run prints a census**, including a clean one —
`scanned 120 commits, 52 triggered, 0 findings` — so a zero-finding run is
positive evidence rather than silence.

**Suppression is two layers, and a third was pre-registered and not
shipped.** The layers that exist: the *narrowing* (only commits adding or
modifying a file under `dev/proposals/` or `dev/plans/`, excluding
`archive/` destinations and `_template.md`), and the commit-SHA whitelist in
`scripts/transition_lint_whitelist.py`. The layer that does not: a
class-level downgrade of a whole false-positive class to `info`. It was
dropped on the argument that no recurring false-positive shape had ever
occurred — an argument that is now **falsified**, and it is recorded here
rather than left for a reader to notice. It stays unshipped because a
class-level downgrade lets a bad shape be absorbed rather than surfaced; the
intended replacement is that a recurring false-positive shape becomes a
proposal.

**What it does not cover.** Stated as gaps, never claimed as coverage.

* **Bundling.** It checks only that a claim is *supported*. It does not
  detect unannounced lifecycle work, or lifecycle work bundled with
  implementation work — leftmost-wins makes that structural.
* **Rename-only commits.** Reject / supersede Decisions and plan-archives are
  never examined; `reject` and `supersede` are commented dead tokens.
* **Merge commits, squashed / rebased / amended history, `git notes`, and
  commit bodies.** Only the subject line is read — which is also why there is
  nowhere to write an in-message opt-out.
* **False negatives are unmeasured.** Its silence on the commits it triggers
  on but does not flag has never been audited.
* **Shape (b) is not corpus-derived the way shape (a) is.** Shape (a)'s
  heuristics were re-derived over a 332-commit window. Shape (b)'s
  discriminator rests on **2 true positives and 1 false positive** — its
  requirement that a review section's heading carry an ISO date is what
  separates a landed review from a *brief* that quotes finding-id grammar,
  and that is thin evidence, said plainly rather than hidden behind shape
  (a)'s much stronger result.

**Its test posture.** The corpus-regression tier lives in
[`bootstrap/tests/test_transition_lint.py`](../bootstrap/tests/test_transition_lint.py)
rather than in a manual command, and it **self-skips** — never fails — if
Cairn's own history is absent, so a history rewrite cannot redden the suite
for a reason unrelated to the code.

**How to add a whitelist entry.** An entry needs a **written reason** *and* a
**paired follow-up** on the heuristic that produced the finding — the reason
is a mandatory dict value precisely so a test can assert it is there. An
entry that suppresses nothing is a latch, and the suite fails on one. If
entries accumulate past a handful, that is the signal to **retire the tool**
to a manual checklist item, not to grow the list.

## scripts/run_portable_security_sweeps.py — one measured offline secret sweep *(team-gated: portable-security-sweeps)*

**Installation check.** The module installs three files as one group:
`scripts/run_portable_security_sweeps.py`,
`scripts/portable_security_policy.json`, and
`dev/modules/portable-security-sweeps.md`. If they are not there, the module is
not selected in your profile.

**It installs no scanner.** You supply **Gitleaks** on `PATH` yourself. `git`
must also be present — the runner calls it for a pre-execution configuration
screen, and Gitleaks calls it transitively for the history leg.

```bash
python scripts/run_portable_security_sweeps.py --target .
python scripts/run_portable_security_sweeps.py --json    # deterministic summary
python scripts/run_portable_security_sweeps.py --security-verification
```

**Offline by default, and there is no other mode.** No network flag exists; the
child environment drops every inherited proxy variable.

**Two version modes.** **full** requires the resolved binary's SHA-256 to match a
digest the project's admission ceremony recorded for your exact
`(version, platform, architecture)`; only full mode can report `0`. **reduced** is
what you get otherwise: real current-tree findings, and an honest `INCOMPLETE`
instead of a clean result it has not earned. A **recorded** digest that does not
match is a contradiction, not an absence, and degrades.

**How to read the exit code.**

| Exit | Meaning | What to do |
|---|---|---|
| `0` | CLEAN — every leg ran in full mode and found nothing | nothing; it is a tripwire that did not trip, not a proof |
| `5` | INCOMPLETE — a leg did not fully run | read the named reason: absent binary, shallow clone, non-Git export, or an unadmitted version |
| `10` | FINDINGS | triage each; suppress only by adding a **reviewed fingerprint** to the policy |
| `20` | DEGRADED — a refusal, or a result the runner will not trust | do not treat as clean; the reason names the control that fired |

Precedence is `20 > 10 > 5 > 0`, so a finding is never hidden behind an
incomplete sibling leg. `NOT APPLICABLE` is distinct from `INCOMPLETE` and never
weakens another leg.

**Suppressions.** The policy carries reviewed fingerprints and nothing else — no
path, argv, environment variable, executable, config file, baseline, digest or
version. A `.gitleaksignore` found *inside* the tree under check is a **refusal**
(exit `20`), not a suppression source.

**Admitting a new adapter version** — an operator act, never part of a sweep and
never reachable from a standing command:

```bash
python scripts/run_portable_security_sweeps.py \
    --verify-version-support /abs/path/to/candidate \
    --confirm-executing-an-unadmitted-binary
```

It **executes a binary the project has not admitted**, says so in its first line
of output, and emits an evidence record. It never admits anything itself:
admission is a reviewed source change.

## See also

* The advisory transition check — `scripts/transition_lint.py` above, and the
  lifecycle rule it makes visible (one commit per lifecycle transition).
* The role-dispatch heuristics — `doctrine/roles.md` > "When to dispatch which
  role".
* The verify-before-asserting discipline these tools serve —
  `doctrine/rationale.md` and the `claim-check` module.
