<!-- cairn-internal-ref-allow: doctrine/coordination.md doctrine/session-routines.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
# Next-session candidates — Cairn

`NEXT_SESSION.md` carries the **cold-pickup handoff**: the
recommended next task and a queue of candidates, each with enough
context — file paths, scope, effort, payoff, risks — to begin
without the prior session's conversation.

It complements `PLANNING.md`: `PLANNING.md` says *what* is queued;
`NEXT_SESSION.md` says *how to actually pick it up*.

`NEXT_SESSION.md` is **rewritten from scratch** by the full-
handoff owner at each goodnight — the physical action is "open
a blank file and write," not "edit the previous version."
Anything in the previous goodnight's version that does not
earn its place in the next session's orientation is dropped;
durable claims migrate to their proper home (doctrine, the
roadmap, a proposal) **before** the rewrite. See
`doctrine/session-routines.md` > "The next-session starting
plan: written from scratch each goodnight" for the load-bearing
reasoning.

The required-signal-read discipline on shared communication
files applies (`doctrine/coordination.md` > "Required
signal+read for coordination-surface files").

## Recommended starting point

<!-- cairn:slot next-start -->
**Task + current state.** **Open plans for the nine proposals accepted
2026-08-03** — but *check the intent log first*. At handoff a concurrent agent
(`claude-d8d22f62`) held an active claim on `dev/plans` with action
`open five plans`, so some of this may already be done. Run
`python tools/intent.py list` and `python tools/lifecycle.py session-start`
before writing anything into `dev/plans/`.

The nine, with what each plan must carry beyond the ordinary:

| Proposal | The thing the plan must not lose |
|---|---|
| `security-verification-activation` | **Plan this first** — it is the dependency root; the two capability proposals define their invocation contract against it |
| `portable-security-sweeps` | **Two Maintainer conditions**: build a Gitleaks *version apparatus* (admit / re-measure / retire), and **Cairn adopts the module itself** so the apparatus is exercised |
| `api-web-security-modules` | The **AW4 adversarial network-client fixtures** are a blocking gate: DNS answer changing between resolution and connection, redirect to every refused address class, connected-peer disagreement, credential carry-over |
| `separator-detection` | **Owns** the `_scan_unicode` yielded-id signature change; carries the coexistence test that fails against today's code |
| `content-scan-detectors` | **Rebases onto** the yielded-id form if it implements second; must not reintroduce the ternary |
| `dependency-advisory-coverage` | Residual baseline admits **locally-built only** (PEP 610 `direct_url.json`), never "public package with no advisory record" |
| `gate-claims-vs-enforcement` | Row E1's fallback is an **archive precondition**, not prose |
| `release-security-bar` | Accepting it did **not** fix `verify_integrity.py`; that is a board row |
| `security-preflight-checklist` | **No plan** — a single implementing commit against the proposal template |

**Why this first.** Nine accepted proposals with no plans is the largest
unconverted decision backlog the board has carried, and two of them
(`separator-detection`, `content-scan-detectors`) edit the same three sites in
`content_scan.py` with a stated ordering rule that only exists in their
Decisions.

**Effort.** Large; naturally splits per proposal. **Payoff.** Converts a night of
decisions into executable work. **Risk.** Plan-opening collides with the
concurrent agent — hence the intent check.

## Other candidates

**Push, and carry the trust root.** 129 commits and
`refs/cairn/gate-anchor` at `e45e1fc` are unpushed. A plain `git push` does
**not** carry custom refs:

```
git push origin master
git push origin refs/cairn/gate-anchor:refs/cairn/gate-anchor
```

Needs Maintainer approval. Until then tonight's trust root and the whole
deliberation record exist on one disk. Pushing also finally makes the
**SR9 external-anchoring** upgrade available — `_gate_manifest.py verify
--trusted-repo <fresh-clone>` means something only once `P` exists off-machine,
and `P` now does.

**Another session's uncommitted engine work.** At handoff the tree carried
modified `bootstrap/verify_integrity.py`, `lockfile.py`, `install.py`,
`upgrade.py`, `test_lockfile_module.py`, `test_verify_integrity.py`, and an
untracked `bootstrap/tests/test_fork_advisory.py`. **Not mine and not
abandoned** — establish ownership before touching or running gates over them.

**Two security follow-ups on the board**, both with revival conditions, neither
urgent:

* **Conda advisory coverage** — 147 conda-only packages, 82 native, unaudited by
  anything Cairn ships. Trivy and OSV-Scanner are eliminated on primary docs;
  **Grype/Syft are unevaluated by anyone** and are the first thing to actually
  run. Revival is execution-bound on purpose.
* **Install-integrity trust anchor** — `verify_integrity.py:47` reads expected
  hashes from the candidate's own lockfile, so a coordinated tamper verifies
  `OK`. Needs its own threat model, not a patch.

**`SECURITY.md` disclosure channel** (Queued) — the half of the superseded
`contributor-entry` that survived. Carries finding [I7]: the channel's deciding
property is whether the forge setting is *actually enabled*, which no reviewer
can establish. **Maintainer live-verification step**, not a review item.

**A doctrine gap worth one small proposal.** `AGENTS.md` frames orientation as a
cold-start/context-loss routine and does not name **opening a lifecycle
artifact** as a trigger. That gap produced a proposal opened 74 minutes after a
sibling plan claimed the same three symbols, superseded the same night. The fix
is one sentence; the evidence is in the archived
`2026-08-03-claude-yaml-parser-divergence`.

**Also unresolved:** there is still **no runbook for the AST baseline
re-anchor**. `AGENTS.md:335-338` no longer points at the wrong one, but the
procedure lives only as precedent (`c3d5bd9`) and as prose inside two plans.
Deferred Maintainer question 4 is marked resolved-with-residual on that point.
