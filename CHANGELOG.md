<!-- A release history necessarily names files as they were at each version; a
     path that later stopped existing does not make the entry wrong. -->

# Changelog

Notable changes to Cairn, newest first. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

**Adding an entry.** Each change adds one entry under `## Unreleased`, in the
same commit or the next.

- **Group it.** Put it under **Major changes** if an adopter would notice it or
  must act on it: a new capability, a change to how they work or what the tools
  do, a security fix, or a removal. Everything else goes under **Minor changes**.
- **Type it first.** Start with one of **Added**, **Changed**,
  **Deprecated**, **Removed**, **Fixed** or **Security**, then ` — `. Keep
  each group in that order, as Keep a Changelog does.
- **One sentence, one link.** Say what changed for the reader, then link the
  plan or proposal. Review, certification and ceremony status stay in the plan.

At a release, rename `Unreleased` to the version and date, and open a new empty
`Unreleased` above it.

## Unreleased

### Major changes

- **Added** — Installed modules get a selection-specific inventory and optional first-use tasks, including later adoption and conservative recovery when existing work conflicts. ([plan](dev/plans/archive/2026-10-29-module-discovery-activation.md))
- **Changed** — Plans and proposals carry less paperwork: the templates repeat less text, and a plan needs no evidence folder unless the work requires one; lifecycle, security and verification obligations are unchanged. ([template plan](dev/plans/archive/2026-11-01-template-burden.md), [evidence plan](dev/plans/archive/2026-10-30-plan-evidence.md))
- **Changed** — Test-once scopes iteration to the changed files and runs the final integration check once after review, narrowing only above the 40-reader guard and reporting every omitted reader. ([proposal](dev/proposals/archive/2026-10-30-claude-test-once-per-change.md))
- **Changed** — Module inventory markers are handled safely: upgrade review copies show the recorded module roster in the upstream `.theirs` copy and keep your bytes in `.ours`, and install, module adoption and staging refuse ambiguous or malformed markers before changing anything. ([rendering plan](dev/plans/archive/2026-10-30-review-inventory-rendering.md), [marker plan](dev/plans/archive/2026-10-30-module-marker-ambiguity.md))
- **Changed** — Review is one bounded pass per stage, light is the default proposal tier, added or widened trust boundaries still get a Security Review, and governing instructions are shorter. ([plan](dev/plans/archive/2026-10-30-cut-the-apparatus.md))
- **Changed** — Handoff preparation now captures the reflection, surveys threads and intents, and shows a preview before you receive the guarded prune command. ([plan](dev/plans/archive/2026-10-30-handoff-preparation.md))
- **Changed** — Change verification is mapped per change and whole-tree certification is separate, and plan, proposal and strategy file names now include their opening date. ([plan](dev/plans/archive/2026-10-28-scoped-change-verification.md); [verification doctrine](doctrine/plans.md))
- **Changed** — Capability floors now follow the task: ordinary authorship and reviews are medium and executing an accepted reviewed plan is low, with a dated local model mapping of three families per tier. ([plan](dev/plans/archive/2026-10-28-model-floor-alignment.md); [roles](doctrine/roles.md))
- **Security** — The local security dispatcher now runs the installed content-security scan and gives API checks only the credentials its validated local policy names; it refuses substituted code and reports unreliable or flagged results instead of claiming clean. ([scan plan](dev/plans/archive/2026-10-29-dispatcher-content-scan.md), [credentials plan](dev/plans/archive/2026-10-30-api-dispatch-credentials.md))
- **Security** — Upgrade now checks saved ancestor bytes before merging, keeps corrupt evidence through repeated manual recovery, refuses specified invisible path characters, and escapes supplied install names in reports; the check catches inconsistent local records but cannot authenticate a cache and lockfile edited together. ([plan](dev/plans/archive/2026-10-30-upgrade-install-integrity.md))
- **Security** — Upgrade refuses project paths that lead into nested Git data, and `upgrade --init-lock` refuses a planted link at any mapped installed path before reading it; hard-link aliases and changes made after a check are not covered. ([nested Git plan](dev/plans/archive/2026-10-30-nested-git-upgrade.md), [init-lock plan](dev/plans/archive/2026-10-30-init-lock-linked-files.md))

### Minor changes

- **Added** — Release publication has a read-only check for the published Release and the signed tag's remote commit, and the guide now separates pushing the signed tag from publishing its Release. ([plan](dev/plans/archive/2026-10-30-tag-release-distinction.md))
- **Added** — Re-anchor and repin have reusable preparation, verification and supervised ceremony commands, and forward-baseline preparation uses independently reviewed inputs. ([commands plan](dev/plans/archive/2026-10-29-ceremony-commands.md), [baseline plan](dev/plans/archive/2026-10-29-forward-trust-baseline.md))
- **Added** — Test-trust boundary machinery separates protected tests from ordinary test changes, with signed-roster authority and two-stage checks. ([plan](dev/plans/archive/2026-10-28-test-trust-boundary.md))
- **Changed** — Review guidance and shipped templates now keep repeatable checks in tests and scripts, and mapped tests catch the removed review-record requirement coming back. ([plan](dev/plans/archive/2026-10-30-probe-ledgers.md))
- **Changed** — Shuffled review-sweep tests reuse each profile install for the pytest session, cutting measured setup from 31.26s to under 1s. ([plan](dev/plans/archive/2026-10-30-certification-cost-audit.md))
- **Changed** — Coordination guidance is clearer: commits to shared files need agreed serialization and inspection, and the work-intent guidance and CLI help say when a claim blocks, what is exempt and the limits of identity. ([sweeps plan](dev/plans/archive/2026-10-30-same-file-sweeps.md), [intent plan](dev/plans/archive/2026-10-30-intent-guidance.md))
- **Changed** — The evidence-stage boundary admits and removes only pytest's exact cache-only setting. ([plan](dev/plans/archive/2026-10-29-release-evidence-environment.md))
- **Changed** — The ordinary board JSON pilot centralizes repeated archive-output capture, and the shipped and self-hosted modules gain matching test-maintenance guidance. ([plan](dev/plans/archive/2026-10-28-ordinary-test-maintenance.md))
- **Changed** — The governing-text inventory picked a documentation home for public methodology explanation, and the accepted-scope template drops repeated rationale. ([plan](dev/plans/archive/2026-10-28-governing-text-single-source.md))
- **Fixed** — Certification tests now repair dispatcher record fixtures and the archived baseline path, and isolate the real ceremony boot while keeping adversarial controls. ([plan](dev/plans/archive/2026-10-30-certification-test-repairs.md))

## 0.5.0 — 2026-10-28

### Major changes

- **Added** — Cairn Plain Language 1.0, a 17-rule writing standard for everything agents write for people: every install carries it in `dev/agent_collaboration.md`, and `docs/plain-language.md` is a full adoption page with the copyable rules, an evidence table and a 30-source bibliography. ([proposal](dev/proposals/archive/2026-10-27-antigravity-plain-language-adoption-docs.md), [rationale](doctrine/rationale.md))
- **Added** — `scripts/repin.py` gives the routine gate re-pins three commands, `status`, `package` and `ceremony`, which stop before the Maintainer types the signing passphrase and never read it. ([plan](dev/plans/archive/repin-build.md))
- **Added** — `upgrade --remove-retired` removes a project's untouched copies of files Cairn stopped shipping, and keeps and names any copy that differs, is untracked or sits behind a link. ([plan](dev/plans/archive/upgrade-removes-retired-files.md))
- **Added** — Drain mode: `/session-start --drain [board | issues | <item>]` sorts open items by lifecycle lane, fixes trivial ones with a failing test, has a fresh session review each fix, and commits locally without posting to GitHub. ([plan](dev/plans/archive/drain-mode.md))
- **Changed** — The re-anchor ceremony needs no outside reviewer: your part is comparing digests, running a few checks, reading a plain report and saying yes, and the old hand path (`drive()`, `--run`, the digest-correcting script) is gone. ([plan](dev/plans/archive/ceremony-without-external-review.md))
- **Changed** — The next-session handoff is a local, untracked note at `dev/reflections/next-session.md` instead of a shipped `dev/NEXT_SESSION.md`; it is read as a hint, never instructions, and counts as absent after 14 days. ([plan](dev/plans/archive/next-session-local-note.md))
- **Changed** — The install report lists slots that only an uninstalled module fills apart from the main list, and `upgrade --plan` and `--stage` print a `[new slot]` line for slots a new template adds. ([plan](dev/plans/archive/engine-batch-f8-slots.md))
- **Changed** — Every install now states which model tier a job needs: the lane sets the lowest tier that may write the work, Security Review stays at high, and a stronger model from the same maker counts as the independent check.
- **Changed** — A trivial change needs no plan and no code review, provided it stays one commit and one area and its final test run would cover only the tests that name it. ([plan](dev/plans/archive/no-plan-changes-end-to-end.md))
- **Removed** — The delayed onboarding prompts, the goodnight helper that never ran, its activation log and eight support files are gone; their content now lives in the day-one task list, so new installs have nine fewer files and an install report about ten lines shorter. ([plan](dev/plans/archive/install-time-onboarding.md))
- **Security** — The re-anchor ceremony now protects its launcher template as the eleventh checked file, and the runbook no longer claims that handing over the launcher separately adds assurance; the check that the launcher in hand equals the template is still a manual step. ([plan](dev/plans/archive/repin-ceremony-hardening.md))
- **Security** — `upgrade` no longer runs programs named in a project's git settings (file-system monitor, clean filter, text converter, hook) when it checks for unsaved edits, and it reads projects in a subfolder of a larger repository correctly. ([plan](dev/plans/archive/upgrade-edit-check-no-repository-programs.md))
- **Security** — `upgrade --plan`, `--stage`, `--adopt-module`, `--adopt-collisions` and `--init-lock` stop with exit 2 when `dev/.cairn/profile.yml` (or, for `--init-lock`, `dev/.cairn`) is a link, instead of reading what it points to, and `--finalize` names a linked vendor wrapper and says to replace it. ([upgrade guide](bootstrap/UPGRADE.md))
- **Security** — `upgrade --apply` no longer writes outside the project through a linked profile, and also refuses a linked lockfile, option-like saved commit names, control characters in module and review-area names, a linked vendor wrapper, and records naming files inside `.git/`; four older findings remain queued. ([review](dev/plans/archive/2026-10-19-security-review-upgrade-lockfile-paths.md))
- **Security** — `session-start` no longer runs a program inside the project that git tracks, recognizes the binding file on case-insensitive disks, refuses a bad binding plainly, and encodes project-supplied text in seven more places; child-process output is still printed unencoded. ([review](dev/plans/archive/2026-10-18-security-review-session-writes.md))

### Minor changes

- **Changed** — The plan and proposal templates add "Keep the plan short" and "Keep the proposal short" sections saying what stays out of the file. ([issue #31](https://github.com/MSUHydrogeology/cairn/issues/31))
- **Fixed** — `upgrade --finalize` on a kept, edited fold-back ledger from an old install now leaves a tree that `verify_integrity` accepts.
- **Fixed** — `link_check.py`, `sync_doc_snippets.py` and `check_cairn.py` skip a tracked Markdown file deleted from disk but not yet committed, instead of crashing. ([proposal](dev/proposals/archive/2026-10-26-claude-check-cairn-deleted-files.md))
- **Fixed** — The board and `session-start` now name an active proposal or plan with a retired or unknown status in one advisory line. ([#32](https://github.com/MSUHydrogeology/cairn/issues/32))

## 0.4.0 — 2026-10-20

### Major changes

- **Added** — Agents may fix cheap defects that break promises already documented in a file, must give one of three reasons to defer work, and must search for reusable code before adding new. ([plan](dev/plans/archive/stewardship-and-reuse.md))
- **Added** — Non-interactive installs, module adoption and upgrades now emit a notice when the model selection mapping is unfilled. ([plan](dev/plans/archive/model-mapping-install-path.md))
- **Added** — `python tools/board.py --json` prints every proposal and plan as plain data (contract `cairn-board/1`), `--maintainer` lists everything waiting on the Maintainer, and the templates prompt for an `In brief` line the board reads. ([plan](dev/plans/archive/board-as-basis.md), [guide](docs/build-a-board-view.md))
- **Added** — The proposal template now asks for one independent scientific check when a change touches a scientific result, and the plan template makes that check accepted scope that only the Maintainer can drop.
- **Added** — `verify_integrity.py` now prints an advisory listing slots that still hold Cairn's placeholder, with a coverage line saying what it could not check.
- **Added** — A hand-copied kernel now has a documented way in: `scaffold.py upgrade --target <repo> --init-lock`, fill four placeholders, then re-run.
- **Added** — Scope reduction now has a trap: narrowing is judged against the artifact as opened or accepted, and a degraded or lost outcome needs a `Scope delta` and the Maintainer's explicit allowance.
- **Added** — Selecting a security capability now runs a default-on local verification dispatcher whose authority can only narrow and whose registry ships empty.
- **Added** — Three opt-in security modules: `api-access-security` and `web-hosting-security` check a declared authorization matrix and HTTP/TLS settings, with agents limited to the local machine, and `portable-security-sweeps` runs a Gitleaks adapter you provide and reports `INCOMPLETE` without it.
- **Added** — The proposal template gains a gated "Security preflight" block of five questions a security-touching change must answer before review.
- **Added** — `bootstrap/PROVENANCE.md` now publishes an out-of-band bootstrap for verifying a release's signed tag with system `git`, plus key rotation and its limits.
- **Changed** — Every install now gives each review the same evidence questions: the nine lenses and falsification ledger live in the installed review-loop document, and an outside read happens only when the Maintainer calls it. ([plan](dev/plans/archive/review-stance-and-lenses.md), [upgrade guide](bootstrap/UPGRADE.md))
- **Changed** — After `--apply`, upgrade now has you run `python bootstrap/verify_integrity.py --target <repo>`, and a filled slot is recorded with `upgrade --finalize <path>`.
- **Changed** — Work handed to a plan that is not yet open must become a board row, since a pointer to an archived file is not a home.
- **Changed** — A review reads a commit, never a shared working tree, and tests an "every place" claim by changing each member of the set to see whether a test catches it.
- **Changed** — A small fix with no plan now runs the tests that own what it touched and records them in its commit body.
- **Changed** — Authorization is now a Maintainer-signed checkpoint bound to a range-review report, and unsigned intermediate commits no longer refuse a ceremony.
- **Changed** — `lifecycle-metrics` moves to schema v2: retained fields now come from `cairn-event-v1` event blocks, and a `schema_version` column separates v2 from v1 snapshots.
- **Changed** — An External proposal review that records `Plan readiness: READY` now lets the plan take a fresh-context Internal review instead of a second cross-type read.
- **Changed** — Session-start orientation now routes through `python tools/lifecycle_planner.py board --compact` instead of opening every active record.
- **Changed** — The homoglyph detector now asks whether characters are confusable, so scientific Greek notation stays clear while Latin/non-Latin lookalikes are still flagged.
- **Changed** — New installs now include content scanning by default (`content-security`, with a `modules_remove` opt-out), and `python-security` is added for declared Python projects.
- **Removed** — The collaboration agreement is no longer installed in new projects; existing copies stay, and `upgrade --plan` reports it as `removed-upstream`. ([plan](dev/plans/archive/remove-collaboration-agreement.md), [upgrade guide](bootstrap/UPGRADE.md))
- **Removed** — Adoption levels are retired: Cairn no longer publishes them, and the onboarding helper's level classification and "Level 1→2 graduation" prompt are gone; read the doctrine, or install with the scaffold and a profile.
- **Removed** — Eight review-prose-derived columns of `lifecycle-metrics` and the `--backfill-from` option are removed.
- **Fixed** — The advisory for a modified `scaffold.py` launcher (a forked facade) compares against trusted upstream bytes, names what it compared against, and advises only restoring the launcher from upstream.
- **Fixed** — The Python dependency audit now proves what it covered and reports CLEAN only with zero unknown dependencies and zero findings.
- **Fixed** — `claim_check` now accepts the `path::node` citation form that doctrine requires, resolving it on its path half.
- **Fixed** — The `lifecycle-metrics` commit-stage vocabulary now reads real commit subjects, so interval columns fill and timestamp reliability is no longer almost always `Best-effort`.
- **Fixed** — The intent post-commit hook no longer warns about unconfigured agent identity on human commits that have no live claims.
- **Security** — The model-selection check now skips comment lines, parses YAML values safely, and refuses merge-key recursion attacks. ([plan](dev/plans/archive/model-mapping-install-path.md))
- **Security** — Installer writes (interactive capture, `.gitignore` seeding, lockfiles) are now atomic and cannot be redirected through symlinks, hardlinks or racing temp files, and the lockfile reader refuses non-regular files. ([plan](dev/plans/archive/model-mapping-install-path.md))
- **Security** — The board now skips symbolic links and refuses non-regular files instead of hanging, so a `dev/` folder kept as a symlink reads as empty after upgrading. ([plan](dev/plans/archive/board-as-basis.md))
- **Security** — The integrity report and the lifecycle orientation output escape text from the lockfile and repository, so a crafted file name or status cannot inject control characters or forge lines.
- **Security** — `bootstrap/security_check.py` takes object ids from Git itself, refuses a folder that is not a repository instead of falling back to SHA-1, and checks object integrity in a clean context the checked repository cannot configure, so its own `fsck.skipList` cannot hide a corrupt object.
- **Security** — Content scanning flags invisible Unicode (ignorable characters, Tag characters, line separators) and checks URLs strictly outside `dev/**` and `docs/**`, which it reads as discussion; lines with emoji variation selectors may gain findings after upgrading.
- **Security** — `verify-ref.sh` now checks the signature of the exact tag you asked about, so a ref re-pointed at another signed tag is refused; the unsigned pin needs `--unprovenanced` and exits 3.
- **Security** — A byline with a look-alike character can no longer pass as a human Maintainer, so `human_maintainers` entries must now be the full display name, spelled with ASCII spaces.

### Minor changes

- **Added** — `docs/build-a-board-view.md` documents the board data schema and its contract promises with a standard-library example (published in Cairn's docs, not installed). ([plan](dev/plans/archive/board-as-basis.md), [guide](docs/build-a-board-view.md))
- **Added** — Cairn's test suite now records its own cost in a gitignored ledger that `tools/suite_cost.py` renders without running anything.
- **Added** — `bootstrap/tests/_gate_preflight.py` now performs the supervised gate re-anchor pre-flight checks and advances the branch and anchor in one transaction.
- **Changed** — The doc-drift module now names a third kind of drift: prose that names a function the code no longer has.
- **Changed** — Code review is no longer described as External by default; External is an escalation for risk the proposal review did not resolve.
- **Changed** — The solo-legacy recipe now installs with the scaffold, with its roster corrected to the eight modules it installs.
- **Changed** — Doctrine now states that a proposal Response always carries one complete current contract, matching what the conformance check already enforces.
- **Changed** — The authoring templates now teach the typed-declaration registry for exact paths that recur in a document.
- **Changed** — `python bootstrap/security_check.py` now covers Cairn's complete local release security bar in one Maintainer-run command.
- **Fixed** — Three sentences in the complexity dimension, its README and the bootstrap guide no longer promise a review lens that no module installs.
- **Fixed** — `python scripts/quality_gate.py --sub neutrality` now reads `fail=0`: every shipped vendor-name leak was reworded and the check slightly tightened.
- **Fixed** — `upgrade --init-lock` no longer recommends a re-install, which over an existing tree writes no lockfile.
- **Fixed** — Object-id widths are now read from the repository's object format, so a SHA-256 repository is no longer refused on the public path.
- **Fixed** — Unicode findings now carry their literal pattern id instead of inferring it from message prose.
- **Fixed** — The release Bandit gate now scans every Python file the installer ships and fails closed when Bandit cannot open a file.
- **Fixed** — `check_cairn` no longer hard-fails on `dev/` paths cited across Cairn's own doctrine, templates and changelog when self-hosted.
- **Fixed** — The `v0.3.0` release commit's quality-gate attestation is corrected; it had claimed a clean run that did not reproduce.

## 0.3.0 — 2026-06-12

### Major changes

- **Added** — `scaffold install` now prompts for your tier-to-model bindings when the `model-selection` module is chosen, so the fidelity gate ships green; non-interactive installs keep the `FILL ME` stub.
- **Added** — `link_check` now ignores links inside balanced inline code spans and honors a file-level `<!-- link-check-allow: ... -->` directive, matching `claim_check`.
- **Added** — `upgrade` carries new files of modules you already adopted, `--adopt-collisions` keeps a customized file that collides with a new upstream file as a tracked fork instead of blocking, and `--apply` fails closed if a new file's destination appeared after `--stage`.
- **Added** — The onboarding launcher and its engine are now tracked in the lockfile and covered by the release security scan, and a new core file landing on an occupied untracked path is a hard block rather than an overwrite.
- **Added** — A container recipe under `bootstrap/container/` lets a team with no host Python run the install and upgrade engine in a throwaway container.
- **Added** — A lifecycle state-machine contract and a read-only `tools/lifecycle_planner.py` (`next`, `scan`, `guard`) report a proposal or plan's state, legal transitions and unmet preconditions without ever changing or committing anything.
- **Added** — A standard-library-only security stack: `content-security` gains a fail-closed self-audit runner, a new opt-in `python-security` module orchestrates bandit, content scan and pip-audit, and install fails early when a selected module's required token is unfilled.
- **Added** — The core `AGENTS.md` template supports `<!-- cairn:if AXIS in ... -->` regions so sections can be included only for matching profiles; the `Human contributors` section is now included only for multi-person teams.
- **Added** — The `session-start` and `session-end` skills point to an optional project-owned `dev/rules/custom_session_routines.md`, giving adopters an installable home for their own routine steps.
- **Added** — A new `dev/measurement/` folder gives every adoption a standard home for its process-health records, and the `lifecycle-metrics` and `incident-trackers` modules now point to it.
- **Added** — Reviewers work a 9-lens review sweep with a two-part coverage line, shipped in the `dual-review` module, and the proposal and plan templates gain a triage-gated author-accounting block.
- **Added** — `scripts/token_budget.py` measures the always-on load against a soft cap, a cache-stable load-order convention is documented, and the core `AGENTS.md` Git-workflow section is about 22% shorter.
- **Added** — The `model-selection` module gains fan-out guidance: each leaf task takes its tier from its own task, never from the orchestrator, and no downshift crosses a data-governance boundary.
- **Added** — Four adopter-proven items join the framework: a dual-review case study, the `claim-check` verify-before-asserting typology, a "lead with the domain" line for surfacing judgment calls, and an opt-in signature-log pattern for the collaboration agreement.
- **Added** — `upgrade --finalize` advances lockfile hashes to the committed on-disk content, so a customized install verifies cleanly; given paths, it re-records only those files, and without paths it refuses a dirty tree unless you pass `--force`.
- **Added** — The proposal and plan templates gain the adopter-developed detail on forward-reference markers, archive preconditions, plan triage, plan review and code-review ledgers, plus five new adopter slots.
- **Added** — `session-start` and `session-end` are invokable skills (`/good-morning`, `/goodnight`) backed by a standard-library `tools/lifecycle.py`, and `session-start` repairs a missing or stale `.claude/skills` link so adopters set up by lockfile copy get their skills.
- **Added** — A new opt-in `architecture-review` module gives teams whose architecture accreted rather than was designed a five-lens review frame to fork into `dev/architecture_review.md`.
- **Added** — `tools/intent.py whoami` prints the per-session identity, and reflection filenames now reuse that session token so a reflection links to its intent-log entries.
- **Added** — Module install now merges module content into target files mechanically, deferring conflicts to a `.cairn-merge-pending` side-file (`--non-interactive` forces deferral), and catches duplicate slots and wrong-slot pastes.
- **Added** — `templates/core/AGENTS.md` gains an "Untracked lifecycle artifacts" section with a cold-start recovery procedure for uncommitted proposal or plan drafts.
- **Added** — Two default-on modules: `documentation-plan` adds a procedure for deciding where a document belongs and a forkable `docs/DOCUMENTATION_PLAN.md`, and `incident-trackers` adds a forkable incident tracker and a goodnight migration step.
- **Added** — Progressive onboarding turns PLANNING into an on-ramp with preset task lists, maturity and action triggers, and at most one active prompt per goodnight, plus new tour docs.
- **Added** — Fold-back now has an active-surfacing protocol with GitHub issue and PR templates, an export-scrub scanner for credentials, private paths and IPs, and a helper that lists candidates ready to file.
- **Added** — `scripts/quality_gate.py` bundles order-independence, vendor-neutrality and redundancy checks into one pre-cut gate (`--sub <name>` to pick one).
- **Added** — `claim_check.py` gains a `claim-check-allow` directive that exempts named paths in one document, and no longer soft-flags numbers next to words like `lines` or `tests`; approximate, date or register a count instead.
- **Added** — Seven entry-surface artifacts: a quickstart, three profile presets, a bootstrap-lite prompt, a codebase-readiness report template, a scientific-minimal example, a README trust box, and honest-framing callouts.
- **Changed** — Archiving now needs a recorded disposition for each deferred follow-up (`accept`, `wontfix`, `defer`, or the new `guard`) instead of just a home on the roadmap board; `Dispositions:` replaces `Follow-ups migrated to:` and old records stay valid.
- **Changed** — Four upgrade and verify fixes: `--adopt-module` notes a local file that a module now supersedes, intent tooling reads `dev/.cairn/intent-config.json` (the old path still works), `check_model_selection.py` checks mapping structure when PyYAML is present, and a forked facade with a dormant installed engine is flagged.
- **Changed** — The proposal and plan templates shrink from ~800-line manuals to short form skeletons, with the teaching moved to new `doctrine/proposals.md` and `doctrine/plans.md` pages.
- **Changed** — The lifecycle-metrics tool gains the measurement subsystems from the adopter fork (annotation counts, collision log, review yield, model tier, output manifest), reads settings from `dev/.cairn/metrics-config.json`, and `--snapshot` now writes indexed `dev/measurement/snapshots/<YYYY-MM-DD>-<N>.csv` files instead of overwriting a per-day proposals CSV.
- **Changed** — `scaffold.py` is now a thin launcher over a private `bootstrap/_scaffold/` package with the same public surface, but tests that monkeypatch must patch the owning submodule rather than the `bootstrap.scaffold` facade.
- **Changed** — Adoption state moves into `dev/.cairn/`: the lockfile (`cairn-lock.yml`, which existing adopters move), the profile (`profile.yml`) and the fidelity manifest, whose old location still works.
- **Changed** — `upgrade --init-lock` now captures the full six-axis profile (failing with a template to complete if none is committed), and `upgrade` rebuilds a missing `dev/.cairn/profile.yml` from the lockfile.
- **Changed** — The windowless commit is now the primary concurrent-session habit: `git commit <paths>` stages and commits in one step, and you verify with `git status --short` and `git diff <paths>` instead of the shared index.
- **Changed** — The work-intent pre-commit check gains an `enforce` setting (`warn`, `confirm`, `block`) and recognizes your own claims by session token, so it warns only about other sessions.
- **Changed** — `scaffold.py upgrade --apply` now refuses when it would overwrite a tracked file with uncommitted edits (`--force` overrides), and `--stage` warns instead.
- **Changed** — `link_check` skips `file://` links and by default excludes `dev/modules/` and `dev/.cairn/` (`--include-modules`, `--include-cairn`), and both `link_check` and `check_cairn` skip archived and reflection files unless you pass `--include-archives`.
- **Changed** — `verify_integrity` no longer flags routine edits to the four adopter-authored living-state files (roadmap, handoff, fold-back ledger, collaboration agreement), while still failing closed if any other file claims that exemption.
- **Changed** — Dual-review now requires a clean code review to show a four-part falsification ledger (or a second independent pass), the collaboration doctrine names a standard session handoff format and a no-cross-attribution review rule, and readiness reports gain a `Status:` field.
- **Changed** — `upgrade` now lists customized files that need a manual merge, stages a review pair for each, and refuses `--apply` until you pass `--ack-review-only`; `--init-lock` also recognizes a renamed vendor wrapper.
- **Changed** — Plan and strategy lifecycle commits may now proceed without per-commit approval, alongside proposals, with the same push and Decision guard-rails.
- **Changed** — `doctrine/doc-governance.md` now covers both governing-file routing and the descriptive `docs/` layer, with common homes for vision and style docs and a note that your docs format is your choice.
- **Changed** — The `upgrade --plan` and `--stage` summary now separates untouched files from locally modified files that merged cleanly.
- **Fixed** — A renamed vendor wrapper (such as `CLAUDE.md`) no longer triggers a spurious "file missing" `review-only` on every `upgrade`.
- **Security** — The onboarding-activate helper now refuses to read or write through symlinks or outside the project, and rejects path-traversal in `--preset` names with a security error.

### Minor changes

- **Added** — `_ast_attest.py` gains a hardened `update-symbol` subcommand and a new `_gate_manifest.py` freezes gate integrity, so unattended registry-cascade batches are risk-bounded by mechanism.
- **Added** — Cairn-maintainer-only `scripts/verify_counts.py` and `scripts/measurements.py` re-measure registered live counts against `<!-- verify: <key> -->` annotations and are wired into `check_cairn`.
- **Added** — `check_cairn` gains a loop-fidelity lens that fails when an adopter-facing template references a Cairn-internal `doctrine/*` path that would dangle after install.
- **Added** — Proposal and plan templates now teach the four ways to clear a count-claim soft flag.
- **Added** — Cairn's own smoke tests now cover the profile presets, the quickstart sequence and the scientific-minimal example.
- **Changed** — `doctrine/rationale.md` is regrouped into a Foundation plus four themed clusters, adds four anchors from the reference adopter, and `docs/further-reading.md` gains a verification-and-validation reading slot.
- **Changed** — The behavioral guard now builds its "before" engine from a trusted git ref and runs only during refactors, replacing the checked-in frozen `scaffold_frozen.py` fixture.
- **Changed** — The `intent.py` and progressive-onboarding tools are split into thin launchers over owned engine packages (`_intent/`, `_onboarding/`), with public behavior and write-containment guards unchanged.
- **Fixed** — The forkable incident-log template no longer shows as `needs-value` on every adopter upgrade, because its placeholders now use angle-bracket syntax.

## 0.2.0 — 2026-05-27

### Major changes

- **Added** — A new `content-security` module lets adopters scan files and PRs for prompt injection, and `verify_integrity.py` detects post-install file modification against the lockfile.
- **Added** — New doc-governance doctrine, reviewer decision-support, a Decision-scribing guard-rail, and a default-on `fold-back-ledger` module for sending improvements back to Cairn. ([doc-governance](doctrine/doc-governance.md))
- **Added** — `scaffold.py upgrade` merges new Cairn doctrine into a customized install without clobbering local edits, using a new `dev/cairn-lock.yml` lockfile. ([UPGRADE](bootstrap/UPGRADE.md))
- **Added** — Three governance presets (`solo-greenfield`, `collaborative-team`, `high-rigor-legacy`) set a baseline module roster, and `scaffold.py --summary` previews the result before installing.
- **Added** — The `coordination-tiers` module installs `tools/intent.py`, a work-intent CLI with `claim`, `list` and `release`, plus opt-in hooks that warn when a commit touches an unclaimed path or one another session holds. ([coordination-tiers](templates/modules/team-gated/coordination-tiers.md), [intent.py](templates/modules/team-gated/intent.py))
- **Added** — Three new modules cover testing discipline, an examples gallery and doc-drift prevention (which installs `link_check.py` and `sync_doc_snippets.py` to catch broken links and stale doc snippets), and a maturity ladder helps teams find their adoption level. ([testing-discipline](templates/modules/team-gated/testing-discipline.md), [doc-drift-prevention](templates/modules/team-gated/doc-drift-prevention.md), [on-ramp](on-ramp/README.md))
- **Added** — The default-on `claim-check` and `lifecycle-metrics` modules now install runnable standard-library scripts instead of pointing adopters at code to copy. ([claim_check.py](templates/modules/default-on/claim_check.py))
- **Added** — New adopter-orientation docs and a minimal worked example trace one change through the lifecycle. ([getting-started](docs/getting-started.md), [examples/minimal](examples/minimal/))
- **Added** — Eleven doctrine mechanisms are ported in, including new `security-review` and `issue-capture` modules and a rate limit on doctrine changes. ([security-review](templates/modules/team-gated/security-review.md), [issue-capture](templates/modules/team-gated/issue-capture.md))
- **Added** — Coordination identity is now derived per session rather than per tool, so concurrent sessions of the same tool no longer release each other's claims. ([coordination](doctrine/coordination.md))
- **Changed** — Every plan now carries a mandatory `Plan review: required(<tier>) | not required(<rationale>)` line, and a required plan is reviewed before implementation begins. ([lifecycle](doctrine/lifecycle.md))
- **Changed** — A work-intent `claim` is now required before every nontrivial edit when a team works concurrently, though it stays a courtesy signal and not a lock. ([coordination](doctrine/coordination.md))
- **Changed** — The goodnight routine gains a staleness sweep, and archiving a plan or removing a roadmap item now has stated preconditions. ([lifecycle](doctrine/lifecycle.md))
- **Security** — The external link check now refuses private, loopback and other internal addresses, and the security lint covers every shipped script. ([SECURITY.md](SECURITY.md))
- **Security** — Templates are now defended as agent-executed instructions: scaffolding refuses to write through symlinks or outside the target, releases carry a derived install manifest, and a content scanner flags suspicious text for human review. ([PROVENANCE.md](bootstrap/PROVENANCE.md))

### Minor changes

- **Added** — Doctrine gains the signal-now, benefit-later principle for coordination and a note that the claim checker cannot verify runtime-behavior claims. ([coordination](doctrine/coordination.md))
- **Added** — Cairn now checks links and claimed paths across its own Markdown with `scripts/check_cairn.py`. ([check_cairn.py](scripts/check_cairn.py))
- **Changed** — Inserting a claim-check marker next to a path is now allowed as mechanical maintenance, even in another agent's review section. ([lifecycle](doctrine/lifecycle.md))

## 0.1.1 — 2026-05-21

### Major changes

- **Added** — Nine doctrine updates ported from an adopter: a required-signal-read mode and collision log for coordination, a rewrite-from-scratch next-session plan, a capability-floor rule for roles, and a new `model-selection` module. ([coordination](doctrine/coordination.md), [model-selection](templates/modules/team-gated/model-selection.md))

## 0.1.0 — 2026-05-20

### Major changes

- **Added** — Initial public release.
