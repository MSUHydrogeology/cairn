<!-- cairn-internal-ref-allow: doctrine/dual-review.md doctrine/plans.md doctrine/rationale.md doctrine/lifecycle.md doctrine/coordination.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see AGENTS.md, "Where doctrine/ references resolve") -->

# Plan: five security-preflight questions land on four template files, and a test proves the twins did not drift

**Source proposal**: `security-preflight-checklist` (accepted 2026-08-03 by
Maintainer Decision). It currently sits at
`dev/proposals/2026-08-03-claude-security-preflight-checklist.md` and moves to
`dev/proposals/archive/` when it archives. The path is cited once, in full,
because Chunk B extracts bytes from it mechanically.
**Status**: open
**Plan review**: required(**Internal**) — the ceiling the proposal header
declared (*"If the Maintainer prefers a plan anyway, **Internal** is the
ceiling"*) and the Decision ratified. **No implementation step runs before the
`## Plan review` section is in the tree.** Why Internal is genuinely the
ceiling, and the one thing about this plan that a reviewer should attack
anyway, are in *Plan review — the brief* below.
**Last update**: 2026-08-04
**Opened**: 2026-08-04

## Source proposal

`security-preflight-checklist` settles one contract: **the proposal template's
existing `### Author-accounting` block gains a gated `####` sub-block of five
security questions — S1 through S5 — that a security-touching change answers
in writing, while its design is still movable, and a reviewer falsifies in one
read.** The plan executes that decision and does not re-litigate it.

The lifecycle ran open -> External security review (Gemini Flash, verdict
SHIP, two concerns [E1] and [E2]) -> author Response -> Decision. There is no
`## Revised proposal` section; the Decision says so in terms and records the
accepted state as *the proposal as opened plus that Response*. Both concerns
were dispositioned in the Response: [E1] (no automated enforcement) stays
declared-unenforced on purpose, and [E2] (ritualization) had its recovery path
bound to two `git grep`-able triggers instead of a monitoring duty.

### Why a plan exists when the Decision said none was needed

Stated first, because it is the one place this artifact could be mistaken for
scope creep. The proposal header reads *"Plan review: not required"* and the
Decision reads *"No plan opens; per the header this is a single implementing
commit against the proposal template."* A plan is nevertheless being written,
at the Maintainer's direction, and the header anticipated exactly that:
*"If the Maintainer prefers a plan anyway, **Internal** is the ceiling."*

So this plan **does not enlarge the accepted contract's file set**. It changes
one thing about how that contract is discharged, and that change is declared
in the open under *The one divergence from the proposal* below.

### Glossary — every term glossed on first use

* **Twin pair** — two files that must carry the same content: Cairn's own copy
  under `dev/`, and the copy under `templates/core/dev/` that the scaffold
  installs into an adopter's tree. This change touches two such pairs.
* **The shipped side / the self-host side** — a file under
  `templates/core/dev/` is the shipped side (what an adopter receives); its
  counterpart under `dev/` is the self-host side (what Cairn uses on itself).
  The two are *not* byte-identical as whole files —
  they diverge inside `cairn:slot` regions — so parity is a claim about a
  *region*, never about the file.
* **`cairn:slot`** — a marked region in a shipped template that the scaffold
  or the adopter fills with project-specific content. Cairn's self-host copy
  has these regions filled; the shipped copy carries the fill instructions.
  Verified for this plan: every difference between the two proposal templates
  is inside such a region, and the `### Author-accounting` block contains none.
* **Oracle** and **subject** — a test is an oracle (what ought to be true) plus
  a subject (the thing checked). When the oracle is *derived at run time* from
  the same object the subject reads, the test cannot fail on a change that
  moves both. A literal typed into the test body is an oracle from a different
  channel, even if a human copied it from the subject once, at authoring time.
* **Perturbation** — a deliberate change to repository state that a test is
  claimed to detect. This repository accepts a test only when its author names
  a state in which it fails **and has run** the change that produces it.
* **Hazard-side perturbation** — a perturbation applied to the thing the test
  is claimed to protect (here: a template file). Perturbing the *test's own
  body* validates the test; only perturbing the hazard validates the claim.
* **Frozen file** — a file whose sha256 is pinned in
  `bootstrap/tests/fixtures/gate_manifest.json`. Editing one makes a later
  `_gate_manifest.py verify` report `FROZEN-MODIFIED`, which is a HOLD.
* **The 0-skipped rule** — `AGENTS.md`'s suite gate requires the engine suite
  green with 0 skipped and 0 xfailed. A `pytest.skip` that ever fires is
  therefore a gate failure, not a silent pass.

## Scope

Executes the accepted contract across **four Markdown template files in two
twin pairs**, **one new test node**, and **two serialized record files**.

**The twin-parity hazard is the whole point of the sequencing.** A template
that drifts from its shipped copy ships adopters something different from what
Cairn uses on itself, and the drift is invisible: both files stay individually
well-formed, every gate stays green, and nothing reads them together. The
proposal's own accounting says parity is *"[e]nforced today by convention
only"*. This plan makes it an acceptance criterion with a test, and Chunk D
proves that test discriminates.

### The one divergence from the proposal, declared

The proposal's Author-accounting states, of the byte-identity invariant:
*"Enforced today by convention only; this change does not add an enforcer, and
says so."* **This plan adds an enforcer for the added sub-block.** That is a
deliberate departure, made at the Maintainer's direction when the plan was
commissioned, and it is recorded here rather than discovered at review.

Three bounds keep it from becoming scope creep, and each is checkable:

1. **No new file.** The enforcer is assertions inside the *one* test node the
   proposal already authorized, in the *one* test file the proposal already
   names.
2. **The added sub-block only, not the whole block.** The wider invariant —
   *the entire `### Author-accounting` block stays byte-identical across the
   twins* — is true today (measured below) and is **not** asserted. Asserting
   it would pin a contract the proposal declined and would make any future
   legitimate slot divergence a test failure. It is recorded as residual R5
   with a named trigger instead.
3. **Strikeable in one line.** Delete assertion group (c) and (d) in Chunk C's
   test and the plan still delivers the accepted contract through the shipped-
   side assertions the proposal specified.

If the Internal reviewer or the Maintainer reads the proposal's no-enforcer
sentence as binding, **Chunk C's parity half is the part to strike**, and
Chunks A, B and the rest of C stand unchanged.

### Out of scope, fenced explicitly

Each of these is a routing decision recorded in the proposal's *Documentation /
doctrine surface*, not an oversight. **Do not widen.**

* **`doctrine/` — nothing under it.** The obvious candidate was a sixth lens on
  the review sweep in `doctrine/dual-review.md`. The proposal declines it on
  two stated grounds: that doctrine says the sweep is *"generic and
  change-agnostic"*, and — decisively — the sweep is the **reviewer's**
  instrument while the measured failure is on the **author's** side. Putting
  these questions in the reviewer's roster would reproduce the exact defect.
* **`AGENTS.md` — no change.** The gating clause *cites* `AGENTS.md`'s
  high-risk-surface list; it does not edit it.
* **The install manifest's row set — no change.** Two rows that already exist
  change content. `python bootstrap/scaffold.py --manifest` is expected
  byte-identical, and Chunk E asserts the empty diff rather than assuming it.
* **`bootstrap/_scaffold/` — no engine byte.** Therefore
  `bootstrap/tests/fixtures/scaffold_ast_baseline.json` is untouched and the
  AST-attestation half of `bootstrap/REANCHOR_RUNBOOK.md` is not engaged.
* **Every gate script** — `scripts/check_cairn.py`, `scripts/claim_check.py`,
  `scripts/quality_gate.py`, `bootstrap/security_check.py`. They are *run* by
  this plan and edited by none of it.
* **A presence linter over filled proposals.** Rejected in the proposal with a
  named revival path (`transition-lint`); residual R3.
* **The default-security-stance question** the Maintainer opened 2026-08-03.
  The proposal states in terms that it is adjacent and not addressed; the
  `content-security` preset-selection surface carries it and needs its own
  proposal.
* **Retro-fitting open proposals.** The block is **prospective only**, per the
  paragraph it will sit inside. No open or archived artifact is retro-fitted —
  including the proposals opened on 2026-08-03 that motivated it.

### Documentation / doctrine surface

* **Deliberation layer — the primary change.** `dev/proposals/_template.md`
  and `dev/plans/_template.md`. Under `docs/DOCUMENTATION_PLAN.md`'s routing, a
  proposal template is deliberation-layer scaffolding: it shapes how a change
  is argued, not what the software is.
* **Shipped templates — adopter-installed.**
  `templates/core/dev/proposals/_template.md` and
  `templates/core/dev/plans/_template.md`. An adopter who scaffolds after this
  lands receives the five questions. This is the *Bootstrap fidelity / install
  contract* trigger in its weakest form: content of existing rows, no row set
  change.
* **Governing layer — none.** No `AGENTS.md` change.
* **`doctrine/` — none**, and that is the routing decision above.
* **Descriptive layer — none.** No `docs/` file changes.
* **Release-facing** — `CHANGELOG.md > Unreleased > Added`, one entry.
* **Deliberation record** — this plan, its plan review, its code review, and
  the `dev/PLANNING.md` rows that serialize the plan-open and the residuals.

<!-- cairn:slot documentation-tier-home -->
**Doc tier home rule** — route doc and doctrine changes by layer per
[`docs/DOCUMENTATION_PLAN.md`](../../docs/DOCUMENTATION_PLAN.md):
cross-cutting prescription → governing layer (`AGENTS.md`);
deliberation about what to build → deliberation layer (`dev/`);
description of the software as it is → descriptive layer (`docs/`). A
plan's *Scope* must name the doctrine-surface touched (or an explicit
"no doctrine surface").
<!-- cairn:end documentation-tier-home -->

## The measured baseline

Every figure below was measured for this plan against the **working tree** on
2026-08-04 under the canonical interpreter
(`/Users/kendal30/conda_envs/lhm/bin/python3.13`, Python 3.13.13) with
`PYTHONDONTWRITEBYTECODE=1`. **No repository file was written while planning.**

**Read the dirty-tree caveat before quoting any of these.** At planning time
the working tree carried eight modified files and two untracked paths from
*concurrent* workflows (`bootstrap/_scaffold/install.py`, `lockfile.py`,
`upgrade.py`, `verify_integrity.py`, `bootstrap/UPGRADE.md`,
`bootstrap/_scaffold/SECURITY_MUTATIONS.md`, two test files, plus an untracked
`bootstrap/tests/test_fork_advisory.py`). Figures that depend on those files
are snapshots of a moving tree. **Re-measure at implementation; do not apply
these numbers.**

| Measurement | Value, `as_of 2026-08-04` | Trustworthy on a dirty tree? |
|---|---|---|
| Anchor: `### Author-accounting` in `dev/proposals/_template.md` | line 230, file is 400 lines | yes — untouched by concurrent work |
| Anchor: same heading in `templates/core/dev/proposals/_template.md` | line 213, file is 362 lines | yes |
| Anchor: `**Prospective only.**` paragraph, `dev/` side / shipped side | line 265 / line 248 | yes |
| Anchor: `### Author-accounting` in `dev/plans/_template.md` | line 216, file is 295 lines | yes |
| Anchor: same heading in `templates/core/dev/plans/_template.md` | line 208, file is 272 lines | yes |
| Author-accounting block parity, proposal pair (`dev` 230-267 vs shipped 213-250) | **byte-identical**, verified by extraction + `diff` | yes |
| Author-accounting block parity, plan pair (`dev` 216-228 vs shipped 208-221) | **byte-identical**, verified by extraction + `diff` | yes |
| `claim_check.py` over each of the four templates and over `test_scaffold.py` | 5 x `OK, no claim-check flags` | yes |
| `check_cairn.py` whole tree | `OK -- 180 Markdown file(s) scanned; no issues; 68 external link(s) not probed` | mostly — the count moves with the tree |
| `quality_gate.py --sub neutrality` | `fail=95 info=21` | **no** — was `fail=99` on 2026-08-03; live figure |
| `bootstrap/scaffold.py --manifest` | 96 lines = 1 header + **95 data rows** | yes |
| `token_budget.py` always-on total | `5,541 tok / 22,317 B` (`AGENTS.md` + `CLAUDE.md`) | yes |
| `pytest bootstrap/tests --collect-only -q` | **1746 collected** | **no** — concurrent workflows are adding nodes; the pinned figure in the gate manifest is 1598 |

**Two of these are load-bearing and neither is a number.**

* **The manifest rows for all four files are `substituted`, not `verbatim`** —
  measured: `dev/plans/_template.md`, `dev/proposals/_template.md` and their
  `core/dev/...` sources all carry `substituted`. So `substitute_tokens` runs
  over the added text at install. **The added text must contain no `{{` token
  sequence**, or the shipped and installed copies diverge. Verified against the
  proposed text: it contains none. Chunk E asserts it.
* **The vendor-neutrality gate covers only one side of each twin pair.**
  Measured in `scripts/quality_gate.py`: `_NEUTRALITY_FILE_SUFFIXES` scans
  every `.md` under `templates/`, and inside `templates/` an exemption
  directive is itself a failure — *"no exemption path; templates ship to
  adopters"*. `dev/` is in no scan root. So a vendor token added to the shipped
  copy fails the gate and the identical token in the self-host copy does not.
  This asymmetry is one more reason parity is checked by a test rather than
  inferred from "the gates are green".

### Gate accounting

* **One frozen file is modified: `bootstrap/tests/test_scaffold.py`.** It is a
  literal key in the 164-entry `frozen_files` map in
  `bootstrap/tests/fixtures/gate_manifest.json` (`as_of 2026-08-04`). None of
  the four Markdown templates is frozen; `CHANGELOG.md` and `dev/PLANNING.md`
  are not frozen. No new file is created, so there is no `FROZEN-NEW` row.
* **The consequence, and it is Maintainer-facing.** After this lands,
  `_gate_manifest.py verify` reports `FROZEN-MODIFIED:
  bootstrap/tests/test_scaffold.py (gate file edited — sha differs)` (message
  text quoted from `bootstrap/tests/_gate_manifest.py`, `as_of 2026-08-04`),
  which is a **HOLD**, and `COLLECTION-ADDED` for the new node, which is a
  recorded **note**, not a hold. See *Maintainer fence* below. The implementing agent
  does **not** re-pin.
* **The frozen map does not gate the suite.** `bootstrap/tests/test_gate_manifest.py`
  verifies against a manifest produced from the live tree at test time; the
  committed fixture is read only by the batch tooling
  (`bootstrap/tests/_gate_manifest.py`, `bootstrap/tests/_gate_preflight.py`)
  when an operator runs it. So `python -m pytest bootstrap/tests` stays green
  across this edit. Carried from the `scan-coverage` plan's measurement of the
  same property; **re-confirm rather than assume**, since that plan has since
  landed edits in this area.
* **No AST re-anchor.** No `bootstrap/_scaffold/` byte changes.
* **No gate-batch window is believed open.** The `gate-reanchor-preflight`
  batch archived 2026-08-03, so the HOLD-by-default posture that applied during
  it is not in force. Re-check at implementation; if a window has since opened,
  the frozen-file edit needs the batch's own handling.

## Sequence

**This is one implementing commit.** The chunks are ordered *working-tree*
steps inside it, not commit boundaries — the accepted scope is a single commit
and this plan does not enlarge it. Each chunk boundary is a **verification**
boundary: the step's acceptance criteria are met before the next step begins.

Chunk order is load-bearing. **Chunk A authors the test first and runs it RED
against the untouched tree.** That is the cheapest and strongest form of the
non-vacuity requirement: the failing state is not constructed, it is the state
the repository is already in, and it costs one `pytest` invocation.

```
0. plan-open  -- this plan + the dev/PLANNING.md row-move        [commit pending]
   (plan review) -- required(Internal); NO implementation before it lands
1. Chunk A -- the test, authored and RUN RED on the untouched tree  [working-tree step]
2. Chunk B -- the five questions land on the proposal twin pair     [working-tree step]
3. Chunk C -- the one clause lands on the plan twin pair            [working-tree step]
4. Chunk D -- six hazard-side perturbations, each RUN               [working-tree step]
5. Chunk E -- the gates, then the single implementing commit        [commit pending]
6. Chunk F -- the serialized record: CHANGELOG.md + dev/PLANNING.md [serialized; text below]
```

---

### Chunk A — the test, authored first and shown RED by the shipped state

| # | File | Change |
|---|------|--------|
| A1 | `bootstrap/tests/test_scaffold.py` | Module-level constants above `class TestInstallCore`, alongside the existing module-level helpers: `_SECURITY_PREFLIGHT_HEADINGS` (a 5-tuple of the literal heading strings), `_SECURITY_PREFLIGHT_GATE_PHRASE = "no trust boundary added, moved, or widened"`, `_SECURITY_PREFLIGHT_OPEN = "#### Security preflight — five questions, answered in writing"`, `_SECURITY_PREFLIGHT_CLOSE = "**Prospective only.**"`, `_PLAN_CLAUSE_MARKER = "security-preflight"`. Each is a **literal typed into the test body**. |
| A2 | `bootstrap/tests/test_scaffold.py` | Module-level helper `_extract_security_preflight(text: str) -> str`: returns the substring from the line equal to `_SECURITY_PREFLIGHT_OPEN` up to (exclusive) the first later line starting with `_SECURITY_PREFLIGHT_CLOSE`; **raises `AssertionError` with a message naming which marker was missing** if either is absent. Failure is *closed*, never a silent empty string — an extractor that returns `""` on a missing marker makes the parity comparison `"" == ""` and is the tautology shape one level down. |
| A3 | `bootstrap/tests/test_scaffold.py` | New node `test_installed_templates_carry_security_preflight_questions(tmp_path)` in `class TestInstallCore`, placed immediately after `test_installed_templates_carry_plan_review_line` (line 360, `as_of 2026-08-04`) and following its idiom exactly: resolve `cairn_root`, `pytest.skip("Cairn templates not available")` when `templates/` is absent, `create_dev_tree(tmp_path)`, `install_core(templates_root, tmp_path, tokens)`. Four assertion groups, below. |

**The four assertion groups, and what each one alone would miss.**

```
(a) SHIPPED SIDE, presence.   Over the INSTALLED tmp_path/dev/proposals/_template.md:
      each of the five literals in _SECURITY_PREFLIGHT_HEADINGS is present,
      and _SECURITY_PREFLIGHT_GATE_PHRASE is present.
      Over the INSTALLED tmp_path/dev/plans/_template.md:
      _PLAN_CLAUSE_MARKER is present.
    Misses: a self-host copy that never received the block.

(b) SELF-HOST SIDE, presence.  The same six literals over
      CAIRN_ROOT/dev/proposals/_template.md, and the marker over
      CAIRN_ROOT/dev/plans/_template.md, read directly.
    Misses: one-sided rewording of prose that is not one of the six literals.

(c) PROPOSAL-PAIR PARITY.  _extract_security_preflight() over
      CAIRN_ROOT/dev/proposals/_template.md and over
      CAIRN_ROOT/templates/core/dev/proposals/_template.md, compared as bytes.
    Misses: an identical wrong edit applied to both sides.

(d) PLAN-PAIR PARITY.  The clause sentence, as a literal in the test body,
      present in BOTH CAIRN_ROOT/dev/plans/_template.md and
      CAIRN_ROOT/templates/core/dev/plans/_template.md, compared after
      collapsing intra-sentence whitespace (the two copies wrap at the same
      column today, but the sentence -- not the wrap -- is the contract).
    Misses: nothing (a) and (b) do not already catch, for this one sentence;
      it is here so the plan pair is covered by the same shape as the
      proposal pair rather than by a different one.
```

**Group (a) plus group (c) is the pair that carries the argument.** (c) catches
the one-sided edit; (a)/(b) catch the two-sided edit that (c) is blind to.
Neither alone is sufficient and the plan does not claim either is.

**The oracle-channel note, stated because it is the thing that goes wrong.**
The oracle for (a), (b) and (d) is a set of literals in the test body. A human
copies those literals from the template **once, at authoring time**; that is
fine and is not a derivation. What is forbidden is the test *reading* a
template at run time to compute what it expects — that is
`test_scan_targets_cover_all_shipped_scripts`'s defect, the one that stayed
green for 63 days across the drift it was named for. Group (c) *does* read both
files at run time, and that is correct: neither file is the oracle for the
other's *content*, only for the other's *agreement*, and (a)/(b) supply the
content oracle independently.

**Acceptance criteria — Chunk A.**

* The node exists and `pytest bootstrap/tests/test_scaffold.py -q` reports
  exactly one failure: the new node.
* **The RED is observed, not predicted, and its message is copied into the
  commit body.** Against the untouched tree, group (a) fails on the first
  missing heading literal. This is the shipped state as the failing state —
  no perturbation was needed to produce it.
* No other node changes status. Baseline before A: whatever
  `pytest bootstrap/tests/test_scaffold.py -q` reports on a clean tree at
  implementation time (re-measure; do not use the 1746 whole-suite figure,
  which was taken on a dirty tree).
* **Nothing is committed in this chunk.**

---

### Chunk B — the five questions land on the proposal twin pair

The inserted bytes are **extracted mechanically from the accepted proposal**,
not retyped from this plan. That is this chunk's answer to S1: the material
that decides what the templates say comes from the committed Decision record,
through a channel this plan does not supply.

| # | File | Change |
|---|------|--------|
| B1 | `dev/proposals/_template.md` | Insert the extracted 43-line sub-block **after** the `This block is **reviewed as evidence...**` paragraph (ends line 263, `as_of 2026-08-04`) and **before** the `**Prospective only.**` paragraph (line 265), separated by one blank line on each side. |
| B2 | `templates/core/dev/proposals/_template.md` | The identical 43 lines, at the identical relative position: after the same paragraph, before `**Prospective only.**` (line 248, `as_of 2026-08-04`). |

**The extraction, specified so it is reproducible.** From
`dev/proposals/2026-08-03-claude-security-preflight-checklist.md`, take lines
**116-158** inclusive (43 lines, verified for this plan: every one begins `> `
or is exactly `>`), strip the leading `> ` (a bare `>` becomes an empty line).
The result:

* begins `#### Security preflight — five questions, answered in writing`
* ends `written claim a reviewer can falsify.`
* contains 4 blank lines
* has **sha256 `277daac432cfff21062a9ec58718138238183e79a4f988a8d90aeec62b01852b`**
  over the 43 lines joined by `\n` with a single trailing newline
  (`as_of 2026-08-04`, against the committed proposal — `git status` on that
  file is empty, so the bytes are HEAD's).

**Verify the hash before inserting.** If it does not match, the proposal moved
and this plan's line numbers are stale: re-read the proposal, re-derive the
block, and say so in the commit body. Do not apply a mismatched extraction.

**The text, reproduced for review convenience only — the proposal is
authoritative:**

```
#### Security preflight — five questions, answered in writing

*Gated to a **security-touching** change: one that adds, moves, or widens a
trust boundary (deserialization, subprocess invocation, parsing, file and path
handling, network I/O, credentials and environment — the `security-review`
module's boundary list), or one that touches a high-risk surface this project's
`AGENTS.md` names. For every other change, one line — "N/A: no trust boundary
added, moved, or widened" — is the correct entry.*

Answer all five, one or two sentences each. These are **design questions, asked
while the design is still movable** — not documentation written after it is
fixed. An absent answer is a review finding. A *wrong* answer is a falsifiable
review finding, which is the point: the reviewer checks a stated claim in one
read instead of hunting for an absence over four rounds.

* **S1 — Who supplied it?** ... (see the proposal, lines 131-152)
* **S2 — Can it fail?** ...
* **S3 — What fires it, over what?** ...
* **S4 — Which way does it break?** ...
* **S5 — Who still wins?** ...

**What these five do not reach.** They are structural questions about where
material comes from and what runs. A semantically valid instruction that is
hostile carries no lexical signature, and no question here finds it. They also
do not check whether an answer is *true* — they convert a hidden property into a
written claim a reviewer can falsify.
```

The five bullets are elided here **on purpose**: an implementing agent that
retypes them from this plan has used the wrong channel. Extract them.

**Acceptance criteria — Chunk B.**

* The 43 inserted lines are byte-identical in both files. Checked directly:
  `diff <(sed -n '<a>,<b>p' dev/proposals/_template.md) <(sed -n '<c>,<d>p'
  templates/core/dev/proposals/_template.md)` is empty, with the ranges
  re-derived after insertion.
* The inserted region's sha256 matches the extraction hash above in **both**
  files.
* **The whole `### Author-accounting` block is still byte-identical across the
  pair.** True before the edit (measured) and must stay true after. This is
  checked as a criterion here and deliberately **not** asserted by a test —
  see residual R5.
* `grep -c '{{' ` over the inserted region returns 0 in both files. The
  manifest marks these rows `substituted`; a token in the added text would make
  the installed copy differ from the shipped one.
* No line of the pre-existing Author-accounting content moved *relative to its
  neighbours*: the `**Prospective only.**` paragraph is still the block's last
  paragraph, and `### Tests required` still follows it.
* `python scripts/claim_check.py <file>` over each of the two files, one file
  per invocation, returns `OK, no claim-check flags` (baseline: both OK).
* **Nothing is committed in this chunk.**

---

### Chunk C — the one clause lands on the plan twin pair

The plan templates get a **clause**, not the block, because their
Author-accounting comment already incorporates the proposal template's block by
reference (*"same discipline as the proposal template's author-accounting"*).
Duplicating the block would create a four-file sync surface — the drift the
wrapper drift-guard exists to prevent — and would trade this change's one
hazard for a worse one.

**Why the plan pair is touched at all**, given the pointer exists: instance i
of the four failures the proposal is built on — finding [CR1] — was written
into a **plan**, not a proposal. A pointer a plan author must follow to reach
the questions is exactly the "the knowledge existed, in a form that did not
apply here" failure this change is about.

| # | File | Change |
|---|------|--------|
| C1 | `dev/plans/_template.md` | Inside the `<!-- Triage-gated ... -->` comment (lines 218-228, `as_of 2026-08-04`), insert the clause as a new sentence immediately after `...to the test that exercises it through its public path.` and before `Cite tests as relative markdown links...`. **Both are on line 223** — the sentence boundary is mid-line, so the insertion re-wraps the rest of the comment. Wrap to the comment's existing ~76-column wrap. |
| C2 | `templates/core/dev/plans/_template.md` | The identical sentence at the identical position inside the same comment (lines 210-221, `as_of 2026-08-04`; the block is byte-identical to C1's, verified for this plan — so the same mid-line boundary applies at the same relative offset). |

**The clause, word-for-word from the proposal (lines 233-235):**

> A security-touching plan re-answers the five security-preflight questions only
> where its chunking changes an answer — most often S2 (which chunk runs the
> mutation) and S3 (which gate command fires the check).

**The wrap is the only permitted difference** between the proposal's rendering
and the inserted text: the proposal wraps it as a 3-line indented blockquote,
the templates wrap the comment at a different column. The *words* are the
contract, which is why Chunk A's group (d) compares after collapsing
intra-sentence whitespace and group (a)/(b) pin only the `security-preflight`
marker.

**Why the marker is `security-preflight` and not a longer literal.** It is the
one token that is (i) present in the clause, (ii) absent from the plan template
today — verified: `grep -c security-preflight` returns 0 in both plan templates
`as_of 2026-08-04` — and (iii) short enough that a re-wrap cannot split it
across lines. A longer literal would fail on a legitimate re-wrap, which trains
an author to weaken the test.

**Acceptance criteria — Chunk C.**

* The clause is present in both files; `grep -c 'security-preflight'` returns
  the same non-zero count in both.
* The two Author-accounting comments remain byte-identical across the pair
  (they are today; the insert must not disturb that).
* The comment still closes with ` -->` and `python scripts/check_cairn.py`
  over both files reports no `instruction-html-comment` flag. **Check this
  explicitly**: the clause is imperative prose added inside an HTML comment,
  and Cairn's content scanner has a detector for exactly that shape. The
  existing comment already carries imperative prose and passes, so the expected
  result is a pass — but the expectation is checked, not assumed, because a
  flag here would need a `cairn-accept` directive, and such a directive is
  **forbidden inside `templates/`** (measured in `scripts/quality_gate.py`).
  A flag on the shipped side would therefore force a rewording, not a
  suppression. That is the correct direction and it is better to find it in
  this chunk than at the gate.
* `python scripts/claim_check.py <file>` over each, one per invocation → OK.
* **Nothing is committed in this chunk.**

---

### Chunk D — six hazard-side perturbations, each RUN

This is the chunk the plan exists for. **Every perturbation below is applied to
a template file — the hazard — never to the test's own body.** Perturbing the
test proves the test can fail; only perturbing the hazard proves the test
protects the thing it names. Each is a working-tree edit, run, then reverted;
after each revert, `git diff <path>` must be empty and `git status --short`
must show no residue.

The whole ledger — the change made, the message observed, the verified restore
— goes in the commit body.

| ID | Perturbation (applied to) | Must go RED | Must stay GREEN | What it proves |
|---|---|---|---|---|
| **P1** | Delete the line `* **S3 — What fires it, over what?** ...` from `templates/core/dev/proposals/_template.md` | group (a) on the S3 literal, **and** group (c) parity | groups (b), (d) | the shipped side is pinned, and a one-sided delete is caught twice |
| **P2** | Delete the same line from `dev/proposals/_template.md` only | group (b) on the S3 literal, **and** group (c) parity | groups (a), (d) | **the self-host side is pinned** — this is the half the proposal's original one-file test would have missed entirely |
| **P3** | Delete `security-preflight` from the clause in `templates/core/dev/plans/_template.md` | groups (a) and (d) | (b), (c) | the shipped plan clause is pinned |
| **P4** | Delete `security-preflight` from the clause in `dev/plans/_template.md` | groups (b) and (d) | (a), (c) | the self-host plan clause is pinned |
| **P5** | **Delete the S4 heading line from BOTH proposal templates**, identically | groups (a) **and** (b) | group (c) — parity holds, both files agree | **the discriminator for the literal-list oracle.** A pure A-vs-B parity check stays green here. P5 going red is what proves (a)/(b) carry weight over (c) — and it is the perturbation that would go GREEN if a later author "simplified" the test by deriving its expected set from a template |
| **P6** | Reword one sentence *inside* the sub-block that is **not** one of the six pinned literals — e.g. change `over four rounds` to `over several rounds` — in `dev/proposals/_template.md` only | group (c) parity | groups (a), (b), (d) | **the discriminator for the parity assertion.** The literal list is blind here. P6 going red is what proves (c) carries weight over (a)/(b) |

**P5 and P6 are the pair that makes this test non-trivial**, and a reviewer
should reproduce those two before any other. Each is red under exactly one half
of the oracle and green under the other; together they show neither half is
redundant. P1-P4 are the per-file coverage sweep and are cheaper.

**One further perturbation, because this repository has an instance of the
failure it guards.**

* **P7 — the code-point pin.** In `templates/core/dev/proposals/_template.md`,
  replace the em dash (`U+2014`) in the S1 heading with an ASCII hyphen-minus,
  changing nothing else. Group (a) must go RED on the S1 literal. This proves
  the heading pin is **code-point-exact**, which matters here specifically:
  `byline-classification` found a live defect in this repository where a
  Cyrillic homoglyph silently changed a classification, and S4 exists because
  of it. A pin that tolerates a confusable is not a pin. Revert; confirm
  `git diff` empty.

**A perturbation that is deliberately NOT run, and why saying so matters.**
There is no perturbation that makes the *installed* copy diverge from the
*shipped* source, because `install_core` copies with token substitution and the
added text has no tokens — the two are the same bytes by construction. Group
(a) therefore tests the shipped source *through* the install path; it does not
independently test the install path. Stated here rather than implied, so nobody
later reads group (a) as an install-fidelity check.

**Acceptance criteria — Chunk D.**

* All seven perturbations **run**, each with its observed failure message
  recorded and each reverted to a byte-identical state
  (`git diff <path>` empty after every one).
* The red/green column is observed to match the table **exactly**. A
  perturbation that goes red in a group the table says should stay green is a
  finding against this plan, not a pass: it means the assertion groups are not
  independent and the discrimination argument above is wrong.
* After the last revert, `pytest bootstrap/tests/test_scaffold.py -q` is fully
  green and `git status --short` shows only the four templates and the test
  file as modified.
* **Nothing is committed in this chunk.**

---

### Chunk E — the gates, then the single implementing commit

| # | File | Change |
|---|------|--------|
| E1 | *(none)* | Run the full gate set below and record the figures. |
| E2 | *(the commit)* | One commit naming exactly five paths: the four templates and `bootstrap/tests/test_scaffold.py`. Path-scoped, `git commit <paths>` with no separate `git add` (all five are tracked). |

**Acceptance criteria — Chunk E.**

* `python -m pytest bootstrap/tests` under the canonical interpreter
  (3.13.13), `PYTHONDONTWRITEBYTECODE=1` — **green, 0 failed / 0 skipped /
  0 xfailed**, with collection **grown by exactly one node** against a
  re-measured pre-change baseline. Re-measure the baseline on the current tree
  immediately before the run; the 1746 figure in this plan was taken on a dirty
  tree and is not a baseline.
* `python bootstrap/scaffold.py --manifest` diffed against a capture taken
  **before** Chunk B into the session scratch directory — **expected empty**,
  95 data rows. The empty diff is the assertion that the install contract's row
  set is untouched. The baseline arrives from a pre-change execution recorded
  outside the repository; the artifact under verification does not supply it.
* `python scripts/check_cairn.py` — OK. 180 Markdown files `as_of 2026-08-04`;
  the count moves with the tree and may only grow.
* `python scripts/quality_gate.py --sub neutrality` — **unchanged against a
  pre-change run in the same session**, not against this plan's `fail=95`. The
  figure moved by four in one day. The added text names no AI model or vendor;
  this is the gate that proves it and it is the gate a shipped template change
  must clear.
* `python scripts/claim_check.py <file>` over each of the four templates, one
  file per invocation (the checker exits 2 on more than one path) — all OK.
* `python scripts/token_budget.py` — unchanged. The always-on budget covers
  `AGENTS.md` and `CLAUDE.md` only (`5,541 tok`, `as_of 2026-08-04`); the
  proposal template is read on demand, so ~43 added lines cost nothing against
  the standing budget. Named because "does this bloat the always-on context" is
  the first fair objection to any template addition.
* **The commit body carries**, and the commit does not land without them:
  1. the seven-row perturbation ledger from Chunk D;
  2. the Chunk A RED observation (the shipped state as the failing state);
  3. the extraction hash and the confirmation that both inserted regions match
     it;
  4. the gate-integrity note: `bootstrap/tests/test_scaffold.py` now differs
     from its pinned sha256 in `bootstrap/tests/fixtures/gate_manifest.json`,
     so a later `_gate_manifest.py verify` reports one `FROZEN-MODIFIED` and
     one `COLLECTION-ADDED`. **Do not re-pin** — see *Maintainer fence*.
* Body length: this is a non-trivial implementing commit, so 15-30 lines, soft
  cap ~50, per `AGENTS.md`. The perturbation ledger is the bulk of it; the
  proposal and plan carry the reasoning and are cross-referenced by stem.

---

### Chunk F — the serialized record

`CHANGELOG.md` and `dev/PLANNING.md` are **shared communication files**, edited
only at defined serialization points. **This plan does not edit them and no
agent executing it edits them in passing.** The exact text is returned to the
Maintainer for the next serialization point (a goodnight scrub or explicit
instruction).

**`CHANGELOG.md > Unreleased > Added` — one entry:**

```
- **Five questions a security-touching change answers before review.** The
  proposal template's `Author-accounting` block now carries a gated
  `Security preflight` sub-block: who supplied the material a decision is made
  from (S1), what one-line mutation makes each enforcing check fail (S2), what
  command fires the check and over what input set (S3), which side of the
  boundary each default and fallback lands on when it goes wrong (S4), and
  which attacker capability still succeeds afterwards (S5). Each traces to a
  real finding in this repository's record; four instances of S1's shape landed
  in one week and four different readers -- never the author -- caught them. The
  plan template gains a one-clause pointer rather than a copy, so the four
  template files stay a two-pair sync surface instead of a four-way one, and a
  new test in `bootstrap/tests/test_scaffold.py` pins the shipped side, the
  self-host side, and their parity. Nothing mechanical checks that a proposal
  *answers* the questions, and the block says so. Proposal
  `security-preflight-checklist`, plan `security-preflight-checklist`.
```

**`dev/PLANNING.md > ## Active` — one row, at plan-open:**

```
* **security-preflight-checklist** *(plan open 2026-08-04; Internal plan review
  required before implementation)* -- five security-preflight questions (S1-S5)
  added to the `Author-accounting` block of both proposal templates, a
  one-clause pointer to both plan templates, and one test in
  `bootstrap/tests/test_scaffold.py` pinning the shipped side, the self-host
  side, and the twin parity between them. One implementing commit over five
  files. The plan departs from the proposal in exactly one declared way -- the
  proposal said parity would stay a convention and the plan makes it an
  assertion -- and fences that departure as strikeable in one line.
```

**`dev/PLANNING.md > ### Deferred follow-ups (durable home)`, under
**Lifecycle apparatus** — one row carrying every residual, so no trigger lives
only in an artifact that will archive:**

```
* **Security-preflight residuals (R1-R5)** *(deferred, Aug 2026)* -- the
  five-question preflight block ships declared-unenforced, and these are its
  named expiry triggers. **R1**: plan templates carry a clause, not the block,
  so a security-touching plan whose source proposal predates the change
  inherits no answered block -- trigger is the first such plan. **R2**: the
  security-touching gate is self-judged; nothing checks an "N/A" line --
  trigger is the *second* review that finds a security-touching change which
  wrote one. **R3**: nothing mechanical fires at all; enforcement is a reviewer
  declining to review an unanswered block -- trigger is the `transition-lint`
  proposal landing a lifecycle linter with somewhere cheap to add a presence
  check. **R4**: five shapes, not all shapes -- trigger is the first security
  finding that fits none of the five, at which point the shape has an instance
  and the recurrence limb applies to adding it. **R5**: the parity test pins
  only the added sub-block, while the whole `Author-accounting` block is
  byte-identical across both twins today -- trigger is the first legitimate
  divergence inside that block (a `cairn:slot` added to one side), which is the
  moment to decide whether the wider invariant is worth asserting. Ritualization
  recovery (cut to S1 and S2) fires on either of two `git grep`-able signals:
  three consecutive proposals whose S1-S5 answers are byte-identical to a prior
  proposal's, or any proposal answering all "N/A" while its own `Touches` line
  names a surface `AGENTS.md` lists under *High-risk surfaces*.
```

## Acceptance criteria

Per-chunk criteria are above; these are the plan-level deliverables.

* **Tests that must pass.**
  * `python -m pytest bootstrap/tests` — the whole suite, green, **0 failed /
    0 skipped / 0 xfailed**, under the canonical interpreter (3.13.13) with
    `PYTHONDONTWRITEBYTECODE=1`. Collection grows by **exactly one** node and
    drops none. Baseline re-measured immediately before the run, not quoted
    from this plan.
  * [`bootstrap/tests/test_scaffold.py`](../../bootstrap/tests/test_scaffold.py)
    — the one new node, with its four assertion groups. The link resolves to
    the existing test **file**; the added **node** does not exist yet, which is
    the one thing the template's link form cannot express.
  * [`bootstrap/tests/test_notice_install.py`](../../bootstrap/tests/test_notice_install.py)
    — unchanged and green. Named because it holds the repository's existing
    twin-parity test, which covers `scripts/`/`tools/` `.py` twins and
    **not** the `dev/**/_template.md` twins; that gap is why Chunk A's group
    (c) exists, and the two must not be confused for each other.
  * **Every assertion group shown non-vacuous by a run hazard-side
    perturbation** (P1-P7), with the ledger in the commit body. Where a check
    cannot be made to fail, the plan says so instead — see Chunk D's
    deliberately-not-run entry.
* **Doc updates that must land.** All hand-authored: the four `_template.md`
  files. No generated docs, no snippet-synced blocks.
  `CHANGELOG.md > Unreleased > Added` — one entry, **serialized**, text in
  Chunk F, not written by the implementing agent.

  <!-- cairn:slot acceptance-doc-tooling -->
  Cairn's doc surface is mostly hand-authored Markdown read on GitHub;
  the doc tooling is drift-prevention, not generation:
  - **Snippet-sync** — `python scripts/sync_doc_snippets.py` pulls
    fenced blocks from runnable example sources into docs; update the
    source, then run the sync (never hand-edit a synced block).
  - **Prose-integrity gate** — `python scripts/check_cairn.py` resolves
    every internal Markdown link / anchor and every claim-path; it is
    the doc smoke for any Markdown change.
  - **Link check** — `python scripts/link_check.py` for the broader
    cross-reference sweep.
  There is no schema-render generator; a plan that introduces one names
  its source + render command here.
  <!-- cairn:end acceptance-doc-tooling -->
* **Examples / smoke checks required.** `python bootstrap/scaffold.py
  --manifest` — expected **byte-identical** to a pre-change capture, which is
  itself the assertion that this change alters no install-contract row.
  **N/A**: the example gallery under `examples/` — this change touches nothing
  the runnable examples demonstrate.
* **Inbound path-link updates.** None expected. `dev/PLANNING.md` and
  `dev/NEXT_SESSION.md` refer to plans by filename stem, not path link, so the
  archive-move needs no edit there. Confirm at archive time rather than assume.

### Author-accounting — invariants, failure modes, edge cases

* **Invariants, each with the chunk that enforces it.**
  * *The shipped proposal template carries all five question headings and the
    gating phrase.* Enforced by Chunk A group (a), in
    [`bootstrap/tests/test_scaffold.py`](../../bootstrap/tests/test_scaffold.py);
    shown to fail by P1 and P5.
  * *The self-host proposal template carries the same six literals.* Enforced
    by group (b); shown to fail by P2 and P5.
  * *The added sub-block is byte-identical across the proposal twins.*
    Enforced by group (c); shown to fail by P1, P2 and P6, and shown **not** to
    fail by P5 — which is the honest statement of its limit.
  * *Both plan templates carry the clause.* Enforced by groups (a), (b) and
    (d); shown to fail by P3 and P4.
  * *The install manifest's row set is unchanged.* Enforced by the empty diff
    against a pre-change capture, in Chunk E. **Not guarded by any test**, and
    that is the claim a reviewer should attack: nothing goes red if a later
    change adds a row.
  * *The whole `### Author-accounting` block stays byte-identical across the
    proposal twins.* True today, checked as a Chunk B criterion, and
    **deliberately not asserted by a test** — residual R5.
  * *The added text carries no `{{token}}`.* Both rows are `substituted`; a
    token would make the installed copy differ from the shipped source.
    Enforced by inspection in Chunk B, **not** by a test.
* **Public-path → test mapping.** This change adds no code entry point. The one
  public surface is the *installed* template, whose entry point is
  `install_core`; Chunk A's node drives that function and asserts against the
  installed file, matching the existing
  `test_installed_templates_carry_plan_review_line` in the same class. Groups
  (b), (c) and (d) read Cairn's own tree directly and are **not** exercised
  through `install_core` — they are self-host parity assertions, not install
  assertions, and the distinction is stated so nobody reads them as coverage of
  the install path.
* **Failure modes.**
  * A heading missing from either proposal template → **closed** (assert).
  * The sub-block present in one twin and absent or reworded in the other →
    **closed** (group (c) raises via `_extract_security_preflight`, or the byte
    comparison fails).
  * The sub-block's start or end marker missing → **closed**: the extractor
    raises with a message naming the missing marker. It does **not** return an
    empty string, which would make the parity comparison vacuously true.
  * The clause missing from either plan template → **closed**.
  * `templates/` absent → **open by design**: `pytest.skip`, the idiom shared
    with the sibling node. It does not fire on the canonical host; if it ever
    does, the 0-skipped rule fails, which is the correct direction.
  * `dev/` absent from the checkout → **open**, same skip idiom, same
    direction. This is a new population for the engine suite (see *Edge cases*).
  * **An author judges their security-touching change not security-touching and
    writes the N/A line** → **open, and intentionally so.** Nothing checks the
    judgment. This is the proposal's residual R2 and the change's largest
    failure mode; it is priced in the proposal's *Alternatives* and is not
    closed here.
  * **A proposal answers all five and the answers are wrong** → **open.** The
    block converts a hidden property into a written claim; it does not check
    the claim's truth. R3.
* **Edge cases handled.** An adopter who installed before this change (their
  template is unchanged until they upgrade — this adds no upgrade obligation).
  A proposal that is security-touching but adds no test (S2's honest answer is
  "no new check; the invariant rests on X", which is itself the finding). A
  plan whose source proposal predates this change (R1). A legitimate re-wrap of
  the plan clause (group (d) compares after collapsing intra-sentence
  whitespace; groups (a)/(b) pin only the unsplittable `security-preflight`
  marker). A confusable code point substituted into a heading (P7 pins the
  em dash exactly). **Out of scope:** proposals already open on 2026-08-03 —
  the block is *prospective only* per the paragraph it sits inside.
* **Known omissions / intentionally untested edges.**
  (a) Nothing tests that a proposal *answers* the questions, and no test can —
  a presence check passes on five "N/A"s and an accuracy check is the judgement
  the block exists to prompt.
  (b) Nothing tests answer quality.
  (c) The install-contract row set is checked by a diff, not by a test.
  (d) The no-`{{token}}` invariant is checked by inspection, not by a test.
  (e) **Chunk A groups (b)-(d) read `CAIRN_ROOT/dev/` from the engine suite,
  which is a new population.** The precedent for *"the engine suite reads
  Cairn's own tree outside `templates/` to enforce twin parity"* is
  `test_every_self_hosted_twin_stays_byte_identical_to_its_source` in
  `bootstrap/tests/test_notice_install.py`, which reads `CAIRN_ROOT / <dst>`
  for `scripts/` and `tools/` destinations. The new element is only the `dev/`
  prefix. Named because it is the kind of thing a reviewer should get to strike
  rather than discover.
  (f) Whether the stale frozen pin is re-anchored now or at the next supervised
  re-anchor is a Maintainer question this plan raises and does not answer.

#### Security preflight — this plan's own five answers

Dogfooded, because a plan that ships the five questions and does not answer
them is the ritual failure it is trying to prevent.

* **S1 — Who supplied it?** This plan makes one decision that matters: *what
  bytes go into the templates*. The input is
  `dev/proposals/2026-08-03-claude-security-preflight-checklist.md` lines
  116-158, read from the committed record (`git status` on that file is empty),
  pinned by sha256 `277daac4...` before insertion. **This plan's own prose is
  explicitly not that channel** — the five bullets are elided from Chunk B on
  purpose so an implementing agent cannot retype them from here. The test's
  oracle is a set of literals typed into the test body; the only run-time read
  of a template as an oracle is group (c), where each file is the oracle for
  the other's *agreement* only, with (a)/(b) supplying content independently.
  No input is supplied, directly or by reference, by anything being decided
  about.
* **S2 — Can it fail?** Seven hazard-side perturbations, P1-P7, every one
  applied to a template file and every one required to be **run**, not
  predicted. P5 and P6 are the discriminating pair: P5 is red under the literal
  oracle and green under parity, P6 the reverse, so neither half of the oracle
  is redundant and neither can be quietly deleted without a red. The one thing
  that would make the test unfalsifiable — deriving the expected set from a
  template at run time — is precisely what P5 detects, forever.
* **S3 — What fires it, over what?** `python -m pytest bootstrap/tests` runs
  it; nothing selects it conditionally except the `pytest.skip` guard shared
  with its sibling, which does not fire on the canonical host (and if it ever
  does, the 0-skipped rule fails — the correct direction). It covers **six
  literal strings and one extracted region across four files, and nothing
  else**. The adopter-facing sentence describing that scope is the test's own
  docstring plus the proposal's *What this change explicitly does not do*
  section; the two must agree, and Chunk A's docstring requirement is what
  makes them.
* **S4 — Which way does it break?** Three degraded paths. (i) The
  security-touching gate: a mis-judged N/A skips the block, landing on the
  **less-scrutiny** side — intentional, R2. (ii) The sub-block extractor: a
  missing marker **raises** rather than returning `""`, landing on the
  more-scrutiny side; the alternative would make parity vacuously true, which
  is the failure direction that matters. (iii) The `pytest.skip` guards:
  absence of `templates/` or `dev/` skips rather than fails at the node, but
  the suite-level 0-skipped rule converts that into a gate failure, so the
  net direction is closed.
* **S5 — Who still wins?** This change assumes **no** attacker capability and
  removes **none**. Every attack that succeeded before it succeeds after it;
  what changes is the round in which a defender is likely to notice. The class
  is closed neither by construction nor by enumeration, because it is not a
  control at all — it is an authoring aid, and the proposal's own S5 says so in
  the same words. The nearest thing to a new surface is the added test's read
  of `CAIRN_ROOT/dev/`, which grants nothing and reads two tracked files.

## Verification

Run under the canonical interpreter
(`/Users/kendal30/conda_envs/lhm/bin/python3.13`, 3.13.13) with
`PYTHONDONTWRITEBYTECODE=1`. A different Python minor silently changes the
suite figure; name the interpreter alongside any figure asserted.

<!-- cairn:slot verification-commands -->
The standing gates Cairn runs before a change lands (the same ones CI
enforces):

* **Engine suite** — `python -m pytest bootstrap/tests` (the whole
  suite; scope to `bootstrap/tests/test_<surface>.py` while iterating,
  but the full suite gates the cut).
* **Prose integrity** — `python scripts/check_cairn.py` (internal link
  / anchor resolution + claim-path check over the Markdown tree).
* **Quality gate** — `python scripts/quality_gate.py` (order-
  independence + vendor-neutrality + redundancy; `--sub neutrality`
  alone for a doctrine / template wording change).
* **Write-time claim check** — `python scripts/claim_check.py <file>` over
  each proposal / plan / doc the change authored. **One file per
  invocation** — the checker takes a single path and exits 2 (usage) on
  more, so loop rather than passing a list.

Plan-specific gates (a security-lint budget, a doc-drift gate, the
model-selection mapping check `python scripts/check_model_selection.py`)
are added per plan when the change touches that surface.
<!-- cairn:end verification-commands -->

**Plan-specific gates, added here because this change touches those surfaces.**

* **The install-contract assertion** — `python bootstrap/scaffold.py
  --manifest`, captured to the session scratch directory **before** Chunk B and
  diffed after Chunk C. **Expected empty**; 95 data rows, `as_of 2026-08-04`.
  A non-empty diff means a row set moved and is a stop-and-re-review.
* **The token-substitution assertion** — `grep -n '{{' ` over each inserted
  region in all four files. Expected: no match. The rows are `substituted`.
* **The neutrality gate on the shipped side** — `python
  scripts/quality_gate.py --sub neutrality`, compared against a **pre-change
  run in the same session**. The figure was `fail=95 info=21` on 2026-08-04 and
  `fail=99` the day before; it is live and must not be quoted from this plan.
  Note the asymmetry recorded above: this gate reads `templates/` and not
  `dev/`, so it covers one side of each twin pair only.
* **The content-scan check on the plan-template comment** — `python
  scripts/check_cairn.py dev/plans/_template.md` and the same over the shipped
  twin. Expected: no `instruction-html-comment` flag. A flag on the shipped
  side cannot be suppressed with a `cairn-accept` directive (forbidden inside
  `templates/`) and must be resolved by rewording.
* **The perturbation ledger** — seven rows, in the commit body: the change
  made, the failure observed with its message, the groups that stayed green,
  and the byte-identical restore verified with `git diff <path>` (empty).
* **The gate-integrity note** — in the commit body: `bootstrap/tests/test_scaffold.py`
  now differs from its pinned sha256 in
  `bootstrap/tests/fixtures/gate_manifest.json`, so a later
  `_gate_manifest.py verify` reports one `FROZEN-MODIFIED` (a HOLD) and one
  `COLLECTION-ADDED` (a recorded note). Do not re-pin.

**Note on doc gates**: drift gates catch **drift**, not **absence** of new doc
updates. `check_cairn` checks link and claim-path integrity, not whether a
sentence is true. Nothing in this verification set establishes that the five
questions are *good* questions — that argument is the proposal's, it was
reviewed, and it is settled.

## Maintainer fence

Three things in this change's blast radius are **not** an implementing agent's
to perform. Each is listed with what the agent does instead.

1. **Re-pinning the gate manifest.** Editing
   `bootstrap/tests/test_scaffold.py` makes its committed sha256 stale, and
   adding a node makes the pinned `node_count` (1598) and `node_ids` list stale
   by one. Re-pinning runs through `bootstrap/REANCHOR_RUNBOOK.md`, which
   states in terms that *"running the steps below is the Maintainer's act — an
   implementing agent must not"* perform them. **The agent's whole obligation
   is to name the stale entry in the commit body.** No re-pin, no
   `_gate_manifest.py` mutation, no `refs/cairn/gate-anchor` movement.
2. **Committing `CHANGELOG.md` or `dev/PLANNING.md`.** Both are shared
   communication files edited only at a serialization point. Chunk F returns
   their text; it does not write them. An implementing agent that bundles
   either into the implementing commit also **loses the deliberation-commit
   carve-out** and re-triggers the approval gate.
3. **Pushing.** The deliberation-artifact carve-out covers `git commit` only.
   Pushing always needs explicit Maintainer approval.

**No key, no credential, and no signing operation is required by this change.**
Stated explicitly because the surrounding batch (`release-authenticity`,
`gate-reanchor-preflight`) is full of ceremonies that do need them, and the
absence here should be a recorded fact rather than an assumption. Nothing in
this plan touches `dev/.cairn/local-env.json`, the allowed-signers roster, the
AST baseline, or any release tag.

**One open Maintainer question, raised and not answered:** whether the stale
frozen pin for `bootstrap/tests/test_scaffold.py` is re-anchored now or folded
into the next supervised re-anchor. This plan does not need an answer to
proceed; it needs the question on the record.

## Plan review

*Required — **Internal**. No implementation step runs until a review has landed
under this heading.*

> **The landed review appends here as a `### Plan review -- <reviewer> --
> YYYY-MM-DD` sub-heading** (plus a `### Sharpening` sub-heading if it raised
> findings). **Do not rename the `## Plan review — the brief` heading below to
> a bare `## Plan review`** — the lifecycle checker matches a section *kind*,
> not a review, so a bare heading would report the gate satisfied before any
> review existed. Measured for a sibling plan against the shipped header regex
> in `tools/lifecycle_planner.py`: a bare `## Plan review` **is** registered as
> a landed review section, while a heading carrying an em dash and further
> words is not parsed as a section at all.

## Plan review — the brief

**The declared tier is Internal, and the Internal round about to run
discharges it.** Said plainly because three sibling plans in this batch carry
a `## Plan review — the brief, and why the tier is not discharged` heading,
and this one is genuinely different.

**Why Internal is the ceiling, checked against the triggers rather than
asserted.** The proposal header set the ceiling and the Decision ratified it.
Re-checking each trigger against this plan's actual file set:

| Trigger (`AGENTS.md` > High-risk surfaces, and the proposal template's triage list) | Touched? |
|---|---|
| `doctrine/` or the invariant kernel | **no** — routing decision, argued in the proposal |
| `AGENTS.md` | **no** — cited, not edited |
| The scaffold / merge engine (`bootstrap/_scaffold/`) | **no** |
| Any gate script (`check_cairn`, `claim_check`, `quality_gate`, `security_check`) | **no** — run, not edited |
| The install contract's **row set** | **no** — content of two existing rows; empty manifest diff asserted |
| Vendor-neutrality boundary | **no new name**; the gate is run as a criterion |
| The by-file license split | **no** |
| The local interpreter binding | **no** |

The one surface that is *adjacent* to a trigger is
`bootstrap/tests/test_scaffold.py`, which is a **frozen** file in the gate
manifest. Frozen is not the same as a gate script: the file is a consumer of
the engine's public functions, it enforces nothing at release time, and the
consequence of editing it is a recorded HOLD for a supervised re-pin, which is
fenced above. An Internal reviewer is competent to that.

**What this review should aim at, in priority order.**

1. **The declared divergence.** The proposal says parity stays a convention;
   this plan makes it an assertion. Is the three-bound fence (no new file,
   sub-block only, strikeable in one line) actually a fence, or does it read as
   one while widening the contract? This is the single place the plan departs
   from the accepted artifact and it is the right place to attack it.
2. **Do P5 and P6 actually discriminate?** The plan's whole non-vacuity
   argument rests on the claim that P5 is red under the literal oracle and
   green under parity, and P6 the reverse. **Reproduce that pair first.** If
   either goes red in both, the two assertion halves are not independent and
   the plan's argument for keeping both is wrong.
3. **Is the extraction channel real, or theatre?** Chunk B elides the five
   bullets so an agent must extract them from the proposal, and pins the result
   by sha256. Does that survive contact with an implementing agent who has this
   plan in context and the proposal in context simultaneously — or does the
   hash just get quoted back? If the answer is the latter, say so; the fix is
   cheap and this is the plan's own S1 answer under test.
4. **The new population.** Groups (b)-(d) read `CAIRN_ROOT/dev/` from
   `bootstrap/tests/`. The precedent cited is
   `test_every_self_hosted_twin_stays_byte_identical_to_its_source`, which
   reads `CAIRN_ROOT/scripts/` and `CAIRN_ROOT/tools/`. Is the `dev/` prefix a
   difference that matters — for a sdist checkout, for a CI runner, for an
   adopter who vendors the engine suite?
5. **The extractor's failure direction.** `_extract_security_preflight` raises
   on a missing marker instead of returning `""`. Confirm that is what the
   specification says *and* that a reviewer of the eventual code would catch a
   later "simplification" to a `.partition()` that returns empty. This is S4
   applied to the plan's own helper.

**What the reviewer should not spend attention on.** The design of the five
questions, the choice of five rather than ten, the decision not to touch
`doctrine/`, and the decision to leave the block unenforced against filled
proposals are all settled by the Decision and are not re-opened by this plan. A
finding that the questions should be reshaped is a finding against the
Decision, not against this plan, and should say so.

**The stopping rule.** A finding is one of exactly two things. Either it names
a violation of a stated invariant in *Author-accounting* or a row in Chunk D's
perturbation table — then it is a bug against a stated property and the fix is
bounded. Or it names a property **not** stated and a perturbation **not** in
the table — then the specification was incomplete, the row is added, and every
earlier chunk is re-swept against it. The second branch is the expensive one
and is supposed to be.

## Code review

*Filled in after implementation commits land.* Per `doctrine/plans.md`, the
reviewer is **not** the implementing agent, the section is append-only, and a
clean final review carries a falsification ledger and a coverage line.

## Code review — the brief (no review has landed)

The landed review appends under the `## Code review` heading above as a
`### Code review -- <reviewer> -- YYYY-MM-DD` sub-heading, beginning with
`**Model**: <model or tier when known>` — queried, never copy-pasted from a
past template or archive.

**The one thing a code reviewer should do that the plan cannot do for them:**
re-run P5 and P6 against the *landed* test rather than against the plan's
description of it. The plan's argument is that the two assertion halves are
independent; only a run against the real code establishes that the shipped test
has the property the plan specified.

## Lasting-truth migration

*Filled in at archive time.* Per the
[Archive preconditions rule](../PLANNING.md#archive-preconditions-proposals-and-plans),
plans archive only after every deferred follow-up has a durable home outside
the plan.

**Pre-declared homes, so no trigger is left in an artifact that will archive:**

| Follow-up | Durable home |
|---|---|
| **R1** — plan templates carry a clause, not the block; a plan whose source proposal predates this change inherits no answered block | `dev/PLANNING.md > Deferred follow-ups (durable home) > Lifecycle apparatus`, in the consolidated R1-R5 row whose text is in Chunk F |
| **R2** — the security-touching gate is self-judged | same row |
| **R3** — nothing mechanical fires; revival path is the `transition-lint` proposal | same row |
| **R4** — five shapes, not all shapes | same row |
| **R5** — the parity test pins the added sub-block only, while the whole `Author-accounting` block is byte-identical across the twins today | same row (this plan's addition; not a proposal residual) |
| The **ritualization recovery triggers** ([E2], bound in the author Response to the External review) | same row — they are `git grep`-able and must outlive both the proposal and this plan |
| The **stale frozen pin** for `bootstrap/tests/test_scaffold.py` | the implementing commit body, plus whatever supervised re-anchor consumes it; **not** this plan |
| The **twin-parity gap for `dev/**/_template.md`** that Chunk A's group (c) partially closes | the test's own docstring, which must state that it covers the added sub-block and not the whole block |

**One thing that must not migrate:** the sub-block's text. Its durable home is
the four template files themselves and the accepted proposal. This plan is not
a second source for it, which is why Chunk B elides the five bullets.

This section is append-only once written.
