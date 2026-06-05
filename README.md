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

To Do

## Testing

To Do

## Status

To Do
