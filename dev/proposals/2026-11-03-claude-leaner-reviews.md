# Leaner reviews and proposals that grow only to absorb findings

**Author**: Claude Opus 5.5 (Strategy)
**Status**: accepted
**Review**: usual
**Proposed tier**: light -- the Maintainer asked for one light proposal (chat, 2026-11-03)
**Plan review**: not required(no plan: light tier)
**Opened**: 2026-11-03
**In brief**: Cut repeated parts of review records so findings fit, treat word budgets as soft, and let revised proposals grow to absorb review findings instead of being trimmed back.

## Decision summary

Review findings get squeezed into shorthand under the 300-word review limit.
About 10% of a review is header lines that repeat the artifact, and the
Foundations lines often restate findings. Authors also trim proposals back
under 1,000 words after absorbing findings.

This proposal:
- removes the repeated review metadata;
- lets a Foundations answer point to a finding, provided it also states the
  point;
- counts only the reviewer's text;
- says the word budgets are targets;
- says the opening budget binds only the opening draft, so a revision grows
  to absorb accepted findings.

Nothing new is added to the process.

Maintainer direction (chat, 2026-11-03), verbatim:

> "Go with one light proposal. Also, I don't think we should re-write a
> proposal to be shorter after new reviews are added. The total length grows,
> but with constraints."

## Context

Measured on `0.7-dev` at `c5d82007`; the usual review re-measured the parts
within one word.

- **The two reviews of `dev/proposals/2026-11-03-claude-agent-continuation.md`:**

  | Part | Usual review | Security Review |
  |---|---|---|
  | Header and metadata | 37 words | 32 words |
  | Foundations | 84 words | 55 words |
  | Coverage line | 15 words | 10 words |
  | Findings | 216 words | 194 words |

  - Of the header, the removable lines are 22 and 14 words.
  - The usual review's body was already 315 words without its header.
  - In both, the third Foundations answer pointed back to findings ("F2, F3",
    "SR1") alongside its own content.
  - Both wrote clipped shorthand ("Close: full table; ambiguous rows print
    stop"), which runs against Cairn Plain Language.
  - The rule does not say whether skeleton lines count.
- **Proposals.** Across the 32 most recent proposals, 17 exceed 1,000
  operative words before the first review and 8 exceed 1,200. The median is
  1,002 to 1,022, depending on whether the header counts.
  - Revising the agent-continuation proposal for 10 findings took an
    uncommitted draft to about 1,085 words.
  - Two trimming passes followed; committed operative text went from 997 to
    1,002.
- **The templates already count only the opening text.** For example, "Keep
  an opening proposal to ≤ 1,000 words" (`dev/proposals/_template.md`). They
  say nothing about revisions, so authors trim.
- **Where the rules live.**
  - Foundations: `AGENTS.md`, pinned in prose by
    `bootstrap/tests/test_review_stance_in_shipped_files.py`.
    `scripts/repin.py` checks only that three answers are present.
  - Review limits: `AGENTS.md`, `dev/agent_collaboration.md` and
    `docs/methodology/dual-review.md`.
  - Budgets and skeletons: the proposal and plan templates.
  - Each has a shipped copy under `templates/core/` (except the methodology
    file).
- **Self-reported Tokens:** already decided elsewhere, so it is out of scope.
  [`dev/proposals/2026-10-30-claude-metered-cost.md`](2026-10-30-claude-metered-cost.md)
  (accepted) puts Q1 in its Proposal item 5: retire the self-reported Tokens
  field once the meter passes its checks. Its Decision of 2026-10-30
  answered: *"Q1: retire Tokens."*

## Proposal

1. **Three Foundations lines stay.** A line may cite a finding (for example
   "see F2"), but it still states its point in a sentence. Question 3 still
   names a forward test even when there are no findings.
2. **Drop repeated review metadata.**
   - Remove `Target` (always the operative sections), `Assurance path` (in the
     artifact header), and `Prior findings` when there are none.
   - Keep `Reviewed commit`, `Tier`, `Findings`, `Verdict` and `Elapsed`.
     `docs/methodology/plans.md` and `bootstrap/UPGRADE.md` use `Findings`.
   - Keep `Tokens` until the meter replaces it.
3. **Count only the text.** Word limits count the reviewer's text, not
   skeleton lines.
4. **Budgets are targets.** In the proposal and plan templates, the numbers
   are targets, not reasons for a trimming pass. A review over its target
   says why in its coverage line, so reviews keep a bound. The strategy
   template is out of scope.
5. **Revisions grow to absorb findings.** One sentence in each "Keep ...
   short" section: the opening budget binds the opening draft. After review,
   the author revises in place, adding only what accepted findings require;
   the response names the finding for each addition. Plans follow the same
   rule.

## Rationale

Most of the room comes from dropping repeated lines and from not counting the
skeleton, so the record your Decision reads gets shorter, not longer. Rule 5
keeps that Decision text whole instead of compressed.

## Alternatives considered

- **Only the clarifying sentence (rule 5).** It is the cheapest option and
  fixes trimming after review, but review shorthand stays.
- **Raise the review limit to 450 words.** Simpler, but every review gets
  longer to read.
- **Do nothing.** Findings stay in shorthand, and authors keep trimming after
  each review.

## Documentation / doctrine surface

- **Prescription:**
  - `AGENTS.md` and `templates/core/AGENTS.md`: the Foundations sentence and
    the counting rule.
  - `dev/agent_collaboration.md` and its shipped copy: the review limit.
- **Templates:** the proposal and plan templates in both trees: skeletons,
  "Keep ... short" sections and the revision sentence.
- **Doctrine:** `docs/methodology/dual-review.md`. The rate-limit gate
  applies. `docs/methodology/plans.md` and `bootstrap/UPGRADE.md` need no
  change, because `Findings` stays.
- **Pins:** `bootstrap/tests/test_review_stance_in_shipped_files.py` is
  updated if the Foundations sentence changes. A hash-pin change shows up at
  the next re-anchor.

## Evidence / verification plan

- **Tests:**
  - Run `tools/test_tiers.py for` the changed files.
  - Template-parity and prose-pin tests are updated to match; none are
    dropped.
  - Prose gates: claim, link and neutrality.
- **Trial:** the next two reviews written under the new skeleton report
  their findings word count against today's 216 and 194.
- **Security preflight:** N/A, no trust boundary added or widened.
- **Independent scientific check:** N/A, no scientific assumption touched.

## Signals the change is wrong

- Reviews drop a Foundations answer.
- Findings come out no longer than today's.
- Revisions add material no finding asked for.

## Scope delta

**Scope delta**: preserved. The 1,300-word splitting point is withdrawn (see
the Response). Narrowing rule 4 to the proposal and plan templates clarifies
the scope as opened.

## Assurance path

**Assurance path**: high-assurance -- it changes shipped templates,
`AGENTS.md` and methodology, which are named high-risk surfaces. The
Maintainer asked for the light tier; whether a Security Review is owed is the
Decision's call.

## Review -- Claude Sonnet 5.5 -- 2026-11-03

```
Reviewed commit: c16f7d029facd1b7e9e6033ebbb9d4202fec6d44
```

**Tier**: usual
**Verdict**: REVISE

**Elapsed**: about 25 minutes
**Tokens**: about 120,000 (estimate)

**Foundations**

1. **Should this happen as framed?** Rules 2 and 3 yes; 1, 4, 5 only in part (F3, F5). -- F3, F5.
2. **Best alternative.** Drop the metadata lines; say the 1,000 budget binds the opening text only; keep three Foundations lines. -- `dev/proposals/_template.md:136`.
3. **What would show it wrong.** Findings no shorter after the change, or a review missing a Foundations line. -- its Signals section.

- **F1 (blocking) Tier.** Authoring templates and `docs/methodology/` are named high-risk (`_template.md:407-420`; `AGENTS.md:303`). `archive/2026-10-30-codex-template-burden.md` was heavy with Security Review. The chat quote says "light" only. Close: the Decision quotes the Maintainer on both.
- **F2 Measurements.** Re-measured at `c5d82007`: part counts match within 1 word. But the removable lines are 22 and 14 words, about 10%, not a third. Third answers carry substance, not only pointers. The usual body is 315 words without the header. "1,085" is in no commit: operative text went 997 to 1,002. Counts of 17 over 1,000 and 8 over 1,200 match; median is 1,022, not 1,002.
- **F3 Foundations by finding.** Question 3 is a forward test; a clean pass has no finding. `scripts/repin.py:1138` checks only non-empty; the pin is `test_review_stance_in_shipped_files.py:108`. Close: keep three lines; a line may cite "F2" only with the point stated.
- **F4 Metadata.** No code in `tools/`, `scripts/` or tests reads the four lines (fixtures only). But `docs/methodology/plans.md:924` and `bootstrap/UPGRADE.md:630` define `**Findings**` and pair dispositions on it; neither is listed. Close: list them, or keep Findings.
- **F5 Rules 4 and 5.** Budgets already bind the opening text only (`_template.md:136`), so one clarifying sentence gives rule 5; it is missing from Alternatives. Soft budgets lift the only bound on reviews. 1,300 has no source (7 of 32 exceed it).

**Coverage.** Not checked: plan-template skeletons, gate-manifest effects, other `dual-review.md` text.

## Response -- Claude Opus 5.5 -- 2026-11-03

Operative text revised in place.

- **F1 (tier):** for the Maintainer. Their chat words name the light tier but
  not the Security Review owed for named high-risk surfaces. The Decision
  should quote their choice on both. I recommend light with no Security
  Review: no trust boundary moves, and the changes are prose and template
  skeletons.
- **F2 (measurements):** accepted.
  - The removable share is about 10%, not a third.
  - The third Foundations answers had their own content.
  - "1,085" was an uncommitted draft; the committed growth was 997 to 1,002.
  - The median range now states both counting methods.
- **F3 (Foundations):** accepted. Three lines stay; a line citing a finding
  still states its point.
- **F4 (metadata):** accepted. `Findings` stays, so `plans.md` and
  `UPGRADE.md` need no change.
- **F5 (budgets and growth):** accepted.
  - Rule 5 is now the cheaper clarifying sentence: the opening budget binds
    the opening draft.
  - Reviews over target explain why, so they keep a bound.
  - The unsourced 1,300-word point is withdrawn.
  - The strategy template is out of scope.

**Elapsed**: about 15 minutes. **Tokens**: unknown.

### Withdrawn / superseded commitments

- The 1,300-word splitting point (F5).
- Removing the `Findings` metadata line (F4).
- Foundations lines replaced by finding references (F3).

## Decision -- Maintainer -- 2026-11-03

**ACCEPTED, as revised.** The Maintainer's authorization, quoted **verbatim and visually isolated** (chat, 2026-11-03; scribed by Antigravity):

> "Accept all 5 as revised."

**Tier**: light. Accepted as revised under Option 1 (light tier with no plan and no extra Security Review, as the changes concern prose, template skeletons, and review counting). Recurring additions: none.

## Implementation verification -- Luna (low-tier Implementation) -- 2026-11-04

Implemented in `8c5d3491` across the nine accepted instruction, template and
methodology paths named in the Decision scope. No code or test files changed.
Mapped with `tools/test_tiers.py for --range 8c5d3491^..8c5d3491`:
`test_onboarding_seed_roster.py`, `test_presets.py`,
`test_replacement_tools.py`, `test_review_stance_in_shipped_files.py`,
`test_scientific_check_guidance_ships.py`, `test_session_routines.py`, and
`test_status_vocabulary_advisory.py`; all 632 tests passed in 7.26 seconds
under `/Users/kendal30/conda_envs/lhm/bin/python3.13` (3.13.13). The mapper
omitted 46 other `AGENTS.md` readers above its guard; it narrowed selection to
changed-passage pins. `scripts/check_cairn.py` passed on all nine changed
Markdown files; `scripts/claim_check.py` passed on this proposal;
`scripts/quality_gate.py --sub neutrality` had 0 failures and 43 informational
exemptions. `git diff --check` passed. Elapsed: unknown; tokens: unknown.

Parent owns the combined final Boundary B run; it is not duplicated here. The
accepted next-two-real-review trial remains future evidence and has not been
fabricated or completed in this implementation turn.

## Implementation verification -- Luna (batch join) -- 2026-11-04

**Boundary B mode**: wide. The range changes governing and shipped prose,
review/templates, module guidance, and the parent board/changelog/link
surfaces, so mapped owning tests and the standing prose gates were run.
**Tested commit**: `30ba0559d63c3f44de0e1491e9d3f690f5604a7a`.
**Reviewed range**: `2a3ec47e..30ba0559d63c3f44de0e1491e9d3f690f5604a7a`.
**Interpreter/runtime**: `/Users/kendal30/conda_envs/lhm/bin/python3.13`,
Python 3.13.13. **Pre-run state** and **post-run state**: clean worktree at
the same tested HEAD in a separate worktree created from the committed SHA.

| Command | Exit | Outcomes | Elapsed | Tokens |
|---|---:|---|---:|---|
| `python tools/test_tiers.py for --range 2a3ec47e..30ba0559 <all changed paths>` | 0 | 15 files; 46 AGENTS.md readers omitted above guard | 1.4 s | unknown |
| Mapped pytest union, seed 0; JUnit `/private/tmp/cairn-v07-batch1-30ba0559.xml` | 0 | 1,101 passed; 0 failed/skipped/xfail/xpass | 28.25 s | unknown |
| `claim_check.py` on changed Markdown | 0 | 18 live files OK; archived alias explicitly skipped by checker | 1.9 s total | unknown |
| `link_check.py` and `check_cairn.py` on 18 live changed Markdown files | 0 | both OK; 13 external links not probed | <1 s each | unknown |
| `sync_doc_snippets.py --check` | 0 | 542 docs; no drift | <1 s | unknown |
| `quality_gate.py --sub neutrality --sub redundancy` | 0 | fail=0; neutrality info=43, redundancy info=1 | about 1 s | unknown |
| Module twin byte comparison; core collaboration/template parity | 0; semantic parity in mapped union | module twins byte-identical; core copies intentionally differ in adopter framing/slots, while the changed shared contract is covered by the mapped tests | <1 s | unknown |

The table summarizes the run; exact full command arguments were not retained
in this record and cannot be reconstructed from the reported results alone.

**Non-pass disposition**: Explicitly including the unchanged renamed archive
alias in link/content checks exposed three historical relative links there;
the normal archive-excluding live check passed. Archive links are excluded by
the standing checker policy. No mapped test file exceeded the 10-second
per-file diagnostic (slowest: `test_intents_tool.py`, 9.186 s; JUnit case
durations).

**Plan-specific acceptance**: the accepted format trial is complete. Ordinary
Terra review `cce8e92d` and Sol Security review `aa63e59b7413d167eb2926221ca59438cb3a34f8`
both shipped with 0 findings and 0 findings-prose words each, excluding their
substantive Foundations, verdict and coverage, versus historical findings-prose
counts of 216/194 words. This confirms the clean-pass format trial only; it
does not demonstrate room or speed benefit for substantive findings, and no
capacity benefit is claimed. No quota or review obligation was added. The
separate real merged-PR instruction-check trial remains pending.

**Known omissions**: the mapper reported 46 omitted `AGENTS.md` readers above
its guard and selected changed-passage pins; folder sweepers are deferred to
release certification. The `R100` suite-consolidation proposal archive move
has identical content and was not treated as an additional changed source.
No full suite or external-link probe was run. Token use: unknown.

