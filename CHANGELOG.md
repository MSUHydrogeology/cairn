<!-- A release history necessarily names files as they were at each version; a
     path that later stopped existing does not make the entry wrong. -->

# Changelog

**Written in [Cairn Plain Language 1.0](docs/plain-language.md).**

Notable changes to Cairn, newest first. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

**Adding an entry.** Each change adds one entry under `## Unreleased`, in the
same commit or the next.

- **Group it.** Put it under **Major changes** if an adopter would notice it or
  must act on it: a new capability, a change to how they work or what the tools
  do, a security fix, or a removal. Everything else goes under **Minor changes**,
  including changes to Cairn's own release and ceremony tools, which adopters
  do not run.
- **Type it first.** Start with one of **Added**, **Changed**,
  **Deprecated**, **Removed**, **Fixed** or **Security**. Keep each group in
  that order, as Keep a Changelog does.
- **Title major changes.** A major entry adds a short title after its type,
  in one bold run: `**Added: Changelog template.**`, then the sentence. Use two
  to five plain words, in sentence case. A minor entry has no title: its type,
  then ` — `.
- **Write it plainly.** Use one or two short sentences, one idea each, saying
  what changed for the reader, and define any Cairn term they may not know.
  The 17 rules are in `dev/agent_collaboration.md`.
- **Link the record.** End with a link to the plan or proposal. Review,
  certification and ceremony status stay there.

At a release, rename `Unreleased` to the version and date, and open a new empty
`Unreleased` above it.

## Unreleased

### Major changes

- **Changed: Achievable implementation plans.** Existing proposal and plan guidance starts from useful, independently finishable outcomes, observable completion, available capabilities and realistic work windows, while preserving queued scope and separate human-operation waits without splitting work by default. ([plan](dev/plans/archive/2026-11-05-smart-goals.md))
- **Added: Advisory next-work selection.** The board can name the next owner and minimum tier from recorded lifecycle evidence, with strict claim checks when available. Generated commit hooks can print the advisory, and drain guidance keeps agents within their own role and target. This does not grant authority or launch unattended work. ([plan](dev/plans/2026-11-05-agent-continuation.md))
- **Changed: Cairn-local execution retries.** Correctable execution errors may receive two feedback-driven same-tier retries before escalation; capability, review, safety and authority limits remain. Adopter templates and broader doctrine are unchanged pending issue #51's full implementation. ([board](dev/PLANNING.md))
- **Changed: Architecture guidance.** The optional rubric now covers legacy, new and mixed systems, names safety-helper homes, and keeps a release assessment in the existing record. Narrow owner-name checks preserve documented standalone copies rather than banning duplication. ([plan](dev/plans/2026-11-05-architecture-and-reuse.md))
- **Added: Public JUnit pulse.** Gauge can summarize explicitly supplied JUnit reports without using Git, and distinguishes testcase phase seconds from testsuite session seconds. Missing tool usage and run comparability remain unknown. ([plan](dev/plans/2026-11-04-metered-cost.md))
- **Added: Optional code map.** The selected architecture-review module provides a bounded filesystem map and advisory function-similarity leads. Secure filesystem scanning remains incomplete on Windows. ([plan](dev/plans/2026-11-05-architecture-and-reuse.md))
- **Changed: Implementation plan completion.** Plans finish after agent-owned scope, reviews and applicable checks are complete. Human trust and release operations remain separate, evidence-backed board waits; archive does not grant permission to activate or release. ([plan](dev/plans/archive/2026-11-04-implementation-plan-completion.md))
- **Changed: Claims across linked worktrees.** Verified worktrees of one clone share the main checkout's claims log, so installed commit hooks can recognize and release their claims; raw checkout aliases, pointer links, reparse points and other layouts fall back locally with a reason. Claims and standalone pruning keep raw caller checks separate from trusted code loading and use the same local fallback. Shared appends refuse a main claims folder removed or linked after import instead of creating it again. Real-hook tests cover absolute and relative pointers on Windows as well as other platforms. Pruning uses recorded time-zone offsets for claim ages and refuses when a concurrent append changes the snapshot. Session-end skips claim pruning outside a main checkout, while separate clones, older tools and typed-event logs remain separate. Session output tests exercise pruning from a main checkout. ([plan](dev/plans/archive/2026-11-04-shared-claims-across-worktrees.md))
- **Changed: Leaner review records.** Reviews retain their three evidenced answers but drop repeated metadata, and word targets count reviewer text rather than the template. Revised proposals and plans grow only to address accepted findings, without a separate trimming pass. ([proposal](dev/proposals/archive/2026-11-03-claude-leaner-reviews.md))
- **Security: Review instruction changes at merge.** Pull-request mergers use their own trusted scanner and read changes for altered behavior or authority, discussing new acceptance markers and concerning outcomes before merging. The step applies at merge, not before pushes or on every commit. ([proposal](dev/proposals/2026-11-03-claude-pr-merge-instruction-check.md))

### Minor changes

- **Changed** — Re-anchor tests reuse pristine setup while keeping each case's Git refs and public signing key separate. The complete test file ran 8-15 seconds faster across two measured orderings. ([plan](dev/plans/2026-11-04-suite-consolidation.md))
- **Changed** — One ordinary CLI test moved to its unit-tier home, with its checks preserved. ([plan](dev/plans/2026-11-04-suite-consolidation.md))
- **Changed** — Ordinary merge and Cairn-prefix tests moved to their existing unit and contract tiers, with their checks preserved. ([plan](dev/plans/2026-11-04-suite-consolidation.md))
- **Changed** — Ordinary certification and verification-boundary tests moved to the existing contract tier, with their checks preserved. ([plan](dev/plans/2026-11-04-suite-consolidation.md))
- **Changed** — Ordinary comprehension and stewardship tests moved to the existing contract tier, with their checks preserved. ([plan](dev/plans/2026-11-04-suite-consolidation.md))
- **Changed** — Four ordinary shipped-policy tests moved to the existing contract tier, preserving their 129 checks. ([plan](dev/plans/2026-11-04-suite-consolidation.md))
- **Changed** — Eight ordinary repository-checker tests moved to the integration tier, preserving their 118 checks. ([plan](dev/plans/2026-11-04-suite-consolidation.md))
- **Fixed** -- Architecture-review installation checks include the code map and its manifest row when counting shipped files. ([plan](dev/plans/2026-11-05-architecture-and-reuse.md))
- **Changed** -- Security Review keeps its normal two-pass limit; each further pass needs a fresh, scoped Maintainer authorization grounded in a specific unresolved question or changed material. ([plan](dev/plans/archive/2026-11-04-security-review-pass-limit.md))
- **Changed** -- Testing guidance now contrasts independently checked scientific inputs with misleading closure and truthiness passes, and offers optional property exploration and observable-criteria prompts. The scientific example also checks two independently specified synthetic input values after residual calculation; the installed-module guard matches the guidance's capitalization. Both module copies name the optional dual-language guidance without a location-dependent link. ([plan](dev/plans/archive/2026-11-04-fault-centered-testing.md))
- **Changed** -- Seven ordinary ceremony checks now share one immutable observation from a real scratch signing ceremony; their existing assertions and negative controls remain. ([plan](dev/plans/2026-11-04-suite-consolidation.md))
- **Fixed** -- When a governing-file selection exceeds its reader limit, tests directly selected by another changed path or import are retained; governing-only readers still follow the passage filter. ([plan](dev/plans/2026-11-04-suite-consolidation.md))
- **Added** -- The v0.7 delivery sequence links accepted proposals for suite consolidation, fault-centered testing and architecture/reuse, with grouped strategy closeout. Reviews and author responses are recorded; implementation planning is next. ([sequence](dev/strategy/2026-11-02-codex-v07-delivery-sequence.md))
- **Added** -- The v0.7 board carries the deferred strict release security run, including duplicate whole-suite invocations and platform-specific skip handling. The historical incomplete run remains distinct from focused Windows evidence. ([board](dev/PLANNING.md))
- **Changed** -- Development now includes the released v0.6.0 baseline and DOI, while accepted v0.7 work and the deferred security run remain on the development board. ([board](dev/PLANNING.md))
- **Changed** -- The v0.7 handoff records accepted work, completed release synchronization and the remaining verification and strategy-retirement tasks. ([board](dev/PLANNING.md))
- **Fixed** -- A trust-check test accepts an already-current generated manifest during setup and still runs its existing security assertions. ([plan](dev/plans/2026-11-04-suite-consolidation.md))
- **Fixed** -- The range-report check compares files against the active protected-test roster instead of the older policy that froze every test. The protection policy and trust records are unchanged. ([plan](dev/plans/2026-11-05-architecture-and-reuse.md))

## 0.6.1 — 2026-11-03

### Major changes

- **Fixed: Editable project history.** The root changelog is tracked for upgrades but no longer hash-attested. Normal install, apply and collision adoption mark it as project-owned living state; ordinary release notes need no repeated finalization. Executable and governing files retain integrity checks. ([plan](dev/plans/archive/2026-11-03-v061-upgrade-repairs.md))
- **Fixed: Windows upgrade compatibility.** Filesystem path comparisons use forward slashes without relaxing manifest validation. Reports escape names unsupported by legacy consoles. Generated text uses UTF-8/LF and verbatim files keep their exact bytes, so Windows newline conversion no longer prevents a clean install lockfile. ([plan](dev/plans/archive/2026-11-03-v061-upgrade-repairs.md))
- **Fixed: Current governing references.** Shipped tools and templates cite current governing sections. References no longer imply that removed stem-only or scheduled rule-rewriting requirements still apply. ([plan](dev/plans/archive/2026-11-03-v061-upgrade-repairs.md))

### Minor changes

- **Fixed** -- Cairn's own gate pre-flight now consumes the protected-test policy recorded in its signed baseline. Its tests exercise the committed default and an explicit legacy-policy fixture. ([plan](dev/plans/archive/2026-11-03-baseline-checker-alignment.md))

## 0.6.0 — 2026-11-02

### Major changes

- **Added: Changelog template.** Every new Cairn install includes a root changelog with Major and Minor sections, ordered entry types, titled major entries, and guidance for keeping, optionally adapting, or saving existing history before starting fresh. Normal install preserves an existing file; upgrades stage new changelog collisions for review. ([plan](dev/plans/archive/2026-11-01-changelog-template.md))
- **Added: Module list and first-use tasks.** Each install now lists the modules you chose, with optional first-use tasks for each. You can adopt a module later, and install keeps your existing work when it conflicts. ([plan](dev/plans/archive/2026-10-29-module-discovery-activation.md))
- **Changed: Quickstart lifecycle.** The quickstart now shows its deliberate tagline example as light and records the final check before a separate archive commit. ([plan](dev/plans/archive/2026-11-02-quickstart-lifecycle-alignment.md))
- **Changed: Scoped certification defaults.** Guidance helps teams choose checks for affected work and record its scope and omissions, while required checks and Cairn's full-tree certification remain in force. ([plan](dev/plans/archive/2026-11-01-project-certification.md))
- **Changed: Security Review triggers.** Guidance explains when reuse through unchanged safeguards does not add a trust boundary and preserves review for new sources, bypasses, wider inputs and exposed outputs. ([plan](dev/plans/archive/2026-11-01-security-trigger-clarity.md))
- **Changed: Scientific model evidence.** Guidance places model runs with the work or release that requires them while retaining configured suite members and all other required checks. ([plan](dev/plans/archive/2026-11-01-model-evidence.md))
- **Changed: Lifecycle descriptions.** The README, diagram, Quickstart, release guidance and published method now show that light proposals have no plan and keep proposal tiers distinct from the outer change lanes. ([plan](dev/plans/archive/2026-11-01-lifecycle-description.md))
- **Changed: Decision options.** Guidance asks agents to show meaningful costs and losses for material choices, name a credible simpler option, and separate the recommendation. ([plan](dev/plans/archive/2026-11-01-decision-options.md))
- **Changed: Focused testing example.** The shipped plan example points to tests for changed files and retains required integration and security checks. ([plan](dev/plans/archive/2026-11-01-focused-testing-example.md))
- **Changed: New board layout.** New installs now get a work board that puts Maintainer waits first, uses release tables for Work, Next step and Record, and includes short terms and agent working rules. Existing project boards and their local content remain under their owners' control. ([plan](dev/plans/archive/2026-11-01-shipped-board-layout.md))
- **Changed: Less paperwork in templates.** Plans and proposals carry less paperwork: the templates repeat less text, and a plan needs no evidence folder unless the work requires one. Lifecycle, security and verification obligations are unchanged. ([template plan](dev/plans/archive/2026-11-01-template-burden.md), [evidence plan](dev/plans/archive/2026-10-30-plan-evidence.md))
- **Changed: Decision summary in proposals.** Proposal templates now prompt a brief summary of the issue, proposed change and meaningful tradeoff before supporting detail; short proposals can stay short. ([plan](dev/plans/archive/2026-11-01-proposal-decision-summary.md))
- **Changed: One whole-project check record.** When Cairn checks the whole project for a release or another authorized purpose, it records the result once. Individual changes no longer need a separate “pending” note; the required checks and when to run them are unchanged. ([plan](dev/plans/archive/2026-11-01-certification-marker.md))
- **Changed: Tests that name the change.** During a change, agents run only the tests that name the changed files, and run the final integration check once, after review. When a governing file such as `AGENTS.md` has more than 40 reading tests, only those pinning the changed passages run, and the rest are listed as omitted. ([proposal](dev/proposals/archive/2026-10-30-claude-test-once-per-change.md))
- **Changed: Module list in upgrade review copies.** Upgrade review copies now show your recorded module list in the upstream `.theirs` copy and keep your own bytes in `.ours`. Install, module adoption and staging refuse an ambiguous or malformed module-list marker before changing anything. ([rendering plan](dev/plans/archive/2026-10-30-review-inventory-rendering.md), [marker plan](dev/plans/archive/2026-10-30-module-marker-ambiguity.md))
- **Changed: Lighter review.** Review is one bounded pass per stage, light is the default proposal tier, added or widened trust boundaries still get a Security Review, and governing instructions are shorter. ([plan](dev/plans/archive/2026-10-30-cut-the-apparatus.md))
- **Changed: Handoff preparation.** `session-end --prepare-handoff` writes your reflection, lists open threads and work claims, and shows a preview before giving you the guarded prune command. ([plan](dev/plans/archive/2026-10-30-handoff-preparation.md))
- **Changed: Scoped change verification.** Each change is verified by the tests mapped to it, and certifying the whole tree is a separate release step. Plan, proposal and strategy file names now start with their opening date. ([plan](dev/plans/archive/2026-10-28-scoped-change-verification.md); [verification doctrine](docs/methodology/plans.md))
- **Changed: Model tier by task.** The lowest model tier allowed for a job now depends on the task: medium for ordinary writing and reviews, low for carrying out an accepted, reviewed plan. Cairn's own model mapping lists three model families per tier. ([plan](dev/plans/archive/2026-10-28-model-floor-alignment.md); [roles](docs/methodology/roles.md))
- **Changed: Published methodology moves to docs.** Cairn's published methodology now lives in `docs/methodology/`; `doctrine/` is removed. Installed guidance keeps its operative duties and points to the published material for context. ([plan](dev/plans/archive/2026-11-01-retire-doctrine.md))
- **Security: Safer security dispatcher.** The local security dispatcher, which runs your installed security checks, now includes the content-security scan and gives API checks only the credentials its validated local policy names. It refuses substituted code and reports unreliable or flagged results instead of claiming clean. ([scan plan](dev/plans/archive/2026-10-29-dispatcher-content-scan.md), [credentials plan](dev/plans/archive/2026-10-30-api-dispatch-credentials.md))
- **Security: Saved-copy checks before merging.** Upgrade checks the saved earlier version of each file before merging, keeps damaged copies through repeated manual recovery, refuses specified invisible characters in paths, and escapes install names in reports. The check catches local records that disagree, but cannot detect a cache and lockfile edited together. ([plan](dev/plans/archive/2026-10-30-upgrade-install-integrity.md))
- **Security: Nested Git data and planted links.** Upgrade refuses project paths that lead into nested Git data, and `upgrade --init-lock` refuses a planted link at any mapped installed path before reading it. Hard-link aliases and changes made after a check are not covered. ([nested Git plan](dev/plans/archive/2026-10-30-nested-git-upgrade.md), [init-lock plan](dev/plans/archive/2026-10-30-init-lock-linked-files.md))
- **Security: Folders at tracked file paths.** Upgrade now treats folders occupying tracked file paths as hard blocks during planning, staging and application. It preserves their contents and requires resolution followed by a fresh stage before applying. ([plan](dev/plans/archive/2026-10-30-upgrade-directory-collisions.md))

### Minor changes

- **Added** — Cairn can prepare a forward AST correction with a guided, independently reviewed workflow without reconstructing old history. ([plan](dev/plans/archive/2026-11-02-forward-ast-preparation.md))

- **Added** — Release publication has a read-only check for the published Release and the signed tag's remote commit, and the guide now separates pushing the signed tag from publishing its Release. ([plan](dev/plans/archive/2026-10-30-tag-release-distinction.md))
- **Added** — Cairn's re-anchor and repin ceremonies, which re-approve the files its test gate protects, have reusable preparation, verification and supervised-run commands. Preparing the new trust baseline uses independently reviewed inputs. ([commands plan](dev/plans/archive/2026-10-29-ceremony-commands.md), [baseline plan](dev/plans/archive/2026-10-29-forward-trust-baseline.md))
- **Added** — Cairn now separates its protected security and trust tests from ordinary tests. A signed list names the protected ones, and changes to them are checked in two stages. ([plan](dev/plans/archive/2026-10-28-test-trust-boundary.md))
- **Changed** — Cairn’s output-bound security test checks the byte cap separately from cleanup success and reaps its probe if cleanup fails; the security runner is unchanged. ([plan](dev/plans/archive/2026-11-02-output-bound-test.md))
- **Changed** — The roadmap keeps engineering improvements, suite consolidation, cost measurement and the selected cleanup in v0.7, with organized adopter feedback and workflow expansion assigned to v0.8. All candidate work and its source records remain on the [board](dev/PLANNING.md).
- **Changed** — The scaffold security inventory no longer carries the obsolete `(R5)` review marker on its core destination safeguard. ([plan](dev/plans/archive/2026-11-02-stray-finding-id.md))
- **Changed** — The upgrade guide now asks you to compare a clean staged merge with the upstream change and your local policy. A clean text merge alone does not show that their rules agree. ([proposal](dev/proposals/archive/2026-11-01-codex-upgrade-merge-warning.md))
- **Changed** — Cairn's documentation and shipped guidance were reviewed for clear language while preserving their instructions and technical meaning. Shipped templates carry the Plain Language marker. ([plan](dev/plans/archive/2026-11-01-plain-language-docs.md))
- **Changed** — The changelog is reorganized: each release lists Major and Minor changes. Each entry starts with its Keep a Changelog type, and each major entry adds a short title. All entries back to 0.1.0 are rewritten in Cairn Plain Language, in one or two sentences with a link to their record.
- **Changed** — Review guidance and shipped templates now keep repeatable checks in tests and scripts, and mapped tests catch the removed review-record requirement coming back. ([plan](dev/plans/archive/2026-10-30-probe-ledgers.md))
- **Changed** — Shuffled review-sweep tests reuse each profile install for the pytest session, cutting measured setup from 31.26s to under 1s. ([plan](dev/plans/archive/2026-10-30-certification-cost-audit.md))
- **Changed** — Coordination guidance is clearer: commits to shared files need agreed serialization and inspection, and the work-intent guidance and CLI help say when a claim blocks, what is exempt and the limits of identity. ([sweeps plan](dev/plans/archive/2026-10-30-same-file-sweeps.md), [intent plan](dev/plans/archive/2026-10-30-intent-guidance.md))
- **Changed** — The clean environment for release evidence now allows only one pytest setting, the one that turns off its cache, and removes it afterwards. ([plan](dev/plans/archive/2026-10-29-release-evidence-environment.md))
- **Changed** — The board's JSON tests share one helper for capturing archive output, and the shipped module and Cairn's copy gain matching test-maintenance guidance. ([plan](dev/plans/archive/2026-10-28-ordinary-test-maintenance.md))
- **Changed** — A survey of governing text chose where public explanations of the methodology live, and the accepted-scope part of the plan template drops repeated reasoning. ([plan](dev/plans/archive/2026-10-28-governing-text-single-source.md))
- **Fixed** — Cairn's certification tests were repaired: the dispatcher fixtures and archived baseline path are fixed, and the real ceremony start-up runs isolated while the adversarial checks stay. ([plan](dev/plans/archive/2026-10-30-certification-test-repairs.md))
- **Fixed** — Cairn's own release tests suppress child bytecode, keep the manifest row count aligned with the accepted changelog mapping, and set the scratch Git branch explicitly. ([plan](dev/plans/archive/2026-11-02-release-test-corrections.md))

## 0.5.0 — 2026-10-28

### Major changes

- **Added: Cairn Plain Language.** Cairn Plain Language 1.0 is a 17-rule writing standard for everything agents write for people. Every install carries it in `dev/agent_collaboration.md`, and `docs/plain-language.md` is a full adoption page with the copyable rules, an evidence table and a 30-source bibliography. ([proposal](dev/proposals/archive/2026-10-27-antigravity-plain-language-adoption-docs.md), [rationale](docs/methodology/rationale.md))
- **Added: Removing retired files.** `upgrade --remove-retired` removes a project's untouched copies of files Cairn stopped shipping, and keeps and names any copy that differs, is untracked or sits behind a link. ([plan](dev/plans/archive/upgrade-removes-retired-files.md))
- **Added: Drain mode.** Drain mode: `/session-start --drain [board | issues | <item>]` works the queue. It sorts open items by lifecycle lane, fixes trivial ones with a failing test, has a fresh session review each fix, and commits locally without posting to GitHub. ([plan](dev/plans/archive/drain-mode.md))
- **Changed: Local next-session note.** The next-session handoff is a local, untracked note at `dev/reflections/next-session.md` instead of a shipped `dev/NEXT_SESSION.md`. It is read as a hint, never as instructions, and counts as absent after 14 days. ([plan](dev/plans/archive/next-session-local-note.md))
- **Changed: New-slot reporting.** The install report lists slots that only an uninstalled module fills apart from the main list, and `upgrade --plan` and `--stage` print a `[new slot]` line for slots a new template adds. ([plan](dev/plans/archive/engine-batch-f8-slots.md))
- **Changed: Model tier for every job.** Every install now states which model tier a job needs. The work's lifecycle lane sets the lowest tier allowed to write it, Security Review stays at the high tier, and a stronger model from the same maker counts as an independent check.
- **Changed: Lighter trivial lane.** A trivial change needs no plan and no code review, provided it stays one commit and one area and its final test run would cover only the tests that name it. ([plan](dev/plans/archive/no-plan-changes-end-to-end.md))
- **Removed: Onboarding prompts retired.** The delayed onboarding prompts, a goodnight helper that never ran, its activation log and eight support files are gone. Their content now lives in the day-one task list, so new installs have nine fewer files and an install report about ten lines shorter. ([plan](dev/plans/archive/install-time-onboarding.md))
- **Security: No project programs during upgrade.** `upgrade` no longer runs programs named in a project's git settings (file-system monitor, clean filter, text converter, hook) when it checks for unsaved edits, and it reads projects in a subfolder of a larger repository correctly. ([plan](dev/plans/archive/upgrade-edit-check-no-repository-programs.md))
- **Security: Linked profile refused.** `upgrade --plan`, `--stage`, `--adopt-module`, `--adopt-collisions` and `--init-lock` stop with exit 2 when `dev/.cairn/profile.yml` is a link, instead of reading what it points to. `--init-lock` also stops when `dev/.cairn` is a link, and `--finalize` names a linked vendor wrapper and says to replace it. ([upgrade guide](bootstrap/UPGRADE.md))
- **Security: No writes through linked files.** `upgrade --apply` no longer writes outside the project through a linked profile. It also refuses a linked lockfile, option-like saved commit names, control characters in module and review-area names, a linked vendor wrapper, and records naming files inside `.git/`. Four older findings remain open. ([review](dev/plans/archive/2026-10-19-security-review-upgrade-lockfile-paths.md))
- **Security: Safer session start.** `session-start` no longer runs a program inside the project that git tracks, finds the interpreter binding file (which names the project's Python) on case-insensitive disks, refuses a bad binding plainly, and encodes project-supplied text in seven more places. Output from programs it starts is still printed unencoded. ([review](dev/plans/archive/2026-10-18-security-review-session-writes.md))

### Minor changes

- **Added** — `scripts/repin.py` runs Cairn's routine re-pins of its test gate in three commands, `status`, `package` and `ceremony`, which stop before the Maintainer types the signing passphrase and never read it. ([plan](dev/plans/archive/repin-build.md))
- **Changed** — The plan and proposal templates add "Keep the plan short" and "Keep the proposal short" sections saying what stays out of the file. ([issue #31](https://github.com/MSUHydrogeology/cairn/issues/31))
- **Changed** — Cairn's re-anchor ceremony needs no outside reviewer: the Maintainer compares digests, runs a few checks, reads a plain report and approves. The old manual path (`drive()`, `--run`, the digest-correcting script) is gone. ([plan](dev/plans/archive/ceremony-without-external-review.md))
- **Fixed** — `upgrade --finalize` on a kept, edited fold-back ledger from an old install now leaves a tree that `verify_integrity` accepts.
- **Fixed** — `link_check.py`, `sync_doc_snippets.py` and `check_cairn.py` skip a tracked Markdown file deleted from disk but not yet committed, instead of crashing. ([proposal](dev/proposals/archive/2026-10-26-claude-check-cairn-deleted-files.md))
- **Fixed** — The board and `session-start` now name an active proposal or plan with a retired or unknown status in one advisory line. ([#32](https://github.com/MSUHydrogeology/cairn/issues/32))
- **Security** — Cairn's re-anchor ceremony now protects its launcher template as the eleventh checked file. The runbook no longer claims that handing over the launcher separately adds assurance, and checking that the launcher matches the template is still manual. ([plan](dev/plans/archive/repin-ceremony-hardening.md))

## 0.4.0 — 2026-10-20

### Major changes

- **Added: Cheap defect fixes and reuse.** Agents may fix cheap defects that break promises already documented in a file, must give one of three reasons to defer work, and must search for reusable code before adding new. ([plan](dev/plans/archive/stewardship-and-reuse.md))
- **Added: Unfilled model mapping notice.** Non-interactive installs, module adoption and upgrades now emit a notice when the model selection mapping is unfilled. ([plan](dev/plans/archive/model-mapping-install-path.md))
- **Added: Board data and Maintainer list.** `python tools/board.py --json` prints every proposal and plan as plain data (contract `cairn-board/1`), `--maintainer` lists everything waiting on the Maintainer, and the templates prompt for an `In brief` line the board reads. ([plan](dev/plans/archive/board-as-basis.md), [guide](docs/build-a-board-view.md))
- **Added: Independent scientific check.** The proposal template now asks for one independent scientific check when a change touches a scientific result, and the plan template makes that check accepted scope that only the Maintainer can drop.
- **Added: Unfilled slot advisory.** `verify_integrity.py` now prints an advisory listing slots that still hold Cairn's placeholder, with a coverage line saying what it could not check.
- **Added: Upgrading a hand-copied install.** A project that copied Cairn's core files by hand now has a documented way to start upgrading: run `scaffold.py upgrade --target <repo> --init-lock`, fill four placeholders, then run it again.
- **Added: Scope reduction judged against acceptance.** Narrowing accepted work is now judged against the plan or proposal as opened or accepted. A result that delivers less needs a `Scope delta` and the Maintainer's explicit allowance.
- **Added: Local security dispatcher.** Choosing a security capability now installs a local dispatcher that runs your security checks. It can only narrow what a check may do, and its list of checks ships empty.
- **Added: Network security modules.** Three opt-in security modules: `api-access-security` and `web-hosting-security` check a declared authorization matrix and HTTP/TLS settings, with agents limited to the local machine, and `portable-security-sweeps` runs a Gitleaks adapter you provide and reports `INCOMPLETE` without it.
- **Added: Security preflight questions.** The proposal template gains a gated "Security preflight" block of five questions a security-touching change must answer before review.
- **Added: Release tag verification guide.** `bootstrap/PROVENANCE.md` explains how to verify a release's signed tag with plain `git`, independently of Cairn's own tools, plus key rotation and its limits.
- **Changed: Shared review questions.** Every review now answers the same evidence questions. The installed review guide holds the nine lenses and the falsification ledger (a record of attempts to prove the change wrong), and an outside review happens only when the Maintainer calls for one. ([plan](dev/plans/archive/review-stance-and-lenses.md), [upgrade guide](bootstrap/UPGRADE.md))
- **Changed: Integrity check after upgrade.** After `--apply`, upgrade now has you run `python bootstrap/verify_integrity.py --target <repo>`, and a filled slot is recorded with `upgrade --finalize <path>`.
- **Changed: Board rows for unopened plans.** Work handed to a plan that is not yet open must become a board row, since a pointer to an archived file is not a home.
- **Changed: Reviews read commits.** A review reads a commit, never a shared working tree, and tests an "every place" claim by changing each member of the set to see whether a test catches it.
- **Changed: Tests recorded for small fixes.** A small fix with no plan now runs the tests that own what it touched and records them in its commit body.
- **Changed: Metrics schema version 2.** `lifecycle-metrics` moves to schema v2. Its fields now come from structured event blocks (`cairn-event-v1`) in the records, and a `schema_version` column tells v2 snapshots from v1.
- **Changed: Plan review after an External proposal review.** When an outside (External) proposal review records `Plan readiness: READY`, the plan can be reviewed by a fresh internal reviewer instead of a second outside one.
- **Changed: Board-first session start.** Session-start orientation now routes through `python tools/lifecycle_planner.py board --compact` instead of opening every active record.
- **Changed: Fewer false look-alike flags.** The homoglyph detector now asks whether characters are confusable, so scientific Greek notation stays clear while Latin/non-Latin lookalikes are still flagged.
- **Changed: Content scanning by default.** New installs now include content scanning by default (`content-security`, with a `modules_remove` opt-out), and `python-security` is added for declared Python projects.
- **Removed: Collaboration agreement retired.** The collaboration agreement is no longer installed in new projects. Existing copies stay, and `upgrade --plan` reports it as `removed-upstream`. ([plan](dev/plans/archive/remove-collaboration-agreement.md), [upgrade guide](bootstrap/UPGRADE.md))
- **Removed: Adoption levels retired.** Adoption levels are retired, along with the onboarding helper's level classification and its "Level 1→2 graduation" prompt. To adopt Cairn, read the doctrine or install it with the scaffold and a profile.
- **Removed: Metrics columns removed.** Eight review-prose-derived columns of `lifecycle-metrics` and the `--backfill-from` option are removed.
- **Fixed: Modified launcher advisory.** The advisory for a modified `scaffold.py` launcher (a forked facade) compares against trusted upstream bytes, names what it compared against, and advises only restoring the launcher from upstream.
- **Fixed: Dependency audit coverage.** The Python dependency audit now proves what it covered and reports CLEAN only with zero unknown dependencies and zero findings.
- **Fixed: Test citations in claim checks.** `claim_check` now accepts the `path::node` citation form that doctrine requires, resolving it on its path half.
- **Fixed: Metrics read real commits.** The `lifecycle-metrics` commit-stage vocabulary now reads real commit subjects, so interval columns fill and timestamp reliability is no longer almost always `Best-effort`.
- **Fixed: Fewer hook warnings for humans.** The intent post-commit hook no longer warns about unconfigured agent identity on human commits that have no live claims.
- **Security: Safer model mapping check.** The model-selection check now skips comment lines, parses YAML values safely, and refuses merge-key recursion attacks. ([plan](dev/plans/archive/model-mapping-install-path.md))
- **Security: Atomic installer writes.** Installer writes (interactive capture, `.gitignore` seeding, lockfiles) are now atomic and cannot be redirected through symlinks, hardlinks or racing temp files, and the lockfile reader refuses non-regular files. ([plan](dev/plans/archive/model-mapping-install-path.md))
- **Security: Board skips links.** The board now skips symbolic links and refuses non-regular files instead of hanging, so a `dev/` folder kept as a symlink reads as empty after upgrading. ([plan](dev/plans/archive/board-as-basis.md))
- **Security: Escaped report text.** The integrity report and the lifecycle orientation output escape text from the lockfile and repository, so a crafted file name or status cannot inject control characters or forge lines.
- **Security: Invisible Unicode and strict URLs.** Content scanning flags invisible Unicode (ignorable characters, Tag characters, line separators) and checks URLs strictly outside `dev/**` and `docs/**`, which it reads as discussion. Lines with emoji variation selectors may gain findings after upgrading.
- **Security: Exact tag signature check.** `verify-ref.sh` now checks the signature of the exact tag you asked about, so a ref re-pointed at another signed tag is refused. An unsigned pin needs `--unprovenanced` and exits 3.
- **Security: Look-alike Maintainer names refused.** A byline with a look-alike character can no longer pass as a human Maintainer, so `human_maintainers` entries must now be the full display name, spelled with ASCII spaces.

### Minor changes

- **Added** — `docs/build-a-board-view.md` documents the board data schema and its contract promises with a standard-library example (published in Cairn's docs, not installed). ([plan](dev/plans/archive/board-as-basis.md), [guide](docs/build-a-board-view.md))
- **Added** — Cairn's test suite now records its own cost in a gitignored ledger that `tools/suite_cost.py` renders without running anything.
- **Added** — `bootstrap/tests/_gate_preflight.py` runs the checks before a supervised re-anchor and advances the branch and the anchor together in one step.
- **Changed** — The doc-drift module now names a third kind of drift: prose that names a function the code no longer has.
- **Changed** — Code review is no longer described as External by default; External is an escalation for risk the proposal review did not resolve.
- **Changed** — The solo-legacy recipe now installs with the scaffold, with its roster corrected to the eight modules it installs.
- **Changed** — Doctrine now states that a proposal Response always carries one complete current contract, matching what the conformance check already enforces.
- **Changed** — The authoring templates now show how to register an exact path once, with its type, when a document cites it repeatedly.
- **Changed** — `python bootstrap/security_check.py` now covers Cairn's complete local release security bar in one Maintainer-run command.
- **Changed** — Approval for a Cairn re-anchor ceremony is now a Maintainer-signed checkpoint tied to a report on the commits under review, and unsigned commits in between no longer stop the ceremony.
- **Fixed** — Three sentences in the complexity dimension, its README and the bootstrap guide no longer promise a review lens that no module installs.
- **Fixed** — `python scripts/quality_gate.py --sub neutrality` now reads `fail=0`: every shipped vendor-name leak was reworded and the check slightly tightened.
- **Fixed** — `upgrade --init-lock` no longer recommends a re-install, which over an existing tree writes no lockfile.
- **Fixed** — Object-id widths are now read from the repository's object format, so a SHA-256 repository is no longer refused on the public path.
- **Fixed** — Unicode findings now carry their literal pattern id instead of inferring it from message prose.
- **Fixed** — The release Bandit gate now scans every Python file the installer ships and fails closed when Bandit cannot open a file.
- **Fixed** — `check_cairn` no longer hard-fails on `dev/` paths cited across Cairn's own doctrine, templates and changelog when self-hosted.
- **Fixed** — The `v0.3.0` release commit's quality-gate attestation is corrected; it had claimed a clean run that did not reproduce.
- **Security** — `bootstrap/security_check.py` takes object ids from Git itself and refuses a folder that is not a repository instead of falling back to SHA-1. It checks object integrity in a clean context the checked repository cannot configure, so its own `fsck.skipList` cannot hide a corrupt object.

## 0.3.0 — 2026-06-12

### Major changes

- **Added: Model bindings at install.** `scaffold install` now asks for your tier-to-model bindings when you choose the `model-selection` module, so its check passes from the start. Non-interactive installs keep the `FILL ME` placeholder.
- **Added: Link check skips code spans.** `link_check` now ignores links inside balanced inline code spans and honors a file-level `<!-- link-check-allow: ... -->` directive, matching `claim_check`.
- **Added: New files of adopted modules.** `upgrade` carries new files of modules you already adopted, and `--apply` fails closed if a new file's destination appeared after `--stage`. `--adopt-collisions` keeps a customized file that collides with a new upstream file as a tracked fork instead of blocking.
- **Added: Launcher tracked and scanned.** The onboarding launcher and its engine are now tracked in the lockfile and covered by the release security scan, and a new core file landing on an occupied untracked path is a hard block rather than an overwrite.
- **Added: Container recipe.** A container recipe under `bootstrap/container/` lets a team with no host Python run the install and upgrade engine in a throwaway container.
- **Added: Lifecycle contract and planner.** A written contract now lists the lifecycle's states and allowed moves. The read-only `tools/lifecycle_planner.py` (`next`, `scan`, `guard`) reports a proposal or plan's state and any unmet conditions without changing anything.
- **Added: Standard-library security stack.** A standard-library-only security stack: `content-security` gains a fail-closed self-audit runner, a new opt-in `python-security` module orchestrates bandit, content scan and pip-audit, and install fails early when a selected module's required token is unfilled.
- **Added: Profile-specific sections.** The core `AGENTS.md` template supports `<!-- cairn:if AXIS in ... -->` regions, so a section can appear only for matching profiles. The `Human contributors` section now appears only for multi-person teams.
- **Added: Custom session routines.** The `session-start` and `session-end` skills point to an optional project-owned `dev/rules/custom_session_routines.md`, giving adopters an installable home for their own routine steps.
- **Added: Measurement folder.** A new `dev/measurement/` folder gives every adoption a standard home for its process-health records, and the `lifecycle-metrics` and `incident-trackers` modules now point to it.
- **Added: Nine-lens review sweep.** Reviewers work a 9-lens review sweep with a two-part coverage line, shipped in the `dual-review` module. The proposal and plan templates gain a block, required when triage calls for it, where the author accounts for the review's findings.
- **Added: Always-on load budget.** `scripts/token_budget.py` measures the always-on load against a soft cap, a cache-stable load-order convention is documented, and the core `AGENTS.md` Git-workflow section is about 22% shorter.
- **Added: Model tiers for subagents.** The `model-selection` module gains fan-out guidance: each leaf task takes its tier from its own task, never from the orchestrator, and no downshift crosses a data-governance boundary.
- **Added: Four adopter practices.** Four practices proven in an adopter's project join Cairn: a dual-review case study, the `claim-check` verify-before-asserting typology, a "lead with the domain" line for surfacing judgment calls, and an opt-in signature-log pattern for the collaboration agreement.
- **Added: Finalize for customized installs.** `upgrade --finalize` advances lockfile hashes to the committed on-disk content, so a customized install verifies cleanly. Given paths, it re-records only those files, and without paths it refuses a dirty tree unless you pass `--force`.
- **Added: Fuller proposal and plan templates.** The proposal and plan templates gain the adopter-developed detail on forward-reference markers, archive preconditions, plan triage, plan review and code-review ledgers, plus five new adopter slots.
- **Added: Session skills.** `session-start` and `session-end` are invokable skills (`/good-morning`, `/goodnight`) backed by a standard-library `tools/lifecycle.py`, and `session-start` repairs a missing or stale `.claude/skills` link so adopters set up by lockfile copy get their skills.
- **Added: Architecture review module.** A new opt-in `architecture-review` module gives teams whose architecture accreted rather than was designed a five-lens review frame to fork into `dev/architecture_review.md`.
- **Added: Session identity.** `tools/intent.py whoami` prints the per-session identity, and reflection filenames now reuse that session token so a reflection links to its intent-log entries.
- **Added: Mechanical module merge.** Module install now merges module content into target files mechanically, deferring conflicts to a `.cairn-merge-pending` side-file (`--non-interactive` forces deferral), and catches duplicate slots and wrong-slot pastes.
- **Added: Recovering untracked drafts.** `templates/core/AGENTS.md` gains an "Untracked lifecycle artifacts" section with a cold-start recovery procedure for uncommitted proposal or plan drafts.
- **Added: Documentation plan modules.** Two default-on modules: `documentation-plan` adds a procedure for deciding where a document belongs and a forkable `docs/DOCUMENTATION_PLAN.md`, and `incident-trackers` adds a forkable incident tracker and a goodnight migration step.
- **Added: Progressive onboarding.** Progressive onboarding turns PLANNING into an on-ramp with preset task lists, maturity and action triggers, and at most one active prompt per goodnight, plus new tour docs.
- **Added: Fold-back protocol.** Fold-back now has an active-surfacing protocol with GitHub issue and PR templates, an export-scrub scanner for credentials, private paths and IPs, and a helper that lists candidates ready to file.
- **Added: Quality gate.** `scripts/quality_gate.py` bundles order-independence, vendor-neutrality and redundancy checks into one pre-cut gate (`--sub <name>` to pick one).
- **Added: Claim check exemptions.** `claim_check.py` gains a `claim-check-allow` directive that exempts named paths in one document. It no longer soft-flags numbers next to words like `lines` or `tests`: approximate, date or register a count instead.
- **Added: Adopter starting points.** Seven new starting points for adopters: a quickstart, three profile presets, a bootstrap-lite prompt, a codebase-readiness report template, a scientific-minimal example, a README trust box, and honest-framing callouts.
- **Changed: Recorded dispositions for follow-ups.** Archiving now needs a recorded disposition for each deferred follow-up (`accept`, `wontfix`, `defer`, or the new `guard`), not just a home on the roadmap board. `Dispositions:` replaces `Follow-ups migrated to:`, and old records stay valid.
- **Changed: Upgrade and verify fixes.** Four upgrade and verify fixes: `--adopt-module` notes a local file that a module now supersedes, intent tooling reads `dev/.cairn/intent-config.json` (the old path still works), `check_model_selection.py` checks mapping structure when PyYAML is present, and a forked facade with a dormant installed engine is flagged.
- **Changed: Short templates.** The proposal and plan templates shrink from ~800-line manuals to short form skeletons, with the teaching moved to new `doctrine/proposals.md` and `doctrine/plans.md` pages.
- **Changed: Fuller lifecycle metrics.** The lifecycle-metrics tool gains the adopter fork's measurement features (annotation counts, collision log, review yield, model tier, output manifest) and reads settings from `dev/.cairn/metrics-config.json`. `--snapshot` now writes numbered files under `dev/measurement/snapshots/` instead of overwriting one file per day.
- **Changed: Adoption state in dev/.cairn.** Adoption state moves into `dev/.cairn/`: the lockfile (`cairn-lock.yml`, which existing adopters move), the profile (`profile.yml`) and the fidelity manifest, whose old location still works.
- **Changed: Full profile in init-lock.** `upgrade --init-lock` now captures the full six-axis profile (failing with a template to complete if none is committed), and `upgrade` rebuilds a missing `dev/.cairn/profile.yml` from the lockfile.
- **Changed: Windowless commits.** The windowless commit is now the primary concurrent-session habit: `git commit <paths>` stages and commits in one step, and you verify with `git status --short` and `git diff <paths>` instead of the shared index.
- **Changed: Claim check enforcement.** The work-intent pre-commit check gains an `enforce` setting (`warn`, `confirm`, `block`) and recognizes your own claims by session token, so it warns only about other sessions.
- **Changed: Uncommitted edits protected.** `scaffold.py upgrade --apply` now refuses when it would overwrite a tracked file with uncommitted edits (`--force` overrides), and `--stage` warns instead.
- **Changed: Link check scope.** `link_check` skips `file://` links and by default excludes `dev/modules/` and `dev/.cairn/` (`--include-modules`, `--include-cairn`), and both `link_check` and `check_cairn` skip archived and reflection files unless you pass `--include-archives`.
- **Changed: Living-state files not flagged.** `verify_integrity` no longer flags routine edits to the four adopter-authored living-state files (roadmap, handoff, fold-back ledger, collaboration agreement), while still failing closed if any other file claims that exemption.
- **Changed: Falsification ledger.** A clean code review must now show a four-part falsification ledger (a record of attempts to prove the change wrong) or a second independent pass. The collaboration doctrine names a standard handoff format and a no-cross-attribution review rule, and readiness reports gain a `Status:` field.
- **Changed: Manual merge review.** `upgrade` now lists customized files that need a manual merge, stages a review pair for each, and refuses `--apply` until you pass `--ack-review-only`. `--init-lock` also recognizes a renamed vendor wrapper.
- **Changed: Lifecycle commits without approval.** Plan and strategy lifecycle commits may now proceed without per-commit approval, alongside proposals, with the same push and Decision guard-rails.
- **Changed: Documentation governance.** `doctrine/doc-governance.md` now covers both governing-file routing and the descriptive `docs/` layer, with common homes for vision and style docs and a note that your docs format is your choice.
- **Changed: Clearer upgrade summary.** The `upgrade --plan` and `--stage` summary now separates untouched files from locally modified files that merged cleanly.
- **Fixed: Renamed wrapper not missing.** A renamed vendor wrapper (such as `CLAUDE.md`) no longer triggers a spurious "file missing" `review-only` on every `upgrade`.
- **Security: Safer onboarding helper.** The onboarding-activate helper now refuses to read or write through symlinks or outside the project, and rejects path-traversal in `--preset` names with a security error.

### Minor changes

- **Added** — `_ast_attest.py` gains a hardened `update-symbol` subcommand, and a new `_gate_manifest.py` freezes the gate's protected files, so unattended batches of registry updates are bounded by a mechanism rather than by review.
- **Added** — Cairn-maintainer-only `scripts/verify_counts.py` and `scripts/measurements.py` re-measure registered live counts against `<!-- verify: <key> -->` annotations and are wired into `check_cairn`.
- **Added** — `check_cairn` now fails when an adopter-facing template cites a Cairn-internal `doctrine/*` path that would not exist after install.
- **Added** — Proposal and plan templates now teach the four ways to clear a count-claim soft flag.
- **Added** — Cairn's own smoke tests now cover the profile presets, the quickstart sequence and the scientific-minimal example.
- **Changed** — `doctrine/rationale.md` is regrouped into a Foundation plus four themed clusters, adds four anchors from the reference adopter, and `docs/further-reading.md` gains a verification-and-validation reading slot.
- **Changed** — The test that compares the engine's behavior before and after a refactor now builds its "before" engine from a trusted git ref and runs only during refactors, replacing the checked-in `scaffold_frozen.py` copy.
- **Changed** — The `intent.py` and progressive-onboarding tools are split into thin launchers over owned engine packages (`_intent/`, `_onboarding/`), with public behavior and write-containment guards unchanged.
- **Changed** — `scaffold.py` is now a thin launcher over a private `bootstrap/_scaffold/` package, with the same public commands. Tests that monkeypatch must patch the owning submodule, not the `bootstrap.scaffold` launcher.
- **Fixed** — The forkable incident-log template no longer shows as `needs-value` on every adopter upgrade, because its placeholders now use angle-bracket syntax.

## 0.2.0 — 2026-05-27

### Major changes

- **Added: Content security module.** A new `content-security` module lets adopters scan files and PRs for prompt injection, and `verify_integrity.py` detects post-install file modification against the lockfile.
- **Added: Doc governance and fold-back.** New doc-governance doctrine, reviewer decision-support, a Decision-scribing guard-rail, and a default-on `fold-back-ledger` module for sending improvements back to Cairn. ([doc-governance](docs/methodology/doc-governance.md))
- **Added: Customized-install upgrades.** `scaffold.py upgrade` merges new Cairn doctrine into a customized install without clobbering local edits, using a new `dev/cairn-lock.yml` lockfile. ([UPGRADE](bootstrap/UPGRADE.md))
- **Added: Governance presets.** Three governance presets (`solo-greenfield`, `collaborative-team`, `high-rigor-legacy`) set a baseline module roster, and `scaffold.py --summary` previews the result before installing.
- **Added: Work-intent claims.** The `coordination-tiers` module installs `tools/intent.py`, a work-intent CLI with `claim`, `list` and `release`, plus opt-in hooks that warn when a commit touches an unclaimed path or one another session holds. ([coordination-tiers](templates/modules/team-gated/coordination-tiers.md), [intent.py](templates/modules/team-gated/intent.py))
- **Added: Testing, examples and doc-drift modules.** Three new modules cover testing discipline, an examples gallery and doc-drift prevention (which installs `link_check.py` and `sync_doc_snippets.py` to catch broken links and stale doc snippets), and a maturity ladder helps teams find their adoption level. ([testing-discipline](templates/modules/team-gated/testing-discipline.md), [doc-drift-prevention](templates/modules/team-gated/doc-drift-prevention.md), [on-ramp](on-ramp/README.md))
- **Added: Runnable default modules.** The default-on `claim-check` and `lifecycle-metrics` modules now install runnable standard-library scripts instead of pointing adopters at code to copy. ([claim_check.py](templates/modules/default-on/claim_check.py))
- **Added: Orientation docs and worked example.** New adopter-orientation docs and a minimal worked example trace one change through the lifecycle. ([getting-started](docs/getting-started.md), [examples/minimal](examples/minimal/))
- **Added: Eleven adopter practices.** Eleven practices from an adopter join the doctrine, including new `security-review` and `issue-capture` modules and a rate limit on doctrine changes. ([security-review](templates/modules/team-gated/security-review.md), [issue-capture](templates/modules/team-gated/issue-capture.md))
- **Added: Per-session identity.** Coordination identity is now derived per session rather than per tool, so concurrent sessions of the same tool no longer release each other's claims. ([coordination](docs/methodology/coordination.md))
- **Changed: Required plan review line.** Every plan now carries a mandatory `Plan review: required(<tier>) | not required(<rationale>)` line, and a required plan is reviewed before implementation begins. ([lifecycle](docs/methodology/lifecycle.md))
- **Changed: Claims before edits.** A work-intent `claim` is now required before every nontrivial edit when a team works concurrently, though it stays a courtesy signal and not a lock. ([coordination](docs/methodology/coordination.md))
- **Changed: Staleness sweep and archive rules.** The goodnight routine gains a staleness sweep, and archiving a plan or removing a roadmap item now has stated preconditions. ([lifecycle](docs/methodology/lifecycle.md))
- **Security: Private addresses refused.** The external link check now refuses private, loopback and other internal addresses, and the security lint covers every shipped script. ([SECURITY.md](SECURITY.md))
- **Security: Templates defended as instructions.** Templates are now treated as instructions agents will run, and defended that way: scaffolding refuses to write through symlinks or outside the target, releases carry a derived install manifest, and a content scanner flags suspicious text for human review. ([PROVENANCE.md](bootstrap/PROVENANCE.md))

### Minor changes

- **Added** — Doctrine gains the signal-now, benefit-later principle for coordination and a note that the claim checker cannot verify runtime-behavior claims. ([coordination](docs/methodology/coordination.md))
- **Added** — Cairn now checks links and claimed paths across its own Markdown with `scripts/check_cairn.py`. ([check_cairn.py](scripts/check_cairn.py))
- **Changed** — Inserting a claim-check marker next to a path is now allowed as mechanical maintenance, even in another agent's review section. ([lifecycle](docs/methodology/lifecycle.md))

## 0.1.1 — 2026-05-21

### Major changes

- **Added: Nine adopter practices.** Nine practices from an adopter join the doctrine: a required-signal-read mode and collision log for coordination, a rewrite-from-scratch next-session plan, a capability-floor rule for roles, and a new `model-selection` module. ([coordination](docs/methodology/coordination.md), [model-selection](templates/modules/team-gated/model-selection.md))

## 0.1.0 — 2026-05-20

### Major changes

- **Added: Initial release.** Initial public release.
