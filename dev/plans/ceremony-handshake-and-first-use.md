<!-- cairn-internal-ref-allow: doctrine/plans.md doctrine/dual-review.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->

# Plan: the reviewed-authority transition, and a real key boundary

**Source proposal**: `dev/proposals/archive/2026-08-12-claude-ceremony-handshake-and-first-use.md`,
accepted as revised at Round 2 (`## Decision -- Anthony Kendall (Maintainer) -- 2026-08-12`).
**Status**: awaiting-plan-review
**Plan review**: required(**External Security Review**) — set by the proposal.
An Internal read missed both defects this corrects, and an Internal read missed
[M2-1] in the parent plan. A same-agent-type reader is not the instrument for
"the mechanism exists but nothing calls it."
**Last update**: 2026-08-12
**Opened**: 2026-08-12

## Source proposal

Accepted terms are R1–R4 of the Round 2 revision. This plan maps them to files
and does not restate them; where this plan and the proposal disagree, the
proposal governs.

## Proposed paths

None. Every path below exists today.

## Scope

**In scope**: the reviewed-authority transition (R1, R2), the authorization
package (R3), the two-invocation protocol (R4), and the R1-F amendment.

**Explicitly out of scope**: OS containment for the evidence stage; a separate
evidence host; hardware-presence keys. All three are named strengthening paths
in the parent plan and none is built here. **This plan does not reduce the
accepted host-persistence residual** and must not be read as doing so.

**Inherited obligation.** The parent plan's `[M2-1]` fix landed at `2df83d2`
with a defect the proposal's review then found: `range_review_report` binds the
**worktree** manifest's digest (`bootstrap/tests/_gate_preflight.py:1007`) while
`apply` commits `authoritative_manifest(...)`. R3-c/R3-d close it; it is called
out here because it is **live in committed code** and would otherwise look like
new work rather than a correction.

**Candidate obligation from the Decision.** The scribe's note records that
`Scope delta: preserved` is arguable on outcome **A3**: R2-c/R3-c bind the
admitted set's digest where A3 wrote the set into the checkpoint message. The
Maintainer accepted unamended. **Chunk D decides it explicitly** rather than
letting it lapse — either the set is written alongside its digest, or the
narrowing is declared.

## Sequence

```
A  source selection: the transition extracts candidate bytes   [commit pending]
B  the reviewed-authority transition + roster continuity        [commit pending]
C  the authorization package, schema and validation             [commit pending]
D  the two-invocation protocol + key-channel preflight          [commit pending]
E  runbook rewrite + the R1-F amendment                         [commit pending]
--- stable bytes ---------------------------------------------------
B1 Boundary B on the stable pre-review commit                   [record]
SR External Security Review of the plan                         [before A]
M2 the parent plan's exact-byte retake, ONE only                [Maintainer]
H  the ceremony                                                 [Maintainer]
```

**Orderings that are load-bearing:**

* **The plan's External Security Review precedes Chunk A.** The proposal set the
  tier; building first would repeat exactly the mistake this plan corrects.
* **A before B.** Source selection decides which bytes execute; a transition
  mode built before that is a mode nothing can reach — finding **[S1]**.
* **C before D.** Stage 2 validates the package, so the package's schema must
  exist before the protocol that consumes it.
* **E last of the agent chunks.** The runbook records what the code does; writing
  it earlier records an intention.

**No chunk moves a Cairn ref, loads a key, or runs a ceremony.**

### Chunk A — source selection ([S1], R2)

| # | File | Change |
|---|------|--------|
| A1 | `bootstrap/REANCHOR_RUNBOOK.md` | a transition run extracts the **candidate commit's** exact closure bytes via sterile plumbing; steady-state runs extract from the anchor. The two modes are **explicit**, never inferred |
| A2 | same | the whole set is verified against the out-of-band review manifest **before Python starts** |
| A3 | `bootstrap/tests/_gate_preflight.py` | bind the exact candidate commit; refuse unresolved, symbolic, moving, partial, duplicate or extra-member sets |
| A4 | `bootstrap/tests/test_gate_preflight.py` | each refusal above, executed; and a test that the anchored checker **cannot** reach transition mode, which is the [S1] defect stated as a test |

### Chunk B — the reviewed-authority transition ([S3], R1)

| # | File | Change |
|---|------|--------|
| B1 | `bootstrap/tests/_gate_preflight.py` | the transition applies whenever the closure changes and **refuses with no delta**; it is not named "first use" anywhere |
| B2 | same | the review manifest has one named trust end: a Maintainer-recorded out-of-band artifact with a strict schema. **Never** read from the candidate; expected values **never** recomputed from it |
| B3 | same | the transition signature verifies against the roster **from the old anchor**. An old anchor with no roster is a distinct, named bootstrap case — never a fallback to the candidate's roster |
| B4 | `bootstrap/tests/test_gate_preflight.py` | fixtures start from the **old anchor's** authority bytes. `_ceremony_repo()`'s pre-aligned closure is what hid [M2-2] and is **not admissible** here |

### Chunk C — the authorization package ([S2], R3)

| # | File | Change |
|---|------|--------|
| C1 | `bootstrap/tests/_gate_preflight.py` | one closed, **versioned** package binding: observed anchor; candidate HEAD and tree; branch and expected-old; the complete canonical range report; the reviewed authority manifest and provenance; the candidate-only `collection`/`interpreter` evidence; the **exact prospective authoritative-manifest bytes and digest**; the package digest |
| C2 | same | stage 2 rejects unknown, missing and duplicate fields; re-derives every Git/static field; rebuilds the authoritative manifest and compares **exact bytes** |
| C3 | same | the accepted executable-only field list is **closed and asserted** — `collection` and `interpreter`, nothing else |
| C4 | same | **R3-d**: the range report's `manifest_sha256` becomes the **prospective** manifest's. This is the live defect in `2df83d2` |
| C5 | same | the checkpoint binds **both** the package/report digest **and** the exact prospective manifest digest |
| C6 | `bootstrap/tests/test_gate_preflight.py` | mutate **every package field and the schema itself**; stale refs and a substituted prospective manifest must move **neither ref** |
| C7 | `bootstrap/tests/_gate_preflight.py` | retract the "trusts no handoff artifact" claim in prose where it appears, and replace it with the narrower true one: no adjacent self-digest authenticates a file |

### Chunk D — two invocations and the key channel ([S4], R4)

| # | File | Change |
|---|------|--------|
| D1 | `bootstrap/tests/_gate_preflight.py` | stage 1: fixed clean environment, supported key channel **absent**, emits the package, prints marker and digest, exits |
| D2 | same | the contract **names the supported key channel** and defines a preflight proving stage 1 cannot sign through it |
| D3 | same | stage 2: separately hash-verified bytes, refuses every candidate-executing operation, validates the package, signs, verifies, expected-old transaction |
| D4 | same | **no boolean confirmation path survives** — `--confirm-supervised-reanchor` is removed, not deprecated |
| D5 | `bootstrap/tests/test_gate_preflight.py` | stage 1 **attempts a real signing operation and must fail**; stage 2 performs and verifies one. Observing an environment variable is the proxy failure the proposal warned about and then committed |
| D6 | this plan + `bootstrap/tests/_gate_preflight.py` | decide the **A3 durable-record question** from the Decision: write the admitted set alongside its digest, or declare the narrowing with a `Scope delta` |

### Chunk E — the runbook and the amendment (R4-e)

| # | File | Change |
|---|------|--------|
| E1 | `bootstrap/REANCHOR_RUNBOOK.md` | the two-stage ceremony as fixed manual commands, both stages, with the key-channel step explicit |
| E2 | same | literal-block tests, per the parent plan's F5 pattern |
| E3 | `dev/plans/git-native-security-foundations.md` | record that **R1-F step 5 is amended** to the two-invocation protocol, in the source proposal's own terms, openly rather than by reinterpretation |
| E4 | `SECURITY.md` | the key-channel contract and what it does **not** claim |

## Acceptance criteria

1. **The transition mode is reachable only by the route that verifies it.** The
   anchored checker cannot enter it; proven by test, not by argument.
2. **No transition without a delta**, and none without a whole-set match against
   the out-of-band manifest.
3. **The old anchor's roster verifies the transition signature**, with the
   no-roster case named separately.
4. **Stage 1 cannot sign.** Proven by attempting a real signing operation and
   requiring failure — not by reading an environment variable.
5. **Stage 2 executes no candidate code** and accepts only the closed
   executable-only field list.
6. **The checkpoint binds the prospective manifest**, not the worktree copy.
7. **Every package field and the schema are mutation-tested**, and a substituted
   prospective manifest moves neither ref.
8. **No boolean confirmation path exists** anywhere in the module.

* **Tests**: the two files named above plus standing gates for every touched
  surface. Ceremony suites stay exhaustive; the parent plan's fence off
  `corpus-tier-cost`'s memo pattern applies here too.
* **Public-path negative controls for every new call**, per [M2-1]: removing any
  one must fail a named test. Helper-level mutation does not satisfy this.
* **Known omissions at plan-open**: [TRU-7] stays unmeasured (M4 only); the
  host-persistence residual is unchanged and out of scope.

## Verification

* **Boundary A**, per chunk: that chunk's tests plus standing gates.
* **Boundary B**: one full suite on a clean commit under the canonical
  interpreter. **Bounded mode is refused** — trust-ceremony surfaces are inside
  the `boundary-b-bounding-clause` Hard Refusal Fence.
* **Boundary C**: independent, and **not by the implementing agent**.
* Then **one** M2 retake on the parent plan under M7, then H.

## Maintainer interventions

| # | Stop | What the Maintainer does |
|---|---|---|
| **N1** | Plan review, before Chunk A | Obtains the **External Security Review** the proposal requires |
| **N2** | The parent plan's M2 retake | One only, on the final bytes |
| **N3** | M3 / M4 — the ceremony | Unchanged from the parent plan; no agent performs any of it |

Everything else is agent work.
