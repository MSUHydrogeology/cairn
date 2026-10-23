# The solo-legacy adopter recipe

A tested adoption path for one scientist, one AI agent and an existing
research codebase (messy, undocumented, half-tested, or all three). The
larger profiles assume a team big enough to staff them. The shortcut of
taking `solo-greenfield` and setting `age: legacy` quietly leaves out
the one module an existing codebase needs. This page avoids both.

## Before you install: the readiness pre-pass

You install with the scaffold like any other adopter, with one extra
step: **fill in
[`templates/codebase-readiness-report.md`](../templates/codebase-readiness-report.md)
first.** Its eleven sections surface hidden state, scientific
assumptions and security boundaries in an existing tree. A new
repository has none of these yet. A solo scientist with a legacy
codebase usually scores "mostly Mixed, with one or two Poor". That
means: start with the profile below and fix the Poor sections first. Do
this before you choose modules, because it tells you whether the two
optional modules below apply to you.

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

You might try `preset: solo-greenfield` with only `age: legacy` and no
`modules_add`. It looks sufficient and is not. The `age` setting changes
what the scaffold *reports*, but the modules it *installs* still come
from the preset's fixed list. For team-size axes the list is
recalculated; for age it is not. The result is the same 6 modules as a
greenfield install, with no `legacy-agent` and no warning. The two
`modules_add` lines are therefore not optional: they add the Legacy
Agent role and the characterization-testing habit
(`dimensions/age.md`) that an existing codebase needs. This is a known
gap in the scaffold, tracked for a later fix. Until then, this
workaround keeps the recipe correct.

## The week-one arc

1. **Fill the readiness report** (`templates/codebase-readiness-report.md`)
   before anything else. It's what the conditional modules above key off.
2. **Your first change: something disposable.** A real trivial edit (a
   typo or one-line fix) needs no proposal. To learn the proposal →
   review → decision steps, though, take one tiny change down the full
   path once, as the [quickstart](quickstart.md) does, before anything
   that matters depends on it. A small accepted proposal can be
   implemented and archived in one commit. Do this first, even on a
   legacy tree.
3. **Then, your first *substantive* proposal: `docs/assumptions.md`.**
   Write down your codebase's load-bearing scientific choices — sign
   conventions, unit conventions, default parameters, calibration
   weights — before any agent edits them. This is the question Cairn is
   most differentiated on, and for a legacy scientific codebase it's the
   proposal that actually protects something.

## Add the science trigger to your own triage rules

Cairn's general list of when to open a proposal does not name
scientific assumptions, so that it fits any project. Your installed
`dev/proposals/_template.md` has a slot for this:
the `<!-- cairn:slot triage-extra-triggers -->` block. Fill it with
something like:

```
Open a proposal when a change touches a scientific assumption this
project guards -- a sign convention, a unit convention, a default
parameter, or a calibration weight/constant. The question to ask:
would the science silently degrade if a contributor changed this
default?
```

Once a proposal is open, the same template's **Independent scientific
check** section covers the assumption itself. For a change that touches
a scientific assumption, it asks for one check that could show the
change is wrong about the world, with an expected value that neither
the new code nor its tests computed.

## Small changes need no proposal

Cairn sorts every change into one of three lanes before anything is
written. A typo or one-line fix is trivial: make the change with its
test and get a code review, with no proposal. A change whose shape is
already settled gets one short change note, reviewed. A new feature, a
contract change or a high-risk surface gets a proposal. When you are
unsure, take the heavier lane. This keeps process off bug fixes while
the changes that matter stay on the record. The full rules are in
[`doctrine/lifecycle.md`](../doctrine/lifecycle.md).
