# Edit list: stale text (plan A of the defect arc)

Companion to `dev/plans/2026-11-20-defect-arc-a-stale-text.md`, which says why this file exists and how to apply it. Each edit gives the exact text to find and the exact text to put in its place. A `Find` block occurs exactly once in every target named for it (checked at the commit the plan names). Copy it byte for byte; a line break inside a block is a real line break. Shipped twins get the identical replacement. No edit names a model or a vendor.

## C1: the quickstart (`docs/quickstart.md`)

### Q1

Targets: `docs/quickstart.md`

Find:

```text
Copy-Item "$CAIRN\bootstrap\profiles\solo-greenfield.yml" profile.yml
```

Replace with:

```text
Copy-Item "$CAIRN\install\profiles\solo-greenfield.yml" profile.yml
```

### Q2

Targets: `docs/quickstart.md`

Find:

```text
python "$CAIRN\bootstrap\scaffold.py" --config profile.yml --target . --summary
python "$CAIRN\bootstrap\scaffold.py" --config profile.yml --target .
```

Replace with:

```text
python "$CAIRN\install\scaffold.py" --config profile.yml --target . --summary
python "$CAIRN\install\scaffold.py" --config profile.yml --target .
```

### Q3

Targets: `docs/quickstart.md`

Find:

```text
> `VENDOR.md`, `NOTICE.md`, `.gitattributes`, `.gitignore`, `dev/`,
```

Replace with:

```text
> `VENDOR.md`, `RULES.md`, `NOTICE.md`, `.gitattributes`, `.gitignore`, `dev/`,
```

### Q4

Targets: `docs/quickstart.md`

Find:

```text
git add AGENTS.md VENDOR.md NOTICE.md .gitattributes .gitignore dev/ .agents/ docs/ CHANGELOG.md
```

Replace with:

```text
git add AGENTS.md VENDOR.md RULES.md NOTICE.md .gitattributes .gitignore dev/ .agents/ docs/ CHANGELOG.md
```

## C2: text that names the pre-0.8 layout

### L1

Targets: `install/profiles/solo-greenfield.yml`; `install/profiles/collaborative-team.yml`; `install/profiles/high-rigor-legacy.yml`

Find:

```text
(per cairn/dimensions/ rubrics):
```

Replace with:

```text
(per install/dimensions/ rubrics):
```

### L2

Targets: `install/profiles/solo-greenfield.yml`

Find:

```text
# bootstrap/scaffold.py's _PRESETS):
```

Replace with:

```text
# install/_scaffold/config.py's _PRESETS):
```

### L3

Targets: `install/profiles/solo-greenfield.yml`

Find:

```text
# See cairn/on-ramp/README.md.
```

Replace with:

```text
# See install/on-ramp/README.md.
```

### L4

Targets: `install/profiles/collaborative-team.yml`

Find:

```text
# cairn/bootstrap/BOOTSTRAP.md with your agent.
```

Replace with:

```text
# install/BOOTSTRAP.md with your agent.
```

### L5

Targets: `install/profiles/high-rigor-legacy.yml`

Find:

```text
# Recommended pre-pass: fill cairn/templates/codebase-readiness-report.md
```

Replace with:

```text
# Recommended pre-pass: fill install/codebase-readiness-report.md
```

### L6

Targets: `install/profiles/high-rigor-legacy.yml`

Find:

```text
# readiness-report pre-pass (cairn/on-ramp/README.md > "Choosing a
```

Replace with:

```text
# readiness-report pre-pass (install/on-ramp/README.md > "Choosing a
```

### L7

Targets: `install/dimensions/human-team.md`

Find:

```text
  (`../bootstrap/fidelity-check.md`). A solo project ships no
```

Replace with:

```text
  (`../fidelity-check.md`). A solo project ships no
```

### L8

Targets: `docs/methodology/rationale.md`

Find:

```text
`AGENTS.md` — lives in `../bootstrap/fidelity-check.md`. The harvest
```

Replace with:

```text
`AGENTS.md` — lives in `../../install/fidelity-check.md`. The harvest
```

### L9

Targets: `docs/case-studies/modflow_tools-fidelity-manifest.yml`

Find:

```text
# Format spec: ../bootstrap/fidelity-check.md
```

Replace with:

```text
# Format spec: ../../install/fidelity-check.md
```

### L10

Targets: `templates/modules/default-on/security-verification.md`; `dev/modules/security-verification.md`

Find:

```text
> Review, the same tier as `bootstrap/_scaffold/` in Cairn's own
```

Replace with:

```text
> Review, the same tier as `install/_scaffold/` in Cairn's own
```

### L11

Targets: `docs/methodology/coordination.md`

Find:

```text
`python tools/intent.py install-precommit`; the scaffold never installs it.
```

Replace with:

```text
`python dev/tools/intent.py install-precommit`; the scaffold never installs it.
```

### L12

Targets: `docs/methodology/coordination.md`

Find:

```text
mismatch, compare `python tools/intent.py whoami` in each relevant command
```

Replace with:

```text
mismatch, compare `python dev/tools/intent.py whoami` in each relevant command
```

### L13

Targets: `docs/methodology/coordination.md`

Find:

```text
`CAIRN_AGENT=synthetic-codex-a python tools/intent.py claim --files src/a.py
```

Replace with:

```text
`CAIRN_AGENT=synthetic-codex-a python dev/tools/intent.py claim --files src/a.py
```

### L14

Targets: `docs/methodology/session-routines.md`

Find:

```text
   (`python tools/intent.py list`) and confirm the hooks are present
   (`python tools/intent.py hooks-status`): a starting session sees who holds
```

Replace with:

```text
   (`python dev/tools/intent.py list`) and confirm the hooks are present
   (`python dev/tools/intent.py hooks-status`): a starting session sees who holds
```

### L15

Targets: `docs/methodology/session-routines.md`

Find:

```text
   When `tools/board.py` is available, use the **board** as an orientation
   view before reading the relevant artifacts:

   ```
   python tools/board.py
```

Replace with:

```text
   When `dev/tools/board.py` is available, use the **board** as an orientation
   view before reading the relevant artifacts:

   ```
   python dev/tools/board.py
```

### L16

Targets: `docs/methodology/session-routines.md`

Find:

```text
(`tools/session.py`). The skill bodies orchestrate the *mechanizable* steps
```

Replace with:

```text
(`dev/tools/session.py`). The skill bodies orchestrate the *mechanizable* steps
```

### L17

Targets: `docs/methodology/session-routines.md`

Find:

```text
The skills + `tools/session.py` carry the *universal* routine — the
```

Replace with:

```text
The skills + `dev/tools/session.py` carry the *universal* routine — the
```

### L18

Targets: `docs/code-map.md`

Find:

```text
python -I tools/code_map.py --root PATH
python -I tools/code_map.py --root PATH --changed src/module.py
python -I tools/code_map.py --root PATH --changed src/a.py --changed src/b.py
python -I tools/code_map.py --root PATH --release
```

Replace with:

```text
python -I dev/tools/code_map.py --root PATH
python -I dev/tools/code_map.py --root PATH --changed src/module.py
python -I dev/tools/code_map.py --root PATH --changed src/a.py --changed src/b.py
python -I dev/tools/code_map.py --root PATH --release
```

### L19

Targets: `dev/plans/_template.md`

Find:

```text
`python tools/board.py --maintainer` lists
```

Replace with:

```text
`python dev/tools/board.py --maintainer` lists
```

### Entries added at plan review (finding 1)

The plan review found four shipped module pages, their Cairn copies, the plan template's tooling slot and one profile comment that still name `scripts/` or `bootstrap/`. Entries S1a to S4b, T1 to T3 and P1 follow, in the reviewer's words. They belong to chunk C2.

### S1a

Targets: `templates/modules/default-on/claim-check.md`; `dev/modules/claim-check.md`

Find:

```text
scaffold installs as `claim_check.py` in the target's `scripts/`
```

Replace with:

```text
scaffold installs as `claim_check.py` in the target's `dev/tools/`
```

### S1b

Targets: `templates/modules/default-on/claim-check.md`; `dev/modules/claim-check.md`

Find:

```text
writes `claim_check.py` into the target's `scripts/` directory
```

Replace with:

```text
writes `claim_check.py` into the target's `dev/tools/` directory
```

### S1c

Targets: `templates/modules/default-on/claim-check.md`; `dev/modules/claim-check.md`

Find:

```text
allow.json, scripts/check_cairn.py,
```

Replace with:

```text
allow.json, tests/check_cairn.py,
```

### S1d

Targets: `templates/modules/default-on/claim-check.md`; `dev/modules/claim-check.md`

Find:

```text
cites Cairn's own `scripts/check_cairn.py`
```

Replace with:

```text
cites Cairn's own `tests/check_cairn.py`
```

### S1e

Targets: `templates/modules/default-on/claim-check.md`; `dev/modules/claim-check.md`

Find:

```text
on itself: `scripts/check_cairn.py` imports
```

Replace with:

```text
on itself: `tests/check_cairn.py` imports
```

### S2a

Targets: `templates/modules/team-gated/content-security.md`; `dev/modules/content-security.md`

Find:

```text
in the target's `scripts/` directory.
```

Replace with:

```text
in the target's `dev/tools/` directory.
```

### S2b

Targets: `templates/modules/team-gated/content-security.md`; `dev/modules/content-security.md`

Find:

```text
writes `content_scan.py` into the target's `scripts/`
```

Replace with:

```text
writes `content_scan.py` into the target's `dev/tools/`
```

### S2c

Targets: `templates/modules/team-gated/content-security.md`; `dev/modules/content-security.md`

Find:

```text
(installed beside the runner in `scripts/`)
```

Replace with:

```text
(installed beside the runner in `dev/tools/`)
```

### S3a

Targets: `templates/modules/team-gated/doc-drift-prevention.md`; `dev/modules/doc-drift-prevention.md`

Find:

```text
`scripts/` directory — `link_check.py`
```

Replace with:

```text
`dev/tools/` directory — `link_check.py`
```

### S3b

Targets: `templates/modules/team-gated/doc-drift-prevention.md`; `dev/modules/doc-drift-prevention.md`

Find:

```text
`scripts/` directory:
```

Replace with:

```text
`dev/tools/` directory:
```

### S3c

Targets: `templates/modules/team-gated/doc-drift-prevention.md`; `dev/modules/doc-drift-prevention.md`

Find:

```text
When Cairn runs `scripts/check_cairn.py`
```

Replace with:

```text
When Cairn runs `tests/check_cairn.py`
```

### S3d

Targets: `templates/modules/team-gated/doc-drift-prevention.md`; `dev/modules/doc-drift-prevention.md`

Find:

```text
citations) into the target's `scripts/`.
```

Replace with:

```text
citations) into the target's `dev/tools/`.
```

### S3e

Targets: `templates/modules/team-gated/doc-drift-prevention.md`; `dev/modules/doc-drift-prevention.md`

Find:

```text
`render_schema_docs.py` under `scripts/`
```

Replace with:

```text
`render_schema_docs.py` under `dev/tools/`
```

### S3f

Targets: `templates/modules/team-gated/doc-drift-prevention.md`

Find:

```text
docs/methodology/, scripts/check_cairn.py,
```

Replace with:

```text
docs/methodology/, tests/check_cairn.py,
```

### S4a

Targets: `templates/modules/default-on/security-verification.md`; `dev/modules/security-verification.md`

Find:

```text
`run_security_verification.py` in the target's `scripts/` directory
```

Replace with:

```text
`run_security_verification.py` in the target's `dev/tools/` directory
```

### S4b

Targets: `templates/modules/default-on/security-verification.md`; `dev/modules/security-verification.md`

Find:

```text
target's `scripts/` directory (copied
```

Replace with:

```text
target's `dev/tools/` directory (copied
```

### T1

Targets: `dev/plans/_template.md`

Find:

```text
`python scripts/sync_doc_snippets.py`
```

Replace with:

```text
`python dev/tools/sync_doc_snippets.py`
```

### T2

Targets: `dev/plans/_template.md`

Find:

```text
`python scripts/check_cairn.py`
```

Replace with:

```text
`python tests/check_cairn.py`
```

### T3

Targets: `dev/plans/_template.md`

Find:

```text
`python scripts/link_check.py`
```

Replace with:

```text
`python dev/tools/link_check.py`
```

### P1

Targets: `dev/.cairn/profile.yml`

Find:

```text
lockfile with `python bootstrap/scaffold.py upgrade --init-lock --target .`
```

Replace with:

```text
lockfile with `python install/scaffold.py upgrade --init-lock --target .`
```

## C3: the prune command and a missing `python`

### R1

Targets: `.agents/skills/session-end/SKILL.md`; `templates/skills/session-end/SKILL.md`

Find:

````text
Give the user this exact command:

```
CAIRN_HANDOFF_OWNER=1 python dev/tools/session.py session-end --handoff
```
````

Replace with:

````text
Give the user this exact command, in the form for the shell the session uses
(give both if you do not know). In bash or zsh:

```
CAIRN_HANDOFF_OWNER=1 python dev/tools/session.py session-end --handoff
```

In PowerShell, which cannot set a variable in front of a command, set it for
this one run:

```
$env:CAIRN_HANDOFF_OWNER = '1'; python dev/tools/session.py session-end --handoff; Remove-Item Env:CAIRN_HANDOFF_OWNER
```
````

### R2

Targets: `dev/modules/coordination-tiers.md`; `templates/modules/team-gated/coordination-tiers.md`

Find:

```text
>   `CAIRN_HANDOFF_OWNER=1 python dev/tools/session.py session-end --handoff`.
```

Replace with:

```text
>   `CAIRN_HANDOFF_OWNER=1 python dev/tools/session.py session-end --handoff`
>   in bash or zsh, or `$env:CAIRN_HANDOFF_OWNER = '1'; python
>   dev/tools/session.py session-end --handoff; Remove-Item
>   Env:CAIRN_HANDOFF_OWNER` in PowerShell.
```

### R3

Targets: `docs/methodology/session-routines.md`

Find:

```text
  `CAIRN_HANDOFF_OWNER=1 python tools/session.py session-end --handoff`.
```

Replace with:

```text
  `CAIRN_HANDOFF_OWNER=1 python dev/tools/session.py session-end --handoff`
  in bash or zsh, or `$env:CAIRN_HANDOFF_OWNER = '1'; python
  dev/tools/session.py session-end --handoff; Remove-Item
  Env:CAIRN_HANDOFF_OWNER` in PowerShell.
```

### R4

Targets: `.agents/skills/session-start/SKILL.md`; `templates/skills/session-start/SKILL.md`

Find:

````text
python dev/tools/session.py session-start
```

It **reports** (read-only)
````

Replace with:

````text
python dev/tools/session.py session-start
```

If `python` is not found (on Windows the message mentions the Microsoft Store),
run the same command with `py -3`, or with the full path of your interpreter.
The installer saved that path as the `interpreter` entry of the
`local-env.json` file in your project's Git folder, under `cairn`.

It **reports** (read-only)
````

## C4: the prose check on a fresh clone

### M1

Targets: `.agents/skills/session-start/SKILL.md`; `templates/skills/session-start/SKILL.md`

Find:

```text
project-export paths (`dev/measurement/meter.json` under each project), and
```

Replace with:

```text
project-export paths (each project's `meter.json` file in `dev/measurement/`), and
```

### M2

Targets: `dev/rules/custom_session_routines.md`

Find:

```text
not read an older `dev/measurement/meter.json`, pass an aggregate path, or
```

Replace with:

```text
not read an older `meter.json` export in `dev/measurement/`, pass an aggregate path, or
```

### M3

Targets: `templates/core/dev/measurement/README.md`

Find:

```text
  `dev/measurement/meter.json` export. The recurring work and cost depend on
```

Replace with:

```text
  `meter.json` export in its `dev/measurement/` folder. The recurring work and cost depend on
```

### M4

Targets: `dev/measurement/certification-run-2026-11-12-per-file.md`

Find:

```text
[suite-cost.md](suite-cost.md) gives the longer account.
```

Replace with:

```text
a local suite-cost file, which Git ignores and a fresh clone does not carry,
gives the longer account.
```

## C5: the upgrade notes and the changelog

### U1

Targets: `install/UPGRADE.md`

Find:

```text
sections before it are migration notes and background: moving to one review
stage, files Cairn stopped shipping, and the two on-disk artifacts. Read them
when the workflow sends you there.
```

Replace with:

```text
sections before it are migration notes and background: moving to one review
stage, the 0.8 layout move, files Cairn stopped shipping, and the two on-disk
artifacts. Read them when the workflow sends you there.
```

### U2

Targets: `install/UPGRADE.md`

Find:

```text
**Start here.** To run an upgrade, go to [The workflow](#the-workflow). The three
```

Replace with:

```text
**Start here.** To run an upgrade, go to [The workflow](#the-workflow). The four
```

### U3

Targets: `install/UPGRADE.md`

Find:

```text
## Files Cairn stopped shipping
```

Replace with:

````text
## Moving an install from 0.7.0 to the 0.8 layout

Cairn 0.8 moved the tool scripts it installs in your project, from `scripts/`
and `tools/` to `dev/tools/`. An install made by 0.7.0 or earlier meets this
move before any ordinary upgrade; an install from 0.8.0 or later does not.
The move runs on its own, and a receipt makes it apply exactly what you
staged. Run it from a full clone of Cairn, with all of its history: the
installer checks each old copy against that history, and a shallow clone
cannot supply it.

1. `python install/scaffold.py upgrade --target <repo> --plan` lists each move
   as `action: old -> new`. It writes nothing. A line that starts `blocked:`
   (for example "unproved ancestry") means the installer could not match an
   old copy to a Cairn release: do step 2 first. Without one, go to step 3.
2. `upgrade --target <repo> --stage --reconcile-layout <REV>` compares the old
   copies with the Cairn revision `<REV>` (the release the project was
   installed from, for example its tag) and prints `Apply to the same project
   with --apply --migration-receipt <digest>`. Run that printed command
   exactly; it ends with `Layout reconciliation complete.` Then run `--plan`
   again.
3. `upgrade --target <repo> --stage` stages the move and prints the same kind
   of `Apply to the same project ...` line.
4. Run that printed command exactly. It ends with `Layout migration
   complete.`
5. Now follow [The workflow](#the-workflow).

If a run stops partway, the next `upgrade` command says where the unfinished
move is; resume it with `--apply --migration-receipt <digest>`.

**Known limit.** `--plan` lists only the moves that can be made now. A second
move can show up only after the first is applied, so the first `--plan` may
not list every move. Run `--plan` again after each apply.

## Files Cairn stopped shipping
````

### U4

Targets: `install/UPGRADE.md`

Find:

```text
  If `--plan` lists files that differ only in line endings, Git converted saved ancestors or scripts when it checked your project out (`core.autocrlf`). Re-clone with `git clone -c core.autocrlf=false` and run `--plan` again; do not edit `dev/.cairn/base/`.
```

Replace with:

```text
  If `--plan` lists files that differ only in line endings, Git converted saved ancestors or scripts when it checked your project out (`core.autocrlf`). Re-clone with `git clone -c core.autocrlf=false` and run `--plan` again; do not edit `dev/.cairn/base/`.

  The same applies to the Cairn checkout you run the upgrade from. On Windows, Git for Windows may set `core.autocrlf=true`, which gives Cairn's own pinned helper files CRLF line endings. The upgrade then stops with `use a Cairn Git checkout with the legacy installer history to verify these old copies`, although the clone has its full history. Clone Cairn with `git clone -c core.autocrlf=false` as well.
```

### CL1

Targets: `CHANGELOG.md`

This entry is written last, after re-reading `## Unreleased`. If a `### Minor changes` heading already sits under `## Unreleased`, add the entry under it, newest first. If none does, add the heading and the entry after the last Major entry, before `## 0.8.0`. It is one line, not a Find and Replace pair.

Entry:

```text
- **Fixed: Stale paths and commands in the docs.** The quickstart's Windows steps, the goodnight prune command, the session-start step for a missing `python`, the upgrade notes and several older path names now match the layout Cairn 0.8 installs, and the prose check passes on a fresh clone. ([plan](dev/plans/2026-11-20-defect-arc-a-stale-text.md))
```

## Scope the Maintainer added: the licence notes

Added on 2026-11-20, after the plan review and before the code review. The two licence notes named folders the 0.8 layout moved or removed. The Maintainer chose to say what the content is instead of listing folders, with the licences unchanged: code is MIT; prose, document templates and explanatory diagrams are CC BY 4.0; the brand mark is CC BY-ND. He approved the words of N1 and N3 and the cut in N2 (chat, 2026-11-20). N4 applies the same rule to one line of the second note; its words are Strategy's. Nothing about what is licensed changes.

### N1

Targets: `LICENSE-CC-BY.md`

Find:

```text
The **prose, templates, and explanatory visuals** in this repository —
the methodology (`docs/methodology/`), the dimensions (`dimensions/`), the case
studies (`case-studies/`), the bootstrap narrative (`bootstrap/*.md`),
the forkable **document templates** — the Markdown (`.md`) files under
`templates/` — the on-ramp (`on-ramp/`), this repository's documentation
(`README.md`, `CITATION.cff`), the project site's page (`docs/index.html`),
and the **explanatory diagrams** under `docs/assets/`
(`dual-review-independence.svg`, `shared-record-across-sessions.svg`,
`three-lanes-of-change.svg`, `independent-scientific-check.svg`,
`two-ways-to-adopt.svg`, `assai-components.svg`,
`assai-authority-boundaries.svg`, and `assai-investigation-cycle.svg`) — are licensed under
the **Creative Commons Attribution 4.0 International License (CC BY 4.0)**.
```

Replace with:

```text
The **prose, document templates, and explanatory diagrams** in this repository
are licensed under the **Creative Commons Attribution 4.0 International License
(CC BY 4.0)**. This is decided by what a file is, not by the folder it sits in.
It covers everything written for people to read or adapt: the methodology and
guides, the case studies, the installation and release instructions, the
forkable **document templates** (the Markdown files Cairn installs in a
project), this repository's `README.md` and `CITATION.cff`, the project site's
page, and every explanatory diagram.
```

### N2

Targets: `LICENSE-CC-BY.md`

Find:

```text
`templates/modules/team-gated/link_check.py`) and anything under `scripts/`.
```

Replace with:

```text
`templates/modules/team-gated/link_check.py`).
```

### N3

Targets: `LICENSE-CC-BY.md`

Find:

```text
All **source code** in this repository — `bootstrap/scaffold.py` and its
tests, the shipped Python tools under `templates/` and `scripts/`, and any
other code file — is licensed separately under the MIT License, which takes
precedence over this document license. See [`LICENSE-MIT.md`](LICENSE-MIT.md).
```

Replace with:

```text
All **source code** in this repository — the installer, the shipped Python
tools, the tests, and any other code file — is licensed separately under the
MIT License, which takes precedence over this document license. See
[`LICENSE-MIT.md`](LICENSE-MIT.md).
```

### N4

Targets: `LICENSE-CC-BY-ND.md`

Find:

```text
  including the tools shipped under `templates/` and `scripts/` — is
```

Replace with:

```text
  including the tools Cairn ships — is
```
