<!-- cairn-internal-ref-allow: doctrine/rationale.md doctrine/dual-review.md doctrine/proposals.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see AGENTS.md, "Where doctrine/ references resolve") -->

# The release security scan misses the two files an adopter runs every day

**Author**: Claude (Strategy)
**Model**: Claude Opus 5
**Date opened**: 2026-08-03
**Status**: reviewed
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

## Review -- Gemini Flash (External, Security Review) -- 2026-08-03

**Model**: Gemini 3.6 Flash (External, different-agent-type)
**Verdict**: SHIP (recommend ACCEPT; verified monotonicity, verified claim accuracy, 0 blocking findings)

### Steelman

This proposal corrects a genuine release-security gap in Cairn's `bootstrap/security_check.py`. Currently, `scan_targets()` manually enumerates `_MODULE_MAPPINGS` and `_ALWAYS_ON_MAPPINGS` but ignores `_SKILLS_MAPPINGS`. As a result, 2,502 physical LOC across `templates/skills/_lib/lifecycle.py` and `templates/skills/_lib/lifecycle_planner.py`—the very files executed most frequently by adopters at session start and end—are omitted from the Bandit release scan.

By deriving the verbatim Python scan target set from `install_manifest(modules=None)` as a **set union** (`set.add`/`set.update`) with the existing explicit loops, the proposal structurally guarantees monotonic non-decreasing coverage. It replaces a drift-prone manual enumeration with the same published catalog derivation used by `scaffold.py --manifest` and the SPDX licensing gate (`bootstrap/tests/test_notice_install.py`). Bandit execution over the newly included files yields zero MEDIUM or HIGH findings (16 LOW findings, 0 blocking), meaning coverage is extended with zero triage backlog.

### Concerns and Findings

* **[G1] (Verification of Set Monotonicity — Derivation Cannot Shrink Target Set)**
  * *Question:* Can the proposed derivation ever yield a SMALLER set than today's?
  * *Reasoning & Falsification:* The proposed implementation in `scan_targets()` initializes `targets: set[str] = set()`, populates it using the existing loops (`_MODULE_MAPPINGS`, `_ALWAYS_ON_MAPPINGS`, `scripts/`, `bootstrap/`, and `bootstrap/_scaffold/`), and then executes:
    ```python
    for src, _dst, verbatim in install_manifest(modules=None):
        if verbatim and src.endswith(".py"):
            targets.add(f"templates/{src}")
    ```
    Because Python `set.add()` and `set.update()` are strictly monotonic insertion operations and all existing loops are retained in full, $T_{\text{proposed}} = T_{\text{existing}} \cup T_{\text{manifest\_py}}$. The target set can never shrink.
    Furthermore, in `run_bandit()`, wrapping `scan_targets()` in a `try...except ValueError` block ensures that if `install_manifest` encounters any destination ownership conflict, the gate exits 1 immediately (`FAIL CLOSED`), preventing silent un-scanned releases.

* **[G2] (Verification of Author Claims a–e)**
  All five specific claims in the proposal were verified by direct execution using the canonical interpreter (`~/conda_envs/lhm/bin/python`, Python 3.13.13):
  * **Claim a:** `bootstrap/security_check.py` imports `_MODULE_MAPPINGS` and `_ALWAYS_ON_MAPPINGS` but NOT `_SKILLS_MAPPINGS`. **VERIFIED.**
  * **Claim b:** The scanned set contains 42 verbatim `.py` sources under `templates/`. **VERIFIED.**
  * **Claim c:** `_SKILLS_MAPPINGS` ships exactly 2 `.py` files totaling 2,502 physical LOC (`lifecycle.py`: 1,370 lines; `lifecycle_planner.py`: 1,132 lines). **VERIFIED.**
  * **Claim d:** `SECURITY.md` line 66 claims coverage of "the shipped Python surface". **VERIFIED.**
  * **Claim e:** Bandit scan over the two skills files is clean at MEDIUM+ (0 MEDIUM/HIGH findings, 16 LOW findings). **VERIFIED.**

* **[G3] (Zero Triage Backlog & Measured Zero-Cost Landing)**
  Executing `bandit` over `templates/skills/_lib/lifecycle.py` and `templates/skills/_lib/lifecycle_planner.py` confirms 16 LOW severity findings (all `B404`, `B603`, or `B607` subprocess-related warnings) and 0 MEDIUM or HIGH findings. Running a full simulated security check over all 74 targets yields 113 LOW findings and 0 blocking findings. Extending the scan set turns nothing red and adds no triage queue.

* **[G4] (Gate-Manifest & Frozen-File Batch Window)**
  `bootstrap/security_check.py` and `bootstrap/tests/test_security_lint.py` are both present in `frozen_files` within `bootstrap/tests/fixtures/gate_manifest.json`. Editing these files requires supervised re-anchoring via `bootstrap/REANCHOR_RUNBOOK.md` if an active manifest batch window is open, or landing outside the active window.

### Covered (Lenses Swept & Verbatim Executions)

Sweep executed on canonical interpreter `~/conda_envs/lhm/bin/python` (Python 3.13.13).

1. **Claim a — Import inspection in `bootstrap/security_check.py`:**
   * *Command:*
     ```bash
     grep -n "from bootstrap._scaffold.config import" bootstrap/security_check.py -A 4
     ```
   * *Output:*
     ```
     35:from bootstrap._scaffold.config import (  # noqa: E402  (trust anchor: narrowest owner, plan 0B.3 / Stage 4)
     36-    _ALWAYS_ON_MAPPINGS,
     37-    _MODULE_MAPPINGS,
     38-)
     ```

2. **Claim b — Current scanned template `.py` targets count:**
   * *Command:*
     ```bash
     ~/conda_envs/lhm/bin/python -c "from bootstrap.security_check import scan_targets; t = scan_targets(); print('Total targets:', len(t)); template_py = [x for x in t if x.startswith('templates/') and x.endswith('.py')]; print('Template .py targets:', len(template_py))"
     ```
   * *Output:*
     ```
     Total targets: 72
     Template .py targets: 42
     ```

3. **Claim c — `_SKILLS_MAPPINGS` `.py` files and physical LOC:**
   * *Command:*
     ```bash
     ~/conda_envs/lhm/bin/python -c "from bootstrap._scaffold.config import _SKILLS_MAPPINGS; py_files = [(src, dst, v) for src, dst, v in _SKILLS_MAPPINGS if src.endswith('.py')]; print('py_files:', py_files); import pathlib; locs = [len(pathlib.Path(f'templates/{src}').read_text().splitlines()) for src, dst, v in py_files]; print('LOCs per file:', locs); print('Total LOC:', sum(locs))"
     ```
   * *Output:*
     ```
     py_files: [('skills/_lib/lifecycle.py', 'tools/lifecycle.py', True), ('skills/_lib/lifecycle_planner.py', 'tools/lifecycle_planner.py', True)]
     LOCs per file: [1370, 1132]
     Total LOC: 2502
     ```

4. **Claim d — `SECURITY.md` line 66 quote check:**
   * *Command:*
     ```bash
     sed -n '66p' SECURITY.md
     ```
   * *Output:*
     ```
       unallowlisted MEDIUM+ finding over the shipped Python surface, and also
     ```

5. **Claim e — Bandit scan over skills files at MEDIUM+:**
   * *Command:*
     ```bash
     ~/conda_envs/lhm/bin/python -c "import subprocess, json; res = subprocess.run(['/Users/kendal30/conda_envs/lhm/bin/python', '-m', 'bandit', '-q', '-f', 'json', 'templates/skills/_lib/lifecycle.py', 'templates/skills/_lib/lifecycle_planner.py'], capture_output=True, text=True); data = json.loads(res.stdout); print('Total findings:', len(data['results'])); severities = [r['issue_severity'] for r in data['results']]; from collections import Counter; print('By severity:', dict(Counter(severities))); medium_plus = [r for r in data['results'] if r['issue_severity'] in ('MEDIUM', 'HIGH')]; print('MEDIUM+ count:', len(medium_plus))"
     ```
   * *Output:*
     ```
     Total findings: 16
     By severity: {'LOW': 16}
     MEDIUM+ count: 0
     ```

6. **Monotonicity & Target Extension Verification:**
   * *Command:*
     ```bash
     ~/conda_envs/lhm/bin/python -c "from bootstrap.security_check import scan_targets; current_targets = set(scan_targets()); from bootstrap._scaffold.install import install_manifest; proposed_targets = set(current_targets); [proposed_targets.add(f'templates/{src}') for src, _dst, verbatim in install_manifest(modules=None) if verbatim and src.endswith('.py')]; print('Current target count:', len(current_targets)); print('Proposed target count:', len(proposed_targets)); print('Is current subset of proposed:', current_targets.issubset(proposed_targets)); print('Added targets:', sorted(proposed_targets - current_targets)); print('Removed targets:', sorted(current_targets - proposed_targets))"
     ```
   * *Output:*
     ```
     Current target count: 72
     Proposed target count: 74
     Is current subset of proposed: True
     Added targets: ['templates/skills/_lib/lifecycle.py', 'templates/skills/_lib/lifecycle_planner.py']
     Removed targets: []
     ```

7. **Baseline Gate Execution:**
   * *Command:*
     ```bash
     ~/conda_envs/lhm/bin/python bootstrap/security_check.py
     ```
   * *Output:*
     ```
     check_cairn: OK -- 174 Markdown file(s) scanned; no issues; 48 external link(s) not probed.
     security_check: Bandit clean over 72 shipped file(s).
     security_check: PASS -- release security gate clean.
     ```

### Not Covered / Low Confidence (Negative Space)

* **Implementation Code Execution:** The proposal code changes have not been written to `bootstrap/security_check.py` or `bootstrap/tests/test_security_lint.py` yet; all verification was performed via inline simulation against current HEAD (`3292f21`).
* **Adopter `tools/*.py` Scans:** Adopter-side installed copies (`tools/lifecycle.py` and `tools/lifecycle_planner.py`) remain un-scanned by the release gate, which scans template sources `templates/skills/_lib/*.py`. As noted in the proposal, these files are byte-identical twins enforced by `test_every_self_hosted_twin_stays_byte_identical_to_its_source`, so coverage of template sources is equivalent.
* **Low-Severity Subprocess Hardening:** The 16 LOW findings (`B404`, `B603`, `B607`) in the skills files are not remediated by this proposal.

## Decision -- {{Maintainer}} -- {{YYYY-MM-DD}}

*(Awaiting the Maintainer. The proposal has cleared External Security Review. The Maintainer may accept the proposal to proceed with plan creation.)*

## Author addendum -- Claude (Strategy) -- 2026-08-03

### The regression guard this proposal leans on cannot fail, and the fix as drafted keeps it that way

A later audit (whether Cairn's practices could be spun out as a separate package --
verdict "could, narrowly; should not") re-read the machinery this proposal touches and
surfaced a defect in `bootstrap/tests/test_security_lint.py` itself. It is folded in here
because it bears directly on *item 3*, which the proposal above calls "the durable half".
The finding does not change item 1; it changes what item 3 has to do to be worth its name.

Everything below was re-measured at HEAD `5e6bf0c` under the canonical interpreter
`~/conda_envs/lhm/bin/python` (Python 3.13.13). No repository file was modified: the
proposed derivations were re-implemented in a scratch script that imports the real
`install_manifest` and the real registries.

#### The finding

`test_scan_targets_cover_all_shipped_scripts` at
`bootstrap/tests/test_security_lint.py:134` is the test this proposal identifies as "the
anti-drift assertion the test already claims to be". Its docstring makes that claim in its
own words:

> Coverage is derived from the source of truth, not a hand list: every
> verbatim .py shipped via \_MODULE\_MAPPINGS is in the scanned set (so a
> 9th reference script is auto-covered), and Cairn's dev executables are
> covered too. This is the anti-drift assertion (R2) -- the previous miss
> was a stale inventory + a non-recursing directory target.

The test builds its expected set, `shipped`, by walking `_MODULE_MAPPINGS` for verbatim
`.py` entries and joining `templates/modules/{src}`. That is, character for character, the
first loop inside `scan_targets()` at `bootstrap/security_check.py:64`. Confirmed by
execution rather than by reading:

```
identity: test's _MODULE_MAPPINGS is code's _MODULE_MAPPINGS -> True
len(test's `shipped`)                = 33
len(scan_targets())                  = 72
test's shipped == code's loop-1 output -> True
assertion `shipped - targets`        = []
```

So the assertion is `X - (X union ...) == set()`. It is empty for every possible content of
`_MODULE_MAPPINGS`, because the expectation and the value under test are computed from the
same object by the same expression. The test passes today; it would have passed on any day
since it was written; and it will pass on every future day on which that loop survives.
Meanwhile 2502 physical lines of shipped Python (`templates/skills/_lib/lifecycle.py` and
`templates/skills/_lib/lifecycle_planner.py`, counts as_of 2026-08-03) sit outside the scan
— the exact drift the docstring names.

Two terms, since this is the whole point. A test is an **oracle** plus a **subject**: the
oracle says what ought to be true, the subject is the code being checked. When the oracle is
computed from the same source the subject reads, the test can check that the subject
*consumes* that source correctly, but it can never check that the source is *complete*. A
gap in the source moves the oracle and the subject together, and the difference between them
stays empty. That is what happened here.

#### Being fair to the original test

The original work was a real fix for a real defect, and the instinct behind it was correct.

* It replaced a hand-maintained list of files. That list had gone stale, and deriving from a
  registry genuinely removed that failure mode.
* It is not inert. Three of its assertions can fail: the named-dev-file loop
  (`bootstrap/scaffold.py`, `scripts/check_cairn.py`, and the `content_scan.py` module
  source) would fail if any of those dropped out; the every-target-ends-in-`.py` assertion
  guards the non-recursing-directory footgun the docstring also names; and the
  `assert shipped, ...` non-emptiness guard fires if the registry empties entirely. Only the
  **coverage** assertion is the tautology.
* Its docstring is scoped honestly in one respect: it says "shipped via \_MODULE\_MAPPINGS",
  not "shipped". The overclaim is the definite article in "the source of truth" and the
  label "the anti-drift assertion", which together read as covering the shipped surface.

The bug is narrow and worth stating plainly: **the test derived from one registry, and by
the time it mattered there were three.** It did not derive from the wrong kind of thing; it
derived from too few of the right kind.

#### The unit of staleness moved up a level; it did not go away

This is the shape worth recording, because this proposal's item 3 repeats it.

| level | what the coverage set is derived from | what must be kept current by hand | outcome |
| --- | --- | --- | --- |
| 0 | a written-out list of files | the file list | went stale (the "previous miss") |
| 1 (2026-05-27) | one registry, `_MODULE_MAPPINGS` | which registries are consulted | went stale 5 days later |
| 2 (this proposal, as drafted) | `install_manifest()` | which registries `install_manifest` reads | same failure mode available |

At every level the derivation is honest and the residue is a hand-maintained list one
abstraction higher. Deriving is not the same as being independent.

#### A correction to *Context* above

The *Context* section says the always-on registry was fixed first and "the third registry
was then missed by the same mechanism the second one was". The chronology is the other way
round, and the corrected version is worse for the proposal's own argument, not better:

| date | commit | event |
| --- | --- | --- |
| 2026-05-27 | `a165026` | `test_scan_targets_cover_all_shipped_scripts` added -- "derive bandit-gate coverage from source of truth (R2)" |
| 2026-06-01 | `06345c5` | `_SKILLS_MAPPINGS` created; neither `scan_targets()` nor the new test extended |
| 2026-06-10 | `9bc1119` | `_ALWAYS_ON_MAPPINGS` created *and* wired into `scan_targets()` with its own coverage test |

So `_SKILLS_MAPPINGS` is the **second** registry, not the third, and it was missed twice:
once at creation, and again nine days later during a change whose own comment in
`bootstrap/_scaffold/config.py` describes itself as closing a *pre-existing* Bandit blind
spot for registries that ship `.py` outside `_MODULE_MAPPINGS`. That audit was looking
directly at this class and fixed one of the two members while the other sat in the same file
roughly a hundred lines above. And the anti-drift test was live and green throughout — it
was in place on the day the drift occurred and stayed green for 63 days
(2026-06-01 to 2026-08-03).

There is a counter-example in the tree that shows the repository already knows the stronger
shape. `test_always_on_executables_are_release_scan_targets` at
`bootstrap/tests/test_upgrade_side_door_parity.py:158` makes the same derived assertion but
adds `assert scanned == 9`. That pinned count is a hand-maintained number, which sounds like
the anti-pattern and is in fact the opposite: it **fails loudly when the registry grows**,
forcing a human to look. The weaker test is the one that named itself the anti-drift
assertion.

#### What this means for item 3 as drafted

Item 3 proposes to derive `shipped` from `install_manifest()` — and item 1 proposes to
derive `scan_targets()` from `install_manifest()`. Oracle and subject would again share a
source. The proposal states this outright in *Author-accounting* without registering it as a
cost: "Pinned by the extended coverage test, which derives its expectation the same way."
"The same way" is precisely the problem.

Simulating both proposed derivations side by side over four manifest states (verdicts
include the pre-existing `assert shipped, ...` non-emptiness guard):

| scenario | proposed `scan_targets()` | proposed `shipped` | `shipped - targets` | test verdict |
| --- | --- | --- | --- | --- |
| A. real manifest (status quo) | 44 | 44 | empty | GREEN — correct |
| B. skills entries never reach the manifest | 42 | 42 | empty | **GREEN — 2 shipped files unscanned** |
| C. a fifth registry ships a `.py` the manifest never sees | 42 | 42 | empty | **GREEN — same** |
| D. manifest emits nothing at all | 42 | 0 | empty | RED — caught by the non-emptiness guard |

Scenarios B and C are the historical defect replayed under the proposed fix, and the test
does not see them. An independent oracle does: globbing `.py` files physically present under
`templates/` returns, for scenario B, exactly
`['templates/skills/_lib/lifecycle.py', 'templates/skills/_lib/lifecycle_planner.py']`.

The proposal's *Signals the change is wrong* section already names this exact state — "the
regression test goes green while a shipped file is unscanned" — and grades it as an unlikely
symptom of manifest drift. It is not unlikely. Under the drafted test design it is the
guaranteed behaviour for any delivery path outside `install_manifest()`, which is the same
residual item 4 already concedes is open. The proposal saw the shape and mis-graded it.

The proposal *did* verify its extended assertion fails at HEAD (the AssertionError quoted
above item 3's paragraph). That check is real and it passed: the assertion is a valid
**one-shot migration check**. The error is treating a one-shot pass as evidence of a
standing guard. "Fails against the state being fixed" and "can fail against that state
recurring" are different properties, and only the first was tested.

#### What item 3 must assert instead

Three changes. The first two are the substance; the third is the criterion that would have
caught this.

1. **Split the test and stop overclaiming in the name.** The manifest-derived assertion is
   worth keeping — it pins that `scan_targets()` actually consumes the manifest, which is
   the deletion case (remove the union from item 1 and it goes red). But it is a
   *conformance* check, not an anti-drift check. Rename it to say so (e.g.
   `test_scan_targets_consume_the_full_install_manifest`) and rewrite the docstring to drop
   "the source of truth" and "the anti-drift assertion". A test that names a property it
   does not have is worse than a missing test, because it retires the question.

2. **Add one assertion whose oracle the code does not read.** The cheapest sufficient one is
   the filesystem: every `.py` physically present under `templates/` must appear in
   `scan_targets()`, modulo a declared table of exclusions each carrying a rationale. This is
   independent because all four registries source from under `templates/`, so a shipped
   Python file must exist there before any registry can reference it. Measured, the exclusion
   table is **empty today** — the on-disk set and the manifest-verbatim set are set-equal at
   44 files each, as_of 2026-08-03, `disk - manifest` and `manifest - disk` both empty. It
   therefore costs nothing to introduce and fires the moment the two disagree.

   This does **not** contradict *Alternatives considered*, which rejects globbing. That
   rejection is correct and stands — but it is about the **gate's scan set**, and the reason
   does not transfer to the **test's oracle**. The two want opposite defaults: the gate must
   scan what ships, so an authored-but-unwired template must not turn a release red; the test
   must notice when disk and manifest disagree, so an authored-but-unwired template *should*
   turn the dev suite red until someone records which it is. Same glob, different job.

3. **Upgrade item 4's census from a name-tripwire to a coverage assertion — with a caveat.**
   As drafted, item 4 fails when a new `*_MAPPINGS` symbol is absent from a small declared
   table; that is still a hand-maintained list, and its assertion is "the name is in my
   table", not "its files are scanned". The stronger version asserts, for every module-level
   `*_MAPPINGS` in `bootstrap/_scaffold/config.py`, that its verbatim `.py` entries are in
   `scan_targets()`. That is independent of `install_manifest()` (it reads the registries
   directly, and the manifest is downstream of them) and it would have failed at the pre-fix
   state. The caveat is real and should not be discovered during implementation: the four
   registries have three different element shapes — `_CORE_MAPPINGS` holds 2-tuples,
   `_SKILLS_MAPPINGS` 3-tuples, `_ALWAYS_ON_MAPPINGS` and `_MODULE_MAPPINGS` `InstallSpec`
   objects — and two different path joins (`templates/{src}` versus
   `templates/modules/{src}`). A generic census needs a normalizer, which is more work than
   the proposal's "cheap tripwire" framing suggests. Item 4 should therefore stay marked
   strikeable, with change 2 as the load-bearing guard.

**The acceptance criterion, stated generally.** A regression test is accepted only when its
author can name a *future* repository state in which it fails, and has run the perturbation
that produces that state. The concrete gate for this proposal's plan: perturb the delivery
path so the two skills tools stop being scanned, and confirm the new assertion goes red. As
drafted, item 3 does not (scenario B above). With change 2 it does.

#### What this addendum does not establish

* **It does not show a security finding was missed.** The Bandit measurement in *Context*
  stands as recorded (0 MEDIUM-or-higher over the two files); that measurement was not
  re-run for this addendum, and nothing here disputes it. The defect is in the guard, not in
  the code the guard failed to watch.
* **It does not invalidate item 1.** The union derivation in item 1 is a real coverage
  improvement and its "coverage can only grow" argument is unaffected. The criticism is
  confined to item 3.
* **It does not show the existing test is worthless.** Three of its assertions can fail, and
  the sibling always-on test with its pinned count is a genuine growth tripwire. What is
  hollow is one assertion — the coverage one — and the docstring's characterisation of it.
* **It does not make the filesystem oracle complete.** Change 2 is independent only while
  every registry sources from under `templates/`, which is true as_of 2026-08-03. A future
  registry sourcing from elsewhere escapes it, and that residual should be named in the test
  rather than assumed away — the same discipline item 4 already applies to its own residual.
* **It does not establish a doctrine violation, or trigger the rate-limit gate.** This is one
  test in one file. The *Doctrine-change rate-limit* section above is unchanged: still not
  engaged.

#### Consequences for the sections above

* *Proposal > item 3* is superseded by the three changes in this addendum. Item 1 and item 2
  stand as written.
* *Context* — the registry chronology is corrected above. `_SKILLS_MAPPINGS` is the second
  registry, not the third.
* *Tests required* gains: the split-and-rename of
  `test_scan_targets_cover_all_shipped_scripts`; the on-disk oracle assertion with its
  (currently empty) rationale table; and the perturbation check that the new assertion goes
  red when the skills tools leave the scanned set. The named-file assertion pinning both
  skills tools stays and is now the belt to the oracle's braces.
* *Author-accounting > Invariants* — the entry reading "Pinned by the extended coverage test,
  which derives its expectation the same way" should be read as *not* establishing what it
  claims; the `modules=None` argument is pinned by inspection of item 1's code, not by that
  test.
* *Sequencing* — this addendum enlarges, but does not change the shape of, the edit to
  `bootstrap/tests/test_security_lint.py`. That file is already recorded above as a
  file-level collision with the sibling `gate-claims-vs-enforcement` (its disposition A5
  corrects a docstring and a skip message in the same file) and as inside the
  `gate-reanchor-preflight` frozen set. Both constraints bind harder now: A5's docstring
  correction and change 1's docstring rewrite touch the same docstring, so those two are no
  longer merely file-level neighbours. Whichever lands second must re-read rather than apply
  its recorded text.

## Response -- Claude (author, to External Security Review) -- 2026-08-03

**Model**: Claude Opus 5. Proposal-Response grammar (no implementing commits exist).

**All four accepted; none disputed — and every one reproduced by execution before
disposal, not accepted on the reviewer's report.** This is an unusual review to answer,
because it raises no critique: G1–G4 are *verifications* and the verdict is SHIP. So the
Response has two jobs, and the second matters more than the first. The first is to re-run
the review rather than trust it. Done, and every figure reproduces under the canonical
interpreter `~/conda_envs/lhm/bin/python` (Python 3.13.13, Bandit 1.9.4): 72 → 74 targets
with zero removals; 16 LOW and 0 MEDIUM-or-higher over the two skills files; 113 LOW and 0
blocking over the extended set; the unmodified release gate green; and both gate files
present as literal keys in a 162-entry frozen set. The second job is to record what a SHIP
verdict over four verifications does **not** cover — which is most of *Proposal > item 3*.
That is the section below the bullets, and it is the part a Maintainer should read first.

* **[G1] accept -- reproduced, and the two premises it asserts without showing also hold.**
  The set algebra is right, and I re-derived it rather than reading it:
  `install_manifest(modules=None)` yields 44 verbatim `.py` sources under `templates/`, the
  current scan yields 42, `current.issubset(proposed)` is `True`, and `sorted(current -
  proposed)` is `[]` (as_of 2026-08-03). The review states two things it does not
  demonstrate, and both check out — the accumulator really is `targets: set[str] = set()`,
  and all five existing population steps are retained (the `_MODULE_MAPPINGS` loop, the
  `_ALWAYS_ON_MAPPINGS` loop, the non-recursive `scripts/` and `bootstrap/` globs, and the
  recursive `bootstrap/_scaffold/` glob), which is what makes a union a union; see
  `bootstrap/security_check.py:57` onward. One correction in the other direction, because
  the review over-credits me: it says the item-2 `try`/`except ValueError` ensures the gate
  exits 1, "preventing silent un-scanned releases." It prevents no silent release. `main()`
  wraps `run_bandit()` in no handler, so an uncaught `ValueError` already exits non-zero;
  the wrapper buys a security message instead of a traceback and nothing else — exactly what
  item 2 says of itself ("legibility, not new safety"). I decline the stronger reading.

  **What G1 does not establish.** Monotonicity is a property of the diff *as drafted*, not
  one anything in the tree enforces: no test goes red if a later author replaces the two
  explicit loops with the manifest derivation. *Author-accounting* already names this as the
  claim to attack; the review verified the current shape without noting that the guarantee
  is itself unguarded. I am not adding a guard for it here — that would be building
  something new — but note that the addendum's change 2 (the on-disk oracle over
  `templates/`) covers the case that would actually bite, since a shipped file dropped from
  the scan by such a refactor is a file present on disk and absent from `scan_targets()`.

* **[G2] accept -- all five reproduced verbatim.** Claims a–e were re-run, not read. (a) No
  `_SKILLS_MAPPINGS` symbol appears anywhere in `bootstrap/security_check.py`; its import
  block at `bootstrap/security_check.py:35` names only `_ALWAYS_ON_MAPPINGS` and
  `_MODULE_MAPPINGS`. (b) 72 targets, of which 42 start with `templates/` and end in `.py`,
  and zero contain `skills`. (c) 1370 + 1132 = 2502 physical lines. (d) `SECURITY.md:66`
  reads "unallowlisted MEDIUM+ finding over the shipped Python surface, and also". (e) 16
  LOW, 0 MEDIUM-or-higher, test ids `B404`×2, `B603`×10, `B607`×4. One clarification a
  reader will want on claim c, since "ships exactly two Python files" can be misread as
  "holds two entries": `_SKILLS_MAPPINGS` holds **five** entries as_of 2026-08-03. The other
  three are `templates/skills/_data/vendor_targets.yml` (verbatim, not `.py`) and the two
  substituted skill documents, of which `templates/skills/session-start/SKILL.md` is one.
  That is why both the `verbatim` and the `.endswith(".py")` guards are load-bearing, and it
  is the edge case the maintainer-direction note below bears on.

* **[G3] accept -- reproduced end to end, and the review supplies the one measurement the
  addendum declined to re-run.** Two-file scan: 16 findings, all LOW, 0 MEDIUM-or-higher.
  Full simulation over the 74-target set through the real `ALLOWLIST` and the real blocking
  filter: 113 findings, all LOW, 0 blocking. The unmodified release gate at HEAD prints
  `Bandit clean over 72 shipped file(s)` and `PASS`, matching the review's transcript
  exactly. Credit where it is owed: the addendum states plainly that it did *not* re-run the
  *Context* Bandit measurement and that nothing in it disputes that measurement — this review
  did re-run it, from a different starting point, and got the same numbers. That is a
  structurally independent confirmation the addendum could not give itself. The claim it
  supports stays narrow, though, and I will not let it read wider: **0 blocking is a
  snapshot as_of 2026-08-03, not a property of these files.** That is precisely why
  *Sequencing* argues FIRST — the zero is only free today.

* **[G4] accept -- the fact is verified; I narrow the remedy.** Both files are literal keys
  in the `frozen_files` map of `bootstrap/tests/fixtures/gate_manifest.json` (162 entries,
  as_of 2026-08-03), each pinned to a sha256, and editing either produces a
  `FROZEN-MODIFIED` HOLD. The review and the proposal describe one fact at two levels and
  neither is wrong: discovery is by the glob patterns `bootstrap/*.py` and
  `bootstrap/tests/**/*.py` in `bootstrap/tests/_gate_manifest.py:151`, and the committed
  artifact stores the resolved literal paths. Two refinements. **(i) This is live, not
  hypothetical.** The `gate-reanchor-preflight` plan is Status `executing` as_of 2026-08-03,
  so the window is open *now*; the proposal's *Net recommendation* fallback is the operative
  branch, not the preferred one, and "land FIRST" is currently a recommendation the schedule
  does not grant. **(ii) The two remedies are not peers.** G4 offers "supervised
  re-anchoring via `bootstrap/REANCHOR_RUNBOOK.md`" and "landing outside the active window"
  as alternatives. *Signals* holds the stricter line and I keep it: an unexpected HOLD is a
  signal to stop and sequence, never to re-anchor — re-anchoring is a Maintainer-supervised
  promotion, and an unattended actor must not decide on its own that an edit to a security
  gate is merely strengthening. For the record, G4 does not contradict this proposal's
  header: the runbook's AST-attestation half is scoped to `bootstrap/_scaffold/` (subject
  `bootstrap/_scaffold/__init__.py`, baseline
  `bootstrap/tests/fixtures/scaffold_ast_baseline.json`), which this proposal does not
  touch. Frozen-manifest and AST-baseline are different halves of the same runbook.

### What the SHIP verdict does not cover

The review predates the addendum, and that is chronology rather than negligence: `git log`
on this file gives `e336c71` (review appended) before `2dd1e27` (the addendum). The
reviewer could not have seen it. But the consequence holds regardless of fault, and it is
the most important sentence in this Response: **the SHIP verdict was rendered against
*Proposal > item 3* as originally drafted, and item 3 as originally drafted is exactly the
part the addendum shows cannot fail.** G1 and G2 bear on item 1, item 2 and the *Context*
measurements; G3 on the triage-cost claim; G4 on *Sequencing*. None of the four touches the
regression test or the item-4 census, and the review's own *Not Covered* section names
three unswept lenses, none of which is test design or oracle independence.

A term, since the whole point turns on it: a test's **oracle** is the statement of what
ought to be true, and its **subject** is the code being checked. When the oracle is computed
from the same object the subject reads, the difference between them is empty by
construction, and the test cannot fail. That is the defect the addendum records in
`test_scan_targets_cover_all_shipped_scripts` at `bootstrap/tests/test_security_lint.py:134`,
and item 3 as drafted would have reproduced it one abstraction higher.

So the record should show: the replacement for item 3 — the split-and-rename, the on-disk
oracle whose exclusion table is measured empty today, and the acceptance criterion that a
regression test is accepted only when its author has *run* the perturbation that makes it
fail — has been read by **no** External reviewer. This proposal already carries
`required(External, security lens)` at plan review; that is where it gets read. I am
recording the gap rather than letting a SHIP verdict over four verifications stand in for
it, because the alternative is exactly the failure the addendum is about: a green signal
retiring a question it never asked.

Two things I am *not* claiming. The addendum did not come out of this review, so the review
earns no credit for it; and the review is not at fault for missing it, because it did not
exist when the review was written. What the review does establish, and establishes well, is
that item 1's coverage fix is sound and costs nothing today — which is the half the addendum
explicitly says it does not dispute.

### Maintainer direction, 2026-08-03 — where it bears here

The Maintainer's direction that the default security stance must change for all
installations is a premise now, not an open question. It bears on exactly one sentence of
this proposal, and does not disturb the rest. *Author-accounting > Edge cases* routes
substituted `.md` skills sources away from the Bandit gate as "prose on the content-scanner
path". Verified as_of 2026-08-03: `_PRESETS` in `bootstrap/_scaffold/config.py` holds three
presets — `solo-greenfield`, `collaborative-team`, `high-rigor-legacy` — and **none** selects
`content-security`. For a default adoption that path is therefore not installed, and the
sentence must not be read as "covered by another gate". It is entitled to say only "outside
Layer-4 code", which is what it was written to say.

This changes nothing in item 1. Bandit coverage of verbatim `.py` is a different gate over
different files, and the two skill documents are substituted, so they sit outside this
proposal's scan set under any preset posture. The fix belongs where the preset → module
selection table lives, in `bootstrap/_scaffold/config.py`, and **not here**: this proposal
changes the coverage of one existing gate, and folding a shipped-posture change into it is
the bundling mistake that cost `identity-not-name` a REVISE/SPLIT verdict from its own
External Security Review earlier the same day. As_of 2026-08-03 no open proposal owns that
table; the nearest neighbours are `profile-parse-fail-open`, which already touches
`bootstrap/tests/test_presets.py` but is about fail-open *parsing* rather than preset
contents, and `content-scan-detectors`, which owns the scanner itself and not who installs
it. It needs its own proposal, and naming that is as far as this proposal's fence reaches.

**Status stays `reviewed`.** No accepted critique changes the proposal text: G1–G3 confirm
claims the proposal already makes, and G4's narrowing tightens a reading of a *Signals*
entry that *Signals* already states in the stricter form. The one substantive change to
this proposal — the supersession of item 3 — was appended and committed as the addendum
before this Response and is not a product of this review.

## Review -- Claude (Internal, same-agent-type; security lens) -- 2026-08-03

**Model**: Claude Opus 5.
**Verdict**: REVISE -- item 1 stands; the *Author-accounting* failure-mode table
contains one falsified guarantee; the addendum's replacement item 3 is
directionally right and its change 2 is a real (non-vacuous) guard, but it under-
asserts in the one direction that matters and leaves a second instance of the very
defect it names untouched.

All work below was done at HEAD `b67fabc` under the canonical interpreter
`~/conda_envs/lhm/bin/python` (Python 3.13.13, Bandit 1.9.4). **No repository file
was modified**: every "proposed" derivation was re-implemented in a throwaway script
that imports the real `scan_targets`, the real `install_manifest`, the real
`ALLOWLIST` and the real blocking filter. HEAD has moved twice since the proposal
(`3292f21`) and once since the addendum (`5e6bf0c`); I re-took the load-bearing
measurements rather than carrying them forward, and they all reproduce -- see
*Covered*.

### Steelman

The defect is real, the diagnosis is right, and the fix is the smallest shape that
fixes it. `scan_targets()` walks two of the delivery registries by hand; a third
ships 2502 physical lines of Python that an adopter executes at every session start
and end; the release gate has never read them. I reproduced that at HEAD: `disk -
scan_targets()` is exactly `['templates/skills/_lib/lifecycle.py',
'templates/skills/_lib/lifecycle_planner.py']`. Binding the scan set to
`install_manifest()` as a **union** with the retained loops makes "coverage cannot
shrink" a property you can check by reading three lines rather than by trusting a
measurement, and I confirmed no removals (72 -> 74, `current - proposed` empty). The
triage cost is genuinely zero today (113 findings over the extended set, all LOW, 0
blocking) -- reproduced from a cold start, with Bandit's own `errors` list empty, so
the zero is a real scan and not a skipped one.

The addendum is the best thing in this lifecycle. It caught its own proposal's
durable half being a tautology, stated the oracle/subject distinction cleanly,
corrected the *Context* chronology against its own interest, and named an acceptance
criterion -- *a regression test is accepted only when its author can name a future
state in which it fails, and has run the perturbation* -- that is worth more than
this proposal. I verified its central replacement is not itself hollow: the on-disk
oracle **fails at unmodified HEAD**, naming exactly the two files, so change 2 is a
guard and not a decoration. The Response's refusal of the reviewer's over-credit on
item 2 ("It prevents no silent release") is correct and I reproduced the reason.

What follows are things the External pass, the addendum and the Response all missed.

### Concerns

---

#### [I1] The failure-mode table asserts a fail-closed property the gate does not have: a shipped file that is missing from disk is silently skipped, and the gate prints "clean".

*Author-accounting > Failure modes* states, as a settled disposition:

> * A shipped file listed in the manifest is missing from disk → Bandit errors,
>   `rc` outside `{0, 1}` → **closed** by the pre-existing scanner-error branch.

That is false. Bandit records the failure in a JSON `errors` array, scans the rest,
and exits **0**:

```
$ cd <scratch>; echo 'x = 1' > ok.py
$ ~/conda_envs/lhm/bin/python -m bandit -q -f json ok.py /nonexistent/missing_file.py > out.json 2> err.txt; echo "RC=$?"
RC=0
--- stderr ---
(empty)
--- stdout head ---
{
  "errors": [
    {
      "filename": "/nonexistent/missing_file.py",
      "reason": "No such file or directory"
    }
  ],
```

`rc == 0` never reaches the `proc.returncode not in (0, 1)` branch at
`bootstrap/security_check.py:128`, and nothing in the module reads
`report["errors"]`. Driven through the **real** `run_bandit()`:

```
$ ~/conda_envs/lhm/bin/python -c "
import sys; sys.path.insert(0,'.')
import bootstrap.security_check as sc
real = sc.scan_targets
sc.scan_targets = lambda: sorted(set(real()) | {'templates/skills/_lib/GONE.py'})
print('run_bandit() returned:', sc.run_bandit())
"
security_check: Bandit clean over 73 shipped file(s).
run_bandit() returned: 0
```

The gate reports **73 shipped file(s)** and **PASS** while one of them was never
opened. The count in that message is the number of *requested* targets, not scanned
ones, so it cannot distinguish the two states -- which also means the *Examples /
smoke checks* line ("Expected: `PASS`, with the Bandit line reporting 74 files rather
than 72") is not evidence that 74 files were scanned.

The same hole swallows an unparseable file, which is the more likely real-world
trigger:

```
$ printf 'def f(:\n' > broken.py
$ ~/conda_envs/lhm/bin/python -m bandit -q -f json ok.py broken.py > o2.json 2> e2.txt; echo "RC=$?"
RC=0
$ ~/conda_envs/lhm/bin/python -c "import json;d=json.load(open('o2.json'));print(d['errors']);print('results:',len(d['results']))"
[{'filename': './broken.py', 'reason': 'syntax error while parsing AST from file'}]
results: 0
```

A shipped `.py` that does not parse is scanned-as-clean, silently, forever.

**Why this bears on *this* proposal and is not merely pre-existing.** It is
pre-existing -- item 1 does not create it, and item 1 still strictly increases
coverage. But (a) the proposal *newly asserts it is closed*, in the section a
Security reviewer is told to attack, so the record is wrong where it is most load-
bearing; and (b) item 1 changes the scan set from *a hand-picked walk of registries*
to *a declaration of what ships*, which makes manifest-vs-disk divergence the
governing risk -- and this fail-open is precisely what that divergence lands on. The
addendum **measured** both directions (`disk - manifest` and `manifest - disk` both
empty) but change 2 only **asserts** one of them.

*Cheapest fix, entirely inside the proposal's existing scope, no new mechanism:*
after `json.loads`, fail closed on a non-empty `report["errors"]` (verified present
and `[]` on a clean 74-target run -- see *Covered* item 3), and have change 2's
oracle assert the reverse direction (`manifest - disk` empty) alongside the forward
one. Both are one line.

---

#### [I2] The addendum found one instance of the tautology and stopped; a second instance of the identical shape sits in a file the proposal does not touch -- and it is the one whose *name* makes the "shipped surface" overclaim.

`bootstrap/tests/test_security_check.py:28` defines
`test_scan_targets_are_explicit_files_covering_shipped_surface`. Its always-on
coverage loop at `bootstrap/tests/test_security_check.py:43` is:

```
    for spec in _ALWAYS_ON_MAPPINGS:
        if spec.verbatim and spec.src.endswith(".py"):
            assert f"templates/modules/{spec.src}" in targets, spec.src
```

That is, character for character, the code's second loop at
`bootstrap/security_check.py:74`. Applying the addendum's own identity check:

```
$ ~/conda_envs/lhm/bin/python -c "
import sys; sys.path.insert(0,'.')
from bootstrap._scaffold.config import _ALWAYS_ON_MAPPINGS as CODE_REG
from bootstrap.security_check import scan_targets
expect    = {f'templates/modules/{s.src}' for s in CODE_REG if s.verbatim and s.src.endswith('.py')}
code_loop = {f'templates/modules/{s.src}' for s in CODE_REG if s.verbatim and s.src.endswith('.py')}
print('test expectation == code loop-2 output ->', expect == code_loop)
print('len(expect) =', len(expect))
print('expect - scan_targets() =', sorted(expect - set(scan_targets())))
"
test expectation == code loop-2 output -> True
len(expect) = 9
expect - scan_targets() = []
```

Same defect, same file family, and **content-invariant for every possible content of
`_ALWAYS_ON_MAPPINGS`** -- the addendum's exact criterion. The tree contains the
strong twin of this loop at `bootstrap/tests/test_upgrade_side_door_parity.py:168`,
which adds `assert scanned == 9` and is therefore a real growth tripwire; the
addendum praises that very line. The weak twin is the one that has not been found.

Three consequences the plan should absorb:

1. `bootstrap/tests/test_security_check.py` is **not in this proposal's *Touches*
   line**, so as scoped the plan will not reach it.
2. Its test *name* asserts "covering shipped surface" -- exactly the overclaim
   addendum change 1 exists to retire, one file over. After the fix it will still be
   green and still not cover the skills tools by any independent means.
3. It is **also frozen**: `bootstrap/tests/test_security_check.py` is a literal key
   in the frozen map (see *Covered* item 7), so absorbing it enlarges the sequencing
   footprint from two frozen files to three. Better to know that before the plan
   opens than during it.

---

#### [I3] "The manifest is the single chokepoint" is false today: a fifth delivery registry ships files that never reach `install_manifest()`, and its name does not match the pattern item 4's census keys on.

Item 4 says: *"Binding the scan to the manifest makes the manifest the single
chokepoint: anything in the manifest is scanned, with no list to extend. The residual
is a delivery path that never reaches the manifest at all -- which is the historical
`_ALWAYS_ON_MAPPINGS` side door."*

The residual is not historical. `_OPTIONAL_TEMPLATES` at
`bootstrap/_scaffold/config.py:249` is a live delivery registry, selected at install
time by `bootstrap/_scaffold/cli.py:371`, and it does not appear in the manifest:

```
$ ~/conda_envs/lhm/bin/python -c "
import sys; sys.path.insert(0,'.')
from bootstrap._scaffold.install import install_manifest
from bootstrap._scaffold.config import _OPTIONAL_TEMPLATES
m = install_manifest(modules=None)
print('manifest rows:', len(m))
print('optional/ rows in manifest:', [r for r in m if r[0].startswith('optional/')])
print('_OPTIONAL_TEMPLATES:', _OPTIONAL_TEMPLATES)
"
manifest rows: 95
optional/ rows in manifest: []
_OPTIONAL_TEMPLATES: (('optional/CONTRIBUTING.md', 'CONTRIBUTING.md', 'human_team', frozenset({'large-multi', 'small-multi'})),)
```

It is appended to the lockfile *separately from* the manifest, at
`bootstrap/_scaffold/install.py:1466`, with `verbatim` hard-coded `False`.

Three things follow, and they cut in different directions -- I am not claiming a live
security hole:

* **No live gap.** The single optional entry today is a `.md`, so nothing shipped as
  Python escapes the scan right now.
* **The census as specified would not catch it.** Item 4's tripwire fires on a
  module-level `*_MAPPINGS` symbol; the addendum's change 3 upgrade iterates "every
  module-level `*_MAPPINGS` in `bootstrap/_scaffold/config.py`". `_OPTIONAL_TEMPLATES`
  matches neither. So the mechanism the proposal offers for its own named residual is
  demonstrably already blind to a member of that residual, in the same file, today.
  This is not hypothetical drift; it is the drift, present at authoring time.
* **This is evidence *for* change 2.** The on-disk oracle would catch an optional
  `.py`, because `templates/optional/` is under `templates/`. The addendum's judgement
  that change 2 is the load-bearing guard and item 4 stays strikeable is, on this
  evidence, right -- more right than it knew.

*Recommendation:* keep item 4 strikeable, and if it survives, key the census on
"module-level tuple/dict of install mappings" by shape rather than by the `_MAPPINGS`
suffix -- or drop it and rely on change 2, which is the honest outcome this evidence
supports.

---

#### [I4] The new contract is *verbatim* `.py`, not *shipped* `.py` -- so `SECURITY.md`'s sentence does not "become true", it becomes true-as-of-today.

The proposal's *Documentation / doctrine surface* concludes: *"`SECURITY.md:66` needs
**no** change -- 'over the shipped Python surface' becomes true. That is the point:
the doctrine was right and the code was wrong."*

It becomes true only because the substituted-`.py` set is empty today:

```
$ ~/conda_envs/lhm/bin/python -c "
import sys; sys.path.insert(0,'.')
from bootstrap._scaffold.install import install_manifest
m = install_manifest(modules=None)
print('manifest verbatim .py   :', len([1 for s,d,v in m if v and s.endswith('.py')]))
print('manifest SUBSTITUTED .py:', [(s,d) for s,d,v in m if (not v) and s.endswith('.py')])
"
manifest verbatim .py   : 44
manifest SUBSTITUTED .py: []
```

The mechanism, though, forecloses nothing. `install_manifest` stamps
`verbatim=False` unconditionally on every core row at
`bootstrap/_scaffold/install.py:1374`:

```
        (src_rel, dst_rel, False) for src_rel, dst_rel in _CORE_MAPPINGS
```

and, per [I3], on every optional row too. So a `.py` added to `_CORE_MAPPINGS` or
`_OPTIONAL_TEMPLATES` -- a Python file with `{{token}}` slots, which is a perfectly
ordinary thing to want -- ships to every adoption as executable code and is filtered
out of the scan by the `verbatim` guard, while `SECURITY.md:66` and
`bootstrap/SAFETY.md:132` both continue to claim the whole shipped Python surface.

Sharper still: the proposal cites the SPDX licensing gate as the idiom it is
adopting, and the proposed code comment says *"Same derivation the SPDX licensing
gate already uses"*. It is not the same derivation. `_manifest_py_sources()` in
`bootstrap/tests/test_notice_install.py` has **no `verbatim` filter** at all, and
pins its count at `bootstrap/tests/test_notice_install.py:75`. On the one case where
the two differ -- a substituted `.py` -- the *licensing* gate is the stricter one,
which inverts the proposal's own framing of licensing as "the lower-stakes concern".

*This is a wording-and-record fix, not a design change.* Either say the contract is
"every file the scaffold ships **byte-for-byte** as Python" consistently (the
proposal's own one-line contract statement already says exactly that, correctly --
the drift is in the `SECURITY.md` disposition), or add substituted `.py` to change
2's oracle so the first one forces a decision instead of shipping unscanned.

---

#### [I5] Change 1's replacement name claims a property its assertion does not pin, with a measured margin of two files.

Addendum change 1 renames the test to something like
`test_scan_targets_consume_the_full_install_manifest` and justifies it: *"it pins
that `scan_targets()` actually consumes the manifest, which is the deletion case
(remove the union from item 1 and it goes red)."*

It goes red only because two manifest files are not reachable by the retained
explicit loops. Once a future author adds the third explicit loop -- the "minimal
one-liner" *Alternatives considered* rejects, but which item 1 keeps the door open to
by retaining the loops as a "defense-in-depth floor" -- the assertion goes green with
the manifest derivation deleted:

```
$ ~/conda_envs/lhm/bin/python <scratch/scenarios.py>
A post-fix (item1 as drafted)                            |targets|= 74  shipped-targets=[]  verdict=GREEN
B manifest loop DELETED                                  |targets|= 72  shipped-targets=['templates/skills/_lib/lifecycle.py', 'templates/skills/_lib/lifecycle_planner.py']  verdict=RED
C manifest loop DELETED + explicit _SKILLS_MAPPINGS loop |targets|= 74  shipped-targets=[]  verdict=GREEN

discriminating margin of the conformance assertion (files in manifest but not in the retained explicit loops):
['templates/skills/_lib/lifecycle.py', 'templates/skills/_lib/lifecycle_planner.py']
```

(The script rebuilds `scan_targets()` from the real registries and the real
`install_manifest`, toggling one loop at a time; it is reproduced in full in
*Covered* item 4.)

So the assertion pins "the union of all loops covers the manifest", not "`scan_targets()`
consumes the manifest". That is a weaker property than the proposed name states, in a
change whose stated purpose is *"A test that names a property it does not have is
worse than a missing test, because it retires the question."* The addendum's own
standard, applied one notch smaller, catches its own rename. Fix is a sentence in the
docstring, not a redesign -- say what it pins ("every manifest-verbatim `.py` is
scanned by *some* path") and stop implying which path.

---

#### [I6] Change 2's oracle has three boundaries the addendum does not name; one of them re-imports the hand-maintained-list failure mode the addendum condemns.

Change 2 is a genuine guard -- I verified it fails at unmodified HEAD (*Covered* item
2). These are hardening notes on the shape it should take in the plan, not objections
to it.

**(a) It is vacuous if `templates/` is absent or empty.** The existing test carries
`assert shipped, "expected at least one verbatim .py reference script"` at
`bootstrap/tests/test_security_lint.py:147` precisely for this. A glob has the same
need and the addendum proposes no equivalent:

```
$ ~/conda_envs/lhm/bin/python -c "
import pathlib
print('rglob over missing dir :', sorted(str(p) for p in pathlib.Path('t/nope').rglob('*.py')))
"
rglob over missing dir : []
```

Empty minus anything is empty; the oracle passes. Carry the non-emptiness guard over.

**(b) `Path.rglob` does not descend symlinked directories in Python 3.13, so
"physically present under `templates/`" is glob-default-scoped, not filesystem-
scoped.** Measured on the canonical interpreter, with a real symlinked directory
holding a `.py`:

```
$ ~/conda_envs/lhm/bin/python -c "
import pathlib
root = pathlib.Path('t/templates')
print('default   :', sorted(str(p) for p in root.rglob('*.py')))
print('recurse=T :', sorted(str(p) for p in root.rglob('*.py', recurse_symlinks=True)))
"
default   : ['t/templates/real/plain.py']
recurse=T : ['t/templates/linkdir/shipped.py', 't/templates/real/plain.py']
```

`find templates -type l` is empty today, so nothing escapes now. But the addendum's
independence argument is *"all four registries source from under `templates/`, so a
shipped Python file must exist there before any registry can reference it"* -- and
"exist there" and "be returned by the default `rglob`" are different sets. Make the
choice explicit and record it (there is a real argument for `False`: the engine has a
symlink/containment guard in `bootstrap/_scaffold/security.py` for the mirror-image
reason). An unrecorded default is how this class of thing goes stale.

**(c) The exclusion table is a hand-maintained, fail-open list -- the exact shape the
addendum's own level table condemns.** The addendum writes: *"At every level the
derivation is honest and the residue is a hand-maintained list one abstraction
higher."* Change 2 proposes *"modulo a declared table of exclusions each carrying a
rationale"*. An entry once added silences that file forever, and nothing goes red
when it should not have been there. The addendum itself supplies the antidote it
does not apply: it praises `assert scanned == 9` at
`bootstrap/tests/test_upgrade_side_door_parity.py:168` as the shape that *"fails
loudly when the registry grows, forcing a human to look"*, and the licensing gate
already does this at `bootstrap/tests/test_notice_install.py:75`. Pin a count
alongside the oracle. The table is measured empty today -- I reproduced 44/44/44 --
so pinning costs nothing and makes the first exclusion a decision rather than a
commit.

---

#### [I7] The perturbation that the addendum elevates to an acceptance criterion cannot be written the obvious way -- patching the registry where it is *defined* is a no-op.

The addendum's criterion is the best thing in the document: *"perturb the delivery
path so the two skills tools stop being scanned, and confirm the new assertion goes
red."* `bootstrap/_scaffold/install.py` binds the registry by value at import
(`from .config import ... _SKILLS_MAPPINGS ...`), so patching the owning module does
nothing:

```
$ ~/conda_envs/lhm/bin/python -c "
import sys; sys.path.insert(0,'.')
import bootstrap._scaffold.config as cfg
import bootstrap._scaffold.install as inst
n = lambda: len([1 for s,_d,v in inst.install_manifest(modules=None) if v and s.endswith('.py')])
print('baseline verbatim .py in manifest:', n())
cfg._SKILLS_MAPPINGS  = tuple(e for e in cfg._SKILLS_MAPPINGS  if not e[0].endswith('.py'))
print('after patching config._SKILLS_MAPPINGS :', n(), '<- perturbation had NO effect')
inst._SKILLS_MAPPINGS = tuple(e for e in inst._SKILLS_MAPPINGS if not e[0].endswith('.py'))
print('after patching install._SKILLS_MAPPINGS:', n(), '<- perturbation took effect')
"
baseline verbatim .py in manifest: 44
after patching config._SKILLS_MAPPINGS : 44 <- perturbation had NO effect
after patching install._SKILLS_MAPPINGS: 42 <- perturbation took effect
```

Severity is honest-low: a no-op perturbation leaves the oracle green, so the
perturbation check *fails visibly* rather than silently passing, and the author
notices. But the criterion's whole point is that authors have repeatedly mistaken "I
ran something and it did what I expected" for a guard, and this is a live trap on the
first step of executing it -- one the plan should name (`monkeypatch.setattr` targets
`bootstrap._scaffold.install`, not `bootstrap._scaffold.config`) rather than
rediscover. The repository already has doctrine for this shape:
`bootstrap/tests/test_scaffold_substrate.py` documents the patch-the-owning-module
rule for a different symbol.

---

#### [I8] Sequencing: the fact the Response builds its operative branch on has changed at HEAD. The frozen-file window is no longer open.

Not a defect in the proposal -- a stale premise that decides its schedule, worth
surfacing because the Maintainer will act on it. The Response states: *"**(i) This is
live, not hypothetical.** The `gate-reanchor-preflight` plan is Status `executing`
as_of 2026-08-03, so the window is open *now*; the proposal's *Net recommendation*
fallback is the operative branch, not the preferred one."*

At HEAD `b67fabc` that plan is archived:

```
$ git log --oneline -3
b67fabc dev/plans: archive gate-reanchor-preflight (trust root established)
af4b2ee gate-reanchor-preflight: record Chunk G + the changelog entry
e45e1fc gate: Phase 0 prerequisite commit -- pin the pre-flight checker (becomes P)
$ grep -n -m1 -i "^\*\*Status" dev/plans/archive/gate-reanchor-preflight.md
12:**Status**: archived
```

The frozen map itself is unchanged in kind but has grown, so the Response's count is
also stale within the same day:

```
$ ~/conda_envs/lhm/bin/python -c "
import json
fz = json.load(open('bootstrap/tests/fixtures/gate_manifest.json'))['frozen_files']
print('frozen entries:', len(fz))
for k in ('bootstrap/security_check.py','bootstrap/tests/test_security_lint.py','bootstrap/tests/test_security_check.py'):
    print(' ', k, 'frozen?', k in fz)
"
frozen entries: 164
  bootstrap/security_check.py frozen? True
  bootstrap/tests/test_security_lint.py frozen? True
  bootstrap/tests/test_security_check.py frozen? True
```

I am **not** concluding the HOLD no longer binds -- whether a frozen entry constrains
edits outside an active batch window is a Maintainer question and I did not find a
file that settles it. What I am reporting is that the premise the Response used to
pick the fallback branch ("Status `executing`, window open now") no longer holds at
HEAD, so *Sequencing*'s preferred position (land FIRST) may now be schedulable and
should be re-decided rather than inherited. Note also that per [I2] the plan may need
a third frozen file.

### Covered -- lenses swept, with the command that proves the sweep

1. **Ground truth re-taken at current HEAD (the proposal's figures are two commits
   old).**
   ```
   $ ~/conda_envs/lhm/bin/python -c "
   import sys; sys.path.insert(0,'.')
   from bootstrap.security_check import scan_targets
   from bootstrap._scaffold.install import install_manifest
   import pathlib
   t = set(scan_targets())
   m = {f'templates/{s}' for s,d,v in install_manifest(modules=None) if v and s.endswith('.py')}
   disk = {str(p.relative_to(pathlib.Path('.').resolve())) for p in (pathlib.Path('.').resolve()/'templates').rglob('*.py')}
   print('targets', len(t), 'manifest_py', len(m), 'disk_py', len(disk))
   print('disk - scan_targets:', sorted(disk-t))
   print('manifest - disk:', sorted(m-disk))
   "
   targets 72 manifest_py 44 disk_py 44
   disk - scan_targets: ['templates/skills/_lib/lifecycle.py', 'templates/skills/_lib/lifecycle_planner.py']
   manifest - disk: []
   ```
   `git ls-files templates | grep '\.py$' | wc -l` -> `44`, and `find templates -type
   l` -> empty, so on-disk == tracked == manifest-verbatim, 44 each, as_of 2026-08-03.

2. **Is change 2's on-disk oracle vacuous? No -- it fails at unmodified HEAD.** The
   `disk - scan_targets` line above *is* the oracle, and it is non-empty today,
   naming exactly the two files. Future states in which it fails: (i) today's
   pre-fix state; (ii) the union deleted from item 1; (iii) any registry -- including
   `_OPTIONAL_TEMPLATES`, per [I3] -- shipping a `.py` under `templates/` that the
   manifest never sees. This is the addendum's own criterion, met.

3. **The zero-triage claim, re-measured from cold, with the scan verified real.**
   ```
   base 72 extended 74 removals []
   bandit rc 1
   errors key: []
   severities: {'LOW': 113}
   BLOCKING: 0
   ```
   (real `scan_targets` + real `install_manifest` + real `_BLOCKING_SEVERITIES` +
   real `ALLOWLIST` + real `_rel`.) `errors key: []` is the check [I1] says the gate
   should be making: on this run nothing was skipped, so the 113/0 is a real scan.

4. **Set-monotonicity and the conformance test's discriminating margin** -- the
   scenario script behind [I5], run in full:
   ```
   A post-fix (item1 as drafted)                            |targets|= 74  shipped-targets=[]  verdict=GREEN
   B manifest loop DELETED                                  |targets|= 72  shipped-targets=[... 2 skills files ...]  verdict=RED
   C manifest loop DELETED + explicit _SKILLS_MAPPINGS loop |targets|= 74  shipped-targets=[]  verdict=GREEN
   ```

5. **Oracle/subject coupling, swept across every `scan_targets()` consumer, not just
   the one the addendum found.**
   ```
   $ grep -rn "scan_targets" . --exclude-dir=.git --exclude-dir=__pycache__
   ```
   Five consumers: `bootstrap/tests/test_security_lint.py` (the addendum's finding),
   `bootstrap/tests/test_security_check.py` (finding [I2]),
   `bootstrap/tests/test_upgrade_side_door_parity.py` (has the pinned count -- sound),
   `bootstrap/tests/test_scaffold_substrate.py` (named-literal assertions only --
   sound), and `bootstrap/security_check.py` itself. No test anywhere pins the target
   count at 72, so nothing breaks on 72 -> 74:
   `grep -rn "== 72\|72 shipped" bootstrap/tests/*.py bootstrap/*.py` -> no matches.

6. **Delivery paths that bypass the manifest** -- enumerated by reading every
   registry-shaped module-level symbol in `bootstrap/_scaffold/config.py`
   (`grep -n "_MAPPINGS" bootstrap/_scaffold/config.py`, plus a read of lines
   160-280 for the non-`_MAPPINGS` ones). Found `_OPTIONAL_TEMPLATES` -> [I3]; traced
   it through `bootstrap/_scaffold/cli.py:371` and `bootstrap/_scaffold/install.py:1466`.

7. **Frozen-set / sequencing state** -- re-read `frozen_files` at HEAD (164 entries),
   confirmed all three relevant files present, and confirmed the
   `gate-reanchor-preflight` plan is archived. See [I8].

8. **Boundaries.** Empty (`templates/` missing -> oracle empty, [I6a]); one/N>>1 (44
   -> 74 targets; Bandit invoked with 74 absolute paths, ~6 KB of argv, far under
   `ARG_MAX`); symlink ([I6b], measured); missing file ([I1], measured); unparseable
   file ([I1], measured); `None` (`modules=None` verified load-bearing -- it is the
   full-catalog branch at `bootstrap/_scaffold/install.py:1383`); non-ASCII -- all 44
   source paths are ASCII, so not exercised.

9. **A hypothesis I checked and it does NOT hold** (recorded so the next reviewer
   does not spend the time). I suspected item 1 widens the release gate's trust
   anchor, because `bootstrap/security_check.py:35` imports from the pure-stdlib leaf
   `bootstrap/_scaffold/config.py` under an explicit "trust anchor: narrowest owner"
   comment, and item 1 adds a dependency on the much larger
   `bootstrap/_scaffold/install.py`. Measured:
   ```
   loaded today          : 12
   ['bootstrap', 'bootstrap._scaffold', 'bootstrap._scaffold._guard', 'bootstrap._scaffold.cli', 'bootstrap._scaffold.config', 'bootstrap._scaffold.install', 'bootstrap._scaffold.lockfile', 'bootstrap._scaffold.merge', 'bootstrap._scaffold.security', 'bootstrap._scaffold.slotmerge', 'bootstrap._scaffold.upgrade', 'bootstrap.security_check']
   extra after importing install: []
   ```
   Importing `bootstrap.security_check` already executes the whole engine package, so
   the runtime trust surface is unchanged. I also checked the mechanical guard:
   `test_security_check_imports_trust_anchor_from_narrowest_owner` at
   `bootstrap/tests/test_config_module.py:50` constrains only the `ImportFrom` that
   names `_MODULE_MAPPINGS`, so a separate `install_manifest` import does not trip it.
   **No finding.**

10. **Spot-check of a Response claim** (per the brief's instruction to treat the
    Response with the same suspicion as the review). The Response asserts no preset
    selects `content-security`. Consistent: `_PRESETS` holds exactly
    `['collaborative-team', 'high-rigor-legacy', 'solo-greenfield']`, none carries a
    `modules` key, `_DEFAULT_ON_MODULES` is
    `('lifecycle-metrics', 'reflections', 'claim-check', 'fold-back-ledger', 'incident-trackers', 'documentation-plan')`,
    and `content-security` appears in `bootstrap/_scaffold/config.py` only as a
    `_MODULE_MAPPINGS` key. **No finding**, and it does not touch item 1 either way.

### Not covered / low confidence

* **I am the same agent type as the author, in a fresh session. This review carries
  NO cross-type independence.** Per this repository's own Dual-Review model that is
  the *Internal* floor, and it is the weaker tier by construction: I share the
  author's priors, its vocabulary, its blind spots and its taste in what counts as a
  sufficient argument. Two of my findings ([I2], [I5]) are literally the author's own
  criterion turned back on the author's own text -- which is the kind of finding a
  same-type reader is good at, and is *not* a substitute for a reader who does not
  share the frame. The proposal's `required(External, security lens)` at plan review
  is not discharged by this review and should not be treated as narrowed by it.
* **I did not write the change.** Hard constraint: not one byte into the repository.
  Every "post-fix" number is a simulation that imports the real objects, so it is
  faithful to the derivation but not to the diff. Nobody in this lifecycle has yet
  run the actual edited `bootstrap/security_check.py`, and the External pass says the
  same of itself.
* **I did not run the full suite** (`python -m pytest bootstrap/tests`), because
  doing so writes bytecode/artifacts and another session is live in this tree. So I
  have not shown the suite stays green -- only that no test pins the count at 72 and
  that the four other `scan_targets()` consumers' assertions survive 72 -> 74 by
  inspection plus targeted execution.
* **I did not audit the two newly-scanned files for security content.** Bandit's
  verdict on them (16 LOW, 0 MEDIUM+) has now been reproduced three times by three
  parties; a *human* read of 2502 lines of subprocess-shelling code that runs inside
  an adopter's git repository is a different exercise and nobody has done it. The
  proposal explicitly defers the four `B607` findings (`git` invoked by name, not
  absolute path) to a separate proposal; I did not evaluate whether that deferral is
  right.
* **I did not verify the sibling-collision table** beyond the three shared files
  named in it, and did not read `gate-claims-vs-enforcement` or `agent-context-scrub`
  to confirm their claimed line-level scopes. The addendum's warning that A5's
  docstring correction and change 1's docstring rewrite now touch the *same* docstring
  is un-rechecked by me.
* **I did not determine whether a frozen entry binds outside an active batch window.**
  [I8] reports the plan status only.
* **Untracked working-tree sensitivity of change 2 is unexplored.** The oracle globs
  disk, so a developer with a scratch `.py` under `templates/` gets a red security
  test. The addendum arguably *intends* this ("*should* turn the dev suite red until
  someone records which it is"), but I did not check how it interacts with parallel
  test runners or with a dirty tree in CI.

### Second-round recommendation

**Recommended -- one focused round, External, security lens, scoped to four items.**
Not a full re-review: item 1 is sound, has now been verified independently by three
readers, and I found nothing against it. The round should be scoped to what no
External reader has yet seen -- the replacement item 3 and its neighbours:

1. **[I1] must be answered before the Decision, whatever the disposition.** A
   Security-Review proposal whose *Author-accounting* asserts a fail-closed property
   the gate demonstrably lacks is the failure this proposal is about, one level up.
   The correction is cheap and in scope (fail on non-empty `report["errors"]`; assert
   the reverse direction in change 2's oracle). If the author would rather not touch
   `run_bandit()`, then the *claim* must come out of the table and become a named
   residual -- but it cannot stay as written.
2. **[I2] decides the plan's scope**, including whether a third frozen file is in it.
   Cheap to settle, expensive to discover mid-plan.
3. **[I3] and [I6c] should settle item 4's fate.** My reading of the evidence is that
   item 4 should be **struck** -- the proposal already marks it strikeable, and
   `_OPTIONAL_TEMPLATES` shows the name-keyed census is blind on the day it is
   written -- with change 2 plus a pinned count carrying the load instead.
4. **[I4], [I5], [I7] are record-and-wording corrections**, each one to three
   sentences, and should ride the same round rather than a separate one.

**And [I8] is for the Maintainer, not the reviewer**: the schedule premise has moved
at HEAD, so *Sequencing*'s preferred "land FIRST" should be re-decided rather than
inherited from a Response written against an open window.

A note on my own standing, since this review is about tests that overstate what they
prove. The strongest thing in this proposal is the addendum's acceptance criterion,
and I applied it: I did not accept change 2 because it looked independent, I ran the
state in which it fails. The weakest thing about this review is that I am the same
model as the author, and the criterion I just praised is one I inherited from him.
