"""Load YAML configuration files into typed simulation config objects."""

from dataclasses import fields
from pathlib import Path

import yaml

from .config import EnvironmentConfig, SimulationConfig, StrategyConfig


def _check_unknown_keys(section_name, data, config_class):
    """Raise a clear error when a YAML section contains unsupported settings."""
    # COmpare YAML keys against dataclass fields so typos fail early
    valid_keys = {field.name for field in fields(config_class)}
    unknown_keys = set(data) - valid_keys

    if unknown_keys:
        raise ValueError(f"{section_name} contains unknown settings: {sorted(unknown_keys)}")


def load_config(path):
    """Load a simulation configuration from a YAML file."""
    config_path = Path(path)

    # Read the user-provided YAML file into plain Python dictionaries.
    with config_path.open("r", encoding="utf-8") as config_file:
        data = yaml.safe_load(config_file) or {}

    # The root YAML object should be a mapping of setting names to values
    if not isinstance(data, dict):
        raise ValueError("config file must contain YAML key/value settings.")

    # Pull out nested sections before building the top level config
    strategy_data = data.get("strategy", {})
    environment_data = data.get("environment", {})

    # Nested config sections should also be mappings, not lists or plain values
    if not isinstance(strategy_data, dict):
        raise ValueError("strategy section must contain YAML key/value settings.")
    if not isinstance(environment_data, dict):
        raise ValueError("environment section must contain YAML key/value settings.")

    _check_unknown_keys("strategy", strategy_data, StrategyConfig)
    _check_unknown_keys("environment", environment_data, EnvironmentConfig)

    # Convert raw dictionaries into typed config objects
    strategy = StrategyConfig(**strategy_data)
    environment = EnvironmentConfig(**environment_data)

    # Keep only top-level simulation settings here
    simulation_data = {
        key: value
        for key, value in data.items()
        if key not in {"strategy", "environment"}
    }
    _check_unknown_keys("top-level config", simulation_data, SimulationConfig)

    config = SimulationConfig(
        **simulation_data,
        strategy=strategy,
        environment=environment,
    )

    config.validate()
    
    return config
