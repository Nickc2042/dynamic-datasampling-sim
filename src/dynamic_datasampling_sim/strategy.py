import numpy as np
from . import simulation_config as default_config #Will now designate the default values from simulation_config.py, but we will pull them into a StrategyConfig object to keep things organized
 
from .config import StrategyConfig


def _legacy_strategy_config():
    """Build a StrategyConfig from the old global defaults <- simulation_config.py"""
    return StrategyConfig(
        initial_strategy_state = default_config.initial_strategy_state,
        high_quality_enabled = default_config.high_quality_enabled,

        active_sampling_frequency = default_config.active_sampling_frequency,
        passive_sampling_frequency = default_config.passive_sampling_frequency,
        initial_sampling_frequency = default_config.initial_sampling_frequency,

        memory_cap = default_config.memory_cap,
        initial_memory = default_config.initial_memory,

        sampling_costs = default_config.sampling_costs,
        initial_current_cost = default_config.initial_current_cost, # supports new variables for future expansion without needing to change this function. Add after this line
    )


class strategy:
    def __init__(self, strattype = "Responsive", strategy_config=None):
        if strategy_config is None:
            strategy_config = _legacy_strategy_config()

        self.strattype = strattype
        self.state = strategy_config.initial_strategy_state
        self.highquality = strategy_config.high_quality_enabled

        self.freqACT = strategy_config.active_sampling_frequency
        self.freqPAS = strategy_config.passive_sampling_frequency
        self.freq = strategy_config.initial_sampling_frequency

        self.memorycap = strategy_config.memory_cap
        self.memory = strategy_config.initial_memory

        self.costs = np.array(strategy_config.sampling_costs)
        self.currentcost = strategy_config.initial_current_cost # If new variables are added to StrategyConfig, they have to be added here as well to be used in the strategy class. Add after this line
