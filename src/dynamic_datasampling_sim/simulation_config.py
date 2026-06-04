"""Default simulation settings.

Edit these values to customize the simulation without changing the core
simulation logic.
"""
# Simulation defaults
default_strategy_type = "WaitingTime" # "WaitingTime", "Responsive"; update when more are added
default_environment_type = "Preset" # "Preset", "Markovian", "OneState", "TimeCorrelations"; update when more are added
default_simulation_time = 600 # This value is usually changed

# Strategy defaults
initial_strategy_state = False # Starts in active state when True
high_quality_enabled = True # Adds high quality sample marker when active
active_sampling_frequency = 1 # Try to have this higher or equal to passive_sampling_frequency
passive_sampling_frequency = 1
initial_sampling_frequency = 1 # Starting sample rate before strategy updates
memory_cap = 10 # Samples remembered before state reset
initial_memory = 0 # Usually unchanged, but can be set to a positive value
sampling_costs = [1, 2]
initial_current_cost = 1

# Environment defaults
initial_environment_state = False # Starts active when True
transition_probabilities = [0.05, 0.01]  # True-to-False, False-to-True
sample_probabilities = [0.9, 0.99]  # True returns True, False returns False
time_correlation_intervals = [
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
preset_data = [ # Maybe add a function which can take in custom preset data, but keep this as default preset data
    0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1,
    0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
    1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
]


# Validation function to make sure configuration values are reasonable. Can be edited to add more checks as needed. But usually do not change
def validate_config(simulation_time=None):
    """Validate the current configuration values."""
    if simulation_time is None:
        simulation_time = default_simulation_time

    if default_simulation_time <= 0:
        raise ValueError("default_simulation_time must be greater than 0.")

    if simulation_time <= 0:
        raise ValueError("simulation_time must be greater than 0.")

    if active_sampling_frequency <= 0 or passive_sampling_frequency <= 0:
        raise ValueError("sampling frequencies must be greater than 0.")

    if initial_sampling_frequency <= 0:
        raise ValueError("initial_sampling_frequency must be greater than 0.")

    if memory_cap <= 0:
        raise ValueError("memory_cap must be greater than 0.")

    if initial_memory < 0:
        raise ValueError("initial_memory cannot be negative.")

    if len(sampling_costs) != 2 or any(cost < 0 for cost in sampling_costs):
        raise ValueError("sampling_costs must contain two non-negative values.")

    if len(transition_probabilities) != 2 or any(
        probability < 0 or probability > 1 for probability in transition_probabilities
    ):
        raise ValueError("transition_probabilities must contain two values between 0 and 1.")

    if len(sample_probabilities) != 2 or any(
        probability < 0 or probability > 1 for probability in sample_probabilities
    ):
        raise ValueError("sample_probabilities must contain two values between 0 and 1.")

    if any(
        len(interval) != 2 or interval[0] >= interval[1]
        for interval in time_correlation_intervals
    ):
        raise ValueError("time_correlation_intervals must contain [start, end] pairs with start < end.")

    if len(preset_data) < simulation_time:
        raise ValueError("preset_data must be at least as long as simulation_time.")