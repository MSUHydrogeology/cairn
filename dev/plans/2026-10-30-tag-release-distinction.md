# Plan: Check GitHub Release publication separately from the tag

**Source proposal**: dev/proposals/archive/2026-10-30-codex-tag-release-distinction.md
**Author**: Codex GPT-6.1 Sol (Implementation plan author)
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-30
**In brief**: Add a read-only publication check and make the release guide distinguish publishing a Release from pushing its signed tag.

## Source proposal

The accepted proposal requires explicit create-or-edit publication, manual notes
and source-link inspection, an independent gate-commit comparison, and the
existing signed-tag requirement. Its Decision authorizes implementation, not a
live release, push or publication.

## Scope

Change `docs/release-process.md` and add a standard-library-only internal
publication checker `scripts/check_release_publication.py` and owning tests
`bootstrap/tests/test_check_release_publication.py`. No stored state or
publishing credentials.

Proposed paths:
* `scripts/check_release_publication.py`
* `bootstrap/tests/test_check_release_publication.py`

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
API host. Tests may isolate transports through child-process fixtures without
adding a production bypass. Protocol sources: [GitHub Release API](https://docs.github.com/en/rest/releases/releases#get-a-release-by-tag-name)
and [Git ls-remote](https://git-scm.com/docs/git-ls-remote).

**Boundary A mapping.** Run
`python -m pytest bootstrap/tests/test_check_release_publication.py` for all C1
invariants and public-command fixtures, using local annotated Git refs and
stubbed Release replies. Cover malformed fields, missing publication date,
lightweight tags, duplicate refs, timeouts, unsafe inputs, encoded tag names,
redirect refusal and help/usage as well as accepted negative cases. Confirm the
real ls-remote invocation against local refs; no live network required.

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

Plan authoring: about 6 minutes; tokens unknown. Python 3.12.9 ran claim,
link and prose checks successfully; neutrality reported zero failures and 43
informational entries. External links were read through official documentation;
no implementation, live publication check or suite was run.
