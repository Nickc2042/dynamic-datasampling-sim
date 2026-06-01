import numpy as np


rng = np.random.default_rng()


def get_sample(strat, environ):
    # Base sample
    if ((environ.environtype == "Markovian") | (environ.environtype == "OneState") | (environ.environtype == "TimeCorrelations")):
        if environ.state:
            sample = rng.random() < environ.sampleprobs[0]
        else:
            sample = rng.random() > environ.sampleprobs[1]
    elif environ.environtype == "Preset":
        sample = environ.state

    # Add high quality modifier if needed
    if strat.highquality and strat.state:
        return sample + (10 * strat.state)
    else:
        return sample


def update_environ(environ, strat, t):
    # Markovian Update
    if environ.environtype == "Markovian":
        # If we reach a new full time step, try to advance the markov chain
        if np.floor(t + (1 / strat.freq)) > np.floor(t):
            if environ.state:
                # transition from true to false with probability given by transprobs
                environ.state = rng.random() > environ.transprobs[0]
            else:
                # transition from false to true with probability given by transprobs
                environ.state = rng.random() < environ.transprobs[1]

    # Time Correlations Update
    elif environ.environtype == "TimeCorrelations":
        # if the current time is within one of the intervals, then set the state to active
        environ.state = np.any((environ.times[:, 0] < t + (1 / strat.freq)) & (environ.times[:, 1] > t + (1 / strat.freq)))

    # Preset Update
    elif environ.environtype == "Preset":
        # set the environment state according to the previous integer time unit
        current_time_index = np.floor(t + (1 / strat.freq))
        environ.state = environ.data[current_time_index.astype(int)]

    return environ


def update_strat(sample, strat):
    # State Updates
    # Responsive
    if strat.strattype == "Responsive":
        # irrelevant sample
        if (sample == 0) | (sample == 10):
            if strat.state:
                strat.memory = strat.memory + 1
                if strat.memory >= strat.memorycap:
                    strat.memory = 0
                    strat.state = False
        # relevant sample
        else:
            strat.memory = 0
            strat.state = True

    # Waitingtime
    elif strat.strattype == "WaitingTime":
        if not strat.state:
            if (sample == 1) | (sample == 11):
                strat.state = True
        else:
            strat.memory = strat.memory + 1
            if strat.memory >= strat.memorycap:
                strat.memory = 0
                if not ((sample == 11) | (sample == 1)):
                    strat.state = False

    # Update the sampling freq & current cost
    if strat.state:
        strat.freq = strat.freqACT
        strat.currentcost = strat.costs[1]
    else:
        strat.freq = strat.freqPAS
        strat.currentcost = strat.costs[0]

    return strat
