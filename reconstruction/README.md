# Independent pandapower screening demonstration (2026)

**This is newly written demonstration code, not a recovery or reproduction of the 2024 KTH PRO1 submission.** The original PDF, historical notebooks, submitted results, and the 2026 demonstration are deliberately kept separate.

## Evidence boundaries

- Network: pandapower's publicly distributed **CIGRE MV** example (`with_der=False`), with the upstream project's own licence.
- Profiles: 24 deterministic **invented** hourly demand multipliers and one illustrative EV charging load (0–0.30 MW at the largest existing load bus). These do not represent the historical assignment's input spreadsheets, charging profiles, network expansion, or market observations.
- Per-hour results: 48 fresh AC power flows, with voltage and line/transformer loading captured immediately after each solve, avoiding the historical notebook's final-state reuse defect.
- Outage screening: removal of each in-service **line and two-winding transformer** for one hour-18 EV snapshot; islanding and numerical nonconvergence are distinct results. This is partial single-component contingency screening, not full operational N-1 security certification.
- Not implemented: original 348 EV profile claim, PV, BESS, smart charging optimisation, generation dispatch, losses minimisation, published report numerics, calibration to an actual utility network, uncertainty analysis.

## Reproduce

Python 3.12:

```bash
python -m venv .venv
# Activate .venv for your shell.
python -m pip install -r reconstruction/requirements.txt
python -m pytest -q reconstruction/tests
python -m reconstruction.run_screen --output reconstruction-output
```

The runner refuses to overwrite nonempty directories. Results:
`hourly.csv`, `single_outages.csv`, `manifest.json`. The manifest records package version, exact scenario boundary and the explicit `historical_pro1_report_reproduced: false` flag.

The GitHub workflow `.github/workflows/reconstruction.yml` executes the full numerical test suite on pushes and PRs and uploads an illustrative run. The existing archive-integrity badge remains separate and does **not** imply that historic results were replicated.

## Engineering interpretation

Voltage constraints, line overloads, islanding, and a solver failure answer different questions. In particular, a nonconvergent or islanded contingency must not be silently presented as a zero-loading secure case. A passing test only verifies this demonstration's internal calculations and output handling; there is no comparison to the submitted report or measured grid operation.

To reconcile the historical study, follow [../REPRODUCTION_PLAN.md](../REPRODUCTION_PLAN.md), respecting [../PROVENANCE.md](../PROVENANCE.md).
