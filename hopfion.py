import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
from skimage.measure import marching_cubes
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.colors as colors
from scipy.ndimage import map_coordinates
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
    'silicon': {'n0': 3.48, 'n2': 6e-18},
    'silicon_nitride': {'n0': 2.0, 'n2': 2.4e-19},
    'inp': {'n0': 3.17, 'n2': 1.5e-17},
    'gaas': {'n0': 3.38, 'n2': 1.5e-17},
    'linbo3': {'n0': 2.14, 'n2': 1.0e-19},
    'diamond': {'n0': 2.39, 'n2': 1.3e-19},
}

# --- Core Simulation Logic ---

def run_vnlse_simulation(initial_field_x, initial_field_y, sim_params):
    """
    Solves the 3D Vector NLSE using a symmetric split-step Fourier method.
    This version is simplified and assumes propagation in z, matching the old script.
    """
    dx, dy, dz_step = sim_params['dx'], sim_params['dy'], sim_params['dz']
    num_steps = sim_params['num_steps']
    k, k0, n2 = sim_params['k'], sim_params['k0'], sim_params['n2']
    store_interval = sim_params.get('store_interval', num_steps)

    nx, ny, _ = initial_field_x.shape
    kx = 2 * np.pi * np.fft.fftfreq(nx, d=dx)
    ky = 2 * np.pi * np.fft.fftfreq(ny, d=dy)
    KX, KY = np.meshgrid(kx, ky)
    linear_operator = np.exp(-1j * (KX**2 + KY**2) / (2 * k) * dz_step / 2)

    field_x, field_y = initial_field_x.copy(), initial_field_y.copy()
    gamma = k0 * n2
    stored_fields = []

    click.echo("Running VNLSE simulation...")
    for i in range(num_steps):
        # Propagate each z-slice
        for z_idx in range(field_x.shape[2]):
            field_x_k_slice = np.fft.fft2(field_x[:, :, z_idx]) * linear_operator
            field_x[:, :, z_idx] = np.fft.ifft2(field_x_k_slice)
            field_y_k_slice = np.fft.fft2(field_y[:, :, z_idx]) * linear_operator
            field_y[:, :, z_idx] = np.fft.ifft2(field_y_k_slice)

        abs_field_x_sq = np.abs(field_x)**2
        abs_field_y_sq = np.abs(field_y)**2
        angle_x, angle_y = np.angle(field_x), np.angle(field_y)
        nonlinear_phase_x = np.exp(1j * gamma * (abs_field_x_sq + (2/3)*abs_field_y_sq + (1/3)*abs_field_y_sq*np.cos(2*angle_y - 2*angle_x)) * dz_step)
        nonlinear_phase_y = np.exp(1j * gamma * (abs_field_y_sq + (2/3)*abs_field_x_sq + (1/3)*abs_field_x_sq*np.cos(2*angle_x - 2*angle_y)) * dz_step)
        field_x *= nonlinear_phase_x
        field_y *= nonlinear_phase_y

        for z_idx in range(field_x.shape[2]):
            field_x_k_slice = np.fft.fft2(field_x[:, :, z_idx]) * linear_operator
            field_x[:, :, z_idx] = np.fft.ifft2(field_x_k_slice)
            field_y_k_slice = np.fft.fft2(field_y[:, :, z_idx]) * linear_operator
            field_y[:, :, z_idx] = np.fft.ifft2(field_y_k_slice)

        if (i + 1) % store_interval == 0:
            stored_fields.append((field_x.copy(), field_y.copy()))
            click.echo(f"Step {i+1}/{num_steps} completed. Storing fields.")

    if not stored_fields:
         stored_fields.append((field_x.copy(), field_y.copy()))

    return stored_fields

# --- Initial Field Creation ---

def create_single_hopfion_field(sim_params):
    grid_size = sim_params['grid_size']
    sim_size = sim_params.get('sim_size', 5.0)
    
    x = np.linspace(-sim_size, sim_size, grid_size)
    y = np.linspace(-sim_size, sim_size, grid_size)
    z = np.linspace(-sim_size, sim_size, grid_size)
    X, Y, Z = np.meshgrid(x, y, z)
    dx, dy = x[1] - x[0], y[1] - y[0]

    u = X + 1j * Y
    v = Z + 1j * sim_params['r_hopfion']
    psi1_raw = u + 1j * v
    psi2_raw = v + 1j * np.conj(u)

    norm = np.sqrt(np.abs(psi1_raw)**2 + np.abs(psi2_raw)**2)
    norm[norm < 1e-9] = 1e-9
    
    amplitude_profile = np.exp(-(X**2 + Y**2) / (2 * sim_params['sigma']**2))
    
    field_x = np.sqrt(sim_params['power']) * (psi1_raw / norm) * amplitude_profile
    field_y = np.sqrt(sim_params['power']) * (psi2_raw / norm) * amplitude_profile
    
    return field_x, field_y, dx, dy

def create_interaction_field(sim_params):
    sim_size = sim_params['sim_size']
    grid_size = sim_params['grid_size']
    x = np.linspace(-sim_size, sim_size, grid_size)
    y = np.linspace(-sim_size, sim_size, grid_size)
    z = np.linspace(-sim_size, sim_size, grid_size)
    X, Y, Z = np.meshgrid(x, y, z)
    grid = (X, Y, Z)
    dx, dy = x[1] - x[0], y[1] - y[0]

    def _create_one(center, velocity, phase):
        x0, y0, z0 = center
        vx, vy = velocity
        X_s, Y_s, Z_s = X - x0, Y - y0, Z - z0
        u, v = X_s + 1j * Y_s, Z_s + 1j * sim_params['r_hopfion']
        psi1, psi2 = u + 1j * v, v + 1j * np.conj(u)
        norm = np.sqrt(np.abs(psi1)**2 + np.abs(psi2)**2)
        norm[norm < 1e-9] = 1e-9
        amp = np.exp(-(X_s**2 + Y_s**2 + Z_s**2) / (2 * sim_params['sigma']**2))
        fx = np.sqrt(sim_params['power']) * (psi1 / norm) * amp * np.exp(1j * (vx*X_s + vy*Y_s + phase))
        fy = np.sqrt(sim_params['power']) * (psi2 / norm) * amp * np.exp(1j * (vx*X_s + vy*Y_s + phase))
        return fx, fy

    h1_x, h1_y = _create_one(sim_params['center1'], sim_params['velocity1'], sim_params['phase1'])
    h2_x, h2_y = _create_one(sim_params['center2'], sim_params['velocity2'], sim_params['phase2'])
    
    return h1_x + h2_x, h1_y + h2_y, dx, dy

# --- Visualization ---

def visualize_and_save(fields, sim_params, filename_prefix):
    field_x, field_y = fields
    grid_size = sim_params['grid_size']
    
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')
    
    total_intensity = np.abs(field_x)**2 + np.abs(field_y)**2
    s3_param = 2 * np.imag(np.conj(field_x) * field_y)
    s3_normalized = s3_param / (total_intensity + 1e-11)
    
    isolevel = total_intensity.max() * sim_params.get('isolevel_fraction', 0.5)
    
    try:
        verts, faces, _, _ = marching_cubes(np.pad(total_intensity, 1), level=isolevel)
        verts -= 1
    except (ValueError, RuntimeError) as e:
        click.echo(f"Marching cubes failed: {e}. Cannot create visualization.", err=True)
        plt.close(fig)
        return

    s3_values_at_verts = map_coordinates(np.pad(s3_normalized, 1), verts.T, order=1)
    face_s3_values = s3_values_at_verts[faces].mean(axis=1)

    cmap = plt.get_cmap('coolwarm')
    norm = colors.Normalize(vmin=face_s3_values.min(), vmax=face_s3_values.max())
    face_colors = cmap(norm(face_s3_values))
    
    mesh = Poly3DCollection(verts[faces], facecolors=face_colors, edgecolor='k', linewidth=0.1, alpha=0.9)
    ax.add_collection3d(mesh)

    ax.set_xlim(0, grid_size); ax.set_ylim(0, grid_size); ax.set_zlim(0, grid_size)
    ax.set_xlabel('X'); ax.set_ylabel('Y'); ax.set_zlabel('Z')
    ax.set_title("3D Hopfion Intensity and Polarization")

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array(face_s3_values)
    cbar = fig.colorbar(sm, shrink=0.6, aspect=20)
    cbar.set_label('Normalized S3 Parameter (Polarization)')

    filename = f"{filename_prefix}_M_{sim_params['material']}_P{sim_params['power']:.2e}_GS{grid_size}.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    click.echo(f"Visualization saved to {filename}")
    plt.close(fig)

# --- CLI ---

@click.group()
def cli():
    """A unified CLI for Hopfion simulations."""
    pass

@click.group(name='run')
def run_group():
    """Run different types of Hopfion simulations."""
    pass

@run_group.command(name='single')
@click.option('--grid-size', default=128, type=int)
@click.option('--power', default=6.87e3, type=float)
@click.option('--num-steps', default=200, type=int)
@click.option('--sigma', default=1.0, type=float)
@click.option('--material', type=click.Choice(MATERIALS.keys()), default='algaas')
@click.option('--output-dir', default='results', type=click.Path())
def run_single(grid_size, power, num_steps, sigma, material, output_dir):
    """Runs a single stationary Hopfion simulation."""
    material_props = MATERIALS[material]
    sim_params = {
        'grid_size': grid_size, 'power': power, 'num_steps': num_steps,
        'sigma': sigma, 'r_hopfion': 1.0, 'wavelength': 1.55, 'dz': 0.1,
        'n0': material_props['n0'], 'n2': material_props['n2'], 'material': material
    }
    
    click.echo(f"Creating initial field for a single hopfion in {material}...")
    initial_field_x, initial_field_y, dx, dy = create_single_hopfion_field(sim_params)
    sim_params.update({'dx': dx, 'dy': dy, 'k0': 2 * np.pi / sim_params['wavelength']})
    sim_params['k'] = sim_params['k0'] * sim_params['n0']

    stored_fields = run_vnlse_simulation(initial_field_x, initial_field_y, sim_params)
    
    os.makedirs(output_dir, exist_ok=True)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename_prefix = os.path.join(output_dir, f"single_hopfion_{timestamp}")
    
    click.echo(f"Saving simulation results...")
    np.savez_compressed(f"{filename_prefix}.npz", stored_fields=np.array(stored_fields, dtype=object), sim_params=sim_params)
    click.echo(f"Results saved to {filename_prefix}.npz")

    click.echo("Visualizing final state...")
    visualize_and_save(stored_fields[-1], sim_params, filename_prefix)

@run_group.command(name='interaction')
@click.option('--grid-size', default=64, type=int)
@click.option('--sim-size', default=10.0, type=float)
@click.option('--power', default=6.87e3, type=float)
@click.option('--num-steps', default=350, type=int)
@click.option('--store-interval', default=10, type=int)
@click.option('--velocity', default=5.0, type=float)
@click.option('--separation', default=10.0, type=float)
@click.option('--phase2', default=np.pi, type=float)
@click.option('--material', type=click.Choice(MATERIALS.keys()), default='algaas')
@click.option('--output-dir', default='results', type=click.Path())
def run_interaction(**kwargs):
    """Runs a two-Hopfion interaction simulation."""
    material_props = MATERIALS[kwargs['material']]
    sim_params = {
        **kwargs, 'r_hopfion': 1.0, 'sigma': 1.0, 'wavelength': 1.55,
        'n0': material_props['n0'], 'n2': material_props['n2'], 'dz': 0.1, 'phase1': 0.0,
    }
    sim_params.update({
        'center1': (-kwargs['separation']/2, 0, 0), 'velocity1': (kwargs['velocity'], 0),
        'center2': (kwargs['separation']/2, 0, 0), 'velocity2': (-kwargs['velocity'], 0)
    })

    click.echo(f"Creating initial field for two hopfions in {kwargs['material']}...")
    initial_field_x, initial_field_y, dx, dy = create_interaction_field(sim_params)
    sim_params.update({'dx': dx, 'dy': dy, 'k0': 2 * np.pi / sim_params['wavelength']})
    sim_params['k'] = sim_params['k0'] * sim_params['n0']

    stored_fields = run_vnlse_simulation(initial_field_x, initial_field_y, sim_params)

    os.makedirs(kwargs['output_dir'], exist_ok=True)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = os.path.join(kwargs['output_dir'], f"hopfion_interaction_{kwargs['material']}_{timestamp}.npz")
    
    click.echo(f"Saving simulation results to {filename}...")
    np.savez_compressed(filename, stored_fields=np.array(stored_fields, dtype=object), sim_params=sim_params)
    click.echo("Results saved.")

cli.add_command(run_group)

if __name__ == '__main__':
    cli()
