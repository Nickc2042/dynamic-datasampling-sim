# ============================================================
# IMPORTS
# ============================================================
import numpy as np

from . import simulation_config as default_config # Almost exactly the same as strategy.py , I will designate the default values from simulation_config.py, but we will pull them into an EnvironmentConfig object to keep things organized

from .config import EnvironmentConfig


# ============================================================
# LEGACY CONFIG HELPER
# ============================================================
def _legacy_environment_config():

    """Build an EnvironmentConfig from the old global defaults - simulation_config.py"""
    return EnvironmentConfig(
        # ---- Core state ----
        initial_environment_state = default_config.initial_environment_state,

        # ---- Probabilities ----
        transition_probabilities = default_config.transition_probabilities,
        sample_probabilities = default_config.sample_probabilities,

        # ---- Time correlation & preset data ----
        time_correlation_intervals = default_config.time_correlation_intervals,
        preset_data = default_config.preset_data, #supports new variables for future expansion without needing to change this function. Add after this line
    )


# ============================================================
# ENVIRONMENT CLASS
# ============================================================
class environment:
    def __init__(self, environtype = "Markovian", environment_config=None):
        if environment_config is None:
            environment_config = _legacy_environment_config()

        # ---- Core state ----
        self.environtype = environtype
        self.state = environment_config.initial_environment_state

        # ---- Probabilities ----
        self.transprobs = np.array(environment_config.transition_probabilities)
        self.sampleprobs = np.array(environment_config.sample_probabilities)

        # ---- Time correlation & preset data ----
        self.times = np.array(environment_config.time_correlation_intervals)
        self.data = np.array(environment_config.preset_data) # If new variables are added to EnvironmentConfig, they have to be added here as well to be used in the environment class. Add after this line


# ============================================================
# DATA GENERATION FROM TIME INTERVALS
# ============================================================
def GenerateDataFromTime(times, Tmax):
    rows, cols = times.shape
    data = []
    counter = 0

    for ii in np.arange(rows):
        currenttime = times[ii, :]
        data = np.append(
            data,
            np.append(
                np.zeros(currenttime[0] - counter),
                np.ones(currenttime[1] - currenttime[0]),
            ),
        )
        counter = currenttime[1]

    if data.size < Tmax:
        data = np.append(data, np.zeros(Tmax - data.size))

    return data