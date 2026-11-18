# Language — single ↔ multi-language

A codebase's **language** position is whether it is written in one
language or several. It is a secondary axis — it changes the test
architecture and names a few extra seams, but it does not reshape
the lifecycle or the roster.

## Scoring rubric

* **Language count.** How many languages carry load-bearing code?
* **Cross-language seams.** Where does one language call into
  another, and how is that boundary tested?
* **Language transition in flight.** Is the project porting from
  one language to another — a state that needs its own
  stewardship?

## Positions

### Single-language

One test framework, one test-tier doctrine. The test architecture
is uniform.

### Multi-language

* A **multi-language test architecture** — each language keeps its
  native test framework, and the test-tier doctrine spans them.
* **Cross-language seams are named explicitly** — the boundary
  where one language calls another is a documented surface with
  its own tests, not an implicit join.
* If a **language transition is in flight**, a port-stewardship
  practice tracks which surfaces have moved, which are
  dual-maintained, and which are frozen pending the port.
