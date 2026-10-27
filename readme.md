# Photonic computing research

Exploratory Python simulations of optical solitons, Hopfion-inspired fields and photonic structures.

## Research scope

The scripts explore nonlinear optical propagation, pulse interactions, polarization textures and resonator-array spectra. They use simplified physical and geometric models for numerical experiments and visualization.

## Repository contents

| File | Purpose |
|---|---|
| [soliton.py](soliton.py) | Nonlinear pulse propagation, collisions, logic-gate experiments and temporal profiles |
| [hopfion.py](hopfion.py) | Initial field construction and simplified vector propagation for single-field and interaction experiments |
| [run_experiments.py](run_experiments.py) | Multiprocessing driver for soliton parameter sweeps, configured within the script |
| [recreated_hopf_soliton.py](recreated_hopf_soliton.py) | Optical field and polarization visualization inspired by Hopf-soliton research |
| [recreated_hopfion_crystal.py](recreated_hopfion_crystal.py) | Rational-map model and visualization of Hopfion lattice textures |
| [recreated_algaas_chip.py](recreated_algaas_chip.py) | Simplified AlGaAs resonator-array spectra and joint spectral intensity |
| [calculate_algaas_params.py](calculate_algaas_params.py) | Estimates for AlGaAs soliton simulation parameters |

## Setup

Requires Python 3. Create a virtual environment and install the [dependencies](requirements.txt):

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows Command Prompt, activate the environment with `venv\Scripts\activate`.

## Run the simulations

View available commands and their options:

```bash
python soliton.py --help
python soliton.py run collision --help
python hopfion.py --help
python hopfion.py run single --help
```

For small example runs:

```bash
python soliton.py run collision --grid-size 32 --num-steps 20 --output-dir results/soliton-example
python hopfion.py run single --grid-size 32 --num-steps 20 --output-dir results/hopfion-example
```

Simulation data and generated figures are saved under `results/` by default. Use `--output-dir` to keep experiments separate. Resolution, material parameters and propagation settings need to be chosen for the experiment being studied.

For parameter sweeps, review `MODE`, `MATERIAL_CONFIGS` and `GRIDS` in [run_experiments.py](run_experiments.py) before launching a batch.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidance and the [contributor agreement](CLA.md).
