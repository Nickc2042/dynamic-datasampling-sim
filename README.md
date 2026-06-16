# Dynamic Data Sampling Simulation

## What This Project Is For

- A **research sandbox** for experimenting with **adaptive sampling strategies** in environments that change over time.
- Lets you ask: *"Which strategy detects state changes best? At what cost? Under which kind of environment?"*
- Built for rapid iteration — swap strategies, swap environments, rerun, compare.

### What it does under the hood

- Simulates a strategy deciding when to sample as the environment shifts.
- Tracks each sample's decision, the environment state, and the cost.
- Supports three environment models:
  - **Preset** — scripted, repeatable state changes.
  - **Markovian** — state changes follow fixed transition probabilities.
  - **TimeCorrelations** — state depends on recent history.

## Goals

- Test how well different sampling strategies detect changes in the environment.
- Keep strategy and environment behavior **configurable via YAML** — no code changes needed.
- Compare **active vs passive sampling** in terms of detection and cost.
- Provide a **simple demo** for quick experiments.

## Strategies

Five strategies are built in. Here's the quick read on each:

| Strategy | In a sentence | Good at | Catch |
|---|---|---|---|
| **Bayesian** | The careful one. | Cheapest overall, low false active rate. | Misses a bit more than the reactive ones. |
| **WaitingTime** | Quick to react, slow to let go. | Best detection on Markovian & Preset. | Samples a lot. |
| **Responsive** | Same idea as WaitingTime. | Best detection on TimeCorrelations. | Samples a lot. |
| **Random** | Not a real strategy — a reference point. | `p=1.0` = sample everything, `p=0.0` = sample nothing. | Ignores all signal. |
| **Periodic** | Samples on a fixed schedule. | Predictable, fixed cost. | Misses about half the changes. |

> **Our rule:** detection beats cost. We'll pay a bit more to miss less.

> **Researched, not implemented:** CUSUM (Page's cumulative-sum change-point detector) has been researched but isn't in the code yet. See [outputs/current_strategies.md](outputs/current_strategies.md) for the writeup.

### Who wins what

- Settings: **100 seeds, T=600**. "Non-degenerate" means `false_active ≤ 0.7`.

| Environment | Cheapest | Best detection | Fewest false alarms |
|---|---|---|---|
| Markovian | **Bayesian** (720) | WaitingTime cap=100 (0.029) | **Bayesian** (0.057) |
| TimeCorrelations | **Bayesian** (823) | Responsive cap=20 (0.045) | **Bayesian** (0.166) |
| Preset | **Bayesian** (803) | WaitingTime cap=50 (0.032) | **Bayesian** (0.078) |

- Full data and the reasoning behind these defaults → [outputs/](outputs/).
- Start with [outputs/README.md](outputs/README.md) and [outputs/current_strategies.md](outputs/current_strategies.md).

## Setup

**1. Create and activate a virtual environment:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```
- If `python3 -m venv` is missing, install it first (e.g. `sudo apt install python3-venv` on Debian/Ubuntu).

**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

**3. Run the demo:**
```bash
python scripts/run_demo.py
```

## Dependencies

- `numpy`
- `matplotlib`
- `pyyaml`

## Repository Structure

- `README.md`
- `requirements.txt`
- `configs/` — YAML configs.
  - `custom_simulation_outline.yml`
  - `modulation.yml`
- `scripts/`
  - `run_demo.py` — run a single simulation, save CSV.
  - `run_comparison.py` — run multiple strategies across many seeds, print aggregated metrics.
- `src/dynamic_datasampling_sim/` — core library.
  - `config.py`, `config_loader.py`, `simulation_config.py` — config loading.
  - `environment.py` — environment models.
  - `strategy.py`, `sampling.py` — sampling strategies.
  - `simulation.py` — the simulator loop.
  - `harness.py` — multi-seed evaluation harness.
  - `metrics.py` — per-run metrics.
  - `plotting.py` — plotting helpers.
- `outputs/` — research artifacts: findings docs, sweep CSVs, rerunnable scripts. See [outputs/README.md](outputs/README.md).

## Usage

### Run with default config
```bash
python3 scripts/run_demo.py
```

- Prints simulation arrays.
- Saves results to `outputs/demo_runs/simulation_results.csv`.

### Run with a custom config
```bash
python3 scripts/run_demo.py --config configs/custom_simulation_outline.yml --output outputs/demo_runs/custom_results.csv
```

### Print a terminal summary
- Shows relevance, quality, and cost.
```bash
python3 scripts/run_demo.py --config configs/custom_simulation_outline.yml --summary
```

### CSV output format

- One row per sample:
  ```csv
  time,environment_state,sample,cost
  ```
- Load into any visualization tool, e.g. [RAWGraphs](https://www.rawgraphs.io/), Plotly Chart Studio, Excel, Google Sheets, or LibreOffice Calc.

## How We Evaluate Strategies

- **Never trust a single run.** One seed can be lucky or unlucky and flip the ranking.
- Every comparison goes through the harness at [src/dynamic_datasampling_sim/harness.py](src/dynamic_datasampling_sim/harness.py).

### Standard recipe used in [outputs/](outputs/)

- Each `(strategy, environment)` pair runs for **T = 600 time steps**.
- Each pair runs across **100 random seeds**.
- Every strategy runs on every environment — full cross product.
- Per-run metrics come from [metrics.py](src/dynamic_datasampling_sim/metrics.py):
  - `total_cost`
  - `missed_active_fraction`
  - `false_active_fraction`
  - `cost_per_relevant_sample`
- `aggregate()` reports **mean, std, and n** per metric, so spread across seeds is visible.

### Run a comparison (easy way)

A ready-made script lives at [scripts/run_comparison.py](scripts/run_comparison.py):

```bash
python3 scripts/run_comparison.py
```

- Runs WaitingTime, Responsive, and Bayesian on the Markovian env.
- 100 seeds each.
- Prints aggregated metrics (cost, miss, false_active) to the terminal.

### Customize the comparison

- Open [scripts/run_comparison.py](scripts/run_comparison.py) and edit the `runs` list.
- Each entry is one strategy/environment pair:
  ```python
  {"label": "Bayesian", "strattype": "Bayesian", "environtype": "TimeCorrelations", "T": 600}
  ```
- Valid `strattype` values: `Bayesian`, `WaitingTime`, `Responsive`, `Random`, `Periodic`.
- Valid `environtype` values: `Preset`, `Markovian`, `TimeCorrelations`.

### Use the harness in your own code

```python
from dynamic_datasampling_sim.harness import run_experiment, aggregate

runs = [{"label": "Bayesian", "strattype": "Bayesian", "environtype": "Markovian", "T": 600}]
rows = run_experiment(runs, n_seeds=100)
summary = aggregate(rows, group_keys=("label",))
```

- `rows` = one dict per `(run, seed)` cell.
- Convert with `pd.DataFrame(rows)` to slice, plot, or export.
- Sweep CSVs in [outputs/data/](outputs/data/) were built this way.

## Status

- **YAML-based modulation** is built and currently in testing.
- Being validated across environment and strategy combinations to confirm correct behavior.

## TODO

- Add a chart of the Henry preset data with an explanation.
