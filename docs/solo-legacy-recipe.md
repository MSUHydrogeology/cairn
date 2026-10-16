<!-- The path above is external-repo: it lives in the adopter's own
     tree (created by their first substantive proposal), not Cairn's. -->

# The solo-legacy adopter recipe

A verified adoption path for the solo scientist + one agent + an
existing research codebase. If you are that persona — one human, one
AI agent, and a codebase that already exists (messy, undocumented,
half-tested, or all three) — the other routes mis-route you: the larger
profiles assume a team big enough to staff them, and the naive shortcut
("just take `solo-greenfield` and set `age: legacy`") silently ships you
a roster missing the one thing a legacy codebase actually needs. This
page is the path that doesn't do either.

## Before you install: the readiness pre-pass

You install with the scaffold, like any other adopter — **with one step
a greenfield adopter skips: fill
[`templates/codebase-readiness-report.md`](../templates/codebase-readiness-report.md)
first.** The eleven-section assessment surfaces hidden state,
scientific assumptions, and security boundaries in an *existing* tree —
exactly what a fresh greenfield repo doesn't have yet. Solo + legacy
usually scores "mostly Mixed with 1-2 Poor", which means start with the
profile below and fix the Poor sections first. Do the pre-pass before
you commit to a module roster, not after — it is what tells you whether
the conditional modules below actually apply to your tree.

## The exact composed profile

Preview the roster with `scaffold.py --summary`, then install it with
the scaffold — the same tool the quickstart runs, pointed at your own
repository.

<!-- solo-legacy-recipe: canonical-profile -->
```yaml
project_name: "<your-repo>"
test_command: "<your test command, or 'no tests today'>"

# solo staffing: one human + one agent
preset: solo-greenfield
# existing codebase -- earns the readiness pre-pass greenfield skips
age: legacy
# legacy-retrofit modules an existing tree needs (the age-gated rows
# the axis override does not auto-derive -- see "why these lines are
# load-bearing" below)
modules_add:
  - legacy-agent
  - testing-discipline
```

Run `python bootstrap/scaffold.py --summary --config profile.yml` from
a Cairn checkout — a release tag you have verified, per
`bootstrap/PROVENANCE.md` — against a copy of this YAML. It should
report an **8-module roster** — the six default-on modules
(`reflections`, `claim-check`, `incident-trackers`,
`documentation-plan`, `content-security`, `security-verification`)
plus `legacy-agent` and `testing-discipline` — with **zero staffability
warnings**. Confirm your own run matches, then install:

```bash
python bootstrap/scaffold.py --config profile.yml --target <your-repo>
```

The scaffold does not overwrite a file your repository already has —
your own `README.md` or `CHANGELOG.md` stays as it is — unless you pass
`--force`; don't. Then do the four steps it prints for a real adoption
(`bootstrap/BOOTSTRAP.md` Act II-3 to II-6).

**Two more modules, conditional on your own readiness-report
findings — don't add them yet:**

* Add `security-review` **if** your readiness report flags a real
  trust boundary — untrusted input meeting your system: file I/O
  reading external data, subprocess calls, path handling, credential
  or environment-variable use. A recharge model reading its own
  well-formed input files typically has none; a pipeline that ingests
  arbitrary user-supplied files typically does.
* Add `model-selection` **if** the pre-pass places your codebase at
  moderate-or-higher complexity. A small, disposable model at low
  complexity does not need it.

Don't force-add these two up front — that pre-empts the readiness
report's own job of telling you whether you need them. The recipe's
whole point is that the pre-pass decides this, not a fixed checklist.

### Why these lines are load-bearing

You might reasonably try `preset: solo-greenfield` with just
`age: legacy` and no `modules_add` — it looks like it should be
enough. It silently isn't: overriding the `age` axis changes what the
resolver *reports*, but the module roster it *builds* still starts from
the preset's static baseline, and that baseline doesn't get re-derived
for the age axis the way it does for team-staffing axes. The naive
override resolves to the same 6 modules a plain greenfield install
gets — no `legacy-agent`, no warning that anything is missing. The two
`modules_add` lines above aren't decoration; they're the actual
legacy-retrofit apparatus (`dimensions/age.md`'s Legacy Agent role and
characterization-testing discipline) your existing codebase needs and
the override alone won't give you. (This is a known engine gap, tracked
for its own future fix — the workaround above is what makes this recipe
correct today.)

## The week-one arc

1. **Fill the readiness report** (`templates/codebase-readiness-report.md`)
   before anything else. It's what the conditional modules above key off.
2. **Your first proposal: the Hello-world trivial accept.** Solo
   greenfield onboarding builds the first lifecycle rep around something
   disposable on purpose — it's the safest way to learn proposal → review
   → decision mechanics before anything that matters rides on it. Do
   that first, even on a legacy tree.
3. **Then, your first *substantive* proposal: `docs/assumptions.md`.**
   Write down your codebase's load-bearing scientific choices — sign
   conventions, unit conventions, default parameters, calibration
   weights — before any agent edits them. This is the question Cairn is
   most differentiated on, and for a legacy scientific codebase it's the
   proposal that actually protects something.

## Add the science trigger to your own triage rules

Cairn's universal triage list doesn't name a scientific-assumption
trigger — it's deliberately general, so it doesn't over-fit to science
projects. Your own installed `dev/proposals/_template.md` has a slot for
exactly this: the `<!-- cairn:slot triage-extra-triggers -->` block.
Fill it with something like:

```
Open a proposal when a change touches a scientific assumption this
project guards -- a sign convention, a unit convention, a default
parameter, or a calibration weight/constant. The question to ask:
would the science silently degrade if a contributor changed this
default?
```

## The escape hatch

If a change is urgent, clearly reversible, or explicitly experimental,
it may proceed without a proposal, but the commit or follow-up note
should say why the proposal step was skipped. This keeps the bypass
traceable without forcing process onto bug fixes or short-lived
experiments. (Your installed `dev/proposals/_template.md` carries this
too — see its own escape-hatch note.)
