"""Independent 2026 pandapower demonstration; NOT a replay of the KTH PRO1 report.

All hourly demand and EV assumptions below are invented for this demonstration.
"""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
import csv
import json
import math
from pathlib import Path

import pandapower as pp
from pandapower import networks, topology


# Deterministic illustrative hourly multipliers, not the historical course XLSX.
DEMAND_MULTIPLIERS = (
    0.65, 0.62, 0.61, 0.62, 0.65, 0.72, 0.82, 0.90,
    0.97, 1.00, 1.02, 1.01, 0.98, 0.97, 1.00, 1.06,
    1.10, 1.16, 1.20, 1.16, 1.05, 0.91, 0.80, 0.72,
)
# A single illustrative EV charging load at the largest existing load bus.
# This is NOT the original assignment's EV data, penetration estimate, or topology.
EV_MW = (
    0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,
    0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.05,
    0.10, 0.20, 0.30, 0.30, 0.25, 0.15, 0.05, 0.00,
)


def create_case(hour: int, ev: bool = False):
    """Construct a FRESH network for every hour (no stale final-snapshot data)."""
    if not 0 <= hour < 24:
        raise ValueError("hour must be between 0 and 23")
    net = networks.create_cigre_network_mv(with_der=False)
    multiplier = DEMAND_MULTIPLIERS[hour]
    net.load.loc[:, "p_mw"] *= multiplier
    net.load.loc[:, "q_mvar"] *= multiplier
    if ev and EV_MW[hour] > 0.0:
        largest_load = net.load["p_mw"].idxmax()
        ev_bus = int(net.load.at[largest_load, "bus"])
        pp.create_load(net, bus=ev_bus, p_mw=EV_MW[hour], q_mvar=0.0,
                       name="synthetic_EV_example")
    return net


def solve_case(net) -> None:
    """Let failures propagate; never invent a replacement result."""
    pp.runpp(net, algorithm="nr", init="flat")
    if not net.converged:
        raise RuntimeError("pandapower did not converge")


def _finite_extreme(values, operation):
    numbers = [float(x) for x in values if math.isfinite(float(x))]
    if not numbers:
        raise ValueError("No finite power-flow results")
    return float(operation(numbers))


def result_row(net, hour: int, ev: bool) -> dict:
    return {
        "scenario": "illustrative_EV" if ev else "base",
        "hour": hour,
        "demand_multiplier": DEMAND_MULTIPLIERS[hour],
        "ev_mw": EV_MW[hour] if ev else 0.0,
        "min_bus_voltage_pu": _finite_extreme(net.res_bus.vm_pu, min),
        "max_bus_voltage_pu": _finite_extreme(net.res_bus.vm_pu, max),
        "max_line_loading_percent": _finite_extreme(net.res_line.loading_percent, max),
        "max_transformer_loading_percent": _finite_extreme(
            net.res_trafo.loading_percent, max
        ),
    }


def hourly_screen() -> list[dict]:
    """Run separate AC power flows and retain each hour immediately."""
    rows = []
    for ev in (False, True):
        for hour in range(24):
            net = create_case(hour, ev=ev)
            solve_case(net)
            rows.append(result_row(net, hour, ev))
    return rows


def n1_screen(base_net) -> list[dict]:
    """Single line/2-winding-transformer outages on the base network.

    Islanding and nonconvergence are reported as failures, never as zero loading
    or successful N-1 cases. Does NOT cover generators, switches, N-k, or all hours.
    """
    rows = []
    for kind in ("line", "trafo"):
        element_table = base_net[kind]
        for idx in element_table.index[element_table.in_service]:
            trial = deepcopy(base_net)
            trial[kind].at[idx, "in_service"] = False
            disconnected = sorted(int(b) for b in topology.unsupplied_buses(trial))
            entry = {
                "element_type": kind,
                "element_index": int(idx),
                "status": "islanded" if disconnected else "unknown",
                "unsupplied_bus_count": len(disconnected),
                "max_line_loading_percent": "",
                "max_transformer_loading_percent": "",
            }
            if not disconnected:
                try:
                    solve_case(trial)
                except (pp.LoadflowNotConverged, RuntimeError):
                    entry["status"] = "nonconvergent"
                else:
                    entry["status"] = "solved"
                    entry["max_line_loading_percent"] = _finite_extreme(
                        trial.res_line.loading_percent, max
                    )
                    entry["max_transformer_loading_percent"] = _finite_extreme(
                        trial.res_trafo.loading_percent, max
                    )
            rows.append(entry)
    return rows


def run_experiment() -> tuple[list[dict], list[dict], dict]:
    hourly = hourly_screen()
    # Only one clearly identified snapshot is screened for line/trafo outages.
    peak = create_case(18, ev=True)
    solve_case(peak)
    contingencies = n1_screen(peak)
    summary = {
        "project": "independent-pandapower-demonstration-2026",
        "pandapower_version": pp.__version__,
        "network": "pandapower built-in CIGRE MV, without DER",
        "demand_profile": "synthetic illustrative 24-hour multipliers",
        "ev_profile": "synthetic single-bus EV injection in MW",
        "n1_scope": "single line and 2-winding transformer outages, hour 18 EV scenario",
        "n1_status_counts": dict(Counter(r["status"] for r in contingencies)),
        "hourly_scenario_rows": len(hourly),
        "contingencies_screened": len(contingencies),
        "historical_pro1_report_reproduced": False,
        "external_network_validation": False,
    }
    return hourly, contingencies, summary


def _write_csv(path: Path, records: list[dict]) -> None:
    if not records:
        raise ValueError("No records to export")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True,
                        help="New directory; existing outputs cannot be overwritten")
    args = parser.parse_args()
    out = args.output
    if out.exists() and any(out.iterdir()):
        raise SystemExit(f"Refusing to overwrite nonempty directory: {out}")
    hourly, contingencies, summary = run_experiment()
    out.mkdir(parents=True, exist_ok=True)
    _write_csv(out / "hourly.csv", hourly)
    _write_csv(out / "single_outages.csv", contingencies)
    with (out / "manifest.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True, allow_nan=False)
        handle.write("\n")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
