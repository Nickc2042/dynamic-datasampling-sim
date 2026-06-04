"""Load YAML configuration files into typed simulation config objects."""

from pathlib import Path

import yaml

from .config import EnvironmentConfig, SimulationConfig, StrategyConfig


def load_config(path):
    """Load a simulation configuration from a YAML file."""
    config_path = Path(path)

    # Read the user-provided YAML file into plain Python dictionaries.
    with config_path.open("r", encoding="utf-8") as config_file:
        data = yaml.safe_load(config_file) or {}

    # Pull out nested sections before building the top level config
    strategy_data = data.get("strategy", {})
    environment_data = data.get("environment", {})

    # Convert raw dictionaries into typed config objects
    strategy = StrategyConfig(**strategy_data)
    environment = EnvironmentConfig(**environment_data)

    # Keep only top-level simulation settings here
    simulation_data = {
        key: value
        for key, value in data.items()
        if key not in {"strategy", "environment"}
    }

    config = SimulationConfig(
        **simulation_data,
        strategy=strategy,
        environment=environment,
    )

    config.validate()
    
    return config
