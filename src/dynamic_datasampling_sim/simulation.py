import numpy as np

from . import simulation_config as config
from .config import SUPPORTED_ENVIRONMENT_TYPES, SUPPORTED_STRATEGY_TYPES
from .environment import environment
from .sampling import get_sample, update_environ, update_strat
from .strategy import strategy


def run_simulation(strattype = None, environtype = None, T = None, simulation_config = None):
    # From simulation_config or the so called "default/legacy"
    if simulation_config is not None:
        if strattype is None:
            strattype = simulation_config.default_strategy_type
        if environtype is None:
            environtype = simulation_config.default_environment_type
        if T is None:
            T = simulation_config.default_simulation_time

        simulation_config.validate(
            simulation_time = T,
            strategy_type = strattype,
            environment_type = environtype,
        )
        strategy_config = simulation_config.strategy
        environment_config = simulation_config.environment
    
    # From defaults if not provided in simulation_config
    else:
        if strattype is None:
            strattype = config.default_strategy_type # View simulation_config.py for details on any "config" variables
        if environtype is None:
            environtype = config.default_environment_type # defaults.py may be added in future updates for cleaner code
        if T is None:
            T = config.default_simulation_time

        config.validate_config(simulation_time = T)
        if strattype not in SUPPORTED_STRATEGY_TYPES:
            raise ValueError(f"strategy_type must be one of {sorted(SUPPORTED_STRATEGY_TYPES)}.")
        if environtype not in SUPPORTED_ENVIRONMENT_TYPES:
            raise ValueError(f"environment_type must be one of {sorted(SUPPORTED_ENVIRONMENT_TYPES)}.")
        strategy_config = None
        environment_config = None

    # Strategy & environment initialization based on earlier choices
    strat = strategy(strattype = strattype, strategy_config = strategy_config)
    environ = environment(environtype =environtype, environment_config = environment_config)

    # initialization for time index
    t = 0

    # initialization for the outputs:
    # times = the times at which we sample
    # states = the states at those times
    # samples = the samples we get
    # costs = the cost at each time
    times = np.array([])
    states = np.array([])
    samples = np.array([])
    costs = np.array([])

    while t < T:
        newsample = get_sample(strat=strat, environ=environ)

        costs = np.append(costs, strat.currentcost)
        samples = np.append(samples, newsample)
        times = np.append(times, t)
        states = np.append(states, environ.state)

        strat = update_strat(sample=newsample, strat=strat)
        environ = update_environ(environ=environ, strat=strat, t=t)

        t = t + (1 / strat.freq)

    return times, states, samples, costs