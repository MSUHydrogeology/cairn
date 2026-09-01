# Plan: a scanner names the set it audited

**Source proposal**: `dev/proposals/archive/2026-08-20-claude-scanner-claim-scope.md`
(accepted 2026-08-20, *"ACCEPTED as revised (Revision 4)"*). **This plan's own
opening commit archives it** — [`_template.md:18-19`](_template.md),
[`doctrine/plans.md:40-41`](../../doctrine/plans.md) — so the path above is where
it lives from the moment this plan exists, not somewhere it goes later.
**Status**: revising-code
**Plan review**: required(**Internal**) — carried verbatim from the proposal
header and re-stated by the Decision (*"Plan review is `required(Internal)` (no
Security Review trigger)"*). The **Security Review: REQUIRED** declaration in
Revisions 2–4 governs the *proposal* review, which the two Codex External rounds
discharged; it is not a plan-review tier. **No implementation commit lands
before the `## Plan review` section is in the tree.** (Code review is separate
and heavier — see *Verification* > *Code-review tier*.)
**Last update**: 2026-08-31
**Opened**: 2026-08-31

## Source proposal

Two adopter reports are one defect: a control claims — or instructs — over a set
wider or narrower than the one it audited. **D1/D1b** scope the content
scanner's exit-3 imperative to the roots it audited and reframe exit 3 as a
disagreement signal. **D2/D2b** add an `in-closure` / `out-of-closure` /
`unknown` reachability annotation to the pip-audit leg's per-distribution rows,
over a fully specified stdlib-only closure, and disclose the coverage ceiling.
This plan executes Revision 4 plus the Amendment's issue-closure contract as
restated in Revision 2; it re-argues nothing.

## Proposed paths

*Forward references this plan creates. Drop a line once its path resolves.*

None outstanding. `dev/measurement/pip-audit-closure-ratio.md` — the
closure-ratio measurement and the tripwire threshold — materialized with Chunk
G, so its declaration is dropped rather than left exempting a path that now
resolves.

## Scope

Executes D1, D1b, D2, D2b, the Revision 4 marker tokenizer and triple-multiset
oracle, the S2 mutation ledger, the closure-size tripwire threshold the proposal
leaves to the plan, the durable home for the adopter's conda measurement, and
the MAINTAINER-GATED issue closures for
[#5](https://github.com/MSUHydrogeology/cairn-scientist-ai-teams/issues/5) (gap
3) and [#6](https://github.com/MSUHydrogeology/cairn-scientist-ai-teams/issues/6).

**Surfaces touched.**

| Surface | Files |
|---|---|
| Content-scan runner (**byte-twinned**) | [`scripts/content_scan_runner.py`](../../scripts/content_scan_runner.py) **[frozen]** + [`templates/modules/team-gated/content_scan_runner.py`](../../templates/modules/team-gated/content_scan_runner.py) **[frozen]** |
| Content-security module doc (**three copies**) | [`templates/modules/team-gated/content-security.md`](../../templates/modules/team-gated/content-security.md), [`dev/modules/content-security.md`](../../dev/modules/content-security.md), `dev/.cairn/base/dev/modules/content-security.md` |
| Dependency-audit orchestrator (**no twin**) | [`templates/modules/team-gated/run_security_audit.py`](../../templates/modules/team-gated/run_security_audit.py) **[frozen]** |
| Python-security module doc (**not installed here**) | [`templates/modules/team-gated/python-security.md`](../../templates/modules/team-gated/python-security.md) |
| Tests | [`bootstrap/tests/test_security_stack.py`](../../bootstrap/tests/test_security_stack.py) **[frozen]** |
| Install records | [`dev/.cairn/cairn-lock.yml`](../../dev/.cairn/cairn-lock.yml) records `"dst": "scripts/content_scan_runner.py"` and `"dst": "dev/modules/content-security.md"` — **cited by `dst` key, never by line**, per the proposal's 2026-08-27 Correction |

**[frozen]** marks a key of the `frozen_files` object in
[`bootstrap/tests/fixtures/gate_manifest.json`](../../bootstrap/tests/fixtures/gate_manifest.json),
read directly from the manifest 2026-08-31. **Four** files this plan changes are
frozen — the two module docs are not. The test file is one of the four because
Chunks A, C, D and E all add nodes to it. Chunk H reports the set and repairs
nothing.

**Deliberately not done.** No exit code, audited set, reported row, baseline
entry, or ambient claim width changes. No `AGENTS.md` doctrine rule (the
proposal declined it). No `dev/PLANNING.md` edit — it serializes at goodnight.

**No `bootstrap/requirements-dev.txt` declaration is owed — decided, not
overlooked.** `packaging` is unshipped *and unused by the suite*: it was the
External round's independent PEP 508 oracle, never an import in
`run_security_audit.py` nor in any node this plan adds (every Chunk C node is a
literal positive/negative over hand-written fixtures). That file documents each
dev-only dependency with a rationale, so listing a library the suite never
imports would make it assert a dependency Cairn does not have. It is therefore
absent from the surfaces table and does not change.

### AUTHORIZED ADDITION — Chunk B's second scoping site

D1b names `content-security.md:122-123`; the same file's exit-contract bullet at
[`:89-91`](../../templates/modules/team-gated/content-security.md) carries a
second, softer copy of the same unscoped imperative (*"prune the baseline"*).
That second site is **an expansion beyond the accepted contract, not a
reduction**, so it could not be disposed of by a reviewer declaring it in scope.
It was routed to the Maintainer on 2026-08-31 and **allowed**:

> **Asked:** *"The scanner plan wants to scope a second sentence in
> content-security.md. The accepted proposal named one sentence (line 122-123)
> that tells an operator to prune the security baseline without saying which
> files were actually audited. There is a second, separate sentence in the
> exit-code contract list at line 89-91 that gives the same unscoped
> instruction. Fixing only the named one leaves the file saying both the new
> careful version and the old blunt one. May the plan fix both?"*
>
> **Answered:** *"Yes, fix both"*

Chunk B therefore scopes both sites. The addition is carried separately in
*Scope delta* so a reader sees scope grew **by allowance, not by drift**.

### Documentation / doctrine surface

**Descriptive layer only** — two shipped module docs (`content-security.md`,
`python-security.md`) describe their own tools, plus the changed docstrings in
the two runners. **No governing-layer change**, and
`dev/measurement/pip-audit-closure-ratio.md` is a measurement record, not
doctrine.

## Sequence

Chunks A–B (D1) and C–G (D2) are independent of each other and may land in
either order. Within D2, C precedes D precedes E, and C precedes G precedes F.
**Chunk M does not execute without the Maintainer's authorization.**

| # | Chunk | Gate | Ships |
|---|---|---|---|
| A | **The scoped imperative** — rewrite `_print_summary`'s exit-3 branch; both twins | plan review cleared | 1 commit |
| B | **The module doc's copies** — same scoping at **both** sites, in all three copies of `content-security.md` | plan review cleared (the second site's allowance is recorded in *Scope*) | 1 commit |
| C | **The declared closure** — the stdlib walk, the marker tokenizer, the caps | plan review cleared | 1–2 commits |
| D | **Retention, annotation, partition** — and the emitted-report oracle | C landed | 1–2 commits |
| E | **The mutation ledger** — five recorded mutations plus the raise-pair | D landed | 1 commit (ledger in the body) |
| F | **The coverage ceiling** — `python-security.md` second paragraph | **G landed** — F quotes G's measured ratio | 1 commit |
| G | **The measurement and the tripwire** — ratio measured, threshold set | C landed | 1 commit |
| H | **Serialization** — lockfile records reconciled, gate-manifest staleness reported | A–G landed | 1 commit |
| M | **Issue closure** — #6 closed, #5 closed-or-progressed | **MAINTAINER-GATED** | 2 comments, no code |

---

### Chunk A — the scoped imperative

Rewrite the STALE branch at
[`scripts/content_scan_runner.py:593-597`](../../scripts/content_scan_runner.py).
Per Revision 2's D1, the message (i) names the **resolved** audited roots, (ii)
says an entry with no occurrence *in that set* may still be live in another
consumer, (iii) instructs the operator to confirm across consumers **and
reconcile the lockfile record** before pruning, and (iv) states that exit 3 means
the baseline and this scan **disagree**, not that the baseline is wrong. Exit 3
still fires over the same condition.

`_print_summary` derives the roots itself by calling `load_audit_roots()`
([`:136-201`](../../scripts/content_scan_runner.py)) from `_ROOTS_MANIFEST`
([`:83`](../../scripts/content_scan_runner.py)). **Its signature does not
change** — `run_security_audit.py:627` calls it positionally across a module
boundary, and a signature change breaks exactly the mixed-tree condition that
produced the report. The docstring states that the message names the set it
audited.

> **AUTHOR-DISCLOSED IMPLEMENTATION DETAIL — in no revision, and named so the
> code reviewer checks it.** A `load_audit_roots()` failure *inside*
> `_print_summary` degrades to the manifest name and says the roots could not be
> resolved. This is **not a new deliverable**: it is what keeps invariant (v) and
> *"exit 3 must not be masked"* true when the message's own input fails, and
> without it the new message could raise on the one path D1 exists to fix.
> **It must not become a new exit path** — the degraded branch returns the same
> code 3, and the node below is what the reviewer falsifies.

**Byte-twin discipline.** The `templates/modules/team-gated/` copy is
byte-identical to the `scripts/` copy (sha256 `4c9af385…`, measured 2026-08-31).
Both change in the **same commit**, which re-verifies `cmp` / `shasum -a 256`
equality before it lands.

**Acceptance.**
* `test_stale_message_names_the_audited_roots` — the exit-3 stderr contains every root `load_audit_roots()` resolves, not just the manifest filename.
* `test_stale_message_defers_to_other_consumers_before_pruning` — the message asks for cross-consumer confirmation and does not issue a bare prune imperative.
* `test_stale_message_requires_lockfile_reconciliation` — the message names the lockfile record.
* `test_print_summary_signature_is_positionally_stable` — five positional parameters, in order, asserted via `inspect.signature`; pins invariant (v).
* `test_unresolvable_roots_degrade_the_message_without_changing_exit_three` — with `load_audit_roots()` forced to raise, the summary still prints and the code is still 3; no new exit path.
* `TestRunnerExitContract::test_stale_baseline_is_three` ([`:487-496`](../../bootstrap/tests/test_security_stack.py)) passes **unmodified** — exit-code invariance.
* The two twins are byte-identical after the commit.

**Falsifier**: restore the old unscoped sentence and the first three nodes go
red; add a sixth positional parameter and the signature node goes red; drop the
degrade and the forced-raise node goes red on an exception, not on a wrong exit
code; edit one twin only and the identity check goes red.

---

### Chunk B — the module doc's copies

Apply the same scoping to
[`templates/modules/team-gated/content-security.md:122-123`](../../templates/modules/team-gated/content-security.md)
— *"it must be deleted before the baseline is current"* becomes the scoped,
confirm-then-reconcile form — and to the softer exit-contract copy at
[`:89-91`](../../templates/modules/team-gated/content-security.md) (*"prune the
baseline"*), **which the Maintainer authorized on 2026-08-31; the quoted
authorization is in *Scope***. The self-hosted copies at `dev/modules/content-security.md` and
`dev/.cairn/base/dev/modules/content-security.md` are **byte-identical**
(sha256 `be93184e…`, measured 2026-08-31) and move in the **same commit**.

**Acceptance.**
* All three copies byte-identical after the commit (`shasum -a 256`).
* Neither surviving bullet issues an unconditional prune; both name the audited-roots set and the lockfile record.
* `python scripts/check_cairn.py` clean; `python scripts/link_check.py` **adds no finding beyond the recorded pre-existing baseline** (*Acceptance criteria* > *Standing gates*).
* `pytest bootstrap/tests/test_content_scan.py` green (it asserts the doc's install destination).

**Falsifier**: leave `:89-91` unscoped and the file states both the scoped and
the unscoped imperative — a reviewer reading only the exit-contract table gets
the old instruction.

---

### Chunk C — the declared closure

New stdlib-only closure walk in
[`templates/modules/team-gated/run_security_audit.py`](../../templates/modules/team-gated/run_security_audit.py),
per Revision 3's corrected policy as amended by Revision 4. No twin. Nothing in
this chunk reaches the report; the walk is a pure function with a docstring
stating its authority and its failure direction.

**The walk's shape, decided here so Chunk D can thread it.**
`resolve_declared_closure(python_package: Path) -> tuple[frozenset[str], frozenset[str]] | None`
— `(in_closure, unknown)` as PEP 503-normalized names, or **`None` when the
whole closure is `unknown`** (a cap exceeded, an unrecognized `extra`
expression, an unresolvable root). One return type carries both the partial and
the total failure, so Chunk D needs no second code path for either.

* **Authority** — `importlib.metadata.packages_distributions()`, rooted at the top-level package named by the final path component of the `python_package` token that [`validate_python_package`](../../templates/modules/team-gated/run_security_audit.py) (`:209-242`) already resolves. No `pyproject.toml`. `importlib.metadata` is already imported at `:67`; no new import.
* **The discoverable set — a second, separate enumeration, named here because the `unknown` remainder cannot be materialized without it.** A *rooted* walk never visits a distribution nothing requires, so the un-reached remainder has to be enumerated independently: the walk calls the existing [`installed_distribution_names()`](../../templates/modules/team-gated/run_security_audit.py) (`:1033-1040`), which already wraps `importlib.metadata.distributions()` and PEP 503-normalizes via `_canonical_name` (`:1027-1031`). No new helper and no new import. **This same set is the "discoverable set" Chunk G's tripwire is a bounded fraction *of*** — one enumeration, two consumers, so the ratio and the annotation can never be computed against different denominators.
* **Normalization** — PEP 503, both sides, before comparison.
* **Requirement names** — the **anchored** match of `[A-Za-z0-9][A-Za-z0-9._-]*` at the start of the stripped requirement, and nothing else. `~` terminates, which is what `cffi~` / `mdurl~` came from. A non-matching leading token takes the **unreadable-metadata disposition, not the absent-requirement one** — the two are separated in *Absent vs unreadable* below, and this is the plan's call on which applies. The edge contributes `unknown` and so does everything reachable only through it; because an unnamed edge resolves to no distribution, its unknowable reach is the **whole un-reached remainder**, so those distributions annotate `unknown` rather than `out-of-closure`, while the reached set still annotates `in-closure`. Decided this way because the absent-model would silently under-include exactly the dependency D2 exists to surface.
* **Extras** — a quote- and whitespace-aware **marker tokenizer**, not a substring test. Unquoted `extra` equality in either operand order → extras-gated → **excluded**. `extra` inside a quoted string is a value → **ignored**. Any **other** unquoted `extra` expression (`!=`, `in`, …) → **the whole closure is `unknown`**.
* **Non-extras markers** — **included** without evaluation.
* **Traversal** — breadth-first over normalized names, memoized on the visited set (which terminates cycles). Exceeding either cap makes the **whole closure `unknown`**, never a truncated one. **The two numbers are decided here, not left to the implementer: node cap 2000, depth cap 32.** 2000 is roughly six times the 301 distributions the External round enumerated in this environment, and 32 is far above any real dependency chain (the measured `scikit-learn` / `rich` / `requests` closures run 5–60 nodes) — so a legitimate closure never trips a cap, while package-controlled metadata cannot drive an unbounded walk. Both are module constants and the cap node reads them rather than re-stating them, so the values can move without the test lying.
* **Absent vs unreadable** — a required name with no installed distribution terminates that branch contributing nothing; an *installed* distribution whose metadata cannot be read contributes `unknown`, and so does everything reachable only through it. No distribution — or more than one — for the root's top-level name → closure empty and **every** distribution `unknown`.

Fixtures are **messy by construction**: an extras-gated requirement, a
non-extras marker-gated requirement, a `Pillow`/`pillow` pair, a cycle, an
ungrammatical requirement token, an unreadable-metadata distribution, and a
distribution in nobody's closure.

**Acceptance** — new nodes in
[`bootstrap/tests/test_security_stack.py`](../../bootstrap/tests/test_security_stack.py):
`test_closure_is_rooted_in_the_installed_distribution_metadata`,
`test_requirement_names_are_normalized_before_comparison`,
`test_requirement_identifier_stops_at_the_version_specifier`,
`test_extras_gated_requirements_are_excluded`,
`test_quoted_extra_text_is_a_value_not_the_marker_variable`,
`test_unrecognized_extra_expression_makes_the_closure_unknown`,
`test_non_extras_markers_are_included_without_evaluation`,
`test_uninstalled_requirement_terminates_the_branch_without_unknown`,
`test_unreadable_metadata_makes_its_subtree_unknown`,
`test_an_ungrammatical_requirement_edge_is_unknown_not_out_of_closure`,
`test_cycles_terminate_via_the_visited_set`,
`test_exceeding_a_traversal_cap_makes_the_whole_closure_unknown`,
`test_unresolvable_root_makes_every_distribution_unknown`, and
`test_closure_walk_imports_only_the_standard_library`. Each carries its reason
in its docstring and no chunk or finding coordinate in its name. The marker
nodes are **independent positives and negatives** over `extra == "x"`,
`extra=="x"`, `extra  ==  "x"`, `"x" == extra`,
`foo; platform_release == "extra == dev"` (kept), `extra != "x"` and
`extra in "x"` (closure `unknown`); the environment marker corpus is a
**positive control only**, since it agrees with the withdrawn predicate and so
cannot validate the replacement. **That corpus is re-measured, not carried
forward**: `as_of 2026-08-31`, under the canonical interpreter,
**2,373** requirement strings carrying a marker clause across 301 installed
distributions, counted as `";" in requirement` over
`importlib.metadata.distributions()`. (The earlier figure of 2,314 was undated
and no node asserts against either number; it is the counting rule and the date
that make this a control rather than a claim.)

**Falsifier**: reinstate the `extra ==` substring test and
`test_quoted_extra_text_is_a_value_not_the_marker_variable` goes red; treat
`extra != "x"` as extras-gated and its node goes red; use an unanchored search
for the identifier and the `~` node goes red; give an ungrammatical edge the
absent-requirement disposition and the un-reached remainder reads
`out-of-closure`, reddening its node; drop the depth cap and the cap node goes
red.

---

### Chunk D — retention, annotation, partition

**How Chunk C's closure reaches the annotation site — two defaulted keyword
parameters, and the defaults are what keep the existing suite green.** `main`
already resolves `pkg = validate_python_package(_REPO_ROOT, lock)`
([`:1285`](../../templates/modules/team-gated/run_security_audit.py)), which is
the root Chunk C's walk needs; today the leg's lambda
([`:1299`](../../templates/modules/team-gated/run_security_audit.py)) does not
pass it on.

* `run_pip_audit_pass(repo_root, *, allow_egress, passthrough_env=(), python_package: Path | None = None)` ([`:1094-1095`](../../templates/modules/team-gated/run_security_audit.py)) — the lambda passes `python_package=pkg`; the leg calls `resolve_declared_closure(python_package)` only when it is not `None`, and **wraps that call in `try/except Exception`, treating a raised exception exactly as a `None` return** — the same fail-closed path, never a second one. Chunk C specifies the walk to return `None` for every *known* failure, so this catch exists for the unforeseen; it is what the forced-raise acceptance nodes below and Chunk E's raise-pair mutation actually exercise.
* `classify_pip_audit_output(text, *, schema_established=None, closure=None)` ([`:879-881`](../../templates/modules/team-gated/run_security_audit.py)) — `closure` takes the walk's return value verbatim.
* **Omitted ⇒ `None` ⇒ every reported distribution annotates `unknown`** — deliberately the same disposition as a failed walk, so there is one fail-closed path and not two. This is what lets the **eleven** existing `run_pip_audit_pass(tmp_path, allow_egress=…)` call sites and the **six** existing `classify_pip_audit_output(…)` call sites in `bootstrap/tests/test_security_stack.py` pass **unmodified**, the three named below among them.
* **The annotation is a reporting axis and nothing else.** It never feeds `coverage.unknown`, the `unknown_total` sum, or the tier. That separation is what makes invariant (iii) true: a distribution annotated `unknown` for reachability does not gate CLEAN, because reachability was never part of the CLEAN question.
* **Retain** `(normalized_name, count)` in `classify_pip_audit_output` where `vulnerabilities += len(vulns)` ([`:942`](../../templates/modules/team-gated/run_security_audit.py)) currently discards the association. **No per-vulnerability identity** — no ids, aliases, or fix versions — so the parse surface bound to `_PIP_AUDIT_SCHEMA_ESTABLISHED` widens by nothing.
* **`Coverage`** ([`:767-787`](../../templates/modules/team-gated/run_security_audit.py)) **gains exactly one field** — `vulnerable: tuple[tuple[str, int], ...]`, appended **last with a default**, so the seven existing fields keep their names, order, tuple indices and meanings and no existing construction or unpacking moves. The per-distribution *rows* are a **report** artifact, not a `Coverage` field; the annotation is joined to `vulnerable` at render time. (This settles the model: the object grows by one additive field, and every acceptance assertion below is written against that, not against whole-object identity.)
* **Annotate** each reported distribution against Chunk C's closure, by a rule stated here so it is not rediscovered: PEP 503-normalize the reported name, then — in `in_closure` → **`in-closure`**; else in `unknown` → **`unknown`**; else → **`out-of-closure`**; and if the walk returned `None`, **every** distribution is `unknown` without consulting either set. `in_closure` is tested first, so a name in both sets reads `in-closure`; Chunk C's traversal cannot produce that overlap, and the order is fixed here rather than left to depend on that.
* **Report the partition** at the coverage-summary print ([`:1198-1203`](../../templates/modules/team-gated/run_security_audit.py)): N vulnerabilities across M distributions, of which X across Y are in the declared closure — **plus the per-distribution rows the annotation lives on, which the report does not carry at all today.** Every distribution still appears.

**Where the new nodes go, and what they must not be called.**
`bootstrap/tests/test_security_stack.py:1240` already carries a banner
`# --- Chunk D: the denominator, the dispositions, and the CLEAN gate ---` from
earlier, unrelated work, and this plan's Chunk D nodes land in the same region.
**Do not extend, reuse, or echo that banner**, and put no chunk letter, finding
id or plan coordinate in a new node name, banner or docstring: two different
"Chunk D"s in one file is exactly the decayed pointer `AGENTS.md` >
*Durable artifacts stand without the deliberation that produced them* forbids.
Node names carry the **property**; the docstring carries the **reason**.

**Acceptance.**
* `test_reported_rows_match_the_literal_expected_triples` — the expected multiset of `(normalized_distribution, count, annotation)` triples is **written literally and pre-normalized in the fixture**, beside a raw child-JSON fixture; the **emitted report** is parsed back into an observed triple multiset; exact equality. The raw fixture carries at least one vulnerable distribution in **each** of `in-closure`, `out-of-closure`, `unknown` — that class coverage is part of the invariant, not of the test plan.
* `test_the_established_coverage_fields_are_unchanged_by_the_annotation` — asserted on the **returned object**, with `closure` supplied and omitted: all seven pre-existing fields (`established`, `scanned`, `no_match`, `unknown`, `note`, `names` — the full tuple, not its length — and `vulnerabilities`) and the returned `(status, tier)` are equal; the appended `vulnerable` field is the only difference, and it is the same either way. `coverage.names` reaches the report only as `len(...)`, so the emitted-report oracle cannot see it.
* `test_report_states_the_in_closure_partition` — the printed line carries both the total and the in-closure subtotal.
* `test_a_failed_closure_annotates_every_distribution_unknown` and `test_a_failed_closure_drops_no_distribution` — the paired assertions for the forced-raise path; the leg still succeeds.
* `test_no_per_vulnerability_identity_is_retained` — no vulnerability id, alias, or fix version reaches `Coverage` or the report.
* Existing exit-contract nodes (`test_d_t2d_report_findings_and_exit_code_cannot_contradict` at [`:1405-1432`](../../bootstrap/tests/test_security_stack.py), `test_d_t2_one_unknown_gates_clean`, `test_d_t1_a_skipped_distribution_is_never_scanned`) pass **unmodified**.

**Falsifier**: compute the expected multiset from the function under test and
the oracle can no longer fail; project the annotation away and mutation 5 in
Chunk E survives.

---

### Chunk E — the mutation ledger

Run each mutation, observe the named node red, restore byte-identically
(`git diff <path>` empty), and record the mutation, the node, and the observed
failure message in the commit body. **S2's answer moves here**; S1, S3 and S4
are unchanged by the chunking.

1. drop a row in the renderer → `test_reported_rows_match_the_literal_expected_triples`;
2. alter a count → same node;
3. omit rows by annotation class (`if row.annotation == "out-of-closure": continue`) — the option-2 collapse → same node;
4. substitute a parent-side enumeration for `coverage.names` → `test_the_established_coverage_fields_are_unchanged_by_the_annotation`;
5. relabel or swap annotation classes while preserving names and counts → `test_reported_rows_match_the_literal_expected_triples`.

Plus the raise-pair: force the closure walk to raise and confirm
`test_a_failed_closure_annotates_every_distribution_unknown` passes **while**
`test_a_failed_closure_drops_no_distribution` also passes.

**Acceptance.** Five mutations, five recorded reds, five byte-identical
restores, in the commit body. **Falsifier**: a mutation that stays green is a
finding against Chunk D's oracle, not a note — the chunk does not close.

---

### Chunk F — the coverage ceiling

A second paragraph in the existing *Declared scope* section of
[`templates/modules/team-gated/python-security.md:35-52`](../../templates/modules/team-gated/python-security.md),
beside the floor disclosure: the leg audits the environment, in a conda workflow
that substantially exceeds the project's own closure, the ratio, and that triage
starts from reachability. **The ratio is Chunk G's measured figure, quoted, not
an independent estimate** — which is why F is gated on G in the *Sequence*
table: two committed artifacts naming different numbers for the same quantity is
worse than either alone. This file is **not** in Cairn's installed roster, so it
has no `dev/modules/` copy and no lockfile record.

**Acceptance.** The paragraph names the ratio recorded in
`dev/measurement/pip-audit-closure-ratio.md` and points at the reachability
annotation; `python scripts/check_cairn.py` clean; `python scripts/link_check.py`
and `python scripts/quality_gate.py --sub neutrality` **add no finding beyond the
recorded pre-existing baseline** (*Acceptance criteria* > *Standing gates*).
**Falsifier**: a paragraph that states the gap without a figure restates the
existing conda-native sentence and adds nothing — the ratio is what makes it a
ceiling.

---

### Chunk G — the measurement and the tripwire

Create `dev/measurement/pip-audit-closure-ratio.md` — the two thresholds the
proposal leaves to the plan, plus the measurement it owes the reporter:

1. the adopter's field measurement — 299 discoverable, 93 in closure, 212 outside, 144 findings across 21 packages, 27 reachable across 2 — **recorded exactly as reported and attributed to issue #6**, so field evidence built by hand does not evaporate into a closed issue. This is gate 4 of the issue-closure contract and Chunk M's comment names this file.

   **The record states, in the file, that the partition does not close:** 93 + 212 = **305** against a stated discoverable total of **299**, a gap of **6**; the two shares (`212/299` = 71%, `93/299` = 31%) sum to 102%, so it is not rounding, and no third bucket is stated to absorb it. **This plan does not resolve which figure moves and does not adjust one to make it close** — these are the adopter's numbers, carried from proposal [`:77-83`](../proposals/archive/2026-08-20-claude-scanner-claim-scope.md) and [`:390-391`](../proposals/archive/2026-08-20-claude-scanner-claim-scope.md), and silently correcting someone else's field data is the worse failure. Chunk M's #6 comment may ask the reporter; it does not assert an answer;
2. the closure ratio measured on a **real environment** under the canonical interpreter, with the interpreter, the root, the distribution count, and an `as_of` date;
3. the **closure-size tripwire threshold** derived from (2), stated as a bounded fraction of the discoverable set, with the reason for the number;
4. the `unknown`-rate observation — the proposal's *"`unknown` becomes the common case"* signal, measured rather than asserted.

**Why `dev/measurement/`, checked against that folder's own rule.**
[`dev/measurement/README.md`](../measurement/README.md) draws membership
two-sided — **not an archive, not framework-adopter state** — and this file is
neither: live, dated, and **gate-backed**, since item 3's threshold is read by
the acceptance node below. The tension is named, not hidden: the README's
positive list says *lifecycle* metrics and this is an *apparatus* measurement,
so the fit rests on the two precedents already in the folder —
`gitleaks-version-support.md`, an apparatus measurement a test binds to, and
`suite-cost.md`, a dated snapshot kept for exactly the reason the README gives
(a figure re-measured every time it is wanted is lost again in between).

**The fixture constraint that makes the tripwire non-vacuous — stated, because
without it the node passes under both policies.** The node's threshold comes from
a *real* environment (item 2) but is asserted over a *fixture* environment, so
the fixture must be **built to cross it**: its **extras-gated subtree alone must
be large enough that including those edges pushes the closure over the recorded
threshold**. A fixture without that property is green whether extras are
included or excluded — a tripwire reporting success without testing its claimed
property, which `AGENTS.md` > *Name the trigger* calls worse than no tool because
it is silent. The denominator is Chunk C's `installed_distribution_names()` set.

**Acceptance.** `test_closure_stays_a_bounded_fraction_of_the_discoverable_set`
— over a fixture environment with a known root, the closure is under the
recorded threshold, and the test's docstring says a re-inflated closure stops
partitioning and makes the axis worthless. `python scripts/claim_check.py` clean
over the new file. **Falsifier — run and recorded, not merely stated**: restore
Revision 2's extras-inclusive policy in the walk, observe this node red, restore
byte-identically, and record the observed failure in the commit body the way
Chunk E records its five. A falsifier that stays green means the fixture
constraint above was not met and the chunk does not close.

---

### Chunk H — serialization

* Reconcile [`dev/.cairn/cairn-lock.yml`](../../dev/.cairn/cairn-lock.yml) for the records keyed `"dst": "scripts/content_scan_runner.py"` (verbatim) and `"dst": "dev/modules/content-security.md"` (non-verbatim, with its `base_cache`). **Cite records by `dst` key, never by line number** — the file is machine-generated and regenerate-only, and the source proposal's own Correction records four line citations into it going void. **The command, scoped, never a hand-edit** (the file is tool-owned):

  ```
  python bootstrap/scaffold.py upgrade --target . \
      --finalize scripts/content_scan_runner.py dev/modules/content-security.md
  ```

  The positional form binds the write-set to exactly those two records so a concurrent session's work is not swept into the integrity record; `--force` is never passed. It advances **`hash` only** — it prints that the base cache / upgrade ancestor is unchanged — so `base_hash` is not moved by it. Chunk B changes the base-cache copy in the same commit, so the two must end **equal** for both records; if the finalize leaves `hash != base_hash`, that reads as a fork against Cairn's own upstream and the commit body says so rather than the chunk closing quietly.
* **Report, do not repair, the gate manifest.** `bootstrap/tests/fixtures/gate_manifest.json` freezes **four** files this plan changes: `scripts/content_scan_runner.py`, `templates/modules/team-gated/content_scan_runner.py`, `templates/modules/team-gated/run_security_audit.py`, **and `bootstrap/tests/test_security_stack.py`** — the test file counts, because Chunks A, C, D and E all add nodes to it. (The two module docs are *not* frozen.) The suite does **not** diff the committed fixture, so nothing goes red and **a green suite is not evidence that no re-anchor is owed**. The final commit body names every `FROZEN-MODIFIED` entry this plan creates and re-pins nothing; the re-anchor is the Maintainer's ceremony. **Re-derive that list at commit time by filtering the manifest's own `frozen_files` keys against the commit's changed paths — do not transcribe this plan's four.** The prose enumeration is what already failed once here; the manifest is the instrument, and a list handed short to a trust ceremony is contradicted by no gate anywhere.
* No `bootstrap/_scaffold/` file changes, so **no AST attestation re-anchor is owed** — stated because its absence is otherwise indistinguishable from an oversight.

**Acceptance.** `python bootstrap/verify_integrity.py --target .` reports **no
violation** for either reconciled path (pre-existing violations on other paths
are named, not fixed). The stale frozen entries are enumerated in the commit
body. **Falsifier**: skip the reconciliation and `verify_integrity` reports the
two paths — which is exactly the sibling-control degradation D1's new message
warns the operator about.

---

### Chunk M — MAINTAINER-GATED: issue closure

> **No step here executes without the Maintainer's authorization, quoted
> verbatim in the commit or comment record.**

Per the Amendment as restated in Revision 2:

* **#6 closes with this work alone** — D2 and D2b are the whole of it.
* **#5 holds gap 3 only**; gaps 1–2 are in `2026-08-20-claude-adopt-into-existing-tree`. #5 closes **only when both have landed**. **Whichever lands second carries the close; the first posts a progress comment** and leaves the issue open. The comment names which proposal took which gap — the adopter offered the split, so it is owed an answer.
* Both are gated on: implementation landed and code-reviewed; **the implementation's External Security code review completed** (gate 2 of the accepted contract — *not* the proposal pass, and not the Internal plan review); a closing comment meeting the honesty bar; the measurement's named home; and Maintainer authorization.
* **The closing comment states, for #6**: that options 1 and 3 were taken and **option 2 refused on the reporter's own caution** about the closure walk, credited to them rather than presented as ours; that the distinction is **standing, not effort**; **the bright line**, published as the emitted-report oracle rather than as a claim about a "finding set"; that the leg reports **per-distribution counts, not per-finding records**; and that the **ambient audit was not narrowed**. For **#5 gap 3**: that the imperative was **wrong, not merely imprecise** — they pruned a security allowlist on our instruction and were saved by a test they happened to have. Both name `dev/measurement/pip-audit-closure-ratio.md`.

**Acceptance.** Each posted comment contains every bullet above that applies to
it; #5's disposition (close vs progress) matches which sibling landed second;
the Maintainer's authorization is quoted verbatim in the record.
**Falsifier**: a close for #5 posted while the sibling is unlanded, or a #6
close that lists what shipped without naming the refusal — either is the exact
failure the Amendment exists to prevent.

## Acceptance criteria

Per-chunk criteria are above. Plan-level:

* **Invariants that must hold at the end.** (i) the emitted-report triple multiset equals the literal fixture multiset; (ii) the seven pre-existing `Coverage` fields and `(status, tier)` are identical with the annotation present and absent, the appended `vulnerable` field being the only difference; (iii) exit codes unchanged across every D1 and D2 path; (iv) neither tool writes the residual baseline; (v) `_print_summary`'s signature is unchanged; (vi) the twins are byte-identical; (vii) the closure walk imports nothing outside the standard library.
* **Suite.** `CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0` — 0 failed, and every skip/xfail/xpass dispositioned in the Boundary B record.
* **Standing gates, against a recorded baseline — three of them are red today for unrelated reasons, and "clean" is not achievable.** `check_cairn.py`, `--sub redundancy`, and `claim_check.py` over this plan and the new measurement file are **clean** (0). `link_check.py`, `quality_gate.py --sub neutrality` and `verify_integrity.py --target .` are compared against this **pre-existing baseline, measured under the canonical interpreter at `2c21818` and re-measured unchanged at `e67959a`, `as_of 2026-08-31`**:

  | gate | exit | baseline | where |
  |---|---:|---:|---|
  | `scripts/link_check.py` | 1 | **3** findings | all three in `templates/modules/default-on/documentation-plan.md`, lines 103, 113 and 123 |
  | `scripts/quality_gate.py --sub neutrality` | 1 | **79** FAILs | the only three under `templates/modules/team-gated/` are `content_scan.py:329,547` and `intent.py:64` — **no file this plan touches** |
  | `bootstrap/verify_integrity.py --target .` | 1 | **21** violations | neither path Chunk H reconciles is among them |

  The criterion is **no new finding beyond that baseline**, not exit 0. A count that moves is investigated before the chunk closes; a count that holds is the pass. Re-measure the baseline if the tree moves under the work — the figures above are dated for exactly that reason.
* **Smoke.** `python scripts/content_scan_runner.py` exercises D1 on this tree. **D2 cannot be smoked here** — `python-security` is not in Cairn's installed roster and the orchestrator has no self-hosted twin under `scripts/` — so it is exercised only through `test_security_stack.py`'s orchestrator fixture against the template file. That is a real omission and is recorded as one.
* **Every new node shown non-vacuous** — by Chunk E's ledger for the D2 oracle, by the Chunk A and Chunk C falsifiers, **and, for Chunk G's tripwire node, by G's own falsifier run and recorded** against the fixture constraint G states. No new node is outside this list.

## Scope delta

**Scope delta**: preserved. No accepted outcome is withdrawn: D1, D1b, D2, D2b,
the Revision 4 tokenizer and triple oracle, the five mutations, the raise-pair,
the tripwire threshold, the measurement home, and both issue closures each land
in a chunk above. The plan review's own walk of every accepted outcome into a
named chunk found none missing.

**One authorized addition, carried separately so it is not read as drift.** The
second scoping site in `content-security.md` (`:89-91`, the exit-contract
*"prune the baseline"* bullet) is scope the accepted proposal named nowhere. It
is **not** absorbed into `preserved`: it grew the plan by the Maintainer's
explicit allowance of 2026-08-31, quoted verbatim in *Scope* > *AUTHORIZED
ADDITION*, obtained before Chunk B lands. The plan reviewer declined to strike it
and declined to authorize it — correctly, since a reviewer can do neither.
Nothing else was added.

Chunk A's disclosed degrade is **not** scope in either direction — it is how an
accepted outcome stays true when its own input fails — and is flagged there so
the code reviewer confirms it opens no new exit path; the plan review agreed no
allowance is owed for it.

## Verification

**Boundary A (iteration, scoped) — the reviewed mapping.**

| Changed surface / invariant | Test node or file | Standing gates |
|---|---|---|
| Exit-3 message, `_print_summary` (A) | the five Chunk A nodes + `TestRunnerExitContract` in `bootstrap/tests/test_security_stack.py` | `check_cairn.py`; twin `shasum`/`cmp` |
| `content-security.md` ×3 (B) | `bootstrap/tests/test_content_scan.py` | `check_cairn.py`, `link_check.py`, three-copy `shasum` |
| Closure walk (C) | the fourteen Chunk C nodes in `bootstrap/tests/test_security_stack.py` | stdlib-only import assertion |
| Retention / annotation / report (D) | the six Chunk D nodes + the unmodified existing pip-audit nodes at `bootstrap/tests/test_security_stack.py:1240-1533` | — |
| Mutation ledger (E) | the Chunk D nodes, perturbed | — |
| `python-security.md` (F) | — (doc) | `check_cairn.py`, `link_check.py`, `quality_gate.py --sub neutrality` |
| Measurement + tripwire (G) | `test_closure_stays_a_bounded_fraction_of_the_discoverable_set` | `claim_check.py` |
| Lockfile records (H) | `bootstrap/tests/test_lockfile_module.py`, `test_lockfile_provenance.py` | `bootstrap/verify_integrity.py --target .` |

**Boundary B (integration).** Declared in advance:

**Boundary B mode**: full — bounded mode is **refused**. **Four**
gate-manifest-frozen files change (Chunk H enumerates them) and two lockfile
records are reconciled, so
the change touches a **contract surface**; the content scanner and the
dependency-audit orchestrator are **security-stack** surfaces. Uncertainty
resolves to `full`, and here there is no uncertainty to resolve. One run, after
the final implementation commit, against a clean unchanged commit under the
canonical interpreter (**Python 3.13.x**,
`/Users/kendal30/conda_envs/lhm/bin/python3.13`):

```
CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0
python scripts/quality_gate.py --sub neutrality --sub redundancy
```

plus the standing gates and smoke listed under *Acceptance criteria*. Append the
evidence then, and not before, as
`## Implementation verification -- <agent> -- YYYY-MM-DD` with the template's
fields: tested SHA, reviewed range, interpreter, clean pre/post state, the
command table with outcomes and elapsed, non-pass disposition, plan-specific
acceptance commands, and known omissions (D2's un-smokable path above).

**Boundary C (falsification)** is the code reviewer's, and it is **not**
re-running the two commands above. Verify the record against the reviewed range,
then attack what would hurt most if wrong: that the oracle's expected multiset is
literal rather than derived; that mutation 5 genuinely reddens; that the
reachability annotation cannot reach `unknown_total` or the tier; that
`load_audit_roots()` inside `_print_summary` cannot swallow exit 3; and that the
twins and the three doc copies are identical on disk. Because Boundary B is
`full`, no `**Bounding**` line is owed.

**Code-review tier.** The accepted issue-closure contract requires *"the
implementation's External Security code review"* before either issue closes. One
External pass with a security lens serves both that gate and the ordinary
code-review floor (not the implementing agent). This is the proposal's own
requirement carried forward, not an escalation this plan invents.

## Dispositions

*Filled at archive-preparation.*

## Plan review -- Claude (Internal, fresh-context subagent) -- 2026-08-31

**Model**: claude-opus-5 (Claude Opus 5)
**Obligation**: Internal
**Tier**: Internal
**Findings**: raised
Reviewed commit: 2c218188bb0837f570526b42200addf0e08f7d4c

Fresh-context Internal pass on the whole plan against the accepted proposal
`dev/proposals/archive/2026-08-20-claude-scanner-claim-scope.md` and against the
live tree. I did not write this plan. I checked *translation fidelity and
executability*, not the design: the Decision of 2026-08-20 settled D1/D1b/D2/D2b,
the marker tokenizer, the triple oracle and the gating, and none of that is
reopened here.

**Verdict: REVISE** — two blocking findings, three notes, two nits, plus one call
routed to the Maintainer because a reviewer cannot make it.

### What I checked

Canonical interpreter `/Users/kendal30/conda_envs/lhm/bin/python3.13`, clean tree
at the reviewed commit, read-only.

* **Instrument control before trusting any absence.** `grep -rc
  test_stale_baseline_is_three bootstrap/tests/test_security_stack.py` → **1**
  (the pattern can match); the same instrument then returns **0** files across
  `bootstrap/ scripts/ templates/` for `resolve_declared_closure` and every new
  node name I spot-checked, so the new names are genuinely free.
* **Counts measured, not taken** — `grep -c "run_pip_audit_pass("` → **11**,
  `grep -c "classify_pip_audit_output("` → **6**; both match `:257` exactly.
* **`frozen_files` in `bootstrap/tests/fixtures/gate_manifest.json`** (183 keys)
  read directly and filtered for every Scope-table surface → **B1**.
* **The cross-module positional call** — `run_security_audit.py:627` is
  `runner._print_summary(code, files, all_flags, new_flags, stale)`, exactly as
  `:124` claims.
* **Both `content-security.md` passages in full** (`:80-95`, `:118-126`) before
  making the Chunk B call, plus the accepted wording at proposal `:874-883`,
  `:1284-1291` and `:2447`.
* **Standing-gate baseline, run just now** — control for **N2**: `check_cairn.py`
  0; `--sub redundancy` 0; `claim_check.py` on this plan 0 with both
  forward-reference exemptions firing; `link_check.py` **1** (3 findings, all
  lines 103, 113 and 123 of
  `templates/modules/default-on/documentation-plan.md`); `--sub
  neutrality` **1** (**79** FAILs — I checked the overlap rather than assuming
  it: the only 3 under `templates/modules/team-gated/` are
  `content_scan.py` (lines 329 and 547) and `intent.py` (line 64), untouched here);
  `verify_integrity.py --target .` **1** (21 violations, neither reconciled path
  among them).
* **The arithmetic of Chunk G's transcribed figures** against proposal `:77-83`
  and `:390-391` → **B2**.

### Steelman

The citation work here is unusually good and should not be contested without new
evidence.

* Every file:line I opened landed on exactly what the plan says: the STALE branch
  at `content_scan_runner.py:593-597`; `load_audit_roots()` at `:136-201`;
  `validate_python_package` at `run_security_audit.py:209-242`; `Coverage` at
  `:767-787` with exactly the seven fields enumerated; `vulnerabilities +=
  len(vulns)` at `:942`; the coverage print at `:1198-1203`; `pkg =
  validate_python_package(...)` at `:1285` and the leg's lambda at `:1299`, which
  today does **not** pass `python_package` on — so Chunk D's edit is real and
  needed, not a restatement. Both byte-identity hashes check out on disk
  (`4c9af385…`, `be93184e…`).
* The `Coverage`-grows-by-one-defaulted-field design is verified safe: all four
  construction sites pass five positional arguments and rely on the two existing
  trailing defaults, and nothing in the tree positionally unpacks a `Coverage`.
  Invariant (ii) is realistic, not hopeful.
* Chunk H's central claim is substantiated rather than asserted:
  `test_gate_manifest.py` never loads the committed fixture — it produces one
  fresh and self-verifies that. Report-not-repair is the correct disposition, and
  citing the lockfile by `dst` key rather than line (`:55`, `:355`) is the right
  lesson from the proposal's own 2026-08-27 Correction.
* `Scope delta: preserved` holds. I walked every accepted outcome — D1, D1b, D2,
  D2b, the Revision 4 tokenizer, the triple oracle, the five mutations, the
  raise-pair, the tripwire threshold, the measurement home, both issue closures
  — into a named chunk. Nothing accepted is quietly dropped.

### Finding B1 (blocking) -- a closed count of frozen files, asserted against an instrument the plan did not run, short by one

`:363` enumerates the gate-manifest-frozen files this plan changes as three:
`scripts/content_scan_runner.py`, `templates/modules/team-gated/content_scan_runner.py`,
`templates/modules/team-gated/run_security_audit.py`. `:432` repeats the count —
*"Three gate-manifest-frozen files change."*

Read directly from the fixture, `frozen_files` also keys
**`bootstrap/tests/test_security_stack.py`** — and Chunks A, C, D and E all add
nodes to that exact file. That is a **fourth** frozen file this plan modifies,
named nowhere in the Scope table, Chunk H, or the Boundary B tally.

Blocking under C0 because the damage is silent and lands on a trust ceremony.
`AGENTS.md`'s own operational pitfall says a frozen file whose bytes change does
not redden anything; Chunk H exists precisely to hand the Maintainer the list the
suite will never produce. A list short by one sends the re-anchor ceremony in
under-informed, and no gate anywhere will contradict it. It is also the exact
failure `AGENTS.md` > *Confirm the instrument before trusting an absence* exists
to prevent. The `full` mode conclusion is unaffected — three frozen files already
force the refusal — so this is a contract-surface accounting defect, not a mode
error.

**Remedy.** Add `bootstrap/tests/test_security_stack.py` to `:363`'s enumeration
and to the Scope table's frozen accounting; change `:432` to four. Keep `:363`'s
"every `FROZEN-MODIFIED` entry this plan creates" wording and add one clause
telling the implementer to re-derive the list from the manifest at commit time
rather than transcribing the plan's — the plan's prose is what just failed.

### Finding B2 (blocking) -- Chunk G transcribes a field measurement whose two categories do not sum to its own total, into a durable file a public issue comment will name

`:328` instructs the implementer to record *"the adopter's field measurement —
299 discoverable, 93 in closure, 212 outside, 144 findings, 27 reachable"*.

**93 + 212 = 305, not 299.** The figures are real and inherited, not invented
here: proposal `:77-83` carries the table (`299` discoverable, `93` in closure,
`212 (71%)` outside) and `:390-391` restates the five inline. `71%` is `212/299`
while `93/299` is `31%` — the two shares sum to 102%, so this is not rounding.
No third bucket is stated to absorb the 6, and neither document says which figure
is the odd one.

Blocking under C0 because of where it lands. `dev/measurement/` is durable and
gate-adjacent, and Chunk M then posts a public comment on issue #6 that **names
this file**, to the adopter who supplied these numbers, under a stated honesty
bar. Handing someone their own field data back as a partition that does not close
is not undone by editing a file afterwards, and the plan gives the implementer
nothing that would make them notice — "transcribe" is the whole spec.

**The remedy is neither a narrowing nor a relitigation.** Gate 4's accepted
outcome is that the field evidence does not evaporate; recording it as reported
*with the discrepancy visible* delivers that more completely than a clean-looking
partition would.

**Remedy.** One added clause in Chunk G item 1: record the five figures as
reported, attributed to issue #6, with an explicit note that the in-closure and
outside counts exceed the stated discoverable total by 6 and that this plan does
not resolve which figure moves. Optionally Chunk M's #6 comment asks the
reporter. Do **not** silently adjust a number to make it close.

### The two disclosed items -- the calls this pass owes

**Chunk B's second site (`content-security.md:89-91`) is genuinely added scope,
and I cannot authorize it.** The accepted terms name one passage: D1b at proposal
`:874-883` and `:1284-1291` cites `content-security.md:122-123`, and the
Decision's accepted-terms summary at `:2447` says *"syncs copy to
`content-security.md:122-123`"*. Having read both passages, `:89-91` is not a
wrapped continuation of that range — it is a separate normative sentence in a
separate section (the exit-code contract list), ending *"prune the baseline."*
No revision or review round saw it. Under `AGENTS.md` that is "a contract the
review never saw" — a deviation, and additions are deviations exactly as removals
are. The plan's own fence at `:99` is therefore correct: Chunk B needs the
**Maintainer's explicit allowance** before it lands. I am also not striking it —
narrowing on a reviewer's own authority is what the scope-floor rule forbids.

**Maintainer question, one sentence.** *Chunk B also wants to scope the exit-3
bullet at `content-security.md:89-91` ("prune the baseline"), which the accepted
proposal named nowhere — may it?* **Recommended default: yes.** Refusing leaves
one file carrying both the new scoped instruction and the old unscoped one, with
the unscoped copy in the exit-code contract an operator reads *first* on exit 3
— which is most of D1b's own stated reason for touching this file (proposal
`:879-880`). Three lines of prose, in the file D1b already opens, with no code,
exit-code or test consequence.

**Chunk A's `load_audit_roots()` degrade is not scope in either direction, and no
allowance is owed.** It adds no deliverable, no exit path, no reported field and
no operator-visible surface beyond the message D1 already rewrites; it is the
failure behavior of an input D1's own message introduces. The plan's handling
needs no change: pinned by
`test_unresolvable_roots_degrade_the_message_without_changing_exit_three`
(`:148`) and named for the code reviewer at `:458`.

### Note N1 (non-blocking) -- Chunk C's `unknown` set needs an environment enumeration the plan never names, and Chunk D's annotation rule is unstated

`:192` fixes the return as `tuple[frozenset[str], frozenset[str]] | None` — two
name sets. `:200` then requires that after an ungrammatical requirement edge *"the
whole un-reached remainder"* annotate `unknown` rather than `out-of-closure`. A
rooted walk never visits that remainder, so materializing it needs an enumeration
of every installed distribution — `importlib.metadata.distributions()`, which the
plan never names; `:198` names only `packages_distributions()`, and only as the
*root*-resolution authority. (`:204`'s unresolvable-root case is fine: `:195`
routes it to `None`.) Relatedly, `:261` says "annotate each reported distribution
… against Chunk C's closure" without stating the three-way rule, in particular
what a reported name absent from both sets gets.

Non-blocking: `test_an_ungrammatical_requirement_edge_is_unknown_not_out_of_closure`
pins the behavior and the stated falsifier reddens on the wrong choice, so the
implementer is forced to the right answer — they just have to rediscover it.

**Remedy.** In Chunk C, say the walk enumerates
`importlib.metadata.distributions()` to materialize the remainder, and note that
this same enumeration is the "discoverable set" Chunk G's tripwire is a fraction
*of*. In Chunk D, state the rule in one line: in `in_closure` → `in-closure`; in
`unknown` → `unknown`; in neither → `out-of-closure`; walk returned `None` → all
`unknown`.

### Note N2 (non-blocking) -- two acceptance criteria demand "clean" from whole-repo gates that are red today for unrelated reasons

`:174` (Chunk B) and `:315-316` (Chunk F) require `link_check.py` and
`quality_gate.py --sub neutrality` **clean**; `:400` repeats both plan-wide.
Measured above: `link_check.py` exits 1 with 3 findings in
`documentation-plan.md`; neutrality exits 1 with 79 FAILs, none in a file this
plan touches. As written, a correct Chunk B or F cannot satisfy these bullets, so
the implementer either blocks on unrelated red or silently redefines "clean" —
the second being likely, and it quietly retires the criterion. Non-blocking: the
failure is loud at run time and the Boundary B record already has a
non-pass-disposition field.

**Remedy.** Scope both to "no new findings beyond the pre-existing baseline," and
name that baseline in the plan the way `:401` already names D2's un-smokable
path: `link_check` 3, `neutrality` 79, `verify_integrity` 21, measured 2026-08-31
at `2c21818`.

### Note N3 (non-blocking) -- Chunk G's tripwire node is the one new node with no non-vacuity guarantee

`:402` claims every new node is shown non-vacuous "by Chunk E's ledger for the D2
oracle and by the Chunk A/C falsifiers elsewhere" — Chunk G is in neither list.
Its node (`:344-347`) asserts a *fixture* closure stays under a threshold derived
from a *real* environment measurement (item 2), and its falsifier — restore the
extras-inclusive policy and the node reddens — only holds if the fixture's
extras-gated subtree is itself large enough to cross the threshold. Nothing says
so, and a fixture built without that property is green under both policies: a
tripwire that reports success without testing its claimed property, which
`AGENTS.md` calls a worse defect than no tool because it is silent.

**Remedy.** State the fixture constraint in Chunk G (the extras-gated subtree
alone must cross the recorded threshold), and add G's node to `:402`'s
non-vacuity coverage with its falsifier required to be *run and recorded*, not
merely stated.

### Nits

* **`:231`'s "2,314-marker environment corpus" carries no `as_of`.** The same
  measurement in this environment today gives 2,373 requirement strings with a
  marker clause — likely drift, and harmless, since the plan is explicit that the
  corpus is a positive control no node asserts against. But `doctrine/plans.md` >
  *Count claims* wants the date and the counting rule attached.
* **A `Chunk D` name collision inside the test file.**
  `bootstrap/tests/test_security_stack.py:1240-1533` already carries a banner
  comment `# --- Chunk D: the denominator, the dispositions, and the CLEAN gate
  ---` from earlier, unrelated work, and `:424` routes *this* plan's Chunk D
  nodes into that same range. Two different "Chunk D"s in one region is the
  decayed-coordinate problem `AGENTS.md` > *Durable artifacts stand without the
  deliberation that produced them* warns about; one line telling the implementer
  not to extend or reuse that banner is enough.

### Verdict

**REVISE** — the plan moves to `revising-plan`. Two blocking findings (B1, B2),
three notes (N1–N3), two nits, one Maintainer question routed above.

Both blocking findings are small, local corrections to a plan that is otherwise
an accurate and executable translation of the accepted proposal; neither touches
its design, chunking, or scope. What could have found otherwise and did not:
every file:line citation I opened resolved as claimed, both byte-identity hashes
matched on disk, both call-site counts matched on `grep -c`, no new symbol or
node name collides with anything in the tree, `claim_check.py` is clean over the
plan, and `Scope delta: preserved` survives a walk of every accepted outcome into
a named chunk. Chunk B stays fenced on the Maintainer's answer however B1 and B2
are dispositioned; Chunks A and C–H are ready to implement once B1 and B2 land.

## Response to plan review -- Claude (author) -- 2026-08-31

Every finding is folded **into the operative cells in place**, per
[`doctrine/plans.md`](../../doctrine/plans.md) — a plan answers its review in its
cells, not in a contract revision. This table is a **pointer**, not a second
copy: read the cell, not the row. Nothing above the `## Plan review` heading is
argued here; the appended pass itself is untouched.

| # | Disposition | Where it landed |
|---|---|---|
| **B1** | accepted | *Scope* > surfaces table now carries a `[frozen]` flag per file plus the manifest-derived count; *Chunk H* > first bullet names the fourth file and adds the re-derive-from-the-manifest instruction; *Verification* > Boundary B mode reads four. |
| **B2** | accepted | *Chunk G* > item 1 — the five figures stay as reported and attributed, with the 6-count gap and the 102% share sum written into the record and explicitly unresolved; Chunk M may ask, not assert. |
| **N1** | accepted | *Chunk C* > new **discoverable set** bullet (the enumeration is the file's existing `installed_distribution_names()`, tied to Chunk G's denominator); *Chunk D* > the **Annotate** bullet now states the three-way rule and its evaluation order. |
| **N2** | accepted-with-variation | *Acceptance criteria* > **Standing gates** carries the measured baseline table once; *Chunk B* and *Chunk F* acceptance point at it instead of demanding "clean". **Variation**: the reviewer's remedy named the baseline inline in the plan; naming it in three places would be three cells answering one question, so it is stated once and referenced twice. `verify_integrity`'s 21 is in the same table for the same reason. |
| **N3** | accepted | *Chunk G* > new **fixture constraint** paragraph, and its falsifier is now *run and recorded* rather than stated; *Acceptance criteria* > non-vacuity bullet adds G's node and closes the list. |
| **NIT-1** | accepted (re-measured) | *Chunk C* > marker-corpus sentence — re-measured under the canonical interpreter rather than dated forward: **2,373** across 301 distributions, `as_of 2026-08-31`, with the counting rule stated. The superseded 2,314 is named so the change is not silent. |
| **NIT-2** | accepted | *Chunk D* > new paragraph before **Acceptance** forbidding extension or reuse of the pre-existing `# --- Chunk D: ...` banner at `test_security_stack.py:1240` and barring any chunk/finding coordinate from a new node name, banner or docstring. |
| **Maintainer question** | routed, allowed | *Scope* > **AUTHORIZED ADDITION** carries the question and answer verbatim as a blockquote, replacing the fence; *Sequence* row B and *Chunk B* drop the gate; *Scope delta* carries the addition separately from `preserved`. |

Nothing is declined.

**What I re-verified rather than took.** Both blocking findings were checked
against the instrument, not the review: `frozen_files` in
`bootstrap/tests/fixtures/gate_manifest.json` read directly (183 keys) confirms
**four** frozen files among this plan's surfaces and confirms the two module docs
are **not** frozen; proposal `:77-83` and `:390-391` confirm the transcribed
figures and the unclosed partition. The three red gates were re-run at `e67959a`
and returned the reviewer's counts unchanged (3 / 79 / 21), so the baseline table
is a measurement of this tree and not a quotation. `installed_distribution_names()`
(`:1033-1040`) and `_canonical_name` (`:1027-1031`) were opened before N1's remedy
named them, so Chunk C reuses an existing helper instead of specifying a new one.
The stale banner at `test_security_stack.py:1240` was read in place.

**Status** moves to `ready-to-implement`: both blocking findings are folded, all
three notes and both nits with them, and Chunk B's fence is discharged by the
recorded authorization rather than removed.

## Implementation verification -- Claude (Implementation) -- 2026-08-31

**Model**: claude-opus-5 (Claude Opus 5)
**Boundary B mode**: full — as this plan declared in advance. Bounded mode was
refused and no `**Bounding**` line is owed. **Four** gate-manifest-frozen files
changed and two lockfile records were reconciled, so the change touches a
**contract surface**; the content scanner and the dependency-audit orchestrator
are **security-stack** surfaces.

**Tested SHA**: `fd28a831ffedcaebf3d4572397d60a108c7352fa`
**Reviewed range**: `d49059d..fd28a83` (eight commits, A–H; **Chunk M was not
executed** — see *Chunk M*, below).
**Interpreter**: `/Users/kendal30/conda_envs/lhm/bin/python3.13` — **Python
3.13.13** (conda-forge, Clang 19.1.7), Cairn's canonical interpreter.
**Clean state**: `git status --short` empty before the run and empty after it;
no file was modified by any command in the table.
**Where it ran**: an isolated git worktree of this repository, not the primary
checkout. That matters for exactly one figure — see *Known omissions* item 3.

### Commands

| # | command | exit | outcome | elapsed |
|---|---|---:|---|---:|
| 1 | `CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0` | 0 | **3211 passed**, 0 failed, **0 skipped, 0 xfail, 0 xpass**, 3 warnings | 562.6 s |
| 2 | `python scripts/quality_gate.py --sub neutrality --sub redundancy` | 1 | neutrality `fail=79 info=21`; redundancy `fail=0 info=0` | 1.0 s |
| 3 | `python scripts/check_cairn.py` | 1 | 3 issues across 174 files | 2 s |
| 4 | `python scripts/link_check.py` | 1 | 3 issues across 174 files | 2 s |
| 5 | `python bootstrap/verify_integrity.py --target .` | 1 | 21 violations | <1 s |
| 6 | `python scripts/claim_check.py dev/plans/scanner-claim-scope.md` | 0 | no flags | <1 s |
| 7 | `python scripts/claim_check.py dev/measurement/pip-audit-closure-ratio.md` | 0 | no flags | <1 s |
| 8 | `python scripts/content_scan_runner.py` (D1 smoke) | 0 | 76 audited text files, clean | 3 s |

### Disposition of every non-pass

Commands 2–5 exit non-zero against the **pre-existing baseline** this plan
records under *Acceptance criteria* > *Standing gates*. The criterion is **no
new finding beyond that baseline**, and each count is unchanged:

* **neutrality 79** — identical to the plan's recorded 79. Checked by overlap
  rather than by count alone: the only three FAILs under
  `templates/modules/team-gated/` are `content_scan.py:329`,
  `content_scan.py:547` and `intent.py:64`, none of which this plan touches.
  **Neither `python-security.md` nor `content-security.md` nor
  `run_security_audit.py` contributes a FAIL.** (This gate is why Chunk F's new
  paragraph quotes the measured ratio without naming the package the
  measurement was rooted at: `modflow_tools` is itself an unsanctioned token
  under `templates/`, as those first two FAILs show.)
* **redundancy 0**, **claim_check 0** — clean, as required.
* **link_check 3** — identical to the recorded baseline, all three at
  `templates/modules/default-on/documentation-plan.md` lines 103, 113 and 123.
* **verify_integrity 21** — identical to the recorded baseline. It read **23**
  after Chunk B and before Chunk H's reconciliation, and Chunk H returned it to
  21; neither reconciled path appears in the 21.
* **check_cairn 3** — the plan records this gate as clean (0), and it *is* clean
  in the primary checkout. All three findings are
  `dev/reviews/2026-08-27-code-review-c5-c6-removals.md` citing
  the suite-cost and suite-runs records under `dev/measurement/`, which are
  **gitignored** (`.gitignore:18-19`) and therefore absent from a fresh
  worktree checkout while present on disk in the primary tree. Their paths are
  named here without backticks on purpose: `claim_check.py` hard-flags a cited
  path that does not resolve, and in this worktree they do not. This is a
  property of where the run happened, not of the change: the count was 3 before
  the first implementation commit and 3 after the last. A reviewer running in
  the primary checkout should expect 0.
* **3 pytest warnings** — all `stevedore/extension.py:187`, a deprecation
  notice from a third-party dev dependency. Nothing this plan touches.

### Plan-specific acceptance

* **Invariant (i)** — the emitted-report triple multiset equals the literal
  fixture multiset: `test_reported_rows_match_the_literal_expected_triples`.
* **Invariant (ii)** — the seven pre-existing `Coverage` fields and the returned
  `(status, tier)` are identical with the annotation present and absent, the
  appended `vulnerable` field being the only difference:
  `test_the_established_coverage_fields_are_unchanged_by_the_annotation`.
* **Invariant (iii)** — exit codes unchanged: the pre-existing exit-contract
  nodes (`TestRunnerExitContract::test_stale_baseline_is_three`,
  `test_d_t2d_report_findings_and_exit_code_cannot_contradict`,
  `test_d_t2_one_unknown_gates_clean`,
  `test_d_t1_a_skipped_distribution_is_never_scanned`) pass **unmodified**, as
  do all eleven `run_pip_audit_pass` and six `classify_pip_audit_output` call
  sites.
* **Invariant (iv)** — neither tool writes the residual baseline: unchanged;
  nothing in this range adds a write.
* **Invariant (v)** — `_print_summary`'s signature:
  `test_print_summary_signature_is_positionally_stable`.
* **Invariant (vi)** — byte-identity, measured on the tested SHA:
  `scripts/content_scan_runner.py` = `templates/modules/team-gated/content_scan_runner.py`
  = `dc34b74062c4b69a0b5667a74904e120cb949717453e80e581bc68344bc696a1`;
  the three `content-security.md` copies (`templates/modules/team-gated/`,
  `dev/modules/`, `dev/.cairn/base/dev/modules/`) =
  `030f15ca2eaf82954490ec1d6b4423ad92035d370c33b6783273477a3049b7b2`.
* **Invariant (vii)** — the closure walk imports nothing outside the standard
  library: `test_closure_walk_imports_only_the_standard_library`, which reads
  the orchestrator's own import graph with `ast` and carries two controls (the
  instrument sees the file's imports; the comparison would flag a third-party
  name).
* **Non-vacuity** — every new node is covered. Chunk A: four falsifiers run.
  Chunk C: five falsifiers run. Chunk D/E: the five-mutation ledger plus the
  raise-pair, in commit `1f418b7`. Chunk G: its own falsifier run and recorded
  in `759fc6c` (extras-inclusive policy → `closure 71/100 exceeds the 50%
  recorded in pip-audit-closure-ratio.md`). No new node is outside this list.
* **D1 exit-3 smoke on this tree, read-only** — the real script loaded against
  the real roots manifest with a synthetic stale entry prints the audited set
  (`AGENTS.md, .agents/skills, dev, docs, RULES.md, CLAUDE.md, VENDOR.md`), the
  disagreement framing, the cross-consumer instruction and the lockfile clause.
  Nothing was written.

### FROZEN-MODIFIED — the re-anchor the Maintainer owes

Re-derived at commit time by filtering the gate manifest's own 183
`frozen_files` keys against the paths this range changed — not transcribed from
this plan's prose. The suite does **not** diff the committed fixture, so the
green run above is **not** evidence that no re-anchor is owed:

* `bootstrap/tests/test_security_stack.py`
* `scripts/content_scan_runner.py`
* `templates/modules/team-gated/content_scan_runner.py`
* `templates/modules/team-gated/run_security_audit.py`

No `bootstrap/_scaffold/` file changed, so **no AST attestation re-anchor is
owed** — stated because its absence is otherwise indistinguishable from an
oversight.

### Known omissions

1. **D2 cannot be smoked on this tree.** `python-security` is not in Cairn's
   installed roster and the orchestrator has no self-hosted twin under
   `scripts/`, so the pip-audit leg is exercised only through
   `test_security_stack.py`'s orchestrator fixture against the template file.
   The plan records this as a real omission and it remains one.
2. **`base_hash` is not equal to `hash`** for the two reconciled lockfile
   records — reported in `fd28a83` rather than closed quietly, as Chunk H
   requires. `--finalize` advances `hash` only. Cairn is its own upstream here
   and the templates moved in the same range, so this reads as a self-hosted
   install one upgrade behind its own source rather than a fork; the on-disk
   base cache already carries the new bytes. Not repaired here.
3. **check_cairn's 3 findings are a worktree artifact**, not a regression — see
   *Disposition*, above. Re-measure in the primary checkout to see 0.
4. **The interpreter version in three earlier commit bodies is wrong.** Commits
   `69906a6` (A), `236e19a` (B) and `73c78e4` (C) say "Python 3.13.7". The
   interpreter was **Python 3.13.13** throughout; nothing else about those runs
   changes. Corrected here rather than by rewriting the commits.
5. **A stale precedent in this plan's own Chunk G rationale.** The plan cites
   the suite-cost record (again unbackticked, for the reason above) as one of
   two precedents for the folder's membership rule. That file is gitignored and
   untracked, so it is not a committed precedent. The other precedent
   (`dev/measurement/gitleaks-version-support.md`) is tracked, is an apparatus
   measurement, and a test binds to it — and the new record follows that
   pattern exactly: `test_closure_stays_a_bounded_fraction_of_the_discoverable_set`
   parses the threshold out of the record itself. The placement stands on the
   one live precedent.

### Chunk M -- NOT EXECUTED

**Chunk M is MAINTAINER-GATED and was skipped in full.** No comment was posted
to issue #5 or #6, no `gh` invocation was made, and no GitHub state was read or
changed. The authorization the chunk names does not exist, and neither does the
gate it also requires (the implementation's External Security code review,
which has not happened). It remains outstanding.

### Author-disclosed reading calls

Three places where the plan admitted more than one reading and the
implementation had to choose. Each is a place to look first.

1. **Which distributions get a report row.** Rows are emitted per **vulnerable**
   distribution — the entries of `Coverage.vulnerable` — so a distribution with
   zero vulnerabilities and one the tool skipped get no row. This follows the
   field's name, the partition sentence ("N vulnerabilities across M
   distributions"), and Chunk M's own wording ("per-distribution counts, not
   per-finding records"). "Every distribution still appears" is therefore read
   as *no vulnerable distribution is omitted, whatever its label*, which is
   exactly what mutation 3 tests.
2. **`closure` on `classify_pip_audit_output` is deliberately inert.** The plan
   fixes the parameter and simultaneously requires that supplying it change
   nothing the function returns. Implemented literally: the parameter is
   accepted, marked inert at the top of the body, and the docstring says the
   seam exists so that a node can prove the annotation never became a coverage
   claim. A reviewer who thinks the parameter should be doing work should read
   that pairing first.
3. **Chunk F names the ratio but does not cite the record's path.** The
   acceptance reads "names the ratio recorded in
   `dev/measurement/pip-audit-closure-ratio.md`", and the paragraph names the
   figures. It does not cite the path, because `python-security.md` installs
   into an adopter's tree and would then point at a file only Cairn has.

## Code review -- Claude (Code Review, independent context) -- 2026-09-01

Reviewed range: `d49059d..fd28a83` (chunks A-H), as merged. SHAs are for
locatability only; nothing below rests on one.
Target: the implementation against this plan's Scope, Sequence, Acceptance
criteria and the appended `## Implementation verification`.
Prior findings: the Internal plan review's B1/B2, N1-N3 and two nits, folded by
the Response and confirmed folded here. First pass over code.
Assurance path: high-assurance (security-stack and contract surfaces).

**Model**: claude-opus-5
**Tier**: External (stance), Code Review
**Independence**: fresh context; I wrote no part of the plan or the
implementation. **Same agent type as the implementer** -- structural freshness,
not cross-vendor distance. Read that discount into the pass.
**Findings**: raised -- 5 (1 blocking, 3 notes, 1 nit)
**Verdict**: REVISE -- status `revising-code`

### Should this have been built this way

Yes, with one disclosure missing. The load-bearing decision is that the
reachability axis is **rendered, never stored**: `closure` enters
`classify_pip_audit_output` and is discarded (`run_security_audit.py:920`), the
labels are joined to `Coverage.vulnerable` at print time (`:1381`), and
`unknown_total` keeps its three original terms. I walked every path a label could
take into the tier and found none. That is what makes an admittedly approximate
walk safe to ship; storing labels on `Coverage` would have put an approximate
resolver inside the object the CLEAN gate reads. Two further calls I would have
made the same way: `resolve_declared_closure` returning `None` for every total
failure, with the leg's `try/except` mapping a raise onto the same `None` (one
fail-closed path, not two); and the caps returning `None` rather than a truncated
closure, which would silently relabel everything it did not reach. The inert
`closure` parameter is dead weight a maintainer will be tempted to "fix" --
defensible as a declared seam, but the one place the discipline rests on a
comment rather than on structure.

### The strongest rejected alternative

**Narrow the leg to audit only the declared closure** -- issue #6's option 2,
refused on the reporter's own caution. Its strongest form is not convenience: it
makes the walk's correctness *loud*. As shipped, a walk error is a silent
mislabel on a row nobody re-checks; narrowed, the same error means a distribution
was never audited -- visible in the UNKNOWN count, and the tier acts on it. It
still loses, for a reason this implementation makes concrete rather than assumed:
narrowing changes the question from *"is the environment I execute in
vulnerable?"* to *"is my closure vulnerable?"*, so a wrong closure **drops
findings** instead of misordering them -- and `pip-audit-closure-ratio.md` §4
measures 6 of 309 top-level names here as ambiguous namespace packages, for which
the narrowed design would audit nothing and say so quietly.

### What would falsify this pass

* A label reaching `unknown_total`, the tier or an exit code on a path I did not
  walk. That is the bright line; its breach makes the axis unshippable.
* An extras-inclusive walk over a real environment landing *below* 50% -- §3's
  separation would then be an artifact of the six roots it measured.
* `test_reported_rows_match_the_literal_expected_triples` surviving mutation 3
  (`if annotation == _REACH_OUT: continue`); if it did, the oracle is decorative.
* The twins diverging on disk. Checked: both runners `dc34b740…`, the three
  `content-security.md` copies all `030f15ca…`, matching the record.

### Findings

**B1 (blocking) -- `out-of-closure` provably contains dependencies the project
declared, and the doc telling an operator to deprioritize it says nothing of it.**

`_marker_extra_disposition` (`run_security_audit.py:1157-1159`) returns
`extras-gated` for any `extra ==` equality and `_requirement_edge` (`:1184`)
turns that into `skip`, so the edge is never followed -- whether or not that
extra was installed. `installed_distribution_names()` still enumerates the
distribution, so with `remainder_unknown` false it is in neither set and
`annotate_reachability` (`:1351`) returns `out-of-closure`. Concretely: a project
declaring `plotting = ["matplotlib"]` under `[project.optional-dependencies]` and
installed as `pip install .[plotting]` gets `matplotlib -- out-of-closure`.
`python-security.md:72-74` calls the label "with respect to your declared
dependency closure" and then instructs "**Start with `in-closure`, then
`unknown`**". An optional-dependency group *is* declared; the sentence names a
set wider than the walk established and the instruction says to skip the
difference. §3's extras-inclusive table puts the excluded set near 180
distributions for the reference root, so it is not a corner.

Blocking, weighed against the bar: it changes no exit code and drops no finding,
so the damage is bounded, but it is an **operator instruction whose scope exceeds
its evidence**, shipped into adopter trees where correcting it costs an upgrade --
the exact failure class D1 exists to answer. The policy is settled and I do not
reopen it: following extras re-inflates the closure to 78% and kills the axis.

**Remedy.** One sentence in `python-security.md`'s new paragraph: extras-gated
requirements are not followed, so a dependency installed through an extra reads
`out-of-closure`; read the label as *"not reached by the default closure"*, not
*"not yours"*. And qualify `:1229` -- "every failure moves a distribution toward
`unknown`" is true of failures and false of this exclusion.

**N1 (note) -- the REACHABILITY banner claims over a set wider than its own
rows.** `:1388-1389` prints "every reported distribution appears either way";
`:1522`, immediately above, defines "reported" as the child's full
`len(coverage.names)` set. Rows come from `coverage.vulnerable`, so the fixture's
5 reported distributions yield 3 rows. The disclosed *reading* is right -- rows
per vulnerable distribution is what "N vulnerabilities across M distributions"
and Chunk M's "per-distribution counts" both mean, and what mutation 3 tests; the
sentence asserts the other one. Non-blocking: the intended sense is recoverable
and nothing carrying a finding is omitted. **Remedy**: "every *vulnerable*
distribution appears whatever its label."

**N2 (note) -- a plan-stated Chunk C falsifier does not reproduce; a substitute
ran and the record does not say so.** Plan `:263` states "use an unanchored search
for the identifier and the `~` node goes red".
`_REQUIREMENT_NAME_RE.search("cffi~=1.0")` returns `cffi`, exactly as `.match`
does, so `test_requirement_identifier_stops_at_the_version_specifier`
(`test_security_stack.py:1714`) stays green. Commit C's ledger records a different
mutation (`~` admitted into the identifier class) that does redden it; the record
then summarizes "Chunk C: five falsifiers run" (plan `:937`), which reads as the
plan's five. Non-blocking, and the substitute is the better mutation: the stated
form reddens `test_an_ungrammatical_requirement_edge_is_unknown_not_out_of_closure`
(`:1811`) instead, so anchoring is pinned either way. **Remedy**: one line naming
the substitution and why.

**N3 (note) -- the tripwire's framing promises an environment check; the node
checks a policy over a synthetic fixture.** `pip-audit-closure-ratio.md:10` and
`:121` describe a wire that trips when a closure re-inflates.
`test_closure_stays_a_bounded_fraction_of_the_discoverable_set` (`:2087`) builds a
100-name literal environment and asserts 11/100 <= 50% and 71/100 > 50% -- a
genuinely non-vacuous **policy** regression detector, pinning the threshold from
both sides, more than plan-review N3 asked. But no real ratio is measured at test
time, so a re-inflation from any other cause trips nothing. **Remedy**: one clause
in §3 saying the node detects a change in the extras policy against a fixture, and
that the environment ratio is re-measured by hand.

**Nit -- citations written without backticks so `claim_check.py` cannot see
them.** Plan `:983` and `:895` name gitignored `dev/measurement/` records bare,
disclosed as deliberate. Honest, but it makes "claim_check 0" a weaker signal
than it reads as. Mark it at the citation site, not only in the record.

### The verification record, Chunk M, and the re-anchor

The record holds. `check_cairn.py` in the primary checkout returns **0 across 174
files**, so the record's worktree-artifact disposition of its `3` is correct --
that was the one figure I would otherwise not have relied on, since the plan
requires that gate clean and the run never observed it clean. Scope is exactly
the eleven files the Scope table names: nothing authorized is undelivered,
nothing extra shipped, `bootstrap/requirements-dev.txt` untouched, and the
stdlib-only node carries two live controls.
`test_the_established_coverage_fields_are_unchanged_by_the_annotation` is true by
construction today (`_ = closure` guarantees it) -- not a defect, but a change
detector aimed at the future edit that would breach the bright line, reddened by
Chunk E's mutation 4. Named so nobody later reads it as evidence about the
current implementation.

**Chunk M is done**: issues #4, #5 and #6 were closed 2026-09-01 on Maintainer
authorization, after this range landed; withholding it during implementation was
correct, and no forge contact happened without the gate. The gate-manifest
re-anchor for the four FROZEN-MODIFIED files (`test_security_stack.py`, both
`content_scan_runner.py` twins, `run_security_audit.py`) is **deferred by the
Maintainer, not forgotten** -- a green suite is not evidence that none is owed,
and the list was re-derived from the manifest's own keys rather than transcribed.

### Verdict

**REVISE** -- one blocking finding (B1), three notes, one nit. Status moves to
`revising-code`; the author's revision closes this loop and no second pass is
owed. B1 is a one-sentence disclosure plus a qualified docstring line, not a
design change; N1 is one word. Everything structural here is sound, and the parts
I attacked hardest -- the bright line, the literal oracle, the fail-closed
pairing, twin parity -- held.
