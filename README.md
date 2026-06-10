# Dynamic Data Sampling Simulation

## Short Description

Dynamic Data Sampling Simulation is a Python project for experimenting with adaptive sampling strategies over changing environments. The simulator supports preset, Markovian, and time-correlated environment models while tracking sample decisions, environment state, and sampling cost.

## Project Goals

- Evaluate dynamic sampling strategies in simulated time-varying environments.
- Make strategy and environment behavior configurable without modifying core simulator logic.
- Compare active and passive sampling tradeoffs in terms of state detection and cost.
- Provide a minimal demo entry point for rapid experimentation.

## Setup

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
   - If `python3 -m venv` is unavailable, install the system package first (for example `sudo apt install python3-venv` on Debian/Ubuntu).
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the demo simulation:
   ```bash
   python scripts/run_demo.py
   ```

## Dependencies

- numpy
- matplotlib
- pyyaml

## Repository Structure

- `README.md`
- `requirements.txt`
- `configs/`
  - `custom_simulation_outline.yml`
  - `modulation.yml`
- `scripts/`
  - `run_demo.py`
- `src/dynamic_datasampling_sim/`
  - `__init__.py`
  - `config_loader.py`
  - `config.py`
  - `environment.py`
  - `plotting.py`
  - `sampling.py`
  - `simulation_config.py`
  - `simulation.py`
  - `strategy.py`

## Usage

Run the default YAML-driven simulation:
```bash
python3 scripts/run_demo.py
```

The script prints the simulation arrays and also saves a CSV file to:
```bash
outputs/simulation_results.csv
```

The CSV contains one row per sample:
```csv
time,environment_state,sample,cost
```

To use a custom simulation config and choose where the CSV is saved:
```bash
python3 scripts/run_demo.py --config configs/custom_simulation_outline.yml --output outputs/custom_results.csv
```

To also print a terminal summary of relevance, quality, and cost:
```bash
python3 scripts/run_demo.py --config configs/custom_simulation_outline.yml --summary
```

The CSV can be loaded into external visualization tools such as [RAWGraphs](https://www.rawgraphs.io/), Plotly Chart Studio, Excel, Google Sheets, or LibreOffice Calc. This keeps the project focused on simulation while letting users create whatever chart or graph they need from the exported data.

## Testing

To run tests with a custom configuration file, use:
```bash
.venv/bin/python scripts/run_demo.py --config path/to/config.yml
```

## Status

The modulation feature was created using YAML-based configuration and is currently in testing. The system is being validated with various environment and strategy combinations to ensure correct behavior across different sampling scenarios.

# Add graph/chart of Henry preset data and explanation around top