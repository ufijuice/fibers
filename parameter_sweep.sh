#!/bin/bash

# A script to run multiple simulations in parallel to sweep a parameter.

echo "Starting parameter sweep for 'power'..."

# 1. Define the parameters you want to sweep.
POWER_LEVELS=(6.0e3 6.5e3 6.87e3 7.0e3 7.5e3)

# 2. Set the maximum number of parallel jobs.
# (Adjust this based on your computer's CPU cores)
MAX_PARALLEL_JOBS=4

# 3. Create a unique directory for the results.
SWEEP_DIR="sweep_power_$(date +%Y%m%d-%H%M%S)"
mkdir -p "$SWEEP_DIR"

# 4. Loop through parameters and run simulations in parallel.
for power in "${POWER_LEVELS[@]}"; do
    echo "Queueing simulation for POWER = $power"
    
    # Ensure your virtual environment is active before running this script.
    # e.g., source venv/bin/activate
    #
    # Run the Python script in the background with the specified power.
    python hopfion.py run interaction --power "$power" --output-dir "$SWEEP_DIR" &

    # If we've hit the max number of parallel jobs, wait for one to finish.
    if [[ $(jobs -r -p | wc -l) -ge $MAX_PARALLEL_JOBS ]]; then
        wait -n
    fi
done

# Wait for any remaining background jobs to complete.
wait

echo "Parameter sweep completed. Results are in the '$SWEEP_DIR' directory."
