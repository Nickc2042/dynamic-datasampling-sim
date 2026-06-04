import numpy as np

from . import simulation_config as config
from .environment import environment
from .sampling import get_sample, update_environ, update_strat
from .strategy import strategy


def run_simulation(strattype=None, environtype=None, T=None):
    if strattype is None:
        strattype = config.default_strategy_type # View simulation_config.py for details on any "config." variables
    if environtype is None:
        environtype = config.default_environment_type # defaults.py may be added in future updates for cleaner code
    if T is None:
        T = config.default_simulation_time

    config.validate_config(simulation_time=T)

    # Strategy & environment initialization based on earlier choices
    strat = strategy(strattype=strattype)
    environ = environment(environtype=environtype)

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