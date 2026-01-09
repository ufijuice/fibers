# Photonic Simulations

This repository contains Python scripts for simulating nonlinear photonic phenomena, specifically focusing on spatial solitons and hopfions. These simulations are based on solving the Nonlinear Schrödinger Equation (NLSE) and the Vector NLSE using the split-step Fourier method.

## Core Concepts

- **Solitons**: Self-reinforcing wave packets that maintain their shape while propagating at a constant velocity. In this context, they are formed when the nonlinear Kerr effect (self-focusing) perfectly balances with linear effects like diffraction and dispersion. They are robust and can interact, making them candidates for information carriers in all-optical computing.
- **Hopfions**: Three-dimensional topological solitons, which are particle-like knots in a physical field. They are characterized by a topological invariant called the Hopf index. Their complex, stable, 3D structure suggests potential for high-density, multi-level information storage and processing, moving beyond binary systems.

## Scripts

### `soliton.py`

A (3+1)D simulation for spatial solitons in a Kerr medium. It models the propagation of pulsed light beams.

**Features:**
- Solves the (3+1)D Nonlinear Schrödinger Equation.
- Includes diffraction, group velocity dispersion (GVD), and the Kerr effect.
- Simulates single pulses, two-pulse collisions, and basic logic gates (e.g., an AND gate where two solitons collide).
- Provides physical realism checks (e.g., peak intensity, fluence, carrier density) to ground the simulation parameters.
- Generates animated GIFs of the simulations.
- Material library with properties for AlGaAs, Silicon, Silica, etc.

**Usage:**
The script uses `click` for its command-line interface.

- **Run a two-soliton collision:**
  ```bash
  python soliton.py run collision --power 7.3e4 --angle 0.2 --material algaas
  ```
- **Run a batch of logic gate simulations (1x1, 1x0, 0x0):**
  ```bash
  python soliton.py run gates --power 7.3e4 --separation 5e-6 --material algaas
  ```
- **Run a debug simulation of a single pulse:**
  ```bash
  python soliton.py run debug-run --power 7.3e4 --disable-diffraction
  ```

### `hopfion.py`

A (3+1)D simulation for optical hopfions.

**Features:**
- Solves the 3D Vector NLSE.
- Creates initial conditions for single hopfions and interacting pairs.
- Visualizes the 3D structure of the hopfion using `marching_cubes`, coloring the surface by polarization (S3 parameter).
- Simulates the interaction (collision) of two hopfions.

**Usage:**

- **Run a single, stationary hopfion simulation:**
  ```bash
  python hopfion.py run single --power 6.87e3 --grid-size 128 --material algaas
  ```
- **Run a two-hopfion interaction:**
  ```bash
  python hopfion.py run interaction --velocity 5.0 --separation 10.0 --material algaas
  ```

### Recreated original papers

- `recreated_algaas_chip.py`: https://journals.aps.org/prxquantum/abstract/10.1103/PRXQuantum.6.010338
- `recreated_hopf_soliton.py`: https://arxiv.org/html/2504.03981v1
- `recreated_hopfion_crystal.py`: https://arxiv.org/html/2406.06096v1

## Setup

1.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Project Goals

- **Short-Term**: Investigate soliton interactions (collisions, logic gates) as a potential mechanism for all-optical signal processing and bandwidth acceleration. The `soliton.py` script is the primary tool for this exploration.
- **Long-Term**: Explore the creation, stability, and interaction of 3D optical hopfions. Their topological nature could offer a robust foundation for novel, non-binary (analog) computing paradigms, where information is encoded in the hopfion's complex 3D state. The `hopfion.py` script serves this long-term vision.

## Results

Simulation outputs (NPZ data files, PNG images, and GIFs) are saved in the `results/` directory by default. Each run is typically timestamped to avoid overwriting.