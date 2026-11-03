# Check instruction changes before merging a pull request

**Author**: Claude Opus 5.5 (Strategy)
**Status**: awaiting-decision
**Review**: usual
**Proposed tier**: light -- one merge-time step in two documents; the Decision can raise it, because one document is a shipped module
**Plan review**: not required(no plan: light tier)
**Opened**: 2026-11-03
**In brief**: Before merging a pull request that changes files agents load, scan the changed files with your own scanner, then judge what agents following the new text would do differently.

## Decision summary

A pull request can change the files agents load as instructions: templates,
`AGENTS.md`, skills and `dev/`. A hostile or careless change there reaches
every agent that reads it. Today nothing tells the person merging a pull
request to check those changes.

This proposal adds one step for whoever merges a pull request that touches
those files:
1. Run the content scan on the changed files, using the scanner from your own
   checkout.
2. Judge the logical outcome: what an agent following the new text would do
   differently.

An optional reviewer agent with no tools may draft that outcome summary. A
person decides.

Nothing runs during your own development, before a push, or on every commit.

Maintainer direction (chat, 2026-11-03), verbatim:

> "if I'm developing here I don't need to scan for prompt injection changes.
> But when I merge a PR, yes. But DON'T add mandatory scans before pushes"

> "Also, should having a content scan review the actual changes themselves,
> not just some malicious pattern?" ... "For instance, the logical outcome of
> the change"

## Context

- **No merge step.** `CONTRIBUTING.md` covers preparing and opening a pull
  request, but not merging one.
- **The scanner exists and already covers untrusted text.**
  `templates/modules/team-gated/content-security.md` (shipped) tells
  adopters to scan "PR diffs, pasted specs, vendored docs" with
  `python scripts/content_scan.py <files>` before an agent reads them.
- **The module also says use your own copy.** It warns:

  > "Do not wire it into untrusted-PR / fork CI -- a run from an attacker's
  > checkout executes the attacker's scanner."

- **Patterns are not outcomes.** The scanner flags known shapes, such as
  override phrases, send-to-URL wording and hidden Unicode. Its own text
  calls it "a tripwire, not a proof". A plainly worded change can still alter
  what agents do. For example, a template sentence saying reviews may be
  skipped for small security changes matches no pattern.
- **Release is already covered.** `bootstrap/security_check.py` runs the
  whole-tree scan (`check_cairn`) at release; it takes about 1 s. This
  proposal does not change that.

## Proposal

1. **`CONTRIBUTING.md` gains "Merging a pull request"**, for whoever merges,
   when a pull request changes agent-loaded or guarding files:
   - **Instruction files:** `AGENTS.md`, `CLAUDE.md`, `VENDOR.md`,
     `RULES.md`, `templates/`, `.agents/skills/`, `dev/` and `docs/`.
   - **Guarding files:** `bootstrap/tests/`, `scripts/`, and the scanner's
     allowlist, baseline and roots files.

   The steps:
   - **Scan with your own tools, without running the pull request.** In your
     own up-to-date checkout:
     1. `git fetch origin pull/<N>/head`.
     2. Write each changed instruction file to a scratch folder with
        `git show FETCH_HEAD:<path>`.
     3. Run your own `python -I scripts/content_scan.py <those files>`.

     Never check out the pull request branch or run its scanner.
   - **New acceptance markers count as hits.** A pull request that adds a
     `cairn-accept` line can hide its own scan hit. Every added marker is
     discussed before merging.
   - **Judge the logical outcome.** Read the changed text and answer: would
     an agent, or a check, following it now
     - skip, shorten or weaken a review;
     - treat something as approved or decided without the Maintainer;
     - run a command, open a URL, or send data it did not before;
     - move authority (roles, fences, permissions, who may push);
     - trust something new (allowlists, baselines, security policy);
     - stop guarding something (a test, a gate, or a scan input that now
       passes when it should fail)?

     For code, tests and scripts, the scan judges nothing: a person reads
     the diff for the last question. Any "yes" is discussed in the pull
     request before merging, even when the change is intended, so the change
     in behavior is on record.
   - **Optional reviewer agent.** A fresh agent started with an empty tool
     list may receive the diff as quoted data and draft answers to those six
     questions. It cannot act on instructions in the diff. Its summary can
     still be manipulated, so a person reads the diff.
2. **The content-security module gains one paragraph** in its Template
   content: the same steps, in adopter-neutral words. Both copies are edited
   together, `templates/modules/team-gated/content-security.md` and
   `dev/modules/content-security.md`, which are byte-identical today.

## Rationale

The merge is the one point where outside text joins the trusted tree. The
pattern scan is cheap and catches the obvious cases. The outcome questions
catch a plainly worded change of behavior, which no pattern can. Your own
development needs neither, because you are the author.

## Alternatives considered

- **Automatic scans in pull-request CI.** Cairn has no CI. The module
  forbids running a pull request's own scanner, and an automatic pass would
  not judge outcomes.
- **Mandatory pre-push or per-commit scans.** The Maintainer ruled these
  out.
- **Pattern scan only.** It misses plainly worded changes of behavior.

## Documentation / doctrine surface

- **Description:** `CONTRIBUTING.md`, the new "Merging a pull request"
  section.
- **Shipped template:** `templates/modules/team-gated/content-security.md`
  and its installed copy `dev/modules/content-security.md`, one paragraph
  each, kept identical.
- **No doctrine change:** `AGENTS.md` and `docs/methodology/` are not
  touched.

## Evidence / verification plan

- **Tests:** run `tools/test_tiers.py for` the three changed files. The
  review found that `test_content_scan.py`,
  `test_default_security_stance.py`, `test_review_stance_in_shipped_files.py`,
  `test_scaffold.py`, `test_security_stack.py` and `test_upgrade.py` name
  them. No test pins the new paragraph.
- **Gates:** claim, link, neutrality and `scripts/check_cairn.py` on both
  files.
- **Trial:** the next merged pull request that touches instruction files
  records the scan result and the six answers in its discussion.
- **Security preflight:**
  - S1: the scanner comes from the merger's own checkout, never from the
    pull request.
  - S2: a test or reviewer confirms the merge text says so.
  - S3: a person runs it at merge.
  - S4: a scan hit or any "yes" leads to discussion before merging.
  - S5: a hostile change that fools both the scan and the reader still
    succeeds. The step narrows that risk; it does not close it.
- **Independent scientific check:** N/A, no scientific assumption touched.

## Signals the change is wrong

- Merges skip the step because it feels heavy.
- The six questions surface nothing on changes that did alter agent
  behavior.
- The reviewer agent's summary is relied on in place of reading.

## Scope delta

**Scope delta**: preserved

## Assurance path

**Assurance path**: high-assurance -- it edits a shipped module, which is a
named high-risk template surface, and `AGENTS.md` makes such surfaces heavy.
Light is proposed because the change is one paragraph of guidance, with no
engine, scanner or check change. If the Decision keeps light, it should say
that reason.

## Review -- Claude Sonnet 5.5 -- 2026-11-03

```
Reviewed commit: 9be60e7e
Target: whole proposal
Prior findings: none
Assurance path: high-assurance
```

**Tier**: usual
**Findings**: raised
**Verdict**: REVISE

**Elapsed**: about 12 minutes
**Tokens**: about 90,000 (estimated)

**Foundations**
1. **Should this happen as framed?** Yes. Nothing covers the merge point, and a person-run step stays within the quoted direction.
2. **Best alternative.** Doing nothing loses the only check on plainly worded behavior changes; the outcome questions are the real value, the scan secondary.
3. **What would show it wrong.** A PR that passes the scan by its own hand. Measured: `scan_text` flags an override line, but with `<!-- cairn-accept: imperative-override reason="x" -->` above it the hit vanishes (`scripts/content_scan.py` lines 128-137, 343).

**Findings** (none blocking)
- F1. A PR can silence its own hits with inline markers. Close: any added `cairn-accept` line counts as a "yes" for discussion.
- F2. "Scan the PR's versions" is not yet doable. Close: name the steps -- `git fetch origin pull/N/head`, `git show FETCH_HEAD:<path>` into a scratch folder, `python -I scripts/content_scan.py`; never check out the PR branch.
- F3. The path list omits `CLAUDE.md`, `VENDOR.md`, `RULES.md`, `docs/` and what makes checks stop guarding: `bootstrap/tests/`, `scripts/`, allowlist and baseline files. Close: add them; say text scanning cannot judge code.
- F4. Reviewer agent: sound if started with an empty tool list; say so.
- F5. `AGENTS.md` says named high-risk surfaces, templates included, trigger heavy. Light is defensible (one paragraph, no engine); the Decision should say so with its reason.
- F6. No test pins the new paragraph (`test_security_stack.py:349` pins other strings in `dev/modules/content-security.md`). That copy is byte-identical to the template; edit both or they drift.

**Coverage**: I ran no test and did not scan a real PR.

## Response -- Claude Opus 5.5 -- 2026-11-03

All six findings accepted; operative text revised in place.

- **F1 (self-hiding hits):** a newly added `cairn-accept` line is treated
  as a hit and discussed before merging.
- **F2 (concrete scan):** named steps: fetch the pull request ref, write
  files out with `git show`, then run your own scanner with `python -I`.
  Never check out the branch.
- **F3 (paths):** `CLAUDE.md`, `VENDOR.md`, `RULES.md` and `docs/` are
  added, plus the guarding files: tests, scripts, and scan allowlists and
  baselines. A sixth question asks whether something stops guarding. The
  text says the scan cannot judge code.
- **F4 (reviewer agent):** started with an empty tool list.
- **F5 (tier):** the Assurance path now states why light is proposed and
  asks the Decision to record that reason.
- **F6 (two copies):** both module copies are edited together. The test
  list now names the six files the review found.

**Elapsed**: about 10 minutes. **Tokens**: unknown.

### Withdrawn / superseded commitments

- The five-question list, superseded by six questions (F3).
- "One paragraph in the shipped module", superseded by both copies (F6).
