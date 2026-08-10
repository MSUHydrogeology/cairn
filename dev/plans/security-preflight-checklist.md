<!-- cairn-internal-ref-allow: doctrine/dual-review.md doctrine/plans.md doctrine/rationale.md doctrine/lifecycle.md doctrine/coordination.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see AGENTS.md, "Where doctrine/ references resolve") -->
<!-- claim-check-allow: dev/proposals/2026-08-03-claude-security-preflight-checklist.md -->
<!-- ^ Source/sibling proposals archived 2026-08-04. These citations sit in
     append-only sections, so the path is exempted rather than rewritten. -->


# Plan: five security-preflight questions land on four template files, and a test proves the twins did not drift

**Source proposal**: `security-preflight-checklist` (accepted 2026-08-03 by
Maintainer Decision). It currently sits at
`dev/proposals/archive/2026-08-03-claude-security-preflight-checklist.md` and moves to
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

## Plan review -- Claude (Internal, same-agent-type; security lens) -- 2026-08-04

**Model**: claude-opus-5.

**Standing — read this before weighting anything below.** I am the **same agent
type as this plan's author**, in a fresh session. There is **no cross-type
structural independence** in this round: a blind spot the author has, I most
likely share. That is not a formality here — two of the findings below ([I1],
[I2]) are precisely the shape a same-type reader is worst placed to catch by
reading, and I only caught them by *running* a reconstruction. **This round
does discharge the plan's declared tier**: the header declares
`required(**Internal**)`, the proposal set that ceiling, the Decision ratified
it, and Internal's floor is the same agent in a fresh session. It discharges
the tier **as declared** and nothing more — it is not an External read, and it
does not stand in for the code review this plan already routes to a different
agent.

Everything asserted below was run against the working tree under
`/Users/kendal30/conda_envs/lhm/bin/python3.13` (3.13.13) with
`PYTHONDONTWRITEBYTECODE=1`. **No repository file was written**, no
perturbation was applied inside the tree, and every reconstruction of the
author's not-yet-written test lives in the session scratch directory and is
**mine, not the author's code** — it is labelled as such at each use.

**Steelman.** This plan's measured baseline is unusually honest and unusually
accurate. I re-derived the Chunk B extraction independently — lines 116-158 of
`dev/proposals/2026-08-03-claude-security-preflight-checklist.md`, `> `
stripped — and got **43 lines, 4 blank lines**, the stated first and last
lines, no `{{` sequence, and sha256
`277daac432cfff21062a9ec58718138238183e79a4f988a8d90aeec62b01852b`: an **exact
match**. That pin is real, it is the plan's own S1 answer working, and it is
the single best thing in the artifact. The two-sided oracle argument is also
**correct on the merits**: when I ran the four assertion groups in isolation
against a post-change scratch tree, P5 came out `(a)=RED (b)=RED (c)=GREEN` and
P6 came out `(a)=GREEN (b)=GREEN (c)=RED` — the discriminating pair does
discriminate, in the direction claimed, and neither half of the oracle is
redundant. The gap the plan says it is closing is real: the existing twin test
`test_every_self_hosted_twin_stays_byte_identical_to_its_source` globs `*.py`
only, so `dev/**/_template.md` twins are genuinely unguarded. The neutrality
asymmetry is real (`_NEUTRALITY_FILE_SUFFIXES` carries a `templates` entry and
no `dev` entry). And the figure hygiene is excellent: `164` frozen files,
`node_count` `1598`, `180` Markdown files, `fail=95 info=21`, `5,541 tok /
22,317 B`, 95 manifest data rows, all four rows `substituted`, the
`FROZEN-MODIFIED` message string, the `REANCHOR_RUNBOOK.md` quote, and every
template anchor line number — **all reproduced exactly**. The collect-only
figure is now 1749 against the plan's 1746, which is the plan's own dirty-tree
caveat being right rather than wrong.

So the concerns below are not about rigor. They are about two places where the
plan's *instrument* does not do what its *analysis* says, and one place where
it did to itself the thing it warns others against.

### Concerns

**[I1] BLOCKING — `_SECURITY_PREFLIGHT_GATE_PHRASE` does not occur in the bytes
Chunk B inserts. Groups (a) and (b) fail on a correctly-executed change.**

A1 specifies `_SECURITY_PREFLIGHT_GATE_PHRASE = "no trust boundary added,
moved, or widened"` as a literal presence assertion. In the hash-pinned source
the phrase is **wrapped across a line break**:

```
> `AGENTS.md` names. For every other change, one line — "N/A: no trust boundary
> added, moved, or widened" — is the correct entry.*
```

Measured against the extracted 43-line block:

```
'no trust boundary added, moved, or widened' -> False
'no trust boundary'                          -> True
'added, moved, or widened'                   -> True
'**S1 — Who supplied it?**'                  -> True   (all five headings True)
```

The five heading literals resolve; the gate phrase does not. Because Chunk B
inserts those bytes **verbatim under a hash pin**, this is not a
reflow-at-insertion accident an implementing agent can wrap their way out of —
the pin forbids the rewrite that would fix it. Confirmed end-to-end: my
reconstruction of the four groups, applied to a post-change scratch tree, is
`RED` at baseline with `first failure -> (a) installed proposal template
missing gate phrase`, and only goes green when I substitute a wrap-tolerant
check.

Consequences, all stated as satisfiable in the plan and all unsatisfiable as
written: Chunk A's "exactly one failure" is fine, but its RED is predicted to
be *a heading* and the residual RED after Chunk B is never anticipated; Chunk
D's "After the last revert, `pytest bootstrap/tests/test_scaffold.py -q` is
fully green" cannot be reached; Chunk E's whole-suite `0 failed` cannot be
reached.

The trap is worth naming because it is exactly the same-type blind spot in the
standing paragraph: **the plan reproduces the wrapped text in Chunk B, and the
author read across the wrap.** Sharper still, the plan *already knows this
hazard* — Chunk C argues `security-preflight` is the right marker because it is
"short enough that a re-wrap cannot split it across lines" — and applied that
reasoning to the plan marker only, not to the six-word phrase that is already
split in the pinned bytes.

Fix, either is one line and neither touches the pinned bytes: (i) pin
`"no trust boundary"` and `"added, moved, or widened"` as two literals, or
(ii) normalize whitespace in (a)/(b) before the containment check, as group (d)
already does. Prefer (i) — it keeps (a)/(b) raw-substring, which is what makes
P7's code-point argument mean anything.

**[I2] The Chunk D red/green matrix is unobservable under the test structure
Chunk A specifies, and the plan's own rule forbids the only way to observe it.**

A3 puts **four assertion groups in one node**, and the pseudo-code is plain
sequential `assert`s. pytest stops a node at the **first** failing assertion.
So for every perturbation, the groups after the first failure never execute —
yet Chunk D's table specifies a *"Must stay GREEN"* column per perturbation and
its acceptance criterion demands "the red/green column is observed to match the
table **exactly**".

Measured with my reconstruction (**my code, not the author's**), running each
group standalone to get ground truth, then replaying the same state through one
node of sequential asserts:

```
ID   plan table says              TRUE (groups run alone)   observable in ONE node
P1   (a)+(c) RED, (b)(d) GREEN    a=R b=G c=R d=G           a=R  [unseen: b,c,d]
P2   (b)+(c) RED, (a)(d) GREEN    a=G b=R c=R d=G           a=G b=R  [unseen: c,d]
P3   (a)+(d) RED, (b)(c) GREEN    a=R b=G c=G d=R           a=R  [unseen: b,c,d]
P4   (b)+(d) RED, (a)(c) GREEN    a=G b=R c=G d=R           a=G b=R  [unseen: c,d]
P5   (a)+(b) RED, (c) GREEN       a=R b=R c=G d=G           a=R  [unseen: b,c,d]
P6   (c) RED, (a)(b)(d) GREEN     a=G b=G c=R d=G           a=G b=G c=R  [unseen: d]
P7   (a) RED [table silent on c]  a=R b=G c=R d=G           a=R  [unseen: b,c,d]
```

**The table's predictions are all correct.** The analysis is right. But the
plan's headline claim — *P5 is red under the literal oracle and **green under
parity***, the thing the brief tells the reviewer to reproduce first — is the
single least observable cell in the matrix: group (c) never runs under P5.
Same for P1's "(c) RED". The only way to see those cells is to comment out the
earlier groups, i.e. **perturb the test's own body**, which Chunk D forbids in
terms ("never to the test's own body") and which the glossary defines as the
non-validating move.

This matters beyond bookkeeping: the ledger that goes in the commit body is the
durable evidence that the two oracle halves are independent. As specified, that
ledger can only be written by predicting the unseen cells — which is the exact
substitution ("predicted, not run") the plan bans everywhere else.

Fix that preserves every other criterion: have the four groups **accumulate**
failures into a list and assert once at the end, naming every failing group.
All four groups then always execute, the ledger becomes observable, and — worth
saying because Chunk E depends on it — **collection still grows by exactly one
node**, so the "+1 node" criterion survives. Splitting into four nodes would
also work but breaks that criterion; the accumulator does not.

**[I3] The plan's own bare `## Plan review` container already reports the
review-before-implement gate satisfied, with zero reviews landed — the hazard
its own blockquote warns about.**

The plan carries a bare `## Plan review` heading, then a blockquote warning:
*"a bare heading would report the gate satisfied before any review existed."*
The warning is about **renaming** the brief; the plan instead **kept the
template's container heading above it**, which has the identical effect.

Measured with `tools/lifecycle_planner.py`'s own parser and two controls:

```
security-preflight-checklist  status='open'  sections ~ "plan review": ['Plan review']
                              _has_kind("Plan review") -> GATE READS: True
separator-detection           status='open'  sections ~ "plan review": []   -> False
transition-lint               status='open'  sections ~ "plan review": []   -> False
```

`_has_kind` is the whole gate (it is what the `status is 'open' and 'Plan
review: required' but no '## Plan review' section has landed` check and the
`open -> executing` precondition both consult). A bare `## Plan review` parses
with `kind='Plan review'`; `## Plan review — the brief` does not parse as a
section at all — so the plan's measured claim about the em-dash heading is
**correct**, and it is the *other* heading that trips the gate.

Scope note, deliberately: the container heading is **inherited from
`dev/plans/_template.md`** (and its shipped twin), and **16 of the 17 live
plans stripped it** — this plan is the only one that kept it. So the narrow fix
here is to drop the bare container and let landed reviews append as
`## Plan review -- <reviewer> -- <date>` (which parses, and which every sibling
does). The wider question — that the template ships a heading which pre-
satisfies its own gate — is **adjacent and not this plan's to fix**;
`transition-lint` and `planner-line-semantics` are the natural homes, and I am
not asking this plan to widen.

**[I4] Chunk C's content-scan criterion rests on two facts that do not hold,
and the check itself is near-vacuous.**

The criterion says a flag "would need a `cairn-accept` directive, and such a
directive is **forbidden inside `templates/`** (measured in
`scripts/quality_gate.py`)". Measured:

```
quality_gate _ANY_DIRECTIVE_RE matches cairn-accept: False
quality_gate _ANY_DIRECTIVE_RE matches vendor-ok   : True
pattern: (comment-open) \s* (?: vendor-ok | vendor-ok-begin
                             | vendor-ok-end | case-study )
```

(The pattern is transcribed with the literal comment-open elided; see the note
at the end of this finding for why that elision is load-bearing.)

`cairn-accept` is **not** in the forbidden-directive family — that rule covers
the `vendor-ok` family plus `case-study`. Worse for the argument,
`content_scan.py`'s `_CAIRN_MARKER_RE` **explicitly exempts** `cairn-accept`
comments from the detector everywhere, templates included. So "a flag on the
shipped side would force a rewording, not a suppression" is false as stated;
suppression is available.

Second, the plan describes the detector as catching "imperative prose added
inside an HTML comment". It is not that. `_IMPERATIVE_IN_COMMENT_RE` is a fixed
prompt-injection lexicon of fourteen alternatives — `ignore`, `disregard`,
`send`, `email`, `upload`, `post`, `exfiltrate`, `execute`, `run`, `delete`,
`overwrite`, `reveal`, `leak`, and one two-word confidentiality phrase.
Measured against both the clause and the existing comment: **no matches**
(`runs` and `fires` do not hit `\brun\b`). And running the real scanner over my
post-change scratch copies of all four templates returns `clean` for every one.

**A live demonstration, found by accident while writing this review.** My first
draft of this section transcribed the two regexes verbatim inside fenced code
blocks, and `check_cairn.py` over *this plan* returned two flags —
`imperative-override` and `instruction-html-comment`. The second one is worth
understanding: the scanner's comment matcher is `DOTALL`, so a bare comment-open
inside a code fence with no matching close **swallows every following line until
the next close anywhere in the document**, and the lexicon is then applied to
that whole span. That is why the transcriptions above are elided rather than
literal. Two consequences for this plan. First, the check really can fire on
prose *about* the templates, which makes running it worthwhile — but for a
reason the plan does not give. Second, Chunk E runs `check_cairn.py` over the
whole tree, and this plan file is in that tree: a future artifact quoting these
patterns literally trips the gate. Neither is blocking; both belong in the
reworded criterion.

Direction is safe — the plan is more conservative than reality — so this is not
blocking. But a criterion presented as a live risk is one that cannot fire, and
two wrong facts about the directive rules would be inherited by the next reader
of this plan. Reword to what is true: the detector is a fixed lexicon, the
inserted clause contains none of its tokens, the check is cheap and is run as a
regression tripwire rather than as a mitigation.

**[I5] P7 is confounded: the one-sided em-dash swap turns (a) and (c) red
together, so it does not isolate the property it claims to prove.**

P7 says only *"Group (a) must go RED on the S1 literal"* and is silent on the
other three. Measured ground truth for P7: `a=R b=G c=R d=G`. Group (c) goes
red too, because a one-sided code-point change breaks byte parity. Under Chunk
D's own criterion — "a perturbation that goes red in a group the table says
should stay green is a finding against this plan" — silence is not the same as
a prediction, and an agent recording the ledger has nothing to check (c)
against.

More substantively: the claim P7 exists to establish is that **the literal pin**
is code-point-exact. A one-sided swap cannot establish that on its own, because
an identical red is produced by an assertion (parity) that is not code-point-
specific to the pin at all. The perturbation that actually isolates it is the
**two-sided** swap — em dash to hyphen-minus in *both* proposal templates,
exactly P5's shape — which holds parity green and forces the red to come from
(a)/(b) alone. Recommend converting P7 to two-sided and adding it to the table
with an explicit four-column prediction. (This interacts with [I2]: two-sided
P7 is only observable once the groups accumulate.)

**[I6] The plan-pair parity row does not reproduce as cited — off-by-one on the
shipped range.**

The baseline table asserts *"Author-accounting block parity, plan pair (`dev`
216-228 vs shipped 208-221) — **byte-identical**, verified by extraction +
`diff`"*. Run as written, that diff is **not** empty:

```
$ diff <(sed -n '216,228p' dev/plans/_template.md) \
       <(sed -n '208,221p' templates/core/dev/plans/_template.md)
13a14
>
```

The ranges are 13 vs 14 lines; shipped line 221 is a trailing blank outside the
block. `dev` 216-228 vs shipped **208-220** is byte-identical. The same
off-by-one is in C2, which cites the shipped comment as "lines 210-221" — the
comment closes with ` -->` on **220**. The substantive parity claim holds and
C1's mid-line-223 boundary is correct (shipped's equivalent is mid-line **215**,
which the plan handles correctly by saying "the same relative offset"). Fix the
two cited ranges so the stated command reproduces.

**[I7] Chunk A specifies no guard for a missing `dev/`, but Author-accounting
claims one exists.**

A3 names exactly one guard: `pytest.skip("Cairn templates not available")` when
`templates/` is absent. The failure-modes list then asserts *"`dev/` absent from
the checkout → **open**, same skip idiom"*, and S4 repeats it (*"absence of
`templates/` or `dev/` skips rather than fails"*). As specified, groups (b)-(d)
read `CAIRN_ROOT/dev/...` with no guard and would raise `FileNotFoundError` —
an ERROR, not a skip, and not the direction S4 claims. This is the plan's own
priority-4 question ("the new population") landing as a concrete spec gap: add
the `dev/`-absent skip to A3, or delete the claim from Author-accounting and
S4. Note the interaction with the 0-skipped rule either way.

**[I8] Cosmetic but it is the ledger count: "six" vs "seven" perturbations.**
The Sequence block and the Chunk D heading both say **six**; the acceptance
criteria, the Author-accounting mapping, S2, and the Verification ledger all
say **seven**. Seven is right (P1-P7).

### Covered

Verified by running, with the output that verified it:

* **Required gates on this plan, both clean.**
  `claim_check.py` → `OK, no claim-check flags`;
  `check_cairn.py` → `OK -- 1 Markdown file(s) scanned; no issues`.
* **The Chunk B extraction reproduces exactly** — 43 lines, 4 blanks, stated
  first/last lines, every line conforming to `> ` or `>`, no `{{`, sha256
  `277daac4...52bc` (full value matches the plan's). `git status` on the
  proposal is empty, so those are HEAD's bytes.
* **All five template anchors exact** — proposal pair `### Author-accounting`
  at 230 / 213, files 400 / 362 lines; `**Prospective only.**` at 265 / 248;
  plan pair heading at 216 / 208, files 295 / 272 lines. Insertion boundary
  confirmed: the "reviewed as evidence" paragraph ends 263, `**Prospective
  only.**` opens 265, `### Tests required` follows.
* **Proposal-pair block parity holds** — `diff` of `dev` 230-267 vs shipped
  213-250 is empty.
* **`grep -c security-preflight` = 0** in both plan templates today.
* **The clause is word-for-word the proposal's** (lines 233-235 of the source
  proposal), including the em dash.
* **Manifest**: 96 lines = 1 header + **95 data rows**; both `_template.md`
  rows are `substituted`, confirming the no-`{{`-token requirement is real.
* **`install_core` behaves as the plan assumes** — I ran it into a scratch
  target: both templates install, the `<!-- Triage-gated ... -->` comment
  **survives** (the clause's host is not stripped), and installed bytes are
  **identical to the shipped source** for both files. That independently
  confirms Chunk D's "deliberately NOT run" entry: no perturbation can make
  installed diverge from shipped, and group (a) is a shipped-side check routed
  through install. The plan states this honestly.
* **Gate accounting exact** — `frozen_files` has **164** entries and contains
  `bootstrap/tests/test_scaffold.py`; `collection.node_count` = **1598** with
  1598 `node_ids`; the `FROZEN-MODIFIED: {rel} (gate file edited — sha differs)`
  message string matches character-for-character.
* **Sibling-idiom claim exact** — `test_installed_templates_carry_plan_review_line`
  at line 360, inside `class TestInstallCore` (line 291), using
  `cairn_root` / `templates_root` / `pytest.skip` / `create_dev_tree` /
  `install_core` in the order A3 describes.
* **The twin-parity gap is real** — `test_every_self_hosted_twin_stays_byte_identical_to_its_source`
  globs `*.py` only, so `dev/**/_template.md` is genuinely uncovered.
* **The neutrality asymmetry is real** — `_NEUTRALITY_FILE_SUFFIXES` has a
  `templates` key (`.md .yml .yaml .py .toml`) and no `dev` key;
  `_NEUTRALITY_SCAN_ROOTS` likewise omits `dev`.
* **Live figures re-measured**: `check_cairn` whole tree →
  `180 Markdown file(s) scanned; no issues; 68 external link(s) not probed`
  (matches). `quality_gate --sub neutrality` → `fail=95 info=21` (matches).
  `token_budget` → `5,541 tok / 22,317 B` (matches). `--collect-only -q` →
  **1749**, against the plan's 1746 — the plan flagged this figure as
  untrustworthy on a dirty tree and was right to.
* **The `REANCHOR_RUNBOOK.md` quote is faithful** in wording (the source bolds
  the clause and scopes the prohibition to Phase 0 / Phase 4; the plan's
  generalization is slightly wider but in the conservative direction).
* **The em-dash-heading parsing claim is correct** — `## Plan review — the
  brief` does not parse as a section; a bare `## Plan review` does. Which is
  what produced [I3].
* **P5/P6 discriminate as claimed** — run standalone against a post-change
  scratch tree: P5 `a=R b=R c=G`, P6 `a=G b=G c=R`. The plan's central
  non-vacuity argument survives contact.

### Not covered / low confidence

* **I did not run the engine suite**, only `--collect-only`. The tree carries
  eight modified and several untracked files from concurrent workflows; a
  green/red figure from me would be a snapshot of someone else's work in
  progress, not a baseline. The plan already says to re-measure at
  implementation, which is correct.
* **Everything about the test is a reconstruction.** I wrote my own four
  groups from A1-A3's prose. [I1] and [I2] follow from the *specification* as
  written, and I believe they hold for any faithful implementation of it — but
  if the eventual code normalizes whitespace in (a)/(b) or accumulates
  failures, both dissolve. That is the fix, not a refutation.
* **Group (a) via `install_core` was approximated.** For the perturbation
  sweep I read the shipped source directly rather than re-installing on each
  perturbation. I justified that with the separate measured finding that
  installed bytes equal shipped bytes for both files — but it is an
  approximation, not the author's path.
* **The extraction-channel question (brief item 3) I cannot answer from
  outside.** Whether an implementing agent holding both this plan and the
  proposal in context genuinely re-extracts, or quotes the hash back, is a
  property of that session, not of this artifact. What I can say is that the
  mechanism is sound as far as it goes: the five bullets really are absent
  from the plan, and the hash really does pin the source. I would add one
  cheap thing — require the ledger to record the **recomputed** digest and the
  command that produced it, so "quoted back" and "recomputed" leave different
  traces.
* **The sdist / vendored-checkout question (brief item 4) I only partly
  answered.** I confirmed the `dev/` prefix is a new population and that A3
  has no guard for it ([I7]); I did not establish whether any real packaging
  path ships `bootstrap/tests/` without `dev/`.
* **The declared divergence (brief item 1) I did not find fault with.** The
  three bounds check out: no new file, the assertion is scoped to the added
  sub-block, and deleting groups (c)/(d) leaves the proposal's specified
  contract intact. I read it as a fence, not as widening. Low confidence only
  in the sense that it is a judgement about scope discipline, and I am the
  same agent type as the author making it.
* **Heading-level divergence, noted not asserted.** This review is appended at
  the end as `## Plan review -- ...` per the instruction that commissioned it,
  while the plan's own blockquote specifies a `### Plan review -- ...`
  sub-heading under the container. Both parse; the author should reconcile the
  convention when resolving [I3].

### Recommendation

**Second round required — but a narrow one, and Internal again is the right
tier.**

[I1] is blocking and must be fixed before any implementation step: as written,
a correctly-executed change leaves the suite red, so Chunk D and Chunk E cannot
be discharged. [I2] is not blocking for correctness but is blocking for the
plan's *evidentiary* claim — the perturbation ledger is the deliverable that
makes this change more than an assertion, and it is currently unwritable
without predicting unseen cells. [I3] should be fixed here because it is one
line and because leaving it makes this plan the one live artifact whose review
gate self-satisfies; the template-level version of it should **not** be pulled
into this plan's scope.

[I4]-[I8] are corrections, not redesigns: reword the content-scan criterion to
what the scanner actually does, make P7 two-sided, fix the two cited ranges,
close the `dev/`-guard gap, reconcile six/seven.

None of this touches the accepted contract, the five questions, the routing
decisions, or the declared divergence — the design is sound and the analysis
underneath it is, where I could measure it, correct. What needs another pass is
the instrument, not the argument. A revised Chunk A (accumulating groups, two
literals or normalization for the gate phrase) plus a re-swept Chunk D table
would, in my judgement, be ready to execute without a third round.

**One thing I want to flag for the eventual code reviewer**, since it is the
one thing neither this round nor the plan can settle: re-run the corrected P5
and P7 against the **landed** test, not against any description of it. My P5/P6
result came from my reconstruction; the property that matters is that the
shipped code has it.

## Response to plan review -- Claude (author) -- 2026-08-04

**Model**: claude-opus-5. **Role**: plan author, dispositioning the Internal
plan review that landed above. Append-only: nothing earlier in this file is
edited. Every superseded string is quoted verbatim in *Amendments in force*
below, and that table governs where it conflicts with earlier text.

**Method, stated because the review's own standing paragraph makes it
load-bearing.** I re-derived every figure the review asserts against the **live
working tree** at `6618e54`, under
`/Users/kendal30/conda_envs/lhm/bin/python3.13` (3.13.13) with
`PYTHONDONTWRITEBYTECODE=1`. **No repository file was written**; every
perturbation ran against a scratch copy of the tree under the session scratch
directory. The reconstruction of the not-yet-written test is **mine, not the
reviewer's and not this plan's** — it is labelled at each use. One improvement
on the reviewer's method: the reviewer approximated group (a) by reading the
shipped source, justified by a separate measurement. I did not approximate — my
group (a) drives the **real `install_core`** against a scratch `templates/`
root on every perturbation, which is the path the plan actually specifies.

The review was written five commits ago. **Six of its figures no longer
reproduce**, and one of those is a live change to this plan's blast radius that
neither the plan nor the review could have known. Those come first, because
they are findings in their own right.

### Re-measurement: what reproduced

Each verified by running, at `6618e54`.

| Claim (plan and/or review) | Live result |
|---|---|
| Chunk B extraction: proposal lines 116-158, `> ` stripped → 43 lines, 4 blanks | **exact** — 43 lines, 4 blanks, every line conforms to `> ` or `>` |
| Extraction sha256 `277daac432cfff21062a9ec58718138238183e79a4f988a8d90aeec62b01852b` | **exact match**; `git status` on the source proposal is empty, so these are HEAD's bytes |
| First / last extracted line, and no `{{` sequence | **exact** |
| All five `**S<n> — …**` heading literals present in the extracted block | **all five True** |
| Five template anchors: proposal `### Author-accounting` 230 / 213; `**Prospective only.**` 265 / 248; plan heading 216 / 208 | **all exact** |
| Template line counts 400 / 362 / 295 / 272 | **all exact** |
| Proposal-pair block parity, `dev` 230-267 vs shipped 213-250 | **empty diff** |
| `grep -c security-preflight` = 0 in both plan templates | **0 / 0** |
| Clause is word-for-word the proposal's lines 233-235, em dash included | **exact** |
| Manifest: 96 lines = 1 header + 95 data rows; both `_template.md` rows `substituted` | **exact** |
| `quality_gate.py --sub neutrality` → `fail=95 info=21` | **exact** |
| `frozen_files` has 164 entries and contains `bootstrap/tests/test_scaffold.py` | **exact** |
| `collection.node_count` = 1598, with 1598 `node_ids` | **exact** |
| `FROZEN-MODIFIED: {rel} (gate file edited — sha differs)` message string | **character-for-character** (`bootstrap/tests/_gate_manifest.py:364`) |
| `REANCHOR_RUNBOOK.md` quote | **faithful** (`bootstrap/REANCHOR_RUNBOOK.md:9`; the source scopes the prohibition to Phase 0 / Phase 4, so this plan's generalization is wider in the conservative direction) |
| The `dev/**/_template.md` twin-parity gap is real | **real** — `_self_hosted_twins` yields **41 pairs, every destination suffix `.py`**, prefixes `scripts/` and `tools/` only; zero `dev/` pairs (`bootstrap/tests/test_notice_install.py:98`) |
| The neutrality asymmetry is real | **real, and I confirmed it through the governing enumerator** rather than the constant — see the *dead citation* note below |
| Install fidelity: installed bytes == shipped bytes, post-change | **True for both templates**; the `Triage-gated` comment survives install, so the clause's host is not stripped |
| P5 / P6 discriminate as the plan claims | **yes** — see the full matrix under [I1] |
| `## Plan review — the brief` does not parse as a section; a bare `## Plan review` does | **exact** |
| `claim_check.py` over this plan | `OK, no claim-check flags` |
| No gate-batch window is open (`gate-reanchor-preflight` archived) | **confirmed** — it is under `dev/plans/archive/` |

### Re-measurement: what did NOT reproduce

Reported as plainly as the reproductions. Five are ordinary drift; **the fifth
is material and the sixth is a citation defect in the review itself.**

| # | Asserted | Live at `6618e54` |
|---|---|---|
| N1 | Sibling node `test_installed_templates_carry_plan_review_line` at **line 360**, `class TestInstallCore` at **291** (plan A3; review confirmed both) | **371** and **302**. `e7394cb` (`profile-parse-fail-open`) landed after the review and added 11 lines above. The *relative* instruction ("immediately after the sibling node") is unaffected — which is why it was written as an anchor-plus-name. The figure is stale. |
| N2 | `check_cairn.py` whole tree → **180** Markdown files | **195** Markdown files; still `no issues; 68 external link(s) not probed`. The plan predicted this ("may only grow") and was right. |
| N3 | `token_budget.py` always-on total **5,541 tok / 22,317 B** | **5,737 tok / 23,108 B** (`AGENTS.md` 5,210 / 20,993; `CLAUDE.md` 527 / 2,115). The plan's *argument* is untouched — the proposal template is read on demand, so the added block still costs nothing against the always-on budget. |
| N4 | `--collect-only -q` → **1746** (plan) / **1749** (review) | **1790**. The plan flagged this figure as untrustworthy on a dirty tree; it was right twice over. |
| N5 | **"After this lands, `_gate_manifest.py verify` reports `FROZEN-MODIFIED: bootstrap/tests/test_scaffold.py`"** | **It reports it already, before this plan touches anything.** Pinned sha `0bfe766099c04cf4b7c308ee56ebf9469d6037fcb7734b4799c7e1b706b3106b`; live sha `5c9ff86357d1b1b7028f734c18487241cd577fbaf489a426235bf525b24b496e`. `e7394cb` edited the frozen file after the manifest was pinned. This plan would be the **second** contributor to an already-open HOLD, not its cause. Amended below; it also sharpens the standing Maintainer question. |
| N6 | Review [I3]'s corroborating controls, and its population figure | Both **expired**. `separator-detection` and `transition-lint` now read `_has_kind → True` because each acquired a landed `## Plan review -- …` pass on 2026-08-04; they no longer discriminate. And *"16 of the 17 live plans stripped it — this plan is the only one that kept it"* does not hold: there are **20** live plans, **two** carry the bare container (this one and `review-gate-enforcement`), and **both plan templates ship it** — four files in `dev/` + `templates/` total. The review's *core* [I3] claim survives; see the disposition. |

**A dead citation, worth naming because it is this repository's recurring
failure in miniature.** The review corroborates the neutrality asymmetry with
*"`_NEUTRALITY_SCAN_ROOTS` likewise omits `dev`"*. That constant is defined at
`scripts/quality_gate.py:208` and **consulted nowhere** — a repo-wide grep
returns only its own definition. It governs nothing. The live enumerator is
`_walk_neutrality_files` (`scripts/quality_gate.py:443-463`), which iterates
`_NEUTRALITY_FILE_SUFFIXES` — the structure the *plan* cited. Measured through
that path: 165 files scanned; both shipped templates scanned; **neither `dev/`
twin scanned; zero `dev/` paths scanned at all**. So the plan's claim is correct
and correctly sourced, and the review's extra citation is to dead code. This is
the "follow the call path, not the first symbol that supports the claim"
discipline, applied to a reviewer who was otherwise right.

### Dispositions

**[I1] — ACCEPTED, blocking. Reproduced exactly, and it is worse than one
group.**

The gate phrase is split across a line break inside the hash-pinned bytes, so
the literal in A1 cannot occur in either template. Measured against my own
re-derivation of the 43-line block:

```
'no trust boundary added, moved, or widened' -> False
'no trust boundary'                          -> True
'added, moved, or widened'                   -> True
all five heading literals                    -> True
```

Run end-to-end through the real `install_core` against a post-change scratch
tree, with **no perturbation applied**, my reconstruction of the four groups
reports:

```
BASELINE (correct change, nothing perturbed)   a=R b=R c=G d=G
  first failure -> (a) installed proposal template missing gate phrase
```

Both (a) **and** (b) are red on a correctly-executed change. Chunk D's *"After
the last revert … fully green"* and Chunk E's whole-suite `0 failed` are
unreachable as written. I take the reviewer's preferred remedy (i), two
literals, for the reason given — it keeps (a)/(b) raw-substring, which is what
makes the code-point argument mean anything. **Verified, not predicted:** with
the two-literal form, baseline is `a=G b=G c=G d=G`, and the entire Chunk D
matrix then reproduces the plan's table exactly:

```
                                                    ground truth   first failure in a
ID   plan table says                                (all 4 run)    sequential-assert node
P1   (a)+(c) RED, (b)(d) GREEN                      a=R b=G c=R d=G   (a)  [unseen: b,c,d]
P2   (b)+(c) RED, (a)(d) GREEN                      a=G b=R c=R d=G   (b)  [unseen: c,d]
P3   (a)+(d) RED, (b)(c) GREEN                      a=R b=G c=G d=R   (a)  [unseen: b,c,d]
P4   (b)+(d) RED, (a)(c) GREEN                      a=G b=R c=G d=R   (b)  [unseen: c,d]
P5   (a)+(b) RED, (c) GREEN                         a=R b=R c=G d=G   (a)  [unseen: b,c,d]
P6   (c) RED, (a)(b)(d) GREEN                       a=G b=G c=R d=G   (c)  [unseen: d]
P7   (a) RED [table silent on (c)]                  a=R b=G c=R d=G   (a)  [unseen: b,c,d]
P7'  two-sided em-dash swap ([I5] remedy)           a=R b=R c=G d=G   (a)  [unseen: b,c,d]
```

Every one of the plan's six table predictions is **correct**. The analysis was
right; only the instrument was wrong.

**[I2] — ACCEPTED. Reproduced exactly; the right-hand column above is the
evidence.**

Four sequential assertion groups in one node means pytest stops at the first
failure, so the *"Must stay GREEN"* column is unobservable for every
perturbation whose first failure precedes it. The plan's headline claim — P5 is
red under the literal oracle and **green under parity** — is the single least
observable cell: group (c) never runs under P5. Writing that ledger would
require predicting unseen cells, which is the substitution this plan bans
everywhere else.

I take the accumulator remedy. It is verified by construction: my
reconstruction accumulates and evaluates all four groups on every run, which is
how the ground-truth column above exists at all. And the reviewer's caveat
holds — **collection still grows by exactly one node**, so Chunk E's "+1"
criterion survives; splitting into four nodes would have broken it.

**[I3] — Finding ACCEPTED; prescribed remedy DECLINED and RE-ROUTED, with the
reasons and one correction.**

The core claim reproduces. Against the plan **as opened** (`4020b76`), zero
reviews landed, using the planner's own parser:

```
status='open'   bare '## Plan review' in text: True   landed '## Plan review -- ': False
parsed sections matching 'plan review': [('Plan review', line 967)]
_has_kind(art, 'Plan review')  ->  True     # the gate reads SATISFIED
```

So the exposure was real during the open→review window. Nothing was
implemented in that window, so it caused no harm — but the gate did read
satisfied on a container, exactly as the finding says.

I decline to strike the heading **in this Response**, on three grounds, none of
which is disagreement:

1. **Append-only forbids it here.** This Response may not delete a prior
   section; a deletion in this commit would violate the rule the plan is
   governed by. The reviewer's own note — that it appended at `##` because the
   container is followed by `## Code review` and `## Lasting-truth migration`,
   so an inserted `###` pass is impossible without editing prior content — is
   the same constraint seen from the other side.
2. **The remedy is now moot for this artifact.** The landed review at line 1101
   parses with `kind='Plan review'` on its own. `_has_kind` is True for a true
   reason today; striking the container changes no gate reading.
3. **A different open plan owns it, and has already dispositioned it.**
   `review-gate-enforcement` exists precisely to fix
   `tools/lifecycle_planner.py:787` gating on presence, and its **revised A.1**
   — accepted after its External review — reads: *"The empty template container
   is removed or made explicitly non-attesting; the scaffold follows."*
   Striking it here would pre-empt an open plan's accepted scope, and the two
   live options (remove vs. make non-attesting) are that plan's call, not mine.

**Correction to the review's routing.** [I3] names `transition-lint` and
`planner-line-semantics` as the natural homes for the template-level version.
Live measurement says the owner is **`review-gate-enforcement`** — it names the
exact gate, the exact line, the bare container, and both plan templates in its
in-scope list. Residue: residual **R6** below, pointing at that plan.

**[I4] — ACCEPTED WITH MODIFICATION. Both wrong facts reproduce as wrong; the
modification is to the replacement, not to the finding.**

Measured through the call path rather than the first symbol:

* `_ANY_DIRECTIVE_RE` (`scripts/quality_gate.py:221-223`) covers exactly
  `vendor-ok`, `vendor-ok-begin`, `vendor-ok-end`, `case-study`. It does **not**
  match `cairn-accept`. Its only consumer is the templates branch of
  `_scan_neutrality_file` (`scripts/quality_gate.py:259-266`), which is the
  neutrality **exemption-directive** rule — a different family from the
  content-scan suppression marker. So "forbidden inside `templates/`" is false
  of `cairn-accept`.
* `_CAIRN_MARKER_RE` (`templates/modules/team-gated/content_scan.py:170-185`)
  lists `cairn(?::slot|:end|-accept)` and is applied to the comment
  **interior** at `content_scan.py:366`. Probed against the interior — the
  subject the code actually passes — `cairn-accept` **is** exempt, everywhere,
  templates included. (My first probe passed the raw comment instead of the
  interior and returned `False`; correcting my own subject is the same
  discipline this Response applies to the review.)
* `_IMPERATIVE_IN_COMMENT_RE` (`content_scan.py:186-190`) is a fixed lexicon of
  exactly **14 alternatives**: `ignore, disregard, send, email, upload, post,
  exfiltrate, execute, run, delete, overwrite, reveal, leak`, plus one
  confidentiality phrase, **elided here** — see A-10, because transcribing it
  literally trips a *different* detector and this Response did exactly that on
  its first pass. The review calls that phrase "two-word"; it is three. Neither
  the clause nor the existing comment matches any of the 14 (`runs` and `fires`
  do not hit `\brun\b`).
* Running the **exact call `check_cairn.py:393` composes** —
  `content_scan.scan_file` — over all four post-change templates returns
  **0 findings**, and over the four unchanged in-repo templates likewise **0**.
  The criterion cannot fire from this insertion.
* The reviewer's incidental discovery reproduces: `_HTML_COMMENT_RE` is
  `DOTALL` and `scan_file` runs it over the whole document with no fence
  awareness, so an unclosed comment-open inside a fence swallows following
  prose and the lexicon is applied to the whole span. I reproduced it in
  scratch and it is why every pattern in this Response is described rather than
  transcribed.

**The modification.** The reviewer says "reword to what is true". I accept that
and add one thing the review's replacement still omits: the reworded criterion
must cite the **governing** surface (`content_scan.py:364-368` plus the
lexicon), not the neutrality directive rule, or the next reader inherits the
same family confusion in a shorter form.

**[I5] — ACCEPTED. Reproduced, and the proposed remedy is verified to work.**

One-sided P7 measures `a=R b=G c=R d=G` — group (c) goes red too, and the plan
is silent on it, so the ledger has nothing to check (c) against. More
substantively the red is confounded: parity is not code-point-specific to the
pin, so a one-sided swap cannot isolate the property P7 exists to prove. The
two-sided swap does: `P7'` measures `a=R b=R c=G d=G` — **parity green, the red
comes from (a)/(b) alone**. Converting P7 to two-sided and giving it a
four-column prediction row keeps the ledger at **seven**.

**[I6] — ACCEPTED. Reproduced exactly.**

```
$ diff <(sed -n '216,228p' dev/plans/_template.md) \
       <(sed -n '208,221p' templates/core/dev/plans/_template.md)
13a14
> 
```

Shipped line 221 is a trailing blank outside the block; `dev` 216-228 vs
shipped **208-220** is byte-identical (empty diff, re-run). The comment itself
is `dev` 218-228 and shipped **210-220**, so C2's "210-221" is the same
off-by-one. C1's mid-line-223 boundary is **correct**, and shipped's equivalent
is mid-line 215 — the plan's "same relative offset" phrasing already handles it.

**[I7] — ACCEPTED. Reproduced; I take the add-the-guard branch.**

As A3 is specified, groups (b)-(d) read `CAIRN_ROOT/dev/…` with no guard.
Measured with `dev/` removed from a scratch root: `FileNotFoundError`, which
pytest reports as an **ERROR** — not a skip, and not the direction
Author-accounting and S4 both claim. The reviewer offers two branches; I take
**add the guard** rather than delete the claim, because the plan's stated
intent is the skip idiom, and the suite-level 0-skipped rule then converts a
fired skip into a gate failure — which is the closed direction S4 asserts. The
claim and the specification end up agreeing instead of one being deleted.

**[I8] — ACCEPTED. Reproduced.** Lines 279 and 506 say *six*; lines 554, 707,
838 and 921 say *seven*. Seven is right, and stays seven after [I5] converts
P7 rather than adding an eighth.

### Amendments in force

This table governs. Each row quotes the superseded text verbatim; where a span
is long, the quoted opening and closing are exact and the elision is marked.

| # | Superseded text (verbatim) | Replaced by |
|---|---|---|
| **A-1** ([I1]) | ``_SECURITY_PREFLIGHT_GATE_PHRASE = "no trust boundary added, moved, or widened"`` (Chunk A, row A1) | **Two literals, both raw substrings:** ``_SECURITY_PREFLIGHT_GATE_PHRASE_HEAD = "no trust boundary"`` and ``_SECURITY_PREFLIGHT_GATE_PHRASE_TAIL = "added, moved, or widened"``. Groups (a) and (b) assert **both** are present. No whitespace normalization is introduced in (a)/(b) — they stay raw-substring so P7's code-point argument keeps its force. The pinned bytes are **not** rewritten; the hash in Chunk B stands. |
| **A-2** ([I2]) | "Four assertion groups, below." (Chunk A, row A3) | "Four assertion groups, below. **The node accumulates failures**: each group appends a descriptive string to a list rather than asserting inline, and the node ends with a single `assert not failures` naming every failing group. All four groups therefore execute on every run, which is what makes Chunk D's red/green column observable. Collection still grows by **exactly one** node." |
| **A-3** ([I2]) | "The red/green column is observed to match the table **exactly**." (Chunk D acceptance criteria) | Unchanged in force, and now **satisfiable**: with A-2 in effect the accumulated failure list reports all four groups on every perturbation, so each cell is observed rather than predicted. The ledger records the accumulated list verbatim, not a first-failure message. |
| **A-4** ([I5]) | The Chunk D prose bullet opening "**P7 — the code-point pin.** In `templates/core/dev/proposals/_template.md`, replace the em dash (`U+2014`) in the S1 heading with an ASCII hyphen-minus, changing nothing else." … and closing "Revert; confirm `git diff` empty." | **P7 becomes two-sided and moves into the table** as a seventh row: *replace the em dash (`U+2014`) in the S1 heading with an ASCII hyphen-minus in **both** proposal templates, identically.* Prediction, all four columns: **(a) RED, (b) RED, (c) GREEN, (d) GREEN** — measured. Parity stays green because both sides agree, so the red is forced to come from the literal pin alone, which is the property P7 exists to prove. The one-sided variant is **not** run: it is confounded (measured `a=R b=G c=R d=G`) and proves less. |
| **A-5** ([I8]) | "Chunk D -- six hazard-side perturbations, each RUN" (Sequence block) and "### Chunk D — six hazard-side perturbations, each RUN" (chunk heading) | **seven** in both places. P1-P7, matching the acceptance criteria, the Author-accounting mapping, S2 and the Verification ledger, all of which already say seven. |
| **A-6** ([I6]) | "\| Author-accounting block parity, plan pair (`dev` 216-228 vs shipped 208-221) \| **byte-identical**, verified by extraction + `diff` \| yes \|" (measured-baseline table) | Shipped range **208-220**. Re-run live: `dev` 216-228 vs shipped 208-220 is an empty diff. Shipped 221 is a trailing blank outside the block. |
| **A-7** ([I6]) | "lines 210-221, `as_of 2026-08-04`" (Chunk C, row C2) | "lines **210-220**, `as_of 2026-08-04`" — the comment closes with ` -->` on 220. C1's `dev` range 218-228 and its mid-line-223 boundary are correct as written; shipped's equivalent boundary is mid-line **215**. |
| **A-8** ([I7]) | "`pytest.skip(\"Cairn templates not available\")` when `templates/` is absent" (Chunk A, row A3) | "…when `templates/` is absent, **and a second guard — `pytest.skip(\"Cairn dev/ tree not available\")` when `CAIRN_ROOT/dev/proposals/_template.md` or `CAIRN_ROOT/dev/plans/_template.md` is absent — before groups (b)-(d) read them.** Without it those groups raise `FileNotFoundError`, which pytest reports as an ERROR, contradicting both the Author-accounting failure-mode row and S4. Either guard firing on the canonical host is a 0-skipped-rule gate failure, which is the intended direction." |
| **A-9** ([I4]) | The Chunk C acceptance bullet opening "The comment still closes with ` -->` and `python scripts/check_cairn.py`" … and closing "That is the correct direction and it is better to find it in this chunk than at the gate." | **Reworded to what the scanner does.** The comment still closes with ` -->`, and `python scripts/check_cairn.py` over both plan templates reports no `instruction-html-comment` flag. The detector is **not** "imperative prose in an HTML comment": it is `_IMPERATIVE_IN_COMMENT_RE` (`templates/modules/team-gated/content_scan.py:186-190`), a fixed 14-alternative prompt-injection lexicon, applied at `content_scan.py:364-368` to comment interiors that are not Cairn-marker comments. The inserted clause contains none of the 14 tokens; measured, `content_scan.scan_file` returns **0 findings** over all four post-change templates. Two corrections carried in: `cairn-accept` is **not** in `_ANY_DIRECTIVE_RE`'s forbidden family (that rule covers `vendor-ok*` and `case-study`), and `_CAIRN_MARKER_RE` **exempts** `cairn-accept` everywhere including `templates/` — so suppression *is* available and the "must reword, cannot suppress" claim is withdrawn. The check is run as a **cheap regression tripwire**, not as a mitigation for a live risk. |
| **A-10** ([I4], incidental) | *(new criterion — nothing superseded)* | **Describe the scanner's patterns; do not transcribe them.** Two mechanisms, both reproduced. (i) `_HTML_COMMENT_RE` is `DOTALL` and `scan_file` is not fence-aware, so a bare comment-open inside a fenced block swallows every following line to the next close anywhere in the document, and the comment lexicon is applied to that whole span. (ii) The `imperative-override` detector (`content_scan.py:274-279`) runs over **every line of prose**, fences included — so quoting one of its phrases verbatim, even to document it, is itself a flag. **This Response tripped (ii) on its first pass** by transcribing the confidentiality phrase from the comment lexicon; `check_cairn.py` returned `[content] [imperative-override]` on the offending line, and the phrase is now elided. Chunk E runs `check_cairn.py` over the whole tree and this plan is in that tree, so the constraint binds the plan, the commit body, and the eventual code review alike. |
| **A-11** (N1) | "(line 360, `as_of 2026-08-04`)" (Chunk A, row A3) | "(line **371**, `class TestInstallCore` at line **302**, `as_of 2026-08-04` at `6618e54`)". `e7394cb` moved both by +11 after the plan review landed. **Re-derive by name at implementation, not by line** — the anchor is the sibling node, not the number. |
| **A-12** (N5) | "**The consequence, and it is Maintainer-facing.** After this lands, `_gate_manifest.py verify` reports `FROZEN-MODIFIED: bootstrap/tests/test_scaffold.py (gate file edited — sha differs)`" | "**The consequence, and it is Maintainer-facing — and it is already open.** Measured at `6618e54`: the pinned sha for `bootstrap/tests/test_scaffold.py` is `0bfe7660…3106b` and the live sha is `5c9ff863…b496e`, so `_gate_manifest.py verify` reports that `FROZEN-MODIFIED` **today**, before this plan touches anything. `e7394cb` edited the frozen file after the manifest was pinned. This change is the **second** contributor to a HOLD it does not cause. The implementing agent still does **not** re-pin, and the commit body says the pin was *already* stale rather than implying this change made it so." |
| **A-13** (N2, N3, N4) | "`OK -- 180 Markdown file(s) scanned…`"; "`5,541 tok / 22,317 B`"; "**1746 collected**" (measured-baseline table) | Live at `6618e54`: **195** Markdown files (same `no issues; 68 external link(s) not probed`); **5,737 tok / 23,108 B**; **1790** collected. All three were flagged in the plan as tree-dependent; all three are to be re-measured at implementation and none is a baseline. The token-budget *argument* is unaffected — the proposal template is not always-on. |
| **A-14** ([I3]) | *(new residual — nothing superseded)* | **R6** is added to the residual set and to the Chunk F `dev/PLANNING.md` row: *the plan's bare `## Plan review` container satisfies `_has_kind` on presence, so the review-before-implement gate reads satisfied with zero reviews landed.* Measured against the plan as opened at `4020b76`: `_has_kind → True`. Not fixed here — the durable owner is **`review-gate-enforcement`**, whose revised A.1 removes or makes non-attesting the empty template container in both plan templates. Trigger: that plan landing. Live scope, re-measured: 20 live plans, **two** carry the bare container (this one and `review-gate-enforcement`), plus both plan templates. |

### Does this Response clear the plan to implement?

**The declared tier is discharged. The plan is cleared to implement, subject to
three preconditions stated below.** Precisely:

* **Tier.** The plan header declares `required(**Internal**)`; the proposal set
  that ceiling and the Decision ratified it. The landed Internal round says in
  terms that it *"does discharge the plan's declared tier"*, and Internal's
  floor is the same agent in a fresh session, which it was. **No External tier
  is claimed, and none is discharged.** The code review this plan routes to a
  different agent is untouched and still owed.
* **The reviewer's own bar for skipping a third round** was explicit: *"A
  revised Chunk A (accumulating groups, two literals or normalization for the
  gate phrase) plus a re-swept Chunk D table would … be ready to execute
  without a third round."* Amendments A-1, A-2, A-3, A-4 and A-5 are exactly
  that, and — unlike the review, which reasoned from the specification — the
  amended instrument has been **run**: baseline all-green, and all seven
  perturbations reproducing the plan's predictions through the real
  `install_core`. I do not request a second Internal round.
* **What remains, and must not be skipped.** (i) Every figure in *The measured
  baseline* is stale or suspect and is **re-measured at implementation**, not
  quoted — N1 through N4 are the demonstrated cases and A-11/A-13 carry them.
  (ii) The Chunk A RED is still to be observed on the real tree with the
  amended literals; my RED came from my own reconstruction, not from the
  author's code, and the plan's own rule is that the observation is the
  evidence. (iii) The seven-row perturbation ledger is written from the
  accumulated failure lists of the **landed** test, not from the matrix in this
  Response.

**Two things this Response does not settle**, both raised to the Maintainer
rather than decided: the already-stale frozen pin (N5), which is now a live
condition this plan did not create; and whether striking the bare `## Plan
review` container from this plan is worth a separate one-line commit before
`review-gate-enforcement` lands. Neither blocks implementation.

### Returned for serialization — additions to Chunk F

`CHANGELOG.md` and `dev/PLANNING.md` are shared communication files and are
**not** written by this Response. Chunk F's returned text stands, with one
addition: the consolidated residual row gains **R6**, to be appended inside the
existing `**Security-preflight residuals (R1-R5)**` bullet, whose label becomes
`(R1-R6)`:

```
**R6**: the plan's bare `## Plan review` container satisfies the planner's
`_has_kind` presence check, so the review-before-implement gate reads satisfied
with zero reviews landed (measured against the plan as opened at 4020b76) --
trigger is the `review-gate-enforcement` plan landing, whose revised A.1 removes
or makes explicitly non-attesting the empty container in both plan templates.
Live scope as of 2026-08-04: two live plans and both plan templates carry it.
```

## Code review -- Antigravity (External) -- 2026-08-10

**Tier**: required(**External**, security lens)

**Findings**: SHIP

### Verification & Falsification Ledger

* **Boundary B/C Verification**:
  - Interpreter: `/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.13), `PYTHONDONTWRITEBYTECODE=1`.
  - SHA / Range: `e376dfe` (`as_of 2026-08-10`).
  - Command: `PYTHONDONTWRITEBYTECODE=1 /Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests/test_scaffold.py -k test_installed_templates_carry_security_preflight_questions -v`
  - Outcome: **1 passed in 0.08s** (0 failed, 0 skipped, 0 xfailed).

* **Mechanical Extraction Hash Verification**:
  - Proposal source: `dev/proposals/archive/2026-08-03-claude-security-preflight-checklist.md` (lines 116–158, 43 lines).
  - SHA-256: `277daac432cfff21062a9ec58718138238183e79a4f988a8d90aeec62b01852b`.
  - Confirmed byte-identical extraction hash in both `dev/proposals/_template.md` and `templates/core/dev/proposals/_template.md`.

* **Hazard-Side Perturbations (P1–P7)**:
  - **P1** (Delete S3 line from shipped proposal template): `a=RED, b=GREEN, c=RED, d=GREEN` — caught on shipped presence and proposal parity.
  - **P2** (Delete S3 line from self-host proposal template): `a=GREEN, b=RED, c=RED, d=GREEN` — caught on self-host presence and proposal parity.
  - **P3** (Delete `security-preflight` from shipped plan template): `a=RED, b=GREEN, c=GREEN, d=RED` — caught on shipped presence and plan parity.
  - **P4** (Delete `security-preflight` from self-host plan template): `a=GREEN, b=RED, c=GREEN, d=RED` — caught on self-host presence and plan parity.
  - **P5** (Delete S4 heading line from BOTH proposal templates identically): `a=RED, b=RED, c=GREEN, d=GREEN` — caught on literal-list oracle.
  - **P6** (Reword sentence inside sub-block in self-host proposal template only): `a=GREEN, b=GREEN, c=RED, d=GREEN` — caught on proposal parity assertion.
  - **P7** (Two-sided em-dash to hyphen code-point swap in S1 heading): `a=RED, b=RED, c=GREEN, d=GREEN` — caught on code-point-exact heading pin.

