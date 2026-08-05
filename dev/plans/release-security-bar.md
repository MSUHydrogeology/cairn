<!-- cairn-internal-ref-allow: doctrine/plans.md doctrine/dual-review.md doctrine/lifecycle.md doctrine/rationale.md doctrine/coordination.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see AGENTS.md, "Where doctrine/ references resolve") -->
<!-- cairn-accept: instruction-html-comment reason="The comment below explains to human readers and to the claim checker why three adopter-tree destination paths are deliberately non-resolving; it carries no directive to an agent and names no action to take." reviewer="Claude (author)" date=2026-08-04 -->
<!-- claim-check-allow: dev/plans/scan-coverage.md, dev/plans/gate-claims-vs-enforcement.md, dev/plans/default-security-stance.md, dev/plans/planner-line-semantics.md, dev/plans/agent-context-scrub.md -->
<!-- ^ Archived 2026-08-04; the plans moved to dev/plans/archive/. These are
<!-- claim-check-allow: dev/proposals/2026-08-03-claude-gate-claims-vs-enforcement.md -->
<!-- ^ Source/sibling proposals archived 2026-08-04. These citations sit in
     append-only sections, so the path is exempted rather than rewritten. -->

     historical citations in append-only or logged content, so the path is
     exempted rather than rewritten -- editing a prior section to chase a
     file move is what AGENTS.md's cite-by-stem convention exists to avoid. -->

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

## Plan review -- Claude (Internal, same-agent-type; security lens) -- 2026-08-04

**Model**: claude-opus-5 (exact id `claude-opus-5`).

> **READ [I1] BEFORE ANYTHING ELSE — this heading is itself a finding.**
> The heading immediately above matches `tools/lifecycle_planner.py`'s
> `_HEADER_RE` (line 509) with `kind = "Plan review"`, and the gate at
> `tools/lifecycle_planner.py:786` calls `_has_kind(art, "Plan review")`
> (definition at `:693`–`:694`), which reads **only the kind prefix** — never
> the tier, the role, or the reviewer. **Landing this Internal review therefore
> flips the plan-review gate to green**, which is the exact outcome the plan's
> own text forbids. Measured, both directions, below. The one-line remedy is on
> the Maintainer fence.

### Standing — declared, not assumed

I am **the same agent type as the plan's author** (Claude, fresh session). There
is **no cross-type independence** in this read. The plan's own *Why this tier*
argument applies to me verbatim: a specification and a same-type review of it
share a prior about what is worth looking for, so the class of hazard neither of
us thinks to enumerate stays invisible in both.

**This review does not discharge the declared tier.** The plan carries
`Plan review: required(**External**)`, carried from the proposal header and
re-stated by the Decision (`3cda505`). External's floor is a different agent type
or a human. I am neither. What follows is an **Internal sharpening pass**: line
citations checked against the tree, figures re-measured, negative controls
reconstructed and run. It is the cheap mechanical half. The expensive half — *are
these the right six properties, and is the fence where an outsider would draw
it* — is untouched by this read and remains owed.

The gap between "this review does not discharge the tier" (true, and the plan
says so) and "the tree will not let it discharge the tier" (**false**, measured)
is [I1].

### Steelman

This is the strongest plan in the current `dev/plans/` set on the dimension it
was written for, and the reasons are specific rather than complimentary.

* **It measured instead of carrying.** The proposal's starting burndown was
  written before three commits landed on 2026-08-03. Rather than inherit it, the
  plan re-derived every row at HEAD and found six of them stale *in the good
  direction*. I re-ran the underlying checks: `b93f8e9`, `5c91c23`, `1dabe4d`,
  `0c6d9de`, `3a2a201`, `18cbf66`, `3cda505` all exist and carry the subjects
  claimed; every line citation in the plan resolves at HEAD `eacb7dd` with the
  quoted text (I checked all 24). That is an unusually clean citation record for
  a 1292-line artifact written in a week when five engine files are being
  rewritten underneath it.
* **It contributes a real finding before it starts.** The Set 2 under-count is
  correct and load-bearing: `install_onboarding` writes
  `dev/modules/onboarding/<preset>.md` plus two shared docs to destinations that
  appear in **no** `install_manifest` row and **no** lockfile record. I verified
  independently — `dev/.cairn/cairn-lock.yml` carries 81 `"dst"` records and
  `grep 'dev/modules/onboarding'` over it returns nothing, while
  `dev/modules/onboarding/` holds three installed files. An adopter-facing
  document that makes a security-gate claim is outside the tamper check. Finding
  this *before* the enumeration is drawn is the plan working as designed.
* **Its central MET-by-residual claim is true, and I reproduced it.** Scaffolded
  `solo-greenfield` from a clean HEAD extract into a scratch target; appended a
  marker to `scripts/claim_check.py`; rewrote that one record's hash in the
  target's own lockfile; re-ran HEAD's verifier. Result: `verify_integrity: OK --
  55 recorded file(s) match dev/.cairn/cairn-lock.yml`, marker still on disk. The
  negative control (same tamper, lockfile untouched) produced `modified (hash
  mismatch): scripts/claim_check.py`. Both directions, as the plan specifies.
  The finding is real and the plan's refusal to fix it — routing it to the
  ledger per the Decision — is the correct call.
* **The B4 refinement is the sharpest idea in the lineage.** "Name any
  perturbation that turns the test red" demonstrably passed on the test that
  motivated the item. Requiring the perturbation to be *in the class the test's
  own name claims* is what discriminates, and the discrimination leg (G2) is
  what makes it checkable rather than assertable. The plan is right that this is
  the first thing to cut under time pressure and right to say so out loud.
* **It names its own worst case.** The enumeration residual is stated as a
  finding with a required deliberate *miss* (NC-A3), not as a caveat; the
  register's legibility failure mode carries a pre-authorized recovery; the
  honest limit — *nothing in this repository mechanically prevents a `git tag`* —
  is stated rather than dressed up. A plan that pre-registers the ways it will
  fail is a plan that can be audited.
* **The two disagreements with the accepted text are surfaced up front**, with
  the evidence (`:786` vs `:792`) and with the alternative reading written out
  so the Maintainer can strike one in a line. That is the right shape for an
  agent that noticed an inconsistency it does not have authority to resolve.

The concerns below are almost all about the **gap between what the plan
specifies and what the tree will do when the specification is executed this
week**. None of them touch the design's core.

### Concerns

**[I1] — the plan-review gate cannot distinguish Internal from External, so this
very review discharges it. (Blocking; the plan's central structural protection is
prose-only.)**

The plan states the rule three times and in bold: *"No burndown chunk lands
until an External review has landed under this heading, and an Internal round
landing first does not change that."* It cites `tools/lifecycle_planner.py:786`
as the mechanism, and demonstrates the heading discipline with a scratch probe.

That probe measured the **presence** half and never the **tier** half. The gate:

```
tools/lifecycle_planner.py:786   if s in ("executing","review","archived") and requires_review \
                          :787           and not _has_kind(art, "Plan review"):
tools/lifecycle_planner.py:693   def _has_kind(art: Artifact, prefix: str) -> bool:
                          :694       return any(s.kind.lower().startswith(prefix.lower())
                                                for s in art.sections)
```

`_has_kind` compares the parsed **kind** only. `Section` carries `role` and
`name` (`_parse_sections`, `:560`–`:590`), and the gate reads neither. Measured
on a scratch copy of this plan outside the repository, status line changed to
`executing`:

```
A. status=executing, no review section:
   lifecycle-planner: VIOLATION: status is 'executing' and 'Plan review:
     required', but no '## Plan review' section has landed (review-before-implement).

B. same file + '### Plan review -- Claude (Internal, same-agent-type;
   security lens) -- 2026-08-04' appended:
   (no violation; planner proceeds to
    "[ok ] append a '## Code review' pass ...")
```

The violation disappears on an **Internal** sub-heading. It disappears at `###`
*and* at `##` — `_has_kind` is level-agnostic, so the plan's own prescribed
`### Plan review -- <reviewer> -- YYYY-MM-DD` form trips it too. The tier lives
only in the `(role)` capture, which nothing consults.

Two consequences:

1. The plan's protection against implementing-before-External is a **sentence**,
   not a gate. The next agent to set status to `executing` runs
   `lifecycle_planner next`, sees green, and has no mechanical signal that the
   required tier never arrived.
2. By the bar's own **B3** — *a documented security control names the command
   that fires it, and that command runs* — the plan's sentence "the gate at
   `tools/lifecycle_planner.py:786` keeps reporting the section missing until a
   real `###` review sub-heading lands" is a **standing-gate claim for a property
   that nothing enforces**. The bar's own gate-blocking mechanism is a B3
   violation. This is also the plan's own *perturb-the-hazard* rule turned on
   itself: the committed probe perturbed the heading's **shape** (the check)
   rather than the reviewer's **tier** (the hazard), and so it passed.

*Remedies, all one line, all the Maintainer's:* (a) rename this section's
heading to a form `_HEADER_RE` rejects — the em-dash-plus-comma shape of the
existing `## Plan review — the brief, …` heading already demonstrates the
technique, verified: that heading does **not** match; or (b) add the tier to the
gate (`_has_kind` variant that reads `role`), which is engine surface and its own
proposal; or (c) accept that the gate is presence-only and delete the claim that
it enforces the tier, keeping the rule as an explicitly-unenforced convention.
Option (c) is the honest minimum and costs nothing.

*I appended under the heading I was instructed to use rather than substituting
one silently.* The gate is now green on this file. Nothing is committed.

**[I2] — Chunk B edits two lines a sibling plan records as owned by a third
lineage that does not claim them. (Blocking for the one chunk that needs
approval.)**

The plan states `templates/onboarding/high-rigor-legacy.md` is *"the only
unclaimed file the proposal's hand-off table leaves inside this bar's budget"*
and takes lines 123 and 164 in Chunk B — the single chunk that loses the
deliberation carve-in and re-triggers the approval gate.

Measured across the sibling tree:

* `dev/plans/default-security-stance.md:133` — *"`templates/onboarding/high-rigor-legacy.md`
  lines 123 / 164. Owned by `gate-claims-vs-enforcement`. Whichever lands second
  must not re-assert what this one falsifies."*
* `dev/plans/default-security-stance.md:871` — the same two lines, *"Already
  owned by `gate-claims-vs-enforcement`; no migration needed."*
* `grep -rn "high-rigor-legacy" dev/plans/gate-claims-vs-enforcement.md
  dev/proposals/*gate-claims*` → **no output.** That lineage does not claim them.

So three plans hold three different beliefs: this one says unclaimed and takes
them; `default-security-stance` says claimed and defers; the named claimant is
silent. That is an **ownership vacuum wearing an ownership label** — and it is
precisely the condition F3's escape exists for, invoked for nothing here because
the plan concluded "unclaimed" without checking the siblings that say otherwise.

Second-order, and not named anywhere in this plan: `default-security-stance`'s
pre-declared changelog text (`:871`, row 7) is *"the default install now carries
the `content-security` scanner"*. If that lands, Chunk B's correction — *"name
only the gate the preset actually installs"* — becomes **false in the opposite
direction** and these two sentences need re-correcting. The plan correctly warns
its wording *"must not presume the default-security-stance change"*; it does not
note the converse, that the correction has a short half-life and a sibling has
already written down the sequencing rule for it.

**[I3] — NC-B1's expected result is falsified by the tree, and it names a file
that does not contain the thing it says to edit. (The plan's only B6 negative
control.)**

NC-B1 reads: *"In a scratch copy of `bootstrap/profiles/high-rigor-legacy.yml`
outside the repository, add `content-security` to the preset's module selection;
… confirm the three `content_scan` rows flip from `—` to `yes`."*

Two independent defects, both measured.

*(a) `bootstrap/profiles/high-rigor-legacy.yml` contains no module selection.*
Stripped of comments the file is exactly three keys:

```
project_name: "High-Rigor-Legacy-Project"
test_command: "pytest"
preset: high-rigor-legacy
```

The preset's module roster lives in `_PRESETS` at
`bootstrap/_scaffold/config.py:1205`, read by `expand_preset` (`:1422`). The
only lever a profile has is `modules_add` (`config.py:1154`) — an **adopter
override**, which tests a different property than *"the measurement reads preset
composition"*.

*(b) Only two of the three rows can flip.* Reconstructed the control with
`modules_add` (block-list form; the inline `[a, b]` form is refused by the
grammar). **This is my reconstruction, not the author's code — the plan commits
no NC-B1 script:**

```
content-security now selected: True
   scripts/content_scan.py             -> yes
   scripts/run_security_audit.py       -> —  (DID NOT FLIP)
   dev/modules/content-security.md     -> yes
```

`scripts/run_security_audit.py` is installed by the **`python-security`** module,
not `content-security`. Measured over all 20 modules. And `python-security` is
selected by **none** of the three presets.

So the B6 table's `—` in that row is correct but for a **different reason** than
the other two, and the plan's single printed cross-check
(`content-security in modules: False`) is offered as evidence for three rows
while supporting only two. An implementing agent executing NC-B1 literally
observes 2-of-3 and must either record a failed control or quietly reconcile it
— and the plan gives no guidance for either. The row needs its own line: *`—`
because no preset selects `python-security`*, with its own flip test.

**[I4] — every citation is pinned to HEAD; every decider is pinned to nothing.
(The plan's own recurring failure, reflexively.)**

The plan is explicit and correct that *"every line citation in this plan is a
HEAD `eacb7dd` citation"* because the working tree is unstable. It then specifies
~30 commands to **RUN**, none of which say *against what checkout*. Run from the
repository, every one executes the **working tree**.

The working tree is not a near-copy of HEAD:

```
bootstrap/_scaffold/config.py   | 441 ++++++--
bootstrap/_scaffold/lockfile.py | 270 ++++++--
bootstrap/_scaffold/install.py  |  33 ++
bootstrap/_scaffold/upgrade.py  |  26 ++
bootstrap/verify_integrity.py   |   8 +-
5 files changed, 686 insertions(+), 92 deletions(-)
```

Tracing each cited line into the working tree:

| HEAD citation | HEAD text | working tree |
| --- | --- | --- |
| `bootstrap/_scaffold/config.py:43` | `return _minimal_yaml_parse(text)` | **text absent from the file** |
| `bootstrap/verify_integrity.py:118` | `for finding in forked_facade_findings(target, lock):` | **text absent from the file** |
| `bootstrap/verify_integrity.py:47` | `lock = read_lockfile(target)` | line 48 |
| `bootstrap/_scaffold/install.py:887 / :982 / :1088` | — | lines 888 / 983 / 1089 |

The plan says *"two of the citations below already differ from it by one line."*
Measured: **four** differ by one line, and **two do not exist in the working tree
at all**. The understatement is not cosmetic, because of what replaced them:

* **`config.py`'s fail-open is already gone.** `_yaml_load` is now a
  *"Compatibility alias for `_minimal_yaml_parse`"* (`:47`–`:53`) and
  `load_config` calls `_minimal_yaml_parse` directly (`:413`); PyYAML is not
  consulted on the profile path. Chunk E row 4's decider — *"feed the profile
  loader a `.yml` line it cannot parse, **with PyYAML unavailable in a scratch
  environment**; … the run establishes the current behaviour so the sibling
  lineage's fix has a **before-state** to be measured against"* — would, run from
  the repo, exercise the **post-fix** loader and record it as the before-state.
  The framing (PyYAML availability) no longer describes the code path at all.
* **The fork advisory's call site has already changed** (`forked_facade_findings(`
  now multi-line at `:123`). B1 row 4's decider would exercise the sibling's
  uncommitted fix while the row's verdict says *"target-supplied at HEAD"*.

This is the plan's own named recurring failure — *the artifact under verification
supplying the material used to verify it* — one layer up: the register would
record runs whose **subject** is neither HEAD nor any committed state, under
verdicts stated about HEAD. The fix is one sentence in *Verification*: **every
decider runs against a clean checkout of the commit its row cites**
(`git archive <sha> | tar -x -C <scratch>`), never the working tree. I used
exactly that to reproduce Chunk C row 5, and it took one command.

**[I5] — Chunk G's restore oracle is wrong against a dirty tree, and would
destroy sibling sessions' uncommitted work. (Safety, not just measurement.)**

Chunk G perturbs **repository files** in place and verifies restore with
*"`git diff <path>` is empty and `git status --short` shows no residue."*

`git diff <path>` empty means *matches the index/HEAD*. For a file another
session has modified, its baseline is **not** empty — so "restore until `git
diff` is empty" is an instruction to **discard the sibling's uncommitted
change**. The files at risk are not hypothetical; at the time of this review:

```
 M bootstrap/verify_integrity.py      <- Chunk C rows 4-5 cite it
 M bootstrap/_scaffold/config.py      <- Chunk E row 4 cites it
 M bootstrap/tests/test_verify_integrity.py   <- B4 enforcer candidate
 M bootstrap/tests/test_lockfile_module.py    <- B4 enforcer candidate
 M bootstrap/tests/test_scaffold.py           (appeared during this review)
 M bootstrap/BOOTSTRAP.md                     (appeared during this review)
```

Two files became dirty *while this review ran* — another session is writing now.

The plan's *Gate accounting* notices the dirty tree, but only to decline a suite
figure. It does not connect it to Chunk G's perturb/restore, and the plan-level
invariant *"No repository file is modified outside Chunk B — enforced by `git
status --short`"* is unsatisfiable as stated: `git status --short` is not clean
at baseline and will not be at any chunk end.

*Correct oracle:* capture `git hash-object <path>` **before** the perturbation
and compare after — index-independent, and it preserves a sibling's uncommitted
bytes. (The `## Code review` section already prescribes `git hash-object` against
`git rev-parse HEAD:<path>` for the auditor — which has the *same* bug, since
`HEAD:<path>` is not the pre-perturbation state of a dirty file.) Better still,
per [I4], perturb a clean scratch checkout and never touch the repository.

**[I6] — B2 row 3 is pre-marked MET and its own decider falsifies it.**

B2's property has two clauses: the check *"binds its verdict to that name"* **and
its output names what it actually verified."* Row 3 (`verify_integrity.py`) is
recorded **MET**, with the evidence being the careful wording at `SECURITY.md:47`
— which is a property of the *document*, not of the check's output.

Ran the row's own decider (*"run `--target <A>` and `--target <B>` … confirm each
output names the lockfile it actually read"*) against two scratch installs from a
clean HEAD extract:

```
--- A ---
verify_integrity: OK -- 55 recorded file(s) match dev/.cairn/cairn-lock.yml (4 adopter-authored living-state file(s) ...)
--- B ---
verify_integrity: OK -- 55 recorded file(s) match dev/.cairn/cairn-lock.yml (4 adopter-authored living-state file(s) ...)
```

**Byte-identical.** The success path names a *repository-relative* lockfile path
— the same string for every target — so the answer does not name the object the
question was about. The decider the plan specifies returns NOT MET, or at best
MET-by-residual, for a row the plan has already written MET.

The row's negative control, by contrast, **passes and passes well**:

```
verify_integrity: no/unparseable dev/.cairn/cairn-lock.yml under /…/tgtC
  -- FAIL CLOSED (cannot attest integrity without a lockfile).
```

The failure path names the target; the success path does not. That asymmetry is
the finding, and it is a one-line fix in a module this plan is fenced out of —
so the row is properly **NOT MET, owner: the `verify_integrity` successor**, not
MET. (Mitigating: `--target` is `required=True` at `bootstrap/verify_integrity.py:149`,
so there is no silent-CWD variant of the hazard.)

This is the concrete cost of [I10] — the tables were drawn before the deciders
were run.

**[I7] — Chunk H's staleness mechanism fails B1 reflexively, and NC-H1's first
leg is a tautology.**

H2's staleness check is `git log -1 --format=%cI -- <surface list>` compared
against the dated `### Code review -- <reviewer> -- <date>` heading. Both inputs
— **the surface list and the date** — live inside `dev/plans/release-security-bar.md`,
the artifact whose freshness is being decided. By B1's own property: the
conclusion depends on material supplied by the artifact under verification, with
no independent channel and no stated residual. A surface omitted from the list is
invisible to the check, permanently and silently. That is the bar's own B1
violation in the bar's own tripwire.

Two smaller defects in the same mechanism:

* **`%cI` is committer date** — rewritable via `GIT_COMMITTER_DATE`, and reset by
  any rebase or cherry-pick, so it is not monotonic with content change. A
  release-gating freshness check should compare **commit identity**: record
  `git rev-parse HEAD` at audit time and report stale iff `git log <recorded>..HEAD
  -- <surfaces>` is non-empty. Same cost, no clock trust.
* **NC-H1 leg 1 is not a control.** *"Confirm the timestamp it returns is the one
  `git log -1 --format=%cI -- <one known-recent path>` returns for the most
  recently touched member"* compares the command **to itself** with a subset of
  its arguments. It validates `git log`'s multi-path semantics — the check —
  never the hazard. The hazard is *a surface changed after the audit and the
  command did not say stale*; the control that perturbs it is to commit a change
  to a surface-list member in a scratch clone with a date after the audit heading
  and confirm the command reports stale. Leg 2 (empty vs false-fresh) is a
  genuine control and should stay.

**[I8] — NC-A1 is a tautological positive control, and Set 1 gets no stated
residual though B1 and B3 both quantify over it.**

NC-A1 plants a fabricated verification step *"in the sweep's idiom"* and confirms
the sweep finds it. A plant constructed to match the pattern the sweep looks for
cannot fail; it demonstrates the sweep is live, not that it is complete. The real
Set 1 hazard is a verification step documented in an idiom the pattern list does
not anticipate — the same hazard NC-A3 handles honestly for Set 3, with a
deliberate **miss** leg whose missing form is quoted into A4 as the residual.

Set 1 has no such leg and **A4 states a residual only for Set 3**. Yet Set 1 is
the higher-exposure enumeration: B1 quantifies over it explicitly (*"For every
verification step in Set 1"*), and B3's Set 3 sweep is scoped by it. An
incomplete Set 1 silently shrinks two bar items at once, and nothing in the plan
would report it.

*Fix:* give NC-A1 the NC-A3 shape — a caught plant **and** a deliberately-missed
plant, with the missed form quoted and A4 extended to state a Set 1 residual.
Set 2's union is better defended (NC-A2's two legs, and its manifest-external
oracle is a genuinely independent channel — a real scaffold run, correctly noted
in the *Channel note*), so this is a Set-1-specific gap.

**[I9] — NC-B2's decider is never defined, and its "exactly 2 → 0" claim is
tautological in the shape most likely to be built.**

NC-B2 turns on a *"claim-vs-table check"* that appears nowhere else in the plan:
no command, no pattern list, no home. It cannot be a script — *"Building any
checker for the bar"* is explicitly out of scope — so it is a grep or a manual
read. Chunk F then makes it load-bearing a second time (*"run against `git show
HEAD:<file>` and against the working file, exactly as NC-B2 does"*), for every
corrected sentence in B3.

If the pattern is derived from the two known-bad sentences (the natural way to
write it, and both share the literal string `content-security +`), then "exactly
2 before, 0 after" is guaranteed by construction: the correction deletes the
string the check greps for. That is perturbing the check dressed as perturbing
the document. The acceptance criterion built on it — *"it fixes the count so a
third passage appearing later is a visible change rather than a silent one"* —
is then true only for a third passage **phrased in the same idiom**, which is an
overclaim by the bar's own B3 standard.

*Fix:* commit the pattern list beside the check (as A3 already promises to do for
Set 3, *"the pattern list is committed, not summarized"*), state that the check
is idiom-bounded, and route its miss into A4's residual rather than into an
acceptance criterion.

**[I10] — Chunk A is declared first, but four register tables are already
drawn, and nothing lets Chunk A's output change them.**

The sequencing rationale is emphatic: *"Chunk A is first because every other item
quantifies over its enumerations — a register built before the fence is countable
is a diagnostic wearing a table."* Agreed, and it is the right principle.

But B1's five rows, B2's four, B5's five and B6's nine are **already written into
this plan**, pre-Chunk-A, carried from the proposal and re-verified. The
enumerations that are supposed to generate the row sets will run against row sets
that already exist. No text says what happens when they disagree — whether a Set
1 member absent from B1's table becomes a new row, a residual, or is silently
dropped.

[I6] is this concern's first casualty: B2 row 3 was marked MET before its decider
was run, and running it falsifies the row. Where a table and a decider disagree,
the pre-drawn table is the thing that will be believed under time pressure.

*Fix, one sentence in Chunk A:* Chunk A's enumerations **supersede** the pre-drawn
tables; any Set member with no row becomes a row (or an explicitly stated
residual), and any pre-drawn row with no Set member is struck. Without it the
fence-first ordering is asserted rather than practised.

**[I11] — the correction Chunk B prescribes still asserts a standing gate, and
so still violates B3.**

Chunk B directs that lines 123 / 164 be *"corrected to name only the gate the
preset actually installs (`security-review`, measured `yes` above) and to phrase
the scanner as an action the adopter runs rather than a standing gate."*

Measured what `security-review` installs:

```
security-review adds: ['dev/modules/security-review.md']
content-security adds: ['dev/modules/content-security.md', 'scripts/content_scan.py',
                        'scripts/content_scan_allowlist.txt', 'scripts/content_scan_residuals.txt',
                        'scripts/content_scan_roots.txt', 'scripts/content_scan_runner.py']
```

`security-review` installs **one Markdown document** and no executable, no hook,
no trigger. So the surviving half of the sentence — *"…security-review gates
apply to the drafted filing body before it leaves the deployment"* — remains a
claim that something **fires automatically**, for a module that ships a review
practice. B3's property is exactly: *"Where nothing fires it automatically, the
sentence says 'run this' rather than implying a standing gate."*

The prescribed correction fixes B6 (reach) and leaves B3 (claim honesty) broken
on the same clause — in the plan's only file edit, in a document that [the plan's
own finding] is lockfile-uncovered. The retained trailing sentence at `:166`
(*"Run the scrub scanner on the draft explicitly before submitting"*) is the
correct idiom and the plan says so; the `security-review` clause should converge
on it too.

**[I12] — NC-A2's monkeypatch rule is stated more broadly than it holds, and the
over-broad form walks into the trap it warns about.**

The plan says: *"Patch the module that binds the registry, not the module that
defines it — `bootstrap/_scaffold/install.py` binds by value at import, and
patching `bootstrap._scaffold.config` is a silent no-op."*

For `_MODULE_MAPPINGS` this is **correct**: it is defined at
`bootstrap/_scaffold/config.py:641` and imported by name into `install.py`
(`from .config import (… _MODULE_MAPPINGS …)`, `install.py:28`–`:35`), so a
`setattr` on `config` leaves `install`'s binding untouched.

But NC-A2's stated goal is *"so one preset **gains a row**"*, and preset
composition is `_PRESETS` at `bootstrap/_scaffold/config.py:1205`, read by
`expand_preset` **from its own module**. Patching `install` cannot reach it;
patching `config` is the only thing that works. An agent applying the rule as
written ("patch install, never config") to a preset-composition perturbation gets
precisely the silent no-op the rule exists to prevent.

*Fix:* scope the rule to the object — `_MODULE_MAPPINGS` → patch `install` (or
mutate the shared dict, which works through either name); `_PRESETS` → patch
`config`.

**[I13] — minor: `bootstrap/PROVENANCE.md:204` is cited as "the comparison"; it
is the extraction.**

At HEAD, `:204`–`:207` is the awk block that extracts `CAIRN_SIGNED_NAME`; the
binding comparison is at `:208` (`[ "$CAIRN_SIGNED_NAME" = "$CAIRN_TAG" ] || {`).
The plan cites `:204` as *"the comparison"* in *What landed*, and B2's table
again says `:204` *"compares the signed name to the name asked for."*

Worth fixing because B2 is **the answer-binding item** and this is its evidence
cell: the plan gets the same distinction exactly right one row down for
`verify-ref.sh` (*":335 extracts … :340 refuses on mismatch"*). The
`extract` / `compare` split is the property; the citation should show it. All
other 23 citations I checked resolve exactly, including `:202`, `:236`, `:335`,
`:340`, `:354`, `:129`, `:188`, `:229`, `:317`, `:245`, `:248`, `:509`, `:786`,
`:792`, `:798`, `:803`, `:806`, `:34`, `:47`, `:118`, `:43`, `:1088`, `:982`,
`:887`, `:597`, `:387`, `:132`, `:47`, `:51`, `:123`, `:164`.

### Covered

Run under the canonical interpreter (`~/conda_envs/lhm/bin/python3.13`, 3.13.13),
`PYTHONDONTWRITEBYTECODE=1`, HEAD `eacb7dd`. **No repository file was modified;
no commit, add, or mv was performed.** Scratch work ran in
`/private/tmp/claude-501/…/scratchpad`, outside the tree.

**Required checkers — both clean.**

```
$ python scripts/claim_check.py dev/plans/release-security-bar.md
claim_check: dev/plans/release-security-bar.md -- 4 path(s) exempted by claim-check-allow:
  … dev/modules/onboarding/high-rigor-legacy.md, scripts/content_scan.py,
    scripts/run_security_audit.py, dev/modules/content-security.md
claim_check: dev/plans/release-security-bar.md -- OK, no claim-check flags.   [exit 0]

$ python scripts/check_cairn.py dev/plans/release-security-bar.md
check_cairn: OK -- 1 Markdown file(s) scanned; no issues.                     [exit 0]
```

The four `claim-check-allow` exemptions are correctly scoped: three are the B6
adopter-tree destinations no preset installs (the finding), one is NC-A2's
manifest-external destination. Each has a template source that resolves; I
confirmed all four sources exist under `templates/modules/team-gated/` and
`templates/onboarding/`.

**Citations.** All 31 `<file>:<line>` citations checked against
`git show eacb7dd:<file>`. **30 exact**; one imprecise ([I13]). Working-tree
divergence measured separately ([I4]).

**Commits.** `b93f8e9`, `5c91c23`, `1dabe4d`, `0c6d9de`, `3a2a201`, `18cbf66`,
`3cda505` all resolve and carry the subjects the plan attributes to them.

**Figures — every one reproduced.**

| Claim | Measured |
| --- | --- |
| `scaffold.py --manifest` → 95 data rows | 96 lines, 1 header → **95** ✓ |
| `frozen_files` 164 entries | **164** ✓; `verify_integrity.py` the only touched-or-contemplated key present ✓; `high-rigor-legacy.md`, `SECURITY.md`, `runtime-contract.md`, `SAFETY.md`, `CHANGELOG.md`, `PLANNING.md` all **not** frozen ✓ |
| `check_cairn` OK over 180 Markdown files, 68 external links | **180 / 68**, exit 0 ✓ |
| 180 of 234 tracked Markdown files | `git ls-files '*.md'` → **234** ✓ |
| 117 tests in the four enforcer modules | `--collect-only` → **117** ✓ |
| lockfile 81 `"dst"`; no `dev/modules/onboarding` record | **81** ✓; grep empty ✓ |
| `dev/modules/onboarding/` holds 3 installed files | ✓ |
| onboarding hashes `c829de48…` / `739bb012…` | ✓ both |
| `lifecycle_planner.py` twin byte-identical `f1552fc7…` | ✓ both |
| module / manifest counts 6-59, 11-77, 14-80 | ✓ all three |
| B6 reach table, 9 rows × 3 presets | **reproduces exactly**, all 27 cells ✓ |
| "two false passages", lines 123 / 164 | ✓ both live at HEAD, identical clause |
| other onboarding sources carry no reach claim | ✓ `solo-greenfield.md`, `collaborative-team.md`, `docs/agent-team-onboarding.md`, `docs/dev-tour.md` all clean |
| three sibling plans read `open` with code in the tree | ✓ `scan-coverage`, `release-authenticity`, `byline-classification` (and three more) |
| F2: no scheduled trigger in the repository | ✓ `.github/` exists, 7 files, **no `workflows/`** |
| `## Plan review — the brief…` not parsed as a section | ✓ `_HEADER_RE` returns no match |

**Deciders reconstructed and run.**

* **Chunk C row 5 — the coordinated lockfile tamper. REPRODUCES.** Clean HEAD
  extract → scaffolded `solo-greenfield` → baseline `OK` (55 files) → marker
  appended to `scripts/claim_check.py` → `modified (hash mismatch)` **[negative
  control fires]** → that record's hash rewritten in the target's own lockfile →
  `verify_integrity: OK -- 55 recorded file(s) match`, marker still on disk
  **[the finding]**. Both directions, exactly as specified. The plan's central
  MET-by-residual row is sound.
* **Chunk D row 3 — the target-substitution analogue. FALSIFIES the row.** See
  [I6]. Negative control (no lockfile → fail closed, names the target) passes.
* **NC-B1 — the B6 flip test. FALSIFIES the stated expectation.** See [I3].
  2 of 3 rows flip.
* **The plan-review gate — presence vs tier. FALSIFIES the plan's protection.**
  See [I1]. Two probes, violation present then absent.
* **`_HEADER_RE` behaviour** on three heading forms, confirming both the plan's
  claim (em-dash heading unparsed) and its blind spot (tier not captured into
  any gate).

*Reconstructions marked:* the NC-B1 harness, the two lifecycle-planner probes,
the tamper harness and the two-target run are **my code**, written in scratch;
the plan commits no scripts for these. They exercise the plan's stated
procedures, not the author's implementations of them.

**Scope boundaries.** Checked the six out-of-scope fences. Five hold cleanly:
`verify_integrity.py` untouched; the default-security-stance change deferred;
`runtime-contract.md` / `SECURITY.md` / `SAFETY.md` contributed-not-edited; no
checker built; the B6 pinning test deliberately absent with the reasoning stated.
The sixth — `templates/onboarding/high-rigor-legacy.md` as "unclaimed" — does not
hold ([I2]). No sibling's surface is otherwise absorbed, and I found no silent
widening past the Decision: the D4 override is correctly followed (the row is
registered, not fixed), and D3 is correctly escalated rather than assumed, with
both forms drafted.

**Gate accounting.** Verified independently and correct as written: no frozen
file touched, no `bootstrap/_scaffold/` file touched (so no AST re-anchor), the
manifest unmoved at 95, `quality_gate --sub neutrality` runs clean over
`templates/` (informational vendor-ok entries only, none in
`templates/onboarding/`). The decision **not** to assert a suite figure against a
dirty tree is right and I did not assert one either.

### Not covered / low confidence

* **The signature constructions were not run** — Chunk C rows 2–3 (attacker
  roster inside the tagged tree) and Chunk D rows 1–2 (tag substitution, plus the
  header-bounding control against a `tag ` line in the message body). These need
  throwaway key generation and are the plan's most security-load-bearing
  deciders. I read the code paths (`verify-ref.sh:335/340/354`,
  `PROVENANCE.md:202`–`:210`) and they look correct, but **reading is not
  running** and this is exactly the class where reading has failed before. The
  External round should run these first.
* **B5's fold rows were not exercised.** I did not feed Cyrillic-homoglyph or
  mathematical-bold bylines through `_fold_word`, and did not verify the R2
  three-class residual empirically. The MET-by-residual reasoning is persuasive
  on inspection; it is unverified here.
* **Chunk E row 5's residual-location question is open.** The plan cites
  **`AGENTS.md`** as where the `_resolve_interpreter` limitation is stated. Cairn's
  root `AGENTS.md` is a Cairn dev document — outside the fence — and
  `templates/core/AGENTS.md` does **not** carry the sentence (checked). The
  *shipped* statement is the docstring at `templates/skills/_lib/lifecycle.py:399`–`:402`
  (*"shape validator, not an authenticator … neither Python identity nor binary
  provenance"*), which installs to `tools/lifecycle.py`. So the residual almost
  certainly **does** reach an adopter and the row is probably fine — but the
  plan's decider watches the wrong file, and *"the residual is only a residual
  while the sentence exists"* is being asserted about a document an adopter never
  receives. Low confidence on the verdict, high confidence the citation should
  move to the docstring. I did not chase whether a docstring satisfies *"written
  where a reader meets the tool."*
* **The full suite was not run**, deliberately, for the plan's own stated reason.
* **Chunk A's enumerations do not exist yet**, so Set 1 and Set 3 could not be
  assessed on content — only their controls' design ([I8], [I9]).
* **The 68 external links were not probed.**
* **The structural blind spot, restated.** I cannot tell you whether the six
  properties are the **right six**, or whether the fence is where an outsider
  would draw it. Those are the two questions the tier exists for, and a same-type
  read is the wrong instrument for both. Everything above is the mechanical half.

### Recommendation for the second round

**Revise, then External.** The design is sound and the mechanical record is
unusually clean; nothing here argues against the plan's shape. But three findings
should be dispositioned **before** an External reviewer spends their round on
them, because they are cheap to fix and would otherwise consume the expensive
read:

* **[I1] must be dispositioned before any burndown chunk**, and it is the
  Maintainer's call, not an author's — the gate is currently green on this file
  because of this review. Option (c) (delete the enforcement claim, keep the rule
  as convention) costs one sentence and is honest; option (a) (rename this
  heading to an unparsed form) restores the block immediately.
* **[I2] needs a one-line ownership ruling.** Three lineages, three beliefs, and
  the named claimant is silent. This gates Chunk B — the only chunk needing
  approval.
* **[I4] and [I5] need one sentence each in *Verification***: deciders run
  against a clean checkout of the cited commit; restore is verified by
  pre-perturbation `git hash-object`, never by `git diff` emptiness. Without
  them, the register's evidence will be about code that is neither HEAD nor any
  committed state, and Chunk G risks destroying a sibling session's uncommitted
  security work.

[I3], [I6], [I8]–[I13] are register-quality corrections that can ride the same
revision; [I6] specifically should flip B2 row 3 off MET before an auditor finds
it, since [I10]'s fix is what prevents the next one.

**On the plan's four questions**, briefly, since it asked:

1. *Is every negative control a perturbation of the hazard?* **Mostly yes, and
   the misses are patterned.** Chunk C row 5, Chunk D rows 1–2's
   header-bounding leg, Chunk E's rejected-input leg, Chunk G's discrimination
   leg and NC-A2's manifest-external leg are all genuine hazard perturbations —
   several are excellent. The failures cluster where the control was written
   *from the answer*: NC-B1 ([I3]), NC-A1 ([I8]), NC-B2 ([I9]), NC-H1 leg 1
   ([I7]). Sampled three at random as instructed, then all of them.
2. *Is the two-reads reading of the audit's home right?* **Yes on the mechanism**
   — I verified `:786` fires at `executing`/`review`/`archived` on plan-review
   and `:792` fires at `archived` on code-review; they are different stages and
   the plan reads them correctly. **But the reading is weaker than the plan
   thinks**, because neither gate reads a tier ([I1]). Splitting the reads is
   still right; the argument for it should not rest on mechanical enforcement.
3. *Is Chunk A's enumeration honest about its own miss?* **For Set 3, yes** —
   NC-A3's deliberate miss is genuinely the right design and A4 states it as a
   finding. **For Set 1, no** ([I8]), and Set 1 is what B1 and B3 quantify over.
4. *Is B1's `verify_integrity` row correctly blocked?* **Yes.** The row is not
   quietly marked MET, the Chunk F dependency is explicit, F3's escape is on the
   Maintainer fence, and the deadlock is named in advance. I reproduced the
   underlying finding. This is the best-executed row in the plan.

**On the two things the plan invited a reviewer to strike:** I would **keep**
both. Chunk G's discrimination leg is the only thing separating B4 from the
weaker form that demonstrably failed — cutting it would return the item to the
state that produced the origin incident. And **not** pinning the B6 table with a
test is the right call, but only if [I7]'s staleness command is repaired: the
plan's own reasoning is that the tripwire substitutes for the pin, and a tripwire
whose surface list is supplied by the artifact it is checking does not.


## Response to plan review -- Claude (author) -- 2026-08-04

**Model**: claude-opus-5 (exact id `claude-opus-5`).

> **The single most important fact in this Response, stated before any
> disposition: the tree moved 61 commits between the review's HEAD `eacb7dd` and
> this Response's HEAD `6618e54`, and three of those commits are the sibling
> lineages this plan's register was pinned to as *in flight*.** The review
> predicted that drift precisely ([I4]) and it has now **landed as commits**.
> Every figure below was re-measured against `6618e54`; nothing is carried from
> the review, and where a review figure does not reproduce that is reported as
> plainly as where it does.

### Standing — what this Response is and is not

I am the plan's author responding to an **Internal** (same-agent-type) plan
review. This Response **does not discharge the declared `required(External)`
tier**, and nothing in it should be read as doing so. Its job is narrower and
stated up front:

* Disposition all thirteen findings, each with mechanical residue.
* Re-measure every figure the review states, against the live tree.
* Record the three findings the *tree itself* has produced since the review.

The review's own recommendation was **"Revise, then External."** This Response
is the revise half. The External half is untouched and remains owed.

---

### Re-measurement — what reproduces, what does not

Run under the canonical interpreter `/Users/kendal30/conda_envs/lhm/bin/python3.13`
(CPython 3.13.13), `PYTHONDONTWRITEBYTECODE=1`, at HEAD `6618e54`, working tree
carrying no tracked modifications. All scratch work ran outside the repository.

**Figures that REPRODUCE unchanged.**

| Claim (plan or review) | Re-measured at `6618e54` |
| --- | --- |
| `scaffold.py --manifest` → 95 data rows | 96 lines, 1 header → **95** ✓ |
| `frozen_files` map, 164 entries | **164** ✓ |
| `bootstrap/verify_integrity.py` the only frozen key among files this plan touches or contemplates | ✓ — and `templates/onboarding/high-rigor-legacy.md`, `SECURITY.md`, `doctrine/runtime-contract.md`, `bootstrap/SAFETY.md`, `CHANGELOG.md`, `dev/PLANNING.md` all **not** frozen ✓ |
| 68 external links not probed | **68** ✓ |
| 117 tests in the four enforcer modules (`--collect-only`) | **117** ✓ |
| B6 reach table, 9 controls × 3 presets | **reproduces exactly — all 27 cells** ✓ |
| module / manifest counts 6–59, 11–77, 14–80 | ✓ all three |
| lockfile carries 81 `"dst"` records; `grep 'dev/modules/onboarding'` empty | **81** ✓; grep returns 0 ✓ |
| `dev/modules/onboarding/` holds 3 installed files | ✓ |
| onboarding hashes `c829de48…` / `739bb012…` | ✓ both, byte-for-byte |
| `lifecycle_planner.py` twin byte-identical `f1552fc7…` | ✓ both |
| F2: `.github/` exists, 7 files, **no `workflows/`** | ✓ — 7 files; `ISSUE_TEMPLATE`, `PULL_REQUEST_TEMPLATE`, `labels.yml` only |
| `## Plan review — the brief…` is not parsed as a section | ✓ `_HEADER_RE` returns no match |
| `quality_gate.py --sub neutrality` | exit 0, informational `vendor-ok` entries only, **none** in `templates/onboarding/` ✓ |
| the seven cited commits `b93f8e9` `5c91c23` `1dabe4d` `0c6d9de` `3a2a201` `18cbf66` `3cda505` | all resolve, all carry the attributed subjects ✓ |
| `dev/PLANNING.md` R2's three measured classes; R3's **3 of 4** variants, Cyrillic open | ✓ both, at `dev/PLANNING.md:328` and `:348` |
| `security-review` installs exactly one Markdown file, zero executables | ✓ — `['dev/modules/security-review.md']` |
| `run_security_audit.py` ships with `python-security`, not `content-security` | ✓ — and `python-security` is selected by **0 of 3** presets |
| `bootstrap/profiles/high-rigor-legacy.yml` carries no module selection | ✓ — exactly three keys, comments stripped |
| `_MODULE_MAPPINGS` holds 20 modules | **20** ✓ |

**Figures that DO NOT reproduce.** Reported as findings, not as inconveniences.

| Claim | Stated | Re-measured at `6618e54` |
| --- | --- | --- |
| `check_cairn` scans 180 Markdown files | 180 | **195** |
| tracked Markdown files | 234 | **249** |
| *"two of the citations below already differ from it by one line"* | 2 | **9 of 28** citations in the plan body no longer resolve to the cited text; 4 are +1 shifts, 3 are a +12 block move, **2 no longer exist** |
| `_MODULE_MAPPINGS` at `bootstrap/_scaffold/config.py:641` (review [I12]) | :641 | **:713** |
| `_PRESETS` at `bootstrap/_scaffold/config.py:1205` (review [I3]) | :1205 | **:1277** |
| `expand_preset` at `bootstrap/_scaffold/config.py:1422` (review [I3]) | :1422 | **:1494** |
| `modules_add` at `bootstrap/_scaffold/config.py:1154` (review [I3]) | :1154 | key list at **:1213**; the read at **:1529** |
| `_yaml_load` alias at `config.py:47`–`:53`; `load_config` calls at `:413` (review [I4]) | :47/:413 | **:46**–`:53`; the call at **:485** |
| the comparison in `bootstrap/PROVENANCE.md` at `:208` (review [I13]) | :208 | **:220** — commit `7bb2072` moved the whole block +12 |
| the review's six dirty tracked files (review [I5]) | 6 modified | **0 modified** — the tree is clean of tracked modifications at this Response |

Two of those non-reproductions are the review being **right about the direction
and wrong about the magnitude** — which is the more useful half. The citation
count is the clear case: the plan said two citations were off by one; the true
figure against the live tree is nine moved, two of them gone entirely.

**The full citation ledger, re-derived.** Twenty-eight distinct `<file>:<line>`
citations appear in the plan body (excluding the landed review section). At
`6618e54`, **19 still resolve to the text the plan cites** and **9 do not**:

```
MOVED  bootstrap/PROVENANCE.md:202       -> the bind-comment is now :214
MOVED  bootstrap/PROVENANCE.md:204       -> the awk extraction is now :216
MOVED  bootstrap/PROVENANCE.md:236       -> the three properties enumerate from :246
MOVED  bootstrap/_scaffold/config.py:43  -> the fail-open fallback NO LONGER EXISTS
MOVED  bootstrap/_scaffold/install.py:887   -> :888
MOVED  bootstrap/_scaffold/install.py:982   -> :983
MOVED  bootstrap/_scaffold/install.py:1088  -> :1089
MOVED  bootstrap/verify_integrity.py:47     -> :48
MOVED  bootstrap/verify_integrity.py:118    -> the target-supplied call NO LONGER EXISTS
```

**Deciders re-run at `6618e54`, not inherited.**

* **Chunk C row 5 — the coordinated lockfile tamper. STILL REPRODUCES.** Clean
  `git archive HEAD` extract into scratch → scaffolded `solo-greenfield` →
  baseline `verify_integrity: OK -- 55 recorded file(s) match
  dev/.cairn/cairn-lock.yml` → marker appended to `scripts/claim_check.py` →
  `modified (hash mismatch): scripts/claim_check.py`, exit 1 **[negative
  control fires]** → that one record's `hash` field rewritten in the target's own
  lockfile → `verify_integrity: OK -- 55 recorded file(s) match`, exit 0, marker
  still on disk **[the finding]**. This survives `fork-advisory-semantics`
  landing in the same module. **The plan's central MET-by-residual row is sound
  at HEAD.**
* **[I6] — B2 row 3. FALSIFIES the row, and now by inspection as well as by
  run.** Two `solo-greenfield` installs into distinct scratch targets; both
  verifier invocations emit a **byte-identical** line naming
  `dev/.cairn/cairn-lock.yml`. Confirmed structurally:
  `bootstrap/verify_integrity.py:139` interpolates only `_LOCKFILE_REL`, a
  repository-relative constant, while the fail-closed path at
  `bootstrap/verify_integrity.py:50` interpolates `{_LOCKFILE_REL} under
  {target}`. The failure path names the object; the success path does not.
  `--target` is `required=True` at `bootstrap/verify_integrity.py:149`, so there
  is no silent-CWD variant.
* **[I1] — the plan-review gate. FALSIFIES the plan's protection, at HEAD.** Two
  probes on scratch copies outside the repository, status line changed to
  `executing`:

```
A. Internal review section REMOVED:
   lifecycle-planner: VIOLATION: status is 'executing' and 'Plan review:
     required', but no '## Plan review' section has landed (review-before-implement).

B. the LANDED Internal review section present, nothing else changed:
   lifecycle-planner: structural conformance: current state is structurally sound.
   lifecycle-planner: -> review
```

  The mechanism is exactly as the review describes: `_HEADER_RE`
  (`tools/lifecycle_planner.py:509`) captures `role` — for the landed heading it
  captures `'Internal, same-agent-type; security lens'` — and `_has_kind`
  (`tools/lifecycle_planner.py:693`) compares only `kind`. The gate at
  `tools/lifecycle_planner.py:787` never reads `role`.
* **Checkers, both clean at `6618e54`.** `claim_check.py` → OK, exit 0 (5
  exemption *events* over 4 distinct globs — the review's "4" counted distinct
  paths, mine counts events; both are right about the same allow-list).
  `check_cairn.py dev/plans/release-security-bar.md` → OK, exit 0.

---

### What the tree did to this plan while the review was being written

Three sibling lineages the register pins rows to have **landed**, each with its
own External code review. This is not a finding against the review; it is the
register going stale in the direction the plan's own edge-case list predicted
(*"A sibling lineage moves a line this plan quotes"*). It is recorded here
because a Response that dispositioned thirteen findings and left four register
rows describing a tree that no longer exists would have failed the same way the
review's [I4] warns about.

* **`fork-advisory-semantics` landed at `9bd6752`**, code review at `7192224`
  (Antigravity, External, security lens). `bootstrap/verify_integrity.py:123`–
  `:124` now reads `forked_facade_findings(target, lock,
  upstream=trusted_upstream(CAIRN_ROOT))`. **Chunk C row 4's stated flip
  condition is satisfied** — the change landed *and* its code review confirms
  the comparison bytes come from the caller's checkout. But that review also
  records residual **R10**: candidate *selection* remains lock-derived
  (`hash != base_hash`) even though the *verdict* operand is now caller-supplied.
  So the row does not flip to clean MET; it becomes decidable, with R10 named.
* **`profile-parse-fail-open` landed at `e7394cb`**, code review at `89f7b7b`.
  The fail-open is gone: `_yaml_load` is a compatibility alias at
  `bootstrap/_scaffold/config.py:46` and `load_config` calls
  `_minimal_yaml_parse` directly at `bootstrap/_scaffold/config.py:485`. PyYAML
  is not consulted on the profile path at all. **Chunk E row 4's decider —
  *"with PyYAML unavailable in a scratch environment"* — no longer describes any
  code path**, and its stated purpose (establish a before-state for the sibling's
  fix) is now unreachable: the fix is the state.
* **`gate-claims-vs-enforcement` completed its entire burndown** — Chunks A–E at
  `8d23afe`, `1e47c08`, `2244eca`, `d1eb48c`, `84fbef4`, plus an External code
  review. This is the fact that turns [I2] and produces [R1] below.

---

### Disposition, finding by finding

Thirteen findings. **Thirteen accepted** — eleven in full, two with
modification. None declined. Every acceptance has a numbered row in *Amendments
in force*; a finding accepted only in prose would be the failure mode this
Response exists to avoid.

**[I1] — the plan-review gate cannot distinguish Internal from External.
ACCEPTED IN FULL, and the remedy has an owner the review could not have known
about.**

Reproduced at HEAD, both probes, above. The plan's blockquote is wrong on **two**
counts, not one, and the second is new since the review:

1. *The enforcement claim.* The gate is presence-only. The sentence *"keeps
   reporting the section missing until a real `###` review sub-heading lands"* is
   a standing-gate claim for a property nothing enforces — the plan's own **B3**
   violation, in the plan's own gate-blocking mechanism. The review is exactly
   right that this is the plan's *perturb-the-hazard* rule turned on itself: the
   committed probe perturbed the heading's **shape** and never the reviewer's
   **tier**.
2. *The prescribed heading shape is itself unbuildable.* Measured for this
   Response: `dev/plans/review-gate-enforcement.md:307`–`:313` records that
   appending a `### Plan review` at the end of a plan **nests under the last H2,
   not under the container**, so putting a pass under the container requires
   inserting into prior file content — which append-only forbids. That plan's
   Response revises its own A.1 to a dated `## Plan review -- <reviewer> --
   <date>` H2 pass. Corpus check at `6618e54`: `grep -rhoE "^#{2,3} Plan review"
   dev/plans dev/proposals` → **59 headings, all `##`, zero `###`**. My reviewer
   used `##` and was right to; this plan's instruction to use `###` was wrong.

**The remedy is not mine to apply and is already owned.** `review-gate-enforcement`
— proposal accepted at `eb1b2b7`, plan opened at `8dfb664`, External plan review
at `f83f20e`, Response at `eaf1109` — carries a Chunk C.1 node *"declared tier
satisfied"* (`dev/plans/review-gate-enforcement.md:103`) with a single-property
falsifier. That is the review's option (b), further along than the review knew.

I take the review's **option (c)** for this plan's own text — delete the
enforcement claim, keep the rule as an explicitly-unenforced convention, and name
the lineage that will make it a gate. I decline to take **option (a)**: renaming
the landed review's heading would edit a prior section (append-only forbids it),
would be a *silent re-gating* of a section its author committed, and is not the
author's to do to a reviewer's byline. **The choice between (a), (b) and (c) as
the durable resolution is the Maintainer's and is in `openQuestions`.**
Amendments **A1**, **A2**, **A3**.

**[I2] — the ownership vacuum on `templates/onboarding/high-rigor-legacy.md`
lines 123 / 164. ACCEPTED IN FULL, and materially strengthened since the
review.**

Re-measured at `6618e54`, every leg reproduces:

* `dev/plans/default-security-stance.md:133` — *"Owned by
  `gate-claims-vs-enforcement`. Whichever lands second must not re-assert what
  this one falsifies."* ✓ verbatim, same line.
* `dev/plans/default-security-stance.md:871` — *"Already owned by
  `gate-claims-vs-enforcement`; **no migration needed**"* ✓ verbatim, same line.
* `grep -c "high-rigor-legacy"` over both `dev/plans/gate-claims-vs-enforcement.md`
  and `dev/proposals/2026-08-03-claude-gate-claims-vs-enforcement.md` → **0 and
  0** ✓.
* Both passages still live at `templates/onboarding/high-rigor-legacy.md:123`
  and `:164`, identical clause ✓.

**What is new:** the named claimant is no longer *silent*, it is **finished**.
`gate-claims-vs-enforcement` landed all five chunks and an External code review.
Its actual file surface was `AGENTS.md`, `bootstrap/container/floor-gate.sh`,
`bootstrap/container/recipe.md`, `bootstrap/DEPENDENCY_BUDGET.md`,
`doctrine/runtime-contract.md`, `bootstrap/fidelity-check.md`,
`doctrine/lifecycle.md`, `bootstrap/SAFETY.md` — and never
`templates/onboarding/`. A lineage that has completed its burndown without
taking two lines it was believed to own has *demonstrated* it does not own them.
So `default-security-stance`'s belief is now stale-and-wrong rather than merely
in conflict, and the vacuum is a fact rather than an inference.

That does **not** license me to take the lines. The plan's own fence — *"an
agent taking a claimed file to unblock its own bar is exactly how a
one-proposal-per-file rule dies"* — applies with more force, not less, when the
evidence favours me. Chunk B is gated on a Maintainer ownership ruling.

The second-order point is accepted too and is live: `default-security-stance` is
still `**Status**: open` with only an Internal plan review, and its pre-declared
changelog text (`dev/plans/default-security-stance.md:871`, row 7) would make
Chunk B's correction false in the opposite direction. Amendments **A4**, **A5**.

**[I3] — NC-B1 is falsified by the tree and names a file that cannot carry the
edit. ACCEPTED IN FULL; the review's mechanism is right, its line numbers are
not.**

Both legs reproduce:

* `bootstrap/profiles/high-rigor-legacy.yml`, comments stripped, is exactly
  `project_name`, `test_command`, `preset` — **no module selection**. The roster
  lives in `_PRESETS`, read by `expand_preset`.
* `content-security` ships `['dev/modules/content-security.md',
  'scripts/content_scan.py', 'scripts/content_scan_runner.py',
  'scripts/content_scan_roots.txt', 'scripts/content_scan_residuals.txt',
  'scripts/content_scan_allowlist.txt']` — six files, and
  **`run_security_audit.py` is not among them**. It ships with `python-security`,
  which is selected by **0 of 3** presets. So only **2 of 3** rows can flip.

The review's line numbers for the mechanism have all moved (`_PRESETS`
`:1205`→**`:1277`**, `expand_preset` `:1422`→**`:1494`**, `modules_add`
`:1154`→ key list **`:1213`** / read **`:1529`**). The amendment carries live
numbers and says they are volatile. Amendment **A6**.

**[I4] — every citation is pinned to HEAD; every decider is pinned to nothing.
ACCEPTED IN FULL. This is the finding the tree has since proved.**

The review predicted the working tree would become the subject of runs whose
verdicts are stated about HEAD. Sixty-one commits later that working tree *is*
HEAD, and the two rows the review flagged are the two rows whose subject
changed. The plan's *"two of the citations … differ by one line"* is
**falsified: nine of twenty-eight**. Amendments **A7**, **A8**, **A15**, **A16**.

**[I5] — Chunk G's restore oracle is wrong against a dirty tree. ACCEPTED IN
FULL. The instance does not reproduce; the hazard does.**

The review's six dirty tracked files are gone — the tree carries no tracked
modification at this Response. That is not a refutation. A tracked file
(`dev/plans/planner-line-semantics.md`) went from modified to committed
*between two tool calls of this Response*, which is the hazard demonstrating
itself. `git diff <path>` empty means *matches the index/HEAD*, so "restore
until `git diff` is empty" remains an instruction to discard whatever a
concurrent session holds. `git hash-object` captured **before** the perturbation
is index-independent and correct in both tree states. The review is also right
that the `## Code review` brief prescribes the same broken oracle against
`git rev-parse HEAD:<path>`; that is amended too. Amendments **A9**, **A10**,
**A11**.

**[I6] — B2 row 3 is pre-marked MET and its own decider falsifies it. ACCEPTED
IN FULL.**

Reproduced by run and confirmed by inspection above. The verdict cell flips to
**NOT MET**, owner: the `verify_integrity` successor named on the deferred
ledger. I want to be precise about what is wrong and what is not: the *document*
sentence at `SECURITY.md:47` is careful and true, exactly as the plan says. It
is simply not evidence for B2's second clause, which is about the **check's
output**. The row cited the right sentence for the wrong clause. Amendment
**A12**.

**[I7] — the staleness mechanism fails B1 reflexively; NC-H1 leg 1 is a
tautology. ACCEPTED IN FULL.**

Both halves are correct and the first is the sharper one: H2's inputs — the
surface list *and* the audit date — both live inside the artifact whose
freshness is being decided, which is B1's property violated by the bar's own
tripwire, with no independent channel and no stated residual. `%cI` is committer
date and is rewritable and non-monotonic; commit identity is the right
comparand. NC-H1 leg 1 compares the command to itself with fewer arguments; leg
2 is a genuine control and is retained. Amendments **A13**, **A14**.

**[I8] — NC-A1 is a tautological positive control; Set 1 gets no residual.
ACCEPTED IN FULL.** A plant constructed in the idiom the sweep greps for cannot
fail. Set 1 is the higher-exposure enumeration precisely because B1 quantifies
over it explicitly and B3's sweep is scoped by it, so an incomplete Set 1
shrinks two bar items at once and nothing reports it. NC-A1 takes NC-A3's
two-leg shape and A4 gains a Set 1 residual. Amendment **A17**.

**[I9] — NC-B2's decider is never defined; its "exactly 2 → 0" is tautological.
ACCEPTED IN FULL.** The check is load-bearing twice (NC-B2, and Chunk F's
per-sentence control) and defined nowhere. Building a script for it is fenced
out, so it is a grep — and a grep derived from the two known-bad sentences is
guaranteed to return 2 then 0, because the correction deletes the string it
greps for. Amendment **A18**.

**[I10] — Chunk A is declared first, but four register tables are already drawn.
ACCEPTED IN FULL, and [I6] is its first casualty exactly as the review says.**
The sequencing principle is right and the plan does not practise it. Without a
supersession rule, a table and a decider that disagree resolve in favour of the
pre-drawn table under time pressure — which is what produced [I6]. Amendment
**A19**.

**[I11] — the prescribed correction still asserts a standing gate. ACCEPTED IN
FULL.** Re-measured: `security-review adds: ['dev/modules/security-review.md']`
— one Markdown document, no executable, no hook, no trigger. Correcting *"the
high-rigor-legacy profile's content-security + security-review gates apply"* to
name only `security-review` fixes B6 and leaves B3 broken on the same clause,
in the plan's only file edit. The retained trailing sentence is the correct
idiom and the whole clause should converge on it. Amendment **A20**.

**[I12] — NC-A2's monkeypatch rule is over-broad and walks into its own trap.
ACCEPTED IN FULL; line numbers re-derived.** The rule is correct for
`_MODULE_MAPPINGS` (defined in `config`, imported by name into `install` at
`bootstrap/_scaffold/install.py:28`–`:35`, so a `setattr` on `config` is a
no-op) and wrong for `_PRESETS`, which `expand_preset` reads from its own
module — so "patch install, never config" produces precisely the silent no-op
the rule exists to prevent. Live line numbers: `_MODULE_MAPPINGS` at
`bootstrap/_scaffold/config.py:713` (review said `:641`); `_PRESETS` at
`bootstrap/_scaffold/config.py:1277` (review said `:1205`). Amendment **A21**.

**[I13] — `bootstrap/PROVENANCE.md:204` is the extraction, not the comparison.
ACCEPTED WITH MODIFICATION — the finding was right at `eacb7dd` and its
prescribed fix is now stale.**

Verified against `git show eacb7dd:bootstrap/PROVENANCE.md`: at the review's
HEAD, `:202` was the bind-comment, `:204` the awk extraction, `:208` the
comparison. The review was correct. But commit `7bb2072` moved the whole block
**+12 lines**, so at `6618e54` the plan's `:202` lands on `git init --bare`,
its `:204` lands on a fetch refspec, and its `:236` lands on *"Discard the
workspace and report."* The live positions are: bind-comment **`:214`**,
extraction **`:216`**, comparison **`:220`**, the three-properties enumeration
from **`:246`**. The modification is that I re-cite to live numbers *and* record
the block as volatile, rather than applying the review's `:204`→`:208`
substitution, which would have replaced one stale citation with another.
Amendment **A22**.

---

### Three findings this Response contributes

These are mine, produced by re-deriving rather than inheriting. They are
recorded here because a Response that only dispositioned would have left the
register describing a tree that no longer exists.

**[R1] — Chunk F names two owners, and at HEAD neither owns its row. The
deadlock the plan designed F3's escape for is not a contingency; it is the
opening state.**

The plan instructed its own successor to check this — *"re-check whether that
plan claims this row before recording the disposition"* — so this is the plan
working, not the plan failing.

* **Row 1, `doctrine/runtime-contract.md:132`** (*"Detects tampered apparatus
  before it can self-audit"* — still live, still at :132, still falsified by
  Chunk C's tamper run, which I re-ran). Attributed to
  `gate-claims-vs-enforcement`. That lineage has now **completed** its burndown.
  It touched `doctrine/runtime-contract.md` at exactly three places — `:46`,
  `:185`, `:189`, the *"floor CI check"* naming rows at
  `dev/plans/gate-claims-vs-enforcement.md:850`–`:852` — and its ledger contains
  **no** row for `:132`. **UNOWNED.**
* **Row 2, `SECURITY.md:51`** (*"flagging any post-install modification"* —
  still live, still at :51). Attributed to `agent-context-scrub`. That plan's
  `SECURITY.md` surface is three *new residual bullets* about the scrub escape
  table (`dev/plans/agent-context-scrub.md:492`–`:494`), none of which touches
  the `:51` clause. The other claimant of that file, `scan-coverage`, claims
  `SECURITY.md:66` (`dev/plans/scan-coverage.md:611`), not `:51`. **UNOWNED.**

This is load-bearing, not bookkeeping: B1's `verify_integrity` row is
MET-by-residual **only if** these two sentences are corrected, and with no owner
for either, the bar's largest row is blocked on nobody. Amendment **A23**.

**[R2] — three register rows are stale in the good direction and one figure pair
is stale in the bad direction.**

Chunk C row 4 and Chunk E row 4 both describe code that no longer exists
(above). And the plan's known-omission (e) figure — *"180 of 234"* — is now
**195 of 249**. The gap is unchanged at 54 files, which is worth saying: the
coverage *deficit* is stable even though both figures moved, so the deferral is
still correctly sized. Amendments **A15**, **A16**, **A24**.

**[R3] — the plan's prescribed review-heading shape is the one shape append-only
cannot produce.** Folded into [I1] above and Amendment **A3**, because it is the
same sentence.

---

### Amendments in force

Each row names the superseded text **verbatim** and states what replaces it.
This plan is append-only: the original text stays where it is, and this table is
what governs at implementation. Where a row supersedes a verdict cell, the
implementing agent records the new verdict in the register it builds, not by
editing the pre-drawn table above.

| # | Superseded text (verbatim) | Replaced by | From |
| --- | --- | --- | --- |
| **A1** | *"so it is not parsed as a section at all, and the gate at `tools/lifecycle_planner.py:786` keeps reporting the section missing until a real `###` review sub-heading lands"* | **Struck as a false enforcement claim.** The container heading is indeed unparsed — that half is measured and true. The gate at `tools/lifecycle_planner.py:787` reads **only the section *kind***: `_has_kind` (`tools/lifecycle_planner.py:693`) never consults the `role` group `_HEADER_RE` (`tools/lifecycle_planner.py:509`) captures. **Any** section whose kind begins "Plan review" clears it, at `##` or `###`, Internal or External. The tier rule is an **explicitly-unenforced convention** until `review-gate-enforcement` Chunk C.1 (`dev/plans/review-gate-enforcement.md:103`) lands. | [I1] |
| **A2** | *"**No burndown chunk lands before the `## Plan review` section is in the tree.**"* | *"**No burndown chunk lands before an External plan review is in the tree. This is a convention this repository does not currently enforce** — the gate cleared when the Internal review landed. Until `review-gate-enforcement` gates on the declared tier, the only thing standing between this plan and a premature implementation is a reader."* | [I1] |
| **A3** | *"**The landed review appends here as a `### Plan review -- <reviewer> -- YYYY-MM-DD` sub-heading**"* | *"The landed review appends as a dated `## Plan review -- <reviewer> -- <date>` H2 pass."* A `###` pass appended at end-of-file nests under the last H2, **not** under the container, so producing one requires inserting into prior content, which append-only forbids — measured and recorded at `dev/plans/review-gate-enforcement.md:307`–`:313`. Corpus at `6618e54`: **59 `##` headings, 0 `###`**. The plan's own reviewer used `##` and was correct. | [I1], [R3] |
| **A4** | *"**Two false reach passages in `templates/onboarding/high-rigor-legacy.md`** — the only unclaimed file the proposal's hand-off table leaves inside this bar's budget (Chunk B)."* | *"Two false reach passages in `templates/onboarding/high-rigor-legacy.md`, a file **two sibling plans record as owned by a third lineage that does not claim it and has now finished without taking it**. `dev/plans/default-security-stance.md:133` and `:871` assign the lines to `gate-claims-vs-enforcement`; that lineage's plan and proposal return **0** matches for `high-rigor-legacy` and its completed Chunks A–E never touched `templates/`. **Chunk B does not start until the Maintainer rules on ownership.**"* | [I2] |
| **A5** | *(new criterion — Chunk B)* | **Chunk B acceptance gains a precondition and a sequencing note.** Precondition: a Maintainer ownership ruling. Note: `default-security-stance` (`**Status**: open`, Internal plan review only) pre-declares changelog text at `dev/plans/default-security-stance.md:871` making `content-security` a default install — which would make Chunk B's correction **false in the opposite direction**. Whichever lands second re-checks the other's sentence. | [I2] |
| **A6** | *"In a scratch copy of `bootstrap/profiles/high-rigor-legacy.yml` outside the repository, add `content-security` to the preset's module selection; re-run the eight-line measurement against the scratch config; confirm the three `content_scan` rows flip from `—` to `yes` for that column only."* | **NC-B1 becomes three legs, because the three rows are `—` for two different reasons.** (i) *Preset-composition leg:* the profile carries **no** module selection — three keys only. Perturb `_PRESETS` (`bootstrap/_scaffold/config.py:1277`, read by `expand_preset` at `:1494`) **in a scratch process**, never a scratch profile. (ii) *Adopter-override leg:* `modules_add` (read at `bootstrap/_scaffold/config.py:1529`) is a different property and is measured separately if at all. (iii) *The third row does not flip and must not be expected to:* `scripts/run_security_audit.py` ships with **`python-security`**, not `content-security`; `python-security` is selected by **0 of 3** presets. Expected result is **2 of 3**, with row 3 flipping only under a `python-security` perturbation. **All line numbers here are `as_of 2026-08-04` and volatile** — `_PRESETS` moved from `:1205` to `:1277` between the review and this Response. | [I3] |
| **A7** | *"**Every line citation in this plan is a HEAD `eacb7dd` citation for the same reason** — the working tree is not a stable reference this week, and two of the citations below already differ from it by one line."* | *"Every line citation in the plan body is an `eacb7dd` citation. **Re-measured at `6618e54`: 19 of 28 still resolve; 9 do not.** Four are +1 shifts (`install.py:887/982/1088`, `verify_integrity.py:47`), three are a +12 block move in `bootstrap/PROVENANCE.md` from commit `7bb2072`, and **two no longer exist** (`config.py:43`, `verify_integrity.py:118`) because the sibling fixes landed. The implementing agent **re-pins the whole citation baseline to its own opening commit** and does not carry `eacb7dd`."* | [I4], [R2] |
| **A8** | *(new sentence — Verification)* | **"Every decider runs against a clean checkout of the commit its row cites — `git archive <sha> \| tar -x -C <scratch>` — never against the working tree, and the row records the sha it ran against."** Used for every reproduction in this Response; it costs one command. | [I4] |
| **A9** | *"**Byte-identical restore, verified.** After each perturbation, `git diff <path>` is empty and `git status --short` shows no residue."* | *"**Byte-identical restore, verified against a pre-perturbation capture.** Record `git hash-object <path>` **before** the perturbation; after restoring, confirm the hash matches. `git diff <path>` emptiness is **rejected** as the oracle: it compares to the index/HEAD, so on a file a concurrent session has modified it is an instruction to destroy that session's uncommitted work."* | [I5] |
| **A10** | *"*No repository file is modified outside Chunk B.* Enforced by `git status --short` at each chunk end."* | *"No repository file is modified **by this plan** outside Chunk B. Enforced per-path: for every path a chunk touched, `git hash-object <path>` matches its pre-chunk capture. A bare `git status --short` is **not** the enforcer — it reports every concurrent session's work and is not clean at baseline in general."* | [I5] |
| **A11** | *"**Confirm each perturbation's byte-identical restore** with `git hash-object` against `git rev-parse HEAD:<path>`, not by reading the ledger."* | *"…with `git hash-object` against **the implementing agent's recorded pre-perturbation hash**, not against `git rev-parse HEAD:<path>` — `HEAD:<path>` is not the pre-perturbation state of a file another session had modified, so the auditor's own oracle carried the same defect."* | [I5] |
| **A12** | *"\| `bootstrap/verify_integrity.py` \| "the recorded install" \| yes, and it says so \| **MET** — the wording at `SECURITY.md:47` … is careful and true as far as B2 goes \|"* | **Verdict flips to NOT MET.** Re-run at `6618e54`: two distinct scratch targets produce **byte-identical** output naming `dev/.cairn/cairn-lock.yml`. The success path (`bootstrap/verify_integrity.py:139`) interpolates only the repo-relative constant `_LOCKFILE_REL`; the fail-closed path (`:50`) interpolates `{_LOCKFILE_REL} under {target}`. B2's second clause — *"its output names what it actually verified"* — fails on the success path. Owner: the `verify_integrity` successor on the deferred ledger. `SECURITY.md:47` stays cited as a **true document sentence that is not evidence for this clause**. | [I6] |
| **A13** | *"the staleness command that consumes it: `git log -1 --format=%cI -- <surface list>` compared against the dated `### Code review -- <reviewer> -- <date>` heading"* | *"…record `git rev-parse HEAD` at audit time in the register, and report stale **iff `git log <recorded>..HEAD -- <surface list>` is non-empty**. Commit identity, not `%cI`: committer date is rewritable via `GIT_COMMITTER_DATE` and is reset by rebase/cherry-pick, so it is not monotonic with content change. **And the surface list carries a stated residual**: it and the audit date both live inside the artifact whose freshness they decide, which is this bar's own **B1** property violated — a surface omitted from the list is invisible permanently and silently. Stated as a finding in the register, not as a caveat."* | [I7] |
| **A14** | *"Take the surface list, run the `git log -1` command, and confirm the timestamp it returns is the one `git log -1 --format=%cI -- <one known-recent path>` returns for the most recently touched member."* | **Leg 1 replaced.** That compares the command to itself with a subset of its arguments — the check, not the hazard. Replacement: **in a scratch clone, commit a change to a surface-list member dated after the audit heading and confirm the command reports stale.** Leg 2 (a path with no commits returns empty rather than a false-fresh timestamp) is a genuine control and is **retained unchanged**. | [I7] |
| **A15** | *"\| The fork advisory \| comparison bytes \| target-supplied at HEAD (`bootstrap/verify_integrity.py:118`); caller-supplied in the uncommitted `fork-advisory-semantics` work \| **in flight** \|"* | **Row is no longer in flight; its stated flip condition is satisfied.** `fork-advisory-semantics` landed at `9bd6752` with an External code review at `7192224`. `bootstrap/verify_integrity.py:123`–`:124` now passes `upstream=trusted_upstream(CAIRN_ROOT)`. **But the row does not become clean MET:** that code review records residual **R10** — candidate *selection* stays lock-derived while the *verdict operand* is caller-supplied. The register dispositions it as MET-by-residual with R10 quoted, or re-derives it against the landed code. | [I4], [R2] |
| **A16** | *"\| The profile loader's fallback YAML parse — `bootstrap/_scaffold/config.py:43` → `_minimal_yaml_parse` \| **guesses** instead of refusing \| **in flight** — `profile-parse-fail-open` \|"* | **Row's subject no longer exists.** `profile-parse-fail-open` landed at `e7394cb` (code review `89f7b7b`). `_yaml_load` is a compatibility alias at `bootstrap/_scaffold/config.py:46` and `load_config` calls `_minimal_yaml_parse` directly at `:485`; PyYAML is not on the profile path. **Chunk E row 4's decider is void as written** — *"with PyYAML unavailable in a scratch environment"* describes no code path, and the before-state it was to establish is unreachable. The row is re-derived against the closed grammar, or struck with a note saying why. | [I4], [R2] |
| **A17** | *"add a Markdown file documenting a fabricated verification step in the sweep's idiom; re-run A1's sweep against the scratch root; confirm the planted step appears"* | **NC-A1 takes NC-A3's two-leg shape.** A caught plant **and** a deliberately-missed plant — a verification step written in an idiom the pattern list does not anticipate — with the missing form **quoted into A4**, and **A4 extended to state a Set 1 residual**. A plant built to match the pattern the sweep greps for cannot fail; it shows the sweep is live, not that it is complete. Set 1 is the higher-exposure enumeration: B1 quantifies over it explicitly and B3's sweep is scoped by it, so an incomplete Set 1 shrinks two items at once. | [I8] |
| **A18** | *"Run the claim-vs-table check against `git show HEAD:templates/onboarding/high-rigor-legacy.md` and confirm it reports **exactly 2** false reach claims; run it against the corrected file and confirm **0**."* | **The check is defined before it is run, or NC-B2 is not run.** Commit the pattern list beside it (as A3 already promises for Set 3), state in terms that it is **idiom-bounded**, and route its miss into **A4's residual** rather than into an acceptance criterion. A pattern derived from the two known-bad sentences returns 2-then-0 *by construction* — the correction deletes the string it greps for — which is perturbing the check dressed as perturbing the document. The claim *"a third passage appearing later is a visible change"* is narrowed to *"a third passage **in the same idiom**"*. **Chunk F's per-sentence control inherits this amendment**, since it is specified as *"exactly as NC-B2 does"*. | [I9] |
| **A19** | *(new sentence — Chunk A)* | **"Chunk A's enumerations supersede the pre-drawn tables. Any Set member with no row becomes a row or an explicitly stated residual; any pre-drawn row with no Set member is struck; and where a pre-drawn verdict and a run disagree, the run governs and the disagreement is recorded."** Without this, fence-first ordering is asserted rather than practised — and [I6] is the first casualty, a row marked MET before its decider was run. | [I10] |
| **A20** | *"corrected to name only the gate the preset actually installs (`security-review`, measured `yes` above) and to phrase the scanner as an action the adopter runs rather than a standing gate"* | *"…and **the `security-review` clause converges on the same imperative idiom**. Measured: `security-review` installs `['dev/modules/security-review.md']` — one Markdown document, no executable, no hook, no trigger. Naming only `security-review` fixes **B6** and leaves **B3** broken on the same clause, because *'…security-review gates apply … before it leaves the deployment'* still asserts something fires automatically. The retained trailing sentence — *'Run the scrub scanner on the draft explicitly before submitting'* — is the target shape for the whole clause, not just the scanner half."* | [I11] |
| **A21** | *"Patch the module that *binds* the registry, not the module that defines it — `bootstrap/_scaffold/install.py` binds by value at import, and patching `bootstrap._scaffold.config` is a silent no-op."* | **Rule is scoped to the object.** For **`_MODULE_MAPPINGS`** the rule holds: defined in `config`, imported by name into `install` (`bootstrap/_scaffold/install.py:28`–`:35`), so `setattr` on `config` is a no-op — patch `install`, or mutate the shared dict. For **`_PRESETS`** it is **inverted**: `expand_preset` reads `_PRESETS` from its own module, so patching `install` cannot reach it and **`config` is the only thing that works**. NC-A2's stated goal is *"one preset gains a row"* — a `_PRESETS` perturbation — so the rule as written walks into the trap it warns about. Live: `_MODULE_MAPPINGS` at `bootstrap/_scaffold/config.py:713`, `_PRESETS` at `:1277`. | [I12] |
| **A22** | *"`bootstrap/PROVENANCE.md:202` — *"Bind the SIGNED name to the name you asked about"*; the comparison is at `bootstrap/PROVENANCE.md:204`; the three bootstrap properties are enumerated from `bootstrap/PROVENANCE.md:236`."* (and B2's table cell repeating `:204` as *"compares the signed name to the name asked for"*) | **All three citations re-pinned, and the extract/compare split made explicit.** At `6618e54`: bind-comment **`:214`**; awk **extraction** **`:216`**; the **comparison** `[ "$CAIRN_SIGNED_NAME" = "$CAIRN_TAG" ]` at **`:220`**; the three properties from **`:246`**. The review's `:204`→`:208` correction was right at `eacb7dd` and is now itself stale — commit `7bb2072` moved the block **+12**. B2 is the answer-binding item, so its evidence cell must show extract-vs-compare the way the `verify-ref.sh` row already does (`:335` extracts, `:340` refuses — **both still exact at `6618e54`**). **`bootstrap/PROVENANCE.md` is a volatile surface and belongs on Chunk H's staleness surface list.** | [I13] |
| **A23** | *"\| `doctrine/runtime-contract.md:132` \| … \| `gate-claims-vs-enforcement` (accepted `3a2a201`; its plan was **being opened concurrently** … — re-check whether that plan claims this row before recording the disposition) \| … \|" and "\| `SECURITY.md:51` \| … \| `agent-context-scrub` (plan open) … \| … \|"* | **The re-check the plan asked for was run, and both owner cells are falsified. Both rows are UNOWNED at `6618e54`.** `gate-claims-vs-enforcement` has **completed** Chunks A–E plus an External code review; its `doctrine/runtime-contract.md` surface is `:46`/`:185`/`:189` only (`dev/plans/gate-claims-vs-enforcement.md:850`–`:852`) and its ledger has no `:132` row. `agent-context-scrub`'s `SECURITY.md` surface is three new residual bullets on the scrub escape table (`dev/plans/agent-context-scrub.md:492`–`:494`), not the `:51` clause; `scan-coverage` claims `SECURITY.md:66` (`dev/plans/scan-coverage.md:611`), not `:51`. **Consequence: F3's escape is engaged at the outset, not as a contingency** — B1's `verify_integrity` row is blocked on two sentences nobody owns. Both passages verified still live and still falsified. | [R1] |
| **A24** | *"(**180 of 234** tracked Markdown files, `as_of 2026-08-04`; the proposal recorded 173 of 218)"* | *"(**195 of 249** tracked Markdown files, `as_of 2026-08-04` at `6618e54`; the review-time figure was 180 of 234 and the proposal recorded 173 of 218). **The deficit is stable at 54 files across all three snapshots**, so the deferral is still correctly sized even though both figures moved. `python scripts/check_cairn.py` → OK over **195** files, 68 external links not probed."* Chunk B's criterion *"`≥180` Markdown files"* was written defensively and **still holds**; it is not amended. | [R2] |

---

### Does this Response clear the plan to implement?

**No.** Stated plainly, because the plan's own machinery cannot say it:

1. **The declared tier is not discharged.** `Plan review: required(**External**)`.
   What has landed is an **Internal** (same-agent-type) review plus this
   author's Response. External's floor is a different agent type or a human.
   Neither the review nor this Response is one. **The tier remains owed.**
2. **The gate says otherwise, and the gate is wrong.** Measured at `6618e54`:
   the plan-review gate is **green on this file right now**, and was green from
   the moment the Internal review landed. Anyone running
   `tools/lifecycle_planner.py next` on this plan at `executing` gets
   *"structurally sound"*. That is [I1], and it means **nothing mechanical
   stands between this plan and a premature implementation**. Amendments A1–A3
   make the plan say so; they do not make the tree enforce it.
3. **Three items need a Maintainer ruling before the chunks they gate can run** —
   [I1]'s remedy choice, [I2]'s ownership ruling (gates Chunk B), and [R1]'s
   unowned Chunk F rows (which gate B1's largest register row). They are in
   `openQuestions`.
4. **The register's own baseline must be re-taken.** Nine of twenty-eight
   citations have moved and two register rows describe code that no longer
   exists. Per A7 and A8, the implementing agent re-pins to its own opening
   commit and runs every decider against a clean checkout of the sha its row
   cites.

**What this Response does discharge:** the mechanical revision the review asked
for. All thirteen findings are dispositioned with residue; every figure the
review stated has been re-measured and reported in both directions; three
findings the tree produced since the review are recorded. Per the review's own
recommendation — *"three findings should be dispositioned **before** an External
reviewer spends their round on them"* — [I1], [I2], [I4] and [I5] are now in the
amendment table rather than waiting to consume the expensive read.

**What an External reviewer still owes, unchanged by this Response:** whether the
six properties are the **right six**, and whether the fence is drawn where an
outsider would draw it. Neither the Internal review nor this Response is the
instrument for either question, and both say so for the same structural reason.

---

### Verification of this Response

Run at `6618e54` under `/Users/kendal30/conda_envs/lhm/bin/python3.13`
(3.13.13), `PYTHONDONTWRITEBYTECODE=1`. **No repository file outside this plan
was modified; no `add`, `mv`, `stash`, `reset` or `push` was performed.** All
scratch work ran outside the tree.

```
$ python scripts/claim_check.py dev/plans/release-security-bar.md
claim_check: dev/plans/release-security-bar.md -- OK, no claim-check flags.   [exit 0]

$ python scripts/check_cairn.py dev/plans/release-security-bar.md
check_cairn: OK -- 1 Markdown file(s) scanned; no issues.                     [exit 0]
```

`git diff --numstat` on this file shows **0 deletions** — this Response is
appended, and no prior section is edited.

## Plan review -- Codex (External) -- 2026-08-05

**Verdict: REVISE.** The response did the useful cleanup: it distinguishes a
dated register from a live claim and it no longer treats an Internal review
heading as a real External gate. Three routed ownership decisions still prevent
the plan from being executable rather than merely diagnostic.

**[E1] Rule the unowned onboarding claims into this scope.**
`templates/onboarding/high-rigor-legacy.md` is demonstrably unowned by the two
lineages the record cites, and the false claims are directly about the release
bar this plan exists to make truthful. Chunk B should own their correction,
with the existing re-check against the default-security wording. Waiting for a
Maintainer ownership ruling here preserves a known false release claim for no
security benefit.

**[E2] Rule the two unowned register rows into the bar's explicit escape path.**
The `doctrine/runtime-contract.md` and `SECURITY.md` rows are not owned by the
named sibling plans. The plan should either correct those exact claims in a
bounded documentation chunk or write a durable, named backlog owner before it
can mark the register usable. A row with no owner is not an acceptable failure
mode for a release control; it is a way for a falsified security assertion to
remain visible yet indefinitely untreated.

**[E3] Make the register's scope a machine-checkable input, not a self-described
list.** A13 correctly admits that a surface omitted from the artifact's own
list is invisible forever. The proposed stale check only detects change in
paths already named. Derive the list from the release-bar mapping/claim
register, store the audit commit separately from the artifact being judged, and
add a fixture that introduces an unlisted release-facing source then proves the
coverage assertion fails. Otherwise the bar can certify freshness while a new
release claim never entered its universe.

I inspected the effective A1--A24 amendments and the response's three declared
open rulings. I did not execute the future register deciders or modify any
release-facing file; no implementation exists yet to exercise.

## Response to plan review -- Claude (author) -- 2026-08-05

**Model**: claude-opus-5 (exact id `claude-opus-5`).

> **Stated before any disposition, because it changes what the rest of this
> Response can claim: an External plan review has now landed (`a5b0f34`,
> 2026-08-05, Codex), and its verdict is REVISE. That satisfies the *presence*
> half of `required(External)` and nothing else.** The same reviewer, the same
> day, on the sibling plan `review-gate-enforcement`, wrote the standard this
> Response is held to: *"I treated the authored Response as evidence of intended
> changes, not as a replacement for the plan's executable contract. The declared
> External tier remains undischarged"* (`dev/plans/review-gate-enforcement.md:371`–`:373`).
> So every acceptance below lands as a numbered amendment row, and the answer to
> *does this clear the plan to implement* is **no**.

### Standing — what this Response is and is not

I am the plan's author responding to an **External** (different-agent-type) plan
review whose verdict is **REVISE**. Its job:

* Disposition all three findings (E1, E2, E3), each with mechanical residue.
* Re-measure every figure the review states **and every figure my own prior
  Response asserts**, against the live tree at HEAD `4385813`.
* Record the findings the tree has produced since `6618e54` — 100 commits.
* Audit the plan's own gates and say which are satisfied today.

**This Response does not discharge the External tier and does not clear the plan
to implement.** An author's Response never discharges a tier it is answering; a
REVISE verdict is a request for a further round, and the reviewer said so in
terms on a sibling plan the same day.

---

### Where the External review actually sits — the briefing's placement claim, re-derived

I was told the External review was *inserted before the existing Internal
sections, not appended at the end*. **That does not reproduce.** Measured:

```
$ git show a5b0f34 --numstat --format=
36      0       dev/plans/release-security-bar.md          # 36 insertions, 0 deletions

$ grep -n '^## ' dev/plans/release-security-bar.md | tail -3
1304: ## Plan review -- Claude (Internal, same-agent-type; security lens) -- 2026-08-04
2029: ## Response to plan review -- Claude (author) -- 2026-08-04
2557: ## Plan review -- Codex (External) -- 2026-08-05
```

The diff hunk header is `@@ -2553,3 +2553,39 @@` — a pure end-of-file append,
zero deletions, and the External section **is** the last section. There is
exactly one `## Plan review -- … (External)` heading in the file. Recorded
because a Response that had "verified" a re-ordering nobody performed would be
the same defect as a finding accepted in prose: an assertion with no measurement
under it.

---

### Re-measurement — what reproduces, what does not

Run under the canonical interpreter `/Users/kendal30/conda_envs/lhm/bin/python3.13`
(CPython 3.13.13), `PYTHONDONTWRITEBYTECODE=1`, at HEAD `4385813`. All scratch
work ran outside the repository. **100 commits** separate `6618e54` (my prior
Response) from `4385813`.

**Figures that REPRODUCE unchanged.**

| Claim (plan, review, or my prior Response) | Re-measured at `4385813` |
| --- | --- |
| `scaffold.py --manifest` → 95 data rows | 96 lines, 1 header → **95** ✓ |
| `frozen_files` map, 164 entries | **164** ✓ |
| `bootstrap/verify_integrity.py` the only frozen key among files this plan touches or contemplates | ✓ — `templates/onboarding/high-rigor-legacy.md`, `SECURITY.md`, `doctrine/runtime-contract.md`, `bootstrap/SAFETY.md`, `CHANGELOG.md`, `dev/PLANNING.md` all **not** frozen ✓ |
| 117 tests in the four enforcer modules (`--collect-only`) | **117** ✓ |
| B6 reach table, 9 controls × 3 presets | **reproduces exactly — all 27 cells** ✓ (but only after the API repair in [S1]) |
| module / manifest counts 6–59, 11–77, 14–80 | ✓ all three |
| `content-security` selected by 0 of 3 presets; `python-security` selected by 0 of 3 | ✓ both |
| `security-review` installs exactly `['dev/modules/security-review.md']` — one Markdown file, zero executables | ✓ |
| `run_security_audit.py` ships with `python-security`, not `content-security` | ✓ |
| `_MODULE_MAPPINGS` holds 20 modules | **20** ✓ |
| lockfile carries 81 `"dst"` records; `grep 'dev/modules/onboarding'` returns 0 | **81** ✓; **0** ✓ |
| `dev/modules/onboarding/` holds 3 installed files | ✓ |
| no `dev/modules/onboarding/*` destination appears in `install_manifest(modules=None)` | ✓ — **the Set 2 under-count finding still holds at HEAD** |
| onboarding hashes `c829de48…` / `739bb012…` | ✓ both, byte-for-byte |
| `bootstrap/profiles/high-rigor-legacy.yml` carries no module selection | ✓ — exactly three keys, comments stripped |
| `.github/` exists, 7 files, **no `workflows/`** | ✓ — `ISSUE_TEMPLATE`, `PULL_REQUEST_TEMPLATE`, `labels.yml` |
| `quality_gate.py --sub neutrality` | exit 0, informational `vendor-ok` entries only, **none** in `templates/onboarding/` ✓ |
| both passages live at `templates/onboarding/high-rigor-legacy.md:123` / `:164`, identical clause | ✓ |
| `doctrine/runtime-contract.md:132` — *"Detects tampered apparatus before it can self-audit"* | ✓ still live, still at `:132` |
| `SECURITY.md:47` careful wording / `SECURITY.md:51` overstatement, four lines apart | ✓ both |
| `dev/PLANNING.md` R2's three classes at `:328`; R3's **3 of 4** at `:348` | ✓ both |
| `_MODULE_MAPPINGS` `:713`, `_PRESETS` `:1277`, `expand_preset` `:1494`, `modules_add` key list `:1213` / read `:1529` | ✓ all five, unmoved since `6618e54` |
| `_yaml_load` compatibility alias at `bootstrap/_scaffold/config.py:46`; `load_config` calls `_minimal_yaml_parse` at `:485` | ✓ both |
| `bootstrap/verify_integrity.py` — `read_lockfile(target)` `:48`, fail-closed naming the target `:50`, `upstream=trusted_upstream(CAIRN_ROOT)` `:123`–`:124`, `--target` `required=True` `:149` | ✓ all four |
| `bootstrap/PROVENANCE.md` live positions: bind-comment `:214`, awk extraction `:216`, comparison `:220` | ✓ all three |
| `bootstrap/container/verify-ref.sh:335` extracts header-bounded, `:340` refuses on mismatch, `:354` pins the roster | ✓ all three |
| `tools/lifecycle_planner.py:509` `_HEADER_RE` | ✓ **unmoved** |
| `templates/skills/_lib/lifecycle.py:387` `_resolve_interpreter` | ✓ unmoved; the shipped *"shape validator, not an authenticator"* sentence at `:398`–`:402` |
| `bootstrap/tests/_gate_preflight.py:597` `anchored_roster` | ✓ |
| `bootstrap/security_check.py:129` / `:188`; `test_security_lint.py:229` / `:317` | ✓ all four |
| E1's ownership legs: `dev/plans/default-security-stance.md:133` and `:871` verbatim; `grep -c high-rigor-legacy` over the `gate-claims-vs-enforcement` plan **and** proposal → **0 and 0** | ✓ all four |
| [R1]'s legs: `gate-claims-vs-enforcement`'s `doctrine/runtime-contract.md` surface is `:46`/`:185`/`:189` only; `agent-context-scrub`'s `SECURITY.md` surface is three residual bullets; `scan-coverage` claims `SECURITY.md:66` | ✓ all three |
| [I1]'s mechanism — the plan-review gate is presence-only | ✓ **re-measured both directions today**, below |

**Figures that DO NOT reproduce.** Reported as plainly as the ones that do.

| Claim | Stated | Re-measured at `4385813` |
| --- | --- | --- |
| `check_cairn` scans **195** Markdown files (my prior Response, A24) | 195 | **176** |
| `check_cairn` — **68** external links not probed | 68 | **48** by default; **68** only under `--include-archives` |
| tracked Markdown files | 249 | **254** (196 outside `/archive/`, 58 inside) |
| *"The deficit is stable at 54 files across all three snapshots"* (A24) | 54 | **78** (176 of 254). **Falsified.** On the comparable non-archive basis it is **20** (176 of 196) |
| plan-body citations that no longer resolve (A7) | 9 of 28 | **10 of 28** — and the composition changed |
| `_has_kind` at `tools/lifecycle_planner.py:693` (review [I1], my A1) | :693 | **:697** — `:693` is now `_decisions` |
| the plan-review gate at `tools/lifecycle_planner.py:786` / `:787` | :786/:787 | **:790**–**:791** |
| the archive preconditions at `tools/lifecycle_planner.py:792`–`:806` | :792–:806 | **:797** (code review), **:802**–**:805** (follow-ups), **:808**–**:810** (fidelity) |
| `bootstrap/_scaffold/install.py:1088` *"reads `templates/onboarding/<preset_name>.md`"*; A7 re-pinned it to `:1089` | :1088 / :1089 | the read is **`src = templates_root / "onboarding" / f"{preset_name}.md"` at `:1085`**; `:1088`–`:1089` are the *warn* string. A7's "+1 shift" characterization does not reproduce |
| `bootstrap/_scaffold/install.py:982` — A7 re-pinned it to `:983` | :983 | **`:982`** still heads the docstring item *"D. Copy the full preset source file"*; A7's shift does not reproduce |
| `lifecycle_planner.py` twin byte-identical at `f1552fc7…` | `f1552fc7…` | **`e428c8c8…`** — the *property* (byte-identical twins) holds; the *figure* is stale |
| the three sibling plan/proposal citations behind A23 | un-archived plan paths | the files **moved to `dev/plans/archive/`**; line numbers hold (`:850`–`:852`, `:611`) |
| `bootstrap/PROVENANCE.md` three-properties enumeration at `:246` (A22) | :246 | the sentence spans **`:245`–`:246`**; the enumeration proper begins **`:248`** |

**The full citation ledger, re-derived rather than inherited.** Extracted every
distinct backticked `` `<file>:<line>` `` citation from the plan **body** (lines
1–1303, excluding all review and Response sections) and opened each one:
**28 distinct citations, 18 resolve to the cited text, 10 do not.**

```
RESOLVES (18)  SECURITY.md:47 :51 | verify-ref.sh:335 :340 :354 |
               security_check.py:129 :188 | _gate_preflight.py:597 |
               test_security_lint.py:229 :317 | verify_integrity.py:34 |
               runtime-contract.md:132 | high-rigor-legacy.md:123 :164 |
               skills/_lib/lifecycle.py:387 | lifecycle_planner.py:245 :248 |
               install.py:982

FAILS (10)     PROVENANCE.md:202  -> `git init --quiet --bare …`   (bind-comment is :214)
               PROVENANCE.md:204  -> a fetch refspec               (extraction :216, comparison :220)
               PROVENANCE.md:236  -> "# 6. Discard the workspace"  (three properties :245-:248)
               config.py:43       -> `_yaml = None`                (the fail-open fallback NO LONGER EXISTS)
               install.py:887     -> a comment                     (_ONBOARDING_DOC_NAMES is :888)
               install.py:1088    -> a warn string                 (the read is :1085)
               verify_integrity.py:47  -> `def verify(target)…`    (read_lockfile is :48)
               verify_integrity.py:118 -> a comment                (the call is :123-:124, WITH upstream=)
               lifecycle_planner.py:786 -> a different message     (the gate is :790-:791)
               lifecycle_planner.py:792 -> `v.append(`             (the code-review gate is :797)
```

The two `tools/lifecycle_planner.py` failures are **new since my prior
Response** — they are the citations A1, A2 and the plan's own gate-accounting
rest on, and both moved while the amendment table asserting them sat in the
file. That is the [I4] hazard reproducing against the amendments themselves.

**Deciders re-run at `4385813`, not inherited.**

* **[I1] — the plan-review gate is still presence-only. RE-MEASURED, BOTH
  DIRECTIONS.** Two scratch copies outside the repository, status line changed
  to `executing`:

```
A. full file (both review sections present):
   lifecycle-planner: current state: executing
   lifecycle-planner: structural conformance: current state is structurally sound.
   lifecycle-planner: -> review

B. same file truncated at line 1303 (both review sections removed):
   lifecycle-planner: VIOLATION: status is 'executing' and 'Plan review:
     required', but no '## Plan review' section has landed (review-before-implement).
```

  The gate at `tools/lifecycle_planner.py:790`–`:791` calls `_has_kind(art,
  "Plan review")` (`:697`), which reads only the section *kind*. `_HEADER_RE`
  (`:509`) captures `role` and nothing consults it. **The gate could not tell
  that an External review landed today — it was green before `a5b0f34` and is
  green after, for the same reason.** `review-gate-enforcement`'s Chunk C.1
  (*"declared tier satisfied"*, `dev/plans/review-gate-enforcement.md:103`) has
  **not** landed: that plan is `**Status**: open` and now carries its own
  REVISE External review (`04b0fa6`).
* **B6 reach table — REPRODUCES, all 27 cells**, after repairing the producing
  command (see [S1]). Module/manifest counts 6–59, 11–77, 14–80 reproduce.
* **The E1 ownership sweep — REPRODUCES, and is now broader.** A repository-wide
  sweep (`grep -rln "onboarding/high-rigor-legacy" dev/plans dev/proposals`,
  live **and** archived) returns nine files. Only two are claim-bearing:
  `dev/plans/default-security-stance.md` (which *defers* the lines at `:133` and
  `:871`) and this plan. The named claimant returns **0** in both its plan and
  its proposal. **No lineage in the repository claims those two lines.**
* **The E2/[R1] ownership sweep — REPRODUCES, and is now broader.** A sweep for
  `runtime-contract.md:132` / *"Detects tampered apparatus"* and for
  `SECURITY.md:51` / *"flagging any post-install"* across every live and
  archived plan and proposal returns **only this plan and its own source
  proposal** as claimants of either row. **Both rows are still UNOWNED at
  `4385813`.**
* **The E3 anchor form — DEMONSTRATED.** `refs/cairn/gate-anchor` is a real ref
  in this repository (`bootstrap/tests/_gate_preflight.py:53`), so an
  out-of-artifact audit anchor has precedent rather than needing invention. The
  amended staleness form runs today:

```
$ git log --oneline refs/cairn/gate-anchor..HEAD -- \
      SECURITY.md doctrine/runtime-contract.md templates/onboarding/high-rigor-legacy.md
2244eca gate-claims-vs-enforcement: Chunk C -- the floor-check names
5c91c23 scan-coverage: the release scan reaches every shipped .py, …
      # non-empty => STALE, which is the verdict the amended command returns
```

* **Checkers, both clean at `4385813`.** `claim_check.py
  dev/plans/release-security-bar.md` → OK, exit 0. `check_cairn.py
  dev/plans/release-security-bar.md` → OK, exit 0.

---

### Disposition, finding by finding

Three findings. **Two accepted with modification, one accepted.** None declined.
Every acceptance has a numbered row in *Amendments in force*; where a
modification exists it is because the branch the review named crosses a fence
the Decision set, and that is stated rather than absorbed.

**[E1] — rule the unowned onboarding claims into this scope. ACCEPTED WITH
MODIFICATION.**

The review is right on the substance and I re-verified every leg at `4385813`,
plus a wider sweep the prior Response did not run. No lineage in this repository
claims `templates/onboarding/high-rigor-legacy.md:123` / `:164`. The named
claimant finished its burndown without touching `templates/`. The only other
mention is a sibling that *defers* to that finished claimant. The review's
consequence-of-waiting argument is correct: an open Maintainer question is not a
neutral state — it holds a **false release claim** in a shipped, adopter-installed,
lockfile-uncovered document, in the release the bar exists to gate.

So I restore Chunk B's ownership of the two passages and strike A4's
open-ended Maintainer precondition.

**The modification, and why it is not a softening.** "Proceed on measurement"
must not become "proceed on the author's conviction" — that is the failure the
plan's own fence names (*"an agent taking a claimed file to unblock its own bar
is exactly how a one-proposal-per-file rule dies"*). So the precondition is
replaced by a **mechanical** one, not deleted:

1. Chunk B re-runs the ownership measurement **at its own opening commit** and
   pastes the output into the register (**NC-B3**, with a positive control that
   proves the check can see a claim when one exists).
2. If any leg returns a claim, Chunk B **stops and escalates** rather than
   editing.
3. Chunk B **keeps its commit-approval gate**. It edits a file outside `dev/`,
   so it loses the deliberation carve-in and the Maintainer sees the diff before
   it lands (`AGENTS.md > Git and commit workflow`). The oversight E1 wanted to
   remove from the *front* of the chunk is still on its *back*, where it costs
   nothing and blocks nothing.

Residual, stated: `default-security-stance` is still `**Status**: open` and now
carries its own **REVISE** External review (`2077a25`). Its pre-declared
changelog text (`dev/plans/default-security-stance.md:871`, row 7) would make
Chunk B's correction false in the opposite direction. A5's sequencing note
governs and is unchanged. Amendments **A25**, **A26**.

**[E2] — rule the two unowned register rows into the bar's explicit escape path.
ACCEPTED.**

The review offers two branches. I take the second and say why the first is not
mine to take.

* *Branch 1 — "correct those exact claims in a bounded documentation chunk"*
  means editing `SECURITY.md` and `doctrine/runtime-contract.md`. Both are
  fenced out of this plan's Scope, and that fence came from the **accepted
  proposal**, which handed both rows off with *"hand off, this file is
  claimed"*. Widening a plan to edit two more shipped documents is a scope
  change past the Decision, which is the Maintainer's, not the author's. It
  stays available and is in `openQuestions`.
* *Branch 2 — "write a durable, named backlog owner before it can mark the
  register usable"* — **taken.** This is fully inside the plan's authority, and
  the review's framing is the sharper half: *"A row with no owner is not an
  acceptable failure mode for a release control."*

Mechanically: F3's escape is the wrong shape for the situation and is
superseded. It was written as *escalate if an owning lineage stalls*; there is
no owning lineage, so its trigger can never fire. It is replaced by a **standing
requirement**: the register may not be reported complete or usable while any row
carries an empty owner cell; an empty owner cell is **NOT MET with a named
block**, never *in flight*; and the block clears only when a
`dev/PLANNING.md` > *Deferred follow-ups (durable home)* > **Security
apparatus** row exists naming both sentences with an owner, a revival condition
and an expiry trigger.

**The material for that row does not come from this plan.** `dev/PLANNING.md` is
a serialized shared file, so the text is **returned** below, not written; and
until it lands there, both rows stay NOT MET. That ordering is deliberate — a
backlog owner recorded only inside the artifact whose completeness it licenses
would be this bar's own B1 violation, which is the very defect E3 names one
finding later. Amendments **A27**, **A28**, plus the returned text.

**[E3] — make the register's scope a machine-checkable input. ACCEPTED WITH
MODIFICATION.**

The finding is correct and is the sharpest of the three: A13 admitted the
residual and then left the mechanism unchanged, so the admission did no work.
The proposed staleness check reads a list the artifact writes about itself and a
date the artifact writes about itself, and can therefore certify freshness over
a universe that never contained the new claim. Three sub-asks, dispositioned
separately:

* **"Store the audit commit separately from the artifact being judged" —
  ACCEPTED IN FULL.** The audit anchor becomes a repository ref,
  `refs/cairn/release-bar-audit`, created by the Maintainer at the commit that
  lands the `## Code review` section. Precedent is in the tree
  (`refs/cairn/gate-anchor`, `bootstrap/tests/_gate_preflight.py:53`) and the
  form is demonstrated running above. Ref creation joins the Chunk M fence.
* **"Derive the list from the release-bar mapping/claim register" — ACCEPTED IN
  FULL, and widened, because derivation alone does not fix the hole.** A list
  derived from the register still only sees paths the register named. So the
  surface list becomes the **union** of (i) a committed extraction over the
  register's own evidence cells and (ii) Chunk A's Set 1/2/3 enumerations,
  which are produced by sweeps that read **the tree**. Chunk A's sweeps are the
  independent channel; the register is not. And a second assertion is added
  alongside staleness — **coverage: every Set member has a register row** — with
  a Set member lacking a row recorded as a NOT MET row, not an omission.
* **"Add a fixture that introduces an unlisted release-facing source then proves
  the coverage assertion fails" — ACCEPTED AS A COMMITTED NEGATIVE CONTROL
  (NC-H2); the *standing automated* form is routed to the Maintainer.** The
  perturbation, both directions, and the discrimination leg all land as
  recorded runs — the same instrument every other row in this plan uses, and
  it is the leg that makes the coverage assertion mean something. What I cannot
  do is ship it as a standing test: *"Building any checker for the bar"* and
  *"Adding a test that pins the B6 reach table"* are both fenced out of Scope on
  the accepted proposal's standing *build nothing new* direction. Turning
  NC-H2 into a pytest is a scope widening past the Decision. It is in
  `openQuestions`, and if the Maintainer rules it required the plan needs a
  proposal-level amendment, not an author's.

Amendments **A29**, **A30**, **A31**, **A32**.

---

### Findings this Response contributes

Produced by re-deriving rather than inheriting. Each has an amendment.

**[S1] — the plan's B6 and Set 2 producing commands are void against the current
engine API. The table survives; the command does not.**

The plan specifies Set 2 as
`install_manifest(modules=expand_preset(load_config(<preset>)))` and B6's
measurement as *"the eight-line `load_config` → `expand_preset` →
`install_manifest` measurement per preset"*. At `4385813`:

```
bootstrap/_scaffold/config.py:1494
    def expand_preset(cfg) -> tuple[list[str], dict[str, object]]      # returns a 2-TUPLE
bootstrap/_scaffold/install.py
    def install_manifest(modules=None) -> list[tuple[str, str, bool]]  # rows are TUPLES, not dicts

$ install_manifest(modules=expand_preset(load_config(p)))
TypeError: unhashable type: 'list'
```

An implementing agent executing the plan's stated measurement literally gets a
`TypeError`, and the Internal review's own reconstruction (`r['dst']`) would
raise `TypeError: tuple indices must be integers`. Repaired — unpack
`(mods, summary)` and read `row[1]` — **the B6 table reproduces exactly, all 27
cells**, and the module/manifest counts hold. This is worth more than a citation
fix: it is the plan's *decider* going stale, not its evidence, and no citation
checker would ever have reported it. A new selection construct,
`_DEFAULT_ON_MODULES` (`bootstrap/_scaffold/config.py:83`), now feeds
`expand_preset`; a Set 2 enumeration that does not account for it is measuring
the wrong roster. Amendment **A33**.

**[S2] — the citation baseline moved again, and this time it moved under the
amendment table.** 18 of 28 body citations resolve; 10 do not. A7 said 9 of 28
and its per-citation characterizations for `install.py:982` / `:1088` do not
reproduce. Two of the new failures are `tools/lifecycle_planner.py:786` and
`:792` — the gate citations A1 and A2 assert. Amendment **A34**.

**[S3] — A24's stability claim is falsified.** *"The deficit is stable at 54
files across all three snapshots"* is now **78** (176 of 254). The mechanism is
visible and matters: `check_cairn` excludes `dev/**/archive/` by default
(`scripts/check_cairn.py --include-archives`), and 58 Markdown files moved into
archives across the 100 commits — so the *scanned* count fell from 195 to 176
while the *tracked* count rose from 249 to 254. On the comparable non-archive
basis the deficit is **20** (176 of 196). A24's `68` external links reproduces
only under `--include-archives`; the default is `48`. Chunk B's defensively
written criterion *"`≥180` Markdown files"* **no longer holds** at 176 and must
be re-derived, not carried. Amendment **A35**.

**[S4] — A23's supporting citations now point into `dev/plans/archive/`, and the
file's own allow-list hides it.** `gate-claims-vs-enforcement` and
`scan-coverage` archived; their line numbers hold at the new paths. The plan's
`claim-check-allow` directive (line 3) exempts both stems, so `claim_check.py`
returns OK **while silently passing over two stale paths** — a correct
exemption doing exactly what an exemption does, recorded because a reader
seeing `claim_check: OK` should not read it as *these citations resolve*.
Amendment **A36**.

**[S5] — the archive preconditions moved, and they are the plan's only genuinely
mechanical gate.** `:792`–`:806` → `:797` (code review), `:802`–`:805`
(follow-ups), `:808`–`:810` (fidelity sign-off). The *mechanism* is unchanged
and still fires; only the citations are stale. Folded into Amendment **A34**
with the rest of the planner re-pin.

---

### Amendments in force

Continues the prior Response's table; **A1–A24 remain in force unchanged except
where a row below supersedes one.** Each row names the superseded text
**verbatim**. This plan is append-only: the original text stays where it is, and
this table is what governs at implementation.

| # | Superseded text (verbatim) | Replaced by | From |
| --- | --- | --- | --- |
| **A25** | *"**Chunk B does not start until the Maintainer rules on ownership.**"* (Amendment A4) | **Struck. Chunk B owns the correction.** No lineage in this repository claims `templates/onboarding/high-rigor-legacy.md:123` / `:164` — re-verified at `4385813` by a repository-wide sweep over live **and** archived plans and proposals: nine files mention the document, only `dev/plans/default-security-stance.md` is claim-bearing and it *defers* (`:133`, `:871`), and the deferral's target returns **0** in both its plan (`dev/plans/archive/gate-claims-vs-enforcement.md`) and its proposal. Waiting preserves a false release claim in a shipped, lockfile-uncovered document for no security benefit. **Three bounded conditions replace the ruling:** (i) Chunk B re-runs the ownership measurement at its own opening commit and pastes the output (**NC-B3**, A26); (ii) any leg returning a claim **stops the chunk and escalates**; (iii) Chunk B keeps its commit-approval gate — it edits outside `dev/`, loses the deliberation carve-in, and the Maintainer sees the diff before it lands. A5's sequencing note against `default-security-stance` is **unchanged and now more live**: that plan carries its own REVISE External review (`2077a25`) and is still `**Status**: open`. | [E1] |
| **A26** | *(new criterion — Chunk B)* | **NC-B3 — the ownership re-check, RUN, both directions.** Positive leg (the hazard is the claim record, not the grep): `grep -rln "onboarding/high-rigor-legacy" dev/plans dev/proposals` and `grep -c "high-rigor-legacy"` over the deferral target's plan and proposal — expected **0 and 0**, with the full file list pasted. Control leg, so the check is not vacuous: run the identical grep shape against a lineage that **does** claim a file — `dev/plans/archive/scan-coverage.md:611` claims `SECURITY.md:66` — and confirm it returns non-zero. A sweep that returns 0 for every input decides nothing. | [E1] |
| **A27** | *"The **escape**, written before it is needed: if an owning lineage has not landed its correction when the register is otherwise complete, the row is **escalated to the Maintainer**, not taken. The bar does not edit a file another lineage claims, and it does not mark the row MET."* (Chunk F, row F3) | **F3's trigger can never fire and is replaced by a standing requirement.** F3 assumed an owning lineage that stalls; re-verified at `4385813`, a sweep for `runtime-contract.md:132` / *"Detects tampered apparatus"* and `SECURITY.md:51` / *"flagging any post-install"* across every live and archived plan and proposal returns **only this plan and its own source proposal**. There is no lineage to stall. **Replacement:** the register may not be reported complete or usable while any row carries an empty owner cell. An empty owner cell is **NOT MET with a named block**, never *in flight*. The block clears only when a `dev/PLANNING.md` > *Deferred follow-ups (durable home)* > **Security apparatus** row exists naming **both** sentences with an owner, a revival condition and an expiry trigger — **outside this plan**, because a backlog owner recorded only in the artifact whose completeness it licenses is this bar's own **B1** violation. Returned text below. The alternative branch the review offered — correcting `SECURITY.md` and `doctrine/runtime-contract.md` in a bounded documentation chunk — is a scope widening past the Decision and is in `openQuestions`. | [E2] |
| **A28** | *"The roll-up table: six items, rows, MET / MET-by-residual / in flight / NOT MET, with the date each was last decided."* (Chunk H, row H1) | *"…**plus an owner column**. The roll-up may not report the register complete or usable while any owner cell is empty; an empty owner cell renders its row **NOT MET with a named block**. **And the roll-up reports the coverage assertion (A30) and the staleness verdict (A29) as two separate cells**, because a fresh-but-incomplete universe and a stale-but-complete one fail differently and a single 'audit OK' cell hides both."* | [E2], [E3] |
| **A29** | *"…record `git rev-parse HEAD` at audit time in the register, and report stale **iff `git log <recorded>..HEAD -- <surface list>` is non-empty**."* (Amendment A13) | **The audit commit moves out of the artifact.** The Maintainer creates **`refs/cairn/release-bar-audit`** at the commit that lands the `## Code review` section; staleness is `git log refs/cairn/release-bar-audit..HEAD -- <surface list>`, non-empty ⇒ stale. Commit identity, not `%cI`, is retained from A13. Precedent: `refs/cairn/gate-anchor` is a real ref in this repository (`bootstrap/tests/_gate_preflight.py:53`), so this reuses an existing pattern rather than inventing one. Demonstrated running in *Re-measurement* above. **Ref creation is Maintainer-only** and joins the Chunk M fence as item 8; an agent creates no `refs/cairn/*`. Recording the sha *only* inside the register is struck: the artifact under verification must not supply the material used to verify it, which is the property this bar's **B1** asserts about everyone else. | [E3] |
| **A30** | *"**The register's surface list** — the explicit set of paths the register's rows depend on — plus the staleness command that consumes it"* (Chunk H, row H2) | **The surface list is derived and unioned, and gains a second assertion.** (i) *Derived leg:* a committed extraction command over the register's own evidence cells, so no path is hand-maintained. (ii) *Independent leg:* **unioned with Chunk A's Set 1 / Set 2 / Set 3 enumerations**, which are produced by sweeps that read the tree — the register is not an independent channel for its own scope, and Chunk A's sweeps are. (iii) *The coverage assertion, new and separate from staleness:* **every Set member has a register row**; a Set member with no row is recorded as a **NOT MET row**, never an omission. A13's stated residual is retained but narrowed — it now covers only what **Chunk A's sweeps** miss (the residual NC-A1/NC-A3 already quote), not everything the plan forgot to list. | [E3] |
| **A31** | *(new criterion — Chunk H)* | **NC-H2 (the coverage assertion can fail), RUN.** In a scratch checkout outside the repository, plant an **unlisted release-facing source** — one adopter-installed Markdown file asserting a security control, and one `templates/**/*.py` — re-run Chunk A's sweeps and the coverage assertion, and confirm the assertion goes **red** naming the planted paths. *Negative control:* an unperturbed scratch checkout must report the assertion **green**, or it fails for every tree and decides nothing. *Discrimination leg:* a modification to a path **already** in the surface list must be caught by the **staleness** command (A29) and **not** by the coverage assertion — the two mechanisms measure different hazards and a run that cannot separate them is measuring one thing twice. Invisible code points in any planted file are written as `U+…`, per Chunk E. | [E3] |
| **A32** | *(new criterion — Chunk H)* | **Four surfaces measured volatile this cycle are named into the surface list explicitly**, independently of whatever the derivation returns: `bootstrap/_scaffold/config.py`, `bootstrap/_scaffold/install.py`, `bootstrap/PROVENANCE.md`, `tools/lifecycle_planner.py`. Each moved a citation the register depends on between `eacb7dd`, `6618e54` and `4385813`. | [E3], [S2] |
| **A33** | *"**Set 2 table** — `install_manifest(modules=expand_preset(load_config(<preset>)))` per shipped preset"* (Chunk A, row A2) and *"**The B6 reproduction** — the eight-line `load_config` → `expand_preset` → `install_manifest` measurement per preset"* (Verification) | **Both producing commands are void as written against the current engine API and are re-derived at the implementing commit.** At `4385813`: `expand_preset` (`bootstrap/_scaffold/config.py:1494`) returns a **2-tuple** `(ordered_modules, summary)`, and `install_manifest` returns `list[tuple[str, str, bool]]` — `(src, dst, verbatim)`, **not** dicts. The plan's expression raises `TypeError: unhashable type: 'list'`; the Internal review's `r['dst']` raises `TypeError: tuple indices must be integers`. Repaired (unpack `(mods, _summary)`; read `row[1]`), **the B6 table reproduces exactly — all 27 cells** — and the counts 6–59 / 11–77 / 14–80 hold. **Set 2 must also account for `_DEFAULT_ON_MODULES` (`bootstrap/_scaffold/config.py:83`)**, a selection construct that did not exist when the plan was written and that `expand_preset` now feeds from. **No citation checker reports this class**: it is the decider going stale, not the evidence. | [S1] |
| **A34** | *"**Re-measured at `6618e54`: 19 of 28 still resolve; 9 do not.**"* (Amendment A7) | *"**Re-measured at `4385813`: 18 of 28 resolve; 10 do not.**"* New failures since A7: `tools/lifecycle_planner.py:786` (the gate is **`:790`**–**`:791`**) and `:792` (the code-review gate is **`:797`**) — the two citations A1 and A2 themselves rest on. A7's per-citation characterizations for `bootstrap/_scaffold/install.py:982`→`:983` and `:1088`→`:1089` **do not reproduce**: `:982` still heads the docstring item, and the template read is at **`:1085`** (`:1088`–`:1089` are the *warn* string). Also re-pinned: `_has_kind` `:693`→**`:697`**; the archive preconditions `:792`–`:806`→**`:797`** / **`:802`**–**`:805`** / **`:808`**–**`:810`**; `_HEADER_RE` **`:509` unmoved**; `bootstrap/PROVENANCE.md` three-properties **`:245`–`:246`**, enumeration from **`:248`** (A22 said `:246`). The `lifecycle_planner.py` twin hash is now **`e428c8c8…`** (A-row figure `f1552fc7…` stale; the byte-identical *property* holds). **The mechanisms behind every one of these are unchanged** — only the coordinates moved, which is exactly why A7 and A8 are the amendments that matter most. | [S2], [S5] |
| **A35** | *"**The deficit is stable at 54 files across all three snapshots**, so the deferral is still correctly sized even though both figures moved. `python scripts/check_cairn.py` → OK over **195** files, 68 external links not probed."* (Amendment A24) | **Falsified.** At `4385813`: `check_cairn` → OK over **176** files, **48** external links not probed; `git ls-files '*.md'` → **254** (196 outside `/archive/`, 58 inside). The deficit is **78**, not 54 — and on the comparable non-archive basis it is **20**. Mechanism, so the next re-measurement is not surprised: `check_cairn` excludes archived sources (`dev/**/archive/`) from its scan by default — `--include-archives` re-includes them and reports 254 files, 68 external links, 95 issues — and 58 Markdown files moved into archives across the 100 commits, so the scanned count fell while the tracked count rose. **A24's ruling that Chunk B's `≥180` criterion "still holds" is withdrawn: 176 < 180.** The criterion is re-derived at the implementing commit, not carried, and the deficit figure is a dated snapshot with its scan basis named — never a "stable" invariant. | [S3] |
| **A36** | *"…its `doctrine/runtime-contract.md` surface is `:46`/`:185`/`:189` only (`dev/plans/gate-claims-vs-enforcement.md:850`–`:852`) … `scan-coverage` claims `SECURITY.md:66` (`dev/plans/scan-coverage.md:611`), not `:51`."* (Amendment A23) | **Paths re-pinned; the finding is unchanged.** Both plans archived: `dev/plans/archive/gate-claims-vs-enforcement.md:850`–`:852` and `dev/plans/archive/scan-coverage.md:611`. **Line numbers hold at the new paths** — verified by opening them. Recorded because this file's `claim-check-allow` directive (line 3) exempts both stems, so `claim_check.py` prints **OK** while passing silently over two stale paths: a correct exemption behaving correctly, and therefore a place where a green checker must not be read as *these citations resolve*. | [S4] |

---

### Returned text for a serialization point — the E2 backlog row

`dev/PLANNING.md` is a serialized shared communication file. The text below is
**returned**, not written, and it lands at a serialization point. **Until it
lands, both Chunk F bar-contributed rows are NOT MET and the register is not
complete** (A27).

For `dev/PLANNING.md` > *Deferred follow-ups (durable home)* > **Security
apparatus** (the group heading is at `dev/PLANNING.md:535` / `:625`), as a new
row **beside** the existing *Install-integrity trust anchor* row rather than
inside it — the two are different failures with different revival conditions:

```
* **Two falsified integrity claims in shipped prose, unowned** — the
  coordinated-lockfile-tamper finding falsifies two sentences that no
  lineage claims: `doctrine/runtime-contract.md:132` ("Detects tampered
  apparatus before it can self-audit") and `SECURITY.md:51` ("flagging any
  post-install modification"). Measured 2026-08-05 at `4385813`: a sweep
  over every live and archived plan and proposal returns only the
  `release-security-bar` plan and its own proposal; the previously named
  owners (`gate-claims-vs-enforcement`, `agent-context-scrub`,
  `scan-coverage`) each claim other lines in those files and never these.
  The neighbouring sentence at `SECURITY.md:47` is careful and true; the
  overstatement is four lines later, so the remedy is two sentences, not a
  document. Owner: unassigned — this row IS the owner of record until a
  lineage takes it. Revival condition: whichever comes first of (a) the
  `verify_integrity` lockfile-anchor successor above, which would make both
  sentences true rather than needing them softened, or (b) the next change
  to either file by any lineage, which must take these two lines with it.
  Expiry trigger: the v0.4.0 tag — the release security bar reports both
  rows NOT MET while this row is open, so the tag is blocked on it.
```

Its arrival is what clears A27's block, and it must be verified **by reading
`dev/PLANNING.md`**, not by reading this plan.

---

### Gate audit — what this plan gates on, and what is satisfied today

Read the gates rather than assumed them. Each row names where the gate is
written.

| Gate | Where | Satisfied at `4385813`? |
| --- | --- | --- |
| **Declared tier `required(External)`** | plan header; re-stated by the Decision (*"The plan carries `required(External)` in its own right; this Decision does not discharge it"*) | **Presence: yes** — an External review landed (`a5b0f34`, Codex, 2026-08-05). **Clearance: no** — the verdict is **REVISE**, and the same reviewer's standing position that same day is that an authored Response is *"evidence of intended changes, not … a replacement for the plan's executable contract"* and that the tier *"remains undischarged"* (`dev/plans/review-gate-enforcement.md:371`–`:373`). **A second External read is owed.** |
| *"**No burndown chunk lands before the `## Plan review` section is in the tree.**"* | plan header | **Literally satisfied** (two review sections are in the tree). Amended by **A2** to *"before an External plan review is in the tree"* — also literally satisfied. **Neither is mechanical**; both are conventions a reader enforces. |
| *"No burndown chunk lands until an External review has landed under this heading, and an Internal round landing first does not change that."* | *Plan review — the brief* | **Literally satisfied.** It does not say *until the External review is cleared*, and a REVISE verdict means it is not. Read together with the row above, the honest statement is: the sentence is now spent, and what blocks implementation is the verdict, not the sentence. |
| **The lifecycle plan-review gate** | `tools/lifecycle_planner.py:790`–`:791`, via `_has_kind` (`:697`) | **Green — and was green before the External review landed.** Re-measured both directions today. It reads only the section *kind*; `_HEADER_RE` (`:509`) captures `role` and nothing consults it. **This gate cannot tell that an External review arrived, and could not have told that one had not.** ([I1], A1–A3.) |
| **Archive preconditions** — `## Code review`, `Follow-ups migrated to:`, loop-fidelity sign-off | `tools/lifecycle_planner.py:797`, `:802`–`:805`, `:808`–`:810` | **Not satisfied, and they do fire.** No `## Code review` section exists. **These are the only mechanically-enforced gates this plan has**, which is why the end-of-line audit is homed there. |
| **Chunk M (Maintainer-only), items 1–7** — the `dev/PLANNING.md` row and precondition clause, the `CHANGELOG.md` line, commissioning the end-of-line audit, reopening D4, F3's escape, the launch sequence, every signing key | Chunk M | **None satisfied.** In particular the returned `## Active` plan-open row has **never landed**: the only `release-security-bar` mention in `dev/PLANNING.md` is at `:640`, and it belongs to the **proposal's** External review finding E1 (the install-integrity trust anchor) — a *different* E1 from this review's, worth flagging so a successor does not read that row as this finding's home. |
| **Chunk M item 8 (new, A29)** — create `refs/cairn/release-bar-audit` at the audit commit | Amendment A29 | Not satisfied; not yet due. |
| **D3 — what the audit blocks (Form A tag-only vs Form B tag + repo-public flip)** | *What the Decision settled*; *The `dev/PLANNING.md` … text this plan returns* | **Unresolved.** Form A remains the plan's assumption absent instruction. |
| **D4 — reopening the `verify_integrity` verbatim-subset anchor** | Chunk M item 4 | **Not reopened** — correct. The Decision's routing to the deferred ledger stands and is visible at `dev/PLANNING.md:626`–`:640`. |
| **F3's escape** | Chunk F, row F3 | **Superseded by A27.** Its trigger (an owning lineage stalls) can never fire, because there is no owning lineage. |
| **[I1]'s remedy choice (a / b / c)** | Amendment A1, `openQuestions` | **Unresolved.** `review-gate-enforcement` is `**Status**: open`, its Chunk C.1 (`dev/plans/review-gate-enforcement.md:103`) has not landed, and it now carries its own REVISE External review (`04b0fa6`). |
| **Chunk B's commit-approval gate** | `AGENTS.md > Git and commit workflow`; *Commit-approval note* | **Stands, unchanged, and is now the live Maintainer checkpoint for E1** (A25). Chunk B edits `templates/onboarding/high-rigor-legacy.md`, loses the deliberation carve-in, and re-triggers per-commit approval. Pushing needs approval in every case. |

**Two gates were satisfiable-in-appearance and are called out so nobody reads
them as clearance:** the lifecycle gate (green since the *Internal* review) and
the *"no burndown chunk before an External review is in the tree"* sentence
(satisfied by a REVISE). Neither says the plan may implement.

---

### Does this Response clear the plan to implement?

**No.** Four reasons, in descending weight:

1. **The External verdict is REVISE and an author's Response does not convert
   it.** The tier's *presence* half is now met; its *clearance* half is not. The
   reviewer's own standard, written the same day on a sibling plan, is that a
   Response is evidence of intent and not a replacement for the executable
   contract, and that the tier remains undischarged. **A second External read is
   owed**, and it should be pointed at the amendment table, not at the original
   text.
2. **E3's full form is a schema this plan still does not contain and cannot
   contain by an author's hand.** A standing automated coverage fixture crosses
   two of this plan's Scope fences, both inherited from the accepted proposal.
   NC-H2 (A31) is a real negative control and it is what I can ship; it is not
   the standing check the review asked for, and calling it one would be the
   overclaim this bar exists to prevent.
3. **Three Maintainer decisions gate work that is otherwise ready.** E2's branch
   (backlog owner — taken — versus a scope widening to correct `SECURITY.md`
   and `doctrine/runtime-contract.md`), E3's fixture form, and D3's Form A/B.
   [I1]'s remedy remains open behind a sibling plan that is itself in REVISE.
   And E2's own acceptance is **not self-discharging**: it clears only when a
   row lands in `dev/PLANNING.md`, which is not this plan's file to write.
4. **The register's baseline must be re-taken for the third time.** 10 of 28
   body citations no longer resolve, two of them the gate citations the
   amendment table itself asserts; and the B6 / Set 2 **producing commands**
   are void against the current engine API ([S1]) — a class no checker in this
   repository reports. Per A7, A8 and A33 the implementing agent re-pins to its
   own opening commit and re-derives both commands before running anything.

**What this Response does discharge:** the mechanical revision the External
round asked for. All three findings are dispositioned with numbered residue;
every figure the review states and every figure my own prior Response asserts
has been re-measured and reported in both directions, including four
non-reproductions in my own amendment table (A7, A22, A23, A24); and five
findings the tree produced since `6618e54` are recorded with amendments.

**What an External reviewer still owes, unchanged:** whether the six properties
are the **right six**, and whether the fence is drawn where an outsider would
draw it. The landed External round engaged ownership and scope-completeness —
which is the more useful half of what it could reach without an implementation
to exercise, and it said so — but neither of those two questions is answered
yet.

---

### Verification of this Response

Run at `4385813` under `/Users/kendal30/conda_envs/lhm/bin/python3.13`
(CPython 3.13.13), `PYTHONDONTWRITEBYTECODE=1`. **No repository file outside
this plan was modified; no `add`, `mv`, `stash`, `reset` or `push` was
performed.** All scratch work — the two lifecycle-planner probes, the B6
re-measurement, the citation ledger, the ownership sweeps — ran outside the
tree, and the two probes were taken on copies, never on the tracked file.

```
$ python scripts/claim_check.py dev/plans/release-security-bar.md
claim_check: dev/plans/release-security-bar.md -- OK, no claim-check flags.   [exit 0]

$ python scripts/check_cairn.py dev/plans/release-security-bar.md
check_cairn: OK -- 1 Markdown file(s) scanned; no issues.                     [exit 0]
```

`git diff --numstat` on this file shows **0 deletions** — this Response is
appended, and no prior section is edited. Note what the first line above does
**not** establish: the file's `claim-check-allow` directive exempts two paths
that have since moved into `dev/plans/archive/` ([S4], A36), so `OK` means *no
unexempted flag*, not *every citation resolves*. The ledger above is the
statement about resolution, and it was produced by opening each file.

## Plan review -- Codex (External) -- 2026-08-05

**Tier**: External
**Findings**: none

**Verdict: SHIP.** A25--A26 own the onboarding corrections, recheck them with a
positive control, and stop on failure, closing [E1]. A27--A28 choose the durable
backlog-owner branch and make the register explicitly NOT MET until the external
`dev/PLANNING.md` row lands. That row has not landed; this is now an honest
execution gate rather than an unresolved remedy choice.

A29--A31 define the ref outside the artifact, derive the scope independently,
take the set union, and run an executable scratch negative control. For this
dated one-time release bar, that is a machine-executed control. A permanent
pytest regression would widen the accepted build-nothing-new scope and is a
reasonable later tightening, not a blocker to this plan.

The Response overstates the remaining Maintainer rulings. The author selected
the local part of [I1]'s remedy by striking the false claim while assigning the
durable row to its serialized owner; A27 selects the [E2] branch; A31 selects
the in-scope fixture form for [E3]; and D3 has an executable Form A default with
Form B only as an optional Maintainer override. SHIP closes this review round.
It does not satisfy the missing PLANNING row, supply the Maintainer's ref, or
make the final release decision.
