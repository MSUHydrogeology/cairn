<!-- cairn-internal-ref-allow: doctrine/rationale.md doctrine/dual-review.md doctrine/proposals.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see AGENTS.md, "Where doctrine/ references resolve") -->

# The release security scan misses the two files an adopter runs every day

**Author**: Claude (Strategy)
**Model**: Claude Opus 5
**Date opened**: 2026-08-03
**Status**: proposed
**Touches**: `bootstrap/security_check.py`, `bootstrap/tests/test_security_lint.py`,
`bootstrap/SAFETY.md`, `SECURITY.md`
**Related**: the broad-look strategy note `2026-07-08-claude-broad-look-skeptical-review`,
Theme 3 item 2; the in-flight `gate-reanchor-preflight` plan (frozen-file sequencing, see
*Signals* below). **Within-set file collisions** (both are Theme 3 siblings; this proposal has
no *cross-lineage* shared file) — this proposal shares `SECURITY.md`
with the sibling `agent-context-scrub`, and shares both `bootstrap/SAFETY.md` and
`bootstrap/tests/test_security_lint.py` with the sibling `gate-claims-vs-enforcement`;
only one proposal of each pair may be **in flight at a time**. It additionally has a
gate-coverage *ordering* relationship — no shared file — with `planner-line-semantics`
and with successor scope 2 of `2026-08-03-claude-identity-not-name`. Both kinds of
constraint are worked out in *Proposal > Sequencing*.
**Plan review**: required(External, security lens). The proposal triage list in
`dev/proposals/_template.md` names **both** touched security files — "`bootstrap/SAFETY.md`
(R-I), `bootstrap/security_check.py`, or the content scanner; a change here is also a
Security Review trigger" — so the tier is not a judgement call, it is the declared trigger.
The specific thing an External security reader must falsify is stated in *Author-accounting*:
that the new derivation can never yield a **smaller** scan set than the old one. This proposal
does **not** touch `bootstrap/_scaffold/`, so the AST attestation baseline and the engine gates
in `bootstrap/REANCHOR_RUNBOOK.md` are not triggered; it only *imports from* the engine
package, which `bootstrap/security_check.py` already does.


**Vocabulary and when the collision constraint binds** (identical in every
proposal of this set, so the set does not disagree with itself). *Within-set* =
two Theme 3 proposals claim the same file. *Cross-lineage* = a Theme 3 proposal
and a successor scope of `identity-not-name` claim the same file; there are
exactly two, `tools/lifecycle_planner.py` and `bootstrap/PROVENANCE.md`. The
constraint binds at **plan-open and implementation, not at proposal-open** — an
open proposal edits no file, so all of this set may be open, reviewed and decided
concurrently. Nothing mechanical enforces the constraint; it is carried by these
tables and by the work-intent claim taken before editing.

## Context

Cairn's release security gate is `bootstrap/security_check.py`. It is fail-closed by design:
a missing Bandit, a scanner error, or any unallowlisted MEDIUM-or-higher finding is a
non-zero exit. Bandit is a code-security linter — it reads Python source and reports patterns
associated with vulnerabilities, each with a severity and a confidence.

`SECURITY.md:66` describes what that gate covers: it fails on any unallowlisted MEDIUM+
finding *"over the shipped Python surface"*. `bootstrap/SAFETY.md:132` is more emphatic —
the Layer-4 executable class is *"the **whole shipped Python surface**, not only the
scaffold"*.

It is not the whole shipped Python surface.

`scan_targets()` at `bootstrap/security_check.py:57` builds its list of files to scan by
walking the scaffold's internal delivery registries — the data structures that say
"install this template file to that path in the adopter's repository." It walks two of them,
`_MODULE_MAPPINGS` and `_ALWAYS_ON_MAPPINGS`. There is a third: `_SKILLS_MAPPINGS` at
`bootstrap/_scaffold/config.py:214`. Nothing in the repository reads it for scanning purposes.

`_SKILLS_MAPPINGS` ships exactly two Python files, unconditionally, to every adoption:

| shipped source | adopter destination | physical lines |
| --- | --- | --- |
| `templates/skills/_lib/lifecycle.py` | `tools/lifecycle.py` | 1370 |
| `templates/skills/_lib/lifecycle_planner.py` | `tools/lifecycle_planner.py` | 1132 |

That is 2502 physical lines (1977 by Bandit's own logical-LOC metric), all counts *as_of
2026-08-03*. These are not peripheral. They are the command-line backend behind the
`session-start` and `session-end` skills — the routines `docs/quickstart.md:166` tells the
adopter their harness surfaces as commands. `AGENTS.md` requires session-start at every cold
start and after every context-loss event. In postdoc-first terms: **the code an adopter
executes most often, in their own repository, against their own git history, is precisely
the code the release security gate has never looked at.**

Measured at HEAD (`3292f21`) under the canonical interpreter:

```
$ python -c "from bootstrap.security_check import scan_targets; t=scan_targets(); \
             print(len(t)); print([x for x in t if 'skills' in x])"
72
[]
```

Seventy-two targets, as_of 2026-08-03. Zero of them from `_SKILLS_MAPPINGS`.

**Why this is a defect and not a design choice.** The same class of miss has already been
found and fixed once in this file. The comment block above `_ALWAYS_ON_MAPPINGS` at
`bootstrap/_scaffold/config.py:301` records it verbatim: `scan_targets()` *"(which derives
shipped-code coverage from `_MODULE_MAPPINGS` only) never release-scanned them."* The fix
at the time was to hand-add a second loop. The third registry was then missed by the same
mechanism the second one was. This is a hand-maintained list that someone must remember to
extend — which is exactly the root cause the strategy note names for Theme 2 as well
(*"hand-maintained descriptions of things that change, with no automatic check that fails
when they fall behind"*).

**The repository already knows how to do this correctly.** This is the part that settles the
shape of the fix. `bootstrap/tests/test_notice_install.py` — the gate that checks every
shipped Python file carries its SPDX license header — derives its file set from
`install_manifest(modules=None)`, joining `f"templates/{src}"`. That helper is at
`bootstrap/tests/test_notice_install.py:43`, and the suite pins its count at 44. Run both
derivations side by side:

```
licensing gate covers .py manifest sources: 44
security gate covers templates/ .py       : 42
covered by licensing but NOT by security  : ['templates/skills/_lib/lifecycle.py',
                                             'templates/skills/_lib/lifecycle_planner.py']
```

Cairn's **licensing** check sees the whole shipped Python surface. Cairn's **security** check
sees 42 of its 44 files. The two it misses are exactly the two the licensing check catches.
The correct derivation is not something this proposal invents — it is already the idiom in
this repository, applied to the lower-stakes concern, while the security gate kept the
drift-prone version.

**The decisive measurement.** The shape of the fix depends entirely on what Bandit says
about those two files, so it was run rather than assumed:

```
$ python -m bandit -q -f json templates/skills/_lib/lifecycle.py \
                              templates/skills/_lib/lifecycle_planner.py
total findings : 16
by severity    : {'LOW': 16}
MEDIUM or HIGH : 0
```

All sixteen are the subprocess family — `B404` (imports `subprocess`), `B603` (call with
non-literal arguments), `B607` (invokes `git` by name rather than absolute path). They are
LOW, and the gate's blocking set is `{"MEDIUM", "HIGH"}`, so **extending coverage creates no
triage backlog and turns nothing red**. This proposal is therefore the small shape the
orchestrating brief anticipated: a coverage fix plus a regression test, not a remediation
project.

Simulating the extension end-to-end over the full 74-target set — the real gate logic,
including the allowlist filter — confirms it:

```
base targets      : 72
extended targets  : 74
bandit rc         : 1
total findings    : 113
by severity       : {'LOW': 113}
BLOCKING (MEDIUM+, unallowlisted): 0
```

The gate passes. What changes is that from now on, a MEDIUM finding introduced into either
file will stop a release instead of shipping.

## Proposal

One contract: **the release Bandit scan covers every file the scaffold ships as byte-for-byte
Python — derived from the published install manifest, not from a hand-picked subset of the
registries behind it.**

### 1. Derive the shipped-code targets from `install_manifest()`

`install_manifest()` in `bootstrap/_scaffold/install.py` already unions all four delivery
registries (`_CORE_MAPPINGS`, `_SKILLS_MAPPINGS`, `_ALWAYS_ON_MAPPINGS`, `_MODULE_MAPPINGS`)
and emits `(source relative to templates/, destination, verbatim)`. It is the same enumeration
adopters depend on through the published `scaffold.py --manifest` contract, and it already
carries a destination-ownership refusal. It is the authoritative answer to "what ships."

Add to `scan_targets()`, as a **union with — not a replacement for** — the two existing loops:

```python
# Everything the scaffold ships as byte-for-byte Python, derived from the SAME
# published enumeration adopters depend on (`scaffold.py --manifest`) rather than
# a hand-picked subset of the registries behind it. Same derivation the SPDX
# licensing gate already uses (bootstrap/tests/test_notice_install.py). Kept as
# a UNION with the explicit loops above: this can only ever ADD targets, never
# remove one, so coverage is monotonically non-decreasing by construction.
# `modules=None` is load-bearing -- it means the FULL published catalog; a
# module subset here would silently shrink the scanned surface.
for src, _dst, verbatim in install_manifest(modules=None):
    if verbatim and src.endswith(".py"):
        targets.add(f"templates/{src}")
```

The union framing is deliberate and is the answer to the reviewer's central question. Because
the new code only calls `set.update`/`set.add`, "could this shrink the scan set?" is
answerable by inspection rather than by trusting a measurement. The two existing loops become
redundant-but-harmless and are **kept on purpose** as a defense-in-depth floor; removing them
is a separate change that would need this same review tier.

Measured, the derivation is an exact superset of today's — 42 shipped-template `.py` targets
become 44, with **zero removals** (as_of 2026-08-03):

```
manifest-derived minus current : ['templates/skills/_lib/lifecycle.py',
                                  'templates/skills/_lib/lifecycle_planner.py']
current minus manifest-derived : []
```

### 2. Fail closed, legibly, if the manifest refuses

`install_manifest()` raises `ValueError` if two sources claim one destination. Today an
uncaught raise would still exit non-zero — fail-closed in effect — but as a traceback rather
than a security message. Wrap the `scan_targets()` call at the top of `run_bandit()`:

```python
try:
    targets = [str(CAIRN_ROOT / t) for t in scan_targets()]
except ValueError as exc:
    print(f"security_check: cannot enumerate the shipped surface ({exc}) -- FAIL CLOSED.",
          file=sys.stderr)
    return 1
```

This is legibility, not new safety, and a reviewer may cut it without weakening the gate.

### 3. The regression test — the durable half

The defect is a list someone forgot to extend, so the durable fix is the test, not the
one-line union. Two assertions in the existing `bootstrap/tests/test_security_lint.py`
(which the release command and the dev gate already share):

* **Extend** `test_scan_targets_cover_all_shipped_scripts` at
  `bootstrap/tests/test_security_lint.py:134` to derive `shipped` from `install_manifest()`
  instead of from `_MODULE_MAPPINGS`. This is the anti-drift assertion the test already
  claims to be; it was simply reading the same partial source the code was.
* **Add** a named-file assertion for the two skills tools, so this specific miss cannot
  recur silently even if the derivation is later refactored.

The extended assertion was written and run against unmodified HEAD to confirm it is a real
regression test and not a tautology:

```
E   AssertionError: shipped verbatim .py not release-scanned:
E   ['templates/skills/_lib/lifecycle.py', 'templates/skills/_lib/lifecycle_planner.py']
1 failed in 0.03s
```

It fails at HEAD with exactly the right message, and passes under the union above.

### 4. The residual, and its tripwire

Binding the scan to the manifest makes the manifest the single chokepoint: anything in the
manifest is scanned, with no list to extend. The residual is a delivery path that never
reaches the manifest at all — which is the historical `_ALWAYS_ON_MAPPINGS` side door.

That residual is already guarded from the other side (such a file is also untracked by the
lockfile and unattested on upgrade, and `assert_always_on_complete` fails closed on a partial
group), so this proposal does **not** build a new mechanism for it. It adds one cheap
tripwire in the same test file: a census that fails when a module-level `*_MAPPINGS` symbol
appears in `bootstrap/_scaffold/config.py` that is not in a small declared table, with the
failure message telling the author to confirm the new registry reaches `install_manifest()`.
This is the part of the proposal a reviewer can strike without breaking the primary fix, and
it is named as such rather than buried.

### Sequencing

Two constraints bear on when this proposal lands. They are different in kind, and
conflating them is how a sequencing decision goes wrong. The first is a **file-collision**
constraint — who may edit which file, when. The second is a **gate-coverage ordering**
constraint — which changes fall on the scanned side of the gate this proposal widens.

**The file collisions — one proposal per shared file, in flight at a time.** Two proposal
*lineages* are open against this tree at once; a lineage here just means a chain of
proposals descending from one origin. Lineage 1 is the supersession of
`2026-08-03-claude-identity-not-name` into four successor scopes. Lineage 2 is the seven
Theme 3 proposals, of which this is one. They were drafted in parallel and could not see
each other, so their claimed file scopes overlap. Verified overlaps for *this* proposal,
as_of 2026-08-03:

| sibling proposal | file(s) shared with this one | relationship |
| --- | --- | --- |
| `agent-context-scrub` | `SECURITY.md` | collision **and** gate-coverage ordering |
| `gate-claims-vs-enforcement` | `bootstrap/SAFETY.md`, `bootstrap/tests/test_security_lint.py` | collision only |
| `planner-line-semantics` | — none — | gate-coverage ordering only |
| `identity-not-name` successor 2 (exact byline classification) | — none — | gate-coverage ordering only |

**The rule: only one proposal of each colliding pair is in flight at a time.** Where the
overlaps actually sit was checked, because that determines whether serializing costs a
rebase or a rewrite — in every case they are file-level, not line-level:

* **`SECURITY.md`.** This proposal's claim is about the *Release security checklist*
  section, and it concludes that section needs **no edit** (see *Documentation / doctrine
  surface*): the existing phrase "over the shipped Python surface" simply becomes true.
  `agent-context-scrub` adds a bullet to a different section, *Documented residual risks
  (consciously accepted)*. This side of the collision is therefore a no-op edit, which
  makes yielding cheap — but the one-in-flight rule applies to *claimed* scope, not to
  realized diffs, so it is recorded and honored rather than argued away.
* **`bootstrap/SAFETY.md`.** This proposal rewrites the Bandit scan-set derivation
  sentence at `bootstrap/SAFETY.md:158` and extends the Layer-4 enumeration of verbatim
  reference scripts. `gate-claims-vs-enforcement`'s disposition B1 re-words a *different*
  sentence in the same file — the content-integrity-scanner clause inside the
  by-file-class review-threshold block.
* **`bootstrap/tests/test_security_lint.py`.** This is a third overlap, beyond the two
  named above, and it is real: the file appears in that sibling's own *Touches* line,
  marked deferred. This proposal edits it substantively (item 3);
  `gate-claims-vs-enforcement`'s disposition A5 corrects a docstring and a skip message
  in it, and is **already deferred** behind the same frozen-file batch discussed below.
  Both are therefore waiting on the same window and must serialize when it opens.

**Not merged.** These proposals stay separate. Merging overlapping scope is the bundling
mistake that cost `2026-08-03-claude-identity-not-name` a REVISE/SPLIT verdict from its
External Security Review earlier the same day; the correct handling is sequencing, not
consolidation.

**The ordering question — this proposal lands FIRST.** Three proposals modify the two
files this one adds to the scan: `agent-context-scrub` (escaping what the orientation
stream relays), `planner-line-semantics` (what counts as a line separator), and
`identity-not-name` successor 2 (exact byline classification). So there is a genuine
ordering question, and it is better settled explicitly than left to fall out of whatever
happens to land first.

Note what the question is **not**. This proposal does not edit
`templates/skills/_lib/lifecycle.py` or its planner twin — it only widens what the gate
*reads*. There is no textual conflict with any of the three, in either order. The only
thing at stake is which side of the gate those three changes fall on.

**The measurement that decides it.** Re-verified at HEAD `3da58c1` under the canonical
interpreter (Bandit 1.9.4), because the whole argument turns on whether landing early
imports a triage backlog:

```
$ python -m bandit -q -f json templates/skills/_lib/lifecycle.py \
                              templates/skills/_lib/lifecycle_planner.py
total findings : 16
by severity    : {'LOW': 16}
MEDIUM or HIGH : 0
test ids       : {'B404': 2, 'B603': 10, 'B607': 4}
```

Zero MEDIUM-or-higher findings, as_of 2026-08-03. The gate's blocking set is
`{"MEDIUM", "HIGH"}`, so **landing first has a measured triage cost of zero**: nothing
turns red, no backlog is created, and the three later proposals inherit a gate that is
green on the day they begin. The obvious objection to going first — that a dirty scan
would make this proposal a blocker, stalling the other three behind a triage queue — was
the thing worth checking, and it does not obtain.

**Position: FIRST.** Four reasons, in descending weight.

1. **The cost asymmetry is measured on one side and unmeasurable on the other.** Landing
   first costs zero — verified above. Landing last costs whatever the three intervening
   changes happen to introduce, which cannot be measured until they land. A choice
   between a measured zero and an unbounded unknown resolves toward the measured zero.
   That is precisely what the measurement was taken to determine.
2. **"Scan final rather than intermediate bytes" confuses an audit with a gate.** A
   one-time audit *should* read the settled artifact — measure once, at the end. A gate
   is a standing check that runs on every release and every dev-suite invocation, and its
   value is exactly that it reads intermediate states, because that is where a defect is
   cheap to fix. Under the audit framing LAST wins; under the gate framing FIRST wins.
   `SECURITY.md`'s *Release security checklist* is unambiguous about which one this is.
   So the framing that favors LAST does not describe the thing being changed.
3. **The three intervening changes are exactly the class this gate exists to watch.** All
   three modify parsing and normalization code — escaping relayed text, redefining a line
   separator, classifying a byline. And the measured character of the existing findings
   says where the risk in these files lives: all sixteen are the subprocess family
   (`B404` import, `B603` non-literal call arguments, `B607` partial executable path).
   Illustratively — not as a claim about what any of those proposals does — a new
   `subprocess` call added with `shell=True` while touching this code is `B602`, which
   Bandit rates **HIGH** severity at HIGH confidence when the command is not a literal
   string (verified against a probe, 2026-08-03). Under LAST that ships and is discovered later, and this proposal inherits a
   HIGH-severity triage as the price of its own coverage fix. Under FIRST it fires in the
   author's own suite run, before landing, attributed to the change that caused it. Same
   defect, very different cost, and the only difference is the order.
4. **Landing first makes three subsequent security reviews cheaper.** All three carry an
   External security read. A reviewer of any of them who asks "is this file covered by
   the release Bandit gate?" gets **no** today. With this proposal landed, the answer is
   **yes**, and the reviewer's remaining scope narrows to what Bandit cannot see. That
   benefit is forfeited entirely if this lands last.

**The honest case for LAST, and why it loses.**

* *Churn — the gate would run over moving code.* Not a cost. The run is automated and
  already happens on every suite invocation; a moving target makes a per-run scan neither
  more expensive nor less correct.
* *Verification economy — verify the extension once, over final bytes.* There is none to
  capture. An External reviewer verifying this proposal's central claim ("the scan set can
  only grow") reads `scan_targets()`, not the two scanned files, and the union framing in
  item 1 makes that check structural rather than empirical. The reviewer's work is
  unchanged by what the two files contain.
* *The genuine one — cost transfer.* If this lands first and one of the three later
  changes does introduce a MEDIUM finding, that change's gate goes red and its author must
  triage before landing. That is a real transfer of cost — but it moves toward the change
  that caused it and earlier in that change's life, which is the cheaper end of both axes.
  It is what a gate is for. The three affected proposals need one sentence each noting
  their gate surface is now wider; that is a courtesy, not a sequencing obstacle.

**The constraint that can override the position.** This proposal does not control its own
schedule. Its two code files, `bootstrap/security_check.py` and
`bootstrap/tests/test_security_lint.py`, are both in the `gate-reanchor-preflight` frozen
set — the list of files whose modification HOLDs by default during an active batch window
(162 frozen entries, as_of 2026-08-03; see *Signals* for why that default exists). The
three proposals it wants to precede touch no frozen file. So if the window is open and no
Maintainer-authorized HOLD resolution is available, this proposal *cannot* land first,
however much it should. In that case the fallback is not "land last quietly" but **land
last with the measurement re-taken**: re-run the two-file Bandit command above over the
post-change bytes before asserting the zero-backlog claim, and treat any non-zero MEDIUM+
count as a finding attributable to whichever change introduced it — not as a cost of this
proposal, and not as grounds to narrow its coverage.

**Net recommendation.** Land this first if the frozen-file window permits; otherwise land
it immediately after the batch closes and before as many of the three as remain unlanded,
re-measuring at that point. The one ordering to avoid is last-of-all with the
2026-08-03 measurement carried forward unchecked.

### Documentation / doctrine surface

Three prose surfaces make a claim broader than the implementation, and are corrected to match:

* `bootstrap/SAFETY.md:158` — *"The Bandit gate derives its scan set from `_MODULE_MAPPINGS`
  (verbatim scripts) plus `scripts/` + `bootstrap/`"*. Corrected to name the manifest
  derivation.
* `bootstrap/SAFETY.md` — the Layer-4 enumeration of verbatim reference scripts (the list
  running from `claim_check.py` through the `content-security` apparatus) does not mention
  `lifecycle.py` or `lifecycle_planner.py` **at all**. They are added. A reviewer using that
  list to decide "does my change ship as code?" would today conclude, wrongly, that the
  skills tools are not Layer-4 code.
* The module docstring of `bootstrap/security_check.py` repeats the `_MODULE_MAPPINGS`-only
  description; corrected in the same commit.

`SECURITY.md:66` needs **no** change — *"over the shipped Python surface"* becomes true.
That is the point: the doctrine was right and the code was wrong.

Routing per `docs/DOCUMENTATION_PLAN.md`: all three are descriptions of the software as it
is, kept in the descriptive/governing files that already own them. No `dev/` doctrine file
and no template changes. Nothing ships to adopters — every touched file is Cairn-internal.

### Doctrine-change rate-limit

**Does not apply — this proposal changes no doctrine.** The rule (*"the whole shipped Python
surface"* is Layer-4 code, gated by Bandit) is unchanged, already accepted, and already
written down. What changes is the implementation and the two sentences that mis-describe it.
Bringing code up to an existing rule is the opposite of a doctrine change, so the recurrence
/ high-risk gate in `doctrine/rationale.md` is not engaged.

## Rationale

* **Which user workflow does it improve?** The adopter's daily one. `tools/lifecycle.py` and
  `tools/lifecycle_planner.py` run at every session start and end, shelling out to `git` in
  the adopter's repository. Postdoc-first: in the first two weeks, these are the two shipped
  Python files the postdoc actually executes, and they are the two the gate never checked.
* **What contract does it clarify?** The release gate's coverage contract. After this change,
  "the shipped Python surface" is a derivation from the published install manifest rather
  than an assertion in prose that the code partially implements.
* **What correctness / reproducibility does it improve?** A security claim in `SECURITY.md`
  becomes verifiable from the code. Cairn's pitch to a research team is recorded, checkable
  reasoning; a security gate whose stated scope exceeds its real scope is the exact failure
  Cairn tells adopters to avoid.
* **Why now?** Pre-first-external-adopter, at v0.3, is the cheapest possible moment: the
  measurement shows zero blocking findings, so the fix costs nothing today. Every day the
  two files evolve, the chance that extending coverage later means paying a triage backlog
  goes up.
* **Standing direction check — "fix defects, build nothing new."** This adds no tool, no
  file, and no mechanism. It changes one function to read an enumeration that already exists,
  using a derivation another test in the same suite already performs, extends one existing
  test, and corrects three sentences. The one thing that could be read
  as "new" is the registry-census tripwire in item 4, which is why it is isolated,
  justified, and explicitly marked strikeable.

## Alternatives considered

* **Do nothing.** Rejected. The gate keeps claiming coverage it does not have; 2502 lines an
  adopter runs daily stay unscanned; a MEDIUM finding introduced into either file ships
  silently. The strategy note flags this as a claim *"a careful reader will catch"* — and the
  first external adopter is a scientist trained to check claims.
* **The minimal one-liner: add a third loop over `_SKILLS_MAPPINGS`.** Rejected, and this is
  the important rejection. It fixes today's instance while reproducing the defect class
  exactly — a hand-picked list of registries that a fourth registry will fall out of. The
  same fix shape was applied to `_ALWAYS_ON_MAPPINGS` and did not prevent this miss. It also
  leaves the repository in the odd state where the licensing gate derives from the manifest
  and the security gate does not.
* **Glob `templates/**/*.py`.** Rejected. Measured as *equivalent today* (44 files either
  way, as_of 2026-08-03), but semantically weaker in both directions: it would scan a template
  authored but not yet wired into a registry (a normal mid-development state) and fail the
  gate on unshipped code, and it would stay green if a shipped file were dropped from the
  manifest but left on disk. The scan should track *what ships*, which is what `SECURITY.md`
  claims.
* **Scan the adopter-facing destinations (`tools/*.py`) instead of the template sources.**
  Rejected. Cairn's own `tools/lifecycle.py` is byte-identical to its template twin today
  (verified with `cmp`, and the suite already enforces it in
  `test_every_self_hosted_twin_stays_byte_identical_to_its_source`), but the shipped source
  is the authority and the installed copy is a derived artifact.
* **Lower the blocking threshold to LOW so the sixteen findings gate.** Rejected as a
  different contract. It would turn the gate red on 113 LOW findings across the post-change
  surface — only 16 of them newly visible, the other 97 already scanned and already tolerated
  (as_of 2026-08-03) — and belongs in its own proposal if anyone wants it. Per
  the no-bundling rule, this proposal changes coverage only, not threshold.
* **Replace the existing loops rather than union with them.** Rejected on review-cost
  grounds. Replacement is measurably equivalent today but forces the security reviewer to
  verify a set *equality* across all future config shapes; the union makes
  "coverage cannot shrink" true by construction.

## Evidence / verification plan

Everything asserted above was produced at HEAD `3292f21` under the canonical interpreter
`~/conda_envs/lhm/bin/python` (Python 3.13.13, Bandit 1.9.4). No repository file was modified
to produce it — the extension was simulated in a scratch script that imports the real
`scan_targets()` and `ALLOWLIST` and applies the real blocking filter.

### Author-accounting — invariants, failure modes, edge cases

* **Invariants.**
  * *Every verbatim `.py` in `install_manifest()` is in `scan_targets()`.* A live invariant,
    enforced by the extended `test_scan_targets_cover_all_shipped_scripts`.
  * *`scan_targets()` never shrinks as a result of this change.* Enforced structurally: the
    new code is a `set.add` into the same accumulator, and the pre-existing loops are
    retained unmodified. This is the single claim an External security reviewer should
    attack — if the union were ever refactored into a replacement, the guarantee becomes
    empirical again.
  * *`install_manifest` is called with `modules=None`.* Load-bearing: any module subset
    would shrink the scanned surface. Pinned by the extended coverage test, which derives
    its expectation the same way.
  * *Every target is a file, never a bare directory.* Pre-existing invariant, already
    enforced in the same test (the missing-`-r` footgun); `templates/{src}` entries are
    single files, so it holds.
* **Failure modes.**
  * `install_manifest()` raises on duplicate destinations → **closed** (exit 1 with a clear
    message, per item 2). Intentional: a release gate that cannot enumerate the surface must
    not proceed.
  * A shipped file listed in the manifest is missing from disk → Bandit errors, `rc` outside
    `{0, 1}` → **closed** by the pre-existing scanner-error branch.
  * A delivery path that bypasses `install_manifest()` entirely → **open**, and named as the
    residual in item 4. Guarded indirectly (lockfile, upgrade attestation,
    `assert_always_on_complete`) and tripwired by the census.
* **Edge cases.** Empty registry → `shipped` empty → the pre-existing
  `assert shipped, "expected at least one verbatim .py reference script"` fires. Non-`.py`
  verbatim entries (`vendor_targets.yml`) → filtered by the `.endswith(".py")` guard, same
  as the existing loops. Substituted (non-verbatim) `.md` skills sources → correctly
  excluded; they are prose on the content-scanner path, not Layer-4 code.
* **Public-path → test mapping.** `scan_targets()` and `run_bandit()` are both exercised
  through their public paths — not via stubs — by
  [`bootstrap/tests/test_security_lint.py`](../../bootstrap/tests/test_security_lint.py),
  which the release command and the dev gate share by import.
* **Known omissions / intentionally untested edges.** The sixteen LOW subprocess findings are
  **recorded, not remediated** — four of them (`B607`) are `git` invoked by name rather than
  absolute path in code that runs inside an adopter's repository. Whether that is worth
  hardening is a real question and a *separate* proposal; bundling it here would mix a
  coverage contract with a code-hardening contract. Cairn's own `tools/*.py` copies remain
  outside the scan (only `scripts/` and `bootstrap/` are globbed); they are byte-identical
  twins of scanned template sources, so this is coverage-neutral today and is not addressed.

### Tests required

* `test_scan_targets_cover_all_shipped_scripts`, in `bootstrap/tests/test_security_lint.py`
  — extended to the manifest derivation. **Confirmed to fail at HEAD** and pass under the fix.
* A new named-file assertion pinning both skills tools into the scanned set.
* A new registry-census assertion (item 4; strikeable).
* `test_no_blocking_security_findings`, in the same file — must stay green over the extended
  set. **Measured green** (0 blocking over 74 targets).
* The full suite, `python -m pytest bootstrap/tests`, under Python 3.13.x.

### Examples / smoke checks

* `python bootstrap/security_check.py` — the real release gate, end to end. Expected: `PASS`,
  with the Bandit line reporting 74 files rather than 72.
* `python bootstrap/scaffold.py --manifest` — unchanged output. The published install
  contract is *read* by this change and must not move; a diff here means something went wrong.
* `python scripts/check_cairn.py` — the doc smoke for the `SAFETY.md` edits.
* `python scripts/claim_check.py` over this proposal before commit.
* **N/A**: the example gallery (`examples/`). This change touches nothing the runnable
  examples demonstrate.

## Signals the change is wrong

* **`scan_targets()` returns fewer shipped-template targets than 42.** The derivation is
  wrong or the union was refactored into a replacement. Recovery: revert to the explicit
  registry loops, which are retained precisely so this revert is a one-line deletion.
* **The release gate starts emitting a `ValueError` traceback instead of a security
  message.** The item-2 guard is missing or misplaced. Recovery: restore the guard; the gate
  is still failing closed in the meantime.
* **`scaffold.py --manifest` output changes.** This proposal must not alter the published
  install contract. Any diff means `install_manifest()` was edited rather than merely read —
  stop and re-review.
* **The regression test goes green while a shipped file is unscanned.** The manifest itself
  has drifted from what the scaffold writes, which is a larger problem than this proposal and
  invalidates its central assumption.
* **Sequencing signal — a frozen-file HOLD.** `bootstrap/security_check.py` and
  `bootstrap/tests/test_security_lint.py` are both inside the gate-integrity manifest's
  **frozen set** (`bootstrap/*.py` and `bootstrap/tests/**/*.py`), where
  `bootstrap/security_check.py` is pinned as a Security-review blocker precisely because it
  is the single source of the scan targets and the allowlist. Modifying a frozen file during
  an active `gate-reanchor-preflight` batch window **HOLDs by default** — deliberately, since
  an unattended actor must not decide on its own that an edit to a gate is "merely
  strengthening." This proposal must therefore land *outside* that window, or as an explicit
  Maintainer-authorized HOLD resolution. If a HOLD fires unexpectedly during implementation,
  that is the signal to stop and sequence rather than to re-anchor. See *Proposal >
  Sequencing* for how this interacts with the cross-lineage file collisions and with the
  argument for landing ahead of the three proposals that modify the newly-scanned files.
* **A colliding sibling lands first against a shared file.** `SECURITY.md`,
  `bootstrap/SAFETY.md`, and `bootstrap/tests/test_security_lint.py` are each claimed by
  this proposal *and* by one Theme 3 sibling. If a sibling has landed, this proposal's
  quoted lines may have moved and its line citations gone stale. Recovery: re-read the
  three files before implementing and re-verify each quoted sentence — do not apply the
  edits from the proposal text alone.
