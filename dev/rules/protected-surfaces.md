# Protected surfaces and trust operations

What needs a proposal, which surfaces are high risk, and who re-anchors. Routed from `RULES.md`. The text below moved from `AGENTS.md` on 2026-11-10 unchanged.

Doctrine or scaffold-engine changes need a proposal. A one-line engine change
also needs Security Review unless it qualifies as the documented cheap defect
repair. High-risk surfaces include `bootstrap/scaffold.py` and
`bootstrap/_scaffold/`; protected tests/control machinery (`conftest.py`,
`security_manifest.py`, `_ast_attest.py`, `_loader_proto.py`, `_gate_*`,
`_oracle*`, and gate/AST fixtures); install/fidelity/gate manifests, lockfile
schema and published install manifest; vendor-neutral methodology and templates;
the per-worktree interpreter binding and its shipped/self-hosted readers and
writer; and `run_portable_security_sweeps.py` plus its policy and shipped
copy. Their required checks and security details are in `bootstrap/SAFETY.md`,
`bootstrap/REANCHOR_RUNBOOK.md`, and the named tests. Changes to high-risk
surfaces retain their proposal and Security Review obligations.

The installer uses a per-worktree binding in Git administration. The reader
`templates/skills/_lib/session.py` is copied byte-for-byte to `tools/session.py`;
the writer is in `bootstrap/_scaffold/install.py`. Rebind after copying a Git
administration directory. The portable sweep is also kept byte-identical
between `scripts/` and `templates/modules/team-gated/`; it resolves and
revalidates host executables immediately before invocation, treats absence as
incomplete and has no egress path.

The AST baseline and gate manifest can become stale silently. Follow
`bootstrap/AST_BASELINE_RUNBOOK.md` for engine edits and
`bootstrap/REANCHOR_RUNBOOK.md` for ceremonies; only the Maintainer performs
the prescribed re-anchor. A fresh clone lacks `refs/cairn/gate-anchor`; fetch
it from the trusted origin and verify the signed commit before relying on it.
