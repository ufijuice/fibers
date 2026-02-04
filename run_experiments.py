

import subprocess
import os
import itertools
import time
import numpy as np

# --- Parameters to Sweep ---
# Define the grid of parameters you want to test.
PARAMETER_GRID = {
    'power': [5.0e4, 7.3e4, 9.0e4],
    'angle': [0.1, 0.2, 0.3],
    'phase': [0, np.pi / 2, np.pi],
    'separation': [4e-6, 6e-6]
}

# --- Simulation Settings ---
BASE_COMMAND = [
    'python', 'soliton.py', 'run', 'collision',
    '--grid-size', '64',  # Use a smaller grid for faster runs
    '--num-steps', '100'   # Fewer steps for quicker experiments
]
RESULTS_DIR = 'results'
EXPERIMENT_NAME = f"experiment_batch_{time.strftime('%Y%m%d-%H%M%S')}"

def run_experiment(params):
    """Constructs and runs a single simulation command."""
    command = BASE_COMMAND.copy()
    
    # Add parameters to the command
    for key, value in params.items():
        command.append(f"--{key}")
        command.append(str(value))
        
    # Add the specific output directory for this run
    command.append('--output-dir')
    command.append(os.path.join(RESULTS_DIR, EXPERIMENT_NAME))

    print("---" * 10)
    print(f"Running with params: {params}")
    # Use a more readable command string for printing
    print(f"Executing: {' '.join(command)}")
    
    try:
        # Execute the command
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print("STDOUT:", result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        print("✅ Experiment completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Experiment failed for params: {params}")
        print("Error:", e)
        print("Stderr:", e.stderr)
    print("---" * 10 + "\n")


def main():
    """
    Generates all parameter combinations and runs the experiments.
    """
    # Create the main directory for this batch of experiments
    batch_output_dir = os.path.join(RESULTS_DIR, EXPERIMENT_NAME)
    os.makedirs(batch_output_dir, exist_ok=True)
    print(f"Created experiment batch directory: {batch_output_dir}")

    # Get all combinations of parameters
    keys, values = zip(*PARAMETER_GRID.items())
    param_combinations = [dict(zip(keys, v)) for v in itertools.product(*values)]
    
    total_experiments = len(param_combinations)
    print(f"Starting batch of {total_experiments} experiments...")

    for i, params in enumerate(param_combinations):
        print(f"\n--- Running Experiment {i+1} of {total_experiments} ---")
        run_experiment(params)
        
    print("🎉 All experiments completed! 🎉")
    print(f"Results are saved in: {batch_output_dir}")


if __name__ == "__main__":
    main()

