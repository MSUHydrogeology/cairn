# Cairn Plain Language

**Cairn Plain Language is a one-page writing standard for what an AI agent
writes to a person.** It has 17 numbered rules and ships in every Cairn
install. Its aim is that a scientist can understand what the agent wrote,
check it, and act on it. This is version 1.0.

## Why it exists

A Maintainer cannot review what they cannot follow. Without a method, "write
plainly" means whatever each agent decides, and the same failure came back
three times in Cairn's own record: opaque terms in a proposal, test names that
only made sense inside one plan, and reader-facing pages full of undefined
internal codes.

Agents add a second problem: they sound surer than they are. In one study, on
average 47% of a model's confident answers were wrong (Zhou et al., 2024).
Fluent prose from an agent therefore raises a reader's trust without showing
that the work was checked.

## What it asks

The rules sit in four groups. The full text is the section "Cairn Plain
Language" in [`dev/agent_collaboration.md`](../dev/agent_collaboration.md); this
page does not repeat it.

| Group | Rules | What it asks of the writer |
| --- | --- | --- |
| Before you write | 1 | Know the reader and what they will do with the text. |
| Everything | 2 to 9 | Conclusion first. Say what you left unchecked. One name per thing. Define terms and keep the field's own. Short sentences, one topic per paragraph. Headings and lists for anything longer than a screen. |
| Instructions | 10 to 12 | One action per step. Say what the reader should see afterwards. Error messages say what to do next, without blame. |
| Scientific reasoning | 13 to 17 | Separate measured, assumed and expected. Give numbers with units and sources. State uncertainty as a number, not "likely". Do not claim more precision than the evidence supports. Say how sure you are about your own work. |

The rules limit how text is built, not which words it uses. A hydrologist's
"hydraulic conductivity" stays; the writer defines it.

## Two examples

These examples are invented to show the change. The numbers and messages in them are not real results.

**A claim about a model (rules 13 to 15 and 17).**

Before:

> The model matches the gauges well and the residuals are small, so it is
> probably fine.

After:

> Measured: Nash-Sutcliffe efficiency 0.71 at one gauge over 2015 to 2020
> (1,826 daily values, from `validate.py`, which I ran). Assumed: the gauge
> record has no ice-affected days; I did not check. Expected but not tested:
> similar skill in other years. I did not run this on Windows.

**A step in instructions (rules 10 and 11).**

Before:

> Install Cairn and make sure it worked.

After:

> 1. Open a terminal in the folder you want to work in.
> 2. Run the installer.
> 3. Check that it printed `installed` and created a `dev/` folder. If it did
>    not, copy the message it printed and ask the agent to fix it before the
>    next step.

## What backs it

The evidence is strongest where scientists are served worst today, and weakest
for the general writing rules.

* **Reasoning rules (13 to 17): published studies.** Pairing probability
  words with numeric ranges raised agreement with the IPCC's intended meaning
  only from 27% to 40% across 25 samples in 24 countries (Budescu et al.,
  2014), and words added to numbers did no better than numbers alone (Mandel
  and Irwin, 2020). One lab study found that a model saying "I'm not sure,
  but..." reduced people's reliance on its wrong answers, though over-reliance
  remained (Kim et al., 2024).
* **Wording, structure and instruction rules (1 to 12): professional
  consensus.** They follow ISO 24495-1:2023 (cited by clause, not copied), the
  US Federal Plain Language Guidelines and ASD-STE100. Most of the underlying
  studies used lay readers, not experts.

**Limits.** The rules were tried on three real passages of Cairn's own
writing before they shipped. No one has yet evaluated them with outside readers
over time, which ISO 24495-1 asks for. The reasoning rules rest on the
literature, not on an incident in Cairn's record. The Maintainer's own read,
about three months after release, is the check.

## Using it in your own project

The standard is versioned, licensed CC BY 4.0, and its rules name nothing
specific to Cairn. To adopt it, copy the section into your agent instructions,
keep the rule numbers, and replace only the opening paragraph and the
"Checking" paragraph, which mention Cairn's review process. Rule numbers never
change between versions, so "rule 15" means the same thing in any project.

Publishing it as a standalone page, with a block to paste in and its own DOI,
is planned after about three months of use.

## Where to read more

* The accepted proposal, with the full evidence and the review record:
  [`dev/proposals/archive/2026-10-26-claude-writing-for-the-reader.md`](../dev/proposals/archive/2026-10-26-claude-writing-for-the-reader.md).
* The reasoning behind it, in [the rationale](../doctrine/rationale.md), under
  "The comprehension floor".
* The [glossary](glossary.md) for any Cairn term used above.
