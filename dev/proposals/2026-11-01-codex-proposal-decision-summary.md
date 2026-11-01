# Make proposals easier to decide

**Author**: Codex GPT-6 (Proposal author)
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: heavy — the shipped proposal template is a named high-risk surface
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-01
**In brief**: Put the problem, proposed change, and tradeoffs at the start of a proposal so the Maintainer can understand the choice without a live translation.

## Context

A Maintainer can be asked to decide a change before its practical consequence
is clear. The proposal template asks for context, a proposal, rationale and
alternatives in separate sections, while its one-sentence `In brief` is also
used by the board. That sentence cannot always carry the problem and the
tradeoffs. The accepted meter proposal, for example, describes several
mechanisms before its rationale and alternatives. Its opening does state the
requested outcome, but a reader must assemble the costs and choice from later
sections (`dev/proposals/2026-10-30-claude-metered-cost.md`). This is an
observation of that artifact, not a measurement of how often readers struggle.

## Proposal

Change the opening prompts in both proposal templates. After the existing
one-line `In brief` header, ask for a short decision summary before supporting
detail: the problem someone notices, the proposed change, and its meaningful
costs or tradeoffs. Write it in ordinary language for the person making the
Decision. Introduce technical terms only when needed, define them where they
first matter, and use a concrete example to make an abstraction clear. Put
implementation and review details after the summary where the reader needs
them. A short proposal may do most of its work in the summary and rationale;
avoid repeating those points just to fill sections. Preserve required evidence,
checks, lifecycle records, the board's one-line field, and security and
scientific preflights when applicable.

In the existing proposal review, consider whether the Maintainer could explain
the choice from the proposal without a live translation. This is a reading
judgment, not a new review stage, mandatory checklist, or readability score.

## Rationale

The existing Cairn Plain Language rules already require a conclusion first,
information needed to decide, definitions, examples, and detail in its own
section (`dev/agent_collaboration.md`, rules 1–3, 5–6 and 9). They apply to
proposals and already make understanding a precondition for Decision. No
change to the general standard is needed: the template should apply those
rules to this particular choice. The cost is a little more thought at the
start and sometimes a few extra sentences; the expected benefit is less work
reconstructing the choice later. I have not measured that benefit.

## Alternatives considered

Leave the template alone: the general rules remain available, but the template
still spreads the information needed for a decision across prompts. Add a new
plain-language rule or scored check: that duplicates existing rules and adds
burden without showing better understanding.

## Documentation / doctrine surface

Change `dev/proposals/_template.md` and its shipped counterpart
`templates/core/dev/proposals/_template.md` in their common, non-slot guidance
and opening prompts. Update `doctrine/proposals.md` only as needed to describe
the revised proposal shape. These are deliberation guidance and published
doctrine, respectively; no software description or governing instruction is
proposed. Keep the shipped and self-hosted common text consistent.

## Evidence / verification plan

### Tests required

Search for readers and byte pins of each changed file, and use
`python tools/test_tiers.py for` on the actual changed paths to identify and run
the required scoped tests. Preserve slot and board behavior. The implementer
must follow the named high-risk surface checks and record Boundary B as
required by `AGENTS.md`.

### Examples / smoke checks

Run the applicable claim, link, snippet and neutrality prose gates. Inspect the
revised template against a short and a technically involved existing proposal:
can a reader find the observed problem, change and tradeoffs before supporting
detail, without losing required evidence? This is a qualitative check, not a
claim that a particular reader was tested. Failure to preserve the required
records or a summary that cannot convey the choice would falsify the design.

#### Security preflight

S1: Authors supply proposal text; reviewers and the Maintainer judge it. The
template guides that text but does not authorize the Decision.
S2: The change relies on existing human review and template checks; the
implementation must identify and exercise a relevant failing case for any
changed machine check. No new machine check is proposed.
S3: The scoped test selector and prose gates above identify checks; the human
review reads the committed proposal and its evidence. Implementation must
trace any changed check to its actual trigger and runner.
S4: This adds no automated default, fallback, parser or authorization path;
missing or unclear decision information remains subject to the existing pause.
S5: A misleading author can still write a plausible summary; reviewers must
compare it with supporting evidence. The change does not claim to eliminate
that risk.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

Summaries routinely omit material costs, repeat the whole proposal, or make
required evidence harder to find; reviewers cannot tell what the Maintainer
is being asked to decide; or the new guidance adds more work than it saves.

## Scope delta

None; this is the opening scope.

## Assurance path

**Assurance path**: high-assurance — the shipped vendor-neutral template is a
named high-risk surface.
