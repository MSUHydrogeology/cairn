<!-- cairn-internal-ref-allow: doctrine/runtime-contract.md doctrine/rationale.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see AGENTS.md, "Where doctrine/ references resolve") -->

# Portable security sweeps for non-Python and polyglot adopters

**Author**: Codex (Strategy, from the Security Review role)
**Model**: OpenAI Codex (GPT-5)
**Date opened**: 2026-08-03
**Status**: reviewed
**Touches**: `bootstrap/_scaffold/config.py` (module registration only), the
team-gated module catalog under `templates/modules/team-gated/`,
`bootstrap/DEPENDENCY_BUDGET.md`, `bootstrap/SAFETY.md`, adopter tool-use
documentation, the install manifest / lockfile file set, and behavioral tests
under `bootstrap/tests/`
**Deliberately not touched**: the existing `python-security` exit contract,
Bandit and pip-audit policy, default preset rosters, external-tool installation,
or the lockfile schema
**Related**: `default-security-stance`, `scan-coverage`,
`release-security-bar`, and the existing `python-security` module
**Plan review**: `required(**External**, security lens)` -- this adds external
executables and subprocess/configuration trust boundaries to a shipped security
module and changes the published install manifest

## Context

Cairn's shipped `python-security` module composes two useful but Python-specific
controls: Bandit over source and pip-audit over dependencies. That is a coherent
Python self-audit, not a portable security posture. A non-Python adopter can
install Cairn without a corresponding dependency, secret, CI-workflow, or
infrastructure sweep, while a polyglot adopter has to invent the composition.

The Maintainer asked during drafting:

> "Outside of Bandit, are there other python packages that we can/should look
> to for security sweeps? How about command line tools for those without
> python?"

and then explicitly asked:

> "Could you please write this up as a proposal?"

That is an explicit go-ahead to deliberate a new mechanism under Cairn's
standing "fix defects, build nothing new" direction. It is input to this draft,
not a Decision to implement it.

The tool landscape divides by security question, not language:

| Question | Focused tool | What it does not answer |
|---|---|---|
| Does source use a suspicious API or propagate untrusted data to a sink? | Bandit for Python; Semgrep or CodeQL for broader/deeper SAST | Whether a dependency version has a published advisory |
| Does a resolved dependency have a known advisory? | pip-audit for Python; OSV-Scanner across ecosystems | Whether the vulnerable path is reachable in every ecosystem |
| Did a credential enter the current tree or Git history? | Gitleaks or detect-secrets | Whether source logic is safe |
| Is CI configuration itself hazardous? | zizmor for GitHub Actions | Application or dependency vulnerabilities |
| Are container/IaC files misconfigured? | Trivy's misconfiguration scanner | General source-code security |

The official tool contracts support those boundaries:

* [pip-audit](https://github.com/pypa/pip-audit) audits Python environments,
  requirements, and supported lockfiles for known vulnerabilities; its own
  security model warns that auditing untrusted dependency input is not a safe
  substitute for installation isolation.
* [OSV-Scanner](https://google.github.io/osv-scanner/usage/scan-source/)
  discovers supported lockfiles and SBOMs in a source tree. Its
  [installation contract](https://google.github.io/osv-scanner/installation/)
  publishes platform binaries with SLSA provenance.
* [Gitleaks](https://github.com/gitleaks/gitleaks) scans Git history,
  directories, files, and stdin for secrets and supports redacted output.
* [zizmor](https://zizmor.sh/) statically audits GitHub Actions and supports an
  explicitly offline run.
* [Trivy filesystem scanning](https://trivy.dev/docs/latest/target/filesystem/)
  separates vulnerability, secret, misconfiguration, and license scanners.
* [Semgrep's local CLI](https://semgrep.dev/docs/category/local-and-cli-scans)
  supports project-specific source rules, while deeper interfile analysis and
  mutable remote rule registries introduce a materially larger policy surface.
* Ruff's [flake8-bandit `S` rules](https://docs.astral.sh/ruff/rules/) are
  Bandit-derived coverage. They are useful fast feedback when Ruff is already
  installed, but not an independent second security layer.

The problem is therefore not a shortage of tools. It is the absence of a
portable contract that says which question each tool answers, which tool is
authoritative for overlapping questions, what was actually scanned, and how
absence or failure differs from clean.

## Proposed paths

Proposed paths:
- `templates/modules/team-gated/portable-security-sweeps.md` -- adopter doctrine for the optional cross-language security layer.
- `templates/modules/team-gated/run_portable_security_sweeps.py` -- standard-library orchestrator source shipped by the module.
- `templates/modules/team-gated/portable_security_policy.json` -- lockfile-covered adapter enablement and suppression policy with no free-form commands.
- `dev/modules/portable-security-sweeps.md` -- adopter-tree destination for the module doctrine.
- `scripts/run_portable_security_sweeps.py` -- adopter-tree destination for the orchestrator.
- `scripts/portable_security_policy.json` -- adopter-tree destination for the reviewed policy.
- `bootstrap/tests/test_portable_security_sweeps.py` -- public-path subprocess, policy, and aggregate-exit tests.

## Proposal

Add a team-gated module named `portable-security-sweeps`. It installs a
standard-library orchestrator and a reviewed JSON policy, but installs no
third-party scanner. External tools remain explicit development/CI
dependencies chosen by the adopter.

The module is **not default-on in v1**. Select it when a project has accepted
and pinned at least one supported external scanner, or when a non-Python or
polyglot project needs a recorded security-sweep contract. Whether it later
belongs in a preset is a separate default-posture Decision informed by real
adopter noise and installation cost.

### 1. One portable authority per question; overlap is disclosed

The initial adapter registry is fixed in the orchestrator:

* **Dependency advisories:** OSV-Scanner over every supported ecosystem it
  discovers. Python-only projects may instead select only `python-security` and
  use pip-audit. When both modules are independently invoked in a polyglot
  project, their Python advisory coverage can overlap; both reports label that
  overlap, and the documentation says explicitly that duplicate findings are
  not independent evidence.
* **Secrets:** Gitleaks over both the current tree and Git history, with secret
  values redacted from stdout and machine reports.
* **GitHub Actions:** zizmor, activated only when workflows or composite actions
  are present and invoked offline.
* **Container/IaC misconfiguration:** Trivy with only the misconfiguration
  scanner enabled. Its vulnerability and secret scanners stay disabled here to
  avoid duplicating OSV-Scanner and Gitleaks.

Semgrep is documented as a high-risk extension point, not an initial adapter.
Its value comes from curated sources, sinks, sanitizers, and project rules; an
ambient remote ruleset would make the gate's meaning mutable. Adding it requires
a follow-up proposal that defines rule provenance, include behavior, resource
limits, and whether rule changes are reviewed as code. CodeQL and language-native
tools such as govulncheck, cargo-audit, and npm audit remain documented choices,
not v1 adapters.

### 2. Fixed adapters, not arbitrary commands

`portable_security_policy.json` selects known adapter IDs and records narrow
adapter options and reviewed suppressions. It cannot supply executable paths,
argument strings, shell fragments, environment variables, or new adapter names.
The script owns every executable name and argument vector.

The JSON schema is strict and versioned inside the file. Unknown keys, duplicate
adapter IDs, wrong types, unknown suppressions, control characters, and an
unsupported schema refuse before any subprocess. The module's complete mapping
group includes doctrine, runner, and policy so an upgrade cannot install or
advance only part of the apparatus.

### 3. Trusted-host executable boundary

This remains a **self-audit of a trusted checkout**, matching
`python-security`; it is not an untrusted-PR containment mechanism.

For each enabled adapter, the runner:

1. resolves the executable from the trusted host environment once;
2. rejects a lexical or resolved path inside the repository;
3. requires a regular executable and records lexical path, resolved path, and
   reported version;
4. invokes the absolute path with `shell=False`, a fixed argv, a bounded output
   size, and a timeout;
5. passes an explicit minimal environment and explicit policy/config path so a
   repository-local ambient config cannot silently suppress findings; and
6. records whether the tool used network access, cached advisory data, or only
   local rules.

Package-manager symlinks outside the repository are allowed after resolution
and both paths are reported. This validates shape and containment, not binary
provenance: the host-installed scanner is a declared executable trust root. The
module documentation must say so plainly. Projects needing stronger assurance
pin scanner artifacts in their environment/bootstrap system and verify vendor
checksums or provenance before Cairn invokes them.

### 4. Network and candidate configuration

Network egress is off by default. An adapter requiring fresh remote advisory
data reports incomplete unless the operator explicitly passes
`--allow-network`; the report names the data sent (normally package coordinates
and versions) and the service contacted. Secret, workflow, and misconfiguration
adapters remain offline.

Every adapter receives an explicit module policy path. A tool-specific ambient
configuration discovered in the target repository is either disabled by argv
or causes a refusal if the tool offers no reliable disable switch. Reviewed
project exceptions live in the lockfile-covered module policy, never in an
unattested side file that can make the sweep clean.

### 5. Shared aggregate exit contract

The orchestrator uses the existing `python-security` aggregate space so
automation and humans learn one interpretation:

* **0 -- CLEAN:** every enabled and applicable adapter ran successfully and
  reported no findings.
* **5 -- INCOMPLETE:** no findings, but an enabled/applicable tool, current
  advisory database, or accepted coverage input was unavailable.
* **10 -- FINDINGS:** at least one adapter reported a security finding.
* **20 -- DEGRADED / TAMPER:** policy/integrity validation failed, executable
  resolution was unsafe, output was malformed, a timeout occurred, or a tool
  failed outside its documented finding exit.

Precedence is 20 > 10 > 5 > 0. A missing executable is never clean. A repository
with no files applicable to a conditional adapter reports that adapter as NOT
APPLICABLE, not incomplete. The report prints each adapter's applicability
reason, tool/version, inputs discovered, coverage count, result, and network
disposition before the aggregate.

### 6. Relationship to `python-security`

Do not broaden or rename `python-security`. Its single-package Bandit contract
and pip-audit behavior are already reviewed and useful. The two modules remain
independently invokable rather than one claiming a leg ran merely because the
other module is installed:

* Python source SAST -> Bandit via `python-security`;
* Python dependency advisories -> pip-audit via `python-security`, and OSV when
  the portable runner is also selected;
* cross-language dependencies, secrets, CI, and IaC -> portable adapters.

The portable report detects when Python manifests and `python-security` are
both present and marks the advisory leg `OVERLAPPING`, including normalized
advisory IDs where the two report formats expose them. It does not suppress a
finding or pretend the other runner executed. A future top-level orchestration
proposal may deduplicate presentation once it can bind both executions; v1
prefers duplicate visible evidence over a silent delegated gap.

### Documentation / doctrine surface

* The new module doctrine owns selection, threat model, adapter matrix, exits,
  trust roots, egress, suppressions, and the statement that a sweep is a
  tripwire rather than proof.
* `bootstrap/DEPENDENCY_BUDGET.md` gains an explicit external-tool adapter
  category: Cairn's shipped runtime stays standard-library-only; optional tools
  are adopter-selected dev/CI dependencies and are never installed by scaffold.
* `bootstrap/SAFETY.md` records the new subprocess and external-executable trust
  boundary, including candidate-controlled config and mutable advisory data.
* Adopter tool-use documentation gives exact commands for installation checks,
  the runner, offline/default behavior, and interpreting 0/5/10/20.
* The install and gate manifests account for all three module files, and the
  changelog names the new opt-in capability without implying that scanners are
  bundled.

This changes shipped module doctrine and the install contract, but does not
change Cairn's cross-project governing doctrine. The doctrine-evolution
rate-limit is nevertheless cleared by the Maintainer-classified security
surface: the proposal introduces executable and suppression trust boundaries,
which are the high-risk limb of `doctrine/rationale.md`.

## Rationale

The user workflow is simple: a Python adopter keeps the focused gate already
shipped; a non-Python or polyglot adopter selects one module and gets a common
report over tools appropriate to its repository. They do not have to infer that
three vulnerability scanners overlap, mistake Ruff's Bandit-derived rules for
independent evidence, or interpret "tool missing" as "secure."

The stable boundary is question-oriented rather than product-oriented. Tools
can be replaced inside an adapter in a reviewed future change without changing
the meaning of dependency, secret, CI, or IaC coverage. The fixed registry and
strict policy preserve Cairn's standard-library runtime and prevent the module
from becoming a generic command execution framework.

This is timely because `default-security-stance` is deciding which security
apparatus fresh adopters receive. That proposal should not solve Python reach
while silently defining non-Python security as out of scope. This proposal does
not need to block it: it supplies a separately reviewable portable layer and
keeps the existing Python decision narrow.

## Alternatives considered

**Add more Python packages to `python-security`.** Rejected as the portable
answer. detect-secrets and Semgrep can add value, but installing them there
would deepen a Python-only module and still leave non-Python adopters without a
contract. Ruff's `S` family mostly duplicates Bandit-derived checks.

**Use Trivy for everything.** Attractive for a solo maintainer because it is
one binary. Rejected as the normative contract: its filesystem scanner spans
dependencies, secrets, misconfiguration, and licenses, making suppressions and
failure semantics harder to attribute. It remains the focused IaC adapter and a
documented one-binary alternative for projects that consciously prefer breadth.

**Run every available scanner and union the findings.** Rejected. Duplicate
advisory databases produce noise, conflicting severity, and unclear coverage;
more output is not more independent evidence when tools answer the same
question from similar feeds.

**Make Semgrep the universal source scanner.** Deferred. It is the strongest
candidate for broader source analysis, but a useful gate requires a pinned rule
authority and project-specific taint modeling. A remote registry preset is too
mutable to become Cairn's security meaning by accident.

**Documentation only.** Cheaper, but it leaves exit aggregation, missing-tool
semantics, executable containment, ambient configuration, and coverage
reporting to every adopter. Those are the security-sensitive parts worth
single-sourcing.

**Do nothing.** Leaves `python-security` coherent but language-bounded and
forces every non-Python adopter to rediscover the same composition and trust
questions.

## Evidence / verification plan

### Author-accounting -- invariants, failure modes, edge cases

**Invariants.**

* No adapter executes through a shell or accepts command text from policy.
  Enforced by a closed adapter registry, schema validation, and argv-capture
  tests through the public runner.
* Candidate-tree content cannot choose the executable or silently supply a
  suppression config. Enforced by repository containment checks and explicit
  lockfile-covered policy paths.
* Missing, stale, malformed, timed-out, or unsafe tooling never maps to clean.
  Enforced by the aggregate precedence table and one public-path test per
  failure class.
* One adapter inside the portable runner answers each security question;
  overlap with an independently-run Python gate is labeled, never presented as
  independent corroboration. Enforced by composition fixtures containing both
  module records and Python lockfiles.
* The orchestrator and policy are integrity-checked before any adapter runs.
  Enforced by lockfile-preflight tests using real installed module records.
* No default invocation uses network egress. Enforced by argv/environment
  capture and a socket-denial test harness; explicit `--allow-network` is the
  only egress transition.

**Failure modes.**

* Tool absent or advisory data unavailable -> exit 5, loud incomplete.
* Findings -> exit 10 even when another leg is incomplete.
* Unsafe executable, policy drift, unknown schema/key, malformed output,
  timeout, signal death, or undocumented tool exit -> exit 20.
* Candidate ambient config cannot be disabled -> exit 20 rather than run with
  unknown suppression policy.
* No applicable files for a conditional adapter -> NOT APPLICABLE, with the
  discovery inputs printed; it does not weaken another adapter.

**Edge cases.** Empty repositories, shallow clones without full history,
non-Git source exports, monorepos with several ecosystems, lockfiles with no
resolved versions, symlinked package-manager launchers outside the repository,
repository-local executables earlier on `PATH`, huge output, invalid UTF-8,
timeouts, stale caches, detached HEAD, and intentionally committed test secrets
all receive explicit fixtures or are named as residuals. In particular, a
shallow clone cannot claim full-history secret coverage; it reports the history
boundary and incomplete coverage.

**Public-path -> test mapping.** The proposed installed runner is exercised
through subprocess in the proposed portable-security test module, using
temporary fake executables that emit each documented exit/output shape.
Scaffold install, manifest, lockfile integrity, and module upgrade/adoption are
exercised through their existing public CLIs with the complete three-file
mapping.

**Known omissions.** v1 does not authenticate host binaries, contain malicious
scanner processes, prove advisory-database correctness, provide Semgrep rules,
or review code reachability. It assumes a trusted host/tool installation and a
trusted checkout, records that assumption, and refuses to market a clean result
as proof.

### Tests required

* Strict policy-schema tests: valid minimal/all-adapter policies plus every
  unknown-key, duplicate, type, control-character, and free-form-command case.
* Executable-boundary tests: absent, repo-local, resolved-into-repo, regular
  trusted-host fake, package-manager-style symlink outside repo, non-executable,
  timeout, signal death, oversized output, and malformed JSON/SARIF.
* Aggregate table tests covering every pairwise precedence combination and NOT
  APPLICABLE versus INCOMPLETE.
* Adapter argv tests proving Gitleaks redaction, zizmor offline mode, Trivy's
  misconfiguration-only scope, OSV network opt-in, and explicit policy paths.
* Ambient-config red-team fixtures for every initial adapter.
* Full-history/shallow/non-Git secret-coverage tests.
* Install-manifest, lockfile, complete-group, collision, adopt-module, upgrade,
  SPDX/license, generated-output, Python-floor, and Bandit-over-shipped-code
  coverage for the new module files.
* `python-security` composition tests proving the portable runner never claims
  the Python runner executed, labels overlapping Python advisory coverage, and
  leaves source SAST explicitly outside the portable result.

### Examples / smoke checks

* Scaffold a non-Python fixture with the module, provide trusted fake binaries,
  and execute the installed public runner end to end with network denied.
* Run the same fixture with every binary absent and require aggregate 5, not 0.
* Plant one dependency advisory, one historical secret, one workflow hazard,
  and one IaC misconfiguration in isolated fixtures and require the responsible
  adapter alone to report it.
* Run `python bootstrap/scaffold.py --manifest` and verify the module's three
  destinations appear exactly once.
* Run the canonical-interpreter suite, `bootstrap/security_check.py`,
  `scripts/check_cairn.py`, claim check over changed prose, generated-output
  scanning, neutrality, and license/SPDX gates.

## Signals the change is wrong

* Fresh clean fixtures produce enough false positives that reviewed
  suppressions become the normal first action. Recovery: keep the module
  documented but do not ship the orchestrator until adapter defaults are tuned.
* An initial adapter cannot disable candidate-controlled ambient configuration.
  Recovery: remove that adapter rather than pretending its result is trusted.
* Supporting external CLI version drift requires a generic command/config
  language. Recovery: keep explicit adapters and split version support; do not
  turn a security module into a shell runner.
* A real adopter cannot distinguish duplicated dependency findings or determine
  which lockfiles were scanned. Recovery: narrow to one dependency authority and
  make the coverage manifest blocking.
* Host binary provenance becomes necessary under the accepted threat model.
  Recovery: split a binary-binding design into its own Security Review rather
  than quietly adding another local executable trust root here.
* The implementation requires a runtime Python package. Recovery: reject the
  design; the orchestrator must remain standard-library-only even though the
  optional scanners are external dev/CI tools.

## External Security Review -- Claude -- 2026-08-03

**Model**: Claude Opus 5
**Tier**: External (different agent type -- the proposal is Codex-authored), security lens
**Reviewed**: the proposal text at `1af0441`, against `templates/modules/team-gated/run_security_audit.py`,
`bootstrap/DEPENDENCY_BUDGET.md`, and the installed module layout.

**Disposition: REVISE.** The contract is sound and the design resists the
failure I most expected -- it does not become a generic command runner. Two
findings are blocking, and I recommend a narrower v1 than proposed.

**What I checked rather than accepted.** The aggregate exit space is real:
`_AGG_INCOMPLETE = 5`, `_AGG_FINDINGS = 10`, `_AGG_DEGRADED = 20`
(`run_security_audit.py:76-78`), so reusing it is accurate. `templates/modules/team-gated/`
is the right home. The claim that Bandit-derived Ruff `S` rules are not an
independent second layer is correct.

**Credit where due**, since a review that only lists faults misrepresents the
artifact: the question-oriented adapter boundary is the right abstraction; the
closed registry with no executable paths, argv, or shell fragments in policy is
the control that keeps this from becoming a shell runner; `20 > 10 > 5 > 0` with
"a missing executable is never clean" is fail-closed in the right direction;
deferring Semgrep because a remote registry would make the gate's meaning
mutable is the correct call and correctly reasoned.

### [PS1] HIGH / BLOCKING -- the executable trust model is a new class, not a match for `python-security`

§3 opens "This remains a **self-audit of a trusted checkout, matching
`python-security`**". That understates a real delta, and a reviewer skimming §3
would take the wrong picture.

The existing module **never executes a host binary.** `_run_tool`'s contract is
explicit: "``argv`` MUST begin ``[sys.executable, "-I", "-m", ...]``"
(`run_security_audit.py:271`). Tools run as Python modules under the *pinned
canonical interpreter in isolated mode*, and `shutil.which("bandit")` /
`shutil.which("pip-audit")` appear only as **presence detection**
(`:333`, `:407`), never as execution authority.

This proposal executes four arbitrary host binaries resolved from `PATH`. That
is unavoidable -- there is no `python -m gitleaks` -- but it is the first time
`PATH` resolution becomes executable authority in this module family, and it
adds four executable trust roots where there were zero.

The proposal does say "the host-installed scanner is a declared executable trust
root", which is honest. The framing around it is not. **Satisfier:** state the
delta explicitly in §3, and enumerate the four binaries in the module's residual
trust set the way `bootstrap/REANCHOR_RUNBOOK.md` now enumerates
`/usr/bin/ssh-keygen` -- a named list a reader can audit, not a general
assurance.

### [PS2] HIGH / BLOCKING -- the ambient-config boundary is asserted per tool and established for none

§4: "A tool-specific ambient configuration discovered in the target repository is
either disabled by argv or causes a refusal if the tool offers no reliable
disable switch."

The whole candidate-configuration boundary rests on a per-tool fact the proposal
never establishes. Does Gitleaks have a flag that ignores an in-repo
`.gitleaks.toml`? Does Trivy ignore an in-repo `trivy.yaml` **and** avoid
fetching its policy bundle? Does zizmor ignore repository config? Each is
plausible and none is demonstrated.

This repository has just spent six review rounds discovering that per-tool and
per-shell facts do not match their documentation -- `/bin/zsh` sources
`$HOME/.zshenv` under `env -i` with a recorded `HOME`, which no amount of
reading "non-interactive shells skip startup files" would have surfaced. An
unestablished per-tool claim at a trust boundary is precisely that shape.

**Satisfier:** before Decision, execute each candidate adapter against a fixture
carrying a hostile ambient config, and record the observed behaviour and the
exact flag that suppressed it. Where no reliable switch exists, drop that
adapter -- which is already the proposal's own recovery under *Signals the change
is wrong*, so this asks it to apply its own rule before shipping rather than
after.

### [PS3] MEDIUM -- adapter output is candidate-controlled and rendered unsanitized

`_run_tool` prints `proc.stdout` and `proc.stderr` straight through
(`run_security_audit.py:283-286`). Scanner output embeds repository-controlled
content: matched filenames, matched lines, workflow fragments. A filename
carrying ANSI escapes, or a newline followed by forged status text, can forge
report lines in the operator's terminal -- and this report is the operator's
evidence for a security decision.

The proposal validates control characters in **policy** (§2) and says nothing
about **output**. Cairn already ships injection apparatus (`content_scan.py`)
whose entire premise is that displayed content can carry instructions; the same
premise applies to a security report assembled from candidate-controlled strings.

**Satisfier:** render only parsed structured fields with control characters
stripped, or escape adapter output before display; add a fixture with a
hostile filename and assert the report cannot be forged. Note this is a latent
defect in the **existing** module too, not only the proposed one.

### [PS4] MEDIUM -- INCOMPLETE becomes the default steady state, and the proposal should own that

`run_pip_audit_pass` returns `_AGG_INCOMPLETE` whenever egress is off
(`:397-406`), and egress is off by default. So an unconfigured `python-security`
run **already can never be CLEAN**. That is defensible for one pass.

The portable module inherits the property and multiplies it: OSV-Scanner needs
advisory data, and Trivy's misconfiguration scanner fetches policy bundles. With
four adapters, aggregate `5` becomes the normal outcome for a correctly
configured repository. A gate whose usual result is INCOMPLETE trains its
operator to stop distinguishing `5` from `0` -- which is the exact signal the
exit contract exists to carry.

**Satisfier:** decide it explicitly rather than inheriting it. Either support
local advisory/policy data so `0` is reachable offline, or state plainly in the
adopter documentation that `5` is the expected default and `0` requires
`--allow-network`. Do not leave the operator to infer which of the two Cairn
means.

### [PS5] MEDIUM -- scope, measured against the standing direction

The proposal flags Cairn's standing "fix defects, build nothing new" direction
and proceeds anyway. That is the right disclosure and I do not think the
proposal is wrong to exist -- but the size deserves a Decision, not an
assumption.

As written, v1 is three shipped files, a versioned policy schema, four
executable trust roots, and roughly forty enumerated required tests, opened
alongside ~10 other in-flight proposals. The security-review cost is not one
review: each adapter carries its own ambient-config surface (PS2), output-parsing
surface (PS3), and version-drift surface that the proposal names under *Signals*.

**Recommendation -- accept the contract, ship one adapter.** Take the
question-oriented boundary, the aggregate semantics, and the strict policy schema
as the reviewed contract, and implement **Gitleaks alone** in v1. It is the
strongest first adapter on this specific evidence: secrets are the
highest-consequence finding class, and it needs no advisory database, so `0`
is reachable offline and PS4 does not bite. Each further adapter then arrives as
its own reviewed increment with its PS2 evidence attached.

### [PS6] LOW -- a note on the quoted authorization, not a challenge to it

The proposal's Context quotes the Maintainer asking a two-part question. The
first part matches what I received in my own channel verbatim; the second ("How
about command line tools for those without python?") I have no way to verify
from here, and it may well have been asked in the Codex channel.

Raising it only because this repository's own scribing rule requires authorizing
quotes to be verbatim and visually isolated *precisely so drift is visible*, and
this quote is doing authorizing work -- it is the proposal's stated go-ahead.
Worth a Maintainer confirmation before it hardens into the record. No suggestion
that it is inaccurate.

### [PS7] Defect surfaced in passing -- the existing runner has no timeout

`_run_tool` calls `subprocess.run(argv, cwd=neutral, shell=False, env=env,
capture_output=True, text=True)` with **no `timeout=`** (`:275-278`). A hung
Bandit or pip-audit blocks the audit indefinitely, and a hang is
indistinguishable from a slow scan.

The proposal correctly requires a timeout for its own adapters (§3.4). That
standard should be back-ported to `python-security`, and doing so is a **defect
fix** that sits comfortably inside the standing direction -- unlike the new
module, it needs no new trust roots. Worth splitting out as its own small
proposal rather than riding this one.

### Scope of this review

I did not evaluate: the adapters' detection quality, OSV/Trivy/Gitleaks/zizmor
advisory-data correctness, the install-manifest and lockfile mechanics beyond
confirming the module layout, `default-security-stance` interaction, or the
proposal's test list for completeness. I verified the exit-code contract, the
`python-security` execution boundary, the output-rendering path, and the
default-egress disposition by reading the shipped runner.
