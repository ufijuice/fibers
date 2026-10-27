# Photonic computing research

This workspace contains exploratory photonic simulations and the current proposal for a **modular photonic NPU**: programmable optical computation supported by electronic memory and control.

## Current presentation

Start with [the presentation index](misc/presentation/README.md).

- [Pitch deck](misc/presentation/photonic_npu_preseed.pdf)
- [One-page overview](misc/presentation/photonic_npu_one_pager.pdf)
- [Technical and funding assumptions](misc/presentation/photonic_npu_diligence.md)
- [Editable feasibility budget](misc/presentation/preseed_budget.py)

The proposed first device is an 8×8 matrix–vector compute tile using a soliton microcomb as its source. Numerical precision, complete-system power, a useful workload and a competitive advantage remain to be established. The existing simulation and generic-PDK layout examples are research preparation; they are not a measured NPU or a foundry-qualified implementation.

The working ask is $750k for a 15-month feasibility program. Earlier light-source and retina pitches and their sales models are [archived](misc/presentation/archive/README.md); their forecasts do not apply to the NPU.

## Repository map

| Location | Purpose |
|---|---|
| misc/presentation/ | Current deck, one-pager, diligence, budget, build script and outreach draft |
| misc/presentation/archive/ | Earlier pitches and analyses, preserved locally with a movement manifest |
| misc/ | Earlier generic-PDK microcomb/retina layout experiments |
| references/ | Paper index and local PDF copies |
| docs/simulations.md | Existing simulation scripts, setup and usage |
| results/ | Generated output; older root figures are in results/legacy-root/ |

Core simulation entry points retain their paths: soliton.py, hopfion.py, run_experiments.py and the recreated_* scripts. The NPU program does not depend on proving the longer-term Hopfion-computing idea.

## Build the presentation

Requires Python 3 and a working pdflatex installation:

    python3 misc/presentation/build.py

The build regenerates the numerical budget, compiles the two PDFs and keeps LaTeX intermediates in misc/presentation/build/. It does not install packages.

## Run the simulations

Create or activate an environment and install the [simulation requirements](requirements.txt):

    python3 -m venv venv
    source venv/bin/activate
    python -m pip install -r requirements.txt
    python soliton.py --help
    python hopfion.py --help

See [simulation notes](docs/simulations.md) for examples and limitations. Layout experiments need additional dependencies described in [misc/README.md](misc/README.md).

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidance.
