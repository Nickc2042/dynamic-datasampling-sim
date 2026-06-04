import numpy as np

from . import simulation_config as config


class environment:
    def __init__(self, environtype="Markovian"):
        self.environtype = environtype
        self.state = config.initial_environment_state
        self.transprobs = np.array(config.transition_probabilities)
        self.sampleprobs = np.array(config.sample_probabilities)
        self.times = np.array(config.time_correlation_intervals)
        self.data = np.array(config.preset_data)


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