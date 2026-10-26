# External Security Review — gate-anchor authority closure — Claude Opus 5 — 2026-08-27

**Verdict**: ADMIT IN PART

All three files' byte changes are admitted into the authority closure at the
digests named below. What is **not** admitted, and what no reading of these
three files could establish, is the end-to-end stage-1 → stage-2 handoff
property that one of the `bootstrap/reanchor.sh` hunks now depends on: its
correctness rests on `bootstrap/reanchor-launcher.template.sh`, which changed in
the same commit, is outside this review's scope, and — in the form the operator
actually runs — is outside the authority closure entirely. Details in the
`reanchor.sh` finding and in *What I could not reach*.

**Tier note.** Cairn's External floor is "a different agent type, or a human."
The Maintainer ruled that a different agent type cannot be staffed. This review
is therefore a same-agent fresh session and shares the implementing session's
model and priors. I have tried to compensate by attacking rather than
reconstructing: every claim I admit below is backed by a command I ran, a
positive control, or a byte comparison — not by finding the author's reasoning
persuasive. Two of my findings are defects in the implementing session's own
evidence.

### The five findings at a glance

None of them blocks admission. None is a weakening of the gate. Three are worth
fixing before the next ceremony.

| id | file | what it is | severity |
|---|---|---|---|
| M-1 | `_gate_manifest.py` | the `expect` beside the fixed command still says "0 skipped"; a real run reports 1 skipped, from a test parametrized over an emptied registry | fix before next ceremony |
| R-1 | `REANCHOR_RUNBOOK.md` | `:169` prints the artifact's own `stage2` and `:173` claims a re-extraction property that command does not have | fix before next ceremony; **predates the anchor** |
| S-1 | `reanchor.sh` | the new precheck runs two values-file executables before the configuration print the file's own comment says must come first | reorder; low |
| S-2 | `reanchor.sh` tests | two of the four claimed precheck test nodes are vacuous — they exercise `validate`, which has no precheck | fix the tests; evidence defect |
| S-3 | `reanchor.sh` | the printed stage-2 command is built from unvalidated, unquoted environment values | low; fails closed downstream |

---

## Range, and a mid-review complication

`HEAD` moved **five times** while I was reviewing:
`a1ea94ea01c447294383e879444160077f6e9120` (where I started) → `45e10d2` →
`ac5af7a` → `aa07cb1` → `a05350f` → `da58925` (where I committed this). One of
those commits, `ac5af7a`, edited `bootstrap/REANCHOR_RUNBOOK.md` — a file in
scope. I re-derived the review against each later commit rather than reporting a
range that no longer exists.

**This review therefore clears content digests, not a ref** — and the approach
held up under exactly the churn it was chosen for. All ten closure members hash
identically at `ac5af7a`, `aa07cb1` and `da58925`; only the first of those moves
touched anything in scope. A re-anchor run against any candidate is covered by
this review only if these three files hash to exactly these values there:

| closure member | sha256 of content (stable across `ac5af7a`…`da58925`) | git blob | git blob at anchor |
|---|---|---|---|
| `bootstrap/reanchor.sh` | `5400817a2566a230b969e65f606984db9036dd45e1c1d0845503e1301f3d9282` | `e5a043b1` | `4bf4489d` |
| `bootstrap/tests/_gate_manifest.py` | `94913bf309297ecdb04fcafe10bbbda27b74d1295c6d561a7f540573b4e0d544` | `0c2b719b` | `4f2e9fc0` |
| `bootstrap/REANCHOR_RUNBOOK.md` | `a861f5592d768358da0b9045d9f4a6d7f8dc050f9a778451efa4bd75df906d4d` | `a981d66a` | `8177f12c` |

The sha256 column is the one that matters: `check_authority_modules` in
`bootstrap/tests/_gate_preflight.py:1349-1386` admits a changed member only when
`admitted.get(rel)` equals the sha256 of the live bytes, so a review manifest
built from this review must carry those three hex strings.

Anchor: `5f992736adf76121e9f3ed53ba6d8e32ce7d8244`.

**The gate-anchor move is separately paused.** Commit `45e10d2` records the
Maintainer's finding that the ceremony's human leg is not real, and states the
move is paused on it. Nothing in this review lifts that pause. I return to it
below, because three of the four `reanchor.sh` fixes act entirely on that leg.

---

## The fact that carries the verdict

Seven of the closure's ten members are **byte-identical to the anchor**. I
compared each one:

```
UNCHANGED  bootstrap/tests/_gate_preflight.py
UNCHANGED  bootstrap/tests/_gate_reanchor.py
UNCHANGED  bootstrap/tests/_gate_transition.py
UNCHANGED  bootstrap/tests/_oracle_activation.py
UNCHANGED  bootstrap/tests/_oracle.py
UNCHANGED  bootstrap/tests/_oracle_trust.py
UNCHANGED  dev/.cairn/allowed_signers
```

Every check the ceremony performs **over the candidate** — the closure and
authority-module comparisons, the transition revalidation, the roster and
signature verification, and the two-ref transaction — lives in those seven
files. To be precise rather than sweeping: `bootstrap/reanchor.sh` does enforce
things, but only over its *own inputs* (the values-file schema, the path
predicates, the package-must-not-exist rule, and now the roster precheck). It
performs no check over the candidate commit and moves no ref; it validates
inputs, prints, and execs the checker.

So the question "does any of this widen what the gate admits" has a structural
answer before it has a line-by-line one: **the code that decides what may be
blessed did not change, and the three files that did change cannot relax a check
they do not implement.** I verified the line-by-line answer anyway, below.

---

## `bootstrap/tests/_gate_manifest.py` — ADMIT

Two hunks, `+7/−3`, from `15906df` and `6e2d98d`.

### Hunk 1 — `GATE_COMMANDS` gains an `env CAIRN_FULL_SUITE=1` prefix

**What changed.** The recorded `bootstrap-suite` command at
`bootstrap/tests/_gate_manifest.py:127-137` goes from
`python -m pytest bootstrap/tests/ -q` to
`env CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests/ -q`, plus a five-line
comment.

**The claimed rationale, tested rather than believed.** The claim is that the
bare form is refused with exit 4 before any test executes. I ran both.

Bare form:

```
$ PYTHONDONTWRITEBYTECODE=1 /Users/kendal30/conda_envs/lhm/bin/python3.13 \
    -m pytest bootstrap/tests/ -q
ERROR: Refusing a broad run: this invocation collected 3170 test(s) across
105 files (limit 40).
Run the tests your change actually maps to, or set CAIRN_FULL_SUITE=1 to allow
the full suite deliberately.
...
3 warnings in 3.94s
bare form exit=4
```

Zero tests ran — the summary line reports warnings only, and 3.94s is collection
time. Exit code captured separately as `4`. The guard fires in
`pytest_collection_finish` (`bootstrap/tests/conftest.py:337`), i.e. after
collection and before execution, with `BROAD_RUN_FILE_THRESHOLD = 40` at
`bootstrap/tests/conftest.py:89`. The claim is exact.

Override form — the recorded command, run verbatim under the canonical
interpreter:

```
$ PATH=/Users/kendal30/conda_envs/lhm/bin:$PATH PYTHONDONTWRITEBYTECODE=1 \
    env CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests/ -q
3169 passed, 1 skipped, 3 warnings in 610.43s (0:10:10)
override form exit=0
```

So the recorded command is one that actually runs and the previous one was not.
That is the defect the hunk fixes, and it is real.

**Does it change what the gate verifies?** No, and this is checkable rather than
arguable. `GATE_COMMANDS` has exactly two consumers, and both **emit** it:
`bootstrap/tests/_gate_manifest.py:474` writes `"gate_commands": GATE_COMMANDS`
into the produced manifest, and the preflight's independent re-derivation at
`bootstrap/tests/_gate_preflight.py:1594` writes `"gate_commands":
G.GATE_COMMANDS`. Nothing executes it. Both sides read the *same Python object*,
so the field cannot even be a source of disagreement between produce and
verify. It is inert recorded data addressed to a human.

**Attacked and not sustained.** I checked whether prefixing `env` changes
interpreter resolution — it does not: `env` resolves `python` through `PATH`
exactly as the shell would, so the pre-existing dependency on the operator's
`PATH` naming lhm/3.13 is neither introduced nor worsened. (On my shell `python`
resolves to a miniforge3 interpreter, not lhm; that is a pre-existing property
of the recorded command's `python` token, identical before and after this hunk,
and I note it only so it is not mistaken for a new defect.)

**Finding M-1 (recorded, does not block admission).** The hunk fixed the `cmd`
and left the `expect` string beside it untouched. That `expect` reads *"all
green; 0 skipped / 0 xfailed"*. The very first execution of the newly-runnable
command reports **1 skipped**, so the recorded expectation is falsified by the
recorded command sitting next to it.

**I chased the skip to its cause, and it is not host-conditional.** Re-running
with `-rs`:

```
SKIPPED [1] bootstrap/tests/test_reference_scripts.py:133:
            got empty parameter set for (module_name)
3176 passed, 1 skipped, 3 warnings in 581.32s (0:09:41)
```

`TestMultiScriptModules` is parametrized over `_MULTI_SCRIPT_MODULES`, which is
now `{}` (`bootstrap/tests/test_reference_scripts.py:70`) because the module it
existed for — the fold-back ledger — was retired in `e0b83b9`. The class
docstring still describes it as covering "fold-back-ledger's 2-script case". So
the property *"a module that ships more than one verbatim script gets all of them
installed"* is currently asserted by nothing, and the skip line is the only trace
of that. This is not a defect in the hunk under review and it is outside my three
files — but it is the concrete reason the recorded `expect` is now wrong, and it
is the kind of vacuity the removal sweep should be looking for.

The skip is deterministic, not a host difference, so the `expect` line is wrong
on any host until either the registry regains an entry or the class is retired
with the module it tested.

This is a consequence of the hunk in a precise sense rather than a pre-existing
defect the hunk inherited: while the command could not run at all, its
expectation was untestable and the mismatch could not surface. Making the command
runnable is what exposed it. Whoever operates the next ceremony will compare a
real run against that `expect` line and find it wrong.

**Call: ADMIT.** Inert data; the claimed rationale reproduced exactly; the stale
`expect` is a documentation defect in recorded data, not a check that can pass
when it should fail.

### Hunk 2 — a `PHASE_SPLIT_TARGETS` entry is dropped

**What changed.** The entry for the deleted lifecycle-metrics template module is
removed from the dict at `bootstrap/tests/_gate_manifest.py:107-117`, leaving
three entries.

**Does removing a phase-split target reduce coverage of anything still
present?** No — it can only *increase* coverage, and in this case it changes
nothing. `PHASE_SPLIT_TARGETS` is an **exclusion** set, not an inclusion one:
`bootstrap/tests/_gate_manifest.py:340` computes
`exclude = set(CASCADE_MUTABLE) | set(PHASE_SPLIT_TARGETS) | {_MANIFEST_REL}`
and subtracts it from the glob-discovered frozen surface. A member is a file
permitted to change without a HOLD. Removing a member therefore *narrows the
exemption* — the strict direction. Its second use, the `phase_mutable` map, is
guarded by `if (tree / rel).is_file()` on **both** the produce side and the
preflight re-derivation side, so a deleted path already contributed nothing to
either.

**The removal is required, not discretionary.**
`bootstrap/tests/test_gate_manifest.py:75` asserts
`set(produced["phase_mutable"]) == set(G.PHASE_SPLIT_TARGETS)`. Because `produce`
filters by `is_file()`, a stale entry for a deleted path makes the left side
smaller than the right and the assertion fails. Keeping the entry would have
reddened the suite.

**Confirmed the instrument rather than trusting the absence.** I verified the
module is genuinely gone rather than moved: `git ls-tree -r HEAD` returns no
`lifecycle_metrics` path, and the same command at the anchor returns 21. I then
enumerated the three surviving entries and confirmed each resolves to a file that
exists on disk — so no other dead exemption is hiding behind this one.

**Call: ADMIT.** Strictly narrowing, forced by the module deletion, no live path
loses coverage.

---

## `bootstrap/REANCHOR_RUNBOOK.md` — ADMIT

**What changed.** `+5/−2` across `b1e655d` and `ac5af7a`. A two-line HTML comment
header — a `claim-check-allow:` directive plus a note beginning `^` that pointed
at it — is replaced by a self-contained five-line note. The claim-check exemption
moved to a config file.

**Does it assert a control that does not exist?** No. I verified the exemption
survived the move with **unchanged scope**, and then confirmed the instrument
before trusting the result.

The config carries the runbook's two paths, keyed per-document, exactly as the
comment scoped them:

```
bootstrap/REANCHOR_RUNBOOK.md -> {'paths': ['dev/.cairn/trusted-activation.yml',
                                            'dev/.cairn/promotion-authorization.yml']}
```

In place, the checker is clean and names the exemptions:

```
$ python scripts/claim_check.py bootstrap/REANCHOR_RUNBOOK.md
claim_check: bootstrap/REANCHOR_RUNBOOK.md -- 2 path(s) exempted by claim-check-allow:
  ... exempted `dev/.cairn/promotion-authorization.yml` ...
  ... exempted `dev/.cairn/trusted-activation.yml` ...
claim_check: bootstrap/REANCHOR_RUNBOOK.md -- OK, no claim-check flags.
```

**Positive control.** A clean report is evidence only if the checker could have
flagged. I copied the identical bytes to a path the config does not name and re-ran:

```
claim_check: .../runbook_copy.md -- 2 hard flag(s):
  :453: [path] cited path does not resolve: `dev/.cairn/promotion-authorization.yml`
  :457: [path] cited path does not resolve: `dev/.cairn/trusted-activation.yml`
```

Same bytes, no exemption, exactly two hard flags. The mechanism is load-bearing
and the scoping is per-document as claimed, not a blanket waiver.

**The orphan was real and is already repaired.** The first commit removed the
directive and left the `^` note dangling — a note pointing at a deleted line. I
found it against the earlier `HEAD`; `ac5af7a` fixed it mid-review by making the
note name the two paths itself. I re-reviewed against the repaired bytes and
they read accurately.

**Call: ADMIT.** Prose, faithful, exemption scope verified unchanged with a
positive control.

**Finding R-1 (recorded, does not block admission).** The runbook contains a
contradiction about the most consequential operator step, and it now conflicts
with the code I am admitting alongside it. `bootstrap/REANCHOR_RUNBOOK.md:169`
prints, as *the command that signs*:

```
sh bootstrap/reanchor.sh stage2 <values> --confirm-package-sha256 <the digest you computed>
```

and `:173` then asserts that "stage 2 re-extracts and re-verifies its own bytes
rather than reusing stage 1's." **That assertion is false for the command
printed directly above it.** Re-extraction into a fresh directory is a property
of the *launcher's* `--stage2` path, not of invoking the artifact's own `stage2`
subcommand — which is exactly what `:305` says, and what `reanchor.sh` now warns
against in its own output. So the file states a control that does not hold for
the invocation it hands the operator.

I am admitting it anyway, and the reason is decisive rather than lenient: **both
lines are already in the anchor.** I confirmed they exist verbatim at
`5f992736` (as `:166` and `:302` there). Refusing the new bytes would not remove
the false claim from the trust root — it is already blessed — and would strand
the exemption repair. The defect predates this delta and should be fixed before
the next ceremony, but it is not something this admission creates.

---

## `bootstrap/reanchor.sh` — ADMIT (with three recorded findings)

`+97/−10`, all from `d091cdd`. Four operator-surface fixes. I read every changed
line.

### The three structural questions, answered first

**Does any of it alter the two-stage boundary?** No. Stage 1 still invokes the
checker through `"$V_env" -i PATH=... HOME=... "$V_python" -E -s "$CHECKER"`
with **no `SSH_AUTH_SOCK`** (`bootstrap/reanchor.sh:511-515`), and stage 2 is
still the only place it is forwarded (`:643-647`). Neither line is in the diff.
The asymmetry that *is* the boundary is untouched.

**Does any of it touch the compare-and-swap on the ref?** No — and it could not.
`reanchor.sh` contains no ref-moving code at all; it builds an argument list and
execs the checker. The two-ref transaction lives in `_gate_reanchor.py`, which I
verified is byte-identical to the anchor.

**Does stage 2 lose the transition when the printed command drops
`--review-manifest`?** This was my sharpest concern about hunk 2, and the answer
is that it fails closed. `bootstrap/tests/_gate_preflight.py:3057-3068` refuses
outright when the package authorizes a reviewed-authority transition and stage 2
was given no `--transition-from-review`: *"A transition cannot be signed as
steady state."* The converse is refused too. So an operator who follows the new
printed advice and reaches stage 2 without a manifest gets a refusal, never a
silent steady-state signature over a closure change.

### Hunk 1 — stage 1 refuses a signing key the anchored roster does not name

**What changed.** A new block at `bootstrap/reanchor.sh:431-478` reads the
`signing_key` `.pub` with the recorded `cat`, reads
`refs/cairn/gate-anchor:dev/.cairn/allowed_signers` with the recorded `git` under
`env -i`, and refuses if the `keytype keydata` pair is absent from the anchored
roster.

**This is purely additive.** It creates a refusal; it removes none. I confirmed
the downstream enforcement it front-runs is unchanged — the checker's own
`validate_signing_key`, the principal check, and the `%G?` verification all live
in `_gate_preflight.py`, byte-identical to the anchor. So even a hypothetical
false *accept* in this precheck grants no authority: it only means the operator
learns later rather than sooner, which is the status quo ante.

**It reads the anchor, not the worktree** — the distinction that makes it
meaningful during a rollover, when those two deliberately differ. Verified in the
source (`cat-file blob refs/cairn/gate-anchor:...`), and the git child is
hardened consistently with the checker's own `_sterile_env`: `--no-replace-objects`,
`core.useReplaceRefs=false`, `core.hooksPath=/dev/null`, `core.fsmonitor=false`,
and — the one that matters most — `GIT_NO_LAZY_FETCH=1` bound rather than
inherited, which is the promisor-remote hole `bootstrap/SAFETY.md` Rule 13
documents. Under `env -i`, absent means enabled; the author bound it.

**No key material reaches output.** The refusal message prints `$V_signing_key`
(the path) only. There is no `set -x`, and the roster contents never enter a
message. I checked this specifically because the block is the first thing in the
artifact to read a key file.

**Degenerate inputs, probed.** Missing anchor ref → refuse. Missing roster blob →
refuse. Empty roster → refuse. Private key supplied instead of a `.pub` → refuse
(with a misleading-but-safe message). All fail closed. I did find one contrived
false-accept: an **empty** `signing_key` file combined with a **whitespace-only**
roster line makes both extracted fields empty on each side and they compare
equal. It grants nothing — the anchored roster is signed content, and the
downstream checks are unchanged — but it is the one input pair where the
comparison does not fail closed, and a `[ -n "$_s1_keytype" ]` guard would close it.

**Two injection paths I went looking for and did not find.** The roster is fed to
the parse loop through an **unquoted** heredoc delimiter, which makes the heredoc
body subject to parameter expansion, command substitution and arithmetic
expansion — so a roster line containing `$(...)` or backticks was the obvious
attack. It does not fire: the body is the single token `$_s1_anchored`, and the
*result* of a parameter expansion is not re-scanned for further expansions, so
roster bytes are inserted literally. Separately, `refuse` is
`printf 'REFUSE: %s\n' "$*"` with a literal format string, so the values-file
path it interpolates cannot become a format specifier.

**Fragility worth naming.** The roster parse assumes `principal keytype keydata`.
An `allowed_signers` line carrying options (`namespaces="git"`) or a
`@cert-authority` prefix would misparse and cause a **false refusal**. That is
the safe direction, but it would strand a ceremony, and the current roster's
shape is the only reason it works.

**Is Rule 13 engaged?** No. `bootstrap/SAFETY.md` Rule 13 enumerates the
**pre-candidate** trust set — what the launcher runs *before* candidate code
starts. This block runs inside candidate code, after the artifact has been
started. `env`, `git` and `cat` are all already in that table and already
validated by `reanchor.sh`'s own `require_executable`. The point at which
candidate code starts is unchanged.

**Finding S-1 (recorded, does not block admission).** The block executes two
values-file executables — `cat` and `git` — **before**
`print_effective_configuration`. That function's own comment at
`bootstrap/reanchor.sh:309-313` states: *"The contract requires the Maintainer to
see what will be used before stage 1."* At the anchor, nothing from the values
file executed before that print; now two things do. I verified this is a change
of fact, not a misreading: at the anchor `$V_git` and `$V_cat` were validated and
printed but never actually invoked by the artifact.

I do not refuse the hunk over it, for a reason I checked rather than assumed:
the print is **not a blocking gate**. `cmd_stage1` prints and proceeds in the
same breath, with no prompt, so the operator never had an opportunity to
interpose between disclosure and execution. Both binaries pass
`require_executable` (absolute, symlink-free on every component, regular,
executable) before use. The fix is a reorder — move the roster block to just
after the print — and it costs nothing.

**Finding S-2 (defect in the implementing session's evidence).** The commit body
claims "Four new nodes on the precheck, including that it refuses BEFORE writing
a package and that it reads the anchor rather than the worktree." I ran them:

```
$ python -m pytest bootstrap/tests/test_reanchor.py -q \
    -k "TestStage1RefusesAKeyTheAnchorDoesNotName"
4 passed, 185 deselected in 1.11s
```

The two **refusal** nodes are sound. The two **accept-path** nodes are vacuous.
`test_the_roster_key_is_accepted` (`bootstrap/tests/test_reanchor.py:2064`) and
the second half of `test_the_check_reads_the_ANCHORED_roster_not_the_worktree_copy`
(`:2070`) both assert success from `_run("validate", ...)` — and `validate` never
executes the precheck. The dispatch at `bootstrap/reanchor.sh:866-874` routes
`validate` to `parse_values` + `print_effective_configuration` + an `OK` line;
the precheck exists only inside `cmd_stage1`. Both nodes would pass unchanged if
the precheck rejected every key on earth.

Their docstrings assert the opposite — *"so the node above is not passing because
every key refuses"* and *"the old key was rejected; the check is reading the
worktree copy rather than the anchor"* — which is the "confirm the instrument
before trusting a result" discipline stated and then not performed. The
consequence is bounded: a false-refusal regression in the precheck would not be
caught, which is an availability risk to the ceremony, not a weakening of it.
Changing `validate` to `stage1` in both nodes would fix it.

### Hunk 2 — stage 1 prints the launcher's stage-2 command, not its own

**What changed.** `bootstrap/reanchor.sh:534-559`. The old block printed
`sh $0 stage2 ...` (plus `--review-manifest`/`--reviewed-candidate` in transition
mode). The new block prints the launcher invocation with `--stage2 <digest>` when
`CAIRN_LAUNCHER` and `CAIRN_PACKET` are set, and generic "run YOUR LAUNCHER"
advice otherwise.

**This is a `printf` change and nothing else.** I grepped: `CAIRN_LAUNCHER`,
`CAIRN_PACKET` and `CAIRN_CANDIDATE` appear in `reanchor.sh` at `:543-547` only,
all inside `printf` arguments. Nothing decides on them. `cmd_stage2` is untouched
and still reachable.

**The printed command is arity-correct.** The launcher's stage-2 entry is
`[ "$#" -eq 5 ] && [ "$4" = "--stage2" ]` at
`bootstrap/reanchor-launcher.template.sh:436`; the printed form supplies packet,
values, candidate, `--stage2`, digest — five arguments with `--stage2` fourth. It
matches.

**The direction of the change is toward the stronger property**, and the
guidance it replaces was wrong: sending the operator to `$0 stage2` reuses the
directory candidate code just ran in, which is precisely what the launcher's
`--stage2` path exists to avoid.

**Finding S-3 (recorded, does not block admission).** The values come from the
**environment**, and the artifact inherits the operator's environment. Stale
`CAIRN_*` exports left over from an earlier session would make stage 1 print a
*stale* launcher, packet and candidate while asserting "same launcher, same
packet, same values." They are also printed unquoted, so a value containing a
newline could forge additional lines in the instruction block.

I checked whether this can produce a bad signature and it cannot: the launcher's
`--stage2` path re-verifies everything from scratch — re-resolves the candidate,
re-verifies every closure blob, re-extracts, re-checks the artifact digest, and
compares the packet against the digest bound into itself. A wrong packet or
candidate produces a refusal, not a signature. The hazard is misdirection and
wasted attempts, not authority. Quoting the values, or having the launcher pass
them as arguments rather than environment, would close it.

### Hunks 3 and 4 — passphrase guidance, and naming a missing agent

**What changed.** Stage 1 gains three `printf` lines telling the operator to
DECLINE a passphrase prompt (`bootstrap/reanchor.sh:504-506`); stage 2 gains four
telling them to ENTER it (`:634-637`); and stage 2 gains an informational note
when `SSH_AUTH_SOCK` is unset (`:602-617`).

**Verified inert.** The `SSH_AUTH_SOCK` note is a read in a test expression that
gates a `printf`; the forwarding at `:643-647` is unchanged. The comment is
explicit that it is a note rather than a refusal, and the code matches the
comment. Stage 1's advice is semantically correct: stage 1 must *fail* to sign,
so a passphrase prompt is the control working and answering it defeats it.

**Call on the file: ADMIT.** No hunk widens what the gate admits, relaxes a
refusal, or makes a check reachable in fewer cases. Three findings recorded, none
of which is a weakening.

---

## The Maintainer's pause, and why it lands on this file

Commit `45e10d2` records that the ceremony's human leg is not real: if an agent
composes the instructions and the Maintainer executes them, the agent is blessing
its own verifier through a human relay. **Three of the four `reanchor.sh` fixes
are changes to that leg** — what the artifact tells the human to type, and what
to do at a prompt. Hunks 2, 3 and 4 alter no machine-checked property whatever;
their entire claimed benefit accrues to a control the Maintainer has just
declared non-functional.

I admit them because they weaken nothing and are strictly better instructions
than the ones they replace. But their *value* is contingent on a disposition the
Maintainer has not yet made, and this review should not be read as evidence that
the human leg works. It is evidence only that these bytes do not make it worse.

---

## What a launcher/packet pair produced from this review would have to bind

1. **All ten closure members in the manifest's `members` map — not the three that
   changed.** I initially had this wrong and checked it:
   `revalidate_transition` computes
   `declared = set(declared_authority_closure())` and refuses unless
   `set(manifest["members"]) == declared`, reporting the missing and unexpected
   entries. A manifest naming only the changed three would be refused as "not
   the authority closure". Each entry is the sha256 of that member's blob **at
   the candidate**, bare hex, and each is re-derived and compared. At `aa07cb1`
   those are:

   | member | sha256 at the candidate |
   |---|---|
   | `bootstrap/tests/_gate_preflight.py` | `8a6de3efc1e9e5a5e4a683556ed058b81bb30ca2264552444e03077167af6e06` |
   | `bootstrap/tests/_gate_manifest.py` | `94913bf309297ecdb04fcafe10bbbda27b74d1295c6d561a7f540573b4e0d544` |
   | `bootstrap/tests/_gate_reanchor.py` | `3cd5d39ec6b64296557bda4ee41d838158c40e89699fc6b3372f4c412466be7c` |
   | `bootstrap/tests/_gate_transition.py` | `545625aea1d229d3977abd52118151477caf1bc5d87479d2e0a3cc08436bca17` |
   | `bootstrap/tests/_oracle_activation.py` | `f8f94efa73eea79d6b366f280024d2bace4d13b4b111f12c65d9ae0f85c9d2c4` |
   | `bootstrap/tests/_oracle.py` | `afc9951ecbbc2693caba76ad14843d4d38560e1c524dddbad37e04e1c3896bed` |
   | `bootstrap/tests/_oracle_trust.py` | `725692f9ad21f1276532dcba7ae49ed307fbd9c18bfdc25212fb048de0c63f42` |
   | `bootstrap/REANCHOR_RUNBOOK.md` | `a861f5592d768358da0b9045d9f4a6d7f8dc050f9a778451efa4bd75df906d4d` |
   | `bootstrap/reanchor.sh` | `5400817a2566a230b969e65f606984db9036dd45e1c1d0845503e1301f3d9282` |
   | `dev/.cairn/allowed_signers` | `8b7fa2f745f187cc06316732a27a2d9f552a6244d57393d95dd3e1a8e923c242` |

   The launcher composes this itself, so nobody hand-writes it. The table is here
   so the Maintainer can check that it composed the right one.

2. **A non-empty anchor→candidate delta that is exactly the three files this
   review clears.** `revalidate_transition` refuses outright when
   `authority_closure_delta(anchor, reviewed_candidate)` is *empty* — the mode
   exists only to carry a closure change — so this is a transition-mode pair and
   cannot be reused for a steady-state run. On the other side,
   `check_authority_closure` and `check_authority_modules` admit a *changed*
   member only when `admitted[rel]` equals the live sha256, so a fourth changed
   member that this review never saw would surface as a `CLOSURE`/`AUTHORITY`
   refusal rather than riding along.
3. **A candidate OID whose tree carries those exact three digests**, and at which
   the other seven closure members are still byte-identical to `5f992736`. This
   is not boilerplate. `HEAD` moved **three times** while this single review was
   in progress — `a1ea94e` through `da58925`, five moves — and one of those
   commits edited a file in scope. Another renamed a `scripts/*.py` that
   the frozen-file glob covers. The candidate must be pinned and quiesced before
   the ceremony starts, not read as "whatever `HEAD` is."
4. **The artifact digest for `bootstrap/reanchor.sh` = the `5400817a…` value
   above**, since the launcher verifies the extracted artifact against a digest
   bound into itself at review time.
5. **A `signing_key` naming a key the *anchored* roster carries.** The new
   precheck now enforces this in the first second; binding a values file that
   contradicts it wastes the ceremony rather than endangering it.
6. **Nothing about `bootstrap/reanchor-launcher.template.sh`.** Its `+10`
   `CAIRN_*` export is outside the closure and outside this review. An
   instantiated launcher lacking it degrades to the generic-advice branch, which
   is safe; a launcher carrying it must still be verified by its own digest
   against its own External review record, not against this one.

---

## Verification runs

| what | command | outcome |
|---|---|---|
| broad-run guard, bare form | `python -m pytest bootstrap/tests/ -q` | exit 4, 0 tests executed, 3.94s |
| broad-run guard, recorded form (at `ac5af7a`) | `env CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests/ -q` | exit 0, 3169 passed / 1 skipped, 610.43s |
| same, re-run with `-rs` (at `aa07cb1`) | as above plus `-rs` | exit 0, 3176 passed / 1 skipped, 581.32s; skip named |
| roster precheck nodes | `pytest bootstrap/tests/test_reanchor.py -k TestStage1RefusesAKeyTheAnchorDoesNotName` | 4 passed, 185 deselected, 1.11s |
| claim-check, in place | `python scripts/claim_check.py bootstrap/REANCHOR_RUNBOOK.md` | OK, 2 paths exempted |
| claim-check, positive control | same bytes at an unexempted path | 2 hard flags — instrument confirmed |
| closure members | blob comparison, anchor vs `ac5af7a` / `aa07cb1` / `da58925` | 7 unchanged, 3 changed as scoped, identical at all three |

Interpreter: `/Users/kendal30/conda_envs/lhm/bin/python3.13` (3.13.x),
`PYTHONDONTWRITEBYTECODE=1`.

I did not run the ceremony. No `stage1`, no `stage2`, no `update-ref`, nothing
touching `refs/cairn/*` or any key. I ran one `git update-index --refresh` while
establishing that a `git status` entry for the runbook was stat-dirty rather than
a content change; it updates the index stat cache only and altered no content.

---

## What I could not reach

* **The end-to-end stage-1 → stage-2 handoff.** Hunk 2's correctness depends on
  the *instantiated* launcher, which is produced per-ceremony out of band, is not
  in the authority closure, and was not available to me. I verified the printed
  command's arity against the shipped template and verified the fail-safe
  branch — I did not observe a real handoff. **This is the "in part" in my
  verdict.**
* **The `+10` delta to `bootstrap/reanchor-launcher.template.sh`**, which landed
  in the same commit as the `reanchor.sh` changes and which hunk 2 consumes. I
  read it and it is presentation-only, but it is outside my assigned scope and I
  did not review it as an artifact.
* **Empirical falsification of finding S-2.** I established the two accept-path
  nodes are vacuous by reading the dispatch and the test harness — `_run` execs
  `/bin/sh bootstrap/reanchor.sh <cmd>`, and the `validate` case contains no call
  into `cmd_stage1`. I did **not** demonstrate it by mutation, because doing so
  would have required editing an implementation file. The source reading is
  unambiguous, but it is a reading, not a measurement.
* **The empty-pub / whitespace-roster-line false accept.** Derived by reading the
  shell parameter expansions, not constructed and run.
* **The rollover path end to end.** I did not perform or simulate a key rollover,
  which is the scenario the new precheck is built for.
* **Whether the human leg is real.** Explicitly out of scope for a byte review,
  and the subject of the Maintainer's own open finding in `45e10d2`. I can say
  these bytes do not degrade it; I cannot say it functions.
* **Anything outside the three assigned files.** In particular I did not review
  `scripts/correct_pinned_digests.py` or
  `bootstrap/tests/test_correct_pinned_digests.py`, which landed mid-review (and
  were renamed mid-review) and which the frozen-file glob covers. They are not
  closure members, so they do not bear on this admission — but they do mean the
  gate manifest surface moved while I was working.
* **A stable tree.** My two full-suite runs were against different commits and
  report different totals (3169 and 3176 passed) because tests were added under
  me. Neither figure is a baseline anyone should carry forward; they are evidence
  about the *guard*, not about the suite.
* **Independent corroboration.** Per the tier note, this is a same-agent fresh
  session. Where I agreed with the implementing session's reasoning, that
  agreement is weak evidence and I have tried to rest the verdict on the byte
  comparisons and the reproduced commands instead.
