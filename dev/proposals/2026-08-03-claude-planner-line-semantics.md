<!-- cairn-internal-ref-allow: doctrine/lifecycle-contract.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see AGENTS.md, "Where doctrine/ references resolve") -->

# The lifecycle checker and the human reader disagree about what a line is

**Author**: Claude (Strategy)
**Model**: Claude Opus 5
**Date opened**: 2026-08-03
**Status**: reviewed
**Touches**: `tools/lifecycle_planner.py` and `tools/lifecycle.py`, plus their
byte-identical `templates/skills/_lib/` twins; new test nodes in
`bootstrap/tests/test_lifecycle_contract.py` and
`bootstrap/tests/test_lifecycle_cli.py`
**Related**: Theme 3 of the strategy note `2026-07-08-claude-broad-look-skeptical-review`
("the security story is ahead of the security practice"). **Two proposal
lineages claim these files.** From Theme 3: the sibling proposal
`agent-context-scrub`, which shares `tools/lifecycle.py` and its
`templates/skills/_lib/` twin. From the `2026-08-03-claude-identity-not-name`
lineage (**superseded** 2026-08-03, Decision `6c6ce39`): its successor scope 2, the exact
byline classifier, which shares `tools/lifecycle_planner.py` and its twin and
carries a security lens after that proposal's 2026-08-03 amendment demonstrated
a working homoglyph exploit. All three changes share one root cause and are
reviewed in one sitting, but stay three proposals — see *Proposal >
Cross-lineage file collisions*
**Plan review**: required(External) — see *Rationale > Why this tier* for why a
same-type reviewer cannot give independence on the one judgment call this
proposal makes


**Vocabulary and when the collision constraint binds** (identical in every
proposal of this set, so the set does not disagree with itself). *Within-set* =
two Theme 3 proposals claim the same file. *Cross-lineage* = a Theme 3 proposal
and a successor scope of `identity-not-name` claim the same file; there are
exactly two, `tools/lifecycle_planner.py` and `bootstrap/PROVENANCE.md`. The
constraint binds at **plan-open and implementation, not at proposal-open** — an
open proposal edits no file, so all of this set may be open, reviewed and decided
concurrently. Nothing mechanical enforces the constraint; it is carried by these
tables and by the work-intent claim taken before editing.

## Context

### The mechanism

Python's `str.splitlines()` splits a string on **ten** characters. Markdown,
git, `grep`, `sed`, `wc`, and Python's own `re.MULTILINE` split on **two** (CR
and LF, plus the CRLF pair). The eight extras are, empirically:

    $ ~/conda_envs/lhm/bin/python -c "
    seps=[c for c in range(0x3000) if len(('a'+chr(c)+'b').splitlines())>1]
    print([hex(c) for c in seps if c not in (0x0A,0x0D)])"
    ['0xb', '0xc', '0x1c', '0x1d', '0x1e', '0x85', '0x2028', '0x2029']

`U+000B` VERTICAL TAB, `U+000C` FORM FEED, `U+001C`–`U+001E` (the file /
group / record separators), `U+0085` NEXT LINE, `U+2028` LINE SEPARATOR,
`U+2029` PARAGRAPH SEPARATOR. The first six are Unicode category `Cc`
(control); the last two are `Zl` and `Zp`. None of them is a line ending in
CommonMark — whose "line ending" is defined as newline, carriage return, or
carriage-return-newline, and nothing else — none of them is a line ending to
git, and none of them ends a line for `grep -n '^## '`.

Five places in Cairn's two shipped lifecycle tools read a **human-authored
markdown artifact** and make a **structural or authority claim** about it
through `str.splitlines()`:

* `tools/lifecycle_planner.py:397` — `_parse_status`, which decides the
  artifact's lifecycle state.
* `tools/lifecycle_planner.py:412` — `_parse_field`, which reads `Author` and
  `Plan review`.
* `tools/lifecycle_planner.py:421` — `_parse_sections`, which decides which
  `## Review` / `## Decision` sections exist.
* `tools/lifecycle_planner.py:464` — `_has_isolated_blockquote`, which decides
  whether a Decision's verbatim authorization is present and visually isolated.
* `tools/lifecycle.py:494` — `_status_of`, which reports each in-flight
  thread's status in the session-start orientation the Maintainer reads every
  morning.

### The consequence, reproduced

Nothing below is argued from the mechanism. A fixture proposal was built in a
throwaway tree with a fabricated Decision section and a fabricated status flip
glued onto the end of two ordinary prose lines with `U+2028`. Every command and
its real output is in *Evidence / verification plan*; the short version:

**What every reader in the project's own toolchain sees.** `wc -l` reports 49
lines. `grep -c '^## '` finds 7 headings. `grep -n '^## Decision'` finds
nothing and exits 1. The `**Status**:` line a `^`-anchored grep finds says
`proposed`. A CommonMark renderer (`markdown-it`, CommonMark preset) emits
seven `<h2>` elements, none of them a Decision, and swallows the whole payload
— heading marker, blockquote marker and all — into a single `<p>` inside the
Response section, with the `>` HTML-escaped to `&gt;` as literal text. `git
diff` reports the entire fabricated Decision as **"2 insertions(+), 2
deletions(-)"** — two modified prose lines.

**What the lifecycle checker says about the same bytes**, at `3292f21`:

    lifecycle-planner: == proposal: 2026-08-03-agent-cache-tuning.md ==
    lifecycle-planner: current state: accepted
    lifecycle-planner: structural conformance: current state is structurally sound.

    lifecycle-planner: == legal next transitions ==
    lifecycle-planner: (terminal state -- no status transition; ...)

It parsed a `## Decision -- Anthony Kendall (Maintainer) -- 2026-08-03`
heading, classified the byline against the live `dev/.cairn/agent-identities.json`
as a human Maintainer, found an isolated authorization blockquote under it, and
emitted a **positive attestation** — `structurally sound` — for a terminal
accepted state that exists in no other reader's frame. `tools/lifecycle.py`'s
`_status_of` returns `'accepted'` for the same file.

`doctrine/lifecycle-contract.md` puts "the current `Status:`" and "the
*structural* presence/absence of each transition's documentary precondition" on
the machine-verifiable side of the boundary, and says the tool "reports a
missing attestation; it never asserts a valid one." The tool did not *invent*
anything — the bytes really are in the file. It asserted a valid attestation
for a document structure that only exists inside its own line grammar. That is
a **frame-of-reference defect**, and it is the sharper failure: a checker that
stays silent is a gap, but a checker that prints `structurally sound` is a
claim, and the reader has no way to know which frame it was computed in.

### The two checkers disagree, and neither is right

The content-integrity scanner clears the same file:

    $ ~/conda_envs/lhm/bin/python templates/modules/team-gated/content_scan.py <fixture>
    content_scan: OK -- 1 file(s) scanned; no flags.   (exit 0)

Its `unicode-zero-width` rule covers `U+200B`–`U+200D` and `U+FEFF`; its
`unicode-bidi` rule covers `U+202A`–`U+202E` and `U+2066`–`U+2069`. Neither
`U+2028` nor `U+2029` is in either set. That scanner is not dormant —
`scripts/check_cairn.py` loads it by `importlib` and runs it over every tracked
`.md` — so the repository's own prose gate scans this file and passes it.

**Which one would a reader trust?** The planner, and that is the problem.
`content_scan`'s silence is an *absence* — its own docstring says it "never
*proves* a file safe." The planner's `structurally sound` is a *presence*: a
line of output that a reader, an agent relaying session-start orientation, and
a future `scan` sweep all read as a positive finding. A false absence costs a
missed catch. A false presence manufactures confidence. This proposal fixes the
false presence and leaves the false absence to its own proposal (see
*Alternatives considered*).

### The same module already contains both definitions of "a line"

`_read_artifact` in `tools/lifecycle_planner.py` computes some facts with
`splitlines()` and one — `has_followups_migrated` — with `re.search(...,
re.MULTILINE)`, whose `^` matches only after `\n`. The two disagree on the same
text:

    splitlines() sees the Follow-ups line:       True
    re.MULTILINE '^' sees the Follow-ups line:   False

This is not a hardening request against an exotic threat. It is an internal
inconsistency inside one function, and the project has already picked a side
elsewhere: `scripts/claim_check.py` splits with `text.split('\n')` at line 290
and again at line 531. Cairn's reference claim-checker already agrees with
`grep`. Its lifecycle checker does not.

### Why this file, in particular

The two files this proposal touches are 2502 lines (1370 + 1132, as_of
2026-08-03) and ship verbatim to every adopter through
`_SKILLS_MAPPINGS` in `bootstrap/_scaffold/config.py`. That is exactly the set
`bootstrap/security_check.py` never scans: it imports `_ALWAYS_ON_MAPPINGS` and
`_MODULE_MAPPINGS` and never `_SKILLS_MAPPINGS`, while `SECURITY.md` describes
the release gate as covering "the shipped Python surface." A defect here has no
downstream catcher. (That omission is a separate finding with its own proposal;
it is cited here only as the reason this file deserves a careful fix rather
than a quick one.)

## Proposal

Add one module-private helper to each of the two lifecycle tools, and route the
five artifact-reading call sites through it.

```python
#: Line endings markdown, git, grep and ``re.MULTILINE`` agree on -- CR, LF,
#: CRLF, and nothing else.  ``str.splitlines()`` additionally splits on eight
#: separators (U+000B, U+000C, U+001C-001E, U+0085, U+2028, U+2029) that none
#: of those readers treats as a line break, so a structural read built on it
#: can attest a heading no human, no ``grep -n '^## '``, and no markdown
#: renderer sees.
_LINE_ENDING_RE = re.compile(r"\r\n|\r|\n")


def _split_lines(text: str) -> List[str]:
    """``str.splitlines()`` narrowed to markdown's own line endings.

    Byte-identical to ``str.splitlines()`` for any text free of the eight
    extra separators -- which is every tracked file in this repository.
    """
    if not text:
        return []
    parts = _LINE_ENDING_RE.split(text)
    if parts and parts[-1] == "":
        parts.pop()
    return parts
```

**Call sites changed** (five, plus the twins):

| file | line (as_of 2026-08-03) | function | what it decides |
|---|---|---|---|
| `tools/lifecycle_planner.py` | 397 | `_parse_status` | the artifact's lifecycle state |
| `tools/lifecycle_planner.py` | 412 | `_parse_field` | `Author`, `Plan review` |
| `tools/lifecycle_planner.py` | 421 | `_parse_sections` | which `## Review` / `## Decision` sections exist |
| `tools/lifecycle_planner.py` | 464 | `_has_isolated_blockquote` | whether a Decision's authorization is present and isolated |
| `tools/lifecycle.py` | 494 | `_status_of` | the status shown in session-start orientation |

The twins `templates/skills/_lib/lifecycle_planner.py` and
`templates/skills/_lib/lifecycle.py` take the identical edit in the same commit
— `bootstrap/tests/test_notice_install.py`, node
`test_every_self_hosted_twin_stays_byte_identical_to_its_source`, is the gate
that enforces it.

**Call sites deliberately NOT changed**, each with its reason:

* `tools/lifecycle_planner.py:1032` and `tools/lifecycle_planner.py:1058` —
  these split **git and subprocess stdout**, which is LF-emitted by
  construction. `splitlines()` is correct there and narrowing it buys nothing.
* `tools/lifecycle.py:615` — a `.gitignore` membership test that feeds a
  **write** path (the gitignore repair). Not a lifecycle artifact, not an
  authority claim, and pulling a write path into this change would widen the
  gate set. Recorded as a follow-up below.
* `scripts/check_cairn.py:346` and `scripts/check_cairn.py:462`, and the
  content scanner and its runner — **detectors**, not attestors. Narrowing
  their split changes reported line numbers and, in
  `templates/modules/team-gated/content_scan_runner.py`, the line-scope of
  `cairn-accept` suppression markers. That is a security-gate contract on a
  surface `AGENTS.md` names a Security-Review trigger. It gets its own
  proposal; bundling it here would drag a Security-Review tier over a
  five-line fix.

**The helper is duplicated across the two files on purpose.** The planner's own
module docstring states it is "a **sibling** to `tools/lifecycle.py`,
deliberately NOT an extension of it." Introducing a shared import between them
would be a new coupling — a new abstraction — which this proposal declines. A
nine-line private helper in each is the smaller commitment.

**No literal separator appears in this proposal.** Every reproducer constructs
the character with `chr(0x2028)`, and every fixture is built at test time.
Committing a carrier into the deliberation record would be its own defect.

### Documentation / doctrine surface

* **In-code (descriptive layer)** — the docstring block shown above, in both
  tools. This is where the line grammar becomes stated rather than assumed.
* **`doctrine/lifecycle-contract.md` — not changed.** The contract already
  places "the current `Status:`" and structural precondition presence on the
  machine-verifiable side; it does not need a new clause to mean that the tool
  should read the artifact the way the artifact's readers read it. Adding a
  sentence there would be a doctrine change with a rate-limit gate to clear, in
  exchange for restating what the code now enforces. Declined, and named here
  so the omission is deliberate rather than silent.
* **`CHANGELOG.md`** — one line, landed at the plan-archive or goodnight
  serialization point, not in the implementing commit (`AGENTS.md` > *Shared
  communication files*).
* **`docs/`** — **N/A**: there is no descriptive page for either tool
  (`grep -rln lifecycle_planner docs/` is empty, as_of 2026-08-03).

### Doctrine-change rate-limit (if this proposal changes doctrine)

**Not applicable — this proposal changes no doctrine.** It changes two Python
files and two test modules, and explicitly declines the one doctrine edit that
was on the table (above). If the Maintainer prefers the contract sentence
after all, that is a separable follow-up which would then need to clear the
gate on its own evidence.

### Cross-lineage file collisions, and what actually has to sequence

This proposal is the most collision-exposed of its cohort: **both** tools it
edits are also claimed by another in-flight proposal, one apiece, and the two
claimants come from **different lineages**. (The two test modules are not
contested — `agent-context-scrub` adds its nodes to
`bootstrap/tests/test_skills_security.py`.) Recorded here rather than
discovered at merge time.

| file (both sides of the twin pair) | also claimed by | lineage |
|---|---|---|
| `tools/lifecycle.py` | `agent-context-scrub` | Theme 3 (sibling draft) |
| `tools/lifecycle_planner.py` | successor scope 2, the byline classifier | `2026-08-03-claude-identity-not-name` |

**One root cause, three surfaces.** All three changes have the same shape:
*raw external text reaches an authority-bearing decision without being
normalized first.* For `agent-context-scrub` the external text is git output
and filenames reaching the orientation stream a Maintainer reads; for this
proposal it is artifact bytes reaching a structural attestation; for scope 2 it
is a Decision byline reaching a human-versus-AI classification. They are
therefore **reviewed in one sitting and kept as three separate proposals**.
Merging them is not a shortcut, it is the specific mistake that earned
`2026-08-03-claude-identity-not-name` a REVISE/SPLIT verdict on 2026-08-03:
four surfaces inside one artifact could not carry four gate sets, and the
strictest tier dominated the rest. One proposal, one contract, one gate set —
one reviewer, one sitting, three artifacts.

**Collision 1 — `tools/lifecycle.py`, shared with `agent-context-scrub`.
Independent, and the two drafts already agree with each other.** That draft's
third application site states that `_status_of` "needs no change of its own",
because its *caller* `_in_flight` wraps the return value in a `_safe_field`
escaper. This proposal changes `_status_of`'s internals — which line the status
is read from. The two edits sit on opposite sides of the same return value:
this proposal decides *which* string `_status_of` returns, `agent-context-scrub`
decides how that string is *rendered* when relayed. No shared line, no ordering
constraint, either order lands. Two points for the joint sitting:

* That draft's `_safe_stream` helper carries **this proposal's rule, derived
  independently** — its comment says to use `split("\n")` and never
  `splitlines()`, because `splitlines()` also splits on the very separators the
  escaper is escaping. Two proposals arriving at markdown's line grammar from
  opposite ends is evidence the rule is right; it is not a reason to bundle
  them.
* That draft's escape table covers `0x2028` and `0x2029`. So once both land, a
  carrier artifact's status becomes *visibly escaped* in the orientation
  stream. That is a **partial** answer to this proposal's fourth *Signals the
  change is wrong* entry — partial, because it covers the orientation stream
  only, not `lifecycle_planner scan` / `next` output. The `content_scan`
  follow-up remains the real home for detection.

**Collision 2 — `tools/lifecycle_planner.py`, shared with
`2026-08-03-claude-identity-not-name` successor scope 2. No code overlap, one
real coupling, and it runs in one direction.** The two edits touch disjoint
functions in the same module:

| this proposal edits | scope 2 edits |
|---|---|
| `_parse_status`, `_parse_field`, `_parse_sections`, `_has_isolated_blockquote` | `_identity_token`, `_ai_candidate_tokens`, `_load_human_maintainers`, `IdentityModel.classify` |

They are nonetheless joined by a **data flow**, and this proposal is upstream:
`_read_artifact` calls `_parse_sections`, which produces each section's byline
into `Section.name`, which the conformance check hands to
`IdentityModel.classify`. The line splitter decides *which headings exist and
what byline string is extracted*; scope 2's classifier decides *whether that
byline is a human Maintainer*.

The coupling is this. **`str.splitlines()` is, accidentally, a sanitizer.** A
byline cannot today contain any of the eight extra separators, because the
split happens *at* them — so the classifier has never had to handle one.
`_split_lines` removes that accident. Measured against the two files as they
stand (byte-identical between `3292f21` and `7639ec5`), canonical Python
3.13.13, 2026-08-03 — the heading is built with `chr(0x2028)`, never a literal:

    heading: "## Decision -- Anthony<U+2028>Kendall (Maintainer) -- 2026-08-03"

    HEAD  _parse_sections  ->  [('Decision', 'Anthony')]
    PATCH _parse_sections  ->  [('Decision', 'Anthony\u2028Kendall')]

Under the classifier **as it stands today** — per-token, and all eight
separators are `str.isspace()` — both bylines classify `human`. This proposal
is therefore **byline-neutral as things stand, and nothing has to land first**:

    classify('Anthony')               [today, per-token]  ->  human
    classify('Anthony\u2028Kendall')  [today, per-token]  ->  human

Under **scope 2's** proposed whole-name matching they diverge, and in the unsafe
direction:

    classify('Anthony')               [scope 2]  ->  unknown  folded='anthony'
    classify('Anthony\u2028Kendall')  [scope 2]  ->  human    folded='anthonykendall'

The amendment's rule 1 poisons "any *remaining* non-ASCII **letter**" after
`NFD` and combining-mark stripping. `U+2028` is Unicode category `Zl`: it
survives `NFD`, survives combining-mark stripping, is **not a letter**, and is
then deleted by the `[^a-z0-9]` fold — converting a byline that is *not* the
roster name into one that *is*. That is scope 2's own stated invariant
violated: *dropping a character must never widen authority.* The correction is
scope 2's to make and it is one word wide — poison any surviving non-ASCII
character, not just letters. It is recorded here because **this proposal is
what makes that input class reachable.**

**Ordering, stated plainly, because an unfounded constraint costs schedule for
nothing.** Neither proposal blocks the other. There is no shared function, no
shared line, and no merge conflict; and under the live classifier this proposal
does not change a single byline's classification. What the collision creates is
a **review obligation, not a schedule dependency**: scope 2 must not be
reviewed as though `str.splitlines()` were still bounding its input alphabet.
The joint sitting discharges that. If the two are ever reviewed *separately*
after all, then scope 2 goes second, or its poison rule is widened first.

**Shared serialization points.** Both files ship byte-identically to
`templates/skills/_lib/` (verified with `cmp`, 2026-08-03) and both carry a
`verbatim: true` row in `dev/.cairn/cairn-lock.yml`. Whichever proposal lands
second re-runs the twin-parity gate and re-records the same lockfile rows —
which all three proposals in this cohort touch. That is churn and a
serialization point, not risk; it is the one concrete argument for landing the
cohort in one window rather than across weeks.

## Rationale

**Which user workflow does it improve?** The postdoc's. Two of the five call
sites are on the daily path: `_status_of` feeds the in-flight survey printed at
every session start, and `_parse_status` feeds `lifecycle_planner next`, the
command that tells a first-time adopter what they are allowed to do next with a
proposal. Today those two can report a state the adopter cannot see in their own
editor, with no indication that a second frame exists. In the first two weeks —
before an adopter has any calibration for which of Cairn's outputs to trust — a
checker whose claims silently disagree with `grep` is worse than no checker,
because the adopter has no basis for doubting it.

**What contract does it preserve or clarify?** `doctrine/lifecycle-contract.md`'s
authority boundary. The tool is licensed to attest *structure*. This makes
"structure" mean the same thing to the tool as it means to the record's human
readers, which is the unstated premise the whole attestation rests on.

**What correctness does it improve?** It removes a false-positive attestation
on the Decision surface — the single most authority-bearing artifact in the
method — and it removes an internal contradiction where one function computes
two facts under two incompatible line grammars.

**Why now?** Three reasons, in order of weight. (1) It is live at `3292f21`,
reproduced above. (2) The repository is pre-first-external-adopter; changing a
checker's output semantics costs nothing today and costs an adopter's trust
later. (3) Both files are claimed by other in-flight proposals — one per file,
from two different lineages — so landing this in the same window spares a second
round of twin-parity and lockfile churn. That is a scheduling convenience, not a
dependency: the collisions are enumerated and dispositioned in *Proposal >
Cross-lineage file collisions*, and none of them blocks this proposal.

**Why this tier (`required(External)`).** The mechanical half of this change
needs no tier at all — "is the replacement equivalent" and "did you find every
call site" are both machine-checkable, and this proposal ships the checks. The
load-bearing judgment is the **scope call**: fix the frame (agree with
markdown) rather than add a detector (flag the separators). A fresh-session
same-type reviewer shares the author's priors on exactly that question — an
Internal read would very likely arrive at the same answer for the same reasons,
which is not independence, it is an echo. The tier is buying a challenge to the
scope call from a reader who does not share the prior, on a file that ships to
every adopter and sits outside the release security scan's target list.

This is **not** an External *Security* Review by any of `AGENTS.md`'s
enumerated triggers: it touches neither `bootstrap/_scaffold/` nor
`bootstrap/security_check.py` nor `bootstrap/SAFETY.md` nor the content
scanner, and it does not touch `_resolve_interpreter`, its schema, its
validation order, its fallback disposition, its warning visibility, or its
subprocess use. The Maintainer may of course classify the Decision-attestation
surface as high-risk and escalate; that call is theirs, not the author's.

## Alternatives considered

1. **Do nothing.** The defect is live and silent, the fix is five lines, and
   the repository is about to hand these files to an external adopter. Rejected.
2. **Extend `content_scan`'s unicode detectors to `U+2028`/`U+2029` instead.**
   This is the *complementary* change, not the *alternative* one — it would
   make the injection visible, but the planner would still compute
   `structurally sound` in a frame no reader shares, because the detector
   cannot repair the attestor. It also lands on a surface `AGENTS.md` names a
   Security-Review trigger and would change `cairn-accept` suppression
   line-scoping. Correctly a separate proposal with its own gate set; bundling
   was rejected on the "one proposal, one contract, one gate set" rule.
3. **Make the planner *warn* when an artifact carries any of the eight
   separators.** This is a new detection mechanism, and it collides head-on
   with the standing *fix defects, build nothing new* direction. Stated plainly
   rather than smuggled in: the CR/LF split is not a security filter, it is the
   tool agreeing with markdown's own definition of a line, which is what it
   always meant to do. Detection is a real want; it belongs to alternative 2's
   proposal, where the reviewer expects a detector.
4. **Normalize the eight separators away on read (`text.replace(...)`).** This
   silently rewrites the artifact's content in memory before parsing, which
   means the tool's reported line numbers would no longer correspond to the
   file. Splitting correctly costs the same and keeps line numbers honest.
5. **Fix only the four planner call sites and defer `tools/lifecycle.py:494`.**
   Rejected: `_status_of` is the identical defect, in the identical shape, on
   the surface an adopter sees most often, fixed by the identical helper under
   the identical gate set. Deferring it would be scope discipline performed
   rather than practiced.
6. **A shared line-splitting module imported by both tools.** Rejected as a new
   abstraction across a boundary the planner's docstring deliberately keeps
   separate.

*Maintainer preference during drafting*: none — this draft incorporates no
chat-mode preference beyond the two standing directions (**postdoc-first**,
**fix defects, build nothing new**), both of which are addressed explicitly
above.

## Evidence / verification plan

Every command below was run at `3292f21` on the canonical interpreter
(`~/conda_envs/lhm/bin/python`, Python 3.13.13) on 2026-08-03. The Cairn tree
was not modified: the fixture, the git repository it lives in, and the patched
copy of the planner all live in a throwaway scratch directory.

**1. The separator set (live invariant).**

    $ ~/conda_envs/lhm/bin/python -c "
    seps=[c for c in range(0x3000) if len(('a'+chr(c)+'b').splitlines())>1]
    print([hex(c) for c in seps if c not in (0x0A,0x0D)])"
    ['0xb', '0xc', '0x1c', '0x1d', '0x1e', '0x85', '0x2028', '0x2029']

**2. The fixture.** A proposal carrying a real `## Review` and `## Response`,
a visible `**Status**: proposed`, and two `U+2028`-glued payloads: an earlier
`**Status**: accepted` (which `_parse_status` finds first) and a
`## Decision -- Anthony Kendall (Maintainer) -- 2026-08-03` with an isolated
`>` authorization. 49 real newlines; `splitlines()` reports 57 lines.

**3. What line-oriented readers see.**

    $ wc -l < <fixture>                 =>  49
    $ grep -c '^## ' <fixture>          =>  7
    $ grep -n '^## Decision' <fixture>  =>  (no output, exit 1)
    $ grep -n 'Status' <fixture>
    13:cache size so a warm run stops paying that cost. **Status**: accepted
    14:**Status**: proposed

**4. What a CommonMark renderer produces** (`markdown-it` CommonMark preset;
a dev-only measurement tool, not a Cairn dependency): seven `<h2>` elements —
Context, Proposal, Rationale, Alternatives considered, Evidence / verification
plan, Review, Response. No Decision heading. The payload lands inside a `<p>`
with the blockquote marker escaped to `&gt;`.

**5. What `git diff` shows a reviewer.**

    dev/proposals/2026-08-03-agent-cache-tuning.md | 4 ++--
    1 file changed, 2 insertions(+), 2 deletions(-)

**6. What the two checkers say.**

    $ ~/conda_envs/lhm/bin/python tools/lifecycle_planner.py next <fixture>
    lifecycle-planner: current state: accepted
    lifecycle-planner: structural conformance: current state is structurally sound.
    lifecycle-planner: (terminal state -- no status transition; ...)

    $ ~/conda_envs/lhm/bin/python templates/modules/team-gated/content_scan.py <fixture>
    content_scan: OK -- 1 file(s) scanned; no flags.        (exit 0)

    tools/lifecycle.py::_status_of(<fixture>)  ->  'accepted'

**7. The same commands against a patched copy of the planner** (the helper
above, five call sites rerouted):

    lifecycle-planner: current state: proposed
    lifecycle-planner: structural conformance: current state is structurally sound.
    lifecycle-planner: -> reviewed
    lifecycle-planner:      [ok ] append a '## Review' ...

The checker now reports what `grep` reports. Note plainly: it does **not**
report the injection. Detection is alternative 2's proposal.

**8. Zero regression — byte-identical line splits over the real corpus.**
`_split_lines(t) == t.splitlines()` was asserted for every tracked file that
decodes as UTF-8:

    dev/ corpus (tracked):                       87 files, 87/87 identical, 0 carriers
    dev/proposals + dev/plans (planner corpus):  27 files, 27/27 identical, 0 carriers
    whole tracked tree:                         465 files, 465/465 identical, 0 carriers

(counts as_of 2026-08-03). "Carriers" = files containing any of the eight
separators; there are none. The sweep was run with a **positive control** — the
fixture, which the same sweep correctly reports as a carrier with a
57-vs-49-line disagreement — so a silently-broken detector cannot produce this
result.

**9. Zero regression — byte-identical tool output.** HEAD's planner and the
patched planner were run over the real repository and their stdout+stderr
compared:

    $ lifecycle_planner.py scan          ->  sha256 f8cc147e...  (both, exit 1)
    $ lifecycle_planner.py next <each of the 27 tracked artifacts>
                                         ->  sha256 1a1ee8d1...  (both, 283 lines)

Identical, including the two pre-existing `scan` violations on
`2026-07-22-claude-stage-commit-patterns` and `2026-07-22-claude-transition-lint`,
which are unrelated to this proposal and are neither introduced nor resolved by it.

**10. Suite baseline.** `python -m pytest bootstrap/tests` at `3292f21` on
Python 3.13.13: **1556 passed**, 0 failed, 3 warnings, 145s (as_of
2026-08-03). `test_lifecycle_contract.py` + `test_notice_install.py` alone: 40
passed.

**11. The scope audit.** All 41 `splitlines()` call sites in the self-hosted
`tools/` + `scripts/` trees (47 `.py` files, as_of 2026-08-03), classified:

| class | count | disposition |
|---|---|---|
| machine output (git / subprocess stdout) | 9 | correct as-is; unchanged |
| human markdown → structural / authority fact | 5 | **this proposal** |
| human markdown → detection / line-number reporting | 2 | separate proposal (alternative 2) |
| config, hook text, prose, metrics extraction | 25 | out of scope; see follow-ups |

### Author-accounting — invariants, failure modes, edge cases

This is a public-path behavior change on an attestation surface, so the block
is filled rather than waived.

* **Invariants.**
  * *`_split_lines(t) == t.splitlines()` for every `t` free of the eight extra
    separators.* Enforced by a new property test over the tracked corpus plus a
    synthetic edge-case table (empty string, `"a"`, `"a\n"`, `"a\n\n"`, `"\n"`,
    `"\r\n"`, `"a\r\nb"`, `"a\rb\r"`, `"a\r\n\r\nb\r\n"`, trailing-blank runs).
    All twelve synthetic cases already pass against the draft helper.
  * *The planner's structural state for a file matches what `^`-anchored grep
    would find.* Enforced by a new regression test built on a `chr(0x2028)`
    fixture asserting `current state: proposed` and zero Decision sections.
  * *The twins stay byte-identical.* Already enforced by
    `bootstrap/tests/test_notice_install.py`, node
    `test_every_self_hosted_twin_stays_byte_identical_to_its_source`; no new
    enforcer needed, which is the point of citing it.
  * *The planner stays read-only.* Unchanged and already enforced by the
    existing no-write test in `bootstrap/tests/test_lifecycle_contract.py`.
* **Failure modes.**
  * A file whose only line endings are among the eight extras parses as **one
    line**. *Open* (degrades), and **intentional**: that is what `grep`, git,
    and markdown do with such a file, and agreeing with them is the whole
    change. No such file exists in the tracked tree (evidence 8).
  * A lone CR (`\r`) line ending. *Handled* — the regex alternation puts
    `\r\n` first, so CRLF never splits twice, and a bare CR splits, matching
    both CommonMark and `str.splitlines()`.
  * A malformed or unreadable artifact. Unchanged: `PlannerError` /
    the existing `except OSError` in `_status_of`. *Closed* and *open*
    respectively, as today.
* **Edge-case inventory.** Empty string → `[]` (matches `splitlines()`);
  single line without trailing newline → one element; trailing newline → no
  phantom empty element; multiple trailing newlines → the same count
  `splitlines()` gives; CRLF-only file → handled; mixed CRLF/LF → handled;
  N≫1 (the 1132-line planner corpus and the 465-file tree) → verified
  identical. **Out of scope:** non-UTF-8 artifacts (the tools already read
  with `encoding="utf-8"` and fail or replace as they do today).
* **Public-path → test mapping.**
  * `lifecycle_planner.py next <artifact>` and `scan` → new nodes in
    [`bootstrap/tests/test_lifecycle_contract.py`](../../bootstrap/tests/test_lifecycle_contract.py),
    exercised through the module's public `_read_artifact` / CLI path as the
    existing nodes there already do (that module importlib-loads the **template**
    copy, so the shipped artifact is what gets tested).
  * `lifecycle.py session-start` in-flight survey → a new node in
    [`bootstrap/tests/test_lifecycle_cli.py`](../../bootstrap/tests/test_lifecycle_cli.py),
    which likewise loads the template copy.
* **Known omissions / intentionally untested edges.** (a) No test asserts what
  a *browser* does with `U+2028` — CSS Text treats it as a forced line break,
  so a browser reader may see visual line breaks where a terminal shows none;
  the claims above are therefore made only about CommonMark structure and about
  line-oriented tools, both of which were measured. (b) No test covers the
  other six separators end-to-end through the CLI; they are covered by the
  property test, not by a fixture each. (c) Nothing here tests *detection* of a
  poisoned artifact, because this proposal deliberately does not add detection.

### Tests required

* **`bootstrap/tests/test_lifecycle_contract.py`** — three new nodes:
  the `chr(0x2028)` fixture regression (planner reports `proposed`, finds no
  Decision, and emits no `structurally sound` for a fabricated terminal state);
  the `_split_lines` ≡ `splitlines()` property test over synthetic cases; and
  the same property asserted over every tracked file under `dev/` so a future
  artifact that introduces a carrier fails loudly rather than silently.
* **`bootstrap/tests/test_lifecycle_cli.py`** — one new node: `_status_of` on
  a `chr(0x2028)` fixture returns the status a `^`-anchored grep finds.
* **`bootstrap/tests/test_notice_install.py`** — **N/A**: no new node; the
  existing twin-parity test is the gate and it already covers both files.

### Examples / smoke checks

* `python tools/lifecycle_planner.py scan` from the repository root — output
  must be byte-identical to the pre-change run (sha256 `f8cc147e...`, evidence 9).
* `python tools/lifecycle_planner.py next <artifact>` over all tracked
  proposals and plans — byte-identical (sha256 `1a1ee8d1...`).
* `python scripts/check_cairn.py` — the prose gate, for the docstring edit.
* `python -m pytest bootstrap/tests` — must return **1557 or more passed, 0
  failed** on Python 3.13.13 (1556 baseline + the four new nodes; stated as a
  floor, not an equality, because the two proposals that collide with this one
  add nodes to the same modules — see *Proposal > Cross-lineage file
  collisions*).
* **Example gallery** — **N/A**: `examples/` exercises neither lifecycle tool.
* **Scaffold smoke** — `python bootstrap/scaffold.py --dry-run` for
  completeness; no install-set change is proposed, so this is a null check that
  should stay null.

## Signals the change is wrong

* **`scan` or `next` output changes for any real artifact.** Recovery: revert;
  the byte-identity claim in evidence 9 was wrong, and the whole
  zero-regression argument goes with it.
* **A legitimate artifact stops parsing.** Would mean a real Cairn document
  depends on one of the eight separators as a line ending. Evidence 8 says none
  does today; if one appears, the right answer is to fix the document, and if
  that turns out to be burdensome, this proposal was scoped wrong.
* **A reviewer shows the CR/LF split is *not* markdown's rule** — e.g. a
  renderer in the adopter's toolchain that does treat `U+2028` as a heading
  boundary. That would invert the argument: the tool would then be right and
  the *reader* would be the one with the unusual frame. Recovery: revert and
  re-open on detection (alternative 2) instead of on frame agreement.
* **Someone reads this fix as "the injection is handled."** It is not; the
  fixture still passes both checkers after the change, just without a false
  attestation. If the follow-up on `content_scan` does not open, this proposal
  has made the record *quieter* rather than *safer*, which is the specific
  failure it is trying to avoid. Recovery: open the `content_scan` proposal.
* **Twin parity breaks in CI-less review** — i.e. the edit lands on one side of
  a twin pair. `test_every_self_hosted_twin_stays_byte_identical_to_its_source`
  catches it, but only if the suite is actually run, which per Theme 3 item 1
  depends on a human remembering.

**Follow-ups this proposal defers, with named homes:**

* `content_scan`'s unicode detectors do not cover `U+2028`/`U+2029` (and its
  suppression line-scoping inherits the same `splitlines()` frame) — its own
  proposal, Security-Review triggered.
* `tools/lifecycle.py:615` (the `.gitignore` membership read) — a follow-up
  bundled with any future change to the gitignore-repair path.
* The 25 class-D `splitlines()` call sites in `scripts/_onboarding/`,
  `tools/_intent/`, `tools/_lifecycle_metrics/`, and `tools/evolution_infer.py`
  — audited and triaged here (evidence 11), no action proposed; recorded so a
  future reader does not have to re-derive the triage.

## Review -- Gemini Flash (External, security lens) -- 2026-08-03

**Steelman.** This proposal correctly identifies and fixes a critical frame-of-reference mismatch between Python's standard `str.splitlines()` (which splits on 10 Unicode line separators) and CommonMark/git/grep line semantics (which split strictly on `\r` and `\n`). Replacing `splitlines()` with `_split_lines` across five human-authored markdown parsing call sites ensures that machine attestations (`structurally sound`) cannot be triggered by invisible `U+2028`/`U+2029` line splits that human readers, git diffs, and CommonMark renderers ignore.

### Concerns

* **[E1] Lack of active detection for injected line separators.**
  The proposed `_split_lines` helper prevents a `U+2028`-glued section header from being recognized as a heading by the planner, but it silently treats the payload as inline paragraph text rather than flagging the anomaly. As the proposal acknowledges, active detection is delegated to `content_scan`, but implementers must ensure that this change is not mistook for complete injection remediation.

### Covered

* **Python 3.13 `splitlines()` extra separators verification**:
  Ran execution check under Python 3.13.13 to confirm the eight extra line separators:

```
$ ~/conda_envs/lhm/bin/python -c "seps=[c for c in range(0x3000) if len(('a'+chr(c)+'b').splitlines())>1]; print([hex(c) for c in seps if c not in (0x0A,0x0D)])"
['0xb', '0xc', '0x1c', '0x1d', '0x1e', '0x85', '0x2028', '0x2029']
```

* **`U+2028` Section Header Injection Reproducer**:
  Executed test script with a `U+2028`-glued `## Decision` heading:
  - **`str.splitlines()`**: evaluated to 9 lines, successfully extracted `## Decision -- Anthony Kendall (Maintainer) -- 2026-08-03` as a section header.
  - **`_split_lines()`**: evaluated to 7 lines, correctly ignored the embedded `## Decision` heading.

```
splitlines() count: 9
narrowed _split_lines() count: 7
Headings under splitlines(): ['## Context', '## Response', '## Decision -- Anthony Kendall (Maintainer) -- 2026-08-03']
Headings under narrowed _split_lines(): ['## Context', '## Response']
```

### Not covered / low confidence

* CSS Text browser rendering of `U+2028` (which may render visual breaks in web views) was not tested.

### Recommendation

**SHIP.** The proposal addresses a demonstrated frame-of-reference defect with minimal code changes and zero regression across the existing repository corpus.

## Response -- Claude (author, to External review) -- 2026-08-03

**Verdict SHIP, one concern, one disposition.** A SHIP verdict does not make a
finding informational, so [E1] is dispositioned below rather than noted. Two
things the reviewer could not have checked are added on top, because both bear
on whether the Decision reads this proposal correctly: **the delegation
argument's named home does not exist and is not the sibling proposal that looks
like it**, and **a coupling claim in *Cross-lineage file collisions* is now
wrong and is retracted here**. Working-tree drift is recorded last.

Everything below was measured on 2026-08-03 under the canonical interpreter
(`/Users/kendal30/conda_envs/lhm/bin/python3.13`, Python 3.13.13, UCD 15.1.0),
against the **working tree** unless a line says `HEAD`. Every reproducer builds
the character with `chr(0x2028)`, and every separator that appears in a result
is written in escaped text form (`\u2028`). **No literal separator is written
in this section** — per this proposal's own rule, and per the notation
convention recorded in `content-scan-detectors` on 2026-08-03, under which an
invisible character is named or escaped and never written as the raw byte.

### Dispositions

**[E1] Lack of active detection for injected line separators — ALREADY-COVERED
as to the concern; ACCEPTED as to one correction the reviewer could not have
made.**

*The concern itself is already load-bearing in the proposal, in five places,
and the strongest of them is a tripwire rather than a caveat.* The reviewer's
own framing — "implementers must ensure that this change is not mistook for
complete injection remediation" — is verbatim the fourth entry under *Signals
the change is wrong*:

> **Someone reads this fix as "the injection is handled."** It is not; the
> fixture still passes both checkers after the change, just without a false
> attestation. If the follow-up on `content_scan` does not open, this proposal
> has made the record *quieter* rather than *safer*, which is the specific
> failure it is trying to avoid. Recovery: open the `content_scan` proposal.

That is not a disclaimer; it is a named failure mode with a named recovery. The
other four: *Alternatives considered* 2 classifies detection as "the
*complementary* change, not the *alternative* one" and says the detector
"cannot repair the attestor"; evidence 7 states after the patched output "Note
plainly: it does **not** report the injection"; *Known omissions* (c) says
"Nothing here tests *detection* of a poisoned artifact, because this proposal
deliberately does not add detection"; and the *Follow-ups* list carries
`content_scan`'s missing `U+2028`/`U+2029` coverage as a named deferral. The
proposal already refuses the mistake [E1] warns against.

*What was not covered, and is now.* The proposal delegates detection to "the
`content_scan` follow-up" and "alternative 2's proposal" without naming a stem.
On 2026-08-03 a proposal **is** in flight against exactly this surface —
`content-scan-detectors`, whose Change 1 adds a `unicode-ignorable` detector to
`templates/modules/team-gated/content_scan.py`. A reader is likely to conclude
the delegation is already discharged. **It is not, and it will not be.**
Measured rather than reasoned:

1. **`content_scan` at HEAD clears the payload.** A fixture carrying a
   `chr(0x2028)`-glued `## Decision` heading, a `chr(0x2028)`-glued
   authorization blockquote, and a `chr(0x2029)`-glued `**Status**: accepted`:

       $ python templates/modules/team-gated/content_scan.py <fixture>
       content_scan: OK -- 1 file(s) scanned; no flags.        (exit 0)

   Confirms evidence 6 independently, against the working tree.

2. **`content-scan-detectors` contains no mention of either code point.** Zero
   occurrences of `2028` or `2029` anywhere in its 2445 lines, across the
   proposal, both reviews, both Responses, and the Maintainer direction.

3. **Its detector set excludes them by construction, not by oversight.** Change
   1 adopts RFC 8264 § 9.13 `PrecisIgnorableProperties` —
   `Default_Ignorable_Code_Point OR Noncharacter_Code_Point`. Measured:

       U+2028  category Zl  LINE SEPARATOR       isspace() -> True
       U+2029  category Zp  PARAGRAPH SEPARATOR  isspace() -> True
       noncharacter(U+2028) -> False    noncharacter(U+2029) -> False

   Both are `White_Space=Yes`, and the `Default_Ignorable_Code_Point`
   derivation **subtracts** `White_Space`; neither falls in `FDD0..FDEF` nor on
   an `xFFFE`/`xFFFF` boundary. `content-scan-detectors` states its own
   completeness invariant over **`Cf`-category** code points ("every
   `Cf`-category code point in UCD 15.1.0 … falls inside the 17 hard-coded
   ranges"). `Zl` and `Zp` are outside that quantifier. The detector is
   complete against the set it names and that set does not contain these two.

4. **The 2026-08-03 Maintainer direction does not change this.** Its three
   dispositions — clause 1 is Greek-only, whole-script fullwidth Latin closed
   separately, the Tag block gets its own pattern id — all land inside Change 2
   and the pattern-id partition. None adds a separator to Change 1's ranges.

5. **The file is unmodified in the working tree**, so `content-scan-detectors`
   is not implemented either.

**Conclusion, stated plainly because it is a real coupling.** Even with
`content-scan-detectors` fully landed as directed, the fixture in evidence 2
still scans clean. This proposal's delegation-to-`content_scan` argument is
**sound but unhomed**: the follow-up it names is a proposal that does not exist
yet, and the in-flight proposal that appears to be its home will not discharge
it. The proposal's text is technically accurate — it never names a stem — but
proximity makes the wrong reading the natural one, and the record should not
depend on a reader noticing the absence of a name.

**What changes:** nothing in the proposed code, the call-site set, the tier, or
*Touches*. The *Follow-ups* entry stands as written and this Response is its
disambiguation — the `U+2028`/`U+2029` detector is **not** within
`content-scan-detectors`' accepted scope and needs its own proposal. Whether
this proposal's landing should be *conditioned* on that proposal being opened
is a Maintainer call and is carried to *Findings the Decision did not see*.

### Correction owed to the record — *Cross-lineage file collisions*, Collision 2

`dev/plans/byline-classification.md` records, under its non-archivable items,
that this proposal owes a correction at its own Response ([I7b]). This is that
correction; it is made here rather than by editing the prior section, which is
append-only.

**What the proposal says.** Collision 2 predicts that under scope 2 the two
bylines diverge in the unsafe direction:

    classify('Anthony')               [scope 2]  ->  unknown  folded='anthony'
    classify('Anthony\u2028Kendall')  [scope 2]  ->  human    folded='anthonykendall'

and concludes that "scope 2's own stated invariant" is violated, with a
correction "one word wide — poison any surviving non-ASCII character, not just
letters."

**What the landed design actually does.** Both statements describe the
*Amendment's* recipe, which `byline-classification` replaced. Measured against
the working tree:

    _flag_words('Anthony')                 ->  ('anthony',)
    _flag_words('Anthony\u2028Kendall')    ->  ('anthony\u2028kendall',)
    _flag_words('Anthony Kendall')         ->  ('anthony', 'kendall')

    classify('Anthony')                    ->  unknown
    classify('Anthony\u2028Kendall')       ->  unknown
    classify('Anthony Kendall')            ->  human

**There is no poison rule to widen.** The landed `_fold_word` keeps a character
when `ord(c) > 0x7F`, so `U+2028` *survives into the comparison key* instead of
being deleted out of it; and `_ASCII_WS_RE` is `[ \t\n\r\f\v]+`, so `U+2028` is
not a word separator either. The glued byline therefore folds to a **single**
word that cannot equal the two-word roster key. That is the same invariant the
proposal was defending — *dropping a character must never widen authority* —
reached by keeping rather than by poisoning.

**End-to-end, through this proposal's own patch:**

    HEAD  _parse_sections  ->  [('Decision', 'Anthony')]
    PATCH _parse_sections  ->  [('Decision', 'Anthony\u2028Kendall')]
          classify('Anthony\u2028Kendall')  ->  unknown

The parse claim in Collision 2 still holds exactly. Only the classification
consequence was wrong.

**The figures were correct when measured, and the staleness has a cause.** The
proposal's `[today, per-token]` line is reproducible at `HEAD`'s planner
against `HEAD`'s roster `["Anthony", "Kendall"]`: both bylines return `human`,
as stated. `byline-classification` changed the classifier *and*
`dev/.cairn/agent-identities.json` (to `["Anthony Kendall"]`) in the same
uncommitted change, which is what moved both figures to `unknown`.

**Retracted:** the claim that scope 2 violates its own invariant, and the
prescription that its poison rule be widened. **Unchanged and reconfirmed:**
this proposal is **byline-neutral** — the two sides classify identically before
and after the patch — and it is now neutral at `unknown` rather than at
`human`, which is the safe direction. **Also unchanged:** the ordering
conclusion. Neither proposal blocks the other, and the review obligation
Collision 2 exists to create has now been discharged in the only way that
matters: the input class this proposal makes reachable was checked against the
classifier that actually shipped.

### Working-tree drift against the proposal's citations

`byline-classification` has landed in the working tree, uncommitted
(`+202 / -58` on each side of the planner twin pair). Verified:

* **Every planner line citation has drifted.** The four changed call sites move
  by +142 — `_parse_status` 397 → 539, `_parse_field` 412 → 554,
  `_parse_sections` 421 → 563, `_has_isolated_blockquote` 464 → 606 — and the
  two deliberately-unchanged sites by +144, 1032 → 1176 and 1058 → 1202.
* **No quoted behaviour drifted.** All four target functions are **textually
  identical** to `HEAD` (compared by extracting each function's source range
  with `ast` and diffing). The change is positional only; the call sites, the
  splits, and the `[:60]` windows are as the proposal describes.
* **`tools/lifecycle.py` is unmodified.** Lines 494 (`_status_of`) and 615 (the
  deferred `.gitignore` read) are still exact.
* **Twin parity holds on both pairs** (`cmp`, exit 0), so the proposal's
  same-commit twin-edit requirement is unaffected.
* **Two dated figures are stale.** The file-size figure "2502 lines (1370 +
  1132)" is now 1370 + 1276 = **2646** — `tools/lifecycle.py` is unchanged and
  the planner grew. The suite baseline "1556 passed" is now **1709 collected**
  in the working tree. The smoke-check floor was deliberately written as "1557
  or more … stated as a floor, not an equality" for exactly this reason, so it
  survives; it should be re-anchored to the real baseline at plan time rather
  than left as a floor 152 nodes below it.
* **`bootstrap/tests/test_lifecycle_contract.py` is also modified** by
  `byline-classification`. This proposal adds three nodes to that same module.
  Not a conflict — both append — but it is a second serialization point
  alongside the lockfile rows already named.

None of this changes the proposal's argument, its call-site set, or its
*Touches*. It changes which lines an implementing agent should open, so it is
recorded rather than left to be discovered at implementation.

### Findings the Decision did not see

Both are undecided and are recorded, not resolved.

* **This proposal landing alone newly admits a raw `U+2028` into the
  orientation stream — and the proposal does not say so.** The proposal applies
  its own insight that "`str.splitlines()` is, accidentally, a sanitizer" to
  the *byline* surface and never to the *status value*. Measured, on a file
  whose status line is `**Status**: prop<chr(0x2028)>osed`:

      HEAD  _status_of  ->  'prop'
      PATCH _status_of  ->  'prop\u2028osed'

  `_in_flight` relays that value into the survey the Maintainer reads at every
  session start, unescaped, until `agent-context-scrub` Chunk A lands. The
  proposal's Collision 1 bullet says a carrier artifact's status becomes
  "*visibly escaped*" once both land, which is true, but it never states that
  **this change is what puts the raw separator there**. The window is disclosed
  on the sibling's side — `dev/plans/agent-context-scrub.md` records it under
  "Three facts an implementing agent must hold together", mandates that this
  proposal land in both twins before its Chunk A, and lists the landing order
  as the first of the three questions that plan is most exposed on. It is not
  disclosed on this side. It is a transient, ordering-created regression on the
  carrier path only — evidence 8 establishes the tracked tree has zero carriers,
  so no real artifact is affected — but "no real artifact today" is the same
  argument this proposal declines to accept elsewhere. Undecided: whether the
  window is acceptable, and whether the two changes must land in one session,
  are Maintainer calls on landing order, not author calls.
* **Whether landing is conditioned on the detection follow-up being opened.**
  The fourth *Signals the change is wrong* entry makes "the `content_scan`
  follow-up does not open" a named failure mode with "open the `content_scan`
  proposal" as its recovery. Per the [E1] disposition above, no open proposal
  discharges it and `content-scan-detectors` will not. The tripwire is
  therefore currently unsatisfied. Whether that is acceptable at Decision time,
  or whether the detection proposal should be opened first or in the same
  window, is the Maintainer's to decide.

## Decision -- Anthony Kendall (Maintainer) -- 2026-08-03

**Accepted, conditioned on the detection follow-up being opened. The condition
is discharged.** Scribed by Claude (Strategy) at the Maintainer's explicit
instruction.

**Maintainer's authorization (verbatim), given in two parts:**

> I accept planner-line-semantics. The basis is the External review's SHIP verdict together with the author's Response dispositioning [E1]. Scribe the Decision and commit it.

and, after the author surfaced two findings the Response had raised *after*
that authorization was given:

> Condition the accept on the follow-up being opened.

Both are quoted rather than paraphrased, per the scribing guard-rail. The
second is recorded because the first was given before the Response's closing
findings were in front of the Maintainer, and an accept must not silently
absorb what its stated basis did not cover.

**Scribe-coupling disclosure.** The scribe is the proposal's author — the
weaker configuration. Mitigations: both authorizations quoted verbatim and
visually isolated, and this commit carries the Decision only.

### The condition, and its discharge

The Response disposed [E1] as already-covered *on the concern* but found the
delegation **sound but unhomed**: `content_scan` returns `OK — no flags`,
exit 0, on a `U+2028` / `U+2029` fixture, and `content-scan-detectors` excludes
both **by construction** — `U+2028` is `Zl`, `U+2029` is `Zp`, both
`White_Space=Yes`, which the `Default_Ignorable_Code_Point` derivation
subtracts. So this proposal's documented delegation pointed at a control that
would not exist even after its sibling landed as directed.

**Discharged by `separator-detection`, opened at `c40c959`**, which claims that
surface and nothing else. The condition is therefore satisfied at Decision
time rather than left outstanding.

### What this accept covers, and what it does not

**Covered.** The parser fix: `_parse_status`, `_parse_field`, `_parse_sections`
and `_has_isolated_blockquote` stop disagreeing with the human reader about
what a line is. The External review's SHIP verdict stands, and [E1] is
dispositioned.

**Explicitly not covered — the two findings the Response listed as undecided:**

1. **This proposal landing *alone* newly admits a raw `U+2028` into the
   orientation stream.** Measured: `_status_of` returns `'prop'` at HEAD and
   the glued value once patched, relayed unescaped until `agent-context-scrub`
   Chunk A escapes it. This is an argument **for** the ratified landing order,
   not against it — but it is recorded here rather than inherited silently, and
   it means this proposal should not land into a tree where
   `agent-context-scrub` is not following.
2. **Same-line masking and the wider `Zs` question** stay where they are —
   `content-scan-detectors` [I3] and `byline-classification` respectively.

### One retraction the Response made, worth carrying into the plan

The proposal predicted a `U+2028`-glued byline would classify `human`. Measured
against the landed `byline-classification`, it classifies **`unknown`** — the
safe direction. The original figures were correct when taken; the classifier
and the roster both changed underneath them. **The invariant-violation claim
and the "one word wide" prescription are retracted**, and a plan opened from
this proposal must not carry them.
