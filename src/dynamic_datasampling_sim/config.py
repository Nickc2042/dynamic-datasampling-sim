"""Typed configuration objects for simulation settings."""

# ============================================================
# IMPORTS
# ============================================================
from dataclasses import dataclass, field
import math
from numbers import Real

# Most of these settings are copied from simulation_config.py, but with slight adjustments to better fit the new structure


# ============================================================
# SUPPORTED TYPES
# ============================================================
SUPPORTED_STRATEGY_TYPES = {"Responsive", "WaitingTime", "Periodic", "Random", "Bayesian"} # Add to this set when new strategy types are added in strategy.py
# Note: "CUSUM" is researched but not implemented yet — see outputs/current_strategies.md.
SUPPORTED_ENVIRONMENT_TYPES = {"Markovian", "OneState", "Preset", "TimeCorrelations"} # Add to this set when new environment types are added in environment.py


# ============================================================
# VALIDATION HELPERS
# ============================================================
def _is_real_number(value): # A real number validator that returns False for bools, since bools are technically ints in Python but we don't want to allow them for numeric settings
    """Return True when value is a finite int/float, but not a bool."""
    return isinstance(value, Real) and not isinstance(value, bool) and math.isfinite(value)


# ============================================================
# STRATEGY CONFIG
# ============================================================
@dataclass
class StrategyConfig:
    """Settings that control sampling strategy behavior."""
    # Default values here will still be the same from initial code

    # ---- Core state ----
    initial_strategy_state: bool = False
    high_quality_enabled: bool = True

    # ---- Sampling frequencies ----
    active_sampling_frequency: float = 1
    passive_sampling_frequency: float = 1
    initial_sampling_frequency: float = 1

    # ---- Memory ----
    memory_cap: int = 40  # WaitingTime — see outputs/memory_cap_findings.md
    responsive_memory_cap: int = 20  # Responsive — see outputs/hysteresis_findings.md (responsive vs waitingtime cap sweep)
    initial_memory: int = 0

    # ---- Costs ----
    sampling_costs: list[float] = field(default_factory=lambda: [1, 2])
    initial_current_cost: float = 1

    # ---- Periodic strategy ----
    # Periodic strategy: alternate between active for N decision steps, then passive for M decision steps
    periodic_active_duration: int = 1
    periodic_passive_duration: int = 1

    # ---- Random strategy ----
    # Random strategy: P(state = active) on each decision step
    activation_probability: float = 0.5

    # ---- Bayesian strategy ----
    # Bayesian strategy: Bayes-filter posterior P(env=active | observations); fixed priors
    bayesian_threshold: float = 0.5  # activate when belief > threshold
    bayesian_p_activate: float = 0.01  # prior P(passive -> active) per decision step
    bayesian_p_deactivate: float = 0.05  # prior P(active -> passive)
    bayesian_p_rel_given_active: float = 0.9  # P(sample relevant | env active)
    bayesian_p_rel_given_passive: float = 0.01  # P(sample relevant | env passive)

    # ---- Ready strategy (trinary expansion) ----
    # Ready strategy: the after-Active watch state. Entered from Active when the event
    # seems to be ending; samples nearly as aggressively as Active to catch resurgence,
    # then returns to Passive after a fixed quiet countdown.

    # Note to sefl: I still don't like having two configs. After Ready state implementation, do something about this
    ready_enabled: bool = True  # global on/off; when False, behavior is the original Passive/Active binary
    ready_sampling_frequency: float = 1  # sample rate in Ready, keep close to active freq so resurgence isn't missed
    ready_countdown: int = 5  # quiet (no relevant data) steps in Ready before -> Passive
    ready_cost: float = 1.5  # cost per sample in Ready, between sampling_costs[0] and [1]

    # ---- CUSUM strategy (researched, not implemented) ----
    # Placeholder for a future Page's cumulative-sum change-point detector. Researched
    # but not implemented yet — config fields intentionally omitted until it lands.
    # See outputs/current_strategies.md for the design.

    # ------------------------------------------------------------
    # VALIDATION
    # ------------------------------------------------------------


    def validate(self):
        """Validate strategy settings."""

        # ---- Core state flags ----
        # Strategy state flags must be booleans because they directly control on/off behavior
        if not isinstance(self.initial_strategy_state, bool):
            raise ValueError("initial_strategy_state must be true or false.")

        if not isinstance(self.high_quality_enabled, bool):
            raise ValueError("high_quality_enabled must be true or false.")

        # ---- Sampling frequencies ----
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

        # ---- Memory ----
        # memory_cap and responsive_memory_cap must be positive integers
        for field_name in ("memory_cap", "responsive_memory_cap"):
            value = getattr(self, field_name)
            if not isinstance(value, int) or isinstance(value, bool):
                raise ValueError(f"{field_name} must be an integer.")
            if value <= 0:
                raise ValueError(f"{field_name} must be greater than 0.")
        if not isinstance(self.initial_memory, int) or isinstance(self.initial_memory, bool):
            raise ValueError("initial_memory must be an integer.")
        if self.initial_memory < 0:
            raise ValueError("initial_memory cannot be negative.")

        # ---- Costs ----
        # Add Description
        if not isinstance(self.sampling_costs, list):
            raise ValueError("sampling_costs must be a list.")
        if len(self.sampling_costs) != 2 or any(not _is_real_number(cost) or cost < 0 for cost in self.sampling_costs):
            raise ValueError("sampling_costs must contain two non-negative values.")

        # Initial cost should be usable as a numeric cost before the first strategy update
        if not _is_real_number(self.initial_current_cost) or self.initial_current_cost < 0:
            raise ValueError("initial_current_cost must be a non-negative number.")

        # ---- Periodic strategy ----
        # Periodic strategy durations: positive integers (no degenerate corners)
        for field_name in ("periodic_active_duration", "periodic_passive_duration"):
            value = getattr(self, field_name)
            if not isinstance(value, int) or isinstance(value, bool):
                raise ValueError(f"{field_name} must be an integer.")
            if value < 1:
                raise ValueError(f"{field_name} must be at least 1.")

        # ---- Random strategy ----
        # Random strategy activation probability: in [0, 1]
        if not _is_real_number(self.activation_probability):
            raise ValueError("activation_probability must be a number.")
        if self.activation_probability < 0 or self.activation_probability > 1:
            raise ValueError("activation_probability must be between 0 and 1.")

        # ---- Bayesian strategy ----
        # Bayesian strategy: threshold, transition priors, likelihoods, initial belief all in [0, 1]
        for field_name in (
            "bayesian_threshold",
            "bayesian_p_activate",
            "bayesian_p_deactivate",
            "bayesian_p_rel_given_active",
            "bayesian_p_rel_given_passive",
        ):
            value = getattr(self, field_name)
            if not _is_real_number(value):
                raise ValueError(f"{field_name} must be a number.")
            if value < 0 or value > 1:
                raise ValueError(f"{field_name} must be between 0 and 1.")

        # ---- Ready strategy ----
        # ready_enabled gates the whole trinary state machine, so it must be a boolean
        if not isinstance(self.ready_enabled, bool):
            raise ValueError("ready_enabled must be true or false.")

        # ready_sampling_frequency mirrors the active/passive frequency checks: a positive number
        if not _is_real_number(self.ready_sampling_frequency):
            raise ValueError("ready_sampling_frequency must be a number.")
        if self.ready_sampling_frequency <= 0:
            raise ValueError("ready_sampling_frequency must be greater than 0.")

        # ready_countdown counts decision steps, so it must be a positive integer (>= 1)
        if not isinstance(self.ready_countdown, int) or isinstance(self.ready_countdown, bool):
            raise ValueError("ready_countdown must be an integer.")
        if self.ready_countdown < 1:
            raise ValueError("ready_countdown must be at least 1.")

        # ready_cost is a per-sample cost like sampling_costs, so it must be non-negative
        if not _is_real_number(self.ready_cost) or self.ready_cost < 0:
            raise ValueError("ready_cost must be a non-negative number.")


# ============================================================
# ENVIRONMENT CONFIG
# ============================================================
@dataclass
class EnvironmentConfig:
    """Settings that control environment state and sample generation."""
    # Default values here will still be the same from initial code

    # ---- Core state ----
    initial_environment_state: bool = False

    # ---- Probabilities ----
    transition_probabilities: list[float] = field(default_factory=lambda: [0.05, 0.01])
    sample_probabilities: list[float] = field(default_factory=lambda: [0.9, 0.99])

    # ---- Time correlation intervals ----
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
    # ---- Preset data ----
    preset_data: list[int] = field(default_factory=list) # This is a placeholder for now

    # ------------------------------------------------------------
    # VALIDATION
    # ------------------------------------------------------------


    def validate(self, simulation_time, environment_type, strategy_config):
        """Validate environment settings."""

        # ---- Core state ----
        # Environment state must be a boolean because sampling logic branches on active/inactive
        if not isinstance(self.initial_environment_state, bool):
            raise ValueError("initial_environment_state must be true or false.")

        # ---- Probabilities ----
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

        # ---- Time correlation intervals ----
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

        # ---- Preset data ----
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


# ============================================================
# TOP-LEVEL SIMULATION CONFIG
# ============================================================
@dataclass
class SimulationConfig:
    """Top-level settings for one simulation run."""

    # ---- Run defaults ----
    default_strategy_type: str= "WaitingTime" # Maybe add some more comments later on to improve code readability?
    default_environment_type: str = "Preset" # Yet to move preset data, so this us more like a placeholder for now
    default_simulation_time: int = 600 # Default

    # ---- Nested configs ----
    strategy: StrategyConfig = field(default_factory=StrategyConfig)
    environment: EnvironmentConfig = field(default_factory=EnvironmentConfig)

    # ------------------------------------------------------------
    # VALIDATION
    # ------------------------------------------------------------


    def validate(self, simulation_time = None, strategy_type = None, environment_type = None):
        """Validate the full simulation configuration."""

        # ---- Resolve defaults ----
        #
        if simulation_time is None:
            simulation_time = self.default_simulation_time
        if strategy_type is None:
            strategy_type = self.default_strategy_type
        if environment_type is None:
            environment_type = self.default_environment_type

        # ---- Strategy / environment names ----
        # Validate the actual strategy/environment names that will be used for this run
        if strategy_type not in SUPPORTED_STRATEGY_TYPES:
            raise ValueError(f"strategy_type must be one of {sorted(SUPPORTED_STRATEGY_TYPES)}.")

        if environment_type not in SUPPORTED_ENVIRONMENT_TYPES:
            raise ValueError(f"environment_type must be one of {sorted(SUPPORTED_ENVIRONMENT_TYPES)}.")

        # ---- Simulation time ----
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

        # ---- Nested config validation ----
        # Validate nested configs as well
        self.strategy.validate()
        self.environment.validate (
            simulation_time=simulation_time,
            environment_type=environment_type,
            strategy_config=self.strategy,)
