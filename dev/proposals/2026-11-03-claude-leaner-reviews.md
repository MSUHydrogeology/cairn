# Leaner reviews and proposals that grow only to absorb findings

**Author**: Claude Opus 5.5 (Strategy)
**Status**: awaiting-review
**Review**: usual
**Proposed tier**: light -- the Maintainer asked for one light proposal (chat, 2026-11-03)
**Plan review**: not required(no plan: light tier)
**Opened**: 2026-11-03
**In brief**: Cut repeated parts of review records so findings fit, treat word budgets as soft, and let revised proposals grow to absorb review findings instead of being trimmed back.

## Decision summary

Reviews are capped at 300 words. About a third of that goes to parts that
repeat other text, so findings get squeezed into shorthand. Authors also spend
passes trimming proposals back under 1,000 words after absorbing review
findings. This proposal:
- removes the repeated parts of a review record;
- says budgets are soft;
- lets a revised proposal grow, but only to absorb accepted findings.

Nothing new is added to the process.

Maintainer direction (chat, 2026-11-03), verbatim:

> "Go with one light proposal. Also, I don't think we should re-write a
> proposal to be shorter after new reviews are added. The total length grows,
> but with constraints."

## Context

Measured on `0.7-dev` at `c5d82007`.

- **The two reviews of `dev/proposals/2026-11-03-claude-agent-continuation.md`:**

  | Part | Usual review | Security Review |
  |---|---|---|
  | Header and metadata | 37 words | 32 words |
  | Foundations | 84 words | 55 words |
  | Coverage line | 15 words | 10 words |
  | Findings | 216 words | 194 words |

  - In both, the third Foundations answer only pointed back to findings: "F2,
    F3" and "SR1".
  - Both reviewers wrote clipped shorthand ("Close: full table; ambiguous rows
    print stop"), which runs against Cairn Plain Language.
  - One reviewer reported "body about 300 words, plus skeleton lines". The
    rule does not say whether skeleton lines count.
- **Proposals.** Across the 32 most recent proposals, operative text before
  the first review has a median of 1,002 words; 17 exceed 1,000 and 8 exceed
  1,200. Five sit at 998 to 1,002 words, which suggests trimming to the line.
  - The agent-continuation proposal absorbed 10 findings and grew from 997 to
    1,085 words.
  - It took two trimming passes to get back under 1,000.
- **Where the rules live.**
  - Foundations: `AGENTS.md` ("A pass starts with three evidenced Foundations
    answers").
  - Review limits: `AGENTS.md`, `dev/agent_collaboration.md` and
    `docs/methodology/dual-review.md`.
  - Budgets and skeletons: `dev/proposals/_template.md` and
    `dev/plans/_template.md`.
  - Each has a shipped copy under `templates/core/` (except the methodology
    file).
- **Self-reported Tokens:** already decided elsewhere, so it is out of scope.
  [`dev/proposals/2026-10-30-claude-metered-cost.md`](2026-10-30-claude-metered-cost.md)
  (accepted) puts Q1 in its Proposal item 5: retire the self-reported Tokens
  field once the meter passes its checks. Its Decision of 2026-10-30
  answered: *"Q1: retire Tokens."*

## Proposal

1. **Foundations may be answered by a finding.** Each pass still answers all
   three questions. A finding that answers one says so, for example "F2 (what
   would show it wrong)". A separate Foundations line is written only when it
   adds something the findings do not.
2. **Drop repeated review metadata.**
   - Remove `Target` (always the operative sections), `Assurance path` (in the
     artifact header), `Findings: raised | none` (shown by the verdict and the
     list), and `Prior findings` when there are none.
   - Keep `Reviewed commit`, `Tier`, `Verdict`, `Elapsed` and `Tokens` until
     the meter replaces Tokens.
3. **Count only the text.** Word limits count the reviewer's text, not
   skeleton lines.
4. **Budgets are soft.** Each "Keep ... short" section states its numbers as
   targets. An author does not make a pass whose only purpose is cutting
   words to reach a number.
5. **Revisions grow, with constraints.** After review, the author revises
   operative text in place, as now. It may grow beyond the opening target,
   but:
   - each added passage answers a named finding, which the response
     identifies;
   - nothing unrelated is added during revision;
   - past about 1,300 operative words, the author considers splitting the
     work and says why in the response.

   Plans follow the same rule.

## Rationale

These changes give findings more room while the record gets shorter, not
longer. Raising the review limit to 450 words was the alternative, and it
would add reading. Rule 5 keeps the Maintainer's Decision text whole instead
of compressed.

## Alternatives considered

- **Raise the review limit to 450 words.** Simpler, but every review gets
  longer to read.
- **Do nothing.** Findings stay in shorthand, and authors keep trimming after
  each review.

## Documentation / doctrine surface

- **Prescription:**
  - `AGENTS.md` and `templates/core/AGENTS.md`: the Foundations sentence and
    the counting rule.
  - `dev/agent_collaboration.md` and its shipped copy: the review limit
    sentence.
- **Templates:** the proposal and plan templates, both copies: skeletons,
  "Keep ... short" sections and the revision rule.
- **Doctrine:** `docs/methodology/dual-review.md`. The doctrine rate-limit gate
  applies.

## Evidence / verification plan

- **Tests:**
  - Run `tools/test_tiers.py for` the changed files.
  - Byte pins and template-parity tests are expected to need matching
    updates. The mapped list names them; none are dropped.
  - Prose gates: claim, link and neutrality.
- **Trial:** the next two reviews written under the new skeleton report their
  findings word count against today's 216 and 194.
- **Security preflight:** N/A, no trust boundary added or widened.
- **Independent scientific check:** N/A, no scientific assumption touched.

## Signals the change is wrong

- Reviews drop a Foundations answer.
- Findings come out no longer than today's.
- Proposals grow without each addition tracing to a finding.

## Scope delta

**Scope delta**: preserved

## Assurance path

**Assurance path**: high-assurance -- it changes shipped templates and
`AGENTS.md`, which are named high-risk surfaces. The Maintainer chose the
light tier; the Decision can change it.
