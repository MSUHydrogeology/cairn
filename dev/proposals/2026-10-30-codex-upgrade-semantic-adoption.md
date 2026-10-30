# Require a decision on clean customized policy merges

**Author**: Codex GPT-6.1 Sol (Strategy)
**Status**: revising
**Review**: usual + Security Review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-30
**In brief**: An upgrade should show when a customized policy file merges cleanly and require its owner to decide whether the new upstream rule was adopted.

## Context

The upgrade already labels a clean merge of a locally edited file
`clean-locally-modified` (`bootstrap/_scaffold/upgrade.py:806-824`) and
advances it automatically. A clean text merge can still carry incompatible
policy. Reproduction through the real `merge_file` entry point: start with
“every change gets review” and “Owner: maintainer”; let the adopter change
the first line to “local lead decides review” and upstream change the
separated owner line to “Owner: security lead.” The result is `clean` and
contains both statements. The merge resolved text placement, not authority.
This is the distinct gap queued as issue #35 in `dev/PLANNING.md`; the
current install-integrity plan protects merge ancestors, not policy adoption.

## Proposal

For a mergeable Markdown file where both the adopter and upstream changed
content since the saved base, keep the clean merged preview but do not let
`--apply` silently advance that file or its base. Report the old, local,
upstream and merged text as a review surface. To complete the upgrade for
that file, require a named-path disposition: either accept the preview after
checking that the upstream change is incorporated, or retain a deliberate
local policy and record that exception. A blanket acknowledgement across all
files cannot clear these decisions. Other files may advance independently;
an unresolved file stays pending and keeps its old base.

Use the existing `clean-locally-modified` classification and stage report.
The plan should fit the path-scoped disposition into the existing stage/apply
and finalize commands where their current contracts allow it; if those
commands cannot express both choices without ambiguity, add the smallest
explicit path-scoped form. Do not claim a text or keyword scanner can decide
whether policy meanings agree. Preserve verbatim-file, untouched-file,
conflict, and ordinary adopter-only edit behavior.

## Rationale

The tool already knows the relevant provenance: old base, adopter bytes and
new upstream bytes. Requiring a decision only when both sides changed one
mergeable file uses that evidence without pretending to understand policy.
It costs one human review per such file, not another review for every upgrade
file. The existing “review all merged files” prose in `bootstrap/UPGRADE.md`
does not make an omitted upstream rule visible before `--apply` advances.

## Alternatives considered

Do nothing keeps the measured clean-merge gap. Block every locally edited
file, even when upstream did not change it, imposes review without new
policy to adopt. Scan for changed rule words is brittle and can pass a
paraphrase. Reuse a single blanket `--ack-review-only` flag is cheaper but
does not record which policy file was read or what was decided.

## Documentation / doctrine surface

Update descriptive `bootstrap/UPGRADE.md` and the upgrade command help to
explain the per-file hold and both dispositions. No doctrine change is
proposed. The proposal and plan remain in `dev/`.

## Evidence / verification plan

### Tests required

In `bootstrap/tests/test_upgrade.py`, use a real installed old base and
changed upstream template to prove the conflicting-policy example holds the
affected file through public `--plan`, `--stage` and `--apply`. Exercise
each named disposition, stale staged bytes, retry, and an unrelated file
advancing. Controls: untouched files, adopter-only edits, conflicts,
verbatim files and a clean merge whose upstream change is accepted. Search
callers of the changed classification and add their owning tests. At Boundary
B, use a wide change-specific run for the engine contract and its public
paths; certification remains separate.

### Examples / smoke checks

Run the public scaffold upgrade commands on a disposable old install, and
`python scripts/check_cairn.py` for changed prose. The current direct
`merge_file` reproduction is a positive control for the semantic gap,
not proof that the proposed disposition works. No full suite per change.

#### Security preflight — five questions, answered in writing

* **S1.** The saved base and new template come from Cairn's selected source;
  adopter bytes, lockfile and disposition path come from the target/operator.
  The target can name the file being judged, so admission must bind it to
  that file's stage evidence.
* **S2.** Deliberately remove the hold or swap the acknowledged path in a
  scratch copy; the public tests above must fail. These mutations await an
  implementation to break, so they have not yet been run.
* **S3.** `bootstrap/scaffold.py upgrade --plan/--stage/--apply` fires the
  check over mergeable tracked Markdown files changed on both sides. The help and
  `bootstrap/UPGRADE.md` must state that exact trigger and hold; the plan
  compares those words with public-command tests.
* **S4.** Unknown disposition, changed stage evidence, unreadable base or
  missing file keeps that file pending; a parse or path error grants no
  authority to advance.
* **S5.** A malicious adopter can lie in its own policy text or deliberately
  approve a harmful choice. This change prevents an unnoticed advancement,
  not a knowingly bad decision.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

An ordinary customized upgrade now requires decisions on files with no
upstream change; a pending policy file advances its base; a path disposition
can be reused for different bytes; or a real policy conflict still disappears
behind a clean status.

## Scope delta

**Scope delta**: preserved.

## Assurance path

**Assurance path**: high-assurance — scaffold engine and install contract.

## Review -- Codex GPT-6.1 Sol (Reviewer) -- 2026-10-30

```
Reviewed commit: 6a40450b2c0d0bf0a8c1db7d3beb357f625bac63
Target: opening proposal, Context through Assurance path
Prior findings: none
Assurance path: high-assurance
```

**Tier**: usual
**Findings**: raised
**Verdict**: REVISE

**Foundations**

1. **Should this happen as framed?** Yes to a decision on clean merges of policy changed on both sides: the merge can settle placement without settling meaning. The framing needs a precise trigger and a defined result for the deliberate-local choice -- proposal lines 15-33; `bootstrap/_scaffold/upgrade.py:801-824`; `bootstrap/_scaffold/upgrade.py:3572-3640`.
2. **Best alternative.** Do nothing plus the existing instruction to review merged files costs no engine change, but leaves the known omission silent. The simpler viable build is a per-path, stage-bound decision using the existing classification and report, with only the state needed to make both decisions durable -- `bootstrap/UPGRADE.md:190-232`; `bootstrap/_scaffold/upgrade.py:1381-1410`; `bootstrap/_scaffold/upgrade.py:3804-3807`.
3. **What would show it wrong.** Withdraw this design if the public-command test cannot distinguish a stock install with no upstream change from a true two-sided policy change, or if either decision loses its meaning on the next upgrade -- `bootstrap/tests/test_upgrade.py:765-793`; `bootstrap/_scaffold/upgrade.py:3572-3640`.

The strongest case is that the operator, rather than a text merger, must decide whether a policy change is acceptable. The existing stage is already a place to see the merged text; the new cost is justified only for files where upstream actually brought a change to consider.

**R1 (blocking): Make the two-sided trigger an explicit invariant.** `clean-locally-modified` means the adopter's file differs from the substituted old base; the classifier does not also require the new upstream template to differ from that base (`bootstrap/_scaffold/upgrade.py:806-824`). The existing test finds even a stock installed `AGENTS.md` in that class because install-time module assembly is absent from its cached base (`bootstrap/tests/test_upgrade.py:765-793`). Holding every file with this label would impose decisions with no new policy, contrary to proposal lines 25-26 and 46-49. Specify how the old and new *materialized* policy views are compared, while keeping the existing class for reporting. Close with public-command tests for an actual two-sided edit, an adopter-only edit, a stock assembled file, and a profile-only sizing change.

**R2 (blocking): Define what each disposition records and what a later upgrade sees.** The proposal promises both an accepted preview and a deliberate local exception, while a pending file keeps its old base (lines 25-33). Today `--apply` advances the global Cairn commit and changes a file's base only when its staged content is applied; other records carry over unchanged (`bootstrap/_scaffold/upgrade.py:3572-3640`). If a local exception retains that old base, the same upstream change is offered again; if it advances the base, the next run may no longer show the rejected upstream rule. State which bytes and decision evidence are recorded for each outcome, whether the exception remains visible later, and how pending differs from deliberately retained after a sibling advances. Close with a two-upgrade test for each outcome and a retry after a sibling applied.

**Coverage**: Claims and design (#1, #3) -- classifier and lock update cited in R1/R2; public path (#2) -- `bootstrap/tests/test_upgrade.py:765-793` currently probes classification, and proposal lines 70-78 call for public commands; silent failure (#4) -- `bootstrap/_scaffold/upgrade.py:3372-3380` shows the current blanket review-only override; cross-document and drift (#5, #6) -- `dev/PLANNING.md:115`, `bootstrap/UPGRADE.md:190-232`, and `bootstrap/UPGRADE.md:283-315`; lifecycle (#7) -- proposal lines 25-38 place the decision at upgrade; domain and scope (#8) -- stock assembled file in R1; satisfiers (#9) -- the tests and contract wording named in R1/R2. **Not covered / low confidence**: I did not run an installed-project reproduction or inspect every lockfile consumer; this is a read of the committed proposal and current production paths, not implementation verification.
