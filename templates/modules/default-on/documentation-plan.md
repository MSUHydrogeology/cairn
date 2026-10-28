<!-- `docs/developer/` below is an illustrative example doc-tier (where an
     adopter might fold style guidance), not a claim about this tree —
     exempted from claim_check path resolution. -->
<!-- The three blocks below are merged into files at the project root, where
     `docs/DOCUMENTATION_PLAN.md` resolves; from this file's own folder it does not. -->
<!-- link-check-allow: docs/DOCUMENTATION_PLAN.md -->

# Module: documentation-plan

**Selected when:** default-on — kept by every deployment that may want
disciplined placement decisions for its documentation and doctrine
artifacts. The cost is one forkable file (`docs/DOCUMENTATION_PLAN.md`)
the adopter customizes once, plus three small cross-reference lines
the module merges into the core templates. The payoff is structural:
the "where does this new doc go?" question has an *algorithmic*
answer, and the doctrine-vs-description boundary stays load-bearing
instead of eroding.
**Adds to:** a forkable placement-decision procedure at
`docs/DOCUMENTATION_PLAN.md` (installed by the scaffold; the adopter
customizes the worked examples for their own tier vocabulary), plus
three short cross-reference lines that land in the adopter's
`AGENTS.md` (the `documentation-discipline` slot) and in the
adopter's `dev/proposals/_template.md` + `dev/plans/_template.md`
(the `documentation-tier-home` slot in each).

The documentation-plan module is the **structural ward against
documentation drift** that every multi-author project hits as the
doc surface grows. Without it, `AGENTS.md` accretes indefinitely
(every operational rule wants to live at root), the
doctrine-vs-description boundary blurs, and new content lands at
random tiers. The module ships the discipline: a four-layer vision
(entry / governing / deliberation / descriptive) + a decision
procedure + voice rules + naming conventions + an AGENTS-vs-
agent_collaboration boundary rule.

## What this module is

A **placement-decision procedure + cross-reference plumbing** that
makes the procedure discoverable from the surfaces an author hits
when adding new content. The module ships:

* The **forkable procedure** at `docs/DOCUMENTATION_PLAN.md` --
  installs from the scaffold into the adopter's tree once. The
  adopter customizes the worked examples (their own file inventory,
  their own tier vocabulary, their own AGENTS-vs-agent_collaboration
  boundary specifics). The doctrine substance (four-layer vision,
  decision procedure, voice rules) is shared by every adopter; the
  *examples* are deployment-specific.
* The **`documentation-discipline` cross-reference** that fills
  the slot in the core `AGENTS.md` (paste content from the
  "Merged into" Block 1 below). Names the procedure + points
  cold-reading authors at it.
* The **`documentation-tier-home` cross-reference** that fills
  the slot in the proposal + plan templates' "Documentation /
  doctrine surface" sections (paste content from "Merged into"
  Blocks 2 and 3 below). Makes the placement-decision procedure
  surface at the moment an author is filling in *what doctrine
  this proposal/plan touches*.

The placement-decision procedure itself is **prose**, not
mechanical enforcement. Programmatic placement-rule enforcement in
`check_cairn.py` is logged as a follow-up for a future module
(deferred;
procedure stabilizes through use before mechanical enforcement
becomes the right next step).

## What this module is NOT

A one-size-fits-all tier vocabulary. The four-layer vision is the
doctrine; the *tier names within each layer* are deployment-
specific (the reference deployment uses `quickstart / user_guide / theory /
reference / developer` for the descriptive layer; a different
deployment might use `getting-started / how-to / explanation /
reference` from the Diátaxis framework, or any other split). The
adopter customizes the descriptive-layer tier names in the
installed `docs/DOCUMENTATION_PLAN.md` to match their own
`docs/` structure.

## Adds to

The adopter's `AGENTS.md` (filled via the `documentation-discipline`
slot anchor in `cairn/templates/core/AGENTS.md`), and the adopter's
`dev/proposals/_template.md` + `dev/plans/_template.md` (filled via
the `documentation-tier-home` slot anchors in
`cairn/templates/core/dev/proposals/_template.md` +
`cairn/templates/core/dev/plans/_template.md`).

## Merged into

The three blocks below are **paste-into-slot content** the adopter (or
an agent on first read of this module) merges into the named target
slot. Cairn's module-merge helper (per
`cairn/bootstrap/BOOTSTRAP.md` > "Module-merge mechanics") will
eventually drive this mechanically via `cairn:merge-target`
directives; mechanical merge is **deferred for this module** pending
resolution of the helper's interaction with the install-lockfile
divergence check (Proposal B's merge pass mutates files post-install,
which currently makes the lockfile's clean-install guard refuse to
write -- a separate follow-up tracked Cairn-side). Manual paste from
the three blocks below is the documented adopter workflow until the
helper integration lands.

### Block 1: `AGENTS.md` -- slot `documentation-discipline`

> This deployment uses a **placement-decision procedure** for
> documentation and doctrine: see [`docs/DOCUMENTATION_PLAN.md`](docs/DOCUMENTATION_PLAN.md)
> for the four-layer vision (entry / governing / deliberation /
> descriptive), the routing rules, and the `AGENTS.md` ↔
> `agent_collaboration.md` boundary doctrine. When adding new
> documentation or doctrine, identify what the content is *doing*
> (prescription / deliberation / description) and route by layer.

### Block 2: `dev/proposals/_template.md` -- slot `documentation-tier-home`

> **Doc tier home rule** -- route doc and doctrine changes by layer
> per [`docs/DOCUMENTATION_PLAN.md`](docs/DOCUMENTATION_PLAN.md):
> cross-cutting prescription → governing layer (`AGENTS.md`);
> deliberation about what to build → deliberation layer (`dev/`);
> description of the software as it is → descriptive layer (`docs/`).
> A proposal that omits the doctrine-surface routing is itself a
> review finding.

### Block 3: `dev/plans/_template.md` -- slot `documentation-tier-home`

> **Doc tier home rule** -- route doc and doctrine changes by layer
> per [`docs/DOCUMENTATION_PLAN.md`](docs/DOCUMENTATION_PLAN.md):
> cross-cutting prescription → governing layer (`AGENTS.md`);
> deliberation about what to build → deliberation layer (`dev/`);
> description of the software as it is → descriptive layer (`docs/`).
> A plan's *Scope* must name the doctrine-surface touched (or an
> explicit "no doctrine surface").

## Forking the procedure

After install, the adopter customizes `docs/DOCUMENTATION_PLAN.md`:

* **Replace the four-layer worked examples** with the adopter's
  actual file inventory (e.g., the entry-layer's `README.md` is
  unchanged but `BOOTSTRAP.md` may not apply; the governing-layer's
  `AGENTS.md` is unchanged but the adopter may name their own
  `STYLE_GUIDE.md` or fold style into `docs/developer/`; the
  descriptive layer's tier names are deployment-specific).
* **Refine the AGENTS-vs-agent_collaboration boundary** if the
  deployment has its own agent-coordination doctrine beyond what
  Cairn ships.
* **Pin the naming convention** -- UPPERCASE landmarks vs.
  lowercase content is the Cairn convention; adopters who prefer
  a different convention pin it here once and apply it
  consistently.

The `<!-- cairn:customized -->` marker (per
`cairn/bootstrap/BOOTSTRAP.md` > "Module-merge mechanics") signals
adopter customization to the fidelity check + the merge helper.
Adopters who customize the cross-reference paragraphs above (e.g.,
to point at a different placement-doc filename) should add the
customized marker so the merge helper preserves the
customization on re-install.

## Cross-reference to `cairn/doctrine/doc-governance.md`

The placement-decision procedure is the **concrete how** of
Cairn's doc-governance rule (`cairn/doctrine/doc-governance.md`
in the Cairn methodology repo). The doc-governance rule names
the principle (build-the-software and operate-safely rules live
in `AGENTS.md`; the deliberation and decision process lives in
`dev/agent_collaboration.md`; each rule has one canonical home
and the other file only points). The placement-decision
procedure operationalizes that principle into the four-layer
vision + decision procedure + boundary rules an author works
through when adding new content.

## Cross-reference to the reference deployment

The placement-decision procedure was validated by the reference
deployment over multiple months of doc-restructure
work (its `docs/DOCUMENTATION_PLAN.md`).
The procedure surfaces here as Cairn doctrine because it is
**Cairn-portable** -- the four-layer vision and the placement
procedure generalize across project domains; only the *tier
names* within the descriptive layer are domain-specific.

Cairn's own self-hosted instance of this procedure lives at
`cairn/docs/DOCUMENTATION_PLAN.md` (Cairn IS its own first
adopter; dogfooding the module on the Cairn tree validates the
discipline before it ships to other adopters).
