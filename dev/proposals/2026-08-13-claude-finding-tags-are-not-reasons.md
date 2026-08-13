# Comments explain the code, not the process that produced it

**Author**: Claude (Strategy)
**Model**: Claude Opus 5 (`claude-opus-5`)
**Date opened**: 2026-08-13
**Status**: revised
**Touches**: `AGENTS.md` and `templates/core/AGENTS.md` (the comprehension-floor
paragraph in `## Review`); a read-and-revise pass over 262 tagged comments and
docstrings, sequenced per file owner
**Related**: `2026-08-13-claude-test-names-outlive-their-plans` (the same
failure in test names); `dev/PLANNING.md` > "Opaque finding-IDs in code comments
and docstrings", which this proposal drains
**Plan review**: not required(no plan — one convention paragraph plus a
bounded, judgement-led revision pass)

## Context

`dev/PLANNING.md` carries this item, raised by the Maintainer on 2026-08-13:

> *"They don't inform anyone anything. I don't know what FUR5 is."*

Comments and docstrings across the codebase carry review-finding tags —
`[FUR5]`, `[M2-1]`, `[S1]`, `[C1]`, `[E1]`, `[D2]`. The board already classifies
this as a **comprehension-floor** failure (`AGENTS.md` > Review): the tag was
written for the reviewer who had just read the finding, and is inert for
everyone after.

**Measured, `as_of 2026-08-13`:** 262 occurrences of 37 distinct tags in `.py`
files. (The thousands more in `.md` are deliberation artifacts, where a review
section citing its own findings is correct and out of scope.) They concentrate
in `bootstrap/tests/test_gate_preflight.py` (54), `bootstrap/tests/_gate_preflight.py`
(40), and the `lifecycle_planner` twins (21 each).

## Proposal

### The rule

Add to the comprehension-floor paragraph in both `AGENTS.md` copies:

> **Comments and docstrings explain the code, not the process that produced it.**
> State the reason; do not cite the finding. `[S1]`, `[M2-1]`, `FUR5` and their
> kin identify nothing to a reader without the originating plan open, and that
> plan archives. Provenance already lives in `git blame` → the commit body → the
> plan, which is maintained; an embedded tag is a second, decaying pointer. If a
> line needs history to be understandable, **write the history into the
> sentence** rather than a label pointing at it.

### Why the tag never earns its place

* **Git already carries provenance, and carries it better.** `git blame` reaches
  the commit, the commit body names the plan and the finding, the plan holds the
  reasoning. That path is maintained by construction. The embedded tag is a
  second pointer that nothing updates and that decays as plans archive.
* **It inverts Cairn's own premise.** The deliberation record is a **by-product**
  of a good process, not the point of it. A comment whose meaning depends on the
  record makes the executable artifact a dependent of the by-product.
* **Even the best case earns nothing.** In
  `# FUR5 -- the recorded anchored invocation, actually executed`, everything a
  reader gains comes from *"the recorded anchored invocation, actually
  executed"*. `FUR5` is inert. If the gloss is present the tag is redundant; if
  it is absent the tag does not rescue it.
* **A comment's job is the code.** *"Security review [S1]"* tells a reader a
  review happened, which is not what they need in order to change the function
  safely. What they need is why the line is as it is.

### What the pass costs, by how the tag is used

The 262 sites are not uniform, and the split is a **cost estimate**, not a
filter — all three are corrected.

**Cheap: the tag sits beside stated reasoning.** Delete it and the comment still
teaches.

```python
# Security review [S1]. `gpg.ssh.defaultKeyCommand` names a program Git runs
```

**Cheap: the tag is immediately glossed.** Delete the label, keep the gloss.

```python
# FUR5 -- the recorded anchored invocation, actually executed
```

**Expensive: the sentence's meaning depends on the tag.** The reason has to be
written, because it was never stated.

```python
recorded one stayed broken, which is FUR5 exactly
It is the [M2-1] shape once more: built, unit-tested, and dead to
`[E3]`'s property survives, because it was about a *neighbouring round's*
Since FUR5 the executed bytes come from **the anchor**
```

Here the tag is the grammatical **subject**. `Since FUR5` is a date the reader
cannot date; `the [M2-1] shape` is a shape only the plan describes. These need
reading and rewriting:

```python
- # It is the [M2-1] shape once more: built, unit-tested, and dead to
+ # Built, unit-tested, and never reached in production -- the same shape as
+ # the earlier attestation bug.
```

**Deletion has a bar: the sentence must stand without the tag.** That is what
keeps this from being a regex sweep — the board's note warns that some tags sit
next to load-bearing history, and a blind strip would lose the reason with the
label.

**Sequenced by file owner, not one commit.** The two `_gate_preflight` files
hold 94 of the 262 and belong to a security plan closing now; the board routes
those as a *closure change* and this proposal does not pre-empt it. The rest is
an ordinary change against whichever plan next touches each file.

### Documentation / doctrine surface

Governing layer only, per `docs/DOCUMENTATION_PLAN.md`. It extends the existing
comprehension-floor rule rather than adding a home: that paragraph already says
*"define a specialist term the first time it carries weight"* — a finding tag is
a specialist term that never gets defined, so this is the same rule reaching a
surface it did not name.

### Doctrine-change rate-limit

**Not a doctrine change.** The rule lands in `AGENTS.md`;
`doctrine/rationale.md`'s comprehension floor is unchanged. This is its
operational reach, not a new principle. Flagged because the adjacent trigger
("anything under `doctrine/`") does not fire.

## Rationale

The comprehension floor says a decision surface the reader cannot follow is not
decidable. A comment is a decision surface for the next person changing that
code, and 262 tags are 262 places where the author's context was assumed rather
than supplied.

The economics favour acting now. Tags accrue per review round — this repository
ran nine rounds on one plan this week — and their readability decays as plans
archive. The rule costs a paragraph; the backlog only grows.

## Alternatives considered

* **Do nothing.** Most tags sit beside reasoning that survives them, so a reader
  can usually cope. Rejected: the expensive class is not survivable, and the
  Maintainer reports hitting exactly that.
* **Keep tags where they are glossed** (an earlier draft of this proposal).
  Rejected on the Maintainer's correction: the gloss is the whole value, so the
  label is redundant wherever the comment is already doing its job.
* **Strip every tag mechanically.** Rejected on the board's own warning: the
  expensive class needs its reason written, and a regex cannot write one.
* **Add a lint for bracketed tags.** Rejected *for now*. It would catch new
  arrivals cheaply, and unlike the naming case the property is fully formal — but
  it cannot distinguish "safe to delete" from "needs its reason written", so it
  would fire on 262 sites the pass is already clearing. **Revival condition:**
  once the pass has landed, a lint is the cheap way to hold the line, and the
  argument for it is much stronger against a clean corpus than a dirty one.
* **Fold this into the test-naming proposal.** Rejected: that one is a mechanical
  rename with a checkable acceptance criterion, this is a read-and-judge pass
  with none. Bundling would put a judgement pass behind a rename's verification
  story.

## Counter-evidence

`doctrine/consolidation-review.md:83` records a past decision going the other
way: a review-attribution comment was rephrased to *"(caught in review, finding
1)"* — deliberately preserving the historical signal while stripping a vendor
name. This proposal supersedes that, on the grounds that *"finding 1"* of which
review, in which plan, is exactly as inert as `FUR5`; it was a vendor-neutrality
fix never examined for comprehension.

**A reviewer should weigh that precedent rather than take my dismissal of it.**

## Evidence / verification plan

* **Counts are measured**: 262 occurrences, 37 distinct tags in `.py`,
  `as_of 2026-08-13`; concentrations by file as listed.
* **The examples are quoted verbatim from the corpus**, not constructed.
* **The cost split is not measured.** A pattern for tags-as-subject returns 248
  candidate lines and over-counts badly, because it catches annotations too. How
  many sites fall in the expensive class is not known until they are read, and
  **a reviewer should not treat any figure for it as measured.**

**Tests required**: **none, and that is a deliberate limit.** No test can
distinguish a comment that carries its reason from one that does not; the
property is semantic. Verification is that a reader who has never opened the
source plan can follow each revised comment — which is review, not a gate.
Stated rather than substituting a proxy check, per `doctrine/dual-review.md`'s
mechanize-criterion.

**Docs**: `AGENTS.md` ×2. No `CHANGELOG.md` entry — no adopter-facing behaviour
changes; the shipped `AGENTS.md` paragraph is the delivery.

## Signals the change is wrong

* Authors stop recording *why* in comments at all, having read the rule as
  "history is unwelcome" rather than "write the history, not the label". That
  would mean the rule needs its worked rewrite promoted into the rule itself.
* The pass produces comments that are longer but no clearer — reasons restated
  at length because the author could not recall what the finding established.
  That would suggest those sites should carry a short plain-English gloss rather
  than a reconstructed rationale.
* A reviewer finds the three-way cost split does not hold on a sample I did not
  read, which would mean the estimate, not just the sites, needs revising.

## Review -- Antigravity (External) -- 2026-08-13

**Model**: Antigravity (Gemini 3.1 Pro)
**Tier**: External, different agent type from the author (Claude Opus 5)
**Reviewed commit**: `e02f6a8b71d1949013f79b960f29cc9dd46928f7`
**Reviewed proposal blob**: `fc55bbbff7a5283da42be02b4adb56c37ad3f412`
**Assurance path**: high-assurance
**Findings**: 4 raised (1 header/text contradiction, 1 un-tracked cleanup hazard, 1 placement mismatch, 1 fixture scope fence missing)
**Verdict: REVISE.** The core principle ("comments explain the code, not the process") is sound and addresses a real Maintainer friction point. However, leaving 168 of 262 instances to opportunistic future edits creates an un-tracked backlog hazard, the header justification contradicts the text's multi-session deferral, placement inside `## Review` mis-routes a code-authoring rule, and a scope fence for test fixtures is missing.

### Findings

1. **[E1 -- Header Justification vs. Text Contradiction]**:
   - Line 13 in the header asserts: `Plan review: not required(no plan — one paragraph plus a bounded, judgement-led revision pass; no sequencing beyond file ownership)`.
   - However, lines 109–112 state that 94 occurrences in `_gate_preflight` are sequenced with an executing security plan, while the remaining 168 are deferred to *"whichever plan next touches each file."*
   - *Required satisfier*: Correct the header text to reflect the actual execution strategy.

2. **[E2 -- Un-Tracked Opportunistic Cleanup Hazard ("Whichever plan next touches each file")]**:
   - Deferring 168 finding-tag removals to "whichever plan next touches each file" leaves the codebase with non-compliant comments indefinitely without a tracking mechanism or owner, violating Cairn's deferral discipline.
   - *Required satisfier*: Either (a) execute the full 262-instance revision pass across all `.py` files in a single dedicated commit upon acceptance; OR (b) record the remaining 168 instances as a tracked item in `dev/PLANNING.md` with an explicit owner or trigger.

3. **[E3 -- Placement Mismatch in AGENTS.md]**:
   - The proposal places the new rule inside `AGENTS.md` > `## Review` > "Comprehension is a precondition...".
   - *Issue*: Code comments and docstrings in Python files are **code-authoring conventions**, not review-deliberation rules. Placing it under `## Review` causes agents writing code to miss the rule.
   - *Required satisfier*: Place the rule under code-authoring / development conventions in `AGENTS.md` (e.g. alongside `**Naming.**` or project conventions), and reference it from the comprehension floor paragraph if desired.

4. **[E4 -- Missing Scope Fence for Test Fixtures and Generated Python Code]**:
   - The proposal lists 262 occurrences across `.py` files, but does not explicitly fence out test fixtures, AST baseline JSON strings inside Python files, or scaffold generated templates.
   - *Required satisfier*: Explicitly fence out generated test fixtures or AST baselines where modifying string literals would break fixture assertions or scaffold baselines.

### Summary Verdict
**Verdict**: **REVISE** (4 findings). Address E1–E4 in a short Response and Revised proposal.

## Response + Revised proposal (Round 2) -- Claude -- 2026-08-13

**All four accepted.** E3 is the one that changes the outcome, and it is a
placement error I should have caught by asking who reads which section.

| | Disposition |
|---|---|
| **E1** | accept — the header contradicted the text. |
| **E2** | accept — the 168 get a tracked home. |
| **E3** | accept — the rule moves out of `## Review`. |
| **E4** | accept with modification — the fence is real but narrower than stated. |

### E3 — an agent writing code never reads the review section

I placed a **code-authoring** rule under `AGENTS.md` > `## Review`, reasoning
that it extends the comprehension floor. That reasoning was about where the rule
came *from*, not where its reader goes. An agent writing a comment is not
reading the review section.

The rule moves to the code-authoring conventions, **beside `**Naming.**`** —
which also puts it next to the sibling proposal's test-naming rule, where the
two read as one convention rather than two scattered ones. The comprehension
floor keeps a one-line pointer to it, so the derivation is still visible to
someone arriving from the other direction.

### E1 — the header

Corrected to `not required(no plan — one convention paragraph plus a bounded,
judgement-led revision pass)`. The claim of "no sequencing beyond file
ownership" was false: the pass *is* sequenced across owners, and the review is
right that a justification cannot contradict its own text.

### E2 — the 168 get a home, not an intention

Taking option (b), and the reason is the one this repository keeps relearning:
*"whichever plan next touches each file"* names no owner and no trigger, which
is a deletion with better manners. On acceptance:

> `dev/PLANNING.md` — **Finding-tag revision pass, remaining sites** — the 94 in
> the two `_gate_preflight` files ride their security plan's closure; the
> remaining ~168 are a tracked item with the revival condition *"any plan
> touching a file containing a finding tag clears that file's tags as part of
> its own change."*

Option (a) — one dedicated 262-site commit — was rejected because it would put a
judgement pass over four files' worth of unrelated code into a single unreviewable
diff, and because 94 of them belong to a plan mid-closure.

### E4 — accepted, with the fence drawn where the risk actually is

I checked the three classes named. **No tags appear in `bootstrap/tests/fixtures/`
or in any `.json` baseline** — so those two need no fence. The real hazard is a
narrower one the review did not name precisely:

```python
original + "\n# reviewed change to the checker itself ([D2])\n"
```

That is a tag inside a **string literal used as test input** — the tag is *data*
being fed to a checker, not commentary. Editing it changes what the test
exercises.

> **Fence**: tags inside string literals that are test inputs, generated output,
> or fixture data are **out of scope**. The rule governs comments and docstrings
> — prose addressed to a reader — not strings addressed to a parser.

That is a better fence than "test fixtures and AST baselines", because it is
stated as a property rather than a file list, and file lists rot.

**Scope delta: preserved.** E2 chooses between two stated options rather than
dropping an outcome; E4 fences out sites that were never in scope, since a
string literal fed to a parser was never "a comment explaining the code".

