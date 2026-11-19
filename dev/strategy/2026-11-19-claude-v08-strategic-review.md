# After v0.8: prove it and lighten it

**Author**: Claude (Strategy)
**Model**: Claude Fable 5.2 (`claude-fable-5-2`); evidence sweeps by five Claude Sonnet subagents
**Date**: 2026-11-19
**Status**: draft
**Type**: product-strategy
**Surfaces this would feed**: the v0.9 and later sections of `dev/PLANNING.md`; the "Still open" list in the guide star; any proposal the Maintainer opens from the moves below.

## Summary

Cairn's core bet is sound, and outside research now supports it. Its weight is the risk. On a fresh Windows machine the 0.8.0 install, integrity check and session start all worked, but the documented Windows first run did not. Each cut since August regrew within days, because adding a rule, review or test is a local choice and removing one is a project. No outside user has yet tested whether Cairn beats a short instruction file with ordinary Git.

I recommend that v0.9 build no new mechanism. It should prove the first hour on every platform, make restraint structural, ship a small core, and get outside evidence. v0.10 should spend what that frees on the scientific core, where Cairn has no competitor. Nothing here is accepted work.

## The question

After v0.8, does Cairn help people ship good scientific code at a cost they will pay? What should v0.9 and v0.10 do about the answer?

## Method

I measured these on 2026-11-19 at tag v0.8.0, on a fresh Windows Server 2022 checkout with Python 3.13.5:

- a real `solo-greenfield` install into a scratch repository, following `docs/quickstart.md`;
- read-only scripts over `git log` and the tracked tree.

Five Sonnet subagents read Cairn's records and outside sources. I mark their figures "reported".

I did not run Cairn's test suite, test macOS or Linux, read the gate code, or read the outside studies in full. The purpose shares below are classed by file name and are approximate.

Two results would show this note wrong: LHM or modflow_tools records showing that the present lifecycle catches scientific errors at an acceptable cost per change; or an outside adopter who prefers the full install to the small core.

## Findings

**It works where it is exercised.** The install took 8.3 seconds and wrote 73 files. `install/verify_integrity.py` passed, and `dev/tools/session.py` and the board ran. The Mac certifying run recorded 5,894 passed and 1 failed in 60 minutes 41 seconds (`dev/measurement/certification-run-2026-11-19.md`). The failure is a pin that waits on the deferred re-anchor.

**The promised avenues have gaps.** In `docs/quickstart.md` the PowerShell column still names the pre-0.8 installer folder, so steps 2 and 3 fail. Its commit command leaves the new rules file untracked. Session start prints Windows paths with stray escape codes and lists two README files as open work. Plain `python` reached only the Windows Store stub on this machine. Issues #93, #95 and #96 add a bash-only command, a broken upgrade from a default Windows clone, and a usage meter that reports this harness's usage as unknown. About 3,400 test functions did not catch the quickstart defect, because no check runs the documented commands on each platform.

**Where the mass sits.**

| Measure | Value |
|---|---|
| Tracked Markdown | 3.78 million words; 89% is proposals and plans, nearly all archived |
| Python | 61,800 unique lines of tools; 116,400 lines of tests |
| Test lines by purpose | pins and re-anchor 24%, installer 19%, security scans 14%, usage meter 11% |
| Smallest install | 117 files, about 41,000 words of live Markdown, 21,700 lines of Python |
| Reading before a first session | about 24,300 words (reported) |
| Science-specific code | one worked example |

**The cost of a change has not fallen.** Median proposal length fell from about 10,800 words in the 0.5 window to 2,000 in 0.6, then crept up to 2,500. Every window shows 7 to 8 commits and 3 to 5 review commits per proposal. Plans opened in the 0.8 window took a median 17 commits and 9 review commits, against the project's own target of 3.5. Authors proposed the heavy tier for 15 of 28 proposals in that window, and 19 of the 28 carried a Security Review. Since 0.3, 59 to 84% of commits in each release window touched only records. The manual Tokens field read "unknown" in 67 of 67 sampled entries (reported).

**Cuts regrow.**

| What | History |
|---|---|
| `AGENTS.md`, words | 5,752 at 0.5; 1,047 at 0.8 |
| All working guidance, words | 16,772 at 0.5; 18,415 at 0.8. The text moved to the guide and the rules folder |
| Test functions | cut from 4,071 to 3,138 on 2026-11-10 (reported); 3,407 at 0.8 |
| Certifying run | about 25 minutes on 10-29 and 49 on 11-12 (both reported); 61 on 11-19 |

**Outside.** Reported, not verified by me: harnesses now supply on-demand skills, hooks that block, a model per subagent, spending caps and usage reports. General spec-and-plan frameworks are crowded, and none targets scientists. Studies favour short rule files, one fresh review grounded in executed checks, and comprehension gates. They find agent-written tests shallow, and most failing agent runs confident and wrong.

## Options

1. Continue the v0.9 board as written. It has fourteen rows: one settles defects, two seek outside evidence, and most of the rest add a tool, module or rule.
2. Stop and wait for an outside adopter.
3. Consolidate: prove, lighten, then build only on the scientific core. I recommend this one.

## Recommendation

**1. Prove the first hour on three platforms.** At each release, run the documented first-run and upgrade commands on macOS, Windows PowerShell and Linux. Let that define multi-host verification, in place of three full-suite runs. Fix the defects above first.

**2. Budget the unit of work, not the file.** A word cap on one file moves text to another. Set targets per change and report them from Git at archive, with no hand-filled field. Suggested starting points for the Maintainer to set: a light change takes 3 commits, 1 review and 600 words of record; a plan takes 8 commits and 4 review commits; the certifying run takes 20 minutes. Delete the Tokens, Elapsed and benefit-versus-cost fields. Let a rule added after an incident expire at the next release unless renewed. Keep archives out of agent searches: in my test a one-line ignore file removed a cached duplicate from this harness's search results.

**3. Ship a small core.** A handful of files and no required Python: the decision note, the independent scientific check, plain-language reporting, one fresh review, and the human who decides and pushes. Everything else becomes a layer the work earns. I expect a core that small to need little installer, upgrade engine or integrity ceremony. Installer and pin tests are about 43% of test lines today.

**4. Stop rebuilding the harness.** Freeze the usage meter and take usage from the harness where it reports it. Use native spending caps instead of building a budget guard. Offer hooks as thin adapters for the few bright lines. Ship one dashboard tab. For security, keep fail-closed installer containment: Security Review of the installer found real defects (reported). In the review of the open re-anchor proposal, weigh replacing pins and ceremony with a human-read diff of the protected files at release.

**5. Get outside evidence before v0.10.** One outside adopter uses the small core for three real changes, with thresholds declared first. Also count, in LHM and modflow_tools, how often a review or a scientific check caught a real error.

**v0.10 and after.** A worked scientific example from a real project; copyable independent-check patterns; issue #19 expressed as check presets; the January evaluation of Cairn Plain Language. Declare 1.0 only with two outside adopters, a stated comparison result, and a release the Maintainer can cut in thirty minutes.

**Residual risk.** A smaller default may drop a safeguard that mattered. The outside trial is the test.

## Open questions

- Which per-change targets does the Maintainer set?
- Does the small core replace the smallest profile, or sit beside it?
- Is the usage meter retired, or kept as an opt-in?
- Who is the second outside adopter?
