"""Evaluation harness for comparing strategies across seeds.

Typical usage:

    from dynamic_datasampling_sim.harness import run_experiment, aggregate

    runs = [
        {"label": "WaitingTime", "strattype": "WaitingTime", "environtype": "Markovian", "T": 500},
        {"label": "Responsive",  "strattype": "Responsive",  "environtype": "Markovian", "T": 500},
        {"label": "Periodic",    "strattype": "Periodic",    "environtype": "Markovian", "T": 500},
        {"label": "Random",      "strattype": "Random",      "environtype": "Markovian", "T": 500},
    ]
    rows = run_experiment(runs, n_seeds=100)
    summary = aggregate(rows, group_keys=("label",))

Rows are returned as a list of dicts (one per (run, seed) cell). Convert to
pandas with `pd.DataFrame(rows)` if desired.
"""

# ============================================================
# IMPORTS
# ============================================================
import numpy as np

from .metrics import compute_all
from .simulation import run_simulation


# ============================================================
# CONSTANTS
# ============================================================
_METRIC_KEYS = (
    "total_cost",
    "missed_active_fraction",
    "false_active_fraction",
    "cost_per_relevant_sample",
)


# ============================================================
# EXPERIMENT RUNNER
# ============================================================
def run_experiment(runs, n_seeds=50, seed_offset=0, verbose=False):
    """Run each spec in `runs` across `n_seeds` seeds and return per-run metrics.

    Each entry in `runs` is a dict of kwargs forwarded to `run_simulation`,
    plus an optional "label" key. The harness supplies `seed`; do not include
    it in the run dict.

    Returns a list of dicts, one per (run, seed) cell, with the run's label,
    seed, identifying kwargs (strattype/environtype/T when present), and all
    metrics from `metrics.compute_all`.
    """
    # ---- Input validation ----
    if n_seeds < 1:
        raise ValueError("n_seeds must be at least 1.")

    # ---- Bookkeeping ----
    rows = []
    total = len(runs) * n_seeds
    done = 0

    # ---- Main run loop ----
    for run in runs:
        if "seed" in run:
            raise ValueError("run dict must not contain 'seed' — seeds are supplied by the harness.")

        run_kwargs = {k: v for k, v in run.items() if k != "label"}
        label = run.get("label") or _auto_label(run_kwargs)

        for seed in range(seed_offset, seed_offset + n_seeds):
            times, env_states, strat_states, samples, costs = run_simulation(seed=seed, **run_kwargs)
            metrics = compute_all(times, env_states, strat_states, samples, costs)

            rows.append({
                "label": label,
                "strattype": run_kwargs.get("strattype"),
                "environtype": run_kwargs.get("environtype"),
                "T": run_kwargs.get("T"),
                "seed": seed,
                **metrics,
            })

            done += 1
            if verbose and (done % max(1, total // 20) == 0 or done == total):
                print(f"  [{done}/{total}] {label} seed={seed}")

    return rows


# ============================================================
# AGGREGATION
# ============================================================
def aggregate(rows, group_keys=("label",), metric_keys=None):
    """Group rows and return mean/std/n per metric per group.

    nan values are ignored (np.nanmean / np.nanstd). inf values propagate —
    cost_per_relevant_sample returns inf when zero relevant samples were
    collected, and that's worth surfacing rather than hiding.

    `n` is the count of finite values used in each group's mean (so the
    researcher can see when a metric was undefined for some seeds).
    """
    # ---- Defaults & guards ----
    if not rows:
        return []
    if metric_keys is None:
        metric_keys = _METRIC_KEYS

    # ---- Group rows by key ----
    groups = {}
    for row in rows:
        key = tuple(row.get(k) for k in group_keys)
        groups.setdefault(key, []).append(row)

    # ---- Compute per-group statistics ----
    out = []
    for key, group_rows in groups.items():
        agg = {gk: kv for gk, kv in zip(group_keys, key)}
        for mk in metric_keys:
            values = np.array([r[mk] for r in group_rows], dtype=float)
            non_nan = ~np.isnan(values)
            finite = np.isfinite(values)
            # Mean tolerates inf (and surfaces it deliberately); std requires >=2 finite values
            agg[f"{mk}_mean"] = float(np.nanmean(values)) if non_nan.any() else float("nan")
            agg[f"{mk}_std"] = float(values[finite].std(ddof=1)) if finite.sum() > 1 else float("nan")
            agg[f"{mk}_n"] = int(finite.sum())
        out.append(agg)

    return out


# ============================================================
# HELPERS
# ============================================================
def _auto_label(run_kwargs):
    """Build a default label like 'WaitingTime_Markovian' from a run dict."""
    parts = [str(run_kwargs.get("strattype") or "strat"),
             str(run_kwargs.get("environtype") or "env")]
    return "_".join(parts)
