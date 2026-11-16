# Trim the templates, testing text and collaboration guide; list the rules that apply

**Author**: Claude Sonnet 5.5 (claude-sonnet-5-5)
**Status**: awaiting-review
**Waiting on Maintainer**: release draft for review
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
