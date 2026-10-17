# CIGRE MV distribution-grid study (PRO1)

An academic study of electric-vehicle integration in a medium-voltage network,
using the CIGRE MV example and pandapower-oriented coursework.

**Status: coursework-material archive, not a verified reproducible software release.**
**Important: the root PDF is a 19-page KTH assignment brief, not a student results report.** The [course-provided brief](PRO1_2024_Sep5.pdf), dated September 2024, outlines tasks, data and grading criteria; it does not document completed project results.
Historical source notebooks were identified on the `step_2` development branch,
but their clean execution, input rights and correspondence to the report have not
been established. No new results or independently validated N-1 capability are
claimed by this repository.

## Research question and scope

The original study brief covers base-case power flow, 24-hour load profiles,
EV charging, managed charging, PV/storage, and contingency/loss analysis.
These are study topics, not a checklist of verified public implementations.
The [historical assignment README](docs/original_assignment_readme.md) is retained
separately and should not be used as a result summary.

## Reproduction status

See [the recovered-source inventory and plan](REPRODUCTION_PLAN.md).
There is currently no supported installation command, scenario runner, automated
numerical test suite or clean-checkout result bundle on the default branch.
Until those exist, cite this as an academic grid-analysis study rather than an
open-source power-flow platform.

## Authorship and reuse

Authorship and course/team permissions must be confirmed before redistributing
or relicensing source, spreadsheets or report material. See [provenance](PROVENANCE.md).
No repository-wide software licence is granted by this documentation update.
Pandapower and other upstream materials retain their own terms.


<!-- ci-workflow-coverage -->
## Continuous integration

[![CI](https://github.com/abhijith-sivaprasadan/PRO1_network/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/abhijith-sivaprasadan/PRO1_network/actions/workflows/ci.yml)

See [CI coverage and limitations](CI.md) for the automated checks. The status badge tracks the default branch.

## Independent 2026 screening code (separate from archived coursework)

A new [pandapower numerical screening demonstration](reconstruction/README.md) is developed separately from the historical report and notebooks. It uses the built-in CIGRE MV example and openly synthetic 24-hour/EV profiles; it is not evidence that the brief's later steps were completed. Its numerical tests cover fresh hourly solves and explicitly recorded line/transformer outage outcomes. **It does not reproduce or validate the original coursework results.** Consult its CI and run artifacts before treating it as tested.
