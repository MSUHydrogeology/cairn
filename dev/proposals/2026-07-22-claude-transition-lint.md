<!-- The paths below appear inside the appended Internal review: illustrative/deliberately-absent example paths, adopter-tree install destinations quoted from a manifest row, and multi-part line citations on real files. Marked, not edited -- reviewer prose is append-only. -->
<!-- claim-check-allow: dev/plans/a-thing.md*, docs/tool-usage.md* -->
<!-- cairn-internal-ref-allow: doctrine/lifecycle.md doctrine/proposals.md doctrine/rationale.md doctrine/coordination.md doctrine/consolidation-review.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
<!-- Forward-reference paths this proposal plans to create; they materialize in the implementing plan. -->
<!-- claim-check-allow: scripts/transition_lint.py, scripts/transition_lint_whitelist.py, bootstrap/tests/test_transition_lint.py, dev/plans/transition-lint.md -->

# The transition-lint: an advisory check that a commit's message matches its lifecycle diff

**Author**: Claude (Strategy)
**Model**: Claude Opus 4.8
**Date opened**: 2026-07-22
**Status**: proposed
**Touches**: a new advisory check `scripts/transition_lint.py` + its suppression whitelist `scripts/transition_lint_whitelist.py`; a new behavioral test `bootstrap/tests/test_transition_lint.py`; a new `docs/tool-usage.md` section; `CHANGELOG.md` at finalization; the deferred row at `dev/PLANNING.md:129` moves at plan-open. **No doctrine, no `AGENTS.md`, no shipped template, no install-manifest entry.**
**Related**: split out of the accepted `2026-07-08-claude-review-record-integrity` (its Part C), per that proposal's Internal-review findings R2, R3, R4, R9 and R10 (`dev/proposals/archive/2026-07-08-claude-review-record-integrity.md:291-321` and `:362-378`) and the author Response that carried them forward as pre-registered constraints (`dev/proposals/archive/2026-07-08-claude-review-record-integrity.md:434-481`); the broad-look review's fold-up candidate at `dev/strategy/2026-07-08-claude-broad-look-skeptical-review.md:673-676`; the deferred roadmap row at `dev/PLANNING.md:129`; the incident ledger established by that proposal's Part B, `dev/measurement/review-floor-deviations.md`.
**Plan review**: required(Internal) — a new tool on a genuinely harder surface (commit diffs + messages) that a fresh-context reader should re-derive the heuristics against the real corpus. No shipped-template, install-contract, doctrine, or security surface, so the Internal floor is the right tier; an External read is welcome but not required by this proposal. Ratified at Decision.

## Context

The accepted `review-record-integrity` proposal corrected a real defect in
Cairn's own showcase arc: commit `17b7e5c`, whose message reads "open
check_cairn self-host-compat (+ Internal review)", added a proposal file
whose `**Status**` line said `proposed` while its tree already carried
**both** a filled-in `## Review -- Claude (Internal, same-session)` section
and a filled-in `## Review -- Gemini (External, different-agent-type)`
section; and the next commit `f4a8308`, messaged "add Gemini External
Review for check_cairn self-host-compat", added no review content at all —
it was `claim_check` marker maintenance mislabelled as a review-append, and
not in its own labelled commit as `doctrine/lifecycle.md:105-106` requires:

> * **auditable + unbundled** — its own labeled `claim-marker maintenance:`
>   commit (additions only), so the diff carries its own proof;

Both commits verify today: `git show 17b7e5c:dev/proposals/2026-06-12-claude-check_cairn-self-host-compat.md`
shows `**Status**: proposed` at its line 10 with `## Review` sections at its
lines 177 and 253, and `git show f4a8308` adds only `claim-check-allow`
marker tokens.

That is a **message/diff mismatch**. The rule it breaks is already doctrine
and already bright-line — `doctrine/lifecycle.md:28-30`:

> * **One commit per transition.** Open, review, response, and
>   decision each land as their own commit. Bundling hides who
>   changed what, and when.

and `doctrine/proposals.md:85-87`:

> Bundling multiple lifecycle stages into one commit hides who changed
> what; bundling lifecycle work with implementation work hides when the
> deliberation actually closed. Keep them separate.

Nothing mechanical enforces it. The sibling's Part A fixed the live
instance and its Part B corrected the record; this is the third leg —
**prevention** — split out at Internal review because it is a different
risk class whose heuristics had to be pinned against real commits rather
than imagined ones (`dev/proposals/archive/2026-07-08-claude-review-record-integrity.md:316-321`).

The felt pain is narrow and specific: an outside auditor reading Cairn's
deliberation record cannot distinguish "written up afterward" from
"fabricated," and the only thing standing between the record and that
ambiguity is an agent remembering a rule at commit time.

## Proposed paths

Proposed paths:
- `scripts/transition_lint.py` — the advisory check; lands in the implementing plan.
- `scripts/transition_lint_whitelist.py` — its commit-SHA suppression whitelist; lands with it.
- `bootstrap/tests/test_transition_lint.py` — its behavioral test; lands with it.
- `dev/plans/transition-lint.md` — the implementing plan; opens after the Decision.

## Proposal

Add `scripts/transition_lint.py`: a stdlib-only, **advisory** check that,
over a bounded rev-range, flags two shapes. Everything below is pinned
here, not deferred to the plan, because the whole reason Part C was split
out was that its rules were unpinned.

### Exit behaviour — advisory means advisory

**`main()` returns `0` whenever the scan completed, no matter how many
findings it printed. It never returns `1`.** The only non-zero return is
`2`, for a usage error (an unparsable rev-range, or a `--root` that is not
a git work tree) — mirroring the usage-error convention already in
`scripts/quality_gate.py:803-808`.

This is pinned in the type system, not just in prose: the `Finding`
dataclass carries `(sha, shape, file, message)` and **has no `severity`
field**. `quality_gate.py`'s `Finding` does carry one
(`scripts/quality_gate.py:97-101`), and its `failed` property
(`scripts/quality_gate.py:114-115`) drives `return 1 if report.failed else 0`
at `scripts/quality_gate.py:819`. Without a severity field there is no
fail-tier to wire up by accident.

### Home — a standalone script, not a `quality_gate.py --sub`

Both were evaluated. Standalone wins on four grounds:

1. **`quality_gate.py` is fail-closed and should stay that way.**
   `scripts/quality_gate.py:819` is `return 1 if report.failed else 0`.
   Housing an always-advisory check there means either forcing every
   finding to `severity="info"` — which collapses the very distinction the
   `Finding` dataclass exists to carry — or introducing a per-sub-gate exit
   policy, i.e. changing the shared gate's exit contract.
2. **Different input domain.** All three existing sub-gates scan the
   working tree. This one reasons over commit **diffs and messages**: it
   needs a rev-range positional, `git` subprocess handling, and rename
   detection that the other three neither share nor want. `quality_gate`'s
   CLI is already heterogeneous (`--seed-list`, `--shingle-size`,
   `--jaccard-threshold`); a fourth, wholly disjoint axis worsens it.
3. **Modifying an existing `scripts/*.py` is the *held* motion under
   Cairn's own gate-control tooling.** `bootstrap/tests/_gate_manifest.py:16`
   byte-freezes `scripts/*.py` by glob, and `bootstrap/tests/_gate_manifest.py:17-18`
   makes "modifying or deleting a frozen file HOLDs by default" — a new
   file is simply not a frozen file. That tooling governs supervised batch
   runs rather than every commit, but the posture it encodes is the point:
   editing `quality_gate.py` touches gate-control bytes Cairn has
   deliberately made expensive to change; adding a sibling script does not.
4. **The safe-git precedent is already a sibling script, not a sub-gate.**
   `scripts/measurements.py:24-27` records that `git_commits_in_range` runs
   git with a fixed argument vector and `shell=False` against a validated
   rev-range; the function is at `scripts/measurements.py:139` and the
   narrow rev-range regex at `scripts/measurements.py:51`. `transition_lint`
   reuses exactly that pattern rather than inventing rev-range validation.

**The honest cost:** a fourth standalone Cairn-only script grows the tool
surface, which is precisely the concern `doctrine/consolidation-review.md`
tracks. Mitigation: a `docs/tool-usage.md` section in the shape of the
existing `## scripts/verify_counts.py — re-measure registered live-invariant
counts *(Cairn-maintainer-only)*` heading at `docs/tool-usage.md:44`, plus a
`## See also` cross-link (`docs/tool-usage.md:147`) — note that
`quality_gate.py` itself is not documented there today, so this is a net
improvement in discoverability rather than a dilution.

**This is Cairn's first check that reasons over commit diffs and messages
rather than scanning files** — a materially harder surface. What makes it
harder is enumerated under *Known omissions* below, and every one of those
gaps is a documented v1 non-goal, not a coverage claim.

### The narrowed trigger (pre-registered constraint R3)

A commit is examined **only** if, after rename-aware enumeration, it has an
**`A` or `M`** entry under `dev/proposals/` or `dev/plans/`, excluding any
path containing `/archive/` and excluding `_template.md`. A rename (`R`) is
never a trigger.

Enumeration is `git diff-tree --no-commit-id --name-status -M -r -z <sha>`,
parsed with the `R<score>\0<source>\0<dest>` / `<status>\0<path>` walk that
already exists at
`templates/modules/team-gated/_intent/conflict.py:749-787` (called at
`templates/modules/team-gated/_intent/conflict.py:841`). That code is
reused rather than re-derived.

**`-M` is load-bearing and this is verified, not asserted.** On the
plan-open commit `5140e21`, `git diff-tree --no-commit-id --name-status -r
5140e21` reports four entries including
`A  dev/proposals/archive/2026-07-08-claude-review-record-integrity.md` —
a fully-reviewed proposal presenting as an *added* file. With `-M` the same
commit reports `R100  dev/proposals/2026-07-08-... -> dev/proposals/archive/2026-07-08-...`.
The `/archive/` path exclusion independently defuses *this* case, but `-M`
is still required for the general one: a proposal renamed within
`dev/proposals/` (a slug correction) would otherwise present as an added
file carrying a full review.

### Shape (a) — the message claims a transition the diff does not contain

**Claim detection is leftmost-wins over a fixed vocabulary, with
hyphen-compound suppression.** Each token is matched as
`(?<![-\w])<token>s?(?![-\w])`, and the *earliest* match in the subject
line wins; a subject claims at most one transition.

| claim token(s) | required evidence |
| --- | --- |
| `open` / `opens` / `opening` | an `A` entry under a trigger root |
| `review` / `reviews` | `## Review` \| `## Plan review` \| `## Code review` |
| `response` / `responses` | `## Response` \| `## Revised proposal` |
| `decision` / `accept` / `reject` / `supersede` | `## Decision` |

Hyphen suppression is what stops the repo's own slugs from reading as
claims: `review-record-integrity`, `automated-review-committer`, and
`review-floor deviations` all contain "review" inside a hyphenated
compound and must not trigger.

**Evidence is added body, never a heading.** A matching section counts only
if the commit adds **≥ 3 non-blank lines whose post-image line numbers fall
inside that section's span**. Heading-presence is worthless here, and this
is the finding the corpus produced that no one pre-registered: **this repo
seeds a titled `## Review` placeholder at open time.** `git show
3ae1d47:dev/proposals/2026-07-08-claude-review-record-integrity.md` carries
`## Review -- Claude (Internal, fresh-context subagent panel) -- 2026-07-08`
at its line 249 with an *"(Awaiting the Internal review…)"* body, and the
genuine review-append `e31625c` therefore adds **no** `+## Review` line at
all — it replaces the awaiting-note with the review body. A heading-based
rule flags the honest commit and misses the dishonest one.

Section spans come from the post-image (`git show <sha>:<path>`); added
line numbers come from `git show -M --format= --unified=0 <sha> -- <path>`
hunk headers.

### Shape (b) — an open commit whose added file already carries a real review

For each `A` entry under a trigger root: if the added blob's header
carries `**Status**: proposed` and any `## Review…` section body contains a
**review-grammar marker** — `[R<n>]`, `[E<n>]`, `**Steelman`, or
`**Covered**` — flag it.

The grammar marker is the discriminator between a *seeded placeholder* and
a *baked-in review*. It is what makes shape (b) fire on `17b7e5c` (twice,
once per baked-in review section) and stay silent on `3ae1d47` and
`87d3498`.

### The exemption model — the carve-in is the only source of truth

`AGENTS.md:149-164` is the sole exemption authority, and the tool's design
**restates it structurally rather than encoding a vocabulary**
(`AGENTS.md:151-157`):

> touching ONLY files under `dev/proposals/`, `dev/plans/`, `dev/strategy/`, or
> the `dev/.cairn/` fold-back ledger (any combination) is a deliberation /
> recording artifact and lands without per-commit approval — as does the single
> goodnight-handoff commit (its routine artifacts: `dev/NEXT_SESSION.md`, the
> end-of-day `dev/PLANNING.md` scrub, `CHANGELOG.md` additions, intent-ledger
> pruning) and the one-line `dev/PLANNING.md` row-move that serializes a
> lifecycle transition (proposal / plan open, supersession, archive).

Concretely, and this is the design's strongest property: **the narrowing
alone discharges the carve-in, so the tool needs no exception vocabulary at
all.**

* Strategy commits, `dev/.cairn/` ledger commits, and goodnight-handoff
  commits carry no `A`/`M` under `dev/proposals/` or `dev/plans/`, so they
  never reach a claim check.
* A bundled `dev/PLANNING.md` row-move is invisible: `dev/PLANNING.md` is
  not a trigger root, and its presence in a commit neither triggers nor
  exempts.
* `CHANGELOG.md` and `dev/NEXT_SESSION.md` are likewise not trigger roots.

**Pre-registered bright line.** The tool ships **no exception keyword, no
in-message opt-out directive, and no new obligation on any contributor.**
If implementation discovers it needs a rule the carve-in does not already
state, that is **new operational doctrine** and stops for its own
rate-limited doctrine proposal — it does not ship inside this tool.

### Suppression — exclusion roots plus a SHA whitelist (pre-registered constraint R10)

Two layers, mirroring the R6 machinery:

1. **Exclusion roots**, module constants in the shape of
   `scripts/quality_gate.py:494` (`_R6_SCAN_ROOTS`) and
   `scripts/quality_gate.py:497` (`_R6_EXCLUDE_DIRS`): trigger roots
   `dev/proposals/`, `dev/plans/`; excluded substring `/archive/`; excluded
   basename `_template.md`.
2. **A commit-SHA whitelist**, `scripts/transition_lint_whitelist.py`
   exporting `WHITELIST: frozenset[str]` of full 40-character SHAs each
   with a per-entry rationale comment — the exact shape and loading
   mechanism of `scripts/quality_gate_unused_def_whitelist.py`, imported by
   file path as at `scripts/quality_gate.py:70-79`. It **ships empty**: the
   two historical incident commits must keep flagging, since they are the
   acid test. An entry is added only with a written reason, so every
   suppression is auditable.

### CLI

```
python scripts/transition_lint.py [<rev-range>] [--report] [--root <dir>]
```

Default rev-range `HEAD~20..HEAD` (bounded and cheap; see Open questions).
`--report` emits TAB-separated `sha<TAB>shape<TAB>file<TAB>message` lines,
mirroring `quality_gate`'s machine-mode contract.

### Explicit non-goals

* It does **not** judge whether editing an already-committed section is a
  permitted refinement or an append-only violation. That is a different
  check.
* It does **not** assess a review's content, quality, attribution, or
  tier-independence.
* It does **not** run in a hook, in CI, or in `check_cairn.py`. It is
  invoked on demand and named in a plan's verification block.
* It is **not** shipped to adopters in v1 (see Alternatives #6).

### Documentation / doctrine surface

* **`docs/tool-usage.md`** — one new section (descriptive layer: a
  description of the software as it is), routed per
  [`docs/DOCUMENTATION_PLAN.md`](../../docs/DOCUMENTATION_PLAN.md).
* **`CHANGELOG.md`** — one entry at finalization.
* **`dev/PLANNING.md:129`** — the deferred "Transition-lint (Part C
  follow-up)" row moves at plan-open (the one-line row-move the carve-in
  blesses).
* **No `AGENTS.md` change and no `doctrine/` change.** The tool enforces
  an *existing* rule (`doctrine/lifecycle.md:28-30`); adding an
  *obligation to run it* would be doctrine and is explicitly out of scope.
* **No shipped template, no module, no install-manifest entry.**
  `python bootstrap/scaffold.py --manifest` emits 95 lines, as_of
  2026-07-22, and contains no `quality_gate.py`, `check_cairn.py`, or
  `measurements.py` — Cairn's own `scripts/` tools are repo-local by
  construction, and `transition_lint.py` joins them there. The install
  contract is untouched.

### Doctrine-change rate-limit (if this proposal changes doctrine)

**N/A — no doctrine change.** This is enforcement tooling for the
already-accepted one-commit-per-transition rule
(`doctrine/lifecycle.md:28-30`, `doctrine/proposals.md:63-87`); the
identical "N/A" for the sibling's Part C was accepted at
`dev/proposals/archive/2026-07-08-claude-review-record-integrity.md:625`.

Stated plainly so it cannot be read as a bypass attempt: this proposal
makes **no** high-risk classification claim. `doctrine/rationale.md:337-344`
limits the single-incident bypass to exactly two surfaces —

> * a **security surface** — the change closes a vulnerability,
>   hardens an authentication path, or removes a credential-leak
>   vector;
> * a **data-loss surface** — the change prevents irrecoverable loss
>   of work that cannot be reconstructed (stronger than "data
>   quality": the bar is that the data *can't* be rebuilt).

— and `doctrine/rationale.md:346-347` closes the door on everything else:

> Any other "this feels urgent" framing falls outside the bypass and
> obeys the recurrence requirement.

Record integrity being Cairn's differentiator is *that* excluded framing.
The gate does not apply here because no doctrine changes; if the exception
model ever diverges from the `AGENTS.md:149-157` carve-in, the gate applies
in full to that divergence, via its own proposal.

## Rationale

* **Which user workflow does it improve?** The maintainer's and each
  agent's commit-time discipline on the deliberation record. It is a
  discipline aid the author can run before opening a plan, and the
  Maintainer can run at a goodnight scrub, that answers one question
  cheaply: does this commit's message match what it actually did?
* **What contract does it preserve or clarify?** The
  one-commit-per-transition rule (`doctrine/lifecycle.md:28-30`) — until
  now enforced only by memory. It clarifies nothing new; it makes an
  existing rule mechanically visible.
* **What transparency / reproducibility does it improve?** The
  record-integrity property a skeptical outsider checks first. The
  differentiator claim is that Cairn's deliberation record is *auditable*;
  a check that the record's own commit messages are true is the cheapest
  possible support for that claim.
* **Why now?** The heuristics are only pinnable against a corpus, and the
  corpus now exists: the Phase-A series from 2026-07-08 to 2026-07-22 added
  plan-open renames, a plan-archive + `PLANNING.md` bundle, strategy
  carve-in commits, and four complete open/review/response/Decision arcs.
  That is exactly what the sibling's review said was missing. Doing it
  *before* the postdoc install also means the record they audit has been
  swept.

## Alternatives considered

1. **Do nothing.** This is the strongest alternative and deserves a fair
   hearing. The last 45 commits (`f0ce2af` back through `e31625c`, as_of
   2026-07-22) produce **zero** findings under the proposed heuristics —
   the discipline is currently holding without a tool. Against that: the
   one time it failed, it failed on the showcase arc, silently, and stayed
   undetected for roughly four weeks until a skeptical audit; and there is
   no tracker that would count a recurrence, since
   `dev/measurement/review-floor-deviations.md` records the *different*
   class `review-floor-deviation` (a review below its independence floor),
   not a message/diff mismatch. The tool costs one repo-local script and
   never blocks anything. Rejected, but a reasonable Maintainer could
   accept it — and should say so rather than let it pass by default.
2. **`quality_gate.py --sub transition`.** Evaluated in full above and
   rejected on the fail-closed exit contract, the disjoint input domain,
   the frozen-file HOLD posture, and the sibling-script git precedent.
3. **A fail-closed gate, or a `--strict` flag returning 1.** Rejected. The
   sibling already deferred escalation
   (`dev/proposals/archive/2026-07-08-claude-review-record-integrity.md:174-179`),
   and a `--strict` flag reopens the exact door that "advisory = always
   exit 0" exists to close. Revisit only with evidence of a sustained
   zero-false-positive record.
4. **A `commit-msg` or `pre-commit` hook.** Rejected for v1 on a mechanical
   ground: `commit-msg` runs before the commit object exists, so there is
   no SHA and no `diff-tree` to enumerate, and shape (b) needs the
   post-image blob. Separately, Cairn's hook-installation surface belongs
   to a team-gated module — `_cmd_install_hook` is defined at
   `templates/modules/team-gated/_intent/hooks.py:130` and wired at
   `templates/modules/team-gated/_intent/cli.py:428`, shipping to adopters
   as `tools/intent.py` — so a hook is a heavier, module-gated,
   install-contract surface than a repo-local script.
5. **A CI job.** Rejected as premature — the broad-look review already
   flags CI absence as untracked
   (`dev/strategy/2026-07-08-claude-broad-look-skeptical-review.md:693`),
   and this proposal should not be the thing that quietly decides Cairn's
   CI story.
6. **Ship it to adopters as a module.** Rejected for v1 and deferred with a
   named trigger. It would add an install-manifest entry — a high-risk
   install-contract surface per `AGENTS.md:310-312` — and, more decisively,
   the heuristics are pinned against *Cairn's own* commit-subject
   conventions (`dev/proposals: <slug> -- Response + Revised`, etc.), which
   an adopter's need not match. Revisit when a second real tree's corpus
   exists to validate against; recorded as a deferred follow-up at archive
   time.
7. **Recommended: a standalone, always-exit-0 `scripts/transition_lint.py`
   with corpus-pinned heuristics, a SHA whitelist, and no doctrine
   surface.**

**Maintainer preference during drafting:** none specific to this proposal
beyond the standing Phase-A direction to split by coherent decision, which
is why this exists as its own proposal rather than as the sibling's Part C.

### Open questions — the Maintainer's calls

1. **The default rev-range.** `HEAD~20..HEAD` is bounded and cheap but
   frankly arbitrary. Alternatives: require an explicit range and exit 2
   without one (most honest, least convenient), or a `--since=<date>`
   default. The proposal defaults to `HEAD~20..HEAD` and asks for a
   ruling.
2. **Whether the corpus-regression test tier belongs in the suite at
   all.** It pins real SHAs, so any history rewrite invalidates it; the
   proposal handles that by skipping rather than failing, but a Maintainer
   might reasonably prefer it as a manual command in the plan's
   verification block instead of a pytest node.
3. **Adopter shipping.** Deferred to v2 above (Alternative #6). Is that
   deferral the Maintainer's intent, or should the 0.4 release scope
   decide it now?
4. **An adjacent observation, surfaced not asserted.** The window contains
   four commits — `87e6529`, `2d665cc`, `8281a0a`, `d32498c` — whose
   subjects begin "Refine Gemini External Review of …" and which modify an
   already-committed Review section. Whether that is ordinary refinement
   by the reviewer of their own not-yet-answered section, or something the
   record should mark, is a question **this lint deliberately does not
   answer** (it is an explicit non-goal). Flagging it here because a
   reviewer will notice the same commits in the corpus and should know it
   was seen and scoped out, not missed.

## Evidence / verification plan

### Dogfood results — the corpus evidence (pre-registered constraint R9)

A prototype of the exact heuristics above was run over Cairn's own history
this session. All numbers are dated snapshots, as_of 2026-07-22, over the
window `d6646a3..HEAD` (the last 120 commits, `d6646a3` dated 2026-06-10
through `f0ce2af` dated 2026-07-22).

| run | commits scanned | passed the narrowed trigger | findings | false positives |
| --- | --- | --- | --- | --- |
| Sibling's literal Part-C wording | 120 | 52 | 26 | 23 |
| Proposed heuristics | 120 | 52 | **3** | **0** |
| Proposed heuristics | 45 | 41 | **0** | **0** |

The 3 findings are **exactly the two known-defective commits**: `17b7e5c`
twice (shape (b), once per baked-in review section) and `f4a8308` once
(shape (a), "add Gemini External Review" with no review body added). The
check therefore reproduces the original incident it was designed for, on
real history, with no false positives anywhere else in the window.

Every must-not-flag structure the sibling's review named was checked
individually and produced **zero** findings: the plan-open rename
`5140e21`; the plan-archive + `PLANNING.md` bundle `a0a617a`; the strategy
carve-in commits `18707e9`, `d0ba903`, `ebb1d6e`; the plan-archive
`d789414`; the proposal-open commits `3ae1d47` and `87d3498`; the genuine
review-append `e31625c`. Beyond that named set, four further real classes
in the window are clean: the four Phase-A Maintainer Decision commits
(`f0ce2af`, `34fb61f`, `6e9e237`, `c23338e`), the four Response + Revised
commits
(`2306f07`, `7c233b5`, `da9933c`, `755165d`), the plan-review and
code-review commits (`28816f0`, `29d46e7`), and the `dev/measurement` +
plan-checkbox bundle `2432f10` — whose subject contains "review-floor",
which hyphen suppression correctly declines to read as a review claim.

Three of the false-positive classes the naive wording produced are worth
naming, because each drove a specific design decision: (i) `dev/proposals:
… -- Response to Gemini External review` reads as a *review* claim under
bare keyword search — fixed by leftmost-wins; (ii) `dev/plans:
review-record-integrity -- Plan review` reads as a review claim from its
*slug* — fixed by hyphen suppression; and (iii) `open` commits flagged as
already containing `## Review` because the repo seeds a titled placeholder
— fixed by the grammar-marker discriminator.

**Reproduction for the reviewer.** The prototype lives in this session's
scratch space only and is deliberately not committed; the plan's
verification block re-runs the same numbers from the shipped script, and
the corpus-regression test (below) pins them.

### Author-accounting — invariants, failure modes, edge cases

* **Invariants.**
  (i) `main()` never returns 1 — *enforced by* an explicit test asserting
  the return value is 0 on a repo with findings, and structurally by
  `Finding` having no `severity` field.
  (ii) Renames are never treated as additions — *enforced by* a synthetic
  `git mv` fixture asserting zero findings.
  (iii) A commit with no `A`/`M` under a trigger root produces no findings
  regardless of its message — *enforced by* a synthetic strategy-only
  commit whose subject says "open … review … Decision".
  (iv) The two incident commits keep flagging — *enforced by* the
  corpus-regression test.
* **Failure modes.** All **open** by design: a missed real case degrades to
  today's memory-enforced status quo; a false positive is a printed line a
  human dismisses. There is no closed failure and no blocking path. A git
  invocation that errors returns an empty enumeration and the commit is
  skipped — the same degrade-to-prior-behaviour posture as
  `templates/modules/team-gated/_intent/conflict.py:757-758`.
* **Edge-case inventory.**
  *Handled:* empty rev-range (no findings, exit 0); rename into `archive/`;
  rename within `dev/proposals/`; a placeholder Review section at open; a
  Decision commit that flips status and appends `## Decision`; a
  reject/supersede Decision that *also* archives in the same commit — note
  the sibling's speculative edge case "a Decision commit that adds no
  section on a rejected-in-place proposal" is **dropped as premised on a
  false model**, since `doctrine/proposals.md:80-83` says a
  rejected/superseded Decision commit "flips status AND moves the file to
  `archive/`", and it still appends a `## Decision` section like any
  other, as the one superseded proposal in the tree shows
  (`dev/proposals/archive/2026-07-08-claude-automated-review-committer.md:428`).
  *Out of scope, v1:* merge commits; rebased or squashed history;
  amended messages; `git notes`; a commit body that contradicts its
  subject (only the subject is parsed).
* **Public-path → test mapping.** `transition_lint.main()` and
  `transition_lint.scan(rev_range)` → `bootstrap/tests/test_transition_lint.py`.
  Written as bare paths here, not relative markdown links, because the test
  file does not exist yet and a link would break `scripts/check_cairn.py`'s
  link check; the plan writes them as real relative links once the files
  land. (Same treatment the sibling used at
  `dev/proposals/archive/2026-07-08-claude-review-record-integrity.md:208-211`.)
* **Known omissions / intentionally untested edges.**
  **Merge commits are silently invisible, and this is verified rather than
  assumed:** `git diff-tree --no-commit-id --name-status -M -r d6646a3` on
  the merge commit `d6646a3` emits nothing at all, so a merge can never
  trigger and can never flag. There are 2 merge commits in the 120-commit
  window, as_of 2026-07-22. This is a documented gap, not coverage.
  Squashed and rebased history is likewise out of scope. The lint reads
  only the subject line, so a body that claims a different transition than
  the subject is not detected. And the whole tool is a *heuristic over
  Cairn's own subject conventions* — it will not generalise unchanged to
  another tree (Alternative #6).

### Tests required

`bootstrap/tests/test_transition_lint.py`, in two tiers:

* **Synthetic-repo tier (the behavioural contract).** Builds throwaway git
  repos under `tmp_path` via `subprocess` with a fixed `-c user.name` /
  `-c user.email` identity, and asserts each shape and each must-not-flag
  structure: a baked-in-review open commit (flags (b)); a
  message-claims-review-but-adds-a-marker commit (flags (a)); a placeholder
  Review at open (no flag); a genuine review-append that replaces the
  placeholder body (no flag); a `git mv` into `archive/` (no flag); a
  slug-only rename within `dev/proposals/` (no flag); a strategy-only
  commit with a transition-word subject (no flag); a `PLANNING.md` row-move
  bundled with a plan-open (no flag); an empty range (no findings, exit 0);
  a whitelisted SHA (suppressed). Guarded by
  `pytestmark = pytest.mark.skipif(shutil.which("git") is None, …)`, in the
  posture of the module-level skipif at
  `bootstrap/tests/test_quality_gate_cli.py:24-26`.
* **Corpus-regression tier (Cairn-repo-only, self-skipping).** Asserts the
  finding set over a *pinned* rev-range of Cairn's real history equals the
  pinned expected set — `17b7e5c` and `f4a8308` flag, and every
  must-not-flag SHA named in the dogfood above does not. **Skips** (never
  fails) if the repo root is not a git work tree or if any pinned SHA does
  not resolve, because a
  history rewrite would otherwise redden the suite for a reason unrelated
  to the code. This brittleness is real and is Open question 2.

**The suite baseline, stated honestly.** `python -m pytest bootstrap/tests`
gives **3 failed, 1408 passed, 3 skipped**, as_of 2026-07-22 (run this
session). The three failures are pre-existing and untouched by this
proposal: `test_ast_attest.py::test_committed_baseline_accounted_for_across_the_engine_package`
and `::test_ast_gate_passes_over_the_full_scaffold_module_set` (the known
stale AST-attestation baseline, issue #1), and
`test_evolution_infer.py::TestGateEval::test_main_suggests_and_json` (the
clock-expired test — its fixture rows are dated 2026-06-05 and 2026-06-01
against a 14-day rolling window). The correct claim is **"the three known
failures stay the only failures, and the added file count rises"** — not
"the suite stays green," which is false today.

**No AST re-anchor is required.** Nothing under `bootstrap/_scaffold/`
changes; `bootstrap/tests/test_ast_attest.py` pins that package only, so
`bootstrap/REANCHOR_RUNBOOK.md` is not in play. If the plan ever finds
itself touching `bootstrap/_scaffold/`, that is a scope breach and stops.

### Examples / smoke checks

* `python scripts/transition_lint.py d6646a3..HEAD` — the live dogfood,
  reproducing the table above from the shipped script.
* `python scripts/transition_lint.py` over this proposal's own commit
  series (open / review / response / Decision, then plan-open) — each must
  come back clean, which is the same self-application the sibling used.
* `python scripts/check_cairn.py` clean over the new `docs/tool-usage.md`
  section and the plan.
* `python scripts/claim_check.py` clean over this proposal and the plan.
* `python scripts/quality_gate.py --sub neutrality` — the new files must
  add **zero** findings to the pre-existing baseline of fail=99 recorded at
  `dev/plans/archive/review-record-integrity.md:387`. (The script names no
  vendor; the check is that this stays true.)
* `python scripts/quality_gate.py --sub redundancy` — confirm the new
  script adds no R6 unreferenced-def findings, or that any addition is a
  legitimate whitelist entry.

## Signals the change is wrong

* **It fires on a benign commit in ordinary use.** Recovery: whitelist the
  SHA with a written reason *and* open a follow-up to fix the heuristic —
  a whitelist entry that is not paired with a heuristic question is the
  start of the "trains people to ignore it" failure. If entries accumulate
  past a handful, retire the tool to a manual checklist item.
* **It goes a full release without firing on anything, and no one runs
  it.** Recovery: that is the "do nothing" alternative winning after the
  fact; delete the script and keep the corpus test as documentation of
  what was checked.
* **The heuristics need a per-commit escape directive in commit messages.**
  Recovery: stop. That is the exception vocabulary diverging from the
  `AGENTS.md:149-157` carve-in, which by this proposal's own bright line
  means new operational doctrine and a rate-limited proposal — not a patch
  to the script.
* **Someone proposes making it fail-closed to "make it matter."**
  Recovery: that is the Theme-3.4 nagging-gate failure mode arriving by a
  different door; require a recorded zero-false-positive window first, via
  its own proposal.
* **The corpus test starts failing after a history rewrite.** Recovery:
  it is specified to skip, not fail; if it fails instead, that is a bug in
  the guard and the tier should be demoted to a manual command per Open
  question 2.

## Review -- Claude (Internal, fresh-context subagent panel) -- 2026-07-22

**Model**: Claude Opus 4.8 (three fresh-context subagents on lenses tailored to this proposal's failure modes; no access to the authoring session; consolidated, none dropped).

**Attribution / committer note.** The panel's findings, transcribed faithfully — none softened, reordered to bury, or dropped. Per the binding practice from the superseded automated-review-committer Decision (2026-07-09), the raw panel source is committed in-tree at `dev/reviews/2026-07-22-transition-lint-internal-panel.json`; committed under the Maintainer's git identity by the author-session as disclosed scribe.

**Steelman.** All three lenses converge on the same read: this is the most carefully grounded proposal in the recent batch, and splitting Part C out to pin the heuristics before the plan was the right call.

Doctrine handling is clean. Every doctrine quote each lens opened is verbatim at its cited line — `doctrine/lifecycle.md:28-30` and `:105-106`, `doctrine/proposals.md:80-83` and `:85-87`, `doctrine/rationale.md:339-344` and `:346-347`, `AGENTS.md:151-157`. After a batch in which two proposals drifted a quote, this one did not. The rate-limit section is exemplary: it names the excluded "it is the differentiator" framing and disclaims it rather than reaching for it. On the doctrine-conformance lens's assigned question the verdict is favorable — the tool ships no exception keyword, no opt-out directive, and no new contributor obligation, so it restates rather than diverges and triggers no rate-limit gate.

The evidence baselines are exact. `python -m pytest bootstrap/tests` gives 3 failed / 1408 passed / 3 skipped with precisely the three named nodes; `python bootstrap/scaffold.py --manifest` emits 95 lines with zero `scripts/` entries, so the install-contract and no-AST-re-anchor claims hold; `quality_gate.py --sub neutrality` fail=99 reproduces.

The corpus work is real and reproduces. Two independent reviewers reproduced the trigger counts exactly (120/52 and 45/41). The false-positive-corpus lens reimplemented the heuristics from the proposal text alone and reproduced dogfood rows 2 and 3 exactly (`d6646a3..HEAD` → 120 scanned / 52 triggered / 3 findings / 0 FP; `HEAD~45..HEAD` → 45/41/0/0), then strengthened the result: over the full 536-commit history only 52 commits ever trigger, yielding the same 3 findings and 0 false positives repo-wide. Margins are healthy — the smallest true-negative margin is 11 added lines against a ≥3 threshold. `-M` really is load-bearing on `5140e21`, and the seeded-`## Review`-placeholder discovery (3ae1d47 seeds the heading at :249; e31625c adds zero `+## Review` lines) is real, non-obvious, and genuinely kills the naive heading rule. The pre-registered sibling constraints R2/R3/R4/R9/R10 are substantively engaged.

**Critiques** (descending severity; each grounded in a command/citation the reviewer ran):

* **[R1] (blocking)** A shipped, default-on commit-subject → lifecycle-stage vocabulary already exists and is never named — and it is already broken on Cairn's own corpus. `templates/modules/default-on/_lifecycle_metrics/gitmeta.py:14-22` defines `_STAGE_COMMIT_PATTERNS`, anchored regexes mapping commit subjects to open/decision/revised/reviewed, consumed by `_resolve_stage_commits` at `:65-83`. It ships to EVERY adopter (the manifest lists `tools/_lifecycle_metrics/gitmeta.py` verbatim). The proposal invents a second, incompatible vocabulary (leftmost-wins substring over a different token set) without citing the first — the exact 'do not invent a mechanism the code already has' hazard. Worse, running the shipped tool this session returns `stage_timestamp_reliability = Best-effort` for all 8 proposals, which per `gitmeta.py:110-112` means NO stage resolved to a commit: the shipped vocabulary matches none of Cairn's `dev/proposals: <slug> -- <stage>` subjects. Cairn would be shipping adopters a vocabulary broken on its own conventions while building a working one for internal use only. This also reframes Alternative #6: the natural v2 home is a `lifecycle_metrics` subcommand — already installed, zero new manifest entries — not a new module, so the 'it would add an install-manifest entry' rejection evaluates the wrong option.
  *Grounding:* templates/modules/default-on/_lifecycle_metrics/gitmeta.py:14-22, :65-83, :110-112; `python bootstrap/scaffold.py --manifest | grep lifecycle` (ships tools/_lifecycle_metrics/gitmeta.py verbatim); `python templates/modules/default-on/lifecycle_metrics.py proposals --root /Users/kendal30/Code/cairn --format csv` -> Best-effort x8
  *Suggested fix:* Add a subsection naming `_STAGE_COMMIT_PATTERNS` as prior art; state explicitly why transition_lint's vocabulary must differ (anchored-stage-resolution vs claim-detection) or single-source it; record the verified Best-effort-x8 drift as a finding and route it to its own follow-up; and re-argue Alternative #6 against a `lifecycle_metrics` subcommand rather than a new module.

* **[R2] (blocking)** The dogfood evidence layer — the one thing Part C was split out to get right — carries three defects, two of them inside sentences framed as verified. (a) MERGE COUNT FALSE [all three lenses]: the 'Known omissions' paragraph, explicitly labelled 'verified rather than assumed', asserts 'There are 2 merge commits in the 120-commit window, as_of 2026-07-22.' There are zero. The repo has exactly two merges in its entire history — d6646a3 (2026-06-10) and 4bf4ee4 (2026-06-09) — and both fall at or before the window's exclusive boundary; the window-scoped figure is the repo-wide total mislabelled. Compounding it, the merge-blindness demonstration is run on d6646a3 itself, which `A..B` semantics exclude from the very window it claims to characterize. This is the single most falsifiable number in the block and a reviewer checks it first — a wrong number inside a sentence claiming verification is precisely the failure mode this repo has been burned by. (b) WINDOW ENDPOINTS WRONG ON BOTH ROWS [all three lenses]: row 1 claims 120 scanned / 52 trigger for a window running 'd6646a3 dated 2026-06-10 through f0ce2af dated 2026-07-22' — but `d6646a3..f0ce2af` is 119 commits / 51 trigger. Row 3 claims 45 / 41 for 'f0ce2af back through e31625c' — but `e31625c..f0ce2af` is 43 / 39 and `e31625c~1..f0ce2af` is 44 / 40. The only ranges yielding 120/52 and 45/41 end at 57d1daf ('dev/plans: open adopter-licensing-compliance (+ archive proposal)'), a commit the proposal never names. The prototype ran past f0ce2af and the text was not re-synced. This matters concretely because the corpus-regression tier is specified to pin 'a *pinned* rev-range': a plan implementing the range as written will not reproduce the table and goes red on the day it lands. 57d1daf is also an in-window plan-open+archive commit absent from the must-not-flag inventory. (c) ROW 1 NOT REPRODUCIBLE [false-positive-corpus lens, raised at substantive severity]: 'Sibling's literal Part-C wording: 120 / 52 / 26 findings / 23 false positives' is not reproducible from the proposal and is internally inconsistent — it reports 52 'passed the narrowed trigger' for a variant whose defining property is that it *lacked* the narrowing (R3: 'The load-bearing narrowing ... is unstated'; R2: the naive plumbing is rename-blind). Best-faith reconstruction — bare keyword search, heading-presence evidence, no hyphen suppression, no leftmost-wins, narrowed trigger retained — yields 6 findings, not 26. Since the prototype is 'deliberately not committed,' a reviewer cannot close the gap, and this is the number that motivates the entire design.
  *Grounding:* (a) `git rev-list --merges --count d6646a3..HEAD` -> 0; `git rev-list --merges HEAD | wc -l` -> 2; `git log --merges --format='%h %ad %s' --date=short` -> d6646a3 2026-06-10, 4bf4ee4 2026-06-09; `git rev-list --merges d6646a3..f0ce2af | wc -l` -> 0. (b) `git rev-list --count d6646a3..f0ce2af` -> 119 (trigger-count loop -> 51); `d6646a3..HEAD` -> 120/52; `git rev-list --count e31625c..f0ce2af` -> 43 (39 trigger); `e31625c~1..HEAD` -> 45/41; `git rev-parse --short HEAD` -> 57d1daf; `git log -1 --format='%h %s' HEAD` -> 57d1daf dev/plans: open adopter-licensing-compliance (+ archive proposal). Reproduced independently by two lenses. (c) Naive reconstruction over `d6646a3..HEAD` printed `NAIVE: triggered=52 findings=6` (flags on 87d3498, 3ae1d47, 5739cc7, 17b7e5c shape-b; 6bdd9c6, 0d24fec shape-a) against the claimed 26/23; rows 2 and 3 reproduced exactly (120/52/3/0 and 45/41/0/0).
  *Suggested fix:* (a) Rewrite to: 'Zero merge commits fall inside the scanned window; the repo's only two merges (4bf4ee4, d6646a3) predate it. The merge-blindness demo runs on d6646a3, which is the window's exclusive boundary and therefore not itself a scanned commit.' (b) Pin both windows as explicit SHA..SHA with their real endpoints (`d6646a3..57d1daf`, `e31625c~1..57d1daf`), restate 120/52 and 45/41 against those, add 57d1daf to the named must-not-flag set, propagate the pinned SHAs to Alternative #1's '45 commits' sentence and the smoke-check command, and state the `A..B`-is-exclusive convention explicitly so 'through' is unambiguous. Do not use `HEAD` in a table whose numbers a reviewer must reproduce. (c) Either quote the sibling's literal Part-C rule text verbatim along with the exact trigger definition used for row 1 (so the 26 is recomputable), or delete the row and justify each design decision solely by the three named false-positive classes (leftmost-wins, hyphen suppression, grammar-marker discriminator) — which are individually checkable and already carry the argument.

* **[R3] (blocking)** Rename-only commits are structurally invisible to the lint, yet the edge-case inventory lists that case under *Handled*. On the tree's only supersession, the entire commit enumerates as a single rename into `archive/`; a rename is never a trigger and the destination is excluded by the `/archive/` substring rule, so the commit never reaches a claim check at all. The inventory spends a paragraph arguing such a commit does append a `## Decision` section — but under the proposal's own trigger rule the commit is never examined, so whether it appends a section is irrelevant. Consequently the shape-(a) vocabulary's `reject` and `supersede` tokens can never be evaluated on the only commit shape doctrine assigns them: they are dead tokens in v1. The same holds for every plan-archive commit. The general rule — 'a commit whose only lifecycle-file motion is a rename is invisible' — is stated nowhere, yet it silently exempts an entire class. 'Handled' reads as 'checked and correct'; the truth is 'silently exempt', and presenting silent exemption as coverage is precisely the overclaim this repo kills proposals for (the same class of error the sibling's R9 flagged).
  *Grounding:* `git diff-tree --no-commit-id --name-status -M -r b064576` emits exactly one line: `R091	dev/proposals/2026-07-08-claude-automated-review-committer.md	dev/proposals/archive/...` — zero A/M entries under a trigger root, so not examined. Same for `d789414` (only `M dev/PLANNING.md` + `R091` plan->archive). Independent prototype confirms neither commit is triggered. Doctrine: `doctrine/proposals.md:322-325` — '**Rejected** and **superseded** proposals move to `dev/proposals/archive/` in the Decision commit itself.'
  *Suggested fix:* Move the reject/supersede-plus-archive case from *Handled* to *Known omissions*, quoting the b064576 enumeration as proof, and state the general rule explicitly: 'a commit whose only lifecycle-file motion is a rename (proposal->archive, plan->archive) is never examined; reject/supersede Decisions and plan-archives are therefore outside coverage.' Add `b064576` and `d789414` to the corpus test as must-SKIP (not merely must-not-flag) so the gap is pinned rather than latent. Either drop `reject`/`supersede` from the claim vocabulary or mark them explicitly as dead tokens in v1.

* **[R4] (substantive)** Three load-bearing matcher details are unpinned or wrong inside the one section that declares 'Everything below is pinned here, not deferred to the plan.' (a) CASE-SENSITIVITY: the claim regex is given as `(?<![-\w])<token>s?(?![-\w])` over an all-lowercase token vocabulary, with no mention of `re.IGNORECASE`. Every real subject in the corpus capitalizes. Under a literal reading of the pinned spec, f4a8308 yields no claim and therefore no shape-(a) finding — directly contradicting the headline result ('3 findings ... f4a8308 once (shape (a))') and reddening the corpus-regression test on the day it lands. The dogfood cannot disambiguate this, because a case-sensitive build produces zero false positives too — it just produces silent false negatives that look like passes. (b) `-M` THRESHOLD: `-M` is argued entirely on its upside ('load-bearing and this is verified') with no examination of the failure mode it introduces. Empirically it changes the *trigger set* on 0 of 120 commits — the `/archive/` exclusion already defuses every real case, and the 'general case' it is defended by (a slug-correction rename within `dev/proposals/`) has never occurred. Meanwhile bare `-M` is a global similarity heuristic that can convert a genuine `A` into an `R` and silently un-trigger a commit; Cairn plans are derived from their proposals, which makes this concrete rather than theoretical. (c) `open`/`opening` TOKENS: the `open` claim fires on any bare 'open' in the subject and requires an `A` entry as evidence, so an M-only commit whose subject merely mentions Cairn's own live 'Open questions' vocabulary is a false positive. Today's rate is 0 only because every historical use of 'open' happens to be a transition verb — the precision rests on an undocumented subject-line convention (`dev/<tree>: open <slug>`), not on the rule. The `opening` token is pure downside: zero true positives in 536 subjects.
  *Grounding:* (a) `git log -1 --format='%s' f4a8308` -> 'dev/proposals: add Gemini External Review for check_cairn self-host-compat'; `git log -1 --format='%h %s' f0ce2af` -> 'Maintainer Decision -- ACCEPT record-corrections'; `git log -1 --format='%h %s' 2306f07` -> 'dev/proposals: record-corrections -- Response + Revised'. (b) `-r` vs `-M -r` trigger sets compared across all 120 commits: zero differences. `git log --diff-filter=R -M -- 'dev/proposals/*'` returns 5 renames, all proposal->archive; no slug correction exists. Synthetic repo demo: a plan-open adding `dev/plans/a-thing.md` derived from its proposal and deleting the proposal without archiving reports `A`+`D` under `-r` but `R096 dev/proposals/2026-01-01-a-thing.md -> dev/plans/a-thing.md` under `-M`. Cairn plans are proposal-derived — `dev/plans/archive/review-record-integrity.md:15` (`## Source proposal`). (c) 12 of 536 subjects match the open vocabulary and all 12 are genuine opens (regex over `git log --format=%s`); none uses 'opening'. 'Open questions' is live vocabulary: `dev/proposals/2026-07-11-claude-record-corrections.md:248`, `:482`, `:541`, and `templates/core/dev/strategy/_template.md:129`. Running the proposal's matcher: 'dev/proposals: transition-lint -- resolve open questions from the Internal review' -> claim=open; 'dev/plans: X -- close out the open acceptance criteria' -> claim=open; 'dev/plans: transition-lint -- opening sequence step 1' -> claim=open. Each would demand an `A` entry an M-only commit lacks.
  *Suggested fix:* (a) State case-insensitive matching explicitly in the pinned spec (`re.IGNORECASE`, or the flag inline), and add a synthetic-tier test asserting that an all-lowercase and an all-uppercase subject produce the same finding. (b) Pin the similarity threshold explicitly — `--find-renames=100%` (or `=90%`) rather than bare `-M` — so pairing is near-exact and a derived plan cannot be absorbed into a rename; add the synthetic derived-plan commit as a must-flag/must-trigger test; and record that `-M` currently changes the trigger set on 0/120 real commits so its cost/benefit is stated honestly. (c) Drop the `opening` token. Anchor the `open` token positionally — require it to be the first word after the `dev/<tree>: ` prefix (which all 12 true positives satisfy) — or require it be immediately followed by a slug-like token. Add the three subjects above as must-not-flag synthetic tests so the regression is pinned.

* **[R5] (substantive)** The exit-code contract has a silent-clean hole, and it cites one git precedent while adopting the opposite error posture from another. The proposal names `scripts/measurements.py:24-27`, `:51`, `:139` as its safe-git precedent — but `measurements.py:150-153` runs git with `check=True` and RAISES on failure, while the design adopts `templates/modules/team-gated/_intent/conflict.py:757-758`'s 'empty on any git error, degrade to prior behaviour'. Combined with 'the only non-zero return is 2, for ... an *unparsable* rev-range', a range that passes the regex but does not RESOLVE (`deadbeef..HEAD`, a deleted branch name, a typo'd SHA) enumerates nothing, prints nothing, and exits 0 — indistinguishable from a clean scan. For a tool whose entire value proposition is 'I ran it and saw nothing,' that is the one failure mode that must never be silent, and it is not covered by the edge-case inventory (which lists only 'empty rev-range (no findings, exit 0)').
  *Grounding:* scripts/measurements.py:150-153 (`check=True`) vs templates/modules/team-gated/_intent/conflict.py:757-758 and :759-767 (`check=False`, return {} on rc!=0); the proposal's own 'Exit behaviour' and 'Edge-case inventory' sections.
  *Suggested fix:* Resolve both endpoints with `git rev-parse --verify` before scanning and return 2 when either fails (usage error, consistent with `scripts/quality_gate.py:803-808`). Always print a one-line census — `scanned N commits, T triggered, F findings` — so a zero-finding run is positive evidence rather than silence. State which of the two git-error postures applies where.

* **[R6] (substantive)** Both halves of the human-facing signal are uninformative as specified. Verified: `git rev-parse --short HEAD~20` = `755165d`, and `17b7e5c` is NOT in `HEAD~20..HEAD`; the proposal's own table records ZERO findings over the last 45 commits. So the DEFAULT invocation returns nothing, indefinitely, for as long as the discipline holds. Meanwhile the only documented invocation that shows anything (`d6646a3..HEAD`) reports the same two immutable historical commits every single run — and the proposal explicitly refuses to whitelist them ('the two historical incident commits must keep flagging, since they are the acid test'). Since history is immutable, that is a permanent, unfixable 3-line wall on the one command a Maintainer is told to run: precisely the 'trains people to ignore it' Theme-3.4 failure the proposal elsewhere guards against, arriving on day one rather than after drift.
  *Grounding:* `git rev-parse --short HEAD~20` -> 755165d; `git rev-list HEAD~20..HEAD | grep -c $(git rev-parse 17b7e5c)` -> 0; proposal dogfood table row '45 / 41 / 0 / 0'; proposal Suppression section ('It ships empty').
  *Suggested fix:* Answer Open question 1 concretely: require an explicit rev-range (exit 2 without one) or default to `--since`. Ship the whitelist with `17b7e5c` and `f4a8308` entered WITH rationale comments pointing at the corpus-regression test, and give the test a whitelist-bypass argument so the acid test lives in pytest — where an immutable historical finding belongs — not in every human-facing run.

* **[R7] (substantive)** The pre-registered R10 constraint named three suppression layers; the design ships two and drops the only one that scales. `dev/proposals/archive/2026-07-08-claude-review-record-integrity.md:375-378` says the R6/Theme-3.4 lesson is the suppression infrastructure — 'exclusion roots + whitelist + info downgrade' — and the accepted Response at `:479-481` pins 'the info-tier analogy' as carried into Part C. This proposal deletes the severity concept outright ('has no `severity` field') and ships exclusion roots + a per-SHA whitelist only, without acknowledging that a pre-registered constraint was dropped. The consequence is concrete: `scripts/quality_gate.py:634` (`sev = "info" if name.startswith("_") else "fail"`) is a CLASS-level downgrade, which is what R6 actually needed; transition_lint has no equivalent. A recurring false-positive SHAPE (a new commit-subject convention) can then only be absorbed one SHA at a time, forever — which the proposal's own Signals section half-notices ('if entries accumulate past a handful, retire the tool'). Separately, 'pinned in the type system' overstates: nothing about a missing field prevents `return 1 if findings else 0`; the test is the pin. This also weakens ground 1 of the standalone-vs-sub-gate argument more than the proposal admits, since the `severity="info"` tier means quality_gate CAN host an all-advisory sub-gate.
  *Grounding:* dev/proposals/archive/2026-07-08-claude-review-record-integrity.md:375-378 and :479-481; scripts/quality_gate.py:634; scripts/quality_gate.py:97-101.
  *Suggested fix:* Either keep a non-exit-affecting `tier: "flag" | "note"` field on `Finding` (printed, never summed into a return code) as the class-level downgrade R10 asked for, or state plainly that R10's info-downgrade layer is being dropped and argue why two layers suffice. Do not leave a pre-registered constraint silently unmet.

* **[R8] (substantive)** The lint detects over-claiming only, never bundling — which is the other half of the very rule it quotes as its warrant. `doctrine/lifecycle.md:28-30` prohibits *bundling* (one commit carrying two transitions), and `doctrine/proposals.md:85-87` carries two clauses; the proposal quotes both but the heuristics test only 'message claims a transition the diff lacks.' Nothing checks the converse: a diff carrying lifecycle work the message does not announce, or lifecycle work bundled with implementation work. Worse, 'a subject claims at most one transition' (leftmost-wins) means an honest bundler is checked on its first claim only, so the tool is guaranteed blind to the very shape the rule exists to prevent; shape (b) covers exactly one bundling pair (open + baked-in review). This is defensible as a v1 scope bound, but it is not in the *Explicit non-goals* list, so the Rationale's claim that the tool 'makes an existing rule mechanically visible' reads as broader coverage than the design delivers.
  *Grounding:* Doctrine verbatim at `doctrine/lifecycle.md:28-30` ('One commit per transition. Open, review, response, and decision each land as their own commit. Bundling hides who changed what, and when.') and `doctrine/proposals.md:85-87` ('Bundling multiple lifecycle stages into one commit hides who changed what; bundling lifecycle work with implementation work hides when the deliberation actually closed.'). Running the proposal's leftmost-wins matcher: 'dev/proposals: X -- Response + Decision (bundled)' -> claim=response only; 'dev/proposals: X -- Internal review + Response' -> claim=review only — both pass silently while carrying two transitions. Real example: `git log -1 --format='%h %s' 28816f0` -> 'dev/plans: review-record-integrity -- Plan review (fresh-context Internal panel) + Sharpening', exactly that shape and clean under the proposed rules.
  *Suggested fix:* Add to *Explicit non-goals*: 'It checks only that a message's claim is supported by the diff. It does not detect the converse — unannounced lifecycle work, or lifecycle work bundled with implementation work (the second clause of `doctrine/proposals.md:85-87`).' Soften the Rationale from 'makes an existing rule mechanically visible' to naming the corner actually covered (over-claiming, plus the open + baked-in-review bundling pair). Optionally add a cheap symmetric check — flag when two or more distinct evidence sections each receive >=3 added non-blank lines in one commit.

* **[R9] (substantive)** `dev/plans/` is declared a trigger root for both shapes, but shape (b) can never fire on a plan: it requires `**Status**: proposed` in the added blob, and no plan ever carries that value. Compounding it, plan review headings are `## Plan review` and `## Code review`, neither of which starts with `## Review`, so shape (b)'s section scan would miss them even if the status test were fixed. The exact analogue of the 17b7e5c incident — a plan opened with a baked-in Plan review — is therefore undetectable, while the proposal's framing implies symmetric coverage across both roots.
  *Grounding:* `dev/plans/_template.md:77` -> `**Status**: open`; `dev/plans/adopter-licensing-compliance.md:8` -> `**Status**: awaiting-plan-review`; `dev/plans/archive/review-record-integrity.md:6` -> `**Status**: archived`. Headings at `dev/plans/archive/review-record-integrity.md:269` (`## Plan review -- ...`) and `:348` (`## Code review -- ...`).
  *Suggested fix:* Either extend shape (b) to accept `**Status**: open|awaiting-plan-review` and scan `## Plan review` / `## Code review` sections in addition to `## Review`, or state plainly in the shape-(b) definition that it is proposals-only and scope `dev/plans/` out of shape (b) — with a corpus test asserting the plan case is a documented gap, not silent.

* **[R10] (substantive)** The exemption model names the wrong doctrine authority, and omits the one whose rules it actually implements. `AGENTS.md:149-164` is an *approval* carve-in — it governs which commits 'land without per-commit approval' — and says nothing about one-commit-per-transition, which is the rule the lint enforces (`doctrine/lifecycle.md:28-30`). The bundling allowances a transition-lint genuinely depends on live in `doctrine/proposals.md:299-325` ('File moves'): :316-320 says the plan-open commit 'moves the proposal to `dev/proposals/archive/` in the same commit,' and :322-325 bundles the move into the reject/supersede Decision. Every must-not-flag the `/archive/` exclusion buys is derived from that section, which the proposal never cites. On the assigned divergence question the verdict is favorable — the tool ships no exception keyword, no opt-out directive, and no new obligation, so it restates rather than diverges and triggers no rate-limit gate — but 'the carve-in is the only source of truth' is not true as written.
  *Grounding:* AGENTS.md:149-164 (approval carve-in, read this session); doctrine/proposals.md:299-325, esp. :316-320 and :322-325 (File moves); doctrine/lifecycle.md:28-30 (the rule the lint enforces).
  *Suggested fix:* Retitle the section 'the carve-in plus the File-moves rule are the only sources of truth,' cite `doctrine/proposals.md:299-325` alongside `AGENTS.md:149-164`, and attribute the `/archive/` exclusion and rename-never-triggers to :316-325 rather than to the approval carve-in. Keep the no-new-vocabulary bright line verbatim — it is correct and is the section's real load-bearing commitment.

* **[R11] (substantive)** 'That code is reused rather than re-derived' overstates what is reusable and, taken literally, breaches the header's own scope claim. `_rename_map_via_git` at `templates/modules/team-gated/_intent/conflict.py:749-787` runs `git diff --cached --name-status -M -z` (line 761), takes no rev-range, and returns only `{dest: source}` for renames — it discards A/M/D/T entries entirely (`i += 2` at :784-786). It cannot enumerate a commit's A/M set, which is exactly what the narrowed trigger needs; only the `-z` token-walk idiom transfers, and the A/M enumeration is new code. Separately, if 'reuse' means import, that would be the first cross-layer import from `templates/` into `scripts/` (verified: no `scripts/*.py` imports template code — the only matches are path strings in scan roots), contradicting the header's 'No ... shipped template' scope claim and coupling a repo-local script to a shipped adopter module that `bootstrap/tests/_gate_manifest.py:167` freezes via `templates/modules/**/*.py`.
  *Grounding:* templates/modules/team-gated/_intent/conflict.py:749-787 (esp. :761 `git diff --cached ... -M -z` and :784-786 discarding non-R entries); bootstrap/tests/_gate_manifest.py:165-167; `grep -n '^import|^from' scripts/measurements.py scripts/check_cairn.py` -> stdlib only; `grep -rn 'templates/modules' scripts/*.py` -> strings and comments only, no import / sys.path / spec_from_file_location.
  *Suggested fix:* Reword to: 'copy/re-implement the documented `-z` `<status>\0<path>` / `R<score>\0<src>\0<dst>` walk idiom from `conflict.py:773-787`, adapted to `diff-tree <sha>`; the A/M enumeration is new code; no import crosses the `scripts/` <-> `templates/` boundary.' Add that non-import to the header's scope claim, and rule out importing from `templates/` into `scripts/` as a layering violation, so the plan cannot quietly take the shortcut.

* **[R12] (minor)** Four citation-accuracy defects a reader checking the argument will hit; `claim_check.py` catches none of them (all in-bounds line numbers), so only a reviewer will — exactly the class of drift this repo has been burned by twice. (i) `bootstrap/tests/_gate_manifest.py`: the `scripts/*.py` byte-freeze glob is at :14 (docstring) and :165-167 (the actual code), not :16; and 'modifying or deleting a frozen file HOLDs by default' spans :15-16, not :17-18 (:17 reads 'run must NOT decide that an edit to an existing gate is merely "strengthening"' and :18 is blank). Substantively, :16 says '*adding a new **test** file* is allowed and recorded' — it does not bless adding a new `scripts/*.py`, so 'a new file is simply not a frozen file' is the right conclusion drawn from the wrong sentence. (ii) The sibling's rate-limit 'N/A' is at `dev/proposals/archive/2026-07-08-claude-review-record-integrity.md:134-141`; the cited :625 is the `## Decision` heading. (iii) `doctrine/consolidation-review.md` is mischaracterized as tracking tool-surface growth. That file is 'the manual half of the redundancy gate' (:1); its R7 (:26-43) is an explicitly *per-dimension* capability checklist run 'For each dimension file under `dimensions/`' whose 'outputs feed the next major-version cut' (:42-43), and R1 (:45-61) filters n-gram prose overlap. Neither has anything to say about the number of repo-local scripts. (iv) The honest-cost paragraph — the one Alternative #1 ('do nothing') turns on — says 'a fourth standalone Cairn-only script', but `ls scripts/*.py | wc -l` = 16 today; `transition_lint.py` plus its whitelist would be the 17th and 18th files.
  *Grounding:* `grep -n '' bootstrap/tests/_gate_manifest.py | sed -n '10,25p'` (glob at :14, HOLD phrase at :15-16, :17 = 'strengthening' sentence, :18 blank; code glob at :165-167, frozen-set membership check at :168-174); `grep -n '' dev/proposals/archive/2026-07-08-claude-review-record-integrity.md | sed -n '622,628p'` (:625 = `## Decision` heading) and :134 = '### Doctrine-change rate-limit'; doctrine/consolidation-review.md:1, :26-43, :45-61; `ls scripts/*.py | wc -l` -> 16.
  *Suggested fix:* (i) Re-anchor to `bootstrap/tests/_gate_manifest.py:15-16` for the HOLD rule and `:165-167` for the glob (the code, not the docstring), and note that the 'adding is allowed' sentence is worded for test files — the argument rests on the frozen-set membership check at `:168-174`, which hashes what exists pre-run. (ii) Cite both :134-141 and :625 for the sibling N/A. (iii) Replace the consolidation-review invocation with an honest 'no doctrine currently tracks script-count growth in `scripts/`; this is a judgement call the Maintainer should make explicitly' — a stronger version of the same honest-cost point. (iv) State the real number (18 files under `scripts/` after this lands). All other anchors the panel checked are accurate and need no change.

**Coverage.** SWEPT (union across the three lenses, all this session):

Doctrine and record. Every `doctrine/` citation opened and line-verified — lifecycle.md:28-30, :105-106; proposals.md:63-87, :76-83, :80-83, :85-87, :136-140, :299-325; rationale.md:323-350, :339-344, :346-347 — and every `AGENTS.md` citation (:149-164, :151-157, :310-312). All verbatim at the cited lines, no drift. Rate-limit gate confirmed correctly declared N/A; confirmed the tool imposes no new obligation, no exception keyword, no opt-out directive. Pre-registered sibling constraints R2/R3/R4 (archive :291-321), R9/R10 (:362-378) and the accepted Response (:434-481) read in full.

Corpus and prototype. One lens built an independent prototype from the proposal text alone and ran it over `d6646a3..HEAD` (120), `HEAD~45..HEAD`, `HEAD~40..HEAD`, and the full 536-commit history — reproducing rows 2 and 3 exactly (120/52/3/0 and 45/41/0/0) and confirming 0 false positives repo-wide with only the 3 true positives (17b7e5c x2 shape-b, f4a8308 shape-a). Added-line evidence margin measured for all 52 triggered commits (min true-negative margin 11, max 160, against a >=3 threshold). `-r` vs `-M -r` trigger sets compared across all 120 commits (zero differences) plus a synthetic-repo demonstration of the `-M` rename-absorption hazard. Claim matcher run against 12 constructed subjects and all 536 real subjects. Two other lenses independently re-derived the trigger counts (120/52, 45/41, 43/39, 119/51), the merge enumeration, and the named SHA shapes: 5140e21 with/without `-M`, b064576 rename shape, d789414, 17b7e5c (status `proposed` at :10, `## Review` at :177 and :253, 7 `[R<n>]` markers), f4a8308 (2 insertions / 1 deletion, markers only), 3ae1d47 placeholder `## Review` at :249, e31625c adding zero `+## Review` lines, 28816f0, 57d1daf.

Code and gates. `scripts/quality_gate.py` dispatch end-to-end (`Finding:87-101`, `failed:113-115`, `_R6_SCAN_ROOTS:494`, `_R6_EXCLUDE_DIRS:497`, info tier `:634`, `_SUB_GATES:659`, `_build_arg_parser:662-712`, `run_gates:773-797`, `main:800-819`, usage-error `:803-808`, whitelist import `:65-79`); `scripts/measurements.py:24-27`, `:51`, `:139`, `:150-153`; `templates/modules/team-gated/_intent/conflict.py:749-787`, `:841`; `hooks.py:130`; `cli.py:428`; `test_quality_gate_cli.py:24-26`; `check_cairn.py:404` (`cairn-internal-ref-allow`); `bootstrap/tests/_gate_manifest.py` (found wrong — see R12); `docs/tool-usage.md:44/:115/:131/:147`; `dev/PLANNING.md:129`. Full suite run three times: 3 failed / 1408 passed / 3 skipped with the same three named nodes. `scaffold.py --manifest` = 95 lines, zero `scripts/` entries. `quality_gate.py --sub neutrality` fail=99 reproduced, matching `dev/plans/archive/review-record-integrity.md:387`. All `## ` heading forms across `dev/proposals/` and `dev/plans/` enumerated to confirm the section vocabulary is complete (including `## Revised proposal` at h2). Shipped `templates/modules/default-on/_lifecycle_metrics/gitmeta.py` read and `lifecycle_metrics.py proposals` executed against this tree.

NEGATIVE SPACE — swept by no lens, and someone should:
1. Security posture of the git subprocess surface and `--root` handling (all three lenses declined; one checked argument-vector shape only).
2. The synthetic-repo test tier's feasibility and fixture design — construction, `git mv` fidelity under `tmp_path`.
3. The review-grammar-marker discriminator's precision, the `>=3` added-non-blank-lines threshold, section-span / hunk-header arithmetic, and `--unified=0` correctness. Related: shape (b)'s `header` bound is undefined in the proposal; the prototype guessed 40 lines, so a shipped implementation could differ there and in hunk-header attribution.
4. The whitelist loading mechanism and the proposed pytest file's internals — neither exists yet, so the finding SET can only be re-derived once code is committed.
5. `docs/tool-usage.md` section wording, the CLI surface, and Open questions 1-3 (correctly routed to the Maintainer).
6. The strategy-review citations (:673-676, :693) and the archive Response citations (:434-481, :174-179, :208-211, :625, :428) beyond the two flagged in R12.
7. `quality_gate.py --sub redundancy` baseline (neutrality was re-run; redundancy was not).
8. The standalone-vs-sub-gate decision on maintenance-cost grounds beyond its four cited warrants, and the adopter-facing consequences of Alternative #6's deferral.

**Second-round recommendation.** UNANIMOUS: REVISE. Two of three lenses additionally recommend a TARGETED second Internal pass before Decision; one recommends going straight to Decision after the Response. The consolidated recommendation is the majority and superset position: REVISE, then a narrow, mechanical second Internal read — not a full re-review. No External read is needed: nothing here touches doctrine, the install contract, a shipped template's contract, or a security surface, and the proposal correctly reads its own tier.

Why not straight to Decision. The design is sound and the doctrine conformance is the cleanest in this batch; what fails is the evidence layer, which is the one thing Part C was split out to get right. R2 and R3 are record-integrity defects rather than design defects — fitting for a record-integrity tool — and both are fixable in an author Response without redesign: R2 states a false number inside a sentence claiming verification and mislabels both dogfood windows (the corpus-regression tier is specified to pin those exact ranges, so the plan as written guarantees a red test on the day it lands); R3 presents a structural blind spot as coverage. R1 is the gate on scope: the proposal should not reach Decision while a shipped, default-on commit-subject lifecycle vocabulary goes unnamed, especially given the verified Best-effort-x8 drift, which is a live finding about adopter-facing code the Maintainer should see before ruling on Open question 3.

What belongs in the Revised proposal text, not the plan. Deferring unpinned rules is exactly what got Part C split out, so these should be settled now: R4a case-insensitivity (it silently inverts the headline f4a8308 result), R4b the pinned `--find-renames` threshold, R4c dropping `opening` plus positional anchoring of `open`, R5 the `rev-parse --verify` + census contract, R6 a resolved default range with the two incident SHAs whitelisted and the acid test moved into pytest, R7 the `tier` field or an explicit statement that R10's info-downgrade layer is dropped, R9 the plan-scope statement, R3's reclassification to Known omissions, and R10's co-authority citation (`doctrine/proposals.md:299-325`). R8 may reasonably be answered by scoping rather than by adding a check — but the Rationale's overclaim should be corrected either way. R11 and R12 are corrections the Response can carry.

Scope of the second Internal pass. Re-read only the Home, Suppression, Exit-behaviour, Dogfood and edge-case-inventory sections against SHA-pinned endpoints; re-run the two rev-ranges and the merge count; confirm the reject/supersede + plan-archive reclassification; confirm the `scripts/` <-> `templates/` non-import is stated in the header scope. The `required(Internal)` plan-review tier is right, and the plan should additionally be bound to re-derive the heuristics and re-run the dogfood numbers from the COMMITTED script, recording both endpoints as SHAs — the finding set is the one claim no reviewer could check this round.

Maintainer calls, surfaced rather than adjudicated:
- Open questions 1-3 are correctly routed to the Maintainer. Two lenses note independently that Open question 1's arbitrary `HEAD~20..HEAD` default is weaker than the proposal admits: a HEAD-relative default is what produced the stale-endpoint error in the first place, so requiring an explicit range (exit 2 otherwise) is the option that would have prevented this proposal's own defect.
- Whether the shipped `_STAGE_COMMIT_PATTERNS` drift (Best-effort x8) becomes its own follow-up — one lens recommends it should, as a defect in shipped adopter code rather than this tool's scope.
- Raised outside any lens and worth the Maintainer's attention: commit 33487fc adds `dev/reviews/2026-07-11-record-corrections-internal-panel.json`, a lifecycle directory that is neither a trigger root in this proposal nor among the four paths named in the `AGENTS.md:151-157` carve-in.