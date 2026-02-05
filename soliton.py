import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import click
import os
import time

# --- Material Library (with Two-Photon Absorption coefficients) ---
MATERIALS = {
    # beta_tpa is in m/W, typical_wavelength in meters, typical_dispersion in ps^2/km
    'algaas': {'n0': 3.3, 'n2': 1e-17, 'beta_tpa': 1.5e-11, 'typical_wavelength': 1.55e-6, 'typical_dispersion': -20.0},
    'silica': {'n0': 1.44, 'n2': 2.6e-20, 'beta_tpa': 0, 'typical_wavelength': 1.55e-6, 'typical_dispersion': -28.0},
    'bk7': {'n0': 1.50, 'n2': 3.45e-20, 'beta_tpa': 0, 'typical_wavelength': 1.06e-6, 'typical_dispersion': -10.0},
    'sapphire': {'n0': 1.75, 'n2': 3.0e-20, 'beta_tpa': 0, 'typical_wavelength': 0.8e-6, 'typical_dispersion': -5.0},
    'zns': {'n0': 2.27, 'n2': 7.9e-18, 'beta_tpa': 5e-11, 'typical_wavelength': 2.0e-6, 'typical_dispersion': -100.0},
    'silicon': {'n0': 3.48, 'n2': 6e-18, 'beta_tpa': 5e-12, 'typical_wavelength': 1.55e-6, 'typical_dispersion': -50.0},
    'silicon_nitride': {'n0': 2.0, 'n2': 2.4e-19, 'beta_tpa': 0, 'typical_wavelength': 1.55e-6, 'typical_dispersion': -30.0},
    'inp': {'n0': 3.17, 'n2': 1.5e-17, 'beta_tpa': 1e-12, 'typical_wavelength': 1.55e-6, 'typical_dispersion': -40.0},
    'gaas': {'n0': 3.38, 'n2': 1.5e-17, 'beta_tpa': 1.5e-11, 'typical_wavelength': 1.55e-6, 'typical_dispersion': -35.0},
    'linbo3': {'n0': 2.14, 'n2': 1.0e-19, 'beta_tpa': 0, 'typical_wavelength': 1.55e-6, 'typical_dispersion': -20.0},
    'diamond': {'n0': 2.39, 'n2': 1.3e-19, 'beta_tpa': 0, 'typical_wavelength': 0.532e-6, 'typical_dispersion': -5.0},
}

# --- Core Simulation & Visualization Logic ---

def calculate_optimal_dz(sim_params, target_phase_shift=0.05):
    """
    Calculate optimal dz step size based on nonlinear phase shift criterion.

    For numerical stability, want: k0 * n2 * I_peak * dz < target_phase_shift

    Args:
        sim_params: Dictionary containing simulation parameters
        target_phase_shift: Target nonlinear phase shift per step (radians)

    Returns:
        Optimal dz value
    """
    power = sim_params['power']
    effective_area = sim_params.get('effective_area', 1e-12)
    n2 = sim_params['n2']
    k0 = sim_params.get('k0')
    if k0 is None:
        wavelength = sim_params.get('wavelength', 1.55e-6)
        k0 = 2 * np.pi / wavelength

    # For a Gaussian beam, the relationship between power (P) and peak intensity (I_0)
    # is P = I_0 * (pi * w_0^2 / 2). The effective area is A_eff = pi * w_0^2.
    # Therefore, I_0 = 2 * P / A_eff.
    peak_intensity = 2 * power / effective_area

    # Calculate dz for target phase shift
    # φ_NL = k0 * n2 * I * dz
    dz_optimal = target_phase_shift / (k0 * n2 * peak_intensity)

    # Sanity check: dz shouldn't be too small (< 1e-6) or too large (> 0.1)
    dz_optimal = max(1e-6, min(dz_optimal, 0.1))

    return dz_optimal

def report_simulation_regime(sim_params):
    """
    Print diagnostic information about the simulation regime.
    """
    material = sim_params.get('material', 'unknown')
    power = sim_params['power']
    wavelength = sim_params.get('wavelength', 1.55e-6)
    n0 = sim_params['n0']
    n2 = sim_params['n2']

    # Calculate critical power for fundamental soliton
    P_crit = wavelength**2 / (n0 * n2)
    N_soliton = np.sqrt(power / P_crit)

    click.echo(f"\n--- Soliton Regime Analysis ---")
    click.echo(f"Material: {material}")
    click.echo(f"Peak Power: {power:.2e} W")
    click.echo(f"Critical Power: {P_crit:.2e} W")
    click.echo(f"Soliton Number N = {N_soliton:.3f}")

    if N_soliton < 0.5:
        click.secho("  → Power too weak: beam will diffract", fg='yellow')
    elif N_soliton < 0.9:
        click.secho("  → Below fundamental soliton regime", fg='yellow')
    elif N_soliton <= 1.2:
        click.secho("  → Fundamental soliton regime ✓", fg='green')
    elif N_soliton <= 2.0:
        click.secho("  → Higher-order soliton (will oscillate/breathe)", fg='cyan')
    else:
        click.secho("  → High-order soliton (complex dynamics)", fg='cyan')

    click.echo(f"-------------------------------\n")

def run_nlse_simulation(initial_field, sim_params):
    """
    Solves the (3+1)D NLSE for pulsed beams.
    Includes diffraction, dispersion, and Kerr nonlinearity.
    Transverse motion is handled by phase tilts in the initial field.
    """

    # --- Grid parameters ---
    ny, nx, nt = initial_field.shape
    dx, dy, dt = sim_params["dx"], sim_params["dy"], sim_params["dt"]
    dz = sim_params["dz"]
    num_steps = sim_params["num_steps"]

    # --- Physical parameters ---
    k0 = sim_params["k0"]
    k = sim_params["k"]
    n2 = sim_params["n2"]

    beta2 = sim_params.get("dispersion", 0.0) * 1e-27  # ps^2/km → s^2/m

    disable_diffraction = sim_params.get("disable_diffraction", False)
    disable_dispersion = sim_params.get("disable_dispersion", False)

    store_interval = sim_params.get("store_interval", 5)

    # --- Frequency grids ---
    kx = 2 * np.pi * np.fft.fftfreq(nx, d=dx)
    ky = 2 * np.pi * np.fft.fftfreq(ny, d=dy)
    omega = 2 * np.pi * np.fft.fftfreq(nt, d=dt)

    KY, KX, OMEGA = np.meshgrid(ky, kx, omega, indexing="ij")

    # --- Linear operators ---
    spatial_op = 0.0 if disable_diffraction else -(KX**2 + KY**2) / (2 * k)

    temporal_op = 0.0 if disable_dispersion else (beta2 / 2) * OMEGA**2

    linear_phase = np.exp(0.5j * (spatial_op + temporal_op) * dz)

    # --- Initialize ---
    field = initial_field.astype(np.complex128)
    field_history = [field.copy()]

    initial_energy = np.sum(np.abs(field)**2) * dx * dy * dt

    click.echo("Running NLSE simulation...")

    for step in range(num_steps):

        # --- Linear half-step ---
        field_f = np.fft.fftn(field)
        field_f *= linear_phase
        field = np.fft.ifftn(field_f)

        # --- Kerr nonlinearity ---
        field *= np.exp(1j * k0 * n2 * np.abs(field)**2 * dz)

        # --- Linear half-step ---
        field_f = np.fft.fftn(field)
        field_f *= linear_phase
        field = np.fft.ifftn(field_f)

        # --- Stability check ---
        if (step + 1) % 20 == 0:
            if not np.all(np.isfinite(field)):
                click.secho("Simulation unstable (NaN/Inf). Reduce dz or power.", fg="red")
                return field_history, initial_energy

        # --- Store history ---
        if (step + 1) % store_interval == 0:
            field_history.append(field.copy())
            energy = np.sum(np.abs(field)**2) * dx * dy * dt
            click.echo(
                f"Step {step+1}/{num_steps} | Energy ratio: {energy/initial_energy:.4f}"
            )

    final_energy = np.sum(np.abs(field)**2) * dx * dy * dt

    click.echo(f"\nInitial energy: {initial_energy:.4e}")
    click.echo(f"Final energy:   {final_energy:.4e}")
    click.echo(f"Energy conserved: {100*final_energy/initial_energy:.2f}%\n")

    return field_history, initial_energy

def animate_simulation(field_history, sim_params, output_filename):
    """
    Creates and saves an animated GIF of the soliton simulation.
    """
    click.echo(f"Generating animation... this may take a moment.")
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    
    sim_size_x = sim_params.get('sim_size_x', 5.0)
    sim_size_y = sim_params.get('sim_size_y', 5.0)
    grid_size = sim_params['grid_size']
    store_interval = sim_params.get('store_interval', 5)

    x_vis = np.linspace(-sim_size_x, sim_size_x, grid_size)
    y_vis = np.linspace(-sim_size_y, sim_size_y, grid_size)
    X_vis, Y_vis = np.meshgrid(x_vis, y_vis)

    max_intensity = max(np.max(frame) for frame in field_history) if field_history else 0
    
    z_upper_lim = max_intensity * 1.1
    if z_upper_lim < 1e-9:
        z_upper_lim = 1.0

    def update_plot(frame_index, field_history, ax):
        ax.clear()
        Z_vis = field_history[frame_index]
        ax.plot_surface(X_vis, Y_vis, Z_vis, cmap='viridis', vmin=0, vmax=max_intensity if max_intensity > 0 else 1)
        ax.set_xlabel('X'); ax.set_ylabel('Y'); ax.set_zlabel('Intensity')
        ax.set_zlim(0, z_upper_lim)
        step = frame_index * store_interval
        ax.set_title(f'Intensity Profile at Propagation Step {step}')

    anim = animation.FuncAnimation(fig, update_plot, frames=len(field_history), fargs=(field_history, ax), interval=100)
    
    try:
        anim.save(output_filename, writer='pillow', fps=10, dpi=100)
        click.echo(f"Animation saved to {output_filename}")
    except Exception as e:
        click.echo(f"Could not save animation: {e}", err=True)
        plt.show()
    plt.close(fig)


def animate_temporal_profile(field_history, sim_params, output_filename):
    """
    Creates and saves an animated GIF of the soliton's temporal profile.
    """
    click.echo(f"Generating temporal animation...")
    fig, ax = plt.subplots(figsize=(8, 6))

    # Reconstruct time axis from sim_params
    pulse_duration_s = sim_params['pulse_duration']
    sim_size_t_s = 10 * pulse_duration_s 
    t_vis = np.linspace(-sim_size_t_s, sim_size_t_s, len(field_history[0])) * 1e15 # convert to fs
    
    ax.set_xlabel('Time (fs)')
    ax.set_ylabel('Intensity (a.u.)')
    max_intensity = max(np.max(frame) for frame in field_history) if field_history else 1.0
    ax.set_ylim(0, max(max_intensity * 1.1, 1e-9))
    ax.set_xlim(t_vis[0], t_vis[-1])

    line, = ax.plot([], [], lw=2)
    title = ax.text(0.5, 1.01, '', transform=ax.transAxes, ha="center", fontsize=12)

    def update(frame_index):
        line.set_data(t_vis, field_history[frame_index])
        step = frame_index * sim_params.get('store_interval', 1)
        title.set_text(f'Temporal Profile at Propagation Step {step}')
        return line, title

    anim = animation.FuncAnimation(fig, update, frames=len(field_history), blit=True, interval=100)
    
    try:
        anim.save(output_filename, writer='pillow', fps=10, dpi=100)
        click.echo(f"Animation saved to {output_filename}")
    except Exception as e:
        click.echo(f"Could not save animation: {e}", err=True)
        # Fallback to showing the plot if saving fails
        plt.show()
    plt.close(fig)

# --- Initial Field Creation ---

def create_single_pulse_field(sim_params):
    """Creates a 3D field grid (x, y, t) with physical units."""
    grid_size = sim_params['grid_size']
    beam_waist_m = sim_params['beam_waist']
    pulse_duration_s = sim_params['pulse_duration']

    # Set grid size to be ~5x the beam waist and ~10x the pulse duration
    sim_size_xy_m = 5 * beam_waist_m
    sim_size_t_s = 10 * pulse_duration_s

    x = np.linspace(-sim_size_xy_m, sim_size_xy_m, grid_size)
    y = np.linspace(-sim_size_xy_m, sim_size_xy_m, grid_size)
    t = np.linspace(-sim_size_t_s, sim_size_t_s, grid_size)

    # Use 'xy' indexing to match FFT conventions
    Y, X, T = np.meshgrid(y, x, t, indexing='ij')
    dx, dy, dt = x[1] - x[0], y[1] - y[0], t[1] - t[0]

    power = sim_params['power']
    effective_area = sim_params['effective_area']

    # Temporal envelope
    pulse_envelope = np.exp(-T**2 / (2 * pulse_duration_s**2))
    # Spatial beam profile
    beam_profile = np.exp(-(X**2 + Y**2) / beam_waist_m**2)

    # Use intensity (W/m²) for correct nonlinear scaling
    peak_intensity = power / effective_area
    initial_field = np.sqrt(peak_intensity) * beam_profile * pulse_envelope
    
    # Update sim_params with physical grid spacings
    sim_params.update({'dx': dx, 'dy': dy, 'dt': dt})
    return initial_field

def create_collision_field(sim_params):
    """Creates a 3D field for two colliding pulses with physical units."""
    grid_size = sim_params['grid_size']
    beam_waist_m = sim_params['beam_waist']
    pulse_duration_s = sim_params['pulse_duration']
    separation = sim_params.get('separation', 10 * beam_waist_m)

    # Set grid size to be large enough for separated beams
    sim_size_xy_m = 3 * separation
    sim_size_t_s = 10 * pulse_duration_s

    x = np.linspace(-sim_size_xy_m, sim_size_xy_m, grid_size)
    y = np.linspace(-sim_size_xy_m, sim_size_xy_m, grid_size)
    t = np.linspace(-sim_size_t_s, sim_size_t_s, grid_size)

    Y, X, T = np.meshgrid(y, x, t, indexing='ij')
    dx, dy, dt = x[1] - x[0], y[1] - y[0], t[1] - t[0]

    k0 = sim_params['k0']
    angle, power, effective_area = (sim_params[k] for k in ['angle', 'power', 'effective_area'])
    phase_b_val = sim_params.get('phase_b', 0.0)

    pulse_envelope = np.exp(-T**2 / (2 * pulse_duration_s**2))
    peak_intensity = power / effective_area
    k_x = k0 * np.sin(angle)

    # Beam 1 (starts left, moves right)
    X1 = X + separation / 2
    beam_profile1 = np.exp(-(X1**2 + Y**2) / beam_waist_m**2)
    E1 = np.sqrt(peak_intensity) * beam_profile1 * pulse_envelope * np.exp(+1j * k_x * X1)

    # Beam 2 (starts right, moves left)
    X2 = X - separation / 2
    beam_profile2 = np.exp(-(X2**2 + Y**2) / beam_waist_m**2)
    phase_exponent_b = -1j * k_x * X2 + 1j * phase_b_val
    phase_factor_b = np.exp(phase_exponent_b)
    E2 = np.sqrt(peak_intensity) * beam_profile2 * pulse_envelope * phase_factor_b

    sim_params.update({'dx': dx, 'dy': dy, 'dt': dt})
    return E1 + E2

def create_gate_field(sim_params):
    """Creates a 3D field for a logic gate with physical units."""
    grid_size = sim_params['grid_size']
    beam_waist_m = sim_params['beam_waist']
    pulse_duration_s = sim_params['pulse_duration']
    separation = sim_params['separation']

    # Set grid size
    sim_size_xy_m = 3 * separation # Ensure grid is large enough for separated beams
    sim_size_t_s = 10 * pulse_duration_s

    x = np.linspace(-sim_size_xy_m, sim_size_xy_m, grid_size)
    y = np.linspace(-sim_size_xy_m, sim_size_xy_m, grid_size)
    t = np.linspace(-sim_size_t_s, sim_size_t_s, grid_size)

    Y, X, T = np.meshgrid(y, x, t, indexing='ij')
    dx, dy, dt = x[1] - x[0], y[1] - y[0], t[1] - t[0]

    k0 = sim_params['k0']
    power, angle, input_a, input_b, effective_area = (sim_params[k] for k in ['power', 'angle', 'input_a', 'input_b', 'effective_area'])
    phase_b_val = sim_params.get('phase_b', 0.0)

    pulse_envelope = np.exp(-T**2 / (2 * pulse_duration_s**2))
    peak_intensity = power / effective_area
    
    # Use physical transverse wavevector
    k_x = k0 * np.sin(angle)

    initial_field = np.zeros_like(X, dtype=complex)
    if input_a == 1:
        X_a = X + separation / 2
        beam_profile_a = np.exp(-(X_a**2 + Y**2) / beam_waist_m**2)
        phase_a = np.exp(+1j * k_x * X_a)
        initial_field += np.sqrt(peak_intensity) * beam_profile_a * pulse_envelope * phase_a
    if input_b == 1:
        X_b = X - separation / 2
        beam_profile_b = np.exp(-(X_b**2 + Y**2) / beam_waist_m**2)
        # Combine phase ramp and relative phase in the exponent before calling np.exp
        phase_exponent_b = -1j * k_x * X_b + 1j * phase_b_val
        phase_factor_b = np.exp(phase_exponent_b)
        initial_field += np.sqrt(peak_intensity) * beam_profile_b * pulse_envelope * phase_factor_b

    sim_params.update({'dx': dx, 'dy': dy, 'dt': dt})
    return initial_field

# --- Realism Check ---

def run_realism_check(sim_params):
    """
    Calculates and prints key physical metrics to ground the simulation.
    """
    click.echo("\n--- Physical Realism Check ---")
    
    h = 6.626e-34; c = 3e8
    
    material = sim_params['material']
    material_props = MATERIALS[material]
    peak_power = sim_params['power']
    pulse_duration = sim_params['pulse_duration']
    effective_area = sim_params['effective_area']
    wavelength = sim_params['wavelength']
    
    peak_intensity = peak_power / effective_area
    pulse_energy = peak_power * (pulse_duration * np.sqrt(2*np.pi))
    fluence = pulse_energy / effective_area
    
    beta_tpa = material_props.get('beta_tpa', 0)
    photon_energy = h * c / wavelength
    
    if beta_tpa > 0 and photon_energy > 0:
        est_carrier_density_m3 = (beta_tpa * peak_intensity**2 / (2 * photon_energy)) * pulse_duration
        est_carrier_density_cm3 = est_carrier_density_m3 / 1e6
    else:
        est_carrier_density_cm3 = 0

    fluence_J_per_cm2 = fluence / 1e4

    click.echo(f"Material: {material}")
    click.echo(f"Peak Intensity: {peak_intensity / 1e13:.2f} GW/cm²")
    click.echo(f"Pulse Energy: {pulse_energy * 1e12:.2f} pJ")
    click.echo(f"Fluence: {fluence_J_per_cm2 * 1000:.2f} mJ/cm²")
    click.echo(f"Est. Peak Carrier Density: {est_carrier_density_cm3:.2e} cm⁻³")

    if material == 'silicon' and est_carrier_density_cm3 > 1e17:
        click.secho("Warning: High estimated carrier density in silicon. "
                    "Free-carrier absorption/dispersion (not modeled) will be significant.", fg='yellow')
    
    if fluence_J_per_cm2 > 0.3:
         click.secho(f"Warning: Fluence is high ({fluence_J_per_cm2:.2f} J/cm²). May approach material damage threshold.", fg='yellow')

    click.echo("------------------------------")


# --- CLI ---

@click.group()
def cli():
    """A unified CLI for soliton simulations."""
    pass

@click.group(name='run')
def run_group():
    """Run different types of soliton simulations."""
    pass

@run_group.command(name='collision')
@click.option('--power', default=7.3e4, type=float, help='Peak power in Watts. Default is ~P_critical for AlGaAs.')
@click.option('--wavelength', default=1.55e-6, type=float, help='Wavelength in meters.')
@click.option('--grid-size', default=128, type=int, help="Grid resolution for X, Y, and T axes.")
@click.option('--num-steps', default=200, type=int, help="Number of propagation steps.")
@click.option('--dz', default=None, type=float, help='Propagation step size in meters.')
@click.option('--separation', default=5e-6, type=float, help='Initial separation between beams in meters.')
@click.option('--angle', default=0.2, type=float, help='Collision angle in radians.')
@click.option('--phase', default=0.0, type=float, help='Relative phase of the second beam in radians.')
@click.option('--pulse-duration', default=50e-15, type=float, help='Duration (std dev) of input pulses in seconds.')
@click.option('--beam-waist', default=1e-6, type=float, help='Beam waist (radius) in meters.')
@click.option('--dispersion', default=-20.0, type=float, help="GVD (β₂) in ps²/km. Use negative for anomalous.")
@click.option('--material', type=click.Choice(MATERIALS.keys()), default='algaas')
@click.option('--output-dir', default='results', type=click.Path())
def run_collision(power, wavelength, grid_size, num_steps, dz, separation, angle, phase, pulse_duration, beam_waist, dispersion, material, output_dir):
    """Simulates the collision of two spatial soliton pulses, saves data, and visualizes."""
    material_props = MATERIALS[material]
    sim_params = {
        'power': power, 'grid_size': grid_size, 'num_steps': num_steps, 'angle': angle,
        'separation': separation, 'phase_b': phase,
        'pulse_duration': pulse_duration, 'beam_waist': beam_waist, 'wavelength': wavelength,
        'dz': dz, 'store_interval': 1, 'n0': material_props['n0'],
        'n2': material_props['n2'], 'material': material, 'effective_area': np.pi * beam_waist**2,
        'dispersion': dispersion
    }

    sim_params.update({'k0': 2 * np.pi / sim_params['wavelength'], 'k': (2 * np.pi / sim_params['wavelength']) * material_props['n0']})

    if dz is None:
        click.echo("Auto-calculating dz...")
        dz_auto = calculate_optimal_dz(sim_params)
        dz_auto = max(1e-8, min(dz_auto, 1e-5)) # Clamp for practical simulation length
        click.echo(f"Auto-calculated dz = {dz_auto:.6e}")
    else:
        dz_auto = dz
        click.echo(f"Using user-specified dz = {dz_auto:.6e}")
    sim_params['dz'] = dz_auto

    report_simulation_regime(sim_params)

    initial_field = create_collision_field(sim_params)

    field_history_full, initial_energy = run_nlse_simulation(initial_field, sim_params)
    
    os.makedirs(output_dir, exist_ok=True)
    filename_base = f"soliton_collision_{material}_P{power:.2e}_GS{grid_size}_N{num_steps}_A{angle:.3f}"
    
    click.echo("Processing animation frames...")
    animation_history = []
    for field in field_history_full:
        # Integrate over time (Z axis) to show spatial (X-Y) beam profile
        # This shows how beams propagate and collide in space
        intensity_spatial = np.sum(np.abs(field)**2, axis=2)
        animation_history.append(intensity_spatial)

    # Save the much smaller, processed data for the animation
    data_filename = os.path.join(output_dir, f"{filename_base}.npz")
    click.echo(f"Saving processed simulation data to {data_filename}...")
    np.savez_compressed(data_filename, animation_history=np.array(animation_history), sim_params=sim_params)
    click.echo("Data saved.")

    anim_filename = os.path.join(output_dir, f"{filename_base}.gif")
    animate_simulation(animation_history, sim_params, anim_filename)

    run_realism_check(sim_params)

def _run_gate_simulation(inputs, power, grid_size, num_steps, dz, separation, angle, pulse_duration, beam_waist, material, output_dir, dispersion, phase_b=0.0, wavelength=1.55e-6):
    """Internal logic for running a single soliton gate simulation."""
    material_props = MATERIALS[material]
    input_a, input_b = int(inputs[0]), int(inputs[2])

    sim_params = {
        'power': power, 'grid_size': grid_size, 'num_steps': num_steps,
        'separation': separation, 'angle': angle, 'input_a': input_a, 'input_b': input_b,
        'pulse_duration': pulse_duration, 'beam_waist': beam_waist, 'wavelength': wavelength,
        'dz': dz, 'store_interval': 1, 'n0': material_props['n0'],
        'n2': material_props['n2'], 'material': material, 'effective_area': np.pi * beam_waist**2,
        'dispersion': dispersion, 'phase_b': phase_b
    }

    sim_params.update({'k0': 2 * np.pi / sim_params['wavelength'], 'k': (2 * np.pi / sim_params['wavelength']) * material_props['n0']})

    if dz is None:
        click.echo("Auto-calculating dz...")
        dz_auto = calculate_optimal_dz(sim_params)
        dz_auto = max(1e-8, min(dz_auto, 1e-5)) # Clamp for practical simulation length
        click.echo(f"Auto-calculated dz = {dz_auto:.6e}")
    else:
        dz_auto = dz
        click.echo(f"Using user-specified dz = {dz_auto:.6e}")
    sim_params['dz'] = dz_auto

    report_simulation_regime(sim_params)

    initial_field = create_gate_field(sim_params)

    field_history_full, initial_energy = run_nlse_simulation(initial_field, sim_params)

    os.makedirs(output_dir, exist_ok=True)
    filename_base = f"soliton_gate_{inputs}_{material}_P{power:.2e}_GS{grid_size}_N{num_steps}_S{separation}_A{angle:.3f}"

    click.echo("Processing animation frames...")
    animation_history = []
    for field in field_history_full:
        # Integrate over time (Z axis) to show spatial (X-Y) beam profile
        intensity_spatial = np.sum(np.abs(field)**2, axis=2)
        animation_history.append(intensity_spatial)

    # Save the much smaller, processed data for the animation
    data_filename = os.path.join(output_dir, f"{filename_base}.npz")
    click.echo(f"Saving processed simulation data to {data_filename}...")
    np.savez_compressed(data_filename, animation_history=np.array(animation_history), sim_params=sim_params)
    click.echo("Data saved.")

    anim_filename = os.path.join(output_dir, f"{filename_base}.gif")
    animate_simulation(animation_history, sim_params, anim_filename)

    run_realism_check(sim_params)

@run_group.command(name='gates')
@click.option('--power', default=7.3e4, type=float, help='Peak power in Watts. Default is ~P_critical for AlGaAs.')
@click.option('--wavelength', default=1.55e-6, type=float, help='Wavelength in meters.')
@click.option('--grid-size', default=64, type=int, help="Grid resolution for X, Y, and Z axes.")
@click.option('--num-steps', default=200, type=int, help="Number of propagation steps.")
@click.option('--dz', default=None, type=float, help='Propagation step size in meters.')
@click.option('--separation', default=5e-6, type=float, help='Spatial separation between input beams in meters.')
@click.option('--angle', default=0.2, type=float, help='Collision angle in radians.')
@click.option('--phase', default=0.0, type=float, help='Relative phase of the second beam in radians.')
@click.option('--pulse-duration', default=50e-15, type=float, help='Duration (std dev) of input pulses in seconds.')
@click.option('--beam-waist', default=1e-6, type=float, help='Beam waist (radius) in meters.')
@click.option('--dispersion', default=0.0, type=float, help="GVD (β₂) in ps²/km. Use negative for anomalous.")
@click.option('--material', type=click.Choice(MATERIALS.keys()), default='algaas')
@click.option('--output-dir', default='results', type=click.Path())
def run_gates(power, wavelength, grid_size, num_steps, dz, separation, angle, phase, pulse_duration, beam_waist, material, output_dir, dispersion):
    """Runs all three gate simulations (1x1, 1x0, 0x0) sequentially."""
    
    all_inputs = ['1x1', '1x0', '0x0']
    
    batch_dir_name = f"sweep_gate_{time.strftime('%Y%m%d-%H%M%S')}"
    batch_dir_path = os.path.join(output_dir, batch_dir_name)
    os.makedirs(batch_dir_path, exist_ok=True)
    click.echo(f"Starting batch run. Results will be in: {batch_dir_path}")

    for inputs in all_inputs:
        click.echo(f"--- Running simulation for inputs: {inputs} ---")
        _run_gate_simulation(
            inputs=inputs,
            power=power,
            grid_size=grid_size,
            num_steps=num_steps,
            dz=dz,
            separation=separation,
            angle=angle,
            pulse_duration=pulse_duration,
            beam_waist=beam_waist,
            material=material,
            output_dir=batch_dir_path,
            dispersion=dispersion,
            phase_b=phase,
            wavelength=wavelength
        )
    
    click.echo("--- All gate simulations completed. ---")

@run_group.command(name='temporal-profile')
@click.option('--power', default=1.0, type=float, help='Peak power in Watts.')
@click.option('--wavelength', default=1.55e-6, type=float, help='Wavelength in meters.')
@click.option('--grid-size', default=256, type=int, help='Grid resolution for time axis.')
@click.option('--num-steps', default=500, type=int, help="Number of propagation steps.")
@click.option('--dz', default=None, type=float, help='Propagation step size in meters.')
@click.option('--pulse-duration', default=50e-15, type=float, help='Duration (std dev) of input pulses in seconds.')
@click.option('--beam-waist', default=1e-6, type=float, help='Beam waist (radius) in meters, used for intensity calculation.')
@click.option('--dispersion', default=-20.0, type=float, help="GVD (β₂) in ps²/km. Negative for anomalous dispersion.")
@click.option('--material', type=click.Choice(MATERIALS.keys()), default='silicon')
@click.option('--output-dir', default='results', type=click.Path())
def run_temporal_profile(power, wavelength, grid_size, num_steps, dz, pulse_duration, beam_waist, dispersion, material, output_dir):
    """Simulates temporal pulse propagation in a waveguide to show dispersion vs. soliton effect."""
    material_props = MATERIALS[material]

    # This command is for temporal effects, so diffraction is disabled.
    disable_diffraction = True
    disable_dispersion = False

    if dz is None:
        # Calculate reasonable dz based on power if not provided
        click.echo("Auto-calculating dz...")
        k0_temp = 2 * np.pi / wavelength
        power_safe = power + 1e-12
        # Simplified dz calculation for temporal case
        dz_auto = 0.1 / (k0_temp * material_props['n2'] * (power_safe / (np.pi * beam_waist**2)))
        dz_auto = max(1e-8, min(dz_auto, 1e-5)) # Clamping for realistic chip-scale steps
        click.echo(f"Auto-calculated dz = {dz_auto:.6e} (for ~0.1 rad nonlinear phase shift/step)")
    else:
        dz_auto = dz
        click.echo(f"Using user-specified dz = {dz_auto:.6e}")

    sim_params = {
        'power': power, 'grid_size': grid_size, 'num_steps': num_steps,
        'pulse_duration': pulse_duration, 'beam_waist': beam_waist, 'wavelength': wavelength,
        'dz': dz_auto, 'store_interval': 10, 'n0': material_props['n0'],
        'n2': material_props['n2'], 'material': material, 'effective_area': np.pi * beam_waist**2,
        'dispersion': dispersion,
        'disable_diffraction': disable_diffraction,
        'disable_dispersion': disable_dispersion
    }
    sim_params.update({'k0': 2 * np.pi / sim_params['wavelength'], 'k': (2 * np.pi / sim_params['wavelength']) * material_props['n0']})

    report_simulation_regime(sim_params)
    initial_field = create_single_pulse_field(sim_params)
    field_history_full, initial_energy = run_nlse_simulation(initial_field, sim_params)
    
    os.makedirs(output_dir, exist_ok=True)
    filename_base = f"temporal_profile_{material}_P{power:.2e}_D{dispersion:.1f}"
    
    click.echo("Processing for temporal animation...")
    animation_history = []
    center_idx = grid_size // 2
    for field in field_history_full:
        # Take a slice at the center of the beam to see the temporal profile
        intensity_temporal = np.abs(field[center_idx, center_idx, :])**2
        animation_history.append(intensity_temporal)

    data_filename = os.path.join(output_dir, f"{filename_base}.npz")
    click.echo(f"Saving processed simulation data to {data_filename}...")
    np.savez_compressed(data_filename, animation_history=np.array(animation_history), sim_params=sim_params)
    click.echo("Data saved.")

    anim_filename = os.path.join(output_dir, f"{filename_base}.gif")
    animate_temporal_profile(animation_history, sim_params, anim_filename)

    run_realism_check(sim_params)


@run_group.command(name='debug-run')
@click.option('--power', default=7.3e4, type=float, help='Peak power in Watts.')
@click.option('--wavelength', default=1.55e-6, type=float, help='Wavelength in meters.')
@click.option('--grid-size', default=64, type=int)
@click.option('--num-steps', default=100, type=int)
@click.option('--dz', default=None, type=float, help='Propagation step size in meters.')
@click.option('--pulse-duration', default=50e-15, type=float, help='Duration (std dev) of input pulses in seconds.')
@click.option('--beam-waist', default=1e-6, type=float, help='Beam waist (radius) in meters.')
@click.option('--dispersion', default=-20.0, type=float, help="GVD (β₂) in ps²/km.")
@click.option('--material', type=click.Choice(MATERIALS.keys()), default='algaas')
@click.option('--disable-diffraction', is_flag=True, help="Turn off spatial diffraction.")
@click.option('--disable-dispersion', is_flag=True, help="Turn off temporal dispersion (GVD).")
@click.option('--output-dir', default='results', type=click.Path())
def debug_run(power, wavelength, grid_size, num_steps, dz, pulse_duration, beam_waist, dispersion, material, disable_diffraction, disable_dispersion, output_dir):
    """Runs a single pulse simulation with options to disable physics for debugging."""
    material_props = MATERIALS[material]

    if dz is None:
        # Calculate reasonable dz based on power if not provided
        click.echo("Auto-calculating dz...")
        k0_temp = 2 * np.pi / wavelength
        power_safe = power + 1e-12
        dz_auto = 0.1 / (k0_temp * material_props['n2'] * (power_safe / (np.pi * beam_waist**2)))
        dz_auto = max(1e-8, min(dz_auto, 1e-5)) # Clamping for realistic chip-scale steps
        click.echo(f"Auto-calculated dz = {dz_auto:.6e} (for ~0.1 rad nonlinear phase shift/step)")
    else:
        dz_auto = dz
        click.echo(f"Using user-specified dz = {dz_auto:.6e}")

    sim_params = {
        'power': power, 'grid_size': grid_size, 'num_steps': num_steps,
        'pulse_duration': pulse_duration, 'beam_waist': beam_waist, 'wavelength': wavelength,
        'dz': dz_auto, 'store_interval': 10, 'n0': material_props['n0'],
        'n2': material_props['n2'], 'material': material, 'effective_area': np.pi * beam_waist**2,
        'dispersion': dispersion,
        'disable_diffraction': disable_diffraction,
        'disable_dispersion': disable_dispersion
    }

    sim_params.update({'k0': 2 * np.pi / sim_params['wavelength'], 'k': (2 * np.pi / sim_params['wavelength']) * material_props['n0']})

    report_simulation_regime(sim_params)

    initial_field = create_single_pulse_field(sim_params)

    field_history_full, initial_energy = run_nlse_simulation(initial_field, sim_params)
    
    os.makedirs(output_dir, exist_ok=True)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename_base = f"debug_run_{material}_P{power:.1f}_D{dispersion:.1f}_diff_{not disable_diffraction}_disp_{not disable_dispersion}_{timestamp}"
    
    click.echo("Processing animation frames...")
    animation_history = []
    for field in field_history_full:
        # Integrate over time (t axis) to show spatial (X-Y) beam profile
        intensity_spatial = np.sum(np.abs(field)**2, axis=2)
        animation_history.append(intensity_spatial)

    data_filename = os.path.join(output_dir, f"{filename_base}.npz")
    click.echo(f"Saving processed simulation data to {data_filename}...")
    np.savez_compressed(data_filename, animation_history=np.array(animation_history), sim_params=sim_params)
    click.echo("Data saved.")

    anim_filename = os.path.join(output_dir, f"{filename_base}.gif")
    animate_simulation(animation_history, sim_params, anim_filename)

    run_realism_check(sim_params)

cli.add_command(run_group)

if __name__ == '__main__':
    cli()
