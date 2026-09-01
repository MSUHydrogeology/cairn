# Plan: Portable sweeps cannot run

**Source proposal**: `dev/proposals/archive/2026-08-20-claude-portable-sweeps-cannot-run.md`
— accepted as revised (Revision 4) on 2026-08-20. **The plan-open commit archives
the source proposal**, so the path above is where it lives from that commit
onward (`dev/plans/_template.md:18-19`, `doctrine/plans.md:40-41`).
**Status**: archived
**Plan review**: required(**Internal**) — carried verbatim from the proposal
header. The **Security Review** the implementation carries is a *different
instrument*: mandated by the portable-sweep executable trust root `AGENTS.md`
names, taken as an **External Security code review** at implementation time per
the Amendment §3, and it neither satisfies nor is satisfied by this plan's
Internal pass.
**Opened**: 2026-08-31

## Source proposal

Five defects in the `portable-security-sweeps` adapter runner, each of which
alone stops the module running: the probe and parser were specified
independently (D1), the inert-key allowlist refuses ordinary developer config
(D2), the runner's own admission comment points at a doc the module does not
install and misstates what an evidence record does (D3), the leg argv sends a
`--timeout` value the adapter rejects (D4), and the adapter's overloaded exit
`1` makes a usage error indistinguishable from a findings result while adapter
stderr reaches durable sinks (D5). The plan executes that decision. It does not
re-litigate it.

**No forward-reference paths.** This plan creates no new file; every edit lands
in a file that resolves today. The one path that resolves only *after* the
plan-open commit's own `git mv` is the header's archive destination.

## Scope

The five defects, in `templates/modules/team-gated/run_portable_security_sweeps.py`
(**the source**, edited first) and its byte-identical twin
`scripts/run_portable_security_sweeps.py`; the tests in
`bootstrap/tests/test_portable_security_sweeps.py`; the module doc
`templates/modules/team-gated/portable-security-sweeps.md`; and the ledger
`dev/measurement/gitleaks-version-support.md`. Plus the issue-closure chunk the
Amendment added.

**Out of scope, and the proposal says so explicitly:** executable resolution and
the revalidation points; the policy schema; `child_env`; the exit precedence;
and the contents of `_ADMITTED_ARTIFACTS` (`scripts/run_portable_security_sweeps.py:112-114`)
— **no artifact is admitted by this change**, and the sha256 in issue #4 arrived
by the candidate channel.

**Measured drift since the proposal was written:** none in the source — every
coordinate the proposal cites still matches. One host fact *has* changed:
`gitleaks 8.30.1` is now on this host's `PATH` (`/opt/homebrew/bin/gitleaks`),
where the ledger's `as_of 2026-08-05` measurement says it is not
(`dev/measurement/gitleaks-version-support.md:65-67`). Chunk G is therefore
performable here; chunk F corrects the ledger claim — ruled **added scope** by
the plan review and **authorized by the Maintainer on 2026-08-31**, quoted
verbatim under F's acceptance criterion.

### Documentation / doctrine surface

Descriptive layer only — the module doc, the measurement ledger, runner comments
and docstrings. **No doctrine rule changes**, so the doctrine-evolution
rate-limit gate is not engaged. `AGENTS.md`'s portable-sweep paragraph is re-read
for agreement in chunk F and is expected to need no edit — none of the properties
it enumerates moves.

## Sequence

Lettered to match this surface's plan family (`dev/plans/archive/portable-security-sweeps.md`).
Order is the proposal's: D1 → D2 → D4 → D5 → D3, because the corrected comment
must state what is true *after* D4 and D5 land.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| A | **D1 — extraction between probe and parse.** One anchored, total extractor accepting exactly `gitleaks version <X.Y.Z>` or bare `<X.Y.Z>`, reached by both probe call sites (`:1381`, `:1733`). `parse_version` (`:275-285`) is **not modified** — `None` keeps meaning *unmeasured*. `fake_tool`'s `--version` default flips to the banner shape; the bare form stays an explicit parametrization | — | 1 commit |
| B | **D2 — a structural inert-key fence. Four deltas at `scripts/run_portable_security_sweeps.py:624-628`, each separately pinned**: the `remote` subsection widens from `[^.]+` to an anchored greedy `.+`, the `branch` subsection widens likewise, `glab-resolved` joins the remote alternation, `vscode-merge-base` joins the branch alternation. The variable stays a closed named set. Non-inert keys **accumulate into one refusal** naming at most `_SCREEN_MAX_NAMED_KEYS = 10` of them plus the elided count; the **two** raises that precede the inert scan in the same loop — the non-file-origin check (`scripts/run_portable_security_sweeps.py:781-783`) and containment — **both stay first-failure** | — | 1 commit |
| C | **D4 — integer-seconds `--timeout`.** The fake gains a per-subcommand flag table derived from the adapter's own `--help` and **lands red first**; then `_leg_argv` (`:1628`) emits the measured integer form and the pinning test is re-pointed | — | 2 commits (red fake, then fix) |
| D | **D5 — exit split and no adapter bytes in any durable outcome.** Pin `--exit-code 42` in the leg argv and set `_EXIT_FINDINGS` to match; rewrite `classify_leg`'s signal (`:995-998`) and unknown-exit (`:999-1003`) reasons as runner-owned messages carrying the numeric exit or signal and nothing from the adapter | — | 1–2 commits |
| E | **The admission matrix proves the exit contract it now depends on** (invariant viii). `cmd_verify_version_support`'s `end_to_end` block runs three recorded scenarios per subcommand, and the ledger says what an evidence record must now contain | — | 1 commit |
| F | **D3 — the comment states what is true.** Correct the runner header comment (`:86-90`, `:99-102`); re-read the module doc and `AGENTS.md` for agreement (**human attestations, recorded in the commit body**); correct the ledger's stale PATH measurement (**Maintainer-authorized addition — see F's acceptance criterion**) | — | 1 commit |
| G | **Real-adapter instruments.** The two smokes the proposal names, run against real gitleaks and recorded | — | evidence, no source change |
| M | **Close adopter issue #4** against the proposal's five gates | **MAINTAINER-GATED** | one comment, one close |

### Fences and mechanical consequences, stated once and bindingly

* **Byte-twin discipline binds A through F.** Every chunk that touches the
  runner edits `templates/modules/team-gated/run_portable_security_sweeps.py`
  **first**, mirrors into `scripts/run_portable_security_sweeps.py` in the
  **same commit**, and re-verifies identity in that commit with
  `test_the_runner_twin_is_byte_identical_to_its_template_source`
  (`bootstrap/tests/test_portable_security_sweeps.py:2300`) and
  `test_every_self_hosted_twin_stays_byte_identical_to_its_source`
  (`bootstrap/tests/test_notice_install.py:114`). A commit that moves one side
  only is a defect, not a step.
* **Gate-manifest and lockfile staleness: reported, not repaired.** Both
  runner paths carry the pre-change sha256 in
  `bootstrap/tests/fixtures/gate_manifest.json:4950-4954` and `:5135-5139`, and
  in `dev/.cairn/cairn-lock.yml:414-419`. The suite does not diff the committed
  fixture, so **nothing goes red and a green suite is not evidence the
  re-anchor is unowed**. The implementing agent names both stale entries in the
  final commit body; the re-anchor is the Maintainer's, per
  `bootstrap/REANCHOR_RUNBOOK.md`. The lockfile is tool-owned and
  regenerate-only — never hand-edited.
* **`_ADMITTED_ARTIFACTS` is not touched by any chunk.** Chunk E changes what a
  matrix *measures and records*; it admits nothing. Admission stays
  un-automated: an automated writer that reads an evidence record and edits the
  set is a path by which anything that can produce a record can admit a binary.
* **M does not execute without the Maintainer's word.** Closing a public issue
  publishes a claim that the reported problem is resolved.

### Invariants this plan is measured against

Inlined so the numerals used below stand without the proposal open; sourced from
Revision 4 (`dev/proposals/archive/2026-08-20-claude-portable-sweeps-cannot-run.md:2331-2345`).

* **(i)** `parse_version` stays strict; `None` means *unmeasured*.
* **(ii)** No leg runs before the configuration screen returns.
* **(iii)** `_ADMITTED_ARTIFACTS` changes only by reviewed source edit.
* **(iv)** The self-hosted runner twin stays byte-identical to its template source.
* **(v)** The emitted leg argv is accepted by the admitted adapter major.
* **(vi)** No byte originating from the adapter's stdout or stderr appears in
  `LegOutcome.reason` — on any exit code, any signal, any path, whether or not
  `read_report` was reached.
* **(vii)** A findings result and a usage error are distinguishable by exit code.
* **(viii)** The admitted exit contract is **measured per candidate**, not
  assumed from the major.

## Acceptance criteria

Per chunk, each falsifiable. Test names pin the property, not this document.

* **A** — a probe output of `gitleaks version 8.30.1` reaches `select_mode` as
  `(8, 30, 1)`; a bare `8.30.1` still does; `parse_version`'s existing tests are
  unmodified and green.
  **Decision — the raw banner survives into the two JSON-visible fields**, not
  the extractor's output. `probe_version`'s return keeps reaching
  `record["candidate_version"]` (`scripts/run_portable_security_sweeps.py:1384`)
  and `facts["adapter_version_output"]` (`:1740`) verbatim: the ledger's purpose
  is recording what the binary actually said, and the triple is derivable from
  the banner while the banner is not derivable from the triple. Pinned because
  the only existing test on either field checks presence, not shape
  (`bootstrap/tests/test_portable_security_sweeps.py:2047-2052`), so leaving it
  to the implementer is an unreviewed change to a `--json` contract.
  **Nodes**: `test_the_version_banner_extracts_to_an_exact_triple`,
  `test_the_bare_version_string_still_extracts`,
  `test_a_prerelease_suffix_does_not_extract`,
  `test_the_evidence_record_keeps_the_raw_version_banner`.
  **Falsifier**: unanchor the extractor — a fixture emitting
  `gitleaks version 8.30.1-dirty` must not parse as `8.30.1`; the prerelease
  node goes red. Then substitute the extracted triple into either JSON-visible
  field — the banner node goes red. Run both mutations and record them (S2).
* **B — all four allowlist deltas, each pinned by its own node, because each is
  independently droppable.** `branch.v1.2.remote` and `branch.release/2.0.remote`
  are INERT (the `branch` widening) and so is `remote.origin.v2.url` (the
  `remote` widening, which the `branch` cases do not exercise);
  `remote.origin.glab-resolved` and `branch.main.vscode-merge-base` — the two
  keys the Decision's D2 term names — are INERT;
  a newline-bearing key, an empty subsection and a suffix-injected variable are
  all REFUSED; a synthesized config with more non-inert keys than the cap
  produces **one** refusal naming the first ten in listing order plus the elided
  count; an include origin outside the candidate's `.git/` refuses
  **immediately**, before the inert scan completes — and so does a
  **non-file config origin** (`scripts/run_portable_security_sweeps.py:781-783`),
  the other raise in that loop, which the accumulation change must leave
  first-failure exactly as it leaves containment.
  **Decision — the cap is ten**, as `_SCREEN_MAX_NAMED_KEYS = 10` beside the
  file's other named caps (`scripts/run_portable_security_sweeps.py:609`):
  offending key names are candidate-controlled text entering a durable sink, so
  the refusal's size must not be candidate-steerable, and ten is enough for an
  operator to recognize the offending family.
  **Nodes**: `test_a_dotted_branch_subsection_is_inert`,
  `test_a_slashed_branch_subsection_is_inert`,
  `test_a_dotted_remote_subsection_is_inert`,
  `test_the_glab_resolved_remote_key_is_inert`,
  `test_the_vscode_merge_base_branch_key_is_inert`,
  `test_a_newline_bearing_key_refuses`,
  `test_an_empty_subsection_is_not_inert`,
  `test_a_suffix_injected_variable_is_not_inert`,
  `test_every_non_inert_key_is_named_in_one_refusal`,
  `test_the_refusal_names_no_more_keys_than_the_cap`,
  `test_the_refusal_states_how_many_keys_it_elided`,
  `test_an_include_origin_outside_the_git_dir_refuses_immediately`.
  **Falsifier — four mutations, one per delta, run separately.** At
  `scripts/run_portable_security_sweeps.py:624-628`: restore `[^.]+` on the
  `branch` pattern alone (the two `branch` nodes go red, the `remote` one stays
  green); restore it on the `remote` pattern alone (the reverse); drop
  `glab-resolved` from the remote alternation; drop `vscode-merge-base` from the
  branch alternation — each of the last two reddens exactly its own key node. A
  single mutation that reddens everything cannot distinguish a fully-landed D2
  from one delta of four, which is the failure this criterion exists to catch.
  Run all four and record them (S2).
* **C** — the flag-table fake lands **red against the current argv in its own
  commit**, and the recorded failure is quoted in that commit body; after the
  fix, `sent == [f"--timeout={runner._ADAPTER_TIMEOUT}"]` at
  `bootstrap/tests/test_portable_security_sweeps.py:1195`, and the ceremony's
  own call site (`scripts/run_portable_security_sweeps.py:1421`) sends the same
  form — which is invariant (v) made checkable.
  **Nodes**: `test_the_adapter_timeout_is_sent_as_integer_seconds`,
  `test_a_flag_the_subcommand_does_not_declare_is_rejected_by_the_fake`,
  `test_the_admission_matrix_argv_is_accepted_by_the_flag_table`.
  **Falsifier**: restore the `s` suffix — the flag-table fake fails. A fake
  that has never failed is not an instrument, which is why the red commit is a
  deliverable and not a courtesy.
* **D** — a findings result and a usage error are distinguishable by exit code;
  and **no byte originating from the adapter's stdout or stderr appears in
  `LegOutcome.reason`, on any exit code, any signal, and any path — whether or
  not `read_report` was reached**.
  **Nodes**: `test_a_findings_exit_is_not_the_adapters_usage_error_exit`,
  `test_no_adapter_stderr_reaches_any_durable_sink` (parametrized over exit
  `1`, exit `42`, an unknown exit, and a negative return code),
  `test_an_invalid_argv_refuses_with_the_argv_reason_not_a_missing_report`.
  **Falsifier — the canary, and it is the one that matters.** Drive
  `classify_leg` with a stderr carrying a unique secret-shaped token across all
  four cases and assert the token appears in no `LegOutcome.reason`, no summary
  JSON (`summarize()`, `:1087`), no human report (`render_report()`,
  `:1113-1137`) and no child document (`child_document()`, `:1140`). Reverting
  either branch to `_diagnostic(stderr)` must turn it red. Separately, revert
  `_EXIT_FINDINGS` to `1` — the ceremony guard at
  `scripts/run_portable_security_sweeps.py:1434` stops admitting the pinned
  findings exit, and E's matrix rows go red.
  **Evidence for the value `42`**, recorded rather than asserted:
  `gitleaks dir --help` declares `--exit-code int ... (default 1)`; measured on
  real 8.30.1 darwin/arm64, clean `0`, leaks-with-`--exit-code 42` `42`,
  invalid `--timeout` `1`, unknown flag `126`. `42` is outside every code the
  adapter chooses on its own.
* **E** — for **both** subcommands (`dir` and `git`), the emitted evidence
  record carries three measured rows: a clean fixture → exit `0`; a planted,
  redacted finding → the pinned findings exit **plus a validated report**; one
  controlled invalid-argv case → an exit that is neither `0` nor the pinned
  findings value. A matrix missing any row refuses with `admit: false`.
  **Decision — the planted-finding fixture shape**, because the obvious choice
  fails silently: a file carrying `api_key = "<a 43-character
  secrets.token_urlsafe(32) value>"`, which real 8.30.1 matches as
  `generic-api-key` and `--redact=100` empties. **Not AWS's own documented
  example key `AKIAIOSFODNN7EXAMPLE`** — the default ruleset allowlists it, so
  the scan exits `0` with an empty report (measured, 8.30.1 darwin/arm64,
  2026-08-31) and the row reads as a passing clean scan.
  **Nodes**: `test_the_evidence_record_carries_a_measured_exit_row_per_subcommand`,
  `test_a_matrix_without_a_planted_finding_row_refuses_to_admit`.
  **Falsifier**: drop the planted-finding scenario — the refusal node goes
  green, which is the failure. The ledger's own bijection nodes
  (`:1977`, `:1993`, `:2005`) stay green: no version is admitted.
* **F** — the runner's header comment references no path the `team-gated`
  module does not install, and no longer says a record "enters" the admitted
  set.
  **Node**: `test_the_runner_comment_references_no_uninstalled_path`.
  **Falsifier**: re-insert `dev/measurement/gitleaks-version-support.md` into
  the runner header comment; the node goes red.
  **The chunk's other three claims are human attestations, not checks — said
  plainly here** in the same voice as G's operator attestation and S3's "a
  person typing it", because a *confirm-nothing-changed* claim has no falsifier
  and a reader must not assume a node exists. Each is recorded in F's commit
  body, naming what was read and what was found: (1) the module doc's mode table
  (`portable-security-sweeps.md:82-85`), unreachability statement (`:96-99`) and
  cadence (`:162-174`) imply no route to full mode that has never worked;
  (2) the ledger's four-step ceremony (`gitleaks-version-support.md:26-38`)
  still reads as four steps and un-automated; (3) `AGENTS.md`'s portable-sweep
  paragraph needs no edit. A code reviewer looks for these three in the commit
  body, not in the suite.
  **The ledger's stale `PATH` measurement — added scope, and authorized.** The
  plan review ruled the correction *added scope* rather than tidying, because
  the fact post-dates the 2026-08-20 Decision, and referred it. Asked and
  answered on 2026-08-31:

  > **Question put to the Maintainer**: "The portable-sweeps plan wants to also
  > fix one sentence in dev/measurement/gitleaks-version-support.md. That
  > sentence says gitleaks is not installed on this machine. It now is --
  > version 8.30.1, measured today. The accepted proposal (2026-08-20) never
  > mentioned that sentence, so this is genuinely new scope rather than tidying,
  > which is why it needs your word. May it?"
  >
  > **Maintainer**: "Yes, fix it"

  The fence is discharged and the correction lands in F. It changes no
  disposition — the set stays empty, because no *Maintainer-supplied,
  checksum-verified* binary has been measured. Following the ledger's own idiom
  of dated measurements that are **superseded, not overwritten** (the Retirement
  log's "with the reason and the date" convention,
  `dev/measurement/gitleaks-version-support.md:75-80`), a new dated line lands
  beside the `as_of 2026-08-05` one (`:65-67`) rather than replacing it. Note
  `test_the_ledger_states_the_empty_set_consequence` (`:2005`) reads this
  section and is the node that catches a careless edit.
* **G** — two real-adapter runs, each recorded with the adapter path and
  version:
  1. `python scripts/run_portable_security_sweeps.py --target <fresh-repo> --json`
     against a fresh repository **carrying at least one commit whose identity
     comes from `GIT_AUTHOR_NAME` / `GIT_AUTHOR_EMAIL` / `GIT_COMMITTER_NAME` /
     `GIT_COMMITTER_EMAIL` in the environment**, yielding `mode == "reduced"`, a
     current-tree leg whose status is `INCOMPLETE` or `FINDINGS`, and **no leg
     with status `DEGRADED`**. Built the ordinary way — `git config user.email` /
     `user.name` — the repository carries local keys chunk B's allowlist still
     refuses, and the run returns `result: 20, DEGRADED` on `user.email` without
     ever reaching a leg (measured, 2026-08-31).
  2. `python scripts/run_portable_security_sweeps.py --verify-version-support
     <binary> --confirm-executing-an-unadmitted-binary`, which must reach a
     **real matrix result** — a record with `end_to_end` rows — rather than
     refusing on argv.
  **Falsifier**: run instrument 1 at the pre-A commit; it must produce
  `result: 5, status: INCOMPLETE` with, verbatim, `adapter version 'gitleaks
  version 8.30.1' is not an exact X.Y.Z; the version is unmeasured, so no scan
  leg was run` (measured on this host, 2026-08-31). If it does not, the
  instrument is not measuring what the plan claims.
  **Ownership**: an agent may run these as verification evidence. The
  **attestation that closes gate 3 of M is the operator's**, naming the adapter
  path and version — a human step, described as one, owned by the Maintainer or
  the adopter. If nobody can satisfy it, the issue does not close.
* **M** — issue #4 closes only when all five hold: (1) implementation landed
  and code-reviewed; (2) the implementation's **External Security code review**
  completed — *not* a proposal review; (3) the legs demonstrably run against a
  real adapter by G's predicate, with the operator's attestation recorded;
  (4) a closing comment naming what was **declined** — the bare `version`
  subcommand and why; that admission was deliberately **not** automated, so
  reduced mode remains the shipped posture; that the reporter's measured digest
  was **not** admitted, with the route by which it could be — and carrying the
  D3 correction (`--verify-version-support` exists; its second half did not
  work), **D4**, and **D5**, stating plainly that the ceremony was
  *un-performable*; (5) Maintainer authorization for the outward-facing act.
  **Falsifier**: the close is gated on verification, not on merge. If the issue
  can close with gate 3 unmet, the fence is not built.

### Security preflight — where chunking changes an answer

* **S2 — which chunk runs the mutation.** Each chunk's own **Falsifier** above
  is that chunk's mutation; each is run and its failure recorded in that chunk's
  commit body.
* **S3 — what fires the check, over what.** Only
  `python -m pytest bootstrap/tests/test_portable_security_sweeps.py`, run by a
  person typing it. **Cairn has no CI, no hook, and no gate selects this
  suite.** That suite drives a Python fake, not gitleaks — which is why all 163
  of its nodes pass today against a module that cannot run. The module doc
  describes operator-run commands (`portable-security-sweeps.md:181`, `:188`),
  not a test trigger, so there is nothing there to disagree with; the only
  trigger over a real adapter is chunk G, whose trigger is a human.
* **S1, S4, S5** are unchanged by the chunking and stand as Revision 4 states
  them. S5 in particular: **nothing bounds adapter execution over
  candidate-controlled file content; the class is open**, and D5 Part B removes
  the stderr relay for the pre-existing codes as well as the one Part A routes.

## Scope delta

**Scope delta**: preserved.

Every outcome the accepted Revision 4 and the Decision commit to is placed in a
chunk: D1→A, D2→B — **all four of its allowlist deltas, each with its own node
and its own mutation** after the plan review found three of the four unverified
— D3→F, D4→C, D5 (Parts A and B)→D, invariant (viii) and the per-candidate exit
contract→E, the two real-adapter instruments→G, the five-gate issue closure→M.
Nothing is dropped, and nothing is deferred — Revision 4's **Deferred: Nothing**
carries into this plan unchanged.

**One item was added, and it was allowed — scope grew, it did not narrow.**
Chunk F's correction of the ledger's stale `PATH` measurement was ruled added
scope by the plan review, put to the Maintainer, and authorized on 2026-08-31;
the authorization is quoted verbatim in F's acceptance criterion. It is recorded
separately here so a reader can see the growth came by allowance and not by
drift: no accepted outcome moved, shrank, or was traded to make room for it.

## Verification

**Boundary A (iteration, scoped) — the reviewed mapping.** Roman numerals are
the inline invariant list above.

| Changed surface / invariant | Mapped test node or file | Standing gates |
|---|---|---|
| A — the extractor; `parse_version` unmodified (invariant i); `fake_tool` default | `test_portable_security_sweeps.py` version-parsing and mode-selection nodes (`:478-524`) plus A's four new nodes, including the raw-banner field shape | twin identity (`:2300`, `test_notice_install.py:114`) |
| B — the inert fence; no leg before the screen returns (invariant ii) | the config-screen block (`test_portable_security_sweeps.py:1145-1423`) plus B's twelve nodes — one per allowlist delta | twin identity |
| C — `_leg_argv` and all three call sites; the emitted argv stays acceptable to the admitted adapter major (invariant v) | the argv/config-flag block (`:907-1145`), `:1186-1200`, the admission-ceremony nodes (`:1881-2266`) | twin identity |
| D — exit contract and `classify_leg` reasons (invariants vi, vii) | report/exit classification (`:1571-1806`), the child-document contract (`:1806-1881`), output-sink/redaction (`:1423-1571`) | twin identity |
| E — the admission matrix (invariant viii); `_ADMITTED_ARTIFACTS` untouched (invariant iii) | `:1977`, `:1993`, `:2005`, `:2135`, plus E's two nodes | `python scripts/check_cairn.py`; `python scripts/claim_check.py dev/measurement/gitleaks-version-support.md` |
| F — comments, module doc, ledger | `:2005`, plus F's node | `python scripts/check_cairn.py`; `python scripts/quality_gate.py --sub neutrality --sub redundancy`; `python scripts/claim_check.py` on each edited document |
| Twin, both sides, every chunk | `test_the_runner_twin_is_byte_identical_to_its_template_source` (`:2300`); `test_the_policy_twin_is_byte_identical_to_its_template_source` (`:2286`); `test_every_self_hosted_twin_carries_spdx_header` (`test_notice_install.py:105`) | — |

The whole file — all 163 nodes, `19.4s` on the canonical interpreter — is cheap
enough to run per chunk, so Boundary A is *the file*, not a node selection; the
table above is what a reviewer checks the file against, and what a failure is
diagnosed with.

**The pre-change baseline is not clean, and `check_cairn`'s figure is not
stable across lifecycle moves. Take your own baseline; do not chase a number
carried forward from here.** Measured on the canonical interpreter immediately
before the two 2026-08-31 plan-open commits, `scripts/check_cairn.py` reported
`6 issue(s) across 173 file(s)` — **four** stale `line-bounds` citations into
`dev/.cairn/cairn-lock.yml` and **two** broken markdown link targets, all six in
the sibling `scanner-claim-scope` proposal, which carries its own self-disposed
`## Correction`. That proposal archived at its own plan-open, and
`check_cairn` skips archived sources, so the six left the count without anything
being fixed. `scripts/quality_gate.py --sub neutrality` reported `fail=79`,
unchanged for months and unrelated to this surface.

The operative instruction, which no frozen figure can carry: **run both gates
on a clean tree immediately before the first implementation commit of this plan
and record what they say.** That measurement is the baseline. A figure that
moves against *it* is this change's; a figure that differs from the numbers
above may only mean an unrelated artifact archived in between.

**Boundary B (integration) — `**Boundary B mode**: full`, and bounded mode is
refused.** Two independent refusal triggers, either of which alone forces the
full suite: the change touches a **contract surface** (both runner paths are
frozen in `bootstrap/tests/fixtures/gate_manifest.json` and pinned in
`dev/.cairn/cairn-lock.yml`), and it touches a **trust-ceremony surface** (the
portable-sweep executable trust root `AGENTS.md` names, and the admission
ceremony itself). This is recorded here, at plan-open, so no later reader has
to re-derive it.

Run once after the final implementation commit, against a clean unchanged
commit under the canonical interpreter (Python 3.13.x):

```
CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0
python scripts/quality_gate.py --sub neutrality --sub redundancy
python scripts/check_cairn.py
python scripts/claim_check.py dev/plans/portable-sweeps-cannot-run.md
python scripts/claim_check.py dev/measurement/gitleaks-version-support.md
```

The last two are the write-time claim check `dev/plans/_template.md:168-169`
requires **once for each authored document** — this plan and the ledger both
change here, and if F's module-doc re-read turns into an edit,
`templates/modules/team-gated/portable-security-sweeps.md` joins the list. F's
per-chunk row below already runs it, but those runs go stale the moment a later
commit touches a document; the clean-tree pass is what catches that.

Append the evidence as
`## Implementation verification -- <agent> -- YYYY-MM-DD` with the tested SHA,
reviewed range, interpreter, clean pre/post state, the command table with
pass/fail/skip/xfail/xpass counts and timing, **the `claim_check` result per
edited document**, the disposition of every non-pass, the plan-specific
acceptance commands (chunk G's two real-adapter runs and their operator
attestation), and known omissions.

**Expected test-count movement, accounted rather than observed:** the file
carries 163 nodes today; A–F add **twenty-five new test names** — four, twelve,
three, three, two and one, by chunk — and re-point one
(`bootstrap/tests/test_portable_security_sweeps.py:1195`). The *collected* total
rises by more than twenty-five, because
`test_no_adapter_stderr_reaches_any_durable_sink` is parametrized over four
cases. Any node that
moves from passed to **skipped** is a defect until reconciled by name — a
passed→skipped transition leaves the collected total unchanged, so a
reconciliation watching only passes is blind to it.

**Known omissions to carry into the record** (Revision 4's, unchanged): the
extractor pins observed shapes only; not tested are Linux, Windows, a symlinked
Git common directory, a malicious adapter binary, a full-mode admitted digest,
or every legal exit an unknown future adapter might choose. The ceremony is
documented and, after C and D, *performable* — **it is not performed by this
change**, and no artifact is admitted.

**Boundary C (falsification, independent).** The code reviewer's, and it is not
re-running the Boundary B command. Verify the record against the reviewed range,
then attack the claims that would hurt most if wrong. Named targets, in order of
what a miss costs: **the canary** — construct a stderr shape the parametrization
did not cover and show it reaches no sink; **the twin** — diff both runner paths
byte-for-byte independently of the suite node that claims it; **the flag-table
fake** — confirm from the commit history that it landed red, because a fake that
was born green proves nothing; **the exit value `42`** — confirm against
`gitleaks --help` on the reviewer's own host rather than against this plan.
Since Boundary B is `full`, no `**Bounding**` field is owed.

**The code-review floor is the ordinary one — not the implementing agent — and
separate from the External Security code review M's gate 2 names.** Neither
substitutes for the other.

## Dispositions

`Dispositions: accept x2, guard x1, wontfix x2, defer x1 (authorized)`

* **accept** — D1 through D5 and the admission matrix, all delivered; the
  exit-table disclosure in both module-doc copies.
* **guard (`bootstrap/tests/test_portable_security_sweeps.py::test_the_adapters_real_redaction_shape_fails_validation`)**
  — reconciling the runner's whole-field redaction check with the shape the
  adapter actually emits is new scope and is not taken here. It is held by a
  node that fails if the real shape ever starts validating, so the gap cannot
  drift back into silence. Also recorded in
  `dev/measurement/gitleaks-version-support.md` under *Known gap*.
* **wontfix** — the uncovered branch at the matrix guard: unreachable by any
  current fixture, and reachable only by a candidate that misreports its own
  output.
* **wontfix** — a follow-up comment on the now-closed issue #4: a comment on a
  closed issue reaches nobody and is therefore not a control. The disclosure
  that does reach an adopter is in the installed module doc, and ships through
  the upgrade path.
* **defer** — the gate-manifest re-anchor for the frozen files this work
  touched. Maintainer authorization, quoted verbatim at `9960814`:

  > "If we don't need to re-anchor now, let's not. We've got a couple of big
  > new features coming, one of which will be a better automation."

  This is a hazard a green suite will not surface: `test_gate_manifest.py`
  verifies a freshly produced manifest and never diffs the committed fixture.

## Plan review -- Claude (Internal, fresh-context subagent) -- 2026-08-31

**Model**: claude-opus-5 (Claude Opus 5)
**Obligation**: Internal
**Tier**: Internal
**Findings**: raised -- 1 blocking, 3 notes, 1 nit
**Reviewed commit**: 2c218188bb0837f570526b42200addf0e08f7d4c
**Target**: the whole plan, header through Dispositions, checked against
`scripts/run_portable_security_sweeps.py` and its `templates/modules/team-gated/`
twin, `bootstrap/tests/test_portable_security_sweeps.py`,
`bootstrap/tests/test_notice_install.py`,
`templates/modules/team-gated/portable-security-sweeps.md`,
`dev/measurement/gitleaks-version-support.md`, `dev/plans/_template.md`, and the
accepted source proposal's Revision 4 and Decision.

The `required(**Internal**)` obligation is the plan header's whole plan-review
clause. This pass does **not** satisfy the External Security **code** review the
implementation carries (M's gate 2), and that instrument does not satisfy this
one.

### What I checked, and the controls

* **Absence claims, control-first** (`AGENTS.md` > "Confirm the instrument before
  trusting an absence"). Controls:
  `test_the_runner_twin_is_byte_identical_to_its_template_source` → 1 hit, and
  `repositoryformatversion` → 1 hit in *each* of runner and test file, so the
  grep reaches both corpora. Against that instrument all **21** new node names in
  A–F return **0** hits, and `_SCREEN_MAX_NAMED_KEYS` is free in source.
* **Collection**: `--collect-only -q` → **163 tests collected**, matching `:314`
  and `:362`; the `3+9+3+3+2+1 = 21` accounting is internally consistent.
  **Twin**: `diff -q` on both runner paths → identical.
* **Standing gates, my own baseline** (Python 3.13.13): `check_cairn.py` → **OK,
  0 issues / 173 files**; `quality_gate.py --sub neutrality` → **fail=79
  info=21**, matching `:328` exactly; `claim_check.py` on the plan → **OK**. The
  `check_cairn` 0-vs-6 gap is the movement the plan predicted and told
  implementers to re-measure rather than carry (`:319-335`) — the instruction
  held, and the drift is the sibling proposal's archival, not this change's.
* **Citations spot-checked by direct read**, not taken from the plan:
  `_EXIT_FINDINGS = 1` (`:829`), the ceremony guard (`:1434`),
  `f"--timeout={_ADAPTER_TIMEOUT}s"` (`:1628`), `_SCREEN_MAX_BYTES` (`:609`),
  both `_diagnostic(stderr)` branches (`:995-1003`), the `s`-suffix pin
  (`test_portable_security_sweeps.py:1194-1195`). All exact.
* **What I did not do**: re-argue the accepted design. I considered whether the
  surface obliges `required(Internal + Internal Security Review)` and stopped —
  the Decision ratifies `required(Internal)` as an accepted term (`:2477`), and
  the plan's S2/S3 section (`:271-287`) is the right instrument for "does
  chunking change a security answer." Challenging the tier would relitigate the
  Decision.

### Steelman

This plan is unusually well anchored, and most of what a plan review normally
catches is already closed:

* **The premise is reproduced, not asserted.** G's falsifier quotes the exact
  pre-change failure string (`:248-252`), and the ceremony guard, the `s`-suffix
  argv and both stderr relays are all where the plan says they are, to the line.
* **Instrument-before-absence is built into the plan.** Chunk C's flag-table fake
  must land **red in its own commit** with the failure quoted (`:161-172`). "A
  fake that has never failed is not an instrument" is exactly right, and making
  the red commit a deliverable rather than a courtesy is the correct shape.
* **The `42` value is measured, not chosen** (`:190-194`), and D's canary
  falsifier names every sink — `summarize()`, `render_report()`,
  `child_document()` — not only `LegOutcome.reason`, so invariant (vi) is stated
  over the whole exit space, the only form that can be falsified.
* **E's fixture decision documents the trap**: `AKIAIOSFODNN7EXAMPLE` is
  allowlisted by the default ruleset, so the obvious fixture would make a
  planted-finding row read as a passing clean scan (`:200-206`) — a silent-failure
  mode caught at plan time.
* **Boundary B is `full` on two independent grounds** (`:337-344`), both of which
  I confirmed: both runner paths are frozen in
  `bootstrap/tests/fixtures/gate_manifest.json` and pinned in
  `dev/.cairn/cairn-lock.yml`, and the surface is the executable trust root
  `AGENTS.md` names. Gate-manifest staleness is correctly *reported, not
  repaired* (`:92-100`), noting a green suite is no evidence the re-anchor is
  unowed. Boundary C is not pre-empted (`:380-389`).
* **Scope delta is `preserved` with every accepted outcome mapped** (`:289-297`).
  B1 is a defect in the *verification* of one mapping, not a drop — but it is why
  that claim does not yet hold.

### Finding B1 (blocking) -- three of D2's four accepted allowlist changes have no acceptance criterion, and B's own falsifier passes without them

**The accepted contract is explicit about the regexes.** Revision 1 states them
literally, restated unchanged in Revision 2
(`dev/proposals/archive/2026-08-20-claude-portable-sweeps-cannot-run.md:863-864`
and `:1262-1263`):

```
\Aremote\..+\.(url|fetch|pushurl|mirror|tagopt|glab-resolved)\Z
\Abranch\..+\.(remote|merge|rebase|vscode-merge-base)\Z
```

and the Decision's D2 term (`:2471`) reads "Permits `remote.<name>.glab-resolved`
and `branch.<name>.vscode-merge-base`". Against today's source
(`scripts/run_portable_security_sweeps.py:624-628`) that is **four** deltas: the
`branch` widening, the `remote` widening, `glab-resolved` joining the remote
alternation, and `vscode-merge-base` joining the branch alternation.

**Chunk B's nine nodes pin exactly one of the four.** `:149-157` names
`test_a_dotted_branch_subsection_is_inert` and
`test_a_slashed_branch_subsection_is_inert` — both `branch.*`. No node exercises
a dotted or slashed **remote** subsection, and no node names either new key. The
falsifier (`:158-160`) is "restore `[^.]+` at `:624-628` — the dotted and slashed
cases go red", which reddens only if the `branch` pattern was widened. **An
implementer who widens `branch` alone and adds neither key leaves all nine named
nodes green.**

**Verified absence, with the control above:** `glab-resolved` and
`vscode-merge-base` appear nowhere in the runner or the test file — their only
occurrences in the whole tree are three deliberation documents (this plan, the
source proposal, `dev/reviews/2026-08-20-adopter-issues-decision-support.md`).
And nothing else catches it: chunk G's instrument 1 builds a *fresh* repository
(`:235-243`) carrying neither key, and Boundary C's four named targets
(`:382-388`) are the canary, the twin, the flag-table fake and the exit value.

**C0 -- would shipping this cause damage that is hard to undo? YES.** D2 is the
adopter-facing half of the reported defect: a `glab` or VS Code user is precisely
the reporter's case, and a half-landed D2 still refuses their checkout with
`DEGRADED (20)` before any leg runs. Chunk M then closes public issue #4 on a
five-gate claim that the module works — undoing that means a reopened public
issue, a second failed adopter install, and a fresh cycle on a shipped module.
This is also a **deny-by-default security allowlist**, where an unpinned entry is
what a later refactor drops silently. The plan's own `Scope delta: preserved`
(`:291`) is what makes this blocking rather than cosmetic: it asserts a
preservation the acceptance criteria do not deliver, and `AGENTS.md`'s floor rule
puts accepted outcomes beyond a reviewer's or an implementer's discretion.

**Remedy — additive only; I am removing nothing.** In chunk B's acceptance
criterion (`:138-160`): add nodes pinning `remote.<name>.glab-resolved` and
`branch.<name>.vscode-merge-base` as INERT, and one dotted-or-slashed **remote**
subsection case; extend the falsifier so restoring `[^.]+` on **both** patterns
reddens named nodes on both. Then update the dependent accounting — B's node
count in the chunk row (`:73`), the Boundary A cell that reads "B's seven nodes"
(`:307`, already inconsistent with the nine listed at `:149-157`), and the
"twenty-one new test names / three, nine, three, three, two and one" figures at
`:362-365`.

### Note N1 -- Boundary B's command block omits `claim_check.py`, on a plan that edits two documents

`dev/plans/_template.md:168-169` lists "Write-time claim check — `python
scripts/claim_check.py <file>` once for each authored proposal, plan, or doc" in
the Boundary B command set. The plan's block (`:349-353`) runs pytest,
`quality_gate` and `check_cairn` — it went *beyond* `AGENTS.md`'s literal
two-command pair to add `check_cairn`, then left `claim_check` out, while two
documents are edited in scope and F's own Boundary A row already runs it
per-chunk (`:311`); the evidence-record fields (`:355-360`) do not ask for it
either. A final clean-tree pass is what catches drift F's own doc edits introduce
after the per-chunk runs go stale. **C0: NO** — a missing command, cheaply added,
with per-chunk coverage already in place. **Remedy**: add `python
scripts/claim_check.py <each edited document>` to the `:349-353` block and name
it in the evidence-record fields.

### Note N2 -- three of chunk F's four acceptance sub-clauses are attestations, not checks

F (`:212-219`) bundles four claims; only the first — the runner header comment —
carries a node (`test_the_runner_comment_references_no_uninstalled_path`) and a
falsifier. The module-doc re-read, the ledger's four-step re-read, and
"`AGENTS.md`'s portable-sweep paragraph is confirmed unchanged-needing" have no
node, command, or falsifier. For a *confirm-nothing-changed* claim that is
defensible, but the plan's own standard is "Per chunk, each falsifiable"
(`:127`), and it labels human-only steps explicitly everywhere else — G's
attestation is "a human step, described as one" (`:255`); S3 names "a person
typing it" (`:277`). Here it does not. **C0: NO** — descriptive layer only.
**Remedy**: label the three as attestations recorded in F's commit body, in the
same voice as `:255`, so a code reviewer knows what evidence to look for instead
of assuming a check exists.

### Note N3 -- chunk A leaves unpinned what the extractor puts in two externally-visible fields

`probe_version`'s raw return reaches `record["candidate_version"]`
(`scripts/run_portable_security_sweeps.py:1384`) and
`facts["adapter_version_output"]` (`:1740`) — both JSON-visible, and
`candidate_version` is a field of every evidence record the ledger will hold. The
only test touching either checks **presence, not shape**
(`bootstrap/tests/test_portable_security_sweeps.py:2045-2049`), and A's criterion
(`:129-134`) pins only what reaches `select_mode`. So whether these carry
`"gitleaks version 8.30.1"` or `"8.30.1"` after A is an unreviewed implementer
choice on a `--json` contract. **C0: NO** — nothing is admitted yet, so no
recorded evidence is invalidated, and a field shape is revertible. **Remedy**:
say which shape survives and pin it. Recommended: keep the **raw banner** — the
ledger's purpose is recording what the binary actually said.

### Nit -- B's accumulation says which branch stays first-failure, but not all of them

B's criterion names containment as staying immediate (`:142-143`).
`screen_local_config` has a *third* immediate raise the plan does not mention —
the non-file-origin check at `scripts/run_portable_security_sweeps.py:781-783` —
which sits before containment in the same loop. Harmless if the implementer
preserves it, silent if not. **C0: NO**. One clause in the chunk row naming both
first-failure branches closes it.

### Scope call -- the ledger's stale `PATH` measurement is added scope, and I cannot authorize it

The plan flags this itself (`:223-232`) and asks the reviewer to rule. **My
ruling: it is added scope.** The reasoning, and the part that decides it:

* *Touching the file is inside the contract.* The proposal's header names
  `dev/measurement/gitleaks-version-support.md` under **Touches** (`:15`), and
  chunk E already edits it under accepted scope (`:76`).
* *But D3's obligation is enumerated, not open-ended.* Revision 4 restates D3 as
  the un-performable ceremony, the comment correction, four steps, un-automated,
  no artifact admitted (`:2290-2292`); the Decision's D3 term (`:2473`) is
  "Documents manual four-step admission procedure; clarifies admission is
  un-automated." The proposal's *Documentation / doctrine surface* section
  (`:185-191`) names the module doc and two docstrings — not the ledger.
* *Decisively: the fact is newer than the Decision.* gitleaks appearing on this
  host's `PATH` was measured **2026-08-31**, eleven days after the **2026-08-20**
  Decision. An accepted contract cannot have decided a fact that did not exist
  when it was accepted — which is what separates this from D3's other
  corrections, every one of which was on the table during review.

**I am not narrowing anything.** A reviewer has no authority to remove accepted
scope and none to grant new scope, and calling this "out of scope" would be the
narrowing-by-review move `AGENTS.md` names outright. The correction stays in the
plan exactly as written; the plan's own fence (`:230`, "it needs the Maintainer's
word before it lands") is simply engaged by this ruling. Chunk F may land
everything else; that one line waits on an answer.

**Question for the Maintainer, one sentence:** *Chunk F wants to also fix one
sentence in `dev/measurement/gitleaks-version-support.md` that says gitleaks is
not installed on this machine — it now is — may it?*
**Recommended default: yes.** That sentence is the stated reason the module ships
in reduced mode, so leaving it wrong invites the next reader to conclude the
empty admitted set is an availability accident rather than the deliberate
Maintainer-supplied-binary control it is. The disposition does not change either
way — the set stays empty.

*Execution suggestion, not a condition*: the ledger's idiom is dated measurements
that get **superseded**, not overwritten (`as_of` stamps throughout; the
Retirement log's "with the reason and the date" convention at `:75-80`). A new
dated line beside the 2026-08-05 one keeps that idiom.

### Verdict

**REVISE.** One blocking finding: chunk B's acceptance criteria verify one of the
four allowlist changes the Decision accepted, and B's own falsifier stays green
without the other three — so the plan's `Scope delta: preserved` does not yet
hold for D2. The remedy is additive and small (three nodes plus the dependent
counts), and everything else in the plan is in unusually good order: I checked
the citations, the collection count, the twin, the standing-gate baselines and
the Boundary B `full` determination against the tree myself, and each held.

**Status → `revising-plan`.** Separately, chunk F's ledger `PATH` correction is
ruled **added scope** and waits on the Maintainer's word before that line lands;
the rest of F is unaffected, and no scope is removed by this pass.

## Response to plan review -- Claude (author) -- 2026-08-31

Every finding is folded **into the operative cell it belongs to**, in place, per
`dev/plans/_template.md:24-32`. This table points at those cells; it does not
restate them, because a second copy of a cell is a second answer to the same
question. The `## Plan review` section above is untouched.

| Finding | Disposition | Where it landed |
|---|---|---|
| **B1** (blocking) — three of D2's four allowlist deltas unpinned; B's falsifier green without them | **accepted** | *Acceptance criteria* > **B**: three added nodes (`test_a_dotted_remote_subsection_is_inert`, `test_the_glab_resolved_remote_key_is_inert`, `test_the_vscode_merge_base_branch_key_is_inert`), the criterion text now naming all four deltas, and the **Falsifier** replaced by four separate mutations that redden disjoint node sets. Dependent counts corrected: the *Sequence* chunk-B row, the Boundary A table's B cell (seven → **twelve**), and *Expected test-count movement* (twenty-one → **twenty-five**; `three, nine, …` → `four, twelve, …`). *Scope delta* now states the D2→B mapping as four-deltas-each-pinned. **One variation, disclosed**: the remedy said to fix "B's node count in the chunk row" — the row carried no count, but it did carry a one-delta description (*"Subsection widens"*, singular), which is corrected instead. |
| **N1** — Boundary B omits `claim_check.py` | **accepted** | *Verification* > Boundary B: two `claim_check` lines added to the command block (this plan, the ledger) with the module doc named conditionally, and **the `claim_check` result per edited document** added to the evidence-record fields. |
| **N2** — three of F's four sub-clauses are unlabelled attestations | **accepted** | *Acceptance criteria* > **F**: the three re-stated as **human attestations recorded in F's commit body**, in the same voice as G's operator attestation and S3's "a person typing it", with what a code reviewer should look for. The *Sequence* chunk-F row carries the same label. |
| **N3** — the extractor's two JSON-visible fields are unpinned | **accepted**, recommendation adopted | *Acceptance criteria* > **A**: a **Decision** clause pinning the **raw banner** (not the triple) into `record["candidate_version"]` and `facts["adapter_version_output"]`, a fourth node `test_the_evidence_record_keeps_the_raw_version_banner`, and a second mutation in A's falsifier. |
| **Nit** — B names containment but not the non-file-origin raise | **accepted** | Named in **both** cells the reviewer's remedy could mean: the *Sequence* chunk-B row and *Acceptance criteria* > **B**, each stating that **both** pre-scan raises stay first-failure. No node added — the remedy asked for a clause, and this is a preserve-unchanged claim, so the twelve-node count stands. |
| **Scope call** — the ledger `PATH` correction is added scope | **resolved: authorized, not absorbed** | Put to the Maintainer and allowed on 2026-08-31. The fence at *Acceptance criteria* > **F** is discharged and the authorization is **quoted verbatim in a blockquote in its place**; *Scope* and *Scope delta* record the growth as an allowance. The reviewer's execution suggestion — supersede the dated line, do not overwrite it — is adopted in F. |

**No finding is declined.** Scope delta stays **preserved** for every accepted
outcome; the one addition is recorded separately so growth-by-allowance is not
mistaken for drift.

**Status → `ready-to-implement`.**

## Implementation verification -- Claude (Implementation) -- 2026-08-31

**Boundary B mode**: full

Bounded mode was refused at plan-open on two independent grounds and both hold:
both runner paths are frozen in `bootstrap/tests/fixtures/gate_manifest.json`
and pinned in `dev/.cairn/cairn-lock.yml` (**contract surface**), and the change
edits the portable-sweep executable trust root and the admission ceremony
(**trust-ceremony surface**).

**Interpreter**: Python 3.13.13, the canonical 3.13.x.
**Reviewed range**: `d49059d..12a536f` -- seven commits, chunks A through F.
**Tested SHA**: `12a536f`, the final implementation commit.
**Clean pre/post state**: `git status --short` empty before the run and after
it; the run mutates nothing tracked.
**Twin**: both runner paths at sha256
`9bf5122ab77741e92c9ce44ffd8371459f0cc68ac732b68432223abb82dbad88`, verified
with `shasum` independently of the suite node that claims it.

### Commands and outcomes

| Command | Outcome | Timing |
|---|---|---|
| `CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0` | **3205 passed, 1 failed**, 0 skipped, 0 xfail, 0 xpass, 3 warnings | 569.01s |
| `python scripts/quality_gate.py --sub neutrality --sub redundancy` | `[neutrality] fail=79 info=21`; `[redundancy] fail=0 info=0`; exit 0 | under 5s |
| `python scripts/check_cairn.py` | `3 issue(s) across 173 file(s)`; 29 external links not probed | under 5s |
| `python scripts/claim_check.py dev/plans/portable-sweeps-cannot-run.md` | **OK, no claim-check flags** | under 5s |
| `python scripts/claim_check.py dev/measurement/gitleaks-version-support.md` | **OK, no claim-check flags** | under 5s |

The module doc `templates/modules/team-gated/portable-security-sweeps.md` was
re-read in chunk F and **not edited**, so it does not join the `claim_check`
list.

### Disposition of every non-pass

* **`test_cairns_own_install_records_all_three_files_in_the_lockfile` -- FAILED,
  expected, not repaired.** It hashes `scripts/run_portable_security_sweeps.py`
  on disk against `dev/.cairn/cairn-lock.yml:414-419`, which still carries the
  pre-change `sha256:3c2ebff3...`. The lockfile is tool-owned and
  regenerate-only; the re-anchor is the Maintainer's.

  **This contradicts one sentence in this plan** (*Fences and mechanical
  consequences*), which says gate-manifest and lockfile staleness means
  "nothing goes red". That is true of the gate manifest and **false of the
  lockfile** -- this node reddened on the first chunk and stayed red through all
  seven commits. The plan was implemented as written (report, do not repair);
  the inaccuracy is recorded rather than worked around.
* **Baselines, measured on a clean tree immediately before chunk A** and
  unchanged by this work: `check_cairn` `3 issue(s) across 173 file(s)` -- all
  three are stale `dev/measurement/` path citations in
  `dev/reviews/2026-08-27-code-review-c5-c6-removals.md`, unrelated to this
  surface; `quality_gate --sub neutrality` `fail=79 info=21`; `--sub redundancy`
  `fail=0`. Every post-change figure matches its own baseline exactly. (The
  plan's frozen `6 issue(s)` figure did not survive, exactly as it warned.)
* **0 skipped, 0 xfail, 0 xpass** in the full run, so no passed-to-skipped
  transition can hide behind an unchanged collected total.

### Test-count movement, reconciled

`bootstrap/tests/test_portable_security_sweeps.py` carried **163** collected
nodes and **100** `def test_` names at `d49059d`; it now carries **191**
collected and **125** names. That is **25 new test names** -- four (A), twelve
(B), three (C), three (D), two (E), one (F), exactly the plan's accounting --
and **+28 collected**, because
`test_no_adapter_stderr_reaches_any_durable_sink` is parametrized over four
cases. One node was re-pointed as the plan directs
(`test_the_gitleaks_timeout_is_strictly_inside_the_outer_deadline`, off the
suffixed `--timeout` string it had been locking in).

### Chunk G -- the two real-adapter instruments

Run against **gitleaks 8.30.1** at `/opt/homebrew/bin/gitleaks`, resolved to
`/opt/homebrew/Cellar/gitleaks/8.30.1/bin/gitleaks`, sha256
`f414bc2fb952be6c9072b75cb411e3368614ef4b16d48dbd9ad238034afd2302`. Git 2.53.0,
darwin/arm64.

**Instrument 1 -- the reduced-mode sweep. Predicate met.** Against a fresh
repository carrying one commit whose identity came from `GIT_AUTHOR_*` /
`GIT_COMMITTER_*` in the environment: `result: 5`, `mode: "reduced"`,
current-tree leg **INCOMPLETE** with the reason *"no finding, but the adapter
version is not admitted on this platform"* -- so the leg **ran** -- history leg
INCOMPLETE (Git is unreachable from the reduced child), and **no leg with status
DEGRADED**.

**Instrument 1's falsifier, run at the pre-A commit `d49059d`** against the same
repository: `result: 5`, `status: INCOMPLETE`, reason verbatim
`adapter version 'gitleaks version 8.30.1' is not an exact X.Y.Z; the version is
unmeasured, so no scan leg was run` -- the exact string this plan predicted. The
instrument measures what the plan claims.

**The documented trap, reproduced.** The same repository built the ordinary way
(`git config user.email` / `user.name`) returns `result: 20`, DEGRADED, before
any leg: `repository-local configuration key(s) ['user.email', 'user.name'] are
not on the reviewed inert allowlist`. That is correct -- `user.*` is not an
inert family and chunk B did not widen it -- and the refusal now names **both**
keys in one message, which is chunk B's accumulation visible on a real tree.

**Instrument 2 -- the admission ceremony. Predicate met; the ceremony does not
complete.** `--verify-version-support /opt/homebrew/bin/gitleaks
--confirm-executing-an-unadmitted-binary` reaches a **real matrix result**: the
record carries `end_to_end` rows, the `current-tree` `clean` row measured
end-to-end against the real adapter (`exit 0`, report validated, zero findings),
and `candidate_version_key: "8.30.1"`. It does **not** refuse on argv, which is
what the predicate asks. For contrast, the same command at `d49059d` returns
`end_to_end: null` and the refusal *"the adapter wrote no report"* -- the true
statement about a false cause D3 named.

The record then refuses at the `planted_finding` row with `admit: false`, on the
runner's own redaction control; see the finding below. **Nothing was admitted;
`_ADMITTED_ARTIFACTS` is untouched and still empty.**

**Gate 3's attestation is NOT closed by this record.** The plan assigns that
attestation to the Maintainer or the adopter as a human step. The runs above are
verification evidence produced by an agent, against a binary found on `PATH`
that is neither Maintainer-supplied nor checksum-verified.

### A defect chunk E surfaced, recorded and not fixed

Measured 2026-08-31 on real 8.30.1 darwin/arm64: `--redact=100` empties `Secret`
to `REDACTED` but renders `Match` as `api_key = "REDACTED"` -- the redacted
secret **inside its surrounding context**. The runner's `_MUST_BE_REDACTED`
check requires the whole field to be `REDACTED` or asterisks, so **no real
finding from this adapter can pass it**: the matrix's planted row refuses, and
an ordinary sweep would report DEGRADED rather than FINDINGS on a real secret.

This is a **pre-existing runner control**, not something this change introduced
-- and it was invisible until chunk E made the matrix measure a real finding,
which is precisely what invariant (viii) exists for. Reconciling the check with
what the adapter emits is **new scope**; it is recorded in
`dev/measurement/gitleaks-version-support.md` under *Known gap* and left for a
decision.

### Frozen and pinned files touched -- reported, not repaired

The re-anchor is the Maintainer's, per `bootstrap/REANCHOR_RUNBOOK.md`.

| File | Where pinned | Recorded | On disk now |
|---|---|---|---|
| `scripts/run_portable_security_sweeps.py` | `gate_manifest.json:4950-4954` | `3c2ebff3...` | `9bf5122a...` |
| `templates/modules/team-gated/run_portable_security_sweeps.py` | `gate_manifest.json:5135-5139` | `3c2ebff3...` | `9bf5122a...` |
| `bootstrap/tests/test_portable_security_sweeps.py` | `gate_manifest.json:4610-4614` | `e5ce3500...` | `1b16651a...` |
| `scripts/run_portable_security_sweeps.py` | `dev/.cairn/cairn-lock.yml:414-419` | `3c2ebff3...` | `9bf5122a...` |

The manifest's `collection` list also enumerates this test file's node ids and
does not yet carry the 25 new names. **The plan named two stale entries; there
are four**, because the test file is frozen too -- and only the lockfile one
reddens.

### Deviations and disclosed implementation choices

Every accepted outcome is delivered; nothing was dropped. Five choices a code
reviewer should see:

1. **`record["candidate_version_key"]` is a new field in the evidence record.**
   The *Sequence* row for A requires the extractor to be "reached by both probe
   call sites", and N3's Decision requires the **raw banner** in the two
   JSON-visible fields -- which implies the extractor's output at the ceremony
   site lands somewhere else. It carries the version component of the
   `(version, platform, architecture)` key a reviewed source change would type;
   without it, after A the ceremony's record names a banner that is not the key
   `select_mode` matches.
2. **Two exit fixtures re-pointed beyond the one the plan counts.**
   `test_an_undocumented_exit_code_is_degraded` and one
   `test_reduced_mode_never_emits_clean` case used `42` as an *undocumented*
   code; `42` is now the pinned findings exit, so both move to `126` -- what
   real 8.30.1 exits on an unknown flag. Ten findings fixtures move from
   `scan_rc=1` to `42` for the same reason.
3. **Chunk F also corrected a second uninstalled path in the same comment
   block** -- `templates/modules/team-gated/run_security_audit.py`, corrected to
   the destination `python-security` installs its orchestrator at,
   `scripts/`+`run_security_audit.py` (**an adopter-side path, deliberately not
   written as one citation**: Cairn has not adopted that module, so it does not
   resolve in this tree). F's criterion is "references **no** path the
   `team-gated` module does not install", so the node would have flagged the
   original.
4. **`end_to_end` is published as it fills**, not assigned once at the end, so a
   refusing record still shows which rows were measured. E's own criterion --
   "a matrix missing any row refuses with `admit: false`" -- presupposes a
   record that can be missing a row.
5. **The fake adapter now scans its target** for the planted `generic-api-key`
   shape and exits the runner-owned `--exit-code` on a hit. A fake that reports
   the same findings whatever it is pointed at cannot measure a findings row.

**Chunk M was NOT executed.** It is MAINTAINER-GATED and closes public issue #4;
no authorization exists, nothing was posted, and `gh` was never run.

### Known omissions, carried unchanged

The extractor pins observed shapes only. Not tested: Linux, Windows, a symlinked
Git common directory, a malicious adapter binary, a full-mode admitted digest,
or every legal exit an unknown future adapter might choose. The ceremony is
documented and, after C and D, *reaches a real matrix result* -- **it is not
performed to completion by this change** (see the redaction finding above), and
**no artifact is admitted**.

Two omissions this implementation adds:

* The **flag table** in the test fake is transcribed by hand from
  `gitleaks dir --help` and `gitleaks git --help` on 8.30.1 darwin/arm64. It is
  an instrument, not a contract: a future adapter's `--help` will not update it.
* The **planted-finding fixture** depends on the default ruleset's
  `generic-api-key` rule and on `--redact=100` behaviour, both measured on
  8.30.1 only.

## Code review -- Claude (Code Review, independent context) -- 2026-09-01

Reviewed range: `d49059d..12a536f` (chunks A-F), plus the post-merge `9960814`, which touches
`dev/.cairn/cairn-lock.yml` only. Target: the runner and its `templates/modules/team-gated/` twin,
`test_portable_security_sweeps.py` and `gitleaks-version-support.md`, against this plan's Scope,
Sequence, criteria and verification record. The plan review's blocking B1 landed in full.

**Stance**: External. **Floor**: not the implementing agent. **Independence, stated honestly**:
fresh-context, **same agent type** as the author -- no cross-type or human distance was staffed.
**Model**: claude-opus-5
**Findings**: raised -- 2 blocking, 2 notes, 2 nits
**Chunk M**: done -- issues #4, #5, #6 closed 2026-09-01 on Maintainer authorization, after the
record above was written, which is why it still says "NOT executed". The gate-manifest re-anchor
for 10 frozen files is **deferred by the Maintainer, not forgotten** (`9960814` quotes it).

### Was it built this way, and should it have been

**Yes, with one reservation.** The load-bearing decision is `_EXIT_FINDINGS = 42`
(`scripts/run_portable_security_sweeps.py:913`) sent as `--exit-code` (`:1840`). It inverts a
dependency: the runner stops *decoding* the adapter's exit vocabulary and starts *imposing*
one. Right call -- that vocabulary is provably ambiguous (`1` is both findings and a
`--timeout` usage error) and no decoder separates them. The cost is a new hard dependency on
the candidate honouring `--exit-code`, and E pays it in the right place: measured per
candidate, refused if unmet (`:1650`). `extract_version` being **total** -- input returned unchanged
on non-match rather than raising or returning `None` (`:310-327`) -- is right too: `parse_version`
stays the single arbiter and invariant (i) survives unchanged. The out-of-scope assertion holds on
a read of the diff: `resolve_executable`, all six `revalidate` sites, `child_env`, the policy
schema, `_AGG_*` precedence and `_ADMITTED_ARTIFACTS` are byte-unchanged; both twins are at
`9bf5122a...` with textually equal chunk diffs, checked outside the suite node.

**The strongest rejected alternative, which the plan never engages: send no `--exit-code`;
discriminate findings from usage error by the report file.** The runner owns `--report-path`,
already unlinks it per row (`:1585`), and `read_report` already raises *"the adapter wrote no
report"*. A usage error writes none; a findings run writes one. `_EXIT_FINDINGS` stays `1`, no
new flag is sent, E's `invalid_argv` row is unnecessary, and **nothing depends on the candidate
honouring a flag** -- strictly less trust in the binary, the direction this surface's doctrine
pushes. It loses on soundness: an adapter can write a report *and* exit on a usage error, and a
truncated report from a killed adapter is indistinguishable from a clean one, whereas the exit
code is the one channel the candidate *tree* cannot steer. The design wins; the alternative
still deserved a line.

**What would falsify it.** One observation: `--verify-version-support` against real 8.30.1 in
which the **`history`/`git`** leg rejects or ignores `--exit-code` -- exiting `1` on findings, or
`126` on an unknown flag. The record shows the real-adapter matrix stopping at
`current-tree`/`planted_finding`: **no `history` row, and no findings row on either leg, has ever
been measured against a real adapter.** If that row comes back wrong, the `--exit-code` dependency
is unsound for half the module and D5 needs the report-file discriminator above. Close B1/B2,
re-run instrument 2: that single observation withdraws this verdict.

### Findings

**B1. BLOCKING -- the planted-finding instrument emits a `Match` shape the real adapter does
not emit, so the findings path is green in the suite and refused in reality.**
`_planted_finding` returns `"Match": "REDACTED"` at line 250 of
`bootstrap/tests/test_portable_security_sweeps.py`; the pre-existing `_finding` helper at
`:1950` does the same. The implementation *measured* what real 8.30.1 emits under
`--redact=100` -- `Match` comes back as `api_key = "REDACTED"`, the secret inside its context
(`dev/measurement/gitleaks-version-support.md:85-95`). `_redaction_is_intact`
(`scripts/run_portable_security_sweeps.py:918-927`) requires the **whole** field to match
`\A(REDACTED|\*+)\Z`, so the real shape raises at `:987-991` and **no real finding from this
adapter can pass**. Both E nodes therefore assert a measurable findings row against a fixture that
misreports the adapter -- the defect class D1 existed to kill, named in this file's own `fake_tool`
docstring: *a fixture emitting a shape the adapter never emits is how a module that cannot run
keeps a green suite* (`:287-288`).

*Polarity -- blocking*: the runtime failure is loud (DEGRADED, not a missed secret), but the
**evidence** failure is silent and durable. The next agent touching redaction validates against
the wrong shape and reads a green suite as proof the findings path works -- the
false-durable-record hazard `AGENTS.md` reserves full weight for here. *Remedy*: a node pinning
the *measured* shape (`runner._redaction_is_intact('api_key = "REDACTED"')`) marked
`pytest.mark.xfail(strict=True)` citing the ledger's Known gap, disposed in the next record.

**B2. BLOCKING -- the installed module doc states an exit-`10` FINDINGS outcome the
implementation's own measurement contradicts, and never names the gap.**
`templates/modules/team-gated/portable-security-sweeps.md:107` tells an adopter `10 | FINDINGS
— at least one validated finding`. After B1, against the only adapter anyone has measured, a
real finding yields `20` DEGRADED, reason *"carries an unredacted 'Match'"*. That doc is unedited
in this range (four files in the diffstat, not it), and the gap lives only in `dev/measurement/`
and this plan -- **neither installed by the `team-gated` module**, as the runner's own new comment
says (`scripts/run_portable_security_sweeps.py:88-94`). F's attestation was honest: the doc needed
no edit *when F's criterion was written*; E surfaced the fact that changes the answer, later.

*Polarity -- blocking*: an outward-facing claim in an installed artifact, now known false, on a
security module whose issue was closed 2026-09-01 as resolved -- an adopter hits DEGRADED on a
real secret with nothing explaining it. *Remedy*: one paragraph near that exit table naming the
gap, the DEGRADED outcome and that it is under decision, plus a follow-up comment on the closed
#4. Neither is new feature scope -- both disclose a limitation the implementation recorded.

**N1. Note -- chunk E's falsifier claim names two nodes; one reddens, and the second passes
because the mutation reproduces the state it asserts.** `63b3027`'s body says *"drop the
planted-finding scenario -- the two E nodes fail"*. Dropping `("planted_finding", planted)` from
the loop (`:1567`) leaves `absent = ["planted_finding"]` (`:1650`), which refuses with `admit:
false`, a refusal naming `planted_finding`, and `rows` carrying `clean` but not
`planted_finding` -- *exactly* what the node at
`bootstrap/tests/test_portable_security_sweeps.py:2693-2711` asserts, so it stays green;
`test_the_evidence_record_carries_a_measured_exit_row_per_subcommand` reddens on `:2685`.
**Judgement on the disclosed item: evidence-record imprecision, not a hole in what the nodes
pin** -- node 2's named property genuinely holds under that mutation; the verifier is right.
Alongside it one real coverage gap: `if scenario == "planted_finding" and not findings` (`:1637`)
is unreachable by any current fixture, because `blind_to_planted=True` exits `0` (`:323-325`) and
is caught by the exit-mismatch check at `:1631`. *Remedy*: correct the falsifier line in this
record, and add a `blind_to_planted=True, scan_rc=42` fixture.

**N2. Note -- the `absent` check is a source-drift guard, not a runtime one, and the ledger reads
as if it were the latter.** `MATRIX_SCENARIOS` (`:1289`) and the loop's inline tuple (`:1567`) are
two literals in one function; every path either returns or writes its row, so at runtime `rows` is
never short one. The check fires only if a future edit moves one literal and not the other -- a
legitimate guard, but *"A record missing any row does not admit"*
(`gitleaks-version-support.md:74`) invites reading it as runtime behaviour. *Remedy*: one clause at
`:1650` saying what it actually guards.

**Nit 1** -- `test_no_adapter_stderr_reaches_any_durable_sink`'s docstring says the invariant is
stated "over the **whole** exit space"; it drives `classify_leg` only. Two `_diagnostic()` relays
survive at `:783` and `:1068` -- both **git** stderr, not the adapter's, so invariant (vi) holds
exactly as worded; add "adapter" to the docstring. **Nit 2** -- `_SCREEN_MAX_NAMED_KEYS`'s comment
(`:653-659`) says it stops the refusal's *size* being candidate-steerable; it bounds the *count* of
names, and the size bound is `_SCREEN_MAX_BYTES` (`:836`), unchanged here. Say "count".

### The verification record, judged

**It holds.** `3205 passed, 1 failed`, the failure disposed as the stale `cairn-lock.yml` hash,
is accurate; `9960814` reconciled it post-merge with a diff of one `hash` line, so **no
implementation, test, executable-template or fixture bytes moved** -- the Boundary B record is
not invalidated and no fresh full run is owed. `Boundary B mode: full` is correct and
over-determined (contract *and* trust-ceremony surface), so no `**Bounding**` field is owed. The
count reconciliation (163→191 collected, 100→125 names, +28 from one 4-way parametrize) matches
the chunk accounting; `0 skipped, 0 xfail, 0 xpass` is the right thing to have recorded, and its own
disclosure that the plan's "nothing goes red" sentence was false of the lockfile, and that four
frozen entries are stale rather than two, is what makes the rest credible. **One figure I would not
lean on**: chunk G instrument 2's "predicate met" -- as
written (*reach a real matrix result rather than refusing on argv*) it is genuinely met, but it is
one row of six on one leg: evidence the ceremony is *reachable*, not that the contract is measured.

**Scope**: preserved both directions. Every accepted outcome is delivered; the one addition (F's
ledger correction) carries its verbatim authorization. The five disclosed choices sit inside what
the plan authorised -- `candidate_version_key` is additive to a record outside the install
contract, the exit-fixture re-pointing follows from `_EXIT_FINDINGS`, and F's second uninstalled
path would have tripped F's own node. `import secrets` is stdlib.

### Verdict

**REVISE.** Two blocking findings, one discovered fact between them, both with small remedies:
the findings-path instrument encodes a shape the adapter does not emit (B1), and the installed
module doc asserts an outcome that fact contradicts (B2). Nothing in the runner's logic is wrong
and the five accepted defects are each genuinely fixed -- the module that could not run now runs,
up to INCOMPLETE. It cannot yet report FINDINGS against a real adapter, and neither the suite nor
the adopter's documentation says so.

**Status → `revising-code`.**

## Response to code review -- Claude (author) -- 2026-09-01

One loop: this revision closes the review (`doctrine/dual-review.md`). Landed at
`aab059e`.

| Finding | Disposition | Where |
|---|---|---|
| **B1** planted fixture emits a shape no adapter produces | **accepted** | `_planted_finding` now emits the adapter's real `Match`; `test_the_adapters_real_redaction_shape_fails_validation` pins the consequence; nine nodes measuring other properties opt into the idealized shape via `ideal_redaction=True` rather than inheriting it |
| **B2** installed doc says a finding yields `10` | **accepted in part** — the doc half delivered; the reviewer's second half, a follow-up comment on the closed #4, is **wontfix**: a comment on a closed issue reaches nobody, so it is not a control (`AGENTS.md`, "a named hazard with no enforcing trigger is not a control"). The installed doc is what reaches an adopter, and it ships through the upgrade path. | disclosure at the exit table in both module-doc copies, stating the finding is still reported and `20` is the fail-closed direction |
| **N1** chunk E's falsifier reddens one node, not two | **accepted as stated** — evidence-record imprecision, not a gap in what the nodes pin; the reviewer's reasoning is recorded and the claim is not repeated | this section |
| **N1b** an uncovered branch at the matrix guard | **wontfix** — unreachable by any current fixture and reachable only by a candidate that lies about its own output; the redaction node now covers the neighbouring path | — |
| nits | **accepted** where they cost a line; otherwise recorded here | — |

**The lasting one.** The fix for D1 contained D1: a fake emitting a shape the
real tool never emits, with green tests over it. The guard is not vigilance —
it is that a fixture's default is now the observed shape, and departing from it
takes an explicit, named argument at the call site.

## Archive -- 2026-09-01

`Dispositions: accept x2, guard x1, wontfix x2, defer x1 (authorized)` — see
*Dispositions* above.

Closed the loop it opened: adopter issue #4, filed 2026-08-20, closed
2026-09-01 on Maintainer authorization. Chunks A–F landed; M executed.

**The lasting truth, worth more than the fix.** The defect this plan repaired
was a fake adapter emitting a version string the real tool never produces, so
the suite stayed green while no scan leg could run. The repair introduced a
planted-finding fixture emitting a *redaction* shape the real tool never
produces — green tests, same file, same class, caught only by code review.
A fixture's default is now the observed shape, and departing from it costs an
explicit argument at the call site.
