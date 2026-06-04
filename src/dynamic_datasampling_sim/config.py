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

    def validate(self):
        """Validate strategy settings."""

        # active/passive_sampling_frequency <= 0
        if self.active_sampling_frequency <= 0 or self.passive_sampling_frequency <= 0:
            raise ValueError("sampling frequencies must be greater than 0.")

        # initial_sampling_frequency <= 0
        if self.initial_sampling_frequency <= 0:
            raise ValueError("initial_sampling_frequency must be greater than 0.")

        # memory_cap <= 0 or initial_memory < 0
        if self.memory_cap <= 0:
            raise ValueError("memory_cap must be greater than 0.")
        if self.initial_memory < 0:
            raise ValueError("initial_memory cannot be negative.")

        # Add Description
        if len(self.sampling_costs) != 2 or any(cost < 0 for cost in self.sampling_costs):
            raise ValueError("sampling_costs must contain two non-negative values.")


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

    def validate(self, simulation_time, environment_type):
        """Validate environment settings."""

        # transition_probabilities and sample_probabilities must each contain two values between 0 and 1
        if len(self.transition_probabilities) != 2 or any(
            probability < 0 or probability > 1 for probability in self.transition_probabilities
        ):
            raise ValueError("transition_probabilities must contain two values between 0 and 1.")

        # sample_probabilities must contain two values between 0 and 1
        if len(self.sample_probabilities) != 2 or any(
            probability < 0 or probability > 1 for probability in self.sample_probabilities
        ):
            raise ValueError("sample_probabilities must contain two values between 0 and 1.")

        # time_correlation_intervals must contain [start, end] pairs with start < end
        if any(
            len(interval) != 2 or interval[0] >= interval[1]
            for interval in self.time_correlation_intervals
        ):
            raise ValueError("time_correlation_intervals must contain [start, end] pairs with start < end.")

        # If environment_type is "Preset", preset_data must be at least as long as simulation_time
        if environment_type== "Preset" and len(self.preset_data) < simulation_time:
            raise ValueError("preset_data must be at least as long as simulation_time.")


@dataclass
class SimulationConfig:
    """Top-level settings for one simulation run."""

    default_strategy_type: str= "WaitingTime" # Maybe add some more comments later on to improve code readability?
    default_environment_type: str = "Preset" # Yet to move preset data, so this us more like a placeholder for now
    default_simulation_time: int = 600 # Default

    strategy: StrategyConfig = field(default_factory=StrategyConfig)
    environment: EnvironmentConfig = field(default_factory=EnvironmentConfig)

    def validate(self, simulation_time=None):
        """Validate the full simulation configuration."""

        #
        if simulation_time is None:
            simulation_time = self.default_simulation_time

        # default_simulation_time and simulation_time are greater than 0
        if self.default_simulation_time <= 0:
            raise ValueError("default_simulation_time must be greater than 0.")

        if simulation_time <= 0:
            raise ValueError("simulation_time must be greater than 0.")

        # Validate nested configs as well
        self.strategy.validate()
        self.environment.validate (
            simulation_time=simulation_time,
            environment_type=self.default_environment_type,
        )
