"""Compare multiple strategies on the same environment across many seeds.

Run with:
    python3 scripts/run_comparison.py
"""

# ============================================================
# IMPORTS & PATH SETUP
# ============================================================
from pathlib import Path
import sys

# Let Python find the project's source code no matter where you run this from.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from dynamic_datasampling_sim.harness import run_experiment, aggregate


# ============================================================
# RUN SPECIFICATIONS
# ============================================================
# Each entry below is one strategy paired with one environment.
# Want to compare different strategies? Add or remove entries here.
# Want to test a different environment? Change "environtype" (Preset, Markovian, TimeCorrelations).
# "T" is how many time steps each simulation runs for.
runs = [
    {"label": "WaitingTime", "strattype": "WaitingTime", "environtype": "Markovian", "T": 600},
    {"label": "Responsive",  "strattype": "Responsive",  "environtype": "Markovian", "T": 600},
    {"label": "Bayesian",    "strattype": "Bayesian",    "environtype": "Markovian", "T": 600},
]


# ============================================================
# RUN EXPERIMENT
# ============================================================
# Run every (strategy, environment) pair across 100 random seeds.
# One seed could be lucky — 100 seeds tells you what's actually happening on average.
# verbose=True prints progress so you know it's not stuck.
rows = run_experiment(runs, n_seeds=100, verbose=True)


# ============================================================
# AGGREGATE RESULTS
# ============================================================
# Group the results by strategy label and compute the average of each metric.
summary = aggregate(rows, group_keys=("label",))


# ============================================================
# PRINT SUMMARY TABLE
# ============================================================
# Pretty-print the results as a small table.
# cost      = total sampling cost (lower is cheaper)
# miss      = fraction of "active" states we missed (lower is better detection)
# false_act = fraction of false alarms (lower is fewer wrong calls)
print()
print("Aggregated results (mean across 100 seeds):")
print()
print(f"{'strategy':<14} {'cost':>10} {'miss':>10} {'false_act':>10}")
for s in summary:
    print(
        f"{s['label']:<14} "
        f"{s['total_cost_mean']:>10.1f} "
        f"{s['missed_active_fraction_mean']:>10.3f} "
        f"{s['false_active_fraction_mean']:>10.3f}"
    )
