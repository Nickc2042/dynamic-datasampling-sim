import numpy as np

from . import simulation_config as config


class strategy:
    def __init__(self, strattype="Responsive"):
        self.strattype = strattype
        self.state = config.initial_strategy_state # Anything "config." variable is set in simulation_config.py, so can be easily edited without changing the core code
        self.highquality = config.high_quality_enabled
        self.freqACT = config.active_sampling_frequency
        self.freqPAS = config.passive_sampling_frequency
        self.freq = config.initial_sampling_frequency
        self.memorycap = config.memory_cap
        self.memory = config.initial_memory
        self.costs = np.array(config.sampling_costs)
        self.currentcost = config.initial_current_cost