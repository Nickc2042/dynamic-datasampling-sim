# ============================================================
# IMPORTS
# ============================================================
import numpy as np
from . import simulation_config as default_config #Will now designate the default values from simulation_config.py, but we will pull them into a StrategyConfig object to keep things organized

from .config import StrategyConfig


# ============================================================
# LEGACY CONFIG HELPER
# ============================================================
def _legacy_strategy_config():
    """Build a StrategyConfig from the old global defaults <- simulation_config.py"""
    return StrategyConfig(
        # ---- Core state ----
        initial_strategy_state = default_config.initial_strategy_state,
        high_quality_enabled = default_config.high_quality_enabled,

        # ---- Sampling frequencies ----
        active_sampling_frequency = default_config.active_sampling_frequency,
        passive_sampling_frequency = default_config.passive_sampling_frequency,
        initial_sampling_frequency = default_config.initial_sampling_frequency,

        # ---- Memory ----
        memory_cap = default_config.memory_cap,
        responsive_memory_cap = default_config.responsive_memory_cap,
        initial_memory = default_config.initial_memory,

        # ---- Costs ----
        sampling_costs = default_config.sampling_costs,
        initial_current_cost = default_config.initial_current_cost,

        # ---- Periodic strategy parameters ----
        periodic_active_duration = default_config.periodic_active_duration,
        periodic_passive_duration = default_config.periodic_passive_duration,

        # ---- Responsive strategy parameters ----
        activation_probability = default_config.activation_probability,

        # ---- Bayesian strategy parameters ----
        bayesian_threshold = default_config.bayesian_threshold,
        bayesian_p_activate = default_config.bayesian_p_activate,
        bayesian_p_deactivate = default_config.bayesian_p_deactivate,
        bayesian_p_rel_given_active = default_config.bayesian_p_rel_given_active,
        bayesian_p_rel_given_passive = default_config.bayesian_p_rel_given_passive, # supports new variables for future expansion without needing to change this function. Add after this line

        # ---- TODO (Ready): not implemented ----
        # Pass ready_enabled / ready_sampling_frequency / ready_countdown / ready_cost here.

        # ---- CUSUM strategy parameters (researched, not implemented) ----
        # Placeholder — add cusum_* params here when the strategy is added.
    )


# ============================================================
# STRATEGY CLASS
# ============================================================
class strategy:
    def __init__(self, strattype = "Responsive", strategy_config=None):
        if strategy_config is None:
            strategy_config = _legacy_strategy_config()

        # ---- Core state ----
        self.strattype = strattype
        self.state = strategy_config.initial_strategy_state
        self.highquality = strategy_config.high_quality_enabled

        # ---- Sampling frequencies ----
        self.freqACT = strategy_config.active_sampling_frequency
        self.freqPAS = strategy_config.passive_sampling_frequency
        self.freq = strategy_config.initial_sampling_frequency

        # ---- Memory ----
        self.memorycap = strategy_config.memory_cap
        self.responsive_memorycap = strategy_config.responsive_memory_cap
        self.memory = strategy_config.initial_memory

        # ---- Costs ----
        self.costs = np.array(strategy_config.sampling_costs)
        self.currentcost = strategy_config.initial_current_cost

        # ---- Periodic strategy parameters ----
        self.periodic_active_duration = strategy_config.periodic_active_duration
        self.periodic_passive_duration = strategy_config.periodic_passive_duration

        # ---- Responsive strategy parameters ----
        self.activation_probability = strategy_config.activation_probability

        # ---- Bayesian strategy parameters ----
        self.bayesian_threshold = strategy_config.bayesian_threshold
        self.bayesian_p_activate = strategy_config.bayesian_p_activate
        self.bayesian_p_deactivate = strategy_config.bayesian_p_deactivate
        self.bayesian_p_rel_given_active = strategy_config.bayesian_p_rel_given_active
        self.bayesian_p_rel_given_passive = strategy_config.bayesian_p_rel_given_passive
        # Uninformative prior; washes out after a few observations, so it isn't configurable
        self.bayesian_belief = 0.5
        # If new variables are added to StrategyConfig, they have to be added here as well to be used in the strategy class. Add after this line

        # ---- TODO(Ready): not implemented ----
        # self.state = raw detection bool; self.mode = {Passive, Active, Ready}. When implemented:
        #   self.mode = "Passive"
        #   self.ready_enabled = strategy_config.ready_enabled
        #   self.freqREADY = strategy_config.ready_sampling_frequency
        #   self.ready_countdown = strategy_config.ready_countdown
        #   self.ready_memory = 0
        #   self.ready_cost = strategy_config.ready_cost

        # ---- CUSUM strategy parameters (researched, not implemented) ----
        # Placeholder — add cusum_h_up/h_down/likelihoods and the s_up/s_down
        # accumulators here when the CUSUM strategy is added.
