# Build `repin`: one tested tool for the routine re-pins, replacing the blocked runner

**Author**: Claude (Strategy)
**Status**: revising
**Review**: usual + Security Review
**Plan review**: required(Internal + Internal Security Review) — the plan edits what the Maintainer's re-anchor trusts and writes into the tree, so its plan review needs the Security pass too
**Opened**: 2026-10-26
**In brief**: Build one committed, tested tool that does the arithmetic of Cairn's routine checksum corrections (the AST baseline, the gate manifest, the lockfile), so the Maintainer reads one short report and types one code instead of running commands an agent wrote that day.

*Authoring tier.* I wrote this at the medium tier, although doctrine sets proposal authoring at high. The reason is the Maintainer's direction, "Go ahead and spawn the lowest-tier agents you can to design, review, and implement proposals toward 0.5", and it applies to this proposal only. The Security Review stays at the high tier.

## In plain terms

**What changes.** Today a re-pin means the Maintainer pastes commands that an agent composed, then types back a number. The Maintainer called this "really just me doing what you tell me to do" (`dev/strategy/2026-08-05-codex-security-strategy.md:1194-1200`). After this build, one committed tool, `repin`, computes what changed, shows it in one screen, and writes the new pin only after the Maintainer types a short code from that screen.

**What the Maintainer does.** Three acts, no key for the routine pins:

1. Read the report and answer one question: does this describe what I meant to bless?
2. Type the 12-character code printed under the report.
3. Commit the files the tool names (or tell the agent to).

An optional fourth act is the real "compare two checksums": ask a fresh agent to run `package` in a clean checkout of the same commit and compare its code with yours.

**Why not just "compare two checksums".** On one machine, a person running `shasum` and a program running `shasum` are the same act by the same user, so the comparison cannot fail in a way that matters. A replay in a clean checkout can fail, because it does not share the working tree. I explain this under Proposal.

**What it costs.** About one tool and its tests, built in five small steps. I have no measure of the code size yet. The Maintainer's go-ahead is on record: "Repin is a build" (`dev/PLANNING.md:45`). The standing direction that a new tool needs its own go-ahead (`dev/PLANNING.md:16-17`) is met by that quote.

**What breaks if I am wrong.** A flaw in this tool could bless a change the Maintainer did not intend. That is why the header declares a Security Review. The fallback if the tool grows too large is to keep only the read-only report (chunk R1) and do the writes by hand, as today.

## Context

**What exists, checked against the tree on the `0.5-dev` base.**

* `scripts/correct_pinned_digests.py` refuses on entry (`scripts/correct_pinned_digests.py:345-347`). An outside security review blocked it with seven findings, two critical: `--authorize` lets any process do the human act, and the plan digest bound only a projection of the plan, so two different trees digested the same (header at `scripts/correct_pinned_digests.py:32-60`). Its 177-line test file still passes the acknowledgement flag to reach the machinery (`bootstrap/tests/test_correct_pinned_digests.py:1-20`).
* Pins are still moved by hand. I counted from `git log --since=2026-08-28 -- <fixture>`: six commits to `bootstrap/tests/fixtures/scaffold_ast_baseline.json` and two to `bootstrap/tests/fixtures/gate_manifest.json`. The AST re-anchors are the frequent case.
* `bootstrap/AST_BASELINE_RUNBOOK.md` is four steps, 194 lines. It says a multi-symbol correction is "Maintainer-run" (`AGENTS.md:521-528`), so the Maintainer runs a procedure written for a specialist.
* The gate manifest still goes stale silently when a frozen file changes after it is committed. Only `python bootstrap/tests/_gate_manifest.py verify` compares the tree with the committed fixture, and nothing runs it unprompted (`AGENTS.md:530-541`).
* The key ceremony has a driver, `scripts/reanchor_ceremony.py` (774 lines). I found no test that mentions it (a grep of `bootstrap/tests/*.py` returned nothing; the instrument can match, since the same grep finds `reanchor.sh` in `bootstrap/tests/test_reanchor.py`).
* The authority closure, the files that decide what the next anchor ceremony runs, has ten members (`bootstrap/tests/_gate_preflight.py:600-626`; I ran `declared_authority_closure()`). The launcher template `bootstrap/reanchor-launcher.template.sh` is not one of them.

**What the 2026-08-28 note says that is now stale.**

* It says the ceremony driver `reanchor_drive.py` "was not yet landed". It landed as `scripts/reanchor_ceremony.py`, a read-mostly driver for the key ceremony only. It does not touch the three routine pins.
* It says a diff of 365 commits is "unreadable". Since the last gate-manifest pin (`6f29519d`) there are 40 commits on `0.5-dev`, and 5 of them touch a protected path (counted with `git log 6f29519d..HEAD`). The size problem is smaller when pins happen at each release.
* Its review rules (an External floor at the proposal, Codex as the natural seat) predate the current doctrine. A called read is the Maintainer's alone (`AGENTS.md`, section "Review"). I do not request one.
* Its "sign the whole tracked tree" and "dedicated ceremony key" design belongs to the anchor tier. The routine pins have no key and no ref move, so I drop that part here (see "What is not carried").
* Its claim that unreviewed changes "refuse" does not survive measurement (see Proposal, provenance).

**Still true, re-verified:** the 19-step registry (`sh bootstrap/reanchor.sh steps`; `bootstrap/reanchor.sh:776-830`); RA-14 as the one judgment (`bootstrap/REANCHOR_RUNBOOK.md:157`); the REL-1 finding (`dev/strategy/2026-08-05-codex-security-strategy.md:1194`); the gate manifest's frozen set is a glob over `bootstrap/tests`, `bootstrap/*.py`, `scripts/*.py` and `templates/modules` (`bootstrap/tests/_gate_manifest.py:353-355`).

## Proposal

**One loop, built once.** A protected set of files changes only through reviewed work. A pin records its state. Drift builds up. A Maintainer approval moves the pin. `repin` does the whole loop for three pins, with typed adapters, one per pin, because their rules differ.

**Three verbs.**

* `status` reads and writes nothing. It prints, per changed protected file: what changed (the existing class names, for example the AST `CHANGED`, `NEW`, `REKEYED`, `DROPPED` and the manifest's `FROZEN-MODIFIED`, `FROZEN-MISSING`, `COLLECTION-DROPPED`); the commits from file history since the last pin; and any lifecycle artifact those commits name.
* `package` computes the full transaction once and writes it to a directory outside the repository. It prints the report and the code.
* `apply` takes that transaction file and the typed code, writes the pinned files, and prints the exact `git commit <paths>` line. It does not commit and does not push.

**Example report (shape only).**

```
repin AST baseline  base 6f29519d  head <commit>
  CHANGED  _MODULE_MAPPINGS        bootstrap/_scaffold/config.py   decides
  NEW      install_report_rows     bootstrap/_scaffold/upgrade.py  decides
  REKEYED  0   DROPPED 0   MISSING 0   DUPLICATE 0
  commits: 3 touch these files; 2 name a plan or proposal; 1 names none
  NOT SHOWN AS REVIEWED: 1 commit names no plan or proposal (listed above)
Does this describe what you intend to bless?   Type: 3f9a0c1d77ab
```

**The transaction object (what "complete" means).** One JSON file, bound by a SHA-256 of its whole bytes, holding every input and every output byte:

* the head commit and its tree id;
* the blob id and SHA-256 of each file `apply` will overwrite (the preimage);
* every influence that is not in the tracked tree, named in the file: the interpreter's version, the git version, the environment the pytest collection runs under;
* the full new contents of each output file.

`apply` reads this file, checks the typed code against its digest, checks each preimage still matches the file on disk (compare-and-swap: refuse if the file changed), and writes from the file's own bytes. It re-derives nothing. This closes the blocked runner's projection defect by construction, because the digest covers the output bytes themselves, not a summary.

**Safe writes.** Temporary file in the same directory, `os.replace`, read back and compared. Refuse a symlink or a path that resolves outside the repository, reusing the engine's containment idea (`bootstrap/_scaffold/_guard.py:49`), not a copy of it.

**Reuse, so nothing is re-implemented.** The AST adapter calls `_ast_attest._merge_current` and `_ast_attest._classify` (`bootstrap/tests/_ast_attest.py:117`, `bootstrap/tests/_ast_attest.py:166`), as the runbook requires ("never a reimplementation"). The manifest adapter calls `_gate_manifest.produce` and imports `_frozen_files` (`bootstrap/tests/_gate_manifest.py:339`) instead of copying the glob, so the rule that says what is protected has one owner, and it is already in the authority closure. The lockfile adapter lifts the plan logic from the old runner (`scripts/correct_pinned_digests.py:239`) under the same transaction format.

**What each check refuses.** The tool refuses, with a reason and no write, on: a dirty tracked file in the protected set; any git error; a declared set with zero members (each such check carries a control test showing it can refuse); an interpreter whose minor version is not the pinned one (the existing tools already hold on this); a failed pytest collection; a preimage that changed; a non-interactive `apply`; and a transaction whose changes include an authority-closure member (see Questions, Q3).

**The typed code: what it is and is not.** It is a confirmation and intent record. It is not authentication. Under one operating-system user, a tool cannot tell a person from a program that opened a pseudo-terminal. So the tool says so in its own text, has no `--authorize` flag and no non-interactive path, and the claim I make is only that an accident or a pipe cannot supply the code. Who else could supply it is the existing same-user residual under the dated trusted-contributor posture (`bootstrap/REANCHOR_RUNBOOK.md:339`). The commit body records the code, the transaction digest and the report, so the next reviewer can replay.

**Provenance, measured, and why it does not refuse.** I measured how well "which commit is covered by a reviewed artifact" can be derived from commit messages. Over `92a72e4c..6f29519d`, 124 commits touch a protected path; 69 name an existing plan or proposal stem or slug (56%). The 55 that name none are mostly real work referred to by another name (for example a commit titled "Remove agreement C1" for a plan with a different slug). A rule that refused on those would refuse most pins. So v1 shows each unnamed commit and counts it, and refuses only on structural states (the list above). The judgment "does this describe what I intend?" is where the Maintainer sees the count. A new trailer convention would fix it, but it is a new mechanism, so I do not propose one. I made this measurement with a throwaway script in my scratch directory; chunk R1 repeats it as a test fixture over a recorded range.

**Classification, and its limit.** "Decides" means code or a test (a file under `bootstrap/*.py`, `bootstrap/tests/**/*.py`, `scripts/*.py`, `templates/modules/**/*.py`, or an engine symbol). "Pinned" means a data fixture under `bootstrap/tests/fixtures/`. I expect most rows to read "decides", so the split removes little noise. I keep it because it is cheap and the note required it. R1 checks whether it splits the last range usefully; if not, it goes.

**Committed tooling versus a human act.**

| Committed, tested | Human |
|---|---|
| Drift detection, classification, provenance, transaction, safe write | Reading the report and answering the one question |
| Refusals and their control tests | Typing the code |
| The printed commit line and commit-body record | Committing (or telling the agent to) |
| `status`, `package` (read only; safe for the agent in the room) | `apply` runs at the Maintainer's terminal, per the Maintainer-run rule in `AGENTS.md:521-528` |

**Chunks, in order, with what each needs from the Maintainer.**

| # | Chunk | Needs from the Maintainer |
|---|---|---|
| R1 | `status` for the AST baseline and the gate manifest, read-only. Static by default; `--collect` opts into the pytest collection, which runs candidate code and says so. Ships the zero-member and refuse-all control tests. | Nothing. Run it once to see whether the report reads well. This chunk alone gives loud-on-modification. |
| R2 | `package` and `apply` for the AST baseline and its known-new manifest. | A fence: the first `apply` against the real tree waits for the Maintainer. Nothing else. |
| R3 | The gate-manifest adapter. | The same fence on its first real `apply`. |
| R4 | The lockfile adapter. Built only if a lockfile correction is owed by then (Q4). | Nothing. |
| R5 | Retire `scripts/correct_pinned_digests.py` and `bootstrap/tests/test_correct_pinned_digests.py`; cut `bootstrap/AST_BASELINE_RUNBOOK.md` to one page that points at the tool. | One gate-manifest re-pin (deleted frozen files hold the gate), paid with the next re-anchor, ideally by `repin` itself. |

**Order against 0.5.** After the engine batch and before drain mode, as the board orders them (`dev/PLANNING.md:76`). Nothing here sits on the 0.5 cut's critical path; the cut's re-anchor stays by hand (`dev/PLANNING.md`, "One re-anchor, at the cut"), unless R2 and R3 are ready and the Maintainer prefers the tool.

**Sequence caution.** New files under `scripts/` and `bootstrap/tests/` are frozen by the glob. They enter the manifest as `FROZEN-NEW` (allowed, recorded) and become `FROZEN-MODIFIED` if edited after a pin includes them. The plan should land R1 through R4 before any pin includes `repin`, or accept one extra re-pin per later edit. The first pin that includes `repin` is not covered by a prior pin of `repin`; the code review of R2 and R3 is the only cover for that first run. I note this plainly because the note claimed "the previous pin covers the tool that moves the next one".

## What is not carried from the note

* **Signed-tree binding, the dedicated ceremony key, the typed confirmation at the anchor tier.** That tier already has a driver (`scripts/reanchor_ceremony.py`) and a runbook. Folding it into `repin` widens the trust surface for no gain to the routine pins. Disposition: not in this proposal; Q7.
* **The launcher template as the eleventh authority-closure member.** The note pre-registered it as an acceptance criterion. Adding a closure member is itself a transition ceremony (`bootstrap/REANCHOR_RUNBOOK.md:311-337`) with a re-reviewed launcher, a different change from adding a routine tool. Disposition: separate proposal; Q7.
* **A sterile temporary worktree for staging.** The note proposed it so the live tree need not go quiet. At 5 protected-path commits since the last pin the dirty-tree refusal is not a bottleneck I can measure. Cut; revisit if the refusal blocks the Maintainer twice.
* **The two-program double hash.** Both programs would hash the same file under the same user; the check cannot fail except by a tool arithmetic bug, which a test pins. I use one digest and say so. The independent comparison is the replay.
* **Runbook rewrite of `bootstrap/REANCHOR_RUNBOOK.md`.** It is an authority-closure member; editing it is a closure change. Not touched here.
* **Deleting the old launcher in `~/Downloads`.** A machine-local file outside the tree. I cannot verify it and do not rely on it.

## Rationale

The routine pins recur, and each hand run is written fresh by whichever agent is present. A tool that has been reviewed once, with its refusals tested, accumulates; a scratch script does not. The REL-1 finding offers two honest answers: reduce the human act to what the Maintainer can do, or stop claiming operator judgment as a control. This takes the first, and states the one place judgment remains: the question in the report.

## Alternatives considered

* **Keep corrections manual.** Cost: six AST pins and two gate-manifest pins since 2026-08-28 were hand-run, each by a fresh script or a pasted command, and the Maintainer carries the dependency on the agent in the room. Benefit: no new code to review. This is the right call if the tool cannot be built small (see falsifiers). It stays the fallback.
* **Only the read-only `status`, hands do the writes.** This is R1 alone. It removes the silent-on-modification gap and the opacity, at the least code. It is the note's own fallback. I propose to stop there if R2 grows past the size stop (Q5).
* **Repair the blocked runner.** The review's close is a redesign, not a patch. The projection digest is its core; fixing it replaces the core.
* **Retire the human leg and say it is a formality** (REL-1's second answer). Honest, but it gives up the one place where a person can notice a change they did not intend.
* **Fold the key ceremony into `repin` now.** Rejected for size and risk; Q7.

## What is lost

* Lockfile corrections stay manual until R4, or permanently if no correction is owed (Q4).
* No automatic trigger: nothing runs `status` unprompted. The silent-on-modification gap narrows (one command shows it) but does not close. A fix would be a session-routine rule, which is new mechanism; I do not propose it.
* Coverage by named artifact is best-effort, not a guarantee. The Maintainer sees the count; the tool does not prove a review exists.
* The note's key-ceremony integration and the launcher-template closure fix are deferred (above). Neither is lost without a record: both are in Q7.

## Documentation / doctrine surface

* Governing layer: no rule text changes. The "Maintainer-run, dry-run-verified direct correction" rule (`AGENTS.md:525-526`) stays; `repin apply` is how the Maintainer runs it.
* Deliberation layer: this file; the strategy note gets a one-line status pointer at R5 (the note is a `dev/strategy` record, edited at a serialization point only).
* Descriptive layer: `bootstrap/AST_BASELINE_RUNBOOK.md` shrinks at R5. `bootstrap/REANCHOR_RUNBOOK.md` is unchanged. The tool's `--help` and module docstring carry the procedure; no new doc.
* Plain Language: the report and every refusal message follow `dev/agent_collaboration.md` rules 10 to 12 (a step, what you should see, what to do if not). The commit-body record follows rule 17: it says which checks ran.

## Install contract and frozen-file impact

* **Install contract:** none. `repin` lives in `scripts/` and `bootstrap/tests/`, is not in an install mapping (a grep for `correct_pinned_digests` in `bootstrap/_scaffold/config.py` finds nothing; the same file does list other `scripts/` files by path, so the grep can match), and it changes no lockfile schema. I did not read the whole mapping list; the plan's scoped check does.
* **Frozen set:** `scripts/repin.py` and `bootstrap/tests/test_repin.py` enter as `FROZEN-NEW` (`bootstrap/tests/_gate_manifest.py:353-355`). R5 deletes two frozen files and the nine pinned test nodes recorded for the old test (a grep of `bootstrap/tests/fixtures/gate_manifest.json` finds nine `test_correct_pinned_digests.py::` ids), so the gate holds with `FROZEN-MISSING` and `COLLECTION-DROPPED` until one re-pin.
* **Authority closure:** unchanged. `repin` is not a member and does not edit one.
* **AST baseline:** unchanged. No `bootstrap/_scaffold/` file is touched.

Proposed paths:
* `scripts/repin.py`
* `bootstrap/tests/test_repin.py`

## Evidence / verification plan

I have not run any of this yet. The plan owns the exact commands. Each row names what triggers it; Cairn has no CI, so a trigger is a person or an agent running a command.

| Check | What it shows | Trigger |
|---|---|---|
| `python -m pytest bootstrap/tests/test_repin.py` | Each refusal, each control, the replay property | The implementer, by hand, per chunk (Boundary A). Then the certifying run. |
| Certifying run (`AGENTS.md:272-296`) | The tool did not break other gates | A person starts it: before a push, before a re-anchor, before a release cut, or when asked. |
| `python bootstrap/tests/_gate_manifest.py verify` | The tree against the committed manifest | **Only a human.** Nothing runs it unprompted (`AGENTS.md:530-541`). `repin status` makes it cheaper to run, no more automatic. |
| `bootstrap/tests/test_ast_attest.py` | An engine change owes an AST re-anchor | The certifying run, or anyone running that test. |
| `python scripts/claim_check.py` and `python scripts/check_cairn.py` on this file and the plan | Paths and lines resolve | The author, by hand, before each commit. |
| `python scripts/quality_gate.py --sub neutrality` | No vendor name in shipped prose | The certifying run; `scripts/` is not shipped, so I expect a clean pass, not coverage. |

**Boundary B for the plan.** The change touches the gate manifest, a contract surface, and a trust-ceremony surface, so bounded mode refuses and the certifying run is the full pair (`AGENTS.md:311-325`).

### Tests required

Home: `bootstrap/tests/test_repin.py` (proposed). Through the real command-line entry, not helpers:

* Two trees that differ only in a kept record produce different transaction digests (the old projection defect), and `apply` refuses a transaction whose output bytes were edited after `package`.
* A preimage changed between `package` and `apply` refuses and leaves every file as it was.
* Zero-member declared sets refuse; a control shows the same check passes when a member exists.
* A non-interactive `apply` refuses. A test says plainly that a pseudo-terminal can still satisfy a terminal check, so the test pins "a pipe cannot" and nothing wider.
* A symlinked output path and a path outside the repository refuse.
* The pytest-collection disclosure appears in output (control: deliberately remove it and see the test fail).
* A refusal control for each refuse-all risk: a guard that refuses on every input fails a test that expects a pass.
* A replay test: `package` at a commit, then `package` in a detached checkout of the same commit, gives the same digest.
* Closure-member change refuses (Q3), and an unrelated change does not.

### Examples / smoke checks

`python scripts/repin.py status` on the live tree (R1 trial); `package` on a scratch copy; `apply` only on a scratch copy until the Maintainer's fence.

#### Security preflight — five questions, answered in writing

* **S1 — Who supplied it?** `status` and `package` read the tracked tree at the head commit, git history, the old fixtures and the candidate's test collection. All of that is supplied by the tree being decided about; that is inherent. The decision inputs the tree cannot supply are the typed code (the person) and the rule for what is protected, which is read from `_gate_manifest.py` and `_gate_preflight.py` as committed at the prior anchor-trusted state, not from the candidate. The plan must show how the tool reads those two from the right commit; I have not designed that yet, and it is the first thing the Security Review should test.
* **S2 — Can it fail?** Each check has a one-line mutation: edit a kept record after `package` (the digest check fails); change a file between `package` and `apply` (the preimage check fails); empty the declared set (the zero-member check refuses); remove the collection disclosure (its test fails). I have not run these; the implementer records each failing output. The typed-code check derives its expected value from the transaction it checks. It cannot detect a malicious transaction, only a different one. I say so in the tool's text.
* **S3 — What fires it, over what?** A person runs `status`, `package`, `apply`. The input set is the protected files declared by the existing tools and the three fixtures. The adopter-facing sentence does not exist: this is a Cairn-internal tool, not shipped. The operator-facing sentence is the tool's own header, which must agree with the table above.
* **S4 — Which way does it break?** Every refusal lands on "no write". A parse error, a git error or an empty set refuses. The one default that could give more authority is unnamed-artifact commits being shown rather than refused (Q2); it fails toward more authority for the Maintainer's judgment, deliberately and visibly.
* **S5 — Who still wins?** The attacker assumed: a process with the Maintainer's operating-system user. It can open a pseudo-terminal, supply the code, edit the tool before it runs, or substitute `git`. This stays open, by enumeration, and is the dated trusted-contributor residual. What this change closes by construction is the projection defect: the digest covers output bytes.

**What the Security Review must examine (I do not perform it).**

1. Transaction completeness: can two materially different trees give one digest? Is every non-tree influence named?
2. The write path: preimage swap, atomicity, symlink and containment, read-back, behaviour on a half-written failure.
3. Subprocess and environment use: sterile git, and the pytest collection that runs candidate code.
4. The human act: what the typed code is claimed to be, whether any path lets a program perform it silently, and the wording of that claim.
5. Where the protected-set rule is read from (S1), and whether the closure-member refusal points the safe way (Q3).
6. Whether the first run of `repin` over itself is acceptably covered (see Sequence caution).
7. Whether refusal messages forward every disclosure the underlying tools make.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Success criteria

* A routine pin is three acts, run from the same committed tool, nothing written for the occasion. I will count minutes at the first real use and record them; I have no baseline for the manual time, so the criterion is the Maintainer's report that it was doable.
* Every change shown is classed, and its provenance line shows the named artifact or says none.
* The AST runbook shrinks to one page; the silent-on-modification gap is visible with one command.
* The REL-1 finding closes under its first answer: operator judgment is claimed only where it occurs, and no written control names a party who does not exist.

## Signals the change is wrong

* **The note's first falsifier.** If the tool's own review-and-freeze burden exceeds the hand cost it replaces, stop at R1. I give a trigger: the tool core exceeds about 600 lines excluding tests (the old runner is 421 lines, the AST runbook 194; 600 is roughly their sum less the part the tool reuses). The number is my choice, not a measure; the Maintainer may set another (Q5).
* **The note's second falsifier.** If per-file pinning cannot be expressed without bringing back projection bookkeeping, keep per-file digests, computed and compared by the tool. This proposal already keeps them (the manifest is per-file SHA-256), so I do not expect this to fire.
* The Maintainer finds the report unreadable at first use, or the typed code becomes a reflex without reading (the habituation risk the note names).
* A refusal fires on ordinary pins more than once in a row (a refuse-all guard).
* Review finds a way for two different outputs to carry one digest.

## Questions for the Maintainer (each has a default; none blocks review)

* **Q1. Is "read one report, type one code" the right human part, instead of "compare two checksums"?** Default: yes. The two-checksum version cannot fail on one machine. The optional replay is the comparison that can.
* **Q2. Commits that name no plan or proposal: show and count, or refuse?** Default: show and count. Refusing would have blocked 55 of 124 commits in the range I measured.
* **Q3. A change to an authority-closure member inside a routine pin: refuse (send to the ceremony) or only flag?** Default: refuse. It points toward less authority; the Maintainer can still do that pin by hand.
* **Q4. Lockfile adapter (R4): build it now, or only if a lockfile correction is owed?** Default: only if owed. The old runner's lockfile logic stays in git history either way.
* **Q5. Stop line:** if the tool core passes about 600 lines before R3, stop at R1, and do writes by hand? Default: yes, and ask me.
* **Q6. Name and place: `repin`, at `scripts/repin.py`?** Default: yes. It is distinct from `reanchor`, which moves a signed ref; the old runner was renamed for exactly that confusion (`scripts/correct_pinned_digests.py:56-66`).
* **Q7. The two items I did not carry:** the key-ceremony integration, and the launcher template becoming an eleventh authority-closure member. Default: each is its own later proposal, the second with its own Security Review. I recommend the second soon, because the launcher template runs before any check and nothing pins it. Say if you want either folded in; that widens this proposal's scope and needs a revision.

## Scope delta

**Scope delta**: preserved. This is the opening version, so nothing has been dropped from a baseline. The differences from the 2026-08-28 note are recorded under "What is not carried", each with a question for the Maintainer.

## Assurance path

**Assurance path**: high-assurance

The change adds a tool that writes the files the gate and the re-anchor trust, which is a trust-ceremony surface and touches the gate manifest, a contract surface named in `AGENTS.md`. Uncertainty resolves to high-assurance. The header declares `usual + Security Review`; the plan declares `required(Internal + Internal Security Review)`. The usual review does not clear the Security Review, and I have written neither.

## Review -- Claude Sonnet 5.5 (Internal) -- 2026-10-26

```
Reviewed commit: d65f4e6bc7ef90596d40e6bd9e49b6b86847effc
Target: the whole proposal (all sections), read as git diff 0.5-dev...0.5-dev-repin, against dev/strategy/2026-08-28-claude-repin-revitalization.md and the "### 0.5" section of dev/PLANNING.md
Prior findings: none
Assurance path: high-assurance
```

**Tier**: usual (pass 1 of 2; the Security Review is a separate pass by another reviewer and is not cleared, ruled on or pre-empted here)
**Findings**: raised (3 blocking, 8 non-blocking)
**Verdict**: REVISE

**Foundations**

1. **Should this happen as framed?** Yes for `status` and the AST baseline; not as framed for the gate manifest. The proposal calls the manifest a keyless "routine pin", but in this repository each manifest pin is the commit the signed anchor points at: `refs/cairn/gate-anchor` is `6f29519d`, a one-file commit to `gate_manifest.json`, and the owed manifest pin is "Maintainer-only; follow `bootstrap/REANCHOR_RUNBOOK.md`" -- `git for-each-ref refs/cairn`, `dev/PLANNING.md:188-206`, `bootstrap/REANCHOR_RUNBOOK.md:391-399`. Doing nothing was already decided against: "Repin is a build" (`dev/PLANNING.md:45`).
2. **Best alternative.** Build R1 and R2 for the AST baseline (6 of the 8 hand pins since 2026-08-28), with `package` running in a detached worktree of the head commit so it is its own replay; give the manifest a ceremony-input step only after F1 is answered. Doing nothing costs 8 hand pins in about 7 weeks and does not touch the 0.5 cut, whose re-anchor stays by hand -- `git log --since=2026-08-28 -- bootstrap/tests/fixtures/scaffold_ast_baseline.json bootstrap/tests/fixtures/gate_manifest.json` (6 and 2, reproduced), `dev/PLANNING.md:75-83`.
3. **What would show it wrong.** The proposal's own three triggers stand (`## Signals the change is wrong`; Q5). I add the one the evidence points at: if the manifest pin cannot be separated from the key move, R3 shrinks to a step inside the ceremony and the "three acts, no key" claim fails. Also, `produce()` always runs a pytest collection, so manifest `package` is never "read only" -- `bootstrap/tests/_gate_manifest.py:384-413`.

### Rulings on the four points

**(a) The human act.** The typed code is a real control, but a narrow one. It ties the screen the Maintainer read to the bytes `apply` writes: if the transaction file is swapped between `package` and `apply`, the code no longer matches. It also stops a pipe or an accident. It is not authentication and not a check that the report is true, and the proposal says both plainly; I agree with its wording. It is also, as the note feared, hex typed from the screen above it, so on its own it can become a reflex. The only act that can fail on one machine is the clean-checkout replay: it differs from the live run in untracked and ignored files, which a pytest collection reads and a dirty-tree check does not see. **Recommendation: require the replay for the gate manifest, keep it optional for the AST baseline.** The AST path only parses tracked bytes (`ast.parse`, no execution -- `bootstrap/tests/_ast_attest.py:100-102`) and is deterministic under the pinned interpreter; the manifest path runs candidate code. Cost to the Maintainer: the replay is an agent session and one yes/no to read ("did the clean-checkout code match mine?"), about one a week at the recent rate. It is the comparison the Maintainer offered in their own words, "I'm happy to compare two different sets of checksums" (`dev/strategy/2026-08-28-claude-repin-revitalization.md:22-26`). It asks nothing of them that needs systems knowledge. The cost of leaving it optional: untracked-state influence goes unnoticed unless someone remembers. "Required" can only be a recorded line in the commit body (`Replay: matched <code> | not run`); nothing can enforce it, so say that.

**(b) The cuts.** Compared one by one in F3. The double hash: the author's to cut; the reasoning holds (both programs hash the same bytes under one user) and the replay replaces it. Key-ceremony integration: the author's to defer; this build does not reach it, and Q7 asks the Maintainer. The sterile worktree: defensible only on the "revisit if it blocks twice" trigger, because the evidence offered (5 commits since the last pin) measures volume, not blocking; F8 shows a cheaper way to avoid the loss. The launcher template as eleventh closure member: **not the author's to cut.** The note pre-registered it as an acceptance criterion, "not a tidiness item". Deferring it to its own proposal is sound (a closure change is a transition ceremony, `bootstrap/REANCHOR_RUNBOOK.md:311-315`), and the proposal asks Q7 and lists the loss, but the Scope delta line says "preserved". Only the Maintainer concedes it.

**(c) The measured claim.** Supported. I re-derived it over the same range, `92a72e4c..6f29519d`, from the tree, with a case-insensitive substring match of every plan and proposal stem and slug (6 or more characters, from `dev/plans` and `dev/proposals`, archive included) against subject and body. Under the proposal's own protected-path definition (`bootstrap/*.py`, `bootstrap/tests/**`, `scripts/*.py`, `templates/modules/**/*.py`, `bootstrap/_scaffold/**`; no merges): 111 commits, 63 linked, 57%. Under the broad reading that reproduces the proposal's 124 (any touch of `bootstrap/`, `scripts/` or `templates/modules/`; no merges): 125 commits, 72 linked, 58%. The proposal's 69 of 124 (56%) is within two points of both. The instrument can match: 63 and 72 are non-zero, and the matched names are real stems (top: `neutrality-and-upgrade-slots`, 15). Then a random sample of 20 of the 53 unlinked commits (seed 26, read by subject line, not diff): about 12 are real work named by an issue-batch id, a chunk id or a shorter name ("Remove agreement C1", "IB7", "GS-CR2 to GS-CR6"); 3 are AST pin commits themselves; 5 are small standalone fixes. So "mostly real work under another name" holds, but it is a reading, not a count, and the proposal gives no number (rule 14). A looser rule (the commit touches a plan or proposal file, or names an issue) lifts 72 of 125 to 86 of 125 (69%), still no refuse-grade rate. So "show and count" is the right v1. One caveat: the tool will see one fixture's range at a time, not this 7-week span that holds six AST pins; the per-range rate is not measured.

**(d) Chunks and the 600-line stop.** The order works: R1 is read-only and adds two new frozen files (`FROZEN-NEW`, allowed); R2 and R3 add writers one pin at a time; R4 is optional; R5 is the only chunk that leaves anything red, and the proposal says so. The by-hand `_gate_manifest.py verify` holds on `FROZEN-MISSING` and `COLLECTION-DROPPED` after R5 while the suite stays green (`AGENTS.md:530-541`); it is acceptable only if R5 lands just before the cut's re-anchor, which the plan should say. The 600 is not a sensible stop as written (F10): it is checked "before R3", after R2, the costly write path, is already built, and the figure adds 421 lines of code to 194 lines of prose.

### Findings

**F1 (blocking). The gate-manifest pin is not shown to be keyless.** The proposal says the routine pins have "no key and no ref move" and the Maintainer's three acts end in "commit". In the record, the last two anchor commits (`bd66a70`, `6f29519d`) both are manifest commits, the owed manifest pin is run by the key ceremony, and the runbook's step 2 ("generate the new gate manifest", `bootstrap/REANCHOR_RUNBOOK.md:391-399`) is a step inside it. The runbook already separates a steady-state re-anchor (no closure change) from a transition (`:311-315`). *Fix:* add a short section saying which R3 is: (i) it writes the new manifest file and stops, and the key move stays in the ceremony; or (ii) a keyless pin that leaves the anchor on an older manifest, with what `verify --anchor-ref` then reports. Restate the Maintainer's acts for the manifest accordingly, and put the choice to the Maintainer as a question with a default. *Closes when:* the proposal answers it in writing and the "three acts" table matches.

**F2 (blocking). "Read only; safe for the agent in the room" and "static by default" are false for the manifest.** `produce()` always starts a pytest collection subprocess with the inherited environment and `sys.executable`, loading the candidate's plugin (`bootstrap/tests/_gate_manifest.py:384-413`). So manifest `package` runs candidate code every time; only `status` can be static. *Fix:* correct the table row and R1; say `status` for the manifest compares file hashes only and does not check collection identity, and that `package` always collects and prints that it runs candidate code. (Whether that is safe is the Security Review's question; I only say the claim as written is wrong.)

**F3 (blocking). The Scope delta says "preserved", but the note's criteria are not all carried.** Compared with the note, one by one:

| The note | The proposal | Disposition |
|---|---|---|
| Three acts in minutes; third act is "the key where the key applies" | Success is the Maintainer's report that it was "doable"; third act is "commit" | Weaker; the key is absent (F1) |
| An unreviewed or unclassifiable change "refuses, loudly" | Shown and counted; refuses only on structural states | Measured cut (ruling c); not on the not-carried list |
| Classification kept as a security acceptance criterion | Kept "cheap" and droppable after R1 | Softened |
| Pre-registered: launcher template joins the closure | Deferred, Q7 | Disclosed; wording wrong; Maintainer concedes |
| Pre-registered: every disclosure forwarded, one control test per disclosure | One disclosure (the collection) tested; the rest sent to the Security Review | Neither carried nor listed as dropped |
| Cut the second values parser | Not mentioned | Belongs with the key tier; add to the not-carried list |
| Loud-on-modification: "the silence is gone" | Success says "visible with one command"; the R1 row says "gives loud-on-modification"; "What is lost" says no automatic trigger | Overstated in the R1 row |
| Risk or volume trigger and a maximum review budget | Absent | Neither carried nor listed |
| Sterile worktree | Cut | Listed (F8) |
| Double hash; signed tree and dedicated key | Cut and deferred | Listed; reasons hold |
| Protected-set rule derived from the prior trusted state | S1: "not designed yet" | Open (F9) |
| The two falsifiers | Carried | Carried |

*Fix:* replace "preserved" with the list of what is reduced, each with a Maintainer question and a default; fix the R1 row to "visible on demand"; enumerate the disclosures `_ast_attest`, `_gate_manifest` and the old runner print (the anchor note "resolved from the TARGET repo", the untracked-files record, the interpreter-minor hold) and either test each or ask the Maintainer to concede. Narrowing here costs the Maintainer a criterion they wrote down; only they concede it.

**F4 (non-blocking). Bind the report to the transaction.** The transaction holds every input and output byte but not the report text the Maintainer reads. The code then ties bytes to a code, not "what you read" to bytes. *Fix:* include the rendered report in the transaction bytes and have `apply` print it again beside the code check. This does not make the report true; it makes the record say what was read.

**F5 (non-blocking). Present the replay in the Maintainer's terms, and let `apply` print its status.** See ruling (a). Make Q1 a choice between required for the manifest and optional for the AST baseline, with the commit-body line `Replay: matched <code> | not run`.

**F6 (non-blocking). Write the provenance rule down once, and fix its wording.** The rule says "name an existing plan or proposal stem or slug" but not: existing at which commit; the minimum match length; case; whether the artifact must be accepted or archived (a rejected or still-open one also matches); or whether "names" implies the plan covers the changed file. The report line "NOT SHOWN AS REVIEWED" implies the named commits were shown as reviewed. *Fix:* put the rule in R1 as the test fixture and the one place it is stated; label the line "names no plan or proposal" and its counterpart "names X (status Y)". Replace "mostly" with the number (ruling c, about 12 of 20 by my reading). Say which path definition the 124 used (111 under the proposal's own).

**F7 (non-blocking). Name the replay's base in the example report.** The example is headed "AST baseline base 6f29519d", the manifest pin; the AST baseline's last pin is `5cbd6583`, 38 seconds earlier. Each fixture has its own base. *Fix:* label each report with its fixture's last-pin commit, and define `REKEYED`, `MISSING` and `DUPLICATE` where the report first appears.

**F8 (non-blocking). Run `package` in a detached worktree of the head commit.** The cut of the sterile worktree rests on "5 commits since the last pin", which measures volume, not blocking. Shared checkouts here have several sessions editing at once. The proposal's own replay test already needs a detached checkout. If `package` always runs in one, the dirty-tree refusal and the untracked-file class go away, and `package` is its own replay. *What it costs:* a temporary directory and a `git worktree add` write path, which the Security Review would take on; collection still inherits the environment. *If the cut stands:* keep the "revisit if it blocks twice" trigger and record who counts.

**F9 (non-blocking). Reuse and S1 disagree about which copy of the protected-set rule runs.** "Reuse" imports `produce` and `_frozen_files` from the tree being decided about and calls that settled; S1 says the rule must come from the prior trusted state and that this is not designed. The collection loads `-p bootstrap.tests._gate_manifest` from the candidate's directory, so the candidate's copy of that closure file runs even if `repin` imported a trusted one (`bootstrap/tests/_gate_manifest.py:389-393`). Q3's refusal is therefore the control that matters, but it does not say what "changes" are measured against (the last pin? the anchor commit?). *Fix:* state both. The default looks safe: none of nine closure files I searched (all but the allowed-signers file) changed in `92a72e4c..6f29519d`, so Q3 would not have refused an ordinary pin.

**F10 (non-blocking). Make the stop line a per-chunk budget.** Check it at the end of R1 (with an estimate for R2) and again at the end of R2; count `apply`, the transaction and the safe write separately from `status` and the report, because that is where review burden sits. Say whether R2's code is discarded or kept unmerged if the stop fires. Replace the "sum" derivation with "my choice", which the proposal already admits. And say R5 lands just before the cut's re-anchor.

**F11 (non-blocking). Readability.** The "In plain terms" section and the Q1-Q7 list read well without a translator. The lower half does not, in places: "preimage", "compare-and-swap" and "pseudo-terminal" (rule 5), "re-anchor" used for both the fixture rewrite and the ref move (rule 4; the old runner was renamed for exactly this, `scripts/correct_pinned_digests.py:56-66`), "mostly" without a number (rule 14), and the "Authoring tier" quote, which has no date and appears nowhere else in the tree (`git grep` finds only this file). *Fix:* gloss the three terms once, use "pin" for the fixture and "re-anchor" only for the ref move, and date the quote.

**Checked and found sound.** `python scripts/claim_check.py` on the proposal: no flags (four typed exemptions for the two proposed paths). By hand, all 28 `path:line` citations resolve in bounds, and the 19 I opened say what the proposal says. Numbers reproduced: 6 AST and 2 manifest pins since 2026-08-28 (a third manifest commit, `bd66a70`, sits at the date boundary and the `--since` filter misses it; not material); 10 closure members; 19 steps (RA-01 to RA-19); line counts 774, 194, 421, 177; nine pinned old-test nodes; no test names `reanchor_ceremony` (the same grep finds `reanchor.sh` in `bootstrap/tests/test_reanchor.py`, so the instrument can match); no `correct_pinned_digests` in `bootstrap/_scaffold/config.py` (that file does list 43 `scripts/` paths). The 40 and 5 commits since the last pin reproduce within one. `bootstrap/AST_BASELINE_RUNBOOK.md` is read by no test, only by `AGENTS.md` (a pointer that survives the R5 cut).

**Coverage line.** I read the proposal, the 2026-08-28 note, the 0.5 section and queued rows of `dev/PLANNING.md`, and the cited lines of the files above. I did not do the Security Review and did not clear it; for it I note only: the write path (atomicity, symlinks, preimage swap), the inherited environment and `sys.executable` in the collection, where the protected-set rule is read from (F9), the pseudo-terminal question in the human act, and whether the code binds the report (F4). I did not read `scripts/reanchor_ceremony.py` (774 lines), the old runner beyond the cited lines, the Codex review, or `_gate_reanchor.py` beyond the data-only promotion docstring; I did not test whether a manifest-only pin that leaves the anchor behind fails any gate (F1 asks the author to answer it). The provenance sample is one range, 20 commits, subject lines only; per-fixture ranges are unmeasured. I did not verify the "doctrine sets proposal authoring at high" claim or the "lowest-tier agents" quote. I did not read R4's lockfile logic. I ran no test and no tool (none exists). Blocking findings: **yes, three (F1, F2, F3)**; the rest are the author's to decide. One loop: no clearing round follows.

## Security Review -- Claude Opus 5.5 -- 2026-10-26

**Obligation**: show that nothing `repin` runs, reads, writes, prints or asks for lets the tree being pinned decide its own pin without that showing on the screen the Maintainer reads; and where one operating-system user cannot be told from another program, show the design says so rather than claiming more.

```
Reviewed commit: d65f4e6bc7ef90596d40e6bd9e49b6b86847effc (proposal text; `git diff eb43b9f0 -- <this file>` was empty before this pass)
Target: the whole proposal, read for the trust-ceremony surface; pass 1 (eb43b9f0) read for the items it left to this pass
Prior findings: none closed; pass 1's F1, F2, F4, F8 and F9 ruled on below from the security side
Assurance path: high-assurance
```

**Tier**: Security Review (pass 2 of 2)
**Findings**: raised (4 blocking, 4 non-blocking)
**Verdict**: REVISE. The Security Review does not clear at `d65f4e6b`; it clears on the conditions at the end of this section.

**In plain terms.** `repin` can be made safe for the AST baseline, because that path only reads source files and never runs them. It should not write the gate manifest: making a manifest means running setup code from the tree being pinned, and the key ceremony already does that job in an isolated copy and then signs the result. The open question in S1, where the "what is protected" rule comes from, has a cheap answer: use the tree's copy of the rule only if its bytes equal what the last anchor pinned, and refuse otherwise. Nothing earlier pins `repin` itself, so its first real write should wait until a key ceremony has pinned it. Two things I measured lie outside this proposal but you should know them: the commit the gate anchor names today (`6f29519d`) carries no signature, and a pre-compiled Python file committed into the tree can replace reviewed source without any gate noticing.

**Foundations**

1. **Should this happen as framed?** Yes for the AST baseline, whose check parses tracked source and executes none of it (`bootstrap/tests/_ast_attest.py:94-100`). No for writing the gate manifest, which the ceremony's Stage A already produces from an isolated copy and Stage B binds into the anchor (`bootstrap/tests/_gate_reanchor.py:10-25`, `bootstrap/tests/_gate_reanchor.py:240-244`, `bootstrap/REANCHOR_RUNBOOK.md:17-24`).
2. **Best alternative.** `repin` writes the AST baseline (and the known-new file when it must change, which then owes a ceremony), plus a read-only manifest `status`; manifest pins stay in the ceremony. Doing nothing leaves the keyless AST pins hand-run: 4 of the 6 AST pins since 2026-08-28 touched only the baseline; the other 2 also changed the frozen `scaffold_ast_known_new.json` and were followed by a manifest re-anchor (`git log --since=2026-08-28` over both fixtures; `6f29519d` follows `5cbd6583`).
3. **What would show it wrong.** Any byte that decides the new pin (the tool, the rule, a compiled module, the environment) coming from the tree being pinned with neither a refusal nor a line on the screen. Two such paths exist in the tooling the proposal reuses: probes 1 and 3 below.

### Probes

Python 3.13.13 (conda-forge), `/Users/kendal30/conda_envs/lhm/bin/python3.13`. Probe 1 ran in a detached worktree of `eb43b9f0` in a fresh folder, removed afterwards; probes 2 to 5 ran in empty scratch folders. No network; no write to the shared checkout except this section.

1. **The environment shapes the pinned collection.** `_gate_manifest._collect(<worktree>)`, the call `produce()` makes: control, exit 0, 4650 nodes, 9 of them in `test_correct_pinned_digests.py`. With `PYTEST_ADDOPTS=--ignore=bootstrap/tests/test_correct_pinned_digests.py` inherited: exit 0, 4641 nodes, 0 of them. `produce()` would pin the smaller set and say nothing (`bootstrap/tests/_gate_manifest.py:389`, `bootstrap/tests/_gate_manifest.py:404-406`). The ceremony's Stage A scrub removes only credential-named variables (`bootstrap/tests/_gate_reanchor.py:76-78`, `bootstrap/tests/_gate_reanchor.py:110-126`), so it inherits the same variable.
2. **A program can type the code.** From this agent's non-interactive shell, one line using the stock `script` utility (which opens a pseudo-terminal, a fake keyboard and screen) gave a child `isatty() == True`, let it open `/dev/tty`, and delivered the 12-character code to `input()`. A plain pipe gave `isatty() == False`.
3. **A compiled file can replace reviewed source.** A package whose `mod.py` says "reviewed source", with `__pycache__/mod.cpython-313.pyc` compiled from other source as an *unchecked* hash-based file (one Python loads without comparing it to the source): a default import ran the compiled file. `-X pycache_prefix=<fresh empty folder>` and `--check-hash-based-pycs always` each ran the source instead. `_frozen_files` skips every path containing `__pycache__` (`bootstrap/tests/_gate_manifest.py:357`); `.gitignore` ignores these files but `git add -f` does not; none is tracked today (`git ls-files | grep -c -E '\.pyc$|__pycache__'` gives 0).
4. **A fixed temporary name follows a planted link.** The write pattern in `_ast_attest.update_symbol` (`bootstrap/tests/_ast_attest.py:425-427`: write `<name>.tmp`, then replace) with a symlink planted at `<name>.tmp`: the link's target was overwritten, and the pinned file became a symlink.
5. **Commit text carries terminal control bytes.** `git log --format=%s` returned ESC and CR bytes raw (checked with `od -c`); `encode_display` (`templates/skills/_lib/session.py:188`) printed them as inert `\x1b` escapes. The old runner printed commit subjects raw (`scripts/correct_pinned_digests.py:218`).

Reads, not probes: `refs/cairn/gate-anchor` names `6f29519d`, whose commit has no `gpgsig` header (`git cat-file commit`) and fails `git verify-commit` (exit 1); the earlier anchor `bd66a70c` shows `G`. The committed manifest equals the anchor's copy byte for byte (`cmp`). It pins as frozen `scaffold_ast_known_new.json`, `_ast_attest.py`, `test_ast_attest.py`, `_gate_manifest.py`, `_gate_preflight.py` and `bootstrap/tests/__init__.py`; `scaffold_ast_baseline.json` is cascade-mutable; `bootstrap/_scaffold/_guard.py` and `tools/session.py` are in no pin of the manifest.

### Answers to the five questions

**1. Where the protected-set rule is read from (S1).** *Plain answer:* read the rule from the tree, but only after checking, without running anything, that its bytes equal what the anchor pinned; if they differ, refuse and send that pin to the ceremony.

*What a candidate tree could do if the rule came from it unchecked.* (a) Narrow `_frozen_files` or add a path to `CASCADE_MUTABLE` or `PHASE_SPLIT_TARGETS` (`bootstrap/tests/_gate_manifest.py:82`, `bootstrap/tests/_gate_manifest.py:107`, `bootstrap/tests/_gate_manifest.py:339`): the file leaves the protected set, and a report that lists changed files by the candidate's rule never mentions it. `PHASE_SPLIT_TARGETS` already holds a test file, so such an edit looks ordinary. (b) Shorten `declared_authority_closure()` (`bootstrap/tests/_gate_preflight.py:600-626`), so Q3's refusal never fires. (c) Change `digest_module` or `_classify` (`bootstrap/tests/_ast_attest.py:94`, `bootstrap/tests/_ast_attest.py:166`) so a changed body keeps its old digest: the new baseline is then wrong, and every later check measures against it. That is the "wrong pin that looks right". (d) Narrow the engine-module glob the AST test uses (`bootstrap/tests/test_ast_attest.py:78`).

*The right reading, in order.* (1) Resolve `HEAD` and `refs/cairn/gate-anchor` once each to object ids and use only the ids after that. (2) Read the anchored manifest as JSON from the object (`git show <anchor-id>:bootstrap/tests/fixtures/gate_manifest.json`): data, no code. (3) Before importing anything outside the standard library, hash each file in a fixed list written in `repin` (itself, `bootstrap/tests/__init__.py`, `_ast_attest.py`, `_gate_manifest.py`, and `_gate_preflight.py` if the closure list comes from it) and compare with that file's anchored `frozen_files` entry; refuse on any difference or absence. (4) Import under `python -I -X pycache_prefix=<fresh empty folder>`, so the bytes checked are the bytes run (probe 3) and no `PYTHON*` variable or same-folder module shadows the standard library; refuse if any compiled file is tracked under an import root. (5) After import, walk the modules actually loaded and refuse any local one outside the list, as `_gate_reanchor._authority_code_files` already does for the ceremony (`bootstrap/tests/_gate_reanchor.py:131-138`). (6) Measure Q3 as blob-id differences between the anchor commit and the head commit for all ten closure members, including the three non-Python ones the manifest does not cover; refuse on any difference. This also answers pass 1's F9: "changes" are measured against the anchor.

*Possible?* Yes for the AST path, which parses and never executes candidate code. No for the manifest: collection imports the candidate's `conftest.py`, every test module and its own copy of `_gate_manifest.py` (pass 1 is right on this), and a conftest hook can change the item list before the plugin records it. No choice of where to read the rule changes that; only isolation does, which is the ceremony's job (SR-2).

*What it does not close.* A commit that edits `scripts/repin.py` itself can delete the check. That edit shows as `FROZEN-MODIFIED` in `_gate_manifest.py verify` run from a trusted checkout and in the next ceremony's report, not on `repin`'s own screen. Running `repin` from an extraction of the anchor commit would close it but needs a launcher, the same unpinned-launcher gap as Q7's second item; I recommend deciding the two together, not here. And "anchored" today means "what this clone's ref names", not "what the Maintainer signed", because `6f29519d` is unsigned.

**2. The first pin that includes `repin`.** The honest story: no earlier pin covers `scripts/repin.py` or `bootstrap/tests/test_repin.py`; they enter as `FROZEN-NEW`, and the R2 code review is the only cover. With SR-1, `repin` refuses its writer until an anchor pins its bytes. That is the design working, not a defect: the first pin that includes `repin` is then a key ceremony, not a `repin` run, and `repin`'s first real `apply` comes after it. That makes the note's claim, "the previous pin covers the tool that moves the next one", true from then on. The Maintainer's act at that ceremony is one command and one yes/no, recorded in its commit body: before stage 2, `git diff <commit the R2 code review named> <candidate> -- scripts/repin.py bootstrap/tests/test_repin.py` prints nothing, and the stage-1 report lists both files as `FROZEN-NEW`. If the Maintainer wants a `repin` write before any ceremony, that is their decision to take; the check that can fail is a fresh agent producing the same baseline by the current runbook in a separate clean checkout, with byte-equal output recorded. If R3 kept a manifest writer, the first manifest `repin` wrote would pin `repin`'s own bytes, the implementer-blesses-its-own-verifier pattern the runbook forbids (`bootstrap/REANCHOR_RUNBOOK.md:11-15`). SR-2 removes that.

**3. Deleting the old runner's tests (nine nodes).** It looks exactly like tampering, by design: `verify` holds with `FROZEN-MISSING` per file and `COLLECTION-DROPPED` per node (`bootstrap/tests/_gate_manifest.py:624`, `bootstrap/tests/_gate_manifest.py:680`) until a new manifest pin. Loud is safe. Where it can hide a real drop: a tenth dropped node in the same range sits in a list of ten, nine of which share one file name. The fix has two parts. The R5 commit body lists the exact two paths and nine node ids. Any manifest `status` splits dropped nodes into "file deleted" and "file still present", printing the second group first and flagged, because a deletion cannot explain a node whose file still exists. Since the manifest pin belongs to the ceremony (SR-2), R5 should land just before the cut's re-anchor so one ceremony pays for it (pass 1's F10 says the same).

**4. Pass 1's open items.**

* *Is the manifest pin keyless (F1)?* No. The anchor names `6f29519d`, a one-file manifest commit. `verify --anchor-ref` holds whenever the working-tree manifest differs from the anchor's copy (`bootstrap/tests/_gate_manifest.py:524-526`). Stage B pins the verifier code against the anchored manifest (`bootstrap/REANCHOR_RUNBOOK.md:22-24`). Stage A already computes the next manifest from an isolated copy (`bootstrap/tests/_gate_reanchor.py:244`). A `repin`-written manifest is therefore either replaced by the ceremony's own or leaves the gate holding until a ceremony. Separately, an AST pin that changes `scaffold_ast_known_new.json` changes a frozen gate file and so also owes a ceremony; 2 of the last 6 AST pins did. "Three acts, no key" holds for the AST baseline only, when the known-new file is unchanged.
* *The inherited environment; "read only, safe for the agent"; "static by default" (F2).* Confirmed false for the manifest: `produce()` always collects (`bootstrap/tests/_gate_manifest.py:406`), with the inherited environment plus one variable (`bootstrap/tests/_gate_manifest.py:389`), and probe 1 shows that environment decides what is pinned. For the AST path, `status` and `package` can be read-only and run no candidate code, given SR-1. A static manifest view already exists, `verify(..., do_collect=False)` (`bootstrap/tests/_gate_manifest.py:532`), but it hashes working-tree files under the tree's own glob (`bootstrap/tests/_gate_manifest.py:578`), so `repin` may call it only after SR-1's check and against a clean extraction (SR-4).
* *Can an agent type the code?* Yes (probe 2). The proposal already says so, and its test pins only "a pipe cannot". Keep every message to that limit; no output may say a person confirmed anything.
* *Does the code bind the report the Maintainer read?* Not as written. The code is the digest of the transaction, the report is not in it, and `package`, which prints both, may run at an agent's screen, so the Maintainer can type a code relayed to them without having read anything the tool printed. SR-3.

**5. Anything else.** The write path is SR-5; untrusted text and output safety are SR-6; the lockfile adapter is SR-7. On race windows: reading the transaction once and rendering and writing from those same in-memory bytes (SR-3) removes the "read report, then apply" window; what remains is a writer running as the same user between the compare-and-swap read and `os.replace`, the accepted same-user residual (`bootstrap/REANCHOR_RUNBOOK.md:187-189`), which the read-back reports but cannot prevent. No issue or pull-request text is read; keep it that way (no network). **What the design refuses, not warns about:** import-list or closure bytes differing from the anchor, or an anchor that does not resolve (SR-1); a tracked compiled file under an import root (SR-1); `HEAD` moving during `package` (SR-4); an output path outside the hard-coded set, including `gate_manifest.json` (SR-2); a code from anything but a terminal, and a transaction file that is a symlink, not the user's own, or writable by others (SR-3, SR-5); a symlinked target or parent, or a target not tracked as a regular file (SR-5). **Shown, not refused:** commits naming no plan or proposal (Q2's default); an unsigned anchor commit, on the first line of every report; a known-new change, with the words "owes a ceremony re-anchor".

### Findings

**SR-1 (blocking). The protected-set rule and the tool's own code are read from the tree being pinned, unchecked.** S1 leaves this undesigned, and "Reuse" imports the tree's copies. *Fix:* put the six steps of answer 1 into "What each check refuses" and S1 as contract text, with the paragraph on what they do not close. *Closed when:* the proposal states that order, and the Tests list adds three, each with its control: a candidate commit that changes `_ast_attest.py` refuses with no write (control: unchanged bytes pass); a tracked unchecked `.pyc` under `bootstrap/tests/__pycache__/` refuses (control: none tracked, passes); a closure-member blob change refuses (control: an unrelated change passes). *Clears the obligation once answered so:* yes.

**SR-2 (blocking). No `repin` path writes the gate manifest.** R3 becomes a static manifest `status` whose output the Maintainer reads at the ceremony's report step; the manifest pin stays in the ceremony. The output set is hard-coded in `repin`: the AST baseline, the known-new file, and the lockfile only if R4 is built. A transaction naming any other path refuses. When the known-new file is among the outputs, the report and the printed commit line say it changes a frozen gate file and owes a ceremony re-anchor. *What is lost:* a tool-written manifest outside the ceremony, which the ceremony would overwrite or which would leave the gate holding (answer 4), so nothing the Maintainer can use; the readable manifest drift view is kept. The narrower change still reaches the cause, opaque hand-run commands, because the manifest's commands already have a driver (`bootstrap/reanchor.sh`). Only the Maintainer concedes the loss. *If the author keeps a writer instead,* it runs in a fresh extraction, starts from an empty environment and adds back only what it names, refuses when any `PYTEST_*` or `PYTHON*` variable is set (probe 1), and is new material needing a second Security Review pass. *Closed when:* the proposal says one or the other, and a test shows a transaction naming `gate_manifest.json` refuses (control: the baseline alone passes). *Clears once answered so:* yes.

**SR-3 (blocking). The typed code binds bytes, not the reading.** *Fix:* `apply` reads the transaction file once into memory and renders the report itself from those bytes: a key-by-key comparison, in `repin`'s own code, of the preimage it found on disk against the output it will write (added, removed, digest changed, old and new digest), never stored report text and never the candidate's `_classify`. It prints its code beneath that render and accepts it only from a terminal. The transaction includes the rendered bytes (pass 1's F4), and the commit body records the code, the transaction digest and the render digest. `package`'s code stays, for the replay comparison only. *Closed when:* the proposal says so, and a test shows that every key `apply` changes appears in the screen it printed before asking (control: drop one row from the render and the test fails). *Clears once answered so:* yes.

**SR-4 (blocking). The transaction names a commit, but its inputs come from the shared working tree.** `digest_module` reads working-tree files (`bootstrap/tests/_ast_attest.py:100`); the engine-module set is a glob that includes untracked files (`bootstrap/tests/test_ast_attest.py:78`); `produce` hashes working-tree bytes for cascade files (`bootstrap/tests/_gate_manifest.py:447`). So with an untracked engine module present, or another session editing during the run, the output follows from bytes that no commit holds, while the transaction says "head commit X". This is the transaction-completeness question: the digest covers the output, but the stated input does not determine it. *Fix:* `package` resolves `HEAD` once, extracts that commit with `git archive` into a fresh private folder, reads only that copy, and refuses if `HEAD` moved by the end. Every git call goes through the existing sterile launcher (`bootstrap/tests/_gate_manifest.py:176-194`), adding `core.fsmonitor=false` to any call that reads a working tree. This is pass 1's F8, now required for security reasons, and it makes `package` its own replay. *Closed when:* the proposal says so, and a test shows an untracked engine module in the working tree does not appear in the output (control: committed, it does). *Clears once answered so:* yes.

**SR-5 (non-blocking; the plan's Security Review must find it in the plan).** Safe-write specifics: (a) temporary files from `tempfile.mkstemp` in the target's folder, never a fixed name (probe 4); (b) refuse when the target or any parent up to the repository root is a symlink (an `os.lstat` walk), or the target is not tracked as a regular file; (c) open with `O_NOFOLLOW` and do the compare-and-swap read immediately before `os.replace`; (d) with two outputs, write and check both temporaries before replacing either; after a partial failure, print which file was replaced and the exact `git restore --source=<head-id> -- <path>` line, exit non-zero, and run no restore itself; (e) the transaction folder from `tempfile.mkdtemp`, and `apply` refuses a transaction file that is a symlink, not the user's own, or writable by others; (f) do **not** import `bootstrap/_scaffold/_guard.py`: it is engine code whose integrity the AST baseline attests, so importing it puts the code being attested inside the tool that attests it, and it is in no manifest pin. Write the containment rule in `repin` and give that reason in a comment, so a later reader does not "fix" it into an import.

**SR-6 (non-blocking; plan).** Untrusted text. Every string from git (subjects, bodies, paths, refs), from file names under `dev/plans` and `dev/proposals`, from the transaction and from a subprocess's error output passes through `encode_display` before it reaches the screen or the printed commit line. Read git output as bytes, not with `text=True`, which turns a CR into a newline before any encoder sees it. Provenance from commit text is a claim anyone can write: label it "the message names <stem>", never "reviewed", and let no refusal or acceptance depend on it. `encode_display` sits outside the manifest (`tools/session.py`), so record its blob id among the transaction's named influences. Test: a commit subject with ESC and CR appears escaped in `status` output (control: an ordinary subject is unchanged).

**SR-7 (non-blocking; only if R4 is built).** "Lift the plan logic from the old runner" carries its CPD-3 defect: `plan_lockfile` imports the tree's engine `config` module, running candidate code before anything is shown (`scripts/correct_pinned_digests.py:239-241`). Parse the mappings from the head commit's blob with `ast`, never import them, and keep any read of a record's `dst` inside the repository by the SR-5 rule.

**SR-8 (non-blocking; outside this proposal, for the Maintainer).** Two pre-existing gaps measured on the way, each worth its own queued row: (a) the current anchor commit `6f29519d` is unsigned, while the runbook says an anchor is trusted for "the signature on the object it names" and "is verified, never assumed" (`bootstrap/REANCHOR_RUNBOOK.md:594-598`); (b) the ceremony's Stage A inherits `PYTEST_*` and `PYTHON*` variables into the collection it pins (probe 1), and no pin covers a force-added compiled file, which can replace any gate helper module's reviewed source (probe 3). Neither blocks this proposal.

**Clearing.** This Security Review does not clear at `d65f4e6b`. It clears on conditions: the author's Response, in its complete current contract, adopts SR-1 to SR-4 as stated, or an alternative that meets each "Closed when" line. The Maintainer at the Decision and the plan's Internal Security Review, already declared in the header, check that they are carried. No second proposal-stage Security pass is needed unless the Response keeps a manifest writer (SR-2's alternative) or replaces the S1 design, which would be new material. SR-5 to SR-7 do not block; the plan carries them. The Status stays `revising`.

**Coverage line.** I read the proposal, pass 1, the cited lines of `_gate_manifest.py`, `_ast_attest.py`, `test_ast_attest.py`, `_gate_preflight.py:590-640`, `_gate_reanchor.py` (header, Stage A, the environment scrub), `_guard.py`, `encode_display`, the old runner's header and lockfile planner, the outside review's CPD-3, CPD-5, CPD-6 and redesign, and the runbook's two-stage, transition and posture sections. I did not read `scripts/reanchor_ceremony.py`, `bootstrap/reanchor.sh` or the launcher template, so I did not check whether the stage-1 report groups dropped nodes or shows the anchor's signature state. I did not trace `_gate_preflight.py`'s own import closure, test the compiled-file path against the real suite (scratch package only), check whether pytest's assertion rewriting touches `_gate_manifest.py` during collection, re-measure pass 1's provenance figures, or read R4's lockfile logic past `scripts/correct_pinned_digests.py:245`. The pseudo-terminal probe ran on macOS only. I ran no test from the suite and never set `CAIRN_FULL_SUITE`.

## Response -- Claude (author) -- 2026-10-26

I accept all eleven usual findings and all seven security findings, two of them with a variation. The Revision below is the complete current contract. Two things changed the design most: `repin` no longer writes the gate manifest (SR-2), and everything it reads comes from a `git archive` extraction of one commit, checked against the anchor before any of it runs (SR-1, SR-4). I also took in the Maintainer's feedback of 2026-10-26, quoted in the Revision.

**Usual review (pass 1)**

* **F1, accepted.** The manifest pin is not keyless. It stays in the key ceremony; `repin` only reads the manifest. The "acts" are restated per pin, and the Maintainer is asked in Q8.
* **F2, accepted.** Manifest `status` is a static comparison and says it does not check collection. There is no `--collect`, and no manifest `package`.
* **F3, accepted.** "Preserved" is gone. The Scope delta lists every criterion of the 2026-08-28 note that is not fully carried, each for the Maintainer to concede or refuse. The launcher template stays a question to the Maintainer (Q7), with the loss stated.
* **F4, accepted, through SR-3.** The rendered report is inside the transaction bytes.
* **F5, accepted with a variation.** The replay is optional for the AST pin, with the commit-body line `Replay: matched <code> | not run`. I did not make it required for the manifest, because `repin` no longer writes the manifest, so there is nothing to replay. Q1.
* **F6, accepted.** The provenance rule is written once, below, with its measured figures.
* **F7, accepted, with a correction.** Each report names its own fixture's last-pin commit. `REKEYED` and `DROPPED` are not class names in `bootstrap/tests/_ast_attest.py` (grep finds neither); I used them loosely. The Revision uses the real names: `CHANGED`, `MISSING`, `DUPLICATE`, `NEW`.
* **F8, accepted, through SR-4.** `package` reads an extraction, so the dirty-tree refusal and the untracked-file class go away.
* **F9, accepted, through SR-1.** Both copies of the rule are settled: it is read from the tree only after its bytes equal the anchor's, and "changes" are measured against the anchor.
* **F10, accepted with a variation.** The stop line is a per-chunk size budget. The numbers are my choice, not a measure (Q5).
* **F11, accepted.** Three terms are glossed once, "pin" names the fixture write, "re-anchor" names only the ref move. I cannot date or source the "Authoring tier" quote and it appears nowhere else, so the Revision does not repeat it; the Maintainer can confirm it.

**Security Review**

* **SR-1, accepted as stated.** The six-step reading order is contract text. Three tests are added, each with its control.
* **SR-2, accepted (the first alternative).** No `repin` path writes `gate_manifest.json`. An AST pin that also changes the frozen `scaffold_ast_known_new.json` owes a ceremony. The chunks are re-cut.
* **SR-3, accepted as stated.** `apply` renders the report itself from the bytes it will write.
* **SR-4, accepted as stated.**
* **SR-5, accepted into the plan,** non-blocking, with one variation: tests build a scratch repository with its own anchor, so `apply` can be tested without ever touching the real tree.
* **SR-6, accepted into the plan,** non-blocking.
* **SR-7, accepted,** and applies only if R4 is built.
* **SR-8 (the unsigned anchor commit; inherited `PYTEST_*` variables and force-added compiled files in the ceremony).** Outside this proposal. The coordinator is putting both to the Maintainer as separate roadmap rows. I do not add them here.

## Revision -- Claude (author) -- 2026-10-26

### Maintainer input

The Maintainer, relayed by the Developer session, 2026-10-26. This is input to the revision, not a Decision:

> "I noticed that the gate anchor ceremony didn't use a key, but honestly it's still too damned complicated for me to properly execute in a meaningful way."

Three things follow. (1) The success test is the Maintainer's report that a pin was doable, so the ceremony part below is written to that test. (2) The Maintainer has not said which part is hard: the commands, knowing what to check, or the key. That is Q9. (3) The current anchor commit is unsigned (measured by the Security Review with `git cat-file commit`), which fits what the Maintainer saw. Whether it should be signed is the SR-8 row, outside this proposal. Every report prints the anchor's signature state on its first line.

### In plain terms

**What changes.** Today a pin means the Maintainer pastes commands an agent wrote that day. After this build, one committed tool, `repin`, computes what changed in the AST baseline, shows it on one screen, and writes the new pin only after the Maintainer types a short code from that screen. For the gate manifest it only shows what changed; the key ceremony still writes it.

**What the Maintainer does, per pin.**

| Pin | What the Maintainer does | Who runs the rest |
|---|---|---|
| AST baseline alone | Read one screen, answer "does this describe what I meant to bless?", type the 12-character code, commit. | `repin`. |
| AST baseline plus `scaffold_ast_known_new.json` | The same, and the screen says "owes a ceremony re-anchor". | `repin` writes both files; then the ceremony row below. Two of the last six AST pins were like this. |
| Gate manifest (a ceremony) | Read one short summary and say yes or no. Then the key and the push, as the runbook assigns them today. | The agent runs every other step. |

**The ceremony row, in a form the Maintainer can carry out and judge.** The agent runs every ceremony step before the key (RA-01 to RA-13 in `bootstrap/REANCHOR_RUNBOOK.md`), then shows one summary from `repin status` of what the manifest pin would change: which files are new, changed or deleted, which commits touched them (by their messages), whether any of the ten authority-closure files changed, and the anchor's signature state. The Maintainer answers one question: "are these the changes I expected?" That is a judgment he can make without systems knowledge.

What he cannot check, and so is not his sign-off: that the checksums are right, that the test collection is complete, that the ceremony report's digest binds what the summary shows. For these, **the control is the agent's recorded step, not his approval.** The agent records each command and its output in the commit body, and a fresh agent may replay it in a clean checkout. The summary is a reading aid computed from the same tree; the digest does not bind it. Nothing in this proposal claims his "yes" verifies a checksum.

**What is left for him, and how long.** Per AST pin: read one screen, type one code, commit; I expect about 5 minutes and have no measure. Per ceremony: read one summary (also about 5 minutes, unmeasured), then the key and the push exactly as today. I do not change the key steps (RA-16, RA-18, RA-19), because they belong to the ceremony driver, not to `repin`. The first real use records the minutes. If the key steps are the hard part, that is a separate proposal (Q9).

**What it costs.** One tool and its tests in five chunks, with a size budget per chunk. I have no measure of its size yet. The go-ahead is on record: "Repin is a build" (`dev/PLANNING.md:45`).

**What breaks if I am wrong.** A flaw could bless a change the Maintainer did not intend. The header declares a Security Review for that reason. If the tool grows too large, the fallback is `status` alone (R1 and R3), with the writes by hand as today.

**Terms.** *Pin*: write a checksum file (the AST baseline, the known-new file, the manifest, the lockfile) so it matches the tree. *Re-anchor*: move the signed ref `refs/cairn/gate-anchor`; only the ceremony does this. *Preimage*: the bytes of a file as they are now, before the tool overwrites them. *Compare-and-swap*: refuse to write if the file's current bytes are not the preimage. *Pseudo-terminal*: a fake keyboard and screen that a program can open; the Security Review showed one can type the code.

### Context (what still holds)

* The old runner `scripts/correct_pinned_digests.py` refuses on entry (`scripts/correct_pinned_digests.py:345-347`). Its review found two critical flaws: `--authorize` lets any process do the human act, and the plan digest covered a projection of the plan, so two different trees digested alike.
* Pins are still by hand. From `git log --since=2026-08-28`: six commits to `bootstrap/tests/fixtures/scaffold_ast_baseline.json`, two to `bootstrap/tests/fixtures/gate_manifest.json`. Of the six AST pins, two also changed the frozen known-new file and were followed by a manifest re-anchor.
* The gate anchor is the commit that changed `gate_manifest.json` last; a manifest pin is part of the key ceremony (`bootstrap/REANCHOR_RUNBOOK.md:391-399`).
* The manifest goes stale silently when a frozen file changes after it is committed; only `python bootstrap/tests/_gate_manifest.py verify` compares (`AGENTS.md:530-541`).
* The ceremony driver `scripts/reanchor_ceremony.py` exists and is read-mostly. The 2026-08-28 note's `reanchor_drive.py` landed under that name. Its 365-commit diff problem is smaller now (40 commits on `0.5-dev` since `6f29519d`, 5 touching a protected path).

### Proposal

**One loop, one tool.** A protected set of files changes only through reviewed work; a pin records the state; `repin` finds the drift and moves the AST pin after a typed code. Gate-manifest pins stay in the ceremony.

**Three verbs.**

* `status` reads and writes nothing. For the AST baseline it prints, per changed symbol, the class (`CHANGED`: body changed; `MISSING`: baselined, now absent; `DUPLICATE`: defined in more than one file; `NEW`: not in the baseline, must be in the known-new file), the commits that touched the file since this fixture's last pin, and the provenance line (below). For the manifest it prints a static drift view (below). Its first line is the anchor's signature state; its second is the count of commits touching protected paths since each fixture's last pin.
* `package` computes the whole transaction from an extraction (below) and writes it to a new private folder outside the repository.
* `apply` reads the transaction once, renders the report itself, shows it, asks for the code, then writes the AST baseline (and the known-new file if it must change). It does not commit and does not push. It prints the exact `git commit <paths>` line.

**Reading order (before anything is shown or written).** All of this is contract; the plan carries the detail.

1. Resolve `HEAD` and `refs/cairn/gate-anchor` once each to object ids; use only the ids. Refuse if the anchor does not resolve.
2. Read the anchored manifest as JSON from the anchor object (`git show <anchor-id>:bootstrap/tests/fixtures/gate_manifest.json`). This is data; no code runs.
3. Extract `HEAD` with `git archive` into a fresh private folder and read only that copy. Every git call goes through the existing sterile launcher (`bootstrap/tests/_gate_manifest.py:176-194`), plus `core.fsmonitor=false` on any call that reads a working tree. Refuse if `HEAD` moved by the end of `package`.
4. Before importing anything outside the standard library, hash each file in a fixed list written in `repin` (`repin` itself, `bootstrap/tests/__init__.py`, `_ast_attest.py`, `_gate_manifest.py`, and `_gate_preflight.py` for the closure list) and compare with that file's `frozen_files` entry in the anchored manifest. Refuse on any difference or absence. `apply` also refuses while the anchor does not pin `repin`'s own two files.
5. Do the work in a child process run under `python -I -X pycache_prefix=<fresh empty folder>`, importing from the extraction, so the bytes checked are the bytes run. Refuse if any compiled file is tracked under an import root. After import, refuse any loaded local module outside the list.
6. Measure the closure as blob-id differences between the anchor commit and `HEAD` for all ten authority-closure members (three are not Python and the manifest does not cover them). Refuse on any difference. This is the one meaning of "changes" in this proposal.

*What this does not close.* A commit that edits `scripts/repin.py` itself can delete step 4. That shows as `FROZEN-MODIFIED` in `_gate_manifest.py verify` from a trusted checkout and in the next ceremony's report, not on `repin`'s screen. Running `repin` from an anchor extraction would close it but needs a launcher; I recommend deciding that together with Q7, not here. "Anchored" means what this clone's ref names, not what the Maintainer signed.

This works for the AST pin because it only parses source (`bootstrap/tests/_ast_attest.py:94-100`). It cannot work for the manifest, because test collection runs the candidate's code; that is why the manifest is not written here.

**Manifest `status` (read only, static).** After steps 1 to 6, it calls the existing static view (`verify(..., do_collect=False)`, `bootstrap/tests/_gate_manifest.py:532`) on the extraction. It shows `FROZEN-MODIFIED`, `FROZEN-MISSING` and new frozen files. It says in its own text that it does not check collection and runs no candidate code. Dropped test nodes appear only where collection runs (`bootstrap/tests/_gate_manifest.py:680`). So `status --dropped-from <file>` reads the saved text of a `verify` run, as data, and prints first, flagged, the dropped nodes whose test file still exists, then those whose file was deleted. A deletion cannot explain the first group. This option is my choice to meet the Security Review's condition without collecting; the plan may find a simpler way.

**The transaction.** One JSON file, bound by the SHA-256 of its bytes:

* the head commit id, its tree id, and the anchor id;
* the blob id and SHA-256 of each file `apply` will overwrite;
* every influence outside the tracked tree, by name: interpreter version, git version, and the blob id of `encode_display` (`tools/session.py`, outside the manifest);
* the full new bytes of each output file;
* the rendered report bytes.

The output set is hard-coded: the AST baseline, the known-new file, and the lockfile only if R4 is built. A transaction naming any other path, including `gate_manifest.json`, refuses.

**`apply` shows the Maintainer what it will write (SR-3).** It reads the transaction once into memory and renders the report itself from those bytes. The render is a key-by-key comparison, in `repin`'s own code, of the file as found on disk against the output it will write: each key added, removed or changed, with old and new digest. It never uses stored report text and never the candidate's `_classify`. It prints its 12-character code beneath that render and accepts the code only from a terminal. The commit body records the code, the transaction digest and the render digest. `package` prints its own code for the replay comparison only. If the known-new file is among the outputs, the report and the commit line say it changes a frozen gate file and owes a ceremony re-anchor. `apply` also refuses if `HEAD` is not the transaction's head commit, or if any file's current bytes differ from its preimage.

**The typed code is a confirmation and intent record, not authentication.** A program can open a pseudo-terminal and type it (probe 2 of the Security Review). The tool says so in its text, has no `--authorize` flag and no non-interactive path, and claims only that a pipe or an accident cannot supply the code. No message says a person confirmed anything. The same-user residual stays under the dated trusted-contributor posture (`bootstrap/REANCHOR_RUNBOOK.md:339`).

**Provenance, written once.** For each commit since a fixture's last pin that touches a file the report names, `status` matches, case-insensitively and as substrings, the stem and the slug (each of 6 or more characters) of every file under `dev/plans` and `dev/proposals`, archive included, as they exist at `HEAD`, against the commit's subject and body. It prints "the message names `<stem>` (status `<Status line>`)" or "the message names no plan or proposal". The word "reviewed" is never used, no refusal depends on the match, and the text is shown as a claim anyone could have written. *Measured, over `92a72e4c..6f29519d`:* my count was 69 of 124 touching commits naming one (56%), under a broad path reading. The pass 1 reviewer reproduced 63 of 111 (57%) under this proposal's own path definition and 72 of 125 (58%) under the broad one. In a sample of 20 unnamed commits read by subject, about 12 were real work under another name (an issue-batch id, a chunk id, a shorter name). That is a reading, not a count. I have not measured a per-fixture range, which is what the tool will see.

**Classification.** "Decides" means code or a test; "pinned" means a data fixture under `bootstrap/tests/fixtures/`. I expect most rows to read "decides". The note required the split, so I keep it; R1 measures whether it separates anything over the last range (Q10).

**Safe writes (plan items, SR-5).** Temporary files from `tempfile.mkstemp` in the target's folder, never a fixed name. Refuse if the target or any parent up to the repository root is a symlink, or the target is not tracked as a regular file. Open with `O_NOFOLLOW`; make the compare-and-swap read immediately before `os.replace`. With two outputs, write and check both temporaries before replacing either. After a partial failure, print which file was replaced and the exact `git restore --source=<head-id> -- <path>` line, exit non-zero, and restore nothing. The transaction folder is from `tempfile.mkdtemp`; `apply` refuses a transaction file that is a symlink, not the user's own, or writable by others. Do not import `bootstrap/_scaffold/_guard.py`: the AST baseline attests that code, so importing it would put the attested code inside the attester. Write the containment rule in `repin` and say why in a comment.

**Untrusted text (plan items, SR-6).** Every string from git, from file names under `dev/plans` and `dev/proposals`, from the transaction, and from a subprocess's error output goes through `encode_display` (`templates/skills/_lib/session.py:188`) before it reaches the screen or the printed commit line. Git output is read as bytes, not with `text=True`.

**Lockfile adapter (R4, SR-7).** If built, it parses the mappings from the `HEAD` blob with `ast` and never imports them (the old runner's `plan_lockfile` imports the tree's engine module, `scripts/correct_pinned_digests.py:239-241`), and keeps any read of a record's `dst` inside the repository by the safe-write rule.

**What each check refuses, with no write.** An anchor that does not resolve; any file in the step-4 list or any closure member differing from the anchor; a tracked compiled file under an import root; `HEAD` moving during `package`; an output path outside the hard-coded set; a code from anything but a terminal; a transaction file that is a symlink, not the user's own, or writable by others; a symlinked target or parent; a changed preimage; an interpreter whose minor version is not the pinned one; any git error; a declared set with zero members (each such check has a control test that passes when a member exists). **Shown, not refused:** commits naming no plan or proposal (Q2); an unsigned anchor commit; a known-new change.

**Disclosures forwarded.** The underlying tools make disclosures: the anchor "resolved from the TARGET repo" note, the untracked-files record, the interpreter-minor hold (named by pass 1; I have not enumerated them all). The plan lists every disclosure the tools `repin` calls make, from their source, and gives each a control test: remove the line and the test fails.

**Chunks.**

| # | Chunk | Needs from the Maintainer |
|---|---|---|
| R1 | The shared core and `status` for the AST baseline: reading order steps 1 to 6, the provenance rule as a test fixture, the classification split, the refusals and their controls. Read only. | Nothing. Run `status` once to see if the report reads well. |
| R2 | The transaction, `package` and `apply` for the AST baseline and the known-new file: safe write, the render in `apply`. | `apply` on the real tree waits for a key ceremony that pins `repin` (below). |
| R3 | Manifest `status`: the static drift view and `--dropped-from`. Read only. Writes nothing, and no `repin` path writes `gate_manifest.json`. | Nothing. |
| R4 | The lockfile adapter, with SR-7. Only if a lockfile correction is owed (Q4). | Nothing. |
| R5 | Retire `scripts/correct_pinned_digests.py` and `bootstrap/tests/test_correct_pinned_digests.py`; cut `bootstrap/AST_BASELINE_RUNBOOK.md` to one page. The commit body lists the two paths and the nine node ids. | One manifest pin by the ceremony. R5 lands just before the 0.5 cut's re-anchor, so that ceremony pays for it once. |

**Size budget, per chunk (my choice, not a measure; Q5).** Lines of code excluding tests: R1 and R3 together about 300; R2 about 300, counting the transaction, `apply` and the safe write separately from `status` and its report, because the review burden sits there. Check at the end of R1, with an estimate for R2, and again at the end of R2. If the budget fires, stop at `status`, keep R2's code unmerged on a branch and not discarded, and do writes by hand.

**The first pin that includes `repin` is a key ceremony.** `scripts/repin.py` and `bootstrap/tests/test_repin.py` enter as `FROZEN-NEW`, and nothing earlier pins them, so with step 4 `apply` refuses until an anchor does. The Maintainer's one manual check at that ceremony, recorded in its commit body: `git diff <commit the R2 code review named> <candidate> -- scripts/repin.py bootstrap/tests/test_repin.py` prints nothing, and the stage-1 report lists both files as `FROZEN-NEW`. If it prints nothing, what was reviewed is what is pinned; if it prints something, refuse. After that ceremony, "the previous pin covers the tool that moves the next one" is true. If the Maintainer wants a `repin` write before any ceremony, the check that can fail is a fresh agent producing the same baseline by the current runbook in a separate clean checkout, with byte-equal output recorded (Q9).

**Order against 0.5.** After the engine batch and before drain mode (`dev/PLANNING.md:76`). Nothing here is on the cut's critical path; the cut's re-anchor stays by hand and is the ceremony that first pins `repin`, unless the Maintainer prefers an earlier one.

### Documentation, install contract, frozen files

* No rule text changes. "Maintainer-run, dry-run-verified direct correction" (`AGENTS.md:525-526`) stays; `repin apply` is how the Maintainer runs it.
* The strategy note gets a one-line status pointer at R5, at a serialization point. `bootstrap/REANCHOR_RUNBOOK.md` is a closure member and is not touched.
* Install contract: none. `repin` is in `scripts/` and `bootstrap/tests/`, not in an install mapping (a grep for `correct_pinned_digests` in `bootstrap/_scaffold/config.py` finds nothing; the same file lists other `scripts/` files, so the grep can match). I did not read the whole mapping list; the plan's scoped check does.
* Frozen set: the two new files enter as `FROZEN-NEW` (`bootstrap/tests/_gate_manifest.py:353-355`). R5 deletes two frozen files and nine pinned nodes, so the gate holds with `FROZEN-MISSING` and `COLLECTION-DROPPED` until the manifest pin. Authority closure and AST baseline: unchanged.
* The report and every refusal message follow Cairn Plain Language rules 10 to 12; the commit-body record follows rule 17.

Proposed paths:
* `scripts/repin.py`
* `bootstrap/tests/test_repin.py`

### Evidence / verification plan

I have run none of this. The plan owns the commands. Cairn has no CI, so every trigger is a person or an agent running a command. Boundary A: `python -m pytest bootstrap/tests/test_repin.py`, per chunk, by the implementer. The certifying run (`AGENTS.md:272-296`) is started by a person before a push, a re-anchor or a release, or on request. `_gate_manifest.py verify` runs only by a person; `repin status` makes it cheaper, not automatic. The change touches the gate manifest and a trust-ceremony surface, so Boundary B is the full pair (`AGENTS.md:311-325`). `claim_check.py` and `check_cairn.py` run on this file and the plan, by the author.

**Tests required** (real command-line entry, not helpers; each with its control):

* Two trees differing only in a kept record give different transaction digests; `apply` refuses a transaction whose output bytes were edited after `package`.
* A candidate commit that changes `_ast_attest.py` refuses with no write (control: unchanged bytes pass).
* A tracked unchecked `.pyc` under `bootstrap/tests/__pycache__/` refuses (control: none tracked, passes).
* A closure-member blob change refuses (control: an unrelated change passes).
* A transaction naming `gate_manifest.json` refuses (control: the baseline alone passes).
* Every key `apply` changes appears in the screen it printed before asking (control: drop one row from the render and the test fails).
* An untracked engine module in the working tree does not appear in the output (control: committed, it does). `HEAD` moving during `package` refuses.
* A commit subject with ESC and CR appears escaped in `status` (control: an ordinary subject is unchanged).
* A preimage changed between `package` and `apply` refuses and leaves every file as it was.
* A non-interactive `apply` refuses. The test says a pseudo-terminal can still satisfy a terminal check and pins only "a pipe cannot".
* A symlinked target, a symlinked parent, a path outside the repository, and a planted `<name>.tmp` link each refuse or are not followed.
* Zero-member sets refuse (control: a member present passes); each refuse-all risk has a control that expects a pass.
* Each disclosure the called tools make appears in output (control: remove it and the test fails).
* `--dropped-from` prints the still-present-file group first (control: a deleted-file node prints second).
* The provenance rule, as a fixture over a recorded range.
* A replay: `package` at a commit, then again in a detached checkout of the same commit, gives the same digest.

Tests build a scratch repository with its own anchor ref; `apply` is never run against the real tree before the first ceremony. No independent scientific check applies.

### Security preflight

* **S1. Who supplied it?** The tree being pinned supplies the files; it does not supply the rule, because the rule's bytes must equal the anchor's before any of it runs (reading order, steps 1 to 6). The typed code supplies the person.
* **S2. Can it fail?** Each check has a mutation in the tests above and a control that passes.
* **S3. What fires it?** A person runs `status`, `package`, `apply`. The tool's header must agree with the table in "In plain terms".
* **S4. Which way does it break?** Every refusal is "no write". The one default that gives more authority is unnamed-artifact commits shown rather than refused (Q2), deliberately and visibly.
* **S5. Who still wins?** A process with the Maintainer's operating-system user: it can type the code, edit the tool before it runs, or substitute `git`. This stays open under the dated posture. The projection defect is closed by construction: the digest covers the output bytes and the render. The unsigned gate anchor and the ceremony's inherited environment are outside this proposal.

### Signals the change is wrong

* The tool exceeds a chunk budget (Q5); stop at `status`.
* If per-file pinning cannot be expressed without projection bookkeeping, keep per-file digests, computed and compared by the tool. The manifest's are per-file already, so I do not expect this to fire.
* The Maintainer finds the report unreadable, or the code becomes a reflex typed without reading.
* A refusal fires on ordinary pins twice in a row (a refuse-all guard).
* Any way for two different outputs to carry one digest.
* The Maintainer says the ceremony summary still needs knowledge he does not have (Q9).

### Questions for the Maintainer (each has a default; none blocks)

* **Q1. Replay.** Optional for the AST pin, recorded as `Replay: matched <code> | not run`. Nothing can enforce "required". Default: optional.
* **Q2. Commits that name no plan or proposal: show and count, or refuse?** Default: show and count; refusing would have blocked about 43% of commits in the measured range.
* **Q3. A closure-member change since the anchor, inside a pin: refuse.** Default: refuse. The Maintainer can still do that pin by hand.
* **Q4. Lockfile adapter: only if a correction is owed.** Default: only if owed.
* **Q5. Size budget per chunk:** about 300 lines each for R1 and R3 together and for R2, excluding tests. Default: those numbers; stop at `status` if R2 passes its budget.
* **Q6. Name and place: `repin`, at `scripts/repin.py`.** Default: yes.
* **Q7. The launcher template as the eleventh authority-closure member (a closure change is a transition ceremony; `bootstrap/REANCHOR_RUNBOOK.md:311-337`), and the key-ceremony integration.** The first is not mine to cut. The note pre-registered it as an acceptance criterion. Default: its own later proposal with its own Security Review. **What is lost until then:** the launcher runs before any check and nothing pins its template, so the ceremony's first bytes are unchecked, and `repin` cannot be run from an anchor extraction. I recommend doing it soon. Say if you want it folded in; that widens scope and needs a revision.
* **Q8. Do you allow the reductions in the Scope delta below, including that `repin` never writes the manifest?** Default: allow, each as listed. Neither I nor a reviewer can concede them.
* **Q9. Which part of the ceremony is too complicated: the commands, knowing what to check, or the key?** Default, until you say: knowing what to check. That is the part this proposal addresses (the agent runs the commands; you read one summary and say yes or no). If it is the key, that is a separate proposal about the ceremony's key steps, not this tool. Also: when should `repin`'s first real write happen? Default: at the cut's re-anchor, with AST pins by hand until then. Alternative: an earlier ceremony of your choosing.
* **Q10. If R1 shows the decides/pinned split separates nothing over the last range, may I drop it?** Default: ask you first.

### Scope delta

**Scope delta**: degraded. The baseline is the opening contract and the 2026-08-28 note it was built from. Only the Maintainer concedes any row (Q8). The proposed dispositions are mine; the unlabelled "carried" rows owe nothing.

* The opening R3: a gate-manifest `package` and `apply`, and the claim "three acts, no key" for the manifest. Now the manifest is read-only here and pinned in the ceremony. **disposition**: accept. Specifying it was rejected because collection runs candidate code and a `repin`-written manifest would either be overwritten by the ceremony or leave the gate holding, so the Maintainer could not use it.
* The note's "three acts, the third the key where the key applies" and "in minutes". Now three acts only for an AST pin that leaves the known-new file unchanged; others owe a ceremony. Minutes are the Maintainer's report, not measured. **disposition**: accept.
* The note's "an unreviewed or unclassifiable change refuses, loudly". Now shown and counted; refusal only on structural states, because about 43% of commits in the measured range name no artifact. **disposition**: accept. (Q2)
* The note's pre-registered "launcher template joins the closure". Not built here. **disposition**: defer. (Q7; loss stated there)
* The note's "every ceremony disclosure is forwarded, one control test per disclosure". Carried for the tools `repin` calls. Not carried for the ceremony driver, which `repin` does not wrap. **disposition**: defer for the driver.
* The note's "cut the second values parser" and "signed tree, dedicated ceremony key, typed confirmation at the anchor tier". Both belong to the launcher and key tier. **disposition**: defer. (Q7)
* The note's "risk or volume trigger". Not built: nothing runs `status` unprompted. `status` prints the commit count since each last pin, so the volume is visible on demand. A session-routine rule would be new mechanism. **disposition**: defer. The "maximum review budget" is carried as the per-chunk size budget.
* The note's "the modification-staleness silence is gone". Now the silence is visible on demand only. **disposition**: accept.
* The note's "the runbooks shrink to a page each". Only the AST runbook shrinks (R5); `bootstrap/REANCHOR_RUNBOOK.md` is a closure member and stays. **disposition**: defer.
* The two-program double hash. Replaced by the optional replay; both programs would hash the same bytes as the same user. **disposition**: accept.
* The note's "the previous pin covers the tool that moves the next one". True only after the first ceremony that pins `repin`; `apply` refuses before. Carried, delayed.
* The deletion of the old launcher in `~/Downloads`: a machine-local file I cannot verify; I do not rely on it.

Carried, no delta: the transaction object, compare-and-swap and read-back writes, the zero-member rule with controls, classification (Q10), the sterile staging (now an extraction), the two falsifiers, and the provenance listing from file history, never pickaxe.

### Assurance path

**Assurance path**: high-assurance, unchanged. The header declares `usual + Security Review` and the plan `required(Internal + Internal Security Review)`. SR-1 to SR-4 are adopted as stated, and the manifest writer, which the Security Review said would need a second pass, is gone, so I expect no second proposal-stage pass. I wrote neither review.

### Withdrawn / superseded commitments

* **Opening R3, the gate-manifest adapter (`package` and `apply` for the manifest).** Replaced by a read-only manifest `status`. Why: SR-2 and F1.
* **"Three acts, no key for the routine pins."** Replaced by the per-pin table. Why: F1, SR-2, and the Maintainer's feedback.
* **"`status` static by default; `--collect` opts into collection"; "`package` read only; safe for the agent in the room".** Withdrawn. Why: F2; collection runs candidate code.
* **"R1 gives loud-on-modification."** Replaced by "visible on demand". Why: F3; nothing runs `status` unprompted.
* **`REKEYED` and `DROPPED` as AST class names.** Replaced by the real names. Why: F7; they do not exist in `bootstrap/tests/_ast_attest.py`.
* **"Reuse: import `produce` and `_frozen_files` and the AST functions from the tree."** Replaced by the six-step reading order. Why: SR-1, F9.
* **The transaction holding "the head commit" read from the shared working tree.** Replaced by a `git archive` extraction of one resolved commit, with a refusal if `HEAD` moves. Why: SR-4, F8.
* **The report text printed by `package` as the thing the code covers.** Replaced by a render `apply` makes itself from the bytes it will write. Why: SR-3, F4.
* **The sterile-worktree cut.** Reversed: the extraction is the sterile staging. Why: F8, SR-4.
* **`apply` rehearsed on a scratch copy of the real tree.** Replaced by tests on a scratch repository with its own anchor. Why: step 4 makes `apply` refuse until an anchor pins `repin`.
* **The 600-line stop checked before R3.** Replaced by a per-chunk budget. Why: F10.
* **"Scope delta: preserved".** Replaced by "degraded" with the table. Why: F3.
* **The "Authoring tier" paragraph.** Not restated. Why: F11; I cannot date or source the quote.
* **"The first pin that includes `repin` is covered by the code review of R2 and R3."** Replaced by a key ceremony with one manual diff check. Why: SR answer 2.
* **"The provenance report line `NOT SHOWN AS REVIEWED`."** Replaced by "the message names ... (status ...)" and "names no plan or proposal". Why: F6, SR-6.

## Response -- Claude (author) -- 2026-10-26 -- the Maintainer widened the scope

The Maintainer widened the scope (quoted in Revision 2), so this is a second Response and Revision. It answers no new review finding. Revision 2 below is the complete current contract and stands alone.

**What changed.**

* **Scope.** From the routine pins to the whole ceremony: the AST pin, the gate-manifest pin and the signed anchor, run by one committed script.
* **The ceremony half already exists.** `scripts/reanchor_ceremony.py` does most of it. I call it; I do not redesign it. What is missing is listed under "What exists, measured".
* **Signing, measured.** With the key in the ssh agent, every signing form I tried signed with no human present. With the agent cut off, every form asked for the passphrase. The script uses the second route.
* **The typed 12-character code is withdrawn.** The Maintainer asked for a yes or no and a passphrase. The passphrase is the one step a program cannot perform, if three conditions hold (stated below).

**Security Review conditions.** SR-1 to SR-4 stay, in full. SR-2 reads: no `repin` path writes `gate_manifest.json`. The script orchestrates the existing producer, which runs in the isolated copy the launcher makes. It is not a second writer. SR-3 varies: `apply` shows the render and asks yes or no, with no code. SR-5 to SR-7 go to the plan as before.

**A second round, and what it reads.** The doctrine allows a second round because a revision that widened scope has material no review has read (`AGENTS.md`, "The lifecycle"). Signing is a new trust-ceremony surface. I ask for a short, targeted Security Review of three things only: the signing step, the whole-ceremony orchestration, and the yes-or-no variation. The header Status is `awaiting-review` for that reason.

## Revision 2 -- Claude (author) -- 2026-10-26 -- the whole ceremony, on the Maintainer's direction

This is the complete current contract. It stands alone: the opening and Revision 1 are history.

### The Maintainer's direction

Relayed to the author with this task, 2026-10-26. This is the Maintainer's own change of scope, and his words are the authority for it. Verbatim and set apart:

> "The commands should be executed automatically via a single script, in my opinion. This script should then use my key which I enter a password for. As of right now, it's some set of steps that still are using one-off scripts built by agents. We've been struggling around this issue for a while now."

Earlier the same day, as quoted in Revision 1:

> "I noticed that the gate anchor ceremony didn't use a key, but honestly it's still too damned complicated for me to properly execute in a meaningful way."

### In plain terms

**What changes.** One committed script runs the whole ceremony. It writes the AST pin, runs the gate-manifest pin and the signing, and checks the result. The Maintainer stops composing or pasting commands.

**What the Maintainer does.**

1. Run one command: `python scripts/repin.py ceremony --values <your values file> --ceremony-dir <your folder>`.
2. Read Summary 1 and type `yes` or `no`. It lists the engine symbols whose pin would change and the commits that touched them. It is skipped when no AST pin is owed.
3. Read Summary 2 and type `yes` or `no`. It lists what the new gate manifest will newly pin, whether any of the ten authority files changed, the anchor's signature state, and the fingerprint of the key that will sign.
4. Type the key's passphrase when the signing tool asks for it.
5. Run the push line the script prints, or tell the agent to. The script never pushes.

If anything else happens, the script stops and says why, in the form rules 10 to 12 of Cairn Plain Language ask for. Nothing is pushed.

Summary 2 cannot exist before Summary 1 is committed, because the ceremony signs a commit made from the committed tree. So an owed AST pin costs two yes answers, and no AST pin costs one (Q1).

**What he judges, and what he does not.** He answers one question in each summary: "are these the changes I expected?" He can answer it without systems knowledge. He cannot check that the checksums are right or that the test collection is complete. Those are **the script's recorded step, not his sign-off**: the script writes a plain-text record outside the repository (every command, its exit status, the digests it computed) and prints the record's path and digest. His "yes" is a confirmation record. It authenticates nothing.

**The one control a program cannot perform.** The passphrase. It is a control only if three things hold. (1) The signing tool is cut off from the ssh agent, or the key is not loaded: measured. (2) No passphrase helper supplies it: measured for `SSH_ASKPASS` and `SSH_ASKPASS_REQUIRE`. (3) The passphrase is not stored in the macOS keychain or in a helper he set up: **not measured, and only he knows** (Q3).

**How long.** Unmeasured. The ceremony's first stage runs a pytest collection of about 4650 test nodes (the Security Review's count); I have not timed it. The first real run records the minutes. One-time needs: a values file, and a current packet-and-launcher pair from the out-of-band review. I do not know whether he has either, or whether the pair matches today's closure. The script's first screen says (Q5).

**What it costs.** One script and its tests, in six chunks with a size budget per chunk. I have no measure of the size yet. The go-ahead is on record: "Repin is a build" (`dev/PLANNING.md:45`).

**What breaks if I am wrong.** A flaw could bless a change he did not intend, or sign when he did not mean to. The header declares a Security Review for that reason. If the tool grows too large, the fallback is `status` alone, with the steps by hand as today.

**Terms.** *Pin*: write a checksum file so it matches the tree. *Anchor*: the ref `refs/cairn/gate-anchor`. *Re-anchor*: move the anchor. *Checkpoint*: the signed commit the ceremony makes from the committed tree plus the new gate manifest; the branch and the anchor both move to it. *Ssh agent*: a background program that holds loaded keys and signs for any program running as the user, with no prompt. *Packet and launcher*: a pair of files produced out of band by a security review. The launcher starts the ceremony, and the packet lists the reviewed digests of the ten authority files. *Values file*: his outside-the-repository file naming the key, the executables and the folders the ceremony uses. *Preimage*: a file's bytes before the tool overwrites it. *Compare-and-swap*: refuse to write if the file's current bytes are not the preimage.

### What exists, measured

* **The ceremony driver does most of the ceremony half.** `scripts/reanchor_ceremony.py` (774 lines) with `--run` runs a preflight, stage 1 without the ssh agent, the report, the package digest computed twice, and stage 2 with the agent, and prints the push line (`scripts/reanchor_ceremony.py:546-676`). It asks three yes-or-no questions. No test names it (a grep of `bootstrap/tests/*.py` finds nothing; the same grep finds `reanchor.sh` in `bootstrap/tests/test_reanchor.py`, so the instrument can match). The anchor pins it (`git show refs/cairn/gate-anchor:bootstrap/tests/fixtures/gate_manifest.json` lists `scripts/reanchor_ceremony.py`).
* **What the driver does not do.**
  1. The AST pin. It is a separate hand step before the ceremony.
  2. Require a human to sign. It tells the Maintainer to `ssh-add` the key and says either way works (`scripts/reanchor_ceremony.py:628-641`). I measured below that a loaded key signs with no human present.
  3. Spare him a trap. Stage 1 can ask for a passphrase that he must decline (`scripts/reanchor_ceremony.py:567-573`, `bootstrap/REANCHOR_RUNBOOK.md:144-146`). By reading the code, the probe runs with stdin closed but keeps the controlling terminal (`bootstrap/tests/_gate_preflight.py:2204-2211`); my measurement below shows that is when a prompt appears.
  4. Check the result. Nothing confirms the anchor ended up signed. The current anchor is not: `git log -1 --format=%G? 6f29519d` gives `N`.
  5. Pass the first test: it has none.
* **Stage 2 forwards the agent socket as it finds it.** `reanchor.sh` starts the checker with `env -i`, which drops other variables, and passes `SSH_AUTH_SOCK` through, empty when unset (`bootstrap/reanchor.sh:655-662`). The route below relies on an empty value acting like an unset one, which I measured.
* **Stage 2 signs.** It names the key on each call (`bootstrap/tests/_gate_preflight.py:2624-2631`), and the branch and the anchor move in one transaction (`bootstrap/REANCHOR_RUNBOOK.md:175-177`). So `commit.gpgsign=false` in this checkout does not matter to it.
* **The unsigned anchor.** Of the five entries in the anchor's reflog, `bd66a70c` shows `G` (the Maintainer's key, fingerprint `SHA256:8R549gtP...`), three earlier ones show `U` (a key the roster does not hold), and `6f29519d` shows `N`. `6f29519d` is a one-file commit to `gate_manifest.json` made on the branch. I infer it was a hand commit and a hand `update-ref`, not a stage-2 checkpoint. The reflog cannot tell the two apart, because by-hand runs use the same fixed reason (`bootstrap/REANCHOR_RUNBOOK.md:429-433`).
* **The machine, read only.** `git config` gives `gpg.format ssh`, `user.signingkey /Users/kendal30/.ssh/cairn_signing.pub`, `commit.gpgsign false`, and `gpg.ssh.allowedsignersfile` pointing at `dev/.cairn/allowed_signers`, which has one line. `git tag -v v0.4.0` reports a good signature by `SHA256:8R549gtP...`. `ssh-add -l` lists two keys, an RSA key (`SHA256:gAhPgXaH...`) and an ED25519 key (`SHA256:wuCkJjCO...`). Neither is the signing key. I did not open the private key and did not read `~/.ssh`.
* **Where the packet and launcher come from.** A review produces them out of band, and the launcher embeds the packet's digest (`bootstrap/reanchor-launcher.template.sh:1-24`). No tool makes them. In the last measured range none of nine closure files changed (the Security Review, pass 2), so a pair should survive routine ceremonies. That is a measurement over one range, not a guarantee.

**Signing routes, measured.** I made a throwaway ed25519 key with a passphrase in a scratch folder, a scratch repository configured like this one (`gpg.format ssh`, `user.signingkey` pointing at the `.pub`), and my own scratch ssh agent. `HOME` pointed at the scratch folder, so nothing read `~/.ssh`. "Terminal" means a pseudo-terminal the harness controlled; "no terminal" means a new session with stdin closed.

| Form | Key in the agent | Agent cut off (`SSH_AUTH_SOCK` unset or empty) |
|---|---|---|
| `ssh-keygen -Y sign` with the `.pub` path | signed, no prompt, with or without a terminal | prompted on the terminal and signed after the passphrase; no terminal: failed, no signature |
| the same with the private-key path, and with `-U` | signed, no prompt | prompted on the terminal and signed after the passphrase (private path; `-U` not tried with the agent cut off) |
| `git commit -S` | signed, no prompt | prompted; no terminal: failed |
| `git tag -s` | signed, no prompt | prompted; no terminal: failed |
| `git commit-tree -S -F -` with the message on a pipe (the ceremony's form) | signed, no prompt | prompted on the terminal even with stdin a pipe; no terminal: failed (measured with the message on the command line) |

Also measured:

* A key loaded in the agent but a signer environment with the socket removed or empty behaves like the right-hand column. Removing the socket makes the route prompt even when the key is loaded.
* `SSH_ASKPASS` and `SSH_ASKPASS_REQUIRE=force` naming a program that prints the passphrase: signed with no human, with or without a terminal. The signer's environment must drop both.
* The probe shape the ceremony uses (no terminal, no socket, helper variables cleared) failed without prompting. So a stage 1 run in a new session removes the prompt he would have to decline. I measured the single `ssh-keygen` call, not the real stage 1.
* `ssh-add -c` (confirm each use): the agent refused to sign when no confirmation helper existed. I did not measure it with a helper, so I do not rely on it.
* `ssh-add -d <key>.pub` removed the key from the agent.

**Assumed, not measured.** The real stage 1 and stage 2 under a pseudo-terminal, with the real launcher. That the signing tool prompts once in stage 2 (I expect one signature). That `DISPLAY` needs clearing (I set it in my test and did not test it alone). Whether his passphrase is stored anywhere a program can read.

### Proposal

**One script, three verbs.** `scripts/repin.py`.

* `status` reads and writes nothing. It prints the AST drift, the manifest drift (static) and the provenance lines, as in Revision 1.
* `package` computes the AST pin's transaction from an extraction and prints its digest. It writes only to a new private folder. A fresh agent can run it in a clean checkout to replay the pin and compare digests. The replay is optional, recorded in the commit body as `Replay: matched <digest> | not run`; nothing can enforce "required".
* `ceremony` runs the whole sequence below. `--first-run` is described under "The first ceremony".

**What the script replaces and what it calls.**

| Existing | What happens to it |
|---|---|
| `scripts/correct_pinned_digests.py` and `bootstrap/tests/test_correct_pinned_digests.py` | Retired in R6. The script refuses on entry already (`scripts/correct_pinned_digests.py:345-347`). |
| `bootstrap/AST_BASELINE_RUNBOOK.md` | Cut to one page that points at the script (R6). |
| `scripts/reanchor_ceremony.py` | **Called, not edited, until R6.** The script imports its read-only helpers (`compare`, `check_packet_pair`, `values_field`, `key_fingerprint`, `key_in_agent`) after the reading-order check below. It does not use `rehearse` (stage 1 makes the same checks, and the rehearsal would run the test collection a second time). It does not use `drive()`. R6 removes `drive()` and `--run` so there is one way to run the ceremony (Q7). That edit changes a frozen file and is paid in a ceremony. |
| `bootstrap/reanchor.sh` and the launcher | **Called, unchanged.** The script runs `validate`, the launcher for stage 1 and for stage 2, `show-report` and `hash-package`. |
| `bootstrap/tests/_ast_attest.py` | Called by the AST pin step, after the reading-order check. |
| `bootstrap/tests/_gate_manifest.py` | **Not called to write.** Its only writer path stays the launcher's stage 1 and stage 2, in the isolated copy. The script calls its static view for `status`. This is SR-2. |
| `ssh-add`, `ssh-keygen`, `git verify-commit` | Called for the agent check, the fingerprint and the final verification. |

**The `ceremony` sequence.**

1. **Checks, no write.** A terminal on stdin and stdout; `HEAD` on a branch; no dirty tracked file (the script lists them and stops); the anchor resolves; the reading order below; `reanchor.sh validate` on the values file; the packet and launcher pair (`check_packet_pair`); the signing key is in the anchored roster; the interpreter is the pinned minor version. If the key is loaded in the agent, the script says so on the first screen (the route in step 5 still prompts).
2. **AST pin, if owed.** Package the transaction from an extraction of `HEAD`, render it, show Summary 1, ask yes or no, write the AST baseline (and the known-new file if it must change), then commit those paths with `git commit <paths>`, never signed and never pushed. The commit body records the transaction digest, the render digest, the interpreter and the checks run. If a pin is owed but a refusal below fires, the script stops here.
3. **Stage 1.** Through the launcher, in a new session with no controlling terminal, stdin closed, and an environment without `SSH_AUTH_SOCK`, `SSH_ASKPASS`, `SSH_ASKPASS_REQUIRE` and `DISPLAY`. This stage runs the candidate's test collection, which executes candidate code; the script prints the banner the checker prints.
4. **Summary 2.** The artifact's `show-report`, the package digest computed twice (the ceremony's `hash-package` and the script's own `hashlib`, which must agree), the manifest drift from `status`, and the key fingerprint. Ask yes or no.
5. **Stage 2, the signing step.** Through the launcher with `--stage2 <digest>`, in a child with the terminal attached and an environment without the four variables above. The launcher's `env -i` already drops the helper variables, and the script removes them too, so it does not depend on that. The signing tool asks for the passphrase directly. **The script never reads, stores or passes the passphrase**, and does not touch the terminal while the prompt is up.
6. **Verification.** Read the roster from the previous anchor's object. Run `git verify-commit` on the new anchor with sterile git and that roster. Refuse to print "done" unless the result is a good signature by the expected fingerprint.
7. **End.** Print the new branch and anchor ids, the record's path and digest, the line "the key was never in the agent, nothing to put away" (or the `ssh-add -d` line if it was), and the push line from `bootstrap/REANCHOR_RUNBOOK.md`, Phase 5. It does not run it.

**Reading order (SR-1), before anything is shown or written.** The detail goes to the plan.

1. Resolve `HEAD` and `refs/cairn/gate-anchor` once each to object ids. Refuse if the anchor does not resolve.
2. Read the anchored manifest as JSON from the anchor object. Data only.
3. Extract `HEAD` with `git archive` into a fresh private folder and read only that copy. Every git call goes through the sterile launcher (`bootstrap/tests/_gate_manifest.py:176-194`), plus `core.fsmonitor=false` where a working tree is read. Refuse if `HEAD` moved by the end of `package`.
4. Before importing anything outside the standard library, hash each file in a fixed list written in `repin` (`bootstrap/tests/__init__.py`, `_ast_attest.py`, `_gate_manifest.py`, `_gate_preflight.py` and `scripts/reanchor_ceremony.py`) and compare with its anchored `frozen_files` entry. Refuse on any difference or absence. `ceremony` and the AST write also refuse while the anchor does not pin `repin`'s own two files, except under `--first-run`.
5. Do the AST work in a child run under `python -I -X pycache_prefix=<fresh empty folder>`, importing from the extraction. Refuse if any compiled file is tracked under an import root. After import, refuse any loaded local module outside the list.
6. Measure the closure as blob-id differences between the anchor and `HEAD` for all ten authority members. For the AST pin, any difference refuses. In the ceremony half, a difference makes a transition ceremony, which needs a reviewed packet; the script says so and stops, because it cannot make one.

*What this does not close.* A commit that edits `scripts/repin.py` can delete step 4. That shows as `FROZEN-MODIFIED` in `_gate_manifest.py verify` run from a trusted checkout and in the next ceremony's report, not on `repin`'s screen. The launcher is the ceremony's pre-candidate trust root and nothing pins its template (Q8). "Anchored" means what this clone's ref names, not what the Maintainer signed, until the anchor is signed.

**Refusals, no write.** Everything under step 1; a tracked compiled file under an import root; `HEAD` moving; an AST pin with `MISSING` or `DUPLICATE` symbols (a review item, never a pin, per `bootstrap/AST_BASELINE_RUNBOOK.md`); a pin that adds or drops a baseline key (a full re-pin); an output path outside the hard-coded set (the AST baseline, the known-new file, the lockfile if R5 is built), including `gate_manifest.json`; a code or answer from anything but a terminal; a transaction file that is a symlink, not the user's own, or writable by others; a symlinked target or parent; a changed preimage; any git error; a declared set with zero members. Each check has a control test that passes when its condition is fine. **Shown, not refused:** commits naming no plan or proposal (their share in the measured range was about 43%); an unsigned previous anchor; a known-new change; a loaded key.

**The AST pin's transaction and render (SR-3, varied).** One JSON file bound by its SHA-256, holding the head and anchor ids, each output's preimage blob id and SHA-256, every influence outside the tracked tree (interpreter, git, the blob id of `encode_display`), the full new bytes and the rendered summary. The script reads it once, renders Summary 1 itself from those bytes (a key-by-key comparison of the file on disk against what it will write, never stored text, never the candidate's `_classify`), shows it, and asks yes or no only on a terminal. **Variation from Revision 1:** no code is typed. A typed code, as the Security Review showed, is confirmation, not authentication, and the Maintainer asked for a yes or no. `apply` is no longer a verb; the write happens inside `ceremony` after the yes. The yes is the Maintainer's confirmation and the record carries it.

**Manifest `status` (static, SR-2).** As in Revision 1: after the reading order it calls `verify(..., do_collect=False)` on the extraction and lists `FROZEN-MODIFIED`, `FROZEN-MISSING` and new frozen files. It says it does not check collection. `status --dropped-from <file>` reads the saved text of a `verify` run and prints first the dropped nodes whose test file still exists. The ceremony shows this in Summary 2.

**Provenance and classification.** For each commit since a fixture's last pin that touches a file the summary names, match case-insensitively, as substrings, the stem and slug (6 or more characters each) of every file under `dev/plans` and `dev/proposals` as they exist at `HEAD`, against the commit's subject and body. Print "the message names `<stem>` (status `<Status line>`)" or "the message names no plan or proposal". Never "reviewed"; no refusal depends on it. Measured over `92a72e4c..6f29519d`: 69 of 124 touching commits named one (my count, broad path reading); the pass-1 reviewer got 63 of 111 (57%) and 72 of 125 (58%). About 12 of a 20-commit sample of the unnamed ones were real work under another name (a reading, not a count). I have not measured a per-fixture range. "Decides" means code or a test; "pinned" means a data fixture; R1 checks the split separates something and drops it if not.

**Safe writes (SR-5, plan).** `tempfile.mkstemp` in the target's folder; refuse a symlinked target or parent or a target not tracked as a regular file; `O_NOFOLLOW`; compare-and-swap read immediately before `os.replace`; with two outputs, write and check both before replacing either; after a partial failure, print what was replaced and the exact `git restore --source=<head-id> -- <path>` line, exit non-zero and restore nothing. The private folder from `tempfile.mkdtemp`. Do not import `bootstrap/_scaffold/_guard.py` (the AST baseline attests that code, so importing it would put the attested code inside the attester); write the containment rule in `repin` and say why in a comment.

**Untrusted text (SR-6, plan).** Every string from git, from file names under `dev/plans` and `dev/proposals`, from the transaction and from a subprocess's error output goes through `encode_display` (`templates/skills/_lib/session.py:188`) before it reaches the screen or a printed command. Git output is read as bytes. This includes the launcher's and the checker's output the script relays.

**Lockfile (R5, SR-7).** Only if a correction is owed. It parses the mappings from the `HEAD` blob with `ast` and never imports them.

**Disclosures forwarded.** The plan lists every disclosure the called tools make, from their source: the candidate-code banner, the anchor "resolved from the TARGET repo" note, the untracked-files record, the interpreter-minor hold, the unsigned-anchor state, the driver's preflight notes. Each gets a control test: remove the line and the test fails.

**The first ceremony.** `scripts/repin.py` and `bootstrap/tests/test_repin.py` enter the manifest as `FROZEN-NEW`, so no anchor pins them. Until one does, step 4 refuses the AST write and `ceremony`. The first run is therefore two things: the AST pin by hand under the runbook, one more time, then `ceremony --first-run`. The flag is valid only while the anchored manifest has no entry for `scripts/repin.py`, so it cannot be used later to skip step 4. The run that first pins `repin` is a ceremony the usual way, and the Maintainer's manual check is recorded with it: `git diff <commit the R4 code review named> <candidate> -- scripts/repin.py bootstrap/tests/test_repin.py` prints nothing, and Summary 2 lists both files as `FROZEN-NEW`. If that prints something, refuse. After that ceremony, "the previous pin covers the tool that moves the next one" is true. If he wants a `repin` write before any ceremony, the check that can fail is a fresh agent producing the same pin by the runbook in a separate clean checkout, with byte-equal output recorded (Q6).

**Chunks.**

| # | Chunk | Needs from the Maintainer |
|---|---|---|
| R1 | Shared core and `status` for the AST baseline: reading order, provenance as a test fixture, classification split, refusals and controls. Read only. | Nothing. Run `status` once to see if it reads well. |
| R2 | The AST transaction, `package`, the render and the write with the safe-write rules; tested in a scratch repository with its own anchor. | Nothing. The first real write waits for the first ceremony. |
| R3 | Manifest `status`: the static view and `--dropped-from`. Read only. | Nothing. |
| R4 | `ceremony`: the sequence above, the signing step, the verification and the record, using the existing ceremony tests' packet and launcher builders (`bootstrap/tests/test_reanchor.py:959-1025`) and a throwaway key. | Nothing until the first real run, which is the first ceremony. |
| R5 | The lockfile adapter, only if a correction is owed. | Nothing. |
| R6 | Retire `scripts/correct_pinned_digests.py` and its test; remove `drive()` and `--run` from `scripts/reanchor_ceremony.py`; cut the AST runbook to one page. The commit body lists the paths and the nine pinned node ids. | One ceremony pays for the manifest changes. R6 lands just before the 0.5 cut's ceremony. |

**Size budget per chunk (my choice, not a measure).** Lines of code excluding tests: R1 and R3 together about 300; R2 about 300; R4 about 250, counting imported helpers as zero because they are not copied. Check at the end of R1 with an estimate for R2, again at the end of R2, and at the end of R4. If a budget fires, stop at `status`, keep the later code unmerged on a branch, and do the steps by hand.

**Order against 0.5.** After the engine batch and before drain mode (`dev/PLANNING.md:76`). The cut's ceremony stays by hand and is the one that first pins `repin`, unless the Maintainer chooses an earlier one.

### Documentation, install contract, frozen files

* No rule text changes. "Maintainer-run, dry-run-verified direct correction" (`AGENTS.md:525-526`) stays; `repin ceremony` is how he runs it. `SECURITY.md` says the ceremony key is dedicated (`SECURITY.md:193-197`). This design uses the key he already signs with; that is a departure from the written rule, put to him as Q2.
* The strategy note gets a one-line status pointer at R6. `bootstrap/REANCHOR_RUNBOOK.md` is a closure member and is not touched.
* Install contract: none. The plan's scoped check confirms `scripts/repin.py` is in no install mapping.
* Frozen set: the two new files enter as `FROZEN-NEW`. R6 deletes two frozen files and nine pinned nodes and edits `scripts/reanchor_ceremony.py`, so the gate holds until the ceremony that follows. The authority closure and the AST baseline are unchanged.
* Every message follows Cairn Plain Language rules 10 to 12. The commit-body record follows rule 17.

Proposed paths:
* `scripts/repin.py`
* `bootstrap/tests/test_repin.py`

### Evidence / verification plan

I have run none of the script; the plan owns the commands. Cairn has no CI, so every trigger is a person or an agent running a command. Boundary A: `python -m pytest bootstrap/tests/test_repin.py` per chunk, by the implementer, plus the existing `bootstrap/tests/test_reanchor.py` (which owns the launcher). The certifying run (`AGENTS.md:272-296`) is started by a person before a push, a re-anchor or a release, or on request. The change touches the gate manifest and a trust-ceremony surface, so Boundary B is the full pair. `claim_check.py` and `check_cairn.py` run on this file and the plan, by the author. The signing tests need `ssh-keygen` and `ssh-agent`; if absent they skip with a named reason, and the record says so.

**Tests required** (real command-line entry; each with its control):

* Two trees that differ only in a kept record give different transaction digests; an edited output byte refuses.
* A candidate that changes `_ast_attest.py` refuses with no write (control: unchanged bytes pass). A tracked `.pyc` under an import root refuses (control: none passes). A closure-member change refuses an AST pin (control: an unrelated change passes).
* A transaction naming `gate_manifest.json` refuses (control: the baseline alone passes). During `ceremony` in a scratch repository, `gate_manifest.json`'s blob id is unchanged until stage 2 runs.
* Every key the write changes appears in the screen printed before the question (control: drop a row from the render and the test fails).
* An untracked engine module in the working tree is not in the output (control: committed, it is). `HEAD` moving refuses.
* A commit subject with ESC and CR is escaped (control: an ordinary subject is unchanged).
* A changed preimage refuses and leaves every file as it was. Symlinked target, symlinked parent, outside path and a planted `<name>.tmp` link each refuse or are not followed.
* An answer from a pipe refuses. The test says a pseudo-terminal can still satisfy a terminal check and pins only "a pipe cannot".
* **Signing, with a throwaway key and its own agent, in a scratch repository:** with the key loaded in the agent, the script's stage 2 still prompts (control: with the socket left in, the same call signs with no prompt, so the test shows it can fail); the signer's environment lacks the four variables (control: with `SSH_ASKPASS_REQUIRE=force` left in, it signs with no human); no terminal fails with no signature; the verification refuses an unsigned checkpoint, a checkpoint signed by a key not in the roster, and a checkpoint verified against the candidate's roster instead of the previous anchor's (control: a good one passes).
* A key in the agent is named on the first screen.
* Stage 1 runs with no controlling terminal and no socket (control: with a terminal the probe prompts).
* Zero-member sets refuse (control: a member present passes); each refuse-all risk has a control that expects a pass.
* Each disclosure the called tools make appears in output (control: remove it and the test fails).
* `status --dropped-from` prints the still-present-file group first. The provenance rule over a recorded range. A replay: `package` at a commit and again in a detached checkout gives one digest.
* `--first-run` refuses once the anchored manifest has an entry for `scripts/repin.py`.

Tests build a scratch repository with its own anchor; the real tree sees no write before the first ceremony.

### Security preflight

* **S1. Who supplied it?** The tree being pinned supplies the files. It does not supply the rule or the tool code the pin runs: their bytes must equal the anchor's before any of it runs (reading order). The person supplies the yes, and the passphrase.
* **S2. Can it fail?** Each check has a mutation in the tests above and a control that passes.
* **S3. What fires it?** A person runs `ceremony`, `status` or `package`. The script's header must agree with "In plain terms".
* **S4. Which way does it break?** Every refusal is "no write, no signature". The defaults that give more authority are shown-not-refused commit provenance and a loaded key that is only named; the second is safe because the signing route does not use the agent.
* **S5. Who still wins?** A process with the Maintainer's operating-system user. It can type a yes on a pseudo-terminal, edit the script before it runs, or substitute `git`. It cannot sign without the passphrase unless the passphrase is stored where it can read it (Q3) or it can read the encrypted key and guess the passphrase. That residual is the dated trusted-contributor posture (`bootstrap/REANCHOR_RUNBOOK.md:339`).
* **S6. What does signing add?** A key use at the end of a script. The script does not hold the key or the passphrase. What the signature means is limited: it says the key signed a commit the roster allows, not that the Maintainer read anything. The reading is his yes, and the script's recorded step.

**What the targeted Security Review must read.** (1) The signing step: the environment, the terminal requirement, the verification against the previous anchor's roster, and the claim in "In plain terms" about the passphrase. (2) The whole-ceremony orchestration: what the script passes to the launcher, how the digest reaches stage 2 after the yes (the driver does the same after its question), the order of the AST commit and the candidate, `--first-run`, and the import of the driver's helpers under step 4. (3) The yes-or-no variation against SR-3.

### Signals the change is wrong

* A chunk exceeds its budget; stop at `status`.
* The Maintainer finds a summary unreadable, or the yes becomes a reflex typed without reading.
* A refusal fires on ordinary runs twice in a row.
* Any way for two different outputs to carry one digest.
* A signing form is found that signs with no human present on the script's route.
* He says the passphrase is stored where a program can read it (Q3); the claim must then be reworded.
* The first real run takes much longer than he can carry out in one sitting (unmeasured; he says).

### Questions for the Maintainer (each has a default; none blocks)

* **Q1. Two summaries when an AST pin is owed?** Default: yes, two, because the second cannot exist until the first pin is committed. The alternative is to commit the pin first with no question, then show one summary. That asks him to bless a pin he has not read.
* **Q2. One key for both your release signing and the anchor?** `SECURITY.md:193-197` says the ceremony key should do nothing else. The roster holds only your key, and adding a second is a change to an authority file, so a transition ceremony. Default: keep one key and record the departure. The signing route does not use the agent, so a loaded key is not the hazard the rule guards against. The remaining cost is that signing a tag or a commit with this key also exposes it to those uses.
* **Q3. Is the key's passphrase stored in the macOS keychain or a passphrase helper?** Only you know. Default: assume not. If yes, the passphrase is not a control, and I will say so in the text.
* **Q4. May the script commit the AST pin, and may it ever push?** Default: it commits the AST pin's paths after your yes, unsigned, and never pushes. It prints the push line. `AGENTS.md` puts pushing with you.
* **Q5. Do you have a current values file and a current packet-and-launcher pair?** I cannot tell from here. Default: the script's first screen says so, and producing a pair stays an out-of-band review, outside this proposal.
* **Q6. The first ceremony.** Default: the AST pin by hand once more, then `ceremony --first-run` at the 0.5 cut, with the manual diff check recorded. Alternative: an earlier ceremony of your choosing.
* **Q7. Remove `drive()` and `--run` from `scripts/reanchor_ceremony.py` at R6?** Default: yes. Two ways to run the ceremony, one without the signing control, is the kind of thing this proposal removes.
* **Q8. The launcher template as the eleventh authority file.** Not mine to cut: the 2026-08-28 note made it an acceptance criterion. It weighs more now that the script calls the launcher. Default: its own proposal with its own Security Review, soon. Say if you want it folded in; that widens scope again.
* **Q9. Do you allow the reductions in the Scope delta below?** Default: allow, each as listed. Neither I nor a reviewer can concede them.

### Scope delta

**Scope delta**: degraded, and widened by the Maintainer. Only he concedes a row (Q9).

**Widened, by his own direction (quoted above):** the whole ceremony is in scope. The key-ceremony integration that Revision 1 deferred (its Q7) is now built. This is an addition, not a reduction, and owes no disposition.

**Carried, no delta:** the transaction and its safe write, the SR-1 reading order, the SR-2 rule that no `repin` path writes the manifest, SR-4's extraction, the provenance listing from file history, the per-chunk budget.

Reductions still standing, or new:

* The typed 12-character code. Now a yes or no, plus the passphrase. **disposition**: accept. His direction asks for a passphrase and a yes or no.
* The note's "signed tree, dedicated ceremony key, typed confirmation at the anchor tier". The signed checkpoint is carried (the existing stage 2). The dedicated key is not built (Q2). The typed confirmation of the digest is not carried: the script supplies the digest after his yes, as the existing driver does. **disposition**: defer the dedicated key; accept the rest.
* The driver's three questions ("Run stage 1 now?", "Does the report describe what you intend to bless?", "Ready for stage 2?"). Now one or two summaries. **disposition**: accept.
* The driver's rehearsal. Not run; stage 1 makes the same checks. **disposition**: accept.
* The note's "launcher template joins the closure". Not built here. **disposition**: defer (Q8).
* The note's "every ceremony disclosure forwarded, one control test per disclosure". Now carried for the tools the script calls, including the driver's helpers, the artifact and the launcher; not for the checker's internal messages the launcher does not print. **disposition**: accept.
* The note's "cut the second values parser" belongs to the launcher tier. **disposition**: defer (Q8).
* The note's "risk or volume trigger". Not built; nothing runs `status` unprompted. **disposition**: defer. The review budget is the per-chunk size budget.
* The note's "the modification-staleness silence is gone". Visible on demand only. **disposition**: accept.
* The note's "the runbooks shrink to a page each". Only the AST runbook shrinks. **disposition**: defer.
* The note's "the previous pin covers the tool that moves the next one". True only after the first ceremony that pins `repin`. Carried, delayed.
* The two-program double hash for the AST pin. One digest plus the optional replay; the ceremony keeps the double hash the driver already has. **disposition**: accept.
* The deletion of the old launcher in `~/Downloads`: a machine-local file I cannot verify; I do not rely on it.

### Assurance path

**Assurance path**: high-assurance, unchanged. The header declares `usual + Security Review` and the plan `required(Internal + Internal Security Review)`. Signing is a new trust-ceremony surface, and the whole-ceremony scope is new material. A short targeted Security Review reads the three things listed under "Security preflight". SR-1 to SR-4 are kept; the manifest writer stays out. I wrote no review.

### Withdrawn / superseded commitments

* **The scope "routine re-pins" and "gate-manifest pins stay in the ceremony, which is not here."** Replaced by the whole ceremony in one script. Why: the Maintainer's direction.
* **"Three acts per pin" and the per-pin table in Revision 1.** Replaced by one command, one or two yes answers, one passphrase and the push. Why: his direction; the ceremony is now in scope.
* **The 12-character typed code, and `apply` as a verb.** Replaced by yes or no inside `ceremony`; the write happens after the yes. Why: his direction, and the Security Review's finding that the code is confirmation, not authentication.
* **`package` printing a code "for the replay comparison only".** Replaced by `package` printing the transaction digest. Why: the code is gone.
* **"I do not change the key steps (RA-16, RA-18, RA-19), because they belong to the ceremony driver, not to `repin`."** Withdrawn. The script now runs them: it makes the key reach the signer by a route that always prompts, runs stage 2, verifies, and prints the push line. Why: his direction.
* **Reading-order step 4's list without the driver.** Extended by `scripts/reanchor_ceremony.py`, and `ceremony` and the AST write refuse until the anchor pins `repin`'s files, except under `--first-run`. Why: the script now imports the driver's helpers.
* **"The first pin that includes `repin` is a key ceremony, with one manual diff check."** Kept in substance, now with `--first-run` and the AST pin by hand once more. Why: the whole-ceremony scope.
* **Chunk numbering R1 to R5.** Re-cut to R1 to R6: the ceremony is R4, the lockfile R5, retirement R6. The budget gains a line for R4. Why: the widened scope.
* **Revision 1's Q1 to Q10.** Replaced by Q1 to Q9 above. Revision 1's Q1 (replay), Q2 (provenance), Q3 (closure refusal), Q4 (lockfile), Q5 (budget), Q6 (name) and Q10 (classification split) are now stated decisions inside the contract, not questions. Why: they are my calls; the Maintainer can still reverse them.
* **Revision 1's Q9, "which part of the ceremony is too complicated: the commands, knowing what to check, or the key?"** Answered by his direction: the commands and the key. Why: he answered it.
* **The driver's `--run` path as a way to run the ceremony.** Superseded; removed at R6 (Q7). Why: one way, with the signing control.

## Security Review (second round) -- Claude Opus 5.5 -- 2026-10-26

**Obligation**: show that the one step Revision 2 calls human, typing the passphrase, cannot be done by a program on the script's route or around it; that every byte the script trusts before that step traces back to something a same-user process cannot quietly rewrite; and that each yes binds the bytes it is said to bless. Where none of that can be shown on one machine and one user, show that the text says so.

```
Reviewed commit: 6bf381c8 (`git diff 6bf381c8 -- <this file>` was empty before this pass; every other file I cite is byte-identical at 6bf381c8 and in the working tree)
Target: Revision 2 only -- the signing step, the whole-ceremony orchestration, the yes-or-no variation, the same-user residual
Prior findings: SR-1 to SR-4 checked below, one line each; SR-5 to SR-8 not re-read
Assurance path: high-assurance
```

**Tier**: Security Review (second round, scope widened by the Maintainer)
**Findings**: raised (5 blocking, 1 non-blocking)
**Verdict**: REVISE. This Security Review does not clear at `6bf381c8`. It clears on conditions: the five blocking fixes below, each a few sentences of contract text and one or two tests. Nothing here asks for a redesign.

**In plain terms.** The signing route works as the author measured: with the key out of the ssh agent, the signer asks once for the passphrase, and with no answer nothing is signed. But the terminal is not what protects you. Any program that knows the passphrase can sign with no terminal at all, or with a fake one. So the passphrase is the only control, and it holds only while four things are true: the key is in no agent, the passphrase is stored nowhere, the key file is encrypted, and the program asking you for it is the reviewed one. You answered the second ("No, I type it every time"). The script can check the first and third, and should refuse rather than warn. The fourth no script can check on its own machine; the text must say so. Separately, the script trusts the anchor before checking its signature, and the anchor today is unsigned, 397 commits after the last signed one. The script should check the signature, and say plainly that the first ceremony starts from an unsigned base.

**Foundations**

1. **Should this happen as framed?** Yes. One committed script with one passphrase prompt replaces the driver's advice to load the key, which my probes show lets any program you run sign (`scripts/reanchor_ceremony.py:636-641`; probes P1, P13). The route itself holds: one prompt, signed; no answer, no signature (P4).
2. **Best alternative.** The same script, with "names a loaded key" turned into "refuses", an encrypted-key check, the anchor's signature checked before the anchor is used, and the passphrase claim restated as the only control (SR2-1 to SR2-3). I found no simpler route that removes a human step without removing the control.
3. **What would show it wrong.** A signature with no person present on the script's route. I found none without the passphrase or a loaded key. With the passphrase known, a stdin pipe or a fake terminal is enough (P6, P7); with the key loaded, removing the socket variable does not cut it off (P13, and `launchctl getenv SSH_AUTH_SOCK`).

**Earlier conditions, still met?**

* **SR-1:** met, except that the hashed list in reading-order step 4 no longer includes `scripts/repin.py` itself; Revision 1's list did. Presence of an anchored entry is not equality (SR2-5).
* **SR-2:** met. No `repin` path writes `gate_manifest.json`; the launcher's stage 2 does, and the Tests list keeps the blob-id test.
* **SR-3:** varied. The render is still made from the in-memory bytes and the "every changed key is on screen" test stays; the typed code becomes a yes. Ruled on under question 3.
* **SR-4:** met (reading-order step 3, and the untracked-module and moved-`HEAD` tests).

### Probes

Python 3.13.13 (`/Users/kendal30/conda_envs/lhm/bin/python3.13`), OpenSSH_10.3p1 (Apple's `/usr/bin` build, LibreSSL 3.3.6), git 2.53.0. All probes ran in an empty scratch folder with `HOME` set to it, `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL` a scratch file, a throwaway ed25519 key with a passphrase I chose, and my own ssh-agent; the folder and agents were removed afterwards. I never read, opened or used `~/.ssh` or the real key, and no probe ran in the shared checkout. "No terminal" means a new session with no controlling terminal. "Terminal" means a pseudo-terminal my harness drove. "Ceremony form" means `git commit-tree -S -F -` with the message on a pipe and the key named per call, as `bootstrap/tests/_gate_preflight.py:2630` does.

| # | Setup | Result |
|---|---|---|
| P1 | Key in agent, no terminal: `ssh-keygen -Y sign`, and the ceremony form | Both signed, no prompt (the author's row, reproduced) |
| P2 | Agent cut, no terminal, stdin closed, both forms | No signature |
| P3 | Agent cut, `SSH_ASKPASS` plus `SSH_ASKPASS_REQUIRE=force` | Signed, no person |
| P4 | Agent cut, terminal, ceremony form | 1 prompt, signed after the answer; unanswered, no signature |
| P5 | `SSH_AUTH_SOCK` set but empty, key loaded, terminal, ceremony form | 1 prompt, signed: empty acts like unset |
| P6 | Agent cut, **no terminal**, passphrase on a stdin pipe | Signed. The signer falls back to stdin when it cannot open a terminal |
| P7 | Fake terminal from `script -q /dev/null`, run from a session with no terminal, passphrase written by a program | Signed. Control: a wrong passphrase, exit 255, no signature |
| P8 | Agent cut, no terminal: `SSH_ASKPASS` alone; `DISPLAY=:0` alone | No signature, each |
| P9 | Agent cut: `DISPLAY=:0` plus `SSH_ASKPASS`, and `WAYLAND_DISPLAY` plus `SSH_ASKPASS`, no `REQUIRE` | Signed, no person. With a terminal present too: 0 prompts, signed |
| P10 | Terminal, ceremony form, `DISPLAY=:0` alone | 0 prompts; failed naming `/usr/X11R6/bin/ssh-askpass`. Control, no `DISPLAY`: 1 prompt |
| P11 | Unencrypted key, agent cut, no terminal | Signed, no person |
| P12 | `ssh-keygen -y -P '' -f <private key>` | Exit 255 on the encrypted key, 0 on the unencrypted one; no prompt either way |
| P13 | Socket variable removed, then its path found by listing the folder | Signed, no prompt |
| P14 | Key added with `ssh-add -c`; the agent started with a confirm helper that says yes | Signed, no person |

Reads, not probes: `launchctl getenv SSH_AUTH_SOCK` returns a path of the form `/var/run/com.apple.launchd.<random>/Listeners` to any process of this user (I did not connect to it). `strings /usr/bin/ssh-keygen | grep -ci keychain` gives 0; `strings /usr/bin/ssh-add` contains `keychain_read_passphrase`. So on this machine the keychain reaches the key through `ssh-add`, into an agent, and not through the signer.

### Answers to the four questions

**1. The signing step.** *Plain answer:* the route closes the no-person paths that run through the signer's environment, and nothing else. It should refuse a loaded key, not name it.

* *What holds.* With the agent cut, the ceremony form prompts once and signs only on the right answer (P4, P5). Stage 2 makes one signing call by reading (`bootstrap/tests/_gate_preflight.py:2630`), so one prompt per run is what I expect; I measured one call, not a whole stage 2. The launcher starts the checker with `env -i` and three variables (`bootstrap/reanchor.sh:658-662`), so no helper variable reaches the signer through it.
* *`DISPLAY`.* Alone it is not a no-person path (P8), but it breaks the route: with a terminal present and the message on a pipe, the signer skips the terminal and fails on the missing `ssh-askpass` (P10). That is the failure `bootstrap/reanchor.sh:380-382` and `:619-622` blame on "no controlling terminal"; P10 shows `DISPLAY` produces it with a terminal present. I cannot tell which caused the 2026-08-19 failures. `WAYLAND_DISPLAY` works like `DISPLAY` (P9), and the author's list of four variables misses it. That is harmless only while `SSH_ASKPASS` is also gone. Build the signer's environment by naming what it keeps, as the launcher does, never by naming what it drops.
* *The terminal is not a control.* The signer reads a passphrase from stdin when there is no terminal (P6), and a fake terminal takes one from a program (P7). Requiring a terminal keeps the prompt visible to you. It does not keep a program out.
* *A loaded key.* Removing `SSH_AUTH_SOCK` from one environment does not cut the agent off from other programs: a same-user process finds the socket another way (P13; `launchctl` hands out the default agent's path). Stage 1 runs candidate code as you, and the checker's own probe drops the socket before probing (`bootstrap/tests/_gate_preflight.py:2201`), so it cannot see a loaded key either. With the key loaded during stage 1, candidate code can sign an anchor-shaped commit with no prompt (P1). Hence SR2-1: refuse.
* *`ssh-add -c`.* Not a control against your own user: whoever starts the agent picks the helper that confirms (P14). The design need not use it.
* *Keychain or helper (Q3).* Answered by the Maintainer on 2026-10-26, through the planning session's question, relayed to me by the coordinator: "No, I type it every time". This is his statement; I did not and could not measure it without touching his key. Had the answer been yes: with the keychain, any process could run `ssh-add --apple-load-keychain` and load the key with no prompt, so the passphrase would be no control at all; with a helper, any process could run the helper itself.

**2. The orchestration.** *Plain answer:* hashing the driver against the anchor shows only that the driver equals what the anchor ref names. Today that ref names an unsigned commit that any process running as you could have written. The trust has to start somewhere a same-user process cannot rewrite unseen. In this design that is two places: the launcher's digest, which the out-of-band review records and you compare, and your passphrase.

* *Where trust starts.* The launcher's header says what you verify: "the launcher's digest, which the review already records" (`bootstrap/reanchor-launcher.template.sh:18-21`). The launcher then checks the packet, and the packet pins the ten authority files, `bootstrap/reanchor.sh` and the allowed-signers roster among them (`bootstrap/tests/_gate_preflight.py:600-626`). Revision 2's five steps for the Maintainer leave that comparison out (SR2-3).
* *The anchor is trusted before it is checked.* Nothing in the existing ceremony reads the previous anchor's own signature: the signature census covers `anchor..head` only, which excludes the anchor itself (`bootstrap/tests/_gate_preflight.py:1218`), and is diagnostic. I searched `_gate_preflight.py`, `reanchor.sh` and the driver for `verify-commit`, `%G?` and `gpgsig`; the search matched the census and the new-commit check (`:2675`), so it could have matched an anchor check, and found none. Reading-order step 4 and verification step 6 then take the frozen-file digests and the roster from that object. Measured: the last anchor that verifies is `bd66a70c` (`G`); `6f29519d` (`N`) is 397 commits later and changes the manifest by 2247 insertions and 230 deletions (`git rev-list --count`, `git diff --stat`).
* *Unchecked execution outside the launcher.* `validate`, `show-report` and `hash-package` run `bootstrap/reanchor.sh` from the working tree, outside the launcher's checked extraction. The driver compares that file with the packet's row before running it (`scripts/reanchor_ceremony.py:553-564`). `repin` does not use `drive()`, and Revision 2 does not carry that check, so the bytes that render Summary 2 would be checked only against the unsigned anchor (SR2-4).
* *What the first run proves.* That the reviewed `repin` bytes (if the manual `git diff` prints nothing) drove a ceremony whose new anchor verifies as signed by the roster key, and that from then on the anchor pins `repin` and the driver. *What it cannot prove.* That `6f29519d` is what you meant to bless, that nothing ran between the review and the run, or that you read the summaries. The first signed anchor blesses everything since `bd66a70c` that the packet does not pin, so the first screen must say so (SR2-3).

**3. The yes-or-no variation.** *Ruling: acceptable on conditions.* The typed code was confirmation, not authentication (pass 1's probe 2), so a yes loses nothing a program could not already supply. What the yes must bind is the bytes, through a digest printed under what you read. Then the record says which bytes a yes was typed against. The conditions:

* **Summary 1.** The render and the write come from one in-memory copy in one process, as Revision 2 says. The transaction and render digests are printed under the render, above the question. After the commit, the script checks from the commit object that only the named paths changed and that their blobs equal the bytes shown (SR2-6a).
* **Summary 2.** The package is hashed before `show-report` and again after the yes, and the script refuses if the two differ. That digest is printed under the report and is the one passed to stage 2. `show-report` runs only after its bytes match the packet (SR2-4).
* **If the report and the bytes could differ,** the yes binds nothing and the script must refuse. Under these conditions they can differ only through a same-user process swapping files inside the show window and swapping them back, which is question 4's residual.
* **The record.** Only the word `yes` counts. Anything else, end of input or a closed terminal counts as no. The commit body says "yes typed on a terminal", never "confirmed by the Maintainer" (SR2-6d).

**4. The same-user residual.** *Plain answer:* nothing in the design stops a process running as you from driving `ceremony` up to the passphrase prompt. A fake terminal gives it the yes answers (pass 1's probe 2) and the terminal check (P7). What stops it there is only that it does not know the passphrase. If his answer holds, his passphrase is stored nowhere such a process can reach; with the key out of the agent, the fake terminal has nothing to type, and a wrong guess signs nothing (P7's control). The agent here did not hold the signing key when the author checked today.

* *What a same-user process can still do.* (a) If the key is loaded at any time, sign anything during that time, with no prompt (P1, P13). (b) Change what runs, so that the passphrase prompt you answer comes from its program, not the reviewed one: `scripts/repin.py` in the working tree, the executables your values file names, your shell's startup files. It then keeps what you type and can sign later, with no person. Nothing on one machine and one user stops (b); the next reviewer of a changed `repin` and the launcher digest you compare narrow it. (c) Copy the encrypted key file, which every process you run can read, and guess the passphrase offline; a strong passphrase is the defence (not measured). The proposal's S5 names (a) and guessing but not (b); SR2-2 adds it.
* *What still depends on your habits.* (1) Never load the signing key into an ssh agent, at any time, including to sign a release tag (v0.4.0 is signed with this key; Q2 keeps one key). SR2-1 turns this into a refusal during a run but cannot see other times. (2) Never store the passphrase: no keychain, helper, file or environment variable. (3) Type it only at the one prompt that follows the second yes; any other passphrase prompt in a run means stop. (4) Keep it long. (5) Compare the launcher's digest with the review's record (SR2-3).
* *What that means.* The signature says the key was used with the passphrase; it says a person was present only while (1) to (3) hold and nothing has replaced the program that asks. That is the trusted-contributor posture already dated in `bootstrap/REANCHOR_RUNBOOK.md` ("The dated posture, and what ends it"), now stated for the signing step. It defends against an agent acting while you are away. It does not defend against one that has turned against you and edits the tools you run.

**Claims sample.** I checked 14 of Revision 2's claims, chosen as every citation and measurement the signing step and the orchestration rest on, plus the cheap counts beside them. Matched: the driver's 774 lines and its run sequence at `scripts/reanchor_ceremony.py:546-676`; the "either way works" advice at `:628-641`; `reanchor.sh:655-662` forwarding an empty socket; the per-call key at `_gate_preflight.py:2624-2631`; the probe at `:2204-2211` keeping the terminal (by reading); no test naming the driver (0 files; the same grep finds 3 for `reanchor.sh`); the anchor manifest listing the driver; the reflog's five entries (`N`, `G`, `U`, `U`, `U`); a one-line roster; `SECURITY.md:193-197`; the builders at `test_reanchor.py:959-1025`; and the whole signing table (P1 to P5; P1's git row first failed in my harness only because my socket path was relative to another folder, and signed once the path was reachable). Did not match: the reading-order list, which dropped `repin` itself (SR2-5). Partly answered: "DISPLAY needs clearing" (P10). Not re-checked: the provenance figures (69 of 124) and Q5's state.

### Findings

**SR2-1 (blocking). Refuse a loaded signing key, look where other programs look, and refuse an unencrypted key.** *Fix:* before stage 1 and again before stage 2, ask both the agent `SSH_AUTH_SOCK` names and the one `launchctl getenv SSH_AUTH_SOCK` names, with `/usr/bin/ssh-add -l`, and refuse if either holds the roster key's fingerprint, printing the exact `ssh-add -d <key>.pub` line. "Could not ask" is shown, not refused. Also refuse if `/usr/bin/ssh-keygen -y -P '' -f <private key>` exits 0 (P12), run with no terminal and stdin closed. The script reads the key file only to learn whether an empty passphrase opens it. *What is lost:* nothing the route uses. *Closed when:* the proposal says so, and tests show a key loaded in a scratch agent refuses before stage 1 (control: unloaded passes), a key in a second agent reached only through the injected lookup refuses (control: absent passes), and an unencrypted key refuses (control: encrypted passes). *Clears once answered so:* yes.

**SR2-2 (blocking). State the passphrase as the only control, with four conditions, not three.** "In plain terms" and S5 say the passphrase is a control if three things hold, and treat the terminal as part of the route. *Fix:* say the terminal keeps the prompt visible and is not a control (P6, P7); list the four conditions (key in no agent; passphrase stored nowhere, his answer recorded with its date; key file encrypted; the program asking is the reviewed one); add S5's item (b). Just before stage 2 the script prints "you will be asked for the passphrase once, now; if asked at any other point, type nothing and stop". *Closed when:* the text says so, and a scratch-ceremony test on a pseudo-terminal counts exactly one prompt with the key unloaded (control: with the socket left in, zero prompts). *Clears:* yes.

**SR2-3 (blocking). Start the trust where a same-user process cannot rewrite it unseen.** *Fix:* (a) the first screen prints the launcher's SHA-256 and asks you to compare it with the digest the review recorded; add this to "What the Maintainer does". (b) Before reading-order step 4, verify the anchor commit with sterile git against the roster whose SHA-256 equals the packet's allowed-signers row. Anything but a good signature by that key refuses, except under `--first-run`, which instead shows: "the comparison base `<id>` is unsigned; the last signed anchor is `<id>`, `<n>` commits earlier; what this ceremony blesses since then rests on the launcher digest you compared". (c) Step 6 verifies the new anchor against that same packet-pinned roster. *What is lost:* nothing; today's base is shown, not refused, on the first run. *Closed when:* the proposal says so, and tests show an unsigned anchor refuses without the flag (control: a signed one passes), an anchor signed by a key outside the roster refuses, and a roster differing from the packet's row refuses. *Clears:* yes.

**SR2-4 (blocking). Check every working-tree script before it runs, and bind Summary 2's yes to a digest.** *Fix:* before each direct `reanchor.sh` call (`validate`, `show-report`, `hash-package`), hash the file and compare with the packet's `artifact_sha256` row, as `scripts/reanchor_ceremony.py:553-564` does. Run a private copy of exactly the hashed bytes. Hash the package before `show-report` and after the yes, refuse on a difference, print that digest under the report, and pass it to stage 2. *Closed when:* the proposal says so, and tests show an artifact differing from the packet refuses before `show-report` runs (control: a match passes) and a package rewritten between the report and the yes refuses (control: unchanged passes). *Clears:* yes.

**SR2-5 (blocking). Put `repin` itself back in the hashed list.** The SR-1 list named it; Revision 2's step 4 checks only that an entry exists. *Fix:* hash `scripts/repin.py` with the others. When its bytes differ from the anchored entry, absent or changed, `ceremony` runs only in first-run mode with the manual `git diff` against the commit the code review named. `--first-run`'s condition becomes "entry absent or different", so a later change to `repin` is pinned by a ceremony it did not vouch for itself. *Closed when:* the text says so, and a test shows an edited `repin.py` refuses `ceremony` without the flag (control: anchored bytes pass). *Clears:* yes.

**SR2-6 (non-blocking; the plan's Security Review checks these).** (a) The AST commit goes through sterile git with hooks off, and is checked from the commit object: only the named paths changed, and their blobs equal `git hash-object --no-filters` of the bytes shown. On a mismatch, refuse and print the undo line without running it. (b) The launcher's stage-2 banner and its no-socket note tell you to `ssh-add` (`bootstrap/reanchor.sh:651`, `:630`). The script must print, before stage 2 and after a stage-2 failure, that this advice does not apply here, and never relay "load it and re-run" as the next step. Changing the banner itself is a closure change. (c) Call `/usr/bin/ssh-keygen` and `/usr/bin/ssh-add` by absolute path; the driver's helpers resolve them through `PATH` (`scripts/reanchor_ceremony.py:498`, `:518`). (d) Only the word `yes` counts. Anything else, end of input or a closed terminal counts as no. The record says "yes typed on a terminal".

**Clearing.** This Security Review does not clear at `6bf381c8`. It clears on conditions: the author's next Response adopts SR2-1 to SR2-5 as stated, or alternatives that meet each "Closed when" line. A third proposal-stage pass is not needed for that; the Maintainer at the Decision and the plan's Internal Security Review check that they are carried. It would be needed only if the Response changes the signing route or the trust root itself. SR2-6 goes to the plan. Following the template ("A review moves a proposal to `revising`"), I set Status to `revising`.

**Coverage line.** I am confident in the probe results above: each ran with a control. I did not run the real launcher, stage 1 or stage 2, under a pseudo-terminal or at all; "one prompt per run" rests on one signing call read at `_gate_preflight.py:2630` and on P4. I did not test the keychain: that would change your keychain. "The signer does not read the keychain" rests on `strings`, not on a run. I did not connect to the default agent's socket, read your key's encryption rounds, read `reanchor.sh`'s `show-report` and `hash-package` bodies, re-measure the provenance figures, or test on Linux. I ran no test from the suite and never set `CAIRN_FULL_SUITE`.
