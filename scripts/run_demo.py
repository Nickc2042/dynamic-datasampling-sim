from pathlib import Path
import sys
import argparse
import csv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.dynamic_datasampling_sim.config_loader import load_config
from src.dynamic_datasampling_sim.simulation import run_simulation


def write_simulation_csv(path, times, states, samples, costs): # Writes the simulation results to a CSV file. Must update if new data is added to simulation output
    output_path = Path(path)
    output_path.parent.mkdir(parents = True, exist_ok = True)

    with output_path.open("w", newline = "", encoding = "utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["time", "environment_state", "sample", "cost"])
        writer.writerows(zip(times, states, samples, costs))

    return output_path


def build_simulation_summary(times, states, samples, costs):
    total_samples = samples.size
    relevant_samples = ((samples == 1) | (samples == 11)).sum()
    high_quality_relevant_samples = (samples == 11).sum()
    false_positive_high_quality_samples = (samples == 10).sum()
    irrelevant_low_quality_samples = (samples == 0).sum()
    active_environment_samples = (states == 1).sum()

    return {
        "total_samples": total_samples,
        "relevant_samples": relevant_samples,
        "high_quality_relevant_samples": high_quality_relevant_samples,
        "false_positive_high_quality_samples": false_positive_high_quality_samples,
        "irrelevant_low_quality_samples": irrelevant_low_quality_samples,
        "active_environment_samples": active_environment_samples,
        "total_cost": costs.sum(),
        "average_cost": costs.mean(),
        "start_time": times[0],
        "end_time": times[-1],
    }


def print_simulation_summary(times, states, samples, costs):
    summary = build_simulation_summary(times, states, samples, costs)
    total_samples = summary["total_samples"]

    def percent(value):
        return (value / total_samples) * 100

    print()
    print("Simulation Summary:")
    print(f"Total Samples: {summary['total_samples']}")
    print(f"Relevant Samples: {summary['relevant_samples']} ({percent(summary['relevant_samples']):.2f}%)")
    print(
        "High-Quality Relevant Samples: "
        f"{summary['high_quality_relevant_samples']} ({percent(summary['high_quality_relevant_samples']):.2f}%)"
    )
    print(
        "False-Positive High-Quality Samples: "
        f"{summary['false_positive_high_quality_samples']} ({percent(summary['false_positive_high_quality_samples']):.2f}%)"
    )
    print(
        "Irrelevant Low-Quality Samples: "
        f"{summary['irrelevant_low_quality_samples']} ({percent(summary['irrelevant_low_quality_samples']):.2f}%)"
    )
    print(
        "Active Environment Samples: "
        f"{summary['active_environment_samples']} ({percent(summary['active_environment_samples']):.2f}%)"
    )
    print(f"Total Cost: {summary['total_cost']:.2f}")
    print(f"Average Cost Per Sample: {summary['average_cost']:.2f}")
    print(f"Recorded Time Range: {summary['start_time']} to {summary['end_time']}")


def main():
    parser = argparse.ArgumentParser() # Parse and allows uerse to specify a config file when running the demo
    parser.add_argument(
        "--config",
        default = PROJECT_ROOT / "configs" / "modulation.yml",
        help = "Path to a YAML simulation config file.",
    )
    parser.add_argument(
        "--output",
        default = PROJECT_ROOT / "outputs" / "simulation_results.csv", # "outputs" folder within the project root, where resutls will be stored
        help = "Path where simulation results will be saved as CSV.",
    )
    parser.add_argument(
        "--summary",
        action = "store_true",
        help = "Print a terminal summary of sample quality, relevance, and cost.",
    )
    args = parser.parse_args()

    simulation_config = load_config(args.config)
    times, states, samples, costs = run_simulation(simulation_config = simulation_config)
    output_path = write_simulation_csv(args.output, times, states, samples, costs)

    print("Sample Times: ")
    print(times)
    print()

    print("Environment States: ")
    print(states)
    print()

    print("Samples Generated: ")
    print(samples)
    print()

    print("Cost Over Time: ")
    print(costs)

    if args.summary:
        print_simulation_summary(times, states, samples, costs)

    print()
    print(f"CSV Results Saved To: {output_path}") # terminal output to inform user where csv was saved


if __name__ == "__main__":
    main()
