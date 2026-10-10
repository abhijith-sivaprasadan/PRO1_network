# CIGRE MV distribution-grid study (PRO1)

An academic study of electric-vehicle integration in a medium-voltage network,
using the CIGRE MV example and pandapower-oriented coursework.

**Status: academic report archive, not a verified reproducible software release.**
The default branch contains the original [report](PRO1_2024_Sep5.pdf).
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
