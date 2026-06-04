"""Typed configuration objects for simulation settings."""

from dataclasses import dataclass, field

# Most of these settings are copied from simulation_config.py, but with slight adjustments to better fit the new structure

@dataclass
class StrategyConfig:
    """Settings that control sampling strategy behavior."""
    # Default values here will still be the same from initial code

    initial_strategy_state: bool = False
    high_quality_enabled: bool = True

    active_sampling_frequency: float = 1
    passive_sampling_frequency: float = 1
    initial_sampling_frequency: float = 1

    memory_cap: int = 10
    initial_memory: int = 0

    sampling_costs: list[float] = field(default_factory=lambda: [1, 2])
    initial_current_cost: float = 1


@dataclass
class EnvironmentConfig:
    """Settings that control environment state and sample generation."""
    # Default values here will still be the same from initial code

    initial_environment_state: bool = False
    transition_probabilities: list[float] = field(default_factory=lambda: [0.05, 0.01])
    sample_probabilities: list[float] = field(default_factory=lambda: [0.9, 0.99])

    time_correlation_intervals: list[list[int]] = field(
        default_factory=lambda: [
            [6, 19],
            [33, 40],
            [51, 58],
            [73, 79],
            [137, 144],
            [150, 165],
            [178, 203],
            [233, 265],
            [311, 315],
            [323, 328],
            [353, 360],
            [402, 408],
            [458, 464],
            [470, 476],
            [485, 490],
            [547, 559],
            [575, 599],
        ]
    )
    preset_data: list[int] = field(default_factory=list) # This is a placeholder for now


@dataclass
class SimulationConfig:
    """Top-level settings for one simulation run."""

    default_strategy_type: str= "WaitingTime" # Maybe add some more comments later on to improve code readability?
    default_environment_type: str = "Preset" # Yet to move preset data, so this us more like a placeholder for now
    default_simulation_time: int = 600 # Default

    strategy: StrategyConfig = field(default_factory=StrategyConfig)
    environment: EnvironmentConfig = field(default_factory=EnvironmentConfig)
