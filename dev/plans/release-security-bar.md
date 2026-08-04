<!-- cairn-internal-ref-allow: doctrine/plans.md doctrine/dual-review.md doctrine/lifecycle.md doctrine/rationale.md doctrine/coordination.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see AGENTS.md, "Where doctrine/ references resolve") -->
<!-- cairn-accept: instruction-html-comment reason="The comment below explains to human readers and to the claim checker why three adopter-tree destination paths are deliberately non-resolving; it carries no directive to an agent and names no action to take." reviewer="Claude (author)" date=2026-08-04 -->
<!-- Three ADOPTER-TREE DESTINATION paths appear in the B6 reach table below.
     They are the paths those controls occupy in an INSTALLED target, and they
     do not resolve in Cairn's own tree precisely because no preset installs
     them -- which is the finding B6 records.  Their template sources resolve
     and are named in the table's footnote.  Carried forward from the source
     proposal, which registered the same three. -->
<!-- A FOURTH adopter-tree destination path, added by this plan: NC-A2's
     manifest-external leg cites `dev/modules/onboarding/high-rigor-legacy.md`,
     the destination `install_onboarding` writes when the high-rigor-legacy
     preset is selected.  Cairn self-hosts `collaborative-team`, so its own tree
     carries `dev/modules/onboarding/collaborative-team.md` (which resolves and
     is cited above) and never the high-rigor-legacy sibling.  The source,
     `templates/onboarding/high-rigor-legacy.md`, resolves and is cited
     throughout. -->
<!-- claim-check-allow: scripts/content_scan.py, scripts/run_security_audit.py, dev/modules/content-security.md, dev/modules/onboarding/high-rigor-legacy.md -->

# Plan: the v0.4.0 release security bar — the register, the deciders, and an audit that terminates

**Source proposal**: `release-security-bar` (accepted 2026-08-03; the Decision
commit is `3cda505`). It currently sits under `dev/proposals/` and moves to
`dev/proposals/archive/` when it archives.
**Status**: open
**Plan review**: required(**External**) — carried from the proposal header
(*"a bar that only its own author has read is a private checklist, not a shared
target"*) and re-stated by the Decision, which closes *"The plan carries
`required(External)` in its own right; this Decision does not discharge it."*
**No burndown chunk lands before the `## Plan review` section is in the tree.**
**Last update**: 2026-08-04
**Opened**: 2026-08-04

## Source proposal

`release-security-bar` settles one contract: **v0.4.0 ships when six named
properties each hold or carry a registered residual, judged against an
enumeration fixed before the judging starts.** The proposal supplies the six
properties (B1–B6), the decider for each, the scope fence they quantify over,
and the design rule that keeps the bar finite — *every item admits a fix or a
registered residual, never silence*.

It went through an External security review (Gemini Flash, security lens →
SHIP, one concern) and an author Response that homed that concern in the
`dev/PLANNING.md` deferred-follow-up ledger rather than in the proposal. The
Decision accepted it and recorded the residual in terms.

This plan executes that decision. It does not re-litigate the six items, the
fence, or the deciders. What it adds is the thing the proposal deliberately
deferred: **the register** — one table per item, one row per surface, each row
carrying the command that decided it and that command's output.

### Glossary — every term glossed on first use

The audience is a scientist who codes. This scope turns on two distinctions
that are easy to nod at and hard to hold.

* **Diagnostic** vs **specificational** check. A diagnostic asks *"is anything
  wrong?"* and returns findings; its list grows when someone looks harder, so
  it has no natural end. A specificational check asks *"does this satisfy the
  following stated properties?"* and returns per-property verdicts against a
  list fixed before the check ran; it ends when the list is exhausted. Every
  security gate in this tree is diagnostic. The bar is the first
  specificational one.
* **The register.** The committed tables in this plan. One per bar item. A row
  names a surface, the decider run against it, that run's output, and a verdict
  in {MET, MET-by-residual, in flight, NOT MET}.
* **Decider.** The command or inspection that settles one row. Never an
  argument; always something with an exit code or an output a second person can
  reproduce.
* **Negative control.** A perturbation of **the hazard** under which the decider
  must return the *other* verdict. A decider that returns MET for every possible
  tree decides nothing; a decider that returns NOT MET for every possible tree
  decides nothing either. Both directions are demonstrated per row.
* **Perturbing the hazard vs perturbing the check.** Editing a test's own body
  and watching it fail validates *the test harness*. Editing the registry, the
  document, or the shipped code path the test claims to guard, and watching the
  test fail, validates *the claim*. Only the second counts. This is B4's whole
  content and it is the standard every row in this plan is held to.
* **MET-by-residual.** The property does not hold, the mechanism's limit is
  real, and **the shipped documentation states plainly what the step does not
  establish**, with an owner and an expiry trigger recorded. This is branch (b)
  of the proposal's design rule. It is what makes the bar clearable; it is not a
  loophole, because what the bar forbids is a *document claiming a property the
  mechanism does not have*.
* **Set 1 / Set 2 / Set 3.** The three enumerable sets the fence quantifies
  over: the verification steps Cairn documents for an adopter to run; the code
  the scaffold installs into an adopter tree; the security claims Cairn's
  adopter-facing prose makes.
* **Fence.** The scope line: the bar quantifies over what a **v0.4.0 adopter is
  exposed to**, and nothing else. Cairn's own development tooling, the
  deliberation record, the case studies and the examples are outside it.

## What the Decision settled, and the two places the accepted text disagrees with itself

Stated up front so the Maintainer can strike a reading in one line rather than
discover it at code review. Where the Decision and earlier proposal text
disagree, **the Decision governs** — and it does, twice.

**1. D4 — the `verify_integrity` lockfile anchor.** The proposal's *Maintainer
decisions* section recommends *fix the verbatim subset for v0.4.0*. The
Decision does the opposite and says so in terms: the finding *"was already
outside this proposal's scope fences and remains so"*, and it routes the work
to `dev/PLANNING.md` > *Deferred follow-ups (durable home)* > **Security
apparatus** > *Install-integrity trust anchor*, naming the three questions a
successor must answer. **This plan follows the Decision.** Concretely: B1's
`verify_integrity` row closes as **MET-by-residual**, which under the design
rule obliges the *documentation* half — the two overstating sentences must be
corrected (Chunk F), or the row is NOT MET and the bar blocks.

That D4 was overridden is itself load-bearing evidence for the second reading:
accepting the proposal did **not** blanket-adopt every recommendation in the
*Maintainer decisions* section.

**2. D3 and the audit's home — where the end-of-line audit actually lands.**
The proposal calls the end-of-line audit *"that plan's own `## Plan review`
stage, tiered External"*. Two sentences later it says the audit triggers when
*"the plan enters `review`"* and that the block is held because *"the plan
cannot reach `archived` without a `## Code review` section, a `Follow-ups
migrated to:` block, and a fidelity sign-off"*. Those are different stages, and
only the second description matches the mechanism the proposal relies on.
Verified against the tree rather than assumed — `tools/lifecycle_planner.py`:

```
tools/lifecycle_planner.py:786   status in (executing, review, archived) and
                                 'Plan review: required' -> a '## Plan review'
                                 section must have landed  (review-BEFORE-implement)
tools/lifecycle_planner.py:792   status == 'archived' -> '## Code review' section
                    :798                              + 'Follow-ups migrated to:'
                    :803                              + loop-fidelity sign-off
```

The plan-review gate fires *before* implementation; the three archive
preconditions fire *at the end of the line*. So this plan carries **two**
External reads and they are different stages:

* **`## Plan review`** — `required(External)`, pre-implementation. It reviews
  the *register design*: is the enumeration right, are the deciders the right
  deciders, is a row's negative control actually a perturbation of the hazard.
  This is the tier the Decision left open.
* **The end-of-line audit** — lands as this plan's **`## Code review`**
  section, which is the stage `tools/lifecycle_planner.py:792` actually checks
  before `archived`, and therefore the one that structurally blocks the tag.
  Tiered External, **not run by the bar's author** (proposal D6).

*Where this reading could be wrong:* if the Maintainer intends exactly one
External read, the correct strike is to delete the pre-implementation
`## Plan review` requirement and let the audit be the only one — at the cost
that the register design is then never read by an outsider until after it is
built, which is the failure mode the proposal's *Why this tier* section argues
against. One line either way.

**D3 — what the audit blocks — is escalated, not assumed.** The proposal
recommends the audit block the tag **and** that the repo-public flip move after
the audit in the recorded launch sequence. Moving the flip re-orders
`dev/PLANNING.md`'s public-launch sequence, which is more than a precondition
clause. Given that D4 was overridden, this plan does not assume D3 was adopted.
It drafts the precondition clause **both ways** (see *The `dev/PLANNING.md` text
this plan returns*) and puts the choice on the Maintainer fence.

## Scope

Executes the accepted contract across nine chunks. **Eight of the nine touch
only `dev/plans/release-security-bar.md`** — this plan is the register's home,
and burning a row down means appending its table and its recorded runs here.
Exactly one chunk edits a file outside `dev/`.

**In scope:**

* The three set enumerations that make the fence countable (Chunk A).
* Six register tables, one per bar item, every row carrying a decider run and a
  negative control (Chunks B–G).
* **Two false reach passages in `templates/onboarding/high-rigor-legacy.md`** —
  the only unclaimed file the proposal's hand-off table leaves inside this bar's
  budget (Chunk B).
* The burndown roll-up, the staleness command, and the changelog line text
  (Chunk H).

**Out of scope, fenced explicitly:**

* **Fixing `bootstrap/verify_integrity.py`.** Per the Decision, this is a
  successor proposal with its own threat model and its own Security Review, and
  the file is claimed by `fork-advisory-semantics` besides. This plan
  *registers* the row; it changes no byte of that module.
* **The default-security-stance change** (proposal D5). B6 stops at stating each
  control's reach. Changing preset composition is an install-contract change and
  is its own proposal, sequenced after B6's table is committed.
* **Editing `doctrine/runtime-contract.md`, `SECURITY.md` or
  `bootstrap/SAFETY.md`.** All three are claimed by in-flight lineages
  (`gate-claims-vs-enforcement`, `agent-context-scrub`). The bar contributes the
  row and the evidence; the owning lineage lands the sentence. Chunk F carries
  the escape if a lineage stalls — and the escape is a Maintainer call, not an
  agent's.
* **Building any checker for the bar.** Rejected in the proposal on the standing
  direction *and* on merit: four of the six items are decided by a judgement over
  an enumeration, and a script that scored them would be a diagnostic, which is
  the thing that failed.
* **Adding a test that pins the B6 reach table.** Tempting and deliberately not
  done. A committed table kept in step with code by hand is precisely the
  *derived-list integrity for non-test lists* case the proposal names as a v0.5
  item; pinning it with a test here would smuggle that scope in. The table's
  staleness is instead held by Chunk H's staleness command. **A reviewer is
  invited to push on this** — it is the closest call in the plan.
* **The five v0.5 deferrals** listed in the proposal's *What is v0.5, said out
  loud*: token-substituted lockfile anchoring, non-test derived-list integrity,
  extending the bar to Cairn's own dev tooling, mutation testing as a standing
  mechanism, cryptographic attestation.

### Documentation / doctrine surface

* **Governing layer — none.** No `AGENTS.md` change and no `doctrine/` change.
  The proposal argues at length that six properties derived from one
  repository's five incidents are not yet a general method, and deliberately
  does **not** promote the bar into `doctrine/`. The doctrine-change rate-limit
  in `doctrine/rationale.md` is therefore not engaged, and this plan does not
  engage it either.
* **Deliberation layer** — this plan, its plan review, its code review, and the
  `dev/PLANNING.md` row-move that serializes the plan-open.
* **Adopter-installed prose — one file.**
  `templates/onboarding/high-rigor-legacy.md`, two passages (Chunk B). This is
  an *installed* document: verified below, `install_onboarding` copies
  `templates/onboarding/<preset>.md` into `<target>/dev/modules/onboarding/`.
* **Release-facing** — one `CHANGELOG.md > Unreleased > Added` line, whose text
  this plan **returns** rather than writes (serialized shared file).
* **Serialized shared files this plan does not edit in-agent** —
  `dev/PLANNING.md` (the plan-open row plus the precondition clause) and
  `CHANGELOG.md`. Both are returned as text under *The `dev/PLANNING.md` text
  this plan returns*.

<!-- cairn:slot documentation-tier-home -->
**Doc tier home rule** — route doc and doctrine changes by layer per
[`docs/DOCUMENTATION_PLAN.md`](../../docs/DOCUMENTATION_PLAN.md):
cross-cutting prescription → governing layer (`AGENTS.md`);
deliberation about what to build → deliberation layer (`dev/`);
description of the software as it is → descriptive layer (`docs/`). A
plan's *Scope* must name the doctrine-surface touched (or an explicit
"no doctrine surface").
<!-- cairn:end documentation-tier-home -->

### Gate accounting

* **No frozen file is edited.** Checked, not assumed: of every file this plan
  touches or contemplates touching, only `bootstrap/verify_integrity.py` is a
  key in the 164-entry `frozen_files` map in
  `bootstrap/tests/fixtures/gate_manifest.json` (`as_of 2026-08-04`), and this
  plan does not touch it. `templates/onboarding/high-rigor-legacy.md`,
  `SECURITY.md`, `doctrine/runtime-contract.md`, `bootstrap/SAFETY.md`,
  `CHANGELOG.md` and `dev/PLANNING.md` are all **not** frozen. **No supervised
  re-pin is engaged by this plan.**
* **No AST re-anchor.** No `bootstrap/_scaffold/` file is touched, so
  `bootstrap/tests/fixtures/scaffold_ast_baseline.json` is unaffected and
  `bootstrap/REANCHOR_RUNBOOK.md`'s attestation half is not engaged.
* **The install contract does not move.** This plan adds and removes no manifest
  row. `python bootstrap/scaffold.py --manifest` emits **95 data rows**,
  `as_of 2026-08-04`; expected diff at every chunk: empty.
* **Doc gates.** `python scripts/check_cairn.py` → OK over **180 Markdown
  files**, 68 external links not probed, `as_of 2026-08-04`. Chunk B edits a
  file under `templates/`, so `python scripts/quality_gate.py --sub neutrality`
  applies to it and its figure must not move.
* **Suite figure deliberately not asserted.** At the time of writing, other
  sessions hold uncommitted work in `bootstrap/_scaffold/install.py`,
  `config.py`, `lockfile.py`, `upgrade.py`, `bootstrap/verify_integrity.py`,
  three test modules, and nine other untracked plans under `dev/plans/`
  (`git status --short`, `as_of 2026-08-04`). A suite count taken over that tree
  would measure someone else's in-flight change. The implementing agent takes
  the baseline at its own start, against a clean tree, and records it in the
  first burndown commit body. **Every line citation in this plan is a HEAD
  `eacb7dd` citation for the same reason** — the working tree is not a stable
  reference this week, and two of the citations below already differ from it by
  one line.

### What is already true at HEAD — re-verified for this plan, not carried from the proposal

Every figure below was re-measured at HEAD `eacb7dd` under the canonical
interpreter (`~/conda_envs/lhm/bin/python3.13`, Python 3.13.13). **The
proposal's starting burndown was written before three implementing commits
landed on 2026-08-03**, so most of it is stale in the *good* direction. The
register starts from these figures, not from the proposal's table.

| Item | Proposal's starting count | Re-verified at HEAD `eacb7dd` |
| --- | --- | --- |
| B1 trust-material provenance | 5 rows: 1 MET, 3 in flight, 1 unowned | **3 MET, 1 in flight, 1 MET-by-residual pending its documentation half** |
| B2 answer-binding | 4 rows: 2 MET, 2 in flight | **4 MET** |
| B3 claim honesty (security subset) | ~14 rows: 0 MET, ~12 delegated, 2 unowned | unchanged: **0 MET**, 2 bar-contributed rows still falsified |
| B4 non-vacuous enforcers | denominator pending, 1 known-failing | the known-failing row is **fixed**; denominator still pending |
| B5 fail-closed direction | 5 rows: 1 MET, 4 in flight | **1 MET, 3 MET-by-residual, 1 in flight** |
| B6 stated reach | table measured, 2 false passages | table **reproduces exactly**; 2 false passages **still live** |

**What landed, and the check that says so.**

* **`release-authenticity` `b93f8e9`.** The documented tag bootstrap and
  `bootstrap/container/verify-ref.sh` both now bind the *signed* tag name to the
  name the caller asked about, and both take their roster by invocation from
  outside the candidate.
  * `bootstrap/PROVENANCE.md:202` — *"Bind the SIGNED name to the name you asked
    about"*; the comparison is at `bootstrap/PROVENANCE.md:204`; the three
    bootstrap properties are enumerated from `bootstrap/PROVENANCE.md:236`.
  * `bootstrap/container/verify-ref.sh:335` extracts the signed name
    header-bounded (so a `tag ` line in the attacker-controlled tag *message*
    cannot be read as the name); `bootstrap/container/verify-ref.sh:340` refuses
    on mismatch; `bootstrap/container/verify-ref.sh:354` pins the roster by `-c
    gpg.ssh.allowedSignersFile`, which outranks repository config.
  * Enforcer test module `bootstrap/tests/test_verify_ref.py` now exists (new in
    that commit).
* **`scan-coverage` `5c91c23`.** The vacuous *"anti-drift assertion"* is gone.
  `bootstrap/security_check.py:129` derives the scan set from
  `install_manifest(modules=None)`; `bootstrap/security_check.py:188` fails
  closed on Bandit's own `errors` array. `bootstrap/tests/test_security_lint.py`
  now carries `test_every_templates_py_on_disk_is_release_scanned` (line 229) —
  an oracle globbed from the working tree, which `scan_targets()` does not read
  — plus `test_the_on_disk_oracle_goes_red_when_a_registry_stops_delivering`
  (line 317), which is a perturbation-of-the-hazard test in the B4 sense.
* **`byline-classification` `1dabe4d`.** The widening fold is gone.
  `tools/lifecycle_planner.py:245` declares an explicit ASCII **allow-set** and
  `tools/lifecycle_planner.py:248`'s `_fold_word` keeps every non-ASCII
  character, so *"no letter and no digit, in any script, folds to nothing"* —
  the invariant that closes the homoglyph promotion. The `templates/` twin is
  byte-identical (both `f1552fc7…`, `shasum -a 256`, `as_of 2026-08-04`), and
  `bootstrap/tests/test_byline_identity.py` is the enforcer module.

**What did not land, verified at HEAD rather than inferred from a plan status.**
Three sibling plans still read `**Status**: open` while their implementing
commits are in the tree, so plan status is not a reliable signal this week. The
register cites the tree.

* `bootstrap/verify_integrity.py:47` is still `lock = read_lockfile(target)` —
  expected hashes come from **the candidate target's own**
  `dev/.cairn/cairn-lock.yml`. `CAIRN_ROOT` at
  `bootstrap/verify_integrity.py:34` only puts the engine on `sys.path`.
* `bootstrap/verify_integrity.py:118` still calls `forked_facade_findings(target,
  lock)` with no upstream argument, so the fork advisory's comparison bytes are
  target-supplied **at HEAD**. The working tree carries another session's
  uncommitted change to `upstream=trusted_upstream(CAIRN_ROOT)`; the register
  row stays *in flight* until that lands and its own code review confirms it.
* `bootstrap/_scaffold/config.py:43` still falls back to `_minimal_yaml_parse`
  when PyYAML is absent — the fail-open profile parse, owned by
  `profile-parse-fail-open`.
* `templates/onboarding/high-rigor-legacy.md:123` and
  `templates/onboarding/high-rigor-legacy.md:164` both still say the
  high-rigor-legacy profile's *content-security + security-review gates apply*.
  Re-measured below: `content-security` is selected by **0 of 3** presets.

### A finding this plan contributes before it starts — Set 2's enumeration under-counts

The proposal defines Set 2 as *"the code the scaffold installs into an adopter
tree — measured, not assumed: `install_manifest` for each shipped preset."*
Measured for this plan, that enumeration is **incomplete**, and the gap lands
squarely on the file Chunk B has to fix.

`bootstrap/_scaffold/install.py:1088` reads
`templates/onboarding/<preset_name>.md` and — per the docstring at
`bootstrap/_scaffold/install.py:982` — copies it to
`<target>/dev/modules/onboarding/<name>.md`, plus the two shared docs named at
`bootstrap/_scaffold/install.py:887` (`docs/agent-team-onboarding.md`,
`docs/dev-tour.md`). **None of those destinations is an `install_manifest`
row.** (Those three citations are **HEAD** line numbers; another session's
uncommitted edit to that module already shifts each by one in the working tree,
which is a concrete instance of the re-read rule below rather than an aside.)
Demonstrated in Cairn's own self-hosted tree, which was scaffolded with
`collaborative-team`:

```
$ ls dev/modules/onboarding/
agent-team-onboarding.md   collaborative-team.md   dev-tour.md

$ grep -c '"dst"' dev/.cairn/cairn-lock.yml          # 81 recorded destinations
$ grep -n 'dev/modules/onboarding' dev/.cairn/cairn-lock.yml   # no output

$ shasum -a 256 templates/onboarding/collaborative-team.md dev/modules/onboarding/collaborative-team.md
c829de48f3fbe9137155372ea75c7870558a9bba2430608529aa01ab99b2a9e8  templates/onboarding/collaborative-team.md
739bb0126b2f41d1a362b185009af5603234db11a34cadca7eca8e5fdcaf11a7  dev/modules/onboarding/collaborative-team.md
```

Three consequences, all `as_of 2026-08-04`:

1. **An adopter-installed document that makes a security-gate claim is outside
   the install manifest**, so `python bootstrap/scaffold.py --manifest` never
   lists it and any Set 2 enumeration built from the manifest alone misses it.
2. **It is also outside the integrity lockfile**, so
   `bootstrap/verify_integrity.py` never checks it — a post-install edit to an
   adopter's `dev/modules/onboarding/*.md` is invisible to the tamper check.
3. The divergent hashes above are **expected drift, not a defect**: Cairn's own
   tree was scaffolded 2026-06-12 and the template has moved since. They are
   shown because they *demonstrate* the file is uncovered — a lockfile-covered
   file could not diverge silently.

This is the `_OPTIONAL_TEMPLATES` shape one layer up, and it is exactly the
residual the proposal names as its largest: *"a verification step, a
normalization site, or a shipped control that nobody listed is invisible to the
bar."* Chunk A's enumeration therefore takes Set 2 as **`install_manifest` ∪ the
manifest-external installs**, and its negative control plants an item in the
manifest-external path specifically.

## Sequence

Chunk order is load-bearing in two places. **Chunk A is first** because every
other item quantifies over its enumerations — a register built before the fence
is countable is a diagnostic wearing a table. **Chunk G (B4) is last among the
register chunks** because its denominator *is* the set of enforcer tests the
other five chunks cite; running it earlier would fix a denominator that is still
moving.

```
0. plan-open   -- this plan; the dev/PLANNING.md row is RETURNED, not written  [commit pending]
   (plan review) -- required(External); NO burndown chunk before it lands
1. Chunk A -- the fence, enumerated and committed (Sets 1, 2, 3)               [commit pending]
2. Chunk B -- B6: reach measured, and the two false passages corrected         [commit pending]
3. Chunk C -- B1: trust-material provenance, 5 rows                            [commit pending]
4. Chunk D -- B2: answer-binding, 4 rows                                       [commit pending]
5. Chunk E -- B5: fail-closed direction, 5 rows                                [commit pending]
6. Chunk F -- B3: claim honesty (security subset)                              [commit pending]
7. Chunk G -- B4: non-vacuous enforcers, denominator from Chunks B-F           [commit pending]
8. Chunk H -- the burndown roll-up, the staleness command, the changelog text  [commit pending]
9. Chunk M -- MAINTAINER-ONLY: the fence                                       [not an agent's]
```

**Commit-approval note.** Chunks A and C–H touch only
`dev/plans/release-security-bar.md`, so each lands under the deliberation
carve-in without per-commit approval. **Chunk B does not** — it edits
`templates/onboarding/high-rigor-legacy.md`, which re-triggers the approval
gate. Pushing needs approval in every case.

---

### Chunk A — the fence, enumerated and committed

The proposal's second finiteness argument: *"the bar does not quantify over 'the
repository', it quantifies over a list you can count."* This chunk produces the
list. Nothing else in the plan is valid before it lands.

| # | File | Change |
|---|------|--------|
| A1 | `dev/plans/release-security-bar.md` | **Set 1 table** — every verification step Cairn documents for an adopter to run, one row each: the step, the `<file>:<line>` where it is documented, whether it is a command or a procedure, and the bar items that quantify over it. Built by a recorded sweep over `SECURITY.md`, `bootstrap/PROVENANCE.md`, `bootstrap/SAFETY.md`, `bootstrap/BOOTSTRAP.md`, `bootstrap/UPGRADE.md`, `bootstrap/container/recipe.md`, `docs/quickstart.md`, and every Markdown destination in Set 2. The sweep's exact command is committed beside the table. |
| A2 | `dev/plans/release-security-bar.md` | **Set 2 table** — `install_manifest(modules=expand_preset(load_config(<preset>)))` per shipped preset, **unioned with the manifest-external installs** measured above (`install_onboarding` writes D and E). The row count per preset is a dated snapshot; the union is the load-bearing part. |
| A3 | `dev/plans/release-security-bar.md` | **Set 3 table** — every sentence in adopter-facing prose that asserts a security control is applied. Built by a recorded pattern sweep (the pattern list is committed, not summarized) over Cairn's adopter-facing docs plus every Markdown destination in Set 2. |
| A4 | `dev/plans/release-security-bar.md` | **The stated residual**, written as a finding rather than a caveat: the deliberately-constructed *miss* from A3's negative control, plus the sentence naming what the enumeration therefore does not establish. |

**Acceptance criteria — Chunk A.**

* Three tables committed, each with the exact command that produced it, each
  re-runnable by a reviewer without modifying the repository.
* **Negative control NC-A1 (Set 1 can see a planted step), RUN.** In a scratch
  copy of the tree outside the repository, add a Markdown file documenting a
  fabricated verification step in the sweep's idiom; re-run A1's sweep against
  the scratch root; confirm the planted step appears. Then re-run against the
  real tree and confirm the committed table is reproduced byte-for-byte. A sweep
  that cannot see a planted step enumerates nothing.
* **Negative control NC-A2 (Set 2 sees the manifest-external path), RUN.** Two
  legs, because the two delivery paths fail independently.
  * *Manifest leg:* in a scratch **process**, monkeypatch
    `bootstrap._scaffold.install`'s registry so one preset gains a row; confirm
    A2's enumeration reports it. Patch the module that *binds* the registry, not
    the module that defines it — `bootstrap/_scaffold/install.py` binds by value
    at import, and patching `bootstrap._scaffold.config` is a silent no-op. This
    trap is recorded in `dev/plans/scan-coverage.md` and cost that plan a whole
    perturbation to characterize.
  * *Manifest-external leg:* scaffold a `high-rigor-legacy` install into a
    scratch target; confirm A2's enumeration reports
    `dev/modules/onboarding/high-rigor-legacy.md` and the two shared docs, and
    that `scaffold.py --manifest` does **not**. If the enumeration reports the
    same set as the manifest, A2 has silently reverted to the proposal's
    under-counting definition.
* **Negative control NC-A3 (Set 3 both catches and misses), RUN.** Write two
  scratch claim sentences under the sweep root: one phrased in the idiom the
  pattern list targets (must be caught) and one phrased so the pattern list
  misses it (must be missed, and the missing form is quoted in A4). The second
  leg is not a failure of the chunk — it is the evidence for the residual, and a
  chunk that reports only the catch is hiding the residual it is required to
  state.
* **Channel note.** Set 2's oracle for the manifest-external leg is a real
  scaffold run into a scratch target — a different program's output, not a
  reading of the registry the enumeration walks.
* **No repository file is modified.** Every leg runs against a scratch copy or a
  scratch process. `git status --short` unchanged at chunk end.

---

### Chunk B — B6: reach measured, and the two false passages corrected

**Property (proposal B6).** For each security control Cairn ships, a committed
table states whether it reaches an install from each named preset, and no Cairn
document claims reach a control does not have.

**The table, re-measured at HEAD `eacb7dd` for this plan** — eight lines against
the real engine (`load_config` → `expand_preset` → `install_manifest` per
preset). It reproduces the proposal's table exactly. Rows are **adopter-tree
destination paths** — where the control lands in an installed target:

| Control (installed path) | solo-greenfield | collaborative-team | high-rigor-legacy |
| --- | --- | --- | --- |
| `scripts/content_scan.py` | — | — | — |
| `scripts/run_security_audit.py` | — | — | — |
| `dev/modules/content-security.md` | — | — | — |
| `dev/modules/security-review.md` | — | — | yes |
| `scripts/link_check.py` | — | yes | yes |
| `tools/intent.py` | — | yes | yes |
| `scripts/claim_check.py` | yes | yes | yes |
| `scripts/foldback_export_scan.py` | yes | yes | yes |
| `tools/lifecycle_planner.py` | yes | yes | yes |

The first three rows do not resolve in Cairn's own tree, which is the finding
rather than a citation error: no preset installs them, so no self-hosted copy
exists. Their sources are `templates/modules/team-gated/content_scan.py`,
`templates/modules/team-gated/run_security_audit.py`, and
`templates/modules/team-gated/content-security.md`. Independent cross-check on
the module side, re-run for this plan:

```
solo-greenfield     content-security in modules: False   (6 modules,  59 manifest rows)
collaborative-team  content-security in modules: False   (11 modules, 77 manifest rows)
high-rigor-legacy   content-security in modules: False   (14 modules, 80 manifest rows)
```

| # | File | Change |
|---|------|--------|
| B1 | `dev/plans/release-security-bar.md` | The reach table above, committed as the B6 register with its producing command, plus a fourth column for the manifest-external installs from Chunk A. |
| B2 | `templates/onboarding/high-rigor-legacy.md` | The passage at `templates/onboarding/high-rigor-legacy.md:123` — *"the high-rigor-legacy profile's content-security + security-review gates apply to the drafted filing body before it leaves the deployment"* — corrected to name only the gate the preset actually installs (`security-review`, measured `yes` above) and to phrase the scanner as an action the adopter runs rather than a standing gate. **Re-read the file before editing**; a sibling lineage may have moved the line. |
| B3 | `templates/onboarding/high-rigor-legacy.md` | The same sentence at `templates/onboarding/high-rigor-legacy.md:164`, in the Row 4 active-surfacing prompt. Same correction. Note the trailing sentence there — *"Run the scrub scanner on the draft explicitly before submitting"* — is already in the correct imperative form and is **retained**, because it is the shape B3 asks for and the shape B2's correction should converge on. |
| B4 | `dev/plans/release-security-bar.md` | The negative and positive results of the claim-vs-table check (below), recorded as the row's evidence. |

**What B2/B3 must not do.** The corrected wording must not presume the
default-security-stance change. B6 states reach; it does not decide what the
defaults *should* be (proposal D5). A correction that reads "…once you install
the content-security module" is fine; one that reads "…which your profile
installs" is a new claim about a stance nobody has decided.

**Acceptance criteria — Chunk B.**

* The reach table is committed with its producing command and reproduces on
  re-run.
* **Negative control NC-B1 (the measurement reads preset composition), RUN.** In
  a scratch copy of `bootstrap/profiles/high-rigor-legacy.yml` outside the
  repository, add `content-security` to the preset's module selection; re-run
  the eight-line measurement against the scratch config; confirm the three
  `content_scan` rows flip from `—` to `yes` for that column only. Restore by
  discarding the scratch copy — **`bootstrap/profiles/` is never edited in the
  working tree**. A measurement whose table cannot flip is reading something
  other than preset composition.
* **Negative control NC-B2 (the claim check flags the live text), RUN.** Run the
  claim-vs-table check against `git show HEAD:templates/onboarding/high-rigor-legacy.md`
  and confirm it reports **exactly 2** false reach claims; run it against the
  corrected file and confirm **0**. This perturbs the hazard — the document text
  — in the only direction that matters, and it fixes the count so a third
  passage appearing later is a visible change rather than a silent one.
* **The other two onboarding sources are checked, not assumed.** Verified for
  this plan: `templates/onboarding/solo-greenfield.md` and
  `templates/onboarding/collaborative-team.md` contain no content-security or
  scanner reach claim, and neither do `docs/agent-team-onboarding.md` or
  `docs/dev-tour.md` — the two shared docs the manifest-external path also
  installs. Recorded so "two passages" is a measured count and not a carried one.
* `python scripts/check_cairn.py` → OK, **≥180** Markdown files.
* `python scripts/quality_gate.py --sub neutrality` → figure unchanged;
  `templates/` is inside its scan roots.
* `python scripts/claim_check.py templates/onboarding/high-rigor-legacy.md` —
  one file per invocation.
* `python bootstrap/scaffold.py --manifest` → **unchanged**, 95 data rows. This
  chunk changes a file's *content*, never the set of installed files.

---

### Chunk C — B1: trust material arrives from outside the artifact under verification

**Property (proposal B1).** For every verification step in Set 1, each input the
step's *conclusion depends on* either (a) arrives through a channel independent
of the artifact under verification, or (b) is named in the step's own shipped
documentation as artifact-supplied, together with the sentence saying what the
step therefore does not establish.

**Where the tree stands, re-verified at HEAD `eacb7dd`.**

| Step | Trust material | Arrival channel | Row |
| --- | --- | --- | --- |
| The gate pre-flight signature check | allowed-signers roster | trusted anchor object, outside the candidate — `anchored_roster` at `bootstrap/tests/_gate_preflight.py:597` | **MET** (the exemplar; fixed in `0c6d9de`) |
| The documented tag-verification bootstrap | signer roster | out-of-band; adopter-typed, supplied by invocation — `bootstrap/PROVENANCE.md:236` | **MET** — landed `b93f8e9` |
| `bootstrap/container/verify-ref.sh` | signer roster | pinned by invocation at `bootstrap/container/verify-ref.sh:354`, verified in a workspace the script created | **MET** — landed `b93f8e9` |
| The fork advisory | comparison bytes | target-supplied at HEAD (`bootstrap/verify_integrity.py:118`); caller-supplied in the uncommitted `fork-advisory-semantics` work | **in flight** |
| `bootstrap/verify_integrity.py` | expected SHA-256 values | the target's own `dev/.cairn/cairn-lock.yml` (`bootstrap/verify_integrity.py:47`) | **MET-by-residual, conditional on Chunk F** |

| # | File | Change |
|---|------|--------|
| C1 | `dev/plans/release-security-bar.md` | The table above as the B1 register, one sub-section per row carrying the falsifying run, its exit code, its output, and its negative control. |
| C2 | `dev/plans/release-security-bar.md` | The `verify_integrity` row written out in full as the plan's **worked example of MET-by-residual**: the reproduction, the ledger entry that owns it (`dev/PLANNING.md` > *Deferred follow-ups* > **Security apparatus** > *Install-integrity trust anchor*), the revival condition, and the explicit statement that the row is **NOT MET until Chunk F lands the documentation half**. |

**Deciders, each with its negative control. Every leg is RUN, and its output is
pasted into the register.**

* **Rows 2 and 3 (the tag bootstrap and `verify-ref.sh`) — the attacker-roster
  construction.** In a scratch repository outside this tree: generate a throwaway
  signing key, commit an attacker-authored roster *inside* the tagged tree, sign
  a tag with the attacker key, and run the documented bootstrap. Expected:
  **REFUSED**, because the roster is supplied by invocation and never read from
  the candidate.
  * *Negative control:* run the identical construction with the genuine
    throwaway roster supplied by invocation, and confirm **PROVENANCED**. A
    decider that refuses every input decides nothing. Both verdicts from one
    harness is the evidence.
  * *Judge the exit code, never the text.* `bootstrap/container/verify-ref.sh`
    records the measurement in-line: git prints a line beginning `Good "git"
    signature` on wrong-roster and empty-roster refusals too. The register's
    evidence column carries exit codes.
* **Row 4 (the fork advisory) — not decided by this plan.** The row records the
  HEAD call site, names the owning lineage, and states the condition under which
  it flips: the `fork-advisory-semantics` change lands **and** its own code
  review confirms the comparison bytes come from the caller's checkout. The bar
  does not mark a row MET on another lineage's uncommitted working tree.
* **Row 5 (`verify_integrity`) — the coordinated lockfile tamper.** Scaffold a
  `solo-greenfield` install into a scratch target outside the tree; append a
  marker line to a shipped `.py`; rewrite that one record's `hash` in the
  target's own lockfile; re-run the verifier. Expected: **exit 0, `OK`**, with
  the marker line present — reproducing the finding against the shipped module
  at HEAD.
  * *Negative control:* the **same** tamper *without* rewriting the lockfile
    record must produce exit 1 and `modified (hash mismatch)`. This is the leg
    that proves the verifier is not simply always-OK, and therefore that the
    finding is about the lockfile's *location* and nothing else.
  * *Second negative control, closing the proposal's own known omission.* The
    proposal states plainly that the finding was measured on **one** record type
    (`verbatim: true`, a `.py` file) in **one** preset, and that *"the mechanism
    is record-type-independent by inspection … but I have not run it, and the
    register should."* The register runs it: repeat the tamper against a
    token-substituted record and against a `living_state` record, and record what
    each does. A `living_state` record is expected to behave differently — it is
    excluded from the tamper check by design — and recording that difference is
    part of the row, not an exception to it.
* **Maintainer fence.** Every signature leg uses a throwaway key generated in a
  scratch directory. **No decider run touches `dev/.cairn/allowed_signers`, the
  Maintainer's signing key, or `refs/cairn/gate-anchor`.**

**Acceptance criteria — Chunk C.** Five rows, each with a falsifying run **and**
its negative control, both with recorded output; the `verify_integrity` row
explicitly blocked on Chunk F; no repository file modified; `git status --short`
unchanged at chunk end.

---

### Chunk D — B2: the answer names the thing that was asked about

**Property (proposal B2).** Any shipped check that reports a verdict about a
*named* identity, version, ref, or file set binds its verdict to that name, and
its output names what it actually verified.

B2 is B1's mirror and the distinction is load-bearing: in the tag-substitution
case the roster arrived correctly out-of-band and the signature was genuinely the
maintainer's — the defect was that the answer concerned a different object than
the question.

**Where the tree stands, re-verified at HEAD `eacb7dd`.**

| Check | Verdict is about | Bound to the name? | Row |
| --- | --- | --- | --- |
| The documented tag bootstrap | a release version | **yes** — `bootstrap/PROVENANCE.md:204` compares the signed name to the name asked for | **MET** — landed `b93f8e9` |
| `bootstrap/container/verify-ref.sh` | a release version | **yes** — `bootstrap/container/verify-ref.sh:340`, over a header-bounded extraction (line 335) so a `tag ` line in the attacker-controlled tag *message* cannot be read as the name | **MET** — landed `b93f8e9` |
| `bootstrap/verify_integrity.py` | "the recorded install" | yes, and it says so | **MET** — the wording at `SECURITY.md:47` (*"confirm the installed tree still matches its recorded install"*) is careful and true as far as B2 goes |
| `tools/lifecycle_planner.py` byline classifier | document structure, not identity | yes | **MET** |

| # | File | Change |
|---|------|--------|
| D1 | `dev/plans/release-security-bar.md` | The table above as the B2 register, with the substitution run recorded per row. |

**Deciders, each with its negative control.**

* **Rows 1 and 2 — the substitution run.** In a scratch repository: create two
  genuine signed tags with the same throwaway key (`v0.3.0` and `v0.5.0`), then
  repoint `refs/tags/v0.5.0` at the `v0.3.0` tag object. Run the documented
  bootstrap and `verify-ref.sh` asking for `v0.5.0`. Expected: **REFUSED**, with
  the output naming the signed name it found.
  * *Negative control:* ask for `v0.3.0` against the same substituted repository
    — the un-substituted question — and confirm **PROVENANCED**. The pair is the
    claim: the check discriminates the *question*, not the repository.
  * *Header-bounding control, because line 335 exists for a reason:* create a
    tag whose **message body** contains a line `tag v0.5.0`, ask for `v0.5.0`,
    and confirm the check still refuses. Perturbing the attacker-controlled free
    text is the hazard here; perturbing the awk script would only test awk.
* **Row 3 — the target-substitution analogue.** Run
  `bootstrap/verify_integrity.py --target <A>` and `--target <B>` against two
  scratch installs and confirm each output names the lockfile it actually read.
  *Negative control:* a target with no `dev/.cairn/cairn-lock.yml` must refuse
  rather than fall back to any other lockfile.
* **Row 4 — the classifier's verdict is about structure.** Confirm from
  `bootstrap/tests/test_byline_identity.py` that the classifier's output names
  the byline it classified. *Negative control:* the row cites the residuals R1
  (exact-name spoof) and R3 (the Cyrillic-homoglyph variant of the independence
  comparator, **3 of 4** measured variants closed) recorded on the
  `dev/PLANNING.md` board — because a B2 row that ignored them would be claiming
  a binding the tool does not have. The row is MET *for B2's property* and cites
  the two residuals as B5's business, not B2's.

**Acceptance criteria — Chunk D.** Four rows, four substitution runs, four
negative controls, outputs recorded; no repository file modified.

---

### Chunk E — B5: no normalization or parse step on an authorization path may widen authority or guess

**Property (proposal B5).** Wherever a shipped tool normalizes or parses an input
before an **authorization, classification, or install-contract** decision, an
input the step cannot fully interpret must move toward *less* authority or toward
refusal — never toward more, and never toward a guess.

**Where the tree stands, re-verified at HEAD `eacb7dd`.** The proposal's five
sites, three of which moved on 2026-08-03.

| Site | Direction on ambiguity | Row |
| --- | --- | --- |
| `tools/lifecycle_planner.py:248` — `_fold_word`, the identity fold (was the `re.sub(r"[^a-z0-9]", …)` one-liner at the proposal's three cited lines) | **neither** — every non-ASCII character survives; only ASCII non-alphanumerics, C0/DEL and combining marks are dropped | **MET-by-residual** — landed `1dabe4d`; residuals R2/R3 ratified on the board |
| The per-word AI-candidate leg | same fold, same direction | **MET-by-residual** — same lineage |
| The roster-entry normalization | same fold, whole-entry; names now compared separator-for-separator | **MET-by-residual** — same lineage, residual R5 |
| The profile loader's fallback YAML parse — `bootstrap/_scaffold/config.py:43` → `_minimal_yaml_parse` | **guesses** instead of refusing | **in flight** — `profile-parse-fail-open` |
| `_resolve_interpreter`, the local interpreter binding — `templates/skills/_lib/lifecycle.py:387` | shape validator, not an authenticator | **MET-by-residual** — `AGENTS.md` states plainly that it checks absoluteness, schema, symlink-freedom and the executable bit, but neither Python identity nor provenance |

The last row is what a MET-by-residual row looks like when done well and it is
already in the tree: nothing about it is fixed; what makes it MET is that the
limitation is written where a reader meets the tool.

**Why the three fold rows are MET-by-residual and not clean MET.** The
promotion defect is closed — no letter and no digit in any script folds to
nothing, so a confusable can no longer be *deleted into* a match on the
human-maintainer allowlist. But the granting fold still makes two distinct names
one key by full case folding and combining-mark stripping, and the
`dev/PLANNING.md` board's R2 records three measured classes where that maps a
**different person's** name onto the rostered one. That is a widening. It is
ratified with the classes named, pinned by tests, and carries a re-marked
mechanical expiry — which is precisely branch (b). Calling it a clean MET would
be the overstatement the bar exists to prevent.

| # | File | Change |
|---|------|--------|
| E1 | `dev/plans/release-security-bar.md` | The table above as the B5 register, with the widening-input run recorded per site. |

**Decider, and the negative control that makes it mean something.** For each
site, feed an input that differs from a *rejected* input only by what the step
drops or cannot interpret, and record which bucket it lands in.

* **Negative control, every row:** the *rejected* input itself must still be
  rejected in the same run. Without that leg, "the widened input was rejected"
  is consistent with the step rejecting everything, and the run proves nothing.
* **Rows 1–3:** feed a Cyrillic-homoglyph byline and a mathematical-bold byline
  alongside the plain rostered name and the plain non-rostered name; record all
  four buckets. Then feed a member of R2's three named classes and record that it
  keys as the rostered name — the row's residual is evidenced by a run, not by a
  citation.
* **Row 4:** feed the profile loader a `.yml` line it cannot parse, with PyYAML
  unavailable in a scratch environment; record whether the loader refuses or
  guesses. The row is *in flight*; the run establishes the current behaviour so
  the sibling lineage's fix has a before-state to be measured against.
* **Row 5:** feed `_resolve_interpreter` a path that satisfies every shape check
  and is not a Python interpreter; confirm it is accepted, and confirm the
  `AGENTS.md` sentence that says so is present and quoted in the register. The
  residual is only a residual while the sentence exists.
* **Invisible code points are written as text.** Where a run's input contains a
  line separator or a control character, the register records it as `U+2028`,
  `U+2029`, `U+0000` — never as a raw byte in the Markdown. A register that
  embeds the payload it is describing is a payload.

**Acceptance criteria — Chunk E.** Five rows; per row, a widening-input run and
the rejected-input control, both with recorded bucket; the three fold rows
explicitly labelled MET-by-residual with the residual quoted; no repository file
modified.

---

### Chunk F — B3: a documented security control names the command that fires it, and that command runs

**Property (proposal B3).** Every sentence in Set 3 that asserts a control *is
applied* names the command and the occasion. Where nothing fires it
automatically, the sentence says "run this" rather than implying a standing gate.

**Scope.** B3 quantifies **only over the security subset** of the twelve-row
(plus two later-audit rows) ledger in `gate-claims-vs-enforcement`. That ledger
is that proposal's and this plan edits none of it. Where a row falls inside both,
that proposal's disposition governs and the register records the row as
*delegated*.

**The two rows the bar contributes beyond that ledger, both still live at HEAD
`eacb7dd`:**

| Location | What it says | Owner | Status |
| --- | --- | --- | --- |
| `doctrine/runtime-contract.md:132` | the integrity check *"Detects tampered apparatus before it can self-audit"* | `gate-claims-vs-enforcement` (accepted `3a2a201`; its plan was **being opened concurrently** as this plan was written and is uncommitted at HEAD `eacb7dd` — re-check whether that plan claims this row before recording the disposition) | **falsified** by Chunk C's coordinated-tamper run |
| `SECURITY.md:51` | *"flagging any post-install modification"* | `agent-context-scrub` (plan open) — `contributor-entry` was **superseded** at `18cbf66`, so the hand-off table's *"whichever is decided first takes the row"* resolves to `agent-context-scrub` | **falsified** in the same run |

Note the asymmetry worth preserving. The sentence beginning at `SECURITY.md:47`
is *carefully* worded — *"confirm the installed tree still matches its recorded
install"* is exactly true. The overstatement is four lines later. A bar item that
flagged the whole document would be noise; one that quotes the sentence is
actionable.

Neither row's remedy is this plan's to write: both files are claimed. What this
plan owes is the row, the evidence, the named owner, and the disposition.

| # | File | Change |
|---|------|--------|
| F1 | `dev/plans/release-security-bar.md` | The B3 register: the delegated rows from the `gate-claims-vs-enforcement` ledger that fall inside the fence, each marked *delegated* with that proposal's disposition quoted; plus the two bar-contributed rows above with their falsifying run cross-referenced to Chunk C. |
| F2 | `dev/plans/release-security-bar.md` | The two standing inspections, RUN and recorded: `find .github -type f` and a `git ls-files` sweep for pipeline filenames, which together establish that **no scheduled trigger exists in this repository at all** — the fact eight ledger rows turn on. |
| F3 | `dev/plans/release-security-bar.md` | The **escape**, written before it is needed: if an owning lineage has not landed its correction when the register is otherwise complete, the row is **escalated to the Maintainer**, not taken. The bar does not edit a file another lineage claims, and it does not mark the row MET. |

**Decider.** For each sentence in scope: locate the named trigger and execute it.
A sentence whose trigger cannot be located is already a finding.

**Negative control (per corrected sentence), RUN.** The check that judges a
sentence must flag the *pre-correction* text and pass the corrected text — run
against `git show HEAD:<file>` and against the working file, exactly as NC-B2
does. A check that passes both texts is measuring nothing. Where the sentence has
not been corrected (both bar-contributed rows), only the flagging leg runs, and
the row stays NOT MET.

**The deadlock this chunk is designed to avoid, named rather than discovered.**
B1's `verify_integrity` row is MET-by-residual **only if** these two sentences
are corrected — that is what branch (b) requires. Both are owned elsewhere. So
the bar can be blocked by a lineage that never picks up a one-sentence fix. F3's
escape is the Maintainer's release valve, and it is on the fence deliberately:
an agent taking a claimed file to unblock its own bar is exactly how a
one-proposal-per-file rule dies.

**Acceptance criteria — Chunk F.** The security subset enumerated from Set 3 and
dispositioned row by row; the two standing inspections run with output; the two
bar-contributed rows recorded as NOT MET with the named owner and the escalation
condition; no repository file modified.

---

### Chunk G — B4: every test the bar names as an enforcer fails against the drift it is named for

**Property (proposal B4).** For each test the register cites as what keeps a row
closed, the plan records (i) a perturbation that is an instance of *the failure
class the test's own name or docstring claims to guard*, (ii) the command
applying it, and (iii) the observed failure output.

**The refinement, and why it is not optional.** A weaker form — *"name any
perturbation that turns the test red"* — passed on the very test that motivated
this item, because three of its *other* assertions genuinely could fail. An
author asked for "a perturbation" would name one of those in good faith and the
vacuous assertion would survive. Requiring the perturbation to be **in the class
the test names** is what discriminates. That distinction is the whole content of
B4, and it is the standard every other chunk in this plan is also held to.

**Denominator.** Defined by the register: the tests Chunks B–F cite as enforcers.
The proposal expects 15–25 rows. For scale, the four modules most likely to
supply them collect **117 tests** (`bootstrap/tests/test_byline_identity.py`,
`test_verify_ref.py`, `test_security_lint.py`, `test_security_check.py`;
`--collect-only`, `as_of 2026-08-04`) — B4 quantifies over the cited enforcers,
not over all 117, and that narrowing is what keeps it finite.

**The one row known to have failed, and its current state.** The proposal's
origin instance — `test_scan_targets_cover_all_shipped_scripts`, whose oracle was
computed from the same object its subject walked, green for 63 days across the
exact drift its docstring named — is **fixed**, at `5c91c23`. Its replacement
(`bootstrap/tests/test_security_lint.py:229`) derives its oracle from a working
tree glob the subject never reads, and
`bootstrap/tests/test_security_lint.py:317` is itself a
perturbation-of-the-hazard test. The B4 register records this row as the
worked example of what a closed row looks like — and re-runs its perturbation
rather than trusting the sibling plan's transcript.

| # | File | Change |
|---|------|--------|
| G1 | `dev/plans/release-security-bar.md` | The B4 register: one row per enforcer test cited in Chunks B–F, each with the test's claimed class (quoted from its name or docstring), the in-class perturbation, the command, and the observed failure output. |
| G2 | `dev/plans/release-security-bar.md` | Per row, the **discrimination leg**: a perturbation in a *different* class under which the test stays green. This is what shows the chosen perturbation is discriminating rather than incidental, and it is the only leg that distinguishes B4 from the weaker form the proposal rejects. |
| G3 | `dev/plans/release-security-bar.md` | The restore ledger: for every perturbation, `git status --short` clean and `git diff <path>` empty afterwards, verified as its own step. |

**Acceptance criteria — Chunk G.**

* Every enforcer test cited in the register has an in-class perturbation run with
  recorded output, plus its discrimination leg.
* **Every perturbation targets the hazard, never the test body.** A row whose
  perturbation edits the test's own assertions is rejected at review; it
  validates the harness and says nothing about the claim. This sentence is the
  acceptance criterion, not commentary.
* **Byte-identical restore, verified.** After each perturbation, `git diff
  <path>` is empty and `git status --short` shows no residue. Where a
  perturbation created a probe file, it is deleted and the deletion confirmed.
* **The edge case the proposal names, handled rather than passed.** If the
  register cites **no** enforcer tests for an item, that is itself a finding and
  the row says so — the item is **not** passed vacuously. An item with zero
  enforcers is an item whose closure rests on nothing.
* **The honest non-perturbation, where it exists.** Where a cited test *cannot*
  be made to fail by any in-class perturbation, the register says so plainly and
  the row is NOT MET. That outcome is the item working, not the item failing.

---

### Chunk H — the burndown roll-up, the staleness command, and the changelog text

| # | File | Change |
|---|------|--------|
| H1 | `dev/plans/release-security-bar.md` | The roll-up table: six items, rows, MET / MET-by-residual / in flight / NOT MET, with the date each was last decided. This is the table the proposal promises the Maintainer can read instead of running diagnostics. |
| H2 | `dev/plans/release-security-bar.md` | **The register's surface list** — the explicit set of paths the register's rows depend on — plus the staleness command that consumes it: `git log -1 --format=%cI -- <surface list>` compared against the dated `### Code review -- <reviewer> -- <date>` heading. If the commit is newer, the audit is stale and the tag waits. No new tooling. |
| H3 | `dev/plans/release-security-bar.md` | The **returned** `CHANGELOG.md` line text (below), recorded here so the serialization point has it and no agent writes it into the shared file mid-plan. |

**Acceptance criteria — Chunk H.**

* The roll-up reproduces from the per-item registers with no figure appearing
  only in the roll-up.
* **Negative control NC-H1 (the staleness command can fire), RUN.** Take the
  surface list, run the `git log -1` command, and confirm the timestamp it
  returns is the one `git log -1 --format=%cI -- <one known-recent path>`
  returns for the most recently touched member. Then run it against a surface
  list containing only a path with no commits and confirm it returns empty
  rather than a false-fresh timestamp — the failure mode that would silently
  pass a stale audit.
* The changelog line is **returned, not written**.

---

### Chunk M (Maintainer-only) — the fence

> **This chunk is not an implementing agent's.** An agent's work ends at Chunk H.
> Everything below needs a key, a credential, a supervised act, or a decision
> that is the Maintainer's by right.

1. **The `dev/PLANNING.md` row and the precondition clause** — a serialized
   shared file. The text is returned below; it lands at a serialization point,
   not from inside a burndown chunk. **The precondition clause has two drafted
   forms and the choice is D3's**: tag-only, or tag plus repo-public flip.
2. **The `CHANGELOG.md` line** — same discipline, text returned below.
3. **Commissioning the end-of-line audit** — External tier, a different agent
   type or a human, and **not the bar's author** (proposal D6). Commissioning it
   from the author would leave the bar codifying its author's blind spots as the
   definition of done, which is the failure the proposal's *Why this tier*
   section is written against.
4. **Reopening D4** — whether `bootstrap/verify_integrity.py`'s verbatim subset
   is anchored for v0.4.0 after all. The Decision routed it to the deferred
   ledger; reopening it is a Maintainer call, and executing it is a successor
   proposal with its own Security Review. **No agent reopens it from inside this
   plan.**
5. **F3's escape** — authorizing the bar to take a sentence in a file another
   lineage claims, if that lineage stalls.
6. **The launch sequence itself** — the repo-public flip, Zenodo, the
   `git tag v0.4.0`, the DOI commit. Named here because the bar's whole purpose
   is to sit in front of them.
7. **Every signing key.** No agent run in this plan touches
   `dev/.cairn/allowed_signers`, the Maintainer's signing key, or
   `refs/cairn/gate-anchor`. Every signature decider uses a throwaway key
   generated in a scratch directory outside the repository, and says so in its
   recorded output.

**The honest limit, restated from the proposal because it is the weakest
enforcement here and dressing it up would be the defect the bar exists to
prevent:** *nothing in this repository mechanically prevents a `git tag`.* The
archive preconditions at `tools/lifecycle_planner.py:792` do mechanically
prevent this **plan** from reaching `archived` without a code review, a
`Follow-ups migrated to:` block and a fidelity sign-off. The link from "the plan
is not archived" to "the tag does not happen" is a sentence written where the
sequence is read — no more, and the register should not claim more.

## Acceptance criteria

Per-chunk criteria are above; these are the plan-level deliverables.

* **Tests that must pass.** **N/A as new tests** — this plan adds no code and no
  test, by design and by the standing *build nothing new* direction. What
  replaces them:
  * `python -m pytest bootstrap/tests` — the whole suite, green, under the
    canonical interpreter (3.13.13) with `PYTHONDONTWRITEBYTECODE=1`. Baseline
    taken by the implementing agent at its own start against a clean tree, not
    quoted from here (see *Gate accounting*). The suite must be green **before
    and after** Chunk B, the only chunk touching a shipped file.
  * **Every decider carries a negative control that perturbs the hazard, not the
    decider.** This is the plan's central acceptance criterion and the one a
    reviewer should sample first. A row whose evidence column contains prose
    instead of a command and its result is rejected.
  * **Every perturbation restores byte-identically**, verified with `git diff
    <path>` and `git status --short` as its own step.
* **Doc updates that must land.** Hand-authored only:
  `templates/onboarding/high-rigor-legacy.md` (two passages, Chunk B) and the
  returned `CHANGELOG.md > Unreleased > Added` line. No generated docs, no
  snippet-synced blocks, no `doctrine/` change, no `AGENTS.md` change.
* **Examples / smoke checks required.** `python bootstrap/scaffold.py
  --manifest` — expected **unchanged**, 95 data rows, which is itself the
  assertion that this plan installs nothing new into an adopter tree. `python
  scripts/check_cairn.py` — OK. **N/A**: the example gallery under `examples/` —
  this plan touches nothing the runnable examples demonstrate.
* **Inbound path-link updates.** None expected. `dev/PLANNING.md` and
  `dev/NEXT_SESSION.md` refer to plans by filename stem, not path link, so the
  archive-move needs no edit there. Confirm at archive time rather than assume.

### Author-accounting — invariants, failure modes, edge cases

* **Invariants, each with the chunk that enforces it.**
  * *The bar's item count is fixed at Decision.* Six. A seventh is a new
    proposal, visibly. Enforced by the audit's scope constraint (falsify rows, do
    not open classes) and by this plan's append-only review sections.
  * *Every row resolves to MET, MET-by-residual, in flight, or NOT MET — never
    silence.* Enforced per-chunk in Acceptance, and re-checked in Chunk H's
    roll-up, where a missing row is a missing table cell.
  * *Every decider is two-sided.* A row carries both a run that produces its
    verdict and a negative control that produces the other one. Enforced by the
    per-chunk NC legs; the single most likely thing to be skipped under time
    pressure, and therefore the thing the plan review should sample.
  * *No perturbation edits a test's own body.* Enforced in Chunk G's acceptance
    and applied to every chunk.
  * *No repository file is modified outside Chunk B.* Enforced by `git status
    --short` at each chunk end.
  * *The install contract does not move.* Enforced by the `--manifest` diff, 95
    rows.
  * *The plan cannot archive incomplete.* Enforced mechanically at
    `tools/lifecycle_planner.py:792`–`:806` — code review, follow-ups block, and
    fidelity sign-off all required for `archived`.
* **Public-path → test mapping.** **N/A**: this plan adds no code and no public
  entry point. The mapping obligation transfers to whatever code a *successor*
  proposal produces, and B4 is the discipline that mapping is held to.
* **Failure modes.**
  * *Open (degrades):* a row is marked MET on a decider that was run sloppily.
    The end-of-line audit is the compensating control; it is not a proof.
  * *Open (degrades):* Chunk A's enumeration is incomplete — a verification step,
    a normalization site, or a shipped control that nobody listed. This is the
    bar's central residual; NC-A3's deliberate miss is the evidence for it and no
    part of the design closes it.
  * *Closed (blocks):* a row owned by an in-flight lineage whose proposal is
    rejected reverts to unowned and the bar blocks. Correct behaviour; the
    register records the dependency so it is visible early.
  * *Closed (blocks):* B1's `verify_integrity` row cannot reach MET-by-residual
    until Chunk F's two sentences are corrected, and both are owned elsewhere.
    F3's escape routes the stall to the Maintainer rather than to an agent.
  * *Open, intentional:* a registered residual ships. That is the design.
* **Edge cases.**
  * *Zero enforcer rows for B4* — a finding the register must state, never a
    vacuous pass (Chunk G acceptance).
  * *A row MET at register time and broken by a later commit* — caught by Chunk
    H's staleness command, not by re-running everything.
  * *A sibling lineage moves a line this plan quotes* — three sibling plans
    currently read `open` while their code is in the tree, so every quoted line
    is re-read at implementation time rather than applied from this text. Stated
    as a rule, not a hope.
  * *The register grows this file past readability* — the proposal names this as
    the real failure mode for a document whose entire value is legibility, with
    the recovery: collapse to one table with six sections and drop the per-item
    prose. Recorded so the recovery is pre-authorized rather than improvised.
* **Known omissions, stated rather than implied.** (a) No mechanism keeps the B6
  reach table in step with `bootstrap/_scaffold/config.py`; the staleness command
  is a tripwire, not a gate, and pinning it with a test is deliberately fenced
  out. (b) The register's evidence is a transcript of runs, and a reviewer who
  re-runs nothing inherits the implementing agent's care — which is why the
  end-of-line audit's job is *falsifying rows*, not reading them. (c) Chunk C's
  fork-advisory row depends on another session's uncommitted work; if that work
  lands differently than its plan describes, the row's condition must be
  re-derived from the landed code. (d) No decider covers an adopter's own
  repository, agents, or practices — the fence is what Cairn ships. (e) The
  `check_cairn` coverage gap re-measured for this plan (**180 of 234** tracked
  Markdown files, `as_of 2026-08-04`; the proposal recorded 173 of 218) is
  outside the fence and deferred to v0.5 — recorded because the numbers moved and
  a stale figure in the register would be its own B3 violation.

## Verification

The concrete commands the implementation must pass. Run under the canonical
interpreter (`~/conda_envs/lhm/bin/python3.13`, 3.13.13) with
`PYTHONDONTWRITEBYTECODE=1`.

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

**Plan-specific gates, added here because this plan touches those surfaces.**

* **The install-contract assertion** — `python bootstrap/scaffold.py --manifest`,
  diffed against a capture taken at the plan-open commit. **Expected empty**, 95
  data rows, `as_of 2026-08-04`. A diff means a chunk edited delivery machinery
  rather than reading it; stop and re-review.
* **The B6 reproduction** — the eight-line `load_config` → `expand_preset` →
  `install_manifest` measurement per preset, re-run at the start of Chunk B and
  again at Chunk H. If the table has moved between them, a sibling landed a
  preset change and every B6 sentence is re-checked.
* **The working-tree cleanliness assertion** — `git status --short` at each chunk
  end, showing no residue from any scratch construction. Every decider in this
  plan is designed to run outside the repository; a modified file at chunk end is
  a defect in the run, not a finding about the tree.
* **The negative-control ledger** — per chunk, in the commit body: the hazard
  perturbed, the verdict observed in both directions, and the restore verified.
* **`python scripts/claim_check.py dev/plans/release-security-bar.md`** and
  **`python scripts/check_cairn.py dev/plans/release-security-bar.md`** after
  every burndown chunk, since each appends citations to this file.

## The `dev/PLANNING.md` and `CHANGELOG.md` text this plan returns

`dev/PLANNING.md` and `CHANGELOG.md` are serialized shared communication files.
The text below is **returned for a serialization point**, not written by an
implementing agent from inside a chunk.

**1. The `## Active` row (plan-open).**

```
* **release-security-bar** *(plan open 2026-08-04)* — the v0.4.0 release
  security bar: six checkable properties (B1 trust-material provenance, B2
  answer-binding, B3 claim honesty, B4 non-vacuous enforcers, B5 fail-closed
  direction, B6 stated reach), a committed register that burns them down one
  surface at a time, and an end-of-line External audit whose job is to falsify
  rows rather than open new classes. The bar is specificational, not
  diagnostic: it ends when its list is exhausted. Re-verified at plan-open,
  three of the proposal's rows closed on 2026-08-03 (`b93f8e9`, `5c91c23`,
  `1dabe4d`); the `verify_integrity` lockfile-anchor row remains a registered
  residual owned by *Deferred follow-ups > Security apparatus >
  Install-integrity trust anchor*, and it is MET only once its two overstating
  sentences are corrected by the lineages that claim those files.
```

**2. The precondition clause in the public-launch sequence — TWO DRAFTED FORMS,
the choice is the Maintainer's (proposal D3).**

*Form A — tag-only (the conservative reading; blocks what the Decision's own
"What it blocks" paragraph names):* append to the `tag v0.4.0 and push` step —

```
tag `v0.4.0` and push (triggers Zenodo deposition → DOI) — **precondition: the
`release-security-bar` plan is archived**, which requires its end-of-line
External audit to have landed and every register row to be MET or a registered
residual
```

*Form B — tag plus the repo-public flip (proposal D3's recommendation; a public
repository can be cloned and installed before any tag exists, so the flip is the
real first-exposure moment for a postdoc):* the same clause, additionally
attached to the `flip the repo to public + set the template-repo flag` step,
which then moves **after** the audit in the recorded order.

**Form A is what this plan assumes absent a Maintainer instruction**, because
D4's recommendation was overridden by the Decision and D3's therefore cannot be
assumed adopted. Form B is a one-line substitution.

**3. The `CHANGELOG.md > Unreleased > Added` line.**

```
* A written, falsifiable definition of secure-enough-to-ship for v0.4.0 — six
  checkable properties with named deciders, a committed register of every
  surface each quantifies over, and an end-of-line External audit that blocks
  the release tag. See the `release-security-bar` proposal and plan.
```

## Plan review — the brief, and why an Internal round does not discharge the tier

*Required — **External**. Implementation does not start until a review has
landed under this heading.*

**The declared tier is `required(External)`**, carried from the proposal header
and re-stated by the Decision in its closing line. **An Internal round does not
discharge it.** Internal review's floor is *the same agent type in a fresh
session*; this artifact was written by Claude, so an Internal read is another
Claude. The proposal's *Why this tier* section argues exactly why that is
insufficient here, and the argument is structural rather than about quality:

> the specific failure mode of a specification written by the same author who
> wrote the diagnostics is that it specifies exactly what the author already
> knows to look for.

An Internal round is still worth running and this plan expects one. It can catch
a wrong line citation, an unsound negative control, a chunk ordering that does
not hold. What it cannot do is test whether the six properties are the *right*
six and whether the fence is drawn where an outsider would draw it — and it
cannot do that for the reason above, not for lack of effort. **So: the Internal
round sharpens; the External round discharges. No burndown chunk lands until an
External review has landed under this heading, and an Internal round landing
first does not change that.**

**The four questions this review should aim at**, in descending weight:

1. **Is every negative control a perturbation of the hazard?** Take three rows
   at random and check that the NC leg changes the registry, the document, or
   the shipped code path — not the checker and not a test body. If any NC
   perturbs the check, that row's evidence is about the harness and the row is
   decoration. This is the plan's central claim and the cheapest thing to
   falsify.
2. **Is the two-reads reading of the audit's home right?** The accepted text
   calls the end-of-line audit the plan's `## Plan review` stage and then
   describes it firing at `review`/`archived`. This plan splits them and routes
   the audit to `## Code review`, on the evidence of
   `tools/lifecycle_planner.py:786` vs `:792`. Attack that: if one External read
   is what was meant, say which one, and say what is lost.
3. **Is Chunk A's enumeration honest about its own miss?** NC-A3 deliberately
   constructs a claim sentence the pattern sweep does not catch. Check that the
   missing form is quoted and that the residual is stated as a finding, not as a
   caveat. An enumeration that reports only its catches is the receding horizon
   with a table.
4. **Is B1's `verify_integrity` row correctly blocked?** The row is
   MET-by-residual *only* if two sentences owned by other lineages are
   corrected. Check that the plan does not quietly mark it MET, that F3's escape
   is on the Maintainer fence rather than an agent's, and that the deadlock is
   named rather than discovered.

Two further things a reviewer is invited to strike rather than accept: the
decision **not** to pin the B6 reach table with a test (fenced as a v0.5
derived-list item, and the closest call in the plan); and Chunk G's
discrimination leg, which roughly doubles B4's per-row cost and is the first
thing to cut if B4 turns out to cost days per row rather than hours.

> **The landed review appends here as a `### Plan review -- <reviewer> --
> YYYY-MM-DD` sub-heading** (plus a `### Sharpening` sub-heading if it raised
> findings). **Do not rename this heading to a bare `## Plan review`.** The
> heading above carries an em dash and a comma, which
> `tools/lifecycle_planner.py`'s `_HEADER_RE` (line 509) does not admit into a
> section *kind* — so it is not parsed as a section at all, and the gate at
> `tools/lifecycle_planner.py:786` keeps reporting the section missing until a
> real `###` review sub-heading lands. A bare `## Plan review` heading would be
> satisfied by an *empty* section; this shape cannot be.
>
> **Measured for this plan, 2026-08-04**, against a scratch copy outside the
> repository with only the status line changed to `executing`:
>
> ```
> $ python tools/lifecycle_planner.py next <scratch>/plans/probe.md
> lifecycle-planner: current state: executing
> lifecycle-planner: VIOLATION: status is 'executing' and 'Plan review:
>   required', but no '## Plan review' section has landed
>   (review-before-implement).
> ```
>
> That is the heading discipline demonstrated on *this* file rather than
> inherited from the sibling plans `scan-coverage`, `release-authenticity` and
> `agent-context-scrub`, which record the same measurement.

## Code review — the end-of-line audit (no review has landed)

*Filled in after the burndown chunks land.* The reviewer is **not** the
implementing agent and **not** the bar's author (proposal D6). Begin with
`**Model**: <model or tier when known; "unknown" if not.>` immediately below a
`### Code review -- <reviewer> -- YYYY-MM-DD` sub-heading.

**This section is the end-of-line audit.** It is not an extra ceremony bolted on
to a code review — it is the stage `tools/lifecycle_planner.py:792` actually
checks before `archived`, which is why the audit is homed here rather than in a
roadmap row. The proposal measured the death mechanism of the previous
follow-on precisely: it was routed to a roadmap row, and the archive
precondition **has no proposal-side arm at all**. Homing this audit in a plan
puts it on the side of the asymmetry where the check fires.

**What it checks — and nothing else.** The six items, against the register,
using the deciders. The auditor's job is to **falsify rows**: take a row marked
MET and run its decider to see whether it holds. A new class found during the
audit goes to the v0.5 list unless the Maintainer classifies it high-risk. That
constraint is what makes the audit terminate, and it is the proposal's sharpest
sentence: *an audit with an open scope is the receding horizon wearing a hat.*

**The falsification ledger this review owes, at minimum:**

* **Independently re-run three negative controls**, chosen by the auditor, rather
  than re-trusting the implementing session's transcript. At least one from
  Chunk C (a signature construction) and one from Chunk G (an in-class
  perturbation).
* **Sample one B4 row and attack its discrimination leg** — find a perturbation
  in the *named* class under which the test stays green. If one exists, the row
  is wrong and B4 has found the thing it exists to find.
* **Confirm each perturbation's byte-identical restore** with `git hash-object`
  against `git rev-parse HEAD:<path>`, not by reading the ledger.
* **Re-run the B6 measurement** and confirm the committed table still reproduces.
  If it does not, a preset moved and every B6 sentence is stale.
* **Run the staleness check** (`git log -1 --format=%cI -- <the register's
  surface list>`) against this section's own date, and say plainly whether the
  audit is stale on the day it is written.
* **State the coverage line**: which rows were re-run, which were read, and which
  were taken on the implementing agent's word.

## Lasting-truth migration

*Filled in at archive time.* Per the
[Archive preconditions rule](../PLANNING.md#archive-preconditions-proposals-and-plans),
plans archive only after every deferred follow-up has a durable home outside the
plan. This section is append-only once written.

**Pre-declared homes, so no follow-up arrives at archive time without one:**

| Follow-up | Durable home |
| --- | --- |
| The five v0.5 deferrals named in the proposal (token-substituted lockfile anchoring; non-test derived-list integrity; extending the bar to Cairn's own dev tooling incl. the `check_cairn` coverage gap; mutation testing as a standing mechanism; cryptographic attestation) | `dev/PLANNING.md` > *Deferred follow-ups (durable home)* — a new **Release bar (v0.5)** group, each row carrying its revival condition |
| The `verify_integrity` lockfile anchor | **already homed**: `dev/PLANNING.md` > *Deferred follow-ups* > **Security apparatus** > *Install-integrity trust anchor* — the plan adds nothing, and re-states the row's three open questions in the register rather than duplicating them on the board |
| **Set 2's manifest-external installs** (`dev/modules/onboarding/*.md` are installed, manifest-unlisted and lockfile-uncovered) — the finding this plan contributes before it starts | `dev/PLANNING.md` > *Deferred follow-ups* > **Scaffold / engine**, as a new row. Revival condition: any change to what `install_onboarding` writes, or the first adopter-reported drift in `dev/modules/onboarding/`. **Not fixed here** — bringing those destinations under the manifest is an install-contract change and needs its own proposal |
| B6's unpinned reach table (no test keeps it in step with preset composition) | the same **Release bar (v0.5)** group, as the concrete instance of *derived-list integrity for non-test lists*. Trigger: the first time the table is found stale by Chunk H's staleness command |
| Chunk A's stated enumeration residual (the deliberately-constructed miss from NC-A3) | this plan's own B-item registers, which archive with it — *"exactly the artifact a v0.5 bar would start from"* |
| Any row still NOT MET at audit time | escalated to the Maintainer as a release-blocking item, **never** migrated to a board row — migrating a blocking row to a board is how the Class C follow-on died |

The register itself does **not** migrate: when this plan archives, it archives as
the record of what v0.4.0 was held to.

See also `doctrine/lifecycle.md` > "Loop-fidelity verification" for the
Decision→implementation fidelity sign-off checkpoint, which this plan owes at
archive alongside the `Follow-ups migrated to:` block and the `## Code review`
section (`tools/lifecycle_planner.py:792`–`:806`).
