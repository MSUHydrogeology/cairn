# Trim the templates, testing text and collaboration guide; list the rules that apply

**Author**: Claude Sonnet 5.5 (claude-sonnet-5-5)
**Status**: awaiting-decision
**Review**: usual + Security Review (until the accepted template-scan change lands; then usual only, plus Security Review for the `board.py` part)
**Proposed tier**: heavy — it rewrites both authoring templates and the shipped always-loaded files, and adds a code warning to a shipped `.py`; the Maintainer sets the tier
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-16
**In brief**: Shorten the text agents must read to start any task, and make each proposal and plan name the few rule files that apply to it.

## Decision summary

An adopter reads about 7,200 words of guidance to do one task, and the v0.7 `AGENTS.md` trim moved bulk into other files instead of removing it. This proposal sets a target length for each bulky file (table below), moves detail agents do not need to run to documentation, and rewrites what stays shorter. It adds one header line, `**Rules that apply**:`, to the proposal and plan templates, and folds the plan's Dispositions section into the closeout record. Cost: adopters who edited these files meet merge conflicts at upgrade. Rules-folder guidance and the run-versus-develop split are follow-ons (items 7 and 8).

## Context

Words counted with `wc -w` at commit `3e4375a6`, 2026-11-16 (re-measured after review; the first draft used `3ec301a9`). Targets are my proposal; the Maintainer sets them.

| File | Cairn copy | Shipped copy | Target (shipped; Cairn's = shipped plus its slots) |
|---|---|---|---|
| Plan template | 4,859 | 4,871 | 3,900 |
| Proposal template | 4,599 | 4,275 | 3,400 |
| Testing-discipline module | 2,134 | 2,134 | 1,400 |
| `dev/agent_collaboration.md` | 6,190 | 6,116 | 4,800 |
| `AGENTS.md` | 945 | 1,125 | no growth |
| Vendor wrapper (`VENDOR.md`; Cairn's `CLAUDE.md`) | 362 | 310 | 170 |
| `RULES.md` | 181 | 60 | no growth |

The three always-loaded files total 1,488 for Cairn (cap 2,000, a written rule, no test) and 1,495 shipped (cap 1,500, held by `bootstrap/tests/test_scaffold.py`). The shipped set sits 5 words under its cap, so any rule added to it needs room first. Maintainer, 2026-11-10: "There simply aren't 5000 words worth of instructions needed to develop in this repo. That is just bloat."

## Proposal

**1. The trim.** Detail a person needs to understand the method but an agent does not need to act moves to documentation (the plan names each destination). What stays is rewritten shorter. Boundary A, B and C, the model capability floors, every refusal and every Maintainer-only step (for example, that only a matching Obligation pass clears an Internal Security Review) keep their full force; only background explanation moves. No operative rule may leave the text agents load, here or in an adopter's install, without the Maintainer's quoted word. Text moved out of a loaded file must land where the same audience receives it: for adopters, a shipped file, never Cairn's own `docs/` (it does not ship). The rewrite starts with the Boundary A, B and C and testing text, because it drives test-building. About 145 of the wrapper's 310 words are notes to the person renaming it; they go.

**2. Constraints** (from the board). The templates must not grow. No test may pin the wording of the result; the plan finds and deletes such tests first, as the `AGENTS.md` trim did. The caps above stand.

**3. `**Rules that apply**:`.** Both templates gain this header line. It lists rule file paths picked from the `RULES.md` routing table, never rule text, or `bright lines only`. A rule that applies but is unlisted is still followed and added to the line. The line never narrows a review, a Security Review trigger or a protected-surface obligation, and an adopter's routing table starts empty. Reviewers compare the line with Scope. About 20 words, paid from the trim. Maintainer, 2026-11-12: "I like all of this."

**4. Dispositions.** The plan template's `## Dispositions` section folds into the closeout record: every "not run, not covered or remaining" line carries a Home (a roadmap row, an issue, a proposal or the Maintainer's quoted word). An empty Home means the plan is not ready to archive. `tools/board.py` (copied byte for byte to `templates/skills/_lib/board.py`) gains one advisory warning for a `ready-to-archive` plan with such a line and no Home. It warns and does not block, writes to stderr only (never into `--json` output), reads plans only through the existing artifact readers, prints only the file name and line number, escaped and bounded, and caps the count. Both copies stay byte-identical, held by a new test. A deferral of accepted scope or of a required check has the Maintainer's quoted word as its Home. A Home an agent creates alone (an issue or a roadmap row) is enough only for a follow-up that defers no accepted scope and no required check. The `wontfix` limits (not allowed when the item reaches an adopter, blocks a release or needs a Decision) and the rule that a `guard` must be a check that runs stay.

**5. Testing rules.** From #77: a test not clearly a public promise is not kept, and a higher-tier agent decides judgment calls. Exempt, and cut only through Security Review: protected surfaces, the security-family test files and native-only IDs in `bootstrap/tests/security_manifest.py`, tests a release document, `SAFETY.md`, `SECURITY_MUTATIONS.md` or a shipped file names as a guard, and refusal, hostile-state and negative-guard tests. Cairn's list lives in `dev/rules/protected-surfaces.md`; the testing-discipline module gets the generic form ("tests your project's release or security records name as guards, and refusal and negative-guard tests"), pointing at the project's own high-risk list in its `AGENTS.md`. That module is team-gated, so adopters without it get no cut rule at all. From #86: test time has an owner and a review cadence for the slowest files. From #88: each new test runs once on a clean checkout. From #81 and the grown-projects note, the principle only, not the record tool: a large project is not one piece, so test each part where it lives, and a change may be verified from current results in place of a whole-suite run. A release's own whole-suite and security-family run is never replaced by earlier results; a release run may reuse results only where a reviewed rule allows it. Each lands as a sentence inside the rewrite.

**6. Appendix (#73).** Default none. Allowed only for a table or arithmetic a reviewer must check that no cited record can hold, as one separate file per proposal, never inline. The 1,000-word budget applies to the text at the Decision, so review additions are cut or moved before it. The plan settles naming (#73 suggests `<stem>--appendix.md`) and board handling.

**7. Rules-folder guidance (#70; entry shape, applicability line, size budget, how a rule enters and leaves).** Not delivered here: it is the first staged module in the companion draft `dev/proposals/2026-11-16-claude-staged-modules-and-triggers.md`, because it needs a trigger design and would add words to files this proposal shrinks. Delivered here: one sentence in the `dev/rules/README.md` shipped with every install, that a Maintainer's rule goes in the rule file with approved wording, never only in agent memory (#70). The companion also edits that README, so the plan orders the two edits.

**8. #74, #76, #79 (run rules apart from development rules; an Operator role; a project-wide `AGENTS.md` entry with pointers into `dev/rules/`).** Recommend a separate follow-on proposal, opened after this one lands. Reason: they change what the always-loaded entry file and the role table mean, not only how long they are, and a reviewer cannot judge a rewrite and a restructure of the same text in one pass. Cost of splitting: an adopter who edited `AGENTS.md` merges twice, though each merge is smaller. Cost of including: one larger conflict (the 2026-11-11 trial found a one-word edit inside a removed paragraph made 93 of 206 lines conflict, and `--apply` refuses until resolved), a heavier review, and a risk that the restructure delays the trim.

## Rationale

Folding Dispositions leaves one closing section, and catches what a review of 11 archived plans found: nine had no Dispositions section.

## Alternatives considered

Do nothing: the load stays and Dispositions keep escaping. Copy rule text into plans: copies drift. Include items 7 and 8: costs above.

## Documentation / doctrine surface

Both templates, the testing module, the collaboration guide, the vendor wrapper, `dev/rules/README.md`, `tools/board.py`. Removed detail lands in `docs/`. A Claude Code project no longer needs a `CLAUDE.md` (2026-11-16 amendment to the repository-layout proposal), which leaves open whether `VENDOR.md` stays. This proposal trims its notes and decides nothing about its fate; if the layout plan removes it first, that line is moot.

## Evidence / verification plan

Word counts per file against the table, by `wc -w`. The plan lists replacements rule by rule, each marked kept, shortened, moved (with destination) or deleted (with reason), so a reviewer can answer "Does any rule weaken or disappear?" row by row. For the proposal as a whole: yes, explanatory wording shrinks by design (detail moves out of loaded text), no security fence or refusal may weaken, and none may disappear. Each ledger row names the rule's new home and marks it shipped or Cairn-only; a rule moved out of loaded text must land where the same audience receives it. Tests: the board warning gets one test through `tools/board.py` with a plan that has a Homeless line and one that has a Home; a `--json` run proves stdout stays clean; a hostile-text plan proves the printed text is escaped and bounded; a byte-identity test compares the two copies of `board.py` (a grep of `bootstrap/tests` found none). The plan's upgrade note tells adopters to move their own rule lines into `RULES.md` before upgrading, because taking Cairn's new text loses an added line. Not checked: how many tests pin template wording; the desktop app's `AGENTS.md` behavior.

Tier and lane. Templates and `AGENTS.md` are high-risk surfaces today, so usual + Security Review applies now. If the accepted template-scan change lands first, prose-only template edits leave the list; the `board.py` copy and any `.py` under `templates/` stay protected. Upgrade: templates and `AGENTS.md` merge as files, so filled slots survive but edits inside rewritten paragraphs conflict.

**Security preflight**: N/A: no trust boundary added or widened; the warning only reads plan text.
**Independent scientific check**: N/A: no scientific assumption or result touched.

## Assurance path

**Assurance path**: high-assurance — touches an install-contract file an adopter executes (`board.py`) and the named high-risk templates.

## Review -- Gemini 4 Hydrogen (ordinary Reviewer, Medium) -- 2026-11-16

```
Reviewed commit: 401de278d48c72c490ecc0ae9d7b0b6aa33697dd
```

**Tier**: usual
**Findings**: raised
**Verdict**: ACCEPT

**Elapsed**: ~1m
**Tokens**: unknown

The proposal cuts always-loaded and template bloat without losing operative rules: it sets word-count targets, moves explanatory prose to `docs/`, routes project rules by path (`**Rules that apply**:`), folds `## Dispositions` into plan closeout with an advisory `tools/board.py` warning, and isolates structural changes (#74/#76/#79) to avoid compound adopter merge conflicts.

**Foundations**

1. **Should this happen as framed?** Yes — shipped always-loaded files sit at 1,495 words against the 1,500-word cap (`bootstrap/tests/test_scaffold.py:656`); `wc -w` on HEAD matches the table within 4 words (`dev/modules/testing-discipline.md` 2,134; `dev/agent_collaboration.md` 6,190; shipped `AGENTS.md` 1,125, `VENDOR.md` 310, `RULES.md` 60).
2. **Best alternative.** Bundle #70 and #74/#76/#79 here; rightly rejected, as #70 needs triggers (`2026-11-16-claude-staged-modules-and-triggers.md`) and restructuring during a rewrite compounds merge conflicts.
3. **What would show it wrong.** If the plan's rule-by-rule table drops or hides operative rules instead of moving only explanatory detail to `docs/`, or if `board.py` blocks instead of warns.

**Does any rule weaken or disappear?** Not in this proposal; it requires a rule-by-rule table in the plan so no operative rule disappears without a recorded reason, and keeps `**Rules that apply**:` as `RULES.md` path pointers.

1. **Non-blocking (plan-stage check).** Both this proposal (item 7) and `2026-11-16-claude-staged-modules-and-triggers.md` edit `templates/core/dev/rules/README.md`; coordinate order at plan time, and leave pointers where agents act on moved detail.

**Coverage**: Read the proposal, `dev/proposals/_template.md`, `RULES.md`, `templates/core/VENDOR.md`, `templates/core/dev/rules/README.md`, `2026-11-16-claude-staged-modules-and-triggers.md` (lines 1-65), `dev/plans/_template.md` (`## Dispositions`); verified `wc -w`, `bootstrap/tests/test_scaffold.py:656`, and `diff -q tools/board.py templates/skills/_lib/board.py`. Did not inspect archived plans for the 9-of-11 count, `tools/board.py` internals, or desktop-app `AGENTS.md` behavior.

## Security Review -- Gemini 4 Argon (Security Reviewer, High) -- 2026-11-16

```
Reviewed commit: 5de2a0662fb988b28710e15c4945d9a0811e428b
```

**Tier**: Security Review
**Findings**: raised
**Verdict**: ACCEPT

**Elapsed**: ~4m
**Tokens**: unknown

Obligation: Can shortening the templates and always-loaded files, adding `**Rules that apply**:`, or modifying `board.py` for plan dispositions weaken boundary enforcement, drop required security checks, or corrupt automated verification?

**Steelman.** The proposal safely addresses acute cap pressure on always-loaded guidance (shipped files sit 5 words under the 1,500-word cap) by trimming non-operative commentary while preserving all binding rules through an explicit rule-by-rule replacement ledger, adds declarative project-rule routing (`**Rules that apply**:`) that defaults to fail-closed, folds plan dispositions into the closeout record with an advisory warning in `tools/board.py` so unperformed checks cannot quietly escape, and cleanly defers structural role redesigns to avoid compounding adopter merge conflicts.

**Foundations**

1. **Should this happen as framed?** Yes — shipped always-loaded files total 1,495 words against the 1,500-word ceiling (`bootstrap/tests/test_scaffold.py:656`), leaving essentially zero room for new rules; `wc -w` at HEAD confirms the bloat (`dev/modules/testing-discipline.md` 2,134 words; `dev/agent_collaboration.md` 6,190; `dev/plans/_template.md` 4,859; `dev/proposals/_template.md` 4,599).
2. **Best alternative.** Do nothing or bundle structural role redesigns (#70, #74, #76, #79); rightly rejected, as doing nothing leaves always-loaded files vulnerable to immediate cap breaches, while bundling structural shifts into a textual diet compounds merge conflicts and obscures rule diffs (`dev/proposals/2026-11-16-claude-staged-modules-and-triggers.md`).
3. **What would show it wrong.** Any operative boundary fence (Boundary A, B, C), model capability floor, or refusal rule being deleted or weakened; `**Rules that apply**:` being treated as an exclusive waiver of unlisted security rules; `tools/board.py` polluting `--json` stdout; or unapproved deferral of required security checks into closeout (`dev/rules/protected-surfaces.md`, `tools/board.py:31`).

**Findings**

- *Blocking*: None.
- *Non-blocking*:
  1. **Plan-stage boundary preservation.** In the plan's rule-by-rule replacement ledger, the author must strictly distinguish between non-operative explanatory prose and operative rules: Boundary A (data governance), Boundary B (model capability floors and self-evaluation refusal), and Boundary C (vendor isolation) are inviolable security fences. The phrase in the proposal "some wording weakens by design" must only apply to moving background explanation to documentation, never to weakening the operational force, scope, or refusals of any security rule (`dev/agent_collaboration.md` > "Verification", `AGENTS.md`).
  2. **`tools/board.py` data stream integrity.** The advisory warning added to `tools/board.py` (and its byte-identical twin `templates/skills/_lib/board.py`) for plans at `ready-to-archive` with homeless remaining lines must write to stderr or human terminal formatting only; it must never emit warnings on stdout when invoked with `--json`, ensuring schema `cairn-board/1` remains machine-parseable without corruption (`tools/board.py:9-12`). Both copies must remain byte-identical (`diff -u tools/board.py templates/skills/_lib/board.py`).
  3. **Disposition home authority.** Folding `## Dispositions` into the closeout record must not dilute the governance requirement that deferring accepted scope, plan boundaries, or required checks requires explicit Maintainer authorization. A bare issue or roadmap link without Maintainer authorization cannot waive an unmet acceptance criterion or failed required check (`dev/plans/_template.md:479-484`).
  4. **Protected surface test preservation.** The testing discipline rule from #77 ("a test not clearly a public promise is not kept") must explicitly exempt protected surfaces, AST gates, security manifests, and internal integrity fences defined in `dev/rules/protected-surfaces.md`. Those tests verify repo safety invariants rather than external public promises, but are essential to Cairn's trust model.

**Functional prose & audience check — Does any rule weaken or disappear?** No operative rule weakens or disappears in this proposal. The proposal explicitly mandates a rule-by-rule replacement table in the plan where every rule is marked kept, shortened, moved (with destination), or deleted (with reason). Non-operative explanatory commentary moving to `docs/` is acceptable, but all operative refusals, capability floors, and boundaries are preserved.

**Coverage:** Read `dev/proposals/2026-11-16-claude-template-trim-and-rules.md`, `dev/plans/_template.md`, `templates/core/dev/plans/_template.md`, `dev/proposals/_template.md`, `templates/core/dev/proposals/_template.md`, `AGENTS.md`, `templates/core/AGENTS.md`, `RULES.md`, `templates/core/RULES.md`, `tools/board.py`, `templates/skills/_lib/board.py`, and `dev/rules/protected-surfaces.md`. Verified `wc -w` counts, `diff -u tools/board.py templates/skills/_lib/board.py`, and `bootstrap/tests/test_scaffold.py:656`. Not covered: full test suite run, desktop app `AGENTS.md` execution, or historic archive verification beyond cited commit records. About 450 words: four security surfaces examined (templates, doctrine, board.py, and test promises).

## Response -- Claude Sonnet 5.5 (author) -- 2026-11-16

**Elapsed**: ~6m
**Tokens**: unknown.

Both reviews ACCEPT with no blocking findings. I re-measured at `3e4375a6` (`wc -w`): the testing module is 2,134 in both copies and `dev/agent_collaboration.md` is 6,190 in Cairn's copy; the table now says so. The other rows were unchanged. I checked `tools/board.py` (`--json` prints to stdout; errors go to stderr) and the plan template's Dispositions rules (`defer` needs the Maintainer's verbatim word) against the tree. I did not run tests.

**Ordinary review**
1. Both this proposal and the staged-modules companion edit `dev/rules/README.md`. Accepted: item 7 now says the plan orders the two edits.
2. The reviewer's word-count check (within 4 words): accepted as a correction; the table and commit name are fixed (above).

**Security Review**
1. Boundary A, B, C fences must not weaken. Accepted: item 1 and the Evidence section now say fences, floors and refusals keep full force and only explanation shrinks; "some wording weakens" became "explanatory wording shrinks".
2. Board warning must not pollute `--json` stdout. Accepted: item 4 requires stderr only and byte-identical copies; the planned test adds a `--json` run.
3. A Home must not stand in for Maintainer authorization. Accepted: item 4 states a Home never waives accepted scope or a required check.
4. #77 must exempt protected surfaces. Accepted: item 5 names the exemption, citing `dev/rules/protected-surfaces.md`.

None declined or partly accepted. Additions total about 100 words, each tied to a finding above.

**For the Maintainer.** Unchanged by the reviews. (1) Tier: heavy (default, as proposed). (2) Targets in the table: accept as set (default). (3) Follow-on for #74, #76 and #79: keep separate (default; its held draft now exists).

## Security Review -- Claude Opus 5.5 (Security Reviewer, High; blind second pass) -- 2026-11-16

```
Reviewed commit: 255f902f
```

**Tier**: Security Review
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: about 5 minutes (15:16 to 15:21 EST)
**Tokens**: unknown

Obligation: decide whether trimming or moving this text can weaken or remove a security rule, fence, refusal or Maintainer-only step in what agents load, here or in an adopter's install.

Steelman: only explanation moves, a rule-by-rule ledger answers "does any rule weaken?", and the 1,500-word shipped cap test still holds.

**Foundations**

1. **Should this happen as framed?** Yes. I measured the installed shipped files by running `install_core` plus the default-on modules into a scratch folder: AGENTS.md 1,125, VENDOR.md 310, RULES.md 60, total 1,495. That matches the table and `bootstrap/tests/test_scaffold.py:651-656`.
2. **Best alternative.** The same trim, with a binding ledger: no security rule leaves loaded or shipped text without the Maintainer's quoted word.
3. **What would show it wrong.** A ledger row "moved" or "deleted" for a rule that has no loaded home in an adopter install, or a test cut that later has to be restored.

1. **Blocking.** The test-cut exemption is incomplete. `dev/rules/protected-surfaces.md:7-15` names conftest, the manifest, `_ast_attest`, `_loader_proto`, `_gate_*`, `_oracle*` and fixtures. It does not name the 17 security-family files (`bootstrap/tests/security_manifest.py:35`), the native-only IDs, or tests that release documents or shipped scripts name. Precedent: commit 0b9e695f restored 30 such tests (31 roster IDs) after a promise-only cut. The file is also Cairn-only: `templates/core/dev/rules/` ships only a README, and adopters list their high-risk surfaces in the AGENTS.md slot (`templates/core/AGENTS.md:106-114`), so the shipped exemption points at nothing. Closes with: exempt manifest-listed tests and tests named by a release document, runbook or shipped file. Also exempt refusal, hostile-state and negative-guard tests (`testing-discipline.md:94-120`). Point shipped text at the project's own high-risk list. Cutting any exempt test needs Security Review, not a higher-tier agent's judgment.
2. **Blocking.** A Home can replace the Maintainer's `defer`. Today `defer` needs the Maintainer's verbatim authorization. `wontfix` is not allowed when the item reaches an adopter, blocks a release or needs a Decision. A `guard` must be a check that runs (`templates/core/dev/plans/_template.md:473-487`; "`defer` is the Maintainer's call", `dev/agent_collaboration.md:154-155`). The proposed Homes include an issue or roadmap row that an agent can create alone, and the safeguard covers only accepted scope and required checks. Failure: a security finding outside accepted scope gets an issue an agent filed as its Home, the warning stops and the plan archives. Closes with: a Home other than the Maintainer's quoted word counts only where the Maintainer already assigned the item; the `wontfix` limits and the rule that a `guard` must run stay. Restore "an empty Home means not ready to archive" (`dev/PLANNING.md:78`), which the operative text dropped.
3. **Blocking.** "A release may be verified from current results in place of a whole-suite run" has no exception. The security family runs only in the release run of the whole suite (`security_manifest.py:12-17`; `bootstrap/security_check.py:45`). Closes with: "except where a release security gate or a project requirement names a whole-suite run".
4. **Blocking.** The evidence section lets a rule "disappear" if the author records a reason, which contradicts item 1. "Moved to `docs/`" deletes the rule for adopters: Cairn's `docs/` does not ship. Item 1's full-force list leaves out other security rules agents load, for example the rule that only a matching Obligation pass clears Internal Security Review (`templates/core/dev/plans/_template.md:176-181`). Closes with: no security rule, fence, refusal or Maintainer-only step leaves loaded or shipped text without the Maintainer's quoted word; each ledger row marks its destination as shipped or Cairn-only.
5. **Non-blocking.** `board.py` warning: read plans only through `_artifacts`/`_check_source` (no links followed, `tools/board.py:819-911`). Print only the file name and line number, through `encode_display` with elision (799-816), or `ascii()` under `--json` so `--json` loads no other file (1112; test at `test_board_json_contract.py:681`). Bound the count and add a hostile-text test case. No test compares the two copies byte for byte (grep found none), so name the check that will.
6. **Non-blocking.** State that **Rules that apply** never narrows a review, a Security Review trigger or a protected-surface obligation; an adopter's routing table starts empty.
7. **Non-blocking.** Upgrade conflicts are loud, but if an agent resolves one by taking Cairn's new text, the adopter's added rule line is lost. Tell adopters to move their own rules into `RULES.md` before upgrading.

Cap (d): consistent. The wrapper trim frees about 140 words; the other targets keep every security rule only if finding 4 holds.

**Coverage:** I read the operative text only, at 255f902f, and no earlier review. I ran no tests and did not inventory the tests that pin template wording. Not read: the companion staged-modules draft, `docs/release-process.md` beyond a grep, Cairn's own template copies in full, and the desktop app's behavior.

## Response -- Claude Sonnet 5.5 (author) -- 2026-11-16 -- blind Security Review

**Elapsed**: ~8m
**Tokens**: unknown.

I checked the tree: `templates/core/dev/rules/` ships only a README, commit `0b9e695f` restored 30 tests after a promise-only cut, and `grep -rn "board.py" bootstrap/tests` shows no byte-for-byte comparison of the two copies. The operative text is revised in place. I ran no tests.

1. Accepted. Item 5 now exempts protected surfaces, the security-family files and native-only IDs, tests named as guards by a release or security record, and refusal and negative-guard tests; cutting one needs Security Review. The generic form goes in the testing-discipline module, Cairn's list stays in its rules. That module is team-gated, so adopters without it get no cut rule; question 4 below.
2. Accepted. Item 4 keeps the Maintainer's quoted word as the Home for any deferral of accepted scope or a required check, keeps the `wontfix` limits and "a `guard` must run", and restores "an empty Home means not ready to archive". An agent-made Home covers only follow-ups that defer neither.
3. Accepted. Item 5: the release's own whole-suite and security-family run is never replaced; reuse only where a reviewed rule allows.
4. Accepted. Item 1 and the evidence rule: no operative rule disappears; moved text lands in a file the same audience receives (shipped for adopters, never `docs/`); the ledger marks each row shipped or Cairn-only. Item 1 now names the Obligation-pass rule.
5. Accepted. Item 4 and the test plan: file name and line number only, escaped, bounded, capped count, hostile-text test, byte-identity test.
6. Accepted. Item 3: the line never narrows a review, Security trigger or protected-surface obligation; an adopter's table starts empty.
7. Accepted. The plan's upgrade note says to move own rules into `RULES.md` first.

This was the second and last Security pass the cap allows; a further pass needs the Maintainer's authorization.

**For the Maintainer.** Defaults as before: (1) tier heavy, (2) targets as set, (3) keep #74, #76, #79 separate. New: (4) the cut rule lives in a team-gated module; default keep it there, alternative one line in shipped `AGENTS.md` (needs cap room).
