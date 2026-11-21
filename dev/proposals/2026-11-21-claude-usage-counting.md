# Count Claude usage toward a project

**Author**: Claude (Strategy), drafted by Claude Sonnet 5.5 (`claude-sonnet-5-5`)
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: heavy — it changes what the meter accepts as proof that usage belongs to a project
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-21
**Rules that apply**: `dev/rules/working-agreements.md`, `dev/rules/conventions.md`, `dev/rules/custom_session_routines.md`
**In brief**: The usage meter would count Claude's own token use toward a project, using the working folder each Claude record names, so the end-of-session report stops showing it as unknown.

## Decision summary

**Conclusion.** Let the meter count Claude usage, sub-agents included. Antigravity gets a look only, with your leave.

**The problem.** You asked for cost data "so we can actually see what works to keep costs down." The end-of-session report shows Claude usage as unknown. The hand-kept cost record measured the wrong thing: the figure the tool gives for each sub-agent is close to the size of its last request, about a thirtieth of what the sub-agents used that day. Two thirds of that day's tokens were the coordinating session's own, which the hand record cannot see (both measured 2026-11-21). Only the tool's logs hold real use. The meter reads them but will not accept the folder a log sits in as proof of the project. You decided (chat, 2026-11-20): "Yes, both CLAUDE and Antigravity should count."

**What is added.**
- A Claude record counts toward a project when its working folder is the project's or inside it, its log is under a folder you approved, and the project's Git remote checks out as for Codex. All 3,434 records measured carry that folder.
- Sub-agent transcripts count the same way. The one-line summaries in the main log are not usage.
- The report shows Claude usage for the project by kind of token.
- One rule sentence: nothing read from a provider log goes into a plan, test, fixture, commit or report except counts and field names from a fixed list.

**What it costs.** Anyone who can write your own logs can make usage count toward a project. Codex already works this way; the harm is a wrong number in a private report. Folders inside the project are new: 59 of 3,434 records came from one.

**Not known.** Whether Antigravity's saved files hold token counts: a look at three transcripts on 2026-11-04 found none, and nothing has been looked at since. Whether repeats of one message always carry equal usage, and whether a summary ties to its transcript by an id: both measured, counts only, before the plan.

**Four choices** (my pick first):
1. *Antigravity.* (a) One count-only look first, with your leave. (b) Build a collector for its live status line now: larger, and a new place where Cairn writes. (c) Leave it out, with the reason shown.
2. *Folders inside the project.* (a) They count. (b) Only the exact path counts, as for Codex.
3. *A table for each agent run.* (a) Not now. (b) Include it now.
4. *When.* (a) v0.9, so issue #96 closes with this release. (b) v0.10.

## Context

The meter (`dev/tools/meter.py`) reads only source folders named in the user's consent file. Its Claude reader marks each assistant event `project_path_unapproved`, ownership unknown. The project export keeps only events with a verified project and proven ownership (`_project_export`), so none reaches a project.

Codex differs: `read_records` sets a project when the record's folder equals exactly one configured project path, then checks the project's Git remote (`_verified_project_remote`). Plan C's check on a real log found one case left: a sub-agent summary in an `attachment` record trips `unsupported_record`. Plan C's Security Review required flagging a `usage` key at any depth and exempting no record by type name.

**Measured 2026-11-21, counts only, one session** (`dev/PLANNING.md`, "The rest of #96"):
- 3,434 assistant records in the session log and 4,947 in 70 sub-agent transcripts. Each has a working folder, session id and request id; every folder was the project's root or inside it.
- Transcripts sit beside the session log, carry the parent's session id and a side-chain mark, and share no message with it.
- 75 summaries in the session log; 70 have totals within one percent of a transcript's last request.

**Read from the code, not measured.** The scanner descends sub-folders to depth 32 (`_enumerate_jsonl`), so transcripts under an approved root are already read. An event key is session, request id and message id. Records with one key and equal usage merge; unequal usage makes the event unknown (`conflicting_usage`).

## Proposal

**A. A Claude record proves its own project.** It counts toward a configured project when all three hold; otherwise it stays unknown, with a reason.
1. Its log lies under an approved source root, as today.
2. Its working folder, compared as text and never opened, is the project's path or lies inside it, for exactly one configured project. A folder inside two counts for neither.
3. The project's Git remote passes the Codex check, which reads the configured project's own `.git/config`.

The log's folder is never proof. A record with no request id stays unknown, as `test_requestless_claude_does_not_guess_lineage_from_directory` pins. Ownership becomes proven only on a record passing all three.

**B. Sub-agent transcripts are usage and count under A; their summaries are not.** Equal repeats already merge by event key; the plan checks this against the repeat measurement. The meter recognises the summary's exact shape, a `usage` value with exactly three whole-number fields (token total, tool count, duration), does not count it, and no longer calls it unsupported. Any other non-assistant record carrying `usage` stays `unsupported_record`. When a session has summaries and no transcript under any approved root, the reading is marked incomplete with a new reason code, kept off the report's harmless list (`_PULSE_BENIGN_REASONS`, `dev/tools/pulse.py`) so the report prints INCOMPLETE.

**C. The report shows it.** `pulse.py` marks a tool PARTIAL when the aggregate has rows for it, so Claude rows appear and no report format changes. I found no pinned test expecting a matching Claude record to stay unknown; I did not read all of `tests/integration/test_meter.py`. The usage-free tests gain a summary case.

**D. Antigravity: look before building.** The reader is a deliberate stub; this proposal builds none. It asks your leave for one count-only look at Antigravity's saved files where you use it: field names from a fixed list, and counts; nothing copied. If they hold token counts and a working folder, a follow-up plan adds a reader under A's rule. If not, the report says why and that part of #96 closes on that reason with your word.

**E. The rule is written down.** One sentence in `dev/rules/custom_session_routines.md`, beside the consent rule: nothing read from a provider log goes into a plan, test, fixture, commit or report except counts and field names from a fixed list. The list is fixed because on 2026-11-21 a count-only check printed a sentence: a record used one as a field name.

**Not here.** A table for each agent run (choice 3); a collector for Antigravity's live status line; usage kept under another field name than `usage`, which stays unseen.

**Ledger cost.** A new `READER_VERSION` may be needed, which makes the meter refuse an older ledger. Earlier Claude events are not back-filled. The plan decides.

## Rationale

The record names its own project, as Codex's does: one trust story, one difference.

## Alternatives considered

- **Do nothing.** Claude stays unknown.
- **Trust the log's folder.** It names the tool, not the project.
- **Count the summaries.** Each is about one request's size.
- **Exempt `attachment` by type name.** Plan C's Security Review rejected it.

## Documentation / doctrine surface

`dev/rules/custom_session_routines.md` (E); `dev/measurement/README.md`; `dev/PLANNING.md`; the changelog.

## Evidence / verification plan

Tests use hand-written records. Failing cases: a folder outside every project; inside two; a failed remote check; repeats with differing usage; a summary with no transcript; another non-assistant record with `usage`. **One developmental check on a real log, with your leave:** the meter's Claude totals for one session, by kind of token, equal an independent count-only sum of its log and transcripts. I ran no test and read no log for this proposal.

### Security preflight

- **S1** Log files under approved roots. A record's folder and ids are data, compared as text, never opened. Project path and remote come from the consent file.
- **S2** Each failing case above leaves usage unknown or the reading incomplete.
- **S3** The user's own `refresh` command, over approved roots and configured projects only.
- **S4** Toward unknown or incomplete, never a guessed number.
- **S5** Forged logs; usage under another field name; a renamed field in a new tool version; logs deleted before a refresh.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

- Totals that differ from the independent sum.
- A project showing usage from work done elsewhere.
- A reading called whole when transcripts were missing.

## Scope delta

**Scope delta**: preserved.

## Assurance path

**Assurance path**: high-assurance
