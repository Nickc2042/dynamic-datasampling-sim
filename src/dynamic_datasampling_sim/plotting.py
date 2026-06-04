import numpy as np
import matplotlib.pyplot as plt


def clean_samples(samples):
    # Removes the high quality / low quality marker on the samples
    rawsamples = np.mod(samples, 10)

    # Removes the relevant/irrelevant marker on the samples
    rawquality = np.floor(samples / 10)

    # Counts the samples in each category:
    # [irrelevant/lowquality, relevant/lowquality, irrelevant/highquality, relevant/highquality]
    samplebreakdown = np.array([np.sum(samples == 0), np.sum(samples == 1), np.sum(samples == 10), np.sum(samples == 11)])

    return rawsamples, rawquality, samplebreakdown


def plot_samples_over_time(times, samples):
    rawsamples, rawquality, samplebreakdown = clean_samples(samples)

    fig, ax = plt.subplots()
    ax.fill_between(
        times,
        np.zeros(np.shape(times)),
        np.ones(np.shape(times)),
        alpha=0.2,
        linewidth=0,
        color="b",
        label="Irrelevant / Low Quality",
    )
    ax.fill_between(
        times,
        np.ones(np.shape(times)),
        2 * np.ones(np.shape(times)),
        alpha=0.2,
        linewidth=0,
        color="r",
        label="Relevant / High Quality",
    )
    ax.plot(times, rawsamples + 0.2, "-", linewidth=1.0, color="k", label="Sample Relevancy")
    ax.plot(times, rawquality + 0.4, "-", color="#808080", label="Measurement Quality")
    ax.legend(loc="upper right")
    ax.set_yticklabels([])
    ax.set_yticks([])
    ax.set(
        xlabel="Time (s)",
        title="Data Generated From a BLANK Environment \n and BLANK Sampling Strategy with PARAMETER = NUMBER",
    )

    return fig, ax


def plot_sample_breakdown(samples, times):
    rawsamples, rawquality, samplebreakdown = clean_samples(samples)

    fig, ax = plt.subplots()
    labels = [
        "Irrelevant\n Low Quality",
        "Relevant\n Low Quality",
        "Irrelevant\n High Quality",
        "Relevant\n High Quality",
    ]
    counts = [
        samplebreakdown[0] / times.size,
        samplebreakdown[1] / times.size,
        samplebreakdown[2] / times.size,
        samplebreakdown[3] / times.size,
    ]
    bar_labels = ["green", "purple", "orange", "red"]
    bar_colors = ["tab:green", "tab:purple", "tab:orange", "tab:red"]

    ax.bar(labels, counts, label=bar_labels, color=bar_colors)
    ax.set_ylabel("Proportion of Data")
    ax.set(ylim=(0, 1))
    ax.set(title="Distribution of High / Low Quality Measurements \n across Relevant / Irrelevant Data")

    return fig, ax