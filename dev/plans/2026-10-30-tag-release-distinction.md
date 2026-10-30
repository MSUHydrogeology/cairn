# Plan: Check GitHub Release publication separately from the tag

**Source proposal**: dev/proposals/archive/2026-10-30-codex-tag-release-distinction.md
**Author**: Codex GPT-6.1 Sol (Implementation plan author)
**Status**: revising-code
**Waiting on Maintainer**: disposition of Security P1
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-30
**In brief**: Add a read-only publication check and make the release guide distinguish publishing a Release from pushing its signed tag.

## Source proposal

The accepted proposal requires create-or-edit publication, notes and source-link
inspection, an independent gate-commit comparison, and signed tags. Its Decision
authorizes implementation, not a live release.

## Scope

Change `docs/release-process.md` and add a standard-library-only internal
publication checker `scripts/check_release_publication.py` and owning tests
`bootstrap/tests/test_check_release_publication.py`. No stored state or
publishing credentials.

**Reuse.** Search `rg --files scripts tools | rg 'release|tag|publish|github'`
found `scripts/bootstrap_github_labels.py`, which mutates labels, not Release
state. No existing publication checker was found. Search
`rg -n 'release-process|check_release_publication' bootstrap/tests scripts tools
--glob '*.py'` found no readers; repeat before implementation and check byte
pins. Read `bootstrap/DEPENDENCY_BUDGET.md` before imports.

### Documentation / doctrine surface

`docs/release-process.md` describes the cut; deliberation stays here. No doctrine
or adopter-template change. Preserve the provenance ceremony in
`bootstrap/PROVENANCE.md`; the checker supplements it.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Checker, command fixtures and guide | Both plan-review obligations closed | Script, tests and cut instructions |
| C2 | Final-commit verification and independent code reviews | C1 committed; wide verification complete | Evidence and usual plus separate Security Review |

No chunk performs the live cut. No re-anchor, push, signature creation or
publication is included.

## Acceptance criteria

### C1

The public command accepts `--repository OWNER/REPO --tag TAG
--expected-commit FULL_SHA`; expected identity never comes from Release metadata
or a local ref. Exit 0 requires a published matching Release and exactly one
remote annotated-tag ref plus one matching peeled ref. Draft, absent, wrong-tag,
wrong-commit, missing/duplicate/ambiguous refs, malformed replies and read failures
exit nonzero with an explanatory diagnostic. Success names only publication
state and remote identity. The guide requires a signed tag on the gate-checked
commit, create-or-edit publication, notes inspection and opening source links;
it states that these do not verify cached archive bytes and prescribes no
force-push or metadata edit as archive repair.

### C2

Wide Boundary B evidence covers the final implementation commit. Independent
usual and Security code reviews inspect that commit and falsify its trust
inputs. Unmet criteria remain open. No scientific check applies.

**Security preflight changes.** S1, S4 and S5 retain the accepted answers.
S2 refusal cases run through the public command in C1. S3 is the documented
post-publication command above, supplied the independently recorded gate SHA.

## Scope delta

**Scope delta**: preserved. No outcome removed or deferred.

## Verification

**Protocol.** Validate OWNER/REPO as two safe GitHub path components, validate a
full 40-hex GitHub commit id, and reject invalid Git tag names before reads.
Use HTTPS GET `https://api.github.com/repos/OWNER/REPO/releases/tags/TAG`,
percent-encoding TAG as one path component, with GitHub JSON Accept header and
no Authorization. Require a JSON object, exact tag_name, boolean draft=false
and nonempty published_at. Reject failed status, malformed types, excessive
response size, timeout and transport failure. Bound the response to 1 MiB and
the read to 30 seconds; do not accept redirect to another host.

Invoke Git without a shell:
`git ls-remote --exit-code --tags https://github.com/OWNER/REPO.git
refs/tags/TAG refs/tags/TAG^{}`. Parse tab-separated full object ids and exact
ref names; reject extra or duplicate records, absent peeled ref or commit
mismatch. Do not use --refs, which suppresses peeling. Bound the subprocess to
30 seconds, disable terminal prompts, and never fall back to local refs or
Release target_commitish. The public interface accepts no alternate remote or
API host.

**Git isolation.** Reuse the closed-environment approach in
`scripts/content_scan_runner.py`, not its audit-specific interface. Resolve the
host Git executable once; run it from a fresh non-repository temporary directory.
Construct a new child environment admitting only PATH and Windows SYSTEMROOT
where needed, plus explicit controls: GIT_CONFIG_NOSYSTEM=1,
GIT_CONFIG_SYSTEM and GIT_CONFIG_GLOBAL set to the null device,
GIT_TERMINAL_PROMPT=0 and GIT_CEILING_DIRECTORIES at the temporary directory's
parent. Inherit no other GIT_*, HOME/XDG, proxy or transport environment.
Prefix the command with `-c protocol.allow=never -c protocol.https.allow=always
-c http.followRedirects=false -c credential.helper=`. No ambient repository,
global, system or injected command configuration may rewrite the URL, select
another transport or supply credentials. Host Git and system TLS trust remain
trusted inputs; this is not executable authentication.

Tests may isolate transports through child-process fixtures without
adding a production bypass. Protocol sources: [GitHub Release API](https://docs.github.com/en/rest/releases/releases#get-a-release-by-tag-name)
and [Git ls-remote](https://git-scm.com/docs/git-ls-remote).

**Boundary A mapping.** Run
`python -m pytest bootstrap/tests/test_check_release_publication.py` for all C1
invariants and public-command fixtures, using local annotated Git refs and
stubbed Release replies. Cover malformed fields, missing publication date,
lightweight tags, duplicate refs, timeouts, unsafe inputs, encoded tag names,
redirect refusal and help/usage as well as accepted negative cases. Add a
public-command fixture with a matching substituted repository and hostile
insteadOf in repository/global/system and GIT_CONFIG_* inputs: it must refuse
or reach the intended HTTPS URL, never accept the substitute. Cover ambient
proxy, helper and redirect settings; inspect the child environment. Confirm real
ls-remote against local refs; no live network required.

For the guide and this plan run `python scripts/claim_check.py PATH`,
`python scripts/link_check.py PATH`, and `python scripts/check_cairn.py PATH`.
Run `python scripts/quality_gate.py --sub neutrality`. Search readers and byte
pins with the known-positive `bootstrap/PROVENANCE.md` control; add any discovered
owning checks before implementation. Inspect snippet markers; if present,
change their source and run `python scripts/sync_doc_snippets.py`.

**Boundary B: wide.** After the final implementation commit, repeat the mapped
owning test family, public-command fixtures and standing gates on a separate
clean copy under canonical Python 3.13.x. Record SHA/range, interpreter path and
version, clean unchanged pre/post state, command exits and counts, elapsed time,
tokens or unknown, non-pass dispositions and omissions. Record
`Certified by: pending`. No full suite or re-anchor is authorized.

**Boundary C.** Fresh reviewers inspect committed bytes and the verification
record, independently attack mismatched trust inputs and refusal behavior, and
record a falsification ledger plus Bounding verdict. They do not rerun Boundary
B. Any mutation report names its unmutated control, total, killed, survivors
and measured equivalents. Live GitHub, archive contents and tag-signature
verification remain outside this helper's coverage.

Plan authoring: about 6 minutes; tokens unknown. Verification is recorded in
opening commit af0fb7ba.


## Plan review -- Codex GPT-6.1 Sol (Reviewer) -- 2026-10-30

```
Reviewed commit: af0fb7ba24e2d71af641dbcc89496daae0738ec9
Target: opening plan and accepted proposal
Prior findings: none
Assurance path: Internal + Internal Security Review
```

**Obligation**: Internal
**Tier**: Internal
**Findings**: none
**Verdict**: advance after the separate Security Review and author response.
**Elapsed**: approximately 3 minutes. **Tokens**: unknown.

**Foundations**:

1. **Should this happen as framed?** Yes: the plan retains the independent gate commit, publication and signed-tag requirements, and bounds the archive claim -- source proposal Proposal; plan C1.
2. **Best alternative.** Manual comparison avoids a helper but repeats checks at every cut; the read-only command preserves the accepted outcomes without publication credentials -- source proposal Alternatives; plan Protocol.
3. **What would show it wrong?** A draft Release or wrong peeled commit passing the public command would defeat the accepted check -- source proposal Tests required; plan Boundary A mapping.

The plan names both remote inputs, refusal cases and public-command fixtures, and keeps the human publication and notes checks. It preserves the signed-tag contract without claiming that source links establish archive contents. The wide verification map names the new test family and prose gates; the live cut remains outside this work -- plan C1, Protocol and Boundary A/B; `bootstrap/PROVENANCE.md:398-407`.

**Covered**: accepted outcomes and scope, trust inputs, failure cases, verification mapping, documentation placement and lifecycle sequencing -- source proposal Proposal and Tests required; plan Scope, Sequence and Verification. **Not covered**: no implementation, live GitHub response, tag signature, archive contents or Security Review.

## Plan review -- Codex GPT-6 (Security Reviewer) -- 2026-10-30

```
Reviewed commit: af0fb7ba24e2d71af641dbcc89496daae0738ec9
Target: protocol, trust inputs, refusal cases and verification mapping
Prior findings: none
Assurance path: high-assurance
Elapsed: about 3 minutes; tokens: unknown
```

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: raised
**Verdict**: REVISE

**Foundations**:

1. **Should this happen as framed?** Yes, once the remote read is bound to the intended host: the accepted check compares the independently supplied gate commit with the published tag and does not claim archive identity. -- source proposal Proposal; plan C1 and Protocol.
2. **Best alternative.** Keep the read-only helper and human publication inspection, while isolating Git configuration for the remote query; manual comparison alone leaves the accepted repeatable check unmet. -- plan Protocol; `scripts/content_scan_runner.py:222-224`.
3. **What would show it wrong?** A draft, malformed response, or a matching tag from a different repository passing the public command would defeat its publication or remote identity claim. -- plan C1 and Boundary A.

**P1 (blocking) — Git can rewrite the fixed remote.** The Protocol fixes the URL and disables terminal prompts but does not isolate Git configuration. Git's `url.*.insteadOf` can redirect that URL: `git -c 'url.file:///private/tmp/nonexistent-cairn-review.insteadOf=https://github.com/example/repo.git' ls-remote --exit-code --tags https://github.com/example/repo.git refs/tags/v1 'refs/tags/v1^{}'` tried the local path. A matching substituted repository could falsely establish the remote tag identity at a release cut. Specify a configuration/environment boundary that prevents URL rewriting and other transport redirection, and add a public-command negative fixture that supplies a matching substituted ref and requires refusal or the intended GitHub read. Preserve bounded, credential-free reads.

**Covered:** claims and production path (plan Protocol and command probe); completeness and failure direction (C1 and P1); consistency and reuse (`bootstrap/PROVENANCE.md:398-407`, `scripts/content_scan_runner.py:222-224`); drift and lifecycle (source Decision and plan Sequence); domain and scope (no scientific result, no live cut); satisfier (P1). **Not covered:** implementation, live GitHub, archive bytes, signature verification, or full suite.


## Response to plan review -- Codex GPT-6.1 Sol -- 2026-10-30

| Finding | Disposition |
|---|---|
| Internal review, no findings | Retained the accepted protocol and mapped outcomes. |
| Security P1 at 32008d9b | Accepted. Verification > Git isolation now excludes ambient repository/global/system and environment configuration, disables redirects and credentials, and limits transport to HTTPS. Boundary A adds the matching-substitute public-command regression and hostile configuration inputs. |

The one-pass review fold is complete; status is ready-to-implement. Scope is
preserved. Host Git and system TLS remain trusted; no new authentication claim
is made. Implementation must measure the isolation and regression, which this
plan response has not run.

**Elapsed**: about 3 minutes. **Tokens**: unknown.

## Implementation verification -- Codex GPT-6.1 Sol (Implementation) -- 2026-10-30

**Boundary B mode**: wide. The checker binds the GitHub Release API result and
GitHub's annotated-tag ref to an independently recorded gate commit. The
public-command fixture family, user guide, and prose gates were covered; a
narrower run would not cover the remote trust inputs and public path.

**Certified by**: pending.
**Tested commit**: `85a8af1cfdd1de273fe2e00242efe360c44b8e5a`.
**Reviewed range**: `9d7f0cd20859eeceb01ba25606c1565a7d5fbe92` through `85a8af1cfdd1de273fe2e00242efe360c44b8e5a`.
**Interpreter/runtime**: `/Users/kendal30/conda_envs/lhm/bin/python3.13`, Python 3.13.13, pytest 9.0.3, macOS.
**Pre-run state**: clean detached checkout at the tested SHA.
**Post-run state**: clean detached checkout at the same SHA; `git status --short` empty and `git rev-parse HEAD` unchanged.

| Command | Exit | Outcomes | Elapsed | Tokens |
|---|---:|---|---:|---|
| `python -m pytest bootstrap/tests/test_check_release_publication.py` | 0 | 30 passed; 0 failed, skipped, xfailed or xpassed | 0.70 s | unknown |
| `python scripts/claim_check.py dev/plans/2026-10-30-tag-release-distinction.md` | 0 | no flags after removing the resolved `Proposed paths` declaration | under 1 s | unknown |
| `python scripts/claim_check.py docs/release-process.md` | 0 | no flags | under 1 s | unknown |
| `python scripts/link_check.py` on the plan and guide | 0 | both passed; one Markdown file each; plan reports 2 external links not probed | under 1 s each | unknown |
| `python scripts/check_cairn.py` on the plan and guide | 0 | both passed; one Markdown file each; plan reports 2 external links not probed | under 1 s each | unknown |
| `python scripts/quality_gate.py --sub neutrality` | 0 | fail=0, info=43 | 0.85 s | unknown |
| Reader and snippet search; positive-control `PROVENANCE.md` search | 0 | one owning test reference; 6 positive-control matches; no snippet markers in the guide | under 1 s | unknown |

**Non-pass disposition**: none in the final candidate. The first plan prose-gate
run found two stale forward-reference declarations; those resolved paths were
removed and all plan prose gates passed on the corrected candidate.
**Plan-specific acceptance commands**: no live GitHub request, Release
publication, tag-signature check, archive-byte check, full suite, or re-anchor
was run; these remain outside this implementation check or explicitly
unauthorized. The snippet-sync command was not needed because the guide has no
snippet markers.
**Known omissions**: live GitHub state and cached archive contents are not
verified by this helper; Release notes and source links remain a human review.
Elapsed implementation verification was about 2 minutes; token use unknown.

## Code review -- Codex GPT-6.1 Terra (Reviewer) -- 2026-10-30

**Reviewed commit**: `85a8af1cfdd1de273fe2e00242efe360c44b8e5a`; verification record `147128ea`.
**Obligation**: Internal. **Tier**: Internal. **Verdict**: REVISE.
**Elapsed**: approximately 4 minutes. **Tokens**: unknown.

**Foundations**:

1. **Should this happen as framed?** Yes: the guide separates publication from the signed tag and the checker compares the remote peeled ref with the independently supplied gate SHA (`docs/release-process.md`, The cut; checker `_parse_remote_refs`).
2. **Best alternative.** Retain the read-only helper with a total response deadline; manual checking would lose the accepted repeatable comparison (plan C1 and Protocol).
3. **What would show it wrong?** A misleading Release or substituted tag passing, or an unbounded remote read, would defeat the check (plan Protocol; finding below).

**P1 (blocking) — API read lacks the required total time bound.** `_fetch_release` passes 30 seconds to `opener.open` and then calls `response.read` without a deadline. That timeout limits socket inactivity, not total response time: a peer sending bytes periodically can keep the read open beyond 30 seconds. A local socket-pair probe with a 0.1-second timeout read five bytes sent every 0.06 seconds in 0.32 seconds. The plan requires the read bounded to 30 seconds; enforce and test an overall deadline, including slow-drip input.

**Falsification ledger**: Wrong commit, duplicate and unexpected refs are refused by parser branches; tests exercise each through `main`. The malicious Git configuration fixture demonstrates an effective rewrite control and inspects the isolated child environment, but substitutes the transport for the final read. API timeout falsified as above. Verification record names clean commit, interpreter, mapped checks and omissions; it does not resolve the deadline gap. **Bounding**: WIDER RUN REQUIRED for a slow-drip deadline check after repair.

**Covered**: acceptance and failure direction (C1 and parser); trust inputs and reuse (Git isolation and hostile fixture); drift, consistency and scope (guide and plan); test satisfier and verification record (Boundary B). **Not covered**: live GitHub, archive bytes, signature verification, full suite or separate Security Review. No mutations run.

## Response to code review -- Codex GPT-6.1 Sol -- 2026-10-30

| Finding | Disposition |
|---|---|
| P1: API read lacks a total deadline | Fixed in `a6da3bed`: the checker uses a monotonic deadline and decreases the socket timeout before each bounded response chunk. A slow-drip socket-pair test through the public command passes; Boundary B was rerun on that commit. No clearing review was run. |

## Implementation verification -- Codex GPT-6.1 Sol (timeout correction) -- 2026-10-30

**Boundary B mode**: wide. Commit `a6da3bed` closes the timeout-bound gap by
applying a monotonic deadline to each bounded response-body read. The new public
command socket-pair test exercises the slow-drip refusal path; the full owning
test file and all mapped prose and standing gates were rerun.

**Certified by**: pending.
**Tested commit**: `a6da3bed98d8277d9606b74bc9f5e8db00fd029c`.
**Reviewed range**: `9d7f0cd20859eeceb01ba25606c1565a7d5fbe92` through `a6da3bed98d8277d9606b74bc9f5e8db00fd029c`.
**Interpreter/runtime**: `/Users/kendal30/conda_envs/lhm/bin/python3.13`, Python 3.13.13, pytest 9.0.3, macOS.
**Pre-run state**: clean detached checkout at the tested SHA.
**Post-run state**: clean detached checkout at the same SHA; `git status --short` empty and `git rev-parse HEAD` unchanged.

| Command | Exit | Outcomes | Elapsed | Tokens |
|---|---:|---|---:|---|
| `python -m pytest bootstrap/tests/test_check_release_publication.py` | 0 | 31 passed; 0 failed, skipped, xfailed or xpassed; includes slow-drip public-command refusal | 0.96 s | unknown |
| `python scripts/claim_check.py` on the plan and guide | 0 | both passed; no flags | under 1 s each | unknown |
| `python scripts/link_check.py` on the plan and guide | 0 | both passed; 1 Markdown file each; plan reports 2 external links not probed | under 1 s each | unknown |
| `python scripts/check_cairn.py` on the plan and guide | 0 | both passed; 1 Markdown file each; plan reports 2 external links not probed | under 1 s each | unknown |
| `python scripts/quality_gate.py --sub neutrality` | 0 | fail=0, info=43 | 0.88 s | unknown |
| Reader/pin search and known-positive `PROVENANCE.md` control | 0 | one owning test reference; 6 positive-control matches; no additional byte-pin reader found | under 1 s | unknown |
| Snippet-marker search in the guide | 1 | no markers; synchronization was unnecessary | under 1 s | unknown |

**Non-pass disposition**: none; the zero-match snippet search is expected.
The ordinary review's P1 deadline finding is addressed by `a6da3bed` and the
slow-drip test through `main`; no clearing review was run.
**Plan-specific acceptance commands**: no live GitHub request, Release
publication, tag-signature check, archive-byte check, full suite or re-anchor
was run. Snippet synchronization was unnecessary because the guide contains no
snippet markers.
**Known omissions**: live GitHub state and cached archive contents remain
unverified; Release notes and source links remain a human review. The separate
Security Review is still owed. Elapsed verification was about 3 minutes; token
use unknown.

## Code review -- Codex GPT-6.1 Sol (Security Reviewer) -- 2026-10-30

**Reviewed commit**: `a6da3bed98d8277d9606b74bc9f5e8db00fd029c`; verification `b6cbba57`; handoff `5ab94aaa`.
**Obligation**: Internal Security Review. **Tier**: Internal Security Review.
**Verdict**: REVISE. **Elapsed**: approximately 5 minutes. **Tokens**: unknown.

**Foundations**:

1. **Should this happen as framed?** Yes: independently supplied commit identity and separate publication avoid conflating a tag push with a Release (C1; checker `_check`; guide The cut).
2. **Best alternative.** Retain this credential-free helper with a deadline covering connection and headers too; manual comparison loses the accepted repeatable check (Protocol; `_fetch_release`).
3. **What would show it wrong?** Substituted identity passing or a remote read exceeding its promised bound (C1; Protocol; probe below).

**P1 (blocking) — Headers precede the deadline guard.** `_fetch_release` calls `opener.open` before `_read_release_body`; HTTP response-header parsing still has only an inactivity timeout. In a separate extraction of the reviewed commit, a public-`main` probe substituted a socket-pair opener using real `http.client.HTTPResponse.begin`. With a 0.1-second budget and a header every 0.04 seconds, refusal occurred after 0.346 seconds. This is a remaining pre-body gap, distinct from the repaired body read. Slow headers can exceed the accepted 30-second total bound. Close with a bounded overall request mechanism and a public-command slow-header regression, including connection/header acquisition.

**Falsification ledger**: Python 3.13.13 probes above; wrong peeled commit and unexpected ref both refused; hostile Git environment keys excluded. Inspected Git isolation, redirect refusal, strict Release fields and independent expected SHA. Boundary B names clean final bytes and 31 passing tests; its slow-drip test covers the body only. No implementation suite rerun or mutations. **Bounding**: WIDER RUN REQUIRED for pre-body deadline coverage.

**Covered**: claims/production/completeness/failure (probe, `_fetch_release`); consistency/reuse/drift/lifecycle (guide The cut, Protocol, reader search with `PROVENANCE.md` positive control); scope (C1); satisfier (P1). **Not covered**: live GitHub, archives, signatures, full suite or re-anchor.

## Response to Security Review -- Codex GPT-6.1 Sol -- 2026-10-30

| Finding | Disposition |
|---|---|
| P1: response headers precede deadline enforcement | Fixed in `0ecd4f49`: the fixed HTTPS handler uses a deadline-aware HTTP response parser for status and headers, caps the connection timeout by remaining time, and shares the deadline with body reads. A slow-header socket-pair regression exercises public `main` through real `HTTPResponse.begin`; Boundary B was rerun on the fix. No clearing review was run. |

## Implementation verification -- Codex GPT-6.1 Sol (header deadline correction) -- 2026-10-30

**Boundary B mode**: wide. The correction covers fixed-host connection setup,
HTTP status and headers, and the response body under one monotonic deadline. The
public-command slow-header and slow-body socket-pair fixtures, owning test file,
user guide and standing gates were rerun.

**Certified by**: pending.
**Tested commit**: `0ecd4f49bed89e2811b6de437ff7802087c46a09`.
**Reviewed range**: `9d7f0cd20859eeceb01ba25606c1565a7d5fbe92` through `0ecd4f49bed89e2811b6de437ff7802087c46a09`.
**Interpreter/runtime**: `/Users/kendal30/conda_envs/lhm/bin/python3.13`, Python 3.13.13, pytest 9.0.3, macOS.
**Pre-run state**: clean detached checkout at the tested SHA.
**Post-run state**: clean detached checkout at the same SHA; `git status --short` empty and `git rev-parse HEAD` unchanged.

| Command | Exit | Outcomes | Elapsed | Tokens |
|---|---:|---|---:|---|
| `python -m pytest bootstrap/tests/test_check_release_publication.py` | 0 | 32 passed; 0 failed, skipped, xfailed or xpassed; includes slow-header and slow-body refusal | 1.27 s | unknown |
| `python scripts/claim_check.py` on the plan and guide | 0 | both passed; no flags | under 1 s each | unknown |
| `python scripts/link_check.py` on the plan and guide | 0 | both passed; 1 Markdown file each; plan reports 2 external links not probed | under 1 s each | unknown |
| `python scripts/check_cairn.py` on the plan and guide | 0 | both passed; 1 Markdown file each; plan reports 2 external links not probed | under 1 s each | unknown |
| `python scripts/quality_gate.py --sub neutrality` | 0 | fail=0, info=43 | 0.87 s | unknown |
| Reader/pin search and known-positive `PROVENANCE.md` control | 0 | one owning test reference; 6 positive-control matches; no additional byte-pin reader found | under 1 s | unknown |
| Snippet-marker search in the guide | 1 | no markers; synchronization was unnecessary | under 1 s | unknown |

**Non-pass disposition**: none; the zero-match snippet search is expected.
The Security Review's P1 is addressed by `0ecd4f49` and the slow-header
regression through the public command. No clearing review was run.
**Plan-specific acceptance commands**: no live GitHub request, Release
publication, tag-signature check, archive-byte check, full suite or re-anchor
was run. Snippet synchronization was unnecessary because the guide contains no
snippet markers.
**Known omissions**: live GitHub state and cached archive contents remain
unverified; Release notes and source links remain a human review. Elapsed
verification was about 2 minutes; token use unknown.

## Code review -- Codex GPT-6.1 Sol (Security Reviewer, second pass) -- 2026-10-30

**Reviewed commit**: `0ecd4f49bed89e2811b6de437ff7802087c46a09`; verification `21d14cb8`.
**Obligation**: Internal Security Review. **Tier**: Internal Security Review.
**Verdict**: REVISE; two-pass cap reached, unresolved criterion to Maintainer.
**Elapsed**: approximately 3 minutes. **Tokens**: unknown.

**Foundations**:

1. **Should this happen as framed?** Yes; C1's independent identity and read-only publication check remain useful (`_fetch_release`, `_parse_remote_refs`).
2. **Best alternative.** Run ordinary urllib in a standard-library worker subprocess with a parent timeout and bounded result. This retains the accepted outcomes and can replace the custom header classes and private socket traversal; manual checking loses the repeatable command.
3. **What would show it wrong?** Connection acquisition exceeding the total deadline (Protocol; probe below).

**P1 remains blocking — DNS is outside the deadline.** `_DeadlineHTTPSConnection.connect` sets a socket timeout, but hostname resolution precedes socket operations. In an extraction of this commit, public `main` used real urllib/HTTPS connection code with only `socket.getaddrinfo` replaced by a resolver sleeping 0.35 seconds then failing. A 0.1-second budget refused after 0.358 seconds. Thus the accepted overall bound is still unmet. Close with an enforceable outer deadline covering resolution, connection, headers and body, plus a delayed-resolver public-command regression. The Maintainer must disposition this named unmet criterion at the cap; a future certification does not close it.

**Falsification ledger**: Python 3.13.13 DNS probe above; subprocess timeout control stopped a 0.35-second sleeper after 0.107 seconds with budget 0.1. Inspected new header reader and Boundary B's 32-test record. Subprocess control measured macOS only; Windows startup/termination and a complete worker design remain unverified. No suite rerun or mutations. **Bounding**: WIDER RUN REQUIRED for connection acquisition.

**Covered**: claims/production/completeness/failure (DNS probe, `connect`); consistency/drift/lifecycle/scope (Protocol, correction record, C1); reuse/satisfier (subprocess alternative and P1). **Not covered**: live GitHub, chunk framing, archives, signatures, full suite or re-anchor.

## Response to Security Review -- Codex GPT-6.1 Sol -- 2026-10-30

| Finding | Disposition |
|---|---|
| P1: DNS resolution can exceed the socket timeout | Fixed in `30466f9a`: the API fetch now runs in a fixed-command Python child and the parent enforces a 30-second `subprocess.run` timeout. This covers DNS, connection, headers and body; a delayed-`getaddrinfo` public-command test verifies fail-closed termination. The two-pass Security Review cap is reached; no third or clearing pass was run. |

## Implementation verification -- Codex GPT-6.1 Sol (bounded API worker) -- 2026-10-30

**Boundary B mode**: wide. The final API path bounds the entire worker process,
including hostname resolution, connection, response headers and body. The
owning test family, public command, guide, plan and standing gates were checked.

**Certified by**: pending.
**Tested commit**: `30466f9a4cf34667f4c3210d4a28ccacd3d4e5fb`.
**Reviewed range**: `9d7f0cd20859eeceb01ba25606c1565a7d5fbe92` through `30466f9a4cf34667f4c3210d4a28ccacd3d4e5fb`.
**Interpreter/runtime**: `/Users/kendal30/conda_envs/lhm/bin/python3.13`, Python 3.13.13, pytest 9.0.3, macOS.
**Pre-run state**: clean detached checkout at the tested SHA.
**Post-run state**: clean detached checkout at the same SHA; `git status --short` empty and `git rev-parse HEAD` unchanged.

| Command | Exit | Outcomes | Elapsed | Tokens |
|---|---:|---|---:|---|
| `python -m pytest bootstrap/tests/test_check_release_publication.py` | 0 | 32 passed; 0 failed, skipped, xfailed or xpassed; includes blocked-resolver worker timeout | 0.83 s | unknown |
| `python scripts/claim_check.py` on the plan and guide | 0 | both passed; no flags | under 1 s each | unknown |
| `python scripts/link_check.py` on the plan and guide | 0 | both passed; 1 Markdown file each; plan reports 2 external links not probed | under 1 s each | unknown |
| `python scripts/check_cairn.py` on the plan and guide | 0 | both passed; 1 Markdown file each; plan reports 2 external links not probed | under 1 s each | unknown |
| `python scripts/quality_gate.py --sub neutrality` | 0 | fail=0, info=43 | 0.93 s | unknown |
| Reader/pin search and known-positive `PROVENANCE.md` control | 0 | one owning test reference; 6 positive-control matches; no additional byte-pin reader found | under 1 s | unknown |
| Snippet-marker search in the guide | 1 | no markers; synchronization was unnecessary | under 1 s | unknown |

**Non-pass disposition**: none; the zero-match snippet search is expected.
Security Review pass 2 of 2 is the final pass; no additional or clearing pass
was run. The P1 is answered by `30466f9a` and the delayed-resolver regression.
**Plan-specific acceptance commands**: no live GitHub request, Release
publication, tag-signature check, archive-byte check, full suite or re-anchor
was run. Snippet synchronization was unnecessary because the guide has no
snippet markers.
**Known omissions and tradeoffs**: `subprocess.run(timeout=...)` starts timing
after OS process creation returns; process creation itself cannot be interrupted
by that timeout. One Python child startup is added per API check. The timeout
behavior was measured on macOS only; Windows process lifecycle was not measured.
Live GitHub state and cached archive contents remain unverified. Elapsed
verification was about 2 minutes; token use unknown.

## Maintainer disposition required -- 2026-10-30

Security Review `7fc6854b` is pass 2 of 2 and retains the blocking P1 at the
review cap. The author implemented a parent-bounded API worker in `30466f9a`
and recorded Boundary B evidence in `f9cca7b9`; this implementation response
does not clear the Security Review finding. The Maintainer must disposition
the P1 before the plan advances to `ready-to-archive`. No third Security pass
or archive step was run.
