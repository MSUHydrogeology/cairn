<!-- claim-check-allow: scripts/content_scan.py, scripts/run_security_audit.py, dev/modules/content-security.md -->
<!-- ^ Three ADOPTER-TREE DESTINATION paths in the B6 reach table. They are the
     paths these controls occupy in an installed target, and they do not resolve
     in Cairn's own tree precisely because no preset installs them -- which is
     the finding B6 records. Their sources resolve and are named in the table's
     footnote. This is the self-host citation gotcha noted in AGENTS.md, in its
     inverted form: not a dev/ path that now resolves, but an installed path
     that never will. -->

# The v0.4.0 release security bar — a written definition of secure-enough-to-ship, so the horizon stops receding

**Author**: Claude (Strategy)
**Model**: Claude Opus 5
**Date opened**: 2026-08-03
**Status**: proposed
**Touches**: nothing yet. On acceptance this opens one new plan
(`release-security-bar`, forward-referenced below) and adds one row plus one
precondition clause to `dev/PLANNING.md` at the plan-open serialization point.
**Deliberately not touched**: `bootstrap/verify_integrity.py`,
`doctrine/runtime-contract.md`, `bootstrap/SAFETY.md`, `AGENTS.md`,
`SECURITY.md`. This proposal **measures** a live defect in the first and quotes
overstated sentences in the next three, and **hands every one of them off** to
the lineage that already claims the file. Recorded in the header so a reader can
tell a routing decision from an oversight without reading to the hand-off table.
**Related**: the four instances of the trust-material failure shape recorded on
2026-08-03 — `gate-reanchor-preflight` finding CR1 (fixed, commit `0c6d9de`),
the External Security Review findings **[IDN1]** and **[IDN4]** on the
superseded `identity-not-name` proposal, and the Internal security-lens finding
**[I1]** on `release-authenticity`; the twelve-row enforcement-claim ledger in
`gate-claims-vs-enforcement`; the vacuous-regression-test addendum in
`scan-coverage`; the homoglyph byline fold in `byline-classification`; the
fail-open profile parser in `profile-parse-fail-open`; the public-launch
sequence in `dev/PLANNING.md` > "Where the project stands"
**Plan review**: required(External) — see *Why this tier*. In short: the whole
value of this artifact is that a *different* reader can hold the tree to it, and
a bar that only its own author has read is a private checklist, not a shared
target.

## Context

### The felt pain, in the Maintainer's words

> "what we did felt like a blind person stumbling into walls and just being told
> 'nope, not done yet'. Can we be more forward-looking?"

> "I need to figure out how to get to a secure interface with less manual
  back-and-forth.

That is a request for a **stopping rule**. This proposal argues the stopping
rule is missing for a structural reason, and supplies one.

### The diagnosis: every gate here is diagnostic, none is specificational

Two kinds of check exist, and this repository has built many of one kind and
none of the other.

* A **diagnostic** check answers *"is anything wrong with this?"* It reports
  findings. Its output is a list that grows when someone looks harder. It has no
  natural end, because "no finding this pass" is not the same as "nothing left".
* A **specificational** check answers *"does this satisfy the following stated
  properties?"* It reports per-property verdicts against a list fixed *before*
  the check ran. It ends when the list is exhausted.

Every security gate in this tree is diagnostic. `bootstrap/security_check.py`
reports Bandit findings. `scripts/check_cairn.py` reports broken links and
claims. A review appends numbered concerns. Each is genuinely useful and each is
open-ended by construction, and **nowhere in this repository is there a written
statement of what secure-enough-to-ship-v0.4.0 means**. So each review round
discovers one more property that was always required but never written down, and
the horizon recedes by exactly one step. Not because reviewers are being
difficult — because there was never a target to be short of.

The receding horizon is not a review-quality problem. It is a **missing
specification**. That is the defect this proposal fixes, and it is a defect of
exactly the kind the two standing directions cover: it is the thing most likely
to burn the first external adopter's first two weeks (postdoc-first), and
fixing it writes a document rather than building a tool (fix defects, build
nothing new).

### The evidence this bar is built from, not imported from best practice

Every item below is justified by an instance that actually occurred in this
repository. Nothing is here because a checklist somewhere else has it.

**One failure shape, four recorded instances, all on 2026-08-03.** *The artifact
under verification supplied the material used to verify it.*

| # | Where | What happened |
| --- | --- | --- |
| CR1 | the gate pre-flight checker | `check_signatures` resolved its allowed-signers roster through the **candidate** repository's own git config, so the tree being inspected chose which keys counted as authorized. Fixed in commit `0c6d9de`, which introduced `anchored_roster` — the roster is now materialized from a trusted anchor object into a path outside the candidate tree. |
| IDN1 | the `identity-not-name` proposal | specified verifying a release tag against a roster committed **inside that tag**. Reproduced by the reviewer: an attacker key, an attacker-authored roster committed beside the payload, a tag signed with that key — `git verify-tag` returns 0 with a Good signature. Internal consistency with attacker-supplied trust material. |
| IDN4 | the same proposal, part 3 | specified comparing an installed tree against "the upstream present on disk", where the **target's own lockfile** supplies the path to that upstream. |
| I1 | the `release-authenticity` proposal | tag substitution. An attacker with forge write access and **no signing key** repoints `refs/tags/v0.5.0` at the genuine `v0.3.0` signed tag object; the documented four-command bootstrap returns exit 0 with "Good git signature", while `git cat-file tag` on the same object prints `tag v0.3.0`. Reproduced in four commands. |

Four instances of one shape, on four different surfaces, all recorded in a
single working day. The compression is itself the finding: the shape was found
four times *because someone finally started looking for it*, having found it
once. Before that it sat in three shipped or specified surfaces at the same
time. A property nobody has written down is a property nobody looks for.

**A fifth instance, measured for this proposal.** I applied the shape as a
*specification* to a surface nobody had reviewed for it, which is precisely the
forward-looking move this proposal is arguing for. Method and full output are in
*Evidence* below; the result:

`bootstrap/verify_integrity.py` reads its expected SHA-256 values from
`dev/.cairn/cairn-lock.yml`, which lives **inside the tree it is verifying**. An
attacker who can write a file in the target can write the lockfile record for
that file. Against a scratch `solo-greenfield` install I appended a line to
`tools/lifecycle.py`, rewrote that one record's `hash`, and re-ran the verifier:

```
verify_integrity: OK -- 55 recorded file(s) match dev/.cairn/cairn-lock.yml
exit=0
```

The backdoor line is present in the file. This is not carelessness by the
verifier's author, who reasoned about it explicitly — the code comment at
`bootstrap/verify_integrity.py:64` opens *"The lockfile is itself a tamper
target"* and hardens the dst-containment and `living_state` paths against
exactly this. The hash field is the one input that cannot be hardened from
inside. What is wrong is not the code's care; it is that **two documents claim
more than the mechanism can deliver**, and there is no property written anywhere
that would have made someone check.

**Other measured evidence, each grounding one bar item.**

* **A regression test named "the anti-drift assertion" cannot fail.**
  `test_scan_targets_cover_all_shipped_scripts` derives its expected set from the
  same Python object the code under test walks — verified by execution, the
  identity check returns `True`. The assertion is `X - (X ∪ …) == ∅`, empty for
  every possible content of that registry. It was live and green for 63 days
  (2026-06-01 to 2026-08-03) across the exact drift its docstring names, while
  2502 lines of shipped Python sat outside the scanned set. Recorded in the
  `scan-coverage` addendum.
* **~12 ledgered instances of a document claiming a mechanical gate that nothing
  fires**, in the `gate-claims-vs-enforcement` ledger — including eight that name
  a CI system this repository does not have, and one shipped verifier that
  returns success without checking the control its document promises.
* **`scripts/check_cairn.py` reports on 173 of 218 tracked Markdown files** while
  a real broken link sits in an unscanned file (counts `as_of 2026-08-03`; the
  scan-coverage lineage owns the remedy).
* **The prose-injection scanner reaches zero default installs.** The
  `content-security` module is selected by **0 of 3** shipped presets (measured
  below), while `templates/onboarding/high-rigor-legacy.md` twice tells that
  preset's adopters that "the high-rigor-legacy profile's content-security +
  security-review gates apply".
* **A homoglyph in a byline flips an AI author into the recognized-human
  bucket.** The normalization at `tools/lifecycle_planner.py:237` is
  `re.sub(r"[^a-z0-9]", "", first.lower())`, which in Python 3 deletes every
  non-ASCII letter — so dropping a character *widens* authority. Recorded with a
  full reproduction in `byline-classification`.

## Proposed paths

*(The plan this proposal opens on acceptance. It does not exist yet.)*

Proposed paths:
- `dev/plans/release-security-bar.md` — the burndown register and the audit's home; lands in the plan-open commit that follows an accepting Decision.

## Proposal

### What is being added

**One document defining six properties, and one plan that burns them down.**
No new script, no new gate, no new doctrine, no change to any shipped file in
this proposal. The deciders are commands that already exist.

* **This proposal** states the bar: six properties, each with the command or
  inspection that decides it, the real instance that justifies it, and where the
  tree stands today.
* **On acceptance** it opens the plan `release-security-bar`, which carries the
  **register** — one table per bar item, one row per surface — and burns it down.
* **The end-of-line audit** is that plan's own `## Plan review` stage, tiered
  External. It is not a new mechanism; it is a lifecycle stage the tooling
  already enforces.
* **The tag is blocked** by the plan not being archived. `dev/PLANNING.md`'s
  public-launch sequence gains one precondition clause naming the plan stem.

### The one design rule that makes a bar finite

A bar nobody can clear is the receding horizon with extra steps. The rule that
prevents that:

> **Every item admits a fix *or* a registered residual — never silence.**
>
> A row is MET when either (a) the property holds, or (b) the shipped
> documentation states plainly what the step does *not* establish, and the gap is
> registered with an owner and an expiry trigger. What the bar forbids is a
> document claiming a property the mechanism does not have.

This is not a loophole; it is the whole point, and it is what would have caught
**every one of the five instances above**. In each case the mechanism's limit was
real and arguably acceptable — what made each a defect was a *sentence claiming
otherwise*. CR1's plan already recorded that the snapshot could not see the
candidate's git config. `bootstrap/verify_integrity.py` already reasons in
comments about lockfile tampering. The gap was never the knowledge; it was that
the knowledge never reached the sentence an adopter reads.

It also makes the bar **achievable inside v0.4.0**, because closing a row never
requires building a mechanism you have not budgeted for. It requires either
building it or saying you did not.

### The scope fence

The bar quantifies over **what a v0.4.0 adopter is exposed to**, and nothing
else. Concretely, three sets:

1. **The verification steps Cairn documents for an adopter to run** — the
   trust-establishing path.
2. **The code the scaffold installs into an adopter tree** — measured, not
   assumed: `install_manifest` for each shipped preset.
3. **The security claims Cairn's adopter-facing prose makes** — the sentences in
   `SECURITY.md`, `bootstrap/SAFETY.md`, `bootstrap/PROVENANCE.md`,
   `doctrine/runtime-contract.md`, and the installed module and onboarding
   documents that assert a control is applied.

**Explicitly outside the fence for v0.4.0**: Cairn's own development tooling
(the quality gates, the AST attestation, the intent hooks), the deliberation
record, the case studies, and the examples. They are not what a postdoc's
security posture rests on. Deferrals are listed under *What is v0.5, said out
loud*.

Each set is **enumerable**, and the enumeration is committed in the plan. That is
the second thing making the bar finite: the bar does not quantify over "the
repository", it quantifies over a list you can count.

### B1 — Trust material arrives from outside the artifact under verification

**Property.** For every verification step in set 1, each input the step's
*conclusion depends on* either (a) arrives through a channel independent of the
artifact under verification, or (b) is named in the step's own shipped
documentation as artifact-supplied, together with the sentence saying what the
step therefore does not establish.

**Decider.** For each step, the register records its inputs and each input's
arrival channel. For every input claimed independent, a falsifying run: construct
the artifact so that it supplies that input with attacker-chosen content, and
record the exit code and output. A row is MET when the falsifying run refuses, or
when the shipped documentation already says the step does not establish what the
run shows it does not establish.

**Origin.** CR1, IDN1, IDN4, I1, and the fifth instance measured above.

**Where the tree stands today**, over the five steps I could enumerate:

| Step | Trust material | Arrival channel | Row |
| --- | --- | --- | --- |
| The gate pre-flight signature check | allowed-signers roster | trusted anchor object, outside the candidate — `anchored_roster` | **MET** (the exemplar; fixed in `0c6d9de`) |
| The documented tag-verification bootstrap | signer roster | out-of-band, designed in `release-authenticity` Part A | **in flight** — designed, not landed |
| `bootstrap/container/verify-ref.sh` | signer roster | inherits the above | **in flight** — same lineage |
| The fork advisory | comparison bytes | target-supplied today; caller-supplied in `fork-advisory-semantics` | **in flight** — designed, not landed |
| `bootstrap/verify_integrity.py` | expected SHA-256 values | the target's own `dev/.cairn/cairn-lock.yml` | **NOT MET, unowned** |

The last row is the one this proposal contributes. It has no owner and it is the
only one of the five with no lineage in flight. Two things about it:

* **The remedy is cheap and the trusted bytes are already on hand.** The verifier
  runs *from a trusted Cairn checkout* — `SECURITY.md:48` says so in bold. For a
  record marked `verbatim: true`, the upstream template is sitting in that
  checkout and can be hashed directly, with no schema change and no new trust
  channel. Measured on a scratch `solo-greenfield` install: **59 records, 29
  verbatim, 27 of them `.py` — and 27 is every Python file that preset installs.**
  The entire executable surface of a default install is anchorable to the
  verifier's own checkout.
* **The other 30 records are token-substituted** and cannot be hashed against
  upstream, because the tokens differ per adopter. Anchoring those needs re-render
  and compare, which is a different mechanism. That half is a v0.5 item.

**What closes B1 for v0.4.0.** The register exists and is committed; the three
in-flight rows land or state their residual; and the `verify_integrity` row is
either fixed for the verbatim subset by a named successor proposal, or its two
overstating sentences are corrected (see the hand-off table). Both branches are
inside a v0.4.0 budget. **Recommendation: fix the verbatim subset**, because
"every executable file in a default install" is a large fraction of the value for
a small, well-bounded change — but that is a Maintainer call.

### B2 — The answer names the thing that was asked about

**Property.** Any shipped check that reports a verdict about a *named* identity,
version, ref, or file set binds its verdict to that name, and its output names
what it actually verified.

B2 is B1's mirror. B1 is about where a check's inputs come from; B2 is about
whether the check's *conclusion* is about the thing the caller asked about. They
are genuinely different: in the tag-substitution case the roster arrived
correctly out-of-band and the signature was genuinely the maintainer's — the
defect was that the answer concerned a different object than the question. Keeping
them apart is what stops a fix to one from being mistaken for a fix to the other,
which is what happened in `release-authenticity`, where the resolver written to
close [IDN2] limb 2 reproduced limb 2 inside itself.

**Decider.** For each such check, run it with the caller's name repointed at a
different genuine object. The check must refuse, or must name the substitution in
its output. This is a four-command run per check, already demonstrated once.

**Origin.** [I1], reproduced; [IDN2] limb 2 — *"the output must answer the
question that was asked"*.

**Where the tree stands today.**

| Check | Verdict is about | Bound to the name? | Row |
| --- | --- | --- | --- |
| The documented tag bootstrap | a release version | **no** — exit 0 for a substituted ref | **in flight** — the `check_name` fix is specified in [I1] and accepted in the Response |
| `bootstrap/container/verify-ref.sh` | a release version | **no** — inherits the resolver | **in flight** — same lineage |
| `bootstrap/verify_integrity.py` | "the recorded install" | yes, and it says so | **MET** — the wording at `SECURITY.md:48` is careful and true as far as B2 goes |
| `tools/lifecycle_planner.py` byline classifier | document structure, not identity | yes, after [IDN3] settled the framing | **MET** |

**What closes B2.** The `release-authenticity` lineage lands its name-binding
fix in both call sites, and the register records the substitution run for each
of the four checks. No unowned work.

### B3 — A documented security control names the command that fires it, and that command runs

**Property.** Every sentence in set 3 that asserts a control *is applied* names
the command and the occasion. Where nothing fires it automatically, the sentence
says "run this" rather than implying a standing gate.

**Decider.** For each such sentence: locate the named trigger and execute it. Plus
the two standing inspections already run by `gate-claims-vs-enforcement` — `find
.github -type f` and a `git ls-files` sweep for pipeline filenames — which
together establish that no scheduled trigger exists in this repository at all.

**Origin.** The twelve-row ledger in `gate-claims-vs-enforcement` (eight rows
naming a CI this repository does not have; one shipped verifier returning success
without checking its promised control) plus the two later-audit rows. The
`bootstrap/SAFETY.md:120` sentence — every change to agent-loaded content *"must
pass the content-integrity scanner"* — is the sharpest instance inside the fence.

**Scope.** B3 quantifies **only over the security subset** of that ledger. The
full ledger is `gate-claims-vs-enforcement`'s and this proposal edits none of it.
Where a row falls inside both, that proposal's disposition governs and the bar
records the row as *delegated*.

**Where the tree stands today.** Two rows the bar contributes beyond the existing
ledger, both from the fifth-instance measurement:

| Location | What it says | Status |
| --- | --- | --- |
| `doctrine/runtime-contract.md:132` | the integrity check *"Detects tampered apparatus before it can self-audit"* | **falsified** by the coordinated-tamper run — hand off, this file is claimed |
| `SECURITY.md:51` | *"flagging any post-install modification"* | **falsified** in the same run: the file was modified post-install and was not flagged — hand off, this file is claimed |

Note the asymmetry worth preserving: the sentence beginning at `SECURITY.md:47` is *carefully* worded —
"confirm the installed tree still matches its recorded install" is exactly true.
The overstatement is three lines later. A bar item that flagged the whole document
would be noise; one that quotes the sentence is actionable.

**What closes B3.** The security subset of the ledger is dispositioned (mostly by
the owning lineage), and the register records, per sentence, the command that
fires it or the corrected wording.

### B4 — Every test the bar names as an enforcer fails against the drift it is named for

**Property.** For each test the register cites as what keeps a row closed, the
plan records (i) a perturbation that is an instance of *the failure class the
test's own name or docstring claims to guard*, (ii) the command applying it, and
(iii) the observed failure output.

**Origin.** `test_scan_targets_cover_all_shipped_scripts`. Its oracle is computed
from the same Python object its subject walks; the identity check returns `True`;
the coverage assertion is empty for every possible registry content. Green for 63
days across the exact drift it names.

**The refinement that makes this item work, and why it is not optional.** A
weaker form — *"name any perturbation that turns the test red"* — **passes on
this very test**, because three of its other assertions genuinely can fail: the
named-dev-file loop, the every-target-ends-in-`.py` assertion, and the
non-emptiness guard. An author asked for "a perturbation" would name one of
those in good faith and the vacuous assertion would survive. Requiring the
perturbation to be *in the class the test names* is what discriminates. That
distinction is the whole content of B4.

**Why candidate item 6 (derived-list integrity) is merged here rather than
listed separately.** With the class refinement, B4 mechanically catches a
shared-source oracle: perturb the named class, observe green, row fails. The
"derive the oracle from something the subject does not read" prescription is the
**remedy**, not the property — and a bar states properties, because a bar that
states remedies constrains implementations it has not seen. The register records
the recommended remedy alongside each row without making it the pass condition.

**What candidate 6 covered that B4 does not**: a *non-test* derived list — a
document mirroring a code list, kept in step by hand. Real (it is the level-0/1/2
staleness pattern recorded in `scan-coverage`), out of the fence for v0.4.0, and
registered as a v0.5 item rather than dropped.

**Where the tree stands today.** The denominator is not yet known, because it is
defined by the register: B4 quantifies over *the tests the other five items cite
as enforcers*, which is what keeps it finite. Expect 15–25 rows. One row is known
to fail today — the anti-drift assertion — and its remedy is already specified in
the `scan-coverage` addendum, which is in flight.

**What closes B4.** Every enforcer test cited in the register has a recorded
in-class perturbation run, with output. This is one scratch edit plus one pytest
invocation per row; it is hours of work, not a project.

### B5 — No normalization or parse step on an authorization path may widen authority or guess

**Property.** Wherever a shipped tool normalizes or parses an input before an
**authorization, classification, or install-contract** decision, an input the
step cannot fully interpret must move toward *less* authority or toward refusal —
never toward more, and never toward a guess.

This merges two candidate framings that the evidence shows are one thing.
Dropping a character that widens authority (the homoglyph fold) and guessing at
an unparseable line instead of refusing (the profile parser) are the same defect:
**the step resolves its own uncertainty in the permissive direction.** Merging
them means one property covers both evidence streams and one inspection covers
both site classes.

**Decider.** For each enumerated site, feed an input that differs from a
*rejected* input only by what the step drops or cannot interpret, and record which
bucket it lands in.

**Origin.** The homoglyph byline fold at `tools/lifecycle_planner.py:237`; the
fail-open `_minimal_yaml_parse`; the `lifecycle:` line a filename can forge
through the orientation stream.

**Where the tree stands today.** Five enumerated sites:

| Site | Direction on ambiguity | Row |
| --- | --- | --- |
| `tools/lifecycle_planner.py:237` — first-word identity token | **widens** — a dropped non-ASCII letter promotes AI to human | **in flight** — `byline-classification` |
| `tools/lifecycle_planner.py:251` — per-word AI candidates | same one-liner, same direction | **in flight** — same lineage |
| `tools/lifecycle_planner.py:293` — roster-entry normalization | same one-liner, whole-entry | **in flight** — same lineage |
| The profile loader's fallback YAML parse | **guesses** instead of refusing | **in flight** — `profile-parse-fail-open` |
| `_resolve_interpreter`, the local interpreter binding | shape validator, not an authenticator | **MET by residual** — `AGENTS.md` already states plainly that it checks shape, not Python identity or provenance |

The last row is worth naming because it is what a MET-by-residual row looks like
when done well, and it is already in the tree. Nothing about it is fixed; what
makes it MET is that the limitation is written where a reader meets the tool.

**What closes B5.** The four in-flight sites land or state their residual, and the
register records the widening-input run for each of the five.

### B6 — Every shipped security control's default-install reach is stated, and the statement is true

**Property.** For each security control Cairn ships, a committed table states
whether it reaches an install from each named preset, and no Cairn document
claims reach a control does not have.

**Decider.** Eight lines against the real engine — `load_config` + `expand_preset`
+ `install_manifest` per preset. Run for this proposal; output below.

**Origin.** `content_scan.py` — the prose-injection scanner, the one control aimed
squarely at the supply-chain risk `bootstrap/SAFETY.md` calls "an LLM blast
radius" — reaches **0 of 3** presets, while `templates/onboarding/high-rigor-legacy.md`
tells that preset's adopters, in two separate passages, that the gate applies to
their drafted filing before it leaves the deployment.

**Where the tree stands today**, measured at HEAD `54478e2` under the canonical
interpreter (`~/conda_envs/lhm/bin/python`, Python 3.13.13). Rows are **adopter-tree
destination paths** — where the control lands in an installed target:

| Control (installed path) | solo-greenfield | collaborative-team | high-rigor-legacy |
| --- | --- | --- | --- |
| `scripts/content_scan.py` | — | — | — |
| `scripts/run_security_audit.py` | — | — | — |
| `dev/modules/content-security.md` | — | — | — |
| `dev/modules/security-review.md` | — | — | yes |
| `scripts/link_check.py` | — | yes | yes |
| `tools/intent.py` | — | yes | yes |
| `scripts/claim_check.py` | yes | yes | yes |
| `scripts/foldback_export_scan.py` | yes | yes | yes |
| `tools/lifecycle_planner.py` | yes | yes | yes |

The first three rows do not resolve in Cairn's own tree, which is the finding
rather than a citation error: no preset installs them, so no self-hosted copy
exists. Their sources are `templates/modules/team-gated/content_scan.py`,
`templates/modules/team-gated/run_security_audit.py`,
and `templates/modules/team-gated/content-security.md`.

**The scope line that keeps B6 finite, and honest.** B6 requires the reach be
**stated and true**. It does **not** decide what the defaults should be. The
Maintainer's 2026-08-03 direction — *"we need to change the default security
stance for all installations"* — is chat input during drafting, not a Decision,
and changing preset composition is a change to the install contract, which is its
own proposal with its own review. What B6 delivers is the **precondition** for
that decision: a measured table, so the stance change is chosen against evidence
instead of against an impression. Folding the stance change in here would bundle
two contracts in one proposal and would be the exact move the house rules forbid.

**What closes B6.** The table is committed in the register, and every document
claiming reach is checked against it. Two passages in
`templates/onboarding/high-rigor-legacy.md` are known false today; that file is
unclaimed by any in-flight proposal, so it is inside this bar's budget.

### The starting burndown — where the tree stands today, honestly

Six items. Rows counted are the surfaces enumerated above; B4's denominator is
defined by the register and is therefore listed as pending.

| Item | Rows | MET today | In flight | Unowned |
| --- | --- | --- | --- | --- |
| B1 trust-material provenance | 5 | 1 | 3 | **1** |
| B2 answer-binding | 4 | 2 | 2 | 0 |
| B3 claim honesty (security subset) | ~14 | 0 | ~12 delegated | **2** |
| B4 non-vacuous enforcers | pending register | 0 | 1 known-failing | pending |
| B5 fail-closed direction | 5 | 1 | 4 | 0 |
| B6 stated reach | 9 controls × 3 presets | table now measured | 0 | **2 false passages** |

Read honestly: **most of the bar is already being worked.** Nine of the
twenty-odd enumerable rows sit in seven proposals already in flight. The bar's
contribution is not new work; it is (i) five unowned rows nobody was going to
find, (ii) a stopping condition for the rows already moving, and (iii) B4, which
is genuinely new labour but is hours per row, not weeks.

That is what makes it achievable inside v0.4.0. If the honest count had come out
the other way — most rows unowned, most needing new mechanism — the correct
recommendation would have been to cut the bar to three items, and I would have
said so.

### The end-of-line audit

The Maintainer asked for an end-of-line audit. An audit you can describe today is
one that happens; one you cannot is how the Class C follow-on died. So this
section names all five things a describable audit needs.

**What it is.** The `## Plan review` stage of the `release-security-bar` plan,
tiered **External** (a different agent type, or a human). It is not a new
mechanism. It is a lifecycle stage `tools/lifecycle_planner.py` already
understands and already checks.

**What triggers it.** v0.4.0 release preparation. Concretely: the plan enters
`review` when every register row is MET or a registered residual, and the review
must complete before the tag step in the public-launch sequence recorded in
`dev/PLANNING.md`.

**What it checks.** The six items, against the register, using the deciders.
**Nothing else.** The auditor's job is to *falsify rows* — take a row marked MET
and run its decider to see whether it holds — not to open new classes. A new
class found during the audit goes to the v0.5 list unless the Maintainer
classifies it high-risk. That constraint is what makes the audit terminate, and
it is the single most important sentence in this proposal: **an audit with an
open scope is the receding horizon wearing a hat.**

**What it blocks.** The `git tag v0.4.0` step. Since Zenodo deposition and the
DOI follow the tag in the recorded sequence, blocking the tag transitively blocks
the DOI. The block is held **structurally**, not by anyone remembering:
`dev/PLANNING.md`'s launch sequence names the plan stem as a precondition on that
step, and the plan cannot reach `archived` without a `## Code review` section, a
`Follow-ups migrated to:` block, and a fidelity sign-off — all three checked at
`tools/lifecycle_planner.py:654`.

**Why this survives where Class C did not.** The `release-authenticity` addendum
measured the death mechanism precisely: the follow-on was routed to a roadmap
row, and the archive precondition **has no proposal-side arm at all** — `archived`
is a plan status, not a proposal status, so on the proposal side the gate is not
lax, it is structurally absent. Homing this audit in a **plan** puts it on the
side of the asymmetry where the check actually fires. That is not a hope; it is
the one measured difference between the two sides.

**Staleness, checkable with two existing commands.** An audit that ran before the
last change to what it covers is not an audit. Compare the newest audit section's
date against the newest commit touching the registered surfaces:

```
git log -1 --format=%cI -- <the register's surface list>
```

against the dated `## Plan review` section heading in the plan. If the commit is
newer, the audit is stale and the tag waits. No new tooling.

### What is v0.5, said out loud

Naming these here rather than silently including them is what keeps v0.4.0's
target fixed. Each is real; none is achievable inside this release without
displacing work the postdoc needs more.

* **Anchoring the token-substituted half of the lockfile.** 30 of 59 records in a
  default install are token-rendered and cannot be hashed against upstream.
  Needs a re-render-and-compare mechanism. v0.5.
* **Derived-list integrity for non-test lists** — the residue candidate item 6
  covered and B4 does not: a document mirroring a code list. v0.5.
* **Extending the bar to Cairn's own development tooling** — the quality gates,
  the AST attestation, the intent hooks, and the `check_cairn` coverage gap
  (173 of 218 files). Outside the adopter-exposure fence. v0.5.
* **Mutation testing as a standing mechanism**, as opposed to B4's one recorded
  perturbation per enforcer. This would be a new tool and needs its own
  go-ahead under the standing direction. v0.5 at the earliest.
* **Cryptographic attestation** (Sigstore-style). Already declared a future
  enhancement in `bootstrap/PROVENANCE.md`; nothing here changes that.

### Hand-offs — every file this proposal measures but does not touch

Following the house pattern (`gate-claims-vs-enforcement` row E1: find it,
evidence it, hand it off, edit nothing).

| Finding | File | Handed to |
| --- | --- | --- |
| Coordinated lockfile tamper passes | `bootstrap/verify_integrity.py` | a **named successor proposal** — the file is claimed by `fork-advisory-semantics`, so the anchor cannot be designed here |
| *"Detects tampered apparatus"* is falsified | `doctrine/runtime-contract.md` | `gate-claims-vs-enforcement`, which already claims this file |
| *"flagging any post-install modification"* is falsified | `SECURITY.md` | `agent-context-scrub` and `contributor-entry` both claim this file; whichever is decided first takes the row |
| The content-scanner gate claim | `bootstrap/SAFETY.md` | `gate-claims-vs-enforcement` row B1, already dispositioned |
| Two false reach passages | `templates/onboarding/high-rigor-legacy.md` | **unclaimed** — inside this bar's plan budget |

`dev/PLANNING.md` is claimed by `transition-lint` and `release-authenticity`. It
is a shared communication file governed by the serialization rule rather than the
one-proposal-per-file constraint; this proposal's edit is a one-line plan-open row
plus one precondition clause, and whichever lands second rebases onto the landed
text.

### Documentation / doctrine surface

**This proposal touches no documentation and no doctrine.** The bar is a
repository-scoped commitment about this project's own release, not methodology
shipped to adopters. Under the doc tier home rule it is **deliberation layer**:
it decides what this project will do before it ships, which is what `dev/` is
for. It is not governing-layer (it is not a rule for making a correct change to
Cairn), and it is not descriptive-layer (it describes no software).

The plan is the durable home. When it archives, the register archives with it as
the record of what v0.4.0 was held to — which is exactly the artifact a v0.5 bar
would start from.

**One thing this deliberately does not do**, and a reviewer should push on it if
they disagree: it does **not** promote the bar into `doctrine/` as methodology
Cairn ships. Six properties derived from one repository's five incidents are not
yet a general method, and shipping them as doctrine would assert a generality the
evidence does not support. If the bar clears its own audit, *that* is the evidence
for a later doctrine proposal — which would clear the rate-limit gate on
recurrence (five instances of one shape is comfortably ≥2 in a rolling window).

### Doctrine-change rate-limit

**Not applicable — this proposal changes no doctrine.** No file under
`doctrine/` is touched, no rule in `AGENTS.md` changes, and no shipped template
or contract moves. The gate does not apply.

Stated explicitly because the omission would otherwise be a review finding, and
because the temptation to write the bar as doctrine is real. Resisting it is a
design decision, argued above.

### Why this tier — required(External)

A bar that only its author has read is a private checklist. The whole mechanism
by which this fixes the Maintainer's problem is that a *second, structurally
independent* reader can hold the tree to a fixed target — which requires that the
target survive contact with someone who did not write it. An Internal read (same
agent type, fresh session) would confirm the rows are internally consistent; it
would not test the thing that matters, which is whether the six properties are
the *right* six and whether the fence is drawn where an outsider would draw it.

There is a second reason, and it is the sharper one. The specific failure mode of
a specification written by the same author who wrote the diagnostics is that it
specifies exactly what the author already knows to look for. The four-instance
recurrence happened *inside* a review process that this same author was running.
An External read is the only structural defence against a bar that codifies the
author's blind spots as the definition of done.

## Rationale

* **Which user workflow does it improve?** The Maintainer's, directly and
  measurably. Today, "are we done?" is answered by running diagnostics and seeing
  whether anyone reports anything, which cannot terminate. After this, it is
  answered by reading a table. The manual back-and-forth the Maintainer wants to
  reduce is caused by the absence of that table, not by the volume of review.
* **What contract does it clarify?** The release contract — what v0.4.0 asserts
  about itself. Today Cairn asserts security properties in five documents with no
  statement of which are load-bearing at release. After this, the load-bearing set
  is six properties with per-row evidence.
* **What transparency or correctness does it improve?** It converts five
  documents' worth of implied claims into either true claims or stated residuals.
  For a repository about to mint a DOI — a permanent, citable identifier for a
  specific artifact — "which release did I verify, and what did that verification
  establish" is the whole question.
* **Why now?** Three reasons converge. The failure shape has recurred five times
  and is now well enough characterized to specify against. Seven proposals are in
  flight against surfaces the bar covers, and they need a stopping condition
  before they are decided, not after. And the tag is the last moment at which the
  cost of a wrong claim is still low — after the DOI, a corrected claim is a
  corrected *published* claim.

**Maintainer preference during drafting** (chat input, shaping the draft, not a
Decision): the two quotes in *Context* are the Maintainer's own framing of the
problem; the request for an end-of-line audit is theirs; and the 2026-08-03
direction *"we need to change the default security stance for all installations"*
is what makes B6's measurement urgent rather than merely tidy. The standing
directions recorded at `dev/PLANNING.md` — postdoc-first, and fix defects build
nothing new — are cited throughout as constraints, not as authorization.

## Alternatives considered

* **Do nothing — keep reviewing until reviewers stop finding things.** Rejected on
  measured evidence. Reviewers did not stop: the same shape was found four times
  in one day on four surfaces, and a fifth instance fell out of the first hour of
  looking for it deliberately. There is no reason to believe a sixth pass
  terminates. Do-nothing is not neutral — it ships v0.4.0 with the claims in
  `doctrine/runtime-contract.md:132` falsified, with the companion sentence at
  `SECURITY.md:51` falsified alongside it, and a DOI minted over them.
* **A checklist imported from an established security framework.** Rejected. Every
  item would be defensible and none would be grounded in this repository's actual
  failure modes; the four-instance shape that dominates this tree's evidence is
  not on any standard list I could apply honestly. Worse, an imported list is long
  and mostly inapplicable, which produces the *opposite* of a stopping rule — a
  large backlog of items no one can dismiss on evidence.
* **Twelve items instead of six.** Considered seriously. The candidate set I was
  given had seven; I merged one into another and split one framing into a merged
  item, netting six. Twelve would cover more, and would not be clearable by
  v0.4.0, and an unclearable bar is the receding horizon with extra ceremony. Six
  is chosen because the honest burndown above says six is reachable.
* **Fewer items — three, covering only the trust-material shape.** Rejected, but
  it is the closest call. Three would be certainly achievable. It would leave B4
  out, and B4 is the item that keeps the other five from rotting: without it, a
  closed row is held by a test that may be as vacuous as the anti-drift assertion
  was for 63 days. B6 similarly cannot be dropped, because it is the precondition
  for the Maintainer's own standing direction. B5 has four in-flight sites and
  costs the bar almost nothing to include.
* **Write the bar as shipped doctrine now.** Rejected; argued under
  *Documentation surface*. Five incidents in one repository are evidence for a
  repository-scoped commitment, not yet for a method Cairn asserts to adopters.
* **Build a checker script that evaluates the bar automatically.** Rejected on the
  standing direction, and independently on merit. Four of the six items are
  decided by a *judgement over an enumeration* (is this arrival channel
  independent? is this perturbation in the named class?), and a script that
  scored them would be a diagnostic — which is the thing that failed. The bar's
  power comes from being read, not from being run.
* **Fold the default-stance change into B6.** Rejected. It bundles two contracts,
  and the install-contract change deserves its own review with its own reach
  evidence — evidence that B6 produces. Sequencing beats bundling here.

## Evidence / verification plan

### What proves this works

The bar is a specification, so "works" means: **applying it finds things that
diagnostics did not, and the finding stops.** The first half is already
demonstrated — writing item B1 as a property and asking it of every step in the
fence produced a live, unowned defect in `bootstrap/verify_integrity.py` within
the first hour, on a surface that had been reviewed repeatedly under the
diagnostic mode. The second half is what the audit tests.

### The fifth-instance measurement, reproducible

All commands run at HEAD `54478e2` under the canonical interpreter
(`~/conda_envs/lhm/bin/python`, Python 3.13.13). **No file in the repository was
modified**; the install was scaffolded into a scratch directory outside the tree.

1. Scaffold a default install and take the baseline:

```
$ python bootstrap/scaffold.py --config <scratch>/p.yml --target <scratch>/target \
      --non-interactive --allow-dev
$ python bootstrap/verify_integrity.py --target <scratch>/target
verify_integrity: OK -- 55 recorded file(s) match dev/.cairn/cairn-lock.yml
  (4 adopter-authored living-state file(s) tracked for upgrade but excluded
   from the tamper check).
```

2. Coordinated tamper — append a line to a shipped executable, then rewrite that
   one record's `hash` in the target's own lockfile:

```
records rewritten: 1 -> new hash sha256:5b13af30c744eb9
```

3. Re-run the verifier:

```
$ python bootstrap/verify_integrity.py --target <scratch>/target
verify_integrity: OK -- 55 recorded file(s) match dev/.cairn/cairn-lock.yml ...
exit=0
$ grep -c BACKDOOR <scratch>/target/tools/lifecycle.py
1
```

4. The anchorable fraction, from the same install's lockfile:

```
total records: 59
verbatim records: 29
verbatim .py records: 27
non-verbatim (token-substituted): 30
```

Cross-checked against the install manifest: `solo-greenfield` installs exactly 27
`.py` files, so **every executable file in a default install is `verbatim` and
therefore anchorable** to the verifier's own trusted checkout.

### The B6 reach measurement, reproducible

Eight lines against the real engine — `load_config`, `expand_preset`,
`install_manifest`, per shipped preset. Output is the B6 table above. Independent
cross-check on the module side:

```
collaborative-team  content-security in modules: False
high-rigor-legacy   content-security in modules: False
solo-greenfield     content-security in modules: False
```

### Suite state at the time of writing

`python -m pytest bootstrap/tests` — **1598 passed**, `as_of 2026-08-03`, under
the canonical interpreter (Python 3.13.13). This proposal changes no code, so the
figure is a baseline for the plan, not a verification of this proposal.

### Author-accounting — invariants, failure modes, edge cases

This is a high-stakes change: it defines the condition under which a public
release ships.

* **Invariants.**
  * *The bar's item count is fixed at Decision.* Enforced socially by the audit's
    scope constraint (falsify rows, do not open classes) and structurally by the
    plan's append-only rule — a new item is a new proposal, visibly.
  * *Every row resolves to MET or a registered residual; never silence.* Enforced
    by the audit, whose pass condition is per-row and enumerated.
  * *The plan cannot archive incomplete.* Enforced mechanically at
    `tools/lifecycle_planner.py:654` — code review, follow-ups block, and fidelity
    sign-off are all required for `archived`.
  * *The tag waits on the plan.* Enforced by the precondition clause in
    `dev/PLANNING.md` and, weakly, by the Maintainer reading it. **This is the
    weakest enforcement in the proposal and I am naming it rather than dressing it
    up**: nothing in this repository mechanically prevents a `git tag`. The
    honest claim is that the precondition is written where the sequence is read.
* **Failure modes.**
  * *Open (degrades):* a row is marked MET on a decider that was run sloppily. The
    audit is the compensating control; it is not a proof.
  * *Open (degrades):* the register's enumeration is incomplete — a verification
    step exists that nobody listed. This is the bar's central residual and it is
    stated under *What this does not establish*.
  * *Closed (refuses):* the plan cannot archive without its three preconditions.
  * *Open, intentional:* a registered residual ships. That is the design.
* **Edge cases.** *Zero rows for an item* — possible for B4 if the register cites
  no tests, which would itself be a finding and the audit must say so rather than
  pass the item vacuously. *A row owned by an in-flight proposal that is rejected*
  — the row reverts to unowned and the bar blocks; this is the correct behaviour
  and the register records the dependency. *A row that is MET at register time and
  broken by a later commit* — caught by the staleness check, not by re-running
  everything.
* **Public-path → test mapping.** **N/A for this proposal**: it adds no code and
  no public entry point. The plan carries the mapping for whatever code its rows
  produce, and B4 is the discipline that mapping is held to.
* **Known omissions / intentionally untested edges.** The `verify_integrity`
  finding is measured on **one** record type (`verbatim: true`, a `.py` file) in
  **one** preset (`solo-greenfield`). I did not test a token-substituted record,
  a `living_state` record, or the other two presets. The mechanism is
  record-type-independent by inspection — the hash comes from the lockfile in
  every branch — but I have not run it, and the register should.

### What this proposal does not establish

Said plainly, because overstating a security artifact is the exact defect it
exists to prevent.

* **It does not establish that Cairn is secure.** Six properties are six
  properties. A defect outside all six ships, and clearing the bar is not evidence
  of its absence.
* **It is not a threat model.** It enumerates no adversaries, assets, or trust
  boundaries. It generalizes five observed failures; it does not derive them from
  a model of who is attacking what. A threat model is a reasonable v0.5 item and I
  am not proposing one.
* **It does not establish that the enumeration is complete.** Every item
  quantifies over a list I built by hand. A verification step, a normalization
  site, or a shipped control that nobody listed is invisible to the bar. This is
  the single largest residual and no part of the design closes it.
* **It does not establish that any row marked MET is actually met.** It establishes
  that a named command was run and its output recorded. B4 is the partial
  compensation and it is partial.
* **It establishes nothing about an adopter's own repository, agents, or
  practices.** The fence is what Cairn ships.
* **It does not make the tag mechanically un-taggable.** See the invariant note
  above.

### Tests required

**N/A for this proposal** — it adds no code. Tests belong to the plan's rows, and
B4 is the standard each must meet: an in-class perturbation, run, with output
recorded. Noted explicitly rather than omitted, per the template.

### Examples / smoke checks

* `python scripts/check_cairn.py` over this file — the prose-integrity smoke for a
  Markdown-only change.
* `python scripts/claim_check.py <this file>` — the path and line-citation check.
  This proposal cites ten distinct repository paths with line numbers; all were verified
  at HEAD `54478e2` at drafting time.
* The two measurement commands in *Evidence* are themselves the smoke checks for
  the two tables this proposal contributes, and both are re-runnable by a
  reviewer without modifying the repository.

## Signals the change is wrong

* **The audit's first pass opens more than two new classes.** That would mean the
  six items are not the right six and the fence is drawn wrong. *Recovery:* stop,
  do not widen the bar mid-flight; take the new classes to a revising proposal and
  let the Maintainer decide whether v0.4.0 waits. Widening a bar during its own
  audit reproduces the receding horizon exactly.
* **Rows get marked MET by argument rather than by output.** The failure signature
  is a register row whose evidence column contains prose instead of a command and
  its result. *Recovery:* the audit rejects the row; if this happens more than
  twice, the bar has become a form to fill in and should be cut to three items
  that are actually run.
* **The burndown does not move for two working sessions while proposals continue
  to land.** That means the bar is not the organizing artifact and work is being
  driven by something else. *Recovery:* surface it at goodnight; either the bar is
  wrong or it is being ignored, and both are worth knowing early.
* **B4 turns out to cost days per row rather than hours.** *Recovery:* cut B4's
  scope to the enforcers of B1 and B2 only — the two items where a vacuous test
  would hide a live exploit — and move the rest to v0.5.
* **The Maintainer finds the bar harder to read than the reviews it replaces.**
  This is the real failure mode for a document whose entire value is legibility.
  *Recovery:* collapse the register to one table with six sections and drop the
  per-item prose; the tables are load-bearing, the prose is scaffolding.

## Maintainer decisions

Six things are the Maintainer's to decide. Each carries a recommendation and the
reasoning behind it. The proposal's status stays `proposed` until a Decision lands.

**A note on how this section was written.** An earlier draft of it supplied, for
each decision, a pre-written sentence for the Maintainer to say back — intended
to reduce composing effort. That was wrong and the sentences have been removed.
Cairn's scribing guard-rail requires the Maintainer's authorization to be quoted
**verbatim**, precisely because a paraphrase "admits semantic drift,
condition-softening, or a hallucinated approval." A sentence an agent wrote for
the Maintainer to repeat is not the Maintainer's authorization; it is the agent's
decision with the Maintainer's name attached. Left in the record, those
blockquotes were formatted exactly as a verbatim authorization would be, and a
later scribe — including the agent that wrote them — could have lifted one as
though it had been said. Recorded rather than silently corrected, because the
draft closed by restating that very guard-rail while breaking it.

**D1 — the "build nothing new" go-ahead.** The standing direction says any new
tool or mechanism needs an explicit go-ahead. This adds no tool, but it does add
a document and a release precondition, which is arguably a mechanism.
*Recommendation: grant it.* The receding horizon **is** the defect this proposal
fixes; it introduces zero code and reuses the plan lifecycle for the audit.

**D2 — six items, or a smaller set.** *Recommendation: six as specified*, with
the item set fixed at Decision so a seventh becomes a new proposal rather than an
audit finding. The smaller alternative worth considering is B1, B2 and B4 for
v0.4.0, deferring B3, B5 and B6 to v0.5.

**D3 — what the audit blocks.** *Recommendation: the audit blocks the v0.4.0 tag,
and the repo-public flip moves after the audit in the launch sequence.* A public
repository can be cloned and installed before any tag exists, so the flip — not
the tag — is the real first-exposure moment for a postdoc. The alternative is to
block the tag only and leave the flip where the recorded sequence puts it.

**D4 — the `verify_integrity` lockfile anchor: v0.4.0 blocker, or registered
residual?** *Recommendation: fix the verbatim subset for v0.4.0.* It covers every
executable file in a default install, the trusted bytes are already in the
verifier's own checkout, and it needs no schema change — but it is a Security
Review surface, needs its own proposal, and that file is currently claimed by
another lineage. If the budget is judged too tight, the alternative is to register
it as a v0.5 residual and correct the two overstating sentences for v0.4.0.

**D5 — does the default-stance change ride here?** *Recommendation: no.* B6 stops
at stating each control's reach. Changing preset composition is an install-contract
change and belongs in its own proposal, sequenced after B6's reach table is
committed.

**D6 — the audit's tier.** *Recommendation: External, and not run by the author of
the bar.*

**On scribing.** If the Maintainer instructs an agent to scribe any of the above,
the Decision-commit guard-rail applies in full: the authorizing sentence is quoted
verbatim and visually isolated in both the `## Decision` block and the commit body,
the commit is Decision-only, and the instruction must be unambiguous on both the
disposition and the commit — or the scribe confirms first rather than guessing.

## Review -- Gemini Flash (External, security lens) -- 2026-08-03

**Steelman.** This proposal addresses the fundamental problem of a "receding security horizon" by replacing open-ended diagnostic checks with a specificational v0.4.0 release security bar. Defining six falsifiable properties (B1–B6) with explicit deciders and a finite burndown plan (`release-security-bar.md`) gives the maintainer a clear stopping rule for v0.4.0 release readiness. The core rule—every item admits either a fix or a registered residual—guarantees that security readiness is achievable within the v0.4.0 scope.

### Concerns

* **[E1] Verification of `verify_integrity.py` verbatim anchoring (Decision D4).**
  The 5th instance reproducer demonstrates that `verify_integrity.py` currently reads expected hashes from the candidate target's own `dev/.cairn/cairn-lock.yml`, allowing a coordinated tamper attack (modifying target files + updating lockfile hashes) to pass as clean (`OK`). For v0.4.0, fixing the verbatim subset (27 Python files) by hashing against the caller's trusted `CAIRN_ROOT` checkout should be prioritized in a successor proposal to close this gap.

### Covered

* **5th Instance Coordinated Lockfile Tamper Reproduction**:
  Executed python test script performing a coordinated tamper against a scaffolded `solo-greenfield` target:
  - **Baseline run**: `verify_integrity: OK -- 55 recorded file(s) match dev/.cairn/cairn-lock.yml` (exit code 0).
  - **Coordinated tamper**: modified `tools/lifecycle.py` and updated SHA-256 hash in target `dev/.cairn/cairn-lock.yml`.
  - **Tampered run**: returned exit code 0 (`verify_integrity: OK`), reproducing verbatim that `verify_integrity.py` currently succumbs to target-controlled lockfile tampering.

```
=== BASELINE INTEGRITY ===
Exit code: 0
Stdout: verify_integrity: OK -- 55 recorded file(s) match dev/.cairn/cairn-lock.yml (4 adopter-authored living-state file(s) tracked for upgrade but excluded from the tamper check).

=== TAMPERED INTEGRITY CHECK (5TH INSTANCE MEASUREMENT) ===
Exit code: 0
Stdout: verify_integrity: OK -- 55 recorded file(s) match dev/.cairn/cairn-lock.yml (4 adopter-authored living-state file(s) tracked for upgrade but excluded from the tamper check).
```

### Not covered / low confidence

* Verification of token-substituted lockfile records (30 of 59 records) requires re-render and compare and is explicitly deferred to v0.5.

### Recommendation

**SHIP.** The proposal's six-property specification, deciders, scope fences, and burndown structure are verified and sound.

