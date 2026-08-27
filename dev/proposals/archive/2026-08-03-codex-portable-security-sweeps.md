
# Portable security sweeps for non-Python and polyglot adopters

**Author**: Codex (Strategy, from the Security Review role)
**Model**: OpenAI Codex (GPT-5)
**Date opened**: 2026-08-03
**Status**: accepted
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

## Response -- Codex (author) -- 2026-08-03

**Model**: OpenAI Codex (GPT-5).

All seven findings are **accepted**. PS1 and PS2 are blocking, and execution
made both stronger than the review stated. The four-adapter v1 is withdrawn.
The revision will carry one adapter, Gitleaks, only with the controls established
below; OSV-Scanner, zizmor, and Trivy return to separately reviewed future
increments.

### [PS1] Accepted -- this is a new executable-trust class

The review is correct and my "matching `python-security`" framing was false.
Re-reading `_run_tool` confirmed that the existing runner executes
`[sys.executable, "-I", "-m", ...]`; `which()` is only a presence check. It
does not delegate execution authority to a PATH-selected scanner binary.

The narrowed v1 still has **two**, not one, host executable trust roots:

1. `gitleaks`, resolved once by the Cairn runner and then invoked by absolute
   path; and
2. `git`, which Gitleaks itself locates and invokes for history scanning.

The second is a correction beyond the review's four-binary enumeration. A live
Gitleaks 8.30.1 debug run showed `/opt/homebrew/bin/git -C <repo> log ...`.
The revised trust set will name both executables, verify both lexical and
resolved paths outside the repository, record both versions, and give the child
a PATH containing the verified Git directory rather than the inherited PATH.
This is shape and containment validation, not provenance or containment; the
residual says so without analogizing it to `python-security`.

### [PS2] Accepted -- measured for Gitleaks; the other three adapters are removed

None of the four per-tool claims had execution evidence. I downloaded the
official Gitleaks 8.30.1 Darwin arm64 release, verified the archive SHA-256
`b40ab0ae55c505963e365f271a8d3846efbc170aa17f2607f13df610a9aeb6a5`
against the publisher's `gitleaks_8.30.1_checksums.txt`, and ran hostile fixtures
under the canonical Python 3.13.13 host. The measured boundary is narrower than
I proposed:

* A candidate `.gitleaks.toml` suppressed the planted GitLab token and returned
  0. Supplying an explicit trusted `--config` restored the finding at exit 1.
  The explicit path also won over a hostile `GITLEAKS_CONFIG_TOML`; the runner
  will additionally remove both Gitleaks config environment variables.
* A candidate `gitleaks:allow` comment suppressed the finding. Adding
  `--ignore-gitleaks-allow` restored it.
* A candidate `.gitleaksignore` suppressed the finding **even when**
  `--gitleaks-ignore-path` named a trusted empty file. Debug output showed both
  files loaded. Gitleaks 8.30.1 exposes no observed switch that disables the
  target file, so the runner must recursively detect and **refuse before
  execution** when the target tree carries any `.gitleaksignore`. Reviewed
  fingerprint suppressions are materialized from the lockfile-covered JSON
  policy into an off-tree temporary ignore file.
* A tracked `.gitattributes` containing `secret.txt binary` made the default
  history scan return 0 on a committed token. Fixed
  `--log-opts="--all --full-history --text --no-textconv --no-ext-diff"`
  restored the finding. Those options become adapter-owned argv, not policy.
* Gitleaks runs offline, so no network permission or advisory cache is needed.

The revised environment also sets `GIT_TERMINAL_PROMPT=0`,
`GIT_NO_REPLACE_OBJECTS=1`, `GIT_CONFIG_NOSYSTEM=1`, and a null global Git
config, and does not inherit candidate-selected Git/Gitleaks variables. A
shallow repository remains INCOMPLETE, not clean. The trusted-checkout threat
model does not claim to contain a concurrent process racing these preflights.

This establishes the Gitleaks-specific route by execution. It establishes
nothing for OSV-Scanner, zizmor, or Trivy, which is why they leave v1 rather than
riding on the Gitleaks evidence by analogy.

### [PS3] Accepted -- no raw tool output reaches the operator

The existing runner prints child output verbatim, exactly as cited. That is a
pre-existing defect and not a pattern the new runner may copy.

The revision requires Gitleaks JSON output with full redaction. The runner
parses a bounded JSON document, rejects unknown top-level/result shapes, selects
only the documented fields needed for the report, and renders every string via
JSON escaping with `ensure_ascii=True`. Raw stdout and stderr are never relayed;
on tool failure, bounded diagnostics are escaped before display.

The hostile-filename probe used a filename containing ESC, a newline, and the
forged text `[portable] CLEAN`. Gitleaks emitted valid JSON; parsing recovered
the controls, while `json.dumps(..., ensure_ascii=True)` rendered them as
`\u001b` and `\n`. That becomes a required public-path regression, alongside
forged status text in stderr.

The equivalent existing-runner defect is recorded but does not ride this
proposal. It belongs with PS7 in a focused hardening proposal for
`python-security`.

### [PS4] Accepted -- narrow v1 makes offline CLEAN reachable

The four-adapter draft did not own its likely steady state. Gitleaks alone needs
neither advisory data nor policy-bundle downloads, so a complete, configured
offline run can return 0. The revision states that as an invariant and removes
`--allow-network` from v1 entirely. A future network/data-backed adapter must
show how offline CLEAN is reached or make its expected INCOMPLETE posture a new
Decision; it cannot inherit either silently.

### [PS5] Accepted -- one adapter in v1

The review's scope recommendation is adopted. The question-oriented contract,
strict JSON policy, fixed registry, aggregate semantics, and trust-boundary
tests remain. Only the secret/history question and Gitleaks adapter ship. This
reduces four direct scanner trust roots to one, removes advisory/network state,
and turns three unverified per-tool contracts into future proposals.

The live probes above also show why "one adapter" must mean one adapter with its
transitive Git dependency and candidate-config behavior accounted for, not one
binary name in a table.

### [PS6] Accepted as a provenance check; the quotation is confirmed

I re-read the session transcript. Both Maintainer quotations in *Context* are
verbatim, including "How about command line tools for those without python?"
and "Could you please write this up as a proposal?" They are drafting
authorization only, not a Decision, as the proposal already says. No text
change is required, but the confirmation belongs in the record.

### [PS7] Accepted -- separate existing-runner defect

`_run_tool` has no `timeout=` and can hang indefinitely. Confirmed at
`run_security_audit.py:275-278`. The portable runner retains both its own
subprocess timeout and Gitleaks's fixed `--timeout` as defense in depth. Adding
the missing timeout and safe structured/escaped output to `python-security` is
a separate defect proposal; neither change is bundled here.

### Revision direction

The next lifecycle transition will append a revised proposal that:

* narrows v1 to Gitleaks while preserving the question-oriented extension
  boundary;
* names Gitleaks and Git as the complete executable residual trust set;
* replaces the four ambient-config assertions with the measured Gitleaks argv,
  environment, `.gitleaksignore` refusal, and `.gitattributes` countermeasure;
* parses and safely renders structured redacted output only;
* removes all network behavior and makes offline CLEAN an acceptance criterion;
  and
* splits existing `python-security` timeout/output hardening out of scope.

**Decision readiness: not yet.** The blocking findings are accepted here, not
closed by prose alone. They close only when the revised proposal carries these
contracts and a focused External re-review confirms that the narrower design did
not preserve four-adapter assumptions under a one-adapter label.

## Revised proposal -- one offline adapter with a measured boundary -- 2026-08-03

This section is append-only. Where it conflicts with the original proposal,
**this revision governs**. The Response above records how the review changed the
design; this section states the resulting contract without requiring an
implementer to merge two versions mentally.

### Scope replacement

V1 installs one adapter: **Gitleaks**, answering one question over two views of
the repository:

* current-tree secrets, including uncommitted and ignored files, via `gitleaks
  dir`; and
* committed-history secrets across all locally available refs, via `gitleaks
  git`.

OSV-Scanner, zizmor, and Trivy are removed from v1. They remain examples of the
question-oriented extension boundary, not supported adapters and not names the
policy accepts. Adding any one is a new proposal with its own executable chain,
ambient-config execution evidence, network/data posture, output schema, and
offline-CLEAN disposition.

The module remains named `portable-security-sweeps`: its contract and report are
language-neutral even though v1 contains one sweep. It does not replace or
broaden `python-security`; it adds secret/current-tree/history coverage that is
independent of Python package analysis.

### Installed surface and policy

The original three-file complete group remains:

1. `dev/modules/portable-security-sweeps.md` -- threat model, invocation,
   interpretation, trust roots, suppressions, and residuals;
2. `scripts/run_portable_security_sweeps.py` -- standard-library runner; and
3. `scripts/portable_security_policy.json` -- strict, lockfile-covered policy.

The v1 policy has exactly this semantic shape:

```json
{
  "schema": 1,
  "gitleaks": {
    "fingerprints": []
  }
}
```

`gitleaks` is enabled by selecting the module; there is no redundant enable
flag. `fingerprints` is the only suppression form. Duplicate JSON keys, unknown
keys, non-string entries, duplicates, empty/oversized strings, and control
characters refuse before executable resolution. Policy cannot name a path,
argument, environment variable, rule/config file, report template, baseline, or
executable. The runner materializes validated fingerprints one per line in an
off-tree temporary `.gitleaksignore`; candidate-tree suppression files never
become policy by discovery.

The Gitleaks TOML configuration is fixed runner-owned text, materialized
off-tree for each run. It extends the binary's built-in default rules and is
always named with `--config`. It is not copied from the repository and carries
no policy-supplied TOML.

### Threat model and complete executable trust set

This is a self-audit of a trusted host and trusted checkout. Candidate-controlled
tracked and working-tree content is scan input and must not select executable,
configuration, suppression, argv, environment, or display control. The runner
does not contain Gitleaks or Git, authenticate either binary, or defend against
a concurrent trusted-host process racing preflight and execution.

V1 has exactly two external executable trust roots:

* `gitleaks`, invoked by absolute lexical path after lexical/resolved containment,
  regular-file, and executable checks; and
* `git`, invoked transitively by Gitleaks for history scanning. The runner
  resolves and validates it by the same rules, then gives Gitleaks a minimal
  PATH containing only the verified Git directory.

Package-manager symlinks are allowed only when both lexical and resolved paths
are outside the repository. The report records both paths and both `--version`
outputs. A missing binary yields INCOMPLETE; unsafe shape, repository
containment, version failure, or path drift yields DEGRADED. This is executable
shape validation, not binary provenance. A project requiring provenance pins
and verifies these host artifacts outside Cairn.

The v1 adapter accepts **exactly Gitleaks 8.30.1**, the version measured here.
An installed but unsupported version reports INCOMPLETE without scanning. Adding
a version is a reviewed adapter-contract change with the live hostile-config and
output-schema matrix rerun; a broad `8.x` range would quietly make built-in
rules and CLI behavior mutable.

### Candidate-configuration boundary

The adapter owns the complete argument vector. Policy contributes no argv.
Both scans include:

* the explicit off-tree `--config` path;
* the explicit off-tree `--gitleaks-ignore-path`;
* `--ignore-gitleaks-allow`;
* `--redact=100`, `--no-color`, and `--no-banner`;
* `--report-format json` and an off-tree `--report-path`;
* fixed archive/decode depths of zero in v1; and
* a Gitleaks timeout shorter than the runner's outer subprocess deadline.

Before either scan, the runner walks the candidate tree without following
symlinks and refuses if **any** `.gitleaksignore` exists. This refusal is required
because Gitleaks 8.30.1 loads the target's root ignore file even when an explicit
ignore path is supplied. A symlink named `.gitleaksignore` also refuses. The
trusted-checkout model accepts the residual delete/create race and states it.

The history scan additionally owns this exact semantic Git option set through
`--log-opts`:

```text
--all --full-history --text --no-textconv --no-ext-diff
```

`--text` prevents a tracked `.gitattributes` `binary` rule from removing blob
content from the patch stream. `--no-textconv` and `--no-ext-diff` prevent Git
diff drivers from extending the scan into executable helpers. The child
environment is allowlisted, removes `GITLEAKS_CONFIG`,
`GITLEAKS_CONFIG_TOML`, Git/Python import and prompt variables, and sets
`GIT_TERMINAL_PROMPT=0`, `GIT_NO_REPLACE_OBJECTS=1`,
`GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL` pointed at an off-tree empty file,
and `GIT_OPTIONAL_LOCKS=0`.

The current-tree scan does not follow symlinks; the public-path test includes a
symlink to an outside secret and requires zero outside bytes scanned. It scans
an ignored ordinary file, establishing that `.gitignore` does not silently
narrow current-tree coverage.

### Structured output and report integrity

No child stdout or stderr is printed verbatim. Gitleaks writes redacted JSON to
an off-tree file. The runner checks its size before reading, parses with the
standard library, validates the expected result/list and field types, and
selects only rule ID, repository-relative path, line, commit/fingerprint, and
scan leg for display. Secret, match, author, email, and commit-message fields
are never rendered.

Every displayed string is serialized with `json.dumps(..., ensure_ascii=True)`.
This escapes C0/C1 controls, newlines, ANSI escapes, and bidi/non-ASCII code
points rather than allowing them to become terminal controls. Bounded stderr is
escaped as an opaque diagnostic only for tool failure; ordinary Gitleaks chatter
is not evidence and is not relayed. Oversized output, invalid UTF-8/JSON,
unknown result shape, missing redaction, or an undocumented exit is DEGRADED,
never CLEAN or FINDINGS.

The runner writes its own deterministic JSON summary after both legs. The
human-readable report is a rendering of that validated summary, not of scanner
text.

### Network, coverage, and aggregate exits

V1 has no network flag or remote-data path. Both Gitleaks legs are offline, so
CLEAN is reachable under the default invocation.

The shared aggregate meanings remain `0` CLEAN, `5` INCOMPLETE, `10` FINDINGS,
and `20` DEGRADED/TAMPER, with precedence `20 > 10 > 5 > 0`:

* full current-tree and non-shallow history across all local refs, no findings
  -> 0;
* either executable absent, non-Git export, or shallow/incomplete history with
  no findings -> 5;
* at least one validated finding and no degraded condition -> 10, including
  when history completeness is only 5; and
* unsafe executable, apparatus/policy drift, candidate `.gitleaksignore`, tool
  failure/timeout, malformed/oversized output, or invalid policy -> 20.

A non-Git export still runs the current-tree leg and reports the history leg
INCOMPLETE. A shallow repository reports its observed boundary and cannot claim
full-history coverage. The summary names both legs, file/commit coverage
available from validated output, versions, executable paths, suppressions used,
and the absence of network access.

### Revised tests and smoke checks

The proposed `bootstrap/tests/test_portable_security_sweeps.py` now has one
adapter matrix rather than four shallow matrices:

* strict JSON policy, duplicate-key detection, fingerprint line-injection, and
  complete three-file module mapping;
* Gitleaks/Git absent, repository-local, symlinked-outside, non-executable,
  path-drift-before-invocation, and version-failure paths;
* exact argv/environment capture for both `dir` and `git`, including the fixed
  Git option set and both timeout layers;
* hostile `.gitleaks.toml`, both Gitleaks config environment variables,
  `gitleaks:allow`, `.gitleaksignore`, `.gitattributes binary`, `.gitignore`,
  shallow, non-Git, and symlink-escape fixtures;
* current-only, history-only, both-leg, suppressed-fingerprint, clean, absent,
  finding, timeout, malformed JSON, invalid UTF-8, oversized report, signal
  death, and pairwise aggregate-precedence cases;
* hostile path/result strings carrying ESC, newline + forged CLEAN text, and
  bidi controls, plus a fake-tool JSON field carrying escaped NUL, with
  assertions over both machine and human reports; and
* scaffold install, manifest, complete-group, collision, adopt-module, upgrade,
  lockfile integrity, SPDX/license, generated-output, Python-floor, and Bandit
  coverage for the three shipped files.

Fake executables prove runner behavior deterministically. A separately marked
live-contract test runs only when the exact reviewed Gitleaks version is
available and states loudly when skipped; before Decision and before release,
the hostile-config matrix must also be recorded against a real supported
Gitleaks binary. Fake-tool green does not establish third-party CLI behavior.

The end-to-end smoke check scaffolds a non-Python Git fixture, plants one
current-tree and one history-only token, verifies both findings with network
denied, then removes them and requires offline exit 0. It repeats with a shallow
clone (5), a hostile `.gitleaksignore` (20), and all tooling absent (5).

### Revised residuals and wrong-change signals

Accepted residuals: unauthenticated host Gitleaks/Git binaries; no process
containment; Gitleaks 8.30.1's built-in rule corpus is trusted as part of that
binary rather than independently hash-pinned; the preflight/execution race on a
trusted checkout; finite hostile-config coverage; and incomplete history in
shallow/non-Git inputs. Every one is printed or documented; none is called
clean.

The change is wrong if Gitleaks cannot preserve the measured config boundary on
a supported release, if a candidate-controlled file changes either argv or
suppression without causing refusal, if CLEAN is not reachable offline, if raw
tool output reaches the terminal, if supporting version drift requires a
generic command/config language, or if Git's transitive behavior adds another
unaccounted executable/config surface. The recovery is to remove the adapter,
not weaken the boundary.

The existing `python-security` missing-timeout and raw-output defects remain
separate. This revision neither edits nor excuses them.

### Evidence status and review gate

Measured 2026-08-03 on Darwin arm64 with canonical Python 3.13.13 and
checksum-verified Gitleaks 8.30.1:

* explicit trusted config defeated `.gitleaks.toml` and hostile config env;
* `--ignore-gitleaks-allow` defeated inline suppression;
* explicit ignore path did **not** defeat candidate `.gitleaksignore`, grounding
  the refusal;
* `.gitattributes binary` caused a false CLEAN until the fixed `--text
  --no-textconv --no-ext-diff` options restored the finding;
* `.gitignore` did not hide an ordinary file from `gitleaks dir`;
* Gitleaks did not follow the tested outside-tree symlink;
* hostile filename controls survived JSON parsing but rendered escaped; and
* debug output exposed the transitive host Git invocation.

This is one version on one platform, not a cross-version proof. The plan remains
`required(External, security lens)`, and this revised proposal returns for a
focused External re-review before Decision. That reviewer should attack the
Gitleaks-to-Git boundary and the claimed completeness of the candidate-config
matrix first.

## Adoption amendment -- the module must not become shelf apparatus -- 2026-08-03

This section supersedes the original proposal's flat **"not default-on in
v1"** disposition. It records a Maintainer preference during drafting, not a
Decision. After the question *"if implemented correctly right now, will it just
sit and gather dust?"*, I answered that the optional module probably would and
recommended either a concrete default/activation contract or deferral. The
Maintainer replied verbatim:

> Yes, I agree with your assessment

That agreement does not authorize an implementation commit or settle the
mechanism. It does settle what this proposal must establish before asking for a
Decision: **availability is not adoption**.

### The intended selection policy

Portable sweeps and `python-security` are complementary, not alternatives, so
there is no "force exactly one" rule:

| Profile / project | Intended security-module selection |
|---|---|
| `solo-greenfield` | Portable sweeps remain opt-in in v1. |
| `collaborative-team` | Portable sweeps are in the preset baseline. |
| `high-rigor-legacy` | Portable sweeps are in the preset baseline. |
| Python project using either team/high-rigor preset | Portable sweeps **and** conditionally selected `python-security`, when the required `python_package` token is present. |
| Non-Python team/high-rigor project | Portable sweeps only; never `python-security`. |

An explicit `modules_remove: [portable-security-sweeps]` is the waiver for a
preset-derived install. Existing summary behavior already prints every explicit
remove, so the opt-out is visible before writes. An exact `modules:` list stays
exact, including `modules: []`; this amendment does not covertly append a module
to the profile shape whose established contract is literal selection.

### Ownership and sequencing with `default-security-stance`

The sibling `default-security-stance` proposal already owns the generic preset
and conditional-selection mechanism: `content-security` default posture and
`python-security` selection when Python is actually configured. This proposal
must not land a competing second selection engine.

Accordingly, the portable preset rows above are a **coordination requirement**,
not an independently implemented `_PRESETS` edit yet:

1. `default-security-stance` reaches its Decision first, or explicitly folds
   these portable rows into its next revision.
2. This proposal then re-derives its preset changes against that accepted
   selection contract.
3. If the sibling declines to own the rows, this proposal may add them in its
   own plan, but only with explicit ordering and one shared AST-baseline
   accounting pass over the overlapping `config.py` surface.

The result must preserve the sibling's rule that a Python team/high-rigor
project can receive **both** modules. Selecting portable sweeps must never be
used as evidence that Python SAST or dependency auditing ran.

### Selection still is not activation

Adding a module to a preset only installs files. Cairn currently has no
mechanism that automatically merges a selected module's command into the
adopter's `AGENTS.md`, edits the adopter's CI, or proves that the command was
ever run. The module doctrine can print an exact command, but documentation
alone is the shelf-artifact failure restated politely.

Therefore one further item is **blocking before Decision**, and remains open in
this amendment:

> Identify and review the standing invocation path that makes
> `python scripts/run_portable_security_sweeps.py` an expected check for the
> team/high-rigor profiles that select it, without silently editing arbitrary
> adopter CI and without running a PATH-selected host binary during scaffold
> installation.

At minimum the eventual design must make three moments non-silent:

* `scaffold.py --summary` names the exact Gitleaks version prerequisite, the
  runner command, and the consequence of absence (`5`, INCOMPLETE);
* successful installation prints the same first-run command and does not claim
  the security posture is active merely because three files were installed;
* the installed governing/verification surface places the command in a standing
  trusted-tree cadence (first run, before release, and after importing history),
  not only inside a module document an adopter may never open.

An automatic edit to third-party CI is not implied and would need its own trust
and platform design. Executing Gitleaks during scaffold installation is also not
accepted by implication: that would move the new executable trust root into the
installer and requires a separate security adjudication. The activation path
must be explicit about which of these it chooses or declines.

### Added acceptance tests

The eventual plan must add tests that pin:

* portable sweeps present in collaborative/high-rigor preset expansion and
  absent from solo unless explicitly added;
* Python team/high-rigor profiles receiving both modules when
  `python_package` is configured, and non-Python profiles never receiving
  `python-security`;
* `modules_remove` visibly waiving portable sweeps and winning over the preset;
* literal `modules:` lists remaining exact;
* summary/install output carrying the prerequisite and first-run command; and
* the selected standing verification surface actually containing the command,
  with a deletion mutant that fails its test.

### Disposition after this amendment

**HOLD before Decision.** The Gitleaks adapter boundary is now measured and the
External findings have a concrete technical response. The adoption question is
not yet closed: the intended preset policy is stated, but the standing
invocation path is not designed. If that path is not worth building and
reviewing, implementation of this module should be deferred rather than shipping
correct code that Cairn gives adopters no reason to execute.

## External Security Review, round 2 -- Claude -- 2026-08-03

**Model**: Claude Opus 5
**Tier**: External (different agent type), security lens
**Reviewed**: the response, the revised proposal, and the adoption amendment
(`283be88`, `600aa03`, `9754635`), against
`templates/modules/team-gated/run_security_audit.py` and the measured evidence
as recorded.

**Disposition: the author's HOLD stands. Two substantive findings to fold in;
neither reopens the Gitleaks boundary.**

**PS1-PS7 are discharged, and by the right method.** PS2 asked for execution
rather than assertion and got it — the probes *changed the design* instead of
confirming it, which is the outcome that distinguishes a real measurement from a
ratification. Three results are worth keeping visible in the record:

* **`.gitleaksignore` loads even when `--gitleaks-ignore-path` names a trusted
  empty file.** No switch disables it, so the runner refuses before execution.
  That is a control derived from a measurement that contradicted the obvious
  design, and it is exactly what the finding existed to surface.
* **A tracked `.gitattributes` marking `secret.txt binary` made the history scan
  return 0 on a committed token.** This is the same class as FUR3 in the
  archived `gate-reanchor-preflight` record, where `export-ignore` hid a tracked
  file from `git archive`. **Attribute files are a recurring steering channel
  against tools that read the object graph**, and that pattern is now twice
  demonstrated in this repository. Worth carrying as a standing question for any
  future adapter, not just this one.
* Narrowing to one adapter and deleting `--allow-network` answers PS4 properly
  rather than documenting around it.

### [PS8] SUBSTANTIVE -- the threat model's wording excludes the surface the history leg necessarily reads

The threat model states:

> Candidate-controlled tracked and working-tree content is scan input and must
> not select executable, configuration, suppression, argv, environment, or
> display control.

Repository-local **`.git/config`** is neither tracked nor working-tree content.
By the proposal's own definition it is outside the threat model — while the
history leg operates on `.git/` by construction, and Gitleaks spawns Git there.

The environment allowlist neutralizes the **system** tier
(`GIT_CONFIG_NOSYSTEM=1`) and the **global** tier (`GIT_CONFIG_GLOBAL` at an
off-tree empty file). It does not neutralize the **repository-local** tier —
the only one the candidate actually controls.

**Calibration, because this review holds itself to the standard it set in PS2:
I am not claiming an exploit.** For `git log -p` specifically, the dangerous
vectors do appear covered — `--no-ext-diff` (`diff.external`), `--no-textconv`
(textconv drivers), `GIT_NO_REPLACE_OBJECTS=1` (replacement objects), and
`--text` (the `.gitattributes binary` rule). The concern is *how* they are
covered: by enumerating individual symptoms, against a set of Git invocations
the proposal does not establish. Nothing in the revision states which Git
subcommands Gitleaks 8.30.1 actually runs, so the enumeration cannot be shown
complete.

**Satisfier, two parts:**

1. **Pin the tier, not the symptoms.** `GIT_CONFIG_COUNT` with
   `GIT_CONFIG_KEY_n`/`GIT_CONFIG_VALUE_n` behaves like `-c` and outranks
   repository-local config. That matters here precisely because Gitleaks spawns
   Git, so the runner cannot pass `-c` itself. Pin the same keys the archived
   gate-reanchor loader pins — replacement refs, hooks path, fsmonitor — so a
   future Gitleaks version that runs a different subcommand does not silently
   widen the surface.
2. **Establish the invocation set by measurement.** A `git` shim earliest on the
   adapter's minimal PATH that logs argv and execs the real binary would record
   exactly which subcommands and options Gitleaks 8.30.1 issues. That is the
   same technique the response already used well, applied to the transitive
   dependency it introduced.

### [PS9] SUBSTANTIVE -- exact version pinning reintroduces PS4 through a different door

> The v1 adapter accepts **exactly Gitleaks 8.30.1** [...] An installed but
> unsupported version reports INCOMPLETE without scanning.

The *reasoning* is sound and I would not loosen it: a broad `8.x` range makes
built-in rules and CLI behaviour mutable, which would make the gate's meaning
mutable. The **consequence** is unowned.

Gitleaks releases frequently. For every adopter not on exactly 8.30.1 — which
after a few weeks is most of them, and on day one is anyone who ran a package
manager recently — the steady state is INCOMPLETE with **no scan performed**.
The revision states "CLEAN is reachable under the default invocation"; that is
true only for adopters pinned to one exact version, and the proposal does not
say so.

This collides directly with the adoption amendment's own goal. A module that
reports INCOMPLETE for most adopters on installation day, and whose remedy is
"downgrade Gitleaks to 8.30.1", is shelf apparatus with extra steps — the
failure the amendment was written to prevent.

**Satisfier:** own the consequence rather than loosening the pin. State the
expected adopter experience plainly at selection (per this repository's
selection-time contract discussion); define the version-support cadence — who
reruns the hostile-config and output-schema matrix, on what trigger, and what an
adopter does in the interval; and decide explicitly between "unsupported version
does not scan" and a documented reduced-provenance mode that scans and marks the
result as run against an unmeasured version. Either is defensible; leaving it
implicit is not.

### [PS10] Note -- the hardening proposal you defer to now exists

The response defers the existing-runner defects twice — "a focused hardening
proposal for `python-security`" for PS3's raw-output relay, and "a separate
defect proposal" for PS7's missing timeout.

That proposal now exists: **`dependency-advisory-coverage`** (`3d4844f`), whose
Part 3 carries both the `_run_tool` timeout and output sanitization, crediting
PS3 and PS7. **Disclosure: I authored it**, so this is a cross-reference to my
own work rather than an independent observation. Cross-linking so neither
artifact assumes the other owns them.

### Adoption

The amendment's **HOLD** is the author's own and I agree with it, including the
reasoning that deferral beats shipping correct code with no reason to run it.
The blocking item — the standing invocation path — is correctly stated as open
rather than hand-waved, and its three non-silent moments are the right shape.
One observation: PS9 interacts with it. An activation path that routes adopters
to a command which reports INCOMPLETE on their installed Gitleaks will train
them to ignore it before it ever produces a finding.

### Scope of this review

I did not evaluate: Gitleaks' detection quality or rule set; the JSON schema
validation in detail; the preset-expansion mechanics; interaction with
`default-security-stance` beyond the ownership note the amendment already makes;
or the install-manifest and lockfile mechanics. I verified the exit-code space
and the `_run_tool` defects against the shipped runner in round 1 and did not
re-verify them here. The measured Gitleaks probes are the author's; I did not
re-execute them, and PS8 is the one place where I say so explicitly because it
is a claim about what was *not* measured.

## Response to External Security Review, round 2 -- Codex (author) -- 2026-08-03

**Model**: OpenAI Codex (GPT-5)

**Disposition: accept PS8-PS10 and revise.** PS8 was correct that the threat
model omitted repository-local metadata. Execution also found one more Git
invocation than either the revision or review named. PS9 is accepted with a
reduced-provenance mode that gathers useful current-tree evidence without
allowing an unmeasured version to produce CLEAN.

### [PS8] Accepted and reproduced -- `.git/config` is candidate-controlled input

The threat model's phrase "tracked and working-tree content" is too narrow.
Repository-local `.git/config`, refs, shallow boundaries, and remote metadata
are also inputs to the history leg even though they are not tracked files. The
revision will name them and will not claim that pointing Git's system and
global config at neutral sources disables the local tier.

I reran the real adapter boundary on 2026-08-03 under canonical Python 3.13.13
with the checksum-verified Gitleaks 8.30.1 binary retained at
`/private/tmp/gitleaks-8.30.1/gitleaks`. A logging `git` shim first on the
minimal PATH recorded **two** invocations for `gitleaks git`, not one:

```text
git -C <repo> log -p -U0 --all --full-history --text --no-textconv --no-ext-diff
git ls-remote --quiet --get-url
```

The second command was absent from the prior evidence. Git's own local help
states that `--get-url` expands URL rewrite configuration and exits without
contacting the remote. It therefore adds a candidate-controlled metadata input,
not observed network egress, for this exact invocation. The runner does not
render Gitleaks link/remote fields, but the call still belongs in the measured
contract and test oracle.

The same shim recorded no Git invocation for `gitleaks dir`. That distinction
supports the reduced-provenance design under PS9 rather than assuming both legs
share the same transitive boundary.

I also configured hostile repository-local values for `core.useReplaceRefs`,
`core.hooksPath`, `core.fsmonitor`, `core.pager`, and `diff.external`. Supplying
the corresponding `GIT_CONFIG_COUNT` / `GIT_CONFIG_KEY_n` /
`GIT_CONFIG_VALUE_n` entries made `git config --get` return the forced values,
and the Gitleaks scan found the planted token without attempting the hostile
fsmonitor or diff paths. This verifies named-key precedence. It does **not**
verify that `GIT_CONFIG_COUNT` neutralizes the entire local tier; it does not.

The revision will therefore:

* drop every inherited `GIT_*` variable and reconstruct only the fixed child
  values;
* force, through `GIT_CONFIG_COUNT`, `core.useReplaceRefs=false`,
  `core.hooksPath=<os.devnull>`, `core.fsmonitor=false`,
  `core.quotePath=false`, `diff.external=` and `core.pager=cat`;
* additionally force `protocol.allow=never` and `protocol.file.allow=never` as
  defense in depth against transport if a future measured invocation changes;
* retain `GIT_NO_REPLACE_OBJECTS=1`, the explicit history argv, null system and
  global config, and the selected-field report parser;
* assert the exact two-command Git invocation set in a live shim test for every
  fully supported Gitleaks version; and
* refuse to add a fully supported version if it invokes an unaccounted Git
  subcommand, drops a required option, contacts a remote, or makes another
  local-config key security-relevant without a pinned or structural control.

This is a measured finite boundary, not complete Git-config sterilization. The
residual is acceptable only while full-mode support remains exact-versioned and
each version reruns the invocation/config matrix.

### [PS9] Accepted -- scan usefully, but reserve CLEAN for measured versions

Exact-only refusal is secure but operationally brittle. It would route an
adopter who received a package-manager update to a standing command that does
nothing. A broad `8.x` full scan is also unacceptable because the history
subcommand set, CLI, output, and built-in rule corpus would become unreviewed.

The revision will use two explicit modes:

1. **Reviewed full mode.** A source-owned exact-version set, initially only
   `8.30.1`, runs both `dir` and `git`. Only this mode can reach CLEAN.
2. **Reduced-provenance current-tree mode.** A strictly parsed, otherwise
   unsupported `8.x.y` release may run only `gitleaks dir` with the same fixed
   config, suppressions, redaction, timeout, bounded report parser, and an
   off-tree empty PATH. A finding remains FINDINGS. No finding is INCOMPLETE
   because history, invocation behavior, and rule-corpus provenance are
   unmeasured. A changed CLI/output contract is DEGRADED. Other major versions,
   prereleases, and unparsable version strings do not execute and are
   INCOMPLETE.

I reproduced the key feasibility claim with 8.30.1: `gitleaks dir` found the
fixture token at exit 1 with an empty PATH and produced the expected redacted
JSON report. That does not establish future 8.x behavior; it establishes that
the reduced mode can deny Git reach without making the current supported binary
inoperable.

Reduced mode still executes a host-installed binary whose behavior has not
received Cairn's live matrix. It is not containment and cannot prove absence of
new egress or child execution inside that binary. The host executable remains
a declared trust root; the report must label this residual prominently. The
reason to accept it is limited: it can surface present-working-tree findings,
cannot produce CLEAN, cannot invoke the history leg, and avoids training users
that a version update means "no scan happened."

The support cadence becomes part of the release contract:

* scaffold summary and install output name the exact full-mode versions and the
  reduced-mode consequence before selection;
* each Cairn release tests the newest candidate Gitleaks 8.x release and retains
  every prior exact version whose matrix still passes;
* a reported real-adopter reduced-mode result is also a support-review trigger;
* adding/removing an exact version requires the live hostile-config, Git-shim,
  output-schema, no-network, and end-to-end matrices plus security-lens review;
  and
* between updates, adopters may keep useful current-tree coverage or pin one of
  the named full-mode versions outside Cairn when they require CLEAN.

The version set is source-owned, never policy-controlled. Reduced mode cannot
silently promote itself after a Cairn update; the exact version must enter the
reviewed set.

### [PS10] Accepted -- record the owner that now exists

`dependency-advisory-coverage` now owns the pre-existing `python-security`
timeout and safe-output work in its strengthened Part 3. This proposal will
cross-reference that artifact and will neither duplicate nor wait on its
implementation for the portable runner's independent controls.

### Adoption dependency now has a concrete owner

The standing invocation path is no longer undesigned. The separate
`security-verification-activation` proposal opened at `af9863c` owns the
default-on local/offline dispatcher, aggregate result, non-silent summary and
install moments, and the adopter `AGENTS.md` cadence. This proposal will record
the reciprocal dependency and remain on HOLD until that activation contract is
accepted. Its registry may invoke only the portable runner's local/offline
entry point; no network or credential-bearing route is introduced here.

### Next transition

This response leaves the proposal **reviewed**. The next commit will append the
replacement Git-config, version-mode, maintenance, activation, and test
contracts and return the artifact to `revised` for focused External re-review.

## Revised proposal, round 2 -- measured Git and usable version drift -- 2026-08-03

This section supersedes the earlier revision's threat-model wording, exact-only
version disposition, Git environment, version tests, adoption HOLD reason, and
evidence summary wherever they conflict. The one-adapter Gitleaks scope,
strict policy, two scan questions, safe output, suppression boundary, aggregate
exits, and other unchanged controls remain governing.

### Expanded candidate surface

Candidate-controlled input includes:

* tracked, untracked, ignored, and working-tree content;
* tracked attributes and every candidate `.gitleaksignore` path;
* repository-local `.git/config`, worktree config, refs, replacement refs,
  remotes, shallow boundaries, and other repository metadata; and
* strings emitted by Gitleaks or its transitive Git process.

The runner must prevent those inputs from selecting an executable, suppression,
runner argv, inherited environment, rendered terminal control, or result
classification. It does not claim to erase all repository-local Git
configuration. Instead, full-mode support is bounded by named semantic pins,
an exact measured Git invocation set, selected-field output, and exact Gitleaks
versions.

### Full-mode Git contract

For Gitleaks 8.30.1, the complete observed transitive Git invocation set is:

```text
git -C <repo> log -p -U0 --all --full-history --text --no-textconv --no-ext-diff
git ls-remote --quiet --get-url
```

The first command supplies history content. The second reads and expands remote
URL metadata but, under Git's documented `--get-url` behavior, exits without
contacting a remote. Remote/link fields are not selected into Cairn's report.
An absent remote may make that metadata lookup fail without invalidating the
secret result; the runner classifies only the supported Gitleaks contract, not
raw Git stderr.

The child environment starts from an allowlist and drops every inherited
`GIT_*`, `GITLEAKS_*`, proxy, Python-import, pager, and prompt variable. It then
sets the already specified neutral HOME/PATH and these Git values:

```text
GIT_TERMINAL_PROMPT=0
GIT_NO_REPLACE_OBJECTS=1
GIT_CONFIG_NOSYSTEM=1
GIT_CONFIG_GLOBAL=<off-tree empty file>
GIT_OPTIONAL_LOCKS=0
GIT_CONFIG_COUNT=8
core.useReplaceRefs=false
core.hooksPath=<os.devnull>
core.fsmonitor=false
core.pager=cat
core.quotePath=false
diff.external=
protocol.allow=never
protocol.file.allow=never
```

The last eight key/value pairs are encoded in ordered
`GIT_CONFIG_KEY_0..7` / `GIT_CONFIG_VALUE_0..7` variables. They outrank the
same named keys in repository-local config. The two protocol denials are
defense in depth against accidental transport; they do not convert an
unmeasured future Git argv into a supported one.

The live-contract test places a logging Git shim first on the minimal test PATH,
executes both finding and clean fixtures, and requires the exact command
multiset above with no third call. It also plants hostile local values for all
eight pinned keys and executable sentinels for hooks, fsmonitor, diff, pager,
and transport. Any sentinel execution, argv drift, network observation, or
changed result fails the supported-version matrix. The production runner still
places the verified real Git directory on PATH; the shim is measurement
instrumentation, not a shipped shell dependency.

### Two version modes

Version parsing is strict ASCII `MAJOR.MINOR.PATCH` with no prefix, suffix,
whitespace, control, or prerelease text. Policy cannot select a version or mode.

**Reviewed full mode.** A source-owned set of exact versions, initially
`{"8.30.1"}`, runs both current-tree and history legs. Each member has passed
the hostile-config, exact-Git-argv, redacted-output, no-network, fixture, and
end-to-end matrices. Only this mode can return aggregate CLEAN.

**Reduced-provenance current-tree mode.** An installed strict `8.x.y` version
outside the reviewed set runs `gitleaks dir` only. It receives the same
runner-owned config, reviewed fingerprint file, suppression override, redaction,
body/report cap, parser, and inner/outer timeouts. PATH points to an off-tree
empty directory; Git is neither resolved nor made reachable for this mode.

Reduced mode classifies:

* a validated secret result as FINDINGS (`10`);
* a validated no-finding result as INCOMPLETE (`5`), explicitly naming
  unsupported version and missing history evidence;
* CLI failure, unexpected child activity observable by the harness,
  invalid/oversized output, or schema drift as DEGRADED (`20`); and
* a missing binary, another major version, prerelease, or unparsable version as
  INCOMPLETE without execution (`5`).

Reduced mode never emits CLEAN and never describes itself as offline-verified.
It executes a host-selected unreviewed scanner binary without containment, so
absence of new egress or child execution is not established. The report names
that residual before its current-tree observations. This is accepted as useful
detection from a declared host trust root, not as evidence equivalent to a
reviewed adapter.

The aggregate precedence remains 20 > 10 > 5 > 0, so a current-tree finding is
not hidden by absent history evidence.

### Version-support operating contract

Scaffold summary, successful install output, and module doctrine must state:

* every exact full-mode version;
* that another 8.x release runs current-tree only and cannot be CLEAN;
* that other versions do not execute;
* the exact aggregate command installed by the activation module; and
* how to pin a supported Gitleaks artifact outside Cairn when full evidence is
  required immediately.

At each Cairn release, the Maintainer or delegated Security Reviewer evaluates
the newest candidate Gitleaks 8.x version. A real-adopter reduced-mode report is
also a support-review trigger. Promotion requires the full live matrix and a
security-lens review of the recorded evidence. Prior exact versions remain
supported while their matrix passes; removal requires the same visible contract
change and migration note. The source-owned set changes only in reviewed Cairn
code, never through adopter policy or ambient configuration.

This cadence does not promise same-day support for every upstream release.
During the interval the adopter gets useful current-tree findings but an honest
INCOMPLETE result, or can pin a named full-mode release. That is the intended
operational state, not an error message left without a remedy.

### Activation dependency and selection sequence

`security-verification-activation` at `af9863c` now owns the standing local /
offline invocation path previously missing from this proposal. Its default-on
dispatcher, summary/install moments, fixed registry, aggregate result, and
`AGENTS.md` cadence satisfy the adoption shape on this side. The portable
registry entry is exact and may invoke no network, credential, or arbitrary
mode.

Decision and implementation order is now:

1. accept `security-verification-activation` or revise this dependency again;
2. accept the portable capability and its preset ownership after
   `default-security-stance` establishes the shared selection mechanism; and
3. land the capability files and activation registry entry in coordinated
   plans, with the deletion-mutant test proving the standing command includes
   the selected portable leg.

Thus the former blocker "the standing invocation path is not designed" is
closed. The proposal remains **HOLD before Decision** while that activation
contract is only proposed and the reciprocal sequencing is unratified. If the
activation proposal is rejected, this module returns to deferral rather than
shipping as shelf apparatus.

### Revised tests and release evidence

In addition to the earlier matrix, the plan must test:

* all inherited `GIT_*` variables dropped and the exact eight counted keys /
  values reconstructed;
* hostile local config for every pin, duplicate local/env values, hooks,
  fsmonitor, external diff, pager, replacement refs, URL rewrites, protocol,
  and a linked-worktree config fixture;
* the exact two-command full-mode Git oracle on clean and finding repositories,
  and zero Git calls from the current-tree leg;
* strict supported, unsupported-8.x, other-major, prerelease, malformed,
  version-command failure, and path-drift classifications;
* reduced mode with an empty PATH, current-tree finding (`10`), no finding
  (`5`), changed CLI/output (`20`), and proof that history-only secrets remain
  explicitly uncovered rather than clean;
* summary/install/doctrine text naming both modes, supported versions, pinning
  remedy, activation command, and no automatic scanner execution during
  scaffold; and
* a release-evidence record containing binary checksum/source, platform,
  Gitleaks and Git versions, exact argv log, hostile-config outcomes, network
  observation method, output-schema result, and end-to-end exits for each
  promoted exact version.

The `dependency-advisory-coverage` artifact independently owns the existing
`python-security` timeout, bounded decoding, sanitization, and descendant
cleanup work identified by PS3/PS7 and strengthened by DAC6. No implementation
or CLEAN claim here depends on that sibling landing.

### Evidence and re-review gate

The 2026-08-03 Darwin arm64 probe now establishes, for Gitleaks 8.30.1 only:

* the exact two Git invocations above for the history leg;
* no Git invocation for the current-tree leg;
* named `GIT_CONFIG_COUNT` values winning over hostile local values;
* protocol denial preserving the supported scan and its no-contact URL lookup;
* full mode finding the planted token at exit 1; and
* current-tree mode with an empty PATH finding the token at exit 1 and emitting
  redacted JSON.

It does not establish cross-platform behavior, complete Git-config
neutralization, or future 8.x behavior. Those remain explicit review and plan
burdens.

This revised proposal returns for focused External Security re-review. The
reviewer should first assess the unexpected `ls-remote --get-url` call, whether
the eight pins and selected-field parser bound its candidate metadata, and
whether automatically executing reduced-mode current-tree scans is acceptable
given the named unmeasured-binary residual.

## External Security Review, round 3 -- Claude -- 2026-08-03

**Model**: Claude Opus 5
**Tier**: External (different agent type), security lens
**Reviewed**: the round-2 response and revision, against the shipped
`run_security_audit.py` and the sibling `security-verification-activation`.

**Disposition: NO BLOCKING FINDINGS.** PS8, PS9 and PS10 are resolved, and PS8
is resolved by evidence that goes past what either the revision or my review
knew.

**PS8 — the shim found something neither of us named.** I suggested a logging
`git` shim on the adapter's minimal PATH to establish the invocation set rather
than assume it. That was run, and it recorded **two** invocations for
`gitleaks git`, not one:

```text
git -C <repo> log -p -U0 --all --full-history --text --no-textconv --no-ext-diff
git ls-remote --quiet --get-url
```

The second was absent from the prior evidence and from my review. The
disposition is also correctly reasoned rather than alarmist: `--get-url` expands
URL-rewrite configuration and exits without contacting the remote, so it is a
candidate-controlled **metadata input**, not observed egress. The threat model
now names repository-local `.git/config`, refs, shallow boundaries and remote
metadata as inputs, and drops the claim that neutralising the system and global
tiers disables the local one. That was the substance of PS8.

**PS9 — the consequence is now owned** rather than left implicit, which was the
whole finding; the reasoning for pinning was never in dispute.

**PS10** — the cross-reference landed; I verified three references to
`security-verification-activation` in this artifact, so the AW7 interval that
made this record misleading is closed.

**Nothing further from me.** The remaining open item is the author's own
adoption HOLD, which is a Maintainer question about whether the activation path
is worth building, not a security finding. I have no basis to hold this artifact
on security grounds.

**Scope:** I did not re-execute the Gitleaks probes, evaluate detection quality,
or review the activation proposal here.

## Decision -- Anthony Kendall (Maintainer) -- 2026-08-03

**ACCEPTED as revised, with two conditions binding on the plan.** Scribed and
committed by Claude at the Maintainer's explicit instruction.

**Maintainer's authorization, quoted verbatim:**

> I accept this proposal as revised. Disposition this so that the plan builds an
> apparatus to address the GitLeaks versioning . We should adopt it here so that
> we can evaluate and test it.

**What is accepted.** The team-gated `portable-security-sweeps` module as
narrowed in revision: a standard-library orchestrator, a strict JSON policy, a
fixed adapter registry, the shared aggregate exit contract, and **one** adapter
— Gitleaks, offline, with no network flag in v1.

### Condition 1 — the plan builds a version apparatus, not a documented fallback

The revision pins **exactly Gitleaks 8.30.1** and, per the round-2 response to
finding **PS9**, adds a reduced-provenance mode so an unmeasured version cannot
produce CLEAN. This condition goes further: the plan must build the
**apparatus** by which a version is *admitted, re-measured, and retired* — the
mechanism, not a one-off mode.

The finding that motivates it, so the plan does not re-derive it: Gitleaks
releases frequently, so for any adopter not on the pinned version the steady
state is INCOMPLETE with no scan performed. Pinning is sound — a broad `8.x`
range would make built-in rules and CLI behaviour mutable, and therefore make
the gate's meaning mutable — but the consequence needed owning rather than
documenting. The reduced-provenance mode is the starting point, not the end
state.

What the apparatus must make routine rather than heroic: rerunning the hostile
ambient-config and output-schema matrix against a candidate version, recording
what was measured, and admitting or refusing that version on evidence.

### Condition 2 — Cairn adopts the module itself

Cairn installs and runs this module on its own tree, so the design is evaluated
by use rather than by argument. This is consistent with Cairn being its own
first adopter, and it is the condition that makes Condition 1 testable: Cairn's
own runs will exercise the version apparatus, including the case where the
installed Gitleaks is not the pinned one.

Two consequences recorded at Decision time: Cairn takes on Gitleaks as a
dev/CI dependency of its own (the module still installs no scanner — the
zero-dependency contract for *shipped runtime* is unchanged), and Cairn's own
install becomes the first evidence about whether the module is usable rather
than merely correct.

**This resolves the adoption HOLD.** The proposal's adoption amendment held
implementation pending a standing invocation path and asked whether the module
was worth building at all. The path now exists —
`security-verification-activation`, accepted the same day — and this Decision
answers the second question affirmatively by directing adoption.

**Review tier discharged.** Required `required(External, security lens)`;
received a Gemini Flash External round and **three** Claude External rounds, the
last with no blocking findings. Findings were closed by execution rather than
argument: the `.gitleaksignore` file loads even when `--gitleaks-ignore-path`
names a trusted empty file, so the runner refuses before execution; and a
logging `git` shim recorded **two** Gitleaks invocations rather than one, the
second (`git ls-remote --quiet --get-url`) absent from all prior evidence
including the reviewer's.

**Next transition:** plan-open. The plan carries `required(External, security
lens)` in its own right, and both conditions above are in its scope; this
Decision does not discharge that review.

**Decision-only commit.** Status flip and this section, nothing else.
