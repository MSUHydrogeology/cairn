# External Security Review -- `correct_pinned_digests.py` -- Codex -- 2026-08-27

**Reviewer**: Codex (External Security)
**Implementing agent**: Claude Opus 5
**Reviewed commit**: `aa07cb1c5aa617e1b8a4fe3923f27c8c3745ba92`
**Reviewed paths**:

* `scripts/correct_pinned_digests.py`
* `bootstrap/tests/test_correct_pinned_digests.py`

The review request used the files' pre-rename names. I applied the requested
substitutions and reviewed the current bytes. Their SHA-256 values are:

```
a3bb3aa146d1b55a10e85c174ca3603471e5a3e29e6665ec65c323f11ba932a8  scripts/correct_pinned_digests.py
cffc0c057d85999ec9ba3dbde5c4ff1d5a1904dd4de08b44ba072338b81c3a93  bootstrap/tests/test_correct_pinned_digests.py
```

**Verdict: BLOCK. Do not use this runner to correct either trust artifact.**

The time-separated A/B comparison is real but substantially narrower than the
security claim made for it. It detects a mutation only when that mutation
changes the plan's current projection. It does not authenticate a human, does
not bind all state that will be written, does not independently reload one of
its principal inputs, and does not make the write all-or-nothing. I reproduced
paths where a non-human applies, A equals B across a material tree change,
undigested state is written, candidate code executes before authorization, a
symlink redirects the write, and an I/O failure leaves invalid partial JSON.

The central human step is therefore still a formality. The checksum is useful
as a transcription and state-binding device after the plan is made complete;
it is not evidence of who approved it or that they read it.

## Findings

### CPD-1 -- `--authorize` lets any process perform the purported human act [CRITICAL, BLOCKING]

`scripts/correct_pinned_digests.py:313-316` explicitly accepts the digest prefix
as a command-line argument when no terminal is present. A process can obtain
the digest from one refused non-interactive run, parse the `PLAN DIGEST` line,
and run again with `--authorize`. It can also import the module and calculate
the digest directly. Removing the flag alone would not authenticate a human:
an agent can allocate a pseudo-terminal and answer `input()`.

I exercised the direct path with a non-TTY stdin, the correct digest, and a
recording apply function. `main()` returned 0 and applied. This is not a
hypothetical objection to `isatty`; it is the supported branch.

The TTY check stops only the literal spelling `yes | tool`. It does not stop a
wrapper, an agent, an expect-style process, or any other program capable of
reading eight characters from stdout. Because agents and the Maintainer run as
the same OS user with the same shell capabilities, this process cannot infer
human identity from stdin.

**Required disposition.** Choose one honest contract:

1. Treat confirmation as a doctrinal Maintainer step and state that the runner
   binds state but does not authenticate the confirmer. Rename `--authorize`
   to `--confirm-plan-digest` and stop citing TTY presence as a security
   boundary; or
2. Require a capability agents do not possess, such as a separate-account or
   hardware-backed signature/physical confirmation, and verify it against a
   trust root outside the tree being corrected.

There is no same-account command-line construction that proves a person read
the plan. Continuing to call this branch human authorization is not available.

### CPD-2 -- The digest does not bind the complete preimage or output, so a wrong state can pass A == B [CRITICAL, BLOCKING]

For the lockfile, `plan_lockfile()` returns only `remove`, `add`, and the record
count. It omits the header, top-level fields, every kept record, the exact input
bytes, and the exact output bytes. `apply_lockfile()` then re-reads the live
document and carries all omitted content into the write. Its only concurrency
check is `len(records) == plan['before']` at lines 255-256.

I built two lockfile states with the same count and the same removal/addition
set. Between derivations I changed a kept record's hash and the top-level
schema. The two plan digests were identical. Apply wrote the changed hash and
schema. The operator's digest authorized neither value.

The AST path has the same second-window defect. Its plan contains only changed
rows. `apply_ast_baseline()` re-reads the complete baseline, updates those rows,
and writes every other row as currently found. I changed an unplanned symbol's
digest and span after derivation without changing the number of baseline
symbols. Apply preserved the unauthorized mutation. The `len(baseline) !=
before` test compares an in-memory dictionary with itself before and after
value updates; it is not a compare-and-swap against the authorized baseline.

The A/B check therefore detects only changes visible in the projected delta.
The smaller B-to-write window also matters: both apply functions consume live
state after B without an exact-preimage check, and the engine/template inputs
can move after B while stale digests are written.

**Required disposition.** The plan must bind, at minimum:

* the exact input artifact bytes and SHA-256;
* every source input and its SHA-256 (engine modules, checker, mapping source,
  templates and destination files, known-new manifest, and relevant HEAD);
* the complete canonical output bytes and SHA-256; and
* the exact semantic diff rendered to the operator.

Immediately before replace, compare the live artifact and every source input
to those authorized preimages. A count is not a preimage. Derive the output
only from the bound snapshot, never from a third live read.

### CPD-3 -- Re-derivation reuses imported candidate code, and candidate code executes before authorization [HIGH, BLOCKING]

`plan_lockfile()` executes `from _scaffold import config as C` at lines
215-217. Importing that submodule first executes `_scaffold/__init__.py`, whose
documented eager facade loads the rest of the scaffold engine. These are the
candidate engine bytes whose trust artifacts may be under correction. The
path-verifying import guard proves location, not provenance or harmlessness.
Candidate code therefore runs with the Maintainer's process privileges before
the plan is displayed or confirmed.

The import is also cached in `sys.modules`. The second call to `plan_lockfile()`
does not independently read a changed `config.py`; it reuses the first module's
`_SKILLS_MAPPINGS` object. In a scratch package I made config write a marker at
import, derived plan A with one mapping, changed the source to two mappings,
and derived B. Candidate code had executed before authorization, B still saw
one mapping, and A's and B's digests were identical.

`plan_ast_baseline()` likewise reuses the imported `_ast_attest` module across
the two calls, although its engine module reads are live. A change to the
checker itself is not independently reloaded.

**Required disposition.** Do not import unverified candidate packages into the
authority process. Parse the required mapping from a closed data format or a
strict AST reader, or execute candidate-derived evidence in an explicitly
untrusted stage whose output is fully checked by pinned code. Perform B in a
fresh process from independently verified checker bytes so module caches cannot
make A and B aliases.

### CPD-4 -- Writes follow symlinks and can leave a partial trust artifact [HIGH, BLOCKING]

Both apply functions end in direct `Path.write_text()` calls. Neither checks
the target or parent chain for symlinks, writes to a same-directory temporary,
fsyncs, atomically replaces, or reads the result back. `main()` catches only
`Refusal`; an `OSError` or interruption during the write escapes as a traceback.

I redirected the baseline path through a symlink and confirmed that apply
wrote the symlink target. I also supplied a writer that truncated the artifact,
wrote one third of the output, and raised `OSError`. The exception escaped and
the remaining artifact was invalid JSON. The failure is neither total nor
converted into a refusal, and it falsifies the test module's broader claim that
a correction cannot half-apply.

**Required disposition.** Refuse a symlink at the leaf or any parent and verify
containment. Write a mode-preserving temporary in the artifact's own directory,
flush and fsync it, atomically replace the exact checked regular file, fsync the
directory where supported, and read back the expected output digest. Preserve
the old artifact on every failure before replace.

### CPD-5 -- The rendered plan omits consequences and can name the wrong provenance [HIGH, BLOCKING]

The operator can authorize only what the render makes comprehensible:

* `render_ast_baseline()` does not display the span that apply writes.
* `render_lockfile()` shows only `dst` (and one `living_state` hint) for a
  removed record, not the full record being deleted. It does not show added
  hashes, top-level changes, kept-state hash, or complete output hash.
* AST provenance uses `git log -1 -S <name>`. Pickaxe `-S` finds a commit that
  changes the count of that string, commonly the symbol's introduction, not a
  later body change that altered its digest.

The provenance failure reproduces against the 15-symbol correction immediately
preceding this tool. For `FunctionDef:_compute_upgrade`, the command the runner
uses returns `ed5a670` from 2026-06-10. The baseline anchor was `77d2b3b`, and
the commit touching `upgrade.py` between that anchor and correction was
`bec2cca` on 2026-08-25. The rendered instruction "Read those commit subjects:
they are what you are authorizing" can therefore point the Maintainer at a
commit outside the relevant range while omitting the relevant one.

**Required disposition.** Render the complete semantic diff and complete
records, full old/new digests, spans, input/output hashes, and every commit in
the baseline-anchor-to-HEAD range that touched the containing file. Do not call
`-S <name>` a trace to the digest-changing commit. If exact symbol provenance
cannot be derived reliably, say so and present the conservative file history.

### CPD-6 -- The AST path drops the existing known-new complete-set guard [HIGH, BLOCKING]

`plan_ast_baseline()` receives `_new` from `_ast_attest._classify()` and ignores
it. It never reads `scaffold_ast_known_new.json`. The existing attestation
procedure requires complete-set equality by digest and multiplicity because a
new top-level symbol is outside the baseline and can otherwise change or vanish
without appearing as CHANGED. That is the load-bearing reason for Step 2 and
precondition 4 in `bootstrap/AST_BASELINE_RUNBOOK.md`.

A Maintainer direct correction may legitimately cover multiple CHANGED symbols
outside the four-symbol self-service allowlist. It does not follow that the
independent known-new guard may disappear. The runner can correct every visible
CHANGED baseline row while unrelated new top-level logic remains unverified.

**Required disposition.** Reuse or reproduce `_ast_attest`'s complete-set
known-new check from independently trusted bytes and bind the manifest plus its
live comparison into the plan. Multi-symbol Maintainer authority is not an
allowance to drop an orthogonal invariant.

### CPD-7 -- Git is a load-bearing oracle but errors fail open as "untracked" [MEDIUM, BLOCKING]

`_tracked()` returns false for every nonzero `git ls-files` result. That
collapses the expected untracked result together with repository errors,
permission failures, a substituted executable, and malformed options. It also
passes the candidate-derived path without a `--` option terminator. A Git
failure can therefore convert "unknown" into "safe to remove".

The three Bandit reports reproduced exactly: B404, B603, and B607, all LOW.
B404/B603 are appropriately low here because the command uses an argv list and
no shell. The existing blanket acceptance of B607 is not sufficient for this
runner's new role: Git decides whether a lockfile record is deleted and which
commit subject the operator reads. A PATH-substituted Git is an authority
substitution, not merely a tooling residual.

**Required disposition.** Resolve and validate the Git executable under an
explicit host-trust rule, record it in the plan, add `--` before paths, and
distinguish the one expected "not tracked" status from every execution error.
Every unexpected return code refuses with stderr. This is separate from the
accepted no-shell Bandit findings.

### CPD-8 -- Two claims are overbroad, though neither is the current exploit [LOW, NON-BLOCKING]

`plan_digest()` uses `json.dumps(..., default=str)`. The current plans contain
JSON-native values, and I found no current native-type mutation that changes an
apply-consumed field without changing the digest. But `default=str` silently
collapses a future custom value with a string having the same presentation; I
confirmed such a collision. A trust-plan schema should reject non-JSON values,
not stringify them.

The lockfile header is preserved for the repository's current LF-terminated
bytes (411 bytes, reproduced). It is not universally byte-for-byte: `read_text`
normalizes CRLF and apply writes LF. A CRLF scratch header changed bytes. Either
state the current-format precondition and refuse anything else, or manipulate
the prefix as bytes.

## Test assessment

The seven dedicated tests pass. The moving-plan test is honest within its
narrow model: if the A/B digest comparison is neutralized, its recording apply
is reached and the test fails; the stable-plan control proves the suite is not
green merely because all paths refuse.

What the tests model is the weakness. Both plans are injected as already-built
small dictionaries, and both apply functions are replaced with lambdas. No test
derives twice from changing real inputs, writes a scratch artifact, compares
pre/post bytes, injects a write failure, swaps a symlink, changes a same-count
record, changes imported config between A and B, checks known-new, or validates
the render against the complete output. The test module's opening total-write
claim is therefore not pinned by the suite.

The real-tree smoke test proves only that planning returns 0 or 2 without a
traceback. It does not verify the plan, render, authorization, or write.

## Recommended redesign

The useful core can survive, but the authority and state-binding questions must
be separated:

1. **State binding:** construct one closed, JSON-native plan containing exact
   input hashes, exact output bytes/hash, source closure, HEAD, and complete
   diff. Render that same object.
2. **Independent re-derivation:** rebuild it in a fresh process from verified
   checker bytes, without importing candidate packages. Compare full digests.
3. **Authorization:** either verify an out-of-band Maintainer capability or
   call the typed value confirmation, not human authentication.
4. **Commit:** exact-preimage compare-and-swap into a regular contained path,
   using atomic replacement and read-back verification.
5. **Evidence:** add public-path tests for every reproduced failure above,
   including controls that prove a guard has not simply become refuse-all.

The operator can still have a simple experience: read one complete diff and
confirm one digest. The machinery beneath that experience must make the digest
cover the state actually written, and the record must be honest about who the
tool can and cannot authenticate.

## Coverage

**Executed:** the seven dedicated tests; the dedicated suite plus
`test_security_lint.py` and `test_gate_manifest.py` (39 passed, canonical Python
3.13.13); Bandit over the runner (three LOW findings: B404/B603/B607); scratch
public-function probes for non-TTY authorization, same-plan lockfile drift,
same-count baseline drift, cached config, pre-authorization candidate execution,
symlink following, partial write, strict-JSON collision, current-header
round-trip, and CRLF-header mutation; and a positive provenance comparison
against the prior 15-symbol correction.

**Read:** both reviewed files in full; `bootstrap/_scaffold/__init__.py` and
`config.py`; `_ast_attest.py`'s classifier, allowlist, and known-new checks;
`bootstrap/AST_BASELINE_RUNBOOK.md`; the current security strategy entries for
fixture correction and human authorization; and commits `ac5af7a`, `aa07cb1`,
`d283589`, `77d2b3b`, and `bec2cca`.

**Not exercised:** no real repository trust artifact was written; no full suite,
gate-anchor ceremony, re-anchor, Windows filesystem, crash/power-loss injection,
or hostile real Git executable was used. I did not review the separate untracked
authority-closure review artifact, and I did not modify it.
