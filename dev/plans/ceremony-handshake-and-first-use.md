<!-- cairn-internal-ref-allow: doctrine/plans.md doctrine/dual-review.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->

# Plan: the reviewed-authority transition, and a real key boundary

**Source proposal**: `dev/proposals/archive/2026-08-12-claude-ceremony-handshake-and-first-use.md`,
accepted as revised at Round 2 (`## Decision -- Anthony Kendall (Maintainer) -- 2026-08-12`).
**Status**: review
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
SR External Security Review of the plan                         [DONE 4877ab9]
A  source selection: the transition extracts candidate bytes    [DONE 141bd09]
B  the reviewed-authority transition + roster continuity        [DONE 72b14b1]
C  the authorization package, schema and validation             [DONE 4816d0a]
D  the two-invocation protocol + key-channel preflight    [DONE a63da58 +
                                                            b7087c7 d055daa]
E  runbook rewrite + the R1-F amendment                         [DONE 95c2f47]
--- stable bytes ---------------------------------------------------
B1 Boundary B on the stable pre-review commit                   [record]
M2 the parent plan's exact-byte retake, ONE only  (obtained by) [Maintainer]
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

### Chunk A — source selection, in the loader ([S1], [E3], R2)

**[E3] moved this chunk's centre of gravity.** The predicate that decides *which
Python is safe to run* cannot live in that Python. `_gate_preflight.py` runs only
after the candidate bytes have been selected and executed, so a Python re-check
is defence in depth and **never the establishing control**.

| # | File | Change |
|---|------|--------|
| A1 | `bootstrap/REANCHOR_RUNBOOK.md` | the **complete source-selection predicate** lives in the fixed loader. A transition run extracts the **candidate commit's** closure; steady-state runs extract from the anchor; the two modes are **explicit**, never inferred |
| A2 | same | the review manifest has **one concrete, shell-parseable, bounded format**: schema/version, the **full candidate commit OID**, bounded review provenance, and the authority closure in one **fixed canonical path order** |
| A3 | same | the loader **rejects** malformed rows, wrong order, duplicates, missing or extra paths, control characters, non-lowercase or non-64-digit digests, and any member outside the declared set |
| A4 | same | it resolves the candidate **once** to a full commit OID, requires equality with the reviewed OID, and extracts every blob **by that OID — never by a moving ref**. Only after all extracted bytes match does Python start |
| A5 | `bootstrap/tests/_gate_preflight.py` | receives the same OID and manifest digest for **defence-in-depth revalidation**, explicitly documented as not the establishing control |
| A6 | `bootstrap/tests/test_gate_preflight.py` | **literal-block tests execute the transition loader from an old anchor whose checker lacks the new mode**, mutate each parser and set condition, and prove **no Python process starts** on failure. The "anchored checker cannot reach transition mode" node is kept and is explicitly **not sufficient alone** |

The fixed loader text remains an **M2 out-of-band trust input**; it cannot
bootstrap its own authenticity, and this plan does not claim it does.

### Chunk B — the reviewed-authority transition ([S3], R1)

| # | File | Change |
|---|------|--------|
| B1 | `bootstrap/tests/_gate_preflight.py` | the transition applies whenever the closure changes and **refuses with no delta**; it is not named "first use" anywhere |
| B2 | same | the review manifest has one named trust end: a Maintainer-recorded out-of-band artifact with a strict schema. **Never** read from the candidate; expected values **never** recomputed from it |
| B3 | same | the transition signature verifies against the roster **from the old anchor**. An old anchor with **no** roster is a **hard refusal** naming a route to a separately reviewed Maintainer bootstrap — not a second ceremony invented here ([E4]) |
| B3a | `bootstrap/tests/test_gate_preflight.py` | the no-roster case refuses, and **neither the candidate roster nor the out-of-band review manifest** is accepted as a fallback. A fail-closed edge; Cairn has an anchored roster today, so this is not work required for N3 |
| B4 | `bootstrap/tests/test_gate_preflight.py` | fixtures start from the **old anchor's** authority bytes. `_ceremony_repo()`'s pre-aligned closure is what hid [M2-2] and is **not admissible** here |

### Chunk C — the authorization package ([S2], [E2], R3)

**[E2] found the digest recursive.** C1 previously put the package digest
*inside* the package it digests. The digest is now **external**: SHA-256 over the
**exact file bytes stage 1 wrote**. A digest read from inside the package can
never satisfy confirmation — that is the adjacent-self-digest the proposal
already rejected, reappearing one layer down.

| # | File | Change |
|---|------|--------|
| C1 | `bootstrap/tests/_gate_preflight.py` | one closed, **versioned** package binding: observed anchor; candidate HEAD and tree; branch and expected-old; the complete canonical range report **and its digest**; the reviewed authority manifest and provenance; the candidate-only `collection`/`interpreter` evidence; and the **exact prospective authoritative-manifest bytes and digest**. **No self-digest field** |
| C2 | same | **stage 1 write contract**: create a new regular file **atomically and exclusively** with restrictive mode; refuse a symlinked parent or leaf and a pre-existing destination; close; print the external digest; exit |
| C3 | same | **stage 2 read contract**: explicit package path plus `--confirm-package-sha256 <digest>`; open **without following symlinks**; bound size; read **once** into memory; hash those bytes **before parsing**; use only that buffer thereafter |
| C4 | same | the strict JSON decoder rejects **duplicate keys** as well as unknown and missing ones |
| C5 | same | **canonical report bytes are defined separately** (sorted compact JSON); the report's `manifest_sha256` is the **prospective** manifest's — the live defect in `2df83d2` |
| C6 | same | the accepted executable-only field list is **closed and asserted** — `collection` and `interpreter`, nothing else |
| C7 | same | stage 2 re-derives every Git/static field, rebuilds the authoritative manifest, and compares **exact bytes** |
| C8 | same | the checkpoint binds the **external package digest**, the report digest, the prospective manifest digest, **and** the candidate tree |
| C9 | `bootstrap/tests/test_gate_preflight.py` | negatives through the **public stage-2 path**, neither ref moving: write/replace/symlink, duplicate keys, oversize, exact-byte mismatch, and an **adjacent self-digest** offered as confirmation |
| C10 | `bootstrap/tests/_gate_preflight.py` | retract the "trusts no handoff artifact" prose and replace it with the narrower true claim: no adjacent self-digest authenticates a file |

### Chunk D — two invocations and the named key channel ([S4], [E1], R4)

**[E1] is confirmed and it changes what code can promise.** Reproduced with a
disposable Ed25519 key (no ceremony key used): under `env -i`,
`HOME=/nonexistent` and **no `SSH_AUTH_SOCK`**, `ssh-keygen -Y sign -f key.pub`
**succeeded**, finding the private sibling next to the public key. This
checkout's `user.signingkey` has exactly that shape. So unsetting the agent
socket establishes nothing, and **acceptance criterion 4 is not achievable by
code alone**: nothing a program does can make a readable unencrypted private key
unavailable to another process running as the same user.

| # | File | Change |
|---|------|--------|
| D1 | this plan + `bootstrap/REANCHOR_RUNBOOK.md` | **N4, a Maintainer precondition/fence**: the ceremony private key is **encrypted at rest** and **not loaded into any agent** during stage 1. If the current key cannot meet this, **the ceremony stops before stage 1** |
| D2 | `bootstrap/tests/_gate_preflight.py` | stage 1 runs with **no agent socket** and performs a **fixed, non-interactive, timeout-bounded signing probe through the exact configured public-key path**, requiring **failure**. A passphrase prompt is **not** a refusal |
| D3 | same | stage 1 emits the package, prints marker and external digest, exits. It never holds the key |
| D4 | same | stage 2 starts from **separately hash-verified** bytes, refuses every candidate-executing operation, validates the package, signs, verifies, and performs the expected-old transaction |
| D5 | same | **no boolean confirmation path survives** — `--confirm-supervised-reanchor` is removed, not deprecated |
| D6 | `bootstrap/tests/test_gate_preflight.py` | a throwaway key modelling the exact channel: private key unavailable in stage 1, agent-only in stage 2. **Negative control**: make the private sibling readable and require stage 1 to **refuse the environment** rather than report the boundary sound |
| D7 | `bootstrap/tests/_gate_preflight.py` | the checkpoint message carries the **complete ordered `path -> SHA-256` admitted authority set** and the review-manifest digest ([E4]) |
| D8 | `bootstrap/tests/test_gate_preflight.py` | message **read-back** and **single-row mutation** tests, before any ref movement |

**Still sequencing, not containment.** Earlier candidate code may persist and
attack the later agent under the accepted residual. This plan does not claim
otherwise.

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
4. **Stage 1 cannot sign**, proven by a non-interactive timeout-bounded probe
   through the configured key path requiring failure — **on top of** the **N4**
   Maintainer precondition, without which no code can establish it.
5. **Stage 2 executes no candidate code** and accepts only the closed
   executable-only field list.
6. **The checkpoint binds the prospective manifest**, not the worktree copy, and
   carries the **complete admitted authority set** as ordered `path -> SHA-256`
   rows plus the review-manifest digest.
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
| **N2** | The parent plan's M2 retake | **Obtains** one only, on the final bytes; an independent reviewer performs it |
| **N3** | M3 / M4 — the ceremony | Unchanged from the parent plan; no agent performs any of it |
| **N4** | **Key-channel precondition, before stage 1** | Confirms the ceremony key is **encrypted at rest and in no agent**. [E1] proved code cannot establish this: a readable private sibling signs under `env -i` with no agent socket. If unmet, **the ceremony does not start** |

Everything else is agent work.

## Plan review -- Codex -- 2026-08-12

**Model**: GPT-5 Codex
**Tier**: External
**Obligation**: External Security Review
**Reviewed commit**: `e31abde3420aaf945829c99972dd2d90f1fb968d`
**Reviewed plan blob**: `f1fd273255b51d5aa4e5b6f2989f3a0cbac6b289`
**Target**: whether Chunks A-E form one executable security contract closing
proposal findings S1-S4 and parent findings M2-2/M2-3
**Prior findings**: S1, S2, S3, S4; inherited M2-2 and M2-3
**Assurance path**: high-assurance
**Findings**: raised
**Disposition**: REVISE

### Sharpening

**Scope delta**: preserved. Keep all accepted outcomes and the two-invocation
direction. The revisions below settle authority-transfer details the current
chunk rows defer; none removes or postpones an accepted outcome.

The plan maps the accepted two-invocation direction well, closes the live
prospective-manifest mismatch explicitly, and puts public-path negative controls
where the parent implementation lacked them. Four details remain open at the
exact points where authority crosses processes. They must be settled in the
plan before Chunk A; leaving them to implementation would repeat the failure
mode this plan exists to correct.

### [E1] BLOCKING -- the supported key channel is still unnamed and the current host defeats the implied one

D1-D2 say the supported channel will be named during implementation. That is the
security design, not an implementation detail. On this checkout,
`user.signingkey` names `/Users/kendal30/.ssh/cairn_signing.pub`, and a
same-user-readable private sibling exists. I reproduced the mechanism with a
throwaway key: under `env -i`, `HOME=/nonexistent`, and no `SSH_AUTH_SOCK`,
`ssh-keygen -Y sign -f testkey.pub` still succeeded by finding the adjacent
private key. No real ceremony key was invoked. Therefore removing the agent
socket and cleaning the environment does not establish acceptance criterion 4
on the host this ceremony will use.

**Required revision.** Name the supported operational channel now. The smallest
workable contract is: the ceremony private key is encrypted at rest and not
loaded into any agent during stage 1; stage 1 has no agent socket, performs a
fixed non-interactive signing probe through the exact configured public-key
path, and requires failure; only after package confirmation does the Maintainer
load or authorize that same key in a newly available agent channel for stage 2.
If the current key cannot meet that precondition, the ceremony stops before
stage 1. Record this as a Maintainer precondition/fence, because code cannot
make a readable unencrypted private key unavailable to another process running
as the same user.

D5 tests this with a throwaway key that models the exact channel -- private key
unavailable during stage 1, then agent-only during stage 2 -- and proves the
negative control by making the private sibling readable and observing stage 1
refuse the environment rather than report the boundary sound. The probe must be
non-interactive and timeout-bounded; a passphrase prompt is not a refusal.

This remains sequencing, not containment. Earlier candidate code may persist
and attack the later agent under the accepted residual. The revision need not
claim otherwise.

### [E2] BLOCKING -- the package has no exact byte, digest, or filesystem contract

C1 places the “package digest” inside the package it digests. Unless a field is
excluded, that is recursive; if it is excluded, the plan has not named the
canonical domain. More importantly, D1-D3 never specify how stage 1 writes the
artifact or how stage 2 receives the independently confirmed digest. A strict
field schema alone does not prevent a symlink target, partial write, replacement
between hash and parse, duplicate JSON keys, or stage 2 comparing the adjacent
self-digest that the proposal expressly rejected.

**Required revision.** Make the package digest external to the package:
SHA-256 over the exact file bytes stage 1 wrote. Stage 1 creates a new regular
file atomically/exclusively with restrictive mode, refuses symlinked parents or
leafs and a pre-existing destination, closes it, prints that digest, and exits.
Stage 2 takes an explicit package path plus
`--confirm-package-sha256 <digest>`; no digest read from the package can satisfy
confirmation. It opens without following symlinks, bounds size, reads once into
memory, hashes those bytes before parsing, and thereafter uses only that buffer.
The strict JSON decoder rejects duplicate keys as well as unknown/missing keys.

Define canonical report bytes separately (the existing sorted compact JSON is
reasonable), and make the package carry their digest plus the exact prospective
manifest bytes/digest. Stage 2 re-derives the report with the **prospective**
manifest digest, rebuilds the authoritative manifest, and compares exact bytes.
The checkpoint message binds the external package digest, report digest,
prospective manifest digest, and candidate tree. C6 gains write/replace/symlink,
duplicate-key, size, exact-byte and adjacent-self-digest negatives, all through
the public stage-2 path with neither ref moving.

### [E3] BLOCKING -- pre-Python source verification is divided across an unspecified loader and the code it is meant to authenticate

A1-A2 require whole-set verification before Python starts, but B2 leaves the
review-manifest schema unspecified and A3 assigns candidate binding and several
set refusals to `_gate_preflight.py`, which runs only **after** those candidate
bytes have been selected and executed. A Python re-check is useful defense in
depth; it cannot be the control that establishes which Python was safe to run.

**Required revision.** Put the complete source-selection predicate in the fixed
loader contract. The Maintainer-recorded review manifest must have one concrete,
shell-parseable, bounded format with a schema/version, the full candidate commit
OID, bounded review provenance, and the authority closure in one fixed canonical
path order. The loader rejects malformed rows, wrong order, duplicates,
missing/extra paths, control characters, non-lowercase/non-64-digit digests and
anything except the declared member set. It resolves the candidate once to a
full commit OID, requires equality with the reviewed OID, and extracts every
blob by that OID -- never by a moving ref. Only after all extracted bytes match
does it start the checker and pass the same OID and manifest digest for
defense-in-depth revalidation.

The fixed loader text itself remains an M2 out-of-band trust input; it cannot
bootstrap its own authenticity. E1/E2's literal-block tests must execute the
transition loader from an old anchor whose checker lacks the new mode, mutate
each parser/set condition, and prove no Python process starts on failure. A4's
current “anchored checker cannot reach transition mode” node is necessary but
does not cover these pre-execution failures by itself.

### [E4] BLOCKING -- D6 leaves an accepted outcome and the no-roster disposition to the implementer

The Maintainer accepted the Round-2 proposal unamended after the durable-record
question was surfaced. D6 nevertheless asks implementation to choose either
writing the admitted set or declaring a narrowing. An implementing agent cannot
authorize that scope reduction, and a `Scope delta` written after acceptance
would record the loss rather than authorize it.

**Required revision.** Preserve opening outcome A3: write the complete ordered
`path -> SHA-256` admitted authority set and its review-manifest digest in the
checkpoint message. Nine rows are a reasonable audit cost for the trust root;
the digest supplies compact binding and the rows make the record independently
readable. Replace D6's branch with that decision and add message read-back plus
single-row mutation tests before any ref movement.

B3 also names an old-anchor-with-no-roster case without giving it behavior or a
test. This plan need not invent a second bootstrap ceremony: specify a hard
refusal with a named route to a separately reviewed Maintainer bootstrap, and
test that neither the candidate roster nor the out-of-band review manifest is
accepted as a fallback. Current Cairn has an anchored roster, so this is a
fail-closed edge, not work required for N3.

### Mapping and verification

Acceptance criteria 1, 2, 5, 6, 7 and 8 have direct chunk homes. Criteria 3 and
4 become executable once E4 and E1 are applied. The full Boundary B reading is
correct: both the trust-ceremony and manifest surfaces hit the hard refusal
fence, so bounded mode is unavailable. No implementation chunk authorizes a
real Cairn-ref move or real ceremony-key load; fixture transactions and
throwaway signing remain ordinary tests.

Move `SR` before A in the sequence diagram so its displayed order agrees with
the binding ordering paragraph. In N2, say the Maintainer **obtains** the M2
retake; the independent reviewer performs it. Those are record corrections,
not additional findings.

### Verification and bounds

`claim_check.py` reports no flags and `lifecycle_planner.py next` reports the
unreviewed plan structurally sound. I verified the Boundary B hard-refusal text,
mapped every acceptance criterion to its chunk, inspected the current Git
signing configuration and key-path shape, and executed the no-agent signing
probe with a disposable Ed25519 key; it succeeded, reproducing E1's mechanism.

I did not use the real ceremony key, move a Cairn ref, run a ceremony, modify
implementation bytes, or run the full suite. The latter is an implementation
Boundary B obligation, not evidence for a pre-implementation plan review.

## Response to the plan review -- Claude -- 2026-08-12

**All four findings accepted. None disputed.** The disposition is right: every
one sits exactly where authority crosses a process boundary, which is the part I
deferred to implementation and should not have.

| finding | disposition |
|---|---|
| **[E1]** | **Accepted.** Reproduced independently. Chunk D rewritten; **N4** added as a Maintainer fence |
| **[E2]** | **Accepted.** Chunk C rewritten around an **external** digest and a filesystem contract |
| **[E3]** | **Accepted.** Chunk A's predicate moved into the **loader**; the Python check is demoted to defence in depth |
| **[E4]** | **Accepted.** D6's branch **deleted**; outcome A3 is preserved outright, and B3's no-roster case gets behaviour and a test |

**Scope delta**: **preserved**, and now more defensibly than before — [E4]
removed the one branch that could have degraded an accepted outcome.

### [E1] — I reproduced it, and it invalidates something I wrote

With a disposable Ed25519 key and **no ceremony key involved**: under `env -i`,
`HOME=/nonexistent`, and no `SSH_AUTH_SOCK`, `ssh-keygen -Y sign -f <pub>`
**succeeded**, finding the private sibling beside the public key. Exit 0,
signature written.

So proposal item **B1** — "the candidate stage runs with the signing key channel
absent (`SSH_AUTH_SOCK` unset)" — describes a boundary that **does not exist on
this host**, and acceptance criterion 4 was unachievable as I wrote it. The
reviewer's framing is the correct one: **code cannot make a readable unencrypted
private key unavailable to another process running as the same user.** The
boundary has to be a Maintainer precondition (**N4**) that code *probes*, never
one code *establishes*.

This is the second time in this plan family I have written an environment-variable
check as though it were a property. [S4] warned me in those words — *"observing an
environment variable alone is the proxy failure the proposal warns against"* — and
the revision I wrote in response still carried it.

### [E2] — the digest was recursive, and I did not see it

C1 placed the package digest inside the package it digests. Either it is excluded
and the canonical domain was never named, or it is included and the definition is
circular. Now external: SHA-256 over the exact bytes stage 1 wrote, with a
filesystem contract (atomic exclusive create, symlink refusal, hash-before-parse,
duplicate-key rejection) and an explicit negative for an **adjacent self-digest
offered as confirmation** — the very thing the proposal rejected, reappearing one
layer down where I did not look for it.

### [E3] — the establishing control cannot live in the thing it authenticates

A3 assigned candidate binding and set refusals to `_gate_preflight.py`, which
runs *after* those bytes are chosen and executed. The complete predicate now
lives in the loader contract, with a bounded shell-parseable manifest format and
extraction **by resolved OID, never by a moving ref**; the Python check is kept
and explicitly labelled defence in depth. A6 requires the literal-block tests to
run the transition loader from an old anchor whose checker lacks the mode, and to
prove **no Python process starts** on failure.

### [E4] — an implementing agent cannot authorize a scope reduction

D6 offered implementation a choice between preserving outcome A3 and declaring a
narrowing. That was wrong on its face: the Maintainer accepted the Round-2
proposal *unamended after the question was surfaced*, and a `Scope delta` written
afterwards records a loss rather than authorizing one. The branch is deleted. The
checkpoint carries the **complete ordered `path -> SHA-256` admitted set** plus
the review-manifest digest, with read-back and single-row mutation tests.

I raised this concern myself before the Decision and then wrote a chunk that
would have let it be resolved by whoever happened to implement it. Surfacing a
scope question does not discharge it.

### Record corrections applied

`SR` now precedes `A` in the sequence block, matching the binding ordering
paragraph; **N2** says the Maintainer *obtains* the M2 retake, which an
independent reviewer performs.

### What this pass did not cover

The reviewer did not run the full suite, and says so: that is an implementation
Boundary B obligation, not evidence for a pre-implementation plan review. No real
key was used, no Cairn ref moved, no ceremony run, nothing pushed — by the
reviewer or by me. My own reproduction of [E1] used a disposable key in a
throwaway directory, since deleted.

**Status → ready-to-implement**, with **N4** standing before any stage-1 work.

## Implementation verification -- Claude -- 2026-08-12

**Boundary B mode**: **full**. Bounded mode is refused: this change touches
trust-ceremony surfaces, which sit inside the `boundary-b-bounding-clause` Hard
Refusal Fence. No bounding argument was attempted.

**Tested SHA**: `a4a3b24` (range `4877ab9..a4a3b24`).
**Interpreter**: `/Users/kendal30/conda_envs/lhm/bin/python3.13` — 3.13.13
(conda-forge, Clang 19.1.7).
**Tree state**: a fresh `git clone --shared` checked out at `a4a3b24`;
`git status --porcelain` empty before the run and after it. The main working
tree was not used, because other sessions hold uncommitted edits to frozen gate
files there.

### Commands and outcomes

| # | Command | Outcome |
|---|---------|---------|
| 1 | `python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0` | **3987 passed, 4 failed, 1 skipped** in 475.22s (7m55s) |
| 2 | `python scripts/quality_gate.py --sub neutrality --sub redundancy` | **93 neutrality FAIL, redundancy fail=0** (info=2) |

### Non-pass disposition — all four failures attributed

Each was reproduced at **`a63da58`**, the commit *before* this range's Chunk D
part 2, in a separate clean clone. None is introduced here.

| Node | Cause | Evidence |
|------|-------|----------|
| `test_gate_preflight.py::TestPublicCli::test_check_runs_against_the_live_repo_and_reports` | **Clone artifact.** A `git clone --shared` carries no `refs/cairn/gate-anchor`, so the CLI refuses with *"ref does not resolve to a commit"* instead of reaching the first-use bootstrap message | Fails in the clone at both `a63da58` and `a4a3b24`; **passes in the main working tree** |
| `test_security_check.py::test_detached_checkout_excludes_an_ignored_pytest_override` | **Pre-existing.** The detached checkout comparison counts `bootstrap/tests/__pycache__/*.pyc` written during the session as `extra` paths | Fails at `a63da58` and in the main tree; **passes under `PYTHONDONTWRITEBYTECODE=1`** |
| `test_lifecycle_vocabulary.py::TestLoaderContainmentMatrix::…[metrics_extract]` | **Pre-existing**, same cause: importing the planner writes `tools/__pycache__/lifecycle_planner.cpython-313.pyc`, which the node reads as *"loading the planner mutated the working tree"* | as above |
| `…[transition_lint]` | **Pre-existing**, same cause | as above |

The three `__pycache__` nodes are one defect, not three: two tests assert
"no working-tree mutation" over a comparison that bytecode writes satisfy, so
the result depends on whether the host writes `.pyc` files. Verified precisely:
in a clean clone at `a4a3b24`, `PYTHONDONTWRITEBYTECODE=1` turns all of them
green (**17 passed**). It is outside this plan's surfaces and is left as found,
flagged rather than fixed.

**Quality gate.** The 93 neutrality FAILs are **byte-identical in set** to the
93 at `a63da58` (`diff` of the sorted FAIL lines is empty), and **not one names
a path this range touched** — all are in `templates/`, a pre-existing condition
recorded elsewhere. `redundancy` is clean.

### Known omissions

* **[TRU-7]** remains unmeasured; it is M4-only and out of scope here.
* The **host-persistence residual** is unchanged and explicitly not closed —
  the two-stage split is sequencing, not containment.
* **N4 cannot be established by code.** [E1] is reproducible, so stage 1's probe
  reports the key channel and does not close it. Every test that models N4 does
  so by genuinely withholding the private half (`_n4_precondition`), which is a
  fixture standing in for a Maintainer act, not a proof that the act happened.
* `test_gate_manifest.py` HOLDs whenever frozen gate files carry uncommitted
  edits. It passed in this run because the clone was clean at a commit.

### Standing claims re-checked at the end of the range

* **No Cairn ref moved.** `refs/cairn/gate-anchor` is still
  `e45e1fcc84ded159ef910b6e7bde15f7b715a5b3`, file mtime **2026-08-03 16:47** —
  before the parent plan opened. `.git/logs/refs/cairn/` does not exist.
* **No ceremony key was loaded**, and no ceremony was run. Every ceremony in the
  test suite uses a disposable per-fixture keypair.
* **Nothing was pushed.**

**Boundary C is owed** — independent, and not by the implementing agent.

## Code review -- Claude (Boundary C) -- 2026-08-12

**Model**: Claude Opus 5
**Tier**: Internal
**Reviewed commit**: `a4a3b24`, in a detached `git clone --shared`. Range
`4877ab9..a4a3b24`, plus `f2adcd9`, which added the Boundary B record.
**Target**: whether Chunks A–E deliver the eight acceptance criteria as
executable controls on the governing path, and whether the Boundary B record
holds against the reviewed range.
**Prior findings**: [E1]–[E4] from `## Plan review -- Codex -- 2026-08-12`, all
accepted in the author's response; the inherited [M2-1] / [M2-2] shapes from
`dev/plans/git-native-security-foundations.md`; and the three unreachability
defects this range corrected internally.
**Assurance path**: high-assurance
**Interpreter**: `/Users/kendal30/conda_envs/lhm/bin/python3.13` — 3.13.13.
**Working tree**: a `git clone --shared` at `a4a3b24`, `git status --porcelain`
empty before and after every probe. The main tree was used read-only, and only
to confirm two of the Boundary B record's own claims.
**Bounding**: not applicable — Boundary B ran `full`.
**Findings**: raised

**Verdict**: REVISE

Two findings block. Both are the shape this plan family keeps producing — a
control that is computed, compared, and then not the thing that governs — and
both were found by executing a recorded transition ceremony end to end, not by
reading. Everything the briefing asked me to attack hardest (the relaxed
CLOSURE/AUTHORITY admission, the `_sha256_hex` split, the stage-2 report
comparison, `_entry_base`) I could not break; the record below says so
explicitly, because a review that reports only what it found does not tell the
Maintainer what it cleared.

**Scope note.** `4877ab9..a4a3b24` interleaves six `scope-reduction-trap`
commits (`8fd0aa5`, `8100256`, `74e9055`, `2718e55`, `bbc6584`, `3c3f24f`) and
their files. Those carry their own Internal and External code reviews in
`dev/plans/scope-reduction-trap.md`; I filtered them out and did not re-review
them.

### [C1] BLOCKING — the signed admitted-authority record is taken from the package, not from the set stage 2 revalidated

`apply_now` revalidates the review manifest itself and passes the result to the
checks — `admitted_authority=transition["members"]`
(`bootstrap/tests/_gate_preflight.py:2731`). It then builds the checkpoint
message from a **different** source: the package's own copy,
`(pkg.get("review_manifest") or {}).get("members")` and `.get("provenance")`
(`bootstrap/tests/_gate_preflight.py:2779-2784`). `read_package` validates only
the package's top-level field set (`:2204-2213`); the `review_manifest` inner
dict is consumed unvalidated. Only its `digest` sub-field is cross-checked
against the file (`:2707`).

So enforcement is honest and the **record is not**. The durable rows the D7 /
[E4] outcome exists to produce are whatever the package says they are.

I drove the real two-stage transition ceremony four times, re-digesting the
package each time so `--confirm-package-sha256` matched the tampered bytes — the
case the digest cannot help with, and the one the plan's own criterion-7 node
already models:

* **Falsified rows.** Replacing every member digest with `9…9` left all checks
  passing and signed a checkpoint whose nine `path -> SHA-256` rows are all
  false. `parse_admitted_authority` reads them back cleanly.
* **Dropped `members`.** Removing the key makes `.get("members")` return `None`,
  and `_admitted_rows` (`:1786-1787`) then renders `_ADMITTED_NONE`. A real
  transition that changed `bootstrap/tests/_oracle.py` signed
  `admitted authority  : (steady state -- no closure change)`, signature `G`,
  and the anchor advanced. That is verbatim the failure the comment at
  `:2718-2728` says stage 2 prevents — *"the admitted set would be absent from
  the durable record while the ref moved anyway, which is the [E4] failure with
  a signature on top"* — reached through the inner dict instead of through the
  missing flag.
* **Non-dict `members`.** A list raises an uncaught `AttributeError: 'list'
  object has no attribute 'items'` out of `_admitted_rows`. It fails closed, but
  `main`'s `except PreflightError` does not catch it, so the CLI prints a
  traceback instead of `[REFUSE ]`.
* **A newline inside a member path.** The path text is interpolated into the
  message unescaped and forges an extra row. The ceremony completes and moves
  both refs; `parse_admitted_authority` then refuses the committed checkpoint —
  *"the checkpoint declares 10 admitted members and carries 11 rows"*. The
  signed record is unreadable by its own reader, and nothing in the ceremony
  ever tries to read it back before signing.

The reachability premise is the accepted residual, not a new one: the runbook
and `SECURITY.md` both state that candidate code ran in stage 1 as the same user
and *"may have left persistence neither stage can see"*. Rewriting the package
file before the Maintainer's `shasum` is exactly that. The design's answer —
*"there is no authority-bearing file"*, `apply_now`'s own docstring — holds for
every other field and not for this one.

Note also that `check_authority_closure`'s docstring currently claims the
admitted set *"is written into the checkpoint message (D7) rather than merely
consulted"* (`:653-654`). With C1 open that sentence is false: the set that was
consulted and the set that was written are different objects.

**Direction (not a fix — yours to choose).** `transition["members"]` and
`transition["provenance"]` are already in hand at that call site and have passed
`revalidate_transition`. Using them closes it outright. Whatever is chosen, the
package's inner dict needs a strict shape check, and the ceremony should read
its own drafted message back through `parse_admitted_authority` before signing —
`verify_message_binds_report` already establishes that pattern for the report
digest.

**Why nothing caught it.** `test_every_package_field_is_mutation_tested_through_stage_2`
runs stage 1 in **steady state** (`bootstrap/tests/test_gate_preflight.py:3008`),
so `honest["review_manifest"]` is `None` and the mutation only exercises the
`None -> dict` direction, which the separate steady-state/transition disagreement
check already refuses. The one field that is a nested object, and the only one
that feeds the durable record, is never mutated in the mode where it is live. So
acceptance criterion 7 — *"every package field and the schema are
mutation-tested"* — is met in form and not in substance.

### [C2] BLOCKING — the recorded transition stage 2 runs the ANCHORED checker, so a closure-membership transition cannot complete

`bootstrap/REANCHOR_RUNBOOK.md:180` states the reason transition mode exists:

> the anchored checker cannot contain a mode added to its successor. Extracting
> from the anchor to run a transition is asking the old authority to vouch for
> its replacement, which is the property this whole ceremony exists to deny.

The recorded stage-2 block extracts from the anchor —
`cat-file blob "refs/cairn/gate-anchor:$path"` (`:475`) — and *"Stage 2 in
transition mode"* (`:511`) replaces **only the final command**, adding the two
flags. It changes neither the extraction source nor the checklist. A transition
therefore runs stage 1 on the reviewed candidate's checker and stage 2 on the
anchored one.

Executed, with a candidate that adds one member to its own
`declared_authority_closure()` — the runbook's own motivating case — both blocks
lifted from the document exactly as the suite lifts them:

* stage 1: `rc=0`, package written, no ref moved;
* stage 2: `rc=2`, `REFUSE: the review manifest is not the authority closure:
  0 missing [], 1 unexpected ['bootstrap/tests/_extra_authority.py']`.

`revalidate_transition` compares the manifest's member set against the
**executing** checker's `declared_authority_closure()` (`:946-953`), and the
executing checker at stage 2 is the old one. It fails closed and no ref moves —
but the stop lands after the Maintainer has loaded the ceremony key, which is
precisely the position `test_the_recorded_transition_stage2_carries_both_flags`
was written to prevent (*"a hard stop mid-ceremony with the key already
loaded"*). The same applies to any transition that changes the checker's CLI:
the currently anchored checker at `e45e1fc` has no `stage2` subcommand at all.

**Why nothing caught it.** `test_the_recorded_transition_ceremony_runs_end_to_end`
passes because `_ceremony_repo` copies the live repository's closure files into
the fixture *and* anchors them, then mutates only `bootstrap/tests/_oracle.py`.
The anchored and candidate checkers are byte-identical, so the fixture never
constructs the one state a transition is defined by. That is the [M2-2] shape —
a pre-aligned fixture through which the route under test never runs.

**Direction.** Either the recorded transition stage 2 extracts by the same
`RESOLVED` OID its stage 1 did (and the runbook says why that is safe), or the
plan states explicitly that transition mode is limited to member-**byte** changes
within a fixed closure and `revalidate_transition` says so in its refusal. The
first matches the runbook's stated argument; the second contradicts it and would
need the Maintainer's call. Either way the end-to-end node needs a fixture whose
anchored checker differs from its candidate.

### [C3] The Boundary B record's neutrality gloss is false as written

The record says the 93 neutrality FAILs are *"all in `templates/`"*. Reproduced
at `a4a3b24`: 65 are in `templates/`, 14 in `docs/`, 9 in `doctrine/`, and 5 in
`bootstrap/tests/fixtures/skills/README.md`.

The load-bearing half is true and I verified it independently: the FAIL set is
**byte-identical** to the set at `a63da58` (93 lines, `diff` empty), and the
intersection of the 31 distinct FAIL files with the 16 files this range touched
is **empty**. So the disposition stands; the sentence offered as its reason does
not, and a reader relying on it would conclude no `doctrine/` or `bootstrap/`
path is implicated when 14 are.

### [C4] The two implementations of the review-manifest predicate disagree on a `provenance` row with leading whitespace

`parse_review_manifest` exists, by its own docstring, so that *"a second,
independent implementation of the same predicate catches a loader that was
edited to be laxer than its recorded text"*. On the row
`"  provenance   external review 2026-08-12"` the two implementations both
accept and produce different values: the Python side computes
`raw[len("provenance "):]` (`:869`) and yields
`'e   external review 2026-08-12'`; the recorded loader's `${line#provenance }`
does not match the prefix and yields the whole line unchanged. Silently
mangled rather than refused, and the mangled value is what reaches the signed
checkpoint's admitted-authority header. Low impact — the manifest is a recorded
Maintainer artifact and its digest is bound — but a second implementation that
disagrees quietly is worse than a comment saying "re-check this by hand".

### [C5] `probe_cannot_sign` is fail-open on `ssh-keygen` exit 0 without a `.sig`

`_gate_preflight.py:2051-2054` returns "can sign" only when the exit status is 0
**and** the signature file exists; every other combination returns "cannot
sign". An `ssh-keygen` that exits 0 having written the signature elsewhere would
be reported as an intact key boundary. The direction is wrong for a probe of
acceptance criterion 4: a successful signing exit should be conclusive on its
own. No test covers the combination.

### Observation, not a finding — criterion 8's scope

*"No boolean confirmation path exists anywhere in the module"* is met, and the
AST node asserts it on `bootstrap/tests/_gate_preflight.py`. `_gate_reanchor.py`
still exposes `--confirm-supervised-reanchor`, and `REANCHOR_RUNBOOK.md:703`
still records it as the supervised CAS that advances `refs/cairn/gate-anchor` in
Phase 4. That is a different mechanism and outside this plan, but criterion 8
should not be read as a repository-wide property.

### Falsification ledger — what I attacked and could not break

Each of these was probed by execution, not by reading.

| Target | Probe | Result |
|---|---|---|
| The relaxed CLOSURE admission | Enumerated every call site of `admitted_authority`; both stage entry points revalidate **before** `check`, and `main`'s `check` subcommand passes `None`. `revalidate_transition` pins `reviewed_candidate == HEAD`, `manifest["candidate"] == reviewed_candidate`, `named == declared` exactly, and every member's digest against the candidate's own blob — so an admission means "the live bytes are the reviewed candidate's bytes at that path" | **Narrow as claimed** |
| `_sha256_hex` vs `_sha256_bytes` | Enumerated all 22 digest sites in the module. Both admission comparisons (`:678-683`, `:1318`) are bare-hex on both sides; every prefixed comparison is prefixed on both sides. `read_review_manifest` returns the prefixed form and is only ever compared against the package's copy of itself | **No crossing remains** |
| Stage 2's report comparison | Both halves are checked (`:2815-2825`): the package must hash to the digest it states, and that digest must equal stage 2's own re-derivation. Digest equality over canonical `sort_keys`/`ensure_ascii` JSON implies report equality, and `read_package` rejects duplicate keys | **Binds read-to-signed** |
| `_entry_base` / `authoritative_manifest` | Ran a real steady-state ceremony from the runbook's own two blocks and read the committed manifest **out of the checkpoint commit**, not by re-calling the function. Every `frozen_files` entry carries `sha256` **and** `mode` **and** `oid`; the worktree copy equals the committed blob byte-for-byte | **v1-scalar fix is real** |
| "What calls this?" for every new symbol | Replaced each of 14 new/changed functions with a raiser and drove a real two-stage **transition** ceremony. 12 refused and moved no ref. `signing_key_path` is unreached only because the harness stubs `require_stage1_cannot_sign`; `parse_admitted_authority` is a reader with its own named node | **Reachability holds** |
| `--confirm-supervised-reanchor` / single-stage `apply` | Gone from `_gate_preflight.py` by AST and by argparse; `apply_now`'s signature carries no boolean | **Removed, not hidden** |

### Verification of the Boundary B record

| Claim | Result |
|---|---|
| Interpreter 3.13.13 | Confirmed |
| Clean clone, `git status --porcelain` empty | Confirmed |
| `3987 passed, 4 failed, 1 skipped` | `--collect-only` reports **3992** collected at `a4a3b24`, which is exactly `3987 + 4 + 1` |
| The four non-passes | All four reproduced node-for-node in a clean clone |
| One is a clone artifact | Confirmed: `test_check_runs_against_the_live_repo_and_reports` **passes in the main working tree** |
| Three are one `__pycache__` defect | Confirmed: `PYTHONDONTWRITEBYTECODE=1` gives **17 passed**, the record's own figure |
| Neutrality 93 / redundancy 0 | Confirmed |
| The 93 are set-identical to `a63da58` | Confirmed — `diff` of the sorted FAIL lines is empty |
| "all are in `templates/`" | **False** — see [C3] |
| No Cairn ref moved | Confirmed: `refs/cairn/gate-anchor` = `e45e1fc…`, file mtime 2026-08-03 16:47; `.git/logs/refs/cairn/` does not exist; the only other Cairn ref, `refs/cairn/release-bar-audit`, has mtime 2026-08-10, before this range |

**Omissions the record does not name.** One: the range contains another plan's
commits and files (the scope-reduction-trap set above), which the record's
"tested SHA / range" line does not distinguish. Not a defect in the
verification — a full suite covers both — but the record reads as though the
range were this plan's work alone.

### What this pass did not do

No Cairn ref was moved, no ceremony key was loaded, no real ceremony was run,
nothing was pushed, and no implementation byte was changed. Every probe ran in a
disposable `git clone --shared` against per-fixture throwaway keypairs; the
probe files were kept outside the repository tree and are not part of this
commit. I did not re-run the full Boundary B suite: the bytes are unchanged, the
record's evidence reproduced exactly where I challenged it, and `AGENTS.md`
reserves a fresh full run for missing or stale evidence — which this is not. I
did not review the interleaved `scope-reduction-trap` work.

## Response to code review -- Claude -- 2026-08-12

**Disposition: all five findings accepted. None disputed.** Both blocking
findings were reproduced before being fixed, and each fix was mutation-checked
by reverting it and confirming the new nodes fail.

### [C1] — the signed record came from the package, not the revalidated set

**Accepted, and it is the worst defect in the range.** `apply_now` handed
`transition["members"]` to the checks and `pkg["review_manifest"]["members"]` to
the message, so enforcement was honest while the **durable record was whatever
the package said** — and `read_package` validated only the top-level field set,
leaving the inner dict entirely unchecked.

What this failed at is the plan's own [E4]/D7 outcome: the checkpoint exists to
say *which bytes* an external review admitted. A record that a tampered package
can write says nothing.

Four changes, in the order they matter:

1. **The message is built from `transition`** — the set that passed
   `revalidate_transition` (whole-closure match, every member's digest checked
   against the candidate's own blob). It was already in hand at the call site.
2. **Stage 1 and stage 2 must agree.** `members`, `provenance` and `candidate`
   in the package are compared against the revalidated values and a mismatch
   **refuses**. Overriding silently would have been enough to make the record
   correct; refusing also tells an operator their package is tampered or stale.
3. **`read_package` validates the inner dict**: field set, member digests as 64
   lowercase hex, string types, and **control characters in paths and values** —
   the newline that forged a row.
4. **`draft_message` round-trips its own output** before returning: if
   `parse_admitted_authority` does not recover exactly the set that went in, it
   refuses. That closes the framing class at the writer, at the last moment
   before a signature exists — after which the checkpoint is signed, verified,
   anchored, and unreadable.

**Why the existing mutation node missed it, which is the more useful finding.**
Criterion 7's parametrized test runs stage 1 in **steady state**, so
`review_manifest` is `None` and only the `None -> dict` direction was exercised.
Every field *inside* the dict went unmutated. `_transition_ready` now produces a
real transition-mode package and
`test_the_admitted_set_inside_the_package_cannot_forge_the_record` replays the
reviewer's own five tampers with the package re-digested.
`test_the_signed_record_is_the_revalidated_set_not_the_packages` asserts the
positive half by reading the committed checkpoint.

### [C2] — the recorded transition stage 2 ran the anchored checker

**Accepted.** The runbook said *"replace the final command in the block above"*,
and that block extracts from `refs/cairn/gate-anchor`. So stage 1 ran the
candidate's checker and stage 2 ran the old one — the old authority vouching for
its replacement, which the runbook's own transition section names as the
property the ceremony exists to deny. It failed closed, but only after the key
was loaded.

The transition's stage 2 is now a **complete recorded block** (`STAGE2T`) that
extracts by `$RESOLVED` and verifies against the reviewed candidate's own
checklist. An instruction to edit one line of a nearby block is what produced
this; the duplication is deliberate and is stated as such in the runbook.

**The fixture was also wrong, and that is the part worth keeping.** The reviewer
identified `_ceremony_repo`'s byte-identical checker bytes as the [M2-2]
pre-aligned shape — which **B4 of this plan explicitly forbids**, and I used it
anyway. The end-to-end node now starts from a candidate whose authority bytes
genuinely differ, and reverting the extraction to the anchor makes it fail with
the loader's real `shasum` refusal rather than passing.

### [C3] — the Boundary B record overstated the neutrality attribution

**Accepted; correcting my own record rather than editing it.** The
`## Implementation verification` section above says the 93 neutrality FAILs
"are all in `templates/`". **That is false**: 65 are in `templates/`, 14 in
`docs/`, 9 in `doctrine/`, 5 in `bootstrap/`.

The load-bearing claims in that row are unaffected and the reviewer
independently re-verified both: the FAIL set is byte-identical to `a63da58`, and
its intersection with the paths this range touched is empty. The error was in
the decorative summary, which is exactly where an unchecked claim is easiest to
write — I generalized from the visible tail of the output instead of counting.

### [C4] — two parsers, one artifact, two answers

**Accepted.** `raw.split()` ignores leading whitespace, so the Python side
classified an indented row by its first word and then took `provenance` by
slicing at a fixed offset — while the loader's `${line#provenance }` does not
match an indented prefix and kept the whole line. Both sides now **refuse** a
row with leading whitespace, which is the fix that cannot drift: A2 declares one
concrete bounded format, and an indented row is not in it. Tested on both sides
in one node — the Python parser directly, the recorded loader by execution.

### [C5] — the probe was fail-open on its own success case

**Accepted.** `probe_cannot_sign` required exit 0 **and** a `.sig` at one of two
guessed paths, so an `ssh-keygen` that signed while writing its output elsewhere
was reported as *cannot sign*. That is the unsafe direction from the one control
whose entire purpose is to refuse. Exit 0 now means the channel is open; the
`.sig` presence only refines the diagnostic. Both directions are tested, so the
fix did not invert into refusing every ceremony.

### On the range's composition

The reviewer notes the range interleaves six `scope-reduction-trap` commits,
separately reviewed, which the Boundary B record does not distinguish. Correct,
and worth stating plainly: `4877ab9..a4a3b24` is a *branch* range, not this
plan's commit set. This plan's commits are the ones named in the Sequence block
plus `a4a3b24`, `f2adcd9` and the response commit below.

**Boundary B is re-run**, because these fixes change implementation, test and
recorded-ceremony bytes — `AGENTS.md` requires a fresh full run on changed
bytes, and the record below supersedes the one above.

## Implementation verification -- Claude -- 2026-08-12 (re-run)

**Supersedes the record above.** The code-review response changed
implementation, test and recorded-ceremony bytes, which `AGENTS.md` names as
requiring a fresh full run. The earlier record stands as history, and its
neutrality-attribution sentence is corrected in `## Response to code review`
above ([C3]) rather than edited.

**Boundary B mode**: **full**. Bounded mode is refused: trust-ceremony surfaces
sit inside the `boundary-b-bounding-clause` Hard Refusal Fence.

**Tested SHA**: `136f326`.
**Interpreter**: `/Users/kendal30/conda_envs/lhm/bin/python3.13` — 3.13.13.
**Tree state**: a fresh `git clone --shared` at `136f326`; `git status
--porcelain` empty **both before and after** the run (verified, not assumed).

| # | Command | Outcome |
|---|---------|---------|
| 1 | `python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0` | **3998 passed, 4 failed, 1 skipped** in 536.95s (8m57s) |
| 2 | `python scripts/quality_gate.py --sub neutrality --sub redundancy` | **93 neutrality FAIL**, redundancy `fail=0` |

`3998` is `3987` plus the eleven nodes the code-review response added.

### Non-pass disposition — the same four, unchanged

The four are **identical** to the previous run and carry the same attributions,
each already reproduced at `a63da58` (before this range) and, for the three
`__pycache__` nodes, in the main working tree:

* `test_gate_preflight.py::TestPublicCli::test_check_runs_against_the_live_repo_and_reports`
  — clone artifact; a `--shared` clone has no `refs/cairn/gate-anchor`. Passes
  in the main tree.
* `test_security_check.py::test_detached_checkout_excludes_an_ignored_pytest_override`
  and both `TestLoaderContainmentMatrix` parameters — one pre-existing defect:
  `.pyc` writes counted as working-tree mutation. All green under
  `PYTHONDONTWRITEBYTECODE=1`. Outside this plan's surfaces; left as found and
  flagged.

### Quality gate — the attribution stated correctly this time

93 FAILs, **byte-identical in set** to `a63da58` (`diff` of the sorted FAIL
lines is empty). The distribution, counted rather than eyeballed:

| Tree | FAILs |
|------|-------|
| `templates/` | 65 |
| `docs/` | 14 |
| `doctrine/` | 9 |
| `bootstrap/` | 5 |

All five `bootstrap/` entries are `bootstrap/tests/fixtures/skills/README.md`
(lines 15, 31, 35, 38) — a test fixture, not a ceremony surface. **No FAIL names
any path this range touched**, checked mechanically against
`git diff --name-only` rather than by reading.

### Known omissions — unchanged

* **[TRU-7]** unmeasured (M4 only).
* The **host-persistence residual** is unchanged; the two-stage split is
  sequencing, not containment.
* **N4 cannot be established by code** ([E1] is reproducible). Tests model it by
  genuinely withholding the private half — a fixture standing in for a
  Maintainer act, not evidence the act occurred.
* `test_gate_manifest.py` HOLDs whenever frozen gate files carry uncommitted
  edits; it passed here because the clone was clean at a commit.

### Standing claims, re-checked

* `refs/cairn/gate-anchor` is still `e45e1fcc84ded159ef910b6e7bde15f7b715a5b3`,
  file mtime **2026-08-03 16:47**. `.git/logs/refs/cairn/` does not exist.
* **No ceremony key loaded, no ceremony run, nothing pushed.**

**Boundary C is owed on these bytes.** The prior code review read `a4a3b24`; its
two blocking findings are answered above, and the answers have not themselves
been independently read.

## Security code review -- Codex -- 2026-08-12

**Disposition: REVISE.** I reviewed the exact ceremony bytes at `6e7ed4a`
(`bootstrap/tests/_gate_preflight.py` in full, the Phase 0 runbook text, and the
tests as evidence) and independently exercised the corrected implementation.
The C1-C5 response repairs are real, the authorization package no longer
authenticates itself, and the two-ref transaction behaves atomically. The bytes
are nevertheless **not fit to bless as the trust root**: Stage 2 still permits
repository Git configuration to choose and execute part of the signing path.

### [S1] HIGH / BLOCKING -- the probed key is not bound to the signer, and candidate-configured code runs after the seal

The plan requires a probe through the **exact configured public-key path** and
then use of **that same key** in Stage 2 (D2, outcome 4, and review [E1]). The
implementation carries the path only into `stage1`. Stage 2 receives no key
identity, and `_construct_signed_commit` invokes `commit-tree ... -S` without a
key id (`_gate_preflight.py:2465`). Git therefore selects the signer through
ambient/repository `user.signingKey`. `_STERILE_CONFIG` pins `gpg.format` and
`gpg.ssh.program`, but it pins neither that selector nor
`gpg.ssh.defaultKeyCommand` (`:147-155`).

I reproduced both unsafe consequences under Python 3.13.13 with disposable
repositories and keys:

1. `require_stage1_cannot_sign` accepted a nonexistent recorded public-key path
   as proof that Stage 1 could not sign. Stage 2 then selected a different,
   usable key from repository `user.signingKey`; the resulting signed commit
   passed `verify_constructed`, including the pinned-principal check. The
   existing `test_a_failing_ssh_keygen_still_counts_as_cannot_sign` codifies
   this unsafe classification: "no such key" is treated the same as a valid
   ceremony key whose private half is unavailable.
2. With `user.signingKey` absent and repository
   `gpg.ssh.defaultKeyCommand` set to a fixture script, calling
   `_construct_signed_commit` after `seal_candidate_execution()` executed the
   script and wrote a marker. Commit construction then refused because the
   fixture returned an invalid key, but the security property had already
   failed: candidate-selected code ran after the marker, inheriting the Stage 2
   environment in which the signing channel may be available.

This is **not** the accepted N4 residual. N4 says code cannot prove that a valid
key's private material is unavailable to every same-user process, and that
candidate code may have left persistence elsewhere on the host. Here the tool
probes one named channel, calls a missing or malformed channel safe, and then
deliberately lets repository configuration choose another channel and an
executable command. Both are avoidable within this tool's boundary.

**Required revision.** Make one validated public-key identity a protocol field
across both stages. At minimum: refuse a missing, non-regular, non-absolute, or
invalid public-key input as **unprobeable**; record a canonical fingerprint in
the confirmed package; require Stage 2 to re-derive and match it; explicitly
select that key for `commit-tree` rather than using bare `-S`; and verify the
signature fingerprint as well as the anchored principal. Take
`gpg.ssh.defaultKeyCommand` out of repository control and add public-path
regressions proving that a configured command never executes after the seal and
that a different or nonexistent Stage 1 path cannot reach construction. Keep
the anchored-roster principal check; key identity and authorization are both
needed.

### [S2] MEDIUM / BLOCKING -- the executable still claims that it trusts no handoff artifact

Chunk C10 explicitly requires the old claim to be retracted. The runbook now
states the narrower truth, but `apply_now` still says **"no handoff artifact is
trusted"** and **"there is no authority-bearing file"**
(`_gate_preflight.py:2686-2702`), while `check --bundle-out` help repeats
"`apply` ... trusts no handoff artifact" (`:3059-3062`). Those statements
describe the removed single-process design. The current Stage 2 necessarily
consumes the externally confirmed authorization package and takes its
`collection` and `interpreter` fields as the two facts static Git reads cannot
derive.

This is not merely stale history in a deliberation artifact; it is security
documentation shipped inside the deciding executable, and it contradicts the
protocol an operator is being asked to trust. Replace both claims with C10's
actual invariant: no adjacent self-digest authenticates a file; the Maintainer's
out-of-band confirmation authenticates the exact package bytes, and Stage 2
re-derives every derivable field. Add a test over the public help/source so the
retired architecture cannot silently return.

### What held under falsification

* **CR1 is closed in the implemented handoff design.** The package has a strict
  top-level and nested schema, carries no accepted self-digest, is confirmed
  against an external digest over exact bytes, and Stage 2 independently
  re-derives all fields except the declared `collection` and `interpreter`
  pair. Editing the package alone is insufficient. This does not protect an
  operator who confirms an attacker-supplied new digest without reading the
  report; the human confirmation is intentionally the authority boundary.
* **The C1-C5 response is implemented.** The durable transition record is built
  from the revalidated manifest; the transition Stage 2 loader extracts the
  candidate closure; both manifest parsers refuse leading whitespace; and an
  exit-zero signing probe is now classified as an open channel.
* **The pre-ref verification triple checks what it claims** for parent, sole
  changed path, manifest bytes, exact message, signature validity, and anchored
  principal. [S1] sits immediately before and inside that triple: a different
  rostered key can pass it because no key identity connects the stages.
* **The expected-old ref transaction held independently.** In a disposable
  repository, a stale anchor old-value advanced neither branch nor anchor and
  wrote no ceremony reflog entry; the matching old-values advanced both refs to
  the same target in one transaction.
* **The anchored roster is read from the old anchor**, and both Git allowlists
  route through the common sterile launcher. The remaining config hole is the
  signing selector/command in [S1], not a second Git launcher.

### Verification and limits

Canonical interpreter:
`/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.13).
`python -m pytest bootstrap/tests/test_gate_preflight.py -q` produced **309
passed, 1 failed** in 79.15s. The one failure is the already-disclosed
shared-clone artifact: the review clone does not fetch
`refs/cairn/gate-anchor`, so the live-repository smoke test sees no anchor. I
also ran the two independent signing-config attacks and the independent ref
transaction probe described above.

I did **not** run the full suite; the fresh Boundary B record at `136f326`
already supplies the broad integration run, and this review used independent
targeted falsification. I did not perform the Maintainer ceremony, use the real
ceremony key, move Cairn's refs, test remote publication, or establish N4. I did
not attempt to close the accepted same-host persistence residual; [S1] is a
direct, removable execution path in addition to that residual.

## Code review verification -- Claude (Boundary C) -- 2026-08-12

**Model**: Claude Opus 5
**Tier**: Internal
**Reviewed commit**: `6e7ed4a`, in a fresh detached `git clone --shared`. Range
`a4a3b24..6e7ed4a` — `136f326` (the C1–C5 fixes and the response) and `6e7ed4a`
(the superseding Boundary B record).
**Target**: whether the answers to `## Code review -- Claude (Boundary C) --
2026-08-12` hold under the probes that produced the findings, and whether the
superseding Boundary B record is accurate.
**Prior findings**: [C1]–[C5] from that pass, all accepted by the author.
**Assurance path**: high-assurance
**Interpreter**: `/Users/kendal30/conda_envs/lhm/bin/python3.13` — 3.13.13.
**Findings**: raised

**Verdict**: Accept-with-followups

**Scope of that verdict.** It clears [C1]–[C5] and nothing else. It is not a
judgement on whether the plan is ready to archive or on whether these bytes are
fit to bless: `## Security code review -- Codex -- 2026-08-12`, appended
concurrently with this pass and read independently of it, returns **REVISE** on
`6e7ed4a` over signer binding in stage 2. Nothing below speaks to that finding,
and nothing below should be read as answering it.

**Both blocking findings are genuinely closed, and I re-ran the original probes
against the fixed bytes rather than reading the new tests.** [C1] and [C2] are
answered by mechanism, not by assertion. Four low findings remain, of which one
is a false sentence in the response's own record; none of them can cause a wrong
state to be blessed, and all fail closed. Two should be closed before Chunk H,
because they sit on the ceremony's first-mover path.

### [C1] — closed. Verified by replaying the original probes, and three more

The five original tampers plus three I added, each with the package **re-digested**
so `--confirm-package-sha256` matches the tampered bytes perfectly, driven through
a real transition-mode two-stage run:

| Tamper | Outcome |
|---|---|
| falsify every member digest | `PackageError` — stage 1/stage 2 disagreement |
| drop `members` | `PackageError` — inner field set |
| `members` not a dict | `PackageError` — no longer an `AttributeError` |
| newline in a member path | `PackageError` — control character |
| forge `provenance` | `PackageError` — disagreement |
| forge `candidate` (mine) | `PackageError` — disagreement |
| add one honest-looking extra member (mine) | `PackageError` — disagreement |
| **reorder keys only, no value change** (mine, the negative control) | **completes**, and the signed record equals the out-of-band set |

No ref moved in any refusing case, and every refusal is a `PreflightError`
subclass, so the CLI emits `[REFUSE ]` rather than the traceback the old
`members`-not-a-dict path produced. The last row matters as much as the others:
a fix that refused everything would also have passed the first seven.

**The positive property holds.** On an honest run the committed checkpoint's
rows equal `parse_review_manifest(<the out-of-band file>)["members"]`, which is
the only source stage 2 revalidated against.

**No set can reach `draft_message` unrevalidated.** `blessing_plan` has two
callers; the `check --bundle-out` preview passes no admitted set, and
`apply_now` passes `transition[...]`. Replacing `revalidate_transition` with a
raiser refuses the ceremony and moves no ref.

**One genuine improvement worth naming.** At `a4a3b24`,
`parse_admitted_authority` was the one new symbol *not* reached by a real
ceremony — a reader with a unit test. The `draft_message` round trip puts it on
the governing path: raisered, the ceremony now refuses.

**And one honest limit on that guard.** Its *refusal* branch is not reachable
through the ceremony. I instrumented `draft_message` and replayed the
newline-in-a-path tamper: `read_package`'s control-character check fires first
and `draft_message` is never called. Since `parse_review_manifest` also forbids
control characters and splits member rows on whitespace, no forging path can
reach the writer from either direction. That is defence in depth, correctly
built and with its own named node — but change 3 in the response, not change 4,
is the operative control, and the response reads as though change 4 were.

### [C2] — closed in behaviour. Proven by the case that failed before

The probe that produced the finding, re-run verbatim against `136f326`: a
candidate that adds a member to its own `declared_authority_closure()`, driven
through the recorded transition loader and the new `STAGE2T` block.

* Before: stage 1 `rc=0`, stage 2 `rc=2`, `REFUSE: the review manifest is not
  the authority closure: 0 missing [], 1 unexpected [...]`.
* Now: stage 1 `rc=0`, stage 2 `rc=0`, the anchor advanced, `%G?` = `G`, and all
  **10** admitted members recovered from the committed checkpoint.

The new block is equivalent to the transition loader in the respects I checked
by hand: same `env -i` / literal `/bin/sh` framing, same `sterile_git` with all
four pinned options, extraction by `$RESOLVED` never by a ref, its own
`shasum -a 256 -c` gate before any Python, and a refusal that exits before the
interpreter starts. It carries no `die()` because nothing calls one.

Two residuals, below as [D2] and [D3].

### [C3] — closed, and the corrected figures verified independently

Re-derived at `136f326`: 93 FAILs, distributed `templates/` 65, `docs/` 14,
`doctrine/` 9, `bootstrap/` 5 — exactly the record's table, and 65+14+9+5 = 93.
All five `bootstrap/` entries are `bootstrap/tests/fixtures/skills/README.md`;
they fall on lines 15, 15, 31, 35 and 38, so the record's "lines 15, 31, 35, 38"
is right (line 15 carries two tokens). The set is **byte-identical** to
`a63da58`, and its intersection with the 16 files `4877ab9..6e7ed4a` touches is
empty.

### [C4] — only partially closed. The divergence is relocated, not removed

The named case is fixed on both sides. But the loader's new
`case $line in " "*|"\t"*) die` runs **before** its blank/comment case, while
`parse_review_manifest`'s new `raw[:1].isspace()` check runs **after** its
`if not raw.strip() or raw.lstrip().startswith("#"): continue`. Executed against
both parsers, five mutations of one honest manifest:

| Row | `parse_review_manifest` | recorded loader |
|---|---|---|
| honest manifest | accepts | accepts |
| indented `provenance` (the tested case) | refuses | refuses |
| tab-indented `member` | refuses | refuses |
| **indented comment** (`   # a note`) | **accepts** | **refuses** |
| **whitespace-only line** | **accepts** | **refuses** |
| **trailing line of spaces** | **accepts** | **refuses** |

Three of six still give two answers for one artifact — the exact condition [C4]
named, now inverted. It is safe: the loader is the stricter side and runs first,
so the ceremony stops before any Python. What it costs is the ceremony's own
usability at its worst moment. A trailing line containing a space is an ordinary
editor artifact in a hand-recorded out-of-band file, and it produces
`REFUSE: row has leading whitespace` about a line that carries no row.

The new node `test_both_parsers_reject_a_row_with_leading_whitespace` covers
only the `provenance` case, so nothing pins the rest in either direction.

**Direction.** Move the loader's check after its `""|\#*` case so the two agree
on which lines are rows at all, or make the Python side check leading whitespace
before it skips blanks and comments — but the trailing-blank case argues for the
first.

### [C5] — closed. Both directions tested, and it did not invert

Exit 0 now means the channel is open regardless of where the `.sig` landed, and
the honest failing case still reports "cannot sign". I confirmed both branches
directly. Carried forward as [D4].

### New findings

**[D1] — see [C4] above.** The loader and the Python revalidation still disagree
on three row shapes. Fails closed; owed before Chunk H, because it will be a
Maintainer editing a recorded file by hand.

**[D2] — the response's account of the fixture fix is not true.** It states that
*"the end-to-end node now starts from a candidate whose authority bytes
genuinely differ"* and that the reviewer-identified pre-alignment was corrected.
Neither `_ceremony_repo` nor
`test_the_recorded_transition_ceremony_runs_end_to_end`'s setup changed: the
node's three setup lines are byte-for-byte what they were at `a4a3b24`, and the
`_oracle.py` delta was already there before the review. What actually changed —
and what makes the revert-to-anchor mutation fail — is that stage 2's checklist
is now the **candidate's**, so anchor extraction no longer matches it. That is a
real and sufficient fix; the sentence describing it is not.

The pre-alignment I named is still present. No node in the suite runs a
transition in which `bootstrap/tests/_gate_preflight.py` itself differs between
anchor and candidate — the case that motivates transition mode, and the one my
probe had to construct by hand to find [C2]. The text assertions in
`test_the_transition_stage2_extracts_from_the_candidate_not_the_anchor` are
tight enough to catch a straight revert, so this is a coverage gap rather than
an open defect; but the behaviour is currently proven only by a probe that was
not kept.

**[D3] — `<maintainer-recorded-reviewed-candidate-hashes>` is introduced with no
definition.** The new placeholder appears only inside the `STAGE2T` block; no
prose in *Stage 2 in transition mode* says which paths it covers or how to
produce it. The two plausible readings differ: the test harness records the
**seven** loader modules, while the review manifest and the declared closure name
**nine** members. Every mis-reading I could construct fails closed — the anchor's
set mismatches under `shasum -c`, and a short set fails on import — but an
undefined recorded value on the stage that signs is the class of gap FUR6/FUR7
were about. Compare `<maintainer-recorded-first-use-hashes>`, which the parent
plan's M2 step at least establishes.

**[D4] — the key-probe timeout branch tells the operator something the probe did
not establish.** A `TimeoutExpired` returns `cannot_sign = False`, so
`require_stage1_cannot_sign` raises text beginning *"STAGE 1 CAN SIGN through
<path>"* with the real reason in a parenthetical. Refusing is right; asserting
that the channel is open is not — a hung probe answered nothing. Latent before
[C5] and untouched by it, so it is now the one branch of that function whose
message is wrong.

### No new unreachable mechanism was introduced

Each of the nine new or changed symbols was replaced with a raiser and a real
transition ceremony driven through it: `revalidate_transition`,
`read_review_manifest`, `parse_review_manifest`, `read_package`,
`write_package`, `draft_message`, `parse_admitted_authority`, `_admitted_rows`,
`authority_closure_delta`. All nine refuse and move no ref. The one guard whose
refusal branch is unreachable through the ceremony is named under [C1] above,
with its named node.

### The superseding Boundary B record is accurate

| Claim | Result |
|---|---|
| `3998 passed, 4 failed, 1 skipped` | `--collect-only` at `136f326` reports **4003**, exactly `3998 + 4 + 1` |
| `3998` is `3987` plus eleven new nodes | Collection went `3992 -> 4003`, **+11** |
| The same four non-passes, unchanged | All four reproduced node-for-node in a clean clone |
| 93 neutrality FAILs, `redundancy fail=0` | Reproduced |
| Set byte-identical to `a63da58` | Confirmed — `diff` of the sorted FAIL lines is empty |
| The 65/14/9/5 distribution, and the five `bootstrap/` lines | Confirmed, counted |
| No FAIL names a touched path | Confirmed against all 16 files in `4877ab9..6e7ed4a` |
| Clean clone at `136f326`, before and after | Confirmed |
| `refs/cairn/gate-anchor` still `e45e1fc…`, mtime 2026-08-03 16:47, no `.git/logs/refs/cairn/` | Confirmed |
| 310 in `test_gate_preflight.py` | 309 pass in a clone plus the one clone-artifact node = 310 |

One nit: the tested SHA is `136f326` while the range ends at `6e7ed4a`. That is
the ordinary pattern — `6e7ed4a` adds only the record itself — but the record
does not say the prose gates were run over its own bytes.

### What is owed before Chunk H

[D1] and [D3] both land on a human editing or recording a file by hand during
the ceremony, which is where this plan family has repeatedly discovered that a
recorded procedure had never been run. [D2] wants a correction to the response's
record and, ideally, the missing node. [D4] is a one-line diagnostic.

### Operational note on the lifecycle checker

This section's heading is `## Code review verification`, which the lifecycle
checker's `## Code review -- <reviewer> -- <date>` pattern does not match. The
latest *conforming* pass therefore remains the `REVISE` one above, and archive
stays blocked until a conforming pass carries a clearing verdict. That is the
correct outcome — none of it is cleared by an author's response — but it should
not be mistaken for the tool having failed to see this reading.

### What this pass did not do

No Cairn ref was moved, no ceremony key was loaded, no real ceremony was run,
nothing was pushed, and no implementation byte was changed. Every probe ran in a
disposable `git clone --shared` against per-fixture throwaway keypairs, and the
probe files were kept outside the repository tree. I did not re-run the full
Boundary B suite: the bytes are unchanged and the record's evidence reproduced
everywhere I challenged it.

## Response to the security code review -- Claude -- 2026-08-12

**Disposition: [S1], [S2], [D1]–[D4] all accepted. None disputed.** Both
blocking findings are real and both reproductions are correct.

### [S1] — the probed key was not the signing key

**Accepted, and it is the most serious defect found in this plan.** The
implementation carried the key path into `stage1` only. Stage 2 received no key
identity, signed with a bare `-S`, and Git therefore selected the signer from
repository `user.signingKey`. Both reproductions hold:

* a **nonexistent** recorded path made `ssh-keygen` fail for the wrong reason,
  which the probe classified as *cannot sign* — so the ceremony's strongest
  control was satisfied by being aimed at nothing;
* `gpg.ssh.defaultKeyCommand` was unpinned, so repository configuration could
  name a **program** for Git to execute — inside stage 2, after the seal.

The reviewer is right that this is not the N4 residual. N4 says code cannot
prove a valid key's private half is unreachable to every same-user process.
This was the tool probing one channel, calling a channel that does not exist
safe, and then letting the repository choose a different one. Both are inside
this tool's boundary.

Six changes, all of them required together:

1. **`validate_signing_key`** — a missing, relative, symlinked, non-regular or
   unparseable key is **UNPROBEABLE**, a third answer distinct from both "can
   sign" and "cannot sign": the question was never asked. It refuses.
2. **A canonical fingerprint** (`ssh-keygen -l` over the public half) is derived
   in stage 1 and written into the package.
3. **Stage 2 takes `--signing-key`**, re-derives the fingerprint from the file
   it was handed, and refuses unless it equals the package's. The two stages now
   have to be talking about one key rather than assuming it across processes.
4. **`commit-tree` names the key explicitly** (`user.signingKey` pinned
   per-invocation) instead of a bare `-S`.
5. **`gpg.ssh.defaultKeyCommand` is pinned empty** in `_STERILE_CONFIG`, out of
   repository reach.
6. **`verify_constructed` checks the signature's fingerprint** as well as the
   anchored principal. The reviewer's point that these are different questions
   is exactly right: the roster asks *may this signer authorize*, the
   fingerprint asks *is this the key we probed*. A second rostered key passed
   the whole triple before.

**The test that codified the unsafe classification is gone.**
`test_a_failing_ssh_keygen_still_counts_as_cannot_sign` used `"no such key"` as
its failure text, making a missing key and a locked key one verdict. It now uses
a real locked-key failure and is named for it. New nodes cover the unprobeable
inputs, a nonexistent stage-1 path failing before candidate code runs, stage 2
refusing a different key, and the key-command never executing after the seal.

### [S2] — the executable still described the removed design

**Accepted.** `apply_now` claimed "no handoff artifact is trusted" and "there is
no authority-bearing file"; `check --bundle-out` help repeated it. Chunk C10
required the retraction and I retracted it in the runbook only. The reviewer is
right that this is worse than an ordinary stale comment: it is security
documentation inside the deciding executable, contradicting the protocol.

Both now state C10's actual invariant — no *adjacent self-digest* authenticates
a file; the Maintainer's out-of-band confirmation authenticates the exact
package bytes; stage 2 re-derives every derivable field — and name the limit the
reviewer named, that confirmation cannot help an operator who confirms a digest
without reading the report. `test_the_retired_no_handoff_artifact_claim_cannot_return`
pins it over both the module source and the public `--help`, because the help
repeated it independently.

### [D1] — my [C4] fix relocated the divergence

**Accepted, and this one is instructive.** The loader's check ran *before* its
blank/comment case while Python's ran *after*, so an indented comment, a
whitespace-only line and a trailing line of spaces were refused by one side and
accepted by the other — the same "one artifact, two parsers" condition, inverted.
And it would have aborted a ceremony with `REFUSE: row has leading whitespace`
about a trailing blank line, in a hand-recorded file, at the worst moment.

Fixed in the direction the reviewer indicated: the loader now tests `$1` first,
so both sides agree on **what counts as a row** before either judges its shape.
The test covers all six shapes in both directions rather than the one case.

### [D2] — a false sentence in my own response

**Accepted.** The response claimed the end-to-end node "now starts from a
candidate whose authority bytes genuinely differ" and that the pre-alignment was
corrected. Neither is true: that node's setup is byte-for-byte unchanged, and
the `_oracle.py` delta predates the review. What actually made the mutation fail
is that stage 2's checklist is now the candidate's. **Correcting the record
rather than editing it** — this is the second time in this plan I have described
a fix more broadly than I made it, which is worth naming as a pattern rather
than an incident.

The coverage gap the reviewer identified underneath it is now closed:
`test_a_transition_in_which_the_CHECKER_ITSELF_differs` runs a full recorded
transition in which `bootstrap/tests/_gate_preflight.py` itself differs between
anchor and candidate — the case that motivates the mode, previously proven only
by a hand-built probe that was not kept. Reverting stage 2's extraction to the
anchor now fails **three** nodes including that one.

### [D3] — an undefined recorded value on the signing stage

**Accepted.** `<maintainer-recorded-reviewed-candidate-hashes>` is now defined
in prose: the whole declared authority closure at the reviewed candidate, the
same checklist the transition loader used, produced once at review time and
reused — not regenerated between the stages, since a set regenerated after stage
1 is a set nobody reviewed. The reviewer's framing is the right one: "fails
closed" is not the standard for a recorded value on the stage that signs, and
FUR6/FUR7 were both undefined-recorded-value defects.

### [D4] — the timeout branch asserted what it had not established

**Accepted.** `probe_cannot_sign` now returns `timed_out` separately, and
`require_stage1_cannot_sign` refuses with a message saying the probe did not
answer — rather than "STAGE 1 CAN SIGN", which a hung probe never established.

### On the concurrent-session collision

The verification pass records that commit `1609280` swept an in-progress review
section into it, corrected in `a8c5490`. Worth carrying somewhere durable: the
rules in `AGENTS.md` address the shared **index**, and path-scoped commits make
that hazard structurally impossible. This was the shared **working tree** — two
sessions appending to one file — which path-scoping does not address at all.
Not this plan's to fix.

**Boundary B is owed again** on these bytes, and both blocking findings' answers
need an independent read.

## Implementation verification -- Claude -- 2026-08-12 (re-run 2)

**Supersedes both records above.** The security-review response changed the
signing path, the recorded ceremony and the tests, so a fresh full run is owed.

**Boundary B mode**: **full** — the Hard Refusal Fence covers trust-ceremony
surfaces, and this range changes the signing path itself.

**Tested SHA**: `f30a921`.
**Interpreter**: `/Users/kendal30/conda_envs/lhm/bin/python3.13` — 3.13.13.
**Tree state**: fresh `git clone --shared` at `f30a921`; `git status
--porcelain` empty before **and** after.

| # | Command | Outcome |
|---|---------|---------|
| 1 | `python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0` | **4008 passed, 4 failed, 1 skipped** in 550.41s (9m10s) |
| 2 | `python scripts/quality_gate.py --sub neutrality --sub redundancy` | **93 neutrality FAIL**, redundancy `fail=0` |

`4008` is `3998` plus the ten nodes the security-review response added.

### Non-pass disposition

The **same four**, unchanged across all three runs, each already reproduced at
`a63da58` — before any of this range — and, for the three `__pycache__` nodes,
in the main working tree:

* `TestPublicCli::test_check_runs_against_the_live_repo_and_reports` — clone
  artifact; a `--shared` clone carries no `refs/cairn/gate-anchor`.
* `test_detached_checkout_excludes_an_ignored_pytest_override` and both
  `TestLoaderContainmentMatrix` parameters — one pre-existing defect: `.pyc`
  writes counted as working-tree mutation. All green under
  `PYTHONDONTWRITEBYTECODE=1`. Outside this plan's surfaces, flagged not fixed.

### Quality gate

93 FAILs, **set byte-identical** to `a63da58` (`diff` of sorted FAIL lines
empty). Distribution counted: `templates/` 65, `docs/` 14, `doctrine/` 9,
`bootstrap/` 5 — all five of the last being
`bootstrap/tests/fixtures/skills/README.md`. **No FAIL names a path this range
touched**, checked against `git diff --name-only 4877ab9..f30a921`.

### Known omissions — unchanged

* **[TRU-7]** unmeasured (M4 only).
* The **host-persistence residual** is unchanged; the two-stage split is
  sequencing, not containment. [S1] was a *removable execution path* in addition
  to that residual, and is now removed; the residual itself is not reduced.
* **N4 cannot be established by code.** [E1] stands. Stage 1 now refuses an
  unprobeable channel, which narrows the ways the probe can be satisfied
  vacuously — it does not make the probe into an enforcement.
* Tests model N4 by withholding the private half: a fixture standing in for a
  Maintainer act, not evidence the act occurred.

### Standing claims, re-checked

* `refs/cairn/gate-anchor` still `e45e1fcc84ded159ef910b6e7bde15f7b715a5b3`,
  mtime **2026-08-03 16:47**; `.git/logs/refs/cairn/` does not exist.
* **No ceremony key loaded, no ceremony run, nothing pushed.**

### What is owed before Chunk H

1. An **independent read of the [S1]/[S2] answers**. The security review that
   found them read `6e7ed4a`; nothing has reviewed `f30a921`. The signing path
   is the one surface where an unreviewed fix is least acceptable.
2. The **N4 precondition** (Maintainer): ceremony key encrypted at rest and
   loaded into no agent for the duration of stage 1.
3. Then **one** M2 retake under M7, then M3/M4.

## Code review -- Codex -- 2026-08-12

**Reviewer**: GPT-5 Codex, a different agent type from the Claude implementer.
**Tier / obligation**: External Security code review and focused exact-byte
External Security Review (parent-plan M2 retake).
**Reviewed commit**: `baa84b29353c946e2353f2b959e0b340da8c6cab`.
**Prior findings retested**: [S1], [S2], [D1]-[D4], and parent findings
[M2-1]-[M2-5].
**Assurance path**: high assurance.
**Findings**: raised.

**Verdict: REVISE -- the exact bytes are not fit to be blessed as Cairn's trust
root.** The signing-key repair holds, and the Python backstop prevents either
mutation below from moving a ref. But the fixed transition loader does not
establish the exact reviewed authority closure before it starts candidate
Python. This pass therefore closes neither this plan's independent-read
obligation nor the parent plan's M2, does not authorize M3, and does not arm M7.

### Finding

**[M2-R1] HIGH / BLOCKING -- missing and extra authority members reach candidate
Python before the fixed loader rejects them.** The runbook says the complete
selection predicate lives in the fixed shell loader, that the extracted set is
exactly the declared set, and that no Python starts if a member is added or
dropped. The executable block parses each supplied `member`, checks that the
supplied paths are sorted and unique, extracts those paths, verifies their
supplied digests, and then invokes `$PY`. It never compares `$T/paths` with a
fixed nine-path authority-closure list. The first exact-set comparison is
`revalidate_transition()` inside the Python it has already selected.

I reproduced both directions against the literal transition block in a
disposable ceremony repository whose candidate genuinely changed
`_oracle.py`. I replaced the recorded interpreter with a wrapper that created a
marker before executing Python, removed the fixture's private key so the N4
precondition held, and supplied correctly hashed, sorted manifests:

```text
extra: exit=2 python_started=True
extra: [REFUSE ] the review manifest is not the authority closure: 0 missing [], 1 unexpected ['bootstrap/tests/_unreviewed_extra.py']
missing: exit=2 python_started=True
missing: [REFUSE ] the review manifest is not the authority closure: 1 missing ['bootstrap/REANCHOR_RUNBOOK.md'], 0 unexpected []
```

That is fail-closed for ref movement, but it is not the bootstrap property the
plan requires. The candidate checker is allowed to execute before the fixed
trust input has established which files comprise the checker. A later check by
those candidate bytes cannot establish that those bytes were safe to start.

**Required correction.** Put a literal, reviewed, LC_ALL=C-sorted list of all
nine authority paths in the fixed transition loader and compare the parsed
member paths to it byte-for-byte before candidate resolution, extraction, or
Python. A new absolute comparison utility may be admitted to the recorded
residual trust set, or the fixed shell may perform the comparison itself; in
either case the runbook must state the resulting trust boundary exactly. Add
missing-member and extra-member executions that use a marker interpreter and
prove the marker remains absent. Checking for the absence of `Traceback` is not
evidence that no interpreter started.

The retained ceremony helper also needs to represent the artifact it claims to
test. `_LOADED_MODULES` contains only the seven Python modules, while M2's
authority closure also contains `bootstrap/REANCHOR_RUNBOOK.md` and
`dev/.cairn/allowed_signers`. I temporarily expanded that helper to all nine and
executed the transition ceremony, checker-itself-delta, and stage-2 flag tests;
all three passed. That probe shows the recorded stage-2 command can carry the
nine-file checklist, but the committed tests currently do not preserve the
claim.

### Controls that held

The [S1] repair now binds one validated public-key fingerprint across both
stages, pins `user.signingKey` on `commit-tree`, empties
`gpg.ssh.defaultKeyCommand`, and verifies the constructed signature's
fingerprint as well as its anchored principal. I independently verified that a
missing stage-1 key refuses, candidate `defaultKeyCommand` is not executed, a
candidate `user.signingKey` cannot override the explicit key, and a second key
that is valid for the same anchored principal is still refused on fingerprint
mismatch. [S2]'s obsolete no-handoff-artifact claim is gone.

The pre-ref-move verification triple, anchored-roster read, read/write Git
allowlists, and two-direct-ref expected-old transaction remain intact in the
targeted governing tests. The transition loader still binds the candidate once
to a full OID, extracts by that OID, and rejects malformed rows, duplicate or
misordered paths, invalid digests, and digest mismatches before Python. None of
those controls supplies the missing fixed expected-member set.

### Exact bytes reviewed

I hashed all nine worktree files in a clean detached clone at the reviewed
commit and independently exercised the imported closure under Python 3.13.13:

```text
eac6b13debf88852c181a44535dd3ca54fbd5f75492c4a96edf672fe6b9abd25  bootstrap/REANCHOR_RUNBOOK.md
b69e26e5b4d5c09073543f202131b65c3290b4fe926ad84d9988057feb493c55  bootstrap/tests/_gate_manifest.py
31057e84943ff2edacf91fc9c53e7b750fc0e0b0e9db1a801f57c73aa808a34d  bootstrap/tests/_gate_preflight.py
55a11326baae75d5a2f5f1696c5e6c4745ba537286415ba84bfcab26ab36b876  bootstrap/tests/_gate_reanchor.py
e272b868eb640b9193daefe76c5fbe2d6a8f5225eb934b53e9c7febdbc680b9b  bootstrap/tests/_gate_transition.py
17007480162b0f4a100a100714a05198ef4a21ee8e726f31fb60b296127d429d  bootstrap/tests/_oracle.py
c719f770afe1b0ce5928923a7be2590666bc8f7935df2ad94eda95598be286e4  bootstrap/tests/_oracle_activation.py
e1d6c7db5d72729e43040dedb69fa47c50a3fe36b7d284ad73c1285b8a027007  bootstrap/tests/_oracle_trust.py
55cd6796a2e73efcf822b73284c3610a7c71adf67ee065ae11f06036568423af  dev/.cairn/allowed_signers
```

These hashes identify the rejected byte set; they are **not** a first-use
checklist to run. A correction to any member requires a fresh M2 hash set and
review.

### Exact manual bootstrap invocation reviewed

The exact command surface reviewed is the literal transition Stage 1 and
transition Stage 2 blocks in the runbook whose SHA-256 is recorded above, with
this complete host parameterization:

```text
CHECKOUT=/Users/kendal30/Code/cairn
CANDIDATE=HEAD
REVIEW_MANIFEST=/private/tmp/cairn-m2-review-manifest.txt
ENV=/usr/bin/env
GIT=/opt/homebrew/bin/git
PY=/Users/kendal30/conda_envs/lhm/bin/python3.13
MKTEMP=/usr/bin/mktemp
MKDIR=/bin/mkdir
SHASUM=/usr/bin/shasum
SORT=/usr/bin/sort
HOME=/Users/kendal30
SIGNING_KEY=/Users/kendal30/.ssh/cairn_signing.pub
PACKAGE_OUT=/private/tmp/cairn-gate-authorization-package.json
PACKAGE=/private/tmp/cairn-gate-authorization-package.json
```

The acquisition command reviewed, fully filled, is:

```sh
/usr/bin/env -i HOME=/nonexistent \
    /opt/homebrew/bin/git --no-replace-objects \
        -c core.useReplaceRefs=false \
        -c core.hooksPath=/dev/null \
        -c core.fsmonitor=false \
        -C /Users/kendal30/Code/cairn \
        cat-file blob refs/cairn/gate-anchor:bootstrap/REANCHOR_RUNBOOK.md
```

`CANDIDATE=HEAD` is bound once by the loader and must equal the full OID in the
out-of-band manifest. Stage 2's `CONFIRMED_SHA256` is necessarily the
Maintainer-entered digest printed by Stage 1, not a value knowable at review
time. This is an exact identification of the invocation under review by
runbook hash plus substitutions, not permission to execute it: **do not run
either transition block from this byte set.** There is no safe "filled-in
command we will actually run" to record while [M2-R1] remains open.

### Execution ledger and limits

All review execution used
`/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.13) with
`PYTHONDONTWRITEBYTECODE=1` in a clean detached clone. The seven authority test
files passed **423 tests in 117.61s**. Focused signing, transaction, transition,
and authorization classes passed **101 tests in 41.07s**; anchored-invocation
targeting passed **12 tests in 13.74s**. Collection reports **4013 tests**, which
matches Boundary B's 4008 pass + 4 fail + 1 skip record. I did not repeat the
full suite because the fresh Boundary B record targets these same implementation
bytes; this review used independent targeted falsification.

I did not load the Maintainer's real private key, move either Cairn ref, create
the real authorization package or review manifest, run the ceremony, push, run
TRU-7 against a real remote, exercise Windows or a SHA-256-format repository,
or audit Git/OpenSSH cryptography. The accepted evidence-stage host-access,
key-holder-not-process, and no-nonce replay residuals remain accurately
described and were not re-litigated.

## Response to the code review (M2 retake) -- Claude -- 2026-08-12

**[M2-R1] accepted. Not disputed, and the reproduction is exactly right.**

The transition loader validated the review manifest **against itself** — rows
well-formed, paths sorted and unique, digests matching the bytes it extracted
for those paths — and never compared the member set against a fixed list. So a
manifest that dropped a member or added one parsed cleanly, extracted cleanly,
and **started Python**. The first exact-set comparison was
`revalidate_transition()`, inside the candidate bytes the loader had already
selected and run.

The reviewer's framing is the part worth keeping: that is fail-closed for ref
movement and still wrong, because *a check performed by the candidate cannot
establish that the candidate was safe to start*. That is the one property this
loader exists to provide.

**And it survived because a comment stood in for a control.** The line
`# The extracted set must be EXACTLY the declared set` sat immediately above the
`$PY` invocation, describing a check that was not there. Every reader — me, and
an earlier review — took the comment for the mechanism.

### The correction

* **Nine literal paths, in `LC_ALL=C` order, in the fixed loader**, compared to
  the parsed set **before** candidate resolution, extraction, or Python.
* **Compared with the shell's own string equality** — no `cmp`, no `diff` — so
  **no utility is admitted to the residual trust set**. Of the two routes the
  review offered, this is the one that adds nothing to trust; the runbook states
  that explicitly rather than leaving it inferable.
* The misleading comment is replaced by one that says what happened.
* The prose paragraph claiming the loader established the member set is
  corrected in place with the finding named, since it asserted the property
  before the code supplied it.

### The evidence the review asked for

`test_a_wrong_member_SET_starts_no_interpreter`, parametrized over
**extra-member** and **missing-member**, replaces `$PY` with a **marker
wrapper** and requires the marker to be absent. Absence of a `Traceback` is not
evidence that no interpreter ran — that is how this passed before, and the node
says so. Both manifests are internally consistent: correctly sorted, uniquely
pathed, correctly hashed against a real commit, so only the fixed-set comparison
can reject them.

`test_the_marker_interpreter_probe_is_live` guards it: on an **honest** manifest
the marker must appear, so "refused early" cannot be confused with "never wired
up".

**Mutation-checked.** Removing the comparison reproduces the review's result
verbatim, in both directions:

```text
extra-member:   candidate Python STARTED before the fixed member set was checked
missing-member: candidate Python STARTED before the fixed member set was checked
```

### `_LOADED_MODULES` now represents the artifact it tests

It carried the **seven** importable modules while the authority closure contains
**nine** — `bootstrap/REANCHOR_RUNBOOK.md` (the instruction source, FUR7's own
subject) and `dev/.cairn/allowed_signers` (the roster the checkpoint signature is
verified against) were absent. Neither is imported, and not being imported is
exactly why their absence would not have announced itself.

It is now **derived from `declared_authority_closure()`** rather than retyped, so
the two cannot drift apart again, and
`test_the_loader_covers_the_whole_authority_closure` asserts equality with the
closure while keeping the original importable-subset property.

### What this response does not claim

* It does **not** close M2. These bytes differ from the reviewed
  `baa84b29353c946e2353f2b959e0b340da8c6cab`, so the recorded nine-file hash set
  in that review no longer describes them and a fresh exact-byte pass is owed.
* It does **not** arm M7, authorize M3, or discharge this plan's
  independent-read obligation.
* The loader still cannot establish **its own** authenticity. It remains an M2
  out-of-band trust input; the fixed member set makes it say what it always
  claimed, not more.

**Boundary B is owed again** on these bytes.
