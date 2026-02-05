import subprocess
import os
import itertools
import time
import multiprocessing
import sys
import numpy as np
from soliton import MATERIALS

# --- CONFIGURATION ---
# Options: 'collision', 'gates', 'temporal'
MODE = 'collision' 

# --- Material configurations ---
MATERIAL_CONFIGS = {
    name: {'wavelength': props['typical_wavelength'], 'dispersion': props['typical_dispersion']}
    for name, props in MATERIALS.items()
}

# --- Parameter Grids ---
GRIDS = {
    'collision': {
        'soliton_order_N': [0.9, 1.0, 1.1, 1.3, 1.5, 2.0],
        'angle': [0.05, 0.1, 0.2, 0.3],
        'phase': [0, np.pi/4, np.pi/2, np.pi],
        'separation': [5e-6, 10e-6],
        'beam-waist': [1e-6, 1.5e-6],
    },
    'gates': {
        'soliton_order_N': [1.0, 1.2, 1.5],
        'angle': [0.1, 0.2],
        'phase': [0, np.pi],
        'separation': [5e-6],
        'beam-waist': [1e-6],
    },
    'temporal': {
        'soliton_order_N': [0.5, 1.0, 2.0, 3.0],
        'dispersion': [-50.0, -20.0, -10.0, 0, 10.0, 20.0],
        'pulse-duration': [30e-15, 50e-15, 100e-15],
    }
}

RESULTS_DIR = 'results'
MODE_DIR = {
    'collision': 'sweep_collisions',
    'gates': 'sweep_gates',
    'temporal': 'sweep_temporal'
}

def calculate_pcrit(material, wavelength):
    """Calculates the critical power for a fundamental spatial soliton."""
    props = MATERIALS[material]
    n0 = props['n0']
    n2 = props['n2']
    return wavelength**2 / (n0 * n2)

def run_experiment(params):
    """Constructs and runs a single simulation command."""
    mode = params.pop('__mode__')
    command = [sys.executable, 'soliton.py', 'run', mode]
    
    # Common settings
    command.extend(['--grid-size', '64', '--num-steps', '150'])
    
    # Power calculation
    n_order = params.pop('soliton_order_N')
    p_crit = calculate_pcrit(params['material'], params['wavelength'])
    actual_power = (n_order**2) * p_crit
    command.extend(['--power', str(actual_power)])
    
    # Add other parameters
    for key, value in params.items():
        if key in ['material', 'wavelength']: # Already handled or pass through
            command.extend([f"--{key}", str(value)])
        elif key in GRIDS[mode]:
            command.extend([f"--{key}", str(value)])

    output_path = os.path.join(RESULTS_DIR, MODE_DIR[mode])
    command.extend(['--output-dir', output_path])

    # Existence check logic
    grid_size = "64"
    num_steps = "150"
    
    if mode == 'collision':
        filename = f"soliton_collision_{params['material']}_P{actual_power:.2e}_GS{grid_size}_N{num_steps}_A{params['angle']:.3f}.npz"
    elif mode == 'gates':
        # Gates command runs 1x1, 1x0, 0x0. We check for the 1x1 as a proxy.
        filename = f"soliton_gate_1x1_{params['material']}_P{actual_power:.2e}_GS{grid_size}_N{num_steps}_S{params['separation']}_A{params['angle']:.3f}.npz"
    else: # temporal
        filename = f"temporal_profile_{params['material']}_P{actual_power:.2e}_D{params['dispersion']:.1f}.npz"

    file_full_path = os.path.join(output_path, filename)
    info = f"{params['material']} | N: {n_order:.1f}"
    if 'angle' in params: info += f" | A: {params['angle']:.2f}"
    
    if os.path.exists(file_full_path):
        return True, info, "Skipped"
    
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        return True, info, ""
    except subprocess.CalledProcessError as e:
        return False, info, e.stderr[:100]

def main():
    print(f"--- Soliton Experiment Runner: {MODE.upper()} MODE ---")
    batch_output_dir = os.path.join(RESULTS_DIR, MODE_DIR[MODE])
    os.makedirs(batch_output_dir, exist_ok=True)

    all_experiments = []
    materials_to_test = list(MATERIAL_CONFIGS.keys())
    
    grid = GRIDS[MODE]
    keys, values = zip(*grid.items())
    
    for material in materials_to_test:
        config = MATERIAL_CONFIGS[material]
        for v in itertools.product(*values):
            params = dict(zip(keys, v))
            params['material'] = material
            params.update(config)
            params['__mode__'] = MODE
            all_experiments.append(params)
    
    total = len(all_experiments)
    num_cpus = multiprocessing.cpu_count()
    print(f"Tasks: {total} | CPUs: {num_cpus} | Dir: {batch_output_dir}\n")

    with multiprocessing.Pool(processes=num_cpus) as pool:
        completed = 0
        for success, info, status in pool.imap_unordered(run_experiment, all_experiments):
            completed += 1
            percent = (completed / total) * 100
            mark = "✅" if success else "❌"
            if status == "Skipped": mark = "⏭️"
            print(f"[{percent:6.2f}%] {completed}/{total} | {info} | {mark} {status}")
        
    print(f"\n🎉 Mode {MODE} completed!")

if __name__ == "__main__":
    main()
