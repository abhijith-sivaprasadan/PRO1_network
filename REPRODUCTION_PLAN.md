# Recovered-source inventory and reproduction gates

Audit date: 2026-08-30. File presence is not successful execution.

| Evidence | Location | Status |
|---|---|---|
| Instructor/course assignment brief (not results report) | `PRO1_2024_Sep5.pdf`, main | 19-page Sep 2024 project instructions; no submitted student results in this PDF |
| Base-case notebook | `Step 1/Step 1 PW.ipynb`, `step_2` | Tracked source exists; local copy has uncommitted edits |
| Time-series notebook | `Step 2/Step 2 PW.ipynb`, `step_2` | Tracked source exists; local copy has uncommitted edits |
| Load shape | `Step 2/Loadshape_step_2.xlsx`, `step_2` | Source and redistribution terms need confirmation |
| Exported time series | `Step 2/time_series_results.xlsx`, `step_2` | Not a clean-run verification record |
| Later notebooks/profiles | Local untracked files | Not published or represented as submitted coursework |

Next steps, in order:

1. Confirm original authors/team contributions and course/input reuse permissions.
2. Obtain the actual team submission/report (if available) and confirm its authorship. Only then map each submitted figure/table to inputs and execution order; the currently linked PDF is merely the assignment brief.
3. Run recovered source in an isolated, pinned pandapower environment; record missing inputs and failures without inventing replacements.
4. Package a labelled reproduction only after mapping its relationship to the original study. Later reconstruction is not historical coursework code.
5. Implement explicit single-element line/transformer removal and record disconnected/nonconvergent contingencies separately from base-case overloads.
6. Once an actual submitted report is available, compare regenerated values against its reported tables with tolerances and a difference table. Until then, numerical equivalence is unassessed.
7. Add package/CLI, scientific tests, CI, attribution and an appropriately scoped licence after these gates pass.

No numerical equivalence, external validation, executable release, or new ownership assertion is made here.

## Specific historical time-series issue (audit 2026-10-17)

The tracked Step 2 notebook invokes `run_timeseries(net)` with an `OutputWriter`, but later constructs `bus_voltages` and `line_loadings` by repeatedly reading `net.res_bus` and `net.res_line` **after** the runner completes. Those tables therefore represent repeated final-state values, rather than archived snapshots for each hour. Assess the OutputWriter's actual recorded values and any existing Excel exports before attributing numerical time-series findings to the study. The independent `reconstruction/` demo intentionally re-solves each hour and is NOT historical report verification.
