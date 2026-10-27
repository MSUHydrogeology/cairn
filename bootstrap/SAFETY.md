<!-- The two `scripts/*_security.py` globs are ADOPTER-tree install destinations
     of Rule 11's two team-gated modules. Cairn does not select those modules on
     itself, so the paths deliberately do not resolve here; the reviewed sources
     are `templates/modules/team-gated/api_access_security.py` and
     `templates/modules/team-gated/web_hosting_security.py`.
     `scripts/run_security_verification.py` is the same class for a DEFAULT-ON
     module: it is the adopter-tree destination of the security-verification
     dispatcher, which Cairn deliberately does not self-host (see that plan's
     Scope, "Cairn does not self-host the dispatcher"). Its reviewed source is
     `templates/modules/default-on/run_security_verification.py`, which the
     Rule 7 self-check greps directly for exactly this reason. -->
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

**Scope: the installer, not what it installs.**  This rule is about the
*bootstrap* — the scaffold and the two Acts.  Cairn now also **ships**
modules whose installed scripts do open network connections when an
adopter runs them.  That is Rule 11, and Rule 5 says nothing about it.
Reading Rule 5 as "nothing Cairn ships touches the network" is a
misreading this paragraph exists to prevent.

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
the prose is right — and **must pass** the content-integrity scanner
(`content_scan.py`, run by [`check_cairn.py`](../scripts/check_cairn.py)).
**Two triggers exist and neither fires on a commit**: the suite scans
generated output and the skills artifacts on every `pytest` run, and
`check_cairn.py` scans the tracked Markdown files **its default filter
keeps** when a person runs it (the **maintainer-run** release gate
`security_check.py` invokes it, when a maintainer runs that).  That
filter is not a formality: `main` wraps the tracked list in
`link_check.filter_sources`, which drops four classes by default —
`dev/**/archive/`, `dev/modules/`, `dev/.cairn/` and `dev/reflections/`,
each re-includable by flag.  **249 tracked, 195 scanned, 54 skipped**
(`as_of 2026-08-04`); the run's own "N Markdown file(s) scanned" banner
is the honest number.  Everything skipped is under `dev/`, so
`doctrine/`, `docs/`, `case-studies/`, `bootstrap/` and `templates/`
are all reached — but `dev/modules/` is **vendored, agent-loaded
content that a default run does not scan**.  Source prose that no
scaffolded profile emits — **including** `doctrine/`, `docs/`,
`case-studies/` and this document — is reached **only** by that manual
run.  **Running it, and resolving what it flags to a clean scan, is the
reviewer's obligation, not a mechanism's guarantee.**  The review threshold
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
  `_MODULE_MAPPINGS` install specs; plus
  `link_check.py`, `sync_doc_snippets.py`, and the
  `content-security` / `python-security` apparatus —
  `content_scan_runner.py`, `run_security_audit.py`; **plus the session
  kernel `session.py` → `tools/session.py` and the board view
  `board.py` → `tools/board.py`**, which install
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
  unions the three delivery registries that reach it — `_CORE_MAPPINGS`,
  `_SKILLS_MAPPINGS`, `_MODULE_MAPPINGS` — so a verbatim script added to
  `_SKILLS_MAPPINGS` or `_MODULE_MAPPINGS`, not `_MODULE_MAPPINGS` alone, is
  scanned with no gate edit. **Two residuals remain, and both are live rather than theoretical:**
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
identity preserved across the split; installs made before 0.5 keep the retired
onboarding helper, which Cairn no longer scans, until `upgrade --remove-retired` removes it,
and its accepted residual risk is this same race window; the
session kernel `tools/session.py` has it too, for a parent folder swapped for a
link between its `_assert_not_linked` check and a write -- the last name is not
exposed, because its writes are an exclusive temp file and a rename); the
model-selection capture, lockfile writers and `.gitignore` append now use the
same replacement pattern, so a won race at the last name overwrites rather
than appends, while a swapped parent remains in the accepted window; and
(2) `check_cairn.py`'s `importlib.exec_module` of sibling tools from
**fixed, script-relative** paths (a deliberate dogfood composition, not a
dynamic-exec vector). See `../SECURITY.md` for the public statement.

**The delete beside the write (Layer 4).** `upgrade --remove-retired` is the
engine's only deletion of a project file, and it is held to the write's rules.
It removes a file only if the path is on Cairn's own list, the bytes match a
digest on that row, and the project's last commit holds the same bytes
(`_committed_copy_matches`, which runs `git cat-file` under a fixed command and
environment so that no program named in the project's `.git/config` runs). The
removal itself (`_remove_unchanged_file`) calls `_assert_safe_write`, then,
where `os.unlink` takes `dir_fd`, opens each folder down to the file without
following links and reads, re-checks and unlinks the file by name through the
last handle. A folder swapped for a link after that check then cannot redirect
the removal; a same-user racer who wins the last instant can remove only a name
inside the project. **On Windows there is no `dir_fd`**: the removal goes by
path, and a folder swapped for a link between the check and the unlink can
redirect it, which is the same accepted window as for the write. Windows also
looks a bare `git` up in the current folder before `PATH`, and the scrubbed
environment does not close that, so run the step from a folder you trust.

**The edit check beside it.** The check that stops `upgrade --apply` or a bare
`--finalize` from overwriting a file with unsaved edits, and warns under
`--stage`, runs no program the project names either: it asks git only for the
index and the last commit through the same launcher (fixed overrides, a scrubbed
environment, lazy fetch off), never runs `git status`, and reads each file
itself through `_assert_safe_write` and `_read_regular_bytes`; when git cannot be
relied on to answer, it stops and names `--force` instead of guessing.

**Documented residual risk: the interpreter binding proves only "git does not
list it now".** The session kernel (`tools/session.py`) runs the program named
in `dev/.cairn/local-env.json`. It does so at `session-start`; at
`session-end --handoff`; and whenever it asks the intent tool for the agent or
session name, which `session-end` also does when `CAIRN_AGENT` or
`CAIRN_SESSION` is not set. Before it runs the program, it refuses a binding
that git's index lists (and one behind a link, inside a submodule, or that git
cannot be asked about). That check stands in for the real question, "was this
file written on this machine?", so a binding that came with the project by
another route is used and its program is run. Five routes are known: a
downloaded archive of a repository that tracked the binding, followed by
`git init`; `git apply` of a patch that creates the file; `git reset` after the
commit that added it; `git rm --cached`, the common "untrack but keep" idiom;
and a copy of the whole working folder (a zip, a synced or shared drive, a
lab-mate's copy), because git ignores the binding, so it travels with the
folder. The copy route also needs the named program to exist at the same
absolute path on the new machine; that is read from the code, not run.
Consequence: a project can choose which program the kernel runs, on a machine
where the operator took the project that way. The binding needs only an
executable file, so the arguments the kernel passes do not limit what runs: it
can be any program, and it runs with the operator's own permissions. The gate
has never been run on Windows or on an HFS+ volume (its tests skip on Windows,
and a run on each is still owed), so what it does when a disk treats two
spellings of one name as the same file is shown only for the disks tried. On a
disk that reports the same inode number (0) for every file, the identity checks
are skipped and only the checks by folded name run; I do not know which real
disks do this. The Maintainer accepted this on 2026-10-19, in writing here and in
the `_resolve_interpreter` docstring, as the interim position, and accepted the
wider description above on 2026-10-26. The full fix is a
separate later proposal and Security Review: keep the binding inside git's own
folder (`git rev-parse --git-common-dir`), where no checkout, archive, patch
or download can carry a file, and read the old path only to say it is no longer
used. Until then the operator's protection is to run `session-start` only in
projects obtained by `git clone` or `git checkout`, and to read a project's
`dev/.cairn/` before trusting it.

### The default-on security-verification dispatcher — a shipped file that runs a child

`security-verification` is **default-on**, so this is Layer-4 code in
*every* adoption, not an opt-in surface. It is recorded here rather than
under Rule 10 or Rule 11 because it triggers neither: it resolves no
executable from `PATH` (its argv head is `sys.executable`) and it opens no
socket. Five facts, and (d) is the one that must not be softened.

* **(a) The scaffold now ships a file that executes a child process in an
  adopter tree.** `scripts/run_security_verification.py` launches a
  capability's own local runner as `[sys.executable, "-I", <registry runner
  path>, <registry argv mode>]`, `shell=False`, under a timeout and an
  output byte cap, with strict UTF-8 and strict JSON on the way back. Every
  element of that vector comes from the **source-owned registry inside the
  dispatcher file**; no adopter file — not the profile, not the lockfile,
  not a policy file — can add, steer, or substitute a child.
* **(b) Dispatch is gated on lockfile integrity and parent-computed
  digests.** The parent hashes the runner's bytes itself and compares
  against the lockfile record; a mismatch, a missing record, an
  unrecognized record key, or a symlinked runner or policy (leaf or parent
  directory) is **DEGRADED (20) with no child launched**. A digest the
  *child* reports is never read. Accepted residual, stated not closed: a
  same-user race between the digest read and the launch, on a trusted
  checkout, under the same threat model as the TOCTOU window above.
* **(c) The child's environment is reduced from ambient.** The child gets
  an explicit minimal `env`, not a copy of the parent's; proxy variables
  (`HTTP_PROXY`, `HTTPS_PROXY`, `ALL_PROXY`, `NO_PROXY`) and
  credential-bearing variables are stripped rather than filtered. Raw child
  stdout and stderr are **never relayed**, at any aggregate level, so a
  child cannot paint the operator's terminal or forge a banner.
* **(d) Command separation is not actor authentication.** The local /
  deployed split is a *command* boundary. Anyone — person or agent — with
  shell access in the tree can invoke another script directly, and **Cairn
  does not claim to distinguish a human process from an agent process.**
  Nothing in this apparatus authenticates who is running it.
* **(e) The dispatcher, its source-owned registry, its child result schema,
  its binding-mode schema, and every registry entry are high-risk
  Security-Review surfaces.** That designation is carried on **three**
  channels, of which **two are tamper-evident** — the lockfile-recorded
  `dev/modules/security-verification.md`, and the hash-pinned dispatcher
  source itself, where the designation sits as a comment block at the
  registry definition site so a registry change and its review trigger are
  one artifact — **and one is not**: the adopter's `AGENTS.md` slot, which
  `<!-- cairn:customized -->` exempts from both the merge and the fidelity
  check. **An adopter who customizes that slot removes the designation from
  their governing document with no side file and no warning from any Cairn
  tool.** (e) is a **recorded residual, not a claim of coverage**; it is
  pinned as a characterization test, not closed.

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

## Rule 10 — A shipped script that invokes a host executable declares its
trust roots, and `PATH` resolution *is* execution authority

The `portable-security-sweeps` module installs a script
(`scripts/run_portable_security_sweeps.py`) that invokes **host executables**.
That is a new boundary in this module family, and the distinction matters: the
existing `python-security` runner executes `[sys.executable, "-I", "-m", …]` — a
known interpreter — and uses `which()` only as *presence detection*. This runner
executes **whatever `PATH` resolves**, so **`PATH` resolution is execution
authority**, not a lookup.

1. **The trust roots are enumerated, never generalized.** Exactly two:
   **`gitleaks`** (the adapter) and **`git`** — invoked by the runner for its
   pre-execution configuration screen, and invoked **transitively by Gitleaks**
   for the history leg. The second fact was found by *executing a logging shim*,
   not by reading documentation, and it was absent from the first enumeration of
   this module's trust set.
2. **Validation is shape and containment, never provenance.** Absolute path;
   regular file; executable bit; and **neither the lexical nor the resolved path
   inside the tree under check** — a package-manager symlink is fine, a symlink
   whose target resolves into the candidate tree is refused. Both paths are
   checked, because each catches a case the other passes.
3. **The only CLEAN-capable mode requires a digest match.** The resolved
   executable is hashed immediately before invocation and compared against the
   admitted-artifact set. A **recorded** digest that does not match is a
   contradiction → DEGRADED. **No** recorded digest for this
   `(version, platform, architecture)` is the ordinary unadmitted case → the
   reduced path, which can never report clean.
4. **Everything under the candidate's `.git/` is candidate-controlled input** —
   repository-local configuration, refs, shallow boundaries, remote metadata,
   `.gitattributes`, and any `.gitleaksignore`. Two controls, and their honest
   descriptions differ:
   * a **deny-by-default pre-execution screen** over the *include-expanded*
     repository-local key set, which is what actually bounds the configuration
     surface; and
   * **counted Git config keys** on the child, which are **defence in depth over
     the keys they name and not a boundary** — measured, a candidate steps around
     them with one `include.path` line or one `includeIf`, and Git offers no way
     to disable the repository-local tier at all.
5. **The accepted residual is printed, not only documented.** Both
   pre-execution screens are **snapshots**: a same-user delete/create race
   between the screen and `exec` on a trusted checkout is accepted and named in
   the runner's own report, not left in a doctrine file an adopter may never open.
6. **No child output is relayed.** Adapter stdout and stderr never reach the
   operator verbatim; every displayed string is rendered
   `ensure_ascii=True`; and no secret-bearing result field is selected into any
   sink.

**Any future shipped script that resolves an executable from `PATH` takes the
same treatment**, and the change takes a Security Review.

---

## Rule 11 — Cairn ships network egress, bounded by the connected peer

Two selectable, team-gated modules — `api-access-security` and
`web-hosting-security` — install scripts that **open outbound TCP connections
and speak HTTP/HTTPS**.  Nothing in the scaffold does this; Rule 5 remains true
about the installer and says nothing about what the installer installs.  This
rule is what covers the shipped runners, and it states the controls *and* what
they leave open.

Both capabilities are **explicit-selection only** — no preset selects them and
they are not in the default-on set — and each installs a facade
(`scripts/api_access_security.py`, `scripts/web_hosting_security.py`) over one
shared four-member engine package installed once per capability.  The engine is
**standard-library-only**; see
[`DEPENDENCY_BUDGET.md`](DEPENDENCY_BUDGET.md) > *No exception*.

1. **The controlling property is the *connected peer*, not the requested
   address.**  All addressing and all socket work live in one function —
   `open_validated_connection` in the shipped
   `_security_net/net.py` — and nothing else in the package opens a socket.  It
   resolves **once**, refuses the **whole** answer set if *any* member falls
   outside the permitted address classes, connects to a literal address from
   that validated set, and then re-reads `getpeername()` and refuses unless the
   peer is **both** in the validated set **and** in a permitted class — closing
   the socket before one application byte is written.  There is no second
   lookup between validation and connection, which is the DNS-rebinding window;
   and the peer check is what makes the classification an SSRF control rather
   than a hint.  A module seam between "classify" and "connect" would be an
   invitation to a caller that skipped one, so there is no such seam.
2. **Two legs, two disjoint address classes, and the split is the design.**
   The agent-facing `local` leg may reach **loopback only** — the policy host
   must be a loopback literal or the exact name `localhost`, checked as a *name
   allowlist before DNS* so a public hostname is refused without a lookup.  The
   Maintainer's `deployed-passive` leg may reach **public only**.  Neither leg
   can be talked into the other's class by a policy field.
3. **Redirects are classified, never followed, and never resolve an
   attacker-chosen name.**  A `3xx` terminates the call with a fixed refusal
   token.  A `Location` host outside the policy's exact allowlist is refused
   **without a DNS lookup**, so the engine cannot be used as a resolver for a
   name of the peer's choosing.  Because nothing follows a redirect, nothing
   authenticating is ever carried to a second origin — there is no second
   request.
4. **TLS is platform-trust-store verification with no weakening path.**
   `check_hostname` is on, `verify_mode` is `CERT_REQUIRED`, the floor is TLS
   1.2, and there is **no policy field, CLI flag, or environment variable in
   either module that reaches either setting**.  On a verification failure the
   OpenSSL *code* is mapped to a fixed reason token; the human-readable
   verification message is never read, so a peer cannot choose text that
   reaches an output channel.
5. **Every read is capped and every wait is bounded.**  Connect and read
   timeouts, a request-byte cap, a response-byte cap, a header-count cap, a
   header-line cap and a status-line cap are all fixed constants in the engine,
   not policy inputs.
6. **Credentials are environment-variable *names*, derived, never values.**  A
   policy declares **ordinal** principals; the variable name is derived by the
   engine as `CAIRN_API_P<N>_CREDENTIAL` and **a policy cannot supply, override,
   or alias it** — a policy key that tries is refused by name.  The two policy
   sections' ordinal sets are disjoint by schema, so the `local` leg
   structurally cannot look up a *deployed* section's variable.  A value read
   from the environment becomes the `Authorization` header of exactly one
   request and is never printed, persisted, logged, or written to the report;
   the one place a raw exception could have carried it — a non-ASCII header
   encode error, whose message *is* the credential — is closed with a fixed
   refusal instead.  This is Rule 9's posture applied to a runtime input:
   **no substitution token, lockfile field, or installed file carries a
   secret.**  The hosting capability reads **no credential at all** and its
   deployed leg is unauthenticated in v1.
7. **Passive versus active, drawn where it actually is.**  The hosting
   capability is passive on **both** legs: declared `GET`/`HEAD` only, no attack
   payload, no crawl, no link-following, no ID inference, and it **refuses to
   issue a grade**.  The API capability's `local` leg **does** send mutation
   methods (`POST`/`PUT`/`PATCH`/`DELETE`) — that is the point of an
   authorization-denial matrix — and it is confined to loopback for exactly that
   reason.  Its `deployed-passive` leg is `GET`/`HEAD` **in code**, refused at
   schema level, so no v1 route produces a non-loopback write.
8. **A remote target is re-authorized by hand, per exact URL.**
   `deployed-passive` refuses unless `--authorize-base-url` is **byte-for-byte**
   the policy's *normalized* base URL.  The argument is deliberately not
   normalized: a trailing slash, an upper-case host, an explicit default port, a
   punycode spelling, an added query, or `http` for `https` all refuse.  Typing
   that argument is a **human act**; an agent that types it has defeated the
   control (`AGENTS.md`-level rule, and the plan's Maintainer fence).
9. **The external tools these modules evaluate are deferred, not adopted.**
   OPA, Cedar, OpenFGA, Schemathesis, ZAP, `testssl.sh`, Trivy and the MDN HTTP
   Observatory are named in the module doctrine as recommended companions,
   deferred adapters, or deliberate exclusions.  **None is installed, and
   neither runner resolves an executable from `PATH`** — so Rule 10's
   trust-root treatment does not attach to these modules, and it would attach
   the moment one of those adapters shipped.
10. **Output carries no observed content.**  Findings carry fixed check,
    operation, case and assertion identifiers, ordinal principal ids, a status
    *class* (`2xx`, not `200`), and — only where an observed value exists at all
    — a five-value magnitude bucket.  Never a value, an exact length, a member
    count, a header, a cookie, a body fragment, a certificate subject, a redirect
    URL or query, a peer-supplied reason phrase, or a credential.  **A finding
    contains no integer at all**, which closes exact cardinality as a *class*
    rather than field by field.
    The bucket is the *only* size-derived thing a finding carries; the size
    itself is discarded at the boundary, and a peer-supplied reason phrase and
    `Location` value are reduced to fixed tokens on the way *in*, so their
    content is never retained even in memory beyond the parse.  Where the API
    capability needs to correlate two equal observations it emits an HMAC-SHA-256
    fingerprint under a **per-run key from the OS CSPRNG**, truncated, never
    printed or persisted: equal within a run, different across runs, so a pasted
    report is not an offline dictionary oracle.  A failure to obtain randomness
    is a refusal raised before the first request rather than a weaker key.  The
    single report file is `report.json`, mode `0600`, in a freshly-created
    temporary directory, and no raw-response artifact is written anywhere.

**What this rule does not protect — stated because a control described past its
reach is worse than no control.**

* **Loopback is a socket property, not a fixture property.**  A loopback
  service that proxies to staging is loopback from `getpeername()`'s point of
  view.  The address check cannot attest a fixture's internals, so **local
  mutation evidence is invalid if the fixture has any upstream route** — and a
  `DELETE` you believed landed on a throwaway record can land on a real one.
  No address check closes this; the module doctrine states it as an open failure
  mode.
* **`--authorize-base-url` is structural command separation, not actor
  authentication.**  A shell process cannot prove who invoked it.  An agent
  holding the Maintainer's terminal and credentials could perform that act.
* **Sanitization protects output channels, not process memory.**  A debugger, a
  core dump, or another process running as the same user is out of reach of
  every control above.
* **The report is sanitized and is still security evidence.**  It can reveal
  operation names, principal relationships and failure counts.  The Maintainer
  reviews it before sharing it and deletes it under the project's
  evidence-retention policy.  The `0600` mode is **POSIX**; no Windows run has
  established an equivalent.
* **CLEAN is narrow.**  It means *the declared matrix or the reviewed
  expectation set held at the named target and time* — no more.  A local CLEAN
  is not a deployed CLEAN, and the runners say so in the summary, in the report,
  and in the dispatcher child document's `evidence_mode`.
* **The deployed request path is exercised only up to its refusal boundaries.**
  No test drives a deployed leg to a *successful* request: none supplies a
  deployed credential and none contacts a real host.  That is the Maintainer
  fence working as intended, and it means the successful-deployed-request path
  itself is **unexercised by Cairn's suite** — run by a person typing
  `python -m pytest bootstrap/tests`; **Cairn has no CI**.
* **Point 10 is held by *structural absence*, not by redaction — and one channel
  is recorded as uncovered.**  There is no shipped code path that writes a
  peer-supplied or credential string to stdout, to stderr, or to the report; the
  sanitizing helper is defence in depth over two fields nothing reads.  The
  cross-runner sweep (`bootstrap/tests/test_security_finding_confidentiality.py`,
  run by a person typing `python -m pytest bootstrap/tests` — **Cairn has no
  CI**) plants a distinct high-entropy marker per channel and, for **nine**
  channels, proves the runner actually reaches the channel by *injecting* the
  leak on a throwaway copy and requiring the sweep to find it, before requiring
  absence from the pristine runner.  Three more — TLS/transport exception text,
  timeout diagnostics, and the certificate subject — are closed as a **class** at
  the refusal constructor, which clamps every reason to a closed vocabulary, and
  that clamp is itself tested with a deletion mutant.  **A policy-declared
  request body is recorded as uncovered**: no finding, report field or summary
  line takes it, so its absence is asserted but its liveness is unproven.
* **Neither capability is a standing check yet.**  As of this rule they are
  **directly invocable only** — no activation-registry entry exists, so nothing
  runs them as part of a standing agent-facing command and neither is
  integrity-classified by the activation dispatcher.  A registry entry is a
  separate change with its own Security Review and its own first-use trust
  artifact.

**Any future shipped script that opens a network connection takes this same
treatment**, and the change takes a Security Review.

---

## Rule 12 — Git owns Git's facts; Cairn owns policy

Cairn does **not** reimplement a Git object algorithm when native plumbing
produces the same fact without executing candidate code or accepting candidate
policy. The division is explicit:

| property | Git owns | Cairn owns |
|---|---|---|
| committed bytes and modes | object ids, trees, `cat-file`, `ls-tree`, `hash-object` | which paths are protected, which modes are allowed |
| history | parent links, reachability, ancestry | the accepted range and its expiry conditions |
| object integrity | `fsck --strict`, fetch-time checks | when integrity is decisive, and how failure is reported |
| key authentication | signed objects and Git's verifier | the out-of-band roster and what authorization *means* |
| ref movement | expected-old transactions, `--no-deref`, reflogs | the exact ref set, the Maintainer fence, publication policy |

**A sterile context beats an enumerated pin.** Object validation runs from a
context the candidate cannot configure — a bare clone that inherits the objects
and none of its `.git/config` — rather than by pinning `fsck.*` on the command
line. Measured on git 2.53.0: a repo-local severity downgrade *is* defeated by
a `-c` pin, but `fsck.skipList` is **multi-valued**, so `-c fsck.skipList=/dev/null`
accumulates with the candidate's entry rather than replacing it. Any design that
enumerates members of an evolving config family is chasing it.

**`fsck` proves structural object integrity — nothing else.** Not
authorization, not safety, not signature validity. Result labels and prose keep
those apart, and the failure is typed distinctly from a scanner finding.

**Local hooks are not an authorization gate.** Cairn uses pre-commit and
post-commit hooks for intent coordination. They are bypassable and replaceable,
and **no decisive release, trust-root or review claim may depend only on a hook
having run.** Porcelain status and reflog output are evidence about local state,
not identity: security-sensitive decisions bind to object ids, explicit refs,
verifier exit status and pinned policy.

## Rule 13 — The re-anchor ceremony's pre-candidate trust set is enumerated,
and every member is recorded rather than resolved

The re-anchor ceremony runs a launcher (`bootstrap/reanchor-launcher.template.sh`,
instantiated by the builder and read by a fresh local reader) which verifies an authorization packet and the authority
closure **before** the first candidate byte executes. Everything the launcher
runs in that window is *pre-candidate*: it decides whether candidate code starts,
so a substituted one is not caught by anything downstream.

**The posture differs from Rule 10 and the difference is the point.** Rule 10
governs scripts where **`PATH` resolution is execution authority**. Here there is
no `PATH` resolution: every executable is an **absolute path recorded by the
Maintainer in the values file**, validated as an existing, symlink-free,
executable regular file, and invoked by that path — which no inherited shell
function or alias can shadow. Ambient discovery is the failure this design
exists to remove: it is what once let a substituted repository answer for the
named one, and a replacement `shasum` vouch for bytes it had just rewritten.

**The pre-candidate set, enumerated:**

| executable | why it is in the window |
|---|---|
| `env` | builds the sterile child for every `git` invocation |
| `git` | resolves the candidate OID once and reads closure blobs by that OID |
| `shasum` | hashes the packet, the snapshot, and every closure blob |
| `mktemp` | creates the extraction directory |
| `mkdir` | creates its subdirectories |
| `cat` | **snapshots the packet into memory before it is parsed** |

**Automatic object fetching is part of this boundary**, and it is not a
seventh tool — it is a way for the candidate to introduce one. A blob-filtered
checkout names its *promisor remote* in its own local config, which is
candidate-controlled input; pointing that at `ext::<program>` makes `git` run
`<program>` the first time it reads an object the checkout lacks. So both
sterile git environments bind **`GIT_NO_LAZY_FETCH=1`**, and they bind it rather
than inherit it: they run under `env -i`, where **absent means enabled**. An
emptied environment is not a safe environment when the safe state requires a
variable to be present. Found by exact-byte security review, reproduced through
the full launcher, and regression-tested against a real promisor checkout.

`printf`, `read`, `case`, `cd` and `pwd` are shell builtins and reach for
nothing, which is why the launcher prefers them wherever a utility would
otherwise be needed — the digest field is split with `${d%% *}` rather than
`cut`, so `cut` does not join this table.

**`cat` is the one addition this ceremony's second iteration made**, and it is
recorded here rather than acquired silently. It is needed because the packet
must be hashed and then parsed from *the same bytes*: the snapshot idiom
(`v=$("$CAT" "$PKT"; printf x); v=${v%x}`) is what preserves trailing bytes that
`$(...)` would otherwise strip. It is invoked **only through its validated
values field**, never by bare name — an executable that is trusted but unbound
can only be found through ambient `PATH`, which is exactly the gap the recorded
paths close.

**What the snapshot does not close, stated rather than implied.** The packet is
read twice — once to hash the file, once to snapshot it — so a same-user writer
can change it in between. Re-hashing the snapshot and comparing **detects**
that; it does not **prevent** it. That is Cairn's accepted same-user residual,
unchanged and not enlarged. The single-buffer property is delivered for
*parsing*; the *reading* is two passes cross-checked.

**Changes to this table, to how any member is resolved, or to the point at which
candidate code starts, take a Security Review.**

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

**And, for the default-on security-verification dispatcher** (Rule 7 >
*The default-on security-verification dispatcher*): if the change touched
`run_security_verification.py`, its registry, its child result schema, or
its binding-mode schema, it takes a **Security Review** — and the
designation must still be present on both tamper-evident channels:

```
grep -c 'high-risk Security-Review surface' \
  templates/modules/default-on/run_security_verification.py \
  dev/modules/security-verification.md
```

Both counts should be non-zero. A zero on either is the designation
having been dropped from a channel that is supposed to be hash-pinned.
