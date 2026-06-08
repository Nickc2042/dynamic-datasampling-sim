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

    print()
    print(f"CSV Results Saved To: {output_path}") # terminal output to inform user where csv was saved


if __name__ == "__main__":
    main()