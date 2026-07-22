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
