"""Evaluation metrics for a single simulation run.

All functions take the arrays returned by `run_simulation`:
    times, env_states, strat_states, samples, costs

Time-weighted metrics (missed_active_fraction, false_active_fraction) compute
duration weights from np.diff(times) — the last sample contributes no weight,
which is negligible for non-trivial run lengths and avoids needing the total
simulation time T as a separate input.

A "relevant" sample is one with value 1 or 11 (the +10 is the high-quality
marker; see strat.highquality in sampling.get_sample).
"""

# ============================================================
# IMPORTS
# ============================================================
import numpy as np


# ============================================================
# COST METRICS
# ============================================================
def total_cost(costs):
    """Sum of per-sample costs over the run."""
    return float(np.asarray(costs).sum())


# ============================================================
# TIME-WEIGHTED STATE METRICS
# ============================================================
def missed_active_fraction(times, env_states, strat_states):
    """Fraction of env-active TIME during which the strategy was passive.

    Returns nan if the environment is never active.
    """
    times = np.asarray(times)
    env = np.asarray(env_states, dtype=bool)
    strat = np.asarray(strat_states, dtype=bool)

    dt = np.diff(times)
    if dt.size == 0:
        return float("nan")

    env_active = env[:-1]
    strat_passive = ~strat[:-1]

    active_time = dt[env_active].sum()
    if active_time == 0:
        return float("nan")

    return float(dt[env_active & strat_passive].sum() / active_time)


def false_active_fraction(times, env_states, strat_states):
    """Fraction of env-passive TIME during which the strategy was active.

    Returns nan if the environment is never passive.
    """
    times = np.asarray(times)
    env = np.asarray(env_states, dtype=bool)
    strat = np.asarray(strat_states, dtype=bool)

    dt = np.diff(times)
    if dt.size == 0:
        return float("nan")

    env_passive = ~env[:-1]
    strat_active = strat[:-1]

    passive_time = dt[env_passive].sum()
    if passive_time == 0:
        return float("nan")

    return float(dt[env_passive & strat_active].sum() / passive_time)


# ============================================================
# EFFICIENCY METRICS
# ============================================================
def cost_per_relevant_sample(samples, costs):
    """Total cost divided by number of relevant samples (value 1 or 11).

    Returns inf when no relevant samples were collected.
    """
    samples = np.asarray(samples)
    n_relevant = int(((samples == 1) | (samples == 11)).sum())
    if n_relevant == 0:
        return float("inf")
    return float(np.asarray(costs).sum() / n_relevant)


# ============================================================
# AGGREGATE
# ============================================================
def compute_all(times, env_states, strat_states, samples, costs):
    """Compute all metrics from a single run and return a dict."""
    return {
        "total_cost": total_cost(costs),
        "missed_active_fraction": missed_active_fraction(times, env_states, strat_states),
        "false_active_fraction": false_active_fraction(times, env_states, strat_states),
        "cost_per_relevant_sample": cost_per_relevant_sample(samples, costs),
    }
