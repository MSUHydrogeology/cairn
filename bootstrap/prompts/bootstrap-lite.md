# bootstrap-lite — the short on-ramp prompt for one-human + one-agent adopters

**What this is**: a short paste-into-the-agent prompt for a
maintainer who has one repository and one AI agent and wants
to bring Cairn in *without* walking the full procedure in
`../BOOTSTRAP.md`.

**When to use it**: you have a real codebase you want to add
Cairn to, you are working with one capable reasoning agent, and
you would rather have the agent assess the repo and recommend a
profile than score the six axes yourself by hand.

**When *not* to use it**: you have a tiny throwaway repository
and want a short "what does Cairn feel like?" walkthrough.
That is what `../../docs/quickstart.md` is for — the quickstart
copies the `solo-greenfield` profile literally and skips the
assessment loop entirely. Come here after the quickstart if you
want to adopt Cairn for real.

**Where this sits**: between the quickstart (`../../docs/quickstart.md`,
which prescribes the profile) and the full bootstrap
(`../BOOTSTRAP.md`, which has the agent and the Maintainer run
Acts I → II → III). bootstrap-lite carries the **assessment +
profile-acceptance loop** of Act I in a one-shot prompt, then
hands off to the scaffold once the Maintainer has accepted the
profile.

> **Important**: the prompt below tells the agent to *propose*
> a profile and **wait for the Maintainer's approval before
> running the scaffold**. The Maintainer's approval of the
> proposed profile is the load-bearing safety gate — installing
> apparatus the Maintainer has not accepted is the failure mode
> the full bootstrap exists to prevent. bootstrap-lite preserves
> that gate; it only collapses the *how I score axes* step.

---

## Paste the block below into your AI agent

(Verbatim is fine. The agent reads `AGENTS.md` and the six-axis
dimension docs in this same Cairn clone for the doctrine; the
prompt itself stays small.)

````text
You are helping me bring Cairn into this repository. Before you
do anything, read:

  * cairn/AGENTS.md — the apparatus you will operate under
  * cairn/dimensions/README.md and the per-axis docs
    (age.md, size.md, complexity.md, language.md, human-team.md,
    agent-team.md) — the six axes you will score
  * cairn/on-ramp/README.md — the two ways in, and the profile table

You may also read cairn/doctrine/README.md and
cairn/doctrine/lifecycle.md if you want grounding before scoring,
but it is not strictly required at this step.

Then walk through the assessment loop below as a single turn.
Do NOT install anything yet — the Maintainer accepts the profile
before any files are written.

Step 1 — survey this repository. Briefly describe:

  * approximate size (single module / multi-module / mono-repo);
  * approximate age and complexity, scientific or otherwise;
  * the test command (or "no tests today");
  * the build / run entry points;
  * any clearly sensitive surfaces I should keep away from your
    edit window;
  * the human contributors (solo / small-multi / large-multi)
    and the agent team (just you / multiple agent types).

Step 2 — score the six axes from the docs above. For each axis
report:

  * the chosen value (use the exact enum values in the per-axis
    docs);
  * a one-sentence reproducible reason (evidence from the repo
    survey, not a vibe).

Step 3 — recommend ONE of the three named governance presets:

  * solo-greenfield — small new repo, one human, one agent
  * collaborative-team — small team, 2-4 humans, 1-2 agent types,
    established codebase
  * high-rigor-legacy — legacy scientific codebase with tests,
    data, reproducibility, security concerns

For the recommended preset, briefly say which axes pushed you to
it and which axes were close calls. If none of the three is a
clean fit, say so — the Maintainer can still scaffold with
modules: instead of preset: (see cairn/bootstrap/BOOTSTRAP.md
Act I-5 — Derive the module selection), but flag the mismatch.

Step 4 — propose the profile YAML for me to review. Copy the
template from cairn/bootstrap/profiles/<recommended-preset>.yml
and:

  * set project_name and test_command from Step 1;
  * keep the preset: line as-is;
  * optionally suggest modules_add: / modules_remove: with
    one-line rationales each (do not silently expand or trim the
    roster).

Print the proposed profile.yml in a fenced block and STOP.

I (the Maintainer) will read your axis scoring and the proposed
profile, and either accept it, ask follow-up questions, or
adjust it. After I accept, I will run

    python cairn/bootstrap/scaffold.py \
        --config profile.yml \
        --target . \
        --summary

to preview, then re-run without --summary to install.

Once the scaffold has installed, propose ONE trivial change as
the first dogfood (e.g., a one-line README tagline), open it as
a proposal under dev/proposals/, and STOP again — same gate as
in cairn/docs/quickstart.md.
````

---

## What the prompt assumes you have already done

* You have cloned Cairn next to your target repo
  <!-- cairn-accept: suspicious-url reason="Literal Cairn clone URL the adopter needs to copy" reviewer="Claude" date=2026-05-28 -->
  (`git clone https://github.com/MSUHydrogeology/cairn.git cairn`).
* You have a working Python 3.11+ environment for
  `bootstrap/scaffold.py`.
* You have one AI coding agent connected to your target repo
  with read + write access to its working tree.

## What the prompt *does not* do

* It does not replace `../BOOTSTRAP.md`. bootstrap-lite
  collapses Act I's six-axis scoring + the profile-acceptance
  loop into a one-shot prompt; Act II's steps after the install,
  and Act III, still apply.
* It does not bypass the Maintainer-acceptance gate. The agent
  STOPs after proposing the profile and after opening the first
  dogfood proposal; both are Maintainer-decision points.
* It does not silently expand or shrink the module roster.
  Use the named preset; flag any `modules_add` / `modules_remove`
  the agent recommends so you can accept or reject each
  intentionally.

## Cross-references

* `../BOOTSTRAP.md` — the full procedure (Acts I → II → III).
* `../profiles/` — the three named governance presets the agent
  recommends among (`solo-greenfield`, `collaborative-team`,
  `high-rigor-legacy`).
* `../../docs/quickstart.md` — the short throwaway-repo
  walk-through; the on-ramp *before* bootstrap-lite.
* `../../on-ramp/README.md` — the two ways in, and how to choose a
  profile.
* `../../dimensions/README.md` and the six per-axis docs — the
  doctrine the agent uses to score axes during Step 2.
