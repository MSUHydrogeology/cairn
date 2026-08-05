# Proposal: classify by file class in the adopter-facing content-scan runner

**Author**: Claude (Implementation)
**Status**: proposed
**Opened**: 2026-08-05
**Review**: required(External Security Review) — this changes a detector's reach
on a security surface adopters install

## Context

`content_scan.py` is single-sourced and serves two callers (its own module
docstring says so): Cairn composes it via `scripts/check_cairn.py` over its own
prose, and the `content-security` module ships it verbatim to adopters, where
`content_scan_runner.py` drives it.

**The two callers disagree about one detector, and the shipped one is wrong.**

| caller | line | `scan_urls` |
|---|---|---|
| `scripts/check_cairn.py` | `:392` | `scan_urls = _is_template_instruction(rel)` |
| `templates/modules/team-gated/content_scan_runner.py` | `:402` | `scan_urls=True` — hardcoded, every file |

The detector's own declared scope, from `content_scan.py`'s module docstring:

> `suspicious-url` -- a non-allowlisted external `http(s)` URL, in files scanned
> with `scan_urls=True` (**executed templates**).

and the parameter's own docstring at `:384-386`:

> `scan_urls` enables the `suspicious-url` detector (use for executed templates;
> **off for discussion prose**).

So the shipped runner applies a template-scoped detector to every file in the
audited roots, which are mostly discussion prose (`dev`, `docs`).

## The measurement

Over the runner's **own** declared roots (`content_scan_roots.txt`: `AGENTS.md`,
`.agents/skills`, `dev`, `docs`, `RULES.md`, `CLAUDE.md`, `VENDOR.md`),
git-tracked `.md`/`.txt`, same allowlist, `as_of` 2026-08-05 at `6b731ad`,
Python 3.13.13:

| configuration | flags |
|---|---|
| as shipped (`scan_urls=True` everywhere) | **79**, all `suspicious-url` |
| classified (`check_cairn.py:392`'s rule) | **0** |

140 files, 7 roots. **Every flag is `suspicious-url`; no other detector fires in
either configuration.**

**What supplied the material.** The classifier is `check_cairn.py`'s existing
`_is_template_instruction`, not a predicate written for this measurement — the
change under test does not supply the rule used to evaluate it. The file set comes
from the runner's own `load_audit_roots()` and `git ls-files`, not a glob of mine.
Script retained at the harness scratch path named in the implementing commit.

## Why this is not a coverage reduction

The obvious objection is that `dev/` prose *is* agent-loaded, so silencing a
detector there loses real coverage. It does not, and the reason is that two
different detectors cover two different threats:

* **`suspicious-url`** answers *"is there an external URL here at all"*. In an
  executed template a bare URL is an instruction to fetch. In prose it is a
  citation. That is why its declared scope is templates.
* **`egress`** answers *"is there an exfiltration verb near a destination"* —
  `send`/`upload`/`post`/... near a URL or an `@` address. **It is unconditional
  and this change does not touch it.** The dangerous prose pattern ("upload the
  results to http://…") is `egress`'s, not `suspicious-url`'s.

The measurement corroborates it rather than asserting it: `egress`,
`imperative-override`, `unicode-zero-width`, `unicode-bidi`, `homoglyph` and
`instruction-html-comment` return **zero** in both configurations, so
classification changes exactly one detector's reach and leaves six untouched.

## Proposed change

1. `content_scan_runner.py` classifies per file instead of hardcoding `True`,
   using the same rule as `check_cairn.py:392`. The rule is **single-sourced**:
   the predicate moves into `content_scan.py` (which both callers already
   import) and both call sites use it. Two copies of a classification rule is
   the defect this proposal is fixing, one level up.
2. A test that pins the asymmetry: an external URL in an instruction-class file
   flags; the same URL in a prose-class file does not; and an `egress` pattern in
   a **prose-class** file still flags. That third assertion is the one that keeps
   a future "just turn URLs off everywhere" change from passing.
3. The runner's docstring states the classification and why, so the next reader
   does not re-derive it from two disagreeing call sites.

## Consequences for work in flight

`default-security-stance` Gate **D-ON-3** requires a named default-adoption
corpus, and **D-ON-2** requires a recorded disposition of the default-on
consequence. This proposal removes the consequence rather than dispositioning it:
the "alarm-fatigue budget" that plan reserves was 79 flags of misconfiguration,
and the residual after this change is **zero**. `default-security-stance`
Amendment 44 row 11 (the allowlist-vs-reviewed-residual policy for those flags)
has nothing left to decide, and `content_scan_residuals.txt` needs no entries for
them.

That is a claim about *this* tree at *this* commit. It does not promise an
adopter's tree is clean, and D-ON's conditions are unchanged by it.

## Scope fence

* **Does not** flip any default selection. `content-security` remains
  team-gated; whether it becomes default-on is `default-security-stance`'s
  question and this proposal takes no position on it.
* **Does not** touch `content_scan.py`'s detectors, the allowlist mechanism, the
  suppression-marker grammar, or the roots manifest.
* **Does not** touch `check_cairn.py`'s behaviour — it already does the right
  thing; it only stops owning a private copy of the predicate.
* The 79 flags are **not** allowlisted, suppressed, or added to
  `content_scan_residuals.txt`. They stop being flags because the detector stops
  being applied outside its declared scope.

## Verification

* `python -m pytest bootstrap/tests` green, count re-measured at the implementing
  commit rather than carried from here (it has reported four different totals in
  three days).
* `python scripts/check_cairn.py` green — it must stay green *and* its flag
  behaviour must not change, since its call site is only being re-pointed at a
  shared predicate.
* The runner over the declared roots: 0 flags, exit 0, re-run at the implementing
  commit.
* `python scripts/quality_gate.py --sub neutrality` — no new FAIL in touched
  files.

---

## Revision 1 -- 2026-08-05 -- the proposed mechanism was wrong, and dangerous

Appended, not edited: the section above is what was believed when it was written.
**Its central conclusion survives. Its proposed mechanism does not, and point 1
was backwards.**

### The defect in the proposal

`check_cairn.py`'s classifier is, in full:

```python
def _is_template_instruction(rel: str) -> bool:
    return rel.startswith('templates/')
```

That is a predicate about **Cairn's source-repo layout**, where source templates
live under `templates/`. It is not a statement about file *role*. An adopter tree
has **no `templates/` directory at all** — the installed instruction surfaces are
`AGENTS.md`, the renamed vendor wrapper, `.agents/skills/`, `RULES.md`, and the
`dev/` tree. Cairn's own audited roots contain nothing under `templates/` either.

Measured, `as_of` 2026-08-05: of the 141 tracked files in the runner's declared
roots, `_is_template_instruction` returns True for **0**.

**So had the proposal been implemented as written, `scan_urls` would have been
`False` for every file in every tree, and the `suspicious-url` detector would
have been silently dead everywhere it ships.** That is not narrowing a detector
to its declared scope; it is deleting it while appearing to configure it.

**And the original measurement could not have revealed this**, which is the part
worth recording. "Classified: 0 flags" was read as *the prose noise is gone*. It
actually meant *URL scanning is off for all 141 files*. Both produce zero. The
measurement I called independent was independent of the **change** while being
coupled to the **layout** — so it confirmed the conclusion I expected by a
mechanism I had not checked. This is the recurring invariant landing on me:
**the artifact under verification must not supply the material used to verify
it**, and a predicate borrowed from a different tree's layout is exactly such
material.

### The corrected mechanism

Classification is by **file role in the tree being scanned**, not by a path
prefix from another tree:

* **instruction class** (`scan_urls=True`) — the agent-loaded instruction
  surfaces: `AGENTS.md`, the vendor wrapper (`CLAUDE.md` / `GEMINI.md` / …),
  `RULES.md`, and everything under `.agents/skills/`. In these a live external
  URL is an instruction to fetch.
* **prose class** (`scan_urls=False`) — `dev/` deliberation and `docs/`. Here a
  URL is a citation.

**Point 1 of the proposal is withdrawn.** Single-sourcing the predicate between
`check_cairn.py` and `content_scan_runner.py` is the **wrong** call: the two
callers scan two different trees with two different layouts, and one shared
prefix test cannot be correct for both. What is legitimately shared is the
*concept* (two classes, and which detector each gets); the *mapping* is
per-caller and must be stated per caller. `check_cairn.py` keeps its
`templates/` test, which is right for the tree it scans.

### Re-measurement under the corrected mechanism

Same roots, same allowlist, `as_of` 2026-08-05:

| | files | flags |
|---|---|---|
| as shipped (`scan_urls=True` everywhere) | 141 | **80**, all `suspicious-url` |
| role-based classification | 4 instruction / 137 prose | **0** |

**The conclusion holds, and now for a reason that was checked rather than
assumed:** all 80 flags fall in the **prose** class, and the 4 instruction-class
files produce **zero** flags with URL scanning **on**. So the instruction surfaces
— the ones where the detector genuinely earns its place — are clean, and the
detector stays live there.

Note the figure moved from **79 to 80** and the file count from 140 to 141
between two runs inside a single session, as a sibling session landed a file.
Neither number is carried forward; both are re-measured at the implementing
commit.

### What the reviewer should attack

Not the numbers — the mechanism, twice over now:

1. **Is the role list complete?** It is an enumeration, and an enumeration of
   instruction surfaces is exactly the kind of list that goes stale when a new
   agent-loaded file appears. What happens to a *new* instruction surface nobody
   adds to the list? It defaults to prose and loses URL detection **silently**.
   That is the same failure shape as the defect this revision corrects, one level
   up, and it is the strongest objection available.
2. **Does `egress` really cover the prose class?** `egress` needs an exfiltration
   verb *near* a destination. A bare hostile URL in `dev/` prose, with no verb,
   is flagged by neither detector under this change. The original section argued
   no coverage was lost; that argument is narrower than it sounded, and the
   residual gap should be named in the runner's docstring rather than left for a
   reader to discover.

## Review -- Codex (External Security Review) -- 2026-08-05

**Tier**: External

**Findings**: raised

**Recommendation: REVISE.** Revision 1 correctly withdraws the cross-tree
classifier. The replacement still defaults an unknown role to the less
protective class, and the runner has two independently reproduced Git-input
channels that its current trust statement does not account for.

### Reproduction

Re-run under `/Users/kendal30/conda_envs/lhm/bin/python3.13` (3.13.13), at
`9bf3524`, using `audited_text_files()` for the file set and the shipped scanner
and allowlist for findings. The current corpus is **82** files, not 141: 4 known
instruction files, 77 known prose files, and 1 unknown file (the roots manifest
itself). As shipped, URL scanning produces **53** findings, all
`suspicious-url`; the proposed enumeration produces 0. The figures in the
proposal were snapshots, not invariants, and should not be carried forward.

The behavioral probes also reproduce the named residual: a bare
`https://evil.example/x` in prose produces no finding with `scan_urls=False`,
while the same destination preceded by a supported transfer verb still
produces `egress`.

### Findings

**[S1 -- important, blocking] Unknown roles fail open.** The proposed
classification enumerates instruction surfaces and therefore makes every new,
misspelled, or otherwise unrecognized path prose. That silently disables URL
detection on the exact future surface the classifier did not anticipate.

Remediation: enumerate the narrower exception instead. Known discussion roots
(`dev/**` and `docs/**`) may use `scan_urls=False`; every other role, including
unknown files, uses `scan_urls=True`. Pin an unknown synthetic path and the
roots manifest in tests. The cost is deliberate: a newly added prose root may
produce URL noise until it is explicitly classified. That visible maintenance
cost is preferable to silently losing a detector on a new agent-loaded file.

**[S2 -- important, pre-existing] Ambient Git environment can redirect the
audited set.** At `templates/modules/team-gated/content_scan_runner.py:172`,
`_git_tracked()` inherits the process environment. With `GIT_DIR` pointed at a
second repository, I observed `_git_tracked(repo_a, ["dev"])` return
the alternate repository's path rather than the target repository's path. The
call's argv roots are **TRUSTED-INPUT** under the v1 self-audit model; its
ambient `GIT_*` environment is **USER-CONTROLLED** process input. An altered
environment can therefore shrink or redirect the set before role classification
occurs.

Remediation: use one runner-local Git launcher that drops every ambient
`GIT_*` key, restores only the values it deliberately needs, disables relevant
execution-bearing repository config, and resolves/reports the Git executable
once. This is a pre-existing runner defect rather than a consequence of role
classification; it may be repaired here or routed to a named security record,
but it should not remain implicit.

**[S3 -- important, pre-existing] Manifest roots are accepted as Git options.**
The same call constructs `git ls-files -z *roots` without an option terminator,
while `load_audit_roots()` permits a relative root beginning with `-`. In a
temporary repository, a manifest root of `--others` made
`audited_text_files()` include an untracked `untracked.md`, contradicting its
git-tracked-set contract. The manifest is **TRUSTED-INPUT**, so this is not an
untrusted-PR injection claim; it is an unsafe parser/subprocess composition on
trusted policy with no stated rationale.

Remediation: reject leading-dash roots and pass `--` before pathspecs. Test the
rejection. Both controls are cheap and make the parser's path grammar match the
subprocess grammar.

**[S4 -- important] The prose blind spot must be part of the contract.** A bare
hostile URL in known discussion prose is detected by neither `suspicious-url`
nor `egress`. This is acceptable in the present self-audit, human-review threat
model: prose legitimately carries citations, and the scanner is a witness, not
a proof. The runner docstring and a regression must nevertheless state and pin
that exact residual; “egress covers the prose threat” is too broad.

### Six-boundary walk and input triage

* **Deserialization -- not applicable.** No object-bearing format is loaded.
  The dynamic import at `content_scan_runner.py:358-363` executes the shipped
  scanner as **TRUSTED-INPUT** apparatus, which is acceptable under the stated
  v1 model and must not be represented as containment.
* **Subprocess invocation -- applicable.** `_git_tracked()` uses `shell=False`,
  but combines **TRUSTED-INPUT** manifest roots with **USER-CONTROLLED** ambient
  Git environment. Findings S2-S3 apply.
* **Parsing -- applicable.** The roots manifest, residual baseline, URL
  allowlist, and scanned repository text are all **TRUSTED-INPUT** in this
  self-audit design. Sentinel, containment, and malformed-input refusals are
  sound; role parsing needs S1, and path-to-argv parsing needs S3.
* **File/path handling -- applicable.** Roots and audited files are
  **TRUSTED-INPUT**. Absolute paths, `..`, symlink escapes, non-regular files,
  and size budgets are refused. The manifest's self-inclusion is useful drift
  evidence, but it cannot authenticate a hostile manifest that also narrows the
  roots or changes the apparatus; that limitation is accurately accepted by
  the v1 trusted-apparatus threat model.
* **Network I/O -- not applicable.** The scanner lexically recognizes URLs but
  performs no fetch.
* **Credentials/environment -- applicable.** No credential is read or logged.
  Ambient Git variables are **USER-CONTROLLED** and security-relevant; S2
  applies. The allowlist and baseline are **TRUSTED-INPUT** policy, not secrets.

### Cross-caller ruling

Revision 1's separation is correct. `scripts/check_cairn.py` must retain its
private Cairn-source-layout predicate; the adopter runner must own its role
mapping. No detector code needs to move. Require focused tests proving
`check_cairn.py` still applies URL scanning to `templates/**` and the runner
applies the fail-closed role rule above. With that separation, the proposed
runner change cannot alter Cairn's existing caller behavior.
