<!-- cairn-internal-ref-allow: doctrine/rationale.md doctrine/dual-review.md doctrine/proposals.md doctrine/doc-governance.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see AGENTS.md, "Where doctrine/ references resolve") -->

# Five questions a security-touching change answers *before* review — extending the Author-accounting block

**Author**: Claude (Strategy)
**Model**: Claude Opus 5
**Date opened**: 2026-08-03
**Status**: proposed
**Touches**: the `### Author-accounting` block in `dev/proposals/_template.md` and
its shipped twin `templates/core/dev/proposals/_template.md` (a new `####`
sub-block, about 40 lines); one clause in the same block in `dev/plans/_template.md`
and its twin `templates/core/dev/plans/_template.md`; one new test in
`bootstrap/tests/test_scaffold.py`; `CHANGELOG.md`; one `dev/PLANNING.md` row.
**Deliberately not touched**: `doctrine/` (nothing under it), `AGENTS.md`, the
install manifest's row set, `bootstrap/_scaffold/`, and every gate script. The
routing argument for leaving `doctrine/` alone is in *Documentation / doctrine
surface*; it is a decision, not an oversight.
**Related**: the superseded `identity-not-name` proposal and its Response, which
recorded the 07:59 measurement this proposal is built on; the archived
`gate-reanchor-preflight` plan, whose [CR1] finding and Chunk E mutation
discipline are two of the five questions already in practice; the
`release-authenticity` proposal and its Internal security review, whose
tag-substitution finding is the fourth instance; `scan-coverage`, which measured
the anti-drift assertion that cannot fail; `gate-claims-vs-enforcement`, whose
twelve-row ledger is the evidence for S3; `byline-classification`, whose
homoglyph defect is the evidence for S4; `content-scan-detectors`, which
recorded that `content-security` is selected by no preset
**Plan review**: not required — the accepted change is a single implementing
commit over four Markdown template files (one added sub-block, one added
clause), one added test, and two record files. No plan, therefore no plan
review. If the Maintainer prefers a plan anyway, **Internal** is the ceiling: no
`doctrine/` file, no `AGENTS.md` rule, no manifest row, no engine code and no
gate script is touched. Ratified at Decision.

## Context

### The felt pain, in the Maintainer's words

  what we did felt like a blind person stumbling into walls and just being told
  'nope, not done yet'. Can we be more forward-looking?
  I need to figure out how to get to a secure interface with less manual
  back-and-forth.
### The mechanism behind the pain

Every gate in this repository is **diagnostic**, never **specificational**. A
review says *this is wrong*. Nothing anywhere says *here is the complete set of
properties this must satisfy*. So each round discovers one more property, and the
horizon recedes by exactly one step. Rounds do not converge because there is no
stated set to converge on.

The release-side half of that problem — *what does secure-enough-to-ship mean for
the release* — is a separate question, and a release-readiness bar is being
drafted concurrently under its own lifecycle (its filename stem is not fixed at
the time of writing, so it is not cited here as one). **This proposal is the
other half: what does done mean for a single change, checked at authoring time,
before a reviewer ever reads it.** The two compose and neither substitutes for
the other; see *Relationship to the release bar* below.

### The measurement that decides the design

Cairn's record contains a specific, dated observation that rules out the obvious
answer ("be more careful"). From the `identity-not-name` Response, recorded by
its own author against himself:

> the author found CR1 at 07:59 and then wrote two fresh instances of the
> identical class into this proposal within the hour. Vigilance did not catch it;
> an adversarial reviewer did.

The knowledge existed. It had been written down, in this repository, that morning.
It was not in a form that **applied at authoring time**, so it did not apply.

That is the whole argument. A reminder to be careful is a bet on vigilance, and
vigilance has a measured failure rate here: **the same failure shape appeared four
times in one week, and four different readers caught it — never the author.**

| # | Instance | Where | Who caught it |
|---|---|---|---|
| i | The gate checker resolved its allowed-signers roster through the **candidate** repository's `.git/config` — the artifact chose whose signatures count. | `gate-reanchor-preflight` plan, finding [CR1]; fixed at `0c6d9de` | an Internal plan review |
| ii | A proposal specified verifying a release tag against a roster **committed inside that tag**. | `identity-not-name`, finding [IDN1] | an External review |
| iii | A proposal specified comparing against *"the upstream present on disk"*, where the target supplies the path. | `identity-not-name`, finding [IDN4] | the same External review |
| iv | **Today.** An attacker with forge write access and **no signing key** repoints `refs/tags/v0.5.0` at the genuine `v0.3.0` signed tag object; the documented bootstrap exits 0 with `Good "git" signature` while `git cat-file tag` reports `tag v0.3.0`. | `release-authenticity`, Internal security review, finding [I1] | an Internal security review, in the resolver written to close instance ii |

One shape: **the artifact under verification supplies the material used to verify
it.** Instance iv is the sharpest, because it landed *inside the fix for instance
ii*, in a document whose own author had already written the rule down.

### The slot already exists — and that is the point

Cairn is not missing a forward-looking mechanism. The `### Author-accounting`
block in `dev/proposals/_template.md` already asks the author for invariants,
failure modes, an edge-case inventory, and a public-path-to-test mapping, and it
already states its purpose in exactly the right words:

  collapsing the review from "find the absence" to "check this claim
The block is byte-identical to its shipped twin at
`templates/core/dev/proposals/_template.md`, so adopters already receive it.

**What went wrong today is not that the slot is missing; it is that the slot was
filled descriptively.** Read the security proposals opened on 2026-08-03: their
Author-accounting blocks are excellent *documentation of a finished design*. They
record what the author decided. They are not the questions the author asked while
deciding. A block filled after the design is fixed cannot change the design, and
therefore cannot prevent the shape it would have caught.

So this proposal adds no new artifact and no new ceremony. It adds five questions
to a block that already exists, with wording that makes them design questions
rather than documentation, and gates them to security-touching changes.

## Proposal

### The five questions

Added to the `### Author-accounting` block in `dev/proposals/_template.md` and
its shipped twin, as a `####` sub-block. Verbatim proposed text:

> #### Security preflight — five questions, answered in writing
>
> *Gated to a **security-touching** change: one that adds, moves, or widens a
> trust boundary (deserialization, subprocess invocation, parsing, file and path
> handling, network I/O, credentials and environment — the `security-review`
> module's boundary list), or one that touches a high-risk surface this project's
> `AGENTS.md` names. For every other change, one line — "N/A: no trust boundary
> added, moved, or widened" — is the correct entry.*
>
> Answer all five, one or two sentences each. These are **design questions, asked
> while the design is still movable** — not documentation written after it is
> fixed. An absent answer is a review finding. A *wrong* answer is a falsifiable
> review finding, which is the point: the reviewer checks a stated claim in one
> read instead of hunting for an absence over four rounds.
>
> * **S1 — Who supplied it?** For each step where this change *decides* something
>   (verifies, authenticates, authorizes, classifies, admits), name every input
>   and the channel it arrives by, and say whether any input is supplied —
>   directly or **by reference** — by the thing being decided about. Apply this to
>   every step in the change *and to every step you describe in prose in this
>   document*.
> * **S2 — Can it fail?** For each test or check this change relies on to enforce
>   an invariant, state the one-line mutation that makes it fail, and confirm you
>   ran it. If a check derives what it expects from the same object it is
>   checking, say so plainly — that check cannot fail.
> * **S3 — What fires it, over what?** Name the command that runs the check, what
>   selects it (a preset, a profile, a suite, or nothing), and the exact input set
>   it covers. Then quote the sentence in adopter-facing prose that describes it,
>   and show the two agree.
> * **S4 — Which way does it break?** For each default, fallback, normalization,
>   and parse-error path this change adds or touches, say which side of the
>   boundary it lands on when it goes wrong — and whether that is *more* authority
>   or less.
> * **S5 — Who still wins?** State the attacker capability this change assumes,
>   then name one capability that still succeeds after it. If you cannot name one,
>   say whether the class is closed **by construction** or merely **by
>   enumeration** — enumeration ages.
>
> **What these five do not reach.** They are structural questions about where
> material comes from and what runs. A semantically valid instruction that is
> hostile carries no lexical signature, and no question here finds it. They also
> do not check whether an answer is *true* — they convert a hidden property into a
> written claim a reviewer can falsify.

### Each question is an existing lesson, given a home that applies at authoring time

This is the "build nothing new" argument, made question by question. Every one of
the five is already written down somewhere in this repository. None of them was
in a place that applied while a design was being written.

| Q | Where the lesson already lives | Why it did not apply |
|---|---|---|
| **S1** | The `identity-not-name` Response states the invariant *"the artifact under verification must not supply the material used to verify it"*, and proposes the channel discipline as *"an observation for the successor plans to carry, not as a new mechanism."* `release-authenticity` then mandates it — for its **plan reviewer**. | It is a reviewer's instrument. The author who wrote it produced two fresh instances within the hour. |
| **S2** | The archived `gate-reanchor-preflight` plan's Chunk E discipline: *"Every test is shown non-vacuous by mutation: remove the check, confirm the test fails, restore the source byte-identical."* | It is a plan-chunk convention in one archived plan. Archived plans are not read. |
| **S3** | `gate-claims-vs-enforcement` is a twelve-row ledger of documents naming a gate nothing fires. | It is a retrospective sweep of existing prose. Nothing stops row thirteen being written tomorrow. |
| **S4** | `byline-classification` and `profile-parse-fail-open` both turn on which side a degraded path lands on. | Both are diagnoses of shipped code, written after the code shipped. |
| **S5** | `release-authenticity`'s residual RA5 is the model answer: *"the candidate-git-config class is closed for this surface, not swept... I found `gpg.ssh.program` by looking for it."* | Written as a residual at the end of a design, not as a constraint at its start. |

### The evidence behind each question, so none is speculative

* **S1 — four instances, four subsystems, one week.** The table in *Context*. Note
  the phrase *by reference*: instance i was not a bad roster, it was a roster whose
  **location** the candidate chose. The same proposal later found that a
  candidate's `gpg.ssh.program` names the **program git runs to verify**, so a
  correct roster passed on the command line was consulted by nothing real. "Who
  supplied it" has to reach one indirection out, or it misses both.
* **S2 — a test named "the anti-drift assertion" that cannot fail.**
  `test_scan_targets_cover_all_shipped_scripts` at
  `bootstrap/tests/test_security_lint.py:134` builds its expected set by
  comprehending over `_MODULE_MAPPINGS` — the same object the code under test
  walks. It was live and green on the day the drift it names occurred, and stayed
  green for 63 days (2026-06-01 to 2026-08-03), as measured in `scan-coverage`.
  The repository already knows the stronger shape: at
  `bootstrap/tests/test_upgrade_side_door_parity.py:158` the sibling test adds a
  hand-pinned `assert scanned == 9`, which fails loudly when the registry grows.
  S2 asks for the mutation precisely because the weaker form is the one that names
  itself anti-drift.
* **S3 — two live coverage gaps and a twelve-row ledger.** `scripts/check_cairn.py`
  leaves roughly 45 of the repository's 218 tracked `.md` files unscanned and
  reports `OK` while a real broken link sits in an unscanned file
  (`scan-coverage`, snapshot `as_of 2026-08-03`; the scanned figure moves with the
  tree, the size of the gap does not). The
  `content-security` module — the prose-injection scanner — is selected by **zero**
  presets, while two onboarding documents tell adopters it applies
  (`content-scan-detectors`). And `gate-claims-vs-enforcement` disposes of twelve
  instances of the same shape, eight of which name a CI system this repository does
  not have. S3's "quote the sentence and show the two agree" is the cheapest form of
  that whole sweep, applied one change at a time.
* **S4 — a normalization that widens authority when a character is dropped.**
  `re.sub(r"[^a-z0-9]", "", raw.lower())` at `tools/lifecycle_planner.py:251`
  strips non-ASCII, so a Cyrillic homoglyph turns `claude` into `clude`: the token
  misses the AI-agent registry and lands in the human-Maintainer allowlist
  (`byline-classification`, defect (a)). The failure direction is *outward* — less
  input produced more authority. S4 exists because nobody asks that question
  spontaneously; the natural question is "does it normalize correctly."
* **S5 — the capability nobody had written down.** The tag-substitution attacker
  holds forge write access and **no signing key**. The entire release-authenticity
  design — the roster, the bare-repository fetch, the `-c` pin, the rotation
  windows — was built against a key-forgery adversary, and it holds against that
  one. Naming the assumed capability up front is what surfaces the adversary the
  design was not built for.

### Where the questions live, and what else changes

* **`dev/proposals/_template.md`** — the sub-block above, appended inside the
  existing `### Author-accounting` section, before its closing **Prospective
  only** paragraph.
* **`templates/core/dev/proposals/_template.md`** — the identical text. The two
  copies' Author-accounting blocks are byte-identical today (verified by
  extraction and `diff`, `as_of 2026-08-03`); the differences between the files
  are confined to `cairn:slot` regions, of which this is not one. The edit lands
  in both or in neither.
* **`dev/plans/_template.md` and its twin** — one clause, because their
  Author-accounting comment already incorporates the proposal template's block by
  reference (*"same discipline as the proposal template's author-accounting"*) and
  states that at plan stage the satisfier is *sequencing*. The clause:

  > A security-touching plan re-answers the five security-preflight questions only
  > where its chunking changes an answer — most often S2 (which chunk runs the
  > mutation) and S3 (which gate command fires the check).

  **Why the plan templates are touched at all**, given the pointer already exists:
  instance i of the four — [CR1] — was written into a **plan**, not a proposal. A
  pointer that a plan author must follow to reach the questions is exactly the
  "the knowledge existed, in a form that did not apply here" failure this proposal
  is about. One clause is the smallest edit that closes it; a duplicated block
  would create a sync surface, which is the drift the wrapper drift-guard exists
  to prevent.
* **`bootstrap/tests/test_scaffold.py`** — one test, described under *Tests
  required*.
* **`CHANGELOG.md`** and one **`dev/PLANNING.md`** row for the residuals.

### What this change explicitly does not do

Stated up front, because overstating an authoring aid is how row thirteen of the
enforcement-claim ledger gets written.

* **It defines done for a change's *accounting*, not for its security.** A change
  can answer all five honestly and still be insecure. The block makes the security
  argument legible; it does not make it correct.
* **Nothing mechanical checks that a proposal answered the questions.** The added
  test checks that the *shipped template still carries them* — nothing more. The
  enforcement is a reviewer declining to review an unanswered block, which is a
  human control with the failure rate documented above.
* **It removes no attacker capability.** See S5 of this proposal's own accounting.
* **It does not change any default.** The Maintainer's 2026-08-03 direction —
  *"we need to change the default security stance for all installations"* — is
  adjacent and is not addressed here; the `content-security` preset-selection
  question named in `content-scan-detectors` is the surface that carries it, and
  it needs its own proposal.

### Relationship to the release bar

Two artifacts, two scopes, one seam:

* The **release bar** answers *is this release secure enough to ship*. It is a
  standing set of properties, checked once per release, by the Maintainer.
* The **preflight** answers *has this change stated what it must state*. It is
  five questions, answered once per security-touching change, by its author,
  before review.

Neither substitutes. A release of changes that each answered the five is not
thereby shippable; a change that answers the five is not thereby releasable. If
both land, the preflight is what makes the release bar cheap to evaluate, because
the answers it needs are already written down per change. If only one lands,
either stands alone. **This proposal makes no claim on the release bar's contents
and takes no dependency on it.**

### Documentation / doctrine surface

* **Deliberation layer** — the two `_template.md` files under `dev/` are the
  primary change. Under `docs/DOCUMENTATION_PLAN.md`'s routing, a proposal
  template is deliberation-layer scaffolding: it shapes how a change is argued,
  not what the software is.
* **Shipped templates** — the two twins under `templates/core/dev/`. These are
  **adopter-installed**, so an adopter who scaffolds after this change receives
  the five questions. The install **contract** is untouched: the manifest's row
  set does not change, only the content of two rows that already exist. This is
  the *Bootstrap fidelity / install contract* trigger in its weakest form.
* **Governing layer — none.** No `AGENTS.md` change.
* **`doctrine/` — none, and this is a routing decision.** The obvious candidate is
  a sixth lens on the review sweep in `doctrine/dual-review.md`. Declined for two
  reasons. First, that doctrine states the sweep is *"generic and
  change-agnostic — the same roster every time"*, and a security-specific lens
  contradicts it; the same doctrine sanctions *author-side* domain extension
  instead (*"each adopter extends the roster with the checks its high-risk
  surfaces demand"*). Second, and decisive: the sweep is the **reviewer's**
  instrument, and the measured failure is on the **author's** side. Putting these
  questions in the reviewer's roster would reproduce the exact defect — knowledge
  that exists, in a place that does not apply at authoring time.
* **Descriptive layer — none.** No `docs/` file changes.

**One observation, recorded and deliberately not fixed here.** The
Author-accounting block cites *"the review sweep that checks it
(`doctrine/dual-review.md`)"*, and `doctrine/dual-review.md` does not mention the
block; the nearest match is lens #3 (design completeness), which covers the
substance without naming the artifact. That is a soft reference, not a false
enforcement claim, so it is **not** treated as a finding here and **not** bundled
into this change. It is offered to `gate-claims-vs-enforcement` as a candidate row
if that author judges it in class.

### Doctrine-change rate-limit

**Applicable, and cleared on the recurrence limb.**

A reasonable reviewer will class this as a doctrine change: it adds a rule that
every contributor to a security-touching change follows, and it ships in a
template adopters install. The gate (`doctrine/rationale.md` > "How the doctrine
evolves under evidence") requires **recurrence** — *"the same failure shape occurs
again (a small count within a rolling window)"* — or a Maintainer high-risk
classification, or goodnight-time synthesis.

**Recurrence is satisfied on the primary evidence, not by analogy.** Four
instances of one shape, within a rolling window of one week (2026-07-27 to
2026-08-03), across four distinct subsystems: a gate pre-flight checker, a release
verification design, an upstream comparison design, and a tag resolver. Instances
are enumerated in *Context*, each with the artifact and the reader who found it.
The rolling-window length is Cairn's to record; one week is stated here as the
observed span, not asserted as a standing policy.

The remaining four questions clear the same limb on their own evidence: S2 has one
measured instance plus a 63-day green window; S3 has a twelve-row ledger; S4 has
two open proposals turning on the same failure direction; S5 has one instance. S1
is the limb this proposal relies on; the others are corroborating, and S5's single
instance is the weakest and is stated as such.

**The high-risk limb is available and is not claimed.** These are security
surfaces, so the Maintainer *could* classify and clear the gate that way. That
classification is the Maintainer's and is not assumed here — the recurrence limb
does not need it.

## Rationale

* **Which user workflow does it improve?** The one the Maintainer named. Today a
  security-touching change enters review with its properties unstated, so the
  review's job is to *discover* them; each round discovers one and stops. With the
  five answered, the review's job is to *falsify five written claims* — a bounded
  task with a stopping condition. That is the difference between "nope, not done
  yet" and a checkable list.
* **What contract does it preserve or clarify?** The Author-accounting block's own
  stated contract — *"collapsing the review from find-the-absence to
  check-this-claim"*. The block promises that today and, for security properties,
  does not deliver it, because it is filled after the design is fixed. This makes
  the promise true for the five properties that have actually failed.
* **What transparency or correctness does it improve?** For a scientist adopting
  Cairn, the durable value is that the record says what a change *does not*
  establish. S5 forces that sentence into every security-touching change; today it
  appears when an author is unusually scrupulous.
* **Why now?** Because the horizon receded four times in one week and the
  proposals that measured it are open *right now*. Every one of them would answer
  these five in minutes, and their reviewers would spend that review on something
  new. Waiting means the next security proposal is drafted under the same
  conditions that produced instance iv.

## Alternatives considered

* **Do nothing.** The honest case for it: every question here is already written
  down, all five lessons are in the record, and the authors are the ones who wrote
  them. Rejected on the single measurement this proposal is built on — the author
  who wrote the rule at 07:59 wrote two violations of it within the hour. Doing
  nothing is a bet on vigilance, priced at four instances per week.
* **A parallel artifact — a `SECURITY_PREFLIGHT.md` checklist, or a new proposal
  section.** Rejected, and this is the alternative with the strongest surface
  appeal. Cairn already has the forward-looking slot, and a second one splits the
  author's attention between two places, creates a sync surface between them, and
  produces exactly the fourth-doc drift the wrapper drift-guard exists to prevent.
  A checklist nobody completes is worse than none, and a second artifact is the
  most reliable way to get one.
* **Add a sixth lens to the review sweep in `doctrine/dual-review.md`.** Rejected
  on two grounds given in *Documentation / doctrine surface*: it contradicts the
  sweep's stated change-agnosticism, and it puts an author-side instrument in the
  reviewer's hands — reproducing the defect. Worth naming because it is the
  cheapest edit and the wrong one.
* **A linter that fails a proposal whose `Touches:` names a security surface and
  whose Author-accounting lacks the five headings.** Rejected for now, with a
  named revival path. It would check *presence*, and the template already warns
  that this block is *"reviewed as evidence, not accepted as a filled form"* —
  a presence gate trains authors to produce five headings with nothing under
  them, which is the ritual-drift signal `doctrine/dual-review.md` already names.
  It is also new machinery under a standing "fix defects, build nothing new"
  direction. Revival path: the open `transition-lint` proposal is the natural home
  if one is ever wanted; recorded as residual R3 rather than built here.
* **Ten questions instead of five.** Rejected on the stated design constraint: a
  checklist nobody completes is worse than none. Five is what the measured
  evidence supports — four shapes plus S5, which is the question that would have
  surfaced instance iv. A sixth question with no instance behind it is
  speculation, and speculation is what makes a checklist skippable.
* **Apply the block to every change, not just security-touching ones.** Rejected:
  a mandatory five-question security block on a typo fix is how a block becomes
  ritual. The gate reuses the trust-boundary list the `security-review` module
  already ships plus the high-risk surfaces `AGENTS.md` already names, so it
  invents no new taxonomy. The cost is that the gate is self-judged — residual R2.
* **Maintainer preference during drafting.** The framing *"can we be more
  forward-looking"* and *"less manual back-and-forth"* is cited as maintainer
  preference during drafting; it shaped the choice of an authoring-time instrument
  over another review-time one, and it is not a Decision.

## Evidence / verification plan

* **Tests** — one new test, named below.
* **Examples / smoke checks** — named below.
* **Docs** — named above under *Documentation / doctrine surface*.

Every claim above was verified against the working tree on 2026-08-03 under the
canonical interpreter (`~/conda_envs/lhm/bin/python`, 3.13.13). The two
byte-identity claims were verified by extracting the blocks and running `diff`.
The four instances in *Context* are cited from the committed record rather than
re-derived; the tag-substitution reproduction is quoted from the Internal security
review that performed it, not re-run here. **No repository byte was written while
drafting this document.**

### Author-accounting — invariants, failure modes, edge cases

* **Invariants.**
  * *The two proposal templates' Author-accounting blocks stay byte-identical.*
    Enforced today by convention only; this change does not add an enforcer, and
    says so. The pre-existing enforcer is the fidelity check listing both files.
  * *The shipped proposal template carries all five question headings.* Enforced
    by the new test below.
  * *The install manifest's row set is unchanged.* Enforced by the assertion that
    `python bootstrap/scaffold.py --manifest` produces a byte-identical diff.
* **Failure modes.** The change is prose in a template plus one presence test.
  The test is **closed** (asserts, raises). The gating clause is deliberately
  **open**: an author who judges their change not security-touching writes one
  N/A line and nothing checks the judgment. That is intentional — see
  *Alternatives* — and is residual R2.
* **Edge cases.** Handled: an adopter who installed before this change (their
  template is unchanged until they upgrade — this adds no upgrade obligation); a
  proposal that is security-touching but adds no test (S2's honest answer is "no
  new check; the invariant rests on X", which is itself the finding); a plan whose
  proposal predates this change (residual R1). Out of scope: proposals already
  open on 2026-08-03 — the template block is **prospective only**, per the
  paragraph it sits inside, and no open or archived artifact is retro-fitted.
* **Public-path → test mapping.** The change adds no code entry point. The one
  public surface is the *installed* template, whose entry point is
  `install_core`; the new test in
  [`bootstrap/tests/test_scaffold.py`](../../bootstrap/tests/test_scaffold.py)
  drives that function and asserts against the installed file, matching the
  existing `test_installed_templates_carry_plan_review_line` in the same class.
  The link resolves to the existing test **file**; the added test **node** does
  not exist yet, which is the one thing the template's link form cannot express.
* **Known omissions / intentionally untested edges.** Nothing tests that a
  proposal answers the questions; nothing tests answer quality; nothing tests the
  plan-template clause beyond its presence in the file.

#### Security preflight — this proposal's own five answers

Dogfooded, both to demonstrate the form and to show it fits in a screen.

* **S1 — Who supplied it?** This change makes no decision at any step: it adds
  prose to a template and a presence assertion. Its one input is
  `templates/core/dev/proposals/_template.md`, read by `install_core` from the
  Cairn tree being installed *from* — never from a candidate tree under
  verification. No input is supplied, directly or by reference, by anything being
  decided about.
* **S2 — Can it fail?** The new test's expected set is a **literal list of five
  strings written in the test**, deliberately *not* derived from the template —
  deriving it from the template is precisely the anti-drift failure at
  `bootstrap/tests/test_security_lint.py:134`. Mutation: delete any one heading
  string from the shipped template and the test fails on that string. **Not yet
  run** — this draft writes no repository bytes; running it is the implementing
  commit's first step, and if it does not fail, the test is wrong.
* **S3 — What fires it, over what?** `python -m pytest bootstrap/tests` runs it;
  nothing selects it conditionally except the existing
  `pytest.skip("Cairn templates not available")` guard shared with its sibling,
  which does not fire on the canonical host (if it ever does, the gate's *0
  skipped* rule fails, which is the correct direction). It covers the **installed
  template's text and nothing else**. The adopter-facing sentence describing it is
  the *What this change explicitly does not do* section above, which states that
  scope in those words.
* **S4 — Which way does it break?** No default and no fallback in the added text.
  The gating clause is the one degraded path: a mis-judged N/A skips the block,
  and the failure lands on the **less-scrutiny** side. Intentional, priced in
  *Alternatives*, recorded as R2. The test has no fallback — a missing heading
  fails.
* **S5 — Who still wins?** This change assumes **no** attacker capability and
  removes **none**. Every attack that succeeded before it succeeds after it. What
  changes is the round in which a defender is likely to notice. Stated that flatly
  because the alternative — implying an authoring aid is a control — is the exact
  overstatement this proposal exists to prevent.

### Tests required

One new test in `bootstrap/tests/test_scaffold.py`, in the class that already
holds `test_installed_templates_carry_plan_review_line`:

* `test_installed_templates_carry_security_preflight_questions` — installs core
  into a `tmp_path` via `install_core`, then asserts the installed
  `dev/proposals/_template.md` contains each of five literal heading strings
  (`S1 — Who supplied it?` … `S5 — Who still wins?`) and the gating phrase
  `no trust boundary added, moved, or widened`, and that the installed
  `dev/plans/_template.md` contains `security-preflight`. Expected strings are
  literals in the test body, never derived from the template.

**What this test does not do**, stated in its docstring so nobody later reads it
as more: it pins the shipped template's text against silent regression. It does
not check that any proposal answers the questions, and no test can.

The `bootstrap/tests` suite must remain all-green with 0 skipped and 0 xfailed on
the canonical interpreter, with collection grown by exactly one node.

### Examples / smoke checks

* `python scripts/check_cairn.py` — the prose-integrity gate, for four Markdown
  files plus this proposal.
* `python scripts/claim_check.py <file>` over this proposal and over each edited
  template, one file per invocation.
* `python scripts/quality_gate.py --sub neutrality` — the added text names no AI
  model or vendor; this is the gate that proves it, and it is the gate a shipped
  template change must clear.
* `python bootstrap/scaffold.py --manifest` — expected **unchanged**. The empty
  diff is the assertion that the install contract's row set is untouched.
* `python scripts/token_budget.py` — expected unchanged. The always-on budget
  covers `AGENTS.md` and `CLAUDE.md` only (5,419 tokens total, `as_of
  2026-08-03`); the proposal template is read on demand, so ~40 added lines cost
  nothing against the standing budget. Named because "does this bloat the
  always-on context" is the first fair objection to any template addition.
* `python -m pytest bootstrap/tests` under the canonical interpreter (3.13.13).

## Residuals and their expiry triggers

Each residual names the place its trigger will actually be read from, because a
trigger recorded only in a proposal is inert once that proposal archives.

| # | Residual | Why accepted | Expiry trigger | Where the trigger lives |
|---|---|---|---|---|
| **R1** | The plan templates get a **clause**, not the block. A plan author who never opens the proposal template gets a pointer, not the questions. | Duplicating the block creates a sync surface between four files; the plan block already incorporates the proposal block by reference. | The first security-touching plan whose source proposal predates this change — its author has no answered block to inherit. | a `dev/PLANNING.md` row |
| **R2** | The security-touching gate is **self-judged**. Nothing checks an N/A line. | The alternative — every change answers five security questions — is how the block becomes ritual. | Any review that finds a security-touching change which wrote the N/A line. That is a countable event; the second occurrence is the trigger. | a `dev/PLANNING.md` row |
| **R3** | **Nothing mechanical fires.** Enforcement is a reviewer declining to review an unanswered block. | A presence gate trains empty headings, and building one contradicts the standing "fix defects, build nothing new" direction. | The `transition-lint` proposal landing a lifecycle linter with a place to add a presence check cheaply. | a `dev/PLANNING.md` row |
| **R4** | **Five shapes, not all shapes.** A sixth failure shape still recedes the horizon by one step. | Five is what the evidence supports; a speculative sixth is what makes a checklist skippable. | The first security finding that fits none of the five. At that point the shape has an instance, and the recurrence limb applies to adding it. | a `dev/PLANNING.md` row |

## Signals the change is wrong

* **The answers converge on boilerplate across changes** — the same five sentences
  with the nouns swapped. `doctrine/dual-review.md` already names this as the
  sweep-going-ritual signal, and it applies identically here. *Recovery:* cut to
  the two questions with the strongest evidence (S1 and S2) or delete the block —
  a ritualized block is worse than none, and this proposal's own argument commits
  it to that conclusion.
* **Authors fill the block after designing, exactly as they do today.** The tell
  is that no answer records a *change* to the design. *Recovery:* the wording is
  wrong, not the mechanism — move the block above `## Proposal` in the template so
  it is physically impossible to fill last. That is a one-line move and it is the
  first thing to try.
* **A security-touching change lands with all five answered and the defect is one
  of the five shapes anyway.** *Recovery:* the question's *wording* failed. Quote
  the answer that passed and the defect it missed, and sharpen that one question —
  which is a single-instance doctrine change and needs the Maintainer's high-risk
  classification.
* **The block adds a review round rather than removing one** — reviewers now argue
  about the answers on top of hunting for absences. *Recovery:* this would mean the
  answers are not being treated as falsifiable claims. Watch the first two
  security reviews after this lands; if the review length grows, revert. The block
  is four Markdown files and one test, so reverting is cheap and total.
* **An adopter finds five security questions in their proposal template
  bewildering.** The postdoc adopter is the test. *Recovery:* the N/A line is the
  designed exit, so the failure would be that the gating clause is unclear.
  Shorten the gate to one sentence naming trust boundaries and drop the
  cross-reference.

## Maintainer decisions

**A note on this section.** An earlier draft supplied, for each option, a
pre-written sentence for the Maintainer to say back. Those have been removed.
Cairn's scribing guard-rail requires the authorization be quoted **verbatim**,
because a paraphrase "admits semantic drift, condition-softening, or a
hallucinated approval" — and a sentence an agent wrote for the Maintainer to
repeat is the agent's decision wearing the Maintainer's name. The options below
describe what each choice means; the wording of any authorization is the
Maintainer's own.


The Maintainer is away. Nothing above assumes approval. Two decisions are theirs;
both have a recommendation, and each option below describes what it means.

**Decision 1 — accept or not, and at what scope.** *Recommended: option A.*

* **A (recommended, both templates).**
  > *"Accepted. Add the five-question security-preflight sub-block to both
  > proposal templates and the one-clause pointer to both plan templates, with the
  > test in `test_scaffold.py`. The rate-limit gate is cleared on the recurrence
  > limb; I am not adding a high-risk classification."*
* **B (proposal templates only).**
  > *"Accepted, proposal templates only. Leave the plan templates alone — the
  > 'same discipline' pointer already covers them. Record R1 as widened."*
* **C (narrower still — no shipped change yet).**
  > *"Accepted for `dev/` only. Do not touch `templates/core/` until we have run
  > the five questions on two of our own security proposals."*
* **D (reject).**
  > *"Rejected. The lessons are already in the record; I do not want a fifth place
  > to keep them."*

**Decision 2 — the plan-review tier.** *Recommended: no plan.*

* **A (recommended).**
  > *"No plan needed — land it as one implementing commit."*
* **B.**
  > *"Open a plan; Internal review is enough."*

**Not a decision, recorded so it is not mistaken for one:** whether a release bar
is adopted is a separate lifecycle. This proposal neither depends on it nor
constrains it.

## Review -- Gemini Flash (External, security lens) -- 2026-08-03

**Steelman.** This proposal targets a well-documented failure mode in Cairn's development process: security guidelines written as reviewer instruments rather than authoring-time design constraints. The proposal adds five structured questions (S1: Who supplied it?, S2: Can it fail?, S3: What fires it, over what?, S4: Which way does it break?, S5: Who still wins?) directly into the proposal template's existing `Author-accounting` block. By forcing authors to state trust material provenance, mutation failure behavior, and residual attacker capabilities while the design is still being written, it shifts security evaluation from open-ended discovery to falsification of explicit claims.

### Concerns

* **[E1] Lack of automated presence or quality enforcement.**
  As acknowledged in residuals R2 and R3, no linter or automated check verifies that an author has answered S1–S5 accurately or refrained from marking a security-touching change as "N/A". Enforcement relies entirely on reviewers holding authors accountable during review.
* **[E2] Risk of ritualization and boilerplate responses.**
  Complex checklists risk becoming copy-pasted boilerplate over time. The proposal explicitly includes a recovery signal (cutting to S1 and S2 if responses become ritualized), which reviewers must actively monitor.

### Covered

* **Claim-check and Manifest Integrity Verification**:
  - `claim_check.py`: verified clean output on `dev/proposals/2026-08-03-claude-security-preflight-checklist.md`.
  - `scaffold.py --manifest`: confirmed that template additions do not alter the install manifest row set.

```
$ ~/conda_envs/lhm/bin/python scripts/claim_check.py dev/proposals/2026-08-03-claude-security-preflight-checklist.md
claim_check: dev/proposals/2026-08-03-claude-security-preflight-checklist.md -- OK, no claim-check flags.
```

```
$ ~/conda_envs/lhm/bin/python bootstrap/scaffold.py --manifest
# Cairn install manifest (destination<TAB>source<TAB>verbatim|substituted)
[... 94 entries, 0 diff vs expected manifest ...]
```

### Not covered / low confidence

* Long-term behavioral impact on authoring patterns across different AI models and human contributors was not empirically evaluated.

### Recommendation

**SHIP.** The proposal's five preflight questions directly address four real security incidents in the repository's record and add no unnecessary build tooling or process overhead.

