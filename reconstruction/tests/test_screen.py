"""Executable numerical smoke and scope tests for the INDEPENDENT reconstruction."""
import pytest

from reconstruction.run_screen import (
    DEMAND_MULTIPLIERS, EV_MW, create_case, hourly_screen, n1_screen,
    run_experiment, solve_case,
)


def test_explicit_nonhistorical_profiles():
    assert len(DEMAND_MULTIPLIERS) == 24
    assert len(EV_MW) == 24
    assert min(DEMAND_MULTIPLIERS) > 0
    assert max(EV_MW) > 0


def test_hourly_ac_results_are_not_final_state_repeated():
    records = hourly_screen()
    assert len(records) == 48
    assert len({r["hour"] for r in records if r["scenario"] == "base"}) == 24
    lookup = {(r["scenario"], r["hour"]): r for r in records}
    morning = lookup[("base", 2)]
    evening = lookup[("base", 18)]
    assert morning["demand_multiplier"] != evening["demand_multiplier"]
    assert abs(morning["max_line_loading_percent"] -
               evening["max_line_loading_percent"]) > 1e-6
    assert lookup[("base", 18)]["ev_mw"] == 0.0
    assert lookup[("illustrative_EV", 18)]["ev_mw"] == pytest.approx(0.30)
    # The illustrative EV load should produce a genuinely different power flow.
    assert abs(lookup[("base", 18)]["max_transformer_loading_percent"] -
               lookup[("illustrative_EV", 18)]["max_transformer_loading_percent"]) > 1e-8


def test_n1_records_every_line_or_trafo_outage():
    net = create_case(18, ev=True)
    solve_case(net)
    results = n1_screen(net)
    count = int(net.line.in_service.sum()) + int(net.trafo.in_service.sum())
    assert len(results) == count
    assert {(r["element_type"], r["element_index"]) for r in results} == {
        (kind, int(idx))
        for kind in ("line", "trafo")
        for idx in net[kind].index[net[kind].in_service]
    }
    assert set(r["status"] for r in results) <= {
        "solved", "islanded", "nonconvergent"
    }
    for row in results:
        if row["status"] != "solved":
            assert row["max_line_loading_percent"] == ""
            assert row["max_transformer_loading_percent"] == ""


def test_summary_cannot_be_mistaken_for_historical_reproduction():
    _, outages, summary = run_experiment()
    assert summary["historical_pro1_report_reproduced"] is False
    assert summary["external_network_validation"] is False
    assert summary["hourly_scenario_rows"] == 48
    assert summary["contingencies_screened"] == len(outages)
    assert sum(summary["n1_status_counts"].values()) == len(outages)
