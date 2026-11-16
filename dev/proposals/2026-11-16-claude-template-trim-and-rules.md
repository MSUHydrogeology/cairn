# Trim the templates, testing text and collaboration guide; list the rules that apply

**Author**: Claude Sonnet 5.5 (claude-sonnet-5-5)
**Status**: revising
**Review**: usual + Security Review (until the accepted template-scan change lands; then usual only, plus Security Review for the `board.py` part)
**Proposed tier**: heavy — it rewrites both authoring templates and the shipped always-loaded files, and adds a code warning to a shipped `.py`; the Maintainer sets the tier
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-16
**In brief**: Shorten the text agents must read to start any task, and make each proposal and plan name the few rule files that apply to it.

## Decision summary

An adopter reads about 7,200 words of guidance to do one task, and the v0.7 `AGENTS.md` trim moved bulk into other files instead of removing it. This proposal sets a target length for each bulky file (table below), moves detail agents do not need to run to documentation, and rewrites what stays shorter. It adds one header line, `**Rules that apply**:`, to the proposal and plan templates, and folds the plan's Dispositions section into the closeout record. Cost: adopters who edited these files meet merge conflicts at upgrade. Rules-folder guidance and the run-versus-develop split are follow-ons (items 7 and 8).

## Context

Words counted with `wc -w` at commit `3ec301a9`, 2026-11-16. Targets are my proposal; the Maintainer sets them.

| File | Cairn copy | Shipped copy | Target (shipped; Cairn's = shipped plus its slots) |
|---|---|---|---|
| Plan template | 4,859 | 4,871 | 3,900 |
| Proposal template | 4,599 | 4,275 | 3,400 |
| Testing-discipline module | 2,130 | 2,130 | 1,400 |
| `dev/agent_collaboration.md` | 6,187 | 6,116 | 4,800 |
| `AGENTS.md` | 945 | 1,125 | no growth |
| Vendor wrapper (`VENDOR.md`; Cairn's `CLAUDE.md`) | 362 | 310 | 170 |
| `RULES.md` | 181 | 60 | no growth |

The three always-loaded files total 1,488 for Cairn (cap 2,000, a written rule, no test) and 1,495 shipped (cap 1,500, held by `bootstrap/tests/test_scaffold.py`). The shipped set sits 5 words under its cap, so any rule added to it needs room first. Maintainer, 2026-11-10: "There simply aren't 5000 words worth of instructions needed to develop in this repo. That is just bloat."

## Proposal

**1. The trim.** Detail a person needs to understand the method but an agent does not need to act moves to documentation (the plan names each destination). What stays is rewritten shorter. The rewrite starts with the Boundary A, B and C and testing text, because it drives test-building. About 145 of the wrapper's 310 words are notes to the person renaming it; they go.

**2. Constraints** (from the board). The templates must not grow. No test may pin the wording of the result; the plan finds and deletes such tests first, as the `AGENTS.md` trim did. The caps above stand.

**3. `**Rules that apply**:`.** Both templates gain this header line. It lists rule file paths picked from the `RULES.md` routing table, never rule text, or `bright lines only`. A rule that applies but is unlisted is still followed and added to the line. Reviewers compare the line with Scope. About 20 words, paid from the trim. Maintainer, 2026-11-12: "I like all of this."

**4. Dispositions.** The plan template's `## Dispositions` section folds into the closeout record: every "not run, not covered or remaining" line carries a Home (a roadmap row, an issue, a proposal or the Maintainer's quoted word). `tools/board.py` (copied byte for byte to `templates/skills/_lib/board.py`) gains one advisory warning for a `ready-to-archive` plan with such a line and no Home. It warns and does not block.

**5. Testing rules.** From #77: a test not clearly a public promise is not kept, and a higher-tier agent decides judgment calls. From #86: test time has an owner and a review cadence for the slowest files. From #88: each new test runs once on a clean checkout. From #81 and the grown-projects note, the principle only, not the record tool: a large project is not one piece, so test each part where it lives, and a release may be verified from current results in place of a whole-suite run. Each lands as a sentence inside the rewrite.

**6. Appendix (#73).** Default none. Allowed only for a table or arithmetic a reviewer must check that no cited record can hold, as one separate file per proposal, never inline. The 1,000-word budget applies to the text at the Decision, so review additions are cut or moved before it. The plan settles naming (#73 suggests `<stem>--appendix.md`) and board handling.

**7. Rules-folder guidance (#70; entry shape, applicability line, size budget, how a rule enters and leaves).** Not delivered here: it is the first staged module in the companion draft `dev/proposals/2026-11-16-claude-staged-modules-and-triggers.md`, because it needs a trigger design and would add words to files this proposal shrinks. Delivered here: one sentence in the `dev/rules/README.md` shipped with every install, that a Maintainer's rule goes in the rule file with approved wording, never only in agent memory (#70).

**8. #74, #76, #79 (run rules apart from development rules; an Operator role; a project-wide `AGENTS.md` entry with pointers into `dev/rules/`).** Recommend a separate follow-on proposal, opened after this one lands. Reason: they change what the always-loaded entry file and the role table mean, not only how long they are, and a reviewer cannot judge a rewrite and a restructure of the same text in one pass. Cost of splitting: an adopter who edited `AGENTS.md` merges twice, though each merge is smaller. Cost of including: one larger conflict (the 2026-11-11 trial found a one-word edit inside a removed paragraph made 93 of 206 lines conflict, and `--apply` refuses until resolved), a heavier review, and a risk that the restructure delays the trim.

## Rationale

Folding Dispositions leaves one closing section, and catches what a review of 11 archived plans found: nine had no Dispositions section.

## Alternatives considered

Do nothing: the load stays and Dispositions keep escaping. Copy rule text into plans: copies drift. Include items 7 and 8: costs above.

## Documentation / doctrine surface

Both templates, the testing module, the collaboration guide, the vendor wrapper, `dev/rules/README.md`, `tools/board.py`. Removed detail lands in `docs/`. A Claude Code project no longer needs a `CLAUDE.md` (2026-11-16 amendment to the repository-layout proposal), which leaves open whether `VENDOR.md` stays. This proposal trims its notes and decides nothing about its fate; if the layout plan removes it first, that line is moot.

## Evidence / verification plan

Word counts per file against the table, by `wc -w`. The plan lists replacements rule by rule, each marked kept, shortened, moved (with destination) or deleted (with reason), so a reviewer can answer "Does any rule weaken or disappear?" row by row. For the proposal as a whole: yes, some wording weakens by design (detail moves out of loaded text), and none may disappear without a recorded reason. Tests: the board warning gets one test through `tools/board.py` with a plan that has a Homeless line and one that has a Home. Not checked: how many tests pin template wording; the desktop app's `AGENTS.md` behavior.

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
