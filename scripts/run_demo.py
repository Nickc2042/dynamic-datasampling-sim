from pathlib import Path
import sys
import argparse


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.dynamic_datasampling_sim.config_loader import load_config
from src.dynamic_datasampling_sim.simulation import run_simulation


def main():
    parser = argparse.ArgumentParser() # Parse and allows uerse to specify a config file when running the demo
    parser.add_argument(
        "--config",
        default = PROJECT_ROOT / "configs" / "modulation.yml",
        help = "Path to a YAML simulation config file.",
    )
    args = parser.parse_args()

    simulation_config = load_config(args.config)
    times, states, samples, costs = run_simulation(simulation_config = simulation_config)

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


if __name__ == "__main__":
    main()