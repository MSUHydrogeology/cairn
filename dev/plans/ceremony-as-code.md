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
