import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import click
import os
import time

# --- Material Library ---
MATERIALS = {
    'algaas': {'n0': 3.3, 'n2': 1e-17},
    'silica': {'n0': 1.44, 'n2': 2.6e-20},
    'bk7': {'n0': 1.50, 'n2': 3.45e-20},
    'sapphire': {'n0': 1.75, 'n2': 3.0e-20},
    'zns': {'n0': 2.27, 'n2': 7.9e-18},
}

# --- Core Simulation & Visualization Logic ---

def run_nlse_simulation(initial_field, sim_params):
    """
    Solves the 3D NLSE using the split-step Fourier method and returns the history.
    """
    dx, dy, dz_step = sim_params['dx'], sim_params['dy'], sim_params['dz']
    num_steps = sim_params['num_steps']
    k, k0, n2 = sim_params['k'], sim_params['k0'], sim_params['n2']
    store_interval = sim_params.get('store_interval', 5)

    nx, ny, _ = initial_field.shape
    kx = 2 * np.pi * np.fft.fftfreq(nx, d=dx)
    ky = 2 * np.pi * np.fft.fftfreq(ny, d=dy)
    KX, KY = np.meshgrid(kx, ky)
    linear_operator = np.exp(-1j * (KX**2 + KY**2) / (2 * k) * dz_step / 2)

    field = initial_field.copy()
    field_history = [np.abs(field[:, :, field.shape[2] // 2])**2]

    click.echo("Running NLSE simulation...")
    for i in range(num_steps):
        for z_idx in range(field.shape[2]):
            field_slice = field[:, :, z_idx]
            field_k_slice = np.fft.fft2(field_slice) * linear_operator
            field_slice = np.fft.ifft2(field_k_slice)
            field_slice *= np.exp(1j * k0 * n2 * np.abs(field_slice)**2 * dz_step)
            field_k_slice = np.fft.fft2(field_slice) * linear_operator
            field[:, :, z_idx] = np.fft.ifft2(field_k_slice)
        
        if (i + 1) % store_interval == 0:
            field_history.append(np.abs(field[:, :, field.shape[2] // 2])**2)
            click.echo(f"Step {i+1}/{num_steps} completed.")

    return field_history

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

    max_intensity = max(np.max(frame) for frame in field_history) if field_history else 1

    def update_plot(frame_index, field_history, ax):
        ax.clear()
        Z_vis = field_history[frame_index]
        ax.plot_surface(X_vis, Y_vis, Z_vis, cmap='viridis')
        ax.set_xlabel('X'); ax.set_ylabel('Y'); ax.set_zlabel('Intensity')
        ax.set_zlim(0, max_intensity * 1.1)
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

# --- Initial Field Creation ---

def create_collision_field(sim_params):
    grid_size = sim_params['grid_size']
    sim_size = 5.0
    x, y, z = (np.linspace(-sim_size, sim_size, grid_size) for _ in range(3))
    X, Y, Z = np.meshgrid(x, y, z)
    dx, dy = x[1] - x[0], y[1] - y[0]
    
    k_vac = 2 * np.pi / sim_params['wavelength']
    angle, power, n0, beam_waist = (sim_params[k] for k in ['angle', 'power', 'n0', 'beam_waist'])

    E1 = np.sqrt(power) * np.exp(-(X**2 + Y**2) / beam_waist**2) * np.exp(1j * k_vac * n0 * (Z * np.cos(angle) + X * np.sin(angle)))
    E2 = np.sqrt(power) * np.exp(-(X**2 + Y**2) / beam_waist**2) * np.exp(1j * k_vac * n0 * (Z * np.cos(angle) - X * np.sin(angle)))
    
    sim_params.update({'dx': dx, 'dy': dy, 'sim_size_x': sim_size, 'sim_size_y': sim_size})
    return E1 + E2

def create_gate_field(sim_params):
    grid_size = sim_params['grid_size']
    sim_size = 10.0
    x, y, z = (np.linspace(-sim_size, sim_size, grid_size) for _ in range(3))
    X, Y, Z = np.meshgrid(x, y, z)
    dx, dy = x[1] - x[0], y[1] - y[0]

    k_vac = 2 * np.pi / sim_params['wavelength']
    power, n0, beam_waist, separation, angle, input_a, input_b = (sim_params[k] for k in ['power', 'n0', 'beam_waist', 'separation', 'angle', 'input_a', 'input_b'])

    initial_field = np.zeros_like(X, dtype=complex)
    if input_a == 1:
        X_a = X + separation / 2
        initial_field += np.sqrt(power) * np.exp(-(X_a**2 + Y**2) / beam_waist**2) * np.exp(-1j * k_vac * n0 * X_a * np.tan(angle))
    if input_b == 1:
        X_b = X - separation / 2
        initial_field += np.sqrt(power) * np.exp(-(X_b**2 + Y**2) / beam_waist**2) * np.exp(1j * k_vac * n0 * X_b * np.tan(angle))

    sim_params.update({'dx': dx, 'dy': dy, 'sim_size_x': sim_size, 'sim_size_y': sim_size})
    return initial_field

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
@click.option('--power', default=6.87e3, type=float)
@click.option('--grid-size', default=128, type=int)
@click.option('--num-steps', default=500, type=int)
@click.option('--angle', default=0.1, type=float)
@click.option('--material', type=click.Choice(MATERIALS.keys()), default='algaas')
@click.option('--output-dir', default='results', type=click.Path())
def run_collision(power, grid_size, num_steps, angle, material, output_dir):
    """Simulates the collision of two spatial solitons."""
    material_props = MATERIALS[material]
    sim_params = {
        'power': power, 'grid_size': grid_size, 'num_steps': num_steps, 'angle': angle,
        'beam_waist': 1.0, 'wavelength': 1.55, 'dz': 0.1, 'store_interval': 10,
        'n0': material_props['n0'], 'n2': material_props['n2']
    }
    
    initial_field = create_collision_field(sim_params)
    sim_params.update({'k0': 2 * np.pi / sim_params['wavelength']})
    sim_params['k'] = sim_params['k0'] * sim_params['n0']

    field_history = run_nlse_simulation(initial_field, sim_params)
    
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"soliton_collision_{material}_P{power:.2e}_GS{grid_size}_N{num_steps}_A{angle}.gif")
    animate_simulation(field_history, sim_params, filename)

@run_group.command(name='gate')
@click.option('--inputs', default='1x1', type=click.Choice(['1x1', '1x0', '0x0']))
@click.option('--power', default=6.87e3, type=float)
@click.option('--grid-size', default=128, type=int)
@click.option('--num-steps', default=200, type=int)
@click.option('--separation', default=5.0, type=float)
@click.option('--angle', default=-0.1, type=float)
@click.option('--material', type=click.Choice(MATERIALS.keys()), default='algaas')
@click.option('--output-dir', default='results', type=click.Path())
def run_gate(inputs, power, grid_size, num_steps, separation, angle, material, output_dir):
    """Simulates a soliton-based AND gate."""
    material_props = MATERIALS[material]
    input_a, input_b = int(inputs[0]), int(inputs[2])
    sim_params = {
        'power': power, 'grid_size': grid_size, 'num_steps': num_steps,
        'separation': separation, 'angle': angle, 'input_a': input_a, 'input_b': input_b,
        'beam_waist': 1.0, 'wavelength': 1.55, 'dz': 0.2, 'store_interval': 5,
        'n0': material_props['n0'], 'n2': material_props['n2']
    }

    initial_field = create_gate_field(sim_params)
    sim_params.update({'k0': 2 * np.pi / sim_params['wavelength']})
    sim_params['k'] = sim_params['k0'] * sim_params['n0']

    field_history = run_nlse_simulation(initial_field, sim_params)

    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"soliton_gate_{inputs}_{material}_P{power:.2e}_GS{grid_size}_N{num_steps}_S{separation}_A{angle}.gif")
    animate_simulation(field_history, sim_params, filename)

cli.add_command(run_group)

if __name__ == '__main__':
    cli()
