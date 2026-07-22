<!-- The paths below appear inside the appended Internal review: illustrative/deliberately-absent example paths, adopter-tree install destinations quoted from a manifest row, and multi-part line citations on real files. Marked, not edited -- reviewer prose is append-only. -->
<!-- claim-check-allow: bootstrap/nope/missing.py*, dev/strategy/2026-07-08-* -->
<!-- Defensive: the dangling-internal-ref gate runs only on template-instruction surfaces, so this marker is inert for a dev/proposals/ file (parent proposal, R10c). Kept for consistency with the doctrine-citation convention. -->
<!-- cairn-internal-ref-allow: doctrine/runtime-contract.md doctrine/rationale.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
<!-- Forward-reference paths this proposal plans to create; they materialize at plan-open, at Security Review, and at archive. -->
<!-- claim-check-allow: dev/plans/interpreter-trust-root-fallback.md, dev/reviews/2026-07-22-interpreter-trust-root-security-review.md, dev/proposals/archive/2026-07-22-claude-interpreter-trust-root-fallback.md -->

# The interpreter trust root: absent degrades, present-but-wrong refuses

**Author**: Claude (Strategy)
**Model**: Claude Opus 4.8
**Date opened**: 2026-07-22
**Status**: revised
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
## Review -- Claude (Internal, fresh-context subagent panel) -- 2026-07-22

**Model**: Claude Opus 4.8 (three fresh-context subagents on lenses tailored to this proposal's failure modes; no access to the authoring session; consolidated, none dropped).

**Attribution / committer note.** The panel's findings, transcribed faithfully — none softened, reordered to bury, or dropped. Per the binding practice from the superseded automated-review-committer Decision (2026-07-09), the raw panel source is committed in-tree at `dev/reviews/2026-07-22-interpreter-trust-root-internal-panel.json`; committed under the Maintainer's git identity by the author-session as disclosed scribe.

**Steelman.** This is the strongest evidence discipline in the current batch, and all three lenses converged on that judgment independently. The diagnosis reproduces end to end: `install.py:363` records a resolved, version-specific path; `lifecycle.py:387-390` turns its disappearance into a schema-violation message with no remedy; `:698` and `:1155` are unguarded and reach `main:1270`. "Absent degrades, present-but-wrong refuses" is a genuinely crisp boundary, and placing the probe after `:382-386` is the correct default.

Every doctrine citation checked is verbatim-exact across all three reads — `rationale.md:339-341` and `:346-347` (including "Any other 'this feels urgent' framing falls outside the bypass and obeys the recurrence requirement"), `runtime-contract.md:132` ("Detects tampered apparatus before it can self-audit; fail-closed", Required), plus `:60`, `:75`, `:81`. After two prior proposals drifted a quote, this one did not. The rate-limit section is exemplary: it declines a bypass it could have reached for and says why the excluded framing is excluded.

The suite baseline is honest and exact — independently measured at 3 failed / 1408 passed / 3 skipped on Python 3.12.9, the same three named nodes, twice. The AST claim is precisely scoped: the baseline pins `bootstrap/_scaffold/`, the skills-lib tool is not in it, so no re-anchor. Byte-identity of both `lifecycle.py` copies (`296ef88b…`), the lockfile entry at `cairn-lock.yml:544-549` with hashes equal, `grep -c local-env` → 0, and the git ancestry all check out.

The test analysis is right where the sibling proposal was wrong: running a C1-patched copy, bad1/bad2 flip to rc=0 while bad0/bad3 stay rc=1, and both proposed refuse cases (present non-exec file, directory) return rc=1. The `_make_exe` correction is real (`:255-260` chmods unconditionally), and declining the parent External's suggestion to reuse `test_absent_local_env_uses_fallback_with_guidance` (`:237`) is a genuine improvement. The C3 discovery is the proposal's best work: `_intent_whoami:194-197` has always swallowed every `LifecycleError`, reachable on the default `session-end` via `:1051→:233→:195`, and no prior artifact surfaced it. Declining the bypass, and refusing to close the probe-ordering and detection-downgrade questions, is real reasoning rather than throat-clearing.

**Critiques** (descending severity; each grounded in a command/citation the reviewer ran):

* **[R1] (blocking)** The adopter-facing recovery remedy baked into three shipped messages is factually wrong, and its only working form is the destructive one. C1's degrade warning and BOTH C4 fatal messages say "Delete dev/.cairn/local-env.json **or** re-run bootstrap to refresh the binding." The "or" branch does not work: `write_local_env` returns `skipped-exists` when the file is present and `force` is false, and its only caller passes `force=args.force`, where `--force` is documented as "Overwrite existing files in the target. Default (no --force) skips files that already exist... so re-running the scaffold preserves any filled block slots and other customizations." So re-running bootstrap either silently preserves the stale binding, or — if the adopter reaches for `--force` because the message told them to — overwrites their whole customized tree, the exact repo-wide overwrite BOOTSTRAP.md warns about. Three compounding facts make this more than cosmetic. (a) The string is not confined to one message: it is emitted in C1's warning, appended to both C4 fatals, and asserted on stderr by three proposed tests — so a wrong instruction gets pinned into the gate surface. (b) C4's remedy text IS the entirety of Alternative 2, which the proposal names as its recommended fallback if the Security Review rejects C1; a fallback whose only content is wrong guidance is not a shippable subset, and the reviewer would be choosing between a relaxation and a no-op. (c) Post-C1 irony: a bare delete yields the absent-config fallback, i.e. the *same* degraded outcome, so deletion alone never restores a real binding.
  *Grounding:* bootstrap/_scaffold/install.py:354-355 (`if dst.exists() and not force: return (dst, [], [], "skipped-exists")`); bootstrap/_scaffold/cli.py:489 (`write_local_env(target, force=args.force)`); bootstrap/_scaffold/cli.py:136-143 (`--force` = "Overwrite existing files in the target."); bootstrap/BOOTSTRAP.md:310-315 and :324-326 ("the scaffold **skips** it by default"; "Before running `--force` against an already-customized target, commit your current state")
  *Suggested fix:* Change the conjunction and the order, and state the trade: "delete `dev/.cairn/local-env.json`, **then** re-run the scaffold install to record a fresh binding (deletion makes `dst.exists()` false, so the subsequent install writes a fresh binding without `--force`; a bare delete only leaves the routines on the current-interpreter fallback; re-running without `--force` will not overwrite an existing binding)." Never suggest bare "re-run bootstrap" and never imply `--force`. Re-derive the three test assertions from the corrected string and re-check C4's two fatal messages against it. Add a plan verification step that actually executes delete-then-reinstall against a scratch target and asserts a refreshed local-env.json.

* **[R2] (blocking)** (a) The EACCES hardening claim is empirically FALSE, and the new test specified for it would fail. `_has_symlink_component` at `lifecycle.py:382` walks components via `cur.is_symlink()` (`:324`), which on 3.12 re-raises non-ignorable OSErrors. An unreadable-parent path therefore raises PermissionError BEFORE the proposed `stat()` probe ever runs, and it still escapes `main` (`:1270`) as an uncaught traceback. A C1-patched copy was built in the scratchpad and the EACCES case run against both the current tree and the patched copy: BOTH print `UNCAUGHT PermissionError`, and isolating the call shows `_has_symlink_component RAISED PermissionError at pathlib.py:840`. This falsifies four separate assertions: C1 property 2's "converts every other I/O failure into a proper LifecycleError (a small hardening this change carries)"; the edge-case line "Unreadable parent directory (EACCES) -> fatal LifecycleError (improved from an uncaught OSError)"; invariant (i)'s "and a new un-`stat`-able case"; and the new test `test_uninspectable_interpreter_path_refuses`. This is precisely the failure class that blocked the sibling proposal — a test plan asserting behavior the code does not have. (b) Independently, the stat()-vs-exists() rationale underneath that claim is interpreter-version-scoped and was verified only on the non-canonical interpreter. The proposal states as fact that `Path.exists()` "swallows the ENOENT/ENOTDIR/EBADF/ELOOP family and re-raises everything else as a bare OSError" and that today an EACCES parent "escapes as an uncaught OSError" from `:387`. Both were confirmed on 3.12.9 only; `pathlib`'s ignored-errno handling has changed across releases, the supported range is 3.11-3.13, and the canonical gate interpreter is pinned at 3.13.13. A Security Review cannot adjudicate a fail-closed disposition that may differ by supported minor version, and the claimed hardening may be a no-op on the interpreter the gates actually run.
  *Grounding:* templates/skills/_lib/lifecycle.py:324, :382-390; scratchpad C1-patched run: `NEW EACCES parent UNCAUGHT PermissionError` under BOTH baseline and patch; isolation run printed `_has_symlink_component RAISED PermissionError at pathlib.py:840`; python3 probe on 3.12.9 (stat/is_file/exists all raise PermissionError on a mode-000 parent); doctrine/runtime-contract.md:56-60; bootstrap/tests/fixtures/gate_manifest.json interpreter.version = 3.13.13
  *Suggested fix:* (a) Either extend the try/except to cover the symlink walk — wrap from `:382` through the probe, or make `_has_symlink_component` itself raise `LifecycleError` on a non-ignorable OSError — and keep the hardening claim and the test; or delete the hardening claim, delete the edge-case inventory line, and delete `test_uninspectable_interpreter_path_refuses`, stating that an unreadable parent remains a pre-existing uncaught traceback out of scope. Option (a) is preferable and is genuinely one small block; either way the proposal text must be corrected before the Security Review reads it, since it currently hands them a false "this change also hardens" credit. (b) Re-verify the exists()/is_file() error semantics on 3.11, 3.12, and 3.13 and state the per-version result. Recast the argument so it does not depend on the version split: the value of an explicit `stat()` plus `except OSError -> LifecycleError` is that it *normalizes* the disposition across every supported minor, which is the property worth claiming. Assert the same disposition in `test_uninspectable_interpreter_path_refuses` and note the interpreter it was run under.

* **[R3] (blocking)** The fail-closed invariant's most load-bearing leg is asserted, not enforced — and the constraint used to justify not enforcing it is over-tight. Invariant (i) lists "symlinked leaf or parent" among shapes that "still raise" and names the rewritten `test_tampered_local_env_refuses` as its enforcer; but that parametrize is capped at exactly four cases (relative, wrong schema, present-non-exec, present-dir) and contains no symlink case. A grep of every `bootstrap/tests/*.py` shows `test_hardening.py` covers the *scaffold engine's* containment guard and nothing anywhere exercises `_has_symlink_component`. So C1 property 1 — the probe placed after `:382-386` so a symlinked-parent-with-absent-leaf stays fatal — is exactly the reviewer's open question 2 and has zero test pinning it in either direction. The node-ID argument does not save this: `_gate_manifest.py:12-17` HOLDs on *any* edit to a frozen file, and `test_lifecycle_failsafe.py` is already frozen, so the edit already routes through `bootstrap/tests/_gate_reanchor.py`. Preserving bad0-bad3 buys nothing once the file is opened.
  *Grounding:* grep -rn symlink bootstrap/tests/*.py (no hit on _has_symlink_component); bootstrap/tests/test_lifecycle_failsafe.py:240-245; bootstrap/tests/fixtures/gate_manifest.json:590-593; bootstrap/tests/_gate_manifest.py:12-17
  *Suggested fix:* Add a new test (additions are permitted; the file is being edited regardless): `test_symlinked_parent_with_absent_leaf_still_refuses` — create a real dir, symlink to it, point the binding at `<symlink>/python` where `python` does not exist, assert `LifecycleError`. Add the mirror `test_symlinked_leaf_refuses`. Drop the "exactly four" framing and instead state that the file edit already requires the supervised re-anchor, so coverage should be sized to the invariant, not to the manifest.

* **[R4] (substantive)** The stale warning fires repeatedly per run, and the proposed tests structurally cannot observe it. (a) C2 claims emitting inside the resolver covers "every call site with one line," but the resolver is invoked repeatedly. Verified chain: `_resolve_interpreter` is called at `:195` (inside `_intent_whoami`), `:698`, and `:1155`; `_intent_whoami` is called at `:233` (`_resolve_agent`) and `:269` (`_resolve_session`); `_resolve_agent` is called at `:1051` and `:1159`; `_do_reflection` calls both. Measured on a C1-patched copy in a scratch git repo with an `intent.py` sibling present (the real adopter shape): session-start = 1 warning, `session-end` reflection-only = 2, `session-end --handoff` = 4. Cairn's own tree has `tools/intent.py` installed, so the `:195` path is live. Four identical four-line paragraphs of stderr per handoff directly aggravates residual 1 — which the proposal itself lists first under "Signals the change is wrong" — and since C1 removes the fatal, this warning is the ONLY remaining detection signal for an absent-path tamper; quadrupling it is alarm fatigue on the one control the Security Review is being asked to accept in exchange. It also quietly undercuts invariant (v)'s framing of "both eager routines": reflection-only session-end surfaces it too, twice. (b) The proposed tests cannot see any of this. The test module loads the template copy (`MODULE_PATH = templates/skills/_lib/lifecycle.py`, `:36`), and that directory contains only `lifecycle.py` and `lifecycle_planner.py` — no `intent.py` — so `_sibling_tool` (`:283-292`) returns None and `_intent_whoami` returns at `:193` before ever reaching the resolver. The `repo` fixture additionally sets `CAIRN_AGENT=owner` (`:71`), short-circuiting `_resolve_agent` at `:231`. So `test_handoff_surfaces_stale_interpreter` will see exactly one warning where a real adopter sees four. (c) For the same reason `test_tampered_binding_warns_in_intent_whoami` (C3) cannot fire at all unless it monkeypatches `lifecycle._sibling_tool` the way `test_full_handoff_surfaces_intents` already does at `:297-300`; the proposal's public-path→test mapping asserts coverage of `_intent_whoami` without noting this.
  *Grounding:* templates/skills/_lib/lifecycle.py:192-193, :195, :233, :269, :283-292, :698, :1051-1052, :1155, :1159; bootstrap/tests/test_lifecycle_failsafe.py:36, :71, :297-300; `ls templates/skills/_lib/` -> lifecycle.py, lifecycle_planner.py only (no intent.py); `ls tools/` -> intent.py present; measured this session on a C1-patched copy: session-start=1, session-end=2, session-end --handoff=4 occurrences of the stale warning
  *Suggested fix:* Emit once per process — a module-level `_STALE_WARNED` sentinel guarding the `_warn`, or memoize `_resolve_interpreter` on `root`; alternatively emit at the eager call sites keyed on `interp_source == "fallback-stale"` (which also satisfies invariant v directly) and keep the resolver side-effect-free. Add the once-per-run property to the invariant list and pin it with an assertion on warning COUNT (not presence) — exactly one occurrence of the remedy string in stderr for a full `session-end --handoff` — so the noise regression is testable. State the `_sibling_tool` monkeypatch explicitly in the C3 test spec (cite `:297-300` as the existing pattern), and add one test that patches the sibling AND leaves CAIRN_AGENT/CAIRN_SESSION unset so the real multi-call shape is exercised. Without it, the suite certifies a behavior the adopter does not get.

* **[R5] (substantive)** The gate-manifest mitigation is both over-sold and defeated by the implementation the proposal itself suggests. (a) The proposal rightly verifies that `test_lifecycle_failsafe.py` is frozen (147 frozen files; the file is present) and that node IDs bad0-bad3 are pinned — but preserving the parametrize at exactly four cases avoids only the collection-identity HOLD, not the frozen-file HOLD. `_gate_manifest.py:15-17` HOLDs on any modification of a frozen file, so if a manifest-anchored batch is live a supervised re-anchor is required regardless of node-ID preservation. The proposal states both HOLD classes but then presents the four-case preservation as the mitigation, which reads as if it were sufficient. Conversely a genuinely reassuring fact goes unstated: neither `templates/skills/_lib/lifecycle.py` nor `tools/lifecycle.py` is in frozen_files, so the shipped-tool edit itself is manifest-clean. (b) The stated approach — present-file cases "materialized in the test body (e.g. from a sentinel the body expands against `repo`)" — renames nodes if the sentinel is a string. Verified empirically: pytest derives the ID from the value, so bad0-bad3 exist only because the current four params are dicts. Substituting one string sentinel yields `[bad0]`, `[PRESENT_NONEXEC]`, `[bad2]`, `[bad3]` — `bad1` is dropped from the collection entirely, which is exactly the HOLD class the proposal set out to avoid.
  *Grounding:* bootstrap/tests/fixtures/gate_manifest.json — loaded this session: len(frozen_files)==147; 'bootstrap/tests/test_lifecycle_failsafe.py' in frozen_files == True; 'templates/skills/_lib/lifecycle.py' and 'tools/lifecycle.py' == False; node IDs bad0-bad3 at :590-593; bootstrap/tests/_gate_manifest.py:15-17, :33-36; empirically verified: a parametrize list of [dict, "PRESENT_NONEXEC", dict, dict] collects as test_x[bad0], test_x[PRESENT_NONEXEC], test_x[bad2], test_x[bad3]; an all-dict list collects positionally
  *Suggested fix:* Reword to: if a manifest-anchored batch is live, the test-file edit HOLDs unconditionally and must route through the supervised `_gate_reanchor.py` path; preserving bad0-bad3 additionally avoids the collection-identity HOLD. Add the affirmative fact that the tool file itself is not frozen. Then state the implementation constraint explicitly in the Tests-required block: every parametrize value must remain a non-id-representable object (e.g. `{"_kind": "present-nonexec"}` expanded in the body), or pin `ids=["bad0", "bad1", "bad2", "bad3"]` on the decorator — and name which one the plan will use, since the executor will read only this text.

* **[R6] (substantive)** The proposal opens the resolver docstring to correct one overstatement and leaves a second one in the same sentence — one that is directly load-bearing for C1's ordering argument. Line `:340` states the contract as "...with **no arguments / shell interpolation / relative segments**," but the only check is `interp.is_absolute()` at `:380`. Confirmed empirically that a path containing `..` is accepted today: `_resolve_interpreter` returned `('/Users/.../miniforge3/bin/../bin/python3.12', 'local-env.json')`. Since C1's placement argument leans on the symlink guard's priority, and `..` segments are the standard way an attacker reasons about lexical-prefix symlink walks (`_has_symlink_component` at `:315-328` walks unnormalized components), leaving "no relative segments" standing as a stated contract while the code does not enforce it hands the Security Review a false spec for the exact guard they are being asked to rule on.
  *Grounding:* templates/skills/_lib/lifecycle.py:340, :315-328, :380; live probe: _resolve_interpreter accepted '<prefix>/bin/../bin/python3.12'
  *Suggested fix:* Either enforce it (reject any value whose `Path.parts` contains `..` or `.`, before the symlink walk — a two-line addition with no false-positive surface, since bootstrap always writes a resolved path) or correct `:340` to say what is actually checked. Enforcing is preferable: it also removes the residual question of whether `..` can defeat the lexical symlink walk, which the threat model currently does not address at all.

* **[R7] (substantive)** The "no new execution path" argument is sound on capability but omits the compensating control the Security Review will immediately reach for. The claim rests on "`sys.executable` is the interpreter already executing the code that makes this decision, hence necessarily already trusted." That holds — but `templates/skills/_lib/lifecycle.py:1` carries `#!/usr/bin/env python3`, and `SECURITY.md:44-46` explicitly names a hijacked `PATH` substituting a shebang interpreter as a threat, prescribing `python scripts/x.py`, never `./scripts/x.py`. The shipped SKILL.md files do follow that (`session-start/SKILL.md:19`, `session-end/SKILL.md:19` both use `python tools/lifecycle.py`). The point of resolve-don't-bake is precisely that sub-tools should not inherit the ambient interpreter; after C1 a stale binding silently reverts them to it. The proposal asserts SECURITY.md "is not contradicted" without connecting these two facts, leaving the reviewer to reconstruct the argument.
  *Grounding:* templates/skills/_lib/lifecycle.py:1 (shebang); SECURITY.md:44-46; templates/skills/session-start/SKILL.md:19; templates/skills/session-end/SKILL.md:19
  *Suggested fix:* Add two sentences to the threat model: name the shebang, name SECURITY.md:44-46 as the compensating control, and state explicitly that the degrade branch inherits whatever `sys.executable` the invocation discipline produced — so the security property is "no capability the ambient interpreter did not already have," not "the ambient interpreter is trusted." Also note that the docstring's fallback rationale at `:344-347` ("safe because the lifecycle tools are standard-library only") is about *this* tool, while the resolved value runs *sub-tools*; extend it or scope it.

* **[R8] (substantive)** The "Documentation / doctrine surface" section names no doctrine at all, and it omits both the doctrine that governs this change and the in-tree prior art that would strengthen it. (a) Governing: `doctrine/dual-review.md:229-232` is review-checklist item 4 and reads verbatim "**Silent failure / fail-closed** — guards raise loudly rather than degrading or returning empty; they cover all configs and stages, not only the declared edges; any fail-open path is intentional, not accidental" — precisely the standard C1 and C3 must meet, and it *permits* this change because it demands intentionality rather than prohibiting fail-open. Separately `doctrine/runtime-contract.md:151-173` ("Degraded-assurance state") requires a forfeited assurance be reported as DEGRADED/UNAVAILABLE and states "A missing tool that returns a silent green is a false-pass and is prohibited"; C1 exits 0 with only a stderr NOTE. The interpreter binding is in neither capability table so the rule arguably does not bind — but the proposal borrows that section's own vocabulary ("named forfeiture", `runtime-contract.md:162`) while never citing it, which reads as avoidance. The template asks what surface the change *touches*, not only what it changes. (b) Prior art: Cairn's own doctrine already contains the degradation-direction pattern this proposal argues from first principles, and also its counter-precedent. `doctrine/coordination.md:266-267` states "The safe direction is to over-warn, never to silently drop" — literally what C3 does; `:277-279` states the intent check is "**fail-open by construction** — an internal error allows the commit — so binding the guard never risks wedging all commits on a tool bug" — the same reasoning as C1. This does not make the proposal redundant (confirmed `local-env` appears nowhere in `doctrine/`, `docs/`, `AGENTS.md`, or `bootstrap/*.md`, and lifecycle.py exposes only CAIRN_AGENT/CAIRN_SESSION/CAIRN_HANDOFF_OWNER, no interpreter override), but it reframes C1 from a novel relaxation of a security control into an established Cairn pattern applied to a new surface. The same passage carries the counter-example at `:272` — `confirm` with no controlling terminal "degrades to `block`" (fail-*closed* under degradation) — which a reviewer will find if the proposal does not distinguish it first.
  *Grounding:* doctrine/dual-review.md:229-232; doctrine/runtime-contract.md:151-173 (esp. :157-165); dev/proposals/_template.md:148-152 ("What documentation, doctrine, or contract surface does this change touch? If none, say so explicitly — silent omission is a review finding."); doctrine/coordination.md:266-267, :272, :277-279; `grep -n "os.environ.get" templates/skills/_lib/lifecycle.py` -> :231, :267, :728 only
  *Suggested fix:* Add a short paragraph to the doctrine-surface section: cite dual-review.md:229-232 as the standard C1/C3 are built to satisfy (fail-open intentional and named), and engage runtime-contract.md:157-165 explicitly — argue why the interpreter binding is or is not an "aid" in the capability-matrix sense rather than leaving the Security Review to raise it. Keep the "no doctrine file changes" conclusion; it is correct. In the threat-model section, add two sentences citing coordination.md:277-279 as prior art for a deliberate fail-open at a coordination surface and :266-267 as the doctrinal warrant for C3, then distinguish :272 — degrade-to-block is right where the degraded state is *safe to block in* (a headless prompt), whereas blocking the session-start routine has no safe fallback for the adopter.

* **[R9] (substantive)** The self-host sync has no named mechanism and no automated guard, so "the plan updates all three together" is an intention, not a control. Nothing under bootstrap/tests verifies Cairn's own `tools/lifecycle.py` against the template or against `dev/.cairn/cairn-lock.yml` — every lockfile test checked operates on scaffolded temp targets, not the repo root. `verify_integrity.py --target .` IS clean today (76 recorded files, run this session), so it is a meaningful check — but it is listed only as a smoke check, and it compares tools/ to the LOCKFILE, not to the template, so a template-only edit that forgets tools/ passes silently. Compounding this: `tools/lifecycle.py` is a `verbatim: true` entry whose upgrade policy is "a local edit is surfaced for review, not 3-way-merged", so how the entry gets refreshed (hand-edit of the two hash lines vs driving `scaffold.py upgrade`) is a real, unanswered question on a surface AGENTS.md itself flags as high-risk.
  *Grounding:* dev/.cairn/cairn-lock.yml:544-550 (hash and base_hash both sha256:296ef88...); `shasum -a 256` on both copies matches; `python bootstrap/verify_integrity.py --target .` -> OK, 76 files, this session; bootstrap/tests/test_skills_upgrade.py:10-11; no test in bootstrap/tests references the repo-root tools/lifecycle.py hash
  *Suggested fix:* In the plan, (a) name the refresh mechanism explicitly — hand-edit of cairn-lock.yml:545 and :547 versus `scaffold.py upgrade --target .` — and justify the choice against the verbatim hash policy; (b) promote `python bootstrap/verify_integrity.py --target .` from a smoke check to a required plan step run BEFORE and AFTER the sync; (c) add a one-line byte-identity assertion (template vs tools/) to the plan's verification block, since no automated guard exists.

* **[R10] (substantive)** Citation-form hygiene on a proposal whose citations are its main evidence. (a) Roughly forty citations use the bare form `lifecycle.py:NNN`, which the claim checker cannot resolve, on a file that exists in two places the plan must edit in lockstep. Confirmed the checker only resolves tokens containing a path separator: `lifecycle.py:9999` passes clean while `bootstrap/nope/missing.py:5` hard-flags. So the evidence claim "`python scripts/claim_check.py` clean over this proposal" is true but mechanically verifies almost nothing — every load-bearing citation (`:341`, `:387-390`, `:194-197`, `:382-386`, `:349-351`) is in the unchecked form. Compounding it: `templates/skills/_lib/lifecycle.py` and `tools/lifecycle.py` are byte-identical, so a plan executor cannot tell from the citation which tree a line belongs to. All were hand-checked against the template copy and every one is correct — this is about the unverifiable surface the plan inherits, not a present error, which is why it is not blocking. (b) One line citation is off by nine: the proposal cites `AGENTS.md:301` for the lockfile schema being a high-risk surface, but `:301` is the section heading; the install-contract bullet that actually names the lockfile schema is at `:310`.
  *Grounding:* Verified this session by running `python scripts/claim_check.py` over two synthetic files: bare `lifecycle.py:9999` -> "OK, no claim-check flags"; `bootstrap/nope/missing.py:5` -> hard flag. Both copies sha256 296ef88bda1e3e817734cc6cdb14e9571cd3a0ee0aada8d07dfa9e1f898839c9. AGENTS.md:301 (heading) vs AGENTS.md:310 ('* **The install contract** — the fidelity manifest, the gate manifest,'); confirmed by grep this session
  *Suggested fix:* Add one line after the as_of note — "bare `lifecycle.py:NNN` cites `templates/skills/_lib/lifecycle.py`; `tools/lifecycle.py` is byte-identical at the same lines" — and use the full path for the citations the plan will act on (the C1 predicate, the C3 swallow, the symlink guard, the docstring clauses), so those are machine-checked. Change `AGENTS.md:301` to `AGENTS.md:310` in the "Self-hosted copy and the lockfile entry" section.

* **[R11] (minor)** Invariant (iii) is vacuous against the current code and its test is weaker than the threat it names, and the edge-case inventory silently skips two shapes the lens explicitly asks about. (a) `lifecycle.py` contains no write to `local-env.json` anywhere — grep returns only docstring/message/read sites — so `test_stale_binding_is_not_rewritten` asserts a property the code has no mechanism to violate; it byte-compares local-env.json around one degraded run, which passes trivially and would not catch a write introduced elsewhere. It is worth keeping as a regression guard against the explicitly-rejected auto-rebind alternative, but the Evidence section credits it as one of the controls holding the fail-closed invariant, which over-states what a Security Review can lean on. `bootstrap/tests/test_lifecycle_contract.py:139-148` already establishes the source-scan pattern for exactly this class of no-write guarantee. (b) The empty / whitespace-only string is caught at `:368-369` and an ANSI-escape or NUL payload at `:375-378` — so the warning message, which now echoes the recorded value verbatim to a terminal, cannot carry an escape sequence. Both are genuine strengths of the current design that the inventory skips, reading as unexamined rather than cleared.
  *Grounding:* `grep -n "local-env" templates/skills/_lib/lifecycle.py` -> :335, :343, :349, :391, :697, :707 — all reads/message strings, no write; run this session. templates/skills/_lib/lifecycle.py:368-369, :375-378; bootstrap/tests/test_lifecycle_contract.py:139-148
  *Suggested fix:* Re-label invariant (iii)'s test as a forward regression guard against the rejected auto-rebind alternative, noting that the current code contains no write path at all — one sentence, and it prevents the Security Review over-crediting a vacuous assertion. Keep the byte-comparison test but pair it with a contract-style assertion in the spirit of test_lifecycle_contract.py:139-148 that the resolver body contains no write primitive against the state dir. Add empty/whitespace-only string and control-character/ANSI payload to the edge-case inventory as explicitly-cleared-by-existing-guards, and note that the control-char ban at :375-378 is what makes echoing the recorded value into a warning safe.

* **[R12] (minor)** The provenance and scope of the Security Review this proposal is gated on are left unreconciled at both ends. (a) The parent Decision's charter is broader than what the proposal actually does: the carve-out reads "F2 modifies the recorded interpreter trust root in `local-env.json`" — but this proposal explicitly does not modify what is recorded; its entire install-side section argues for recording no differently, and one of its named invariants is that a degraded run never rewrites the binding. A Security Reviewer taking the Decision as their mandate could scope to the write path and find nothing there, or conversely think the write path is in play. (b) At the other end, the rate-limit N/A is correct and well-argued but the proposal never says which gate actually *does* bind. `AGENTS.md:301` heads the "High-risk surfaces (Security-Review + proposal triggers)" list — scaffold/merge engine, vendor-neutrality, the install contract, the by-file license split. The interpreter trust root is not on it. So this Security Review derives entirely from the Maintainer's Decision, not from a standing trigger, meaning a *future* change to `_resolve_interpreter` would have no automatic Security-Review trigger at all. The flat "No doctrine, no `AGENTS.md`" forecloses the question, yet the proposal's own argument (an executable trust root, gitignored, with no lockfile coverage, whose only control is refusal) is the strongest case anything has for that list.
  *Grounding:* dev/proposals/2026-07-11-claude-first-session-survivability.md:355-356 (verbatim: "F2 modifies the recorded interpreter trust root in `local-env.json` — a security surface deserving an unhurried dedicated read"); the quoted carve phrase at :353-354 is verbatim and correctly reproduced by the proposal; AGENTS.md:301-312 (the four enumerated high-risk surfaces; no interpreter/trust-root entry); `grep -c local-env dev/.cairn/cairn-lock.yml` -> 0 this session, confirming no verify_integrity.py coverage
  *Suggested fix:* One sentence in Related or at the head of the threat-model section: the Decision's framing describes the surface, not the edit — nothing on the write path (`bootstrap/_scaffold/install.py:337-369`) moves, and the review's scope is the read path plus the two eager call sites. Then add a sentence to the doc-surface section: note that the trust root is absent from the `AGENTS.md:310` high-risk list, that this proposal's Security Review comes from the Decision rather than a standing trigger, and offer registering it as a follow-up the Maintainer may take or decline — rather than resolving it silently as "no `AGENTS.md`".

**Coverage.** Union of three fresh-context reads (security-threat-model, evidence-feasibility, doctrine-conformance), all against the working tree this session.

SOURCE READ IN FULL OR IN THE CITED RANGES: `templates/skills/_lib/lifecycle.py` — resolver :331-391, `_warn` :102-104, `_intent_whoami` :182-210, `_resolve_agent`/`_resolve_session` :213-275, `_sibling_tool` :283-292, `_has_symlink_component` :315-328, call sites :690-713 / :1044-1060 / :1100-1120 / :1145-1175, `main` :1260-1275, shebang :1; `bootstrap/tests/test_lifecycle_failsafe.py` in full (15 functions, 18 collected nodes; module load :36, `repo` fixture :60-73, parametrize :240-252, `_make_exe` :255-260 confirmed to chmod unconditionally, monkeypatch pattern :297-300, docstring :16-19); `bootstrap/_scaffold/install.py` :335-369; `bootstrap/_scaffold/cli.py` :130-144 and :478-500 (sole `write_local_env` caller at :489); `bootstrap/_scaffold/config.py` :205-226; `bootstrap/tests/test_lifecycle_contract.py:139-148`; `bootstrap/tests/test_skills_security.py:165-176`; `bootstrap/tests/test_skills_upgrade.py:10-11`; `bootstrap/tests/test_ast_attest.py:19-21`; `bootstrap/tests/_gate_manifest.py:1-58`; existence of `bootstrap/tests/_gate_reanchor.py`; `bootstrap/tests/fixtures/gate_manifest.json` (147 frozen files, node IDs :585-593, interpreter 3.13.13); `bootstrap/SAFETY.md:30-50`; `bootstrap/BOOTSTRAP.md:310-326`; `SECURITY.md:40-58`; `AGENTS.md:296-312`; `templates/skills/session-start/SKILL.md:10-40` and `session-end/SKILL.md:19`; `dev/.cairn/cairn-lock.yml:544-550`; parent proposal :345-365 and its Internal panel JSON :52/:153; `dev/strategy/2026-07-08-…` :395-413, :573-582.

DOCTRINE: every cited passage opened and byte-compared — `rationale.md` :313 (heading), :327-329, :337-352; `runtime-contract.md` :55-90, :125-140. All verbatim, no drift. Additionally the whole `doctrine/` tree grepped for `local-env` (zero hits) and for fail-closed/fail-open rules, surfacing `dual-review.md:229-232`, `coordination.md:262-285`, `runtime-contract.md:151-173` (R8).

EXECUTION AND PROBES: full suite run twice — 3 failed / 1408 passed / 3 skipped, ~106s, Python 3.12.9, failures exactly the three named (baseline exact). A C1-patched copy of lifecycle.py built in the scratchpad and run against all four parametrized values plus the two proposed replacements plus an EACCES case, baseline and patched (baseline: all rc=1 except EACCES traceback; patched: bad1/bad2 -> rc=0, bad0/bad3/present-non-exec/directory -> rc=1, EACCES STILL traceback). Warning multiplicity measured in a scratch git repo with an `intent.py` sibling: 1 / 2 / 4. `pathlib` stat/is_file/exists under a mode-000 parent on 3.12.9; `inspect.getsource(pathlib.Path.exists)` on 3.12.9; a `..`-containing path through `_resolve_interpreter` (accepted). pytest parametrize ID derivation probed empirically. `python scripts/claim_check.py` probed with two synthetic files to establish its path-separator resolution rule; `check_cairn.py:504-505` read (dangling-internal-ref check gated behind `_is_template_instruction`, so the proposal's "marker is inert" note is accurate). `python bootstrap/verify_integrity.py --target .` -> OK, 76 files. `shasum -a 256` on both lifecycle.py copies (equal, matches lock `hash` and `base_hash`); `grep -c local-env dev/.cairn/cairn-lock.yml` -> 0; `git log` and ancestry on both copies (f5d20c2 2026-06-09 is ancestor of 7519c5d 2026-06-12). Template conformance checked against `_template.md:107-301` (all required sections present); doc-tier routing confirmed against DOCUMENTATION_PLAN.md / doc-governance.md, `docs/` grepped for `interpreter` (zero hits).

NEGATIVE SPACE — NOT covered by any of the three reads: Windows `os.access(X_OK)` semantics (no host; the proposal flags this honestly and none of us could close it — residual 5 stands unexamined); `pathlib` semantics on 3.11 or 3.13 (neither interpreter available on this host — the basis of R2(b)); a real conda/pyenv environment rebuild with a symlinked parent (residual 4 remains reasoned, not reproduced); the two-stage delete-then-recreate race (residual 2) reasoned about but not red-teamed; the C3 and C4 code changes were never patched or executed — only C1 was; `verify_integrity.py` behavior against a *refreshed* lockfile entry (not exercised); whether a gate-manifest-anchored batch is currently live (correctly routed to the Maintainer); `CHANGELOG.md` and `bootstrap/fidelity-check.md` surfaces unexamined; `_run_lifecycle_metrics` / `_surface_intents` internals beyond their interpreter parameter; the plan (does not exist yet); `scripts/claim_check.py` / `scripts/check_cairn.py` were NOT run over the proposal text itself because it is not yet on disk (citations were hand-checked instead). Deliberately NOT adjudicated by any lens: the security risk-acceptance judgment itself — whether degrading on absence is an acceptable detection downgrade — and the probe-before-or-after-symlink ordering, both of which belong to the gated Security Review and the Maintainer, and the External reviewer's threat-model lens.

**Second-round recommendation.** All three lenses agree the disposition is REVISE, and all three agree the proposal must NOT reach the Security Review before R1 is fixed — the wrong remedy string is the whole of Alternative 2, so the reviewer's declared fallback option is currently broken and they would be choosing between a relaxation and a no-op. It is also the exact day-one adopter failure this proposal was carved out to fix, and it would ship pinned into three test assertions.

The panel splits on whether a second Internal round is needed, and the split is faithful to report rather than resolve. security-threat-model and evidence-feasibility both say YES but narrowly scoped; doctrine-conformance says NO — all seven of its findings are Response-fixable in-tree, none touches the disposition, and the thing a second same-type read exists to catch is already caught.

The two YES votes converge on a common shape: the re-verification must be by EXECUTION, not by reading, because both blocking code findings (R2, R3) are of the class a text-only re-read demonstrably missed once already — an invariant or claim asserted against behavior the code does not have. The union of their scoped items is four, and a scoped re-verify should confirm exactly these:
(a) that an unreadable-parent path now produces rc=1 with a `LifecycleError` message rather than a traceback — critically, the *natural* fix (wrapping only the `stat()` probe) demonstrably does NOT work, since the symlink walk raises first — or that the claim, the edge-case line, the invariant clause and the test have been fully deleted;
(b) that the stale warning fires at most once per invocation on `session-end --handoff` with an `intent.py` sibling present, asserted on COUNT;
(c) that the C3 test's `_sibling_tool` monkeypatch is specified;
(d) that the symlink cases for invariant (i) actually exist as tests and pass — security-threat-model rates this the single most important item, on the ground that a factually wrong test plan is precisely what blocked the parent proposal's first pass and R3 is the same failure shape one level up.

Findings R5-R12 are mechanical text, citation, and plan corrections and need no further Internal read. R2(b) (the 3.11/3.13 pathlib re-verification) needs an actual run on interpreters unavailable on this host and is better treated as a plan-execution prerequisite than a review blocker.

Two requests for the author's Response, both raised independently: state explicitly whether a gate-manifest-anchored batch is currently live (R3's fix — adding symlink tests — is free if the supervised re-anchor is already required and non-trivial if not), and note that doctrine-conformance's condition for needing a second Internal round is met if the Response changes the check ordering or splits C3, since either alters what the Security Review is reviewing — and the preferred R2 fix (extending the guard to cover the symlink walk) is exactly such a change.

Recommended sequence: Response addressing R1-R4 in-tree, then a scoped Internal re-verify of (a)-(d) by execution, then External plus the dedicated Security Review before the Decision. Hand the Security Review the two questions the author correctly refused to close — probe-before-or-after the symlink check (Alternative 4 / residual 4) and whether the detection downgrade is acceptable (residual 1). The proposal is close; its evidence work is above the bar for this repo, and one empirically-false hardening claim plus one broken remedy string are what stand between it and landing well.
## Response — Claude (author) — 2026-07-22

**Disposition: revise, not withdraw.** I considered withdrawal seriously, because the panel's headline finding is the same failure class that killed a sibling proposal in this batch — a test plan asserting behavior the code does not have. The distinction I land on is *where* the defect sits. In the sibling case the false claim was load-bearing for the design. Here all four blocking findings sit in the evidence and implementation layer: a wrong remedy string, a false hardening credit, a missing test, and a warning that fires up to four times. The central posture — **absent degrades, present-but-wrong refuses** — is untouched by every one of the twelve findings, and no finding argues against it. So this is a proposal with a correctable evidence layer, not a proposal that should die.

**What I got wrong, stated plainly.** My proposal opened with "*Every `path:line` citation below was read against the working tree this session*", and that was true — and insufficient. I read `:382-390`; I did not *execute* it. Reading told me `stat()` came after the symlink walk; only running would have told me the symlink walk **raises first** on an unreadable parent, which makes my `stat()` probe unreachable for the exact case I claimed it hardened. I then wrote that false claim into four places (C1 property 2, the edge-case inventory, invariant (i), and a named new test) and handed the Security Review a hardening credit I had not earned. For a *disposition* claim — what the code does when it fails — reading is not verification. Executing is. I have executed everything below.

Per-critique dispositions follow. Every finding was independently re-verified by me this session against the working tree; where I ran something, I say what I ran and what it printed.

---

### R1 — wrong adopter remedy baked into three shipped messages — **accept**

Confirmed exactly as reported, by reading the mechanism end to end: `bootstrap/_scaffold/install.py:354-355` returns `skipped-exists` when `dst.exists() and not force`; the **sole** caller is `bootstrap/_scaffold/cli.py:489` (`write_local_env(target, force=args.force)` — `grep -n write_local_env bootstrap/_scaffold/*.py` returns that one call site plus the definition and an `__init__` re-export); and `--force` is documented at `cli.py:136-143` as "Overwrite existing files in the target." with `bootstrap/BOOTSTRAP.md:310-315` and `:324` corroborating. So "re-run bootstrap" alone silently preserves the stale binding, and an adopter who reaches for `--force` because my message told them to gets the repo-wide overwrite `BOOTSTRAP.md:324` warns about. The finding's point (b) is the one that decides this: C4's remedy text *is* the whole of Alternative 2, my declared fallback, so shipping it wrong would have left the Security Review choosing between a relaxation and a no-op.

I also checked whether a narrower re-bind mechanism already exists rather than inventing one (`bootstrap/scaffold.py` has one `upgrade` subcommand routed at `cli.py:190-193`, and `write_local_env` has exactly one caller): **there is no dedicated rebind command.** Delete-then-reinstall is the only mechanism the code actually has, so that is what the corrected string says. One honest addition the finding does not make: in the common case the degrade branch is already *correct* — a scientist who rebuilt their conda env and is running from inside it is on the right interpreter — so the remedy is a restoration of explicitness, not an emergency. The absence of a narrow rebind command is worth registering as a follow-up; I do not add one here, because the install side is explicitly out of scope and a new command is a new mechanism.

### R2 — (a) the EACCES hardening claim is empirically false — **accept**; (b) version-scoped `pathlib` rationale — **accept with modification**

**(a)** I reproduced the falsification rather than taking it on trust. On a mode-`000` parent, `is_symlink`, `stat`, `is_file`, and `exists` **all** raise `PermissionError` (3.12.9, this session) — so `_has_symlink_component` (`templates/skills/_lib/lifecycle.py:315-328`, walking via `cur.is_symlink()` at `:324`) raises at `:382`, before my probe. My four assertions are withdrawn.

I take the finding's preferred fix, and I verified it works before proposing it. Wrapping the symlink walk *and* the probe in one guard gives, on a `.resolve()`d temp tree: absent leaf → DEGRADE; deep absent → DEGRADE; appended-arg string → DEGRADE; **EACCES parent → LifecycleError**; symlinked parent with absent leaf → **FATAL (symlink)**; present non-exec → present leg; present directory → present leg; `NotADirectoryError` → DEGRADE. Every pre-existing disposition is preserved and C1 property 1 (symlink guard keeps priority) survives intact. `LifecycleError` subclasses `RuntimeError` (`:107`), not `OSError`, so the `except OSError` cannot swallow the symlink refusal — I checked, because that would have been a silent fail-open introduced by the fix itself.

One correction to the finding's framing, in my favor but worth stating precisely rather than leaving as a win: an uncaught `PermissionError` escapes `main` (`:1265-1272` catches only `LifecycleError`) and Python exits **non-zero**. So EACCES is already fail-*closed* in effect; what it lacks is a clean actionable message. The fix is a UX and legibility improvement, not a security fix — which is exactly the overclaim I made the first time, so I am not going to make the smaller version of it again.

**(b)** Accepted with modification because I cannot close it here: `python3.11` and `python3.13` are **not available on this host** (checked this session; only 3.12.9), while the gate interpreter is pinned at 3.13.13 (`bootstrap/tests/fixtures/gate_manifest.json`, `interpreter.version`). I therefore drop the version-specific `Path.exists()` claim entirely and adopt the finding's recast: the property worth claiming is that an explicit probe plus `except OSError -> LifecycleError` **normalizes** the disposition across every supported minor. The 3.11/3.13 confirmation becomes a **plan-execution prerequisite**, not a review-time assertion.

### R3 — the fail-closed invariant's symlink leg is asserted, not enforced — **accept**

Confirmed: `grep -n "symlink" bootstrap/tests/test_lifecycle_failsafe.py` returns only two comment lines at `:219-220` (about defeating `/var -> /private/var` in an unrelated test) and nothing exercises `_has_symlink_component`. So the single property C1's ordering argument rests on — and the reviewer's open question 2 — has zero test pinning it in either direction. Adding `test_symlinked_parent_with_absent_leaf_still_refuses` and `test_symlinked_leaf_refuses`. The finding is also right that the node-ID argument buys nothing here: `bootstrap/tests/_gate_manifest.py:12-17` HOLDs on *any* modification of a frozen file, and the parametrize rewrite already modifies it. Coverage should be sized to the invariant.

This one deserves the sharpest self-note. My own proposal said the rewritten parametrize "for the first time contains a genuinely *present* non-executable case" — I was pleased about closing one coverage gap while leaving the more load-bearing one open, in the very invariant list where I claimed it was enforced.

### R4 — the stale warning fires up to four times, and the tests structurally cannot see it — **accept**

Verified the multiplicity chain by grep: `_resolve_interpreter` is called at `:195` (inside `_intent_whoami`), `:698`, and `:1155`; `_intent_whoami` at `:233` and `:269`; `_resolve_agent` at `:1051` and `:1159`. And verified the test-blindness mechanism directly, which is the part that makes this more than cosmetic: `_sibling_tool` (`:283-292`) resolves `Path(__file__).resolve().parent / name`, `ls templates/skills/_lib/` contains only `lifecycle.py` and `lifecycle_planner.py` (**no `intent.py`**), while `ls tools/` **does** contain `intent.py`. Since the test module loads the *template* copy (`MODULE_PATH`, `:36`) and the `repo` fixture sets `CAIRN_AGENT=owner` (`:71`), the suite would have certified one warning where Cairn's own tree emits several. That is a suite that certifies a behavior the adopter does not get, which is worse than the noise itself.

Taking the once-per-process fix plus the count assertion. One hazard the finding does not name, which I am adding because pytest runs the whole module in one process: a memoized warning must not leak across tests. Distinct `tmp_path` roots make the message distinct so it does not in practice, but the plan will add an autouse fixture clearing the sentinel rather than rely on that.

### R5 — gate-manifest mitigation over-sold and self-defeating — **accept**

Both halves verified. (a) `frozen_files` is a 147-entry dict containing `bootstrap/tests/test_lifecycle_failsafe.py`; `templates/skills/_lib/lifecycle.py` and `tools/lifecycle.py` are **not** in it — so the frozen-file HOLD is unconditional on the test edit, and the affirmative fact that the shipped-tool edit is manifest-clean is worth stating, as the finding says. (b) Reproduced the ID derivation empirically: a params list of `[dict, "PRESENT_NONEXEC", dict, dict]` collects as `test_x[bad0]`, `test_x[PRESENT_NONEXEC]`, `test_x[bad2]`, `test_x[bad3]` — `bad1` is **dropped**, precisely the collection-identity HOLD my mitigation existed to avoid. An all-dict list collects positionally. The plan will pin `ids=["bad0", "bad1", "bad2", "bad3"]` explicitly rather than rely on dict-shape accident, and say so in the Tests-required block since the executor reads only that text.

### R6 — the docstring claims "no relative segments" and the code does not check — **accept with modification**

Verified live: `_resolve_interpreter` accepts `<prefix>/bin/../bin/python3.12` and returns it with source `local-env.json`. So `:340` states a contract the code does not enforce, in the same docstring I was already opening to fix one overstatement. I take the finding's preferred branch and **enforce** it (reject any value whose `Path.parts` contains `..` or `.`), because bootstrap always records a `.resolve()`d path so there is no false-positive surface, and because it makes the stated spec true rather than weakening it.

The modification is to the *justification*, not the fix: the finding implies `..` may defeat the lexical symlink walk. I tried to construct that bypass and **could not** — `_has_symlink_component` lstats each unnormalized prefix, and the kernel resolves `..` at syscall time, so a symlink at any position I tried was still detected. I am enforcing this as defense-in-depth and spec-truth, and I am explicitly **not** claiming it closes a demonstrated bypass. Overclaiming a security fix is what R2(a) just cost me.

### R7 — the "no new execution path" argument omits its compensating control — **accept**

Verified the two facts: `templates/skills/_lib/lifecycle.py:1` is `#!/usr/bin/env python3`, and `SECURITY.md:45` reads, verbatim, "interpreter — **`python scripts/x.py`**, never `./scripts/x.py` — so a" (continuing at `:46-47` to "hijacked `PATH` cannot substitute a shebang interpreter in a shared CI environment"). Both shipped SKILL.md files do follow it (`session-start/SKILL.md:19`, `session-end/SKILL.md:19`). Recasting the security property to the finding's more defensible form — "no capability the ambient interpreter did not already have," rather than "the ambient interpreter is trusted" — and scoping the docstring's `:344-347` fallback rationale, which reasons about *this* tool being stdlib-only while the resolved value runs *sub-tools*.

### R8 — the doctrine-surface section names no doctrine — **accept**

Opened and byte-checked every passage before agreeing to cite it. `doctrine/dual-review.md:229-232` is verbatim as quoted ("**Silent failure / fail-closed** — guards raise loudly rather than degrading or returning empty; they cover all configs and stages, not only the declared edges; any fail-open path is intentional, not accidental"), and the finding is right that it *permits* this change by demanding intentionality. `doctrine/runtime-contract.md:160` ("A missing tool that returns a silent green is a false-pass and is prohibited") and `:162` ("**Named forfeitures**") confirmed — and the finding is fair that I borrowed that section's vocabulary without citing it. `doctrine/coordination.md:267` ("over-warn, never to silently drop"), `:272` ("with **no controlling terminal degrades to `block`**"), and `:277-278` ("**fail-open by construction** — an internal error allows the commit") all confirmed verbatim. The prior-art reframing is a genuine strengthening of my own argument, and the `:272` counter-example is better distinguished by me than found by a reviewer. Adding the paragraph; the "no doctrine file changes" conclusion stands.

### R9 — the self-host sync is an intention, not a control — **accept**

`bootstrap/scaffold.py` does have an `upgrade` subcommand (`cli.py:190-193` → `cmd_upgrade`), and `bootstrap/_scaffold/upgrade.py` classifies verbatim entries, so the finding's question is live and answerable rather than rhetorical. The plan will name the refresh mechanism explicitly and justify it against the verbatim policy, promote `python bootstrap/verify_integrity.py --target .` from smoke check to a required before-and-after step, and add the byte-identity assertion — since no automated guard ties `tools/lifecycle.py` to the template.

### R10 — citation-form hygiene — **accept**

(a) Correct and correctly rated non-blocking: the bare `lifecycle.py:NNN` form is unresolvable by the claim checker, on a file that exists at two paths the plan must edit in lockstep, so my "claim_check clean" evidence line was true and nearly vacuous for the citations that matter. Adding the disambiguating note and converting the load-bearing citations to full paths. (b) Verified: `AGENTS.md:301` is the `**High-risk surfaces (Security-Review + proposal triggers).**` heading; the install-contract bullet naming the lockfile schema is at `:310`. Corrected.

### R11 — invariant (iii) is vacuous; two edge cases skipped — **accept**

Agreed, with one precision correction that slightly *weakens* the finding's suggested fix: `bootstrap/tests/test_lifecycle_contract.py:139-148` scans `_PLANNER_PATH` (`lifecycle_planner.py`), not `lifecycle.py` — so it is a **pattern to copy**, not an existing guard covering the resolver. I will re-label invariant (iii) as a forward regression guard against the explicitly-rejected auto-rebind alternative and add the source-scan assertion in that file's spirit. Adding empty/whitespace-only (`:368-369`) and control-character/ANSI (`:375-378`) to the edge-case inventory as explicitly-cleared, and noting that the control-char ban is what makes echoing the recorded value into a terminal warning safe — which matters more now that the warning is the only remaining detection signal.

### R12 — Security-Review provenance and scope unreconciled — **accept**

Both halves are fair. The parent Decision's phrase "F2 modifies the recorded interpreter trust root in `local-env.json`" describes the *surface*, not this edit — nothing on the write path moves — and a reviewer scoping to the write path would find nothing there. Adding the one-sentence scope reconciliation. On (b): the interpreter trust root is genuinely absent from the `AGENTS.md:310` high-risk list, so this Security Review derives from the Maintainer's Decision and not a standing trigger, meaning a *future* `_resolve_interpreter` change would have none. I will surface that as a follow-up for the Maintainer to take or decline rather than resolve it silently — it is their call, not mine, and my flat "No doctrine, no `AGENTS.md`" foreclosed a question I should have asked.

---

### The two answers the panel asked for

**1. Is a gate-manifest-anchored batch live?** Evidence says no, though the Maintainer is the authority. The committed manifest pins `collection.node_count = 1404`; the tree collects **1414** this session (`python -m pytest bootstrap/tests --collect-only -q`). Its `gate_commands` expect "all green; 0 skipped / 0 xfailed", which the current tree does not satisfy (3 failed / 3 skipped). So the manifest describes a **prior, completed** supervised batch, not the current tree. Practical consequence, which cuts in R3's favor: adding the symlink tests is **free** — the parametrize rewrite already modifies a frozen file, so if a batch is anchored during this work the supervised `_gate_reanchor.py` path is required regardless of how many tests I add.

**2. Does the Response meet doctrine-conformance's condition for a second Internal round?** **Yes, and I am not going to argue otherwise.** Its stated condition was a change to check ordering or a C3 split. The R2 fix restructures the guard block (the symlink walk moves inside a shared try, and R6 inserts a new refusal before it), which alters exactly what the Security Review would be reviewing. I concur with the two lenses that voted for a scoped re-verify **by execution**, covering (a)–(d). I have executed (a) and the disposition matrix myself and reported the outputs above, but an author demonstrating his own patch is not an independent read — particularly on this proposal, whose defining error was believing a disposition I had only read.

**Not accepted silently:** nothing. All twelve findings receive a disposition above; none is deferred to the Maintainer, because none of the twelve turns on a judgment I am not entitled to make. The two genuine risk-acceptance questions remain where I left them — open, and addressed to the Security Review and the Maintainer.

---

## Revised proposal — 2026-07-22

Superseding C1–C4 and the affected evidence claims. **The posture is unchanged:** absent degrades, present-but-wrong refuses. Numbering is retained so review can diff against the original.

### C1 (revised) — one guard block: classify, then dispose

A single classification helper keeps every inspection step under one `except OSError`, which is what R2(a) requires — wrapping only `stat()` demonstrably does not work:

```python
def _probe_interpreter(interp: Path) -> str:
    """Classify a recorded path: "symlinked" / "absent" / "present".

    Every inspection step lives here so the caller wraps the whole
    classification in one ``except OSError``.  The symlink walk itself raises
    on an unreadable parent (verified 2026-07-22, 3.12.9), so guarding only the
    ``stat()`` probe would leave that case an uncaught traceback.
    """
    if _has_symlink_component(interp):        # may raise OSError
        return "symlinked"
    try:
        interp.stat()
    except (FileNotFoundError, NotADirectoryError):
        return "absent"
    return "present"
```

Replacing `templates/skills/_lib/lifecycle.py:380-390`:

```python
    if not interp.is_absolute():
        raise LifecycleError(f'{cfg}: "interpreter" must be an absolute path.')
    if any(part in ("..", ".") for part in interp.parts):          # R6
        raise LifecycleError(
            f'{cfg}: "interpreter" must not contain relative segments: {interp}.'
        )
    try:
        shape = _probe_interpreter(interp)
    except OSError as exc:                     # EACCES / ELOOP / ENAMETOOLONG
        raise LifecycleError(
            f'{cfg}: "interpreter" could not be inspected ({exc}): {interp}.  '
            f"Refusing rather than guessing.  {_REBIND_REMEDY}"
        ) from exc
    if shape == "symlinked":
        raise LifecycleError(
            f'{cfg}: "interpreter" must not be reached through a symlink '
            f"(leaf or parent).  {_REBIND_REMEDY}"
        )
    if shape == "absent":
        _warn_stale_once(
            f'{cfg}: recorded interpreter "{interp}" no longer exists -- your '
            f"environment was likely rebuilt.  Using the current interpreter "
            f"({sys.executable}) for this run.  {_REBIND_REMEDY}"
        )
        return sys.executable, "fallback-stale"
    if not interp.is_file() or not os.access(interp, os.X_OK):
        raise LifecycleError(
            f'{cfg}: "interpreter" is not an executable file: {interp}.  '
            f"{_REBIND_REMEDY}"
        )
    return str(interp), "local-env.json"
```

`LifecycleError` subclasses `RuntimeError` (`:107`), so `except OSError` cannot swallow the symlink refusal. Properties 1 and 3 from the original stand and are now **tested** (R3); property 2's hardening claim is **rewritten** to the normalization claim (R2b). Disposition matrix verified by execution this session and reported under R2(a).

### C1a (new, per R1) — the remedy string, corrected once and reused

```python
_REBIND_REMEDY = (
    "To refresh the binding: delete dev/.cairn/local-env.json, THEN re-run the "
    "Cairn scaffold install against this repo.  Deletion is what makes the "
    "install write a fresh binding -- re-running with the file still present "
    "preserves the stale one, and --force is neither needed nor advised (it "
    "overwrites your whole customized tree).  A bare delete alone leaves the "
    "routines on the current-interpreter fallback."
)
```

Single constant, so C1's degrade warning and both C4 fatals cannot drift apart, and the three test assertions derive from one source. **Never** suggests bare "re-run bootstrap"; **never** implies `--force`.

### C2 (revised) — emit once per process

`_warn_stale_once` guards `_warn` with a module-level sentinel, because the resolver is reached up to four times in one `session-end --handoff` (R4). Return type stays `Tuple[str, str]`, preserving `test_space_in_interpreter_path_accepted`; source token stays `"fallback-stale"`; the `:705-710` branch stays keyed to `"fallback"`. The plan adds an autouse fixture clearing the sentinel between tests.

### C3, C4 — unchanged in substance

C3 adds the `_warn` in `_intent_whoami`'s swallow (`:194-197`) and corrects `:341`. C4 appends `_REBIND_REMEDY` to the messages that stay fatal. Both now also carry the R8 doctrine grounding: C3 is `doctrine/coordination.md:267` ("over-warn, never to silently drop") applied to a surface that currently does the opposite; C1's deliberate fail-open is the intentionality `doctrine/dual-review.md:229-232` demands and is prior-arted by `coordination.md:277-278`, distinguished from `:272` (degrade-to-block is right where the degraded state is safe to block in; blocking `session-start` leaves the adopter no fallback).

### Tests (revised)

Added over the original: `test_symlinked_parent_with_absent_leaf_still_refuses` and `test_symlinked_leaf_refuses` (R3); a warning-**count** assertion — exactly one occurrence of the remedy across a full `session-end --handoff` (R4); an explicit `_sibling_tool` monkeypatch in the C3 test, following `test_full_handoff_surfaces_intents` at `:297-300`, plus one test leaving `CAIRN_AGENT`/`CAIRN_SESSION` unset so the real multi-call shape is exercised (R4c); a resolver source-scan for write primitives in the spirit of `test_lifecycle_contract.py:139-148`, noting that test targets the *planner*, not this module (R11). `test_uninspectable_interpreter_path_refuses` is **retained** — now valid against the revised guard, verified — with a root/non-POSIX skip guard. The parametrize keeps four cases and pins `ids=["bad0","bad1","bad2","bad3"]` explicitly (R5b).

**Baseline, restated honestly and unchanged:** `python -m pytest bootstrap/tests` → **3 failed, 1408 passed, 3 skipped**, 1414 collected, Python 3.12.9 (not the canonical 3.13.13). The three failures are pre-existing: two `test_ast_attest.py` nodes (issue #1) and `test_evolution_infer.py::TestGateEval::test_main_suggests_and_json` (clock-expired). `test_lifecycle_failsafe.py` alone: **18 passed in 1.66s**. The suite is not green and this proposal does not make it green.

**Plan-execution prerequisite (R2b):** re-run the disposition matrix on 3.11 and 3.13 before the Decision; neither interpreter exists on this host.

**Unchanged:** no `bootstrap/_scaffold/` edit, therefore no AST re-anchor. No doctrine change, and the rate-limit bypass is not invoked and would not be available.

### Still open, still not mine to close

Both questions go to the Security Review and the Maintainer, unchanged: **is the detection downgrade acceptable** (residuals 1 and 3), and **probe before or after the symlink check** (Alternative 4 / residual 4). Alternative 2 — guidance only, C4 alone — remains the shippable fallback, and with R1 fixed it is now a real one rather than a wrapper around wrong advice.

## Review -- Gemini (External, different-agent-type) -- 2026-07-22

**Model**: Gemini 3.6 Flash / Antigravity
**Verdict**: SHIP (conditional on parallel Security Review sign-off for C1 and Maintainer resolution of risk acceptance)

### Steelman
This proposal resolves a critical day-one failure mode where conda or pyenv environment rebuilds delete the recorded interpreter binary, leaving `session-start` and goodnight handoffs refusing to run with a confusing schema-violation message. The posture ("absent degrades, present-but-wrong refuses") allows daily workflows to survive routine environment rebuilds while preserving strict fail-closed refusal for present-but-unexecutable or tampered files on disk. The revised proposal fixes the Internal panel's findings: it corrects the remedy guidance string (`_REBIND_REMEDY` instructs adopters to delete `local-env.json` first so `write_local_env` writes a fresh binding without `--force`), adds a process-level sentinel (`_warn_stale_once`) to prevent stderr warning quadrupling during handoffs, wraps `_has_symlink_component` and the probe in a unified `try...except OSError` block, and updates the test plan to relocate absent-path cases while pinning parametrize IDs.

### Critiques

* **[E1] (Verification of Corrected Remedy String `_REBIND_REMEDY`)**
  Verification of `bootstrap/_scaffold/install.py:354-355` (`write_local_env`) confirms the fix for R1:
  1. `write_local_env` returns `skipped-exists` when `dst.exists() and not force`. Therefore, re-running scaffold install with `local-env.json` present silently skipped rewriting the stale path.
  2. Prompting adopters to use `--force` was dangerous because `--force` overwrites all customized files in the target tree (`bootstrap/_scaffold/cli.py:136-143`).
  3. Correcting `_REBIND_REMEDY` to instruct adopters to **delete `dev/.cairn/local-env.json` first, then re-run install** guarantees that `dst.exists()` is False, writing a fresh binding safely without requiring `--force`.

* **[E2] (Verification of Warning Multiplicity Control `_warn_stale_once`)**
  `_resolve_interpreter` is called up to four times during a full `session-end --handoff` (`_intent_whoami:195`, `cmd_session_start:698`, `_do_reflection:1051`, `_do_full_handoff:1155`). Guarding `_warn` with the process-level `_warn_stale_once` sentinel prevents stderr quadrupling, ensuring adopters receive exactly one clear warning per run.

* **[E3] (Verification of Test Plan Soundness & Frozen Gate Manifest Handling)**
  * The test plan in `bootstrap/tests/test_lifecycle_failsafe.py` correctly relocates `/usr/bin/python --foo` and `/no/such/python` out of `test_tampered_local_env_refuses` into `test_stale_interpreter_path_degrades_with_guidance`, and adds a present-but-non-executable file (created without `+x`) and a directory case to `test_tampered_local_env_refuses`.
  * Preserving `ids=["bad0", "bad1", "bad2", "bad3"]` on the parametrize decorator prevents pytest collection ID shifts.
  * Because `test_lifecycle_failsafe.py` is in `frozen_files` of `gate_manifest.json`, editing it requires a supervised re-anchor via `_gate_reanchor.py`.

* **[E4] (Non-Security Boundary & Security Review Partition)**
  The non-security aspects (remedy text accuracy, warning sentinel, docstring fixes, and test structure) are coherent and verified. The two risk-acceptance questions (whether the detection downgrade for absent paths is acceptable, and probe ordering relative to symlinks) are properly partitioned and reserved for the parallel Security Review and Maintainer.

### Coverage

* **Covered**:
  * Inspected `_resolve_interpreter`, `_has_symlink_component`, and `_intent_whoami` in `templates/skills/_lib/lifecycle.py:315-395` and `tools/lifecycle.py`.
  * Checked `write_local_env` behavior in `bootstrap/_scaffold/install.py:335-369` and `cli.py:489`.
  * Analyzed failsafe tests in `bootstrap/tests/test_lifecycle_failsafe.py:216-287`.
  * Verified `gate_manifest.json` frozen files entries.
* **Not covered**:
  * Parallel Security Review pass (running separately).
  * Execution on Python 3.11 and 3.13 (to be verified during plan execution).

## Security Review -- Codex (dedicated Security Review) -- 2026-07-22

**Role and partition.** This is the Maintainer-ordered Security Review of the
read path, not the parallel External gate and not a recommendation on whether
the proposal as a whole should land. Scope was
`templates/skills/_lib/lifecycle.py:182-210` (`_intent_whoami`) and
`:318-394` (`_has_symlink_component` / `_resolve_interpreter`), plus the eager
resolver calls at `:701` and `:1158`. The write path was inspected only to
confirm the scope fence: `bootstrap/_scaffold/install.py:337-369` is unchanged,
and the proposed degraded path does not rewrite the binding.

**Security adjudication: ACCEPT the absent-path detection downgrade, REQUIRE
absence classification after the symlink walk.** This sign-off is conditional
on S1's record correction before Decision and on the revised tests actually
passing during implementation. It accepts a narrow risk trade, not the broader
claim that the current binding authenticates an interpreter.

### Trust-boundary classification

`dev/.cairn/local-env.json` starts as project-produced input, but the reader has
no provenance or integrity signal after installation: it is untracked,
gitignored, mutable, and not lockfile-covered. For this review it is therefore
**user-controlled at read time**. JSON loading does not execute code; the
security boundary is the later use of its string as argv[0]. The subprocess
sites correctly avoid a shell and pass an explicit argv list, so argument and
shell injection are not the issue. Executable selection is.

### Findings

* **[S1] Important, blocking record correction -- the proposal overstates
  shape validation as tamper detection.** The threat-model claim that an
  attacker-controlled redirect becomes loud is false for the most direct
  redirect: the current resolver accepts any absolute, present,
  non-symlinked, executable regular file. It checks neither Python identity nor
  binary provenance. Executing the current code on Python 3.13.13 confirmed
  that a shell script satisfying those shape checks is selected and run.
  **Attack scenario:** a writer changes `local-env.json` to an existing regular
  executable they control; the next routine executes it without a warning.
  **Satisfier:** before Decision, append a correction classifying the file as
  an operationally trusted executable binding and the resolver as a strict
  *shape* validator, not an authenticator. Remove or qualify the statements
  that redirect tampering is necessarily loud and that refusal is the only
  control. This is a record correction, not a request to add binary attestation
  to C1.

* **[S2] Important, pre-existing residual -- the symlink walk has a
  check/use race.** On both the current resolver and an in-memory implementation
  of revised C1, I replaced a checked real parent with a symlink after
  `_has_symlink_component` returned and before execution. The selected lexical
  path then executed the retargeted shell script (`BASELINE_RACE_EXECUTED` on
  current code; `RACE_EXECUTED` on revised C1). **Attack scenario:** a process
  able to rename an interpreter parent wins the narrow interval between the
  symlink walk and subprocess execution. **Disposition:** I do not accept this
  residual as closed or describe the symlink guard as race-free. It predates
  C1 and the absent branch does not create it; the attacker prerequisites also
  generally permit replacing the interpreter directly, so it does not block
  this bounded downgrade. Register it separately if Cairn intends this binding
  to resist a concurrent local writer rather than merely detect static bad
  shapes.

* **[S3] Important carry-forward, non-blocking to C1 -- native Windows execute
  semantics remain unverified.** No Windows host was available, so the
  universal statement that every present non-executable file refuses is not
  security-verified there. `os.access(..., os.X_OK)` is unchanged by this
  proposal, and the POSIX disposition is verified across every supported
  Python minor. **Satisfier:** do not claim the present-non-executable leg as a
  cross-platform verified guarantee until a native-Windows production-path
  test exercises it; carry the limitation as an explicit residual meanwhile.

### Required risk rulings

**1. Detection downgrade -- accepted.** The absent branch never executes or
persists the recorded value. It selects `sys.executable`, which is already
running the lifecycle process, so the branch grants no executable capability
that this invocation does not already possess. A writer can force loss of path
continuity and can suppress the former hard stop, but cannot use an absent path
to choose the child executable. The loss is therefore detection/assurance, not
direct code execution. That trade is proportionate to the reproduced rebuild
failure provided the degradation remains conspicuous: one stderr warning per
process, the stale value and current interpreter named, the source reported as
`fallback-stale`, actionable non-`--force` recovery guidance, and no automatic
rewrite. The appended-argument and `ENOTDIR` shapes are included in this
acceptance deliberately; provenance cannot be inferred from an absent path's
spelling.

The delete/recreate residual was red-teamed. Recreating the recorded path after
classification did not change the current run: revised C1 still returned
`sys.executable`. Deleting a path after a `present` classification caused the
later file/execute checks to refuse. On a later invocation a recreated
executable can be selected, but S1 establishes that the current resolver would
already select that executable if it had been created first; the downgrade
adds no new capability.

**2. Probe ordering -- symlink first, then absence.** This is required, not a
preference. Probing first would intentionally erase the symlink guard exactly
when a symlink target is absent, even though the component remains retargetable
out of band. A benign rebuild through a newly symlinked parent must take the
fatal path plus rebind remedy. The revised `_probe_interpreter` ordering is the
accepted ordering: walk every component first, then classify
`FileNotFoundError` / `NotADirectoryError` as absent, with the whole
classification normalized through the outer `except OSError`.

### Pre-existing fail-open ruling

`_intent_whoami`'s broad `except LifecycleError` is in scope because it is a
reader call site and currently removes the only detection signal for every
invalid binding shape. It does **not** need a separate record: retain C3 in this
proposal. Keeping its fallback non-fatal is acceptable because the intent tool
is optional, its script is repository-controlled, and it runs under the
interpreter already executing the lifecycle command. The catch must surface
the original refusal reason before fallback, and the resolver docstring must
state this exception instead of claiming universal pre-execution refusal.

### Governance recommendation

**Yes -- register this boundary on `AGENTS.md`'s high-risk-surface list in a
separate follow-up.** The standing trigger should cover the local interpreter
binding, `_resolve_interpreter`, and every call site that executes its result;
changes to schema, validation order, fallback/disposition, warning visibility,
or subprocess use should require Security Review. The module-level rule already
says a moved or widened trust boundary triggers review, but the current
operational list does not make this existing executable boundary discoverable.

### Execution evidence and negative space

The revised classifier/disposition matrix was executed, not inferred, on
Python **3.11.15**, **3.12.9**, and the canonical **3.13.13** on macOS as a
non-root user. All three agreed on absent, `ENOTDIR`, symlinked-parent,
unreadable-parent, delete/recreate, and present-then-delete dispositions; 3.12
and 3.13 also ran the complete structural matrix. Unreadable parents became a
clean `LifecycleError`; symlinked leaf/parent stayed fatal; absent and
appended-argument-shaped paths degraded; present non-executable files and
directories refused. The once-per-process stale-warning sentinel emitted once
across repeated stale resolutions.

Not covered: native Windows execution, a real conda rebuild whose rebuilt
parent is a symlink rather than the equivalent filesystem shape, and a design
that closes S2's concurrent check/use race. No network, credential, or shell
surface exists in the reviewed branch.

## Decision -- {{Maintainer}} -- {{YYYY-MM-DD}}

*(Awaiting the Maintainer. The revised proposal has cleared Internal and External non-security reviews. Two decisions belong to the Maintainer with Security Review input: (1) Whether the detection downgrade for absent paths is acceptable; (2) Whether to probe before or after the symlink check.)*
