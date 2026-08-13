# Plan: the ceremony as verified code

**Source proposal**: `dev/proposals/archive/2026-08-13-claude-ceremony-as-code.md`,
accepted as revised at Revision 4 (`## Decision -- Anthony Kendall (Maintainer)
-- 2026-08-13`).
**Status**: awaiting-plan-review
**Plan review**: required(**External Security Review**) — set by the Decision.
Four External passes shaped this contract and each found a real defect; the
implementation changes what executes during the trust-root ceremony.
**Last update**: 2026-08-13
**Opened**: 2026-08-13

## Source proposal

The accepted contract is R1–R10 of Revision 4, as amended by the withdrawal
ledgers. This plan maps it to files and does not restate it; where plan and
proposal disagree, **the proposal governs**.

**The objective is the acceptance test**, quoted from the accepted contract
because every chunk below is measured against it rather than against size:

> The re-anchor ceremony must be performable, end to end, by the Maintainer
> alone — without an agent generating a script, retyping a digest, or
> improvising a reader — and without any control being weaker than it was
> before.

## Proposed paths

Proposed paths:
- `bootstrap/reanchor.sh` — the ceremony artifact named by the Decision; created in Chunk C, joins the authority closure at M3.
- `bootstrap/reanchor-values.example` — the values-file template a Maintainer copies and fills outside the repository; created in Chunk B.
- `bootstrap/tests/test_reanchor.py` — the artifact's own contract tests; created in Chunk B and grown through F.

## Scope

**In scope**: the launcher and packet (R1, R6, R9, R10), the values schema
(R2, R7), the operator command surface (R3), the step registry and
doc-agreement tests (R4), the two key-probe corrections (R5 riders 1–2), the
dedicated-key rollover (R8), the finding-tag cleanup (R5 rider 4), the runbook
restructure, and `SECURITY.md`'s adopter-facing key guidance.

**Explicitly out of scope**: the accepted host-persistence residual, the
key-holder-not-process limit, and the no-nonce replay posture. This plan does not
reduce them. It also does not change N4's substance — the Maintainer's key act
remains human.

**One accepted-scope fence, declared not assumed.** R5 makes riders 1 and 2 the
**implementation floor**: the new operator surface must not land while the key
probe still measures a channel candidate code can bypass. Chunk A therefore
precedes the surface work and is not reorderable.

### Documentation / doctrine surface

* `bootstrap/REANCHOR_RUNBOOK.md` — restructured (Chunk F). Governing layer; it
  prescribes an operational procedure and stays where it is.
* `SECURITY.md` — the dedicated-key requirement and why a shared authentication
  key makes N4 fragile (Chunk H). Descriptive layer, adopter-facing.
* **No doctrine change.** R1-F is unchanged; this plan makes it true rather than
  amending it, so the doctrine rate-limit gate does not apply.

## Sequence

```
PR  External Security Review of this plan                    [required]
A   the two key-probe corrections (the floor)                [commit]
B   the values schema, parser, and `validate`                [commit]
C   the ceremony artifact and its subcommands                [commit]
D   the packet, the launcher, and their binding              [commit]
E   the step registry and the doc-agreement tests            [commit]
F   the runbook restructure                                  [commit]
G   the finding-tag cleanup                                  [commit]
H   SECURITY.md adopter guidance                             [commit]
--- stable bytes -----------------------------------------------------
B1  Boundary B, full, on the stable pre-review commit        [record]
CR  independent code review                                  [review]
M2  exact-byte External Security Review + launcher/packet    [Maintainer]
M3  the ceremony: key rollover AND transition, in one        [Maintainer]
M4  atomic publication                                       [Maintainer]
```

**Orderings that are load-bearing:**

* **A first**, per the accepted fence above. A nicer operator surface over a
  weaker probe fails the objective's second half.
* **B before C.** The artifact's every subcommand reads the values file, so its
  schema and refusals must exist before the commands that consume them.
* **C before D.** The launcher extracts and hashes the artifact; the artifact
  must exist to be named, hashed, and placed in the closure.
* **D before E.** The registry enumerates the steps the launcher and artifact
  actually perform.
* **F after C–E.** The runbook records what the code does; written earlier it
  records an intention. This is the parent plan's own lesson, applied.
* **G anywhere after A**, and deliberately not first: the tag cleanup touches
  files Chunks A–E also edit, and doing it first guarantees conflicts.

**No chunk moves a Cairn ref, loads a key, or runs a ceremony.**

### Chunk A — the key-probe corrections ([R5] riders 1–2, the floor)

| # | File | Change |
|---|------|--------|
| A1 | `bootstrap/tests/_gate_preflight.py` | the probe must measure **the channel candidate code has**. Either it stops dropping `SSH_AUTH_SOCK` for itself, or the ceremony stops forwarding it to Stage 1 — the plan picks one and the runbook's claim matches |
| A2 | same | the "non-interactive" docstring is corrected: `ssh-keygen` reads `/dev/tty`, so the probe **prompts** on a controlling terminal. State what a prompt means for the operator and that declining is the act establishing N4 |
| A3 | `bootstrap/tests/test_gate_preflight.py` | an agent-held key must make the probe report **can sign**. Modelled with a disposable key added to a scratch agent, never the ceremony key |

**A1 is a design choice this plan must make, not defer.** Dropping the forward is
simpler and narrows the stage; keeping it and probing through the agent is closer
to what candidate code can reach. The reviewed plan names which, and why.

### Chunk B — the values schema and its parser ([R2], [R7])

| # | File | Change |
|---|------|--------|
| B1 | `bootstrap/reanchor-values.example` | the template, with every key from R7's table and a comment naming each value's security use |
| B2 | `bootstrap/reanchor.sh` | the parser: **no `source`, no `eval`, no command substitution, no shell expansion**. R7's lexical grammar exactly |
| B3 | same | every R7 refusal: unknown, duplicate, missing, malformed, relative, control character, wrong file type, missing executable bit, symlink at leaf **or any parent** |
| B4 | same | **no ambient fallback**: an absent field refuses. Never `PATH`, `HOME`, Git config, or any other ambient source |
| B5 | same | the `validate` subcommand prints the **complete effective non-secret configuration** |
| B6 | `bootstrap/tests/test_reanchor.py` | one node per refusal, each proving the refusal fires and nothing else runs |

### Chunk C — the artifact and its operator surface ([R3])

| # | File | Change |
|---|------|--------|
| C1 | `bootstrap/reanchor.sh` | `stage1`, `show-report`, `hash-package`, `stage2` alongside `validate` |
| C2 | same | `show-report` renders the package's range report in a **bounded, human-readable** form — the step that currently has no command at all |
| C3 | same | `hash-package` computes the digest the Maintainer confirms, over the bytes on disk |
| C4 | `bootstrap/tests/test_reanchor.py` | every subcommand exercised **through its public path**, not a helper |

### Chunk D — the packet, the launcher, and the binding ([R1], [R6], [R9], [R10])

| # | File | Change |
|---|------|--------|
| D1 | `bootstrap/reanchor.sh` | the packet schema: version, provenance, closure rows, artifact path, artifact digest — **and no candidate OID** |
| D2 | same | R10's closure constraints: the artifact path identifies **exactly one** closure row, and its separate digest **equals that row** |
| D3 | the launcher (M2-delivered; its reviewed text reproduced in the runbook) | opens the packet **bounded, regular, symlink-free**; reads **once**; hashes **before parsing**; compares against its **embedded** digest; parses only that buffer |
| D4 | same | resolves the candidate ref **once**, verifies every closure blob at that OID, **composes** the transient review manifest, extracts and hashes the artifact, then invokes `stage1` |
| D5 | `bootstrap/tests/test_reanchor.py` | a **mutated packet with a consistently rewritten row set** must refuse — the [R4-E1] attack, run rather than argued |
| D6 | same | a **marker interpreter** proves no candidate code starts on any packet or closure failure |

### Chunk E — the step registry and doc agreement ([R4])

| # | File | Change |
|---|------|--------|
| E1 | `bootstrap/reanchor.sh` | the closed, ordered registry: stable step ID, stage, command, inputs, security-relevant outcome |
| E2 | `bootstrap/tests/test_reanchor.py` | the runbook cites **every ID exactly once**, with **no unknown IDs**; every public command is exercised |

**What E does not claim**, restated here because the proposal withdrew a stronger
version: this is a drift signal on the procedure's *shape*. It attests nothing
about whether the surrounding explanation is accurate. That prose is reviewed.

### Chunk F — the runbook restructure

| # | File | Change |
|---|------|--------|
| F1 | `bootstrap/REANCHOR_RUNBOOK.md` | executable blocks replaced by: the reproduced launcher (marked **not the authority source**), the prerequisites, and what each step establishes |
| F2 | same | the rationale — FUR5–FUR10 and the review history — **kept**. It is what made four External passes effective |
| F3 | same | the two gaps the old runbook had: where the manifest comes from (the launcher), and how to read the report (`show-report`) |
| F4 | same | a prerequisites list: what the Maintainer must have before starting |

### Chunk G — the finding-tag cleanup ([R5] rider 4)

| # | File | Change |
|---|------|--------|
| G1 | repository-wide | bare `[FUR5]`, `[M2-1]`, `[S1]`-style tags in comments and docstrings replaced by the reason they stand for |
| G2 | — | **read, not swept.** Each site is judged: keep the reason, drop or gloss the label. A tag adjacent to load-bearing history keeps the history |

### Chunk H — the adopter-facing key guidance ([R8])

| # | File | Change |
|---|------|--------|
| H1 | `SECURITY.md` | the dedicated-ceremony-key requirement, and why a shared authentication key makes N4 fragile — with the 2026-08-13 evidence |
| H2 | same | what auto-loading (`AddKeysToAgent`, `UseKeychain`) does to the precondition |

## Acceptance criteria

1. **The Maintainer performs the ceremony from one command**, with no
   agent-authored script, no retyped digest, and no improvised reader.
2. **No candidate code starts** on any packet, closure, values, or artifact
   failure — proven by a marker interpreter, not by absence of a traceback.
3. **A consistently rewritten packet refuses**, because the launcher's embedded
   digest does not match.
4. **The artifact is a closure member by construction** — its path is exactly one
   closure row and its digest equals that row.
5. **The probe measures the channel candidate code has**, proven by an
   agent-held disposable key making it report *can sign*.
6. **The values parser never executes its input** and never falls back to an
   ambient value.
7. **Every public command is exercised through its public path**, and the runbook
   cites every step ID exactly once with none unknown.
8. **The ceremony key is dedicated**, encrypted at rest, auto-load disabled, and
   the old anchored roster authorized exactly one transition to install it.

* **Tests**: `bootstrap/tests/test_reanchor.py` and
  `bootstrap/tests/test_gate_preflight.py`, plus standing gates for every touched
  surface.
* **Public-path negative controls for every new command**: removing any one must
  fail a named test. Helper-level mutation does not satisfy this.
* **Known omissions at plan-open**: the three residuals named under *Scope*
  remain; `[TRU-7]` is closed and not revisited.

## Verification

* **Boundary A**, per chunk: that chunk's tests plus standing gates.
* **Boundary B**: one full suite on a clean commit under the canonical
  interpreter. **Bounded mode is refused** — trust-ceremony surfaces sit inside
  the `boundary-b-bounding-clause` Hard Refusal Fence, and this plan changes the
  ceremony itself.
* **Boundary C**: independent, and **not by the implementing agent**.
* Then **M2** on the exact bytes, then **M3**, then **M4**.

## Maintainer interventions

| | what | when | discharges by | must not |
|---|---|---|---|---|
| **N1** | **Dedicated key creation and all private-key handling** | before M3 | Creating an encrypted ceremony key used for nothing else, with auto-load disabled, and committing **only** the public half | Let any agent generate, move, encrypt, or load it. This is a fence, not a preference |
| **N2** | **M2 produces the launcher and packet** | after the M2 record commits | Delivering the paired launcher and OID-free packet out of band, with the launcher carrying the packet's digest as a literal | Put a candidate OID in either. Let the candidate repository carry them |
| **N3** | **The ceremony** — rollover and transition in one | after M2 | The old anchored roster authorizing the single transition that installs the new roster and the new closure | Let an agent run it, load the key, or move a Cairn ref |
| **N4** | **Publication** | after M3 | One atomic push of branch and anchor | Let an agent push. No two-push fallback |

**M3 is one ceremony, not two.** The roster is a closure member, so the
transition that blesses this plan's bytes is the same transition that installs
the new key. R8 specified this; it is restated here because splitting it would
cost a second ceremony and a second M2.

## Lasting-truth migration

*Filled in at archive time.*

## Plan review -- Claude (Internal, fresh-context) -- 2026-08-13

**Model**: Claude Opus 5
**Tier**: Internal
**Obligation**: this plan declares `Plan review: required(External Security
Review)`. **This pass does not discharge it.** An Internal same-agent-type read
is not structurally independent and carries no security mandate; the declared
External Security Review is still outstanding and must be obtained before
implementation begins. What this pass is for is narrower: catching the defects
an External Security reviewer should not have to spend its one pass on, so that
pass can be spent on the shell snapshot contract and the executable trust set —
the work the Revision 4 reviewer explicitly assigned to it.
**Reviewed commit**: `a1cdf86` (plan as opened)
**Target**: the whole plan against the Revision 4 contract (R1–R10 plus the R5
riders and every withdrawal ledger) in
`dev/proposals/archive/2026-08-13-claude-ceremony-as-code.md`, plus the plan's
own objective test and *Scope* fence
**Findings**: raised — 6 blocking, 7 substantive, 4 minor
**Disposition**: **REVISE before the External Security pass.**

### What is right

The chunking is legible and the orderings that *are* stated are the right ones
(A as the floor, B before C, F after C–E). Boundary B is correctly refused into
full mode with the right fence named. The *Scope* section declares the accepted
fence rather than assuming it, names three residuals as out of scope, and
correctly says no doctrine changes so the rate-limit gate does not apply. Chunk
E carries the "what E does not claim" paragraph, which is the withdrawal from
[E4] surviving into the plan — exactly the habit this family needed. R4, R9's
launcher sequence, and R10's two closure constraints have real homes.

The findings below are not about ambition. They are about the plan's own
recurring defect class, which four External passes found in the proposal and
which is present here in six new places: **a mechanism given a chunk but never
reached by the governing path, or a control asserted at intent rather than
sequenced into evidence.**

### Blocking

**[I1] The launcher is an M2 output, yet Chunks D and F build, test, and
reproduce it above the stable-bytes line — before M2 exists.**

Chunk D's rows D3 and D4 name the File as "the launcher (M2-delivered)". D5 and
D6 are tests of that launcher's refusals. F1 reproduces its text in the runbook.
All four sit above `--- stable bytes ---`; M2 sits below it. Acceptance criteria
1, 3, and the packet half of 2 are properties of the launcher.

So one of three things is true and the plan says which none of them: (a) the
implementing agent authors the launcher in-repo, which contradicts R1 and R6 and
reinstates exactly the candidate-controlled authority source [E1] blocked; (b)
Chunk D's tests exercise a stand-in launcher, in which case the tests pass while
the governing artifact is never reached — the defect class itself; or (c) Chunk
D cannot be implemented at all in its stated position.

F1 has the same problem in prose form: the runbook cannot reproduce launcher
text that will not be produced until two steps later, so what lands in F is a
guess, and nothing in the plan notices when M2's real launcher differs from it.

*Owed*: name the artifact bytes the implementing agent authors, where they live,
how M2 converts them into the out-of-band delivery, what D5/D6 actually execute,
and what checks the runbook's reproduction against the delivered launcher.

**[I2] `bootstrap/reanchor.sh` never joins the authority closure in any chunk.**

*Proposed paths* says it "joins the authority closure at M3". It does not. The
closure is a hard-coded list returned by `declared_authority_closure()` in
`bootstrap/tests/_gate_preflight.py:575` — itself a closure member. Membership is
a **code change in the candidate**, which must land before M2 reviews bytes; M3
blesses the new closure, it does not create it. No chunk touches that function.

The knock-ons are unowned too: the runbook's recorded checklist block goes from
nine rows to ten; `bootstrap/tests/test_gate_preflight.py`'s closure tests and
`_LOADED_MODULES` derivation move with it; the packet's closure rows (D1) and
R10's "exactly one closure row" constraint (D2) presuppose the tenth member
exists. Note also that `bootstrap/reanchor.sh` is **not** covered by
`_gate_manifest._frozen_files()`, whose globs are `bootstrap/*.py`,
`bootstrap/tests/**/*.py`, `scripts/*.py`, `templates/modules/**/*.py`
(`bootstrap/tests/_gate_manifest.py:347`) — so the artifact's freeze coverage is
a decision this plan owes, not an inherited default.

This is an accepted item carried unchanged from the opening contract (Revision
1's ledger: "the artifact's membership in the authority closure and the
transition ceremony that membership requires"). It is homeless.

**[I3] Chunk F deletes the fenced blocks a large body of existing tests
executes, and no chunk updates those tests — so R3's end-to-end contract has no
home and criterion 1 has no evidence producer.**

`bootstrap/tests/test_gate_preflight.py` lifts the runbook's Phase-0 blocks
verbatim and runs them: `_runbook_block`, `_runbook_ceremony_script`,
`_runbook_acquisition_command`, and the two recorded-ceremony transition nodes.
F1 replaces those blocks with prose and a reproduction. Chunk A is the only chunk
that touches that file, and only for the key probe.

Three consequences the plan does not address:

1. Chunk F as written breaks those tests. Nothing sequences their replacement.
2. The proposal's *Evidence / verification plan* said those tests "must be
   **extended, not replaced** — they currently execute the runbook's literal text
   and would otherwise have nothing to execute." No chunk extends them.
3. R3's end-to-end contract — start from only the M2 outputs and a valid values
   file, execute the exact launcher and the public stage commands, finish at the
   expected two-ref transaction — appears in **no chunk**. C4 exercises
   subcommands; D5/D6 are packet refusals; E2 is doc agreement. None of them is
   a two-stage transition in a disposable repository.

Relatedly, `_substitute()` ("Fill the Maintainer-recorded placeholders in a
recorded block") is precisely the helper R3 forbids: *"No test helper fills an
unrecorded placeholder — such a helper would rebuild the present defect inside
the test, which is how the current recorded ceremony passed while being
unusable."* The plan neither retires it nor says what stands in its place.

**[I4] A1 is not decided — and the rest of the plan has silently decided it
anyway, in a way that contradicts A1's own framing.**

The plan writes "**A1 is a design choice this plan must make, not defer**" and
then, one sentence later, "The reviewed plan names which, and why." That is the
deferral, wearing the decision's clothes. Nothing in the plan names which.

It is worse than a deferral, because two other rows have already picked a side.
A3 requires "an agent-held key must make the probe report **can sign**", and
acceptance criterion 5 repeats it. That holds only on the *keep the forward and
probe through the agent* branch. On the other branch — the ceremony stops
forwarding `SSH_AUTH_SOCK` to Stage 1 — an agent-held key is **not** reachable
by candidate code, the correct probe result is *cannot sign*, and A3 and
criterion 5 are wrong as written.

The second branch is also unimplementable inside Chunk A as tabled. The
forwarding lives in `bootstrap/REANCHOR_RUNBOOK.md` (the `SSH_AUTH_SOCK` rows at
lines 95, 218, 511 and 624), not in `_gate_preflight.py`; Chunk A's File column
names only `_gate_preflight.py` and `test_gate_preflight.py`. Chunk A is declared
the non-reorderable floor, so on that branch the floor cannot be met at A.

Finally, R5 rider 1's second half — "**and the runbook's claim to match whichever
is chosen**" — has no row in Chunk F.

**[I5] The one-command ceremony never prints the effective configuration.**

R2 and [E2] require the artifact to print the complete effective non-secret
configuration **before Stage 1**, "so the Maintainer sees what will be used while
it is still free to stop." The plan puts that printing only in `validate` (B5).
R9's governing path is: one Maintainer command → launcher → `stage1`. `validate`
is never invoked on that path. A control built, unit-tested, and unreachable
from the only route the ceremony actually takes — this is the family's signature
defect, reintroduced.

Either `stage1` prints the effective configuration itself, or the launcher
invokes `validate` before `stage1` and the plan says so. As written, the accepted
R2 obligation is not delivered.

**[I6] The Revision 4 reviewer's explicit plan-review constraint is unanswered.**

The SHIP review closed with a constraint addressed to *this* plan review:

> The plan must name the byte-preserving snapshot mechanism, prove that the
> hashed bytes are the parsed bytes under malformed/NUL/trailing-LF inputs, and
> add any executable used for snapshotting or hashing to the explicit host trust
> set.

D3 restates R10's prose ("reads **once**; hashes **before parsing**; … parses
only that buffer") and stops. No row names the snapshot mechanism — the reviewer
flagged this precisely because POSIX `$(…)` strips trailing newlines and cannot
carry NUL, so the obvious shell idiom does *not* satisfy R10. No test node covers
malformed, NUL-bearing, or trailing-LF packets. R7's executable table is not
extended for whatever the launcher uses to snapshot and hash.

This is the single item the declared External Security pass was told to falsify,
and the plan hands it back to that pass unanswered. Answering it here is the
highest-value revision in this review.

### Substantive

**[I7] N1's roster commit, as fenced, can invalidate M2.**

`dev/.cairn/allowed_signers` is a closure member
(`bootstrap/tests/_gate_preflight.py:594`). N1's *when* is "before M3" and its
*discharges by* includes "committing **only** the public half". M2 sits between
the stable-bytes line and M3, so "before M3" permits the roster commit to land
**after** M2's exact-byte review — which invalidates it under R6's invalidation
rule and under the parent plan's own M7 (`any byte changes after M2's exact-byte
review` → *"that disposition is **invalid**; M2 is re-taken"*,
`dev/plans/archive/git-native-security-foundations.md` M-table).

Two fixes are owed: tighten N1's *when* to "before Boundary B", and give the
roster edit and its closure-digest consequences a chunk. No chunk currently
touches `dev/.cairn/allowed_signers`.

**[I8] N1–N4 collide with the live fence numbering, and the plan's own Scope
line uses the old meaning against its own table.**

Across this lineage and the source proposal, **N4 is the key-channel
precondition before Stage 1** — `dev/plans/archive/ceremony-handshake-and-first-use.md:207`,
`dev/plans/archive/git-native-security-foundations.md:2262`,
`bootstrap/REANCHOR_RUNBOOK.md:495`, `dev/PLANNING.md:744`, and R3/R5/R8 of the
proposal ("The Maintainer still types the passphrase and makes the key available
at N4's boundary"). This plan redefines N4 as **Publication** and N1 as key
creation.

Then *Scope* says: "It also does not change N4's substance — the Maintainer's key
act remains human." That sentence is true of the **old** N4 and false of the
plan's own table, where N4 is a push. An External Security reviewer holding the
runbook in one hand and this plan in the other will read two different N4s at the
most safety-critical point in the document. Renumber this plan's fences, or adopt
the existing numbering and extend it.

Two further defects in that table:

* **N2 is not a Maintainer intervention.** "M2 produces the launcher and packet"
  is the External Security reviewer's act. As a row in *Maintainer interventions*
  it tells the Maintainer nothing to do and nothing to check, and it invites the
  Maintainer to produce the launcher — which would collapse the independence R1
  exists to create. State the Maintainer's actual act (obtain and retain the
  pair; verify the launcher digest through the M2 channel).
* **There is no fence for the values file.** Authoring `reanchor-values` with
  real, resolved host paths is a Maintainer act on the trust surface, and no row
  covers it.

**[I9] The plan obligation carried out of the [R3-E1] review has no chunk.**

Revision 3, *Plan obligation carried from this review*: *"The plan owes a
human-readable setup-and-refresh step for the values file that records resolved
paths and can be re-run after a toolchain upgrade."* The motivating fact is
concrete — the reviewed host path `/opt/homebrew/bin/git` is a symlink, its
resolved target embeds the Git version, and R7's no-symlink rule therefore makes
the entry go stale at every Homebrew upgrade.

B1 delivers a commented `.example` template. A template is not a setup-and-refresh
procedure, and nothing anywhere addresses re-running it after an upgrade. F4's
prerequisites list does not name it either. Homeless accepted obligation.

**[I10] Boundary A is a citation of the doctrine, not a reviewed mapping — and
for the plan's most security-critical artifact it is empty.**

`AGENTS.md` and `dev/plans/_template.md` both require Boundary A to be a
*reviewed mapping*: "for each changed invariant and public path, name the exact
affected test node/file and every standing non-pytest gate for the touched
surface." The plan says "that chunk's tests plus standing gates". No node names,
no gate commands, and no per-chunk mapping.

That is not merely a formality here. **There is no standing gate for
`bootstrap/reanchor.sh` at all**: `_gate_manifest._frozen_files()` globs only
Python (`bootstrap/tests/_gate_manifest.py:347`), `bootstrap/security_check.py`'s
Bandit gate scans Python, `scripts/quality_gate.py`'s three sub-gates
(order-independence, neutrality, redundancy) do not read shell, and the
repository has no shellcheck or any other shell linter. So a new executable
entering the authority closure is covered by exactly one thing — a test file this
plan also writes — and the plan never says so. Chunks F, G and H are prose and
name no claim/link/neutrality gate either, which `AGENTS.md` requires for
prose-only work.

Boundary C has the same shape: "independent, and not by the implementing agent"
restates the doctrine and names no falsification target.

**[I11] The `### Author-accounting — invariants, failure modes, edge cases`
subsection is missing, and it is the section that would have caught [I1]–[I6].**

The plan template gates that subsection on high-stakes changes; this plan is
declared high-assurance on a named high-risk surface, so it is required. Its
plan-stage satisfier is exactly the audit above: *"each invariant has an
enforcing test sequenced into a chunk, and each public entry point this plan
touches is mapped, in its acceptance criteria, to the test that exercises it
through its public path"*, plus re-answering S2 (which chunk runs the mutation)
and S3 (which gate command fires the check). None of that exists.

The *Acceptance criteria* block also drops two required lines: **Doc updates that
must land** (Chunks F, G and H are entirely documentation, and there is no
`CHANGELOG.md` row or explicit N/A) and **Examples / smoke checks** (the proposal
answered this with a reasoned N/A; the plan omits it). No test is cited as a
relative markdown link, so the link checker verifies none of them.

**[I12] Chunk E's doc-agreement test cannot pass until Chunk F lands.**

E2 asserts the runbook "cites **every ID exactly once**, with **no unknown
IDs**". The runbook cites no step IDs until F1–F4 restructure it, and the plan's
stated ordering is "F after C–E". Chunk E therefore commits red, which breaks the
per-chunk Boundary A discipline the plan asserts one section later. Either E2
moves into F, or F's runbook work splits so the citation surface exists when E
lands.

**[I13] Chunk G is scoped "repository-wide" with no append-only fence.**

The tags G targets — `[FUR5]`, `[M2-1]`, `[S1]` — occur thickly in
`dev/proposals/archive/` and `dev/plans/archive/`, which are **append-only
lifecycle records** (`AGENTS.md` > The lifecycle: "Never edit a prior section").
G2's "read, not swept" governs judgement, not blast radius. G needs an explicit
exclusion of the deliberation record, stated as a fence rather than assumed. Note
also that G edits `bootstrap/tests/_gate_preflight.py`, a closure member — the
stated ordering does put it before the stable-bytes line, which is correct, but
the plan should say why that ordering is load-bearing rather than incidental.

### Minor

**[I14] Criterion 2 is broader than the evidence D6 produces.** Criterion 2
covers "any packet, closure, **values, or artifact** failure"; D6's marker
interpreter covers "any packet **or closure** failure". Values and artifact
failures have no named evidence producer. Criterion 6's "the values parser
**never executes** its input" likewise has none: B6 is "one node per refusal",
and a refusal test does not establish non-execution. The node that would is a
positive canary — a values file carrying `$(…)` or backticks, asserted to leave
no marker.

**[I15] B1 reinstates a withdrawn key, and B3 drops half of R7's grammar.** B1
says "every key from R7's table". R7's table still lists `review_manifest`, which
R9 withdrew explicitly (*"`review_manifest` **leaves** the values-file
schema"*) — read literally, B1 puts a withdrawn authority input back into the
mutable file. B3's refusal list also omits R7's trailing-whitespace refusal, the
4096-byte line and 64 KiB file bounds, the UTF-8/LF encoding rule, the column-0
comment rule, and the `schema` version pin.

**[I16] Criterion 8 is not establishable by the implementation.** "Encrypted at
rest, auto-load disabled" are host-configuration facts no test reaches, and the
whole criterion only becomes true after N1 and M3 — i.e. after every verification
boundary this plan runs. It belongs as a Maintainer attestation with a named
record, not as an acceptance criterion the implementation can satisfy. Criterion
1 has the same shape in a milder form: it is the objective, and on the current
chunking nothing produces evidence for it (see [I3]).

**[I17] Label collision: `B1`.** It names both a *Sequence* step (the Boundary B
record) and a Chunk B row (`bootstrap/reanchor-values.example`). In a plan whose
Chunk G exists to remove labels that identify nothing, this one is worth
spending a character on.

### Scope check

Nothing in the chunks **exceeds** the accepted scope: every row traces to an
R-item, a rider, or a named documentation surface, and the three declared
residuals are not touched. The plan falls **short** in the places [I2], [I3],
[I6] and [I9] name — four accepted outcomes with no chunk. Against the plan's own
quoted objective test, the second half ("without any control being weaker than it
was before") is the one at risk: [I3] would retire executing end-to-end coverage
without replacing it, and [I5] would ship a Maintainer stop-point that the
one-command path never reaches.

### Coverage and confidence

**Covered**: R1–R10 and the four R5 riders enumerated against every chunk row;
the four withdrawal ledgers; the objective test and *Scope* fence; the sequence's
stated orderings; acceptance criteria 1–8 against their evidence producers; the
Boundary A/B/C mapping against `AGENTS.md` and `dev/plans/_template.md`; the
N1–N4 table against the live fence vocabulary; and the standing-gate surface for
a new shell artifact, read from `_gate_manifest._frozen_files()`,
`bootstrap/security_check.py` and `scripts/quality_gate.py`.

**Not covered / low confidence**: I ran no tests, moved no ref, loaded no key,
ran no ceremony, and pushed nothing. I did not attempt to design the shell
snapshot mechanism [I6] asks for, and I did not assess whether a POSIX artifact
can meet R7's grammar without an auxiliary utility — both belong to the External
Security pass. I did not re-litigate the three accepted residuals.

**Recommendation**: revise for [I1]–[I6] first — they are the ones that change
what the chunk tables *say*, and an External Security reviewer asked to read the
current text would spend its pass rediscovering them instead of falsifying the
snapshot contract it was explicitly assigned. **The required External Security
Review remains outstanding and is not discharged by this pass.**
