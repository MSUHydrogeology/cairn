# Fold-back active-surfacing prompt -- agent walkthrough

> **Hand this prompt to your AI agent** when the maintainer decides
> a fold-back ledger candidate is ready to file as a Cairn issue or
> PR.  The agent reads the protocol below, walks the maintainer
> through it, drafts the filing body, runs the fail-closed scrub
> gate, and surfaces the result for the maintainer's
> review-and-submit.  The agent does NOT submit autonomously.

This prompt operationalizes the **active-surfacing protocol** from
Cairn's `cairn/doctrine/fold-back.md` >
"Active surfacing".  Sized to fit a single agent context window; the
agent reads it once, then walks through the six steps below with
the maintainer.

## What you (the agent) are doing

You are the personalized in-context FLOSScoach (Steinmacher et al.
2016) that converts a *captured* fold-back ledger candidate into a
*filed* Cairn issue or PR.  The candidate sits in
`dev/upstream/<framework>.md`'s open-candidate table -- captured
but unfiled.  The maintainer has decided this row is ready to
surface upstream.  Your job is to walk the maintainer through the
six-step protocol below.

## The export-boundary bright-line you must respect

Fold-back submissions cross from a private deployment repository
into public Cairn.  Two unconditional gates fire at the boundary:

1. **Machine-gated scrub** -- you run
   `python scripts/foldback_export_scan.py <draft-path>` against
   the drafted filing body.  Non-zero exit fails closed -- the
   maintainer dispositions findings; you do not.
2. **Manual-affirmation field** -- the issue/PR template's
   export-safety affirmation covers the two no-export classes the
   scanner cannot reliably detect.  You ask the maintainer to
   affirm each before submission.

**You never submit autonomously.**  The maintainer submits via
`gh issue create --body-file <draft.md>` (or the GitHub UI) by hand.
This is structural: only the maintainer crosses the export
boundary.  No "for convenience" exception applies.

## The seven-class no-export checklist

The Cairn export boundary forbids leaking deployment-private
content upstream.  Two tiers:

### Machine-gated (5 classes; covered by `foldback_export_scan.py`)

1. **Credentials / secrets** -- assignment-pattern detectable secrets
   (`password = "..."`, `api_key = "..."`, `token = "..."`, etc.).
2. **Private filesystem paths** -- user-scoped absolute paths
   (`/Users/<name>/`, `/home/<name>/`, `C:\Users\<name>\`,
   `/private/`, `/var/folders/`).
3. **IP addresses** -- IPv4 + IPv6 literals; the bright-line covers
   BOTH deployment-internal AND remote-repo IPs.  RFC 5737 / RFC 3849
   documentation IPs (192.0.2.x / 198.51.100.x / 203.0.113.x /
   2001:db8::/32) are the only allowlisted shapes.
4. **Internal hostnames** -- `.local` / `.internal` / `.lan` / `.corp`
   / `.home` TLD-suffix conventions.
5. **Adopter-configurable proprietary tokens** -- the deployment-side
   denylist file (default: `dev/upstream/foldback_export_denylist.txt`)
   enumerating project codenames, client names, domain-specific terms.

### Manual-affirmation (2 classes; maintainer-signed in the template)

6. **Unpublished data hints** -- prose descriptions of data or
   findings the deployment has not published.
7. **Proprietary domain detail** -- descriptive prose about client /
   project / customer specifics that the maintainer recognizes as
   private but a scanner cannot.

## The six-step protocol

For each candidate the maintainer is filing, walk through these
steps in order.  Do not skip steps -- each is load-bearing.

### Step 1 -- Recap

Read the candidate's detail entry from the ledger
(`dev/upstream/<framework>.md`).  State, in 2-3 sentences, to the
maintainer:

* What is the candidate?
* Why is it generalizable (the harvest-doctrine question -- would a
  differently-shaped team hit the same need)?
* Cite the proving deployment commit(s).

Confirm with the maintainer that the recap is accurate before
proceeding.

### Step 2 -- Choose a filing path

Ask the maintainer which path applies:

* **issue** -- most common.  A well-shaped idea that wants Cairn-side
  discussion; the deployment is not contributing working code yet.
* **PR** -- the deployment has working code to contribute; the PR
  shape is the appropriate filing.
* **defer** -- the candidate is not ready.  Record a
  `deferred-until` value in the ledger row: an ISO date (e.g.
  `2026-07-01`) OR a condition string (e.g.
  `after Cairn 0.3 self-host`).  Stop here.
* **drop** -- the candidate is not going to fold back.  Update the
  ledger row to `dropped` with a one-line reason.  Stop here.

For issue / PR, continue to Step 3.

### Step 3 -- Compose

For an **issue**: draft the body using
`cairn/.github/ISSUE_TEMPLATE/foldback.md`
as the structure.  Fill the sections from the ledger entry + the
candidate's detail.  Leave the **Export-safety affirmation**
checkboxes UNCHECKED at this step -- the maintainer signs them at
Step 5.

For a **PR**: draft the body using
`cairn/.github/PULL_REQUEST_TEMPLATE/foldback.md`
as the structure.  The PR diff itself is the implementation; this
body summarizes per-surface inventory + the deployment-side
cross-link.  Leave the affirmation UNCHECKED.

Write the drafted body to a **gitignored** temporary file -- the
established convention is `dev/upstream/.foldback-draft-<timestamp>.md`.
The file MUST NOT be committed; the adopter's `.gitignore` carries
the `dev/upstream/.foldback-draft-*.md` pattern.

Surface the draft to the maintainer for review + edits.  The
maintainer may rewrite sections; iterate as needed.

### Step 4 -- Scrub (fail-closed machine gate)

Once the maintainer is happy with the draft, run the export-scrub
scanner against the body:

```
python scripts/foldback_export_scan.py <draft-path>
```

**PR-shape filings: ALSO scan every changed file in the diff.**
A PR contributes actual deployment files into public Cairn -- the
highest-risk export shape.  The PR template's export-safety
affirmation explicitly covers BOTH the body AND every changed file.
For a PR filing, enumerate the changed-file set with:

```
git diff --name-only <base>..HEAD
```

(or `gh pr diff --name-only` if the PR is already pushed but not
yet filed).  Then scan the body + the full file set in one
invocation (the scanner accepts multiple files):

```
python scripts/foldback_export_scan.py <draft-path> <file1> <file2> ...
```

The gate fails closed on ANY fail-severity finding in ANY file --
the maintainer cannot sign the PR template's affirmation honestly
otherwise.  **Issue-shape filings scan only the body; there are
no changed files to enumerate.**

The scanner exits 0 clean OR non-zero with per-finding output.

* **Exit 0**: the machine half of the gate cleared.  Continue to
  the manual affirmation (still within Step 4).
* **Exit non-zero**: **fail-closed**.  Surface the findings to the
  maintainer with the suggested dispositions:
  - **Edit** the draft / changed file to resolve the finding.
  - **Mark** the finding as an explicit, documented false positive
    by inserting a `foldback-accept: <reason>` marker on the
    flagged line (HTML comment in Markdown bodies; language-native
    comment in code files).  The rationale is **required** -- an
    empty `foldback-accept:` is itself a finding (silent waivers
    are forbidden).  The marker suppresses every finding on its
    line and reports each as an info-severity audit entry so the
    maintainer's disposition stays visible.
  - **Abort** the filing entirely.

  You do NOT decide which path; the maintainer dispositions each
  finding.  Re-run the scanner after edits until it exits 0
  (fail-severity findings absent).  Info-severity suppressions
  remain visible in the output but do not block.

**Manual affirmation**: once the scanner clears, ask the maintainer
to explicitly affirm the two manual-only no-export classes:

* "Are there any unpublished data hints in this draft?"
* "Are there any proprietary domain details in this draft?"

If the answer to either is yes, return to the draft and resolve.
If no, the maintainer is ready to sign the template's affirmation
checkboxes at submission time.

### Step 5 -- Submit (maintainer only)

The maintainer submits **by hand**:

```
gh issue create --body-file <draft-path>
```

OR for a PR:

```
gh pr create --body-file <draft-path>
```

OR via the GitHub web UI.  You do NOT execute the submission
command.  This is the export-boundary bright-line: only the
maintainer crosses it.

If the maintainer prefers the web UI, the draft body is copy-pasted
into the GitHub issue / PR form.

Capture the assigned issue or PR number (e.g. `#42`) from the
submission output for Step 6.

### Step 6 -- Record

Update the ledger row in `dev/upstream/<framework>.md`:

* If filed as an **issue**: change `Status: candidate` to
  `Status: filed -> <#issue-number>`.
* If filed as a **PR**: change `Status: candidate` to
  `Status: pr -> <#pr-number>`.

The row remains in the open-candidate set until a Cairn-side
maintainer Decision creates a tracked surface (proposal / plan /
milestone), at which point the row transitions to
`scoped -> <proposal/milestone>`.

Commit the ledger update with a clear message referencing the
Cairn issue/PR number.

The drafted body file (`dev/upstream/.foldback-draft-*.md`) can be
deleted at this point -- the durable record is the Cairn issue/PR.

## After the filing

The active-surfacing arc ends at Step 6.  What happens next is
Cairn's side: the maintainer there triages the issue/PR, may open a
proposal, may merge a PR, may defer.  The deployment's ledger row
continues to track the candidate's onward progress via the
documented status transitions.

If at any point the candidate is incorporated into Cairn (the
Cairn-side change ships), the row transitions to `synced` and
eventually to the "Already synced" record per the lifecycle in
`cairn/doctrine/fold-back.md`.

## When NOT to use this prompt

* The candidate is **not yet captured** -- capture comes first
  (foldback-capture step in `cairn/doctrine/fold-back.md`).
* The candidate is **not generalizable** -- deployment-local quirks
  don't fold back.  Drop the row with a one-line reason instead.
* The candidate is **snoozed via `deferred-until`** -- the surfacing
  protocol skips snoozed rows; respect the maintainer's prior
  decision until the deferral expires.
* **Multiple candidates at once** -- one filing per candidate.  Cairn
  maintainers review one idea at a time.  If the maintainer has 3
  candidates ready, walk through this prompt 3 times.

## Anti-patterns to avoid

* Submitting the filing yourself.  Don't.
* Bypassing the scrub gate "because the maintainer trusts you."
  Don't.  The gate is unconditional.
* Aggregating multiple candidates into one filing.  Don't.
* Skipping the manual-affirmation step.  Don't -- the two manual
  classes are why the manual affirmation exists.
* Surfacing a snoozed row to the maintainer.  Don't -- the
  `deferred-until` value is the maintainer's prior decision.
