# Protected surfaces and trust operations

What needs a proposal, which surfaces are high risk, and who re-anchors. Routed from `RULES.md`. The text below moved from `AGENTS.md` on 2026-11-10 unchanged.

Doctrine or scaffold-engine changes need a proposal. A one-line engine change
also needs Security Review unless it qualifies as the documented cheap defect
repair. High-risk surfaces include `install/scaffold.py` and
`install/_scaffold/`; protected tests/control machinery (`conftest.py`,
`security_manifest.py`, `_ast_attest.py`, `_loader_proto.py`, `_gate_*`,
`_oracle*`, and gate/AST fixtures); install/fidelity/gate manifests, lockfile
schema and published install manifest; vendor-neutral methodology; Python
templates, installer structure (`cairn:slot`, `{{token}}`, and parsed task
syntax), and functional template configuration such as
`templates/core/gitattributes.txt`;
the per-worktree interpreter binding and its shipped/self-hosted readers and
writer; and `run_portable_security_sweeps.py` plus its policy and shipped
copy. Their required checks and security details are in `install/SAFETY.md`,
`release/REANCHOR_RUNBOOK.md`, and the named tests. Changes to high-risk
surfaces retain their proposal obligation. Prose-only changes to template prose
do not enter the high-risk list; a change that also alters code, installer
structure, or functional configuration remains high-risk. A change gets the
heavy tier when it alters what a high-risk surface does or accepts, or adds a
place where outside input meets the system; merely touching a surface does
not. When in doubt, take the Security Review. A project rule that names its
own Security Review still applies.

The installer uses a per-worktree binding in Git administration. The reader
`templates/skills/_lib/session.py` is copied byte-for-byte to `dev/tools/session.py`;
the writer is in `install/_scaffold/install.py`. Rebind after copying a Git
administration directory. The portable sweep is also kept byte-identical
between `dev/tools/` and `templates/modules/team-gated/`; it resolves and
revalidates host executables immediately before invocation, treats absence as
incomplete and has no egress path.

The AST baseline and gate manifest can become stale silently. Follow
`release/AST_BASELINE_RUNBOOK.md` for engine edits and
`release/REANCHOR_RUNBOOK.md` for ceremonies; only the Maintainer performs
the prescribed re-anchor. A fresh clone lacks `refs/cairn/gate-anchor`; fetch
it from the trusted origin and verify the signed commit before relying on it.

Plan finishing and the AST baseline. Moved from `dev/agent_collaboration.md` > "Plans and records" on 2026-11-10 unchanged: A verified expected AST mismatch from reviewed planned engine changes remains unpassed until the separate release baseline operation, but alone does not block plan archive. Unexpected AST drift remains implementation work.

Tests exempt from the promise-only cut. Cut only through a Security Review: tests of the surfaces above; the security-family files and native-only IDs in `tests/security_manifest.py`; tests that a release document, `install/SAFETY.md`, `install/_scaffold/SECURITY_MUTATIONS.md` or a shipped file names as a guard; and refusal, hostile-state and negative-guard tests. The generic rule is in the testing-discipline module.
