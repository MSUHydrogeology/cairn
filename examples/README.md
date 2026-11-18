# Worked examples

These small runnable projects teach Cairn workflows. Their records are
illustrative, not claims of real independent review or research. They are not
installer templates or [real-project case studies](../docs/case-studies/).
Use Python 3.11+ and pytest, from a local Cairn checkout.

| Question | Walkthrough | Commands and expected result | Limit |
|---|---|---|---|
| How does a light change work? | [Greeting](minimal/README.md) | `python examples/minimal/greet.py Ada` prints `Hello, Ada!`; `python -m pytest examples/minimal/test_greet.py` passes. | Toy CLI; no plan is needed. |
| How is a scientific change planned and checked? | [Water budget](scientific-minimal/README.md) | `python examples/scientific-minimal/water_budget.py` writes closed residuals and exits 0; its README also runs pytest and an input that exits 2. | Synthetic closure does not validate a model. |
| How do I install, customize and upgrade? | [Disposable upgrade](scientific-minimal/upgrade.md) | Follow its local checkout and scaffold commands; the named slot survives staged review and apply. | Needs local Git history and disk space; never use a real project. |
| How do I leave work for someone else? | [Handoff](scientific-minimal/handoff.md) | Run the linked water-budget checks and compare the bounded note. | The handoff is illustrative, not a transcript. |
