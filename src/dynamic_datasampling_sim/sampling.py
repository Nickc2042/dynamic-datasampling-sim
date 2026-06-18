# ============================================================
# IMPORTS
# ============================================================
import numpy as np


# ============================================================
# SAMPLE GENERATION
# ============================================================
def get_sample(strat, environ, rng):
    # ---- Base sample ----
    if ((environ.environtype == "Markovian") | (environ.environtype == "OneState") | (environ.environtype == "TimeCorrelations")):
        if environ.state:
            sample = rng.random() < environ.sampleprobs[0]
        else:
            sample = rng.random() > environ.sampleprobs[1]
    elif environ.environtype == "Preset":
        sample = environ.state

    # ---- High quality modifier ----
    # TODO(Ready) Ready reuses Active quality in v1. When Ready gets its own tier,
    # rework the +10 encoding so the ==1/11 relevant-sample test still holds.
    if strat.highquality and strat.state:
        return sample + (10 * strat.state)
    else:
        return sample


# ============================================================
# ENVIRONMENT UPDATE
# ============================================================
def update_environ(environ, strat, t, rng):
    # ---- Markovian Update ----
    if environ.environtype == "Markovian":
        # If we reach a new full time step, try to advance the markov chain
        if np.floor(t + (1 / strat.freq)) > np.floor(t):
            if environ.state:
                # transition from true to false with probability given by transprobs
                environ.state = rng.random() > environ.transprobs[0]
            else:
                # transition from false to true with probability given by transprobs
                environ.state = rng.random() < environ.transprobs[1]

    # ---- Time Correlations Update ----
    elif environ.environtype == "TimeCorrelations":
        # if the current time is within one of the intervals, then set the state to active
        environ.state = np.any((environ.times[:, 0] < t + (1 / strat.freq)) & (environ.times[:, 1] > t + (1 / strat.freq)))

    # ---- Preset Update ----
    elif environ.environtype == "Preset":
        # set the environment state according to the previous integer time unit
        current_time_index = np.floor(t + (1 / strat.freq))
        environ.state = environ.data[current_time_index.astype(int)]

    return environ


# ============================================================
# STRATEGY UPDATE
# ============================================================
def update_strat(sample, strat, rng):
    # State Updates
    # ---- Responsive ----
    if strat.strattype == "Responsive":
        # irrelevant sample
        if (sample == 0) | (sample == 10):
            if strat.state:
                strat.memory = strat.memory + 1
                if strat.memory >= strat.responsive_memorycap:
                    strat.memory = 0
                    strat.state = False
        # relevant sample
        else:
            strat.memory = 0
            strat.state = True

    # ---- WaitingTime ----
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

    # ---- Periodic ----
    # Periodic: open-loop baseline — alternate active/passive on a fixed schedule, ignore samples
    elif strat.strattype == "Periodic":
        strat.memory = strat.memory + 1
        if strat.state:
            if strat.memory >= strat.periodic_active_duration:
                strat.memory = 0
                strat.state = False
        else:
            if strat.memory >= strat.periodic_passive_duration:
                strat.memory = 0
                strat.state = True

    # ---- Random ----
    # Random: no-information baseline — fresh Bernoulli draw each decision step, ignore samples
    elif strat.strattype == "Random":
        strat.state = bool(rng.random() < strat.activation_probability)

    # ---- CUSUM (researched, not implemented) ----
    # Placeholder for a future Page's cumulative-sum change-point detector strategy.
    # Researched but deliberately not implemented yet — see the CUSUM writeup in
    # outputs/current_strategies.md for the design and why it was parked. To add it,
    # elif strat.strattype == "CUSUM":
    #     ...

    # ---- Bayesian ----
    # Forward filtering for a 2-state HMM (recursive Bayes filter): track the
    # posterior belief b = P(env active | observations so far), activate when
    # b > threshold. Two steps per sample:
    #   predict:  b' = b*(1 - p_deactivate) + (1 - b)*p_activate     (transition prior)
    #   update:   b  = Lact*b' / (Lact*b' + Lpas*(1 - b'))           (Bayes' rule)
    # where L* = P(this observation | env active/passive).
    # See Rabiner (1989), HMM tutorial; Russell & Norvig (AIMA), temporal filtering.
    elif strat.strattype == "Bayesian":
        relevant = (sample == 1) | (sample == 11)
        prior = strat.bayesian_belief * (1 - strat.bayesian_p_deactivate) \
            + (1 - strat.bayesian_belief) * strat.bayesian_p_activate
        lik_active = strat.bayesian_p_rel_given_active if relevant else 1 - strat.bayesian_p_rel_given_active
        lik_passive = strat.bayesian_p_rel_given_passive if relevant else 1 - strat.bayesian_p_rel_given_passive
        posterior = lik_active * prior
        strat.bayesian_belief = posterior / max(posterior + lik_passive * (1 - prior), 1e-12)
        strat.state = strat.bayesian_belief > strat.bayesian_threshold

    # ---- TOD(Ready): tri-state wrapper (not implemented) ----
    # strat.state = raw detection bool; strat.mode = {Passive, Active, Ready}:
    #   detection = strat.state
    #   if strat.mode == "Active" and not detection:
    #       strat.mode = "Ready"; strat.ready_memory = 0
    #   elif strat.mode == "Ready":
    #       if (sample == 1) | (sample == 11):
    #           strat.mode = "Active"; strat.state = True      # resurgence -> back to Active
    #       else:
    #           strat.ready_memory += 1
    #           if strat.ready_memory >= strat.ready_countdown:
    #               strat.mode = "Passive"; strat.state = False
    #   elif detection:
    #       strat.mode = "Active"                              # Passive -> Active (never via Ready)
    #   else:
    #       strat.mode = "Passive"

    # ---- Sampling frequency & cost update ----
    # TODO(Ready): prepend a Ready tier before Active/Passive:
    #   if strat.mode == "Ready": strat.freq = strat.freqREADY; strat.currentcost = strat.ready_cost
    if strat.state:
        strat.freq = strat.freqACT
        strat.currentcost = strat.costs[1]
    else:
        strat.freq = strat.freqPAS
        strat.currentcost = strat.costs[0]

    return strat