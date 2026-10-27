# Existing simulation tools

The Python entry points remain at the repository root. They model exploratory optical fields and propagation. They are not the circuit or device model of the proposed NPU and do not establish fabricated-chip performance.

## Setup

    python3 -m venv venv
    source venv/bin/activate
    python -m pip install -r requirements.txt

The simulation requirements include NumPy, Matplotlib, SciPy, Click and scikit-image. The separate generic-PDK layout experiments require packages such as gdsfactory and their test dependencies; they are outside this simulation environment specification.

## soliton.py

An exploratory split-step Fourier model of nonlinear propagation with diffraction, dispersion and Kerr terms. It includes collision and gate scenarios, material parameters and diagnostics.

Examples retained from the earlier README:

    python soliton.py run collision --power 7.3e4 --angle 0.2 --material algaas
    python soliton.py run gates --power 7.3e4 --separation 5e-6 --material algaas
    python soliton.py run debug-run --power 7.3e4 --disable-diffraction

Inspect the CLI before running large jobs:

    python soliton.py --help
    python soliton.py run --help

## hopfion.py

An exploratory vector-field propagation model with 3D visualization, including single structures and interactions.

    python hopfion.py run single --power 6.87e3 --grid-size 128 --material algaas
    python hopfion.py run interaction --velocity 5.0 --separation 10.0 --material algaas

The plotted structure and its propagation are not, by themselves, a verified topological invariant, stable physical memory, or computing operation.

## Other scripts

- run_experiments.py runs parameter sweeps using soliton.py. Its configuration and result-skip behavior remain unchanged.
- calculate_algaas_params.py contains material/parameter calculations.
- recreated_algaas_chip.py explores a model related to [the AlGaAs photon-pair paper](https://journals.aps.org/prxquantum/abstract/10.1103/PRXQuantum.6.010338).
- recreated_hopf_soliton.py refers to [Space-Time Hopfion Crystals](https://arxiv.org/abs/2406.06096).
- recreated_hopfion_crystal.py refers to [Construction of Hopfion Crystals](https://arxiv.org/abs/2504.03981).

The recreated_* filenames are retained for compatibility; the scripts have not been independently validated as reproductions of the cited papers. The local copies of those papers now reside in [references/papers](../references/papers/).

## Outputs

Most simulation output is in results/. Some older scripts write beside the entry point. Existing root-level PNG and GIF files were moved without changing their contents to results/legacy-root/. Future root images remain ignored by Git.

The cleanup did not alter simulation algorithms or launch a new parameter sweep.
