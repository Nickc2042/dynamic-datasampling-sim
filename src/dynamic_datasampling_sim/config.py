"""Typed configuration objects for simulation settings."""

from dataclasses import dataclass, field
import math
from numbers import Real

# Most of these settings are copied from simulation_config.py, but with slight adjustments to better fit the new structure

SUPPORTED_STRATEGY_TYPES = {"Responsive", "WaitingTime"} # Add to this set when new strategy types are added in strategy.py
SUPPORTED_ENVIRONMENT_TYPES = {"Markovian", "OneState", "Preset", "TimeCorrelations"} # Add to this set when new environment types are added in environment.py


def _is_real_number(value): # A real number validator that returns False for bools, since bools are technically ints in Python but we don't want to allow them for numeric settings
    """Return True when value is a finite int/float, but not a bool."""
    return isinstance(value, Real) and not isinstance(value, bool) and math.isfinite(value)

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

    # VALIDATION below


    def validate(self):
        """Validate strategy settings."""

        # Strategy state flags must be booleans because they directly control on/off behavior
        if not isinstance(self.initial_strategy_state, bool):
            raise ValueError("initial_strategy_state must be true or false.")

        if not isinstance(self.high_quality_enabled, bool):
            raise ValueError("high_quality_enabled must be true or false.")

        # active/passive_sampling_frequency <= 0
        if not _is_real_number(self.active_sampling_frequency) or not _is_real_number(self.passive_sampling_frequency):
            raise ValueError("sampling frequencies must be numbers.")
        if self.active_sampling_frequency <= 0 or self.passive_sampling_frequency <= 0:
            raise ValueError("sampling frequencies must be greater than 0.")

        # initial_sampling_frequency <= 0
        if not _is_real_number(self.initial_sampling_frequency):
            raise ValueError("initial_sampling_frequency must be a number.")
        if self.initial_sampling_frequency <= 0:
            raise ValueError("initial_sampling_frequency must be greater than 0.")

        # memory_cap <= 0 or initial_memory < 0
        if not isinstance(self.memory_cap, int) or isinstance(self.memory_cap, bool):
            raise ValueError("memory_cap must be an integer.")
        if self.memory_cap <= 0:
            raise ValueError("memory_cap must be greater than 0.")
        if not isinstance(self.initial_memory, int) or isinstance(self.initial_memory, bool):
            raise ValueError("initial_memory must be an integer.")
        if self.initial_memory < 0:
            raise ValueError("initial_memory cannot be negative.")

        # Add Description
        if not isinstance(self.sampling_costs, list):
            raise ValueError("sampling_costs must be a list.")
        if len(self.sampling_costs) != 2 or any(not _is_real_number(cost) or cost < 0 for cost in self.sampling_costs):
            raise ValueError("sampling_costs must contain two non-negative values.")

        # Initial cost should be usable as a numeric cost before the first strategy update
        if not _is_real_number(self.initial_current_cost) or self.initial_current_cost < 0:
            raise ValueError("initial_current_cost must be a non-negative number.")

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

    # VALIDATION below


    def validate(self, simulation_time, environment_type, strategy_config):
        """Validate environment settings."""

        # Environment state must be a boolean because sampling logic branches on active/inactive
        if not isinstance(self.initial_environment_state, bool):
            raise ValueError("initial_environment_state must be true or false.")

        # transition_probabilities and sample_probabilities must each contain two values between 0 and 1
        if not isinstance(self.transition_probabilities, list):
            raise ValueError("transition_probabilities must be a list.")
        if len(self.transition_probabilities) != 2 or any(
            not _is_real_number(probability) or probability < 0 or probability > 1 for probability in self.transition_probabilities
        ):
            raise ValueError("transition_probabilities must contain two values between 0 and 1.")

        # sample_probabilities must contain two values between 0 and 1
        if not isinstance(self.sample_probabilities, list):
            raise ValueError("sample_probabilities must be a list.")
        if len(self.sample_probabilities) != 2 or any(
            not _is_real_number(probability) or probability < 0 or probability > 1 for probability in self.sample_probabilities
        ):
            raise ValueError("sample_probabilities must contain two values between 0 and 1.")

        # time_correlation_intervals must contain [start, end] pairs with start < end
        if not isinstance(self.time_correlation_intervals, list):
            raise ValueError("time_correlation_intervals must be a list.")
        if any(
            not isinstance(interval, list)
            or len(interval) != 2
            or not _is_real_number(interval[0])
            or not _is_real_number(interval[1])
            or interval[0] < 0
            or interval[0] >= interval[1]
            for interval in self.time_correlation_intervals
        ):
            raise ValueError("time_correlation_intervals must contain non-negative [start, end] pairs with start < end.")

        # TimeCorrelations needs at least one interval to describe when the environment is active
        if environment_type== "TimeCorrelations" and len(self.time_correlation_intervals) == 0:
            raise ValueError("time_correlation_intervals cannot be empty for a TimeCorrelations environment.")

        # Preset data should be an explicit 0/1 sequence so it can index environment states cleanly
        if not isinstance(self.preset_data, list):
            raise ValueError("preset_data must be a list.")
        if any(value not in {0, 1, False, True} for value in self.preset_data):
            raise ValueError("preset_data must contain only 0/1 values.")

        # If environment_type is "Preset", preset_data must cover the largest possible look-ahead update
        if environment_type == "Preset":
            max_update_step = 1 / min(strategy_config.active_sampling_frequency, strategy_config.passive_sampling_frequency)
            required_preset_length = math.ceil(simulation_time + max_update_step)
            if len(self.preset_data) < required_preset_length:
                raise ValueError(
                    f"preset_data must contain at least {required_preset_length} values for this simulation_time and sampling frequency."
                )


@dataclass
class SimulationConfig:
    """Top-level settings for one simulation run."""

    default_strategy_type: str= "WaitingTime" # Maybe add some more comments later on to improve code readability?
    default_environment_type: str = "Preset" # Yet to move preset data, so this us more like a placeholder for now
    default_simulation_time: int = 600 # Default

    strategy: StrategyConfig = field(default_factory=StrategyConfig)
    environment: EnvironmentConfig = field(default_factory=EnvironmentConfig)

    # VALIDATION below
    

    def validate(self, simulation_time = None, strategy_type = None, environment_type = None):
        """Validate the full simulation configuration."""

        #
        if simulation_time is None:
            simulation_time = self.default_simulation_time
        if strategy_type is None:
            strategy_type = self.default_strategy_type
        if environment_type is None:
            environment_type = self.default_environment_type

        # Validate the actual strategy/environment names that will be used for this run
        if strategy_type not in SUPPORTED_STRATEGY_TYPES:
            raise ValueError(f"strategy_type must be one of {sorted(SUPPORTED_STRATEGY_TYPES)}.")

        if environment_type not in SUPPORTED_ENVIRONMENT_TYPES:
            raise ValueError(f"environment_type must be one of {sorted(SUPPORTED_ENVIRONMENT_TYPES)}.")

        # default_simulation_time and simulation_time are greater than 0
        if not _is_real_number(self.default_simulation_time):
            raise ValueError("default_simulation_time must be a number.")
        if self.default_simulation_time <= 0:
            raise ValueError("default_simulation_time must be greater than 0.")

        # simulation_time may be overridden at runtime, so validate it separately from the default
        if not _is_real_number(simulation_time):
            raise ValueError("simulation_time must be a number.")
        if simulation_time <= 0:
            raise ValueError("simulation_time must be greater than 0.")

        # Validate nested configs as well
        self.strategy.validate()
        self.environment.validate (
            simulation_time=simulation_time,
            environment_type=environment_type,
            strategy_config=self.strategy,)
