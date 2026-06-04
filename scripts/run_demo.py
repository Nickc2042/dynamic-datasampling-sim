from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.dynamic_datasampling_sim.simulation import run_simulation


def main():
    times, states, samples, costs = run_simulation()

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