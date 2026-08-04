<!-- claim-check-allow: scripts/_onboarding/ -->
# SAFETY.md — bootstrap safety constraints (R-I)

This document states the safety rules that govern every Cairn
bootstrap run.  They are **non-negotiable** — they do not bend
when a project is in a hurry or a block slot needs rich content.

The bootstrap's scope is *installation*: reading the Cairn
`templates/` tree and writing a customized copy into a target
repository.  The safety rules define what is permitted in that
scope and what is not.

---

## Rule 1 — No private target content enters Cairn

The bootstrap **never** reads content from the target repository
and writes it into the Cairn repository itself.  The Cairn repo
is a public Open Science artifact; the target repo may be private,
proprietary, or under embargo.

**What the bootstrap may do**: read target-repo files during Act I
to fill out the assessment profiles (the Project Profile and Team
Profile).  Those profiles are written into `dev/.cairn/` *in the
target repo* (the adoption-state home, beside the lockfile + install
config), not into Cairn.

**What the bootstrap must not do**: copy architecture diagrams,
scientific data, source code snippets, or any other target-repo
content into any Cairn file.

If a case study is written for a target project and it will appear
in the Cairn `case-studies/` directory, the Maintainer must
explicitly approve each piece of content before it is committed to
Cairn.  See Rule 5.

## Rule 2 — Generated files carry no sensitive data

Every file the bootstrap writes into the target repository must be
free of:

* **Secrets and credentials**: API keys, passwords, tokens, private
  keys — none of these belong in `AGENTS.md` or any `dev/` file.
* **Local filesystem paths**: a path like
  `/Users/jsmith/projects/mymodel/` in a committed file is a
  privacy leak and a portability hazard.  Use repository-relative
  paths or environment variables.
* **Proprietary data**: model calibration data, restricted
  observational records, or any data the project cannot release
  publicly.

The block slot `project-conventions` in `AGENTS.md` is the most
likely location for a privacy violation — the agent filling it
should describe development habits and pitfalls without encoding
any of the above.

## Rule 3 — Case studies require explicit Maintainer approval

Before any case-study content is committed to the Cairn
`case-studies/` directory, the Maintainer of the *target* project
must explicitly approve:

1. That the project may be named publicly as a Cairn case study.
2. That each piece of content (the dimension profile, the narrative,
   any empirical data) is cleared for public release.
3. If the target project is under a publication embargo: that the
   case study does not disclose embargoed results or data.

This approval must be recorded in a committed note (e.g., in the
Cairn plan or a `dev/strategy/` note in the target repo) before
the case-study file is written.

## Rule 4 — External issue drafts require Maintainer approval

If the bootstrap or a bootstrapped agent drafts an issue for an
external project (e.g., an upstream library bug report in
`dev/.cairn/`), the Maintainer must review and approve
the draft before it is posted externally.  The bootstrap does not
post anything to external systems.

## Rule 5 — The bootstrap does not read from the internet

The scaffold script (`scaffold.py`) and the Act I–II procedure do
not make network requests.  If the Act I assessment requires
reading external documentation (e.g., a library's API docs), the
agent may fetch it interactively — but this is Act I *research*,
not a bootstrap operation, and the fetched content must be
summarized in the profile files, not embedded verbatim into Cairn.

## Rule 6 — Vendor-addendum files do not contaminate shared files

A target project may use a specific AI tool and want tool-specific
habits in a vendor addendum file (e.g., `CLAUDE.md`).  That file
may contain tool-specific vocabulary.  The shared `AGENTS.md` and
all `dev/` files must remain **vendor-neutral**: no model names,
no vendor API references.

If the bootstrap or a customizing agent adds a vendor addendum,
the addendum must:

1. Begin by importing `AGENTS.md` (so the shared content stays
   single-sourced).
2. Contain only tool-specific habits that do not apply across
   tools.
3. Not be confused with the shared `AGENTS.md` — it is a
   supplement, not a replacement.

## Rule 7 — Templates are agent-executed instructions

Cairn's templates, doctrine, and case-study prose are forked into
adopter repositories and **auto-loaded by AI agents as governing
instructions**.  Cairn is, in effect, a *supply chain of
agent-executed instructions*, and an upstream compromise has an LLM
blast radius: a hidden instruction injected into a template reaches
**every downstream adopter's agents at once**.

Therefore **template integrity is a security property**, not only a
correctness one.  Every change to agent-loaded content is reviewed
for *injected, hidden, or unsafe instructions* — not just for whether
the prose is right — and must pass the content-integrity scanner (`content_scan.py`, run by
[`check_cairn.py`](../scripts/check_cairn.py)).  The review threshold
scales **by file class**:

* **Source template → instruction file** (the core `AGENTS.md`
  template, the `dev/` templates) — strictest: full scanner +
  injection-review on every change.
* **Doctrine** (`doctrine/*.md`, the module templates) — scanned;
  injection-review on change.
* **Docs / case-study prose** (`docs/*.md`, `case-studies/*.md`) —
  scanned, lighter threshold.
* **Executable code** — Layer 4 (Bandit + the symlink/containment
  hardening), not the prose scanner. This class is the **whole shipped
  Python surface**, not only the scaffold: the scaffold engine — the thin
  **launcher + facade** `bootstrap/scaffold.py` over the private
  `bootstrap/_scaffold/` **engine package** (eight owned modules —
  `security`, `slotmerge`, `merge`, `config`, `lockfile`, `install`,
  `upgrade`, `cli` — plus the verifying loader `_guard.py`; *every module
  under that package is Layer-4 code*, scanned **recursively**) — *and*
  every verbatim reference script the scaffold
  installs into an adopter (`claim_check.py`, `lifecycle_metrics.py`,
  `intent.py` — now a thin facade over the owned `_intent/` package whose
  **git-hook installer `_intent/hooks.py` writes executable hooks into
  `.git/hooks/`**; each of the seven `_intent/*.py` engine files is Layer-4
  code, covered automatically because all seven are verbatim
  `_MODULE_MAPPINGS` install specs; `onboarding_activate.py` — likewise now a
  thin facade over the owned `_onboarding/` package (seven engine files) whose
  **write-containment guards** (`_assert_safe_write` / `_assert_safe_read` /
  `_assert_safe_dir_for_glob` + the `OnboardingError` / `OnboardingSecurityError`
  taxonomy) live **single-source** in `_onboarding/security.py`; unlike the
  others it installs via the engine function `install_onboarding()` (not
  `_MODULE_MAPPINGS`), which fans the package out verbatim into
  `scripts/_onboarding/` through `_assert_safe_write`, so all seven files are
  Layer-4 code reached by the recursive `scripts/` + `bootstrap/` scan; plus
  `link_check.py`, `sync_doc_snippets.py`, and the
  `content-security` / `python-security` apparatus —
  `content_scan_runner.py`, `run_security_audit.py`; **plus the two
  session-lifecycle tools `lifecycle.py` → `tools/lifecycle.py` and
  `lifecycle_planner.py` → `tools/lifecycle_planner.py`**, which install
  verbatim and **unconditionally** to every adoption as the command-line
  backend behind the `session-start` / `session-end` routines) *and* Cairn's
  own dev tools (`check_cairn.py`, `content_scan.py`, `security_check.py`,
  `verify_integrity.py`). The Bandit gate derives its scan set from the
  **published install manifest** — every file the scaffold ships
  byte-for-byte as Python, the same enumeration behind
  `scaffold.py --manifest` — plus `scripts/` + `bootstrap/`,
  and it **recurses the `bootstrap/_scaffold/` engine package** (excluding the
  `bootstrap/tests/` attack fixtures), so a newly-shipped script *or a
  newly-extracted engine module* is covered automatically; a reviewer must
  know a change ships **as code** (Layer 4), not prose.
  **What that derivation closes, and the residuals it does not.** The manifest
  unions the four delivery registries that reach it — `_CORE_MAPPINGS`,
  `_SKILLS_MAPPINGS`, `_ALWAYS_ON_MAPPINGS`, `_MODULE_MAPPINGS` — so a
  verbatim script added to `_SKILLS_MAPPINGS`, `_ALWAYS_ON_MAPPINGS` or
  `_MODULE_MAPPINGS`, not `_MODULE_MAPPINGS` alone, is scanned with no gate
  edit. **Two residuals remain, and both are live rather than theoretical:**
  * `_CORE_MAPPINGS` reaches the manifest but is emitted
    `verbatim=False` unconditionally (`install_manifest` builds its rows as
    `[(src, dst, False) for src, dst in _CORE_MAPPINGS]`), while
    `scan_targets()` filters on `verbatim and src.endswith('.py')`. A `.py`
    added there therefore **cannot** be scanned by the gate. Measured
    2026-08-03: 17 core rows, none verbatim, and no `.py` among them today.
  * `_OPTIONAL_TEMPLATES` in `bootstrap/_scaffold/config.py` ships axis-gated
    project-root templates and never reaches the manifest at all (and installs
    token-substituted, so the `verbatim` filter would drop it even if it did).

  Both residuals are held **by the dev suite, not by the gate** —
  `test_every_templates_py_on_disk_is_release_scanned` in
  `bootstrap/tests/test_security_lint.py` globs `templates/` **on disk** and
  subtracts the scan set, so a shipped-but-unscanned `.py` reddens it wherever
  it was registered. Verified by perturbation, 2026-08-03: writing a real
  `.py` under `templates/optional/` reddens that node (with
  `test_templates_py_count_is_pinned` and
  `test_the_on_disk_oracle_goes_red_when_a_registry_stops_delivering`), while
  `test_a_templates_py_no_registry_delivers_is_reported_unscanned` — which
  builds its own `tmp_path` tree and never reads the real `templates/` —
  **passes**, and so cannot hold either residual.
* **Generated instruction files** (a scaffolded `AGENTS.md` / `dev/`
  tree) — strictest overall; see Rule 8.

The scanner is a **witness, not a safety proof** — a high-noise,
incomplete tripwire that *forces* human review.  It never certifies a
template safe; a clean scan plus a by-class human injection-review is
the bar.

**Documented residual risks (Layer 4).** Two findings are *consciously
accepted* under the stated threat model (no concurrent filesystem
attacker; no untrusted code path), recorded here so a future reviewer can
tell "known and accepted" from "missed": (1) a small TOCTOU window between
the scaffold engine's `_assert_safe_write` containment check and the write
(the check lives in `bootstrap/_scaffold/security.py`, its single-source
identity preserved across the split; the onboarding helper's own
`_assert_safe_write` / `_assert_safe_read` / `_assert_safe_dir_for_glob` guards,
now single-sourced in `_onboarding/security.py` after the onboarding-split,
share the same consciously-accepted window under the same threat model); and
(2) `check_cairn.py`'s `importlib.exec_module` of sibling tools from
**fixed, script-relative** paths (a deliberate dogfood composition, not a
dynamic-exec vector). See `../SECURITY.md` for the public statement.

## Rule 8 — The bootstrap profile is operationally-trusted input

The scaffold substitutes profile token values **verbatim** into
agent-loaded files, so a profile is itself part of the
instruction supply chain.  Profiles are therefore treated as
**operationally-trusted input**:

1. **Committed and reviewed as code** — never pulled from a chat
   message, email, or issue comment at scaffold time.
2. **Diffed against the generated output** — confirm the token values
   land where expected and inject no instruction text into the
   generated `AGENTS.md` / `dev/` tree.
3. **Never run from an untrusted third party** unreviewed — a hostile
   profile can inject downstream-agent instructions through a token
   value (a static, supply-chain variant of prompt injection).

Any sample profiles Cairn ships are part of the same supply chain and
get the same review + scan.  See
[`PROVENANCE.md`](PROVENANCE.md) for the release-provenance controls
(Layer 1) these rules rest on.

---

## Rule 9 — No secret-bearing substitution tokens

The install lockfile (`dev/.cairn/cairn-lock.yml`; see [`UPGRADE.md`](UPGRADE.md))
records the **token values** substituted at install into a **tracked**
file — so a substitution token that carried a secret would leak it into
version control.  Therefore: **Cairn templates must not introduce
secret-bearing substitution tokens** (passwords, API keys, access tokens,
credentials).  A token is for benign, reviewable configuration
(`project_name`, `test_command`, a command path), not for a secret.

The lockfile writer enforces this mechanically: it **refuses** to record a
token whose name looks secret-bearing (`password`, `passwd`, `secret`,
`credential`, `token`, `key`) unless that name is explicitly allow-listed.
This is the same coordination-files-carry-no-secrets posture as Rules 1-2,
applied to the substitution surface.

---

## Self-check before committing any bootstrap output

Before committing bootstrap-generated or bootstrap-customized
files, verify:

```
grep -rni \
  'password\|token\|secret\|api.key\|private.key\|BEGIN PRIVATE\|BEGIN RSA' \
  <target>/AGENTS.md <target>/dev/
```

```
grep -rn '/Users/\|/home/\|C:\\Users\\' \
  <target>/AGENTS.md <target>/dev/
```

Both commands should return zero matches.
