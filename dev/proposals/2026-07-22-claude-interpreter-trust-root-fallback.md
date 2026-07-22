<!-- Defensive: the dangling-internal-ref gate runs only on template-instruction surfaces, so this marker is inert for a dev/proposals/ file (parent proposal, R10c). Kept for consistency with the doctrine-citation convention. -->
<!-- cairn-internal-ref-allow: doctrine/runtime-contract.md doctrine/rationale.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
<!-- Forward-reference paths this proposal plans to create; they materialize at plan-open, at Security Review, and at archive. -->
<!-- claim-check-allow: dev/plans/interpreter-trust-root-fallback.md, dev/reviews/2026-07-22-interpreter-trust-root-security-review.md, dev/proposals/archive/2026-07-22-claude-interpreter-trust-root-fallback.md -->

# The interpreter trust root: absent degrades, present-but-wrong refuses

**Author**: Claude (Strategy)
**Model**: Claude Opus 4.8
**Date opened**: 2026-07-22
**Status**: proposed
**Touches**: `templates/skills/_lib/lifecycle.py` (`_resolve_interpreter`, `_intent_whoami`, and the two eager call sites); its byte-identical self-hosted copy `tools/lifecycle.py` plus that file's one entry in `dev/.cairn/cairn-lock.yml`; `bootstrap/tests/test_lifecycle_failsafe.py` (relocated + new cases). **Explicitly not touched**: `bootstrap/_scaffold/` (no engine edit, therefore no AST re-anchor — argued below), `doctrine/`, `AGENTS.md`.
**Related**: carved out of the accepted `2026-07-11-claude-first-session-survivability` as its Finding 2 — the Maintainer's Decision (`dev/proposals/2026-07-11-claude-first-session-survivability.md:352-358`) accepted F1/F3/F4 and carved F2 out to open "as **its own proposal, gated on a dedicated Security Review**". Both review tiers of that proposal reached the split independently (Internal R4, External E3), and its Internal panel pre-registered hard constraints on this change (R1 test design, R3 doctrine framing, R5 appended-argument shape, R7 warning plumbing) that this proposal adopts. Upstream signal: `dev/strategy/2026-07-08-claude-broad-look-skeptical-review.md:399-413` (day-one item 10) and recommendation **A7** at `:575-579`. Raw Internal panel source for the parent: `dev/reviews/2026-07-11-first-session-internal-panel.json`.
**Plan review**: required(External) — the floor is a fresh-context Internal read, and an **External (different-agent-type or human) read plus the dedicated Security Review the Decision already gated this on** are both required before the Decision. This proposal *relaxes* a fail-closed control on an executable trust root; it should not land on a same-type read.

*(Every `path:line` citation below was read against the working tree this session; line numbers are a dated snapshot as_of 2026-07-22, not a live invariant. The full suite was run this session — real baseline in "Evidence".)*

## Context

`dev/.cairn/local-env.json` is an **executable trust root**: it names the Python binary the session routines invoke sub-tools with, as an explicit argv list — `bootstrap/_scaffold/install.py:363` writes it, and `templates/skills/_lib/lifecycle.py:906` (`[interpreter, str(intent_tool), "list"]`), `:198` (`whoami`), and `_run_lifecycle_metrics` (`:1166`) execute it. The file is machine-local: `bootstrap/_scaffold/config.py:224` seeds it into `.gitignore`, and it has **no entry in the install lockfile** (`grep -c local-env dev/.cairn/cairn-lock.yml` → `0`, this session), so `bootstrap/verify_integrity.py` — the control `doctrine/runtime-contract.md:132` marks **Required** ("Detects tampered apparatus before it can self-audit; fail-closed") — does not cover it. That is exactly why the reader carries its own strict schema.

**The breaker.** `write_local_env` records `str(Path(sys.executable).resolve())` (`install.py:363`); its own docstring (`install.py:342-345`) says `.resolve()` "dereferences every symlink component", so under conda / homebrew / pyenv the recorded value is a **version-specific** absolute path (`…/envs/foo/bin/python3.13`). A routine environment rebuild deletes it. On the read side:

* an **absent config** is a graceful fallback — `lifecycle.py:349-351` returns `(sys.executable, "fallback")`;
* a **recorded-then-deleted binary** falls through the schema checks to `lifecycle.py:387-390` and raises `LifecycleError('… "interpreter" is not an executable file: {interp}.')` — a message with **no recovery guidance**, phrased as a schema violation;
* the two eager call sites are unguarded — `cmd_session_start` at `:698`, `_do_full_handoff` at `:1155` — so the exception reaches `main` (`:1265-1272`), which prints `ERROR:` and returns `1`.

Net: after an ordinary conda rebuild — the target adopter's normal — `session-start` and the goodnight handoff refuse to start, and the message reads like tamper detection rather than "your environment moved." The broad-look audit reproduced this end-to-end (`dev/strategy/2026-07-08-claude-broad-look-skeptical-review.md:405-410`) and its recommendation A7 asks to "make a vanished Python path a warning-with-fallback instead of a fatal error" (`:577-578`).

**A second, verified fact the parent proposal did not surface, and a security reviewer needs.** The resolver's own docstring claims "Any violation **refuses before running anything**" (`lifecycle.py:341`). That is **not universally true today**: `_intent_whoami` already wraps the resolver and swallows *every* `LifecycleError` silently —

```
lifecycle.py:194-197
    try:
        interpreter, _ = _resolve_interpreter(root)
    except LifecycleError:
        interpreter = sys.executable
```

— and then runs `intent.py` under `sys.executable` at `:198`. The chain is reachable on the most-run command: `cmd_session_end` (`:1111`) → `_do_reflection` (`:1048`) → `_resolve_agent` (`:1051`) → `_intent_whoami` (`:233`) → the swallow. So on the default `session-end` (reflection-only) path a **tampered** binding produces no error, no warning, and no refusal. The runtime outcome is safe (only the already-running stdlib interpreter and a lockfile-covered tracked script execute), but the *detection* is already lost on that path — silently and for every violation class, which is strictly broader and quieter than what this proposal asks for.

## Proposed paths

Proposed paths:
- `dev/plans/interpreter-trust-root-fallback.md` — the implementing plan; materializes at plan-open if accepted.
- `dev/reviews/2026-07-22-interpreter-trust-root-security-review.md` — the dedicated Security Review artifact this proposal is gated on; materializes when that pass runs.
- `dev/proposals/archive/2026-07-22-claude-interpreter-trust-root-fallback.md` — this file's archive destination at plan-open.

## Proposal

**The posture, stated once: absent degrades, present-but-wrong refuses.** A structurally-valid recorded interpreter path that no longer *exists* is treated as the absent-config case — warn loudly, fall back to the interpreter already running the CLI, print re-bind guidance, exit `0`. A path that **exists** but is wrong — a non-executable regular file, a directory, a symlinked leaf or parent, a relative path, a control-charactered string, an extra-key or unreadable config — stays **fatal**, unchanged.

### C1 — the carve, placed and bounded precisely (`_resolve_interpreter`)

Replace the single predicate at `lifecycle.py:387-390` with an explicit absence probe followed by the existing check:

```python
    try:
        interp.stat()
    except (FileNotFoundError, NotADirectoryError):
        _warn(
            f'{cfg}: recorded interpreter "{interp}" no longer exists -- your '
            "environment was likely rebuilt.  Using the current interpreter.  "
            "Delete dev/.cairn/local-env.json or re-run bootstrap to refresh "
            "the binding."
        )
        return sys.executable, "fallback-stale"
    except OSError as exc:                       # EACCES / ELOOP / ENAMETOOLONG …
        raise LifecycleError(
            f'{cfg}: "interpreter" could not be inspected ({exc}): {interp}.  '
            "Refusing rather than guessing."
        ) from exc
    if not interp.is_file() or not os.access(interp, os.X_OK):
        raise LifecycleError(...)                # unchanged disposition
```

Three properties are load-bearing and each is checkable by a reviewer:

1. **Placement.** The probe goes *after* `_has_symlink_component` (`lifecycle.py:382-386`), so a stale path reached through a symlinked leaf or parent stays **fatal**. A symlink is retargetable out-of-band — that is the S2 threat the guard exists for — and we cannot distinguish a benign relocation from a malicious one. This deliberately leaves a residual (below).
2. **`stat()`, not `exists()`.** `Path.exists()` swallows the `ENOENT`/`ENOTDIR`/`EBADF`/`ELOOP` family and *re-raises* everything else as a bare `OSError` that `main` (`:1270`) does not catch — an uncaught traceback. Probing with `stat()` and degrading **only** on `FileNotFoundError`/`NotADirectoryError` makes the fail-open surface exactly "the path is not there", converts every other I/O failure into a proper `LifecycleError` (a small **hardening** this change carries alongside the relaxation), and keeps the message actionable.
3. **Degradation is reachable only after every structural check has passed.** Schema, non-empty string, control characters, absoluteness, and symlink-freedom are all upstream of the probe. There is no path by which a malformed *value* reaches the degrade branch.

### C2 — surface the degrade at every call site, without changing the signature

The warning is emitted **inside** `_resolve_interpreter` (via the existing `_warn`, which writes to stderr — `lifecycle.py:102-104`). Reason: the resolver returns `Tuple[str, str]` and `bootstrap/tests/test_lifecycle_failsafe.py:272` unpacks exactly two values, so widening the return to carry the stale path would turn an existing test red; and the parent's Internal review (R7) verified that the remedy `_warn` at `lifecycle.py:705-710` fires only when `interp_source == "fallback"`, while `_do_full_handoff` (`:1155`) discards the source entirely and prints no interpreter section at all. Emitting at the point of knowledge covers `cmd_session_start`, `_do_full_handoff`, and any future caller with one line. The cost — the resolver gains a stderr side-effect — is named, not hidden; it already performs file I/O and raises.

The source token is `"fallback-stale"`, so `cmd_session_start`'s existing line at `:704` renders `interpreter: <path>  (from fallback-stale)`. The `:705-710` branch stays keyed to `"fallback"` (the absent-*config* message), so nothing is double-printed. The docstring's "Returns … source is `"local-env.json"` or `"fallback"`" (`:343-344`) is updated to list the third value.

### C3 — stop swallowing a tamper silently (`_intent_whoami`)

Add a `_warn` inside the existing `except LifecycleError` at `lifecycle.py:196`, naming the refusal, and keep the non-fatal fallback (the intent tool is team-gated and optional — `:185-187` — and must not become a hard requirement of the default-on skill). Then correct `:341` so "refuses before running anything" names its one non-fatal exception rather than overstating the guarantee.

**Scope argument.** This is in scope because the Security Review's question — *does the interpreter trust root fail closed?* — cannot be answered without it: today the honest answer is "on the eager paths yes, on the reflection path it has always failed open, silently, for every violation class." Leaving that undocumented while relaxing the eager path would hand the reviewer a false baseline. It is also the smallest component (one `_warn`, one docstring clause, zero disposition change) and touches the same function family. It is nonetheless the **weakest-fitting** piece; the Maintainer may split it at no cost to C1/C2 (Alternative 6).

### C4 — recovery guidance on the messages that stay fatal

Append the same one-line remedy ("delete `dev/.cairn/local-env.json` or re-run bootstrap to refresh the binding") to the symlink refusal (`:383-386`) and the not-an-executable refusal (`:388-390`). **No disposition changes** — this is operator guidance on messages that keep refusing, and it is the mitigation for the symlinked-stale-parent residual C1 deliberately does not cover.

### The install side: record no differently — argued, not assumed

The parent proposal asserted "no change to `write_local_env`". Having examined the alternatives, I reach the same conclusion but for a reason worth stating, because two of the alternatives are actively worse:

* **Record the *non-resolved* `sys.executable`.** Under conda/pyenv `…/bin/python` is a symlink to `…/bin/python3.13`. `_has_symlink_component` (`lifecycle.py:315-328`) refuses any symlinked leaf or parent, so an unresolved binding would be **refused on the very first run** — converting today's post-rebuild failure into a day-zero failure. `.resolve()` exists precisely to satisfy the reader's own schema (`install.py:342-345`). Strictly worse.
* **Record nothing.** Every routine would fall back to whichever interpreter the harness happened to launch the tool with — surrendering resolve-don't-bake for all adopters to fix a subset's churn.
* **Record a richer binding** (env prefix, a "rebind hint") — the strict single-key schema (`lifecycle.py:363-366`) refuses any extra key, so this is a trust-root **schema** change: it widens the attacker-controlled field set and makes new bindings unreadable by an un-upgraded copy of the tool. Rejected.
* **Auto-rewrite the binding on stale detection.** Rejected on security grounds and worth stating explicitly for the reviewer: it turns a read path into a write at a trust root, and any *transient* absence — an unmounted volume, a network filesystem hiccup, a mid-rebuild window — would **permanently rebind** the trust root to whatever interpreter happened to be running. That is a genuine new attack primitive (transiently hide the recorded binary, then own the binding). **The proposed behavior never writes: the recorded value is left byte-for-byte intact, and re-binding stays an explicit adopter action.** A test pins this.

The defect is a read-side interpretation error — "gone" being read as "violated" — so the fix belongs on the read side.

### Self-hosted copy and the lockfile entry

`bootstrap/_scaffold/config.py:211` maps `skills/_lib/lifecycle.py` → `tools/lifecycle.py` (`verbatim: true`). Cairn self-hosts, so the repo carries both, and this session they are **byte-identical** (`shasum -a 256` on each → `296ef88bda1e3e817734cc6cdb14e9571cd3a0ee0aada8d07dfa9e1f898839c9`), which is also the `hash` **and** `base_hash` recorded for the `tools/lifecycle.py` entry at `dev/.cairn/cairn-lock.yml:544-549`. `git log --oneline -- tools/lifecycle.py` returns exactly one commit (`7519c5d`, "Adopt Cairn within Cairn: self-host the apparatus"), and the most recent commit touching the template (`f5d20c2`) precedes it — so **this is the first change to the shipped `lifecycle.py` since Cairn self-hosted**, and the sync obligation has never been exercised here.

The plan therefore updates all three together — template, `tools/lifecycle.py`, and that single lockfile entry's `hash`/`base_hash` — so Cairn's own tree stays verifiable under `bootstrap/verify_integrity.py`. This is a **hash refresh for one changed file, not a lockfile-schema change**; the schema (a high-risk surface per `AGENTS.md:301`) is untouched. The accepted F1/F3/F4 work also edits `lifecycle.py` (its F4 self-description fix), so whichever lands first carries the same one-time obligation and the other must re-anchor its line citations — a sequencing note for the plan, not a conflict.

### Documentation / doctrine surface

* **Shipped-tool docstrings** — `lifecycle.py:331-348` (the trust-root contract, the source-value list, and the "refuses before running anything" clause) and the comment at `:370-374`, whose claim that an appended-argument string "is caught by the `is_file()` check below" becomes wrong under C1 (such a string is an absent *path* and now degrades). Both are corrected in the same commit as the behavior.
* **The test module's own docstring** — `bootstrap/tests/test_lifecycle_failsafe.py:16-19` states "a tampered config refuses before running anything"; it is re-worded to the two-branch posture.
* **`CHANGELOG.md`** — one entry at release, describing the posture in adopter terms.
* **No doctrine, no `AGENTS.md`.** Per the doc-tier home rule, this is a behavior change in a shipped tool plus its own reference text — the descriptive layer. `bootstrap/SAFETY.md` and `SECURITY.md` were both checked and **neither promises anything about the interpreter binding's failure disposition**: SAFETY.md Rule 2 (`:37`, `:44-46`) forbids local filesystem paths in *generated committed* files, which `local-env.json` satisfies by being gitignored (`config.py:218-226`; asserted at `bootstrap/tests/test_skills_security.py:172-176`), and SECURITY.md's nearest statement (`:44-54`) is about running shipped scripts through a trusted interpreter and verifying the installed tree against the lockfile. Nothing there needs to change, and nothing there is contradicted.
* **Not templated for adopters.** The behavior ships to every adopter through the shipped tool, so the tool's own text is the adopter-facing documentation surface. No template prose changes.

### Doctrine-change rate-limit (if this proposal changes doctrine)

**N/A — this proposal changes no doctrine.** No file under `doctrine/` is added or altered; the interpreter trust root's disposition is code behavior and a tool docstring, not a codified rule (the parent's Internal panel independently grepped `doctrine/` and confirmed no rule codifies it). The gate at `doctrine/rationale.md` > "How the doctrine evolves under evidence" governs *new doctrine* and does not apply.

I want to be explicit about the bypass rather than leave it ambiguous, because "it touches security" is the most tempting bad argument available here: **I do not invoke the high-risk single-incident bypass, and it would not be available if I did.** `doctrine/rationale.md:339-341` scopes the security surface to a change that "closes a vulnerability, hardens an authentication path, or removes a credential-leak vector" — this proposal *relaxes* a control (C1) and adds detection (C3, C4); it closes no vulnerability. `:346-347` is unambiguous that "Any other 'this feels urgent' framing falls outside the bypass and obeys the recurrence requirement." The imminent adopter install is urgency framing, not a bypass. None of that blocks this proposal — it simply is not a doctrine change. *If* review concludes the "absent degrades, present-but-wrong refuses" rule should be **codified** in `doctrine/`, that is a separate proposal which must clear the gate on recurrence or goodnight synthesis, and this proposal does not attempt it.

### Threat model, and whether degrading opens a door

**What the fatal-on-tamper behavior defends.** The adversary is someone who can write `dev/.cairn/local-env.json` on the adopter's machine — a malicious dependency's install hook, a compromised agent session, a co-tenant on a shared box, a hostile process in a CI container. The file is untracked and gitignored, so it is **invisible to code review, to `git status`, and to the lockfile-driven `verify_integrity.py`** (verified: no lockfile entry). Redirecting it to an attacker-controlled binary gets that binary executed by an argv-list `subprocess.run` during the routine the adopter trusts most. Fail-closed refusal makes the redirect loud instead of silent — and refusal is the *only* control on this file, which is why it is strict.

**What it does not defend, stated honestly.** An adversary who can write `dev/.cairn/local-env.json` can usually also write `tools/lifecycle.py`. The trust root is therefore not a containment boundary against a full-tree writer; its value is against a **narrower** writer (one who can drop a file into an untracked dotfolder but whose edit to a tracked, lockfile-covered file would be caught by `git status` / `verify_integrity.py`) and as a **tamper-evidence** surface. Overclaiming here would be easy and wrong.

**Does degrading on absence open a new door? No — and here is the argument, not the assertion.** In the degrade branch the recorded string is **never passed to `subprocess.run`, never joined into a command, never used at all**; it appears only inside a warning message. The interpreter that runs instead is `sys.executable` — the interpreter *already executing the code that makes this decision*, hence necessarily already trusted. So the set of binaries reachable through this config strictly does not grow: an absent path was never executable to begin with, and `sys.executable` was already reachable through the pre-existing absent-config branch at `:349-351` and through the pre-existing swallow at `:196-197`. **No new execution path is created.**

**Residuals — named, with their true weight:**

1. **Detection is downgraded, not execution.** A tamper that writes a *nonexistent* path (a typo, an appended-argument string like `/usr/bin/python --foo`, a path into a not-yet-created directory) moves from a hard refusal to a stderr warning with `rc == 0`. An adopter who ignores stderr will not notice their trust root was edited. This is the real cost and the reviewer's main lever. Mitigations: the warning names the recorded value verbatim, both eager routines emit it, and C3 removes the *silent* swallow that is the worse version of this same problem.
2. **The two-stage / delete-then-recreate race.** An attacker could write a not-yet-existing path (degrade, warn, `rc == 0`), then create an attacker-controlled binary there, so run *N+1* executes it. But this is a **fail-late, not a new capability**: an attacker able to create that file later could equally have created it *first*, and today's code accepts an existing, non-symlinked, executable file without complaint. The carve costs an accidental early alarm in a badly-sequenced attack, not a control. There is also a narrow TOCTOU between the `stat()` probe and the later `subprocess.run` — pre-existing in the accept path, unchanged in kind, and its worst outcome remains a refusal or a failed exec.
3. **The appended-argument shape degrades rather than refuses.** `/usr/bin/python --foo` was *designed* to be caught by `is_file()` (the comment at `:370-374`); under C1 it is an absent path and degrades. Safe — the string is never executed and the arguments are discarded with it — but the parent's Internal review (R5) was right that "only pure absence degrades" is imprecise, and the parent's Response chose this disposition deliberately over a raw-string heuristic (which cannot distinguish `--foo` from a legitimate spaced path such as `My Drive/python` and would regress `test_space_in_interpreter_path_accepted`). This proposal adopts that choice, updates the now-wrong comment, and flags it here as the single most reviewable consequence.
4. **A stale path with a symlinked parent stays fatal.** If an environment rebuild leaves any component of the recorded path a symlink, `:382-386` refuses before the probe, so those adopters still hard-fail — the fix does not reach them. Deliberate (see C1 property 1); C4 at least gives them the remedy in the message. If the Security Review judges this residual worse than the risk of probing before the symlink check, the ordering is a one-line change and I would rather it be their call than mine.
5. **`os.access(..., os.X_OK)` is not a meaningful execute test on Windows.** `doctrine/runtime-contract.md:75` and `:81` acknowledge Windows adopters. I could **not verify Windows behavior this session** (no Windows host available), so I flag rather than assert: if `X_OK` is degenerate there, the "present-but-non-executable refuses" leg may be weaker on Windows. This is **pre-existing** — the predicate at `:387` is unchanged by this proposal — but a Security Review should record it rather than inherit it silently.

**The fail-closed invariant, and what enforces it.** *No path that exists on disk is ever degraded around.* Every present-but-wrong shape — non-executable regular file, directory, symlinked leaf or parent, relative path, control characters, extra key, unreadable JSON, un-`stat`-able path — still raises `LifecycleError` before anything runs. Enforced by the rewritten `test_tampered_local_env_refuses` parametrize (which for the first time contains a genuinely *present* non-executable case), `test_extra_key_in_local_env_refused`, and a new un-`stat`-able case. The companion invariant — *a degraded run never rewrites the binding* — is enforced by a byte-comparison test.

## Rationale

* **Which user workflow does it improve?** The daily loop, for the adopter whose environment churns — which is every conda/pyenv scientist, and specifically our first external adopter. `session-start` and the goodnight handoff currently refuse to run after a routine `conda env remove && conda env create`, with a message that reads like an attack was detected. After this change they run, warn once, and tell the adopter exactly how to re-bind.
* **What contract or boundary does it preserve or clarify?** It makes the trust-root contract *say what it does*: today the docstring promises "any violation refuses before running anything" while one call site has always swallowed every violation. After this change the contract is a legible two-branch rule — absent degrades with a named forfeiture, present-but-wrong refuses — with the one non-fatal path documented instead of hidden.
* **What correctness / reproducibility does it improve?** The routines stop conflating "your environment moved" with "someone edited your trust root", which is the difference between an adopter who re-binds in ten seconds and one who concludes the apparatus is broken. And the tamper *class* gains real test coverage it does not have today.
* **Why now?** The parent proposal's Decision carved this out on 2026-07-22 specifically so it could get an unhurried dedicated Security Review, and Phase A closes before the first adopter installs. The security question is small and self-contained *right now*; bundled later into a larger change it would not be.

## Alternatives considered

1. **Do nothing.** The reproduced breaker ships into a one-shot first adoption; the adopter's first conda rebuild ends their daily loop with a message implying tampering. Rejected — but it is the honest baseline, and it *is* the safest option from a pure trust-root standpoint. Anyone arguing for it is arguing that detection of absent-path edits outweighs the adopter's daily loop; I disagree, but the trade is real and the reviewer should weigh it.
2. **Guidance only — keep every disposition fatal, just improve the message** (C4 alone). Strictly smaller and gives up nothing security-wise: the adopter is told "delete `local-env.json` or re-run bootstrap." It still costs them a hard failure and a manual step on every rebuild, so it fixes the confusion but not the breakage. **This is my recommended fallback if the Security Review is uncomfortable with C1** — it is a genuine, shippable subset, not a consolation.
3. **Guard the call sites instead of the resolver** — wrap `:698` and `:1155` in `try/except LifecycleError` and degrade there, as `_intent_whoami` already does at `:194-197`. Rejected: catching `LifecycleError` at the call site degrades on *every* violation class including real tampering, which is the fail-open the strict schema exists to prevent, and it is what makes the existing swallow a problem rather than a precedent to copy.
4. **Degrade on absence *before* the symlink check.** Would also rescue the symlinked-stale-parent adopters (residual 4). Rejected as author's default because a symlinked component is retargetable out-of-band and the ordering is what keeps that guard first — but the change is one line and I explicitly put it to the Security Review rather than deciding it unilaterally.
5. **Fix it on the install side** — record a non-resolved path, record nothing, record a richer binding, or auto-rebind on staleness. All four analyzed above; each is either refused by the reader's own schema on day zero, surrenders resolve-don't-bake for everyone, changes the trust-root schema, or (auto-rebind) creates a transient-absence-to-permanent-rebind primitive. Rejected on the merits, not by assumption.
6. **Split C3 (the `_intent_whoami` warning) out.** Viable at no cost to C1/C2/C4. Kept here because the Security Review cannot assess "does this fail closed?" against a false baseline; offered to the Maintainer as the natural trim if a tighter scope is wanted.
7. **Recommended: C1 + C2 + C3 + C4 together**, with the corrected test design below, through External + the dedicated Security Review before the Decision.

**Open questions I am not entitled to close — the Maintainer's (with the Security Review advising):**

* **Is the detection downgrade acceptable?** C1 converts a hard refusal into a warning for every *absent-path* edit of the trust root, including tamper-shaped ones (residual 1, residual 3). Execution is unaffected; tamper-evidence is weakened. This is the single judgment the whole proposal rests on, and it is a risk-acceptance call, not a technical one.
* **Probe before or after the symlink check?** (Alternative 4 / residual 4.) After = today's symlink guard keeps priority and symlinked-parent adopters still hard-fail. Before = they are rescued, at the cost of degrading on a shape the guard exists to catch. I default to *after*; I would rather the Security Review own this line than inherit my default silently.
* **Should C3 ride along or split?** (Alternative 6.) It is one `_warn`, but it also *documents* a pre-existing silent fail-open — which may deserve its own record rather than a paragraph inside another proposal's Security Review.
* **Should the two-branch posture be codified in `doctrine/` at all?** I argue no (it is tool behavior, and codifying it must clear the rate-limit gate on its own evidence). If the Maintainer wants it as doctrine, that is a separate, separately-gated proposal.

## Evidence / verification plan

### Author-accounting — invariants, failure modes, edge cases

* **Invariants.**
  * *(i)* **Nothing that exists on disk is degraded around** — every present-but-wrong shape still raises before anything runs. *Enforced by* the rewritten `test_tampered_local_env_refuses` parametrize (present non-executable file; present directory; relative path; wrong schema), `test_extra_key_in_local_env_refused` (`bootstrap/tests/test_lifecycle_failsafe.py:278-287`, unchanged), and a new un-`stat`-able-path case.
  * *(ii)* **The recorded value is never executed in the degrade branch** — it appears only in a warning string. *Enforced by* the fallback test asserting the resolved interpreter equals `sys.executable`, never the recorded value.
  * *(iii)* **A degraded run never rewrites the binding.** *Enforced by* a new byte-comparison test on `dev/.cairn/local-env.json` before and after a degraded `session-start`.
  * *(iv)* **Degradation is unreachable until every structural check has passed** — schema, control chars, absoluteness, symlink-freedom all precede the probe. *Enforced by* the placement itself plus the refuse-parametrize cases that exercise each earlier gate.
  * *(v)* **Both eager routines surface the degrade.** *Enforced by* one test per call site (`session-start`, `session-end --handoff`) asserting the remedy text on stderr.
* **Failure modes.** C1's new branch is **fail-open by design and by named forfeiture** for the absence case only; every other branch is **fail-closed and unchanged**, and the `OSError`-that-is-not-`ENOENT` path is newly fail-*closed* (today it escapes as an uncaught `OSError`). C3 changes no disposition — it converts a silent fail-open into a *loud* fail-open. C4 changes no disposition at all.
* **Edge-case inventory.** Absent leaf → degrade. Present non-executable regular file → fatal. Present directory → fatal. Symlinked leaf or parent, stale or live → fatal (`:382-386`, priority preserved). Broken symlink at the leaf → fatal via the symlink guard, never reaching the probe. Relative / control-charactered / extra-key / unreadable JSON → fatal, untouched. Appended-argument string → **degrades** (residual 3, deliberate). Unreadable parent directory (`EACCES`) → fatal `LifecycleError` (improved from an uncaught `OSError`). Path recreated between the probe and the exec → out of scope (pre-existing TOCTOU class). `sys.executable` itself unusable → out of scope, pre-existing.
* **Public-path → test mapping.** `lifecycle._resolve_interpreter` (and, through it, `cmd_session_start` / `_do_full_handoff` / `_intent_whoami`) → [`../../bootstrap/tests/test_lifecycle_failsafe.py`](../../bootstrap/tests/test_lifecycle_failsafe.py), exercised through the public `lifecycle.main([...])` entry point for the call-site behavior and through `_resolve_interpreter` directly for the resolver contract — matching how the file already splits those two levels (`:225` vs `:272`).
* **Known omissions / intentionally untested edges.** Windows `os.access(..., os.X_OK)` semantics — flagged, unverified this session, pre-existing (residual 5). Real conda/homebrew symlinked-*parent* layouts — reasoned from the guard, not reproduced on a real rebuilt environment (residual 4); a hand-run on an actual rebuilt conda env before the Decision would be the single most valuable piece of evidence I cannot produce here. The un-`stat`-able-path test needs a root/Windows skip guard, and I have not proven that guard is sufficient on every CI platform. No adversarial red-team of the two-stage race was performed beyond the reasoning in residual 2.

### Tests required

All in `bootstrap/tests/test_lifecycle_failsafe.py`. **The parent's Internal review (R1) and External review (E1) both established that the naive version of this change turns the suite red, and both were right** — I re-verified it this session:

* `test_tampered_local_env_refuses` (`:240-252`) asserts `rc == 1` for **four** parametrized values, and **two of them are absent-path values**: `/usr/bin/python --foo` (`:242`) and `/no/such/python` (`:243`). Both are absolute and non-symlinked, so under C1 they return `rc == 0`. They must be **relocated**, not merely supplemented.
* **Replace** them with cases that are genuinely *present*: a regular file without the execute bit, and a directory. **A correction to the reviews' suggested fix**: it proposed building the non-executable file "via `_make_exe` without chmod", which is not possible — `_make_exe` (`:255-260`) unconditionally does `path.chmod(path.stat().st_mode | stat.S_IXUSR)`. A new sibling helper (write only, no chmod) is needed. Note also that `_make_exe` is *defined below* the parametrize (`:255` vs `:240`) and module-level parametrize values cannot use the `repo` fixture, so present-file cases must be materialized in the test body (e.g. from a sentinel the body expands against `repo`), not in the decorator.
* **New** `test_stale_interpreter_path_degrades_with_guidance`, parametrized over the two relocated values: asserts `rc == 0`, `(from fallback-stale)` on stdout, and the re-bind remedy on stderr.
* **New** `test_stale_binding_is_not_rewritten`: the `local-env.json` bytes are identical before and after a degraded run (invariant iii).
* **New** `test_uninspectable_interpreter_path_refuses`: an un-`stat`-able path raises `LifecycleError` (skip-guarded for root and non-POSIX).
* **New** `test_handoff_surfaces_stale_interpreter`: `session-end --handoff` (with the designation marker, as `test_handoff_with_marker_runs_and_prunes` already sets up) emits the remedy — the `:1155` call site, which prints nothing today.
* **New** `test_tampered_binding_warns_in_intent_whoami` (C3): a present-but-wrong binding produces a NOTE on stderr instead of silence, and `_intent_whoami` still returns non-fatally.
* **Must stay green, unchanged**: `test_interpreter_resolved_from_local_env_and_reported` (`:216-229`), `test_absent_local_env_uses_fallback_with_guidance` (`:232-237` — the absent-*config* case, distinct from the new stale-*path* case, so its `"no dev/.cairn/local-env.json"` stderr assertion is untouched), `test_space_in_interpreter_path_accepted` (`:263-275` — the reason C2 keeps the 2-tuple return), `test_extra_key_in_local_env_refused` (`:278-287`).

**Gate-manifest consequence — verified, and not the AST re-anchor.** `bootstrap/tests/test_lifecycle_failsafe.py` is in the frozen set of the committed gate-integrity manifest (`bootstrap/tests/fixtures/gate_manifest.json`; 147 frozen files as_of 2026-07-22), whose verifier HOLDs on a frozen-file edit and on a dropped or renamed pytest node while allowing additions (`bootstrap/tests/_gate_manifest.py:12-17`, `:33-36`). That manifest is a **batch-scoped pre-run control**, produced in a supervised prerequisite commit and checked with `verify --anchor-ref <SHA>` (`bootstrap/tests/_gate_manifest.py:41-53`); it is **not** part of `python -m pytest bootstrap/tests` — my full-suite run this session did not exercise it. Two concrete implications for the plan: (a) confirm with the Maintainer whether a manifest-anchored batch is live, and if so route the test edits through the supervised re-anchor path (`bootstrap/tests/_gate_reanchor.py`); (b) keeping the refuse-parametrize at **exactly four** cases preserves the node IDs `bad0`–`bad3` recorded at `bootstrap/tests/fixtures/gate_manifest.json:590-593`, so no node is dropped. Giving the parametrize semantic `ids=` would be more readable but *renames* those four nodes — a HOLD class. I default to preserving the IDs and flag the readability trade for the plan.

**No AST re-anchor — verified, not assumed.** `bootstrap/tests/test_ast_attest.py` pins the engine package rooted at `bootstrap/_scaffold/__init__.py` (`bootstrap/tests/test_ast_attest.py:20`) against `bootstrap/tests/fixtures/scaffold_ast_baseline.json`. This proposal edits **nothing** under `bootstrap/_scaffold/` — the install side is explicitly unchanged — so it does not mutate a baselined symbol digest and triggers **no** re-anchor per `bootstrap/REANCHOR_RUNBOOK.md`. (The accepted F1/F3/F4 work does, separately.)

### Examples / smoke checks

* **Manual repro, both directions** — point `dev/.cairn/local-env.json` at a deleted path and run `python tools/lifecycle.py session-start`: must warn with the remedy and exit `0`. Then point it at a present non-executable file and re-run: must refuse and exit `1`. This is the two-line demonstration of the whole posture and belongs in the plan's verification block.
* **Real environment rebuild** — rebuild a conda env, then run `session-start` against the now-stale binding. Named here because it is the actual reported failure and no unit test substitutes for it; also the check most likely to expose residual 4 (symlinked parent).
* **Self-host verification** — after syncing `tools/lifecycle.py` and refreshing its lockfile entry, run `python bootstrap/verify_integrity.py --target .` from a trusted checkout and confirm Cairn's own tree still verifies.
* **`python -m pytest bootstrap/tests`** — the honest baseline, measured this session: **3 failed, 1408 passed, 3 skipped in 101.68s**, under Python **3.12.9** (not the canonical 3.13 named at `doctrine/runtime-contract.md:60`). The three failures are pre-existing and untouched by this proposal: two `bootstrap/tests/test_ast_attest.py` nodes (the known stale engine baseline, issue #1) and `bootstrap/tests/test_evolution_infer.py` `TestGateEval::test_main_suggests_and_json`, which hardcodes June-2026 dates against a rolling 14-day window and has been red by passage of time. **The suite is not green and this proposal does not make it green**; the pass/fail claim is "no *new* failures, and `test_lifecycle_failsafe.py` goes from 18 passed to 18-plus-the-new-nodes passed" (18 passed in 1.69s this session).
* **`python scripts/claim_check.py`** clean over this proposal and the plan; **`python scripts/check_cairn.py`** clean over the edited files.
* **N/A** — the example gallery (`examples/minimal/`, `examples/scientific-minimal/`) and `python bootstrap/scaffold.py --dry-run`: neither exercises the lifecycle tool's runtime interpreter resolution, so neither is meaningful evidence here.

## Signals the change is wrong

* **An adopter runs for weeks on `fallback-stale` without noticing.** If the warning is routinely ignored, we have traded a loud failure for silent drift — the routines quietly using a different interpreter than the project's. *Recovery:* escalate the surfacing (repeat it in the `session-end` summary, or make `session-start` exit non-zero after N consecutive stale runs), or fall back to Alternative 2 and keep it fatal with better guidance.
* **The Security Review finds a shape where "absent" is attacker-influenced in a way I have not modelled** — some path where the *absence itself* is the exploit. *Recovery:* Alternative 2 (guidance only) is a complete, shippable subset that requires deleting only C1 and C2; C3 and C4 stand alone and strictly improve detection.
* **The relocated test cases turn out to still be load-bearing as refusals** — i.e. review decides an appended-argument string must refuse regardless of path existence. *Recovery:* re-add a targeted raw-string check *before* the probe, accepting that it cannot distinguish `--foo` from a legitimate spaced path and will need `test_space_in_interpreter_path_accepted` re-litigated. The parent's Response rejected this; a Security Review may legitimately overrule that.
* **C3's new warning fires noisily on a normal reflection-only `session-end`.** If some benign configuration makes `_intent_whoami` hit a `LifecycleError` routinely, we have added noise to the most-run command. *Recovery:* the warning is one line and trivially reverted to the silent swallow; C3 is independent of C1/C2/C4.
* **The self-host sync causes lockfile churn we did not anticipate** — e.g. `verify_integrity.py` flags something beyond the single refreshed entry. *Recovery:* revert the `tools/lifecycle.py` sync and land the template change alone, accepting a documented, deliberate divergence in Cairn's own tree until the next full upgrade pass.
* **Nobody hits it.** If the first adopter never rebuilds their environment, this was Phase-A effort spent on a hypothetical while other day-one breakers waited. *Recovery:* none needed — the change is small and independently revertable — but it would be evidence that reproduced-breaker triage should weight *frequency*, not just severity.